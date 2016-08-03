

class ArithmeticError(Exception):
    """Custom exception that stores the arithmetic operation that failed
    """

    def __init__(self, message, operation):
        super(ArithmeticError, self).__init__(message)
        self._operation = operation

    @property
    def operation(self):
        return self._operation
