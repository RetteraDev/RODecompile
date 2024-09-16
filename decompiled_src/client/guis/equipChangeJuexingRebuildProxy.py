#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeJuexingRebuildProxy.o
from gamestrings import gameStrings
import BigWorld
import uiUtils
import const
import utils
import copy
import gametypes
import commcalc
import gameglobal
from uiProxy import UIProxy
from callbackHelper import Functor
from gamestrings import gameStrings
from data import sys_config_data as SCD
from cdata import equip_juexing_reforge_data as EJRD
from cdata import game_msg_def_data as GMDD

def sort_unEquip(a, b):
    if a['quality'] > b['quality']:
        return -1
    if a['quality'] < b['quality']:
        return 1
    if a['sortIdx'] < b['sortIdx']:
        return -1
    if a['sortIdx'] > b['sortIdx']:
        return 1
    if a['score'] > b['score']:
        return -1
    if a['score'] < b['score']:
        return 1
    return 0


class EquipChangeJuexingRebuildProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeJuexingRebuildProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getDetailInfo': self.onGetDetailInfo,
         'getConsumeInfo': self.onGetConsumeInfo,
         'setDiKouFlag': self.onSetDiKouFlag,
         'removeItem': self.onRemoveItem,
         'confirm': self.onConfirm,
         'useOld': self.onUseOld,
         'useNew': self.onUseNew,
         'clickYunChuiBtn': self.onClickYunChuiBtn,
         'clickCoinBtn': self.onClickCoinBtn,
         'showHelp': self.onShowHelp}
        self.panelMc = None
        self.selectedPos = None
        self.materialId = 0
        self.materialNum = 0

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.refreshLeftList()

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.selectedPos = None

    def refreshLeftList(self, refreshKind = -1):
        if self.panelMc:
            p = BigWorld.player()
            info = {}
            refreshAll = refreshKind == -1
            equipList = []
            if refreshAll or refreshKind == const.RES_KIND_EQUIP:
                for i, item in enumerate(p.equipment):
                    if not item:
                        continue
                    if not self.checkItem(item):
                        continue
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                    itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                    itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                    itemInfo['pos'] = [const.RES_KIND_EQUIP, 0, i]
                    equipList.append(itemInfo)

                equipList.sort(key=lambda x: x['sortIdx'])
            info['equipList'] = equipList
            subEquipList = []
            if refreshAll or refreshKind == const.RES_KIND_SUB_EQUIP_BAG:
                for pos in gametypes.EQU_PART_SUB:
                    item = commcalc.getAlternativeEquip(p, pos)
                    if not item:
                        continue
                    if not self.checkItem(item):
                        continue
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                    itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                    itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                    itemInfo['pos'] = [const.RES_KIND_SUB_EQUIP_BAG, 0, pos]
                    subEquipList.append(itemInfo)

                subEquipList.sort(key=lambda x: x['sortIdx'])
            info['subEquipList'] = subEquipList
            unEquipList = []
            if refreshAll or refreshKind == const.RES_KIND_INV:
                for pg in p.inv.getPageTuple():
                    for ps in p.inv.getPosTuple(pg):
                        item = p.inv.getQuickVal(pg, ps)
                        if item == const.CONT_EMPTY_VAL:
                            continue
                        if not self.checkItem(item):
                            continue
                        itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                        itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                        itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                        itemInfo['quality'] = getattr(item, 'quality', 0)
                        itemInfo['score'] = getattr(item, 'score', 0)
                        itemInfo['pos'] = [const.RES_KIND_INV, pg, ps]
                        unEquipList.append(itemInfo)

                unEquipList.sort(cmp=sort_unEquip)
            info['unEquipList'] = unEquipList
            info['refreshAll'] = refreshAll
            info['refreshKind'] = refreshKind
            info['noItemHint'] = self.getNoItemHint()
            self.panelMc.Invoke('refreshLeftList', uiUtils.dict2GfxDict(info, True))

    def getSelectItem(self):
        p = BigWorld.player()
        item = None
        if self.selectedPos and self.selectedPos[0] == const.RES_KIND_EQUIP:
            item = p.equipment.get(self.selectedPos[2])
        elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            item = commcalc.getAlternativeEquip(p, self.selectedPos[2])
        elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
            item = p.inv.getQuickVal(self.selectedPos[1], self.selectedPos[2])
        return item

    def onGetDetailInfo(self, *arg):
        kind = int(arg[3][0].GetNumber())
        page = int(arg[3][1].GetNumber())
        pos = int(arg[3][2].GetNumber())
        if self.selectedPos and self.selectedPos[0] == kind and self.selectedPos[1] == page and self.selectedPos[2] == pos:
            return
        self.selectedPos = (kind, page, pos)
        self.refreshDetailInfo()

    def refreshDetailInfo(self, playEffect = False):
        if self.panelMc:
            info = {}
            item = self.getSelectItem()
            if item and hasattr(item, 'enhJuexingData'):
                targetItemInfo = {}
                if self.selectedPos and self.selectedPos[0] in (const.RES_KIND_EQUIP, const.RES_KIND_SUB_EQUIP_BAG):
                    targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
                    targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                info['targetItemInfo'] = targetItemInfo
                info.update(self.getJuexingOriginInfo(item))
                info.update(self.getJuexingNewInfo(item))
                info['playEffect'] = playEffect
                info['isEmpty'] = False
            else:
                info['isEmpty'] = True
            info.update(self.getJuexingAddtionInfo())
            self.panelMc.Invoke('refreshDetailInfo', uiUtils.dict2GfxDict(info, True))

    def onGetConsumeInfo(self, *arg):
        self.refreshConsumeInfo()

    def onSetDiKouFlag(self, *arg):
        self.uiAdapter.equipChange.useDiKou = arg[3][0].GetBool()
        self.refreshConsumeInfo()

    def refreshConsumeInfo(self):
        if self.panelMc:
            p = BigWorld.player()
            info = {}
            item = self.getSelectItem()
            if not item:
                return
            self.materialId, self.materialNum = self.getMaterialIdAndNum(item)
            materialInfo = uiUtils.getGfxItemById(self.materialId)
            own = p.inv.countItemInPages(self.materialId, enableParentCheck=True)
            materialInfo['numStr'] = uiUtils.convertNumStr(own, self.materialNum, notEnoughColor='#E51717')
            materialInfo['needHelp'] = own < self.materialNum
            info['materialInfo'] = materialInfo
            if self.uiAdapter.equipChange.useDiKou:
                itemDict = {self.materialId: self.materialNum}
                btnEnabled = uiUtils.checkEquipMaterialDiKou(itemDict)
            else:
                itemDict = {}
                btnEnabled = own >= self.materialNum
            info['useDiKou'] = self.uiAdapter.equipChange.useDiKou
            info['diKouInfo'] = uiUtils.getEquipMaterialDiKouInfo(itemDict)
            info['isFree'] = self.getMaterialIsFree()
            if info['isFree']:
                info['btnLabel'] = gameStrings.EQUIP_CHANGE_JUEXING_REBUILD_CONFIRM_BTN_FREE
                info['btnEnabled'] = True
            else:
                info['btnLabel'] = gameStrings.EQUIP_CHANGE_JUEXING_REBUILD_CONFIRM_BTN
                info['btnEnabled'] = btnEnabled
            self.panelMc.Invoke('refreshConsumeInfo', uiUtils.dict2GfxDict(info, True))

    def onRemoveItem(self, *arg):
        self.selectedPos = None
        self.refreshDetailInfo()

    def onConfirm(self, *arg):
        item = self.getSelectItem()
        if not item:
            return
        if item.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        newItem = copy.deepcopy(item)
        tempJXAlldata = getattr(newItem, 'tempJXAlldata', [])
        if len(tempJXAlldata) > 0:
            for value in tempJXAlldata:
                newItem.enhJuexingData[value[0]] = value[1]

            newJuexingList = uiUtils.buildJuexingContentList(newItem)
        else:
            newJuexingList = []
        for value in newJuexingList:
            if value[3] >= 3:
                msg = uiUtils.getTextFromGMD(GMDD.data.NEW_JUEXING_HIGH_QUALITY_HINT)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirmStep1)
                return

        self.trueConfirmStep1()

    def trueConfirmStep1(self):
        p = BigWorld.player()
        item = self.getSelectItem()
        if not item:
            return
        if gameglobal.rds.configData.get('enableFreeJuexingRebuild', False) and p.getFame(const.REFORGE_EQUIP_JUEXING_FAME_ID) > 0:
            if not item.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
            else:
                self.trueConfirm()
            return
        if self.uiAdapter.equipChange.useDiKou:
            itemDict = {self.materialId: self.materialNum}
        else:
            itemDict = {}
        _, yunChuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
        if yunChuiNeed > 0 and not item.isForeverBind():
            msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
            return
        if p.inv.countItemBind(self.materialId, enableParentCheck=True):
            if not item.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
            else:
                self.trueConfirm()
        else:
            self.trueConfirm()

    def trueConfirm(self):
        item = self.getSelectItem()
        if not item:
            return
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableFreeJuexingRebuild', False) and p.getFame(const.REFORGE_EQUIP_JUEXING_FAME_ID) > 0:
            isFree = True
        else:
            isFree = False
        p.cell.reforgeEquipJuexingAllNew(self.selectedPos[0], self.selectedPos[1], realPos, isFree)

    def onUseOld(self, *arg):
        item = self.getSelectItem()
        if not item:
            return
        if item.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.NEW_JUEXING_MISS_CONFIRM)
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.selectJuexing, False))

    def onUseNew(self, *arg):
        item = self.getSelectItem()
        if not item:
            return
        if item.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.OLD_JUEXING_MISS_CONFIRM)
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.selectJuexing, True))

    def selectJuexing(self, isNew):
        item = self.getSelectItem()
        if not item:
            return
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        BigWorld.player().cell.confirmReforgeEquipJuexingAllNew(isNew, self.selectedPos[0], self.selectedPos[1], realPos, item.uuid)

    def onClickYunChuiBtn(self, *arg):
        mall = self.uiAdapter.tianyuMall
        if mall.mallMediator:
            mall.hide()
        mall.show(keyWord=gameStrings.TEXT_INVENTORYPROXY_3299)

    def onClickCoinBtn(self, *arg):
        BigWorld.player().openRechargeFunc()

    def onShowHelp(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        if gameglobal.rds.configData.get('enableNewItemSearch', False):
            self.uiAdapter.itemSourceInfor.openPanel()
        else:
            self.uiAdapter.help.showByItemId(itemId)

    def juexingRebuildResult(self, resKind, page, pos, itemUUID, jxData):
        p = BigWorld.player()
        newItem = None
        if resKind == const.RES_KIND_EQUIP:
            newItem = p.equipment.get(pos)
        elif resKind == const.RES_KIND_SUB_EQUIP_BAG:
            newItem = commcalc.getAlternativeEquip(p, pos)
        elif resKind == const.RES_KIND_INV:
            newItem = p.inv.getQuickVal(page, pos)
        if not newItem:
            return
        else:
            if newItem.uuid == itemUUID:
                newItem.tempJXAlldata = jxData
            item = self.getSelectItem()
            if not item:
                return
            if item.uuid == itemUUID:
                self.refreshDetailInfo()
            return

    def juexingRebuildFinish(self, resKind, page, pos, itemUUID, ok):
        self.refreshLeftList(resKind)
        item = self.getSelectItem()
        if not item:
            return
        if item.uuid == itemUUID:
            self.refreshDetailInfo(ok)

    def checkItem(self, item):
        if not item or not hasattr(item, 'isItemCanRebuild'):
            return False
        return item.isItemCanRebuild()

    def getNoItemHint(self):
        return SCD.data.get('equipChangeJuexingRebuildNoItemHint', '')

    def getJuexingAddtionInfo(self):
        info = {}
        if gameglobal.rds.configData.get('enableFreeJuexingRebuild', False):
            info['showFree'] = True
            freeNum = BigWorld.player().getFame(const.REFORGE_EQUIP_JUEXING_FAME_ID)
            info['freeNum'] = freeNum
            info['freeTips'] = SCD.data.get('equipChangeJuexingRebuildFreeTips', '')
        else:
            info['showFree'] = False
        return info

    def getJuexingOriginInfo(self, item):
        info = {}
        customPropColor = {'baseProp': {},
         'ratioProp': {}}
        for key in item.enhJuexingData.iterkeys():
            if uiUtils.hasJuexingNew(key):
                customPropColor['baseProp'][key] = '#808080'
            else:
                customPropColor['ratioProp'][key] = '#808080'

        setattr(item, 'customPropColor', customPropColor)
        info['juexingList'] = uiUtils.buildJuexingContentList(item)
        del item.customPropColor
        return info

    def getJuexingNewInfo(self, item):
        info = {}
        newItem = copy.deepcopy(item)
        tempJXAlldata = getattr(newItem, 'tempJXAlldata', [])
        if len(tempJXAlldata) > 0:
            info['hasNewJuexing'] = True
            for value in tempJXAlldata:
                newItem.enhJuexingData[value[0]] = value[1]

            customPropColor = {'baseProp': {},
             'ratioProp': {}}
            for key in newItem.enhJuexingData.iterkeys():
                if uiUtils.hasJuexingNew(key):
                    customPropColor['baseProp'][key] = '#808080'
                else:
                    customPropColor['ratioProp'][key] = '#808080'

            setattr(newItem, 'customPropColor', customPropColor)
            info['newJuexingList'] = uiUtils.buildJuexingContentList(newItem)
        else:
            info['hasNewJuexing'] = False
        return info

    def getMaterialIdAndNum(self, item):
        enhJuexingData = getattr(item, 'enhJuexingData', {})
        maxJuexingLv = 0
        for key in enhJuexingData:
            if enhJuexingData[key]:
                if key > maxJuexingLv:
                    maxJuexingLv = key

        itemNeed = EJRD.data.get(maxJuexingLv, {}).get('itemNeed', [])
        if not itemNeed:
            return (-1, -1)
        return itemNeed[0]

    def getMaterialIsFree(self):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableFreeJuexingRebuild', False):
            return p.getFame(const.REFORGE_EQUIP_JUEXING_FAME_ID) > 0
        else:
            return False
