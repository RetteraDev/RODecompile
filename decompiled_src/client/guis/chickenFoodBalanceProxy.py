#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/chickenFoodBalanceProxy.o
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

class ChickenFoodBalanceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChickenFoodBalanceProxy, self).__init__(uiAdapter)
        self.resultInfo = None
        self.widget = None
        self.openCallback = None
        self.cfFactory = chickenFoodFactory.getInstance()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHICKEN_FOOD_BALANCE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHICKEN_FOOD_BALANCE:
            self.widget = widget
            self.initUI()

    def show(self, resultInfo):
        self.resultInfo = resultInfo
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHICKEN_FOOD_BALANCE, True)

    def clearWidget(self):
        self.widget = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHICKEN_FOOD_BALANCE)

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
        self.widget.gotoAndStop('zhankaidognhua')
        gameglobal.rds.sound.playSound(5114)
        if self.openCallback:
            ASUtils.cancelCallBack(self.openCallback)
        self.openCallback = ASUtils.callbackAtFrame(self.widget.mainMc, 28, self.after)

    def after(self, *arg):
        self.widget.gotoAndStop('richang')
        self.widget.mainMc.rankBtn.addEventListener(events.MOUSE_CLICK, self.handleClickRankBtn, False, 0, True)
        self.widget.mainMc.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCloseBtn, False, 0, True)
        self.widget.mainMc.closeBtn.closeLabelMc.gotoAndStop('normal')
        self.refreshInfo()

    def refreshInfo(self):
        if self.hasBaseData():
            if self.widget.currentFrameLabel == 'richang':
                totalScore = 0
                self.widget.mainMc.itemListMc.gotoAndStop(''.join(('num', str(len(self.resultInfo)))))
                for i, v in enumerate(self.resultInfo):
                    foodNo, foodId, quality, star, score, uTime = v
                    totalScore += score
                    item = getattr(self.widget.mainMc.itemListMc, 'item' + str(foodNo - 1), None)
                    if item:
                        detailInfo = self.cfFactory.getFoodDetailInfoById(foodId)
                        item.foodNoMc.gotoAndStop(''.join(('foodInfo', str(foodNo))))
                        name = detailInfo.get('name', '')
                        rare = detailInfo.get('rare', 0)
                        icon = detailInfo.get('icon', 0)
                        item.foodName.htmlText = self.cfFactory.transFoodName(name, rare)
                        item.starMc.gotoAndStop(''.join(('star', str(star))))
                        iconPath = self.cfFactory.getChickenIcon(uiConst.ICON_SIZE110, icon)
                        scoreStr = gameStrings.CHICKENFOOD_SCORE_STR % score
                        colorStr = uiUtils.getColorByQuality(rare)
                        info = {'iconPath': iconPath,
                         'score': scoreStr,
                         'colorStr': colorStr}
                        item.foodIcon.setData(info)

                _str = ''
                _str = gameStrings.CHICKENFOOD_SCORE_STR % totalScore
                _str = ''.join((gameStrings.CHICKENFOOD_TOTALSOCRE_STR, str(_str)))
                self.widget.mainMc.scoreTxt.text = _str

    def handleClickCloseBtn(self, *args):
        self.hide()

    def handleClickRankBtn(self, *args):
        self.cfFactory.showRank(True)

    def hasBaseData(self):
        if self.cfFactory and self.widget:
            return True
        return False
