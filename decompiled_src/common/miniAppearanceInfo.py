#Embedded file name: I:/bag/tmp/tw2/res/entities\common/miniAppearanceInfo.o
from userInfo import UserInfo
from miniAppearance import MiniAppearance

class MiniAppearanceInfo(UserInfo):

    def createObjFromDict(self, dict):
        return MiniAppearance(dict)

    def getDictFromObj(self, obj):
        return obj.fixedDict

    def isSameType(self, obj):
        return type(obj) is MiniAppearance


instance = MiniAppearanceInfo()
