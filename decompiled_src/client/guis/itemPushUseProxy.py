#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemPushUseProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import utils
from uiProxy import UIProxy
from guis import uiUtils
from callbackHelper import Functor
from item import Item
from helpers import cellCmd
from data import item_data as ID
from data import equip_prefix_prop_data as EPPD
from cdata import game_msg_def_data as GMDD
from cdata import pack_data as PD
from data import use_item_wish_data as UIWD
TYPE_NORMAL = 1
TYPE_WABAO = 2

class ItemPushUseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ItemPushUseProxy, self).__init__(uiAdapter)
        self.modelMap = {'useItem': self.onUseItem,
         'initData': self.onInitData,
         'overWidget': self.onOverWidget,
         'outWidget': self.onOutWidget}
        self.mediator = None
        self.itemId = None
        self.uuid = None
        self.item = None
        self.isPush = False
        self.isClickPush = False
        self.isActionClick = False
        self.callBackHandler = None
        self.questPanelCloseShow = None
        self.isSpecial = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_PUSH_USE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ITEM_PUSH_USE:
            self.mediator = mediator

    def checkAndShow(self):
        if self.questPanelCloseShow:
            self.show(self.questPanelCloseShow)

    def checkCanShow(self, uuId):
        p = BigWorld.player()
        item, _, _ = p.inv.findItemByUUID(uuId)
        if item and item.type == Item.BASETYPE_PACK:
            newSize = PD.data.get(item.id, {}).get('size', 0)
            for pos in xrange(0, p.inv.enabledPackSlotCnt):
                i = p.bagBar.getQuickVal(0, pos)
                if i == const.CONT_EMPTY_VAL:
                    return True
                oldSize = PD.data.get(i.id, {}).get('size', 0)
                if newSize > oldSize:
                    return True

            return False
        return True

    def show(self, uuId, forceShow = False):
        if not self.checkCanShow(uuId):
            return
        elif self.uiAdapter.quest.isShow:
            self.questPanelCloseShow = uuId
            return
        else:
            self.questPanelCloseShow = None
            self.isSpecial = forceShow
            if self.mediator == None and (self.isPush and not self.isActionClick or forceShow):
                p = BigWorld.player()
                self.uuid = uuId
                self.item, _, _ = p.inv.findItemByUUID(self.uuid)
                self.isClickPush = False
                if self.item:
                    self.itemId = self.item.id
                    if ID.data.get(self.itemId, {}).get('usePush', None):
                        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ITEM_PUSH_USE)
                        self.startTimeOut()
            return

    def clearWidget(self):
        self.mediator = None
        self.itemId = None
        self.uuid = None
        self.item = None
        self.isSpecial = False
        self.cancelTimeOut()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ITEM_PUSH_USE)

    def onUseItem(self, *args):
        p = BigWorld.player()
        item, bagPage, bagPos = p.inv.findItemByUUID(self.uuid)
        if bagPos != const.CONT_NO_POS and bagPage != const.CONT_NO_PAGE:
            if item and gameglobal.rds.ui.treasureBoxWish.checkShowTreasureBoxWish(item.id) and not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_TREASURE_BOX_WISH_CBT):
                gameglobal.rds.ui.inventory.showTreasureBoxWish(item, uiConst.CHECK_ONCE_TYPE_TREASURE_BOX_WISH_CBT)
            elif item and item.type == Item.BASETYPE_PACK:
                index = -1
                size = 1000
                newSize = PD.data.get(item.id, {}).get('size', 0)
                for pos in xrange(0, p.inv.enabledPackSlotCnt):
                    i = p.bagBar.getQuickVal(0, pos)
                    if i == const.CONT_EMPTY_VAL:
                        index = pos
                        size = 0
                        break
                    oldSize = PD.data.get(i.id, {}).get('size', 0)
                    if newSize > oldSize and oldSize < size:
                        index = pos
                        size = oldSize

                if index != -1:
                    cellCmd.equipPack(bagPage, bagPos, index)
            else:
                self.isClickPush = True
                p.useBagItem(bagPage, bagPos)
        else:
            p.showGameMsg(GMDD.data.PUSH_USED_MSG, ())
        self.hide()

    def onInitData(self, *args):
        if not self.item:
            self.hide()
            return
        dataObj = {}
        dataObj['iconPath'], dataObj['color'] = uiUtils.getItemDataByItemId(self.itemId)
        itemName = self.item.name
        if hasattr(self.item, 'prefixInfo'):
            for prefixItem in EPPD.data[self.item.prefixInfo[0]]:
                if prefixItem['id'] == self.item.prefixInfo[1]:
                    if utils.isInternationalVersion():
                        itemName = self.item.name + prefixItem['name']
                    else:
                        itemName = prefixItem['name'] + self.item.name
                    break

        dataObj['itemName'] = itemName
        dataObj['usePushType'] = ID.data.get(self.itemId, {}).get('usePush')
        if dataObj['usePushType'] == TYPE_WABAO:
            dataObj['itemName'] = uiUtils.getItemColorName(self.itemId)
        return uiUtils.dict2GfxDict(dataObj, True)

    def onGetToolTip(self, *arg):
        return gameglobal.rds.ui.inventory.GfxToolTip(self.item)

    def cancelTimeOut(self):
        if self.callBackHandler:
            BigWorld.cancelCallback(self.callBackHandler)
            self.callBackHandler = None

    def startTimeOut(self):
        if self.callBackHandler:
            BigWorld.cancelCallback(self.callBackHandler)
        if not self.isSpecial:
            self.callBackHandler = BigWorld.callback(uiConst.ITEM_PUSH_USE_SHOW_TIME, Functor(self.hide))
        else:
            self.callBackHandler = BigWorld.callback(uiConst.ITEM_PUSH_USE_WABAO_SHOW_TIME, Functor(self.hide))

    def onOverWidget(self, *arg):
        self.cancelTimeOut()

    def onOutWidget(self, *arg):
        self.startTimeOut()
