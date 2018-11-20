import util.audio as audio
from signals.signal import SineWave, Signal, ConstantSignal
from signals.operation import Multiply, Sum, Normalize, Subtract
from signals.modulation import FrequencyModulation, IQModulation, AmplitudeModulation, DSBSCModulation
from plot.plot import SignalPlot

def main():
    inputWavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\input.wav"
    outputWavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\output.wav"

    # voice = audio.extractSignalsFromWav(inputWavFile)[0]
    # sampleRate = voice.getSampleRate()
    sampleRate = 960000
    # sampleRate = 240000
    rightChannel = SineWave(2.0, 430.0, sampleRate)
    leftChannel = SineWave(0.7, 1013.0, sampleRate)
    pilotSubCarrier = SineWave(0.1, 19000.0, sampleRate)
    stereoSubCarrier = SineWave(0.1, 38000.0, sampleRate)
    rdsSubCarrier = SineWave(0.1, 57000.0, sampleRate)
    mono = Normalize(Sum(leftChannel, rightChannel))
    # mono = SineWave(0.6, 400, sampleRate)
    stereo = DSBSCModulation(1.0, 38000.0, Normalize(Subtract(leftChannel, rightChannel)), modIndex=0.5)
    resulting = Normalize(Sum(Sum(mono, pilotSubCarrier), stereo), 0.7)
    # resulting = Sum(mono, pilotSubCarrier)

    #
    fm = FrequencyModulation(1.0, 106300000.0, resulting)
    iq = IQModulation(1.0, 106300000.0, fm)
    # #
    audio.exportWavFromSignal(iq.getSignals(), sampleRate * 4, outputWavFile)
if __name__ == "__main__":
    main()