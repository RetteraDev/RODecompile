#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeRuneExchangeProxy.o
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
from data import new_rune_feed_data as NRFD
from data import sys_config_data as SCD
from data import new_rune_data as NRD
from data import new_rune_consume_data as NRCD
from data import rune_prop_pskill_map_data as RPSMD
from data import new_rune_property_data as NRPD
from cdata import hierogram_crystal_to_new_data as HCTND
from cdata import game_msg_def_data as GMDD

class EquipChangeRuneExchangeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeRuneExchangeProxy, self).__init__(uiAdapter)
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
        self.rightIndex = 0
        self.isItemCntEnough = False
        self.isCashCntEnough = False
        self.itemUuIdList = []

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
        for i in xrange(4):
            selectedMc = self.widget.right.selected.getChildByName('selected%d' % i)
            selectedMc.selectedMc.idx = i
            selectedMc.selectedMc.addEventListener(events.MOUSE_CLICK, self.handleSelectedItem, False, 0, True)
            selectedMc.slot0.slot.dragable = False

        self.widget.right.exchangeBtn.addEventListener(events.BUTTON_CLICK, self.handleExchangeBtnClick, False, 0, True)
        self.widget.helpIcon.helpKey = SCD.data.get('runeExchangeHelpKey', 1)
        self.widget.noItemHint.getChildAt(0).text = gameStrings.EQUIP_CHANGE_RUNE_NO_ITEM_DESC.get('exchange', '')
        ASUtils.setHitTestDisable(self.widget.right.needCash.cash, True)

    def handleExchangeBtnClick(self, *args):
        rightData = self.getRightData()
        itemIdList = rightData['itemIdList']
        if self.rightIndex == 3:
            itemId = 0
            transType = const.HIEROGRAM_TRANS_TYPE_RANDOM
        else:
            itemId = itemIdList[self.rightIndex] if self.rightIndex < len(itemIdList) else 0
            transType = const.HIEROGRAM_TRANS_TYPE_FIXED
        resKind = const.RES_KIND_INV if self.selectedBag == uiConst.BAG_INV else const.RES_KIND_HIEROGRAM_BAG
        gamelog.info('jbx:transferToNewHierogram', self.selectedPos[1], self.selectedPos[2], transType, itemId)
        transType = const.HIEROGRAM_TRANS_TYPE_FIXED if itemId else const.HIEROGRAM_TRANS_TYPE_RANDOM
        item = self.getItemByPos(*self.selectedPos)
        if item.isOldRune():
            BigWorld.player().base.transferToNewHierogram(resKind, self.selectedPos[1], self.selectedPos[2], transType, itemId)
        else:
            confirmTxt = uiUtils.getTextFromGMD(GMDD.data.RUNE_EXCHANGE_CONFIRM, 'GMDD.data.RUNE_EXCHANGE_CONFIRM')
            self.uiAdapter.messageBox.showYesNoMsgBox(confirmTxt, Functor(BigWorld.player().base.transferToNewHierogram, resKind, self.selectedPos[1], self.selectedPos[2], transType, itemId))

    def onTransferToNewHierogram(self, newItem):
        if not self.widget:
            return
        elif not newItem:
            return
        else:
            tab = self.selectedPos[0]
            p = BigWorld.player()
            if tab == uiConst.BAG_INV:
                inv = p.inv
            else:
                inv = p.hierogramBag
            _, page, pos = inv.findItemByUUID(newItem.uuid)
            if page != None and pos != None:
                self.selectedPos = (self.selectedPos[0], page, pos)
            self.selectedMc = None
            self.rightData = {}
            self.isItemCntEnough = False
            self.isCashCntEnough = False
            self.refreshInfo()
            self.widget.scrollWndList.scrollbar.validateNow()
            self.widget.scrollWndList.validateNow()
            if self.itemUuIdList:
                newPosition = self.itemUuIdList.index(newItem.uuid) * 1.0 / len(self.itemUuIdList) * self.widget.scrollWndList.scrollbar.maxPosition + 40
            else:
                newPosition = 0
            self.widget.scrollWndList.scrollbar.position = newPosition
            return

    def handleSelectedItem(self, *args):
        e = ASObject(args[3][0])
        if self.rightIndex == e.currentTarget.idx:
            return
        self.rightIndex = int(e.currentTarget.idx)
        self.refreshConsume()

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
        hieroCrystals = p.hierogramDict.get('hieroCrystals', None)
        itemList = []
        minLv = self.getExchangeMinLv()
        uuIdList = []
        if self.selectedBag == uiConst.BAG_EQUIP_RUNE:
            for pos, item in hieroCrystals.iteritems():
                if item and p.getRuneData(item.id, 'lv', 0) >= minLv and not p.getRuneData(item.id, 'benyuanType', None):
                    itemList.append(self.uiAdapter.equipChangeRuneFeed.getGfxItemData(item, self.selectedBag, pos[0], pos[1]))
                    uuIdList.append(item.uuid)

        elif self.selectedBag == uiConst.BAG_INV:
            for pageIdx, page in enumerate(BigWorld.player().inv.pages):
                for pos, item in enumerate(page):
                    if item and item.isRune() and p.getRuneData(item.id, 'lv', 0) >= minLv and not p.getRuneData(item.id, 'benyuanType', None):
                        itemList.append(self.uiAdapter.equipChangeRuneFeed.getGfxItemData(item, self.selectedBag, pageIdx, pos))
                        uuIdList.append(item.uuid)

        else:
            for pageIdx, page in enumerate(BigWorld.player().hierogramBag.pages):
                for pos, item in enumerate(page):
                    if item and item.isRune() and p.getRuneData(item.id, 'lv', 0) >= minLv and not p.getRuneData(item.id, 'benyuanType', None):
                        itemList.append(self.uiAdapter.equipChangeRuneFeed.getGfxItemData(item, self.selectedBag, pageIdx, pos))
                        uuIdList.append(item.uuid)

        return (itemList, uuIdList)

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
        itemList, self.itemUuIdList = self.getRuneList()
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
            for i in xrange(4):
                selectedMc = self.widget.right.selected.getChildByName('selected%d' % i)
                selectedMc.selectedMc.label = ' '
                selectedMc.slot0.slot.setItemSlotData(None)

            self.widget.right.needCash.cash.text = '--'
            self.widget.right.propDesc.text = ''
            return

    def getProgerssBarColor(self, currentPercent, maxPercent):
        for limitValue, color in SCD.data.get('runeFeedColorRange', ()):
            if currentPercent < limitValue * maxPercent:
                return color

        return 'green'

    def getMaxPercentByLv(self, level):
        maxVal = 1
        for data in NRPD.data.itervalues():
            if data['minLv'] <= level and data['maxVal'] > maxVal:
                maxVal = data['maxVal']

        maxVal = (maxVal - 1) * 100.0
        return maxVal

    def getRightData(self):
        p = BigWorld.player()
        rightData = {}
        itemIdList = []
        item = self.getItemByPos(*self.selectedPos)
        if item:
            lv = p.getRuneData(item.id, 'lv', 0)
            itemIdList = HCTND.data.get(item.id, {}).get(1, [])
            rightData['consuemData'] = NRCD.data.get(lv, {})
        rightData['itemIdList'] = itemIdList
        rightData['itemId'] = item.id
        self.widget.right.propDesc.text = gameStrings.EQUIP_CHANGE_RUNE_PROP_RANGE % (0.01, self.getMaxPercentByLv(lv))
        return rightData

    def refreshRight(self):
        if not self.selectedPos:
            self.refreshRightNoItem()
            return
        ASUtils.setHitTestDisable(self.widget.right, False)
        ASUtils.setMcEffect(self.widget.right, '')
        item = self.getItemByPos(*self.selectedPos)
        slot = self.widget.right.slot2.slot
        itemData = uiUtils.getGfxItemById(item.id, srcType='equipChangeRune_%d_%d_%d' % self.selectedPos)
        slot.setItemSlotData(itemData)
        slot.validateNow()
        ASUtils.autoSizeWithFont(slot.valueAmount, 14, slot.valueAmount.textWidth, 9)
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

    def refreshConsume(self):
        rightData = self.getRightData()
        p = BigWorld.player()
        consumeData = rightData['consuemData']
        itemIdList = rightData['itemIdList']
        consumeItemId, consuemCnt = consumeData['fixedItems'][0]
        consumeOwnCnt = min(consuemCnt, p.inv.countItemInPages(consumeItemId, enableParentCheck=True))
        consumeItemData = uiUtils.getGfxItemById(consumeItemId)
        if consumeOwnCnt < consuemCnt:
            consumeItemData['state'] = uiConst.COMPLETE_ITEM_LEAKED
            consumeItemData['count'] = uiUtils.toHtml('%d/%d' % (consumeOwnCnt, consuemCnt), '#FF471C')
        else:
            consumeItemData['count'] = '%d/%d' % (consumeOwnCnt, consuemCnt)
            consumeItemData['state'] = uiConst.ITEM_NORMAL
        randConsumeItemId, randconsumeItemCnt = consumeData['randomItems'][0]
        randOwnCnt = min(randconsumeItemCnt, p.inv.countItemInPages(randConsumeItemId, enableParentCheck=True))
        randConsumeItemData = uiUtils.getGfxItemById(randConsumeItemId)
        typeName = self.getTypeName(rightData['itemId'])
        if randOwnCnt < randconsumeItemCnt:
            randConsumeItemData['state'] = uiConst.COMPLETE_ITEM_LEAKED
            randConsumeItemData['count'] = uiUtils.toHtml('%d/%d' % (randOwnCnt, randconsumeItemCnt), '#FF471C')
        else:
            randConsumeItemData['state'] = uiConst.ITEM_NORMAL
            randConsumeItemData['count'] = '%d/%d' % (randOwnCnt, randconsumeItemCnt)
        for i in xrange(3):
            selectedMc = self.widget.right.selected.getChildByName('selected%d' % i)
            selectedMc.selectedMc.selected = i == self.rightIndex
            if i == self.rightIndex:
                self.isItemCntEnough = consumeOwnCnt >= randconsumeItemCnt
                self.widget.right.needCash.cash.text = consumeData['fixedCash']
                self.isCashCntEnough = p.cash + p.bindCash >= consumeData['fixedCash']
            selectedMc.slot0.slot.setItemSlotData(consumeItemData)
            selectedMc.slot0.slot.validateNow()
            ASUtils.autoSizeWithFont(selectedMc.slot0.slot.valueAmount, 14, selectedMc.slot0.slot.valueAmount.width, 9)
            itemId = itemIdList[i] if i < len(itemIdList) else 0
            propName = p.getRuneOwnProp(itemId)
            selectedMc.selectedMc.label = gameStrings.RUNE_EXCHANGE_FIX % (uiUtils.toHtml(propName, '#ffc961'), typeName)

        selectedMc = self.widget.right.selected.selected3
        if self.rightIndex == 3:
            selectedMc.selectedMc.selected = True
            self.isItemCntEnough = randOwnCnt >= randconsumeItemCnt
            self.isCashCntEnough = p.cash + p.bindCash >= consumeData['randomCash']
            self.widget.right.needCash.cash.text = consumeData['randomCash']
        else:
            selectedMc.selectedMc.selected = False
        selectedMc.slot0.slot.setItemSlotData(randConsumeItemData)
        selectedMc.slot0.slot.validateNow()
        ASUtils.autoSizeWithFont(selectedMc.slot0.slot.valueAmount, 14, selectedMc.slot0.slot.valueAmount.width, 9)
        selectedMc.selectedMc.label = gameStrings.RUNE_EXCHANGE_RAND % typeName

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshLeftItemList()
        self.refreshRight()
