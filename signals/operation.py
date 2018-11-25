import signal
import math

class BinaryOperation(signal.Signal):

    def __init__(self, signal1, signal2, op):
        if signal1.getSampleRate() != signal2.getSampleRate():
            raise Exception("Sample rates doest'n match.")
        self.signal1 = signal1
        self.signal2 = signal2
        self.op = op
        self.cache = {}
        self.integralCache = {}
        self.samplePeriod = 1.0 / self.signal1.getSampleRate()

    def getSampleRate(self):
        return self.signal1.getSampleRate()

    def get(self, index):
        value = self.cache.get(index, None)
        if value is None:
            value = self.op(self.signal1.get(index), self.signal2.get(index))
            self.cache[index] = value
        return value

    def getLength(self):
        return self.signal1.getLength() if self.signal1.getLength() > self.signal2.getLength() else self.signal2.getLength()

class Sum(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a + b
        super(Sum, self).__init__(signal1, signal2, op)

    def getMax(self):
        return self.signal1.getMax() + self.signal2.getMax()

    def getMin(self):
        return self.signal1.getMin() + self.signal2.getMin()

    def integral(self, index):
        i = self.integralCache.get(index, None)
        if i is None:
            i = self.signal1.integral(index) + self.signal2.integral(index)
            self.integralCache[index] = i
        return i

class Subtract(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a - b
        super(Subtract, self).__init__(signal1, signal2, op)

    def getMax(self):
        return self.signal1.getMax() - self.signal2.getMin()

    def getMin(self):
        return self.signal1.getMin() - self.signal2.getMax()

    def integral(self, index):
        i = self.integralCache.get(index, None)
        if i is None:
            i = self.signal1.integral(index) - self.signal2.integral(index)
            self.integralCache[index] = i
        return i


class Multiply(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a * b
        super(Multiply, self).__init__(signal1, signal2, op)

    def getMax(self):
        maxmax = self.signal1.getMax() * self.signal2.getMax()
        minmin = self.signal1.getMin() * self.signal2.getMin()
        return maxmax if maxmax > minmin else minmin

    def getMin(self):
        maxmin = self.signal1.getMax() * self.signal2.getMin()
        minmax = self.signal1.getMin() * self.signal2.getMax()
        return maxmin if maxmin < minmax else minmax

class UnaryOperation(signal.Signal):

    def __init__(self, signal):
        self.signal = signal
        self.cache = {}
        self.integralCache = {}
        self.samplePeriod = 1.0 / self.signal.getSampleRate()

    def getSampleRate(self):
        return self.signal.getSampleRate()

    def get(self, index):
        raise Exception("Unimplemented unary operation.")

    def getLength(self):
        raise Exception("Unimplemented method.")

class Shift(UnaryOperation):

    def __init__(self, signal, samplesToShift):
        super(Shift, self).__init__(signal)
        self.samplesToShift = samplesToShift

    def get(self, index):
        return self.signal.get(index + self.samplesToShift)

    def getMax(self):
        return self.signal1.getMax()

    def getMin(self):
        return self.signal1.getMin()

    def integral(self, index):
        return self.signal.integral(index) - self.signal.integral(self.samplesToShift)

    def getLength(self):
        return None if self.signal.getLength() is None else self.signal.getLength() - self.samplesToShift

class Inverse(UnaryOperation):

    def __init__(self, signal):
        super(Inverse, self).__init__(signal)

    def getMax(self):
        return self.signal1.getMin()

    def getMin(self):
        return self.signal1.getMax()

    def get(self, index):
        return -self.signal.get(index)

    def integral(self, index):
        return -self.signal.integral(index)

class Normalize(UnaryOperation):

    def __init__(self, signal, factor=1.0):
        super(Normalize, self).__init__(signal)
        self.factor = factor
        self.maxAbs = abs(self.signal.getMax()) if abs(self.signal.getMax()) > abs(self.signal.getMin()) else abs(self.signal.getMin())
        self.k = self.factor / self.maxAbs if self.maxAbs != 0.0 else 1.0

    def getMax(self):
        return self.k * self.signal.getMax()

    def getMin(self):
        return self.k * self.signal.getMin()

    def get(self, index):
        return self.k * self.signal.get(index)

    def getLength(self):
        return self.signal.getLength()