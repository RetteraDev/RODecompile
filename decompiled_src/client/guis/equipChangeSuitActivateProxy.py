#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeSuitActivateProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import const
from item import Item
from uiProxy import UIProxy
from guis import ui
from ui import unicode2gbk
import gametypes
import commcalc
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from cdata import equip_suits_data as ESD
from cdata import equip_suit_show_data as ESSD
from cdata import equip_suit_activation_data as ESAD
from callbackHelper import Functor
EQUIPSUIT_ICON_PATH = 'equipSuit/'

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


def sort_Equip(a, b):
    if not a['suitName'] and b['suitName']:
        return -1
    if a['suitName'] and not b['suitName']:
        return 1
    if a['sortIdx'] < b['sortIdx']:
        return -1
    if a['sortIdx'] > b['sortIdx']:
        return 1
    return 0


class EquipChangeSuitActivateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeSuitActivateProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getDetailInfo': self.onGetDetailInfo,
         'removeItem': self.onRemoveItem,
         'confirm': self.onConfirm,
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

    def getSuitIdAndName(self, item):
        mySuitId = getattr(item, 'suitId', None)
        suitName = ''
        if mySuitId:
            mySuitId = getattr(item, 'suitId')
            suitName = self.getSuitNameBySuitId(mySuitId)
            if self.isActivate(mySuitId):
                suitName = "<font color=\'#7acc29\'>" + suitName + '</font>'
        return (mySuitId, suitName)

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
                    if not self.canSuit(item):
                        continue
                    mySuitId, suitName = self.getSuitIdAndName(item)
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                    itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                    itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                    itemInfo['pos'] = [const.RES_KIND_EQUIP, 0, i]
                    itemInfo['suitName'] = suitName
                    itemInfo['suitId'] = mySuitId
                    equipList.append(itemInfo)

                equipList.sort(cmp=sort_Equip)
            info['equipList'] = equipList
            if bInit and selBtnType == -1 and not seluuid:
                for itemInfo in equipList:
                    _suitId = itemInfo.get('suitId', None)
                    if not _suitId:
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
                    if not self.canSuit(item):
                        continue
                    mySuitId, suitName = self.getSuitIdAndName(item)
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                    itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                    itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                    itemInfo['pos'] = [const.RES_KIND_SUB_EQUIP_BAG, 0, pos]
                    itemInfo['suitName'] = suitName
                    itemInfo['suitId'] = mySuitId
                    subEquipList.append(itemInfo)

                subEquipList.sort(cmp=sort_Equip)
            info['subEquipList'] = subEquipList
            if bInit and selBtnType == -1 and not seluuid:
                for itemInfo in subEquipList:
                    _suitId = itemInfo.get('suitId', None)
                    if not _suitId:
                        selBtnType = const.RES_KIND_EQUIP
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
                        if not self.canSuit(item):
                            continue
                        mySuitId, suitName = self.getSuitIdAndName(item)
                        itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                        itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                        itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                        itemInfo['quality'] = getattr(item, 'quality', 0)
                        itemInfo['score'] = getattr(item, 'score', 0)
                        itemInfo['pos'] = [const.RES_KIND_INV, pg, ps]
                        itemInfo['suitName'] = suitName
                        itemInfo['suitId'] = mySuitId
                        unEquipList.append(itemInfo)

                unEquipList.sort(cmp=sort_unEquip)
            info['unEquipList'] = unEquipList
            if bInit and selBtnType == -1 and not seluuid:
                for itemInfo in unEquipList:
                    _suitId = itemInfo.get('suitId', None)
                    if not _suitId:
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

    def canSuit(self, item):
        if not item.isEquip():
            return False
        if item.isYaoPei():
            return False
        if item.isWingOrRide():
            return False
        suitDatas = ESAD.data.get(item.id, [])
        if not suitDatas:
            return False
        fitSchool = False
        for data in suitDatas:
            schoolShowLimit = data.get('schoolShowLimit', ())
            if BigWorld.player().school in schoolShowLimit:
                fitSchool = True

        if not fitSchool:
            return False
        schReq = ID.data.get(item.id, {}).get('schReq', ())
        if schReq and BigWorld.player().school not in schReq:
            return False
        return True

    def getSuitItem(self):
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
            item = self.getSuitItem()
            if item:
                targetItemInfo = {}
                if self.selectedPos and self.selectedPos[0] in (const.RES_KIND_EQUIP, const.RES_KIND_SUB_EQUIP_BAG):
                    targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
                    targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                info['targetItemInfo'] = targetItemInfo
                info['suitTypeInfo'] = self.getSuitTypeInfo(item)
                info['isEmpty'] = False
            else:
                info['isEmpty'] = True
            self.panelMc.Invoke('refreshDetailInfo', uiUtils.dict2GfxDict(info, True))

    def onRemoveItem(self, *arg):
        self.selectedPos = None
        self.refreshDetailInfo()

    def onConfirm(self, *arg):
        _index = int(arg[3][0].GetNumber())
        _suitId = int(arg[3][1].GetNumber())
        _uuid = unicode2gbk(arg[3][2].GetString())
        self.onActivateSuit(_index, _suitId, _uuid)

    def getSuitTypeInfo(self, it):
        ret = []
        data = ESAD.data.get(it.id, [])
        for suitIndex, item in enumerate(data):
            suitId = item.get('suitId')
            schoolShowLimit = item.get('schoolShowLimit', ())
            if BigWorld.player().school not in schoolShowLimit:
                continue
            suitData = ESD.data.get(suitId, {})
            suitName = ESSD.data.get(suitId, {}).get('name', '')
            suitType = ESSD.data.get(suitId, {}).get('type', 1)
            suitTypeName = ESSD.data.get(suitId, {}).get('typeName', '')
            ret.append((suitIndex,
             suitId,
             suitName,
             suitType,
             suitTypeName))

        return ret

    def getSuitCostInfo(self, index, suitId, activateItemId):
        ret = {}
        p = BigWorld.player()
        suitActiveData = ESAD.data
        data = suitActiveData.get(activateItemId, [])[index]
        itemNum = 1
        itemId = data.get('itemId')
        cashNum = data.get('cash', 0)
        it = Item(itemId)
        needCount = itemNum
        ownCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
        countStr = uiUtils.convertNumStr(ownCount, needCount)
        costInfo = uiUtils.getGfxItem(it, appendInfo={'count': countStr,
         'itemId': itemId})
        ret['costItem'] = costInfo
        ret['isItemEnough'] = not ownCount < needCount
        ret['costCash'] = uiUtils.convertNumStr(p.cash, cashNum, False)
        ret['ownCash'] = p.cash
        return ret

    def onSelectSuit(self, *args):
        self.currentIndex = int(args[3][0].GetNumber())
        self.currentSuitId = int(args[3][1].GetNumber())
        self.showEquipDetail(self.currentIndex, self.currentSuitId)

    def getSuitPreviewInfo(self, mySuitId):
        suitDict = {}
        suitName = ''
        suitGetSkill = ''
        suitNotGetSkill = ''
        suitList = []
        suitData = ESD.data.get(mySuitId, {})
        suitShowData = ESSD.data.get(mySuitId, {})
        if len(suitData.items()) <= 0:
            return suitDict
        suits = suitShowData.get('posName', [])
        if len(suits) <= 0:
            return suitDict
        suitName = suitData.items()[0][1].get('name', '')
        p = BigWorld.player()
        if p:
            suitMaxNum = len(suits)
            suitCurNum = p.suitsCache.get(mySuitId, 0)
            selItem = self.getSuitItem()
            bAdd = False
            for suit in suits:
                if len(suit) == 2:
                    part = gametypes.EQUIP_SUIT_PART.get(suit[0], 0)
                    equip = p.equipment.get(part)
                    if equip:
                        selItemSuitId = getattr(selItem, 'suitId')
                        equipSuitId = getattr(equip, 'suitId')
                        if equipSuitId == mySuitId or not bAdd and selItem.whereEquip()[0] == part:
                            suitList.append((1, suit[1]))
                        else:
                            suitList.append((0, suit[1]))
                        if not bAdd and suitCurNum < suitMaxNum and selItem.whereEquip()[0] == part and equipSuitId != mySuitId:
                            suitCurNum = suitCurNum + 1
                            bAdd = True
                    elif not bAdd and selItem.whereEquip()[0] == part:
                        suitList.append((1, suit[1]))
                        if suitCurNum < suitMaxNum:
                            suitCurNum = suitCurNum + 1
                            bAdd = True
                    else:
                        suitList.append((0, suit[1]))

            suitName = gameStrings.TEXT_EQUIPCHANGESUITACTIVATEPROXY_372 % (suitName, suitCurNum, suitMaxNum)
            suitData = sorted(suitData.iteritems(), key=lambda x: x[0])
            for item in suitData:
                if item[0] == 'suits':
                    continue
                desc = '[%s]%s<br>' % (str(item[0]), item[1].get('desc', ''))
                if item[0] <= suitCurNum:
                    suitGetSkill += uiUtils.toHtml(desc, '#73E539')
                else:
                    suitNotGetSkill += uiUtils.toHtml(desc, '#808080')

        suitDict = {'suitName': suitName,
         'suitList': suitList,
         'suitGetSkill': suitGetSkill,
         'suitNotGetSkill': suitNotGetSkill}
        return suitDict

    def isActivate(self, mySuitId):
        p = BigWorld.player()
        if p:
            suitCurNum = p.suitsCache.get(mySuitId, 0)
        suitData = ESD.data.get(mySuitId, {})
        suitData = sorted(suitData.iteritems(), key=lambda x: x[0])
        for item in suitData:
            if item[0] == 'suits':
                continue
            if item[0] <= suitCurNum:
                return True

        return False

    def onGetSelectedInfo(self, *args):
        _index = int(args[3][0].GetNumber())
        _suitId = int(args[3][1].GetNumber())
        _uuid = unicode2gbk(args[3][2].GetString())
        it = self.getSuitItem()
        if not it:
            return
        ret = {}
        ret['previewInfo'] = self.getSuitPreviewInfo(_suitId)
        ret['costInfo'] = self.getSuitCostInfo(_index, _suitId, it.id)
        return uiUtils.dict2GfxDict(ret, True)

    def onOpenHelp(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        if gameglobal.rds.configData.get('enableNewItemSearch', False):
            self.uiAdapter.itemSourceInfor.openPanel()
        else:
            self.uiAdapter.help.showByItemId(itemId)

    def onActivateSuit(self, index, suitId, uuid):
        if not uuid:
            return
        p = BigWorld.player()
        item = self.getSuitItem()
        if not item:
            return
        if item.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        consumeItemId = ESAD.data.get(item.id, [])[index].get('itemId')
        bindCount = p.inv.countItemBind(consumeItemId, enableParentCheck=True)
        if not item.isForeverBind() and bindCount:
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ACTIVE_BIND, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.activiateSuit, suitId))
        else:
            self.activiateSuit(suitId)

    def activiateSuit(self, suitId):
        p = BigWorld.player()
        it = self.getSuitItem()
        if it:
            ownSuitId = getattr(it, 'suitId', None)
            if ownSuitId and ownSuitId != suitId:
                msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_ALREADY_ACTIVE, gameStrings.TEXT_EQUIPCHANGESUITACTIVATEPROXY_453)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onRealActivate, suitId))
            elif ownSuitId and ownSuitId == suitId:
                msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_SAME_SUITACTIVE, gameStrings.TEXT_EQUIPCHANGESUITACTIVATEPROXY_456)
                p.showTopMsg(msg)
            else:
                self.cellActiveSuit(suitId, it)

    def onRealActivate(self, suitId):
        p = BigWorld.player()
        it = self.getSuitItem()
        if it:
            self.cellActiveSuit(suitId, it)

    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.EQIP_SUIT_ACTIVATE)
    def cellActiveSuit(self, suitId, it):
        p = BigWorld.player()
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        p.cell.addSuitEffectToItemNew(self.selectedPos[0], self.selectedPos[1], realPos, suitId)

    def onActivateSuccess(self):
        if self.panelMc:
            BigWorld.callback(0.2, self.refreshLeftList)
            BigWorld.callback(0.2, self.refreshDetailInfo)
            self.panelMc.Invoke('playSuccessEffect')

    def getSuitNameBySuitId(self, mySuitId):
        suitName = ''
        suitData = ESD.data.get(mySuitId, {})
        suitShowData = ESSD.data.get(mySuitId, {})
        if len(suitData.items()) <= 0:
            return ''
        suits = suitShowData.get('posName', [])
        if len(suits) <= 0:
            return ''
        suitName = suitData.items()[0][1].get('name', '')
        p = BigWorld.player()
        if p:
            suitMaxNum = len(suits)
            suitCurNum = p.suitsCache.get(mySuitId, 0)
            suitName = gameStrings.TEXT_EQUIPCHANGESUITACTIVATEPROXY_372 % (suitName, suitCurNum, suitMaxNum)
        return suitName
