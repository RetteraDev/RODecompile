#Embedded file name: I:/bag/tmp/tw2/res/entities\common/spriteWingWorldResInfo.o
from spriteWingWorldRes import SpriteWingWorldRes, SpriteWingWorldResVal
from userInfo import UserInfo

class SpriteWingWorldResInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = SpriteWingWorldRes()
        data = dict['data'][0]
        obj.resDictCurrent = data['resDictCurrent']
        obj.fameCurrent = data['fameCurrent']
        obj.specialRareLv = data['specialRareLv']
        obj.specialCntDay = data['specialCntDay']
        obj.maxSpeed = data['maxSpeed']
        obj.resetDailyTime = data['resetDailyTime']
        obj.resTotalDay = data['resTotalDay']
        for each in data['spriteInSlots']:
            eObj = SpriteWingWorldResVal()
            eObj.spriteIndex = each['spriteIndex']
            eObj.lastCalcTime = each['lastCalcTime']
            eObj.remainCalcCnt = each['remainCalcCnt']
            obj.spriteInSlots[each['slotIndex']] = eObj

        return obj

    def getDictFromObj(self, obj):
        data = {'resDictCurrent': obj.resDictCurrent,
         'fameCurrent': obj.fameCurrent,
         'unlockedSlots': obj.unlockedSlots,
         'specialRareLv': obj.specialRareLv,
         'specialCntDay': obj.specialCntDay,
         'maxSpeed': obj.maxSpeed,
         'resetDailyTime': obj.resetDailyTime,
         'resTotalDay': obj.resTotalDay}
        spriteInSlots = []
        for slotIndex, spriteVal in obj.spriteInSlots.iteritems():
            spriteInSlots.append({'spriteIndex': spriteVal.spriteIndex,
             'lastCalcTime': spriteVal.lastCalcTime,
             'slotIndex': slotIndex,
             'remainCalcCnt': spriteVal.remainCalcCnt})

        data['spriteInSlots'] = spriteInSlots
        return {'data': [data]}

    def isSameType(self, obj):
        return type(obj) is SpriteWingWorldRes


instance = SpriteWingWorldResInfo()
