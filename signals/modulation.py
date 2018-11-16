import signal
import trigonometry
import const
import numpy as np

class WideFrequencyModulation(signal.Signal):

    def __init__(self, amplitude, carrierFrequency, modulatingSignal, sampleRate, phase=0.0):
        self.sampleRate = sampleRate
        self.modulatingSignal = modulatingSignal
        self.amplitude = amplitude
        self.carrierFrequency = carrierFrequency
        self.phase = phase
        self.data = np.array([])
        self.samplePeriod = 1.0 / sampleRate

    def get(self, index):
        if index < 0:
            raise Exception("Negative index not supported for WFM.")
        elif (len(self.data)>index):
            return self.data[index]
        elif index > 0:
            phi = self.get(index - 1)
            phi += const.PI2 * (self.carrierFrequency + 75000.0 * self.modulatingSignal.get(index)) * self.samplePeriod
            value = self.amplitude * trigonometry.SINE_TABLE.sin(phi)
        elif index == 0:
            value = self.phase
        np.insert(self.data, index, value)
        return value
