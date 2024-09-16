#Embedded file name: /WORKSPACE/data/entities/common/summonspriteappearanceinfo.o
from summonSpriteAppearance import SummonSpriteAppearanceVal, SummonSpriteAppearanceDict
from userInfo import UserInfo

class SummonSpriteAppearanceDictInfo(UserInfo):

    def createObjFromDict(self, dict):
        apDict = SummonSpriteAppearanceDict()
        if dict and dict.has_key('data') and dict['data']:
            for aVal in dict['data']:
                apList = SummonSpriteAppearanceVal(aVal['spriteId'])
                apList.curUseDict = aVal['curUseDict']
                apList.hasList.extend(aVal['hasList'])
                apList.tempDict.update(aVal['tempDict'])
                apDict[apList.spriteId] = apList

        return apDict

    def getDictFromObj(self, obj):
        data = []
        for apList in obj.itervalues():
            data.append({'spriteId': apList.spriteId,
             'hasList': apList.hasList,
             'curUseDict': apList.curUseDict,
             'tempDict': apList.tempDict})

        return {'data': data}

    def isSameType(self, obj):
        return type(obj) is SummonSpriteAppearanceDict


instance = SummonSpriteAppearanceDictInfo()
