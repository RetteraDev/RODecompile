#Embedded file name: I:/bag/tmp/tw2/res/entities\common/effectInfo.o
from userInfo import UserInfo
from effect import Effect

class EffectInfo(UserInfo):

    def createObjFromDict(self, dict):
        return Effect(dict)

    def getDictFromObj(self, obj):
        return obj.fixedDict

    def isSameType(self, obj):
        return type(obj) is Effect


instance = EffectInfo()
