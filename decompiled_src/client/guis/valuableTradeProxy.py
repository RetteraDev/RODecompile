#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/valuableTradeProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
import utils
import const
from guis import uiConst
from guis import uiUtils
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD

class ValuableTradeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ValuableTradeProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'getData': self.onGetData,
         'fetchTradeCash': self.onFetchTradeCash,
         'fetchAlltTradeCash': self.onFetchAlltTradeCash}
        self.mediator = None
        self.bindType = 'valuableTrade'
        self.type = 'valuableTrade'
        self.itemList = {}

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_VALUABLE_TRADE:
            self.mediator = mediator

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[13:]), int(idItem[4:]))

    def _getKey(self, page, pos):
        return 'valuableTrade%d.slot%d' % (page, pos)

    def show(self):
        open = gameglobal.rds.configData.get('enableValuableTrade', False)
        if open:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VALUABLE_TRADE)

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_VALUABLE_TRADE)

    def onGetData(self, *arg):
        data = self._getData()
        return data

    def _getData(self):
        ret = {}
        ret['desc'] = GMD.data.get(GMDD.data.VALUABLE_TRADE_DESC, {}).get('text', gameStrings.TEXT_VALUABLETRADEPROXY_60)
        ret['hasAvaliableTrade'] = False
        data = BigWorld.player().valuableTrade
        tradeList = []
        self.itemList = {}
        nowTime = utils.getNow()
        cnt = 0
        for i in data:
            tradeObj = {}
            tradeObj['index'] = cnt
            tradeObj['nuid'] = '%d' % data[i].nuid
            tradeObj['roleName'] = data[i].peerRole
            tradeObj['cash'] = data[i].cash
            tradeObj['tradeType'] = data[i].tradeType
            avaliableTime = data[i].tTrade + SCD.data.get('valuableItemLatchTime', const.VALUABLE_ITEM_LATCH_TIME)
            tradeObj['avaliableTime'] = avaliableTime
            tradeObj['endTime'] = utils.formatDatetime(avaliableTime)
            tradeObj['isFreezed'] = avaliableTime > nowTime
            if avaliableTime <= nowTime:
                ret['hasAvaliableTrade'] = True
            tradeObj['items'] = self.updateItemList(data[i].items)
            self.itemList[cnt] = data[i].items
            tradeList.append(tradeObj)
            cnt += 1

        tradeList.sort(key=lambda k: k['avaliableTime'])
        ret['list'] = tradeList
        return uiUtils.dict2GfxDict(ret, True)

    def updateData(self):
        if self.mediator:
            self.mediator.Invoke('updateView', self._getData())

    def updateItemList(self, itemList):
        ret = []
        for item in itemList:
            itemObj = uiUtils.getGfxItemById(item.id)
            ret.append(itemObj)

        return ret

    def onFetchTradeCash(self, *arg):
        nuidStr = arg[3][0].GetString()
        if nuidStr == '':
            return
        nuid = long(nuidStr)
        BigWorld.player().cell.fetchValuableTradeCash(nuid)

    def onFetchAlltTradeCash(self):
        pass

    def getTotalCash(self):
        data = BigWorld.player().valuableTrade
        totalCash = 0
        for i in data:
            totalCash += data[i].cash

        return totalCash

    def onGetToolTip(self, key):
        page, pos = self.getSlotID(key)
        if self.itemList.has_key(page) and pos < len(self.itemList[page]):
            item = self.itemList[page][pos]
            if item == None:
                return
            return gameglobal.rds.ui.inventory.GfxToolTip(item)
        else:
            return
