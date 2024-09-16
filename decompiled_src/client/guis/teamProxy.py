#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/teamProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import formula
import gamelog
import ui
import uiUtils
import utils
import gametypes
import copy
from uiProxy import UIProxy
from ui import gbk2unicode
from ui import unicode2gbk
from callbackHelper import Functor
from guis import groupDetailFactory
from guis import menuManager
from helpers import taboo
from gamestrings import gameStrings
from data import school_data as SD
from data import chunk_mapping_data as CMD
from data import game_msg_data as GMD
from data import sys_config_data as SCD
from data import group_label_data as GLD
from cdata import group_fb_menu_data as GFMD
from data import fb_data as FD
from cdata import font_config_data as FCD
from cdata import game_msg_def_data as GMDD
import clientUtils

class TeamProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TeamProxy, self).__init__(uiAdapter)
        self.modelMap = {'isInTeam': self.onIsInTeam,
         'isChangeTeamInfo': self.onIsChangeTeamInfo,
         'getEnableGroupDetailForcely': self.onGetEnableGroupDetailForcely,
         'isQuickTeamInfo': self.onIsQuickTeamInfo,
         'getTeamList': self.onGetTeamList,
         'getMemberList': self.onGetMemberList,
         'isLeader': self.onIsLeader,
         'clickCloseBtn': self.onClickCloseBtn,
         'clickCreateTeamBtn': self.onClickCreateTeamBtn,
         'clickApplyJoinBtn': self.onClickApplyJoinBtn,
         'clickDeleteMember': self.onClickDeleteMember,
         'clickChangeLeaderBtn': self.onClickChangeLeader,
         'clickLeaveBtn': self.onClickLeave,
         'clickRefreshBtn': self.onClickRefresh,
         'clickSearchBtn': self.onClickSearch,
         'getApplyMember': self.onGetApplyer,
         'acceptGroup': self.onAcceptApplyGroup,
         'rejectGroup': self.onRejectApplyGroup,
         'clearApplyer': self.onClearApplyer,
         'applyTimeOut': self.onApplyTimeOut,
         'getTeamName': self.onGetTeamName,
         'getAssignMode': self.onGetAssignMode,
         'setAssignMode': self.onSetAssignMode,
         'changeTab': self.onChangeTab,
         'changeToGroup': self.onChangeToGroup,
         'setFilter': self.onSetFilter,
         'clickApplyOk': self.onClickApplyOk,
         'clickApplyCancel': self.onClickApplyCancel,
         'clickApplyClose': self.onClickApplyClose,
         'getApplyPushInfo': self.onGetApplyPushInfo,
         'clickApplyWithNonGroupOk': self.onClickApplyWithNonGroupOk,
         'clickApplyWithNonGroupCancel': self.onClickApplyWithNonGroupCancel,
         'clickApplyWithNonGroupClose': self.onClickApplyWithNonGroupClose,
         'getApplyPushInfoWithNonGroup': self.onGetApplyPushInfoWithNonGroup,
         'applyWithNonGroupTimeout': self.onApplyWithNonGroupTimeout,
         'getDropDownMenuInfo': self.onGetDropDownMenuInfo,
         'getCreateTeamInfo': self.onGetCreateTeamInfo,
         'goBackToHallClick': self.onGoBackToTeamHall,
         'quickCreateClick': self.onQuickCreateClick,
         'isPublish': self.onIsPublish,
         'getLeftListMenuInfo': self.onGetLeftListMenuInfo,
         'getTeamDetailInfo': self.onGetTeamDetailInfo,
         'getMenuId': self.onGetMenuId,
         'setFilterKey': self.onSetFilterKey,
         'clickApplyGroupMatch': self.onClickApplyGroupMatch,
         'setCreateTeamGoalType': self.onSetCreateTeamGoalType,
         'setTeamDetailGoalType': self.onSetTeamDetailGoalType,
         'getDropMenuIndex': self.onGetDropMenuIndex,
         'inviteCC': self.onInviteCC,
         'isShowCC': self.isShowCC,
         'groupMatchBtnVisiable': self.onGroupMatchBtnVisiable,
         'shareTeamInfo': self.onShareTeamInfo,
         'isShareEnable': self.isShareEnable,
         'getEnableYecha': self.onGetEnableYecha,
         'getLabelInfo': self.onGetLabelInfo,
         'getLvLimit': self.onGetLvLimit,
         'refreshAvlActivity': self.onRefreshAvlActivity,
         'setAutoShare': self.onSetAutoShare,
         'getAutoShareTips': self.onGetAutoShareTips,
         'setTeamType': self.onSetTeamType,
         'getOpenTypeNeed': self.onGetOpenTypeNeed,
         'getAutoLabel': self.onGetAutoLabel,
         'hasGoal': self.onHasGoal,
         'getLvAllowShare': self.onGetLvAllowShare,
         'getGroupDetailTips': self.onGetGroupDetailTips,
         'isMeetLv': self.onIsMeetLv,
         'getTipsString': self.onGetTipsString}
        self.mediator = None
        self.groupDetailFactory = groupDetailFactory.getInstance()
        self.actTypeData = {}
        self.actAvlData = {}
        self.reset()
        self.teamApplyMed = None
        self.teamApplyWithNonGroupMed = None
        self.isAutoShare = True
        self.labelId = 0
        self.openGoalType = None
        self.isOpenType = False
        self.autoLabelIndex = None
        self.isGoalType = False
        self.isForceSelectedDetailInfo = False
        self.hotTagList = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_TEAM, self.close)
        uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_APPLY_TEAM, {'click': self.showApply,
         'refresh': self.refreshApply})
        uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP, {'click': self.showApplyWithNonGroup,
         'refresh': self.refreshApplyWithNonGroup,
         'timeout': self.applyWithNonGroupTimeOut})

    def isShowCC(self, *arg):
        isCCVersion = gameglobal.rds.configData.get('isCCVersion', False)
        return GfxValue(isCCVersion)

    def isShareEnable(self, *args):
        ret = []
        isShareEnable = gameglobal.rds.configData.get('enableTeamInfoShare', False)
        ret.append(isShareEnable)
        ret.append(not BigWorld.player().isInFullTeam())
        ret.append(self.getShareBtnTipsInfo())
        return uiUtils.array2GfxAarry(ret, True)

    def onIsMeetLv(self, *args):
        return GfxValue(BigWorld.player().lv >= SCD.data.get('team2GroupLv', 35))

    def onGetTipsString(self, *args):
        p = BigWorld.player()
        if p.isTeamLeader():
            return GfxValue(gbk2unicode(gameStrings.TEAM2GROUP_DISABLE_TIPS % SCD.data.get('team2GroupLv', 35)))
        else:
            return GfxValue(gbk2unicode(gameStrings.TEAM2GROUP_MEMBER_TIPS))

    def onClickApplyOk(self, *arg):
        srcId = long(arg[3][1].GetString())
        srcName = arg[3][2].GetString()
        p = BigWorld.player()
        if self.checkCanApply():
            p.acceptApplyGroup(srcName, srcId)
            self.closeApplyWidget()

    def checkCanApply(self):
        p = BigWorld.player()
        if p.ntStatus == gametypes.NT_STATUS_NPC_TRIGGER_AND_NO_OPEN_BOX:
            if p.members and len(p.members) >= 2:
                p.showGameMsg(GMDD.data.NEW_PLAYER_TREASURE_BOX_TEAM_FULL, ())
                return False
        return True

    def onClickApplyCancel(self, *arg):
        p = BigWorld.player()
        self.applyDataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_APPLY_TEAM)
        for item in self.applyDataList:
            p.rejectApplyGroup(item['data'][2], long(item['data'][1]))

        self.closeApplyWidget()

    def onClickApplyClose(self, *arg):
        self.closeApplyWidget()

    def closeApplyWidget(self):
        self.teamApplyMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TEAM_APPLY)

    def showApply(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TEAM_APPLY)

    def onGetApplyPushInfo(self, *arg):
        self.applyDataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_APPLY_TEAM)
        data = [len(self.applyDataList), []]
        for item in self.applyDataList:
            item['data'][0] = self._getRemainTime(item['startTime'])
            data[1].append(item['data'])

        ar = uiUtils.array2GfxAarry(data)
        return ar

    def _getRemainTime(self, val):
        return int(30 - (BigWorld.player().getServerTime() - val))

    def refreshApply(self):
        dataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_APPLY_TEAM)
        if self.teamApplyMed != None:
            data = [len(dataList), []]
            for item in dataList:
                item['data'][0] = self._getRemainTime(item['startTime'])
                data[1].append(item['data'])

            ar = uiUtils.array2GfxAarry(data)
            self.teamApplyMed.Invoke('refresh', ar)

    def onApplyWithNonGroupTimeout(self, *arg):
        srcGbId = long(arg[3][0].GetString())
        srcName = unicode2gbk(arg[3][1].GetString())
        self._applyWithNonGroupTimeout(srcGbId, srcName)

    def _applyWithNonGroupTimeout(self, srcGbId, srcName):
        BigWorld.player().cell.rejectApplyByGroupWithTgtNonGroup(srcName, srcGbId)
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP, gameglobal.rds.ui.team._getApplyDataWithNonGroup(srcGbId))

    def onClickApplyWithNonGroupOk(self, *arg):
        p = BigWorld.player()
        dataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP)
        needRemoveGbIds = []
        for item in dataList:
            srcGbId = long(item['data'][1])
            needRemoveGbIds.append(srcGbId)
            p.cell.popSrcGbIdWithTgtNonGroup(srcGbId)
            p.inviteGroup(item['data'][2])

        for gbId in needRemoveGbIds:
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP, gameglobal.rds.ui.team._getApplyDataWithNonGroup(gbId))

        self.closeApplyWithNonWidget()

    def onClickApplyWithNonGroupCancel(self, *arg):
        p = BigWorld.player()
        dataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP)
        needRemoveGbIds = []
        for item in dataList:
            gbId = long(item['data'][1])
            needRemoveGbIds.append(gbId)
            p.cell.rejectApplyByGroupWithTgtNonGroup(item['data'][2], gbId)

        for gbId in needRemoveGbIds:
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP, gameglobal.rds.ui.team._getApplyDataWithNonGroup(gbId))

        self.closeApplyWithNonWidget()

    def onClickApplyWithNonGroupClose(self, *arg):
        self.closeApplyWithNonWidget()

    def closeApplyWithNonWidget(self):
        self.teamApplyWithNonGroupMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TEAM_APPLY_WITH_NON_GROUP)

    def showApplyWithNonGroup(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TEAM_APPLY_WITH_NON_GROUP)

    def onGetApplyPushInfoWithNonGroup(self, *arg):
        self.applyDataListWithNonGroup = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP)
        data = [len(self.applyDataListWithNonGroup), []]
        for item in self.applyDataListWithNonGroup:
            item['data'][0] = self._getRemainTime(item['startTime'])
            data[1].append(item['data'])

        ar = uiUtils.array2GfxAarry(data, True)
        return ar

    def refreshApplyWithNonGroup(self):
        dataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP)
        if self.teamApplyWithNonGroupMed != None:
            data = [len(dataList), []]
            for item in dataList:
                item['data'][0] = self._getRemainTime(item['startTime'])
                data[1].append(item['data'])

            ar = uiUtils.array2GfxAarry(data, True)
            self.teamApplyWithNonGroupMed.Invoke('refresh', ar)

    def applyWithNonGroupTimeOut(self, item):
        srcGbId = long(item['data'][1])
        self._applyWithNonGroupTimeout(srcGbId, item['data'][2])
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP, self._getApplyDataWithNonGroup(srcGbId))

    def reset(self):
        self.teamIndex = -1
        self.memIndex = 0
        self.isFilter = False
        self.teamName = ''
        self.teamTarget = 0
        self.ctCurGoal = const.GROUP_GOAL_FB
        self.tdCurGoal = const.GROUP_HOT_TAGS
        self.isSearchResult = False
        self.groupType = gametypes.GROUP_TYPE_TEAM_GROUP
        self.isShow = False
        self.assignRule = const.GROUP_ASSIGN_FREE
        self.assignQuality = const.GROUP_ASSIGN_QUALITY[2]

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TEAM:
            self.mediator = mediator
        elif widgetId == uiConst.WIDGET_TEAM_APPLY:
            self.teamApplyMed = mediator
        elif widgetId == uiConst.WIDGET_TEAM_APPLY_WITH_NON_GROUP:
            self.teamApplyWithNonGroupMed = mediator

    def onGetAutoLabel(self, *args):
        index = self.autoLabelIndex if self.autoLabelIndex and not BigWorld.player().isInTeamOrGroup() else -1
        name = GLD.data.get(index, {}).get('name', '')
        return GfxValue(gbk2unicode(name))

    def onHasGoal(self, *args):
        hasGoal = self.hasGoal()
        return GfxValue(hasGoal)

    def getShareTeamInfoMsg(self, groupNUID = None):
        return self.groupDetailFactory.getShareTeamInfoMsg(groupNUID)

    def onShareTeamInfo(self, *args):
        p = BigWorld.player()
        if not uiUtils.checkShareTeamLvLimit():
            teamInfoUseLv = SCD.data.get('teamInfoUseLv', 20)
            p.showGameMsg(GMDD.data.TEAM_INFO_LV_LIMIT, (teamInfoUseLv,))
            return
        if not p.isInTeamOrGroup():
            return
        if p.headerGbId != p.gbId:
            BigWorld.player().showGameMsg(GMDD.data.SHARE_TEAM_ONLY_LEADER, ())
            return
        if self.hasGoal():
            msg = self.getShareTeamInfoMsg()
            p.cell.chatToGroupInfo(msg)
            gameglobal.rds.ui.teamComm.setHornStartCoolDown()
        else:
            gameglobal.rds.ui.createTeamV2.show()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.team.teamDetailMc = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TEAM)
        self.autoLabelIndex = None

    def onIsInTeam(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.groupNUID > 0)

    def onGetTeamList(self, *arg):
        groupType = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        p._getTeamsInfo()
        ret = self.movie.CreateArray()
        self.groupNUIDList = []
        index = 0
        for value in p.teamsInfo:
            if groupType != value[8]:
                continue
            self.groupNUIDList.append(value[5])
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(gbk2unicode(value[0])))
            ar.SetElement(1, GfxValue(value[1]))
            ar.SetElement(2, GfxValue(value[3]))
            ar.SetElement(3, GfxValue(value[4]))
            ar.SetElement(4, GfxValue(value[2]))
            if groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
                ar.SetElement(5, GfxValue(const.TEAM_MAX_NUMBER))
            else:
                ar.SetElement(5, GfxValue(const.GROUP_MAX_NUMBER))
            ret.SetElement(index, ar)
            index += 1

        return ret

    def _getMapNameByGbId(self, gbId):
        p = BigWorld.player()
        defalultName = '???'
        chunkName = ''
        spaceNo = 0
        if p.gbId == gbId:
            spaceNo = p.spaceNo
            chunkName = BigWorld.ChunkInfoAt(p.position)
        else:
            if not hasattr(p, 'membersPos'):
                return defalultName
            if not p.membersPos.has_key(gbId):
                return defalultName
            spaceNo = p.membersPos[gbId][0]
            chunkName = p.membersPos[gbId][3]
        mapName = formula.whatLocationName(spaceNo, chunkName, includeMLInfo=True)
        return mapName

    def onGetMemberList(self, *arg):
        p = BigWorld.player()
        ret = self.movie.CreateArray()
        index = 0
        self.memGbId = []
        self.memName = []
        for key, value in p._getSortedMembers():
            if not p._checkValidSchool(value['school']):
                continue
            self.memGbId.append(key)
            self.memName.append(value['roleName'])
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(gbk2unicode(value['roleName'])))
            ar.SetElement(1, GfxValue(value['level']))
            ar.SetElement(2, GfxValue(gbk2unicode(SD.data[value['school']]['name'])))
            ar.SetElement(3, GfxValue(p.headerGbId == key))
            ar.SetElement(4, GfxValue(value['isOn']))
            ar.SetElement(5, GfxValue(gbk2unicode(self._getMapNameByGbId(key))))
            ret.SetElement(index, ar)
            index += 1

        return ret

    def refreshTeamDetails(self):
        if self.mediator != None:
            self.mediator.Invoke('refreshPanel')

    def refreshSocialTeamsInfo(self):
        gamelog.debug('@hjx social#refreshSocialTeamsInfo:', self.isShow)
        if not self.isShow:
            return
        else:
            if not self.isSearchResult:
                p = BigWorld.player()
                self.groupDetailFactory.resetDetailByType(p.teamGoal, p.teamsInfo)
            if self.mediator != None:
                self.mediator.Invoke('refreshDetail')
            else:
                if not self.isShow:
                    gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TEAM)
                self.isShow = True
            return

    def refreshBtn(self):
        if self.mediator != None:
            self.mediator.Invoke('refreshBtn')

    def onIsLeader(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.isTeamLeader())

    def show(self):
        p = BigWorld.player()
        if not p.checkMapLimitUI(gametypes.MAP_LIMIT_UI_SOCIAL):
            return
        elif p.inFubenTypes(const.FB_TYPE_ARENA):
            p.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
            return
        elif p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            p.showGameMsg(GMDD.data.BATTLE_FIELD_FORBIDDEN_WITH_TEAM, ())
            return
        else:
            if p.isInTeamOrGroup():
                self.tdCurGoal = const.GROUP_GOAL_DEFAULT
            if self.mediator is None:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TEAM)
            self.isShow = True
            self.isSearchResult = False
            return

    def changeTeamHallVisible(self):
        if self.mediator is None:
            self.show()
        else:
            self.close()

    def close(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TEAM)
        self.isShow = False
        self.autoLabelIndex = None

    def onClickCloseBtn(self, *arg):
        self.close()

    def _getDefaultName(self):
        p = BigWorld.player()
        if self.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
            return p.realRoleName + gameStrings.TEXT_TEAMPROXY_495
        else:
            return p.realRoleName + gameStrings.TEXT_CONST_165

    def onClickCreateTeamBtn(self, *arg):
        self.autoLabelIndex = None
        p = BigWorld.player()
        if p.isInTeam():
            gameglobal.rds.ui.memberDetailsV2.changeUIVisible()
        elif p.isInGroup():
            if gameglobal.rds.ui.group.groupInfoMed:
                gameglobal.rds.ui.group.closeGroupInfoPanel()
            else:
                gameglobal.rds.ui.group.showGroupInfoPanel()
        else:
            self.onQuickCreateClick()

    def onGoBackToTeamHall(self, *arg):
        if self.mediator:
            self.close()
        else:
            self.show()

    def onClickApplyJoinBtn(self, *arg):
        headerRoleName = unicode2gbk(arg[3][0].GetString())
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_ARENA):
            p.showGameMsg(GMDD.data.ARENA_FORBIDDEN_WITH_TEAM, ())
            return
        if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            p.showGameMsg(GMDD.data.BATTLE_FIELD_FORBIDDEN_WITH_TEAM, ())
            return
        gamelog.debug('@hjx social#onClickApplyJoinBtn:', headerRoleName)
        if headerRoleName:
            p.applyGroup(headerRoleName)
        else:
            gamelog.error('@hjx onClickApplyJoinBtn error:%d' % (self.tdCurGoal,))

    def onClickDeleteMember(self, *arg):
        self.memIndex = int(arg[3][0].GetNumber())
        if self.memIndex < 0 or self.memIndex >= len(self.memGbId):
            return
        p = BigWorld.player()
        p.deleteMemFromTeam(self.memGbId[self.memIndex], self.memName[self.memIndex])

    def onClickChangeLeader(self, *arg):
        self.memIndex = int(arg[3][0].GetNumber())
        if self.memIndex < 0 or self.memIndex >= len(self.memGbId):
            return
        p = BigWorld.player()
        p.changeTeamLeader(self.memGbId[self.memIndex])

    def onClickLeave(self, *arg):
        menuManager.getInstance().leaveTeam()

    def onClickRefresh(self, *arg):
        teamName = unicode2gbk(arg[3][0].GetString())
        goalType = int(arg[3][1].GetNumber())
        gamelog.debug('@hjx social#onClickRefresh:', goalType)
        p = BigWorld.player()
        p.queryPublicTeams(teamName, goalType)

    def onClickSearch(self, *arg):
        self.teamName = unicode2gbk(arg[3][0].GetString())
        self.teamTarget = int(arg[3][1].GetNumber())
        gamelog.debug('@hjx social#onClickRefresh:', self.teamName, self.teamTarget)
        p = BigWorld.player()
        self.isSearchResult = True
        p.queryPublicTeams(self.teamName, 0)

    def _getPassingTime(self, startTime):
        p = BigWorld.player()
        return p.getServerTime() - startTime

    def onGetApplyer(self, *arg):
        p = BigWorld.player()
        ret = self.movie.CreateArray()
        for index, value in enumerate(p._getApplyer()):
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(gbk2unicode(value[0])))
            ar.SetElement(1, GfxValue(value[1]))
            ar.SetElement(2, GfxValue(gbk2unicode(SD.data[value[2]]['name'])))
            ar.SetElement(3, GfxValue(self._getPassingTime(value[3])))
            ret.SetElement(index, ar)

        return ret

    def onApplyTimeOut(self, *arg):
        index = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if index != -1 and index < len(p.applyer):
            del p.applyer[index]
            self.refreshApplyer()
            pIndex = gameglobal.rds.ui.teamComm.pageIndex
            gameglobal.rds.ui.teamComm.refreshApplyer(pIndex)

    def onAcceptApplyGroup(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        if index != -1 and index < len(p.applyer):
            p.acceptApplyGroup(p.applyer[index][0], p.applyer[index][4])

    def _getApplyData(self, srcId):
        dataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_APPLY_TEAM)
        for item in dataList:
            if long(item['data'][1]) == srcId:
                return item

    def _getApplyDataWithNonGroup(self, srcId):
        dataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP)
        for item in dataList:
            if long(item['data'][1]) == srcId:
                return item

    def onRejectApplyGroup(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        if index != -1 and index < len(p.applyer):
            p.rejectApplyGroup(p.applyer[index][0], p.applyer[index][4])

    def onClearApplyer(self, *arg):
        p = BigWorld.player()
        for value in p.applyer:
            p.rejectApplyGroup(value[0], value[4])

    def refreshApplyer(self):
        if self.mediator:
            self.mediator.Invoke('refreshApplyMember')

    def pushApplyMessage(self, srcName, srcLevel, srcSchool, srcGbId):
        startTime = BigWorld.player().getServerTime()
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_APPLY_TEAM, {'startTime': startTime,
         'totalTime': 30,
         'data': [30,
                  str(srcGbId),
                  gbk2unicode(srcName),
                  srcLevel,
                  srcSchool]})
        if not BigWorld.player().inCombat:
            self.showApply()

    def pushApplyMessageWithNonGroup(self, srcName, srcLevel, srcSchool, srcGbId):
        startTime = BigWorld.player().getServerTime()
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP, {'startTime': startTime,
         'totalTime': 30,
         'data': [30,
                  str(srcGbId),
                  srcName,
                  srcLevel,
                  srcSchool]})
        if not BigWorld.player().inCombat:
            self.showApplyWithNonGroup()

    def onGetTeamName(self, *arg):
        p = BigWorld.player()
        if hasattr(p, 'detailInfo') and len(p.detailInfo) > 0:
            return GfxValue(gbk2unicode(p.detailInfo['teamName']))
        else:
            return GfxValue(gbk2unicode(self._getDefaultName()))

    def onGetAssignMode(self, *arg):
        ret = self.movie.CreateArray()
        p = BigWorld.player()
        self.assignRule = p.groupAssignWay
        self.assignQuality = const.GROUP_ASSIGN_QUALITY[p.groupAssignQuality]
        ret.SetElement(0, GfxValue(self.assignRule))
        ret.SetElement(1, GfxValue(self.assignQuality))
        return ret

    def onSetAssignMode(self, *arg):
        self.assignRule = int(arg[3][0].GetNumber())
        self.assignQuality = int(arg[3][1].GetNumber())
        BigWorld.player().cell.setGroupAssign(self.assignRule, const.GROUP_ASSIGN_QUALITY[self.assignQuality])

    def onChangeTab(self, *arg):
        type = int(arg[3][0].GetNumber())
        self.groupType = type

    def onChangeToGroup(self, *arg):
        if self.showTeam2GroupWarning(BigWorld.player().cell.team2Group):
            return
        BigWorld.player().cell.team2Group()

    def showTeam2GroupWarning(self, func):
        warning = False
        p = BigWorld.player()
        for questLoopId, info in SCD.data.get('team2GroupNeedWarning', {}).iteritems():
            loop = p.questLoopInfo.get(questLoopId)
            if loop is None:
                continue
            loopInfo = loop.questInfo
            if not loopInfo:
                continue
            currQuestId = loopInfo[-1][0]
            questIds, msgName = info
            if currQuestId in questIds:
                msg = uiUtils.getTextFromGMD(getattr(GMDD.data, msgName))
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, func)
                warning = True

        return warning

    def onSetFilter(self, *arg):
        self.isFilter = arg[3][0].GetBool()
        BigWorld.player().queryPublicTeams('', self.teamTarget)

    def onGetDropDownMenuInfo(self, *arg):
        goalType = int(arg[3][0].GetNumber())
        return self.groupDetailFactory.getDropDownMenuInfo(goalType)

    def isChangeTeamInfo(self):
        p = BigWorld.player()
        return p.groupNUID > 0

    def onIsChangeTeamInfo(self, *arg):
        return GfxValue(self.isChangeTeamInfo())

    def onGetEnableGroupDetailForcely(self, *args):
        return GfxValue(utils.enableGroupDetailForcely())

    def isQuickTeamInfo(self):
        p = BigWorld.player()
        if not hasattr(p, 'detailInfo'):
            return False
        elif p.groupNUID > 0 and p.detailInfo['goal'] == const.GROUP_GOAL_DEFAULT:
            return True
        else:
            return False

    def onIsQuickTeamInfo(self, *arg):
        return GfxValue(self.isQuickTeamInfo())

    def onGetCreateTeamInfo(self, *arg):
        info = {}
        p = BigWorld.player()
        if hasattr(p, 'detailInfo') and self.isChangeTeamInfo():
            info = p.detailInfo
        else:
            info['teamName'] = self._getDefaultName()
            info['lvMin'] = 1
            info['lvMax'] = 79
            info['goal'] = const.GROUP_GOAL_FB
            info['schoolReq'] = const.SCHOOL_SET
        return uiUtils.dict2GfxDict(info, True)

    def hasGoal(self):
        hasGoal = False
        p = BigWorld.player()
        if getattr(p, 'detailInfo', {}).get('goal', const.GROUP_GOAL_DEFAULT) != const.GROUP_GOAL_DEFAULT:
            hasGoal = True
        return hasGoal

    def _getLevel(self, levelStr):
        level = levelStr.split(',')
        try:
            lvMin = int(level[0])
            lvMax = int(level[1])
        except ValueError:
            return (False, 1, 100)

        return (True, lvMin, lvMax)

    def _getNeedSchool(self, schoolStr):
        if schoolStr == '':
            return []
        else:
            return [ int(x) for x in schoolStr.split(',') ]

    def _getTeamName(self):
        return self._getDefaultName()

    def onSetCreateTeamGoalType(self, *arg):
        self.ctCurGoal = int(arg[3][0].GetNumber())

    def onSetTeamDetailGoalType(self, *arg):
        self.tdCurGoal = int(arg[3][0].GetNumber())

    def onGetDropMenuIndex(self, *arg):
        return uiUtils.array2GfxAarry(self.groupDetailFactory.dropMenuVal2Index(self.ctCurGoal))

    def onQuickCreateClick(self, *arg):
        self.quickCreateGroup()

    def quickCreateGroup(self, groupReason = gametypes.TEAM_REASON_NORMAL):
        p = BigWorld.player()
        teamName = self._getTeamName()
        if len(teamName) > const.TEAM_NAME_LENGTH:
            p.showGameMsg(GMDD.data.NAME_LENGTH, const.TEAM_NAME_LENGTH)
            return
        chunkName = BigWorld.ChunkInfoAt(p.position)
        firstKey = CMD.data.get(chunkName, {}).get('mapAreaId', 999)
        secondKey = self.groupDetailFactory.goalIns[const.GROUP_GOAL_DEFAULT].getDefaultSecondKey()
        thirdKey = self.groupDetailFactory.goalIns[self.ctCurGoal].getDefaultThirdKey()
        info = (teamName,
         const.GROUP_GOAL_DEFAULT,
         const.DEFAULT_GROUP_LV_MIN,
         const.DEFAULT_GROUP_LV_MAX,
         const.DEFAULT_GROUP_SCH_REQ,
         const.DEFAULT_GROUP_PUBLIC,
         firstKey,
         secondKey,
         thirdKey)
        gamelog.debug('@hjx social#onQuickCreateClick:', info)
        if p.isInTeamOrGroup():
            p.setGroupDetails(info)
        else:
            p.buildGroup(info, gametypes.GROUP_TYPE_TEAM_GROUP, groupReason)

    def buildNoDetailGroup(self):
        p = BigWorld.player()
        teamName = self._getTeamName()
        if len(teamName) > const.TEAM_NAME_LENGTH:
            p.showGameMsg(GMDD.data.NAME_LENGTH, const.TEAM_NAME_LENGTH)
            return
        chunkName = BigWorld.ChunkInfoAt(p.position)
        firstKey = CMD.data.get(chunkName, {}).get('mapAreaId', 999)
        secondKey = const.DEFAULT_GROUP_SECOND_KEY
        thirdKey = const.DEFAULT_GROUP_THIRD_KEY
        info = (teamName,
         const.GROUP_GOAL_DEFAULT,
         const.DEFAULT_GROUP_LV_MIN,
         const.DEFAULT_GROUP_LV_MAX,
         const.DEFAULT_GROUP_SCH_REQ,
         const.DEFAULT_GROUP_PUBLIC,
         firstKey,
         secondKey,
         thirdKey)
        gamelog.debug('@hjx buildNoDetailGroup:', info)
        if p.isInTeamOrGroup():
            p.setGroupDetails(info)
        else:
            p.buildGroup(info, gametypes.GROUP_TYPE_TEAM_GROUP)

    def onIsPublish(self, *arg):
        return GfxValue(BigWorld.isPublishedVersion())

    def onGetLeftListMenuInfo(self, *arg):
        leftListMenuInfo = self.groupDetailFactory.getLeftListMenuInfo()
        self.hotTagList = self.groupDetailFactory.goalIns[const.GROUP_HOT_TAGS].hotTagItems
        return leftListMenuInfo

    def onSetFilterKey(self, *arg):
        goalType = int(arg[3][0].GetNumber())
        firstKeyIndex = int(arg[3][1].GetNumber())
        secondKeyIndex = int(arg[3][2].GetNumber())
        isGoalType = arg[3][3].GetBool()
        self._doSetFilterKey(goalType, firstKeyIndex, secondKeyIndex, isGoalType)

    def onGetMenuId(self, *args):
        return GfxValue(SCD.data.get('teamHallMenuId', 1000))

    @ui.callInCD(1)
    def _doSetFilterKey(self, goalType, firstKeyIndex, secondKeyIndex, isGoalType):
        gamelog.debug('@hjx social#onSetFilterKey:', goalType, firstKeyIndex, secondKeyIndex)
        self.tdCurGoal = goalType
        self.isSearchResult = False
        if not self.groupDetailFactory.goalIns.has_key(self.tdCurGoal):
            return
        self.isGoalType = isGoalType
        self.groupDetailFactory.goalIns[self.tdCurGoal].setFilterKey(firstKeyIndex, secondKeyIndex)
        if self.tdCurGoal == const.GROUP_HOT_TAGS:
            BigWorld.player().queryPublicTeams('', const.GROUP_GOAL_RELAXATION)
        else:
            BigWorld.player().queryPublicTeams('', self.tdCurGoal)

    def onClickApplyGroupMatch(self, *arg):
        self.groupDetailFactory.goalIns[self.tdCurGoal].applyGroupMatch()

    def onGroupMatchBtnVisiable(self, *args):
        return GfxValue(self.groupDetailFactory.goalIns[self.tdCurGoal].groupMatchBtnVisiable())

    def getShareGroupInfo(self):
        p = BigWorld.player()
        if hasattr(p, 'detailInfo'):
            return
        if p.groupNUID == 0:
            return
        goalDesc = self.groupDetailFactory.goalIns[p.detailInfo['goal']].getTeamGoalDesc(p.detailInfo['firstKey'], p.detailInfo['secondKey'], p.detailInfo['thirdKey'])
        msg = GMD.data.get(GMDD.data.GROUP_SHARE_MSG, {}).get('text', '')
        msg = msg % (p.detailInfo.get('teamName', ''), goalDesc)
        return msg

    def onGetTeamDetailInfo(self, *arg):
        gamelog.debug('@hjx social#onGetTeamDetailInfo:', self.isSearchResult, self.tdCurGoal)
        canJoinFilter = arg[3][0].GetBool()
        if self.isSearchResult:
            teamsInfo = BigWorld.player().teamsInfo
            if canJoinFilter:
                teamsInfo = self._canJoinFilter(teamsInfo)
            return self.groupDetailFactory.getTeamDetailInfo(teamsInfo)
        else:
            if self.isGoalType:
                teamsInfo = self.groupDetailFactory.goalIns[self.tdCurGoal].getGoalTypeInfos()
            else:
                teamsInfo = self.groupDetailFactory.goalIns[self.tdCurGoal].getTeamDetailInfo()
            if canJoinFilter:
                teamsInfo = self._canJoinFilter(teamsInfo)
            return uiUtils.array2GfxAarry(teamsInfo, True)

    def onInviteCC(self, *arg):
        p = BigWorld.player()
        p.doInviteTeam()

    def showByLink(self):
        BigWorld.player().showTeamInfo(True)

    def onGetEnableYecha(self, *argS):
        return GfxValue(gameglobal.rds.configData.get('enableNewSchoolYeCha', False))

    def getShareBtnTipsInfo(self):
        teamInfoUseLv = SCD.data.get('teamInfoUseLv', 20)
        if BigWorld.player().lv < teamInfoUseLv:
            info = gameStrings.TEXT_TEAMPROXY_914 % teamInfoUseLv
        elif self.hasGoal():
            info = gameStrings.TEXT_TEAMPROXY_916 % uiConst.SHARE_TEAM_INFO_CD
        else:
            info = SCD.data.get('needDetailInfoTips', '')
        return info

    def _canJoinFilter(self, data):
        teamsInfo = copy.deepcopy(data)
        p = BigWorld.player()
        for team in data:
            if team['groupType'] == gametypes.GROUP_TYPE_TEAM_GROUP and team['memberCount'] >= const.TEAM_MAX_NUMBER or team['groupType'] == gametypes.GROUP_TYPE_RAID_GROUP and team['memberCount'] >= const.GROUP_MAX_NUMBER or p.school not in team['schoolReq'] or p.lv < team['lvMin'] or p.lv > team['lvMax']:
                teamsInfo.remove(team)

        return teamsInfo

    def refreshJoinTeam(self):
        if self.mediator:
            self.mediator.Invoke('refreshJoinTeam')
            gameglobal.rds.ui.memberDetailsV2.show()

    def _checkAvailable(self, item):
        p = BigWorld.player()
        if item.get('lv'):
            minlv, maxlv = item['lv']
            if p.lv < minlv or p.lv > maxlv:
                return False
        weekSet = item.get('weekSet', 0)
        timeStart = item.get('timeStart')
        timeEnd = item.get('timeEnd')
        if timeStart and timeEnd:
            if not utils.inCrontabRange(timeStart, timeEnd, weekSet=weekSet):
                return False
        return True

    def _avlFilter(self, data):
        tData = copy.deepcopy(data)
        gldd = GLD.data
        for type, typeList in data.items():
            tmpList = tData.get(type, [])
            for key in typeList:
                item = gldd.get(key, {})
                if not self._checkAvailable(item):
                    tmpList.remove(key)

        return tData

    def onGetLabelInfo(self, *args):
        gldd = GLD.data
        ret = []
        for type, data in self.actAvlData.items():
            for i in range(0, len(data)):
                item = gldd.get(data[i], {})
                if item.get('hot', 0):
                    label = {}
                    label['type'] = type
                    label['index'] = i
                    label['name'] = item.get('name', '')
                    label['order'] = item.get('order', 0)
                    ret.append(label)

        ret.sort(key=lambda x: x['order'], reverse=True)
        return uiUtils.array2GfxAarry(ret, True)

    def onGetLvLimit(self, *args):
        btnName = args[3][0].GetString()
        fIndex = int(args[3][1].GetNumber())
        sIndex = int(args[3][2].GetNumber())
        if btnName == 'btn5':
            if sIndex < 0:
                return uiUtils.array2GfxAarry((1, const.MAX_LEVEL))
            key = self.actAvlData.get(fIndex)[sIndex - 1]
            gldd = GLD.data
            item = gldd.get(key, {})
            if item.get('recommendLv'):
                return uiUtils.array2GfxAarry(item['recommendLv'])
            if item.get('lv'):
                return uiUtils.array2GfxAarry(item['lv'])
        elif btnName == 'btn2':
            tIndex = int(args[3][3].GetNumber())
            dropDownMenuInfo = self.groupDetailFactory.goalIns[const.GROUP_GOAL_FB].dropDownMenuInfo
            if dropDownMenuInfo and fIndex and sIndex and tIndex:
                fData = dropDownMenuInfo[fIndex]
                fKey = fData['key']
                sData = fData['data'][sIndex]
                sKey = sData['key']
                tData = sData['data'][tIndex]
                tKey = tData['key']
                fbNo = GFMD.data.get(fKey, {}).get(sKey, {}).get(tKey, {}).get('fbNo', 0)
                if fbNo:
                    lv = []
                    lv.append(FD.data.get(fbNo, {}).get('lvMin', 1))
                    lv.append(FD.data.get(fbNo, {}).get('lvMax', const.MAX_CURRENT_LEVEL))
                    return uiUtils.array2GfxAarry(lv)
            else:
                return uiUtils.array2GfxAarry((1, const.MAX_CURRENT_LEVEL))
        return uiUtils.array2GfxAarry((1, const.MAX_LEVEL))

    def onRefreshAvlActivity(self, *args):
        gldd = GLD.data
        groupActType = SCD.data.get('groupActivityType', {})
        if not self.actTypeData:
            actTypeData = {}
            for tid in groupActType.keys():
                actTypeData[tid] = []

            for key, val in gldd.items():
                type = val.get('type', 0)
                if type not in groupActType.keys():
                    continue
                actTypeData[type].append(key)

            for type, li in actTypeData.items():
                actTypeData[type].sort(key=lambda x: gldd.get(x, {}).get('order', 0), reverse=True)

            self.actTypeData = actTypeData
        self.actAvlData = self._avlFilter(self.actTypeData)

    def onSetAutoShare(self, *args):
        self.isAutoShare = args[3][0].GetBool()

    def onGetAutoShareTips(self, *args):
        if not uiUtils.checkShareTeamLvLimit():
            autoShareTips = gameStrings.SHARE_TEAN_LV_LMIT_TIP % SCD.data.get('teamInfoUseLv', 20)
        else:
            autoShareTips = gameStrings.SHARE_TEAM_DETAIL_TIP
        return GfxValue(gbk2unicode(autoShareTips))

    def openTeamWithType(self, labelId, type = const.GROUP_HOT_TAGS):
        self.labelId = labelId
        self.openGoalType = type
        if not self.isShow:
            self.isOpenType = True
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TEAM)
            self.isShow = True
        elif self.mediator:
            self._selectTeamType()

    def _selectTeamType(self):
        if self.openGoalType == const.GROUP_HOT_TAGS:
            if self.mediator:
                firstKey = self.groupDetailFactory.goalList.index(const.GROUP_HOT_TAGS)
                secondKey = -1
                for key in self.hotTagList:
                    if key == self.labelId:
                        secondKey = self.hotTagList.index(key)

                if secondKey >= 0:
                    keyList = [firstKey, secondKey]
                    self.mediator.Invoke('selectHotTag', uiUtils.array2GfxAarry(keyList))
                else:
                    gldd = GLD.data
                    firstKey = self.groupDetailFactory.goalList.index(const.GROUP_GOAL_RELAXATION)
                    secondKey = gldd.get(self.labelId, {}).get('type', 0) - 1
                    sList = self.actAvlData.get(secondKey + 1, [])
                    if self.labelId in sList:
                        thirdKey = sList.index(self.labelId)
                        keyList = [firstKey,
                         secondKey,
                         thirdKey,
                         self.openGoalType]
                        self.mediator.Invoke('selectTeamType', uiUtils.array2GfxAarry(keyList))
        elif self.openGoalType == const.GROUP_GOAL_FB:
            if self.mediator:
                firstKey = self.groupDetailFactory.goalList.index(const.GROUP_GOAL_FB)
                secondKey = -1
                thirdKey = -1
                fbMenuInfo = self.groupDetailFactory.goalIns[const.GROUP_GOAL_FB].menuInfo
                fbGroupNo = utils.getFbGroupNo(self.labelId)
                for fVal in fbMenuInfo:
                    if fVal['key'] == fbGroupNo:
                        secondKey = fbMenuInfo.index(fVal)
                        sVal = fVal['data']
                        primaryLevel = FD.data.get(self.labelId, {}).get('primaryLevel', 0)
                        for tVal in sVal:
                            if tVal['key'] == primaryLevel:
                                thirdKey = sVal.index(tVal)

                keyList = [firstKey,
                 secondKey,
                 thirdKey,
                 self.openGoalType]
                self.mediator.Invoke('selectTeamType', uiUtils.array2GfxAarry(keyList))

    def onSetTeamType(self, *args):
        self._selectTeamType()
        self.isOpenType = False

    def onGetOpenTypeNeed(self, *args):
        return GfxValue(self.isOpenType)

    def onGetLvAllowShare(self, *args):
        return GfxValue(uiUtils.checkShareTeamLvLimit())

    def onGetGroupDetailTips(self, *args):
        tips = ''
        if not uiUtils.checkShareTeamLvLimit():
            tips = gameStrings.GROUP_DETAIL_LV_LIMIT_TIP % SCD.data.get('teamInfoUseLv', 20)
        return GfxValue(gbk2unicode(tips))
