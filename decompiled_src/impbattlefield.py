#Embedded file name: /WORKSPACE/data/entities/client/impl/impbattlefield.o
import BigWorld
import Sound
import json
from Scaleform import GfxValue
import sMath
import copy
import gameglobal
import gametypes
import const
import gamelog
import formula
import utils
import cPickle
import zlib
import random
from sMath import distance3D
import logicInfo
from item import Item
from helpers import CEFControl
import clientcom
import clientUtils
from skillDataInfo import SkillInfoVal
from guis import generalPushMappings
from fbStatistics import FubenStats
from battleFieldBagCommon import BattleFieldBagCommon
from callbackHelper import Functor
import appSetting
from guis import uiConst
from guis import uiUtils
from guis import events
from helpers.eventDispatcher import Event
from sfx import keyboardEffect
from sfx import sfx
from gamestrings import gameStrings
from helpers import ccControl
from guis.messageBoxProxy import MBButton
from data import battle_field_data as BFD
from data import battle_field_mode_data as BFMD
from data import sys_config_data as SCD
from data import game_msg_data as GMD
from data import zaiju_data as ZD
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD
from data import fb_entity_data as FED
BATTLE_FIELD_START = 1
BATTLE_FIELD_QUIT = 2

class ImpBattleField(object):

    def _refreshBattleFieldInfo(self):
        gameglobal.rds.ui.teamComm.refreshMemberInfo(False)
        gameglobal.rds.ui.battleField.refreshBFStats()
        gameglobal.rds.ui.deadAndRelive.bfReliveCountDown()

    def battleFieldQuery(self, info):
        info = cPickle.loads(zlib.decompress(info))
        memberStats, sideStats, memberInfo, res, timeRec, fbNo, isBfTroopLogon, isNeedRefreshCounting, sideIndex, sideNUID, firstBloodKiller, headerGbId, arrange, sideName, allSideNUID, extra = info
        self.bfDuelStats = memberStats
        self.battleFieldTeam = memberInfo
        if self == BigWorld.player():
            self._refreshMemberBuffState()
        self.bfSideStats = sideStats
        self.bfRes = res
        self.bfTimeRec = timeRec
        self.battleFieldFbNo = fbNo
        self.bfSideIndex = sideIndex
        self.bfSideNUID = sideNUID
        self.bfHeaderGbId = headerGbId
        self.bfArrange = arrange
        self.bfAllSideNUID = allSideNUID
        self.isBfTroopLogon = isBfTroopLogon
        if isNeedRefreshCounting:
            self.isNeedRefreshCounting = True
        self.setBattleFieldPuppetName()
        self._setMemberPos()
        self._refreshBattleFieldInfo()
        self.firstBloodKiller = firstBloodKiller
        if firstBloodKiller:
            self._calcFirstBloodKillerTitle()
        self.updateBfMemStats()
        scoreList = extra.get('scoreList', [])
        if scoreList:
            self.bfScoreList = scoreList
        if self.inFubenType(const.FB_TYPE_BATTLE_FIELD_FLAG):
            self.bfFlagInfo = extra.get('flagInfo', {})
            gameglobal.rds.ui.littleMap.showBfFlagInfo()
        elif self.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
            self.bfFortInfo = extra.get('fortInfo', {})
            self.bfPlaneInfo = extra.get('planeInfo', {})
        elif self.inFubenType(const.FB_TYPE_BATTLE_FIELD_HUNT):
            trapInfoList = []
            inTrapPos = extra.get('inTrapPos', None)
            if inTrapPos:
                trapInfoList.extend(inTrapPos)
            inTrapList = extra.get('inTrapList', [])
            if inTrapList:
                trapInfoList.extend(inTrapList)
            for pos, srcGbId, desGbId in inTrapList:
                if desGbId:
                    gameglobal.rds.ui.littleMap.addBFHuntIcon(uiConst.ICON_TYPE_HUNT_TRAP, srcGbId, desGbId, pos, 'catch', forceUpdate=False)
                else:
                    gameglobal.rds.ui.littleMap.addBFHuntIcon(uiConst.ICON_TYPE_HUNT_TRAP, srcGbId, desGbId, pos, 'lose', forceUpdate=False)

            gameglobal.rds.ui.littleMap.showBFHuntInfo()
        elif self.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA):
            self.availableRoleZaijuSet = extra.get('availableRoleZaijuSet', set())
            gameglobal.rds.ui.bfDotaChooseHeroRight.refreshFrame()
            self.enemyInRangeBFDotaInfoList = extra.get('enemyInRangeBFDotaInfoList', [])
            allStats = extra.get('allStats', {})
            for syncType, synVal in allStats.iteritems():
                self.syncBattleFieldOwnStats(synVal, syncType)

            roleZaijuInfo = extra.get('roleZaijuInfo', {})
            for gbId, zaijuId in roleZaijuInfo.iteritems():
                self.bfDotaZaijuRecord[gbId] = zaijuId
                self.preloadDotaZaiju(gbId, zaijuId)
                if gbId == self.gbId and zaijuId == 0 and not getattr(self, 'backToBfEnd', False):
                    self.showBfDotaChooseHero()

            gameglobal.rds.ui.bfDotaChooseHeroLeft.refreshFrame()
            skillsInfo = extra.get('talentSkillIds', {})
            for gbId, skills in skillsInfo.iteritems():
                self.bfDotaTalentSkillRecord[gbId] = skills

            self.availableTalenSkillIds = []
            for availalbeTalenSkillId in DCD.data.get('BATTLE_FIELD_DOTA_AVAILABLE_TALENT_SKILL_LIST', []):
                self.availableTalenSkillIds.append(availalbeTalenSkillId)

            self.availableTalenSkillIds.extend(list(extra.get('availableTalenSkillIds', [])))
            gameglobal.rds.ui.littleMap.refreshBattleFiledEntity()
            gamelog.debug('@lhb bf#dota extra', extra)
        gameglobal.rds.ui.bFFortInfoV1.setSideName(sideName)
        gameglobal.rds.ui.bFFlagStatsV1.setSideName(sideName)
        self.resetBulletInfo()
        gameglobal.rds.ui.teamComm.refreshMemberInfo(True)

    def resetBulletInfo(self):
        if hasattr(self, 'bfSideNUID') and self.bfSideNUID and hasattr(self, 'bfBulletInfo') and self.bfBulletInfo:
            self.bfBulletInfo = {}

    def isSameBFTeam(self, tgtGbId):
        try:
            srcIndex = self.bfArrange.index(self.gbId)
            tgtIndex = self.bfArrange.index(tgtGbId)
        except:
            return False

        if srcIndex / const.TEAM_MAX_NUMBER == tgtIndex / const.TEAM_MAX_NUMBER:
            return True
        else:
            return False

    def battleFieldArrange(self, arrange):
        gamelog.debug('@hjx bf#battleFieldArrange:', arrange)
        gameglobal.rds.ui.group.changeBFArrangeData(self.bfArrange, arrange)
        self.bfArrange = arrange
        gameglobal.rds.ui.group.refreshGroupInfo()
        gameglobal.rds.ui.teamComm.refreshMemberInfo(False)

    def syncBattleFieldMemberCombatStats(self, gbId, memStats, fromHostName):
        gamelog.debug('@hjx bf#battleFieldMemberCombatStats:', gbId, type(memStats))
        if not self.bfDuelStats.has_key(gbId):
            self.bfDuelStats[gbId] = FubenStats()
        self.bfDuelStats[gbId].patchStats(memStats)
        self.updateBfMemStats()
        gameglobal.rds.ui.dispatchEvent(events.EVNET_BF_DUEL_STATE_CHAGNE, (gbId, memStats, fromHostName))

    def triggerWeakProtect(self):
        gamelog.debug('@lhb triggerWeakProtect')
        gameglobal.rds.ui.deadAndRelive.isTriggerWeakProtect = True
        gameglobal.rds.ui.deadAndRelive.setTriggerWeakProtect()

    def syncBattleFieldMemberMonsterStats(self, gbId):
        gamelog.debug('@hjx bf#battleFieldMemberMonsterStats:', gbId)
        if not self.bfDuelStats.has_key(gbId):
            self.bfDuelStats[gbId] = FubenStats()
        self.bfDuelStats[gbId].record(FubenStats.K_KILL_MONSTER_CNT, 1)
        self.updateBfMemStats()

    def battleFieldPunishByReport(self, fbNo, index):
        gamelog.debug('@hjx bf#battleFieldPunishByReport:', fbNo)
        forceKictOutIntervalByReport = DCD.data.get('forceKictOutIntervalByReport', 10)
        reportDesc = DCD.data.get('reportDesc', {})
        msg = '你因为如下原因被过半队友举报:\n' + reportDesc.get(index, '') + '\n'
        buttons = [MBButton('确定', None)]
        gameglobal.rds.ui.messageBox.show(True, '提醒', msg + '强制被踢出战场倒计时:', buttons, repeat=forceKictOutIntervalByReport)

    def _isInMemStats(self, gbId):
        index = -1
        for i, stats in enumerate(self.bfMemStats):
            if stats and stats.has_key('gbId') and stats['gbId'] == gbId:
                index = i
                break

        return index

    def updateBfMemStats(self):
        for mGbId, mDuelStats in self.bfDuelStats.iteritems():
            index = self._isInMemStats(mGbId)
            memItem = self.getMemInfoByGbId(mGbId)
            if not memItem:
                continue
            item = {'damage': mDuelStats.getStats(FubenStats.K_DAMAGE),
             'gbId': mGbId,
             'roleName': memItem['roleName'],
             'level': memItem['level'],
             'school': memItem['school'],
             'cure': mDuelStats.getStats(FubenStats.K_CURE),
             'killNum': mDuelStats.getStats(FubenStats.K_KILL_AVATAR_CNT),
             'deathNum': mDuelStats.getStats(FubenStats.K_DEATH_CNT),
             'assistNum': mDuelStats.getStats(FubenStats.K_ASSIST_CNT),
             'killMonsterNum': mDuelStats.getStats(FubenStats.K_KILL_MONSTER_CNT)}
            if index != -1:
                self.bfMemStats[index] = item
            else:
                self.bfMemStats.append(item)

    def battleFieldRescoure(self, fbNo, subGroupIds, groupId, res):
        self.bfRes = res
        gameglobal.rds.ui.battleField.refreshBFStats()
        gameglobal.rds.ui.bFScoreAward.refreshHpInfo()
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
            if formula.inGuildTournamentQL(fbNo):
                return
            if subGroupIds:
                gameglobal.rds.ui.bFGuildTournamentLive.refreshBFStats(groupId, subGroupIds)

    def battleFieldRescoureWithScore(self, res, bfScoreList):
        self.bfRes = res
        oldScore = getattr(self, 'bfScoreList', {}).get(self.gbId, 0)
        newScore = bfScoreList.get(self.gbId, 0)
        if newScore - oldScore > 0:
            cfgLab = DCD.data.get('huntDefLabel', ('\xb5\xc3\xb7\xd6', '#47E036'))
            gameglobal.rds.ui.showDefaultLabel(cfgLab[0], newScore - oldScore, cfgLab[1])
            soundId = SCD.data.get('HUNT_SOUND_SCORE_ADD', 5109)
            gameglobal.rds.sound.playSound(soundId, position=BigWorld.player().position)
        self.bfScoreList = bfScoreList
        gameglobal.rds.ui.scoreInfo.refreshFrame()
        gameglobal.rds.ui.littleScoreInfo.refreshFrame()

    def battleFieldFlagInfo(self, flagInfo):
        self.bfFlagInfo = flagInfo
        gameglobal.rds.ui.littleMap.showBfFlagInfo()

    def battleFieldHookScore(self, score):
        self.bfHookScore = score
        gameglobal.rds.ui.battleField.refreshHookScore()

    def syncBattleFieldMemberInfo(self, mGbId, mType, mInfo, headerGbId):
        gamelog.debug('@hjx bf#syncBattleFieldMemberInfo:', self.roleName, mGbId, mType, mInfo, headerGbId)
        if mType == gametypes.DUEL_MEM_PUSH or mType == gametypes.DUEL_MEM_UPDATE:
            self.battleFieldTeam[mGbId] = mInfo
        elif mType == gametypes.DUEL_MEM_POP:
            self.battleFieldTeam.pop(mGbId, None)
            self.bfDuelStats.pop(mGbId, None)
        if mInfo.has_key('score'):
            self.bfScoreList[mGbId] = mInfo['score']
        if mGbId in self.reliveTimeRecord and mInfo.get('life', gametypes.LIFE_ALIVE) == gametypes.LIFE_ALIVE:
            self.reliveTimeRecord.pop(mGbId)
        self.bfHeaderGbId = headerGbId
        self.setBattleFieldPuppetName()
        self._setMemberPos()
        gameglobal.rds.ui.teamComm.refreshMemberInfo(False, False)
        gameglobal.rds.ui.battleField.refreshTmpResultWidget()
        gameglobal.rds.ui.bfDotaChooseHeroLeft.refreshFrame()
        if formula.inHuntBattleField(self.mapID):
            gameglobal.rds.ui.scoreInfo.refreshFrame()
            gameglobal.rds.ui.littleScoreInfo.refreshFrame()
        if formula.inDotaBattleField(self.mapID) and not getattr(self, 'isInBfDotaChooseHero', False):
            self.addAceInfo()
        if mType == gametypes.DUEL_MEM_POP or mType == gametypes.DUEL_MEM_PUSH:
            gameglobal.rds.ui.teamComm.refreshMemberInfo()
        else:
            gameglobal.rds.ui.teamComm.refreshSingleMember(mGbId)

    def addAceInfo(self):
        deadCnt = 0
        for gbId, memInfo in self.battleFieldTeam.iteritems():
            if memInfo['sideNUID'] != self.bfSideNUID and memInfo['life'] == gametypes.LIFE_DEAD:
                deadCnt += 1

        maxNum = BFD.data.get(self.mapID, {}).get('maxNum', 10)
        if deadCnt == maxNum / 2:
            if getattr(self, 'isAceKillValid', False):
                gameglobal.rds.ui.bfDotaKill.addAceKillInfo()
                self.isAceKillValid = False
        else:
            self.isAceKillValid = True

    def syncBattleFieldDotaTriggerPskillCD(self, cdInfoDict):
        for pSkillId, nextTriggerTime in cdInfoDict.iteritems():
            self.updatePSkillNextTriggerTime(pSkillId, nextTriggerTime)

        gamelog.debug('@lhb syncBattleFieldDotaTriggerPskillCD ', cdInfoDict)

    def battleFieldCountDown(self, fbNo, enterBFTimeStamp):
        gamelog.debug('@hjx bf#battleFieldCountDown:', self.id, enterBFTimeStamp, self.getServerTime(), fbNo, uiUtils.getDuelCountTime('readyTime', self.getBattleFieldFbNo()))
        gameglobal.rds.ui.battleField.closeTips()
        gameglobal.rds.ui.arena.openArenaMsg()
        readyTime = uiUtils.getDuelCountTime('readyTime', fbNo)
        exitTime = readyTime + enterBFTimeStamp
        quitTime = BFD.data.get(fbNo, {}).get('durationTime', 0) + readyTime + enterBFTimeStamp
        if formula.inHuntBattleField(fbNo):
            if utils.getNow() < exitTime:
                gameglobal.rds.ui.vehicleChoose.setExitTime(exitTime)
            gameglobal.rds.ui.littleScoreInfo.setQuitTime(quitTime)
        elif formula.inDotaBattleField(self.mapID):
            gameglobal.rds.ui.bfDotaChooseHeroRight.exitTime = exitTime
        self.addTimerCount(BATTLE_FIELD_START, readyTime, enterBFTimeStamp)
        gameglobal.rds.ui.bfDotaSimple.enterBFTimeStamp = enterBFTimeStamp

    def battleFieldEndNotify(self, sideStats):
        if not self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return
        fbNo = formula.getFubenNo(self.spaceNo)
        mode = formula.fbNo2BattleFieldMode(fbNo)
        scenarioName = BFMD.data.get(mode, {}).get('scenarioName', '')
        if scenarioName:
            self.scenarioPlay(scenarioName, 0)
        self.bfSideStats = sideStats
        self.motionPin()
        self.showGameMsg(GMDD.data.BATTLE_FIELD_QUIT_IN_COUNT, (uiUtils.getDuelCountTime('quitTime', self.getBattleFieldFbNo()),))
        self.addTimerCount(BATTLE_FIELD_QUIT, uiUtils.getDuelCountTime('quitTime', self.getBattleFieldFbNo()))
        gameglobal.rds.ui.topBar.isQuitBF = True

    def syncBattleFieldOwnStats(self, statsValue, statsType):
        if not hasattr(self, 'bfOwnStas'):
            self.bfOwnStas = {}
        self.bfOwnStas[statsType] = statsValue
        gameglobal.rds.ui.dispatchEvent(events.EVNET_BF_DUEL_STATE_CHAGNE)
        gamelog.debug('@lhb syncBattleFieldOwnStats ', statsValue, statsType)

    def getBfOwnStas(self, type):
        return getattr(self, 'bfOwnStas', {}).get(type, 0)

    def showDonateAdd(self, addDonate, srcType):
        gamelog.debug('@lhb showDonateAdd ', addDonate, srcType)
        gameglobal.rds.ui.showRewardLabel(addDonate, const.REWARD_LABEL_BF_TONGJI)

    def showFinalStaticDetail(self, staticInfo):
        gamelog.debug('@lhb showFinalStaticDetail ', staticInfo)
        self.bfEnd = True
        self.resetBfMemFromTeamInfo()
        self.getBfMemFromStaticInfo(staticInfo)
        gameglobal.rds.ui.bfDotaFinalDetail.refreshInfo()

    def showStaticsDetail(self, staticInfo):
        gamelog.debug('@lhb showStaticsDetail ', staticInfo)
        self.getBfMemFromStaticInfo(staticInfo)

    def showStaticsDetailViaGuild(self, fbNo, subGroupIds, groupId, staticInfo, extraStaticInfo):
        self.getBfMemFromStaticInfo(staticInfo, extraStaticInfo, fbNo)

    def getBfMemFromStaticInfo(self, staticInfo, extraStaticInfo = None, fbNoInput = None):
        if staticInfo.get(const.BF_COMMON_FIRST_BLOOD_GBID, 0):
            self.firstBloodKiller = staticInfo.get(const.BF_COMMON_FIRST_BLOOD_GBID, 0)
        for gbId, memPerform in staticInfo.iteritems():
            isInsert = False
            if gbId == const.BF_COMMON_FIRST_BLOOD_GBID:
                continue
            oldMemPerform = {}
            index = -1
            for idx, perform in enumerate(self.bfMemPerforms):
                if perform['gbId'] == gbId:
                    index = idx
                    oldMemPerform = perform
                    break

            if index < 0:
                oldMemPerform = memPerform
                oldMemPerform['gbId'] = gbId
                isInsert = True
            commonList = [const.BF_COMMON_JIBAI_DONATE,
             const.BF_COMMON_DAMAGE,
             const.BF_COMMON_CURE,
             const.BF_COMMON_BE_DAMAGE,
             const.BF_COMMON_KILL_NUM,
             const.BF_COMMON_ASSIST_NUM,
             'frequentVer',
             'stableVer',
             const.BF_COMMON_SIDE_NUID]
            for type in commonList:
                self.updateMemPerformValue(oldMemPerform, memPerform, type)

            fbNo = formula.getFubenNo(self.spaceNo) if not fbNoInput else fbNoInput
            if formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_RES:
                self.updateMemPerformValue(oldMemPerform, memPerform, const.BF_RES_SPECIAL_BOSS_JIBAI_DONATE, 'bfSpecialScore0')
                oldMemPerform['bfSpecialScore1'] = self.getDonateFromScore(memPerform, const.BF_RES_SPECIAL_ZAIJU_DAMAGE, fbNo) if memPerform.has_key(const.BF_RES_SPECIAL_ZAIJU_DAMAGE) else oldMemPerform.get('bfSpecialScore1', 0)
            elif formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_FLAG:
                oldMemPerform['bfSpecialScore0'] = self.getDonateFromScore(memPerform, const.BF_FLAG_FIGHT_IN_FLAG_TIME, fbNo) if memPerform.has_key(const.BF_FLAG_FIGHT_IN_FLAG_TIME) else oldMemPerform.get('bfSpecialScore0', 0)
                oldMemPerform['bfSpecialScore1'] = self.getDonateFromScore(memPerform, const.BF_FLAG_HOLD_FLAG_CNT, fbNo) if memPerform.has_key(const.BF_FLAG_HOLD_FLAG_CNT) else oldMemPerform.get('bfSpecialScore1', 0)
            elif formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_FORT:
                oldMemPerform['bfSpecialScore0'] = self.getDonateFromScore(memPerform, const.BF_FORT_FIGHT_IN_FLAG_TIME, fbNo) if memPerform.has_key(const.BF_FORT_FIGHT_IN_FLAG_TIME) else oldMemPerform.get('bfSpecialScore0', 0)
                oldMemPerform['bfSpecialScore1'] = self.getDonateFromScore(memPerform, const.BF_FORT_WITH_FLY_DAMAGE_TOTAL, fbNo) if memPerform.has_key(const.BF_FORT_WITH_FLY_DAMAGE_TOTAL) else oldMemPerform.get('bfSpecialScore1', 0)
            elif formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_DOTA:
                self.updateMemPerformValue(oldMemPerform, memPerform, const.BF_DOTA_DAMAGE_WITH_TOWER)
                self.updateMemPerformValue(oldMemPerform, memPerform, const.BF_DOTA_DAMAGE_TO_AVATR)
                self.updateMemPerformValue(oldMemPerform, memPerform, const.BF_DOTA_BE_DAMAGE_FROM_AVATR)
                self.updateMemPerformValue(oldMemPerform, memPerform, const.BF_COMMON_DEATH_NUM)
                self.updateMemPerformValue(oldMemPerform, memPerform, const.BF_DOTA_MAX_COMBO_KILL)
                self.updateMemPerformValue(oldMemPerform, memPerform, const.BF_DOTA_MAX_COMBO_KILL_IN_TIME)
            elif formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_NEW_FLAG:
                oldMemPerform[const.BF_COMMON_JIBAI_DONATE] = self.getNewFlagPointValue(memPerform, const.BF_NEW_FLAG_POINT_SRC_AVATAR, fbNo) if memPerform.has_key(const.BF_NEW_FLAG_POINT_SRC_AVATAR) else oldMemPerform.get(const.BF_COMMON_JIBAI_DONATE, 0)
                oldMemPerform['bfSpecialScore0'] = self.getNewFlagPointValue(memPerform, const.BF_NEW_FLAG_POINT_SRC_MONSTER, fbNo) if memPerform.has_key(const.BF_NEW_FLAG_POINT_SRC_MONSTER) else oldMemPerform.get('bfSpecialScore0', 0)
                oldMemPerform['bfSpecialScore1'] = self.getNewFlagPointValue(memPerform, const.BF_NEW_FLAG_POINT_SRC_TOWER, fbNo) if memPerform.has_key(const.BF_NEW_FLAG_POINT_SRC_TOWER) else oldMemPerform.get('bfSpecialScore1', 0)
            elif formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_CQZZ:
                oldMemPerform['bfSpecialScore0'] = int(memPerform.get(const.BF_CQZZ_POINT_SRC_FLAG, 0)) if memPerform.has_key(const.BF_CQZZ_POINT_SRC_FLAG) else oldMemPerform.get('bfSpecialScore0', 0)
                oldMemPerform['bfSpecialScore1'] = int(memPerform.get(const.BF_CQZZ_POINT_SRC_AVATAR, 0)) if memPerform.has_key(const.BF_CQZZ_POINT_SRC_AVATAR) else oldMemPerform.get('bfSpecialScore1', 0)
                oldMemPerform[const.BF_COMMON_JIBAI_DONATE] = int(memPerform.get(const.BF_CQZZ_POINT_SRC_AVATAR, 0)) if memPerform.has_key(const.BF_CQZZ_POINT_SRC_AVATAR) else oldMemPerform.get(const.BF_COMMON_JIBAI_DONATE, 0)
            if extraStaticInfo:
                oldMemPerform['lv'] = extraStaticInfo.get(gbId, (0, 0, '', 0))[0]
                oldMemPerform['school'] = extraStaticInfo.get(gbId, (0, 0, '', 0))[1]
                oldMemPerform['roleName'] = extraStaticInfo.get(gbId, (0, 0, '', 0))[2]
                oldMemPerform['sideNUID'] = extraStaticInfo.get(gbId, (0, 0, '', 0))[3]
            if not isInsert:
                self.bfMemPerforms[index] = oldMemPerform
            else:
                self.bfMemPerforms.append(memPerform)

        self._genTitleDesc()
        gameglobal.rds.ui.battleField.refreshBFFinalResult()
        gameglobal.rds.ui.battleField.refreshTmpResultWidget()
        gameglobal.rds.ui.bfDotaDetail.refreshInfo()

    def updateMemPerformValue(self, oldMemPeform, memPerform, type, oldKey = None):
        if oldKey == None:
            oldKey = type
        oldMemPeform[oldKey] = memPerform.get(type, oldMemPeform.get(oldKey, 0))

    def getDonateFromScore(self, memPerform, key, fbNo = None):
        if not fbNo:
            fbNo = self.getBattleFieldFbNo()
        if memPerform.has_key(key):
            bfItem = BFD.data.get(fbNo)
            donateKey = '%sDonateVal' % key
            limitKey = '%sDonateLimit' % key
            if bfItem.get(limitKey, 0):
                return int(min(bfItem.get(limitKey, 0), memPerform.get(key, 0) * bfItem.get(donateKey, 0)))
            else:
                return int(memPerform.get(key, 0) * bfItem.get(donateKey, 0))
        else:
            return 0

    def getNewFlagPointValue(self, memPerform, key, fbNo = None):
        keyMap = {const.BF_NEW_FLAG_POINT_SRC_AVATAR: 'newFlagAvatarPointLimit',
         const.BF_NEW_FLAG_POINT_SRC_MONSTER: 'newFlagMonsterPointLimit',
         const.BF_NEW_FLAG_POINT_SRC_TOWER: 'newFlagTowerPointLimit'}
        if not fbNo:
            fbNo = self.getBattleFieldFbNo()
        if memPerform.has_key(key):
            bfItem = BFD.data.get(fbNo, {})
            realKey = keyMap.get(key, '')
            if realKey and bfItem.has_key(realKey):
                return int(min(memPerform.get(key, 0), bfItem.get(realKey, 0)))
            else:
                return int(memPerform.get(key, 0))
        else:
            return 0

    def resetBfMemFromTeamInfo(self):
        gbIdList = []
        bfFrequentVerList = []
        bfStableVerList = []
        for gbId, teamInfo in self.battleFieldTeam.iteritems():
            gbIdList.append(gbId)
            isFindVer = False
            for memPerform in self.bfMemPerforms:
                if memPerform.get('gbId', 0) == gbId:
                    isFindVer = True
                    bfFrequentVerList.append(memPerform.get('frequentVer', 0))
                    bfStableVerList.append(memPerform.get('stableVer', 0))

            if not isFindVer:
                memPerform = {'gbId': 0,
                 'frequentVer': 0,
                 'stableVer': 0,
                 'bfSpecialScore1': 0,
                 'bfSpecialScore0': 0,
                 'damage': 0,
                 'jibai': 0,
                 'cure': 0,
                 'beDamage': 0,
                 'sideNUID': 0}
                memPerform['frequentVer'] = 0
                memPerform['stableVer'] = 0
                memPerform['gbId'] = gbId
                memPerform['roleName'] = self.battleFieldTeam.get(gbId, {}).get('roleName')
                self.bfMemPerforms.append(memPerform)
                bfFrequentVerList.append(0)
                bfStableVerList.append(0)

        tmpDelMem = []
        for i in xrange(0, len(self.bfMemPerforms)):
            memGbId = self.bfMemPerforms[i].get('gbId', 0)
            if memGbId not in gbIdList:
                tmpDelMem.append(self.bfMemPerforms[i])

        for mem in tmpDelMem:
            self.bfMemPerforms.remove(mem)

        return (gbIdList, bfFrequentVerList, bfStableVerList)

    def showBattleFieldHistoryInfo(self, historyInfo, qType):
        historyInfo = cPickle.loads(zlib.decompress(historyInfo))
        gamelog.debug('@lhb showBattleFieldHistoryInfo ', historyInfo)
        battleFieldFortHistory = historyInfo.get('battleFieldFortHistory', {})
        battleFieldResHistory = historyInfo.get('battleFieldResHistory', {})
        battleFieldFlagHistory = historyInfo.get('battleFieldFlagHistory', {})
        battleFieldNewFlagHistory = historyInfo.get('battleFieldNewFlagHistory', {})
        battleFieldCqzzHistory = historyInfo.get('battleFieldCqzzHistory', {})
        battleFieldPUBGHistory = historyInfo.get('battleFieldPUBGHistory', {})
        if battleFieldFortHistory:
            for key, item in battleFieldFortHistory.iteritems():
                self.bfHistoryInfo['battleFieldFortHistory'][key] = item

        if battleFieldResHistory:
            for key, item in battleFieldResHistory.iteritems():
                self.bfHistoryInfo['battleFieldResHistory'][key] = item

        if battleFieldFlagHistory:
            for key, item in battleFieldFlagHistory.iteritems():
                self.bfHistoryInfo['battleFieldFlagHistory'][key] = item

        if battleFieldNewFlagHistory:
            for key, item in battleFieldNewFlagHistory.iteritems():
                self.bfHistoryInfo['battleFieldNewFlagHistory'][key] = item

        if battleFieldCqzzHistory:
            for key, item in battleFieldCqzzHistory.iteritems():
                self.bfHistoryInfo['battleFieldCqzzHistory'][key] = item

        if battleFieldPUBGHistory:
            for key, item in battleFieldPUBGHistory.iteritems():
                self.bfHistoryInfo['battleFieldPUBGHistory'][key] = item

        self.bfHistoryVers[0] = self.bfHistoryInfo.get('battleFieldFlagHistory', {}).get('version', 0)
        self.bfHistoryVers[1] = self.bfHistoryInfo.get('battleFieldResHistory', {}).get('version', 0)
        self.bfHistoryVers[2] = self.bfHistoryInfo.get('battleFieldFortHistory', {}).get('version', 0)
        self.bfHistoryVers[3] = self.bfHistoryInfo.get('battleFieldNewFlagHistory', {}).get('version', 0)
        self.bfHistoryVers[4] = self.bfHistoryInfo.get('battleFieldCqzzHistory', {}).get('version', 0)
        self.bfHistoryVers[5] = self.bfHistoryInfo.get('battleFieldPUBGHistory', {}).get('version', 0)
        if qType == const.BATTLE_FIELD_HISTORY_SHENGYA:
            if gameglobal.rds.ui.battleFieldHistory.isNeedShow:
                gameglobal.rds.ui.battleFieldHistory.show()
        elif qType == const.BATTLE_FIELD_HISTORY_LEIDA:
            if gameglobal.rds.ui.pvpBattleFieldV2.widget:
                gameglobal.rds.ui.pvpBattleFieldV2.initData()

    def showIgnoreDotaCalc(self):
        text = GMD.data.get(GMDD.data.IGNORE_DOTA_CALC, {}).get('text', '')
        return gameglobal.rds.ui.messageBox.showMsgBox(text, self.cell.quitBattleField, yesBtnText='离开战场')

    def battleFieldResultNotify(self, result, resultInfo):
        gamelog.debug('@zhangkuo battleFieldResultNotify ', result, resultInfo)
        gamelog.debug('@hjx bf#battleFieldResultNotify:', result, resultInfo)
        if self.isInBfDota() and resultInfo.get('ignoreDotaCalc', False):
            gamelog.info('jbx:ignoreDotaCalc')
            self.ignoreDotaCalcIdMsgBox = self.showIgnoreDotaCalc()
            return
        self.bfResult = result
        self.bfResultInfo = resultInfo
        self.isShowEnd = True
        msg = ''
        if result == const.LOSE:
            msg = '很遗憾你在本场战场中失利了！'
            if self.isInBfDota():
                gameglobal.rds.sound.playSound(5699)
        elif result == const.TIE:
            msg = '平分秋色，本场战场以平局结束！'
        elif result == const.WIN:
            msg = '恭喜你获得本场战场的胜利！'
            if self.isInBfDota():
                gameglobal.rds.sound.playSound(5698)
        fbNo = formula.getFubenNo(self.spaceNo)
        if not formula.isGuildTournament(fbNo):
            self.chatToEventEx(msg, const.CHANNEL_COLOR_RED)
        self._genTitleDesc()
        self.callArenaMsg('showGameOver', (result,))
        mode = formula.fbNo2BattleFieldMode(fbNo)
        delayShowInterval = BFMD.data.get(mode, {}).get('delayShowInterval', 6)
        BigWorld.callback(delayShowInterval, Functor(self.showBattleFieldResult))
        self.getBfMemPerforms()
        self.bfEnd = True

    def getBfMemPerforms(self):
        if not self.bfEnd:
            gbIdList, bfFrequentVerList, bfStableVerList = self.resetBfMemFromTeamInfo()
            try:
                self.cell.queryBattleFieldDetails(gbIdList, bfFrequentVerList, bfStableVerList)
            except:
                msg = 'getBfMemPerforms %s %s %s' % (str(gbIdList), str(bfFrequentVerList), str(bfStableVerList))
                BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})

    def queryAllGtBattleFieldDetails(self, groupId):
        gbIdList, bfFrequentVerList, bfStableVerList = self.getBFDetailVers()
        try:
            self.cell.queryAllGtBattleFieldDetails(gbIdList, bfFrequentVerList, bfStableVerList, groupId)
        except:
            msg = 'queryAllGtBattleFieldDetails %s %s %s %d' % (str(gbIdList),
             str(bfFrequentVerList),
             str(bfStableVerList),
             groupId)
            BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})

    def getBFDetailVers(self):
        gbIdList = []
        bfFrequentVerList = []
        bfStableVerList = []
        for memPerform in self.bfMemPerforms:
            gbIdList.append(memPerform.get('gbId', 0))
            bfFrequentVerList.append(memPerform.get('frequentVer', 0))
            bfStableVerList.append(memPerform.get('stableVer', 0))

        return (gbIdList, bfFrequentVerList, bfStableVerList)

    def delayShowDotaDetail(self):
        if not formula.inDotaBattleField(self.mapID):
            return
        gameglobal.rds.ui.bfDotaDetail.show()

    def delayShowSocreInfo(self):
        if not formula.inHuntBattleField(BigWorld.player().mapID):
            return
        if gameglobal.rds.ui.scoreInfo.widget:
            gameglobal.rds.ui.scoreInfo.refreshFrame()
        else:
            gameglobal.rds.ui.scoreInfo.show()

    def battleFieldFirstBloodNotify(self, killer, killee):
        if formula.inDotaBattleField(self.mapID):
            return
        self.showGameMsg(GMDD.data.BATTLE_FIELD_FIRST_BLOOD, (killer, killee))
        self.notifyBattleFieldStatsInfo(const.BATTLE_FIELD_STATS_TYPE_FIRST_BLOOD, (killer, killee))

    def battleFieldKillAvatar(self, killerGbId, killeeGbId):
        killerZaijuId = self.bfDotaZaijuRecord.get(killerGbId, 0)
        killeeZaijuId = self.bfDotaZaijuRecord.get(killeeGbId, 0)
        soundId = ZD.data.get(killerZaijuId, {}).get('deathBroadCast', {}).get(killeeZaijuId, 0)
        if soundId:
            gameglobal.rds.sound.playSound(soundId)
        gamelog.debug('@hjx dota#battleFieldKillAvatar:', killerGbId, killeeGbId)

    def showGetFameFailedMsg(self):
        if not self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return
        if self.inFubenType(const.FB_TYPE_BATTLE_FIELD_NEW_FLAG):
            return
        if hasattr(self, 'bfResultInfo') and not self.bfResultInfo.get('canGetFame', True):
            msg = GMD.data.get(GMDD.data.BATTLE_FIELD_GET_FAME_FAILED_NOTIFY, {}).get('text', '')
            self.bfMsgBoxId = gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def closeGetFameFailedMsg(self):
        if hasattr(self, 'bfMsgBoxId') and self.bfMsgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.bfMsgBoxId)
            self.bfMsgBoxId = 0

    def showBattleFieldResult(self):
        if self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            if self.inFubenType(const.FB_TYPE_BATTLE_FIELD_HOOK):
                pass
            elif self.inFubenType(const.FB_TYPE_BATTLE_FIELD_RACE):
                pass
            elif self.inFubenType(const.FB_TYPE_BATTLE_FIELD_HUNT):
                gameglobal.rds.ui.scoreInfo.show()
            elif self.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA):
                gameglobal.rds.ui.bfDotaDetail.hide()
                voteResult = self.bfResultInfo.get('voteResult', {})
                gameglobal.rds.ui.bfDotaFinalDetail.voteResult = voteResult
                gameglobal.rds.ui.bfDotaFinalDetail.show()
            elif self.isInPUBG():
                pass
            else:
                self._genTitleDesc()
                gameglobal.rds.ui.battleField.showBFFinalResultWidget()

    def _getFlagStats(self, mGbId):
        if not self.inFubenType(const.FB_TYPE_BATTLE_FIELD_FLAG):
            return {}
        memberFlagStats = self.bfResultInfo.get('memberFlagStats', {})
        return memberFlagStats.get(mGbId, {})

    def _calcBFScore(self):
        for index, value in enumerate(self.bfMemPerforms):
            self.bfMemPerforms[index]['titleNum'] = sum(value.get('titleDesc', []))

    def _calcFirstBloodKillerTitle(self):
        BATTLE_FIELD_TITLE_DESC_NUM_LIMIT = SCD.data.get('BATTLE_FIELD_TITLE_DESC_NUM_LIMIT', 6)
        for memStats in self.bfMemPerforms:
            if not memStats.has_key('titleDesc'):
                memStats['titleDesc'] = [ 0 for i in xrange(BATTLE_FIELD_TITLE_DESC_NUM_LIMIT) ]
            if memStats['gbId'] == self.firstBloodKiller:
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_FIRST_BLOOD] = 1

    def _genTitleDesc(self):
        if BigWorld.player().isInPUBG():
            return
        if len(self.bfResultInfo) == 0:
            return
        if not self.bfMemPerforms:
            return
        BATTLE_FIELD_TITLE_DESC_NUM_LIMIT = SCD.data.get('BATTLE_FIELD_TITLE_DESC_NUM_LIMIT', 6)
        for memStats in self.bfMemPerforms:
            if not memStats.has_key('titleDesc'):
                memStats['titleDesc'] = [ 0 for i in xrange(BATTLE_FIELD_TITLE_DESC_NUM_LIMIT) ]
            if memStats['gbId'] == getattr(self, 'firstBloodKiller', 0):
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_FIRST_BLOOD] = 1
            else:
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_FIRST_BLOOD] = 0
            for gbId, mvpItem in self.bfResultInfo.get('mvps', []).iteritems():
                if gbId == memStats.get('gbId', 0):
                    memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_MVP] = 1

            if len(self.bfMemPerforms) < 2:
                continue
            memInfo = self.getMemInfoByGbId(memStats['gbId'])
            if self.isBfTop(const.BF_COMMON_CURE, memStats):
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_CURE] = 1
            else:
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_CURE] = 0
            if self.isBfTop(const.BF_COMMON_DAMAGE, memStats):
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_DAMAGE] = 1
            else:
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_DAMAGE] = 0
            if self.isBfTop(const.BF_COMMON_BE_DAMAGE, memStats):
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_BE_DAMAGE] = 1
            else:
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_BE_DAMAGE] = 0
            if self.isBfTop(const.BF_COMMON_JIBAI_DONATE, memStats):
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_JI_BAI] = 1
            else:
                memStats['titleDesc'][const.BATTLE_FIELD_TITLE_INDEX_JI_BAI] = 0

        self._calcBFScore()

    def isBfTop(self, key, memInfo):
        isTop = True
        if memInfo.get(key, 0) == 0:
            return False
        for mem in self.bfMemPerforms:
            if mem.get('gbId', 0) and mem.get('gbId', 0) != memInfo.get('gbId', 0):
                if mem.get(key, 0) > memInfo.get(key, 0):
                    isTop = False

        return isTop

    def getMemInfoByGbId(self, gbId):
        if not self.battleFieldTeam.has_key(gbId):
            return {}
        return self.battleFieldTeam[gbId]

    def getMemStatsByGbId(self, gbId):
        memStats = {}
        for item in self.bfMemStats:
            if item['gbId'] == gbId:
                memStats = item
                break

        return memStats

    def getBfResult(self):
        if hasattr(self, 'bfResult'):
            return self.bfResult
        else:
            return const.WIN

    def getMySideKillNum(self):
        if hasattr(self, 'bfSideStats') and hasattr(self, 'bfSideIndex'):
            return self.bfSideStats[self.bfSideIndex]['killNum']
        else:
            return 12

    def getMySideDeathNum(self):
        if hasattr(self, 'bfSideStats') and hasattr(self, 'bfSideIndex'):
            return self.bfSideStats[self.bfSideIndex]['deathNum']
        else:
            return 34

    def getMySideAssistNum(self):
        if hasattr(self, 'bfSideStats') and hasattr(self, 'bfSideIndex'):
            return self.bfSideStats[self.bfSideIndex]['assistNum']
        else:
            return 14

    def getOtherSideKillNum(self):
        if hasattr(self, 'bfSideStats') and hasattr(self, 'bfSideIndex'):
            return self.bfSideStats[1 - self.bfSideIndex]['killNum']
        else:
            return 15

    def getOtherSideDeathNum(self):
        if hasattr(self, 'bfSideStats') and hasattr(self, 'bfSideIndex'):
            return self.bfSideStats[1 - self.bfSideIndex]['deathNum']
        else:
            return 18

    def getOtherSideAssistNum(self):
        if hasattr(self, 'bfSideStats') and hasattr(self, 'bfSideIndex'):
            return self.bfSideStats[1 - self.bfSideIndex]['assistNum']
        else:
            return 19

    def battleFieldApplySucc(self, fbNo):
        gamelog.debug('@hjx bf#battleFieldApplySucc:', self.id, fbNo)
        self.showGameMsg(GMDD.data.BATTLE_FIELD_APPLY_SUCC, ())
        self.battleFieldFbNo = fbNo
        gameglobal.rds.ui.duelMatchTime.addMatchTimeItem(fbNo)
        gameglobal.rds.ui.battleField.refreshBFPanel(uiConst.BF_PANEL_STAGE_APPLYED)
        self.battleFieldStage = uiConst.BF_PANEL_STAGE_APPLYED
        gameglobal.rds.ui.pvPPanel.pvpPanelRefreshBF()

    def battleFieldUpRegionSucc(self, fbNo, regionId):
        pass

    def onSuccJumpQueue(self, fbNo, sideNUID, res, isJumpWeakSide):
        self.isJumpQueue = True
        self.bfSideNUID = sideNUID
        self.bfRes = res
        self.bfIsJumpWeakSide = isJumpWeakSide
        gameglobal.rds.ui.battleField.tipsTimeStamp = self.getServerTime()
        gameglobal.rds.ui.battleField.isJumpQueue = True
        gameglobal.rds.ui.battleField.refreshBattleFieldTip(uiConst.BF_JUMP_QUEUE_TIP, confrimTimeOut=True)
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_BF_MATCHED)

    def confirmJumpQueue(self):
        bfAwardResBase = DCD.data.get('bfAwardResBase')
        if bfAwardResBase is None:
            return
        fbNo = self.getBattleFieldFbNo()
        fbType = formula.whatFubenType(fbNo)
        if fbType == const.FB_TYPE_BATTLE_FIELD_DOTA:
            msg = uiUtils.getTextFromGMD(GMDD.data.BATTLE_FIELD_DOTA_JUMP_QUEUE_NOTIFY)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self._doConfirmJumpQueue)
        elif self.bfIsJumpWeakSide:
            msg = uiUtils.getTextFromGMD(GMDD.data.BATTLE_FIELD_JUMP_WEAK_NOTIFY)
            bfExtraZhanXun = DCD.data.get('bfExtraZhanXun', 0)
            msg = msg % (bfExtraZhanXun,)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self._doConfirmJumpQueue)
        else:
            self._doConfirmJumpQueue()

    def _doConfirmJumpQueue(self):
        fbNo = self.getBattleFieldFbNo()
        if fbNo is None:
            return
        self.cell.confirmJumpQueue(fbNo)

    def cancelJumpQueue(self):
        fbNo = self.getBattleFieldFbNo()
        if fbNo is None:
            return
        self.cell.cancelJumpQueue(fbNo)

    def showBattleFieldConfirmMsg(self, fbNo):
        if self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return
        gameglobal.rds.ui.battleField.tipsTimeStamp = self.getServerTime()
        gameglobal.rds.ui.battleField.refreshBattleFieldTip(uiConst.BF_ENTER_TIP, confrimTimeOut=True)
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_BF_MATCHED)
        gameglobal.rds.ui.battleField.refreshBFPanel(uiConst.BF_PANEL_STAGE_MATCHED)
        self.battleFieldStage = uiConst.BF_PANEL_STAGE_MATCHED
        gameglobal.rds.ui.pvPPanel.pvpPanelRefreshBF()
        self.battleFieldFbNo = fbNo
        uiUtils.showWindowEffect()

    def onConfirmEnterBattleField(self):
        gamelog.debug('jorsef: onConfirmEnterBattleField')
        gameglobal.rds.ui.battleField.refreshBattleFieldTip(uiConst.BF_ENTER_WAITING_TIP)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_BF_MATCHED)

    def getBattleFieldFbNo(self):
        if self.battleFieldFbNo != 0:
            return self.battleFieldFbNo
        enableCrossServerBF = gameglobal.rds.configData.get('enableCrossServerBF', False)
        fbNo = formula.genBattleFieldFbNoByLv(self.lv, gameglobal.rds.ui.battleField.selFbMode, enableCrossServerBF)
        if fbNo:
            return fbNo
        gamelog.info('@hjx getBattleFieldFbNo:', self.lv)

    def getBattleFieldMode(self):
        return const.BATTLE_FIELD_MODE_RES

    def _bfConditionCheck(self):
        minLv, maxLv = formula.getBattleFieldLvReq(gameglobal.rds.ui.battleField.selFbMode)
        if not utils.canEnterPvP():
            return False
        if self.lv < minLv or self.lv > maxLv:
            gamelog.debug('@hjx bf#applyBattleField failed:', self.lv, minLv, maxLv)
            self.showGameMsg(GMDD.data.BATTLE_FIELD_APPLY_FAILED_LV, (minLv, maxLv))
            return False
        return True

    def applyBattleFieldDuplicate(self):
        flag = gameglobal.rds.ui.pvPPanel.getGroupHeaderCandidateFlag()
        self.cell.applyBattleField(self.getBattleFieldFbNo(), flag, False)

    def applyBattleFieldOfPerson(self):
        if not self._bfConditionCheck():
            return
        if self.isInTeamOrGroup():
            self.showGameMsg(GMDD.data.APPLY_FAILED_IN_GROUP, ())
            return
        flag = gameglobal.rds.ui.pvPPanel.getGroupHeaderCandidateFlag()
        self.cell.applyBattleField(self.getBattleFieldFbNo(), flag, False)

    def applyBattleFieldOfTeam(self, numType):
        if not self._bfConditionCheck():
            return
        if not self.isInTeamOrGroup():
            self.showGameMsg(GMDD.data.DUEL_APPLY_FAILED_NOT_IN_GROUP, ())
            return
        if self.groupHeader != self.id:
            self.showGameMsg(GMDD.data.DUEL_APPLY_FAILED_NOT_HEADER, ())
            return
        flag = gameglobal.rds.ui.pvPPanel.getGroupHeaderCandidateFlag()
        self.cell.applyBattleFieldOfTeam(self.getBattleFieldFbNo(), numType, flag, False)

    def abortBattleField(self):
        self.cell.abortBattleField(self.battleFieldFbNo)

    def cancelApplyBattleField(self):
        self.cell.cancelApplyBattleField(self.battleFieldFbNo)

    def quitWaitingBattleField(self, fbNo):
        self.battleFieldFbNo = 0
        gameglobal.rds.ui.duelMatchTime.removeMatchTimeItem(fbNo)
        gameglobal.rds.ui.battleField.refreshBFPanel(uiConst.BF_PANEL_STAGE_INIT)
        gameglobal.rds.ui.battleField.closeTips()
        self.battleFieldStage = uiConst.BF_PANEL_STAGE_INIT
        gameglobal.rds.ui.pvPPanel.pvpPanelRefreshBF()

    def battleFieldConfirmRelive(self):
        self.cell.battleFieldConfirmRelive()

    def onStartBattleFieldRelive(self, interval):
        gameglobal.rds.ui.player.onStartBattleFieldRelive(interval)

    def onAvatarDieNotify(self, mGbId, reliveTime):
        self.reliveTimeRecord[mGbId] = utils.getNow() + reliveTime + uiUtils.getReliveCountDownTime()
        gamelog.debug('@hjx onAvatarDieNotify:', mGbId, reliveTime)

    def onReliveInBattleFieldBySYS(self, tRelive):
        self.bfTimeRec['tRelive'] = tRelive

    def onBattleFieldRelive(self):
        gameglobal.rds.ui.deadAndRelive.hide()
        if gameglobal.rds.ui.fbDeadData.mediator:
            gameglobal.rds.ui.fbDeadData.hide()
        if gameglobal.rds.ui.fbDeadDetailData.mediator:
            gameglobal.rds.ui.fbDeadDetailData.hide()

    def getMyRes(self):
        winResLimit = BFD.data.get(self.getBattleFieldFbNo(), {}).get('winResLimit', 100)
        if hasattr(self, 'bfRes') and hasattr(self, 'bfSideNUID') and self.bfRes.has_key(self.bfSideNUID):
            myRes = self.bfRes.get(self.bfSideNUID, 0)
            if myRes >= winResLimit:
                return winResLimit
            return myRes
        else:
            return 0

    def getEnemyRes(self):
        winResLimit = BFD.data.get(self.getBattleFieldFbNo(), {}).get('winResLimit', 100)
        if hasattr(self, 'bfRes') and hasattr(self, 'bfSideNUID') and self.bfRes.has_key(self.bfSideNUID):
            bfSideIndex = self.bfRes.keys().index(self.bfSideNUID)
            enemySideIndex = 1 - bfSideIndex
            enemyRes = self.bfRes.values()[enemySideIndex]
            if enemyRes >= winResLimit:
                return winResLimit
            return enemyRes
        else:
            return 0

    def getMyBullet(self):
        if not hasattr(self, 'bfBulletInfo') or not hasattr(self, 'bfSideNUID'):
            return 0
        else:
            return self.bfBulletInfo.get(self.bfSideNUID, 0)

    def getEnemyBullet(self):
        if not hasattr(self, 'bfBulletInfo') or not hasattr(self, 'bfSideNUID'):
            return 0
        elif len(self.bfBulletInfo) < 2:
            return 0
        else:
            bfSideIndex = self.bfBulletInfo.keys().index(self.bfSideNUID)
            enemySideIndex = 1 - bfSideIndex
            return self.bfBulletInfo.values()[enemySideIndex]

    def getMyScore(self, fbNo = 0):
        if not fbNo:
            fbNo = self.getBattleFieldFbNo()
        bfData = BFD.data.get(fbNo, {})
        planeTotalCnt = bfData.get('planeTotalCnt', 5)
        planeConsumeScore = bfData.get('planeConsumeScore', 100)
        maxScore = planeTotalCnt * planeConsumeScore
        if hasattr(self, 'bfScore') and hasattr(self, 'bfSideNUID') and self.bfScore.has_key(self.bfSideNUID):
            myScore = self.bfScore.get(self.bfSideNUID, 0)
            if myScore >= maxScore:
                return maxScore
            return myScore
        else:
            return 0

    def getEnemyScore(self, fbNo = 0):
        if not fbNo:
            fbNo = self.getBattleFieldFbNo()
        bfData = BFD.data.get(fbNo, {})
        planeTotalCnt = bfData.get('planeTotalCnt', 5)
        planeConsumeScore = bfData.get('planeConsumeScore', 100)
        maxScore = planeTotalCnt * planeConsumeScore
        if hasattr(self, 'bfScore') and hasattr(self, 'bfSideNUID') and self.bfScore.has_key(self.bfSideNUID):
            bfSideIndex = self.bfScore.keys().index(self.bfSideNUID)
            enemySideIndex = 1 - bfSideIndex
            enemyScore = self.bfScore.values()[enemySideIndex]
            if enemyScore >= maxScore:
                return maxScore
            return enemyScore
        else:
            return 0

    def onBattleFieldLoaded(self, fbNo):
        p = BigWorld.player()
        if self.isNeedRefreshCounting:
            self.isNeedRefreshCounting = False
            gameglobal.rds.ui.battleField.startCounting()
        if self.bfGroupNeedOpen:
            self.bfGroupNeedOpen = False
            gameglobal.rds.ui.group.showGroupTeam()
            if self.bfSideNUID:
                ccControl.joinTeam(str(self.bfSideNUID), const.CC_GROUP_TYPE_ZHANCHANG)
        bfFirstEnter = getattr(self, 'bfFirstEnter', True)
        if bfFirstEnter:
            self.bfFirstEnter = False
            if formula.inHuntBattleField(self.mapID):
                if not p.bianshen[1]:
                    gameglobal.rds.ui.vehicleChoose.show()
                gameglobal.rds.ui.littleScoreInfo.show()
            if formula.inDotaBattleField(self.mapID):
                if not self.bianshen[1] and not getattr(self, 'isInBfDotaChooseHero', False) and not getattr(self, 'backToBfEnd', False):
                    self.showBfDotaChooseHero()
                if getattr(self, 'isInBfDotaChooseHero', False):
                    gameglobal.rds.sound.playBossMusic(741, True)
                self.setOtherWidgetVisible(False)
                gameglobal.rds.ui.dispatchEvent(events.EVENT_PLAYER_SPACE_NO_CHANGED, 0)
            gameglobal.rds.tutorial.onEnterFuben(fbNo)
        if p.isPUBGFbNo(fbNo):
            p.onPUBGLoaded(fbNo)

    def startSoliloquizeTimer(self):
        if not getattr(self, 'soliloquizeTimer', None):
            nextTime = self.getNextSoliloquizeTime()
            if not nextTime:
                return
            self.soliloquizeTimer = BigWorld.callback(nextTime, self.updateSoliloquizeTimer)

    def getNextSoliloquizeTime(self):
        min, max = DCD.data.get('soliloquizeTimeRange', (5, 10))
        if not min + max:
            return 99999999999L
        return random.randint(min, max)

    def getSoliloquizeVoiceId(self):
        zaiJuId = self.bianshen[1]
        if not zaiJuId:
            return 0
        voices = ZD.data.get(zaiJuId, {}).get('soliloquizeVoices', ())
        if not voices:
            return 0
        voiceId = random.choice(voices)
        return voiceId

    def getInteractiveVoice(self):
        zaiJuId = self.bianshen[1]
        voicesList = []
        if not zaiJuId:
            return 0
        for id in self.selfSideDotaEntityIdSet:
            entity = BigWorld.entities.get(id, None)
            if entity and distance3D(self.position, entity.position) < 30.0:
                interactiveZaiJuId = entity.bianshen[1]
                voices = ZD.data.get(zaiJuId, {}).get('interactiveVoices', {}).get(interactiveZaiJuId, ())
                if voices:
                    voicesList.extend(voices)

        if not len(voicesList):
            return 0
        return random.choice(voicesList)

    def updateSoliloquizeTimer(self):
        if not gameglobal.rds.configData.get('enableDotaBf', False):
            return
        if not formula.inDotaBattleField(getattr(self, 'mapID', 0)):
            self.endSoliloquizeTimer()
            return
        voiceList = []
        soliloquizeVoiceId = self.getSoliloquizeVoiceId()
        if soliloquizeVoiceId:
            voiceList.append(soliloquizeVoiceId)
        interactiveVoiceId = self.getInteractiveVoice()
        if interactiveVoiceId:
            voiceList.append(interactiveVoiceId)
        if not voiceList:
            self.endSoliloquizeTimer()
            return
        if voiceList and self.life != gametypes.LIFE_DEAD:
            soundId = random.choice(voiceList)
            gameglobal.rds.sound.playSound(soundId, position=self.position)
        nextTime = self.getNextSoliloquizeTime()
        if not nextTime:
            self.endSoliloquizeTimer()
            return
        self.soliloquizeTimer = BigWorld.callback(nextTime, self.updateSoliloquizeTimer)

    def endSoliloquizeTimer(self):
        if getattr(self, 'soliloquizeTimer', None):
            BigWorld.cancelCallback(self.soliloquizeTimer)
        self.soliloquizeTimer = None

    def onAvatarEnterDotaZaiju(self):
        if gameglobal.rds.ui.camera.isShow:
            gameglobal.rds.ui.camera.clearWidget()
        if gameglobal.rds.ui.cameraV2.isShow:
            gameglobal.rds.ui.cameraV2.clearWidget()
        if not getattr(self, 'backToBfEnd', False):
            delayTime = DCD.data.get('soliloquizeDelayTime', 10)
            BigWorld.callback(delayTime, self.startSoliloquizeTimer)
        self.hideBfDotaChooseHero()
        BigWorld.callback(3, self.delayPlayTempCampSound)
        gameglobal.rds.ui.bfDotaKill.show()
        gameglobal.rds.ui.bfDotaVote.show()
        if not gameglobal.rds.ui.bfDotaItemAndProp.widget:
            gameglobal.rds.ui.bfDotaItemAndProp.show()
        if not gameglobal.rds.ui.bfDotaSimple.widget:
            gameglobal.rds.ui.bfDotaSimple.show()
        shopId = DCD.data.get('BF_DOTA_COMPOSITE_SHOP_ID', 0)
        self.base.openPrivateShop(0, shopId)
        self.autoSkill.resetDotaZaijuAutoSkill(self.bianshen[1])
        gameglobal.rds.ui.littleMap.onPlayerEnterDotaZaiju()
        self.topLogo.initDotaBlood()
        self.base.queryBFDotaFavorEquip(self.bianshen[1])
        for gbId, fecthId in self.preloadDotaZaijuFetchs.iteritems():
            fecthId and BigWorld.cancelBgTask(fecthId)

        self.preloadDotaZaijuFetchs = {}
        if gameglobal.rds.configData.get('enableBfDotaMapMark', False):
            gameglobal.rds.ui.littleMap.showBfDotaBtns(300, 20)
            gameglobal.rds.ui.bfDotaSignal.show()

    def delayPlayTempCampSound(self):
        if self.tempCamp == const.BF_DOTA_TEMP_CAMP_BLUE:
            gameglobal.rds.sound.playSound(742)
        else:
            gameglobal.rds.sound.playSound(743)

    @property
    def isChooseHeroLoadedCompletd(self):
        if gameglobal.rds.ui.bfDotaChooseHeroLeft.widget and gameglobal.rds.ui.bfDotaChooseHeroBottom.widget and gameglobal.rds.ui.bfDotaChooseHeroRight.widget and gameglobal.rds.ui.bfDotaChooseHeroBottom.showEntity and getattr(gameglobal.rds.ui.bfDotaChooseHeroBottom.showEntity, 'firstFetchFinished', False):
            return True
        return False

    def onEnterDotaBf(self):
        gameglobal.rds.ui.littleMap.changeToBfDotaMode(True)
        self.selfSideDotaEntityIdSet = set()
        self.bfDotaOtherEquipInfo = {}
        self.oldEquipVersion = 0
        self.bfDotaLvRecord = {}
        self.holdPreloadDotaZaijuModel = {}
        self.backToBfEnd = False
        self.reliveTimeRecord = {}
        self.bfOwnStas = {}
        self.bfDotaSkillInitRecord = {}
        self.bfDotaEntityIdRecord.setdefault(const.DOTA_ENTITY_TYPE_LITTLE_MAP, set()).add(self.id)
        self.visibleBfDotaEnemyIdSet = set()
        if clientcom.bfDotaAoIInfinity():
            self.addBfDotaTimer()
        gameglobal.rds.ui.bfDotaDetail.hide()
        BigWorld.setFloraMaxDrawingDist(500)
        BigWorld.setFloraDensity(1.0)
        uiUtils.setAvatarPhysics(self.getSavedOperationMode(), forceChagne=True)
        gameglobal.rds.ui.topBar.setMpaNameTxtVisible(False)
        keyboardEffect.removeEffectsEnterBfDota()

    def onLeaveDotaBf(self):
        gameglobal.rds.ui.littleMap.changeToBfDotaMode(False)
        self.selfSideDotaEntityIdSet = set()
        self.bfDotaOtherEquipInfo = {}
        self.oldEquipVersion = 0
        self.bfDotaLvRecord = {}
        self.holdPreloadDotaZaijuModel = {}
        self.preloadDotaZaijuFetchs = {}
        self.reliveTimeRecord = {}
        self.battleFieldBag.clear()
        self.bfOwnStas = {}
        self.availableTalenSkillIds = []
        self.bfDotaSkillInitRecord = {}
        self.bfDotaEntityIdRecord = {}
        self.visibleBfDotaEnemyIdSet = set()
        gameglobal.rds.ui.littleMap.oldHpInfo = {}
        gameglobal.rds.ui.bfDotaSimple.hide()
        gameglobal.rds.ui.bfDotaDetail.hide()
        gameglobal.rds.ui.bfDotaItemAndProp.hide()
        gameglobal.rds.ui.zaijuV2.hide()
        gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_SKILL_TGT)
        gameglobal.rds.ui.bfDotaShop.hide()
        gameglobal.rds.ui.bfDotaKill.hide()
        gameglobal.rds.ui.bfDotaFinalDetail.hide()
        gameglobal.rds.ui.bfDotaShopPush.hide()
        gameglobal.rds.ui.bfDotaVote.hide()
        self.hideBfDotaChooseHero()
        self.topLogo.removeDotaBlood()
        self.circleEffect.delSkillRangeCircleModel()
        gameglobal.PLANE_MODEL = None
        gameglobal.PLANE_MODEL_PARENT_NODE = None
        if appSetting.VideoQualitySettingObj.oldFloraMaxDrawingDist:
            BigWorld.setFloraMaxDrawingDist(appSetting.VideoQualitySettingObj.oldFloraMaxDrawingDist)
        if appSetting.VideoQualitySettingObj.oldFloraDensity:
            BigWorld.setFloraDensity(appSetting.VideoQualitySettingObj.oldFloraDensity)
        self.optionalTargetLocked = None
        uiUtils.setAvatarPhysics(self.getSavedOperationMode(), forceChagne=True)
        gameglobal.rds.ui.littleMap.resetPlayerIcon()
        popItemList = []
        for itemId, _ in logicInfo.cooldownItem.iteritems():
            if Item.isDotaBattleFieldItem(itemId):
                popItemList.append(itemId)

        for itemId in popItemList:
            logicInfo.cooldownItem.pop(itemId, None)

        self.topLogo.showBlood(False)
        gameglobal.rds.ui.littleMap.hideBfDotaBtns()
        gameglobal.rds.ui.bfDotaSignal.hide()
        keyboardEffect.addEffectsLeaveBfData()
        self.delBfDotaTimer()
        if getattr(self, 'ignoreDotaCalcIdMsgBox', 0):
            gameglobal.rds.ui.messageBox.dismiss(self.ignoreDotaCalcIdMsgBox)
            self.ignoreDotaCalcIdMsgBox = 0
        gameglobal.rds.ui.topBar.setMpaNameTxtVisible(False)

    def setOtherWidgetVisible(self, visible):
        if gameglobal.rds.ui.actionbar.mc:
            gameglobal.rds.ui.actionbar.mc.Invoke('setVisible', GfxValue(visible))
        if gameglobal.rds.ui.actionbar.wsMc:
            gameglobal.rds.ui.actionbar.wsMc.Invoke('setVisible', GfxValue(visible))
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ACTION_BARS, visible)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WUSHUANG_BARS, visible)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ITEMBAR, visible)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ITEMBAR2, visible)
        gameglobal.rds.ui.bullet.setVisible(visible)
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.SetVisible(visible)
        if visible:
            gameglobal.rds.ui.actionbar.setSchoolCenter()

    def showBfDotaChooseHero(self):
        if getattr(self, 'isInBfDotaChooseHero', False):
            return
        self.filterChooseHeroSound = True
        self.isInBfDotaChooseHero = True
        x = round(self.position[0])
        y = round(self.position[2])
        yaw = self.yaw
        gameglobal.rds.ui.littleMap.setPlayerPos(x, y, yaw)
        BigWorld.simpleShaderDistance(gameglobal.HUGE_SIMPLE_SHADER_DISTANCE)
        ccControl.closeCC()
        BigWorld.callback(2, self.doShowBfDotaChooseHero)

    def doShowBfDotaChooseHero(self):
        gameglobal.rds.ui.bfDotaChooseHeroLeft.show()
        gameglobal.rds.ui.bfDotaChooseHeroBottom.show()
        gameglobal.rds.ui.bfDotaChooseHeroRight.show()
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_BUFF_NOTICE, False)

    def hideBfDotaChooseHero(self):
        if not self.isInBfDotaChooseHero:
            return
        Sound.stopStateMusic()
        BigWorld.simpleShaderDistance(gameglobal.NORMAL_SIMPLE_SHADER_DISTANCE)
        self.isInBfDotaChooseHero = False
        gameglobal.rds.ui.bfDotaChooseHeroLeft.hide()
        gameglobal.rds.ui.bfDotaChooseHeroBottom.hide()
        gameglobal.rds.ui.bfDotaChooseHeroRight.hide()
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_BUFF_NOTICE, True)

    def enterBFBefore(self):
        self.enemyMaxRes = self.myMaxRes = BFD.data.get(self.getBattleFieldFbNo(), {}).get('winResLimit', 100)
        gameglobal.rds.ui.duelMatchTime.resetDuelMatch()
        gameglobal.rds.ui.teamComm.closeTeamPlayer()
        gameglobal.rds.ui.battleField.refreshBFStats()
        gameglobal.rds.ui.teamComm.refreshMemberInfo()
        gameglobal.rds.ui.battleField.stage = uiConst.BF_PANEL_STAGE_IN_GAME
        self.battleFieldStage = uiConst.BF_PANEL_STAGE_IN_GAME
        gameglobal.rds.ui.battleField.closeTips()
        self._refreshMemberBuffState(1)
        filterWidgets = [uiConst.WIDGET_TEAM_INVITE_V2,
         uiConst.WIDGET_CHAT_LOG,
         uiConst.WIDGET_BF_STATS,
         uiConst.WIDGET_BFFLAG_STATS,
         uiConst.WIDGET_BULLET,
         uiConst.WIDGET_SKILL_PUSH,
         uiConst.WIDGET_DEAD_RELIVE,
         uiConst.WIDGET_ARENA_COUNT_DOWN,
         uiConst.WIDGET_FEEDBACK_ICON,
         uiConst.WIDGET_GROUPMEMBER,
         uiConst.WIDGET_LOADING,
         uiConst.WIDGET_BATTLE_FIELD_FORT_INFO,
         uiConst.WIDGET_BF_FLAG_STATS_V1,
         uiConst.WIDGET_BF_FORT_INFO_V1,
         uiConst.WIDGET_BF_GUILD_TOURNAMENT_OBSERVE,
         uiConst.WIDGET_BATTLE_OF_FORT_PROGRESS_BAR,
         uiConst.WIDGET_BUFF_LISTENER_SHOW,
         uiConst.WIDGET_BATTLE_CQZZ_RPGRESS_BAR,
         uiConst.WIDGET_BATTLE_RACE_COUNT_DOWN]
        filterWidgets.extend(uiConst.HUD_WIDGETS)
        gameglobal.rds.ui.unLoadAllWidget(filterWidgets)
        gameglobal.rds.ui.battleField.showMonsterTimer(True)
        gameglobal.rds.ui.battleField.showTopMsg()
        gameglobal.rds.ui.map.realClose()
        gameglobal.rds.ui.chat.goToBattleField()
        self.nearEnemyPlayersInfo = {}
        self.showCancelHideInBFConfirm()
        gameglobal.rds.ui.topBar.isQuitBF = False
        self.bfTeammateInfo = {}
        self.bfEnemyInfo = {}
        self.bfDotaTalentSkillRecord = {}
        talentSkillIndexList = getattr(self, 'bfDotaTalentSkillIndexList', [0, 1])
        skill0 = utils.getTalentSkillByIndex(talentSkillIndexList[0])
        skill1 = utils.getTalentSkillByIndex(talentSkillIndexList[1])
        self.bfDotaTalentSkillRecord[self.gbId] = [skill0, skill1]
        self.isShowEnd = False

    def _isBattleFieldReady(self):
        if not hasattr(self, 'bfTimeRec'):
            return False
        elif not self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return False
        elif self.bfTimeRec.has_key('tReady') and self.bfTimeRec['tReady'] <= self.getServerTime():
            return True
        else:
            return False

    def bfGoHome(self):
        if not self._isBattleFieldReady():
            self.showGameMsg(GMDD.data.BATTLE_FIELD_GO_HOME_FAILED_NOT_START, ())
            return
        BigWorld.player().cell.onGoHome()

    def onLeaveBattleField(self, oldFbNo):
        gameglobal.rds.ui.battleField.closeBFWidget()
        self.battleFieldStage = uiConst.BF_PANEL_STAGE_INIT
        gameglobal.rds.ui.pvPPanel.pvpPanelRefreshBF()
        gameglobal.rds.ui.arena.closeArenaCountDown()
        gameglobal.rds.ui.chat.goToWorld()
        gameglobal.rds.ui.group.hide()
        self.motionUnpin()
        self._refreshMemberBuffState(1)
        gameglobal.rds.ui.battleField.showMonsterTimer(False)
        self.isNeedCounting = False
        self.bfIsGenTitle = False
        ccControl.leaveTeam(str(self.bfSideNUID), const.CC_GROUP_TYPE_ZHANCHANG)
        self.bfMemStats = []
        self.bfMemPerforms = []
        self.bfEnd = False
        self.bfSideStats = {}
        self.battleFieldTeam = {}
        self.bfTimeRec = {}
        self.bfDuelStats = {}
        self.bfSideIndex = 0
        self.bfSideNUID = 0
        self.bfRes = {}
        self.bfArrange = {}
        self.bfHeaderGbId = 0
        self.bfResultInfo = {}
        self.battleFieldFbNo = 0
        self.bfGroupNeedOpen = True
        self.bfIsJumpWeakSide = False
        self.bfFortInfo = {}
        self.bfPlaneInfo = {}
        self.bfPlanePosInfo = []
        self.bfScore = {}
        self.bfScoreList = {}
        self.bfGbIdTimerRef = {}
        self.bfBulletInfo = {}
        self.bfFirstEnter = True
        self.battleFieldBag = BattleFieldBagCommon()
        gameglobal.rds.ui.littleMap.showBfFortInfo()
        gameglobal.rds.ui.battleField.monsterInfo = {}
        gameglobal.rds.ui.vehicleSkill.hide()
        gameglobal.rds.ui.scoreInfo.hide()
        gameglobal.rds.ui.littleMap.clearBFHuntIcons()
        self.bfTeammateInfo = {}
        self.bfEnemyInfo = {}
        self.bfDotaZaijuRecord = {}
        self.bfDotaTalentSkillRecord = {}
        self.setOtherWidgetVisible(True)
        self.isJumpQueue = False
        self.isShowEnd = False
        self.cqzzFlagPosGetState = {}
        self.endSoliloquizeTimer()
        if self.isPUBGFbNo(oldFbNo):
            self.onLeavePUBG()

    def notifyEntityPosInFuben(self, entityInfo):
        gameglobal.rds.ui.littleMap.showFBEntityIcon(entityInfo)

    def notifyMonsterHpInBF(self, subGroupIds, monsterInfo):
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
            if subGroupIds:
                nuids, subGroupIds, monsterNUID = subGroupIds
                gameglobal.rds.ui.bFGuildTournamentLive.setHpInfo(monsterInfo, monsterNUID, subGroupIds)
        if not self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return
        gameglobal.rds.ui.battleField.setHpInfo(monsterInfo)
        gameglobal.rds.ui.bFScoreAward.setHpInfo(monsterInfo)
        gameglobal.rds.ui.littleMap.setHpInfo(monsterInfo)

    def resBattleFieldTeamInfo(self, result):
        if not self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return
        enemyMembers = {}
        friendMembers = {}
        for memberGbId, info in result.iteritems():
            if not self.battleFieldTeam.has_key(memberGbId):
                continue
            if self.isInBfDota():
                oldLv = self.bfDotaLvRecord.get(memberGbId, 1)
                newLv = info.get(gametypes.TEAM_SYNC_PROPERTY_LV, 1)
                newLv = 1 if newLv > DCD.data.get('BATTLE_FIELD_DOTA_MAX_LEVEL', 18) else newLv
                self.bfDotaLvRecord[memberGbId] = max(oldLv, newLv)
            if self.battleFieldTeam[memberGbId]['sideNUID'] == self.bfSideNUID:
                friendMembers[memberGbId] = info
            else:
                if clientcom.bfDotaAoIInfinity() and info.get(gametypes.TEAM_SYNC_PROPERTY_ENTID, 0) not in self.visibleBfDotaEnemyIdSet:
                    continue
                enemyMembers[memberGbId] = info

        self.onReceiveBattleFieldFriendsInfo(friendMembers)
        self.onReceiveBattleFieldEnemysInfo(enemyMembers)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_BF_TEAMINFO_CHANGE)

    def getBattleFieldCampInfo(self, players):
        if self.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA):
            if clientcom.bfDotaAoIInfinity():
                visibleEnemys = []
                for entityId in self.visibleBfDotaEnemyIdSet:
                    entity = BigWorld.entities.get(entityId, None)
                    entity and visibleEnemys.append((entity.gbId, entity.id))

                players += visibleEnemys
            else:
                players += self.enemyInRangeBFDotaInfoList
        farawayPlayers, nearPlayers = self._classfyPlayersByDist(players)
        if len(farawayPlayers):
            gbIdList = [ player[0] for player in farawayPlayers ]
            entIdList = [ player[1] for player in farawayPlayers ]
            self.cell.startGroupInfoSync()
            self.cell.getBattleFieldTeamInfo(gbIdList, entIdList)
        else:
            self.cell.stopPropertySync()
        self.nearEnemyPlayersInfo = {}
        for player in nearPlayers:
            if self.battleFieldTeam.has_key(player.gbId) and self.bfSideNUID != self.battleFieldTeam[player.gbId]['sideNUID']:
                self.nearEnemyPlayersInfo[player.gbId] = {gametypes.TEAM_SYNC_PROPERTY_ROLENAME: player.roleName,
                 gametypes.TEAM_SYNC_PROPERTY_POSITION: player.position}

        if not len(farawayPlayers):
            self.onReceiveBattleFieldEnemysInfo()

    def refreshBattleFieldCampInfo(self):
        if not self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return
        if hasattr(self, 'bfRefreshTimer') and self.bfRefreshTimer != 0:
            BigWorld.cancelCallback(self.bfRefreshTimer)
            self.bfRefreshTimer = 0
        if self.hasState(const.BATTLE_FIELD_HUNT_DETECTION_BUFF):
            others = [ (mGbId, mVal['id']) for mGbId, mVal in self.battleFieldTeam.iteritems() ]
        else:
            others = [ (mGbId, mVal['id']) for mGbId, mVal in self.battleFieldTeam.iteritems() if mVal['id'] in gameglobal.rds.ui.teamComm.memberId ]
        self.getBattleFieldCampInfo(others)
        self.bfRefreshTimer = BigWorld.callback(utils.getRefreshAvatarInfoInterval(self), self.refreshBattleFieldCampInfo)

    def onReceiveBattleFieldFriendsInfo(self, res):
        for gbId, info in res.iteritems():
            if not self.battleFieldTeam.has_key(gbId):
                return
            hp = info.get(gametypes.TEAM_SYNC_PROPERTY_HP, 0)
            mhp = info.get(gametypes.TEAM_SYNC_PROPERTY_MHP, 0)
            mp = info.get(gametypes.TEAM_SYNC_PROPERTY_MP, 0)
            mmp = info.get(gametypes.TEAM_SYNC_PROPERTY_MMP, 0)
            lv = info.get(gametypes.TEAM_SYNC_PROPERTY_LV, 0)
            spaceNo = info.get(gametypes.TEAM_SYNC_PROPERTY_SPACENO, 0)
            pos = info.get(gametypes.TEAM_SYNC_PROPERTY_POSITION, 0)
            roleName = info.get(gametypes.TEAM_SYNC_PROPERTY_ROLENAME)
            chunkName = info.get(gametypes.TEAM_SYNC_PROPERTY_CHUNKNAME)
            self.bfTeammateInfo[gbId] = info
            if self.battleFieldTeam[gbId]['sideNUID'] == self.bfSideNUID:
                memberId = self.battleFieldTeam[gbId]['id']
                for idx, mid in enumerate(gameglobal.rds.ui.teamComm.memberId):
                    if mid == memberId:
                        oldVal = gameglobal.rds.ui.teamComm.getPyHp(idx, memberId)
                        gameglobal.rds.ui.teamComm.setOldVal(idx, hp, mhp, mp, mmp, lv)
                        if oldVal != 0:
                            gameglobal.rds.ui.teamComm.setTeamHp(memberId, hp, mhp)
                            gameglobal.rds.ui.teamComm.setTeamMp(memberId, mp, mmp)

                for idx, mid in enumerate(gameglobal.rds.ui.group.memberId):
                    if mid == memberId:
                        oldVal = gameglobal.rds.ui.group.getPyHp(idx, memberId)
                        gameglobal.rds.ui.group.setOldVal(idx, hp, mhp, mp, mmp, lv)
                        if oldVal != hp:
                            gameglobal.rds.ui.group.setTeamHp(memberId, hp, mhp)
                            gameglobal.rds.ui.group.setTeamMp(memberId, mp, mmp)

                self.membersPos[gbId] = (spaceNo,
                 pos,
                 roleName,
                 chunkName,
                 memberId)

    def battleFieldHuntTrackInfo(self, positon):
        p = BigWorld.player()
        huntTrapId = getattr(p, 'huntTrapId', 0)
        gameglobal.rds.ui.littleMap.addBFHuntIcon(uiConst.ICON_TYPE_HUNT_SPRITE, huntTrapId, huntTrapId, positon, 'trap')
        func = Functor(gameglobal.rds.ui.littleMap.delBFHuntIcon, uiConst.ICON_TYPE_HUNT_SPRITE, huntTrapId, huntTrapId)
        showTime = DCD.data.get('footStepTime', 5)
        BigWorld.callback(showTime, func)
        p.huntTrapId = huntTrapId - 1

    def battleFieldHuntTrapInfo(self, pos, srcGbId, desGbId):
        p = BigWorld.player()
        bfGbIdTimerRef = getattr(self, 'bfGbIdTimerRef', {})
        self.bfGbIdTimerRef = bfGbIdTimerRef
        if bfGbIdTimerRef:
            timer = bfGbIdTimerRef.get((srcGbId, desGbId), 0)
            if timer:
                BigWorld.cancelCallback(timer)
                bfGbIdTimerRef[srcGbId, desGbId] = 0
        gameglobal.rds.ui.littleMap.addBFHuntIcon(uiConst.ICON_TYPE_HUNT_TRAP, srcGbId, desGbId, pos, 'catch')
        if self.bfSideIndex == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
            if self.gbId == srcGbId:
                gameglobal.rds.ui.vehicleSkill.refreshFrame(uiConst.TRAP_STATE_TRIGGER)
                p.showGameMsg(GMDD.data.BATTLE_FIELD_HUNT_ENEMY_INTRAP, ())
        else:
            p.showGameMsg(GMDD.data.BATTLE_FIELD_HUNT_MATE_INTRAP, ())
        soundId = SCD.data.get('HUNT_SOUND_TRAP', 5106)
        gameglobal.rds.sound.playSound(soundId, position=pos)

    def battleFieldHuntRunAwayFromTrap(self, pos, srcGbId, desGbId):
        bfGbIdTimerRef = getattr(self, 'bfGbIdTimerRef', {})
        self.bfGbIdTimerRef = bfGbIdTimerRef
        if bfGbIdTimerRef:
            timer = bfGbIdTimerRef.get((srcGbId, desGbId), 0)
            if timer:
                BigWorld.cancelCallback(timer)
                bfGbIdTimerRef[srcGbId, desGbId] = 0
        gameglobal.rds.ui.littleMap.addBFHuntIcon(uiConst.ICON_TYPE_HUNT_TRAP, srcGbId, desGbId, pos, 'lose')
        gameglobal.rds.ui.vehicleSkill.refreshFrame(uiConst.TRAP_STATE_BROKEN)
        disappearTime = DCD.data.get('trapDisappearTime', 2)
        delayDelTrapFun = Functor(self.delayDelTrap, uiConst.ICON_TYPE_HUNT_TRAP, srcGbId, desGbId)
        timer = BigWorld.callback(disappearTime, delayDelTrapFun)
        self.bfGbIdTimerRef[srcGbId, desGbId] = timer
        if gameglobal.rds.ui.pressKeyF.interactiveAvatars:
            gameglobal.rds.ui.pressKeyF.show()
        soundId = SCD.data.get('HUNT_SOUND_TRAP_BROKE', 5107)
        gameglobal.rds.sound.playSound(soundId, position=pos)

    def battleFieldHuntTrapBeDestroyed(self, pos, srcGbId, desGbId):
        bfGbIdTimerRef = getattr(self, 'bfGbIdTimerRef', {})
        self.bfGbIdTimerRef = bfGbIdTimerRef
        if bfGbIdTimerRef:
            timer = bfGbIdTimerRef.get((srcGbId, desGbId), 0)
            if timer:
                BigWorld.cancelCallback(timer)
                bfGbIdTimerRef[srcGbId, desGbId] = 0
        gameglobal.rds.ui.littleMap.addBFHuntIcon(uiConst.ICON_TYPE_HUNT_TRAP, srcGbId, desGbId, pos, 'lose')
        gameglobal.rds.ui.vehicleSkill.refreshFrame(uiConst.TRAP_STATE_BROKEN)
        disappearTime = DCD.data.get('trapDisappearTime', 5)
        delayDelTrapFun = Functor(self.delayDelTrap, uiConst.ICON_TYPE_HUNT_TRAP, srcGbId, desGbId)
        timer = BigWorld.callback(disappearTime, delayDelTrapFun)
        soundId = SCD.data.get('HUNT_SOUND_TRAP_BROKE', 5107)
        gameglobal.rds.sound.playSound(soundId, position=pos)

    def delayDelTrap(self, type, srcGbId, desGbId):
        gameglobal.rds.ui.littleMap.delBFHuntIcon(type, srcGbId, desGbId)
        gameglobal.rds.ui.vehicleSkill.refreshFrame(uiConst.TRAP_STATE_NORMAL)

    def onReceiveBattleFieldEnemysInfo(self, farawayEnemyInfo = None):
        enemyInfo = {}
        hasattr(self, 'nearEnemyPlayersInfo') and enemyInfo.update(self.nearEnemyPlayersInfo)
        farawayEnemyInfo and enemyInfo.update(farawayEnemyInfo)
        self.bfEnemyInfo = enemyInfo
        self.showEnemyPlayer(enemyInfo)

    def getPlayerDotaLv(self, gbId):
        entityId = self.battleFieldTeam.get(gbId, {}).get('id', 0)
        entity = BigWorld.entities.get(entityId, None)
        if not hasattr(self, 'bfDotaLvRecord'):
            self.bfDotaLvRecord = {}
        oldLv = self.bfDotaLvRecord.get(gbId, 1)
        if not entity:
            if self.battleFieldTeam.get(gbId, {}).get('sideNUID') == self.bfSideNUID:
                newLv = self.bfTeammateInfo.get(gbId, {}).get(gametypes.TEAM_SYNC_PROPERTY_LV, 1)
            else:
                newLv = self.bfEnemyInfo.get(gbId, {}).get(gametypes.TEAM_SYNC_PROPERTY_LV, 1)
        else:
            newLv = entity.battleFieldDotaLv
        newLv = 1 if newLv > DCD.data.get('BATTLE_FIELD_DOTA_MAX_LEVEL', 18) else newLv
        self.bfDotaLvRecord[gbId] = max(newLv, oldLv)
        return self.bfDotaLvRecord[gbId]

    def showEnemyPlayer(self, enemysInfo):
        gameglobal.rds.ui.littleMap.showEnemyPlayer(enemysInfo)

    def onBattleFieldPrepareDone(self):
        if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
            return
        gameglobal.rds.ui.battleField.startCounting()

    def onOpenBattleFieldShop(self, items):
        gameglobal.rds.ui.battleField.openItemShop(items)

    def updateBattleFieldShopSingleItem(self, page, pos, remainNum):
        gameglobal.rds.ui.battleFieldShop.updateSingleItem(page, pos, remainNum)

    def notifyBattleFieldStatsInfo(self, sType, arg):
        p = BigWorld.player()
        if formula.inDotaBattleField(self.mapID):
            return
        if sType == const.BATTLE_FIELD_STATS_TYPE_FIRST_BLOOD:
            gameglobal.rds.ui.battleField.showFirstKill(*arg)
        elif sType == const.BATTLE_FIELD_STATS_TYPE_ASSIST:
            gameglobal.rds.ui.battleField.showAssist()
        elif sType == const.BATTLE_FIELD_STATS_TYPE_COMBO_KILL:
            if p.isInPUBG():
                gameglobal.rds.ui.pubgKillAssist.showKill(*arg)
            else:
                gameglobal.rds.ui.battleField.showKill(*arg)

    def battleFieldFortInfo(self, subGroupIds, score, fortInfo, bulletInfo):
        gamelog.debug('@hjx fort#battleFieldFortInfo:', self.roleName, score, fortInfo, bulletInfo)
        self.bfScore = score
        self.bfFortInfo = fortInfo
        self.bfBulletInfo = bulletInfo
        gameglobal.rds.ui.battleField.refreshAllPlaneInfo()
        gameglobal.rds.ui.battleField.refreshAllBulletInfo()
        gameglobal.rds.ui.littleMap.showBfFortInfo()
        gameglobal.rds.ui.map.addBattleFortIcon()
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
            gameglobal.rds.ui.bFGuildTournamentLive.refreshAllPlane()

    def battleFieldPlaneInfo(self, subGroupId, score, planeInfo):
        gamelog.debug('@hjx fort#battleFieldPlaneInfo:', self.roleName, score, planeInfo)
        self.bfScore = score
        self.bfPlaneInfo = planeInfo
        gameglobal.rds.ui.littleMap.showBfFortInfo()
        gameglobal.rds.ui.battleField.refreshAllPlaneInfo()
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
            gameglobal.rds.ui.bFGuildTournamentLive.refreshAllPlane()

    def battleFieldBulletInfo(self, bulletInfo):
        gamelog.debug('@hjx fort#battleFieldBulletInfo:', self.roleName, bulletInfo)
        self.bfBulletInfo = bulletInfo
        gameglobal.rds.ui.littleMap.showBfFortInfo()
        gameglobal.rds.ui.battleField.refreshAllBulletInfo()

    def onEnterFortTrap(self, fortId, curValMap):
        gamelog.debug('@hjx fort#onEnterFortTrap:', self.roleName, fortId, curValMap)
        gameglobal.rds.ui.battleField.enterFort(fortId, curValMap)

    def onLeaveFortTrap(self, fortId):
        gamelog.debug('@hjx fort#onLeaveFortTrap:', self.roleName, fortId)
        gameglobal.rds.ui.battleField.leaveFort(fortId)

    def onSyncPosInfoInFortBattleField(self, posInfo):
        self.bfPlanePosInfo = posInfo
        gameglobal.rds.ui.littleMap.showBfFortInfo()
        gameglobal.rds.ui.map.addBattlePlaneIcon()

    def battleFieldHuntTargetLogOff(self, srcGbId, desGbId):
        gameglobal.rds.ui.littleMap.delBFHuntIcon(uiConst.ICON_TYPE_HUNT_TRAP, srcGbId, desGbId)

    def battleFieldHuntMateLogOff(self, srcGbId, desGbId):
        gameglobal.rds.ui.littleMap.delBFHuntIcon(uiConst.ICON_TYPE_HUNT_TRAP, srcGbId, desGbId)

    def onBossMonsterDieInFortBattleField(self, fbEntityNo):
        if fbEntityNo:
            clientShip = BigWorld.player().getClientShip(fbEntityNo)
            if clientShip:
                clientShip.playMonsterDieAction()

    def notifyEnemyRoleIds(self, enemyRoleIdDict):
        for gbId, zaijuId in enemyRoleIdDict.iteritems():
            self.bfDotaZaijuRecord[gbId] = zaijuId

    def notifyRechooseRoleId(self, playerGbId, zaijuId):
        self.bfDotaZaijuRecord[playerGbId] = zaijuId

    def confirmRoleInBattleFieldDota(self, tgtGbId, roleZaijuId):
        gamelog.debug('@lhb bf#dota confirmRoleInBattleFieldDota', tgtGbId, roleZaijuId)
        if tgtGbId != self.gbId:
            gameglobal.rds.sound.playSound(5615)
        self.bfDotaZaijuRecord[tgtGbId] = roleZaijuId
        self.preloadDotaZaiju(tgtGbId, roleZaijuId)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_BF_DOTA_ZAIJU_CHANGE, tgtGbId)

    def cancelRoleInBattleFieldDota(self, tgtGbId, roleZaijuId):
        self.bfDotaZaijuRecord[tgtGbId] = 0
        gameglobal.rds.ui.dispatchEvent(events.EVENT_BF_DOTA_ZAIJU_CHANGE, tgtGbId)
        gamelog.debug('@lhb bf#dota cancelRoleInBattleFieldDota', tgtGbId, roleZaijuId)

    def changeTalentSkills(self, tgtGbId, talentSkillIds):
        gamelog.debug('@lhb bf#dota changeTalentSkills', tgtGbId, talentSkillIds)
        self.bfDotaTalentSkillRecord[tgtGbId] = talentSkillIds
        gameglobal.rds.ui.dispatchEvent(events.EVENT_TALENT_SKILL_CHANGE, tgtGbId)

    def onBackToBattleFieldEnd(self):
        self.backToBfEnd = True
        gamelog.debug('@lhb onBackToBattleFieldEnd')

    def notifyDotaKillInfo(self, isFirstBlood, killerGbId, killeeGbId, killerAccumulateKill, killeeAccumulateKillCnt, comboKill):
        gamelog.debug('@hjx dota bf#notifyDotaKillInfo:', isFirstBlood, killerGbId, killeeGbId, killerAccumulateKill, killeeAccumulateKillCnt, comboKill)
        if getattr(self, 'isInBfDotaChooseHero', False):
            return
        if isFirstBlood:
            gameglobal.rds.ui.bfDotaKill.addFirstBloodInfo(killerGbId, killeeGbId)
        else:
            gameglobal.rds.ui.bfDotaKill.addNormalKillInfo(killerGbId, killeeGbId, killerAccumulateKill, killeeAccumulateKillCnt, comboKill)

    def showAddBattleFieldCash(self, killeeEntId, deltaCash, cashSource):
        mapKey = uiConst.BF_DOTA_ADD_COIN_NORMAL
        if cashSource in gametypes.BATTLE_FIELD_DOTA_ADDCASH_SOURCE_BY_ME_SET:
            mapKey = uiConst.BF_DOTA_ADD_COIN_SPECIAL
        gameglobal.rds.ui.showRewardLabel(deltaCash, mapKey, killeeEntId)
        soundId = DCD.data.get('bf_dota_sound_add_cash', 5121)
        gameglobal.rds.sound.playSound(soundId)
        gamelog.debug('@lhb showAddBattleFieldCash ', deltaCash, cashSource)

    def onQueryOthersBagInfoInDotaBattleField(self, version, othersBagInfo):
        othersBagInfo = cPickle.loads(zlib.decompress(othersBagInfo))
        gamelog.debug('@hjx dota#onQueryOthersBagInfoInDotaBattleField', version, othersBagInfo)
        self.bfDotaOtherEquipInfo = othersBagInfo
        self.oldEquipVersion = version

    def enemyRangeInBattleFieldDota(self, roleLeaveList, roleEnterList):
        gamelog.debug('@lhb bf#dota enemyPositionInBattleFieldDota', roleLeaveList, roleEnterList, self.enemyInRangeBFDotaInfoList)
        for roleLeaveItem in roleLeaveList:
            if roleLeaveItem in self.enemyInRangeBFDotaInfoList:
                self.enemyInRangeBFDotaInfoList.remove(roleLeaveItem)

        for roleEnterItem in roleEnterList:
            self.enemyInRangeBFDotaInfoList.append(roleEnterItem[0])
            self.showEnemyEnterRangeInBattleFieldDota(roleEnterItem[0][1], roleEnterItem[0][0], roleEnterItem[1])

    def onEnterVehicle(self, old):
        if formula.inDotaBattleField(self.mapID):
            entities = self.getDotaEntities()
            selfTempCamp = getattr(self, 'tempCamp', 0)
            selfVehicleId = getattr(self, 'vehicleId', 0)
            hasEnemy = False
            for entity in entities:
                if getattr(entity, 'vehicleId', 0) == selfVehicleId:
                    if self.isEnemy(entity):
                        hasEnemy = True
                        self.cell.onEnemyEnterRangeInBattleFieldDota(entity.id)
                        gamelog.info('@jbx:onEnemyEnterRangeInBattleFieldDota', entity.id)

            if not hasEnemy:
                self.cell.onMyLeaveRangeInBattleFieldDota()
                gamelog.info('@jbx:onMyLeaveRangeInBattleFieldDota')

    def getDotaEntities(self):
        arr = []
        for entity in BigWorld.entities.values():
            if utils.instanceof(entity, 'Avatar'):
                arr.append(entity)
            elif getattr(entity, 'isBattleFieldDotaTower', False):
                arr.append(entity)

        return arr

    def onLeaveVehicle(self, old):
        if formula.inDotaBattleField(self.mapID):
            entities = self.getDotaEntities()
            selfTempCamp = getattr(self, 'tempCamp', 0)
            selfVehicleId = old
            inVehicleEnemys = []
            hasInVehicleTeammate = False
            hasEnemy = False
            for entity in entities:
                if self.isEnemy(entity):
                    hasEnemy = True
                    if getattr(entity, 'vehicleId', 0) == selfVehicleId:
                        inVehicleEnemys.append(entity)
                else:
                    hasInVehicleTeammate = True

            if not hasInVehicleTeammate:
                for entity in inVehicleEnemys:
                    entity.cell.onMyLeaveRangeInBattleFieldDota()
                    gamelog.info('@jbx:onEnemyLeaveRangeInBattleFieldDota', entity.id)

            if hasEnemy:
                self.cell.onMyEnterRangeInBattleFieldDota()
                gamelog.info('@jbx:onMyEnterRangeInBattleFieldDota')

    def getEnemyGbIdList(self):
        idList = []
        for gbId, mInfo in self.battleFieldTeam.iteritems():
            if mInfo['sideNUID'] != self.bfSideNUID:
                idList.append(gbId)

        return idList

    def getTeammateGbIdList(self):
        idList = []
        for gbId, mInfo in self.battleFieldTeam.iteritems():
            if mInfo['sideNUID'] == self.bfSideNUID:
                idList.append(gbId)

        return idList

    def getOtherAliveTeamMateEntityIds(self):
        idList = []
        for gbId, mInfo in self.battleFieldTeam.iteritems():
            if gbId != self.gbId and mInfo['life'] == gametypes.LIFE_ALIVE and mInfo['sideNUID'] == self.bfSideNUID:
                idList.append(mInfo['id'])

        idList.sort()
        return idList

    def onQueryBattleFieldDotaRole(self, dotaRoleInfo):
        """
        
        Args:
            dotaRoleInfo: {roleId: expiredTime}
        
        Returns:
        
        """
        gamelog.debug('@lhb favorequip onQueryBattleFieldDotaRole ', dotaRoleInfo)
        dotaRoleInfo['serverTime'] = utils.getNow()
        CEFControl.execute('queryBattleFieldDotaRole', dotaRoleInfo)

    def onQueryBFDotaFavorEquip(self, favorEquipInfo):
        """
        
        Args:
        
            favorEquipInfo: {'favorEquipDict': {1:[\xce\xef\xc6\xb71,\xce\xef\xc6\xb72...],2:[\xce\xef\xc6\xb71,\xce\xef\xc6\xb72...]}, 'defaultFavorKey': 1}
            'defaultFavorKey': \xb5\xb1\xc7\xb0\xc4\xac\xc8\xcf\xb5\xc4\xcd\xc6\xbc\xf6key
        
        Returns:
        
        """
        gamelog.debug('@lhb favorequip onQueryBFDotaFavorEquip ', favorEquipInfo)
        configData = ZD.data.get(favorEquipInfo.get('roleId', 10000), {})
        favorEquipInfo['recommend_equips'] = configData.get('recommend_equips', ((),))[-1]
        gameglobal.rds.ui.bfDotaShop.selectedFavorEquipsKey = favorEquipInfo.get('defaultFavorKey', 1)
        CEFControl.execute('queryBFDotaFavorEquip', favorEquipInfo)
        self.favorEquipInfo = favorEquipInfo

    def onQueryBFDotaTokenSucc(self, tokenJsonStr):
        gamelog.debug('@lhb onQueryBFDotaToken onQueryBFDotaTokenSucc ', tokenJsonStr)
        tokenDic = json.loads(tokenJsonStr)
        gameglobal.rds.ui.bfDotaHeros.getTokenCallBack(tokenDic['data'])

    def onQueryBFDotaTokenFail(self, reason):
        gamelog.debug('@lhb onQueryBFDotaToken onQueryBFDotaTokenFail ', reason)

    def onSetBFDotaFavorEquipFail(self):
        CEFControl.execute('setBFDotaFavorEquip', {'succ': False})

    def onSetBFDotaFavorEquipSucc(self):
        CEFControl.execute('setBFDotaFavorEquip', {'succ': True})

    def onSetBFDotaFavorAliasFail(self):
        CEFControl.execute('setBFDotaFavorEquipAlias', {'succ': False})

    def onSetBFDotaFavorAliasSucc(self):
        CEFControl.execute('setBFDotaFavorEquipAlias', {'succ': True})

    def onSetBFDotaDefaultFavorEquipFail(self):
        CEFControl.execute('setBFDotaDefaultFavorEquip', {'succ': False})

    def onSetBFDotaDefaultFavorEquipSucc(self):
        CEFControl.execute('setBFDotaDefaultFavorEquip', {'succ': True})

    def showEnemyEnterRangeInBattleFieldDota(self, enemyRoleId, enemyRoleGbId, enemyRolePos):
        enemyEnt = BigWorld.entities.get(enemyRoleId)
        if enemyEnt:
            enemyRolePos = enemyEnt.position

    def receiveMarkDoneDota(self, markType, markValue, markerGbId):
        gamelog.debug('@lhb receiveMarkDoneDota ', markType, markValue, markerGbId)
        gameglobal.rds.ui.littleMap.showPosition(markValue)
        gameglobal.rds.ui.bfDotaSignal.refreshSignalInfo(markerGbId, markType)
        if markerGbId == self.gbId:
            gameglobal.rds.ui.littleMap.playBfDotaBtnsCoolDown()

    def notifyBFDotaCDTime(self, playerGbId, skillId, skillLv, skillCDTime):
        gamelog.debug('@lhb notifyBFDotaCDTime ', playerGbId, skillId, skillLv, skillCDTime)
        gameglobal.rds.ui.bfDotaItemAndProp.playSkillCdCoolDown(playerGbId, skillId, skillLv, skillCDTime)
        self.bfDotaSkillInitRecord.setdefault(playerGbId, {}).setdefault(skillId, True)

    def notifyBFDotaSkillInit(self, playerGbId, skillId):
        gamelog.debug('@lhb notifyBFDotaSkillInit ', playerGbId, skillId)
        self.bfDotaSkillInitRecord.setdefault(playerGbId, {}).setdefault(skillId, True)

    def onGetBattleFieldMembersTotalCash(self, totalCashDict):
        self.bfDotaTotalCashDict = totalCashDict
        gameglobal.rds.ui.bfDotaDetail.refreshInfo()

    def playBfDotaLvUpEff(self):
        self.fashion._attachFx(self.id, self.model, [1020], False)

    def isInBfDota(self):
        return formula.inDotaBattleField(getattr(self, 'mapID', 0))

    def isInBfChaos(self):
        return self.bfChaosModeDetail['bfChaosModeType']

    def getBfDuelStatsInfo(self, gbId, type):
        selfMemPerform = None
        for memPerform in self.bfMemPerforms:
            if gbId == memPerform['gbId']:
                selfMemPerform = memPerform
                break

        if not selfMemPerform:
            return (0, 3)
        value = selfMemPerform.get(type, 0)
        upperCnt = 0
        for memPerform in self.bfMemPerforms:
            if memPerform.get(const.BF_COMMON_SIDE_NUID, 0) == selfMemPerform['sideNUID'] and memPerform.get(type, 0) > value:
                upperCnt += 1

        if not value:
            upperCnt = 3
        return (value, min(3, upperCnt + 1))

    def addBfDotaTimer(self):
        if not getattr(self, 'bfDotaTimer', 0):
            self.bfDotaTimer = BigWorld.callback(0.1, self.bfDotaTimerFunc)

    def bfDotaTimerFunc(self):
        self.visibleBfDotaEnemyIdSet = set()
        p = BigWorld.player()
        if not p.isInBfDota() or not self.inWorld or not p or p.id != self.id:
            return
        entitySet = self.bfDotaEntityIdRecord.get(const.DOTA_ENTITY_TYPE_LITTLE_MAP, set())
        teamMateSet = set()
        enemySet = set()
        for entityId in self.bfDotaEntityIdRecord.get(const.DOTA_ENTITY_TYPE_TEAMMATE, []):
            entity = BigWorld.entities.get(entityId, None)
            entity and teamMateSet.add(entity)

        for entityId in entitySet:
            entity = BigWorld.entities.get(entityId, None)
            if entity:
                if p.isEnemy(entity):
                    enemySet.add(entity)
                else:
                    teamMateSet.add(entity)

        for enemy in enemySet:
            for teamMate in teamMateSet:
                if enemy and teamMate and sMath.distance3D(enemy.position, teamMate.position) < DCD.data.get('bfDotaVisibleDistance', 80):
                    enemyVehicleId = getattr(enemy, 'vehicleId', 0)
                    teamMateVehicleId = getattr(teamMate, 'vehicleId', 0)
                    if not enemyVehicleId:
                        self.visibleBfDotaEnemyIdSet.add(enemy.id)
                    elif enemyVehicleId == teamMateVehicleId:
                        self.visibleBfDotaEnemyIdSet.add(enemy.id)
                    elif getattr(enemy, 'inCombat', False):
                        self.visibleBfDotaEnemyIdSet.add(enemy.id)

        self.bfDotaTimer = BigWorld.callback(0.1, self.bfDotaTimerFunc)

    def delBfDotaTimer(self):
        if getattr(self, 'bfDotaTimer', 0):
            BigWorld.cancelCallback(self.bfDotaTimer)
            self.bfDotaTimer = 0

    def preloadDotaZaiju(self, playerGbId, zaijuId):
        gamelog.info('jbx:preloadDotaZaiju', playerGbId, zaijuId)
        if not playerGbId or not zaijuId:
            return
        mapId = formula.getMapId(self.spaceNo)
        if not formula.inDotaBattleField(mapId):
            return
        if self.bianshen[1]:
            return
        if not gameglobal.rds.configData.get('enableDotaZaijuPreLoad', False):
            return
        effs = self.getAllSkillEffectByZaijuId(zaijuId)
        effectLv = self.getEffectLv()
        for eff in effs:
            sfx.gEffectMgr.preloadFx(eff, effectLv)

        modelId = ZD.data.get(zaijuId, {}).get('modelId', 0)
        if not modelId:
            return
        if self.preloadDotaZaijuFetchs.get(playerGbId, 0):
            BigWorld.cancelBgTask(self.preloadDotaZaijuFetchs[playerGbId])
        actionList = self.getAllSkillActionsByZaijuId(zaijuId)
        attachments = self.modelServer.rideAttached.getAttachments(zaijuId, ZD.data.get(zaijuId, {}), 0, [])
        if not attachments:
            return
        a = attachments[0]
        fullModelPath = a[0]
        dye = a[6] if a[6] else a[1]
        res = [fullModelPath, ('*', dye)]
        finishedCallback = Functor(self._preloadDotaZaijuModelFinished, playerGbId, zaijuId, actionList)
        gamelog.info('jbx:fetchModel', self.modelServer.rideAttached.threadID, finishedCallback, attachments[0])
        self.preloadDotaZaijuFetchs[playerGbId] = clientUtils.fetchModel(self.modelServer.rideAttached.threadID, finishedCallback, *res)

    def _preloadDotaZaijuModelFinished(self, playerGbId, zaijuId, actionList, model):
        gamelog.info('jbx:_preloadDotaZaijuModelFinished', playerGbId, zaijuId, actionList, model)
        if actionList:
            self.holdPreloadDotaZaijuModel[playerGbId] = (zaijuId, model)
            self.preloadDotaZaijuFetchs[playerGbId] = 0
            if model and hasattr(model, 'resideActions'):
                model.resideActions(*actionList)

    def notifyDotaBFVoteForPlayer(self, gbId, roleName, voteType):
        """
        \xcd\xf5\xd5\xdf\xb6\xd4\xbe\xf6\xcd\xa8\xd6\xaa\xcd\xe6\xbc\xd2\xbf\xc9\xd2\xd4\xb7\xa2\xc6\xf0\xbe\xd9\xb1\xa8
        :param gbId: \xb1\xbb\xbe\xd9\xb1\xa8\xcd\xe6\xbc\xd2\xb5\xc4id
        :param roleName: \xb1\xbb\xbe\xd9\xb1\xa8\xcd\xe6\xbc\xd2\xb5\xc4\xbd\xc7\xc9\xab\xc3\xfb
        :param voteType: \xbe\xd9\xb1\xa8\xc0\xe0\xd0\xcd\xa3\xac\xbc\xfbgametypes.DOTA_BF_VOTE_TYPE_EXP\xcf\xe0\xb9\xd8
        :return:
        """
        gameglobal.rds.ui.bfDotaVote.addVoteInfo(gbId, roleName, voteType)
        gamelog.debug('@zhangkuo notifyDotaBFVoteForPlayer', gbId, roleName, voteType)

    def setNewFlagBattleFieldStatus(self, battleId, actId, status):
        gamelog.debug('@zmk setNewFlagBattleFieldStatus', battleId, actId, status)
        if not self.newFlagBattleFieldStatus.has_key(battleId):
            self.newFlagBattleFieldStatus[battleId] = {}
        self.newFlagBattleFieldStatus[battleId][actId] = status

    def setAllNewFlagStatus(self, dictStatus):
        gamelog.debug('@zmk setAllNewFlagStatus', dictStatus)
        if self.newFlagBattleFieldStatus:
            self.newFlagBattleFieldStatus.update(dictStatus)
        else:
            self.newFlagBattleFieldStatus = dictStatus

    def setNewFlagBattleFieldStage(self, battleId, actId, stage):
        gamelog.debug('@zmk setNewFlagBattleFieldStage', battleId, actId, stage)
        if not self.newFlagBattleFieldStage.has_key(battleId):
            self.newFlagBattleFieldStage[battleId] = {}
        self.newFlagBattleFieldStage[battleId][actId] = stage
        if stage in (gametypes.NEW_FLAG_BF_STAGE_OPEN, gametypes.NEW_FLAG_BF_STAGE_CLOSE):
            self.newFlagClear()
        self.updateNewFlagGeneralPushIcon()

    def newFlagClear(self):
        self.battleFieldZaijus = {}
        self.battleFieldZaijusCommitTime = {}
        self.battleFiedlMonstersPos = {}
        self.battleFiedlOccupyInfo = {}

    def setAllNewFlagStage(self, dictStage):
        gamelog.debug('@zmk setAllNewFlagStage', dictStage)
        if self.newFlagBattleFieldStage:
            self.newFlagBattleFieldStage.update(dictStage)
        else:
            self.newFlagBattleFieldStage = dictStage
        overAppplyBattleId = 0
        canApply = False
        for battleId, mVal in dictStage.iteritems():
            for stage in mVal.itervalues():
                if stage == gametypes.NEW_FLAG_BF_STAGE_OPEN:
                    self.notifyApplyNewFlag(battleId)
                    canApply = True
                    break
                else:
                    overAppplyBattleId = battleId

        if not canApply and overAppplyBattleId:
            self.endApplyNewFlag(overAppplyBattleId)
        self.updateNewFlagGeneralPushIcon()

    def updateNewFlagGeneralPushIcon(self):
        curBattleId = 0
        curStage = 0
        for battleId, mVal in self.newFlagBattleFieldStage.iteritems():
            for stage in mVal.itervalues():
                if stage == gametypes.NEW_FLAG_BF_STAGE_START:
                    curStage = stage
                    curBattleId = battleId
                if stage == gametypes.NEW_FLAG_BF_STAGE_OPEN:
                    if curStage != gametypes.NEW_FLAG_BF_STAGE_START:
                        curStage = stage
                        curBattleId = battleId

        gameglobal.rds.ui.battleOfFortPush.battleId = curBattleId
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GENERAL_PUSH_STATECHANGE, (generalPushMappings.GENERAL_PUSH_BATTLE_OF_FORT, curStage))

    def resetNewFlag(self, dictStage):
        """\xd6\xd8\xd6\xc3\xb6\xe1\xc6\xec\xd5\xbd\xb3\xa1"""
        gamelog.debug('@zmk resetNewFlag', dictStage)
        self.newFlagBattleFieldStage = dictStage
        for battleId, mVal in dictStage.iteritems():
            for actId in mVal.iterkeys():
                self.setNewFlagBattleFieldStatus(battleId, actId, gametypes.NEW_FLAG_BF_STATE_DEFAULT)

    def notifyApplyNewFlag(self, battleId):
        """
        \xcd\xa8\xd6\xaa\xcd\xe6\xbc\xd2\xbf\xc9\xd2\xd4\xb1\xa8\xc3\xfb\xc1\xcb
        """
        gamelog.debug('@zmk notifyApplyNewFlag', battleId)
        BigWorld.flashWindow(2)
        pushId = BFMD.data.get(battleId, {}).get('battleSignUpPushId', 11544)
        if pushId not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': Functor(self.onPushSignUpClick, battleId, pushId)})

    def endApplyNewFlag(self, battleId):
        gamelog.debug('@zmk endApplyNewFlag', battleId)
        pushId = BFMD.data.get(battleId, {}).get('battleSignUpPushId', 11544)
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def onPushSignUpClick(self, battleId, pushId):
        gamelog.debug('@zmk onPushSignUpClick', battleId, pushId)
        gameglobal.rds.ui.battleOfFortSignUp.show(battleId)
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def onApplyNewFlag(self, battleId, actId):
        """
        \xb3\xc9\xb9\xa6\xb1\xa8\xc3\xfb\xba\xec\xca\xaf\xb1\xa4\xd5\xf9\xb6\xe1\xd5\xbd\xb5\xc4\xbb\xd8\xb5\xf7
        :param battleId: \xd5\xbd\xb3\xa1ID
        :param actId:\xbb\xee\xb6\xaf\xb3\xa1\xb4\xceID\xa3\xa8\xc8\xe7\xa3\xba1,2,3,4\xa3\xa9
        :return:
        """
        gamelog.debug('@zmk onApplyNewFlag', battleId, actId)
        self.setNewFlagBattleFieldStatus(battleId, actId, gametypes.NEW_FLAG_BF_STATE_CONFIRMED_APPLY)
        battleData = BFMD.data.get(battleId, {})
        startBattleTimeParts = battleData.get('startBattleTimeParts', ['14:00-14.30',
         '14:30-15:00',
         '21:00-21:30',
         '21:30-22:00'])
        startT, endT = startBattleTimeParts[actId - 1].split('-')
        self.showGameMsg(battleData.get('onApplyTimingBattleSuccessMsgId', 51848), (actId, startT, endT))
        gameglobal.rds.ui.battleOfFortSignUp.show(battleId)

    def notifyConfirmApplyNewFlag(self, battleId, actId, gbId, roleName):
        """
        \xb6\xd3\xb3\xa4\xb1\xa8\xc3\xfb\xa3\xac\xcd\xa8\xd6\xaa\xb6\xd3\xd3\xd1\xc8\xb7\xc8\xcf\xca\xc7\xb7\xf1\xb1\xa8\xc3\xfb\xba\xec\xca\xaf\xb1\xa4\xd5\xf9\xb6\xe1\xd5\xbd
        :param battleId: \xd5\xbd\xb3\xa1ID
        :param actId: \xbb\xee\xb6\xaf\xb3\xa1\xb4\xceID
        :param gbId: \xb6\xd3\xb3\xa4\xb5\xc4gbId
        :param roleName: \xb6\xd3\xb3\xa4\xbd\xc7\xc9\xab\xc3\xfb
        """
        gamelog.debug('@zmk notifyConfirmApplyNewFlag', battleId, actId, gbId, roleName)
        self.setNewFlagBattleFieldStatus(battleId, actId, gametypes.NEW_FLAG_BF_STATE_CONFIRMING_APPLY)
        battleData = BFMD.data.get(battleId, {})
        if gbId == self.gbId:
            self.showGameMsg(battleData.get('onConfirmApplyTimingBattleHeaderMsgId', 0), ())
        else:
            mode = battleData.get('mode', 0)
            startBattleTimeParts = battleData.get('startBattleTimeParts', ['14:00-14.30',
             '14:30-15:00',
             '21:00-21:30',
             '21:30-22:00'])
            msg = uiUtils.getTextFromGMD(battleData.get('onConfirmApplyTimingBattleTeammateMsgId', 51442), '%s,%s,%s') % (roleName, actId, startBattleTimeParts[actId - 1])
            if mode == const.BATTLE_FIELD_MODE_TIMING_PUBG:
                ConfirmApplyCallBack = self.cell.confirmApplyTimingPUBGBattleField
            else:
                ConfirmApplyCallBack = self.cell.confirmApplyNewFlagBattleField
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(ConfirmApplyCallBack, battleId, actId, gbId, True), noCallback=Functor(ConfirmApplyCallBack, battleId, actId, gbId, False), repeat=battleData.get('timingBattleConfirmApplyTime', 60), repeatText=gameStrings.CLAN_CHALLENGE_REPEAT, countDownFunctor=Functor(ConfirmApplyCallBack, battleId, actId, gbId, False), canEsc=True)

    def onConfirmApplyNewFlag(self, battleId, actId, gbId, isOk):
        """
        \xc8\xb7\xc8\xcf\xb1\xa8\xc3\xfb\xbd\xe1\xb9\xfb\xb5\xc4\xbb\xd8\xb5\xf7
        :param battleId: \xd5\xbd\xb3\xa1ID
        :param actId: \xbb\xee\xb6\xafID
        :param gbId: \xb6\xd3\xb3\xa4gbId
        :param isOk: \xca\xc7\xb7\xf1\xc8\xb7\xc8\xcf\xb1\xa8\xc3\xfb
        :return:
        """
        gamelog.debug('@zmk onConfirmApplyNewFlag', battleId, actId, gbId, isOk)
        state = gametypes.NEW_FLAG_BF_STATE_DEFAULT
        if isOk:
            state = gametypes.NEW_FLAG_BF_STATE_CONFIRMED_APPLY
        self.setNewFlagBattleFieldStatus(battleId, actId, state)
        gameglobal.rds.ui.battleOfFortSignUp.show(battleId)
        if gbId == self.gbId:
            if isOk:
                self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TIMING_BATTLE_TEAMMATE_CONFIRM_APPLY,))
            else:
                self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TIMING_BATTLE_TEAMMATE_REJECT_APPLY,))
        elif isOk:
            self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TIMING_BATTLE_SELF_CONFIRM_APPLY,))
        else:
            self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TIMING_BATTLE_SELF_REJECT_APPLY,))

    def notifyConfirmEnterNewFlag(self, battleId, actId, nextTimestamp):
        """
        \xba\xec\xca\xaf\xb1\xa4\xd5\xf9\xb6\xe1\xd5\xbd\xbf\xaa\xca\xbc\xc7\xb0\xcd\xa8\xd6\xaa\xcd\xe6\xbc\xd2\xc8\xb7\xc8\xcf\xca\xc7\xb7\xf1\xbd\xf8\xc8\xeb\xd5\xbd\xb3\xa1
        :param battleId: \xd5\xbd\xb3\xa1\xb1\xe0\xba\xc5
        :param actId: \xbb\xee\xb6\xaf\xb3\xa1\xb4\xceID
        :param nextTimestamp: \xbf\xaa\xca\xbc\xc6\xa5\xc5\xe4\xb5\xc4\xca\xb1\xbc\xe4\xb4\xc1
        :return:
        """
        gamelog.debug('@zmk confirmEnterNewFlagBattleField', battleId, actId)
        self.setNewFlagBattleFieldStatus(battleId, actId, gametypes.NEW_FLAG_BF_STATE_CONFIRMING_ENTER)
        BigWorld.flashWindow(2)
        gameglobal.rds.ui.battleOfFortTimeDown.sureSignUp = False
        gameglobal.rds.ui.battleOfFortTimeDown.show(battleId, actId, nextTimestamp)
        pushId = BFMD.data.get(battleId, {}).get('battleStartSurePushId', 11545)
        if pushId not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': Functor(self.onPushBeforeTheStartClick, battleId, actId, nextTimestamp)})

    def onPushBeforeTheStartClick(self, battleId, actId, nextTimestamp):
        gameglobal.rds.ui.battleOfFortTimeDown.show(battleId, actId, nextTimestamp)

    def onConfirmEnterNewFlag(self, battleId, actId, isOk):
        """
        \xc8\xb7\xc8\xcf\xca\xc7\xb7\xf1\xbd\xf8\xc8\xeb\xd5\xbd\xb3\xa1\xb5\xc4\xbb\xd8\xb5\xf7
        :param actId:
        :param isOk:
        :return:
        """
        gamelog.debug('@zmk onConfirmEnterNewFlag', battleId, actId, isOk, self.roleName)
        p = BigWorld.player()
        if isOk:
            self.setNewFlagBattleFieldStatus(battleId, actId, gametypes.NEW_FLAG_BF_STATE_CONFIRMED_ENTER)
            gameglobal.rds.ui.battleOfFortTimeDown.setSureSignUpDesc()
        else:
            self.setNewFlagBattleFieldStatus(battleId, actId, gametypes.NEW_FLAG_BF_STATE_DEFAULT)
            gameglobal.rds.ui.battleOfFortTimeDown.cancelSignUp()

    def onNewFlagBattleFieldReady(self, nextTimestamp):
        """\xd5\xbd\xb3\xa1\xd7\xbc\xb1\xb8\xbd\xd7\xb6\xce"""
        gamelog.debug('@zhangkuo onNewFlagBattleFieldReady [nextTimestamp]', nextTimestamp)

    def syncNewFlagOccupyInfo(self, occupyInfo):
        """
        \xcd\xac\xb2\xbd\xcb\xae\xbe\xa7\xcb\xfe\xd5\xbc\xc1\xec\xd0\xc5\xcf\xa2 {\xcb\xae\xbe\xa7\xcb\xfe\xc8\xab\xbe\xd6\xb1\xe0\xba\xc5\xa3\xba{'camp': \xd5\xbc\xc1\xec\xb7\xbd, 'fortId': \xcb\xae\xbe\xa7\xcb\xfeID, 'curValMap': \xd5\xbc\xc1\xec\xbd\xf8\xb6\xc8,}}
        """
        gamelog.debug('@zhangkuo syncNewFlagOccupyInfo', str(occupyInfo))
        self.battleFiedlOccupyInfo = occupyInfo
        gameglobal.rds.ui.battleOfFortProgressBar.updateNewFlagOccupyPoint(occupyInfo)
        gameglobal.rds.ui.battleOfFortProgressBar.updateNewFlagTowerTrap(occupyInfo)
        gameglobal.rds.ui.littleMap.showBattleFortCrystalIcon()

    def onEnterNewFlagTowerTrap(self, towerId, curValMap):
        """
        \xbd\xf8\xc8\xeb\xcb\xae\xbe\xa7\xcb\xfe\xb7\xb6\xce\xa7
        :param towerId: \xcb\xae\xbe\xa7\xcb\xfeID
        :param curValMap: \xcb\xae\xbe\xa7\xb5\xc4\xd5\xbc\xc1\xec\xc7\xe9\xbf\xf6 {camp1:\xd5\xbc\xc1\xec\xbd\xf8\xb6\xc8\xa3\xac camp2:\xd5\xbc\xc1\xec\xbd\xf8\xb6\xc8}
        """
        gamelog.debug('@zhangkuo onEnterNewFlagTowerTrap', towerId, curValMap)
        gameglobal.rds.ui.battleOfFortProgressBar.enterNewFlagTowerTrap(towerId, curValMap)

    def onLeaveNewFlagTowerTrap(self, towerId):
        """
        \xc0\xeb\xbf\xaa\xcb\xae\xbe\xa7\xcb\xfe\xb7\xb6\xce\xa7
        :param towerId: \xcb\xae\xbe\xa7\xcb\xfeID
        :return:
        """
        gamelog.debug('@zhangkuo onLeaveNewFlagTowerTrap', towerId)
        gameglobal.rds.ui.battleOfFortProgressBar.leaveNewFlagTowerTrap(towerId)

    def syncNewFlagDonatePoint(self, point, rank):
        """
        \xcd\xac\xb2\xbd\xb8\xf6\xc8\xcb\xb9\xb1\xcf\xd7\xba\xcd\xc5\xc5\xc3\xfb\xd0\xc5\xcf\xa2
        :param point: \xb8\xf6\xc8\xcb\xb9\xb1\xcf\xd7\xd6\xb5
        :param rank: \xb9\xb1\xcf\xd7\xc5\xc5\xc3\xfb
        """
        gamelog.debug('@zhangkuo syncNewFlagDonatePoint [point][rank]', point, rank)
        gameglobal.rds.ui.battleOfFortProgressBar.updateNewFlagDonate(point, rank)

    def syncNewFlagCanhunPos(self, data):
        """
        \xcd\xac\xb2\xbd\xb2\xd0\xbb\xea\xce\xbb\xd6\xc3\xa1\xa2\xd5\xbc\xc1\xec\xd0\xc5\xcf\xa2 \xd4\xf6\xc1\xbf\xb8\xfc\xd0\xc2
        """
        gamelog.debug('@zhangkuo syncNewFlagCanhunPos', data)
        battleFieldZaijusCommitTime = getattr(self, 'battleFieldZaijusCommitTime', {})
        for zaijuNUID, info in data.iteritems():
            if zaijuNUID in battleFieldZaijusCommitTime:
                if utils.getNow() - battleFieldZaijusCommitTime[zaijuNUID] < 5:
                    continue
            self.battleFieldZaijus[zaijuNUID] = info

        gamelog.debug('@zhangkuo syncNewFlagCanhunPos', self.battleFieldZaijus)
        gameglobal.rds.ui.littleMap.showBattleFortZaijuIcon()

    def onEnterCanhunZaiju(self, NUID, camp, gbId):
        """
        \xd3\xd0\xcd\xe6\xbc\xd2\xca\xb0\xc8\xa1\xc1\xcb\xb2\xd0\xbb\xea\xd4\xd8\xbe\xdf
        :param NUID: \xd4\xd8\xbe\xdf\xb5\xc4\xce\xa8\xd2\xbb\xb1\xea\xca\xb6
        :param camp: \xcd\xe6\xbc\xd2\xd5\xf3\xd3\xaa
        :param gbId: \xcd\xe6\xbc\xd2GBID
        :return:
        """
        gamelog.debug('@zhangkuo onEnterCanhunZaiju', NUID, camp, gbId)
        gameglobal.rds.ui.battleOfFortProgressBar.enterNewFlagZaiju(NUID, camp, gbId)
        if gbId == self.gbId:
            self.showGameMsg(GMDD.data.NEW_FALG_OCCUPIED_ZAIJU, ())
        if NUID in self.battleFieldZaijus:
            self.battleFieldZaijus[NUID]['camp'] = camp
            gameglobal.rds.ui.littleMap.showBattleFortZaijuIcon()

    def onLeaveCanhunZaiju(self, NUID, camp, gbId):
        """
        \xd3\xd0\xcd\xe6\xbc\xd2\xc0\xeb\xbf\xaa\xc1\xcb\xb2\xd0\xbb\xea\xd4\xd8\xbe\xdf
        :param NUID: \xd4\xd8\xbe\xdf\xb1\xea\xca\xb6
        :param camp: \xd5\xf3\xd3\xaa
        :param gbId: \xcd\xe6\xbc\xd2GBID
        """
        gamelog.debug('@zhangkuo onLeaveCanhunZaiju', NUID, camp, gbId)
        gameglobal.rds.ui.battleOfFortProgressBar.leaveNewFlagZaiju(NUID, camp, gbId)
        if NUID in self.battleFieldZaijus:
            self.battleFieldZaijus[NUID]['camp'] = 0
            gameglobal.rds.ui.littleMap.showBattleFortZaijuIcon()

    def onMonsterBornInNewFlag(self, fbEntityNo):
        """
        \xb9\xd6\xce\xef\xb3\xf6\xcf\xd6
        """
        pos = FED.data.get(fbEntityNo, {}).get('pos', (0, 0, 0))
        gamelog.debug('@zhangkuo onMonsterBornInNewFlag', fbEntityNo, pos)
        self.battleFiedlMonstersPos[fbEntityNo] = copy.deepcopy(pos)
        gameglobal.rds.ui.littleMap.showBattleFortMonsterIcon()

    def onMonsterDieInNewFlag(self, fbEntityNo):
        """
        \xb9\xd6\xce\xef\xcf\xfb\xca\xa7
        """
        pos = FED.data.get(fbEntityNo, {}).get('pos', (0, 0, 0))
        gamelog.debug('@zhangkuo onMonsterDieInNewFlag', fbEntityNo, pos)
        if fbEntityNo in self.battleFiedlMonstersPos:
            self.battleFiedlMonstersPos.pop(fbEntityNo)
            gameglobal.rds.ui.littleMap.showBattleFortMonsterIcon()

    def notifyPlayerNotEnoughInNewFlag(self, battleId, actId):
        """\xc8\xcb\xca\xfd\xb2\xbb\xd7\xe3\xce\xde\xb7\xa8\xbf\xaa\xc6\xf4\xd5\xbd\xb3\xa1"""
        gamelog.debug('@zhangkuo notifyPlayerNotEnoughInNewFlag', battleId, actId)
        p = BigWorld.player()
        p.unlockKey(gameglobal.KEY_POS_UI)
        msg = uiUtils.getTextFromGMD(GMDD.data.BATTLE_OF_FORT_LESS_MEMBERS, '%d') % actId
        gameglobal.rds.ui.messageBox.showAlertBox(msg)
        if hasattr(self, 'newFlagMsgBoxId') and self.newFlagMsgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.newFlagMsgBoxId)
            self.newFlagMsgBoxId = 0

    def notifyMatchingInNewFlag(self, battleId, actId):
        """\xd5\xfd\xd4\xda\xc6\xa5\xc5\xe4"""
        gamelog.debug('@zmk notifyMatchingInNewFlag', battleId, actId)
        p = BigWorld.player()
        if p.newFlagBattleFieldStatus[battleId][actId] != gametypes.NEW_FLAG_BF_STATE_CONFIRMED_ENTER:
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.BATTLE_OF_FORT_NOTIFY_MATCHINT, '')
        self.newFlagMsgBoxId = gameglobal.rds.ui.messageBox.showAlertBox(msg)
        gameglobal.rds.ui.battleOfFortTimeDown.hideProxy()

    def onZaijuCommitedInNewFlag(self, gbId, zaijuNUID):
        """\xd4\xd8\xbe\xdf\xb1\xbb\xc9\xcf\xbd\xbb"""
        gamelog.debug('@zhangkuo onZaijuCommitedInNewFlag', gbId, zaijuNUID)
        if zaijuNUID in self.battleFieldZaijus:
            self.battleFieldZaijus.pop(zaijuNUID)
        if not hasattr(self, 'battleFieldZaijusCommitTime'):
            self.battleFieldZaijusCommitTime = {}
        self.battleFieldZaijusCommitTime[zaijuNUID] = utils.getNow()
        gameglobal.rds.ui.littleMap.showBattleFortZaijuIcon()

    def syncNewFlagInfo(self, towerInfo, donateInfo, zaijuInfo, monsterInfo):
        """\xd6\xd8\xd0\xc2\xc9\xcf\xcf\xdf\xcd\xac\xb2\xbd\xb5\xb1\xc7\xb0\xcb\xf9\xd3\xd0\xd0\xc5\xcf\xa2"""
        gamelog.debug('@zhangkuo syncNewFlagInfo', towerInfo, donateInfo, zaijuInfo, monsterInfo)
        self.syncNewFlagOccupyInfo(towerInfo)
        self.syncNewFlagDonatePoint(*donateInfo)
        self.battleFieldZaijus.clear()
        self.battleFieldZaijusCommitTime = {}
        self.syncNewFlagCanhunPos(zaijuInfo)
        for fbEntityNo in monsterInfo:
            self.onMonsterBornInNewFlag(fbEntityNo)

    def onCancelJoinNewFlag(self, battleID, actID, gbId, roleName):
        """\xb3\xc9\xb9\xa6\xc8\xa1\xcf\xfb\xb1\xa8\xc3\xfb"""
        gamelog.debug('@zmk onCancelJoinNewFlag', battleID, actID, gbId, roleName)
        battleData = BFMD.data.get(battleID, {})
        startBattleTimeParts = battleData.get('startBattleTimeParts', ['14:00-14.30',
         '14:30-15:00',
         '21:00-21:30',
         '21:30-22:00'])
        startT, endT = startBattleTimeParts[actID - 1].split('-')
        if self.gbId == gbId:
            self.showGameMsg(battleData.get('onTimingBattleCancelJoinSelfMsgId', '%d%s%s'), (actID, startT, endT))
            self.setNewFlagBattleFieldStatus(battleID, actID, gametypes.NEW_FLAG_BF_STATE_DEFAULT)
            gameglobal.rds.ui.battleOfFortSignUp.show(battleID)
        else:
            self.showGameMsg(battleData.get('onTimingBattleCancleJoinOtherMsgId', '%s%d%s%s'), (roleName,
             actID,
             startT,
             endT))

    def updateBattleFiledQueueNum(self, fbNo, num, bShow):
        """
        \xb8\xfc\xd0\xc2\xd5\xbd\xb3\xa1\xc5\xc5\xb6\xd3\xb6\xd3\xc1\xd0\xd6\xd0\xb5\xc4\xc8\xcb\xca\xfd
        :param fbNo: \xd5\xbd\xb3\xa1\xb8\xb1\xb1\xbe\xba\xc5
        :param num: \xb5\xb1\xc7\xb0\xb6\xd3\xc1\xd0\xd6\xd0\xb5\xc8\xb4\xfd\xb5\xc4\xca\xfd\xc1\xbf
        :param bShow: \xca\xc7\xb7\xf1\xcf\xd4\xca\xbe
        """
        gamelog.debug('@zhangkuo updateBattleFiledQueueNum', fbNo, num, bShow)

    def setBattleFieldPuppetName(self):
        for gbId, info in self.battleFieldTeam.iteritems():
            roleName = info.get('roleName', '')
            splitNames = roleName.split('-')
            if len(splitNames) == 2:
                name, fromHostName = splitNames
                info['roleName'] = name
                info['fromHostName'] = fromHostName

    def onQueryDotaFreeRandomRoleList(self, roleList):
        """
        \xb2\xe9\xd1\xafdota\xc3\xe2\xb7\xd1\xcb\xe6\xbb\xfa\xd3\xa2\xd0\xdb
        :param roleList: \xd3\xa2\xd0\xdb\xc1\xd0\xb1\xed
        """
        gamelog.info('jbx:freeList', roleList)
        self.bfDotaFreeRoleList = roleList
        gameglobal.rds.ui.bfDotaChooseHeroRight.refreshFrame()

    def updateWYSLStage(self, dictStage):
        """
        \xb8\xfc\xd0\xc2\xbb\xee\xb6\xaf\xd7\xb4\xcc\xac\xc1\xd0\xb1\xed
        """
        print '@lyh updateWYSLStage', dictStage

    def setWYSLStageById(self, actId, status):
        """
        \xb8\xfc\xd0\xd0\xc4\xb3\xb8\xf6\xd7\xd3\xbb\xee\xb6\xaf\xd7\xb4\xcc\xac
        """
        print '@lyh setWYSLStageById', actId, status

    def notifyConfirmApplyWYSL(self, actId, gbId, roleName):
        """
        \xb6\xd3\xb3\xa4\xb1\xa8\xc3\xfb  \xb6\xd3\xd4\xb1\xc8\xb7\xc8\xcf
        :param gbId: \xb6\xd3\xb3\xa4gbid
        :param roleName: \xb6\xd3\xb3\xa4\xc3\xfb
        """
        print '@lyh notifyConfirmApplyWYSL', actId, gbId, roleName

    def onConfirmApplyWYSL(self, actId, gbId, isOk):
        """
        \xb1\xa8\xc3\xfb\xca\xc7\xb7\xf1\xb3\xc9\xb9\xa6\xb7\xb4\xc0\xa1
        :param actId: \xbb\xee\xb6\xafID
        :param gbId: \xb6\xd3\xb3\xa4gbid
        :param isOk: \xca\xc7\xb7\xf1\xb3\xc9\xb9\xa6
        """
        print '@lyh onConfirmApplyWYSL', actId, gbId, isOk

    def setWuYinSuLanBattleFieldStatus(self, actId, status):
        """
        \xb1\xa8\xc3\xfb\xd7\xb4\xcc\xac\xce\xac\xbb\xa4
        :param actId: \xbb\xee\xb6\xafID
        :param status: \xb1\xa8\xc3\xfb\xd7\xb4\xcc\xac
        """
        print '@lyh setWuYinSuLanBattleFieldStatus', actId, status

    def onApplyWuYinSuLan(self, actId):
        """
        \xb5\xa5\xc8\xcb\xb1\xa8\xc3\xfb\xb3\xc9\xb9\xa6
        :param actId: \xbb\xee\xb6\xafID
        """
        print '@lyh onApplyWuYinSuLan', actId

    def onConfirmEnterWYSL(self, actId):
        """
        \xbd\xf8\xc8\xeb\xce\xed\xd3\xb0\xcb\xd5\xc0\xbd\xb8\xb1\xb1\xbe
        :param actId: \xbb\xee\xb6\xafID
        """
        print '@lyh onConfirmEnterWYSL', actId

    def onEnterWYSLSucc(self, actId, fbNo):
        """
        \xbd\xf8\xc8\xeb\xce\xed\xd3\xb0\xcb\xd5\xc0\xbd\xb8\xb1\xb1\xbe\xb3\xc9\xb9\xa6
        :param actId: \xbb\xee\xb6\xafID
        :param fbNo: \xb8\xb1\xb1\xbe\xba\xc5
        """
        print '@lyh onEnterWYSLSucc', actId
