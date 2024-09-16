#Embedded file name: /WORKSPACE/data/entities/common/battlefieldgains.o
import gamelog
import const
import BigWorld
import gametypes
from userDictType import UserDictType
from userSoleType import UserSoleType
from data import battle_field_data as BFD
if BigWorld.component in ('base', 'cell'):
    from data import log_src_def_data as LSDD

class BattleFieldGainItem(UserSoleType):

    def __init__(self, winMatch = 0, loseMatch = 0, duelMatch = 0, killCount = 0, dieCount = 0):
        self.winMatch = winMatch
        self.loseMatch = loseMatch
        self.duelMatch = duelMatch
        self.killCount = killCount
        self.dieCount = dieCount

    def win(self, killCount, dieCount):
        self.winMatch += 1
        self.killCount += killCount
        self.dieCount += dieCount

    def lose(self, killCount, dieCount):
        self.loseMatch += 1
        self.killCount += killCount
        self.dieCount += dieCount

    def duel(self, killCount, dieCount):
        self.duelMatch += 1
        self.killCount += killCount
        self.dieCount += dieCount


class BattleFieldGains(UserDictType):

    def __init__(self, fame, addedFame, streakKill):
        self.fame = fame
        self.addedFame = addedFame
        self.streakKill = streakKill

    def win(self, fbNo, killCount, dieCount):
        if not self.has_key(fbNo):
            self[fbNo] = BattleFieldGainItem()
        self[fbNo].win(killCount, dieCount)

    def lose(self, fbNo, killCount, dieCount):
        if not self.has_key(fbNo):
            self[fbNo] = BattleFieldGainItem()
        self[fbNo].lose(killCount, dieCount)

    def duel(self, fbNo, killCount, dieCount):
        if not self.has_key(fbNo):
            self[fbNo] = BattleFieldGainItem()
        self[fbNo].duel(killCount, dieCount)

    def calcGotFame(self, fbNo, myGbId, beKilledId, comboKillCnt, fame, owner):
        gamelog.debug('@hjx fame#calcGotFame:', fbNo, myGbId, beKilledId, comboKillCnt, fame)
        if myGbId == beKilledId:
            lastKillRatio = BFD.data.get(fbNo, {}).get('lastKillRatio', 2.0)
            fame = fame * lastKillRatio
        streakKillRatioes = BFD.data.get(fbNo, {}).get('streakKillRatioes', [])
        if comboKillCnt >= 0 and comboKillCnt < len(streakKillRatioes):
            ratio = streakKillRatioes[comboKillCnt]
            fame = fame * ratio
        self.addFame(fame, owner)

    def addFame(self, fame, owner, fameId = const.JUN_ZI_FAME_ID, op = gametypes.ZHAN_XUN_SRC_DEFAULT):
        if op == gametypes.ZHAN_XUN_SRC_BONUS:
            logSrcType = LSDD.data.LOG_SRC_BATTLE_FIELD_ZHAN_XUN_BONUS
        else:
            logSrcType = LSDD.data.LOG_SRC_BATTLE_FIELD
        if owner:
            diffVal = owner.addFame(fameId, fame, srcType=logSrcType, srcId1=op)
            return diffVal

    def addFameForActivityStateBonus(self, fame, owner, fameId, op):
        fameVal = owner.getActivityStateBonus(gametypes.ACTIVITY_STATES_TYPE_BATTLE_FIELD, fame, {'logSrc': LSDD.data.LOG_SRC_BATTLE_FIELD,
         'op': op,
         'fameId': fameId})
        if fameVal > 0:
            return owner.addFame(fameId, fameVal, srcType=LSDD.data.LOG_SRC_ACTIVITY_STATE_BONUS, srcId1=op)
        else:
            return 0

    def _lateReload(self):
        super(BattleFieldGains, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
