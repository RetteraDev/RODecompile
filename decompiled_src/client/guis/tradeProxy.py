#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tradeProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
from guis import uiConst
from callbackHelper import Functor
from uiProxy import SlotDataProxy
from ui import gbk2unicode
from item import Item
from guis import ui
from guis import uiUtils
from guis import events
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD

class TradeProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(TradeProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'trade'
        self.type = 'trade'
        self.modelMap = {'getNames': self.onGetNames,
         'setLockNum': self.onSetLockNum,
         'confirmTrade': self.onConfirmTrade,
         'cancelTrade': self.onCancelTrade,
         'fitting': self.onFitting,
         'inputMoney': self.onInputMoney,
         'confirmMoney': self.onConfirmMoney,
         'cancelMoney': self.onCancelMoney,
         'getCash': self.onGetCash}
        self.mediator = None
        self.peerId = None
        self.mLock = False
        self.tLock = False
        self.isLock = False
        self.mSerial = 0
        self.tSerial = 0
        self.Items = [[const.CONT_EMPTY_VAL] * 12, [const.CONT_EMPTY_VAL] * 12]
        self.isShow = False
        self.callbackHandler = None
        self.traderQueue = {}
        self.traderCallbackHandler = {}
        self.mCash = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_TRADE_VIEW, Functor(self.onCancelTrade, None))

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[5:]), int(idItem[4:]))

    def _getKey(self, page, pos):
        return 'trade%d.slot%d' % (page, pos)

    def setItem(self, item, page, pos):
        if item:
            key = self._getKey(page, pos)
            if self.binding.get(key, None):
                data = uiUtils.getGfxItem(item)
                p = BigWorld.player()
                if hasattr(item, 'cdura') and item.cdura == 0:
                    self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_BROKEN))
                elif item.type == Item.BASETYPE_EQUIP and item.canEquip(p, item.whereEquip()[0]):
                    self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_BROKEN))
                elif not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                    self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_NOT_USE))
                else:
                    self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
                self.Items[page][pos] = item

    def removeItem(self, isSelf, page, pos, serial):
        if isSelf:
            self.mSerial = serial
        else:
            self.tSerial = serial
        key = self._getKey(page, pos)
        if self.binding.get(key, None):
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)
            self.Items[page][pos] = const.CONT_EMPTY_VAL

    def tradeItem(self, item, page, pos, isSelf, serial):
        if isSelf:
            self.mSerial = serial
        else:
            self.tSerial = serial
        self.setItem(item, page, pos)

    def tradeMoney(self, cash, isSelf, serial):
        if isSelf:
            self.mSerial = serial
            self.mCash = cash
            self.setSelfMoney(cash)
        else:
            self.tSerial = serial
            self.setOtherMoney(cash)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TRADE_VIEW:
            self.mediator = mediator
            BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def onGetNames(self, *arg):
        ret = self.movie.CreateArray()
        p = BigWorld.player()
        peerPlayer = BigWorld.entities.get(self.peerId) if self.peerId else None
        pRoleName = p.realRoleName if p else ''
        peerRoleName = peerPlayer.roleName if peerPlayer else ''
        ret.SetElement(0, GfxValue(gbk2unicode(peerRoleName)))
        ret.SetElement(1, GfxValue(gbk2unicode(pRoleName)))
        return ret

    def onSetLockNum(self, *arg):
        self.isLock = arg[3][0].GetBool()
        gameglobal.rds.sound.playSound(gameglobal.SD_33)
        if self.isLock:
            BigWorld.player().cell.tradeConfirm()
        else:
            BigWorld.player().cell.tradeUnConfirm()

    @ui.callFilter(uiConst.CONFIRM_TRADE)
    @ui.checkInventoryLock()
    def onConfirmTrade(self, *arg):
        BigWorld.player().cell.tradeFinal(self.mSerial, self.tSerial, BigWorld.player().cipherOfPerson)
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def onCancelTrade(self, *arg):
        BigWorld.player().cell.tradeCancel()
        self.hide()
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def onInputMoney(self, *arg):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TRADE_MONEY, True)

    def onConfirmMoney(self, *arg):
        val = arg[3][0].GetString()
        val = int(val) if val else 0
        p = BigWorld.player()
        if p.cash + self.mCash == 0:
            BigWorld.player().showTopMsg(gameStrings.TEXT_TRADEPROXY_156)
            return
        if not ui.inputRangeJudge((0, p.cash + self.mCash, GMDD.data.ITEM_TRADE_MONEY_NUM), val, (p.cash + self.mCash,)):
            return
        BigWorld.player().cell.tradeCash(val)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TRADE_MONEY)
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def onCancelMoney(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TRADE_MONEY)
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def onNotifySlotUse(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        if page == uiConst.TRADE_SLOTS_THEIR:
            return
        item = self.Items[page][pos]
        if not item:
            return
        BigWorld.player().cell.tradeItemR(pos, item.cwrap)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        i = self.Items[page][pos]
        if i == None:
            return
        else:
            return gameglobal.rds.ui.inventory.GfxToolTip(i)

    def onFitting(self, *arg):
        key = arg[3][0].GetString()
        page, pos = self.getSlotID(key)
        it = self.Items[page][pos]
        if it:
            gameglobal.rds.ui.fittingRoom.addItem(it)

    def onGetCash(self, *arg):
        cash = getattr(BigWorld.player(), 'cash', 0)
        return GfxValue(cash)

    def show(self, id):
        self.peerId = id
        self.mLock = False
        self.tLock = False
        self.mSerial = 0
        self.tSerial = 0
        self.mCash = 0
        self.Items = [[const.CONT_EMPTY_VAL] * 12, [const.CONT_EMPTY_VAL] * 12]
        if gameglobal.rds.ui.fubenLogin.isShow:
            gameglobal.rds.ui.fubenLogin.dismiss()
        if gameglobal.rds.ui.quest.isShow:
            gameglobal.rds.ui.quest.close()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()
        if gameglobal.rds.ui.funcNpc.isShow:
            gameglobal.rds.ui.funcNpc.close()
        if gameglobal.rds.ui.debate.isShow:
            gameglobal.rds.debate.closeDebatePanel()
        if gameglobal.rds.ui.multiNpcChat.isShow:
            gameglobal.rds.ui.multiNpcChat.close()
        if gameglobal.rds.ui.map.isShow:
            gameglobal.rds.ui.map.realClose()
        self.isShow = True
        if gameglobal.rds.ui.shop.show:
            gameglobal.rds.ui.shop.hide()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TRADE_VIEW)
        gameglobal.rds.ui.inventory.show(False)
        self.callbackHandler = BigWorld.callback(0.5, self.checkTradeDist)
        gameglobal.rds.ui.actionbar.enableItemBar(False)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TRADE_VIEW)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TRADE_MONEY)
        gameglobal.rds.ui.characterDetailAdjust.closeTips()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NUMBER_VIEW)
        self.isShow = False
        if self.callbackHandler != None:
            BigWorld.cancelCallback(self.callbackHandler)
            self.callbackHandler = None
        gameglobal.rds.ui.actionbar.enableItemBar(True)

    def checkTradeDist(self):
        p = BigWorld.player()
        tgt = BigWorld.entities.get(self.peerId, None)
        if not tgt:
            p.cell.tradeCancel()
        else:
            dist = p.position.distTo(tgt.position)
            if dist > const.MAKE_TRADE_DIST:
                p.cell.tradeCancel()
        self.callbackHandler = BigWorld.callback(0.5, self.checkTradeDist)

    def setTradeBtnEnable(self, enable):
        if self.mediator != None:
            self.mediator.Invoke('setTradeBtnEnable', GfxValue(enable))

    def setOtherMoney(self, value):
        if self.mediator != None:
            self.mediator.Invoke('setOtherMoney', GfxValue(value))

    def setSelfMoney(self, value):
        if self.mediator != None:
            self.mediator.Invoke('setSelfMoney', GfxValue(value))

    def setLockState(self, isSelf, lock):
        if isSelf:
            self.mLock = lock
            if self.mediator != None:
                self.mediator.Invoke('setLockCheck', GfxValue(lock))
                self.mediator.Invoke('setSelfBagEnable', GfxValue(lock))
            if not lock:
                self.tLock = lock
                if self.mediator != None:
                    self.mediator.Invoke('setOtherBagEnable', GfxValue(lock))
        else:
            self.tLock = lock
            if self.mediator != None:
                self.mediator.Invoke('setOtherBagEnable', GfxValue(lock))
            if not lock:
                self.mLock = lock
                if self.mediator != None:
                    self.mediator.Invoke('setLockCheck', GfxValue(lock))
                    self.mediator.Invoke('setSelfBagEnable', GfxValue(lock))
        self.setTradeBtnEnable(self.canClickTrade())

    def canClickTrade(self):
        if self.mLock and self.tLock:
            return True
        return False

    def findFirstEmptySlot(self):
        for i, item in enumerate(self.Items[1]):
            if item == const.CONT_EMPTY_VAL:
                return i

        return -1

    def disableTradeBtn(self):
        if self.mediator != None:
            self.mediator.Invoke('disableTradeBtn')

    def setOtherGreen(self):
        if self.mediator != None:
            self.mediator.Invoke('setOtherGreen')

    def setSelfGreen(self):
        if self.mediator != None:
            self.mediator.Invoke('setSelfGreen')

    def reset(self):
        self.mediator = None
        self.peerId = None
        self.mLock = False
        self.tLock = False
        self.isLock = False
        self.mSerial = 0
        self.tSerial = 0
        self.mCash = 0
        self.Items = [[const.CONT_EMPTY_VAL] * 12, [const.CONT_EMPTY_VAL] * 12]
        self.isShow = False
        if self.callbackHandler != None:
            BigWorld.cancelCallback(self.callbackHandler)
        self.callbackHandler = None
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def escForReject(self):
        t = 0
        who = None
        for k, v in self.traderQueue.items():
            if v[0] > t:
                who = k

        if not who:
            return
        else:
            if self.traderCallbackHandler.has_key(who):
                BigWorld.cancelCallback(self.traderCallbackHandler.pop(who))
            if self.traderQueue.has_key(who):
                self.traderQueue.pop(who)
            BigWorld.player().cell.tradeReject(who)
            return

    @ui.uiEvent(uiConst.WIDGET_TRADE_VIEW, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            pos = self.findFirstEmptySlot()
            if pos != -1:
                self.setInventoryItem(nPage, nItem, uiConst.TRADE_SLOTS_MINE, pos)
            return

    def setInventoryItem(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        i = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if nPageDes == uiConst.TRADE_SLOTS_MINE:
            if not i:
                return
            if self.Items[nPageDes][nItemDes]:
                return
            if i.cwrap > 1:
                if not self.checkItemCanTrade(i):
                    BigWorld.player().showGameMsg(GMDD.data.ITEM_TRADE_NOTRADE, ())
                    return
                gameglobal.rds.ui.inventory.showNumberInputWidget(uiConst.NUMBER_WIDGET_ITEM_TRADE, nPageSrc, nItemSrc, nItemDes)
            elif i.isRuneEquip() and getattr(i, 'runeData', ()):
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_INVENTORYPROXY_1914, Functor(gameglobal.rds.ui.inventory.confirmTradeItem, nPageSrc, nItemSrc, nItemDes, i.cwrap))
            else:
                p.cell.tradeItem(nPageSrc, nItemSrc, nItemDes, i.cwrap)

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            i = BigWorld.player().inv.getQuickVal(page, pos)
            appreniceTradePermit = SCD.data.get('appreniceTradePermit', ())
            if i.id in appreniceTradePermit:
                return False
            if i.isForeverBind():
                return True

    def checkItemCanTrade(self, invItemData):
        appreniceTradePermit = SCD.data.get('appreniceTradePermit', ())
        if invItemData.id in appreniceTradePermit:
            return True
        if invItemData.isItemNoTrade():
            return False
        return True
