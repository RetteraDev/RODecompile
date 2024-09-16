#Embedded file name: I:/bag/tmp/tw2/res/entities\common/wingWorldSoulBossInfo.o
from wingWorldSoulBoss import WingWorldSoulBossVal, WingWorldSoulBoss
from userInfo import UserInfo

class WingWorldSoulBossInfo(UserInfo):

    def __init__(self):
        pass

    def createObjFromDict(self, dict):
        obj = WingWorldSoulBoss()
        for child in dict['soulBoss']:
            cfgId = child['cfgId']
            state = child.get('state', 0)
            monument = child.get('monument', None)
            bossVal = WingWorldSoulBossVal(cfgId)
            bossVal.state = state
            bossVal.monumentData = monument
            obj[cfgId] = bossVal

        return obj

    def getDictFromObj(self, obj):
        soulBoss = []
        for bossVal in obj.itervalues():
            monument = {}
            if bossVal.monumentData:
                monument['npcId'] = bossVal.monumentData.get('npcId', 0)
                monument['spaceNo'] = bossVal.monumentData.get('spaceNo')
                monument['position'] = bossVal.monumentData.get('position')
                monument['direction'] = bossVal.monumentData.get('direction')
                monument['args'] = bossVal.monumentData.get('args')
            soulBoss.append({'cfgId': bossVal.cfgId,
             'state': bossVal.state,
             'monument': monument})

        return {'soulBoss': soulBoss}

    def isSameType(self, obj):
        return type(obj) is WingWorldSoulBoss


instance = WingWorldSoulBossInfo()
