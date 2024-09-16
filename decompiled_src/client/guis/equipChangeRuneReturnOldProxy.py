#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeRuneReturnOldProxy.o
import BigWorld
import math
import gameglobal
import uiConst
import events
import gamelog
import const
import item
from callbackHelper import Functor
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from guis import tipUtils
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import new_rune_consume_data as NRCD
from data import rune_prop_pskill_map_data as RPSMD
from data import game_msg_data as GMD
from cdata import hierogram_crystal_to_old_data as HCTOD
from cdata import game_msg_def_data as GMDD

class EquipChangeRuneReturnOldProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeRuneReturnOldProxy, self).__init__(uiAdapter)
        self.widget = None
        self.modelMap = {'initPanel': self.onInitPanel,
         'unRegisterPanel': self.onUnRegisterPanel}
        self.reset()

    def reset(self):
        self.selectedBag = uiConst.BAG_INV
        self.selectedMc = None
        self.selectedPos = None
        self.autoSelected = True
        self.rightData = {}
        self.isItemCntEnough = False
        self.isCashCntEnough = False

    def onInitPanel(self, *args):
        self.widget = ASObject(args[3][0])
        self.initUI()
        self.refreshInfo()

    def onUnRegisterPanel(self, *args):
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.scrollWndList.itemRenderer = 'EquipChangeBG_LeftItem'
        self.widget.scrollWndList.itemHeight = 64
        self.widget.scrollWndList.labelFunction = self.labelFunction
        self.widget.equipBtn.groupName = 'runeFeed'
        self.widget.invBagBtn.groupName = 'runeFeed'
        self.widget.runeBagBtn.groupName = 'runeFeed'
        self.widget.equipBtn.tabIdx = uiConst.BAG_EQUIP_RUNE
        self.widget.equipBtn.visible = False
        self.widget.invBagBtn.tabIdx = uiConst.BAG_INV
        self.widget.runeBagBtn.tabIdx = uiConst.RUNE_INV_BAG
        self.widget.equipBtn.addEventListener(events.BUTTON_CLICK, self.handleBagChangeClick, False, 0, True)
        self.widget.invBagBtn.addEventListener(events.BUTTON_CLICK, self.handleBagChangeClick, False, 0, True)
        self.widget.runeBagBtn.addEventListener(events.BUTTON_CLICK, self.handleBagChangeClick, False, 0, True)
        self.widget.right.slot2.slot.dragable = False
        selectedMc = self.widget.right.selected.getChildByName('selected0')
        selectedMc.idx = 0
        selectedMc.selected = True
        self.widget.right.exchangeBtn.addEventListener(events.BUTTON_CLICK, self.handleExchangeBtnClick, False, 0, True)
        self.widget.noItemHint.getChildAt(0).text = gameStrings.EQUIP_CHANGE_RUNE_NO_ITEM_DESC.get('return', '')
        ASUtils.setHitTestDisable(self.widget.right.needCash.cash, True)

    def handleExchangeBtnClick(self, *args):
        p = BigWorld.player()
        item = self.uiAdapter.equipChangeRuneFeed.getItemByPos(*self.selectedPos)
        oldItemId = self.getReturnOldId(item.id)
        text = GMD.data.get(GMDD.data.EQUIP_CHANGE_RUNE_RETURN, {}).get('text', '%s,%s') % (p.getRuneData(item.id, 'name', ''), p.getRuneData(oldItemId, 'name', ''))
        self.uiAdapter.messageBox.showYesNoMsgBox(text, self.confirmCallback)

    def confirmCallback(self):
        p = BigWorld.player()
        resKind = const.RES_KIND_HIEROGRAM_BAG if self.selectedBag == uiConst.RUNE_INV_BAG else const.RES_KIND_INV
        gamelog.info('jbx:transferBackOldHierogram', resKind, self.selectedPos[1], self.selectedPos[2])
        p.base.transferBackOldHierogram(resKind, self.selectedPos[1], self.selectedPos[2])

    def onTransferBackOldHierogram(self, newItem):
        self.selectedMc = None
        self.selectedPos = None
        self.autoSelected = True
        self.refreshInfo()

    def handleBagChangeClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.tabIdx == self.selectedBag:
            return
        else:
            self.selectedBag = int(e.currentTarget.tabIdx)
            self.autoSelected = True
            self.selectedPos = None
            self.refreshInfo()
            return

    def getItemByPos(self, tab, page, pos):
        p = BigWorld.player()
        if tab == uiConst.BAG_EQUIP_RUNE:
            return p.hierogramDict.get('hieroCrystals', {}).get((page, pos), None)
        elif tab == uiConst.BAG_INV:
            return BigWorld.player().inv.getQuickVal(page, pos)
        else:
            return BigWorld.player().hierogramBag.getQuickVal(page, pos)

    def getExchangeMinLv(self):
        keys = NRCD.data.keys()
        keys.sort()
        return keys[0]

    def getRuneList(self):
        p = BigWorld.player()
        itemList = []
        if self.selectedBag == uiConst.BAG_INV:
            for pageIdx, page in enumerate(p.inv.pages):
                for pos, item in enumerate(page):
                    if item and item.isNewHieroCrystal():
                        itemList.append(self.uiAdapter.equipChangeRuneFeed.getGfxItemData(item, self.selectedBag, pageIdx, pos))

        else:
            for pageIdx, page in enumerate(p.hierogramBag.pages):
                for pos, item in enumerate(page):
                    if item and item.isNewHieroCrystal():
                        itemList.append(self.uiAdapter.equipChangeRuneFeed.getGfxItemData(item, self.selectedBag, pageIdx, pos))

        return itemList

    def labelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.data = itemData
        itemMc.pos = itemData.pos
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)
        if self.selectedPos and self.selectedPos[0] == itemData.pos[0] and self.selectedPos[1] == itemData.pos[1] and self.selectedPos[2] == itemData.pos[2]:
            if self.selectedMc:
                self.selectedMc.selected = False
            self.selectedMc = itemMc
            self.selectedMc.selected = True
        else:
            itemMc.selected = False

    def handleItemClick(self, *args):
        if not self.widget or not self.widget.stage:
            return
        e = ASObject(args[3][0])
        pos = (e.currentTarget.pos[0], e.currentTarget.pos[1], e.currentTarget.pos[2])
        if pos == self.selectedPos:
            return
        if self.selectedMc:
            self.selectedMc.selected = False
        self.rightIndex = 0
        e.currentTarget.selected = True
        self.selectedMc = e.currentTarget
        self.selectedPos = pos
        self.refreshRight()

    def refreshLeftItemList(self):
        itemList = self.getRuneList()
        if not self.selectedPos and self.autoSelected and itemList:
            self.autoSelected = False
            self.selectedPos = itemList[0]['pos']
        self.widget.scrollWndList.dataArray = itemList
        self.widget.noItemHint.visible = not bool(itemList)
        self.widget.equipBtn.selected = self.selectedBag == uiConst.BAG_EQUIP_RUNE
        self.widget.runeBagBtn.selected = self.selectedBag == uiConst.RUNE_INV_BAG
        self.widget.invBagBtn.selected = self.selectedBag == uiConst.BAG_INV

    def refreshRightNoItem(self):
        if not self.widget:
            return
        else:
            ASUtils.setHitTestDisable(self.widget.right, True)
            ASUtils.setMcEffect(self.widget.right, 'gray')
            self.widget.right.slot2.slot.setItemSlotData(None)
            selectedMc = self.widget.right.selected.getChildByName('selected0')
            selectedMc.label = ' '
            self.widget.right.needCash.cash.text = '--'
            return

    def getProgerssBarColor(self, currentPercent, maxPercent):
        for limitValue, color in SCD.data.get('runeFeedColorRange', ()):
            if currentPercent < limitValue * maxPercent:
                return color

        return 'green'

    def refreshRight(self):
        if not self.selectedPos:
            self.refreshRightNoItem()
            return
        ASUtils.setHitTestDisable(self.widget.right, False)
        ASUtils.setMcEffect(self.widget.right, '')
        item = self.getItemByPos(*self.selectedPos)
        itemData = uiUtils.getGfxItemById(item.id, srcType='equipChangeRune_%d_%d_%d' % self.selectedPos)
        self.widget.right.slot2.slot.setItemSlotData(itemData)
        self.refreshConsume()

    def getTypeName(self, itemId):
        p = BigWorld.player()
        benyuanType = p.getRuneData(itemId, 'benyuanType', None)
        if benyuanType:
            for value in RPSMD.data.itervalues():
                if value.get('benyuanType', 0) == benyuanType:
                    return value.get('typeName')

        else:
            runeEffectType = p.getRuneData(itemId, 'runeEffectType', 0)
            for value in RPSMD.data.itervalues():
                if value.get('runeEffectType', 0) == runeEffectType:
                    return value.get('typeName')

        return ''

    def getReturnOldId(self, itemId):
        oldCrystalList = HCTOD.data.get(itemId, {}).get(1, [])
        oldItemId = oldCrystalList[0] if oldCrystalList else 0
        if not item.Item.isBindItem(itemId):
            oldItemId = item.Item.parentId(oldItemId)
        return oldItemId

    def refreshConsume(self):
        p = BigWorld.player()
        item = self.uiAdapter.equipChangeRuneFeed.getItemByPos(*self.selectedPos)
        if not item:
            return
        oldRuneId = self.getReturnOldId(item.id)
        runeLv = p.getRuneData(item.id, 'lv', 5)
        consumeCash = NRCD.data.get(runeLv, {}).get('recoverCash', 0)
        self.widget.right.selected.selected0.label = gameStrings.RUNE_RETURN_OLD % uiUtils.toHtml(p.getRuneData(oldRuneId, 'name', ''), '#ffc961')
        self.widget.right.needCash.cash.text = str(consumeCash)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshLeftItemList()
        self.refreshRight()
