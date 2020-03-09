import util.audio as audio
import numpy as np
import const
import logging
from signals.smath.fouriertrans import getMagnitudesFromDFT
from signals.signal import SineWave, Signal, ConstantSignal, DigitalSignal
from util.phase_detector import phaseDetector
from util.rds import RadioDataSystem
from signals.operation import Multiply, Sum, Normalize, Subtract, Shift
from signals.modulation import FrequencyModulation, IQModulation, AmplitudeModulation, DSBSCModulation
from plot.plot import SignalPlot

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def main():
    # carrierWaveFile = r"C:\Users\rodolfo\Documents\HDSDR\19khz-carrier.wav"
    carrierWaveFile = r"C:\Users\rodolfo\Documents\HDSDR\57khz-carrier.wav"
    rdsWaveFile = r"C:\Users\rodolfo\Documents\HDSDR\rds-signal.wav"
    outputWavFile = r"C:\Users\rodolfo\Documents\HDSDR\output.wav"

    subCarrierSignal = audio.extractSignalsFromWav(carrierWaveFile)[0]
    rdsSignal = audio.extractSignalsFromWav(rdsWaveFile)[0]
    sampleRate = subCarrierSignal.getSampleRate()
    # sampleRate = 960000

    nCarrier = Normalize(subCarrierSignal)
    nRdsSignal = Normalize(rdsSignal)
    multiplied = Normalize(Multiply(nCarrier, nRdsSignal))

    # plot = SignalPlot([notaSignal])
    # plot.setXAxisFunction(lambda samples: map(lambda x: 1.0 * x / sampleRate, range(len(samples))))
    # plot.plotSamples(notaSignal.getLength())

    # inputSignal = SineWave(1.0, 19000.0, sampleRate)
    # sin1 = SineWave(0.02, 56996.42, sampleRate, phase=3.816544200259476*3)
    # # m, std = phaseDetector(sin1, inputSignal, sampleRate, sampleInterval=(sampleRate*0.1, sampleRate*0.3), frequency=19000, result=const.RADIANS)
    # # print('Mean: %s, Std Dev: %s' % (m, std))
    # plot = SignalPlot([sin1, inputSignal])
    # plot.plotInterval(sampleRate*0.4, sampleRate*0.5)
    # 56996.42
    # sin2 = SineWave(0.04, 18998.89*3, sampleRate, phase=3.816544200259476*3)
    # plot = SignalPlot([inputSignal, sin2])
    # plot.plotInterval(sampleRate*0.0, sampleRate*0.0008)

    # sin1 = SineWave(0.04, 19001.0, sampleRate, phase=-6.067061982368344)
    # sin2 = SineWave(0.04, 19000.0, sampleRate, phase=const.PI+0.223451)
    # m, std = phaseDetector(sin1, sin2, sampleRate, sampleLength=sampleRate, frequency=19000, result=const.RADIANS)
    # print('Mean: %s, Std Dev: %s' % (m, std))
    # plot = SignalPlot([sin1, sin2])
    # plot.plotSamples(1920)

    # ft = np.fft.rfft(multiplied.getRange(int(40.2 * sampleRate), int(44.0 * sampleRate)))
    # ftSignal = Signal(getMagnitudesFromDFT(ft), sampleRate)
    # plot = SignalPlot([ftSignal])
    # plot.setXAxisFunction(lambda samples: list(map(lambda x: 1.0 * x * sampleRate / (2*len(samples)), range(len(samples)))))
    # plot.plotSamples(ftSignal.getLength())

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
    audio.exportWavFromSignal(multiplied, sampleRate * 1, outputWavFile)

    # d = DigitalSignal([0x55], 1, 400, low=-1.0, high=1.0)
    # dsbsc = DSBSCModulation(1.0, 5.3, d, modIndex=0.5)
    # plot = SignalPlot([d, dsbsc])
    # plot.plotSamples(d.getLength())

    # msg = "THAIS EH UMA PESSOA MUITO LEGAL, COISA MAIS LINDA DE DEUS, FOFA!"
    # rds = RadioDataSystem(0x00)
    # s = rds.getRadioTextSignal(msg, 192000)
    # rdsSignal = Normalize(DSBSCModulation(1.0, 57000.0, s, modIndex=0.5), 0.01)
    # resulting = Sum(mono, Sum(rdsSignal, pilotSubCarrier))
    # fm = FrequencyModulation(1.0, 106300000.0, resulting)
    # iq = IQModulation(1.0, 106300000.0, fm)
    # audio.exportWavFromSignal(iq.getSignals(), rdsSignal.getLength(), outputWavFile)

    # plot = SignalPlot([s])
    # plot.setXAxisFunction(lambda samples: list(map(lambda x: 1.0 * x / sampleRate, range(len(samples)))))
    # plot.plotSamples(s.getLength())

if __name__ == "__main__":
    main()