#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/equipPrePropTransferProxy.o
import BigWorld
import copy
import gameglobal
import gametypes
import const
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from guis import ui
from guis import events
from cdata import item_synthesize_set_data as ISSD
from data import equip_pre_prop_exchange_data as EPPED
from data import equip_synthesize_category_data as ESCD
from cdata import game_msg_def_data as GMDD
from cdata import pre_prop_transfer_show_data as PPTSD

class EquipPrePropTransferProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipPrePropTransferProxy, self).__init__(uiAdapter)
        self.type = 'EquipPrePropTransfer'
        self.bindType = 'EquipPrePropTransfer'
        self.modelMap = {'initTab': self.initTab,
         'setTabInfo': self.onSetTabInfo,
         'getDetailInfo': self.onGetDetailInfo,
         'removeItem': self.onRemoveItem,
         'confirm': self.onConfirm}
        self.mediator = None
        self.entityId = 0
        self.filterId = 0
        self.selectedEid = 0
        self.category = {}
        self.hasBindMaterial = False
        for key, value in ESCD.data.items():
            self.category[key] = value.get('categoryName', '')

        self.tabInfo = {}
        self.isMaterialEnough = True
        self.posMap = {}
        self.successMap = {}
        self.nowShowList = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_PRE_PROP_TRANSFER, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_PRE_PROP_TRANSFER:
            self.mediator = mediator
            if BigWorld.player():
                BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
                BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)

    @ui.callFilter(1)
    def onConfirm(self, *arg):
        p = BigWorld.player()
        hasNotBindItem = False
        itemPreProps = [None, None]
        for i in xrange(2):
            pos = self.posMap.get(i, (None, None))
            if pos[0] == None:
                return
            item = p.inv.getQuickVal(pos[0], pos[1])
            if not item:
                return
            if hasattr(item, 'preprops'):
                itemPreProps[i] = item.preprops
            if not item.isForeverBind():
                hasNotBindItem = True

        if itemPreProps[0] == itemPreProps[1]:
            BigWorld.player().showGameMsg(GMDD.data.PRE_PROP_IS_SAME, ())
            return
        if hasNotBindItem:
            bindHint = uiUtils.getTextFromGMD(GMDD.data.PRE_PROPS_ITEM_BINDHINT_TEXT)
            if not bindHint:
                bindHint = '\n转移后装备将全部绑定,是否继续'
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(bindHint, self.onTrueCommit)
        else:
            self.onTrueCommit()

    def onTrueCommit(self):
        if self.posMap == self.successMap:
            bindHint = uiUtils.getTextFromGMD(GMDD.data._CHANGE_PRE_PROPS_SECOND_TIME)
            if not bindHint:
                bindHint = '\n你已成功进行前缀置换,是否再次进行置换'
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(bindHint, self.onTrueCommitStep2)
        else:
            self.onTrueCommitStep2()

    def onTrueCommitStep2(self):
        npcEnt = BigWorld.entities.get(self.entityId)
        if not npcEnt:
            return
        pos0 = self.posMap.get(0, (None, None))
        pos1 = self.posMap.get(1, (None, None))
        if pos0[0] == None or pos1[0] == None:
            return
        self.npcCellExchangeEquipPreProp(npcEnt, pos0[0], pos0[1], pos1[0], pos1[1], self.selectedEid)

    @ui.looseGroupTradeConfirm([2,
     3,
     4,
     5], GMDD.data.PRE_PROP_EXCHANGE)
    def npcCellExchangeEquipPreProp(self, npcEnt, srcPage, srcPos, tgtPage, tgtPos, selEid):
        npcEnt.cell.exchangeEquipPreProp(srcPage, srcPos, tgtPage, tgtPos, selEid)

    def reset(self):
        self.mediator = None
        self.hasBindMaterial = False
        self.selectedEid = 0
        self.binding = {}
        self.successMap = {}
        self.isMaterialEnough = True

    def show(self, entId, filterId = 0):
        if not PPTSD.data.get(filterId):
            return
        self.entityId = entId
        self.filterId = filterId
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_PRE_PROP_TRANSFER)

    def clearWidget(self):
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_PRE_PROP_TRANSFER)
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
            self.doSelectedEid(self.selectedEid)

    def initTab(self, *arg):
        if self.mediator:
            nameList = self.getTabName()
            self.mediator.Invoke('setTabList', uiUtils.array2GfxAarry(nameList, True))

    def getTabName(self):
        if not self.tabInfo:
            for item in EPPED.data:
                data = EPPED.data[item]
                schoolShowLimit = data.get('schoolShowLimit')
                category = data.get('category')
                if schoolShowLimit:
                    for school in schoolShowLimit:
                        self.tabInfo.setdefault(school, {})
                        self.tabInfo[school].setdefault(category, [])
                        self.tabInfo[school][category].append(item)

                else:
                    for school in const.DEFAULT_GROUP_SCH_REQ:
                        self.tabInfo.setdefault(school, {})
                        self.tabInfo[school].setdefault(category, [])
                        self.tabInfo[school][category].append(item)

        self.nowShowList = {}
        data = PPTSD.data.get(self.filterId, {}).get('syncthesizeId')
        for value in data:
            itemId = value[0]
            funcId = value[1]
            self.nowShowList.setdefault(itemId, [])
            self.nowShowList[itemId].append(funcId)

        nowShowData = PPTSD.data.get(self.filterId, {}).get('showList')
        cateList = nowShowData.keys()
        cateList.sort()
        cateNameList = []
        for cate in cateList:
            cateNameList.append([cate, self.category[cate]])

        return cateNameList

    def onSetTabInfo(self, *arg):
        cate = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        school = p.school
        itemFuncList = self.tabInfo.get(school, {}).get(cate, [])
        showList = PPTSD.data.get(self.filterId, {}).get('showList').get(cate)
        if not showList:
            return
        ret = []
        for lineList in showList:
            lineArray = []
            for itemId in lineList:
                hasFunc = False
                funcList = []
                for funcId in self.nowShowList[itemId]:
                    if funcId in itemFuncList:
                        hasFunc = True
                        funcList.append(funcId)

                if hasFunc:
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    count = p.inv.countItemInPages(itemId, enableParentCheck=True, includeLatch=True)
                    if count < 1:
                        itemInfo['count'] = "<font color = \'#FB0000\'>×%d</font>" % count
                    else:
                        itemInfo['count'] = '×%d' % count
                    itemInfo['eid'] = funcList[0]
                    lineArray.append(itemInfo)

            if len(lineArray):
                ret.append(lineArray)

        self.mediator.Invoke('setItemList', uiUtils.array2GfxAarry(ret, True))

    def onGetDetailInfo(self, *arg):
        eid = int(arg[3][0].GetNumber())
        self.removeItem(0, False)
        self.doSelectedEid(eid)
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def doSelectedEid(self, eid, refresh = False):
        if self.mediator:
            self.selectedEid = eid
            p = BigWorld.player()
            epped = EPPED.data.get(eid, {})
            info = {}
            cashNeed = epped.get('cashNeed', ())
            if cashNeed and cashNeed > p.cash:
                cashNeed = "<font color = \'#FB0000\'>%s</font>" % format(cashNeed, ',')
            else:
                cashNeed = format(cashNeed, ',')
            info['cashNeed'] = cashNeed
            self.hasBindMaterial = False
            self.isMaterialEnough = True
            itemGroup = epped.get('materialSetNeed', ())
            groupItems = [ [item.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT), item['itemId'], item['numRange'][0]] for item in ISSD.data.get(itemGroup, []) ]
            materialList = []
            for itemSearchType, itemId, needNum in groupItems:
                itemInfo = uiUtils.getGfxItemById(itemId)
                enableParentCheck = True if itemSearchType == gametypes.ITEM_MIX_TYPE_PARENT else False
                ownNum = p.inv.countItemInPages(itemId, enableParentCheck=enableParentCheck)
                if p.inv.countItemInPages(itemId, enableParentCheck=enableParentCheck, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY):
                    self.hasBindMaterial = True
                if ownNum < needNum:
                    self.isMaterialEnough = False
                itemInfo['numStr'] = uiUtils.convertNumStr(ownNum, needNum)
                materialList.append(itemInfo)

            info['materialList'] = materialList
            self.mediator.Invoke('setMaterial', uiUtils.dict2GfxDict(info, True))
            self.refreshItemInfo()

    def refreshItemInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            itemPos0 = self.posMap.get(0, (None, None))
            itemPos1 = self.posMap.get(1, (None, None))
            btnEnabled = self.isMaterialEnough == True
            useHintItem = False
            if itemPos0[0] == None:
                btnEnabled = False
                useHintItem = True
                itemId = EPPED.data.get(self.selectedEid, {}).get('id', 0)
                info['itemInfo0'] = uiUtils.getGfxItemById(itemId, "<font color = \'#FB0000\'>0/1</font>")
                info['showHint0'] = True
                info['content0'] = "<font color = \'#FB0000\'>缺少装备\n无法获取属性</font>"
                info['itemInfo1'] = {}
                info['showHint1'] = False
                info['content1'] = "<font color = \'#FB0000\'>缺少装备\n无法获取属性</font>"
            elif itemPos1[0] == None:
                btnEnabled = False
                item0 = p.inv.getQuickVal(itemPos0[0], itemPos0[1])
                info['itemInfo0'] = uiUtils.getGfxItem(item0, location=const.ITEM_IN_BAG)
                info['showHint0'] = False
                info['content0'] = "<font color= \'#79C725\'>%s</font>" % uiUtils.getItemPreprops(item0, True)
                info['itemInfo1'] = {}
                info['showHint1'] = True
                info['content1'] = "<font color = \'#FB0000\'>缺少装备\n无法获取属性</font>"
            else:
                item0 = p.inv.getQuickVal(itemPos0[0], itemPos0[1])
                info['itemInfo0'] = uiUtils.getGfxItem(item0, location=const.ITEM_IN_BAG)
                info['showHint0'] = False
                info['content0'] = "<font color= \'#79C725\'>%s</font>" % uiUtils.getItemPreprops(item0, True)
                item1 = p.inv.getQuickVal(itemPos1[0], itemPos1[1])
                info['itemInfo1'] = uiUtils.getGfxItem(item1, location=const.ITEM_IN_BAG)
                info['showHint1'] = False
                info['content1'] = "<font color= \'#79C725\'>%s</font>" % uiUtils.getItemPreprops(item1, True)
            cashNeed = EPPED.data.get(self.selectedEid, {}).get('cashNeed', 0)
            if cashNeed and cashNeed > p.cash:
                btnEnabled = False
            info['btnEnabled'] = btnEnabled
            info['useHintItem'] = useHintItem
            self.mediator.Invoke('refreshItemInfo', uiUtils.dict2GfxDict(info, True))

    def onSuccess(self):
        if self.mediator:
            self.doSelectedEid(self.selectedEid)
            self.mediator.Invoke('playEffect', ())
        BigWorld.player().showGameMsg(GMDD.data.PRE_PROP_TRANSFER_SUCCESS, ())
        self.successMap = copy.deepcopy(self.posMap)

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        _, slot = self.getSlotID(key)
        if self.posMap.get(slot, (None, None))[0] == None:
            return
        self.removeItem(slot, True)

    def getSlotID(self, key):
        _, idItem = key.split('.')
        return (0, int(idItem[4:]))

    def _getKey(self, slot):
        return 'EquipPrePropTransfer0.slot%d' % slot

    def setItem(self, srcBar, srcSlot, destSlot):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(srcBar, srcSlot)
        if srcItem.hasLatch():
            p.showGameMsg(GMDD.data.PRE_PROP_ITEM_LATCH, ())
            return
        self.removeItem(destSlot, False)
        key = self._getKey(destSlot)
        if self.binding.has_key(key):
            self.posMap[destSlot] = (srcBar, srcSlot)
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
            self.refreshItemInfo()

    def removeItem(self, slot, needRefresh):
        key = self._getKey(slot)
        if self.binding.has_key(key):
            srcBar, _ = self.posMap.get(slot, (None, None))
            if srcBar != None:
                self.posMap.pop(slot)
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        if slot == 0:
            self.removeItem(1, False)
        if needRefresh:
            self.refreshItemInfo()

    def findEmptyPos(self):
        for i in xrange(2):
            if not self.posMap.has_key(i):
                return i

        return 1

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            itemPos0 = self.posMap.get(0, (None, None))
            if itemPos0[0] == None:
                itemId = EPPED.data.get(self.selectedEid, {}).get('id', 0)
                if item.id == itemId:
                    return (page, pos) in self.posMap.values()
                else:
                    return True
            elif gameglobal.rds.configData.get('enableManualEquip', False):
                targetId = EPPED.data.get(self.selectedEid, {}).get('targetId', ())
                if item.id in targetId:
                    return (page, pos) in self.posMap.values()
                else:
                    return True
            else:
                itemId = EPPED.data.get(self.selectedEid, {}).get('id', 0)
                if item.id == itemId:
                    return (page, pos) in self.posMap.values()
                else:
                    return True
        else:
            return False

    @ui.uiEvent(uiConst.WIDGET_EQUIP_PRE_PROP_TRANSFER, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        if not self.mediator:
            return
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        desPos = self.findEmptyPos()
        self.setInventoryItem(nPage, nItem, desPos)

    def setInventoryItem(self, nPageSrc, nItemSrc, nItemDes):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if srcItem:
            if nItemDes == 0:
                itemId = EPPED.data.get(self.selectedEid, {}).get('id', 0)
                if srcItem.id == itemId:
                    self.setItem(nPageSrc, nItemSrc, nItemDes)
            else:
                itemPos0 = self.posMap.get(0, (None, None))
                if itemPos0[0] == None:
                    return
                if gameglobal.rds.configData.get('enableManualEquip', False):
                    targetId = EPPED.data.get(self.selectedEid, {}).get('targetId', ())
                    if srcItem.id in targetId:
                        self.setItem(nPageSrc, nItemSrc, nItemDes)
                else:
                    itemId = EPPED.data.get(self.selectedEid, {}).get('id', 0)
                    if srcItem.id == itemId:
                        self.setItem(nPageSrc, nItemSrc, nItemDes)
