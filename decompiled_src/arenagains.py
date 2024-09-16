#Embedded file name: /WORKSPACE/data/entities/common/arenagains.o
from userDictType import UserDictType
from userSoleType import UserSoleType
import BigWorld
import formula
import const
import utils
import gametypes
import gamelog
if BigWorld.component in ('base', 'cell'):
    import gameengine
    import serverlog
import utils
from data import arena_data as AD
from data import arena_mode_data as AMD
from data import duel_config_data as DCD
from cdata import arena_rank_add_score_data as ARASC

class ArenaGainItem(UserSoleType):

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

    def getTotal(self):
        return self.winMatch + self.loseMatch + self.duelMatch

    def reset(self):
        self.winMatch = 0
        self.loseMatch = 0
        self.duelMatch = 0
        self.killCount = 0
        self.dieCount = 0


class ArenaGains(UserDictType):
    K1 = DCD.data.get('KValue', 400.0)

    def __init__(self, arenaScore, arenaLevel, streak, weekPlayCnt = 0, weekExchangeFameFlag = False, lastOutTime = 0, curSeason = 0, curLevel = 0):
        self.arenaScore = arenaScore
        self.arenaLevel = arenaLevel
        self.streak = streak
        self.weekPlayCnt = weekPlayCnt
        self.weekExchangeFameFlag = weekExchangeFameFlag
        self.lastOutTime = lastOutTime
        self.curSeason = curSeason
        self.curLevel = curLevel

    def isValidTime(self, fbNo):
        if not AD.data.has_key(fbNo):
            utils.reportWarning('ArenaGains fbNo is error:%d' % (fbNo,))
            return False
        arenaData = AD.data[fbNo]
        startTime = arenaData.get('arenaScoreStartTimes', (utils.CRON_ANY,))
        endTime = arenaData.get('arenaScoreEndTimes', (utils.CRON_ANY,))
        if len(startTime) != len(endTime):
            utils.reportWarning('ArenaGains length of startTime not match with endTime:%d,%d' % (len(startTime), len(endTime)))
            return False
        elif True in [ utils.inCrontabRange(startTime[i], endTime[i]) for i in xrange(len(startTime)) ]:
            return True
        else:
            return False

    def win(self, owner, fbNo, otherAverageScores, killCount, dieCount):
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        if not self.has_key(arenaMode):
            self[arenaMode] = ArenaGainItem()
        self[arenaMode].win(killCount, dieCount)
        self.streak += 1
        score = self.calcAddArenaScore(fbNo, const.WIN, otherAverageScores)
        return self.addScore(owner, arenaMode, int(score))

    def lose(self, owner, fbNo, otherAverageScores, killCount, dieCount):
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        if not self.has_key(arenaMode):
            self[arenaMode] = ArenaGainItem()
        self[arenaMode].lose(killCount, dieCount)
        self.streak -= 1
        score = self.calcAddArenaScore(fbNo, const.LOSE, otherAverageScores)
        return self.addScore(owner, arenaMode, int(score))

    def duel(self, owner, fbNo, otherAverageScores, killCount, dieCount):
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        if not self.has_key(arenaMode):
            self[arenaMode] = ArenaGainItem()
        score = self.calcAddArenaScore(fbNo, const.TIE, otherAverageScores)
        self.streak = 0
        self[arenaMode].duel(killCount, dieCount)
        return self.addScore(owner, arenaMode, score)

    def winByQuitEarly(self, owner, fbNo, killCount, dieCount):
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        if not self.has_key(arenaMode):
            self[arenaMode] = ArenaGainItem()
        self[arenaMode].win(killCount, dieCount)
        self.streak += 1
        return 0

    def loseByQuitEarly(self, owner, fbNo, otherAverageScores, killCount, dieCount):
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        if not self.has_key(arenaMode):
            self[arenaMode] = ArenaGainItem()
        self[arenaMode].lose(killCount, dieCount)
        self.streak -= 1
        score = self.calcAddArenaScore(fbNo, const.LOSE_QUIT_EARLY, otherAverageScores)
        return self.addScore(owner, arenaMode, int(score))

    def addScore(self, owner, arenaMode, score):
        index = formula.getArenaLvTag(arenaMode, owner.lv)
        if index == -1:
            utils.reportWarning('addScore warning index is -1, arenaMode:%d, lv:%d' % (arenaMode, owner.lv))
            return None
        else:
            maxArenaScores = AMD.data.get(arenaMode, {}).get('maxArenaScores', ())
            if len(maxArenaScores) == 0:
                self.arenaScore += score
                return score
            if index >= len(maxArenaScores):
                utils.reportWarning('addScore warning index over flow, arenaMode:%d, lv:%d, index:%d' % (arenaMode, owner.lv, index))
                return None
            maxArenaScore = maxArenaScores[index]
            oldArenaScore = self.arenaScore
            if self.arenaScore + score > maxArenaScore:
                self.arenaScore = maxArenaScore
            else:
                self.arenaScore += score
            return self.arenaScore - oldArenaScore

    def calcExpectedValue(self, x):
        if utils.getCommonGameConfig('enableFormulaValue'):
            return formula.calcFormulaById(DCD.data.get('KValueFormulaId', 90242), {'x': x})
        else:
            return 1 / (1.0 + 10 ** (-x / self.K1))

    def calcAddArenaScore(self, fbNo, fWin, otherAverageScores):
        enableAddScore = AD.data.get(fbNo, {}).get('enableAddScore', 0)
        if not enableAddScore:
            return 0
        score = 0
        if utils.getCommonGameConfig('enableFormulaValue'):
            for index, data in ARASC.data.iteritems():
                if self.arenaScore >= data.get('minScore', 0) and self.arenaScore <= data.get('maxScore', 0):
                    formulaName = self.getFormulaName(fWin)
                    fId = formulaName and data.get(formulaName) or 0
                    if fId:
                        score = formula.calcFormulaById(fId, {'val': self.calcExpectedValue(self.arenaScore - otherAverageScores)})
                    else:
                        utils.reportWarning('@xjw calcAddArenaScore, %d, %d, %d, %d, %s' % (fbNo,
                         fWin,
                         int(otherAverageScores),
                         index,
                         formulaName))
                    break

        elif fWin == const.WIN:
            if self.arenaScore < 1000:
                score = round((1 - self.calcExpectedValue(self.arenaScore - otherAverageScores)) * 50 + 10)
            elif 1000 <= self.arenaScore < 1200:
                score = round((1 - self.calcExpectedValue(self.arenaScore - otherAverageScores)) * 60 + 0)
            elif 1200 <= self.arenaScore < 2000:
                score = round((1 - self.calcExpectedValue(self.arenaScore - otherAverageScores)) * 32)
            else:
                score = round((1 - self.calcExpectedValue(self.arenaScore - otherAverageScores)) * 16)
        elif fWin == const.TIE:
            if self.arenaScore < 1000:
                score = 10
        elif fWin == const.LOSE:
            if self.arenaScore < 1000:
                score = 10
            elif 1000 <= self.arenaScore < 1200:
                score = 0
            elif 1200 <= self.arenaScore < 2000:
                score = round(-self.calcExpectedValue(self.arenaScore - otherAverageScores) * 32)
            else:
                score = round(-self.calcExpectedValue(self.arenaScore - otherAverageScores) * 16)
        elif fWin == const.WIN_QUIT_EARLY:
            score = 0
        elif fWin == const.LOSE_QUIT_EARLY:
            if self.arenaScore < 1200:
                score = 0
            elif 1200 <= self.arenaScore < 2000:
                score = round(-self.calcExpectedValue(self.arenaScore - otherAverageScores) * 32)
            else:
                score = round(-self.calcExpectedValue(self.arenaScore - otherAverageScores) * 16)
        return score

    def getFormulaName(self, fWin):
        if fWin == const.WIN:
            return 'winFormula1'
        if fWin == const.TIE:
            return 'tieFormula'
        if fWin == const.LOSE:
            return 'loseFormula1'
        if fWin == const.WIN_QUIT_EARLY:
            return 'winFormula2'
        if fWin == const.LOSE_QUIT_EARLY:
            return 'loseFormula2'
        return ''

    def subScore(self, owner, score, op = gametypes.ARENA_SUB_SCORE_OP_DEFAULT, arenaModeType = const.ARENA_MODE_TYPE_NORMAL):
        if BigWorld.component != 'cell':
            return
        gamelog.info('@hjx arena#subScore:', owner, self.arenaScore, score, op)
        oldArenaScore = self.arenaScore
        self.arenaScore = max(800, self.arenaScore - score)
        if op in gametypes.ARENA_SUB_SCORE_NEED_RESET:
            if arenaModeType == const.ARENA_MODE_TYPE_BALANCE:
                owner.onArenaDuanWeiAutoAwardEx(op)
                owner.arenaAwardFlagEx.clear()
                owner.arenaAwardFlagEx = owner.arenaAwardFlagEx
                owner.updateArenaAwardFlag(arenaModeType)
            else:
                owner.onArenaDuanWeiAutoAward(op)
                owner.arenaAwardFlag.clear()
                owner.arenaAwardFlag = owner.arenaAwardFlag
                owner.updateArenaAwardFlag()
        if BigWorld.component in ('base', 'cell'):
            serverlog.genArenaScoreLog(owner, op, self.arenaScore, self.arenaScore - oldArenaScore, 0, arenaModeType)

    def calcWinRatio(self):
        winCnt = 0
        totalCnt = 0
        for val in self.itervalues():
            winCnt += val.winMatch
            totalCnt += val.getTotal()

        if totalCnt > 0:
            return 1.0 * winCnt / totalCnt
        else:
            return 0

    def getWinCnt(self):
        winCnt = 0
        for val in self.itervalues():
            winCnt += val.winMatch

        return winCnt

    def reset(self):
        for val in self.itervalues():
            val.reset()

    def _lateReload(self):
        super(ArenaGains, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
