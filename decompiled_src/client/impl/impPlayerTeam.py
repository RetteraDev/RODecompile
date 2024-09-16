#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerTeam.o
from gamestrings import gameStrings
import Math
import BigWorld
import cPickle
import zlib
import const
import copy
import gameglobal
import gametypes
import gamelog
import utils
import formula
import keys
import random
import clientcom
import gameconfigCommon
from callbackHelper import Functor
from guis import uiConst
from guis import groupUtils
from guis import uiUtils
from guis import events
from sMath import distance2D
from sfx import sfx
from guis import ui
from helpers import navigator
from helpers import cellCmd
from helpers import loadingProgress
from helpers import ccManager
from appSetting import Obj as AppSettings
from data import message_desc_data as MDD
from data import game_msg_data as GMD
from data import state_data as SD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import fb_data as FBD
from data import map_config_data as MCD

class ImpPlayerTeam(object):

    def _refreshMembers(self):
        gamelog.debug('jorsef: _refreshMembers called!', self.groupNUID)
        gameglobal.rds.ui.memberDetailsV2.refreshMembers()
        gameglobal.rds.ui.teamComm.refreshMemberInfo()
        gameglobal.rds.ui.teamComm.hideMenu()
        gameglobal.rds.ui.teamComm.setAssignInfo()
        self._refreshTeamBuff()

    def hasInFollowMember(self):
        for mVal in self.members.itervalues():
            if mVal.get('inGroupFollow', False):
                return True

        return False

    def refreshMemberInfo(self):
        if not hasattr(self, 'members'):
            return
        if not self.isInTeamOrGroup():
            return
        if getattr(self, 'refreshTimer', 0) != 0:
            BigWorld.cancelCallback(self.refreshTimer)
            self.refreshTimer = 0
        others = set([ (mGbId, mVal['id']) for mGbId, mVal in self.members.iteritems() if mVal['id'] in gameglobal.rds.ui.teamComm.memberId ])
        if self.isInGroup():
            others = others.union(set([ (mGbId, mVal['id']) for mGbId, mVal in self.members.iteritems() if mVal['id'] in gameglobal.rds.ui.group.memberId ]))
        self.getOthersInfo(others)
        self.refreshTimer = BigWorld.callback(utils.getRefreshAvatarInfoInterval(self), self.refreshMemberInfo)
        if self.groupHeader == self.id and self.hasInFollowMember():
            self.cell.startGroupHeaderFollowSync()

    def _refreshTeamBuff(self):
        for mGbId, mVal in self.members.iteritems():
            if mGbId == self.gbId:
                continue
            mid = mVal['id']
            member = BigWorld.entities.get(mid, None)
            if not member:
                continue
            if not getattr(member, 'IsAvatar', False):
                continue
            member.clientBuffRefresh()

    def _setMemberPos(self):
        if not hasattr(self, 'membersPos'):
            self.membersPos = {}
        myMembers = {}
        if self.isInPUBG():
            myMembers = getattr(self, 'members', {})
        elif self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            for key, value in self.battleFieldTeam.items():
                if self.bfSideNUID == value['sideNUID']:
                    myMembers[key] = value

        elif self.inFubenTypes(const.FB_TYPE_ARENA):
            myMembers = self.arenaTeam
        elif self.isInTeamOrGroup():
            myMembers = getattr(self, 'members', {})
        needRm = []
        for mGbId, mVal in myMembers.iteritems():
            if mGbId == self.gbId:
                continue
            isOn, mid = mVal['isOn'], mVal['id']
            member = BigWorld.entities.get(mid, None)
            if member and (getattr(member, 'IsAvatar', False) or utils.instanceof(member, 'Puppet')):
                self.membersPos[mGbId] = (self.spaceNo,
                 member.position,
                 member.roleName,
                 BigWorld.ChunkInfoAt(member.position),
                 mid)
            if not isOn and self.membersPos.has_key(mGbId):
                needRm.append(mGbId)

        for mGbId, _ in self.membersPos.iteritems():
            if mGbId not in myMembers:
                needRm.append(mGbId)

        [ self.membersPos.pop(mGbId) for mGbId in needRm ]

    def getMembersPosProperly(self):
        isShaxingFuben = FBD.data.get(formula.getFubenNo(self.spaceNo), {}).get('isShaxingFuben')
        if isShaxingFuben and self.inFightObserve():
            return self.observedMembersPos
        else:
            return self.membersPos

    def onSetTemporaryGroupFollowOut(self, mGbId, flag):
        gamelog.debug('@zq#impPlayerTeam onSetTemporaryGroupFollowOut', mGbId, flag)
        if not self.members.has_key(mGbId):
            return
        self.groupFollowTempOutInfo[mGbId] = flag
        gameglobal.rds.ui.teamComm.refreshMemberInfo()

    def onSyncHeaderClientPos(self, x, y, z, spaceNo, isPathFinding, isForcely):
        gamelog.debug('@zq#impPlayerTeam onSyncHeaderClientPos', x, y, z, spaceNo, isPathFinding, isForcely)
        self.groupFollowHeaderGroundPos = Math.Vector3(x, y, z)
        enabledPath = gameglobal.rds.configData.get('enableGroupFollowHeaderPath')
        if enabledPath:
            self.groupFollowHeaderSpaceNo = spaceNo
            self.groupFollowHeaderInPathFinding = isPathFinding
        if enabledPath or isForcely:
            self.updateGroupFollowPathFinding()

    def syncGroupFollowHeaderPosCheck(self):
        if hasattr(self, 'groupHeader') and self.groupHeader == self.id:
            BigWorld.callback(const.SYNC_HEADER_GROUND_POS_INTERVAL, Functor(self.syncGroupFollowHeaderPosCheck))
            self.syncHeaderClientGroundPos()

    def refreshMemberPos(self):
        p = BigWorld.player()
        if not self.inWorld:
            return
        if formula.inHuntBattleField(BigWorld.player().mapID):
            gameglobal.rds.ui.map.addTeamMate([])
            gameglobal.rds.ui.littleMap.showTeamMate([])
            return
        if not (gameglobal.rds.configData.get('enableYmfMemberPos', False) and self.isInLueYingGu()):
            self._setMemberPos()
            teamArr = []
            membersPos = self.getMembersPosProperly()
            for mGbId, (spaceNo, pos, roleName, chunkName, entityId) in membersPos.iteritems():
                if self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
                    isHeader = mGbId == p.bfHeaderGbId
                    isAssistant = False
                    isJieQi = uiUtils.isJieQiTgt(mGbId)
                    isZhenChuan = uiUtils.isZhenChuanTgt(mGbId)
                    if p.isInPUBG() and p.checkTeammateDeadInPUBG(mGbId):
                        pos = p.getDeadTeammatePosInPUBG(mGbId)
                elif hasattr(self, 'members'):
                    isHeader = self.members.get(mGbId, {}).get('isHeader', False)
                    isAssistant = self.members.get(mGbId, {}).get('isAssistant', False)
                    isJieQi = uiUtils.isJieQiTgt(mGbId)
                    isZhenChuan = uiUtils.isZhenChuanTgt(mGbId)
                else:
                    isHeader = False
                    isAssistant = False
                    isJieQi = False
                    isZhenChuan = False
                isPartner = False
                if mGbId in getattr(self, 'partner', {}):
                    isPartner = True
                isMarriageTgt = False
                if roleName == self.marriageTgtName:
                    isMarriageTgt = True
                teamArr.append([pos,
                 mGbId,
                 roleName,
                 spaceNo,
                 chunkName,
                 entityId,
                 isHeader,
                 isAssistant,
                 self.isInMyTeamByGbId(mGbId),
                 isJieQi,
                 isZhenChuan,
                 isPartner,
                 isMarriageTgt])

            gameglobal.rds.ui.map.addTeamMate(teamArr)
            gameglobal.rds.ui.littleMap.showTeamMate(teamArr)
        if getattr(self, 'refPosTimer', 0) != 0:
            BigWorld.cancelCallback(self.refPosTimer)
            self.refPosTimer = 0
        self.refPosTimer = BigWorld.callback(utils.getRefreshAvatarInfoInterval(self), self.refreshMemberPos)

    def cancelTeamCallback(self):
        if getattr(self, 'refreshTimer', 0) != 0:
            BigWorld.cancelCallback(self.refreshTimer)
            self.refreshTimer = 0
        if getattr(self, 'refPosTimer', 0) != 0:
            BigWorld.cancelCallback(self.refPosTimer)
            self.refPosTimer = 0

    def _clearWidgets(self):
        gameglobal.rds.ui.createTeamV2.hide()

    def sortMembers(self, members):
        return sorted(members.iteritems(), key=lambda d: d[1].get('isHeader', 0), reverse=True)

    def getMemberIntimacy(self, member):
        if len(member) != 2:
            return 0
        gbIdList = member.keys()
        if self.gbId not in gbIdList:
            return 0
        myIndex = gbIdList.index(self.gbId)
        otherGbId = gbIdList[1 - myIndex]
        if self.friend.has_key(otherGbId):
            fVal = self.friend[otherGbId]
            if fVal.acknowledge:
                return fVal.intimacy
            else:
                return 0
        else:
            return 0

    def groupQuery(self, headerGbId, assignWay, arrangeDict, groupType, detailInfo, fbs, members, newSmallTeamMemGbIds):
        gamelog.debug('jorsef: groupQuery', self.id, self.groupNUID, headerGbId, assignWay, arrangeDict, groupType, detailInfo, fbs, members)
        if not hasattr(self, 'lastheaderGbId'):
            self.lastheaderGbId = 0
        self.headerGbId = headerGbId
        self.detailInfo = detailInfo
        self.arrangeDict = arrangeDict
        self._refreshAllRealModelState()
        diffList, addedMembers = self.getDiffMembers(members)
        oldMember = self.members.keys() if hasattr(self, 'members') else []
        newMember = [] if not members else members.keys()
        delMem = set(oldMember) - set(newMember)
        addMem = set(newMember) - set(oldMember)
        delMemId = 0
        if delMem:
            delMemId = self.members.get(tuple(delMem)[0], {}).get('id', 0)
        oldSmallTeamGbIds = self.smallTeamGbIds if hasattr(self, 'smallTeamGbIds') else []
        smallDelMem = set(oldSmallTeamGbIds) - set(newSmallTeamMemGbIds)
        smallAddMem = set(newSmallTeamMemGbIds) - set(oldSmallTeamGbIds)
        self.smallTeamGbIds = newSmallTeamMemGbIds
        if gameglobal.rds.configData.get('enablePubSubOperationClient', True):
            if smallAddMem or smallDelMem:
                addMemIds = []
                delMemIds = []
                for mgbid in smallAddMem:
                    a = members[mgbid].get('id', 0)
                    if a and a != self.id:
                        addMemIds.append(a)

                for mgbid in smallDelMem:
                    d = self.members[mgbid].get('id', 0)
                    if d and d != self.id:
                        delMemIds.append(d)

                if addMemIds or delMemIds:
                    self.cell.reqModTeamSubscribees(addMemIds, delMemIds)
        self.members = members
        if len(delMem) != 0 or len(addMem) != 0:
            gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_GROUP_MEMBER, uiConst.GROUP_MEMBER_CHANGED)
        self.onQuestInfoModifiedAtClient(const.QD_JIEQI, exData={'refreshAll': 1})
        self._refreshAllRealModelState()
        self._refreshHidingPower(diffList)
        self._setMemberPos()
        self._setApplyer()
        gamelog.debug('hjx debug groupQuery:', self.headerGbId, self.detailInfo, self.members, self.groupType)
        if self.groupNUID > 0:
            self._refreshMembers()
            gameglobal.rds.ui.group.refreshGroupInfo()
        self._refreshMemberBuffState()
        if self.groupNUID == 0:
            self._clearWidgets()
        self.removeApplyerAfterDone()
        gameglobal.rds.ui.assign.refreshAssignBtn(self.gbId == self.headerGbId)
        gameglobal.rds.ui.assign.refreshTeamInfo()
        for gbId in delMem:
            self.othersInfo.pop(gbId, None)

        if self.headerGbId != self.lastheaderGbId:
            gameglobal.rds.ui.shishenMode.hide()
            gameglobal.rds.ui.topBar.refreshTopBarWidgets()
            self.lastheaderGbId = self.headerGbId
        if self.inWorld and self.yabiaoData:
            gameglobal.rds.ui.yaBiao.refreshYabiaoView()
        if getattr(self.friend, 'inited', False):
            for member in addedMembers:
                self.base.addContact(member.get('roleName'), gametypes.FRIEND_GROUP_TEMP, 0)

        self.refreshTopLogoColor(addedMembers, delMemId)
        for value in members.values():
            teamer = BigWorld.entity(value['id'])
            teamer and teamer.topLogo and teamer.topLogo.updateRoleName(teamer.topLogo.name)
            gameglobal.rds.ui.refreshTeamLogoOrIdentity(value.get('id', 0))

        self.queryTeamGuideQuestStatus()

    def refreshTopLogoColor(self, addedMembersId, delMemId):
        p = BigWorld.player()
        if addedMembersId:
            for addId in addedMembersId:
                en = BigWorld.entity(addId.get('id'))
                en and en.topLogo.updateRoleName(en.topLogo.name)

        if delMemId:
            en = BigWorld.entity(delMemId)
            en and en.topLogo.updateRoleName(en.topLogo.name)

    def isHeader(self):
        return self.members.get(self.gbId, {}).get('isHeader', False)

    def isAssistant(self):
        return self.members.get(self.gbId, {}).get('isAssistant', False)

    def removeApplyerAfterDone(self):
        for key in self.members.keys():
            self.delApplyerByGbId(key)

    def getDiffMembers(self, members):
        diffList = []
        if hasattr(self, 'members') and self.members:
            oldMember = self.members.keys()
        else:
            oldMember = []
        newMember = [] if not members else members.keys()
        delMem = set(oldMember) - set(newMember)
        addMem = set(newMember) - set(oldMember)
        for i in delMem:
            if self.members.has_key(i):
                diffList.append(self.members.get(i)['id'])

        addedMembers = []
        for i in addMem:
            if members.has_key(i):
                diffList.append(members.get(i)['id'])
                addedMembers.append(members.get(i))

        return (diffList, addedMembers)

    def _refreshHidingPower(self, diffList):
        if diffList:
            for eid in diffList:
                teamer = BigWorld.entity(eid)
                if teamer and teamer != self and hasattr(teamer, 'resetHiding'):
                    teamer.resetHiding()

    def _refreshAllTeamer(self):
        if self == BigWorld.player():
            if gameglobal.gHideOtherPlayerFlag in (gameglobal.HIDE_ALL_PLAYER, gameglobal.HIDE_NOBODY):
                return
            for value in self.members.values():
                teamer = BigWorld.entity(value['id'])
                if teamer and teamer != self:
                    teamer.refreshOpacityState()
                    gameglobal.rds.ui.refreshTeamLogoOrIdentity(value.get('id', 0))

    def _refreshAllRealModelState(self):
        for value in self.members.values():
            teamer = BigWorld.entity(value['id'])
            if teamer and teamer != self:
                teamer.refreshRealModelState()

    def updatePublicTeamDetails(self, teamNUID, info):
        gamelog.debug('jorsef: updatePublicTeamDetails', teamNUID, info)
        info.sort(cmp=lambda x, y: cmp(x[4], y[4]), reverse=True)
        self.teamDetails = info

    def groupRequest(self, groupNUID, groupType, srcGbId, srcRole, srcSchool, srcLevel, memCount, teamName, memberDetail, params):
        gamelog.debug('hjx debug groupRequest:', groupNUID, groupType, srcGbId, srcRole, memCount, teamName, memberDetail, params)
        self.srcInviteGroupType = groupType
        gameglobal.rds.ui.teamInviteV2.pushInviteMessage(groupNUID, srcGbId, memCount, srcRole, teamName, srcSchool, srcLevel, memberDetail, groupType, params)

    def groupRecommend(self, groupType, recommendGbId, recommendName, recommendSch, recommendLv, headerName, memCount, teamName, params):
        gamelog.debug('hjx debug team groupRecommend:', headerName, recommendSch, recommendLv, params)
        self.showGameMsg(GMDD.data.GROUP_RECOMMEND, (recommendName, headerName))
        gameglobal.rds.ui.teamInviteV2.pushRecommendMessage(recommendGbId, recommendName, recommendLv, recommendSch, memCount, headerName, teamName, groupType, params)

    def updatePubTeamInfo(self, teamGoal, info):
        gamelog.debug('jorsef: updatePubTeamInfo', info)
        self.teamsInfo = info
        self.teamGoal = teamGoal
        gameglobal.rds.ui.team.refreshSocialTeamsInfo()

    def onQueryLinkTeamInfo(self, info):
        info = cPickle.loads(zlib.decompress(info))
        gamelog.debug('@jinjj group#onQueryLinkTeamInfo', info)
        if not hasattr(self, 'teamInfoQueryDict'):
            self.teamInfoQueryDict = {}
        self.teamInfoQueryDict[info['groupNUID']] = info
        gameglobal.rds.ui.chat.showTeamTooltip(info)
        if hasattr(self, 'clearQueryTeamInfoCallBack'):
            if self.clearQueryTeamInfoCallBack != -1:
                BigWorld.cancelCallback(self.clearQueryTeamInfoCallBack)
        self.clearQueryTeamInfoCallBack = BigWorld.callback(5, self.clearQueryTeamInfo)

    def clearQueryTeamInfo(self):
        self.teamInfoQueryDict = {}
        self.clearQueryTeamInfoCallBack = -1

    def showQuickJoinGroup(self):
        if self.checkCanQuickJoinWorldWarGroup():
            gameglobal.rds.ui.quickJoin.setJoinType(uiConst.QUICK_JOIN_GROUP_WORLD_WAR)
            gameglobal.rds.ui.quickJoin.showJoinClick()
        elif self.checkCanQuickJoinDiGongGroup():
            gameglobal.rds.ui.quickJoin.setJoinType(uiConst.QUICK_JOIN_GROUP_DIGONG)
            gameglobal.rds.ui.quickJoin.showJoinClick()

    def updateDiGongTeamInfo(self, info):
        if len(info) == 0:
            self.showGameMsg(GMDD.data.APPLY_QUICK_GROUP_FAILED_NO_TEAM, ())
            return
        if not self.checkCanQuickJoinDiGongGroup():
            return
        gameglobal.rds.ui.team.groupDetailFactory.applyGroupInDiGong(info)

    def updateWorldWarTeamInfo(self, info):
        gamelog.debug('@hjx ww#updateWorldWarTeamInfo:', info)
        if len(info) == 0:
            self.showGameMsg(GMDD.data.APPLY_QUICK_GROUP_FAILED_NO_TEAM, ())
            return
        if not self.checkCanQuickJoinWorldWarGroup():
            return
        gameglobal.rds.ui.team.groupDetailFactory.applyGroupInWorldWar(info)

    def _getSortedMembers(self):
        p = BigWorld.player()
        if p.isInPUBG():
            if hasattr(self, 'members'):
                return self.sortMembers(self.members)
        if self.inFightObserve():
            return self.sortMembers(self.observedMembers)
        if hasattr(self, 'members'):
            return self.sortMembers(self.members)
        return []

    def _getTeamsInfo(self):
        if not hasattr(self, 'teamsInfo'):
            self.teamsInfo = []

    def _getMembers(self):
        if not hasattr(self, 'members'):
            self.members = {}
        return self.members

    def _getTeamDetails(self):
        if not hasattr(self, 'teamDetails'):
            self.teamDetails = []

    def _getDetailInfo(self):
        if not hasattr(self, 'detailInfo'):
            self.detailInfo = {}

    def _getApplyer(self):
        if not hasattr(self, 'applyer'):
            self.applyer = []
        return self.applyer

    def _setApplyer(self):
        if not hasattr(self, 'applyer'):
            self.applyer = []

    def _checkValidSchool(self, school):
        return school in const.ALL_SCHOOLS

    def isTeamFull(self):
        if hasattr(self, 'members'):
            if len(self.members) == const.TEAM_MAX_NUMBER:
                return True
            else:
                return False
        return False

    def unloadWidgets(self):
        self._refreshMemberBuffState()
        gamelog.debug('hjx debug unloadWidgets')
        self.queryPublicTeams('', const.GROUP_GOAL_DEFAULT)
        gameglobal.rds.ui.player.setLeaderIcon(False)
        gameglobal.rds.ui.teamComm.closeTeamPlayer()
        gameglobal.rds.ui.createTeamV2.hide()
        gameglobal.rds.ui.memberDetailsV2.hide()
        gameglobal.rds.ui.team.assignRule = const.GROUP_ASSIGN_FREE
        gameglobal.rds.ui.team.assignQuality = const.GROUP_ASSIGN_QUALITY[2]
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_APPLY_TEAM)
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP)
        gameglobal.rds.ui.teamComm.hideMenu()
        gameglobal.rds.ui.team.refreshBtn()
        gameglobal.rds.ui.invitePlayer.hide()

    def onTeamGoalChanged(self, groupNUID):
        if not uiUtils.checkShareTeamLvLimit():
            return
        gameglobal.rds.ui.dispatchEvent(events.EVENT_TEAM_GOAL_CHANGED)

    def onTeamGoalChangedByCall(self, groupNUID):
        p = BigWorld.player()
        msg = gameglobal.rds.ui.team.getShareTeamInfoMsg()
        p.cell.chatToGroupInfo(msg)
        p.cell.chatToGuild(msg, True)

    def notifyInviteGroupFailedWithNoGroupAlready(self, tgtRoleName):
        self.inviteGroupFailedInfo.setdefault('tgtRoleNameSet', set()).add(tgtRoleName)
        gameglobal.rds.ui.team.buildNoDetailGroup()

    def buildGroup(self, groupDetails, groupType, buildReason = gametypes.TEAM_REASON_NORMAL):
        if buildReason == gametypes.TEAM_REASON_NEW_PLAYER_TREASURE:
            groupDetails = list(groupDetails)
            groupDetails.append(gametypes.NT_GROUP_TYPE)
            self.cell.buildGroupByType(groupType, False, *groupDetails)
            return
        self.cell.buildGroup(groupType, False, *groupDetails)

    def setGroupDetails(self, groupDetails, callBackType = 0):
        groupDetailsList = list(groupDetails)
        groupDetailsList.append(callBackType)
        self.cell.setGroupDetails(*groupDetailsList)

    def inviteGroup(self, tgtRoleName):
        gamelog.debug('hjx debug inviteGroup:', tgtRoleName)
        if self.inFubenTypes(const.FB_TYPE_ARENA):
            self.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
            return
        if self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.showGameMsg(GMDD.data.BATTLE_FIELD_FORBIDDEN_WITH_TEAM, ())
            return
        if self.groupMatchStatus > 0:
            msg = MDD.data.get('ACCEPT_GROUP_MATCH_STATUS_NOTIFY', gameStrings.TEXT_IMPPLAYERTEAM_592)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cancelGroupMatch, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_595, noBtnText=gameStrings.TEXT_IMPPLAYERTEAM_596)
            return
        self.cell.inviteGroup(tgtRoleName)

    def recommendGroup(self, tgtRoleName):
        if self.inFubenTypes(const.FB_TYPE_ARENA):
            self.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
            return
        if self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.showGameMsg(GMDD.data.BATTLE_FIELD_FORBIDDEN_WITH_TEAM, ())
            return
        self.cell.recommendGroup(tgtRoleName)

    def acceptGroup(self, groupNUID, srcGbId, srcRole):
        if self.isInTeam() and self.isHeader():
            if not gameglobal.rds.ui.assign.isTeamBagEmpty():
                msg = GMD.data.get(GMDD.data.GROUP_INVITE_TEAM_NOTIFY_ASSIGN_TEMPBAG_NOT_EMPTY, {}).get('text', '')
                self.acceptMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._doAcceptGroup, groupNUID, srcGbId, srcRole), noCallback=Functor(self._doRejectInvite, srcGbId))
                return
            if self.inFuben():
                msg = GMD.data.get(GMDD.data.GROUP_INVITE_TEAM_NOTIFY_IN_FUBEN, {}).get('text', '')
                self.acceptMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._doAcceptGroup, groupNUID, srcGbId, srcRole), noCallback=Functor(self._doRejectInvite, srcGbId))
                return
        if self.groupMatchStatus > 0:
            msg = MDD.data.get('ACCEPT_GROUP_MATCH_STATUS_NOTIFY', gameStrings.TEXT_IMPPLAYERTEAM_592)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cancelGroupMatch, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_595, noBtnText=gameStrings.TEXT_IMPPLAYERTEAM_596)
            return
        self._doAcceptGroup(groupNUID, srcGbId, srcRole)

    def _doAcceptGroup(self, groupNUID, srcGbId, srcRole):
        self.acceptMsgBoxId = 0
        gameglobal.rds.ui.teamInviteV2.onInviteRecommendResult(srcGbId)
        if utils.getEnableIgnoreTgtGroup() and self.groupNUID > 0 and self.srcInviteGroupType == gametypes.GROUP_TYPE_TEAM_GROUP and len(self.members) == 1:
            msg = MDD.data.get('ACCEPT_GROUP_NOTIFY_WITH_ONE_MEMBER', gameStrings.TEXT_IMPPLAYERTEAM_639)
            groupTypeDesc = gametypes.GROUP_DESC_BY_TYPE.get(self.groupType, '')
            msg = msg % (groupTypeDesc, groupTypeDesc)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._realDoAcceptGroup, groupNUID, srcGbId, srcRole), yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noCallback=Functor(self._doRejectInvite, srcGbId), noBtnText=gameStrings.TEXT_AVATAR_2876_1)
        else:
            self.cell.acceptGroup(groupNUID, srcGbId, srcRole)

    def _realDoAcceptGroup(self, groupNUID, srcGbId, srcRole):
        self.quitGroup()
        self.acceptGroupAfterQuit = (groupNUID, srcGbId, srcRole)

    def checkAcceptGroupWithQuitGroupAuto(self):
        if not utils.getEnableIgnoreTgtGroup():
            return
        if len(self.acceptGroupAfterQuit) == 0:
            return
        if len(self.members) != 1:
            return
        groupNUID, srcGbId, srcRole = self.acceptGroupAfterQuit
        self.cell.acceptGroup(groupNUID, srcGbId, srcRole)

    def _doRejectInvite(self, srcGbId):
        self.rejectInviteGroup(srcGbId)
        self.acceptMsgBoxId = 0
        gameglobal.rds.ui.teamInviteV2.onInviteRecommendResult(srcGbId)

    def queryTeamDetailByGroupNUID(self, groupNUID):
        self.cell.queryTeamDetails(groupNUID)

    @ui.callFilter(2)
    def applyGroup(self, tgtRoleName, groupType = gametypes.GROUP_TYPE_TEAM_GROUP):
        if self.inFubenTypes(const.FB_TYPE_ARENA):
            self.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
            return
        if self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.showGameMsg(GMDD.data.BATTLE_FIELD_FORBIDDEN_WITH_TEAM, ())
            return
        if tgtRoleName != '':
            if utils.getEnableIgnoreTgtGroup() and self.groupNUID > 0 and len(self.members) == 1:
                msg = MDD.data.get('APPLY_GROUP_NOTIFY_WITH_ONE_MEMBER', gameStrings.TEXT_IMPPLAYERTEAM_687)
                groupTypeDesc = gametypes.GROUP_DESC_BY_TYPE.get(self.groupType, '')
                msg = msg % (groupTypeDesc, groupTypeDesc)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._doApplyGroupWithQuitGroup, tgtRoleName), yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1)
            else:
                self._doApplyGroup(tgtRoleName)

    def resetWithQuitGroupAutoInfo(self):
        self.needApplyGroupAfterQuit = False
        self.applyGroupTgtRoleNameAfterQuit = ''
        self.srcInviteGroupType = gametypes.GROUP_TYPE_NON_GROUP
        self.acceptGroupAfterQuit = ()

    def _doApplyGroup(self, tgtRoleName):
        if tgtRoleName != '':
            self.cell.applyGroup(tgtRoleName)

    def _doApplyGroupWithQuitGroup(self, tgtRoleName):
        if tgtRoleName != '':
            self.quitGroup()
            self.needApplyGroupAfterQuit = True
            self.applyGroupTgtRoleNameAfterQuit = tgtRoleName

    def checkApplyGroupWithQuitGroupAuto(self):
        if not utils.getEnableIgnoreTgtGroup():
            return
        if not self.needApplyGroupAfterQuit:
            return
        if self.applyGroupTgtRoleNameAfterQuit == '':
            return
        if len(self.members) != 1:
            return
        print '@hjx checkApplyGroupWithQuitGroupAuto:', self.roleName
        self._doApplyGroup(self.applyGroupTgtRoleNameAfterQuit)

    def applyGroupSucc(self, roleName, level, school, groupNUID):
        gameglobal.rds.ui.teamComm.showApply(roleName, level, school, 0, groupNUID, False)
        gameglobal.rds.ui.quickJoin.showJoining()

    def acceptApplyGroup(self, srcName, srcGbId):
        if self.groupMatchStatus > 0:
            msg = MDD.data.get('ACCEPT_GROUP_MATCH_STATUS_NOTIFY', gameStrings.TEXT_IMPPLAYERTEAM_592)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.cancelGroupMatch, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_595, noBtnText=gameStrings.TEXT_IMPPLAYERTEAM_596)
        else:
            self._doAcceptApplyGroup(srcName, srcGbId)

    def _doAcceptApplyGroup(self, srcName, srcGbId):
        self.cell.acceptApplyGroup(srcName, srcGbId)
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_APPLY_TEAM, gameglobal.rds.ui.team._getApplyData(srcGbId))

    def rejectApplyGroup(self, srcName, srcGbId):
        self.cell.rejectApplyGroup(srcName, srcGbId)
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_APPLY_TEAM, gameglobal.rds.ui.team._getApplyData(srcGbId))

    def rejectInviteGroup(self, srcGbId):
        self.cell.rejectInviteGroup(srcGbId)

    def rejectRecommendGroup(self, srcGbId):
        self.cell.rejectRecommendGroup(srcGbId)

    def applyGroupOvertime(self, srcGbId):
        self.cell.applyGroupOvertime(srcGbId)

    def inviteGroupOvertime(self, srcGbId):
        self.cell.inviteGroupOvertime(srcGbId)

    def quitGroup(self):
        if gameglobal.rds.ui.assign.isTeamBagEmpty() or not self.isHeader():
            self._doQuitGroup()
        else:
            msg = GMD.data.get(GMDD.data.GROUP_ASSIGN_TEAMBAG_NOT_EMPTY, {}).get('text', gameStrings.TEXT_IMPPLAYERTEAM_769)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self._doQuitGroup)

    def _doQuitGroup(self):
        self.clearInDyingEntity()
        self.cell.quitGroup()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_DISSOLVE_TEAM_PUSH)

    def deleteMemFromTeam(self, tgtGbId, tgtName):
        if self.yabiaoData:
            msg = uiUtils.getTextFromGMD(GMDD.data.YABIAO_KICK_TEAM_MSG, gameStrings.TEXT_IMPPLAYERTEAM_780) % tgtName
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.kickOutGroup, tgtGbId, tgtName), yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_783, noBtnText=gameStrings.TEXT_IMPPLAYERTEAM_784)
        else:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_IMPPLAYERTEAM_786 % tgtName, Functor(self.cell.kickOutGroup, tgtGbId, tgtName), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def changeTeamLeader(self, tgtGbId):
        self.cell.abdicatedGroup(tgtGbId)

    def delApplyerByGbId(self, gbId):
        gamelog.debug('hjx debug team delApplyerByGbId:', gbId, self.applyer)
        index = self.findApplyerByGbId(gbId)
        if index != -1:
            del self.applyer[index]
            gameglobal.rds.ui.team.refreshApplyer()
            gameglobal.rds.ui.teamComm.refreshApplyer(index)
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_APPLY_TEAM, gameglobal.rds.ui.team._getApplyData(gbId))

    def delAllApplyer(self):
        if hasattr(self, 'applyer'):
            for index, value in enumerate(self.applyer):
                self.cell.applyerGroupFailed(value[4], GMDD.data.APPLY_FAIL)

            self.applyer = []
            gameglobal.rds.ui.teamComm.removeApplyer()

    def applyByGroup(self, srcName, srcLevel, srcSchool, srcGbId):
        if self.findApplyerByGbId(srcGbId) == -1:
            gamelog.debug('hjx debug team: applyByGroup', srcName, srcLevel, srcGbId)
            self.applyer.append((srcName,
             srcLevel,
             srcSchool,
             self.getServerTime(),
             srcGbId))
            gameglobal.rds.ui.team.pushApplyMessage(srcName, srcLevel, srcSchool, srcGbId)
            self.showGameMsg(GMDD.data.GROUP_APPLY_IN, (srcName,))
            gameglobal.rds.ui.team.refreshApplyer()
            gameglobal.rds.ui.teamComm.playShine()
            index = gameglobal.rds.ui.teamComm.pageIndex
            gameglobal.rds.ui.teamComm.refreshApplyer(index)

    def onApplyByGroupWithTgtNonGroup(self, srcName, srcLevel, srcSchool, srcGbId):
        gameglobal.rds.ui.team.pushApplyMessageWithNonGroup(srcName, srcLevel, srcSchool, srcGbId)

    def rejectApply(self, groupNUID):
        gamelog.debug('hjx debug team rejectApply:', groupNUID)
        self.showGameMsg(GMDD.data.APPLY_FAIL, ())

    def findApplyerByGbId(self, gbId):
        if hasattr(self, 'applyer'):
            for index, value in enumerate(self.applyer):
                if gbId == value[4]:
                    return index

        return -1

    def onApplyerFailed(self, groupNUID, msgId, msgArg):
        self.showGameMsg(msgId, msgArg)

    def groupAward(self, item, assignWay, owner, ok, pickTime, extra):
        gamelog.debug('@zs groupAward', item, assignWay, owner, ok, self.id, pickTime)
        if extra and extra.has_key('spaceNo'):
            spaceNo = extra.get('spaceNo')
            if (self.inWingCity() or formula.spaceInWingCity(spaceNo)) and spaceNo != self.spaceNo:
                gamelog.warning('groupAward not in same wing city space', self.spaceNo, spaceNo, item, assignWay)
                return
        if self._isInCross() and assignWay not in (const.GROUP_ASSIGN_DICE_JOB, const.GROUP_ASSIGN_DICE, const.GROUP_ASSIGN_NONE):
            return
        if assignWay == const.GROUP_ASSIGN_HEADER:
            gameglobal.rds.ui.assign.updateTeamBag(item, ok, owner)
        elif assignWay in (const.GROUP_ASSIGN_DICE_JOB, const.GROUP_ASSIGN_DICE):
            gameglobal.rds.ui.assign.showDice(item, ok, pickTime)
        elif assignWay == const.GROUP_ASSIGN_AUCTION:
            gameglobal.rds.ui.assign.updateAuctionBag(item, ok)
        elif assignWay == const.GROUP_ASSIGN_NONE:
            gameglobal.rds.ui.assign.closeTeambag()
            gameglobal.rds.ui.assign.closeDice()
            gameglobal.rds.ui.assign.closeAuction()
            gameglobal.rds.ui.assign.reset()

    def _classfyPlayersByDist(self, players):
        farawayPlayers = []
        nearPlayers = []
        for gbId, pid in players:
            entity = BigWorld.entities.get(pid, None)
            if clientcom.bfDotaAoIInfinity():
                if entity and pid in self.bfDotaEntityIdRecord.get(const.DOTA_ENTITY_TYPE_LITTLE_MAP, set()):
                    nearPlayers.append(entity)
            elif pid:
                if not entity:
                    farawayPlayers.append((gbId, pid))
                elif distance2D(self.position, entity.position) >= 75:
                    farawayPlayers.append((gbId, pid))
                else:
                    nearPlayers.append(entity)

        return (farawayPlayers, nearPlayers)

    def getOthersInfo(self, others):
        farawayPlayers, nearPlayers = self._classfyPlayersByDist(others)
        gamelog.debug('@hjx group#getOthersInfo:', others, farawayPlayers)
        if len(farawayPlayers):
            gbIdList = [ player[0] for player in farawayPlayers ]
            entIdList = [ player[1] for player in farawayPlayers ]
            self.cell.startGroupInfoSync()
            self.cell.getOthersInfo(gbIdList, entIdList)
        else:
            self.cell.stopPropertySync()

    def getMembersProperly(self):
        p = BigWorld.player()
        if p.isInPUBG():
            return self.members
        elif self.inFightObserve():
            return self.observedMembers
        else:
            return self.members

    def onReceiveMemberInfo(self, memberGbId, info):
        gamelog.debug('@hjx group#onReceiveMemberInfo0:', memberGbId, info, self.members.has_key(memberGbId), self.isInTeam())
        if not self.members.has_key(memberGbId):
            return
        memberId = self.members[memberGbId]['id']
        hp, mhp, mp, mmp, lv = info
        gameglobal.rds.ui.memberDetailsV2.refreshMembers()
        if self.isInTeam():
            gamelog.debug('zt: member info', gameglobal.rds.ui.teamComm.memberId, memberId)
            for idx, mid in enumerate(gameglobal.rds.ui.teamComm.memberId):
                if mid == memberId:
                    gameglobal.rds.ui.teamComm.setOldVal(idx, hp, mhp, mp, mmp, lv)
                    return

        if self.isInGroup() and groupUtils.isInSameTeam(self.gbId, memberGbId):
            for idx, mid in enumerate(gameglobal.rds.ui.teamComm.memberId):
                if mid == memberId:
                    gamelog.debug('@hjx group#onReceiveMemberInfo1:', memberGbId, info)
                    gameglobal.rds.ui.teamComm.setOldVal(idx, hp, mhp, mp, mmp, lv)

        if self.isInGroup():
            for idx, mid in enumerate(gameglobal.rds.ui.group.memberId):
                if mid == memberId:
                    gameglobal.rds.ui.group.setOldVal(idx, hp, mhp, mp, mmp, lv)
                    return

    def resOthersInfo(self, result):
        if not hasattr(self, 'othersInfo'):
            self.othersInfo = {}
        for memberGbId, info in result.iteritems():
            if self.othersInfo.has_key(memberGbId):
                self.othersInfo[memberGbId].update(info)
            else:
                self.othersInfo[memberGbId] = info

        for memberGbId, info in result.iteritems():
            mid = -1
            hp = self.othersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_HP, -1)
            mhp = self.othersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_MHP, -1)
            mp = self.othersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_MP, -1)
            mmp = self.othersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_MMP, -1)
            lv = info.get(gametypes.TEAM_SYNC_PROPERTY_LV, -1)
            spaceNo = info.get(gametypes.TEAM_SYNC_PROPERTY_SPACENO, 0)
            pos = info.get(gametypes.TEAM_SYNC_PROPERTY_POSITION)
            roleName = info.get(gametypes.TEAM_SYNC_PROPERTY_ROLENAME)
            chunkName = info.get(gametypes.TEAM_SYNC_PROPERTY_CHUNKNAME)
            teamInfo = (hp,
             mhp,
             mp,
             mmp,
             lv)
            if self.inFubenTypes(const.FB_TYPE_ARENA):
                self.onReceiveArenaCampInfo(memberGbId, teamInfo)
                if self.arenaTeam.has_key(memberGbId):
                    mid = self.arenaTeam[memberGbId]['id']
            elif self.isInTeam() or self.isInGroup():
                self.onReceiveMemberInfo(memberGbId, teamInfo)
                if self.members.has_key(memberGbId):
                    mid = self.members[memberGbId]['id']
            if mid == -1:
                continue
            if self.membersPos.has_key(memberGbId):
                spaceNo = spaceNo or self.membersPos[memberGbId][0]
                pos = pos or self.membersPos[memberGbId][1]
                roleName = roleName or self.membersPos[memberGbId][2]
                chunkName = chunkName or self.membersPos[memberGbId][3]
            self.membersPos[memberGbId] = (spaceNo,
             pos,
             roleName,
             chunkName,
             mid)

        self._fixOthersInfo(result)
        self.refreshTeammateInfoInWidget(result)

    def checkOldTeamMemberInfo(self, memberGbId):
        if not self.members.has_key(memberGbId):
            return
        memberId = self.members[memberGbId]['id']
        if self.isInTeam():
            for idx, mid in enumerate(gameglobal.rds.ui.teamComm.memberId):
                if mid == memberId:
                    return gameglobal.rds.ui.teamComm.oldHp[idx]

    def _fixOthersInfo(self, result):
        if not self.isInTeam():
            return
        for memberGbId in self.members.iterkeys():
            if memberGbId != self.gbId and memberGbId not in result and memberGbId in self.othersInfo:
                hp = self.othersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_HP, -1)
                if hp != self.checkOldTeamMemberInfo(memberGbId):
                    mhp = self.othersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_MHP, -1)
                    mp = self.othersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_MP, -1)
                    mmp = self.othersInfo[memberGbId].get(gametypes.TEAM_SYNC_PROPERTY_MMP, -1)
                    lv = self.othersInfo.get(gametypes.TEAM_SYNC_PROPERTY_LV, -1)
                    teamInfo = (hp,
                     mhp,
                     mp,
                     mmp,
                     lv)
                    self.onReceiveMemberInfo(memberGbId, teamInfo)

    def refreshTeammateInfoInWidget(self, res):
        p = BigWorld.player()
        if p.isInTeam() and p.isInPUBG():
            for gbId, info in res.iteritems():
                if self.members.has_key(gbId):
                    memberId = self.members[gbId]['id']
                    hp = info.get(gametypes.TEAM_SYNC_PROPERTY_HP, 0)
                    mhp = info.get(gametypes.TEAM_SYNC_PROPERTY_MHP, 0)
                    mp = info.get(gametypes.TEAM_SYNC_PROPERTY_MP, 0)
                    mmp = info.get(gametypes.TEAM_SYNC_PROPERTY_MMP, 0)
                    if mhp != 0:
                        gameglobal.rds.ui.teamComm.setTeamHp(memberId, hp, mhp)
                    if mmp != 0:
                        gameglobal.rds.ui.teamComm.setTeamMp(memberId, mp, mmp)

    def receivePos(self, gbId, posX, posZ, littmeMapNo):
        p = BigWorld.player()
        if p.isInPUBG() and hasattr(p, 'setTeammateMapMarkInPUBG'):
            p.setTeammateMapMarkInPUBG(gbId, posX, posZ, littmeMapNo)
        else:
            gameglobal.rds.ui.littleMap.showPosition((posX, 0, posZ), littmeMapNo)

    def canInviteTeam(self, target):
        if not target:
            return False
        className = target.__class__.__name__
        if className != 'Avatar':
            return False
        isTeamMember = False
        for id in self._getMembers().keys():
            if id == target.gbId:
                isTeamMember = True
                break

        if not isTeamMember and target.id != self.id:
            return True
        return False

    def canApplyTeam(self, target):
        if not target:
            return False
        className = target.__class__.__name__
        if className != 'Avatar':
            return False
        if not self.isInTeam() and target.id != self.id and target.isInTeam():
            return True
        return False

    def inviteTeam(self, tgtRoleName):
        if not tgtRoleName:
            return
        if self.inFubenTypes(const.FB_TYPE_ARENA):
            self.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
            return
        if self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.showGameMsg(GMDD.data.BATTLE_FIELD_FORBIDDEN_WITH_TEAM, ())
            return
        if tgtRoleName == self.roleName:
            self.chatToEventEx(gameStrings.TEXT_MENUMANAGER_1120, const.CHANNEL_COLOR_GREEN)
            return
        if not self.isInTeam() or self.groupHeader == self.id:
            self.inviteGroup(tgtRoleName)
        else:
            self.recommendGroup(tgtRoleName)

    def applyTeam(self, tgtRoleName):
        if not tgtRoleName:
            return
        if self.inFubenTypes(const.FB_TYPE_ARENA):
            self.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
            return
        if self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.showGameMsg(GMDD.data.BATTLE_FIELD_FORBIDDEN_WITH_TEAM, ())
            return
        self.applyGroup(tgtRoleName)

    def groupArrange(self, arrangeDict):
        gameglobal.rds.ui.group.changeArrangeData(self.arrangeDict, arrangeDict)
        self.arrangeDict = arrangeDict
        gameglobal.rds.ui.group.refreshGroupInfo()
        gameglobal.rds.ui.teamComm.refreshMemberInfo(False)
        self._refreshTeamBuff()
        self.onQuestInfoModifiedAtClient(const.QD_JIEQI, exData={'refreshAll': 1})

    def setEntityMark(self, mark):
        self.groupMark = mark
        for key, value in self.groupMark.items():
            ent = BigWorld.entities.get(key)
            if ent and hasattr(ent, 'topLogo') and ent.topLogo:
                ent.topLogo.setTeamLogo(value)

    def resetEntityMark(self):
        if hasattr(self, 'groupMark'):
            for key in self.groupMark.iterkeys():
                ent = BigWorld.entities.get(key)
                if ent and hasattr(ent, 'topLogo') and ent.topLogo:
                    ent.topLogo.removeTeamLogo()

            self.groupMark = {}

    def addEntityMark(self, entityId, markFlag):
        self.groupMark[entityId] = markFlag
        ent = BigWorld.entities.get(entityId)
        if ent and ent.topLogo:
            markIdentityFlag = gameglobal.rds.ui.getGroupIdentityType(entityId, AppSettings.get(keys.SET_TEAM_TOP_LOGO_MARK, 1))
            ent.topLogo.setTitleEffectHeight()
            if markFlag == uiConst.MENU_SPECIAL_MARK:
                ent.topLogo.removeTeamLogo()
                if markIdentityFlag:
                    ent.topLogo.setTeamIdentity(markIdentityFlag)
                else:
                    ent.topLogo.removeTeamIdentity()
            else:
                ent.topLogo.removeTeamIdentity()
                ent.topLogo.setTeamLogo(markFlag)

    def delEntityMark(self, entityId):
        self.groupMark.pop(entityId, None)
        ent = BigWorld.entities.get(entityId)
        if ent and hasattr(ent, 'topLogo') and ent.topLogo:
            ent.topLogo.removeTeamLogo()
            markId = self.groupMark.get(entityId, uiConst.MENU_SPECIAL_MARK)
            markFlag = gameglobal.rds.ui.getGroupIdentityType(entityId, AppSettings.get(keys.SET_TEAM_TOP_LOGO_MARK, 1))
            ent.topLogo.setTitleEffectHeight()
            if markId == uiConst.MENU_SPECIAL_MARK and markFlag:
                ent.topLogo.setTeamIdentity(markFlag)
            else:
                ent.topLogo.removeTeamIdentity()

    def onSetMapMark(self, groupMapMark, mapMarkStatus):
        gamelog.debug('@hjx marking#setMapMark:', groupMapMark)
        self.groupMapMark = groupMapMark
        for key, val in self.groupMapMark.items():
            if mapMarkStatus.has_key(key) and mapMarkStatus[key]:
                if not self.attachFx.has_key(val['effectId']):
                    fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, [gameglobal.EFFECT_HIGH,
                     gameglobal.EFF_DEFAULT_PRIORITY,
                     None,
                     val['effectId'],
                     sfx.EFFECT_UNLIMIT,
                     val['pos'],
                     0,
                     val['yaw'],
                     0,
                     sfx.KEEPEFFECTTIME])
                    self.addFx(val['effectId'], fx)

        gameglobal.rds.ui.littleMap.showMapMark()

    def onResetMapMark(self):
        gamelog.debug('@hjx marking#resetMapMark:', self.groupMapMark)
        for val in self.groupMapMark.values():
            self.removeFx(val['effectId'])

        self.groupMapMark = {}
        gameglobal.rds.ui.littleMap.showMapMark()

    def onAddMapMark(self, mapMarkIndex, extra, mapMarkStatus):
        gamelog.debug('@hjx marking#addMapMark:', self.id, mapMarkIndex, extra)
        self.groupMapMark[mapMarkIndex] = extra
        if not mapMarkStatus[mapMarkIndex]:
            return
        else:
            if self.attachFx.has_key(extra['effectId']):
                self.removeFx(extra['effectId'])
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, [gameglobal.EFFECT_HIGH,
             gameglobal.EFF_DEFAULT_PRIORITY,
             None,
             extra['effectId'],
             sfx.EFFECT_UNLIMIT,
             extra['pos'],
             0,
             extra['yaw'],
             0,
             sfx.KEEPEFFECTTIME])
            self.addFx(extra['effectId'], fx)
            gameglobal.rds.ui.littleMap.showMapMark()
            return

    def onDelMapMark(self, mapMarkIndex):
        gamelog.debug('@hjx marking#delMapMark:', mapMarkIndex, self.groupMapMark)
        self.groupMapMark.pop(mapMarkIndex, None)
        self.removeFx(self.groupMapMark[mapMarkIndex]['effectId'])
        gameglobal.rds.ui.littleMap.showMapMark()

    def askForGroupPrepare(self, groupNUID):
        gamelog.debug('@hjx prepare#askForGroupPrepare:', groupNUID, self.roleName)
        if self.groupNUID > 0 and groupNUID == self.groupNUID and not self.isHeader():
            gameglobal.rds.ui.group.showPrepareAskMsg()
        gameglobal.rds.ui.group.startPrepare()

    def updateGroupPrepare(self, result, isEnd):
        gamelog.debug('@hjx prepare#updateGroupPrepare:', result, self.roleName, isEnd)
        if isEnd:
            self.groupPrepareInfo = {}
            gameglobal.rds.ui.group.clearPrepareInfo()
        else:
            self.groupPrepareInfo = result
            gameglobal.rds.ui.group.setPrePareInfo()

    def queryPublicTeams(self, teamName, teamTarget, firstKey = -1, secondKey = -1, thirdKey = -1):
        if teamTarget == const.GROUP_HOT_TAGS:
            teamTarget = const.GROUP_GOAL_RELAXATION
        isFilter = gameglobal.rds.ui.team.isFilter
        self.cell.queryPublicTeams(teamName, teamTarget, firstKey, secondKey, thirdKey, isFilter)

    def onSetGroupType(self, groupType):
        gamelog.debug('@hjx group#onSetGroupType:', groupType)

    def getGroupNum(self):
        if not hasattr(self, 'members'):
            return 0
        if self.groupNUID == 0:
            return 0
        return len(self.members)

    def cancelGroupMatch(self):
        if self.groupMatchStatus == gametypes.GROUP_MATCH_STATUS_DEFAULT:
            self.onDiscardMatchSeat()
            return
        self.cell.cancelGroupMatch(self.groupMatchClass)

    def onUpdateGroupMatchInfo(self, groupMatchClass, matchMemberInfo, matchStartTime, extra):
        gamelog.debug('@hjx groupMatch#onUpdateGroupMatchInfo:', self.id, matchMemberInfo, matchStartTime, extra)
        self.groupMatchClass = groupMatchClass
        self.groupMatchMemberInfo = matchMemberInfo
        self.groupMatchStartTime = matchStartTime
        self.groupMatchExtra = extra
        if self.groupMatchStatus == gametypes.GROUP_MATCH_STATUS_DEFAULT:
            return
        gameglobal.rds.ui.teamComm.showGroupMatch()
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GROUP_MATCHED)

    def onNotifyMatchGroupDone(self):
        uiUtils.showWindowEffect()

    def onDiscardMatchSeat(self):
        gamelog.debug('@hjx groupMatch#onDiscardMatchSeat:', self.id)
        gameglobal.rds.ui.teamComm.closeGroupMatch()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GROUP_MATCHED)

    def refreshAssignMode(self):
        if self.isInTeam():
            gameglobal.rds.ui.memberDetailsV2.refreshAssignMode()
        elif self.isInGroup():
            gameglobal.rds.ui.group.refreshAssignMode()
        gameglobal.rds.ui.teamComm.refreshAssignMode()

    def getOthersNewState(self, entity, newSet, refresh = False):
        if self == entity:
            return
        if not getattr(entity, 'IsAvatar', False):
            return
        battleFieldTeam = getattr(self, 'battleFieldTeam', {})
        arenaTeam = getattr(self, 'arenaTeam', {})
        if not self.isInMyTeamByGbId(entity.gbId) and not battleFieldTeam.has_key(entity.gbId) and not arenaTeam.has_key(entity.gbId):
            return
        if not hasattr(self, 'memberBuffState'):
            self.memberBuffState = {}
        oldSet, oldBuffKeySet = self.memberBuffState.get(entity.gbId, (set(), set()))
        if refresh == False:
            addSet = newSet - oldSet
            delSet = oldSet - newSet
            if not addSet and not delSet:
                return
        buffDataDict = {}
        buffKeySet = set()
        delBuff = []
        buffNum = 0
        deBuffNum = 0
        for stateId, srcId, totalTime, layerNum, startTime in newSet:
            bdata = SD.data.get(stateId, {})
            isHide = bdata.get('iconUnshow', 0)
            if isHide:
                continue
            priority = bdata.get('priority', 255)
            unShow = bdata.get('unShow', 0)
            if unShow == 1:
                continue
            data = self._getTargetStateData(entity, stateId, srcId, totalTime, layerNum, startTime)
            data['totalTime'] = totalTime
            data['startTime'] = startTime
            data['priority'] = priority
            buffKey = '%s_%s' % (data['id'], data['srcId'])
            data['buffKey'] = buffKey
            buffKeySet.add(buffKey)
            if data['type'] == 1 or data['type'] == 3:
                deBuffNum = deBuffNum + 1
                if deBuffNum >= 8:
                    continue
            else:
                buffNum = buffNum + 1
                if buffNum >= 8:
                    continue
            if buffKey not in buffDataDict:
                buffDataDict[buffKey] = data

        buffData = buffDataDict.values()
        buffData.sort(cmp=self.cmpBuff)
        if gameglobal.rds.ui.teamComm.teamPlayerMed:
            if not oldBuffKeySet and not oldBuffKeySet:
                refresh = True
            if not refresh:
                delBuff = list(oldBuffKeySet - buffKeySet)
            gameglobal.rds.ui.teamComm.updateBuffData(entity.roleName, buffData, delBuff, refresh)
            self.memberBuffState[entity.gbId] = (newSet, buffKeySet)

    def cmpBuff(self, e1, e2):
        if e1['priority'] != e2['priority']:
            return cmp(e1['priority'], e2['priority'])
        else:
            timer1 = e1['timer']
            timer2 = e2['timer']
            if timer1 == -100:
                timer1 = 999999
            if timer2 == -100:
                timer2 = 999999
            return cmp(timer1, timer2)

    def _refreshMemberBuffState(self, refreshType = 0):
        if not hasattr(self, 'memberBuffState'):
            return
        battleFieldTeam = getattr(self, 'battleFieldTeam', {})
        arenaTeam = getattr(self, 'arenaTeam', {})
        if refreshType:
            self.memberBuffState = {}
            return
        delList = []
        for gbId in self.memberBuffState:
            members = getattr(self, 'members', {})
            if refreshType == 0:
                if gbId not in members and not battleFieldTeam.has_key(gbId) and not arenaTeam.has_key(gbId):
                    delList.append(gbId)

        for gbId in delList:
            del self.memberBuffState[gbId]

    def isInMyTeamByGbId(self, tgtGbId):
        try:
            if self.isInPUBG():
                srcIndex = self.arrangeDict.get(self.gbId, -1)
                tgtIndex = self.arrangeDict.get(tgtGbId, -1)
            elif self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
                srcIndex = self.bfArrange.index(self.gbId)
                tgtIndex = self.bfArrange.index(tgtGbId)
            elif self.isInLueYingGu():
                srcIndex = self.pvpArrange.index(self.gbId)
                tgtIndex = self.pvpArrange.index(tgtGbId)
            else:
                srcIndex = self.arrangeDict.get(self.gbId, -1)
                tgtIndex = self.arrangeDict.get(tgtGbId, -1)
                if srcIndex < 0 or tgtIndex < 0:
                    return False
            if srcIndex / const.TEAM_MAX_NUMBER == tgtIndex / const.TEAM_MAX_NUMBER:
                return True
            return False
        except:
            return False

    def onInviteGroupFollow(self):
        """
        \xe9\x98\x9f\xe5\x91\x98\xe6\x94\xb6\xe5\x88\xb0\xe9\x98\x9f\xe9\x95\xbf\xe7\x9a\x84\xe5\x8f\xac\xe5\x94\xa4\xe8\xb7\x9f\xe9\x9a\x8f\xe8\xaf\xb7\xe6\xb1\x82
        Returns:
        
        """
        gamelog.debug('@zq impPlayerTeam follow#onInviteGroupFollow:')
        gameglobal.rds.ui.groupFollowHeaderCall.show()

    def onSyncInGroupFollow(self, info):
        """
        \xe5\x90\x8c\xe6\xad\xa5\xe5\x90\x84\xe4\xb8\xaa\xe9\x98\x9f\xe5\x91\x98\xe7\x9a\x84\xe8\xb7\x9f\xe9\x9a\x8f\xe7\x8a\xb6\xe6\x80\x81
        Args:
            info:
        
        Returns:
        
        """
        gamelog.debug('@zq impPlayerTeam follow#onSyncInGroupFollow:', info)
        for gbId, flag in info.iteritems():
            if self.members.has_key(gbId):
                self.members[gbId]['inGroupFollow'] = flag

        gameglobal.rds.ui.teamComm.refreshMemberInfo()

    def onQueryGroupHeaderFollowInfo(self, info):
        """
        \xe9\x98\x9f\xe9\x95\xbf\xe4\xbd\x8d\xe7\xbd\xae\xe3\x80\x81\xe9\x80\x9f\xe5\xba\xa6\xe4\xbf\xa1\xe6\x81\xaf\xe7\x9a\x84\xe5\x90\x8c\xe6\xad\xa5
        Args:
            info: {
                gametypes.TEAM_SYNC_PROPERTY_POSITION:(header.position[0],header.position[1],header.position[2]),
                gametypes.TEAM_SYNC_PROPERTY_SPEED: header.speed,
            }
        speed\xe5\x8f\x82\xe8\x80\x83iAvatarMotion.def\xe4\xb8\xadspeed\xe7\x9a\x84\xe5\xae\x9a\xe4\xb9\x89
        Returns:
        
        """
        gamelog.debug('@zq impPlayerTeam follow#onQueryGroupHeaderFollowInfo:', info)
        self.gourpFollowTime = 0
        self.clientGroupFollowInfo = info
        headerEnt = BigWorld.entity(self.groupHeader)
        if headerEnt:
            self.clientGroupFollowInfo[gametypes.TEAM_SYNC_PROPERTY_POSITION] = headerEnt.position
        self.updateGroupFollowPathFinding()

    def beginGroupFollow(self):
        if self.canRecoverGroupFollow():
            self.clientGroupFollowInfo = {}
            self.groupFollow()
        elif not self.checkTempGroupFollow():
            self.clientGroupFollowInfo = {}
            self.groupFollow()

    def groupFollow(self):
        if self.isRealGroupFollow():
            if not hasattr(self, 'gourpFollowTime'):
                self.gourpFollowTime = 0
            if not hasattr(self, 'groupFollowSpeedState'):
                self.groupFollowSpeedState = self.isGroupSyncSpeed()
            if self.groupFollowSpeedState != self.isGroupSyncSpeed():
                self.groupFollowSpeedState = self.isGroupSyncSpeed()
                self._setSpeedFunc()
            if self.isGroupSyncSpeed() and not self.qinggongState == gametypes.QINGGONG_STATE_DEFAULT:
                cellCmd.endUpQinggongState()
            if not self.gourpFollowTime == -1:
                self.gourpFollowTime += const.GROUPFOLLOW_INTERVAL
            BigWorld.callback(const.GROUPFOLLOW_INTERVAL, Functor(self.groupFollow))
            if self.clientGroupFollowInfo and self.isRealGroupFollow():
                distance = 0.1
                desireDist = 1
                dirVector = ()
                headerPosition = self.getGroupFollowHeaderPosition()
                headerSpaceNo = self.getGroupFollowHeaderSpaceNo()
                dirVector = self.position - headerPosition
                length = dirVector.length
                limitData = SCD.data.get('groupFollowSyncLimitTime', {})
                limitNum = 0
                maxLimit = 0
                for k, v in limitData.iteritems():
                    if utils.inRange(k, length):
                        limitNum = v
                    if v > maxLimit:
                        maxLimit = v

                if not limitNum:
                    limitNum = maxLimit
                if self.gourpFollowTime >= limitNum or self.gourpFollowTime == -1:
                    self.cell.queryGroupHeaderFollowInfo(self.headerGbId, self.groupHeader)
            else:
                self.cell.queryGroupHeaderFollowInfo(self.headerGbId, self.groupHeader)
        else:
            if not self.delayGroupFollow:
                navigator.getNav().stopPathFinding(False)
            if self.ap.isTracing:
                self.ap.isTracing = False
                self.ap.clearChaseData()

    def updateGroupFollowPathFinding(self):
        if self.isRealGroupFollow():
            endDist = 1.0
            dirVector = ()
            headerPosition = self.getGroupFollowHeaderPosition()
            headerSpaceNo = self.getGroupFollowHeaderSpaceNo()
            dirVector = self.position - headerPosition
            length = dirVector.length
            dirVector.y = 0
            horizonLength = dirVector.length
            groupFollowSyncTraceRange = SCD.data.get('groupFollowSyncTraceRange', 30)
            traceRange = groupFollowSyncTraceRange.get(const.GROUPFOLLOW_SPEED_RANGE_FOOT, 0)
            headerEnt = BigWorld.entity(self.groupHeader)
            if headerEnt:
                if headerEnt.inFly:
                    traceRange = groupFollowSyncTraceRange.get(const.GROUPFOLLOW_SPEED_RANGE_FLY, 0)
                elif headerEnt.bianshen[0]:
                    traceRange = groupFollowSyncTraceRange.get(const.GROUPFOLLOW_SPEED_RANGE_RIDE, 0)
            else:
                traceRange = groupFollowSyncTraceRange.get(const.GROUPFOLLOW_SPEED_RANGE_FLY, 0)

            def _failedCB():
                self.gourpFollowTime = -1

            randomEndDis = random.randint(50, 150) * 0.01
            if self.canPathFindingWingWorld(headerSpaceNo):
                from helpers import wingWorld
                wingWorld.pathFinding((headerPosition[0],
                 headerPosition[1],
                 headerPosition[2],
                 headerSpaceNo), endDist=endDist, showMsg=False, fromGroupFollow=True, failedCallback=_failedCB)
            elif self.groupFollowHeaderInPathFinding:
                navigator.getNav().pathFinding((headerPosition[0],
                 headerPosition[1],
                 headerPosition[2],
                 headerSpaceNo), endDist=endDist, showMsg=False, fromGroupFollow=True, failedCallback=_failedCB)
            elif length < traceRange and headerEnt:
                if not self._groupFollowCheckCanFlyRide() and self.canEnterWingWithGorupFollow():
                    cellCmd.enterWingFly(False)
                else:
                    self.groupFollowTraceUpRiding()
                if not self.ap.isTracing:
                    self.followOtherAvatarWithDist(headerEnt, endDist + randomEndDis)
            elif length > endDist + 1.5 and horizonLength > endDist:
                navigator.getNav().pathFinding((headerPosition[0],
                 headerPosition[1],
                 headerPosition[2],
                 headerSpaceNo), endDist=endDist, showMsg=False, fromGroupFollow=True, failedCallback=_failedCB)
        else:
            navigator.getNav().stopPathFinding(False)
            if self.ap.isTracing:
                self.ap.isTracing = False
                self.ap.clearChaseData()

    def groupFollowTraceUpRiding(self):
        if not self.inFly and not self.inRiding() and hasattr(self, 'equipment') and self.equipment[gametypes.EQU_PART_RIDE] and not self.equipment[gametypes.EQU_PART_RIDE].isExpireTTL() and not formula.mapLimit(formula.LIMIT_RIDE, formula.getMapId(self.spaceNo)):
            return self.enterRide()
        return False

    def canEnterWingWithGorupFollow(self):
        if not self.inSwim and not self.inCombat and not self.inFly:
            equip = self.equipment[gametypes.EQU_PART_WINGFLY]
            if equip:
                if formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(self.spaceNo)):
                    return False
                if self.stateMachine.checkStatus(const.CT_OPEN_WINGFLY_CAST):
                    return True
        return False

    def getIsAllFollow(self):
        for k, v in self.members.iteritems():
            if v.get('id', None) == getattr(self, 'id', None):
                continue
            if not v.get('inGroupFollow', False):
                return False

        return True

    def getIsAllNotFollow(self):
        for k, v in self.members.iteritems():
            if v.get('id', None) == getattr(self, 'id', None):
                continue
            if v.get('inGroupFollow', False):
                return False

        return True

    def getIsAllMembersNotOnline(self):
        for k, v in self.members.iteritems():
            if v.get('id', None) == getattr(self, 'id', None):
                continue
            if v.get('isOn', False):
                return False

        return True

    def isGroupSyncSpeed(self):
        if self.clientGroupFollowInfo and self.inGroupFollow:
            hPosition = None
            headerEnt = BigWorld.entity(self.groupHeader)
            if headerEnt:
                hPosition = headerEnt.position
            if not hPosition:
                hPosition = self.getGroupFollowHeaderPosition()
            dirVector = self.position - hPosition
            length = dirVector.length
            groupFollowSyncSpeedRange = SCD.data.get('groupFollowSyncSpeedRange', 30)
            if length <= groupFollowSyncSpeedRange:
                return True
        return False

    def getGroupFollowHeaderSpaceNo(self):
        if self.groupFollowHeaderInPathFinding and self.groupFollowHeaderSpaceNo:
            return self.groupFollowHeaderSpaceNo
        if self.clientGroupFollowInfo:
            return self.clientGroupFollowInfo.get(gametypes.TEAM_SYNC_PROPERTY_SPACENO, 0)
        if self.groupFollowHeaderSpaceNo:
            return self.groupFollowHeaderSpaceNo
        return self.spaceNo

    def getGroupFollowHeaderPosition(self):
        headerPosition = None
        if self.groupFollowHeaderInPathFinding and self.groupFollowHeaderGroundPos and self.groupFollowHeaderSpaceNo:
            return self.groupFollowHeaderGroundPos
        else:
            if self.clientGroupFollowInfo:
                headerEnt = BigWorld.entity(self.groupHeader)
                pos = None
                if headerEnt:
                    pos = BigWorld.findDropPoint(self.spaceID, Math.Vector3(headerEnt.position[0], headerEnt.position[1] + 0.5, headerEnt.position[2]))
                    if pos:
                        pos = pos[0]
                if pos:
                    headerPosition = pos
                if not headerPosition and self.groupFollowHeaderGroundPos:
                    headerPosition = self.groupFollowHeaderGroundPos
                if not headerPosition:
                    headerPosition = self.clientGroupFollowInfo.get(gametypes.TEAM_SYNC_PROPERTY_POSITION, ())
                    headerSpaceNo = self.clientGroupFollowInfo.get(gametypes.TEAM_SYNC_PROPERTY_SPACENO, 0)
                    pos = None
                    if headerSpaceNo == self.spaceNo:
                        heightArray = (1, 5, 10, 20, 40, 100)
                        for h in heightArray:
                            pos = BigWorld.findDropPoint(self.spaceID, Math.Vector3(headerPosition[0], headerPosition[1] + h, headerPosition[2]))
                            if pos:
                                pos = pos[0]
                                break

                    if not pos:
                        pos = Math.Vector3(headerPosition[0], navigator.UNKNOWN_Y, headerPosition[2])
                    if pos:
                        headerPosition = pos
            if not headerPosition:
                headerPosition = self.position
            return headerPosition

    def syncHeaderClientGroundPos(self, x = 0, y = 0, z = 0, spaceNo = 0, delayTime = 0, force = False):
        if self.id == getattr(self, 'groupHeader', None):
            if self.groupFollowHeaderPathCallback:
                gamelog.debug('bgf@impPlayerTeam syncHeaderClientGroundPos', self.groupFollowHeaderPathCallback)
                BigWorld.cancelCallback(self.groupFollowHeaderPathCallback)
                self.groupFollowHeaderPathCallback = None
            if delayTime:
                self.groupFollowHeaderPathCallback = BigWorld.callback(delayTime, Functor(self._syncHeaderClientGroundPos, x, y, z, spaceNo, force))
            else:
                self._syncHeaderClientGroundPos(x, y, z, spaceNo, force)

    def _syncHeaderClientGroundPos(self, x = 0, y = 0, z = 0, spaceNo = 0, force = False):
        if self.id != getattr(self, 'groupHeader', None):
            return
        else:
            isAllNotFollow = self.getIsAllNotFollow()
            if isAllNotFollow:
                return
            if self.isPathfinding and spaceNo == 0:
                return
            if not self.isPathfinding:
                pos = BigWorld.findDropPoint(self.spaceID, Math.Vector3(self.position[0], self.position[1] + 0.5, self.position[2]))
                if pos:
                    pos = pos[0]
                    x, y, z = pos
                else:
                    x, y, z = self.position
                spaceNo = self.spaceNo
            enabledPath = gameglobal.rds.configData.get('enableGroupFollowHeaderPath')
            if enabledPath and self.headerPathCache and self.isPathfinding == self.headerPathCache[4] and spaceNo == self.headerPathCache[3]:
                newPos = Math.Vector3(x, y, z)
                oldPos = Math.Vector3(self.headerPathCache[:3])
                if (newPos - oldPos).length < 2:
                    return
            gamelog.debug('bgf@impPlayerTeam _syncHeaderClientGroundPos', x, y, z, spaceNo, self.isPathfinding, self.id)
            if force:
                self.cell.syncHeaderClientPosForcely(x, y, z, spaceNo, self.isPathfinding)
            else:
                self.cell.syncHeaderClientPos(x, y, z, spaceNo, self.isPathfinding)
            self.headerPathCache = (x,
             y,
             z,
             spaceNo,
             self.isPathfinding)
            return

    def _groupFollowCheckCanFlyRide(self):
        if self.equipment.get(gametypes.EQU_PART_RIDE) and self.equipment.get(gametypes.EQU_PART_RIDE).isExpireTTL():
            return False
        if not self.isOnFlyRide():
            return False
        if not self.equipment.get(gametypes.EQU_PART_RIDE).haveTalent(gametypes.RIDE_TALENT_FLYRIDE):
            return False
        if formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(self.spaceNo)) and not self._checkWWArmyCanFlyRide():
            return False
        return True

    def isGroupInAction(self, excludeMe = True):
        for gbId, mVal in self.members.iteritems():
            if excludeMe and gbId == self.gbId:
                continue
            if mVal['isOn']:
                e = BigWorld.entities.get(mVal['id'])
                if e and e.groupActionState == gametypes.GROUP_ACTION_STATE_IN:
                    return True

        return False

    def set_groupActionState(self, old):
        if self.groupActionState == gametypes.GROUP_ACTION_STATE_NONE:
            if gameglobal.rds.ui.pressKeyF.isMonster == True:
                gameglobal.rds.ui.pressKeyF.removeType(const.F_MONSTER)
                gameglobal.rds.ui.pressKeyF.setType(const.F_MONSTER)
            elif gameglobal.rds.ui.pressKeyF.monster:
                gameglobal.rds.ui.pressKeyF.monster.triggerTrap(True)
                if not gameglobal.rds.ui.pressKeyF.isMonster:
                    gameglobal.rds.ui.pressKeyF.monster = None
        elif self.groupActionState == gametypes.GROUP_ACTION_STATE_PREPARE:
            if gameglobal.rds.ui.pressKeyF.isMonster == True:
                gameglobal.rds.ui.pressKeyF.removeType(const.F_MONSTER)
                gameglobal.rds.ui.pressKeyF.setType(const.F_MONSTER)
        elif self.groupActionState == gametypes.GROUP_ACTION_STATE_IN:
            if gameglobal.rds.ui.pressKeyF.isMonster == True:
                gameglobal.rds.ui.pressKeyF.isMonster = False
                gameglobal.rds.ui.pressKeyF.removeType(const.F_MONSTER)
        elif self.groupActionState == gametypes.GROUP_ACTION_STATE_DONE:
            gameglobal.rds.ui.pressKeyF.monster = None
            self.groupActionState = gametypes.GROUP_ACTION_STATE_NONE

    def groupFollowTraceFail(self):
        headerPosition = None
        endDist = 1.5
        if self.inGroupFollow and self.clientGroupFollowInfo:
            headerPosition = self.getGroupFollowHeaderPosition()
            headerSpaceNo = self.getGroupFollowHeaderSpaceNo()

            def _failedCB():
                self.gourpFollowTime = -1

        if not headerPosition:
            return
        else:
            navigator.getNav().pathFinding((headerPosition[0],
             headerPosition[1],
             headerPosition[2],
             headerSpaceNo), endDist=endDist, showMsg=False, fromGroupFollow=True, failedCallback=_failedCB)
            return

    def quickGroupFollow(self, isDown):
        if isDown and gameglobal.rds.ui.teamComm.teamPlayerMed:
            if self.isInTeam() and (not self.isInGroup() or gameconfigCommon.enableNewGroupFollow()):
                if self.isHeader():
                    if not self.getIsAllFollow():
                        gameglobal.rds.ui.teamComm.onInviteGroupFollow()
                else:
                    gameglobal.rds.ui.teamComm.onGroupFollowMember()

    def setTempGroupFollow(self):
        if self.inGroupFollow or getattr(self, 'delayGroupFollow', None):
            delayGroupFollowTime = SCD.data.get('tempGroupFollowDelayTime', 5)
            self.setDelayGroupFollowState(True)
            if self.ap.isTracing:
                self.ap.isTracing = False
                self.ap.clearChaseData()
            callbackId = getattr(self, 'delayGroupFollowCB', 0)
            if callbackId:
                BigWorld.cancelCallback(callbackId)
            self.delayGroupFollowCB = BigWorld.callback(delayGroupFollowTime, self.applyDelayGroupFollow)

    def applyDelayGroupFollow(self):
        if self.delayGroupFollow and self.inGroupFollow:
            if not self.canRecoverGroupFollow():
                self.setTempGroupFollow()
            else:
                self.setDelayGroupFollowState(False)
                self.beginGroupFollow()
        else:
            self.setDelayGroupFollowState(False)

    def canRecoverGroupFollow(self):
        if self.ap.isAnyDirKeyDown() or loadingProgress.instance().inLoading or self.isPathfinding and not navigator.getNav().fromGroupFollow or self.isInvalidRecoverGroupFollowState() or getattr(self, 'isDoingAction', None) or self.groupFollowAutoAttackFlag:
            return False
        else:
            return True

    def isInvalidRecoverGroupFollowState(self):
        stats = SCD.data.get('invalidRecoverGroupFollowState', ())
        sm = getattr(self, 'stateMachine', None)
        if sm:
            for stat in stats:
                name = sm.getCheckMethod(stat)
                func = None
                if name:
                    func = getattr(sm, name, None)
                if func and func():
                    return True

        return False

    def isRealGroupFollow(self):
        return getattr(self, 'inGroupFollow', False) and not getattr(self, 'delayGroupFollow', False)

    def canTempGroupFollow(self):
        enabled = gameglobal.rds.configData.get('enableTempGroupFollow', False)
        return enabled

    def checkTempGroupFollow(self, bMsg = True, msgType = GMDD.data.GROUPFOLLOW_FORBIDDEN_MOVE, srcType = const.DELAY_GROUP_FOLLOW_MANUAL):
        if getattr(self, 'inGroupFollow', None):
            if self.canTempGroupFollow():
                if self.delayGroupFollowType:
                    if self.delayGroupFollowType < srcType:
                        return False
                    self.delayGroupFollowType = srcType
                else:
                    self.delayGroupFollowType = srcType
                self.setTempGroupFollow()
                self._setSpeedFunc()
                return True
            else:
                if bMsg:
                    self.showGameMsg(msgType, ())
                return False
        return True

    def setDelayGroupFollowState(self, state):
        self.delayGroupFollow = state
        flag = gametypes.GROUP_FOLLOW_TEMPORARY_OUT if state else gametypes.GROUP_FOLLOW_TEMPORARY_DEFAULT
        if not state:
            self.delayGroupFollowType = const.DELAY_GROUP_FOLLOW_NONE
        self.cell.setTemporaryGroupFollowOut(state)

    def checkGroupFollowDelayPriority(self, dType):
        if self.delayGroupFollowType and self.delayGroupFollowType < dType:
            return False
        return True

    def canGroupFollowAutoAttack(self):
        if not gameglobal.rds.configData.get('enableGroupFollowAutoAttack', False):
            return False
        if not uiUtils.hasVipBasic():
            return
        if not int(AppSettings.get(keys.SET_UI_GROUP_FOLLOW_AUTO_ATTACK_PATH, 1)):
            return False
        if not self.checkGroupFollowDelayPriority(const.DELAY_GROUP_FOLLOW_AUTOATTACK):
            return False
        return MCD.data.get(formula.getMapId(self.spaceNo), {}).get('canGroupFollowAutoAttack', 0)

    def startGroupFollowAutoAttack(self):
        self.groupFollowAutoAttackFlag = False
        if not getattr(self, 'inGroupFollow', False) and not getattr(self, 'delayGroupFollow', False):
            return
        elif not self.canGroupFollowAutoAttack():
            return
        else:
            for memberGbId in self.members:
                if self.members.get(memberGbId, {}).get('isHeader', False):
                    ent = BigWorld.entities.get(self.members.get(memberGbId, {}).get('id', 0))
                    if not getattr(ent, 'inCombat', 0):
                        return
                    lockedId = getattr(ent, 'lockedId', 0) if ent else 0
                    target = BigWorld.entities.get(lockedId, None)
                    if not target:
                        target = self.autoSkill.getTarget()
                        if not target:
                            return
                    if self.isEnemy(target):
                        uiUtils.onTargetSelect(target)
                        self.groupFollowAutoAttackFlag = True
                        self.autoSkill.start()
                    return

            return

    def stopGroupFollowAutoAttack(self):
        self.groupFollowAutoAttackFlag = False

    def onSyncClientTeamCCInfo(self, clientTeamCCInfo):
        """
        \xe5\x85\xb7\xe4\xbd\x93\xe5\x8d\x8f\xe8\xae\xae\xe7\x9a\x84\xe6\xa0\xbc\xe5\xbc\x8f\xef\xbc\x8c\xe5\x8f\xaf\xe4\xbb\xa5\xe5\x8f\x82\xe8\x80\x83\xef\xbc\x9ahttp://km.netease.com/wiki/show?page_id=7918
        Args:
            clientTeamCCInfo:
        
        Returns:
        
        """
        gamelog.debug('@zmm cc#onSyncClientTeamCCInfo:', clientTeamCCInfo)
        ccManager.instance().registerTeamInfo(clientTeamCCInfo)

    def checkTeamInfo(self):
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_ARENA):
            gameglobal.rds.ui.teamComm.refreshMemberInfo(False)
            gameglobal.rds.ui.teamEnemyArena.refreshMemberInfo(False)
        elif p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            gameglobal.rds.ui.teamComm.refreshMemberInfo(False)
            gameglobal.rds.ui.group.refreshGroupInfo()
        elif p.isInTeam():
            gameglobal.rds.ui.teamComm.refreshMemberInfo(False)
        elif p.isInGroup():
            gameglobal.rds.ui.teamComm.refreshMemberInfo(False)
            gameglobal.rds.ui.group.refreshGroupInfo()
