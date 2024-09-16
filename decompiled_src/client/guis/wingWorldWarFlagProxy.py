#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldWarFlagProxy.o
import BigWorld
import uiConst
import events
import gameglobal
from uiProxy import UIProxy
from asObject import ASObject
from data import sys_config_data as SCD
from data import wing_world_country_flag_data as WWCFD
COLUMN_NUM = 8
IMPAGE_PATH = 'wingWorld/wingWorldFlag/%d.dds'

class WingWorldWarFlagProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldWarFlagProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectedItemMc = None
        self.selectedflagId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_WAR_FLAG, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_WAR_FLAG:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_WAR_FLAG)

    def reset(self):
        self.selectedItemMc = None
        self.selectedflagId = 0

    def show(self):
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_WAR_FLAG)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.warFlagList.itemRenderer = 'M12_InventorySlot64x64'
        self.widget.warFlagList.column = COLUMN_NUM
        self.widget.warFlagList.itemHeight = 75
        self.widget.warFlagList.itemWidth = 75
        self.widget.warFlagList.dataArray = []
        self.widget.warFlagList.lableFunction = self.itemFunction
        self.widget.warFlagList.validateNow()

    def refreshInfo(self):
        if not self.widget:
            return
        warFlags = self.getWarFlagList()
        self.widget.warFlagList.dataArray = warFlags
        self.widget.warFlagList.validateNow()
        self.updateSureBtnState()

    def _onSureBtnClick(self, e):
        if not self.selectedflagId:
            return
        p = BigWorld.player()
        p.cell.setWingWorldCountryFlag(self.selectedflagId)

    def _onCancelBtnClick(self, e):
        self.hide()

    def handleItemMcDown(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.selectedflagId and self.selectedflagId == itemMc.flagId:
            return
        if self.selectedItemMc:
            self.selectedItemMc.setSlotState(uiConst.ITEM_NORMAL)
        itemMc.setSlotState(uiConst.ITEM_SELECTED)
        self.selectedItemMc = itemMc
        self.selectedflagId = itemMc.flagId
        self.updateSureBtnState()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.flagId = itemData.flagId
        itemMc.iconId = itemData.iconId
        itemMc.setSlotState(uiConst.ITEM_NORMAL)
        itemMc.fitSize = True
        itemMc.dragable = False
        iconPath = IMPAGE_PATH % itemData.iconId
        itemMc.setItemSlotData({'iconPath': iconPath})
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleItemMcDown, False, 0, True)
        if itemData.usedFlag:
            itemMc.setSlotState(uiConst.ITEM_DISABLE)

    def getWarFlagList(self):
        p = BigWorld.player()
        usedFlags = p.wingWorld.country.getUsedFlags()
        itemList = []
        for flagId in WWCFD.data.iterkeys():
            data = WWCFD.data.get(flagId, {})
            iconId = data.get('icon', 0)
            usedFlag = flagId in usedFlags
            itemInfo = {}
            itemInfo['flagId'] = flagId
            itemInfo['iconId'] = iconId
            itemInfo['usedFlag'] = usedFlag
            itemList.append(itemInfo)

        return itemList

    def updateSureBtnState(self):
        if not self.widget:
            return
        self.widget.sureBtn.enabled = self.selectedflagId
