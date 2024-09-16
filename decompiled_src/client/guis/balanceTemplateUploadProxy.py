#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceTemplateUploadProxy.o
import BigWorld
import gameglobal
import uiConst
import gamelog
import gametypes
import events
import utils
import const
from guis import tipUtils
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from callbackHelper import Functor
from guis import uiUtils
from data import sys_config_data as SCD
MAX_CASE_NUM = 6
MAX_EQUIP_NUM = 14
ITEM_X = 0
ITEM_START_Y = 0
ITEM_OFFSET_Y = 30
SHOW_EQUIP_INDEXS = [0,
 1,
 4,
 3,
 2,
 9,
 6,
 21,
 22,
 7,
 8,
 10,
 23,
 5]
SHOW_SCHEME_INDEXS = [0,
 1,
 2,
 4,
 5]

class BalanceTemplateUploadProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceTemplateUploadProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BALANCE_ARENA_UPLOAD, self.hide)

    def reset(self):
        self.currEquips = {}
        self.currSechemes = {}
        self.itemInfo = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BALANCE_ARENA_UPLOAD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BALANCE_ARENA_UPLOAD)

    def show(self, itemInfo):
        self.itemInfo = itemInfo
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BALANCE_ARENA_UPLOAD)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.setCaseList()
        self.initCasePanel()

    def setCaseList(self):
        p = BigWorld.player()
        for i in xrange(1, MAX_CASE_NUM):
            btn = self.widget.chooseList.getChildByName('btn%d' % i)
            btn.gotoAndStop('used')
            btn.tfInput.focused = False
            btn.visible = False

        defaultBtn = self.widget.chooseList.btn0
        defaultBtn.visible = True
        defaultBtn.gotoAndStop('used')
        defaultBtn.tfInput.visible = False
        defaultBtn.changeBtn.visible = False
        defaultBtn.tf.text = gameStrings.BALANCE_ARENA_UPLOAD_DEFAULT_NAME % p.playerName

    def handleClickChangeName(self, *args):
        e = ASObject(args[3][0])
        btn = e.currentTarget.parent
        btn.tf.visible = False
        btn.tfInput.visible = True
        btn.tfInput.textField.addEventListener(events.FOCUS_EVENT_FOCUS_IN, self.handleInputFocusIn, False, 0, True)
        btn.tfInput.textField.addEventListener(events.FOCUS_EVENT_FOCUS_OUT, self.handleInputFocusOut, False, 0, True)
        btn.tfInput.focused = True

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

    def initCasePanel(self):
        self.widget.casePanel.visible = True
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
        for j in SHOW_SCHEME_INDEXS:
            itemRenderMc = self.widget.getInstByClsName('BalanceTemplateUpload_skillItem')
            panel.skillList.canvas.addChild(itemRenderMc)
            itemRenderMc.x = ITEM_X
            itemRenderMc.y = posY
            posY += ITEM_OFFSET_Y
            itemRenderMc.index = j
            itemRenderMc.name = 'item%d' % j
            itemRenderMc.title.text = gameStrings.SCHEME_TITLE_DICT.get(j + 1, '')
            itemRenderMc.notUse.visible = False

        panel.synBtn.addEventListener(events.MOUSE_CLICK, self.handleClickApplyBtn, False, 0, True)

    def handleClickApplyBtn(self, *args):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.BALANCE_ARENA_UPLOAD_TEAMPLATE_CONFIRM, self.uploadTemplate)

    def uploadTemplate(self):
        if hasattr(self.itemInfo, 'id'):
            gamelog.debug('dxk@balanceTemplateUpload uploadTemplate', self.itemInfo.id)
            p = BigWorld.player()
            p.base.commitCharTemp(gametypes.CHAR_TEMP_TYPE_ARENA, self.itemInfo.id)
        self.hide()

    def getItemTipByIndex(self, itemIndex):
        equip = self.currEquips.get(itemIndex)
        if equip != None:
            return tipUtils.getItemTipByLocation(equip, const.ITEM_IN_BLARENA_TEMPLATE)
        else:
            return

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            panel = self.widget.casePanel
            p = BigWorld.player()
            self.currEquips = {}
            self.currSechemes = {}
            for i in xrange(MAX_EQUIP_NUM):
                item = panel.getChildByName('item%d' % i)
                item.lose.visible = False
                item.slot.dragable = False
                equipInfo = p.equipment[SHOW_EQUIP_INDEXS[i]]
                self.currEquips[SHOW_EQUIP_INDEXS[i]] = equipInfo
                if equipInfo:
                    equipId = equipInfo.id
                    item.slot.itemId = equipId
                    item.slot.setItemSlotData(uiUtils.getGfxItem(equipInfo, appendInfo={'srcType': 'templateUp' + str(SHOW_EQUIP_INDEXS[i]),
                     'itemId': equipInfo.id}))
                    item.lose.visible = False
                else:
                    item.slot.itemId = 0
                    item.slot.setItemSlotData(None)

            for idx in SHOW_SCHEME_INDEXS:
                schemeItem = self.widget.casePanel.skillList.canvas.getChildByName('item%d' % idx)
                curNo, name = self.getSchemeNameByIndex(schemeItem.index + 1)
                self.currSechemes[idx] = curNo
                schemeItem.value.label = name

            return

    def getSchemeNameByIndex(self, type):
        name = ''
        expireTime = 0
        curNo = -1
        p = BigWorld.player()
        if type == uiConst.ONEKEYCONFIG_CONTENT_ID_WUSHUANG:
            curNo = p.getCurWSSchemeNo()
            name = p.getCurWSSchemeName()
            expireTime = p.getWSSchemeExpireTime(curNo)
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_PROP:
            curNo = p.curPropScheme
            scheme = p.getPropSchemeById(curNo)
            if scheme:
                name = scheme.get('schemeName', '')
                expireTime = scheme.get('expireTime', 0)
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_SKILLPOINT:
            curNo = p.skillPointSchemeIndex
            scheme = p.getSkillSchemeById(curNo)
            name = BigWorld.player().getSkillSchemeName(curNo)
            if scheme:
                expireTime = scheme[4]
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_SHORTCUT:
            curNo = gameglobal.rds.ui.actionbar.getCurrSchemeNo()
            name = gameStrings.SHORTCUT_SCHEME_NAME % curNo
            expireTime = 0
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_EQUIPSOUL:
            curNo = p.currEquipSoulSchemeNo
            name = p.getCurEquipSoulSchemeName()
            expireTime = p.getEquipSoulSchemeExpireTime(curNo)
        elif type == uiConst.ONEKEYCONFIG_CONTENT_ID_CARD:
            curNo = p.cardBag.get('equipSlot', 0)
            if curNo == 0 or curNo == 1:
                curNo = 1
            name = gameStrings.CARD_SCHEME_NAME % curNo
        if expireTime and expireTime < utils.getNow():
            name += gameStrings.SCHEME_EXPIRE_DESC
        return (curNo, name)
