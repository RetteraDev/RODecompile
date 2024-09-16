#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildInheritProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import uiUtils
import ui
import formula
import gametypes
import utils
from uiTabProxy import UITabProxy
from callbackHelper import Functor
from gamestrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import MenuManager
from messageBoxProxy import MBButton
from data import guild_config_data as GCD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
TAB_INDEX_APPLY = 0
TAB_INDEX_INVITE = 1
BTN_TYPE_ERROR = 0
BTN_TYPE_APPLY = 1
BTN_TYPE_INVITE = 2

def sort_apply(a, b):
    if a['lvValid'] > b['lvValid']:
        return -1
    if a['lvValid'] < b['lvValid']:
        return 1
    if a['online'] > b['online']:
        return -1
    if a['online'] < b['online']:
        return 1
    if a['hasCnt'] > b['hasCnt']:
        return -1
    if a['hasCnt'] < b['hasCnt']:
        return 1
    if a['xiuweiLv'] > b['xiuweiLv']:
        return -1
    if a['xiuweiLv'] < b['xiuweiLv']:
        return 1
    return 0


def sort_invite(a, b):
    if a['lvValid'] > b['lvValid']:
        return -1
    if a['lvValid'] < b['lvValid']:
        return 1
    if a['online'] > b['online']:
        return -1
    if a['online'] < b['online']:
        return 1
    if a['hasCnt'] > b['hasCnt']:
        return -1
    if a['hasCnt'] < b['hasCnt']:
        return 1
    if a['xiuweiLv'] < b['xiuweiLv']:
        return -1
    if a['xiuweiLv'] > b['xiuweiLv']:
        return 1
    return 0


class GuildInheritProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(GuildInheritProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        self.requestMsgBoxIds = {}
        self.inviteMsgBoxIds = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_INHERIT, self.hide)

    def reset(self):
        super(GuildInheritProxy, self).reset()
        self.applyInfoDict = {}
        self.inviteInfoDict = {}
        self.invitedGbIds = []
        self.requestedGbIds = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_INHERIT:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)

    def clearWidget(self):
        super(GuildInheritProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_INHERIT)

    def _getTabList(self):
        return [{'tabIdx': TAB_INDEX_APPLY,
          'tabName': 'tabBtn0',
          'view': 'GuildInherit_DetailMc'}, {'tabIdx': TAB_INDEX_INVITE,
          'tabName': 'tabBtn1',
          'view': 'GuildInherit_DetailMc'}]

    def show(self):
        if not gameglobal.rds.configData.get('enableGuildInherit', False):
            BigWorld.player().showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        if self.widget:
            self.widget.swapPanelToFront()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_INHERIT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.helpIcon.helpKey = GCD.data.get('guildInheritXiuweiLvHelpKey', 0)
        self.initTabUI()

    def onTabChanged(self, *args):
        super(GuildInheritProxy, self).onTabChanged(*args)
        self.currentView.scrollWndList.itemRenderer = 'GuildInherit_ScrollWndListItem'
        self.currentView.scrollWndList.dataArray = []
        if self.currentTabIndex == TAB_INDEX_APPLY:
            self.currentView.scrollWndList.lableFunction = self.applyItemFunction
        else:
            self.currentView.scrollWndList.lableFunction = self.inviteItemFunction
        self.currentView.scrollWndList.itemHeight = 37
        self.queryInfo()
        self.refreshInfo()

    def queryInfo(self):
        p = BigWorld.player()
        if self.currentTabIndex == TAB_INDEX_APPLY:
            p.cell.guildInheritGetGiverList()
        else:
            p.cell.guildInheritGetReceiverList()

    def updateApplyListInfo(self, applyInfoList):
        self.applyInfoDict = {}
        for applyInfo in applyInfoList:
            self.applyInfoDict[applyInfo[0]] = {'isFlowback': applyInfo[1],
             'xiuweiLv': applyInfo[2],
             'useCnt': applyInfo[3],
             'isClicked': False}

        self.refreshApplyInfoInCD()

    def updateInviteListInfo(self, inviteInfoList):
        self.inviteInfoDict = {}
        for inviteInfo in inviteInfoList:
            self.inviteInfoDict[inviteInfo[0]] = {'isFlowback': inviteInfo[1],
             'xiuweiLv': inviteInfo[2],
             'useCnt': inviteInfo[3],
             'isClicked': False}

        self.refreshInviteInfoInCD()

    @ui.callInCD(0.5)
    def refreshInfoInCD(self):
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        if self.currentTabIndex == TAB_INDEX_APPLY:
            self.refreshApplyInfo()
        else:
            self.refreshInviteInfo()

    @ui.callInCD(0.5)
    def refreshApplyInfoInCD(self):
        self.refreshApplyInfo()

    def refreshApplyInfo(self):
        if not self.widget:
            return
        elif self.currentTabIndex != TAB_INDEX_APPLY:
            return
        else:
            self.currentView.gotoNpc.visible = True
            self.currentView.gotoNpc.target.htmlText = gameStrings.GUILD_INHERIT_GOTO_ACTIVITY_NPC
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            lvLimit = GCD.data.get('guildInheritMinLevelLtd', 0)
            xiuweiLevelDiff = GCD.data.get('xiuweiLevelDiff', 0)
            todayGiveInheritCnt = GCD.data.get('todayGiveInheritCnt', 0)
            applyList = []
            for gbId, itemDetail in self.applyInfoDict.iteritems():
                member = guild.member.get(gbId, None)
                if not member:
                    continue
                xiuweiLv = itemDetail.get('xiuweiLv', 0)
                if member.level < lvLimit:
                    lvValid = False
                else:
                    lvValid = xiuweiLv >= p.xiuweiLevel + xiuweiLevelDiff
                applyList.append({'gbId': gbId,
                 'online': member.online,
                 'lvValid': lvValid,
                 'xiuweiLv': xiuweiLv,
                 'hasCnt': todayGiveInheritCnt > itemDetail.get('useCnt', 0)})

            applyList.sort(cmp=sort_apply)
            self.currentView.scrollWndList.dataArray = applyList
            self.currentView.scrollWndList.validateNow()
            self.currentView.emptyHint.visible = len(applyList) == 0
            leftCnt = max(GCD.data.get('todayRecvInheritCnt', 0) - p.todayRecvInheritCnt, 0)
            self.currentView.hint.htmlText = uiUtils.getTextFromGMD(GMDD.data.GUILD_INHERIT_APPLY_PANEL_HINT, '%d') % leftCnt
            return

    @ui.callInCD(0.5)
    def refreshInviteInfoInCD(self):
        self.refreshInviteInfo()

    def refreshInviteInfo(self):
        if not self.widget:
            return
        elif self.currentTabIndex != TAB_INDEX_INVITE:
            return
        else:
            self.currentView.gotoNpc.visible = False
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            lvLimit = GCD.data.get('guildInheritMinLevelLtd', 0)
            xiuweiLevelDiff = GCD.data.get('xiuweiLevelDiff', 0)
            todayRecvInheritCnt = GCD.data.get('todayRecvInheritCnt', 0)
            inviteList = []
            for gbId, itemDetail in self.inviteInfoDict.iteritems():
                member = guild.member.get(gbId, None)
                if not member:
                    continue
                xiuweiLv = itemDetail.get('xiuweiLv', 0)
                if member.level < lvLimit:
                    lvValid = False
                else:
                    lvValid = p.xiuweiLevel >= xiuweiLv + xiuweiLevelDiff
                inviteList.append({'gbId': gbId,
                 'online': member.online,
                 'lvValid': lvValid,
                 'xiuweiLv': xiuweiLv,
                 'hasCnt': todayRecvInheritCnt > itemDetail.get('useCnt', 0)})

            inviteList.sort(cmp=sort_invite)
            self.currentView.scrollWndList.dataArray = inviteList
            self.currentView.scrollWndList.validateNow()
            self.currentView.emptyHint.visible = len(inviteList) == 0
            leftCnt = max(GCD.data.get('todayGiveInheritCnt', 0) - p.todayGiveInheritCnt, 0)
            self.currentView.hint.htmlText = uiUtils.getTextFromGMD(GMDD.data.GUILD_INHERIT_INVITE_PANEL_HINT, '%d') % leftCnt
            return

    def applyItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        gbId = long(itemData.gbId)
        itemDetail = self.applyInfoDict.get(gbId, {})
        guild = BigWorld.player().guild
        member = guild.member.get(gbId, None) if guild else None
        if not itemDetail or not member:
            itemMc.visible = False
            return
        else:
            itemMc.visible = True
            itemMc.overMc.visible = False
            if itemData.online:
                itemMc.gotoAndStop('online')
                itemMc.space.text = formula.whatAreaName(member.spaceNo, member.areaId)
            else:
                itemMc.gotoAndStop('offline')
                itemMc.space.text = gameStrings.GUILD_INHERIT_OFFLINE_TEXT
            itemMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(member.school))
            itemMc.playerName.text = member.role
            itemMc.xiuweiLv.text = itemData.xiuweiLv
            if not itemData.lvValid:
                if member.level < GCD.data.get('guildInheritMinLevelLtd', 0):
                    itemMc.timesFlag.text = gameStrings.GUILD_INHERIT_LEVEL_INVALID
                else:
                    itemMc.timesFlag.text = gameStrings.GUILD_INHERIT_XIUWEI_LEVEL_INVALID
            elif not itemData.hasCnt:
                itemMc.timesFlag.text = gameStrings.GUILD_INHERIT_TIMES_INVALID
            else:
                itemMc.timesFlag.text = ''
            if itemDetail.get('isFlowback', 0):
                itemMc.flowbackFlag.visible = True
                TipManager.addTip(itemMc.flowbackFlag, GCD.data.get('guildInheritFlowbackFlag', ''))
            else:
                itemMc.flowbackFlag.visible = False
            itemMc.gbId = gbId
            if not itemData.online or not itemData.hasCnt or not itemData.lvValid:
                itemMc.sendMsg.visible = True
                itemMc.btn.visible = False
                itemMc.sendMsg.addEventListener(events.MOUSE_CLICK, self.handleClickSendMsg, False, 0, True)
            else:
                itemMc.sendMsg.visible = False
                itemMc.btn.visible = True
                if itemDetail.get('isClicked', False) or gbId in self.requestedGbIds:
                    itemMc.btnType = BTN_TYPE_ERROR
                    itemMc.btn.label = gameStrings.GUILD_INHERIT_ALREADY_LABEL
                    itemMc.btn.enabled = False
                else:
                    itemMc.btnType = BTN_TYPE_APPLY
                    itemMc.btn.label = gameStrings.GUILD_INHERIT_APPLY_LABEL
                    itemMc.btn.enabled = True
                itemMc.btn.addEventListener(events.BUTTON_CLICK, self.handleClickBtn, False, 0, True)
            itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverItem, False, 0, True)
            itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleOutItem, False, 0, True)
            MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_GUILD, {'roleName': member.role})
            return

    def inviteItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        gbId = long(itemData.gbId)
        itemDetail = self.inviteInfoDict.get(gbId, {})
        guild = BigWorld.player().guild
        member = guild.member.get(gbId, None) if guild else None
        if not itemDetail or not member:
            itemMc.visible = False
            return
        else:
            itemMc.visible = True
            itemMc.overMc.visible = False
            if itemData.online:
                itemMc.gotoAndStop('online')
                itemMc.space.text = formula.whatAreaName(member.spaceNo, member.areaId)
            else:
                itemMc.gotoAndStop('offline')
                itemMc.space.text = gameStrings.GUILD_INHERIT_OFFLINE_TEXT
            itemMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(member.school))
            itemMc.playerName.text = member.role
            itemMc.xiuweiLv.text = itemData.xiuweiLv
            if not itemData.lvValid:
                if member.level < GCD.data.get('guildInheritMinLevelLtd', 0):
                    itemMc.timesFlag.text = gameStrings.GUILD_INHERIT_LEVEL_INVALID
                else:
                    itemMc.timesFlag.text = gameStrings.GUILD_INHERIT_XIUWEI_LEVEL_INVALID
            elif not itemData.hasCnt:
                itemMc.timesFlag.text = gameStrings.GUILD_INHERIT_TIMES_INVALID
            else:
                itemMc.timesFlag.text = ''
            if itemDetail.get('isFlowback', 0):
                itemMc.flowbackFlag.visible = True
                TipManager.addTip(itemMc.flowbackFlag, GCD.data.get('guildInheritFlowbackFlag', ''))
            else:
                itemMc.flowbackFlag.visible = False
            itemMc.gbId = gbId
            if not itemData.online or not itemData.hasCnt or not itemData.lvValid:
                itemMc.sendMsg.visible = True
                itemMc.btn.visible = False
                itemMc.sendMsg.addEventListener(events.MOUSE_CLICK, self.handleClickSendMsg, False, 0, True)
            else:
                itemMc.sendMsg.visible = False
                itemMc.btn.visible = True
                if itemDetail.get('isClicked', False) or gbId in self.invitedGbIds:
                    itemMc.btnType = BTN_TYPE_ERROR
                    itemMc.btn.label = gameStrings.GUILD_INHERIT_ALREADY_LABEL
                    itemMc.btn.enabled = False
                else:
                    itemMc.btnType = BTN_TYPE_INVITE
                    itemMc.btn.label = gameStrings.GUILD_INHERIT_INVITE_LABEL
                    itemMc.btn.enabled = True
                itemMc.btn.addEventListener(events.BUTTON_CLICK, self.handleClickBtn, False, 0, True)
            itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverItem, False, 0, True)
            itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleOutItem, False, 0, True)
            MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_GUILD, {'roleName': member.role})
            return

    def handleClickSendMsg(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget.parent
        gbId = long(itemMc.gbId)
        p = BigWorld.player()
        if p.friend.isFriend(gbId):
            self.uiAdapter.friend.beginChat(gbId)
        else:
            p.base.addContactByGbId(gbId, gametypes.FRIEND_GROUP_FRIEND, 0)

    def handleClickBtn(self, *args):
        e = ASObject(args[3][0])
        if not e.currentTarget.parent:
            return
        itemMc = e.currentTarget.parent
        gbId = long(itemMc.gbId)
        p = BigWorld.player()
        btnType = itemMc.btnType
        if btnType == BTN_TYPE_APPLY:
            if not uiUtils.hasVipBasic():
                p.showGameMsg(GMDD.data.GUILD_INHERIT_SELF_IS_NOT_VIP, ())
                return
            self.requestedGbIds.append(gbId)
            p.cell.guildInheritSendRequest(gbId)
        elif btnType == BTN_TYPE_INVITE:
            if not uiUtils.hasVipBasic():
                p.showGameMsg(GMDD.data.GUILD_INHERIT_SELF_IS_NOT_VIP, ())
                return
            self.invitedGbIds.append(gbId)
            p.cell.guildInheritSendInvite(gbId)

    def handleOverItem(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = True

    def handleOutItem(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = False

    def handleGotoNPC(self, *args):
        seekId = SCD.data.get('inheriteNpcSeekID', 0)
        uiUtils.findPosById(seekId)
        self.hide()

    def updateGuildInheritPushMsg(self, msgType, data):
        if not gameglobal.rds.configData.get('enableGuildInherit', False):
            return
        pushMessage = self.uiAdapter.pushMessage
        if not pushMessage.hasPushData(msgType, {'data': data}):
            pushMessage.setCallBack(msgType, {'click': Functor(self.showPushMsg, msgType)})
            pushMessage.addPushMsg(msgType, {'data': data,
             'startTime': utils.getNow(),
             'totalTime': 60})

    def showPushMsg(self, msgType):
        pushMessage = self.uiAdapter.pushMessage
        pushData = pushMessage.getFirstData(msgType)
        pushMessage.removeData(msgType, pushData)
        if not pushData:
            return
        data = pushData.get('data', {})
        gbId = data.get('gbId', 0)
        roleName = data.get('roleName', '')
        if msgType == uiConst.MESSAGE_TYPE_GUILD_INHERIT_APPLY:
            msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_INHERIT_APPLY_PUSH_HINT, '%s') % roleName
            buttons = (MBButton(gameStrings.ITEM_MSG_BOX_YESBTN_LABEL_DEFAULT, Functor(self.confrimRequest, gbId), dismissOnClick=False), MBButton(gameStrings.ITEM_MSG_BOX_NOBTN_LABEL_DEFAULT))
            self.requestMsgBoxIds[gbId] = self.uiAdapter.messageBox.show(False, gameStrings.ITEM_MSG_BOX_TITLE_DEFAULT, msg, buttons)
        elif msgType == uiConst.MESSAGE_TYPE_GUILD_INHERIT_INVITE:
            msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_INHERIT_INVITE_PUSH_HINT, '%s') % roleName
            buttons = (MBButton(gameStrings.ITEM_MSG_BOX_YESBTN_LABEL_DEFAULT, Functor(self.confrimInvite, gbId), dismissOnClick=False), MBButton(gameStrings.ITEM_MSG_BOX_NOBTN_LABEL_DEFAULT))
            self.inviteMsgBoxIds[gbId] = self.uiAdapter.messageBox.show(False, gameStrings.ITEM_MSG_BOX_TITLE_DEFAULT, msg, buttons)

    def confrimRequest(self, gbId):
        p = BigWorld.player()
        if not uiUtils.hasVipBasic():
            p.showGameMsg(GMDD.data.GUILD_INHERIT_SELF_IS_NOT_VIP, ())
            return
        p.cell.guildInheritReplyTheRequest(gbId)

    def confrimInvite(self, gbId):
        p = BigWorld.player()
        if not uiUtils.hasVipBasic():
            p.showGameMsg(GMDD.data.GUILD_INHERIT_SELF_IS_NOT_VIP, ())
            return
        p.cell.guildInheritReplyTheInvite(gbId)

    def refreshCurrentViewList(self):
        if not self.widget:
            return
        else:
            dataArray = self.currentView.scrollWndList.dataArray
            self.currentView.scrollWndList.dataArray = None
            self.currentView.scrollWndList.dataArray = dataArray
            self.currentView.scrollWndList.validateNow()
            return

    def dissMissMsgBox(self, msgType, gbId):
        if msgType == uiConst.MESSAGE_TYPE_GUILD_INHERIT_APPLY:
            if gbId in self.requestMsgBoxIds:
                msgBoxId = self.requestMsgBoxIds[gbId]
                gameglobal.rds.ui.messageBox.dismiss(msgBoxId)
                del self.requestMsgBoxIds[gbId]
        elif msgType == uiConst.MESSAGE_TYPE_GUILD_INHERIT_INVITE:
            if gbId in self.inviteMsgBoxIds:
                msgBoxId = self.inviteMsgBoxIds[gbId]
                gameglobal.rds.ui.messageBox.dismiss(msgBoxId)
                del self.inviteMsgBoxIds[gbId]
