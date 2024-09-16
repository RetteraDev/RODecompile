#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/raffleProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import gametypes
import const
import random
from uiProxy import UIProxy
from callbackHelper import Functor
from data import fame_data as FD
from data import raffle_data as RD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
STATE_NORMAL = 0
STATE_CHOOSE = 1

class RaffleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RaffleProxy, self).__init__(uiAdapter)
        self.modelMap = {'close': self.onClose,
         'confirm': self.onConfirm,
         'select': self.onSelect}
        self.mediator = None
        self.state = STATE_NORMAL
        self.raffleId = 0
        self.resPos = (const.CONT_NO_PAGE, const.CONT_NO_POS)
        self.resItemId = 0
        self.fromLoopChargeData = None
        self.startTurnTimer = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_RAFFLE, self.checkAndHide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RAFFLE:
            self.mediator = mediator
            self.refreshInfo()
            gameglobal.rds.sound.playSound(gameglobal.SD_4)

    def clearWidget(self):
        self.mediator = None
        if self.startTurnTimer:
            self.startTurnTimer = 0
            BigWorld.cancelCallback(self.startTurnTimer)
        if self.fromLoopChargeData:
            BigWorld.player().base.finishChargeRaffle(self.uiAdapter.activitySaleLoopCharge.getRewardKeyVal()[0])
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RAFFLE)

    def checkAndHide(self):
        if self.state == STATE_CHOOSE:
            return
        self.hide()

    def reset(self):
        self.state = STATE_NORMAL
        self.raffleId = 0
        self.resPos = (const.CONT_NO_PAGE, const.CONT_NO_POS)
        self.resItemId = 0
        self.fromLoopChargeData = None

    def show(self, it, fromLoopChargeData = None):
        raffleId = it.getRaffleId() if it else 0
        if not RD.data.has_key(raffleId) and not fromLoopChargeData:
            return
        if it and it.hasLatch():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        if not self.mediator:
            self.raffleId = raffleId
            self.resItemId = it.id if it else 0
            self.fromLoopChargeData = fromLoopChargeData
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RAFFLE, isModal=True)

    def refreshInfo(self):
        if self.mediator:
            rd = RD.data.get(self.raffleId, {})
            if not rd and not self.fromLoopChargeData:
                return
            raffleItemSetInfo = gameglobal.rds.ui.treasureBoxWish.getWishRaffleItemSetInfo(self.resItemId) or rd.get('raffleItemSetInfo') or self.fromLoopChargeData
            if not raffleItemSetInfo:
                return
            info = {}
            info['title'] = rd.get('description', '')
            fixedConsume = rd.get('fixedConsume')
            if fixedConsume:
                costHint = ''
                for consumeType, consumeId, consumeVal in fixedConsume:
                    if costHint != '':
                        costHint += gameStrings.TEXT_ACTIVITYFACTORY_280
                    if consumeType == const.RAFFLE_CONSUME_MONEY:
                        if consumeId == gametypes.BIND_CASH_ITEM:
                            costHint += gameStrings.TEXT_RAFFLEPROXY_102 % format(consumeVal, ',')
                        elif consumeId == gametypes.CASH_ITEM:
                            costHint += gameStrings.TEXT_RAFFLEPROXY_104 % format(consumeVal, ',')
                    elif consumeType == const.RAFFLE_CONSUME_FAME:
                        costHint += "<font color=\'#E5842E\'>%s</font>%s" % (format(consumeVal, ','), FD.data.get(consumeId, {}).get('name', ''))

                info['costHint'] = gameStrings.TEXT_RAFFLEPROXY_107 % costHint
            else:
                info['costHint'] = ''
            itemList = []
            for i in xrange(len(raffleItemSetInfo)):
                itemId, num, _ = raffleItemSetInfo[i]
                itemInfo = {}
                itemInfo['itemId'] = itemId
                itemInfo['iconPath'] = uiUtils.getItemIconFile64(itemId)
                itemInfo['num'] = '' if num == 1 else num
                itemList.append(itemInfo)

            info['itemList'] = itemList
            info['fromLoopCharge'] = True if self.fromLoopChargeData else False
            if self.fromLoopChargeData and self.uiAdapter.activitySaleLoopCharge.getRewardKeyVal()[1].get('showSpecialEff', 0):
                info['showSpecialEff'] = True
            else:
                info['showSpecialEff'] = False
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            self.startTurn()

    def startTurn(self):
        self.state = STATE_NORMAL
        if self.startTurnTimer:
            BigWorld.cancelCallback(self.startTurnTimer)
        if self.mediator:
            info = {}
            info['times'] = ''
            btnEnabled = True
            info['btnEnabled'] = btnEnabled
            self.mediator.Invoke('startTurn', uiUtils.dict2GfxDict(info, True))

    def choose(self, page, pos, idx):
        if self.resPos != (page, pos) and not self.fromLoopChargeData:
            return
        self.state = STATE_CHOOSE
        if self.mediator:
            gameglobal.rds.sound.playSound(3974)
            frameIntervalList = []
            frameToTimesList = []
            raffleFrameToTimes = SCD.data.get('raffleFrameToTimes', ())
            for value in raffleFrameToTimes:
                frameIntervalList.append(value[0])
                times = random.randint(value[1], value[2])
                frameToTimesList.append(times)

            info = {}
            info['frameIntervalList'] = frameIntervalList
            info['frameToTimesList'] = frameToTimesList
            info['idx'] = idx
            self.mediator.Invoke('choose', uiUtils.dict2GfxDict(info, True))

    def success(self, page, pos, idx):
        gameglobal.rds.sound.stopSound(3974)
        BigWorld.player().showGameMsg(GMDD.data.RAFFLE_SUCCESS_HINT, ())
        if self.startTurnTimer:
            BigWorld.cancelCallback(self.startTurnTimer)
        self.startTurnTimer = BigWorld.callback(2, self.startTurn)

    def onClose(self, *arg):
        self.checkAndHide()

    def onConfirm(self, *arg):
        p = BigWorld.player()
        if self.fromLoopChargeData:
            if not self.uiAdapter.activitySaleLoopCharge.getRewardCnt():
                p.showGameMsg(GMDD.data.RAFFLE_FIXEDCONSUME_LACK_HINT, ())
                self.startTurn()
            else:
                p.base.startChargeRaffle(self.uiAdapter.activitySaleLoopCharge.getRewardKeyVal()[0])
                self.startTurn()
            return
        pos = p.inv.findItemInPages(self.resItemId, enableParentCheck=False)
        if pos[0] == const.CONT_NO_PAGE and pos[1] == const.CONT_NO_POS:
            p.showGameMsg(GMDD.data.RAFFLE_FIXEDCONSUME_LACK_HINT, ())
            self.startTurn()
            return
        it = p.inv.getQuickVal(pos[0], pos[1])
        if not it:
            p.showGameMsg(GMDD.data.RAFFLE_FIXEDCONSUME_LACK_HINT, ())
            self.startTurn()
            return
        enabled = True
        costBindCash = 0
        fixedConsume = RD.data.get(self.raffleId, {}).get('fixedConsume')
        if fixedConsume:
            for consumeType, consumeId, consumeVal in fixedConsume:
                if consumeType == const.RAFFLE_CONSUME_MONEY:
                    if consumeId == gametypes.BIND_CASH_ITEM:
                        costBindCash += consumeVal
                        if p.bindCash + p.cash < consumeVal:
                            enabled = False
                    elif consumeId == gametypes.CASH_ITEM:
                        if p.cash < consumeVal:
                            enabled = False
                if consumeType == const.RAFFLE_CONSUME_FAME:
                    if p.getFame(consumeId) < consumeVal:
                        enabled = False

        if not enabled:
            p.showGameMsg(GMDD.data.RAFFLE_FIXEDCONSUME_LACK_HINT, ())
            self.startTurn()
            return
        self.resPos = pos
        if uiUtils.checkBindCashEnough(costBindCash, p.bindCash, p.cash, Functor(p.onConfirmUseItem, it, self.resPos[0], self.resPos[1]), True):
            p.onConfirmUseItem(it, self.resPos[0], self.resPos[1])

    def onSelect(self, *arg):
        p = BigWorld.player()
        if self.state == STATE_NORMAL:
            return
        self.state = STATE_NORMAL
        if self.fromLoopChargeData:
            BigWorld.player().base.finishChargeRaffle(self.uiAdapter.activitySaleLoopCharge.getRewardKeyVal()[0])
            if self.startTurnTimer:
                BigWorld.cancelCallback(self.startTurnTimer)
            self.startTurnTimer = BigWorld.callback(2, self.startTurn)
            return
        pos = p.inv.findItemInPages(self.resItemId, enableParentCheck=False)
        if pos[0] == const.CONT_NO_PAGE and pos[1] == const.CONT_NO_POS:
            self.startTurn()
            return
        it = p.inv.getQuickVal(pos[0], pos[1])
        if not it:
            self.startTurn()
            return
        self.resPos = pos
        p.cell.useCommonItemWithParam(self.resPos[0], self.resPos[1], const.RAFFLE_STAGE, 1)
