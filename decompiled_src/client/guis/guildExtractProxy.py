#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildExtractProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
from uiProxy import UIProxy
from data import guild_factory_product_data as GFPD

class GuildExtractProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildExtractProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.productId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_EXTRACT, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_EXTRACT:
            self.mediator = mediator
            self.refreshInfo()

    def show(self, productId):
        self.productId = productId
        if self.mediator:
            self.refreshInfo()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_EXTRACT)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_EXTRACT)

    def reset(self):
        self.productId = 0

    def refreshInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            productInfo = GFPD.data.get(self.productId, {})
            factory = guild._getFactory(productInfo.get('type', gametypes.GUILD_FACTORY_PRODUCT_MACHINE))
            itemId = productInfo.get('itemId', 0)
            itemInfo = uiUtils.getGfxItemById(itemId)
            itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
            itemInfo['stockNum'] = factory.product.get(self.productId, 0)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(itemInfo, True))

    def onConfirm(self, *arg):
        num = int(arg[3][0].GetNumber())
        BigWorld.player().cell.fetchGuildFactoryProduct(self.productId, num)
        self.hide()
