#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/crossServerBagProxy.o
import BigWorld
from uiProxy import SlotDataProxy
import gameglobal
import const
import ui
import gametypes
import events
import decorator
from helpers import cellCmd
from guis import uiConst
from guis import cursor
from guis import uiUtils
from guis import uiDrag
from item import Item
from guis.asObject import ASObject
from guis.asObject import ASUtils
from Scaleform import GfxValue
from gamestrings import gameStrings
from callbackHelper import Functor
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
MAX_SLOT_COUNT = 36
MAX_TAB_COUNT = 5

def checkCrossServerBagCanUpdate():

    def func(method, *args):
        if not gameglobal.rds.ui.crossServerBag.isShow():
            return None
        else:
            return method(*args)

    return decorator.decorator(func)


class CrossServerBagProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(CrossServerBagProxy, self).__init__(uiAdapter)
        self.widget = None
        self.binding = {}
        self.bindType = 'crossBag_'
        self.type = 'crossBagSlot'
        self.nPageSrc = None
        self.nItemSrc = None
        self.isSplitState = False
        self.isCanAutoSortCrossInv = True
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CROSS_SERVER_BAG, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CROSS_SERVER_BAG:
            self.widget = widget
            self.reset()
            self.initUI()
            self.refreshAll()

    def reset(self):
        self.allItemData = list()
        self.clearSplitState()

    def show(self):
        if not self.widget:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CROSS_SERVER_BAG)

    @checkCrossServerBagCanUpdate()
    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        for tabIdx in xrange(MAX_TAB_COUNT):
            getattr(self.widget, 'eqBtn%d' % tabIdx).visible = False

        self.initSlotData()
        self.widget.pickAllBtn.addEventListener(events.BUTTON_CLICK, self.handlePickAllClick)
        self.widget.openInventory.addEventListener(events.BUTTON_CLICK, self.handleOpenInventoryClick)
        self.widget.splitBtn.addEventListener(events.BUTTON_CLICK, self.handleSplitItemClick)
        self.widget.sortBtn.addEventListener(events.BUTTON_CLICK, self.handleSortItemClick)
        self.updateSortBtnState()

    def initSlotData(self):
        for slotIdx in xrange(MAX_SLOT_COUNT):
            getattr(self.widget.bag, 'newIcon%d' % slotIdx).visible = False
            slotMc = getattr(self.widget.bag, 'slot%d' % slotIdx)
            slotMc.binding = 'crossBag_0.slot%d' % slotIdx
            slotMc.addEventListener(events.MOUSE_CLICK, self.handleSlotClick, False, 0, True)

    def handleSlotClick(self, *args):
        p = BigWorld.player()
        e = ASObject(args[3][0])
        slotMc = e.currentTarget
        buttonIdx = e.buttonIdx
        if not slotMc:
            return
        nPage, nItem = self.getSlotID(slotMc.binding)
        if buttonIdx == uiConst.LEFT_BUTTON:
            self.checkCanSplitItem(nPage, nItem)
        elif buttonIdx == uiConst.RIGHT_BUTTON:
            if self.isSplitState:
                self.clearSplitState()
                return
            self.realUseCrossItem(nPage, nItem)

    def handleOpenInventoryClick(self, *args):
        self.clearSplitState()
        if not gameglobal.rds.ui.inventory.isShow():
            gameglobal.rds.ui.inventory.show()
        else:
            gameglobal.rds.ui.inventory.hide()

    @ui.checkEquipChangeOpen()
    def handleSplitItemClick(self, *args):
        if self.isSplitState:
            self.clearSplitState()
        else:
            self.setSplitState()

    def clearSplitState(self):
        if self.isSplitState:
            self.isSplitState = False
            if ui.get_cursor_state() == ui.SPLIT_STATE:
                ui.reset_cursor()

    def setSplitState(self):
        self.uiAdapter.clearState()
        self.isSplitState = True
        if ui.get_cursor_state() != ui.SPLIT_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.SPLIT_STATE)
            ui.set_cursor(cursor.splitItem)
            ui.lock_cursor()

    def checkCanSplitItem(self, nPageSrc, nItemSrc):
        if self.isSplitState:
            p = BigWorld.player()
            nPageDes, nItemDes = p.crossInv.searchEmptyInPages()
            if nItemDes == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.BAG_FULL, ())
                return
            sItem = p.crossInv.getQuickVal(nPageSrc, nItemSrc)
            if not sItem:
                return
            if not sItem.isWrap():
                p.showGameMsg(GMDD.data.ITEM_SPLIT_FORBIDDEN_LESS, ())
                return
            if sItem.hasLatch():
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
            if gameglobal.rds.ui.trade.isShow:
                p.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
                return
            if p.curEquippingInPUBGCB:
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
            gameglobal.rds.ui.messageBox.showYesNoInput(msg=gameStrings.CROSS_SERVER_BAG_SPLIT_HINT_TXT, textAlign='center', yesCallback=Functor(self.realRequestSplitItem, nPageSrc, nItemSrc), inputMax=sItem.mwrap, style=uiConst.MSG_BOX_INPUT_INT, defaultInput=1)
            self.clearSplitState()

    def realRequestSplitItem(self, nPageSrc, nItemSrc, inputStr):
        p = BigWorld.player()
        i = p.crossInv.getQuickVal(nPageSrc, nItemSrc)
        if not i:
            return
        nPageDes, nItemDes = p.crossInv.searchEmptyInPages()
        if nItemDes == const.CONT_NO_POS:
            p.showGameMsg(GMDD.data.BAG_FULL, ())
            return
        judge = (1, i.mwrap, GMDD.data.ITEM_TRADE_NUM)
        curInputNum = int(inputStr)
        if not ui.inputRangeJudge(judge, curInputNum, (i.mwrap,)):
            return
        cellCmd.exchangeCrossInv(nPageSrc, nItemSrc, curInputNum, nPageDes, nItemDes)

    @ui.checkEquipChangeOpen()
    def handleSortItemClick(self, *args):
        p = BigWorld.player()
        self.clearSplitState()
        if not self.checkCanAutoSortCrossInv():
            return
        p.cell.autoSortCrossInv()
        self.resetAutoSortCrossInv(False)
        BigWorld.callback(SCD.data.get('autoSortInvCD', 30), Functor(self.resetAutoSortCrossInv, True))

    def checkCanAutoSortCrossInv(self):
        p = BigWorld.player()
        if not self.isCanAutoSortCrossInv:
            p.showGameMsg(GMDD.data.ITEM_TRADE_FORBIDDEN_SORT, ())
            return False
        for widgetId in gameglobal.rds.ui.inventory.checkForbiddenSortProxys:
            isWidgetLoaded = gameglobal.rds.ui.isWidgetLoaded(widgetId)
            if isWidgetLoaded:
                p.showGameMsg(GMDD.data.ITEM_TRADE_FORBIDDEN_SORT, ())
                return False

        state_arr = [ui.SIGNEQUIP_STATE,
         ui.RENEWAL_STATE,
         ui.IDENTIFY_ITEM_STATE,
         ui.IDENTIFY_MANUAL_EQUIP_STATE,
         ui.CHANGE_BIND_STATE,
         ui.RENEWAL_STATE2,
         ui.RESET_FASHION_PROP]
        if ui.get_cursor_state() in state_arr:
            p.showGameMsg(GMDD.data.ITEM_TRADE_FORBIDDEN_SORT, ())
            return False
        if p.curEquippingInPUBGCB:
            p.showGameMsg(GMDD.data.ITEM_TRADE_FORBIDDEN_SORT, ())
            return False
        return True

    def resetAutoSortCrossInv(self, enabled):
        self.isCanAutoSortCrossInv = enabled
        self.updateSortBtnState()

    @checkCrossServerBagCanUpdate()
    def updateSortBtnState(self):
        if self.isCanAutoSortCrossInv:
            self.widget.sortBtn.enabled = True
        else:
            self.widget.sortBtn.enabled = False

    @ui.checkEquipChangeOpen()
    def handlePickAllClick(self, *args):
        self.clearSplitState()
        self.realPickAll()

    def realPickAll(self):
        BigWorld.player().cell.takeAllCrossInvItems()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CROSS_SERVER_BAG)

    def _getKey(self, bar, slot):
        return 'crossBag_%d.slot%d' % (bar, slot)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[9:]), int(idItem[4:]))

    @property
    def isSoul(self):
        return BigWorld.player()._isSoul()

    @checkCrossServerBagCanUpdate()
    def refreshAll(self):
        self.refreshData()
        self.refreshUI()

    def refreshData(self):
        pass

    @checkCrossServerBagCanUpdate()
    def refreshUI(self):
        self.refreshAllBtn()
        self.refreshAllSlot()

    @checkCrossServerBagCanUpdate()
    def refreshAllBtn(self):
        self.widget.openInventory.visible, self.widget.openInventory.enabled = self._getUIVisibleData('openInventory')
        self.widget.pickAllBtn.visible, self.widget.pickAllBtn.enabled = self._getUIVisibleData('pickAllBtn')

    @checkCrossServerBagCanUpdate()
    def refreshAllSlot(self):
        allItemData = self._getCrossBagItems()
        for itemData in allItemData:
            slotIdx = itemData['slotId']
            if slotIdx >= MAX_SLOT_COUNT:
                continue
            self.refreshOneSlot(itemData, 0, slotIdx)

    @checkCrossServerBagCanUpdate()
    def refreshOneSlot(self, itemData, page, pos):
        slotMc = getattr(self.widget.bag, 'slot%d' % pos)
        if slotMc:
            slotMc.setItemSlotData(itemData)

    def _getUIVisibleData(self, uiName):
        p = BigWorld.player()
        if uiName == 'pickAllBtn':
            if p.isInPUBG():
                return (False, False)
            return (not self.isSoul, not self.isSoul)
        if uiName == 'openInventory':
            if p.isInPUBG():
                return (False, False)
            return (not self.isSoul, not self.isSoul)
        return (False, False)

    def _getCrossBagItems(self):
        ret = []
        p = BigWorld.player()
        crossBag = p.crossInv
        i = 0
        for ps in xrange(crossBag.posCount):
            it = crossBag.getQuickVal(0, ps)
            if it == const.CONT_EMPTY_VAL:
                continue
            state = self._getSlotState(0, ps)
            obj = uiUtils.getGfxItem(it, appendInfo={'slotId': ps,
             'state': state})
            self._checkCoolDown(it, 0, ps)
            ret.append(obj)
            i += 1

        return ret

    def _getSlotState(self, page, pos):
        p = BigWorld.player()
        item = p.crossInv.getQuickVal(page, pos)
        if item == const.CONT_EMPTY_VAL:
            return
        key = self._getKey(0, pos)
        if not self.binding.has_key(key):
            return
        elif item.isExpireTTL():
            return uiConst.EQUIP_EXPIRE_TIME_RE
        elif not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
            return uiConst.EQUIP_NOT_USE
        elif item.isLatchOfTime():
            return uiConst.ITEM_LATCH_TIME
        elif hasattr(item, 'latchOfCipher'):
            return uiConst.ITEM_LATCH_CIPHER
        elif item.type == Item.BASETYPE_EQUIP and (hasattr(item, 'cdura') and item.cdura == 0 or item.canEquip(p, item.whereEquip()[0])):
            return uiConst.EQUIP_BROKEN
        else:
            return uiConst.ITEM_NORMAL

    def addItem(self, item, page, pos):
        if item == const.CONT_EMPTY_VAL:
            return
        state = self._getSlotState(0, pos)
        obj = uiUtils.getGfxItem(item, appendInfo={'slotId': pos,
         'state': state})
        self.refreshOneSlot(obj, page, pos)
        self._checkCoolDown(item, page, pos)

    def removeItem(self, page, pos):
        self.refreshOneSlot(None, page, pos)
        gameglobal.rds.ui.actionbar.stopCoolDown(page, pos, False, isCross=True)

    def updateItem(self, item, page, pos):
        if item == const.CONT_EMPTY_VAL:
            return
        state = self._getSlotState(0, pos)
        obj = uiUtils.getGfxItem(item, appendInfo={'slotId': pos,
         'state': state})
        self.refreshOneSlot(obj, page, pos)

    def realUseCrossItem(self, nPage, nItem):
        p = BigWorld.player()
        if not p._isSoul() and not gameglobal.rds.configData.get('enableUseCrossInv', False):
            return
        if gameglobal.rds.ui.inventory.isShow() and self.isShow():
            nPageDes, nItemDes = p.inv.searchEmptyInPages()
            if nItemDes == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.BAG_FULL, ())
                return
            uiDrag._endCrossBagSlotToBagslot(nPage, nItem, nPageDes, nItemDes)
            return
        p.useBagItem(nPage, nItem, fromBag=const.RES_KIND_CROSS_INV)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        i = BigWorld.player().crossInv.getQuickVal(0, pos)
        if i == None:
            return
        else:
            return gameglobal.rds.ui.inventory.GfxToolTip(i)

    def confirmDiscard(self, *arg):
        p = BigWorld.player()
        if self.nPageSrc == uiConst.BAG_PAGE_QUEST:
            item = p.questBag.getQuickVal(0, self.nItemSrc)
            if item != const.CONT_EMPTY_VAL:
                p.showGameMsg(GMDD.data.ITEM_CANNOT_DROP, (item.name,))
        else:
            item = p.realInv.getQuickVal(self.nPageSrc, self.nItemSrc)
            if item != const.CONT_EMPTY_VAL:
                num = item.cwrap
                judge = (1, item.mwrap, GMDD.data.ITEM_TRADE_NUM)
                if ID.data.get(item.id, {}) and not ui.inputRangeJudge(judge, num, (item.mwrap,)):
                    return
                BigWorld.player().cell.discardItem(self.nPageSrc, self.nItemSrc, num)
                gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def cancelDiscard(self, *arg):
        if self.nPageSrc == uiConst.BAG_PAGE_QUEST:
            item = BigWorld.player().questBag.getQuickVal(0, self.nItemSrc)
        else:
            item = BigWorld.player().realInv.getQuickVal(self.nPageSrc, self.nItemSrc)
        if item != const.CONT_EMPTY_VAL:
            gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def _checkCoolDown(self, item, page, pos):
        if item.type == Item.BASETYPE_CONSUMABLE:
            gameglobal.rds.ui.actionbar.playCooldown(page, pos, item.id, False, isCrossBag=True)

    def isShow(self):
        if self.widget:
            return True
        return False
