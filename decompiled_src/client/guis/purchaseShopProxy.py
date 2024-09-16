#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/purchaseShopProxy.o
from gamestrings import gameStrings
import BigWorld
import math
from Scaleform import GfxValue
from callbackHelper import Functor
from helpers import capturePhoto
import gameglobal
import const
import utils
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from data import item_data as ID
from cdata import font_config_data as FCD
from data import fame_data as FD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import composite_shop_trade_data as CSTD

class PurchaseShopProxy(SlotDataProxy):
    NOTSELLALL = [410128,
     410129,
     410130,
     410131]

    def __init__(self, uiAdapter):
        super(PurchaseShopProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetInfo,
         'sellClick': self.onSellClick,
         'refreshClick': self.onRefreshClick,
         'sellAllClick': self.onSellAllClick,
         'getBtnTip': self.onGetBtnTip,
         'itemClick': self.onItemClick}
        self.mediator = None
        self.purchaseShopId = None
        self.purchaseCurrPage = 0
        self.npcId = 0
        self.purchasePageStamp = {}
        self.purchaseShopItemInfo = {}
        self.fameType = 0
        self.percent = 0
        self.messageBoxId = 0
        self.purchaseShopGen = None
        self.notSellAllList = []
        self.itemArray = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_PURCHASE_SHOP, self.clearWidget)

    def show(self, npcId):
        self.npcId = npcId
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PURCHASE_SHOP)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PURCHASE_SHOP:
            self.mediator = mediator
            self.notSellAllList = SCD.data.get('notSellAllList', self.NOTSELLALL)

    def initPurchaseShopGen(self, npc):
        if not self.purchaseShopGen:
            self.purchaseShopGen = capturePhoto.PurchaseShopPhotoGen.getInstance('gui/taskmask.tga', 425)
            uiUtils.takePhoto3D(self.purchaseShopGen, npc, npc.npcId)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PURCHASE_SHOP)
        self.purchaseShopId = None
        self.purchaseCurrPage = 0
        self.npcId = 0
        self.purchasePageStamp = {}
        self.purchaseShopItemInfo = {}
        self.fameType = 0
        self.percent = 0
        self.notSellAllList = []
        self.itemArray = []
        if self.purchaseShopGen:
            self.purchaseShopGen.endCapture()
            self.purchaseShopGen = None

    def onGetInfo(self, *arg):
        ent = BigWorld.entities.get(self.npcId)
        if not ent:
            return
        self.purchaseShopId = ent.purchaseShopId
        stamp = self.purchasePageStamp.get(self.purchaseCurrPage, 0)
        self.refreshFameData()
        self.setRefreshCDTip()
        self.initPurchaseShopGen(ent)
        ent.cell.purchaseShopTurnPage(self.purchaseCurrPage, stamp, False)

    def refreshFameData(self):
        itemData = {}
        itemData['fameType'] = self.fameType
        fame = BigWorld.player().getFame(self.fameType)
        if fame == None:
            return
        else:
            fameLv = 1
            maxLv = 1
            value = FD.data.get(self.fameType, {})
            if not len(value):
                return
            for lv, fameValue in value.get('lvUpNeed', {}).items():
                if fame >= fameValue:
                    fameLv = lv + 1
                maxLv = lv

            fameLv = min(maxLv, fameLv)
            itemData['fameLvName'] = SCD.data.get('fameLvNameModify', {}).get(fameLv, '')
            itemData['fameName'] = FD.data.get(self.fameType, {}).get('name', '')
            if fameLv == 1:
                itemData['max'] = value.get('lvUpNeed', {}).get(fameLv, 0)
                itemData['fame'] = fame
            elif fameLv == maxLv and fame >= value.get('maxVal', 0):
                itemData['max'] = value.get('lvUpNeed', {}).get(maxLv, 0) - value.get('lvUpNeed', {}).get(fameLv - 1, 0)
                itemData['fame'] = itemData['max']
            else:
                minValue = value.get('lvUpNeed', {}).get(fameLv - 1, 0)
                itemData['fame'] = fame - minValue
                itemData['max'] = value.get('lvUpNeed', {}).get(fameLv, fame) - minValue
            self.percent = SCD.data.get('fameLvNamePercent', {}).get(fameLv, 0)
            itemData['famePercent'] = self.percent
            todayFame = BigWorld.player().purchaseFame.get(self.fameType, 0)
            limitFame = utils.getDailyFameLimit(BigWorld.player(), self.fameType)
            if limitFame == const.MAX_PURCHASE_LIMIT:
                itemData['todayRemain'] = -1
            else:
                itemData['todayRemain'] = utils.getDailyFameLimit(BigWorld.player(), self.fameType) - todayFame
            itemData['fameTips'] = gameStrings.TEXT_PURCHASESHOPPROXY_128 % (itemData['fameName'], uiUtils.toHtml(itemData['todayRemain'], '#8FB259'))
            if self.mediator:
                self.mediator.Invoke('setPurChaseShopData', uiUtils.dict2GfxDict(itemData, True))
            return

    def isFameMax(self, fameID):
        fame = BigWorld.player().getFame(fameID)
        if fame == None:
            return False
        else:
            value = FD.data.get(fameID, {})
            maxFame = value.get('maxVal', 0)
            return fame >= maxFame

    def setPurchaseItem(self, page, stamp, itemInfo = None, forceUpdate = False):
        if itemInfo != None:
            self.purchaseShopItemInfo[page] = {}
            pos = 0
            for item in itemInfo:
                self.purchaseShopItemInfo[page][pos] = item
                pos += 1

        pageInfo = self.purchaseShopItemInfo[page]
        self.purchasePageStamp[page] = stamp
        self.purchaseCurrPage = page
        self.setPageItem(page, stamp, pageInfo, forceUpdate)

    def setPageItem(self, page, stamp, pageInfo, forceUpdate = False):
        itemArray = []
        for pos in xrange(len(pageInfo)):
            it = pageInfo[pos]
            itemInfo = self._getItemInfo(pos, it)
            itemArray.append(itemInfo)

        if self.mediator:
            self.mediator.Invoke('refreshShop', uiUtils.array2GfxAarry(itemArray, True))
            self.itemArray = itemArray

    def refreshItems(self):
        if self.mediator and self.itemArray:
            p = BigWorld.player()
            for index in xrange(len(self.itemArray)):
                item = self.itemArray[index]
                item['count'] = p.inv.countItemInPages(item['id'])

            self.mediator.Invoke('refreshShop', uiUtils.array2GfxAarry(self.itemArray, True))

    def _getItemInfo(self, pos, it):
        if not it:
            return {}
        p = BigWorld.player()
        data = ID.data.get(it.id, {})
        itemInfo = {}
        itemId = it.id
        fameType = self._getFameType(itemId)
        count = p.inv.countItemInPages(itemId)
        iconPath = uiUtils.getItemIconFile40(itemId)
        if hasattr(it, 'quality'):
            quality = it.quality
        else:
            quality = data.get('quality', 1)
        qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        itemInfo['qualitycolor'] = qualitycolor
        itemInfo['count'] = count
        if count >= 1:
            count = 1
        else:
            count = 0
        itemInfo['icon'] = {'iconPath': iconPath,
         'itemId': itemId,
         'count': count,
         'srcType': 'purchaseShop'}
        sPrice, _ = self.getBuyBackPrice(self.purchaseShopId, it.id)
        itemInfo['sPrice'] = sPrice
        itemInfo['pos'] = pos
        itemInfo['id'] = it.id
        itemInfo['fameName'] = FD.data.get(fameType, {}).get('name', '')
        fameLimit = self.getItemFameLimit(it)
        if fameLimit != -1:
            itemInfo['fameLimitLvName'] = self.getFameLvName(fameType, fameLimit)
            if p.getFame(fameType) >= fameLimit:
                itemInfo['canBuy'] = True
            else:
                itemInfo['canBuy'] = False
        else:
            itemInfo['canBuy'] = True
        return itemInfo

    def getFameLvName(self, fameType, fameLimit):
        lvUpNeed = FD.data.get(fameType, {}).get('lvUpNeed', {})
        if not lvUpNeed:
            return None
        else:
            for key, value in lvUpNeed.items():
                if fameLimit > value:
                    continue
                if value > fameLimit:
                    fameName = SCD.data.get('fameLvNameModify', {}).get(key, '')
                    return fameName

            return ''

    def getItemFameLimit(self, item):
        fameData = CSTD.data.get(item.compositeId, {}).get('fameLimit', [])
        if fameData:
            return fameData[0][1]
        else:
            return -1

    def getBuyBackPrice(self, purchaseShopId, itemId):
        sFamePrice = 0
        sPrice = 0
        itemRecord = ID.data.get(itemId, '')
        if itemRecord == '':
            return (sFamePrice, sPrice)
        famePriceDict = itemRecord.get('buybackFamePrice', '')
        if famePriceDict:
            return (famePriceDict.values()[0][1], itemRecord.get('sPrice', 0))
        famePriceDict = itemRecord.get('famePrice', '')
        if famePriceDict != '':
            for key in famePriceDict.keys():
                if purchaseShopId in key:
                    fameData = famePriceDict[key]
                    fameId = fameData[0]
                    sFamePrice = fameData[1]
                    if len(fameData) > 2:
                        fprices = fameData[2]
                        fameLv = BigWorld.player().getFameLv(fameId)
                        for i in xrange(0, len(fprices), 2):
                            if fameLv >= fprices[i]:
                                sFamePrice = fprices[i + 1]
                            else:
                                break

                    break

        sPrice = itemRecord['sPrice']
        return (sFamePrice, sPrice)

    def onSellClick(self, *arg):
        if not self.purchaseShopItemInfo:
            return
        pos = arg[3][0].GetNumber()
        item = self.purchaseShopItemInfo[self.purchaseCurrPage][pos]
        if not item:
            return False
        self.fameType = self._getFameType(item.id)
        if self._calcCanSellNum(item, 0) <= 0:
            BigWorld.player().showGameMsg(GMDD.data.FAME_DAILY_LIMIT, (FD.data.get(self._getFameType(item.id), {}).get('name', ''), item.name))
            return
        gameglobal.rds.ui.purchaseSell.show(item, self.npcId, pos, self.purchaseShopId, self.percent)
        if self.messageBoxId:
            gameglobal.rds.ui.messageBox.dismiss(self.messageBoxId)
            self.messageBoxId = 0

    def onRefreshClick(self, *arg):
        npcEntity = BigWorld.entities.get(self.npcId)
        if not npcEntity:
            return
        stamp = self.purchasePageStamp.get(self.purchaseCurrPage, 0)
        npcEntity.cell.purchaseShopTurnPage(self.purchaseCurrPage, stamp, True)
        self.setRefreshAble(False)
        BigWorld.callback(SCD.data.get('setPurchaseRefreshCD', 5), Functor(self.setRefreshAble, True))

    def setRefreshAble(self, isEnable):
        if self.mediator:
            self.mediator.Invoke('setRefreshAble', GfxValue(isEnable))

    def onSellAllClick(self, *arg):
        p = BigWorld.player()
        if self.percent == 0:
            BigWorld.player().showGameMsg(GMDD.data.COMPOSITE_SHOP_SELL_FORBIDDEN_PRE_LIMIT, ())
            return
        allFame, fameName = self._sellAll()
        if utils.getDailyFameLimit(p, self.fameType) - p.purchaseFame.get(self.fameType, 0) <= 0:
            BigWorld.player().showGameMsg(GMDD.data.FAME_DAILY_LIMIT_BY_ALL, FD.data.get(self.fameType, {}).get('name', ''))
            return
        defaultSellAllString = gameStrings.TEXT_PURCHASESHOPPROXY_304
        self.messageBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(defaultSellAllString, self.confirmSellAll)
        if gameglobal.rds.ui.purchaseSell.mediator:
            gameglobal.rds.ui.purchaseSell.hide()

    def _calcCanSellNum(self, item, sumFame):
        p = BigWorld.player()
        fameType = self._getFameType(item.id)
        value = FD.data.get(fameType, {})
        fameLv = 0
        maxLv = 0
        fame = BigWorld.player().getFame(fameType)
        if not len(value):
            return 0
        for lv, fameValue in value.get('lvUpNeed', {}).items():
            if fame >= fameValue:
                fameLv = lv + 1
            maxLv = lv

        fameLv = min(maxLv, fameLv)
        percent = SCD.data.get('fameLvNamePercent', {}).get(fameLv, 0)
        currFame = p.purchaseFame.get(fameType, 0) + sumFame * percent
        fprice = self._getFamePrice(item.id)
        if fprice <= 0:
            return 0
        fameType = self._getFameType(item.id)
        ret = int((utils.getDailyFameLimit(p, fameType) - currFame) / (fprice * percent))
        if ret > 0:
            return ret
        else:
            return 0

    def _sellAll(self):
        if not self.purchaseShopItemInfo:
            return (0, '')
        p = BigWorld.player()
        pageInfo = self.purchaseShopItemInfo[self.purchaseCurrPage]
        sumFame = 0
        fameName = FD.data.get(self.fameType, {}).get('name', '')
        for pos in xrange(len(pageInfo)):
            it = pageInfo[pos]
            itemId = it.id
            if itemId in self.notSellAllList:
                continue
            count = p.inv.countItemInPages(itemId)
            num = self._calcCanSellNum(it, sumFame)
            if num <= 0:
                continue
            sellCount = min(count, num)
            sPrice, _ = self.getBuyBackPrice(self.purchaseShopId, itemId)
            sumFame += sPrice * sellCount

        return (int(math.ceil(sumFame * self.percent)), fameName)

    def confirmSellAll(self):
        if not self.purchaseShopItemInfo:
            return
        p = BigWorld.player()
        sunFame = 0
        pageInfo = self.purchaseShopItemInfo[self.purchaseCurrPage]
        for pos in xrange(len(pageInfo.keys())):
            it = pageInfo[pos]
            itemId = it.id
            if itemId in self.notSellAllList:
                continue
            count = p.inv.countItemInPages(itemId)
            sellCount = min(count, self._calcCanSellNum(it, sunFame))
            sPrice, _ = self.getBuyBackPrice(self.purchaseShopId, itemId)
            if sellCount <= 0:
                continue
            for srcPage, srcPos in p.inv.findAllItemInPages(itemId):
                if sellCount <= 0:
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
                        continue
                    cwrap = p.inv.getQuickVal(srcPage, srcPos).cwrap
                    fameType = self._getFameType(itemId)
                    if self.isFameMax(fameType):
                        continue
                    if sellCount <= cwrap:
                        ent.cell.purchaseShopBuy(srcPage, srcPos, sellCount, 0, pos)
                        sunFame += sPrice * sellCount
                        break
                    else:
                        ent.cell.purchaseShopBuy(srcPage, srcPos, cwrap, 0, pos)
                        sunFame += sPrice * cwrap
                        sellCount -= cwrap

    def setSingleItem(self, page, pos, item):
        if not item:
            return
        if not self.purchaseShopItemInfo:
            return
        self.purchaseShopItemInfo[page][pos] = item
        itemInfo = self._getItemInfo(pos, item)
        if self.mediator:
            self.mediator.Invoke('refreshSingleItem', uiUtils.dict2GfxDict(itemInfo, True))

    def setRefreshCDTip(self):
        cdTime = SCD.data.get('setPurchaseRefreshCD', 5)
        if self.mediator:
            self.mediator.Invoke('setRefreshCDTip', GfxValue(cdTime))

    def onGetBtnTip(self, *arg):
        tip = SCD.data.get('PurchaseShopSellBtnTip', gameStrings.TEXT_PURCHASESHOPPROXY_416)
        return GfxValue(gbk2unicode(tip))

    def _getFameType(self, itemId):
        data = ID.data.get(itemId, {})
        price = data.get('buybackFamePrice', {})
        if price:
            fameType = price.values()[0][0]
            return fameType
        else:
            return 0

    def _getFamePrice(self, itemId):
        data = ID.data.get(itemId, {})
        price = data.get('buybackFamePrice', {})
        if price:
            fameType = price.values()[0][1]
            return fameType
        else:
            return 0

    def onItemClick(self, *arg):
        itemId = arg[3][0].GetNumber()
        data = ID.data.get(itemId, {})
        fameType = self._getFameType(itemId)
        if fameType:
            self.fameType = fameType
            self.refreshFameData()
