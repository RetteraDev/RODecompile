#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impTrade.o
import BigWorld
import Sound
import const
import gameglobal
import gamelog
import Avatar
from callbackHelper import Functor
from guis import uiConst
from commTrade import ValuableTradeVal
from cdata import game_msg_def_data as GMDD

class ImpTrade(object):

    def tradeCash(self, isSelf, cash, serial):
        gamelog.debug('pgf::ImpTrade:tradeCash, isSelf, cash, serial', isSelf, cash, serial)
        self.tradeUnConfirm(isSelf)
        gameglobal.rds.ui.trade.tradeMoney(cash, isSelf, serial)

    def tradeItem(self, isSelf, pos, item, serial):
        gamelog.debug('pgf::ImpTrade:tradeItem, isSelf, pos, item, serial', isSelf, pos, item, serial)
        page = uiConst.TRADE_SLOTS_MINE if isSelf else uiConst.TRADE_SLOTS_THEIR
        self.tradeUnConfirm(isSelf)
        if item != const.CONT_EMPTY_VAL:
            gameglobal.rds.ui.trade.tradeItem(item, page, pos, isSelf, serial)
        else:
            gameglobal.rds.ui.trade.removeItem(isSelf, page, pos, serial)

    def tradeRequest(self, who):
        if len(gameglobal.rds.ui.trade.traderQueue) >= const.TRADE_MAX_PROPOSER or gameglobal.rds.ui.trade.traderQueue.has_key(who):
            BigWorld.player().cell.tradeOver(who)
            return
        gamelog.debug('pgf::ImpTrade:trade_request, who', who)
        t = BigWorld.player().getServerTime()
        ent = BigWorld.entities.get(who)
        if not ent:
            return
        name = ent.roleName
        gameglobal.rds.ui.trade.traderQueue[who] = (t, name)
        gameglobal.rds.ui.trade.traderCallbackHandler[who] = BigWorld.callback(60, Functor(self.autoCancelRequest, who, t))
        gameglobal.rds.sound.playSound(gameglobal.SD_32)
        data = {'data': [who, gameglobal.rds.ui.trade.traderQueue[who]],
         'startTime': t,
         'totalTime': 60}
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_TRADE, data)
        if not BigWorld.player().inCombat:
            gameglobal.rds.ui.tradeRequest.show()
        for k, v in gameglobal.rds.ui.trade.traderQueue.items():
            if k != who and v[1] == name:
                BigWorld.player().cell.tradeOver(k)
                data = {'data': [k, v],
                 'startTime': v[0],
                 'totalTime': 60}
                gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_TRADE, data)
                gameglobal.rds.ui.trade.traderQueue.pop(k)

    def onTradeAccept(self, who):
        BigWorld.player().cell.tradeAccept(who)
        if gameglobal.rds.ui.trade.traderCallbackHandler.has_key(who):
            BigWorld.cancelCallback(gameglobal.rds.ui.trade.traderCallbackHandler.pop(who))
        if gameglobal.rds.ui.trade.traderQueue.has_key(who):
            data = {'data': [who, gameglobal.rds.ui.trade.traderQueue[who]]}
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_TRADE, data)
            gameglobal.rds.ui.trade.traderQueue.pop(who)
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def onTradeReject(self, who):
        BigWorld.player().cell.tradeReject(who)
        if gameglobal.rds.ui.trade.traderCallbackHandler.has_key(who):
            BigWorld.cancelCallback(gameglobal.rds.ui.trade.traderCallbackHandler.pop(who))
        if gameglobal.rds.ui.trade.traderQueue.has_key(who):
            data = {'data': [who, gameglobal.rds.ui.trade.traderQueue[who]]}
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_TRADE, data)
            gameglobal.rds.ui.trade.traderQueue.pop(who)
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def autoCancelRequest(self, who, time):
        if gameglobal.rds.ui.trade.traderQueue.has_key(who) and gameglobal.rds.ui.trade.traderQueue[who][0] == time:
            data = {'data': [who, gameglobal.rds.ui.trade.traderQueue[who]]}
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_TRADE, data)
            gameglobal.rds.ui.trade.traderQueue.pop(who)
            ent = BigWorld.entities.get(who)
            if ent:
                ent.cell.tradeDate(self.id)

    def tradeStart(self, id):
        gamelog.debug('pgf::ImpTrade:tradeStart, id', id)
        Sound.playSimple('ui_1069')
        self.isTrading = True
        if gameglobal.rds.ui.trade.traderQueue.has_key(id):
            data = {'data': [id, gameglobal.rds.ui.trade.traderQueue[id]]}
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_TRADE, data)
            gameglobal.rds.ui.trade.traderQueue.pop(id)
        gameglobal.rds.ui.trade.show(id)

    def tradeConfirm(self, isSelf):
        gamelog.debug('pgf::ImpTrade:tradeConfirm, isSelf', isSelf)
        Sound.playSimple('ui_1070')
        gameglobal.rds.ui.trade.setLockState(isSelf, True)

    def tradeUnConfirm(self, isSelf):
        gamelog.debug('trade unconfirm', isSelf, self.id)
        Sound.playSimple('ui_1070')
        gameglobal.rds.ui.trade.setLockState(isSelf, False)

    def tradeFinal(self, isSelf):
        gamelog.debug('pgf::ImpTrade:tradeFinal, isSelf', isSelf)
        if isSelf:
            gameglobal.rds.ui.trade.setSelfGreen()
        else:
            gameglobal.rds.ui.trade.setOtherGreen()

    def tradeFinish(self):
        gamelog.debug('pgf::ImpTrade:tradeFinis')
        self.isTrading = False
        gameglobal.rds.ui.trade.hide()
        gameglobal.rds.sound.playSound(gameglobal.SD_36)

    def tradeCancel(self):
        gamelog.debug('pgf::ImpTrade:tradeCancel')
        self.isTrading = False
        gameglobal.rds.ui.trade.hide()

    def beginTrade(self):
        if self.targetLocked != None and type(self.targetLocked) == Avatar.Avatar:
            gamelog.debug('PGF::doRequest: send trade request to %s' % self.targetLocked.roleName)
            self.cell.tradeRequest(self.targetLocked.id)

    def tradeItemFinish(self, itemList):
        gameglobal.rds.ui.showSpecialCurve(itemList)

    def sendValuableTrade(self, data):
        for dto in data:
            valuableTrade = ValuableTradeVal().fromDTO(dto)
            self.valuableTrade[valuableTrade.nuid] = valuableTrade

    def onAddValuableTrade(self, dto):
        valuableTrade = ValuableTradeVal().fromDTO(dto)
        self.valuableTrade[valuableTrade.nuid] = valuableTrade
        self.showGameMsg(GMDD.data.VALUABLE_TRADE_CASH, (valuableTrade.cash,))
        if gameglobal.rds.ui.valuableTrade.mediator:
            gameglobal.rds.ui.valuableTrade.updateData()
        gameglobal.rds.tutorial.onGetFreezeCash()

    def onRemoveValuableTrade(self, nuid):
        self.valuableTrade.pop(nuid)
        if gameglobal.rds.ui.valuableTrade.mediator:
            gameglobal.rds.ui.valuableTrade.updateData()
