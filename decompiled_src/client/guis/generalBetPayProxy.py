#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/generalBetPayProxy.o
import BigWorld
from guis import ui
import gameglobal
import uiConst
from guis import events
from uiProxy import UIProxy
from data import sys_config_data as SCD
from guis.asObject import ASObject
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
import const
CHOOSE_ITEM_NUM = 6
DEFAULT_PAY_NUM_LIST = [10000,
 30000,
 50000,
 100000,
 200000,
 600000]

class GeneralBetPayProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GeneralBetPayProxy, self).__init__(uiAdapter)
        self.widget = None
        self.lastSelectItem = None
        self.payList = []
        self.bId = 0
        self.optIndex = 0
        self.option = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GENERAL_BET_PAY, self.hide)

    def reset(self):
        self.lastSelectItem = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GENERAL_BET_PAY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GENERAL_BET_PAY)
        self.lastSelectItem = None

    def show(self, bId, optIndex, option):
        self.bId = bId
        self.optIndex = optIndex
        self.option = option
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GENERAL_BET_PAY)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.icon.bonusType = 'yunChui'
        self.payList = SCD.data.get('generalBetPayList', DEFAULT_PAY_NUM_LIST)
        for i in xrange(CHOOSE_ITEM_NUM):
            chooseMc = self.widget.getChildByName('choose%d' % i)
            chooseMc.item.label = '       %d' % self.payList[i]
            chooseMc.icon.bonusType = 'yunChui'
            chooseMc.item.index = i
            chooseMc.item.addEventListener(events.EVENT_SELECT, self.onCheckBoxSelected)

        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirmBtnClick)

    def onCheckBoxSelected(self, *args):
        e = ASObject(args[3][0])
        if not e.currentTarget.selected:
            return
        if self.lastSelectItem and self.lastSelectItem != e.currentTarget:
            self.lastSelectItem.selected = False
        self.lastSelectItem = e.currentTarget

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.num.text = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
        self.widget.answer.text = gameStrings.MY_BET_ANSWER % self.option

    @ui.checkInventoryLock()
    def onConfirmBtnClick(self, *args):
        p = BigWorld.player()
        if self.lastSelectItem:
            index = self.lastSelectItem.index
            payNum = self.payList[index]
            if self.checkCashEnough(payNum):
                p.cell.doBet(self.bId, self.optIndex, payNum)
                self.hide()
            else:
                gameglobal.rds.ui.generalBetTianBi.show(payNum)
                return

    def checkCashEnough(self, payNum):
        p = BigWorld.player()
        if p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID) >= payNum:
            return True
        else:
            return False
