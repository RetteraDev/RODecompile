#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client/netWork.o
from gamestrings import gameStrings
import time
import httplib
import urllib
import traceback
import BigWorld
import C_ui
import Math
import ResMgr
import const
import gamelog
import game
import clientcom
import gameglobal
import gametypes
import utils
from appearance import Appearance
from appSetting import Obj as AppSettings
from guis import uiConst
from helpers import loadingProgress
from helpers import pyBgTask
from callbackHelper import Functor

class LoginParams(object):

    def __init__(self, userName, passwold, inactivityTimeout):
        self.username = userName
        self.password = passwold
        self.inactivityTimeout = inactivityTimeout


def initOffline():
    gameglobal.rds.loginScene.clearScene()
    gameglobal.rds.GameState = gametypes.GS_PLAYGAME
    spaceID = BigWorld.createSpace()
    gameglobal.rds.clientSpace = spaceID
    gameglobal.rds.isSinglePlayer = True
    gameglobal.rds.school = const.SCHOOL_YUXU
    BigWorld.worldDrawEnabled(True)
    game.endTitleCg(True)
    if hasattr(BigWorld, 'bigMapEnabled'):
        BigWorld.bigMapEnabled(False)
    try:
        uv = gameglobal.rds.configSect.readString('universe/name')
        dirInfo = ResMgr.openSection('universes/' + uv + '/universe.settings')
        if dirInfo:
            dir = dirInfo.keys()[0]
        else:
            dir = 'fb_jjc'
        spaceName = 'universes/' + uv + '/' + dir
        posSect = ResMgr.openSection(spaceName + '/space.settings/startPosition')
        if not posSect:
            posSect = ResMgr.openSection(spaceName + '/space.localsettings/startPosition')
        if posSect is None:
            pos = Math.Vector3(0, 0, 0)
        else:
            pos = posSect.asVector3
        faceDirSect = ResMgr.openSection(spaceName + '/space.settings/startDirection')
        if not faceDirSect:
            faceDirSect = ResMgr.openSection(spaceName + '/space.localsettings/startDirection')
        if faceDirSect is None:
            faceDir = Math.Vector3(1, 0, 0)
        else:
            faceDir = faceDirSect.asVector3
    except:
        gamelog.error('zf:Error:read config section for universes')
        traceback.print_exc()
        return

    if spaceID != None:
        gameglobal.rds.clientSpaceMapping = BigWorld.addSpaceGeometryMapping(spaceID, None, 'universes/eg/' + dir)
    aspect = Appearance(dict())
    playerID = BigWorld.createEntity('Avatar', spaceID, 0, pos, faceDir, {'camp': 1,
     'aspect': aspect})
    BigWorld.player(BigWorld.entities.get(playerID))


def enterNewXrjm():
    BigWorld.callback(1, _initArtOffline)


def initArtOffline():
    _initArtOffline()


def _initArtOffline():
    gameglobal.rds.loginManager.setGtLogonMode(False)
    BigWorld.createEntity('Account', gameglobal.rds.loginScene.spaceID, 0, (0, 0, 0), (0, 0, 0), {})
    gameglobal.rds.isSinglePlayer = False
    gameglobal.rds.applyOfflineCharShowData = True
    uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST = uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST_NEW
    gameglobal.rds.GameState = gametypes.GS_LOGIN
    gameglobal.rds.loginScene.initCamera()
    gameglobal.rds.loginScene.clearPlayer()
    BigWorld.worldDrawEnabled(True)
    if hasattr(BigWorld, 'bigMapEnabled'):
        BigWorld.bigMapEnabled(False)
    game.endTitleCg(True)
    gameglobal.rds.ui.characterCreate.gotoCharacterSelectZero()


def initOnline(userName):
    gameglobal.rds.isSinglePlayer = False
    if gameglobal.rds.loginManager.isGtLogonMode():
        hostIP = gameglobal.rds.loginManager.hostIP()
        hostName = gameglobal.rds.loginManager.titleName()
        saveHost(hostName, 0)
    else:
        hostIP = gameglobal.rds.configSect.readString('login/host')
        hostName = gameglobal.rds.configSect.readString('login/hostname')
    gameglobal.rds.clientInfo.proxy = gameglobal.rds.loginManager.proxyVendor()
    gameglobal.rds.clientInfo.net_vendor = gameglobal.rds.loginManager.netVendor()
    gameglobal.rds.loginUserName = None
    gameglobal.rds.loginUserPassword = None
    gameglobal.rds.loginHostIp = hostIP
    gameglobal.rds.gbId = 0
    gameglobal.rds.hostName = hostName
    disconnect(Functor(loginHostReally, userName, hostIP))


def isRecheckKeyValid():
    try:
        return 0 < utils.getNow() - int(gameglobal.rds.loginManager.reCheckKey[32:]) < 150
    except:
        return False


def onConnect(stage, status, err, userName):
    gamelog.debug('jorsef: connect call back info:', stage, status, err, userName, BigWorld.player())
    gameglobal.rds.ui.loginSelectServer.releaseLockServer()
    if stage == 1 and status <= 0:
        if status == -69:
            if BigWorld.isPublishedVersion():
                gameglobal.rds.ui.characterDetailAdjust.showTips(gameStrings.TEXT_NETWORK_138)
            else:
                gameglobal.rds.ui.characterDetailAdjust.showTips(gameStrings.TEXT_NETWORK_140)
        elif status == -68:
            gameglobal.rds.ui.characterDetailAdjust.showTips(gameStrings.TEXT_NETWORK_142)
            if hasattr(gameglobal.rds, 'reTryLoginOnTransferTimer') and gameglobal.rds.reTryLoginOnTransferTimer:
                BigWorld.cancelCallback(gameglobal.rds.reTryLoginOnTransferTimer)
                gameglobal.rds.reTryLoginOnTransferTimer = 0
            if hasattr(gameglobal.rds, 'transServerInfo') and gameglobal.rds.transServerInfo and gameglobal.rds.reTryLoginOnTransferCnt < 10:
                gameglobal.rds.reTryLoginOnTransferTimer = BigWorld.callback(3, reTryLoginOnTransfer)
        elif status == -2:
            gameglobal.rds.ui.characterDetailAdjust.showTips(gameStrings.TEXT_NETWORK_149)
        elif status in (-11, -12):
            gameglobal.rds.ui.characterDetailAdjust.showTips(gameStrings.TEXT_NETWORK_151)
        elif status in (-76, -77, -80, -81, -82):
            gameglobal.rds.ui.characterDetailAdjust.showTips(gameStrings.TEXT_NETWORK_156)
        else:
            gameglobal.rds.ui.characterDetailAdjust.showTips(gameStrings.TEXT_NETWORK_158)
    elif stage == 1 and status == 1:
        gamelog.debug('Logon: connected to server, still waiting for data transmition')
        gameglobal.rds.offline = False
    elif stage == 1 and status == -69:
        if BigWorld.isPublishedVersion():
            gameglobal.rds.ui.chat.addMessage(str(const.CHAT_CHANNEL_WORLD), gameStrings.TEXT_NETWORK_138, 'sys')
        else:
            gameglobal.rds.ui.chat.addMessage(str(const.CHAT_CHANNEL_WORLD), gameStrings.TEXT_NETWORK_166, 'sys')
    else:
        if stage == 2:
            gamelog.debug('Logon: got first packet, Status:', status)
            return
        if stage == 6:
            gamelog.debug('server temporarily down')
            if gameglobal.rds.needSendInfoToHttp:
                sendInfoToHttp(status, userName)
            if status == 1:
                onDisconnected()
            else:
                gameglobal.rds.ui.characterDetailAdjust.showTips(gameStrings.TEXT_NETWORK_158)
        else:
            gameglobal.rds.ui.characterDetailAdjust.showTips(gameStrings.TEXT_NETWORK_158)


def sendGadInfo(urs, macAddr):
    if not BigWorld.isPublishedVersion():
        return
    if hasattr(gameglobal.rds, 'transServerInfo') and gameglobal.rds.transServerInfo:
        return
    mgr = pyBgTask.getMgr()
    mgr.add_task(doRealSendGadInfo, (urs, macAddr))


def doRealSendGadInfo(urs, macAddr):
    url = 'gad.netease.com'
    p = {'urs': urs,
     'mac': macAddr}
    params = urllib.urlencode(p)
    try:
        conn = httplib.HTTPConnection(url)
        conn.request('GET', '/gad/point?point_id=1797&s=vzmRbbJIWJXxkPh0nGV46UvsPpc%3D&' + params)
        gamelog.debug('m.l@sendGadInfo', '/gad/point?point_id=1797&s=vzmRbbJIWJXxkPh0nGV46UvsPpc%3D&' + params)
        r = conn.getresponse()
        conn.close()
    except:
        pass


def sendInfoToHttp(status, userName):
    return
    if not BigWorld.isPublishedVersion():
        return
    if hasattr(gameglobal.rds, 'transServerInfo') and gameglobal.rds.transServerInfo:
        return
    mgr = pyBgTask.getMgr()
    mgr.add_task(doRealSendInfoToHttp, (status, userName))


def doRealSendInfoToHttp(status, userName):
    gameglobal.rds.needSendInfoToHttp = False
    player = BigWorld.player()
    if player:
        p = {'time': str(int(time.time())),
         'x': player.position[0],
         'y': player.position[1],
         'z': player.position[2],
         'latency': str(player.latency),
         'gbID': player.gbId,
         'mapID': player.mapID,
         'urs': userName,
         'roleName': player.roleName,
         'status': status,
         'serverName': gameglobal.rds.loginManager.titleName()}
        params = urllib.urlencode(p)
        try:
            serverId = utils.getHostId()
            if serverId >= 10000 and serverId <= 30000:
                conn = httplib.HTTPConnection('106.2.48.8:13480')
            else:
                conn = httplib.HTTPConnection('pgpp-util02.i.nease.net:13480')
            conn.request('GET', '/stat01?' + params)
            r = conn.getresponse()
            if r.status != 200:
                return
            conn.close()
        except:
            pass


def onDisconnectedCallBack():
    gameglobal.rds.disconnectCB()
    gameglobal.rds.disconnectCB = None


def getServerIPByName(serverName):
    serverInfo = gameglobal.rds.loginManager.srvDict.findByName(serverName)
    if serverInfo:
        zone, idx = serverInfo
        entry = gameglobal.rds.loginManager.srvDict.item[zone][idx]
        locale = int(entry.locale)
        if locale == 3:
            locale = 0
        return entry.ip[locale]
    return ''


def getServerIPListByName(serverName):
    serverInfo = gameglobal.rds.loginManager.srvDict.findByName(serverName)
    if serverInfo:
        zone, idx = serverInfo
        entry = gameglobal.rds.loginManager.srvDict.item[zone][idx]
        return entry.ip
    return []


def transferServerLogin():
    if hasattr(gameglobal.rds, 'transServerInfo') and gameglobal.rds.transServerInfo:
        fromHostId, toHostId, roleName, password, transType = gameglobal.rds.transServerInfo[2]
        toHostId = gameglobal.rds.transServerInfo[0]
        userName = gameglobal.rds.transServerInfo[1]
        toServerName = utils.getServerName(toHostId)
        hostIP = getServerIPByName(toServerName)
        hostIpList = getServerIPListByName(toServerName)
        gamelog.info('zt: transfer', fromHostId, toHostId, userName, password, transType, hostIP)
        if hostIP:
            gameglobal.rds.loginManager.disconnectFromGame()
            loginHostReally(userName, hostIP, hostIpList)
            gameglobal.KEEP_HIDE_MODE_CUSTOM = True
            game.clearAll(False, True)
        return


def onDisconnected():
    gamelog.debug('jjh@netWork onDisconnected ', gameglobal.rds.loginUserName)
    if gameglobal.rds.loginUserName and gameglobal.rds.gbId:
        from helpers import protect
        protect.nepRoleLogout(gameglobal.rds.loginUserName, gameglobal.rds.gbId)
    gameglobal.rds.offline = True
    if hasattr(gameglobal.rds, 'transServerInfo') and gameglobal.rds.transServerInfo:
        transferServerLogin()
        return
    gamelog.debug('zs: connect gamestate', gameglobal.rds.GameState)
    if gameglobal.rds.GameState != gametypes.GS_START and gameglobal.rds.GameState != gametypes.GS_CONNECT:
        game.clearAll(False)
        BigWorld.worldDrawEnabled(False)
        BigWorld.endGrayFilter(1)
        disconnectStr = ''
        if hasattr(gameglobal.rds, 'relogStr') and gameglobal.rds.relogStr:
            disconnectStr += gameglobal.rds.relogStr
            gameglobal.rds.relogStr = ''
        disconnectStr += gameStrings.TEXT_NETWORK_316
        gameglobal.rds.ui.characterDetailAdjust.showTips(disconnectStr, 1)
        delayTime = 8.0
        if gameglobal.rds.GameState == gametypes.GS_LOADING:
            C_ui.cursor_show(True)
            loadingProgress.instance().onProgressEnd()
        elif gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            BigWorld.resetEntityManager()
        BigWorld.callback(delayTime, Functor(game.clearAll, True, False, False))
    game.tick()
    gameglobal.rds.GameState = gametypes.GS_START
    gameglobal.rds.loginUserName = None
    gameglobal.rds.loginUserPassword = None
    gameglobal.rds.loginHostIp = None
    gameglobal.rds.gbId = 0
    gameglobal.rds.loginManager.resetProxyKey()
    BigWorld.setWindowTitle(0, '')
    BigWorld.setWindowTitle(1, '')
    BigWorld.setWindowTitle(2, '')
    BigWorld.setWindowTitle(3, '')
    if gameglobal.rds.disconnectCB != None:
        BigWorld.callback(0.2, onDisconnectedCallBack)
        return
    else:
        return


def loginHostReally(userName, host, hostIps = None):
    loginManager = gameglobal.rds.loginManager
    gameglobal.rds.hostName = loginManager.titleName()
    loginParams = LoginParams(userName, loginManager.reCheckKey, 20)
    realHost = host
    hostIps = hostIps or loginManager.hostIPS()
    if loginManager.isGtLogonMode():
        if loginManager.proxyVendor():
            if loginManager.isEduNet():
                realHost = hostIps[2]
            else:
                idx = min(loginManager.netVendor() - 1, len(hostIps) - 1)
                realHost = hostIps[idx]
            ip = realHost.split(':')[0]
            if ip == '':
                ip = '0.0.0.0'
            gamelog.debug('@zhp: loginHostReally need proxy', ip)
            BigWorld.setProxy(ip)
        else:
            gamelog.debug('@zhp: loginHostReally NOT NEED proxy')
            BigWorld.setProxy('0.0.0.0')
            idx = min(loginManager.netVendor() - 1, len(hostIps) - 1)
            realHost = hostIps[idx]
    gamelog.debug('jorsef: loginHostReally called: ', userName, realHost, loginManager.netVendor())
    gameglobal.rds.loginScene.clearSpaceAndPlayer()
    BigWorld.connect(realHost, loginParams, lambda state, step, err = '', userName = userName: onConnect(state, step, err, userName))


def saveHost(hostName, vendor):
    AppSettings['conf/lastServer/serv'] = hostName
    AppSettings['conf/lastServer/netverdor'] = vendor
    AppSettings.save()


def disconnect(callback = None):
    if gameglobal.rds.offline:
        if callback:
            callback()
        return
    gameglobal.rds.disconnectCB = callback
    gameglobal.rds.hostName = ''
    BigWorld.setWindowTitle(0, gameglobal.rds.hostName)
    BigWorld.setWindowTitle(1, '')
    BigWorld.setWindowTitle(2, '')
    BigWorld.setWindowTitle(3, '')
    BigWorld.disconnect()


def reTransfer():
    gamelog.debug('connect reTransfer...', gameglobal.rds.transServerInfo)
    if hasattr(gameglobal.rds, 'reTransferCallback'):
        del gameglobal.rds.reTransferCallback
    if gameglobal.rds.transServerInfo:
        gameglobal.rds.transferCount += 1
        if gameglobal.rds.transferCount < 10:
            gameglobal.rds.reTransferCallback = BigWorld.callback(10, reTransfer)
        else:
            gameglobal.rds.transferCount = 0
        game.onQuit(isCrossServer=True)
        BigWorld.disconnect()


def transferServer(hostId, account, info):
    gamelog.debug('zt:game.transferServer', hostId, account, info)
    gameglobal.rds.transServerInfo = (hostId, account, info)
    game.onQuit(isCrossServer=True)
    BigWorld.disconnect()
    loadingProgress.instance().show(True, 'ycdg', True)
    gameglobal.rds.transferCount = 0
    if hasattr(gameglobal.rds, 'reTransferCallback'):
        BigWorld.cancelCallback(gameglobal.rds.reTransferCallback)
    gameglobal.rds.reTransferCallback = BigWorld.callback(10, reTransfer)


def reTryLoginOnTransfer():
    transferServerLogin()
    gameglobal.rds.reTryLoginOnTransferCnt += 1


def reSendPwd(userName, password):
    if userName == gameglobal.rds.loginUserName:
        key = gameglobal.rds.loginManager.getProxyKey()
        if key:
            BigWorld.player().base.login(password, key, clientcom.CLIENT_REVISION, gameglobal.rds.clientInfo)
        else:
            gameglobal.rds.loginManager.genProxyKey(lambda key: _onGetProxyKey(password, key))
    else:
        disconnect(Functor(initOnline, userName))


def _onGetProxyKey(password, key):
    if BigWorld.player() and BigWorld.player().__class__.__name__ == 'PlayerAccount':
        BigWorld.player().base.login(password, key, clientcom.CLIENT_REVISION, gameglobal.rds.clientInfo)


def sendInfoForLianYun(status, isClose = False):
    if not BigWorld.isPublishedVersion():
        return
    if not gameglobal.rds.configData.get('enableLianYunStatistisc', False):
        return
    mgr = pyBgTask.getMgr()
    mgr.add_task(realSendInfoForLianYun, (status, isClose))


def realSendInfoForLianYun(status, isClose):
    if gameglobal.rds.isFeiHuo:
        ver = '4.0.1'
    elif gameglobal.rds.isYiYou:
        ver = '4.0.3'
    elif gameglobal.rds.isShunWang:
        ver = '4.0.4'
    else:
        ver = '4.0.2'
    if hasattr(gameglobal.rds, 'transServerInfo') and gameglobal.rds.transServerInfo:
        return
    if isClose:
        status += 1
    if gameglobal.GAME_LOG_STATE.has_key(status):
        if gameglobal.GAME_LOG_STATE[status]:
            return
    gameglobal.GAME_LOG_STATE[status] = False
    p = {'v': ver,
     'code': str(gameglobal.rds.gameCode),
     'type': str(status),
     'computer': str(gameglobal.rds.macaddrs),
     'time': time.strftime('%Y-%m-%d-%H-%M-%S')}
    params = urllib.urlencode(p)
    try:
        conn = httplib.HTTPConnection('hd.tianyu.163.com')
        conn.request('GET', '/dlstat?' + params)
        r = conn.getresponse()
        if r.status != 200:
            return
        gameglobal.GAME_LOG_STATE[status] = True
        gamelog.debug('sendInfoForLianYun:', r.status, status, str(p), gameglobal.GAME_LOG_STATE[status], ver)
        conn.close()
    except:
        gameglobal.GAME_LOG_STATE[status] = False
