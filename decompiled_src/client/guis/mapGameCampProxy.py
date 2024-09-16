#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameCampProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from asObject import ASUtils
from data import map_game_config_data as MGCD

class MapGameCampProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameCampProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_CAMP, self.hide)

    def reset(self):
        self.camp = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_CAMP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        gameglobal.rds.ui.mapGameMapV2.initMapPos()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_CAMP)

    def show(self, campId):
        self.camp = campId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_CAMP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.redDesc.tf.htmlText = MGCD.data.get('redCampDesc', '')
        self.widget.blackDesc.tf.htmlText = MGCD.data.get('blackCampDesc', '')

    def refreshInfo(self):
        if not self.widget:
            return
        if self.camp == 2:
            self.widget.redMc.visible = True
            self.widget.blackMc.visible = False
            ASUtils.callbackAtFrame(self.widget.redMc, 150, self.afterSelectCamp)
        elif self.camp == 1:
            self.widget.redMc.visible = False
            self.widget.blackMc.visible = True
            ASUtils.callbackAtFrame(self.widget.blackMc, 150, self.afterSelectCamp)
        else:
            self.widget.redMc.visible = False
            self.widget.blackMc.visible = False

    def afterSelectCamp(self, *args):
        if self.camp == 2:
            self.widget.redMc.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onHide, False, 0, True)
        elif self.camp == 1:
            self.widget.blackMc.confirmBtn.addEventListener(events.MOUSE_CLICK, self.onHide, False, 0, True)

    def onHide(self, *arg):
        self.hide()
