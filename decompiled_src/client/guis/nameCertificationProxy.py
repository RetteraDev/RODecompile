#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/nameCertificationProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from guis.asObject import ASObject
from guis.asObject import ASUtils
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import sys_config_data as SCD

class NameCertificationProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NameCertificationProxy, self).__init__(uiAdapter)
        self.widget = None
        self.login = None
        self.reset()

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_NAME_CERTIFICATION:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NAME_CERTIFICATION)

    def show(self, login):
        self.login = login
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_NAME_CERTIFICATION)

    def initUI(self):
        self.widget.gotoConfirm.addEventListener(events.MOUSE_CLICK, self.handleGotoConfirmBtnClick, False, 0, True)
        self.widget.visitorMode.addEventListener(events.MOUSE_CLICK, self.handleVisitorModeBtnClick, False, 0, True)
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleOutBtnClick, False, 0, True)
        self.widget.hintTxt.htmlText = gameStrings.NAME_CERTIFICATION_HINT_TXT
        self.widget.upHint.htmlText = gameStrings.NAME_CERTIFICATION_UP_HINT_TXT
        self.widget.downHint.htmlText = gameStrings.NAME_CERTIFICATION_DOWN_HINT_TXT

    def handleOutBtnClick(self, *args):
        if self.login:
            self.login.gotoLoginPage()
        self.hide()

    def handleVisitorModeBtnClick(self, *args):
        seconds = SCD.data.get('VISITOR_INTERVAL_TIME', 3600)
        minute = seconds // 60
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.NAME_CERTIFICATION_VISITOR_MODE_HINT % minute, yesCallback=self.realVisitorMode)

    def realVisitorMode(self):
        self.login.logonClient.finishRealNameReq()
        self.hide()

    def handleGotoConfirmBtnClick(self, *args):
        url = SCD.data.get('NAME_CERTIFICATION_URL', 'http://reg.163.com')
        loginInfo = gameglobal.rds.ui.feihuoLogin.loginInfo
        if loginInfo:
            if loginInfo.loginType == uiConst.LOGIN_TYPE_SHUNWANG:
                url = SCD.data.get('SHUNWANG_NAME_CERTIFICATION_URL', 'https://passport.kedou.com/front/noLogin/login_front.jsp?')
            elif loginInfo.loginType == uiConst.LOGIN_TYPE_FEIHUO:
                url = SCD.data.get('FEIHUO_NAME_CERTIFICATION_URL', url)
        BigWorld.openUrl(url)
