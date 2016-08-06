"""Perform arithmetic operations from strings
"""
import ast
import operator as op

from arithmetic_computing.arithmetic.string_arithmetic_error \
    import StringArithmeticError


class StringArithmetic(object):
    """The StringArithmetic class lets us perform
    mathematical operations from a string.
    """

    def __init__(self):
        # supported operators
        self._operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Pow: op.pow,
            ast.BitXor: op.xor,
            ast.USub: op.neg
        }

    def calculate(self, expr):
        """Calculate arithmetic operations contained in the given string

        :param expr: String to calculate
        :type expr: str
        :return: result of the arithmetic operation
        :rtype: mixed
        """
        try:
            body = ast.parse(expr, mode='eval').body
            return self._calculate(body)
        except (TypeError, SyntaxError, ZeroDivisionError):
            raise StringArithmeticError("Can't calculate %s" % expr, expr)

    def _calculate(self, node):
        """Calculate the node value depending on its type

        :param node: Node to process
        :type node: ast.AST
        :return: Result
        :rtype: mixed
        """
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            return self._operators[type(node.op)](
                self._calculate(node.left),
                self._calculate(node.right)
            )
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            return self._operators[type(node.op)](self._calculate(node.operand))
        else:
            raise TypeError(node)
