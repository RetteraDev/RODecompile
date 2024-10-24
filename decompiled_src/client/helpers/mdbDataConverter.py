#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/mdbDataConverter.o
import BigWorld
import MemoryDB
import gamelog
import os
import struct
import cacheMDB
ATTR_TYPE_INT = 1
ATTR_TYPE_FLOAT = 2
ATTR_TYPE_STR = 3
ATTR_TYPE_EVAL = 4
CONVERT_DATA_FAILED = -1
BINARY_DIR = 'datacache'
BINARY_NAME = 'cache.data'
NEW_FLAG_FILE_PATH = 'new'
BINARY_ENCRYPT_NAME = 'tianyu_tool.log'

def getBinaryCachePath():
    if hasattr(MemoryDB, 'withEncrypt'):
        return '../game/' + BINARY_ENCRYPT_NAME
    else:
        return '../game/' + BINARY_DIR + '/' + BINARY_NAME


def getNewFlagPath():
    return '../game/' + BINARY_DIR + '/' + NEW_FLAG_FILE_PATH


def createNewFlagFile(isNew):
    with open(BINARY_DIR + '/' + NEW_FLAG_FILE_PATH, 'wb') as f:
        f.write(isNew)


try:
    os.mkdir(BINARY_DIR)
except:
    pass

WITH_VARINT_FUNC = False
if hasattr(MemoryDB, 'withVarInt'):
    WITH_VARINT_FUNC = True
USE_VARINT = True
if not WITH_VARINT_FUNC:
    USE_VARINT = False
MSB = 128
MSBALL = -128
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

    def getModuleAttrByte(self, valueAttrs):
        attrBytes = []
        length = len(valueAttrs)
        attrBytes.append(struct.pack('i', length))
        for i in xrange(len(valueAttrs)):
            keyName = valueAttrs[i][0]
            aType = valueAttrs[i][1]
            packKey = '3h%dsc' % len(keyName)
            attrType = getAttrType(aType)
            byte = struct.pack(packKey, len(keyName) + 1, attrType, i, keyName, ' ')
            attrBytes.append(byte)

        return attrBytes

    def getKeyByte(self, keyType, key):
        if keyType == cacheMDB.KEY_TYPE_INT:
            return [struct.pack('I', key)]
        if keyType == cacheMDB.KEY_TYPE_TUPLE_INT:
            return [struct.pack('2I', *key)]
        raise Exception('%s, %s not implemented!' % (str(keyType), str(key)))

    def getValueByteSeperate(self, valueType, value):
        if valueType == 'I':
            if USE_VARINT:
                zzValue = zigZagEncode64(value)
                return varintEncode(zzValue)
            else:
                return struct.pack('i', value)
        else:
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

    def getModuleValueByte(self, module):
        dataBytes = []
        i = 0
        keyType = module.keyType
        valueAttrs = module.valueAttrs
        length = len(valueAttrs) / 32 + 1
        for key, value in module.data.iteritems():
            if not cacheMDB.checkMDBKeyValue(keyType, key, value):
                continue
            keyByte = self.getKeyByte(keyType, key)
            dataBytes.extend(keyByte)
            valueByte = self.getValueByte(valueAttrs, value, length)
            dataBytes.extend(valueByte)
            i = i + 1

        return [struct.pack('I', i)] + dataBytes

    def getModuleLenBytes(self, datas):
        return [struct.pack('I', len(datas))]

    def convertDataToBytes(self, module):
        if not module.data:
            raise Exception('data empty!')
        if not hasattr(module, 'keyType'):
            raise Exception('keyType empty!')
        if not hasattr(module, 'valueAttrs'):
            raise Exception('valueAttrs empty!')
        dataBytes = []
        name = self.getModuleName(module)
        nameBytes = self.getModuleNameByte(module.keyType, name)
        dataBytes.append(nameBytes)
        attrBytes = self.getModuleAttrByte(module.valueAttrs)
        dataBytes.extend(attrBytes)
        kvBytes = self.getModuleValueByte(module)
        dataBytes.extend(kvBytes)
        return dataBytes

    def writeNewFlagFile(self):
        with open(BINARY_DIR + '/' + NEW_FLAG_FILE_PATH, 'w') as f:
            if USE_VARINT:
                f.write('1')
            else:
                f.write('0')

    def getBinaryDataPath(self):
        return BINARY_DIR + '/' + BINARY_NAME

    def getEncryptor(self):
        from Crypto.Cipher import AES
        password = 'binaryData@#&~@1'
        return AES.new(password, AES.MODE_ECB)

    def pad(self, s):
        from Crypto.Cipher import AES
        BS = AES.block_size
        return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    def encryptStr(self, inStr, out_filename, datarevision, chunksize = 65536):
        encryptor = self.getEncryptor()
        enccontent = []
        lengthToEnc = len(inStr)
        start = 0
        i = 0
        while True:
            if lengthToEnc <= 0:
                break
            chunk = inStr[start:start + chunksize]
            start += chunksize
            lengthToEnc -= chunksize
            if len(chunk) % 16 != 0:
                chunk += ' ' * (16 - len(chunk) % 16)
            enccontent.append(encryptor.encrypt(chunk))
            i = i + 1

        enccontent.append(encryptor.encrypt(struct.pack('I', datarevision) + '            '))
        filePath = getBinaryCachePath()
        if os.path.exists(filePath):
            return
        with open(out_filename, 'wb') as outfile:
            outfile.writelines(enccontent)

    def encryptDataStr(self, bytes, datarevision):
        inStr = ''.join(bytes)
        self.encryptStr(inStr, BINARY_ENCRYPT_NAME, datarevision)

    def writeBytesToFile(self, abytes, datarevision):
        if hasattr(MemoryDB, 'withEncrypt'):
            return
        relativePath = self.getBinaryDataPath()
        with open(relativePath, 'wb') as f:
            f.writelines(abytes)
            f.write(struct.pack('I', datarevision))

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

    def getModuleName(self, module):
        return '_'.join(module.__name__.split('.'))

    def releaseStrPool(self):
        self.strPoolList = []
        self.strIndexDict = {}

    def thinData(self, modules):
        for module in modules:
            name = self.getModuleName(module)
            module.data = cacheMDB.convert_to_bytes_dict(module.data, module.keyType, name, module.attrs)
            module.attrs = None
            module.valueAttrs = None

    def isPublishedVersion(self):
        return hasattr(BigWorld, 'isPublishedVersion') and BigWorld.isPublishedVersion()

    def getRevision(self, f, fileSize):
        revision = 0
        if hasattr(MemoryDB, 'withEncrypt'):
            f.seek(fileSize - 16)
            chunk = f.read(16)
            encryptor = self.getEncryptor()
            byte = encryptor.decrypt(chunk)
            revision, = struct.unpack('I', byte[0:4])
        else:
            f.seek(fileSize - 4)
            revision, = struct.unpack('I', f.read(-1))
        return revision

    def convertData(self, modules, datarevision):
        filePath = getBinaryCachePath()
        try:
            if os.path.exists(filePath):
                needRemoveFile = False
                fileSize = os.path.getsize(filePath)
                with open(filePath, 'rb') as f:
                    revision = self.getRevision(f, fileSize)
                    if revision == datarevision:
                        if self.isPublishedVersion():
                            return
                        fileTime = os.stat(filePath).st_mtime
                        for module in modules:
                            moduleFileName = module.__file__
                            if moduleFileName[-3:] == 'pyc':
                                moduleFilePy = moduleFileName[0:-1]
                            elif moduleFileName[-2:] == 'py':
                                moduleFilePy = moduleFileName
                            else:
                                continue
                            if os.path.exists(moduleFilePy) and os.stat(moduleFilePy).st_mtime > fileTime:
                                needRemoveFile = True
                                break

                    else:
                        needRemoveFile = True
                if needRemoveFile:
                    os.remove(filePath)
                else:
                    return
        except Exception as e:
            gamelog.debug('@m.l convertData', e.message)
            return CONVERT_DATA_FAILED

        abytes = self.getModuleLenBytes(modules)
        for module in modules:
            temp = self.convertDataToBytes(module)
            abytes.extend(temp)
            module.valueAttrs = None

        stringPoolBytes = self.getStringPoolBytes()
        abytes.extend(stringPoolBytes)
        self.writeBytesToFile(abytes, datarevision)
        abytes.append(struct.pack('I', datarevision))
        self.encryptDataStr(abytes, datarevision)
        self.releaseStrPool()
