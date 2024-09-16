#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildDonateProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import events
import uiUtils
import ui
import uiConst
import gameconfigCommon
from uiProxy import SlotDataProxy
from callbackHelper import Functor
from guis.asObject import ASObject
from data import guild_config_data as GCD
from data import consumable_item_data as CID
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
from item import Item
DONATE_TYPE_GUILD = 0
DONATE_TYPE_SERVER = 1

class GuildDonateProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(GuildDonateProxy, self).__init__(uiAdapter)
        self.modelMap = {'setCash': self.onSetCash,
         'getCash': self.onGetCash,
         'donate': self.onDonate,
         'openInventory': self.onOpenInventory,
         'removeItem': self.onRemoveItem}
        self.mediator = None
        self.widget = None
        self.bindType = 'guildDonate'
        self.type = 'guildDonate'
        self.posMap = {}
        self.donateType = DONATE_TYPE_GUILD
        self.extraData = {}
        self.itemNum = {}
        self.cash = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_DONATE, self.hide)

    def reset(self):
        for key, val in self.posMap.items():
            page, pos = val
            self.posMap.pop(key)
            gameglobal.rds.ui.inventory.updateSlotState(page, pos)

        self.itemNum = {}
        self.bindingData = {}
        self.cash = 0
        self.donateType = DONATE_TYPE_GUILD
        self.extraData = {}

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_DONATE:
            self.mediator = mediator
            self.widget = ASObject(mediator).getWidget()
            self.refreshInfo()
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def refreshInfo(self):
        if not self.widget:
            return
        if self.donateType == DONATE_TYPE_GUILD:
            self.widget.title.textField.text = gameStrings.DONATE_GUILD_TITLE
            self.widget.subTitle.text = gameStrings.DONATE_GUILD_SUBTITLE
            self.widget.gainText.htmlText = ''
        elif self.donateType == DONATE_TYPE_SERVER:
            self.widget.title.textField.text = gameStrings.DONATE_SERVER_TITLE
            self.widget.subTitle.text = gameStrings.DONATE_SERVER_SUBTITLE
            self.widget.gainText.htmlText = ''
        self.updateDonateValue()

    def show(self, donateType = DONATE_TYPE_GUILD, extraData = {}):
        p = BigWorld.player()
        if donateType == DONATE_TYPE_SERVER:
            if not gameconfigCommon.enableCrossClanWarPreActivity():
                p.showGameMsg(GMDD.data.EXCITEMENT_FORBIDDEN_FUNC, ())
                return
        if donateType == DONATE_TYPE_GUILD:
            p.cell.queryGuildDonateWeeklyNum()
        if not p.guildNUID:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
            return
        else:
            if self.donateType != donateType:
                self.clearItem()
                self.reset()
            self.donateType = donateType
            if self.mediator:
                self.mediator.Invoke('swapPanelToFront')
                self.refreshInfo()
                BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_DONATE)
            self.onOpenInventory(None)
            return

    def clearWidget(self):
        self.mediator = None
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_DONATE)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def clearItem(self):
        for slot in range(const.GUILD_DONATE_ITEM_NUM_LIMIT):
            self.removeItem(0, slot)

    def onSetCash(self, *arg):
        try:
            cash = int(arg[3][0].GetNumber())
        except:
            return

        self.cash = cash
        self.updateDonateValue()

    def onGetCash(self, *arg):
        p = BigWorld.player()
        donateDailyMaxMoney = GCD.data.get('donateDailyMaxMoney', const.GUILD_DONATE_DAILY_MAX_MONEY)
        cash = donateDailyMaxMoney - p.guildDonateDaily
        if cash > p.cash:
            cash = p.cash
        info = {}
        info['cashMax'] = cash
        info['tips'] = gameStrings.TEXT_GUILDDONATEPROXY_128 % donateDailyMaxMoney
        return uiUtils.dict2GfxDict(info, True)

    def onDonate(self, *arg):
        p = BigWorld.player()
        itemIds = []
        itemCnts = []
        pages = []
        poses = []
        for key, val in self.bindingData.items():
            if key.find('guildDonate0') != -1 and val:
                it, pg, ps = p.inv.findItemByUUID(val.uuid)
                if it != const.CONT_EMPTY_VAL:
                    itemIds.append(it.id)
                    pages.append(pg)
                    poses.append(ps)
                    itemCnts.append(self.itemNum.get(key, val.cwrap))

        self.checkMaxRes(self.cash, itemIds, itemCnts, pages, poses)

    def checkMaxRes(self, cash, itemIds, itemCnts, pages, poses):
        if self.donateType == DONATE_TYPE_GUILD:
            self.guildDonateCheckMaxRes(cash, itemIds, itemCnts, pages, poses)
        elif self.donateType == DONATE_TYPE_SERVER:
            self.doServerDonate(cash, itemIds, itemCnts, pages, poses)

    def serverDonateCheckMaxRes(self, cash, itemIds, itemCnts, pages, poses):
        self.hide()

    def guildDonateCheckMaxRes(self, cash, itemIds, itemCnts, pages, poses):
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        mojing = 0
        xirang = 0
        wood = 0
        guildMoney = 0
        for i, itemId in enumerate(itemIds):
            pg, ps, itemCnt = pages[i], poses[i], itemCnts[i]
            it = p.inv.getQuickVal(pg, ps)
            if it.isMojing():
                mojing += itemCnt * CID.data.get(it.id, {}).get('num', 1)
            elif it.isXirang():
                xirang += itemCnt * CID.data.get(it.id, {}).get('num', 1)
            elif it.isWood():
                wood += itemCnt * CID.data.get(it.id, {}).get('num', 1)
            elif it.isGuildMoney():
                guildMoney += itemCnt * CID.data.get(it.id, {}).get('guildMoney', 0)

        resNames = []
        if cash + guildMoney and cash + guildMoney + guild.bindCash > guild._getMaxBindCash():
            resNames.append(gameStrings.TEXT_GUILDDONATEPROXY_182)
        if mojing and mojing + guild.mojing > guild._getMaxMojing():
            resNames.append(const.GUILD_RES_MOJING)
        if xirang and xirang + guild.xirang > guild._getMaxXirang():
            resNames.append(const.GUILD_RES_XIRANG)
        if wood and wood + guild.wood > guild._getMaxWood():
            resNames.append(const.GUILD_RES_WOOD)
        if not resNames:
            self.doDonate(cash, itemIds, itemCnts, pages, poses)
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_DONATE_ANYWAY_CONFIRM)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg % gameStrings.TEXT_CHATPROXY_403.join(resNames), Functor(self.doDonate, cash, itemIds, itemCnts, pages, poses), gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235)

    def doDonate(self, cash, itemIds, itemCnts, pages, poses):
        p = BigWorld.player()
        p.cell.guildDonate(cash, itemIds, itemCnts, pages, poses)
        p.cell.queryGuildDonateWeeklyNum()
        self.hide()

    def doServerDonate(self, cash, itemIds, itemCnts, pages, poses):
        p = BigWorld.player()
        p.cell.donateForClanWar(itemIds, itemCnts, pages, poses)
        p.cell.queryGuildDonateWeeklyNum()
        self.hide()

    def onOpenInventory(self, *arg):
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[11:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'guildDonate%d.slot%d' % (bar, slot)

    def setItem(self, srcBar, srcSlot, destBar, destSlot, item, num):
        self.removeItem(destBar, destSlot)
        key = self._getKey(destBar, destSlot)
        if self.binding.has_key(key):
            self.bindingData[key] = item
            self.itemNum[key] = num
            data = uiUtils.getGfxItemById(item.id, num)
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
            self.posMap[destBar, destSlot] = (srcBar, srcSlot)
            gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
            self.updateDonateValue()

    def removeItem(self, bar, slot):
        key = self._getKey(bar, slot)
        if self.binding.has_key(key):
            self.bindingData[key] = None
            self.itemNum[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            srcBar, srcSlot = self.posMap.get((bar, slot), (None, None))
            if srcBar != None:
                self.posMap.pop((bar, slot))
                gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
            self.updateDonateValue()

    def findEmptyPos(self):
        for i in xrange(6):
            key = (0, i)
            if not self.posMap.has_key(key):
                return i

        return -1

    def updateDonateValue(self):
        if self.mediator:
            p = BigWorld.player()
            if self.donateType == DONATE_TYPE_GUILD:
                donateValue = self.cash / GCD.data.get('donateContribRate', const.GUILD_DONATE_CONTRIB_RATE)
                for key, item in self.bindingData.items():
                    if item == None:
                        continue
                    if item.isMojing():
                        donateValue += self.itemNum[key] * CID.data.get(item.id, {}).get('num', 1) * GCD.data.get('mojingContrib', const.GUILD_DONATE_MOJING_CONTRIB)
                    elif item.isXirang():
                        donateValue += self.itemNum[key] * CID.data.get(item.id, {}).get('num', 1) * GCD.data.get('xirangContrib', const.GUILD_DONATE_XIRANG_CONTRIB)
                    elif item.isWood():
                        donateValue += self.itemNum[key] * CID.data.get(item.id, {}).get('num', 1) * GCD.data.get('woodContrib', const.GUILD_DONATE_WOOD_CONTRIB)
                    elif item.isGuildMoney():
                        donateValue += self.itemNum[key] * CID.data.get(item.id, {}).get('guildMoney', 0) / GCD.data.get('donateContribRate', const.GUILD_DONATE_CONTRIB_RATE)
                    elif item.isGuildOtherRes():
                        donateValue += self.itemNum[key] * CID.data.get(item.id, {}).get('contrib', 0)
                    elif item.isTianyucanjing():
                        donateValue += self.itemNum[key] * CID.data.get(item.id, {}).get('num', 1) * GCD.data.get('tianyucanjingContrib', const.GUILD_DONATE_MOJING_CONTRIB)

                donateValue = int(donateValue)
                donateMaxValue = GCD.data.get('guildDonateWeeklyMaxNum', 0)
                guildDonateWeeklyNum = p.guild.guildDonateWeeklyNum if p.guild else 0
                self.widget.gainText.htmlText = gameStrings.DONATE_GUILD_GAINTXT % (donateValue, donateMaxValue - guildDonateWeeklyNum)
                if donateValue == 0:
                    self.widget.gainText.htmlText = ''
            elif self.donateType == DONATE_TYPE_SERVER:
                serverDonateValue = 0
                donateValue = 0
                for key, item in self.bindingData.items():
                    if item == None:
                        continue
                    if item.isServerDonate():
                        serverDonateValue += self.itemNum[key] * CID.data.get(item.id, {}).get('serverContrib', 0)
                        donateValue += self.itemNum[key] * CID.data.get(item.id, {}).get('contrib', 0)

                self.widget.gainText.htmlText = gameStrings.DONATE_SERVER_GAINTXT % (donateValue, serverDonateValue)
                if donateValue == 0 and serverDonateValue == 0:
                    self.widget.gainText.htmlText = ''

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if self.donateType == DONATE_TYPE_GUILD:
                if (page, pos) in self.posMap.values():
                    return True
                if item.isMojing():
                    return False
                if item.isXirang():
                    return False
                if item.isWood():
                    return False
                if item.isGuildMoney():
                    return False
                if item.isGuildOtherRes():
                    return False
                if item.isWingWorldGuildMoney():
                    return False
            elif self.donateType == DONATE_TYPE_SERVER:
                if (page, pos) in self.posMap.values():
                    return True
                if item.isServerDonate():
                    return False
            return True
        else:
            return False

    @ui.uiEvent(uiConst.WIDGET_GUILD_DONATE, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            desPos = gameglobal.rds.ui.guildDonate.findEmptyPos()
            self.setInventoryItem(nPage, nItem, 0, desPos)
            return

    def setInventoryItem(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if srcItem:
            if self.donateType == DONATE_TYPE_SERVER and srcItem.isServerDonate():
                if srcItem.hasLatch():
                    p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                if srcItem.cwrap > 1:
                    gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.NUMBER_WIDGET_ITEM_GUILD_DONATE, nPageSrc, nItemSrc, nItemDes)
                else:
                    self.setItem(nPageSrc, nItemSrc, 0, nItemDes, srcItem, srcItem.cwrap)
            elif self.donateType == DONATE_TYPE_GUILD:
                if srcItem.isItemGuildDonate():
                    if srcItem.hasLatch():
                        p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                        return
                    if srcItem.cwrap > 1:
                        gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.NUMBER_WIDGET_ITEM_GUILD_DONATE, nPageSrc, nItemSrc, nItemDes)
                    else:
                        self.setItem(nPageSrc, nItemSrc, 0, nItemDes, srcItem, srcItem.cwrap)
                else:
                    p.showGameMsg(GMDD.data.GUILD_DONATE_ITEM_CONNOT, ())
