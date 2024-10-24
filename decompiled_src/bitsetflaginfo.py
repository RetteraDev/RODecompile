#Embedded file name: /WORKSPACE/data/entities/common/bitsetflaginfo.o
import zlib
import BigWorld
from userInfo import UserInfo

class BitSetFlagInfo(UserInfo):

    def createFromStream(self, stream):
        try:
            return bytearray(zlib.decompress(stream))
        except:
            return bytearray('')

    def addToStream(self, obj):
        obj.rstrip(' ')
        return zlib.compress(str(obj), 3)

    def createObjFromDict(self, d):
        try:
            return bytearray(zlib.decompress(d['data']))
        except:
            return bytearray('')

    def getDictFromObj(self, obj):
        obj.rstrip(' ')
        return {'data': zlib.compress(str(obj))}

    def isSameType(self, obj):
        return type(obj) is bytearray


instance = BitSetFlagInfo()
