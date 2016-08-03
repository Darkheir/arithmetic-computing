#!/usr/bin/env python
import logging
import sys

from arithmetic_computing.communication.client_socket import ClientSocket
from arithmetic_computing.communication.communication_error import CommunicationError
from arithmetic_computing.helper.arguments_parser import ArgumentsParser
from arithmetic_computing.helper.timer import Timer

from arithmetic_computing.helper.file_access import FileAccess


class Client(object):

    def __init__(self):
        self._operations = None
        self._calculation_results = None

    def calculate_on_server(self, socket):
        """Send operations to calculate to the server and retrieve the results

        :param socket: Socket to connect to
        :type socket: str
        """
        socket_client = ClientSocket(socket)
        try:
            socket_client.open()
            socket_client.send(self._operations)
            self._calculation_results = socket_client.receive()
        except CommunicationError, comm_error:
            logging.error("Communication error: %s", str(comm_error))
            logging.info("Exiting")
            sys.exit(1)
        finally:
            socket_client.close()

    def load_operations(self, operation_path):
        """Load the operations to perform from the file

        :param operation_path: Path of the operations file
        :type operation_path: str
        """
        try:
            self._operations = FileAccess.read_lines(operation_path)
        except IOError, io_error:
            logging.error("Error reading operations: %s", str(io_error))
            logging.info("Exiting")
            sys.exit(1)

    def write_results(self, result_path):
        """Write the operations results into the given file

        :param result_path: Path of the file we need to write the results to
        :type result_path: str
        """
        try:
            FileAccess.write_lines(result_path, self._calculation_results)
        except IOError, io_error:
            logging.error("Error writing result: %s", str(io_error))
            logging.info("Exiting")
            sys.exit(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    operation_file, result_file, socket_address = ArgumentsParser.parse_client_arguments()

    timer = Timer()
    timer.start()

    client = Client()
    client.load_operations(operation_file)
    client.calculate_on_server(socket_address)
    client.write_results(result_file)

    logging.info("Mathematical duration: %f seconds", timer.time())
