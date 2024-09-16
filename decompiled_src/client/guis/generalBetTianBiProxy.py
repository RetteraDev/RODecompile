#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/generalBetTianBiProxy.o
import BigWorld
import math
import gameglobal
import uiConst
import events
import const
from uiProxy import UIProxy
from guis import uiUtils
from guis import ui
from data import sys_config_data as SCD
BUY_MAX_NUM = 999
TIANBI_COST = 10

class GeneralBetTianBiProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GeneralBetTianBiProxy, self).__init__(uiAdapter)
        self.widget = None
        self.buyNum = 0
        self.betNum = 0
        self.requireNum = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GENERAL_BET_TIANBI, self.hide)

    def reset(self):
        self.buyNum = 1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GENERAL_BET_TIANBI:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GENERAL_BET_TIANBI)
        self.reset()

    def show(self, betNum):
        self.betNum = betNum
        self.calcRequireTianBi()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GENERAL_BET_TIANBI)
        else:
            self.refreshInfo()

    def calcRequireTianBi(self):
        p = BigWorld.player()
        currFame = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
        self.requireNum = max(0, self.betNum - currFame)
        if self.requireNum <= 0:
            self.hide()
        cost = SCD.data.get('yunchuiCreditPerCoin', 0)
        if cost == 0:
            return
        self.buyNum = int(math.ceil(self.requireNum * 1.0 / (cost * TIANBI_COST)))

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.icon0.bonusType = 'yunChui'
        self.widget.icon1.bonusType = 'yunChui'
        self.widget.icon2.bonusType = 'tianBi'
        self.widget.icon3.bonusType = 'yunChui'

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        tianbi = p.unbindCoin + p.bindCoin + p.freeCoin
        self.widget.betNum.text = str(self.betNum)
        self.widget.requireNum.text = str(self.requireNum)
        self.widget.payNum.text = str(self.buyNum * TIANBI_COST)
        self.widget.getNum.text = str(self.buyNum * TIANBI_COST * SCD.data.get('yunchuiCreditPerCoin', 0))
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)

    @ui.checkInventoryLock()
    def handleConfirmBtnClick(self, *args):
        p = BigWorld.player()
        p.cell.buyYunChuiCreditConsumeCoin(self.buyNum * TIANBI_COST, p.cipherOfPerson)
        self.hide()
