import math
import scipy.io.wavfile
import numpy as np
import fractions
import matplotlib.pyplot as pyplot
from subprocess import call
import os
from signals import signal
from signals.modulation import FrequencyModulation
from plot.plot import SignalPlot

def main():

    sampleRate = 10000
    s = signal.SineWave(1.0, 1.0, sampleRate)
    fm = FrequencyModulation(1, 10, s, sampleRate, deviation=4)
    p = SignalPlot([s, fm])
    p.plotSeconds(4)

    #wavFile = r"C:\users\rodolfo\desktop\pure-sine.wav"
    #wavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\HDSDR_20181107_192455Z_106300kHz_AF.wav"
    #wavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\HDSDR_20181107_192455Z_106300kHz_IF.wav"
    #wavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\HDSDR_20181107_192455Z_106300kHz_RF.wav"
    # wavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\HDSDR_20181107_192455Z_106300kHz_RF_My_RF.wav"
    # inputWavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\input.wav"
    # #player = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    # audioDuration = 8.0
    # sinusoidDetail = 512
    # frequency = 300.0
    # sampleFrequency = 384000.0
    # bins = 20000
	#
    # sineTable = getSineTable(sinusoidDetail)
    #
    # #signal1 = generatePureSine(1.0, 1.0, 10, 1024, sineTable)
    # #signal2 = generateFMSignal(1.0, 3.0, signal1, 1024, sineTable)
    # #pyplot.plot(range(len(signal1)), signal1)
    # #pyplot.plot(range(len(signal2)), signal2)
    # #pyplot.show()
    #
    # wavReadFile = scipy.io.wavfile.read(inputWavFile)
    # rightChannel = wavReadFile[1]
    # audioDuration = 1.0*len(rightChannel)/sampleFrequency
    #
    # lo = generatePureSine(1.0, 106300000.0, audioDuration, sampleFrequency, sineTable)
    # loShifted = generatePureSine(1.0, 106300000.0, audioDuration, sampleFrequency, sineTable, phase=math.pi/2.0)
    # #leftAudio = generatePureSine(1.0, 300.0, audioDuration, sampleFrequency, sineTable)
    # #rightAudio = generatePureSine(1.0, 1000.0, audioDuration, sampleFrequency, sineTable)
    # #monoAudio = multiplySignals(sumSignals(leftAudio, rightAudio), 0.5)
    #
    # pilotSubCarrier = generatePureSine(0.1, 19000.0, audioDuration, sampleFrequency, sineTable)
    # stereoSubCarrier = generatePureSine(0.1, 38000.0, audioDuration, sampleFrequency, sineTable)
    # leftChannel = generatePureSine(0.2, 1000.0, audioDuration, sampleFrequency, sineTable)
    #
    # monoAudio = multiplySignals(sumSignals(rightChannel, leftChannel), 0.5)
    # monoAudio = sumSignals(monoAudio, pilotSubCarrier)
    #
    # stereoModulation = sumSignals(multiplySignals(subtractSignals(leftChannel, rightChannel), 0.5), 1.0)
    # stereoChannel = subtractSignals(multiplySignals(stereoSubCarrier, stereoModulation), multiplySignals(stereoSubCarrier, 0.5))
    # resultingAudio = sumSignals(monoAudio, stereoChannel)
    #
    # fmSignal = generateFMSignal(1.0, 106300000.0, resultingAudio, sampleFrequency, sineTable)
    #
    # i = multiplySignals(fmSignal, lo)
    # q = multiplySignals(fmSignal, loShifted)
    #
    # #pyplot.plot(range(len(i)), i)
    # #pyplot.plot(range(len(q)), q)
    # #pyplot.show()
    #
    # scipy.io.wavfile.write(wavFile, int(sampleFrequency), np.array(zip(i, q)))

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