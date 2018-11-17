import signal
import trigonometry
import const
import numpy as np

class WideFrequencyModulation(signal.Signal):

    def __init__(self, amplitude, carrierFrequency, modulatingSignal, sampleRate):
        self.sampleRate = sampleRate
        self.modulatingSignal = modulatingSignal
        self.amplitude = amplitude
        self.carrierFrequency = carrierFrequency

    def get(self, index):
        if index < 0:
            raise Exception("Negative index not supported for WFM.")
        return self.amplitude * const.PI2 * (self.carrierFrequency * (index * self.samplePeriod) + 75000.0 * self.modulatingSignal.integral(index))
