#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangePrefixTransferProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import const
import ui
import gametypes
import commcalc
from uiProxy import UIProxy
from Scaleform import GfxValue
from callbackHelper import Functor
from data import equip_pre_prop_exchange_data as EPPED
from cdata import item_synthesize_set_data as ISSD
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


class EquipChangePrefixTransferProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangePrefixTransferProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getFitPos': self.onGetFitPos,
         'filterLeftList': self.onFilterLeftList,
         'getDetailInfo': self.onGetDetailInfo,
         'getConsumeInfo': self.onGetConsumeInfo,
         'removeItem': self.onRemoveItem,
         'confirm': self.onConfirm,
         'showHelp': self.onShowHelp}
        self.panelMc = None
        self.selectedPos = None
        self.tgtSelectedPos = None
        self.lastTransfer = None
        self.prefixTransferMap = {}

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.initData()
        self.refreshLeftList()

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.selectedPos = None
        self.tgtSelectedPos = None
        self.lastTransfer = None

    def initData(self):
        if self.prefixTransferMap != {}:
            return
        for key, value in EPPED.data.iteritems():
            itemId = value.get('id', 0)
            targetId = value.get('targetId', [])
            if itemId <= 0 or targetId == []:
                continue
            if itemId not in self.prefixTransferMap:
                self.prefixTransferMap[itemId] = {}
            for tId in targetId:
                self.prefixTransferMap[itemId][tId] = key

    def refreshLeftList(self, refreshKind = -1):
        if self.panelMc:
            p = BigWorld.player()
            info = {}
            refreshAll = refreshKind == -1
            srcItem = self.getTransferItem(0)
            srcItemId = srcItem.id if srcItem else 0
            equipList = []
            if refreshAll or refreshKind == const.RES_KIND_EQUIP:
                for i, item in enumerate(p.equipment):
                    if not item:
                        continue
                    if not self.canTransfer(item, srcItemId):
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
                    if not self.canTransfer(item, srcItemId):
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
                        if not self.canTransfer(item, srcItemId):
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
            self.panelMc.Invoke('refreshLeftList', uiUtils.dict2GfxDict(info, True))

    def canTransfer(self, item, srcItemId):
        if not item.isEquip():
            return False
        if item.isYaoPei():
            return False
        if srcItemId <= 0:
            if item.id not in self.prefixTransferMap:
                return False
        else:
            targetId = self.prefixTransferMap.get(srcItemId, {})
            if item.id not in targetId:
                return False
        return True

    def getTransferItem(self, idx):
        p = BigWorld.player()
        item = None
        if idx == 0:
            if self.selectedPos and self.selectedPos[0] == const.RES_KIND_EQUIP:
                item = p.equipment.get(self.selectedPos[2])
            elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
                item = commcalc.getAlternativeEquip(p, self.selectedPos[2])
            elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
                item = p.inv.getQuickVal(self.selectedPos[1], self.selectedPos[2])
        elif idx == 1:
            if self.tgtSelectedPos and self.tgtSelectedPos[0] == const.RES_KIND_EQUIP:
                item = p.equipment.get(self.tgtSelectedPos[2])
            elif self.tgtSelectedPos and self.tgtSelectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
                item = commcalc.getAlternativeEquip(p, self.tgtSelectedPos[2])
            elif self.tgtSelectedPos and self.tgtSelectedPos[0] == const.RES_KIND_INV:
                item = p.inv.getQuickVal(self.tgtSelectedPos[1], self.tgtSelectedPos[2])
        return item

    def onGetFitPos(self, *arg):
        kind = int(arg[3][0].GetNumber())
        page = int(arg[3][1].GetNumber())
        pos = int(arg[3][2].GetNumber())
        p = BigWorld.player()
        srcItem = self.getTransferItem(0)
        newItem = None
        if kind == const.RES_KIND_EQUIP:
            newItem = p.equipment.get(pos)
        elif kind == const.RES_KIND_SUB_EQUIP_BAG:
            newItem = commcalc.getAlternativeEquip(p, pos)
        elif kind == const.RES_KIND_INV:
            newItem = p.inv.getQuickVal(page, pos)
        fitPos = -1
        if not newItem:
            pass
        elif not srcItem:
            fitPos = 0
        elif self.canTransfer(newItem, srcItem.id):
            fitPos = 1
        return GfxValue(fitPos)

    def onFilterLeftList(self, *arg):
        self.refreshLeftList()

    def onGetDetailInfo(self, *arg):
        kind = int(arg[3][0].GetNumber())
        page = int(arg[3][1].GetNumber())
        pos = int(arg[3][2].GetNumber())
        tKind = int(arg[3][3].GetNumber())
        tPage = int(arg[3][4].GetNumber())
        tPos = int(arg[3][5].GetNumber())
        if self.selectedPos and self.selectedPos[0] == kind and self.selectedPos[1] == page and self.selectedPos[2] == pos and self.tgtSelectedPos and self.tgtSelectedPos[0] == tKind and self.tgtSelectedPos[1] == tPage and self.tgtSelectedPos[2] == tPos:
            return
        self.selectedPos = (kind, page, pos)
        self.tgtSelectedPos = (tKind, tPage, tPos)
        self.refreshDetailInfo()

    def refreshDetailInfo(self, playEffect = False):
        if self.panelMc:
            info = {}
            srcItem = self.getTransferItem(0)
            if srcItem:
                srcItemInfo = {}
                if self.selectedPos and self.selectedPos[0] in (const.RES_KIND_EQUIP, const.RES_KIND_SUB_EQUIP_BAG):
                    srcItemInfo = uiUtils.getGfxItem(srcItem, location=const.ITEM_IN_EQUIPMENT)
                elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
                    srcItemInfo = uiUtils.getGfxItem(srcItem, location=const.ITEM_IN_BAG)
                info['srcItemInfo'] = srcItemInfo
                info['srcItemNeedClear'] = False
            else:
                info['srcItemNeedClear'] = True
            tgtItem = self.getTransferItem(1)
            if tgtItem:
                tgtItemInfo = {}
                if self.tgtSelectedPos and self.tgtSelectedPos[0] in (const.RES_KIND_EQUIP, const.RES_KIND_SUB_EQUIP_BAG):
                    tgtItemInfo = uiUtils.getGfxItem(tgtItem, location=const.ITEM_IN_EQUIPMENT)
                elif self.tgtSelectedPos and self.tgtSelectedPos[0] == const.RES_KIND_INV:
                    tgtItemInfo = uiUtils.getGfxItem(tgtItem, location=const.ITEM_IN_BAG)
                info['tgtItemInfo'] = tgtItemInfo
                info['tgtItemNeedClear'] = False
            else:
                info['tgtItemNeedClear'] = True
            if srcItem and tgtItem:
                srcPrefixProp = uiUtils.getItemPreprops(srcItem, True)
                if srcPrefixProp != '':
                    srcPrefixTitle = gameStrings.TEXT_EQUIPCHANGEPREFIXTRANSFERPROXY_271 % uiUtils.getItemPreName(srcItem)
                    srcPrefixPropList = srcPrefixProp.split('<br>')
                else:
                    srcPrefixTitle = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                    srcPrefixPropList = []
                info['srcPrefixTitle'] = srcPrefixTitle
                info['srcPrefixPropList'] = srcPrefixPropList
                tgtPrefixProp = uiUtils.getItemPreprops(tgtItem, True)
                if tgtPrefixProp != '':
                    tgtPrefixTitle = gameStrings.TEXT_EQUIPCHANGEPREFIXTRANSFERPROXY_271 % uiUtils.getItemPreName(tgtItem)
                    tgtPrefixPropList = tgtPrefixProp.split('<br>')
                else:
                    tgtPrefixTitle = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                    tgtPrefixPropList = []
                info['tgtPrefixTitle'] = tgtPrefixTitle
                info['tgtPrefixPropList'] = tgtPrefixPropList
                info['playEffect'] = playEffect
                info['isEmpty'] = False
            else:
                info['isEmpty'] = True
            self.panelMc.Invoke('refreshDetailInfo', uiUtils.dict2GfxDict(info, True))

    def onGetConsumeInfo(self, *arg):
        self.refreshConsumeInfo()

    def refreshConsumeInfo(self):
        if self.panelMc:
            p = BigWorld.player()
            info = {}
            srcItem = self.getTransferItem(0)
            tgtItem = self.getTransferItem(1)
            if not srcItem or not tgtItem:
                return
            eid = self.prefixTransferMap.get(srcItem.id, {}).get(tgtItem.id, 0)
            epped = EPPED.data.get(eid, {})
            if not epped:
                return
            btnEnabled = True
            materialSetNeed = epped.get('materialSetNeed', 0)
            issd = ISSD.data.get(materialSetNeed, [])
            itemList = []
            for issdData in issd:
                itemId = issdData.get('itemId', 0)
                if itemId == 0:
                    continue
                itemNum = issdData.get('numRange', (0, 0))[0]
                itemInfo = uiUtils.getGfxItemById(itemId)
                enableParentCheck = True if issdData.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT) == gametypes.ITEM_MIX_TYPE_PARENT else False
                own = p.inv.countItemInPages(itemId, enableParentCheck=enableParentCheck)
                itemInfo['numStr'] = uiUtils.convertNumStr(own, itemNum, notEnoughColor='#E51717')
                itemInfo['needHelp'] = own < itemNum
                if own < itemNum:
                    btnEnabled = False
                itemList.append(itemInfo)

            info['itemList'] = itemList
            needCash = epped.get('cashNeed', 0)
            info['cashStr'] = uiUtils.convertNumStr(p.cash, needCash, showOwnStr=False, needThousand=True)
            if p.cash < needCash:
                btnEnabled = False
            info['btnEnabled'] = btnEnabled
            self.panelMc.Invoke('refreshConsumeInfo', uiUtils.dict2GfxDict(info, True))

    def onRemoveItem(self, *arg):
        idx = int(arg[3][0].GetNumber())
        needRefresh = arg[3][1].GetBool()
        if idx == 0:
            self.selectedPos = None
            self.refreshLeftList()
        elif idx == 1:
            self.tgtSelectedPos = None
        if needRefresh:
            self.refreshDetailInfo()

    def onConfirm(self, *arg):
        p = BigWorld.player()
        srcItem = self.getTransferItem(0)
        tgtItem = self.getTransferItem(1)
        if not srcItem or not tgtItem:
            return
        if srcItem.hasLatch() or tgtItem.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        if getattr(srcItem, 'preprops', []) == getattr(tgtItem, 'preprops', []):
            p.showGameMsg(GMDD.data.PRE_PROP_IS_SAME, ())
            return
        if not srcItem.isForeverBind() or not tgtItem.isForeverBind():
            msg = uiUtils.getTextFromGMD(GMDD.data.PRE_PROPS_ITEM_BINDHINT_TEXT, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.trueConfirmStep1)
        else:
            self.trueConfirmStep1()

    def trueConfirmStep1(self):
        srcItem = self.getTransferItem(0)
        tgtItem = self.getTransferItem(1)
        if not srcItem or not tgtItem:
            return
        if self.lastTransfer and self.lastTransfer[0] == srcItem.uuid and self.lastTransfer[1] == tgtItem.uuid:
            msg = uiUtils.getTextFromGMD(GMDD.data.PRE_PROPS_CHANGE_SECOND_TIME, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.trueConfirmStep2, srcItem, tgtItem))
        else:
            self.trueConfirmStep2(srcItem, tgtItem)

    @ui.looseGroupTradeConfirm(1, GMDD.data.PRE_PROP_EXCHANGE)
    def trueConfirmStep2(self, srcItem, tgtItem):
        self.trueConfirmStep3(srcItem, tgtItem)

    @ui.looseGroupTradeConfirm(2, GMDD.data.PRE_PROP_EXCHANGE)
    def trueConfirmStep3(self, srcItem, tgtItem):
        self.trueConfirm()

    def trueConfirm(self):
        srcItem = self.getTransferItem(0)
        tgtItem = self.getTransferItem(1)
        if not srcItem or not tgtItem:
            return
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        tgtRealPos = self.tgtSelectedPos[2]
        if self.tgtSelectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            tgtRealPos = gametypes.equipTosubEquipPartMap.get(self.tgtSelectedPos[2], -1)
        if tgtRealPos < 0:
            return
        eid = self.prefixTransferMap.get(srcItem.id, {}).get(tgtItem.id, 0)
        epped = EPPED.data.get(eid, {})
        if not epped:
            return
        BigWorld.player().cell.exchangeEquipPrePropNew(self.selectedPos[0], self.selectedPos[1], realPos, self.tgtSelectedPos[0], self.tgtSelectedPos[1], tgtRealPos, eid)

    def onShowHelp(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        if gameglobal.rds.configData.get('enableNewItemSearch', False):
            self.uiAdapter.itemSourceInfor.openPanel()
        else:
            self.uiAdapter.help.showByItemId(itemId)

    def prefixTransferSuccess(self, srcUUID, tgtUUID):
        self.refreshLeftList()
        self.refreshDetailInfo(True)
        BigWorld.player().showGameMsg(GMDD.data.PRE_PROP_TRANSFER_SUCCESS, ())
        self.lastTransfer = (srcUUID, tgtUUID)
