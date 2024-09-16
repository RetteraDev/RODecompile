#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/teamInviteV2Proxy.o
import BigWorld
import copy
import gameglobal
import uiConst
import const
import utils
import events
import gametypes
import groupDetailFactory
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis import relationLabelUtils
from callbackHelper import Functor
TOTAL_TIME = 30
TEAM_MEMBER_MAX = 5
TEAM_NAME_IDX = 0
REMAIN_TIME_IDX = 1
GROUPNUID_IDX = 2
SRC_GBID_IDX = 3
SRC_NAME_IDX = 4
MEMBERS_IDX = 5
MEMBER_CNT_IDX = 6
SRC_PARAMS_IDX = 7

class TeamInviteV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TeamInviteV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.handler = None
        self.data = []
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_TEAM_INVITE_V2, self.hide)

    def setPushMsgCallback(self):
        inviteCallbacks = {'click': self.showInvite,
         'refresh': self.refresh,
         'timeout': self.inviteTimeOut}
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_INVITE_TEAM, inviteCallbacks)
        recommendCallbacks = {'click': self.showRecommend,
         'refresh': self.refresh,
         'timeout': self.recommendTimeOut}
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM, recommendCallbacks)

    def reset(self):
        self.handler and BigWorld.cancelCallback(self.handler)
        self.handler = None
        self.hoverItem = None
        self.showType = uiConst.MESSAGE_TYPE_INVITE_TEAM

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TEAM_INVITE_V2:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TEAM_INVITE_V2)

    def show(self, showType):
        isTypeChanged = showType != self.showType
        self.showType = showType
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_TEAM_INVITE_V2)
        else:
            self.refresh(isTypeChanged)

    def initUI(self):
        self.refreshAllUI()
        self.initListProp()
        self.handler = BigWorld.callback(0.5, self.refreshCountDownCallback)
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def getRemainTime(self, totalTime, startTime):
        if not totalTime or not startTime:
            return 0
        return max(0, int(totalTime - (utils.getNow() - startTime)))

    def initListProp(self):
        self.widget.teamList.itemRenderer = 'TeamInviteV2_PlayerItem'
        self.widget.teamList.lableFunction = self.itemLabelFunc

    def updateList(self):
        if not self.widget:
            return
        self.widget.teamList.dataArray = self.data
        self.widget.teamList.validateNow()

    def refreshCountDownCallback(self):
        self.handler and BigWorld.cancelCallback(self.handler)
        self.refresh()
        self.handler = BigWorld.callback(0.5, self.refreshCountDownCallback)

    def refresh(self, isTypeChanged = False):
        if not self.widget:
            return
        if not self.getMsgData(self.showType):
            self.hide()
            return
        isInviteNumChanged = self.isInviteNumChanged()
        if isTypeChanged or isInviteNumChanged:
            self.refreshAllUI()
        else:
            self.refreshListTime()

    def isInviteNumChanged(self):
        oldData = self.data
        newData = self.getMsgData(self.showType)
        return len(oldData) != len(newData)

    def refreshAllUI(self):
        self.data = self.getCurrentMsgDataCopy()
        self.updateList()
        if self.showType == uiConst.MESSAGE_TYPE_INVITE_TEAM:
            self.widget.inviteNumTf.htmlText = gameStrings.TEAM_INVITE_NUM % len(self.data)
            self.widget.title.textField.text = gameStrings.TEAM_INVITE
            self.widget.srcTf.text = gameStrings.TEAM_INVITER
        else:
            self.widget.inviteNumTf.htmlText = gameStrings.TEAM_RECOMMEND_NUM % len(self.data)
            self.widget.title.textField.text = gameStrings.TEAM_RECOMMEND
            self.widget.srcTf.text = gameStrings.TEAM_RECOMMENDER

    def refreshListTime(self):
        items = self.widget.teamList.items
        for item in items:
            self.updateItemRemindTime(item)

    def itemLabelFunc(self, *args):
        item = ASObject(args[3][1])
        itemInfo = ASObject(args[3][0])
        item.data = itemInfo.data
        item.startTime = itemInfo.startTime
        item.totalTime = itemInfo.totalTime
        self.updateItemInviterInfo(item)
        self.updateItemMember(item)
        self.updateItemRemindTime(item)
        self.updateItemGoal(item)
        self.registerEvent(item)
        item.overBg.visible = self.hoverItem == item

    def updateItemInviterInfo(self, item):
        info = item.data
        item.inviterNameTf.text = info[SRC_NAME_IDX]
        self.updateItemLabel(item, info[SRC_GBID_IDX])
        self.updateItemInviterPhoto(item)

    def updateItemLabel(self, item, gbId):
        labelFrameNames = relationLabelUtils.getValidLabelsName(gbId)
        labelCnt = len(labelFrameNames)
        for i in xrange(uiConst.PLAYER_ITEM_MAX_LABEL):
            label = getattr(item.labelMc, 'label%d' % i)
            if i < labelCnt:
                label.gotoAndStop(labelFrameNames[i])
                label.visible = True
            else:
                label.visible = False

    def updateItemInviterPhoto(self, item):
        info = item.data
        photo = info[SRC_PARAMS_IDX].get('srcPhoto')
        item.inviterIcon.setContentUnSee()
        item.inviterIcon.fitSize = True
        if not photo:
            school = info[SRC_PARAMS_IDX].get('srcSchool')
            sex = info[SRC_PARAMS_IDX].get('srcSex')
            photo = BigWorld.player().friend.getDefaultPhoto(school, sex)
            item.inviterIcon.loadImage(photo)
        else:
            item.inviterIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
            item.inviterIcon.url = photo

    def updateItemMember(self, item):
        info = item.data
        memberDetail = info[MEMBERS_IDX]
        groupMemberTf = item.groupMemberTf
        teamMemberMc = item.teamMemberMc
        if not (memberDetail and groupMemberTf and teamMemberMc):
            groupMemberTf.visible = False
            teamMemberMc.visible = False
            return
        groupType = info[SRC_PARAMS_IDX].get('groupType', gametypes.GROUP_TYPE_TEAM_GROUP)
        if groupType == gametypes.GROUP_TYPE_RAID_GROUP:
            teamMemberMc.visible = False
            self.updateGroupMember(groupMemberTf, info[MEMBER_CNT_IDX])
        elif groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
            groupMemberTf.visible = False
            self.updateTeamMember(teamMemberMc, memberDetail)

    def updateGroupMember(self, groupMemberTf, memberCnt):
        groupMemberTf.visible = True
        groupMemberTf.htmlText = gameStrings.TEAM_GROUP_NUMBER % memberCnt

    def updateTeamMember(self, teamMemberMc, memberDetail):
        teamMemberMc.visible = True
        memberCnt = len(memberDetail)
        for i in xrange(TEAM_MEMBER_MAX):
            playerMc = getattr(teamMemberMc, 'p%d' % i)
            if i >= memberCnt:
                playerMc.visible = False
            else:
                memberInfo = memberDetail[i]
                frameName = uiConst.SCHOOL_FRAME_DESC.get(memberInfo.school)
                schoolName = const.SCHOOL_DICT.get(memberInfo.school)
                playerMc.gotoAndStop(frameName)
                tipStr = gameStrings.TEAM_INVITE_PLAYER_TIP % (memberInfo.roleName, schoolName, memberInfo.level)
                TipManager.addTip(playerMc, tipStr)
                playerMc.visible = True

    def updateItemRemindTime(self, item):
        remainTime = self.getRemainTime(item.startTime, item.totalTime)
        item.countDownTf.text = gameStrings.TEAM_TIME_TEXT % remainTime

    def updateItemGoal(self, item):
        info = item.data
        params = info[SRC_PARAMS_IDX]
        goalType = params.get('goal', 0)
        fKey = params.get('firstKey', 1)
        sKey = params.get('secondKey', 1)
        tKey = params.get('thirdKey', 1)
        teamGoal1, teamGoal2 = groupDetailFactory.getInstance().getTeamGoalMultiDesc(goalType, fKey, sKey, tKey)
        item.goalTf1.text = teamGoal1
        item.goalTf2.text = teamGoal2

    def registerEvent(self, item):
        item.joinBtn.addEventListener(events.BUTTON_CLICK, self.handleClickJoinBtn, False, 0, True)
        item.addEventListener(events.MOUSE_ROLL_OVER, self.handleRollOver, False, 0, True)
        item.addEventListener(events.MOUSE_ROLL_OUT, self.handleRollOut, False, 0, True)

    def handleRollOver(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget
        item.overBg.visible = True
        self.hoverItem = item

    def handleRollOut(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget
        item.overBg.visible = False
        self.hoverItem = None

    def handleClickJoinBtn(self, *args):
        e = ASObject(args[3][0])
        item = e.currentTarget.parent
        if self.showType == uiConst.MESSAGE_TYPE_INVITE_TEAM:
            self.acceptInvite(item)
        else:
            self.acceptRecommend(item)

    def acceptInvite(self, item):
        if not item.data:
            return
        groupNUID = long(item.data[GROUPNUID_IDX])
        srcGbId = long(item.data[SRC_GBID_IDX])
        srcName = item.data[SRC_NAME_IDX]
        p = BigWorld.player()
        if p.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
            if self.uiAdapter.team.showTeam2GroupWarning(Functor(p.acceptGroup, groupNUID, srcGbId, srcName)):
                return
        p.acceptGroup(groupNUID, srcGbId, srcName)

    def acceptRecommend(self, item):
        if not item.data:
            return
        headerName = item.data[SRC_PARAMS_IDX].get('headerName', '')
        BigWorld.player().applyGroup(headerName)
        srcId = long(item.data[SRC_GBID_IDX])
        delData = self.getItemDataByGbId(self.showType, srcId)
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM, delData)

    def _onMinimizeBtnClick(self, e):
        self.hide()

    def _onIgnoreBtnClick(self, e):
        p = BigWorld.player()
        if self.showType == uiConst.MESSAGE_TYPE_INVITE_TEAM:
            for item in self.getMsgData(self.showType):
                p.rejectInviteGroup(long(item['data'][SRC_GBID_IDX]))

        else:
            for item in self.getMsgData(self.showType):
                p.rejectRecommendGroup(long(item['data'][SRC_GBID_IDX]))

        gameglobal.rds.ui.pushMessage.removePushMsg(self.showType)
        self.hide()

    def onInviteRecommendResult(self, srcGbId):
        delData = self.getItemDataByGbId(self.showType, srcGbId)
        gameglobal.rds.ui.pushMessage.removeData(self.showType, delData)
        self.hide()

    def getCurrentMsgDataCopy(self):
        return copy.copy(self.getMsgData(self.showType))

    def getMsgData(self, msgType):
        ret = gameglobal.rds.ui.pushMessage.getDataList(msgType)
        if ret:
            return ret
        return []

    def getItemDataByGbId(self, msgType, srcId):
        msgData = gameglobal.rds.ui.pushMessage.getDataList(msgType)
        ret = [ item for item in msgData if long(item['data'][SRC_GBID_IDX]) == srcId ]
        if ret:
            return ret[0]
        else:
            return None

    def showInvite(self):
        self.show(uiConst.MESSAGE_TYPE_INVITE_TEAM)

    def showRecommend(self):
        self.show(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM)

    def pushInviteMessage(self, groupNUID, srcGbId, memCount, srcName, teamName, srcSchool, srcLevel, memberDetail, groupType, params):
        startTime = utils.getNow()
        members = [{'roleName': srcName,
          'school': srcSchool,
          'level': srcLevel}]
        members.extend(memberDetail)
        params['srcSchool'] = srcSchool
        params['groupType'] = groupType
        inviteData = {'startTime': startTime,
         'totalTime': TOTAL_TIME,
         'data': [teamName,
                  TOTAL_TIME,
                  groupNUID,
                  srcGbId,
                  srcName,
                  members,
                  memCount,
                  params]}
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_INVITE_TEAM, inviteData)
        if not BigWorld.player().inCombat and not self.widget:
            self.showInvite()

    def pushRecommendMessage(self, srcGbId, srcName, srcLevel, srcSchool, memCount, headerName, teamName, groupType, params):
        startTime = utils.getNow()
        memberDetail = params.get('memberDetail', [])
        members = [{'roleName': srcName,
          'school': srcSchool,
          'level': srcLevel}]
        members.extend(memberDetail)
        params['srcSchool'] = srcSchool
        params['groupType'] = groupType
        params['headerName'] = headerName
        recommendData = {'startTime': startTime,
         'totalTime': TOTAL_TIME,
         'data': [teamName,
                  TOTAL_TIME,
                  0,
                  srcGbId,
                  srcName,
                  members,
                  memCount,
                  params]}
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM, recommendData)
        if not BigWorld.player().inCombat and not self.widget:
            self.showRecommend()

    def inviteTimeOut(self, item):
        p = BigWorld.player()
        srcId = long(item['data'][SRC_GBID_IDX])
        p.rejectInviteGroup(srcId)
        timeoutData = self.getItemDataByGbId(uiConst.MESSAGE_TYPE_INVITE_TEAM, srcId)
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_INVITE_TEAM, timeoutData)
        if hasattr(p, 'acceptMsgBoxId') and p.acceptMsgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(p.acceptMsgBoxId)

    def recommendTimeOut(self, item):
        p = BigWorld.player()
        srcId = long(item['data'][SRC_GBID_IDX])
        p.cell.recommendGroupOverTime(srcId)
        timeoutData = self.getItemDataByGbId(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM, srcId)
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM, timeoutData)
        if hasattr(p, 'acceptMsgBoxId') and p.acceptMsgBoxId:
            gameglobal.rds.ui.messageBox.dismiss(p.acceptMsgBoxId)
