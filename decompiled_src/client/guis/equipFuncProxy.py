#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/equipFuncProxy.o
import copy
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import gametypes
import const
import itemToolTipUtils
import utils
from guis import uiConst
from guis import uiUtils
from guis import messageBoxProxy
from uiProxy import SlotDataProxy
from item import Item
from guis import ui
from callbackHelper import Functor
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from cdata import font_config_data as FCD
from data import prop_ref_data as PRD
from cdata import equip_enhance_prop_data as EEPD
from cdata import equip_enhance_probability_data as EEPBD
from cdata import equip_enhancement_transfer_data as EETD
from data import equip_enhance_juexing_data as EEJD
from cdata import equip_order_factor_data as EOFD

class EquipFuncProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipFuncProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'getFuncType': self.onGetFuncType,
         'confirmEnhance': self.onConfirmEnhance,
         'openInventory': self.onOpenInventory,
         'removeItem': self.onRemoveItem,
         'confirmTransfer': self.onConfirmTransfer,
         'selectAllow': self.onSelectAllow}
        self.mediator = None
        self.type = 'equipFunc'
        self.bindType = 'equipFunc'
        self.funcType = uiConst.EQUIP_FUNC_ENHANCE
        self.posMap = {}
        self.npcId = 0
        self.allow = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_FUNC, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_FUNC:
            self.mediator = mediator
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.mediator = None
        self.allow = False
        if self.funcType in (uiConst.EQUIP_FUNC_ENHANCE, uiConst.EQUIP_FUNC_TRANSFER):
            for i in xrange(0, 7):
                self.removeItem(self.funcType, i)

        self.posMap = {}
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_FUNC)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def show(self, npcId, type = uiConst.EQUIP_FUNC_ENHANCE):
        self.npcId = npcId
        self.funcType = type
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_FUNC)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[9:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'equipFunc%d.slot%d' % (bar, slot)

    def setItem(self, srcBar, srcSlot, destBar, destSlot, it, needItem = False, itemNeedNum = 0):
        key = self._getKey(destBar, destSlot)
        if not self.binding.has_key(key):
            return
        if self.funcType == uiConst.EQUIP_FUNC_ENHANCE:
            if destSlot != 0:
                for k, v in self.bindingData.items():
                    if v and v.id == it.id:
                        bar, slot = self.getSlotID(k)
                        self.removeItem(bar, slot)

            self.bindingData[key] = it
            if destSlot == 0:
                gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
            iconPath = uiUtils.getItemIconFile64(it.id)
            if destSlot == 0:
                count = it.cwrap
            else:
                count = BigWorld.player().inv.countItemInPages(it.id)
            data = {'iconPath': iconPath,
             'count': count}
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
            if hasattr(it, 'quality'):
                quality = it.quality
            else:
                quality = ID.data.get(it.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
            if self.posMap.has_key((destBar, destSlot)):
                gameglobal.rds.ui.inventory.updateSlotState(self.posMap[destBar, destSlot][0], self.posMap[destBar, destSlot][1])
            self.posMap[destBar, destSlot] = (srcBar, srcSlot)
            if destSlot == 0:
                previewKey = self._getKey(destBar, destSlot + 1)
                if self.binding.has_key(previewKey):
                    self.binding[previewKey][1].InvokeSelf(uiUtils.dict2GfxDict(data))
                    self.binding[previewKey][0].Invoke('setSlotColor', GfxValue(color))
            self.refreshContent()
        elif self.funcType == uiConst.EQUIP_FUNC_TRANSFER:
            if destSlot >= 2:
                srcKey = self._getKey(uiConst.EQUIP_FUNC_TRANSFER, 0)
                dstKey = self._getKey(uiConst.EQUIP_FUNC_TRANSFER, 1)
                srcIt = self.bindingData.get(srcKey, None)
                dstIt = self.bindingData.get(dstKey, None)
                if not srcIt or not dstIt:
                    return
                enhLv = getattr(srcIt, 'enhLv', 0)
                eData = EETD.data.get((enhLv, dstIt.order), {})
                itemCost = [ itemId for itemId, itemNum in eData.get('baseItemCost', []) ]
                if self.allow == True:
                    keepLvItemCost = [ itemId for itemId, itemNum in self.getKeepLvItemCost(srcIt, dstIt) ]
                    itemCost.extend(keepLvItemCost)
                if it.getParentId() not in itemCost and it.id not in itemCost:
                    return
                for k, v in self.bindingData.items():
                    if v and (v.id == it.id or v.id == it.getParentId() or v.getParentId() == it.id):
                        bar, slot = self.getSlotID(k)
                        self.removeItem(bar, slot)

            self.bindingData[key] = it
            iconPath = uiUtils.getItemIconFile64(it.id)
            if destSlot < 2:
                count = it.cwrap
            else:
                parentId = it.getParentId()
                result = BigWorld.player().inv.countItemChild(parentId)
                if result[0] > 0:
                    it = Item(result[1][0])
                else:
                    it = Item(parentId)
                self.bindingData[key] = it
                count = BigWorld.player().inv.countItemInPages(it.getParentId(), enableParentCheck=True)
            if needItem == True:
                count = uiUtils.convertNumStr(count, itemNeedNum)
            data = {'iconPath': iconPath,
             'count': count}
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
            if hasattr(it, 'quality'):
                quality = it.quality
            else:
                quality = ID.data.get(it.id, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
            self.posMap[destBar, destSlot] = (srcBar, srcSlot)
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
            if destSlot < 2:
                self.refreshContent()

    def removeItem(self, bar, slot):
        key = self._getKey(bar, slot)
        if not self.binding.has_key(key):
            return
        if self.funcType == uiConst.EQUIP_FUNC_ENHANCE:
            self.bindingData[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            if self.posMap.has_key((bar, slot)):
                gameglobal.rds.ui.inventory.updateSlotState(self.posMap[bar, slot][0], self.posMap[bar, slot][1])
            if self.posMap.has_key((bar, slot)):
                self.posMap.pop((bar, slot))
            if slot == 0:
                previewKey = self._getKey(bar, slot + 1)
                if self.binding.has_key(previewKey):
                    self.binding[previewKey][1].InvokeSelf(data)
                    self.binding[previewKey][0].Invoke('setSlotColor', GfxValue('nothing'))
                for i in xrange(2, 7):
                    self.removeItem(uiConst.EQUIP_FUNC_ENHANCE, i)

            self.refreshContent()
        elif self.funcType == uiConst.EQUIP_FUNC_TRANSFER:
            self.bindingData[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            if self.posMap.has_key((bar, slot)):
                gameglobal.rds.ui.inventory.updateSlotState(self.posMap[bar, slot][0], self.posMap[bar, slot][1])
            if self.posMap.has_key((bar, slot)):
                self.posMap.pop((bar, slot))
            if slot < 2:
                self.refreshContent()

    def moveItem(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        srcPage, srcPos = self.posMap.get((nPageSrc, nItemSrc), [-1, -1])
        dstPage, dstPos = self.posMap.get((nPageDes, nItemDes), [-1, -1])
        srcIt = p.inv.getQuickVal(srcPage, srcPos)
        dstIt = p.inv.getQuickVal(dstPage, dstPos)
        self.setItem(srcPage, srcPos, nPageDes, nItemDes, srcIt)
        if dstIt:
            self.setItem(dstPage, dstPos, nPageSrc, nItemSrc, dstIt)
        else:
            self.removeItem(nPageSrc, nItemSrc)
        gameglobal.rds.ui.inventory.updateSlotState(srcPage, srcPos)
        gameglobal.rds.ui.inventory.updateSlotState(dstPage, dstPos)
        self.posMap[nPageSrc, nItemSrc] = [dstPage, dstPos]
        self.posMap[nPageDes, nItemDes] = [srcPage, srcPos]

    def refreshContent(self, succ = False):
        if self.funcType == uiConst.EQUIP_FUNC_ENHANCE:
            self.refreshEnhanceContent(succ)
        elif self.funcType == uiConst.EQUIP_FUNC_TRANSFER:
            self.refreshTransferContent(succ)

    def refreshEnhanceContent(self, succ):
        p = BigWorld.player()
        srcKey = self._getKey(0, 0)
        if succ:
            srcIt = None
            if self.posMap.has_key((0, 0)):
                srcIt = p.inv.getQuickVal(*self.posMap[0, 0])
                self.bindingData[srcKey] = srcIt
                self.setItem(self.posMap[0, 0][0], self.posMap[0, 0][1], 0, 0, srcIt)
            if self.posMap.has_key((0, 0)):
                gameglobal.rds.ui.inventory.updateSlotState(self.posMap[0, 0][0], self.posMap[0, 0][1])
            for i in xrange(2, 7):
                key = self._getKey(uiConst.EQUIP_FUNC_ENHANCE, i)
                if not self.posMap.has_key((uiConst.EQUIP_FUNC_ENHANCE, i)):
                    self.removeItem(uiConst.EQUIP_FUNC_ENHANCE, i)
                    continue
                page, pos = self.posMap[uiConst.EQUIP_FUNC_ENHANCE, i]
                it = self.bindingData.get(key, None)
                count = p.inv.countItemInPages(it.id) if it else 0
                if count:
                    self.setItem(page, pos, uiConst.EQUIP_FUNC_ENHANCE, i, it)
                else:
                    self.removeItem(uiConst.EQUIP_FUNC_ENHANCE, i)

        else:
            srcIt = self.bindingData.get(srcKey, None)
        srcProps = []
        srcRet = []
        dstProps = []
        dstRet = []
        enhanceRandProps = {}
        enhanceProps = {}
        btnEnabled = False
        prob = ''
        enhLv = maxEnhLv = 0
        consumeItemIds = []
        isItemEnough = True
        for i in xrange(2, 7):
            key = self._getKey(uiConst.EQUIP_FUNC_ENHANCE, i)
            it = self.bindingData.get(key, None)
            if it and it.id not in consumeItemIds:
                consumeItemIds.append(it.id)

        consumeItemIds.sort()
        consumeItemIds = tuple(consumeItemIds)
        if srcIt:
            order = srcIt.order
            orderFactor = EOFD.data.get(order, {}).get('factor', 1.0)
            if hasattr(srcIt, 'enhanceProps'):
                for lv in xrange(1, srcIt.enhLv + 1):
                    for pid, pType, pVal in srcIt.enhanceProps.get(lv, []):
                        if pType == gametypes.DATA_TYPE_NUM and srcIt._isIntPropRef(pid):
                            srcProps.append((pid, pType, pVal * orderFactor))
                        else:
                            srcProps.append((pid, pType, pVal * orderFactor))

            if hasattr(srcIt, 'enhanceRandProps'):
                for lv in xrange(1, srcIt.enhLv + 1):
                    for pid, pType, pVal in srcIt.enhanceRandProps.get(lv, []):
                        if pType == gametypes.DATA_TYPE_NUM and srcIt._isIntPropRef(pid):
                            srcProps.append((pid, pType, pVal * orderFactor))
                        else:
                            srcProps.append((pid, pType, pVal * orderFactor))

            srcProps = itemToolTipUtils._mergeProps(srcProps)
            for prop in srcProps:
                info = PRD.data[prop[0]]
                propName = info.get('name', '')
                if info['type'] == 2:
                    propVal = '+'
                elif info['type'] == 1:
                    propVal = '-'
                if info['showType'] == 0:
                    propVal += str(int(prop[2]))
                elif info['showType'] == 2:
                    propVal += str(round(prop[2], 1))
                else:
                    propVal += str(round(prop[2] * 100, 1)) + '%'
                srcRet.append([propName, propVal])

            srcRet += self._getJueXingInfo(srcIt)
            enhLv = getattr(srcIt, 'enhLv', 0)
            for elv in xrange(0, enhLv + 2):
                enhPropData = EEPD.data.get((elv,
                 srcIt.equipType,
                 srcIt.equipSType,
                 srcIt.enhanceType))
                if not enhPropData:
                    continue
                if enhPropData.get('randPropId'):
                    result, _ = srcIt._getRandPropsByIdAndQuality(enhPropData['randPropId'], enhPropData.get('quality', 0))
                    randProps = []
                    for res in result:
                        randProps.append(res)

                    enhanceRandProps[elv] = randProps
                enhanceProps[elv] = list(enhPropData.get('enhProps', ()))

            for lv in xrange(0, enhLv + 2):
                for pid, pType, pVal in enhanceProps.get(lv, []):
                    if pType == gametypes.DATA_TYPE_NUM and srcIt._isIntPropRef(pid):
                        dstProps.append((pid, pType, pVal * orderFactor))
                    else:
                        dstProps.append((pid, pType, pVal * orderFactor))

                for pid, pType, pVal in enhanceRandProps.get(lv, []):
                    if pType == gametypes.DATA_TYPE_NUM and srcIt._isIntPropRef(pid):
                        dstProps.append((pid, pType, pVal * orderFactor))
                    else:
                        dstProps.append((pid, pType, pVal * orderFactor))

            dstProps = itemToolTipUtils._mergeProps(dstProps)
            for prop in dstProps:
                info = PRD.data[prop[0]]
                propName = info.get('name', '')
                if info['type'] == 2:
                    propVal = '+'
                elif info['type'] == 1:
                    propVal = '-'
                if info['showType'] == 0:
                    propVal += str(int(prop[2]))
                elif info['showType'] == 2:
                    propVal += str(round(prop[2], 1))
                else:
                    propVal += str(round(prop[2] * 100, 1)) + '%'
                dstRet.append([propName, propVal])

            dstRet += self._getJueXingInfo(srcIt)
            equipType = getattr(srcIt, 'equipType', 0)
            equipSType = getattr(srcIt, 'equipSType', 0)
            if utils.getEquipEnhJuexingPyData().has_key((equipType,
             equipSType,
             enhLv + 1,
             srcIt.enhanceType)):
                dstRet.append(['精炼觉醒', ''])
                dstRet.append(['会出现随机属性', ''])
            maxEnhLv = getattr(srcIt, 'maxEnhlv', enhLv)
            if enhLv < maxEnhLv:
                pass
            else:
                prob = '当前装备精炼等级已达上限'
                btnEnabled = False
                dstRet = []
        if prob == '' or not isItemEnough:
            prob = self.checkRule(srcIt, None, consumeItemIds, isItemEnough)
        ret = [srcRet,
         dstRet,
         srcIt != None,
         btnEnabled,
         prob,
         enhLv,
         min(maxEnhLv, enhLv + 1)]
        if self.mediator != None:
            self.mediator.Invoke('refreshContent', uiUtils.array2GfxAarry(ret, True))

    def refreshTransferContent(self, succ):
        if not self.mediator:
            return
        p = BigWorld.player()
        srcKey = self._getKey(1, 0)
        dstKey = self._getKey(1, 1)
        if succ:
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        srcIt = self.bindingData.get(srcKey, None)
        dstIt = self.bindingData.get(dstKey, None)
        cost = ''
        itemCostStr = ''
        moneyEnough = False
        consumeItemEnough = True
        for slot in xrange(2, 7):
            self.removeItem(uiConst.EQUIP_FUNC_TRANSFER, slot)

        needShowSlot = False
        if srcIt and dstIt:
            enhLv = getattr(srcIt, 'enhLv', 0)
            eData = EETD.data.get((enhLv, dstIt.order), {})
            cost = eData.get('mCost', '')
            if cost != '':
                moneyEnough = p.cash >= cost
                cost = '消耗%s: %s' % (const.CASH_DESC, str(cost))
            itemCost = eData.get('baseItemCost', [])
            keepLvItemCost = self.getKeepLvItemCost(srcIt, dstIt)
            if keepLvItemCost:
                self.mediator.Invoke('setCheckBox', GfxValue(True))
            else:
                self.mediator.Invoke('setCheckBox', GfxValue(False))
            needShowSlot = False
            if self.allow == True:
                itemCost.extend(keepLvItemCost)
            elif len(keepLvItemCost):
                needShowSlot = True
            if len(itemCost):
                needShowSlot = True
            itemCostStr = '消耗物品: ' if itemCost else ''
            for itemId, itemNum in itemCost:
                srcBar, srcSlot = p.inv.findItemInPages(itemId, enableParentCheck=True)
                if srcSlot != const.CONT_NO_POS:
                    it = p.inv.getQuickVal(srcBar, srcSlot)
                    consumeItemEnough = p.inv.countItemInPages(itemId, enableParentCheck=True) >= itemNum
                else:
                    consumeItemEnough = False
                    it = Item(itemId, 0)
                destSlot = self.findEmptyPos()
                self.setItem(srcBar, srcSlot, uiConst.EQUIP_FUNC_TRANSFER, destSlot, it, True, itemNum)
                itemCostStr += '%d个%s ' % (itemNum, ID.data.get(itemId, {}).get('name', ''))

        else:
            self.mediator.Invoke('setCheckBox', GfxValue(False))
        canTransfer = getattr(srcIt, 'enhLv', 0) > getattr(dstIt, 'enhLv', 0)
        if not canTransfer:
            costStr = self.checkRule(srcIt, dstIt, [])
        else:
            costStr = cost + '\n' + itemCostStr
        contentList = None
        if srcIt and dstIt:
            if hasattr(srcIt, 'enhJuexingData'):
                testIt = copy.deepcopy(dstIt)
                testIt.enhJuexingData = srcIt.enhJuexingData
                testIt.enhLv = getattr(srcIt, 'enhLv', 1)
                contentList = uiUtils.buildJuexingContentList(testIt)
        ret = [srcIt != None and dstIt != None and consumeItemEnough and canTransfer,
         moneyEnough and canTransfer,
         costStr,
         needShowSlot,
         contentList]
        self.mediator.Invoke('refreshContent', uiUtils.array2GfxAarry(ret, True))

    def findEmptyPos(self):
        pos = 2
        for i in xrange(2, 7):
            key = (self.funcType, i)
            if not self.posMap.has_key(key):
                return i

        return pos

    def findTransferItemPos(self):
        pos = 0
        key = (self.funcType, 0)
        pos = 1 if self.posMap.has_key(key) else 0
        return pos

    def getKeepLvItemCost(self, srcItem, tgtItem):
        eetd = EETD.data.get((getattr(srcItem, 'enhLv', 0), tgtItem.order), {})
        if not eetd:
            return []
        if tgtItem.order <= srcItem.order:
            return eetd.get('keepLvItemCostLow', [])
        return eetd.get('keepLvItemCost', [])

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return GfxValue('')

    def onClosePanel(self, *arg):
        self.hide()

    def onGetFuncType(self, *arg):
        return GfxValue(self.funcType)

    def onConfirmEnhance(self, *arg):
        p = BigWorld.player()
        if self.funcType == uiConst.EQUIP_FUNC_ENHANCE:
            page, pos = self.posMap.get((0, 0), [0, 0])
            consumeItems = ((0, 2),
             (0, 3),
             (0, 4),
             (0, 5),
             (0, 6))
            consumeItemPage = [ (self.posMap[it][0] if self.posMap.has_key(it) else -1) for it in consumeItems ]
            consumeItemPos = [ (self.posMap[it][1] if self.posMap.has_key(it) else -1) for it in consumeItems ]
            enhanceDstItem = p.inv.getQuickVal(page, pos)
            npcEnt = BigWorld.entities.get(self.npcId)
            if not npcEnt:
                return
            for i, (pg, ps) in enumerate(zip(consumeItemPage, consumeItemPos)):
                it = p.inv.getQuickVal(pg, ps)
                key = self._getKey(consumeItems[i][0], consumeItems[i][1])
                item = self.bindingData.get(key, None)
                if not item:
                    continue
                if not it or it.id != item.id:
                    itemPg, itemPs = p.inv.findItemInPages(item.id, includeExpired=True, includeLatch=True, includeShihun=True)
                    if itemPg == const.CONT_NO_PAGE:
                        p.showGameMsg(GMDD.data.EQUIP_ENHANCE_FAIL_ITEM_LESS, ())
                        return
                    self.posMap[consumeItems[i]] = (itemPg, itemPs)
                    self.onConfirmEnhance(arg)
                    return
                if it.isForeverBind() and not enhanceDstItem.isForeverBind():
                    itData = ID.data.get(it.id, {})
                    MBButton = messageBoxProxy.MBButton
                    text = GMD.data.get(GMDD.data.EQUIP_ENHANCE_BIND, {}).get('text', '使用%s精炼会导致装备绑定，点确认之后，继续精炼')
                    consumeItemPage = filter(lambda c: c != -1, consumeItemPage)
                    consumeItemPos = filter(lambda c: c != -1, consumeItemPos)
                    buttons = [MBButton('确认', Functor(self.doEnhanceItem, page, pos, consumeItemPage, consumeItemPos), True, True), MBButton('取消')]
                    self.msgBoxId = gameglobal.rds.ui.messageBox.show(True, '', text % itData.get('name'), buttons)
                    return

            consumeItemPage = filter(lambda c: c != -1, consumeItemPage)
            consumeItemPos = filter(lambda c: c != -1, consumeItemPos)
            self.doEnhanceItem(page, pos, consumeItemPage, consumeItemPos)

    def doEnhanceItem(self, page, pos, itemIds, itemNums):
        npcEnt = BigWorld.entities.get(self.npcId)
        npcEnt and npcEnt.cell.enhanceItemInv(page, pos, itemIds, itemNums)

    def zeroTransConfirm(self):
        p = BigWorld.player()
        if self.funcType == uiConst.EQUIP_FUNC_TRANSFER:
            srcPage, srcPos = self.posMap.get((1, 0), [0, 0])
            dstPage, dstPos = self.posMap.get((1, 1), [0, 0])
            srcIt = p.inv.getQuickVal(srcPage, srcPos)
            itData = ID.data.get(srcIt.id, {})
            dstIt = p.inv.getQuickVal(dstPage, dstPos)
            srcMaxEnhLv = getattr(srcIt, 'enhLv', 0)
            dstMaxEnhLv = getattr(dstIt, 'maxEnhlv', 0)
            dstEnhLv = getattr(dstIt, 'enhLv', 0)
            if srcIt.isForeverBind() and not dstIt.isForeverBind():
                MBButton = messageBoxProxy.MBButton
                buttons = [MBButton('确定', Functor(self.firstTransferConfirm, srcPage, srcPos, dstPage, dstPos, dstMaxEnhLv < srcMaxEnhLv, dstEnhLv != 0), True, True), MBButton('取消')]
                text = GMD.data.get(GMDD.data.EQUIP_ENHANCE_TRANSFER_BIND, {}).get('text', '使用%s精炼转移会导致装备绑定，点确认之后，继续精炼转移')
                self.msgBoxId = gameglobal.rds.ui.messageBox.show(True, '', text % itData.get('name'), buttons)
            elif dstMaxEnhLv < srcMaxEnhLv:
                self.secondTransferConfirm(srcPage, srcPos, dstPage, dstPos, dstEnhLv != 0)
            elif dstEnhLv != 0:
                self.thirdTransferConfirm(srcPage, srcPos, dstPage, dstPos)
            else:
                self.doEnhanceTransfer(srcPage, srcPos, dstPage, dstPos)

    def onConfirmTransfer(self, *arg):
        p = BigWorld.player()
        if self.funcType == uiConst.EQUIP_FUNC_TRANSFER:
            srcPage, srcPos = self.posMap.get((1, 0), [0, 0])
            dstPage, dstPos = self.posMap.get((1, 1), [0, 0])
            srcIt = p.inv.getQuickVal(srcPage, srcPos)
            dstIt = p.inv.getQuickVal(dstPage, dstPos)
            self.onConfirmTransferNext(srcIt, dstIt)

    @ui.checkEquipCanReturn(2, GMDD.data.RETURN_BACK_ENHANCE_TRANS)
    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.RETURN_BACK_ENHANCE_TRANS)
    def onConfirmTransferNext(self, srcIt, dstIt):
        contentList = uiUtils.buildJuexingContentList(srcIt)
        if not hasattr(srcIt, 'equipType') or not hasattr(dstIt, 'equipType') or not hasattr(srcIt, 'equipSType') or not hasattr(dstIt, 'equipSType'):
            return
        if (srcIt.equipType != dstIt.equipType or srcIt.equipSType != dstIt.equipSType) and len(contentList):
            txt = uiUtils.getTextFromGMD(GMDD.data.NOT_SAME_TYPE_TRANSFER)
            if not txt:
                txt = '不同类型的装备进行精炼转移可能会导致部分精炼觉醒效果暂时失效，确认转移吗？'
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.beforeZeroConfirm))
        else:
            self.beforeZeroConfirm()

    def beforeZeroConfirm(self):
        p = BigWorld.player()
        srcPage, srcPos = self.posMap.get((1, 0), [0, 0])
        dstPage, dstPos = self.posMap.get((1, 1), [0, 0])
        srcIt = p.inv.getQuickVal(srcPage, srcPos)
        dstIt = p.inv.getQuickVal(dstPage, dstPos)
        enhLv = getattr(srcIt, 'enhLv', 0)
        data = EETD.data.get((enhLv, dstIt.order), {})
        if not data:
            gameglobal.rds.ui.messageBox.showMsgBox('当前状态不能转移')
        elif self.allow == False and self.getKeepLvItemCost(srcIt, dstIt):
            txt = uiUtils.getTextFromGMD(GMDD.data.USE_KEEP_LV_ITEM)
            if not txt:
                txt = '如不使用防降级道具,该次转移精炼等级将有可能下降'
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(txt, Functor(self.zeroTransConfirm))
        else:
            self.zeroTransConfirm()

    def doEnhanceTransfer(self, srcPage, srcPos, dstPage, dstPos):
        p = BigWorld.player()
        srcIt = p.inv.getQuickVal(srcPage, srcPos)
        dstIt = p.inv.getQuickVal(dstPage, dstPos)
        keepLvItemCost = self.getKeepLvItemCost(srcIt, dstIt)
        keepLv = self.allow if keepLvItemCost != [] else True
        npcEnt = BigWorld.entities.get(self.npcId)
        npcEnt and npcEnt.cell.itemEnhancementTransfer(srcPage, srcPos, dstPage, dstPos, keepLv)

    def firstTransferConfirm(self, srcPage, srcPos, dstPage, dstPos, needSecondConfirm = False, needThirdConfirm = False):
        if needSecondConfirm:
            self.secondTransferConfirm(srcPage, srcPos, dstPage, dstPos, needThirdConfirm)
        elif needThirdConfirm:
            self.thirdTransferConfirm(srcPage, srcPos, dstPage, dstPos)
        else:
            self.doEnhanceTransfer(srcPage, srcPos, dstPage, dstPos)

    def secondTransferConfirm(self, srcPage, srcPos, dstPage, dstPos, needThirdConfirm = False):
        msg = '源装备的精炼等级大于目标装备的精炼等级上限，超出的精炼等级将暂时失效，是否要继续精炼转移？'
        if needThirdConfirm:
            self.msgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.thirdTransferConfirm, srcPage, srcPos, dstPage, dstPos))
        else:
            self.msgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doEnhanceTransfer, srcPage, srcPos, dstPage, dstPos))

    def thirdTransferConfirm(self, srcPage, srcPos, dstPage, dstPos):
        msg = '被转移装备的精炼等级将被覆盖，确定转移吗？'
        self.msgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doEnhanceTransfer, srcPage, srcPos, dstPage, dstPos))

    def onOpenInventory(self, *arg):
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if bar == uiConst.EQUIP_FUNC_ENHANCE or slot in (0, 1):
            self.removeItem(bar, slot)

    def _getJueXingInfo(self, it):
        ret = []
        return ret

    def onSelectAllow(self, *args):
        self.allow = args[3][0].GetBool()
        self.refreshTransferContent(True)

    def checkRule(self, srcIt, dstIt = None, consumeItemIds = [], isItemEnough = True):
        desc = '请放入待精炼装备和精炼材料' if self.funcType == uiConst.EQUIP_FUNC_ENHANCE else '请放入需要转移和被转移的装备'
        if not srcIt and not dstIt and not consumeItemIds:
            return desc
        if self.funcType == uiConst.EQUIP_FUNC_ENHANCE:
            if consumeItemIds and not srcIt:
                desc = '请放入待精炼装备'
            elif srcIt and not consumeItemIds:
                desc = '请放入精炼材料'
            elif not isItemEnough:
                desc = '放入的精炼材料数量不足'
            else:
                for cId in consumeItemIds:
                    if cId not in EEPBD.data.keys():
                        desc = '放入的精炼材料类型不符'
                        break

        elif self.funcType == uiConst.EQUIP_FUNC_TRANSFER:
            if srcIt and not dstIt:
                desc = '请放入需要转移的装备'
            elif dstIt and not srcIt:
                desc = '请放入需要被转移的装备'
            elif getattr(srcIt, 'enhLv', 0) <= getattr(dstIt, 'enhLv', 0):
                desc = '被转移装备的精炼等级大于或等于转移装备的精炼等级，无法转移'
            enhLv = getattr(srcIt, 'enhLv', 0)
            if enhLv != 0:
                if dstIt:
                    if not EETD.data.get((enhLv, dstIt.order), {}):
                        desc = '当前装备精炼转移非法'
        return desc

    def onSuccessForTransfer(self):
        if self.mediator:
            srcKey = self._getKey(1, 0)
            dstKey = self._getKey(1, 1)
            p = BigWorld.player()
            srcPage, srcPos = self.posMap.get((1, 0), [0, 0])
            dstPage, dstPos = self.posMap.get((1, 1), [0, 0])
            srcIt = p.inv.getQuickVal(srcPage, srcPos)
            dstIt = p.inv.getQuickVal(dstPage, dstPos)
            self.bindingData[srcKey] = srcIt
            self.bindingData[dstKey] = dstIt
            self.binding[srcKey][0].Invoke('refreshTip')
            self.binding[dstKey][0].Invoke('refreshTip')
            self.refreshContent(True)

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if item and item.isYaoPei():
                return True
            if self.funcType == uiConst.EQUIP_FUNC_TRANSFER:
                for i in xrange(0, 7):
                    nowPage, nowPos = gameglobal.rds.ui.equipFunc.posMap.get((self.funcType, i), (-1, -1))
                    if nowPage != -1 or nowPos != -1:
                        if i > 1:
                            p = BigWorld.player()
                            it = p.inv.getQuickVal(nowPage, nowPos)
                            if it:
                                if it.getParentId() == item.getParentId():
                                    return True
                        elif page == nowPage and pos == nowPos:
                            return True

        return False
