#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/manualEquipLvUpProxy.o
import BigWorld
import math
import re
import gamelog
import itemToolTipUtils
import const
from callbackHelper import Functor
from gamestrings import gameStrings
from item import Item
import uiConst
from guis import events
from guis import uiUtils
from guis import tipUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from uiProxy import UIProxy
from data import equip_data as ED
from data import sys_config_data as SCD
from data import formula_client_data as FCD
from cdata import upgrade_manual_equip as UMD
from cdata import game_msg_def_data as GMDD
from cdata import equip_special_props_data as ESPD
from cdata import item_fame_score_cost_data as IFSCD
COST_ITEM_MAX_CNT = 3
COLOR_RED = '#d34024'

class ManualEquipLvUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ManualEquipLvUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MANUAL_EQUIP_LV_UP, self.hide)

    def reset(self):
        self.equipList = []
        self.selectedEquipMc = None
        self.selectedEquipPos = None
        self.costInfo = None
        self.isCostItemEnough = False
        self.isRarity = False
        self.makeNeedCnt = 0
        self.makeSelectedItems = []
        self.selectedChooseItem = None
        self.selectedChooseItemMc = None
        self.newItem = None
        self.npcEntityId = 0
        self.isCacheOk = False
        self.isItemOk = False
        self.isEquipOk = False

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MANUAL_EQUIP_LV_UP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.reset()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MANUAL_EQUIP_LV_UP)

    def show(self, npcEntityId):
        if BigWorld.player().lv < 70:
            BigWorld.player().showGameMsg(GMDD.data.MANUAL_EQUIP_LVUP_LV_NEED, ())
            return
        if not self.widget:
            self.npcEntityId = npcEntityId
            self.uiAdapter.loadWidget(uiConst.WIDGET_MANUAL_EQUIP_LV_UP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.removeAllInst(self.widget.left.scrollWndList.canvas, True)
        self.widget.left.scrollWndList.itemRenderer = 'ManualEquipLvUp_GemItem'
        self.widget.left.scrollWndList.labelFunction = self.equipItemLabelFunction
        self.widget.left.scrollWndList.cacheAsBitmap = True
        self.widget.left.sureBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBtnClick, False, 0, True)
        self.widget.left.diKou.checkBox.selected = True
        self.widget.left.diKou.checkBox.addEventListener(events.EVENT_SELECT, self.handleDikouSelectedChange, False, 0, True)
        self.widget.left.diKou.yunChui.btn.addEventListener(events.BUTTON_CLICK, self.handleYunChuiBtnClick, False, 0, True)
        self.widget.left.diKou.yunChui.icon.bonusType = 'yunChui'
        self.widget.left.diKou.coin.btn.addEventListener(events.BUTTON_CLICK, self.handleCoinBtnClick, False, 0, True)
        self.widget.chooseEquip.visible = False
        self.widget.chooseEquip.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleChooseEquipCloseBtnClick, False, 0, True)
        self.widget.chooseEquip.equipList.itemRenderer = 'M12_InventorySlot'
        self.widget.chooseEquip.equipList.labelFunction = self.chooseEquipLabelFunction
        self.widget.chooseEquip.equipList.cacheAsBitmap = True
        self.widget.chooseEquip.equipList.column = 6
        self.widget.chooseEquip.item0.showCloseBtn = False
        self.widget.chooseEquip.item1.showCloseBtn = False
        self.widget.chooseEquip.item0.keepCloseBtn = True
        self.widget.chooseEquip.item1.keepCloseBtn = True
        self.widget.chooseEquip.item0.stateMc.visible = False
        self.widget.chooseEquip.item1.stateMc.visible = False
        self.widget.chooseEquip.item0.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleRemoveBtnClick, False, 0, True)
        self.widget.chooseEquip.item1.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleRemoveBtnClick, False, 0, True)
        self.widget.chooseEquip.item0.slot.dragable = False
        self.widget.chooseEquip.item1.slot.dragable = False
        self.widget.left.oldEquip.slot.dragable = False
        self.widget.left.newEquip.slot.dragable = False
        self.widget.left.txtTips.htmlText = SCD.data.get('manualEquipLvUpTips', '')
        self.widget.removeAllInst(self.widget.chooseEquip.equipList.canvas, True)

    def handleRemoveBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemIndex = int(e.currentTarget.parent.name[-1])
        if itemIndex < len(self.makeSelectedItems):
            self.makeSelectedItems.pop(itemIndex)
        self.selectedChooseItem = None
        self.refreshCostInfo()
        self.refreshChooseEquips()

    def handleAddBtnClick(self, *args):
        if len(self.makeSelectedItems) >= self.makeNeedCnt:
            return
        itemData = self.selectedChooseItemMc.itemData
        item = BigWorld.player().inv.getQuickVal(int(itemData[0]), int(itemData[1]))
        if not item:
            return
        if item.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        refineCnt = getattr(item, 'refineManual', {}).get(item.REFINE_MANUAL_REFINE_CNT, 0)
        totalNum, lostNum, enhProp = uiUtils.getEquipTotalRefine(item)
        msgTxt = ''
        if item.isRarityMiracle():
            msgTxt += uiUtils.getTextFromGMD(GMDD.data.MANUAL_EQUIP_LVUP_RARITY, '') + '\n'
        if refineCnt:
            msgTxt += uiUtils.getTextFromGMD(GMDD.data.MANUAL_EQUIP_LVUP_REFINE, '') + '\n'
        if totalNum:
            msgTxt += uiUtils.getTextFromGMD(GMDD.data.MANUAL_EQUIP_LVUP_JUEXING, '') + '\n'
        if msgTxt:
            msgTxt += gameStrings.MANUAL_EQUIP_LV_UP_CONFIRM
            self.uiAdapter.messageBox.showYesNoMsgBox(msgTxt, Functor(self.doAddChooseEquip, itemData), textAlign='left')
        else:
            self.doAddChooseEquip(itemData)

    def doAddChooseEquip(self, itemData):
        self.makeSelectedItems.append((int(itemData[0]), int(itemData[1])))
        self.selectedChooseItem = None
        self.selectedChooseItemMc = None
        self.refreshCostInfo()
        self.refreshChooseEquips()

    def chooseEquipLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.doChooseEquipLabelFunction(itemData, itemMc)

    def doChooseEquipLabelFunction(self, itemData, itemMc):
        itemPage = int(itemData[0])
        itemPos = int(itemData[1])
        item = BigWorld.player().inv.getQuickVal(itemPage, itemPos)
        itemData = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
        itemMc.dragable = False
        if (itemPage, itemPos) == self.selectedChooseItem:
            if self.selectedChooseItemMc:
                self.selectedChooseItemMc.setSlotState(uiConst.ITEM_NORMAL)
            self.selectedChooseItemMc = itemMc
            self.selectedChooseItemMc.setSlotState(uiConst.ITEM_SELECTED)
        else:
            itemData['state'] = uiConst.ITEM_NORMAL
        itemMc.setItemSlotData(itemData)
        itemMc.itemData = (itemPage, itemPos)
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleSelectedItemClick, False, 0, True)

    def handleSelectedItemClick(self, *args):
        if not self.widget:
            return
        if len(self.makeSelectedItems) == self.makeNeedCnt:
            return
        e = ASObject(args[3][0])
        itemData = e.currentTarget.itemData
        if itemData in self.makeSelectedItems:
            return
        if itemData == self.selectedChooseItem:
            return
        if self.selectedChooseItemMc:
            self.selectedChooseItemMc.setSlotState(uiConst.ITEM_NORMAL)
        self.selectedChooseItemMc = e.currentTarget
        self.selectedChooseItem = itemData
        e.currentTarget.setSlotState(uiConst.ITEM_SELECTED)
        self.handleAddBtnClick()

    def handleChooseEquipCloseBtnClick(self, *args):
        self.widget.chooseEquip.visible = False

    def handleDikouSelectedChange(self, *args):
        self.refreshSureBtnEnable()

    def handleYunChuiBtnClick(self, *args):
        self.uiAdapter.tianBiToYunChui.show()

    def handleCoinBtnClick(self, *args):
        BigWorld.player().openRechargeFunc()

    def handleSureBtnClick(self, *args):
        if not self.makeSelectedItems:
            return
        if not (self.isCacheOk and (self.isItemOk or self.isCostItemEnough and self.widget.left.diKou.checkBox.selected) and self.isEquipOk):
            return
        equipList = []
        equipList.extend(self.selectedEquipPos)
        for page, pos in self.makeSelectedItems:
            equipList.append(page)
            equipList.append(pos)

        gamelog.info('jbx:upgradeManaulEquip', self.npcEntityId, equipList)
        self.uiAdapter.messageBox.showYesNoMsgBox(uiUtils.getTextFromGMD(GMDD.data.MANUAL_EQUIP_LVUP_CONFIRM, ''), Functor(BigWorld.player().cell.upgradeManaulEquip, self.npcEntityId, equipList))

    def equipItemLabelFunction(self, *args):
        mc = ASObject(args[3][1])
        itemData = ASObject(args[3][0])
        itemPage = int(itemData[0])
        itemPos = int(itemData[1])
        item = BigWorld.player().inv.getQuickVal(itemPage, itemPos)
        if not item:
            return
        mc.overMc.visible = False
        ASUtils.setHitTestDisable(mc.overMc, True)
        ASUtils.setHitTestDisable(mc.selectedMc, True)
        mc.item.data = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
        mc.item.setSlotState(uiConst.ITEM_NORMAL)
        mc.item.pos = itemData
        mc.item.dragable = False
        mc.txtName.htmlText = uiUtils.getItemColorNameByItem(item)
        mc.txtProperty.htmlText = ''
        mc.addEventListener(events.MOUSE_OVER, self.onGemItemOver, False, 0, True)
        mc.addEventListener(events.MOUSE_OUT, self.onGemItemOut, False, 0, True)
        mc.addEventListener(events.MOUSE_CLICK, self.onEquipItemClick, False, 0, True)
        if self.selectedEquipPos == (itemPage, itemPos):
            if self.selectedEquipMc:
                self.selectedEquipMc.selectedMc.visible = False
            mc.selectedMc.visible = True
            self.selectedEquipMc = mc
        else:
            mc.selectedMc.visible = False

    def onEquipItemClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.item.pos == self.selectedEquipPos:
            return
        else:
            p = BigWorld.player()
            item = BigWorld.player().inv.getQuickVal(e.currentTarget.item.pos[0], e.currentTarget.item.pos[1])
            if not item:
                return
            if item.hasLatch():
                BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
            if self.selectedEquipMc:
                self.selectedEquipMc.selectedMc.visible = False
            self.selectedEquipMc = e.currentTarget
            self.selectedEquipMc.selectedMc.visible = True
            self.selectedEquipPos = tuple(e.currentTarget.item.pos)
            self.selectedChooseItem = None
            self.makeSelectedItems = []
            self.isRarity = getattr(item, 'rarityMiracle', 0) == Item.EQUIP_IS_RARITY
            if not self.isRarity:
                data = item._getRandomEquipStarPropData()
                starPropFixScore = data.get('starPropFixScore', 0)
                allStarSEffectScore = starPropFixScore + ESPD.data.get(data.get('starSEffect', 0), {}).get('equipScore', 0)
                initScoreWithAllStar = item.initScore + allStarSEffectScore
                rarityMiracle = item.calcRarityMiracleEquip(initScoreWithAllStar)
                if rarityMiracle == Item.EQUIP_IS_RARITY or rarityMiracle == Item.EQUIP_IS_MIRACLE:
                    self.isRarity = True
            cfgData = UMD.data.get((item.id, 1 if self.isRarity else 0), {})
            needItemId, cnt, makeType = cfgData.get('extraNeedEquip', (0, 0, 0))
            self.refreshNewItem()
            self.makeNeedCnt = cnt
            self.refreshEquipInfo()
            self.refreshChooseEquips()
            return

    def onGemItemOver(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = True

    def onGemItemOut(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.overMc.visible = False

    def getEquipList(self):
        equipList = []
        p = BigWorld.player()
        for pageIndex, pageItems in enumerate(p.inv.pages):
            for posIndex, item in enumerate(pageItems):
                if not item:
                    continue
                isRarity = 1 if getattr(item, 'rarityMiracle', 0) == Item.EQUIP_IS_RARITY else 0
                if UMD.data.get((item.id, isRarity), None):
                    equipList.append((pageIndex, posIndex))

        return equipList

    def refreshEquipList(self):
        if not self.widget:
            return
        self.equipList = self.getEquipList()
        if not self.selectedEquipPos and self.equipList:
            for page, pos in self.equipList:
                item = BigWorld.player().inv.getQuickVal(page, pos)
                if item and not item.hasLatch():
                    self.selectedEquipPos = (page, pos)
                    self.isRarity = getattr(item, 'rarityMiracle', 0) == Item.EQUIP_IS_RARITY
                    cfgData = UMD.data.get((item.id, 1 if self.isRarity else 0), {})
                    needItemId, cnt, makeType = cfgData.get('extraNeedEquip', (0, 0, 0))
                    self.makeNeedCnt = cnt
                    self.refreshNewItem()
                    break

        self.widget.left.scrollWndList.dataArray = self.equipList
        self.widget.left.noItemHint.visible = not bool(self.equipList)

    def getCanUnbindTimes(self, i):
        configTimes = ED.data.get(i.id, {}).get('unbindTimes', 0)
        equipUnbindTimes = getattr(i, 'unbindTimes', 0)
        return configTimes - equipUnbindTimes

    def refreshSureBtnEnable(self):
        if not self.widget:
            return
        self.widget.left.sureBtn.disabled = False
        self.widget.left.sureBtn.enabled = self.isCacheOk and self.isEquipOk and (self.isItemOk or self.isCostItemEnough and self.widget.left.diKou.checkBox.selected)
        TipManager.removeTip(self.widget.left.sureBtn)
        if self.widget.left.sureBtn.enabled:
            if self.newItem.lvReq > BigWorld.player().lv:
                self.widget.left.sureBtn.disabled = True
                TipManager.addTip(self.widget.left.sureBtn, gameStrings.MANUAL_EQUIP_LV_REQUIRE % self.newItem.lvReq)

    def getSpecialProps(self, i):
        seManualProp = []
        for spId in i.getSpecialPropList():
            spData = ESPD.data.get(spId, {})
            if spData:
                seManualProp.append("<font color = \'#FF7F00\'>%s:%s</font>\n" % (spData.get('name', 'errorName'), spData.get('desc', 'errorDesc')))

        return seManualProp

    def setRandMc(self, itemMc, valueMc, itemInfo):
        itemMc.txt.htmlText = itemInfo['pName']
        if itemInfo['barType'] != 'no':
            valueMc.pValue.visible = False
            valueMc.progressBar.visible = True
            valueMc.subProgressBar.visible = True
            valueMc.progressBar.pValue.htmlText = itemInfo['pValue']
            valueMc.progressBar.currentValue = 100 - itemInfo['barValue']
            valueMc.subProgressBar.bar.gotoAndStop(itemInfo['barType'])
            valueMc.subProgressBar.currentValue = itemInfo['subBarValue']
        else:
            valueMc.progressBar.visible = False
            valueMc.subProgressBar.visible = False
            valueMc.pValue.htmlText = itemInfo['pValue']

    def setPropItem(self, propItem, prop):
        propItem.pName.htmlText = prop['pName']
        if prop['barType'] != 'no':
            propItem.pValue.visible = False
            propItem.progressBar.visible = True
            propItem.subProgressBar.visible = True
            propItem.progressBar.pValue.htmlText = prop['pValue']
            propItem.progressBar.currentValue = 100 - prop['barValue']
            propItem.subProgressBar.bar.gotoAndStop(prop['barType'])
            propItem.subProgressBar.currentValue = prop['subBarValue']
        else:
            propItem.progressBar.visible = False
            propItem.subProgressBar.visible = False
            propItem.pValue.htmlText = prop['pValue']

    def refreshPropList(self, propMc, propInfo, compareInfo = None):
        if not self.widget:
            return
        self.widget.removeAllInst(propMc, True)
        startY = 0
        for index, prop in enumerate(propInfo['shiftPropList']):
            propItem = self.widget.getInstByClsName('ManualEquipLvUp_PropItem')
            propItem.upMc.visible = False
            propMc.addChild(propItem)
            if compareInfo:
                newVale = self.getPropValue(prop)
                if index < len(compareInfo['shiftPropList']):
                    oldValue = self.getPropValue(compareInfo['shiftPropList'][index])
                    propItem.upMc.visible = True
                    if newVale and oldValue and float(newVale) - float(oldValue) > 0.0001:
                        propItem.upMc.visible = True
                    else:
                        propItem.upMc.visible = False
            self.setPropItem(propItem, prop)
            propItem.x = 0
            propItem.y = startY
            startY += 22

        if propInfo['extraProp']:
            propTxtItem = self.widget.getInstByClsName('ManualEquipLvUp_HieroWakeTitle')
            propMc.addChild(propTxtItem)
            propTxtItem.y = startY
            propTxtItem.x = 0
            propTxtItem.contentTxt.htmlText = propInfo['extraProp']
            propTxtItem.contentTxt.height = propTxtItem.contentTxt.textHeight + 10
            startY += propTxtItem.contentTxt.height + 10
        self.widget.left.propList.refreshHeight(startY)

    def getPropValue(self, propInfo):
        pValueStr = propInfo['pValue']
        pValueStr = re.findall('\\+(\\d+\\.*\\d*)', pValueStr)
        if pValueStr:
            return pValueStr[0]
        else:
            return None

    def getNeedItemInfo(self, needItemInfo, param):
        fId = needItemInfo[1][0]
        f = FCD.data.get(fId, {}).get('formula', None)
        needItemCnt = math.ceil(f(param))
        return (int(needItemInfo[0]), int(needItemCnt))

    def getCostInfo(self):
        costInfo = {}
        costItem = []
        item = BigWorld.player().inv.getQuickVal(self.selectedEquipPos[0], self.selectedEquipPos[1])
        costData = UMD.data.get((item.id, self.isRarity), {})
        needItemInfoA = costData.get('needItemA', 0)
        yangSlotsCnt = len([ sVal for sVal in getattr(item, 'yangSlots', []) if not sVal.isLocked() ])
        yinSlotsCnt = len([ sVal for sVal in getattr(item, 'yinSlots', []) if not sVal.isLocked() ])
        paramsA = {'yangSlotsCnt': yangSlotsCnt,
         'yinSlotsCnt': yinSlotsCnt,
         'p1': needItemInfoA[1][1],
         'p2': needItemInfoA[1][2]}
        needItems = []
        needItemIdA, needItemCntA = self.getNeedItemInfo(needItemInfoA, paramsA)
        if needItemCntA > 0:
            needItems.append((needItemIdA, needItemCntA))
        needItemInfoB = costData.get('needItemB', 0)
        paramsB = {'maxStarLv': item.maxStarLv,
         'p1': needItemInfoB[1][1],
         'p2': needItemInfoB[1][2]}
        needItemIdB, needItemCntB = self.getNeedItemInfo(needItemInfoB, paramsB)
        if needItemCntB > 0:
            needItems.append((needItemIdB, needItemCntB))
        diKouYunchui = 0
        diKouTianbi = 0
        for itemId, needCnt in needItems:
            ownCnt = BigWorld.player().inv.countItemInPages(itemId, enableParentCheck=True)
            isEnough = True
            if ownCnt < needCnt:
                ownCntStr = uiUtils.toHtml(str(ownCnt), COLOR_RED)
                countStr = '%s/%d' % (ownCntStr, needCnt)
                diKouNeed = IFSCD.data.get(itemId, {}).get(453, 0)
                diKouYunchui += (needCnt - ownCnt) * diKouNeed
                isEnough = False
                diKouTianbi += (needCnt - ownCnt) * 0
            else:
                countStr = '%d/%d' % (ownCnt, needCnt)
            itemInfo = uiUtils.getGfxItemById(itemId, countStr)
            itemInfo['isEnough'] = isEnough
            costItem.append(itemInfo)

        costInfo['costItem'] = costItem
        costInfo['diKouYunchui'] = diKouYunchui
        costInfo['diKouTianbi'] = diKouTianbi
        needCashInfo = costData.get('needCash', 0)
        paramsCash = {'maxStarLv': item.maxStarLv,
         'p1': needCashInfo[1],
         'p2': needCashInfo[2]}
        fId = needCashInfo[0]
        f = FCD.data.get(fId, {}).get('formula', None)
        needCash = int(math.ceil(f(paramsCash)))
        costInfo['needCash'] = needCash
        return costInfo

    def refreshCostInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        costInfo = self.getCostInfo()
        self.costInfo = costInfo
        tianbiEnough = True
        yunChuiEnought = True
        self.isItemOk = True
        for i in xrange(COST_ITEM_MAX_CNT):
            costMc = self.widget.left.getChildByName('costItem%d' % i)
            costMc.removeEventListener(events.MOUSE_CLICK, self.handleStateMcClick)
            costMc.removeEventListener(events.MOUSE_CLICK, self.handleCostEquipClick)
            if i >= len(costInfo['costItem']):
                costMc.visible = False
            else:
                costMc.visible = True
                itemInfo = costInfo['costItem'][i]
                costMc.slot.setItemSlotData(itemInfo)
                costMc.slot.validateNow()
                ASUtils.autoSizeWithFont(costMc.slot.valueAmount, 14, costMc.slot.valueAmount.width, 4)
                if itemInfo['isEnough']:
                    costMc.stateMc.visible = False
                else:
                    self.isItemOk = False
                    ASUtils.setHitTestDisable(costMc.stateMc, True)
                    costMc.stateMc.visible = True
                    costMc.itemId = itemInfo['id']
                    costMc.addEventListener(events.MOUSE_CLICK, self.handleStateMcClick, False, 0, True)

        costEquipIndex = len(costInfo['costItem'])
        item = p.inv.getQuickVal(self.selectedEquipPos[0], self.selectedEquipPos[1])
        isRarity = 1 if getattr(item, 'rarityMiracle', 0) == Item.EQUIP_IS_RARITY else 0
        costEquipItemId, cnt, makeType = UMD.data.get((item.id, isRarity), {}).get('extraNeedEquip', (0, 0, 0))
        if len(self.makeSelectedItems) >= self.makeNeedCnt:
            textStr = '%d/%d' % (len(self.makeSelectedItems), self.makeNeedCnt)
        else:
            textStr = '%s/%d' % (uiUtils.toHtml(str(len(self.makeSelectedItems)), COLOR_RED), self.makeNeedCnt)
        costEquipItemData = uiUtils.getGfxItemById(costEquipItemId, textStr)
        costMc = self.widget.left.getChildByName('costItem%d' % costEquipIndex)
        costMc.visible = True
        costMc.slot.setItemSlotData(costEquipItemData)
        ASUtils.setHitTestDisable(costMc.stateMc, True)
        if len(self.makeSelectedItems) >= self.makeNeedCnt:
            costMc.stateMc.visible = False
        else:
            costMc.stateMc.visible = True
        costMc.addEventListener(events.MOUSE_CLICK, self.handleCostEquipClick, False, 0, True)
        if costInfo['diKouYunchui'] > p.getFame(453):
            self.widget.left.diKou.yunChui.value.htmlText = uiUtils.toHtml('%s/%s' % (p.getFame(453), costInfo['diKouYunchui']), COLOR_RED)
            self.widget.left.diKou.yunChui.btn.enabled = True
            yunChuiEnought = False
        else:
            self.widget.left.diKou.yunChui.btn.enabled = False
            self.widget.left.diKou.yunChui.value.htmlText = '%s/%s' % (p.getFame(453), costInfo['diKouYunchui'])
        self.widget.left.diKou.coin.visible = False
        self.isCostItemEnough = tianbiEnough or yunChuiEnought
        self.isCacheOk = BigWorld.player().cash >= costInfo['needCash']
        self.widget.left.needCash.cash.htmlText = costInfo['needCash'] if self.isCacheOk else uiUtils.toHtml(costInfo['needCash'], COLOR_RED)
        self.refreshSureBtnEnable()

    def handleCostEquipClick(self, *args):
        if self.widget.chooseEquip.visible:
            self.widget.chooseEquip.visible = False
        else:
            self.widget.chooseEquip.visible = True
            self.refreshChooseEquips()

    def getChooseEquipsList(self):
        itemList = []
        p = BigWorld.player()
        item = p.inv.getQuickVal(self.selectedEquipPos[0], self.selectedEquipPos[1])
        isRarity = 1 if getattr(item, 'rarityMiracle', 0) == Item.EQUIP_IS_RARITY else 0
        needItemId, cnt, makeType = UMD.data.get((item.id, isRarity), {}).get('extraNeedEquip', (0, 0, 0))
        for pageIndex, pageItems in enumerate(p.inv.pages):
            for pos, chooseItem in enumerate(pageItems):
                if not chooseItem:
                    continue
                if (pageIndex, pos) in self.makeSelectedItems:
                    continue
                if chooseItem.uuid == item.uuid:
                    continue
                if chooseItem.id == needItemId and makeType == chooseItem.makeType:
                    itemList.append((pageIndex, pos))

        return itemList

    def refreshChooseEquips(self):
        if not self.widget:
            return
        if not self.selectedEquipPos:
            self.widget.chooseEquip.visible = False
            return
        self.widget.chooseEquip.visible = True
        p = BigWorld.player()
        item = p.inv.getQuickVal(self.selectedEquipPos[0], self.selectedEquipPos[1])
        self.isRarity = getattr(item, 'rarityMiracle', 0) == Item.EQUIP_IS_RARITY
        cfgData = UMD.data.get((item.id, 1 if self.isRarity else 0), {})
        needItemId, cnt, makeType = cfgData.get('extraNeedEquip', (0, 0, 0))
        self.makeNeedCnt = cnt
        self.refreshSelectedItems()
        itemList = self.getChooseEquipsList()
        if itemList and not self.selectedChooseItem:
            self.selectedChooseItem = tuple(itemList[0])
        self.widget.chooseEquip.equipList.dataArray = itemList
        self.refreshSelectedCnt()
        if self.isRarity:
            self.widget.chooseEquip.txtTips.htmlText = SCD.data.get('manualEquipLvUpChooseItemRarity', '')
        else:
            self.widget.chooseEquip.txtTips.htmlText = SCD.data.get('manualEquipLvUpChooseItemNotRarity', '')
        self.isEquipOk = len(self.makeSelectedItems) >= self.makeNeedCnt
        self.refreshSureBtnEnable()

    def refreshSelectedItems(self):
        self.widget.chooseEquip.item1.visible = self.makeNeedCnt != 1
        if not self.widget.chooseEquip.item1.visible:
            self.widget.chooseEquip.item0.x = 112
        else:
            self.widget.chooseEquip.item0.x = 55
        for i in xrange(self.makeNeedCnt):
            itemMc = self.widget.chooseEquip.getChildByName('item%d' % i)
            if i < len(self.makeSelectedItems):
                item = BigWorld.player().inv.getQuickVal(*self.makeSelectedItems[i])
                itemMc.slot.setItemSlotData(uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG))
                itemMc.setState(uiConst.SLOT_STATE_EMPTY)
                itemMc.showCloseBtn = True
            else:
                itemMc.slot.setItemSlotData(None)
                itemMc.showCloseBtn = False

    def refreshSelectedCnt(self):
        if not self.widget:
            return
        self.widget.chooseEquip.txtChoosed.text = gameStrings.MANUAL_EQUIP_SELECTED_CNT % (len(self.makeSelectedItems), self.makeNeedCnt)

    def handleStateMcClick(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.itemId:
            self.uiAdapter.itemSourceInfor.openPanel()

    def refreshEquipInfo(self):
        if not self.widget:
            return
        else:
            item = None
            if self.selectedEquipPos:
                item = BigWorld.player().inv.getQuickVal(self.selectedEquipPos[0], self.selectedEquipPos[1])
            if not item:
                self.widget.left.oldEquip.slot.setItemSlotData(None)
                self.widget.left.txtOldEquipName.text = ''
                self.widget.left.txtOldBindCnt.text = ''
                self.widget.left.newEquip.slot.setItemSlotData(None)
                self.widget.left.txtNewEquipName.text = ''
                self.widget.left.txtNewBindCnt.text = ''
                self.widget.left.txtNotSelectedEquip.visible = True
                self.widget.left.propList.visible = False
                self.widget.left.emptyMc.visible = True
                self.widget.left.needCash.cash.text = ''
                self.widget.left.sureBtn.enabled = False
                self.widget.left.txtOldBind.text = ''
                self.widget.left.txtNewBind.text = ''
                self.widget.chooseEquip.visible = False
                return
            self.widget.left.emptyMc.visible = False
            self.widget.left.propList.visible = True
            self.widget.left.txtNotSelectedEquip.visible = False
            self.widget.removeAllInst(self.widget.left.propList.canvas.oldProps, False)
            self.widget.removeAllInst(self.widget.left.propList.canvas.newProps, False)
            self.widget.left.oldEquip.slot.setItemSlotData(uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG))
            self.widget.left.txtOldEquipName.htmlText = uiUtils.getItemColorNameByItem(item)
            self.widget.left.txtOldBindCnt.text = gameStrings.MANUAL_EQUIP_LV_UP % self.getCanUnbindTimes(item)
            self.widget.left.txtOldBind.text = gameStrings.MANUAL_EQUIP_BIND if item.isForeverBind() else gameStrings.MANUAL_EQUIP_UNBIND
            propInfo = itemToolTipUtils.formatRet(BigWorld.player(), item)
            self.refreshPropList(self.widget.left.propList.canvas.oldProps, propInfo)
            self.refreshNewItem()
            self.refreshCostInfo()
            return

    def onGetToolTip(self):
        return tipUtils.getItemTipByLocation(self.newItem, const.ITEM_IN_BAG)

    def refreshNewItem(self):
        item = None
        p = BigWorld.player()
        if self.selectedEquipPos:
            item = BigWorld.player().inv.getQuickVal(self.selectedEquipPos[0], self.selectedEquipPos[1])
        else:
            self.widget.left.newEquip.slot.setItemSlotData(None)
            self.widget.left.txtNewEquipName.text = ''
            self.widget.left.txtNewBindCnt.text = ''
            self.widget.left.txtNewBind.text = ''
            self.refreshPropList(self.widget.left.propList.canvas.newProps, {'shiftPropList': [],
             'extraProp': ''})
            return
        propInfo = itemToolTipUtils.formatRet(BigWorld.player(), item)
        cfgData = UMD.data.get((item.id, 1 if self.isRarity else 0), {})
        targetEquipId = cfgData.get('targetEquip', 0)
        newEquip = Item(targetEquipId)
        upgradeEquip = newEquip.createUpgradeEquip(item, cfgData)
        fromGuilds = [item.uuid]
        for page, pos in self.makeSelectedItems:
            fromGuilds.append(p.inv.getQuickVal(page, pos).uuid)

        upgradeEquip.fromGuid = fromGuilds
        self.newItem = newEquip
        self.widget.left.newEquip.slot.setItemSlotData(uiUtils.getGfxItemById(self.newItem.id, srcType='manuqlEquipLvUp'))
        self.widget.left.txtNewEquipName.htmlText = uiUtils.getItemColorNameByItem(self.newItem)
        self.widget.left.txtNewBindCnt.text = gameStrings.MANUAL_EQUIP_LV_UP % self.getCanUnbindTimes(self.newItem)
        self.widget.left.txtNewBind.text = gameStrings.MANUAL_EQUIP_BIND if self.newItem.isForeverBind() else gameStrings.MANUAL_EQUIP_UNBIND
        newPropInfo = itemToolTipUtils.formatRet(BigWorld.player(), self.newItem, location=const.ITEM_IN_BAG)
        self.refreshPropList(self.widget.left.propList.canvas.newProps, newPropInfo, propInfo)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshEquipList()
        self.refreshEquipInfo()
        self.refreshChooseEquips()

    def onUpgradeEquipSucc(self):
        self.equipList = []
        self.selectedEquipMc = None
        self.selectedEquipPos = None
        self.costInfo = None
        self.isCostItemEnough = False
        self.isRarity = False
        self.makeNeedCnt = 0
        self.makeSelectedItems = []
        self.selectedChooseItem = None
        self.selectedChooseItemMc = None
        self.newItem = None
        self.isCacheOk = False
        self.isItemOk = False
        self.isEquipOk = False
        self.refreshInfo()
