#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/runeInvProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gamelog
from guis import ui
from guis import uiUtils
from guis import uiConst
from guis import tipUtils
from callbackHelper import Functor
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
import events
from uiProxy import SlotDataProxy
PAGE_ITEMS_CNT = 36
BAG_SOLT_NUM = 6
BAG_PAGE_MAX_CNT = 5
from data import sys_config_data as SCD
from data import game_msg_data as GMD
from data import rune_prop_pskill_map_data as RPPMD
from cdata import game_msg_def_data as GMDD
EFFECT_TYPE_ALL = -1000
PROP_TYPE_ALL = -1000

class RuneInvProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(RuneInvProxy, self).__init__(uiAdapter)
        self.widget = None
        self.bindType = 'runeInv'
        self.type = 'runeInv'
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_RUNE_BAG, self.hide)

    def reset(self):
        self.currentPage = 0
        self.selectedPos = None
        self.lastSelectedPageMc = None
        self.filterEffectType = None
        self.filterPropId = None
        self.effectTypes = []
        self.runePropIds = []
        self.searchRange = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RUNE_BAG:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        p = BigWorld.player()
        if p:
            p.unRegisterEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
            p.unRegisterEvent(const.EVENT_ITEM_REMOVE, self.onItemChange)
            p.unRegisterEvent(const.EVENT_ITEM_SORT, self.onItemChange)
            p.unRegisterEvent(const.EVENT_ITEM_MOVE, self.onItemMove)
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RUNE_BAG)

    def show(self):
        if not self.widget:
            p = BigWorld.player()
            p.registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
            p.registerEvent(const.EVENT_ITEM_REMOVE, self.onItemChange)
            p.registerEvent(const.EVENT_ITEM_MOVE, self.onItemMove)
            p.registerEvent(const.EVENT_ITEM_SORT, self.onItemChange)
            self.uiAdapter.loadWidget(uiConst.WIDGET_RUNE_BAG)

    def onItemMove(self, params):
        srcKind, srcPage, srcPos, dstKind, dstPage, dstPos = params
        gamelog.info('jbx:onItemMove', srcKind, srcPage, srcPos, dstKind, dstPage, dstPos)
        self.onItemChange((srcKind, srcPage, srcPos))
        self.onItemChange((dstKind, dstPage, dstPos))

    def onItemChange(self, paragms):
        kind = paragms[0]
        page = paragms[1]
        pos = paragms[2]
        item = paragms[3] if len(paragms) > 3 else None
        gamelog.info('jbx:onItemChange', kind, page, pos, item)
        if kind == const.RES_KIND_HIEROGRAM_BAG:
            self.updateItem(page, pos)
        if kind == const.RES_KIND_HIEROGRAM_BAG_BAR:
            self.refreshBagSlot()

    def initUI(self):
        p = BigWorld.player()
        p.genPropToNameMap()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        for i in self.getInv().getPageTuple():
            pageBtn = self.widget.getChildByName('eqBtn%d' % (i + 1))
            pageBtn.idx = i
            pageBtn.addEventListener(events.BUTTON_CLICK, self.handlePageBtnClick, False, 0, True)
            pageBtn.addEventListener(events.MOUSE_ROLL_OVER, self.handlePageBtnRollOver, False, 0, True)

        self.widget.autoPutBtn.addEventListener(events.BUTTON_CLICK, self.handleAutoPutBtnClick, False, 0, True)
        self.widget.autoSortBtn.addEventListener(events.BUTTON_CLICK, self.handleAutoSortBtnClick, False, 0, True)
        self.widget.clearBtn.addEventListener(events.BUTTON_CLICK, self.handleClearBtnClick, False, 0, True)
        self.widget.searachBtn.addEventListener(events.BUTTON_CLICK, self.handleSearchBtnClick, False, 0, True)
        effectTypes = p.runeType2PropDic.keys()
        effectTypes.insert(0, gameStrings.RUNE_EFFECT_TYPE_ALL)
        self.effectTypes = effectTypes
        self.widget.dropDownType.labelFunction = self.dropDownTypeItemToLabel
        self.widget.dropDownType.addEventListener(events.INDEX_CHANGE, self.handleDropDownTypeIndexChange, False, 0, True)
        self.widget.dropDownType.defaultText = gameStrings.RUNE_BAG_FILTER_TYPE
        ASUtils.setDropdownMenuData(self.widget.dropDownType, effectTypes)
        self.widget.dropDownProp.labelFunction = self.dropDownPropItemToLabel
        self.widget.dropDownProp.addEventListener(events.INDEX_CHANGE, self.handleDropDownPropIndexChange, False, 0, True)
        self.widget.inputLow.textField.restrict = '0-9.'
        self.widget.inputHigh.textField.restrict = '0-9.'
        ASUtils.setHitTestDisable(self.widget.txt0, True)
        self.refreshDropDownPropData()

    def refreshDropDownPropData(self):
        self.runePropIds = []
        p = BigWorld.player()
        if not self.filterEffectType:
            for props in p.runeType2PropDic.itervalues():
                self.runePropIds.extend(props)

        else:
            self.runePropIds = p.runeType2PropDic.get(self.filterEffectType, [])
        self.runePropIds.insert(0, (0, 0, PROP_TYPE_ALL))
        ASUtils.setDropdownMenuData(self.widget.dropDownProp, self.runePropIds)
        self.widget.dropDownProp.defaultText = gameStrings.RUNE_BAG_FILTER_PROP
        self.refreshSlotEnable()

    def handleDropDownPropIndexChange(self, *args):
        index = int(self.widget.dropDownProp.selectedIndex)
        if index >= len(self.runePropIds):
            return
        else:
            self.filterPropId = self.runePropIds[index][2]
            if self.filterPropId == PROP_TYPE_ALL:
                self.filterPropId = None
            self.refreshSlotEnable()
            return

    def dropDownPropItemToLabel(self, *args):
        typeData = ASObject(args[3][0])
        propId = typeData[2]
        if propId == PROP_TYPE_ALL:
            return GfxValue(ui.gbk2unicode(gameStrings.RUNE_PROP_TYPE_ALL))
        return GfxValue(ui.gbk2unicode(RPPMD.data.get(propId, {}).get('listName', '')))

    def handleDropDownTypeIndexChange(self, *args):
        selectedIdx = self.widget.dropDownType.selectedIndex
        if selectedIdx >= len(self.effectTypes):
            return
        else:
            self.filterEffectType = self.effectTypes[selectedIdx]
            if self.filterEffectType == gameStrings.RUNE_EFFECT_TYPE_ALL:
                self.filterEffectType = None
            self.filterPropId = None
            self.widget.dropDownProp.selectedIndex = -1
            self.refreshDropDownPropData()
            self.refreshSlotEnable()
            return

    def dropDownTypeItemToLabel(self, *args):
        return args[3][0]

    def handleSearchBtnClick(self, *args):
        try:
            lowSide = float(self.widget.inputLow.text)
            highSide = float(self.widget.inputHigh.text)
            if lowSide >= 0 and highSide > 0 and lowSide < highSide:
                self.searchRange = (lowSide * 1.0 / 100, highSide * 1.0 / 100)
                self.refreshSlotEnable()
            else:
                BigWorld.player().showGameMsg(GMDD.data.RUNE_INV_QUERY_ERROR_RANGE, ())
        except:
            BigWorld.player().showGameMsg(GMDD.data.RUNE_INV_QUERY_ERROR_RANGE, ())

    def handleClearBtnClick(self, *args):
        self.searchRange = None
        self.widget.inputLow.text = ' '
        self.widget.inputHigh.text = ' '
        self.refreshSlotEnable()

    def handleAutoSortBtnClick(self, *args):
        if self.uiAdapter.equipChange.mediator:
            BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
            return
        BigWorld.player().base.sortHierogramBag()

    def handleAutoPutBtnClick(self, *args):
        if self.uiAdapter.equipChange.mediator:
            BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
            return
        BigWorld.player().base.allInv2HierogramBag()

    def handlePageBtnRollOver(self, *args):
        if not self.uiAdapter.inventory.isInDragCommonItem():
            return
        e = ASObject(args[3][0])
        page = int(e.currentTarget.idx)
        if page == self.currentPage:
            return
        self.currentPage = page
        if self.lastSelectedPageMc:
            self.lastSelectedPageMc.selected = False
        self.lastSelectedPageMc = e.currentTarget
        self.lastSelectedPageMc.selected = True
        self.refreshItems()

    def handlePageBtnClick(self, *args):
        e = ASObject(args[3][0])
        page = int(e.currentTarget.idx)
        if page == self.currentPage:
            return
        self.currentPage = page
        if self.lastSelectedPageMc:
            self.lastSelectedPageMc.selected = False
        self.lastSelectedPageMc = e.currentTarget
        self.lastSelectedPageMc.selected = True
        self.refreshItems()

    def getInv(self):
        return BigWorld.player().hierogramBag

    def updateItem(self, page, pos):
        if not self.widget:
            return
        else:
            if page == self.currentPage:
                slotMc = self.widget.shenGeBagSlot.getChildByName('slot%d' % pos)
                slotMc.addEventListener(events.MOUSE_CLICK, self.handlleSlotItemClick, False, 0, True)
                newIcon = self.widget.shenGeBagSlot.getChildByName('newIcon%d' % pos)
                newIcon.visible = False
                if pos >= self.getInv().posCountDict.get(page, 0):
                    slotMc.visible = False
                    return
                slotMc.visible = True
                slotMc.binding = 'runeInv_%d_%d' % (page, pos)
                item = self.getInv().getQuickVal(page, pos)
                itemData = None
                if item:
                    itemData = uiUtils.getGfxItem(item)
                slotMc.setItemSlotData(itemData)
            return

    def handlleSlotItemClick(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            binding = e.currentTarget.binding
            if not binding:
                return
            if not self.uiAdapter.inventory.mediator:
                return
            page, pos = self.getSlotID(binding)
            item = self.getInv().getQuickVal(page, pos)
            if not item:
                return
            hieroType = p.getRuneData(item.id, 'runeType', 0)
            if not hieroType:
                return
            dstPage, desPos = BigWorld.player().inv.searchEmptyInPages()
            if desPos == const.CONT_NO_PAGE or dstPage == const.CONT_NO_POS or not item:
                return
            gamelog.info('jbx:hierogramBag2Inv', page, pos, item.cwrap, dstPage, desPos)
            BigWorld.player().cell.hierogramBag2Inv(page, pos, item.cwrap, dstPage, desPos)

    def refreshItems(self):
        if not self.widget:
            return
        for i in xrange(PAGE_ITEMS_CNT):
            self.updateItem(self.currentPage, i)

        self.refreshSlotEnable()

    def getSlotID(self, key):
        _, page, pos = key.split('_')
        return (int(page), int(pos))

    def getSlotValue(self, movie, idItem, idCon):
        return None

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        if page != uiConst.RUNE_INV_SLOT_PAGE:
            item = self.getInv().getQuickVal(page, pos)
        else:
            item = self.getBagBar().getQuickVal(0, pos)
        if item == None:
            return
        else:
            return tipUtils.getItemTipByLocation(item)

    def getBagBar(self):
        return BigWorld.player().hierogramBagBar

    def getBagSlotData(self):
        container = self.getBagBar()
        dataList = []
        for ps in xrange(container.posCount):
            it = container.getQuickVal(0, ps)
            if it == const.CONT_EMPTY_VAL:
                dataList.append((ps,
                 None,
                 uiConst.ITEM_NORMAL,
                 ''))
                continue
            itemData = uiUtils.getGfxItem(it)
            state = uiConst.ITEM_NORMAL
            dataList.append((ps,
             itemData,
             state,
             itemData['color']))

        return dataList

    def refreshBagSlot(self):
        if not self.widget:
            return
        else:
            value = self.getInv().enabledPackSlotCnt
            for i in xrange(BAG_SOLT_NUM):
                bagSlotMc = self.widget.getChildByName('bagslot%d' % i)
                shineSlotMc = self.widget.getChildByName('shineSlot%d' % i)
                bagSlotMc.bg.lock.visible = i >= value
                bagSlotMc.idx = i
                bagSlotMc.isLocked = i >= value
                bagSlotMc.binding = 'runeInv_%d_%d' % (uiConst.RUNE_INV_SLOT_PAGE, i)
                bagSlotMc.addEventListener(events.MOUSE_CLICK, self.handleBagBarMouseClick, False, 0, True)
                if i >= value:
                    bagSlotMc.bg.gotoAndPlay('bg')
                    if i == value:
                        bagSlotMc.validateNow()
                        TipManager.addTip(bagSlotMc, gameStrings.TEXT_RUNEINVPROXY_324)
                        shineSlotMc.visible = True
                    else:
                        TipManager.removeTip(bagSlotMc)
                        shineSlotMc.visible = False
                else:
                    bagSlotMc.bg.gotoAndPlay('bag' + str(i + 1))
                    TipManager.removeTip(bagSlotMc)
                    shineSlotMc.visible = False

            bagData = self.getBagSlotData()
            for index, data in enumerate(bagData):
                slot = self.widget.getChildByName('bagslot%d' % index)
                if slot:
                    slot.setItemSlotData(data[1])
                    slot.setSlotState(data[2])
                    slot.validateNow()
                else:
                    slot.setItemSlotData(None)

            return

    def handleBagBarMouseClick(self, *args):
        e = ASObject(args[3][0])
        slot = e.target
        expandSlotNum = self.getInv().enabledPackSlotCnt
        if e.currentTarget.isLocked and expandSlotNum == slot.idx:
            self.enlargeSlot(expandSlotNum)
        elif e.buttonIdx == events.RIGHT_BUTTON:
            self.useBarItem(slot.idx)

    def useBarItem(self, slotIdx):
        p = BigWorld.player()
        it = self.getBagBar().getQuickVal(0, slotIdx)
        if it:
            pg, ps = p.searchBestPosInInv(it)
            if ps == const.CONT_NO_POS:
                return
            p.cell.hierogramBagSlot2Inv(slotIdx, it.id, pg, ps)

    def enlargeSlot(self, slotIdx):
        config = SCD.data.get('hierogramBagEnlargeCost', [])
        if len(config) > slotIdx and slotIdx != -1:
            data = config[slotIdx]
            if data != None:
                p = BigWorld.player()
                needBindCash = data[0]
                itemCount = data[1]
                gameglobal.rds.ui.expandPay.bindCash = needBindCash
                if itemCount == 0:
                    gameglobal.rds.ui.expandPay.expandType = uiConst.EXPAND_RUNE_INV_EXPAND
                    self.showPayMessage(needBindCash)
                else:
                    gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_RUNE_INV_EXPAND, slotIdx)

    def showPayMessage(self, needMoney):
        msg = GMD.data.get(GMDD.data.NEED_CONSUME_BINDCASH, {}).get('text', gameStrings.TEXT_INVENTORYPROXY_3159)
        msg = msg % needMoney
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, gameglobal.rds.ui.expandPay.onEnlargeBag)

    def refreshPageCount(self):
        if not self.widget:
            return
        else:
            if self.lastSelectedPageMc:
                self.lastSelectedPageMc.selected = False
                if not self.getInv().posCountDict.get(self.lastSelectedPageMc.idx, 0):
                    self.currentPage = 0
                self.lastSelectedPageMc = None
            for i in self.getInv().getPageTuple():
                pageEnable = bool(self.getInv().posCountDict.get(i, 0))
                eqBtn = self.widget.getChildByName('eqBtn%d' % (i + 1))
                eqBtn.visible = pageEnable
                if pageEnable and i == self.currentPage:
                    eqBtn.selected = True
                    self.lastSelectedPageMc = eqBtn

            return

    def getItemFilterEnable(self, item):
        if not item.isRune():
            return False
        p = BigWorld.player()
        keySet = set()
        for skillId, skillLv in p.getRuneData(item.id, 'pskillList', []):
            key = p.runeTypeMap.get((uiConst.RUNE_EFFECT_TYPE_SKILL, skillId), set())
            if key:
                keySet = keySet | set(key)

        for propId, value in p.getRuneData(item.id, 'props', []):
            key = p.runeTypeMap.get((uiConst.RUNE_EFFECT_TYPE_PROP, propId), set())
            if key:
                keySet = keySet | set(key)

        if self.filterPropId and self.filterPropId not in keySet:
            return False
        if self.filterEffectType:
            if all([ RPPMD.data.get(key, {}).get('typeName', '') != self.filterEffectType for key in keySet ]):
                return False
        if self.searchRange:
            lowSide, highSide = self.searchRange
            addPercent = p.getRuneAddPercent(item)
            return lowSide <= addPercent <= highSide
        return True

    def refreshSlotEnable(self):
        if not self.widget:
            return
        for i in xrange(PAGE_ITEMS_CNT):
            slotMc = self.widget.shenGeBagSlot.getChildByName('slot%d' % i)
            if i >= self.getInv().posCountDict.get(self.currentPage, 0):
                continue
            item = self.getInv().getQuickVal(self.currentPage, i)
            if not item:
                continue
            slotMc.enabled = self.getItemFilterEnable(item)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshPageCount()
        self.refreshItems()
        self.refreshBagSlot()

    def getBagSlotTipData(self, args):
        args = ASObject(args)
        ps = int(args.pos)
        item = self.getBagBar().getQuickVal(0, ps)
        itemData = {}
        if item != const.CONT_EMPTY_VAL:
            itemData = uiUtils.getGfxItem(item)
        return uiUtils.dict2GfxDict(itemData, True)
