#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/login.o
from gamestrings import gameStrings
import BigWorld
import time
import game
import gameglobal
import gametypes
import loginSceneNew
import const
import uiConst
import gamelog
import formula
import clientcom
import netWork
import utils
import ServerZone
import qrcode
from helpers import remoteInterface
from callbackHelper import Functor
from loginClient import loginClient
from gameclass import Singleton
from random import choice
from data import sys_config_data as SCD
LS_OFFLINE = 0
LS_LOGING = 1
LS_LOGED = 2
LOGON_STAGE_LOADING = -1
LOGON_STAGE_FIRST = 0
LOGON_STAGE_LICENSE = 1
LOGON_STAGE_NOTICE = 2
LOGON_STAGE_LOGIN = 3
LOGON_STAGE_CHAR = 4
LOGON_STAGE_SCHOOL = 5
LOGON_STAGE_DETAIL = 6
NEW_LOGON_STAGE_SET = 99
NEW_LOGON_STAGE_TRY_CONNECT = 100
NEW_LOGON_STAGE_CONNECTED = 101
NEW_LOGON_STAGE_TRY_LOGON = 102
NEW_LOGON_STAGE_QUERY_USER = 103
NEW_LOGON_STAGE_QUERIED = 104
NEW_LOGON_STAGE_GTPRE = 105
NEW_LOGON_STAGE_GTLOGIN = 106
NEW_LOGON_STAGE_TRY_QRCODE = 107
NEW_LOGON_STAGE_QRCODE_CONNECTED = 108
NEW_LOGON_STAGE_TRY_FEIHUO = 109
NEW_LOGON_STAGE_FEIHUO_CONNECTED = 110
NEW_LOGON_STAGE_TRY_YIYOU = 111
NEW_LOGON_STAGE_YIYOU_CONNECTED = 112
GT_FIRST_HOST_INDEX = 0
state = LS_OFFLINE

def getInstance():
    return LoginManager.getInstance()


class LoginManager(object):
    __metaclass__ = Singleton
    LOGON1 = 0
    LOGON2 = 1

    def __init__(self):
        self.characterList = CharacterList()
        self.logonClient = None
        self.logonMode = self.LOGON2
        self.connectBegin = 0
        self.autoLogin = True
        self.autoIntoServer = True
        self.pageIndex = 0
        self.disconnecting = False
        self.cache = {}
        self.srvDict = ServerZone.ServerZone()
        if not self.srvDict.load():
            return
        else:
            self.userNameSaved = ''
            self.userPasswordSaved = ''
            self.reCheckKey = ''
            self.gskey = ''
            self.rpkey = ('', '')
            self.stage = LOGON_STAGE_LOADING
            self.proxyKey = ''
            self.replyKeyErrorRetry = 0
            self.keyErrMsgBox = None
            self.zhiShengGbId = 0
            self.gtKick = False
            self.setGtLogonMode(gameglobal.rds.configSect.readBool('login/gtLogin', True))
            self.gt_hosts = list(gameglobal.rds.configSect.readStrings('login/gtHost/Host'))
            self.gtDomain = gameglobal.rds.configSect.readString('login/gtDomain')
            if not self.gt_hosts:
                self.gt_hosts = ['10.240.120.53']
            if self.gtDomain:
                self.gt_hosts.insert(GT_FIRST_HOST_INDEX, self.gtDomain)
            self.gtHostIndex = 0
            self.gtHostChoices = range(len(self.gt_hosts))
            self.gt_port = gameglobal.rds.configSect.readInt('login/gtPort', 8766)
            gameglobal.rds.loginHostIP = None
            self.useLoginSceneNew = True
            self.waitingForEnterGame = False
            if not game.cgMovie:
                gameglobal.rds.loginScene = loginSceneNew.LoginScene()
                gameglobal.rds.loginScene.loadSpace()
            BigWorld.worldDrawEnabled(False)
            return

    def reset(self):
        self.disconnecting = False
        self.zhiShengGbId = 0

    def onReceiveChar(self, auth, name, lv, appinfo, phyinfo, signal, spaceNo, chunk, avatarConfig, extra, gbID = 0, resetInfo = {}, isHoliday = False):
        gamelog.debug('hjx: onReceiveChar', auth, name, lv, appinfo, phyinfo, signal, spaceNo, chunk)
        self.characterList.addNew(auth, name, lv, appinfo, phyinfo, signal, spaceNo, chunk, avatarConfig, extra, gbID, resetInfo, isHoliday)

    def onUpdateCharacterAuth(self, gbId, auth):
        for i in range(len(self.characterList.characterDetail)):
            detail = self.characterList.characterDetail[i]
            if detail['gbID'] == gbId:
                detail['auth'] = auth
                self._onCharaterAuthChange(auth, gbId)
                break

    def _onCharaterAuthChange(self, auth, gbId):
        detail = None
        index = -1
        for i in range(len(self.characterList.characterDetail)):
            detail = self.characterList.characterDetail[i]
            if detail['gbID'] == gbId:
                detail['auth'] = auth
                index = i
                break

        if detail:
            if auth == const.AUTH_VALID_PERMIT:
                gameglobal.rds.ui.characterCreate.setRoleCharacter(index, self.characterList.getCharacterInfo(index))
                return
            if auth == const.AUTH_VALID_SELLING:
                gameglobal.rds.ui.characterCreate.setSellingCharacter(index)
                return
            if auth == const.AUTH_VALID_BOUGHT:
                gameglobal.rds.ui.characterCreate.setBoughtCharacter(index)
                return

    def setSelectedChar(self, name):
        self.characterList.setSelectedChar(name)

    def disconnectFromGame(self):
        if self.disconnecting:
            return
        else:
            self.disconnecting = True
            if gameglobal.rds.GameState != gametypes.GS_LOGIN:
                game.onQuit(False)
            BigWorld.enableCameraChange(False)
            BigWorld.worldDrawEnabled(False)
            BigWorld.disconnect()
            from helpers import protect
            protect.nepRoleLogout(gameglobal.rds.loginUserName, gameglobal.rds.gbId)
            BigWorld.resetEntityManager()
            gameglobal.rds.loginUserName = None
            gameglobal.rds.loginUserPassword = None
            gameglobal.rds.loginHostIp = None
            gameglobal.rds.gbId = 0
            BigWorld.setWindowTitle(0, '')
            BigWorld.setWindowTitle(1, '')
            BigWorld.setWindowTitle(2, '')
            self.resetProxyKey()
            game.tick()
            return

    def onDisconnect(self):
        p = BigWorld.player()
        if p and hasattr(p, 'ap'):
            p.ap.release()
        if self.gtKick:
            self.gtKick = False
            self.pageIndex = 1
            self.updatePage()
            game.playBinkCg('login')
            return
        if self.isGtLogonMode():
            self.pageIndex = 1
            self.tryQueryUser()
        else:
            self.pageIndex = 1
            self.updatePage()

    def onGtDisconnect(self):
        if self.pageIndex == 2:
            self.pageIndex = 1
            self.updatePage()
            game.playBinkCg('login')
        elif self.pageIndex == 3 and not (BigWorld.player() and BigWorld.player().__class__.__name__ == 'PlayerAvatar'):
            self.gtKick = True
            gameglobal.rds.ui.characterCreate.doReturnLogin(bRefreshServerList=False)

    def setLogonMode(self, mode):
        self.logonMode = mode
        if mode == self.LOGON1:
            self.stage = LOGON_STAGE_LOADING
        elif mode == self.LOGON2:
            self.stage = NEW_LOGON_STAGE_SET

    def setGtLogonMode(self, isGt):
        self.setLogonMode(self.LOGON2) if isGt else self.setLogonMode(self.LOGON1)

    def isGtLogonMode(self):
        return self.logonMode == self.LOGON2

    def onLoging(self):
        global state
        state = LS_LOGING

    def tryConnect(self):
        if self.logonClient is None:
            self.logonClient = loginClient()
            self.logonClient.set_reporter(self)
        if self.logonClient.get_status() > loginClient.ST_INIT:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_LOGIN_244, Functor(self.onLoginReply, True))
            self.tryDisconnect()
            return
        else:
            if self.gtDomain and GT_FIRST_HOST_INDEX in self.gtHostChoices:
                self.gtHostIndex = GT_FIRST_HOST_INDEX
            else:
                self.gtHostIndex = choice(self.gtHostChoices)
            gamelog.debug('b.e.:tryConnect', self.gt_hosts[self.gtHostIndex])
            self.logonClient.connect((self.gt_hosts[self.gtHostIndex], self.gt_port))
            self.connectBegin = BigWorld.time()
            self.stage = NEW_LOGON_STAGE_TRY_CONNECT
            self.autoIntoServer = True
            if len(self.gtHostChoices) == len(self.gt_hosts):
                gameglobal.rds.ui.showTips(gameStrings.TEXT_LOGIN_258, False)
            self.gtHostChoices.remove(self.gtHostIndex)
            return

    def resetQRCodeCD(self):
        if getattr(self, 'getQRCodeCD', None):
            delattr(self, 'getQRCodeCD')

    def tryConnectQRCode(self):
        if getattr(self, 'getQRCodeCD', None):
            return
        else:
            self.getQRCodeCd = True
            BigWorld.callback(2, self.resetQRCodeCD)
            if self.logonClient is None:
                self.logonClient = loginClient()
                self.logonClient.set_reporter(self)
            if self.gtDomain and GT_FIRST_HOST_INDEX in self.gtHostChoices:
                self.gtHostIndex = GT_FIRST_HOST_INDEX
            else:
                self.gtHostIndex = choice(self.gtHostChoices)
            gamelog.debug('b.e.:tryConnectQRCode', self.gt_hosts[self.gtHostIndex])
            self.logonClient.connect((self.gt_hosts[self.gtHostIndex], self.gt_port))
            self.connectBegin = BigWorld.time()
            self.stage = NEW_LOGON_STAGE_TRY_QRCODE
            self.autoIntoServer = True
            return

    def tryConnectFeihuo(self):
        if self.logonClient is None:
            self.logonClient = loginClient()
            self.logonClient.set_reporter(self)
        if self.gtDomain and GT_FIRST_HOST_INDEX in self.gtHostChoices:
            self.gtHostIndex = GT_FIRST_HOST_INDEX
        else:
            self.gtHostIndex = choice(self.gtHostChoices)
        self.logonClient.status = self.logonClient.ST_INIT
        self.logonClient.connect((self.gt_hosts[self.gtHostIndex], self.gt_port))
        self.connectBegin = BigWorld.time()
        self.stage = NEW_LOGON_STAGE_TRY_FEIHUO
        self.autoIntoServer = True

    def tryConnectyYiyou(self):
        if self.logonClient is None:
            self.logonClient = loginClient()
            self.logonClient.set_reporter(self)
        if self.gtDomain and GT_FIRST_HOST_INDEX in self.gtHostChoices:
            self.gtHostIndex = GT_FIRST_HOST_INDEX
        else:
            self.gtHostIndex = choice(self.gtHostChoices)
        self.logonClient.status = self.logonClient.ST_INIT
        self.logonClient.connect((self.gt_hosts[self.gtHostIndex], self.gt_port))
        self.connectBegin = BigWorld.time()
        self.stage = NEW_LOGON_STAGE_TRY_YIYOU
        self.autoIntoServer = True

    def tryDisconnect(self):
        if self.logonClient:
            try:
                self.logonClient.disconnect()
            except:
                pass

            self.logonClient = None

    def retryEkey(self):
        self.logonClient.status = self.logonClient.ST_NEED_EKEY
        self.keyErrMsgBox = None

    def retryMimaka(self):
        self.logonClient.status = self.logonClient.ST_NEED_MIMAKA
        self.keyErrMsgBox = None

    def mimakaLimit(self):
        self.logonClient.status = self.logonClient.ST_CAN_LOGON
        self.keyErrMsgBox = None
        self.gotoLoginPage()

    def checkLogonState(self):
        if gameglobal.rds.GameState >= gametypes.GS_LOADING:
            return
        elif self.logonClient is None:
            return
        elif not self.isGtLogonMode():
            return
        else:
            client = self.logonClient
            status = client.get_status()
            if status == loginClient.ST_INIT:
                if self.stage == NEW_LOGON_STAGE_TRY_CONNECT:
                    if self.gtHostChoices:
                        self.tryDisconnect()
                        self.tryConnect()
                self.checkTimeoutNew()
            elif status == loginClient.ST_CAN_LOGON:
                if self.stage == NEW_LOGON_STAGE_TRY_CONNECT:
                    self.stage = NEW_LOGON_STAGE_CONNECTED
                    self.tryLoginClient()
                elif self.stage == NEW_LOGON_STAGE_TRY_QRCODE:
                    self.stage = NEW_LOGON_STAGE_QRCODE_CONNECTED
                    self.queryQRCode()
                elif self.stage == NEW_LOGON_STAGE_TRY_FEIHUO:
                    self.stage = NEW_LOGON_STAGE_FEIHUO_CONNECTED
                    self.queryFeihuo()
                elif self.stage == NEW_LOGON_STAGE_TRY_YIYOU:
                    self.stage = NEW_LOGON_STAGE_YIYOU_CONNECTED
                    self.queryYiyou()
            elif status == loginClient.ST_NEED_EKEY:
                self.ekeyp()
                self.onLoging()
            elif status == loginClient.ST_EKEY_ERR:
                if self.keyErrMsgBox is None:
                    self.keyErrMsgBox = gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_LOGIN_368, self.retryEkey)
            elif status == loginClient.ST_REAL_NAME_NO:
                self.nameCertificationReq()
                self.onLoging()
            elif status == loginClient.ST_REAL_NAME_WAIT:
                self.finishNameCertificationReq()
            elif status == loginClient.ST_REAL_NAME_PASS:
                self.finishNameCertificationReq()
            elif status == loginClient.ST_REAL_NAME_FAIL:
                self.nameCertificationReq()
                self.onLoging()
            elif status == loginClient.ST_REAL_NAME_FINISH:
                pass
            elif status == loginClient.ST_NEED_MIMAKA:
                self.passCard(self.logonClient.ppc)
                self.onLoging()
            elif status == loginClient.ST_MIMAKA_ERR:
                if self.keyErrMsgBox is None:
                    self.keyErrMsgBox = gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_LOGIN_386, self.retryMimaka)
            elif status == loginClient.ST_MIMAKA_ERR_LIMIT:
                if self.keyErrMsgBox is None:
                    self.keyErrMsgBox = gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_LOGIN_389, self.mimakaLimit)
            elif status == loginClient.ST_LOGINED:
                self.tryQueryUser()
            elif status == loginClient.ST_QUERYUSER:
                self.checkTimeoutUser()
            elif status == loginClient.ST_CHOSE_SERVER:
                if self.stage == NEW_LOGON_STAGE_QUERY_USER:
                    gamelog.debug('b.e.:new login zone server', client.getServers())
                    self.srvDict.updateCharNum(client.getServers())
                    self.stage = NEW_LOGON_STAGE_QUERIED
                    self.pageIndex = 2
                    self.updatePage()
                    self._checkAutoIntoServer()
            elif client.get_status() == loginClient.ST_LOGIN_PRE:
                if self.stage == NEW_LOGON_STAGE_GTPRE:
                    self.tryGtLogin()
            elif status == loginClient.ST_CONNECTING:
                if BigWorld.time() - self.connectBegin > 30:
                    self.logonClient.on_disconnected()
            return

    def checkTimeoutNew(self):
        if self.stage == NEW_LOGON_STAGE_TRY_CONNECT:
            gamelog.debug('b.e.: checkTimeoutNew', BigWorld.time() - self.connectBegin)
            if BigWorld.time() - self.connectBegin > 10:
                gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_LOGIN_415, Functor(self.onLoginReply, True))
                self.stage = NEW_LOGON_STAGE_SET

    def checkTimeoutUser(self):
        if self.stage == NEW_LOGON_STAGE_QUERY_USER:
            gamelog.debug('b.e.: checkTimeoutUser', BigWorld.time() - self.connectBegin)
            if BigWorld.time() - self.connectBegin > 10:
                gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_LOGIN_422, Functor(self.onLoginReply, True))
                self.stage = NEW_LOGON_STAGE_TRY_CONNECT

    def ekeyp(self):
        gameglobal.rds.ui.hideTips()
        gameglobal.rds.ui.mibao.showJiangJunLing(self)

    def passCard(self, msg):
        gameglobal.rds.ui.hideTips()
        gameglobal.rds.ui.mibao.showMibaoCard(self, msg)

    def nameCertificationReq(self):
        gameglobal.rds.ui.hideTips()
        gameglobal.rds.ui.nameCertification.show(self)

    def finishNameCertificationReq(self):
        self.logonClient.finishRealNameReq()

    def tryLoginClient(self):
        gamelog.debug('b.e.: tryLoginClient', BigWorld.player())
        userName = self.userName()
        password = self.userPwd()
        self.userNameSaved = userName
        self.userPasswordSaved = password
        self.reCheckKey = ''
        if gameglobal.rds.loginAuthType == const.LOGIN_AUTH_RU_GC:
            self.logonClient.logonByMRToken(userName, password, '0000-0000-0000-0000', gameglobal.rds.logOnAttemptKey)
        elif gameglobal.rds.loginAuthType == const.LOGIN_AUTH_EU_GC:
            self.logonClient.logonByEUToken(userName, password, '0000-0000-0000-0000', gameglobal.rds.logOnAttemptKey)
        else:
            self.logonClient.logon(userName, password, '0000-0000-0000-0000', gameglobal.rds.logOnAttemptKey)
        self.stage = NEW_LOGON_STAGE_TRY_LOGON

    def tryQueryUser(self):
        client = self.logonClient
        gamelog.debug('b.e.: tryQueryUser', client)
        if client:
            if client.status < client.ST_LOGINED:
                self.updatePage()
                return
            client.status = client.ST_LOGINED
            client.queryuser(self.userNameSaved)
            self.connectBegin = BigWorld.time()
            self.stage = NEW_LOGON_STAGE_QUERY_USER

    def _checkAutoIntoServer(self):
        if not self.autoLogin or not self.autoIntoServer:
            return False
        else:
            self.autoIntoServer = False
            charNum = self._getSelEntry().charNum
            if charNum > 0:
                gameglobal.rds.ui.showTips(gameStrings.TEXT_LOGIN_479, False)
                self.tryConnectGameServer()
                return True
            serversInfo = self.logonClient.getServers()
            if serversInfo and len(serversInfo) > 0:
                zoneData = None
                for treply in serversInfo:
                    if treply.usernum > 0:
                        zoneData = self.srvDict.findByNameExcludeHide(treply.server)
                        break

                if zoneData:
                    gameglobal.rds.ui.showTips(gameStrings.TEXT_LOGIN_479, False)
                    gameglobal.rds.ui.loginSelectServer.select(zoneData[0], zoneData[1], zoneData[2])
                    self.tryConnectGameServer()
                    return True
            return False

    def userName(self):
        return gameglobal.rds.ui.loginWin.userName

    def userPwd(self):
        return gameglobal.rds.ui.loginWin.md5Pwd

    def gsKey(self):
        return self.gskey

    def rpKey(self):
        return self.rpkey

    def _getSelEntry(self):
        return gameglobal.rds.ui.loginSelectServer.getSelEntry()

    def hostIPS(self):
        return self._getSelEntry().ip

    def serverMode(self):
        return int(self._getSelEntry().mode)

    def hostIP(self):
        index = int(self._getSelEntry().locale)
        if index == 3:
            index = 0
        return self._getSelEntry().ip[index]

    def hostTitle(self):
        return self._getSelEntry().title

    def isBgp(self):
        return self._getSelEntry().bgp

    def isEduNet(self):
        return self._getSelEntry().isEduNet

    def hostType(self):
        return int(self._getSelEntry().locale) + 1

    def netVendor(self):
        if gameglobal.rds.ui.loginSelectServer.venderIdx == 0:
            return gameglobal.rds.loginManager.srvDict.service
        return gameglobal.rds.ui.loginSelectServer.venderIdx

    def realVendor(self):
        return gameglobal.rds.ui.loginSelectServer.venderIdx

    def proxyVendor(self):
        try:
            vendor = self.netVendor()
            if self.isBgp():
                if self.isEduNet() and vendor == 3:
                    gamelog.debug('zhp: proxy vendor, edunet')
                    return True
                return False
            if vendor == 0:
                gamelog.debug('zhp: proxy vendor, auto')
                return True
            if self.hostType() == vendor:
                gamelog.debug('zhp:proxy not vendor')
                return False
        except Exception as e:
            gamelog.error(e.message)
            return False

        return True

    def hostName(self):
        return self._getSelEntry().name

    def titleName(self):
        return self._getSelEntry().title

    def tryConnectGameServer(self):
        if not self.logonClient or self.logonClient.checkInitState():
            return
        self.reset()
        hostName = self.hostName()
        titleName = self.titleName()
        if hostName != titleName:
            msg = gameStrings.TEXT_LOGIN_585 % (hostName, titleName, titleName)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.doConnectGameServer, gameStrings.TEXT_IMPPLAYERTEAM_644, gameglobal.rds.ui.loginSelectServer.releaseLockServer, gameStrings.TEXT_AVATAR_2876_1)
            return
        self.doConnectGameServer()

    def doConnectGameServer(self):
        netWork.initOnline(self.userNameSaved)

    def tryGtLoginPre(self, ip_key):
        if not self.logonClient or self.logonClient.checkInitState():
            return
        if self.stage == NEW_LOGON_STAGE_GTLOGIN:
            self.stage = NEW_LOGON_STAGE_QUERIED
            self.logonClient.status = self.logonClient.ST_CHOSE_SERVER
        if self.stage in (NEW_LOGON_STAGE_QUERIED, NEW_LOGON_STAGE_GTPRE):
            account = BigWorld.player()
            if account.__class__.__name__ == 'PlayerAccount':
                if self.logonClient:
                    account.base.gtLoginPre('', self.logonClient.getServerUUID(), self.logonClient.getServiceUUID(), ip_key, clientcom.CLIENT_REVISION, gameglobal.rds.clientInfo)
                    self.stage = NEW_LOGON_STAGE_GTPRE

    def tryGtLogin(self):
        if not self.logonClient or self.logonClient.checkInitState():
            return
        if self.stage == NEW_LOGON_STAGE_GTPRE:
            account = BigWorld.player()
            if account.__class__.__name__ == 'PlayerAccount':
                if self.logonClient:
                    logininfo = self.logonClient.getLoginInfo()
                    if logininfo:
                        account.base.gtLogin(self.logonClient.getServerUUID(), self.logonClient.getServiceUUID(), logininfo.randkey, self.userPasswordSaved, self._getSelEntry().charNum)
                        self.stage = NEW_LOGON_STAGE_GTLOGIN

    def onLoginReply(self, prevPage = False, popomsg = ''):
        gamelog.debug('b.e.:onLoginReply', prevPage, popomsg)
        p = BigWorld.player()
        if p.__class__.__name__ == 'PlayerAvatar' and popomsg:
            gameglobal.rds.ui.characterDetailAdjust.closeTips()
            gameglobal.rds.ui.messageBox.showMsgBox(popomsg)
        if prevPage:
            self.prevPage()

    def onClientReply(self, prevPage = False, popomsg = ''):
        gamelog.debug('b.e.:onClientReply', prevPage, popomsg)
        p = BigWorld.player()
        if prevPage:
            self.prevPage()
        if p.__class__.__name__ != 'PlayerAvatar' and popomsg:
            gameglobal.rds.ui.characterDetailAdjust.showTips(popomsg)

    def queryQRCode(self):
        if self.logonClient:
            self.logonClient.getQRCode()

    def queryFeihuo(self):
        CEFModule = None
        try:
            import CEFManager as CEFModule
            from helpers import CEFControl
        except:
            CEFModule = None

        CEFControl.requestInnerText(self.feihuoRequestInnerTextCB)

    def feihuoRequestInnerTextCB(self, cookie):
        userName = 'szh141'
        self.logonClient.feiHuoLogin(userName, cookie, '0000-0000-0000-0000', gameglobal.rds.logOnAttemptKey)
        self.stage = NEW_LOGON_STAGE_TRY_LOGON

    def queryYiyou(self):
        loginInfo = gameglobal.rds.ui.feihuoLogin.loginInfo
        uid = getattr(loginInfo, 'yiyouUID', '')
        token = getattr(loginInfo, 'yiyouToken', '')
        self.logonClient.yiyouLogin(uid, token)
        self.stage = NEW_LOGON_STAGE_TRY_LOGON

    def onQRCode(self, codeUUID):
        codeMaker = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=2)
        code = '{\"s\":\"urs\",\"a\":\"login\",\"l\":{\"p\":\"ty\",\"i\":\"%s\"}}' % codeUUID
        codeMaker.add_data(code)
        codeMaker.make(fit=True)
        img = codeMaker.make_image()
        pngUrl = img.convert('RGB').tostring('jpeg', 'RGB', 90)
        if pngUrl:
            gameglobal.rds.ui.loginWin.setQRCode(pngUrl)

    def _onUpdateQRCode(self, pngURL):
        if pngURL:
            gameglobal.rds.ui.loginWin.setQRCode(pngURL)

    def updatePage(self):
        gameglobal.rds.ui.hideTips()
        index = self.pageIndex
        gamelog.debug('b.e.:updatePage', index)
        if self.isGtLogonMode():
            if index == 0:
                pass
            elif index == 1:
                self.gotoLoginPage()
            elif index == 2:
                self.gotoServerPage()
            elif index == 3:
                self.gotoCharPage()
        elif index == 0:
            pass
        elif index == 1:
            self.gotoLoginPage()
        elif index >= 2:
            self.gotoCharPage()

    def firstPage(self):
        self.pageIndex = 1
        self.updatePage()

    def prevPage(self):
        self.pageIndex -= 1
        if self.pageIndex < 1:
            self.pageIndex = 1
        self.updatePage()

    def nextPage(self):
        self.pageIndex += 1
        m = 3 if self.isGtLogonMode() else 2
        if self.pageIndex > m:
            self.pageIndex = m
        self.updatePage()

    def gotoLoginPage(self):
        self.tryDisconnect()
        self.gtHostChoices = range(len(self.gt_hosts))
        gameglobal.rds.ui.feihuoLogin.feihuoLoginHide(False)
        gameglobal.rds.ui.loginSelectServer.hide()
        gameglobal.rds.ui.loginWin.showLoginWin()

    def gotoServerPage(self):
        gameglobal.rds.ui.feihuoLogin.hide()
        gameglobal.rds.ui.loginWin.hide()
        gameglobal.rds.ui.loginSelectServer.show()

    def gotoCharPage(self):
        gameglobal.rds.ui.loginWin.clearEffect()
        gameglobal.rds.ui.loginWin.writeUserInfo()
        gameglobal.rds.ui.feihuoLogin.hide()
        gameglobal.rds.ui.loginWin.hide()
        gameglobal.rds.ui.loginSelectServer.hide()
        gameglobal.rds.ui.characterCreate.loadAllCCWidgets()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TOP_MESSAGE)

    def getProxyKey(self):
        return self.proxyKey

    def genProxyKey(self, callback):
        remoteInterface.getNetKey(Functor(self._onProxyKey, callback))

    def _onProxyKey(self, callback, data):
        if data != '':
            self.proxyKey = data
        else:
            self.proxyKey = ''
        callback(data)

    def resetProxyKey(self):
        self.replyKeyErrorRetry = 0
        self.proxyKey = ''

    def updateChange(self, gbID, info):
        if self.cache:
            for i, data in enumerate(self.characterList.characterDetail):
                if data.get('gbID', 0) == self.cache.get('gbID', 0):
                    for key, value in self.cache.iteritems():
                        if key == 'hair':
                            self.characterList.characterDetail[i]['physique'].hair = value
                        elif key == 'bodyType':
                            self.characterList.characterDetail[i]['physique'].bodyType = value
                        elif key == 'sex':
                            self.characterList.characterDetail[i]['physique'].sex = value
                        elif key == 'school':
                            self.characterList.characterDetail[i]['physique'].school = value
                        else:
                            self.characterList.updateCharacterInfo(i, {key: value})

                if data.get('gbID', 0) == gbID:
                    self.characterList.updateCharacterInfo(i, info)

            self.cache = {}

    def gbID2Index(self, gbID):
        return self.characterList.gbID2uiIndex(gbID)


class CharacterList(object):
    CHARACTER_PROP_TEMPLATE = {'auth': None,
     'name': 'None',
     'rename': None,
     'school': None,
     'appearance': None,
     'physique': None,
     'signal': None,
     'avatarConfig': None,
     'lv': None,
     'where': None,
     'spaceNo': None,
     'chunk': None,
     'extra': None,
     'gbID': None,
     'resetInfo': {},
     'isHoliday': None}

    def __init__(self):
        self.clearAll()

    def checkExists(self, name):
        for ch in self.characterDetail:
            if ch['name'] == name:
                return True

        return False

    def getCharacterIdxByGBID(self, gbID):
        if not gbID:
            return -1
        for i in xrange(len(self.characterDetail)):
            if self.characterDetail[i]['gbID'] == gbID:
                return i

        return -1

    def isCancelDetele(self, auth, name):
        if auth == const.AUTH_VALID_PERMIT:
            for i in xrange(len(self.characterDetail)):
                if self.characterDetail[i]['name'] == name:
                    if self.characterDetail[i]['auth'] in (const.AUTH_VALID_COOL, const.AUTH_VALID_DELETE):
                        return True

            return False
        else:
            return False

    def addNew(self, auth, name, lv, appinfo, phyinfo, signal, spaceNo, chunk, avatarConfig, extra, gbID = 0, restInfo = {}, isHoliday = False):
        gamelog.debug('@zs login.addNew', auth, name, self.isCancelDetele(auth, name), self.checkExists(name))
        if self.checkExists(name):
            if auth == const.AUTH_VALID_DROP:
                l = len(self.characterDetail)
                for i in xrange(l):
                    if self.characterDetail[i]['name'] == name:
                        self.characterDetail.remove(self.characterDetail[i])
                        self.count -= 1
                        self.isEmpty[self.count] = True
                        break

                if gameglobal.rds.loginScene.inCreateStage():
                    if self.count:
                        self.relayout()
                    else:
                        gameglobal.rds.loginScene.clearPlayer()
                        gameglobal.rds.ui.characterCreate.setFocusCharacter(-1)
                        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHARACTER_CREATE_TIP)
                for index in xrange(len(self.characterDetail)):
                    if self.characterDetail[index]['auth'] in (const.AUTH_VALID_COOL, const.AUTH_VALID_DELETE):
                        gameglobal.rds.ui.characterCreate.setCoolCharacter(index)
                    else:
                        gameglobal.rds.ui.characterCreate.setRoleCharacter(index, self.getCharacterInfo(index))
                        if self.characterDetail[index]['auth'] == const.AUTH_VALID_BOUGHT:
                            gameglobal.rds.ui.characterCreate.setBoughtCharacter(index)
                        elif self.characterDetail[index]['auth'] == const.AUTH_VALID_SELLING:
                            gameglobal.rds.ui.characterCreate.setSellingCharacter(index)

                gameglobal.rds.ui.characterCreate.setRoleCharacter(self.count, {'name': ''})
                return
            if auth == const.AUTH_VALID_COOL:
                for i in xrange(len(self.characterDetail)):
                    if self.characterDetail[i]['name'] == name:
                        self.characterDetail[i]['auth'] = auth
                        self.characterDetail[i]['extra']['tDeleteInterval'] = extra['tDeleteInterval']
                        self.characterDetail[i]['extra']['tNotify'] = int(time.time())
                        gameglobal.rds.ui.characterCreate.setCoolCharacter(i)
                        return

            elif auth == const.AUTH_VALID_DELETE:
                for i in xrange(len(self.characterDetail)):
                    if self.characterDetail[i]['name'] == name:
                        self.characterDetail[i]['auth'] = auth
                        gameglobal.rds.ui.characterCreate.setDeleteCharacter(i)
                        return

            else:
                if self.isCancelDetele(auth, name):
                    for i in xrange(len(self.characterDetail)):
                        if self.characterDetail[i]['name'] == name:
                            self.characterDetail[i]['auth'] = auth
                            gameglobal.rds.ui.characterCreate.setCancelDeleteCharacter(i)
                            return

                    return
                if auth == const.AUTH_VALID_SELLING:
                    for i in xrange(len(self.characterDetail)):
                        if self.characterDetail[i]['name'] == name:
                            gameglobal.rds.ui.characterCreate.setSellingCharacter(i)
                            break

                    return
                if auth == const.AUTH_VALID_BOUGHT:
                    for i in xrange(len(self.characterDetail)):
                        if self.characterDetail[i]['name'] == name:
                            gameglobal.rds.ui.characterCreate.setBoughtCharacter(i)
                            break

                    return
        if auth == const.AUTH_VALID_DROP:
            gamelog.debug('ypc@ error: adding a dropped character!')
            return
        if auth == const.AUTH_VALID_PERMIT:
            characterIdx = self.getCharacterIdxByGBID(gbID)
            gamelog.debug('dxk@ item rename character', characterIdx)
            if characterIdx >= 0:
                self.characterDetail[characterIdx]['name'] = name
                self.characterDetail[characterIdx]['rename'] = ''
                gameglobal.rds.ui.characterCreate.setRoleCharacter(characterIdx, self.getCharacterInfo(characterIdx))
                return
        if auth == const.AUTH_VALID_RENAME:
            characterIdx = self.getCharacterIdxByGBID(gbID)
            gamelog.debug('dxk@ rename character', characterIdx)
            if characterIdx >= 0:
                rename = ''
                if utils.isRenameString(name):
                    rename = name
                    if utils.isMigrateRename(name):
                        name = utils.parseMigrateName(name)
                    else:
                        name = utils.preRenameString(name)
                self.characterDetail[characterIdx]['name'] = name
                self.characterDetail[characterIdx]['rename'] = rename
                gameglobal.rds.ui.characterCreate.setRoleCharacter(characterIdx, self.getCharacterInfo(characterIdx))
                return
        self.addCharacter(auth, name, lv, appinfo, phyinfo, signal, spaceNo, chunk, avatarConfig, extra, gbID, restInfo, isHoliday)
        lastIndex = self.count - 1
        gameglobal.rds.ui.characterCreate.setRoleCharacter(lastIndex, self.getCharacterInfo(lastIndex))
        if auth == const.AUTH_VALID_COOL:
            gameglobal.rds.ui.characterCreate.setCoolCharacter(lastIndex)
        elif auth == const.AUTH_VALID_DELETE:
            gameglobal.rds.ui.characterCreate.setDeleteCharacter(lastIndex)
        elif self.isCancelDetele(auth, name):
            gameglobal.rds.ui.characterCreate.setCancelDeleteCharacter(lastIndex)
        elif auth == const.AUTH_VALID_SELLING:
            gamelog.debug('ypc@ login AUTH_VALID_SELLING!', lastIndex)
            gameglobal.rds.ui.characterCreate.setSellingCharacter(lastIndex)
        elif auth == const.AUTH_VALID_BOUGHT:
            gameglobal.rds.ui.characterCreate.setBoughtCharacter(lastIndex)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHARACTER_CREATE_TIP)
        if self.isFirstCharacter:
            self.isFirstCharacter = False

    def setStraightLvUpInfo(self, info):
        for i, data in enumerate(self.straightLvUpInfo):
            if data in self.characterDetail:
                self.characterDetail.remove(data)
                self.count -= 1
                self.isEmpty[self.count] = True

        for i, data in enumerate(info):
            temp = dict(self.CHARACTER_PROP_TEMPLATE)
            temp.update(data)
            data.update(temp)
            data['name'] = data['sourceGbId']
            data['auth'] = const.AUTH_VALID_LVUP
            data['lv'] = 'Lv.%d' % data['lv']

        self.straightLvUpInfo = info
        self.characterDetail = self.straightLvUpInfo + self.characterDetail
        for i, data in enumerate(info):
            if self.count >= const.CHAR_NUM:
                self.isEmpty.append(False)
            else:
                self.isEmpty[self.count] = False
            gameglobal.rds.ui.characterCreate.setRoleCharacter(i, self.getCharacterInfo(i))
            self.count += 1

    def setSelectedChar(self, name):
        if gameglobal.rds.loginScene.inCreateStage():
            for i in xrange(len(self.characterDetail)):
                char = self.characterDetail[i]
                if name == char['name']:
                    self.relayout(i)
                    return

            self.relayout(0)

    def addCharacter(self, auth, name, lv, appinfo, phyinfo, signal, spaceNo, chunk, avatarConfig, extra, gbID = 0, restInfo = {}, isHoliday = False):
        gamelog.debug('hjx:received new player-info ', len(self.characterDetail), ':', name, ' ')
        gamelog.debug('jorsef:received new player, appinfo:', appinfo)
        rename = ''
        if utils.isRenameString(name):
            rename = name
            if utils.isMigrateRename(name):
                name = utils.parseMigrateName(name)
            else:
                name = utils.preRenameString(name)
        if auth == const.AUTH_VALID_COOL:
            extra['tNotify'] = int(time.time())
        self.characterDetail.append({'auth': auth,
         'name': name,
         'rename': rename,
         'school': phyinfo.school,
         'appearance': appinfo,
         'physique': phyinfo,
         'signal': signal,
         'avatarConfig': avatarConfig,
         'lv': lv,
         'where': formula.whatLocationName(spaceNo, chunk),
         'spaceNo': spaceNo,
         'chunk': chunk,
         'extra': extra,
         'gbID': gbID,
         'resetInfo': restInfo,
         'isHoliday': isHoliday})
        if self.count >= const.CHAR_NUM:
            self.isEmpty.append(False)
        else:
            self.isEmpty[self.count] = False
        self.count += 1

    def getCharacterInfo(self, index):
        character = self.characterDetail[index]
        ret = {}
        ret['auth'] = character['auth']
        ret['name'] = character['name']
        ret['school'] = character['school']
        ret['lv'] = character['lv']
        ret['where'] = character['where']
        ret['resetInfo'] = character['resetInfo']
        ret['extra'] = character['extra']
        ret['isHoliday'] = character['isHoliday']
        ret['changedSchool'] = character['resetInfo'].get(gametypes.RESET_PROPERTY_SCHOOL, 0)
        if character.has_key('beginTime'):
            validTime = character['beginTime'] + SCD.data.get('straightLvUpKeepTime', 5184000)
            st = time.localtime(validTime)
            ret['validTime'] = gameStrings.TEXT_LOGIN_1028 % (st.tm_year, st.tm_mon, st.tm_mday)
        return ret

    def getCharacterOriginalInfo(self, index):
        if index >= 0 and index < len(self.characterDetail):
            return self.characterDetail[index]
        else:
            return None

    def relayout(self, index = 0):
        gamelog.debug('hjx: relayout', self.count, index)
        if self.count > 0:
            gameglobal.rds.ui.characterCreate.setFocusCharacter(index)
            gameglobal.rds.loginScene.placePlayer(self.characterDetail[index])
        else:
            gameglobal.rds.ui.characterCreate.setFocusCharacter(-1)

    def clearAll(self):
        self.characterDetail = []
        self.straightLvUpInfo = []
        self.isFirstCharacter = True
        self.count = 0
        self.isEmpty = [ True for i in xrange(const.CHAR_NUM) ]

    def isDeleteTimeOut(self, index):
        if index >= len(self.characterDetail):
            return False
        elif self.characterDetail[index]['auth'] != const.AUTH_VALID_COOL:
            return False
        tDeleteInterval = self.characterDetail[index]['extra']['tDeleteInterval']
        tNotify = self.characterDetail[index]['extra']['tNotify']
        tPass = tDeleteInterval - (int(time.time()) - tNotify)
        if tPass <= 0:
            return True
        else:
            return False

    def gbID2uiIndex(self, gbID):
        for i, data in enumerate(self.characterDetail):
            if data.get('gbID', 0) == gbID:
                return i

        return -1

    def updateCharacterInfo(self, index, data):
        self.characterDetail[index].update(data)

    def getAllInfo(self):
        ret = []
        for i, data in enumerate(self.characterDetail):
            ret.append(self.getCharacterInfo(i))

        return ret
