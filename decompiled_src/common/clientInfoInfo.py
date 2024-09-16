#Embedded file name: I:/bag/tmp/tw2/res/entities\common/clientInfoInfo.o
from userInfo import UserInfo
from clientInfo import ClientInfo

class ClientInfoInfo(UserInfo):

    def createObjFromDict(self, dict):
        return ClientInfo(dict)

    def getDictFromObj(self, obj):
        return obj.fixedDict

    def isSameType(self, obj):
        return type(obj) is ClientInfo


instance = ClientInfoInfo()
