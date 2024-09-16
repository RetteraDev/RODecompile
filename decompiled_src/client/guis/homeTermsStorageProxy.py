#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/homeTermsStorageProxy.o
import BigWorld
import events
import uiConst
import uiUtils
import const
import gameglobal
from item import Item
from guis import ui
from asObject import ASObject
from uiProxy import SlotDataProxy
from pickledItem import PickledItem
from callbackHelper import Functor
from guis.asObject import TipManager
from gameStrings import gameStrings
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
TOTAL_SLOT = 48

class HomeTermsStorageProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(HomeTermsStorageProxy, self).__init__(uiAdapter)
        self.widget = None
        self.bindType = 'homeTStorage'
        self.type = 'homeTStorage'
        self.pages = []
        self.page = const.STORAGE_PAGE_LOW
        self.stroageVersion = 0
        self.itemsList = []
        self.isAutoSort = True
        for pg in xrange(TOTAL_SLOT):
            self.pages.append([ None for ps in xrange(TOTAL_SLOT) ])

        uiAdapter.registerEscFunc(uiConst.WIDGET_HOME_TERMS_STORAGE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_HOME_TERMS_STORAGE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    @ui.checkInventoryLock()
    def show(self, curPage, itemsList, version):
        self.setPage(curPage)
        self.setStorageVersion(version)
        self.itemsList = itemsList
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_HOME_TERMS_STORAGE)
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()
        p = BigWorld.player()
        p.checkSetPassword()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_HOME_TERMS_STORAGE)

    def reset(self):
        self.page = const.STORAGE_PAGE_LOW
        self.stroageVersion = 0

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.autoSortBtn.addEventListener(events.BUTTON_CLICK, self.handleClickAutoSorty, False, 0, True)
        self.widget.autoSortBtn.enabled = self.isAutoSort
        self.widget.autoSortBtn.mouseEnabled = True
        TipManager.addTip(self.widget.autoSortBtn, gameStrings.HOME_STORAGE_SORT_CD)

    def handleClickAutoSorty(self, *args):
        if not self.isAutoSort:
            return
        p = BigWorld.player()
        p.cell.sortStorageHome()
        self.setAutoSortAble(False)
        BigWorld.callback(SCD.data.get('autoSortInvCD', 30), Functor(self.setAutoSortAble, True))

    def setAutoSortAble(self, isEnable):
        self.isAutoSort = isEnable
        if self.widget:
            self.widget.autoSortBtn.enabled = isEnable
            self.widget.autoSortBtn.mouseEnabled = True

    def refreshInfo(self):
        for i, item in enumerate(self.itemsList):
            self.pages[self.page][i] = item

        self.updateSlotInfo()

    def updateSlotInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            for i in range(TOTAL_SLOT):
                slot = self.widget.itemMc.getChildByName('slot%d' % i)
                if slot and i < len(self.itemsList):
                    slot.visible = True
                    slot.binding = 'homeTStorage0.slot%d' % i
                    slot.addEventListener(events.MOUSE_CLICK, self.handleClickRightItem, False, 0, True)
                    slot.setItemSlotData(None)
                    item = self.itemsList[i]
                    if item:
                        itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_HOME_STORAGE)
                        itemInfo['count'] = item.cwrap
                        if not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                            itemInfo['state'] = uiConst.EQUIP_NOT_USE
                        else:
                            itemInfo['state'] = uiConst.ITEM_NORMAL
                        slot.setItemSlotData(itemInfo)
                else:
                    slot.visible = False

            return

    def getSlotID(self, key):
        _, idPos = key.split('.')
        pos = int(idPos[4:])
        return (self.page, pos)

    def _getKey(self, page, pos):
        return 'homeTStorage%d.slot%d' % (page, pos)

    def getQuickVal(self, page, pos):
        if page == const.CONT_NO_PAGE and pos == const.CONT_NO_POS:
            return None
        elif page < len(self.pages) and pos < len(self.pages[page]):
            it = self.pages[page][pos]
            if it.__class__ is PickledItem:
                it.changeToItem()
            return it
        else:
            return None

    def updateItem(self, item, page, pos):
        if not self.widget:
            return
        else:
            self.pages[page][pos] = item
            self.itemsList[pos] = item
            slot = self.widget.itemMc.getChildByName('slot%d' % pos)
            if item:
                itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_HOME_STORAGE)
                itemInfo['count'] = item.cwrap
                p = BigWorld.player()
                if not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                    itemInfo['state'] = uiConst.EQUIP_NOT_USE
                else:
                    itemInfo['state'] = uiConst.ITEM_NORMAL
            else:
                itemInfo = None
            slot.setItemSlotData(itemInfo)
            return

    def getStorageVersion(self):
        return self.stroageVersion

    def setStorageVersion(self, version):
        self.stroageVersion = version

    def setPage(self, page):
        self.page = page

    def getPage(self):
        return self.page

    @ui.uiEvent(uiConst.WIDGET_HOME_TERMS_STORAGE, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onStorageItemClick(self, event):
        event.stop()
        srcItem = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        p = BigWorld.player()
        cipher = p.cipherOfPerson
        nPageDes, nItemDes = self.searchBestInHomeStorage(srcItem.id, srcItem.cwrap, srcItem)
        if nPageDes != const.CONT_NO_PAGE:
            p.cell.inv2StorageHome(nPage, nItem, srcItem.cwrap, nPageDes, nItemDes, cipher, self.stroageVersion)
        else:
            p.showGameMsg(GMDD.data.STORAGE_FULL, ())

    def searchBestInHomeStorage(self, itemId, amount, src = None):
        if amount > Item.maxWrap(itemId):
            return (const.CONT_NO_PAGE, const.CONT_NO_POS)
        if not src:
            src = Item(itemId, cwrap=amount, genRandProp=False)
        if src.canWrap():
            for ps in range(len(self.itemsList)):
                dst = self.getQuickVal(self.page, ps)
                if dst == const.CONT_EMPTY_VAL:
                    continue
                if dst.id != src.id:
                    continue
                if dst.overBear(amount):
                    continue
                if not src.canMerge(src, dst):
                    continue
                return (self.page, ps)

        for ps in range(len(self.itemsList)):
            srcItem = self.getQuickVal(self.page, ps)
            if not srcItem:
                return (self.page, ps)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def handleClickRightItem(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            slot = e.currentTarget
            nPageSrc, nItemSrc = self.getSlotID(slot.binding)
            srcItem = self.getQuickVal(nPageSrc, nItemSrc)
            if not srcItem:
                return
            p = BigWorld.player()
            nPageDes, nItemDes = p.inv.searchBestInPages(srcItem.id, srcItem.cwrap, srcItem)
            if nPageDes != const.CONT_NO_PAGE:
                p.cell.storageHome2Inv(nPageSrc, nItemSrc, srcItem.cwrap, nPageDes, nItemDes, p.cipherOfPerson, self.stroageVersion)
            else:
                p.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())

    def findItemByUUID(self, uuid):
        if not self.widget:
            return
        for ps in range(len(self.itemsList)):
            obj = self.getQuickVal(self.page, ps)
            if obj == const.CONT_EMPTY_VAL:
                continue
            if obj.uuid != uuid:
                continue
            else:
                return (obj, self.page, ps)

        return (const.CONT_EMPTY_VAL, const.CONT_NO_PAGE, const.CONT_NO_POS)
