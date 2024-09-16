#Embedded file name: I:/bag/tmp/tw2/res/entities\common/socAttributeInfo.o
from userInfo import UserInfo
from socAttribute import SocAttribute

class AttributeInfo(UserInfo):

    def createObjFromDict(self, dict):
        return SocAttribute(dict)

    def getDictFromObj(self, obj):
        return obj.fixedDict

    def isSameType(self, obj):
        return type(obj) is SocAttribute


instance = AttributeInfo()
