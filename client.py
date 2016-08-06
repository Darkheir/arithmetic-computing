#!/usr/bin/env python
import logging
import sys

from arithmetic_computing.communication.client_socket import ClientSocket
from arithmetic_computing.communication.communication_error \
    import CommunicationError
from arithmetic_computing.helper.arguments_parser import parse_client_arguments
from arithmetic_computing.helper.timer import Timer

from arithmetic_computing.helper.file_access import read_lines, write_lines


class Client(object):

    def __init__(self, client_sock):
        self._operations = None
        self._calculation_results = []
        self._client_socket = client_sock

    def calculate_on_server(self):
        """Send operations to calculate to the server and retrieve the results
        """
        socket_client = self._client_socket
        try:
            socket_client.open()
            socket_client.send(self._operations)
            self._calculation_results = socket_client.receive()
        except CommunicationError, comm_error:
            logging.error("Communication error: %s", str(comm_error))
            raise
        finally:
            socket_client.close()

    def load_operations(self, operation_path):
        """Load the operations to perform from the file

        :param operation_path: Path of the operations file
        :type operation_path: str
        """
        try:
            self._operations = read_lines(operation_path)
        except IOError, io_error:
            logging.error("Error reading operations: %s", str(io_error))
            raise

    def write_results(self, result_path):
        """Write the operations results into the given file

        :param result_path: Path of the file we need to write the results to
        :type result_path: str
        """
        try:
            write_lines(result_path, self._calculation_results)
        except IOError, io_error:
            logging.error("Error writing result: %s", str(io_error))
            raise


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    operation_file, result_file, socket_address = parse_client_arguments()

    timer = Timer()
    timer.start()

    client_socket = ClientSocket(socket_address)
    client = Client(client_socket)
    try:
        client.load_operations(operation_file)
        client.calculate_on_server()
        client.write_results(result_file)
    except Exception:
        logging.info("Exiting")
        sys.exit(1)

    logging.info("Mathematical duration: %f seconds", timer.time())
