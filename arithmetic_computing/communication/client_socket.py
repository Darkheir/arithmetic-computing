"""Client part of socket communication
"""
import json
import socket

from arithmetic_computing.communication.base_socket import BaseSocket
from arithmetic_computing.communication.communication_error \
    import CommunicationError


class ClientSocket(BaseSocket):
    """Class that represents the client in a socket communication.

    """

    def __init__(self, address, buffer_size=4096, serializer=json):
        super(ClientSocket, self).__init__(address, buffer_size, serializer)
        self._connection_open = False

    @property
    def connection_socket(self):
        """In client communication there is only one socket
         so we return the base one

        :return: Socket
        :rtype: socket.socket
        """
        return self._socket

    def open(self):
        """Open the socket communication
        """
        if self._connection_open:
            return

        try:
            self.connection_socket.connect(self._address)
            self._connection_open = True
        except socket.error, error:
            error_message = "Can't connect to the server, %s" % str(error)
            raise CommunicationError(error_message)

    def close(self):
        """Close the communication
        """
        if not self._connection_open:
            return
        self.connection_socket.close()
        self._connection_open = False
