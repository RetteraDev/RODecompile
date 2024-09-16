#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeRuneToItemProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import events
import const
from guis.asObject import ASObject
import gamelog
from guis.asObject import ASUtils
from guis.asObject import TipManager
from callbackHelper import Functor
from guis import uiUtils
from gamestrings import gameStrings
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import game_msg_data as GMD
from data import rune_to_material_num_data as RTMND
from cdata import game_msg_def_data as GMDD
RUNE_ITEM_MAX_CNT = 6

class EquipChangeRuneToItemProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeRuneToItemProxy, self).__init__(uiAdapter)
        self.modelMap = {'initPanel': self.onInitPanel,
         'unRegisterPanel': self.onUnRegisterPanel}
        self.widget = None
        self.reset()

    def reset(self):
        self.selectedBag = uiConst.BAG_INV
        self.targetItemNum = 0
        self.runeItemNum = 0
        self.runeData = {}

    def onExchangeHierogramSucc(self):
        self.targetItemNum = 0
        self.runeItemNum = 0
        self.runeData = {}
        self.refreshInfo()

    def onInitPanel(self, *args):
        p = BigWorld.player()
        self.widget = ASObject(args[3][0])
        self.initUI()
        self.refreshInfo()

    def onUnRegisterPanel(self, *args):
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.invBagBtn.addEventListener(events.BUTTON_CLICK, self.handleInvBagBtnClick, False, 0, True)
        self.widget.invBagBtn.groupName = 'equipChangeRuneToItem'
        self.widget.runeBagBtn.addEventListener(events.BUTTON_CLICK, self.handleInvRuneBtnClick, False, 0, True)
        self.widget.runeBagBtn.groupName = 'equipChangeRuneToItem'
        self.widget.scrollWndList.itemRenderer = 'EquipChangeBG_LeftItem'
        self.widget.scrollWndList.itemHeight = 64
        self.widget.scrollWndList.labelFunction = self.labelFunction
        for i in xrange(RUNE_ITEM_MAX_CNT):
            slotMc = self.widget.right.getChildByName('runeItem%d' % i)
            slotMc.slot.dragable = False
            slotMc.slot.setItemSlotData(None)
            slotMc.slotIdx = i
            slotMc.addEventListener(events.MOUSE_CLICK, self.handleRemoveItemClick, False, 0, True)

        self.widget.right.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.noItemHint.getChildAt(0).text = gameStrings.EQUIP_CHANGE_RUNE_NO_ITEM_DESC.get('toItem', '')
        self.widget.helpIcon.helpKey = SCD.data.get('runeToItemHelpKey', 1)

    def handleConfirmBtnClick(self, *args):
        if not self.runeData:
            return
        p = BigWorld.player()
        hieroExchangeTargetNum = getattr(p, 'hieroExchangeTargetNum', 0)
        hieroExchangeSourceNum = getattr(p, 'hieroExchangeSourceNum', 0)
        maxSourceType, maxSourceNum = SCD.data.get('runeBeExchangedLimit', (1, -1))
        maxTargetType, maxTargetNum = SCD.data.get('runeExchangeLimit', (1, -1))
        if maxSourceNum - hieroExchangeSourceNum - self.runeItemNum < 0:
            p.showGameMsg(GMDD.data.RUNE_TO_MATERIAL_SOURCE_ITEM_OVER_CNT, ())
            return
        if maxTargetNum - hieroExchangeTargetNum - self.targetItemNum < 0:
            p.showGameMsg(GMDD.data.RUNE_TO_MATERIAL_TARGET_ITEM_OVER_CNT, ())
            return
        itemIdList = []
        itemNumList = []
        resKindList = []
        pageList = []
        posList = []
        for bagType, page, pos in self.runeData.iterkeys():
            item = self.uiAdapter.equipChangeRuneFeed.getItemByPos(bagType, page, pos)
            if not item:
                continue
            itemIdList.append(item.id)
            itemNumList.append(self.runeData[bagType, page, pos][2])
            resKindList.append(const.RES_KIND_INV if bagType == uiConst.BAG_INV else const.RES_KIND_HIEROGRAM_BAG)
            pageList.append(page)
            posList.append(pos)

        gamelog.info('jbx:exchangeHierogramMaterial', itemIdList, itemNumList, resKindList, pageList, posList)
        p.base.exchangeHierogramMaterial(itemIdList, itemNumList, resKindList, pageList, posList)

    def handleRemoveItemClick(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx != uiConst.RIGHT_BUTTON:
            return
        else:
            slotIdx = e.currentTarget.slotIdx
            pos = None
            for itemPos, data in self.runeData.iteritems():
                if data[1] == slotIdx:
                    pos = itemPos
                    break

            if not pos:
                return
            if pos[0] == self.selectedBag:
                self.runeData[pos][0].selected = False
            e.currentTarget.slot.setItemSlotData(None)
            removeCnt = self.runeData[pos][2]
            self.runeData.pop(pos)
            item = self.uiAdapter.equipChangeRuneFeed.getItemByPos(*pos)
            targetItemNum = RTMND.data.get(item.id, {}).get('num', 0)
            self.runeItemNum -= removeCnt
            self.targetItemNum -= removeCnt * targetItemNum
            self.refreshItemCnt()
            return

    def labelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.data = itemData
        itemMc.pos = itemData.pos
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleItemClick, False, 0, True)
        pos = (int(itemData.pos[0]), int(itemData.pos[1]), int(itemData.pos[2]))
        if pos in self.runeData:
            self.runeData[pos][0].selected = False
            self.runeData[pos][0] = itemMc
            itemMc.selected = True
        else:
            itemMc.selected = False

    def handleInvBagBtnClick(self, *args):
        if self.selectedBag == uiConst.BAG_INV:
            return
        e = ASObject(args[3][0])
        e.currentTarget.selected = True
        self.selectedBag = uiConst.BAG_INV
        self.refreshInfo()

    def handleInvRuneBtnClick(self, *args):
        if self.selectedBag == uiConst.RUNE_INV_BAG:
            return
        e = ASObject(args[3][0])
        e.currentTarget.selected = True
        self.selectedBag = uiConst.RUNE_INV_BAG
        self.refreshInfo()

    def getMinCanToItemLv(self):
        return 3

    def handleItemClick(self, *args):
        if not self.widget or not self.widget.stage:
            return
        e = ASObject(args[3][0])
        if e.currentTarget.selected:
            return
        pos = (e.currentTarget.pos[0], e.currentTarget.pos[1], e.currentTarget.pos[2])
        if pos in self.runeData or len(self.runeData) >= RUNE_ITEM_MAX_CNT:
            return
        item = self.uiAdapter.equipChangeRuneFeed.getItemByPos(*pos)
        targetItemNum = RTMND.data.get(item.id, {}).get('num', 0)
        p = BigWorld.player()
        if not targetItemNum:
            p.showGameMsg(GMDD.data.RUNE_TO_MATERIAL_WRONG_ITEM_ID, ())
            return
        if self.getLeftTargetNum() <= 0 or self.getLeftSourceItem() <= 0:
            p.showGameMsg(GMDD.data.RUNE_TO_ITEM_OVER_CNT, ())
            return
        if item.cwrap > 1:
            self.uiAdapter.inventory.showNumberInputWidget(confirmCallback=Functor(self.confirmAddItem, item, targetItemNum, pos, e.currentTarget))
        else:
            self.confirmAddItem(item, targetItemNum, pos, e.currentTarget, 1)

    def confirmAddItem(self, item, targetItemNum, pos, targetMc, num):
        if not self.widget or not targetMc.stage:
            return
        if not num:
            return
        num = min(num, item.cwrap)
        emptyPos = range(RUNE_ITEM_MAX_CNT)
        for selectedMc, slotIdx, _ in self.runeData.itervalues():
            emptyPos.remove(slotIdx)

        self.runeItemNum += num
        self.targetItemNum += num * targetItemNum
        insertIdx = emptyPos[0]
        self.runeData[pos] = [targetMc, insertIdx, num]
        targetMc.selected = True
        self.refreshRight()

    def checkRuneItem(self, item, minLv):
        p = BigWorld.player()
        return item and p.getRuneData(item.id, 'lv', 1) >= minLv and item.isOldRune() and not p.getRuneData(item.id, 'benyuanType', None)

    def getRuneList(self):
        p = BigWorld.player()
        hieroCrystals = p.hierogramDict.get('hieroCrystals', None)
        itemList = []
        minLv = self.getMinCanToItemLv()
        if self.selectedBag == uiConst.BAG_EQUIP_RUNE:
            for pos, item in hieroCrystals.iteritems():
                if self.checkRuneItem(item, minLv):
                    itemList.append(self.uiAdapter.equipChangeRuneFeed.getGfxItemData(item, self.selectedBag, pos[0], pos[1]))

        elif self.selectedBag == uiConst.BAG_INV:
            for pageIdx, page in enumerate(BigWorld.player().inv.pages):
                for pos, item in enumerate(page):
                    if self.checkRuneItem(item, minLv):
                        itemList.append(self.uiAdapter.equipChangeRuneFeed.getGfxItemData(item, self.selectedBag, pageIdx, pos))

        else:
            for pageIdx, page in enumerate(BigWorld.player().hierogramBag.pages):
                for pos, item in enumerate(page):
                    if self.checkRuneItem(item, minLv):
                        itemList.append(self.uiAdapter.equipChangeRuneFeed.getGfxItemData(item, self.selectedBag, pageIdx, pos))

        return itemList

    def refreshLeftItemList(self):
        itemList = self.getRuneList()
        self.widget.scrollWndList.dataArray = itemList
        self.widget.noItemHint.visible = not bool(itemList)
        self.widget.runeBagBtn.selected = self.selectedBag == uiConst.RUNE_INV_BAG
        self.widget.invBagBtn.selected = self.selectedBag == uiConst.BAG_INV

    def refreshRight(self):
        p = BigWorld.player()
        slotList = range(RUNE_ITEM_MAX_CNT)
        for pos, data in self.runeData.iteritems():
            slotIdx = data[1]
            itemCnt = data[2]
            slotList.remove(slotIdx)
            slotMc = self.widget.right.getChildByName('runeItem%d' % slotIdx)
            item = self.uiAdapter.equipChangeRuneFeed.getItemByPos(*pos)
            itemSlotData = self.uiAdapter.equipChangeRuneFeed.getGfxItemData(item, count=itemCnt, *pos)
            slotMc.slot.dragable = False
            slotMc.slot.setItemSlotData(itemSlotData)

        for slotIdx in slotList:
            slotMc = self.widget.right.getChildByName('runeItem%d' % slotIdx)
            slotMc.slot.dragable = False
            slotMc.slot.setItemSlotData(None)

        self.refreshItemCnt()

    def getLeftTargetNum(self):
        p = BigWorld.player()
        hieroExchangeTargetNum = getattr(p, 'hieroExchangeTargetNum', 0)
        maxTargetType, maxTargetNum = SCD.data.get('runeExchangeLimit', (1, -1))
        return maxTargetNum - hieroExchangeTargetNum - self.targetItemNum

    def getLeftSourceItem(self):
        p = BigWorld.player()
        hieroExchangeSourceNum = getattr(p, 'hieroExchangeSourceNum', 0)
        maxSourceType, maxSourceNum = SCD.data.get('runeBeExchangedLimit', (1, -1))
        return maxSourceNum - hieroExchangeSourceNum - self.runeItemNum

    def refreshItemCnt(self):
        if not self.widget:
            return
        maxSourceType, maxSourceNum = SCD.data.get('runeBeExchangedLimit', (1, -1))
        maxTargetType, maxTargetNum = SCD.data.get('runeExchangeLimit', (1, -1))
        targetTypeStr = gameStrings.EQUIP_CHANGE_RUNE_TO_ITEM_TYPE_STR.get(maxTargetType, '')
        sourceTypeStr = gameStrings.EQUIP_CHANGE_RUNE_TO_ITEM_TYPE_STR.get(maxSourceType, '')
        leftTargetNum = self.getLeftTargetNum()
        leftSourceNum = self.getLeftSourceItem()
        if leftTargetNum <= 0:
            leftTargetCntStr = uiUtils.toHtml(str(leftTargetNum), '#FF471C') + '/' + str(maxTargetNum)
        else:
            leftTargetCntStr = '%d/%d' % (leftTargetNum, maxTargetNum)
        if leftSourceNum <= 0:
            leftSourceCntStr = uiUtils.toHtml(str(leftSourceNum), '#FF471C') + '/' + str(maxSourceNum)
        else:
            leftSourceCntStr = '%d/%d' % (leftSourceNum, maxSourceNum)
        leftItemStr = uiUtils.toHtml('%s(%s)' % (leftTargetCntStr, targetTypeStr), '#ffc961')
        self.widget.right.txtLeftItem.htmlText = gameStrings.EQUIP_CHANGE_RUNE_TO_ITEM_ITEM_CNT % leftItemStr
        leftRuneStr = uiUtils.toHtml('%s(%s)' % (leftSourceCntStr, sourceTypeStr), '#ffc961')
        self.widget.right.txtLeftRune.htmlText = gameStrings.EQUIP_CHANGE_RUNE_TO_ITEM_RUNE_CNT % leftRuneStr
        self.widget.right.toItems.slot.dragable = False
        slotData = uiUtils.getGfxItemById(SCD.data.get('runeExchangeItemId', 999), max(1, self.targetItemNum))
        self.widget.right.toItems.slot.setItemSlotData(slotData)
        self.widget.right.confirmBtn.enabled = leftTargetNum >= 0 and leftSourceNum >= 0

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshLeftItemList()
        self.refreshRight()
