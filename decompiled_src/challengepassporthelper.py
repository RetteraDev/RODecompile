#Embedded file name: /WORKSPACE/data/entities/client/helpers/challengepassporthelper.o
import BigWorld
import gameglobal
import gametypes
import challengePassportUtils
from guis import uiUtils
from guis import events
from helpers.eventDispatcher import Event
from cdata import challenge_passport_cnt_reverse_data as CPCRD
from data import challenge_passport_lv_data as CPLD
from data import challenge_passport_lv_new_server_data as CPLNSD
from data import challenge_passport_target_data as CPTD

def getTargetList(targetType, season):
    allTargetList = CPCRD.data.get((targetType, season), [])
    targetList = []
    handledGroupId = []
    p = BigWorld.player()
    for targetId in allTargetList:
        if CPTD.data.get(targetId, {}).get('hide'):
            continue
        groupId = CPTD.data.get(targetId, {}).get('groupId', 0)
        if groupId:
            if groupId in handledGroupId:
                continue
            handledGroupId.append(groupId)
            selectTargetId = p.challengePassportData.optionalTarget.get(groupId, {}).get('id', 0)
            if selectTargetId:
                targetList.append(selectTargetId)
        else:
            targetList.append(targetId)

    targetList.sort()
    return targetList


def getTargetsInfoByType(targetType):
    season = uiUtils.getCurrentChallengePassportSeason()
    targetList = getTargetList(targetType, season)
    p = BigWorld.player()
    numDoneTarget = 0
    numAllTarget = len(targetList)
    allExp = 0
    allDoneExp = 0
    for targetId in targetList:
        config = CPTD.data.get(targetId, {})
        perTimeExp = config.get('exp', 0)
        totalFinishCnt = config.get('finishCnt', 0)
        finishCnt = p.challengePassportData.getTargetFinishTimes(targetId)
        isDone = isTargetDone(targetId)
        if totalFinishCnt > 1:
            doneExp = perTimeExp * totalFinishCnt if isDone else perTimeExp * finishCnt
            totalExp = perTimeExp * totalFinishCnt
        else:
            doneExp = perTimeExp if isDone else 0
            totalExp = perTimeExp
        allExp += totalExp
        allDoneExp += doneExp
        if isDone:
            numDoneTarget += 1

    return (allDoneExp,
     allExp,
     numAllTarget,
     numDoneTarget,
     targetList)


def isTargetDone(targetId):
    p = BigWorld.player()
    config = CPTD.data.get(targetId, {})
    totalFinishCnt = config.get('finishCnt', 0)
    if 'finishCnt' in config:
        isDone = p.challengePassportData.dayTarget.get(targetId, 0) >= totalFinishCnt
        isDone |= p.challengePassportData.weekTarget.get(targetId, 0) >= totalFinishCnt
        isDone |= p.challengePassportData.seasonTarget.get(targetId, 0) >= totalFinishCnt
    else:
        isDone = p.challengePassportData.dayTarget.get(targetId, 0) > 0
        isDone |= p.challengePassportData.weekTarget.get(targetId, 0) > 0
        isDone |= p.challengePassportData.seasonTarget.get(targetId, 0) > 0
    return isDone


def getTargetCurrentProgress(targetId):
    p = BigWorld.player()
    prop = CPTD.data.get(targetId, {}).get('property', '')
    return p.statsInfo.get(prop, 0)


def isNewChallengePassportServer():
    season = uiUtils.getCurrentChallengePassportSeason()
    return season == -1


def getChallengePassportLvData():
    if isNewChallengePassportServer():
        tmpData = CPLNSD.data
    else:
        tmpData = CPLD.data
    from data import challenge_passport_config_data as CPCD
    season = uiUtils.getCurrentChallengePassportSeason()
    maxLv = challengePassportUtils.challengePassportMaxLv(season)
    data = {}
    for i in xrange(1, maxLv + 1):
        data[i] = tmpData.get((season, i), {})

    return data


class ChallengePassportDataHelper(object):
    lv = property(lambda self: self._lv)
    exp = property(lambda self: self._exp)
    isCharge = property(lambda self: self._isCharge)
    bonusPool = property(lambda self: self._bonusPool)
    dayTarget = property(lambda self: self._dayTarget)
    weekTarget = property(lambda self: self._weekTarget)
    seasonTarget = property(lambda self: self._seasonTarget)
    season = property(lambda self: self._season)
    optionalTarget = property(lambda self: self._optionalTarget)

    def __init__(self):
        super(ChallengePassportDataHelper, self).__init__()
        self._lv = 0
        self._exp = 0
        self._isCharge = False
        self._bonusPool = set()
        self._dayTarget = {}
        self._weekTarget = {}
        self._seasonTarget = {}
        self._version = 10000
        self._firstNotify = False
        self._onSceneLoaded = False
        self._season = -1
        self._optionalTarget = {}

    def updateInfo(self, info):
        print 'ypc@ challenge updateinfo', info
        self._version = info.get('version', 0)
        dirty = False
        if 'lv' in info and self._lv != info.get('lv', 0):
            self._lv = info.get('lv', 0)
            dirty = True
        if 'exp' in info and self._exp != info.get('exp', 0):
            self._exp = info.get('exp', 0)
            dirty = True
        if 'isCharge' in info and self._isCharge != info.get('isCharge', 0):
            self._isCharge = info.get('isCharge', 0)
            dirty = True
        if 'bonusPool' in info and self._bonusPool != info.get('bonusPool', set()):
            self._bonusPool = info.get('bonusPool', set())
            dirty = True
        if 'dayTarget' in info:
            self._dayTarget = info.get('dayTarget', 0)
            dirty = True
        if 'weekTarget' in info:
            self._weekTarget = info.get('weekTarget', 0)
            dirty = True
        if 'seasonTarget' in info:
            self._seasonTarget = info.get('seasonTarget', 0)
            dirty = True
        if 'season' in info:
            self._season = info.get('season', -1)
            dirty = True
        if 'optionalTarget' in info:
            self._optionalTarget = info.get('optionalTarget', {})
            dirty = True
        if dirty:
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
            evt = Event(events.EVNET_CHALLENGE_PASSPORT_DATA_CHANGE)
            gameglobal.rds.ui.dispatchEvent(evt)

    def challengePassportNotify(self):
        self._firstNotify = True
        if self._onSceneLoaded:
            self._firstNotify = False
            gameglobal.rds.ui.challengePassportAppoint.show()

    def onSceneLoaded(self):
        self._onSceneLoaded = True
        if self._firstNotify:
            self._firstNotify = False
            gameglobal.rds.ui.challengePassportAppoint.show()

    def requestInfo(self):
        print 'ypc@ requestInfo'
        p = BigWorld.player()
        p.base.challengePassportSyncInfo(self._version)

    def requestReceiveBonus(self, lv):
        print 'ypc@ requestReceiveBonus', lv
        p = BigWorld.player()
        p.base.challengePassportReceiveBonus(lv)

    def requestBuyLevel(self):
        print 'ypc@ requestBuyLevel'
        p = BigWorld.player()
        p.base.challengePassportBuyLv()

    def hasRewardNotTaken(self):
        CPLvData = getChallengePassportLvData()
        allBonus = set(range(1, self._lv + 1))
        allNotTaken = self._bonusPool
        notTaken = allBonus - allNotTaken
        for i in notTaken:
            if self._isCharge:
                return True
            freeBonus = CPLvData.get(i, {}).get('freeBonus', -1)
            if freeBonus != -1:
                return True
        else:
            return False

    def getMinNotTakenLevel(self):
        CPLvData = getChallengePassportLvData()
        for i in xrange(1, self._lv + 1):
            if i not in self._bonusPool:
                if self._isCharge:
                    return i
                freeBonus = CPLvData.get(i, {}).get('freeBonus', -1)
                if freeBonus != -1:
                    return i
        else:
            return min(self._lv + 1, len(CPLvData))

    def getTargetFinishTimes(self, targetId):
        targetType = CPTD.data.get(targetId, {}).get('type', 0)
        if targetType == gametypes.CHALLENGE_PASSPORT_TYPE_DAY:
            return self._dayTarget.get(targetId, 0)
        if targetType in gametypes.CHALLENGE_PASSPORT_TYPE_WEEK:
            return self._weekTarget.get(targetId, 0)
        if targetType == gametypes.CHALLENGE_PASSPORT_TYPE_SEASON:
            return self._seasonTarget.get(targetId, 0)
        return 0
