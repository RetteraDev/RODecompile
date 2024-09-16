#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeEnhanceTransferProxy.o
from gamestrings import gameStrings
import BigWorld
import uiUtils
import const
import ui
import utils
import copy
import gametypes
import commcalc
import gameglobal
from uiProxy import UIProxy
from Scaleform import GfxValue
from cdata import equip_enhancement_transfer_data as EETD
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


class EquipChangeEnhanceTransferProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeEnhanceTransferProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getFitPos': self.onGetFitPos,
         'getDetailInfo': self.onGetDetailInfo,
         'getConsumeInfo': self.onGetConsumeInfo,
         'setKeepLvFlag': self.onSetKeepLvFlag,
         'setDiKouFlag': self.onSetDiKouFlag,
         'removeItem': self.onRemoveItem,
         'confirm': self.onConfirm,
         'clickYunChuiBtn': self.onClickYunChuiBtn,
         'clickCoinBtn': self.onClickCoinBtn,
         'showHelp': self.onShowHelp}
        self.panelMc = None
        self.selectedPos = None
        self.tgtSelectedPos = None
        self.keepLv = True

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.refreshLeftList()

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.selectedPos = None
        self.tgtSelectedPos = None
        self.keepLv = True

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
                    if not self.canEnhance(item):
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
                    if not self.canEnhance(item):
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
                        if not self.canEnhance(item):
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

    def canEnhance(self, item):
        if not item.isEquip():
            return False
        if item.isYaoPei():
            return False
        if item.getMaxEnhLv(BigWorld.player()) == 0:
            return False
        return True

    def getEnhanceItem(self, idx):
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
        srcItem = self.getEnhanceItem(0)
        tgtItem = self.getEnhanceItem(1)
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
        elif not srcItem and not tgtItem:
            fitPos = 0
        elif not srcItem and tgtItem:
            if getattr(newItem, 'enhLv', 0) <= getattr(tgtItem, 'enhLv', 0):
                p.showGameMsg(GMDD.data.EQUIP_ENHANCE_TRANSFER_ENHLV_ERROR, ())
            elif not EETD.data.get((getattr(newItem, 'enhLv', 0), tgtItem.order), {}):
                p.showGameMsg(GMDD.data.EQUIP_ENHANCE_TRANSFER_ITEM_ERROR, ())
            else:
                fitPos = 0
        elif getattr(srcItem, 'enhLv', 0) <= getattr(newItem, 'enhLv', 0):
            p.showGameMsg(GMDD.data.EQUIP_ENHANCE_TRANSFER_ENHLV_ERROR, ())
        elif not EETD.data.get((getattr(srcItem, 'enhLv', 0), newItem.order), {}):
            p.showGameMsg(GMDD.data.EQUIP_ENHANCE_TRANSFER_ITEM_ERROR, ())
        else:
            fitPos = 1
        return GfxValue(fitPos)

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

    def refreshDetailInfo(self):
        if self.panelMc:
            info = {}
            srcItem = self.getEnhanceItem(0)
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
            tgtItem = self.getEnhanceItem(1)
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
                info['star'] = uiUtils.getEquipStar(srcItem)
                info['starTips'] = gameStrings.TEXT_EQUIPCHANGEENHANCEPROXY_227
                newItem = copy.deepcopy(tgtItem)
                newEnhLv = getattr(srcItem, 'enhLv', 0)
                setattr(newItem, 'enhLv', newEnhLv)
                newEnhJuexingData = copy.deepcopy(getattr(srcItem, 'enhJuexingData', {}))
                setattr(newItem, 'enhJuexingData', newEnhJuexingData)
                newEnhanceRefining = copy.deepcopy(getattr(srcItem, 'enhanceRefining', {}))
                setattr(newItem, 'enhanceRefining', newEnhanceRefining)
                newEnhJuexingAddRatio = copy.deepcopy(getattr(srcItem, 'enhJuexingAddRatio', {}))
                setattr(newItem, 'enhJuexingAddRatio', newEnhJuexingAddRatio)
                newTotalNum, newLostNum, newEnhProp = uiUtils.getEquipTotalRefine(newItem)
                newNumStr = '+%d%%' % newTotalNum
                if newLostNum:
                    newNumStr += uiUtils.toHtml(' -%d%%' % newLostNum, color='#CC2929')
                if newEnhProp == '':
                    newEnhProp = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                newTotalRefine = '%s ( %s )' % (newEnhProp, newNumStr)
                info['newTotalRefine'] = newTotalRefine
                info['juexingList'] = uiUtils.buildJuexingContentList(newItem)
                info['isEmpty'] = False
            else:
                info['isEmpty'] = True
            self.panelMc.Invoke('refreshDetailInfo', uiUtils.dict2GfxDict(info, True))

    def onGetConsumeInfo(self, *arg):
        self.refreshConsumeInfo()

    def onSetKeepLvFlag(self, *arg):
        self.keepLv = arg[3][0].GetBool()
        self.refreshConsumeInfo()

    def onSetDiKouFlag(self, *arg):
        self.uiAdapter.equipChange.useDiKou = arg[3][0].GetBool()
        self.refreshConsumeInfo()

    def refreshConsumeInfo(self):
        if self.panelMc:
            p = BigWorld.player()
            info = {}
            srcItem = self.getEnhanceItem(0)
            tgtItem = self.getEnhanceItem(1)
            if not srcItem or not tgtItem:
                return
            valid, keepLvItemCost = self.getKeepLvItemCost(srcItem, tgtItem)
            if not valid:
                return
            btnEnabled = True
            info['showKeepLv'] = keepLvItemCost != []
            info['keepLv'] = self.keepLv
            if keepLvItemCost and self.keepLv:
                itemDict = {}
                itemList = []
                for itemId, num in keepLvItemCost:
                    itemDict[itemId] = num
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    own = p.inv.countItemInPages(itemId, enableParentCheck=True)
                    itemInfo['numStr'] = uiUtils.convertNumStr(own, num, notEnoughColor='#E51717')
                    itemInfo['needHelp'] = own < num
                    if own < num:
                        btnEnabled = False
                    itemList.append(itemInfo)

                info['itemList'] = itemList
                if self.uiAdapter.equipChange.useDiKou:
                    btnEnabled = uiUtils.checkEquipMaterialDiKou(itemDict)
                else:
                    itemDict = {}
                info['useDiKou'] = self.uiAdapter.equipChange.useDiKou
                info['diKouInfo'] = uiUtils.getEquipMaterialDiKouInfo(itemDict)
            needCash = EETD.data.get((getattr(srcItem, 'enhLv', 0), tgtItem.order), {}).get('mCost', 0)
            info['cashStr'] = uiUtils.convertNumStr(p.cash, needCash, showOwnStr=False, needThousand=True)
            if p.cash < needCash:
                btnEnabled = False
            info['btnEnabled'] = btnEnabled
            self.panelMc.Invoke('refreshConsumeInfo', uiUtils.dict2GfxDict(info, True))

    def getKeepLvItemCost(self, srcItem, tgtItem):
        eetd = EETD.data.get((getattr(srcItem, 'enhLv', 0), tgtItem.order), {})
        if not eetd:
            return (False, [])
        if tgtItem.order <= srcItem.order:
            return (True, eetd.get('keepLvItemCostLow', []))
        return (True, eetd.get('keepLvItemCost', []))

    def onRemoveItem(self, *arg):
        idx = int(arg[3][0].GetNumber())
        needRefresh = arg[3][1].GetBool()
        if idx == 0:
            self.selectedPos = None
        elif idx == 1:
            self.tgtSelectedPos = None
        if needRefresh:
            self.refreshDetailInfo()

    def onConfirm(self, *arg):
        srcItem = self.getEnhanceItem(0)
        tgtItem = self.getEnhanceItem(1)
        if not srcItem or not tgtItem:
            return
        if srcItem.hasLatch() or tgtItem.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        self.trueConfirmStep1(srcItem, tgtItem)

    @ui.checkEquipCanReturn(const.LAST_PARAMS, GMDD.data.RETURN_BACK_ENHANCE_TRANS)
    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.RETURN_BACK_ENHANCE_TRANS)
    def trueConfirmStep1(self, srcItem, tgtItem):
        if not hasattr(srcItem, 'equipType') or not hasattr(tgtItem, 'equipType') or not hasattr(srcItem, 'equipSType') or not hasattr(tgtItem, 'equipSType'):
            return
        if not srcItem.cmpGemEquipType(tgtItem.id):
            BigWorld.player().showGameMsg(GMDD.data.ENHANCE_TRANSFER_FAIL_GEM_EQUIT_TYPE, ())
            return
        if srcItem.equipType != tgtItem.equipType or srcItem.equipSType != tgtItem.equipSType:
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ENHANCE_TRANSFER_NOT_SAME_TYPE, '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirmStep2)
        else:
            self.trueConfirmStep2()

    def trueConfirmStep2(self):
        srcItem = self.getEnhanceItem(0)
        tgtItem = self.getEnhanceItem(1)
        if not srcItem or not tgtItem:
            return
        valid, keepLvItemCost = self.getKeepLvItemCost(srcItem, tgtItem)
        if not valid:
            return
        if keepLvItemCost and not self.keepLv:
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ENHANCE_TRANSFER_CAN_USE_KEEP_LV, '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirmStep3)
        else:
            self.trueConfirmStep3()

    def trueConfirmStep3(self):
        srcItem = self.getEnhanceItem(0)
        tgtItem = self.getEnhanceItem(1)
        if not srcItem or not tgtItem:
            return
        valid, keepLvItemCost = self.getKeepLvItemCost(srcItem, tgtItem)
        if not valid:
            return
        if keepLvItemCost and self.keepLv:
            itemDict = {}
            for itemId, num in keepLvItemCost:
                itemDict[itemId] = num

            _, _, coinNeed, _ = utils.calcEquipMaterialDiKou(BigWorld.player(), itemDict)
            if coinNeed > 0:
                msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ENHANCE_TRANSFER_NEED_COIN, '')
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirmStep4)
                return
        self.trueConfirmStep4()

    def trueConfirmStep4(self):
        srcItem = self.getEnhanceItem(0)
        tgtItem = self.getEnhanceItem(1)
        if not srcItem or not tgtItem:
            return
        valid, keepLvItemCost = self.getKeepLvItemCost(srcItem, tgtItem)
        if not valid:
            return
        if keepLvItemCost and self.keepLv:
            itemDict = {}
            for itemId, num in keepLvItemCost:
                itemDict[itemId] = num

            _, yunChuiNeed, _, _ = utils.calcEquipMaterialDiKou(BigWorld.player(), itemDict)
            if yunChuiNeed > 0 and not tgtItem.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ENHANCE_TRANSFER_BIND, '%s') % ''
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirmStep5)
                return
        if srcItem.isForeverBind() and not tgtItem.isForeverBind():
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ENHANCE_TRANSFER_BIND, '%s') % uiUtils.getItemColorNameByItem(srcItem)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirmStep5)
        else:
            self.trueConfirmStep5()

    def trueConfirmStep5(self):
        srcItem = self.getEnhanceItem(0)
        tgtItem = self.getEnhanceItem(1)
        if not srcItem or not tgtItem:
            return
        if getattr(srcItem, 'enhLv', 0) > tgtItem.getMaxEnhLv(BigWorld.player()):
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ENHANCE_TRANSFER_LV_INVALID, '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirmStep6)
        else:
            self.trueConfirmStep6()

    def trueConfirmStep6(self):
        srcItem = self.getEnhanceItem(0)
        tgtItem = self.getEnhanceItem(1)
        if not srcItem or not tgtItem:
            return
        if getattr(tgtItem, 'enhLv', 0) != 0:
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ENHANCE_TRANSFER_LV_COVER, '')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
        else:
            self.trueConfirm()

    def trueConfirm(self):
        srcItem = self.getEnhanceItem(0)
        tgtItem = self.getEnhanceItem(1)
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
        valid, keepLvItemCost = self.getKeepLvItemCost(srcItem, tgtItem)
        if not valid:
            return
        keepLv = self.keepLv if keepLvItemCost != [] else True
        BigWorld.player().cell.itemEnhancementTransferNew(self.selectedPos[0], self.selectedPos[1], realPos, self.tgtSelectedPos[0], self.tgtSelectedPos[1], tgtRealPos, keepLv)

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

    def enhanceTransferSuccess(self):
        self.refreshLeftList()
        if self.panelMc:
            info = {}
            tgtItem = self.getEnhanceItem(1)
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
            self.panelMc.Invoke('transferSuccess', uiUtils.dict2GfxDict(info, True))
