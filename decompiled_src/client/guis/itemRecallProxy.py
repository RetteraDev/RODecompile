#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemRecallProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import const
import gametypes
from uiProxy import SlotDataProxy
from guis import ui
from guis import uiConst
from guis import uiUtils
from guis import events
from item import Item
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import item_recall_config_data as IRCD
from cdata import item_recall_npc_data as IRND
from data import fame_data as FD
from data import sys_config_data as SCD

class ItemRecallProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ItemRecallProxy, self).__init__(uiAdapter)
        self.modelMap = {'removeBack': self.onRemoveBack,
         'confirmRecall': self.onConfirmRecall,
         'getDesc': self.onGetDesc}
        self.type = 'itemRecall'
        self.bindType = 'itemRecall'
        self.recallMed = None
        self.recallIds = []
        self.recallObj = {}
        self.recallItem = None
        self.npcId = 0
        self.funcId = 0
        self.srcPos = [None, None]
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_RECALL, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ITEM_RECALL:
            self.recallMed = mediator
            BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def show(self, npcId, funcId):
        if gameglobal.rds.configData.get('enableItemRecall', False):
            self.npcId = npcId
            self.funcId = funcId
            self.updateRecallIds()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ITEM_RECALL)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.resetRecall()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        self.recallMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ITEM_RECALL)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[10:]), int(idItem[4:]))

    def onRemoveBack(self, *arg):
        self.resetRecall()

    def onConfirmRecall(self, *arg):
        if self.recallItem == None:
            BigWorld.player().showGameMsg(GMDD.data.ITEM_RECALL_NONE_ITEM, ())
            return
        elif self.recallItem.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_RECALL_ITEM_HAS_LATCH, ())
            return
        else:
            recallId = self.recallObj.get(self.recallItem.id, 0)
            data = IRCD.data.get(recallId, {})
            recallType = data.get('recallType', 0)
            if recallType == gametypes.RECALL_TYPE_ITEM_DISASS:
                if self.recallItem.type == Item.BASETYPE_EQUIP and getattr(self.recallItem, 'enhLv', 0) > 0:
                    msg = uiUtils.getTextFromGMD(GMDD.data.ITEM_RECALL_FORBIDDEN_WITH_ENHLV, gameStrings.TEXT_ITEMRECALLPROXY_86)
                    gameglobal.rds.ui.messageBox.showMsgBox(msg)
                    return
            if recallType == gametypes.RECALL_TYPE_EQUIP_DISASS:
                if self.recallItem.type == Item.BASETYPE_EQUIP and (getattr(self.recallItem, 'starExp', 0) > 0 or getattr(self.recallItem, 'starLv', 0) > 0):
                    msg = GMD.data.get(GMDD.data.ITEM_RECALL_STAR_TIPS, {}).get('text', gameStrings.TEXT_ITEMRECALLPROXY_92)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.confirmRecallItem))
                    return
            self.confirmRecallItem()
            return

    def confirmRecallItem(self):
        if self.npcId != 0:
            npc = BigWorld.entities.get(self.npcId)
            if npc:
                if self.recallItem != None and self.srcPos[0] != None and self.srcPos[1] != None:
                    npc.cell.recycleItemForCompensation(self.srcPos[0], self.srcPos[1], 1, self.recallObj[self.recallItem.id])

    def resetRecall(self):
        self.recallItem = None
        removePage = self.srcPos[0]
        removePos = self.srcPos[1]
        self.srcPos = [None, None]
        if removePage != None and removePos != None:
            gameglobal.rds.ui.inventory.updateSlotState(removePage, removePos)
        self.resetPanel()

    def resetPanel(self):
        if self.recallMed:
            self.recallMed.Invoke('resetPanel')

    @ui.uiEvent(uiConst.WIDGET_ITEM_RECALL, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onItemRecycleItemClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            if self.checkRecallable(i.id):
                self.setInventoryItem(i, nPage, nItem)
            return

    def setInventoryItem(self, it, page, pos):
        if it.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_RECALL_ITEM_HAS_LATCH, ())
            return
        else:
            oldPage = self.srcPos[0]
            oldPos = self.srcPos[1]
            self.recallItem = it
            self.srcPos[0] = page
            self.srcPos[1] = pos
            if oldPage != None and oldPos != None:
                gameglobal.rds.ui.inventory.updateSlotState(oldPage, oldPos)
            ret = self._getData()
            if self.recallMed:
                self.recallMed.Invoke('setPage', uiUtils.dict2GfxDict(ret, True))
            return

    def checkRecallable(self, itemId):
        return itemId in self.recallIds

    def updateRecallIds(self):
        self.recallIds = []
        self.recallObj = {}
        if self.funcId != 0:
            recallId = IRND.data.get(self.funcId, {}).get('recallId', [])
            for index in recallId:
                itemId = IRCD.data.get(index, {}).get('itemId', 0)
                children = self._getChildId(itemId)
                for childId in children:
                    self.recallIds.append(childId)
                    self.recallObj[childId] = index

                self.recallIds.append(itemId)
                self.recallObj[itemId] = index

    def _getChildId(self, itemId):
        p = BigWorld.player()
        children = p.inv.findAllItemInPages(itemId, enableParentCheck=True)
        childrenIds = []
        for page, pos in children:
            it = p.inv.getQuickVal(page, pos)
            if it:
                childrenIds.append(it.id)

        return childrenIds

    def isItemDisabled(self, kind, page, pos, item):
        if self.recallMed:
            if self.srcPos[0] == page and self.srcPos[1] == pos:
                return True
            if self.checkRecallable(item.id):
                return False
            return True

    def _getData(self):
        ret = {}
        if self.recallItem != None:
            recallId = self.recallObj.get(self.recallItem.id, 0)
            data = IRCD.data.get(recallId, {})
            recallType = data.get('recallType', 0)
            if recallType == gametypes.RECALL_TYPE_EQUIP_SWAP:
                ret = self._getEquipRecallList(recallId)
                ret['type'] = recallType
            elif recallType == gametypes.RECALL_TYPE_ITEM_DISASS:
                ret = self._getItemRecallList(recallId)
                ret['type'] = recallType
            elif recallType == gametypes.RECALL_TYPE_EQUIP_DISASS:
                if self.npcId != 0:
                    npc = BigWorld.entities.get(self.npcId)
                    if npc:
                        if self.recallItem != None and self.srcPos[0] != None and self.srcPos[1] != None:
                            npc.cell.probeRecycleItemForCompensation(self.srcPos[0], self.srcPos[1], 1, self.recallObj[self.recallItem.id])
        return ret

    def _getFameData(self, fames):
        fameObj = {}
        for fame in fames:
            fameObj = {}
            fameObj['itemId'] = 0
            fameObj['type'] = 'fame'
            fameName = FD.data.get(fame[0], {}).get('name', gameStrings.TEXT_CHALLENGEPROXY_199_1)
            fameObj['count'] = '%d' % fame[1]
            fameObj['labelName'] = fameName

        return fameObj

    def _getExpObj(self, exp):
        expObj = {}
        expObj['itemId'] = 0
        expObj['type'] = 'exp'
        expName = SCD.data.get('bonusDict', {}).get('exp', gameStrings.TEXT_GAMETYPES_6408)
        expObj['count'] = '%d' % exp
        expObj['labelName'] = expName
        return expObj

    def _getCashObj(self, cashes):
        ret = []
        cashObj = {}
        if cashes[0] > 0:
            cashObj['itemId'] = 0
            cashObj['type'] = 'cash'
            cashName = SCD.data.get('bonusDict', {}).get('bindCash', gameStrings.TEXT_INVENTORYPROXY_3297)
            cashObj['count'] = '%d' % cashes[0]
            cashObj['labelName'] = cashName
            ret.append(cashObj)
        cashObj = {}
        if cashes[1] > 0:
            cashObj['type'] = 'cash'
            cashObj['itemId'] = 0
            cashName = SCD.data.get('bonusDict', {}).get('cash', gameStrings.TEXT_INVENTORYPROXY_3296)
            cashObj['count'] = '%d' % cashes[1]
            cashObj['labelName'] = cashName
            ret.append(cashObj)
        return ret

    def _getItemRecallList(self, recallId):
        recallId = self.recallObj.get(self.recallItem.id, 0)
        data = IRCD.data.get(recallId, {})
        items = data.get('items', [])
        fames = data.get('fames', [])
        exp = data.get('exp', 0)
        cashes = data.get('cash', [])
        ret = {}
        ret['item'] = []
        ret['recallItem'] = uiUtils.getGfxItem(self.recallItem, appendInfo={'count': 1}, location=const.ITEM_IN_BAG)
        if len(items) > 0:
            for item in items:
                itemObj = {}
                itemObj['itemId'] = item[0]
                itemObj['type'] = 'item'
                itemName = uiUtils.getItemColorName(itemObj['itemId'])
                itemObj['count'] = '%d' % item[1]
                itemObj['labelName'] = itemName
                ret['item'].append(itemObj)

        if len(fames) > 0:
            fame = self._getFameData(fames)
            ret['item'].append(fame)
        if exp > 0:
            expObj = self._getExpObj(exp)
            ret['item'].append(expObj)
        if len(cashes) > 0:
            cashArr = self._getCashObj(cashes)
            for cashObj in cashArr:
                ret['item'].append(cashObj)

        return ret

    def updateEquipDisassData(self, itemList, compExp, compCash, compFames):
        ret = {}
        recallId = self.recallObj.get(self.recallItem.id, 0)
        data = IRCD.data.get(recallId, {})
        recallType = data.get('recallType', 0)
        ret['type'] = recallType
        ret['recallItem'] = uiUtils.getGfxItem(self.recallItem, appendInfo={'count': 1}, location=const.ITEM_IN_BAG)
        ret['item'] = []
        if len(itemList) > 0:
            for item in itemList:
                itemObj = {}
                itemObj['itemId'] = item.id
                itemObj['type'] = 'item'
                itemName = uiUtils.getItemColorName(item.id)
                itemObj['labelName'] = itemName
                itemObj['count'] = item.cwrap
                ret['item'].append(itemObj)

        if len(compFames) > 0:
            fame = self._getFameData(compFames)
            ret['item'].append(fame)
        if compExp > 0:
            expObj = self._getExpObj(compExp)
            ret['item'].append(expObj)
        if len(compCash) > 0:
            cashArr = self._getCashObj(compCash)
            for cashObj in cashArr:
                ret['item'].append(cashObj)

        if self.recallMed:
            self.recallMed.Invoke('setPage', uiUtils.dict2GfxDict(ret, True))

    def _getEquipRecallList(self, recallId):
        ret = {}
        ret['recallItem'] = uiUtils.getGfxItem(self.recallItem, appendInfo={'count': 1}, location=const.ITEM_IN_BAG)
        data = IRCD.data.get(recallId, {})
        newItemId = data.get('newEquipId', 0)
        ret['newItem'] = uiUtils.getGfxItemById(newItemId)
        ret['props'] = []
        if data.get('starExp', 0):
            ret['props'].append(SCD.data.get('equipPropsText', {}).get('starExp', gameStrings.TEXT_ITEMRECALLPROXY_330))
        if data.get('preProp', 0):
            ret['props'].append(SCD.data.get('equipPropsText', {}).get('preProp', gameStrings.TEXT_ITEMRECALLPROXY_332))
        if data.get('randomProp', 0):
            ret['props'].append(SCD.data.get('equipPropsText', {}).get('randomProp', gameStrings.TEXT_EQUIPMIXNEWPROXY_291))
        if data.get('refineLv', 0):
            ret['props'].append(SCD.data.get('equipPropsText', {}).get('refineLv', gameStrings.TEXT_ITEMRECALLPROXY_336))
        if data.get('refineEffects', 0):
            ret['props'].append(SCD.data.get('equipPropsText', {}).get('refineEffects', gameStrings.TEXT_EQUIPMIXNEWPROXY_295))
        if data.get('starLv', 0):
            ret['props'].append(SCD.data.get('equipPropsText', {}).get('starLv', gameStrings.TEXT_ITEMRECALLPROXY_340))
        if data.get('gemNum', 0):
            ret['props'].append(SCD.data.get('equipPropsText', {}).get('gemNum', gameStrings.TEXT_ITEMRECALLPROXY_342))
        return ret

    def onGetDesc(self, *arg):
        ret = {}
        ret['desc'] = IRND.data.get(self.funcId, {}).get('desc', gameStrings.TEXT_ITEMRECALLPROXY_349)
        ret['visible'] = True
        return uiUtils.dict2GfxDict(ret, True)
