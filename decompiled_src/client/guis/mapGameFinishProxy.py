#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mapGameFinishProxy.o
import BigWorld
import uiConst
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASUtils
from data import map_game_config_data as MGCD
RESULT_SUCC = 1
RESULT_FAIL = 0

class MapGameFinishProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameFinishProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_FINISH, self.hide)

    def reset(self):
        self.timer = None
        self.result = 0
        self.content = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_FINISH:
            self.widget = widget
            self.delTimer()
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.delTimer()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_FINISH)

    def show(self, succ, content):
        self.result = succ
        self.content = content
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_FINISH)

    def initUI(self):
        ASUtils.setHitTestDisable(self.widget.mainMc, True)
        if self.result == RESULT_SUCC:
            self.widget.mainMc.gotoAndStop('victory')
        else:
            self.widget.mainMc.gotoAndStop('defeat')
        self.widget.mainMc.content.text = self.content
        self.addTimer()

    def refreshInfo(self):
        if not self.widget:
            self.delTimer()
            return

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(5, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        self.hide()

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None
