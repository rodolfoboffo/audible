from signals.signal import SineWave, Signal
from signals.operation import Sum
from plot.plot import SignalPlot
import numpy as np
import math

def getMagnitudesFromDFT(dft):
    mags, phases = [], []
    for i in range(len(dft)):
        mags.append(math.sqrt(dft[i].real * dft[i].real + dft[i].imag * dft[i].imag))
        # phases.append(360.0 * math.atan(dft[i].imag / dft[i].real) / (2 * math.pi))
    return mags

def main():
    sampleRate = 230000
    s1 = SineWave(1.0, 400, sampleRate)
    s2 = SineWave(0.1, 500, sampleRate)
    sum = Sum(s1, s2)
    ft = np.fft.rfft(sum.getRange(0, 20000))
    ift = np.fft.irfft(ft)
    iftSignal = Signal(ift, sampleRate)
    ftSignal = Signal(getMagnitudesFromDFT(ft), sampleRate)
    # p = SignalPlot([sum, iftSignal])
    # p.plotSamples(iftSignal.getLength())
    p = SignalPlot([ftSignal])
    p.plotSamples(ftSignal.getLength())

if __name__ == "__main__":
    main()