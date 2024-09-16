#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryFireWorkProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
import const
from uiProxy import UIProxy
from guis import uiUtils
from guis import ui
from guis.asObject import ASObject
from guis.asObject import ASUtils
from helpers import cellCmd
from cdata import game_msg_def_data as GMDD

class MarryFireWorkProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryFireWorkProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MARRY_FIRE_WORK, self.hide)

    def reset(self):
        self.itemData = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_FIRE_WORK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        super(MarryFireWorkProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_FIRE_WORK)

    def refreshInfo(self):
        if not self.widget:
            return

    def initUI(self):
        ASUtils.setHitTestDisable(self.widget.fireWorkNode, True)
        self.timer = BigWorld.callback(20, self.hide)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_FIRE_WORK)
