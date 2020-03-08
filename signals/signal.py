import numpy as np
from signals.smath import trigonometry
import const


class Signal(object):

    def __init__(self, samples, sampleRate):
        self.signal = samples
        self.sampleRate = sampleRate
        self.samplePeriod = 1.0 / sampleRate
        self.integralCache = {}
        self.cache = {}
        self.max = None
        self.min = None

    def getSampleRate(self):
        return self.sampleRate

    def get(self, index):
        value = self.cache.get(index, None)
        if value is None:
            value = self.signal[index] if index >= 0 and index < len(self.signal) else 0.0
            self.cache[index] = value
        return value

    def integral(self, index):
        i = self.integralCache.get(index, None)
        if i is None:
            if index > 0:
                i = self.integral(index-1) + self.samplePeriod * self.get(index)
            else:
                i = self.samplePeriod * self.get(index)
            self.integralCache[index] = i
        return i

    def getMax(self):
        if self.max is None:
            self.max = np.amax(self.signal)
        return self.max

    def getMin(self):
        if self.min is None:
            self.min = np.amin(self.signal)
        return self.min

    def getRange(self, start=0, end=None):
        i = start
        j = end or len(self.signal)
        s = []
        while i < j:
            s.append(self.get(i))
            i += 1
        return np.array(s)

    def getLength(self):
        return len(self.signal)


class PeriodicSignal(Signal):

    def __init__(self, samples, sampleRate):
        super(PeriodicSignal, self).__init__(samples, sampleRate)

    def get(self, index):
        return super(PeriodicSignal, self).get(index % len(self.signal))

    def integral(self, index):
        return super(PeriodicSignal, self).integral(index % len(self.signal)) + super(PeriodicSignal, self).integral(len(self.signal)-1) * (index / len(self.signal))

    def getLength(self):
        return None

class ConstantSignal(PeriodicSignal):

    def __init__(self, const, sampleRate):
        super(PeriodicSignal, self).__init__(np.array([const]), sampleRate)


class SineWave(Signal):

    def __init__(self, amplitude, frequency, sampleRate, phase=0.0):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.sampleRate = sampleRate
        self.samplePeriod = 1.0 / sampleRate
        self.cache = {}
        self.integralCache = {}

    def get(self, index):
        value = self.cache.get(index, None)
        if value is None:
            value = self.amplitude * trigonometry.SINE_TABLE.sin(const.PI2 * self.frequency * index / self.sampleRate + self.phase)
            self.cache[index] = value
        return value

    def getMax(self):
        return self.amplitude

    def getMin(self):
        return -1.0 * self.amplitude

    def getLength(self):
        return None

class DigitalSignal(Signal):

    def __init__(self, byteStream, clock, sampleRate, low=0.0, high=1.0):
        super(DigitalSignal, self).__init__(None, sampleRate)
        self.byteStream = byteStream
        self.clock = clock
        self.low = low
        self.high = high
        self.signal = self.generateSignal(byteStream, clock, sampleRate, low=low, high=high)

    def generateSignal(self, byteStream, clock, sampleRate, low=0.0, high=1.0):
        s = []
        samplePerClock = sampleRate / clock
        for byte in byteStream:
            for i in range(8):
                b = byte & 0x01
                v = high if b else low
                s += [v] * int(samplePerClock)
                byte = byte >> 1
        return np.array(s)