#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/newMDBConverter.o
import BigWorld
import gamelog
import os
import struct
from cacheMDB import KEY_TYPE_INT
from cacheMDB import KEY_TYPE_TUPLE_INT
from cacheMDB import checkMDBKeyValue
MAX_INT = 2147483647
ATTR_TYPE_INT = 1
ATTR_TYPE_FLOAT = 2
ATTR_TYPE_STR = 3
ATTR_TYPE_EVAL = 4
CONVERT_DATA_FAILED = -1
BINARY_ENCRYPT_NAME = 'tianyu_tool.mdb'
MD5_FILE_NAME = 'tianyu_tool_temp.log'

def getBinaryCachePath():
    return '../game/' + BINARY_ENCRYPT_NAME


MSB = 128
MSBALL = ~127
VARINT_N1 = 128
VARINT_N2 = 16384
VARINT_N3 = 2097152
VARINT_N4 = 268435456
VARINT_N5 = 34359738368L
VARINT_N6 = 4398046511104L
VARINT_N7 = 562949953421312L
VARINT_N8 = 72057594037927936L
VARINT_N9 = 9223372036854775808L

def varintEncodingLength(n):
    if n < VARINT_N1:
        return 1
    if n < VARINT_N2:
        return 2
    if n < VARINT_N3:
        return 3
    if n < VARINT_N4:
        return 4
    if n < VARINT_N5:
        return 5
    if n < VARINT_N6:
        return 6
    if n < VARINT_N7:
        return 7
    if n < VARINT_N8:
        return 8
    if n < VARINT_N9:
        return 9
    raise NotImplemented


def zigZagEncode32(n):
    return n << 1 ^ n >> 31


def zigZagDecode32(n):
    return n >> 1 ^ -(n & 1)


def zigZagEncode64(n):
    return n << 1 ^ n >> 63


def zigZagDecode64(n):
    return n >> 1 ^ -(n & 1)


def varintEncode(n):
    _bytes = []
    while n & MSBALL:
        byte = n & 255 | MSB
        n = n >> 7
        _bytes.append(struct.pack('B', byte))

    _bytes.append(struct.pack('B', n))
    return _bytes


def varint_decode(_bytes):
    result = 0
    bits = 0
    idx = 0
    ptr, = struct.unpack('B', _bytes[idx])
    while ptr & MSB:
        result += (ptr & 127) << bits
        idx = idx + 1
        ptr, = struct.unpack('B', _bytes[idx])
        bits += 7

    result += (ptr & 127) << bits
    return result


def getAttrType(aType):
    if aType == 'I':
        return ATTR_TYPE_INT
    if aType == 'F':
        return ATTR_TYPE_FLOAT
    if aType == 'S':
        return ATTR_TYPE_STR
    if aType == 'E':
        return ATTR_TYPE_EVAL
    raise Exception('%s not implement!' % str(aType))


def getSingleBit(x, index):
    return x & 1 << index


def setSingleBit(x, index, on):
    if on:
        return int(x | 1 << index)
    else:
        return int(x & ~(1 << index))


class MDBDataConverter(object):

    def __init__(self):
        super(MDBDataConverter, self).__init__()
        self.strPoolList = []
        self.strIndexDict = {}
        self.strLen = 0
        self.strPoolUnWriteIdx = 0
        self.moduleOffsets = {}
        self.nowOffset = 0
        self.writedModule = set([])

    def addStringCache(self, stra):
        self.strLen = self.strLen + 1
        if stra not in self.strIndexDict:
            self.strPoolList.append(stra)
            idx = len(self.strPoolList) - 1
            self.strIndexDict[stra] = idx
            return idx
        else:
            return self.strIndexDict[stra]

    def getModuleNameByte(self, keyType, name):
        length = len(name)
        key = 'ii%dsc' % length
        return struct.pack(key, keyType, length + 1, name, ' ')

    def appendModuleAttrByte(self, dataBytes, valueAttrs):
        length = len(valueAttrs)
        dataBytes.append(struct.pack('i', length))
        for i in xrange(len(valueAttrs)):
            keyName = valueAttrs[i][0]
            aType = valueAttrs[i][1]
            packKey = '3h%dsc' % len(keyName)
            attrType = getAttrType(aType)
            byte = struct.pack(packKey, len(keyName) + 1, attrType, i, keyName, ' ')
            dataBytes.append(byte)

    def getKeyByte(self, keyType, key):
        if keyType == KEY_TYPE_INT:
            return [struct.pack('I', key)]
        if keyType == KEY_TYPE_TUPLE_INT:
            return [struct.pack('2I', *key)]
        raise Exception('%s, %s not implemented!' % (str(keyType), str(key)))

    def getValueByteSeperate(self, valueType, value):
        if valueType == 'I':
            zzValue = zigZagEncode64(value)
            return varintEncode(zzValue)
        if valueType == 'F':
            return struct.pack('f', value)
        if valueType == 'S':
            idx = self.addStringCache(value)
            return struct.pack('I', idx)
        if valueType == 'E':
            sValue = str(value)
            idx = self.addStringCache(sValue)
            return struct.pack('I', idx)
        raise Exception('%s %s not implemented!' % (str(valueType), str(value)))

    def setValueFlag(self, flags, index, on):
        x = index / 32
        y = index % 32
        flags[x] = setSingleBit(flags[x], y, on)
        return flags

    def getValueByte(self, valueAttrs, valueDict, flagLength):
        valueBytes = []
        flags = []
        for i in xrange(flagLength):
            flags.append(0)

        seqs = []
        seq = 0
        for valueName, valueType in valueAttrs:
            if valueDict.has_key(valueName):
                valueByte = self.getValueByteSeperate(valueType, valueDict.get(valueName))
                if isinstance(valueByte, list):
                    valueBytes.extend(valueByte)
                else:
                    valueBytes.append(valueByte)
                flags = self.setValueFlag(flags, seq, 1)
                seqs.append(seq)
            seq = seq + 1

        packKey = '%dI' % flagLength
        return [struct.pack(packKey, *flags)] + valueBytes

    def appendModuleValueByte(self, dataBytes, data, keyType, name, attrs, valueAttrs):
        dataBytes.append(struct.pack('I', 0))
        numIndex = len(dataBytes)
        i = 0
        length = len(valueAttrs) / 32 + 1
        for key, value in data.iteritems():
            if not checkMDBKeyValue(keyType, key, value):
                continue
            keyByte = self.getKeyByte(keyType, key)
            dataBytes.extend(keyByte)
            valueByte = self.getValueByte(valueAttrs, value, length)
            dataBytes.extend(valueByte)
            i = i + 1

        dataBytes[numIndex - 1] = struct.pack('I', i)
        return dataBytes

    def getSepStrPoolByte(self):
        byteList = []
        byteList.append(struct.pack('I', len(self.strPoolList) - self.strPoolUnWriteIdx))
        for idx in xrange(self.strPoolUnWriteIdx, len(self.strPoolList)):
            strValue = self.strPoolList[idx]
            packKey = 'i%dsc' % len(strValue)
            byte = struct.pack(packKey, len(strValue) + 1, strValue, ' ')
            byteList.append(byte)

        return byteList

    def seekStrPool(self):
        self.strPoolUnWriteIdx = len(self.strPoolList)

    def getModuleLenBytes(self, datas):
        return [struct.pack('I', len(datas))]

    def convertDataToBytes(self, data, keyType, name, attrs, valueAttrs):
        dataBytes = [struct.pack('I', 0)]
        nameBytes = self.getModuleNameByte(keyType, name)
        dataBytes.append(nameBytes)
        self.appendModuleAttrByte(dataBytes, valueAttrs)
        self.appendModuleValueByte(dataBytes, data, keyType, name, attrs, valueAttrs)
        kvBytes = self.getSepStrPoolByte()
        self.seekStrPool()
        dataBytes.extend(kvBytes)
        return dataBytes

    def getEncryptor(self):
        from Crypto.Cipher import AES
        password = 'binaryData@#&~@1'
        return AES.new(password, AES.MODE_ECB)

    def pad(self, s):
        from Crypto.Cipher import AES
        BS = AES.block_size
        return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    def encryptStr(self, inStr, out_filename, chunksize, moduleName):
        encryptor = self.getEncryptor()
        lengthToEnc = len(inStr)
        start = 0
        with open(out_filename, 'ab') as outfile:
            while True:
                if lengthToEnc <= 0:
                    break
                chunk = inStr[start:start + chunksize]
                start += chunksize
                lengthToEnc -= chunksize
                encryptContent = encryptor.encrypt(chunk)
                outfile.write(encryptContent)

        self.nowOffset = self.nowOffset + len(inStr)
        self.writedModule.add(moduleName)

    def deCryptFile(self, filePath):
        encryptor = self.getEncryptor()
        fileSize = os.path.getsize(filePath)
        gamelog.debug('m.l@MDBDataConverter.deCryptFile', filePath, fileSize)
        array = []
        with open(filePath, 'rb') as f:
            size = 0
            while size < fileSize:
                f.seek(size)
                chunk = f.read(16)
                size = size + 16
                byte = encryptor.decrypt(chunk)
                array.append(byte)

        with open('decrpteFile.log', 'ab') as outfile:
            for a in array:
                outfile.write(a)

    def decryptModule(self, filePath):
        fileSize = os.path.getsize(filePath)
        with open(filePath, 'rb') as f:
            bytes = f.read()
            offset = 0
            moduleLen, = struct.unpack('i', bytes[offset:offset + 4])
            moduleNum = 0
            while moduleLen > 0:
                keyType, nameLen = struct.unpack('ii', bytes[offset + 4:offset + 12])
                nameKey = '%ds' % nameLen
                name, = struct.unpack(nameKey, bytes[offset + 12:offset + 12 + nameLen])
                logMsg = 'm.l@MDBDataConverter.deCrypt module idx:%d, len:%d, type:%d, %s, %x, %x' % (moduleNum,
                 moduleLen,
                 keyType,
                 name,
                 offset,
                 offset + moduleLen)
                gamelog.debug(logMsg)
                moduleNum = moduleNum + 1
                offset = offset + moduleLen
                moduleLen, = struct.unpack('i', bytes[offset:offset + 4])
                if moduleLen == MAX_INT:
                    version, = struct.unpack('i', bytes[offset + 4:offset + 8])
                    gamelog.debug('m.l@MDBDataConverter.decryptModule over version:', version)
                    break

    def encryptDataStr(self, bytes, moduleName):
        inStr = ''.join(bytes)
        self.encryptStr(inStr, BINARY_ENCRYPT_NAME, 65536, moduleName)

    def getStringPoolBytes(self):
        byteList = []
        byteList.append(struct.pack('I', len(self.strPoolList)))
        for stra in self.strPoolList:
            packKey = 'i%dsc' % len(stra)
            byte = struct.pack(packKey, len(stra) + 1, stra, ' ')
            byteList.append(byte)

        return byteList

    def isExportedKey(self, module, key):
        for valueAttr in module.valueAttrs:
            if valueAttr[0] == key:
                return True

        return False

    def writeExtraPy(self, module):
        new_dict = {}
        new_dict.update(module.data)
        keys = new_dict.keys()
        for k in keys:
            v = new_dict.get(k)
            if type(v) == dict:
                keys = v.keys()
                for key in keys:
                    if self.isExportedKey(module, key):
                        del v[key]

                if not v:
                    del new_dict[k]

        with open(module.__name__ + '_extra.py', 'w') as f:
            f.write('# -*- coding: gbk -*-\n')
            f.write('data = ' + str(new_dict))
            f.write('\n')

    def releaseStrPool(self):
        self.strPoolList = []
        self.strIndexDict = {}
        self.moduleOffsets = {}

    def isPublishedVersion(self):
        return hasattr(BigWorld, 'isPublishedVersion') and BigWorld.isPublishedVersion()

    def getNewMDBVersion(self, f, fileSize):
        if fileSize < 16:
            return None
        f.seek(fileSize - 16)
        chunk = f.read(16)
        encryptor = self.getEncryptor()
        byte = encryptor.decrypt(chunk)
        revision, = struct.unpack('I', byte[4:8])
        return revision

    def writeMDBModule(self, data, keyType, name, attrs, valueAttrs):
        gamelog.debug('m.l@MDBDataConverter.writeMDBModule', name)
        if name in self.writedModule:
            gamelog.debug('m.l@MDBDataConverter.writeMDBModule already', name)
            return
        moduleBytes = self.convertDataToBytes(data, keyType, name, attrs, valueAttrs)
        length = 0
        for i in moduleBytes:
            length = length + len(i)

        if length % 16 != 0:
            moduleBytes.append(' ' * (16 - length % 16))
            length = length + (16 - length % 16)
        moduleBytes[0] = struct.pack('I', length)
        self.encryptDataStr(moduleBytes, name)

    def writeMDBEnd(self):
        from data import datarevision
        gamelog.debug('m.l@MDBDataConverter.writeMDBEnd', int(datarevision.REVISION) % 2147483647)
        moduleBytes = [struct.pack('II', 2147483647, int(datarevision.REVISION) % 2147483647) + '        ']
        self.encryptDataStr(moduleBytes, '')
        self.releaseStrPool()


MDBConverter = MDBDataConverter()
