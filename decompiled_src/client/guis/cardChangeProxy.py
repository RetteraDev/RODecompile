#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardChangeProxy.o
import math
import BigWorld
import gameglobal
import gametypes
import events
import uiUtils
import uiConst
import utils
import const
import ui
import gameconfigCommon
from asObject import ASObject
from asObject import ASUtils
from asObject import TipManager
from gamestrings import gameStrings
from callbackHelper import Functor
from uiProxy import UIProxy
from data import item_data as ID
from data import prop_ref_data as PRD
from data import prop_data as PD
from data import sys_config_data as SCD
from data import conditional_prop_data as CPD
from data import card_wash_group_data as CWGD
from data import equip_enhance_item_config_data as EEICD
from cdata import game_msg_def_data as GMDD
from cdata import pskill_template_data as PTD
from cdata import pskill_data as PDD
TEMP_ICON = 'summonedSprite/icon/1014.dds'
CARD_CHANGE_WASH_TYPE = 1
CARD_CHANGE_REMOVE_TYPE = 2
CARD_CHANGE_WASH_TYPE_FRAGMENT = 1
CARD_CHANGE_WASH_TYPE_WASHPOINT = 2
CARD_CHANGE_WASH_TYPE_TIANBI = 3
CARD_CHANGE_REMOVE_TYPE_ITEM = 1
CARD_CHANGE_REMOVE_TYPE_FRAGMENT = 2
CARD_BTN_SLOT_1 = 1
CARD_BTN_SLOT_2 = 2
CARD_BTN_SLOT_QUMO = 3
CARD_BTN_SLOT_DISHE = 4
PROP_ITEM_OFFSET_Y = 25
LEFT_DOWN_PROP_ITEM_OFFSET_Y = 22
NUM_ENOUGH_COLOR = '#ffc961'
CARD_SLOT_TYPE_1 = 1
CARD_SLOT_TYPE_2 = 2
CARD_PROP_TYPE_1 = 1
CARD_PROP_TYPE_2 = 2
NEWPROP_REMAIN_RADIO = 1.2
BONUS_TYPE_DICT = {1: 'huanjiannulin',
 2: 'huanjiandishe'}
WASHPROP_NUM_PERCENT_ADD = 5
TAB_INDEX_CARD_CHANGE = 3

class CardChangeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardChangeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.showCardCd = True
        self.reset()

    @property
    def tempId(self):
        return self.uiAdapter.cardSystem.tempId

    @property
    def cardBag(self):
        p = BigWorld.player()
        cardBag = p.allCardBags.get(self.tempId, {})
        return cardBag

    def reset(self):
        self.updateTimeCB = None
        self.isSpecialChange = False
        self.specialChangeInfo = {}

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()
        self.cancelCdTimeCallBack()

    def initUI(self):
        self.widget.washTabBtn.groupName = 'tabBtn'
        self.widget.removeTabBtn.groupName = 'tabBtn'
        self.widget.washTabBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.removeTabBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.washTabBtn.selected = True
        self.widget.propTabMc.tab0.groupName = 'propTabBtn'
        self.widget.propTabMc.tab1.groupName = 'propTabBtn'
        self.widget.propTabMc.tab0.addEventListener(events.BUTTON_CLICK, self.handlePropTabBtnClick, False, 0, True)
        self.widget.propTabMc.tab1.addEventListener(events.BUTTON_CLICK, self.handlePropTabBtnClick, False, 0, True)
        self.widget.propTabMc.tab0.selected = True
        for i in xrange(0, 10):
            cardBtn = getattr(self.widget.tabMc, 'cardBtn' + str(i), None)
            if cardBtn:
                cardBtn.groupName = 'cardBtn'
                cardBtn.addEventListener(events.BUTTON_CLICK, self.handleCardBtnClick, False, 0, True)

        self.widget.tabMc.cardBtn0.selected = True
        self.widget.washBtn.addEventListener(events.BUTTON_CLICK, self.handleWashBtnClick, False, 0, True)
        self.widget.oldWashBtn.addEventListener(events.BUTTON_CLICK, self.handleOldWashBtnClick, False, 0, True)
        self.widget.newWashBtn.addEventListener(events.BUTTON_CLICK, self.handleNewWashBtnClick, False, 0, True)
        self.widget.takeEffectBtn.addEventListener(events.BUTTON_CLICK, self.handleTakeEffectBtnClick, False, 0, True)
        self.widget.helpIcon.visible = False
        self.widget.lackMaterialCheckBox.visible = False
        self.widget.lackMaterialCheckBox.selected = False
        self.widget.lackMaterialCheckBox.addEventListener(events.EVENT_SELECT, self.handleLackMaterialCheckBoxClick, False, 0, True)
        self.widget.washComsumableMc.selFragmentBtn.groupName = 'washComsumableMc'
        self.widget.washComsumableMc.selWashPointBtn.groupName = 'washComsumableMc'
        self.widget.washComsumableMc.tianbiBtn.groupName = 'washComsumableMc'
        self.widget.washComsumableMc.selFragmentBtn.addEventListener(events.BUTTON_CLICK, self.handleWashSubTypeBtnClick, False, 0, True)
        self.widget.washComsumableMc.selWashPointBtn.addEventListener(events.BUTTON_CLICK, self.handleWashSubTypeBtnClick, False, 0, True)
        self.widget.washComsumableMc.tianbiBtn.addEventListener(events.BUTTON_CLICK, self.handleWashSubTypeBtnClick, False, 0, True)
        self.widget.washComsumableMc.selWashPointBtn.selected = True
        self.widget.washComsumableMc.pointDesc.moneyIcon.bonusType = 'fame'
        self.widget.removeComsumableMc.itemBtn.groupName = 'removeComsumableMc'
        self.widget.removeComsumableMc.fragmentBtn.groupName = 'removeComsumableMc'
        self.widget.removeComsumableMc.itemBtn.addEventListener(events.BUTTON_CLICK, self.handleRemoveSubTypeBtnClick, False, 0, True)
        self.widget.removeComsumableMc.fragmentBtn.addEventListener(events.BUTTON_CLICK, self.handleRemoveSubTypeBtnClick, False, 0, True)
        self.widget.removeComsumableMc.itemBtn.selected = True
        self.widget.removeTabBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.uiAdapter.cardSystem.setMenuComm()
        self.widget.cardList.column = 3
        self.widget.cardList.itemHeight = 180
        self.widget.cardList.itemWidth = 130
        self.widget.cardList.itemRenderer = 'CardSystem_CardContainer'
        self.uiAdapter.cardSystem.setAllCardList(filterFunc=self.filterCardFunc)
        self.refreshLeftDetailMc()
        self.refreshCdTime()
        self.refreshRightInfo()
        self.refreshNoCardDesc()
        BigWorld.callback(0.1, self.setWashFilter)

    def setWashFilter(self):
        if self.isSpecialChange:
            washNumId = self.specialChangeInfo.get('washNumId', 0)
            self.uiAdapter.cardSystem.setWashNumIdFilter([washNumId])

    def filterCardFunc(self, cardObj):
        if not cardObj:
            return False
        if cardObj.noFixToSlot:
            return False
        cardType = self.getCardBtnType()
        if not cardObj.slot:
            if cardType == CARD_BTN_SLOT_QUMO:
                if cardObj.propType == CARD_PROP_TYPE_1:
                    return True
            elif cardType == CARD_BTN_SLOT_DISHE:
                if cardObj.propType == CARD_PROP_TYPE_2:
                    return True
        else:
            for slotId in cardObj.slot:
                sType, slotIndex = self.uiAdapter.cardSystem.parseSlotId(slotId)
                if cardType == CARD_BTN_SLOT_1:
                    if sType == CARD_SLOT_TYPE_1:
                        return True
                elif cardType == CARD_BTN_SLOT_2:
                    if sType == CARD_SLOT_TYPE_2:
                        return True

        return False

    def getCardBtnType(self):
        return int(self.widget.tabMc.cardBtn0.group.selectedButton.data)

    def onSelectedCard(self, cardItem, inital = False, oldCardId = 0):
        if not self.hasBaseData():
            return
        self.widget.propTabMc.tab0.slected = True
        self.refreshLeftDetailMc()
        self.refreshRightInfo()
        self.refreshNoCardDesc()

    def handleVersionMenuSel(self, *args):
        pass

    def handleTypeMenuSel(self, *args):
        pass

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        self.refreshCardList()
        self.refreshLeftDetailMc()
        self.refreshCdTime()
        self.refreshRightInfo()
        self.refreshNoCardDesc()

    def refreshNoCardDesc(self):
        p = BigWorld.player()
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
        cardObj = p.getCard(selCardId)
        if cardObj:
            self.widget.leftTopNoCardDesc.visible = False
            self.widget.leftDownNoCardDesc.visible = False
            self.widget.rightTopNoCardDesc.visible = not cardObj.isBreakRank
        else:
            self.widget.leftDownNoCardDesc.visible = True
            self.widget.rightTopNoCardDesc.visible = True
            self.widget.leftTopNoCardDesc.visible = True
        self.widget.cutLine.visible = not self.widget.rightTopNoCardDesc.visible and not self.widget.rightPropertyList.canvas.singlePropertyMc.visible

    def refreshCardList(self):
        if not self.hasBaseData():
            return
        self.uiAdapter.cardSystem.setAllCardList(filterFunc=self.filterCardFunc, sortFunc=self.sortCardFunc)
        self.refreshRightInfo()

    def sortCardFunc(self, cardIds):
        if cardIds:
            p = BigWorld.player()

            def sort_cardId(cardId1, cardId2):
                cardObj1 = p.getCard(cardId1)
                cardObj2 = p.getCard(cardId2)
                if cardObj1.isBreakRank and not cardObj2.isBreakRank:
                    return 1
                if not cardObj1.isBreakRank and cardObj2.isBreakRank:
                    return -1
                if cardObj1.showPriority < cardObj2.showPriority:
                    return 1
                if cardObj1.showPriority > cardObj2.showPriority:
                    return -1
                return 0

            cardIds.sort(cmp=sort_cardId, reverse=True)
        return cardIds

    def refreshLeftDetailMc(self):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
        cardObj = p.getCard(selCardId)
        if not cardObj:
            self.widget.leftDetailMc.visible = False
            return
        self.widget.leftDetailMc.visible = True
        cardMc = self.widget.leftDetailMc.cardMc
        if cardMc:
            cardMc.icon.fitSize = True
            cardMc.littleIcon.fitSize = True
            itemData = cardObj.getConfigData()
            cardMc.nameTxt.text = itemData.get('name', '')
            cardMc.icon.loadImage(cardObj.cardIcon)
            cardMc.littleIcon.loadImage(cardObj.equipIcon)
            self.uiAdapter.cardSystem.setCardLevel(cardMc, cardObj.advanceLvEx)
        self.setPropertyMc(self.widget.leftDetailMc.leftPropertyList.canvas.leftPropertyMc, cardObj.curWashProps, itemType='CardChange_BigPropItem', isShort=False)

    def refreshCdTime(self):
        self.cancelCdTimeCallBack()
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
        cardObj = p.getCard(selCardId)
        if not cardObj:
            self.widget.leftDetailMc.cdProgressBar.visible = False
            self.widget.leftDetailMc.cdTimeTxt.visible = False
            return
        curSelType, subType = self.getCurSlectedType()
        if cardObj.isCoolingDown and curSelType == CARD_CHANGE_WASH_TYPE:
            self.widget.leftDetailMc.cdProgressBar.visible = True
            self.widget.leftDetailMc.cdTimeTxt.visible = True
            self.updateTimeCB = BigWorld.callback(1, self.refreshCdTime)
            cdTime = cardObj.lastDelWashTime + const.CARD_WASH_COOL_DOWN - utils.getNow()
            cdStr = utils.formatDurationShortVersion(cdTime)
            self.widget.leftDetailMc.cdTimeTxt.text = gameStrings.CARD_CHANGE_WASH_CD_TIME_TXT % (cdStr,)
            self.widget.leftDetailMc.cdProgressBar.lableVisible = False
            self.widget.leftDetailMc.cdProgressBar.maxValue = const.CARD_WASH_COOL_DOWN
            self.widget.leftDetailMc.cdProgressBar.currentValue = utils.getNow() - cardObj.lastDelWashTime
        else:
            self.widget.leftDetailMc.cdProgressBar.visible = False
            self.widget.leftDetailMc.cdTimeTxt.visible = False

    def cancelCdTimeCallBack(self):
        if self.updateTimeCB:
            BigWorld.cancelCallback(self.updateTimeCB)
        self.updateTimeCB = None

    def refreshRightInfo(self):
        if not self.hasBaseData():
            return
        else:
            p = BigWorld.player()
            selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
            cardObj = p.getCard(selCardId, tempId=self.tempId)
            curSelType, subType = self.getCurSlectedType()
            curWashIndexTab = self.getCurWashIndexTab()
            self.widget.rightPropertyList.canvas.singlePropertyMc.visible = False
            self.widget.singlePropTitle.visible = False
            if curSelType == CARD_CHANGE_WASH_TYPE:
                self.widget.washTitle.visible = True
                self.widget.removeTitle.visible = False
                self.widget.washBtn.label = gameStrings.CARD_CHANGE_WASH
                self.widget.takeEffectMc.visible = False
                self.widget.leftPropTitle.visible = False
                self.widget.rightPropTitle.visible = False
                self.widget.takeEffectBtn.visible = False
                self.widget.takeEffectMc.visible = False
                self.widget.saveTxt.visible = False
                self.widget.firstChangeTips.visible = False
                if cardObj:
                    self.widget.firstChangeTips.visible = not bool(cardObj.washProps) and not bool(cardObj.newWashProps) and cardObj.isBreakRank
                    if cardObj.washIndex == curWashIndexTab:
                        self.widget.takeEffectMc.visible = gameconfigCommon.enableCardWashScheme()
                    else:
                        self.widget.takeEffectBtn.visible = gameconfigCommon.enableCardWashScheme() and cardObj.isBreakRank
                    self.widget.saveTxt.visible = gameconfigCommon.enableCardWashScheme()
                    self.widget.saveTxt.text = gameStrings.CARD_CHANGE_WASH_SAVE_TXT + str(curWashIndexTab + 1)
                    self.widget.leftPropTitle.visible = True
                    self.widget.rightPropTitle.visible = True
                    self.widget.leftPropTitle.titleTxt.text = gameStrings.CARD_CHANGE_CUR_WASH_TITLE
                    self.widget.rightPropTitle.titleTxt.text = gameStrings.CARD_CHANGE_RE_WASH_TITLE
                    self.widget.rightPropertyList.visible = True
                    self.widget.propTabMc.visible = gameconfigCommon.enableCardWashScheme()
                    self.widget.washComsumableMc.visible = cardObj.isBreakRank
                    self.widget.removeComsumableMc.visible = False
                    showWashProp = self.getShowCardWashProp(cardObj)
                    self.widget.oldWashBtn.visible = bool(showWashProp) and bool(cardObj.newWashProps)
                    self.widget.newWashBtn.visible = bool(cardObj.newWashProps)
                    self.widget.washBtn.enabled = cardObj.isBreakRank
                    CARD_SYSTEM_PROP_TYPE_DESC = SCD.data.get('CARD_SYSTEM_PROP_TYPE_DESC', {})
                    fragmentName = CARD_SYSTEM_PROP_TYPE_DESC.get(cardObj.propType, '')
                    ownFragmentCnt = self.cardBag.get('fragment', {}).get(cardObj.propType, 0)
                    needFragmentCnt = cardObj.getWashCost()
                    self.widget.washComsumableMc.fragmentCountTxt.htmlText = gameStrings.CARD_CHANGE_FRAGMENT_COST_TXT % (fragmentName, uiUtils.convertNumStr(ownFragmentCnt, needFragmentCnt, enoughColor=NUM_ENOUGH_COLOR))
                    self.widget.washComsumableMc.fragmentDesc.moneyIcon.bonusType = BONUS_TYPE_DICT.get(cardObj.propType, '')
                    self.widget.washComsumableMc.pointDesc.moneyIcon.tip = gameStrings.CARD_WASH_POINT_TIP_TXT % (fragmentName,)
                    needTianbi = needFragmentCnt * const.CARD_FRAGMENT_TIANBI_RATE
                    ownTianbi = p.unbindCoin + p.bindCoin + p.freeCoin
                    self.widget.washComsumableMc.tianbiTxt.htmlText = gameStrings.CARD_CHANGE_TIANBI_COST_TXT % (uiUtils.convertNumStr(ownTianbi, needTianbi, enoughColor=NUM_ENOUGH_COLOR),)
                    ownWashPoint = self.cardBag.get('cardWashPoint', {}).get(cardObj.propType, 0)
                    needWashPoint = int(math.floor(needFragmentCnt / const.CARD_FRAGMENT_POINT_RATE))
                    if cardObj.isCoolingDown:
                        self.widget.washComsumableMc.washPointDesc.washPointTxt.htmlText = gameStrings.CARD_CHANGE_WASH_CD_TXT
                        self.widget.washComsumableMc.selWashPointBtn.enabled = False
                        ASUtils.setMcEffect(self.widget.washComsumableMc.washPointDesc, 'gray')
                    else:
                        ownWashPoint = self.cardBag.get('cardWashPoint', {}).get(cardObj.propType, 0)
                        needWashPoint = int(math.floor(needFragmentCnt / const.CARD_FRAGMENT_POINT_RATE))
                        self.widget.washComsumableMc.washPointDesc.washPointTxt.htmlText = gameStrings.CARD_CHANGE_WASHPOINT_COST_TXT % (fragmentName, uiUtils.convertNumStr(ownWashPoint, needWashPoint, enoughColor=NUM_ENOUGH_COLOR))
                        self.widget.washComsumableMc.selWashPointBtn.enabled = ownWashPoint >= needWashPoint
                        ASUtils.setMcEffect(self.widget.washComsumableMc.washPointDesc, '' if ownWashPoint >= needWashPoint else 'gray')
                    btnList = [self.widget.washComsumableMc.selWashPointBtn, self.widget.washComsumableMc.tianbiBtn, self.widget.washComsumableMc.selFragmentBtn]
                    initBtn = self.widget.washComsumableMc.selWashPointBtn.group.selectedButton
                    for btn in btnList:
                        if not btn.enabled and btn.selected:
                            btn.selected = False
                            if initBtn == btn:
                                initBtn = None
                        if not initBtn and btn.enabled and not btn.selected:
                            btn.selected = True
                            initBtn = btn

                    if cardObj.isBreakRank:
                        showWashProp = self.getShowCardWashProp(cardObj)
                        self.setPropertyMc(self.widget.rightPropertyList.canvas.leftPropertyMc, showWashProp)
                        self.setPropertyMc(self.widget.rightPropertyList.canvas.rightPropertyMc, cardObj.newWashProps)
                        self.widget.rightPropertyList.canvas.leftPropertyMc.visible = True
                        self.widget.rightPropertyList.canvas.rightPropertyMc.visible = True
                    else:
                        self.setPropertyMc(self.widget.rightPropertyList.canvas.leftPropertyMc, {})
                        self.setPropertyMc(self.widget.rightPropertyList.canvas.rightPropertyMc, {})
                else:
                    self.widget.rightPropertyList.visible = False
                    self.widget.propTabMc.visible = False
                    self.widget.washComsumableMc.visible = False
                    self.widget.removeComsumableMc.visible = False
                    self.widget.oldWashBtn.visible = False
                    self.widget.newWashBtn.visible = False
                    self.widget.washBtn.enabled = False
                    self.widget.leftPropTitle.visible = False
                    self.widget.rightPropTitle.visible = False
            elif curSelType == CARD_CHANGE_REMOVE_TYPE:
                self.widget.saveTxt.visible = False
                self.widget.takeEffectMc.visible = False
                self.widget.takeEffectBtn.visible = False
                self.widget.propTabMc.visible = False
                self.widget.washTitle.visible = False
                self.widget.removeTitle.visible = True
                self.widget.oldWashBtn.visible = False
                self.widget.newWashBtn.visible = False
                self.widget.takeEffectMc.visible = False
                self.widget.leftPropTitle.visible = False
                self.widget.rightPropTitle.visible = False
                self.widget.firstChangeTips.visible = False
                self.widget.washBtn.label = gameStrings.CARD_CHANGE_REMOVE
                if cardObj:
                    self.widget.leftPropTitle.visible = True
                    self.widget.rightPropTitle.visible = True
                    self.widget.leftPropTitle.titleTxt.text = gameStrings.CARD_CHANGE_WASH_TITLE % gameStrings.CARD_WASH_INDEX.get(0, '')
                    self.widget.rightPropTitle.titleTxt.text = gameStrings.CARD_CHANGE_WASH_TITLE % gameStrings.CARD_WASH_INDEX.get(1, '')
                    self.widget.rightPropertyList.visible = True
                    self.widget.rightTopNoCardDesc.visible = False
                    self.widget.washComsumableMc.visible = False
                    self.widget.removeComsumableMc.visible = True
                    self.widget.washBtn.enabled = True
                    CARD_SYSTEM_PROP_TYPE_DESC = SCD.data.get('CARD_SYSTEM_PROP_TYPE_DESC', {})
                    fragmentName = CARD_SYSTEM_PROP_TYPE_DESC.get(cardObj.propType, '')
                    washCost = cardObj.compoundFragmentCnt(0)
                    itemId = cardObj.cardItemParentId
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
                    state = uiConst.ITEM_NORMAL if count else uiConst.ITEM_GRAY
                    numStr = uiUtils.convertNumStr(count, washCost / cardObj.fagmentCntValue)
                    itemInfo['state'] = state
                    self.widget.removeComsumableMc.itemNumTxt.htmlText = numStr
                    self.widget.removeComsumableMc.itemSlot.dragable = False
                    self.widget.removeComsumableMc.itemSlot.setItemSlotData(itemInfo)
                    self.widget.removeComsumableMc.itemBtn.enabled = bool(count)
                    itemId = SCD.data.get('fragmentItemId', {}).get(cardObj.propType, 0)
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    count = self.cardBag.get('fragment', {}).get(cardObj.propType, 0)
                    state = uiConst.ITEM_NORMAL if count else uiConst.ITEM_GRAY
                    numStr = uiUtils.convertNumStr(count, washCost)
                    itemInfo['state'] = state
                    self.widget.removeComsumableMc.fragmentNumTxt.htmlText = numStr
                    self.widget.removeComsumableMc.fragmentSlot.dragable = False
                    self.widget.removeComsumableMc.fragmentSlot.setItemSlotData(itemInfo)
                    self.widget.removeComsumableMc.fragmentName.text = gameStrings.CARD_COMMON_FRAGMENT_TXT % (fragmentName,)
                    self.widget.removeComsumableMc.fragmentBtn.enabled = bool(count)
                    if not self.widget.removeComsumableMc.itemBtn.enabled and self.widget.removeComsumableMc.itemBtn.selected:
                        self.widget.removeComsumableMc.fragmentBtn.selected = True
                    self.setPropertyMc(self.widget.rightPropertyList.canvas.leftPropertyMc, cardObj.washProps)
                    self.setPropertyMc(self.widget.rightPropertyList.canvas.rightPropertyMc, cardObj.washPropsEx)
                    self.widget.rightPropertyList.canvas.leftPropertyMc.visible = True
                    self.widget.rightPropertyList.canvas.rightPropertyMc.visible = True
                    if not gameconfigCommon.enableCardWashScheme():
                        self.widget.rightPropertyList.canvas.leftPropertyMc.visible = False
                        self.widget.rightPropertyList.canvas.rightPropertyMc.visible = False
                        self.widget.leftPropTitle.visible = False
                        self.widget.rightPropTitle.visible = False
                        self.widget.rightPropertyList.canvas.singlePropertyMc.visible = True
                        self.setPropertyMc(self.widget.rightPropertyList.canvas.singlePropertyMc, cardObj.curWashProps)
                        self.widget.singlePropTitle.visible = True
                        self.widget.singlePropTitle.titleTxt.text = gameStrings.CARD_CHANGE_CUR_WASH_TITLE
                else:
                    self.widget.rightPropertyList.visible = False
                    self.widget.rightTopNoCardDesc.visible = True
                    self.widget.washComsumableMc.visible = False
                    self.widget.removeComsumableMc.visible = False
                    self.widget.washBtn.enabled = False
                    self.widget.leftPropTitle.visible = False
                    self.widget.rightPropTitle.visible = False
            if cardObj:
                washCost = cardObj.getWashCost()
                lackFragment = max(0, washCost - self.cardBag.get('fragment', {}).get(cardObj.propType, 0))
                needTianbi = lackFragment * const.CARD_FRAGMENT_TIANBI_RATE
                tips = gameStrings.CARD_TIANBI_DIKOU % (needTianbi,)
                if tips:
                    TipManager.addTip(self.widget.helpIcon, tips)
                self.widget.curWashAdd.visible = True
                self.widget.newWashAdd.visible = True
                showWashProp = self.getShowCardWashProp(cardObj)
                self.widget.curWashAdd.htmlText = gameStrings.CARD_CHANGE_PROPPERTY_ADD % (len(showWashProp) * const.CARD_WASH_PROP_NUM_ADD_PCT,)
                newWashAddText = gameStrings.CARD_CHANGE_PROPPERTY_ADD_LESS if len(cardObj.newWashProps) < len(showWashProp) else gameStrings.CARD_CHANGE_PROPPERTY_ADD_MORE
                self.widget.newWashAdd.htmlText = newWashAddText % (len(cardObj.newWashProps) * const.CARD_WASH_PROP_NUM_ADD_PCT,)
            else:
                self.setPropertyMc(self.widget.rightPropertyList.canvas.leftPropertyMc, {})
                self.setPropertyMc(self.widget.rightPropertyList.canvas.rightPropertyMc, {})
                self.widget.curWashAdd.visible = False
                self.widget.newWashAdd.visible = False
            if curSelType == CARD_CHANGE_REMOVE_TYPE:
                self.widget.curWashAdd.visible = False
                self.widget.newWashAdd.visible = False
            self.widget.propHelpIcon.visible = self.widget.newWashAdd.visible
            self.refreshSpecialChange()
            self.refreshCdTime()
            return

    def setPropertyMc(self, itemMc, pData, itemType = 'CardChange_PropItem', isShort = True):
        if not self.hasBaseData():
            return
        elif not itemMc:
            return
        else:
            self.widget.removeAllInst(itemMc)
            if not pData:
                return
            i = 0
            pText = ''
            height = 0
            for k, v in pData.iteritems():
                propertyItem = self.widget.getInstByClsName(itemType)
                washGroupId = v.get('washGroupId', 0)
                sequence = k
                stage = v.get('stage', 0)
                sType = v.get('sType', 0)
                sId = v.get('sId', 0)
                sNum = v.get('sNum', 0)
                fullProp = v.get('fullProp', False)
                tips = ''
                washData = CWGD.data.get((washGroupId,
                 sequence,
                 stage,
                 sType,
                 sId), {})
                quality = washData.get('quality', 0)
                normalColor = uiConst.CARD_PROP_QUALITY_NORMAL_COLOR
                qualityColor = normalColor
                try:
                    qualityColor = uiConst.CARD_COLORS[quality - 1]
                except:
                    pass

                if sType == const.CARD_PROP_TYPE_PROPS:
                    shortPropertyName = PRD.data.get(sId, {}).get('shortName', '')
                    detailPropertyName = PRD.data.get(sId, {}).get('name', '')
                    propertyName = shortPropertyName if isShort else detailPropertyName
                    _, sNum = self.uiAdapter.cardSystem.transPropVal(sId, sNum)
                    pText = self.uiAdapter.cardSystem.formatPropStr(propertyName, sNum, separator='', titleColor=normalColor, valColor=qualityColor)
                elif sType == const.CARD_PROP_TYPE_PASSIVE:
                    shortDesc = PDD.data.get((sId, sNum), {}).get('mainEff', '')
                    detailDesc = PDD.data.get((sId, sNum), {}).get('mainEnhEff', '')
                    pText = shortDesc if isShort else detailDesc
                    pText = pText % (qualityColor,)
                    if isShort:
                        tips = detailDesc % (qualityColor,)
                    pText = uiUtils.toHtml(pText, normalColor)
                elif sType == const.CARD_PROP_TYPE_SPECIAL:
                    pName = CWGD.data.get((washGroupId,
                     sequence,
                     stage,
                     sType,
                     sId), {}).get('name', '')
                    pText = uiUtils.toHtml(pName, normalColor)
                elif sType == const.CARD_PROP_TYPE_CONDITIONAL_PROPS:
                    condData = CPD.data.get(sId, {})
                    formatType = int(condData.get('formatType', 0))
                    shortDesc = condData.get('cColorDesc', '')
                    detailDesc = condData.get('colorDesc', '')

                    def transDesc(desc, setColor = None):
                        if setColor:
                            if formatType == const.COND_PROP_NUM_PERCENT:
                                desc = desc % (setColor, sNum * 100)
                            else:
                                desc = desc % (setColor, sNum)
                        elif formatType == const.COND_PROP_NUM_PERCENT:
                            desc = desc % (sNum * 100,)
                        else:
                            desc = desc % (sNum,)
                        return desc

                    pDesc = transDesc(detailDesc if not isShort else shortDesc, setColor=qualityColor)
                    pText = uiUtils.toHtml(pDesc, color=normalColor)
                    if isShort:
                        tips = uiUtils.toHtml(transDesc(detailDesc, setColor=qualityColor), color=uiConst.CARD_PROP_BALCK_COLOR)
                propertyItem.fullIcon.visible = fullProp
                propertyItem.normalIcon.visible = not fullProp
                propertyItem.contentTxt.htmlText = pText
                if tips:
                    TipManager.addTip(propertyItem, tips)
                propertyItem.contentTxt.height = propertyItem.contentTxt.textHeight + 4
                propertyItem.x = 1
                propertyItem.y = height
                height += propertyItem.contentTxt.textHeight + 1
                itemMc.addChild(propertyItem)
                i += 1

            self.widget.rightPropertyList.refreshHeight()
            self.widget.leftDetailMc.leftPropertyList.refreshHeight()
            return

    def getCurSlectedType(self):
        selType = int(self.widget.washTabBtn.group.selectedButton.data)
        subType = 0
        if selType == CARD_CHANGE_WASH_TYPE:
            subType = int(self.widget.washComsumableMc.selFragmentBtn.group.selectedButton.data)
        elif selType == CARD_CHANGE_REMOVE_TYPE:
            subType = int(self.widget.removeComsumableMc.itemBtn.group.selectedButton.data)
        return (selType, subType)

    def getCurWashIndexTab(self):
        curWashIndexTab = int(self.widget.propTabMc.tab0.group.selectedButton.data)
        return curWashIndexTab

    def getShowCardWashProp(self, cardObj, washIndex = -1):
        if washIndex == -1:
            washIndex = self.getCurWashIndexTab()
        if not washIndex:
            return cardObj.washProps
        elif not cardObj.washPropsEx:
            return {}
        else:
            return cardObj.washPropsEx

    def handleTabBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        t.selected = True
        self.refreshLeftDetailMc()
        self.refreshRightInfo()
        self.refreshNoCardDesc()

    def handlePropTabBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        t.selected = True
        self.refreshLeftDetailMc()
        self.refreshRightInfo()

    def handleTakeEffectBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        propTab = self.getCurWashIndexTab()
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
        cardObj = p.getCard(selCardId, tempId=self.tempId)
        (itemId, itemNum), = SCD.data.get('cardSecondWashSchemeCost', {}).get(cardObj.monsterType, {}).get(cardObj.propType, {})
        itemName = ID.data.get(itemId, {}).get('name', '')
        if propTab and cardObj.checkUnlockWashScheme(propTab):
            msg = gameStrings.CARD_CHANGE_WASH_UNLOCK_SCHEME_CONFIRM_TXT % (itemName, itemNum)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.unlockCardWashScheme, cardObj.id, propTab))
            return
        p.base.changeCardWashScheme(selCardId, propTab)

    def handleCardBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        t.selected = True
        self.refreshCardList()

    @ui.checkInventoryLock()
    def handleWashBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
        cardObj = p.getCard(selCardId, tempId=self.tempId)
        if not cardObj:
            return
        cipher = p.cipherOfPerson
        if self.isSpecialChange:
            sWashNumId = self.specialChangeInfo.get('washNumId', 0)
            if cardObj.washNumId == sWashNumId:
                specialItemId = self.specialChangeInfo.get('itemId', 0)
                func = Functor(p.base.washCardWithItem, cardObj.id, specialItemId, cipher)
                showWashProp = self.getShowCardWashProp(cardObj)
                if self.checkWashCondition(cardObj.newWashProps, showWashProp, func):
                    func()
            else:
                p.showGameMsg(GMDD.data.NOT_CARD_WASH_ITEM, ())
            return
        washCost = cardObj.getWashCost()
        curSelType, subType = self.getCurSlectedType()
        if curSelType == CARD_CHANGE_WASH_TYPE:
            if subType == CARD_CHANGE_WASH_TYPE_FRAGMENT:
                if self.widget.lackMaterialCheckBox.selected:
                    lackFragment = max(0, washCost - self.cardBag.get('fragment', {}).get(cardObj.propType, 0))
                    dikouNum = lackFragment * const.CARD_FRAGMENT_TIANBI_RATE
                    self._washCard(selCardId, cipher, const.CARD_DIKOU_TYPE_TIANBI, dikouNum)
                else:
                    self._washCard(selCardId, cipher, 0, 0)
            elif subType == CARD_CHANGE_WASH_TYPE_WASHPOINT:
                self._washCard(selCardId, cipher, const.CARD_DIKOU_TYPE_WASH_POINT, washCost)
            elif subType == CARD_CHANGE_WASH_TYPE_TIANBI:
                lackFragment = washCost
                dikouNum = lackFragment * const.CARD_FRAGMENT_TIANBI_RATE
                self._washCard(selCardId, cipher, const.CARD_DIKOU_TYPE_TIANBI, dikouNum)
        elif curSelType == CARD_CHANGE_REMOVE_TYPE:
            if subType == CARD_CHANGE_REMOVE_TYPE_ITEM:
                self._delWashCard(selCardId, cipher, const.CARD_DIKOU_TYPE_CARD_ITEM, 1)
            elif subType == CARD_CHANGE_REMOVE_TYPE_FRAGMENT:
                if self.widget.lackMaterialCheckBox.selected:
                    lackFragment = max(0, washCost - self.cardBag.get('fragment', {}).get(cardObj.propType, 0))
                    dikouNum = lackFragment * const.CARD_FRAGMENT_TIANBI_RATE
                    self._delWashCard(selCardId, cipher, const.CARD_DIKOU_TYPE_TIANBI, dikouNum)
                else:
                    self._delWashCard(selCardId, cipher, 0, 0)

    def _delWashCard(self, cardId, cipher, dikouType, dikouNum):
        p = BigWorld.player()
        cardObj = p.getCard(cardId)
        returnRate = self.uiAdapter.cardSystem.getWashPointRetunRate(cardObj)
        washPoint = math.floor(cardObj.washNum * cardObj.washFragmentCnt * returnRate)
        CARD_SYSTEM_PROP_TYPE_DESC = SCD.data.get('CARD_SYSTEM_PROP_TYPE_DESC', {})
        fragmentName = CARD_SYSTEM_PROP_TYPE_DESC.get(cardObj.propType, '')
        _msg = gameStrings.CARD_CHANGE_REMOVE_CONFIRM_MESSAGE % (washPoint, fragmentName)
        self.uiAdapter.messageBox.showYesNoMsgBox(_msg, yesCallback=Functor(p.base.delWashCard, cardId, cipher, dikouType, dikouNum))

    @ui.checkInventoryLock()
    def _washCard(self, cardId, cipher, dikouType, dikouNum):
        p = BigWorld.player()
        cardObj = p.getCard(cardId)
        if not cardObj:
            return
        func = Functor(p.base.washCard, cardId, cipher, dikouType, dikouNum)
        showWashProp = self.getShowCardWashProp(cardObj)
        if self.checkWashCondition(cardObj.newWashProps, showWashProp, func):
            func()

    def checkWashCondition(self, desertedProp, targetProp, func, prefix = gameStrings.CARD_CHANGE_NEW_PROP):

        def _confirmMsgFunc(msg):
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=func)

        if len(desertedProp) > len(targetProp):
            _msg = gameStrings.CARD_WASH_NEW_PROP_MORE_CONFIRM % (prefix,)
            _confirmMsgFunc(_msg)
            return False
        oldScore = 0
        for k, v in targetProp.iteritems():
            oldScore += v.get('score', 0)

        newScore = 0
        for k, v in desertedProp.iteritems():
            newScore += v.get('score', 0)
            if v.get('fullProp', False):
                _msg = gameStrings.CARD_WASH_NEW_PROP_MAX_CONFIRM % (prefix,)
                _confirmMsgFunc(_msg)
                return False

        if newScore > oldScore * NEWPROP_REMAIN_RADIO:
            _msg = gameStrings.CARD_WASH_NEW_PROP_SCORE_CONFIRM % (prefix,)
            _confirmMsgFunc(_msg)
            return False
        return True

    def handleOldWashBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        schemeSelect = self.getCurWashIndexTab()
        func = Functor(self.confirmWashCard, 0, schemeSelect)
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
        cardObj = p.getCard(selCardId)
        showWashProp = self.getShowCardWashProp(cardObj)
        if self.checkWashCondition(cardObj.newWashProps, showWashProp, func, gameStrings.CARD_CHANGE_NEW_PROP):
            func()

    def handleNewWashBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        schemeSelect = self.getCurWashIndexTab()
        func = Functor(self.confirmWashCard, 1, schemeSelect)
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
        cardObj = p.getCard(selCardId)
        showWashProp = self.getShowCardWashProp(cardObj)
        if self.checkWashCondition(showWashProp, cardObj.newWashProps, func, gameStrings.CARD_CHANGE_OLD_PROP):
            func()

    @ui.checkInventoryLock()
    def confirmWashCard(self, confirmNo, schemeSelect = 0):
        p = BigWorld.player()
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
        if selCardId:
            cipher = p.cipherOfPerson
            p.base.confirmWashCard(selCardId, cipher, confirmNo, schemeSelect)

    def handleWashSubTypeBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        t.selected = True

    def handleRemoveSubTypeBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        t.selected = True

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def handleLackMaterialCheckBoxClick(self, *arg):
        pass

    def showSpecialChange(self, item, nPage, nItem):
        if not gameglobal.rds.configData.get('enableCardSpecialChange', False):
            return
        eData = EEICD.data.get(item.id, {})
        washNumId = eData.get('washNumId', 0)
        self.specialChangeInfo = {'itemId': item.id,
         'desc': eData.get('desc', ''),
         'washNumId': washNumId}
        self.uiAdapter.cardSystem.hide()
        self.uiAdapter.cardSystem.show(TAB_INDEX_CARD_CHANGE, isSpecialChangeForChangeTab=True)
        self.uiAdapter.cardSystem.setWashNumIdFilter([washNumId])

    def refreshSpecialChange(self):
        if not self.hasBaseData():
            return
        if self.isSpecialChange:
            self.widget.washTitle.visible = False
            self.widget.removeTitle.visible = False
            self.widget.washComsumableMc.visible = False
            self.widget.removeComsumableMc.visible = False
            self.widget.helpIcon.visible = False
            self.widget.washTabBtn.visible = False
            self.widget.removeTabBtn.visible = False
            self.widget.specialChangeMc.visible = True
            if self.specialChangeInfo:
                p = BigWorld.player()
                itemId = self.specialChangeInfo.get('itemId', 0)
                itemInfo = uiUtils.getGfxItemById(itemId)
                count = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
                state = uiConst.ITEM_NORMAL if count else uiConst.ITEM_GRAY
                numStr = uiUtils.convertNumStr(count, 1)
                itemInfo['state'] = state
                self.widget.specialChangeMc.contentTxt.htmlText = self.specialChangeInfo.get('desc', '')
                self.widget.specialChangeMc.removeComsumableMc.itemSlot.dragable = False
                self.widget.specialChangeMc.removeComsumableMc.itemSlot.setItemSlotData(itemInfo)
                self.widget.specialChangeMc.removeComsumableMc.itemNumTxt.htmlText = numStr
        else:
            self.widget.specialChangeMc.visible = False
