#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipMixProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
import gametypes
import const
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from guis import ui
from callbackHelper import Functor
from item import Item
from data import equip_synthesize_category_data as ESCD
from data import equip_synthesize_data as ESD
from data import item_data as ID
from cdata import font_config_data as FCD
from cdata import item_synthesize_set_data as ISSD
from cdata import equip_synthesize_npc_function_data as ESNFD
from cdata import game_msg_def_data as GMDD

class EquipMixProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipMixProxy, self).__init__(uiAdapter)
        self.modelMap = {'getItemList': self.onGetItemList,
         'getItemFormula': self.onGetItemFormula,
         'getOtherInfo': self.onGetOtherInfo,
         'confirm': self.onConfirm,
         'close': self.onClose}
        self.reset()
        self.category = [ value.get('categoryName', '') for key, value in ESCD.data.items() ]
        self.hasBindMaterial = False

    def _registerMediator(self, widgetId, mediator):
        pass

    def reset(self):
        self.mediator = None
        self.entityId = None
        self.itemId = None
        self.idx = None
        self.filterId = None
        self.hasBindMaterial = False

    def show(self, entId, filterId = 0):
        self.entityId = entId
        self.filterId = filterId

    def clearWidget(self):
        self.reset()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def _createItemList(self):
        p = BigWorld.player()
        ret = []
        idd = ID.data
        for cateId, title in enumerate(self.category):
            content = []
            synDatas = ESNFD.data.get(self.filterId, {}).get('syncthesizeId', ())
            funcType = ESNFD.data.get(self.filterId, {}).get('funcType', 0)
            gamelog.debug('@zqc synDatas', synDatas)
            for itemId, synMethod in synDatas:
                gamelog.debug('jinjj-----synMethod----', itemId, synMethod)
                idx, value = synMethod, ESD.data.get((itemId, synMethod))
                if value:
                    schoolLimit = value.get('schoolShowLimit', [])
                    if funcType == uiConst.FORMULA_TYPE_MIX and value.get('type', 0) == uiConst.FORMULA_TYPE_MIX and (not schoolLimit or p.realSchool in schoolLimit) and value.get('category', 0) == cateId + 1:
                        iData = idd.get(itemId, {})
                        iconPath = uiUtils.getItemIconFile64(itemId)
                        name = iData.get('name', '')
                        triggerIdx = synDatas.index((itemId, synMethod), 0)
                        content.append({'iconPath': iconPath,
                         'name': name,
                         'itemId': itemId,
                         'idx': idx,
                         'triggerIdx': triggerIdx})
                    content.sort(key=lambda k: k['triggerIdx'])

            if len(content):
                ret.append({'title': title,
                 'content': content,
                 'cateId': cateId})

        return ret

    def _createFormula(self):
        targetItemId = self.itemId
        idx = self.idx
        p = BigWorld.player()
        ret = {}
        eData = ESD.data.get((targetItemId, idx))
        if eData:
            items = eData.get('materialNeed', ())
            itemGroup = eData.get('materialSetNeed', ())
            groupItems = [ [item.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT), item['itemId'], item['numRange'][0]] for item in ISSD.data.get(itemGroup, []) ]
            items += tuple(groupItems)
            material = []
            self.hasBindMaterial = False
            for itemSearchType, itemId, itemNum in items:
                iData = ID.data.get(itemId, {})
                iconPath = uiUtils.getItemIconFile64(itemId)
                quality = iData.get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                enableParentCheck = True if itemSearchType == gametypes.ITEM_MIX_TYPE_PARENT else False
                maxNum = p.inv.countItemInPages(itemId, enableParentCheck=enableParentCheck)
                if p.inv.countItemInPages(itemId, enableParentCheck=enableParentCheck, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY):
                    self.hasBindMaterial = True
                material.append({'iconPath': iconPath,
                 'quality': color,
                 'maxNum': maxNum,
                 'needNum': itemNum,
                 'itemId': itemId})

            tData = ID.data.get(targetItemId, {})
            iconPath = uiUtils.getItemIconFile64(targetItemId)
            quality = tData.get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            target = {'iconPath': iconPath,
             'quality': color,
             'itemId': targetItemId}
            ret = {'material': material,
             'target': target}
        return ret

    def _cashInfo(self, itemId, idx):
        ret = {}
        p = BigWorld.player()
        fData = ESD.data.get((itemId, idx), [])
        if fData:
            cash = fData.get('cashNeed', 0)
        ret['needCash'] = str(cash)
        ret['bindCash'] = str(p.bindCash)
        ret['cash'] = str(p.cash)
        return ret

    def refresh(self):
        if self.mediator:
            ret = self._createFormula()
            if len(ret) <= 0:
                return
            self.mediator.Invoke('setItemFormula', uiUtils.dict2GfxDict(ret, True))
            if self.itemId is None or self.idx is None:
                return
            itemId = str(self.itemId)
            idx = str(self.idx)
            self.mediator.Invoke('updateCash', (GfxValue(itemId), GfxValue(idx)))

    def onGetItemList(self, *arg):
        ret = self._createItemList()
        return uiUtils.array2GfxAarry(ret, True)

    def onGetItemFormula(self, *arg):
        self.itemId = int(arg[3][0].GetString())
        self.idx = int(arg[3][1].GetString())
        ret = self._createFormula()
        return uiUtils.dict2GfxDict(ret, True)

    def onGetOtherInfo(self, *arg):
        itemId = int(arg[3][0].GetString())
        idx = int(arg[3][1].GetString())
        return uiUtils.dict2GfxDict(self._cashInfo(itemId, idx), True)

    @ui.callFilter(1)
    def onConfirm(self, *arg):
        itemId = int(arg[3][0].GetString())
        idx = int(arg[3][1].GetString())
        data = ESD.data.get((itemId, idx))
        if data:
            name = uiUtils.getItemColorName(itemId)
            msg = uiUtils.getTextFromGMD(GMDD.data.MIX_ITEM_CONFIRM_TEXT)
            if msg:
                msg = msg % name
            else:
                msg = gameStrings.TEXT_EQUIPMIXNEWPROXY_539 % name
            targetBind = ID.data.get(itemId, {}).get('bindType', 0) == gametypes.ITEM_BIND_TYPE_FOREVER
            if self.hasBindMaterial or targetBind:
                bindHint = uiUtils.getTextFromGMD(GMDD.data.MIX_ITEM_BINDHINT_TEXT)
                if not bindHint:
                    bindHint = gameStrings.TEXT_EQUIPMIXNEWPROXY_544
                msg += bindHint
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onTrueCommit, itemId, idx))

    def onTrueCommit(self, itemId, idx):
        npcEnt = BigWorld.entities.get(self.entityId)
        npcEnt and npcEnt.cell.mixEquipItem(itemId, idx)

    def onClose(self, *arg):
        self.hide()

    def getTargetToolTip(self):
        item = Item(self.itemId)
        if self.hasBindMaterial:
            item.bindType = gametypes.ITEM_BIND_TYPE_FOREVER
        return gameglobal.rds.ui.inventory.GfxToolTip(item, const.ITEM_IN_NONE)
