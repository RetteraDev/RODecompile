#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildStorageProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gametypes
import ui
import uiConst
import uiUtils
import cursor
import events
from uiProxy import SlotDataProxy
from callbackHelper import Functor
from item import Item
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD
from cdata import guild_storage_data as GSD

class GuildStorageProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(GuildStorageProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'guildStorage'
        self.type = 'guildStorage'
        self.modelMap = {'getAuthorization': self.onGetAuthorization,
         'getResourceInfo': self.onGetResourceInfo,
         'setGuildStorageItem': self.onSetGuildStorageItem,
         'isInDragItem': self.onIsInDragItem,
         'donate': self.onDonate,
         'donateWithCoin': self.onDonateWithCoin,
         'donateReserve': self.onDonateReserve,
         'clickManager': self.onClickManager,
         'clickAuto': self.onClickAuto,
         'splitItem': self.onSplitItem,
         'fetchItem': self.onFetchItem,
         'fetchAssgin': self.onFetchAssgin,
         'cancelAssgin': self.onCancelAssgin,
         'everyOneFetch': self.onEveryOneFetch,
         'discardItem': self.onDiscardItem,
         'hasItem': self.onHasItem,
         'splitSlot': self.onSplitSlot,
         'getItemFetchFlag': self.onGetItemFetchFlag}
        self.mediator = None
        self.markerId = 0
        self.buildLv = 0
        self.isSplitState = False
        self.page = const.STORAGE_PAGE_LOW
        self.isResourcePanel = False
        self.infoDic = {}
        self.pageStamp = {}
        self.npcId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_STORAGE, self.hide)

    def show(self, markerId, npcId = 0):
        if not self.mediator:
            self.markerId = markerId
            self.npcId = npcId
            gameglobal.rds.ui.guild.hideAllGuildBuilding()
            BigWorld.player().checkSetPassword()
            gameglobal.rds.ui.inventory.show(layoutType=uiConst.LAYOUT_NPC_FUNC)
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_STORAGE, layoutType=uiConst.LAYOUT_NPC_FUNC)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_STORAGE:
            self.mediator = mediator
            self.refreshInitData()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_STORAGE)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        if gameglobal.rds.ui.guildMemberAssgin.mediator:
            gameglobal.rds.ui.guildMemberAssgin.hide()
        p = BigWorld.player()
        if p:
            p.cell.guildCloseContainer(gametypes.GUILD_BUILDING_STORAGE_ID)

    def reset(self):
        self.markerId = 0
        self.npcId = 0
        self.buildLv = 0
        self.page = const.STORAGE_PAGE_LOW
        self.isResourcePanel = False

    def refreshInitData(self):
        if self.mediator:
            guild = BigWorld.player().guild
            marker = guild.marker.get(self.markerId)
            buildValue = guild.building.get(marker.buildingNUID)
            self.buildLv = buildValue.level if buildValue else 0
            info = {}
            info['level'] = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % self.buildLv
            tabCount = const.GUILD_STORAGE_PAGE_NUM
            for i in range(1, const.GUILD_STORAGE_PAGE_NUM):
                posCount = guild.storage.posCountDict.get(i, 0)
                if posCount == 0:
                    tabCount = i
                    break

            info['tabCount'] = tabCount
            self.mediator.Invoke('refreshInitData', uiUtils.dict2GfxDict(info, True))

    def onGetAuthorization(self, *arg):
        return GfxValue(gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_STORAGE_MGR))

    def onGetResourceInfo(self, *arg):
        self.isResourcePanel = True
        self.refreshResourceInfo()

    def refreshResourceInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            info = {}
            baseData = GSD.data.get(self.buildLv, {})
            cash = guild.bindCash
            maxCash = guild._getMaxBindCash()
            baseCashLimit = baseData.get('bindCash', 0)
            info['cash'] = '%s/%s' % (format(cash, ','), format(maxCash, ','))
            info['cashTips'] = gameStrings.TEXT_GUILDSTORAGEPROXY_129 % (format(baseCashLimit, ','), format(maxCash - baseCashLimit, ','), format(maxCash, ','))
            wood = guild.wood
            maxWood = guild._getMaxWood()
            baseWoodLimit = baseData.get('wood', 0)
            info['wood'] = '%s/%s' % (format(wood, ','), format(maxWood, ','))
            info['woodTips'] = gameStrings.TEXT_GUILDSTORAGEPROXY_135 % (format(baseWoodLimit, ','), format(maxWood - baseWoodLimit, ','), format(maxWood, ','))
            mojing = guild.mojing
            maxMojing = guild._getMaxMojing()
            baseMojingLimit = baseData.get('mojing', 0)
            info['mojing'] = '%s/%s' % (format(mojing, ','), format(maxMojing, ','))
            info['mojingTips'] = gameStrings.TEXT_GUILDSTORAGEPROXY_141 % (format(baseMojingLimit, ','), format(maxMojing - baseMojingLimit, ','), format(maxMojing, ','))
            xirang = guild.xirang
            maxXirang = guild._getMaxXirang()
            baseXirangLimit = baseData.get('xirang', 0)
            info['xirang'] = '%s/%s' % (format(xirang, ','), format(maxXirang, ','))
            info['xirangTips'] = gameStrings.TEXT_GUILDSTORAGEPROXY_147 % (format(baseXirangLimit, ','), format(maxXirang - baseXirangLimit, ','), format(maxXirang, ','))
            info['repairRate'] = '%d%%' % (guild._getMaintainFeeRate() * 100)
            info['repairRateTips'] = GCD.data.get('maintainFeeTips', '')
            info['reserveCash'] = format(guild.reserveCash if hasattr(guild, 'reserveCash') else 0, ',')
            info['reserveBindCash'] = format(guild.reserveBindCash if hasattr(guild, 'reserveBindCash') else 0, ',')
            info['reserveCoin'] = format(guild.reserveCoin if hasattr(guild, 'reserveCoin') else 0, ',')
            otherRes = []
            maxOtherRes = guild._getMaxOtherRes()
            otherResList = GCD.data.get('otherResList', None)
            if otherResList:
                for itemId in otherResList:
                    itemInfo = uiUtils.getGfxItemById(itemId)
                    itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
                    ownNum = guild.otherRes.get(itemId, 0)
                    itemInfo['itemNum'] = format(ownNum, ',')
                    itemInfo['numTips'] = '%s/%s' % (format(ownNum, ','), format(maxOtherRes, ','))
                    otherRes.append(itemInfo)

            info['otherRes'] = otherRes
            self.mediator.Invoke('refreshResourceInfo', uiUtils.dict2GfxDict(info, True))

    def onSetGuildStorageItem(self, *arg):
        page = int(arg[3][0].GetNumber())
        self.isResourcePanel = False
        p = BigWorld.player()
        if not p.guild:
            return
        e = self._getEntity()
        if not e:
            return
        stamp = p.guild.storage.stamp[page]
        if stamp == 0:
            self.setGuildStorageItem(page)
        e.cell.turnGuildContainerPage(gametypes.GUILD_BUILDING_STORAGE_ID, page, stamp)

    def setGuildStorageItem(self, idx):
        p = BigWorld.player()
        self.setPage(idx)
        posCount = p.guild.storage.posCountDict.get(idx, 0)
        self.setSlotCount(posCount)
        for ps in xrange(p.guild.storage.posCount):
            it = p.guild.storage.getQuickVal(idx, ps)
            if it == const.CONT_EMPTY_VAL:
                self.removeItem(idx, ps)
            else:
                self.addItem(it, idx, ps)

    def refresh(self):
        self.setGuildStorageItem(self.page)

    def _getKey(self, page, pos):
        return 'guildStorage%d.slot%d' % (page, pos)

    def removeItem(self, page, pos):
        if self.page != page:
            return
        else:
            key = self._getKey(0, pos)
            if self.binding.get(key, None) is not None:
                data = GfxValue(0)
                data.SetNull()
                self.setAssginFlag(page, pos, 1)
                self.binding[key][1].InvokeSelf(data)
            return

    def setAssginFlag(self, page, pos, fetchFlag):
        if self.mediator:
            self.mediator.Invoke('setAssginFlag', (GfxValue(page), GfxValue(pos), GfxValue(fetchFlag)))

    def setPage(self, page):
        self.page = page

    def setSlotCount(self, slotCount):
        if self.mediator:
            self.mediator.Invoke('setSlotCount', GfxValue(slotCount))

    def addItem(self, item, page, pos):
        if self.page != page:
            return
        else:
            if item is not None:
                key = self._getKey(0, pos)
                fetchFlag = self.getFetchFlag(item)
                self.setAssginFlag(page, pos, fetchFlag)
                self.addRealItem(key, item)
                self.updateSlotState(page, pos)
            return

    def addRealItem(self, key, item):
        if self.binding.get(key, None) is not None:
            data = uiUtils.getGfxItem(item, location=const.ITEM_IN_GUILDSTORAGE)
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))

    def getFetchFlag(self, item):
        p = BigWorld.player()
        if item != const.CONT_EMPTY_VAL:
            if hasattr(item, 'gatype'):
                if item.gatype == gametypes.GUILD_STORAGE_ASSIGN_TYPE_MEMBER and item.toGbId == p.gbId:
                    return gametypes.GUILD_STORAGE_ASSIGN_TYPE_MEMBER
                if item.gatype == gametypes.GUILD_STORAGE_ASSIGN_TYPE_ALL:
                    return gametypes.GUILD_STORAGE_ASSIGN_TYPE_ALL
        return gametypes.GUILD_STORAGE_ASSIGN_TYPE_ADMIN

    def updateSlotState(self, page, pos):
        if self.page != page:
            return
        p = BigWorld.player()
        item = p.guild.storage.getQuickVal(page, pos)
        if item == const.CONT_EMPTY_VAL:
            return
        key = self._getKey(0, pos)
        if not self.binding.has_key(key):
            return
        if not gameglobal.rds.ui.inventory.isfilter(item):
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_GRAY))
        elif item.isMallFashionRenewable() and item.isExpireTTL():
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_EXPIRE_TIME_RE))
        elif not item.isMallFashionRenewable() and item.isExpireTTL():
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_EXPIRE_TIME))
        elif not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_NOT_USE))
        elif item.isLatchOfTime():
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_LATCH_TIME))
        elif hasattr(item, 'latchOfCipher'):
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_LATCH_CIPHER))
        elif item.type == Item.BASETYPE_EQUIP and (hasattr(item, 'cdura') and item.cdura == 0 or item.canEquip(p, item.whereEquip()[0])):
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_BROKEN))
        else:
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))

    def onIsInDragItem(self, *arg):
        return GfxValue(gameglobal.rds.ui.inDragStorageItem or gameglobal.rds.ui.inDragCommonItem or gameglobal.rds.ui.inDragFashionBagItem or gameglobal.rds.ui.inDragMaterialBagItem)

    def onDonate(self, *arg):
        if gameglobal.rds.ui.guildDonateReserve.mediator:
            gameglobal.rds.ui.guildDonateReserve.hide()
        gameglobal.rds.ui.guildDonate.show()

    def onDonateWithCoin(self, *args):
        gameglobal.rds.ui.guild.onDonateWithCoin()

    def onDonateReserve(self, *arg):
        if gameglobal.rds.ui.guildDonate.mediator:
            gameglobal.rds.ui.guildDonate.hide()
        gameglobal.rds.ui.guildDonateReserve.show()

    def onClickManager(self, *arg):
        gameglobal.rds.ui.guildResidentManager.showOrHide(self.markerId)

    def onClickAuto(self, *arg):
        BigWorld.player().cell.storageGuildSort()

    def onSplitItem(self, *arg):
        if self.isSplitState:
            self.clearSplitState()
        else:
            self.setSplitState()

    def clearSplitState(self):
        if self.isSplitState:
            self.isSplitState = False
            if ui.get_cursor_state() == ui.SPLIT_STATE:
                ui.reset_cursor()

    def setSplitState(self):
        self.uiAdapter.clearState()
        self.isSplitState = True
        if ui.get_cursor_state() != ui.SPLIT_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.SPLIT_STATE)
            ui.set_cursor(cursor.splitItem)
            ui.lock_cursor()

    def clearState(self):
        self.clearSplitState()

    def getSlotID(self, key):
        _, idPos = key.split('.')
        pos = int(idPos[4:])
        return (self.page, pos)

    def onFetchItem(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        sItem = p.guild.storage.getQuickVal(page, pos)
        if sItem:
            dstPg, dstPos = p.inv.searchBestInPages(sItem.id, sItem.cwrap, sItem)
            if dstPg != const.CONT_NO_PAGE:
                if sItem.cwrap > 1:
                    gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.WIDGET_GUILD_STORAGE, page, pos, -1, dstPg, dstPos)
                else:
                    p.cell.storageGuild2inv(page, pos, sItem.uuid, sItem.cwrap, sItem.id, dstPg, dstPos)
            else:
                p.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())

    def onFetchAssgin(self, *arg):
        key = arg[3][0].GetString()
        nPage, nPos = self.getSlotID(key)
        p = BigWorld.player()
        data = []
        for i in p.guild.member.keys():
            data.append((i,
             p.guild.member[i].role,
             p.guild.member[i].level,
             const.SCHOOL_DICT[p.guild.member[i].school]))

        gameglobal.rds.ui.guildMemberAssgin.show(nPage, nPos, data)

    def onCancelAssgin(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        sItem = p.guild.storage.getQuickVal(page, pos)
        if sItem:
            p.cell.storageGuildCancelAssign(page, pos, sItem.uuid)

    def onEveryOneFetch(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        sItem = p.guild.storage.getQuickVal(page, pos)
        if sItem:
            p.cell.storageGuildAssignAnyMember(page, pos, sItem.uuid)

    def onDiscardItem(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        sItem = p.guild.storage.getQuickVal(page, pos)
        if sItem:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_GUILDSTORAGEPROXY_373, Functor(p.cell.storageGuildDiscard, page, pos, sItem.uuid, sItem.cwrap))

    def onHasItem(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        i = p.guild.storage.getQuickVal(page, pos)
        if i == None:
            return GfxValue(False)
        else:
            return GfxValue(True)

    def onSplitSlot(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if not self.isSplitState:
            return
        else:
            p = BigWorld.player()
            item = p.guild.storage.getQuickVal(page, pos)
            if item == None:
                return
            if not item.isWrap():
                p.showGameMsg(GMDD.data.ITEM_SPLIT_FORBIDDEN_LESS, ())
                return
            dstPos = p.guild.storage.searchEmpty(self.page)
            if dstPos == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.GUILD_STORAGE_NO_POS, ())
                return
            gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.WIDGET_GUILD_STORAGE, page, pos)
            self.clearSplitState()
            return

    def onGetItemFetchFlag(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        page, pos = self.getSlotID(key)
        item = p.guild.storage.getQuickVal(page, pos)
        if hasattr(item, 'gatype'):
            return GfxValue(item.gatype)
        else:
            return GfxValue(gametypes.GUILD_STORAGE_ASSIGN_TYPE_ADMIN)

    def _getEntity(self):
        e = None
        if self.npcId:
            e = BigWorld.entities.get(self.npcId)
        else:
            e = BigWorld.player()
        return e

    def invItemToGuildStorage(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if srcItem:
            desItem = p.guild.storage.getQuickVal(nPageDes, nItemDes)
            if desItem and srcItem.id == desItem.id and srcItem.cwrap + desItem.cwrap > desItem.mwrap:
                p.showGameMsg(GMDD.data.SHOP_ITEM_WRAP_OVER, ())
                return
            if desItem and srcItem.id != desItem.id:
                p.showGameMsg(GMDD.data.ITEM_INTO_GUILD_STORAGE_FAILED, ())
                return
            if gameglobal.rds.configData.get('enableInventoryLock', False):
                p.getCipher(self.onInvItemToGuildStorage, (nPageSrc,
                 nItemSrc,
                 srcItem.cwrap,
                 nPageDes,
                 nItemDes))
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_STORAGE_PUT_HINT, gameStrings.TEXT_GUILDSTORAGEPROXY_436)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.inv2StorageGuild, nPageSrc, nItemSrc, srcItem.cwrap, nPageDes, nItemDes, ''))

    def onInvItemToGuildStorage(self, cipher, nPageSrc, nItemSrc, cwrap, nPageDes, nItemDes):
        msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_STORAGE_PUT_HINT, gameStrings.TEXT_GUILDSTORAGEPROXY_436)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.inv2StorageGuild, nPageSrc, nItemSrc, cwrap, nPageDes, nItemDes, cipher))

    @ui.uiEvent(uiConst.WIDGET_GUILD_STORAGE, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        elif self.isResourcePanel:
            return
        else:
            p = BigWorld.player()
            nItemDes = p.guild.storage.searchBestInGuildStorage(i.id, i.cwrap, self.page)
            if nItemDes == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.GUILD_STORAGE_NO_POS, ())
                return
            self.invItemToGuildStorage(nPage, nItem, self.page, nItemDes)
            return
