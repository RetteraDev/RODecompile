#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbWalletSubWndProxy.o
import BigWorld
from guis import ui
import gameglobal
import uiConst
import base64
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import events
from guis import hotkeyProxy
from guis.asObject import ASUtils
from guis import hotkey as HK
from guis.asObject import ASObject
from guis.asObject import FocusManager
from guis import ftbWalletHelper
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
WND_TYPE_NONE = -1
WND_TYPE_CREATE = 0
WND_TYPE_SET_PASSWORD = 1
WND_TYPE_PASSWORLD = 2
WND_TYPE_OPEN = 3
WND_TYPE_REST_PASSWORLD0 = 4
WND_TYPE_REST_PASSWORLD1 = 5
WND_TYPE_PRIVATEKEY_PASSWORLD = 6
WND_TYPE_BINDKEY_PASSWORLD = 7
WND_TYPE_ACTIVITY_PASSWORLD = 8
WND_TYPE_FORGET_PASSWORLD = 9
PASSWD_MAX_CHAR = 6

class FtbWalletSubWndProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FtbWalletSubWndProxy, self).__init__(uiAdapter)
        self.widget = None
        self.wndType = WND_TYPE_NONE
        self.confirmCallback = None
        self.cancelCallBack = None
        self.tempPass = ''
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FTB_WALLET_SUBWND, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FTB_WALLET_SUBWND:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FTB_WALLET_SUBWND)

    def showCreateWnd(self):
        self.show(WND_TYPE_CREATE, lambda : gameglobal.rds.ui.ftbWalletBackUp.show())

    def showSetPassWnd(self):
        self.show(WND_TYPE_SET_PASSWORD)

    def showOpenWnd(self):
        self.show(WND_TYPE_OPEN, self.showPassWnd)

    def showPassWnd(self):
        self.show(WND_TYPE_PASSWORLD)

    def showResetPassWndState0(self):
        self.show(WND_TYPE_REST_PASSWORLD0, self.showResetPassWndState1)

    def showResetPassWndState1(self):
        self.show(WND_TYPE_REST_PASSWORLD1)

    def showViewPrivateKeyWnd(self, callback = None):
        self.show(WND_TYPE_PRIVATEKEY_PASSWORLD, callback)

    def showViewBindCodeWnd(self, callback = None):
        self.show(WND_TYPE_BINDKEY_PASSWORLD, callback)

    def showActivityPasswordWnd(self, callback = None):
        self.show(WND_TYPE_ACTIVITY_PASSWORLD, callback)

    @ui.checkInventoryLock()
    def showForgetPasswordWnd(self):
        self.show(WND_TYPE_FORGET_PASSWORLD, None)

    def show(self, wndType = WND_TYPE_CREATE, confirmCallback = None, cancelCallback = None):
        if wndType < 0:
            return
        self.hide()
        self.wndType = wndType
        self.confirmCallback = confirmCallback
        self.cancelCallBack = cancelCallback
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FTB_WALLET_SUBWND)

    def onConfirmBtnClick(self, *args):
        if self.wndType == WND_TYPE_PASSWORLD:
            ftbWalletHelper.getInstance().queryPrivateKey(self.widget.msgBox.passInput.text, self.onCheckOpenCallback, WND_TYPE_PASSWORLD)
            return
        if self.wndType == WND_TYPE_PRIVATEKEY_PASSWORLD:
            ftbWalletHelper.getInstance().queryPrivateKey(self.widget.msgBox.passInput.text, self.onQueryKeyCallBack, WND_TYPE_PRIVATEKEY_PASSWORLD)
            return
        if self.wndType == WND_TYPE_BINDKEY_PASSWORLD:
            ftbWalletHelper.getInstance().queryPrivateKey(self.widget.msgBox.passInput.text, self.onQueryKeyCallBack, WND_TYPE_BINDKEY_PASSWORLD)
            return
        if self.wndType == WND_TYPE_REST_PASSWORLD0:
            passwd = self.widget.msgBox.passInput.text
            ftbWalletHelper.getInstance().checkPassword(passwd, Functor(self.onCheckResetPasswdCallback, passwd), WND_TYPE_REST_PASSWORLD0)
            return
        if self.wndType == WND_TYPE_REST_PASSWORLD1:
            p = BigWorld.player()
            if len(self.widget.msgBox.passInput.text) != 6:
                p.showGameMsg(GMDD.data.FTB_WALLET_PASSWD_NOT_NONE, ())
            elif self.widget.msgBox.passInput.text != self.widget.msgBox.confirmInput.text:
                p.showGameMsg(GMDD.data.FTB_WALLET_PASSWD_NOT_SAME, ())
            else:
                p.base.modifyFtbWalletPasswd(self.tempPass, self.widget.msgBox.passInput.text)
            return
        if self.wndType == WND_TYPE_SET_PASSWORD:
            p = BigWorld.player()
            if len(self.widget.msgBox.passInput.text) != 6:
                p.showGameMsg(GMDD.data.FTB_WALLET_PASSWD_NOT_NONE, ())
            elif self.widget.msgBox.passInput.text != self.widget.msgBox.confirmInput.text:
                p.showGameMsg(GMDD.data.FTB_WALLET_PASSWD_NOT_SAME, ())
            else:
                p.base.createFtbWallet(self.widget.msgBox.passInput.text)
            return
        if self.wndType == WND_TYPE_ACTIVITY_PASSWORLD:
            p = BigWorld.player()
            p.base.doFtbUserApiAuth(base64.b64encode(self.widget.msgBox.passInput.text), '')
            self.hide()
        else:
            if self.wndType == WND_TYPE_FORGET_PASSWORLD:
                p = BigWorld.player()
                if len(self.widget.msgBox.passInput.text) != 6:
                    p.showGameMsg(GMDD.data.FTB_WALLET_PASSWD_NOT_NONE, ())
                elif self.widget.msgBox.passInput.text != self.widget.msgBox.confirmInput.text:
                    p.showGameMsg(GMDD.data.FTB_WALLET_PASSWD_NOT_SAME, ())
                else:
                    p.base.resetFtbWalletPasswd(self.widget.msgBox.passInput.text, p.cipherOfPerson)
                    self.hide()
                return
            self.hide()
            if self.confirmCallback:
                self.confirmCallback()

    def onCreateFTBWallet(self):
        if self.wndType == WND_TYPE_SET_PASSWORD:
            self.hide()

    def onCheckOpenCallback(self, info):
        self.hide()
        gameglobal.rds.ui.ftbWalletBackUp.show()

    def onCheckResetPasswdCallback(self, passwd, info):
        if info == True:
            self.hide()
            self.tempPass = passwd
            if self.confirmCallback:
                self.confirmCallback()
        elif self.widget.msgBox.infoText:
            self.widget.msgBox.infoText.htmlText = gameStrings.FTB_WALLET_FALSE_PASS

    def onModifyPasswdCallback(self, isOk):
        if isOk:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.FTB_WALLET_CHANGE_PASSWD,))
            gameglobal.rds.ui.ftbWallet.resetPrivateInfo()
            self.hide()
            if self.confirmCallback:
                self.confirmCallback()

    def onQueryKeyCallBack(self, info):
        self.hide()
        if self.confirmCallback:
            self.confirmCallback()

    def onCancelBtnClick(self, *args):
        self.hide()
        if self.cancelCallBack:
            self.cancelCallBack()

    def getWndInfoMap(self, wndType):
        wndFuncMap = {WND_TYPE_CREATE: (0, self.refreshCreateWnd),
         WND_TYPE_SET_PASSWORD: (1, self.refreshSetPassWnd),
         WND_TYPE_PASSWORLD: (2, self.refreshPassWnd),
         WND_TYPE_OPEN: (3, self.refreshOpenWnd),
         WND_TYPE_REST_PASSWORLD0: (4, self.refreshReset0Wnd),
         WND_TYPE_REST_PASSWORLD1: (5, self.refreshReset1Wnd),
         WND_TYPE_PRIVATEKEY_PASSWORLD: (2, self.refreshViewPrivateKeyWnd),
         WND_TYPE_BINDKEY_PASSWORLD: (2, self.refreshViewBindKeyWnd),
         WND_TYPE_ACTIVITY_PASSWORLD: (2, self.refreshViewActivityPasswd),
         WND_TYPE_FORGET_PASSWORLD: (6, self.refreshForgetWnd)}
        return wndFuncMap.get(wndType, None)

    def refreshCreateWnd(self, msgBox):
        pass

    def refreshSetPassWnd(self, msgBox):
        self.setInputAsHintInput(msgBox.passInput)
        self.setInputAsHintInput(msgBox.confirmInput)
        FocusManager.setFocus(msgBox.passInput)

    def refreshPassWnd(self, msgBox):
        msgBox.txtTitle.text = gameStrings.FTB_WALLET_OPEN
        msgBox.inputTitle.text = gameStrings.FTB_WALLET_OPEN_DESC
        self.setInputAsHintInput(msgBox.passInput)
        msgBox.infoText.text = ''

    def refreshViewPrivateKeyWnd(self, msgBox):
        msgBox.txtTitle.text = gameStrings.FTB_WALLET_VIEW_PRIVATEKEY
        msgBox.inputTitle.text = gameStrings.FTB_WALLET_VIEW_PRIVATEKEY_DESC
        self.setInputAsHintInput(msgBox.passInput)
        msgBox.infoText.text = ''

    def refreshViewBindKeyWnd(self, msgBox):
        msgBox.txtTitle.text = gameStrings.FTB_WALLET_VIEW_BINDKEY
        msgBox.inputTitle.text = gameStrings.FTB_WALLET_VIEW_BINDKEY_DESC
        self.setInputAsHintInput(msgBox.passInput)
        msgBox.infoText.text = ''

    def refreshViewActivityPasswd(self, msgBox):
        msgBox.txtTitle.text = gameStrings.FTB_ACTIVITY_AUTH
        msgBox.inputTitle.text = gameStrings.FTB_ACTIVITY_AUTH_DESC
        self.setInputAsHintInput(msgBox.passInput)
        msgBox.infoText.text = ''

    def refreshOpenWnd(self, msgBox):
        pass

    def refreshReset0Wnd(self, msgBox):
        self.setInputAsHintInput(msgBox.passInput)
        msgBox.infoText.text = ''

    def refreshReset1Wnd(self, msgBox):
        self.setInputAsHintInput(msgBox.passInput)
        self.setInputAsHintInput(msgBox.confirmInput)
        FocusManager.setFocus(msgBox.passInput)

    def refreshForgetWnd(self, msgBox):
        self.setInputAsHintInput(msgBox.passInput)
        self.setInputAsHintInput(msgBox.confirmInput)
        FocusManager.setFocus(msgBox.passInput)

    def setInputAsHintInput(self, inputMc):
        if not inputMc:
            return
        inputMc.textField.restrict = '0-9'
        inputMc.textField.maxChars = PASSWD_MAX_CHAR
        inputMc.addEventListener(events.FOCUS_EVENT_FOCUS_IN, self.onInputFucusIn)
        inputMc.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.onInputFocusOut)
        inputMc.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.onKeyBoardKeyUp)

    def onKeyBoardKeyUp(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == events.KEYBOARD_CODE_TAB:
            if e.currentTarget.name == 'passInput':
                if self.widget.msgBox.getChildByName('confirmInput'):
                    FocusManager.setFocus(self.widget.msgBox.confirmInput)
            elif e.currentTarget.name == 'confirmInput':
                if self.widget.msgBox.getChildByName('passInput'):
                    FocusManager.setFocus(self.widget.msgBox.passInput)

    def handleKeyBoardUp(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == events.KEYBOARD_CODE_ENTER or e.keyCode == events.KEYBOARD_CODE_ENTER:
            self.onConfirmBtnClick()

    def onInputFucusIn(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.displayAsPassword = True

    def onInputFocusOut(self, *args):
        e = ASObject(args[3][0])
        if e.target.text == '':
            e.currentTarget.displayAsPassword = False

    def onForgetPassworldClick(self, *args):
        if gameglobal.rds.configData.get('enableResetFTBPasswd', False):
            self.showForgetPasswordWnd()
        else:
            msg = gameStrings.FTB_WALLET_FORGET_TEXT
            gameglobal.rds.ui.messageBox.showMsgBox(msg, showTitle=gameStrings.FTB_WALLET_FORGET_TITLE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        wndInfo = self.getWndInfoMap(self.wndType)
        if wndInfo:
            gotoFrame = wndInfo[0]
            self.widget.msgBox.gotoAndStop('type%s' % str(gotoFrame))
        confirmBtn = self.widget.msgBox.getChildByName('confirmBtn')
        cancelBtn = self.widget.msgBox.getChildByName('cancelBtn')
        forgetLink = self.widget.msgBox.getChildByName('forgetLink')
        if confirmBtn:
            confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirmBtnClick)
        if cancelBtn:
            cancelBtn.addEventListener(events.BUTTON_CLICK, self.onCancelBtnClick)
        if forgetLink:
            forgetLink.htmlText = gameStrings.FTB_FORGET_PASS
            forgetLink.addEventListener(events.MOUSE_CLICK, self.onForgetPassworldClick)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyBoardUp)
        wndInfo = self.getWndInfoMap(self.wndType)
        if wndInfo:
            refreshFunc = wndInfo[1]
            refreshFunc(self.widget.msgBox)
