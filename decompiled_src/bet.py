#Embedded file name: /WORKSPACE/data/entities/common/bet.o
import BigWorld
import utils
from userSoleType import UserSoleType
from userDictType import UserDictType
if BigWorld.component == 'client':
    from data import formula_client_data as FSD
elif BigWorld.component in ('base', 'cell'):
    import gameengine
    from data import formula_server_data as FSD
from data import sys_config_data as SCD
from data import region_server_config_data as RSCD
BET_REFRESH_MAGIC_NUM = 65
BET_SPLIT = '@_@'
BET_STATE_NONE = 0
BET_STATE_BETED = 1
BET_STATE_FAILED = 2
BET_STATE_SUCC = 3
MANUAL_BET_ID_MIN = 1
MANUAL_BET_ID_MAX = 10000
AUTOMATIC_BET_ID_MIN = 10001
AUTOMATIC_BET_ID_MAX = 999999
GM_QUERY_MANUAL = 1
GM_QUERY_AUTOMATIC = 2
GM_QUERY_ALL = 3
BET_STATE_WRONG = -1
BET_STATE_INIT = 0
BET_STATE_START = 1
BET_STATE_DDL = 2
BET_STATE_CALC = 3
BET_STATE = {BET_STATE_START: 'tStart',
 BET_STATE_DDL: 'tDDL',
 BET_STATE_CALC: 'tCalc'}
DEFAULT_ANS = 99
DO_BET_UPDATE_INTERVAL = 3
BET_EXTRA_SEASON = 1
BET_TOP_RANK_LENGTH = 200
NOTIFY_TYPE_BET_START = 1
NOTIFY_TYPE_BET_CALC = 2
NOTIFY_TYPE_BET_CLOSE = 3
BET_ST_EXAMPLE = 10000

def getCrossBetHostId(hostId = 0):
    hostId = hostId or utils.getHostId()
    return RSCD.data.get(hostId, {}).get('betRegionHostId', 0)


def getCrossBetStub(hostId = 0):
    return gameengine.getGlobalStubByName('CrossBetStub', utils.getServerName(getCrossBetHostId(hostId)))


class BetVal(UserSoleType):

    def __init__(self, bId = 0, reward = None, tStart = 0, tDDL = 0, tCalc = 0, ans = DEFAULT_ANS, state = 0, desc = '', option = None, calcFlag = False, extra = None):
        self.bId = bId
        self.reward = reward if reward else []
        self.tStart = tStart
        self.tDDL = tDDL
        self.tCalc = tCalc
        self.ans = ans
        self.state = state
        self.desc = desc
        self.option = option if option else []
        self.calcFlag = calcFlag
        self.extra = extra

    def getBetPoolByGbId(self, gbId):
        for choice, rVal in enumerate(self.reward):
            if gbId not in rVal:
                continue
            return BetClientVal(self.bId, choice, rVal[gbId])

    def addGbIdToBetPool(self, gbId, choice, fame):
        if len(self.reward) <= choice:
            return
        self.reward[choice][gbId] = fame

    def genReturnBet(self):
        res = []
        for rVal in self.reward:
            for gbId, reward in rVal.iteritems():
                res.append((gbId, reward))

        return res

    def getBetPoolOverall(self):
        rRight = 0
        rTotal = 0
        for choice, rVal in enumerate(self.reward):
            rSum = sum(rVal.values())
            if choice == self.ans:
                rRight = rSum
            rTotal += rSum

        return (rRight, rTotal - rRight)

    def getBetPoolChoiceDetail(self):
        res = []
        for rVal in self.reward:
            cnt = sum(rVal.values())
            res.append(cnt)

        return res

    def setBetPoolChoiceDetail(self, hostId, betRes):
        for choice, val in enumerate(betRes):
            self.reward[choice][hostId] = val

    def calcBetBonus(self, rRight, rWrong):
        res = []
        fId = SCD.data.get('betCalcBonusFormulaId', 0)
        f = FSD.data.get(fId, {}).get('formula', None)
        if not f:
            return res
        if self.ans == DEFAULT_ANS:
            return res
        for gbId, reward in self.reward[self.ans].iteritems():
            bonus = int(f({'rRight': float(rRight),
             'rWrong': float(rWrong),
             'rSelf': float(reward)}))
            res.append((gbId, bonus))

        return res

    def addOption(self, op):
        self.option.append(op)
        self.reward.append({})

    def setAns(self, ans, tCalc):
        self.ans = ans
        self.tCalc = tCalc

    def setStamp(self, tStart, tDDL):
        self.tStart = tStart
        self.tDDL = tDDL

    def nextState(self):
        return self.state + 1

    def gotoNextState(self):
        nState = self.nextState()
        now = utils.getNow()
        if nState in BET_STATE:
            bStamp = getattr(self, BET_STATE[nState], 0)
            if bStamp and now >= bStamp:
                self.state = self.nextState()
                return True
        return False

    def getDTO(self):
        rewardRes = []
        for reward in self.reward:
            rewardRes.append(sum(reward.values()))

        return (self.bId,
         rewardRes,
         self.tStart,
         self.tDDL,
         self.tCalc,
         self.ans,
         self.state,
         self.desc,
         self.option,
         self.calcFlag,
         self.extra)

    def fromDTO(self, dto):
        self.bId, self.reward, self.tStart, self.tDDL, self.tCalc, self.ans, self.state, self.desc, self.option, self.calcFlag, self.extra = dto
        return self

    def getDTOInServer(self, includeExtra = False):
        reward = self.reward if includeExtra else None
        option = self.option if includeExtra else None
        return (self.bId,
         self.tStart,
         self.tDDL,
         self.tCalc,
         self.ans,
         self.state,
         self.calcFlag,
         self.desc,
         reward,
         option,
         self.extra)

    def fromDTOInServer(self, dto):
        self.bId, self.tStart, self.tDDL, self.tCalc, self.ans, self.state, self.calcFlag, self.desc, reward, option, self.extra = dto
        if reward and option:
            self.reward = reward
            self.option = option
        return self

    def getBetClientAnswer(self):
        if BigWorld.component == 'client':
            now = utils.getNow()
            if now >= self.tDDL:
                return self.ans
            return DEFAULT_ANS
        return self.ans

    def isInShowTime(self):
        if BigWorld.component == 'client':
            now = utils.getNow()
            if self.tStart and self.tStart <= now:
                return True
            return False
        return True


class BetDict(UserDictType):

    def _lateReload(self):
        super(BetDict, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()


class BetClientVal(UserSoleType):

    def __init__(self, bId = 0, choice = 0, fame = 0):
        self.bId = bId
        self.choice = choice
        self.fame = fame

    def getDTO(self):
        return (self.bId, self.choice, self.fame)

    def fromDTO(self, dto):
        self.bId, self.choice, self.fame = dto
        return self
