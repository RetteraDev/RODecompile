#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildAuctionBuyProxy.o
import BigWorld
import uiConst
import uiUtils
import ui
from uiProxy import UIProxy
from gamestrings import gameStrings

class GuildAuctionBuyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildAuctionBuyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_AUCTION_BUY, self.hide)

    def reset(self):
        self.type = uiConst.GUILD_AUCTION_BUY_TYPE_GUILD_BID
        self.itemInfo = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_AUCTION_BUY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_AUCTION_BUY)

    def show(self, type, itemInfo):
        self.type = type
        self.itemInfo = itemInfo
        if self.widget:
            self.refreshInfo()
            self.widget.swapPanelToFront()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_AUCTION_BUY)

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.itemSlot.dragable = False

    def refreshInfo(self):
        if not self.widget:
            return
        if self.type in (uiConst.GUILD_AUCTION_BUY_TYPE_GUILD_BID, uiConst.GUILD_AUCTION_BUY_TYPE_WORLD_BID):
            self.widget.title.textField.text = gameStrings.GUILD_AUCTION_BUY_TITLE_BID
        else:
            self.widget.title.textField.text = gameStrings.GUILD_AUCTION_BUY_TITLE_BUY
        itemId = self.itemInfo.get('itemId', 0)
        self.widget.itemSlot.setItemSlotData(uiUtils.getGfxItemById(itemId, stateFlag=True))
        self.widget.itemName.htmlText = uiUtils.getItemColorName(itemId)
        self.widget.tianbi.text = format(self.itemInfo.get('price', 0), ',')

    def _onConfirmBtnClick(self, e):
        self.realConfirm()

    @ui.checkInventoryLock()
    def realConfirm(self):
        p = BigWorld.player()
        if self.type in (uiConst.GUILD_AUCTION_BUY_TYPE_GUILD_BID, uiConst.GUILD_AUCTION_BUY_TYPE_GUILD_BUY):
            p.base.buyGuildConsignGood(self.itemInfo.get('vendorSource', 0), self.itemInfo.get('uuid', 0), self.itemInfo.get('itemId', 0), self.type in (uiConst.GUILD_AUCTION_BUY_TYPE_GUILD_BID, uiConst.GUILD_AUCTION_BUY_TYPE_WORLD_BID), self.itemInfo.get('price', 0), p.cipherOfPerson)
        else:
            p.base.buyWorldConsignGood(self.itemInfo.get('vendorSource', 0), self.itemInfo.get('uuid', 0), self.itemInfo.get('itemId', 0), self.type in (uiConst.GUILD_AUCTION_BUY_TYPE_GUILD_BID, uiConst.GUILD_AUCTION_BUY_TYPE_WORLD_BID), self.itemInfo.get('price', 0), p.cipherOfPerson)
        self.hide()
