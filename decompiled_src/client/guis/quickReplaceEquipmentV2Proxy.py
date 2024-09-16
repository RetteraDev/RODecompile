#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/quickReplaceEquipmentV2Proxy.o
import BigWorld
import uiConst
import gamelog
import gameglobal
import events
import utils
import itemToolTipUtils
import const
import copy
from guis.asObject import TipManager
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from callbackHelper import Functor
from guis import ui
from item import Item
from guis import uiUtils
from data import sys_config_data as SCD
from cdata import wen_yin_data as WYD
from cdata import game_msg_def_data as GMDD
MAX_CASE_NUM = 6
MAX_EQUIP_NUM = 14
MAX_SCHEME_ITEM_NUM = 6
CONFIG_ITEM_X = 0
CONFIG_ITEM_START_Y = 0
CONFIG_ITEM_OFFSET_Y = 30
FUWEN_MAX_SLOT_NUM = 5
WENYIN_MAX_SLOT_NUM = 7
GEM_MAX_CNT = 6
EQUIP_PLACE_EQUIPMENT = 0
EQUIP_PLACE_SUBEQUIPMENT = 1
EQUIP_PLACE_INVENTORY = 2
EQUIP_PLACE_STORAGE = 3
TABLE_BTN_NAME_EQUIP = 'equipTabBtn'
TABLE_BTN_NAME_CONFIG = 'configTabBtn'
TABLE_BTN_NAME_FUWEN = 'fuwenTabBtn'
TABLE_BTN_NAME_HIEROGRAM = 'hierogramTabBtn'
TABLE_BTN_NAME_CARD = 'cardTabBtn'
TABLE_BTN_NAME_GEM = 'gemTabBtn'
tabBtnList = {TABLE_BTN_NAME_EQUIP: 'equipPanel',
 TABLE_BTN_NAME_CONFIG: 'configPanel',
 TABLE_BTN_NAME_FUWEN: 'fuwenPanel',
 TABLE_BTN_NAME_HIEROGRAM: 'hierogramPanel',
 TABLE_BTN_NAME_CARD: 'cardPanel',
 TABLE_BTN_NAME_GEM: 'gemPanel'}
SUB_TAB_MAP = {1: TABLE_BTN_NAME_EQUIP,
 2: TABLE_BTN_NAME_CONFIG,
 3: TABLE_BTN_NAME_FUWEN,
 4: TABLE_BTN_NAME_HIEROGRAM,
 5: TABLE_BTN_NAME_CARD,
 6: TABLE_BTN_NAME_GEM}
SUB_TAB_LIST = [TABLE_BTN_NAME_EQUIP,
 TABLE_BTN_NAME_CONFIG,
 TABLE_BTN_NAME_FUWEN,
 TABLE_BTN_NAME_HIEROGRAM,
 TABLE_BTN_NAME_CARD,
 TABLE_BTN_NAME_GEM]
TAB_IN_USE = [TABLE_BTN_NAME_EQUIP, TABLE_BTN_NAME_FUWEN, TABLE_BTN_NAME_GEM]

class QuickReplaceEquipmentV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QuickReplaceEquipmentV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_QUICK_REPLACE_QUIPMENT_V2, self.hide)

    def reset(self):
        self.widget = None
        self.allSchemes = {}
        self.schemeList = []
        self.currSchemeNo = 0
        self.selectTabBtnName = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_QUICK_REPLACE_QUIPMENT_V2:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_QUICK_REPLACE_QUIPMENT_V2)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_QUICK_REPLACE_QUIPMENT_V2)
        else:
            self.initUI()
        BigWorld.player().base.afterClickOneKeyConfigPush()

    def initUI(self):
        p = BigWorld.player()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.chooseList.btn0.gotoAndStop('used')
        self.widget.chooseList.btn0.tfInput.visible = False
        self.widget.chooseList.btn3.visible = False
        self.widget.chooseList.btn4.visible = False
        self.widget.chooseList.btn5.visible = False
        for schemeNo in xrange(MAX_CASE_NUM):
            btn = self.widget.chooseList.getChildByName('btn%d' % schemeNo)
            btn.special.visible = False

        schemePanel = self.widget.schemePanel
        schemePanel.visible = False
        posX = 281
        enableTab = self.getEnableTab()
        for tabBtn in SUB_TAB_LIST:
            btn = schemePanel.getChildByName(tabBtn)
            btn.visible = False
            if tabBtn in enableTab:
                btn.x = posX
                posX += 70
                btn.visible = True
                btn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick, False, 0, True)

        self.widget.schemePanel.synBtn.addEventListener(events.MOUSE_CLICK, self.handleClickSingleSynBtn, False, 0, True)
        self.widget.applyBtn.addEventListener(events.MOUSE_CLICK, self.handleClickApplyBtn, False, 0, True)
        self.selectTabBtnName = TABLE_BTN_NAME_EQUIP
        self.initEquipPanel()
        p.base.queryOneKeyConfigScheme()

    def getEnableTab(self):
        enableTab = copy.copy(TAB_IN_USE)
        if not gameglobal.rds.configData.get('enableGuanYinOneKeyScheme', False):
            if TABLE_BTN_NAME_FUWEN in enableTab:
                enableTab.remove(TABLE_BTN_NAME_FUWEN)
        if not gameglobal.rds.configData.get('enableWenYinOneKeyScheme', False):
            if TABLE_BTN_NAME_GEM in enableTab:
                enableTab.remove(TABLE_BTN_NAME_GEM)
        if not gameglobal.rds.configData.get('enableEquipOneKeyScheme', False):
            if TABLE_BTN_NAME_EQUIP in enableTab:
                enableTab.remove(TABLE_BTN_NAME_EQUIP)
        return enableTab

    def initEquipPanel(self):
        self.widget.buyPanel.visible = False
        panel = self.widget.schemePanel.equipPanel
        panel.equipTitle.desc.text = gameStrings.SCHEME_EQUIP_TITLE
        panel.configTitle.desc.text = gameStrings.SCHEME_CONGIF_TITLE
        for i in xrange(MAX_EQUIP_NUM):
            item = panel.getChildByName('item%d' % i)
            item.lose.visible = False
            item.lookup.visible = False
            item.slot.dragable = False
            item.slot.itemId = 0
            item.slot.setItemSlotData(None)

        while panel.configList.canvas.numChildren > 0:
            panel.configList.canvas.removeChildAt(0)

        posY = CONFIG_ITEM_START_Y
        for j in xrange(MAX_SCHEME_ITEM_NUM):
            itemRenderMc = self.widget.getInstByClsName('QuickReplaceEquipment_skillItem')
            panel.configList.canvas.addChild(itemRenderMc)
            itemRenderMc.x = CONFIG_ITEM_X
            itemRenderMc.y = posY
            posY += CONFIG_ITEM_OFFSET_Y
            itemRenderMc.index = j
            itemRenderMc.name = 'item%d' % j
            itemRenderMc.title.text = gameStrings.SCHEME_TITLE_DICT.get(j + 1, '')
            itemRenderMc.notUse.visible = False
            itemRenderMc.value.addEventListener(events.MOUSE_CLICK, self.handleClickChooseScheme, False, 0, True)

    def awakeItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])

    def setSchemeInfo(self, currSchemeNo, schemes):
        self.currSchemeNo = currSchemeNo
        self.schemeList = schemes

    def refreshInfo(self):
        if not self.widget:
            return
        for schemeNo in xrange(MAX_CASE_NUM):
            btn = self.widget.chooseList.getChildByName('btn%d' % schemeNo)
            btn.type = schemeNo
            btn.special.visible = btn.type == uiConst.ONEKEYCONFIG_SCHEME_ID_SPECIAL
            btn.addEventListener(events.MOUSE_CLICK, self.handleClickBtn, False, 0, True)
            btn.state = 'notuse'
            btn.gotoAndStop('notuse')
            btn.notuse.selected = schemeNo == self.currSchemeNo
            for scheme in self.schemeList:
                if schemeNo == scheme[0]:
                    btn.state = 'used'
                    btn.gotoAndStop('used')
                    btn.used.selected = schemeNo == self.currSchemeNo
                    btn.tf.text = scheme[2] if scheme[2] else gameStrings.INIT_SCHEME_TITLE
                    ASUtils.setHitTestDisable(btn.tf, True)
                    status = scheme[3]
                    expireTime = scheme[4]
                    if scheme[0] == uiConst.ONEKEYCONFIG_SCHEME_ID_SPECIAL and status == const.SCHEME_STATUS_DISABLE:
                        btn.state = 'notuse'
                        btn.gotoAndStop('notuse')
                        break
                    btn.tfInput.visible = False
                    btn.changeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickChangeName, False, 0, True)
                    self.allSchemes[schemeNo] = scheme[1]
                    nextBtn = self.widget.chooseList.getChildByName('btn%d' % (schemeNo + 1))
                    if nextBtn:
                        nextBtn.visible = True
                    break

        self.refreshSchemePanel()

    def addSingleSchemeInfo(self, schemeNo, scheme):
        for schemeInfo in self.schemeList:
            index = schemeInfo[0]
            if index == schemeNo:
                self.schemeList.remove(schemeInfo)

        self.schemeList.append(scheme)
        if len(scheme) > 1:
            self.allSchemes[schemeNo] = scheme[1]
        self.refreshInfo()

    def refreshSchemePanel(self):
        if not self.widget:
            return
        self.widget.schemePanel.visible = True
        self.widget.buyPanel.visible = False
        for i, btnName in enumerate(tabBtnList):
            tabBtn = self.widget.schemePanel.getChildByName(btnName)
            panelMc = self.widget.schemePanel.getChildByName(tabBtnList[btnName])
            if btnName == self.selectTabBtnName:
                tabBtn.selected = True
                if panelMc:
                    panelMc.visible = True
                    self.widget.schemePanel.visible = True
                    self.updateSelectTabMc(panelMc)
            else:
                tabBtn.selected = False
                if panelMc:
                    panelMc.visible = False

    def updateSelectTabMc(self, panelMc):
        if panelMc.name == 'cardPanel':
            self.updateCardPanel()
        elif panelMc.name == 'configPanel':
            self.updateConfigPanel()
        elif panelMc.name == 'fuwenPanel':
            self.updateFuwenPanel()
        elif panelMc.name == 'hierogramPanel':
            self.updateHierogramPanel()
        elif panelMc.name == 'gemPanel':
            self.updateGemPanel()
        else:
            self.updateEquipPanel()

    def handleTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        btnName = e.currentTarget.name
        self.setTabSelected(btnName)

    def setTabSelected(self, btnName):
        if btnName != self.selectTabBtnName:
            self.selectTabBtnName = btnName
            self.refreshSchemePanel()

    def updateEquipPanel(self):
        panel = self.widget.schemePanel.equipPanel
        scheme = self.allSchemes.get(self.currSchemeNo, {})
        self.equipLoseNum = 0
        self.initEquipPanel()
        if scheme and scheme.get(uiConst.ONEKEYCONFIG_CONTENT_ID_EQUIP):
            equipSchemeInfo = scheme.get(uiConst.ONEKEYCONFIG_CONTENT_ID_EQUIP)
            for i in xrange(MAX_EQUIP_NUM):
                item = panel.getChildByName('item%d' % i)
                equipInfo = equipSchemeInfo.get(uiConst.EQU_PART_MAIN[i])
                if equipInfo:
                    equipId = equipInfo[1]
                    euipUUID = equipInfo[0]
                    item.slot.itemId = equipId
                    it, place = self.checkEquipByUUID(euipUUID)
                    if not it:
                        item.lose.visible = False
                        item.slot.setItemSlotData(None)
                    elif place == EQUIP_PLACE_EQUIPMENT:
                        item.lose.visible = False
                        iconPath = uiUtils.getItemIconFile64(it.id)
                        itemInfo = {'iconPath': iconPath,
                         'overIconPath': iconPath,
                         'color': uiUtils.getItemColorByItem(it),
                         'state': gameglobal.rds.ui.roleInfo.calcSlotState(it, False),
                         'cornerMark': itemToolTipUtils.getCornerMark(it),
                         'uuid': euipUUID.encode('hex'),
                         'location': const.ITEM_IN_EQUIPMENT}
                        item.slot.setItemSlotData(itemInfo)
                        ASUtils.setHitTestDisable(item.lookup, True)
                        item.addEventListener(events.MOUSE_ROLL_OVER, self.onItemMouseOver, False, 0, True)
                        item.addEventListener(events.MOUSE_ROLL_OUT, self.onItemMouseOut, False, 0, True)
                        item.linkText = 'equip'
                        item.addEventListener(events.MOUSE_CLICK, self.handleClickItem, False, 0, True)
                    else:
                        item.lose.visible = True
                        item.slot.setItemSlotData(uiUtils.getGfxItemById(equipId, 1))
                        item.slot.validateNow()
                        TipManager.removeTip(item.slot)
                        self.equipLoseNum += 1

            for idx in xrange(MAX_SCHEME_ITEM_NUM):
                schemeItem = self.widget.schemePanel.equipPanel.configList.canvas.getChildByName('item%d' % idx)
                schemeIndex = scheme.get(idx + 1, 0)
                curNo, name = self.getSchemeNameByIndex(schemeItem.index + 1, schemeIndex)
                schemeItem.value.label = name
                schemeItem.notUse.visible = curNo != schemeIndex

    def updateConfigPanel(self):
        panel = self.widget.schemePanel.configPanel
        scheme = self.allSchemes.get(self.currSchemeNo, {})
        if scheme:
            for idx in xrange(MAX_SCHEME_ITEM_NUM):
                schemeItem = panel.getChildByName('item%d' % idx)
                schemeItem.index = idx
                schemeItem.title.text = gameStrings.SCHEME_TITLE_DICT.get(idx + 1, '')
                schemeIndex = scheme.get(idx + 1, 0)
                curNo, name = self.getSchemeNameByIndex(idx + 1, schemeIndex)
                schemeItem.value.label = name
                schemeItem.notUse.visible = curNo != schemeIndex

    def updateFuwenPanel(self):
        panel = self.widget.schemePanel.fuwenPanel
        scheme = self.allSchemes.get(self.currSchemeNo, {})
        fuwenInfo = scheme.get(uiConst.ONEKEYCONFIG_CONTENT_ID_GUANYIN) if scheme else {}
        if scheme and fuwenInfo:
            for slotId in xrange(FUWEN_MAX_SLOT_NUM):
                itemMc = getattr(panel, 'skillItem' + str(slotId))
                itemMc.slot.dragable = False
                itemMc.lookup.visible = False
                slotVal = fuwenInfo.get(slotId)
                bookId = 0
                for part, id in slotVal.iteritems():
                    if id > 0:
                        bookId = id

                if bookId:
                    place = self.checkItemById(bookId)
                    itemMc.lose.visible = place != EQUIP_PLACE_EQUIPMENT
                    itemMc.slot.binding = 'skills20.' + str(bookId)
                    itemInfo = gameglobal.rds.ui.guanYinV3.createSkillInfo(bookId)
                    itemMc.slot.setItemSlotData(itemInfo)
                    itemMc.txtName.text = itemInfo['skillName']
                    ASUtils.setHitTestDisable(itemMc.lookup, True)
                    itemMc.linkText = 'fuwen'
                    itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.onItemMouseOver, False, 0, True)
                    itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.onItemMouseOut, False, 0, True)
                    itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickItem, False, 0, True)
                else:
                    itemMc.lose.visible = False
                    itemMc.slot.setItemSlotData(None)
                    itemMc.txtName.text = ''

        else:
            for slotId in xrange(FUWEN_MAX_SLOT_NUM):
                itemMc = getattr(panel, 'skillItem' + str(slotId))
                itemMc.slot.dragable = False
                itemMc.lose.visible = False
                itemMc.lookup.visible = False
                itemMc.slot.setItemSlotData(None)
                itemMc.txtName.text = ''

    def updateHierogramPanel(self):
        panel = self.widget.schemePanel.hierogramPanel
        scheme = self.allSchemes.get(self.currSchemeNo, {})
        if scheme:
            pass

    def updateCardPanel(self):
        panel = self.widget.schemePanel.cardPanel
        scheme = self.allSchemes.get(self.currSchemeNo, {})
        if scheme:
            pass

    def updateGemPanel(self):
        panel = self.widget.schemePanel.gemPanel
        scheme = self.allSchemes.get(self.currSchemeNo, {})
        gemInfo = scheme.get(uiConst.ONEKEYCONFIG_CONTENT_ID_WENYIN) if scheme else {}
        index = 0
        for partId, partData in WYD.data.iteritems():
            itemMc = getattr(panel, 'item%d' % index)
            itemMc.linkText = 'gem'
            itemMc.addEventListener(events.BUTTON_CLICK, self.handleClickItem, False, 0, True)
            if itemMc:
                itemId = partData.get('showItemId', 999)
                itemName = uiUtils.getItemColorName(itemId)
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId))
                itemMc.label = itemName
                if gemInfo:
                    gemList = gemInfo.get(partId, [])
                    for i in xrange(GEM_MAX_CNT):
                        gemMc = getattr(itemMc, 'gem%d' % i)
                        gType = Item.GEM_TYPE_YANG if i < Item.GEM_SLOT_MAX_CNT else Item.GEM_TYPE_YIN
                        newGemId = gemList[i] if gemList else 0
                        gemSlot = BigWorld.player().wenYin.getGemSlot(partId, gType, i % Item.GEM_SLOT_MAX_CNT)
                        oldGemId = gemSlot.gem.id if gemSlot and gemSlot.isFilled() else 0
                        if newGemId == oldGemId or newGemId == Item.parentId(oldGemId):
                            gemMc.lose.visible = False
                        else:
                            gemMc.lose.visible = True
                        gemMc.slot.dragable = False
                        if len(gemList) > i and gemList[i] > 0:
                            gemMc.slot.setItemSlotData(uiUtils.getGfxItemById(gemList[i], 1))
                        else:
                            gemMc.slot.setItemSlotData(None)
                            gemMc.lose.visible = False

                else:
                    for i in xrange(GEM_MAX_CNT):
                        gemMc = getattr(itemMc, 'gem%d' % i)
                        gemMc.slot.setItemSlotData(None)
                        gemMc.slot.dragable = False
                        gemMc.lose.visible = False

            index += 1

    def checkEquipByUUID(self, UUID):
        place = -1
        item, _ = BigWorld.player().equipment.findEquipByUUID(UUID)
        if item:
            place = EQUIP_PLACE_EQUIPMENT
            return (item, place)
        item, _, _ = BigWorld.player().subEquipment.findItemByUUID(UUID)
        if item:
            place = EQUIP_PLACE_SUBEQUIPMENT
            return (item, place)
        item, _, _ = BigWorld.player().inv.findItemByUUID(UUID)
        if item:
            place = EQUIP_PLACE_INVENTORY
            return (item, place)
        item, _, _ = BigWorld.player().storage.findItemByUUID(UUID)
        if item:
            place = EQUIP_PLACE_STORAGE
            return (item, place)
        return (item, place)

    def checkItemById(self, itemId):
        place = -1
        equipedFuwenList = []
        for slotId, guanYin in BigWorld.player().guanYin.iteritems():
            if guanYin.guanYinStat < 0:
                continue
            part = guanYin.guanYinStat
            if part >= 0 and guanYin.guanYinInfo[part] > 0:
                equipedFuwenList.append(Item.parentId(guanYin.guanYinInfo[part]))

        if itemId in equipedFuwenList:
            place = EQUIP_PLACE_EQUIPMENT
            return place
        page, pos = BigWorld.player().inv.findItemById(itemId)
        if page != const.CONT_NO_PAGE and pos != const.CONT_NO_POS:
            place = EQUIP_PLACE_INVENTORY
            return place
        page, pos = BigWorld.player().storage.findItemById(itemId)
        if page != const.CONT_NO_PAGE and pos != const.CONT_NO_POS:
            place = EQUIP_PLACE_STORAGE
            return place
        return place

    def handleClickItem(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.linkText == 'equip':
            gameglobal.rds.ui.roleInfo.show()
        elif e.currentTarget.linkText == 'fuwen':
            gameglobal.rds.ui.roleInfo.onOpenGuanYin()
        elif e.currentTarget.linkText == 'gem':
            gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_GEM)

    def onItemMouseOver(self, *args):
        itemMc = ASObject(args[3][0]).currentTarget
        if itemMc.lookup and itemMc.slot.data:
            itemMc.lookup.visible = True

    def onItemMouseOut(self, *args):
        itemMc = ASObject(args[3][0]).currentTarget
        if itemMc.lookup:
            itemMc.lookup.visible = False

    def handleClickBtn(self, *args):
        e = ASObject(args[3][0])
        curBtn = e.currentTarget
        type = curBtn.type
        state = curBtn.state
        self.currSchemeNo = type
        for schemeNo in xrange(MAX_CASE_NUM):
            btn = self.widget.chooseList.getChildByName('btn%d' % schemeNo)
            if btn.state == 'used':
                btn.used.selected = type == schemeNo
            else:
                btn.notuse.selected = type == schemeNo

        if state == 'used':
            self.refreshSchemePanel()
        else:
            self.addNewScheme(type)

    def addNewScheme(self, type):
        self.widget.schemePanel.visible = False
        self.widget.buyPanel.visible = True
        if type == uiConst.ONEKEYCONFIG_SCHEME_ID_SPECIAL:
            self.widget.buyPanel.buyDesc.text = gameStrings.BUY_NEW_SPECIAL_SCHEME_DESC
            self.widget.buyPanel.buyBtn.removeEventListener(events.MOUSE_CLICK, self.handleClickBuyExtraScheme)
            self.widget.buyPanel.buyBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBuySpecailScheme, False, 0, True)
        elif type in uiConst.ONEKEYCONFIG_SCHEME_ID_EXTRA:
            self.widget.buyPanel.buyDesc.text = gameStrings.BUY_NEW_EXTRA_SCHEME_DESC
            self.widget.buyPanel.buyBtn.removeEventListener(events.MOUSE_CLICK, self.handleClickBuySpecailScheme)
            self.widget.buyPanel.buyBtn.type = type
            self.widget.buyPanel.buyBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBuyExtraScheme, False, 0, True)

    def handleClickChangeName(self, *args):
        e = ASObject(args[3][0])
        btn = e.currentTarget.parent
        btn.tf.visible = False
        btn.tfInput.visible = True
        btn.tfInput.textField.addEventListener(events.FOCUS_EVENT_FOCUS_IN, self.handleInputFocusIn, False, 0, True)
        btn.tfInput.textField.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.handleInputFocusOut, False, 0, True)
        btn.tfInput.focused = True

    def handleClickBuySpecailScheme(self, *args):
        self.uiAdapter.tianyuMall.showMallTab(10001, 0)

    def handleClickBuyExtraScheme(self, *args):
        p = BigWorld.player()
        e = ASObject(args[3][0])
        btn = e.currentTarget
        type = btn.type
        msg = gameStrings.BUY_NEW_EXTRA_SCHEME_MSG
        costList = SCD.data.get('enableOneKeyConfigSchemedData', (400000, 600000, 800000, 1000000))
        cost = costList[type - 2]
        isCashEnough = p.bindCash + p.cash >= cost
        isBindCashEnough = p.bindCash >= cost
        if isCashEnough and not isBindCashEnough:
            msg = gameStrings.BUY_NEW_EXTRA_SCHEME_USE_CASH_MSG
        bonusIcon = {'bonusType': 'bindCash',
         'value': str(cost)}
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(BigWorld.player().cell.enableOneKeyConfigSchemeOnCell, self.currSchemeNo), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, bonusIcon=bonusIcon)

    def handleInputFocusIn(self, *args):
        e = ASObject(args[3][0])
        btn = e.currentTarget.parent.parent
        oldName = btn.tf.text
        btn.tf.visible = False
        btn.tfInput.visible = True
        btn.tfInput.text = oldName
        btn.tfInput.maxChars = 8

    def handleInputFocusOut(self, *args):
        e = ASObject(args[3][0])
        newName = e.currentTarget.text
        btn = e.currentTarget.parent.parent
        btn.tf.text = newName
        btn.tf.visible = True
        btn.tfInput.visible = False
        BigWorld.player().base.setOneKeyConfigSchemeName(btn.type, newName)

    @ui.checkEquipChangeOpen()
    def handleClickApplyBtn(self, *args):
        if self.equipLoseNum >= SCD.data.get('equipLoseNum', 5) and not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_APPLY_ONEKEY_SCHREME, False):
            msg = gameStrings.CHANGE_SCHEME_EQUIP_LOSE_MSG
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.applyScheme, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_APPLY_ONEKEY_SCHREME)
        else:
            self.applyScheme()

    @ui.checkInventoryLock()
    def handleClickSingleSynBtn(self, *args):
        if self.selectTabBtnName == TABLE_BTN_NAME_EQUIP:
            msg = gameStrings.SYN_SCHEME_EQUIP_MSG
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(BigWorld.player().cell.saveOKCSEquipAndConfig, self.currSchemeNo, BigWorld.player().cipherOfPerson))
        elif self.selectTabBtnName == TABLE_BTN_NAME_FUWEN:
            msg = gameStrings.SYN_SCHEME_FUWEN_MSG
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(BigWorld.player().cell.saveOKCSGuanYin, self.currSchemeNo, BigWorld.player().cipherOfPerson))
        elif self.selectTabBtnName == TABLE_BTN_NAME_GEM:
            msg = gameStrings.SYN_SCHEME_GEM_MSG
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(BigWorld.player().cell.saveOKCSWenYin, self.currSchemeNo, BigWorld.player().cipherOfPerson))

    def applyScheme(self):
        p = BigWorld.player()
        p.saveWSShortcut(self.uiAdapter.actionbar.getClientShortCut())
        gameglobal.rds.ui.roleInfo.resetAddPoint()
        gameglobal.rds.ui.roleInfo.updatePotBtnVisible()
        gameglobal.rds.ui.roleInfo.updateAllPotential()
        p.cell.switchOneKeyConfigScheme(self.currSchemeNo)

    @ui.checkInventoryLock()
    def handleClickSynBtn(self, *args):
        msg = gameStrings.SYN_SCHEME_MSG
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(BigWorld.player().cell.saveOneKeyConfigSchemeOnCell, self.currSchemeNo, BigWorld.player().cipherOfPerson))

    def handleClickChooseScheme(self, *args):
        e = ASObject(args[3][0])
        schemeType = e.target.parent.index
        self.openSchemeChoosePanel(schemeType + 1)

    def getSchemeNameByIndex(self, type, index):
        name = ''
        expireTime = 0
        curNo = -1
        p = BigWorld.player()
        if type == uiConst.ONEKEYCONFIG_CONTENT_ID_WUSHUANG:
            curNo = p.getCurWSSchemeNo()
            name = p.getWSSchemeName(index)
            expireTime = p.getWSSchemeExpireTime(index)
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_PROP:
            curNo = p.curPropScheme
            scheme = p.getPropSchemeById(index)
            if scheme:
                name = scheme.get('schemeName', '')
                expireTime = scheme.get('expireTime', 0)
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_SKILLPOINT:
            curNo = p.skillPointSchemeIndex
            scheme = p.getSkillSchemeById(index)
            name = BigWorld.player().getSkillSchemeName(index)
            if scheme:
                expireTime = scheme[4]
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_SHORTCUT:
            curNo = gameglobal.rds.ui.actionbar.getCurrSchemeNo()
            name = gameStrings.SHORTCUT_SCHEME_NAME % (index + 1)
            expireTime = 0
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_EQUIPSOUL:
            curNo = p.currEquipSoulSchemeNo
            name = p.getEquipSoulSchemeName(index)
            expireTime = p.getEquipSoulSchemeExpireTime(index)
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_CARD:
            curNo = p.cardBag.get('equipSlot', 0)
            if index == 0 or index == 1:
                index = 1
            name = gameStrings.CARD_SCHEME_NAME % index
        if expireTime and expireTime < utils.getNow():
            name += gameStrings.SCHEME_EXPIRE_DESC
        return (curNo, name)

    def openSchemeChoosePanel(self, type):
        if type == uiConst.ONEKEYCONFIG_CONTENT_ID_WUSHUANG:
            gameglobal.rds.ui.schemeSwitch.show(uiConst.SCHEME_SWITCH_WUSHUANG)
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_PROP:
            gameglobal.rds.ui.propScheme.show()
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_SKILLPOINT:
            gameglobal.rds.ui.skillScheme.show()
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_SHORTCUT:
            pass
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_EQUIPSOUL:
            self.uiAdapter.schemeSwitch.show(uiConst.SCHEME_SWITCH_EQUIP_SOUL)
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_CARD:
            gameglobal.rds.ui.cardSystem.show(tabIndex=2)

    def pushOneKeyConfigMessage(self):
        pushId = uiConst.MESSAGE_TYPE_ONEKEY_CONFIG
        if pushId not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': self.onPushMsgClick})

    def removeOneKeyConfigPushMsg(self):
        pushId = uiConst.MESSAGE_TYPE_ONEKEY_CONFIG
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def onPushMsgClick(self):
        if not self.widget:
            msg = gameStrings.ONEKEY_CONFIG_PUSH_MSG
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=gameglobal.rds.ui.actionbar.onChangeEquip)
        self.removeOneKeyConfigPushMsg()
