#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/equipPropTransferProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import const
import math
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from guis import ui
from ui import gbk2unicode
from guis import tipUtils
from guis import events
from cdata import game_msg_def_data as GMDD
from cdata import equip_props_transfer_data as EPTD
from cdata import item_synthesize_set_data as ISSD

class EquipPropTransferProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipPropTransferProxy, self).__init__(uiAdapter)
        self.modelMap = {'selectedEID': self.onSelectedEid,
         'notifySlotUse': self.onNotifySlotUse,
         'confirm': self.onConfirm,
         'selectedTransPart': self.selectedTransPart,
         'checkIsCanCheck': self.onCheckIsCanCheck}
        self.reset()
        self.hasBindMaterial = False
        self.isMaterialEnough = False
        self.type = 'EquipPropTransfer'
        self.bindType = 'EquipPropTransfer'
        self.posMap = {}
        self.itemMap = {}
        self.targetPos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
        self.sourcePos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
        self.selectedEid = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_PROP_TRANSFER, self.clearWidget)

    def onNotifySlotUse(self, *args):
        binding = args[3][0].GetString()
        bar, slot = self.getSlotID(binding)
        self.removeItem(bar, slot)

    def selectedTransPart(self, *args):
        self.doSelectedEid(self.selectedEid)

    def onCheckIsCanCheck(self, *args):
        checkPos = int(args[3][0].GetNumber())
        useCashList = EPTD.data.get(self.selectedEid, {}).get('cashNeed', ())
        if len(useCashList) > checkPos:
            cashNeed = useCashList[checkPos]
        else:
            cashNeed = 0
        materialSetNeedList = EPTD.data.get(self.selectedEid, {}).get('materialSetNeed', ())
        if len(materialSetNeedList) > checkPos:
            materialNeed = materialSetNeedList[checkPos]
        else:
            materialNeed = 0
        if materialNeed == 0 and cashNeed == 0:
            BigWorld.player().showGameMsg(GMDD.data.ITEM_PROP_TRANSFER_CANNOT_SELECTED, ())
            return GfxValue(False)
        else:
            return GfxValue(True)

    @ui.callFilter(1)
    def onConfirm(self, *args):
        p = BigWorld.player()
        hasNotBindItem = False
        posMap = {}
        posMap[0] = self.targetPos
        posMap[1] = self.sourcePos
        for i in xrange(2):
            pos = posMap.get(i)
            if not pos:
                return
            item = p.inv.getQuickVal(pos[0], pos[1])
            if not item:
                return
            if not item.isForeverBind():
                hasNotBindItem = True

        if hasNotBindItem:
            bindHint = uiUtils.getTextFromGMD(GMDD.data.PROPS_ITEM_BINDHINT_TEXT)
            if not bindHint:
                bindHint = '\n转移后装备将全部绑定,是否继续'
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(bindHint, self.onTrueCommit)
        else:
            self.onTrueCommit()

    def onTrueCommit(self):
        npcEnt = BigWorld.entities.get(self.entityId)
        if not npcEnt:
            return
        if self.targetPos[0] == const.CONT_NO_PAGE or self.sourcePos[0] == const.CONT_NO_PAGE:
            return
        p = BigWorld.player()
        targetItem = p.inv.getQuickVal(self.targetPos[0], self.targetPos[1])
        sourceItem = p.inv.getQuickVal(self.sourcePos[0], self.sourcePos[1])
        if targetItem.hasGem() or sourceItem.hasGem():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_PROP_TRANSFER_HAS_GEM, ())
            return
        checkList = self.getCheckList()
        if checkList[0] and targetItem._getEquipStarExpCeil() < sourceItem.calcTotalStarExp():
            gameglobal.rds.ui.messageBox.showYesNoMsgBox('超出的融合度会消失，确认转移吗？', self.trueCommitStep2)
        else:
            self.trueCommitStep2()

    def trueCommitStep2(self):
        npcEnt = BigWorld.entities.get(self.entityId)
        if not npcEnt:
            return
        if self.targetPos[0] == const.CONT_NO_PAGE or self.sourcePos[0] == const.CONT_NO_PAGE:
            return
        checkList = self.getCheckList()
        self.npcCellTransferEquipProps(npcEnt, self.sourcePos[0], self.sourcePos[1], self.targetPos[0], self.targetPos[1], self.selectedEid, checkList)

    @ui.looseGroupTradeConfirm([4, 5], GMDD.data.EQUIP_PROPS_TRANSFER)
    def npcCellTransferEquipProps(self, npcEnt, srcPage, srcPos, tgtPage, tgtPos, selEId, checkList):
        npcEnt.cell.transferEquipProps(srcPage, srcPos, tgtPage, tgtPos, selEId, checkList)

    def countItemSlots(self, it):
        num = 0
        for itemSlot in it.yangSlots:
            if itemSlot.isLocked() == False:
                num = num + 1

        for itemSlot in it.yinSlots:
            if itemSlot.isLocked() == False:
                num = num + 1

        return num

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_PROP_TRANSFER:
            self.mediator = mediator
            self.buildMap()
            self.refreshContent()
            if BigWorld.player():
                BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
                BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def buildMap(self):
        if not self.itemMap:
            for key in EPTD.data:
                itemId = EPTD.data[key].get('targetId')
                self.itemMap.setdefault(itemId, [])
                self.itemMap[itemId].append(key)

    def reset(self):
        self.selectedEid = -1
        self.mediator = None
        self.targetPos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
        self.sourcePos = [const.CONT_NO_PAGE, const.CONT_NO_POS]

    def show(self, entId, filterId = 0):
        self.entityId = entId
        self.filterId = filterId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_PROP_TRANSFER)

    def clearWidget(self):
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_PROP_TRANSFER)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def onItemRemove(self, params):
        self.refreshAll(params)

    def onItemChange(self, params):
        self.refreshAll(params)

    def refreshAll(self, params):
        if self.mediator:
            if params[0] != const.RES_KIND_INV:
                return
            if self.selectedEid != -1:
                self.doSelectedEid(self.selectedEid)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[17:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'EquipPropTransfer%d.slot%d' % (bar, slot)

    @ui.uiEvent(uiConst.WIDGET_EQUIP_PROP_TRANSFER, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        if not self.mediator:
            return
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        if self.targetPos[0] == const.CONT_NO_PAGE:
            self.setItem(nPage, nItem, 0, 0)
        elif self.selectedEid:
            sourceId = EPTD.data[self.selectedEid].get('sourceId')
            if sourceId == i.id:
                self.setItem(nPage, nItem, 0, 1)
            else:
                self.setItem(nPage, nItem, 0, 0)

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if self.itemMap.get(item.id):
                if page == self.targetPos[0] and pos == self.targetPos[1]:
                    return True
                if page == self.sourcePos[0] and pos == self.sourcePos[1]:
                    return True
                return False
            if self.targetPos[0] != const.CONT_NO_PAGE:
                targetItem = BigWorld.player().inv.getQuickVal(self.targetPos[0], self.targetPos[1])
                if not targetItem:
                    return True
                funcList = self.itemMap.get(targetItem.id)
                findUse = False
                for funcId in funcList:
                    itemId = EPTD.data[funcId].get('sourceId')
                    if itemId == item.id:
                        findUse = True

                if findUse == False:
                    return True
                elif page == self.sourcePos[0] and pos == self.sourcePos[1]:
                    return True
                else:
                    return False
            else:
                return True
            return True
        else:
            return False

    def getCheckList(self):
        checkList = [0, 0, 0]
        if self.mediator:
            num = int(self.mediator.Invoke('getCheckList', ()).GetNumber())
            for i in [2, 1, 0]:
                checkList[i] = num >> i
                num = int(num % math.pow(2, i))

        return checkList

    def setItem(self, srcBar, srcSlot, destBar, destSlot):
        if not self.mediator:
            return
        p = BigWorld.player()
        key = self._getKey(destBar, destSlot)
        it = p.inv.getQuickVal(srcBar, srcSlot)
        if it.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_STORAGE_LOCKED, ())
            return
        if destSlot == 0:
            funcList = self.itemMap.get(it.id)
            if self.mediator:
                self.mediator.Invoke('resetCheckBox', GfxValue(True))
            if funcList:
                itemData = uiUtils.getItemData(it.id)
                itemData['srcType'] = 'EquipPropTransfer%d' % destSlot
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(itemData))
                self.binding[key][0].Invoke('setSlotColor', GfxValue(itemData['quality']))
                self.bindingData[key] = it
                self.targetPos = [srcBar, srcSlot]
                self.setFuncList(funcList)
                name = uiUtils.getItemColorName(it.id)
                if self.mediator:
                    self.mediator.Invoke('setTargetName', GfxValue(gbk2unicode(name)))
            else:
                return
        elif destSlot == 1:
            if self.selectedEid != -1:
                sourceId = EPTD.data.get(self.selectedEid, {}).get('sourceId')
                if sourceId:
                    if sourceId == it.id:
                        self.sourcePos = [srcBar, srcSlot]
                        key = self._getKey(0, 1)
                        targetItemData = uiUtils.getItemData(sourceId)
                        targetItemData['count'] = '1/1'
                        targetItemData['srcType'] = 'EquipPropTransfer1'
                        self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(targetItemData))
                        self.binding[key][0].Invoke('setSlotColor', GfxValue(targetItemData['quality']))
                        self.bindingData[key] = it
                        self.mediator.Invoke('setHint', GfxValue(False))
                    else:
                        BigWorld.player().showGameMsg(GMDD.data.EQUIP_PROP_TRANS_PUT_RIGHT_ITEM, ())
            else:
                BigWorld.player().showGameMsg(GMDD.data.EQUIP_PROP_TRANS_PUT_TARGET_ITEM_FIRST, ())
        self.refreshContent()

    def refreshIips(self):
        for i in xrange(2):
            key = self._getKey(0, i)
            p = BigWorld.player()
            if i == 0:
                if self.targetPos[0] != const.CONT_NO_PAGE:
                    self.bindingData[key] = p.inv.getQuickVal(self.targetPos[0], self.targetPos[1])
            elif self.sourcePos[0] != const.CONT_NO_PAGE:
                self.bindingData[key] = p.inv.getQuickVal(self.sourcePos[0], self.sourcePos[1])
            self.binding[key][0].Invoke('refreshTip')

    def setFuncList(self, funcList):
        if not self.mediator:
            return
        funcInfoList = []
        for funcId in funcList:
            funcData = self.getFuncItemList(funcId, False)
            oneList = []
            oneList.append(funcData['targetItem'])
            oneList.extend(funcData['material'])
            funcInfoList.append({'material': oneList,
             'funcId': funcId,
             'funcName': funcData['funcName']})

        self.mediator.Invoke('setSynFuncList', uiUtils.array2GfxAarry(funcInfoList, True))
        if self.selectedEid == -1:
            if len(funcList):
                self.selectedEid = funcList[0]
            else:
                self.selectedEid = -1
        elif len(funcList):
            if self.selectedEid in funcList:
                pass
            else:
                self.selectedEid = funcList[0]
        else:
            self.selectedEid = -1
        self.mediator.Invoke('selectedEid', GfxValue(self.selectedEid))

    def onSelectedEid(self, *args):
        funcId = int(args[3][0].GetNumber())
        self.mediator.Invoke('resetCheckBox', GfxValue(True))
        self.doSelectedEid(funcId)

    def doSelectedEid(self, funcId):
        if not self.mediator:
            return
        self.selectedEid = funcId
        self.hasBindMaterial = False
        self.isMaterialEnough = False
        funcData = self.getFuncItemList(funcId, True)
        p = BigWorld.player()
        material = funcData['material']
        self.mediator.Invoke('setMaterial', uiUtils.array2GfxAarry(material, True))
        key = self._getKey(0, 1)
        souceIt = funcData['targetItem']
        souceIt['srcType'] = 'EquipPropTransfer1'
        self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(souceIt))
        self.binding[key][0].Invoke('setSlotColor', GfxValue(souceIt['quality']))
        if not self.sourcePos:
            souceItem = p.inv.getQuickVal(self.sourcePos[0], self.sourcePos[1])
            self.bindingData[key] = souceItem
        else:
            self.bindingData[key] = None
        self.hasBindMaterial = funcData['hasBindMaterial']
        self.isMaterialEnough = funcData['isMaterialEnough']
        useCash = self.getCashNeed(self.selectedEid)
        if useCash == 0:
            cash = ''
        else:
            cash = useCash
        if useCash and not useCash <= p.cash:
            cash = "<font color = \'#FB0000\' >%d</font>" % useCash
        self.mediator.Invoke('setUseCash', GfxValue(cash))
        self.refreshContent()

    def onGetToolTip(self, srcType, itemId):
        pos = int(srcType[17:])
        key = self._getKey(0, pos)
        it = self.bindingData.get(key)
        if it:
            return gameglobal.rds.ui.inventory.GfxToolTip(it)
        else:
            return tipUtils.getItemTipById(itemId)

    def getFuncItemList(self, funcId, forMain = True):
        data = EPTD.data[funcId]
        ret = {}
        p = BigWorld.player()
        ret['funcName'] = data.get('funcName', '')
        sourceId = data.get('sourceId')
        itemGroup = data.get('materialSetNeed')
        targetOwnNum = p.inv.countItemInPages(sourceId, True)
        targetItemData = uiUtils.getItemData(sourceId)
        needHint = False
        if forMain:
            if self.sourcePos[0] == const.CONT_NO_PAGE:
                if targetOwnNum != 1:
                    targetItemData['count'] = "<font color = \'#FB0000\' >0/1</font>"
                    self.sourcePos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
                    needHint = True
                else:
                    targetItemData['count'] = '1/1'
                    itemPosList = p.inv.findAllItemInPages(sourceId, gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, True)
                    self.sourcePos = [itemPosList[0][0], itemPosList[0][1]]
            else:
                souceItem = p.inv.getQuickVal(self.sourcePos[0], self.sourcePos[1])
                if souceItem and souceItem.id == sourceId:
                    targetItemData['count'] = '1/1'
                elif targetOwnNum != 1:
                    targetItemData['count'] = "<font color = \'#FB0000\' >0/1</font>"
                    self.sourcePos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
                    needHint = True
                else:
                    targetItemData['count'] = '1/1'
                    itemPosList = p.inv.findAllItemInPages(sourceId, gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, True)
                    self.sourcePos = [itemPosList[0][0], itemPosList[0][1]]
        elif targetOwnNum < 1:
            targetItemData['count'] = "<font color = \'#FB0000\' >0/1</font>"
        else:
            targetItemData['count'] = '%d/1' % targetOwnNum
        ret['targetItem'] = targetItemData
        ret['cashNeed'] = data.get('cashNeed')
        checkList = self.getCheckList()
        groupItems = []
        if type(itemGroup) != int:
            for i in xrange(3):
                if checkList[i]:
                    itemDataList = [ [item.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT), item['itemId'], item['numRange'][0]] for item in ISSD.data.get(itemGroup[i], []) ]
                    for itemSearchType, itemIdM, itemNum in itemDataList:
                        finedPos = -1
                        for j in xrange(len(groupItems)):
                            if groupItems[j][1] == itemIdM:
                                finedPos = j
                                break

                        if finedPos != -1:
                            groupItems[j][2] = groupItems[j][2] + itemNum
                        else:
                            groupItems.append([itemSearchType, itemIdM, itemNum])

        else:
            groupItems = [ [item.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT), item['itemId'], item['numRange'][0]] for item in ISSD.data.get(itemGroup, []) ]
        hasBindMaterial = False
        isMaterialEnough = True
        material = []
        for itemSearchType, itemIdM, itemNum in groupItems:
            itemData = uiUtils.getItemData(itemIdM)
            enableParentCheck = True if itemSearchType == gametypes.ITEM_MIX_TYPE_PARENT else False
            maxNum = p.inv.countItemInPages(itemIdM, enableParentCheck=enableParentCheck)
            if p.inv.countItemInPages(itemIdM, enableParentCheck=enableParentCheck, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY):
                hasBindMaterial = True
            itemData['maxNum'] = maxNum
            itemData['needNum'] = itemNum
            if maxNum < itemNum:
                isMaterialEnough = False
            numStr = uiUtils.convertNumStr(itemData['maxNum'], itemData['needNum'])
            itemData['count'] = numStr
            material.append(itemData)

        ret['material'] = material
        ret['needHint'] = needHint
        ret['isMaterialEnough'] = isMaterialEnough
        ret['hasBindMaterial'] = hasBindMaterial
        return ret

    def removeItem(self, bar, slot):
        if not self.mediator:
            return
        key = self._getKey(bar, slot)
        if not self.binding.has_key(key):
            return
        if slot == 0:
            self.mediator.Invoke('clearAll', ())
            self.bindingData[key] = None
            for i in xrange(2):
                key2 = self._getKey(0, i)
                data = GfxValue(0)
                data.SetNull()
                self.binding[key2][1].InvokeSelf(data)
                self.binding[key2][0].Invoke('setSlotColor', GfxValue('nothing'))

            self.targetPos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
            self.sourcePos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
            self.selectedEid = -1
            self.mediator.Invoke('resetCheckBox', GfxValue(False))
        elif slot == 1:
            if self.selectedEid != -1:
                self.refreshContent()
                itemId = EPTD.data.get(self.selectedEid, {}).get('sourceId', ())
                itemData = uiUtils.getItemData(itemId)
                itemData['count'] = "<font color = \'#FB0000\' >0/1</font>"
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(itemData))
                self.binding[key][0].Invoke('setSlotColor', GfxValue(itemData['quality']))
                self.bindingData[key] = None
                self.sourcePos = [const.CONT_NO_PAGE, const.CONT_NO_POS]
            else:
                return
        self.refreshContent()

    def getCashNeed(self, eid):
        useCashList = EPTD.data.get(eid, {}).get('cashNeed', ())
        if type(useCashList) != int:
            useCash = 0
            checkList = self.getCheckList()
            for i in xrange(len(checkList)):
                if checkList[i]:
                    useCash = useCash + useCashList[i]

        else:
            useCash = useCashList
        return useCash

    def refreshContent(self):
        if self.mediator:
            canConfirm = False
            useCash = self.getCashNeed(self.selectedEid)
            p = BigWorld.player()
            if self.isMaterialEnough and self.targetPos[0] != const.CONT_NO_PAGE and self.sourcePos[0] != const.CONT_NO_PAGE and not useCash > p.cash:
                checkList = self.getCheckList()
                find = False
                for item in checkList:
                    if item == 1:
                        find = True
                        break

                canConfirm = find
            self.mediator.Invoke('setConfirmBtn', GfxValue(canConfirm))
            self.refreshIips()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
            if self.targetPos[0] != const.CONT_NO_PAGE and self.sourcePos[0] == const.CONT_NO_PAGE:
                self.mediator.Invoke('setHint', GfxValue(True))
            else:
                self.mediator.Invoke('setHint', GfxValue(False))

    def onSuccess(self):
        if self.mediator:
            self.doSelectedEid(self.selectedEid)
            self.mediator.Invoke('playEffect', ())
        self.refreshIips()
        BigWorld.player().showGameMsg(GMDD.data.PROP_TRANSFER_SUCCESS, ())
