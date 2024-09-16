#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impClanChallenge.o
import math
import BigWorld
import const
import gameconfigCommon
import gamelog
import gameglobal
import gametypes
import utils
from item import Item
from guis import uiConst
from guis import generalPushMappings
from guis.clanChallengeProxy import TAB_IDX_CROSS_CLAN_CHALLENGE
from guis import events
from helpers import clanWar
from helpers.clanWar import ReliveBoardVal, BuildingVal
from callbackHelper import Functor
from gamestrings import gameStrings
from data import quest_marker_data as QMD
from data import item_data as ID
from data import chunk_mapping_data as CMD
from data import clan_war_fort_data as CWFD
from data import clan_war_marker_data as CWMD
from data import game_msg_data as GMD
from data import clan_war_challenge_config_data as CWCCD
from data import region_server_config_data as RSCD
from data import cross_clan_war_config_data as CWCFD
from cdata import game_msg_def_data as GMDD
CW_START = 1
CW_END = 2
SHOW_COUNT = [300,
 60,
 30,
 20,
 15,
 10,
 9,
 8,
 7,
 6,
 5,
 4,
 3,
 2,
 1]
COUNT_DOWN_NUM = (5, 4, 3, 2, 1)
ANIMATION_SHOW_COUNT = [15, 10]
START_COUNT = 1
END_COUNT = 2

class ImpClanChallenge(object):

    def getClanChallengeHostId(self):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE and getattr(self, 'clanWarCrossHostId', 0) and self.clanWarCrossHostId != gameglobal.rds.ui.crossClanWar.getGlobalHostId():
            return self.clanWarCrossHostId
        return self.getOriginHostId()

    def notifyClanWarApply(self, tgtHostId):
        """
        :param tgtHostId:
        :return:
        """
        gamelog.info('@zhoukun@CCW, notifyClanWarApply,', tgtHostId)
        self.crossClanWarTgtHostId = tgtHostId
        gameglobal.rds.ui.crossClanWar.refreshInfo()

    def notifyClanWarApplyCross(self, srcHostId, guildName):
        """
        :param srcHostId:
        :param guildName:
        :return:
        """
        gamelog.info('@zhoukun@CCW, notifyClanWarApplyCross,', srcHostId, guildName)

    def onGetClanWarOpenInfo(self, info):
        """
        :param info: [fortCnt, buildingCnt, rank, memberCnt, guildKillCnt, fameScore, killCnt, dmg, cure]
        :return:
        """
        hostId = info[-1]
        info = info[:-1]
        gamelog.info('@zhoukun@CCW, onGetClanWarOpenInfo,', info, hostId)
        if hostId == utils.getHostId():
            self.clanWarHistoryData = info
        else:
            self.crossClanWarHistoryData = info
        gameglobal.rds.ui.crossClanWar.refreshInfo()

    def onGetClanWarGuildStats(self, key, guildKillCnt, hostId):
        """
        :param guildKillCnt:
        :return:
        """
        if hostId != utils.getCurrHostId():
            return
        gamelog.info('@zhoukun@CCW, onGetClanWarGuildStats,', key, guildKillCnt)
        crossClanWarRealTimeInfo = getattr(self, 'crossClanWarRealTimeInfo', {})
        if key == const.CLAN_WAR_STATS_GUILD_KEY_KILL_SCORE:
            crossClanWarRealTimeInfo['guildKillCnt'] = guildKillCnt
        elif key == const.CLAN_WAR_STATS_GUILD_KEY_RECORD_SCORE:
            crossClanWarRealTimeInfo['guildRecordScore'] = guildKillCnt
        self.crossClanWarRealTimeInfo = crossClanWarRealTimeInfo

    def onGetClanWarMemberStats(self, killCnt, dmg, cure):
        """
        :param killCnt:
        :param dmg:
        :param cure:
        :return:
        """
        gamelog.info('@zhoukun@CCW, onGetClanWarMemberStats,', killCnt, dmg, cure)
        crossClanWarRealTimeInfo = getattr(self, 'crossClanWarRealTimeInfo', {})
        crossClanWarRealTimeInfo['killCnt'] = killCnt
        crossClanWarRealTimeInfo['dmg'] = dmg
        crossClanWarRealTimeInfo['cure'] = cure
        self.crossClanWarRealTimeInfo = crossClanWarRealTimeInfo

    def onGetClanWarMemberFameStats(self, fameScore):
        """
        :param fameScore:
        :return:
        """
        gamelog.info('@zhoukun@CCW, onGetClanWarMemberFameStats,', fameScore)
        crossClanWarRealTimeInfo = getattr(self, 'crossClanWarRealTimeInfo', {})
        crossClanWarRealTimeInfo['fameScore'] = fameScore
        self.crossClanWarRealTimeInfo = crossClanWarRealTimeInfo

    def isInCrossClanWarStatus(self):
        return self._isSoul() and self.crossServerGoal == gametypes.SOUL_OUT_GOAL_CROSS_CLAN_WAR

    def onGetOccupyInfoOnEnd(self, data, hostId):
        """
        :param data: [(fortId, guildNuid, guildName, guildFlag, fortOwnerClanNUID, hostId),...]
        :param hostId:
        :return:
        """
        gamelog.info('jbx:onGetOccupyInfoOnEnd', data, hostId)
        self.globalClanWarEndData = (data, hostId)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GLOBAL_CLAN_WAR, {'click': self.showGlobalClanWarOccupy})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GLOBAL_CLAN_WAR)

    def showGlobalClanWarOccupy(self):
        globalClanWarEndData = getattr(self, 'globalClanWarEndData', None)
        if not globalClanWarEndData:
            return
        else:
            gameglobal.rds.ui.crossClanWar.showClanWarResult = True
            self.onGetFortOccupyInfo(*globalClanWarEndData)
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GLOBAL_CLAN_WAR)
            return

    def onRegistCallServiceSuccAfterCheckCanEnter(self):
        gamelog.info('@zhoukun@CCW, onRegistCallServiceSuccAfterCheckCanEnter,')
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GLOBAL_CLAN_WAR_ENTER, {'click': self.globalClanWarEnterConfirm})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GLOBAL_CLAN_WAR_ENTER)
        self.globalClanWarEnterConfirm()

    def globalClanWarEnterConfirm(self):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(GMD.data.get(GMDD.data.GLOBAL_CLAN_WAR_ENTER_CONFIRM, {}).get('text', 'GLOBAL_CLAN_WAR_ENTER_CONFIRM'))

    def onNotifyNormalClanWarEnd(self):
        gamelog.info('jbx:onNotifyNormalClanWarEnd')
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_NORMAL_CLAN_WAR_END, {'click': self.confirmNormalClanWarEnd})
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_NORMAL_CLAN_WAR_END)

    def confirmNormalClanWarEnd(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_NORMAL_CLAN_WAR_END)
        text = GMD.data.get(GMDD.data.CONRIM_NORMAL_CLAN_WAR_END, {}).get('text', 'GMDD.data.CONRIM_NORMAL_CLAN_WAR_END')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(text)

    def onSyncClanWarChallengeStage(self, stage):
        """
        :param stage:
        :return:
        """
        gamelog.info('jbx:onSyncClanWarChallengeStage', stage)
        oldState = getattr(self, 'clanWarChallengeState', 0)
        self.localClanWarChallengeState = stage
        if stage == const.CLAN_WAR_CHALLENGE_STAGE_PREPARE:
            self.cell.queryClanWarChallengeBaseInfo(self.getClanChallengeHostId())
        elif oldState == const.CLAN_WAR_CHALLENGE_STAGE_PREPARE and stage > const.CLAN_WAR_CHALLENGE_STAGE_PREPARE:
            if not getattr(self, 'clanChallengeMemberInfo', {}):
                self.cell.queryClanWarChallengeAllMemberInfo(self.getClanChallengeHostId())
        elif not stage:
            self.localClanChallengeCombatResult = {}
            self.localClanChallengeMemberInfo = {}
            self.localClanChallengeMemberDetail = {}
            self.localClanWarChallengeBaseInfo = {}
            self.localTargetChallengeGuild = {}
            self.crossClanChallengeCombatResult = {}
            self.crossClanChallengeMemberInfo = {}
            self.crossClanChallengeMemberDetail = {}
            self.crossClanWarChallengeBaseInfo = {}
            self.crossTargetChallengeGuild = {}
        gameglobal.rds.ui.clanChallenge.refreshClanChallenge()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GENERAL_PUSH_STATECHANGE, (generalPushMappings.GENERAL_PUSH_CLAN_CHALLENGE, stage))
        if stage > const.CLAN_WAR_CHALLENGE_STAGE_COMBAT_ROUND1:
            self.cell.queryClanWarChallengeAllCombatInfo(self.getClanChallengeHostId())

    def get_clanChallengeCombatResult(self):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            return self.crossClanChallengeCombatResult
        else:
            return self.localClanChallengeCombatResult

    def set_clanChallengeCombatResult(self, value):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            self.crossClanChallengeCombatResult = value
        else:
            self.localClanChallengeCombatResult = value

    clanChallengeCombatResult = property(get_clanChallengeCombatResult, set_clanChallengeCombatResult, '', '')

    def get_ClanWarChallengeState(self):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            return self.crossClanWarChallengeState
        else:
            return self.localClanWarChallengeState

    def set_ClanWarChallengeState(self, value):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            self.crossClanWarChallengeState = value
        else:
            self.localClanWarChallengeState = value

    clanWarChallengeState = property(get_ClanWarChallengeState, set_ClanWarChallengeState, '', '')

    def get_clanChallengeMemberInfo(self):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            return self.crossClanChallengeMemberInfo
        else:
            return self.localClanChallengeMemberInfo

    def set_clanChallengeMemberInfo(self, value):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            self.crossClanChallengeMemberInfo = value
        else:
            self.localClanChallengeMemberInfo = value

    clanChallengeMemberInfo = property(get_clanChallengeMemberInfo, set_clanChallengeMemberInfo, '', '')

    def get_clanChallengeMemberDetail(self):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            return self.crossClanChallengeMemberDetail
        else:
            return self.localClanChallengeMemberDetail

    def set_clanChallengeMemberDetail(self, value):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            self.crossClanChallengeMemberDetail = value
        else:
            self.localClanChallengeMemberDetail = value

    clanChallengeMemberDetail = property(get_clanChallengeMemberDetail, set_clanChallengeMemberDetail, '', '')

    def get_clanWarChallengeBaseInfo(self):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            return self.crossClanWarChallengeBaseInfo
        else:
            return self.localClanWarChallengeBaseInfo

    def set_clanWarChallengeBaseInfo(self, value):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            self.crossClanWarChallengeBaseInfo = value
        else:
            self.localClanWarChallengeBaseInfo = value

    clanWarChallengeBaseInfo = property(get_clanWarChallengeBaseInfo, set_clanWarChallengeBaseInfo, '', '')

    def get_TargetChallengeGuild(self):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            return self.crossTargetChallengeGuild
        else:
            return self.localTargetChallengeGuild

    def set_TargetChallengeGuild(self, value):
        if gameglobal.rds.ui.clanChallenge.tabIdx == TAB_IDX_CROSS_CLAN_CHALLENGE:
            self.localTargetChallengeGuild = value
        else:
            self.crossTargetChallengeGuild = value

    targetChallengeGuild = property(get_TargetChallengeGuild, set_TargetChallengeGuild, '', '')

    def onQueryClanWarChallengeBaseInfo(self, data, hostId, stage):
        """
        :param data:
        # if stage <= const.CLAN_WAR_CHALLENGE_STAGE_APPLY:
        # data = [[fortId, ownerHost, ownerGuildNUID, ownerGuildName, ownerGuildFlag, [applyGuild1, applyGuild2, ...], [(nuid, name, prestige, isReApply, isEnemy, isUseItem, tWhen),...]],...]
        # if stage > const.CLAN_WAR_CHALLENGE_STAGE_APPLY:
        # data = [[fortId, ownerHost, ownerGuildNUID, ownerGuildName, ownerGuildFlag, challengeGuildNUID, challengeGuildName],...]
        :return:
        """
        if not self.guild:
            BigWorld.callback(1, Functor(self.onQueryClanWarChallengeBaseInfo, data, hostId, stage))
            return
        if hostId and hostId != self.getOriginHostId():
            self.crossClanWarChallengeState = stage
            self.crossClanWarChallengeBaseInfo = {}
            self.crossTargetChallengeGuild = {}
        else:
            self.localClanWarChallengeBaseInfo = {}
            self.localTargetChallengeGuild = {}
        gamelog.info('jbx:onQueryClanWarChallengeBaseInfo', data, hostId, stage)
        for fortInfo in data:
            self.processFortInfo(fortInfo, hostId, stage)

        gameglobal.rds.ui.clanChallenge.refreshInfo()

    def getClanWarChallengeBaseInfo(self, fortId):
        clanWarChallengeBaseInfo = getattr(self, 'clanWarChallengeBaseInfo', {})
        return clanWarChallengeBaseInfo.get(fortId, [])

    def processFortInfo(self, fortInfo, hostId = 0, clanWarChallengeState = None):
        fortInfo = list(fortInfo)
        if clanWarChallengeState == None:
            clanWarChallengeState = self.clanWarChallengeState
        if hostId and hostId != self.getOriginHostId():
            clanWarChallengeBaseInfo = self.crossClanWarChallengeBaseInfo
            targetChallengeGuild = self.crossTargetChallengeGuild
        else:
            clanWarChallengeBaseInfo = self.localClanWarChallengeBaseInfo
            targetChallengeGuild = self.localTargetChallengeGuild
        if clanWarChallengeState <= const.CLAN_WAR_CHALLENGE_STAGE_APPLY:
            fortInfo[-1].sort(cmp=self.cmpChallengeGuild)
            if targetChallengeGuild.has_key(fortInfo[0]):
                targetChallengeGuild.pop(fortInfo[0])
            for nuid in fortInfo[-2]:
                if nuid == self.guild.nuid:
                    targetChallengeGuild[fortInfo[0]] = fortInfo[3]
                    break

        elif clanWarChallengeState > const.CLAN_WAR_CHALLENGE_STAGE_APPLY:
            fortId, hostId, ownerGuildNUID, ownerGuildName, ownerGuildFlag, challengeNUID, challengeGuildName = fortInfo
            if targetChallengeGuild.has_key(fortId):
                targetChallengeGuild.pop(fortId)
            if ownerGuildNUID and challengeNUID and (ownerGuildNUID == self.guild.nuid or challengeNUID == self.guild.nuid):
                targetChallengeGuild[fortId] = ownerGuildName
        clanWarChallengeBaseInfo[fortInfo[0]] = fortInfo

    def getWeightedPrestige(self, infoA):
        nuidA, nameA, prestigeA, isReApplyA, isEnemyA, isUseItemA, tWhenA = infoA
        percent = 1.0
        if isReApplyA:
            percent = percent * CWCCD.data.get('prestigeReduceRatio', 0.5)
        if isEnemyA:
            percent = percent * CWCCD.data.get('prestigeEnhanceRatio', 1.2)
        return percent

    def cmpChallengeGuild(self, infoA, infoB):
        if infoA[5] and not infoB[5]:
            return -1
        if not infoA[5] and infoB[5]:
            return 1
        prestigeA = infoA[2] * self.getWeightedPrestige(infoA)
        prestigeB = infoB[2] * self.getWeightedPrestige(infoB)
        if prestigeA != prestigeB:
            return int(math.ceil(prestigeB - prestigeA))
        return infoA[6] - infoB[6]

    def getClanChallengeMeberDetail(self, gbId):
        clanChallengeMemberDetail = getattr(self, 'clanChallengeMemberDetail', {})
        return clanChallengeMemberDetail.get(gbId, None)

    def queryClanWarChallengeMemberInfo(self, fortId):
        if getattr(self, 'clanWarChallengeState', None) == const.CLAN_WAR_CHALLENGE_STAGE_APPLY:
            return
        else:
            self.cell.queryClanWarChallengeMemberInfo(fortId, self.getClanChallengeHostId())
            return

    def tryGetClanWarChallengeMemberInfo(self, fortId):
        if fortId and not getattr(self, 'clanChallengeMemberInfo', {}).has_key(fortId):
            self.queryClanWarChallengeMemberInfo(fortId)

    def onQueryClanWarChallengeMemberInfo(self, memberInfo, hostId, stage):
        """
        :param data:
        # data = [fortId, commander, member={}, layout=[[0,0,0,0,0], [0,0,0], [0], [0,0,0], [0,0,0,0,0]]]
        :return:
        """
        gamelog.info('jbx:onQueryClanWarChallengeMemberInfo', memberInfo)
        if hostId and hostId != self.getOriginHostId():
            clanChallengeMemberInfo = self.crossClanChallengeMemberInfo
            clanChallengeMemberDetail = self.crossClanChallengeMemberDetail
            self.crossClanWarChallengeState = stage
        else:
            clanChallengeMemberInfo = self.localClanChallengeMemberInfo
            clanChallengeMemberDetail = self.localClanChallengeMemberDetail
        clanChallengeMemberInfo[memberInfo[0]] = memberInfo
        clanChallengeMemberDetail.update(memberInfo[2])
        gameglobal.rds.ui.clanChallengeSet.refreshInfo()
        gameglobal.rds.ui.clanChallengeResult.refreshInfo()
        gameglobal.rds.ui.clanChallenge.refreshClanChallenge()

    def onQueryClanWarChallengeAllMemberInfo(self, data, hostId, stage):
        """
        :param data: [[fortId, commander, member={}, layout=[[0,0,0,0,0], [0,0,0], [0], [0,0,0], [0,0,0,0,0]]], ...]
        :return:
        """
        if hostId and hostId != self.getOriginHostId():
            clanChallengeMemberInfo = self.crossClanChallengeMemberInfo
            clanChallengeMemberDetail = self.crossClanChallengeMemberDetail
            self.crossClanWarChallengeState = stage
        else:
            clanChallengeMemberInfo = self.localClanChallengeMemberInfo
            clanChallengeMemberDetail = self.localClanChallengeMemberDetail
        clanChallengeMemberInfo.clear()
        clanChallengeMemberDetail.clear()
        for memberInfo in data:
            clanChallengeMemberInfo[memberInfo[0]] = memberInfo
            clanChallengeMemberDetail.update(memberInfo[2])

        gameglobal.rds.ui.clanChallengeSet.refreshInfo()
        gameglobal.rds.ui.clanChallengeResult.refreshInfo()
        gameglobal.rds.ui.clanChallenge.refreshClanChallenge()
        gamelog.info('jbx:onQueryClanWarChallengeAllMemberInfo', data)

    def isMemberInClanWarChallenge(self, gbId):
        for memberInfo in getattr(self, 'clanChallengeMemberInfo', {}).values():
            if gbId in memberInfo[2]:
                return True

        return False

    def isClanChallengeCommander(self, fortId):
        return getattr(self, 'clanChallengeMemberInfo', {}).has_key(fortId) and self.clanChallengeMemberInfo[fortId][1] == self.gbId

    def onQueryClanWarChallengeCombatInfo(self, info, hostId, stage):
        """
        :param data: \xe5\xb7\xb2\xe7\xbb\x93\xe6\x9d\x9f\xe7\x9a\x84\xe5\xb8\x83\xe5\xb1\x80\xe5\x8f\x8a\xe7\xbb\x93\xe6\x9e\x9c
        # data = [fortId, ownerGuildNUID, ownerCommanderGbId, ownerLayoutGbId=[[0,0,0,0,0], [0,0,0]], challengeGuildNUID, challengeCommanderGbId, challengeLayoutGbId=[[0,0,0,0,0], [0,0,0]], winGuildNUID=[0,0], tStart],
        :return:
        """
        gamelog.info('jbx:onQueryClanWarChallengeCombatInfo', info)
        if not info:
            return
        if hostId and hostId != self.getOriginHostId():
            clanChallengeCombatResult = self.crossClanChallengeCombatResult
            self.crossClanWarChallengeState = stage
        else:
            clanChallengeCombatResult = self.localClanChallengeCombatResult
        clanChallengeCombatResult[info[0]] = info
        if utils.getNow() - gameglobal.rds.ui.clanChallengeResult.showResult < 2:
            gameglobal.rds.ui.clanChallengeResult.show(info[0])
            gameglobal.rds.ui.clanChallengeResult.showResult = 0
        else:
            gameglobal.rds.ui.clanChallengeResult.refreshInfo()

    def onQueryClanWarChallengeAllCombatInfo(self, data, hostId, stage):
        """
        :param data: [[fortId, ownerGuildNUID, ownerCommanderGbId, ownerLayoutGbId=[[0,0,0,0,0], [0,0,0]], challengeGuildNUID, challengeCommanderGbId, challengeLayoutGbId=[[0,0,0,0,0], [0,0,0]], winGuildNUID=[0,0], tStart], ...]
        :param hostId:
        :return:
        """
        gamelog.info('jbx:onQueryClanWarChallengeAllCombatInfo', data, hostId)
        if hostId and hostId != self.getOriginHostId():
            clanChallengeCombatResult = self.crossClanChallengeCombatResult
            self.crossClanWarChallengeState = stage
        else:
            clanChallengeCombatResult = self.localClanChallengeCombatResult
        clanChallengeCombatResult.clear()
        for info in data:
            if info:
                clanChallengeCombatResult[info[0]] = info

        gameglobal.rds.ui.clanChallenge.refreshClanChallenge()
        gameglobal.rds.ui.clanChallengeResult.refreshInfo()

    def onQueryClanWarChallengeObserveInfo(self, data):
        """
        :param data: [[self.fortId, self.ownerGuild.nuid, self.ownerGuild.name, self.ownerGuild.member, self.ownerGuild.layout[nRound], self.challengeGuild.nuid, self.challengeGuild.name, self.challengeGuild.member, self.challengeGuild.layout[nRound], utils.getHostId()], ...]
        :return:
        """
        gamelog.info('jbx:onQueryClanWarChallengeObserveInfo', data)
        self.clanChallengeObData = data
        gameglobal.rds.ui.clanChallengeObList.refreshInfo()

    def onApplyClanWarChallenge(self, data):
        """
        :param data:
        # data = [fortId, ownerGuildHost, ownerGuildNUID, ownerGuildName, ownerGuildFlag, [applyGuild1, applyGuild2, ...], [(nuid, name, prestige, isReApply, isEnemy, isUseItem, tWhen),...]]
        :return:
        """
        gamelog.info('jbx:onApplyClanWarChallenge', data)
        self.processFortInfo(data)
        gameglobal.rds.ui.clanChallenge.refreshClanChallenge()

    def onCancelApplyClanWarChallenge(self, data):
        """
        :param data:
        # data = [[fortId, ownerGuildHost, ownerGuildNUID, ownerGuildName, ownerGuildFlag, [applyGuild1, applyGuild2, ...], [(nuid, name, prestige, isReApply, isEnemy, isUseItem, tWhen),...]], ...]
        :return:
        """
        gamelog.info('jbx:onCancelApplyClanWarChallenge', data)
        for fortInfo in data:
            self.processFortInfo(fortInfo)

        gameglobal.rds.ui.clanChallenge.refreshInfo()

    def onSetClanWarChallengeCommander(self, fortId, commanderGbId, tgtHostId):
        """
        :param fortId:
        :param commanderGbId:
        :return:
        """
        if tgtHostId and tgtHostId != self.getOriginHostId():
            clanChallengeMemberInfo = self.crossClanChallengeMemberInfo
        else:
            clanChallengeMemberInfo = self.localClanChallengeMemberInfo
        if clanChallengeMemberInfo.has_key(fortId):
            clanChallengeMemberInfo[fortId][1] = commanderGbId
        gamelog.info('jbx:onSetClanWarChallengeCommander, fortId, guildNUID, commanderGbId', fortId, commanderGbId)
        gameglobal.rds.ui.clanChallenge.refreshInfo()
        gameglobal.rds.ui.clanChallengeSet.refreshInfo()

    def onAddClanWarChallengeMember(self, fortId, member, tgtHostId):
        """
        :param fortId:
        :param guildNUID:
        :param member: set()
        :return:
        """
        gamelog.info('jbx:onAddClanWarChallengeMember', fortId, member)
        if tgtHostId and tgtHostId != self.getOriginHostId():
            clanChallengeMemberInfo = self.crossClanChallengeMemberInfo
        else:
            clanChallengeMemberInfo = self.localClanChallengeMemberInfo
        if clanChallengeMemberInfo.has_key(fortId):
            clanChallengeMemberInfo[fortId][2] = member
        gameglobal.rds.ui.clanChallengeSet.refreshInfo()

    def onRemoveClanWarChallengeMember(self, fortId, member, layout, tgtHostId):
        """
        :param fortId:
        :param guildNUID:
        :param member: set()
        :param layout: [[0,0,0,0,0], [0,0,0], [0], [0,0,0], [0,0,0,0,0]]]
        :return:
        """
        gamelog.info('jbx:onRemoveClanWarChallengeMember', fortId, member, layout)
        if tgtHostId and tgtHostId != self.getOriginHostId():
            clanChallengeMemberInfo = self.crossClanChallengeMemberInfo
        else:
            clanChallengeMemberInfo = self.localClanChallengeMemberInfo
        if clanChallengeMemberInfo.has_key(fortId):
            clanChallengeMemberInfo[fortId][2] = member
            clanChallengeMemberInfo[fortId][3] = layout
        gameglobal.rds.ui.clanChallengeSet.refreshInfo()

    def onSetClanWarChallengeLayout(self, fortId, layout, tgtHostId):
        """
        :param fortId:
        :param guildNUID:
        :param layout: [[0,0,0,0,0], [0,0,0], [0], [0,0,0], [0,0,0,0,0]]]
        :return:
        """
        gamelog.info('jbx:onSetClanWarChallengeLayout', fortId, layout)
        if tgtHostId and tgtHostId != self.getOriginHostId():
            clanChallengeMemberInfo = self.crossClanChallengeMemberInfo
        else:
            clanChallengeMemberInfo = self.localClanChallengeMemberInfo
        if clanChallengeMemberInfo.has_key(fortId):
            clanChallengeMemberInfo[fortId][3] = layout
        gameglobal.rds.ui.clanChallengeSet.refreshInfo()

    def onSyncClanWarChallengeInspireInfo(self, inspireCnt):
        """
        :param inspireCnt:
        :return:
        """
        gamelog.info('jbx:onSyncClanWarChallengeInspireInfo', inspireCnt)
        oldValue = getattr(self, 'clanChallengeInspireCnt', 0)
        self.clanChallengeInspireCnt = inspireCnt
        gameglobal.rds.ui.bFGuildTournamentObserve.refreshClanWarChallengeInspreInfo(inspireCnt, oldValue)

    def onInviteAddClanWarChallengeMember(self, fortId, hostId):
        """
        :param fortId:
        :return:
        """
        gamelog.info('jbx:onInviteAddClanWarChallengeMember', fortId)
        fortName = CWFD.data.get(fortId, {}).get('showName', '')
        serverName = RSCD.data.get(hostId, {}).get('serverName', '')
        msg = GMD.data.get(GMDD.data.CLAN_CHALLENGE_INVITE, {}).get('text', 'GMDD.data.CLAN_CHALLENGE_INVITE %s,%s') % (serverName, fortName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.confirmAddClanWarChallengeMember, fortId, hostId), repeat=CWCCD.data.get('inviteConfirmCounter', 60), repeatText=gameStrings.CLAN_CHALLENGE_REPEAT, noCallback=Functor(self.cell.cancelAddClanWarChallengeMember, fortId, hostId))

    def onClanWarChallengeCombatStart(self, nRound, hostId):
        """
        :param nRound: \xe8\xbd\xae\xe6\xac\xa1
        :return:
        """
        gamelog.info('jbx:onClanWarChallengeCombatStart', nRound)
        msg = GMD.data.get(GMDD.data.ENTER_CLAN_CHALLENGE_COFNIRM, {}).get('text', 'GMDD.data.ENTER_CLAN_CHALLENGE_COFNIRM%d') % (nRound + 1)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.enterClanWarChallenge, hostId), repeat=CWCCD.data.get('combatStartConfirmCounter', 60), repeatText=gameStrings.CLAN_CHALLENGE_REPEAT, countDownFunctor=Functor(self.cell.enterClanWarChallenge, hostId))

    def onSyncClanWarRecordScoreRank(self, data, hostId):
        """
        :param data: [(nuid, score), ...]
        :param hostId:
        :return:
        """
        gamelog.info('jbx:onSyncClanWarRecordScoreRank', data, hostId)
        crossClanWarRealTimeInfo = getattr(self, 'crossClanWarRealTimeInfo', {})
        crossClanWarRealTimeInfo.pop('guildRecordRank', None)
        data.sort(cmp=lambda a, b: cmp(a[1], b[1]), reverse=True)
        for rankIdx, scoreInfo in enumerate(data):
            guildNuid, score = scoreInfo
            if guildNuid == self.guildNUID:
                crossClanWarRealTimeInfo['guildRecordRank'] = str(rankIdx + 1)
                crossClanWarRealTimeInfo['guildRecordScore'] = str(score)

        self.crossClanWarRealTimeInfo = crossClanWarRealTimeInfo

    def onQueryClanWarAddEvent(self, data):
        """
        :param data:[(scoreAdd + scoreLimit, self.prestige, fortIds, utils.getNow()), ...]
        :return:
        """
        gamelog.info('yedawang### onQueryClanWarEvent', data)
        gameglobal.rds.ui.clanWarIncident.setAddEventData(data)

    def onQueryClanWarLimitEvent(self, data):
        """
        :param data: [(nuid, name, host, time), ...]
        :return:
        """
        gamelog.info('yedawang### onQueryClanWarEvent', data)
        gameglobal.rds.ui.clanWarIncident.setLimitEventData(data)

    def inGlobalClanWarTime(self):
        if not gameconfigCommon.enableGlobalClanWar():
            return False
        return utils.inCrontabRange(CWCFD.data.get('globalStartTime', ''), CWCFD.data.get('globalEndTime', ''))
