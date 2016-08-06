from unittest import TestCase

import mock

from arithmetic_computing.arithmetic.string_arithmetic import StringArithmetic
from arithmetic_computing.arithmetic.list_arithmetic_callback import ListArithmeticCallback
from arithmetic_computing.arithmetic.string_arithmetic_error import StringArithmeticError


class TestListArithmeticCallback(TestCase):

    def setUp(self):
        self._mock_calculator = mock.Mock(spec=StringArithmetic)
        self._list_callback = ListArithmeticCallback(self._mock_calculator)

    def test_call_empty(self):
        result = self._list_callback([])
        self.assertEqual(result, [])

    def test_call_error(self):
        self._mock_calculator.calculate.side_effect = StringArithmeticError("Message", "error_operation")
        result = self._list_callback(['will fail'])
        self.assertEqual(result, ["error(error_operation)"])

    def test_call(self):
        self._mock_calculator.calculate.side_effect = [5, 1.5, StringArithmeticError("Message", "error_operation")]
        result = self._list_callback(['3 + 2 ', '3 / 2', 'error'])
        expected = ["5", "1.5", "error(error_operation)"]
        self.assertEqual(result, expected)
