#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/guildShopBuyProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
from uiProxy import UIProxy
from data import guild_shop_data as GSD
from cdata import game_msg_def_data as GMDD

class GuildShopBuyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildShopBuyProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'changeNum': self.onChangeNum,
         'clickConfirm': self.onClickConfirm}
        self.mediator = None
        self.item = None
        self.shopType = 0
        self.page = 0
        self.pos = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_SHOP_BUY, self.hide)

    def show(self, item, shopType, page, pos):
        self.item = item
        self.shopType = shopType
        self.page = page
        self.pos = pos
        if self.mediator:
            self.refreshInfo()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_SHOP_BUY)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_SHOP_BUY:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_SHOP_BUY)

    def reset(self):
        self.item = None
        self.shopType = 0
        self.page = 0
        self.pos = 0

    def onInitData(self, *arg):
        self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            if not self.item:
                return
            itemInfo = uiUtils.getGfxItem(self.item)
            itemInfo['itemId'] = self.item.id
            itemInfo['itemName'] = uiUtils.getItemColorName(self.item.id)
            itemInfo['count'] = str(itemInfo['count'])
            limit = GSD.data[self.item.gsid].get('limit', 0)
            itemInfo['limit'] = '每天限购%d个' % limit if limit > 0 else '每天不限购买'
            itemInfo['contrib'] = uiUtils.convertNumStr(p.guildContrib, self.item.contrib, False, needThousand=True)
            info['itemInfo'] = itemInfo
            info['maxNum'] = min(self.item.mwrap, self.item.cwrap)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onChangeNum(self, *arg):
        num = int(arg[3][0].GetNumber())
        info = {}
        info['totalCost'] = uiUtils.convertNumStr(BigWorld.player().guildContrib, self.item.contrib * num, False, needThousand=True)
        info['confirmEnable'] = num > 0
        return uiUtils.dict2GfxDict(info, True)

    def onClickConfirm(self, *arg):
        num = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if num <= self.item.mwrap:
            p.cell.buyGuildShopItem(self.shopType + 1, self.page, self.pos, self.item.uuid, num, self.item.id, getattr(self.item, 'gsid'))
        elif num > self.item.mwrap:
            p.showGameMsg(GMDD.data.SHOP_BUY_ITEM_OVER_MWRAP, ())
        self.hide()
