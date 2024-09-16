#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjSpriteBeInvitedProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import events
import utils
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import MenuManager
from data import zmj_fuben_config_data as ZFCD
from cdata import game_msg_def_data as GMDD

class ZmjSpriteBeInvitedProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjSpriteBeInvitedProxy, self).__init__(uiAdapter)
        self.todayAssistNum = 0
        self.inviteInfoList = []
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZMJ_SPRITE_BE_INVITED, self.hide)

    def reset(self):
        super(ZmjSpriteBeInvitedProxy, self).reset()
        self.widget = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZMJ_SPRITE_BE_INVITED:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(ZmjSpriteBeInvitedProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZMJ_SPRITE_BE_INVITED)

    def show(self):
        if not gameglobal.rds.configData.get('enableZMJAssist', False):
            return
        if self.widget:
            self.widget.swapPanelToFront()
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZMJ_SPRITE_BE_INVITED)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.helpIcon.helpKey = ZFCD.data.get('zmjSpriteBeInvitedHelpKey', 0)
        self.widget.mainMc.scrollWndList.itemRenderer = 'ZmjSpriteBeInvited_ScrollWndListItem'
        self.widget.mainMc.scrollWndList.dataArray = []
        self.widget.mainMc.scrollWndList.lableFunction = self.itemFunction
        self.widget.mainMc.scrollWndList.itemHeight = 37
        self.refreshInfo()

    def addAssistApply(self, qType, todayAssistNum, gbId, name, fbNo, nuid, star, awardFame):
        if not gameglobal.rds.configData.get('enableZMJAssist', False):
            return
        else:
            self.todayAssistNum = todayAssistNum
            if self.inviteInfoList:
                for applyInfo in reversed(self.inviteInfoList):
                    if applyInfo.get('gbId', 0) == gbId:
                        self.inviteInfoList.remove(applyInfo)
                        break

            p = BigWorld.player()
            applyInfo = {}
            applyInfo['qType'] = qType
            applyInfo['gbId'] = gbId
            applyInfo['name'] = name
            applyInfo['fbNo'] = fbNo
            applyInfo['nuid'] = nuid
            applyInfo['star'] = star
            applyInfo['awardFame'] = awardFame
            applyInfo['timeStamp'] = utils.getNow()
            if qType == const.ZMJ_ASSIST_TYPE_FRIEND:
                friends = p.friend
                if friends:
                    friendVal = friends.get(gbId, None)
                    if friendVal:
                        applyInfo['school'] = friendVal.school
            elif qType == const.ZMJ_ASSIST_TYPE_GUILD:
                guild = p.guild
                if guild:
                    member = guild.member.get(gbId, None)
                    if member:
                        applyInfo['school'] = member.school
            self.inviteInfoList.append(applyInfo)
            self.pushInviteMessage()
            self.refreshInfo()
            return

    def removeAssistApply(self, gbId):
        for applyInfo in reversed(self.inviteInfoList):
            if applyInfo.get('gbId', 0) == gbId:
                self.inviteInfoList.remove(applyInfo)

        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        self.todayAssistNum = BigWorld.player().zmjData.get(const.ZMJ_FB_INFO_ASSIST_OTHER_DAY_CNT, 0)
        if self.inviteInfoList:
            for applyInfo in reversed(self.inviteInfoList):
                if applyInfo.get('timeStamp', 0) + ZFCD.data.get('maxWaitTimePerApply', 60) < utils.getNow():
                    self.inviteInfoList.remove(applyInfo)

        self.inviteInfoList.sort(cmp=lambda x, y: cmp(x['timeStamp'], y['timeStamp']), reverse=True)
        if not self.inviteInfoList:
            self.removeInvitePushMsg()
        self.widget.mainMc.scrollWndList.dataArray = self.inviteInfoList
        self.widget.mainMc.scrollWndList.validateNow()
        self.widget.mainMc.emptyHint.text = gameStrings.ZMJ_SPRITE_BE_INVITE_EMPTY_TXT
        self.widget.mainMc.emptyHint.visible = len(self.inviteInfoList) == 0
        leftCnt = max(ZFCD.data.get('beApplyAssistDayLimit', 0) - self.todayAssistNum, 0)
        self.widget.remainTip.htmlText = gameStrings.ZMJ_SPRITE_BE_INVITE_REMAIN_TXT % leftCnt

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if not itemData:
            itemMc.visible = False
            return
        itemMc.visible = True
        itemMc.overMc.visible = False
        if itemData.school:
            itemMc.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(itemData.school))
        itemMc.playerName.text = itemData.name
        itemMc.level.text = itemData.star
        itemMc.reward.text = '%s/%s' % (itemData.awardFame, itemData.awardFame)
        itemMc.agreeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickAgreeBtn, False, 0, True)
        itemMc.refuseBtn.addEventListener(events.MOUSE_CLICK, self.handleClickRefuseBtn, False, 0, True)
        itemMc.data = itemData
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleOverItem, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleOutItem, False, 0, True)
        menuParam = {'roleName': itemData.name,
         'gbId': itemData.gbId}
        MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_CHAT, menuParam)

    def handleClickAgreeBtn(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget.parent
        data = itemMc.data
        gbId = long(data.gbId)
        qType = data.qType
        fbNo = data.fbNo
        spaceNUID = data.nuid
        p = BigWorld.player()
        self.todayAssistNum = p.zmjData.get(const.ZMJ_FB_INFO_ASSIST_OTHER_DAY_CNT, 0)
        leftCnt = max(ZFCD.data.get('beApplyAssistDayLimit', 0) - self.todayAssistNum, 0)
        if leftCnt == 0:
            p.showGameMsg(GMDD.data.ZMJ_AGREE_ASSIST_FAIL_NOT_HAS_NUM, ())
            return
        BigWorld.player().cell.agreeZMJAssist(qType, gbId, fbNo, long(spaceNUID))

    def handleClickRefuseBtn(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget.parent
        data = itemMc.data
        gbId = long(data.gbId)
        for applyInfo in reversed(self.inviteInfoList):
            if applyInfo.get('gbId', 0) == gbId:
                self.inviteInfoList.remove(applyInfo)

        if not self.inviteInfoList:
            self.removeInvitePushMsg()
        self.widget.mainMc.scrollWndList.dataArray = self.inviteInfoList
        self.widget.mainMc.scrollWndList.validateNow()
        self.widget.mainMc.emptyHint.visible = len(self.inviteInfoList) == 0

    def handleOverItem(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = True

    def handleOutItem(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = False

    def pushInviteMessage(self):
        pushId = uiConst.MESSAGE_TYPE_ZMJ_SPRITE_INVITE
        if pushId not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': self.onPushMsgClick})

    def removeInvitePushMsg(self):
        pushId = uiConst.MESSAGE_TYPE_ZMJ_SPRITE_INVITE
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def onPushMsgClick(self):
        self.show()
