#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaCommonTipsProxy.o
import BigWorld
import uiConst
from uiProxy import UIProxy

class ArenaCommonTipsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaCommonTipsProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENA_COMMON_TIPS, self.hide)

    def reset(self):
        self.tipsType = 0
        self.currentPanel = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ARENA_COMMON_TIPS:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENA_COMMON_TIPS)

    def show(self, tipsType = uiConst.ARENA_MATCH_WAIT):
        self.tipsType = tipsType
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENA_COMMON_TIPS)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.miniBtn

    def refreshInfo(self):
        if not self.widget:
            return
        panelPos = [27, 75]
        if self.currentPanel:
            self.widget.removeChild(self.currentPanel)
        if self.tipsType == uiConst.ARENA_MATCH_WAIT:
            self.currentPanel = self.widget.getInstByClsName('ArenaCommonTips_matchWait')
        self.currentPanel.x = panelPos[0]
        self.currentPanel.y = panelPos[1]
        self.widget.addChild(self.currentPanel)
