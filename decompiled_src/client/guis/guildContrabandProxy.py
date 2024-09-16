#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildContrabandProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from data import sale_business_data as SBD
from data import sale_business_reverse_data as SBRD
from cdata import game_msg_def_data as GMDD

class GuildContrabandProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildContrabandProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.entityId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_CONTRABAND, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_CONTRABAND:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_CONTRABAND)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.entityId = 0

    def show(self, entityId):
        self.entityId = entityId
        p = BigWorld.player()
        if not p.zaijuBag.getBlackItemInfo():
            p.showGameMsg(GMDD.data.GUILD_BUSINESS_NO_BLACK_ITEM, ())
            self.hide()
            return
        if self.mediator:
            self.refreshInfo()
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_CONTRABAND)

    def refreshInfo(self):
        if self.mediator:
            info = {}
            blackItems = BigWorld.player().zaijuBag.getBlackItemInfo()
            totalCash = 0
            itemList = []
            for itemId in blackItems.iterkeys():
                count = len(blackItems[itemId])
                itemInfo = uiUtils.getGfxItemById(itemId, count)
                totalCash += SBD.data.get(SBRD.data.get(itemId, 0), {}).get('blackPrice', 0) * count
                itemList.append(itemInfo)

            info['itemList'] = itemList
            info['totalCash'] = format(totalCash, ',')
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        p = BigWorld.player()
        blackItems = p.zaijuBag.getBlackItemInfo()
        saleIds = []
        positions = []
        for itemId in blackItems.iterkeys():
            count = len(blackItems[itemId])
            saleIds.extend([SBRD.data.get(itemId, 0)] * count)
            positions.extend(blackItems[itemId])

        p.sellBusinessItemToNpc(self.entityId, saleIds, positions, True)
        self.hide()
