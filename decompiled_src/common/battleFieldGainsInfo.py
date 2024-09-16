#Embedded file name: I:/bag/tmp/tw2/res/entities\common/battleFieldGainsInfo.o
import BigWorld
from userInfo import UserInfo
from battleFieldGains import BattleFieldGains, BattleFieldGainItem
if BigWorld.component == 'client':
    from iStreamInfoCommon import bindStream
else:
    from iStreamInfo import bindStream

class BattleFieldGainsInfo(UserInfo):

    def createObjFromDict(self, dict):
        battleFieldGains = BattleFieldGains(fame=dict['fame'], addedFame=dict['addedFame'], streakKill=dict['streakKill'])
        for child in dict['details']:
            dVal = BattleFieldGainItem(loseMatch=child['loseMatch'], winMatch=child['winMatch'], duelMatch=child['duelMatch'], killCount=child['killCount'], dieCount=child['dieCount'])
            battleFieldGains[child['fbNo']] = dVal

        return battleFieldGains

    def getDictFromObj(self, obj):
        dVals = []
        for fbNo, tVal in obj.iteritems():
            dVals.append({'fbNo': fbNo,
             'loseMatch': tVal.loseMatch,
             'winMatch': tVal.winMatch,
             'duelMatch': tVal.duelMatch,
             'killCount': tVal.killCount,
             'dieCount': tVal.dieCount})

        return {'details': dVals,
         'fame': obj.fame,
         'addedFame': obj.addedFame,
         'streakKill': obj.streakKill}

    def _createObjFromStream(self, stream):
        details, fame, addedFame, streakKill = stream
        battleFieldGains = BattleFieldGains(fame=fame, addedFame=addedFame, streakKill=streakKill)
        for fbNo, loseMatch, winMatch, duelMatch, killCount, dieCount in details:
            dVal = BattleFieldGainItem(loseMatch=loseMatch, winMatch=winMatch, duelMatch=duelMatch, killCount=killCount, dieCount=dieCount)
            battleFieldGains[fbNo] = dVal

        return battleFieldGains

    def _getStreamFromObj(self, obj):
        return ([ (fbNo,
          x.loseMatch,
          x.winMatch,
          x.duelMatch,
          x.killCount,
          x.dieCount) for fbNo, x in obj.iteritems() ],
         obj.fame,
         obj.addedFame,
         obj.streakKill)

    def isSameType(self, obj):
        return type(obj) is BattleFieldGains


instance = BattleFieldGainsInfo()
bindStream(instance)
