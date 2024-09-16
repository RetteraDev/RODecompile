#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendInviteV2Proxy.o
from gamestrings import gameStrings
import BigWorld
import events
import gameglobal
import gametypes
import ui
import qrcode
import keys
import base64
from uiProxy import UIProxy
from asObject import ASObject
from guis import uiUtils
from guis import messageBoxProxy
from guis import summonFriendInviteFriend
from guis import summonFriendInviteRecomme
from guis import summonFriendInviteActivity
from callbackHelper import Functor
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
INVITE_SHOP_ID = 308
TAB_MAX_COUNT = 6
TABLE_BTN_NAME_INVITE = 'inviteBtn'
TABLE_BTN_NAME_FRIEND = 'friendBtn'
TABLE_BTN_NAME_RECOMME = 'recommeBtn'
TABLE_BTN_NAME_ACTIVITY = 'activityBtn'
m_tTabBtnDict = {TABLE_BTN_NAME_INVITE: 'inviteMc',
 TABLE_BTN_NAME_FRIEND: 'friendMc',
 TABLE_BTN_NAME_RECOMME: 'recommeMc',
 TABLE_BTN_NAME_ACTIVITY: 'activityMc'}

class SummonFriendInviteV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonFriendInviteV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectTabBtnName = ''
        self.tabBtnList = []
        self.firstShow = True
        self.friendProxy = summonFriendInviteFriend.SummonFriendInviteFriend(self)
        self.recommeProxy = summonFriendInviteRecomme.SummonFriendInviteRecomme(self)
        self.activityProxy = summonFriendInviteActivity.SummonFriendInviteActivity(self)
        self.subProxys = {TABLE_BTN_NAME_INVITE: self,
         TABLE_BTN_NAME_FRIEND: self.friendProxy,
         TABLE_BTN_NAME_RECOMME: self.recommeProxy,
         TABLE_BTN_NAME_ACTIVITY: self.activityProxy}

    def reset(self):
        self.selectTabBtnName = ''
        self.tabBtnList = []

    def unRegisterPanel(self):
        self.friendProxy.hideWidget()
        self.recommeProxy.hideWidget()
        self.activityProxy.hideWidget()
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.tabBtnList = []
        for i, btnName in enumerate(m_tTabBtnDict):
            tabBtn = self.widget.invitePanel.getChildByName(btnName)
            tabBtn.removeEventListener(events.BUTTON_CLICK, self.handleTabBtnClick)
            if tabBtn.name == TABLE_BTN_NAME_ACTIVITY:
                if self.enableActivity():
                    self.tabBtnList.append(tabBtn)
                    tabBtn.visible = True
                else:
                    tabBtn.visible = False
            elif tabBtn.name == TABLE_BTN_NAME_RECOMME:
                if self.enableMyInvitor():
                    self.tabBtnList.append(tabBtn)
                    tabBtn.visible = True
                else:
                    tabBtn.visible = False
            else:
                self.tabBtnList.append(tabBtn)
            if tabBtn.visible and not self.selectTabBtnName:
                self.selectTabBtnName = btnName
            tabBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)

        self.refreshTabBtns()

    def refreshTabBtns(self):
        tabCount = len(self.tabBtnList)
        for i in range(tabCount):
            tabBtn = self.tabBtnList[i]
            tabBtn.x = 102 * i
            tabBtn.focusable = False

    def enableActivity(self):
        enable = gameglobal.rds.configData.get('enableFriendInviteActivity', False)
        return enable

    def enableMyInvitor(self):
        p = BigWorld.player()
        playerLv = p.lv
        limitLv = SCD.data.get('summonFriendInvitedLimitLv', 20)
        return playerLv <= limitLv

    def refreshInfo(self):
        if not self.widget:
            return
        self.getSelectedSubProxy().showWidget()

    def getSelectedSubProxy(self):
        return self.subProxys.get(self.selectTabBtnName)

    def handleTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        btnName = e.currentTarget.name
        self.setTabSelected(btnName)

    def setTabSelected(self, btnName):
        if btnName != self.selectTabBtnName:
            self.selectTabBtnName = btnName
            subProxy = self.subProxys.get(btnName)
            if subProxy:
                subProxy.showWidget()

    def showWidget(self):
        self.updateTabBtnState()

    def updateTabBtnState(self):
        for i, btnName in enumerate(m_tTabBtnDict):
            btnMc = self.widget.invitePanel.getChildByName(btnName)
            panelMc = self.widget.invitePanel.getChildByName(m_tTabBtnDict[btnName])
            if btnName == self.selectTabBtnName:
                btnMc.selected = True
                if panelMc:
                    panelMc.visible = True
                    self.updateSelectTabMc(panelMc)
            else:
                btnMc.selected = False
                if panelMc:
                    panelMc.visible = False

    def updateSelectTabMc(self, panelMc):
        if panelMc.name == 'inviteMc':
            self.refreshWidget()
        elif panelMc.name == 'friendMc':
            self.friendProxy.refreshWidget()
        elif panelMc.name == 'recommeMc':
            self.recommeProxy.refreshWidget()
        else:
            self.activityProxy.refreshWidget()

    def refreshWidget(self):
        self.widget.invitePanel.inviteMc.myInviteMc.confirmCopyWeb.addEventListener(events.MOUSE_CLICK, self.onCopyWebToClipBoard, False, 0, True)
        self.refreshInvite()

    def refreshInvite(self):
        if not self.widget:
            return
        p = BigWorld.player()
        inviteMc = self.widget.invitePanel.inviteMc
        if SCD.data.get('friendInviterLv', 40) > p.lv:
            p.showGameMsg(GMDD.data.INVITE_FRIEND_LV_WRONG, ())
            inviteMc.myInviteMc.visible = False
            inviteMc.noneInviteDesc.visible = True
            return
        if not getattr(BigWorld.player(), 'friendInviteVerifyCode', ''):
            p.cell.genFriendInviteVerifyCode()
            return
        inviteMc.myInviteMc.visible = True
        inviteMc.noneInviteDesc.visible = False
        data = self.getIWantSummonData()
        inviteMc.myInviteMc.ruleWeb.htmlText = data['webRule']
        inviteMc.myInviteMc.qrCodeRule.htmlText = data['QRRule']
        inviteMc.myInviteMc.qrcode.fitSize = True
        inviteMc.myInviteMc.qrcode.loadImageByBase64(data['QRCode'])

    def getIWantSummonData(self):
        data = {}
        data['webRule'] = uiUtils.getTextFromGMD(GMDD.data.WEB_SUMMON_RULE, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_195)
        data['myCode'] = getattr(BigWorld.player(), 'friendInviteVerifyCode', '')
        data['webUrl'] = SCD.data.get('Summon_Friend_Web_addr', 'http://tianyu.163.com/?=%s') % data['myCode']
        data['qrUrl'] = SCD.data.get('Summon_Friend_QR_addr', 'http://tianyu.163.com/?=%s') % data['myCode']
        data['QRRule'] = uiUtils.getTextFromGMD(GMDD.data.QR_SUMMON_RULE, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_199)
        codeMaker = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=2, border=1)
        codeMaker.add_data(data['qrUrl'])
        codeMaker.make(fit=True)
        img = codeMaker.make_image()
        pngUrl = img.convert('RGB').tostring('jpeg', 'RGB', 90)
        data['QRCode'] = base64.encodestring(pngUrl)
        return data

    @ui.callFilter(1, True)
    def onCopyWebToClipBoard(self, *args):
        p = BigWorld.player()
        myCode = getattr(p, 'friendInviteVerifyCode', '')
        if myCode:
            if BigWorld.isPublishedVersion():
                webUrl = SCD.data.get('Summon_Friend_Web_addr', 'http://tianyu.163.com/?=%s') % myCode
            else:
                webUrl = 'http://hd-test-qc.tianyu.163.com/2015/friend?code=%s' % myCode
            BigWorld.setClipBoardText(webUrl)
            msg = uiUtils.getTextFromGMD(GMDD.data.COPY_URL_SUCCESS, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_221)
            gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def showMessageBox(self):
        if not gameglobal.rds.configData.get('enableSummonFriendV2', False):
            if not gameglobal.rds.configData.get('enableInvitePoint', False):
                gameglobal.rds.ui.summonFriend.showMessageBox()
            else:
                gameglobal.rds.ui.summonFriendNew.showMessageBox()
            return
        if self.firstShow:
            self.firstShow = False
        else:
            return
        p = BigWorld.player()
        inviteId = 0
        summedData = self.friendProxy.getSummedPlayersData()
        canShow = True
        if BigWorld.player().lv > SCD.data.get('friendInviteeLv') or summedData.get('totalCount', 0) > 0:
            canShow = False
        if canShow:
            for fid in p.friendInviteInfo:
                if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                    inviteId = fid

            if not inviteId:
                return
            MBButton = messageBoxProxy.MBButton
            title = uiUtils.getTextFromGMD(GMDD.data.BIND_HINT_TITLE, gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_252)
            msg = uiUtils.getTextFromGMD(GMDD.data.BIND_HINT_MESSAGEBOX, gameStrings.TEXT_SUMMONFRIENDINVITERECOMME_138) % p.friendInviteInfo[inviteId].get('playerName', '')
            buttons = [MBButton(gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_254, Functor(self.sendConfirmBind, ''), fastKey=keys.KEY_Y), MBButton(gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_254_1, fastKey=keys.KEY_N), MBButton(gameStrings.TEXT_SUMMONFRIENDINVITEV2PROXY_254_2, self.onKnowSummon)]
            gameglobal.rds.ui.messageBox.show(True, title, msg, buttons)

    def sendConfirmBind(self, code):
        p = BigWorld.player()
        if not code:
            if not p.friendInviterGbId:
                inviteId = 0
                for fid in p.friendInviteInfo:
                    if p.friendInviteInfo[fid].get('status') == gametypes.FRIEND_INVITE_STATUS_PRE_INVITER:
                        inviteId = fid
                        break

                if inviteId:
                    p.base.invitedFriendByGbId(inviteId)
            else:
                return
        p.base.invitedFriendByVerifyCode(code)

    def onKnowSummon(self):
        self.setTabSelected(TABLE_BTN_NAME_RECOMME)

    def setBtnTabName(self, btnName):
        if not btnName:
            return
        if self.widget:
            ASUtils.DispatchButtonEvent(getattr(self.widget.invitePanel, btnName))
        else:
            self.selectTabBtnName = btnName
