#Embedded file name: I:/bag/tmp/tw2/res/entities\common/physiqueInfo.o
from userInfo import UserInfo
from physique import Physique

class PhysiqueInfo(UserInfo):

    def createObjFromDict(self, dict):
        return Physique(dict)

    def getDictFromObj(self, obj):
        return obj.fixedDict

    def isSameType(self, obj):
        return type(obj) is Physique


instance = PhysiqueInfo()
