#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/wwKillScoreRankListProxy.o
import BigWorld
from uiProxy import UIProxy
from operator import itemgetter
import gameglobal
import utils
from guis import uiConst
from guis import uiUtils
from data import region_server_config_data as RSCD

class WwKillScoreRankListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WwKillScoreRankListProxy, self).__init__(uiAdapter)
        self.modelMap = {'getData': self.onGetWwKillScoreData}
        self.mediator = None
        self.cacheData = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_WW_KILL_SCORE_RANK_LIST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WW_KILL_SCORE_RANK_LIST:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WW_KILL_SCORE_RANK_LIST)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WW_KILL_SCORE_RANK_LIST)

    def clearData(self):
        self.cacheData = {}

    def onGetWwKillScoreData(self, *arg):
        ver = self.cacheData.get('ver', 0)
        data = self.cacheData.get('data', [])
        BigWorld.player().base.getTopWWKillScore(ver)
        return uiUtils.dict2GfxDict(self._genWwKillScoreData(data), True)

    def refreshView(self, data, ver):
        self.cacheData['ver'] = ver
        self.cacheData['data'] = data
        self.updateView(data)

    def updateView(self, data):
        if self.mediator:
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(self._genWwKillScoreData(data), True))

    def _genWwKillScoreData(self, data):
        ret = {}
        data = self._sortKillData(data)
        ret['list'] = []
        ret['selfRank'] = 0
        ret['selfData'] = {}
        myGbid = BigWorld.player().gbId
        curServerId = utils.getCurrHostId()
        for i in xrange(len(data)):
            obj = {}
            info = data[i]
            obj['rank'] = i + 1
            name = info[1]
            isCrossRoleName = utils.isCrossRoleName(name)
            obj['playerName'] = utils.parseRoleNameFromCrossName(name) if isCrossRoleName else name
            obj['serverName'] = utils.parseServerNameFromCrossName(name) if isCrossRoleName else RSCD.data.get(int(curServerId), {}).get('serverName', '')
            obj['kill'] = data[i][3][0]
            obj['combo'] = data[i][3][1]
            if data[i][0] == myGbid:
                ret['selfRank'] = i + 1
                ret['selfData'] = obj
            ret['list'].append(obj)

        return ret

    def _sortKillData(self, data):
        if len(data) < 1:
            return []
        temp = sorted(data, key=itemgetter(3), reverse=True)
        return temp
