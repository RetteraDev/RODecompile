#Embedded file name: /WORKSPACE/data/entities/common/teamendless.o
import gamelog
import random
import const
import BigWorld
import gametypes
import utils
import copy
from userSoleType import UserSoleType
from userDictType import UserDictType
from data import team_endless_config_data as TECD

class TeamEndlessProgressVal(UserSoleType):

    def __init__(self, lv = 1, onceRewardState = 0, levelRewardState = 0):
        super(TeamEndlessProgressVal, self).__init__()
        self.lv = lv
        self.onceRewardState = onceRewardState
        self.levelRewardState = levelRewardState


class TeamEndlessProgress(UserDictType):

    def _lateReload(self):
        super(TeamEndlessProgress, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def setItem(self, lv, item):
        self[lv] = item

    def pushVal(self, lv, onceRewardState, levelRewardState):
        self[lv] = TeamEndlessProgressVal(lv=lv, onceRewardState=onceRewardState, levelRewardState=levelRewardState)

    def completeNewLv(self, maxLv):
        for lv, mVal in self.iteritems():
            if lv > maxLv or mVal.onceRewardState != gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT:
                continue
            mVal.onceRewardState = gametypes.TEAM_ENDLESS_REWARD_STATE_ENABLE

    def takeOnceReward(self, lv):
        if not self.has_key(lv):
            return
        self[lv].onceRewardState = gametypes.TEAM_ENDLESS_REWARD_STATE_TAKEN

    def canTakeOnceReward(self, lv):
        if not self.has_key(lv):
            return False
        return self[lv].onceRewardState == gametypes.TEAM_ENDLESS_REWARD_STATE_ENABLE

    def takeLevelReward(self, lv):
        if not self.has_key(lv):
            return
        self[lv].levelRewardState = gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT

    def canTakeLevelReward(self, lv):
        if not self.has_key(lv):
            return False
        return self[lv].levelRewardState == gametypes.TEAM_ENDLESS_REWARD_STATE_ENABLE

    def enableLevelReward(self, lv):
        if not self.has_key(lv):
            return
        self[lv].levelRewardState = gametypes.TEAM_ENDLESS_REWARD_STATE_ENABLE


class TeamEndlessVal(UserSoleType):

    def __init__(self, lvType = 1, maxLv = 0, maxEnableLv = 1, progress = None, bestRecordWeekly = None):
        super(TeamEndlessVal, self).__init__()
        self.lvType = lvType
        self.maxLv = maxLv
        self.maxEnableLv = maxEnableLv
        self.progress = TeamEndlessProgress() if progress is None else progress
        self.bestRecordWeekly = {} if bestRecordWeekly is None else bestRecordWeekly


class TeamEndless(UserDictType):

    def __init__(self, tLastReset = 0):
        super(TeamEndless, self).__init__()
        self.tLastReset = tLastReset

    def _lateReload(self):
        super(TeamEndless, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def setItem(self, lvType, item):
        self[lvType] = item

    def unlockLevel(self, lvType, lv):
        if not self.has_key(lvType):
            self[lvType] = TeamEndlessVal(lvType=lvType, maxLv=lv, maxEnableLv=lv + 1)
            for i in xrange(1, lv + 1):
                self[lvType].progress.pushVal(i, gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT, gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT)

            return
        for i in xrange(1, lv + 1):
            if self[lvType].progress.has_key(i):
                continue
            self[lvType].progress.pushVal(lv, gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT, gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT)

    def maxLv(self, lvType):
        if not self.has_key(lvType):
            return 0
        return self[lvType].maxLv

    def maxEnableLv(self, lvType):
        if not self.has_key(lvType):
            return 1
        return self[lvType].maxEnableLv

    def setMaxLv(self, lvType, maxLv):
        """\xcd\xa8\xb9\xd8\xc1\xcb\xd0\xc2\xb5\xc4\xc4\xd1\xb6\xc8"""
        if maxLv <= self.maxLv(lvType):
            return
        for i in xrange(self.maxLv(lvType) + 1, maxLv + 1):
            self[lvType].progress.pushVal(i, gametypes.TEAM_ENDLESS_REWARD_STATE_ENABLE, gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT)

        self[lvType].maxLv = maxLv

    def setMaxEnableLv(self, lvType, maxEnableLv):
        if not self.has_key(lvType):
            return
        self[lvType].maxEnableLv = maxEnableLv

    def randomReduceMaxEnableLv(self):
        lv1, lv2 = TECD.data.get('reduceLevelWeekly', (0, 0))
        x = random.randint(lv1, lv2)
        for val in self.itervalues():
            val.maxEnableLv = max(1, val.maxEnableLv - x)

    def canTakeOnceReward(self, lvType, lv):
        if not self.has_key(lvType):
            return False
        return self[lvType].progress.canTakeOnceReward(lv)

    def takeOnceReward(self, lvType, lv):
        if not self.has_key(lvType):
            return
        self[lvType].progress.takeOnceReward(lv)

    def canTakeLevelReward(self, lvType, lv):
        if not self.has_key(lvType):
            return False
        return self[lvType].progress.canTakeLevelReward(lv)

    def takeLevelReward(self, lvType, lv):
        if not self.has_key(lvType):
            return
        self[lvType].progress.takeLevelReward(lv)

    def enableLevelReward(self, lvType, lv):
        if not self.has_key(lvType):
            return
        self[lvType].progress.enableLevelReward(lv)

    def updateBestRecordWeekly(self, lvType, lv):
        if not self.has_key(lvType):
            return
        now = utils.getNow()
        if not self[lvType].bestRecordWeekly:
            self[lvType].bestRecordWeekly = (lv, now)
            return
        oldLv, t = self[lvType].bestRecordWeekly
        if lv > oldLv:
            self[lvType].bestRecordWeekly = (lv, now)

    def getSyncData(self, lvType, minLv = 0, maxLv = 0):
        if not self.has_key(lvType):
            return {}
        val = self[lvType]
        data = {lvType: {'maxLv': val.maxLv,
                  'maxEnableLv': val.maxEnableLv,
                  'bestRecordWeekly': copy.deepcopy(val.bestRecordWeekly)}}
        if minLv == 0 or maxLv == 0 or minLv > maxLv:
            return data
        progress = {}
        for pVal in self[lvType].progress.itervalues():
            if pVal.lv < minLv or pVal.lv > maxLv:
                continue
            progress[pVal.lv] = {'onceRewardState': pVal.onceRewardState,
             'levelRewardState': pVal.levelRewardState}

        data[lvType]['progress'] = progress
        return data

    def updateBySyncData(self, data):
        gamelog.debug('@zhangkuo updateBySyncData', data)
        for lvType, tVal in data.iteritems():
            progress = TeamEndlessProgress()
            for lv, pVal in tVal.get('progress', {}).iteritems():
                progress.pushVal(lv, pVal.get('onceRewardState', 0), pVal.get('levelRewardState', 0))

            if not self.has_key(lvType):
                self[lvType] = TeamEndlessVal(lvType=lvType, maxLv=tVal.get('maxLv', 0), maxEnableLv=tVal.get('maxEnableLv', 1), bestRecordWeekly=tVal.get('bestRecordWeekly', None), progress=progress)
            else:
                if tVal.get('maxLv'):
                    self[lvType].maxLv = tVal.get('maxLv')
                if tVal.get('maxEnableLv'):
                    self[lvType].maxEnableLv = tVal.get('maxEnableLv')
                if tVal.get('bestRecordWeekly'):
                    self[lvType].bestRecordWeekly = tVal.get('bestRecordWeekly')
                for lv, pVal in progress.iteritems():
                    self[lvType].progress[lv] = pVal

    def endTeamEndless(self, lvType, lv):
        """\xcc\xf4\xd5\xbd\xc1\xcb\xd0\xc2\xb5\xc4\xcc\xf5\xc4\xbf\xa3\xac\xb3\xf5\xca\xbc\xbb\xaf\xb2\xe3\xbc\xb6\xd0\xc5\xcf\xa2"""
        if not self.has_key(lvType):
            self[lvType] = TeamEndlessVal(lvType=lvType)
        for i in xrange(1, lv + 1):
            if self[lvType].progress.has_key(i):
                continue
            self[lvType].progress.pushVal(i, gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT, gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT)
