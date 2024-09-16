#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mixFameJewelryProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
from callbackHelper import Functor
from guis import ui
from guis import uiConst
from guis import uiUtils
from guis import events
from uiProxy import SlotDataProxy
from item import Item
from data import fame_data as FD
from data import equip_data as ED
from data import equip_synthesize_data as ESD
from cdata import item_synthesize_set_data as ISSD
from cdata import game_msg_def_data as GMDD

class MixFameJewelryProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(MixFameJewelryProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'clearAllBindings': self.onClearAllBindings,
         'clearPanel': self.onClearPanel,
         'getJewelryItemsInfo': self.onGetJewelryItemsInfo,
         'comfirmMix': self.onComfirmMix,
         'jewelryResultClick': self.onJewelryResultClick,
         'showFit': self.onShowFit}
        self.type = 'mixFameJewelry'
        self.bindType = 'mixFameJewelry'
        self.srcPos = [-1, -1]
        self.mediator = None
        self.item = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_MIX_FAME_JEWELRY, self.onClose)

    def onClearAllBindings(self, *arg):
        self.binding = {}

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MIX_FAME_JEWELRY:
            self.item = None
            self.mediator = mediator
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[14:]), int(idItem[4:]))

    def show(self):
        if not gameglobal.rds.configData.get('enableMixJewelry', False):
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MIX_FAME_JEWELRY)
        if self.mediator:
            self.mediator.Invoke('show')
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.item = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MIX_FAME_JEWELRY)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def clearPanel(self):
        if self.mediator:
            self.item = None
            self.mediator.Invoke('clearPanel')
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def onClearPanel(self, *arg):
        self.item = None

    @ui.uiEvent(uiConst.WIDGET_MIX_FAME_JEWELRY, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onMixFameJewelryItemClick(self, event):
        event.stop()
        it = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if it == None:
            return
        else:
            if self.matchCondition(it):
                self.equipItem(it, nPage, nItem)
            return

    def resetInventoryItemState(self):
        removePage = self.srcPos[0]
        removePos = self.srcPos[1]
        self.srcPos = [-1, -1]
        self.item = None
        gameglobal.rds.ui.inventory.updateSlotState(removePage, removePos)

    def equipItem(self, item, nPageSrc, nItemSrc):
        if self.item:
            self.resetInventoryItemState()
        self.updateItem(item, nPageSrc, nItemSrc)

    def getBonus(self, mixData):
        p = BigWorld.player()
        cashNeed = mixData.get('cashNeed')
        if cashNeed:
            return ('cash', cashNeed, p.cash + p.bindCash)
        fameNeed = mixData.get('fameNeed')
        if fameNeed:
            fameNum = fameNeed[1]
            fameId = fameNeed[0]
            bonusType = FD.data.get(fameId, {}).get('transferToFameOnMaxValIcon', 'fame')
            return (bonusType, fameNum, p.fame.get(fameId, 0))
        return ('cash', 0, 0)

    def getNeedResource(self, srcItemId, mixData):
        itemGroup = mixData.get('materialSetNeed', ())
        groupItems = [ [item.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT), item['itemId'], item['numRange'][0]] for item in ISSD.data.get(itemGroup, []) ]
        return (groupItems[0][0], groupItems[0][1], groupItems[0][2])

    def updateItem(self, item, nPageSrc, nItemSrc):
        self.item = item
        self.srcPos[0] = nPageSrc
        self.srcPos[1] = nItemSrc
        gameglobal.rds.ui.inventory.updateSlotState(self.srcPos[0], self.srcPos[1])
        itemInfo = uiUtils.getGfxItemById(item.id)
        equipData = ED.data.get(item.id, {})
        mixJewelryId = equipData.get('mixJewelryId', ())
        mixData = ESD.data.get(mixJewelryId, {})
        p = BigWorld.player()
        bonusType, needBonus, ownNum = self.getBonus(mixData)
        needItemInfo = {}
        itemTp, itemId, needItemNum = self.getNeedResource(item.id, mixData)
        enableParentCheck = True if itemTp == gametypes.ITEM_MIX_TYPE_PARENT else False
        resultItemId = mixData.get('result', 0)
        resultItemInfo = uiUtils.getGfxItemById(resultItemId)
        needItemInfo['cash'] = needBonus
        needItemInfo['playerCash'] = ownNum
        ownCount = p.inv.countItemInPages(itemId, enableParentCheck=enableParentCheck)
        needItemInfo['hasItem'] = ownCount
        needItemInfo['needItem'] = needItemNum
        needItemInfo['item'] = uiUtils.getGfxItemById(itemId, '')
        needItemInfo['bonusType'] = bonusType
        self.updateEquipSlot(itemInfo, needItemInfo, resultItemInfo)
        gameglobal.rds.ui.inventory.updateSlotState(self.srcPos[0], self.srcPos[1])

    def updateEquipSlot(self, unBindInfo, needItemInfo, resultItemInfo):
        if self.mediator:
            self.mediator.Invoke('updateEquipSlot', (uiUtils.dict2GfxDict(unBindInfo, True), uiUtils.dict2GfxDict(needItemInfo, True), uiUtils.dict2GfxDict(resultItemInfo, True)))

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator:
            if self.notSuitUnBind(item):
                return True
            if item == self.item:
                return True
        return False

    def notSuitUnBind(self, item):
        if item:
            ed = ED.data.get(item.id)
            if ed and ed.get('mixJewelryId'):
                return False
        return True

    def matchCondition(self, item):
        if self.notSuitUnBind(item):
            return False
        return True

    def onGetJewelryItemsInfo(self, *arg):
        ret = []
        return uiUtils.array2GfxAarry(ret, True)

    def onComfirmMix(self, *arg):
        if self.srcPos:
            msg = gameStrings.TEXT_MIXFAMEJEWELRYPROXY_199
            self.messageBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.comfirmMix, self.srcPos), gameStrings.TEXT_MIXFAMEJEWELRYPROXY_200, None, gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def comfirmMix(self, srcPos):
        p = BigWorld.player()
        item = p.inv.getQuickVal(srcPos[0], srcPos[1])
        if not item:
            return
        equipData = ED.data.get(item.id, {})
        mixJewelryId = tuple(equipData.get('mixJewelryId', ()))
        BigWorld.player().cell.mixFameJewelryItem(mixJewelryId, self.srcPos[0], self.srcPos[1])

    def onJewelryResultClick(self, *arg):
        pass

    def mixJewelrySucc(self):
        self.mediator.Invoke('mixJewelrySucc')
        BigWorld.player().showGameMsg(GMDD.data.MIX_FAME_JEWELRY_SUCCESS, ())

    def onShowFit(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        self.uiAdapter.fittingRoom.addItem(Item(itemId))
