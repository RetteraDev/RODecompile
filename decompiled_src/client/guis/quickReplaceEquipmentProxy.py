#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/quickReplaceEquipmentProxy.o
import BigWorld
import uiConst
import gamelog
import gameglobal
import events
import utils
import itemToolTipUtils
import const
from guis.asObject import TipManager
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from callbackHelper import Functor
from guis import ui
from guis import uiUtils
from data import sys_config_data as SCD
MAX_CASE_NUM = 6
MAX_EQUIP_NUM = 14
MAX_SCHEME_ITEM_NUM = 6
ITEM_X = 0
ITEM_START_Y = 0
ITEM_OFFSET_Y = 30
EQUIP_PLACE_EQUIPMENT = 0
EQUIP_PLACE_SUBEQUIPMENT = 1
EQUIP_PLACE_INVENTORY = 2
EQUIP_PLACE_STORAGE = 3

class QuickReplaceEquipmentProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QuickReplaceEquipmentProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_QUICK_REPLACE_QUIPMENT, self.hide)

    def reset(self):
        self.widget = None
        self.allSchemes = {}
        self.schemeList = []
        self.currSchemeNo = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_QUICK_REPLACE_QUIPMENT:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_QUICK_REPLACE_QUIPMENT)

    def show(self):
        if gameglobal.rds.configData.get('enableQuickReplaceEquipmentV2', False):
            gameglobal.rds.ui.quickReplaceEquipmentV2.show()
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_QUICK_REPLACE_QUIPMENT)
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

        self.initCasePanel()
        p.base.queryOneKeyConfigScheme()

    def initCasePanel(self):
        self.widget.casePanel.visible = True
        self.widget.buyPanel.visible = False
        panel = self.widget.casePanel
        for i in xrange(MAX_EQUIP_NUM):
            item = panel.getChildByName('item%d' % i)
            item.lose.visible = False
            item.slot.dragable = False
            item.slot.itemId = 0
            item.slot.setItemSlotData(None)

        while panel.skillList.canvas.numChildren > 0:
            panel.skillList.canvas.removeChildAt(0)

        posY = ITEM_START_Y
        for j in xrange(MAX_SCHEME_ITEM_NUM):
            itemRenderMc = self.widget.getInstByClsName('QuickReplaceEquipment_skillItem')
            panel.skillList.canvas.addChild(itemRenderMc)
            itemRenderMc.x = ITEM_X
            itemRenderMc.y = posY
            posY += ITEM_OFFSET_Y
            itemRenderMc.index = j
            itemRenderMc.name = 'item%d' % j
            itemRenderMc.title.text = gameStrings.SCHEME_TITLE_DICT.get(j + 1, '')
            itemRenderMc.notUse.visible = False
            itemRenderMc.value.addEventListener(events.MOUSE_CLICK, self.handleClickChooseScheme, False, 0, True)

        panel.applyBtn.addEventListener(events.MOUSE_CLICK, self.handleClickApplyBtn, False, 0, True)
        panel.synBtn.addEventListener(events.MOUSE_CLICK, self.handleClickSynBtn, False, 0, True)

    def setSchemeInfo(self, currSchemeNo, schemes):
        if gameglobal.rds.configData.get('enableQuickReplaceEquipmentV2', False):
            gameglobal.rds.ui.quickReplaceEquipmentV2.setSchemeInfo(currSchemeNo, schemes)
            return
        self.currSchemeNo = currSchemeNo
        self.schemeList = schemes

    def refreshInfo(self):
        if gameglobal.rds.configData.get('enableQuickReplaceEquipmentV2', False):
            gameglobal.rds.ui.quickReplaceEquipmentV2.refreshInfo()
            return
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
        if gameglobal.rds.configData.get('enableQuickReplaceEquipmentV2', False):
            gameglobal.rds.ui.quickReplaceEquipmentV2.addSingleSchemeInfo(schemeNo, scheme)
            return
        for schemeInfo in self.schemeList:
            index = schemeInfo[0]
            if index == schemeNo:
                self.schemeList.remove(schemeInfo)

        self.schemeList.append(scheme)
        self.allSchemes[schemeNo] = scheme
        self.refreshInfo()

    def refreshSchemePanel(self):
        self.initCasePanel()
        self.widget.casePanel.visible = True
        self.widget.buyPanel.visible = False
        panel = self.widget.casePanel
        scheme = self.allSchemes.get(self.currSchemeNo)
        self.equipLoseNum = 0
        if scheme:
            for i in xrange(MAX_EQUIP_NUM):
                item = panel.getChildByName('item%d' % i)
                equipSchemeInfo = scheme.get(uiConst.ONEKEYCONFIG_CONTENT_ID_EQUIP)
                equipInfo = equipSchemeInfo.get(uiConst.EQU_PART_MAIN[i])
                if equipInfo:
                    equipId = equipInfo[1]
                    euipUUID = equipInfo[0]
                    item.slot.itemId = equipId
                    it, place = self.checkEquipByUUID(euipUUID)
                    if not item:
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
                    else:
                        item.lose.visible = True
                        item.slot.setItemSlotData(uiUtils.getGfxItemById(equipId, 1))
                        item.slot.validateNow()
                        TipManager.removeTip(item.slot)
                        self.equipLoseNum += 1

            for idx in xrange(MAX_SCHEME_ITEM_NUM):
                schemeItem = self.widget.casePanel.skillList.canvas.getChildByName('item%d' % idx)
                schemeIndex = scheme.get(idx + 1, 0)
                curNo, name = self.getSchemeNameByIndex(schemeItem.index + 1, schemeIndex)
                schemeItem.value.label = name
                schemeItem.notUse.visible = curNo != schemeIndex

        else:
            self.initCasePanel()

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
        self.widget.casePanel.visible = False
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
        e = ASObject(args[3][0])
        btn = e.currentTarget
        type = btn.type
        msg = gameStrings.BUY_NEW_EXTRA_SCHEME_MSG
        costList = SCD.data.get('enableOneKeyConfigSchemedData', (400000, 600000, 800000, 1000000))
        cost = costList[type - 2]
        bonusIcon = {'bonusType': 'bindCash',
         'value': str(cost)}
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(BigWorld.player().cell.enableOneKeyConfigSchemeOnCell, self.currSchemeNo), yesBtnText=gameStrings.COMMON_CONFIRM, noBtnText=gameStrings.COMMON_CANCEL, bonusIcon=bonusIcon, style=uiConst.MSG_BOX_BUY_ITEM)

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

    def handleClickApplyBtn(self, *args):
        if self.equipLoseNum >= SCD.data.get('equipLoseNum', 5) and not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_APPLY_ONEKEY_SCHREME, False):
            msg = gameStrings.CHANGE_SCHEME_EQUIP_LOSE_MSG
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.applyScheme, isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_APPLY_ONEKEY_SCHREME)
        else:
            self.applyScheme()

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
