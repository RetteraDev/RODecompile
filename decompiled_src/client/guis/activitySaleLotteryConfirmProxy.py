#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleLotteryConfirmProxy.o
import BigWorld
import uiConst
import events
import gametypes
import gamelog
import gameglobal
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis import uiUtils
from guis import ui
from data import item_data as ID
from data import sys_config_data as SCD
from data import random_lottery_data as RLD
from cdata import game_msg_def_data as GMDD
CONSUME_BIND_ITEM = 1
CONSUME_ITEM = 2
CONSUME_TIANBI = 3

class ActivitySaleLotteryConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleLotteryConfirmProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACTIVITY_SALE_LOTTERY_CONFIRM, self.hide)

    def reset(self):
        self.widget = None
        self.selectType = 0
        self.remindAgain = True
        self.countType = 0
        self.consumeTypeList = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ACTIVITY_SALE_LOTTERY_CONFIRM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACTIVITY_SALE_LOTTERY_CONFIRM)

    def show(self, countType):
        if not self.widget:
            self.countType = countType
            self.uiAdapter.loadWidget(uiConst.WIDGET_ACTIVITY_SALE_LOTTERY_CONFIRM)
        else:
            self.initUI()

    def initUI(self):
        p = BigWorld.player()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        data = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        consumeBindItemTotalNum = 0
        consumeItemTotalNum = 0
        consumeTianbiTotalNum = p.unbindCoin + p.bindCoin + p.freeCoin
        consumeItemId = data.get('consumeItemId', (411415,))
        consumeBindItemId = data.get('consumeBindItemId', (411416,))
        for itemId in consumeBindItemId:
            itemNum = p.inv.countItemInPages(itemId)
            consumeBindItemTotalNum += itemNum

        for itemId in consumeItemId:
            itemNum = p.inv.countItemInPages(itemId)
            consumeItemTotalNum += itemNum

        self.widget.consumeBindItem.slot.dragable = False
        self.widget.consumeBindItem.slot.itemId = consumeBindItemId[0]
        self.widget.consumeBindItem.slot.setItemSlotData(uiUtils.getGfxItemById(consumeBindItemId[0]))
        self.widget.consumeBindItem.itemCheckBox.selected = False
        self.consumeTypeList.append(self.widget.consumeBindItem.itemCheckBox)
        self.widget.consumeBindItem.type = CONSUME_BIND_ITEM
        self.widget.consumeBindItem.bind.visible = True
        self.widget.consumeBindItem.unbind.visible = False
        numberTxt = 'x1' if self.countType == 1 else 'x10'
        self.widget.consumeBindItem.itemName.text = ID.data.get(consumeBindItemId[0], {}).get('name', '') + numberTxt
        self.widget.consumeBindItem.itemCount.text = gameStrings.RANDOM_LOTTERY_LEFT_TEXT % consumeBindItemTotalNum
        self.widget.consumeBindItem.itemCheckBox.addEventListener(events.BUTTON_CLICK, self.handleSelect, False, 0, True)
        self.widget.consumeItem.slot.dragable = False
        self.widget.consumeItem.slot.itemId = consumeItemId[0]
        self.widget.consumeItem.slot.setItemSlotData(uiUtils.getGfxItemById(consumeItemId[0]))
        self.widget.consumeItem.itemCheckBox.selected = False
        self.consumeTypeList.append(self.widget.consumeItem.itemCheckBox)
        self.widget.consumeItem.type = CONSUME_ITEM
        self.widget.consumeItem.bind.visible = False
        self.widget.consumeItem.unbind.visible = True
        self.widget.consumeItem.itemName.text = ID.data.get(consumeItemId[0], {}).get('name', '') + numberTxt
        self.widget.consumeItem.itemCount.text = gameStrings.RANDOM_LOTTERY_LEFT_TEXT % consumeItemTotalNum
        self.widget.consumeItem.itemCheckBox.addEventListener(events.BUTTON_CLICK, self.handleSelect, False, 0, True)
        self.widget.consumeTianbi.itemCheckBox.selected = False
        self.consumeTypeList.append(self.widget.consumeTianbi.itemCheckBox)
        self.widget.consumeTianbi.type = CONSUME_TIANBI
        self.widget.consumeTianbi.itemName.text = gameStrings.RANDOM_LOTTERY_TIANBI if self.countType == 1 else gameStrings.RANDOM_LOTTERY_TIANBI2
        self.widget.consumeTianbi.itemCount.text = gameStrings.RANDOM_LOTTERY_LEFT_TEXT % consumeTianbiTotalNum
        self.widget.consumeTianbi.itemCheckBox.addEventListener(events.BUTTON_CLICK, self.handleSelect, False, 0, True)
        self.widget.againBtn.addEventListener(events.BUTTON_CLICK, self.handleAgainBtnClick, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def handleCancelBtnClick(self, *args):
        gameglobal.rds.ui.activitySaleLottery.selectType = 0
        gameglobal.rds.ui.activitySaleLottery.remindAgain = True
        self.clearWidget()

    def handleAgainBtnClick(self, *args):
        target = ASObject(args[3][0]).currentTarget
        self.remindAgain = target.selected == False

    @ui.callFilter(2.5)
    @ui.checkInventoryLock()
    def handleConfirmBtnClick(self, *args):
        if not self.selectType:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.NOT_CHOOSE__COSUME_ITEM, ())
        if self.selectType and self.countType:
            gameglobal.rds.ui.activitySaleLottery.remindAgain = self.remindAgain
            gameglobal.rds.ui.activitySaleLottery.selectType = self.selectType
            gameglobal.rds.ui.activitySaleLottery.setLotteryBtn(False)
            BigWorld.player().cell.randomLotteryDrawOptimizeRequest(self.countType, self.selectType)

    def handleSelect(self, *args):
        target = ASObject(args[3][0]).currentTarget
        if target.selected == True:
            self.selectType = target.parent.type
        else:
            self.selectType = 0
        for checkBox in self.consumeTypeList:
            checkBox.selected = self.selectType == checkBox.parent.type
