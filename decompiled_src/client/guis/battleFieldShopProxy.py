#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/battleFieldShopProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import const
import gameglobal
import uiConst
import gamelog
from uiProxy import SlotDataProxy
from guis import uiUtils
from ui import gbk2unicode
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from cdata import font_config_data as FCD

class BattleFieldShopProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(BattleFieldShopProxy, self).__init__(uiAdapter)
        self.modelMap = {'getMoney': self.onGetMoney,
         'getItemList': self.onGetItemList,
         'changePage': self.onChangePage,
         'getPageCount': self.onGetPageCount,
         'buySingleItem': self.onBuySingleItem,
         'buyFailed': self.onBuyFailed}
        self.bindType = 'battlefield'
        self.type = 'battlefield'
        self.show = False
        self.mediator = None
        self.shopItems = []
        self.pagePosCnt = const.SHOP_WIDTH * const.SHOP_HEIGHT
        self.currPage = None
        self.pageCount = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_BATTLE_FIELD_SHOP, Functor(self.hide, True))

    def openShop(self, items):
        self.show = True
        self.pageCount = len(items) / self.pagePosCnt + 1
        self.currPage = 0
        self.shopItems = items
        self.uiAdapter.loadWidget(uiConst.WIDGET_BATTLE_FIELD_SHOP, layoutType=uiConst.LAYOUT_DEFAULT)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BATTLE_FIELD_SHOP:
            self.mediator = mediator
            self.setPageItem(0)

    def _getItemsByPage(self, page):
        if page >= self.pageCount:
            return []
        if not self.shopItems:
            return []
        startPos = page * self.pagePosCnt
        endPos = min(startPos + self.pagePosCnt, len(self.shopItems))
        res = []
        for pos in range(startPos, endPos):
            res.append(self.shopItems[pos])

        return res

    def _getItemByPos(self, page, pos):
        tPos = page * self.pagePosCnt + pos
        if tPos >= len(self.shopItems):
            return None
        else:
            return self.shopItems[tPos]

    def setPageItem(self, page):
        if not self.mediator:
            return
        itemPage = self.movie.CreateArray()
        itemList = self._getItemsByPage(page)
        for pos in xrange(len(itemList)):
            item = itemList[pos]
            obj = self.movie.CreateObject()
            data = ID.data.get(item.id, {})
            name = data.get('name', 'error')
            path = uiUtils.getItemIconFile40(item.id)
            obj.SetMember('name', GfxValue(gbk2unicode(name)))
            obj.SetMember('value', GfxValue(str(item.battleFieldScoreConsume)))
            obj.SetMember('path', GfxValue(path))
            if item.remainNum >= 0:
                num = item.remainNum
            else:
                num = 999
            obj.SetMember('num', GfxValue(num))
            if hasattr(item, 'quality'):
                quality = item.quality
            else:
                quality = data.get('quality', 1)
            color = '0x' + FCD.data.get(('item', quality), {}).get('color', '#ffffff')[1:]
            qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'white')
            obj.SetMember('qualitycolor', GfxValue(qualitycolor))
            obj.SetMember('color', GfxValue(color))
            obj.SetMember('state', GfxValue(uiConst.ITEM_NORMAL))
            itemPage.SetElement(pos, obj)

        obj = self.movie.CreateObject()
        obj.SetMember('money', GfxValue(str(BigWorld.player().battleFieldScore)))
        obj.SetMember('page', GfxValue(page + 1))
        itemPage.SetElement(pos + 1, obj)
        if self.mediator:
            self.mediator.Invoke('setPageItem', itemPage)

    def onBuyFailed(self, *arg):
        p = BigWorld.player()
        p.showGameMsg(GMDD.data.LACK_BATTALEFIELD_SCORE, ())

    def onBuySingleItem(self, *arg):
        page = int(arg[3][0].GetNumber())
        pos = int(arg[3][1].GetNumber())
        it = self._getItemByPos(page, pos)
        if not it:
            gamelog.error('shopProxy, no data in infoDic ', page, pos)
            return
        p = BigWorld.player()
        bagPage, bagPos = p.inv.searchBestInPages(it.id, 1, it)
        if bagPage == const.CONT_NO_PAGE or bagPos == const.CONT_NO_POS:
            p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())
            return
        p.cell.buyBattleFileItem(page, pos, 1)
        gameglobal.rds.sound.playSound(gameglobal.SD_26)

    def onChangePage(self, *arg):
        self.currPage = int(arg[3][0].GetNumber())
        self.setPageItem(self.currPage)

    def onGetPageCount(self, *arg):
        self.show = True
        return GfxValue(self.pageCount)

    def onRegisterShop(self, *arg):
        self.mc = arg[3][0]
        self.setPageItem(0)

    def onGetMoney(self, *arg):
        return GfxValue(str(BigWorld.player().battleFieldScore))

    def refreshMoney(self):
        if self.mediator != None:
            self.mediator.Invoke('refreshMoney')

    def onGetItemList(self, *arg):
        itemList = self.movie.CreateArray()
        for i in range(0, 20):
            obj = self.movie.CreateObject()
            obj.SetMember('name', GfxValue(gbk2unicode(gameStrings.TEXT_BATTLEFIELDSHOPPROXY_171)))
            obj.SetMember('value', GfxValue(str((i + 1) * 100)))
            itemList.SetElement(i, obj)

        return itemList

    def setPageCount(self):
        self.mediator.Invoke('setPageCount', GfxValue(self.pageCount))

    def onCloseShop(self, *arg):
        self.show = False
        self.mediator = None
        self.shopItems = []
        self.pageCount = 0
        self.currPage = None

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BATTLE_FIELD_SHOP)

    def reset(self):
        self.onCloseShop()

    def getSlotID(self, key):
        return (self.currPage, int(key[16:]))

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        it = self._getItemByPos(page, pos)
        if it == None:
            return
        else:
            return self.uiAdapter.inventory.GfxToolTip(it, const.ITEM_IN_NONE)

    def updateSingleItem(self, page, pos, remainNum):
        it = self._getItemByPos(page, pos)
        if not it:
            return
        it.remainNum = remainNum
        if page == self.currPage:
            self.mediator.Invoke('setSingleItem', (GfxValue(page), GfxValue(pos), GfxValue(remainNum)))
