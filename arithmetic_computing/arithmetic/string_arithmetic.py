import ast
import operator as op

from arithmetic_computing.arithmetic.arithmetic_error import ArithmeticError


class StringArithmetic(object):
    """The StringArithmetic class lets us perform mathematical operation from a string.
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
        try:
            body = ast.parse(expr, mode='eval').body
            return self._calculate(body)
        except (TypeError, SyntaxError):
            raise ArithmeticError("Can't calculate %s" % expr, expr)
    
    def _calculate(self, node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            return self._operators[type(node.op)](self._calculate(node.left), self._calculate(node.right))
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            return self._operators[type(node.op)](self._calculate(node.operand))
        else:
            raise TypeError(node)
