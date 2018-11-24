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

def crc(value, key, dataLength, crcLength):
    value = value << crcLength # tamanho da chave - 1
    key = key << (dataLength-1) # tamanho do dado - tamanho da chave # 14 - 4
    # print ("%s" % bin(value))[2:-crcLength], ("%s" % bin(value))[-crcLength:]
    # print ("%s" % bin(key))[2:]
    i = 0
    j = 1 << dataLength + crcLength - 1
    while i < dataLength - crcLength + 1:
        while j & value == 0 and i < dataLength-crcLength+1:
            j >>= 1
            key >>= 1
            i += 1
        value = value ^ key
        j >>= 1
        key >>= 1
        i += 1
        # print "v", ("%s" % bin(value))[2:-crcLength], ("%s" % bin(value))[-crcLength:]
        # print "k", ("%s" % bin(key))[2:-crcLength], ("%s" % bin(key))[-crcLength:]
        # print ("%s" % bin(key))[2:]
    return value


def main():
    crc(int('0b11010011101100', 2), int('0b1011', 2), 14, 3)

if __name__ == "__main__":
    main()