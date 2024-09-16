#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/meterialBagProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gametypes
import ui
import utils
from uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from helpers import cellCmd
from cdata import game_msg_def_data as GMDD

class MeterialBagProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(MeterialBagProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'meterial'
        self.type = 'meterial'
        self.page = uiConst.METERIAL_PAGE_LOW
        self.modelMap = {'initMeterialBag': self.onInitMeterialBag,
         'setPage': self.onSetPage,
         'allInv2MaterialBag': self.onAllInv2MaterialBag,
         'arrangeMeterialBag': self.onArrangeMeterialBag,
         'clickExpandSlot': self.onClickExpandSlot,
         'enlargeSlot': self.onEnlargeSlot,
         'activeMaterialBag': self.onActiveMaterialBag,
         'isActived': self.onIsActived,
         'isDragging': self.onIsInDragCommonItem,
         'useItem': self.onUseItem}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_METERIAL_BAG, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_METERIAL_BAG:
            self.mediator = mediator
            return self._initData()

    def show(self):
        if gameglobal.rds.configData.get('enableNewMaterialBag', False):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_METERIAL_BAG)

    def clearWidget(self):
        self.mediator = None
        self.page = uiConst.METERIAL_PAGE_LOW
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_METERIAL_BAG)
        gameglobal.rds.ui.funcNpc.close()
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.mediator.Invoke('resetTempBagFlag')

    def _getKey(self, page, pos):
        return 'meterial%d.slot%d' % (page, pos)

    def getSlotID(self, key):
        idPage, idPos = key.split('.')
        pos = int(idPos[4:])
        page = int(idPage[8:])
        if page == 1:
            return (const.METERIAL_BAG_PAGE_BAG, pos)
        return (self.page, pos)

    def _initData(self, *arg):
        ret = {}
        p = BigWorld.player()
        ret['isActived'] = BigWorld.player().materialBagEnabled
        ret['items'] = self._getItems()
        ret['pages'] = len(p.materialBag.posCountDict.keys()) if hasattr(p.materialBag, 'posCountDict') else 1
        ret['enabledPackSlotCnt'] = getattr(p.materialBag, 'enabledPackSlotCnt', 0)
        ret['barItems'] = self._getBarItems()
        return uiUtils.dict2GfxDict(ret, True)

    def _getItems(self):
        items = []
        p = BigWorld.player()
        pageCnt = getattr(p.materialBag, 'posCountDict', {}).get(self.page, 0)
        for ps in xrange(pageCnt):
            it = p.materialBag.getQuickVal(self.page, ps)
            if it == const.CONT_EMPTY_VAL:
                items.append(None)
            else:
                state = uiConst.ITEM_NORMAL
                if hasattr(it, 'latchOfTime'):
                    state = uiConst.ITEM_LATCH_TIME
                elif hasattr(it, 'latchOfCipher'):
                    state = uiConst.ITEM_LATCH_CIPHER
                items.append(uiUtils.getGfxItem(it, appendInfo={'state': state}, location=const.ITEM_IN_METERIAL_BAG))

        return items

    def _getBarItems(self):
        items = []
        p = BigWorld.player()
        for ps in xrange(const.MATERIAL_BAG_BAR_HEIGHT):
            it = p.materialBagBar.getQuickVal(0, ps)
            if it == const.CONT_EMPTY_VAL:
                items.append(None)
            else:
                items.append(uiUtils.getGfxItem(it))

        return items

    def onInitMeterialBag(self, *arg):
        pass

    def onSetPage(self, *arg):
        page = int(arg[3][0].GetNumber())
        self.page = page
        self.updateSlots()

    def updateSlots(self):
        items = self._getItems()
        if self.mediator:
            self.mediator.Invoke('updateSlots', uiUtils.array2GfxAarry(items, True))

    @ui.checkEquipChangeOpen()
    @ui.callInCD(1)
    def onAllInv2MaterialBag(self, *arg):
        BigWorld.player().base.allInv2MaterialBag()

    def onArrangeMeterialBag(self, *arg):
        BigWorld.player().base.sortMaterialBag()

    def onActiveMaterialBag(self, *arg):
        gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_MATERIAL_BAG_ACTIVE, 0)

    def enablePackSlot(self, pos):
        if self.mediator:
            self.mediator.Invoke('enablePackSlot', GfxValue(pos))

    def onClickExpandSlot(self, *arg):
        pass

    def onEnlargeSlot(self, *arg):
        p = BigWorld.player()
        if not p.materialBagEnabled:
            p.showGameMsg(GMDD.data.FORBIDDEN_ENLARGE_BEFORE_ACTIVE, ())
            return
        elif not p.getAbilityData(utils.getAbilityKey(gametypes.ABILITY_MATERIAL_BAG_ENLARGE, None)):
            p.showGameMsg(GMDD.data.ITEM_MATERIAL_INV_NEED_ABILITY, ())
            return
        else:
            gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_MATERIAL_BAG_EXPAND, arg[3][0].GetNumber())
            return

    def removeItem(self, page, pos):
        if self.page != page:
            return
        else:
            key = self._getKey(0, pos)
            if self.binding.get(key, None):
                data = GfxValue(1)
                data.SetNull()
                self.binding[key][1].InvokeSelf(data)
            return

    def addItem(self, item, page, pos):
        if self.page != page:
            return
        else:
            if item:
                key = self._getKey(0, pos)
                if self.binding.get(key, None):
                    state = uiConst.ITEM_NORMAL
                    if hasattr(item, 'latchOfTime'):
                        state = uiConst.ITEM_LATCH_TIME
                    elif hasattr(item, 'latchOfCipher'):
                        state = uiConst.ITEM_LATCH_CIPHER
                    data = uiUtils.getGfxItem(item, appendInfo={'state': state}, location=const.ITEM_IN_METERIAL_BAG)
                    self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data, True))
            return

    def addBarItem(self, item, pos):
        if item is not None:
            key = self._getKey(1, pos)
            if self.binding.get(key, None):
                data = uiUtils.getGfxItem(item)
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data, True))

    def removeBarItem(self, pos):
        key = self._getKey(1, pos)
        if self.binding.get(key, None):
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
            self.binding[key][1].InvokeSelf(data)

    def onGetToolTip(self, *arg):
        p = BigWorld.player()
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if page == const.METERIAL_BAG_PAGE_BAG:
            it = p.materialBagBar.getQuickVal(0, pos)
            if it:
                return gameglobal.rds.ui.inventory.GfxToolTip(it)
        if page == 0:
            i = p.materialBag.getQuickVal(page, pos)
            if i == const.CONT_EMPTY_VAL:
                return gameglobal.rds.ui.inventory.GfxToolTip(i)

    def refreshAll(self):
        if self.mediator:
            self.mediator.Invoke('refreshAll', self._initData())

    def onIsActived(self, *arg):
        return GfxValue(BigWorld.player().materialBagEnabled)

    def refreshActive(self):
        if self.mediator:
            self.mediator.Invoke('refreshActive', GfxValue(BigWorld.player().materialBagEnabled))

    def onIsInDragCommonItem(self, *arg):
        return GfxValue(gameglobal.rds.ui.inDragStorageItem or gameglobal.rds.ui.inDragCommonItem or gameglobal.rds.ui.inDragFashionBagItem or gameglobal.rds.ui.inDragMaterialBagItem)

    def onUseItem(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        materialBagItemSrc = p.materialBag.getQuickVal(page, pos)
        if materialBagItemSrc:
            dstPg, dstPos = p.inv.searchBestInPages(materialBagItemSrc.id, materialBagItemSrc.cwrap, materialBagItemSrc)
            if dstPg != const.CONT_NO_POS and dstPos != const.CONT_NO_POS:
                cellCmd.materialBag2inv(page, pos, materialBagItemSrc.cwrap, dstPg, dstPos)
            else:
                p.showGameMsg(GMDD.data.BAG_FULL, ())
