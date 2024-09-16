#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMergeStartProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
from uiProxy import UIProxy
import sys
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import sys_config_data as SCD

class GuildMergeStartProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMergeStartProxy, self).__init__(uiAdapter)
        self.widget = None
        self.guildDbId = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MERGE_START, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_MERGE_START:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_MERGE_START)

    def show(self):
        if not self.widget:
            self.uiAdapter.funcNpc.close()
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_MERGE_START)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.txtGuildName.textField.restrict = '0-9'
        self.widget.txtGuildName.maxChars = 10

    def refreshInfo(self):
        if not self.widget:
            return

    def handleConfirmBtnClick(self, *args):
        try:
            self.guildDbid = int(self.widget.txtGuildName.text)
        except:
            gamelog.error('jbx:parseInt error', self.widget.txtGuildName.text)
            return

        p = BigWorld.player()
        gamelog.info('jbx:queryTargetInfoInGuildMerger', self.guildDbid)
        self.guildDbid and p.base.queryTargetInfoInGuildMerger(self.guildDbid)
        self.hide()
