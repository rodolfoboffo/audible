def crc(value, key, dataLength, crcLength, initialFiller=0):
    value = (value << crcLength) + initialFiller # tamanho da chave - 1
    key = key << (dataLength-1) # tamanho do dado - tamanho da chave # 14 - 4
    # print "v", ("%s" % bin(value))[2:-crcLength], ("%s" % bin(value))[-crcLength:]
    # print "k", ("%s" % bin(key))[2:]
    j = 1 << dataLength + crcLength - 1
    for i in range(dataLength - 1):
        if j & value != 0:
            value = value ^ key
        j >>= 1
        key >>= 1
        # print "v", ("%s" % bin(value))[2:-crcLength], ("%s" % bin(value))[-crcLength:]
        # print "k", ("%s" % bin(key))[2:-crcLength], ("%s" % bin(key))[-crcLength:]
    return value

def crcCheck(value, c, key, dataLength, crcLength):
    return crc(value, key, dataLength, crcLength, initialFiller=c) == 0

def main():
    c = crc(int("0b11010011101100", 2), int("0b1011", 2), 14, 3)
    print(bin(c))
    # print bin(crc(int('0b1100000110000000', 2), int('0b10001001', 2), 16, 7))
    print(crcCheck(int("0b11010011101100", 2), c, int("0b1011", 2), 14, 3))

if __name__ == "__main__":
    main()