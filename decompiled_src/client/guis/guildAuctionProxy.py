#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildAuctionProxy.o
import BigWorld
import gameglobal
import uiConst
import ui
import events
from uiTabProxy import UITabProxy
from cdata import game_msg_def_data as GMDD

class GuildAuctionProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(GuildAuctionProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_AUCTION, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_AUCTION:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)

    def clearWidget(self):
        super(GuildAuctionProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_AUCTION)

    def reset(self):
        super(GuildAuctionProxy, self).reset()

    def clearAll(self):
        self.uiAdapter.guildAuctionGuild.clearAll()
        self.uiAdapter.guildAuctionWorld.clearAll()

    def _getTabList(self):
        return [{'tabIdx': uiConst.GUILD_AUCTION_TAB_GUILD,
          'tabName': 'tabBtn0',
          'view': 'GuildAuctionGuildWidget',
          'proxy': 'guildAuctionGuild'}, {'tabIdx': uiConst.GUILD_AUCTION_TAB_WORLD,
          'tabName': 'tabBtn1',
          'view': 'GuildAuctionWorldWidget',
          'proxy': 'guildAuctionWorld'}]

    def show(self, showTabIndex):
        if not gameglobal.rds.configData.get('enableGuildConsign', False):
            BigWorld.player().showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        self.showTabIndex = showTabIndex
        if self.widget:
            self.widget.swapPanelToFront()
            self.widget.setTabIndex(self.showTabIndex)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_AUCTION)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()

    def refreshInfo(self):
        if not self.widget:
            return
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    @ui.uiEvent(uiConst.WIDGET_GUILD_AUCTION, events.EVENT_TIANBI_COIN_CHANGED)
    def refreshTianbiInfo(self, event):
        if not self.widget:
            return
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshTianbiInfo'):
            proxy.refreshTianbiInfo()
