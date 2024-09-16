#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardMakeProxy.o
import BigWorld
from Scaleform import GfxValue
import math
import gameglobal
import gametypes
import events
import uiUtils
import uiConst
import const
import ui
from uiProxy import UIProxy
from asObject import TipManager
from asObject import ASUtils
from asObject import Tweener
from asObject import ASObject
from gamestrings import gameStrings
from callbackHelper import Functor
from data import base_card_data as BCD
from data import consumable_item_data as CID
from data import prop_ref_data as PRD
from data import sys_config_data as SCD
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
OP_UPGRADE_CARD_PROGRESS = 1
OP_DEGRADE_CARD_PROGRESS = 2
OP_DEGRADE_CARD_DECOMPOSE = 3
OP_CARD_RENEWAL = 4
PROGRESS_VALUE = 100
CONSUMABLE_NUM_MAX = 2

class CardMakeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardMakeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.showCardEquip = True
        self.reset()

    def reset(self):
        self.cardAnim = None
        self.flashCardAnimCB = None
        self.animCB = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.cancelAnimCallBack()
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.consumableMc.itemMax.addEventListener(events.BUTTON_CLICK, self._onItemMaxClick, False, 0, True)
        self.widget.consumableMc.fragmentMax.addEventListener(events.BUTTON_CLICK, self._onFragmentMaxClick, False, 0, True)
        self.widget.progressYellow.labelFunction = self.maxProgressLabelFunc
        self.widget.consumableMc.itemCount.minCount = 0
        self.widget.consumableMc.fragmentCount.minCount = 0
        self.widget.consumableMc.itemCount.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCountChange, False, 0, True)
        self.widget.consumableMc.fragmentCount.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCountChange, False, 0, True)
        self.widget.compoundRadioBtn.group.addEventListener(events.EVENT_CHANGE, self.handleOpBtnSelected, False, 0, True)
        self.widget.nulinIcon.bonusType = 'huanjiannulin'
        self.widget.disheIcon.bonusType = 'huanjiandishe'
        self.uiAdapter.cardSystem.setMenuComm()
        self.cardAnim = self.widget.getInstByClsName('CardSystem_CardAdvanceAnim')
        self.widget.addChild(self.cardAnim)
        self.cardAnim.visible = False
        self.cardAnim.x = 230
        self.cardAnim.y = 200
        self.widget.cardList.column = 3
        self.widget.cardList.itemHeight = 230
        self.widget.cardList.itemWidth = 168
        self.widget.cardList.itemRenderer = 'CardSystem_CardContainer'
        self.uiAdapter.cardSystem.setAllCardList(filterFunc=self.filterCardFunc)
        cardId = self.uiAdapter.cardSystem.getCurSelCardId()
        self.setRightPanel(cardId)

    def filterCardFunc(self, cardObj):
        if not cardObj:
            return False
        return True

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        self.uiAdapter.cardSystem.setMenuComm()
        self.refreshCardList()
        cardId = self.uiAdapter.cardSystem.getCurSelCardId()
        self.setRightPanel(cardId)

    def refreshCardList(self):
        if not self.hasBaseData():
            return
        self.uiAdapter.cardSystem.setAllCardList(filterFunc=self.filterCardFunc)
        cardId = self.uiAdapter.cardSystem.getCurSelCardId()
        self.setRightPanel(cardId)

    def maxProgressLabelFunc(self, *args):
        return GfxValue(gameStrings.CARD_MAX_DESC)

    def handlePropMenuSel(self, *args):
        pass

    def handleVersionMenuSel(self, *args):
        pass

    def handleTypeMenuSel(self, *args):
        pass

    def onSelectedCard(self, cardItem, inital = False, oldCardId = 0):
        if not cardItem:
            return
        self.setRightPanel(cardItem.cardId, oldCardId=oldCardId)

    def setRightPanel(self, cardId, oldCardId = 0):
        if not self.hasBaseData():
            return
        else:
            p = BigWorld.player()
            cardObj = p.getCard(cardId)
            self.setOpBtn(cardObj, oldCardId)
            if cardObj:
                self.widget.nameTxt.visible = True
                self.widget.clearEnergyMc.visible = True
                self.widget.addDurationMc.visible = True
                self.widget.noneOpMc.visible = True
                self.widget.progressYellow.visible = True
                self.widget.progressBlue.visible = True
                self.widget.consumableMc.visible = True
                self.widget.confirmBtn.visible = True
                baseData = cardObj.getConfigData()
                name = baseData.get('name', '')
                advanceLv = cardObj.advanceLvEx
                self.widget.nameTxt.text = gameStrings.CARD_MAKE_NAME_STR % (name, advanceLv)
                self.widget.consumableMc.itemCount.count = 0
                self.widget.consumableMc.fragmentCount.count = 0
                self.widget.progressBlue.visible = False
                self.widget.progressYellow.visible = False
                progressBar = self.widget.progressYellow if cardObj.isFullAdvance else self.widget.progressBlue
                progressBar.visible = True
                if cardObj.isFullAdvance:
                    progressBar.maxValue = PROGRESS_VALUE
                    progressBar.currentValue = PROGRESS_VALUE
                else:
                    if cardObj.actived:
                        needProgress = cardObj.compoundFragmentCnt(cardObj.advanceLv + 1)
                    else:
                        needProgress = cardObj.compoundFragmentCnt(0)
                    progressBar.maxValue = needProgress
                    progressBar.currentValue = int(cardObj.progress)
                curOpType = self.getCurOpType()
                CARD_SYSTEM_PROP_TYPE_DESC = SCD.data.get('CARD_SYSTEM_PROP_TYPE_DESC', {})
                fragmentName = CARD_SYSTEM_PROP_TYPE_DESC.get(cardObj.propType, '')
                if curOpType == OP_UPGRADE_CARD_PROGRESS:
                    self.widget.addDurationMc.visible = False
                    self.widget.confirmBtn.enabled = True
                    if cardObj.progress < needProgress:
                        self.widget.clearEnergyMc.visible = False
                        self.widget.consumableMc.visible = True
                        self.widget.noneOpMc.visible = False
                        self.widget.consumableMc.titleTxt.text = gameStrings.CARD_MAKE_COST_TITLE_TXT % (fragmentName,)
                        itemId = cardObj.cardItemParentId
                        itemInfo = uiUtils.getGfxItemById(itemId)
                        count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
                        self.widget.consumableMc.itemSlot.numTxt.htmlText = count
                        self.widget.consumableMc.itemSlot.slot.dragable = False
                        self.widget.consumableMc.itemSlot.slot.setItemSlotData(itemInfo)
                        itemId = SCD.data.get('fragmentItemId', {}).get(cardObj.propType, 0)
                        itemInfo = uiUtils.getGfxItemById(itemId)
                        count = p.cardBag.get('fragment', {}).get(cardObj.propType, 0)
                        self.widget.consumableMc.fragmentSlot.numTxt.htmlText = count
                        self.widget.consumableMc.fragmentSlot.slot.dragable = False
                        self.widget.consumableMc.fragmentSlot.slot.setItemSlotData(itemInfo)
                        if cardObj.operatingCard:
                            self.widget.consumableMc.fragmentSlot.visible = False
                            self.widget.consumableMc.fragmentCount.visible = False
                            self.widget.consumableMc.fragmentMax.visible = False
                            self.widget.consumableMc.itemSlot.x = 104
                            self.widget.consumableMc.itemCount.x = 70
                            self.widget.consumableMc.itemMax.x = 152
                        else:
                            self.widget.consumableMc.fragmentSlot.visible = True
                            self.widget.consumableMc.fragmentCount.visible = True
                            self.widget.consumableMc.fragmentMax.visible = True
                            self.widget.consumableMc.itemSlot.x = 38
                            self.widget.consumableMc.itemCount.x = 4
                            self.widget.consumableMc.itemMax.x = 86
                        self.refreshConsumableFragmentInfo()
                    else:
                        self.widget.clearEnergyMc.visible = True
                        self.widget.consumableMc.visible = False
                        self.widget.noneOpMc.visible = False
                        label = ''
                        contentText = ''
                        bossItems = None
                        if cardObj.isCurrentPeriod:
                            bossItems = cardObj.getBossItems()
                        if not cardObj.actived:
                            label = SCD.data.get('CARD_MAKE_COMPOUND_DESC', gameStrings.CARD_MAKE_COMPOUND)
                            contentText = SCD.data.get('CARD_MAKE_COMPOUND_CONTENT', '')
                        elif cardObj.advanceLv < const.CARD_BREAK_RANK:
                            label = SCD.data.get('CARD_MAKE_UPGRADE_DESC', gameStrings.CARD_MAKE_UPGRADE)
                            if bossItems:
                                contentText = SCD.data.get('CARD_MAKE_UPGRADE_CONTENT_EX', '%d') % (cardObj.advanceLv + 1)
                            else:
                                contentText = SCD.data.get('CARD_MAKE_UPGRADE_CONTENT', '%d') % (cardObj.advanceLv + 1)
                        else:
                            rankUpItems = cardObj.getRankUpItems()
                            itemStr = ''
                            itemNum = 0
                            if rankUpItems:
                                itemId, itemNum = rankUpItems[0]
                                itemStr = ID.data.get(itemId, {}).get('name', '')
                                if bossItems:
                                    contentText = SCD.data.get('CARD_DIFF_BREAK_RANK_CONTENT_EX', '%d%d%s%d') % (cardObj.advanceLv + 1,
                                     itemId,
                                     itemStr,
                                     itemNum)
                                else:
                                    contentText = SCD.data.get('CARD_DIFF_BREAK_RANK_CONTENT', '%d%d%s%d') % (cardObj.advanceLv + 1,
                                     itemId,
                                     itemStr,
                                     itemNum)
                            label = SCD.data.get('CARD_DIFF_BREAK_RANK_DESC', gameStrings.CARD_DIFF_BREAK_RANK)
                        self.widget.clearEnergyMc.titleTxt.htmlText = label
                        self.widget.clearEnergyMc.contentTxt.htmlText = contentText
                elif curOpType == OP_DEGRADE_CARD_PROGRESS:
                    self.widget.addDurationMc.visible = False
                    self.widget.confirmBtn.enabled = True
                    self.widget.clearEnergyMc.visible = True
                    self.widget.consumableMc.visible = False
                    self.widget.noneOpMc.visible = False
                    fragmentItemId = SCD.data.get('fragmentItemId', {}).get(cardObj.propType, 0)
                    getFragmentCnt = int(cardObj.progress * cardObj.decomposeFragmentCnt(cardObj.advanceLv + 1) * 1.0 / const.CARD_DECOMPOSE_MUL)
                    self.widget.clearEnergyMc.titleTxt.htmlText = SCD.data.get('CARD_MAKE_DEGRADE_TYPE_PROGRESS_DESC', gameStrings.CARD_MAKE_DEGRADE_TYPE_PROGRESS)
                    self.widget.clearEnergyMc.contentTxt.htmlText = SCD.data.get('CARD_MAKE_DEGRADE_TYPE_PROGRESS_CONTENT', '%d%d%d%s') % (cardObj.advanceLv,
                     getFragmentCnt,
                     fragmentItemId,
                     fragmentName)
                elif curOpType == OP_DEGRADE_CARD_DECOMPOSE:
                    self.widget.addDurationMc.visible = False
                    self.widget.confirmBtn.enabled = True
                    self.widget.clearEnergyMc.visible = True
                    self.widget.consumableMc.visible = False
                    self.widget.noneOpMc.visible = False
                    deType = 0
                    if cardObj.actived and cardObj.advanceLvEx > 0:
                        deType = const.CARD_DEGRADE_TYPE_RANK
                    if cardObj.actived and cardObj.advanceLvEx == 0 and cardObj.progress == 0:
                        deType = const.CARD_DEGRADE_TYPE_DECOMPOSE
                    getFragmentCnt = 0
                    label = ''
                    contentText = ''
                    fragmentItemId = SCD.data.get('fragmentItemId', {}).get(cardObj.propType, 0)
                    if deType == const.CARD_DEGRADE_TYPE_RANK:
                        getFragmentCnt = int(cardObj.progress * cardObj.decomposeFragmentCnt(cardObj.advanceLv + 1) * 1.0 / const.CARD_DECOMPOSE_MUL)
                        getFragmentCnt += int(cardObj.compoundFragmentCnt(cardObj.advanceLv) * cardObj.decomposeFragmentCnt(cardObj.advanceLv) * 1.0 / const.CARD_DECOMPOSE_MUL)
                        label = SCD.data.get('CARD_MAKE_DEGRADE_DESC', gameStrings.CARD_MAKE_DECOMPOSE)
                        returnItems = []
                        if cardObj.isCurrentPeriod:
                            items = cardObj.getBossItems(cardObj.advanceLv - 1)
                            for itemId, itemNum in items:
                                retNum = int(round(itemNum * cardObj.bossItemRetRate))
                                if retNum > 0:
                                    returnItems.append((itemId, retNum))

                        if returnItems:
                            itemId, itemNum = returnItems[0]
                            contentText = SCD.data.get('CARD_MAKE_DEGRADE_CONTENT_EX', '%d%d%d%s%d%s') % (cardObj.advanceLv - 1,
                             getFragmentCnt,
                             fragmentItemId,
                             fragmentName,
                             itemNum,
                             fragmentName)
                        else:
                            contentText = SCD.data.get('CARD_MAKE_DEGRADE_CONTENT', '%d%d%d%s') % (cardObj.advanceLv - 1,
                             getFragmentCnt,
                             fragmentItemId,
                             fragmentName)
                    elif deType == const.CARD_DEGRADE_TYPE_DECOMPOSE:
                        getFragmentCnt = int(cardObj.compoundFragmentCnt(0) * cardObj.decomposeFragmentCnt(0) * 1.0 / const.CARD_DECOMPOSE_MUL)
                        label = SCD.data.get('CARD_MAKE_DECOMPOSE_DESC', gameStrings.CARD_MAKE_DECOMPOSE)
                        contentText = SCD.data.get('CARD_MAKE_DECOMPOSE_CONTENT', '%d%d%s') % (getFragmentCnt, fragmentItemId, fragmentName)
                    self.widget.clearEnergyMc.titleTxt.htmlText = label
                    self.widget.clearEnergyMc.contentTxt.htmlText = contentText
                elif curOpType == OP_CARD_RENEWAL:
                    self.widget.addDurationMc.visible = True
                    self.widget.confirmBtn.enabled = True
                    self.widget.clearEnergyMc.visible = False
                    self.widget.consumableMc.visible = False
                    self.widget.noneOpMc.visible = False
                    self.refreshAddDurationInfo(True)
                else:
                    self.widget.confirmBtn.enabled = False
                    self.widget.clearEnergyMc.visible = False
                    self.widget.consumableMc.visible = False
                    self.widget.addDurationMc.visible = False
                    self.widget.noneOpMc.visible = True
                    cardCollectorEdition = SCD.data.get('cardCollectorsEdition', ())
                    if cardObj.version in cardCollectorEdition:
                        self.widget.noneOpMc.titleTxt.text = gameStrings.CARD_MAKE_CARD_COLLECTOR_NONE_OP_TXT
                    else:
                        self.widget.noneOpMc.titleTxt.text = gameStrings.CARD_MAKE_CARD_LEVEL_LIMIT_OP_TXT
            else:
                self.widget.nameTxt.visible = False
                self.widget.clearEnergyMc.visible = False
                self.widget.addDurationMc.visible = False
                self.widget.noneOpMc.visible = False
                self.widget.progressYellow.visible = False
                self.widget.progressBlue.visible = False
                self.widget.consumableMc.visible = False
                self.widget.confirmBtn.visible = False
            self.widget.fragmentCountTxt0.text = p.cardBag.get('fragment', {}).get(const.CARD_PROP_TYPE_PVE, 0)
            self.widget.fragmentCountTxt1.text = p.cardBag.get('fragment', {}).get(const.CARD_PROP_TYPE_PVP, 0)
            return

    def setOpBtn(self, cardObj, oldCardId = 0):
        if not self.hasBaseData():
            return
        elif not cardObj:
            self.widget.compoundRadioBtn.visible = False
            self.widget.resetEnergyRadioBtn.visible = False
            self.widget.lowerRadioBtn.visible = False
            self.widget.tipIcon.visible = False
            return
        else:
            self.widget.compoundRadioBtn.visible = True
            self.widget.resetEnergyRadioBtn.visible = True
            self.widget.lowerRadioBtn.visible = True
            self.widget.tipIcon.visible = True
            p = BigWorld.player()
            enabled = False
            label = ''
            tip = ''
            needProgress = 0
            if cardObj.actived:
                needProgress = cardObj.compoundFragmentCnt(cardObj.advanceLv + 1)
            else:
                needProgress = cardObj.compoundFragmentCnt(0)
            if cardObj.progress < needProgress:
                label = gameStrings.CARD_MAKE_ADD_TYPE_PROGRESS
                result0 = cardObj.checkUpgradeProgress(1, 0)
                result1 = cardObj.checkUpgradeProgress(0, 1)
                if not result0 and not result1:
                    tip = uiUtils.getTextFromGMD(result0.param[0])
                enabled = bool(result0) or bool(result1)
                needRoleLv = cardObj.getNeedRoleLv(cardObj.advanceLv + 1)
                needRoleLv -= p.cardBag.get('specialProp', {}).get('reduceAdvanceLevel', {}).get(cardObj.id, 0)
                if p.lv < needRoleLv:
                    enabled = False
                    tip = uiUtils.getTextFromGMD(GMDD.data.CARD_PROGRESS_LACK_ROLE_LEVEL)
                    tip = tip % (needRoleLv,)
            else:
                if not cardObj.actived:
                    label = SCD.data.get('CARD_MAKE_COMPOUND_DESC', gameStrings.CARD_MAKE_COMPOUND)
                elif cardObj.advanceLvEx < const.CARD_BREAK_RANK:
                    label = SCD.data.get('CARD_MAKE_UPGRADE_DESC', gameStrings.CARD_MAKE_UPGRADE)
                else:
                    label = SCD.data.get('CARD_DIFF_BREAK_RANK_DESC', gameStrings.CARD_DIFF_BREAK_RANK)
                if not cardObj.actived:
                    result = cardObj.checkCompose()
                    if not result:
                        tip = uiUtils.getTextFromGMD(result.param[0])
                    enabled = bool(result)
                else:
                    result = cardObj.checkAdvance()
                    if not result:
                        tip = uiUtils.getTextFromGMD(result.param[0])
                    advanceLvValid, advanceLvMsg = self.uiAdapter.cardSystem.checkCardCanAdvance(cardObj=cardObj, advanceLv=True)
                    if not advanceLvValid:
                        tip = advanceLvMsg
                    enabled = bool(result)
                    if enabled and cardObj.isBreakRank:
                        enabled = advanceLvValid
                needRoleLv = cardObj.getNeedRoleLv(cardObj.advanceLv + 1)
                needRoleLv -= p.cardBag.get('specialProp', {}).get('reduceAdvanceLevel', {}).get(cardObj.id, 0)
                if p.lv < needRoleLv:
                    enabled = False
                    tip = uiUtils.getTextFromGMD(GMDD.data.CARD_ADVANCE_LACK_ROLE_LEVEL)
                    tip = tip % (needRoleLv,)
            self.widget.compoundRadioBtn.enabled = enabled
            self.widget.compoundRadioBtn.label = label
            self.widget.compoundRadioBtn.validateNow()
            if tip:
                self.widget.compoundRadioBtn.mouseEnabled = True
                TipManager.addTip(self.widget.compoundRadioBtn, tip)
            else:
                TipManager.removeTip(self.widget.compoundRadioBtn)
            bItems = cardObj.getBossItems()
            bItems = bItems if bItems else ()
            rItems = cardObj.getRankUpItems()
            rItems = rItems if rItems else ()
            tipIconTip = ''
            if bItems and not rItems:
                tipIconTip = SCD.data.get('CARD_UPGRADE_ITEM_TIP1')
            elif not bItems and rItems:
                tipIconTip = SCD.data.get('CARD_UPGRADE_ITEM_TIP2')
            elif bItems and rItems:
                tipIconTip = SCD.data.get('CARD_UPGRADE_ITEM_TIP3')
            needItems = bItems + rItems
            if needItems:
                self.widget.tipIcon.visible = True
                self.widget.tipIcon.x = self.widget.compoundRadioBtn.x + self.widget.compoundRadioBtn.textField.textWidth + 30
            else:
                self.widget.tipIcon.visible = False
            needItemTxt = ''
            for i, (itemId, num) in enumerate(needItems):
                itemName = ID.data.get(itemId, {}).get('name', '')
                needItemTxt += gameStrings.CARD_ITEM_NUM_STR % (itemName, num)
                if i < len(needItems) - 1:
                    needItemTxt += gameStrings.CARD_STR_CONNECT_POINT

            if needItemTxt:
                tipIconTip = tipIconTip % (needItemTxt,)
                TipManager.addTip(self.widget.tipIcon, tipIconTip)
            enabled = False
            label = ''
            tip = ''
            if cardObj.noDecProgress and cardObj.canRenewal:
                label = SCD.data.get('CARD_MAKE_RENEWAL', gameStrings.CARD_MAKE_RENEWAL)
                result = cardObj.checkCanAddDuration()
                if not result:
                    tip = uiUtils.getTextFromGMD(result.param[0])
                enabled = bool(result)
                self.widget.resetEnergyRadioBtn.data = OP_CARD_RENEWAL
            else:
                if cardObj.actived:
                    label = SCD.data.get('CARD_MAKE_DEGRADE_TYPE_PROGRESS_DESC', gameStrings.CARD_MAKE_DEGRADE_TYPE_PROGRESS)
                    result = cardObj.checkDegradeProgress(const.CARD_DEGRADE_TYPE_PROGRESS)
                    if not result:
                        tip = uiUtils.getTextFromGMD(result.param[0])
                    enabled = bool(result)
                else:
                    enabled = False
                    label = SCD.data.get('CARD_MAKE_DEGRADE_TYPE_PROGRESS_DESC', gameStrings.CARD_MAKE_DEGRADE_TYPE_PROGRESS)
                    tip = uiUtils.getTextFromGMD(GMDD.data.CARD_NON_COMPOUND)
                self.widget.resetEnergyRadioBtn.data = OP_DEGRADE_CARD_PROGRESS
            self.widget.resetEnergyRadioBtn.enabled = enabled
            self.widget.resetEnergyRadioBtn.label = label
            if tip:
                self.widget.resetEnergyRadioBtn.mouseEnabled = True
                TipManager.addTip(self.widget.resetEnergyRadioBtn, tip)
            else:
                TipManager.removeTip(self.widget.resetEnergyRadioBtn)
            enabled = False
            label = ''
            tip = ''
            if cardObj.actived:
                if cardObj.advanceLvEx > 0:
                    label = SCD.data.get('CARD_MAKE_DEGRADE_DESC', gameStrings.CARD_MAKE_DEGRADE)
                    result = cardObj.checkDegradeProgress(const.CARD_DEGRADE_TYPE_RANK)
                    if not result:
                        tip = uiUtils.getTextFromGMD(result.param[0])
                    enabled = bool(result)
                else:
                    label = SCD.data.get('CARD_MAKE_DECOMPOSE_DESC', gameStrings.CARD_MAKE_DECOMPOSE)
                    result = cardObj.checkDecompose()
                    if not result:
                        tip = uiUtils.getTextFromGMD(result.param[0])
                    enabled = bool(result)
            else:
                enabled = False
                label = SCD.data.get('CARD_MAKE_DECOMPOSE_DESC', gameStrings.CARD_MAKE_DECOMPOSE)
                tip = uiUtils.getTextFromGMD(GMDD.data.CARD_NON_COMPOUND)
            self.widget.lowerRadioBtn.enabled = enabled
            self.widget.lowerRadioBtn.label = label
            if tip:
                self.widget.lowerRadioBtn.mouseEnabled = True
                TipManager.addTip(self.widget.lowerRadioBtn, tip)
            else:
                TipManager.removeTip(self.widget.lowerRadioBtn)
            if self.widget.compoundRadioBtn.group.selectedButton and not self.widget.compoundRadioBtn.group.selectedButton.enabled:
                self.widget.compoundRadioBtn.group.selectedButton.selected = False
                self.widget.compoundRadioBtn.group.selectedButton = None
            if not self.widget.compoundRadioBtn.group.selectedButton or not self.widget.compoundRadioBtn.group.selectedButton.enabled or cardObj.id != oldCardId and oldCardId:
                radioBtnList = [self.widget.compoundRadioBtn, self.widget.resetEnergyRadioBtn, self.widget.lowerRadioBtn]
                for btn in radioBtnList:
                    if btn.enabled:
                        btn.selected = True
                        break

            return

    def getCurOpType(self):
        if not self.hasBaseData():
            return 0
        elif self.widget.compoundRadioBtn.group.selectedButton:
            return self.widget.compoundRadioBtn.group.selectedButton.data
        else:
            return None

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def handleOpBtnSelected(self, *arg):
        if not self.hasBaseData():
            return
        cardId = self.uiAdapter.cardSystem.getCurSelCardId()
        self.setRightPanel(cardId)

    @ui.checkInventoryLock()
    def handleConfirmBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        else:
            p = BigWorld.player()
            opType = self.getCurOpType()
            cardId = self.uiAdapter.cardSystem.getCurSelCardId()
            cardObj = p.getCard(cardId)
            cipher = p.cipherOfPerson
            deType = 0
            if opType == OP_UPGRADE_CARD_PROGRESS:
                if cardObj.actived:
                    needProgress = cardObj.compoundFragmentCnt(cardObj.advanceLv + 1)
                else:
                    needProgress = cardObj.compoundFragmentCnt(0)
                if cardObj.progress < needProgress:
                    itemNum = self.widget.consumableMc.itemCount.count
                    fragmentCnt = self.widget.consumableMc.fragmentCount.count
                    itemEnergy = itemNum * cardObj.fagmentCntValue
                    fragmentEnergy = const.CARD_FRAGMENT_LINGLI_RATE * fragmentCnt
                    energyNum = itemEnergy + fragmentEnergy
                    _msg = None
                    isShowCheckBox = False
                    checkOnceType = None
                    if cardObj.progress + energyNum > needProgress:
                        _msg = gameStrings.CARD_MAKE_UPGRADE_PROGRESS_OVERFLOW
                    if cardObj.noDecomposeLv:
                        if not self.uiAdapter.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_CARD_UPGRADE_PROGRESS_NODECOMPOSELV):
                            _msg = gameStrings.CARD_UPGRADE_PROGRESS_NODECOMPOSELV_MSG
                            isShowCheckBox = True
                            checkOnceType = uiConst.CHECK_ONCE_TYPE_CARD_UPGRADE_PROGRESS_NODECOMPOSELV
                        if cardObj.advanceLvEx >= const.CARD_BREAK_RANK:
                            if not self.uiAdapter.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_CARD_UPGRADE_PROGRESS_BREAK_RANK_NODECOMPOSELV):
                                _msg = gameStrings.CHECK_ONCE_TYPE_CARD_UPGRADE_PROGRESS_BREAK_RANK_NODECOMPOSELV
                                isShowCheckBox = True
                                checkOnceType = uiConst.CHECK_ONCE_TYPE_CARD_UPGRADE_PROGRESS_BREAK_RANK_NODECOMPOSELV
                    if not _msg:

                        def upFunc():
                            p.base.upgradeCardProgress(cardId, cipher, fragmentCnt, itemNum)

                    else:

                        def upFunc():
                            self.uiAdapter.messageBox.showYesNoMsgBox(_msg, yesCallback=Functor(p.base.upgradeCardProgress, cardId, cipher, fragmentCnt, itemNum), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, isShowCheckBox=isShowCheckBox, checkOnceType=checkOnceType)

                    upgradeCardProgressFunc = upFunc
                    advanceLvValid, advanceLvMsg = self.uiAdapter.cardSystem.checkCardCanAdvance(cardObj=cardObj, advanceLv=False)
                    if not advanceLvValid and not self.uiAdapter.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_CARD_UPGRADE_PROGRESS_NOT_BY_SERVER_PROGRESS):
                        self.uiAdapter.messageBox.showYesNoMsgBox(advanceLvMsg, yesCallback=upgradeCardProgressFunc, yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_CARD_UPGRADE_PROGRESS_NOT_BY_SERVER_PROGRESS)
                    else:
                        upgradeCardProgressFunc()
                else:
                    self._advanceCard()
            elif opType == OP_DEGRADE_CARD_PROGRESS:
                deType = const.CARD_DEGRADE_TYPE_PROGRESS
                getFragmentCnt = int(cardObj.progress * cardObj.decomposeFragmentCnt(cardObj.advanceLv + 1) * 1.0 / const.CARD_DECOMPOSE_MUL)
                label = SCD.data.get('CARD_MAKE_DEGRADE_TYPE_PROGRESS_DESC', gameStrings.CARD_MAKE_DEGRADE_TYPE_PROGRESS)
                CARD_SYSTEM_PROP_TYPE_DESC = SCD.data.get('CARD_SYSTEM_PROP_TYPE_DESC', {})
                fragmentName = CARD_SYSTEM_PROP_TYPE_DESC.get(cardObj.propType, '')
                _msg = ''.join((label, '\n', gameStrings.CARD_MAKE_FRAGMENT_ADD % (fragmentName, getFragmentCnt)))
                self.uiAdapter.messageBox.showYesNoMsgBox(_msg, yesCallback=Functor(p.base.degradeCardProgress, cardId, deType, cipher), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)
            elif opType == OP_DEGRADE_CARD_DECOMPOSE:
                deType = 0
                _msg = ''
                if cardObj.actived and cardObj.advanceLvEx > 0:
                    deType = const.CARD_DEGRADE_TYPE_RANK
                if cardObj.actived and cardObj.advanceLvEx == 0 and cardObj.progress == 0:
                    deType = const.CARD_DEGRADE_TYPE_DECOMPOSE
                getFragmentCnt = 0
                if deType == const.CARD_DEGRADE_TYPE_RANK:
                    self.uiAdapter.cardDiffConfirm.show(cardId, uiConst.CARD_DIFF_TYPE_DEGRADE, Functor(p.base.degradeCardProgress, cardId, deType, cipher))
                    return
                if deType == const.CARD_DEGRADE_TYPE_DECOMPOSE:
                    self.uiAdapter.cardDiffConfirm.show(cardId, uiConst.CARD_DIFF_TYPE_DEGRADE, Functor(p.base.degradeCardProgress, cardId, deType, cipher))
                    return
                if not _msg:
                    decomposeDesc = SCD.data.get('CARD_MAKE_DECOMPOSE_DESC', gameStrings.CARD_MAKE_DECOMPOSE)
                    _msg = ''.join((decomposeDesc, '\n', gameStrings.CARD_MAKE_FRAGMENT_ADD % (getFragmentCnt,)))
                self.uiAdapter.messageBox.showYesNoMsgBox(_msg, yesCallback=Functor(p.base.degradeCardProgress, cardId, deType, cipher), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)
            elif opType == OP_CARD_RENEWAL:
                itemIds = []
                itemNums = []
                durationDay = 0
                for i in xrange(CONSUMABLE_NUM_MAX):
                    consumableMc = getattr(self.widget.addDurationMc.canvas, 'consumableMc' + str(i), None)
                    if consumableMc:
                        count = consumableMc.itemCount.count
                        itemId = consumableMc.itemId
                        if count:
                            itemIds.append(itemId)
                            itemNums.append(count)
                        data = CID.data.get(itemId)
                        duration = data.get('addCardDuration', 0)
                        day = duration / const.SECONDS_PER_DAY
                        durationDay += day * consumableMc.itemCount.count

                if itemIds and itemNums:
                    validCardList = []
                    for _cardId, itemData in BCD.data.iteritems():
                        cardObj = p.getCard(_cardId)
                        cardData = cardObj.getConfigData()
                        cardAdvanceData = cardObj.getAdvanceData()
                        if not cardObj.canRenewal:
                            continue
                        if not cardObj.isValidCard():
                            continue
                        if _cardId == cardId:
                            continue
                        if not cardObj.actived:
                            continue
                        validCardList.append(_cardId)

                    if len(validCardList) >= const.CARD_MAX_RENEWAL_EFFECT_NUM:
                        self.uiAdapter.cardRenewalDetail.show(cardId, validCardList, durationDay, itemIds, itemNums)
                    else:
                        self.uiAdapter.cardRenewalSimple.show(cardId, durationDay, itemIds, itemNums)
            return

    def handleCompoundBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        self._advanceCard()

    def handleBreakBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        self._advanceCard()

    @ui.checkInventoryLock()
    def _advanceCard(self):
        if not self.hasBaseData():
            return
        cardId = self.uiAdapter.cardSystem.getCurSelCardId()
        p = BigWorld.player()
        cipher = p.cipherOfPerson
        cardObj = p.getCard(cardId)

        def _func(itemCount = self.widget.consumableMc.itemCount.count, fragmentCount = self.widget.consumableMc.fragmentCount.count):
            if cardObj.actived:
                needProgress = 0
                if cardObj.actived:
                    needProgress = cardObj.compoundFragmentCnt(cardObj.advanceLv + 1)
                else:
                    needProgress = cardObj.compoundFragmentCnt(0)
                needProgress -= cardObj.progress
                itemEnergy = itemCount * cardObj.fagmentCntValue
                fragmentEnergy = const.CARD_FRAGMENT_LINGLI_RATE * fragmentCount
                energyNum = itemEnergy + fragmentEnergy
                if cardObj.advanceLv == const.CARD_MAX_RANK - 1 and energyNum + cardObj.progress > needProgress:
                    _msg = gameStrings.CARD_MAKE_UPGRADE_CARD_MORE_PROGRESS
                    self.uiAdapter.messageBox.showYesNoMsgBox(_msg, yesCallback=Functor(p.base.advanceCard, cardId, cipher), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL)
                    return
                p.base.advanceCard(cardId, cipher)
            else:
                p.base.compoundCard(cardId, cipher, 0, const.CARD_COMPOUND_TYPE_MAKE)

        self.uiAdapter.cardDiffConfirm.show(cardId, uiConst.CARD_DIFF_TYPE_UPGRADE, _func)

    def handleDurationCountChange(self, *arg):
        if not self.hasBaseData():
            return
        self.refreshAddDurationInfo()

    def refreshAddDurationInfo(self, resetItemSlot = False):
        if not self.hasBaseData():
            return
        else:
            cardId = self.uiAdapter.cardSystem.getCurSelCardId()
            p = BigWorld.player()
            cardObj = p.getCard(cardId)
            if resetItemSlot:
                self.widget.removeAllInst(self.widget.addDurationMc.canvas)
                renewalItems = cardObj.renewalItems
                for i, itemId in enumerate(renewalItems):
                    consumableMc = self.widget.getInstByClsName('CardMake_ConsumableItemMc')
                    if consumableMc:
                        itemInfo = uiUtils.getGfxItemById(itemId)
                        consumableMc.itemSlot.slot.setItemSlotData(itemInfo)
                        consumableMc.itemSlot.slot.dragable = False
                        consumableMc.itemId = itemId
                        consumableMc.itemCount.minCount = 0
                        consumableMc.itemCount.count = 0
                        consumableMc.itemCount.addEventListener(events.EVENT_COUNT_CHANGE, self.handleDurationCountChange, False, 0, True)
                        consumableMc.itemMax.addEventListener(events.BUTTON_CLICK, self._onDurationItemMaxClick, False, 0, True)
                        consumableMc.name = 'consumableMc' + str(i)
                        if len(renewalItems) == 1:
                            consumableMc.x = 66
                        else:
                            consumableMc.x = 4 + i * 132
                    self.widget.addDurationMc.canvas.addChild(consumableMc)

            durationDay = 0
            for i in xrange(CONSUMABLE_NUM_MAX):
                consumableMc = getattr(self.widget.addDurationMc.canvas, 'consumableMc' + str(i), None)
                if consumableMc:
                    itemId = consumableMc.itemId
                    count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
                    consumableMc.itemSlot.numTxt.text = count
                    consumableMc.itemCount.maxCount = count
                    data = CID.data.get(itemId)
                    duration = data.get('addCardDuration', 0)
                    day = duration / const.SECONDS_PER_DAY
                    durationDay += day * consumableMc.itemCount.count

            self.widget.addDurationMc.preDurationTxt.text = gameStrings.CARD_ADD_DURATION_TIME_TXT % (durationDay,)
            return

    def handleCountChange(self, *arg):
        if not self.hasBaseData():
            return
        self.refreshConsumableFragmentInfo()

    def refreshConsumableFragmentInfo(self):
        if not self.hasBaseData():
            return
        cardId = self.uiAdapter.cardSystem.getCurSelCardId()
        p = BigWorld.player()
        cardObj = p.getCard(cardId)
        itemId = cardObj.cardItemParentId
        count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
        needProgress = 0
        if cardObj.actived:
            needProgress = cardObj.compoundFragmentCnt(cardObj.advanceLv + 1)
        else:
            needProgress = cardObj.compoundFragmentCnt(0)
        needProgress -= cardObj.progress
        itemEnergy = self.widget.consumableMc.itemCount.count * cardObj.fagmentCntValue
        fragmentEnergy = const.CARD_FRAGMENT_LINGLI_RATE * self.widget.consumableMc.fragmentCount.count
        energyNum = itemEnergy + fragmentEnergy
        self.widget.consumableMc.preEnergyTxt.text = gameStrings.CARD_MAKE_PRE_ENERGY % (energyNum,)
        itemMaxCount = max(math.ceil((needProgress - fragmentEnergy) * 1.0 / cardObj.fagmentCntValue), 0)
        fragmentMaxCount = max(math.ceil((needProgress - itemEnergy) * 1.0 / const.CARD_FRAGMENT_LINGLI_RATE), 0)
        self.widget.consumableMc.itemCount.maxCount = min(count, itemMaxCount)
        self.widget.consumableMc.fragmentCount.maxCount = min(p.cardBag.get('fragment', {}).get(cardObj.propType), fragmentMaxCount)

    def showCardAnim(self, preCardObj, sufCardObj):
        if not self.hasBaseData():
            return
        if not preCardObj:
            return
        if not sufCardObj:
            return
        if not self.cardAnim:
            return
        self.cancelAnimCallBack()
        self.cardAnim.visible = True
        self.cardAnim.alpha = 1
        self.cardAnim.gotoAndPlay(0)
        self.uiAdapter.cardSystem.setCardMc(self.cardAnim.normalCardAnim.normalCard.card, preCardObj)
        self.uiAdapter.cardSystem.setCardMc(self.cardAnim.goldCard, sufCardObj)
        self.flashCardAnimCB = ASUtils.callbackAtFrame(self.cardAnim, 45, self.flashCardAnimCallBack)
        gameglobal.rds.sound.playSound(6189)

    def flashCardAnimCallBack(self, *arg):
        if not self.hasBaseData():
            return

        def _animCallBack():
            Tweener.addTween(self.cardAnim, {'alpha': 0,
             'time': 0.5,
             'transition': 'easeinsine',
             'onComplete': self.cardDisappearCompleted})

        self.animCB = BigWorld.callback(0.5, _animCallBack)

    def cardDisappearCompleted(self, *arg):
        if not self.hasBaseData():
            return
        self.cardAnim.visible = False

    def cancelAnimCallBack(self):
        if self.flashCardAnimCB:
            ASUtils.cancelCallBack(self.flashCardAnimCB)
            self.flashCardAnimCB = None
        if self.animCB:
            BigWorld.cancelCallback(self.animCB)
            self.animCB = None
        if self.cardAnim:
            Tweener.removeTweens(self.cardAnim)
        if self.cardAnim:
            self.cardAnim.visible = False

    def _onItemMaxClick(self, *arg):
        if not self.hasBaseData():
            return
        self.widget.consumableMc.itemCount.count = self.widget.consumableMc.itemCount.maxCount

    def _onDurationItemMaxClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        if t:
            p = BigWorld.player()
            itemId = t.parent.itemId
            t.parent.itemCount.count = t.parent.itemCount.maxCount

    def _onFragmentMaxClick(self, *arg):
        if not self.hasBaseData():
            return
        self.widget.consumableMc.fragmentCount.count = self.widget.consumableMc.fragmentCount.maxCount
