#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMergeAcceptProxy.o
import BigWorld
import uiConst
import events
import gamelog
from gamestrings import gameStrings
from uiProxy import UIProxy
from data import guild_config_data as GCD

class GuildMergeAcceptProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMergeAcceptProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MERGE_ACCEPT, self.close)

    def reset(self):
        self.data = {}
        self.leftTime = 60

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_MERGE_ACCEPT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_MERGE_ACCEPT)

    def show(self, fGuildNuid, leaderRole, name):
        self.data = {'fGuildNuid': fGuildNuid,
         'name': leaderRole,
         'guildName': name}
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_MERGE_ACCEPT)

    def close(self, isRefuse = True):
        gamelog.info('jbx:hide, isRefuse', isRefuse)
        p = BigWorld.player()
        fGuildNuid = self.data.get('fGuildNuid')
        gamelog.info('jbx:onApplyGuildMerger', fGuildNuid, not isRefuse)
        p.cell.onApplyGuildMerger(fGuildNuid, not isRefuse)
        self.hide()

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleNoBtnClick, False, 0, True)
        self.widget.txtDesc.htmlText = GCD.data.get('guildMergeAcceptDes', '%s,%s') % (self.data.get('name', ''), self.data.get('guildName', ''))
        self.widget.txtConfirm.htmlText = GCD.data.get('guildMergeAcceptTimeDes', '')
        self.widget.progressBar.maxValue = 60
        self.widget.yesBtn.addEventListener(events.BUTTON_CLICK, self.handleYesBtnClick, False, 0, True)
        self.widget.noBtn.addEventListener(events.BUTTON_CLICK, self.handleNoBtnClick, False, 0, True)
        self.leftTime = 60
        self.countDown()

    def countDown(self):
        if not self.widget:
            return
        if not self.leftTime:
            self.close(True)
            return
        self.widget.progressBar.currentValue = self.leftTime
        self.widget.txtLeftTime.text = gameStrings.GUILD_MERGE_ACCEPT_COUNT_DOWN % self.leftTime
        self.leftTime -= 1
        BigWorld.callback(1, self.countDown)

    def refreshInfo(self):
        if not self.widget:
            return

    def handleYesBtnClick(self, *args):
        gamelog.info('jbx:handleYesBtnClick')
        self.close(False)

    def handleNoBtnClick(self, *args):
        self.close(True)
