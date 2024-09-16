#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBonfireBoxProxy.o
import BigWorld
import uiConst
from uiProxy import UIProxy

class GuildBonfireBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBonfireBoxProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BONFIRE_BOX, self.hide)

    def reset(self):
        self.showTime = 3

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_BONFIRE_BOX:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_BONFIRE_BOX)
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def show(self, showTime):
        self.showTime = showTime
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_BONFIRE_BOX)
        else:
            self.initUI()

    def initUI(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
        self.timer = BigWorld.callback(self.showTime, self.hide)
        self.widget.box.gotoAndPlay(1)
