from unittest import TestCase

import mock

from arithmetic_computing.helper.timer import Timer


class TestTimer(TestCase):

    def setUp(self):
        self._timer = Timer()

    def test_start(self):
        self._timer.start()
        self.assertIsNotNone(self._timer._start)

    def test_reset(self):
        self._timer._start = 1000
        self._timer.reset()
        self.assertIsNone(self._timer._start)

    def test_time_not_started(self):
        result = self._timer.time()
        self.assertEqual(result, float(0))

    @mock.patch('arithmetic_computing.helper.timer.time')
    def test_time(self, mock_time):
        mock_time.time.return_value = 1  # _get_current_time will return 1000
        self._timer.start()

        mock_time.time.return_value = 10  # _get_current_time will return 10000
        result = self._timer.time()
        self.assertEqual(result, float(10-1))
