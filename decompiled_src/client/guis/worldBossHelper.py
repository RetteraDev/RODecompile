#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/worldBossHelper.o
import BigWorld
import Math
import const
import utils
import gameglobal
import formula
import gametypes
from gameclass import Singleton
from helpers import tickManager
from gamestrings import gameStrings
from guis import uiUtils
from guis import uiConst
from data import duel_config_data as DCD
from data import monster_model_client_data as MMCD
from data import world_monster_refresh_data as WMRD
QUERY_INTERVAL = 0.5
LOOP_QUERY_RANK_INTERVAL = 8
NOTICE_INTERVAL = 300
NOTICE_ENT_NUM = 300
CHECK_OFFSET = 1
QUEST_TRACK_REMAIN_TIME = 120
WORLD_BOSS_STAGE_NONE = 0
WORLD_BOSS_STAGE_BOSS = 1
WORLD_BOSS_STAGE_BOSS_DIE = 2
WORLD_BOSS_STAGE_RARE_BOSS = 3
WORLD_BOSS_STAGE_RARE_BOSS_DIE = 4

class WorldBossHelper(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.tickId = 0
        self.bossRankCache = {}
        self.bossGuildRankCache = {}
        self.bossDict = {}
        self.lastCheckResult = 0
        self.cacheCheckResult = 0
        self.lastQueryTopTime = 0
        self.lastNoticeTime = 0
        self.queryWorldResultCallback = None
        self.resetCacheResultCallback = None

    def onEnterWorld(self):
        self.lastCheckResult = 0
        self.cacheCheckResult = 0
        self.lastNoticeTime = 0
        self.worldBossResultQueryCheck()

    def clearBossInfos(self):
        self.bossDict = {}
        self.bossRankCache = {}
        self.bossGuildRankCache = {}
        self.stopTick()
        if self.queryWorldResultCallback:
            BigWorld.cancelCallback(self.queryWorldResultCallback)
        self.queryWorldResultCallback = None
        if self.resetCacheResultCallback:
            BigWorld.cancelCallback(self.resetCacheResultCallback)
        self.resetCacheResultCallback = None

    def queryWorldBossInfo(self):
        p = BigWorld.player()
        p.base.queryWorldBossList(0)

    def onActivityStart(self):
        gameglobal.rds.ui.topBar.refreshTopBarWidgets()
        self.startTick()
        self.addWorldBossPushIcon()
        self.queryWorldBossInfo()
        BigWorld.callback(5, self.postCheckQuestBossInfo)
        gameglobal.rds.ui.chat.updatePadChannels()

    def postCheckQuestBossInfo(self):
        self.queryWorldBossInfo()

    def onActivityEnd(self):
        gameglobal.rds.ui.topBar.refreshTopBarWidgets()
        self.stopTick()
        if self.resetCacheResultCallback:
            BigWorld.cancelCallback(self.resetCacheResultCallback)
        self.resetCacheResultCallback = None
        self.removeWorldBossPushIcon()
        self.removeWorldBossChooseBuffPush()
        gameglobal.rds.ui.worldBossBuff.hide()
        self.onLeaveWorldBossRange()
        self.onGetBossInfo([])
        gameglobal.rds.ui.chat.updatePadChannels()

    def getRangeRefId(self):
        return self.lastCheckResult

    def getCacheRefId(self):
        return self.cacheCheckResult

    def _getInRangeWorldBossRefId(self):
        p = BigWorld.player()
        baseCheckRadius = DCD.data.get('worldBossAreaWidth', 60)
        checkResult = 0
        if not formula.inWorld(p.spaceNo):
            return 0
        for refId in self.bossDict:
            bossInfo = self.bossDict.get(refId, {})
            if not bossInfo:
                continue
            bossPos = bossInfo.get('position', (0, 0))
            if self.lastCheckResult == refId:
                checkRadius = baseCheckRadius + CHECK_OFFSET
            else:
                checkRadius = baseCheckRadius - CHECK_OFFSET
            if abs(p.position.x - bossPos[0]) < checkRadius and abs(p.position.z - bossPos[2]) < checkRadius:
                checkResult = refId
                break

        return checkResult

    def isInWorldBossActivity(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableWorldBoss', False):
            return False
        return getattr(p, 'worldBossActivityState', 0) != 0

    def isInWorldBossRange(self):
        return self.lastCheckResult != 0

    def isShowQuestTrack(self):
        return self.cacheCheckResult != 0

    def onEnterWorldBossRange(self, refId):
        gameglobal.rds.ui.questTrack.showWorldBossTrack(True)
        self.checkShowSwitchBattleCloth()
        p = BigWorld.player()
        if self.isRareBossRefId(refId):
            p.cell.checkForcePK(gametypes.IMP_PK_RESOURCE_WORLDBOSS)

    def onLeaveWorldBossRange(self):
        p = BigWorld.player()
        p.cell.checkForcePK(gametypes.IMP_PK_RESOURCE_WORLDBOSS)

    def startTick(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = tickManager.addTick(0.8, self.checkLoop)
        self.lastCheckResult = 0

    def getAttendValue(self, refId):
        p = BigWorld.player()
        attendDict = getattr(p, 'worldBossAttendDict', {})
        return attendDict.get(refId, 0)

    def stopTick(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = 0
        self.lastCheckResult = 0
        self.cacheCheckResult = 0
        gameglobal.rds.ui.questTrack.showWorldBossTrack(False)

    def checkLoop(self):
        p = BigWorld.player()
        if not p.inWorld:
            return
        else:
            if not self.isInWorldBossActivity():
                checkResult = 0
            elif not formula.inWorld(p.spaceNo):
                checkResult = 0
            else:
                checkResult = self._getInRangeWorldBossRefId()
            if self.lastCheckResult != checkResult:
                self.lastQueryTopTime = 0
                self.lastCheckResult = checkResult
                if checkResult:
                    if self.resetCacheResultCallback:
                        BigWorld.cancelCallback(self.resetCacheResultCallback)
                    self.resetCacheResultCallback = None
                    self.cacheCheckResult = self.lastCheckResult
                    self.onEnterWorldBossRange(checkResult)
                else:
                    self.addResetCacheCallBack()
                    self.onLeaveWorldBossRange()
            if self.cacheCheckResult:
                if utils.getNow() - self.lastQueryTopTime > LOOP_QUERY_RANK_INTERVAL:
                    self.queryBossRankInfo(checkResult)
                    self.lastQueryTopTime = utils.getNow()
            return

    def addResetCacheCallBack(self):
        if self.resetCacheResultCallback:
            BigWorld.cancelCallback(self.resetCacheResultCallback)
        self.resetCacheResultCallback = BigWorld.callback(QUEST_TRACK_REMAIN_TIME, self.doResetCacheResultCallBack)

    def doResetCacheResultCallBack(self):
        if self.lastCheckResult == 0:
            self.cacheCheckResult = 0
            gameglobal.rds.ui.questTrack.showWorldBossTrack(False)

    def addWorldBossPushIcon(self):
        if not self.isInWorldBossActivity():
            return
        if uiConst.MESSAGE_TYPE_WORLD_BOSS not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WORLD_BOSS)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_BOSS, {'click': self.onPushMsgClick})

    def onPushMsgClick(self):
        gameglobal.rds.ui.worldBossMap.show()

    def removeWorldBossPushIcon(self):
        if uiConst.MESSAGE_TYPE_WORLD_BOSS in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_BOSS)

    def worldBossResultQueryCheck(self, noCheck = False):
        if not gameglobal.rds.configData.get('enableWorldBoss', False):
            return
        worldBossResultPushRange = DCD.data.get('worldBossResultPushRange', ())
        if not worldBossResultPushRange:
            return
        p = BigWorld.player()
        if not p or not p.inWorld:
            return
        now = utils.getNow()
        startCrontab, endCrontab = worldBossResultPushRange
        if self.queryWorldResultCallback:
            BigWorld.cancelCallback(self.queryWorldResultCallback)
        if noCheck or utils.inCrontabRange(startCrontab, endCrontab):
            self.queryWorldBossAccount()
            endTime = utils.getNextCrontabTime(endCrontab)
            if endTime > now:
                self.queryWorldResultCallback = BigWorld.callback(endTime - now, self.worldBossResultQueryCheck)
        else:
            self.removeWorldBossResultPushIcon()

    def queryWorldBossAccount(self):
        p = BigWorld.player()
        if not getattr(p, 'worldBossAccount', None):
            p.base.queryWorldBossAccount()

    def addWorldBossResultPushIcon(self):
        if uiConst.MESSAGE_TYPE_WORLD_BOSS_RESULT not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WORLD_BOSS_RESULT)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_BOSS_RESULT, {'click': self.onResultPushMsgClick})

    def onResultPushMsgClick(self):
        self.removeWorldBossResultPushIcon()
        gameglobal.rds.ui.worldBossMap.show(True)

    def removeWorldBossResultPushIcon(self):
        if uiConst.MESSAGE_TYPE_WORLD_BOSS_RESULT in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_BOSS_RESULT)

    def onWorldBossBuffStatRefresh(self, showWnd = False):
        p = BigWorld.player()
        buffList = getattr(p, 'worldBossChooseBuffs', 0)
        isDrop = getattr(p, 'worldBossBuffDrop', False)
        if self.isInWorldBossActivity() and buffList and not isDrop:
            self.addWorldBossChooseBuffPush()
            if showWnd:
                gameglobal.rds.ui.worldBossBuff.show()
        else:
            self.removeWorldBossChooseBuffPush()
            gameglobal.rds.ui.worldBossBuff.hide()

    def addWorldBossChooseBuffPush(self):
        if not self.isInWorldBossActivity():
            return
        if uiConst.MESSAGE_TYPE_WORLD_BOSS_BUFF not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WORLD_BOSS_BUFF)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_BOSS_BUFF, {'click': self.onBuffPushMsgClick})

    def removeWorldBossChooseBuffPush(self):
        if uiConst.MESSAGE_TYPE_WORLD_BOSS_BUFF in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_BOSS_BUFF)

    def onBuffPushMsgClick(self):
        gameglobal.rds.ui.worldBossBuff.show()

    def onChooseBuff(self, buffId):
        gameglobal.rds.ui.worldBossBuff.refreshInfo()

    def inSelectBuffState(self):
        p = BigWorld.player()
        if self.getChooseBuff():
            return False
        worldBossChooseBuffs = getattr(p, 'worldBossChooseBuffs', [])
        return bool(worldBossChooseBuffs)

    def getSelectBuffList(self):
        p = BigWorld.player()
        worldBossChooseBuffs = getattr(p, 'worldBossChooseBuffs', [])
        return worldBossChooseBuffs

    def getChooseBuff(self):
        p = BigWorld.player()
        worldBossChooseBuffs = getattr(p, 'worldBossChooseBuffs', 0)
        if type(worldBossChooseBuffs) == int:
            return worldBossChooseBuffs
        else:
            return 0

    def showSwichBattleClothConfirm(self):
        p = BigWorld.player()
        if p.operation['commonSetting'][17] == True:
            return
        msg = gameStrings.SWITCH_ZHANPAO_CONFIRM
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesBtnText=gameStrings.COMMON_BTN_YES, noBtnText=gameStrings.COMMON_BTN_NO, yesCallback=self.switchBattleCloth)

    def switchBattleCloth(self):
        p = BigWorld.player()
        if not p.stateMachine.checkStatus(const.CT_CLAN_WAR_ARMOR):
            return
        if p.operation['commonSetting'][17] == True:
            return
        p.operation['commonSetting'][17] = True
        p.sendOperation()
        uiUtils.setClanWarArmorMode()

    def queryBossRankInfo(self, refId, isGuild = True):
        p = BigWorld.player()
        version = 0
        if isGuild:
            p.base.quickQueryTopUniversal(gametypes.TOP_TYPE_WORLD_BOSS_GUILD_RANK, version, str(refId))
        else:
            p.base.quickQueryTopUniversal(gametypes.TOP_TYPE_WORLD_BOSS_RANK, version, str(refId))

    def getBossRankInfo(self, refId):
        rankInfo = self.bossRankCache.get(refId, {})
        rankList = []
        for rankItem in rankInfo.get(gametypes.TOP_UNIVERSAL_DATA_LIST, []):
            rankList.append([rankItem.get(gametypes.TOP_UNIVERSAL_ROLE_NAME, ''), rankItem.get(gametypes.TOP_UNIVERSAL_VALUE, '')])

        return rankList

    def getBossTotalDmg(self, refId):
        rankInfo = self.bossGuildRankCache.get(refId, {})
        totalDmg = max(0, rankInfo.get(gametypes.TOP_UNIVERSAL_WORLD_BOSS_TOTAL_DMG, 0))
        return totalDmg

    def getGuildBossRankInfo(self, refId):
        rankInfo = self.bossGuildRankCache.get(refId, {})
        totalDmg = max(1, rankInfo.get(gametypes.TOP_UNIVERSAL_WORLD_BOSS_TOTAL_DMG, 0))
        rankList = []
        for rankItem in rankInfo.get(gametypes.TOP_UNIVERSAL_DATA_LIST, []):
            dmg = rankItem.get(gametypes.TOP_UNIVERSAL_VALUE, '')
            percent = dmg * 1.0 / totalDmg
            rankList.append([rankItem.get(gametypes.TOP_UNIVERSAL_GUILD_NAME, ''),
             '%0.1f%%' % (percent * 100),
             dmg,
             rankItem.get(gametypes.TOP_UNIVERSAL_GUILD_NUID, 0)])

        return rankList

    def onGetBossRankInfo(self, rankInfo):
        refId = int(rankInfo[gametypes.TOP_UNIVERSAL_KEY])
        topId = rankInfo[gametypes.TOP_UNIVERSAL_TOP_ID]
        rankList = rankInfo[gametypes.TOP_UNIVERSAL_DATA_LIST]
        rankList.sort(cmp=self.rankSortFunction, reverse=True)
        if topId == gametypes.TOP_TYPE_WORLD_BOSS_GUILD_RANK:
            self.bossGuildRankCache[refId] = rankInfo
        else:
            self.bossRankCache[refId] = rankInfo
        gameglobal.rds.ui.worldBossDetail.refreshRank(refId)
        if self.lastCheckResult == refId:
            gameglobal.rds.ui.questTrack.refreshWorldBossInfo()

    def rankSortFunction(self, val1, val2):
        return cmp(val1.get(gametypes.TOP_UNIVERSAL_VALUE), val2.get(gametypes.TOP_UNIVERSAL_VALUE))

    def getWorldBossInfos(self):
        return self.bossDict

    def seekToWorldBoss(self, refId):
        bossInfo = self.bossDict.get(refId, {})
        position = bossInfo.get('position', None)
        if position:
            pos = Math.Vector3(position[0], position[1], position[2])
            uiUtils.findPosByPos(1, pos)

    def getWorldBossDetail(self, refId):
        detail = self.bossDict.get(refId, {})
        if not detail:
            return {}
        detail['guildRank'] = self.getGuildBossRankInfo(refId)
        detail['personalRank'] = self.getBossRankInfo(refId)
        detail['totalDmg'] = self.getBossTotalDmg(refId)
        detail['attendVal'] = self.getAttendValue(refId)
        return detail

    def getWorldBossInfo(self, refId):
        return self.bossDict.get(refId, {})

    def getWorldBossRefList(self):
        return self.bossDict.keys()

    def getBossRoundImgPath(self, bossType):
        iconId = MMCD.data.get(bossType, {}).get('worldBossPicId', 1)
        return 'worldBoss/round/%03d.dds' % iconId

    def getBossImgPath(self, bossType):
        iconId = MMCD.data.get(bossType, {}).get('worldBossPicId', 1)
        return 'worldBoss/card/%03d.dds' % iconId

    def getBossLargeImgPath(self, bossType):
        iconId = MMCD.data.get(bossType, {}).get('worldBossPicId', 1)
        return 'worldBoss/card/big_%03d.dds' % iconId

    def getBossMapImgPath(self, bossType):
        iconId = MMCD.data.get(bossType, {}).get('worldBossPicId', 1)
        return 'worldBoss/map/%03d.dds' % iconId

    def getBossLittleMapImgPath(self, bossType):
        iconId = MMCD.data.get(bossType, {}).get('worldBossPicId', 1)
        return 'worldBoss/map/small_%03d.dds' % iconId

    def onGetBossInfo(self, bossList):
        self.bossDict = {}
        for bossInfo in bossList:
            refId = bossInfo['refId']
            charType = bossInfo['bossType']
            self.bossDict[refId] = bossInfo
            bossInfo['bossRoundIcon'] = self.getBossRoundImgPath(charType)
            bossInfo['bossName'] = MMCD.data.get(charType, {}).get('name', '')
            bossInfo['bossIcon'] = self.getBossLargeImgPath(charType)
            bossInfo['bossSmallIcon'] = self.getBossImgPath(charType)
            bossInfo['mapIcon'] = self.getBossMapImgPath(charType)
            bossInfo['fortId'] = WMRD.data.get(refId, {}).get('fortId', 0)
            bossInfo['mapLittleIcon'] = self.getBossLittleMapImgPath(charType)
            bossInfo['desc'] = MMCD.data.get(charType, {}).get('desc', '')
            bossInfo['isRare'] = self.isRareBoss(charType)

        if self.cacheCheckResult not in self.bossDict:
            self.cacheCheckResult = 0
        self.checkLoop()
        gameglobal.rds.ui.worldBossDetail.refreshInfo()
        gameglobal.rds.ui.littleMap.refreshWorldBossIcon()
        gameglobal.rds.ui.map.addWorldBossIcons()
        gameglobal.rds.ui.worldBossMap.refreshInfo()

    def getStageTipText(self):
        currStage = self.getCurrentStage()
        worldBossStageText = DCD.data.get('worldBossStageTips', ['', '', ''])
        if currStage == WORLD_BOSS_STAGE_BOSS:
            return worldBossStageText[0]
        if currStage == WORLD_BOSS_STAGE_BOSS_DIE:
            return worldBossStageText[1]
        if currStage in [WORLD_BOSS_STAGE_RARE_BOSS, WORLD_BOSS_STAGE_RARE_BOSS_DIE]:
            return worldBossStageText[2]
        return ''

    def getCurrentStage(self):
        currStage = WORLD_BOSS_STAGE_NONE
        for refId in self.bossDict:
            bossInfo = self.bossDict[refId]
            if not self.isRareBossRefId(refId):
                if bossInfo.get('isLive', False):
                    currStage = WORLD_BOSS_STAGE_BOSS
                else:
                    currStage = WORLD_BOSS_STAGE_BOSS_DIE

        for refId in self.bossDict:
            bossInfo = self.bossDict[refId]
            if self.isRareBossRefId(refId):
                if bossInfo.get('isLive', False):
                    currStage = WORLD_BOSS_STAGE_RARE_BOSS
                elif currStage == WORLD_BOSS_STAGE_BOSS_DIE:
                    currStage = WORLD_BOSS_STAGE_RARE_BOSS_DIE

        return currStage

    def onUpdateAttendValue(self):
        gameglobal.rds.ui.questTrack.refreshWorldBossInfo()

    def getBossBaseInfoByBossId(self, charType):
        bossInfo = {}
        bossInfo['bossRoundIcon'] = self.getBossRoundImgPath(charType)
        bossInfo['bossName'] = MMCD.data.get(charType, {}).get('name', '')
        bossInfo['bossIcon'] = self.getBossLargeImgPath(charType)
        bossInfo['bossSmallIcon'] = self.getBossImgPath(charType)
        bossInfo['mapIcon'] = self.getBossMapImgPath(charType)
        bossInfo['mapLittleIcon'] = self.getBossLittleMapImgPath(charType)
        bossInfo['desc'] = MMCD.data.get(charType, {}).get('desc', '')
        bossInfo['isRare'] = self.isRareBoss(charType)
        return bossInfo

    def getWorldBossRewards(self, refId):
        if self.isRareBossRefId(refId):
            return DCD.data.get('worldBossRareRewardList', [])
        return DCD.data.get('worldBossRewardList', [])

    def getNormalWorldBossIds(self):
        return DCD.data.get('normalWorldBossIds', [])

    def getRareWorldBossId(self):
        return DCD.data.get('rareWorldBossId', [0])[0]

    def isRareBossRefId(self, refId):
        bossId = self.bossDict.get(refId, {}).get('bossType', 0)
        if bossId:
            return bossId == self.getRareWorldBossId()
        return False

    def isRareBoss(self, bossId):
        return bossId == self.getRareWorldBossId()

    def getWorldBossCardInfo(self):
        p = BigWorld.player()
        cardInfo = {}
        worldBossCardInfo = getattr(p, 'worldBossCardInfo', {})
        for monsterId in worldBossCardInfo:
            cardInfo[monsterId] = worldBossCardInfo[monsterId].get('cnt', 0)

        return cardInfo

    def checkShowSwitchBattleCloth(self):
        entitiesNum = len(BigWorld.entities)
        if utils.getNow() - self.lastNoticeTime > NOTICE_INTERVAL:
            if entitiesNum > NOTICE_ENT_NUM:
                self.showSwichBattleClothConfirm()
                self.lastNoticeTime = utils.getNow()

    def addTestInfo(self):
        ttl = 1000
        bossList = [{'bossType': 25152,
          'ttl': ttl,
          'startTime': utils.getNow(),
          'isLive': False,
          'position': (100, 200, 100),
          'rareWorldBoss': False,
          'refId': 209,
          'firstAttacker': {},
          'killer': {}}]
        p = BigWorld.player()
        p.worldBossActivityState = True
        self.onGetBossInfo(bossList)


def getInstance():
    return WorldBossHelper.getInstance()
