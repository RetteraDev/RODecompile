#Embedded file name: /WORKSPACE/data/entities/common/lunzhanyundianinfo.o
import gamelog
from userInfo import UserInfo
from userSoleType import UserSoleType

class LunZhanYunDian(UserSoleType):

    def __init__(self):
        self.damage = 0
        self.cure = 0
        self.killCount = 0
        self.assistCount = 0
        self.victoryRound = 0
        self.arenaMode = 0
        self.lzydApplyTime = 0
        self.lzydApplyType = 0
        self.singleDamage = 0
        self.singleCure = 0


class LunZhanYunDianInfo(UserInfo):

    def createObjFromDict(self, objDict):
        obj = LunZhanYunDian()
        if objDict.has_key('damage'):
            obj.damage = objDict['damage']
        if objDict.has_key('cure'):
            obj.cure = objDict['cure']
        if objDict.has_key('killCount'):
            obj.killCount = objDict['killCount']
        if objDict.has_key('assistCount'):
            obj.assistCount = objDict['assistCount']
        if objDict.has_key('victoryRound'):
            obj.victoryRound = objDict['victoryRound']
        if objDict.has_key('arenaMode'):
            obj.arenaMode = objDict['arenaMode']
        if objDict.has_key('lzydApplyTime'):
            obj.lzydApplyTime = objDict['lzydApplyTime']
        if objDict.has_key('lzydApplyType'):
            obj.lzydApplyType = objDict['lzydApplyType']
        if objDict.has_key('singleDamage'):
            obj.lzydApplyType = objDict['singleDamage']
        if objDict.has_key('singleCure'):
            obj.lzydApplyType = objDict['singleCure']
        return obj

    def getDictFromObj(self, obj):
        objDict = {}
        objDict['damage'] = obj.damage
        objDict['cure'] = obj.cure
        objDict['killCount'] = obj.killCount
        objDict['assistCount'] = obj.assistCount
        objDict['victoryRound'] = obj.victoryRound
        objDict['arenaMode'] = obj.arenaMode
        objDict['lzydApplyTime'] = obj.lzydApplyTime
        objDict['lzydApplyType'] = obj.lzydApplyType
        objDict['singleDamage'] = obj.singleDamage
        objDict['singleCure'] = obj.singleCure
        return objDict

    def isSameType(self, obj):
        return type(obj) is LunZhanYunDian


instance = LunZhanYunDianInfo()
