#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/PNGEncode.o
import binascii
import os
import cPickle

class PNGEncode(object):
    """\xbd\xe2\xce\xf6png\xcd\xbc\xc6\xac\xa3\xac\xc8\xbb\xba\xf3\xbf\xc9\xd2\xd4\xd4\xdapng\xcd\xbc\xc6\xac\xb5\xc4IEND\xca\xfd\xbe\xdd\xbf\xe9\xc0\xef\xc8\xa1\xca\xfd\xbe\xdd"""
    PNG_END_TAG = 'IEND'
    PNG_BEGIN_HEAD = 9894494448401390090L
    HEAD_LEN = 8
    TAG_LEN = 4
    CRC_LEN = 4

    def __init__(self):
        self.pathName = None
        self.file = None

    def open(self, pathName):
        try:
            self.pathName = pathName
            self.file = open(pathName, 'rb+')
        except:
            self.file = None

    def findInstertPosition(self):
        if not self.file:
            return -1
        self.file.seek(0, os.SEEK_SET)
        begin = self.file.read(self.HEAD_LEN)
        if int(binascii.b2a_hex(begin), 16) != self.PNG_BEGIN_HEAD:
            return -1
        while True:
            data = self.file.read(8)
            if not data:
                return -1
            l = int(binascii.b2a_hex(data[0:4]), 16)
            tag = data[4:]
            if tag == self.PNG_END_TAG:
                return self.file.tell() - 8
            self.file.seek(l + self.CRC_LEN, os.SEEK_CUR)

    def insertExtraData(self, data):
        pos = self.findInstertPosition()
        if pos == -1:
            return
        self.file.seek(pos, os.SEEK_SET)
        data = cPickle.dumps(data)
        l = len(data)
        self.file.write(binascii.a2b_hex(self.intToHexStr(l)))
        self.file.write(self.PNG_END_TAG)
        self.file.write(data)
        crc = self.crc32(self.PNG_END_TAG + data)
        self.file.write(binascii.a2b_hex(self.intToHexStr(crc)))

    def getExtraData(self):
        pos = self.findInstertPosition()
        if pos == -1:
            return {}
        self.file.seek(pos, os.SEEK_SET)
        data = self.file.read(8)
        if not data:
            return None
        l = int(binascii.b2a_hex(data[0:4]), 16)
        if not l:
            return {}
        data = self.file.read(l)
        data = cPickle.loads(data)
        return data

    def intToHexStr(self, x):
        s = '%08x' % x
        return s

    def crc32(self, data):
        return binascii.crc32(data) & 4294967295L

    def save(self):
        if self.file:
            self.file.close()
            self.file = None
            self.pathName = None

    def calMD5(self):
        if self.file:
            return 1
        return 0

    def insertMD5(self):
        md5 = self.calMD5()
        if md5:
            self.insertExtraData({'md5': md5})

    def getMd5(self):
        data = self.getExtraData()
        if data.has_key('md5'):
            return data['md5']
        return ''

    def hasMd5(self):
        data = self.getExtraData()
        return data.has_key('md5')


if __name__ == '__main__':
    coder = PNGEncode()
    coder.open('2.png')
    data = {1: 2}
    coder.insertExtraData(data)
    data = coder.getExtraData()
    print 'data %s\n' % data
