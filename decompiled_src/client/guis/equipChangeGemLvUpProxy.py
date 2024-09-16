#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeGemLvUpProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
from guis import ui
from item import Item
from guis import uiUtils
import gametypes
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis import uiUtils
from callbackHelper import Functor
import utils
import itemToolTipUtils
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import equip_gem_data as EGD
from cdata import equip_gem_inverted_data as EGID
from cdata import game_msg_def_data as GMDD
GEM_SLOT_MAX_CNT = 5

class EquipChangeGemLvUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeGemLvUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.modelMap = {'initPanel': self.onInitPanel,
         'unRegisterPanel': self.onUnRegisterPanel}
        self.gemLvUpClicked = False
        self.reset()

    def reset(self):
        self.gemData = {}
        self.gemLv = None
        self.gemType = None
        self.selectedMcDic = {}
        self.needNum = 0
        self.mixItemEnough = False

    def onInitPanel(self, *args):
        self.widget = ASObject(args[3][0])
        self.initUI()
        self.refreshInfo()

    def onUnRegisterPanel(self, *args):
        self.reset()
        self.widget = None

    def initUI(self):
        self.widget.invBag.selected = True
        self.widget.helpIcon.visible = False
        self.widget.scrollWndList.itemRenderer = 'EquipChangeGem_GemItem'
        self.widget.scrollWndList.labelFunction = self.labelFunction
        for i in xrange(GEM_SLOT_MAX_CNT + 1):
            self.setGemSlotItem(i, None)
            slotMc = self.widget.getChildByName('slot%d' % i).slot
            slotMc.addEventListener(events.MOUSE_CLICK, self.handleSlotRemove, False, 0, True)
            slotMc.slotIdx = i
            slotMc.validateNow()

        self.widget.lvUpBtn.enabled = False
        self.widget.costItem.visible = False
        self.widget.lvUpBtn.addEventListener(events.BUTTON_CLICK, self.handleLvUpBtnClick, False, 0, True)

    def onGemLvUpNotify(self, rune):
        if not self.widget:
            return
        else:
            self.setGemSlotItem(GEM_SLOT_MAX_CNT, rune)
            for i in xrange(GEM_SLOT_MAX_CNT):
                self.setGemSlotItem(i, None)

            for addCount, selectedMc in self.selectedMcDic.itervalues():
                selectedMc.selectedMc.visible = False

            self.selectedMcDic.clear()
            self.gemLv = None
            self.gemType = None
            self.gemData = {}
            self.needNum = 0
            oldPositon = self.widget.scrollWndList.scrollbar.position
            self.refreshInfo()
            self.widget.scrollWndList.validateNow()
            self.widget.scrollWndList.scrollbar.position = oldPositon
            return

    def handleLvUpBtnClick(self, *args):
        gemPosList = tuple(self.gemData.values())
        srcGems = []
        p = BigWorld.player()
        for itemPos in gemPosList:
            item = BigWorld.player().inv.getQuickVal(itemPos[0], itemPos[1])
            if not item:
                continue
            if not BigWorld.player().inv.isEmpty(itemPos[0], itemPos[1]):
                srcGems.append(BigWorld.player().inv.getQuickVal(itemPos[0], itemPos[1]))

        if not srcGems:
            return
        bindInfo = [ gem.isForeverBind() for gem in srcGems if gem ]
        gemData = utils.getEquipGemData(srcGems[0].id)
        gemLv, gemType, gemSubType = gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)
        if gemLv == 0:
            return
        newGemId = EGID.data.get((gemLv + 1, gemType, gemSubType))
        mixItemNeed = EGD.data.get(newGemId, {}).get('mixItemNeed')
        if mixItemNeed:
            bindNum = p.inv.countItemInPages(mixItemNeed, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY, enableParentCheck=True)
            bindInfo.append(bindNum > 0)
        if any(bindInfo) and not all(bindInfo):
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_MIX_GEM_BIND, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._onConfirmMixBindEquipGem, gemPosList))
        else:
            self._onConfirmMixBindEquipGem(gemPosList)

    def _onConfirmMixBindEquipGem(self, gemPosList):
        p = BigWorld.player()
        srcGems = [ p.inv.getQuickVal(pg, pos) for pg, pos in gemPosList ]
        if not all(srcGems):
            return
        gemData = utils.getEquipGemData(srcGems[0].id)
        gemLv, gemType, gemSubType = gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)
        if gemLv == 0:
            return
        newGemId = EGID.data.get((gemLv + 1, gemType, gemSubType))
        newGemData = utils.getEquipGemData(newGemId)
        if newGemData.has_key('levelLimit') and p.lv < newGemData['levelLimit']:
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_MIX_GEM_LV_LIMIT, '')
            msg = msg % (newGemData.get('orderLimit', 1),)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._onConfirmMixLvLimitEquipGem, gemPosList))
        else:
            p.cell.mixEquipGem(gemPosList)

    def _onConfirmMixLvLimitEquipGem(self, runeData):
        BigWorld.player().cell.mixEquipGem(runeData)

    def handleSlotRemove(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx != uiConst.RIGHT_BUTTON:
            return
        else:
            slotIdx = int(e.currentTarget.slotIdx)
            if self.gemData.has_key(slotIdx):
                page, pos = self.gemData[slotIdx]
                if not self.selectedMcDic.has_key((page, pos)):
                    return
                addCount, selectedMc = self.selectedMcDic[page, pos]
                addCount -= 1
                if not addCount:
                    selectedMc.selectedMc.visible = False
                    self.selectedMcDic.pop((page, pos))
                else:
                    self.selectedMcDic[page, pos] = (addCount, selectedMc)
                self.gemData.pop(slotIdx)
            self.setGemSlotItem(slotIdx, None)
            self.refreshLvUpEnabled()
            return

    def labelFunction(self, *args):
        data = ASObject(args[3][0])
        mc = ASObject(args[3][1])
        item = BigWorld.player().inv.getQuickVal(int(data.itemPos[0]), int(data.itemPos[1]))
        if not item:
            return
        mc.overMc.visible = False
        ASUtils.setHitTestDisable(mc.overMc, True)
        ASUtils.setHitTestDisable(mc.selectedMc, True)
        itemData = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
        mc.item.data = itemData
        mc.item.pos = data.pos
        mc.item.dragable = False
        mc.txtName.htmlText = data.gemName
        mc.txtProperty.htmlText = data.addProp
        mc.addEventListener(events.MOUSE_OVER, self.onGemItemOver, False, 0, True)
        mc.addEventListener(events.MOUSE_OUT, self.onGemItemOut, False, 0, True)
        mc.addEventListener(events.MOUSE_CLICK, self.onGemItemClick, False, 0, True)
        mc.selectedMc.visible = False

    def onGemItemOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = True

    def onGemItemOut(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = False

    def refreshMixItem(self, mixItemId):
        if not mixItemId:
            self.widget.costItem.visible = False
            self.mixItemEnough = True
        else:
            self.widget.costItem.visible = True
            ownCnt = BigWorld.player().inv.countItemInPages(mixItemId, enableParentCheck=True)
            ownCnt = min(1, ownCnt)
            self.mixItemEnough = bool(ownCnt)
            itemData = uiUtils.getGfxItemById(mixItemId)
            countStr = '%d/%d' % (ownCnt, 1)
            if self.mixItemEnough:
                itemData['count'] = uiUtils.toHtml(countStr, '#FFFFE7')
            else:
                itemData['count'] = uiUtils.toHtml(countStr, '#F43804')
            self.widget.costItem.slot.setItemSlotData(itemData)
        self.refreshLvUpEnabled()

    def refreshLvUpEnabled(self):
        self.widget.lvUpBtn.enabled = self.mixItemEnough and len(self.gemData) == self.needNum

    def onGemItemClick(self, *args):
        if not self.widget:
            return
        else:
            if len(args) == 1:
                currentTarget = args[0]
            else:
                currentTarget = ASObject(args[3][0]).currentTarget
            if currentTarget.selectedMc.visible:
                return
            p = BigWorld.player()
            pos = currentTarget.item.pos
            page, pos = int(pos[0]), int(pos[1])
            i = BigWorld.player().inv.getQuickVal(page, pos)
            if not i:
                return
            addCount = 0
            if i.isEquipGem():
                if i.type == Item.BASETYPE_EQUIP_GEM:
                    gemData = utils.getEquipGemData(i.id)
                    gemLv, gemType, gemSubType = gemData.get('lv', 0), gemData.get('type', 0), gemData.get('subType', 0)
                    if self.gemData:
                        if gemLv != self.gemLv:
                            p.showGameMsg(GMDD.data.EQUIP_GEM_LVUP_RULE_LV_ERROR, ())
                            return
                        if (gemType, gemSubType) != self.gemType:
                            p.showGameMsg(GMDD.data.EQUIP_GEM_LVUP_RULE_TYPE_ERROR, ())
                            return
                    else:
                        self.gemLv = gemLv
                        self.gemType = (gemType, gemSubType)
                    newGemId = EGID.data.get((gemLv + 1, gemType, gemSubType))
                    needNum = SCD.data.get('EquipGemGemLvUpCount', 4)
                    mixItemId = EGD.data.get(newGemId, {}).get('mixItemNeed')
                    self.refreshMixItem(mixItemId)
                    if mixItemId:
                        needNum -= 1
                    self.needNum = needNum
                    gemCount = min(i.cwrap, max(1, needNum - len(self.gemData)))
                    gemCount and self.setGemSlotItem(GEM_SLOT_MAX_CNT, None)
                    for num in xrange(needNum):
                        self.addGemItem(page, pos)
                        addCount += 1
                        gemCount = gemCount - 1
                        if gemCount == 0:
                            currentTarget.selectedMc.visible = True
                            self.selectedMcDic[page, pos] = (addCount, currentTarget)
                            return

                    p.showGameMsg(GMDD.data.Gem_LVUP_GEM_FULL, (needNum,))
                currentTarget.selectedMc.visible = True
                self.selectedMcDic[page, pos] = (addCount, currentTarget)
            return

    def addGemItem(self, page, pos):
        p = BigWorld.player()
        item = p.inv.getQuickVal(page, pos)
        for slotId in xrange(GEM_SLOT_MAX_CNT):
            if slotId not in self.gemData:
                self.setGemSlotItem(slotId, item)
                self.gemData[slotId] = (page, pos)
                break

        self.refreshLvUpEnabled()

    def setGemSlotItem(self, slotId, item):
        if not self.widget:
            return
        else:
            slotMc = self.widget.getChildByName('slot%d' % slotId)
            slotData = None
            if item:
                slotData = uiUtils.getGfxItemById(item.id)
                slotData['count'] = 1
            slotMc.slot.setItemSlotData(slotData)
            return

    def getItemList(self):
        p = BigWorld.player()
        itemList = []
        for pg in p.inv.getPageTuple():
            for ps in p.inv.getPosTuple(pg):
                item = p.inv.getQuickVal(pg, ps)
                if item == const.CONT_EMPTY_VAL:
                    continue
                if item.isEquipGem():
                    gemData = EGD.data.get(item.parentId(item.id), {})
                    if not gemData:
                        continue
                    itemInfo = {}
                    itemInfo['itemPos'] = (pg, ps)
                    data = utils.getEquipGemData(item.id)
                    prop = data.get('gemProps', [])
                    addProp = ''
                    if len(prop) > 0:
                        addProp += itemToolTipUtils.getGemProp(prop)
                    itemInfo['addProp'] = addProp
                    itemInfo['gemName'] = uiUtils.getItemColorNameByItem(item, True)
                    itemInfo['gemLv'] = data.get('lv', 0)
                    itemInfo['isBinded'] = item.isForeverBind()
                    itemInfo['isAttProp'] = gemData.get('subType', 1) == 2
                    itemInfo['pos'] = (pg, ps)
                    itemList.append(itemInfo)

        return itemList

    def refreshLeftItemList(self):
        if not self.widget or not self.widget.stage:
            return
        gemList = self.getItemList()
        self.widget.scrollWndList.dataArray = gemList
        self.widget.noItemHint.visible = not bool(gemList)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshLeftItemList()
