"""Callback for arithmetic operations of list of strings
"""
import logging

from arithmetic_computing.arithmetic.string_arithmetic_error\
    import StringArithmeticError
from arithmetic_computing.arithmetic.string_arithmetic \
    import StringArithmetic


class ListArithmeticCallback(object):
    """Callback that takes as a parameter a list of strings to calculate

    It returns the list of results as strings.

    In case of the arithmetic calculus failed error(operation_str)
    is added to the results list in place of the real result
    where "operation_str" is the operation that failed
    """

    def __init__(self, calculator=StringArithmetic()):
        self._calculator = calculator
        self._logger = logging.getLogger(__name__)

    def __call__(self, operations):
        """Perform the calculations

        :param operations:List of operations to calculate
        :type operations: list[str]
        :return: List of results
        :rtype: list[str]
        """
        results = []
        for operation in operations:
            try:
                result = str(self._calculator.calculate(operation))
            except StringArithmeticError, error:
                self._logger.warning(error.message)
                # Silently add "error(operation_str)" in place of the result
                result = "error(%s)" % error.operation
            results.append(result)
        return results
