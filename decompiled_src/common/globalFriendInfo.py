#Embedded file name: I:/bag/tmp/tw2/res/entities\common/globalFriendInfo.o
from userInfo import UserInfo
from globalFriend import GlobalFriend

class GlobalFriendInfo(UserInfo):

    def createObjFromDict(self, dict):
        return GlobalFriend.createInstance(dict)

    def getDictFromObj(self, obj):
        return obj.getDTO()

    def isSameType(self, obj):
        return type(obj) is GlobalFriend


instance = GlobalFriendInfo()
