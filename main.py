import math
import scipy.io.wavfile
import numpy as np
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

class PeriodicSignal(Signal):

    def __init__(self, signal, sampleRate):
        super(PeriodicSignal, self).__init__(signal, sampleRate)

    def get(self, index):
        return self.signal[index%len(self.signal)]

class ConstantSignal(PeriodicSignal):

    def __init__(self, const, sampleRate):
        super(PeriodicSignal, self).__init__(np.array([const]), sampleRate)

class BinaryOperation(Signal):

    def __init__(self, signal1, signal2, op):
        if signal1.getSampleRate() != signal2.getSampleRate():
            raise Exception("Sample rates doest'n match.")
        self.signal1 = signal1
        self.signal2 = signal2
        self.op = op

    def getSampleRate(self):
        return self.signal1.getSampleRate()

    def get(self, index):
        return self.op(self.signal1.get(index), self.signal2.get(index))

class Sum(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a + b
        super(Sum, self).__init__(signal1, signal2, op)

class Subtract(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a - b
        super(Sum, self).__init__(signal1, signal2, op)

class Multiply(BinaryOperation):

    def __init__(self, signal1, signal2):
        op = lambda a, b: a * b
        super(Sum, self).__init__(signal1, signal2, op)

class PhaseShift(Signal):

    def __init__(self, signal, phase):
        self.signal = signal
        self.phaseShift = phase

    def 

def getSineTable(sinusoidDetail):
    sin = []
    for i in range(sinusoidDetail):
        sin.append(math.sin(2 * math.pi / sinusoidDetail * i))
    return np.array(sin)

def mySin(x, sineArray):
    i = int(x/(2*math.pi)*len(sineArray))%len(sineArray)
    return sineArray[i]

def myCos(x, sineArray):
    i = int((math.pi/2.0 - x)/(2*math.pi)*len(sineArray))%len(sineArray)
    return sineArray[i]

def generatePureSine(amplitude, frequency, sampleRate, sineArray, phase=0.0):
    data = []
    for i in range(int(sampleRate*duration)):
        data.append(amplitude*mySin(2*math.pi*frequency*i/sampleRate + phase, sineArray))
    return np.array(data)

def generateFMSignal(amplitude, carrierFrequency, audioSignal, sampleRate, sineArray, phase=0.0):
    data = []
    phi = phase
    t = 1.0 / sampleRate
    for i in range(len(audioSignal)):
        if i != 0:
            phi += 2 * math.pi * (carrierFrequency + 75000.0*audioSignal[i]) * t
        data.append(amplitude * mySin(phi, sineArray))
    return np.array(data)

def sumSignals(signal1, signal2):
    r = []
    if (isinstance(signal1, np.ndarray) and isinstance(signal2, np.ndarray)):
        for i in range(max(len(signal1), len(signal2))):
            r.append((getSample(signal1, i) or 0.0) + (getSample(signal2, i) or 0.0))
    else:
        acSignal, dcSignal = (signal1, signal2) if isinstance(signal1, np.ndarray) else (signal2, signal1)
        for i in range(len(acSignal)):
            r.append(acSignal[i] + dcSignal)
    return np.array(r)

def subtractSignals(signal1, signal2):
    r = []
    if (isinstance(signal1, np.ndarray) and isinstance(signal2, np.ndarray)):
        for i in range(max(len(signal1), len(signal2))):
            r.append((getSample(signal1, i) or 0.0) - (getSample(signal2, i) or 0.0))
    else:
        acSignal, dcSignal, invert = (signal1, signal2, 1.0) if isinstance(signal1, np.ndarray) else (signal2, signal1, -1.0)
        for i in range(len(acSignal)):
            r.append((acSignal[i] - dcSignal)*invert)
    return np.array(r)

def multiplySignals(signal1, signal2):
    r = []
    if (isinstance(signal1, np.ndarray) and isinstance(signal2, np.ndarray)):
        for i in range(max(len(signal1), len(signal2))):
            r.append((getSample(signal1, i) or 0.0) * (getSample(signal2, i) or 0.0))
    else:
        acSignal, dcSignal = (signal1, signal2) if isinstance(signal1, np.ndarray) else (signal2, signal1)
        for i in range(len(acSignal)):
            r.append(acSignal[i] * dcSignal)
    return np.array(r)

def getSample(signal, index):
    return signal[index] if len(signal) > index else None

def hanningFunction(sampleIndex, totalSamples, sineArray):
    return 0.5 - 0.5*myCos(2*math.pi*sampleIndex/totalSamples, sineArray)
	
def discreteFourierTransform(signal, nBins, sineArray):
    reals, img = [], []
    windowingFunction = hanningFunction
    for m in range(nBins):
        reals.append(0.0)
        img.append(0.0)
        for n in range(nBins):
            reals[-1] += windowingFunction(n, nBins, sineArray)*signal[n]*myCos(2*math.pi*n*m/nBins ,sineArray)
            img[-1] += windowingFunction(n, nBins, sineArray)*signal[n]*mySin(2*math.pi*n*m/nBins, sineArray)
    return reals, img

def getMagnitudesFromDFT(dft):
    mags, phases = [], []
    if isinstance(dft, tuple):
        reals, img = dft
        for i in range(len(reals)):
            mags.append(math.sqrt(reals[i] * reals[i] + img[i] * img[i]))
            phases.append(360.0 * math.atan(img[i] / reals[i]) / (2 * math.pi))
    else:
        for i in range(len(dft)):
            mags.append(math.sqrt(dft[i].real * dft[i].real + dft[i].imag * dft[i].imag))
            phases.append(360.0 * math.atan(dft[i].imag / dft[i].real) / (2 * math.pi))
    return mags

def maxMin(signal):
        max = 0.0
        min = 0.0
        for i in range(len(signal)):
            max = signal[i] if signal[i] > max else max
            min = signal[i] if signal[i] < min else min
        print "max", max
        print "min", min

def main():
    #wavFile = r"C:\users\rodolfo\desktop\pure-sine.wav"
    #wavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\HDSDR_20181107_192455Z_106300kHz_AF.wav"
    #wavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\HDSDR_20181107_192455Z_106300kHz_IF.wav"
    #wavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\HDSDR_20181107_192455Z_106300kHz_RF.wav"
    wavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\HDSDR_20181107_192455Z_106300kHz_RF_My_RF.wav"
    inputWavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\input.wav"
    #player = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    audioDuration = 8.0
    sinusoidDetail = 512
    frequency = 300.0
    sampleFrequency = 384000.0
    bins = 20000
	
    sineTable = getSineTable(sinusoidDetail)

    #signal1 = generatePureSine(1.0, 1.0, 10, 1024, sineTable)
    #signal2 = generateFMSignal(1.0, 3.0, signal1, 1024, sineTable)
    #pyplot.plot(range(len(signal1)), signal1)
    #pyplot.plot(range(len(signal2)), signal2)
    #pyplot.show()

    wavReadFile = scipy.io.wavfile.read(inputWavFile)
    rightChannel = wavReadFile[1]
    audioDuration = 1.0*len(rightChannel)/sampleFrequency

    lo = generatePureSine(1.0, 106300000.0, audioDuration, sampleFrequency, sineTable)
    loShifted = generatePureSine(1.0, 106300000.0, audioDuration, sampleFrequency, sineTable, phase=math.pi/2.0)
    #leftAudio = generatePureSine(1.0, 300.0, audioDuration, sampleFrequency, sineTable)
    #rightAudio = generatePureSine(1.0, 1000.0, audioDuration, sampleFrequency, sineTable)
    #monoAudio = multiplySignals(sumSignals(leftAudio, rightAudio), 0.5)

    pilotSubCarrier = generatePureSine(0.1, 19000.0, audioDuration, sampleFrequency, sineTable)
    stereoSubCarrier = generatePureSine(0.1, 38000.0, audioDuration, sampleFrequency, sineTable)
    leftChannel = generatePureSine(0.2, 1000.0, audioDuration, sampleFrequency, sineTable)

    monoAudio = multiplySignals(sumSignals(rightChannel, leftChannel), 0.5)
    monoAudio = sumSignals(monoAudio, pilotSubCarrier)

    stereoModulation = sumSignals(multiplySignals(subtractSignals(leftChannel, rightChannel), 0.5), 1.0)
    stereoChannel = subtractSignals(multiplySignals(stereoSubCarrier, stereoModulation), multiplySignals(stereoSubCarrier, 0.5))
    resultingAudio = sumSignals(monoAudio, stereoChannel)

    fmSignal = generateFMSignal(1.0, 106300000.0, resultingAudio, sampleFrequency, sineTable)

    i = multiplySignals(fmSignal, lo)
    q = multiplySignals(fmSignal, loShifted)

    #pyplot.plot(range(len(i)), i)
    #pyplot.plot(range(len(q)), q)
    #pyplot.show()

    scipy.io.wavfile.write(wavFile, int(sampleFrequency), np.array(zip(i, q)))

    #signal2 = generatePureSine(0.5, 2000.0, 1.0, sampleFrequency, sineTable, phase=(3*math.pi/4.0))
    #signal3 = sumSignals(signal1, signal2)
    
    #dft = discreteFourierTransform(signal3, bins, sineTable)
    #dftMags = getMagnitudesFromDFT(dft)
    #pyplot.plot(range(len(signal1)), signal1)
    #pyplot.plot(range(len(signal2)), signal2)
    #pyplot.plot(range(len(signal3)), signal3)
    # data2 = generatePureSine(1, 1000, 4, sampleRate, sineTable)
    # # pyplot.plot(range(len(data2)), data2)
    # data3 = multiplySignals(data1, data2)
    #pyplot.plot(map(lambda x: x*sampleFrequency/bins, range(len(dftMags))), dftMags)
    #pyplot.plot(map(lambda x: x*sampleFrequency/bins, range(len(dft[1]))), dft[1])
    #pyplot.plot(range(len(signal3[:8])), signal3[:8])
    #pyplot.show()

    # print data
    #
    #scipy.io.wavfile.write(wavFile, sampleRate, signal3)
    #call([player, wavFile])
	
    #wavReadFile = scipy.io.wavfile.read(wavFile)
    #sampleFrequency = wavReadFile[0]
    #print sampleFrequency
    #signalMag = getMagnitudesFromDFT((list(map(lambda x: x[0], wavReadFile[1])), list(map(lambda x: x[1], wavReadFile[1]))))

    #print len(wavReadFile[1])

    #i = list(map(lambda x: x[0] / 32767.0, wavReadFile[1][:100]))
    #pyplot.plot(range(len(i)), i)
    #pyplot.show()

    #startPoint = int(startTime * sampleFrequency)
    #dft = np.fft.fft(audio3)
    #dftMags = getMagnitudesFromDFT(dft)
    #pyplot.plot(map(lambda x: x*sampleFrequency/bins, range(len(dftMags[:bins/2]))), dftMags[:bins/2])
    #dft2 = np.fft.fft(list(map(lambda x: x[1], wavReadFile[1][:bins])))
    #dftMags2 = getMagnitudesFromDFT(dft2)
    #pyplot.plot(range(len(audio3)), audio3)
    #pyplot.show()

if __name__ == "__main__":
    main()