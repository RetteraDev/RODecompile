#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/purchaseSellProxy.o
import BigWorld
import gameglobal
import const
import utils
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from data import item_data as ID
from data import fame_data as FD
from cdata import font_config_data as FCD
from cdata import game_msg_def_data as GMDD

class PurchaseSellProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(PurchaseSellProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetInfo,
         'confirmBtnClick': self.onConfirmBtnClick,
         'cancelBtnClick': self.onCancelBtnClick}
        self.mediator = None
        self.sellItem = None
        self.percent = 0
        self.purchaseShopId = 0
        self.fameType = 0
        self.npcId = 0
        self.pos = 0
        self.num = 0
        self.item = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_PURCHASE_SELL, self.hide)

    def show(self, sellItem, npcId, pos, purchaseShopId, percent):
        self.sellItem = sellItem
        self.purchaseShopId = purchaseShopId
        self.percent = percent
        self.npcId = npcId
        self.pos = pos
        self.fameType = ID.data.get(sellItem.id, {}).get('buybackFamePrice').values()[0][0]
        self.famePrice = ID.data.get(sellItem.id, {}).get('buybackFamePrice').values()[0][1]
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PURCHASE_SELL)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PURCHASE_SELL:
            self.mediator = mediator

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.sellItem = None
        self.percent = 0
        self.purchaseShopId = 0
        self.fameType = 0
        self.npcId = 0
        self.pos = 0
        self.num = 0
        self.item = None

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PURCHASE_SELL)

    def onGetInfo(self, *arg):
        if not self.sellItem:
            return
        it = self.sellItem
        itemId = it.id
        data = ID.data.get(itemId, {})
        if not data:
            return
        itemInfo = {}
        itemInfo['percent'] = self.percent
        itemInfo['name'] = data.get('name', '')
        famePrice, _ = gameglobal.rds.ui.purchaseShop.getBuyBackPrice(self.purchaseShopId, itemId)
        itemInfo['famePrice'] = famePrice
        count = BigWorld.player().inv.countItemInPages(itemId)
        iconPath = uiUtils.getItemIconFile40(itemId)
        maxCount = it.maxNum
        itemInfo['currCount'] = self._calcCanSellNum()
        itemInfo['maxCount'] = maxCount
        itemInfo['icon'] = {'iconPath': iconPath,
         'itemId': itemId,
         'srcType': 'purchaseShop'}
        itemInfo['count'] = count
        itemInfo['fameName'] = FD.data.get(self.fameType, {}).get('name', '')
        if hasattr(it, 'quality'):
            quality = it.quality
        else:
            quality = data.get('quality', 1)
        color = '0x' + FCD.data.get(('item', quality), {}).get('color', '#ffffff')[1:]
        qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        itemInfo['color'] = color
        itemInfo['qualitycolor'] = qualitycolor
        return uiUtils.dict2GfxDict(itemInfo, True)

    def onConfirmBtnClick(self, *arg):
        num = int(arg[3][0].GetNumber())
        item = self.sellItem
        p = BigWorld.player()
        if not item:
            return
        count = p.inv.countItemInPages(item.id)
        if count < num:
            return
        for srcPage, srcPos in p.inv.findAllItemInPages(item.id):
            if num <= 0:
                break
            if srcPage == const.CONT_NO_PAGE and srcPos == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.NO_COMPOSITE_SHOP_ITEM_IN_INV, ())
                return
            if p.inv.getQuickVal(srcPage, srcPos).hasLatch():
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
            if self.npcId:
                ent = BigWorld.entity(self.npcId)
                if not ent:
                    return
                cwrap = p.inv.getQuickVal(srcPage, srcPos).cwrap
                if num <= cwrap:
                    ent.cell.purchaseShopBuy(srcPage, srcPos, num, 0, self.pos)
                    num = 0
                    break
                else:
                    ent.cell.purchaseShopBuy(srcPage, srcPos, cwrap, 0, self.pos)
                    num -= cwrap

        self.hide()

    def onCancelBtnClick(self, *arg):
        self.hide()

    def _calcCanSellNum(self):
        p = BigWorld.player()
        currFame = p.purchaseFame.get(self.fameType, 0)
        fprice = self.famePrice
        ret = int((utils.getDailyFameLimit(p, self.fameType) - currFame) / (fprice * self.percent))
        if ret > 0:
            return ret
        else:
            return 0
