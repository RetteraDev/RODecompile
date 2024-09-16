#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/digongLeaderSettingProxy.o
import gameglobal
from uiProxy import UIProxy
from guis import uiConst

class DigongLeaderSetting(UIProxy):

    def __init__(self, uiAdapter):
        super(DigongLeaderSetting, self).__init__(uiAdapter)
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_DIGONG_LEADER_SETTING, self.onClose)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DIGONG_LEADER_SETTING:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DIGONG_LEADER_SETTING)

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DIGONG_LEADER_SETTING)

    def onGetLeaderSettingInfo(self, *arg):
        pass
