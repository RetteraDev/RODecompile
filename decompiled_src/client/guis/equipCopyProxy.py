#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipCopyProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
from callbackHelper import Functor
from ui import gbk2unicode
from guis import uiConst
from guis import uiUtils
from guis import events
from guis import ui
from uiProxy import SlotDataProxy
from item import Item
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import equip_data as ED

class EquipCopyProxy(SlotDataProxy):
    EFFECT_TIME = 0.5

    def __init__(self, uiAdapter):
        super(EquipCopyProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.type = 'equipCopy'
        self.bindType = 'equipCopy'
        self.isMaterialEnough = False
        self.nowCallBack = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_COPY, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_COPY:
            self.mediator = mediator
        self.isMaterialEnough = False
        self.mediator.Invoke('setCanConfirm', GfxValue(False))
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)
        BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
        BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)

    def onItemRemove(self, params):
        kind = params[0]
        page = params[1]
        pos = params[2]
        if kind != const.RES_KIND_INV:
            return
        targetKey = self._getKey(0, 1)
        targetItem = self.bindingData.get(targetKey, {}).get('item')
        targetPos = self.bindingData.get(targetKey, {}).get('pos')
        if targetItem:
            if targetPos == [page, pos]:
                self.removeItem(0, 1)

    def onItemChange(self, params):
        kind = params[0]
        page = params[1]
        pos = params[2]
        if kind != const.RES_KIND_INV:
            return
        targetKey = self._getKey(0, 0)
        targetItem = self.bindingData.get(targetKey, {}).get('item')
        targetPos = self.bindingData.get(targetKey, {}).get('pos')
        if targetItem:
            if targetPos == [page, pos]:
                self.setItem(page, pos, 0, 0)
                item = BigWorld.player().inv.getQuickVal(page, pos)
                self.bindingData[targetKey] = {'item': item,
                 'pos': targetPos}
                self.binding[targetKey][0].Invoke('refreshTip')

    def getTargetToolTip(self):
        key = self._getKey(0, 0)
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key]['item'])
        else:
            return GfxValue('')

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key]['item'])
        else:
            return GfxValue('')

    def setItem(self, srcBar, srcSlot, destBar, destSlot, count = ''):
        if not self.mediator:
            return
        p = BigWorld.player()
        it = p.inv.getQuickVal(srcBar, srcSlot)
        targetKey = self._getKey(destBar, destSlot)
        if self.checkItemCanPut(it, destSlot, True):
            self.bindingData[targetKey] = {'item': it,
             'pos': [srcBar, srcSlot]}
            data = uiUtils.getItemData(it.id)
            color = uiUtils.getItemColor(it.id)
            data['color'] = color
            if count:
                data['count'] = count
            if destSlot == 0:
                data['srcType'] = 'equipCopy'
            self.binding[targetKey][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        if destSlot == 0:
            targetKey = self._getKey(0, 1)
            rubbingItem = self.bindingData.get(targetKey, {}).get('item')
            if not self.checkItemCanPut(rubbingItem, 1, False):
                self.removeItem(0, 1)
            self.isMaterialEnough = False
        if destSlot == 0 or destSlot == 1:
            self.refreshSlot2()
        self.refreshHint()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def removeItem(self, bar, slot):
        if not self.mediator:
            return
        key = self._getKey(bar, slot)
        data = GfxValue(0)
        data.SetNull()
        self.binding[key][1].InvokeSelf(data)
        self.bindingData[key] = {}
        if slot == 0:
            self.removeItem(0, 1)
            self.removeItem(0, 2)
        elif slot == 1:
            self.removeItem(0, 2)
        self.refreshHint()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        if slot == 2 and self.mediator:
            self.mediator.Invoke('setMaterailNum', GfxValue(''))

    def checkItemCanPut(self, item, destSlot, needAnnouce = False):
        p = BigWorld.player()
        if not item:
            return False
        if item.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_STORAGE_LOCKED, ())
            return False
        if destSlot == 0:
            if item.isCanRubbing():
                if not item.checkPlayerCondition(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, needLvCheck=False):
                    if needAnnouce == True:
                        BigWorld.player().showGameMsg(GMDD.data.EQUIP_CAN_NOT_RUBBING, ())
                    return False
                return True
            else:
                if needAnnouce == True:
                    BigWorld.player().showGameMsg(GMDD.data.EQUIP_CAN_NOT_RUBBING, ())
                return False
        else:
            if destSlot == 1:
                targetKey = self._getKey(0, 0)
                targetItem = self.bindingData.get(targetKey, {}).get('item')
                if not targetItem:
                    if needAnnouce == True:
                        BigWorld.player().showGameMsg(GMDD.data.PLEAE_INPUT_RUBBING_TARGET, ())
                    return False
                if getattr(item, 'equipType', -1) == Item.EQUIP_BASETYPE_ARMOR_RUBBING and targetItem.equipType == Item.EQUIP_BASETYPE_ARMOR or getattr(item, 'equipType', -1) == Item.EQUIP_BASETYPE_WEAPON_RUBBING and targetItem.equipType == Item.EQUIP_BASETYPE_WEAPON:
                    if targetItem.equipSType != item.equipSType:
                        if needAnnouce == True:
                            BigWorld.player().showGameMsg(GMDD.data.RUBBING_ITEM_CANNOT_USE_IN_TARGET, ())
                        return False
                    if not item.checkPlayerCondition(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, needLvCheck=False):
                        if needAnnouce == True:
                            BigWorld.player().showGameMsg(GMDD.data.EQUIP_CAN_NOT_RUBBING, ())
                        return False
                else:
                    if needAnnouce == True:
                        BigWorld.player().showGameMsg(GMDD.data.ITEM_NOT_RUBBING_ITEM, ())
                        return False
                    return False
                return True
            if destSlot == 2:
                materialIDList = SCD.data.get('rubbingMateials', ())
                if item.getParentId() in materialIDList:
                    return True
                else:
                    if needAnnouce == True:
                        BigWorld.player().showGameMsg(GMDD.data.NOT_RUBBING_MATERIAL, ())
                    return False
        return False

    def clearWidget(self):
        self.mediator = None
        self.isMaterialEnough = False
        self.bindingData = {}
        self.binding = {}
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)
        if self.nowCallBack:
            BigWorld.cancelCallback(self.nowCallBack)
            self.nowCallBack = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_COPY)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def _getKey(self, bar, slot):
        return 'equipCopy%d.slot%d' % (bar, slot)

    def show(self, npcId = 0):
        self.npcId = npcId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_COPY)

    def refreshHint(self):
        equipKey = self._getKey(0, 0)
        equipCopyKey = self._getKey(0, 1)
        equip = self.bindingData.get(equipKey)
        equipCopy = self.bindingData.get(equipCopyKey)
        tips = ''
        if not equip:
            tips = uiUtils.getTextFromGMD(GMDD.data.EQUIP_COPY_HINT_TIPS_1, gameStrings.TEXT_EQUIPCOPYPROXY_239)
        elif not equipCopy:
            tips = uiUtils.getTextFromGMD(GMDD.data.EQUIP_COPY_HINT_TIPS_2, gameStrings.TEXT_EQUIPCOPYPROXY_242)
        elif not self.isMaterialEnough:
            tips = uiUtils.getTextFromGMD(GMDD.data.EQUIP_COPY_HINT_TIPS_3, gameStrings.TEXT_EQUIPCOPYPROXY_245)
        if self.mediator:
            self.mediator.Invoke('setHint', GfxValue(gbk2unicode(tips)))
            if tips:
                self.mediator.Invoke('setCanConfirm', GfxValue(False))
            else:
                self.mediator.Invoke('setCanConfirm', GfxValue(True))
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        self.binding[equipKey][0].Invoke('refreshTip')
        self.binding[equipCopyKey][0].Invoke('refreshTip')

    def isItemDisabled(self, kind, page, pos, nowItem):
        if self.mediator and kind == const.RES_KIND_INV:
            for i in xrange(0, 2):
                targetKey = self._getKey(0, i)
                targetPos = self.bindingData.get(targetKey, {}).get('pos')
                if targetPos == [page, pos]:
                    return True

            if nowItem.isCanRubbing():
                return False
            targetKey = self._getKey(0, 0)
            targetItem = self.bindingData.get(targetKey, {}).get('item')
            if not targetItem:
                return True
            if getattr(nowItem, 'equipType', -1) == Item.EQUIP_BASETYPE_ARMOR_RUBBING and targetItem.equipType == Item.EQUIP_BASETYPE_ARMOR or getattr(nowItem, 'equipType', -1) == Item.EQUIP_BASETYPE_WEAPON_RUBBING and targetItem.equipType == Item.EQUIP_BASETYPE_WEAPON:
                if targetItem.equipSType != nowItem.equipSType:
                    return True
                else:
                    return False
            return True
        else:
            return False

    def refreshSlot2(self):
        if self.mediator:
            targetKey = self._getKey(0, 1)
            targetItem = self.bindingData.get(targetKey, {}).get('item')
            if not targetItem:
                self.removeItem(0, 2)
                return
            ed = ED.data.get(targetItem.id, {})
            consumeItemNum = ed.get('rubbingMaterialNum', 1)
            materialIDList = SCD.data.get('rubbingMateials', ())
            count = 0
            useMaterialID = 0
            for materialID in materialIDList:
                count = count + BigWorld.player().inv.countItemInPages(materialID, enableParentCheck=True)
                if count > 0:
                    useMaterialID = materialID
                    result = BigWorld.player().inv.countItemChild(materialID)
                    if result[0] > 0:
                        useMaterialID = result[1][0]
                    break

            if count == 0:
                useMaterialID = materialIDList[0]
            materialIt = Item(useMaterialID)
            if self.checkItemCanPut(materialIt, 2, False):
                data = uiUtils.getItemData(useMaterialID)
                countStr = '%d/%d' % (count, consumeItemNum)
                if count >= consumeItemNum:
                    countStr = uiUtils.toHtml(countStr, '#FFFFE7')
                else:
                    countStr = uiUtils.toHtml(countStr, '#F43804')
                color = uiUtils.getItemColor(materialIt.id)
                data['color'] = color
                if count >= consumeItemNum:
                    self.isMaterialEnough = True
                if self.mediator:
                    self.mediator.Invoke('setMaterailNum', GfxValue(countStr))
                targetKey = self._getKey(0, 2)
                self.binding[targetKey][1].InvokeSelf(uiUtils.dict2GfxDict(data))
                self.bindingData[targetKey] = {'item': materialIt,
                 'pos': None}

    @ui.uiEvent(uiConst.WIDGET_EQUIP_COPY, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            if i.isCanRubbing():
                self.setItem(nPage, nItem, 0, 0)
            else:
                self.setItem(nPage, nItem, 0, 1)
            return

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[9:]), int(idItem[4:]))

    def onNotifySlotUse(self, *args):
        nPage, nItem = self.getSlotID(args[3][0].GetString())
        if nItem != 2:
            self.removeItem(nPage, nItem)

    @ui.callFilter(1)
    def onConfirm(self, *args):
        if self.isMaterialBind():
            targetKey = self._getKey(0, 0)
            targetItem = self.bindingData.get(targetKey, {}).get('item')
            if targetItem:
                if not targetItem.isForeverBind():
                    txt = uiUtils.getTextFromGMD(GMDD.data.RUBBING_BIND_CONFIRM, gameStrings.TEXT_EQUIPCOPYPROXY_362)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.startConfirm))
                else:
                    self.startConfirm()
        else:
            self.startConfirm()

    def isMaterialBind(self):
        for i in xrange(1, 3):
            targetKey = self._getKey(0, i)
            if self.bindingData[targetKey]:
                item = self.bindingData[targetKey].get('item')
                ret = BigWorld.player().inv.countItemBind(item.getParentId(), enableParentCheck=True)
                if ret:
                    return ret

        return False

    def startConfirm(self):
        if self.mediator:
            self.mediator.Invoke('playEffect', ())
            if self.nowCallBack:
                BigWorld.cancelCallback(self.nowCallBack)
            self.nowCallBack = BigWorld.callback(self.EFFECT_TIME, Functor(self.trueConfirm))

    def trueConfirm(self):
        targetKey = self._getKey(0, 0)
        targetItemPos = self.bindingData.get(targetKey, {}).get('pos')
        targetKey = self._getKey(0, 1)
        rubbingPos = self.bindingData.get(targetKey, {}).get('pos')
        targetKey = self._getKey(0, 2)
        materialItem = self.bindingData.get(targetKey, {}).get('item')
        if targetItemPos and rubbingPos and materialItem:
            self.cellRubbingEquip(targetItemPos[0], targetItemPos[1], const.RES_KIND_INV, rubbingPos[0], rubbingPos[1], materialItem.getParentId())

    @ui.looseGroupTradeConfirm([1, 2], GMDD.data.EQUIP_RUBBING)
    def cellRubbingEquip(self, ePage, ePos, kind, iPage, iPos, mId):
        BigWorld.player().cell.rubbingEquip(ePage, ePos, kind, iPage, iPos, mId)
