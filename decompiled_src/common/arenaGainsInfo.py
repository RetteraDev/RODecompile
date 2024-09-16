#Embedded file name: I:/bag/tmp/tw2/res/entities\common/arenaGainsInfo.o
from userInfo import UserInfo
from arenaGains import ArenaGains, ArenaGainItem

class ArenaGainsInfo(UserInfo):

    def createObjFromDict(self, dict):
        arenaGains = ArenaGains(arenaScore=dict['arenaScore'], arenaLevel=dict['arenaLevel'], streak=dict['streak'], weekPlayCnt=dict['weekPlayCnt'], weekExchangeFameFlag=dict['weekExchangeFameFlag'], lastOutTime=dict['lastOutTime'])
        if dict.has_key('curSeason'):
            arenaGains.curSeason = dict['curSeason']
        if dict.has_key('curLevel'):
            arenaGains.curLevel = dict['curLevel']
        for child in dict['details']:
            dVal = ArenaGainItem(loseMatch=child['loseMatch'], winMatch=child['winMatch'], duelMatch=child['duelMatch'], killCount=child['killCount'], dieCount=child['dieCount'])
            arenaGains[child['arenaMode']] = dVal

        return arenaGains

    def getDictFromObj(self, obj):
        dVals = []
        for arenaMode, tVal in obj.iteritems():
            dVals.append({'arenaMode': arenaMode,
             'loseMatch': tVal.loseMatch,
             'winMatch': tVal.winMatch,
             'duelMatch': tVal.duelMatch,
             'killCount': tVal.killCount,
             'dieCount': tVal.dieCount})

        return {'details': dVals,
         'arenaScore': obj.arenaScore,
         'arenaLevel': obj.arenaLevel,
         'streak': obj.streak,
         'weekPlayCnt': obj.weekPlayCnt,
         'weekExchangeFameFlag': obj.weekExchangeFameFlag,
         'lastOutTime': obj.lastOutTime,
         'curSeason': obj.curSeason,
         'curLevel': obj.curLevel}

    def isSameType(self, obj):
        return type(obj) is ArenaGains


instance = ArenaGainsInfo()
