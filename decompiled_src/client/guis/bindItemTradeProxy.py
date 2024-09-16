#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bindItemTradeProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import utils
from callbackHelper import Functor
from guis import events
from guis import ui
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
BIT_MODE_NONE = 0
BIT_MODE_GIVE = 1
BIT_MODE_ACCEPT = 2
MAX_BAG_NUM = 24

class BindItemTradeProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(BindItemTradeProxy, self).__init__(uiAdapter)
        self.modelMap = {'cancelTrade': self.onCancelTrade,
         'getTradeData': self.onGetTradeData,
         'revertItem': self.onRevertItem,
         'confirmTrade': self.onConfirmTrade,
         'closeTradeRequest': self.onCloseTradeRequest,
         'getRequestData': self.onGetRequestData,
         'acceptRequest': self.onAcceptRequest,
         'ignoreAllRequests': self.onIgnoreAllRequests}
        self.mediator = None
        self.requestMediator = None
        self.bindType = 'bindItemTrade'
        self.type = 'bindItemTrade'
        self.widgetId = uiConst.WIDGET_BIND_ITEM_TRADE
        self.requestWidgetId = uiConst.WIDGET_BIND_ITEM_TRADE_REQUEST
        self.reset()
        self.traderQueue = {}
        self.traderCallbackHandler = {}
        self.distCheckHandler = None
        uiAdapter.registerEscFunc(self.widgetId, self.onCancelTrade)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.widgetId:
            self.mediator = mediator
            BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)
        elif widgetId == self.requestWidgetId:
            self.requestMediator = mediator

    def show(self, bitMode, peerId):
        if self.bitMode != BIT_MODE_NONE:
            return
        else:
            self.bitMode = bitMode
            self.peerId = peerId
            gameglobal.rds.ui.loadWidget(self.widgetId)
            if self.distCheckHandler:
                BigWorld.cancelCallback(self.distCheckHandler)
                self.distCheckHandler = None
            self.distCheckHandler = BigWorld.callback(0.5, self.checkTradeDist)
            return

    def checkTradeDist(self):
        p = BigWorld.player()
        tgt = BigWorld.entities.get(self.peerId, None)
        if not tgt:
            p.cell.itemGiveCancel()
        else:
            dist = p.position.distTo(tgt.position)
            if dist > const.MAKE_TRADE_DIST:
                p.cell.itemGiveCancel()
        if self.distCheckHandler:
            BigWorld.cancelCallback(self.distCheckHandler)
            self.distCheckHandler = None
        self.distCheckHandler = BigWorld.callback(0.5, self.checkTradeDist)

    def showRequest(self):
        gameglobal.rds.ui.loadWidget(self.requestWidgetId)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(self.widgetId)
        self.mediator = None
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
        if self.distCheckHandler:
            BigWorld.cancelCallback(self.distCheckHandler)
            self.distCheckHandler = None

    def reset(self):
        self.giveItems = [const.CONT_EMPTY_VAL] * MAX_BAG_NUM
        self.bitMode = BIT_MODE_NONE
        self.peerId = 0
        self.mSerial = 0
        self.tSerial = 0

    def getSlotID(self, key):
        bar, slotId = key.split('.')
        return (int(bar[13:]), int(slotId[4:]))

    def refreshRequest(self):
        if self.requestMediator:
            self.requestMediator.Invoke('refreshRequest')

    def onItemGiveRequest(self, peerId):
        p = BigWorld.player()
        if len(self.traderQueue) >= const.TRADE_MAX_PROPOSER:
            p.cell.itemGiveOver(peerId)
            return
        if self.traderQueue.has_key(peerId):
            p.cell.itemGiveOver(peerId)
            return
        t = utils.getNow()
        ent = BigWorld.entities.get(peerId)
        if not ent:
            return
        name = ent.roleName
        self.traderQueue[peerId] = (t, name)
        gameglobal.rds.sound.playSound(gameglobal.SD_32)
        self.traderCallbackHandler[peerId] = BigWorld.callback(60, Functor(self.autoCancelRequest, peerId, t))
        data = {'data': [peerId, self.traderQueue[peerId]],
         'startTime': t,
         'totalTime': 60}
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_BIND_ITEM_TRADE, data)
        if not p.inCombat:
            self.showRequest()

    def autoCancelRequest(self, who, time):
        if not self.traderQueue.has_key(who):
            return
        if self.traderQueue[who][0] != time:
            return
        ent = BigWorld.entities.get(who)
        if ent:
            ent.cell.itemGiveDate(BigWorld.player().id)
        self.removeQueueItem(who)

    def onItemGiveStart(self, peerId):
        self.show(BIT_MODE_GIVE, peerId)
        gameglobal.rds.ui.inventory.show()

    def onItemAcceptStart(self, peerId):
        self.show(BIT_MODE_ACCEPT, peerId)
        self.removeQueueItem(peerId)
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    @ui.uiEvent(uiConst.WIDGET_BIND_ITEM_TRADE, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        if self.bitMode == BIT_MODE_ACCEPT:
            return
        else:
            i = event.data['item']
            nPage = event.data['page']
            nItem = event.data['pos']
            if i == None:
                return
            pos = self.findFirstEmptySlot()
            if pos < 0:
                return
            self.bagItem2GiveItem(nPage, nItem, pos)
            return

    def onBagSlotToBindItemSlot(self, nPageSrc, nItemSrc, nItemDes):
        if self.bitMode == BIT_MODE_ACCEPT:
            return
        self.bagItem2GiveItem(nPageSrc, nItemSrc, nItemDes)

    def findFirstEmptySlot(self):
        for i, item in enumerate(self.giveItems):
            if item == const.CONT_EMPTY_VAL:
                return i

        return -1

    def bagItem2GiveItem(self, bagPage, bagPos, givePos):
        p = BigWorld.player()
        item = p.inv.getQuickVal(bagPage, bagPos)
        if not item:
            return
        if item.cwrap <= 1:
            BigWorld.player().cell.giveItem(bagPage, bagPos, givePos, 1)
            return
        gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.NUMBER_WIDGET_BIND_ITEM_TRADE, bagPage, bagPos, givePos)

    def onItemGive(self, pos, item, serial):
        self.giveItems[pos] = item
        self.mSerial = serial
        self.refreshItems()

    def onItemGiven(self, pos, item, serial):
        self.giveItems[pos] = item
        self.tSerial = serial
        self.refreshItems()

    def onGiveItemRevert(self, pos, serial):
        self.giveItems[pos] = const.CONT_EMPTY_VAL
        self.mSerial = serial
        self.refreshItems()

    def onItemGiveCancel(self):
        self.removeQueueItem(self.peerId)
        gameglobal.rds.sound.playSound(gameglobal.SD_3)
        self.hide()

    def onItemGiveFinal(self):
        if self.bitMode == BIT_MODE_GIVE:
            self.enableConfirm(False)
        elif self.bitMode == BIT_MODE_ACCEPT:
            self.enableConfirm(True)

    def onItemGiveFinish(self):
        self.hide()

    def onItemGiveItemFinish(self):
        pass

    def findItemByUUID(self, uuid):
        for i, item in enumerate(self.giveItems):
            if item and item.uuid == uuid:
                return item

    def refreshItems(self):
        if not self.mediator:
            return
        itemsArray = []
        for i, item in enumerate(self.giveItems):
            info = {}
            if item == const.CONT_EMPTY_VAL:
                info['empty'] = True
            else:
                info['empty'] = False
                info['pos'] = i
                info.update(uiUtils.getGfxItem(item, location=const.ITEM_IN_BIND_TRADE))
            itemsArray.append(info)

        self.mediator.Invoke('refreshItemsInfo', uiUtils.array2GfxAarry(itemsArray, True))

    def enableConfirm(self, enable):
        if not self.mediator:
            return
        self.mediator.Invoke('enableConfirm', GfxValue(enable))

    def removeQueueItem(self, peerId):
        if self.traderCallbackHandler.has_key(peerId):
            BigWorld.cancelCallback(self.traderCallbackHandler.pop(peerId))
        if self.traderQueue.has_key(peerId):
            data = {'data': [peerId, self.traderQueue[peerId]]}
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_BIND_ITEM_TRADE, data)
            self.traderQueue.pop(peerId)

    def onCancelTrade(self, *arg):
        self.hide()
        BigWorld.player().cell.itemGiveCancel()
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def onGetTradeData(self, *arg):
        ret = {}
        ent = BigWorld.entities.get(self.peerId)
        peerName = ent.roleName if ent else gameStrings.TEXT_BINDITEMTRADEPROXY_303
        ret['mode'] = self.bitMode
        ret['peerName'] = peerName
        return uiUtils.dict2GfxDict(ret, True)

    def onRevertItem(self, *arg):
        pos = int(arg[3][0].GetNumber())
        self.revertGiveItem(pos)

    def revertGiveItem(self, pos):
        BigWorld.player().cell.giveItemRevert(pos)

    @ui.callFilter(uiConst.CONFIRM_TRADE)
    @ui.checkInventoryLock()
    def onConfirmTrade(self, *arg):
        p = BigWorld.player()
        if self.bitMode == BIT_MODE_GIVE:
            p.cell.itemGiveFinal(self.mSerial, self.tSerial, p.cipherOfPerson)
        elif self.bitMode == BIT_MODE_ACCEPT:
            p.cell.itemAcceptFinal(self.mSerial, self.tSerial, p.cipherOfPerson)

    def onCloseTradeRequest(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.requestWidgetId)
        self.requestMediator = None

    def onGetRequestData(self, *arg):
        dataList = gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_BIND_ITEM_TRADE)
        pushData = [ item['data'] for item in dataList ]
        pushData.sort(key=lambda k: k[1][0])
        ret = []
        ret.append(gameStrings.TEXT_BINDITEMTRADEPROXY_340)
        ret.append(len(pushData))
        ret.append(gameStrings.TEXT_BINDITEMTRADEPROXY_342)
        playerData = []
        for item in pushData:
            playerInfo = {}
            playerInfo['name'] = item[1][1]
            playerInfo['remainTime'] = int(60 - (utils.getNow() - item[1][0]))
            playerInfo['peerId'] = item[0]
            playerData.append(playerInfo)

        ret.append(playerData)
        return uiUtils.array2GfxAarry(ret, True)

    def onAcceptRequest(self, *arg):
        peerId = int(arg[3][0].GetNumber())
        BigWorld.player().cell.itemGiveRequestAccept(peerId)

    def onIgnoreAllRequests(self, *arg):
        peerIdList = []
        for peerId in self.traderQueue:
            BigWorld.player().cell.itemGiveReject(peerId)
            peerIdList.append(peerId)

        for peerId in peerIdList:
            self.removeQueueItem(peerId)

        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def isItemDisabled(self, kind, page, pos, item):
        if not self.mediator:
            return False
        if kind != const.RES_KIND_INV:
            return False
        if self.bitMode == BIT_MODE_ACCEPT:
            return True
        if self.bitMode == BIT_MODE_GIVE:
            if not hasattr(item, 'tradeAssignList'):
                return True
            peerEnt = BigWorld.entities.get(self.peerId)
            if not peerEnt:
                return True
            canTrade = item.canGroupTrade() and peerEnt.gbId in item.tradeAssignList
            return not canTrade
        return False
