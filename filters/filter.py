from signals.signal import SineWave, Signal
from signals.operation import Sum, Normalize, BinaryOperation, Multiply
from plot.plot import SignalPlot
from signals.smath.fouriertrans import getDFTFrequencies
import numpy as np

class Convolution(BinaryOperation):

    def __init__(self, signal1, signal2):
        self.signal1 = signal1
        self.signal2 = signal2
        self.cache = {}
        self.integralCache = {}
        coefficients = self.signal2.getRange()
        summ = sum(coefficients)
        self.max = summ * self.signal1.getMax()
        self.min = summ * self.signal1.getMin()

    def getSampleRate(self):
        return self.signal1.getSampleRate()

    def get(self, index):
        value = self.cache.get(index, None)
        if value is None:
            value = 0.0
            for i in range(self.signal2.getLength()):
                half = int(self.signal2.getLength()/2)
                if i < half:
                    value += self.signal1.get(index+i) * self.signal2.get(i)
                else:
                    value += self.signal1.get(index+half-i-1) * self.signal2.get(i)
            self.cache[index] = value
        return value

    def getLength(self):
        return self.signal1.getLength()

    def getMax(self):
        return self.max

    def getMin(self):
        return self.min

class FIRFilterBase(Convolution):

    def __init__(self, signal1, signal2):
        self.plottableFilterSignal = None
        super(FIRFilterBase, self).__init__(signal1, signal2)

    def getFilterSignal(self, plottable=False):
        if not plottable:
            return self.filterSignal
        if self.plottableFilterSignal:
            return self.plottableFilterSignal
        self.plottableFilterSignal = self.transformFilterSignal(self.filterSignal)
        return self.plottableFilterSignal

    def transformFilterSignal(self, filterSignal):
        signal = filterSignal.getRange()
        halfLen = int(len(signal) / 2)
        signal = list(signal[halfLen:]) + list(signal[:halfLen])
        return Signal(signal, filterSignal.getSampleRate())

class BandPassFilter(FIRFilterBase):

    def __init__(self, signal, filterDetail, lowestFrequency=None, highestFrequency=None):
        self.signal = signal
        self.highestFrequency = highestFrequency
        self.lowestFrequency = lowestFrequency
        self.filterDetail = filterDetail

        frequencies = getDFTFrequencies(filterDetail, self.signal.getSampleRate())
        filterFreq = list(map(lambda f: 1.0 if f < (highestFrequency or self.signal.getSampleRate()/2.0) and f > (lowestFrequency or 0.0) else 0.0, frequencies))
        filterSequence = list(np.fft.irfft(filterFreq))
        self.filterSignal = Normalize(Signal(filterSequence, self.signal.getSampleRate()))
        super(BandPassFilter, self).__init__(self.signal, self.filterSignal)

class LowPassFilter(BandPassFilter):

    def __init__(self, signal, filterDetail, highestFrequency):
        super(LowPassFilter, self).__init__(signal, filterDetail, highestFrequency=highestFrequency)

def main():
    sampleRate = 44000
    s1 = SineWave(1.0, 400, sampleRate)
    s2 = SineWave(0.8, 700, sampleRate)
    sum = Sum(s1, s2)

    filteredSignal = BandPassFilter(sum, 200, 350, 450)
    filterSignal = filteredSignal.getFilterSignal(plottable=True)
    p = SignalPlot([filterSignal])
    p.plotSamples(filterSignal.getLength())

    p = SignalPlot([s1, Multiply(0.006, filteredSignal)])
    p.setXAxisFunction(lambda samples: getDFTFrequencies(len(samples), sampleRate))
    p.plotSamples(800)


if __name__ == "__main__":
    main()