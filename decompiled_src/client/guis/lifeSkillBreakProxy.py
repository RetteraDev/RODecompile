#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/lifeSkillBreakProxy.o
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import uiUtils

class LifeSkillBreakProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LifeSkillBreakProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'getData': self.onGetData}
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_LIFE_SKILL_BREAK:
            self.mediator = mediator

    def show(self, index):
        if self.mediator:
            return
        self.index = index
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LIFE_SKILL_BREAK, True)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LIFE_SKILL_BREAK)

    def reset(self):
        self.mediator = None
        self.index = 0

    def onClickClose(self, *args):
        self.hide()

    def onGetData(self, *args):
        ret = {}
        ret['index'] = self.index
        return uiUtils.dict2GfxDict(ret, True)
