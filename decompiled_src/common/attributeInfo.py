#Embedded file name: I:/bag/tmp/tw2/res/entities\common/attributeInfo.o
from userInfo import UserInfo
from attribute import Attribute

class AttributeInfo(UserInfo):

    def createObjFromDict(self, dict):
        return Attribute(dict)

    def getDictFromObj(self, obj):
        return obj.fixedDict

    def isSameType(self, obj):
        return type(obj) is Attribute


instance = AttributeInfo()
