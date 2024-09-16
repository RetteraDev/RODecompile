#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildChangeNameProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
from uiProxy import UIProxy

class GuildChangeNameProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildChangeNameProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_CHANGE_NAME, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_CHANGE_NAME:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_CHANGE_NAME)

    def show(self):
        if not self.widget:
            self.uiAdapter.funcNpc.close()
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_CHANGE_NAME)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.yesBtn.addEventListener(events.BUTTON_CLICK, self.handleYesBtnClick, False, 0, True)
        self.widget.noBtn.addEventListener(events.BUTTON_CLICK, self.handleNoBtnClick, False, 0, True)

    def handleYesBtnClick(self, *args):
        gamelog.info('jbx:handleYesBtnClick')
        if not self.widget.txtNewName.text:
            return
        BigWorld.player().cell.applyRenameGuildAfterGuildMerger(self.widget.txtNewName.text)
        self.hide()

    def handleNoBtnClick(self, *args):
        gamelog.info('jbx:handleNoBtnClick')
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
