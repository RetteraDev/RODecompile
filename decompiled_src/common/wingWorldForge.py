#Embedded file name: I:/bag/tmp/tw2/res/entities\common/wingWorldForge.o
import BigWorld
import const
import random
import utils
from checkResult import CheckResult
from cdata import game_msg_def_data as GMDD
from data import wing_world_config_data as WWCFD
from data import guild_config_data as GCD
from data import item_data as ID

class WingWorldForge(object):

    def __init__(self):
        self.carryRes = {}
        self.genBonus = {}
        self.genItems = []
        self.clientItems = []
        self.level = 0
        self.state = const.WINGWORLD_FORGE_STATE_NONE
        self.genTimesWeekly = 0
        self.lastStartTime = 0
        self.round = 0
        self.maxRound = 0
        self.count = 0
        self.maxCount = 0
        if BigWorld.component == 'base':
            self.forgeStartTimerID = 0
            self.forgeEndTimerID = 0

    def reset(self):
        self.carryRes = {}
        self.genBonus = {}
        self.genItems = []
        self.clientItems = []
        self.level = 0
        self.state = const.WINGWORLD_FORGE_STATE_NONE
        self.genTimesWeekly = 0
        self.lastStartTime = 0
        self.round = 0
        self.maxRound = 0
        self.count = 0
        self.maxCount = 0

    def getStateStr(self):
        return const.WINGWORLD_FORGE_STATE_STR(self.state, '')

    def canAddCarryRes(self):
        if self.state != const.WINGWORLD_FORGE_STATE_NONE:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_STATE_NOT_NONE,))
        if self.carryRes and len(self.carryRes) > 0:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_HAS_CARRY_RES,))
        return CheckResult(True, 0)

    def addCarryRes(self, carryRes, level, isBroken):
        self.carryRes = {}
        if isBroken:
            pct = WWCFD.data.get('YaBiaoFailResPct', 0.5)
            for resId, resVal in (carryRes or {}).iteritems():
                self.carryRes[resId] = int(resVal * pct)

        else:
            self.carryRes = carryRes
        self.level = level

    def canAddExtraRes(self):
        if self.state != const.WINGWORLD_FORGE_STATE_NONE:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_STATE_NOT_NONE,))
        if not self.carryRes or len(self.carryRes) <= 0:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_NO_CARRY_RES,))
        return CheckResult(True, 0)

    def canStartForge(self):
        if self.state != const.WINGWORLD_FORGE_STATE_NONE:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_STATE_NOT_NONE,))
        startTime = WWCFD.data.get('wingWorldForgeStartTime', '0 0 * * *')
        endTime = WWCFD.data.get('wingWorldForgeEndTime', '59 23 * * *')
        startArr = startTime.split(' ')
        endArr = endTime.split(' ')
        inTime = utils.inSimpleTimeRange([startArr[0], startArr[1], startArr[4]], [endArr[0], endArr[1], endArr[4]])
        if not inTime:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_NOT_OPEN_TIME,))
        weeklyTimes = WWCFD.data.get('rongluResLimit', const.WINGWORLD_FORGE_WEEKLY_COUNT)
        if self.genTimesWeekly >= weeklyTimes:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_LACK_TIME,))
        if not self.carryRes or len(self.carryRes) <= 0:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_NO_CARRY_RES,))
        return CheckResult(True, 0)

    def startForge(self):
        self.genTimesWeekly += 1
        self.round = 0
        self.count = 0

    def canEnd(self):
        if self.state == const.WINGWORLD_FORGE_STATE_NONE:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_STATE_NONE,))
        if self.state == const.WINGWORLD_FORGE_STATE_END:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_STATE_END,))
        return True

    def canStartRound(self):
        if self.state != const.WINGWORLD_FORGE_STATE_START:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_STATE_NOT_START,))
        return CheckResult(True, 0)

    def canEndRound(self):
        if self.state != const.WINGWORLD_FORGE_STATE_START:
            return CheckResult(False, (GMDD.data.GUILD_FORGE_STATE_NOT_START,))
        return CheckResult(True, 0)

    def endForge(self):
        if self.state == const.WINGWORLD_FORGE_STATE_NONE or self.state == const.WINGWORLD_FORGE_STATE_END:
            return
        self.state = const.WINGWORLD_FORGE_STATE_END

    def resetWeekly(self):
        self.genTimesWeekly = 0

    def clearRes(self):
        self.carryRes = {}
        self.genBonus = {}
        self.genItems = []
        self.clientItems = []

    def changeState(self, state):
        if self.state == state:
            return False
        self.state = state
        return True

    def randomBonusList(self):
        random.shuffle(self.genItems)

    def randomClientBonusList(self):
        random.shuffle(self.clientItems)

    def getClientItemNames(self):
        if self.round <= 0:
            return []
        names = []
        startIndex = const.WINGWORlD_FORGE_ROUND_NUM * (self.round - 1)
        endIndex = min(const.WINGWORlD_FORGE_ROUND_NUM * self.round, self.maxCount)
        items = self.clientItems[startIndex:endIndex]
        for item in items:
            if item and item[0]:
                itemId, _ = item[0]
                itemData = ID.data.get(itemId)
                if itemData:
                    names.append(itemData.get('name', ''))

        return names
