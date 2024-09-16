#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTopSetGiftProxy.o
import BigWorld
import gametypes
import gamelog
from callbackHelper import Functor
import gameglobal
import uiConst
import events
from guis import ui
from guis.asObject import TipManager
from uiProxy import UIProxy
from data import school_top_config_data as STCD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class SchoolTopSetGiftProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTopSetGiftProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TOP_SET_GIFT, self.hide)

    def reset(self):
        self.seletedType = gametypes.SCHOOL_TOP_LUCKY_BAG_TYPE_2
        self.maxCnt = STCD.data.get('luckyBagNumLimit', 99)
        self.singleCost = 0
        self.totalCnt = 1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TOP_SET_GIFT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    @property
    def selfData(self):
        p = BigWorld.player()
        return p.getSelfCandidateData()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TOP_SET_GIFT)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TOP_SET_GIFT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.txtInput.maxNum = self.maxCnt
        self.widget.txtInput.text = 0
        self.widget.radioBtn0.addEventListener(events.BUTTON_CLICK, self.handleRaio0Click, False, 0, True)
        self.widget.radioBtn0.validateNow()
        luckyBagItems = STCD.data.get('luckyBagItems', {})
        TipManager.addItemTipById(self.widget.radioBtn0, luckyBagItems.get(gametypes.SCHOOL_TOP_LUCKY_BAG_TYPE_1, 999))
        self.widget.radioBtn1.addEventListener(events.BUTTON_CLICK, self.handleRaio1Click, False, 0, True)
        self.widget.radioBtn1.validateNow()
        TipManager.addItemTipById(self.widget.radioBtn1, luckyBagItems.get(gametypes.SCHOOL_TOP_LUCKY_BAG_TYPE_2, 999))
        self.widget.radioBtn2.addEventListener(events.BUTTON_CLICK, self.handleRaio2Click, False, 0, True)
        self.widget.radioBtn2.validateNow()
        TipManager.addItemTipById(self.widget.radioBtn2, luckyBagItems.get(gametypes.SCHOOL_TOP_LUCKY_BAG_TYPE_3, 999))
        self.widget.prevBtn.addEventListener(events.BUTTON_CLICK, self.handlePrevBtnClick, False, 0, True)
        self.widget.nextBtn.addEventListener(events.BUTTON_CLICK, self.handleNextBtnClick, False, 0, True)
        self.widget.txtInput.addEventListener(events.EVENT_CHANGE, self.refreshTotalPay, False, 0, True)
        self.widget.sureBtn.addEventListener(events.BUTTON_CLICK, self.handleSureBtnClick, False, 0, True)
        self.widget.maxBtn.addEventListener(events.BUTTON_CLICK, self.handleMaxBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshCostType()

    def getSelectedType(self):
        if self.widget.radioBtn0.selected:
            return gametypes.SCHOOL_TOP_LUCKY_BAG_TYPE_1
        elif self.widget.radioBtn1.selected:
            return gametypes.SCHOOL_TOP_LUCKY_BAG_TYPE_2
        else:
            return gametypes.SCHOOL_TOP_LUCKY_BAG_TYPE_3

    def refreshCostType(self):
        p = BigWorld.player()
        selectedType = self.getSelectedType()
        costType, costNum = STCD.data.get('luckyBagCost', {1: (1, 1000),
         2: (1, 8000),
         3: (2, 18)}).get(selectedType, (1, 100))
        if costType == gametypes.SCHOOL_TOP_LUCKY_BAG_COST_CASH:
            self.widget.coinIcon.bonusType = 'cash'
            self.singleCost = costNum
            self.totalCnt = p.bindCash + p.cash
        elif costType == gametypes.SCHOOL_TOP_LUCKY_BAG_COST_COIN:
            self.widget.coinIcon.bonusType = 'tianBi'
            self.singleCost = costNum
            self.totalCnt = p.unbindCoin + p.bindCoin + p.freeCoin
        self.refreshTotalPay()

    def refreshTotalPay(self, *args):
        value = int(self.widget.txtInput.text) if self.widget.txtInput.text else 0
        self.widget.totlePay.text = '%d/%d' % (value * self.singleCost, self.totalCnt)

    def handlePrevBtnClick(self, *args):
        oldCnt = int(self.widget.txtInput.text) if self.widget.txtInput.text else 0
        self.widget.txtInput.text = str(max(0, oldCnt - 1))
        self.refreshTotalPay()

    def handleNextBtnClick(self, *args):
        oldCnt = int(self.widget.txtInput.text) if self.widget.txtInput.text else 0
        self.widget.txtInput.text = str(min(self.maxCnt, oldCnt + 1))
        self.refreshTotalPay()

    def handleRaio0Click(self, *args):
        self.widget.txtInput.text = 0
        self.refreshCostType()

    def handleRaio1Click(self, *args):
        self.widget.txtInput.text = 0
        self.refreshCostType()

    def handleRaio2Click(self, *args):
        self.widget.txtInput.text = 0
        self.refreshCostType()

    def handleSureBtnClick(self, *args):
        p = BigWorld.player()
        value = int(self.widget.txtInput.text) if self.widget.txtInput.text else 0
        if not value:
            return
        totalCost = value * self.singleCost
        if totalCost < self.totalCnt:
            self.doPay()
        else:
            costType, costNum = STCD.data.get('luckyBagCost', {1: (1, 1000),
             2: (1, 8000),
             3: (2, 18)}).get(self.getSelectedType(), (1, 100))
            if costType == gametypes.SCHOOL_TOP_LUCKY_BAG_COST_CASH:
                p.showGameMsg(GMDD.data.NOT_ENOUGH_CASH, ())
            else:
                p.showGameMsg(GMDD.data.NOT_ENOUGH_COIN, ())

    @ui.checkInventoryLock()
    def doPay(self):
        p = BigWorld.player()
        costType, costNum = STCD.data.get('luckyBagCost', {1: (1, 1000),
         2: (1, 8000),
         3: (2, 18)}).get(self.getSelectedType(), (1, 100))
        gamelog.info('jbx:addSchoolTopLuckyBag', self.getSelectedType(), int(self.widget.txtInput.text))
        if costType == gametypes.SCHOOL_TOP_LUCKY_BAG_COST_COIN:
            text = GMD.data.get(GMDD.data.LUCKY_BAG_COST_COIN_CONFIRM, {}).get('text', '%d') % (costNum * int(self.widget.txtInput.text))
            self.uiAdapter.messageBox.showYesNoMsgBox(text, Functor(p.cell.addSchoolTopLuckyBag, self.getSelectedType(), int(self.widget.txtInput.text)))
        else:
            p.cell.addSchoolTopLuckyBag(self.getSelectedType(), int(self.widget.txtInput.text))

    def handleMaxBtnClick(self, *args):
        self.widget.txtInput.text = str(self.maxCnt)
        self.refreshTotalPay()
