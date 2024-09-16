#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chickenFoodShowProxy.o
import random
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

class ChickenFoodShowProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChickenFoodShowProxy, self).__init__(uiAdapter)
        self.widget = None
        self.foodNum = None
        self.foodInfo = None
        self.otherInfo = None
        self.cfFactory = chickenFoodFactory.getInstance()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHICKEN_FOOD_SHOW:
            self.widget = widget
            self.initUI()

    def show(self, foodNum, foodInfo, otherInfo):
        self.foodNum = foodNum
        self.foodInfo = foodInfo
        self.otherInfo = otherInfo
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHICKEN_FOOD_SHOW, True)

    def clearWidget(self):
        self.widget = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHICKEN_FOOD_SHOW)

    def reset(self):
        self.foodNum = None
        self.foodInfo = None
        self.otherInfo = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.mainMc.barMc.barMc.addEventListener(events.PROCESSING_END, self.handleBarMcProgressing, False, 0, True)
        gameglobal.rds.sound.playSound(5113)
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            foodId, quality, lessValue, excessValue = self.foodInfo
            detailInfo = self.cfFactory.getFoodDetailInfoById(foodId)
            rare = detailInfo.get('rare', 0)
            icon = detailInfo.get('icon', 0)
            iconPath = self.cfFactory.getChickenIcon(uiConst.ICON_SIZE110, icon)
            self.widget.mainMc.icon.loadImage(iconPath)
            self.widget.mainMc.randomTxt.text = gameStrings.CHICKEN_SUBMIT_RANDOM_TXT.get(random.randint(1, 11), '')

    def handleBarMcProgressing(self, *args):
        gameglobal.rds.ui.chickenFoodSubmit.show(self.foodNum, self.foodInfo, self.otherInfo)
        self.hide()

    def hasBaseData(self):
        if self.foodNum and self.foodInfo and self.otherInfo and self.widget:
            return True
        return False
