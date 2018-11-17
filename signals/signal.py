import math
import scipy.io.wavfile
import numpy as np
import trigonometry
import const
import fractions
import matplotlib.pyplot as pyplot
from subprocess import call
import os


class Signal(object):

    def __init__(self, samples, sampleRate):
        self.signal = samples
        self.sampleRate = sampleRate
        self.samplePeriod = 1.0 / sampleRate
        self.integralArray = None

    def getSampleRate(self):
        return self.sampleRate

    def get(self, index):
        return self.signal[index]

    def integral(self, index):
        if self.integralArray is None:
            self.initializeIntegral(self.signal)
        return self.integralArray[index]

    def initializeIntegral(self, signal):
        area = 0.0
        iArray = []
        for i in range(len(signal)):
            area += self.samplePeriod * self.get(i)
            iArray[i] = area
        return iArray

    def getRange(self, start=0, end=None):
        i = start
        j = end or len(self.signal)
        s = []
        while i < j:
            s.append(self.get(i))
            i += 1
        return np.array(s)

    def getLength(self, seconds):
        return self.getRange(0, end=int(seconds*self.sampleRate))

class PeriodicSignal(Signal):

    def __init__(self, samples, sampleRate):
        super(PeriodicSignal, self).__init__(samples, sampleRate)

    def get(self, index):
        return self.signal[index % len(self.signal)]

    def integral(self, index):
        if self.integralArray is None:
            self.initializeIntegral(self.signal)
        return self.integralArray[index % len(self.signal)] + self.integralArray[-1] * (index / len(self.signal))


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

    def get(self, index):
        return self.amplitude * trigonometry.SINE_TABLE.sin(const.PI2 * self.frequency * index / self.sampleRate + self.phase)

    def integral(self, index):
        return -1.0 * self.amplitude * (
                trigonometry.SINE_TABLE.cos(const.PI2 * self.frequency * index / self.sampleRate + self.phase)
                - trigonometry.SINE_TABLE.cos(self.phase)
            )
