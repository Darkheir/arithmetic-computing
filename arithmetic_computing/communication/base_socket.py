import json
import socket
import os
import logging


class BaseSocket(object):
    """Base class to represent a socket.

    It implements common operations in a very basic way:
     * Send data
     * Receive data

    In this implementation the data is serialized before being sent and deserialized after being received
    The serializer can be specified in the constructor. It must implements 2 methods:
        * dumps to serialize data
        * loads to deserialize data

    To control that all the data has been received a very simple mechanism is used:
    Before sending data we calculate the size of the serialized data to send
    and it is added at the begging of the data. This lets us be sure all the data has been send.

    It doesn't replace a real integrity control nor an authentication of the data.
    """

    def __init__(self, address, buffer_size=4096, serializer=json, sock=socket.socket):
        self._buffer_size = buffer_size
        address = os.path.expanduser(address)
        address = os.path.abspath(address)
        self._address = address
        self._serializer = serializer
        self._socket = sock(socket.AF_UNIX, socket.SOCK_STREAM)
        self._logger = logging.getLogger(__name__)

    @property
    def connection_socket(self):
        raise NotImplementedError("Child classes must implement this method")

    def send(self, data):
        """Send the given data through the socket.

        The data is serialized and the size of the serialized data is
        added at the beginning of the data.

        :param data: Data to send. The data must be serializable.
        :type data: mixed
        """
        data = self._serializer.dumps(data)
        self._logger.debug("Sending string of size %d", len(data))
        data = "%d|%s" % (len(data), data)
        self.connection_socket.sendall(data)

    def receive(self):
        """Receive data through the socket and deserialize it

        :return:
        :rtype:
        """
        data = self.connection_socket.recv(self._buffer_size)
        split = data.split("|")
        expected_size = int(split[0])
        received = split[1]
        while data and len(received) < expected_size:
            data = self.connection_socket.recv(self._buffer_size)
            received += data
        self._logger.debug("Received string of size %d", len(received))
        return self._serializer.loads(received)
