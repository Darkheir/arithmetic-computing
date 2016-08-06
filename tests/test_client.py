from unittest import TestCase

import mock

from client import Client
from arithmetic_computing.communication.communication_error import CommunicationError


class TestClient(TestCase):

    def setUp(self):
        self._mock_client_socket = mock.Mock()
        self._client = Client(self._mock_client_socket)

    @mock.patch("client.read_lines")
    def test_load_operations(self, mock_read_lines):
        self._client.load_operations("fake/path")
        mock_read_lines.assert_called_with("fake/path")

    @mock.patch("client.read_lines")
    def test_load_operations_error(self, mock_read_lines):
        mock_read_lines.side_effect = IOError()
        with self.assertRaises(IOError):
            self._client.load_operations("fake/path")

    @mock.patch("client.write_lines")
    def test_write_results(self, mock_write_lines):
        self._client._calculation_results = []
        self._client.write_results("fake/path")
        mock_write_lines.assert_called_with("fake/path", [])

    @mock.patch("client.write_lines")
    def test_write_results(self, mock_write_lines):
        mock_write_lines.side_effect = IOError()
        with self.assertRaises(IOError):
            self._client.write_results("fake/path")

    def test_calculate_on_server_data_sent(self):
        self._client._operations = []
        self._client.calculate_on_server()
        self._mock_client_socket.send.assert_called_with([])

    def test_calculate_on_server_socket_closed(self):
        self._client._operations = []
        self._client.calculate_on_server()
        self._mock_client_socket.close.assert_called_with()

    def test_calculate_on_server_error(self):
        self._mock_client_socket.receive.side_effect = CommunicationError()
        with self.assertRaises(CommunicationError):
            self._client.calculate_on_server()

    def test_calculate_on_server_error_socket_closed(self):
        self._mock_client_socket.receive.side_effect = CommunicationError()
        try:
            self._client.calculate_on_server()
        except CommunicationError:
            pass
        self._mock_client_socket.close.assert_called_with()