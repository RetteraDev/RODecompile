#Embedded file name: I:/bag/tmp/tw2/res/entities\common/wushuangInfo.o
from userInfo import UserInfo
from wushuang import Wushuang

class WushuangInfo(UserInfo):

    def createObjFromDict(self, dict):
        return Wushuang(dict)

    def getDictFromObj(self, obj):
        return obj.fixedDict

    def isSameType(self, obj):
        return type(obj) is Wushuang


instance = WushuangInfo()
