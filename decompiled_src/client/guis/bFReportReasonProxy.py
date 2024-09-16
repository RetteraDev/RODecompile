#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bFReportReasonProxy.o
import BigWorld
from Scaleform import GfxValue
import uiConst
import uiUtils
from uiProxy import UIProxy
from ui import gbk2unicode
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD

class BFReportReasonProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BFReportReasonProxy, self).__init__(uiAdapter)
        self.modelMap = {'reportPlayerReason': self.onReportPlayerReason,
         'getPlayerName': self.onGetPlayerName}
        self.mediator = None
        self.initData = []
        self.reportGbid = 0
        self.reportReason = 0
        self.playerName = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_BFREPORT_REASON, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BFREPORT_REASON:
            self.mediator = mediator
            self.initData = self._genGetData()
            return uiUtils.array2GfxAarry(self.initData, True)

    def show(self, gbid, playerName):
        self.reportGbid = gbid
        self.playerName = playerName
        self.uiAdapter.loadWidget(uiConst.WIDGET_BFREPORT_REASON)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BFREPORT_REASON)

    def reset(self):
        self.mediator = None
        self.initData = []
        self.reportGbid = 0
        self.reportReason = 0
        self.playerName = ''

    def onReportPlayerReason(self, *arg):
        p = BigWorld.player()
        if not arg[3][0].GetString():
            p.showGameMsg(GMDD.data.NEED_CHOOSE_ONE_REPORT_REASON, ())
            return
        id = int(arg[3][0].GetString())
        p = BigWorld.player()
        self.reportReason = id
        p.cell.applyBattleFieldReport(self.reportGbid, self.reportReason)
        self.hide()

    def onGetPlayerName(self, *arg):
        return GfxValue(gbk2unicode(self.playerName))

    def _genGetData(self):
        ret = []
        data = DCD.data.get('reportDesc', {})
        for key, value in data.items():
            ob = {'index': str(key),
             'val': value}
            ret.append(ob)

        return ret
