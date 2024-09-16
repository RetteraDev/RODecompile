#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/awakeRecastProxy.o
import BigWorld
import uiConst
import const
import gametypes
import events
import gameglobal
import commcalc
import copy
import utils
from item import Item
from uiProxy import UIProxy
from guis import uiUtils
from guis import asObject
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import equip_enhance_item_config_data as EEICD
from data import equip_data as ED
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
JUEXING_MAX_NUM = 4

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


class AwakeRecastProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AwakeRecastProxy, self).__init__(uiAdapter)
        self.widget = None
        self.consumeItemId = 0
        self.leftListInfo = {}
        self.selectedUUID = ''
        self.selectedPos = []
        self.selectedMc = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_AWAKE_RECAST, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_AWAKE_RECAST:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_AWAKE_RECAST)

    def reset(self):
        self.consumeItemId = 0
        self.leftListInfo = {}
        self.selectedUUID = ''
        self.selectedPos = []
        self.selectedMc = None

    def show(self, consumeItemId):
        if not gameglobal.rds.configData.get('enableReforgeEquipJuexingWithItem', False):
            return
        self.selectedUUID = ''
        self.consumeItemId = consumeItemId
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_AWAKE_RECAST)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.awakeRecastPanel.equipBtn.groupName = 'leftTab'
        self.widget.awakeRecastPanel.equipBtn.addEventListener(events.BUTTON_CLICK, self.handleClickLeftTab, False, 0, True)
        self.widget.awakeRecastPanel.subEquipBtn.groupName = 'leftTab'
        self.widget.awakeRecastPanel.subEquipBtn.addEventListener(events.BUTTON_CLICK, self.handleClickLeftTab, False, 0, True)
        self.widget.awakeRecastPanel.unEquipBtn.groupName = 'leftTab'
        self.widget.awakeRecastPanel.unEquipBtn.addEventListener(events.BUTTON_CLICK, self.handleClickLeftTab, False, 0, True)
        self.widget.awakeRecastPanel.effect.visible = False
        ASUtils.setHitTestDisable(self.widget.awakeRecastPanel.effect, True)
        self.widget.awakeRecastPanel.targetItem.clear()
        self.widget.awakeRecastPanel.targetItem.showCloseBtn = True
        self.widget.awakeRecastPanel.targetItem.slot.addEventListener(events.MOUSE_CLICK, self.handleRemoveItem, False, 0, True)
        self.widget.awakeRecastPanel.targetItem.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleRemoveItem, False, 0, True)
        self.widget.awakeRecastPanel.useOldBtn.addEventListener(events.BUTTON_CLICK, self.handleUseOld, False, 0, True)
        self.widget.awakeRecastPanel.useNewBtn.addEventListener(events.BUTTON_CLICK, self.handleUseNew, False, 0, True)
        self.widget.awakeRecastPanel.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirm, False, 0, True)
        self.widget.awakeRecastPanel.equipBtn.selected = True
        self.widget.awakeRecastPanel.scrollWndList.itemRenderer = 'AwakeRecast_LeftItem'
        self.widget.awakeRecastPanel.scrollWndList.dataArray = []
        self.widget.awakeRecastPanel.scrollWndList.lableFunction = self.itemFunction

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshLeftList(self.getLeftList())

    def handleClickLeftTab(self, *args):
        e = asObject.ASObject(args[3][0])
        if e.currentTarget.selected:
            return
        e.currentTarget.selected = True
        self.refreshLeftList(self.leftListInfo)

    def handleRemoveItem(self, *args):
        e = asObject.ASObject(args[3][0])
        if e.currentTarget.name == 'slot':
            if e.buttonIdx == uiConst.RIGHT_BUTTON:
                self.removeItem()
        elif e.currentTarget.name == 'closeBtn':
            self.removeItem()

    def handleUseOld(self, *args):
        item = self.getRebuildItem()
        if not item:
            return
        if item.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.NEW_JUEXING_MISS_CONFIRM)
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.selectJuexing, False))

    def selectJuexing(self, isNew):
        item = self.getRebuildItem()
        if not item:
            return
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        BigWorld.player().cell.confirmReforgeEquipJuexingAllNew(isNew, self.selectedPos[0], self.selectedPos[1], realPos, item.uuid)

    def handleUseNew(self, *args):
        item = self.getRebuildItem()
        if not item:
            return
        if item.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        msg = uiUtils.getTextFromGMD(GMDD.data.OLD_JUEXING_MISS_CONFIRM)
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.selectJuexing, True))

    def handleConfirm(self, *args):
        item = self.getRebuildItem()
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
        item = self.getRebuildItem()
        if not item:
            return
        if gameglobal.rds.configData.get('enableFreeJuexingRebuild', False) and p.getFame(const.REFORGE_EQUIP_JUEXING_FAME_ID) > 0:
            if not item.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
            else:
                self.trueConfirm()
            return
        if not item.isForeverBind():
            msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
            return
        if p.inv.countItemBind(self.consumeItemId, enableParentCheck=True):
            if not item.isForeverBind():
                msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.trueConfirm)
            else:
                self.trueConfirm()
        else:
            self.trueConfirm()

    def trueConfirm(self):
        item = self.getRebuildItem()
        if not item:
            return
        realPos = self.selectedPos[2]
        if self.selectedPos[0] == const.RES_KIND_SUB_EQUIP_BAG:
            realPos = gametypes.equipTosubEquipPartMap.get(self.selectedPos[2], -1)
        if realPos < 0:
            return
        p = BigWorld.player()
        p.cell.reforgeEquipJuexingAllNewWithItem(self.selectedPos[0], self.selectedPos[1], realPos, self.consumeItemId)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.data = itemData
        itemMc.disabled = itemData.isItemDisabled
        if not itemMc.disabled and self.selectedUUID == itemData.uuid:
            itemMc.selected = True
            self.selectedMc = itemMc
        else:
            itemMc.selected = False
        if itemMc.disabled:
            itemMc.removeEventListener(events.MOUSE_CLICK, self.handleClickLeftItem)
            itemMc.removeEventListener(events.EVENT_REMOVED_FROM_STAGE, self.handleBGLeftItemRemoved)
        else:
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleClickLeftItem, False, 0, True)
            itemMc.addEventListener(events.EVENT_REMOVED_FROM_STAGE, self.handleBGLeftItemRemoved, False, 0, True)

    def handleClickLeftItem(self, *args):
        e = asObject.ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.selectedUUID == itemMc.data.uuid:
            return
        if self.selectedMc:
            self.selectedMc.selected = False
        self.selectedMc = itemMc
        self.selectedMc.selected = True
        self.selectedUUID = self.selectedMc.data.uuid
        self.selectedPos = self.selectedMc.data.pos
        self.refreshDetailInfo()

    def handleBGLeftItemRemoved(self, *args):
        e = asObject.ASObject(args[3][0])
        e.currentTarget.removeEventListener(events.MOUSE_CLICK, self.handleClickLeftItem)
        e.currentTarget.removeEventListener(events.EVENT_REMOVED_FROM_STAGE, self.handleBGLeftItemRemoved)

    def checkItemDisabled(self, equipId):
        edData = ED.data.get(equipId, {})
        equipType = edData.get('equipType', 0)
        enhanceType = edData.get('enhanceType', 1)
        if equipType == Item.EQUIP_BASETYPE_WEAPON:
            subType = edData.get('weaponSType', 0)
        elif equipType == Item.EQUIP_BASETYPE_ARMOR:
            subType = edData.get('armorSType', 0)
        elif equipType == Item.EQUIP_BASETYPE_JEWELRY:
            subType = edData.get('jewelSType', 0)
        itemToEquipType = EEICD.data.get(self.consumeItemId, {}).get('equipType', (0, 0, 0))
        if itemToEquipType[0] == equipType and itemToEquipType[1] == subType and itemToEquipType[2] == enhanceType:
            return False
        return True

    def getLeftList(self, refreshKind = -1):
        p = BigWorld.player()
        info = {}
        refreshAll = refreshKind == -1
        equipList = []
        equipList1 = []
        equipList2 = []
        if refreshAll or refreshKind == const.RES_KIND_EQUIP:
            for i, item in enumerate(p.equipment):
                if not item:
                    continue
                if not item.isItemCanRebuild():
                    continue
                itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                itemInfo['pos'] = [const.RES_KIND_EQUIP, 0, i]
                itemInfo['isItemDisabled'] = self.checkItemDisabled(item.id)
                if itemInfo['isItemDisabled']:
                    equipList2.append(itemInfo)
                else:
                    equipList1.append(itemInfo)

            equipList1.sort(key=lambda x: x['sortIdx'])
            equipList2.sort(key=lambda x: x['sortIdx'])
            equipList = equipList1 + equipList2
        info['equipList'] = equipList
        subEquipList = []
        subEquipList1 = []
        subEquipList2 = []
        if refreshAll or refreshKind == const.RES_KIND_SUB_EQUIP_BAG:
            for pos in gametypes.EQU_PART_SUB:
                item = commcalc.getAlternativeEquip(p, pos)
                if not item:
                    continue
                if not item.isItemCanRebuild():
                    continue
                itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
                itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                itemInfo['pos'] = [const.RES_KIND_SUB_EQUIP_BAG, 0, pos]
                itemInfo['isItemDisabled'] = self.checkItemDisabled(item.id)
                if itemInfo['isItemDisabled']:
                    subEquipList2.append(itemInfo)
                else:
                    subEquipList1.append(itemInfo)

            subEquipList1.sort(key=lambda x: x['sortIdx'])
            subEquipList2.sort(key=lambda x: x['sortIdx'])
            subEquipList = subEquipList1 + subEquipList2
        info['subEquipList'] = subEquipList
        unEquipList = []
        unEquipList1 = []
        unEquipList2 = []
        if refreshAll or refreshKind == const.RES_KIND_INV:
            for pg in p.inv.getPageTuple():
                for ps in p.inv.getPosTuple(pg):
                    item = p.inv.getQuickVal(pg, ps)
                    if item == const.CONT_EMPTY_VAL:
                        continue
                    if not item.isItemCanRebuild():
                        continue
                    itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
                    itemInfo['itemName'] = uiUtils.getItemColorNameByItem(item, True, -1, True)
                    itemInfo['sortIdx'] = uiUtils.getEquipSortIdxByPart(item)
                    itemInfo['quality'] = getattr(item, 'quality', 0)
                    itemInfo['score'] = getattr(item, 'score', 0)
                    itemInfo['pos'] = [const.RES_KIND_INV, pg, ps]
                    itemInfo['isItemDisabled'] = self.checkItemDisabled(item.id)
                    if itemInfo['isItemDisabled']:
                        unEquipList2.append(itemInfo)
                    else:
                        unEquipList1.append(itemInfo)

            unEquipList1.sort(cmp=sort_unEquip)
            unEquipList2.sort(cmp=sort_unEquip)
            unEquipList = unEquipList1 + unEquipList2
        info['unEquipList'] = unEquipList
        info['refreshAll'] = refreshAll
        info['refreshKind'] = refreshKind
        info['noItemHint'] = SCD.data.get('equipChangeJuexingRebuildNoItemHint', '')
        return info

    def refreshLeftList(self, info):
        if info.get('refreshAll', False):
            self.leftListInfo = info
        elif info['refreshKind'] == const.RES_KIND_EQUIP:
            self.leftListInfo['equipList'] = info.get('equipList', [])
        elif info['refreshKind'] == const.RES_KIND_SUB_EQUIP_BAG:
            self.leftListInfo['subEquipList'] = info.get('subEquipList', [])
        elif info['refreshKind'] == const.RES_KIND_INV:
            self.leftListInfo['unEquipList'] = info.get('unEquipList', [])
        if self.widget.awakeRecastPanel.equipBtn.selected and (self.leftListInfo['refreshAll'] or self.leftListInfo['refreshKind'] == const.RES_KIND_EQUIP):
            if self.selectedUUID == '' and len(self.leftListInfo.get('equipList', [])) > 0:
                if not self.leftListInfo['equipList'][0]['isItemDisabled']:
                    self.selectedUUID = self.leftListInfo['equipList'][0]['uuid']
                    self.selectedPos = self.leftListInfo['equipList'][0]['pos']
            self.widget.awakeRecastPanel.scrollWndList.dataArray = self.leftListInfo.get('equipList', [])
            self.widget.awakeRecastPanel.scrollWndList.validateNow()
            self.widget.awakeRecastPanel.noItemHint.visible = len(self.leftListInfo.get('equipList', [])) <= 0
        elif self.widget.awakeRecastPanel.subEquipBtn.selected and (self.leftListInfo['refreshAll'] or self.leftListInfo['refreshKind'] == const.RES_KIND_SUB_EQUIP_BAG):
            if self.selectedUUID == '' and len(self.leftListInfo.get('subEquipList', [])) > 0:
                if not self.leftListInfo['subEquipList'][0]['isItemDisabled']:
                    self.selectedUUID = self.leftListInfo['subEquipList'][0]['uuid']
                    self.selectedPos = self.leftListInfo['subEquipList'][0]['pos']
            self.widget.awakeRecastPanel.scrollWndList.dataArray = self.leftListInfo.get('subEquipList', [])
            self.widget.awakeRecastPanel.scrollWndList.validateNow()
            self.widget.awakeRecastPanel.noItemHint.visible = len(self.leftListInfo.get('subEquipList', [])) <= 0
        elif self.widget.awakeRecastPanel.unEquipBtn.selected and (self.leftListInfo['refreshAll'] or self.leftListInfo['refreshAll'] == const.RES_KIND_INV):
            if self.selectedUUID == '' and len(self.leftListInfo.get('unEquipList', [])) > 0:
                if not self.leftListInfo['unEquipList'][0]['isItemDisabled']:
                    self.selectedUUID = self.leftListInfo['unEquipList'][0]['uuid']
                    self.selectedPos = self.leftListInfo['unEquipList'][0]['pos']
            self.widget.awakeRecastPanel.scrollWndList.dataArray = self.leftListInfo.get('unEquipList', [])
            self.widget.awakeRecastPanel.scrollWndList.validateNow()
            self.widget.awakeRecastPanel.noItemHint.visible = len(self.leftListInfo.get('unEquipList', [])) <= 0
        self.refreshDetailInfo()

    def removeItem(self):
        if self.selectedUUID == '':
            return
        else:
            self.selectedUUID = ''
            self.selectedPos = [-1, -1, -1]
            if self.selectedMc:
                self.selectedMc.selected = False
            self.selectedMc = None
            self.refreshDetailInfo()
            return

    def getDetailInfo(self, playEffect):
        info = {}
        item = self.getRebuildItem()
        if item:
            targetItemInfo = {}
            if self.selectedPos and self.selectedPos[0] in (const.RES_KIND_EQUIP, const.RES_KIND_SUB_EQUIP_BAG):
                targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_EQUIPMENT)
            elif self.selectedPos and self.selectedPos[0] == const.RES_KIND_INV:
                targetItemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
            info['targetItemInfo'] = targetItemInfo
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
            info['playEffect'] = playEffect
            info['isEmpty'] = False
        else:
            info['isEmpty'] = True
        if gameglobal.rds.configData.get('enableFreeJuexingRebuild', False):
            info['showFree'] = True
            freeNum = BigWorld.player().getFame(const.REFORGE_EQUIP_JUEXING_FAME_ID)
            info['freeNum'] = freeNum
            info['freeTips'] = SCD.data.get('equipChangeJuexingRebuildFreeTips', '')
        else:
            info['showFree'] = False
        return info

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

    def refreshDetailInfo(self, playEffect = False):
        info = self.getDetailInfo(playEffect)
        self.widget.awakeRecastPanel.effect.visible = False
        if info.get('isEmpty', True):
            self.widget.awakeRecastPanel.targetItem.clear()
            self.widget.awakeRecastPanel.emptyCover.visible = True
            self.widget.awakeRecastPanel.detail.visible = False
            self.widget.awakeRecastPanel.useOldBtn.enabled = False
            self.widget.awakeRecastPanel.useNewBtn.enabled = False
            self.widget.awakeRecastPanel.confirmBtn.enabled = False
            return
        else:
            if info.get('playEffect', False):
                self.widget.awakeRecastPanel.effect.visible = True
                self.widget.awakeRecastPanel.effect.gotoAndPlay(1)
            self.widget.awakeRecastPanel.targetItem.slot.setItemSlotData(info.get('targetItemInfo', None))
            self.widget.awakeRecastPanel.detail.visible = True
            juexingLen = len(info.get('juexingList', []))
            for i in xrange(JUEXING_MAX_NUM):
                itemMc = self.widget.awakeRecastPanel.detail.getChildByName('juexing%d' % i)
                if i >= juexingLen:
                    itemMc.visible = False
                    continue
                itemInfo = info['juexingList'][i]
                itemMc.visible = True
                itemMc.prop.htmlText = itemInfo[1]
                itemMc.stageLv.gotoAndStop('l%s' % itemInfo[3])

            if info.get('hasNewJuexing', False):
                self.widget.awakeRecastPanel.detail.newJuexing.gotoAndStop('new')
                self.widget.awakeRecastPanel.useOldBtn.enabled = True
                self.widget.awakeRecastPanel.useNewBtn.enabled = True
                newJuexingLen = len(info.get('newJuexingList', []))
                for i in xrange(JUEXING_MAX_NUM):
                    itemMc = self.widget.awakeRecastPanel.detail.newJuexing.getChildByName('juexing%d' % i)
                    if i >= newJuexingLen:
                        itemMc.visible = False
                        continue
                    itemInfo = info['newJuexingList'][i]
                    itemMc.visible = True
                    itemMc.prop.htmlText = itemInfo[1]
                    itemMc.stageLv.gotoAndStop('l%s' % itemInfo[3])

            else:
                self.widget.awakeRecastPanel.detail.newJuexing.gotoAndStop('old')
                self.widget.awakeRecastPanel.useOldBtn.enabled = False
                self.widget.awakeRecastPanel.useNewBtn.enabled = False
                self.widget.awakeRecastPanel.emptyCover.visible = False
            self.widget.awakeRecastPanel.emptyCover.visible = False
            self.refreshConsumeInfo()
            return

    def getConsumeInfo(self):
        p = BigWorld.player()
        info = {}
        item = self.getRebuildItem()
        if not item:
            return info
        myItemNum = p.inv.countItemInPages(uiUtils.getParentId(self.consumeItemId), enableParentCheck=True)
        needNum = EEICD.data.get(self.consumeItemId, {}).get('num', 0)
        count = str('%s/%d' % (myItemNum, needNum))
        consumeInfo = uiUtils.getGfxItemById(self.consumeItemId, count)
        info['consumeInfo'] = consumeInfo
        btnEnabled = myItemNum >= needNum
        if gameglobal.rds.configData.get('enableFreeJuexingRebuild', False):
            isFree = p.getFame(const.REFORGE_EQUIP_JUEXING_FAME_ID) > 0
        else:
            isFree = False
        info['isFree'] = isFree
        if isFree:
            info['btnLabel'] = gameStrings.EQUIP_CHANGE_JUEXING_REBUILD_CONFIRM_BTN_FREE
            info['btnEnabled'] = True
        else:
            info['btnLabel'] = gameStrings.EQUIP_CHANGE_JUEXING_REBUILD_CONFIRM_BTN
            info['btnEnabled'] = btnEnabled
        return info

    def refreshConsumeInfo(self):
        info = self.getConsumeInfo()
        if not info:
            return
        self.widget.awakeRecastPanel.detail.resultDesc.htmlText = EEICD.data.get(self.consumeItemId, {}).get('desc', '')
        self.widget.awakeRecastPanel.detail.slot.dragable = False
        self.widget.awakeRecastPanel.detail.slot.setItemSlotData(info['consumeInfo'])
        self.widget.awakeRecastPanel.confirmBtn.label = info.get('btnLabel', '')
        self.widget.awakeRecastPanel.confirmBtn.enabled = info.get('btnEnabled', False)

    def juexingRebuildResult(self, resKind, page, pos, itemUUID, jxData):
        if not self.widget:
            return
        else:
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
            if newItem.uuid == itemUUID:
                newItem.tempJXAlldata = jxData
            item = self.getRebuildItem()
            if not item:
                return
            if item.uuid == itemUUID:
                self.refreshDetailInfo()
            return

    def juexingRebuildFinish(self, resKind, page, pos, itemUUID, ok):
        if not self.widget:
            return
        self.refreshLeftList(self.getLeftList(resKind))
        item = self.getRebuildItem()
        if not item:
            return
        if item.uuid == itemUUID:
            self.refreshDetailInfo(ok)
