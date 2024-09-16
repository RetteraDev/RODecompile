#Embedded file name: I:/bag/tmp/tw2/res/entities\common/safeModeInfo.o
from userInfo import UserInfo
from safeMode import SafeMode

class SafeModeInfo(UserInfo):

    def createObjFromDict(self, dic):
        sminfo = SafeMode(dic)
        return sminfo

    def getDictFromObj(self, obj):
        return obj.fixedDict

    def isSameType(self, obj):
        return type(obj) is SafeMode


instance = SafeModeInfo()
