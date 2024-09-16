#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/storageProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import utils
from item import Item
from guis import ui
from uiProxy import SlotDataProxy
from guis import uiConst
from callbackHelper import Functor
from guis import uiUtils
from guis import events
from ui import unicode2gbk
from ui import gbk2unicode
from guis import pinyinConvert
from data import item_data as ID
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class StorageProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(StorageProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'storage'
        self.type = 'storage'
        self.modelMap = {'clickClose': self.onClickClose,
         'autoSort': self.onAutoSort,
         'getinitData': self.onGetinitData,
         'getinitTipData': self.onGetinitTipData,
         'clickTipClose': self.onClickTipClose,
         'clickTipConfirmBtn': self.onClickTipConfirmBtn,
         'openTip': self.onOpenTip,
         'setInvItem': self.onSetInvItem,
         'isInDragItem': self.onIsInDragItem,
         'getTipTooltip': self.onGetTipTooltip,
         'useItem': self.onUseItem,
         'leftClickItem': self.onLeftClickItem,
         'useBarItem': self.onUseBarItem,
         'lockStorage': self.onLockStorage,
         'saveCash': self.onSaveCash,
         'getCash': self.onGetCash,
         'enlargeSlot': self.onEnlargeSlot,
         'getItemNames': self.onGetItemNames,
         'getSearchItems': self.onGetSearchItems,
         'clearSearchList': self.onClearSearchList}
        self.mediator = None
        self.tipMediator = None
        self.isAutoSort = True
        self.item = None
        self.npcId = 0
        self.page = const.STORAGE_PAGE_LOW
        self.tipsType = 0
        self.enlargeCost = 0
        self.hasShowPasswordHint = False
        self.searchList = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_STORAGE, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_STORAGE_TIP, self.closeTip)

    @ui.checkInventoryLock()
    def show(self, npcId):
        self.npcId = npcId
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_STORAGE)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_STORAGE:
            self.mediator = mediator
            p = BigWorld.player()
            if gameglobal.rds.configData.get('enableInventoryLock', False):
                p.checkSetPassword()
            BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
            self.enableStorageSearch()
        elif widgetId == uiConst.WIDGET_STORAGE_TIP:
            self.tipMediator = mediator

    def reset(self):
        super(self.__class__, self).reset()
        self.npcId = 0
        self.item = None
        self.page = const.STORAGE_PAGE_LOW
        self.searchList = []

    def onItemChange(self, params):
        if params[0] != const.RES_KIND_STORAGE:
            return
        page = params[1]
        pos = params[2]
        item = BigWorld.player().storage.getQuickVal(page, pos)
        if item == const.CONT_EMPTY_VAL:
            return
        key = self._getKey(page, pos)
        if not self.binding.has_key(key):
            return
        self.binding[key][0].Invoke('refreshTip')
        self.updateSlotState(page, pos)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_STORAGE)
        if self.tipMediator:
            self.tipMediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_STORAGE_TIP)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)

    def clearPassWordHint(self):
        self.hasShowPasswordHint = False

    def onClickClose(self, *arg):
        self.hide()

    def onClickTipClose(self, *arg):
        self.closeTip()

    def closeTip(self):
        self.tipMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_STORAGE_TIP)
        self.item = None
        self.tipsType = 0

    def onAutoSort(self, *arg):
        if self.npcId and BigWorld.entities.get(self.npcId):
            BigWorld.entities.get(self.npcId).cell.autoSortStorage()
            self.setAutoSortAble(False)
            BigWorld.callback(SCD.data.get('autoSortInvCD', 30), Functor(self.setAutoSortAble, True))

    def setAutoSortAble(self, isEnable):
        self.isAutoSort = isEnable
        if self.mediator:
            self.mediator.Invoke('setAutoSortAble', GfxValue(isEnable))

    def updateStorageCash(self, storageCash):
        if self.mediator:
            self.mediator.Invoke('updateStorageCash', GfxValue(str(storageCash)))

    def onGetinitData(self, *arg):
        movie = arg[0]
        initObj = movie.CreateObject()
        bagArr = movie.CreateArray()
        itemArr = movie.CreateArray()
        p = BigWorld.player()
        initObj.SetMember('storageCash', GfxValue(str(p.storageCash)))
        initObj.SetMember('isAutoSort', GfxValue(self.isAutoSort))
        tabCount = p.storage.pageCount
        for i in range(1, p.storage.pageCount):
            posCount = p.storage.posCountDict.get(i, 0)
            if posCount == 0:
                tabCount = i
                break

        initObj.SetMember('enabledPackSlotCnt', GfxValue(p.storage.enabledPackSlotCnt))
        initObj.SetMember('tabCount', GfxValue(tabCount))
        i = 0
        for ps in xrange(p.storage.posCountDict[const.STORAGE_PAGE_LOW]):
            it = p.storage.getQuickVal(self.page, ps)
            if it == const.CONT_EMPTY_VAL:
                continue
            arr = gameglobal.rds.ui.inventory.initItemArr(it, ps)
            bagArr.SetElement(i, arr)
            i += 1

        initObj.SetMember('bagArr', bagArr)
        i = 0
        for ps in xrange(p.storage.enabledPackSlotCnt):
            it = p.storageBar.getQuickVal(0, ps)
            if it == const.CONT_EMPTY_VAL:
                continue
            arr = gameglobal.rds.ui.inventory.initItemArr(it, ps, const.RES_KIND_TEMP_BAG)
            itemArr.SetElement(i, arr)
            i += 1

        initObj.SetMember('itemArr', itemArr)
        return initObj

    def onClickTipConfirmBtn(self, *arg):
        p = BigWorld.player()
        if self.tipsType == 0:
            ent = BigWorld.entities.get(self.npcId)
            if ent:
                if uiUtils.checkBindCashEnough(self.enlargeCost, p.bindCash, p.cash, ent.cell.enlargeStorageSlot):
                    ent.cell.enlargeStorageSlot()
        elif self.tipsType == 1:
            if uiUtils.checkBindCashEnough(self.enlargeCost, p.bindCash, p.cash, p.base.toEnlargeFashionBagSlot):
                p.base.toEnlargeFashionBagSlot()
        self.closeTip()

    def onOpenTip(self, *arg):
        self.showStorageTip(0)

    def showStorageTip(self, type = 0):
        if type == 0:
            if BigWorld.player().storage.enabledPackSlotCnt < const.STORAGE_MAX_SLOT_NUM:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_STORAGE_TIP)
        elif type == 1:
            if BigWorld.player().fashionBag.enabledPackSlotCnt < const.FASHION_BAG_MAX_SLOT_NUM:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_STORAGE_TIP)
        self.tipsType = type

    def onSetInvItem(self, *arg):
        p = BigWorld.player()
        idx = int(arg[3][0].GetNumber())
        for ps in xrange(p.storage.posCount):
            self.removeItem(self.page, ps)

        self.setPage(idx)
        for ps in xrange(p.storage.posCount):
            if gameglobal.rds.ui.inDragStorageItem and gameglobal.rds.ui.dragStoragePageSrc == idx and gameglobal.rds.ui.dragStorageItemSrc == ps:
                continue
            it = p.storage.getQuickVal(idx, ps)
            if it == const.CONT_EMPTY_VAL:
                continue
            self.addItem(it, idx, ps)

        posCount = p.storage.posCountDict.get(idx, 0)
        if posCount != 0:
            self.setSlotCount(posCount)

    def setPage(self, page):
        self.page = page

    def onIsInDragItem(self, *arg):
        return GfxValue(gameglobal.rds.ui.inDragStorageItem or gameglobal.rds.ui.inDragCommonItem or gameglobal.rds.ui.inDragFashionBagItem or gameglobal.rds.ui.inDragMaterialBagItem)

    def onGetinitTipData(self, *arg):
        movie = arg[0]
        initObj = movie.CreateObject()
        p = BigWorld.player()
        if self.tipsType == 0:
            storageEnlargeCost = SCD.data.get('storageEnlargeCost')
        elif self.tipsType == 1:
            storageEnlargeCost = SCD.data.get('fashionBagEnlargeCost')
        else:
            self.closeTip()
            return
        if not storageEnlargeCost:
            self.closeTip()
            return
        if self.tipsType == 1:
            enabledPackSlotCnt = p.fashionBag.enabledPackSlotCnt
        else:
            enabledPackSlotCnt = p.storage.enabledPackSlotCnt
        tipData = storageEnlargeCost[enabledPackSlotCnt]
        self.enlargeCost = tipData[0]
        initObj.SetMember('money', GfxValue(self.enlargeCost))
        initObj.SetMember('playerCash', GfxValue(p.bindCash))
        self.item = Item(tipData[1][0], tipData[1][1], False)
        allCount = p.inv.countItemInPages(int(self.item.getParentId()), enableParentCheck=True)
        itemInfo = self.getItemInfo(self.item.id)
        itemInfo['count'] = uiUtils.convertNumStr(allCount, self.item.cwrap)
        initObj.SetMember('item', uiUtils.dict2GfxDict(itemInfo, True))
        initObj.SetMember('itemCount', GfxValue(self.item.cwrap))
        initObj.SetMember('currentCount', GfxValue(allCount))
        return initObj

    def getItemInfo(self, itemId):
        info = {}
        data = ID.data.get(itemId, {})
        if data:
            info['id'] = itemId
            info['name'] = data.get('name', '')
            info['iconPath'] = uiUtils.getItemIconFile64(itemId)
        return info

    def onGetTipTooltip(self, *arg):
        return self.uiAdapter.inventory.GfxToolTip(self.item)

    def onUseItem(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if self.npcId and BigWorld.entities.get(self.npcId):
            p = BigWorld.player()
            sItem = p.storage.getQuickVal(page, pos)
            if sItem:
                dstPg, dstPos = p.inv.searchBestInPages(sItem.id, sItem.cwrap, sItem)
                if dstPg != const.CONT_NO_PAGE:
                    self.gotoStorage2inv(page, pos, sItem.id, sItem.cwrap, dstPg, dstPos)
                else:
                    p.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())

    @ui.checkInventoryLock()
    def gotoStorage2inv(self, page, pos, itemId, cwrap, dstPg, dstPos):
        if self.npcId:
            npc = BigWorld.entities.get(self.npcId)
            if npc:
                npc.cell.storage2inv(page, pos, itemId, cwrap, dstPg, dstPos, BigWorld.player().cipherOfPerson)

    @ui.checkInventoryLock()
    def gotoStorageSlot2Inv(self, pos, itemId, dstPg, dstPos):
        if self.npcId:
            npc = BigWorld.entities.get(self.npcId)
            if npc:
                npc.cell.storageSlot2Inv(pos, itemId, dstPg, dstPos, BigWorld.player().cipherOfPerson)

    @ui.callFilter(1, True)
    def onLeftClickItem(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        p = BigWorld.player()
        if gameglobal.rds.ui.inventory.isUnlatchState:
            sItem = p.storage.getQuickVal(page, pos)
            if sItem:
                if not sItem.hasLatch():
                    gameglobal.rds.ui.inventory.clearUnlatchState()
                    return
                if sItem.isLatchOfTime():
                    p.base.unLatchTimeStorage(page, pos)
                else:
                    gameglobal.rds.ui.inventoryPassword.show(const.LATCH_ITEM_STORAGE, page, pos)
                gameglobal.rds.ui.inventory.clearUnlatchState()
        elif gameglobal.rds.ui.inventory.isLatchTimeState:
            sItem = p.storage.getQuickVal(page, pos)
            if sItem:
                if not sItem.canLatch():
                    BigWorld.player().showGameMsg(GMDD.data.LATCH_FORBIDDEN_NO_LATCH, ())
                    return
                gameglobal.rds.ui.inventoryLatchTime.show(const.LATCH_ITEM_STORAGE, page, pos)
                gameglobal.rds.ui.inventory.clearLatchTimeState()
        elif gameglobal.rds.ui.inventory.isLatchCipherState:
            item = p.storage.getQuickVal(page, pos)
            if item:
                if not item.hasLatch():
                    p.base.latchCipherStorage(page, pos)
                else:
                    uiUtils.unLatchItem(item, const.LATCH_ITEM_STORAGE, page, pos)

    def onUseBarItem(self, *arg):
        pass

    def getSlotID(self, key):
        idPage, idPos = key.split('.')
        pos = int(idPos[4:])
        page = int(idPage[7:])
        if page == 1:
            return (const.STORAGE_PAGE_BAG, pos)
        return (self.page, pos)

    def _getKey(self, page, pos):
        return 'storage%d.slot%d' % (page, pos)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        if page == const.STORAGE_PAGE_BAG:
            i = p.storageBar.getQuickVal(0, pos)
        else:
            i = p.storage.getQuickVal(page, pos)
        if i == None:
            return
        else:
            return gameglobal.rds.ui.inventory.GfxToolTip(i)

    def updateSlotState(self, page, pos):
        if self.page != page:
            return
        p = BigWorld.player()
        item = p.storage.getQuickVal(page, pos)
        if item == const.CONT_EMPTY_VAL:
            return
        key = self._getKey(0, pos)
        if item.type == Item.BASETYPE_CONSUMABLE:
            gameglobal.rds.ui.actionbar.playCooldown(0, pos, item.id, False, True)
        if not self.binding.has_key(key):
            return
        if not gameglobal.rds.ui.inventory.isfilter(item):
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_GRAY))
        elif item.isMallFashionRenewable() and item.isExpireTTL():
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_EXPIRE_TIME_RE))
        elif not item.isMallFashionRenewable() and item.isExpireTTL():
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_EXPIRE_TIME))
        elif not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_NOT_USE))
        elif item.isLatchOfTime():
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_LATCH_TIME))
        elif hasattr(item, 'latchOfCipher'):
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_LATCH_CIPHER))
        elif item.type == Item.BASETYPE_EQUIP and (hasattr(item, 'cdura') and item.cdura == 0 or item.canEquip(p, item.whereEquip()[0])):
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_BROKEN))
        elif hasattr(item, 'shihun') and item.shihun == True:
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_SHIHUN_REPAIR))
        else:
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))

    def updateCurrentPageSlotState(self):
        if self.mediator:
            posCount = BigWorld.player().storage.posCountDict.get(self.page, 0)
            for pos in xrange(0, posCount):
                self.updateSlotState(self.page, pos)

    def addItem(self, item, page, pos):
        if self.page != page:
            return
        else:
            if item is not None:
                key = self._getKey(0, pos)
                self.addRealItem(key, item)
                self.updateSlotState(page, pos)
                if self.searchList:
                    self.binding[key][0].Invoke('setSearchState', GfxValue(self.inSearchList(item.uuid)))
            return

    def addBarItem(self, item, pos):
        if item is not None:
            key = self._getKey(1, pos)
            self.addRealItem(key, item)

    def addRealItem(self, key, item):
        if self.binding.get(key, None) is not None:
            data = uiUtils.getGfxItem(item)
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))

    def removeItem(self, page, pos):
        if self.page != page:
            return
        else:
            key = self._getKey(0, pos)
            if self.binding.get(key, None) is not None:
                data = GfxValue(1)
                data.SetNull()
                self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
                self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
                self.binding[key][0].Invoke('setSearchState', GfxValue(False))
                self.binding[key][1].InvokeSelf(data)
                gameglobal.rds.ui.actionbar.stopCoolDown(0, pos, False, True)
            return

    def removeBarItem(self, pos):
        key = self._getKey(1, pos)
        if self.binding.get(key, None) is not None:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)

    def enablePackSlot(self, pos):
        if self.mediator:
            self.mediator.Invoke('enablePackSlot', GfxValue(pos))

    def setBagTabAble(self, tabPos, isEnable):
        if self.mediator:
            self.mediator.Invoke('setBagTabAble', (GfxValue(tabPos), GfxValue(isEnable)))

    def setSlotCount(self, slotCount):
        if self.mediator:
            self.mediator.Invoke('setSlotCount', GfxValue(slotCount))

    def setFirstTab(self):
        if self.mediator:
            self.mediator.Invoke('setFirstTab')

    def onLockStorage(self, *arg):
        p = BigWorld.player()
        if not p.hasInvPassword:
            gameglobal.rds.ui.inventorySetPassword.show()
        else:
            gameglobal.rds.ui.inventoryResetPassword.show()

    def onSaveCash(self, *arg):
        gameglobal.rds.ui.storageCash.show(0)

    def onGetCash(self, *arg):
        gameglobal.rds.ui.storageCash.show(1)

    def inSearchList(self, uuid):
        for pg in self.searchList:
            for item in pg:
                if item[2] == uuid:
                    return True

        return False

    def onClearSearchList(self, *args):
        self.searchList = []

    def _updateSearchList(self):
        p = BigWorld.player()
        if self.searchList:
            for pg in self.searchList:
                for item in pg:
                    it = p.storage.getQuickVal(item[0], item[1])
                    if it.uuid != item[2]:
                        pg.remove(item)

    def onGetItemNames(self, *arg):
        p = BigWorld.player()
        text = unicode2gbk(arg[3][0].GetString())
        ret = []
        if text == '':
            return uiUtils.array2GfxAarry(ret)
        text = text.lower()
        searchList = p.storage.searchAllByName(text, self.findItemFunc)
        for pg in searchList:
            for item in pg:
                it = p.storage.getQuickVal(item[0], item[1])
                name = gbk2unicode(it.name)
                if name not in ret:
                    ret.append(gbk2unicode(it.name))

        return uiUtils.array2GfxAarry(ret)

    def onGetSearchItems(self, *args):
        name = args[3][0].GetString()
        p = BigWorld.player()
        self.searchList = p.storage.searchAllByName(unicode2gbk(name), self.findItemFunc)
        return uiUtils.array2GfxAarry(self.searchList)

    def findItemFunc(self, itemName, name):
        find = False
        isPinyinAndHanzi = utils.isPinyinAndHanzi(name)
        if isPinyinAndHanzi == const.STR_ONLY_PINYIN:
            itemName2 = pinyinConvert.strPinyinFirst(itemName)
            find = itemName2.find(name) != -1
        else:
            find = itemName.find(name) != -1
        return find

    def enableStorageSearch(self):
        enableSearch = gameglobal.rds.configData.get('enableStorageSearch', True)
        if self.mediator:
            self.mediator.Invoke('enableSearch', GfxValue(enableSearch))

    def _transferCashToStorage(self, amount):
        if self.npcId:
            npc = BigWorld.entities.get(self.npcId)
            if npc:
                npc.cell.transferCashToStorage(amount)

    @ui.checkInventoryLock()
    def _drawCashFromStorage(self, amount):
        if self.npcId:
            npc = BigWorld.entities.get(self.npcId)
            if npc:
                npc.cell.drawCashFromStorage(amount, BigWorld.player().cipherOfPerson)

    def onEnlargeSlot(self, *arg):
        gameglobal.rds.ui.expandPay.updateNpcId(self.npcId)
        gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_STORAGE_EXPAND, arg[3][0].GetNumber())

    @ui.uiEvent(uiConst.WIDGET_STORAGE, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onStorageItemClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            p = BigWorld.player()
            if self.npcId:
                ent = BigWorld.entities.get(self.npcId)
                if not ent:
                    return
                if i.isOneQuest():
                    p.showGameMsg(GMDD.data.ITEM_CAN_NOT_MOVE_TO_STORAGE, ())
                    return
                emptyPg, emptyPos = p.storage.searchBestInPages(i.id, i.cwrap, i)
                if emptyPg != const.CONT_NO_PAGE:
                    ent.cell.inv2storage(nPage, nItem, i.cwrap, emptyPg, emptyPos)
                else:
                    p.showGameMsg(GMDD.data.STORAGE_FULL, ())
            return
