#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chickenFoodSubmitProxy.o
import BigWorld
import gameglobal
import gamelog
import time
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import chickenFoodFactory
from guis import uiUtils
from gameStrings import gameStrings
from cdata import chicken_meal_quality_material_info_data as CMQMID
COUNTDOWN_CHECK_TIME = 1

class ChickenFoodSubmitProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChickenFoodSubmitProxy, self).__init__(uiAdapter)
        self.widget = None
        self.foodNum = None
        self.foodInfo = None
        self.otherInfo = None
        self.countDown = 0
        self.countDownCallBack = None
        self.cfFactory = chickenFoodFactory.getInstance()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHICKEN_FOOD_SUBMIT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHICKEN_FOOD_SUBMIT:
            self.widget = widget
            self.initUI()

    def show(self, foodNum, foodInfo, otherInfo):
        self.foodNum = foodNum
        self.foodInfo = foodInfo
        self.otherInfo = otherInfo
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHICKEN_FOOD_SUBMIT)

    def clearWidget(self):
        self.widget = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHICKEN_FOOD_SUBMIT)

    def reset(self):
        if self.countDownCallBack:
            BigWorld.cancelCallback(self.countDownCallBack)
            self.countDownCallBack = None
        self.foodNum = None
        self.foodInfo = None
        self.otherInfo = None

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        self.countDown = 30

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.closeBtn.closeLabelMc.gotoAndStop('countDown')
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            foodId, quality, lessValue, excessValue = self.foodInfo
            detailInfo = self.cfFactory.getFoodDetailInfoById(foodId)
            self.widget.foodNoMc.gotoAndStop(''.join(('foodInfo', str(self.foodNum))))
            name = detailInfo.get('name', '')
            rare = detailInfo.get('rare', 0)
            icon = detailInfo.get('icon', 0)
            self.widget.foodName.htmlText = self.cfFactory.transFoodName(name, rare)
            iconPath = self.cfFactory.getChickenIcon(uiConst.ICON_SIZE110, icon)
            score = ''
            colorStr = uiUtils.getColorByQuality(rare)
            info = {'iconPath': iconPath,
             'score': score,
             'colorStr': colorStr}
            self.widget.foodIcon.setData(info)
            barInfo = self.otherInfo.get('barInfo', {})
            for i, item in enumerate(barInfo):
                getattr(self.widget.allBarMc, 'barMc' + str(i)).setData(item)

            result, star, score, uTime = self.otherInfo.get('foodResult', {})
            _str = gameStrings.CHICKENFOOD_SCORE_STR % score
            self.widget.scoreTxt.text = _str
            self.widget.starMc.gotoAndStop(''.join(('star', str(star))))
            self.countDownFunc()

    def hasBaseData(self):
        if self.otherInfo and self.foodInfo and self.foodNum and self.cfFactory and self.widget:
            return True
        return False

    def countDownFunc(self):
        if self.countDownCallBack:
            BigWorld.cancelCallback(self.countDownCallBack)
            self.countDownCallBack = None
        self.widget.closeBtn.closeLabelMc.countTxt.text = '(%ds)' % self.countDown
        self.countDown -= 1
        if self.countDown < 0:
            self.countDown = 0
            self.hide()
            return
        else:
            self.countDownCallBack = BigWorld.callback(COUNTDOWN_CHECK_TIME, self.countDownFunc)
            return