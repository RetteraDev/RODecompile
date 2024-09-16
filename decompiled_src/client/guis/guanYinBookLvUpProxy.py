#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/guanYinBookLvUpProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import events
import ui
import const
import gametypes
import random
from uiProxy import SlotDataProxy
from callbackHelper import Functor
from data import guanyin_pskill_pool_data as GPPD
from cdata import guanyin_book_data as GBD
from cdata import game_msg_def_data as GMDD
TAB_LVUP = 0
TAB_MIX = 1
STATUS_NONE = 0
STATUS_MIX_NORML = 20
STATUS_MIX_EFFECT = 21
STATUS_MIX_RESULT = 22

class GuanYinBookLvUpProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(GuanYinBookLvUpProxy, self).__init__(uiAdapter)
        self.bindType = 'guanYinBookLvUp'
        self.type = 'guanYinBookLvUp'
        self.modelMap = {'getLvUpInfo': self.onGetLvUpInfo,
         'getMixInfo': self.onGetMixInfo,
         'removeItem': self.onRemoveItem,
         'lvUp': self.onLvUp,
         'mix': self.onMix,
         'realMix': self.onRealMix,
         'continueMix': self.onContinueMix}
        self.mediator = None
        self.posMap = {}
        self.currentTabIndex = TAB_LVUP
        self.status = STATUS_NONE
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUAN_YIN_BOOK_LVUP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUAN_YIN_BOOK_LVUP:
            self.mediator = mediator
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUAN_YIN_BOOK_LVUP)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def reset(self):
        self.currentTabIndex = TAB_LVUP
        self.status = STATUS_NONE
        self.clearPosMap()

    def clearPosMap(self):
        self.posMap = {}
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUAN_YIN_BOOK_LVUP)
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def refreshInfo(self):
        if self.currentTabIndex == TAB_LVUP:
            self.refreshLvUpInfo()
        elif self.currentTabIndex == TAB_MIX:
            self.refreshMixInfo()

    def onGetLvUpInfo(self, *arg):
        self.currentTabIndex = TAB_LVUP
        self.clearPosMap()
        self.refreshLvUpInfo()

    def refreshLvUpInfo(self):
        if self.mediator:
            self.status = STATUS_NONE
            p = BigWorld.player()
            info = {}
            itemPos = self.posMap.get((0, 0), (const.CONT_NO_PAGE, const.CONT_NO_POS))
            item = p.inv.getQuickVal(itemPos[0], itemPos[1])
            if item:
                info['extraVisible'] = True
                info['itemInfo'] = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                info['itemName'] = uiUtils.getItemColorNameByItem(item)
                gpd = GBD.data.get(item.id, {})
                btnEnabled = True
                bookNeed = gpd.get('bookId', 0)
                info['bookNeed'] = bookNeed
                costItemInfo = uiUtils.getGfxItemById(bookNeed)
                ownNum = p.inv.countItemInPages(bookNeed, enableParentCheck=True)
                if item.getParentId() == uiUtils.getParentId(bookNeed):
                    ownNum -= 1
                needNum = 1
                if ownNum < needNum:
                    costItemInfo['count'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
                    btnEnabled = False
                else:
                    costItemInfo['count'] = '%d/%d' % (ownNum, needNum)
                info['costItemInfo'] = costItemInfo
                itemNeed = gpd.get('lvupItem')
                if itemNeed:
                    itemId, needNum = itemNeed
                    extraItemInfo = uiUtils.getGfxItemById(itemId)
                    ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
                    if ownNum < needNum:
                        extraItemInfo['count'] = "<font color = \'#F43804\'>%d/%d</font>" % (ownNum, needNum)
                        btnEnabled = False
                    else:
                        extraItemInfo['count'] = '%d/%d' % (ownNum, needNum)
                    info['extraItemInfo'] = extraItemInfo
                    info['extraItemVisible'] = True
                else:
                    info['extraItemVisible'] = False
                cashNeed = gpd.get('lvupCash', 0)
                if p.cash < cashNeed:
                    cash = uiUtils.toHtml(format(cashNeed, ','), '#F43804')
                    btnEnabled = False
                else:
                    cash = format(cashNeed, ',')
                info['cash'] = cash
                info['btnEnabled'] = btnEnabled
            else:
                info['extraVisible'] = False
            self.mediator.Invoke('refreshLvUpInfo', uiUtils.dict2GfxDict(info, True))

    def onGetMixInfo(self, *arg):
        self.currentTabIndex = TAB_MIX
        self.clearPosMap()
        self.refreshMixInfo()

    def refreshMixInfo(self):
        if self.mediator:
            self.status = STATUS_MIX_NORML
            p = BigWorld.player()
            info = {}
            info['title'] = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_BOOK_MIX_NORMAL_HINT, '请先放入需要合成的符文')
            itemPos = self.posMap.get((0, 0), (const.CONT_NO_PAGE, const.CONT_NO_POS))
            item = p.inv.getQuickVal(itemPos[0], itemPos[1])
            if item:
                info['extraVisible'] = True
                info['itemInfo'] = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                info['itemName'] = uiUtils.getItemColorNameByItem(item)
                costItemPos = self.posMap.get((0, 1), (const.CONT_NO_PAGE, const.CONT_NO_POS))
                costItem = p.inv.getQuickVal(costItemPos[0], costItemPos[1])
                info['costItemInfo'] = uiUtils.getGfxItem(costItem, location=const.ITEM_IN_BAG) if costItem else None
                info['costItemName'] = uiUtils.getItemColorNameByItem(costItem) if costItem else ''
                info['btnEnabled'] = item != None and costItem != None
            else:
                info['extraVisible'] = False
            self.mediator.Invoke('refreshMixInfo', uiUtils.dict2GfxDict(info, True))

    def onRemoveItem(self, *arg):
        if self.status in (STATUS_MIX_EFFECT, STATUS_MIX_RESULT):
            return
        key = arg[3][0].GetString()
        _, slot = self.getSlotID(key)
        if self.posMap.get((0, slot), (const.CONT_NO_PAGE, const.CONT_NO_POS))[0] == const.CONT_NO_PAGE:
            return
        self.removeItem(slot, True)

    def getSlotID(self, key):
        _, idItem = key.split('.')
        return (0, int(idItem[4:]))

    def _getKey(self, slot):
        return 'guanYinBookLvUp.slot%d' % slot

    def setItem(self, srcBar, srcSlot, destSlot):
        if self.status == STATUS_MIX_EFFECT:
            return
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(srcBar, srcSlot)
        if srcItem.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        if hasattr(srcItem, 'expireTime') or hasattr(srcItem, 'commonExpireTime'):
            p.showGameMsg(GMDD.data.GUAN_YIN_BOOK_MIX_ITEM_EXPIRETIME_ERROR, ())
            return
        if self.currentTabIndex == TAB_MIX and srcItem and destSlot == 0:
            if GBD.data.get(srcItem.id, {}).get('pid') == None:
                p.showGameMsg(GMDD.data.GUAN_YIN_BOOK_MIX_ITEM_ERROR, ())
                return
        self.removeItem(destSlot, False)
        key = self._getKey(destSlot)
        if self.binding.has_key(key):
            self.posMap[0, destSlot] = (srcBar, srcSlot)
            gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
            self.refreshInfo()

    def removeItem(self, slot, needRefresh):
        key = self._getKey(slot)
        if self.binding.has_key(key):
            srcBar, srcSlot = self.posMap.get((0, slot), (const.CONT_NO_PAGE, const.CONT_NO_POS))
            if srcBar != const.CONT_NO_PAGE:
                self.posMap.pop((0, slot))
                gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
                if self.currentTabIndex == TAB_MIX and slot == 0:
                    self.removeItem(1, False)
        if needRefresh:
            self.refreshInfo()

    def findEmptyPos(self):
        if self.currentTabIndex == TAB_LVUP:
            return 0
        if self.currentTabIndex == TAB_MIX:
            for i in xrange(2):
                key = (0, i)
                if not self.posMap.has_key(key):
                    return i

            return 1
        return 0

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if item.isGuanYinNormalSkillBook():
                if (page, pos) in self.posMap.values():
                    return True
                if self.currentTabIndex == TAB_LVUP:
                    return False
                if self.currentTabIndex == TAB_MIX:
                    p = BigWorld.player()
                    itemPos = self.posMap.get((0, 0), (const.CONT_NO_PAGE, const.CONT_NO_POS))
                    resItem = p.inv.getQuickVal(itemPos[0], itemPos[1])
                    if not resItem:
                        return False
                    gbd1 = GBD.data.get(item.id, {})
                    gbd2 = GBD.data.get(resItem.id, {})
                    if gbd1.get('type', 0) == gbd2.get('type', 0) and gbd1.get('lv', 0) == gbd2.get('lv', 0):
                        return False
                return True
            else:
                return True
        else:
            return False

    @ui.uiEvent(uiConst.WIDGET_GUAN_YIN_BOOK_LVUP, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        desPos = self.findEmptyPos()
        self.setInventoryItem(nPage, nItem, desPos)

    def setInventoryItem(self, nPageSrc, nItemSrc, nItemDes):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if srcItem:
            if srcItem.isGuanYinNormalSkillBook():
                self.setItem(nPageSrc, nItemSrc, nItemDes)

    def onLvUp(self, *arg):
        if self.currentTabIndex != TAB_LVUP:
            return
        bookNeed = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        itemPos = self.posMap.get((0, 0), (const.CONT_NO_PAGE, const.CONT_NO_POS))
        item = p.inv.getQuickVal(itemPos[0], itemPos[1])
        if not item:
            return
        isBind = item.isForeverBind()
        ownBindNum = p.inv.countItemInPages(bookNeed, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY, enableParentCheck=True)
        if item.getParentId() == uiUtils.getParentId(bookNeed) and isBind:
            ownBindNum -= 1
        if isBind and ownBindNum <= 0 or not isBind and ownBindNum > 0:
            msg = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_BOOK_LV_UP_USE_UNBIND_HINT, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.realLvUp, itemPos[0], itemPos[1]))
        else:
            self.realLvUp(itemPos[0], itemPos[1])

    def realLvUp(self, page, pos):
        BigWorld.player().cell.guanYinPskillLvUpInInv(page, pos)
        self.hide()

    def onMix(self, *arg):
        if self.currentTabIndex != TAB_MIX:
            return
        p = BigWorld.player()
        itemPos = self.posMap.get((0, 0), (const.CONT_NO_PAGE, const.CONT_NO_POS))
        item = p.inv.getQuickVal(itemPos[0], itemPos[1])
        costItemPos = self.posMap.get((0, 1), (const.CONT_NO_PAGE, const.CONT_NO_POS))
        costItem = p.inv.getQuickVal(costItemPos[0], costItemPos[1])
        if not item or not costItem:
            return
        isBind = item.isForeverBind()
        isCostBind = costItem.isForeverBind()
        if isBind and not isCostBind or not isBind and isCostBind:
            msg = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_BOOK_MIX_USE_UNBIND_HINT, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.showMixEffct, itemPos[0], itemPos[1], costItemPos[0], costItemPos[1]))
        else:
            self.showMixEffct(itemPos[0], itemPos[1], costItemPos[0], costItemPos[1])

    def showMixEffct(self, page1, pos1, page2, pos2):
        if self.currentTabIndex != TAB_MIX:
            return
        if self.mediator:
            self.status = STATUS_MIX_EFFECT
            info = {}
            info['title'] = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_BOOK_MIX_EFFECT_HINT, '合成中')
            item = BigWorld.player().inv.getQuickVal(page1, pos1)
            pid = GBD.data.get(item.id, {}).get('pid')
            if not pid:
                return
            itemList = [ x.get('itemId', 0) for x in GPPD.data.get(pid, []) ]
            if len(itemList) <= 0:
                return
            if len(itemList) < 5:
                itemList = (itemList * 5)[:5]
            else:
                itemList = random.sample(itemList, 5)
            mixList = []
            for itemId in itemList:
                iconPath, color = uiUtils.getItemDataByItemId(itemId)
                mixList.append({'iconPath': iconPath,
                 'color': color})

            info['mixList'] = mixList
            info['page1'] = page1
            info['pos1'] = pos1
            info['page2'] = page2
            info['pos2'] = pos2
            self.mediator.Invoke('showMixEffct', uiUtils.dict2GfxDict(info, True))

    def onRealMix(self, *arg):
        if self.currentTabIndex != TAB_MIX:
            return
        if self.status != STATUS_MIX_EFFECT:
            return
        page1 = int(arg[3][0].GetNumber())
        pos1 = int(arg[3][1].GetNumber())
        page2 = int(arg[3][2].GetNumber())
        pos2 = int(arg[3][3].GetNumber())
        BigWorld.player().cell.guanYinPskillBookMix(page1, pos1, page2, pos2)

    def mixSuccess(self, resultId, page, pos):
        if self.currentTabIndex != TAB_MIX:
            return
        if self.mediator:
            self.status = STATUS_MIX_RESULT
            self.clearPosMap()
            info = {}
            info['title'] = uiUtils.getTextFromGMD(GMDD.data.GUAN_YIN_BOOK_MIX_SUCCESS_HINT, '合成成功')
            item = BigWorld.player().inv.getQuickVal(page, pos)
            if item:
                info['itemInfo'] = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                info['itemName'] = uiUtils.getItemColorName(item.id)
                self.posMap[0, 0] = (page, pos)
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
            else:
                info['itemInfo'] = uiUtils.getGfxItemById(resultId)
                info['itemName'] = uiUtils.getItemColorName(resultId)
            self.mediator.Invoke('mixSuccess', uiUtils.dict2GfxDict(info, True))

    def onContinueMix(self, *arg):
        if self.currentTabIndex != TAB_MIX:
            return
        self.refreshMixInfo()
