#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipChangeRefiningProxy.o
import BigWorld
import copy
import const
import commcalc
import gametypes
import itemToolTipUtils
from callbackHelper import Functor
from gamestrings import gameStrings
from item import Item
import uiConst
from guis import events
from guis import ui
import gamelog
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis import uiUtils
from uiProxy import UIProxy
from cdata import equip_special_props_data as ESPD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import manual_equip_props_data as MEPD
PREFIX_MAX_NUM = 4
MATERIAL_ITEM_MAX_NUM = 5
RAND_PROP_MAX_CNT = 3
SPECIAL_PROP_MAX_CNT = 2

class EquipChangeRefiningProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipChangeRefiningProxy, self).__init__(uiAdapter)
        self.widget = None
        self.showMessageBox = True
        self.reset()

    def reset(self):
        self.selectedUUID = ''
        self.selectedPos = [-1, -1, -1]
        self.leftListInfo = {}
        self.selectedMc = None
        self.resKind = -1
        self.oldPropCache = {}
        self.firstRefresh = True
        self.resetItem = None

    def registerPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def itemChange(self, kind, page, pos, randomIdx):
        if not self.widget:
            return
        item = self.getItem(kind, page, pos)
        (kind,
         page,
         pos,
         item)
        if item.uuid.encode('hex') == self.selectedUUID:
            _, oldSpecialProps = self.oldPropCache.get(self.selectedUUID, ([], []))
            newSpecialProps = self.getSpecialProps(item)
            showEffect = False
            if len(newSpecialProps) >= len(oldSpecialProps):
                for index, prop in enumerate(newSpecialProps):
                    if index >= len(oldSpecialProps) or prop != oldSpecialProps[index]:
                        showEffect = True
                        break

            self.refreshLeftList(self.resKind, False)
            self.refreshDetailInfo(showEffect, randomIdx)

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        scrollWndList = self.widget.scrollWndList
        scrollWndList.itemRenderer = 'EquipChangeBG_LeftItem'
        scrollWndList.itemHeight = 64
        scrollWndList.lableFunction = self.itemFunction
        equipBtn = self.widget.equipBtn
        equipBtn.groupName = 'leftTab'
        equipBtn.data = const.RES_KIND_EQUIP
        equipBtn.addEventListener(events.BUTTON_CLICK, self.handleClickLeftTab, False, 0, True)
        subEquipBtn = self.widget.subEquipBtn
        subEquipBtn.data = const.RES_KIND_SUB_EQUIP_BAG
        subEquipBtn.groupName = 'leftTab'
        subEquipBtn.addEventListener(events.BUTTON_CLICK, self.handleClickLeftTab, False, 0, True)
        unEquipBtn = self.widget.unEquipBtn
        unEquipBtn.data = const.RES_KIND_INV
        unEquipBtn.groupName = 'leftTab'
        unEquipBtn.addEventListener(events.BUTTON_CLICK, self.handleClickLeftTab, False, 0, True)
        effect = self.widget.effect
        effect.visible = False
        ASUtils.setHitTestDisable(effect, True)
        targetItem = self.widget.targetItem
        targetItem.clear()
        targetItem.showCloseBtn = False
        targetItem.closeBtn.visible = False
        detail = self.widget.detail
        detail.needCash.cashIcon.bonusType = 'bindCash'
        equipBtn.selected = True
        helpIcon = self.widget.helpIcon
        helpIcon.helpKey = SCD.data.get('equipChangeRefiningHelpKey')
        scrollWndList.dataArray = []
        scrollWndList.validateNow()
        self.widget.resetBtn.addEventListener(events.BUTTON_CLICK, self.handleResetBtnClick, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfrimBtnClick, False, 0, True)

    @ui.checkInventoryLock()
    def handleConfrimBtnClick(self, *args):
        if not self.widget:
            return
        info = self.getDetailInfo()
        p = BigWorld.player()
        isCashEnough = True
        isBindCashEnough = True
        if info['targetItemInfo']['isBind']:
            isCashEnough = info['costCache'] <= p.cash + p.bindCash
            isBindCashEnough = p.bindCash >= info['costCache']
        else:
            isCashEnough = info['costCache'] <= p.cash
        if not isCashEnough:
            p.showGameMsg(GMDD.data.EQUIP_CHANGE_REFINING_CASH_NOT_ENOUGH, ())
            return
        if not isBindCashEnough and not self.uiAdapter.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_EQUIP_REFINI, False):
            msg = GMD.data.get(GMDD.data.EQUIP_CHANGE_REFINING_USE_CASH, {}).get('text', 'GMDD.data.EQUIP_CHANGE_REFINING_USE_CASH')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.checkBindCash, info), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_EQUIP_REFINI)
            return
        if self.showMessageBox:
            self.showMessageBox = False
            msg = GMD.data.get(GMDD.data.EQUIP_CHANGE_REFINING_FIRST, {}).get('text', 'GMDD.data.EQUIP_CHANGE_REFINING_FIRST')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.checkCycleCnt, info, self.selectedPos[0], self.selectedPos[1], self.selectedPos[2]))
        else:
            self.checkCycleCnt(info, self.selectedPos[0], self.selectedPos[1], self.selectedPos[2])

    def checkBindCash(self, info):
        if self.showMessageBox:
            self.showMessageBox = False
            msg = GMD.data.get(GMDD.data.EQUIP_CHANGE_REFINING_FIRST, {}).get('text', 'GMDD.data.EQUIP_CHANGE_REFINING_FIRST')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.checkCycleCnt, info, self.selectedPos[0], self.selectedPos[1], self.selectedPos[2]))
        else:
            self.checkCycleCnt(info, self.selectedPos[0], self.selectedPos[1], self.selectedPos[2])

    def checkCycleCnt(self, info, resKind, page, pos):
        if info['checkCycleCnt']:
            msg = GMD.data.get(GMDD.data.EQUIP_CHANGE_REFINING_CYCLE_CNT, {}).get('text', 'GMDD.data.EQUIP_CHANGE_REFINING_CYCLE_CNT')
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.doRefining, resKind, page, pos))
        else:
            self.doRefining(resKind, page, pos)

    def doRefining(self, resKind, page, pos):
        gamelog.info('jbx:refineManualEquipment', resKind, page, pos)
        BigWorld.player().cell.refineManualEquipment(resKind, page, pos)

    def handleResetBtnClick(self, *args):
        msg = GMD.data.get(GMDD.data.EQUIP_CHANGE_REFINING_RESUME_CONFIRM, {}).get('text', 'GMDD.data.EQUIP_CHANGE_REFINING_RESUME_CONFIRM')
        item = copy.deepcopy(self.getRefiningItem())
        item.unrefineManualProperties()
        item.rarityMiracle = Item.EQUIP_NOT_DECIDED
        item.calcScores(calcRarityMiracle=True, extra={'owner': BigWorld.player()})
        self.resetItem = item
        itemData = uiUtils.getGfxItem(self.resetItem, location=const.ITEM_IN_REFINING)
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.confirmResumeCallback, self.selectedPos[0], self.selectedPos[1], self.selectedPos[2]), itemData=itemData)

    def confirmResumeCallback(self, resKind, page, pos):
        gamelog.info('jbx:unrefineManualEquipment', resKind, page, pos)
        BigWorld.player().cell.unrefineManualEquipment(resKind, page, pos)

    def canRefining(self, item):
        return item.isManualEquip() and MEPD.data.get(item.id, {}).get('canRefine', 0)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshLeftList(self.resKind)

    def getLeftListInfo(self, refreshKind = -1):
        info = {}
        p = BigWorld.player()
        refreshAll = refreshKind == -1
        equipList = []
        if refreshAll or refreshKind == const.RES_KIND_EQUIP:
            for i, item in enumerate(p.equipment):
                if not item:
                    continue
                if not self.canRefining(item):
                    continue
                if getattr(item, 'bindType', 0) != gametypes.ITEM_BIND_TYPE_FOREVER:
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
                if not self.canRefining(item):
                    continue
                if getattr(item, 'bindType', 0) != gametypes.ITEM_BIND_TYPE_FOREVER:
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
                    if not self.canRefining(item):
                        continue
                    if getattr(item, 'bindType', 0) != gametypes.ITEM_BIND_TYPE_FOREVER:
                        continue
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                    itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                    itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                    itemInfo['quality'] = getattr(item, 'quality', 0)
                    itemInfo['score'] = getattr(item, 'score', 0)
                    itemInfo['pos'] = [const.RES_KIND_INV, pg, ps]
                    unEquipList.append(itemInfo)

            unEquipList.sort(cmp=self.sort_unEquip)
        info['unEquipList'] = unEquipList
        info['refreshAll'] = refreshAll
        info['refreshKind'] = refreshKind
        return info

    def sort_unEquip(self, a, b):
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

    def refreshLeftList(self, refreshKind = -1, refreshDetail = True):
        info = self.getLeftListInfo(refreshKind)
        if info['refreshAll']:
            self.leftListInfo = info
        elif info['refreshKind'] == const.RES_KIND_EQUIP:
            self.leftListInfo['equipList'] = info['equipList']
        elif info['refreshKind'] == const.RES_KIND_SUB_EQUIP_BAG:
            self.leftListInfo['subEquipList'] = info['subEquipList']
        elif info['refreshKind'] == const.RES_KIND_INV:
            self.leftListInfo['unEquipList'] = info['unEquipList']
        equipBtn = self.widget.equipBtn
        scrollWndList = self.widget.scrollWndList
        noItemHint = self.widget.noItemHint
        subEquipBtn = self.widget.subEquipBtn
        unEquipBtn = self.widget.unEquipBtn
        leftListInfo = self.leftListInfo
        if equipBtn.selected and (info['refreshAll'] or info['refreshKind'] == const.RES_KIND_EQUIP):
            if self.selectedUUID == '' and len(self.leftListInfo['equipList']) > 0:
                self.selectedUUID = self.leftListInfo['equipList'][0]['uuid']
                self.selectedPos = self.leftListInfo['equipList'][0]['pos']
            scrollWndList.dataArray = self.leftListInfo['equipList']
            scrollWndList.validateNow()
            noItemHint.visible = len(self.leftListInfo['equipList']) <= 0
        elif subEquipBtn.selected and (info['refreshAll'] or info['refreshKind'] == const.RES_KIND_SUB_EQUIP_BAG):
            if self.selectedUUID == '' and len(self.leftListInfo['subEquipList']) > 0:
                self.selectedUUID = self.leftListInfo['subEquipList'][0]['uuid']
                self.selectedPos = self.leftListInfo['subEquipList'][0]['pos']
            scrollWndList.dataArray = self.leftListInfo['subEquipList']
            scrollWndList.validateNow()
            noItemHint.visible = len(leftListInfo['subEquipList']) <= 0
        elif unEquipBtn.selected and (info['refreshAll'] or info['refreshKind'] == const.RES_KIND_INV):
            if self.selectedUUID == '' and len(leftListInfo['unEquipList']) > 0:
                self.selectedUUID = leftListInfo['unEquipList'][0]['uuid']
                self.selectedPos = leftListInfo['unEquipList'][0]['pos']
            scrollWndList.dataArray = leftListInfo['unEquipList']
            scrollWndList.validateNow()
            noItemHint.visible = len(leftListInfo['unEquipList']) <= 0
        if refreshDetail:
            self.refreshDetailInfo()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        item = ASObject(args[3][1])
        item.data = itemData
        if self.selectedUUID == itemData.uuid:
            item.selected = True
            self.selectedMc = item
        else:
            item.selected = False
        item.addEventListener(events.MOUSE_CLICK, self.handleClickLeftItem, False, 0, True)
        item.addEventListener(events.EVENT_REMOVED_FROM_STAGE, self.handleBGLeftItemRemoved, False, 0, True)

    def handleBGLeftItemRemoved(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.removeEventListener(events.MOUSE_CLICK, self.handleClickLeftItem)
        e.currentTarget.removeEventListener(events.EVENT_REMOVED_FROM_STAGE, self.handleBGLeftItemRemoved)

    def handleClickLeftTab(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.selected:
            return
        else:
            self.selectedUUID = ''
            self.selectedPos = [-1, -1, -1]
            self.selectedMc = None
            self.resKind = int(e.currentTarget.data)
            e.currentTarget.selected = True
            self.firstRefresh = True
            self.refreshLeftList(self.resKind)
            return

    def handleClickLeftItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.selectedUUID == itemMc.data['uuid']:
            return
        self.firstRefresh = True
        if self.selectedMc:
            self.selectedMc.selected = False
        self.selectedMc = itemMc
        self.selectedMc.selected = True
        self.selectedUUID = self.selectedMc.data['uuid']
        self.selectedPos = self.selectedMc.data['pos']
        self.refreshDetailInfo()

    def getSpecialProps(self, i):
        mySes = []
        seManualProp = []
        for spId in i.getSpecialPropList():
            spData = ESPD.data.get(spId, {})
            if spData:
                seManualProp.append("<font color = \'#FF7F00\'>%s:%s</font>\n" % (spData.get('name', 'errorName'), spData.get('desc', 'errorDesc')))

        return seManualProp

    def getItem(self, resKind, page, pos):
        p = BigWorld.player()
        item = None
        if resKind == const.RES_KIND_EQUIP:
            item = p.equipment.get(pos)
        elif resKind == const.RES_KIND_SUB_EQUIP_BAG:
            item = commcalc.getAlternativeEquip(p, pos)
        elif resKind == const.RES_KIND_INV:
            item = p.inv.getQuickVal(page, pos)
        return item

    def getRefiningItem(self):
        p = BigWorld.player()
        item = None
        if self.selectedPos and self.selectedPos[0] == const.RES_KIND_EQUIP:
            item = p.equipment.get(self.selectedPos[2])
        elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            item = commcalc.getAlternativeEquip(p, self.selectedPos[2])
        elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
            item = p.inv.getQuickVal(self.selectedPos[1], self.selectedPos[2])
        return item

    def getDetailInfo(self, playEffect = False):
        info = {}
        item = self.getRefiningItem()
        p = BigWorld.player()
        if item:
            targetItemInfo = {}
            location = const.ITEM_IN_BAG
            if self.selectedPos and self.selectedPos[0] in (const.RES_KIND_EQUIP, const.RES_KIND_SUB_EQUIP_BAG):
                targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                location = const.ITEM_IN_EQUIPMENT
            elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
                targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                location = const.ITEM_IN_BAG
            canRefining = True
            targetItemInfo['isBind'] = getattr(item, 'bindType', 0) == gametypes.ITEM_BIND_TYPE_FOREVER
            info['targetItemInfo'] = targetItemInfo
            basic, rand, enh, basicShift, randShift = itemToolTipUtils.calAttrVal(item, location)
            randPropList = itemToolTipUtils.getRandProp(item, False, rand, [])
            shiftRandPropList = itemToolTipUtils.getRandProp(item, False, rand, randShift)
            propList = []
            shiftPropList = []
            itemToolTipUtils.addRandPropList(item, propList, shiftPropList, randPropList, shiftRandPropList)
            info['randPropList'] = shiftPropList
            info['specialPropList'] = self.getSpecialProps(item)
            info['playEffect'] = playEffect
            info['isEmpty'] = False
            makeType = item.makeType
            if targetItemInfo['isBind']:
                costItemId = SCD.data.get('refineManualEquipmentBindItemId', {}).get(makeType, 999)
            else:
                costItemId = SCD.data.get('refineManualEquipmentItemId', {}).get(makeType, 999)
            if targetItemInfo['isBind']:
                ownCount = BigWorld.player().inv.countItemInPages(Item.parentId(costItemId), enableParentCheck=True)
            else:
                ownCount = BigWorld.player().inv.countItemInPages(costItemId)
            needCount = MEPD.data.get(item.id, {}).get('refineItemCnt', 15)
            info['costItem'] = (costItemId, ownCount, needCount)
            canRefining = canRefining and ownCount >= needCount
            info['costCache'] = MEPD.data.get(item.id, {}).get('refineCash', 1000)
            info['resumeCount'] = getattr(item, 'refineManual', {}).get(item.REFINE_MANUAL_UNREFINE_CNT, 0)
            info['totalRefiningCount'] = getattr(item, 'refineManual', {}).get(item.REFINE_MANUAL_REFINE_CNT, 0)
            refineManualCntCycle = SCD.data.get('refineManualCntCycle', {}).get(makeType, 100000)
            info['checkCycleCnt'] = getattr(item, 'refineManual', {}).get(item.REFINE_MANUAL_SPECIAL_PROP_BASE_CNT, 0) >= refineManualCntCycle
            info['refiningCount'] = info['totalRefiningCount'] - info['resumeCount'] * SCD.data.get('unrefineManualEquipmentBaseCnt', 100)
            info['canRefining'] = canRefining
        else:
            info['isEmpty'] = True
        return info

    def setPropText(self, *args):
        args = ASObject(args[3][0])
        mc = args[0]
        oldProp, newProp = args[1], args[2]
        mc.oldProp.txt.htmlText = oldProp
        mc.newProp.txt.htmlText = newProp

    def setRandMc(self, itemMc, valueMc, itemInfo):
        itemMc.txt.htmlText = itemInfo['pName']
        if itemInfo['barType'] != 'no':
            valueMc.pValue.visible = False
            valueMc.progressBar.visible = True
            valueMc.subProgressBar.visible = True
            valueMc.progressBar.pValue.htmlText = itemInfo['pValue']
            valueMc.progressBar.currentValue = 100 - itemInfo['barValue']
            valueMc.subProgressBar.bar.gotoAndStop(itemInfo['barType'])
            valueMc.subProgressBar.currentValue = itemInfo['subBarValue']
        else:
            valueMc.progressBar.visible = False
            valueMc.subProgressBar.visible = False
            valueMc.pValue.htmlText = itemInfo['pValue']

    def frameCallback(self, *args):
        args = ASObject(args[3][0])
        randPropMc = args[0]
        randPropInfo = args[1]
        if randPropInfo:
            self.setRandMc(randPropMc.newProp, randPropMc.newValue, randPropInfo)

    def refreshDetailInfo(self, playEffect = False, randomIdx = None):
        info = self.getDetailInfo(playEffect)
        effect = self.widget.effect
        targetItem = self.widget.targetItem
        detail = self.widget.detail
        emptyCover = self.widget.emptyCover
        effect.visible = False
        if info['isEmpty']:
            self.widget.targetItem.clear()
            self.widget.emptyCover.visible = True
            self.widget.detail.visible = False
            self.widget.confirmBtn.enabled = False
            self.widget.txtIsBind.text = ''
            self.widget.resetBtn.enabled = False
            self.widget.refiningCount.text = ''
            self.widget.resetBtn.label = ''
            return
        else:
            self.widget.emptyCover.visible = False
            self.widget.detail.visible = True
            if info['playEffect']:
                effect.visible = True
                effect.gotoAndPlay(1)
            else:
                effect.visible = False
            targetItem.slot.setItemSlotData(info['targetItemInfo'])
            targetItem.slot.setItemSlotData(info['targetItemInfo'])
            self.widget.txtIsBind.text = gameStrings.EQUIP_CHANGE_REFINING_BIND if info['targetItemInfo']['isBind'] else gameStrings.EQUIP_CHANGE_REFINING_UNBIND
            randPropList, specialPropList = info['randPropList'], info['specialPropList']
            uuid = info['targetItemInfo']['uuid']
            oldRandPropList, oldSpecialPropList = self.oldPropCache.get(uuid, ([], []))
            for i in xrange(RAND_PROP_MAX_CNT):
                randPropMc = self.widget.detail.getChildByName('randProp%d' % i)
                randPropInfo = randPropList[i] if i < len(randPropList) else None
                oldPropInfo = oldRandPropList[i] if i < len(oldRandPropList) else None
                if randomIdx != None and randomIdx == i:
                    randPropMc.gotoAndPlay('new')
                    randPropMc.gotoAndPlay('new')
                    self.setRandMc(randPropMc.oldProp, randPropMc.oldValue, oldPropInfo)
                    self.setRandMc(randPropMc.newProp, randPropMc.newValue, randPropInfo)
                    ASUtils.callbackAtFrame(randPropMc, 20, self.frameCallback, randPropMc, randPropInfo)
                    ASUtils.callbackAtFrame(randPropMc, 25, self.frameCallback, randPropMc, randPropInfo)
                else:
                    randPropMc.gotoAndStop('old')
                    self.setRandMc(randPropMc.oldProp, randPropMc.oldValue, randPropInfo)

            for i in xrange(SPECIAL_PROP_MAX_CNT):
                specialPropMc = self.widget.detail.getChildByName('sepcialProp%d' % i)
                specialPropInfo = specialPropList[i] if i < len(specialPropList) else None
                oldSpecialPropInfo = oldSpecialPropList[i] if i < len(oldSpecialPropList) else None
                if self.firstRefresh:
                    specialPropMc.gotoAndStop('old')
                    if i < len(specialPropList):
                        specialPropMc.oldProp.txt.htmlText = specialPropList[i]
                    else:
                        specialPropMc.oldProp.txt.htmlText = ''
                    continue
                elif self.oldPropCache.has_key(uuid) and specialPropInfo and oldSpecialPropInfo and specialPropInfo != oldSpecialPropInfo:
                    specialPropMc.gotoAndPlay('new')
                    specialPropMc.gotoAndPlay('new')
                    oldPropTxt = oldSpecialPropList[i] if i < len(oldSpecialPropList) else ''
                    newPropTxt = specialPropList[i] if i < len(specialPropList) else ''
                    if i < len(oldSpecialPropList) and (i >= len(specialPropList) or specialPropList[i] != oldSpecialPropList[i]):
                        specialPropMc.oldProp.txt.htmlText = oldSpecialPropList[i]
                    else:
                        specialPropMc.oldProp.txt.htmlText = ''
                    ASUtils.callbackAtFrame(specialPropMc, 20, self.setPropText, specialPropMc, oldPropTxt, newPropTxt)
                    ASUtils.callbackAtFrame(specialPropMc, 25, self.setPropText, specialPropMc, oldPropTxt, newPropTxt)
                else:
                    specialPropMc.gotoAndStop('old')
                    specialPropMc.gotoAndStop('old')
                    if i < len(specialPropList):
                        specialPropMc.oldProp.txt.htmlText = specialPropList[i]
                    else:
                        specialPropMc.oldProp.txt.htmlText = ''

            self.oldPropCache[info['targetItemInfo']['uuid']] = (randPropList, specialPropList)
            costItemId, ownCount, needCount = info['costItem']
            self.widget.detail.bindText.text = gameStrings.EQUIP_CHANGE_REFINING_BIND if info['targetItemInfo']['isBind'] else gameStrings.EQUIP_CHANGE_REFINING_UNBIND
            costItemData = uiUtils.getGfxItemById(costItemId, '%d/%d' % (ownCount, needCount))
            self.widget.detail.slot2.slot.setItemSlotData(costItemData)
            self.widget.detail.slot2.slot.valueAmount.visible = False
            self.widget.detail.slot2.txtNum.text = '%d/%d' % (ownCount, needCount)
            if ownCount < needCount:
                self.widget.detail.slot2.setState(uiConst.SLOT_STATE_HELP)
                self.widget.detail.slot2.addEventListener(events.BUTTON_CLICK, self.handleStaetClick, False, 0, True)
                self.widget.detail.slot2.itemId = costItemId
            else:
                self.widget.detail.slot2.setState(uiConst.SLOT_STATE_EMPTY)
                self.widget.detail.slot2.removeEventListener(events.BUTTON_CLICK, self.handleStaetClick, False)
            self.widget.detail.needCash.cashIcon.bonusType = 'bindCash' if info['targetItemInfo']['isBind'] else 'cash'
            self.widget.detail.needCash.cash.text = info['costCache']
            refiningCount, resumeCount = info['refiningCount'], info['resumeCount']
            canResumeCnt = refiningCount / SCD.data.get('unrefineManualEquipmentBaseCnt', 100)
            self.widget.resetBtn.enabled = bool(canResumeCnt)
            self.widget.resetBtn.label = gameStrings.EQUIP_CHANGE_RESUME_COUNT % canResumeCnt
            self.widget.refiningCount.text = gameStrings.EQUIP_CHANGE_REFINING_COUNT % refiningCount
            unrefineManualEquipmentBaseCnt = SCD.data.get('unrefineManualEquipmentBaseCnt', 100)
            TipManager.addTip(self.widget.refiningCount, gameStrings.EQUIP_CHANGE_TOTAL_REFINING_COUNT % (unrefineManualEquipmentBaseCnt * resumeCount + refiningCount, unrefineManualEquipmentBaseCnt))
            self.widget.confirmBtn.enabled = info['canRefining']
            self.firstRefresh = False
            return

    def handleStaetClick(self, *args):
        self.uiAdapter.itemSourceInfor.openPanel()
