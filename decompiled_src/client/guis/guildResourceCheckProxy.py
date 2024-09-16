#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildResourceCheckProxy.o
import BigWorld
import gamelog
import uiConst
import events
from uiProxy import UIProxy

class GuildResourceCheckProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildResourceCheckProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RESOURCE_CHECK, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_RESOURCE_CHECK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_RESOURCE_CHECK)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_RESOURCE_CHECK)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        guildResourcesList = getattr(BigWorld.player(), 'guildResourcesList', [])
        listLen = len(guildResourcesList)
        self.widget.txt0.text = guildResourcesList[0] if 0 < listLen else 0
        self.widget.txt1.text = guildResourcesList[1] if 1 < listLen else 0
        self.widget.txt2.text = guildResourcesList[2] if 2 < listLen else 0

    def handleConfirmBtnClick(self, *args):
        p = BigWorld.player()
        guildResourcesList = getattr(p, 'guildResourcesList', [])
        gamelog.info('jbx:applyWingWorldYabiao', guildResourcesList)
        p.applyYabiao()
        self.hide()
