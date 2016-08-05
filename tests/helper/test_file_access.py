from unittest import TestCase
import mock

import arithmetic_computing.helper.file_access as file_access


class TestFileAccess(TestCase):

    @mock.patch('arithmetic_computing.helper.file_access.os.path')
    def test_read_lines_file_not_exists(self, mock_path):
        mock_path.isfile.return_value = False
        with self.assertRaises(IOError):
            file_access.read_lines("test")

    @mock.patch('arithmetic_computing.helper.file_access.open', create=True)
    @mock.patch('arithmetic_computing.helper.file_access.os.path')
    def test_read_lines_empty_file_open_called(self, mock_path, mock_open):
        mock_path.isfile.return_value = True

        fake_path = "/fake/path"
        mock_path.abspath.return_value = fake_path
        mock_path.expanduser.return_value = fake_path

        # Mock the open in the with statement
        file_mock = mock.MagicMock(spec=file)
        mock_open.return_value.__enter__.return_value = file_mock

        # Empty file
        file_mock.read.return_value = ""

        result = file_access.read_lines(fake_path)
        self.assertEqual(result, [])

    @mock.patch('arithmetic_computing.helper.file_access.open', create=True)
    @mock.patch('arithmetic_computing.helper.file_access.os.path')
    def test_read_lines_file_open_called(self, mock_path, mock_open):
        mock_path.isfile.return_value = True

        fake_path = "/fake/path"
        mock_path.abspath.return_value = fake_path
        mock_path.expanduser.return_value = fake_path

        # Mock the open in the with statement
        file_mock = mock.MagicMock(spec=file)
        mock_open.return_value.__enter__.return_value = file_mock

        file_mock.read.return_value = "line_1\nline_2"

        result = file_access.read_lines(fake_path)
        self.assertEqual(result, ['line_1', 'line_2'])

    @mock.patch('arithmetic_computing.helper.file_access.open', create=True)
    def test_writes_lines_empty(self, mock_open):
        # Mock the open in the with statement
        file_mock = mock.MagicMock(spec=file)
        mock_open.return_value.__enter__.return_value = file_mock

        path = "fake/path"
        file_access.write_lines(path, [])
        file_mock.write.assert_called_with('\n')

    @mock.patch('arithmetic_computing.helper.file_access.open', create=True)
    def test_writes_lines(self, mock_open):
        # Mock the open in the with statement
        file_mock = mock.MagicMock(spec=file)
        mock_open.return_value.__enter__.return_value = file_mock

        path = "fake/path"
        file_access.write_lines(path, ['line_1', 'line_2'])
        file_mock.write.assert_called_with('line_1\nline_2\n')
