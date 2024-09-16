#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impGuildTournament.o
from gamestrings import gameStrings
import gameglobal
import const
import gametypes
import BigWorld
import formula
import gamelog
from guis import uiUtils
from helpers import tournament
from guis import uiConst
from callbackHelper import Functor
from helpers.tournament import TournamentRankVal
from cdata import game_msg_def_data as GMDD
from cdata import rank_guild_tournament_star_data as RGTSD
from data import guild_config_data as GCD

class ImpGuildTournament(object):

    def onQueryGuildTournament(self, groupId, data, ver):
        guild, matches, nextCandidateGuildNUIDs, state, roundNum, seedGuildNUIDs, trainingState, trainingMatches = data
        t = self.guildTournament[groupId]
        t.guild = guild
        t.matches = matches
        if len(t.matches) <= const.GUILD_TOURNAMENT_MAX_ROUND:
            t.matches.append(nextCandidateGuildNUIDs)
        t.seedGuildNUIDs = seedGuildNUIDs
        t.state = state
        t.roundNum = roundNum
        t.trainingState = trainingState
        t.ver = ver
        if gameglobal.rds.configData.get('enableWWGuildTournament', False):
            gameglobal.rds.ui.guildWWTournamentResult.refreshPanel()
        else:
            gameglobal.rds.ui.guildTournamentResult.refreshInfo(groupId)
        gameglobal.rds.ui.guildMatch.refreshInfo(groupId)

    def onQueryGuildTournamentKeep(self, groupId):
        pass

    def onQueryGuildTournamentRanks(self, groupId, data, ver):
        ranks = []
        for i, (guildNUID, guildName, score, totalScore) in enumerate(data):
            ranks.append(TournamentRankVal(rank=i + 1, guildNUID=guildNUID, guildName=guildName, score=score, totalScore=totalScore))

        t = self.guildTournament[groupId]
        t.ranks = ranks
        t.rankVer = ver
        gameglobal.rds.ui.guildTournamentRank.refreshInfo(groupId)
        if gameglobal.rds.configData.get('enableGuildTournamentSeason', False):
            gameglobal.rds.ui.guildWWTournamentRank.show(groupId)

    def onQueryGuildTournamentRanksKeep(self, groupId):
        if gameglobal.rds.configData.get('enableGuildTournamentSeason', False):
            gameglobal.rds.ui.guildWWTournamentRank.show(groupId)

    def onQueryWWGuildTournamentRanks(self, groupId, data, forUse, ver):
        ranks = []
        for i, (guildNUID, guildName) in enumerate(data):
            ranks.append(TournamentRankVal(rank=i + 1, guildNUID=guildNUID, guildName=guildName))

        t = self.guildTournament[groupId]
        t.ranks = ranks
        t.rankVer = ver
        if forUse == gametypes.GUILD_TOURNAMENT_QUERY_FOR_RANK:
            gameglobal.rds.ui.guildWWTournamentRank.show(groupId)
        elif forUse == gametypes.GUILD_TOURNAMENT_QUERY_FOR_RESULT:
            gameglobal.rds.ui.guildWWTournamentResult.show(groupId)

    def onQueryWWGuildTournamentRanksKeep(self, groupId):
        gameglobal.rds.ui.guildWWTournamentRank.show(groupId)

    def onQueryGuildTournamentSimple(self, data):
        for i, (mixed, appliedSeedNum, state, simpleVer, trainingState, trainingAppliesByNuid) in enumerate(data):
            groupId = i + 1
            t = self.guildTournament[groupId]
            t.isSeed = False
            t.hasApplied = False
            t.canEnter = False
            for subGroupId, (isSeed, hasApplied, canEnter, isInMatches) in enumerate(mixed):
                subGroup = t.getSubGroup(subGroupId)
                subGroup.isSeed = isSeed
                subGroup.hasApplied = hasApplied
                subGroup.canEnter = canEnter
                subGroup.isInMatches = isInMatches
                if isSeed:
                    t.isSeed = True
                if hasApplied:
                    t.hasApplied = True
                if canEnter:
                    t.canEnter = True
                if isInMatches:
                    t.isInMatches = True

            t.appliedSeedNum = appliedSeedNum
            t.state = state
            t.simpleVer = simpleVer
            t.trainingState = trainingState
            t.trainingAppliesByNuid = trainingAppliesByNuid

        if gameglobal.rds.configData.get('enableWWGuildTournament', False):
            gameglobal.rds.ui.guild.refreshWWTournamentInfo()
            gameglobal.rds.ui.guildWWTournamentResult.refreshPanel()
        else:
            gameglobal.rds.ui.guild.refreshTournamentInfo()
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
            gameglobal.rds.ui.bFGuildTournamentLive.showPanel()

    def onQueryGuildTournamentSimpleKeep(self):
        pass

    def onQueryNgtApply(self, isJoined, groupId):
        gamelog.debug('dxk@onQueryNgtApply', isJoined, groupId)
        t = self.crossRankGtn[groupId]
        t.hasApplied = isJoined
        if gameglobal.rds.configData.get('enableWWGuildTournament', False):
            gameglobal.rds.ui.guild.refreshWWTournamentInfo()
        self.checkPushNGTNApplyPush()

    def onNotifyGuildNgtStart(self, groupId):
        gamelog.debug('dxk@onNotifyGuildNgtStart', groupId)
        if self.lv > 60:
            self.notifyGuildNgtStartFlag = True
            gameglobal.rds.ui.guild.getRankTournamentSimpleInfo()

    def onSyncNgtStateToClient(self, state):
        gamelog.debug('dxk@onSyncNgtStateToClient', state)
        self.NgtState = state
        for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
            self.crossRankGtn[groupId].state = state

        gameglobal.rds.ui.guild.getRankTournamentSimpleInfo()

    def onApplyGuildTournament(self, groupId):
        t = self.guildTournament[groupId]
        t.hasApplied = True
        self.checkPushNGTNApplyPush()
        if gameglobal.rds.configData.get('enableWWGuildTournament', False):
            gameglobal.rds.ui.guild.getTournamentSimpleInfo()
            gameglobal.rds.ui.guild.refreshWWTournamentInfo()
        else:
            gameglobal.rds.ui.guild.refreshTournamentInfo()

    def onGuildTournamentBFNotify(self, groupId, bCross = False):
        if bCross:
            if groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CROSS_GTN_BF_NOTIFY_QL)
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_CROSS_GTN_BF_NOTIFY_QL, {'click': Functor(self.showBF, groupId, bCross)})
            elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CROSS_GTN_BF_NOTIFY_BH)
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_CROSS_GTN_BF_NOTIFY_BH, {'click': Functor(self.showBF, groupId, bCross)})
        elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_BF_NOTIFY_QL)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_BF_NOTIFY_QL, {'click': Functor(self.showBF, groupId, bCross)})
        elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_BF_NOTIFY_BH)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_BF_NOTIFY_BH, {'click': Functor(self.showBF, groupId, bCross)})

    def queryGuildTournamentSimple(self):
        guildTournamentQL = self.guildTournament.get(gametypes.GUILD_TOURNAMENT_GROUP_QL)
        guildTournamentBH = self.guildTournament.get(gametypes.GUILD_TOURNAMENT_GROUP_BH)
        if guildTournamentQL != None and guildTournamentBH != None:
            self.cell.queryGuildTournamentSimple(guildTournamentQL.simpleVer, guildTournamentBH.simpleVer)

    def showBF(self, groupId, bCross):
        if bCross:
            if groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_CROSS_GTN_BF_NOTIFY_QL)
            elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_CROSS_GTN_BF_NOTIFY_BH)
            else:
                return
        elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_BF_NOTIFY_QL)
        elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_BF_NOTIFY_BH)
        else:
            return
        if bCross:
            gameglobal.rds.ui.guild.showAssignTab(uiConst.GUILDINFO_TAB_CROSS_TOURNAMENT)
        else:
            gameglobal.rds.ui.guild.showAssignTab(uiConst.GUILDINFO_TAB_TOURNAMENT)

    def onGuildTournamentSeedApplyNotify(self, groupId):
        if groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_SEED_APPLY_QL)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_SEED_APPLY_QL, {'click': Functor(self.showSeedApply, groupId)})
        elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_SEED_APPLY_BH)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_SEED_APPLY_BH, {'click': Functor(self.showSeedApply, groupId)})

    def showSeedApply(self, groupId):
        if groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_SEED_APPLY_QL)
        elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_SEED_APPLY_BH)
        else:
            return
        gameglobal.rds.ui.guild.showAssignTab(uiConst.GUILDINFO_TAB_TOURNAMENT)

    def onGuildTournamentRoundEnd(self, groupId, roundNum):
        if groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_ROUND_END_QL)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_ROUND_END_QL, {'click': Functor(self.showRoundEnd, groupId)})
        elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_ROUND_END_BH)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_ROUND_END_BH, {'click': Functor(self.showRoundEnd, groupId)})

    def showRoundEnd(self, groupId):
        p = BigWorld.player()
        if groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_ROUND_END_QL)
        elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_TOURNAMENT_ROUND_END_BH)
        else:
            return
        if gameglobal.rds.configData.get('enableWWGuildTournament', False):
            tournamentResult = p.worldWar.tournamentResult
            p.cell.queryWWTournament(groupId, tournamentResult.groupVer[groupId], tournamentResult.guildVer)
            gameglobal.rds.ui.guildWWTournamentResult.readyToShow()
        else:
            gameglobal.rds.ui.guildTournamentResult.show(groupId)

    def onQueryCrossGtnKeep(self, groupId):
        pass

    def onQueryCrossGtn(self, groupId, dto, ver):
        t = self.crossGtn[groupId]
        t.fromDTO(dto)
        t.ver = ver
        gameglobal.rds.ui.guildCrossTResult.refreshInfo(groupId)
        gameglobal.rds.ui.guildCrossTFinalResult.refreshInfo(groupId)
        gameglobal.rds.ui.guildCrossScoreTResult.onQueryCrossGtn(groupId)

    def onQueryCrossGtnSimpleKeep(self):
        pass

    def onQueryCGTNMode(self, mode):
        self.crossGTNMode = mode

    def isInCrossGuildTournamentCirCular(self):
        return getattr(self, 'crossGTNMode', 0) == gametypes.CROSS_GUILD_TOURNAMENT_CIRCULAR

    def onQueryCrossGtnSimple(self, data):
        for i, (isCandidate, canEnter, state, simpleVer) in enumerate(data):
            groupId = i + 1
            t = self.crossGtn[groupId]
            t.isCandidate = isCandidate
            t.canEnter = canEnter
            t.state = state
            t.simplerVer = simpleVer

        gameglobal.rds.ui.guild.refreshCrossTournamentInfo()

    def queryNewGuildTournamentSimple(self):
        guildTournamentQL = self.crossRankGtn.get(gametypes.GUILD_TOURNAMENT_GROUP_QL)
        guildTournamentBH = self.crossRankGtn.get(gametypes.GUILD_TOURNAMENT_GROUP_BH)
        if guildTournamentQL != None and guildTournamentBH != None:
            self.cell.queryNewGuildTournamentSimple(guildTournamentQL.simpleVer, guildTournamentBH.simpleVer)

    def onQueryNewGtnSimpleKeep(self):
        pass

    def onQueryNewGtnSimple(self, data):
        gamelog.debug('dxk@onQueryNewGtnSimple', data)
        for i, (isCandidate, canEnter, state, simpleVer, roundNum) in enumerate(data):
            groupId = i + 1
            t = self.crossRankGtn[groupId]
            t.isCandidate = isCandidate
            t.canEnter = canEnter
            t.state = state
            t.simplerVer = simpleVer
            t.roundNum = roundNum

        self.checkPushNGTNEnterPush()
        gameglobal.rds.ui.guild.refreshWWTournamentInfo()

    def onRequestNgtGuildRankInfo(self, rankInfo):
        gamelog.debug('dxk onRequestNgtGuildRankInfo', rankInfo)
        groupId = rankInfo['groupId']
        t = self.crossRankGtn[groupId]
        t.rank = rankInfo['rank']
        t.groupScore = rankInfo['groupScore']
        t.bonus = rankInfo['bonus']
        gameglobal.rds.ui.guild.refreshRankTournamentInfo()

    def onChooseStrategyReply(self, groupId, groupRoundNum, strategyOne, strategyTwo, fbNo):
        t = self.crossRankGtn[groupId]
        gamelog.debug('dxk onChoose StrategyReply', groupId, groupRoundNum, strategyOne, strategyTwo, fbNo)
        realRound = groupRoundNum + 1
        if t.matchInfo.has_key(realRound):
            matchInfo = t.matchInfo[realRound]
            matchInfo['strategyOne'] = strategyOne
            matchInfo['strategyTwo'] = strategyTwo
            matchInfo['fbNo'] = fbNo
        gameglobal.rds.ui.guild.refreshRankTournamentInfo()

    def onRequestGuildTournamentBattleInfo(self, battleInfo):
        gamelog.debug('dxk@onRequestGuildTournamentBattleInfo', battleInfo)
        for matchInfo in battleInfo:
            groupId = matchInfo.get('groupId', 0)
            roundNum = matchInfo.get('roundNum', 0)
            if groupId and roundNum:
                t = self.crossRankGtn[groupId]
                t.matchInfo[roundNum] = matchInfo

        gameglobal.rds.ui.guild.refreshWWTournamentInfo()

    def onUpdateTournamentInspirePraiseInfo(self, fbNo, guildNUIDs, subGroupIds, groupId, groupNames, gtInspireMorales, praisesNum, livesNum, tReady):
        """
        \xe5\xa2\x9e\xe5\x8a\xa0\xe7\xbb\x93\xe4\xbc\xb4\xe4\xbc\x99\xe4\xbc\xb4\xe7\x9a\x84\xe6\x88\x90\xe5\x8a\x9f\xe5\x90\x8e\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83
        Args:
            fbNo:\xe5\x8c\xba\xe5\x88\x86\xe6\x88\x98\xe5\x9c\xba
            guildNUIDs:(nuid1,nuid2)
            subGroupInfo:(subgroupId1, subgroupId2),\xe7\x99\xbd\xe8\x99\x8e\xe6\x9c\x892\xe4\xb8\xaa\xe6\x88\x98\xe5\x9c\xbafbNo\xe7\x9b\xb8\xe5\x90\x8c,\xe7\x94\xa8subGroupId\xe5\x8c\xba\xe5\x88\x86\xe4\xb8\x8d\xe5\x90\x8c\xe6\x88\x98\xe5\x9c\xba
            gtInspireMorales:(morale1,morale2)
        Returns:
        
        """
        if self.isInGuildNUIDs(guildNUIDs):
            gameglobal.rds.ui.bFGuildTournamentLive.pushLiveMessage(guildNUIDs, subGroupIds, groupId)
            gameglobal.rds.ui.bFGuildTournamentLive.setInspirePraiseData(fbNo, guildNUIDs, subGroupIds, gtInspireMorales, praisesNum, livesNum, tReady, groupId, groupNames)
        if formula.inGuildTournamentQL(fbNo) or formula.inNewGuildTournmanetFORT(fbNo):
            gameglobal.rds.ui.bFFortInfoV1.setInspirePraiseData(gtInspireMorales, guildNUIDs, praisesNum, livesNum)
        elif formula.inGuildTournamentBH(fbNo) or formula.inNewGuildTournmanetFLAG(fbNo):
            gameglobal.rds.ui.bFFlagStatsV1.setInspirePraiseData(gtInspireMorales, guildNUIDs, praisesNum, livesNum)
        elif formula.inNewGuildTournmanetCQZZ(fbNo):
            pass
        elif formula.inNewGuildTournmanetLYG(fbNo):
            pass

    def isInGuildNUIDs(self, guildNUIDs):
        for guildNUID in guildNUIDs:
            if self.guildNUID == guildNUID:
                return True

        return False

    def onUpdateGtInspireCoolDown(self, coolDownReady):
        gameglobal.rds.ui.bFGuildTournamentLive.setCoolDown(coolDownReady)
        gameglobal.rds.ui.bFGuildTournamentObserve.setCoolDown(coolDownReady)
        gameglobal.rds.ui.guild.refreshGtnInspireCoolDown()

    def onUpdateWatchGtBattleEvent(self, fbNo, subGroupIds, groupId, eventType, eventArgs):
        """
        GUILD_TOURNAMENT_EVENT_AVATAR_COMBAT_KILL = 1 (\xe5\x85\xac\xe4\xbc\x9anuid, \xe8\xa7\x92\xe8\x89\xb2\xe5\x90\x8d\xe5\xad\x97, \xe8\xbf\x9e\xe6\x9d\x80\xe6\xac\xa1\xe6\x95\xb0)
        GUILD_TOURNAMENT_EVENT_OCCUPY_FORT = 2 (\xe5\x85\xac\xe4\xbc\x9anuid, fortId)
        GUILD_TOURNAMENT_EVENT_PLAYER_LANDING_PLANE = 3 (\xe5\x85\xac\xe4\xbc\x9anuid, \xe8\xa7\x92\xe8\x89\xb2\xe5\x90\x8d\xe5\xad\x97)
        GUILD_TOURNAMENT_EVENT_PLANE_DESTROY = 4 (\xe5\x85\xac\xe4\xbc\x9anuid,)
        GUILD_TOURNAMENT_EVENT_FIRE_HURT = 5 (\xe5\x85\xac\xe4\xbc\x9anuid, \xe4\xbc\xa4\xe5\xae\xb3)
        GUILD_TOURNAMENT_EVENT_OCCUPY_FLAG = 6 (\xe5\x85\xac\xe4\xbc\x9anuid, \xe8\xa7\x92\xe8\x89\xb2\xe5\x90\x8d\xe5\xad\x97, flagId\xe8\xa7\x81battle_field_flag_data)
        GUILD_TOURNAMENT_EVENT_HOLD_CQZZ_FLAG = 7 (\xe5\x85\xac\xe4\xbc\x9anuid\xef\xbc\x8c\xe9\x98\xb5\xe8\x90\xa5ID\xef\xbc\x8c \xe7\x8e\xa9\xe5\xae\xb6\xe5\x90\x8d\xe5\xad\x97\xef\xbc\x89 \xe8\x83\x8c\xe6\x97\x97
        GUILD_TOURNAMENT_EVENT_COMMIT_CQZZ_FLAG = 8 \xef\xbc\x88\xe5\x85\xac\xe4\xbc\x9anuid\xef\xbc\x8c \xe9\x98\xb5\xe8\x90\xa5ID\xef\xbc\x8c \xe7\x8e\xa9\xe5\xae\xb6\xe5\x90\x8d\xe5\xad\x97\xef\xbc\x89 \xe4\xba\xa4\xe6\x97\x97
        GUILD_TOURNAMENT_EVENT_PUT_BACK_CQZZ_FLAG = 9 \xef\xbc\x88\xe5\x85\xac\xe4\xbc\x9anuid\xef\xbc\x8c \xe9\x98\xb5\xe8\x90\xa5ID\xef\xbc\x8c \xe7\x8e\xa9\xe5\xae\xb6\xe5\x90\x8d\xe5\xad\x97\xef\xbc\x89\xe6\x94\xbe\xe5\x9b\x9e\xe6\x97\x97\xe5\xb8\x9c
        """
        print 'cgy#onUpdateWatchGtBattleEvent: ', fbNo, subGroupIds, eventType, eventArgs
        gameglobal.rds.ui.bFGuildTournamentLive.setInspirePraiseEventData(fbNo, subGroupIds, eventType, eventArgs, groupId)

    def onGuildTournamentBattleFieldEnd(self, fbNo, subGroupIds, groupId):
        print 'cgy#onGuildTournamentBattleFieldEnd: ', fbNo, subGroupIds
        gameglobal.rds.ui.bFGuildTournamentLive.clearPanel(groupId, subGroupIds)

    def onAddPraiseForBattleFieldSucc(self, fbNo, subGroupId, groupId):
        self.showGameMsg(GMDD.data.BATTLE_FIELD_ADD_PRAISE_SUCC, ())
        gameglobal.rds.ui.bFGuildTournamentLive.disablePraiseBtn(groupId, subGroupId)

    def onGtTrainingApplyNotifycation(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_GUILD_TRAIN_TOURNAMENT)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_GUILD_TRAIN_TOURNAMENT, {'click': self.onClickShowTrainMsg})

    def onClickShowTrainMsg(self):
        msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_TRAIN_TOURNAMENT_APPLY)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.openTrainPanel, isModal=False, msgType='pushLoop', textAlign='center')
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_GUILD_TRAIN_TOURNAMENT)

    def openTrainPanel(self):
        gameglobal.rds.ui.guild.show(uiConst.GUILDINFO_TAB_TOURNAMENT)

    def getGuildRankLevel(self):
        qlRankKey = tournament.getRankStarKey(gametypes.GUILD_TOURNAMENT_GROUP_QL, self.groupScoreQL)
        bhRankKey = tournament.getRankStarKey(gametypes.GUILD_TOURNAMENT_GROUP_BH, self.groupScoreBH)
        qlRankInfo = RGTSD.data.get(qlRankKey, {})
        bhRankInfo = RGTSD.data.get(bhRankKey, {})
        return max(qlRankInfo.get('rank', 0), bhRankInfo.get('rank', 0))

    def getGuildRankLevelType(self):
        qlRankKey = tournament.getRankStarKey(gametypes.GUILD_TOURNAMENT_GROUP_QL, self.groupScoreQL)
        bhRankKey = tournament.getRankStarKey(gametypes.GUILD_TOURNAMENT_GROUP_BH, self.groupScoreBH)
        qlRankInfo = RGTSD.data.get(qlRankKey, {})
        bhRankInfo = RGTSD.data.get(bhRankKey, {})
        return max(qlRankInfo.get('rankType', 0), bhRankInfo.get('rankType', 0))

    def checkPushNGTNApplyPush(self):
        for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
            if self.crossRankGtn[groupId].state == gametypes.NEW_GTN_STATE_APPLY:
                if not self.crossRankGtn[groupId].hasApplied:
                    if uiConst.MESSAGE_TYPE_NGTN_START_APPLY not in gameglobal.rds.ui.pushMessage.msgs:
                        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_NGTN_START_APPLY, {'click': Functor(self.onGTNApplyPushClick, groupId)})
                        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_NGTN_START_APPLY)
                    return

        if uiConst.MESSAGE_TYPE_NGTN_START_APPLY in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_NGTN_START_APPLY)

    def onGTNApplyPushClick(self, groupId):
        gameglobal.rds.ui.guild.show(tabIdx=uiConst.GUILDINFO_TAB_TOURNAMENT)

    def checkPushNGTNEnterPush(self):
        canEnterGroup = 0
        for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
            if self.crossRankGtn[groupId].canEnter:
                if uiConst.MESSAGE_TYPE_NGTN_ENTER not in gameglobal.rds.ui.pushMessage.msgs:
                    gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_NGTN_ENTER, {'click': Functor(self.onGTNApplyPushClick, groupId)})
                    gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_NGTN_ENTER)
                canEnterGroup = groupId
                break

        if not canEnterGroup or not self.inFightObserve() and (formula.inNewGuildTournamentQL(getattr(self, 'mapID', 0)) or formula.inNewGuildTournamentBH(getattr(self, 'mapID', 0))):
            if uiConst.MESSAGE_TYPE_NGTN_ENTER in gameglobal.rds.ui.pushMessage.msgs:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_NGTN_ENTER)
            canEnterGroup = 0
        if canEnterGroup and getattr(self, 'notifyGuildNgtStartFlag', False):
            msg = GCD.data.get('newGtnConfirmEnterMsg', 'confirm enter')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.confirmEnterNGTN, canEnterGroup), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=None, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)
        self.notifyGuildNgtStartFlag = False

    def confirmEnterNGTN(self, groupId):
        self.cell.enterNewGTN(groupId)
        gameglobal.rds.ui.bFScoreAward.setBFInfo(groupId, uiConst.BF_SCORE_AWARD_GUILD_TOURNAMENT)
