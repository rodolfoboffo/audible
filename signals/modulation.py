import signal
import const
import signals.operation
from signals.math import trigonometry
import const

class Modulation(signal.Signal):

    def __init__(self, modulatingSignal):
        self.sampleRate = modulatingSignal.getSampleRate()
        self.samplePeriod = 1.0 / self.sampleRate
        self.modulatingSignal = modulatingSignal

class IQModulation(Modulation):

    def __init__(self, amplitude, oscillatorFrequency, modulatingSignal):
        super(IQModulation, self).__init__(modulatingSignal)
        self.amplitude = amplitude
        self.oscillatorFrequency = oscillatorFrequency
        self.localOscillator = signal.SineWave(self.amplitude, oscillatorFrequency, self.getSampleRate(), phase=0.0)
        self.shiftedLocalOscillator = signal.SineWave(self.amplitude, oscillatorFrequency, self.getSampleRate(), phase=const.PI_HALF)
        self.inPhase = signals.operation.Multiply(self.modulatingSignal, self.localOscillator)
        self.quadrature = signals.operation.Multiply(self.modulatingSignal, self.shiftedLocalOscillator)

    def getInPhaseSignal(self):
        return self.inPhase

    def getQuadratureSignal(self):
        return self.quadrature

    def getSignals(self):
        return [self.getInPhaseSignal(), self.getQuadratureSignal()]

    def get(self, index):
        return [self.getInPhaseSample(index), self.getQuadratureSample(index)]

    def getInPhaseSample(self, index):
        return self.getInPhaseSignal().get(index)

    def getQuadratureSample(self, index):
        return self.getQuadratureSignal().get(index)

class FrequencyModulation(Modulation):

    def __init__(self, amplitude, carrierFrequency, modulatingSignal, deviation=75000.0):
        super(FrequencyModulation, self).__init__(modulatingSignal)
        self.deviation = deviation
        self.amplitude = amplitude
        self.carrierFrequency = carrierFrequency

    def get(self, index):
        if index < 0:
            raise Exception("Negative index not supported for FM.")
        return self.amplitude * trigonometry.SINE_TABLE.sin(const.PI2 * (self.carrierFrequency * (index * self.samplePeriod) + self.deviation * self.modulatingSignal.integral(index)))
