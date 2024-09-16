#Embedded file name: I:/bag/tmp/tw2/res/entities\common/itemInfo.o
import utils
from item import Item
from userInfo import UserInfo

class ItemInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = utils.createItemObjFromDict(dict)
        obj.consistent()
        return obj

    def getDictFromObj(self, obj):
        prop = utils.getItemSaveData(obj)
        return prop

    def isSameType(self, obj):
        return type(obj) is Item


instance = ItemInfo()
