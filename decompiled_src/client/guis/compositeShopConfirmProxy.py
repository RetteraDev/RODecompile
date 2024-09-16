#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/compositeShopConfirmProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import keys
from ui import gbk2unicode
from uiProxy import UIProxy
from appSetting import Obj as AppSettings
from callbackHelper import Functor
from guis import uiUtils
from data import fame_data as FD
from data import composite_shop_data as CSD
from cdata import game_msg_def_data as GMDD

class CompositeShopConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CompositeShopConfirmProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm,
         'getData': self.onGetData,
         'setCheck': self.onSetCheck,
         'getChk': self.onGetChk}
        self.mediator = None
        self.nPage = const.CONT_NO_PAGE
        self.nItem = const.CONT_NO_POS
        self.message = ''

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_COMPOSITE_SHOP_COMFIRM:
            self.mediator = mediator

    def show(self, nPage, nItem):
        if self.mediator:
            return
        self.nPage = nPage
        self.nItem = nItem
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_COMPOSITE_SHOP_COMFIRM, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_COMPOSITE_SHOP_COMFIRM)

    def onGetChk(self, *args):
        return GfxValue(gameglobal.rds.ui.compositeShop.confirmStatus)

    def onSetCheck(self, *args):
        gameglobal.rds.ui.compositeShop.confirmStatus = args[3][0].GetBool()
        AppSettings[keys.SET_COMPOSITE_SHOP_CONFIRM] = gameglobal.rds.ui.compositeShop.confirmStatus
        AppSettings.save()
        gameglobal.rds.ui.yunChuiShop.updateSet()
        gameglobal.rds.ui.compositeShop.updateCheckBox()

    def reset(self):
        super(self.__class__, self).reset()
        self.message = ''
        self.nPage = const.CONT_NO_PAGE
        self.nItem = const.CONT_NO_POS

    def onClickConfirm(self, *arg):
        p = BigWorld.player()
        gameglobal.rds.ui.compositeShop.confirmStatus = int(arg[3][0].GetBool())
        AppSettings[keys.SET_COMPOSITE_SHOP_CONFIRM] = gameglobal.rds.ui.compositeShop.confirmStatus
        AppSettings.save()
        compositeShop = gameglobal.rds.ui.compositeShop
        yunChuiShop = gameglobal.rds.ui.yunChuiShop
        compositeShop.updateCheckBox()
        yunChuiShop.updateSet()
        i = BigWorld.player().inv.getQuickVal(self.nPage, self.nItem)
        if i == const.CONT_EMPTY_VAL:
            self.hide()
            return
        canSell, fameData = i.canSellToCompositeShopId(p.openShopId)
        canSellNormalToCompositeShop = i.canSellNormalToCompositeShop(p.openShopId)
        if compositeShop.mediator:
            npc = BigWorld.entities.get(compositeShop.npcId)
        else:
            npc = BigWorld.entities.get(yunChuiShop.npcId)
        if yunChuiShop.mediator and yunChuiShop.isPrivateShop or compositeShop.isPrivateShop():
            functorSell = Functor(p.base.sellPrivateShopItem, p.openShopId, self.nPage, self.nItem, i.cwrap, False)
        else:
            functorSell = Functor(npc.cell.compositeShopBuy, p.openShopId, self.nPage, self.nItem, i.cwrap, False)
        if canSell or canSellNormalToCompositeShop:
            if i.isRuneEquip() and getattr(i, 'runeData', ()):
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_COMPOSITESHOPCONFIRMPROXY_92, functorSell)
            else:
                functorSell()
        else:
            p.showGameMsg(GMDD.data.COMPOSITESHOP_FORBIDDEN_SELL_SHOP_BYBACK, ())
        self.hide()

    def onClickClose(self, *arg):
        self.hide()

    def onGetData(self, *arg):
        i = BigWorld.player().inv.getQuickVal(self.nPage, self.nItem)
        shopId = BigWorld.player().openShopId
        if i != const.CONT_EMPTY_VAL and (gameglobal.rds.ui.compositeShop.mediator or gameglobal.rds.ui.yunChuiShop.mediator):
            canSell, fameData = i.canSellToCompositeShopId(shopId)
            if canSell:
                fameId, fameNum = fameData
                if i.canBuyBack(const.SHOP_TYPE_COMPOSITE):
                    return GfxValue(gbk2unicode(gameStrings.TEXT_COMPOSITESHOPCONFIRMPROXY_112 % (i.name, fameNum, FD.data[fameId]['name'])))
                else:
                    return GfxValue(gbk2unicode(gameStrings.TEXT_COMPOSITESHOPCONFIRMPROXY_114 % (i.name, fameNum, FD.data[fameId]['name'])))
            elif i.canSellNormalToCompositeShop(shopId):
                shopName = CSD.data.get(shopId, {}).get('shopName', '')
                msg = uiUtils.getTextFromGMD(GMDD.data.SELL_NORMAL_TO_COMPOSITESHOP_CONFIRM, '%s %s') % (i.name, shopName)
                return GfxValue(gbk2unicode(msg))
        self.hide()

    def updateCheckBox(self):
        if self.mediator:
            self.mediator.Invoke('updateCheckBox', GfxValue(gameglobal.rds.ui.compositeShop.confirmStatus))
