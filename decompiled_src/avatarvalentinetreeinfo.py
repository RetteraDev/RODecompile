#Embedded file name: /WORKSPACE/data/entities/common/avatarvalentinetreeinfo.o
import gamelog
from userInfo import UserInfo
from userSoleType import UserSoleType

class AvatarValentineTree(UserSoleType):

    def __init__(self):
        self.dailyStealCount = 0
        self.canWatering = True
        self.fruitNum = 0
        self.treePos = (0, 0, 0)
        self.partner = 0
        self.treeEntityId = 0
        self.createTime = 0


class AvatarValentineTreeInfo(UserInfo):

    def createObjFromDict(self, objDict):
        obj = AvatarValentineTree()
        if objDict.has_key('dailyStealCount'):
            obj.dailyStealCount = objDict['dailyStealCount']
        if objDict.has_key('canWatering'):
            obj.canWatering = objDict['canWatering']
        if objDict.has_key('fruitNum'):
            obj.fruitNum = objDict['fruitNum']
        if objDict.has_key('treePos'):
            obj.treePos = objDict['treePos']
        if objDict.has_key('partner'):
            obj.partner = objDict['partner']
        if objDict.has_key('treeEntityId'):
            obj.treeEntityId = objDict['treeEntityId']
        if objDict.has_key('createTime'):
            obj.createTime = objDict['createTime']
        if objDict.has_key('canHarvest'):
            obj.canHarvest = objDict['canHarvest']
        return obj

    def getDictFromObj(self, obj):
        objDict = {}
        objDict['dailyStealCount'] = obj.dailyStealCount
        objDict['canWatering'] = obj.canWatering
        objDict['fruitNum'] = obj.fruitNum
        objDict['treePos'] = obj.treePos
        objDict['partner'] = obj.partner
        objDict['treeEntityId'] = obj.treeEntityId
        objDict['createTime'] = obj.createTime
        objDict['canHarvest'] = obj.canHarvest
        return objDict

    def isSameType(self, obj):
        return type(obj) is AvatarValentineTree


instance = AvatarValentineTreeInfo()
