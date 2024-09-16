#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeRuneLvUpProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
import gamelog
from guis import uiUtils
import formula
from guis import ui
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis import tipUtils
from gamestrings import gameStrings
from callbackHelper import Functor
from guis.asObject import TipManager
from uiProxy import SlotDataProxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from cdata import rune_lv_up_consume_data as RLUCD
from data import new_rune_data as NRD
from data import rune_data as RD
from data import new_rune_consume_data as NRCD
from cdata import rune_v2_sub_group_data as RV2SGD
from cdata import rune_sub_group_data as RSGD
RUNE_SLOT_MAX_CNT = 5

class EquipChangeRuneLvUpProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeRuneLvUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.modelMap = {'initPanel': self.onInitPanel,
         'unRegisterPanel': self.onUnRegisterPanel}
        self.runeLvUpClicked = False
        self.reset()

    def reset(self):
        self.selectedInv = uiConst.BAG_INV
        self.runeData = {}
        self.runeLv = None
        self.runeType = None
        self.selectedMcDic = {}
        self.needNum = 0
        self.mixItemEnouth = False
        self.consumeCoin = 0

    def onInitPanel(self, *args):
        widget = ASObject(args[3][0])
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def onUnRegisterPanel(self, *args):
        self.widget = None
        self.reset()

    def refreshRuneLvUpDesc(self):
        if not self.widget:
            return
        else:
            oldRuneIds = []
            newRuneIds = []
            p = BigWorld.player()
            for slotIdx in xrange(RUNE_SLOT_MAX_CNT):
                tab, page, pos = self.runeData.get(slotIdx, (None, None, None))
                if page != None and pos != None:
                    item = self.uiAdapter.equipChangeRuneFeed.getItemByPos(tab, page, pos)
                    if item and item.id:
                        if RD.data.has_key(item.id):
                            oldRuneIds.append(item.id)
                        else:
                            newRuneIds.append(item.id)

            if not oldRuneIds and not newRuneIds:
                self.widget.right.runeLvUpDesc.htmlText = gameStrings.EQUIP_CHANGE_RUNE_LV_UP_DESC
                self.widget.right.allRuneBtn.visible = False
                ASUtils.setMcEffect(self.widget.right.cost, 'gray')
                self.widget.right.cashTxt.text = '--'
                ASUtils.setMcEffect(self.widget.right.cashIcon, 'gray')
                ASUtils.setMcEffect(self.widget.right.cashTxt, 'gray')
                return
            self.widget.right.allRuneBtn.visible = True
            ASUtils.setMcEffect(self.widget.right.cost)
            ASUtils.setMcEffect(self.widget.right.cashIcon)
            ASUtils.setMcEffect(self.widget.right.cashTxt)
            allSubType = [ self._getRuneItemSubType(runeId) for runeId in oldRuneIds + newRuneIds ]
            allSubType = set(allSubType)
            if oldRuneIds and not newRuneIds:
                if len(allSubType) == 1:
                    gamelog.info('jbx:runeLvUpDesc1')
                    newRuneId = self.getNextLvRuneId(oldRuneIds[0], self.runeLv)
                    self.widget.right.runeLvUpDesc.htmlText = SCD.data.get('runeLvUpDesc1', 'runeLvUpDesc%s') % p.getRuneData(newRuneId, 'name', '')
                else:
                    gamelog.info('jbx:runeLvUpDesc2')
                    self.widget.right.runeLvUpDesc.htmlText = SCD.data.get('runeLvUpDesc2', 'runeLvUpDesc%s') % gameStrings.EQUIP_CHANGE_RUNE_TYPE_DESC.get(self.runeType, '')
            elif len(allSubType) > 1:
                gamelog.info('jbx:runeLvUpDesc3')
                self.widget.right.runeLvUpDesc.htmlText = (SCD.data.get('runeLvUpDesc3', 'runeLvUpDesc%s') % gameStrings.EQUIP_CHANGE_RUNE_TYPE_DESC.get(self.runeType, ''),)
            else:
                newPropIds = [ p.getRuneData(runeId, 'props', None) for runeId in newRuneIds ]
                newPropIds = set(newPropIds)
                if len(newPropIds) > 1:
                    gamelog.info('jbx:runeLvUpDesc4')
                    self.widget.right.runeLvUpDesc.htmlText = SCD.data.get('runeLvUpDesc4', 'runeLvUpDesc')
                else:
                    gamelog.info('jbx:runeLvUpDesc5')
                    newRuneId = self.getNextLvNewRuneId(newRuneIds[0], self.runeLv)
                    self.widget.right.runeLvUpDesc.htmlText = SCD.data.get('runeLvUpDesc5', 'runeLvUpDesc%s') % p.getRuneData(newRuneId, 'name', '')
            return

    def initUI(self):
        p = BigWorld.player()
        self.widget.invBag.addEventListener(events.BUTTON_CLICK, self.handleInvBagBtnClick, False, 0, True)
        self.widget.invBag.groupName = 'equipChangeRuneLvUp'
        self.widget.invRune.addEventListener(events.BUTTON_CLICK, self.handleInvRuneBtnClick, False, 0, True)
        self.widget.invRune.groupName = 'equipChangeRuneLvUp'
        self.widget.scrollWndList.itemRenderer = 'EquipChangeBG_LeftItem'
        self.widget.scrollWndList.itemHeight = 64
        self.widget.scrollWndList.labelFunction = self.scrollWndListLabelFunction
        self.widget.invBag.selected = True
        self.widget.allRuneTypes.visible = False
        self.widget.right.lvUpBtn.enabled = False
        self.widget.right.runeLvUpDesc.htmlText = SCD.data.get('runeLvUpDesc', '')
        for i in xrange(RUNE_SLOT_MAX_CNT):
            self.setRuneSlotItem(i, None)
            slotMc = self.widget.getChildByName('slot%d' % i).slot
            slotMc.addEventListener(events.MOUSE_CLICK, self.handleSlotRemove, False, 0, True)
            slotMc.dragable = False
            slotMc.slotIdx = i
            slotMc.validateNow()

        self.widget.right.lvUpBtn.addEventListener(events.BUTTON_CLICK, self.handleLvUpBtnClick, False, 0, True)
        self.widget.right.cost.gotoAndStop('cost1')
        self.widget.right.cost.visible = False
        self.widget.right.cost.materialItem.slot.setItemSlotData(None)
        self.widget.right.cost.materialItem.stateMc.visible = False
        self.widget.right.allRuneBtn.addEventListener(events.BUTTON_CLICK, self.handleAllRuneBtnClick, False, 0, True)
        self.widget.allRuneTypes.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleAllRuneCloseClick, False, 0, True)
        self.widget.right.returnItem.helpIcon.helpKey = SCD.data.get('runeLvUpReturnItemHelp', 1)
        self.widget.lvUpHintTxt.text = self.getCurLvUpHintTxt(p.lv)

    def handleAllRuneCloseClick(self, *args):
        self.widget.allRuneTypes.visible = False

    def refreshAllRuneTypes(self):
        runeAllTypes = SCD.data.get('runeAllTypes', ())
        if self.runeType == 1:
            runeAllTypes = runeAllTypes[0:4]
        else:
            runeAllTypes = runeAllTypes[4:]
        for index, typeData in enumerate(runeAllTypes):
            runeTypeMc = self.widget.allRuneTypes.getChildByName('runeType%d' % index)
            itemId, prop0, prop1, prop2 = typeData
            itemData = uiUtils.getGfxItemById(itemId)
            runeTypeMc.item.slot.setItemSlotData(itemData)
            runeTypeMc.txtName.htmlText = uiUtils.getItemColorName(itemId)
            runeTypeMc.txtProp0.text = prop0
            runeTypeMc.txtProp1.text = prop1
            runeTypeMc.txtProp2.text = prop2

    def handleAllRuneBtnClick(self, *args):
        self.widget.allRuneTypes.visible = not self.widget.allRuneTypes.visible
        if self.widget.allRuneTypes.visible:
            self.refreshAllRuneTypes()

    def handleLvUpBtnClick(self, *args):
        runeData = tuple(self.runeData.values())
        hasBind = False
        hasUnBind = False
        for itemPos in runeData:
            item = self.getItemByPos(*itemPos)
            if not item:
                continue
            if item.isForeverBind():
                hasBind = True
            else:
                hasUnBind = True

        itemCost = RLUCD.data.get((self.runeLv, self.runeType), {}).get('itemCost', [])
        if len(itemCost) > 0:
            itemId = int(itemCost[0])
            parentId = uiUtils.getParentId(itemId)
            _result1 = BigWorld.player().inv.countItemBind(itemId)
            _result2 = BigWorld.player().inv.countItemBind(parentId)
            hasCostItemBind = BigWorld.player().inv.countItemChild(itemId)
            _result3 = False
            if hasCostItemBind[0]:
                for childId in hasCostItemBind[1]:
                    _result3 = BigWorld.player().inv.countItemBind(childId)

            if _result1 or _result2 or _result3:
                hasBind = True
        if hasBind and hasUnBind:
            txt = uiUtils.getTextFromGMD(GMDD.data.RUNE_BIND_CONFIRM)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.realCommit, runeData))
        else:
            self.realCommit(runeData)

    def checkRuneSubTypes(self, runeData):
        p = BigWorld.player()
        if runeData:
            srcGems = [ self.uiAdapter.equipChangeRuneFeed.getItemByPos(tab, pg, pos) for tab, pg, pos in runeData ]
            firstGemType = 0
            for gem in srcGems:
                if gem:
                    firstGemType = self._getRuneItemSubType(gem.id)
                    break

            for gem in srcGems:
                if gem:
                    gemType = self._getRuneItemSubType(gem.id)
                    if firstGemType != gemType:
                        return False

        return True

    def _getRuneItemSubType(self, rId):
        p = BigWorld.player()
        runeType = p.getRuneData(rId, 'runeType', 0)
        if runeType == const.RUNE_TYPE_BENYUAN:
            return p.getRuneData(rId, 'benyuanType', 0)
        else:
            return p.getRuneData(rId, 'runeEffectType', 0)

    def realCommit(self, runeData):
        if self.checkRuneSubTypes(runeData):
            self.confirmRuneLvUp(runeData)
        else:
            descStr = uiUtils.getTextFromGMD(GMDD.data.RUNE_LV_UP_MIX_TYPES, 'GMDD.data.RUNE_LV_UP_MIX_TYPES')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(descStr, Functor(self.confirmRuneLvUp, runeData), msgType='runeLvUp', isShowCheckBox=True)

    def getNextLvRuneId(self, hieroId, runeLv):
        p = BigWorld.player()
        hieroType = p.getRuneData(hieroId, 'runeType', 0)
        subType = self._getRuneItemSubType(hieroId)
        rawPool = RSGD.data.get((hieroType, subType, runeLv + 1), [])
        if rawPool:
            return rawPool[0]
        return 0

    def getNextLvNewRuneId(self, hieroId, runeLv):
        p = BigWorld.player()
        hieroType = p.getRuneData(hieroId, 'runeType', 0)
        subType = self._getRuneItemSubType(hieroId)
        rawPool = RV2SGD.data.get((hieroType, subType, runeLv + 1), [])
        needPropType = NRD.data.get(hieroId, {}).get('propType', 0)
        pool = []
        for newId in rawPool:
            if needPropType == NRD.data.get(newId, {}).get('propType'):
                pool.append(newId)

        if pool:
            return pool[0]
        return 0

    def confirmRuneLvUp(self, runeData):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableHierogram', False):
            posList = []
            for posInfo in runeData:
                posWithInv = []
                if posInfo[0] == uiConst.RUNE_INV_BAG:
                    posWithInv = [const.RES_KIND_HIEROGRAM_BAG]
                else:
                    posWithInv = [const.RES_KIND_INV]
                posWithInv.extend(list(posInfo[1:]))
                posList.append(posWithInv)

            if self.widget.right.returnItem.checBox.selected:
                coinOwn = p.unbindCoin + p.bindCoin + p.freeCoin
                if self.consumeCoin and coinOwn < self.consumeCoin:
                    p.showGameMsg(GMDD.data.NOT_ENOUGH_COIN, ())
                else:
                    gamelog.info('jbx:composeNewHierogram, HIEROGRAM_COMPOSE_EXTRA_USE_COIN')
                    p.base.composeNewHierogram(posList, const.HIEROGRAM_COMPOSE_EXTRA_USE_COIN)
                return
            p.base.composeNewHierogram(posList, 0)
        else:
            p.cell.runeLvUp(runeData)

    def onRuneLvUpNotify(self, runeData):
        if not self.widget:
            return
        else:
            self.setRuneSlotItem(RUNE_SLOT_MAX_CNT, runeData, uiConst.EQUIP_CHANGE_NEW_ITEM_POS, uiConst.EQUIP_CHANGE_NEW_ITEM_POS)
            for i in xrange(RUNE_SLOT_MAX_CNT):
                self.setRuneSlotItem(i, None)

            for addCount, selectedMc in self.selectedMcDic.itervalues():
                selectedMc.selectedMc.visible = False

            self.selectedMcDic.clear()
            self.runeLv = None
            self.runeType = None
            self.runeData = {}
            self.needNum = 0
            oldPositon = self.widget.scrollWndList.scrollbar.position
            self.refreshLeftItems()
            self.refreshCostCoin()
            self.widget.right.lvUpBtn.enabled = False
            self.widget.scrollWndList.validateNow()
            self.widget.scrollWndList.scrollbar.position = oldPositon
            return

    def handleSlotRemove(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx != uiConst.RIGHT_BUTTON:
            return
        else:
            slotIdx = int(e.currentTarget.slotIdx)
            if not self.runeData.has_key(slotIdx):
                return
            tab, page, pos = self.runeData[slotIdx]
            if self.runeData.has_key(slotIdx) and self.selectedMcDic.has_key((tab, page, pos)):
                addCount, selectedMc = self.selectedMcDic[tab, page, pos]
                addCount -= 1
                if not addCount:
                    selectedMc.selectedMc.visible = False
                    self.selectedMcDic.pop((tab, page, pos))
                else:
                    self.selectedMcDic[tab, page, pos] = [addCount, selectedMc]
                self.runeData.pop(slotIdx)
            self.setRuneSlotItem(slotIdx, None)
            self.widget.right.lvUpBtn.enabled = len(self.runeData) == self.needNum and self.mixItemEnouth
            if not len(self.runeData):
                self.widget.right.cost.visible = False
                self.runeType = None
                self.runeLv = None
            self.refreshRuneLvUpDesc()
            self.refreshCostCoin()
            return

    def clearCacheData(self):
        for i in xrange(RUNE_SLOT_MAX_CNT):
            self.setRuneSlotItem(i, None)

        self.runeData = {}
        self.runeLv = None
        self.runeType = None
        self.selectedMcDic = {}
        self.needNum = 0
        self.mixItemEnouth = False

    def handleInvRuneBtnClick(self, *args):
        if self.selectedInv == uiConst.RUNE_INV_BAG:
            return
        e = ASObject(args[3][0])
        e.currentTarget.selected = True
        self.selectedInv = uiConst.RUNE_INV_BAG
        self.refreshLeftItems()

    def getInv(self):
        if self.selectedInv == uiConst.BAG_INV:
            return BigWorld.player().inv
        else:
            return BigWorld.player().hierogramBag

    def handleInvBagBtnClick(self, *args):
        if self.selectedInv == uiConst.BAG_INV:
            return
        e = ASObject(args[3][0])
        e.currentTarget.selected = True
        self.selectedInv = uiConst.BAG_INV
        self.refreshLeftItems()

    def scrollWndListLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.data = itemData
        itemMc.pos = itemData.pos
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleRuneItemClick, False, 0, True)
        if self.selectedMcDic.has_key((int(itemData.pos[0]), int(itemData.pos[1]), int(itemData.pos[2]))):
            itemMc.selected = True
            self.selectedMcDic[int(itemData.pos[0]), int(itemData.pos[1]), int(itemData.pos[2])][1] = itemMc
        else:
            itemMc.selected = False

    def refreshCostCoin(self):
        totalFeedCount = 0
        for tab, page, pos in self.runeData.itervalues():
            item = self.uiAdapter.equipChangeRuneFeed.getItemByPos(tab, page, pos)
            if item and item.isNewHieroCrystal():
                feedCount = item.getHieroSysProps('feedCount')
                totalFeedCount += feedCount

        self.consumeCoin = formula.getHieroCrystalComposeCoin(totalFeedCount) if totalFeedCount else 0
        if self.consumeCoin:
            self.widget.right.returnItem.visible = True
            self.widget.right.returnItem.cashTxt.text = str(self.consumeCoin)
        else:
            self.widget.right.returnItem.visible = False

    def refreshCostItem(self):
        oldRuneIds = []
        newRuneIds = []
        for tab, page, pos in self.runeData.itervalues():
            item = self.uiAdapter.equipChangeRuneFeed.getItemByPos(tab, page, pos)
            if item and item.id:
                if RD.data.has_key(item.id):
                    oldRuneIds.append(item.id)
                else:
                    newRuneIds.append(item.id)

        itemId, itemCnt = RLUCD.data.get((self.runeLv, self.runeType), {}).get('itemCost', [0, 0])
        cash = RLUCD.data.get((self.runeLv, self.runeType), {}).get('mCost', 0)
        self.widget.right.cost.visible = True
        ownCount = BigWorld.player().inv.countItemInPages(itemId, enableParentCheck=True)
        itemData = uiUtils.getGfxItemById(itemId)
        if oldRuneIds and newRuneIds:
            self.widget.right.cost.gotoAndStop('cost2')
            self.widget.right.cost.materialItem2.stateMc.visible = False
            transCfgData = NRCD.data.get(self.runeLv, {})
            transItemId, transItemCnt = transCfgData.get('fixedItems', ((999, 10),))[0]
            transItemCnt *= len(oldRuneIds)
            cash += transCfgData.get('fixedCash', 0) * len(oldRuneIds)
            transItemOwnCnt = BigWorld.player().inv.countItemInPages(transItemId, enableParentCheck=True)
            transItemData = uiUtils.getGfxItemById(transItemId)
            if transItemOwnCnt >= transItemCnt:
                transItemData['count'] = '%d/%d' % (transItemCnt, transItemCnt)
                self.widget.right.cost.materialItem2.slot.setItemSlotData(transItemData)
                self.widget.right.cost.materialItem2.slot.validateNow()
                self.mixItemEnouth = True
                self.widget.right.cost.materialItem2.slot.setSlotState(uiConst.ITEM_NORMAL)
            else:
                transItemData['count'] = '%s/%d' % (uiUtils.toHtml(str(transItemOwnCnt), '#FF471C'), transItemCnt)
                self.widget.right.cost.materialItem2.slot.setItemSlotData(transItemData)
                self.widget.right.cost.materialItem2.slot.validateNow()
                self.mixItemEnouth = False
                self.widget.right.cost.materialItem2.slot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
        else:
            self.widget.right.cost.gotoAndStop('cost1')
            self.mixItemEnouth = True
        if ownCount >= itemCnt:
            itemData['count'] = '%d/%d' % (ownCount, itemCnt)
            self.widget.right.cost.materialItem.slot.setItemSlotData(itemData)
            self.widget.right.cost.materialItem.slot.validateNow()
            self.mixItemEnouth = self.mixItemEnouth and True
            self.widget.right.cost.materialItem.slot.setSlotState(uiConst.ITEM_NORMAL)
        else:
            itemData['count'] = '%s/%d' % (uiUtils.toHtml(str(ownCount), '#FF471C'), itemCnt)
            self.widget.right.cost.materialItem.slot.setItemSlotData(itemData)
            self.widget.right.cost.materialItem.slot.validateNow()
            self.mixItemEnouth = False
            self.widget.right.cost.materialItem.slot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
        self.widget.right.cost.materialItem.stateMc.visible = False
        self.widget.right.lvUpBtn.enabled = len(self.runeData) == self.needNum and self.mixItemEnouth
        self.widget.right.cost.txtItem.visible = not self.mixItemEnouth
        self.widget.right.cashTxt.text = str(cash)

    def handleRuneItemClick(self, *args):
        if not self.widget or not self.widget.stage:
            return
        else:
            e = ASObject(args[3][0])
            currentTarget = e.currentTarget
            p = BigWorld.player()
            if self.needNum and len(self.runeData) == self.needNum:
                p.showGameMsg(GMDD.data.RUNE_LVUP_ITEM_CNT_FULL, self.needNum)
                return
            pos = currentTarget.pos
            page, pos = int(pos[1]), int(pos[2])
            item = self.getInv().getQuickVal(page, pos)
            if not item or not item.isRune():
                p.showGameMsg(GMDD.data.WRONG_TYPE_FOR_RUNE_LVUP, ())
                return
            cwarp = item.cwrap - self.selectedMcDic.get((self.selectedInv, page, pos), [0, None])[0]
            if not cwarp:
                return
            runeType = p.getRuneData(item.id, 'runeType', 0)
            runeLv = p.getRuneData(item.id, 'lv', 0)
            self.setRuneSlotItem(RUNE_SLOT_MAX_CNT, None)
            if not self.runeType:
                self.runeType = runeType
                self.runeLv = runeLv
            else:
                if runeType != self.runeType:
                    p.showGameMsg(GMDD.data.RUNE_LVUP_RULE_TYPE_ERROR, ())
                    return
                if runeLv != self.runeLv:
                    p.showGameMsg(GMDD.data.RUNE_LVUP_RULE_LV_ERROR, ())
                    return
            self.needNum = const.RUNE_ITEM_MIX_NUM_NEED.get(runeType, 0)
            runeCount = min(cwarp, max(0, self.needNum - len(self.runeData)))
            for num in xrange(runeCount):
                self.addRuneItem(page, pos)

            currentTarget.selected = True
            oldCnt = self.selectedMcDic.get((self.selectedInv, page, pos), (0, None))[0]
            self.selectedMcDic[self.selectedInv, page, pos] = [oldCnt + runeCount, currentTarget]
            self.refreshRuneLvUpDesc()
            self.refreshCostItem()
            self.refreshCostCoin()
            return

    def setRuneSlotItem(self, slotId, item, page = None, pos = None):
        if not self.widget:
            return
        else:
            slotMc = self.widget.getChildByName('slot%d' % slotId)
            slotData = None
            if item:
                slotData = self.uiAdapter.equipChangeRuneFeed.getGfxItemData(item, self.selectedInv, page, pos, count=1)
            slotMc.slot.setItemSlotData(slotData)
            return

    def getItemByPos(self, tab, page, pos):
        p = BigWorld.player()
        if tab == uiConst.BAG_EQUIP_RUNE:
            return p.hierogramDict.get('hieroCrystals', {}).get((page, pos), None)
        elif tab == uiConst.BAG_INV:
            return BigWorld.player().inv.getQuickVal(page, pos)
        else:
            return BigWorld.player().hierogramBag.getQuickVal(page, pos)

    def addRuneItem(self, page, pos):
        item = self.getItemByPos(self.selectedInv, page, pos)
        for slotId in xrange(RUNE_SLOT_MAX_CNT):
            if slotId not in self.runeData:
                self.runeData[slotId] = (self.selectedInv, page, pos)
                self.setRuneSlotItem(slotId, item, page, pos)
                break

        self.widget.right.lvUpBtn.enabled = len(self.runeData) == self.needNum and self.mixItemEnouth

    def getLeftItemList(self):
        inv = self.getInv()
        itemList = []
        p = BigWorld.player()
        for pageIdx, page in enumerate(inv.pages):
            for pos, item in enumerate(page):
                if item and item.isRune() and p.getRuneData(item.id, 'lv', 0) < SCD.data.get('runeMaxLv', 9):
                    itemData = uiUtils.getGfxItemById(item.id, srcType='equipChangeRune_%d_%d_%d' % (self.selectedInv, pageIdx, pos), count=item.cwrap)
                    itemData['itemName'] = uiUtils.getItemColorName(item.id)
                    desc = self.uiAdapter.equipChangeRuneFeed.getPropAndAddPercent(item)
                    itemData['itemName2'] = desc
                    itemData['pos'] = (self.selectedInv, pageIdx, pos)
                    itemList.append(itemData)

        return itemList

    def refreshLeftItems(self):
        itemList = self.getLeftItemList()
        self.widget.scrollWndList.dataArray = itemList
        self.widget.noItemHint.visible = not bool(itemList)
        self.refreshRuneLvUpDesc()

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshLeftItems()
        self.refreshCostCoin()

    def getCurLvUpHintTxt(self, lv):
        p = BigWorld.player()
        runeLvUpHintDict = SCD.data.get('runeLvUpHintDict', {})
        for runeLvUpHintInterval, runeLvUpHintTxt in runeLvUpHintDict.iteritems():
            if runeLvUpHintInterval[0] <= lv <= runeLvUpHintInterval[1]:
                return runeLvUpHintTxt

        return ''
