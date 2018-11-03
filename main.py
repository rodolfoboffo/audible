import math
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as pyplot
from subprocess import call
import os

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

def generatePureSine(amplitude, frequency, duration, sampleRate, sineArray, phase=0.0):
    data = []
    for i in range(int(sampleRate*duration)):
        data.append(amplitude*mySin(2*math.pi*frequency*i/sampleRate + phase, sineArray))
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
    mags, phases = [], []
    for i in range(nBins):
        mags.append(math.sqrt(reals[i]*reals[i] + img[i]*img[i]))
        phases.append(360.0*math.atan(img[i]/reals[i])/(2*math.pi))
    return mags, phases
	
def main():
    wavFile = r"C:\users\rodolfo\desktop\pure-sine.wav"
    player = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    sampleRate = 44100
    audioDuration = 1
    sinusoidDetail = 512
    frequency = 300.0
    sampleFrequency = 8000.0
    bins = 750

    sineTable = getSineTable(sinusoidDetail)
    signal1 = generatePureSine(1.0, 1000.0, 1.0, sampleFrequency, sineTable)
    signal2 = generatePureSine(0.5, 2000.0, 1.0, sampleFrequency, sineTable, phase=(3*math.pi/4.0))
    signal3 = sumSignals(signal1, signal2)

    dft = discreteFourierTransform(signal3, bins, sineTable)
    #print dft
    #s1 = generatePureSine(1.0, 3.0, 1.0, 200, sineTable)
    #s2 = generatePureSine(1.0, 3.0, 1.0, 200, sineTable, phase=math.pi/2)
    #print signal3
    # print myCos(0, sineTable)
    # data1 = generatePureSine(1, 1, 4, sampleRate, sineTable)
    #pyplot.plot(range(len(signal1)), signal1)
    #pyplot.plot(range(len(signal2)), signal2)
    #pyplot.plot(range(len(signal3)), signal3)
    # data2 = generatePureSine(1, 1000, 4, sampleRate, sineTable)
    # # pyplot.plot(range(len(data2)), data2)
    # data3 = multiplySignals(data1, data2)
    pyplot.plot(map(lambda x: x*sampleFrequency/bins, range(len(dft[0]))), dft[0])
    #pyplot.plot(map(lambda x: x*sampleFrequency/bins, range(len(dft[1]))), dft[1])
    #pyplot.plot(range(len(signal3[:8])), signal3[:8])
    pyplot.show()

    # print data
    #
    #scipy.io.wavfile.write(wavFile, sampleRate, signal3)
    #call([player, wavFile])

if __name__ == "__main__":
    main()