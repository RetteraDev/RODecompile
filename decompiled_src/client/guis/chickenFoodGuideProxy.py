#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chickenFoodGuideProxy.o
import BigWorld
import gameglobal
import time
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from guis import chickenFoodFactory
from gameStrings import gameStrings
from guis.asObject import ASUtils
from cdata import chicken_meal_quality_material_info_data as CMQMID

class ChickenFoodGuideProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChickenFoodGuideProxy, self).__init__(uiAdapter)
        self.widget = None
        self.openCallback = None
        self.cfFactory = chickenFoodFactory.getInstance()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHICKEN_FOOD_GUIDE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHICKEN_FOOD_GUIDE:
            self.widget = widget
            self.initUI()

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHICKEN_FOOD_GUIDE, True)

    def clearWidget(self):
        self.widget = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHICKEN_FOOD_GUIDE)

    def reset(self):
        self.resultInfo = None
        if self.openCallback:
            ASUtils.cancelCallBack(self.openCallback)
            self.openCallback = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.gotoAndStop('jingzhi')
        self.widget.mainMc.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCloseBtn, False, 0, True)

    def handleClickCloseBtn(self, *args):
        self.widget.gotoAndStop('donghua')
        if self.openCallback:
            ASUtils.cancelCallBack(self.openCallback)
        self.openCallback = ASUtils.callbackAtFrame(self.widget.mainMc2, 9, self.after)

    def after(self, *arg):
        self.hide()

    def handleClickRankBtn(self, *args):
        self.cfFactory.showRank(True)

    def hasBaseData(self):
        if self.cfFactory and self.widget:
            return True
        return False
