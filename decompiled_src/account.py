#Embedded file name: /WORKSPACE/data/entities/client/account.o
import time
import cPickle
import BigWorld
import Sound
import game
import gameglobal
import clientcom
import gametypes
import gamelog
import const
import netWork
import keys
import utils
import gameConfigUtils
import zlib
from crontab import setCrontabTimeZone
from iClient import IClient
from guis import exceptChannel
from guis import uiConst
from guis import messageBoxProxy
from guis import uiUtils
from helpers import stateSafe
from helpers import protect
from helpers import cgPlayer
from helpers import uuControl
from helpers import seqTask
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from gamestrings import gameStrings

def checkDisableRain():
    if not gameglobal.rds.enablePlanb:
        return
    msgInfo = "您的显卡驱动版本不是最新，由于老版本的N卡驱动对《天谕》兼容性不佳，为了优化游戏体验，请务必更新到最新的驱动版本,<a href=\'event:http://www.geforce.cn/drivers\'><u><font color=\'#00D7FF\'>前往更新</font></u></a>"
    try:
        ver = int(BigWorld.VideoCardDesc()[0].split('+')[1])
        if ver >= 35887 and ver <= 35906:
            if hasattr(BigWorld, 'getOSDesc'):
                if 'win10' in BigWorld.getOSDesc().lower():
                    BigWorld.enableRain(False)
                    gameglobal.rds.ui.messageBox.showMsgBox(msgInfo)
            elif BigWorld.OSDesc().find('Windows') < 0:
                BigWorld.enableRain(False)
                gameglobal.rds.ui.messageBox.showMsgBox(msgInfo)
    except:
        pass


class Account(IClient):

    def __init__(self):
        super(Account, self).__init__()
        gamelog.debug('Account.__init__:', self.id)
        self.exception = exceptChannel.ExceptChannel(True, False)
        self.resetPropFlags = {}
        self.prePayGbId = 0
        self.sharedCnt = 0

    def enterWorld(self, initial = 1):
        pass

    def loginReply(self, status, msg):
        gamelog.debug('Account.error:', msg)

    def checkCharacter(self, msg):
        pass

    def disconnect(self):
        pass

    def characterDetail(self, auth, gbId, name, lv, appearance, physique, signal, spaceNo, chunk, avatarConfig, extra, isHoliday = False):
        pass

    def setDefaultCharacter(self, name):
        pass

    def showLoginScene(self):
        pass

    def hotfixMD5Send(self, smd5):
        pass

    def setPublicServer(self, publicServer):
        pass

    def setHostId(self, hostId):
        pass

    def clearScene(self):
        pass

    def setPrePayFlag(self, prePrayGbId):
        pass

    def prePaySucc(self, gbId):
        pass

    def checkQuitHoliday(self, gbId):
        pass

    def updateClientConfig(self, config):
        pass

    def overpass(self):
        pass

    def sendPropFlags(self, flags):
        pass

    def onGetAccountPhone(self, phone):
        pass

    def onSetAccountPhone(self, flag):
        pass

    def onApplyMessageRemind(self, remind, flag):
        pass

    def onExceptIp(self, ipInfo1, ipInfo2):
        pass

    def confirmDeleteWithCoin(self, roleName, coin, mallCash):
        pass

    def onQueryQueuePlace(self, queuePlace):
        pass

    def returnCCToken(self, rc, content):
        pass

    def showGameMsg(self, msgId, data):
        pass

    def showPhoneBindBoxOnLogin(self):
        pass

    def onNotifyQueueMsg(self, msg, dura):
        pass

    def showMessageBoxAfterVideo(self, msgId, args, title):
        pass

    def showBufferedMsg(self):
        pass

    def onChargeFailed(self):
        pass

    def updateUrsPointData(self, commonPoints, commonFPoints, standbyPoints, specialPoints, specialFPoints):
        pass

    def setServerTimeZone(self, timeZone, zoneName):
        pass

    def showFeihuoMsg(self):
        pass

    def applyCharCfg(self, avatarCfg):
        pass

    def onFetchNOSKey(self, md5Text, timeStamp, args):
        pass

    def onUploadCharCfgData(self, nuid):
        pass

    def syncSharedCnt(self, sharedCnt):
        pass

    def sendStraightLvUpInfo(self, extraInfo):
        pass

    def onGetRandomName(self, randName):
        pass

    def onCheckRealNameFailed(self):
        pass

    def boughtCharacterDetail(self, auth, gbId, name, lv, appearance, physique, signal, spaceNo, chunk, avatarConfig, extra, isHoliday, boughtSeq):
        pass

    def onTakeBackCbgCharacter(self, auth, gbId):
        pass

    def onTakeAwayCbgCharacter(self, auth, gbId):
        pass

    def onTakeAwayCbgCharacterFail(self, gbId):
        pass

    def onTakeBackCbgCharacterWhenNotOpOnCBGWeb(self):
        pass

    def onAvatarBeTakeAway(self, gbId, roleName):
        pass


class PlayerAccount(Account):
    REPLY_MSG = 0
    REPLY_WAITING_URS = 1
    REPLY_CREATE_AND_SELECT = 2
    REPLY_PASSWORD = 3
    REPLY_CREATE_SUCCESS = 4
    REPLY_RELOG = 5
    REPLY_PROCESSING_RELONG = 6
    REPLY_MIMAKA = 7
    REPLY_EKEY = 8
    REPLY_PHONE = 9
    REPLY_WALLOW = 10
    REPLY_IP = 11
    REPLY_EMAIL_VERIFY = 12
    REPLY_KEY_ERROR = 13
    REPLY_IN_QUEUE = 14
    REPLY_UNACTIVED = 15
    REPLY_BODYTYPE_SUCCESS = 16
    REPLY_AVATARCONFIG_SUCCESS = 17
    REPLY_RENAME_SUCCESS = 18
    REPLY_PHONE_INVALID = 19
    REPLY_SERVER_LOADED = 20
    REPLY_CANCEL_PROP_FLAG = 21
    REPLY_SCHOOL_TRANSFER_SUCCESS = 22

    def __init__(self):
        super(PlayerAccount, self).__init__()
        gamelog.debug('jorsef: playerAccount.init')
        self.commonPoints = 0

    def enterWorld(self, initial = 1):
        Account.enterWorld(self, initial)
        uuControl.pollGetStatus()
        index = gameglobal.rds.loginIndex
        scenePos = gameglobal.rds.loginScene.SCENE_POSITION[index]
        BigWorld.setZonePriority(scenePos[3], -gameglobal.LOGINZONE_PRIO)
        BigWorld.setZonePriority('hand', gameglobal.LOGINZONE_PRIO)
        cam = gameglobal.rds.cam.cc
        cam.needfixCamera = False
        BigWorld.setDepthOfField(False)

    def onBecomePlayer(self):
        gamelog.debug('Account onBecomePlayer')
        self.enterWorld(1)
        if gameglobal.rds.isSinglePlayer:
            return
        if hasattr(gameglobal.rds, 'transServerInfo') and gameglobal.rds.transServerInfo:
            fromHostId, toHostId, playerName, password, transType = gameglobal.rds.transServerInfo[2]
            fromServer = utils.getServerName(fromHostId)
            gamelog.debug('jorsef: transfer', fromServer, playerName, password, transType)
            BigWorld.player().base.transfer(fromHostId, playerName, password, transType)
            gameglobal.rds.transServerInfo = None
            gameglobal.rds.transferCount = 0
            if hasattr(gameglobal.rds, 'reTransferCallback'):
                BigWorld.cancelCallback(gameglobal.rds.reTransferCallback)
                del gameglobal.rds.reTransferCallback
            return
        if gameglobal.rds.reTryLoginOnTransferTimer:
            BigWorld.cancelCallback(gameglobal.rds.reTryLoginOnTransferTimer)
            gameglobal.rds.reTryLoginOnTransferTimer = 0
        gameglobal.rds.reTryLoginOnTransferCnt = 0
        userName = gameglobal.rds.ui.loginWin.userName
        password = gameglobal.rds.ui.loginWin.md5Pwd
        gameglobal.rds.GameState = gametypes.GS_CONNECT
        gameglobal.rds.ui.loginWin.startTime = time.time()
        gameglobal.rds.loginUserName = userName
        gameglobal.rds.loginUserPassword = password
        if gameglobal.rds.loginManager.isGtLogonMode():
            key = gameglobal.rds.loginManager.getProxyKey()
            if key:
                gameglobal.rds.loginManager.tryGtLoginPre(key)
            else:
                gameglobal.rds.loginManager.genProxyKey(self._onGetProxyKey)
        else:
            netWork.reSendPwd(userName, password)
        self.accountLastSyncTime = BigWorld.time()
        stateSafe.startAccountCheck()
        self.sendFeiHuoInfo()
        if gameglobal.rds.gameCode:
            BigWorld.player().base.setClientGameCode(gameglobal.rds.gameCode)

    def sendFeiHuoInfo(self):
        if not hasattr(self, 'playerName'):
            return
        if self.playerName.find('feihuo.163.com') >= 0:
            gameglobal.rds.loginType = gameglobal.GAME_LOGIN_TYPE_FEIHUO
        elif self.playerName.find('yiyou.163.com') >= 0:
            gameglobal.rds.loginType = gameglobal.GAME_LOGIN_TYPE_YIYOU
        elif self.playerName.find('shunwang.163.com') >= 0:
            gameglobal.rds.loginType = gameglobal.GAME_LOGIN_TYPE_SHUNWANG
        else:
            gameglobal.rds.loginType = gameglobal.GAME_LOGIN_TYPE_DEFAULT
        if gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_FEIHUO:
            gameglobal.rds.logLoginState = gameglobal.GAME_FEIHUO_ACCOUNT
        elif gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_YIYOU:
            gameglobal.rds.logLoginState = gameglobal.GAME_YIYOU_ACCOUNT
        elif gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_SHUNWANG:
            gameglobal.rds.logLoginState = gameglobal.GAME_SHUNWANG_ACCOUNT
        else:
            gameglobal.rds.logLoginState = gameglobal.GAME_ACCOUNT
        netWork.sendInfoForLianYun(gameglobal.rds.logLoginState)

    def sendFeiHuoNoCharInfo(self):
        if gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_FEIHUO:
            gameglobal.rds.logLoginState = gameglobal.GAME_FEIHUO_NO_CHARACTOR
        elif gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_YIYOU:
            gameglobal.rds.logLoginState = gameglobal.GAME_YIYOU_NO_CHARACTOR
        elif gameglobal.rds.loginType == gameglobal.GAME_LOGIN_TYPE_SHUNWANG:
            gameglobal.rds.logLoginState = gameglobal.GAME_SHUNWANG_NO_CHARACTOR
        else:
            gameglobal.rds.logLoginState = gameglobal.GAME_NO_CHARACTOR
        netWork.sendInfoForLianYun(gameglobal.rds.logLoginState)

    def _onGetProxyKey(self, key):
        gameglobal.rds.loginManager.tryGtLoginPre(key)

    def characterDetail(self, auth, gbId, name, lv, appearance, physique, signal, spaceNo, chunk, avatarConfig, extra, isHoliday = False):
        gamelog.debug('ypc@ Account characterDetail!')
        restInfo = self.resetPropFlags.get(gbId, {})
        gameglobal.rds.loginManager.onReceiveChar(auth, name, lv, appearance, physique, signal, spaceNo, chunk, avatarConfig, extra, gbId, restInfo, isHoliday)

    def setDefaultCharacter(self, name):
        gameglobal.rds.loginManager.setSelectedChar(name)

    def _updateWindowTitle(self):
        BigWorld.setWindowTitle(0, gameglobal.rds.hostName)

    def checkCharacter(self, msg):
        pass

    def handleKeyEvent(self, isDown, key, mods):
        pass

    def setPrePayFlag(self, prePayGbId):
        self.prePayGbId = prePayGbId

    def showLoginScene(self):
        gameglobal.rds.GameState = gametypes.GS_LOGIN
        gameglobal.rds.loginManager.replyKeyErrorRetry = 0
        BigWorld.enableCameraChange(True)
        gameglobal.rds.loginManager.nextPage()
        gameglobal.rds.loginScene.initCamera()
        gameglobal.rds.ui.characterDetailAdjust.closeTips()
        gameglobal.rds.ui.messageBox.dismissQueue()
        game.endTitleCg(True)
        Sound.changeZone('music/login', '')
        BigWorld.setFxaaSampleQuality(2)
        BigWorld.enableFxaa(True)
        BigWorld.limitForegroundFPS(0)
        BigWorld.worldDrawEnabled(True)
        BigWorld.enableU3DOF(True)
        BigWorld.setZonePriority('hand', gameglobal.LOGINZONE_PRIO)
        game.cancelTick()
        self._updateWindowTitle()
        checkDisableRain()
        game.tickAsyncCore()

    def showPhoneBindBoxOnLogin(self):
        gameglobal.rds.ui.characterDetailAdjust.closeTips()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PHONE_BIND_BOX, True)

    def onNotifyQueueMsg(self, msg, dura):
        gameglobal.rds.ui.playTips.show(msg, dura)

    def confirmRelogOk(self):
        key = gameglobal.rds.loginManager.getProxyKey()
        if key:
            BigWorld.player().base.confirmRelog(1, gameglobal.rds.loginManager.getProxyKey())
        else:
            gameglobal.rds.loginManager.genProxyKey(lambda key: self._confirmRelog(1, key))

    def confirmRelogNotOk(self):
        key = gameglobal.rds.loginManager.getProxyKey()
        if key:
            BigWorld.player().base.confirmRelog(0, gameglobal.rds.loginManager.getProxyKey())
        else:
            gameglobal.rds.loginManager.genProxyKey(lambda key: self._confirmRelog(0, key))

    def _confirmRelog(self, ok, key):
        BigWorld.player().base.confirmRelog(ok, key)

    def _unloadRelogTips(self):
        gameglobal.rds.ui.characterDetailAdjust.closeTips()

    def logCharacterClick(self, roleName):
        characterClickInfo, lastCharacterId, lastHairId, hasSelfAvatar = gameglobal.rds.ui.characterDetailAdjust.getCharacterClickInfo()
        clickDump = cPickle.dumps(characterClickInfo)
        self.base.logCharacterClick(roleName, clickDump, lastCharacterId, lastHairId, hasSelfAvatar)

    def loginReply(self, status, msg):
        gamelog.info('b.e.: PlayerAccount.loginReply:', status, msg)
        if status == self.REPLY_RELOG:
            gameglobal.rds.ui.characterDetailAdjust.closeTips()
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton('确定', self.confirmRelogOk), MBButton('取消', self.confirmRelogNotOk)]
            gameglobal.rds.ui.messageBox.show(True, '', msg, buttons)
            return
        if status == self.REPLY_PROCESSING_RELONG:
            gameglobal.rds.ui.characterDetailAdjust.showTips('正在处理中。。。', 1)
            if msg == 'fast':
                BigWorld.callback(5, self._unloadRelogTips)
            else:
                BigWorld.callback(15, self._unloadRelogTips)
            return
        if status == self.REPLY_CREATE_SUCCESS:
            BigWorld.callback(0.3, Functor(self.returnToCreate, True))
            if gameglobal.rds.GSNumber:
                self.base.activateGSCode(gameglobal.rds.GSNumber, msg)
                gameglobal.rds.GSNumber = ''
            self.logCharacterClick(msg)
            return
        if status == self.REPLY_SERVER_LOADED:
            gameglobal.rds.ui.messageBox.setTipsDesc(msg)
            return
        if status == self.REPLY_KEY_ERROR:
            gameglobal.rds.loginManager.resetProxyKey()
            if gameglobal.rds.loginManager.replyKeyErrorRetry < const.REPLY_KEY_ERROR_RETRY_NUM:
                gamelog.error('reply key error', msg, 'try to re-', msg)
                gameglobal.rds.loginManager.replyKeyErrorRetry += 1
                if msg == 'login':
                    userName = gameglobal.rds.ui.loginWin.userName
                    password = gameglobal.rds.ui.loginWin.md5Pwd
                    netWork.reSendPwd(userName, password)
                elif msg == 'gtLoginPre':
                    gameglobal.rds.loginManager.genProxyKey(self._onGetProxyKey)
                elif msg == 'confirmRelog':
                    self.confirmRelogOk()
                return
            msg = '获取外网IP出错'
        if status == self.REPLY_UNACTIVED:
            gameglobal.rds.ui.characterDetailAdjust.closeTips()
            MBButton = messageBoxProxy.MBButton
            buttons = [MBButton('前往激活', self.confirmActiveAccount), MBButton('以后再说', None)]
            gameglobal.rds.ui.messageBox.show(True, '', msg, buttons, style=uiConst.MSG_BOX_BLUE)
            return
        if status == self.REPLY_RENAME_SUCCESS:
            gbID = gameglobal.rds.loginManager.cache.get('gbID', 0)
            gameglobal.rds.loginManager.updateChange(gbID, {'resetInfo': self.resetPropFlags.get(gbID, {})})
            index = gameglobal.rds.loginManager.gbID2Index(gbID)
            gameglobal.rds.ui.characterDetailAdjust.onCloseNameInput()
            if index >= 0:
                gameglobal.rds.ui.characterCreate.setRoleCharacter(index, gameglobal.rds.loginManager.characterList.getCharacterInfo(index))
                gameglobal.rds.ui.characterCreate.setFocusCharacter(index)
                gameglobal.rds.loginManager.characterList.characterDetail[index]['rename'] = ''
        if status in (self.REPLY_BODYTYPE_SUCCESS, self.REPLY_AVATARCONFIG_SUCCESS, self.REPLY_SCHOOL_TRANSFER_SUCCESS):
            gbID = gameglobal.rds.loginManager.cache.get('gbID', 0)
            index = gameglobal.rds.loginManager.gbID2Index(gbID)
            updateData = {'resetInfo': self.resetPropFlags.get(gbID, {})}
            if status == self.REPLY_SCHOOL_TRANSFER_SUCCESS:
                info = gameglobal.rds.loginManager.characterList.getCharacterOriginalInfo(index)
                resetInfo = info.get('resetInfo', {})
                physique = info.get('physique', None)
                changedSchool = resetInfo.get(gametypes.RESET_PROPERTY_SCHOOL, 0)
                if physique and changedSchool:
                    physique.school = changedSchool
                    updateData['school'] = changedSchool
            gameglobal.rds.loginManager.updateChange(gbID, updateData)
            if index >= 0:
                gameglobal.rds.ui.characterCreate.setRoleCharacter(index, gameglobal.rds.loginManager.characterList.getCharacterInfo(index))
            self.returnToCreate(False)
        if status == self.REPLY_CANCEL_PROP_FLAG:
            gbID = gameglobal.rds.loginManager.cache.get('gbID', 0)
            gameglobal.rds.loginManager.updateChange(gbID, {'resetInfo': self.resetPropFlags.get(gbID, {})})
            index = gameglobal.rds.loginManager.gbID2Index(gbID)
            if index >= 0:
                gameglobal.rds.ui.characterCreate.setFocusCharacter(index)
        if status == self.REPLY_PASSWORD:
            if msg == '同一IP验证口令失败次数超过6次':
                warnMsg = SCD.data.get('ursLoginWarning', "本次登录存在风险，请前往<a href=\'event:https://m.reg.163.com/stable.html?curl=https://m.reg.163.com&product=%s&source=%s&username=%s\'><u><font color=\'#00D7FF\'>id.163.com</font></u></a>修改密码后重新登录")
                warnMsg = warnMsg % ('ty', 'apijg', gameglobal.rds.ui.loginWin.userName)
                gameglobal.rds.ui.messageBox.showMsgBox(warnMsg)
        gamelog.debug('@hjx account#loginReply:', status, msg)
        try:
            if status == self.REPLY_IN_QUEUE:
                gameglobal.rds.ui.messageBox.refreshQueueCnt(int(msg))
                return
        except:
            return

        if msg == '请点[创建角色]创建人物':
            self.showVideo()
        elif msg:
            if gameglobal.rds.ui.characterDetailAdjust.characterNameMed:
                gameglobal.rds.ui.characterDetailAdjust.setErrorMsg(msg)
            else:
                gameglobal.rds.ui.characterDetailAdjust.showTips(msg)

    def clearLoginWin(self):
        gameglobal.rds.ui.loginWin.writeUserInfo()
        gameglobal.rds.ui.loginWin.hide()
        gameglobal.rds.ui.loginSelectServer.hide()

    def showVideo(self):
        self.sendFeiHuoNoCharInfo()
        self.isShowingVideo = True
        self.clearLoginWin()
        self.cgPlayer = cgPlayer.CGPlayer()
        game.cgMovie = self.cgPlayer
        config = {'position': (0, 0, 1.0),
         'w': 2,
         'h': 2,
         'loop': False,
         'callback': self.endVideo,
         'loadCallback': gameglobal.rds.ui.loginWin.clearEffect}
        gameglobal.rds.ui.hideAllUI()
        Sound.enableMusic(False)
        self.cgPlayer.playMovie('xuanren', config)

    def endVideo(self):
        self.isShowingVideo = False
        gameglobal.rds.ui.restoreUI()
        Sound.enableMusic(True)
        self.showBufferedMsg()
        gameglobal.rds.ui.loginWin.enterNewXrjm()
        if game.cgMovie:
            game.cgMovie.endMovie()
            game.cgMovie = None

    def confirmActiveAccount(self):
        url = 'http://ty.163.com/2013/jy/jihuo.html'
        clientcom.openFeedbackUrl(url)

    def returnToCreate(self, isCreateNew = False):
        if gameglobal.rds.loginScene.inAvatarStage():
            gameglobal.rds.loginScene.handleKeyEvent(0, keys.KEY_RIGHTMOUSE, 0, 0)
            gameglobal.rds.ui.characterDetailAdjust.returnToCreate(isCreateNew)

    def clearScene(self):
        if gameglobal.rds.loginScene.inDetailAdjustStage():
            gameglobal.rds.ui.characterDetailAdjust.clearAllCDWidgets()
        gameglobal.rds.loginScene.clearScene()

    def hotfixMD5Send(self, smd5):
        if gameglobal.gHotfixMD5 != smd5:
            self.base.fetchHotfix()

    def onQueryQueuePlace(self, queuePlace):
        gamelog.debug('@hjx queue#onQueryQueueTicket:', self.id, queuePlace)
        gameglobal.rds.ui.messageBox.onQueryQueuePlace(queuePlace)

    def setPublicServer(self, publicServer):
        pass

    def setHostId(self, hostId):
        self.hostId = hostId
        gameglobal.rds.g_serverid = hostId
        protect.nepChooseServer(hostId, gameglobal.rds.hostName)

    def disconnect(self):
        netWork.disconnect()

    def losePhysics(self):
        pass

    def restorePhysics(self):
        pass

    def loseGravity(self):
        pass

    def restoreGravity(self):
        pass

    def overpass(self):
        uiUtils.showWindowEffect()
        gameglobal.rds.sound.playSound(gameglobal.SD_459)

    def updateClientConfig(self, config):
        import gameconfigCommon
        rawConf = gameconfigCommon.convertDataWithCid(cPickle.loads(zlib.decompress(config)))
        gameglobal.resetConfigData()
        gameglobal.rds.configData.update(rawConf)
        gameConfigUtils.updateClientConfigFromAccount(gameglobal.rds.configData)

    def sendPropFlags(self, flags):
        self.resetPropFlags.update(flags)

    def onGetAccountPhone(self, phone):
        gameglobal.rds.ui.messageBox.setDefaultPhone(phone)

    def onSetAccountPhone(self, flag):
        if flag:
            gameglobal.rds.ui.messageBox.gotoThirdPanel()
        else:
            gameglobal.rds.ui.messageBox.gotoFirstPanel()

    def onApplyMessageRemind(self, remind, flag):
        if flag:
            if remind:
                gameglobal.rds.ui.messageBox.gotoThirdPanel()
            else:
                gameglobal.rds.ui.messageBox.gotoFirstPanel()
                gameglobal.rds.ui.messageBox.setAlreadyState(False)
        else:
            gameglobal.rds.ui.messageBox.gotoFirstPanel()
            gameglobal.rds.ui.messageBox.queueMsgBoxId = gameglobal.rds.ui.messageBox.showMsgBox('该手机号今日收取排队短信提醒\n已达上限，无法再预约。')

    def onExceptIp(self, ipInfo1, ipInfo2):
        gamelog.debug('@zqc %s %s' % (ipInfo1, ipInfo2))
        gameglobal.rds.ui.messageBox.showMsgBox('本次登陆地址异常\n上次登陆%s%s\n本次登陆%s%s' % (ipInfo1['province_name'],
         ipInfo1['city_name'],
         ipInfo2['province_name'],
         ipInfo2['city_name']))

    def confirmDeleteWithCoin(self, roleName, coin, mallCash):
        gameglobal.rds.ui.characterCreate.confirmDeleteWithCoin(roleName, coin, mallCash)

    def returnCCToken(self, rc, content):
        if rc == 0:
            gameglobal.rds.ccToken = content.split(' ')[1]
        else:
            gameglobal.rds.ui.systemTips.show('获取登入数据失败，请重启cc')

    def showMsgBoxWithTitle(self, msg, title):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton('确认', None, fastKey=keys.KEY_Y)]
        gameglobal.rds.ui.messageBox.show(True, title, msg, buttons)

    def showMessageBoxAfterVideo(self, msgId, args, title):
        msg = uiUtils.getTextFromGMD(msgId) % args
        if msgId == GMDD.data.RESERVE_SUCC_MSG:
            gameglobal.rds.ui.messageBox.showMsgBox(msg, callback=self.showCharacterPrePay, showTitle=title)
        elif not getattr(self, 'isShowingVideo', False):
            self.showMsgBoxWithTitle(msg, title)
        else:
            if not hasattr(self, 'buffedMsgList'):
                self.buffedMsgList = []
            self.buffedMsgList.append((msg, title))

    def showCharacterPrePay(self):
        if gameglobal.rds.configData.get('isReservationOnlyServer', False) and gameglobal.rds.configData.get('enablePrePayCoin', False):
            characterList = gameglobal.rds.loginManager.characterList
            if len(characterList.characterDetail) > 0 and getattr(BigWorld.player(), 'prePayGbId', 0) <= 0:
                gameglobal.rds.ui.characterPrePay.show()

    def showBufferedMsg(self):
        for msg, title in getattr(self, 'buffedMsgList', []):
            self.showMsgBoxWithTitle(msg, title)

        self.buffedMsgList = []

    def updateUrsPointData(self, commonPoints, commonFPoints, standbyPoints, specialPoints, specialFPoints):
        self.commonPoints = commonPoints + commonFPoints

    def prePaySucc(self, gbId):
        self.prePayGbId = gbId
        gameglobal.rds.ui.characterCreate.updatePreBtnState()

    def checkQuitHoliday(self, gbId):
        gameglobal.rds.ui.holidayMessageBox.show()

    def setServerTimeZone(self, timeZone, zoneName):
        gameglobal.SERVER_TIME_ZONE = timeZone
        gameglobal.SERVER_TIME_ZONE_NAME = zoneName
        setCrontabTimeZone(zoneName)

    def showFeihuoMsg(self):
        pass

    def applyCharCfg(self, avatarCfg, bodyType, sex, nuid):
        gamelog.debug('@fj applyCharCfg', avatarCfg, bodyType, sex, nuid)
        retVal = gametypes.APPLY_CHAR_CFG_NOT_ONLINE
        if gameglobal.rds.loginScene.inAvatarStage():
            player = gameglobal.rds.loginScene.player
            if player and player.physique.sex == sex and player.physique.bodyType == bodyType:
                gameglobal.rds.ui.characterDetailAdjust.applyAvatarConfig(avatarCfg)
                retVal = gametypes.APPLY_CHAR_CFG_SUCC
            else:
                retVal = gametypes.APPLY_CHAR_CFG_BODY_TYPE_ERR
        else:
            retVal = gametypes.APPLY_CHAR_CFG_NOT_IN_NIELIAN
        self.base.onApplyCharCfg(retVal, nuid)

    def uploadNOSFile(self, filePath, fileType, fileSrc, extra, callbackFunc = None, callbackArgs = ()):
        if '.' in filePath.split('/')[-1][:-4]:
            self.showGameMsg(GMDD.data.UPLOAD_PIC_FAIL_BY_INVALIDNAME, ())
            return
        if not hasattr(self, 'nosUploadCallbackCaches'):
            self.nosUploadCallbackCaches = {}
        self.nosUploadCallbackCaches[filePath] = (fileType,
         fileSrc,
         extra,
         callbackFunc,
         callbackArgs)
        self.base.fetchNOSKey(filePath)

    def onFetchNOSKey(self, md5Text, timeStamp, filePath):
        if self.nosUploadCallbackCaches.has_key(filePath):
            fileType, fileSrc, extra, callbackName, callbackArgs = self.nosUploadCallbackCaches.pop(filePath)
        else:
            fileType, fileSrc, extra, callbackName, callbackArgs = (gametypes.NOS_FILE_UNKNOWN,
             None,
             None,
             None,
             None)
        seqTask.addNOSSeqTask(gametypes.NOS_SERVICE_UPLOAD, (md5Text,
         timeStamp,
         filePath,
         fileType,
         fileSrc,
         extra), (callbackName, callbackArgs))

    def onUploadCharCfgData(self, nuid):
        gamelog.debug('onUploadCharCfgData', nuid)
        gameglobal.rds.ui.characterDetailAdjust.showShare(nuid)

    def syncSharedCnt(self, sharedCnt):
        self.sharedCnt = sharedCnt

    def sendStraightLvUpInfo(self, straightLvUpInfo):
        gamelog.debug('bgf@sendStraightLvUpInfo', straightLvUpInfo)
        gameglobal.rds.loginManager.characterList.setStraightLvUpInfo(straightLvUpInfo)

    def onGetRandomName(self, randName):
        gameglobal.rds.ui.characterDetailAdjust.setInputName(randName)

    def onCheckRealNameFailed(self):
        gameglobal.rds.ui.messageBox.showMsgBox(uiUtils.getTextFromGMD(GMDD.data.REAL_NAME_CHECK_FAILED), callback=self._gotoCommitRealName)

    def _gotoCommitRealName(self):
        BigWorld.openUrl(SCD.data.get('realNameWebLink', ''))
        gameglobal.rds.loginManager.onDisconnect()
        BigWorld.callback(1, gameglobal.rds.ui.loginSelectServer.onClickBack)

    def boughtCharacterDetail(self, auth, gbId, name, lv, appearance, physique, signal, spaceNo, chunk, avatarConfig, extra, isHoliday, boughtSeq):
        """
        \xb7\xa2\xcb\xcd\xd2\xd1\xb9\xba\xc2\xf2\xb5\xc4\xbd\xc7\xc9\xab\xd0\xc5\xcf\xa2\xa3\xac\xba\xcdcharacterDetail\xb5\xc4\xb2\xce\xca\xfd\xbd\xe1\xb9\xb9\xcf\xe0\xcd\xac\xa3\xac\xd6\xbb\xca\xc7\xd5\xe2\xb8\xf6\xbd\xc7\xc9\xab\xd4\xdd\xb2\xbb\xca\xf4\xd3\xda\xb8\xc3\xd5\xcb\xbb\xa7\xa3\xac\xbd\xf6\xcc\xe1\xb9\xa9\xd4\xa4\xc0\xc0\xa3\xac\xce\xde\xb7\xa8\xb5\xc7\xc2\xbc\xa3\xac\xd0\xe8\xd2\xaa\xc1\xec\xc8\xa1\xba\xf3\xb2\xc5\xbf\xc9\xb5\xc7\xc2\xbc
        :param auth: \xc0\xed\xc2\xdb\xc9\xcf\xce\xaa const.AUTH_VALID_SELLING\xa3\xac\xc1\xec\xc8\xa1\xba\xf3\xb2\xc5\xbf\xc9\xb5\xc7\xc2\xbc 
        :param gbId: 
        :param name: 
        :param lv: 
        :param appearance: 
        :param physique: 
        :param signal: 
        :param spaceNo: 
        :param avatarConfig: 
        :param extra: 
        :param isHoliday:
        :param boughtSeq: \xb9\xba\xc2\xf2\xcb\xb3\xd0\xf2\xa3\xac\xca\xfd\xd4\xbd\xb4\xf3\xd4\xbd\xd0\xc2
        """
        if not hasattr(self, 'boughtCharacterData'):
            self.boughtCharacterData = {}
        boughtCharacterData = {'auth': auth,
         'gbId': gbId,
         'name': name,
         'lv': lv,
         'appearance': appearance,
         'physique': physique,
         'signal': signal,
         'spaceNo': spaceNo,
         'chunk': chunk,
         'avatarConfig': avatarConfig,
         'extra': extra,
         'isHoliday': isHoliday,
         'boughtSeq': boughtSeq}
        gamelog.debug('ypc@ error boughtCharacterDetail!', boughtCharacterData)
        self._updateBoughtCharacterDetail(gbId, boughtCharacterData)

    def onTakeBackCbgCharacter(self, auth, gbId):
        """
        \xc2\xf4\xbc\xd2\xca\xd5\xbb\xd8\xd5\xfd\xd4\xda\xb3\xf6\xca\xdb\xb5\xc4\xbd\xc7\xc9\xab
        \xb8\xc3\xbd\xc7\xc9\xab\xd4\xda\xd5\xe6\xd5\xfd\xca\xdb\xb3\xf6\xd6\xae\xc7\xb0\xa3\xac\xc8\xd4\xca\xf4\xd3\xda\xb8\xc3\xd5\xcb\xbb\xa7\xa3\xac\xcb\xf9\xd2\xd4\xca\xc7\xcd\xa8\xb9\xfdcharacterDetail\xb7\xa2\xcb\xcd\xb5\xc4
        :param auth: \xbf\xcd\xbb\xa7\xb6\xcb\xd0\xe8\xcd\xac\xb2\xbd\xd0\xde\xb8\xc4\xd6\xb8\xb6\xa8\xbd\xc7\xc9\xab\xb7\xe2\xbd\xfb\xd7\xb4\xcc\xac\xce\xaaauth\xa3\xac\xc0\xed\xc2\xdb\xc9\xcf\xb7\xa2\xc0\xb4\xb5\xc4\xce\xaaconst.AUTH_VALID_PERMIT 
        :param gbId: \xd6\xb8\xb6\xa8\xb5\xc4\xbd\xc7\xc9\xab\xa3\xac\xca\xc7\xd5\xfd\xd4\xda\xb3\xf6\xca\xdb\xd6\xd0\xb5\xc4\xbd\xc7\xc9\xab
        """
        gamelog.debug('ypc@ onTakeBackCbgCharacter!')
        gameglobal.rds.loginManager.onUpdateCharacterAuth(gbId, auth)

    def onTakeAwayCbgCharacter(self, auth, gbId):
        """
        \xc2\xf2\xbc\xd2\xc1\xec\xc8\xa1\xc2\xf2\xb5\xbd\xb5\xc4\xbd\xc7\xc9\xab
        \xb8\xc3\xbd\xc7\xc9\xab\xd4\xda\xd5\xe6\xd5\xfd\xc1\xec\xc8\xa1\xd6\xae\xc7\xb0\xa3\xac\xb2\xbb\xca\xf4\xd3\xda\xb8\xc3\xd5\xcb\xbb\xa7\xa3\xac\xcb\xf9\xd2\xd4\xca\xc7\xcd\xa8\xb9\xfdbuyCharacterDetail\xb7\xa2\xcb\xcd\xb5\xc4
        :param auth: \xbf\xcd\xbb\xa7\xb6\xcb\xd0\xe8\xcd\xac\xb2\xbd\xd0\xde\xb8\xc4\xd6\xb8\xb6\xa8\xbd\xc7\xc9\xab\xb7\xe2\xbd\xfb\xd7\xb4\xcc\xac\xce\xaaauth\xa3\xac\xc0\xed\xc2\xdb\xc9\xcf\xb7\xa2\xc0\xb4\xb5\xc4\xce\xaaconst.AUTH_VALID_PERMIT 
        :param gbId: \xd6\xb8\xb6\xa8\xb5\xc4\xbd\xc7\xc9\xab\xa3\xac\xca\xc7\xd2\xd1\xb9\xba\xc2\xf2\xb5\xc4\xbd\xc7\xc9\xab
        """
        self._updateBoughtCharacterDetail(gbId, None)

    def onTakeAwayCbgCharacterFail(self, gbId):
        gameglobal.rds.ui.characterDetailAdjust.showTips('领取购买角色失败！')

    def onTakeBackCbgCharacterWhenNotOpOnCBGWeb(self):
        msg = gameStrings.CBG_ROLE_WARNING_NEED_GOTO_WEB
        gameglobal.rds.ui.characterDetailAdjust.showTips(msg)

    def _updateBoughtCharacterDetail(self, gbId, data):
        if not hasattr(self, 'boughtCharacterData'):
            return
        if gbId:
            if data:
                self.boughtCharacterData[gbId] = data
            elif gbId in self.boughtCharacterData:
                self.boughtCharacterData.pop(gbId)
        gameglobal.rds.ui.characterCreate.onShowBoughtCharacter()

    def onAvatarBeTakeAway(self, gbId, roleName):
        gameglobal.rds.ui.characterDetailAdjust.showTips('您出售的角色 %s 已被领取' % (roleName,))
