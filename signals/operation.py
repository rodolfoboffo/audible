import signal

class BinaryOperation(signal.Signal):

    def __init__(self, signal1, signal2, op):
        if signal1.getSampleRate() != signal2.getSampleRate():
            raise Exception("Sample rates doest'n match.")
        self.signal1 = signal1
        self.signal2 = signal2
        self.op = op

    def getSampleRate(self):
        return self.signal1.getSampleRate()

    def get(self, index):
        return self.op(self.signal1.get(index), self.signal2.get(index))


class Sum(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a + b
        super(Sum, self).__init__(signal1, signal2, op)


class Subtract(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a - b
        super(Sum, self).__init__(signal1, signal2, op)


class Multiply(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a * b
        super(Sum, self).__init__(signal1, signal2, op)
