#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tradeRequestProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
from guis import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy

class TradeRequestProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TradeRequestProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRequestData': self.onGetRequestData,
         'acceptRequest': self.onAcceptRequest,
         'ignoreAllRequests': self.onIgnoreAllRequests,
         'closePanel': self.onClosePanel}
        self.mediator = None
        self.tradeQueue = []
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_TRADE, {'click': self.show,
         'refresh': self.refresh})

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TRADE_REQUEST:
            self.mediator = mediator

    def onGetRequestData(self, *arg):
        dataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_TRADE)
        data = {}
        for item in dataList:
            data[item['data'][0]] = item['data'][1]

        self.setTradeQueue(data)
        ret = self.genQueue()
        return ret

    def onAcceptRequest(self, *arg):
        idx = int(arg[3][0].GetNumber())
        BigWorld.player().onTradeAccept(self.tradeQueue[idx][2])
        self.hide()

    def onIgnoreAllRequests(self, *arg):
        for item in self.tradeQueue:
            BigWorld.player().onTradeReject(item[2])

        self.tradeQueue = []
        self.hide()

    def onClosePanel(self, *arg):
        self.hide()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TRADE_REQUEST)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TRADE_REQUEST)

    def reset(self):
        self.mediator = None
        self.tradeQueue = []

    def genQueue(self):
        ret = self.movie.CreateArray()
        ret.SetElement(0, GfxValue(gbk2unicode(gameStrings.TEXT_BINDITEMTRADEPROXY_340)))
        ret.SetElement(1, GfxValue(len(self.tradeQueue)))
        ret.SetElement(2, GfxValue(gbk2unicode(gameStrings.TEXT_TRADEREQUESTPROXY_66)))
        arr = self.movie.CreateArray()
        for i, item in enumerate(self.tradeQueue):
            ar = self.movie.CreateArray()
            ar.SetElement(0, GfxValue(gbk2unicode(item[1])))
            ar.SetElement(1, GfxValue(self._getRemainTime(item[0])))
            arr.SetElement(i, ar)

        ret.SetElement(3, arr)
        return ret

    def setTradeQueue(self, que):
        self.tradeQueue = []
        for k, v in que.items():
            if v:
                self.tradeQueue.append([v[0], v[1], k])

        self.tradeQueue.sort(key=lambda k: k[0])

    def refresh(self):
        dataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_TRADE)
        data = {}
        for item in dataList:
            data[item['data'][0]] = item['data'][1]

        self.setTradeQueue(data)
        if len(self.tradeQueue) > 0:
            if self.mediator != None:
                self.mediator.Invoke('refresh', self.genQueue())
        else:
            self.hide()

    def _getRemainTime(self, val):
        return int(60 - (BigWorld.player().getServerTime() - val))
