import util.audio as audio
from signals.modulation import FrequencyModulation, IQModulation

def main():
    inputWavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\input.wav"
    outputWavFile = r"C:\Users\rodolfo.souza\Documents\HDSDR\output.wav"
    voice = audio.extractSignalsFromWav(inputWavFile)[0]
    fm = FrequencyModulation(1.0, 106300000.0, voice)
    iq = IQModulation(1.0, 106300000.0, fm)

    audio.exportWavFromSignal(iq.getSignals(), voice.getLength(), outputWavFile)

if __name__ == "__main__":
    main()