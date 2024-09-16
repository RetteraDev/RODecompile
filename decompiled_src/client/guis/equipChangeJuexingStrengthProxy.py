#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeJuexingStrengthProxy.o
import BigWorld
import const
import gametypes
import commcalc
import gameglobal
import utils
import copy
from callbackHelper import Functor
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import uiUtils
from guis.equipChangeJuexingRebuildProxy import EquipChangeJuexingRebuildProxy
from cdata import equip_juexing_reforge_data as EJRD
from cdata import game_msg_def_data as GMDD

def checkTabVisible():
    if not gameglobal.rds.configData.get('enableEquipChangeJuexingStrength', False):
        return False
    p = BigWorld.player()
    for i, item in enumerate(p.equipment):
        if not item:
            continue
        if uiUtils.isItemHasJuexingNew(item):
            return True

    for pos in gametypes.EQU_PART_SUB:
        item = commcalc.getAlternativeEquip(p, pos)
        if not item:
            continue
        if uiUtils.isItemHasJuexingNew(item):
            return True

    for pg in p.inv.getPageTuple():
        for ps in p.inv.getPosTuple(pg):
            item = p.inv.getQuickVal(pg, ps)
            if item == const.CONT_EMPTY_VAL:
                continue
            if uiUtils.isItemHasJuexingNew(item):
                return True

    return False


class EquipChangeJuexingStrengthProxy(EquipChangeJuexingRebuildProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeJuexingStrengthProxy, self).__init__(uiAdapter)
        self.modelMap.update({'confirm': self.onConfirm,
         'useOld': self.onUseOld,
         'useNew': self.onUseNew})

    def initDataModel(self, dataModel, whichModel):
        super(EquipChangeJuexingStrengthProxy, self).initDataModel(dataModel, whichModel)

    def checkItem(self, item):
        if not item:
            return False
        return uiUtils.isItemHasJuexingNew(item)

    def onConfirm(self, *arg):
        item = self.getSelectItem()
        if not item:
            return
        if uiUtils.isItemHasTempJuexingNewGoldProp(item):
            msg = uiUtils.getTextFromGMD(GMDD.data.NEW_JUEXING_HIGH_QUALITY_HINT)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.realTrueConfirm)
            return
        self.realTrueConfirm()

    def realTrueConfirm(self):
        p = BigWorld.player()
        item = self.getSelectItem()
        if not item:
            return
        if item.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
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
        if not gameglobal.rds.configData.get('enableEquipChangeJuexingStrength', False):
            return
        item = self.getSelectItem()
        if not item:
            return
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        p = BigWorld.player()
        p.cell.reforgeEquipJuexingStrength(self.selectedPos[0], self.selectedPos[1], realPos)

    def selectJuexing(self, isNew):
        item = self.getSelectItem()
        if not item:
            return
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        BigWorld.player().cell.confirmReforgeEquipJuexingStrength(isNew, self.selectedPos[0], self.selectedPos[1], realPos, item.uuid)

    def getJuexingAddtionInfo(self):
        info = {}
        info['showFree'] = False
        return info

    def juexingStrengthResult(self, resKind, page, pos, itemUUID, tempJXStrength, tempJXAddRatio):
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
                newItem.tempJXStrength = tempJXStrength
                newItem.tempJXAddRatio = tempJXAddRatio
            item = self.getSelectItem()
            if not item:
                return
            if item.uuid == itemUUID:
                self.refreshDetailInfo()
            return

    def juexingStrengthFinish(self, resKind, page, pos, itemUUID, ok):
        self.refreshLeftList(resKind)
        item = self.getSelectItem()
        if not item:
            return
        if item.uuid == itemUUID:
            self.refreshDetailInfo(ok)

    def getJuexingOriginInfo(self, item):
        info = {}
        customPropColor = {'baseProp': {}}
        juexingDataList = getattr(item, 'enhJuexingData', {})
        for key in juexingDataList.iterkeys():
            if not uiUtils.hasJuexingNew(key):
                customPropColor['baseProp'][key] = '#808080'

        setattr(item, 'customPropColor', customPropColor)
        info['juexingList'] = uiUtils.buildJuexingContentList(item)
        del item.customPropColor
        return info

    def getJuexingNewInfo(self, item):
        info = {}
        if not hasattr(item, 'enhJuexingAddRatio'):
            return info
        newItem = copy.deepcopy(item)
        tempJXStrength = getattr(newItem, 'tempJXStrength', [])
        tempJXAddRatio = getattr(newItem, 'tempJXAddRatio', [])
        if len(tempJXStrength) > 0:
            info['hasNewJuexing'] = True
            newItem.enhJuexingData = tempJXStrength
            newItem.enhJuexingAddRatio = tempJXAddRatio
            customPropColor = {'baseProp': {}}
            for key in newItem.enhJuexingData.iterkeys():
                if not uiUtils.hasJuexingNew(key):
                    customPropColor['baseProp'][key] = '#808080'

            setattr(newItem, 'customPropColor', customPropColor)
            info['newJuexingList'] = uiUtils.buildJuexingContentList(newItem)
        else:
            info['hasNewJuexing'] = False
        return info

    def calcAddRatio(self, old, new):
        if old == 0:
            return 0
        return max(new / old - 1, 0)

    def getMaterialIdAndNum(self, item):
        enhJuexingData = getattr(item, 'enhJuexingData', {})
        maxJuexingLv = 0
        for key in enhJuexingData:
            if enhJuexingData[key]:
                if key > maxJuexingLv:
                    maxJuexingLv = key

        itemNeed = EJRD.data.get(maxJuexingLv, {}).get('strengthItemNeed', [])
        if not itemNeed:
            return (-1, -1)
        return itemNeed[0]

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
            itemDict = {self.materialId: self.materialNum}
            if self.uiAdapter.equipChange.useDiKou:
                btnEnabled = uiUtils.checkEquipMaterialDiKou(itemDict)
            else:
                btnEnabled = own >= self.materialNum
            info['useDiKou'] = self.uiAdapter.equipChange.useDiKou
            info['diKouInfo'] = uiUtils.getEquipMaterialDiKouInfo(itemDict)
            info['isFree'] = False
            if info['isFree']:
                info['btnLabel'] = gameStrings.EQUIP_CHANGE_JUEXING_REBUILD_CONFIRM_BTN_FREE
                info['btnEnabled'] = True
            else:
                info['btnLabel'] = gameStrings.EQUIP_CHANGE_JUEXING_REBUILD_CONFIRM_BTN
                info['btnEnabled'] = btnEnabled
            self.panelMc.Invoke('refreshConsumeInfo', uiUtils.dict2GfxDict(info, True))
