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

def generatePureSine(amplitude, frequency, duration, sampleRate, sineArray):
    data = []
    for i in range(int(sampleRate*duration)):
        data.append(amplitude*mySin(2*math.pi*frequency*i/sampleRate, sineArray))
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

def main():
    wavFile = r"C:\users\rodolfo\desktop\pure-sine.wav"
    player = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    sampleRate = 44100
    audioDuration = 1
    sinusoidDetail = 512
    frequency = 300.0

    sineTable = getSineTable(sinusoidDetail)
    print myCos(0, sineTable)
    # data1 = generatePureSine(1, 1, 4, sampleRate, sineTable)
    # # pyplot.plot(range(len(data1)), data1)
    # data2 = generatePureSine(1, 1000, 4, sampleRate, sineTable)
    # # pyplot.plot(range(len(data2)), data2)
    # data3 = multiplySignals(data1, data2)
    # pyplot.plot(range(len(data3)), data3)
    # pyplot.show()

    # print data
    #
    # scipy.io.wavfile.write(wavFile, sampleRate, data3)
    # call([player, wavFile])

if __name__ == "__main__":
    main()