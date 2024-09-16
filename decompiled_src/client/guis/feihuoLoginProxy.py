#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/feihuoLoginProxy.o
from gamestrings import gameStrings
import urlparse
import BigWorld
from Scaleform import GfxValue
CEFModule = None
try:
    import CEFManager as CEFModule
except:
    CEFModule = None

import uiConst
import events
import ui
import clientcom
import gameglobal
import keys
import netWork
from gameStrings import gameStrings
import cefUIManager
from helpers import CEFControl
from uiProxy import UIProxy
from guis import innerIEProxy
from callbackHelper import Functor
from guis import uiUtils
from ui import gbk2unicode
from appSetting import Obj as AppSettings
from cdata import game_msg_def_data as GMDD

class FeihuoLoginProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FeihuoLoginProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickReturn': self.onClickReturn,
         'resetPosition': self.resetPosition}
        self.reset()
        self.webUI = None
        self.loginInfo = None
        self.width = 391
        self.height = 265
        self.swfPath = 'gui/widgets/FeihuoLogin' + uiAdapter.getUIExt()
        self.insName = 'FeiHuoWeb'
        self.realUrl = False
        self.loginSucc = False
        self.addEvent(events.EVENT_INNER_IE_HIDE, self.resetVisible, isGlobal=True)
        if clientcom.enalbePreOpenCEF():
            CEFControl.openCEFProgress()

    def show(self, loginType = uiConst.LOGIN_TYPE_FEIHUO):
        self.loginType = loginType
        gameglobal.rds.ui.loginWin.isQRCodeShow = False
        self.loginInfo = self.getLoginInfo(loginType)
        if not self.loginInfo:
            return
        if not CEFModule:
            return
        if not CEFModule.isCefProcessRunning():
            swShow = gameglobal.SW_HIDE if BigWorld.isPublishedVersion() else gameglobal.SW_SHOW
            CEFModule.openCefProcess(gameglobal.CEF_PROCESS_NAME, self.width, self.height, swShow)
        if not cefUIManager.getInstance().registerCefUI(uiConst.WIDGET_FEIHUO_LOGIN2, closeFunc=self.hide, forceOpen=True):
            return
        if not self.mediator:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FEIHUO_LOGIN2)
        else:
            self.startPlay()

    def getOffset(self):
        widget = self.mediator.Invoke('getWidget')
        widgetX = widget.GetMember('x').GetNumber()
        widgetY = widget.GetMember('y').GetNumber()
        iconX = widget.GetMember('picture').GetMember('x').GetNumber()
        iconY = widget.GetMember('picture').GetMember('y').GetNumber()
        scaleX, scaleY = self.getWidgetScale()
        return (int(iconX + widgetX * scaleX), int(iconY + widgetY * scaleY))

    def startPlay(self, refresh = True):
        CEFModule.setConnBindedCallback(self.connectionBindedCallback)
        CEFModule.setTextureChangeCallback(self.textureChangeCallback)
        self.refreshDrawToFlash()
        self.oldX, self.oldY = self.getOffset()
        CEFModule.initImgBuff()
        CEFModule.setPosition(self.oldX, self.oldY)
        CEFModule.resize(self.width, self.height)
        CEFModule.setVisible(True)
        if self.loginInfo.urlPath == uiConst.SHUNWANG_WEB_URL:
            CEFModule.setAlphaColor(16777215)
        else:
            CEFModule.setAlphaColor(-1)
        if refresh:
            CEFModule.loadURL(self.loginInfo.urlPath)
        CEFModule.setCefRequestCallback(self.handleCEFRequest)

    def handleCEFRequest(self, urlPath, requestLen):
        if self.ulrInDomains(getattr(self.loginInfo, 'redirctDomains', []), urlPath):
            if gameglobal.rds.lastKey != keys.KEY_BACKSPACE:
                if not self.uiAdapter.innerIE.mediator:
                    self.uiAdapter.innerIE.show(urlPath, enableKeyEvent=True, code=uiConst.IE_NOLIMIT_TRANSFER, width=700, height=406, enableGoBack=True, skinType=uiConst.IE_SKIN_TYPE_ONLY_FRAME, urlChangeCallback=self.handleCEFRequest)
                self.setVisible(False)
            else:
                CEFModule.loadURL(self.loginInfo.urlPath)
        elif not self.ulrInDomains(self.loginInfo.domains, urlPath) and self.loginInfo.urlPath != urlPath and urlPath.find(self.loginInfo.resetPwdKeyWorld) == -1:
            if 'reg.163.com/?error' in urlPath:
                self.uiAdapter.messageBox.showAlertBox(uiUtils.getTextFromGMD(GMDD.data.LOGIN_ACCOUNT_IS_LOCKED))
                CEFModule.loadURL(self.loginInfo.urlPath)
        elif self.loginInfo.loginHost and urlPath.find(self.loginInfo.loginHost) != -1:
            self.setSuccText(gameStrings.TEXT_FEIHUOLOGINPROXY_130)
            BigWorld.callback(0.5, self.loginInfo.realLogin)
            if self.uiAdapter.innerIE.mediator:
                self.loginSucc = True
                self.uiAdapter.innerIE.setVisible(False)
                BigWorld.callback(1, self.uiAdapter.innerIE.hide)
        elif not self.realUrl and urlPath.find('oauth2.feihuo.com') != -1:
            suffix = self.getSuffix()
            if suffix:
                newSuffix = suffix.replace('&amp;', '&')
                newPath = urlPath + '&' + newSuffix
                self.realUrl = True
                CEFModule.loadURL(newPath)
        elif urlPath.find(self.loginInfo.resetPwdKeyWorld) != -1:
            CEFModule.loadURL(self.loginInfo.urlPath)
            clientcom.openFeedbackUrl(urlPath)
        elif urlPath.find('token') != -1 and self.loginInfo.loginType == uiConst.LOGIN_TYPE_YIYOU:
            try:
                result = urlparse.urlparse(urlPath)
                params = urlparse.parse_qs(result.query, True)
                self.loginInfo.yiyouUID = params.get('uid', [''])[0]
                self.loginInfo.yiyouToken = params['token'][0]
                self.loginInfo.realLogin()
                self.uiAdapter.innerIE.setVisible(False)
                self.setSuccText(gameStrings.TEXT_FEIHUOLOGINPROXY_130)
                if self.uiAdapter.innerIE.mediator:
                    BigWorld.callback(1, self.uiAdapter.innerIE.hide)
            except:
                CEFModule.loadURL(self.loginInfo.urlPath)

    def refreshDrawToFlash(self):
        CEFModule.drawToFlash(self.swfPath, self.insName, 0, 0, self.width, self.height)

    def textureChangeCallback(self, width, height):
        self.refreshDrawToFlash()

    def connectionBindedCallback(self, bind):
        CEFModule.loadURL(self.loginInfo.urlPath)
        CEFModule.resize(self.width, self.height)
        self.refreshDrawToFlash()

    def getWidgetScale(self):
        widget = self.mediator.Invoke('getWidget')
        scaleX = widget.GetMember('scaleX').GetNumber()
        scaleY = widget.GetMember('scaleY').GetNumber()
        return (scaleX, scaleY)

    def resetPosition(self, *arg):
        x = int(arg[3][0].GetNumber())
        y = int(arg[3][1].GetNumber())
        if self.mediator:
            CEFModule.setPosition(x, y)
            self.oldX = x
            self.oldY = y
            scale = CEFControl.getDPIScale()
            scaleX, scaleY = self.getWidgetScale()
            CEFModule.setScale(scaleX / scale, scaleY / scale)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FEIHUO_LOGIN2)

    def onClickReturn(self, *arg):
        self.feihuoLoginHide(isShowLoginWin=True)

    def feihuoLoginHide(self, isShowLoginWin = True):
        if not self.mediator:
            return
        self.hide()
        if isShowLoginWin:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LOGIN_WIN)
            gameglobal.rds.logLoginState = gameglobal.GAME_NTES_LOGIN
            if self.loginInfo.loginType in [uiConst.LOGIN_TYPE_FEIHUO, uiConst.LOGIN_TYPE_YIYOU, uiConst.LOGIN_TYPE_SHUNWANG]:
                netWork.sendInfoForLianYun(gameglobal.rds.logLoginState)

    def hide(self, destroy = True):
        self.setVisible(False)
        super(FeihuoLoginProxy, self).hide(destroy)

    def onURLChange(self, urlPath):
        if self.ulrInDomains(getattr(self.loginInfo, 'redirctDomains', []), urlPath):
            if gameglobal.rds.lastKey != keys.KEY_BACKSPACE:
                if not self.uiAdapter.innerIE.mediator:
                    self.uiAdapter.innerIE.show(urlPath, enableKeyEvent=True, code=uiConst.IE_NOLIMIT_TRANSFER, width=700, height=406, enableGoBack=True, skinType=uiConst.IE_SKIN_TYPE_ONLY_FRAME, urlChangeCallback=self.onURLChange)
                self.setVisible(False)
            else:
                self.loadUrl(self.loginInfo.urlPath)
        elif not self.ulrInDomains(self.loginInfo.domains, urlPath) and self.loginInfo.urlPath != urlPath and urlPath.find(self.loginInfo.resetPwdKeyWorld) == -1:
            if 'reg.163.com/?error' in urlPath:
                self.uiAdapter.messageBox.showAlertBox(uiUtils.getTextFromGMD(GMDD.data.LOGIN_ACCOUNT_IS_LOCKED))
            self.loadUrl(self.loginInfo.urlPath)
        elif self.loginInfo.loginHost and urlPath.find(self.loginInfo.loginHost) != -1:
            self.setSuccText(gameStrings.TEXT_FEIHUOLOGINPROXY_130)
            BigWorld.callback(0.5, self.loginInfo.realLogin)
            if self.uiAdapter.innerIE.mediator:
                self.uiAdapter.innerIE.hide()
        elif not self.realUrl and urlPath.find('oauth2.feihuo.com') != -1:
            suffix = self.getSuffix()
            if suffix:
                newSuffix = suffix.replace('&amp;', '&')
                newPath = urlPath + '&' + newSuffix
                self.realUrl = True
                self.webUI.loadURL(newPath)
        elif urlPath.find(self.loginInfo.resetPwdKeyWorld) != -1:
            self.webUI.loadURL(self.loginInfo.urlPath)
            clientcom.openFeedbackUrl(urlPath)
        elif urlPath.find('token') != -1 and self.loginInfo.loginType == uiConst.LOGIN_TYPE_YIYOU:
            try:
                result = urlparse.urlparse(urlPath)
                params = urlparse.parse_qs(result.query, True)
                self.loginInfo.yiyouUID = params.get('uid', [''])[0]
                self.loginInfo.yiyouToken = params['token'][0]
                self.loginInfo.realLogin()
                self.setSuccText(gameStrings.TEXT_FEIHUOLOGINPROXY_130)
                if self.uiAdapter.innerIE.mediator:
                    self.uiAdapter.innerIE.hide()
            except:
                self.webUI.loadURL(self.loginInfo.urlPath)

    def ulrInDomains(self, domains, url):
        if domains:
            for domain in domains:
                if url.find(domain) != -1:
                    return True

        return False

    def getSuffix(self):
        ret = AppSettings.get(keys.SET_FEIHUO_SUFFIX, '')
        return ret

    def setSuccText(self, text):
        if self.mediator:
            self.loginSucc = True
            self.mediator.Invoke('setSuccText', GfxValue(gbk2unicode(text)))

    def loadUrl(self, url):
        CEFModule.loadURL(url)

    def reset(self):
        self.mediator = None
        self.loginSucc = False

    def clearWidget(self):
        CEFModule.setAlphaColor(-1)
        cefUIManager.getInstance().unregisterCefUI(uiConst.WIDGET_FEIHUO_LOGIN2)
        CEFModule.setVisible(False)
        CEFModule.setPosition(0, 0)
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FEIHUO_LOGIN2)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        self.startPlay()
        if self.loginInfo.loginType == uiConst.LOGIN_TYPE_FEIHUO:
            gameglobal.rds.logLoginState = gameglobal.GAME_FEIHUO_LOGIN
        elif self.loginInfo.loginType == uiConst.LOGIN_TYPE_YIYOU:
            gameglobal.rds.logLoginState = gameglobal.GAME_YIYOU_LOGIN
        elif self.loginInfo.loginType == uiConst.LOGIN_TYPE_SHUNWANG:
            gameglobal.rds.logLoginState = gameglobal.GAME_SHUNWANG_LOADING
        netWork.sendInfoForLianYun(gameglobal.rds.logLoginState)
        initData = {'title': self.loginInfo.title,
         'type': int(bool(gameglobal.rds.enableNewLoginScene))}
        return uiUtils.dict2GfxDict(initData, True)

    def getLoginInfo(self, loginType):
        if loginType == uiConst.LOGIN_TYPE_FEIHUO:
            return FeiHuoLoginInfo(loginType)
        if loginType == uiConst.LOGIN_TYPE_YIYOU:
            return YiYouLoginInfo(loginType)
        if loginType == uiConst.LOGIN_TYPE_SHUNWANG:
            return ShunWangLoginInfo(loginType)

    def setVisible(self, visible):
        if self.mediator:
            self.mediator.Invoke('getWidget').SetVisible(visible)

    def resetVisible(self):
        if not self.loginSucc:
            self.show(self.loginType)
            CEFModule.resize(self.width, self.height)


class FeiHuoLoginInfo(object):

    def __init__(self, loginType):
        self.loginType = loginType
        self.urlPath = uiConst.FEIHUO_WEB_URL
        self.loginHost = 'feihuo.163.com'
        self.resetPwdKeyWorld = 'resetPwd'
        self.title = gameStrings.TEXT_FEIHUOLOGINPROXY_338
        self.domains = ('oauth2.feihuo.com', 'feihuo.163.com', 'qq.com', 'feihuo.com')
        self.redirctDomains = ('graph.qq.com',)

    def realLogin(self):
        gameglobal.rds.loginManager.tryConnectFeihuo()


class YiYouLoginInfo(object):

    def __init__(self, loginType):
        self.loginType = loginType
        self.urlPath = uiConst.YIYOU_WEB_URL
        self.loginHost = None
        self.resetPwdKeyWorld = 'findpwd'
        self.title = gameStrings.TEXT_FEIHUOLOGINPROXY_351
        self.yiyouUID = ''
        self.yiyouToken = ''
        self.domains = ('ylwpk.com', 'pk.yilewan.com')
        self.redirctDomains = ('graph.qq.com', 'weixin.qq.com')

    def realLogin(self):
        gameglobal.rds.loginManager.tryConnectyYiyou()


class ShunWangLoginInfo(object):

    def __init__(self, loginType):
        self.loginType = loginType
        self.urlPath = uiConst.SHUNWANG_WEB_URL
        self.loginHost = 'shunwang.163.com'
        self.resetPwdKeyWorld = 'pwdFind_all_front'
        self.title = gameStrings.TEXT_FEIHUOLOGINPROXY_366
        self.domains = ('ty.swjoy.com', 'shunwang.163.com')

    def realLogin(self):
        gameglobal.rds.loginManager.tryConnectFeihuo()
