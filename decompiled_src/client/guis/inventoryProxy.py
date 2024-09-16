#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/inventoryProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gametypes
import ui
import utils
import tipUtils
import item
import keys
import formula
import gameconfigCommon
import gamelog
from item import Item
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import SlotDataProxy
from guis import cursor
from guis import uiConst
from guis import uiDrag
from guis import uiUtils
from guis import pinyinConvert
from helpers import cellCmd
from callbackHelper import Functor
from helpers.eventDispatcher import Event
from guis import events
from appSetting import Obj as AppSettings
from gameStrings import gameStrings
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import rune_data as RD
from data import item_data as ID
from cdata import font_config_data as FCD
from data import equip_data as ED
from data import item_synthesize_data as ISD
from data import sys_config_data as SYSCD
from data import consumable_item_data as CID
from data import sys_config_data as SCD
from cdata import manual_equip_result_reverse_data as MERRD
from data import mall_category_data as MCD
from data import use_item_wish_data as UIWD
from data import base_card_data as BCD
SWITCH_BIND_TYPE_UNBIND = 0
SWITCH_BIND_TYPE_CHANGE = 1
SORT = 0
SPLIT = 1
TEMP_BAG_CHECKBOX_KEY = keys.SET_UI_INFO + '/tempBagCheckBox'

class InventoryProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(InventoryProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'bag_'
        self.type = 'bagslot'
        self.modelMap = {'getBagSlotBindings': self.onGetBagSlotBindings,
         'closeInventory': self.closeInventory,
         'notifySlotDragEndEx': self.notifySlotDragEndEx,
         'cancelSplit': self.cancelSplit,
         'confirmSplit': self.confirmSplit,
         'confirmDiscard': self.confirmDiscard,
         'cancelDiscard': self.cancelDiscard,
         'playCooldown': self.onPlayCooldown,
         'getinitData': self.onGetinitData,
         'setInvItem': self.onSetInvItem,
         'sendSet': self.onSendSet,
         'isShopShow': self.onIsShopShow,
         'inRepair': self.onInRepair,
         'sellSomeItem': self.onSellSomeItem,
         'sellAllItem': self.onSellAllItem,
         'repair': self.onRepair,
         'clearState': self.onClearState,
         'initBagItem': self.onInitBagItem,
         'initBagBarItem': self.onInitBagBarItem,
         'initTempBagItem': self.onInitTempBagItem,
         'initCommodeBagItem': self.onInitFashionBagItem,
         'pickAllItem': self.onPickAllItem,
         'autoSortInventory': self.onAutoSortInventory,
         'splitItem': self.onSplitItem,
         'disasItem': self.onDisasItem,
         'fitting': self.onFitting,
         'latchCipherItem': self.onLatchCipherItem,
         'latchTimeItem': self.onLatchTimeItem,
         'unlatchItem': self.onUnlatchItem,
         'latchCipher': self.onLatchCipher,
         'latchTime': self.onLatchTime,
         'unlatch': self.onUnlatch,
         'latchCipherSetting': self.onLatchCipherSetting,
         'useAllItem': self.onUseAllItem,
         'isInDragCommonItem': self.onIsInDragCommonItem,
         'useBarItem': self.onUseBarItem,
         'inSplitState': self.onInSplitState,
         'inDisasItem': self.onInDisasItem,
         'inDisassemble': self.onInDisassemble,
         'inUnlatchState': self.onInUnlatchState,
         'inLatchTimeState': self.onInLatchTimeState,
         'inLatchCipherState': self.onInLatchCipherState,
         'splitSlot': self.onSplitSlot,
         'disasSlot': self.onDisasSlot,
         'disassembleSlot': self.onDisassembleSlot,
         'inSynthesizeState': self.onInSynthesizeState,
         'synthesizeDesItem': self.onSynthesizeDesItem,
         'deleteNewIcon': self.onDeleteNewIcon,
         'selectedType': self.onSelectedType,
         'inDyeState': self.onInDyeState,
         'dyeDesItem': self.onDyeDesItem,
         'openCompose': self.onOpenCompose,
         'disassembleItem': self.onDisassembleItem,
         'clickItem': self.onClickItem,
         'openTempBag': self.onOpenTempBag,
         'getTempBagInitData': self.onGetTempBagInitData,
         'initMeterialInvBagItem': self.onInitMaterialBagItem,
         'initMallInvBagItem': self.onInitMallInvBagItem,
         'closeInvTempBag': self.onCloseInvTempBag,
         'arrangeMeterialBag': self.onArrangeMeterialBag,
         'allInv2MaterialBag': self.onAllInv2MaterialBag,
         'clearPassword': self.onClearPassword,
         'enlargeSlot': self.onEnlargeSlot,
         'popWarning': self.onPopWarning,
         'openFashionBag': self.onOpenFashionBag,
         'inChangeOwnerState': self.onInChangeOwnerState,
         'changeOwner': self.onChangeOwner,
         'clearChangeOwnerState': self.resetChangeOwnerState,
         'setNeatenType': self.onSetNeatenType,
         'getNeatenType': self.onGetNeatenType,
         'setCipherType': self.onSetCipherType,
         'setSwitchBindType': self.onSetSwitchBindType,
         'getSwitchBindType': self.onGetSwitchBindType,
         'openUnBindItemWidget': self.onOpenUnBindItemWidget,
         'activeMaterialBag': self.onActiveMaterialBag,
         'getEnableMaterialBag': self.onGetEnableMaterialBag,
         'clearAllBindings': self.onClearAllBindings,
         'changeBind': self.onChangeBind,
         'getItemNames': self.onGetItemNames,
         'getFunctionBtnTips': self.onGetFunctionBtnTips,
         'getSearchItems': self.onGetSearchItems,
         'clearSearchList': self.onClearSearchList,
         'getfrozenPunish': self.onGetfrozenPunish,
         'isEnableCrossBag': self.isEnableCrossBag,
         'openCrossBag': self.onOpenCrossBag,
         'getMeterialBagName': self.onGetMeterialBagName,
         'tempBagCheckBox': self.onTempBagCheckBox,
         'clickYunbiBtn': self.onClickYunbiBtn,
         'clickYunquanBtn': self.onClickYunquanBtn,
         'clickTianbiBtn': self.onClickTianbiBtn,
         'clickYunchuiBtn': self.onClickYunchuiBtn,
         'clickYingLingBtn': self.onClickYingLingBtn,
         'getCfg': self.onGetCfg,
         'getEnableSpriteMaterialBag': self.onGetEnableSpriteMaterialBag,
         'openRuneInv': self.onOpenRuneInv,
         'getEnableRuneInv': self.onGetEnableRuneInv}
        self.page = uiConst.BAG_PAGE_LOW
        self.itemFilter = uiConst.FILTER_ITEM_ALL
        self.mediator = None
        self.dropMBIds = []
        self.numberMediator = None
        self.tempBagMediator = None
        self.isAutoSortInventory = True
        self.isAutoArrangeMaterialBag = True
        self.newItemSequence = []
        self.isSplitState = False
        self.isDisasState = False
        self.isDisassembleState = False
        self.isSynthesizeState = False
        self.isUnlatchState = False
        self.isLatchTimeState = False
        self.isLatchCipherState = False
        self.isState = False
        self.SynthesizeSrcItemId = const.ITEM_NO_ID
        self.SynthesizeSrcItemPage = const.CONT_NO_PAGE
        self.SynthesizeSrcItemPos = const.CONT_NO_POS
        self.isDyeState = False
        self.isSignEquipState = False
        self.isDyePlaneState = False
        self.dyeItemPage = const.CONT_NO_PAGE
        self.dyeItemPos = const.CONT_NO_POS
        self.signItemPage = const.CONT_NO_PAGE
        self.signItemPos = const.CONT_NO_POS
        self.SynthesizeTgtMaterial = ()
        self.filterSubtype = 0
        self.tempBagType = ''
        self.cipherResetTime = 0
        self.invBagSlot = 0
        self.tempBagNum = 0
        self.tempMallBagNum = 0
        self.openWithTemp = None
        self.isChangeOwnerState = False
        self.changeOwnerItemPos = [-1, -1]
        self.nPageSrc = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_INVENTORY, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_NUMBER_VIEW, 'unLoadWidget')
        uiAdapter.registerEscFunc(uiConst.WIDGET_INVENTORY_TEMP_BAG, self.hide)
        self.stateParams = None
        self.containerProxy = None
        self.neatenType = SORT
        self.currentLockType = 0
        self.switchBindType = 1
        self.searchList = []
        self.checkDisableProxys = ['runeLvUp',
         'itemRecast',
         'runeReforging',
         'bindItemTrade',
         'modelFittingRoom',
         'runeForging',
         'guildDonate',
         'consign',
         'mail',
         'guanYinAddSkill',
         'equipFunc',
         'equipFeed',
         'equipEnhance',
         'yaoPeiMix',
         'yaoPeiFeed',
         'yaoPeiTransfer',
         'yaoPeiReforge',
         'wingAndMountUpgrade',
         'roundTable',
         'unBindItem',
         'lottery',
         'equipmentSlot',
         'equipGem',
         'equipMixNew',
         'mixFameJewelry',
         'itemRecall',
         'equipCopy',
         'equipSuit',
         'fireWorkSender',
         'fashionPropTransfer',
         'trade',
         'yaBiao',
         'huiZhangRepair',
         'wishMade',
         'tabAuctionConsign',
         'tabAuctionCrossServer',
         'itemMsgBox',
         'skillAppearanceConfirm',
         'actEffectAppearanceConfirm',
         'randomDye']
        self.checkForbiddenSortProxys = [uiConst.WIDGET_MAIL_BOX,
         uiConst.WIDGET_CONSIGN,
         uiConst.WIDGET_GUILD_DONATE,
         uiConst.WIDGET_EQUIP_ENHANCE,
         uiConst.WIDGET_EQUIP_MIX_NEW,
         uiConst.WIDGET_ITEM_RECAST,
         uiConst.WIDGET_EQUIP_FEED,
         uiConst.WIDGET_EQUIPMENT_SLOT,
         uiConst.WIDGET_EQUIP_GEM_ADD_REMOVE,
         uiConst.WIDGET_TRADE_VIEW,
         uiConst.WIDGET_EQUIP_LV_UP,
         uiConst.WIDGET_ITEM_RECALL,
         uiConst.WIDGET_EXPAND_PAY,
         uiConst.WIDGET_EQUIP_COPY,
         uiConst.WIDGET_FIRE_WORK,
         uiConst.WIDGET_FASHION_PROP_TRANSFER,
         uiConst.WIDGET_WISH_MADE,
         uiConst.WIDGET_TAB_AUCTION,
         uiConst.WIDGET_ITEM_MSG_BOX]

    def setRenewalState(self, page, index):
        self.stateParams = (page, index)
        if self.containerProxy:
            posCount = self.containerProxy.posCountDict.get(self.page, 0)
            for pos in xrange(0, posCount):
                if gameglobal.rds.configData.get('enableFashionBagRenew', False):
                    self.uiAdapter.fashionBag.show()
                self.updateSlotState(self.page, pos)
                self.uiAdapter.roleInfo.show(uiConst.ROLEINFO_TAB_FASHION)
                self.uiAdapter.roleInfo.updateSlotState()

    def onSetNeatenType(self, *args):
        nType = int(args[3][0].GetNumber())
        self.setNeatenType(nType)

    def setNeatenType(self, type):
        self.neatenType = type
        if self.neatenType == SORT:
            self.clearSplitState()
        if self.mediator:
            self.mediator.Invoke('setNeatenType', GfxValue(self.neatenType))

    def onGetNeatenType(self, *args):
        return GfxValue(self.neatenType)

    def onSetCipherType(self, *args):
        type = int(args[3][0].GetNumber())
        self.setCipherType(type)

    def setCipherType(self, type):
        self.currentLockType = type
        if self.mediator:
            self.mediator.Invoke('setCipherType', GfxValue(self.currentLockType))

    def onSetSwitchBindType(self, *args):
        type = int(args[3][0].GetNumber())
        if type == SWITCH_BIND_TYPE_UNBIND and not gameglobal.rds.configData.get('enableUnbindEquip', False):
            self.setSwitchBindType(SWITCH_BIND_TYPE_CHANGE)
            BigWorld.player().showGameMsg(GMDD.data.UNBIND_NOT_OPEN, ())
            return
        self.setSwitchBindType(type)

    def setSwitchBindType(self, type):
        self.switchBindType = type
        if self.mediator:
            self.mediator.Invoke('setSwitchBindType', GfxValue(self.switchBindType))

    def onGetCfg(self, *args):
        data = {}
        data['enableInventoryLock'] = gameglobal.rds.configData.get('enableInventoryLock', False)
        return uiUtils.dict2GfxDict(data, True)

    def onUpdateClientCfg(self):
        if self.mediator:
            self.mediator.Invoke('refreshPanelCfg')

    def onGetSwitchBindType(self, *args):
        if not gameglobal.rds.configData.get('enableUnbindEquip', False):
            self.switchBindType = SWITCH_BIND_TYPE_CHANGE
        return GfxValue(self.switchBindType)

    def disableDisassemble(self):
        if self.mediator:
            self.mediator.Invoke('disableDisassemble')

    def disableUnBind(self):
        if self.switchBindType == SWITCH_BIND_TYPE_UNBIND:
            self.setSwitchBindType(SWITCH_BIND_TYPE_CHANGE)

    def onClearSearchList(self, *args):
        self.searchList = []

    @ui.checkEquipChangeOpen()
    def onOpenUnBindItemWidget(self, *args):
        gameglobal.rds.ui.unBindItem.show()

    def _updateSearchList(self):
        p = BigWorld.player()
        if self.searchList:
            for pg in self.searchList:
                for itemData in pg:
                    it = p.inv.getQuickVal(itemData[0], itemData[1])
                    if it.uuid != itemData[2]:
                        pg.remove(itemData)

    def onGetSearchItems(self, *args):
        name = args[3][0].GetString()
        p = BigWorld.player()
        self.searchList = p.inv.searchAllByName(unicode2gbk(name), self.findItemFunc)
        return uiUtils.array2GfxAarry(self.searchList)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INVENTORY:
            self.mediator = mediator
            self.mediator.SetVisible(True)
            p = BigWorld.player()
            self.containerProxy = p.inv
            BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
            BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)
            self.setNeatenType(self.neatenType)
            self.setCipherType(self.currentLockType)
            self.setSwitchBindType(self.switchBindType)
            if self.openWithTemp is not None:
                self.openTempBagByType(self.openWithTemp)
            self.setBindConfig()
            self.enableInvSearch()
            self.updateFrozenPunishVisible()
        elif widgetId == uiConst.WIDGET_NUMBER_VIEW:
            self.numberMediator = mediator
            if self.whichType in (uiConst.NUMBER_WIDGET_ITEM_TRADE,
             uiConst.NUMBER_WIDGET_ITEM_MAIL,
             uiConst.NUMBER_WIDGET_BIND_ITEM_TRADE,
             uiConst.NUMBER_WIDGET_ITEM_GUILD_DONATE,
             uiConst.NUMBER_WIDGET_WISH_MADE,
             uiConst.NUMBER_WIDGET_RANDOM_DYE):
                i = BigWorld.player().inv.getQuickVal(self.nPage, self.nPos)
                if i:
                    self.numberMediator.Invoke('setText', GfxValue(str(int(i.cwrap))))
        elif widgetId == uiConst.WIDGET_INVENTORY_TEMP_BAG:
            self.tempBagMediator = mediator

    def enableInvSearch(self):
        enableSearch = gameglobal.rds.configData.get('enableInvSearch', False)
        if self.mediator:
            self.mediator.Invoke('enableSearch', GfxValue(enableSearch))

    def setBindConfig(self):
        if self.mediator:
            self.mediator.Invoke('setChangeBindVisible', GfxValue(gameglobal.rds.configData.get('enableBindItemConvert', False)))

    def onItemRemove(self, params):
        self.refreshAllPos(params)

    def onItemChange(self, params):
        self.refreshAllPos(params)

    @ui.uiEvent(uiConst.WIDGET_INVENTORY, events.EVENT_ITEM_CHANGE)
    def onItemChangeNew(self, event):
        if event.data.get('kind') != const.RES_KIND_INV:
            return
        page = event.data.get('page')
        pos = event.data.get('pos')
        itemVal = BigWorld.player().inv.getQuickVal(page, pos)
        if itemVal == const.CONT_EMPTY_VAL:
            return
        key = self._getKey(page, pos)
        if not self.binding.has_key(key):
            return
        self.binding[key][0].Invoke('refreshTip')
        self.updateSlotState(page, pos)

    def refreshAllPos(self, params):
        if params[0] != const.RES_KIND_INV:
            return
        page = params[1]
        if self.page != page:
            return
        posNum = BigWorld.player().inv.posCountDict.get(page, 0)
        for pos in xrange(posNum):
            itemVal = BigWorld.player().inv.getQuickVal(page, pos)
            if itemVal == const.CONT_EMPTY_VAL:
                continue
            key = self._getKey(page, pos)
            if not self.binding.has_key(key):
                continue
            self.binding[key][0].Invoke('refreshTip')
            self.updateSlotState(page, pos)

    def resetLatchCipher(self, *args):
        time = SYSCD.data.get('resetCipherTime', 0)
        timeStr = utils.formatDuration(time)
        msg = gameStrings.TEXT_INVENTORYPROXY_408 % timeStr
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doTrueResetLatchCipher))

    def doTrueResetLatchCipher(self):
        BigWorld.player().base.resetCipher()

    def onSellSomeItem(self, *arg):
        pass

    @ui.checkEquipChangeOpen()
    def onUseBarItem(self, *arg):
        itemId = arg[3][0]
        nPage, nItem = gameglobal.rds.ui.sack.getSlotID(itemId.GetString())
        p = BigWorld.player()
        if nPage == const.BAG_BAR_BIND_ID:
            it = p.bagBar.getQuickVal(0, nItem)
            if it:
                pg, ps = p.searchBestPosInInv(it)
                if ps == const.CONT_NO_POS:
                    return
                p.cell.unequipPack(nItem, pg, ps)
        elif nPage == const.CART_BIND_ID:
            it = p.cart.getQuickVal(0, nItem)
            if it:
                pg, ps = p.searchBestPosInInv(it)
                if ps == const.CONT_NO_POS:
                    return
                p.cell.takeCart(nItem, pg, ps)
        elif nPage == const.MATERIAL_BAG_BIND_ID:
            it = p.materialBag.getQuickVal(0, nItem)
            if it:
                pg, ps = p.searchBestPosInInv(it)
                if ps == const.CONT_NO_POS:
                    p.showGameMsg(GMDD.data.BAG_FULL, ())
                    return
                cellCmd.materialBag2inv(0, nItem, it.cwrap, pg, ps)
        elif nPage == const.FASHION_BAG_BIND_ID:
            it = p.fashionBag.getQuickVal(0, nItem)
            if it:
                pg, ps = p.searchBestPosInInv(it)
                if ps == const.CONT_NO_POS:
                    p.showGameMsg(GMDD.data.BAG_FULL, ())
                    return
                p.cell.fashionBag2inv(0, nItem, it.cwrap, pg, ps)
        elif nPage == const.TEMP_BAG_BIND_ID:
            it = p.tempBag.getQuickVal(0, nItem)
            if it:
                if Item.isQuestItem(it.id):
                    pg, ps = p.questBag.searchBestInPages(it.id, it.cwrap, it)
                    if ps == const.CONT_NO_POS:
                        p.showGameMsg(GMDD.data.BAG_FULL, ())
                        return
                    p.cell.takeTempBagItemToQuestBag(nItem, it.cwrap, pg, ps)
                else:
                    pg, ps = p.searchBestPosInInv(it)
                    if ps == const.CONT_NO_POS:
                        p.showGameMsg(GMDD.data.BAG_FULL, ())
                        return
                    p.cell.takeTempBagItem(nItem, it.cwrap, pg, ps)
        elif nPage == const.MALL_BAR_BIND_ID:
            it = p.mallBag.getQuickVal(0, nItem)
            if it:
                pg, ps = p.searchBestPosInInv(it)
                if ps == const.CONT_NO_POS:
                    p.showGameMsg(GMDD.data.BAG_FULL, ())
                    return
                p.cell.takeMallBagItem(nItem, pg, ps)

    def isInDragCommonItem(self):
        return gameglobal.rds.ui.inDragStorageItem or gameglobal.rds.ui.inDragCommonItem or gameglobal.rds.ui.inDragFashionBagItem or gameglobal.rds.ui.inDragMaterialBagItem or gameglobal.rds.ui.inDragSpriteMaterialBagItem or gameglobal.rds.ui.inDragRuneInvItem

    def onIsInDragCommonItem(self, *arg):
        return GfxValue(self.isInDragCommonItem())

    def onUseAllItem(self, *arg):
        itemId = arg[3][0]
        nPage, nItem = self.getSlotID(itemId.GetString())
        if nPage == uiConst.BAG_PAGE_QUEST:
            return
        BigWorld.player().batchUseBagItem(nPage, nItem)

    def onClearAllBindings(self, *arg):
        self.binding = {}

    def onDeleteNewIcon(self, *arg):
        itemId = arg[3][0]
        page, pos = self.getSlotID(itemId.GetString())
        self._removeNewItemSequence(page, pos)

    def setAutoSortAble(self, isEnable):
        self.isAutoSortInventory = isEnable
        if self.mediator:
            self.mediator.Invoke('setNeatenBtnEnable', GfxValue(isEnable))

    @ui.checkEquipChangeOpen()
    def onAutoSortInventory(self, *arg):
        p = BigWorld.player()
        if self.isDyePlaneState:
            p.showGameMsg(GMDD.data.ITEM_TRADE_FORBIDDEN_SORT, ())
            return
        for widgetId in self.checkForbiddenSortProxys:
            isWidgetLoaded = gameglobal.rds.ui.isWidgetLoaded(widgetId)
            if isWidgetLoaded:
                p.showGameMsg(GMDD.data.ITEM_TRADE_FORBIDDEN_SORT, ())
                return

        state_arr = [ui.SIGNEQUIP_STATE,
         ui.RENEWAL_STATE,
         ui.IDENTIFY_ITEM_STATE,
         ui.IDENTIFY_MANUAL_EQUIP_STATE,
         ui.CHANGE_BIND_STATE,
         ui.RENEWAL_STATE2,
         ui.RESET_FASHION_PROP]
        if ui.get_cursor_state() in state_arr:
            p.showGameMsg(GMDD.data.ITEM_TRADE_FORBIDDEN_SORT, ())
            return
        if gameglobal.rds.ui.runeLvUp.mediator:
            if gameglobal.rds.ui.runeLvUp.pageType == 'runeLvUp':
                p.showGameMsg(GMDD.data.RUNE_LVUP_FORBIDDEN_SORT, ())
            elif gameglobal.rds.ui.runeLvUp.pageType == 'yinyangGem':
                p.showGameMsg(GMDD.data.GEM_RUNE_LVUP_FORBIDDEN_SORT, ())
            return
        if gameglobal.rds.ui.runeForging.invPos == const.CONT_NO_POS and gameglobal.rds.ui.runeReforging.invPos == const.CONT_NO_POS:
            if p.stateMachine.checkStatus(const.CT_SORT_INV):
                p.cell.autoSortInv()
                self.setAutoSortAble(False)
                BigWorld.callback(SYSCD.data.get('autoSortInvCD', 30), Functor(self.setAutoSortAble, True))
        else:
            p.showGameMsg(GMDD.data.ITEM_ENHANCE_FORBIDDEN_SORT, ())

    @ui.checkEquipChangeOpen()
    def onSplitItem(self, *arg):
        if self.isSplitState:
            self.clearSplitState()
        else:
            self.setSplitState()

    @ui.checkEquipChangeOpen()
    def onDisasItem(self, *arg):
        if self.isDisasState:
            self.clearDisasState()
        else:
            self.setDisasState()

    @ui.checkEquipChangeOpen()
    def onChangeBind(self, *args):
        gameglobal.rds.ui.clearState()
        if ui.get_cursor_state() != ui.CHANGE_BIND_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.CHANGE_BIND_STATE)
            ui.set_cursor(cursor.changeBind)
            ui.lock_cursor()
        self.updateCurrentPageSlotState()

    def setPassWord(self):
        gameglobal.rds.ui.inventorySetPassword.show()

    @ui.checkEquipChangeOpen()
    def onLatchCipherItem(self, *arg):
        if self.currentLockType == 0:
            if not BigWorld.player().hasInvPassword:
                gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_INVENTORYPROXY_576, self.setPassWord)
            elif self.isLatchCipherState:
                self.clearLatchCipherState()
            else:
                self.clearState()
                self.setLatchCipherState()
        else:
            self.onLatchTimeItem()

    def onLatchTimeItem(self, *arg):
        if self.isLatchTimeState:
            self.clearLatchTimeState()
        else:
            self.clearState()
            self.setLatchTimeState()

    def onUnlatchItem(self, *arg):
        if self.isUnlatchState:
            self.clearUnlatchState()
        else:
            self.setUnlatchState()

    @ui.callFilter(1, True)
    def onLatchCipher(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if page == uiConst.BAG_PAGE_QUEST:
            return
        itemVal = BigWorld.player().inv.getQuickVal(page, pos)
        if not itemVal:
            return
        if not itemVal.hasLatch():
            BigWorld.player().cell.latchCipher(const.LATCH_ITEM_INV, page, pos)
        else:
            uiUtils.unLatchItem(itemVal, const.LATCH_ITEM_INV, page, pos)

    def onLatchTime(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if page == uiConst.BAG_PAGE_QUEST:
            return
        itemVal = BigWorld.player().inv.getQuickVal(page, pos)
        if not itemVal:
            return
        if not itemVal.canLatch():
            BigWorld.player().showGameMsg(GMDD.data.LATCH_FORBIDDEN_NO_LATCH, ())
            return
        gameglobal.rds.ui.inventoryLatchTime.show(const.LATCH_ITEM_INV, page, pos)
        self.clearLatchTimeState()

    def onUnlatch(self, *arg):
        p = BigWorld.player()
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if page == uiConst.BAG_PAGE_QUEST:
            return
        sItem = p.inv.getQuickVal(page, pos)
        if not sItem:
            return
        if not sItem.hasLatch():
            self.clearUnlatchState()
            return
        if sItem.isLatchOfTime():
            p.cell.unLatchTime(const.LATCH_ITEM_INV, page, pos)
        else:
            gameglobal.rds.ui.inventoryPassword.show(const.LATCH_ITEM_INV, page, pos)
        self.clearUnlatchState()

    def onLatchCipherSetting(self, *arg):
        p = BigWorld.player()
        if not p.hasInvPassword:
            gameglobal.rds.ui.inventorySetPassword.show()
        else:
            gameglobal.rds.ui.inventoryResetPassword.show()

    def onGetHasInvPassWord(self, *args):
        p = BigWorld.player()
        if getattr(p, 'cipherResetTime', 0):
            return GfxValue(False)
        else:
            return GfxValue(p.hasInvPassword)

    def setHasPassword(self, hasPassWorld):
        if self.mediator:
            self.mediator.Invoke('setInventoryLatchTip', GfxValue(hasPassWorld))

    def onClearState(self, *arg):
        gameglobal.rds.ui.clearState()

    def clearState(self):
        self.clearCommonState()
        self.clearSynthesizeState()
        self.clearDisasState()
        self.clearDyeState()
        self.clearSplitState()
        self.clearLatchCipherState()
        self.clearLatchTimeState()
        self.clearUnlatchState()
        self.clearSignEquipState()
        self.clearChangeOwnerState()
        self.clearDisassembleState()

    def clearCommonState(self):
        self.stateParams = None
        if ui.get_cursor_state() == ui.CHANGE_BIND_STATE:
            ui.reset_cursor()
        self.updateCurrentPageSlotState()

    def clearSignEquipState(self):
        if self.isSignEquipState:
            self.isSignEquipState = False
            self.updateCurrentPageSlotState()
            self.uiAdapter.roleInfo.updateSlotState()
            self.signItemPage = const.CONT_NO_PAGE
            self.signItemPos = const.CONT_NO_POS

    def setUnlatchState(self):
        self.uiAdapter.clearState()
        self.isUnlatchState = True
        if ui.get_cursor_state() != ui.UNLATCH_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.UNLATCH_STATE)
            ui.set_cursor(cursor.unlock)
            ui.lock_cursor()

    def clearUnlatchState(self):
        if self.isUnlatchState:
            self.isUnlatchState = False
            if ui.get_cursor_state() == ui.UNLATCH_STATE:
                ui.reset_cursor()

    def setLatchTimeState(self):
        self.uiAdapter.clearState()
        self.isLatchTimeState = True
        if ui.get_cursor_state() != ui.LATCH_TIME_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.LATCH_TIME_STATE)
            ui.set_cursor(cursor.timelock)
            ui.lock_cursor()

    def clearLatchTimeState(self):
        if self.isLatchTimeState:
            self.isLatchTimeState = False
            if ui.get_cursor_state() == ui.LATCH_TIME_STATE:
                ui.reset_cursor()

    def setLatchCipherState(self):
        self.uiAdapter.clearState()
        self.isLatchCipherState = True
        if ui.get_cursor_state() != ui.LATCH_CIPHER_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.LATCH_CIPHER_STATE)
            ui.set_cursor(cursor.cipherlock)
            ui.lock_cursor()

    def clearLatchCipherState(self):
        if self.isLatchCipherState:
            self.isLatchCipherState = False
            if ui.get_cursor_state() == ui.LATCH_CIPHER_STATE:
                ui.reset_cursor()

    def setSplitState(self):
        self.uiAdapter.clearState()
        self.isSplitState = True
        if ui.get_cursor_state() != ui.SPLIT_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.SPLIT_STATE)
            ui.set_cursor(cursor.splitItem)
            ui.lock_cursor()

    def clearSplitState(self):
        if self.isSplitState:
            self.isSplitState = False
            if ui.get_cursor_state() == ui.SPLIT_STATE:
                ui.reset_cursor()

    def setDisasState(self):
        self.uiAdapter.clearState()
        self.isDisasState = True
        if ui.get_cursor_state() != ui.DISAS_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.DISAS_STATE)
            ui.set_cursor(cursor.decompose)
            ui.lock_cursor()
            self.updateCurrentPageSlotState()

    def clearDisasState(self):
        if self.isDisasState:
            self.isDisasState = False
            if ui.get_cursor_state() == ui.DISAS_STATE:
                ui.reset_cursor()
            self.updateCurrentPageSlotState()

    def setDisassembleState(self):
        self.uiAdapter.clearState()
        self.isDisassembleState = True
        if ui.get_cursor_state() != ui.DISASSEMBLE_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.DISASSEMBLE_STATE)
            ui.set_cursor(cursor.disassemble)
            ui.lock_cursor()
        self.updateCurrentPageSlotState()

    def clearDisassembleState(self):
        if self.isDisassembleState:
            self.isDisassembleState = False
            if ui.get_cursor_state() == ui.DISASSEMBLE_STATE:
                ui.reset_cursor()
            self.updateCurrentPageSlotState()

    def setSignEquipState(self, page, index):
        p = BigWorld.player()
        self.isSignEquipState = True
        posCount = p.inv.posCountDict.get(self.page, 0)
        self.signItemPage = page
        self.signItemPos = index
        for pos in xrange(0, posCount):
            self.updateSlotState(self.page, pos)

    def setChangeOwnerState(self, page, index):
        p = BigWorld.player()
        self.isChangeOwnerState = True
        self.changeOwnerItemPos[0] = page
        self.changeOwnerItemPos[1] = index
        if ui.get_cursor_state() != ui.CHANGE_OWNER_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.CHANGE_OWNER_STATE)
            ui.set_cursor(cursor.changeOwner)
            ui.lock_cursor()
        posCount = p.inv.posCountDict.get(self.page, 0)
        for pos in xrange(0, posCount):
            self.updateSlotState(self.page, pos)

    def clearChangeOwnerState(self):
        if self.isChangeOwnerState:
            self.isChangeOwnerState = False
            if ui.get_cursor_state() == ui.CHANGE_OWNER_STATE:
                ui.reset_cursor()
            self.updateCurrentPageSlotState()

    def resetChangeOwnerState(self, *arg):
        self.clearChangeOwnerState()

    def setIdentifyState(self, page, index):
        p = BigWorld.player()
        posCount = p.inv.posCountDict.get(self.page, 0)
        self.stateParams = (page, index)
        for pos in xrange(0, posCount):
            self.updateSlotState(self.page, pos)

    def setDyeState(self, fashionFirst = True):
        self.uiAdapter.clearState()
        self.isDyeState = True
        if ui.get_cursor_state() != ui.DYE_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.DYE_STATE)
            ui.set_cursor(cursor.dye)
            ui.lock_cursor()
        p = BigWorld.player()
        posCount = p.inv.posCountDict.get(self.page, 0)
        for pos in xrange(0, posCount):
            if not (self.dyeItemPage == self.page and self.dyeItemPos == pos):
                self.updateSlotState(self.page, pos)

        if not self.uiAdapter.roleInfo.isShow:
            if fashionFirst and self.uiAdapter.roleInfo.isFashionCanDye():
                self.uiAdapter.roleInfo.show(uiConst.ROLEINFO_TAB_FASHION)
            else:
                self.uiAdapter.roleInfo.show()
        self.uiAdapter.roleInfo.updateSlotState()

    def clearDyeState(self):
        if self.isDyeState:
            self.isDyeState = False
            if ui.get_cursor_state() == ui.DYE_STATE:
                ui.reset_cursor()
            self.dyeItemPage = const.CONT_NO_PAGE
            self.dyeItemPos = const.CONT_NO_POS
            self.updateCurrentPageSlotState()
            self.uiAdapter.roleInfo.updateSlotState()
            self.uiAdapter.dyeColor.hide()

    def setDyePlaneState(self):
        self.clearState()
        self.isDyePlaneState = True
        p = BigWorld.player()
        posCount = p.inv.posCountDict.get(self.page, 0)
        for pos in xrange(0, posCount):
            if not (self.dyeItemPage == self.page and self.dyeItemPos == pos):
                self.updateSlotState(self.page, pos)

    def clearDyePlaneState(self):
        if self.isDyePlaneState:
            self.isDyePlaneState = False
            self.updateCurrentPageSlotState()

    def setSynthesizeState(self):
        self.uiAdapter.clearState()
        self.isSynthesizeState = True
        if ui.get_cursor_state() != ui.SYNTHESIZE_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.SYNTHESIZE_STATE)
            ui.set_cursor(cursor.pickup)
            ui.lock_cursor()

    def clearSynthesizeState(self):
        if self.isSynthesizeState:
            self.isSynthesizeState = False
            if ui.get_cursor_state() == ui.SYNTHESIZE_STATE:
                ui.reset_cursor()
            self.SynthesizeSrcItemId = const.ITEM_NO_ID
            self.SynthesizeSrcItemPage = const.CONT_NO_PAGE
            self.SynthesizeSrcItemPos = const.CONT_NO_POS
            self.SynthesizeTgtMaterial = ()
            self.updateCurrentPageSlotState()

    def setFilterBySubtype(self, filterSubtype):
        self.filterSubtype = filterSubtype
        self.updateCurrentPageSlotState()

    def onFitting(self, *arg):
        key = arg[3][0].GetString()
        nPage, nItem = self.getSlotID(key)
        if nPage != uiConst.BAG_PAGE_QUEST:
            BigWorld.player().previewBagItem(nPage, nItem)

    def onChangeOwner(self, *arg):
        p = BigWorld.player()
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if page == uiConst.BAG_PAGE_QUEST:
            return
        sItem = p.inv.getQuickVal(page, pos)
        if not sItem:
            return
        if self.isChangeOwnerState and sItem.type == Item.BASETYPE_EQUIP_GEM and not sItem.ownedBy(BigWorld.player().gbId):
            BigWorld.player().cell.occupyEquipGem(const.RES_KIND_INV, self.changeOwnerItemPos[0], self.changeOwnerItemPos[1], page, pos)
            self.clearChangeOwnerState()

    def onSplitSlot(self, *arg):
        itemId = arg[3][0]
        p = BigWorld.player()
        self.nPageSrc, self.nItemSrc = self.getSlotID(itemId.GetString())
        if self.nPageSrc == uiConst.BAG_PAGE_QUEST:
            itemVal = p.questBag.getQuickVal(0, self.nItemSrc)
            if itemVal != const.CONT_EMPTY_VAL:
                p.showGameMsg(GMDD.data.QUEST_ITEM_SPLIT_FORBIDDEN, ())
            return
        self.nPageDes, self.nItemDes = p.inv.searchEmptyInPages()
        if self.nItemDes == const.CONT_NO_POS:
            p.showGameMsg(GMDD.data.ITEM_SPLIT_FORBIDDEN_POS, ())
            return
        sItem = p.inv.getQuickVal(self.nPageSrc, self.nItemSrc)
        if not sItem:
            return
        if not sItem.isWrap():
            p.showGameMsg(GMDD.data.ITEM_SPLIT_FORBIDDEN_LESS, ())
            return
        if sItem.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        if gameglobal.rds.ui.trade.isShow:
            p.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
            return
        self.showNumberInputWidget(uiConst.NUMBER_WIDGET_SPLIT)
        self.clearSplitState()

    def onPickAllItem(self, *arg):
        id = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if id == const.CART_BIND_ID:
            p.cell.takeAllCart()
        if id == const.TEMP_BAG_BIND_ID:
            p.cell.takeAllTempBagItem()
        elif id == const.MATERIAL_BAG_BIND_ID:
            p.cell.allMaterialBag2inv()
        elif id == const.FASHION_BAG_BIND_ID:
            p.cell.allFashionBag2inv()
        elif id == const.MALL_BAR_BIND_ID:
            p.cell.takeAllMallBagItem()

    def onSellAllItem(self, *arg):
        itemId = arg[3][0]
        nPage, nItem = self.getSlotID(itemId.GetString())
        if nPage == uiConst.BAG_PAGE_QUEST:
            i = BigWorld.player().questBag.getQuickVal(0, nItem)
        else:
            i = BigWorld.player().inv.getQuickVal(nPage, nItem)
        if i == const.CONT_EMPTY_VAL:
            return
        if i.isRuneHasRuneData():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_SELL_RUNE_EQUIP, ())
            return
        if not i.canSell(shopType=BigWorld.player().openShopType, compositeShopId=BigWorld.player().openShopId):
            BigWorld.player().showGameMsg(GMDD.data.SHOP_CANNOT_BUYBACK, ())
            return
        if i.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        msg = ''
        msgId = 0
        if i.hasGem():
            msgId = GMDD.data.EQUIP_CAN_NOT_SELL_WITH_GEM
        elif i.isGuanYin() and len(i.getAllGuanYinPskill()) > 0:
            msgId = GMDD.data.GUAN_YIN_SALE_HINT
        elif i.isRuneEquip() and getattr(i, 'runeData', ()):
            msgId = GMDD.data.EQUIP_SELL_RUNE
        if i.isEquip() and getattr(i, 'enhLv', 0) and i.quality >= uiConst.DISAS_MESSAGEBOX_QUALITY:
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_SELL_QUALITY_AND_ENHLV, gameStrings.TEXT_INVENTORYPROXY_1016)
        elif i.sellWithConfirm() and i.quality >= uiConst.DISAS_MESSAGEBOX_QUALITY:
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_SELL_QUALITY, gameStrings.TEXT_INVENTORYPROXY_1018)
        elif i.isEquip() and getattr(i, 'enhLv', 0):
            msg = uiUtils.getTextFromGMD(GMDD.data.EQUIP_SELL_ENHLV, gameStrings.TEXT_INVENTORYPROXY_1020)
        if msgId != 0:
            p = BigWorld.player()
            p.showGameMsg(msgId, ())
        elif msg != '':
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.sellConfirm, nPage, nItem))
        else:
            self.sellConfirm(nPage, nItem)

    def sellConfirm(self, nPage, nItem):
        if nPage == uiConst.BAG_PAGE_QUEST:
            i = BigWorld.player().questBag.getQuickVal(0, nItem)
        else:
            i = BigWorld.player().inv.getQuickVal(nPage, nItem)
        if i is None:
            return
        else:
            compositeShopInfo = getattr(i, 'compositeShopInfo', None)
            noReturn = utils.getItemNoReturn(ID.data.get(i.id, {}))
            if not noReturn and compositeShopInfo and utils.getNow() - compositeShopInfo[0] < SYSCD.data.get('timeToReturnShop', 600):
                msg = GMD.data.get(GMDD.data.CONFIRM_SELL_SHOP_NOTIFY, {}).get('text', '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doSellItem, i, nPage, nItem))
            else:
                self.doSellItem(i, nPage, nItem)
            return

    def doSellItem(self, item, nPage, nItem):
        if item and BigWorld.player().openShopId:
            npc = BigWorld.entities.get(gameglobal.rds.ui.shop.npcId)
            npc and npc.cell.buy(BigWorld.player().openShopId, nPage, nItem, item.cwrap)
            gameglobal.rds.sound.playSound(gameglobal.SD_401)

    def onInUnlatchState(self, *arg):
        return GfxValue(self.isUnlatchState)

    def onInLatchTimeState(self, *arg):
        return GfxValue(self.isLatchTimeState)

    def onInLatchCipherState(self, *arg):
        return GfxValue(self.isLatchCipherState)

    def onInSplitState(self, *arg):
        return GfxValue(self.isSplitState)

    def onInDisasItem(self, *arg):
        return GfxValue(self.isDisasState)

    def onInDisassemble(self, *arg):
        return GfxValue(self.isDisassembleState)

    def onInSynthesizeState(self, *arg):
        return GfxValue(self.isSynthesizeState)

    def onInChangeOwnerState(self, *arg):
        return GfxValue(self.isChangeOwnerState)

    def onSynthesizeDesItem(self, *arg):
        if self.isSynthesizeState:
            itemId = arg[3][0]
            nPage, nItem = self.getSlotID(itemId.GetString())
            p = BigWorld.player()
            i = p.inv.getQuickVal(nPage, nItem)
            if i == const.CONT_EMPTY_VAL:
                return
            if i.getParentId() in self.SynthesizeTgtMaterial:
                p.useSynthesizeItem(self.SynthesizeSrcItemPage, self.SynthesizeSrcItemPos)
                self.clearSynthesizeState()

    def onGetItemNames(self, *arg):
        p = BigWorld.player()
        text = unicode2gbk(arg[3][0].GetString())
        ret = []
        if text == '':
            return uiUtils.array2GfxAarry(ret)
        text = text.lower()
        searchList = p.inv.searchAllByName(text, self.findItemFunc)
        for pg in searchList:
            for itemData in pg:
                it = p.inv.getQuickVal(itemData[0], itemData[1])
                name = gbk2unicode(it.name)
                if name not in ret:
                    ret.append(gbk2unicode(it.name))

        return uiUtils.array2GfxAarry(ret)

    def findItemFunc(self, itemName, name):
        find = False
        isPinyinAndHanzi = utils.isPinyinAndHanzi(name)
        if isPinyinAndHanzi == const.STR_ONLY_PINYIN:
            itemName2 = pinyinConvert.strPinyinFirst(itemName)
            find = itemName2.find(name) != -1
        else:
            find = itemName.lower().find(name.lower()) != -1
        return find

    def onDisasSlot(self, *arg):
        if self.isDisasState:
            itemId = arg[3][0]
            nPage, nItem = self.getSlotID(itemId.GetString())
            p = BigWorld.player()
            if nPage == uiConst.BAG_PAGE_QUEST:
                itemVal = p.questBag.getQuickVal(0, nItem)
                if itemVal != const.CONT_EMPTY_VAL:
                    p.showGameMsg(GMDD.data.DISAS_TYPE_FORBIDDEN, ())
                return
            i = p.inv.getQuickVal(nPage, nItem)
            if i == const.CONT_EMPTY_VAL:
                return
            if i.canDisass():
                needMsgBox = False
                if i.quality >= uiConst.DISAS_MESSAGEBOX_QUALITY:
                    needMsgBox = True
                    if i.isYaoPei() and getattr(i, 'yaoPeiExp', 0) > 0:
                        msg = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_DISASSEMBLE_QUALITY_AND_EXP_HINT, '')
                    else:
                        msg = gameStrings.TEXT_INVENTORYPROXY_1139
                elif i.isEquip() and getattr(i, 'enhLv', 0):
                    needMsgBox = True
                    msg = gameStrings.TEXT_INVENTORYPROXY_1143
                elif i.isYaoPei() and getattr(i, 'yaoPeiExp', 0) > 0:
                    needMsgBox = True
                    msg = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_DISASSEMBLE_EXP_HINT, '')
                elif i.isRuneEquip() and getattr(i, 'runeData', ()):
                    needMsgBox = True
                    msg = gameStrings.TEXT_INVENTORYPROXY_1151
                if needMsgBox:
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.disasConfirm, nPage, nItem))
                else:
                    self._disasConfirm(nPage, nItem)
                return
            p.showGameMsg(GMDD.data.DISAS_TYPE_FORBIDDEN, ())

    def disasConfirm(self, nPage, nItem):
        self._disasConfirm(nPage, nItem)

    def _disasConfirm(self, nPage, nItem):
        p = BigWorld.player()
        i = p.inv.getQuickVal(nPage, nItem)
        if i == const.CONT_EMPTY_VAL:
            return
        cidData = CID.data.get(i.id, {})
        sType = cidData.get('sType', 0)
        if sType == Item.SUBTYPE_2_CARD:
            cardId = CID.data.get(i.id, {}).get('cardId', 0)
            cardObj = p.getCard(cardId, True)
            disasType = BCD.data.get(cardId, {}).get('disasType', 0)
            if disasType == const.CARD_DISAS_TYPE_COMMON:
                p.cell.disassembleItem(nPage, nItem)
            else:
                recommendLv = cardObj.advanceLv
                curRate = cardObj.getDecomponseRate(cardObj.advanceLv, cardObj.actived)
                for i in xrange(cardObj.advanceLv, const.CARD_MAX_RANK + 1):
                    rate = cardObj.getDecomponseRate(i, True)
                    if rate > curRate:
                        recommendLv = i
                        break

                if recommendLv > cardObj.advanceLv:
                    self.uiAdapter.messageBox.showYesNoMsgBox(gameStrings.CARD_DISAS_CARD_ITEM % (recommendLv, recommendLv), yesCallback=Functor(p.cell.useCommonItemWithParam, nPage, nItem, 'behavior', const.CARD_ITEM_BEHAVIOR_DECOMPOSE))
                else:
                    p.cell.useCommonItemWithParam(nPage, nItem, 'behavior', const.CARD_ITEM_BEHAVIOR_DECOMPOSE)
        else:
            p.cell.disassembleItem(nPage, nItem)

    def onDisassembleSlot(self, *arg):
        if self.isDisassembleState:
            itemId = arg[3][0]
            nPage, nItem = self.getSlotID(itemId.GetString())
            p = BigWorld.player()
            if nPage == uiConst.BAG_PAGE_QUEST:
                itemVal = p.questBag.getQuickVal(0, nItem)
                if itemVal != const.CONT_EMPTY_VAL:
                    p.showGameMsg(GMDD.data.DISASSEMBLE_TYPE_FORBIDDEN, ())
                return
            i = p.inv.getQuickVal(nPage, nItem)
            if i == const.CONT_EMPTY_VAL:
                return
            if i.canDisassemble():
                if i.hasLatch():
                    p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                if i.hasGem():
                    p.showGameMsg(GMDD.data.DISASSEMBLE_FAIL_HAS_GEM, ())
                    return
                p.cell.disassembleEquip(nPage, nItem)
                return
            p.showGameMsg(GMDD.data.DISASSEMBLE_TYPE_FORBIDDEN, ())

    def onInDyeState(self, *arg):
        return GfxValue(self.isDyeState)

    def doIdentifyEquip(self, nPage, nItem):
        p = BigWorld.player()
        if nPage == uiConst.BAG_PAGE_QUEST:
            i = BigWorld.player().questBag.getQuickVal(0, nItem)
        elif nPage == const.INV_PAGE_EQUIP:
            i = p.equipment.get(nItem)
        else:
            i = BigWorld.player().inv.getQuickVal(nPage, nItem)
        if i:
            if i.hasLatch():
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
        else:
            return
        identifyItem = p.inv.getQuickVal(self.stateParams[0], self.stateParams[1])
        if not identifyItem or identifyItem.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        tgtItem = p.inv.getQuickVal(nPage, nItem)
        if identifyItem.isForeverBind() and not tgtItem.isForeverBind():
            msg = GMD.data.get(GMDD.data.IDENTIFY_EQUIP_BIND, {}).get('text', gameStrings.TEXT_INVENTORYPROXY_1252)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.identifyManualEquip, self.stateParams[0], self.stateParams[1], nPage, nItem))
        else:
            p.cell.identifyManualEquip(self.stateParams[0], self.stateParams[1], nPage, nItem)
        gameglobal.rds.ui.clearState()

    def doIdentifyItem(self, nPage, nItem):
        p = BigWorld.player()
        if nPage == uiConst.BAG_PAGE_QUEST:
            i = BigWorld.player().questBag.getQuickVal(0, nItem)
        elif nPage == const.INV_PAGE_EQUIP:
            i = p.equipment.get(nItem)
        else:
            i = BigWorld.player().inv.getQuickVal(nPage, nItem)
        if i:
            if i.hasLatch():
                p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
        else:
            return
        identifyItem = p.inv.getQuickVal(self.stateParams[0], self.stateParams[1])
        if identifyItem.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        if not i.canBeIdentified():
            return
        if getattr(identifyItem, 'cstype', 0) != item.Item.SUBTYPE_2_LIFE_SKILL_ITEM_IDENTIFY:
            return
        identifyType = CID.data.get(identifyItem.id, {}).get('identifyType', -1)
        if i.getIdentifyType() == identifyType:
            name = uiUtils.getItemColorName(i.id)
            identifyName = uiUtils.getItemColorName(identifyItem.id)
            desc = gameStrings.TEXT_INVENTORYPROXY_1284 % (name, identifyName)
            self.uiAdapter.messageBox.showYesNoMsgBox(desc, Functor(self.onRealIdentify, self.stateParams[0], self.stateParams[1], nPage, nItem, const.RES_KIND_INV), gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)
            gameglobal.rds.ui.clearState()

    def onRealIdentify(self, srcPage, srcPos, tgtPage, tgtPos, resKind):
        BigWorld.player().cell.identifyItem(tgtPage, tgtPos, srcPage, srcPos)

    def doAddStarExp(self, resKind, tgtPage, tgtPos):
        p = BigWorld.player()
        if resKind == const.RES_KIND_INV:
            i = p.inv.getQuickVal(tgtPage, tgtPos)
        elif resKind == const.RES_KIND_EQUIP:
            i = p.equipment.get(tgtPos)
        else:
            i = const.CONT_EMPTY_VAL
        if not i:
            return
        if i.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        if not i.canUseAddStarExpItem():
            p.showGameMsg(GMDD.data.ADD_STAR_EXP_FAIL_ITEM, ())
            return
        starExp = getattr(i, 'starExp', 0)
        toTopExp = i._getEquipStarExpCeil()
        if starExp >= toTopExp:
            p.showGameMsg(GMDD.data.ADD_STAR_EXP_FAIL_EXP_MAX, ())
            return
        itemPos = ui.get_bindItemPos()
        addExpItem = p.inv.getQuickVal(itemPos[1], itemPos[2])
        if not addExpItem:
            return
        if addExpItem.isEquipStarExpItem():
            disassembleStarExp = CID.data.get(addExpItem.id, {}).get('equipStarExp', 0)
        else:
            disassembleStarExp = getattr(addExpItem, 'disassembleStarExp', 0)
        if starExp + disassembleStarExp > toTopExp:
            overflow = True
        else:
            overflow = False
        if not i.isForeverBind() and addExpItem.isForeverBind():
            changeToBind = True
        else:
            changeToBind = False
        needMsgBox = False
        if changeToBind and overflow:
            needMsgBox = True
            msg = uiUtils.getTextFromGMD(GMDD.data.ADD_STAR_EXP_UNBIND_AND_OVERFLOW_HINT, gameStrings.TEXT_INVENTORYPROXY_1339)
        elif changeToBind:
            needMsgBox = True
            msg = uiUtils.getTextFromGMD(GMDD.data.ADD_STAR_EXP_UNBIND_HINT, gameStrings.TEXT_INVENTORYPROXY_1343)
        elif overflow:
            needMsgBox = True
            msg = uiUtils.getTextFromGMD(GMDD.data.ADD_STAR_EXP_OVERFLOW_HINT, gameStrings.TEXT_INVENTORYPROXY_1347)
        if needMsgBox:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.useItemOfEquipStarExp, itemPos[1], itemPos[2], resKind, tgtPage, tgtPos))
        else:
            p.cell.useItemOfEquipStarExp(itemPos[1], itemPos[2], resKind, tgtPage, tgtPos)
        gameglobal.rds.ui.clearState()

    def doRenewerItem(self, nPage, nItem):
        p = BigWorld.player()
        if nPage == uiConst.BAG_PAGE_QUEST:
            i = BigWorld.player().questBag.getQuickVal(0, nItem)
        elif nPage == const.INV_PAGE_EQUIP:
            i = p.equipment.get(nItem)
        else:
            i = BigWorld.player().inv.getQuickVal(nPage, nItem)
        if i == const.CONT_EMPTY_VAL:
            return
        elif i.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        else:
            renewalItem = p.inv.getQuickVal(self.stateParams[0], self.stateParams[1])
            if renewalItem:
                if renewalItem.hasLatch():
                    p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
            else:
                return
            if not i.canRenewalIndependent():
                p.showGameMsg(GMDD.data.ITEM_CAN_NOT_RENEWAL, ())
                return
            elif getattr(renewalItem, 'cstype', 0) != item.Item.SUBTYPE_2_ITEM_RENEWAL:
                return
            renewalType = CID.data.get(renewalItem.id, {}).get('renewalType', -1)
            if i.getRenewalType() == renewalType:
                name = uiUtils.getItemColorName(i.id)
                renewalItemName = uiUtils.getItemColorName(renewalItem.id)
                desc = gameStrings.TEXT_FASHIONBAGPROXY_126 % (name, renewalItemName)
                if nPage == const.INV_PAGE_EQUIP:
                    self.uiAdapter.messageBox.showYesNoMsgBox(desc, Functor(self.onRealResume, self.stateParams[0], self.stateParams[1], nPage, nItem, const.RES_KIND_EQUIP), gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)
                else:
                    self.uiAdapter.messageBox.showYesNoMsgBox(desc, Functor(self.onRealResume, self.stateParams[0], self.stateParams[1], nPage, nItem, const.RES_KIND_INV), gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)
                gameglobal.rds.ui.clearState()
                return
            p.showGameMsg(GMDD.data.ITEM_NOT_RENEWAL_SAME_TYPE, ())
            return

    def doChangeBindItem(self, page, pos):
        p = BigWorld.player()
        i = p.inv.getQuickVal(page, pos)
        if i.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_STORAGE_LOCKED, ())
            return
        if not utils.checkValuableTradeItem(i):
            p.showGameMsg(GMDD.data.VALUABLE_ITEM_LATCH, uiUtils.getItemColorName(i.id))
            return
        if p:
            if i.isForeverBind():
                bindHint = uiUtils.getTextFromGMD(GMDD.data.CHANGE_BIND_CONFIRM, gameStrings.TEXT_INVENTORYPROXY_1418) % uiUtils.getItemColorName(i.id)
            else:
                bindHint = uiUtils.getTextFromGMD(GMDD.data.CHANGE_UNBIND_CONFIRM, gameStrings.TEXT_INVENTORYPROXY_1418) % uiUtils.getItemColorName(i.id)
            self.uiAdapter.messageBox.showYesNoMsgBox(bindHint, Functor(p.cell.convertBindItem, page, pos))

    def onClickItem(self, *args):
        itemId = args[3][0]
        nPage, nItem = self.getSlotID(itemId.GetString())
        p = BigWorld.player()
        if ui.get_cursor_state() == ui.ADD_STAR_EXP_STATE:
            self.doAddStarExp(const.RES_KIND_INV, nPage, nItem)
            return GfxValue(True)
        if ui.get_cursor_state() == ui.RENEWAL_STATE:
            self.doRenewerItem(nPage, nItem)
            return GfxValue(True)
        if ui.get_cursor_state() == ui.RENEWAL_STATE2:
            i = BigWorld.player().inv.getQuickVal(nPage, nItem)
            if i:
                if i.isMallFashionRenewable():
                    gameglobal.rds.ui.itemResume.show(i, nPage, nItem)
            return GfxValue(True)
        if ui.get_cursor_state() == ui.RESET_FASHION_PROP:
            i = BigWorld.player().inv.getQuickVal(nPage, nItem)
            if i:
                if i.isFashionEquip() and hasattr(i, 'fashionTransProp'):
                    msg = uiUtils.getTextFromGMD(GMDD.data.FASHION_RESTORE_MSG, gameStrings.TEXT_INVENTORYPROXY_1447)
                    title = uiUtils.getTextFromGMD(GMDD.data.FASHION_RESTORE_TITLE, gameStrings.TEXT_INVENTORYPROXY_1448)
                    itemPos = ui.get_bindItemPos()
                    sourceIt = BigWorld.player().inv.getQuickVal(itemPos[1], itemPos[2])
                    msg = msg % uiUtils.getItemColorName(sourceIt.id)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doRestoreFashion, itemPos[1], itemPos[2], nPage, nItem), title=title)
                    return
        elif ui.get_cursor_state() == ui.CHANGE_BIND_STATE:
            itemId = args[3][0]
            nPage, nItem = self.getSlotID(itemId.GetString())
            if nPage == uiConst.BAG_PAGE_QUEST:
                return GfxValue(False)
            i = BigWorld.player().inv.getQuickVal(nPage, nItem)
            if not i:
                return GfxValue(False)
            elif i.getBindConvertId():
                self.doChangeBindItem(nPage, nItem)
                return GfxValue(True)
            else:
                return GfxValue(False)
        else:
            if ui.get_cursor_state() == ui.IDENTIFY_ITEM_STATE:
                itemId = args[3][0]
                nPage, nItem = self.getSlotID(itemId.GetString())
                self.doIdentifyItem(nPage, nItem)
                return GfxValue(True)
            if ui.get_cursor_state() == ui.IDENTIFY_MANUAL_EQUIP_STATE:
                itemId = args[3][0]
                nPage, nItem = self.getSlotID(itemId.GetString())
                self.doIdentifyEquip(nPage, nItem)
                return GfxValue(True)
            if self.isSignEquipState:
                itemId = args[3][0]
                nPage, nItem = self.getSlotID(itemId.GetString())
                p = BigWorld.player()
                if nPage == uiConst.BAG_PAGE_QUEST:
                    i = BigWorld.player().questBag.getQuickVal(0, nItem)
                else:
                    i = BigWorld.player().inv.getQuickVal(nPage, nItem)
                signItem = p.inv.getQuickVal(self.signItemPage, self.signItemPos)
                if i == const.CONT_EMPTY_VAL:
                    return GfxValue(True)
                if getattr(signItem, 'cstype', 0) not in (item.Item.SUBTYPE_2_SIGN_ITEM, item.Item.SUBTYPE_2_SIGN_CLEAN):
                    p.showGameMsg(GMDD.data.NOT_SIGN_ITEM, ())
                    return GfxValue(True)
                if i.isCanSign():
                    signNum = ED.data.get(i.id, {}).get('signNum', 1)
                    pageList = []
                    posList = []
                    if signItem.isExpireTTL():
                        p.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (signItem.name,))
                        return
                    if signItem.hasLatch():
                        p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                        return
                    posList.append(self.signItemPos)
                    pageList.append(self.signItemPage)
                    if signItem.cwrap < signNum:
                        signNum -= signItem.cwrap
                        allList = p.inv.findAllItemInPages(signItem.id, gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, True, False, False, False)
                        for pg, ps in allList:
                            if pg != self.signItemPos and ps != self.signItemPage:
                                cit = p.inv.getQuickVal(pg, ps)
                                if not cit.isExpireTTL() and not cit.hasLatch():
                                    signNum -= cit.cwrap
                                    posList.append(ps)
                                    pageList.append(pg)

                    else:
                        signNum = 0
                    if signNum:
                        p.showGameMsg(GMDD.data.NOT_ENOUGH_SIGN, ())
                        return
                    gameglobal.rds.ui.equipSign.show(nPage, nItem, pageList, posList, const.RES_KIND_INV)
                    gameglobal.rds.ui.clearState()
                    return GfxValue(True)
                p.showGameMsg(GMDD.data.ITEM_CANNOT_SIGN, ())
                return GfxValue(True)
            return GfxValue(False)

    def doRestoreFashion(self, srcPage, srcPos, tgtPage, tgtPos):
        gameglobal.rds.ui.clearState()
        p = BigWorld.player()
        p.cell.restoreFashionProp(const.RES_KIND_INV, srcPage, srcPos, tgtPage, tgtPos)

    def onRealResume(self, srcPage, srcPos, tgtPage, tgtPos, resKind):
        BigWorld.player().cell.renewalItemOfUse(srcPage, srcPos, tgtPage, tgtPos, resKind)

    def onDyeDesItem(self, *arg):
        if self.isDyeState:
            nPage, nItem = self.getSlotID(arg[3][0].GetString())
            p = BigWorld.player()
            i = p.inv.getQuickVal(self.uiAdapter.inventory.dyeItemPage, self.uiAdapter.inventory.dyeItemPos)
            if i.isDye():
                self._onDyeDesItem(nPage, nItem)
            elif i.isRongGuang():
                self._onRongGuangDesItem(nPage, nItem)
            elif getattr(i, 'cstype', 0) == item.Item.SUBTYPE_2_RUBBING_CLEAN:
                self._onRubbingCleanItem(nPage, nItem)
            elif hasattr(i, 'cstype') and i.cstype == item.Item.SUBTYPE_2_COLOR_CARD:
                self.useColorCard(nPage, nItem)

    def _onDyeDesItem(self, nPage, nItem):
        p = BigWorld.player()
        if nPage == const.INV_PAGE_EQUIP:
            equip = p.equipment.get(nItem)
        elif nPage == const.INV_PAGE_WARDROBE:
            equip = p.wardrobeBag.getDrobeItem(nItem)
        else:
            equip = p.inv.getQuickVal(nPage, nItem)
        if equip and equip.isCanDye():
            dyeItem = p.inv.getQuickVal(self.uiAdapter.inventory.dyeItemPage, self.uiAdapter.inventory.dyeItemPos)
            if dyeItem and dyeItem.getDyeType() in (Item.CONSUME_DYE_CLEAN, Item.CONSUME_DYE_RANDOM, Item.CONSUME_DYE_MAGIC):
                desc = ''
                if dyeItem.getDyeType() == Item.CONSUME_DYE_CLEAN and getattr(equip, 'dyeMaterials', []):
                    desc = SYSCD.data.get('dyeCleanTip', gameStrings.TEXT_INVENTORYPROXY_1569)
                    if gameglobal.rds.configData.get('enableWardrobe', False):
                        desc = gameStrings.WARDROBE_CLEAN_DYE_TIP
                elif dyeItem.getDyeType() == Item.CONSUME_DYE_RANDOM:
                    desc = SYSCD.data.get('dyeRandomTip', gameStrings.TEXT_INVENTORYPROXY_1573)
                elif dyeItem.getDyeType() == Item.CONSUME_DYE_MAGIC:
                    desc = SYSCD.data.get('dyeMagicTip', gameStrings.TEXT_INVENTORYPROXY_1575)
                if desc:
                    self.uiAdapter.messageBox.showYesNoMsgBox(desc, Functor(self.dyeEquipment, nPage, nItem), gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)
                else:
                    p.showGameMsg(GMDD.data.EQUIP_NO_DYE, ())
            else:
                gameglobal.rds.ui.dyeColor.setItemInfo(equip.name, uiUtils.getItemColor(equip.id))
                gameglobal.rds.ui.dyeColor.show(True, self.dyeItemPage, self.dyeItemPos, nPage, nItem)
        else:
            p.showGameMsg(GMDD.data.EQUIP_CANNOT_DYE, ())

    def _onRongGuangDesItem(self, nPage, nItem):
        p = BigWorld.player()
        if nPage == const.INV_PAGE_EQUIP:
            equip = p.equipment.get(nItem)
        elif nPage == const.INV_PAGE_WARDROBE:
            equip = p.wardrobeBag.getDrobeItem(nItem)
        else:
            equip = p.inv.getQuickVal(nPage, nItem)
        if equip and equip.isCanRongGuang():
            rongGuangItem = p.inv.getQuickVal(self.uiAdapter.inventory.dyeItemPage, self.uiAdapter.inventory.dyeItemPos)
            if rongGuangItem and rongGuangItem.getRongGuangType() in (Item.CONSUME_RONGGUANG_CLEAN,):
                desc = SYSCD.data.get('rongGuangCleanTip', gameStrings.TEXT_INVENTORYPROXY_1597)
                if getattr(equip, 'rongGuang', []):
                    self.uiAdapter.messageBox.showYesNoMsgBox(desc, Functor(self.rongGuangEquipment, nPage, nItem), gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)
                else:
                    p.showGameMsg(GMDD.data.EQUIP_NO_RONGGUANG, ())
            else:
                gameglobal.rds.ui.dyeColor.setItemInfo(equip.name, uiUtils.getItemColor(equip.id))
                gameglobal.rds.ui.dyeColor.show(False, self.dyeItemPage, self.dyeItemPos, nPage, nItem)
        else:
            p.showGameMsg(GMDD.data.EQUIP_CANNOT_RONGGUANG, ())

    def _onRubbingCleanItem(self, nPage, nItem):
        p = BigWorld.player()
        if nPage == const.INV_PAGE_EQUIP:
            equip = p.equipment.get(nItem)
        elif nPage == const.INV_PAGE_WARDROBE:
            equip = p.wardrobeBag.getDrobeItem(nItem)
        else:
            equip = p.inv.getQuickVal(nPage, nItem)
        if equip and equip.isCanRubbing() and getattr(equip, 'rubbing', 0):
            p.cell.useRubbingCleanItem(const.RES_KIND_INV, self.dyeItemPage, self.dyeItemPos, nPage, nItem)
            self.clearDyeState()

    def rongGuangEquipment(self, nPage, nItem):
        if self.isDyeState:
            p = BigWorld.player()
            if nPage == const.INV_PAGE_EQUIP:
                i = p.equipment.get(nItem)
            elif nPage == const.INV_PAGE_WARDROBE:
                i = p.wardrobeBag.getDrobeItem(nItem)
            else:
                i = BigWorld.player().inv.getQuickVal(nPage, nItem)
            if i and i.isCanRongGuang():
                p.cell.useRongGuangItem(const.RES_KIND_INV, self.dyeItemPage, self.dyeItemPos, nPage, nItem)
                self.clearDyeState()

    def dyeEquipment(self, nPage, nItem, dyeMethod = const.DYE_COPY):
        if self.isDyeState:
            p = BigWorld.player()
            if nPage == const.INV_PAGE_EQUIP:
                i = p.equipment.get(nItem)
            elif nPage == const.INV_PAGE_WARDROBE:
                i = p.wardrobeBag.getDrobeItem(nItem)
            else:
                i = BigWorld.player().inv.getQuickVal(nPage, nItem)
            dyeItem = p.inv.getQuickVal(self.dyeItemPage, self.dyeItemPos)
            diyColor = self.uiAdapter.dyeColor.getDyeColor()
            if dyeItem and dyeItem.getDyeType() == Item.CONSUME_DYE_SUPER:
                if diyColor == '':
                    return
            if i == const.CONT_EMPTY_VAL:
                return
            if i.isCanDye():
                p.cell.useDyeItem(const.RES_KIND_INV, self.dyeItemPage, self.dyeItemPos, nPage, nItem, const.DYE_COPY, diyColor)
                self.clearDyeState()
                if gameglobal.rds.ui.roleInfo.headGen:
                    model = gameglobal.rds.ui.roleInfo.headGen.adaptor.attachment
                    if model:
                        uiUtils.recoveDyeModel(model)

    def onIsShopShow(self, *arg):
        return GfxValue(gameglobal.rds.ui.shop.getIsShow())

    def onInRepair(self, *arg):
        return GfxValue(gameglobal.rds.ui.shop.inRepair)

    def onSendSet(self, *arg):
        itemId = arg[3][0]
        nPage, nItem = self.getSlotID(itemId.GetString())
        if nPage == uiConst.BAG_PAGE_QUEST:
            i = BigWorld.player().questBag.getQuickVal(0, nItem)
        else:
            i = BigWorld.player().inv.getQuickVal(nPage, nItem)
        if i != const.CONT_EMPTY_VAL:
            if i.isNeedHyperlink():
                BigWorld.player().constructItemInfo(const.RES_KIND_INV, nPage, nItem)
            else:
                color = FCD.data.get(('item', ID.data.get(i.id, {}).get('quality', 1)), {}).get('color', '#CCCCCC')
                msg = "<font color=\'%s\'>[<a href = \'event:item%s\'><u>%s</u></a>]</font>" % (color, str(i.id) + i.getExtraLinkInfo(), str(i.name) + i.getNameSuffix())
                gameglobal.rds.ui.sendLink(msg)

    def onGetBagSlotBindings(self, *arg):
        bagId = arg[3][0].GetString()
        movie = arg[0]
        arr = movie.CreateArray()
        for i in range(0, 16):
            item = 'bag_%s.slot%d' % (bagId, i)
            arr.SetElement(i, GfxValue(item))

        return arr

    def onGetinitData(self, *arg):
        ret = {}
        p = BigWorld.player()
        self.tempBagNum = const.TEMP_BAG_WIDTH * const.TEMP_BAG_HEIGHT - p.tempBag.countBlank(0)
        self.tempMallBagNum = const.MALL_BAG_WIDTH * const.MALL_BAG_HEIGHT - p.mallBag.countBlank(0)
        ret['isAutoSortInventory'] = self.isAutoSortInventory
        ret['pageNum'] = self.page
        ret['tempBagNum'] = self.tempBagNum
        ret['tempMallBagNum'] = self.tempMallBagNum
        ret['valueTradeButtonVisible'] = gameglobal.rds.configData.get('enableValuableTrade', False)
        ret['bagTabCount'] = self._getTabCount()
        ret['bagSlot'] = p.inv.enabledPackSlotCnt
        ret['tempBagCheckBoxState'] = AppSettings.get(TEMP_BAG_CHECKBOX_KEY, 0)
        ret['tempBagCheckBoxLabel'] = SCD.data.get('TEMPBAG_CHECKBOX_LABEL_DESC', gameStrings.TEXT_CHATPROXY_633)
        self.updataMoney()
        self.updateMoneyBtn()
        return uiUtils.dict2GfxDict(ret, True)

    def _getTabCount(self):
        p = BigWorld.player()
        tabCount = uiConst.BAG_PAGE_NUM
        for i in range(0, uiConst.BAG_PAGE_NUM):
            posCount = p.inv.posCountDict.get(i, 0)
            if posCount == 0:
                tabCount = i
                break

        return tabCount

    def setBagTabAble(self, type, isEnable):
        if self.mediator:
            self.mediator.Invoke('setBagTabAble', (GfxValue(type), GfxValue(isEnable)))

    def onRepair(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if page == uiConst.BAG_PAGE_QUEST:
            return
        gameglobal.rds.ui.shop.doRepair(page, pos)

    def initItemArr(self, it, pos, kind = const.RES_KIND_INV):
        obj = uiUtils.getGfxItem(it)
        state = self._getSlotState(uiConst.BAG_PAGE_LOW, pos, it, kind)
        arr = [pos,
         obj,
         state,
         obj['color']]
        return uiUtils.array2GfxAarry(arr, True)

    def onInitBagBarItem(self, *arg):
        p = BigWorld.player()
        ret = self._initItemList(p.bagBar, const.RES_KIND_INV_BAR)
        return ret

    def onInitTempBagItem(self, *arg):
        retMap = {}
        p = BigWorld.player()
        lenth = self.tempBagDataLenth(p.tempBag.pages)
        ret = self._initItemList(p.tempBag, const.RES_KIND_TEMP_BAG)
        isInterruptUpdate = gameglobal.rds.ui.activitySaleLuckyLottery.checkTempBagDataValid()
        if isInterruptUpdate:
            ret = self.movie.CreateArray()
        retMap['lenth'] = lenth
        retMap['data'] = ret
        return uiUtils.dict2GfxDict(retMap, True)

    def tempBagDataLenth(self, tempBagItemList):
        ret = 0
        flag = False
        for i, item in enumerate(tempBagItemList[0]):
            if item:
                flag = True
            else:
                flag = False
            if flag:
                ret = i

        return ret

    def onInitFashionBagItem(self, *arg):
        p = BigWorld.player()
        ret = self._initItemList(p.fashionBag, const.RES_KIND_FASHION_BAG)
        return ret

    def onInitMaterialBagItem(self, *arg):
        p = BigWorld.player()
        ret = self._initItemList(p.materialBag, const.RES_KIND_MATERIAL_BAG)
        return ret

    def onInitMallInvBagItem(self, *arg):
        p = BigWorld.player()
        ret = self._initItemList(p.mallBag, const.RES_KIND_MALL_BAG)
        return ret

    def onInitBagItem(self, *arg):
        p = BigWorld.player()
        ret = self._initItemList(p.inv)
        posCount = p.inv.posCountDict.get(uiConst.BAG_PAGE_LOW, 0)
        self.setSlotCount(posCount)
        return ret

    def _initItemList(self, container, kind = const.RES_KIND_INV):
        if container == None:
            return
        else:
            ret = self.movie.CreateArray()
            i = 0
            for ps in xrange(container.posCount):
                it = container.getQuickVal(0, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                arr = self.initItemArr(it, ps, kind)
                ret.SetElement(i, arr)
                i += 1
                if kind == const.RES_KIND_INV:
                    if it.uuid in self.newItemSequence:
                        self.setNewIconVisible(ps, True)
                    self.checkItemEffectAndCoolDown(it, uiConst.BAG_PAGE_LOW, ps)

            return ret

    def showNumberInputWidget(self, whichType = None, page = -1, pos = -1, martPos = -1, dstPg = -1, dstPos = -1, confirmCallback = None):
        self.whichType = whichType
        if self.whichType in (uiConst.NUMBER_WIDGET_ITEM_TRADE,
         uiConst.NUMBER_WIDGET_ITEM_MAIL,
         uiConst.NUMBER_WIDGET_BIND_ITEM_TRADE,
         uiConst.NUMBER_WIDGET_ITEM_GUILD_DONATE,
         uiConst.WIDGET_GUILD_STORAGE,
         uiConst.NUMBER_WIDGET_WISH_MADE,
         uiConst.NUMBER_WIDGET_RANDOM_DYE):
            self.nPage = page
            self.nPos = pos
            self.martPos = martPos
            self.dstPg = dstPg
            self.dstPos = dstPos
        self.confirmCallback = confirmCallback
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NUMBER_VIEW, True)

    def notifySlotDragEndEx(self, *arg):
        gameglobal.rds.ui.inDragCommonItem = False
        srcId = arg[3][0]
        destId = arg[3][1]
        _, self.nItemSrc = self.getSlotID(srcId.GetString())
        if gameglobal.rds.ui.inventory.page != uiConst.BAG_PAGE_QUEST:
            self.nPageSrc = gameglobal.rds.ui.dragInvPageSrc
        else:
            return
        p = BigWorld.player()
        if self.nPageSrc == None or self.nItemSrc == None:
            return
        else:
            sItem = p.inv.getQuickVal(self.nPageSrc, self.nItemSrc)
            if not sItem:
                return
            if destId.IsNull():
                return
            dest = destId.GetString()
            if dest.find('.') == -1:
                return
            self.nPageDes, self.nItemDes = self.getSlotID(dest)
            if dest[0:7] == 'consign':
                gameglobal.rds.ui.consign.setItem(1, 99, sItem, self.nPageSrc, self.nItemSrc)
                return
            if dest[0:17] == 'tabAuctionConsign':
                gameglobal.rds.ui.tabAuctionConsign.setItem(1, 99, sItem, self.nPageSrc, self.nItemSrc)
                return
            if dest[0:21] == 'tabAuctionCrossServer':
                gameglobal.rds.ui.tabAuctionCrossServer.setItem(1, 99, sItem, self.nPageSrc, self.nItemSrc)
                return
            dItem = p.inv.getQuickVal(self.nPageDes, self.nItemDes)
            if hasattr(sItem, 'cwrap') and sItem.cwrap == 1:
                cellCmd.exchangeInv(self.nPageSrc, self.nItemSrc, sItem.cwrap, self.nPageDes, self.nItemDes)
            else:
                if gameglobal.rds.ui.trade.isShow:
                    p.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
                    return
                if not dItem or Item.canMerge(sItem, dItem):
                    if sItem and sItem.isOneQuest():
                        p.showGameMsg(GMDD.data.QUEST_ITEM_SPLIT_FORBIDDEN, ())
                        return
                    if sItem.hasLatch():
                        p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                        return
                    self.showNumberInputWidget(uiConst.NUMBER_WIDGET_SPLIT)
            return

    def cancelSplit(self, *arg):
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_NUMBER_VIEW)))
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def confirmSplit(self, *arg):
        numStr = arg[3][0].GetString()
        if numStr == '':
            num = 0
        else:
            num = int(numStr)
        p = BigWorld.player()
        if self.whichType == uiConst.NUMBER_WIDGET_SPLIT:
            i = p.inv.getQuickVal(self.nPageSrc, self.nItemSrc)
            if not i:
                self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_NUMBER_VIEW)))
                gameglobal.rds.sound.playSound(gameglobal.SD_2)
                return
            judge = (1, i.mwrap, GMDD.data.ITEM_TRADE_NUM)
            if not ui.inputRangeJudge(judge, num, (i.mwrap,)):
                return
            cellCmd.exchangeInv(self.nPageSrc, self.nItemSrc, num, self.nPageDes, self.nItemDes)
        elif self.whichType == uiConst.NUMBER_WIDGET_MONEY:
            if not ui.inputRangeJudge(ui.INPUT_RANGE_1_99, num):
                return
            p.cell.discardMoney(num)
        elif self.whichType == uiConst.NUMBER_WIDGET_ITEM_TRADE:
            i = p.inv.getQuickVal(self.nPage, self.nPos)
            if not i:
                return
            if i.hasLatch():
                BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
            if not i or not ui.inputRangeJudge((1, i.cwrap, GMDD.data.ITEM_TRADE_NUM), num, (i.cwrap,)):
                return
            if i.isRuneEquip() and getattr(i, 'runeData', ()):
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_INVENTORYPROXY_1914, Functor(self.confirmTradeItem, self.nPage, self.nPos, self.martPos, num))
            else:
                p.cell.tradeItem(self.nPage, self.nPos, self.martPos, num)
        elif self.whichType == uiConst.NUMBER_WIDGET_BIND_ITEM_TRADE:
            i = p.inv.getQuickVal(self.nPage, self.nPos)
            if not i:
                return
            if i.hasLatch():
                BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
            if not i or not ui.inputRangeJudge((1, i.cwrap, GMDD.data.ITEM_TRADE_NUM), num, (i.cwrap,)):
                return
            p.cell.giveItem(self.nPage, self.nPos, self.martPos, num)
        elif self.whichType == uiConst.NUMBER_WIDGET_ITEM_MAIL:
            i = p.inv.getQuickVal(self.nPage, self.nPos)
            if not i or not ui.inputRangeJudge((1, i.cwrap, GMDD.data.ITEM_TRADE_NUM), num, (i.cwrap,)):
                return
            gameglobal.rds.ui.mail.setItem(self.nPage, self.nPos, 0, self.martPos, i, num)
        elif self.whichType == uiConst.NUMBER_WIDGET_ITEM_GUILD_DONATE:
            i = p.inv.getQuickVal(self.nPage, self.nPos)
            if not i or not ui.inputRangeJudge((1, i.cwrap, GMDD.data.ITEM_TRADE_NUM), num, (i.cwrap,)):
                return
            gameglobal.rds.ui.guildDonate.setItem(self.nPage, self.nPos, 0, self.martPos, i, num)
        elif self.whichType == uiConst.NUMBER_WIDGET_RANDOM_DYE:
            i = p.inv.getQuickVal(self.nPage, self.nPos)
            if not i or not ui.inputRangeJudge((1, i.cwrap, GMDD.data.ITEM_TRADE_NUM), num, (i.cwrap,)):
                return
            gameglobal.rds.ui.randomDye.setItem(self.nPage, self.nPos, 0, self.martPos, i, num)
        elif self.whichType == uiConst.WIDGET_GUILD_STORAGE:
            if p.guild and p.guild.storage:
                if self.dstPg == -1:
                    i = p.guild.storage.getQuickVal(self.nPage, self.nPos)
                    if not i or not ui.inputRangeJudge((1, i.cwrap, GMDD.data.ITEM_TRADE_NUM), num, (i.cwrap,)):
                        return
                    dstPos = p.guild.storage.searchEmpty(self.nPage)
                    if dstPos == const.CONT_NO_POS:
                        p.showGameMsg(GMDD.data.GUILD_STORAGE_NO_POS, ())
                    else:
                        p.cell.storageGuildExchange(self.nPage, self.nPos, i.uuid, num, self.nPage, dstPos, '')
                else:
                    i = p.guild.storage.getQuickVal(self.nPage, self.nPos)
                    if not i or not ui.inputRangeJudge((1, i.cwrap, GMDD.data.ITEM_TRADE_NUM), num, (i.cwrap,)):
                        return
                    sItem = p.guild.storage.getQuickVal(self.nPage, self.nPos)
                    p.cell.storageGuild2inv(self.nPage, self.nPos, sItem.uuid, num, sItem.id, self.dstPg, self.dstPos)
        elif self.whichType == uiConst.NUMBER_WIDGET_WISH_MADE:
            i = p.inv.getQuickVal(self.nPage, self.nPos)
            if not i or not ui.inputRangeJudge((1, i.cwrap, GMDD.data.ITEM_TRADE_NUM), num, (i.cwrap,)):
                return
            gameglobal.rds.ui.wishMade.setItem(self.nPage, self.nPos, 0, self.martPos, i, num)
        if getattr(self, 'confirmCallback', None):
            self.confirmCallback(num)
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_NUMBER_VIEW)))
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def confirmTradeItem(self, invPage, invPos, martPos, amount):
        BigWorld.player().cell.tradeItem(invPage, invPos, martPos, amount)

    def confirmDiscard(self, *arg):
        p = BigWorld.player()
        if self.nPageSrc == uiConst.BAG_PAGE_QUEST:
            item = p.questBag.getQuickVal(0, self.nItemSrc)
            if item != const.CONT_EMPTY_VAL:
                p.showGameMsg(GMDD.data.ITEM_CANNOT_DROP, (item.name,))
        else:
            item = p.inv.getQuickVal(self.nPageSrc, self.nItemSrc)
            if item != const.CONT_EMPTY_VAL:
                num = item.cwrap
                judge = (1, item.mwrap, GMDD.data.ITEM_TRADE_NUM)
                if ID.data.get(item.id, {}) and not ui.inputRangeJudge(judge, num, (item.mwrap,)):
                    return
                BigWorld.player().cell.discardItem(self.nPageSrc, self.nItemSrc, num)
                gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def cancelDiscard(self, *arg):
        if self.nPageSrc == uiConst.BAG_PAGE_QUEST:
            item = BigWorld.player().questBag.getQuickVal(0, self.nItemSrc)
        else:
            item = BigWorld.player().inv.getQuickVal(self.nPageSrc, self.nItemSrc)
        if item != const.CONT_EMPTY_VAL:
            gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def closeInventory(self, *arg):
        self.onCloseInvTempBag()
        self.hide()
        self.filterSubtype = 0

    def resetData(self):
        self.page = uiConst.BAG_PAGE_LOW
        self.itemFilter = uiConst.FILTER_ITEM_ALL
        self.dropMBIds = []
        self.numberMediator = None
        gameglobal.rds.ui.inDragCommonItem = False
        self.newItemSequence = []
        self.clearState()
        self.filterSubtype = 0
        self.openWithTemp = None
        self.searchList = []

    def reset(self):
        super(self.__class__, self).reset()
        self.resetData()
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            if gameglobal.rds.ui.equipMixNew.mediator:
                return
            gameglobal.rds.ui.funcNpc.closeByInv()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.tempBagMediator = None
        self.openWithTemp = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INVENTORY)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NUMBER_VIEW)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INVENTORY_TEMP_BAG)
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.onItemChange)
                BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.onItemRemove)
        self.uiAdapter.clearState()
        if gameglobal.rds.ui.payItem.isShow:
            gameglobal.rds.ui.payItem.closePayItem()
        if gameglobal.rds.ui.consign.mediator:
            gameglobal.rds.ui.consign.removeItem(1, 99)
        if gameglobal.rds.ui.tabAuctionConsign.panelMc:
            gameglobal.rds.ui.tabAuctionConsign.removeItem(1, 99)
        if gameglobal.rds.ui.tabAuctionCrossServer.panelMc:
            gameglobal.rds.ui.tabAuctionCrossServer.removeItem(1, 99)
        if gameglobal.rds.ui.mail.mediator:
            gameglobal.rds.ui.mail.clearItem()
        if gameglobal.rds.ui.guildDonate.mediator:
            gameglobal.rds.ui.guildDonate.clearItem()
        if gameglobal.rds.ui.equipFeed.mediator:
            gameglobal.rds.ui.equipFeed.hide()
        if gameglobal.rds.ui.storage.mediator:
            gameglobal.rds.ui.storage.hide()
        if gameglobal.rds.ui.equipMix.mediator:
            gameglobal.rds.ui.equipMix.clearWidget()
        if gameglobal.rds.ui.yaoPeiMix.mediator:
            gameglobal.rds.ui.yaoPeiMix.hide()
        if gameglobal.rds.ui.yaoPeiFeed.mediator:
            gameglobal.rds.ui.yaoPeiFeed.hide()
        if gameglobal.rds.ui.yaoPeiTransfer.mediator:
            gameglobal.rds.ui.yaoPeiTransfer.hide()
        if gameglobal.rds.ui.yaoPeiReforge.mediator:
            gameglobal.rds.ui.yaoPeiReforge.hide()
        if gameglobal.rds.ui.homeTermsStorage.widget:
            gameglobal.rds.ui.homeTermsStorage.hide()
        if gameglobal.rds.ui.randomDye.widget:
            gameglobal.rds.ui.randomDye.clearItem()
        self.dispatchEvent(events.EVENT_INVENTORY_CLOSE)

    def checkCanShow(self):
        p = BigWorld.player()
        if gameglobal.rds.ui.itemPreviewSelect.widget:
            p.showGameMsg(GMDD.data.FORBIDEN_INVENTORY_IN_ITEM_PREVIEW, ())
            return False
        if not p.checkMapLimitUI(gametypes.MAP_LIMIT_UI_INV):
            return False
        if p._isSchoolSwitch():
            p.showGameMsg(GMDD.data.FORBIDEN_INVENTORY_IN_SCHOOL_SWITCH, ())
            return False
        if formula.inDotaBattleField(p.mapID):
            return False
        return True

    def show(self, visible = True, layoutType = 0, tempPanel = None):
        if not self.checkCanShow():
            return
        if visible and self.mediator:
            self.hide(False)
            self.resetData()
        self.openWithTemp = tempPanel
        self.uiAdapter.loadWidget(uiConst.WIDGET_INVENTORY, False, False, layoutType)
        self.dispatchEvent(events.EVENT_INVENTORY_OPEN)

    def setFirstTab(self):
        if self.mediator:
            self.mediator.Invoke('setFirstTab')

    def setSlotCount(self, slotCount):
        if self.mediator:
            self.mediator.Invoke('setSlotCount', GfxValue(slotCount))

    def onPlayCooldown(self, *arg):
        pass

    def onRegisterNumberWidget(self, *arg):
        self.numberMediator = arg[3][0]
        if self.whichType in (uiConst.NUMBER_WIDGET_ITEM_TRADE, uiConst.NUMBER_WIDGET_ITEM_MAIL, uiConst.NUMBER_WIDGET_BIND_ITEM_TRADE):
            i = BigWorld.player().inv.getQuickVal(self.nPage, self.nPos)
            self.numberMediator.Invoke('setText', GfxValue(str(int(i.cwrap))))

    def onSetInvItem(self, *arg):
        p = BigWorld.player()
        idx = int(arg[3][0].GetNumber())
        if self.page == uiConst.BAG_PAGE_QUEST:
            posCount = p.questBag.posCount
        else:
            posCount = p.inv.posCountDict.get(self.page, 0)
        for ps in xrange(posCount):
            self.removeItem(self.page, ps)
            self.setNewIconVisible(ps, False)

        self.setPage(idx)
        if idx == uiConst.BAG_PAGE_QUEST:
            posCount = p.questBag.posCount
        else:
            posCount = p.inv.posCountDict.get(idx, 0)
        for ps in xrange(posCount):
            if idx == uiConst.BAG_PAGE_QUEST:
                it = p.questBag.getQuickVal(0, ps)
            else:
                it = p.inv.getQuickVal(idx, ps)
            if it == const.CONT_EMPTY_VAL:
                continue
            self.addItem(it, idx, ps)

        self.setSlotCount(posCount)
        if gameglobal.rds.ui.payItem.isShow:
            gameglobal.rds.ui.payItem.refreshPayBag()

    def updataMoney(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            info['yunbi'] = format(p.cash, ',') if hasattr(p, 'cash') else gameStrings.TEXT_INVENTORYPROXY_2183
            info['yunquan'] = format(p.bindCash, ',') if hasattr(p, 'bindCash') else gameStrings.TEXT_INVENTORYPROXY_2183
            if hasattr(p, 'unbindCoin') and hasattr(p, 'bindCoin') and hasattr(p, 'freeCoin'):
                tianBi = p.unbindCoin + p.bindCoin + p.freeCoin
                info['tianbi'] = format(tianBi, ',')
            else:
                info['tianbi'] = gameStrings.TEXT_INVENTORYPROXY_2183
            info['yunchui'] = format(p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID), ',')
            self.mediator.Invoke('updateGold', uiUtils.dict2GfxDict(info, True))

    def updateMoneyBtn(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            yunbiBtnMinLv = SYSCD.data.get('yunbiBtnMinLv', 0)
            info['yunbiBtnEnabled'] = p.lv >= yunbiBtnMinLv
            info['yunbiBtnGrayTip'] = gameStrings.TEXT_INVENTORYPROXY_2204 % yunbiBtnMinLv
            yunquanBtnMinLv = SYSCD.data.get('yunquanBtnMinLv', 0)
            info['yunquanBtnEnabled'] = p.lv >= yunquanBtnMinLv
            info['yunquanBtnGrayTip'] = gameStrings.TEXT_INVENTORYPROXY_2204 % yunquanBtnMinLv
            tianbiBtnMinLv = SYSCD.data.get('tianbiBtnMinLv', 0)
            info['tianbiBtnEnabled'] = p.lv >= tianbiBtnMinLv
            info['tianbiBtnGrayTip'] = gameStrings.TEXT_INVENTORYPROXY_2204 % tianbiBtnMinLv
            if gameglobal.rds.configData.get('enablePrivateYunChuiShop', False):
                yunchuiBtnMinLv = SCD.data.get('privateYunChuiShopMinLv', 20)
            else:
                yunchuiBtnMinLv = SYSCD.data.get('yunchuiBtnMinLv', 0)
            info['yunchuiBtnEnabled'] = p.lv >= yunchuiBtnMinLv
            info['yunchuiBtnGrayTip'] = gameStrings.TEXT_INVENTORYPROXY_2204 % yunchuiBtnMinLv
            info['yunbiBtnHowTip'] = SYSCD.data.get('yunbiBtnHowTip', gameStrings.TEXT_INVENTORYPROXY_2221)
            info['yunquanBtnHowTip'] = SYSCD.data.get('yunquanBtnHowTip', gameStrings.TEXT_INVENTORYPROXY_2222)
            info['tianbiBtnHowTip'] = SYSCD.data.get('tianbiBtnHowTip', gameStrings.TEXT_INVENTORYPROXY_2223)
            if gameglobal.rds.configData.get('enablePrivateYunChuiShop', False):
                info['yunchuiBtnHowTip'] = SYSCD.data.get('privateYunChuiTip', gameStrings.TEXT_INVENTORYPROXY_2225)
            else:
                info['yunchuiBtnHowTip'] = SYSCD.data.get('yunchuiBtnHowTip', gameStrings.TEXT_INVENTORYPROXY_2227)
            self.mediator.Invoke('updateGoldBtn', uiUtils.dict2GfxDict(info, True))

    def setPage(self, page):
        self.page = page

    def getSlotID(self, key):
        _, idItem = key.split('.')
        nItem = int(idItem[4:])
        return (self.page, nItem)

    def getSlotValue(self, movie, idItem, idCon):
        return None

    def addSackItem(self, item, page, pos):
        if item is not None:
            key = self._getSackKey(page, pos)
            if gameglobal.rds.ui.sack.binding.get(key, None) is not None:
                data = uiUtils.getGfxItem(item)
                color = data['color']
                gameglobal.rds.ui.sack.binding[key][0].Invoke('setSlotColor', GfxValue(color))
                gameglobal.rds.ui.sack.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data, True))
                if page == const.MATERIAL_BAG_BIND_ID:
                    if hasattr(item, 'latchOfTime'):
                        gameglobal.rds.ui.sack.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_LATCH_TIME))
                    elif hasattr(item, 'latchOfCipher'):
                        gameglobal.rds.ui.sack.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_LATCH_CIPHER))

    def removeSackItem(self, page, pos):
        key = self._getSackKey(page, pos)
        if gameglobal.rds.ui.sack.binding.get(key, None) is not None:
            data = GfxValue(1)
            data.SetNull()
            gameglobal.rds.ui.sack.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
            gameglobal.rds.ui.sack.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            gameglobal.rds.ui.sack.binding[key][1].InvokeSelf(data)

    def addItem(self, item, page, pos):
        if self.page != page:
            return
        else:
            if item is not None:
                key = self._getKey(page, pos)
                if self.binding.get(key, None) is not None:
                    data = uiUtils.getGfxItem(item)
                    color = data['color']
                    self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
                    if self.searchList:
                        self.binding[key][0].Invoke('setSearchState', GfxValue(self.inSearchList(item.uuid)))
                    self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data, True))
                    self.checkItemEffectAndCoolDown(item, page, pos)
            self.updateSlotState(page, pos)
            return

    def inSearchList(self, uuid):
        for pg in self.searchList:
            for itemData in pg:
                if itemData[2] == uuid:
                    return True

        return False

    def checkItemEffectAndCoolDown(self, item, page, pos):
        if page != uiConst.BAG_PAGE_QUEST and item.type == Item.BASETYPE_CONSUMABLE:
            gameglobal.rds.ui.actionbar.playCooldown(page, pos, item.id, False)
        if item.id in gameglobal.rds.ui.payItem.items and gameglobal.rds.ui.payItem.isShow:
            self.showWarnEffect(pos, True)
        else:
            self.showWarnEffect(pos, False)

    def _removeNewItemSequence(self, page, pos):
        if page != uiConst.BAG_PAGE_QUEST:
            item = BigWorld.player().inv.getQuickVal(page, pos)
            if item and item.uuid in self.newItemSequence:
                self.newItemSequence.remove(item.uuid)
                self.setNewIconVisible(pos, False)

    def removeItem(self, page, pos):
        if self.page != page:
            return
        else:
            key = self._getKey(0, pos)
            if self.binding.get(key, None) is not None:
                data = GfxValue(1)
                data.SetNull()
                self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
                self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
                self.binding[key][0].Invoke('setSearchState', GfxValue(False))
                self.binding[key][1].InvokeSelf(data)
                gameglobal.rds.ui.actionbar.stopCoolDown(page, pos, False)
            self.setNewIconVisible(pos, False)
            self.showWarnEffect(pos, False)
            if gameglobal.rds.ui.payItem.isShow:
                gameglobal.rds.ui.payItem.refreshPayBag()
            return

    def _getKey(self, page, pos):
        return 'bag_%d.slot%d' % (0, pos)

    def _getSackKey(self, page, pos):
        return 'sack%d.slot%d' % (page, pos)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        if self.page == uiConst.BAG_PAGE_QUEST:
            i = p.questBag.getQuickVal(0, pos)
        else:
            i = BigWorld.player().inv.getQuickVal(page, pos)
        if i == None:
            return
        else:
            return self.GfxToolTip(i)

    def GfxToolTip(self, item, location = const.ITEM_IN_BAG):
        return tipUtils.getItemTipByLocation(item, location)

    def canSellToPrivateShop(self, i):
        shopId = SCD.data.get('privateCompositeShopId', 0)
        canSell, fameData = i.canSellToCompositeShopId(shopId)
        canSell = canSell and i.canSell(shopType=const.SHOP_TYPE_COMPOSITE, compositeShopId=shopId)
        canNavigate = ID.data.get(i.id, {}).has_key('navigatorTarget')
        return canSell and canNavigate

    def onNotifySlotUse(self, *arg):
        itemId = arg[3][0]
        nPage, nItem = self.getSlotID(itemId.GetString())
        p = BigWorld.player()
        if self.isShow() and gameglobal.rds.ui.crossServerBag.isShow():
            nPageDes, nItemDes = p.crossInv.searchEmptyInPages()
            if nItemDes == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.BAG_FULL, ())
                return
            uiDrag._endBagslotToCrossBagSlot(nPage, nItem, nPageDes, nItemDes)
            return
        elif self.isShow() and gameglobal.rds.ui.runeInv.widget:
            dstPage = self.uiAdapter.runeInv.currentPage
            dstPos = p.hierogramBag.searchEmpty(dstPage)
            if dstPos == const.CONT_NO_POS or dstPage == const.CONT_NO_POS:
                return
            uiDrag._endBagslotToRuneInv(nPage, nItem, dstPage, dstPos)
            return
        elif nPage == uiConst.BAG_PAGE_QUEST:
            p.useQuestItem(nPage, nItem)
            return
        else:
            i = p.inv.getQuickVal(nPage, nItem)
            if i == const.CONT_EMPTY_VAL:
                return
            acExcitement = i.getAcExcitement()
            if acExcitement and not p.checkExcitementFeature(acExcitement):
                return
            data = {}
            data['item'] = i
            data['page'] = nPage
            data['pos'] = nItem
            e = Event(events.EVENT_INVENTORY_ITEM_CLICKED, data)
            self.dispatchEvent(e)
            if e.handled:
                return
            yunChuiShop = gameglobal.rds.ui.yunChuiShop
            isYunChuiShopOpen = gameglobal.rds.ui.combineMall.currentTab == 1 and yunChuiShop.mediator
            compositeShop = gameglobal.rds.ui.compositeShop
            shopId = p.openShopId
            p.recordItem = i
            if compositeShop.mediator or isYunChuiShopOpen:
                composite = compositeShop
                if i.hasLatch():
                    p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                if composite.option == composite.OPTION_SHOP_BUY_BACK:
                    compositeShop.sellBuyBackItem(i)
                    return
                if compositeShop.mediator:
                    npc = BigWorld.entities.get(compositeShop.npcId)
                else:
                    npc = BigWorld.entities.get(yunChuiShop.npcId)
                if not npc and not yunChuiShop.isPrivateShop and not compositeShop.isPrivateShop():
                    return
                if hasattr(i, 'compositeShopId') and i.canReturnToShop():
                    if i.isRuneHasRuneData():
                        p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_RUNE_EQUIP, ())
                        return
                    if yunChuiShop.isPrivateShop:
                        p.base.compositeShopReturn(shopId, i.id, nPage, nItem)
                    elif i.compositeShopId == shopId:
                        npc.cell.compositeShopReturn(i.id, shopId, nPage, nItem)
                    return
                if i.isRuneHasRuneData():
                    p.showGameMsg(GMDD.data.ITEM_SELL_RUNE_EQUIP, ())
                    return
                canSell = i.canSell(shopType=p.openShopType, compositeShopId=shopId)
                canSellToPurchaseShop = i.canSellToPurchaseShop()
                canSellToCompositeShop = i.canSellToCompositeShop()
                canSellNormalToCompositeShop = i.canSellNormalToCompositeShop(shopId)
                if yunChuiShop.mediator and yunChuiShop.isPrivateShop or compositeShop.isPrivateShop():
                    functorSell = Functor(p.base.sellPrivateShopItem, shopId, nPage, nItem, i.cwrap, False)
                else:
                    functorSell = Functor(npc.cell.compositeShopBuy, shopId, nPage, nItem, i.cwrap, False)
                if not canSell:
                    p.showGameMsg(GMDD.data.NO_SELL_TO_SHOP, ())
                    return
                if canSell and not canSellToCompositeShop and not canSellToPurchaseShop and not canSellNormalToCompositeShop:
                    p.showGameMsg(GMDD.data.COMPOSITESHOP_FORBIDDEN_SELL, ())
                    return
                if i.canSell(shopType=p.openShopType, compositeShopId=shopId) and not i.canSellToCompositeShop() and not canSellNormalToCompositeShop:
                    p.showGameMsg(GMDD.data.COMPOSITESHOP_FORBIDDEN_SELL_SHOP, ())
                    return
                canSell, fameData = i.canSellToCompositeShopId(shopId)
                if canSell or canSellNormalToCompositeShop:
                    if compositeShop.confirmStatus:
                        if i.isRuneEquip() and getattr(i, 'runeData', ()):
                            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_COMPOSITESHOPCONFIRMPROXY_92, functorSell)
                        else:
                            functorSell()
                    else:
                        gameglobal.rds.ui.compositeShopConfirm.show(nPage, nItem)
                else:
                    p.showGameMsg(GMDD.data.COMPOSITESHOP_FORBIDDEN_SELL_SHOP_BYBACK, ())
                return
            elif self.canSellToPrivateShop(i) and self.canOpenPrivateShop():
                p.getPrivateCompositeShop()
                return
            if gameglobal.rds.ui.wingAndMountUpgrade.mediator:
                if gameglobal.rds.ui.wingAndMountUpgrade.checkItemCanDrag(i):
                    gameglobal.rds.ui.wingAndMountUpgrade.setItem(const.RES_KIND_INV, nPage, nItem)
                    return
            if gameglobal.rds.ui.equipMixNew.mediator:
                gameglobal.rds.ui.equipMixNew.setNeedItem(nPage, nItem)
                return
            if gameglobal.rds.ui.wingAndMount.mediator:
                movePos = gameglobal.rds.ui.wingAndMount.searchEmptyPos()
                movePage = gameglobal.rds.ui.wingAndMount.selectIdx
                if i.isWingOrRide():
                    gameglobal.rds.ui.wingAndMount.moveItemFromBagIntoMine(nPage, nItem, movePage, movePos)
                    return
            if gameglobal.rds.ui.huiZhangRepair.mediator:
                gameglobal.rds.ui.huiZhangRepair.setRepairHuiZhang(nPage, nItem, i)
                return
            elif gameglobal.rds.ui.itemRecast.recastMed:
                gameglobal.rds.ui.itemRecast.addItemToRecast(i, nPage, nItem)
                return
            if gameglobal.rds.ui.treasureBoxWish.checkShowTreasureBoxWish(i.id):
                if gameglobal.rds.ui.treasureBoxWish.checkShowMessageBox(i, Item.SUBTYPE_2_ITEM_BOX, uiConst.CHECK_ONCE_TYPE_TREASURE_BOX_WISH_NORMAL):
                    self.showTreasureBoxWish(i, uiConst.CHECK_ONCE_TYPE_TREASURE_BOX_WISH_NORMAL)
                    return
                if gameglobal.rds.ui.treasureBoxWish.checkShowMessageBox(i, Item.SUBTYPE_2_CBT, uiConst.CHECK_ONCE_TYPE_TREASURE_BOX_WISH_CBT):
                    self.showTreasureBoxWish(i, uiConst.CHECK_ONCE_TYPE_TREASURE_BOX_WISH_CBT)
                    return
                if gameglobal.rds.ui.treasureBoxWish.checkShowMessageBox(i, Item.SUBTYPE_2_RAFFLE, uiConst.CHECK_ONCE_TYPE_TREASURE_BOX_WISH_RAFFLE):
                    self.showTreasureBoxWish(i, uiConst.CHECK_ONCE_TYPE_TREASURE_BOX_WISH_RAFFLE)
                    return
            if gameglobal.rds.ui.avoidDoingActivityTip.widget:
                if gameglobal.rds.ui.avoidDoingActivityTip.setItem(i):
                    return
            cidData = CID.data.get(i.id, {})
            sType = cidData.get('sType', 0)
            if sType == Item.SUBTYPE_2_SPRITE_FOOD:
                spriteExp = cidData.get('spriteExp', 0)
                familiarExp = cidData.get('familiarExp', 0)
                spriteIndex = gameglobal.rds.ui.summonedWarSprite.recordSpriteIndex
                if spriteExp:
                    gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX0, spriteIndex, 'feedExpMc')
                elif familiarExp:
                    gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX0, spriteIndex, 'feedPrivityMc')
                return
            elif sType == Item.SUBTYPE_2_SPRITE_SPECIAL:
                spriteIndex = gameglobal.rds.ui.summonedWarSprite.recordSpriteIndex
                gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX0, spriteIndex, 'feedPrivityMc')
                return
            if sType == Item.SUBTYPE_2_SPRITE_EGG and getattr(i, 'quality', 1) >= uiConst.DISAS_MESSAGEBOX_QUALITY:
                if not gameglobal.rds.ui.messageBox.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_OPEN_SPRITE_EGG):
                    msg = uiUtils.getTextFromGMD(GMDD.data.SURE_OPEN_HIGH_QUALITY_SPRITE_EGG, '')
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.useBagItem, nPage, nItem), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_OPEN_SPRITE_EGG)
                    return
            if sType == Item.SUBTYPE_2_CARD or sType == Item.SUBTYPE_2_CARD_ADD_DURATION:
                gameglobal.rds.ui.cardSystem.useCardItem(i, nPage, nItem)
                return
            elif sType == Item.SUBTYPE_2_CARD_SPECIAL_WASH:
                gameglobal.rds.ui.cardChange.showSpecialChange(i, nPage, nItem)
                return
            elif sType == Item.SUBTYPE_2_RANDOM_LOTTERY:
                gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_LOTTERY)
                return
            elif sType == Item.SUBTYPE_2_TURN_OVER_CARD:
                gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_TURN_OVER_CARD)
                return
            elif sType == Item.SUBTYPE_2_RANDOM_CARD_DRAW:
                gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_RANDOM_CARD_DRAW)
                return
            elif sType == Item.SUBTYPE_2_RANDOM_TREASURE_BAG_CONSUME:
                gameglobal.rds.ui.randomTreasureBagMain.show(bagId=cidData.get('randomTBId', 0), enableScrollToCurBag=True)
                return
            elif sType == Item.SUBTYPE_2_QEUIP_ENHANCE_ITEM:
                gameglobal.rds.ui.awakeRecast.show(i.id)
                return
            elif sType == Item.SUBTYPE_2_SPRITE_XIU_LIAN_ITEM and gameglobal.rds.ui.summonedWarSprite.checkXiuLianLvAndJinejie():
                gameglobal.rds.ui.summonedWarSprite.show(uiConst.WAR_SPRITE_TAB_INDEX3)
                return
            elif sType == Item.SUBTYPE_2_SELECT_TO_OPEN_BOX:
                gameglobal.rds.ui.selectOpenBox.show(i.id, nPage, nItem)
                return
            elif gameglobal.rds.ui.mail.mediator and gameglobal.rds.ui.mail.curTab == 1:
                return
            if gameglobal.rds.ui.equipEnhance.mediator:
                if i.isEquip():
                    if not i.isYaoPei() and i.getMaxEnhLv(p):
                        gameglobal.rds.ui.equipEnhance.setItem(nPage, nItem, uiConst.EQUIP_FUNC_ENHANCE, 0, i)
                    else:
                        p.showGameMsg(GMDD.data.ITEM_ENHANCE_FORBID, ())
                else:
                    if gameglobal.rds.ui.equipEnhance.isItemInView(nPage, nItem):
                        return
                    pos = gameglobal.rds.ui.equipEnhance.findEmptyPos()
                    if hasattr(i, 'type') and i.type == Item.BASETYPE_ENHANCE:
                        gameglobal.rds.ui.equipEnhance.setItem(nPage, nItem, 0, pos, i)
                    else:
                        p.showGameMsg(GMDD.data.ITEM_ENHANCE_FORBID, ())
            elif gameglobal.rds.ui.equipSuit.activateMediator:
                gameglobal.rds.ui.equipSuit.setItem(nPage, nItem, 0, 0, i)
            elif gameglobal.rds.ui.equipFeed.mediator:
                if i.isEquip():
                    pos = gameglobal.rds.ui.equipFeed.findEmptyPos()
                    if pos != -1:
                        if pos == 0 or pos > 0 and ED.data.get(i.id, {}).get('canBeFeed', 0):
                            gameglobal.rds.ui.equipFeed.setItem(nPage, nItem, 0, pos, i)
                    else:
                        gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_INVENTORYPROXY_2604)
            elif gameglobal.rds.ui.dyePlane.isShow:
                gameglobal.rds.ui.dyePlane.setEquip(nPage, nItem, i, const.RES_KIND_INV)
            elif gameglobal.rds.ui.dyeReset.isShow:
                gameglobal.rds.ui.dyeReset.setEquip(nPage, nItem, i, const.RES_KIND_INV)
            elif i.isGuildDonateItem():
                gameglobal.rds.ui.guildDonate.show()
            elif i.isSkillAppearanceItem():
                item = p.inv.getQuickVal(nPage, nItem)
                gameglobal.rds.ui.skillAppearanceConfirm.onUseItem(item)
            elif i.isActEffectAppearanceItem():
                item = p.inv.getQuickVal(nPage, nItem)
                gameglobal.rds.ui.actEffectAppearanceConfirm.onUseItem(item)
            elif i.isJingJie():
                gameglobal.rds.ui.roleInfo.show(tabIdx=uiConst.ROLEINFO_TAB_JINGJIE)
            elif i.isEquipSoulStar():
                if not gameglobal.rds.configData.get('enableEquipSoul', False):
                    return
                gameglobal.rds.ui.equipSoul.show(True)
            elif i.type == Item.BASETYPE_FURNITURE:
                if gameglobal.rds.ui.homeEditor.isInHomeEditorMode():
                    if i.hasLatch():
                        p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                        return
                    if i.isExpireTTL():
                        return
                    gameglobal.rds.ui.homeEditor.useFurniture(i, nPage, nItem, const.RES_KIND_INV)
                else:
                    p.showGameMsg(GMDD.data.FURNITURE_NOT_USE, ())
            else:
                if gameglobal.rds.configData.get('enableHierogram', False) and not gameglobal.rds.ui.equipChange.mediator:
                    if i.isHieroEquip():
                        if gameglobal.rds.ui.roleInformationHierogram.isLegitimateSlot(uiConst.HIERO_CLICK_BAG_ITEM, uiConst.HIERO_TYPE_EQUIP):
                            p.cell.equipHieroEquipment(nPage, nItem)
                        return
                    if i.isHieroCrystal():
                        hieroType = p.getRuneData(i.id, 'runeType', 0)
                        if not hieroType:
                            return
                        if gameglobal.rds.ui.roleInformationHierogram.isLegitimateSlot(uiConst.HIERO_CLICK_BAG_ITEM, hieroType):
                            part = gameglobal.rds.ui.roleInformationHierogram.getCrystalBestPart(hieroType)
                            if part == -1:
                                return
                            if not i.isForeverBind():
                                msg = GMD.data.get(GMDD.data.RUNE_EQUIP_BIND_TIP, {}).get('text', gameStrings.TEXT_INVENTORYPROXY_2658)
                                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.addHieroCrystal, hieroType, part, nPage, nItem))
                            else:
                                p.cell.addHieroCrystal(hieroType, part, nPage, nItem)
                        return
                else:
                    if i.isRuneEquip():
                        cellCmd.equipRuneEquipment(nPage, nItem)
                        return
                    if i.isRune():
                        runeType = p.getRuneData(i.id, 'runeType', 0)
                        if not runeType:
                            return
                        if p.runeBoard.runeEquip:
                            runeEquipPart = []
                            runeEquipSlotNum = p.runeBoard.runeEquip.getRuneEquipSlotNum(runeType)
                            for runeDataVal in p.runeBoard.runeEquip.runeData:
                                if runeDataVal.runeSlotsType == runeType:
                                    runeEquipPart.append(runeDataVal.part)

                            for part in range(runeEquipSlotNum):
                                if part not in runeEquipPart:
                                    if not i.isForeverBind():
                                        msg = GMD.data.get(GMDD.data.RUNE_EQUIP_BIND_TIP, {}).get('text', gameStrings.TEXT_INVENTORYPROXY_2658)
                                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(cellCmd.addRune, runeType, part, nPage, nItem))
                                    else:
                                        cellCmd.addRune(runeType, part, nPage, nItem)
                                    return

                            p.showGameMsg(GMDD.data.RUNE_ITEM_FULL, ())
                        return
                if i.isExploreEquip():
                    p.useExploreItem(i, nPage, nItem)
                    return
                if i.isRaffle():
                    gameglobal.rds.ui.raffle.show(i)
                    return
                if i.isMallDiscount():
                    mallDiscountShowTab = CID.data.get(i.id, {}).get('mallDiscountShowTab')
                    if mallDiscountShowTab and len(mallDiscountShowTab) == 2:
                        if mallDiscountShowTab in MCD.data:
                            gameglobal.rds.ui.tianyuMall.showMallTab(mallDiscountShowTab[0], mallDiscountShowTab[1])
                        return
                synthesizeData = ISD.data.get(i.getParentId(), None)
                if synthesizeData and synthesizeData['type'] not in (gametypes.ITEM_SYNTHESIZE_EQUIP, gametypes.ITEM_SYNTHESIZE_UPGRADE_EQUIP):
                    if synthesizeData['type'] == gametypes.ITEM_SYNTHESIZE_DIRECTIONAL:
                        if hasattr(i, 'isExpireTTL') and i.isExpireTTL():
                            p.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(i.id)['name'],))
                            return
                        self.setSynthesizeState()
                        self.SynthesizeSrcItemId = i.getParentId()
                        self.SynthesizeSrcItemPage = nPage
                        self.SynthesizeSrcItemPos = nItem
                        self.SynthesizeTgtMaterial = synthesizeData['tgtMaterial']
                        posCount = p.inv.posCountDict.get(self.page, 0)
                        for pos in xrange(0, posCount):
                            if not (self.SynthesizeSrcItemPage == self.page and self.SynthesizeSrcItemPos == pos):
                                self.updateSlotState(self.page, pos)

                    elif synthesizeData['type'] == 2:
                        p.useSynthesizeItem(nPage, nItem)
                else:
                    if i.type == Item.BASETYPE_EQUIP and p._isSchoolSwitch():
                        return
                    if p._isSoul() and gameglobal.rds.configData.get('enableCrossServerBag', False):
                        p.showGameMsg(GMDD.data.CROSS_BAG_ITEM_FORBIDDEN_DRAG, ())
                        return
                    return p.useBagItem(nPage, nItem)
            return

    def showTreasureBoxWish(self, i, onceType):
        gameglobal.rds.ui.treasureBoxWish.saveUseItemWishConfirm(i.id)
        seekId = SCD.data.get('treasureBoxWishSeekId', 0)
        msg = SCD.data.get('treasureBoxWishDesc', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(uiUtils.findPosWithAlert, seekId), isShowCheckBox=True, checkOnceType=onceType)

    def updateCurrentPageSlotState(self):
        if self.page == uiConst.BAG_PAGE_QUEST:
            return
        if self.mediator and utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            posCount = BigWorld.player().inv.posCountDict.get(self.page, 0)
            for pos in xrange(0, posCount):
                self.updateSlotState(self.page, pos)

    def getRenewalType(self):
        p = BigWorld.player()
        if ui.get_cursor_state() == ui.RENEWAL_STATE:
            if self.stateParams:
                if len(self.stateParams) == 2:
                    renewalItem = p.inv.getQuickVal(self.stateParams[0], self.stateParams[1])
                    if not renewalItem:
                        return -1
                    renewalType = CID.data.get(renewalItem.id, {}).get('renewalType', -1)
                    return renewalType
        return -1

    def checkItemDisabled(self, page, pos, item, kind = const.RES_KIND_INV):
        for proxyName in self.checkDisableProxys:
            if hasattr(self.uiAdapter, proxyName):
                proxy = getattr(self.uiAdapter, proxyName)
                if hasattr(proxy, 'isItemDisabled'):
                    isDisable = proxy.isItemDisabled(kind, page, pos, item)
                    if isDisable:
                        return True

        return False

    def updateSlotState(self, page, pos):
        if self.page != page or page == uiConst.BAG_PAGE_QUEST:
            return
        p = BigWorld.player()
        if not p:
            return
        item = p.inv.getQuickVal(page, pos)
        if item == const.CONT_EMPTY_VAL:
            self.setNewIconVisible(pos, False)
            return
        if item:
            self.setNewIconVisible(pos, item.uuid in self.newItemSequence)
        key = self._getKey(page, pos)
        if not self.binding.has_key(key):
            return
        state = self._getSlotState(page, pos, item)
        if gameglobal.rds.ui.compositeShop.mediator:
            gameglobal.rds.ui.compositeShop.refreshBuyItemDisplayData()
        yunChuiShopProxy = gameglobal.rds.ui.yunChuiShop
        if yunChuiShopProxy.mediator:
            yunChuiShopProxy.refreshBuyItemData()
        gameglobal.rds.ui.activityShop.refreshBuySetting()
        self.binding[key][0].Invoke('setSlotState', GfxValue(state))

    def _getSlotState(self, page, pos, item, kind = const.RES_KIND_INV):
        p = BigWorld.player()
        state = uiConst.ITEM_NORMAL
        if ui.get_cursor_state() == ui.RENEWAL_STATE:
            if self.stateParams:
                if len(self.stateParams) == 2:
                    renewalItem = p.inv.getQuickVal(self.stateParams[0], self.stateParams[1])
                    if not renewalItem:
                        return state
                    renewalType = CID.data.get(renewalItem.id, {}).get('renewalType', -1)
                    if page == self.stateParams[0] and pos == self.stateParams[1]:
                        return uiConst.ITEM_DISABLE
                    if item.getRenewalType() != renewalType or not item.canRenewalIndependent():
                        return uiConst.ITEM_GRAY
        if ui.get_cursor_state() == ui.RENEWAL_STATE2:
            if not item.isMallFashionRenewable():
                return uiConst.ITEM_GRAY
        if ui.get_cursor_state() == ui.RESET_FASHION_PROP:
            itemPos = ui.get_bindItemPos()
            if page == itemPos[1] and pos == itemPos[2]:
                return uiConst.ITEM_GRAY
            if not item.isFashionEquip() or not hasattr(item, 'fashionTransProp'):
                return uiConst.ITEM_GRAY
        if ui.get_cursor_state() == ui.IDENTIFY_ITEM_STATE:
            if self.stateParams:
                if len(self.stateParams) == 2:
                    identifyItem = p.inv.getQuickVal(self.stateParams[0], self.stateParams[1])
                    identifyType = CID.data.get(identifyItem.id, {}).get('identifyType', -1)
                    if not item.canBeIdentified() or item.getIdentifyType() != identifyType:
                        return uiConst.ITEM_DISABLE
                    if page == self.stateParams[0] and pos == self.stateParams[1]:
                        return uiConst.ITEM_DISABLE
        if ui.get_cursor_state() == ui.IDENTIFY_MANUAL_EQUIP_STATE:
            if self.stateParams:
                if len(self.stateParams) == 2:
                    identifyItem = p.inv.getQuickVal(self.stateParams[0], self.stateParams[1])
                    if not identifyItem:
                        return state
                    equipIdentifyType = CID.data.get(identifyItem.id, {}).get('equipIdentifyType', -1)
                    equipIdentifyMinLv = CID.data.get(identifyItem.id, {}).get('equipIdentifyMinLv', -1)
                    equipIdentifyMaxLv = CID.data.get(identifyItem.id, {}).get('equipIdentifyMaxLv', -1)
                    realItemId = MERRD.data.get(item.id, {}).get('targetEquipId', 0)
                    if not realItemId:
                        return uiConst.ITEM_DISABLE
                    realItem = Item(realItemId)
                    if not realItem.isManualEquip():
                        return uiConst.ITEM_DISABLE
                    if getattr(realItem, 'equipType', None) != equipIdentifyType:
                        return uiConst.ITEM_DISABLE
                    if getattr(realItem, 'lvReq', 0) > equipIdentifyMaxLv or getattr(realItem, 'lvReq', 0) < equipIdentifyMinLv:
                        return uiConst.ITEM_DISABLE
        if ui.get_cursor_state() == ui.CHANGE_BIND_STATE:
            if item.getBindConvertId() == 0:
                return uiConst.ITEM_DISABLE
        if ui.get_cursor_state() == ui.CHANGE_OWNER_STATE:
            if item.type == Item.BASETYPE_EQUIP_GEM and not item.ownedBy(BigWorld.player().gbId):
                return uiConst.ITEM_NORMAL
            else:
                return uiConst.ITEM_DISABLE
        if ui.get_cursor_state() == ui.ADD_STAR_EXP_STATE:
            if not item.isEquip():
                return uiConst.ITEM_DISABLE
        if self.page == uiConst.BAG_PAGE_QUEST:
            if not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                return uiConst.EQUIP_NOT_USE
            else:
                return uiConst.ITEM_NORMAL
        if self.filterSubtype > 0 and getattr(item, 'cstype', 0) != self.filterSubtype:
            state = uiConst.ITEM_DISABLE
        elif not self.isfilter(item):
            state = uiConst.ITEM_GRAY
        elif self.checkItemDisabled(page, pos, item, kind):
            state = uiConst.ITEM_DISABLE
        elif self.isDyePlaneState and self.uiAdapter.dyePlane.isInDyePlane(page, pos, const.RES_KIND_INV):
            state = uiConst.ITEM_DISABLE
        elif self.isSynthesizeState and item.getParentId() not in self.SynthesizeTgtMaterial:
            state = uiConst.ITEM_GRAY
        elif kind == const.RES_KIND_INV and self.isDisasState and not item.canDisass():
            state = uiConst.ITEM_DISABLE
        elif kind == const.RES_KIND_INV and self.isDisassembleState and not item.canDisassemble():
            state = uiConst.ITEM_DISABLE
        elif (self.isDyeState or self.isDyePlaneState) and not self.isShowInDyeState(item):
            state = uiConst.ITEM_GRAY
        elif self.isSignEquipState and not item.isCanSign():
            state = uiConst.ITEM_DISABLE
        elif item.isMallFashionRenewable() and item.isExpireTTL():
            state = uiConst.EQUIP_EXPIRE_TIME_RE
        elif not item.isMallFashionRenewable() and item.isExpireTTL():
            state = uiConst.EQUIP_EXPIRE_TIME
        elif not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
            state = uiConst.EQUIP_NOT_USE
        elif not self.checkLastWeekActivation(item):
            state = uiConst.EQUIP_NOT_USE
        elif item.type == Item.BASETYPE_EQUIP and (hasattr(item, 'cdura') and item.cdura == 0 or item.canEquip(p, item.whereEquip()[0])):
            state = uiConst.EQUIP_BROKEN
        elif hasattr(item, 'shihun') and item.shihun == True:
            state = uiConst.EQUIP_SHIHUN_REPAIR
        elif hasattr(item, 'valuableLatchOfTime') and item.valuableLatchOfTime > p.getServerTime():
            state = uiConst.ITEM_LATCH_TIME
        else:
            state = uiConst.ITEM_NORMAL
        if state == uiConst.ITEM_NORMAL:
            if item.isLatchOfTime():
                state = uiConst.ITEM_LATCH_TIME
            elif hasattr(item, 'latchOfCipher'):
                state = uiConst.ITEM_LATCH_CIPHER
        elif item.isLatchOfTime():
            state = uiConst.ITEM_LATCH_TIME * 1000 + state
        elif hasattr(item, 'latchOfCipher'):
            state = uiConst.ITEM_LATCH_CIPHER * 1000 + state
        return state

    def showWarnEffect(self, pos, visible):
        if self.mediator:
            self.mediator.Invoke('showWarnEffect', (GfxValue(pos), GfxValue(visible)))

    def setNewIconVisible(self, pos, isVisible):
        if self.mediator:
            self.mediator.Invoke('setNewIconVisible', (GfxValue(pos), GfxValue(isVisible)))

    def openTempBag(self):
        if self.mediator:
            self.mediator.Invoke('openTempBag')
        elif gameglobal.rds.ui.itemPushUse.isClickPush or gameglobal.rds.ui.itemPushUse.isActionClick:
            self.show()
            BigWorld.callback(1, Functor(self.openTempBag))

    def forceUpdateTempBag(self):
        self.closeTempBag()
        self.openTempBag()
        self.updateTempBagNum()

    def updateTempBagNum(self):
        self.tempBagNum = const.TEMP_BAG_WIDTH * const.TEMP_BAG_HEIGHT - BigWorld.player().tempBag.countBlank(0)
        if self.mediator:
            self.mediator.Invoke('setTempBagNum', GfxValue(self.tempBagNum))
        if gameglobal.rds.ui.systemButton.mediator:
            gameglobal.rds.ui.systemButton.showInventoryNewItem()

    def updateMallTempBagNum(self):
        self.tempMallBagNum = const.MALL_BAG_WIDTH * const.MALL_BAG_HEIGHT - BigWorld.player().mallBag.countBlank(0)
        if self.mediator:
            self.mediator.Invoke('setMallTempBagNum', GfxValue(self.tempMallBagNum))
        if gameglobal.rds.ui.systemButton.mediator:
            gameglobal.rds.ui.systemButton.showInventoryNewItem()

    def closeTempBag(self):
        if self.mediator:
            self.mediator.Invoke('closeTempBag')

    def onSelectedType(self, *arg):
        itemFilter = int(arg[3][0].GetNumber())
        if not (self.itemFilter in (uiConst.FILTER_ITEM_BAIT, uiConst.FILTER_ITEM_FURNITURE) and itemFilter == uiConst.FILTER_ITEM_ALL):
            self.itemFilter = itemFilter
        self.updateCurrentPageSlotState()
        gameglobal.rds.ui.storage.updateCurrentPageSlotState()

    def setItemFilter(self, filterValue):
        self.itemFilter = filterValue
        self.updateCurrentPageSlotState()
        gameglobal.rds.ui.storage.updateCurrentPageSlotState()

    def isfilter(self, item):
        if self.itemFilter == uiConst.FILTER_ITEM_EQUIP:
            if item.type == Item.BASETYPE_EQUIP and item.equipType in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_ARMOR, Item.EQUIP_BASETYPE_JEWELRY):
                return True
        elif self.itemFilter == uiConst.FILTER_ITEM_FASHION:
            if item.type == Item.BASETYPE_EQUIP and item.equipType == Item.EQUIP_BASETYPE_FASHION:
                return True
        elif self.itemFilter == uiConst.FILTER_ITEM_POTION:
            if item.type == Item.BASETYPE_CONSUMABLE and item.cstype == Item.SUBTYPE_2_POTION:
                return True
        elif self.itemFilter == uiConst.FILTER_ITEM_MATERIAL:
            if item.type == Item.BASETYPE_MATERIAL:
                return True
        elif self.itemFilter == uiConst.FILTER_ITEM_BAIT:
            if getattr(item, 'cstype', 0) == Item.SUBTYPE_2_FISHING_BAIT:
                return True
        elif self.itemFilter == uiConst.FILTER_ITEM_MIGRATE_FOBBIDDEN:
            unbindItemList = MCD.data.get('unbindItemList', [])
            blacklist = self._getMigrateBlacklist()
            if not item.bindType == 1 and item.id not in unbindItemList or item.id in blacklist:
                return True
        elif self.itemFilter == uiConst.FILTER_ITEM_CROSS_SERVER:
            if ID.data.get(item.id, {}).get('canTakeToCrossServer', 0):
                return True
        elif self.itemFilter == uiConst.FILTER_ITEM_FURNITURE:
            if item.type == Item.BASETYPE_FURNITURE and not gameglobal.rds.ui.homeEditor.isFurnitureUsedOut(item):
                return True
        else:
            return True
        return False

    def _getMigrateBlacklist(self):
        blacklist = []
        ret = MCD.data.get('itemHoldMax', [])
        for item in ret:
            blacklist.append(item[0])

        return blacklist

    def onOpenCompose(self, *arg):
        if gameconfigCommon.enableEquipChangeGemLvUp():
            checkshowTime, duration = SCD.data.get('equipChangeRedPointShowTime', (1557334680, 518400))
            if checkshowTime < utils.getNow() <= checkshowTime + duration:
                self.uiAdapter.equipChange.showRedPoint = True
            self.uiAdapter.equipChange.show(uiConst.EQUIPCHANGE_TAB_GEM, 1)
            return
        if gameglobal.rds.ui.equipChange.mediator:
            BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
            return
        if gameglobal.rds.ui.runeLvUp.mediator:
            gameglobal.rds.ui.runeLvUp.hide()
        else:
            gameglobal.rds.ui.runeLvUp.show(BigWorld.player().id)

    @ui.checkEquipChangeOpen()
    def onDisassembleItem(self, *arg):
        if self.isDisassembleState:
            self.clearDisassembleState()
        else:
            if not gameglobal.rds.configData.get('enableDisassembleEquip', False):
                BigWorld.player().showGameMsg(GMDD.data.DISASSEMBLE_NOT_OPEN, ())
                return
            self.setDisassembleState()

    def onOpenTempBag(self, *arg):
        self.openTempBagByType(arg[3][0].GetString())

    def openTempBagByType(self, btype):
        if btype == uiConst.INVENTORY_TEMP_BAG_MATERIAL and not gameglobal.rds.configData.get('enableMaterialBag', False):
            BigWorld.player().showGameMsg(GMDD.data.MATERIAL_BAG_FUNCTION_FORBIDEN, ())
            return
        if btype == uiConst.INVENTORY_TEMP_BAG_MATERIAL and gameglobal.rds.configData.get('enableNewMaterialBag', False):
            gameglobal.rds.ui.meterialBag.show()
        else:
            self.openSackBagByType(btype)
        self.closeTempBag()
        if gameglobal.rds.ui.fashionBag.mediator:
            gameglobal.rds.ui.fashionBag.hide()

    def openSackBagByType(self, btype):
        self.tempBagType = btype
        if self.tempBagMediator == None:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INVENTORY_TEMP_BAG)
        if self.tempBagMediator != None:
            self.tempBagMediator.Invoke('show')

    def onGetTempBagInitData(self, *arg):
        ret = {}
        ret['bagType'] = self.tempBagType
        ret['isActived'] = BigWorld.player().materialBagEnabled
        ret['autoSortState'] = self.isAutoArrangeMaterialBag
        return uiUtils.dict2GfxDict(ret)

    def onCloseInvTempBag(self, *arg):
        if gameglobal.rds.ui.meterialBag.mediator and gameglobal.rds.configData.get('enableNewMaterialBag', False):
            gameglobal.rds.ui.meterialBag.hide()
        self.closeMaterialBag()
        if gameglobal.rds.ui.fashionBag.mediator:
            gameglobal.rds.ui.fashionBag.hide()
        if self.mediator:
            self.mediator.Invoke('resetTempBagFlag')

    def closeMaterialBag(self):
        if self.tempBagMediator:
            self.tempBagMediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INVENTORY_TEMP_BAG)

    def onArrangeMeterialBag(self, *arg):
        if self.isAutoArrangeMaterialBag:
            BigWorld.player().base.sortMaterialBag()
            self.updateAutoSortMaterialBag(False)
            BigWorld.callback(SYSCD.data.get('autoSortInvCD', 30), Functor(self.updateAutoSortMaterialBag, True))

    def updateAutoSortMaterialBag(self, flag):
        self.isAutoArrangeMaterialBag = flag
        if self.tempBagMediator:
            self.tempBagMediator.Invoke('setAutoArrangeBtnState', GfxValue(flag))

    @ui.checkEquipChangeOpen()
    @ui.callInCD(1)
    def onAllInv2MaterialBag(self, *arg):
        BigWorld.player().base.allInv2MaterialBag()

    def onClearPassword(self, *arg):
        p = BigWorld.player()
        if not p.hasInvPassword:
            p.showTopMsg(gameStrings.TEXT_INVENTORYPROXY_3101)
        else:
            gameglobal.rds.ui.clearPassword.show()

    def confirmClearPassword(self):
        p = BigWorld.player()
        p.base.resetCipher()

    def chooseColorCard(self, page, pos):
        self.dyeItemPage = page
        self.dyeItemPos = pos
        if ui.get_cursor_state() != ui.TARGET_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.TARGET_STATE)
            ui.set_cursor(cursor.dye)
            ui.lock_cursor()
        p = BigWorld.player()
        self.isDyeState = True
        posCount = p.inv.posCountDict.get(self.page, 0)
        for pos in xrange(0, posCount):
            if not (self.dyeItemPage == self.page and self.dyeItemPos == pos):
                self.updateSlotState(self.page, pos)

    def useColorCard(self, equipPage, eqiupPos):
        p = BigWorld.player()
        equip = p.inv.getQuickVal(equipPage, eqiupPos)
        if equip.isCanDye():
            if self.isDyeState:
                p.cell.useColorCard(const.RES_KIND_INV, self.dyeItemPage, self.dyeItemPos, equipPage, eqiupPos)
                self.dyeItemPage = const.CONT_NO_PAGE
                self.dyeItemPos = const.CONT_NO_POS
                self.isDyeState = False
                if ui.get_cursor_state() == ui.TARGET_STATE:
                    ui.reset_cursor()
                self.updateCurrentPageSlotState()

    def updateBagSlot(self, count):
        self.invBagSlot = count
        if self.mediator:
            self.mediator.Invoke('updateBagSlot', GfxValue(self.invBagSlot))

    def onEnlargeSlot(self, *arg):
        slotIdx = int(arg[3][0].GetNumber())
        config = SCD.data.get('invEnlargeCost', [])
        if len(config) > slotIdx and slotIdx != -1:
            data = config[slotIdx]
            if data != None:
                p = BigWorld.player()
                needBindCash = data[0]
                itemCount = data[1]
                gameglobal.rds.ui.expandPay.bindCash = needBindCash
                if itemCount == 0:
                    gameglobal.rds.ui.expandPay.expandType = uiConst.EXPAND_INVENTORY_EXPAND
                    self.showPayMessage(needBindCash)
                else:
                    gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_INVENTORY_EXPAND, arg[3][0].GetNumber())

    def showPayMessage(self, needMoney):
        msg = GMD.data.get(GMDD.data.NEED_CONSUME_BINDCASH, {}).get('text', gameStrings.TEXT_INVENTORYPROXY_3159)
        msg = msg % needMoney
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, gameglobal.rds.ui.expandPay.onEnlargeBag)

    def isShowInDyeState(self, item):
        if item:
            if self.isDyePlaneState:
                return item.isCanDye()
            if self.isDyeState:
                p = BigWorld.player()
                if self.dyeItemPage != const.CONT_NO_PAGE and self.dyeItemPos != const.CONT_NO_POS:
                    i = p.inv.getQuickVal(self.dyeItemPage, self.dyeItemPos)
                    if i:
                        if i.isDye():
                            return item.isCanDye() and getattr(item, 'dyeMaterials', [])
                        if i.isRongGuang():
                            if i.getRongGuangType() == Item.CONSUME_RONGGUANG_CLEAN:
                                return getattr(item, 'rongGuang', [])
                            else:
                                return item.isCanRongGuang()
                        if getattr(i, 'cstype', 0) == Item.SUBTYPE_2_RUBBING_CLEAN:
                            return item.isCanRubbing() and getattr(item, 'rubbing', 0)
        return False

    def onPopWarning(self, *arg):
        page = int(arg[3][0].GetNumber())
        event = arg[3][1].GetString()
        p = BigWorld.player()
        if page == const.MATERIAL_BAG_BIND_ID:
            if event == 'unLatchItem':
                p.showGameMsg(GMDD.data.UNLATCH_IN_MATERAIL_BAG_FORBIDDEN, ())
            elif event == 'latchTimeItem':
                p.showGameMsg(GMDD.data.LATCH_TIME_IN_MATERAIL_BAG_FORBIDDEN, ())
            elif event == 'latchChipherItem':
                p.showGameMsg(GMDD.data.LATCH_CHIPHER_IN_MATERAIL_BAG_FORBIDDEN, ())

    def onOpenFashionBag(self, *args):
        if not gameglobal.rds.ui.fashionBag.mediator:
            self.closeTempBag()
            self.closeMaterialBag()
            if self.mediator:
                self.mediator.Invoke('resetTempBagFlag')
        if gameglobal.rds.ui.fashionBag.mediator:
            gameglobal.rds.ui.fashionBag.hide()
        else:
            gameglobal.rds.ui.fashionBag.askForShow()

    def hide(self, destroy = True):
        if self.isDyePlaneState:
            self.uiAdapter.dyePlane.close()
            return
        self.clearWidget()
        if destroy:
            self.reset()

    def onInventoryItemClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            p = BigWorld.player()
            if i.isRuneEquip():
                cellCmd.equipRuneEquipment(nPage, nItem)
                return
            if i.isRune():
                runeType = p.getRuneData(i.id, 'runeType', 0)
                if not runeType:
                    return
                if p.runeBoard.runeEquip:
                    runeEquipPart = []
                    runeEquipSlotNum = p.runeBoard.runeEquip.getRuneEquipSlotNum(runeType)
                    for runeDataVal in p.runeBoard.runeEquip.runeData:
                        if runeDataVal.runeSlotsType == runeType:
                            runeEquipPart.append(runeDataVal.part)

                    for part in range(runeEquipSlotNum):
                        if part not in runeEquipPart:
                            cellCmd.addRune(runeType, part, nPage, nItem)
                            return

                    p.showGameMsg(GMDD.data.RUNE_ITEM_FULL, ())
                return
            if i.isExploreEquip():
                p.useExploreItem(i, nPage, nItem)
                return
            synthesizeData = ISD.data.get(i.getParentId(), None)
            if synthesizeData and synthesizeData['type'] not in (gametypes.ITEM_SYNTHESIZE_EQUIP, gametypes.ITEM_SYNTHESIZE_UPGRADE_EQUIP):
                if synthesizeData['type'] == gametypes.ITEM_SYNTHESIZE_DIRECTIONAL:
                    if hasattr(i, 'isExpireTTL') and i.isExpireTTL():
                        p.showGameMsg(GMDD.data.ITEM_TTL_EXPIRE, (ID.data.get(i.id)['name'],))
                        return
                    self.setSynthesizeState()
                    self.SynthesizeSrcItemId = i.getParentId()
                    self.SynthesizeSrcItemPage = nPage
                    self.SynthesizeSrcItemPos = nItem
                    self.SynthesizeTgtMaterial = synthesizeData['tgtMaterial']
                    posCount = p.inv.posCountDict.get(self.page, 0)
                    for pos in xrange(0, posCount):
                        if not (self.SynthesizeSrcItemPage == self.page and self.SynthesizeSrcItemPos == pos):
                            self.updateSlotState(self.page, pos)

                elif synthesizeData['type'] == 2:
                    p.useSynthesizeItem(nPage, nItem)
            else:
                if i.type == Item.BASETYPE_EQUIP and p._isSchoolSwitch():
                    return
                return p.useBagItem(nPage, nItem)
            return

    def onActiveMaterialBag(self, *arg):
        gameglobal.rds.ui.expandPay.show(uiConst.EXPAND_MATERIAL_BAG_ACTIVE, 0)

    def onGetEnableMaterialBag(self, *arg):
        flag = gameglobal.rds.configData.get('enableMaterialBag', False)
        ability = BigWorld.player().getAbilityData(utils.getAbilityKey(gametypes.ABILITY_MATERIAL_BAG_ON, None))
        return GfxValue(flag and ability)

    def onGetFunctionBtnTips(self, *arg):
        inventoryBtnTips = SYSCD.data.get('inventoryBtnTips', {})
        tipsDict = {'composeBtnTip': inventoryBtnTips.get('composeBtnTip', ''),
         'disasBtnTip': inventoryBtnTips.get('disasBtnTip', ''),
         'disassembleBtnTip': inventoryBtnTips.get('disassembleBtnTip', ''),
         'timeLockBtnTip': inventoryBtnTips.get('timeLockBtnTip', ''),
         'cipherBtnTip': inventoryBtnTips.get('cipherBtnTip', ''),
         'unBindBtnTip': inventoryBtnTips.get('unBindBtnTip', ''),
         'switchBindBtnTip': inventoryBtnTips.get('switchBindBtnTip', ''),
         'sortBtnTip': inventoryBtnTips.get('sortBtnTip', ''),
         'splitBtnTip': inventoryBtnTips.get('splitBtnTip', ''),
         'yunbiBtnTip': inventoryBtnTips.get('yunbiBtnTip', gameStrings.TEXT_INVENTORYPROXY_3296),
         'yunquanBtnTip': inventoryBtnTips.get('yunquanBtnTip', gameStrings.TEXT_INVENTORYPROXY_3297),
         'tianbiBtnTip': inventoryBtnTips.get('tianbiBtnTip', gameStrings.TEXT_INVENTORYPROXY_3298),
         'yunchuiBtnTip': inventoryBtnTips.get('yunchuiBtnTip', gameStrings.TEXT_INVENTORYPROXY_3299)}
        return uiUtils.dict2GfxDict(tipsDict, True)

    def updateFrozenPunishVisible(self):
        valueFrozenPunishVisible = False
        p = BigWorld.player()
        freezeCash = getattr(p, 'freezeCash')
        maxFreezeCash = getattr(p, 'maxFreezeCash')
        notEnoughCash = maxFreezeCash - freezeCash
        if freezeCash != 0 or notEnoughCash != 0:
            valueFrozenPunishVisible = True
        if self.mediator:
            self.mediator.Invoke('updateFrozenPunishIconVisible', GfxValue(valueFrozenPunishVisible))

    def onGetfrozenPunish(self, *arg):
        p = BigWorld.player()
        cash = getattr(p, 'cash')
        freezeCash = getattr(p, 'freezeCash')
        maxFreezeCash = getattr(p, 'maxFreezeCash')
        freezeCashBail = getattr(p, 'freezeCashBail')
        allCash = cash + freezeCash
        notEnoughCash = maxFreezeCash - freezeCash
        text = GMD.data.get(GMDD.data.FROZEN_PUNISH_TIPS, {}).get('text', gameStrings.TEXT_INVENTORYPROXY_3322)
        text = text % (cash,
         freezeCash,
         notEnoughCash,
         allCash)
        return GfxValue(gbk2unicode(text))

    def isEnableCrossBag(self, *arg):
        enable = self.checkCrossBagEnable()
        return GfxValue(enable)

    def canOpenPrivateShop(self):
        if gameglobal.rds.configData.get('enablePrivateYunChuiShop', False):
            if BigWorld.player().lv >= SCD.data.get('privateYunChuiShopMinLv', 17):
                return True
        return False

    def checkCrossBagEnable(self):
        p = BigWorld.player()
        minCrossLv = SCD.data.get('minCrossServerBagLv', 69)
        enable = gameglobal.rds.configData.get('enableCrossServerBag', False) and p.lv >= minCrossLv or len(gameglobal.rds.ui.crossServerBag._getCrossBagItems()) > 0 or p.gmMode
        return enable

    def onOpenCrossBag(self, *arg):
        if gameglobal.rds.ui.crossServerBag.isShow():
            gameglobal.rds.ui.crossServerBag.hide()
        elif self.checkCrossBagEnable():
            gameglobal.rds.ui.crossServerBag.show()

    def onGetMeterialBagName(self, *arg):
        bagName = SYSCD.data.get('meterialBagName', gameStrings.TEXT_INVENTORYPROXY_3350)
        return GfxValue(gbk2unicode(bagName))

    def onTempBagCheckBox(self, *arg):
        tempBagCheck = int(arg[3][0].GetNumber())
        AppSettings[TEMP_BAG_CHECKBOX_KEY] = tempBagCheck

    def onClickYunbiBtn(self, *arg):
        gameglobal.rds.ui.help.show(gameStrings.TEXT_INVENTORYPROXY_3296)

    def onClickYunquanBtn(self, *arg):
        gameglobal.rds.ui.help.show(gameStrings.TEXT_INVENTORYPROXY_3297)

    def onClickTianbiBtn(self, *arg):
        mall = gameglobal.rds.ui.tianyuMall
        if mall.mallMediator:
            mall.hide()
        mall.show()

    def onClickYunchuiBtn(self, *arg):
        if gameglobal.rds.configData.get('enablePrivateYunChuiShop', False):
            if not self.canOpenPrivateShop():
                BigWorld.player().showGameMsg(GMDD.data.YUN_CHUI_SHOP_NOT_AVALIBLE, ())
                return
        if gameglobal.rds.ui.yunChuiShop.mediator:
            if gameglobal.rds.ui.combineMall.widget:
                gameglobal.rds.ui.yunChuiShop.checkParentShow()
                gameglobal.rds.ui.yunChuiShop.hide()
        self.openYunChuiShop()

    def onClickYingLingBtn(self, *arg):
        if gameglobal.rds.ui.spriteMaterialBag.widget:
            gameglobal.rds.ui.spriteMaterialBag.hide()
        else:
            gameglobal.rds.ui.spriteMaterialBag.show()

    def openYunChuiShop(self):
        if gameglobal.rds.configData.get('enablePrivateYunChuiShop', False):
            if not self.canOpenPrivateShop():
                BigWorld.player().showGameMsg(GMDD.data.YUN_CHUI_SHOP_NOT_AVALIBLE, ())
                return
            BigWorld.player().getPrivateCompositeShop()
        else:
            gameglobal.rds.ui.help.show(gameStrings.TEXT_INVENTORYPROXY_3299)

    def checkLastWeekActivation(self, item):
        lastWeekActivation = BigWorld.player().lastWeekActivation
        itemData = ID.data.get(item.id, {})
        if itemData.has_key('lastWeekActivationReq'):
            if lastWeekActivation < itemData['lastWeekActivationReq'] and not self.checkUseItemOpenDays():
                return False
        if itemData.has_key('maxLastWeekActivationReq'):
            if lastWeekActivation > itemData['maxLastWeekActivationReq'] and not self.checkUseItemOpenDays():
                return False
        return True

    def checkUseItemOpenDays(self):
        openServerDayLimit = SCD.data.get('openServerDayLimit', 0)
        if openServerDayLimit and utils.getServerOpenDays() > openServerDayLimit:
            return False
        return True

    def isShow(self):
        if self.mediator:
            return True
        return False

    def onGetEnableSpriteMaterialBag(self, *arg):
        result = False
        return GfxValue(result)

    def onOpenRuneInv(self, *args):
        gamelog.info('jbx:onOpenRuneInv')
        self.uiAdapter.runeInv.show()

    def onGetEnableRuneInv(self, *args):
        return GfxValue(gameconfigCommon.enableHierogramBag() and BigWorld.player().checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_HIEROGRAM))
