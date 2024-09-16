#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chickenFoodMainProxy.o
import BigWorld
import gameglobal
import gamelog
import time
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import chickenFoodFactory
from guis import uiUtils
from asObject import ASUtils
from gameStrings import gameStrings
from cdata import chicken_meal_quality_material_info_data as CMQMID

class ChickenFoodMainProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChickenFoodMainProxy, self).__init__(uiAdapter)
        self.widget = None
        self.cfFactory = chickenFoodFactory.getInstance()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHICKEN_FOOD_MAIN:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHICKEN_FOOD_MAIN)

    def clearWidget(self):
        self.widget = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHICKEN_FOOD_MAIN)

    def reset(self):
        pass

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        ASUtils.setHitTestDisable(self.widget.mainBg, True)
        self.widget.rankBtn.addEventListener(events.MOUSE_CLICK, self.handleClickRankBtn, False, 0, True)
        self.widget.helpMc.textField.htmlText = gameStrings.CHICKENFOOD_GUIDESTR
        self.widget.helpMc.addEventListener(events.MOUSE_CLICK, self.handleClickHelpMc, False, 0, True)
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            starMax = self.cfFactory.getStarNumMax()
            if self.cfFactory.isWaiting:
                self.widget.foodNameTx.visible = False
                self.widget.waitingTx.visible = True
                waitStr = ''
                if not self.cfFactory.waitingNum < 0:
                    waitStr = ''.join((gameStrings.CHICKENFOOD_WAITING_STR, '(%ds)' % self.cfFactory.waitingNum))
                else:
                    waitStr = gameStrings.CHICKENFOOD_WAITING_STR
                self.widget.waitingTx.text = waitStr
                for i in xrange(starMax):
                    getattr(self.widget, 'star' + str(i)).visible = False

            else:
                self.widget.waitingTx.visible = False
                self.widget.foodNameTx.visible = True
                foodDetail = self.cfFactory.getCurFoodDetail()
                name = foodDetail.get('name', '')
                rare = foodDetail.get('rare', 0)
                self.widget.foodNameTx.htmlText = self.cfFactory.transFoodName(name, rare)
                starNum = self.cfFactory.getCurFoodStarNum()
                for i in xrange(starMax):
                    getattr(self.widget, 'star' + str(i)).visible = i < starNum

            self.widget.foodNoTxt.text = self.cfFactory.getFoodNoStr()
            self.widget.scoreTxt.text = self.cfFactory.getScoreStr()
            barInfo = self.cfFactory.getCurBarInfo()
            for i, item in enumerate(barInfo):
                getattr(self.widget, 'barMc' + str(i)).setData(item)

    def handleClickRankBtn(self, *args):
        self.cfFactory.showRank(True)

    def handleClickHelpMc(self, *args):
        gameglobal.rds.ui.chickenFoodGuide.show()

    def startTimeClock(self, waitingTime):
        if self.cfFactory:
            self.cfFactory.setWaitingTimer(waitingTime)

    def hasBaseData(self):
        if self.cfFactory and self.widget:
            return True
        else:
            return False
