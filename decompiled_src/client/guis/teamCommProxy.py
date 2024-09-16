#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/teamCommProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import uiUtils
import groupUtils
import gametypes
import formula
import keys
import utils
import gameconfigCommon
from ui import gbk2unicode
from teamBaseProxy import TeamBaseProxy
from callbackHelper import Functor
from gamestrings import gameStrings
from guis import hotkeyProxy
from guis import hotkey
from guis import ui
from appSetting import Obj as AppSettings
from data import school_data as SD
from data import sys_config_data as SCD
from data import arena_mode_data as AMD
from data import fb_data as FD
from data import photo_border_data as PBD
from cdata import game_msg_def_data as GMDD
PHOTO_MODE_DETAIL = 1
PHOTO_MODE_SIMPLE = 2

class TeamCommProxy(TeamBaseProxy):

    def __init__(self, uiAdapter):
        super(TeamCommProxy, self).__init__(uiAdapter)
        self.modelMap = {'getMemberInfo': self.onGetMemberInfo,
         'selectTeamPlayer': self.onSelectTeamPlayer,
         'clickGroupMatchMini': self.onClickGroupMatchMini,
         'clickGroupMatchCancel': self.onClickGroupMatchCancel,
         'getGroupMatchInfo': self.onGetGroupMatchInfo,
         'getApplyerInfo': self.onGetApplyerInfo,
         'acceptGroup': self.onAcceptApplyGroup,
         'rejectGroup': self.onRejectApplyGroup,
         'getPage': self.onGetPage,
         'changePage': self.onChangePage,
         'applyTimeOut': self.onApplyTimeOut,
         'isTeamLeader': self.onIsTeamLeader,
         'getWaitingTime': self.onGetWaitingTime,
         'getLocationTip': self.onGetLocationTip,
         'clickTeamBagIcon': self.onClickTeamBagIcon,
         'getInitInfo': self.onGetInitInfo,
         'setAssignMode': self.onSetAssignMode,
         'freshBuffInfo': self.freshBuffInfo,
         'shareTeamInfo': self.onShareTeamInfo,
         'switchCamera': self.onSwitchCamera,
         'hornCoolDown': self.onHornCoolDown,
         'inviteGroupFollow': self.onInviteGroupFollow,
         'cancelGroupFollow': self.onCancelGroupFollow,
         'groupFollowMember': self.onGroupFollowMember,
         'getGroupFollowInfo': self.onGetGroupFollowInfo,
         'isInTeam': self.onIsInTeam,
         'isInGroup': self.onIsInGroup,
         'callMember': self.onCallMember,
         'getCallMemberCd': self.onGetCallMemberCd,
         'getGroupFollowHotkeyDesc': self.onGetGroupFollowHotkeyDesc,
         'getGroupFollowConfig': self.onGetGroupFollowConfig,
         'setGroupFollowConfig': self.onSetGruopFollowConfig,
         'isInFullTeam': self.onIsInFullTeam,
         'handleInvitePlayer': self.onHandleInvitePlayer,
         'handleVoiceSetting': self.onHandleVoiceSetting,
         'getPhotoMode': self.onGetPhotoMode,
         'setPhotoMode': self.onSetPhotoMode}
        self.teamType = uiConst.COMMON_TEAM
        self.teamPlayerMed = None
        self.groupMatchMed = None
        self.groupMatchMini = False
        self.castTestHandler = None
        self.canCastSkillList = []
        self.timer = None
        self.photoMode = PHOTO_MODE_DETAIL
        self.reset()
        uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GROUP_MATCHED, {'click': self.clickPushIcon})

    def onShareTeamInfo(self, *arg):
        p = BigWorld.player()
        if not uiUtils.checkShareTeamLvLimit():
            teamInfoUseLv = SCD.data.get('teamInfoUseLv', 20)
            p.showGameMsg(GMDD.data.TEAM_INFO_LV_LIMIT, (teamInfoUseLv,))
            return
        if p.headerGbId != p.gbId:
            BigWorld.player().showGameMsg(GMDD.data.SHARE_TEAM_ONLY_LEADER, ())
            return
        if self.uiAdapter.team.hasGoal():
            msg = gameglobal.rds.ui.team.getShareTeamInfoMsg()
            p.cell.chatToGroupInfo(msg)
            self.setHornStartCoolDown()
        else:
            gameglobal.rds.ui.createTeamV2.show()

    def onHornCoolDown(self, *arg):
        if gameglobal.rds.ui.team.isAutoShare:
            self.timer = BigWorld.callback(uiConst.SHARE_TEAM_INFO_CD, self.afterHornEndCoolDown)
            if self.teamPlayerMed:
                self.teamPlayerMed.Invoke('setHornStartCoolDown')

    def refreshHornBtnTipsInfo(self):
        if self.teamPlayerMed:
            tips = self.uiAdapter.team.getShareBtnTipsInfo()
            self.teamPlayerMed.Invoke('refreshHornBtnTips', GfxValue(gbk2unicode(tips)))

    def onSwitchCamera(self, *arg):
        targetEntId = int(arg[3][0].GetNumber())
        targetGbId = int(arg[3][1].GetString())
        p = BigWorld.player()
        if targetEntId == getattr(p, 'gmFollow', 0):
            return
        if p.isInPUBG():
            p.cell.pubgObserve(targetEntId, targetGbId)
        else:
            p.cell.obSpecificTgt(targetEntId)

    def reset(self):
        self.pageIndex = 0
        self.modifyIsOpen = False
        self.srcGbId = 0
        self.canCastSkillList = []
        self._resetPlayerProperty()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_COMM_TEAM_PLAYER:
            self.teamPlayerMed = mediator
            self.photoMode = AppSettings.get(keys.TEAM_COMMON_PHOTO_MODE, PHOTO_MODE_DETAIL)
            BigWorld.callback(0.2, self.refreshCanCastSkill)
        elif widgetId == uiConst.WIDGET_GROUP_MATCH:
            self.groupMatchMed = mediator

    def refreshCanCastSkill(self):
        if self.teamPlayerMed:
            ret = []
            p = BigWorld.player()
            if not p:
                return
            for value in self.memberId:
                ent = BigWorld.entities.get(value, None)
                canCastSkill = uiUtils.canCastSkill(ent)
                ret.append(canCastSkill)

            if self.canCastSkillList != ret:
                self.canCastSkillList = ret
                self.teamPlayerMed.Invoke('refreshCanCastSkill', uiUtils.array2GfxAarry(ret))
            self.castTestHandler = BigWorld.callback(0.2, self.refreshCanCastSkill)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.teamPlayerMed = None
        if self.castTestHandler:
            BigWorld.cancelCallback(self.castTestHandler)
        self.castTestHandler = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_COMM_TEAM_PLAYER)

    def closeTeamPlayer(self):
        super(TeamCommProxy, self).closeTeamPlayer()
        self.stopTimer()
        self.teamPlayerMed = None
        if self.castTestHandler:
            BigWorld.cancelCallback(self.castTestHandler)
        self.castTestHandler = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_COMM_TEAM_PLAYER)
        self._resetPlayerProperty()

    def _findTeamName(self, index):
        groupType = gameglobal.rds.ui.team.groupType
        p = BigWorld.player()
        teamIndex = 0
        for i, info in enumerate(p.teamsInfo):
            if info[8] != groupType:
                continue
            if teamIndex == index:
                return gbk2unicode(info[0])
            teamIndex += 1

        return gbk2unicode('')

    def _findTeamIndex(self, idx):
        groupType = gameglobal.rds.ui.team.groupType
        p = BigWorld.player()
        if not hasattr(p, 'teamsInfo') or idx == -1:
            return -1
        teams = filter(lambda x: x[8] == groupType, p.teamsInfo)
        if idx >= len(teams):
            return -1
        return p.teamsInfo.index(teams[idx])

    def getMemberASValue(self, index, key, value, isNearby = None):
        p = BigWorld.player()
        if not p._checkValidSchool(value['school']):
            return
        else:
            valueId = value['id']
            isHeadLeader = getattr(p, 'headerGbId', None) == key
            groupFollowFlag = p.groupFollowTempOutInfo.get(key, False)
            groupFollowState = 'follow'
            lv = value['level']
            isNearby = isNearby if isNearby != None else BigWorld.entities.has_key(valueId)
            canSwitchCam = True
            reliveTime = 0
            isDied = False
            if groupFollowFlag == gametypes.GROUP_FOLLOW_TEMPORARY_OUT:
                groupFollowState = 'fight'
            if self.teamType == uiConst.COMMON_TEAM:
                if valueId and valueId == p.id:
                    return
                if not groupUtils.isInSameTeam(p.gbId, key) and not p.inFightObserve():
                    return
                if p.isInPUBG() and p.checkTeammateDeadInPUBG(key):
                    canSwitchCam = False
            elif self.teamType == uiConst.ARENA_TEAM:
                if valueId == p.id or value['sideNUID'] != p.sideNUID:
                    return
                if not value['isIn']:
                    return
                isHeadLeader = False
                groupFollowState = ''
                fbNo = formula.getFubenNo(p.spaceNo)
                arenaMode = formula.fbNo2ArenaMode(fbNo)
                if AMD.data.get(arenaMode, {}).get('needReCalcLv', 0):
                    lv = formula.calcArenaLv(arenaMode, value['level'])
                else:
                    lv = value['level']
                reliveTime = 0
            elif self.teamType == uiConst.BATTLEFIELD_TEAM:
                if valueId == p.id or value['sideNUID'] != p.bfSideNUID:
                    return
                if not p.isSameBFTeam(key):
                    return
                isHeadLeader = False
                groupFollowState = ''
                if not value['isIn']:
                    return
                if value['isConfirmRelive']:
                    reliveTime = uiUtils.getBFReliveTime(value)
                isDied = value['life'] == gametypes.LIFE_DEAD
            ent = BigWorld.entities.get(valueId, None)
            canCastSkill = uiUtils.canCastSkill(ent) and isNearby
            if p.targetLocked:
                selected = p.targetLocked.id == valueId
            else:
                selected = False
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(gbk2unicode(value['roleName'])))
            ar.SetElement(1, GfxValue(lv))
            ar.SetElement(2, GfxValue(value['school']))
            ar.SetElement(3, GfxValue(isHeadLeader))
            ar.SetElement(4, self.getHp(index, valueId))
            ar.SetElement(5, self.getMhp(index, valueId))
            ar.SetElement(6, self.getMp(index, valueId))
            ar.SetElement(7, self.getMmp(index, valueId))
            ar.SetElement(8, self.getBuffList())
            ar.SetElement(9, GfxValue(value['isOn']))
            ar.SetElement(10, GfxValue(True))
            ar.SetElement(11, GfxValue(int(valueId)))
            ar.SetElement(12, GfxValue(str(key)))
            ar.SetElement(13, GfxValue(canCastSkill))
            ar.SetElement(14, GfxValue(selected))
            ar.SetElement(15, GfxValue(isDied))
            ar.SetElement(16, GfxValue(reliveTime))
            ar.SetElement(17, GfxValue(p.gmFollow))
            ar.SetElement(18, GfxValue(bool(p.gmFollow and p.gmFollow == value.get('id', None))))
            ar.SetElement(19, GfxValue(canSwitchCam))
            ar.SetElement(20, GfxValue(value.get('inGroupFollow', False)))
            ar.SetElement(21, GfxValue(gbk2unicode(groupFollowState)))
            ar.SetElement(22, GfxValue(value.get('ccMode', 0)))
            borderId = value.get('borderId', 1)
            ar.SetElement(23, GfxValue(gbk2unicode(p.getPhotoBorderIcon(borderId, uiConst.PHOTO_BORDER_ICON_SIZE40), True)))
            defaultPhoto = 'headIcon/%s.dds' % str(value['school'] * 10 + value['sex'])
            ar.SetElement(24, GfxValue(gbk2unicode(defaultPhoto, True)))
            prefixBg = PBD.data.get(borderId, {}).get('prefixBg', 'normal')
            ar.SetElement(25, GfxValue(gbk2unicode(prefixBg)))
            ar.SetElement(26, GfxValue(p.getTeammateNoInPUBG(key)))
            return ar

    def onGetMemberInfo(self, *arg):
        p = BigWorld.player()
        listInfo = self.movie.CreateArray()
        index = 0
        memberList = []
        if self.teamType == uiConst.COMMON_TEAM:
            if hasattr(p, 'headerGbId') and p.headerGbId == p.gbId:
                flag = True
            else:
                flag = False
            gameglobal.rds.ui.player.setLeaderIcon(flag)
            memberList = p._getSortedMembers()
        elif self.teamType == uiConst.ARENA_TEAM:
            memberList = p.arenaTeam.items()
        elif self.teamType == uiConst.BATTLEFIELD_TEAM:
            memberList = p.battleFieldTeam.items()
        elif self.teamType == uiConst.SSC_TEAM:
            pass
        for key, value in memberList:
            valueId = value['id']
            ar = self.getMemberASValue(index, key, value)
            if not ar:
                continue
            listInfo.SetElement(index, ar)
            self.memberId[index] = valueId
            self.roleNameList[index] = value['roleName']
            listInfo.SetElement(index, ar)
            self.memberId[index] = valueId
            index += 1

        for i in xrange(index, const.TEAM_MAX_NUMBER):
            self._resetPropertyByIndex(i)

        ret = self.movie.CreateArray()
        ret.SetElement(0, GfxValue(self.teamType))
        ret.SetElement(1, listInfo)
        showCam = p.inFightObserve()
        ret.SetElement(2, GfxValue(showCam))
        return ret

    def refreshSingleMember(self, key, isNearby = None):
        if not self.teamPlayerMed:
            return
        else:
            p = BigWorld.player()
            value = None
            if self.teamType == uiConst.COMMON_TEAM:
                value = p.members.get(key, None)
            elif self.teamType == uiConst.ARENA_TEAM:
                value = p.arenaTeam.get(key, None)
            elif self.teamType == uiConst.BATTLEFIELD_TEAM:
                value = p.battleFieldTeam.get(key, None)
            if not value:
                return
            valueId = value.get('id', 0)
            if not valueId:
                return
            index = self._getTeamIndex(valueId)
            sameSideNuid = True
            if self.teamType == uiConst.BATTLEFIELD_TEAM:
                sameSideNuid = value['sideNUID'] == p.bfSideNUID
            elif self.teamType == uiConst.ARENA_TEAM:
                sameSideNuid = value['sideNUID'] == p.sideNUID
            if index == -1:
                if not sameSideNuid:
                    return
                else:
                    self.refreshMemberInfo(False)
                    return
            ar = self.getMemberASValue(index, key, value, isNearby)
            if ar:
                self.teamPlayerMed.Invoke('refreshMember', (GfxValue(index), ar, GfxValue(False)))
            return

    def refreshMemberInfo(self, isNeedOpen = True, refreshSelfWidget = True):
        p = BigWorld.player()
        super(TeamCommProxy, self).refreshMemberInfo(isNeedOpen, refreshSelfWidget)
        if not refreshSelfWidget:
            return
        if not p.inWorld:
            return
        if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD) and p.inLiveOfGuildTournament > 0:
            return
        if p.inFubenTypes(const.FB_TYPE_ARENA):
            self.teamType = uiConst.ARENA_TEAM
        elif p.isInPUBG():
            self.teamType = uiConst.COMMON_TEAM
        elif p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.teamType = uiConst.BATTLEFIELD_TEAM
        elif p.inFubenTypes(const.FB_TYPE_SHENGSICHANG_SET):
            self.teamType = uiConst.SSC_TEAM
        elif p.groupNUID > 0:
            self.teamType = uiConst.COMMON_TEAM
        elif p.inFightObserve():
            self.teamType = uiConst.COMMON_TEAM
        else:
            return
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('refreshInfo')
        elif isNeedOpen:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_COMM_TEAM_PLAYER)

    def onSelectTeamPlayer(self, *arg):
        index = int(arg[3][0].GetNumber())
        if index != -1:
            entity = self._getEntityById(self.memberId[index])
            uiUtils.onTargetSelect(entity)

    def hideMenu(self):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('hideMenu')

    def showApply(self, srcName, srcLevel, srcSchool, srcGbId, groupNUID, isSelf):
        self.groupNUID = groupNUID

    def _getPassingTime(self, index):
        p = BigWorld.player()
        return int(p.getServerTime() - p.applyer[index][3]) + 1

    def onGetApplyerInfo(self, *arg):
        index = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        ret = []
        if index < len(p.applyer):
            ret.append(p.applyer[index][0])
            ret.append(p.applyer[index][1])
            ret.append(p.applyer[index][2])
            ret.append(self._getPassingTime(index))
            ret.append(p.applyer[index][3] if len(p.applyer[index]) > 3 else 0)
        return uiUtils.array2GfxAarry(ret, True)

    def onApplyTimeOut(self, *arg):
        index = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if index < len(p.applyer):
            for i in xrange(index + 1):
                p.applyGroupOvertime(p.applyer[0][4])
                del p.applyer[0]

        self.refreshApplyer(index + 1)
        gameglobal.rds.ui.team.refreshApplyer()

    def onAcceptApplyGroup(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        if index < len(p.applyer):
            p.acceptApplyGroup(p.applyer[index][0], p.applyer[index][4])

    def onRejectApplyGroup(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        if index < len(p.applyer):
            p.rejectApplyGroup(p.applyer[index][0], p.applyer[index][4])

    def onGetPage(self, *arg):
        return GfxValue(self.getPage())

    def onIsTeamLeader(self, *arg):
        p = BigWorld.player()
        if p.isInTeamOrGroup() and p.groupHeader == p.id:
            return GfxValue(True)
        return GfxValue(False)

    def getPage(self):
        p = BigWorld.player()
        return len(p.applyer)

    def refreshApplyer(self, index = 0):
        page = self.getPage()
        if page == 0:
            self.removeApplyer()
            return
        index = index % page
        if index >= page:
            return
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('refreshApplyer', GfxValue(index))
        self.playShine()

    def playShine(self):
        if self.teamPlayerMed:
            if self.getPage() - 1 > self.pageIndex:
                self.teamPlayerMed.Invoke('playShine')
            else:
                self.teamPlayerMed.Invoke('playNormal')

    def onChangePage(self, *arg):
        self.pageIndex = int(arg[3][0].GetNumber())
        self.playShine()

    def removeApplyer(self):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('removeAppler')

    def setHit(self, id, hitNum):
        index = self._getTeamIndex(id)
        if index == -1:
            return
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('setHit', (GfxValue(index), GfxValue(hitNum)))

    def endHit(self):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('endHit')

    def setMvp(self, id):
        index = self._getTeamIndex(id)
        if index == -1:
            return
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('setMvp', GfxValue(index))
            BigWorld.callback(3, Functor(self.endMvp, id))

    def endMvp(self, id):
        index = self._getTeamIndex(id)
        if index == -1:
            return
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('endMvp', GfxValue(index))

    def showGroupMatch(self):
        if self.groupMatchMed:
            self.groupMatchMed.Invoke('refreshGroupMatch')
        else:
            if self.groupMatchMini:
                return
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GROUP_MATCH)

    def closeGroupMatch(self):
        self.groupMatchMed = None
        self.groupMatchMini = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GROUP_MATCH)

    def onGetWaitingTime(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.getServerTime() - p.groupMatchStartTime)

    def _getGroupMatchSchoolList(self):
        p = BigWorld.player()
        ar = self.movie.CreateArray()
        for index, value in enumerate(p.groupMatchMemberInfo):
            ar.SetElement(index, GfxValue(value['school']))

        return ar

    def onGetGroupMatchInfo(self, *arg):
        p = BigWorld.player()
        ret = self.movie.CreateObject()
        desc = uiUtils.getGroupMatchDesc()
        ret.SetMember('desc', GfxValue(gbk2unicode(desc)))
        ret.SetMember('cnt', GfxValue(len(p.groupMatchMemberInfo)))
        ret.SetMember('schoolList', self._getGroupMatchSchoolList())
        return ret

    def onClickGroupMatchMini(self, *arg):
        if self.groupMatchMed:
            self.closeGroupMatch()
        else:
            self.showGroupMatch()
        self.groupMatchMini = True

    def onClickGroupMatchCancel(self, *arg):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_TEAMCOMMPROXY_556, yesCallback=self.doCancelGroupMatch, yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)

    def doCancelGroupMatch(self):
        p = BigWorld.player()
        p.cancelGroupMatch()

    def getMembers(self):
        p = BigWorld.player()
        if p.isInPUBG():
            return p.members
        elif p.inFightObserve():
            return p.getObservedMembers()
        else:
            return p.members

    def clickPushIcon(self):
        self.groupMatchMini = False
        self.onClickGroupMatchMini()

    def _getSchoolDesc(self, gbId):
        p = BigWorld.player()
        desc = ''
        if not p.isInTeamOrGroup():
            return desc
        members = self.getMembers()
        if not members.has_key(gbId):
            return desc
        mVal = members[gbId]
        return gameStrings.TEXT_TEAMCOMMPROXY_584 + const.SCHOOL_DICT[mVal['school']]

    def onGetLocationTip(self, *arg):
        gbId = int(arg[3][0].GetString())
        desc = uiUtils.getLocationByGbId(gbId)
        if desc:
            desc += '\n' + self._getSchoolDesc(gbId)
        return GfxValue(gbk2unicode(desc))

    def setSelect(self, entId, selected):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('setSelect', (GfxValue(entId), GfxValue(selected)))

    def onClickTeamBagIcon(self, *arg):
        if gameglobal.rds.ui.assign.isTeamBagShow:
            gameglobal.rds.ui.assign.closeTeambag()
        else:
            gameglobal.rds.ui.assign.showTeambag()

    def _createAssignInfo(self):
        p = BigWorld.player()
        showBagEffect = not gameglobal.rds.ui.assign.isTeamBagEmpty()
        assignEnabled = p.isTeamLeader()
        rule = p.groupAssignWay
        quality = const.GROUP_ASSIGN_QUALITY[p.groupAssignQuality]
        ret = {'showBagEffect': showBagEffect,
         'assignEnabled': assignEnabled,
         'rule': rule,
         'quality': quality}
        return ret

    def setAssignInfo(self):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('setAssignInfo', uiUtils.dict2GfxDict(self._createAssignInfo()))
        BigWorld.player().refreshAssignMode()

    def onGetInitInfo(self, *arg):
        ret = self._createAssignInfo()
        ret['hornBtnTips'] = self.uiAdapter.team.getShareBtnTipsInfo()
        return uiUtils.dict2GfxDict(ret, True)

    def onSetAssignMode(self, *arg):
        assignRule = int(arg[3][0].GetNumber())
        assignQuality = int(arg[3][1].GetNumber())
        BigWorld.player().cell.setGroupAssign(assignRule, const.GROUP_ASSIGN_QUALITY[assignQuality])

    def refreshAssignMode(self):
        p = BigWorld.player()
        assignRule = p.groupAssignWay
        assignQuality = const.GROUP_ASSIGN_QUALITY[p.groupAssignQuality]
        ret = [assignRule, assignQuality]
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('refreshAssignMode', uiUtils.array2GfxAarry(ret))

    def setChatBubble(self, srcRole, msg):
        try:
            index = self.roleNameList.index(srcRole)
            bubbleDuration = SCD.data.get('bubbleDuration', 4)
        except:
            return

        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('setChatBubbleByIndex', (GfxValue(index), GfxValue(gbk2unicode(msg)), GfxValue(bubbleDuration)))

    def setHornStartCoolDown(self):
        self.timer = BigWorld.callback(uiConst.SHARE_TEAM_INFO_CD, self.afterHornEndCoolDown)
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('setHornStartCoolDown')

    def afterHornEndCoolDown(self):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('afterHornEndCoolDown')

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def onInviteGroupFollow(self, *arg):
        p = BigWorld.player()
        if p.getIsAllMembersNotOnline():
            p.showGameMsg(GMDD.data.GROUPFOLLOW_MEMBERS_NOT_ON, ())
            return
        p.cell.inviteGroupFollow()

    def onCancelGroupFollow(self, *arg):
        p = BigWorld.player()
        p.cell.cancelGroupFollow()

    def onGroupFollowMember(self, *arg):
        p = BigWorld.player()
        if p.inGroupFollow:
            p.cell.cancelGroupFollow()
        else:
            fbList = getattr(p, 'fbStatusList', [])
            fbList = self.uiAdapter.phaseFuben.filterFuben(fbList)
            headerSpaceNo = p.membersPos.get(p.headerGbId, (0,))[0]
            fbNo = formula.getFubenNo(headerSpaceNo)
            name = formula.whatLocationName(headerSpaceNo, '', includeMLInfo=True)
            pFbNo = formula.getFubenNo(p.spaceNo)
            if fbList and p.spaceNo != headerSpaceNo and not pFbNo:
                if fbNo:
                    fbInfo = FD.data.get(fbNo, {})
                    if fbInfo.get('isPushIcon', None):
                        self.uiAdapter.phaseFuben.openPhaseListByGroupFollow()
                        p.showGameMsg(GMDD.data.GROUPFOLLOW_ENTERFUBEN_MESSAGE, (name,))
                        return
            p.cell.applyGroupFollow()

    def onGetGroupFollowInfo(self, *arg):
        p = BigWorld.player()
        info = {}
        info['isHeader'] = p.isHeader()
        groupFollowMcType = 'zhaohuan'
        if p.isHeader():
            info['enabledFollow'] = not p.getIsAllFollow()
            info['enabledCancel'] = not p.getIsAllNotFollow()
            if p.isInTeam() and gameconfigCommon.enableCallTeamMember():
                groupFollowMcType = 'zhaohuan2'
            elif p.isInGroup() and gameconfigCommon.enableNewGroupFollow():
                groupFollowMcType = 'zhaohuan'
            else:
                groupFollowMcType = 'zhaohuan'
        else:
            if p.inGroupFollow:
                info['btnText'] = gameStrings.GROUP_FOLLOW_BTN_TEXT_CANCEL
            else:
                info['btnText'] = gameStrings.GROUP_FOLLOW_BTN_TEXT_FOLLOW if p.isInTeam() else gameStrings.GROUP_FOLLOW_BTN_TEXT_FOLLOW_GROUP
            hotKeyDesc = self.getGroupFollowHotkeyDesc()
            if hotKeyDesc:
                info['btnText'] = info['btnText'] % self.getGroupFollowHotkeyDesc().join(('(', ')'))
            else:
                info['btnText'] = info['btnText'] % ('',)
            groupFollowMcType = 'gensui'
        info['groupFollowMcType'] = groupFollowMcType
        return uiUtils.dict2GfxDict(info, True)

    def onIsInTeam(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.isInTeam())

    def onIsInGroup(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.isInGroup())

    def onCallMember(self, *arg):
        p = BigWorld.player()
        p.cell.callGroupFollow()

    def onGetCallMemberCd(self, *arg):
        p = BigWorld.player()
        cd = 0
        if hasattr(p, 'tCallTeamMemberExpire'):
            cd = max(p.tCallTeamMemberExpire - utils.getNow(), 0)
        formatStr = 'ss' if cd < const.TIME_INTERVAL_MINUTE else 'mm'
        timeStr = utils.formatTimeStr(cd, formatStr, replaceOnce=True)
        cdDesc = gameStrings.GROUP_FOLLOW_BTN_TEXT_CALL_CD % (timeStr,) if cd else gameStrings.GROUP_FOLLOW_BTN_TEXT_CALL
        notFollow = p.getIsAllNotFollow()
        info = {'cd': cd,
         'cdDesc': cdDesc,
         'notFollow': notFollow}
        return uiUtils.dict2GfxDict(info, True)

    def refreshCallMemberInfo(self):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('refreshCallMemberBtn')

    def onGetGroupFollowHotkeyDesc(self, *arg):
        hotKeyDesc = self.getGroupFollowHotkeyDesc()
        return GfxValue(gbk2unicode(gameStrings.GROUP_FOLLOW_HOTKEY % (hotKeyDesc,)))

    def getGroupFollowHotkeyDesc(self, *arg):
        _, _, hotKeyDesc = hotkeyProxy.getKeyContent(hotkey.KEY_GROUP_FOLLOW)
        return hotKeyDesc

    def onGetGroupFollowConfig(self, *arg):
        configData = {}
        configData['isAutoAccept'] = AppSettings.get(keys.SET_UI_GROUP_FOLLOW_AUTO_ACCEPT_SETTING_PATH, 1)
        configData['isAutoEnterFuben'] = AppSettings.get(keys.SET_UI_GROUP_FOLLOW_AUTO_ENTER_SETTING_PATH, 1)
        configData['isAutoAttack'] = AppSettings.get(keys.SET_UI_GROUP_FOLLOW_AUTO_ATTACK_PATH, 1)
        configData['isAutoAttackVisible'] = gameglobal.rds.configData.get('enableGroupFollowAutoAttack', False)
        configData['hasVipBasic'] = uiUtils.hasVipBasic()
        configData['vipTips'] = uiUtils.getTextFromGMD(GMDD.data.CAN_USE_AFTER_VIP_ACTIVATE_HINT, '')
        return uiUtils.dict2GfxDict(configData, True)

    def onSetGruopFollowConfig(self, *arg):
        selResult = int(arg[3][0].GetNumber())
        selType = arg[3][1].GetString()
        if selType == 'isAutoAccept':
            AppSettings[keys.SET_UI_GROUP_FOLLOW_AUTO_ACCEPT_SETTING_PATH] = selResult
        elif selType == 'isAutoEnterFuben':
            AppSettings[keys.SET_UI_GROUP_FOLLOW_AUTO_ENTER_SETTING_PATH] = selResult
        elif selType == 'isAutoAttack':
            AppSettings[keys.SET_UI_GROUP_FOLLOW_AUTO_ATTACK_PATH] = selResult
            if selResult == 0:
                BigWorld.player().stopGroupFollowAutoAttack()

    def onIsInFullTeam(self, *args):
        return GfxValue(BigWorld.player().isInFullTeam())

    def onHandleInvitePlayer(self, *args):
        gameglobal.rds.ui.invitePlayer.show()

    def onHandleVoiceSetting(self, *args):
        gameglobal.rds.ui.voiceSetting.show()

    def setSelfVoiceMode(self, mode):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('setSelfVoiceMode', GfxValue(mode))

    def setOtherVoiceMode(self, gbId, mode):
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('setOtherVoiceMode', (GfxValue(str(gbId)), GfxValue(mode)))

    def onGetPhotoMode(self, *args):
        return GfxValue(self.photoMode)

    @ui.callFilter(0.5)
    def onSetPhotoMode(self, *args):
        newMode = int(args[3][0].GetNumber())
        if newMode == self.photoMode:
            return
        AppSettings[keys.TEAM_COMMON_PHOTO_MODE] = newMode
        self.photoMode = newMode
        AppSettings.save()
        if self.teamPlayerMed:
            self.teamPlayerMed.Invoke('refreshInfo')
