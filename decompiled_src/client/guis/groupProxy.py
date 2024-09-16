#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/groupProxy.o
from gamestrings import gameStrings
import copy
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import gamelog
import uiUtils
import gametypes
import utils
import formula
from ui import gbk2unicode
from teamBaseProxy import TeamBaseProxy
from messageBoxProxy import MBButton
from guis.teamGoalMenuHelper import TeamGoalMenuHelper
from data import game_msg_data as GMD
from data import battle_field_data as BFD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD

class GroupProxy(TeamBaseProxy):

    def __init__(self, uiAdapter):
        super(GroupProxy, self).__init__(uiAdapter)
        self.modelMap = {'showTeamWidget': self.onShowTeamWidget,
         'getGroupInfo': self.onGetGroupInfo,
         'confirmGroup': self.onConfirmGroup,
         'promptAss': self.onPromptAss,
         'removeTeamate': self.onRemoveTeamate,
         'showGroupCreateInfo': self.onShowGroupCreateInfo,
         'closeGroupInfo': self.onCloseGroupInfo,
         'leaveGroup': self.onLeaveGroup,
         'getGroupTeamInfo': self.onGetGroupTeamInfo,
         'closeTeamWidget': self.onCloseTeamWidget,
         'changeLeader': self.onChangeLeader,
         'changeArrange': self.onChangeArrange,
         'changeAssignType': self.onChangeAssignType,
         'setSign': self.onSetSign,
         'cancelSign': self.onCancelSign,
         'getMark': self.onGetMark,
         'clickMemItem': self.onClickMemItem,
         'clickTeamIndex': self.onClickTeamIndex,
         'markScene': self.onMarkScene,
         'getLocationTip': self.onGetLocationTip,
         'goBackToHallClick': self.onGoBackToHallClick,
         'isTeamLeader': self.onIsTeamLeader,
         'doInviteCC': self.onInviteCC,
         'isShowCC': self.isShowCC,
         'getPrepareInfo': self.onGetPrepareInfo,
         'confirmPrepare': self.onConfirmPrepare,
         'clearPrepareInfo': self.onClearPrepareInfo,
         'initStartPrepareTime': self.onInitStartPrepareTime,
         'isEnablePrepare': self.onIsEnablePrepare,
         'getMemberUIScale': self.onGetMemberUIScale,
         'setMemberUIScale': self.onSetMemberUIScale,
         'shareTeamInfo': self.onShareTeamInfo,
         'isShowShareMenuBtn': self.onIsShowShareMenuBtn,
         'getEnableYecha': self.onGetEnableYecha,
         'handleInvitePlayer': self.onHandleInvitePlayer,
         'isCloseTeamGoal': self.onIsCloseTeamGoal,
         'getEnableTianzhao': self.onGetEnableTianzhao}
        self.groupInfoType = None
        self.groupInfoMed = None
        self.groupMemMed = None
        self.teamSet = set()
        self.isShow = False
        self.currentData = None
        self.currentMemData = {}
        self.markMapIndex = 1
        self.castTestHandler = None
        self.canCastSkillList = []
        self.askPrepareMsg = None
        self.startPrepareTime = None
        self.memberUIScale = 1
        uiAdapter.registerEscFunc(uiConst.WIDGET_GROUPINFO_PANEL, self.closeGroupInfoPanel)

    def onInviteCC(self, *arg):
        p = BigWorld.player()
        p.doInviteTeam()

    def onIsShowShareMenuBtn(self, *args):
        p = BigWorld.player()
        isShareEnable = gameglobal.rds.configData.get('enableTeamInfoShare', False)
        return GfxValue(isShareEnable and p.isTeamLeader())

    def onShareTeamInfo(self, *args):
        p = BigWorld.player()
        if not uiUtils.checkShareTeamLvLimit():
            teamInfoUseLv = SCD.data.get('teamInfoUseLv', 20)
            p.showGameMsg(GMDD.data.TEAM_INFO_LV_LIMIT, (teamInfoUseLv,))
            return
        gameglobal.rds.ui.team.onShareTeamInfo()
        p = BigWorld.player()
        if not hasattr(p, 'headerGbId'):
            return
        if p.headerGbId != p.gbId:
            return

    def isShowCC(self, *arg):
        isCCVersion = gameglobal.rds.configData.get('isCCVersion', False)
        return GfxValue(isCCVersion)

    def _registerMediator(self, widgetId, mediator):
        gamelog.debug('GroupProxy:', widgetId)
        if widgetId == uiConst.WIDGET_GROUPINFO_PANEL:
            self.groupInfoMed = mediator
        elif widgetId == uiConst.WIDGET_GROUPMEMBER:
            self.groupMemMed = mediator
            BigWorld.callback(0.2, self.refreshCanCastSkill)
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.groupInfoType = uiConst.GROUP_INFO_TYPE_BATTLEFIELD
        elif p.isInLueYingGu():
            self.groupInfoType = uiConst.GROUP_INFO_TYPE_NORMAL
        elif p.isInGroup():
            self.groupInfoType = uiConst.GROUP_INFO_TYPE_NORMAL

    def onInitStartPrepareTime(self, *args):
        self.initStartPrepareTime()

    def onIsEnablePrepare(self, *args):
        return GfxValue(utils.isGroupPrepareEnabled())

    def onGetMemberUIScale(self, *args):
        return GfxValue(self.memberUIScale)

    def onSetMemberUIScale(self, *args):
        self.memberUIScale = args[3][0].GetNumber()

    def initStartPrepareTime(self):
        if self.startPrepareTime:
            time = SCD.data.get('groupPrepareInterval', 30)
            leftTime = int(time - (BigWorld.player().getServerTime() - self.startPrepareTime))
            self.groupInfoMed.Invoke('startPrepare', GfxValue(leftTime))

    def refreshGroupInfo(self):
        if not self._checkValid():
            return
        if self.groupInfoMed:
            data = self.initGroupInfo()
            if data != self.currentData:
                self.currentData = copy.deepcopy(data)
                self.groupInfoMed.Invoke('refresh', uiUtils.dict2GfxDict(data, True))
        self.refreshTeamInfo()

    def _resetPlayerProperty(self):
        self.oldHp = [ -1 for i in xrange(50) ]
        self.oldMhp = [ -1 for i in xrange(50) ]
        self.oldMp = [ -1 for i in xrange(50) ]
        self.oldMmp = [ -1 for i in xrange(50) ]
        self.oldLv = [ 0 for i in xrange(50) ]
        self.isReal = False
        self.memberId = [ 0 for i in xrange(50) ]

    def _isGroupPrepare(self, gbId):
        p = BigWorld.player()
        if gbId == 0:
            return False
        if not hasattr(p, 'groupPrepareInfo'):
            return False
        if not p.groupPrepareInfo:
            return False
        return p.groupPrepareInfo.get(gbId, gametypes.GROUP_PREPARE_TYPE_DEFAULT) == gametypes.GROUP_PREPARE_TYPE_CONFIRM

    def onGetPrepareInfo(self, *args):
        return uiUtils.array2GfxAarry(self._getPrepareInfo())

    def onConfirmPrepare(self, *args):
        p = BigWorld.player()
        p.cell.askForGroupPrepare()

    def startPrepare(self):
        p = BigWorld.player()
        self.startPrepareTime = p.getServerTime()
        time = SCD.data.get('groupPrepareInterval', 30)
        p.groupPrepareInfo = {p.headerGbId: gametypes.GROUP_PREPARE_TYPE_CONFIRM}
        self.setPrePareInfo()
        if self.groupInfoMed:
            self.groupInfoMed.Invoke('startPrepare', GfxValue(time))

    def showPrepareAskMsg(self):
        time = SCD.data.get('groupPrepareInterval', 30)
        msg = GMD.data.get(GMDD.data.PREPARE_CONFIRM_MSG, {}).get('text', gameStrings.TEXT_GROUPPROXY_190)
        buttons = [MBButton(gameStrings.TEXT_GROUPPROXY_191, self.answerGroupPrepare), MBButton(gameStrings.TEXT_GROUPPROXY_191_1, None)]
        self.askPrepareMsg = gameglobal.rds.ui.messageBox.show(True, gameStrings.TEXT_GROUPPROXY_192, msg, buttons, repeat=time)

    def answerGroupPrepare(self):
        p = BigWorld.player()
        p.cell.answerGroupPrepare(gametypes.GROUP_PREPARE_TYPE_CONFIRM)

    def _getPrepareInfo(self):
        ret = []
        p = BigWorld.player()
        arrange = uiUtils.recoverArrange(p.arrangeDict)
        for gbId in arrange:
            ret.append(self._isGroupPrepare(gbId))

        return ret

    def setPrePareInfo(self):
        if self.groupInfoMed:
            self.groupInfoMed.Invoke('setConfirmPrepare', uiUtils.array2GfxAarry(self._getPrepareInfo()))

    def clearPrepareInfo(self):
        p = BigWorld.player()
        self.startPrepareTime = None
        if hasattr(p, 'groupPrepareInfo'):
            p.groupPrepareInfo = {}
        if self.groupInfoMed:
            self.groupInfoMed.Invoke('clearPrepareInfo')
        if self.askPrepareMsg:
            gameglobal.rds.ui.messageBox.dismiss(self.askPrepareMsg)
            self.askPrepareMsg = None

    def onClearPrepareInfo(self, *args):
        self.clearPrepareInfo()

    def getMaxTeamCount(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if fbNo > const.FB_NO_BATTLE_FIELD_START and fbNo < const.FB_NO_ARENA_START:
            maxGroupNum = BFD.data.get(fbNo, {}).get('maxGroupNum', 0)
            if maxGroupNum:
                return maxGroupNum
        return 10

    def initGroupInfo(self):
        if not self._checkValid():
            return
        else:
            p = BigWorld.player()
            data = {}
            if self.groupInfoType == uiConst.GROUP_INFO_TYPE_NORMAL:
                assignQuality = const.GROUP_ASSIGN_QUALITY[p.groupAssignQuality]
                isHeader = p.members.get(p.gbId, {}).get('isHeader', False)
                isAssistant = p.members.get(p.gbId, {}).get('isAssistant', False)
                data = {'name': p.detailInfo['teamName'],
                 'quality': assignQuality,
                 'type': p.groupAssignWay,
                 'isHeader': isHeader,
                 'isAssistant': isAssistant}
                info = []
                for i in xrange(self.getMaxTeamCount()):
                    teamData = []
                    teamList = self.getTeamListById(i)
                    for item in teamList:
                        if item != 0 and p.members.has_key(item):
                            teamData.append(p.members[item])
                            teamData[-1]['gbId'] = item
                        else:
                            teamData.append(None)

                    info.append(teamData)

                data['info'] = info
                data['groupInfoType'] = self.groupInfoType
            elif self.groupInfoType == uiConst.GROUP_INFO_TYPE_BATTLEFIELD:
                isHeader = p.gbId == p.bfHeaderGbId
                data = {'groupInfoType': self.groupInfoType,
                 'name': gameStrings.TEXT_GROUPPROXY_260,
                 'isHeader': isHeader,
                 'isAssistant': False}
                members = self._getMembersInfo()
                if members:
                    info = []
                    for i in xrange(self.getMaxTeamCount()):
                        teamData = []
                        teamList = self.getTeamListById(i)
                        for item in teamList:
                            if item != 0 and members.has_key(item):
                                memberData = members[item]
                                memberData['isHeader'] = item == p.bfHeaderGbId
                                teamData.append(memberData)
                                teamData[-1]['gbId'] = item
                            else:
                                teamData.append(None)

                        info.append(teamData)

                    data['info'] = info
            elif self.groupInfoType == uiConst.GROUP_INFO_TYPE_LUE_YING_GU:
                isHeader = p.gbId == p.pvpHeader
                data = {'groupInfoType': self.groupInfoType,
                 'name': gameStrings.TEXT_GROUPPROXY_282,
                 'isHeader': isHeader,
                 'isAssistant': False}
                members = self._getMembersInfo()
                if members:
                    info = []
                    for i in xrange(self.getMaxTeamCount()):
                        teamData = []
                        teamList = self.getTeamListById(i)
                        for item in teamList:
                            if item != 0:
                                if members.has_key(item):
                                    memberData = members[item]
                                    memberData['isHeader'] = item == p.pvpHeader
                                    memberData['isOn'] = True
                                    teamData.append(memberData)
                                    teamData[-1]['gbId'] = item
                            else:
                                teamData.append(None)

                        info.append(teamData)

                    data['info'] = info
            return data

    def _getMembersInfo(self):
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_NORMAL:
            return BigWorld.player().members
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_BATTLEFIELD:
            return BigWorld.player().battleFieldTeam
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_LUE_YING_GU:
            return BigWorld.player().pvpMemInfo

    def _getArrange(self):
        p = BigWorld.player()
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_NORMAL:
            return uiUtils.recoverArrange(p.arrangeDict)
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_BATTLEFIELD and hasattr(p, 'bfArrange'):
            return p.bfArrange
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_LUE_YING_GU and hasattr(p, 'pvpArrange'):
            return p.pvpArrange

    def getTeamListById(self, teamId):
        arrange = self._getArrange()
        teamList = []
        if arrange:
            for i in xrange(5):
                teamList.append(arrange[i + 5 * teamId])

        return teamList

    def onClickMemItem(self, *arg):
        try:
            teamId = int(arg[3][0].GetNumber())
            index = int(arg[3][1].GetNumber())
            entId = self.getEntIdbyIndex(teamId * 5 + index)
            ent = BigWorld.entities.get(entId)
            if ent:
                uiUtils.onTargetSelect(ent)
        except:
            pass

    def onMarkScene(self, *arg):
        mark = arg[3][0].GetString()
        p = BigWorld.player()
        if mark[1:] == 'stop':
            p.cell.clearMarkMap()
        else:
            self.markMapIndex = int(mark[1:])
            p.ap.startMarkMap(True)

    def onClickTeamIndex(self, *arg):
        index = int(arg[3][0].GetNumber())
        if index in self.teamSet:
            self.removeTeamWidget(index)
        else:
            self.addTeamWidget(index)

    def onGetGroupTeamInfo(self, *arg):
        data = []
        self.getShowTeamSet()
        for i in self.teamSet:
            info = self.getTeamInfoById(i)
            data.append(info)

        return uiUtils.array2GfxAarry(data, True)

    def getShowTeamSet(self):
        self.teamSet.clear()
        arrange = self._getArrange()
        if arrange:
            for index in xrange(50):
                if arrange[index]:
                    self.teamSet.add(index / 5)

    def addTeamWidget(self, teamId):
        data = self.getTeamInfoById(teamId)
        self.groupMemMed.Invoke('addTeam', uiUtils.array2GfxAarry(data, True))
        self.teamSet.add(teamId)

    def removeTeamWidget(self, teamId):
        self.teamSet.remove(teamId)
        self.groupMemMed.Invoke('removeTeam', GfxValue(teamId))

    def onShowTeamWidget(self, *arg):
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD) and p.inLiveOfGuildTournament > 0:
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_GROUPMEMBER)

    def onCloseTeamWidget(self, *arg):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GROUPMEMBER)
        self.groupMemMed = None
        self.currentMemData = {}
        if self.castTestHandler:
            BigWorld.cancelCallback(self.castTestHandler)
        self.castTestHandler = None

    def onGetGroupInfo(self, *arg):
        data = self.initGroupInfo()
        if not data:
            return
        if self.groupMemMed:
            data['showTeam'] = True
        else:
            data['showTeam'] = False
        self.refreshTeamInfo()
        return uiUtils.dict2GfxDict(data, True)

    def onConfirmGroup(self, *arg):
        pass

    def onGetMark(self, *arg):
        index = int(arg[3][0].GetNumber())
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_NORMAL:
            p = BigWorld.player()
            entId = self.getEntIdbyIndex(index)
            if entId != None:
                mark = p.groupMark.get(entId)
                if mark != None:
                    return GfxValue(p.groupMark[entId])
                else:
                    return GfxValue(0)
        else:
            return GfxValue(0)

    def getEntIdbyIndex(self, index):
        arrange = self._getArrange()
        members = self._getMembersInfo()
        if arrange and members:
            gbId = arrange[index]
            entId = members.get(gbId, {}).get('id')
            return entId
        else:
            return None

    def onPromptAss(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        arrange = self._getArrange()
        members = self._getMembersInfo()
        gbId = arrange[index]
        roleName = members.get(gbId, {}).get('roleName')
        isAssistant = members.get(gbId, {}).get('isAssistant')
        if roleName and not isAssistant:
            p.cell.accreditAssistant(roleName)
        elif roleName and isAssistant:
            p.cell.relieveAssistant(roleName)

    def onRemoveTeamate(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        gbId = self._getArrange()[index]
        roleName = self._getMembersInfo().get(gbId, {}).get('roleName')
        if roleName and self.groupInfoType == uiConst.GROUP_INFO_TYPE_NORMAL:
            p.deleteMemFromTeam(gbId, roleName)

    def onShowGroupCreateInfo(self, *arg):
        gameglobal.rds.ui.createTeamV2.show()

    def onCloseGroupInfo(self, *arg):
        self.groupInfoMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GROUPINFO_PANEL)
        self.isShow = False

    def onLeaveGroup(self, *arg):
        p = BigWorld.player()
        p.quitGroup()

    def clearOnLeave(self):
        self.closeGroupInfoPanel()
        self.closeAllWidget()

    def closeAllWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GROUPMEMBER)
        self.groupMemMed = None
        self.currentMemData = {}
        if self.castTestHandler:
            BigWorld.cancelCallback(self.castTestHandler)
        self.castTestHandler = None

    def onChangeLeader(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        gbId = self._getArrange()[index]
        if self.groupInfoType in (uiConst.GROUP_INFO_TYPE_NORMAL, uiConst.GROUP_INFO_TYPE_BATTLEFIELD):
            if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
                p.cell.abdicatedBattleFieldGroup(gbId)
            else:
                p.cell.abdicatedGroup(gbId)

    def onChangeArrange(self, *arg):
        p = BigWorld.player()
        srcIndex = int(arg[3][0].GetNumber())
        destIndex = int(arg[3][1].GetNumber())
        srcGbId = self._getArrange()[srcIndex]
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_NORMAL:
            p.cell.arrangeGroup(srcGbId, destIndex)
        elif self.groupInfoType == uiConst.GROUP_INFO_TYPE_BATTLEFIELD:
            p.cell.arrangeBattleFieldGroup(srcGbId, destIndex)

    def onChangeAssignType(self, *arg):
        assignType = int(arg[3][0].GetNumber())
        qualityType = int(arg[3][1].GetNumber())
        BigWorld.player().cell.setGroupAssign(assignType, const.GROUP_ASSIGN_QUALITY[qualityType])

    def onSetSign(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        flag = int(arg[3][1].GetNumber())
        entId = self.getEntIdbyIndex(index)
        p.cell.markEntity(entId, flag)

    def onCancelSign(self, *arg):
        index = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        entId = self.getEntIdbyIndex(index)
        p.cell.markEntity(entId, 0)

    def getTeamInfoById(self, teamId):
        teamData = []
        teamList = self.getTeamListById(teamId)
        index = teamId * 5 + 0
        members = self._getMembersInfo()
        for item in teamList:
            if members.get(item):
                memberInfo = self.getTeamateInfoByGbId(index, item)
                self.currentMemData[index] = memberInfo
                teamData.append(memberInfo)
            else:
                teamData.append(None)
            index = index + 1

        return [teamId, teamData]

    def getTeamateInfoByGbId(self, index, gbId):
        p = BigWorld.player()
        members = self._getMembersInfo()
        playerInfo = copy.deepcopy(members[gbId])
        playerInfo['hp'], playerInfo['mhp'], playerInfo['mp'], playerInfo['mmp'] = self.getPyPlayerInfo(index, playerInfo['id'])
        if p.targetLocked:
            playerInfo['isSelect'] = p.targetLocked.id == playerInfo['id']
        else:
            playerInfo['isSelect'] = False
        ent = BigWorld.entities.get(playerInfo['id'])
        playerInfo['overDis'] = False
        if ent:
            if uiUtils.canCastSkill(ent):
                playerInfo['overDis'] = False
            else:
                playerInfo['overDis'] = True
        else:
            playerInfo['overDis'] = True
        self.memberId[index] = playerInfo['id']
        playerInfo['gbId'] = str(gbId)
        stateData = p.getTeamStateDataByEntId(playerInfo['id'])
        playerInfo['stateData'] = stateData
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_LUE_YING_GU:
            playerInfo['isHeader'] = gbId == p.pvpHeader
        elif self.groupInfoType == uiConst.GROUP_INFO_TYPE_BATTLEFIELD:
            playerInfo['isHeader'] = gbId == p.bfHeaderGbId
            if playerInfo.has_key('fromHostName') and playerInfo['fromHostName'] != '':
                playerInfo['roleName'] = playerInfo.get('roleName', '') + '-' + playerInfo['fromHostName']
        return playerInfo

    def refreshTeamInfo(self):
        if self.groupMemMed:
            data = {}
            arrange = self._getArrange()
            members = self._getMembersInfo()
            index = 0
            for gbId in arrange:
                if gbId == 0 or not members.get(gbId):
                    if self.currentMemData.get(index):
                        data[index] = None
                        self.currentMemData[index] = None
                    index = index + 1
                else:
                    entId = members.get(gbId, {}).get('id', 0)
                    header = members.get(gbId, {}).get('isHeader', 0)
                    assistant = members.get(gbId, {}).get('isAssistant', 0)
                    on = members.get(gbId, {}).get('isOn', 0)
                    oldData = self.currentMemData.get(index, {})
                    if oldData:
                        oldPos = oldData.get('gbId', 0)
                        oldHeader = oldData.get('isHeader', 0)
                        oldAssistant = oldData.get('isAssistant', 0)
                        oldOn = oldData.get('isOn', 0)
                        if (entId == 0 or BigWorld.entities.get(entId)) and str(gbId) == oldPos and oldHeader == header and oldAssistant == assistant and oldOn == on:
                            index = index + 1
                            continue
                    playerInfo = self.getTeamateInfoByGbId(index, gbId)
                    if playerInfo != self.currentMemData.get(index):
                        data[index] = playerInfo
                        self.currentMemData[index] = playerInfo
                    index = index + 1

            if data:
                self.groupMemMed.Invoke('refreshTeam', uiUtils.dict2GfxDict(data, True))

    def refreshCanCastSkill(self):
        if not self.groupMemMed:
            return
        ret = []
        for i in self.teamSet:
            for j in xrange(5):
                index = i * 5 + j
                entId = self.memberId[index]
                ent = BigWorld.entities.get(entId)
                canCastSkill = False
                if ent:
                    canCastSkill = uiUtils.canCastSkill(ent)
                if (index, canCastSkill) not in self.canCastSkillList:
                    ret.append((index, canCastSkill))

        if self.canCastSkillList != ret:
            self.canCastSkillList = ret
            self.groupMemMed.Invoke('refreshCanCastSkill', uiUtils.array2GfxAarry(ret))
        self.castTestHandler = BigWorld.callback(0.3, self.refreshCanCastSkill)

    def setSelect(self, index):
        if self.groupMemMed:
            self.groupMemMed.Invoke('setSelect', GfxValue(index))

    def unSelect(self):
        if self.groupMemMed:
            self.groupMemMed.Invoke('unSelect')

    def setGroupHp(self, id, hp, mhp):
        if not self.groupMemMed:
            return
        else:
            index = self.getTeamIdByEntId(id)
            if index is None:
                return
            if self.groupMemMed:
                self.groupMemMed.Invoke('setHp', (GfxValue(index), GfxValue(hp), GfxValue(mhp)))
            return

    def setGroupMp(self, id, mp, mmp):
        if not self.groupMemMed:
            return
        else:
            index = self.getTeamIdByEntId(id)
            if index is None:
                return
            if self.groupMemMed:
                self.groupMemMed.Invoke('setMp', (GfxValue(index), GfxValue(mp), GfxValue(mmp)))
            return

    def getTeamIdByEntId(self, entId):
        index = 0
        arrange = self._getArrange()
        members = self._getMembersInfo()
        if arrange and members:
            for item in arrange:
                info = members.get(item)
                if info == None:
                    index = index + 1
                    continue
                mId = info.get('id')
                if mId == entId:
                    return index
                index = index + 1

    def showGroupInfoPanel(self):
        self.isShow = True
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_ARENA):
            p.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
            return
        if p.inFubenType(const.FB_TYPE_SHENGSICHANG):
            p.showGameMsg(GMDD.data.SSC_FORBIDDEN_WITH_TEAM, ())
            return
        if p.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            p.showGameMsg(GMDD.data.TEAM_SSC_FORBIDDEN_WITH_TEAM, ())
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GROUPINFO_PANEL)

    def closeGroupInfoPanel(self):
        self.isShow = False
        self.groupInfoMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GROUPINFO_PANEL)

    def showGroupTeam(self):
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD) and p.inLiveOfGuildTournament > 0:
            return
        if p.inFubenTypes(const.FB_TYPE_ARENA):
            p.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
            return
        if p.inFubenType(const.FB_TYPE_SHENGSICHANG):
            p.showGameMsg(GMDD.data.SSC_FORBIDDEN_WITH_TEAM, ())
            return
        if p.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            p.showGameMsg(GMDD.data.TEAM_SSC_FORBIDDEN_WITH_TEAM, ())
            return
        if p.isInPUBG():
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GROUPMEMBER)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.groupInfoMed = None
        self.groupMemMed = None
        self.currentMemData = {}
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GROUPINFO_PANEL)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GROUPMEMBER)

    def refreshAssignMode(self):
        p = BigWorld.player()
        self.assignRule = p.groupAssignWay
        self.assignQuality = const.GROUP_ASSIGN_QUALITY[p.groupAssignQuality]
        ret = [self.assignRule, self.assignQuality]
        if self.groupInfoMed:
            self.groupInfoMed.Invoke('refreshAssignMode', uiUtils.array2GfxAarry(ret))

    def onGetLocationTip(self, *arg):
        try:
            gbId = int(arg[3][0].GetString())
            ret = uiUtils.getLocationByGbId(gbId)
        except:
            ret = ''

        return GfxValue(gbk2unicode(ret))

    def onGoBackToHallClick(self, *arg):
        gameglobal.rds.ui.team.show()

    def _checkValid(self):
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_BATTLEFIELD:
            return BigWorld.player().battleFieldTeam
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_NORMAL:
            return BigWorld.player().isInGroup() and BigWorld.player().members
        if self.groupInfoType == uiConst.GROUP_INFO_TYPE_LUE_YING_GU:
            return BigWorld.player().pvpMemInfo

    def setStateIcon(self, entityId, newData):
        index = self.getTeamIdByEntId(entityId)
        if index is None:
            return
        else:
            if self.groupMemMed:
                self.groupMemMed.Invoke('setState', (GfxValue(index), uiUtils.array2GfxAarry(newData)))
            return

    def onIsTeamLeader(self, *arg):
        p = BigWorld.player()
        if p.isInTeamOrGroup() and p.groupHeader == p.id:
            return GfxValue(True)
        return GfxValue(False)

    def changeArrangeData(self, oldArrange, newArrange):
        for key in oldArrange.keys():
            oldIndex = oldArrange.get(key)
            newIndex = newArrange.get(key)
            if oldIndex != None and newIndex != None and oldIndex != newIndex:
                self.oldMhp[newIndex], self.oldMhp[oldIndex] = self.oldMhp[oldIndex], self.oldMhp[newIndex]
                self.oldHp[newIndex], self.oldHp[oldIndex] = self.oldHp[oldIndex], self.oldHp[newIndex]
                self.memberId[newIndex], self.memberId[oldIndex] = self.memberId[oldIndex], self.memberId[newIndex]

    def changeBFArrangeData(self, oldArrange, newArrange):
        for gbId in oldArrange:
            if not gbId:
                continue
            try:
                oldIndex = oldArrange.index(gbId)
            except:
                oldIndex = None

            try:
                newIndex = newArrange.index(gbId)
            except:
                newIndex = None

            if oldIndex != None and newIndex != None and oldIndex != newIndex:
                self.oldMhp[newIndex], self.oldMhp[oldIndex] = self.oldMhp[oldIndex], self.oldMhp[newIndex]
                self.oldHp[newIndex], self.oldHp[oldIndex] = self.oldHp[oldIndex], self.oldHp[newIndex]
                self.memberId[newIndex], self.memberId[oldIndex] = self.memberId[oldIndex], self.memberId[newIndex]

    def onGetEnableYecha(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableNewSchoolYeCha', False))

    def onHandleInvitePlayer(self, *args):
        gameglobal.rds.ui.invitePlayer.show()

    def onIsCloseTeamGoal(self, *args):
        return GfxValue(TeamGoalMenuHelper.isNeedCloseTeamGoal())

    def onGetEnableTianzhao(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableNewSchoolTianZhao', False))
