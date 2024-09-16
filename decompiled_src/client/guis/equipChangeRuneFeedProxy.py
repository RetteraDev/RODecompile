#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeRuneFeedProxy.o
import BigWorld
import math
import gameglobal
import uiConst
import events
import const
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from guis import tipUtils
from uiProxy import UIProxy
from data import new_rune_feed_data as NRFD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class EquipChangeRuneFeedProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeRuneFeedProxy, self).__init__(uiAdapter)
        self.widget = None
        self.modelMap = {'initPanel': self.onInitPanel,
         'unRegisterPanel': self.onUnRegisterPanel}
        self.newItem = None
        self.reset()

    def reset(self):
        self.selectedBag = uiConst.BAG_EQUIP_RUNE
        self.selectedMc = None
        self.selectedPos = None
        self.autoSelected = True
        self.itemCount = 1

    def onInitPanel(self, *args):
        print 'jbx:onInitPanel'
        self.widget = ASObject(args[3][0])
        self.initUI()
        self.refreshInfo()

    def getTotalMinPercent(self, level = None):
        minValue = 1.0
        for value in NRFD.data.itervalues():
            if level and value.get('minLv', 0) != level:
                continue
            minValue = min(minValue, value.get('minVal', 1))

        return round(minValue - 1.0, 4)

    def getTotalMaxPercent(self, level = None):
        maxValue = 1.0
        for value in NRFD.data.itervalues():
            if level and value.get('minLv', 0) != level:
                continue
            maxValue = max(maxValue, value.get('maxVal', 1))

        return round(maxValue - 1.0, 4)

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
        self.widget.invBagBtn.tabIdx = uiConst.BAG_INV
        self.widget.runeBagBtn.tabIdx = uiConst.RUNE_INV_BAG
        self.widget.equipBtn.addEventListener(events.BUTTON_CLICK, self.handleBagChangeClick, False, 0, True)
        self.widget.invBagBtn.addEventListener(events.BUTTON_CLICK, self.handleBagChangeClick, False, 0, True)
        self.widget.runeBagBtn.addEventListener(events.BUTTON_CLICK, self.handleBagChangeClick, False, 0, True)
        self.widget.right.detail.materialControl.minimum = 0
        self.widget.right.detail.materialControl.value = 0
        self.widget.right.detail.materialControl.addEventListener(events.INDEX_CHANGE, self.handleNumChange, False, 0, True)
        self.widget.right.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.right.txtSucc.visible = False
        self.widget.right.txtFailed.visible = False
        self.widget.right.detail.maxBtn.addEventListener(events.BUTTON_CLICK, self.handleMaxBtnClick, False, 0, True)
        self.widget.noItemHint.getChildAt(0).text = gameStrings.EQUIP_CHANGE_RUNE_NO_ITEM_DESC.get('feed', '')
        ASUtils.setHitTestDisable(self.widget.right.effect, True)

    def handleMaxBtnClick(self, *args):
        self.widget.right.detail.materialControl.value = self.widget.right.detail.materialControl.maximum

    def handleConfirmBtnClick(self, *args):
        itemId, minCnt = SCD.data.get('hierogramGrowItem', (240248, 1))
        p = BigWorld.player()
        ownCnt = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if ownCnt < self.itemCount:
            p.showGameMsg(GMDD.data.HIEROGRAMGROWITEM_LACK_ITEM, ())
            return
        if self.selectedBag == uiConst.BAG_INV:
            resKind = const.RES_KIND_INV
        elif self.selectedBag == uiConst.BAG_EQUIP_RUNE:
            resKind = const.RES_KIND_HIEROGRAM_CRYSTALS
        else:
            resKind = const.RES_KIND_HIEROGRAM_BAG
        p.base.feedHierogram(resKind, self.selectedPos[1], self.selectedPos[2], itemId, self.itemCount)

    def onFeedHierogram(self, newItem, addValue):
        self.refreshInfo()
        if self.widget:
            if addValue < 1e-07:
                self.widget.right.txtFailed.visible = True
                self.widget.right.txtSucc.visible = False
            else:
                self.widget.right.txtFailed.visible = False
                self.widget.right.txtSucc.visible = True
                self.widget.right.txtSucc.text = gameStrings.RUNE_SUCC_ADD % (addValue * 100)
            self.widget.right.effect.gotoAndPlay(1)

    def handleNumChange(self, *args):
        self.itemCount = int(self.widget.right.detail.materialControl.value)
        self.refreshAddPropRange()

    def refreshAddPropRange(self):
        if not self.selectedPos:
            return
        p = BigWorld.player()
        item = self.getItemByPos(*self.selectedPos)
        currentPercent = self.getItemCurrentAddPercent(item)
        isMaxPercent = currentPercent >= self.getMaxFeedVal()
        feedData = self.getFeedData(currentPercent)
        itemId, minCnt = SCD.data.get('hierogramGrowItem', (240248, 1))
        self.itemCount = max(self.itemCount, minCnt)
        self.widget.right.detail.materialControl.minimum = minCnt
        self.widget.right.detail.materialControl.value = self.itemCount
        ownCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
        if isMaxPercent:
            maxCount = 1
        else:
            maxCount = min(10, math.ceil(1.0 / (feedData['rate'] * 1.0 / 10000)))
            maxCount = max(minCnt, maxCount)
        self.widget.right.detail.materialControl.maximum = maxCount
        self.widget.right.materialItem.clear()
        itemData = uiUtils.getGfxItemById(itemId, self.itemCount)
        if ownCount >= self.itemCount:
            itemData['count'] = '%d/%d' % (ownCount, self.itemCount)
            self.widget.right.materialItem.setState(uiConst.SLOT_STATE_EMPTY)
            self.widget.right.materialItem.slot.removeEventListener(events.MOUSE_CLICK, self.handleShowHelp)
        else:
            self.widget.right.materialItem.setState(uiConst.SLOT_STATE_HELP)
            itemData['count'] = uiUtils.toHtml('%d/%d' % (ownCount, self.itemCount), '#FF471C')
            self.widget.right.materialItem.slot.addEventListener(events.MOUSE_CLICK, self.handleShowHelp, False, 0, True)
        self.widget.right.materialItem.slot.setItemSlotData(itemData)
        if isMaxPercent:
            self.widget.right.detail.successRate.text = '--'
            self.widget.right.detail.refineRange.text = '--'
        else:
            succRate = feedData['rate'] / 10000.0 * self.itemCount
            self.widget.right.detail.successRate.text = '%.2f%%' % (min(1.0, succRate) * 100)
            minAddRate = feedData['minAddRate']
            maxAddRate = feedData['maxAddRate']
            if succRate >= 1.0:
                maxAddRate = maxAddRate * succRate
            self.widget.right.detail.refineRange.text = '%.2f%%~%.2f%%' % (minAddRate * 100, maxAddRate * 100)
            self.widget.right.detail.needCash.cash.text = '0'
        control = self.widget.right.detail.materialControl
        control.nextBtn.enabled = not control.value == control.maximum

    def handleShowHelp(self, *args):
        self.uiAdapter.itemSourceInfor.openPanel()

    def handleBagChangeClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.tabIdx == self.selectedBag:
            return
        else:
            self.autoSelected = True
            self.selectedPos = None
            self.selectedBag = e.currentTarget.tabIdx
            self.refreshInfo()
            return

    def onGetToolTip(self, srcType):
        _, tab, page, pos = srcType.split('_')
        tab = int(tab)
        page = int(page)
        pos = int(pos)
        if page == pos == uiConst.EQUIP_CHANGE_NEW_ITEM_POS:
            item = self.newItem
            return tipUtils.getItemTipByLocation(item, const.ITEM_IN_BAG)
        elif tab == uiConst.BAG_INV:
            item = BigWorld.player().inv.getQuickVal(page, pos)
            return tipUtils.getItemTipByLocation(item, const.ITEM_IN_BAG)
        elif tab == uiConst.RUNE_INV_BAG:
            item = BigWorld.player().hierogramBag.getQuickVal(page, pos)
            return tipUtils.getItemTipByLocation(item, const.ITEM_IN_BAG)
        elif tab == uiConst.BAG_EQUIP_RUNE:
            hieroCrystals = BigWorld.player().hierogramDict.get('hieroCrystals', None)
            item = hieroCrystals.get((page, pos))
            return tipUtils.getItemTipByLocation(item, const.ITEM_IN_BAG)
        elif tab == uiConst.BAG_RUNE_SHARE:
            hieroEquip = getattr(BigWorld.player(), 'sharedHierogramInfo', {}).get('hieroCrystals', {})
            item = hieroEquip.get((page, pos), None)
            return tipUtils.getItemTipByLocation(item, const.ITEM_IN_BAG)
        else:
            return

    def getPropAndAddPercent(self, item):
        p = BigWorld.player()
        propDesc = p.getRuneOwnProp(item.id)
        addPercent = p.getRuneAddPercent(item)
        if addPercent:
            propDesc = '%s+(%.2f%%)' % (propDesc, addPercent * 100)
        return propDesc

    def getGfxItemData(self, item, tab, page, pos, count = None):
        count = item.cwrap if not count else count
        itemData = uiUtils.getGfxItemById(item.id, srcType='equipChangeRune_%d_%d_%d' % (tab, page, pos), count=count)
        itemData['pos'] = (tab, page, pos)
        itemData['itemName'] = uiUtils.getItemColorName(item.id)
        itemData['itemName2'] = self.getPropAndAddPercent(item)
        if page == pos == uiConst.EQUIP_CHANGE_NEW_ITEM_POS:
            self.newItem = item
        return itemData

    def getItemByPos(self, tab, page, pos):
        p = BigWorld.player()
        if tab == uiConst.BAG_EQUIP_RUNE:
            return p.hierogramDict.get('hieroCrystals', {}).get((page, pos), None)
        elif tab == uiConst.BAG_INV:
            return BigWorld.player().inv.getQuickVal(page, pos)
        elif tab == uiConst.BAG_RUNE_SHARE:
            hieroEquip = getattr(BigWorld.player(), 'sharedHierogramInfo', {}).get('hieroCrystals', {})
            return hieroEquip.get((page, pos), None)
        else:
            return BigWorld.player().hierogramBag.getQuickVal(page, pos)

    def getMinCanFeedRuneLv(self):
        minvLv = 5
        for value in NRFD.data.itervalues():
            minLv = min(minvLv, value['minLv'])

        return minLv

    def checkItem(self, item, minLv, maxVal):
        p = BigWorld.player()
        return item and p.getRuneData(item.id, 'lv', 1) >= minLv and not item.isOldRune()

    def getMaxFeedVal(self):
        maxVal = 1.0
        for value in NRFD.data.itervalues():
            if value['maxVal'] > maxVal:
                maxVal = value['maxVal']

        return round(maxVal - 1.0, 4)

    def getRuneList(self):
        p = BigWorld.player()
        hieroCrystals = p.hierogramDict.get('hieroCrystals', None)
        itemList = []
        minLv = self.getMinCanFeedRuneLv()
        maxFeedVal = self.getMaxFeedVal()
        if self.selectedBag == uiConst.BAG_EQUIP_RUNE:
            for pos, item in hieroCrystals.iteritems():
                if self.checkItem(item, minLv, maxFeedVal):
                    itemList.append(self.getGfxItemData(item, self.selectedBag, pos[0], pos[1]))

        elif self.selectedBag == uiConst.BAG_INV:
            for pageIdx, page in enumerate(BigWorld.player().inv.pages):
                for pos, item in enumerate(page):
                    if self.checkItem(item, minLv, maxFeedVal):
                        itemList.append(self.getGfxItemData(item, self.selectedBag, pageIdx, pos))

        else:
            for pageIdx, page in enumerate(BigWorld.player().hierogramBag.pages):
                for pos, item in enumerate(page):
                    if self.checkItem(item, minLv, maxFeedVal):
                        itemList.append(self.getGfxItemData(item, self.selectedBag, pageIdx, pos))

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
        ASUtils.setMcEffect(self.widget.right, 'gray')
        ASUtils.setHitTestDisable(self.widget.right, True)
        self.widget.right.progressBar.currentValue = 0
        self.widget.right.progressBar.maxValue = self.getTotalMaxPercent()
        barData = {}
        barData['refinePer'] = '0%'
        barData['refineRange'] = gameStrings.RUNE_ADD_PROP % (self.getTotalMaxPercent() * 100)
        barData['lvTxt'] = gameStrings.RUNE_NOW_PROP
        self.widget.right.targetItem.clear()
        self.widget.right.progressBar.data = barData
        self.widget.right.txtSucc.text = ''
        self.widget.right.materialItem.clear()
        self.widget.right.detail.materialControl.value = 0
        self.widget.right.detail.successRate.text = '--'
        self.widget.right.detail.refineRange.text = '--'
        self.widget.right.detail.needCash.cash.text = '--'

    def getItemCurrentAddPercent(self, item):
        return BigWorld.player().getRuneAddPercent(item)

    def getFeedData(self, currentPercent):
        for value in NRFD.data.itervalues():
            if round(value['minVal'] - 1.0, 4) <= currentPercent < round(value['maxVal'] - 1.0, 4):
                return value

        return {}

    def getProgerssBarColor(self, currentPercent, maxPercent):
        if currentPercent >= maxPercent:
            return 'full'
        for limitValue, color in SCD.data.get('runeFeedColorRange', ()):
            if currentPercent < limitValue * maxPercent:
                return color

        return 'green'

    def refreshRight(self):
        if not self.selectedPos:
            self.refreshRightNoItem()
            return
        p = BigWorld.player()
        ASUtils.setMcEffect(self.widget.right, '')
        ASUtils.setHitTestDisable(self.widget.right, False)
        item = self.getItemByPos(*self.selectedPos)
        runeLv = p.getRuneData(item.id, 'lv', 1)
        currentPercent = self.getItemCurrentAddPercent(item)
        isMaxPercent = currentPercent >= self.getMaxFeedVal()
        feedData = self.getFeedData(currentPercent)
        itemId, minCnt = SCD.data.get('hierogramGrowItem', (240248, 1))
        self.itemCount = max(self.itemCount, minCnt)
        self.widget.right.detail.materialControl.minimum = minCnt
        self.widget.right.detail.materialControl.value = self.itemCount
        if isMaxPercent:
            maxCount = 1
        else:
            maxCount = min(10, math.ceil(1.0 / (feedData['rate'] * 1.0 / 10000)))
            maxCount = max(minCnt, maxCount)
        self.widget.right.detail.materialControl.maximum = maxCount
        barData = {}
        barData['lvTxt'] = gameStrings.RUNE_NOW_PROP
        barData['refinePer'] = '%.2f%%' % (currentPercent * 100)
        currentMaxPercent = self.getTotalMaxPercent(runeLv)
        currentMinPercent = self.getTotalMinPercent(runeLv)
        barData['refineRange'] = gameStrings.RUNE_ADD_PROP % (currentMaxPercent * 100)
        self.widget.right.progressBar.data = barData
        color = self.getProgerssBarColor(currentPercent, currentMaxPercent)
        self.widget.right.progressBar.bar.gotoAndStop(color)
        self.widget.right.progressBar.thumb.gotoAndStop(color)
        self.widget.right.progressBar.thumb.visible = currentPercent < self.getTotalMaxPercent()
        self.widget.right.progressBar.minValue = currentMinPercent
        self.widget.right.progressBar.maxValue = currentMaxPercent
        self.widget.right.progressBar.currentValue = currentPercent
        self.widget.right.targetItem.clear()
        itemData = uiUtils.getGfxItemById(item.id)
        itemData['srcType'] = 'equipChangeRune_%d_%d_%d' % (self.selectedPos[0], self.selectedPos[1], self.selectedPos[2])
        self.widget.right.targetItem.slot.setItemSlotData(itemData)
        self.widget.right.materialItem.clear()
        self.refreshAddPropRange()
        if isMaxPercent:
            self.widget.right.confirmBtn.enabled = False
        else:
            self.widget.right.confirmBtn.enabled = True

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshLeftItemList()
        self.refreshRight()
