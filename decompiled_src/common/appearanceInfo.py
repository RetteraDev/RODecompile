#Embedded file name: I:/bag/tmp/tw2/res/entities\common/appearanceInfo.o
from userInfo import UserInfo
from appearance import Appearance

class AppearanceInfo(UserInfo):

    def createObjFromDict(self, dict):
        return Appearance(dict)

    def getDictFromObj(self, obj):
        return obj.fixedDict

    def isSameType(self, obj):
        return type(obj) is Appearance


instance = AppearanceInfo()
