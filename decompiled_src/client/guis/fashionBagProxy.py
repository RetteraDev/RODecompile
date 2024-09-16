#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fashionBagProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gametypes
import ui
import item
from helpers.eventDispatcher import Event
from guis import events
from item import Item
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from data import consumable_item_data as CID
from cdata import game_msg_def_data as GMDD
from cdata import material_dye_data as MDD

class FashionBagProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(FashionBagProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'FashionBag'
        self.type = 'FashionBag'
        self.modelMap = {'openPicBag': self.onOpenPicBag,
         'setFashionBagItem': self.onSetFashionBagItem,
         'selectedType': self.onSelectedType,
         'openAutoFetch': self.onOpenAutoFetch,
         'useItem': self.onUseItem,
         'sortItem': self.onSortItem,
         'getinitData': self.onGetinitData,
         'getFashionBagPageCount': self.onGetFashionBagPageCount,
         'expendBag': self.onExpendBag,
         'setInvItem': self.onSetInvItem,
         'isInDragItem': self.onIsInDragItem,
         'clickItem': self.onClickItem}
        self.mediator = None
        self.isAutoSortInventory = True
        self.page = const.FASHION_BAG_PAGE_LOW
        self.itemFilter = uiConst.FILTER_ITEM_ALL
        self.isDyePlaneState = False
        self.dyeItemPage = const.CONT_NO_PAGE
        self.dyeItemPos = const.CONT_NO_POS
        self.isDyePlaneState = False
        self.isDyeState = False
        self.checkDisableProxys = ['itemMsgBox']
        uiAdapter.registerEscFunc(uiConst.WIDGET_FASHION_BAG, self.hide)

    def onExpendBag(self, *args):
        gameglobal.rds.ui.storage.showStorageTip(1)

    def onGetFashionBagPageCount(self, *args):
        p = BigWorld.player()
        return GfxValue(p.fashionBag.pageCount)

    def onSetInvItem(self, *arg):
        p = BigWorld.player()
        idx = int(arg[3][0].GetNumber())
        for ps in xrange(p.fashionBag.posCount):
            self.removeItem(self.page, ps)

        self.setPage(idx)
        for ps in xrange(p.fashionBag.posCount):
            it = p.fashionBag.getQuickVal(idx, ps)
            if it == const.CONT_EMPTY_VAL:
                continue
            self.addItem(it, idx, ps)

        posCount = p.fashionBag.posCountDict.get(idx, 0)
        if posCount != 0:
            self.setSlotCount(posCount)

    def onIsInDragItem(self, *arg):
        return GfxValue(gameglobal.rds.ui.inDragStorageItem or gameglobal.rds.ui.inDragCommonItem or gameglobal.rds.ui.inDragFashionBagItem or gameglobal.rds.ui.inDragMaterialBagItem)

    def onClickItem(self, *arg):
        if not gameglobal.rds.configData.get('enableFashionBagRenew', False):
            return
        itemId = arg[3][0]
        nPage, nItem = self.getSlotID(itemId.GetString())
        p = BigWorld.player()
        if ui.get_cursor_state() == ui.RENEWAL_STATE2:
            i = BigWorld.player().fashionBag.getQuickVal(nPage, nItem)
            if i:
                if i.isMallFashionRenewable():
                    gameglobal.rds.ui.itemResume.show(i, nPage, nItem, const.RES_KIND_FASHION_BAG)
            return GfxValue(True)
        if ui.get_cursor_state() == ui.RENEWAL_STATE:
            self.doRenewerItem(nPage, nItem)

    def doRenewerItem(self, nPage, nItem):
        stateParams = gameglobal.rds.ui.inventory.stateParams
        p = BigWorld.player()
        i = BigWorld.player().fashionBag.getQuickVal(nPage, nItem)
        if i == const.CONT_EMPTY_VAL:
            return
        if i.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        renewalItem = p.inv.getQuickVal(stateParams[0], stateParams[1])
        if renewalItem:
            if renewalItem.hasLatch():
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
        else:
            return
        if not i.canRenewalIndependent():
            p.showGameMsg(GMDD.data.ITEM_CAN_NOT_RENEWAL, ())
            return
        if getattr(renewalItem, 'cstype', 0) != item.Item.SUBTYPE_2_ITEM_RENEWAL:
            return
        renewalType = CID.data.get(renewalItem.id, {}).get('renewalType', -1)
        if i.getRenewalType() == renewalType:
            name = uiUtils.getItemColorName(i.id)
            renewalItemName = uiUtils.getItemColorName(renewalItem.id)
            desc = gameStrings.TEXT_FASHIONBAGPROXY_126 % (name, renewalItemName)
            self.uiAdapter.messageBox.showYesNoMsgBox(desc, Functor(self.onRealResume, stateParams[0], stateParams[1], nPage, nItem, const.RES_KIND_FASHION_BAG), gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)
        else:
            p.showGameMsg(GMDD.data.ITEM_NOT_RENEWAL_SAME_TYPE, ())
            return

    def onRealResume(self, srcPage, srcPos, tgtPage, tgtPos, resKind):
        BigWorld.player().cell.renewalItemOfUse(srcPage, srcPos, tgtPage, tgtPos, resKind)

    def getFashionBagSlotCount(self):
        p = BigWorld.player()
        if hasattr(p.fashionBag, 'enabledSlotCnt'):
            return p.fashionBag.enabledSlotCnt
        else:
            return p.fashionBag.posCount

    def getPageSlotCount(self, page):
        count = self.getFashionBagSlotCount()
        p = BigWorld.player()
        if count > page * p.fashionBag.posCount:
            return p.fashionBag.posCount
        else:
            return count - (page - 1) * p.fashionBag.posCount

    def refreshBag(self):
        if self.mediator:
            p = BigWorld.player()
            self.mediator.Invoke('initBagTab', GfxValue(p.fashionBag.pageCount))
            pageCount = self.getPageSlotCount(self.page + 1)
            self.setSlotCount(pageCount)
            self.refresh()

    def askForShow(self):
        BigWorld.player().base.openFashionBag()

    def show(self):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_FASION_BAG):
            return
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FASHION_BAG)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FASHION_BAG:
            self.mediator = mediator
            BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)

    def onItemChange(self, params):
        if params[0] != const.RES_KIND_FASHION_BAG:
            return
        page = params[1]
        pos = params[2]
        item = BigWorld.player().fashionBag.getQuickVal(page, pos)
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
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FASHION_BAG)
            if BigWorld.player():
                if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                    BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.page = const.FASHION_BAG_PAGE_LOW

    def onGetinitData(self, *arg):
        initObj = self.movie.CreateObject()
        itemArr = self.movie.CreateArray()
        p = BigWorld.player()
        initObj.SetMember('isAutoSortInventory', GfxValue(self.isAutoSortInventory))
        initObj.SetMember('enabledPackSlotCnt', GfxValue(BigWorld.player().fashionBag.enabledPackSlotCnt))
        i = 0
        for ps in xrange(p.fashionBag.enabledPackSlotCnt):
            it = p.fashionBagBar.getQuickVal(0, ps)
            if it == const.CONT_EMPTY_VAL:
                continue
            arr = gameglobal.rds.ui.inventory.initItemArr(it, ps, const.RES_KIND_TEMP_BAG)
            itemArr.SetElement(i, arr)
            i += 1

        initObj.SetMember('itemArr', itemArr)
        return initObj

    def onOpenPicBag(self, *arg):
        gameglobal.rds.ui.dyePanel.show()

    def onSelectedType(self, *arg):
        itemFilter = int(arg[3][0].GetNumber())
        self.itemFilter = itemFilter
        self.updateCurrentPageSlotState()

    def clearDyeState(self):
        if self.isDyeState:
            self.isDyeState = False
            if ui.get_cursor_state() == ui.DYE_STATE:
                ui.reset_cursor()
            self.dyeItemPage = const.CONT_NO_PAGE
            self.dyeItemPos = const.CONT_NO_POS
            self.uiAdapter.roleInfo.updateSlotState()
            self.uiAdapter.dyeColor.hide()

    def clearState(self):
        self.clearDyeState()
        if gameglobal.rds.configData.get('enableFashionBagRenew', False):
            self.updateCurrentPageSlotState()

    def setDyePlaneState(self):
        self.clearState()
        self.isDyePlaneState = True
        p = BigWorld.player()
        if self.mediator:
            posCount = p.fashionBag.posCountDict.get(self.page, 0)
            for pos in xrange(0, posCount):
                if not (self.dyeItemPage == self.page and self.dyeItemPos == pos):
                    self.updateSlotState(self.page, pos)

    def clearDyePlaneState(self):
        if self.isDyePlaneState:
            self.isDyePlaneState = False
            if self.mediator:
                self.updateCurrentPageSlotState()

    def updateCurrentPageSlotState(self):
        if self.page == const.FASHION_BAG_PAGE_BAG:
            return
        if self.mediator:
            posCount = BigWorld.player().fashionBag.posCount
            for pos in xrange(0, posCount):
                self.updateSlotState(self.page, pos)

    @ui.checkEquipChangeOpen()
    def onOpenAutoFetch(self, *arg):
        gameglobal.rds.ui.autoFetchFashion.show()

    def onSetFashionBagItem(self, *arg):
        self.setFashionBagItem(int(arg[3][0].GetNumber()))

    def setFashionBagItem(self, page):
        idx = page
        p = BigWorld.player()
        for ps in xrange(p.fashionBag.posCount):
            self.removeItem(self.page, ps)

        self.setPage(idx)
        pageCount = self.getPageSlotCount(idx + 1)
        self.setSlotCount(pageCount)
        for ps in xrange(p.fashionBag.posCount):
            if gameglobal.rds.ui.inDragStorageItem and gameglobal.rds.ui.dragStoragePageSrc == idx and gameglobal.rds.ui.dragStorageItemSrc == ps:
                continue
            it = p.fashionBag.getQuickVal(idx, ps)
            if it == const.CONT_EMPTY_VAL:
                continue
            self.addItem(it, idx, ps)

    def setSlotCount(self, slotCount):
        if self.mediator:
            self.mediator.Invoke('setSlotCount', GfxValue(slotCount))

    def addItem(self, item, page, pos):
        if self.page != page:
            return
        else:
            if item is not None:
                key = self._getKey(0, pos)
                self.addRealItem(key, item)
                self.updateSlotState(page, pos)
            return

    def addBarItem(self, item, pos):
        if item is not None:
            key = self._getKey(1, pos)
            self.addRealItem(key, item)

    def removeBarItem(self, pos):
        key = self._getKey(1, pos)
        if self.binding.get(key, None) is not None:
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
            self.binding[key][1].InvokeSelf(data)

    def enablePackSlot(self, pos):
        if self.mediator:
            self.mediator.Invoke('enablePackSlot', GfxValue(pos))

    def setFirstTab(self):
        if self.mediator:
            self.mediator.Invoke('setFirstTab')

    def setBagTabAble(self, tabPos, isEnable):
        if self.mediator:
            self.mediator.Invoke('setBagTabAble', (GfxValue(tabPos), GfxValue(isEnable)))

    def removeItem(self, page, pos):
        if self.page != page:
            return
        else:
            key = self._getKey(0, pos)
            if self.binding.get(key, None) is not None:
                data = GfxValue(1)
                data.SetNull()
                self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
                self.binding[key][1].InvokeSelf(data)
            return

    def addRealItem(self, key, item):
        if self.binding.get(key, None) is not None:
            data = uiUtils.getGfxItem(item)
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data, True))

    def updateSlotState(self, page, pos):
        if not self.mediator or self.page != page:
            return
        key = self._getKey(0, pos)
        if not self.binding.has_key(key):
            return
        p = BigWorld.player()
        item = p.fashionBag.getQuickVal(page, pos)
        if item == const.CONT_EMPTY_VAL:
            return
        if not self.isfilter(item):
            state = uiConst.ITEM_GRAY
        elif self.checkItemDisabled(page, pos, item):
            state = uiConst.ITEM_DISABLE
        elif (self.isDyeState or self.isDyePlaneState) and self.uiAdapter.dyePlane.isInDyePlane(page, pos, const.RES_KIND_FASHION_BAG):
            state = uiConst.ITEM_DISABLE
        elif (self.isDyeState or self.isDyePlaneState) and not item.isCanDye():
            state = uiConst.ITEM_GRAY
        elif item.isMallFashionRenewable() and item.isExpireTTL():
            state = uiConst.EQUIP_EXPIRE_TIME_RE
        elif not item.isMallFashionRenewable() and item.isExpireTTL():
            state = uiConst.EQUIP_EXPIRE_TIME
        elif not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
            state = uiConst.EQUIP_NOT_USE
        elif item.type == Item.BASETYPE_EQUIP and (hasattr(item, 'cdura') and item.cdura == 0 or item.canEquip(p, item.whereEquip()[0])):
            state = uiConst.EQUIP_BROKEN
        else:
            state = uiConst.ITEM_NORMAL
        if state == uiConst.ITEM_NORMAL:
            if item.isLatchOfTime():
                state = uiConst.ITEM_LATCH_TIME
            elif hasattr(item, 'latchOfCipher'):
                state = uiConst.ITEM_LATCH_CIPHER
        elif item.isLatchOfTime():
            state = uiConst.ITEM_LATCH_TIME * 1000 + state
        elif hasattr(item, 'latchOfCipher'):
            state = uiConst.ITEM_LATCH_CIPHER * 1000 + state
        self.binding[key][0].Invoke('setSlotState', GfxValue(state))

    def isfilter(self, item):
        if self.itemFilter == uiConst.FASHION_FILTER_ITEM_FASHION:
            if item.type == Item.BASETYPE_EQUIP and item.equipType == Item.EQUIP_BASETYPE_FASHION and item.equipSType in Item.FASHION_BAG_FASHION[1:5]:
                return True
        elif self.itemFilter == uiConst.FASHION_FILTER_ITEM_JEWELRY:
            if item.type == Item.BASETYPE_EQUIP and item.equipType == Item.EQUIP_BASETYPE_FASHION and item.equipSType in Item.FASHION_BAG_JEWELRY[1:5]:
                return True
        elif self.itemFilter == uiConst.FASHION_FILTER_ITEM_PENDANT:
            if item.type == Item.BASETYPE_EQUIP and item.equipType == Item.EQUIP_BASETYPE_FASHION and item.equipSType in Item.FASHION_BAG_PENDANT[1:6]:
                return True
        elif self.itemFilter == uiConst.FASHION_FILTER_ITEM_WEAPON:
            if item.type == Item.BASETYPE_EQUIP and item.equipType == Item.EQUIP_BASETYPE_FASHION_WEAPON:
                return True
        else:
            return True
        return False

    def checkItemDisabled(self, page, pos, item):
        for proxyName in self.checkDisableProxys:
            if hasattr(self.uiAdapter, proxyName):
                proxy = getattr(self.uiAdapter, proxyName)
                if hasattr(proxy, 'isItemDisabled'):
                    isDisable = proxy.isItemDisabled(const.RES_KIND_FASHION_BAG, page, pos, item)
                    if isDisable:
                        return True

        return False

    def setPage(self, page):
        self.page = page

    def onGetToolTip(self, *arg):
        p = BigWorld.player()
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if page == const.STORAGE_PAGE_BAG:
            i = p.fashionBagBar.getQuickVal(0, pos)
        else:
            i = p.fashionBag.getQuickVal(page, pos)
        if i == const.CONT_EMPTY_VAL:
            return
        return gameglobal.rds.ui.inventory.GfxToolTip(i)

    def _getKey(self, page, pos):
        return 'FashionBag%d.slot%d' % (page, pos)

    def getSlotID(self, key):
        idPage, idPos = key.split('.')
        pos = int(idPos[4:])
        page = int(idPage[10:])
        if page == 1:
            return (const.FASHION_BAG_PAGE_BAG, pos)
        return (self.page, pos)

    def refresh(self):
        self.setFashionBagItem(self.page)

    def onUseItem(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        i = BigWorld.player().fashionBag.getQuickVal(page, pos)
        if i == const.CONT_EMPTY_VAL:
            return
        data = {}
        data['item'] = i
        data['page'] = page
        data['pos'] = pos
        e = Event(events.EVENT_FASHION_ITEM_CLICKED, data)
        self.dispatchEvent(e)
        if e.handled:
            return
        if gameglobal.rds.ui.randomDye.widget:
            if Item.isMaterialItem(i.id) and i.id in MDD.data.keys():
                if MDD.data.get(i.id, {}).get('dyeType') == Item.CONSUME_DYE_NORMAL:
                    BigWorld.player().showGameMsg(GMDD.data.RANDOM_DYE_ONLY_FROM_INV, ())
                    return
        if gameglobal.rds.ui.dyePlane.isShow:
            gameglobal.rds.ui.dyePlane.setEquip(page, pos, i, const.RES_KIND_FASHION_BAG)
        elif gameglobal.rds.ui.dyeReset.isShow:
            gameglobal.rds.ui.dyeReset.setEquip(page, pos, i, const.RES_KIND_FASHION_BAG)
        else:
            BigWorld.player().useFashionBagItem(page, pos)

    def onSortItem(self, *arg):
        BigWorld.player().base.sortFashionBag()
        self.setAutoSortAble(False)
        BigWorld.callback(30, Functor(self.setAutoSortAble, True))

    def setAutoSortAble(self, isEnable):
        self.isAutoSortInventory = isEnable
        if self.mediator:
            self.mediator.Invoke('setAutoSortAble', GfxValue(isEnable))
