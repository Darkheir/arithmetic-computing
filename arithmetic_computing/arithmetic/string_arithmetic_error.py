

class StringArithmeticError(ArithmeticError):
    """Custom exception that stores the arithmetic operation that failed
    """

    def __init__(self, message, operation):
        super(StringArithmeticError, self).__init__(message)
        self._operation = operation

    @property
    def operation(self):
        return self._operation
