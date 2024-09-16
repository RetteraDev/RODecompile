#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/loginSelectServerProxy.o
from gamestrings import gameStrings
import json
from Scaleform import GfxValue
import BigWorld
import ResMgr
import const
import gameglobal
import gamelog
import uiConst
import uiUtils
import utils
import netWork
from ServerZone import ServerEntry
from helpers import remoteInterface
from ui import gbk2unicode, unicode2gbk, callFilter
from uiProxy import DataProxy
from data import sys_config_data as SCD
import gametypes
from random import choice

class LoginSelectServerProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(LoginSelectServerProxy, self).__init__(uiAdapter)
        self.bindType = 'loginSelectServer'
        self.modelMap = {'onClickSelectServer': self.onClickSelectServer,
         'onClickBack': self.onClickBack,
         'onClickCloseChangeWidget': self.onClickCloseChangeWidget,
         'onClickConfirmChange': self.onClickConfirmChange,
         'isLockServer': self.isLockServer,
         'refreshServerList': self.onRefreshServerList,
         'bindPhone': self.onBindPhone,
         'intoSelectServer': self.onIntoSelectServer,
         'intoChoiceNoviceServer': self.onIntoChoiceNoviceServer,
         'searchServer': self.onSearchServer}
        self.mediator = None
        self.selZone = ''
        self.selIdx = 0
        self.selServerIdx = 0
        self.venderIdx = 0
        self.lockChooseServer = False
        self.srvListUrl = ''
        self.isAutoGenNeoName = False
        self.noviceServerInfoType = 0
        self.clickServerInfo = []

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_LOGIN_SELECT_SERVER:
            self.mediator = mediator
            initData = {'netVenders': uiConst.NET_VENDERS.values(),
             'venderIdx': self.venderIdx,
             'newbieServerTip': SCD.data.get('newbieServerTip', gameStrings.TEXT_LOGINSELECTSERVERPROXY_59),
             'joinServerTip': SCD.data.get('joinServerTip', gameStrings.TEXT_LOGINSELECTSERVERPROXY_60)}
            osDesc = BigWorld.OSDesc().lower()
            isXp = osDesc.find('xp') != -1 or osDesc.find('server') != -1
            if isXp:
                initData['enableOpenSearchServer'] = False
            else:
                initData['enableOpenSearchServer'] = True
            self._queryServerStatus()
            if utils.isInternationalVersion():
                self.onRefreshServerList()
            return uiUtils.dict2GfxDict(initData, True)
        if widgetId == uiConst.WIDGET_SERVER_NOVICE_GUILD:
            initData = {'type': self.noviceServerInfoType,
             'imgs': map(lambda x: 'noviceServer/%s.dds' % x, SCD.data.get('noviceServerGuildImgs', [1001, 1002, 1003])),
             'intoOldServerTime': SCD.data.get('intoOldServerTime', 10),
             'autoIntoNovieServerTime': SCD.data.get('autoIntoNovieServerTime', 5),
             'linkTxt': SCD.data.get('noviceServerInfoLink', '')}
            if self.noviceServerInfoType == uiConst.SERVER_NOVICE_TRANS_INFO:
                initData['content'] = SCD.data.get('noviceServerTransInfo', gameStrings.TEXT_LOGINSELECTSERVERPROXY_79) % self.clickServerInfo[-1]
            else:
                initData['content'] = SCD.data.get('noviceServerDesc', gameStrings.TEXT_LOGINSELECTSERVERPROXY_81) % self.clickServerInfo[-1]
            self.mediator.Invoke('setVisible', GfxValue(False))
            return uiUtils.dict2GfxDict(initData, True)
        if widgetId == uiConst.WIDGET_FORCE_CHANGE_NAME:
            return uiUtils.dict2GfxDict({'maxChars': const.MAX_CHAR_NAME,
             'isInternationalVersion': utils.isInternationalVersion()}, True)

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_PHONE_BIND_BOX:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PHONE_BIND_BOX)
        elif widgetId == uiConst.WIDGET_SERVER_NOVICE_GUILD:
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_SERVER_NOVICE_GUILD)
            if self.mediator:
                self.mediator.Invoke('setVisible', GfxValue(True))
        else:
            DataProxy._asWidgetClose(self, widgetId, multiID)

    def setup(self):
        try:
            sect = ResMgr.openSection('../game/conf.xml')
            hostName = ''
            if sect:
                hostName = sect.readString('lastServer/serv')
            else:
                hostName = gameglobal.rds.loginManager.srvDict.firstMachine
            if hostName:
                self.selZone, self.selIdx, self.selServerIdx = gameglobal.rds.loginManager.srvDict.findByNameExcludeHide(hostName)
            else:
                self.selZone, self.selIdx, self.selServerIdx = gameglobal.rds.loginManager.srvDict.firstZone, 0, 0
        except:
            self.selZone, self.selIdx, self.selServerIdx = gameglobal.rds.loginManager.srvDict.firstZone, 0, 0

    def select(self, selZone, selIdx, selServerIdx):
        self.selZone = selZone
        self.selIdx = selIdx
        self.selServerIdx = selServerIdx
        if self.mediator:
            ret = self.movie.CreateArray()
            ret.SetElement(0, GfxValue(gbk2unicode(self.selZone)))
            ret.SetElement(1, GfxValue(int(self.selIdx)))
            self.mediator.Invoke('selectServer', ret)

    def getValue(self, key):
        if key == 'loginSelectServer.setData':
            ret = self.movie.CreateArray()
            srvDict = gameglobal.rds.loginManager.srvDict
            if srvDict:
                for i, key in enumerate(srvDict.keys):
                    rr = self.movie.CreateObject()
                    ar = self.movie.CreateArray()
                    for j, v in enumerate(srvDict.item.get(key)):
                        info = self.movie.CreateObject()
                        busy = int(v.busy)
                        info.SetMember('busy', GfxValue(busy))
                        info.SetMember('locale', GfxValue(int(v.locale)))
                        info.SetMember('name', GfxValue(gbk2unicode(v.name)))
                        info.SetMember('title', GfxValue(gbk2unicode(v.title)))
                        info.SetMember('mode', GfxValue(int(v.mode)))
                        info.SetMember('charNum', GfxValue(int(v.charNum)))
                        ar.SetElement(j, info)

                    charNum = srvDict.getCharNumByZone(key)
                    rr.SetMember('zone', GfxValue(gbk2unicode(key)))
                    rr.SetMember('values', ar)
                    rr.SetMember('charNum', GfxValue(int(charNum)))
                    ret.SetMember(i, rr)

            return ret
        if key == 'loginSelectServer.selectServer':
            ret = self.movie.CreateArray()
            ret.SetElement(0, GfxValue(gbk2unicode(self.selZone)))
            ret.SetElement(1, GfxValue(int(self.selIdx)))
            return ret

    def show(self):
        self.setup()
        loadWidgetsList = [uiConst.WIDGET_LOGINLOGO, uiConst.WIDGET_LOGIN_SELECT_SERVER, uiConst.WIDGET_LOGINLOGOTIPS2]
        gameglobal.rds.loginScene.loadWidgets(loadWidgetsList)
        gameglobal.rds.logLoginState = gameglobal.GAME_SERVER_SELECT
        netWork.sendInfoForLianYun(gameglobal.rds.logLoginState)

    def hide(self, destroy = True):
        unloadWidgetsList = [uiConst.WIDGET_LOGIN_SELECT_SERVER, uiConst.WIDGET_PHONE_BIND_BOX, uiConst.WIDGET_SERVER_NOVICE_GUILD]
        gameglobal.rds.loginScene.unloadWidgets(unloadWidgetsList)
        gameglobal.rds.ui.serverMergeQuery.hide()

    def getSelEntry(self):
        if gameglobal.rds.isSinglePlayer:
            return ServerEntry()
        if gameglobal.rds.loginManager.isGtLogonMode():
            return gameglobal.rds.loginManager.srvDict.item.get(self.selZone)[self.selServerIdx]
        return ServerEntry()

    @callFilter(uiConst.SERVER_CALL_ABANDONTASK, showMsg=False)
    def onClickSelectServer(self, *arg):
        selZone = unicode2gbk(arg[3][0].GetString())
        selIdx = int(arg[3][1].GetNumber())
        selServerIdx = int(arg[3][2].GetNumber())
        tmpVenderIdx = int(arg[3][3].GetNumber())
        self.clickSelectServer(selZone, selIdx, selServerIdx, tmpVenderIdx)

    def clickSelectServer(self, selZone, selIdx, selServerIdx, tmpVenderIdx):
        if self.enableNoviceServerGuild() and gameglobal.rds.loginManager.srvDict.findNoviceServers():
            try:
                selEntry = gameglobal.rds.loginManager.srvDict.item.get(selZone)[selServerIdx]
            except:
                return

            self.clickServerInfo = [selZone,
             selIdx,
             selServerIdx,
             tmpVenderIdx,
             selEntry.title]
            if selEntry.charNum == 0 and int(selEntry.mode) == gametypes.SERVER_MODE_SHOW_NOVICE_TIP:
                self.showNoviceServerTrans()
            elif selEntry.charNum == 0 and int(selEntry.mode) == gametypes.SERVER_MODE_NOVICE:
                self.showNoviceServerInfo()
            else:
                self.doConnectServer(selZone, selIdx, selServerIdx, tmpVenderIdx)
        else:
            self.doConnectServer(selZone, selIdx, selServerIdx, tmpVenderIdx)

    def doConnectServer(self, zone, idx, serverIdx, venderIdx):
        if zone and idx != -1:
            self.selZone = zone
            self.selIdx = idx
            self.selServerIdx = serverIdx
            self.venderIdx = venderIdx
            gameglobal.rds.loginManager.tryConnectGameServer()
            if gameglobal.rds.offline:
                self.lockChooseServer = True
        else:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_LOGINSELECTSERVERPROXY_212)

    def onClickBack(self, *arg):
        gameglobal.rds.loginManager.prevPage()
        gameglobal.rds.loginScene.clearScene()
        gameglobal.rds.GameState = gametypes.GS_START
        BigWorld.callback(0, gameglobal.rds.loginScene.loadSpace)
        if gameglobal.rds.enableBinkLogoCG:
            import game
            game.playBinkCg('login')

    def onClickCloseChangeWidget(self, *arg):
        self.closeForceChangNameWidget()

    def onClickConfirmChange(self, *arg):
        newName = arg[3][0].GetString()
        if not gameglobal.rds.ui.characterDetailAdjust.checkName(newName):
            return
        newName = unicode2gbk(newName)
        self.lockChooseServer = False
        p = BigWorld.player()
        if hasattr(p.base, 'renameCharacter'):
            p.base.renameCharacter(self.oldName, newName, self.userSchool, self.clientRev, self.isAutoGenNeoName)
        gameglobal.rds.loginManager.cache = {'gbID': self.gbID,
         'name': newName}

    def showForceChangeNameWidget(self, oldName, userSchool, clientRev, gbID, isAutoGenNeoName = False):
        self.oldName = oldName
        self.userSchool = userSchool
        self.clientRev = clientRev
        self.gbID = gbID
        self.isAutoGenNeoName = isAutoGenNeoName
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHARACTER_NAME_INPUT_NEW, True)

    def envSDKForceChangeName(self, oldName, userSchool, clientRev):
        p = BigWorld.player()
        p.base.renameCharacter(oldName, '', userSchool, clientRev, True)

    def closeForceChangNameWidget(self):
        gameglobal.rds.ui.characterDetailAdjust.onCloseNameInput()
        self.lockChooseServer = False

    def releaseLockServer(self):
        self.lockChooseServer = False

    def isLockServer(self, *arg):
        if self.lockChooseServer:
            gameglobal.rds.ui.characterDetailAdjust.showTips(gameStrings.TEXT_LOGINSELECTSERVERPROXY_260)
        return GfxValue(self.lockChooseServer)

    @callFilter(30)
    def onRefreshServerList(self, *arg):
        if not self.srvListUrl:
            try:
                file = open(const.UPDATE_FILE, 'rb')
                for line in file:
                    key = 'ServerList'
                    if line[:len(key)] == key:
                        self.srvListUrl = line[len(key) + 1:].strip()
                        break

                file.close()
            except Exception as e:
                gamelog.debug('@zhp read update fail', e)

        if self.srvListUrl:
            remoteInterface.getServerList(self.srvListUrl, self._refreshServerList)

    def onBindPhone(self, *args):
        phoneNum = unicode2gbk(args[3][0].GetString()).strip()
        if utils.isValidPhoneNum(phoneNum):
            BigWorld.player().base.bindReservationPhone(phoneNum)
            return GfxValue(True)
        else:
            return GfxValue(False)

    def onIntoSelectServer(self, *args):
        if self.clickServerInfo:
            self.doConnectServer(self.clickServerInfo[0], self.clickServerInfo[1], self.clickServerInfo[2], self.clickServerInfo[3])

    def onIntoChoiceNoviceServer(self, *args):
        noviceServers = gameglobal.rds.loginManager.srvDict.findNoviceServers()
        if not noviceServers:
            gamelog.error('@zhp no noviceServers to login')
            return
        zone, idx, serverIdx = choice(noviceServers)
        self.doConnectServer(zone, idx, serverIdx, self.clickServerInfo[3])

    def onSearchServer(self, *args):
        gameglobal.rds.ui.serverMergeQuery.show()

    def _refreshServerList(self, serverList):
        serverList = serverList.splitlines()
        if serverList:
            gameglobal.rds.loginManager.srvDict.refreshServerList(serverList)
            self.setup()
            for key in self.binding.keys():
                data = self.getValue(key)
                if data != None:
                    self.binding[key][1].InvokeSelf(data)

            self._queryServerStatus()

    def enabeldServerReservation(self):
        return True

    def enableNoviceServerGuild(self):
        return True

    def _queryServerStatus(self):
        if self.enabeldServerReservation():
            remoteInterface.getServerStatus(self._onGetServerStatus)

    def _onGetServerStatus(self, status):
        if not status or not self.mediator:
            return
        try:
            result = []
            data = json.loads(status, encoding='UTF-8')
            for k, v in data.items():
                result.append((k.encode(utils.defaultEncoding()), v.encode(utils.defaultEncoding())))

            if data:
                self.mediator.Invoke('refreshStatus', uiUtils.array2GfxAarry(result, True))
        except:
            gamelog.error('@zhp getServerStatus error' + status)

    def showNoviceServerTrans(self):
        if self.enableNoviceServerGuild():
            self.noviceServerInfoType = uiConst.SERVER_NOVICE_TRANS_INFO
            self.uiAdapter.loadWidget(uiConst.WIDGET_SERVER_NOVICE_GUILD)

    def showNoviceServerInfo(self):
        if self.enableNoviceServerGuild():
            self.noviceServerInfoType = uiConst.SERVER_NOVICE_SERVER_DESC
            self.uiAdapter.loadWidget(uiConst.WIDGET_SERVER_NOVICE_GUILD)
