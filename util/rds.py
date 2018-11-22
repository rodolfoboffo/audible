import math

AGGREGATE_WORD_A = 0xFC
AGGREGATE_WORD_B = 0x198
AGGREGATE_WORD_C = 0x168
AGGREGATE_WORD_C_LINE = 0x350
AGGREGATE_WORD_D = 0x1B4
AGGREGATE_WORD_E = 0x00

class RadioDataSystem(object):

    def __init__(self, pi):
        self.pi = pi

    def getRadioTextSignal(self, text):
        textLength = len(text) if len(text) <= 64 else 64
        croppedText = text[:textLength]

    def getVerificationCode(self, word):
        pass