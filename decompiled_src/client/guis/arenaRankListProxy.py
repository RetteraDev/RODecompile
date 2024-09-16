#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaRankListProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
from Scaleform import GfxValue
import gameglobal
import utils
import const
import formula
from guis import ui
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from cdata import game_msg_def_data as GMDD
from data import school_data as SD

class ArenaRankListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaRankListProxy, self).__init__(uiAdapter)
        self.modelMap = {'requestData': self.onRequestData,
         'requestCrossData': self.onRequestCrossData,
         'getNoticeText': self.onGetNoticeText,
         'getRankData': self.onGetRankData,
         'getPlayerLv': self.onGetPlayerLv,
         'enableCrossArenaRank': self.onEnableCrossServerRank}
        self.mediator = None
        self.schoolList = SD.data.keys()
        self.arenaInfo = {}
        self.arenaMode = 0
        self.myRank = -1
        self.myCrossRank = -1
        self.crossArenaInfo = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENA_RANK_LIST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ARENA_RANK_LIST:
            self.mediator = mediator

    def show(self, arenaMode = 0):
        self.arenaMode = arenaMode
        if gameglobal.rds.configData.get('enableNewArenaRank', False):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_RANK_LIST)

    def reset(self):
        self.mediator = None

    def clearData(self):
        self.arenaInfo = {}
        self.crossArenaInfo = {}

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_RANK_LIST)

    @ui.callInCD(1)
    def onRequestData(self, *arg):
        rankType = int(arg[3][0].GetNumber())
        lvKey = arg[3][1].GetString()
        if lvKey == '':
            lvKey = self.getPlayerTopRankKey()
            lvKey = '%s_%d' % (lvKey, 0)
        p = BigWorld.player()
        if rankType == 0:
            if self.arenaInfo.has_key(lvKey):
                ver = self.arenaInfo[lvKey][0]
                self.refreshArenaInfo(ver, self.arenaInfo[lvKey][1], lvKey, self.arenaInfo[lvKey][2])
            else:
                ver = 0
            if formula.isBalanceArenaMode(self.arenaMode):
                p.base.getTopArenaScoreTimer(ver, lvKey + const.ARENA_BALANCE_POSTFIX)
            else:
                p.base.getTopArenaScoreTimer(ver, lvKey)

    @ui.callInCD(1)
    def onRequestCrossData(self, *arg):
        rankType = int(arg[3][0].GetNumber())
        lvKey = arg[3][1].GetString()
        if lvKey == '':
            lvKey = self.getPlayerTopRankKey()
            lvKey = '%s_%d' % (lvKey, 0)
        p = BigWorld.player()
        if rankType == 1:
            if self.crossArenaInfo.has_key(lvKey):
                ver = self.crossArenaInfo[lvKey][0]
                self.refreshCrossArenaInfo(ver, self.crossArenaInfo[lvKey][1], lvKey, self.crossArenaInfo[lvKey][2])
            else:
                ver = 0
            if formula.isBalanceArenaMode(self.arenaMode):
                p.base.getGlboalTopArenaScore(ver, lvKey + const.ARENA_BALANCE_POSTFIX)
            else:
                p.base.getGlboalTopArenaScore(ver, lvKey)

    def onGetRankData(self, *arg):
        rankType = int(arg[3][0].GetNumber())
        lvKey = arg[3][1].GetString()
        if lvKey == '':
            lvKey = self.getPlayerTopRankKey()
            lvKey = '%s_%d' % (lvKey, 0)
        if rankType == 1:
            if self.crossArenaInfo.has_key(lvKey):
                ver = self.crossArenaInfo[lvKey][0]
                self.refreshCrossArenaInfo(ver, self.crossArenaInfo[lvKey][1], lvKey, self.crossArenaInfo[lvKey][2])
        elif rankType == 0:
            if self.arenaInfo.has_key(lvKey):
                ver = self.arenaInfo[lvKey][0]
                self.refreshArenaInfo(ver, self.arenaInfo[lvKey][1], lvKey, self.arenaInfo[lvKey][2])

    def onGetNoticeText(self, *arg):
        notice = ''
        rankType = int(arg[3][0].GetNumber())
        if rankType == 0:
            notice = uiUtils.getTextFromGMD(GMDD.data.AREN_RANK_NOTICE, gameStrings.TEXT_ARENARANKLISTPROXY_122)
        elif rankType == 1:
            notice = uiUtils.getTextFromGMD(GMDD.data.CROSS_AREN_RANK_NOTICE, gameStrings.TEXT_ARENARANKLISTPROXY_124)
        return GfxValue(gbk2unicode(notice))

    def refreshArenaInfo(self, ver, info, key, myRank):
        self.arenaInfo[key] = [ver, info, myRank]
        self.updateArenaInfo(info, myRank)
        lvKeyStr = self._getLvKey(key)
        self.refreshLvSelected(lvKeyStr)

    def refreshCrossArenaInfo(self, ver, info, key, myRank):
        self.crossArenaInfo[key] = [ver, info, myRank]
        self.updateCrossArenaInfo(info, myRank)
        lvKeyStr = self._getLvKey(key)
        self.refreshLvSelected(lvKeyStr)

    def updateArenaInfo(self, data, myRank):
        ret = {}
        ret['myRank'] = myRank
        ret['list'] = []
        for i, item in enumerate(data):
            obj = {}
            index = i + 1
            roleName = item['roleName']
            school = SD.data[item['school']]['name'] if item['school'] in self.schoolList else gameStrings.TEXT_GAME_1747
            lv = item['val'][0]
            combat = item['val'][1]
            isSelf = BigWorld.player().gbId == item['gbId']
            obj['index'] = uiUtils.toHtml(index, color='#a65b11') if isSelf else index
            obj['roleName'] = uiUtils.toHtml(roleName, color='#a65b11') if isSelf else roleName
            obj['school'] = school
            obj['schoolIdx'] = item['school']
            obj['lv'] = uiUtils.toHtml(lv, color='#a65b11') if isSelf else lv
            obj['combat'] = uiUtils.toHtml(combat, color='#a65b11') if isSelf else combat
            obj['isSelf'] = isSelf
            ret['list'].append(obj)

        if self.mediator:
            self.mediator.Invoke('updateArenaInfo', uiUtils.dict2GfxDict(ret, True))

    def updateCrossArenaInfo(self, data, myRank):
        if not gameglobal.rds.configData.get('enableNewArenaRank', False):
            return
        ret = {}
        ret['myRank'] = myRank
        ret['list'] = []
        for i, item in enumerate(data):
            obj = {}
            index = i + 1
            roleName = item['roleName']
            school = SD.data[item['school']]['name'] if item['school'] in self.schoolList else gameStrings.TEXT_GAME_1747
            lv = item['val'][0]
            combat = item['val'][1]
            serverName = utils.getServerName(item['val'][3])
            isSelf = BigWorld.player().gbId == item['gbId']
            obj['index'] = uiUtils.toHtml(index, color='#a65b11') if isSelf else index
            obj['roleName'] = uiUtils.toHtml(roleName, color='#a65b11') if isSelf else roleName
            obj['school'] = school
            obj['schoolIdx'] = item['school']
            obj['lv'] = uiUtils.toHtml(lv, color='#a65b11') if isSelf else lv
            obj['combat'] = uiUtils.toHtml(combat, color='#a65b11') if isSelf else combat
            obj['serverName'] = uiUtils.toHtml(serverName, color='#a65b11') if isSelf else serverName
            obj['isSelf'] = isSelf
            ret['list'].append(obj)

        if self.mediator:
            self.mediator.Invoke('updateCrossArenaInfo', uiUtils.dict2GfxDict(ret, True))

    def getPlayerTopRankKey(self):
        return uiUtils.getPlayerTopRankKey()

    def refreshLvSelected(self, lvKey):
        if self.mediator:
            self.mediator.Invoke('refreshLvSelected', GfxValue(lvKey))

    def _getLvKey(self, key):
        splitIdx = key.rfind('_')
        lvStr = key[0:splitIdx]
        return lvStr

    def onGetPlayerLv(self, *arg):
        return GfxValue(self.getPlayerTopRankKey())

    def onEnableCrossServerRank(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableCrossArenaRank', False))
