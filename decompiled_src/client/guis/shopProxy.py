#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/shopProxy.o
from gamestrings import gameStrings
import BigWorld
import const
import gameglobal
import gamelog
import gametypes
import item
import uiConst
from guis import cursor
from guis import ui
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from Scaleform import GfxValue
from callbackHelper import Functor
from item import Item
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class ShopProxy(SlotDataProxy):
    OPTION_SHOP = 0
    OPTION_BUY_BACK = 1

    def __init__(self, uiAdapter):
        super(ShopProxy, self).__init__(uiAdapter)
        self.modelMap = {'getMoney': self.onGetMoney,
         'getItemList': self.onGetItemList,
         'getPageCount': self.onGetPageCount,
         'changePage': self.onChangePage,
         'buyItem': self.onBuyItem,
         'sendItem': self.onSendItem,
         'recieveItem': self.onRecieveItem,
         'closeQuantity': self.onCloseQuantity,
         'buySingleItem': self.onBuySingleItem,
         'buyFailed': self.onBuyFailed,
         'fitting': self.onFitting,
         'setOption': self.onSetOption,
         'repair': self.onRepair,
         'batchRepair': self.onBatchRepair,
         'canRepair': self.onCanRepair,
         'buyBackItem': self.onBuyBackItem}
        self.bindType = 'shop'
        self.type = 'shop'
        self.show = False
        self.infoDic = {}
        self.mediator = None
        self.quantityMediator = None
        self.page = None
        self.pos = None
        self.currPage = None
        self.npcId = None
        self.option = self.OPTION_SHOP
        self.pageStamp = {}
        self.inRepair = False
        self.canRepair = False
        self.itemPage = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SHOP, Functor(self.hide, True))
        uiAdapter.registerEscFunc(uiConst.WIDGET_SHOP_QUANTITY, Functor(self.onCloseQuantity, None))

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SHOP:
            self.mediator = mediator
            self.show = True
            if self.itemPage:
                self.mediator.Invoke('setPageItem', self.itemPage)
                self.itemPage = None
        elif widgetId == uiConst.WIDGET_SHOP_QUANTITY:
            self.quantityMediator = mediator

    def getIsShow(self):
        return self.show

    def onRepair(self, *arg):
        gameglobal.rds.sound.playSound(gameglobal.SD_27)
        npc = BigWorld.entity(self.npcId)
        canRepair = npc.canRepairInfo[BigWorld.player().openShopId]
        if not npc or not canRepair:
            return
        if gameglobal.rds.ui.roleInfo.isShow:
            gameglobal.rds.ui.roleInfo.hide()
        gameglobal.rds.ui.roleInfo.show()
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()
        self.inRepair = True
        if ui.get_cursor_state() != ui.REPAIR_STATE:
            ui.reset_cursor()
            self.cursorLock = False
            ui.set_cursor_state(ui.REPAIR_STATE)
            ui.set_cursor(cursor.repair)
            ui.lock_cursor()
            self.cursorLock = True

    def doRepair(self, page, pos):
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            return
        if p.inCombat:
            p.showGameMsg(GMDD.data.REPAIR_FORBIDDEN_IN_COMBAT, ())
            return
        if page == const.INV_PAGE_EQUIP:
            equip = p.equipment.get(pos)
        elif page == const.INV_PAGE_SUBEQUIP:
            equip = p.subEquipment.get(const.DEFAULT_SUB_EQU_PAGE_NO, pos)
        else:
            equip = p.inv.getQuickVal(page, pos)
        if equip == const.CONT_EMPTY_VAL:
            return
        if not equip.isEquip():
            p.showGameMsg(GMDD.data.REPAIR_ITEM_CAN_NOT_REPAIR, (equip.name,))
            return
        if not equip.canRepair():
            p.showGameMsg(GMDD.data.REPAIR_EQUIP_CAN_NOT_REPAIR, (equip.name,))
            return
        if not equip.needRepair():
            p.showGameMsg(GMDD.data.REPAIR_NEED_NOT_REPAIR, (equip.name,))
            return
        cost = equip.repairCost(p.school, p.lv)
        if not p.canPay(cost):
            p.showGameMsg(GMDD.data.REPAIR_NO_ENOUGH_CASH, ())
            return
        msg = GMD.data.get(GMDD.data.REPAIR_COST, {}).get('text', gameStrings.TEXT_SHOPPROXY_141)
        msg = msg % (equip.name, cost)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.gotoDoRepairConfirm, cost, page, pos))

    def gotoDoRepairConfirm(self, cost, page, pos):
        p = BigWorld.player()
        if uiUtils.checkBindCashEnough(cost, p.bindCash, p.cash, Functor(self.doRepairConfirm, page, pos)):
            self.doRepairConfirm(page, pos)

    def doRepairConfirm(self, page, pos):
        npc = BigWorld.entity(self.npcId)
        if npc:
            npc.cell.repair(BigWorld.player().openShopId, page, pos)

    def onBatchRepair(self, *arg):
        gameglobal.rds.sound.playSound(gameglobal.SD_27)
        npc = BigWorld.entity(self.npcId)
        canRepair = npc.canRepairInfo[BigWorld.player().openShopId]
        if not npc:
            return
        if not npc.inWorld or not canRepair:
            return
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            return
        if p.inCombat:
            p.showGameMsg(GMDD.data.REPAIR_FORBIDDEN_IN_COMBAT, ())
            return
        totalCost = 0
        tmp = []
        for equip in p.equipment:
            if not equip or not equip.isEquip() or not equip.canRepair():
                continue
            if not equip.needRepair():
                continue
            totalCost += equip.repairCost(p.school, p.lv)
            tmp.append(equip)

        if not tmp:
            p.showGameMsg(GMDD.data.REPAIR_NO_EQUIP_NEED_REPAIR, ())
            return
        if not p.canPay(totalCost):
            p.showGameMsg(GMDD.data.REPAIR_NO_ENOUGH_CASH, ())
            return
        self.inRepair = True
        msg = GMD.data.get(GMDD.data.REPAIR_ALL_COST, {}).get('text', gameStrings.TEXT_SHOPPROXY_200)
        msg = msg % (totalCost,)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.gotoDoBatchRepairConfirm, totalCost))

    def gotoDoBatchRepairConfirm(self, cost):
        p = BigWorld.player()
        if uiUtils.checkBindCashEnough(cost, p.bindCash, p.cash, self.doBatchRepairConfirm):
            self.doBatchRepairConfirm()

    def doBatchRepairConfirm(self):
        npc = BigWorld.entity(self.npcId)
        if npc and BigWorld.player().openShopId:
            npc.cell.repairAll(BigWorld.player().openShopId)
            self.clearRepairState()

    def cancelBatchRepair(self):
        self.clearRepairState()

    def onCanRepair(self, *arg):
        return GfxValue(self.canRepair)

    def onSetOption(self, *arg):
        self.option = int(arg[3][0].GetNumber())
        if self.option == self.OPTION_SHOP:
            ent = BigWorld.entities.get(self.npcId)
            if ent and BigWorld.player().openShopId:
                stamp = self.pageStamp.get(self.currPage, 0)
                ent.cell.turnPage(BigWorld.player().openShopId, self.currPage, stamp)
        elif self.option == self.OPTION_BUY_BACK:
            self._setBuyBackItem()
            self.onCloseQuantity()

    def onBuyFailed(self, *arg):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.SHOP_MONEY_LESS, ())

    @ui.callFilter(0.5, False)
    def onBuyItem(self, *arg):
        try:
            num = int(arg[3][0].GetNumber())
        except:
            return

        it = self.infoDic.get(self.page, {}).get(self.pos, None)
        if not it:
            gamelog.error('shopProxy, no data in infoDic ', self.page, self.pos)
            return
        else:
            judge = (1, it.mwrap, GMDD.data.ITEM_TRADE_NUM)
            if not ui.inputRangeJudge(judge, num, (it.mwrap,)):
                return
            p = BigWorld.player()
            if num > item.Item.maxWrap(it.id):
                p.showGameMsg(GMDD.data.SHOP_BUY_ITEM_OVER_MWRAP, ())
                return
            if ID.data.get(it.id, {}).get('needOwner'):
                it.setOwner(p.gbId, p.realRoleName)
            bagPage, bagPos = self._findBestPos(it, num)
            if bagPage == const.CONT_NO_PAGE or bagPos == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())
                return
            if self.option == self.OPTION_SHOP:
                totalPrice = int(it.bPrice) * num
                priceType = ID.data.get(it.id, {}).get('bPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
                if priceType == gametypes.ITEM_PRICE_TYPE_BIND_CASH:
                    if uiUtils.checkBindCashEnough(totalPrice, p.bindCash, p.cash, Functor(self.gotoSell, self.page, self.pos, num, bagPage, bagPos)):
                        self.gotoSell(self.page, self.pos, num, bagPage, bagPos)
                else:
                    self.gotoSell(self.page, self.pos, num, bagPage, bagPos)
            elif self.option == self.OPTION_BUY_BACK:
                self.retrieve(self.pos)
            self.onCloseQuantity()
            return

    def _findBestPos(self, it, num):
        if it.isOneQuest():
            bagPage, bagPos = BigWorld.player().questBag.searchBestInPages(it.id, num, it)
        elif BigWorld.player()._isInCross():
            if gameglobal.rds.configData.get('enableWingWorld', False):
                bagPage, bagPos = BigWorld.player().crossInv.searchBestInPages(it.id, num, it)
        else:
            bagPage, bagPos = BigWorld.player().inv.searchBestInPages(it.id, num, it)
        return (bagPage, bagPos)

    def onFitting(self, *arg):
        page = int(arg[3][0].GetNumber())
        pos = int(arg[3][1].GetNumber())
        ent = BigWorld.entity(self.npcId)
        if not ent:
            return
        else:
            if self.option == self.OPTION_SHOP:
                it = self.infoDic.get(page, {}).get(pos, None)
                if it:
                    gameglobal.rds.ui.fittingRoom.addItem(it)
            return

    @ui.callFilter(0.5, False)
    def onBuySingleItem(self, *arg):
        page = int(arg[3][0].GetNumber())
        pos = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        if self.option == self.OPTION_SHOP:
            it = self.infoDic.get(page, {}).get(pos, None)
            if not it:
                gamelog.error('shopProxy, no data in infoDic ', page, pos)
                return
            if ID.data.get(it.id, {}).get('needOwner'):
                it.setOwner(p.gbId, p.realRoleName)
            bagPage, bagPos = self._findBestPos(it, 1)
            if bagPage == const.CONT_NO_PAGE or bagPos == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())
                return
            totalPrice = int(it.bPrice)
            priceType = ID.data.get(it.id, {}).get('bPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
            if priceType == gametypes.ITEM_PRICE_TYPE_BIND_CASH:
                if uiUtils.checkBindCashEnough(totalPrice, p.bindCash, p.cash, Functor(self.gotoSell, page, pos, 1, bagPage, bagPos)):
                    self.gotoSell(page, pos, 1, bagPage, bagPos)
            else:
                self.gotoSell(page, pos, 1, bagPage, bagPos)
        elif self.option == self.OPTION_BUY_BACK:
            self.retrieve(pos)

    def gotoSell(self, page, pos, num, bagPage, bagPos):
        ent = BigWorld.entity(self.npcId)
        if ent and BigWorld.player().openShopId:
            ent.cell.sell(BigWorld.player().openShopId, page, pos, num, bagPage, bagPos)
            gameglobal.rds.sound.playSound(gameglobal.SD_26)

    def gotoRetrieve(self, pos):
        ent = BigWorld.entity(self.npcId)
        if ent and BigWorld.player().openShopId:
            ent.cell.retrieve(BigWorld.player().openShopId, pos)
            gameglobal.rds.sound.playSound(gameglobal.SD_26)

    def onChangePage(self, *arg):
        if self.option == self.OPTION_BUY_BACK:
            return
        self.currPage = int(arg[3][0].GetNumber())
        ent = BigWorld.entities.get(self.npcId)
        if ent:
            stamp = self.pageStamp.get(self.currPage, 0)
            ent.cell.turnPage(BigWorld.player().openShopId, self.currPage, stamp)

    def onGetPageCount(self, *arg):
        self.show = True
        return GfxValue(self.pageCount)

    def onRegisterShop(self, *arg):
        pass

    def onGetMoney(self, *arg):
        return GfxValue(str(BigWorld.player().cash + BigWorld.player().bindCash))

    def refreshMoney(self):
        if self.mediator != None:
            self.mediator.Invoke('refreshMoney')

    def onGetItemList(self, *arg):
        itemList = self.movie.CreateArray()
        for i in range(0, 20):
            obj = self.movie.CreateObject()
            obj.SetMember('name', GfxValue(gbk2unicode(gameStrings.TEXT_BATTLEFIELDSHOPPROXY_171)))
            obj.SetMember('value', GfxValue(str((i + 1) * 100)))
            itemList.SetElement(i, obj)

        return itemList

    def setPageCount(self):
        self.mediator.Invoke('setPageCount', GfxValue(self.pageCount))

    @ui.callAfterTime()
    def refreshInfoByCache(self):
        if not self.mediator:
            return
        stamp = self.pageStamp.get(self.currPage, 0)
        self.setPageItem(self.currPage, stamp)

    def setPageItem(self, page, stamp, info = None, forceUpdate = False):
        self.pageStamp[page] = stamp
        self.currPage = page
        if info != None:
            self.infoDic[page] = {}
            for i, itemData in enumerate(info):
                self.infoDic[page][i] = itemData

        itemArray = []
        p = BigWorld.player()
        questItemIdList = p.getUnfinishedQuestNeedItemIdList()
        pageInfo = self.infoDic.get(page, {})
        for pos in xrange(len(pageInfo)):
            it = pageInfo[pos]
            remainNum = getattr(it, 'remainNum', 1)
            data = ID.data.get(it.id, {})
            if data.get('quality') == 0 and data.get('type') == Item.BASETYPE_EQUIP:
                it = Item(it.id)
            itemInfo = uiUtils.getGfxItem(it)
            itemInfo['name'] = uiUtils.getItemColorNameByItem(it)
            itemInfo['value'] = str(it.bPrice)
            if not it.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                itemInfo['state'] = uiConst.EQUIP_NOT_USE
            else:
                itemInfo['state'] = uiConst.ITEM_NORMAL
            itemInfo['priceType'] = data.get('bPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
            itemInfo['mwrap'] = data.get('mwrap', 1)
            itemInfo['count'] = remainNum
            itemInfo['questFlagVisible'] = it.id in questItemIdList
            itemArray.append(itemInfo)

        otherInfo = {}
        otherInfo['money'] = str(p.cash + p.bindCash)
        otherInfo['page'] = page + 1
        itemArray.append(otherInfo)
        if self.mediator:
            self.mediator.Invoke('setPageItem', uiUtils.array2GfxAarry(itemArray, True))
        else:
            self.itemPage = uiUtils.array2GfxAarry(itemArray, True)
        if forceUpdate:
            self.setCurrentPage(page, forceUpdate)

    def setSingleItem(self, page, pos, item):
        if self.infoDic:
            it = self.infoDic.get(page, {}).get(pos, None)
            if it:
                num = item.remainNum
                it.remainNum = num
                self.infoDic[page][pos] = it
                if page == self.currPage and self.mediator:
                    self.mediator.Invoke('setSingleItem', (GfxValue(page), GfxValue(pos), GfxValue(num)))

    def onCloseShop(self, *arg):
        self.hide()

    def clearWidget(self):
        self.show = False
        self.option = self.OPTION_SHOP
        self.pageStamp = {}
        if self.inRepair:
            self.clearRepairState()
        if self.npcId and BigWorld.player().openShopId:
            ent = BigWorld.entity(self.npcId)
            if ent:
                ent.cell.closeShop(BigWorld.player().openShopId)
        self.uiAdapter.playLeaveAction(self.npcId)
        BigWorld.player().openShopId = 0
        BigWorld.player().openShopType = 0
        self.npcId = 0
        self.mediator = None
        self.onCloseQuantity()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        if self.inRepair:
            self.clearRepairState()
        for val in gameglobal.rds.ui.messageBox.loadeds.values():
            if val[1] == uiConst.MESSAGEBOX_SHOP:
                gameglobal.rds.ui.messageBox.dismiss()

        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHOP)

    def onSendItem(self, *arg):
        self.page = int(arg[3][0].GetNumber())
        self.pos = int(arg[3][1].GetNumber())
        isEmpty = arg[3][2].GetBool()
        if isEmpty:
            BigWorld.player().showGameMsg(GMDD.data.SHOP_ITEM_SOLD_OUT, ())
            return
        if not self.quantityMediator:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SHOP_QUANTITY)
        else:
            self.quantityMediator.Invoke('initItem', self.onRecieveItem())

    def onRecieveItem(self, *arg):
        obj = {}
        item = self.infoDic.get(self.page, {}).get(self.pos, None)
        if not item:
            gamelog.error('shopProxy, no data in infoDic ', self.page, self.pos)
            return obj
        else:
            p = BigWorld.player()
            data = ID.data.get(item.id, {})
            obj = uiUtils.getGfxItem(item, appendInfo={'itemId': item.id})
            obj['name'] = uiUtils.getItemColorNameByItem(item)
            obj['value'] = item.bPrice
            priceType = data.get('bPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
            obj['priceType'] = priceType
            if not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                obj['state'] = uiConst.EQUIP_NOT_USE
            else:
                obj['state'] = uiConst.ITEM_NORMAL
            num = item.remainNum
            obj['num'] = num
            if item.remainNum == -1:
                mwrap = self.checkMaxNum(item, item.mwrap, data)
            else:
                mwrap = self.checkMaxNum(item, min(item.remainNum, item.mwrap), data)
            if mwrap <= 0:
                mwrap = 1
            obj['mwrap'] = mwrap
            obj['money'] = BigWorld.player().cash + BigWorld.player().bindCash
            return uiUtils.dict2GfxDict(obj, True)

    def checkMaxNum(self, item, mwrap, data):
        low = 1
        high = mwrap
        while low <= high:
            mid = (low + high) / 2
            if self._checkMaxNum(item, mid, data):
                low = mid + 1
            else:
                high = mid - 1

        return high

    def _checkMaxNum(self, item, maxNum, data):
        owner = BigWorld.player()
        consumeCash = item.bPrice
        if consumeCash == 0:
            return True
        consumeCashType = data.get('bPriceType', gametypes.CONSUME_CASH_TYPE_NO_LIMIT)
        consumeCash *= maxNum
        if consumeCashType in (gametypes.CONSUME_CASH_TYPE_NO_LIMIT, gametypes.CONSUME_CASH_TYPE_BIND_CASH):
            if not owner._canPay(consumeCash):
                return False
        elif consumeCashType == gametypes.CONSUME_CASH_TYPE_CASH:
            if owner.cash < consumeCash:
                return False
        return True

    def onSellReItem(self, *arg):
        pass

    def onCloseQuantity(self, *arg):
        self.quantityMediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SHOP_QUANTITY)

    def delayedShowShop(self, shopId):
        BigWorld.player().openShopId = shopId
        BigWorld.player().openShopType = const.SHOP_TYPE_COMMON
        self.uiAdapter.loadWidget(uiConst.WIDGET_SHOP)
        ent = BigWorld.entities.get(self.npcId)
        if ent:
            stamp = self.pageStamp.get(self.currPage, 0)
            ent.cell.turnPage(shopId, self.currPage, stamp)

    @ui.callFilter(1)
    def showShop(self, npcId, shopId, pageCount, discount, layoutType = uiConst.LAYOUT_DEFAULT):
        gamelog.debug('showShop', npcId, self.npcId, self.show)
        p = BigWorld.player()
        if p.openShopId == shopId and self.show:
            return False
        p.openShopId = shopId
        p.openShopType = const.SHOP_TYPE_COMMON
        p.stopAutoQuest()
        closeShopFlag = False
        if p.openShopId != shopId and self.show:
            self.onCloseShop(0)
            closeShopFlag = True
        self.npcId = npcId
        self.pageCount = pageCount
        self.discount = discount
        self.pageStamp = {}
        self.option = self.OPTION_SHOP
        self.currPage = 0
        ent = BigWorld.entities.get(npcId)
        self.canRepair = ent.canRepairInfo[shopId]
        if not gameglobal.rds.ui.enableUI:
            BigWorld.player().showUI(True)
        if closeShopFlag:
            BigWorld.callback(0.5, Functor(self.delayedShowShop, shopId))
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SHOP, layoutType=layoutType)
        return True

    def getSlotID(self, key):
        return (self.currPage, int(key[9:]))

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if self.option == self.OPTION_SHOP:
            it = self.infoDic.get(page, {}).get(pos, None)
            if it == None:
                return
        elif self.option == self.OPTION_BUY_BACK:
            p = BigWorld.player()
            its = p.buyBackDict.get(const.BUY_BACK_SHOP_PAGE, [])
            it = None
            if its and pos < len(its):
                it = its[pos]
            if it == None:
                return
        if self.option == self.OPTION_BUY_BACK:
            ret = gameglobal.rds.ui.inventory.GfxToolTip(it)
        else:
            data = ID.data.get(it.id, {})
            if data.get('quality') == 0 and data.get('type') == Item.BASETYPE_EQUIP:
                it = Item(it.id)
            ret = gameglobal.rds.ui.inventory.GfxToolTip(it, const.ITEM_IN_SHOP)
        return ret

    def setCurrentPage(self, page, forceUpdate = False):
        if self.mediator:
            self.mediator.Invoke('setPage', (GfxValue(page), GfxValue(forceUpdate)))

    def clearRepairState(self):
        self.inRepair = False
        if ui.get_cursor_state() == ui.REPAIR_STATE:
            ui.reset_cursor()
            self.cursorLock = False

    def _setBuyBackItem(self):
        if self.mediator:
            p = BigWorld.player()
            if const.BUY_BACK_SHOP_PAGE in p.buyBackDict:
                itemList = p.buyBackDict[const.BUY_BACK_SHOP_PAGE]
            else:
                itemList = []
            itemArray = []
            for it in itemList:
                if it == None:
                    continue
                data = ID.data.get(it.id, {})
                itemInfo = uiUtils.getGfxItem(it)
                itemInfo['name'] = uiUtils.getItemColorNameByItem(it)
                itemInfo['value'] = str(it.sPrice)
                if not it.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                    itemInfo['state'] = uiConst.EQUIP_NOT_USE
                else:
                    itemInfo['state'] = uiConst.ITEM_NORMAL
                itemInfo['priceType'] = data.get('sPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
                itemInfo['mwrap'] = data.get('mwrap', 1)
                itemArray.append(itemInfo)

            otherInfo = {}
            otherInfo['money'] = str(p.cash + p.bindCash)
            otherInfo['page'] = 0
            itemArray.append(otherInfo)
            self.mediator.Invoke('setPageItem', uiUtils.array2GfxAarry(itemArray, True))

    def updateBuyBackItem(self):
        if self.option != self.OPTION_BUY_BACK:
            return
        self._setBuyBackItem()

    def onBuyBackItem(self, *arg):
        pos = int(arg[3][0].GetNumber())
        self.retrieve(pos)

    def retrieve(self, pos):
        p = BigWorld.player()
        items = p.buyBackDict.get(const.BUY_BACK_SHOP_PAGE, [])
        item = None
        if items and pos < len(items):
            item = items[pos]
        if not item:
            return
        else:
            num = item.cwrap
            totalPrice = int(item.sPrice) * num
            priceType = ID.data.get(item.id, {}).get('sPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
            if priceType == gametypes.ITEM_PRICE_TYPE_BIND_CASH:
                if uiUtils.checkBindCashEnough(totalPrice, p.bindCash, p.cash, Functor(self.gotoRetrieve, pos)):
                    self.gotoRetrieve(pos)
            else:
                self.gotoRetrieve(pos)
            return
