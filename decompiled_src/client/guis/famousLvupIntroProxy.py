#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/famousLvupIntroProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
from uiProxy import UIProxy
from guis import asObject
from cdata import game_msg_def_data as GMDD

class FamousLvupIntroProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FamousLvupIntroProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_FAMOUS_LV_UP_INTRO, self.hidePanel)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.widget.becomeFamousBtn.addEventListener(events.MOUSE_CLICK, self.handleClickBecomeFamous)
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleHidePanel)

    def show(self):
        if self.widget:
            self.clearWidget()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAMOUS_LV_UP_INTRO)

    def hidePanel(self):
        self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAMOUS_LV_UP_INTRO)

    def handleClickBecomeFamous(self, *args):
        if gameglobal.rds.ui.roleInformationJunjie.stage < 0:
            return
        if gameglobal.rds.ui.roleInformationJunjie.stage == gametypes.FAMOUS_GENERAL_STAGE_PREPARE:
            BigWorld.player().showGameMsg(GMDD.data.FAMOUS_GENERAL_NEXT_WEEK_TIP, ())
            return
        BigWorld.player().cell.promote2FamousGeneral()
        self.clearWidget()

    def handleHidePanel(self, *args):
        self.clearWidget()
