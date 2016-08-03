import logging
from multiprocessing import Process, Pipe


class ListProcessingCallback(object):
    """Class that will process the content of a list by splitting it in several sub lists.

    Each sub list will be executed in a different process

    The result of the process will also be a list
    """

    def __init__(self, callback, processes_number=1):
        """
        :param callback: Callback to apply for each sub list
        :type callback: mixed
        :param processes_number: Number of processes to launch
        :type processes_number: int
        """
        self._processes_number = processes_number
        self._callback = callback
        self._logger = logging.getLogger(__name__)

    def __call__(self, data):
        """Perform the actual processing

        :param data: Data to process
        :type data: list
        :return: Result
        :rtype: list
        """
        self._logger.info("Processing list of %d elements", len(data))
        lists = self._split_list(data)
        # Launch processes
        processes = self._launch(lists)
        # return process results
        results = self._get_results(processes)
        self._logger.info("List processed")
        return results

    def _launch(self, lists):
        """Creates and launches processes

        :param lists: Lists to pass as param to each created process
        :type lists: list[list]
        :return: List of launched processes and the associated communication
        :rtype: list[tuple]
        """
        processes = []
        for data_list in lists:
            parent_connection, child_connection = Pipe()
            process = Process(target=self._compute_process, args=(data_list, child_connection,))
            process.start()
            self._logger.debug("Process started. PID: %d", process.pid)
            processes.append((process, parent_connection))
        return processes

    def _get_results(self, processes):
        """Get execution result from each process

        :param processes: List of processes
        :type processes: list[tuple]
        :return: Computed result
        :rtype: list
        """
        result = []
        # Get results from processes
        for process, connection in processes:
            result.extend(connection.recv())
            # Wait for the process to terminate
            process.join()
            self._logger.debug("Process with PID %d has finished", process.pid)
        return result

    def _split_list(self, list_to_split):
        """Split a list into n parts, n being the number of processes that will later be created

        :param list_to_split: List to split
        :type list_to_split: list
        :return: List of n lists
        :rtype: list[list]
        """
        length = len(list_to_split)
        lists = []
        self._logger.debug("Splitting list into %d part(s)", self._processes_number)
        for i in range(self._processes_number):
            start = i * length // self._processes_number
            end = (i + 1) * length // self._processes_number
            split = list_to_split[start:end]
            lists.append(split)
        return lists

    def _compute_process(self, data, connection):
        """Represents the process computation.

        Each launched process will perform those operations

        :param data: Data to process
        :type data: list
        :param connection: Connection to send back data to parent process
        :type connection: process.communication
        """
        result = self._callback(data)
        connection.send(result)
        connection.close()
