#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pubgAutoPickSettingProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
import const
import ui
import pubgUtils
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
import clientUtils

class PubgAutoPickSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PubgAutoPickSettingProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PUBG_AUTO_PICK_SETTING, self.hide)

    def reset(self):
        self.autoPickSettingData = dict()
        for type in pubgUtils.AUTO_PICK_ALL_TYPE:
            self.autoPickSettingData[type] = True

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PUBG_AUTO_PICK_SETTING:
            self.widget = widget
            self.reset()
            self.initData()
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUBG_AUTO_PICK_SETTING)

    def initData(self):
        p = BigWorld.player()
        for type in pubgUtils.AUTO_PICK_ALL_TYPE:
            self.autoPickSettingData[type] = p.checkAutoPickTypeEnable(type)

    def initUI(self):
        if not self.widget:
            return
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.titleTxt.text = gameStrings.PUBG_AUTO_PICK_SETTING_TITLE
        self.widget.centerHintTxt.text = gameStrings.PUBG_AUTO_PICK_SETTING_CENTER_HINT
        self.widget.equipTxt.text = gameStrings.PUBG_AUTO_PICK_SETTING_EQUIP_TEXT
        self.widget.skillTxt.text = gameStrings.PUBG_AUTO_PICK_SETTING_SKILL_TEXT
        self.widget.itemTxt.text = gameStrings.PUBG_AUTO_PICK_SETTING_ITEM_TEXT
        self.initAllCheckBoxUI()

    def initAllCheckBoxUI(self):
        self.widget.equipCheckBox.selected = self.autoPickSettingData[pubgUtils.AUTO_PICK_EQUIPMENT]
        self.widget.equipCheckBox.autoPickType = pubgUtils.AUTO_PICK_EQUIPMENT
        self.widget.skillCheckBox.selected = self.autoPickSettingData[pubgUtils.AUTO_PICK_SKILL]
        self.widget.skillCheckBox.autoPickType = pubgUtils.AUTO_PICK_SKILL
        self.widget.drugCheckBox.selected = self.autoPickSettingData[pubgUtils.AUTO_PICK_POTION]
        self.widget.drugCheckBox.autoPickType = pubgUtils.AUTO_PICK_POTION
        self.widget.equipCheckBox.addEventListener(events.BUTTON_CLICK, self.handleCheckBoxClick, False, 0, True)
        self.widget.skillCheckBox.addEventListener(events.BUTTON_CLICK, self.handleCheckBoxClick, False, 0, True)
        self.widget.drugCheckBox.addEventListener(events.BUTTON_CLICK, self.handleCheckBoxClick, False, 0, True)

    def handleCheckBoxClick(self, *args):
        checkBox = ASObject(args[3][0]).currentTarget
        autoPickType = int(checkBox.autoPickType)
        self.autoPickSettingData[autoPickType] = checkBox.selected

    def handleConfirmBtnClick(self, *args):
        p = BigWorld.player()
        for type in pubgUtils.AUTO_PICK_ALL_TYPE:
            p.setAutoPickTypeEnable(type, self.autoPickSettingData[type])

        self.hide()
        gameglobal.rds.ui.pubgAutoPick.refreshAll()

    def show(self):
        p = BigWorld.player()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PUBG_AUTO_PICK_SETTING)
