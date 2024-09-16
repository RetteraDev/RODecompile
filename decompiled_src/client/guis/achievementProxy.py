#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achievementProxy.o
import BigWorld
import gameglobal
import uiConst
from Scaleform import GfxValue
from guis import ui
from uiProxy import UIProxy
from ui import gbk2unicode

class AchievementProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AchievementProxy, self).__init__(uiAdapter)
        self.mediator = None
        self.pointMediator = None
        self.modelMap = {'clickDoneAchievement': self.onClickDoneAchievement}
        self.achievePlusStr = ''

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ACHIEVEMENT_DONE:
            self.pointMediator = mediator
        elif widgetId == uiConst.WIDGET_ACHIEVEMENT_PLUS:
            return GfxValue(gbk2unicode(self.achievePlusStr))

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_ACHIEVEMENT_PLUS:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ACHIEVEMENT_PLUS)
        else:
            UIProxy._asWidgetClose(self, widgetId, multiID)

    def onClickDoneAchievement(self, *arg):
        gameglobal.rds.ui.achvment.getAchieveData()

    @ui.scenarioCallFilter()
    @ui.callAfterTime(1)
    def showAchiPlus(self, plusStr):
        self.achievePlusStr = plusStr
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACHIEVEMENT_PLUS)
