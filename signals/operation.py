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

    def getLength(self):
        return self.signal1.getLength() if self.signal1.getLength() > self.signal2.getLength() else self.signal2.getLength()

class Sum(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a + b
        super(Sum, self).__init__(signal1, signal2, op)


class Subtract(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a - b
        super(Subtract, self).__init__(signal1, signal2, op)


class Multiply(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a * b
        super(Multiply, self).__init__(signal1, signal2, op)

class UnaryOperation(signal.Signal):

    def __init__(self, signal):
        self.signal = signal

    def getSampleRate(self):
        return self.signal1.getSampleRate()

    def get(self, index):
        raise Exception("Unimplemented unary operation.")

    def getLength(self):
        raise Exception("Unimplemented method.")

class Shift(UnaryOperation):

    def __init__(self, signal, samplesToShift):
        self.signal = signal
        self.samplesToShift = samplesToShift

    def get(self, index):
        return self.signal.get(index + self.samplesToShift)

    def getLength(self):
        return None if self.signal.getLength() is None else self.signal.getLength() - self.samplesToShift

class Inverse(UnaryOperation):

    def __init__(self, signal):
        self.signal = signal

    def get(self, index):
        return -1.0 * self.signal.get(index)