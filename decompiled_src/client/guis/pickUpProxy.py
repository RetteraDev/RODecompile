#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pickUpProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import ui
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from guis import hotkeyProxy
from guis import uiUtils
from cdata import game_msg_def_data as GMDD

class PickUpProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(PickUpProxy, self).__init__(uiAdapter)
        self.type = 'pickUp'
        self.bindType = 'pickUp'
        self.modelMap = {'pickItem': self.onPickItem,
         'pickAllItem': self.onPickAllItem}
        self.mediator = None
        self.boxId = None
        self.items = None
        self.isBusiness = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_PICK_UP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PICK_UP:
            self.mediator = mediator
            self.refreshItemList()
            _, _, desc = hotkeyProxy.getPickAsKeyContent()
            return GfxValue(gbk2unicode(gameStrings.TEXT_PICKUPPROXY_36 % desc))

    def reset(self):
        self.boxId = None
        self.items = None
        self.isBusiness = False

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PICK_UP)

    def hide(self, destroy = True):
        if self.isBusiness and self.boxId:
            box = BigWorld.entities.get(self.boxId)
            if box:
                box.cell.leaveBox()
        super(PickUpProxy, self).hide(destroy)

    def hideById(self, boxId):
        if self.boxId == boxId and self.mediator:
            self.hide()

    def show(self, boxId, items, isBusiness):
        self.boxId = boxId
        self.items = items
        self.isBusiness = isBusiness
        if not items:
            if self.mediator:
                self.hide()
            return
        if self.mediator:
            self.refreshItemList()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PICK_UP)

    def getSlotID(self, key):
        return (0, int(key[11:]))

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        _, pos = self.getSlotID(key)
        if pos >= len(self.items):
            return
        it = self.items[pos]
        ret = gameglobal.rds.ui.inventory.GfxToolTip(it)
        return ret

    def refreshItemList(self):
        if self.mediator:
            if not self.items:
                self.hide()
                return
            itemList = []
            for pos in xrange(len(self.items)):
                it = self.items[pos]
                itemInfo = uiUtils.getGfxItem(it)
                itemInfo['itemName'] = uiUtils.getItemColorNameByItem(it, length=9)
                itemList.append(itemInfo)

            self.mediator.Invoke('refreshItemList', uiUtils.array2GfxAarry(itemList, True))

    def onPickItem(self, *arg):
        idx = int(arg[3][0].GetNumber())
        self.pickOneItem(idx, const.CONT_NO_PAGE, const.CONT_NO_POS)

    @ui.callFilter(1, False)
    def pickOneItem(self, idx, dstPg, dstPos):
        it = self.items[idx]
        if it == None:
            return
        elif self.boxId == None:
            return
        else:
            box = BigWorld.entities.get(self.boxId)
            if not box:
                return
            p = BigWorld.player()
            if self.isBusiness:
                if gameglobal.rds.ui.guildBusinessBag.canPickUp(1):
                    box.cell.pickBusinessItems([idx])
                else:
                    p.showGameMsg(GMDD.data.GUILD_BUSINESS_ITEM_PICK_UP_ERROR, ())
                return
            if dstPg == const.CONT_NO_PAGE:
                dstPg, dstPos = p.inv.searchBestInPages(it.id, it.cwrap, it)
                if dstPg == const.CONT_NO_PAGE:
                    p.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())
                    return
            box.cell.confirmPickOneItem(it.uuid, dstPg, dstPos)
            return

    @ui.callFilter(1, False)
    def onPickAllItem(self, *arg):
        if self.boxId == None:
            return
        else:
            box = BigWorld.entities.get(self.boxId)
            if not box:
                return
            if self.isBusiness:
                if gameglobal.rds.ui.guildBusinessBag.canPickUp(len(self.items)):
                    itemList = range(len(self.items))
                    box.cell.pickBusinessItems(itemList)
                else:
                    BigWorld.player().showGameMsg(GMDD.data.GUILD_BUSINESS_ITEM_PICK_UP_ERROR, ())
                return
            box.cell.confirmPickAllItem()
            return

    def updateByOne(self, boxId, itemUUID):
        if self.boxId != boxId:
            return
        pos = 0
        itemLen = len(self.items)
        while pos < itemLen:
            it = self.items[pos]
            if it.uuid == itemUUID:
                self.items.pop(pos)
                break
            pos += 1

        if len(self.items) == 0:
            self.hide()
        else:
            self.refreshItemList()

    def updateByList(self, boxId, itemUUIDs):
        if self.boxId != boxId:
            return
        pos = 0
        itemLen = len(self.items)
        while pos < itemLen:
            it = self.items[pos]
            if it.uuid not in itemUUIDs:
                self.items.pop(pos)
                itemLen -= 1
            else:
                pos += 1

        if len(self.items) == 0:
            self.hide()
        else:
            self.refreshItemList()
