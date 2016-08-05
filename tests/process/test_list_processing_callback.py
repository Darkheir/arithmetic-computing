from unittest import TestCase

import mock

from arithmetic_computing.process.list_processing_callback import ListProcessingCallback


class TestListProcessingCallback(TestCase):

    def setUp(self):
        self._mock_callback = mock.Mock()

    def test_split_list_in_1(self):
        list_callback = ListProcessingCallback(self._mock_callback, 1)
        to_split = range(1, 4)

        result = list_callback._split_list(to_split)

        self.assertEqual(result, [to_split])

    def test_split_list_in_n(self):
        list_callback = ListProcessingCallback(self._mock_callback, 2)
        to_split = range(1, 4)

        result = list_callback._split_list(to_split)

        self.assertEqual(result, [[1], [2, 3]])

    def test__compute_process_callback_called(self):
        connection = mock.Mock()
        data = ["data"]

        list_callback = ListProcessingCallback(self._mock_callback, 2)
        list_callback._compute_process(data, connection)

        self._mock_callback.assert_called_with(data)

    def test__compute_process_send_called(self):
        connection = mock.Mock()
        data = ["data"]

        returned = "Fake returned value"
        self._mock_callback.return_value = returned

        list_callback = ListProcessingCallback(self._mock_callback, 2)
        list_callback._compute_process(data, connection)

        connection.send.assert_called_with(returned)

    def test_get_results(self):
        mock_connection_1 = mock.Mock()
        mock_process_1 = mock.Mock()
        mock_connection_1.recv.return_value = range(1, 4)

        mock_connection_2 = mock.Mock()
        mock_process_2 = mock.Mock()
        mock_connection_2.recv.return_value = range(4, 7)
        processes = [
            (mock_process_1, mock_connection_1),
            (mock_process_2, mock_connection_2),
        ]

        list_callback = ListProcessingCallback(None, 2)
        results = list_callback._get_results(processes)

        self.assertEqual(results, range(1, 7))

    @mock.patch("arithmetic_computing.process.list_processing_callback.Pipe")
    @mock.patch("arithmetic_computing.process.list_processing_callback.Process")
    def test_launch_processes_created(self, mock_process, mock_pipe):
        # List of 2 list to create 2 processes
        data_input = [[], []]

        # Mock the Pipe object
        parent_conn = mock.Mock()
        child_conn = mock.Mock()
        mock_pipe.return_value = (parent_conn, child_conn)

        list_callback = ListProcessingCallback(None, 2)
        list_callback._launch(data_input)

        # Check the process constructor has been called
        mock_process.assert_called_with(target=list_callback._compute_process, args=([], child_conn,))

    @mock.patch("arithmetic_computing.process.list_processing_callback.Pipe")
    @mock.patch("arithmetic_computing.process.list_processing_callback.Process")
    def test_launch_return_value(self, mock_process, mock_pipe):
        data_input = [[]]

        # Mock the Pipe object
        parent_conn = mock.Mock()
        child_conn = mock.Mock()
        mock_pipe.return_value = (parent_conn, child_conn)

        # Mock the Process object
        process = mock.Mock()
        mock_process.return_value = process

        list_callback = ListProcessingCallback(None, 2)
        result = list_callback._launch(data_input)

        # Check the process and connection are returned
        self.assertEqual(result, [(process, parent_conn)])

    @mock.patch("arithmetic_computing.process.list_processing_callback.Pipe")
    @mock.patch("arithmetic_computing.process.list_processing_callback.Process")
    def test_call(self, mock_process, mock_pipe):
        list_callback = ListProcessingCallback(self._mock_callback, 2)
        data = [1, 2, 3]

        # Fake creation of the pipe
        parent_conn = mock.Mock()
        child_conn = mock.Mock()
        mock_pipe.return_value = (parent_conn, child_conn)

        # Fake creation of the process
        process = mock.Mock()
        mock_process.return_value = process

        # What the pipe returns
        parent_conn.recv.side_effect = [range(1, 4), range(4, 7)]

        result = list_callback(data)

        self.assertEqual(result, range(1, 7))
