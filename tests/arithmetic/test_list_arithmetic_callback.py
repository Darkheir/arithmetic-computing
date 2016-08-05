from unittest import TestCase

import mock

from arithmetic_computing.arithmetic.string_arithmetic import StringArithmetic
from arithmetic_computing.arithmetic.list_arithmetic_callback import ListArithmeticCallback
from arithmetic_computing.arithmetic.arithmetic_error import ArithmeticError


class TestListArithmeticCallback(TestCase):

    def setUp(self):
        self._mock = mock.Mock(spec=StringArithmetic)
        self._list_callback = ListArithmeticCallback(self._mock)

    def test_call_empty(self):
        result = self._list_callback([])
        self.assertEqual(result, [])

    def test_call_error(self):
        self._mock.calculate.side_effect = ArithmeticError("Message", "error_operation")
        result = self._list_callback(['will fail'])
        self.assertEqual(result, ["error(error_operation)"])

    def test_call(self):
        self._mock.calculate.side_effect = [5, 1.5, ArithmeticError("Message", "error_operation")]
        result = self._list_callback(['3 + 2 ', '3 / 2', 'error'])
        expected = ["5", "1.5", "error(error_operation)"]
        self.assertEqual(result, expected)
