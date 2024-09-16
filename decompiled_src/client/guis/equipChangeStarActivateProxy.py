#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeStarActivateProxy.o
from gamestrings import gameStrings
import BigWorld
import gamelog
import gameglobal
import uiUtils
import const
import utils
from item import Item
from uiProxy import UIProxy
from guis import ui
import gametypes
import commcalc
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from cdata import equip_active_star_cost_data as EASCD
from cdata import font_config_data as FCD
from data import item_data as ID

def sort_unEquip(a, b):
    if a['inactiveStarLv'] > 0 and b['inactiveStarLv'] <= 0:
        return -1
    if a['inactiveStarLv'] <= 0 and b['inactiveStarLv'] > 0:
        return 1
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


def sort_Equip(a, b):
    if a['inactiveStarLv'] > 0 and b['inactiveStarLv'] <= 0:
        return -1
    if a['inactiveStarLv'] <= 0 and b['inactiveStarLv'] > 0:
        return 1
    if a['sortIdx'] < b['sortIdx']:
        return -1
    if a['sortIdx'] > b['sortIdx']:
        return 1
    return 0


class EquipChangeStarActivateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeStarActivateProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getDetailInfo': self.onGetDetailInfo,
         'removeItem': self.onRemoveItem,
         'confirm': self.onConfirm,
         'clickCoinBtn': self.onClickCoinBtn,
         'clickYunChuiBtn': self.onClickYunChuiBtn,
         'setDiKouFlag': self.onSetDiKouFlag,
         'getSelectedInfo': self.onGetSelectedInfo,
         'openHelp': self.onOpenHelp}
        self.panelMc = None
        self.selectedPos = None

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.refreshLeftList(bInit=True)

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.selectedPos = None

    def refreshLeftList(self, refreshKind = -1, bInit = False):
        if self.panelMc:
            p = BigWorld.player()
            info = {}
            refreshAll = refreshKind == -1
            selInfo = {}
            selBtnType = -1
            seluuid = ''
            selPos = []
            equipList = []
            if refreshAll or refreshKind == const.RES_KIND_EQUIP:
                for i, item in enumerate(p.equipment):
                    if not item:
                        continue
                    if not self.canStar(item):
                        continue
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                    itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                    itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                    itemInfo['pos'] = [const.RES_KIND_EQUIP, 0, i]
                    itemInfo['inactiveStarLv'] = getattr(item, 'inactiveStarLv', 0)
                    equipList.append(itemInfo)

                equipList.sort(cmp=sort_Equip)
            info['equipList'] = equipList
            if bInit and selBtnType == -1 and not seluuid:
                for itemInfo in equipList:
                    if itemInfo:
                        selBtnType = const.RES_KIND_EQUIP
                        seluuid = itemInfo.get('uuid', None)
                        selPos = itemInfo.get('pos', None)
                        break

            subEquipList = []
            if refreshAll or refreshKind == const.RES_KIND_SUB_EQUIP_BAG:
                for pos in gametypes.EQU_PART_SUB:
                    item = commcalc.getAlternativeEquip(p, pos)
                    if not item:
                        continue
                    if not self.canStar(item):
                        continue
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                    itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                    itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                    itemInfo['pos'] = [const.RES_KIND_SUB_EQUIP_BAG, 0, pos]
                    itemInfo['inactiveStarLv'] = getattr(item, 'inactiveStarLv', 0)
                    subEquipList.append(itemInfo)

                subEquipList.sort(cmp=sort_Equip)
            info['subEquipList'] = subEquipList
            if bInit and selBtnType == -1 and not seluuid:
                for itemInfo in subEquipList:
                    if itemInfo:
                        selBtnType = const.RES_KIND_SUB_EQUIP_BAG
                        seluuid = itemInfo.get('uuid', None)
                        selPos = itemInfo.get('pos', None)
                        break

            unEquipList = []
            if refreshAll or refreshKind == const.RES_KIND_INV:
                for pg in p.inv.getPageTuple():
                    for ps in p.inv.getPosTuple(pg):
                        item = p.inv.getQuickVal(pg, ps)
                        if item == const.CONT_EMPTY_VAL:
                            continue
                        if not self.canStar(item):
                            continue
                        itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                        itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                        itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                        itemInfo['quality'] = getattr(item, 'quality', 0)
                        itemInfo['score'] = getattr(item, 'score', 0)
                        itemInfo['pos'] = [const.RES_KIND_INV, pg, ps]
                        itemInfo['inactiveStarLv'] = getattr(item, 'inactiveStarLv', 0)
                        unEquipList.append(itemInfo)

                unEquipList.sort(cmp=sort_unEquip)
            info['unEquipList'] = unEquipList
            if bInit and selBtnType == -1 and not seluuid:
                for itemInfo in unEquipList:
                    if itemInfo:
                        selBtnType = const.RES_KIND_INV
                        seluuid = itemInfo.get('uuid', None)
                        selPos = itemInfo.get('pos', None)
                        break

            info['refreshAll'] = refreshAll
            info['refreshKind'] = refreshKind
            selInfo['selBtnType'] = selBtnType
            selInfo['seluuid'] = seluuid
            selInfo['selPos'] = selPos
            info['selInfo'] = selInfo
            info['bInit'] = bInit
            self.panelMc.Invoke('refreshLeftList', uiUtils.dict2GfxDict(info, True))

    def canStar(self, item):
        if not item.isEquip():
            return False
        if item.isYaoPei():
            return False
        if item.isWingOrRide():
            return False
        if item.isFashionEquip():
            return False
        if item.isGuanYin():
            return False
        if not getattr(item, 'inactiveStarLv', 0):
            return False
        return True

    def getStarItem(self):
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

    def refreshDetailInfo(self):
        if self.panelMc:
            info = {}
            item = self.getStarItem()
            if item:
                targetItemInfo = {}
                if self.selectedPos and self.selectedPos[0] in (const.RES_KIND_EQUIP, const.RES_KIND_SUB_EQUIP_BAG):
                    targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
                    targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                info['targetItemInfo'] = targetItemInfo
                info['isEmpty'] = False
            else:
                info['isEmpty'] = True
            self.panelMc.Invoke('refreshDetailInfo', uiUtils.dict2GfxDict(info, True))

    def onRemoveItem(self, *arg):
        self.selectedPos = None
        self.refreshDetailInfo()

    def onConfirm(self, *arg):
        gamelog.debug('@zq onConfirm')
        equip = self.getStarItem()
        self.onTrueActiveStarLv(equip)

    def onClickYunChuiBtn(self, *arg):
        mall = self.uiAdapter.tianyuMall
        if mall.mallMediator:
            mall.hide()
        mall.show(keyWord=gameStrings.TEXT_INVENTORYPROXY_3299)

    def onClickCoinBtn(self, *arg):
        BigWorld.player().openRechargeFunc()

    def onGetSelectedInfo(self, *arg):
        ret = {}
        it = self.getStarItem()
        self.appendStarCostInfo(ret, it)
        self.appendEquipStarInfo(ret, it)
        gamelog.debug('@zq ret', ret)
        return uiUtils.dict2GfxDict(ret, True)

    def appendStarCostInfo(self, srcInfo, it):
        ret = {}
        p = BigWorld.player()
        starCostData = EASCD.data.get((it.quality, it.order), None)
        if starCostData is None:
            return
        else:
            itemId, costFormula, cashFormula = starCostData['itemId'], starCostData['itemNum'], starCostData['cash']
            itemNum = it.evalValue(costFormula[0], costFormula[1:])
            cashNum = it.evalValue(cashFormula[0], cashFormula[1:])
            expNum = it._getEquipStarUpExp()
            it = Item(itemId)
            ret['costItem'] = self.basicItemInfo(it)
            ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
            ret['materialNum'] = uiUtils.convertNumStr(ownNum, itemNum)
            ret['costItem']['count'] = ret['materialNum']
            enableEquipDiKou = gameglobal.rds.configData.get('enableEquipDiKou', False)
            itemDict = {}
            if self.uiAdapter.equipChange.useDiKou:
                itemDict = {itemId: itemNum}
                btnEnabled = uiUtils.checkEquipMaterialDiKou(itemDict)
            else:
                itemDict = {}
                btnEnabled = ownNum >= itemNum
            ret['useDiKou'] = self.uiAdapter.equipChange.useDiKou
            ret['diKouInfo'] = uiUtils.getEquipMaterialDiKouInfo(itemDict)
            costItemEnough = True
            if enableEquipDiKou:
                itemDict = {itemId: itemNum}
                self.appendDiKouInfo(ret, itemDict)
                if not uiUtils.checkEquipMaterialDiKou(itemDict):
                    costItemEnough = False
            elif itemNum > ownNum:
                costItemEnough = False
            if p.cash < cashNum:
                btnEnabled = False
            ret['btnEnabled'] = btnEnabled
            ret['costItemEnough'] = costItemEnough
            ret['needCostItem'] = itemNum > 0
            ret['costCash'] = uiUtils.convertNumStr(p.cash, cashNum, False)
            ret['ownCash'] = p.cash
            ret['costExp'] = expNum
            srcInfo['costInfo'] = ret
            return

    def basicItemInfo(self, it, withId = True):
        ret = {}
        itemId = it.id
        itemInfo = ID.data.get(itemId, {})
        if hasattr(it, 'quality'):
            quality = it.quality
        else:
            quality = itemInfo.get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
        icon = uiUtils.getItemIconFile64(itemId)
        name = itemInfo.get('name', gameStrings.TEXT_TIANYUMALLPROXY_1455)
        mwrap = itemInfo.get('mwrap', 1)
        if withId:
            ret['itemId'] = itemId
        ret['name'] = name
        ret['color'] = color
        ret['iconPath'] = icon
        ret['mwrap'] = mwrap
        return ret

    def appendDiKouInfo(self, ret, itemDict):
        if itemDict != {}:
            p = BigWorld.player()
            _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
            yunchuiOwn = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
            if yunchuiNeed > yunchuiOwn:
                ret['yunchui'] = '%s/%s' % (uiUtils.toHtml(format(yunchuiOwn, ','), '#FB0000'), format(yunchuiNeed, ','))
                ret['yunchuiEnabled'] = True
            else:
                ret['yunchui'] = '%s/%s' % (format(yunchuiOwn, ','), format(yunchuiNeed, ','))
                ret['yunchuiEnabled'] = False
            ret['diKouVisible'] = True
        else:
            ret['diKouVisible'] = False

    def onOpenHelp(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        if gameglobal.rds.configData.get('enableNewItemSearch', False):
            self.uiAdapter.itemSourceInfor.openPanel()
        else:
            self.uiAdapter.help.showByItemId(itemId)

    def onSetDiKouFlag(self, *arg):
        self.uiAdapter.equipChange.useDiKou = arg[3][0].GetBool()
        self.refreshConsumeInfo()

    def refreshConsumeInfo(self):
        ret = {}
        it = self.getStarItem()
        self.appendStarCostInfo(ret, it)
        if self.panelMc:
            self.panelMc.Invoke('setMaterialInfo', uiUtils.dict2GfxDict(ret['costInfo'], True))

    def appendEquipStarInfo(self, ret, it):
        starInfo = {}
        if not hasattr(it, 'activeStarLv'):
            starInfo['activeStarLv'] = 0
            starInfo['inactiveStarLv'] = 0
            starInfo['starLv'] = 0
            starInfo['starExp'] = 0
            starInfo['seExtraStarLv'] = 0
        else:
            starInfo['activeStarLv'] = it.activeStarLv
            starInfo['inactiveStarLv'] = it.inactiveStarLv
            starInfo['starLv'] = it.starLv
            starInfo['starExp'] = it.starExp
            starInfo['seExtraStarLv'] = int(it.seExtraStarLv)
        starInfo['maxStarLv'] = getattr(it, 'maxStarLv', -1)
        ret['starInfo'] = starInfo

    def onActivateStar(self):
        self.onTrueActiveStarLv()

    @ui.checkEquipCanReturnByPos(const.LAST_PARAMS, GMDD.data.ACTIVE_STAR_LV)
    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.ACTIVE_STAR_LV)
    def onTrueActiveStarLv(self, equip):
        p = BigWorld.player()
        activeCostData = EASCD.data[equip.quality, equip.order]
        itemId, costFormula, cashFormula = activeCostData['itemId'], activeCostData['itemNum'], activeCostData['cash']
        itemNum = equip.evalValue(costFormula[0], costFormula[1:])
        remain, res = p.inv.cntItemWithPlans(itemId, itemNum, enableParentCheck=True)
        if gameglobal.rds.configData.get('enableEquipDiKou', False):
            itemDict = {itemId: itemNum}
            if not uiUtils.checkEquipMaterialDiKou(itemDict):
                p.showGameMsg(GMDD.data.EQUIP_STAR_LV_ACTIVE_ITEM_NOT_ENOUGH, ())
                return
            _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
            if yunchuiNeed > 0 and not equip.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.onActiveStarLvNew)
                return
        elif remain:
            p.showGameMsg(GMDD.data.EQUIP_STAR_LV_ACTIVE_ITEM_NOT_ENOUGH, ())
            return
        needBind = any([ p.inv.getQuickVal(pg, ps).isForeverBind() for pg, ps, _ in res ])
        if needBind and not equip.isForeverBind():
            msg = GMD.data.get(GMDD.data.ACTIVE_STAR_LV_BIND, {}).get('text', gameStrings.TEXT_EQUIPCHANGESTARACTIVATEPROXY_450)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.onActiveStarLvNew)
        else:
            self.onActiveStarLvNew()

    def onActivateSuccess(self):
        if self.panelMc:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.EQUIPCHANGE_ACTIVE_STAR_LV_SUCCESS, ())
            BigWorld.callback(0.2, self.refreshLeftList)
            BigWorld.callback(0.2, self.refreshDetailInfo)
            self.panelMc.Invoke('playSuccessEffect')
            gameglobal.rds.sound.playSound(3988)

    def onActiveStarLvNew(self):
        p = BigWorld.player()
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        p.cell.activeStarLvNew(self.selectedPos[0], self.selectedPos[1], realPos)
