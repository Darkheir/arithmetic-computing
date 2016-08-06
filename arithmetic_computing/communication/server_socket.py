import json
import logging
import os

from arithmetic_computing.communication.base_socket import BaseSocket
from arithmetic_computing.communication.communication_error import CommunicationError


class ServerSocket(BaseSocket):
    """Class to represent a server in a socket communication.

    The main method is "serve" and will run the server
    """

    def __init__(self, address, buffer_size=4096, serializer=json):
        super(ServerSocket, self).__init__(address, buffer_size, serializer)
        self._connection_socket = None
        self._logger = logging.getLogger(__name__)

    @property
    def connection_socket(self):
        """In server communication the communication socket is the one we get from "accept" method

        :return: Socket
        :rtype: socket.socket
        """
        return self._connection_socket

    def serve(self, received_callback):
        """Wait for a client to connect.

        When a client is connected it will:
            * receive data from it,
            * call the callback method with the received data as a parameter
            * send back the returned value.

        The callback must have one parameter, the data received and return a serializable value

        :param received_callback: Callback to call when the server received data
        :type received_callback: mixed
        """
        self._unlink_socket()
        self._socket.bind(self._address)

        self._logger.info('Listening on %s', self._address)
        self._socket.listen(1)
        try:
            self._wait_for_connection_loop(received_callback)
        finally:
            self._logger.debug("Closing main socket")
            self._socket.close()

    def _unlink_socket(self):
        """Remove the socket so it can be used again

        If the socket is not removable an exception is raised.
        """
        try:
            os.unlink(self._address)
        except OSError:
            if os.path.exists(self._address):
                raise CommunicationError("Socket address already exists and is not removable")

    def _wait_for_connection_loop(self, callback):
        """Infinite loop to serve client requests.

        The infinite loop has been split in its own method so we still can test the rest

        :param callback: Callback to call when the server received data
        :type callback: mixed
        """
        while True:
            self._wait_for_connection(callback)

    def _wait_for_connection(self, callback):
        """Wait for a communication and calls _handle_connection
        once a link has been established

        :param callback: Callback to call when the server received data
        :type callback: mixed
        """
        self._logger.info('Waiting for a connection ...')
        self._connection_socket, client_address = self._socket.accept()
        self._logger.info('Connection received')
        try:
            self._handle_connection(callback)
        finally:
            # Clean up the communication
            self._connection_socket.close()
            self._connection_socket = None
            self._logger.info("End of communication")

    def _handle_connection(self, callback):
        """Handle a communication, it will:
            * Receive data from the client
            * Call the callback with the received data and get the returned value
            * Send back the returned data if there are any

        :param callback: Callback to call when the server received data
        :type callback: mixed
        """
        data = self.receive()
        self._logger.debug('Data received')

        self._logger.debug("Calling the callback")
        result = callback(data)
        self._logger.debug('Callback returned')

        if result is not None:
            self._logger.debug('Sending back data from callback')
            self.send(result)
