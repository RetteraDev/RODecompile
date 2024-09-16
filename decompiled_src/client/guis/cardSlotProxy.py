#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cardSlotProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import events
import uiUtils
import uiConst
import const
import ui
import math
import gameconfigCommon
from asObject import ASObject
from asObject import TipManager
from asObject import ASUtils
from asObject import RedPotManager
from guis import tipUtils
from gamestrings import gameStrings
from callbackHelper import Functor
from uiProxy import UIProxy
from data import base_card_data as BCD
from data import card_suit_data as CSD
from data import sys_config_data as SCD
from data import card_equip_type_data as CETD
from cdata import pskill_data as PDD
from cdata import pskill_template_data as PTD
from cdata import game_msg_def_data as GMDD
from cdata import card_compose_to_suit_data as CCTSD
from data import card_slot_resonance_data as CSRD
TEMP_ICON = 'summonedSprite/icon/1014.dds'
CONFIG_DATA_NUM = 10
TAB_INDEX_CARD_SLOT = 2
DROP_DOWN_ROW_MAX = 5
PROP_ITEM_HEIGHT = 13
BACKUP_SLOT_LIST_Y_1 = 0
BACKUP_SLOT_LIST_Y_2 = 40
CUR_SLOT_LIST_Y_1 = 34
CUR_SLOT_LIST_Y_2 = 74
RESONANCE_PANEL_BGIMG_INIT_HEIGHT = 75
RESONANCE_START_POS_X = 12
RESONANCE_START_POS_Y = 68
RESONANCE_BIG_TITLE_POS_X = 10
RESONANCE_SMALL_TITLE_POS_X = 13
RESONANCE_ITEM_POS_X = 27
RESONANCE_UNLOCK_POS_X = 11
RESONANCE_NEXT_STAGE_POS_X = 87
RESONANCE_BGMC_WIDTH = 260

class CardSlotProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CardSlotProxy, self).__init__(uiAdapter)
        self.widget = None
        self.showCardEquip = True
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
        self.menuData = []
        self.tabDict = {}
        self.previewCompose = []
        self.excludeCompose = []
        self.rightEquipTypeCardIds = []
        self.selectedSlotId = None
        self.selectedSlotItem = None
        self.canRefreshCard = False
        self.isResonancePanelOpening = False

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        p = BigWorld.player()
        self.widget.curSlotList.canvas.y = CUR_SLOT_LIST_Y_1 if gameconfigCommon.enableCardSlotExtend() else CUR_SLOT_LIST_Y_2
        self.widget.backupSlotList.canvas.y = BACKUP_SLOT_LIST_Y_1 if gameconfigCommon.enableCardSlotExtend() else BACKUP_SLOT_LIST_Y_2
        self.widget.moreBtn.addEventListener(events.BUTTON_CLICK, self.handleMoreBtnClick, False, 0, True)
        self.widget.moreBtn.visible = not bool(self.tempId)
        self.widget.buffListenerSettingBtn.addEventListener(events.BUTTON_CLICK, self.handleBuffListenerSettingBtnClick, False, 0, True)
        self.widget.moreBtn.x = 653 if gameconfigCommon.enableBuffListener() else 703
        self.widget.buffListenerSettingBtn.visible = True if gameconfigCommon.enableBuffListener() else False
        self.widget.opTipTxt.htmlText = gameStrings.CARD_SLOT_EQUIP_CARD_TIP
        self.widget.cardBtn0.groupName = 'slotTab'
        self.widget.cardBtn0.data = 1
        self.widget.cardBtn1.groupName = 'slotTab'
        self.widget.cardBtn1.data = 2
        self.widget.cardBtn0.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.cardBtn1.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)
        self.widget.suitHelp.visible = gameglobal.rds.configData.get('enableChangeCardSuit', 0)
        self.tabDict = {self.widget.cardBtn0.data: self.widget.cardBtn0,
         self.widget.cardBtn1.data: self.widget.cardBtn1}
        equipSlot = self.cardBag.get('equipSlot', 0)
        if equipSlot in self.tabDict:
            btn = self.tabDict.get(equipSlot, None)
            if btn:
                btn.selected = True
        else:
            self.widget.cardBtn0.selected = True
        self.uiAdapter.cardSystem.setMenuComm()
        self.widget.propertyList.itemRenderer = 'CardSlot_PropertyItem'
        self.widget.propertyList.labelFunction = self.propertyItemFunc
        self.widget.propertyList.itemHeightFunction = self.propListItemHeightFunction
        self.widget.propertyList.dataArray = []
        self.widget.curSlotList.column = 3
        self.widget.curSlotList.itemHeight = 100
        self.widget.curSlotList.itemWidth = 86
        self.widget.curSlotList.itemRenderer = 'CardSlot_SlotItem'
        self.widget.curSlotList.labelFunction = self.slotListFunction
        self.widget.curSlotList.dataArray = []
        self.widget.backupSlotList.column = 3
        self.widget.backupSlotList.itemHeight = 100
        self.widget.backupSlotList.itemWidth = 86
        self.widget.backupSlotList.itemRenderer = 'CardSlot_SlotItem'
        self.widget.backupSlotList.labelFunction = self.slotListFunction
        self.widget.backupSlotList.dataArray = []
        self.widget.backupSlotList.activateBtn.addEventListener(events.BUTTON_CLICK, self.handleActivateBtnClick, False, 0, True)
        self.refreshSlotList()
        self.widget.cardList.column = 3
        self.widget.cardList.itemHeight = 230
        self.widget.cardList.itemWidth = 168
        self.widget.cardList.itemRenderer = 'CardSystem_CardContainer'
        self.uiAdapter.cardSystem.setAllCardList(filterFunc=self.filterCardFunc)
        self.canRefreshCard = True
        self.refreshScore()
        self.setTemplateState()
        self.showResonancePanelBtn()

    def setTemplateState(self):
        p = BigWorld.player()
        if p.isUsingTemp() and not p.inBalanceTemplateWhiteList() or self.tempId:
            self.widget.backupSlotList.activateBtn.visible = False

    def filterCardFunc(self, cardObj):
        if not cardObj:
            return False
        if cardObj.noFixToSlot:
            return False
        return True

    def refreshInfo(self):
        if not self.hasBaseData():
            return

    def canFixToSlot(self, slotId, cardObj):
        p = BigWorld.player()
        slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
        if slotCardId == cardObj.id:
            return True
        cardInSlot = p.getCard(slotCardId, True, tempId=self.tempId) if slotCardId != 0 else None
        if cardInSlot and cardInSlot.slot and cardObj.slot:
            return False
        elif not cardObj.actived and self.cardBag.get('fragment', {}).get(cardObj.propType, 0) < cardObj.compoundFragmentCnt(0):
            return False
        else:
            return True

    def canCompoundCard(self, cardObj):
        p = BigWorld.player()
        if self.cardBag.get('fragment', {}).get(cardObj.propType, 0) >= cardObj.compoundFragmentCnt(0):
            return True

    def refreshCardList(self):
        if not self.hasBaseData():
            return
        if not self.canRefreshCard:
            return
        self.uiAdapter.cardSystem.setAllCardList(filterFunc=self.filterCardFunc)

    def refreshCurSuitMenu(self):
        if not self.hasBaseData():
            return
        self.menuData = []
        p = BigWorld.player()
        sceneType = p.getCardSceneType()
        propertyData = []
        sType = self.getCurSlotType()
        suitInfo = self.getPskillEffects(sType)
        equipSlot = self.cardBag.get('equipSlot', 0)
        propType = 0
        curSuitId, curSuitRank = self.cardBag.get('equipSuit', {}).get(sType, (0, 0))
        selIndex = 0
        hasFullSuit = False
        i = 0
        slotNumMax = SCD.data.get('cardSlotNowMaxNum', const.CARD_SLOT_NOW_MAX_NUM)
        for k, v in suitInfo.iteritems():
            suitData = CSD.data.get(k, {})
            if (curSuitId, curSuitRank) == k:
                selIndex = i
            if len(suitData.get('compose', ())) == slotNumMax:
                hasFullSuit = True
            i += 1

        if hasFullSuit:
            for k, v in suitInfo.iteritems():
                suitData = CSD.data.get(k, {})
                propType = suitData.get('propType', 0)
                titleName = suitData.get('name', '')
                _suitId, _suitRank = k
                info = {'label': titleName,
                 'iconType': 0,
                 'suitId': _suitId,
                 'suitRank': _suitRank}
                self.menuData.append(info)

        else:
            selIndex = 0
            suitData = CSD.data.get((curSuitId, curSuitRank), {})
            propType = suitData.get('propType', 0)
            titleName = suitData.get('name', '')
            info = {'label': titleName,
             'iconType': 0,
             'suitId': curSuitId,
             'suitRank': curSuitRank}
            self.menuData.append(info)
        ASUtils.setDropdownMenuData(self.widget.suitMenu, self.menuData)
        self.widget.suitMenu.selectedIndex = selIndex
        self.widget.suitMenu.menuRowCount = min(len(self.menuData), DROP_DOWN_ROW_MAX)
        self.widget.suitMenu.clickItemFunction = self.handleMenuItemClick
        self.widget.suitMenu.addEventListener(events.LIST_EVENT_INDEX_CHANGE, self.handleSuitMenuItemSelected, False, 0, True)
        self.widget.suitMenu.visible = bool(self.widget.propertyList.dataArray) and gameglobal.rds.configData.get('enableChangeCardSuit', 0)
        self.widget.suitHelp.visible = self.widget.suitMenu.visible

    def handleMenuItemClick(self, *arg):
        if not self.hasBaseData():
            return GfxValue(False)
        e = ASObject(arg[3][0])
        t = e.target
        selIndex = e.index
        selData = self.widget.suitMenu.dataProvider[selIndex]
        suitId = selData.get('suitId', 0)
        suitRank = selData.get('suitRank', 0)
        sType = self.getCurSlotType()
        p = BigWorld.player()
        p.base.setCardSlotSuit(sType, suitId)
        return GfxValue(False)

    def handleSuitMenuItemSelected(self, *arg):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        selIndex = self.widget.suitMenu.selectedIndex
        selData = self.widget.suitMenu.dataProvider[selIndex]
        suitId = selData.get('suitId', 0)
        suitRank = selData.get('suitRank', 0)
        sType = self.getCurSlotType()
        p.base.setCardSlotSuit(sType, suitId)

    def handlePropMenuSel(self, *args):
        pass

    def handleVersionMenuSel(self, *args):
        pass

    def handleTypeMenuSel(self, *args):
        pass

    def onSelectedCard(self, cardItem, inital = False, oldCardId = 0):
        if cardItem:
            p = BigWorld.player()
            cardObj = p.getCard(cardItem.cardId, tempId=self.tempId)
            if cardObj and cardObj.slot:
                sType = self.getCurSlotType()
                for slotId in cardObj.slot:
                    slotType, slotIndex = self.uiAdapter.cardSystem.parseSlotId(slotId)
                    if sType == slotType:
                        self.selectSlot(slotType, slotIndex - 1)

        self.refreshRevertBtn()

    def autoSelectEmptySlot(self):
        p = BigWorld.player()
        sType = self.getCurSlotType()
        slotNum = self.cardBag.get('slotNum', {}).get(sType, 0)
        for i in xrange(0, slotNum):
            slotId = sType * const.CARD_SLOT_DIV_NUM + i + 1
            slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
            if not slotCardId:
                self.selectSlot(sType, i)
                break

    def selectSlot(self, sType, index):
        p = BigWorld.player()
        slotNum = self.cardBag.get('slotNum', {}).get(sType, 0)
        if not index < slotNum:
            return
        slotId = sType * const.CARD_SLOT_DIV_NUM + index + 1
        if self.selectedSlotId != slotId:
            self.setSelectedItemBySlotId(slotId)

    def setSelectedItemBySlotId(self, slotId):
        oldSlotId = self.selectedSlotId
        newSlotId = slotId
        items = self.widget.curSlotList.items
        oldItem = None
        newItem = None
        for item in items:
            if newSlotId == item.slotId:
                newItem = item
            if oldSlotId == item.slotId:
                oldItem = item

        if slotId:
            if oldItem and self.selectedSlotId and oldItem.slotId == self.selectedSlotId:
                oldItem.selectedMc.visible = False
            self.selectedSlotId = newSlotId
            if newItem:
                self.selectedSlotItem = newItem
            if self.selectedSlotItem:
                self.selectedSlotItem.selectedMc.visible = True
        else:
            self.selectedSlotId = None
            self.selectedSlotItem = None
        self.notifySlotSelected()

    def notifySlotSelected(self):
        if self.selectedSlotItem:
            self.uiAdapter.cardSystem.setEquipTypeFilter(self.selectedSlotItem.previewEquipType)

    def getCurSlotType(self):
        if not self.hasBaseData():
            return
        return int(self.widget.cardBtn0.group.selectedButton.data)

    @ui.callAfterTime()
    def refreshSlotList(self, resetSelSlot = False):
        if not self.hasBaseData():
            return
        self.calcPreviewCompose()
        p = BigWorld.player()
        sType = self.getCurSlotType()
        equipSlot = self.cardBag.get('equipSlot', 0)
        curList, otherList = self.getListMc()
        curList.visible = True
        otherList.visible = False
        slotNumMax = SCD.data.get('cardSlotNowMaxNum', const.CARD_SLOT_NOW_MAX_NUM)
        slotNum = self.cardBag.get('slotNum', {}).get(sType, 0)
        if resetSelSlot:
            self.selectedSlotId = 0
        if not self.selectedSlotId:
            slotNum = self.cardBag.get('slotNum', {}).get(sType, 0)
            for i in xrange(0, slotNum):
                slotId = sType * const.CARD_SLOT_DIV_NUM + i + 1
                slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
                if not slotCardId:
                    self.selectedSlotId = slotId
                    break

        if not self.selectedSlotId:
            self.selectedSlotId = sType * const.CARD_SLOT_DIV_NUM + 1
        curList.dataArray = range(slotNumMax)
        curList.validateNow()
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
        self.refreshCardList()
        self.refreshRevertBtn()
        self.refreshPropertyList()
        self.refreshScore()
        self.refreshCurSuitMenu()
        self.notifySlotSelected()
        self.refreshResonancePanel()
        self.uiAdapter.cardSuit.setLeftList()

    def propertyItemFunc(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            itemMc.contentTxt.htmlText = info.label
            itemMc.normalIcon.visible = bool(info.iconType)

    def propListItemHeightFunction(self, *arg):
        if self.hasBaseData():
            info = ASObject(arg[3][0])
            descItem = self.widget.getInstByClsName('CardSlot_PropertyItem')
            descItem.contentTxt.htmlText = info.label
            height = max(PROP_ITEM_HEIGHT, descItem.contentTxt.textHeight)
            return GfxValue(height)

    def slotListFunction(self, *arg):
        index = int(arg[3][0].GetNumber())
        itemMc = ASObject(arg[3][1])
        if itemMc:
            p = BigWorld.player()
            sType = self.getCurSlotType()
            slotId = sType * const.CARD_SLOT_DIV_NUM + index + 1
            slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
            slotNum = self.cardBag.get('slotNum', {}).get(sType, 0)
            itemMc.sIndex = index
            itemMc.slotId = slotId
            if self.isLockSlot(slotId):
                itemMc.gotoAndStop('lock')
                itemMc.icon.fitSize = True
                itemMc.littleIcon.fitSize = True
                itemMc.previewIcon.fitSize = True
                itemMc.icon.loadImage('')
                itemMc.littleIcon.loadImage('')
                itemMc.previewIcon.loadImage('')
                self.uiAdapter.cardSystem.setCardLevel(itemMc, 0)
            elif self.isUnopenSlot(slotId):
                itemMc.gotoAndStop('unopen')
                itemMc.icon.fitSize = True
                itemMc.littleIcon.fitSize = True
                itemMc.previewIcon.fitSize = True
                itemMc.icon.loadImage('')
                itemMc.littleIcon.loadImage('')
                itemMc.previewIcon.loadImage('')
                self.uiAdapter.cardSystem.setCardLevel(itemMc, 0)
            else:
                itemMc.gotoAndStop('normal')
                itemMc.icon.fitSize = True
                itemMc.littleIcon.fitSize = True
                itemMc.previewIcon.fitSize = True
                itemMc.icon.loadImage('')
                itemMc.littleIcon.loadImage('')
                itemMc.previewIcon.loadImage('')
                if slotCardId:
                    itemMc.slotCardId = slotCardId
                    cardObj = p.getCard(slotCardId, tempId=self.tempId)
                    itemData = cardObj.getConfigData()
                    itemMc.icon.loadImage(cardObj.cardIcon)
                    itemMc.littleIcon.loadImage(cardObj.equipIcon)
                    self.uiAdapter.cardSystem.setCardLevel(itemMc, cardObj.advanceLvEx)
                    TipManager.addTipByType(itemMc, tipUtils.TYPE_CARD_TIP, (slotCardId,))
                else:
                    itemMc.slotCardId = 0
                    self.uiAdapter.cardSystem.setCardLevel(itemMc, 0)
            self.setItemPreviewIcon(itemMc)
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleSlotClick, False, 0, True)
            if not self.isDeadSlot(slotId):
                slotType, slotIndex = self.uiAdapter.cardSystem.parseSlotId(self.selectedSlotId)
                isSel = sType == slotType and index + 1 == slotIndex
                itemMc.selectedMc.visible = isSel
                if isSel:
                    self.selectedSlotItem = itemMc

    def refreshScore(self):
        if not self.hasBaseData():
            return False
        slotScore = sum(self.uiAdapter.cardSystem.getValidSlotScores())
        self.widget.scoreTxt.text = int(slotScore)

    def handleTabBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.target
        t.selected = True
        self.refreshSlotList(True)

    def handleSlotClick(self, *arg):
        if not self.hasBaseData():
            return
        e = ASObject(arg[3][0])
        t = e.currentTarget
        p = BigWorld.player()
        slotId = getattr(t, 'slotId', 0)
        if slotId:
            if self.isDeadSlot(slotId):
                if self.canUnlockSlot(slotId):
                    targetType, targetSlotIndex = self.uiAdapter.cardSystem.parseSlotId(slotId)
                    unlockCash = SCD.data.get('unlockCardSlotCash', {}).get((targetType, targetSlotIndex), 0)
                    self.uiAdapter.messageBox.showYesNoMsgBox(gameStrings.CARD_UNLOCK_SLOT_CASH_MSG % (unlockCash,), yesCallback=Functor(p.base.unlockCardSlot, slotId))
                else:
                    p.showGameMsg(GMDD.data.CARD_OPEN_SLOT_LIMIT, ())
            else:
                self.setSelectedSlot(t)
                self.refreshRevertBtn()
                if e.buttonIdx == uiConst.RIGHT_BUTTON and not self.tempId:
                    slotCardId = self.cardBag.get('cardSlots', {}).get(self.selectedSlotId, 0)
                    if slotCardId:
                        p.base.unfixCardFromSlot(self.selectedSlotId)

    def setSelectedSlot(self, slotItem):
        if not slotItem:
            return
        if self.selectedSlotItem and self.selectedSlotId and self.selectedSlotItem.slotId == self.selectedSlotId:
            self.selectedSlotItem.selectedMc.visible = False
        self.selectedSlotId = slotItem.slotId
        self.selectedSlotItem = slotItem
        if self.selectedSlotItem:
            self.selectedSlotItem.selectedMc.visible = True
        if self.selectedSlotId:
            p = BigWorld.player()
            slotCardId = self.cardBag.get('cardSlots', {}).get(self.selectedSlotId, 0)
            if slotCardId:
                self.uiAdapter.cardSystem.selectedCardId = slotCardId
                self.uiAdapter.cardSystem.scrollToCard = slotCardId
        self.refreshCardList()
        self.notifySlotSelected()

    def getListMc(self):
        if not self.hasBaseData():
            return (None, None)
        else:
            p = BigWorld.player()
            sType = self.getCurSlotType()
            equipSlot = self.cardBag.get('equipSlot', 0)
            curList = self.widget.curSlotList if equipSlot == sType else self.widget.backupSlotList
            otherList = self.widget.curSlotList if equipSlot != sType else self.widget.backupSlotList
            return (curList, otherList)

    def refreshPropertyList(self):
        if not self.hasBaseData():
            return
        self.widget.propertyList.dataArray = self.getSuitPropertyDesc()
        self.widget.nullTxt.visible = not bool(self.widget.propertyList.dataArray)

    def refreshRevertBtn(self):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        slotCardId = self.cardBag.get('cardSlots', {}).get(self.selectedSlotId, 0)
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()

    def handleRevertBtnClick(self, *arg):
        p = BigWorld.player()
        slotCardId = self.cardBag.get('cardSlots', {}).get(self.selectedSlotId, 0)
        selCardId = self.uiAdapter.cardSystem.getCurSelCardId()
        isEqual = selCardId == slotCardId
        if isEqual:
            p.base.unfixCardFromSlot(self.selectedSlotId)
        else:
            self.fixCard(selCardId)

    @ui.checkInventoryLock()
    def replaceAndFixSlot(self, cardId, slotIndex):
        slotName = SCD.data.get('CARD_SYSTEM_SLOT_NAME_%d' % (slotIndex,), '')
        p = BigWorld.player()
        cipher = p.cipherOfPerson
        self.uiAdapter.messageBox.showYesNoMsgBox(gameStrings.CARD_SLOT_COMPOUND_REPLACE_CONFIRM_MESSAGE % slotName, yesCallback=Functor(p.base.compoundCard, cardId, cipher, 0, const.CARD_COMPOUND_TYPE_REPLACE))

    def handleActivateBtnClick(self, *arg):
        if not self.hasBaseData():
            return
        sType = self.getCurSlotType()
        p = BigWorld.player()
        p.base.setEquipSlot(sType)

    def fixCard(self, cardId):
        if self.tempId:
            return
        p = BigWorld.player()
        cardObj = p.getCard(cardId, tempId=self.tempId)
        if cardObj:
            targetType, targetSlotIndex = self.uiAdapter.cardSystem.parseSlotId(self.selectedSlotId)
            if not cardObj.actived:
                return
            if self.isDeadSlot(self.selectedSlotId):
                return
            p.base.fixCardToSlot(cardId, self.selectedSlotId)

    def isLockSlot(self, slotId):
        targetType, targetSlotIndex = self.uiAdapter.cardSystem.parseSlotId(slotId)
        slotNum = self.cardBag.get('slotNum', {}).get(targetType, 0)
        if targetSlotIndex == slotNum + 1:
            return True
        return False

    def isUnopenSlot(self, slotId):
        targetType, targetSlotIndex = self.uiAdapter.cardSystem.parseSlotId(slotId)
        slotNum = self.cardBag.get('slotNum', {}).get(targetType, 0)
        if targetSlotIndex > slotNum + 1:
            return True
        return False

    def isDeadSlot(self, slotId):
        return self.isUnopenSlot(slotId) or self.isLockSlot(slotId)

    def canUnlockSlot(self, slotId):
        return self.isLockSlot(slotId)

    def getSuitPropertyDesc(self):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        sceneType = p.getCardSceneType()
        propertyData = []
        sType = self.getCurSlotType()
        suitInfo = self.getPskillEffects(sType)
        equipSlot = self.cardBag.get('equipSlot', 0)
        propType = 0
        curSuitId, curSuitRank = self.cardBag.get('equipSuit', {}).get(sType, (0, 0))
        if not gameglobal.rds.configData.get('enableChangeCardSuit', 0):
            for k, v in suitInfo.iteritems():
                suitData = CSD.data.get(k, {})
                propType = suitData.get('propType', 0)
                titleName = suitData.get('name', '')
                info = {'label': titleName,
                 'iconType': 0}
                propertyData.append(info)
                for eff, lv in v:
                    sname = PDD.data.get((eff, lv), {}).get('desc', '')
                    info = {'label': sname,
                     'iconType': 1}
                    propertyData.append(info)

                info = {'label': '  ',
                 'iconType': 0}
                propertyData.append(info)

        else:
            suitData = CSD.data.get((curSuitId, curSuitRank), {})
            propType = suitData.get('propType', 0)
            effect = suitInfo.get((curSuitId, curSuitRank), ())
            for eff, lv in effect:
                sname = PDD.data.get((eff, lv), {}).get('desc', '')
                info = {'label': sname,
                 'iconType': 1}
                propertyData.append(info)

            if propertyData:
                info = {'label': '  ',
                 'iconType': 0}
                propertyData.append(info)
        descName = ''
        if propertyData:
            if equipSlot == sType:
                if propType == sceneType:
                    descName = gameStrings.CARD_VALID_SUIT_IN_SCENE_TXT
                else:
                    descName = gameStrings.CARD_VALID_SUIT_NOT_IN_SCENE_TXT
            else:
                descName = gameStrings.CARD_INVALID_SUIT_TXT
        elif equipSlot == sType:
            descName = gameStrings.CARD_VALID_SUIT_IN_SCENE_TXT
        else:
            descName = gameStrings.CARD_INVALID_SUIT_TXT
        self.widget.propListTitle.htmlText = descName
        return propertyData

    def getPskillEffects(self, equipType):
        equipTypes, suitRankDict = self.getEquipedCardTypesAndRank(equipType)
        suitInfo = {}
        school = self.cardBag.get('school', 0)
        for (suitId, rank), cData in CSD.data.iteritems():
            compose = cData.get('compose', ())
            suitRank = suitRankDict.get(compose, -1)
            if suitRank != rank:
                continue
            if set(compose) == set(equipTypes) & set(compose):
                effects = []
                suitEffect = cData.get('effect', [])
                for effectDict in suitEffect:
                    effect = effectDict.get(school, None)
                    if not effect:
                        effect = effectDict.get(0, None)
                    if effect:
                        effects.append(effect)

                suitInfo[suitId, rank] = effects

        return suitInfo

    def getEquipedCardTypesAndRank(self, equipSlot = None):
        p = BigWorld.player()
        if not equipSlot:
            equipSlot = self.cardBag.get('equipSlot', 0)
        cardSlots = self.cardBag.get('cardSlots', 0)
        equipedCardTypes = []
        suitRankDict = {}
        slotIdBegin = equipSlot * const.CARD_SLOT_DIV_NUM + 1
        slotNumMax = SCD.data.get('cardSlotNowMaxNum', const.CARD_SLOT_NOW_MAX_NUM)
        slotIdEnd = slotIdBegin + slotNumMax
        for slotId in xrange(slotIdBegin, slotIdEnd):
            cardId = cardSlots.get(slotId, 0)
            if cardId:
                cardObj = p.getCard(cardId, tempId=self.tempId)
                equipType = BCD.data.get(cardId, {}).get('equipType', 0)
                if equipType:
                    for compose, v in CCTSD.data.iteritems():
                        if equipType in compose:
                            suitRank = suitRankDict.get(compose, -1)
                            suitRank = cardObj.advanceLvEx if suitRank > cardObj.advanceLvEx or suitRank == -1 else suitRank
                            suitRankDict[compose] = suitRank

                    equipedCardTypes.append(equipType)

        return (equipedCardTypes, suitRankDict)

    def onCompoundCard(self, cardId, costFragment, param):
        if not self.hasBaseData():
            return

    def handleMoreBtnClick(self, *arg):
        gameglobal.rds.ui.cardSuit.show()

    def handleBuffListenerSettingBtnClick(self, *arg):
        gameglobal.rds.ui.buffListenerSetting.show()

    def setPreviewIcon(self, compose):
        if not self.hasBaseData():
            return
        self.previewCompose = compose
        self.calcPreviewCompose()
        items = self.widget.curSlotList.items
        for itemMc in items:
            self.setItemPreviewIcon(itemMc)

        self.notifySlotSelected()

    def setItemPreviewIcon(self, itemMc):
        if not itemMc:
            return
        index = itemMc.sIndex
        itemMc.previewEquipType = 0
        itemMc.previewIcon.visible = False
        if self.previewCompose:
            if itemMc.slotCardId not in self.rightEquipTypeCardIds:
                for eType in self.previewCompose:
                    if eType not in self.excludeCompose:
                        iconId = CETD.data.get(eType, {}).get('icon', 'notFound')
                        itemMc.previewIcon.loadImage(''.join(('card/cardtype/', str(iconId), '.dds')))
                        itemMc.previewEquipType = eType
                        self.excludeCompose.append(eType)
                        itemMc.previewIcon.visible = True
                        break

    def calcPreviewCompose(self):
        p = BigWorld.player()
        self.excludeCompose = []
        self.rightEquipTypeCardIds = []
        sType = self.getCurSlotType()
        slotIdDefault = sType * const.CARD_SLOT_DIV_NUM
        slotNum = self.cardBag.get('slotNum', {}).get(sType, 0)
        for slotId in xrange(slotIdDefault + 1, slotIdDefault + slotNum + 1):
            slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
            cardObj = p.getCard(slotCardId)
            if cardObj:
                if cardObj.equipType in self.previewCompose and cardObj.equipType not in self.excludeCompose:
                    self.rightEquipTypeCardIds.append(cardObj.id)
                    self.excludeCompose.append(cardObj.equipType)

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def showTemplate(self, tempId):
        self.uiAdapter.cardSystem.show(TAB_INDEX_CARD_SLOT, tempId=tempId)

    def getCardSlotPropType(self, cardSlotId):
        p = BigWorld.player()
        curFSPropType = const.CARD_SCENE_TYPE_NONE
        slotNum = self.cardBag.get('slotNum', {}).get(cardSlotId, 0)
        for j in xrange(1, slotNum + 1):
            slotId = cardSlotId * const.CARD_SLOT_DIV_NUM + j
            slotCardId = self.cardBag.get('cardSlots', {}).get(slotId, 0)
            cardObj = p.getCard(slotCardId, tempId=self.tempId)
            if cardObj:
                curFSPropType = cardObj.propType
                break

        return curFSPropType

    def getAllCardSlotScore(self):
        slotScoreList = []
        for slotId, _ in self.cardBag.get('equipSuit').iteritems():
            slotScore = sum(self.uiAdapter.cardSystem.getCardSlotScores(slotId))
            slotScoreList.append([slotId, slotScore])

        slotScoreList.sort(cmp=lambda data1, data2: cmp(data1[1], data2[1]), reverse=True)
        return slotScoreList

    def getFirstSecondSlotScore(self):
        allCardSlotScoreList = self.getAllCardSlotScore()
        curFirstScore = allCardSlotScoreList[0][1]
        curSecondScore = allCardSlotScoreList[1][1]
        return (curFirstScore, curSecondScore)

    def isCardSlotResonanceEnable(self):
        p = BigWorld.player()
        slotScoreList = self.getAllCardSlotScore()
        curFirstScoreCardSlotId = slotScoreList[0][0]
        curSecondScoreCardSlotId = slotScoreList[1][0]
        curFSPropType = self.getCardSlotPropType(curFirstScoreCardSlotId)
        curSSPropType = self.getCardSlotPropType(curSecondScoreCardSlotId)
        if set(list([curFSPropType, curSSPropType])) == const.CARD_SLOT_RESONANCE_VALID_SET:
            return (True, [])
        elif not curFSPropType and not curSSPropType:
            return (False, [const.CARD_SCENE_TYPE_NULIN, const.CARD_SCENE_TYPE_DISHE])
        else:
            lackPropTypeList = list()
            if curFSPropType != const.CARD_SCENE_TYPE_NULIN and curSSPropType != const.CARD_SCENE_TYPE_NULIN:
                lackPropTypeList.append(const.CARD_SCENE_TYPE_NULIN)
            if curFSPropType != const.CARD_SCENE_TYPE_DISHE and curSSPropType != const.CARD_SCENE_TYPE_DISHE:
                lackPropTypeList.append(const.CARD_SCENE_TYPE_DISHE)
            return (False, lackPropTypeList)

    def getCurNextCardSlotResonanceData(self):
        curFirstScore, curSecondScore = self.getFirstSecondSlotScore()
        resonanceEnable, lackPropTypeList = self.isCardSlotResonanceEnable()
        if not resonanceEnable:
            curSecondScore = 0
        curTempMaxFirstScore = 0
        curTempMaxSecondScore = 0
        curResonanceIdx = 0
        curResonanceData = dict()
        for idx, resonanceData in CSRD.data.iteritems():
            if curTempMaxFirstScore < resonanceData['firstScore'] <= curFirstScore and curTempMaxSecondScore < resonanceData['secondScore'] <= curSecondScore:
                curTempMaxFirstScore = resonanceData['firstScore']
                curTempMaxSecondScore = resonanceData['secondScore']
                curResonanceData = resonanceData
                curResonanceIdx = idx

        if not curResonanceIdx or not curResonanceData:
            return (None, CSRD.data.get(1, {}))
        elif not CSRD.data.get(curResonanceIdx + 1, {}):
            return (curResonanceData, None)
        else:
            return (curResonanceData, CSRD.data.get(curResonanceIdx + 1, {}))

    def getCurCardSlotResonanceScore(self):
        curResonanceData, nextResonanceData = self.getCurNextCardSlotResonanceData()
        if not curResonanceData:
            return 0
        return curResonanceData.get('resonanceScore', 0)

    def showResonancePanelBtn(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableCardSlotResonance', False):
            self.widget.resonancePanelBtn.visible = False
            return
        self.widget.resonancePanelBtn.label = gameStrings.CARD_SLOT_RESONANCE_NAME
        self.widget.resonancePanelBtn.visible = True
        lvLimit = SCD.data.get('cardSlotResonanceLvLimit', 70)
        if p.lv >= lvLimit:
            self.widget.resonancePanelBtn.disabled = False
            self.widget.resonancePanelBtn.addEventListener(events.BUTTON_CLICK, self.handleOpenResonancePanel, False, 0, True)
            self.widget.resonancePanel.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseResonancePanel, False, 0, True)
            RedPotManager.addRedPot(self.widget.resonancePanelBtn, uiConst.CARDSLOT_RESONANCE_RED_POT, (self.widget.resonancePanelBtn.width - 7, -4))
        else:
            TipManager.addTip(self.widget.resonancePanelBtn, gameStrings.LEVEL_LIMIT_OPEN % lvLimit)
            self.widget.resonancePanelBtn.disabled = True

    def handleOpenResonancePanel(self, *args):
        self.isResonancePanelOpening = not self.isResonancePanelOpening
        self.openResonancePanel(self.isResonancePanelOpening)

    def handleCloseResonancePanel(self, *args):
        self.isResonancePanelOpening = False
        self.openResonancePanel(self.isResonancePanelOpening)

    def refreshResonancePanel(self):
        self.openResonancePanel(self.isResonancePanelOpening)

    def openResonancePanel(self, show):
        if not self.widget:
            return
        panel = self.widget.resonancePanel
        panel.visible = show
        if not show:
            return
        panel.title.text = gameStrings.CARD_SLOT_RESONANCE_NAME
        panel.helpIcon.helpKey = SCD.data.get('cardSlotResonanceHelpKey', 0)
        mainContent = panel.getChildByName('mainContent')
        if not mainContent:
            mainContent = self.widget.getInstByClsName('flash.display.MovieClip')
            mainContent.name = 'mainContent'
            panel.addChild(mainContent)
        else:
            while mainContent.numChildren > 0:
                mainContent.removeChildAt(0)

        mainContent.x = RESONANCE_START_POS_X
        mainContent.y = RESONANCE_START_POS_Y
        curResonanceData, nextResonanceData = self.getCurNextCardSlotResonanceData()
        panel.resonanceScoreTxt.text = gameStrings.CARD_SLOT_RESONANCE_SCORE_NAME % math.floor(self.getCurCardSlotResonanceScore())
        curPosY = 0
        if not curResonanceData:
            curPosY = self.allResonanceDetailContent(False, curPosY + 5, mainContent, nextResonanceData)
        elif not nextResonanceData:
            curPosY = self.allResonanceDetailContent(True, curPosY, mainContent, curResonanceData)
        else:
            curPosY = self.allResonanceDetailContent(True, curPosY, mainContent, curResonanceData)
            curPosY = self.addResonanceNextMc(curPosY, mainContent)
            curPosY = self.allResonanceDetailContent(False, curPosY + 5, mainContent, nextResonanceData)
        panel.bgImage.height = RESONANCE_PANEL_BGIMG_INIT_HEIGHT + curPosY

    def addMCChild(self, parent, child, x, y, width = None, height = None):
        parent.addChild(child)
        child.x = x
        child.y = y
        if width:
            child.width = width
        if height:
            child.height = height
        return child.y + child.height

    def allResonanceDetailContent(self, isCurrent, curPosY, mainContent, resonanceData):
        isCurTxt = 'current' if isCurrent else 'next'
        startPosY = curPosY
        title = self.widget.getInstByClsName('CardSlot_ResonanceTitle')
        title.text.gotoAndStop(isCurTxt)
        title.logo.gotoAndStop(isCurTxt)
        title.text.text.text = resonanceData.get('name', '')
        curPosY = self.addMCChild(mainContent, title, RESONANCE_BIG_TITLE_POS_X, curPosY)
        curFirstScore, curSecondScore = self.getFirstSecondSlotScore()
        resonanceEnable, lackPropTypeList = self.isCardSlotResonanceEnable()
        if not isCurrent:
            if not resonanceEnable:
                curSecondScore = 0
            unLockContent = self.widget.getInstByClsName('CardSlot_ResonanceUnLockContent')
            firstScoreTxt = gameStrings.CARD_SLOT_RESONANCE_PANEL_UNLOCK_TRUE if curFirstScore >= resonanceData.get('firstScore', 0) else gameStrings.CARD_SLOT_RESONANCE_PANEL_UNLOCK_FALSE
            unLockContent.firstScore.htmlText = firstScoreTxt % (curFirstScore, resonanceData.get('firstScore', 0))
            secondScoreTxt = gameStrings.CARD_SLOT_RESONANCE_PANEL_UNLOCK_TRUE if curSecondScore >= resonanceData.get('secondScore', 0) else gameStrings.CARD_SLOT_RESONANCE_PANEL_UNLOCK_FALSE
            unLockContent.secondScore.htmlText = secondScoreTxt % (curSecondScore, resonanceData.get('secondScore', 0))
            curPosY = self.addMCChild(mainContent, unLockContent, RESONANCE_UNLOCK_POS_X, curPosY)
        for lackPropType in lackPropTypeList:
            lackPropTypeMc = self.widget.getInstByClsName('CardSlot_ResonanceUnLockFailTip')
            lackPropTypeMc.text.text = gameStrings.CARD_SLOT_RESONANCE_PANEL_FAIL_UNLOCK_TIP % gameStrings.CARD_SYSTEM_PROP_TYPE_DESC.get(lackPropType, '')
            curPosY = self.addMCChild(mainContent, lackPropTypeMc, RESONANCE_UNLOCK_POS_X, curPosY)

        curPosY = self.addResonanceItemList(curPosY, mainContent, gameStrings.CARD_SLOT_RESONANCE_PANEL_SOMMONED_SPRITE_IN_COMBAT_TITLE, resonanceData.get('spriteInCombatProperty', []), isCurrent)
        curPosY = self.addResonanceItemList(curPosY, mainContent, gameStrings.CARD_SLOT_RESONANCE_PANEL_SOMMONED_SPRITE_OUT_COMBAT_TITLE, resonanceData.get('spriteOutCombatProperty', []), isCurrent)
        bgMc = self.widget.getInstByClsName('M12_TongYong_bg')
        bgMc.name = 'bgMc'
        curPosY = self.addMCChild(mainContent, bgMc, 0, startPosY, RESONANCE_BGMC_WIDTH, curPosY - startPosY + 5)
        mainContent.setChildIndex(bgMc, 0)
        return curPosY

    def addResonanceItemList(self, curPosY, mainContent, smallTitleTxt, propertyList, isCurrent):
        smallTitle = self.widget.getInstByClsName('CardSlot_ResonanceSmallTitle')
        smallTitle.text.htmlText = smallTitleTxt
        curPosY = self.addMCChild(mainContent, smallTitle, RESONANCE_SMALL_TITLE_POS_X, curPosY)
        for propItemData in propertyList:
            item = self.widget.getInstByClsName('CardSlot_ResonanceItem')
            if isCurrent:
                item.text.htmlText = gameStrings.CARD_SLOT_RESONANCE_PANEL_CUR_ITEM_TEXT % propItemData
            else:
                item.text.htmlText = gameStrings.CARD_SLOT_RESONANCE_PANEL_NEXT_ITEM_TEXT % propItemData
            curPosY = self.addMCChild(mainContent, item, RESONANCE_ITEM_POS_X, curPosY)

        return curPosY

    def addResonanceNextMc(self, curPosY, mainContent):
        smallTitle = self.widget.getInstByClsName('CardSlot_ResonanceNextStage')
        return self.addMCChild(mainContent, smallTitle, RESONANCE_NEXT_STAGE_POS_X, curPosY)
