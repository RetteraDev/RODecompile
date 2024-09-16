#Embedded file name: I:/bag/tmp/tw2/res/entities\common/summonedSpriteAccessoryInfo.o
from summonedSpriteAccessory import SummonedSpriteAccessory
from userInfo import UserInfo

class SummonedSpriteAccessoryInfo(UserInfo):

    def createObjFromDict(self, dic):
        summonedSpriteAccessory = SummonedSpriteAccessory()
        for part, data in dic['accessoryDict'].iteritems():
            summonedSpriteAccessory[part] = data

        summonedSpriteAccessory.templateId = dic['templateId']
        summonedSpriteAccessory.learnedTemplate = dic['learnedTemplate']
        return summonedSpriteAccessory

    def getDictFromObj(self, obj):
        accessoryDict = {}
        for part, data in obj.iteritems():
            accessoryDict[part] = data

        return {'templateId': obj.templateId,
         'accessoryDict': accessoryDict,
         'learnedTemplate': obj.learnedTemplate}

    def isSameType(self, obj):
        return type(obj) is SummonedSpriteAccessory


instance = SummonedSpriteAccessoryInfo()
