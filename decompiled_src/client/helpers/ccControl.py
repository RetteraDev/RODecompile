#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/ccControl.o
import hashlib
import urllib
import json
import time
import BigWorld
import gameglobal
import gamelog
import const
import remoteInterface
import formula
from gameclass import Singleton
from guis.ui import gbk2unicode
from guis.ui import unicode2gbk
from helpers.cc import isCCUpdating
from guis import hotkey
from guis import hotkeyProxy
from guis import ui
from data import school_data as SD
from cdata import game_msg_def_data as GMDD
KEY = 2855688680L
GAME_ID = 21
CLIENT_TYPE = 1
URL_PREFIX = 'http://114.113.200.183:8282/login/game_token'
gDisAbleCCBox = False

def loadMicCard(channelId):
    if getattr(gameglobal.rds, 'micCardPath', None):
        showMicCard(gameglobal.rds.micCardPath)
    else:
        remoteInterface.getMicCardInfo(channelId, _fetchMicCardInfo)


def _fetchMicCardInfo(data):
    gamelog.debug('_fetchMicCardInfo', data)
    if data:
        data = json.loads(data)
        gameglobal.rds.micCardRetCode = data.get('retcode', -1)
        urlPicture = data.get('usermiccard', None)
        remoteInterface.downloadMicCardFromCC(urlPicture, showMicCard)
    else:
        gameglobal.rds.micCardRetCode = -1


def showMicCard(fileName):
    fileName = unicode2gbk(fileName)
    gameglobal.rds.micCardPath = fileName
    fileName = '../%s/' % const.IMAGES_DOWNLOAD_DIR + fileName
    gameglobal.rds.ui.messageBox.showMicCard(fileName)


def httpGetInfo(configkey, roleId, configUrs, gameId, clientType, urlPrefix):
    """
    roleid : [\xb1\xd8\xcc\xee] \xd3\xce\xcf\xb7\xbd\xc7\xc9\xab\xb5\xc4id\xa3\xac\xca\xc7\xd2\xbb\xb8\xf6INT\xd0\xcd\xd5\xfb\xca\xfd
    urs : [\xb1\xd8\xcc\xee] \xd5\xca\xba\xc5\xb5\xc4urs
    gameid : [\xb1\xd8\xcc\xee] \xd3\xce\xcf\xb7\xb5\xc4id\xa3\xac\xca\xc7\xd2\xbb\xb8\xf6INT\xd0\xcd\xd5\xfb\xca\xfd
    ts: [\xb1\xd8\xcc\xee] utc\xb5\xc4\xca\xb1\xbc\xe4\xa3\xa8\xb8\xf1\xca\xbd\xa3\xba20141208023018\xa3\xa9
    clienttype: [\xb1\xd8\xcc\xee] \xbf\xcd\xbb\xa7\xb6\xcb\xc0\xe0\xd0\xcd\xa3\xac\xca\xc7\xd2\xbb\xb8\xf6INT\xd0\xcd\xd5\xfb\xca\xfd
    sign: [\xb1\xd8\xcc\xee] \xb2\xce\xca\xfd\xb5\xc4md5\xc7\xa9\xc3\xfb
    """
    key = configkey
    role_id = roleId
    urs = configUrs
    game_id = gameId
    client_type = clientType
    url_prefix = urlPrefix
    ts = time.strftime('%Y%m%d%H%M%S')
    login_args = (key,
     role_id,
     urs,
     game_id,
     ts,
     client_type)
    sign = hashlib.md5(''.join(map(str, login_args))).hexdigest()
    info = {'roleid': role_id,
     'urs': urs,
     'gameid': game_id,
     'ts': ts,
     'clienttype': client_type,
     'sign': sign}
    try:
        url = '%s?%s' % (url_prefix, urllib.urlencode(info))
        fd = urllib.urlopen(url)
        res = fd.read()
        fd.close()
    except:
        return False

    return res


def getCCLoginInfo(configkey, roleId, configUrs, gameId, clientType, urlPrefix):
    httpInfo = httpGetInfo(configkey, roleId, configUrs, gameId, clientType, urlPrefix)
    try:
        loginInfo = json.loads(httpInfo)
        loginInfo['role_id'] = roleId
        loginInfo['client_type'] = clientType
        loginInfo['client_key'] = configkey
        return json.dumps(loginInfo)
    except:
        return ''


def testGetCCLoginInfo():
    p = BigWorld.player()
    URS = p.roleURS
    ROLE_ID = str(p.gbId)
    loginCC = getCCLoginInfo(KEY, ROLE_ID, URS, GAME_ID, CLIENT_TYPE, URL_PREFIX)
    return loginCC


def startCC():
    if formula.inDotaBattleField(BigWorld.player().mapID):
        return False
    if not gameglobal.rds.configData.get('enableCCBox', False):
        return False
    p = BigWorld.player()
    if isCCUpdating():
        p.showGameMsg(GMDD.data.COMMON_MSG, ('cc\xd5\xfd\xd4\xda\xb8\xfc\xd0\xc2\xd6\xd0\xa3\xac\xc7\xeb\xc9\xd4\xba\xf3\xd4\xd9\xca\xd4',))
        return False
    if not getattr(gameglobal.rds, 'ccBox', None):
        gameglobal.rds.ccBox = BigWorld.PyCCBox()
    gameglobal.rds.ccBox.runCCBoxApp()
    tickCCResult()


def closeCC():
    p = BigWorld.player()
    if p.groupNUID > 0:
        leaveTeam(str(p.groupNUID))
    if getattr(gameglobal.rds, 'ccBox', None):
        gameglobal.rds.ccBox.closeCCBox()
        gameglobal.rds.ccBox = None


def isCCRunning():
    if not getattr(gameglobal.rds, 'ccBox', None):
        return False
    return gameglobal.rds.ccBox.isRunning()


ccResultHandle = None

def tickCCResult():
    global ccResultHandle
    if ccResultHandle:
        BigWorld.cancelCallback(ccResultHandle)
        ccResultHandle = None
    if not getattr(gameglobal.rds, 'ccBox', None):
        return
    ret = gameglobal.rds.ccBox.getJsonData()
    if ret:
        cmdResult = json.JSONDecoder().decode(ret)
        parseCCCommond(cmdResult)
    ccResultHandle = BigWorld.callback(0.1, tickCCResult)


def parseCCCommond(cmdResult):
    ccBoxCmdParseManager.paraseCommand(cmdResult)
    gamelog.debug('parseCCCommond', cmdResult)


def initCCGameData():
    p = BigWorld.player()
    roleName = p.realRoleName
    initDict = {'type': 'init-game-data',
     'nick': gbk2unicode(roleName),
     'menpai_name': gbk2unicode(SD.data[p.school]['name']),
     'level': p.lv}
    ccBoxCmd(initDict)


def initCCLoginData():
    loginDict = {'type': 'login',
     'login_info': testGetCCLoginInfo()}
    ccBoxCmd(loginDict)


def initCCLoginDataFromServer(data):
    loginDict = {'type': 'login',
     'login_info': data}
    ccBoxCmd(loginDict)


def initCCBoxInfo(content, extra):
    loginInfo = json.loads(content)
    loginInfo.update(extra)
    dump = json.dumps(loginInfo)
    initCCLoginDataFromServer(dump)
    initCCGameData()
    if not hasattr(gameglobal.rds, 'tutorial'):
        return
    gameglobal.rds.tutorial.onGetStartCCBox()


def ccBoxCmd(cmdDict):
    if not cmdDict:
        return
    if not gameglobal.rds.configData.get('enableCCBox', False):
        return
    cmdData = json.JSONEncoder().encode(cmdDict)
    if getattr(gameglobal.rds, 'ccBox', None):
        ret = gameglobal.rds.ccBox.control(cmdData, 0)
        gamelog.debug('ccBoxCmd', cmdDict, ret)


def joinTeam(teamName, teamType = const.CC_GROUP_TYPE_TEAM):
    enableZhanChangCC = gameglobal.rds.configData.get('enableZhanChangCC', False)
    if not enableZhanChangCC and teamType == const.CC_GROUP_TYPE_ZHANCHANG:
        return
    if not enableZhanChangCC:
        teamType = 4
        teamNameType = 'team'
    else:
        teamNameType = 'name'
    if not isCCRunning():
        if gameglobal.JOIN_TEAM_OPEN_CC and teamType == const.CC_GROUP_TYPE_TEAM or gameglobal.JOIN_ZHANCHANG_OPEN_CC and teamType == const.CC_GROUP_TYPE_ZHANCHANG:
            startCC()
            return
    joinDict = {'type': 'change-group',
     'group_type': teamType,
     'is_join': 1,
     teamNameType: teamName}
    ccBoxCmd(joinDict)


def leaveTeam(teamName, teamType = const.CC_GROUP_TYPE_TEAM):
    enableZhanChangCC = gameglobal.rds.configData.get('enableZhanChangCC', False)
    if not enableZhanChangCC and teamType == const.CC_GROUP_TYPE_ZHANCHANG:
        return
    if not enableZhanChangCC:
        teamType = 4
        teamNameType = 'team'
    else:
        teamNameType = 'name'
    joinDict = {'type': 'change-group',
     'group_type': teamType,
     'is_join': 0,
     teamNameType: teamName}
    ccBoxCmd(joinDict)


def closeForm():
    joinDict = {'type': 'close-one-form'}
    ccBoxCmd(joinDict)


def startInnerCC(rid, cid):
    joinDict = {'type': 'start-cc',
     'rid': rid,
     'cid': cid}
    ccBoxCmd(joinDict)


def setCCVisible(value = 1):
    joinDict = {'type': 'set-all-visible',
     'visible': value}
    ccBoxCmd(joinDict)


def enableQuitConfirm(value = 1):
    joinDict = {'type': 'enable-quit-confirm',
     'enable': value}
    ccBoxCmd(joinDict)


def expandMaintool(value = 1):
    joinDict = {'type': 'expand-maintool',
     'is_expanded': value}
    ccBoxCmd(joinDict)


def toggle():
    if not gameglobal.rds.configData.get('enableCCBox', False):
        return False
    if isCCRunning():
        closeCC()
    else:
        startCCInterval()
    return True


@ui.callFilter(1)
def startCCInterval():
    startCC()


class CommandUnit(object):

    def __init__(self, cmdType):
        super(CommandUnit, self).__init__()
        self.cmdType = cmdType

    def use(self, cmdResult):
        pass


class ParseStartUp(CommandUnit):

    def use(self, cmdResult):
        isSu = cmdResult.get('is_suc', False)
        if isSu:
            p = BigWorld.player()
            p.tryLoginCCBox()


class ParseCloseResult(CommandUnit):

    def use(self, cmdResult):
        result = cmdResult.get('result', False)
        if result == 0:
            closeCC()


class ParseShareRoom(CommandUnit):

    def use(self, cmdResult):
        rid = str(cmdResult.get('rid'))
        if cmdResult.has_key('cid'):
            rid += '-0'
        p = BigWorld.player()
        p.doSendLink(p.realRoleName, rid, False, 0, const.CC_OFFICAL_ROOM)


class ParseFormCount(CommandUnit):

    def __init__(self, cmdType):
        super(ParseFormCount, self).__init__(cmdType)
        self.formCount = 0

    def use(self, cmdResult):
        self.formCount = cmdResult.get('count', 0)

    def closeForm(self):
        if self.formCount:
            closeForm()

    def isFormOpen(self):
        return self.formCount


class ParseHotKey(CommandUnit):

    def use(self, cmdResult):
        channelKey = cmdResult.get('channel_key')
        speechKey = cmdResult.get('speech_key')
        self.checkKey(channelKey)
        self.checkKey(speechKey)

    def checkKey(self, keyData):
        l = len(keyData)
        if l == 1 and keyData[0] == -1 or l == 0:
            return
        gameCode = keyData[0]
        mods = 0
        if l == 2:
            mods = hotkey.getModsNum(keyData[0])
            gameCode = keyData[1]
        keydef = hotkey.keyDef(gameCode, 1, mods)
        sameArray = hotkeyProxy.getInstance().searchSameKey(gameCode, mods)
        p = BigWorld.player()
        if len(sameArray) and p:
            p.showTopMsg('您在cc设置的%s与原先的\"%s\"冲突,请注意确认' % (keydef.getDesc(1), sameArray[0][1]))


class CommandParseManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.commands = {}
        self.reloadAllCmds()

    def paraseCommand(self, cmdResult):
        cmdType = cmdResult.get('type', None)
        if not cmdType:
            if cmdResult.has_key('speech_key'):
                cmdType = 'speech_key'
        if cmdType in self.commands:
            self.commands[cmdType].use(cmdResult)

    def add(self, unit):
        if unit.cmdType:
            self.commands[unit.cmdType] = unit

    def reloadAllCmds(self):
        self.add(ParseStartUp('startup-finish'))
        self.add(ParseShareRoom('share-room'))
        self.add(ParseFormCount('get-form-count'))
        self.add(ParseHotKey('speech_key'))

    def closeForm(self):
        if self.commands.has_key('get-form-count'):
            self.commands['get-form-count'].closeForm()

    def isFormOpen(self):
        if self.commands.has_key('get-form-count'):
            return self.commands['get-form-count'].isFormOpen()
        return False


ccBoxCmdParseManager = CommandParseManager.getInstance()

def test():
    remoteInterface.downloadMicCardFromCC('cc.cottage.netease.com/nsep/miccard/26079223_1413025912.png')
