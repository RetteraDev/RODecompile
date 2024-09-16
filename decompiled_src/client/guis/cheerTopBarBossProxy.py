#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cheerTopBarBossProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from asObject import TipManager
from gamestrings import gameStrings
from data import wing_world_config_data as WWCD

class CheerTopBarBossProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CheerTopBarBossProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_CHEER_TOPBAR_BOSS, self.hide)

    def reset(self):
        self.teamName = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_CHEER_TOPBAR_BOSS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_CHEER_TOPBAR_BOSS)

    def show(self, teamName = ''):
        self.teamName = teamName
        if not gameglobal.rds.configData.get('enableWingWorldXinMo', False):
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_CHEER_TOPBAR_BOSS)
        else:
            self.refreshInfo()

    def initUI(self):
        TipManager.addTip(self.widget.personIcon, gameStrings.CHEER_TOP_BAR_PERSON_ICON_TIP)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.teamName0.text = self.teamName
        self.widget.teamName1.text = WWCD.data.get('cheerTopBarBossDesc', '')
        self.widget.personNum.text = getattr(p, 'xinMoAnnalFakeCnt', 0)
