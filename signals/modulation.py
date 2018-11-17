import signal
import trigonometry
import const
import numpy as np

class WideFrequencyModulation(signal.Signal):

    def __init__(self, amplitude, carrierFrequency, modulatingSignal, sampleRate, deviation=75000.0):
        self.sampleRate = sampleRate
        self.samplePeriod = 1.0 / sampleRate
        self.deviation = deviation
        self.modulatingSignal = modulatingSignal
        self.amplitude = amplitude
        self.carrierFrequency = carrierFrequency

    def get(self, index):
        if index < 0:
            raise Exception("Negative index not supported for WFM.")
        return self.amplitude * trigonometry.SINE_TABLE.sin(const.PI2 * (self.carrierFrequency * (index * self.samplePeriod) + self.deviation * self.modulatingSignal.integral(index)))
