#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMergePushProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
import gametypes
from guis import uiUtils
from uiProxy import UIProxy
from data import guild_config_data as GCD

class GuildMergePushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMergePushProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MERGE_PUSH, self.close)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_MERGE_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_MERGE_PUSH)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_MERGE_PUSH)

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleRefuseBtnClick, False, 0, True)
        self.widget.txtDesc.htmlText = GCD.data.get('guildMergePushDesc', '')
        self.widget.txtMergeTips.htmlText = GCD.data.get('guildMergePushHow', '')
        self.widget.txtMergeReward.htmlText = GCD.data.get('guildMergePushReward', '')
        self.widget.startMerge.addEventListener(events.BUTTON_CLICK, self.handleStartMergeClick, False, 0, True)
        self.widget.openHelp.addEventListener(events.BUTTON_CLICK, self.handleOpenHelpClick, False, 0, True)
        self.widget.refuseBtn.addEventListener(events.BUTTON_CLICK, self.handleRefuseBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def close(self, isRefuse = True):
        gamelog.info('jbx:refuse', isRefuse)
        p = BigWorld.player()
        self.hide()
        self.hide()
        if isRefuse:
            p.cell.refuseRecommendGuildMergerNotify()

    def handleStartMergeClick(self, *args):
        gamelog.info('jbx:handleStartMergeClick')
        uiUtils.findPosById(GCD.data.get('guildMergeSeekId', 0))
        self.close(False)

    def handleOpenHelpClick(self, *args):
        gamelog.info('jbx:handleOpenHelpClick')
        self.uiAdapter.guildMergeHelp.show()
        self.close(False)

    def handleRefuseBtnClick(self, *args):
        gamelog.info('jbx:handleRefuseBtnClick')
        self.close(True)
