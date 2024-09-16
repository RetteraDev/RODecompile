#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/loginWinProxy.o
from gamestrings import gameStrings
import hashlib
import time
import os
import ResMgr
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import game
import uiConst
import gamelog
import utils
import uiUtils
import netWork
import clientcom
import ui
import base64
import const
from uiProxy import UIProxy
from ui import unicode2gbk
from ui import gbk2unicode
from helpers import cgPlayer
from cdata import game_msg_def_data as GMDD
from guis.ui import callFilter
from sfx import screenEffect
DAT_FILE = '../game/user.dat'
UPDATE_FILE = '../update.ini'

class LoginWinProxy(UIProxy):
    NORMAL_MODE = 0
    QR_MODE = 1

    def __init__(self, uiAdapter):
        super(LoginWinProxy, self).__init__(uiAdapter)
        self.modelMap = {'EnterOnline': self.onEnterOnline,
         'EnterOffline': self.onEnterOffline,
         'EnterArtOffline': self.onEnterArtOffline,
         'EnterVideo': self.onEnterVideo,
         'registerLoginWin': self.onRegisterLoginWin,
         'isRemember': self.onIsRemember,
         'isGtLogin': self.onIsGtLogin,
         'isGtAutoLogin': self.onIsGtAutoLogin,
         'getAccAndPwd': self.onGetAccAndPwd,
         'openIme': self.onOpenIme,
         'getCapsLight': self.getCapsLight,
         'quitGameClick': self.onQuitGameClick,
         'findPassword': self.onFindPassword,
         'registerAccount': self.onRegisterAccount,
         'getAccountNames': self.onGetAccountNames,
         'EnterXrjm': self.onEnterXrjm,
         'getQRContent': self.onGetQRContent,
         'getQRLogin': self.onGetQRLogin,
         'setQRLogin': self.setQRLogin,
         'refreshQRCode': self.refreshQRCode,
         'setIsQRState': self.onSetIsQRState,
         'clickFeiHuo': self.onClickFeiHuo}
        self.mc = None
        self.isRemember = True
        self.userName = ''
        self.md5Pwd = ''
        self.lastInputPwd = ''
        self.startTime = 0
        self.isQRCodeLogin = False
        self.loginRecord = []
        self.qrQueryCallBack = None
        self.queryClient = None
        self.cgPlayer = None
        self.isQRCodeShow = False

    def _initData(self):
        if gameglobal.rds.loginAuthType == const.LOGIN_AUTH_RU_GC:
            userName = BigWorld.getCommandArg('-sz_id')
            passwd = BigWorld.getCommandArg('-sz_token')
            isRemember = False
            isGt = True
            isGtAuto = True
            loginRecord = '[]'
            isQRCodeLogin = False
        elif gameglobal.rds.loginAuthType == const.LOGIN_AUTH_EU_GC:
            userName = BigWorld.getCommandArg('-mycom_user_id')
            passwd = BigWorld.getCommandArg('-my_com_code')
            isRemember = False
            isGt = True
            isGtAuto = True
            loginRecord = '[]'
            isQRCodeLogin = False
        else:
            try:
                userName, passwd, isRemember, isGt, isGtAuto, loginRecord, isQRCodeLogin = self.readUserInfo().split('	')
                BigWorld.setDmpPlayerInfo('', userName)
                isRemember = isRemember == 'True'
                isGt = isGt == 'True'
                isGtAuto = isGtAuto == 'True'
                isQRCodeLogin = isQRCodeLogin == 'True'
            except:
                try:
                    userName, passwd, isRemember, isGt, isGtAuto, loginRecord = self.readUserInfo().split('	')
                    isRemember = isRemember == 'True'
                    isGt = isGt == 'True'
                    isGtAuto = isGtAuto == 'True'
                    isQRCodeLogin = False
                except:
                    userName = ''
                    passwd = ''
                    isRemember = False
                    isGt = False
                    isGtAuto = True
                    loginRecord = '[]'
                    isQRCodeLogin = False

        self.userName = userName
        self.md5Pwd = passwd
        self.lastInputPwd = passwd
        self.setRememberStatus(isRemember)
        loginRecord = loginRecord.replace('[', '').replace(']', '').replace("\'", '')
        self.loginRecord = loginRecord.replace(' ', '').split(',')
        self.isQRCodeLogin = isQRCodeLogin
        gameglobal.rds.loginManager.autoLogin = isGtAuto

    @ui.callFilter(1, False)
    def onSetIsQRState(self, *args):
        ret = args[3][0].GetBool()
        self.isQRCodeShow = False
        if ret == False:
            mod = self.NORMAL_MODE
            gameglobal.rds.loginManager.tryDisconnect()
        else:
            mod = self.QR_MODE
            self.isQRCodeShow = True
        self.mc.Invoke('selectType', GfxValue(mod))

    def readUserInfo(self):
        text = None
        try:
            f = open(DAT_FILE, 'rb')
            text = f.read()
            f.close()
        except:
            f = None

        return text

    def onGetQRLogin(self, *args):
        return GfxValue(self.isQRCodeLogin)

    @ui.callFilter(2, False)
    def refreshQRCode(self, *args):
        self.tryQuery()

    def tryQuery(self):
        self.mc.Invoke('setQRCode', GfxValue(gbk2unicode('')))
        gameglobal.rds.loginManager.tryDisconnect()
        gameglobal.rds.loginManager.tryConnectQRCode()

    def onGetQRContent(self, *args):
        hint = uiUtils.getTextFromGMD(GMDD.data.LOGIN_QR_CONTENT)
        return GfxValue(gbk2unicode(hint))

    def setQRLogin(self, *args):
        ret = args[3][0].GetBool()
        self.isQRCodeLogin = ret
        self.writeUserInfo()

    def setQRCode(self, codeBuff):
        buffer = base64.encodestring(codeBuff)
        self.mc.Invoke('setQRCode', GfxValue(buffer))

    def writeUserInfo(self):
        userName = self.userName.replace('\n', '').strip()
        for suffix in gametypes.ACCOUNT_TYPE_SUFFIX_DICT.iterkeys():
            if userName.find(suffix) != -1:
                return

        if userName.count('@') > 1:
            userName = userName[:userName.rfind('@')]
        passwd = ''
        isRemember = self.isRemember
        isGt = gameglobal.rds.loginManager.isGtLogonMode()
        isGtAuto = gameglobal.rds.loginManager.autoLogin
        loginRecord = str(self.loginRecord)
        isQRCodeLogin = self.isQRCodeLogin
        if not isRemember:
            userName = ''
        userInfo = '%s	%s	%s	%s	%s	%s	%s' % (userName,
         passwd,
         isRemember,
         isGt,
         isGtAuto,
         loginRecord,
         isQRCodeLogin)
        try:
            f = open(DAT_FILE, 'wb')
            f.write(userInfo)
            f.close()
        except:
            f = None

    def onRegisterLoginWin(self, *arg):
        self.mc = arg[3][0]
        gamelog.debug('b.e.:onRegisterLoginWin', self.mc)
        if BigWorld.isPublishedVersion():
            self.setPublishFunc()
        isFeiHuo = gameglobal.rds.isFeiHuo
        isYiYou = gameglobal.rds.isYiYou
        isShunWang = gameglobal.rds.isShunWang
        initData = {'isLianYun': isShunWang or isFeiHuo,
         'isFeiHuo': isFeiHuo,
         'isYiYou': isYiYou,
         'isShunWang': isShunWang}
        return uiUtils.dict2GfxDict(initData, True)

    def setPublishFunc(self):
        self.mc.Invoke('setPublishFunc')

    def onFindPassword(self, *arg):
        BigWorld.openUrl('http://reg.163.com/getpasswd/RetakePassword.jsp')

    @callFilter(2)
    def onEnterOnline(self, *arg):
        name = arg[3][0].GetString().strip()
        password = arg[3][1].GetString()
        self._onEnterOnline(name, password)

    def _onEnterOnline(self, name, password):
        msg = None
        if not name and not password:
            msg = gameStrings.TEXT_LOGINWINPROXY_236
        elif not name:
            msg = gameStrings.TEXT_LOGINWINPROXY_238
        elif not password:
            msg = gameStrings.TEXT_LOGINWINPROXY_240
        if msg:
            gameglobal.rds.ui.characterDetailAdjust.setMsg(msg)
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TIP, True)
            return
        elif not utils.isValidEmail(name) and not gameglobal.rds.loginAuthType:
            gameglobal.rds.ui.characterDetailAdjust.setMsg(gameStrings.TEXT_LOGINWINPROXY_247)
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TIP, True)
            return
        else:
            self.userName = unicode2gbk(name)
            if password != self.lastInputPwd:
                m = hashlib.md5(password)
                if gameglobal.rds.loginAuthType:
                    self.md5Pwd = password
                else:
                    self.md5Pwd = m.hexdigest()
                self.lastInputPwd = self.md5Pwd
            if gameglobal.rds.loginManager:
                gameglobal.rds.loginManager.reset()
            if gameglobal.rds.GameState == gametypes.GS_CONNECT and not gameglobal.rds.loginManager.isGtLogonMode():
                now = time.time()
                gamelog.debug('hjx connect:', self.startTime, now)
                if now - self.startTime > uiConst.CONNECTINTERVAL:
                    netWork.reSendPwd(self.userName, self.md5Pwd)
                return
            BigWorld.worldDrawEnabled(True)
            if hasattr(BigWorld, 'bigMapEnabled'):
                BigWorld.bigMapEnabled(False)
            if gameglobal.rds.loginManager.isGtLogonMode():
                self.uiAdapter.unLoadWidget(uiConst.WIDGET_LOGIN_WIN)
                gameglobal.rds.loginManager.tryConnect()
            else:
                netWork.initOnline(self.userName)
            userName = self.userName.replace('\n', '').strip()
            if userName.count('@') > 1:
                userName = userName[:userName.rfind('@')]
            if userName not in self.loginRecord:
                self.loginRecord.append(userName)
            gameglobal.rds.sound.playSound(gameglobal.SD_2)
            return

    def showLoginWin(self):
        BigWorld.worldDrawEnabled(True)
        screenEffect.showDarkAngle(1)
        self._initData()
        self.uiAdapter.loadWidget(uiConst.WIDGET_LOGINLOGO)
        self.uiAdapter.loadWidget(uiConst.WIDGET_LOGINLOGOTIPS2)
        self.uiAdapter.loadWidget(uiConst.WIDGET_PLAYTIPS)
        self.uiAdapter.loadWidget(uiConst.WIDGET_SYSTEMTIPS)
        self.uiAdapter.systemSingleTip.show()
        isShowSecrecy = True
        version = '0'
        try:
            if not os.path.isfile(UPDATE_FILE):
                isShowSecrecy = False
            file = open(UPDATE_FILE, 'rb')
            for line in file:
                if line[:7] == 'Version':
                    version = line[8:].strip()
                    break

            file.close()
            sect = ResMgr.openSection('../game/conf.xml')
            if sect:
                lastVersion = sect.readString('version').strip()
                if lastVersion == version:
                    isShowSecrecy = False
        except IOError:
            pass

        if isShowSecrecy:
            self.uiAdapter.secrecy.show(version)
        else:
            self.realShow()
        game.tick()

    def realShow(self):
        if gameglobal.rds.isFeiHuo or gameglobal.rds.isYiYou or gameglobal.rds.isShunWang:
            if gameglobal.rds.isFeiHuo:
                loginType = uiConst.LOGIN_TYPE_FEIHUO
            elif gameglobal.rds.isYiYou:
                loginType = uiConst.LOGIN_TYPE_YIYOU
            elif gameglobal.rds.isShunWang:
                loginType = uiConst.LOGIN_TYPE_SHUNWANG
            gameglobal.rds.ui.feihuoLogin.show(loginType)
        elif gameglobal.rds.loginAuthType == const.LOGIN_AUTH_RU_GC:
            userName = BigWorld.getCommandArg('-sz_id')
            passwd = BigWorld.getCommandArg('-sz_token')
            self._onEnterOnline(userName, passwd)
        elif gameglobal.rds.loginAuthType == const.LOGIN_AUTH_EU_GC:
            userName = BigWorld.getCommandArg('-mycom_user_id')
            passwd = BigWorld.getCommandArg('-my_com_code')
            self._onEnterOnline(userName, passwd)
        else:
            gameglobal.rds.logLoginState = gameglobal.GAME_NTES_LOGIN
            self.uiAdapter.loadWidget(uiConst.WIDGET_LOGIN_WIN, False, True)
            self.uiAdapter.loginWinBottom.show()

    def hide(self, destroy = True):
        unloadWidgetsList = [uiConst.WIDGET_LOGIN_WIN, uiConst.WIDGET_LOGINLOGO, uiConst.WIDGET_LOGINLOGOTIPS2]
        gameglobal.rds.loginScene.unloadWidgets(unloadWidgetsList)
        self.uiAdapter.loginWinBottom.hide()
        self.mc = None
        self.qrQueryCallBack = None
        self.queryClient = None

    def onClickFeiHuo(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LOGIN_WIN)
        btnName = arg[3][0].GetString()
        if btnName == 'feiHuoBtn':
            loginType = uiConst.LOGIN_TYPE_FEIHUO
        elif btnName == 'yiyouBtn':
            loginType = uiConst.LOGIN_TYPE_YIYOU
        elif btnName == 'shunWangBtn':
            loginType = uiConst.LOGIN_TYPE_SHUNWANG
        gameglobal.rds.ui.feihuoLogin.show(loginType)

    def onEnterOffline(self, *arg):
        self.clearEffect()
        self.hide()
        netWork.initOffline()

    def onEnterArtOffline(self, *arg):
        self.clearEffect()
        self.hide()
        gameglobal.rds.loginScene.clearSpace()
        BigWorld.callback(1, self.realInitArtOffline)

    def realInitArtOffline(self):
        gameglobal.rds.loginScene.loadOfflineSpace()
        netWork.initArtOffline()

    def onEnterXrjm(self, *arg):
        self.enterNewXrjm()

    def enterNewXrjm(self):
        self.clearEffect()
        self.hide()
        gameglobal.rds.ui.characterCreate.gotoCharacterSelectZero()

    def clearEffect(self):
        BigWorld.callback(0.2, self._endMovie)

    def _endMovie(self):
        if self.cgPlayer:
            self.cgPlayer.endMovie()
            self.cgPlayer = None

    def onEnterVideo(self, *arg):
        gameglobal.rds.loginScene.clearSpace()
        gameglobal.rds.loginScene.loadSpace()

    def playMovie(self):
        if not self.cgPlayer:
            self.cgPlayer = cgPlayer.CGPlayer()
            config = {'position': (0, 0, 1.0),
             'w': 2,
             'h': 2,
             'loop': True,
             'callback': None}
            self.cgPlayer.playMovie('login_loop', config)

    def onIsRemember(self, *arg):
        self.setRememberStatus(arg[3][0].GetBool())

    def onIsGtLogin(self, *arg):
        pass

    def onIsGtAutoLogin(self, *arg):
        isGtAuto = arg[3][0].GetBool()
        gameglobal.rds.loginManager.autoLogin = isGtAuto
        self.writeUserInfo()

    def onGetAccAndPwd(self, *arg):
        arr = self.movie.CreateArray()
        arr.SetElement(0, GfxValue(self.userName))
        arr.SetElement(1, GfxValue(self.md5Pwd))
        arr.SetElement(2, GfxValue(self.isRemember))
        arr.SetElement(3, GfxValue(gameglobal.rds.loginManager.isGtLogonMode()))
        arr.SetElement(4, GfxValue(gameglobal.rds.loginManager.autoLogin))
        return arr

    def onOpenIme(self, *arg):
        BigWorld.closeIme()

    def getCapsLight(self, *arg):
        return GfxValue(BigWorld.capsLockOn())

    def onQuitGameClick(self, *arg):
        BigWorld.quit()

    def setRememberStatus(self, isRemember):
        if BigWorld.isPublishedVersion():
            return
        self.isRemember = isRemember

    def onRegisterAccount(self, *arg):
        url = 'http://reg.163.com/reg/reg.jsp?product=ty&url=http%3A%2F%2Fty.163.com%2F2013%2Fzm%2F&loginurl=http%3A%2F%2Fty.163.com%2F2013%2Fzm%2F'
        clientcom.openFeedbackUrl(url)

    def onGetAccountNames(self, *arg):
        prefix = arg[3][0].GetString()
        addParten = arg[3][1].GetString()
        suffixs = ['@163.com',
         '@qq.com',
         '@sina.com',
         '@126.com',
         '@vip.qq.com']
        ret = {}
        ret['name'] = []
        recordNum = 0
        for record in self.loginRecord:
            if record.find(prefix) != -1:
                ret['name'].append({'label': record})
                recordNum += 1

        for suffix in suffixs:
            if suffix.find(addParten) != -1:
                ret['name'].append({'label': prefix + suffix})

        ret['splitIdx'] = recordNum - 1
        return uiUtils.dict2GfxDict(ret, True)

    def setCapsTip(self):
        if self.mc:
            self.mc.Invoke('doSetCapsTip', GfxValue(BigWorld.capsLockOn()))
