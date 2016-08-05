from unittest import TestCase

import mock

from arithmetic_computing.communication.base_socket import BaseSocket


class TestBaseSocket(TestCase):

    def setUp(self):
        self._mock_serializer = mock.Mock()
        self._socket = BaseSocket("address", serializer=self._mock_serializer)

    @mock.patch("arithmetic_computing.communication.base_socket.BaseSocket.connection_socket")
    def test_send_serializer_called(self, mock_connection):
        # We patch connection to avoid the raise NotImplementedError
        self._mock_serializer.dumps.return_value = "dumped_data"

        data = "data"
        self._socket.send(data)

        self._mock_serializer.dumps.assert_called_with(data)

    @mock.patch("arithmetic_computing.communication.base_socket.BaseSocket.connection_socket")
    def test_send_sendall_called(self, mock_connection):
        dumped = "dumped_data"
        self._mock_serializer.dumps.return_value = dumped

        data = "data"
        self._socket.send(data)

        expected = "%d|%s" % (len(dumped), dumped)
        mock_connection.sendall.assert_called_with(expected)

    @mock.patch("arithmetic_computing.communication.base_socket.BaseSocket.connection_socket")
    def test_receive_call_serializer(self, mock_connection):
        # Simulate chunks of data, None to mark the end
        mock_connection.recv.side_effect = ["11|du", "mped_", "data", "Not called"]

        self._socket.receive()

        self._mock_serializer.loads.assert_called_with("dumped_data")

    @mock.patch("arithmetic_computing.communication.base_socket.BaseSocket.connection_socket")
    def test_receive_call(self, mock_connection):
        # Simulate chunks of data, None to mark the end
        mock_connection.recv.side_effect = ["11|du", "mped_", "data", "Not called"]
        self._mock_serializer.loads.return_value = "data"

        result = self._socket.receive()

        self.assertEqual(result, "data")