#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangePrefixRebuildProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import const
import ui
import copy
import uiConst
import gametypes
import commcalc
from uiProxy import UIProxy
from callbackHelper import Functor
from data import equip_synthesize_data as ESD
from data import equip_prefix_prop_data as EPPD
from cdata import item_synthesize_set_data as ISSD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

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


class EquipChangePrefixRebuildProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangePrefixRebuildProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getDetailInfo': self.onGetDetailInfo,
         'getConsumeInfo': self.onGetConsumeInfo,
         'changeMethod': self.onChangeMethod,
         'removeItem': self.onRemoveItem,
         'confirm': self.onConfirm,
         'useOld': self.onUseOld,
         'useNew': self.onUseNew,
         'showHelp': self.onShowHelp}
        self.panelMc = None
        self.selectedPos = None
        self.methodTabIdx = 0
        self.methodIdx = 0
        self.prefixRebuildMap = {}

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.initData()
        self.refreshLeftList()

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.selectedPos = None
        self.methodTabIdx = 0
        self.methodIdx = 0

    def initData(self):
        if self.prefixRebuildMap != {}:
            return
        for key, value in ESD.data.iteritems():
            if value.get('type', 0) != uiConst.FORMULA_TYPE_PREFIX_WASH:
                continue
            itemId, methodIdx = key
            if itemId not in self.prefixRebuildMap:
                self.prefixRebuildMap[itemId] = set()
            self.prefixRebuildMap[itemId].add(methodIdx)

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
                    if not self.canPrefixRebuild(item):
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
                    if not self.canPrefixRebuild(item):
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
                        if not self.canPrefixRebuild(item):
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

    def canPrefixRebuild(self, item):
        if not item.isEquip():
            return False
        if item.isYaoPei():
            return False
        if item.id not in self.prefixRebuildMap:
            return False
        return True

    def getRebuildItem(self):
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

    def getNewPrepfixItem(self, curItem):
        newItem = None
        newPrefixInfo = getattr(curItem, 'newPrefixInfo', ())
        if len(newPrefixInfo) > 0:
            preGroupId, prefixId, _ = newPrefixInfo
            newItem = copy.deepcopy(curItem)
            newItem.removePrefixProps()
            newItem.preprops = []
            newItem.prefixInfo = (preGroupId, prefixId)
            prefixData = EPPD.data.get(preGroupId, {})
            for pd in prefixData:
                if pd.get('id', 0) == prefixId:
                    props = pd.get('props', [])
                    for pid, pType, pVal in props:
                        newItem.preprops.append((pid, pType, pVal))

                    break

        return newItem

    def refreshDetailInfo(self, playEffect = False):
        if self.panelMc:
            info = {}
            item = self.getRebuildItem()
            if item:
                targetItemInfo = {}
                if self.selectedPos and self.selectedPos[0] in (const.RES_KIND_EQUIP, const.RES_KIND_SUB_EQUIP_BAG):
                    targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
                    targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                info['targetItemInfo'] = targetItemInfo
                prefixProp = uiUtils.getItemPreprops(item)
                if prefixProp != '':
                    prefixTitle = uiUtils.getItemPreName(item)
                    prefixPropList = prefixProp.split('<br>')
                else:
                    prefixTitle = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                    prefixPropList = []
                info['prefixTitle'] = prefixTitle
                info['prefixPropList'] = prefixPropList
                newItem = self.getNewPrepfixItem(curItem=item)
                if newItem:
                    newPrefixProp = uiUtils.getItemPreprops(newItem)
                    if newPrefixProp != '':
                        newPrefixTitle = uiUtils.getItemPreName(newItem)
                        newPrefixPropList = newPrefixProp.split('<br>')
                    else:
                        newPrefixTitle = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                        newPrefixPropList = []
                    info['newPrefixTitle'] = newPrefixTitle
                    info['newPrefixPropList'] = newPrefixPropList
                    info['hasNewPrefix'] = True
                else:
                    info['hasNewPrefix'] = False
                    info['newPrefixTitle'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                info['playEffect'] = playEffect
                methodSet = self.prefixRebuildMap.get(item.id, set())
                info['methodLen'] = len(methodSet)
                info['isEmpty'] = False
            else:
                info['isEmpty'] = True
            self.panelMc.Invoke('refreshDetailInfo', uiUtils.dict2GfxDict(info, True))

    def onGetConsumeInfo(self, *arg):
        self.refreshConsumeInfo()

    def onChangeMethod(self, *arg):
        methodTabIdx = int(arg[3][0].GetNumber())
        self.methodTabIdx = methodTabIdx
        self.refreshConsumeInfo()

    def refreshConsumeInfo(self):
        if self.panelMc:
            p = BigWorld.player()
            info = {}
            item = self.getRebuildItem()
            if not item:
                return
            methodList = list(self.prefixRebuildMap.get(item.id, set()))
            methodList.sort()
            if len(methodList) <= 0:
                return
            if len(methodList) <= self.methodTabIdx:
                self.methodTabIdx = 0
            self.methodIdx = methodList[self.methodTabIdx]
            esd = ESD.data.get((item.id, self.methodIdx), {})
            if not esd:
                return
            info['methodTabIdx'] = self.methodTabIdx
            btnEnabled = True
            materialSetNeed = esd.get('materialSetNeed', 0)
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
            needCash = esd.get('cashNeed', 0)
            ownCash = p.cash + p.bindCash
            info['cashStr'] = uiUtils.convertNumStr(ownCash, needCash, showOwnStr=False, needThousand=True)
            needExpXiuwei = esd.get('expNeed', 0)
            ownExpXiuwei = p.expXiuWei
            if needExpXiuwei <= 0:
                info['expStr'] = ''
            else:
                info['expStr'] = uiUtils.convertNumStr(ownExpXiuwei, needExpXiuwei, showOwnStr=False, needThousand=True)
            if ownCash < needCash:
                btnEnabled = False
            info['btnEnabled'] = btnEnabled
            self.panelMc.Invoke('refreshConsumeInfo', uiUtils.dict2GfxDict(info, True))

    def onRemoveItem(self, *arg):
        self.selectedPos = None
        self.refreshDetailInfo()

    def onConfirm(self, *arg):
        p = BigWorld.player()
        item = self.getRebuildItem()
        if not item:
            return
        if item.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        esd = ESD.data.get((item.id, self.methodIdx), {})
        if not esd:
            return
        if uiUtils.checkBindCashEnough(esd.get('cashNeed', 0), p.bindCash, p.cash, Functor(self.trueConfirmStep1, item)):
            self.trueConfirmStep1(item)

    @ui.checkEquipCanReturn(const.LAST_PARAMS, GMDD.data.RETURN_BACK_EQUIP_WASH)
    @ui.looseGroupTradeConfirm(const.LAST_PARAMS, GMDD.data.RETURN_BACK_EQUIP_WASH)
    def trueConfirmStep1(self, item):
        p = BigWorld.player()
        esd = ESD.data.get((item.id, self.methodIdx), {})
        if not esd:
            return
        newItem = self.getNewPrepfixItem(item)

        def selectOldPrefixAndConfirm():
            gameglobal.rds.ui.equipChangePrefixRebuild.selectPrefix(False)
            gameglobal.rds.ui.equipChangePrefixRebuild.trueConfirm()

        if newItem and newItem.getPrefixScore() > item.getPrefixScore():
            msg = uiUtils.getTextFromGMD(GMDD.data.PREFIX_REBUILD_BETTER_NEW_PREFIX_SCORE_HINT, '')
            confirmFunc = Functor(gameglobal.rds.ui.messageBox.showYesNoMsgBox, msg, selectOldPrefixAndConfirm)
        else:
            confirmFunc = selectOldPrefixAndConfirm
        if not item.isForeverBind():
            materialSetNeed = esd.get('materialSetNeed', 0)
            issd = ISSD.data.get(materialSetNeed, [])
            hasBindMaterial = False
            for issdData in issd:
                itemId = issdData.get('itemId', 0)
                if itemId == 0:
                    continue
                enableParentCheck = True if issdData.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT) == gametypes.ITEM_MIX_TYPE_PARENT else False
                ownBindNum = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY, enableParentCheck=enableParentCheck)
                if ownBindNum > 0:
                    hasBindMaterial = True
                    break

            if hasBindMaterial:
                msg = uiUtils.getTextFromGMD(GMDD.data.PREFIX_REBUILD_BIND_HINT, '')
                confirmFunc = Functor(gameglobal.rds.ui.messageBox.showYesNoMsgBox, msg, confirmFunc)
        needExpXiuwei = esd.get('expNeed', 0)
        if needExpXiuwei > 0 and p.expXiuWei < needExpXiuwei:
            if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_EQUIP_CHANGE_PREFIX_REBUILD):
                msg = GMD.data.get(GMDD.data.ENHANCE_SKILL_CONSUME_EXP_NOTIFY, {}).get('text', '')

                def tempShowBoxFunc(msg, confirmFunc, isShowCheckBox, checkOnceType):
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=confirmFunc, isShowCheckBox=isShowCheckBox, checkOnceType=checkOnceType)

                confirmFunc = Functor(tempShowBoxFunc, msg, confirmFunc, True, uiConst.CHECK_ONCE_TYPE_EQUIP_CHANGE_PREFIX_REBUILD)
        confirmFunc()

    def trueConfirm(self):
        item = self.getRebuildItem()
        if not item:
            return
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        BigWorld.player().cell.resetEquipPrefixNew(self.selectedPos[0], self.selectedPos[1], realPos, item.id, self.methodIdx)

    def onUseOld(self, *arg):
        item = self.getRebuildItem()
        if not item:
            return
        if item.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.NEW_PREP_PROPS_MISS_CONFIRM, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.selectPrefix, False))

    def onUseNew(self, *arg):
        item = self.getRebuildItem()
        if not item:
            return
        if item.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.OLD_PREP_PROPS_MISS_CONFIRM, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.selectPrefix, True))

    def selectPrefix(self, isNew):
        item = self.getRebuildItem()
        if not item:
            return
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        BigWorld.player().cell.confirmResetEquipPrefixNew(self.selectedPos[0], self.selectedPos[1], realPos, isNew)

    def onShowHelp(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        if gameglobal.rds.configData.get('enableNewItemSearch', False):
            self.uiAdapter.itemSourceInfor.openPanel()
        else:
            self.uiAdapter.help.showByItemId(itemId)

    def prefixRebuildResult(self, resKind, page, pos):
        if self.selectedPos and self.selectedPos[0] == resKind and self.selectedPos[1] == page and self.selectedPos[2] == pos:
            self.refreshDetailInfo()

    def prefixRebuildFinish(self, resKind, page, pos, ok):
        self.refreshLeftList(resKind)
        if self.selectedPos and self.selectedPos[0] == resKind and self.selectedPos[1] == page and self.selectedPos[2] == pos:
            self.refreshDetailInfo(ok)
