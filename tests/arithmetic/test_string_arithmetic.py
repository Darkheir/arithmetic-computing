from unittest import TestCase

from arithmetic_computing.arithmetic.string_arithmetic import StringArithmetic
from arithmetic_computing.arithmetic.arithmetic_error import ArithmeticError


class TestStringArithmetic(TestCase):

    def setUp(self):
        self._string_arithmetic = StringArithmetic()

    def test_calculate_bad_expression(self):
        with self.assertRaises(ArithmeticError):
            self._string_arithmetic.calculate("nothing good")

    def test_calculate_simple_addition(self):
        result = self._string_arithmetic.calculate("6 + 7")
        self.assertEqual(result, 13)

    def test_calculate_simple_subtraction(self):
        result = self._string_arithmetic.calculate("6 - 7")
        self.assertEqual(result, -1)

    def test_calculate_simple_division(self):
        result = self._string_arithmetic.calculate("6 / 7")
        expected = float(6)/7
        self.assertEqual(result, expected)

    def test_calculate_simple_multiplication(self):
        result = self._string_arithmetic.calculate("6 * 7")
        expected = 6 * 7
        self.assertEqual(result, expected)

    def test_calculate_big_operation(self):
        result = self._string_arithmetic.calculate("6 + 7 / 5 - 12")
        expected = 6 + (float(7) / 5) - 12
        self.assertEqual(result, expected)

    def test_calculate_division_by_zero(self):
        with self.assertRaises(ArithmeticError):
            self._string_arithmetic.calculate("5 / 0")

    def test_calculate_invalid_operation(self):
        with self.assertRaises(ArithmeticError):
            print self._string_arithmetic.calculate("6 + 5 + p")
