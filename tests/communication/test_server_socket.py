from unittest import TestCase
from functools import wraps
from multiprocessing import Process

import mock

from arithmetic_computing.communication.server_socket import ServerSocket
from arithmetic_computing.communication.communication_error import CommunicationError


class TestServerSocket(TestCase):
    """
    Test class for the server socket.

    Private methods are tested since an infinite loop make the test of the whole chain difficult
    """

    def setUp(self):
        self._address = "address"
        self._mock_serializer = mock.Mock()
        self._socket = ServerSocket(self._address, serializer=self._mock_serializer)

    @mock.patch('arithmetic_computing.communication.server_socket.os')
    @mock.patch('arithmetic_computing.communication.base_socket.os.path')
    def test_unlink_socket_success(self, mock_path, mock_os):
        # Ignore the expanduser and abspath because its user environment dependant
        mock_path.expanduser.return_value = self._address
        mock_path.abspath.return_value = self._address

        # Create the socket here so we can patch expanduser and abspath
        socket = ServerSocket(self._address, serializer=self._mock_serializer)

        mock_os.unlink.return_value = True

        socket._unlink_socket()

        mock_os.unlink.assert_called_with(self._address)

    @mock.patch('arithmetic_computing.communication.server_socket.os')
    def test_unlink_socket_error(self, mock_os):
        mock_os.unlink.side_effect = OSError()

        with self.assertRaises(CommunicationError):
            self._socket._unlink_socket()

    @mock.patch('arithmetic_computing.communication.base_socket.BaseSocket.receive')
    @mock.patch('arithmetic_computing.communication.base_socket.BaseSocket.send')
    def test_handle_connection_callback_called(self, mock_send, mock_receive):
        mock_receive.return_value = "Fake Data"
        callback = mock.Mock()

        self._socket._handle_connection(callback)

        callback.assert_called_with("Fake Data")

    @mock.patch('arithmetic_computing.communication.base_socket.BaseSocket.receive')
    @mock.patch('arithmetic_computing.communication.base_socket.BaseSocket.send')
    def test_handle_connection_send_not_called(self, mock_send, mock_receive):
        mock_receive.return_value = "Fake Data"
        callback = mock.Mock()
        callback.return_value = None

        self._socket._handle_connection(callback)

        mock_send.assert_not_called()

    @mock.patch('arithmetic_computing.communication.base_socket.BaseSocket.receive')
    @mock.patch('arithmetic_computing.communication.base_socket.BaseSocket.send')
    def test_handle_connection_send_called(self, mock_send, mock_receive):
        mock_receive.return_value = "Fake Data"
        mock_send.return_value = True
        callback = mock.Mock()
        callback.return_value = "Fake callback"

        self._socket._handle_connection(callback)

        mock_send.assert_called_with("Fake callback")


    @mock.patch('arithmetic_computing.communication.base_socket.BaseSocket.receive')
    @mock.patch('arithmetic_computing.communication.base_socket.BaseSocket.send')
    def test_wait_for_connection_close_connection_called(self, mock_send, mock_receive):
        mock_socket = mock.Mock()
        mock_connection_socket = mock.Mock()
        mock_socket.accept.return_value = (mock_connection_socket, None)
        self._socket._socket = mock_socket

        callback = mock.Mock()
        self._socket._wait_for_connection(callback)

        mock_connection_socket.close.assert_called_with()

    @mock.patch('arithmetic_computing.communication.server_socket.ServerSocket._wait_for_connection_loop')
    @mock.patch('arithmetic_computing.communication.server_socket.os')
    def test_serve_loop_called(self, mock_os, mock_wait_loop):
        # Exceptionally we patch a private method of the class
        # because it launches an infinite loop
        self._socket._socket = mock.Mock()
        callback = mock.Mock()

        self._socket.serve(callback)

        mock_wait_loop.assert_called_with(callback)

    @mock.patch('arithmetic_computing.communication.server_socket.ServerSocket._wait_for_connection_loop')
    @mock.patch('arithmetic_computing.communication.server_socket.os')
    def test_serve_socket_close_called(self, mock_os, mock_wait_loop):
        # Exceptionally we patch a private method of the class
        # because it launches an infinite loop
        mock_socket = mock.Mock()
        self._socket._socket = mock_socket
        callback = mock.Mock()

        self._socket.serve(callback)

        mock_socket.close.assert_called_with()

    def test_connection_socket(self):
        sock = self._socket.connection_socket
        self.assertIsInstance(sock, None)