#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeStarLvUpProxy.o
from gamestrings import gameStrings
import BigWorld
import gamelog
import gameglobal
import uiUtils
import const
import utils
import uiConst
from item import Item
from uiProxy import UIProxy
from guis import ui
import gametypes
import commcalc
from data import equip_data as ED
from cdata import game_msg_def_data as GMDD
from cdata import equip_lvup_star_cost_data as ELSCD
from cdata import font_config_data as FCD
from data import item_data as ID
from cdata import equip_star_factor_data as ESFCD
from cdata import equip_quality_factor_data as EQFD
from data import prop_ref_data as PRD

def float2Int(num):
    return int(num)


def roundAttr(num):
    return round(int(num * 10) / 10.0, 1)


def sort_unEquip(a, b):
    if a['canLvUp'] and not b['canLvUp']:
        return -1
    if not a['canLvUp'] and b['canLvUp']:
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
    if a['canLvUp'] and not b['canLvUp']:
        return -1
    if not a['canLvUp'] and b['canLvUp']:
        return 1
    if a['sortIdx'] < b['sortIdx']:
        return -1
    if a['sortIdx'] > b['sortIdx']:
        return 1
    return 0


class EquipChangeStarLvUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeStarLvUpProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getDetailInfo': self.onGetDetailInfo,
         'removeItem': self.onRemoveItem,
         'confirm': self.onConfirm,
         'getSelectedInfo': self.onGetSelectedInfo,
         'openHelp': self.onOpenHelp}
        self.panelMc = None
        self.selectedPos = None
        self.pushMsgData = None

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.refreshLeftList(bInit=True)

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.selectedPos = None
        self.pushMsgData = None

    def showStarLvUpByAutoPush(self):
        part = self.uiAdapter.pushMessage.getLastData(uiConst.MESSAGE_TYPE_EQUIP_STAR_LV_UP).get('data', 0)
        gamelog.debug('@zq showStarLvUpByAutoPush', part)
        self.pushMsgData = part
        self.uiAdapter.pushMessage.removeData(uiConst.MESSAGE_TYPE_EQUIP_STAR_LV_UP, {'data': part})
        self.uiAdapter.equipChange.show(uiConst.EQUIPCHANGE_TAB_STAR, 1)

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
                    itemInfo['canLvUp'] = self.isCanLvUp(item)
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
                    itemInfo['canLvUp'] = self.isCanLvUp(item)
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
                        itemInfo['canLvUp'] = self.isCanLvUp(item)
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

            if self.pushMsgData:
                item = p.equipment.get(self.pushMsgData)
                if item:
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                    itemInfo['pos'] = [const.RES_KIND_EQUIP, 0, self.pushMsgData]
                    if itemInfo:
                        selBtnType = const.RES_KIND_EQUIP
                        seluuid = itemInfo.get('uuid', None)
                        selPos = itemInfo.get('pos', None)
                        self.pushMsgData = None
            info['refreshAll'] = refreshAll
            info['refreshKind'] = refreshKind
            selInfo['selBtnType'] = selBtnType
            selInfo['seluuid'] = seluuid
            selInfo['selPos'] = selPos
            info['selInfo'] = selInfo
            info['bInit'] = bInit
            self.panelMc.Invoke('refreshLeftList', uiUtils.dict2GfxDict(info, True))

    def isCanLvUp(self, it):
        expNum = it._getEquipStarUpExp()
        if getattr(it, 'starLv', 0) < getattr(it, 'maxStarLv', -1) and getattr(it, 'starExp', -1) >= expNum:
            return True
        return False

    def canStar(self, item):
        if not item.isEquip():
            return False
        if item.isYaoPei():
            return False
        if item.isWingOrRide():
            return False
        if item.isFashionEquip():
            return False
        if not self.isCanLvUp(item):
            return False
        if item.isGuanYin():
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

    def onGetSelectedInfo(self, *arg):
        ret = {}
        it = self.getStarItem()
        self.appendEquipProps(ret, it)
        self.appendEquipStarInfo(ret, it)
        self.appendStarCostInfo(ret, it)
        return uiUtils.dict2GfxDict(ret, True)

    def appendEquipProps(self, ret, i):
        basic, rand, pre, extra = self.calAttrVal(i)
        props = []
        if ED.data[i.id]['equipType'] == 1:
            basicItem = []
            newBasic = []
            for item in basic:
                if item[0] == 118:
                    basicItem.append('basic')
                    basicItem.append(gameStrings.TEXT_EQUIPENHANCERESULTPROXY_157)
                    basicItem.append(str(item[2]) + '-')
                    basicItem.append(str(item[3]) + '-')
                elif item[0] == 119:
                    basicItem[2] += str(item[2])
                    basicItem[3] += str(item[3])
                else:
                    newBasic.append(item)

            if len(basicItem) > 1:
                props.append(basicItem)
            basic = newBasic
            basicItem = []
            newBasic = []
            for item in basic:
                if item[0] == 120:
                    basicItem.append('basic')
                    basicItem.append(gameStrings.TEXT_EQUIPCHANGESTARLVUPPROXY_324)
                    basicItem.append(str(item[2]) + '-')
                    basicItem.append(str(item[3]) + '-')
                elif item[0] == 121:
                    basicItem[2] += str(item[2])
                    basicItem[3] += str(item[3])
                else:
                    newBasic.append(item)

            if len(basicItem) > 1:
                props.append(basicItem)
            basic = newBasic
        for item in basic:
            basicItem = []
            info = PRD.data[item[0]]
            basicItem.append('basic')
            basicItem.append(info['name'])
            if info['showType'] == 0:
                basicItem.append(str(float2Int(item[2])))
                basicItem.append(str(float2Int(item[3])))
            elif info['showType'] == 2:
                basicItem.append(str(round(item[2], 1)))
                basicItem.append(str(round(item[3], 1)))
            else:
                basicItem.append(str(round(item[2] * 100, 1)) + '%')
                basicItem.append(str(round(item[3] * 100, 1)) + '%')
            props.append(basicItem)

        self._appendProps(props, pre, 'pre')
        self._appendProps(props, extra, 'extra')
        self._appendProps(props, rand, 'rand')
        ret['props'] = props

    def _calAttrVal(self, item, attrs, rank, bFloat, attrStr = ''):
        p = BigWorld.player()
        ret = []
        if hasattr(item, 'starLv'):
            starLv = item.addedStarLv
        else:
            starLv = 0
        nextStarLv = starLv + 1
        starFactor = ESFCD.data.get(starLv, {}).get('factor', 1.0)
        quality = getattr(item, 'quality', 1)
        if not quality:
            quality = 1
        qualityFactor = EQFD.data.get(quality, {}).get('factor', 1.0)
        nextStarFactor = ESFCD.data.get(nextStarLv, {}).get('factor', 1.0)
        for pid, pType, pVal in attrs:
            if pType == gametypes.DATA_TYPE_NUM and item._isIntPropRef(pid):
                if bFloat:
                    if attrStr == 'rprops':
                        valFactor = starFactor
                        nextValFactor = nextStarFactor
                        if gameglobal.rds.configData.get('enableNewLv89', False):
                            valFactor = starFactor + item.isSesMaker(p.gbId)
                            nextValFactor = nextStarFactor + item.isSesMaker(p.gbId)
                        ret.append((pid,
                         pType,
                         roundAttr(pVal * valFactor * qualityFactor),
                         roundAttr(pVal * nextValFactor * qualityFactor)))
                    else:
                        ret.append((pid,
                         pType,
                         pVal * starFactor * qualityFactor,
                         pVal * nextStarFactor * qualityFactor))
                else:
                    ret.append((pid,
                     pType,
                     float2Int(pVal * starFactor * qualityFactor),
                     float2Int(pVal * nextStarFactor * qualityFactor)))
            else:
                ret.append((pid,
                 pType,
                 pVal * starFactor * qualityFactor,
                 pVal * nextStarFactor * qualityFactor))

        if rank:
            ret = [ tuple(list(r) + [PRD.data[r[0]]['priorityLevel'], PRD.data[r[0]]['showColor']]) for r in ret ]
            ret.sort(key=lambda k: k[4])
        return ret

    def calAttrVal(self, item):
        basic = []
        rand = []
        pre = []
        extra = []
        if hasattr(item, 'props'):
            basic = self._calAttrVal(item, item.props, False, False, 'props')
        if hasattr(item, 'rprops'):
            rand = self._calAttrVal(item, item.rprops, True, True, 'rprops')
        if hasattr(item, 'preprops'):
            pre = self._calAttrVal(item, item.preprops, True, True, 'preprops')
        if hasattr(item, 'extraProps'):
            extra = self._calAttrVal(item, item.extraProps, True, True, 'extraProps')
        return (basic,
         rand,
         pre,
         extra)

    def _appendProps(self, props, data, type):
        for item in data:
            propItem = []
            info = PRD.data[item[0]]
            propItem.append(type)
            propItem.append(info['name'])
            if info['type'] == 2:
                propItem.append('+')
                propItem.append('+')
            elif info['type'] == 1:
                propItem.append('-')
                propItem.append('-')
            if info['showType'] == 0:
                propItem[2] += str(float2Int(item[2]))
                propItem[3] += str(float2Int(item[3]))
            elif info['showType'] == 2:
                propItem[2] += str(round(item[2], 1))
                propItem[3] += str(round(item[3], 1))
            else:
                propItem[2] += str(round(item[2] * 100, 1)) + '%'
                propItem[3] += str(round(item[3] * 100, 1)) + '%'
            props.append(propItem)

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

    def appendStarCostInfo(self, srcInfo, it):
        ret = {}
        p = BigWorld.player()
        starCostData = ELSCD.data.get((it.quality, it.starLv), None)
        if starCostData is None:
            return
        else:
            itemId, costFormula, cashFormula = starCostData['itemId'], starCostData['itemNum'], starCostData['cash']
            itemNum = it.evalValue(costFormula[0], costFormula[1:])
            cashNum = it.evalValue(cashFormula[0], cashFormula[1:])
            expNum = it._getEquipStarUpExp()
            nextExpNum = it._getEquipStarUpExpByStarLv(it.starLv + 1)
            it = Item(itemId)
            ret['costItem'] = self.basicItemInfo(it)
            ownNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
            ret['materialNum'] = uiUtils.convertNumStr(ownNum, itemNum)
            ret['costItem']['count'] = ret['materialNum']
            enableEquipDiKou = False
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
            ret['nextCostExp'] = nextExpNum
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

    @ui.checkEquipCanReturnByPos(const.LAST_PARAMS, GMDD.data.ACTIVE_STAR_LV_UP_INV)
    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.ACTIVE_STAR_LV_UP_INV)
    def onTrueStarLvUpInv(self, item):
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        BigWorld.player().cell.equipStarLvupNew(self.selectedPos[0], self.selectedPos[1], realPos)

    def onConfirm(self, *arg):
        it = self.getStarItem()
        self.onTrueStarLvUpInv(it)

    def onActivateSuccess(self):
        if self.panelMc:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.EQUIPCHANGE_STAR_LV_UP_SUCCESS, ())
            BigWorld.callback(0.2, self.refreshLeftList)
            BigWorld.callback(0.2, self.refreshDetailInfo)
            self.panelMc.Invoke('playSuccessEffect')
            gameglobal.rds.sound.playSound(3988)
