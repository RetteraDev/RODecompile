#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spriteMaterialBagProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
import const
from uiProxy import SlotDataProxy
from Scaleform import GfxValue
from guis import uiUtils
from guis import ui
from guis.asObject import ASObject
from guis.asObject import ASUtils
from helpers import cellCmd
from cdata import game_msg_def_data as GMDD
MAX_BAG_SLOTS = 36
TAB_COUNT = 5
MAX_EXPAND_SLOTS = 6
curPage = 0
expandSlotNum = 0

class SpriteMaterialBagProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(SpriteMaterialBagProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.page = uiConst.METERIAL_PAGE_LOW
        self.bindType = 'spriteMaterial'
        self.type = 'spriteMaterial'
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPRITE_MATERIAL, self.hide)

    def reset(self):
        self.itemData = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SPRITE_MATERIAL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return

    def clearWidget(self):
        for i in range(0, MAX_BAG_SLOTS):
            slot = getattr(self.widget.meterialBag, 'slot%s' % i)
            if slot:
                slot.removeEventListener(events.MOUSE_CLICK, self.handleItemMouseClick)

        for i in range(0, MAX_EXPAND_SLOTS):
            bagSlot = getattr(self.widget, 'bagslot%s' % i)
            if bagSlot:
                bagSlot.removeEventListener(events.MOUSE_CLICK, self.handleBagBarMouseClick)

        for i in range(0, TAB_COUNT):
            tab = getattr(self.widget, 'tab%s' % i)
            if tab:
                tab.removeEventListener(events.MOUSE_CLICK, self.onTabClick)

        self.widget.autoFetch.removeEventListener(events.MOUSE_CLICK, self.onGetSpriteMeterialItemFromBag)
        self.widget.sortBtn.removeEventListener(events.MOUSE_CLICK, self.onArrangeClick)
        self.widget = None
        self.page = uiConst.METERIAL_PAGE_LOW
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SPRITE_MATERIAL)
        gameglobal.rds.ui.funcNpc.close()

    @ui.checkInventoryLock()
    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SPRITE_MATERIAL)

    def initUI(self):
        if not self.widget:
            return
        self.widget.defaultCloseBtn = self.widget.closeBtn
        for i in range(0, MAX_BAG_SLOTS):
            newIcon = getattr(self.widget.meterialBag, 'newIcon%s' % i)
            slot = getattr(self.widget.meterialBag, 'slot%s' % i)
            if newIcon:
                newIcon.visible = False
            if slot:
                slot.binding = 'spriteMaterial0.slot%s' % i
                slot.addEventListener(events.MOUSE_CLICK, self.handleItemMouseClick, False, 0, True)

        for i in range(0, MAX_EXPAND_SLOTS):
            bagSlot = getattr(self.widget, 'bagslot%s' % i)
            shineSlot = getattr(self.widget, 'shineSlot%s' % i)
            if bagSlot:
                bagSlot.binding = 'spriteMaterial1.slot%s' % i
                bagSlot.idx = i
                bagSlot.bg.lock.visible = True
                bagSlot.isLocked = True
                bagSlot.addEventListener(events.MOUSE_CLICK, self.handleBagBarMouseClick, False, 0, True)
            if shineSlot:
                shineSlot.visible = False

        for i in range(0, TAB_COUNT):
            tab = getattr(self.widget, 'tab%s' % i)
            if tab:
                tab.data = i
                tab.addEventListener(events.MOUSE_CLICK, self.onTabClick, False, 0, True)
                tab.addEventListener(events.MOUSE_OVER, self.onTabRollOver, False, 0, True)

        self.widget.autoFetch.addEventListener(events.MOUSE_CLICK, self.onGetSpriteMeterialItemFromBag, False, 0, True)
        self.widget.sortBtn.addEventListener(events.MOUSE_CLICK, self.onArrangeClick, False, 0, True)
        self.widget.tab0.selected = True
        self.widget.activeBtn.visible = False
        self.refreshAll()

    def _getKey(self, page, pos):
        return 'spriteMeterial%d.slot%d' % (page, pos)

    def handleItemMouseClick(self, *args):
        e = ASObject(args[3][0])
        slot = e.currentTarget
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            nPage, nPos = self.getSlotID(slot.binding)
            p = BigWorld.player()
            item = p.spriteMaterialBag.getQuickVal(nPage, nPos)
            if item:
                emptyPg, emptyPos = p.inv.searchBestInPages(item.id, item.cwrap, item)
                if emptyPg == const.CONT_NO_PAGE or emptyPos == const.CONT_NO_POS:
                    p.showGameMsg(GMDD.data.BAG_FULL, ())
                    return
                self.dragSpriteMaterialBagToBagSlot(nPage, nPos, emptyPg, emptyPos)

    @ui.uiEvent(uiConst.WIDGET_SPRITE_MATERIAL, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        if not self.widget:
            return
        else:
            event.stop()
            i = event.data['item']
            nPage = event.data['page']
            nPos = event.data['pos']
            if i == None:
                return
            p = BigWorld.player()
            emptyPg, emptyPos = self.searchBestInPages(i.id, i.cwrap, i)
            if emptyPg == const.CONT_NO_PAGE or emptyPos == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.SPRITE_MATERIAL_BAG_FULL, ())
                return
            self.dragBagSlotToSpriteMaterialBag(nPage, nPos, emptyPg, emptyPos)
            return

    def searchBestInPages(self, itemId, amount, src = None):
        from item import Item
        p = BigWorld.player()
        if amount > Item.maxWrap(itemId):
            return (const.CONT_NO_PAGE, const.CONT_NO_POS)
        if not src:
            src = Item(itemId, cwrap=amount, genRandProp=False)
        pages = p.spriteMaterialBag.posCountDict.keys()
        if src.canWrap():
            for pg in pages:
                posCount = p.spriteMaterialBag.posCountDict[pg]
                for ps in xrange(posCount):
                    dst = p.spriteMaterialBag.getQuickVal(pg, ps)
                    if dst == const.CONT_EMPTY_VAL:
                        continue
                    if dst.id != src.id:
                        continue
                    if dst.overBear(amount):
                        continue
                    if not src.canMerge(src, dst):
                        continue
                    return (pg, ps)

        for pg in pages:
            for ps in xrange(p.spriteMaterialBag.posCountDict[pg]):
                if not p.spriteMaterialBag.getQuickVal(pg, ps) and ps != const.CONT_NO_POS:
                    return (pg, ps)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def getSlotID(self, key):
        idPage, idPos = key.split('.')
        pos = int(idPos[4:])
        page = int(idPage[14:])
        if page == 1:
            return (const.METERIAL_BAG_PAGE_BAG, pos)
        return (self.page, pos)

    def handleBagBarMouseClick(self, *args):
        e = ASObject(args[3][0])
        bagSlot = e.currentTarget
        if bagSlot.isLocked and self.expandSlotNum == bagSlot.idx:
            self.enlargeSlot(self.expandSlotNum)
        elif e.buttonIdx == uiConst.RIGHT_BUTTON:
            self.clickExpandSlot(bagSlot.binding)

    def enlargeSlot(self, index):
        gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_SPRITE_MATERIAL_BAG_EXPAND, index)

    def clickExpandSlot(self, *arg):
        pass

    def onTabClick(self, *args):
        e = ASObject(args[3][0])
        curPage = e.currentTarget.data
        self.setPage(curPage)
        for i in range(0, TAB_COUNT):
            tab = getattr(self.widget, 'tab%s' % i)
            if tab:
                tab.selected = False

        e.currentTarget.selected = True

    def onTabRollOver(self, *args):
        if gameglobal.rds.ui.inDragStorageItem or gameglobal.rds.ui.inDragCommonItem or gameglobal.rds.ui.inDragSpriteMaterialBagItem:
            self.onTabClick(*args)

    def setPage(self, curPage):
        self.page = int(curPage)
        self.updateSlots()

    def onGetSpriteMeterialItemFromBag(self, *args):
        p = BigWorld.player()
        p.base.allInv2SpriteMaterialBag()

    def onArrangeClick(self, *args):
        p = BigWorld.player()
        p.base.sortSpriteMaterialBag()

    def refreshAll(self, *args):
        if not self.widget:
            return
        self.updateSlots()
        self.updateTabs()
        self.enablePackSlot()

    def refreshAllWithPackSlot(self):
        if not self.widget:
            return
        self.updateSlotsVisible()
        self.updateTabs()
        self.enablePackSlot()

    def updateSlotsVisible(self):
        p = BigWorld.player()
        cnt = len(p.spriteMaterialBag.posCountDict.keys()) if hasattr(p.spriteMaterialBag, 'posCountDict') else 1
        onlyVisible = False
        if self.page >= cnt:
            self.page = uiConst.METERIAL_PAGE_LOW
            for i in range(0, TAB_COUNT):
                tab = getattr(self.widget, 'tab%s' % i)
                if tab:
                    tab.selected = False

            getattr(self.widget, 'tab%s' % self.page).selected = True
        else:
            onlyVisible = True
        slotItems = self._getItems()
        for i in range(0, MAX_BAG_SLOTS):
            self.updateOneSlot(i, slotItems, onlyVisible)

    def updateSlots(self):
        slotItems = self._getItems()
        for i in range(0, MAX_BAG_SLOTS):
            self.updateOneSlot(i, slotItems)

    def updateOneSlot(self, pos, slotItems = None, onlyVisible = False):
        if not self.widget:
            return
        slot = getattr(self.widget.meterialBag, 'slot%s' % pos)
        slotItems = slotItems or self._getItems()
        if slot:
            slot.visible = pos < len(list(slotItems))
            if slot.visible and not onlyVisible:
                slot.bg.gotoAndPlay('normal')
                slot.setItemSlotData(slotItems[pos])

    def updateTabs(self):
        p = BigWorld.player()
        cnt = len(p.spriteMaterialBag.posCountDict.keys()) if hasattr(p.spriteMaterialBag, 'posCountDict') else 1
        for i in range(0, TAB_COUNT):
            tab = getattr(self.widget, 'tab%s' % i)
            if tab:
                tab.visible = i < cnt

    def enablePackSlot(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.expandSlotNum = getattr(p.spriteMaterialBag, 'enabledPackSlotCnt', 0)
        for i in range(0, MAX_EXPAND_SLOTS):
            bagSlot = getattr(self.widget, 'bagslot%s' % i)
            shineSlot = getattr(self.widget, 'shineSlot%s' % i)
            if bagSlot:
                bagSlot.bg.lock.visible = i >= self.expandSlotNum
                bagSlot.isLocked = i >= self.expandSlotNum
            if shineSlot:
                shineSlot.visible = i == self.expandSlotNum
            if i < self.expandSlotNum:
                bagSlot.bg.gotoAndPlay('bag%s' % (i + 1))

        barItems = self._getBarItems()
        for i in range(0, MAX_EXPAND_SLOTS):
            bagSlot = getattr(self.widget, 'bagslot%s' % i)
            if bagSlot:
                bagSlot.visible = i < len(barItems)
            if bagSlot.visible:
                bagSlot.setItemSlotData(barItems[i])

    def _getItems(self):
        items = []
        p = BigWorld.player()
        pageCnt = getattr(p.spriteMaterialBag, 'posCountDict', {}).get(self.page, 0)
        for ps in xrange(pageCnt):
            it = p.spriteMaterialBag.getQuickVal(self.page, ps)
            if it == const.CONT_EMPTY_VAL:
                items.append(None)
            else:
                state = uiConst.ITEM_NORMAL
                if hasattr(it, 'latchOfTime'):
                    state = uiConst.ITEM_LATCH_TIME
                elif hasattr(it, 'latchOfCipher'):
                    state = uiConst.ITEM_LATCH_CIPHER
                itemInfo = uiUtils.getGfxItemById(it.id, it.cwrap, appendInfo={'state': state})
                itemInfo['srcType'] = '%s/%s/%s' % ('spriteMaterialBag', self.page, ps)
                items.append(itemInfo)

        return items

    def _getBarItems(self):
        items = []
        p = BigWorld.player()
        for ps in xrange(const.MATERIAL_BAG_BAR_HEIGHT):
            it = p.spriteMaterialBagBar.getQuickVal(0, ps)
            if it == const.CONT_EMPTY_VAL:
                items.append(None)
            else:
                items.append(uiUtils.getGfxItem(it))

        return items

    def dragBagSlotToSpriteMaterialBag(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        sItem = BigWorld.player().inv.getQuickVal(nPageSrc, nItemSrc)
        if nPageDes == -1:
            p.base.toInv2SpriteMaterialBagSlot(nPageSrc, nItemSrc, nItemDes)
        else:
            p.base.inv2spriteMaterialBag(nPageSrc, nItemSrc, sItem.cwrap, nPageDes, nItemDes)

    def dragSpriteMaterialBagToSpriteMaterialBag(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        sItem = BigWorld.player().spriteMaterialBag.getQuickVal(nPageSrc, nItemSrc)
        if nPageSrc == -1 and nPageDes == -1:
            p.base.spriteMaterialBagSlot2spriteMaterialBagSlot(nItemSrc, nItemDes)
        else:
            if nPageSrc == -1 or nPageDes == -1:
                return
            if sItem:
                p.base.spriteMaterialBag2spriteMaterialBag(nPageSrc, nItemSrc, sItem.cwrap, nPageDes, nItemDes)

    def dragSpriteMaterialBagToBagSlot(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        if nPageSrc == -1:
            sItem = BigWorld.player().spriteMaterialBagBar.getQuickVal(0, nItemSrc)
            if sItem:
                p.cell.toSpriteMaterialBagSlot2Inv(nItemSrc, sItem.id, nPageDes, nItemDes)
        else:
            sItem = BigWorld.player().spriteMaterialBag.getQuickVal(nPageSrc, nItemSrc)
            if sItem:
                p.cell.spriteMaterialBag2inv(nPageSrc, nItemSrc, sItem.cwrap, nPageDes, nItemDes)

    def removeItem(self, page, pos):
        self.updateOneSlot(pos)

    def addItem(self, item, page, pos):
        self.updateOneSlot(pos)

    def addBarItem(self, item, pos):
        self.enablePackSlot()

    def removeBarItem(self, pos):
        self.enablePackSlot()

    def onGetToolTip(self, *arg):
        p = BigWorld.player()
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if page == const.METERIAL_BAG_PAGE_BAG:
            it = p.spriteMaterialBagBar.getQuickVal(0, pos)
            if it:
                return gameglobal.rds.ui.inventory.GfxToolTip(it)
