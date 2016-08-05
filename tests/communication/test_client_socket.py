from unittest import TestCase
from socket import error as SocketError

import mock

from arithmetic_computing.communication.client_socket import ClientSocket
from arithmetic_computing.communication.communication_error import CommunicationError

class TestClientSocket(TestCase):

    def setUp(self):
        self._address = "address"
        self._mock_serializer = mock.Mock()
        self._socket = ClientSocket(self._address, serializer=self._mock_serializer)

    @mock.patch("arithmetic_computing.communication.client_socket.ClientSocket.connection_socket")
    def test_already_open(self, mock_connection):
        self._socket._connection_open = True
        self._socket.open()

        mock_connection.connect.assert_not_called()

    @mock.patch('arithmetic_computing.communication.base_socket.os.path')
    @mock.patch("arithmetic_computing.communication.client_socket.ClientSocket.connection_socket")
    def test_open_connect_called(self, mock_connection, mock_path):
        # Ignore the expanduser and abspath because its user environment dependant
        mock_path.expanduser.return_value = self._address
        mock_path.abspath.return_value = self._address

        socket = ClientSocket(self._address, serializer=self._mock_serializer)
        socket.open()

        mock_connection.connect.assert_called_with('address')

    @mock.patch('arithmetic_computing.communication.base_socket.os.path')
    @mock.patch("arithmetic_computing.communication.client_socket.ClientSocket.connection_socket")
    def test_open_connection_error(self, mock_connection, mock_path):
        # raise exception
        mock_connection.connect.side_effect = SocketError()

        with self.assertRaises(CommunicationError):
            self._socket.open()

    @mock.patch("arithmetic_computing.communication.client_socket.ClientSocket.connection_socket")
    def test_already_closed(self, mock_connection):
        self._socket.close()

        mock_connection.close.assert_not_called()

    @mock.patch("arithmetic_computing.communication.client_socket.ClientSocket.connection_socket")
    def test_close_called(self, mock_connection):
        self._socket._connection_open = True

        self._socket.close()

        mock_connection.close.assert_called_with()

