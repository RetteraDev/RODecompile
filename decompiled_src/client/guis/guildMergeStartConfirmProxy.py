#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMergeStartConfirmProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
from gamestrings import gameStrings
from uiProxy import UIProxy
from data import sys_config_data as SCD

class GuildMergeStartConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMergeStartConfirmProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MERGE_START_CONFIRM, self.hide)

    def reset(self):
        self.data = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_MERGE_START_CONFIRM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_MERGE_START_CONFIRM)

    def show(self, name, leaderRole, r, level, onlineMaxNum):
        self.data = {'guildName': name,
         'name': leaderRole,
         'rank': r,
         'level': level,
         'txtOnlineNum': onlineMaxNum}
        if not self.widget:
            self.uiAdapter.funcNpc.close()
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_MERGE_START_CONFIRM)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.txtDesc.htmlText = gameStrings.GUILD_MERGE_START_CONFIRM_TXT % self.data.get('guildName', '')
        self.widget.txtGuildName.text = self.data.get('name', '')
        self.widget.txtRank.text = self.data.get('rank', 0)
        self.widget.txtLv.text = self.data.get('level', 0)
        self.widget.txtOnlineNum.text = self.data.get('txtOnlineNum', 0)

    def handleConfirmBtnClick(self, *args):
        p = BigWorld.player()
        gamelog.info('jbx:applyGuildMerger', self.uiAdapter.guildMergeStart.guildDbid)
        p.cell.applyGuildMerger(self.uiAdapter.guildMergeStart.guildDbid)
        self.hide()
