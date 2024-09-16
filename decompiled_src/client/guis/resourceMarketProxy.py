#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/resourceMarketProxy.o
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
import uiUtils
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import resourceMarketManager
from cdata import game_msg_def_data as GMDD
from data import kuiling_config_data as KCD

class ResourceMarketProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ResourceMarketProxy, self).__init__(uiAdapter)
        self.bindType = 'resourceMarket'
        self.type = 'resourceMarket'
        self.marketId = 1
        self.modelMap = {'getTitleInfo': self.onGetTitleInfo,
         'getMarketInfo': self.onGetMarketInfo,
         'getHotResourceInfo': self.onGetHotResourceInfo,
         'getBagInfo': self.onGetBagInfo,
         'closeClick': self.onCloseClick,
         'refreshClick': self.onRefreshClick,
         'tabBtnClick': self.onTabBtnClick,
         'buyResClick': self.onBuyResClick,
         'buyHotResClick': self.onBuyHotResClick,
         'sellResClick': self.onSellResClick,
         'getDealInfo': self.onGetDealInfo,
         'closeDealWidget': self.onCloseDealWidget,
         'dealConfirmClick': self.onDealConfirmClick,
         'dealCancelClick': self.onDealCancelClick,
         'getTotalPrice': self.onGetTotalPrice,
         'getPanelInfo': self.onGetPanelInfo}
        self.resourceMarketManager = resourceMarketManager.getInstance()
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_RESOURCE_MARKET, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RESOURCE_MARKET:
            self.mediator = mediator

    def reset(self):
        self.isShow = False
        self.mediator = None
        self.tabType = 0
        self.buyIndex = 0
        self.sellIndex = 0
        self.typeStr = ''
        self.resourceMarketManager.reset()

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[9:]), int(idItem))

    def show(self):
        p = BigWorld.player()
        self.marketId = KCD.data.get(p.kuilingOrg, {})['marketId']
        p.cell.queryMarketInfo(self.marketId, self.resourceMarketManager.timeStamp)

    def refreshResourceMarket(self, marketId, marketInfo, timeStamp):
        gamelog.debug('@hjx market#refreshResourceMarket:', marketId, marketInfo, timeStamp)
        self.resourceMarketManager.resetInsByMarketId(marketId, marketInfo, self.tabType, timeStamp)
        if self.mediator:
            self.mediator.Invoke('refreshMarket')
            self.mediator.Invoke('refreshHotResource')
            self.mediator.Invoke('refreshBag')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RESOURCE_MARKET)

    def close(self):
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RESOURCE_MARKET)
        self.isShow = False
        self.resourceMarketManager.reset()

    def onCloseClick(self, *arg):
        self.close()

    def onRefreshClick(self, *arg):
        p = BigWorld.player()
        self.marketId = KCD.data.get(p.kuilingOrg, {})['marketId']
        p.cell.queryMarketInfo(self.marketId, self.resourceMarketManager.timeStamp)

    def onTabBtnClick(self, *arg):
        self.tabType = int(arg[3][0].GetNumber())
        self.resourceMarketManager.marketIns.setTabType(self.tabType)
        if self.mediator:
            self.mediator.Invoke('refreshMarket')
            self.mediator.Invoke('refreshHotResource')

    def onBuyResClick(self, *arg):
        self.buyIndex = int(arg[3][0].GetNumber())
        self.typeStr = 'buy'
        gamelog.debug('@hjx market#onBuyResClick:', self.buyIndex)
        self.resourceMarketManager.marketIns.createDealIns(self.typeStr, self.buyIndex)
        self.showDealWidget()

    def onBuyHotResClick(self, *arg):
        self.buyIndex = int(arg[3][0].GetNumber())
        self.typeStr = 'buyHot'
        gamelog.debug('@hjx market#onBuyHotResClick:', self.buyIndex)
        self.resourceMarketManager.marketIns.createDealIns(self.typeStr, self.buyIndex)
        self.showDealWidget()

    def onBuyFromMarket(self, mid, iid, count, price):
        if self.mediator:
            self.resourceMarketManager.marketIns.updateDealInfo(mid, iid, count, price)
            info = self.resourceMarketManager.marketIns.getDealPanelInfo()
            gamelog.debug('@hjx market#onBuyFromMarket:', info)
            self.mediator.Invoke('updateBuyItem', (GfxValue(self.buyIndex), uiUtils.dict2GfxDict(info, True), GfxValue(self.typeStr)))

    def onSellResClick(self, *arg):
        self.sellIndex = int(arg[3][0].GetNumber())
        self.typeStr = 'sell'
        gamelog.debug('@hjx market#onSellResClick:', self.sellIndex)
        self.resourceMarketManager.marketIns.createDealIns(self.typeStr, self.sellIndex)
        self.showDealWidget()

    def onSellToMarket(self, mid, iid, count, price):
        if self.mediator:
            self.resourceMarketManager.marketIns.updateDealInfo(mid, iid, count, price)
            info = self.resourceMarketManager.marketIns.getDealPanelInfo()
            gamelog.debug('@hjx market#onSellToMarket:', info)
            self.mediator.Invoke('updateSellItem', uiUtils.dict2GfxDict(info, True))

    def onGetTotalPrice(self, *arg):
        cnt = int(arg[3][0].GetNumber())
        gamelog.debug('@hjx market#onGetTotalPrice:', self.resourceMarketManager.marketIns.calcTotalPrice(cnt))
        return GfxValue(self.resourceMarketManager.marketIns.calcTotalPrice(cnt)[0])

    def onGetPanelInfo(self, *arg):
        return self.resourceMarketManager.marketIns.getMarketPanelInfo()

    def showDealWidget(self):
        if self.typeStr == '':
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RESOURCE_DEAL, True)

    def closeDealWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RESOURCE_DEAL)

    def onCloseDealWidget(self, *arg):
        self.closeDealWidget()

    def onDealConfirmClick(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        amount = int(arg[3][1].GetNumber())
        price = int(arg[3][2].GetNumber())
        if amount == 0:
            BigWorld.player().showGameMsg(GMDD.data.RESOURCE_MARKET_DEAL_FAILED, ())
            return
        gamelog.debug('@hjx market#onDealConfirmClick:', itemId, amount, price)
        self.resourceMarketManager.marketIns.dealConfirmClick(itemId, amount, price)
        self.closeDealWidget()

    def onDealCancelClick(self, *arg):
        self.closeDealWidget()

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RESOURCE_MARKET)

    def onGetTitleInfo(self, *arg):
        return self.resourceMarketManager.getTitleInfo()

    def onGetMarketInfo(self, *arg):
        return self.resourceMarketManager.getMarketInfo()

    def onGetHotResourceInfo(self, *arg):
        return self.resourceMarketManager.getHotResourceInfo()

    def onGetBagInfo(self, *arg):
        return self.resourceMarketManager.getBagInfo()

    def onGetDealInfo(self, *arg):
        info = {}
        info['typeStr'] = self.typeStr
        info.update(self.resourceMarketManager.marketIns.getDealPanelInfo())
        return uiUtils.dict2GfxDict(info, True)

    def refreshPanel(self):
        if self.mediator:
            self.mediator.Invoke('refreshPanel')
