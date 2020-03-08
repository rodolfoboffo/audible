import util.audio as audio
import numpy as np
from signals.smath.fouriertrans import getMagnitudesFromDFT
from signals.signal import SineWave, Signal, ConstantSignal, DigitalSignal
from util.rds import RadioDataSystem
from signals.operation import Multiply, Sum, Normalize, Subtract
from signals.modulation import FrequencyModulation, IQModulation, AmplitudeModulation, DSBSCModulation
from plot.plot import SignalPlot

def main():
    inputWavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\input.wav"
    outputWavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\output.wav"

    notaWavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\mi-la.wav"
    notaSignal = audio.extractSignalsFromWav(notaWavFile)[0]
    sampleRate = notaSignal.getSampleRate()

    # plot = SignalPlot([notaSignal])
    # plot.setXAxisFunction(lambda samples: map(lambda x: 1.0 * x / sampleRate, range(len(samples))))
    # plot.plotSamples(notaSignal.getLength())

    ft = np.fft.rfft(notaSignal.getRange(int(40.2 * sampleRate), int(44.0 * sampleRate)))
    ftSignal = Signal(getMagnitudesFromDFT(ft), sampleRate)
    plot = SignalPlot([ftSignal])
    plot.setXAxisFunction(lambda samples: map(lambda x: 1.0 * x * sampleRate / (2*len(samples)), range(len(samples))))
    plot.plotSamples(ftSignal.getLength())

    # # voice = audio.extractSignalsFromWav(inputWavFile)[0]
    # # sampleRate = voice.getSampleRate()
    # sampleRate = 960000
    # # sampleRate = 240000
    # rightChannel = SineWave(2.0, 430.0, sampleRate)
    # leftChannel = SineWave(0.7, 1013.0, sampleRate)
    # pilotSubCarrier = SineWave(0.1, 19000.0, sampleRate)
    # stereoSubCarrier = SineWave(0.1, 38000.0, sampleRate)
    # rdsSubCarrier = SineWave(0.1, 57000.0, sampleRate)
    # mono = Normalize(Sum(leftChannel, rightChannel))
    # # mono = SineWave(0.6, 400, sampleRate)
    # stereo = DSBSCModulation(1.0, 38000.0, Normalize(Subtract(leftChannel, rightChannel)), modIndex=0.5)
    # resulting = Normalize(Sum(Sum(mono, pilotSubCarrier), stereo), 0.7)
    # # resulting = Sum(mono, pilotSubCarrier)

    #
    # fm = FrequencyModulation(1.0, 106300000.0, resulting)
    # iq = IQModulation(1.0, 106300000.0, fm)
    # # #
    # audio.exportWavFromSignal(iq.getSignals(), sampleRate * 4, outputWavFile)

    # d = DigitalSignal([0x55], 1, 400, low=-1.0, high=1.0)
    # dsbsc = DSBSCModulation(1.0, 5.3, d, modIndex=0.5)
    # plot = SignalPlot([d, dsbsc])
    # plot.plotSamples(d.getLength())

    # msg = "THAIS EH UMA PESSOA MUITO LEGAL, COISA MAIS LINDA DE DEUS, FOFA!"
    # rds = RadioDataSystem(0x00)
    # s = rds.getRadioTextSignal(msg, 960000)
    # rdsSignal = Normalize(DSBSCModulation(1.0, 57000.0, s, modIndex=0.5), 0.01)
    # resulting = Sum(mono, Sum(rdsSignal, pilotSubCarrier))
    # fm = FrequencyModulation(1.0, 106300000.0, resulting)
    # iq = IQModulation(1.0, 106300000.0, fm)
    # audio.exportWavFromSignal(iq.getSignals(), rdsSignal.getLength(), outputWavFile)

if __name__ == "__main__":
    main()