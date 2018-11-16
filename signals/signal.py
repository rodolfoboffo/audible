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

    def getSampleRate(self):
        return self.sampleRate

    def get(self, index):
        return self.signal[index]

    def getRange(self, start=0, end=None):
        i = start
        j = end or len(self.signal)
        s = []
        while i < j:
            return s.append(self.get(i))
        return np.array(s)

    def getLength(self, seconds):
        return self.getRange(0, int(seconds*self.sampleRate))

class PeriodicSignal(Signal):

    def __init__(self, samples, sampleRate):
        super(PeriodicSignal, self).__init__(samples, sampleRate)

    def get(self, index):
        return self.signal[index % len(self.signal)]


class ConstantSignal(PeriodicSignal):

    def __init__(self, const, sampleRate):
        super(PeriodicSignal, self).__init__(np.array([const]), sampleRate)


class SineWave(Signal):

    def __init__(self, amplitude, frequency, sampleRate, phase=0.0):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.sampleRate = sampleRate

    def get(self, index):
        return self.amplitude * trigonometry.SINE_TABLE.sin(const.PI2 * self.frequency * index / self.sampleRate + self.phase)