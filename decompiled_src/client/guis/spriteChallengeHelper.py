#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spriteChallengeHelper.o
from gamestrings import gameStrings
import BigWorld
import sys
import gametypes
import gameglobal
import utils
from gameclass import Singleton
from guis.asObject import TipManager
from guis import tipUtils
from guis import uiConst
from data import sprite_challenge_data as SCD
from data import bonus_history_check_data as BHCD
from data import sprite_challenge_config_data as SCCD
from cdata import sprite_challenge_season_list_data as SCSLD
import const

def getInstance():
    return SpriteChallengeHelper.getInstance()


class SpriteChallengeHelper(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(SpriteChallengeHelper, self).__init__()

    def getOnceRewardState(self, lvKey, diffIdx):
        if self.isRewardGeted(lvKey, diffIdx):
            return gametypes.SPRITE_CHALLENGE_STATE_TAKEN
        if self.getCurrentProgress(lvKey) >= diffIdx:
            return gametypes.SPRITE_CHALLENGE_STATE_ENABLE
        return gametypes.SPRITE_CHALLENGE_STATE_DEFAULT

    def getMaxProgress(self, lvKey):
        spriteChallengeRankInfo = SCCD.data.get('spriteChallengeRankInfo', {})
        lvKeyStr = self.getLvKeyStrByLvType(lvKey)
        return spriteChallengeRankInfo.get(lvKeyStr, {}).get('maxLv', 10)

    def getMaxShowProgress(self, lvKey):
        p = BigWorld.player()
        maxProgress = self.getMaxProgress(lvKey)
        spriteChallengeInfo = getattr(p, 'spriteChallengeInfo', {})
        currentProgress = self.getCurrentProgress(lvKey)
        lvKeyStr = self.getLvKeyStrByLvType(lvKey)
        avaliableProgress = self.getAvailableLv(lvKey)
        serverMaxProgress = spriteChallengeInfo.get(lvKeyStr, {}).get('maxProgress', 0)
        if currentProgress >= serverMaxProgress:
            serverMaxProgress = max(serverMaxProgress + 5, currentProgress + 1)
        serverMaxProgress = max(serverMaxProgress, avaliableProgress)
        return max(const.SPRITE_CHALLENGE_MAX_MIN_SHOW_NUM, min(serverMaxProgress, maxProgress))

    def getAvailableLv(self, lvKey):
        p = BigWorld.player()
        spriteChallengeInfo = getattr(p, 'spriteChallengeInfo', {})
        lvKeyStr = self.getLvKeyStrByLvType(lvKey)
        availableProgress = spriteChallengeInfo.get(lvKeyStr, {}).get('availableProgress', 0)
        return min(max(self.getCurrentProgress(lvKey) + 1, availableProgress), self.getMaxProgress(lvKey))

    def getCurrentProgress(self, lvKey):
        p = BigWorld.player()
        spriteChallengeInfo = getattr(p, 'spriteChallengeInfo', {})
        lvKeyStr = self.getLvKeyStrByLvType(lvKey)
        progressKeys = spriteChallengeInfo.get(lvKeyStr, {}).get('finishProgress', {})
        maxProgress = 0
        for progKey in progressKeys:
            progress = int(progKey)
            if progress > maxProgress:
                maxProgress = progress

        return maxProgress

    def getCurrentSeason(self, lvKey):
        p = BigWorld.player()
        spriteChallengeInfo = getattr(p, 'spriteChallengeInfo', {})
        lvKeyStr = self.getLvKeyStrByLvType(lvKey)
        if spriteChallengeInfo.has_key(lvKeyStr):
            return spriteChallengeInfo.get(lvKeyStr, {}).get('season', 1)
        if spriteChallengeInfo.values():
            return spriteChallengeInfo.values()[0].get('season', 1)
        return 0

    def getCurrentSeasonLocal(self, useLastSeason = True):
        for season in SCSLD.data:
            beginTime = utils.parseCrontabPatternWithYear(SCSLD.data.get(season, {}).get('beginTime', ''))
            endTime = utils.parseCrontabPatternWithYear(SCSLD.data.get(season, {}).get('endTime', ''))
            if not utils.inTimeTupleRangeWithYear(beginTime, endTime, utils.getNow()):
                continue
            else:
                return season

        if useLastSeason:
            lastSeason = 0
            for season in SCSLD.data:
                beginTime = utils.parseCrontabPatternWithYear(SCSLD.data.get(season, {}).get('beginTime', ''))
                now = utils.getNow()
                nextStartTime = utils.nextByTimeTupleWithYear(beginTime, now) + now
                if nextStartTime != sys.maxint:
                    return lastSeason
                lastSeason = season

        return -1

    def inSpriteChallengeSeason(self):
        for season in SCSLD.data:
            beginTime = utils.parseCrontabPatternWithYear(SCSLD.data.get(season, {}).get('beginTime', ''))
            endTime = utils.parseCrontabPatternWithYear(SCSLD.data.get(season, {}).get('endTime', ''))
            if not utils.inTimeTupleRangeWithYear(beginTime, endTime, utils.getNow()):
                continue
            else:
                return True

        return False

    def queryBonusInfo(self):
        p = BigWorld.player()
        p.cell.queryBonusHistory(self.getBonusGroup())

    def getBonusGroup(self):
        spriteChallengeRankInfo = SCCD.data.get('spriteChallengeRankInfo', {})
        lvKeyStr = self.getSelfLvKeyStr()
        bonusCheckId = spriteChallengeRankInfo.get(lvKeyStr, {}).get('bonusCheckId', 0)
        return BHCD.data.get(bonusCheckId, {}).get('group', 0)

    def getRemainRewardTime(self):
        p = BigWorld.player()
        spriteChallengeRankInfo = SCCD.data.get('spriteChallengeRankInfo', {})
        lvKeyStr = self.getSelfLvKeyStr()
        bonusCheckId = spriteChallengeRankInfo.get(lvKeyStr, {}).get('bonusCheckId', 0)
        if bonusCheckId:
            bhcd = BHCD.data.get(bonusCheckId, {})
            return max(0, bhcd.get('times', 0) - p.bonusHistory.get(bonusCheckId, 0))
        return 0

    def fakeAddBonusTime(self):
        p = BigWorld.player()
        spriteChallengeRankInfo = SCCD.data.get('spriteChallengeRankInfo', {})
        lvKeyStr = self.getSelfLvKeyStr()
        bonusCheckId = spriteChallengeRankInfo.get(lvKeyStr, {}).get('bonusCheckId', 0)
        if bonusCheckId:
            p.bonusHistory[bonusCheckId] = p.bonusHistory.get(bonusCheckId, 0) + 1

    def getBuffByDiffIdx(self, lvKey, diffIdx):
        if not gameglobal.rds.configData.get('enableSpriteChallengeSpBuff', False):
            return 0
        return SCD.data.get((lvKey, diffIdx), {}).get('displayStateId', 0)

    def getFullBuffByDiffIdx(self, lvKey, diffIdx):
        if not gameglobal.rds.configData.get('enableSpriteChallengeSpBuff', False):
            return []
        return SCD.data.get((lvKey, diffIdx), {}).get('stateId', [])

    def getFullAffByDiffIdx(self, lvKey, diffIdx):
        return SCD.data.get((lvKey, diffIdx), {}).get('affixNo', [])

    def getSelfLvKey(self):
        endlessAvailableLv = SCCD.data.get('spriteChallengeAvailableLv', {})
        defaultLvType = gametypes.SPRITE_CHALLENGE_LV_45
        if endlessAvailableLv:
            defaultLvType = endlessAvailableLv.keys()[0]
        p = BigWorld.player()
        for lvType, lvRange in endlessAvailableLv.iteritems():
            if lvRange[0] <= p.lv <= self.convertMaxLv(lvRange[1]):
                return lvType

        return defaultLvType

    def convertMaxLv(self, lvMax):
        convertLvs = SCCD.data.get('maxLvConvert', ())
        if len(convertLvs) == 2 and lvMax == convertLvs[0]:
            return convertLvs[1]
        return lvMax

    def getSelfLvKeyStr(self):
        return self.getLvKeyStrByLvType(self.getSelfLvKey())

    def isRewardGeted(self, lvKey, diffIdx):
        p = BigWorld.player()
        spriteChallengeInfo = getattr(p, 'spriteChallengeInfo', {})
        lvKeyStr = self.getLvKeyStrByLvType(lvKey)
        challengeInfo = spriteChallengeInfo.get(lvKeyStr, {})
        return challengeInfo.get('finishProgress', {}).get(diffIdx, 0)

    def getLvKeyStrByLvType(self, lvKey):
        endlessAvailableLv = SCCD.data.get('spriteChallengeAvailableLv', ())
        lvRange = endlessAvailableLv.get(lvKey, ())
        if lvRange:
            return '%d_%d' % lvRange
        return '0_0'

    def turnLvKeyStr2LvKey(self, lvKeyStr):
        endlessAvailableLv = SCCD.data.get('spriteChallengeAvailableLv', ())
        for lvKey, lvRange in enumerate(endlessAvailableLv):
            if lvRange:
                if '%d_%d' % lvRange == lvKeyStr:
                    return lvKey

        return 0

    def getWeekRewardLeftTime(self):
        endTime = SCCD.data.get('weekRewardCrontab', '')
        if endTime == '':
            return 0
        leftTime = utils.getNextCrontabTime(endTime) - utils.getNow()
        return max(0, leftTime)

    def getFakeRankStr(self, topRank):
        if 0 < topRank <= const.TOP_SPRITE_CHALLENGE_REAL_TOP_NUM:
            return str(topRank)
        if topRank > const.TOP_SPRITE_CHALLENGE_REAL_TOP_NUM:
            index = topRank - const.TOP_SPRITE_CHALLENGE_REAL_TOP_NUM - 1
            rankStrs = SCCD.data.get('FbRewardsNotInTop', [])
            if index < len(rankStrs[1]):
                rankFrom, rankTo = rankStrs[1][index][1]
                if rankFrom == 0:
                    rankFrom = gameStrings.TEXT_SPRITECHALLENGEHELPER_210
                else:
                    rankFrom = '%d%%' % (rankFrom * 100)
                rankTo = '%d%%' % (rankTo * 100)
                return '%s-%s' % (rankFrom, rankTo)
        return ''

    def getMaxAttendNum(self, diffIdx):
        return SCD.data.get((self.getSelfLvKey(), diffIdx), {}).get('spriteNum', 1)

    def getSeasonRewardLeftTime(self):
        currSeason = self.getCurrentSeasonLocal()
        endTime = SCSLD.data.get(currSeason, {}).get('endTime', '')
        if endTime == '':
            return 0
        leftTime = utils.getNextCrontabTime(endTime) - utils.getNow()
        return max(0, leftTime)

    def getFriendRankGbIds(self, lvKey, diffIdx):
        p = BigWorld.player()
        spriteChallengeInfo = getattr(p, 'spriteChallengeInfo', {})
        friendSpriteChallengeInfo = spriteChallengeInfo.get(lvKey, {}).get('friendSpriteChallengeInfo', {})
        friendList = friendSpriteChallengeInfo.get(diffIdx, [])
        gbIds = [ info[4] for info in friendList ]
        return gbIds

    def startLevel(self, diffIdx):
        p = BigWorld.player()
        spriteChallengeData = SCD.data.get((self.getSelfLvKey(), diffIdx), {})
        attendList, checkList, fameList = self.getAttendAndCheckList(spriteChallengeData.get('spriteNum', 1))
        p.base.spriteChallengeStart(self.getSelfLvKeyStr(), diffIdx, attendList, checkList, fameList)

    def getSeasonAwardKey(self, lvKeyStr = None):
        lvKeyStr = lvKeyStr if lvKeyStr else self.getSelfLvKeyStr()
        season = self.getCurrentSeasonLocal()
        spriteChallengeRankInfo = SCCD.data.get('spriteChallengeRankInfo', {})
        fbNo = spriteChallengeRankInfo.get(lvKeyStr, {}).get('fbNo', 0)
        return (gametypes.TOP_TYPE_SPRITE_CHALLENGE, fbNo * 1000 + season, 0)

    def getWeekAwardKey(self, lvKeyStr = None):
        lvKeyStr = lvKeyStr if lvKeyStr else self.getSelfLvKeyStr()
        season = self.getCurrentSeasonLocal()
        spriteChallengeRankInfo = SCCD.data.get('spriteChallengeRankInfo', {})
        fbNo = spriteChallengeRankInfo.get(lvKeyStr, {}).get('fbNo', 0)
        return (gametypes.TOP_TYPE_SPRITE_CHALLENGE, fbNo * 1000 + 900 + season, 0)

    def getLastSelectCheckList(self, maxNum):
        p = BigWorld.player()
        cList = []
        for i in xrange(maxNum, 0, -1):
            for challengeList in p.spriteChallengeList:
                if len(challengeList) == i:
                    cList = list(challengeList)
                    if self.needFakeLast(maxNum):
                        lastNum = 0
                        for j, info in enumerate(cList):
                            if info[2] == 2:
                                if lastNum == 1:
                                    infoListInfo = list(info)
                                    infoListInfo[2] = 3
                                    cList[j] = infoListInfo
                                lastNum += 1

                    return cList

        return cList

    def getAttendAndCheckList(self, maxNum):
        p = BigWorld.player()
        attendList = []
        checkList = []
        fameList = []
        challengeList = self.getLastSelectCheckList(maxNum)
        for i, info in enumerate(challengeList):
            if i < maxNum:
                attendList.append(info[0])
                checkList.append(info[1])
                if self.needFakeLast(maxNum) and info[2] == 3:
                    fameList.append(2)
                else:
                    fameList.append(info[2])

        spriteIndexs = p.summonSpriteList.keys()
        spriteIndexs.sort(cmp=self.spriteSortFunc)
        index = len(attendList)
        if len(attendList) < maxNum:
            for spIdx in spriteIndexs:
                if spIdx not in attendList:
                    attendList.append(spIdx)
                    checkList.append(0)
                    fameList.append(index)
                    if len(attendList) == maxNum:
                        break
                    index += 1

        return (attendList, checkList, fameList)

    def getSpriteSlotTip(self, diffIdx, slot):
        diffInfo = SCD.data.get((self.getSelfLvKey(), diffIdx))
        return diffInfo.get('tip%d' % (slot + 1), '')

    def getSpriteSlotBuff(self, diffIdx, slot):
        diffInfo = SCD.data.get((self.getSelfLvKey(), diffIdx))
        return diffInfo.get('initBuff', [-1,
         -1,
         -1,
         -1])[slot]

    def spriteSortFunc(self, idx1, idx2):
        p = BigWorld.player()
        spriteInfo1 = p.summonSpriteList.get(idx1, {})
        spriteInfo2 = p.summonSpriteList.get(idx2, {})
        if spriteInfo1 and spriteInfo2:
            return cmp(spriteInfo2.get('props', {}).get('lv', 0), spriteInfo1.get('props', {}).get('lv', 0))
        return 0

    def addFamiEnd(self):
        p = BigWorld.player()
        for challengeList in p.spriteChallengeList:
            for i, info in enumerate(challengeList):
                if len(info) == 2:
                    info = list(info)
                    info.append(-1)
                    challengeList[i] = info

    def needResetSpriteFami(self, maxNum = 4):
        challengeList = self.getLastSelectCheckList(maxNum)
        if len(challengeList) != maxNum:
            return True
        orderList = [ info[2] for info in challengeList ]
        for i in xrange(maxNum):
            if i not in orderList:
                return True

        return False

    def needFakeLast(self, maxNum):
        return maxNum == 4 and self.getSelfLvKey() == gametypes.SPRITE_CHALLENGE_LV_45

    def getTopSpriteFami(self, maxNum = 4, onlyIdx = False):
        topInfos = []
        p = BigWorld.player()
        for spriteIdx in p.summonSpriteList:
            spriteInfo = p.summonSpriteList.get(spriteIdx, {})
            fami = int(spriteInfo.get('props', {}).get('familiar', 0))
            insert = False
            for i, topInfo in enumerate(topInfos):
                if i >= maxNum:
                    break
                if fami > topInfo[0]:
                    topInfos.insert(i, [fami, spriteIdx])
                    insert = True
                    break

            if not insert and len(topInfos) < maxNum:
                topInfos.append([fami, spriteIdx])

        topInfos = topInfos[:maxNum]
        for i in xrange(len(topInfos), maxNum):
            topInfos.append([0, 0])

        if onlyIdx:
            topInfos = [ info[1] for info in topInfos ]
        elif self.needFakeLast(maxNum) and maxNum == 4:
            topInfos[3][0] = topInfos[2][0]
        return topInfos

    def setLinkedUIVisible(self, visible):
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ACTION_BARS, visible)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WUSHUANG_BARS, visible)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_SUMMONED_SPRITE_UNIT_FRAMEV2, visible)
