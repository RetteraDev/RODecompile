#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/famousSeasonIntroProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from data import famous_general_config_data as FGCD

class FamousSeasonIntroProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FamousSeasonIntroProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_FAMOUS_SEASON_INTRO, self.hidePanel)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.widget.intro.htmlText = FGCD.data.get('seasonIntro', '')
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleHidePanel)
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleHidePanel)

    def show(self):
        if self.widget:
            self.clearWidget()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAMOUS_SEASON_INTRO)

    def hidePanel(self):
        self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAMOUS_SEASON_INTRO)

    def handleHidePanel(self, *args):
        self.clearWidget()
