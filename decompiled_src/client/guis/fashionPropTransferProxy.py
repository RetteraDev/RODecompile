#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fashionPropTransferProxy.o
from gamestrings import gameStrings
import BigWorld
import time
from Scaleform import GfxValue
import gameglobal
import const
import utils
from ui import gbk2unicode
from guis import uiConst
from guis import uiUtils
from guis import tipUtils
from guis import events
from guis import ui
from uiProxy import SlotDataProxy
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import equip_data as ED

class FashionPropTransferProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(FashionPropTransferProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'getHintText': self.onGetHintText,
         'notifySlotUse': self.onNotifySlotUse,
         'getItemType': self.onGetItemType,
         'onSelected': self.onSelected}
        self.mediator = None
        self.type = 'FashionPropTransfer'
        self.bindType = 'FashionPropTransfer'
        self.nowStage = 0
        self.posMap = {}
        self.nowOption = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FASHION_PROP_TRANSFER, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FASHION_PROP_TRANSFER:
            self.mediator = mediator
            self.nowStage = 0
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FASHION_PROP_TRANSFER)

    def clearWidget(self):
        self.nowOption = 0
        self.nowStage = 0
        if self.mediator:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FASHION_PROP_TRANSFER)
            self.mediator = None
            self.posMap = {}
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def setNowStage(self, stage = 0):
        if self.mediator:
            self.mediator.Invoke('setNowStep', GfxValue(stage))
            self.nowStage = stage

    def onTransSuccess(self):
        self.setNowStage(3)
        if self.mediator:
            self.mediator.Invoke('playerDoneEffect')

    def setConfirmEnabled(self, ret = False):
        if self.mediator:
            self.mediator.Invoke('setConfirmEnable', GfxValue(ret))

    @ui.callFilter(3)
    def onConfirm(self, *args):
        if self.nowStage == 3:
            self.removeItem(1, 0)
        else:
            sourcePage, sourcePos = self.posMap.get(0, (-1, -1))
            targetPage, targetPos = self.posMap.get(1, (-1, -1))
            if sourcePage != -1 and sourcePos != -1 and targetPage != -1 and targetPos != -1:
                BigWorld.player().cell.fashionPropTransfer(sourcePage, sourcePos, targetPage, targetPos, self.nowOption)
            return

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if self.nowStage == 0:
                if self.isItemCanTransfer(item):
                    return False
                else:
                    return True
            elif (self.isItemCanTransfer(item) or self.isItemCanBeTransfer(item)) and self.itemNotIn(page, pos):
                return False
            else:
                return True

        return False

    def isItemCanTransfer(self, item):
        if not item.isFashionEquip():
            return False
        if item.suitId == 0 and item.props == []:
            return False
        sed = ED.data.get(item.id)
        if not sed.get('fashionPropOut', 0):
            return False
        return True

    def itemNotIn(self, page, pos):
        sourcePage, sourcePos = self.posMap.get(0, (-1, -1))
        targetPage, targetPos = self.posMap.get(1, (-1, -1))
        if sourcePage == page and sourcePos == pos:
            return False
        if targetPage == page and targetPos == pos:
            return False
        return True

    def isItemCanBeTransfer(self, item):
        if not item.isFashionEquip():
            return False
        sed = ED.data.get(item.id)
        if not sed:
            return False
        sourceKey = self._getKey(1, 0)
        sourceIt = self.bindingData.get(sourceKey)
        if not sourceIt:
            return False
        if sourceIt == item:
            return False
        if sed.get('fashionPropIn', 0):
            if item.isFashionEquip():
                if item.equipSType == sourceIt.equipSType:
                    return True
        return False

    def onGetHintText(self, *args):
        txt = uiUtils.getTextFromGMD(GMDD.data.GET_FASHION_PROP_TRANSFER_HINT_TXT, gameStrings.TEXT_FASHIONPROPTRANSFERPROXY_144)
        txt = txt % self.getNowSetedItemType()
        return GfxValue(gbk2unicode(txt))

    def onGetItemType(self, *args):
        txt = self.getNowSetedItemType()
        return GfxValue(gbk2unicode(txt))

    def onNotifySlotUse(self, *args):
        binding = args[3][0].GetString()
        bar, slot = self.getSlotID(binding)
        if slot < 2:
            self.removeItem(bar, slot)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[19:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'FashionPropTransfer%d.slot%d' % (bar, slot)

    def setItem(self, srcBar, srcSlot, destBar, destSlot):
        if not self.mediator:
            return
        key = self._getKey(destBar, destSlot)
        if not self.binding.has_key(key):
            return
        p = BigWorld.player()
        it = p.inv.getQuickVal(srcBar, srcSlot)
        if it.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.FASHION_PROP_TRANS_ITEM_LATCH, ())
            return
        if destSlot == 0:
            if self.isItemCanTransfer(it):
                key = self._getKey(1, destSlot)
                self.bindingData[key] = it
                self.posMap[destSlot] = [srcBar, srcSlot]
                itemData = uiUtils.getItemData(it.id)
                itemData['srcType'] = 'FashionPropTransfer%d' % destSlot
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(itemData))
                self.binding[key][0].Invoke('setSlotColor', GfxValue(itemData['quality']))
                self.removeItem(1, 1)
                self.setNowStage(1)
            else:
                BigWorld.player().showGameMsg(GMDD.data.FASHION_ITEM_CANNOT_TRANSFER, ())
        elif destSlot == 1:
            if self.isItemCanBeTransfer(it):
                self.bindingData[key] = it
                self.posMap[destSlot] = [srcBar, srcSlot]
                itemData = uiUtils.getItemData(it.id)
                itemData['srcType'] = 'FashionPropTransfer%d' % destSlot
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(itemData))
                self.binding[key][0].Invoke('setSlotColor', GfxValue(itemData['quality']))
                self.setNowStage(2)
                self.resetTimeSelectedList(it)
                self.setSelectedOption(0)
            else:
                BigWorld.player().showGameMsg(GMDD.data.FASHION_ITEM_CANNOT_BE_TRANSFER, ())
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def onSelected(self, *args):
        option = int(args[3][0].GetNumber())
        self.setSelectedOption(option)

    def resetTimeSelectedList(self, item):
        ted = ED.data.get(item.id)
        validTimes = ted.get('fashionPropTransValidTime', [])
        consumes = ted.get('fashionPropTransConsume', [])
        if len(validTimes) != len(consumes):
            return
        if len(validTimes) == 0:
            return
        timeArray = []
        for validTime in validTimes:
            if validTime == 0:
                arrStr = gameStrings.TEXT_SELFADAPTIONSHOPPROXY_38
                timeArray.append(arrStr)
            else:
                arrStr = gameStrings.TEXT_FASHIONPROPTRANSFERPROXY_229 % validTime
                timeArray.append(arrStr)

        if self.mediator:
            self.mediator.Invoke('setOptionContent', uiUtils.array2GfxAarry(timeArray, True))

    def setSelectedOption(self, option):
        self.nowOption = option
        key = self._getKey(1, 1)
        it = self.bindingData.get(key)
        if not it:
            return
        ted = ED.data.get(it.id)
        validTimes = ted.get('fashionPropTransValidTime', [])
        consumes = ted.get('fashionPropTransConsume', [])
        if len(validTimes) != len(consumes):
            return
        nums = consumes[option]
        cItemId = SCD.data.get('fashionPropTransConsumeItemId', 999)
        count = BigWorld.player().inv.countItemInPages(cItemId, enableParentCheck=True)
        itemData = uiUtils.getItemData(cItemId)
        key2 = self._getKey(1, 2)
        itemData['srcType'] = 'FashionPropTransfer2'
        if count >= nums:
            descStr = '%d/%d' % (count, nums)
            self.setConfirmEnabled(True)
        else:
            descStr = "<font color = \'#FB0000\'>%d</font>/%d" % (count, nums)
            self.setConfirmEnabled(False)
        itemData['count'] = descStr
        self.binding[key2][1].InvokeSelf(uiUtils.dict2GfxDict(itemData))
        self.binding[key2][0].Invoke('setSlotColor', GfxValue(itemData['quality']))
        validTime = validTimes[option]
        if validTime == 0:
            arrStr = gameStrings.TEXT_SELFADAPTIONSHOPPROXY_38
        else:
            arrStr = time.strftime('%Y.%m.%d  %H:%M', time.localtime(utils.getNow() + validTimes[option] * 3600 * 24))
        timeStr = gameStrings.TEXT_FASHIONPROPTRANSFERPROXY_268 + arrStr
        if self.mediator:
            self.mediator.Invoke('setHintTimeContent', GfxValue(gbk2unicode(timeStr)))
            self.mediator.Invoke('setSelectOption', GfxValue(option))

    def getNowSetedItemType(self):
        key = self._getKey(1, 0)
        it = self.bindingData.get(key)
        if it:
            return SCD.data.get('fashionTypeMap', {}).get(it.equipSType, gameStrings.TEXT_GM_COMMAND_ITEM_1707)

    def removeItem(self, bar, slot):
        key = self._getKey(bar, slot)
        if not self.binding.has_key(key):
            return
        else:
            self.bindingData[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            if self.posMap.has_key(slot):
                self.posMap.pop(slot)
            if slot == 0:
                self.removeItem(1, 1)
            elif slot == 1:
                self.removeItem(1, 2)
            if self.posMap.has_key(0) and self.posMap.has_key(1):
                self.setNowStage(2)
            elif self.posMap.has_key(0):
                self.setNowStage(1)
            else:
                self.setNowStage(0)
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
            return

    @ui.uiEvent(uiConst.WIDGET_FASHION_PROP_TRANSFER, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        if not self.mediator:
            return
        else:
            event.stop()
            i = event.data['item']
            nPage = event.data['page']
            nItem = event.data['pos']
            if i == None:
                return
            if self.nowStage == 0:
                self.setItem(nPage, nItem, 0, 0)
            elif self.nowStage == 1 or self.nowStage == 2:
                if self.isItemCanBeTransfer(i):
                    self.setItem(nPage, nItem, 1, 1)
                elif self.isItemCanTransfer(i):
                    self.setItem(nPage, nItem, 0, 0)
            return

    def onGetToolTip(self, *arg):
        itemPos = arg[0][19:]
        key = self._getKey(1, int(itemPos))
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        else:
            return tipUtils.getItemTipById(arg[1])
