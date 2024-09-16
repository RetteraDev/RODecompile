#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/offlineIncomeProxy.o
import BigWorld
import gameglobal
import gametypes
import const
import uiConst
import uiUtils
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class OfflineIncomeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(OfflineIncomeProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInfo': self.onGetInfo,
         'confirm': self.onConfirm}
        self.mediator = None
        self.incomes = []
        self.opCode = 0
        self.dbID = 0
        self.mtype = 0
        self.bindType = 0
        self.amount = 0
        self.extra1Amount = 0
        self.extra2Amount = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_OFFLINE_INCOME, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_OFFLINE_INCOME:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_OFFLINE_INCOME)

    def clearAll(self):
        self.incomes = []

    def show(self, opCode):
        if len(self.incomes) == 0:
            return
        if sum([ (1 if offlineIncome.opcode == opCode else 0) for offlineIncome in self.incomes ]) == 0:
            return
        self.opCode = opCode
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_OFFLINE_INCOME)

    def onGetInfo(self, *args):
        self.refreshInfo()

    def refreshInfo(self):
        if not self.mediator:
            return
        for offlineIncome in self.incomes:
            if offlineIncome.opcode != self.opCode:
                continue
            self.dbID = offlineIncome.dbID
            self.mtype = offlineIncome.mtype
            self.bindType = offlineIncome.bindType
            self.amount = offlineIncome.amount
            self.extra1Amount = offlineIncome.extra1Amount
            self.extra2Amount = offlineIncome.extra2Amount
            desc = ''
            if offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_GUILD_DISMISS:
                if self.mtype == const.MONEY_TYPE_CASH:
                    if self.bindType == const.CASH_TYPE_UNBIND:
                        desc = uiUtils.getTextFromGMD(GMDD.data.GUILD_SALARY_RETURN_CASH, '')
                    elif self.bindType == const.CASH_TYPE_BIND:
                        desc = uiUtils.getTextFromGMD(GMDD.data.GUILD_SALARY_RETURN_BIND_CASH, '')
                elif self.mtype == const.MONEY_TYPE_COIN:
                    desc = uiUtils.getTextFromGMD(GMDD.data.GUILD_SALARY_RETURN_COIN, '')
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_BID_REFEND:
                desc = uiUtils.getTextFromGMD(GMDD.data.GUILD_CONSIGN_BID_REFEND_HINT, '')
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_PROFIT:
                desc = uiUtils.getTextFromGMD(GMDD.data.GUILD_CONSIGN_PROFIT_HINT, '')
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_WORLD_CONSIGN_BID_REFEND:
                desc = uiUtils.getTextFromGMD(GMDD.data.WORLD_CONSIGN_BID_REFEND_HINT, '')
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_DESTORY_REFEND:
                desc = uiUtils.getTextFromGMD(GMDD.data.GUILD_CONSIGN_DESTORY_REFEND_HINT, '')
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_BONUS_GIVE_FREE_COIN:
                desc = uiUtils.getTextFromGMD(GMDD.data.BONUS_GIVE_FREE_COIN_HINT, '')
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_QUIZZES_BIND_COIN:
                desc = uiUtils.getTextFromGMD(GMDD.data.QUIZZES_GIVE_BIND_COIN_HINT, '')
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_COUNTRY_CONSIGN_PROFIT:
                desc = uiUtils.getTextFromGMD(GMDD.data.WING_WORLD_CONSIGN_PROFIT_HINT, '')
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_CBG_ROLE:
                desc = uiUtils.getTextFromGMD(GMDD.data.CBG_GET_COIN, '')
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_SCHOOL_TOP_LUCKY_BAG:
                desc = uiUtils.getTextFromGMD(GMDD.data.CELE_LUCKY_BAG_HINT, '')
            info = {'desc': desc,
             'mtype': self.mtype,
             'bindType': self.bindType}
            if self.mtype == const.MONEY_TYPE_COIN and self.bindType == const.COIN_TYPE_UNBIND_BIND_FREE:
                info['amount'] = self.amount + self.extra1Amount + self.extra2Amount
            else:
                info['amount'] = self.amount
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            return

    def onConfirm(self, *args):
        BigWorld.player().cell.fetchOfflineIncome(self.dbID, self.mtype, self.bindType, self.amount, self.extra1Amount, self.extra2Amount)
        self.hide()

    def notifyUIPushMsg(self):
        pushDict = {gametypes.OFFLINE_INCOME_OP_GUILD_DISMISS: False,
         gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_BID_REFEND: False,
         gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_PROFIT: False,
         gametypes.OFFLINE_INCOME_OP_WORLD_CONSIGN_BID_REFEND: False,
         gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_DESTORY_REFEND: False,
         gametypes.OFFLINE_INCOME_OP_BONUS_GIVE_FREE_COIN: False,
         gametypes.OFFLINE_INCOME_OP_QUIZZES_BIND_COIN: False,
         gametypes.OFFLINE_INCOME_OP_COUNTRY_CONSIGN_PROFIT: False,
         gametypes.OFFLINE_INCOME_OP_CBG_ROLE: False,
         gametypes.OFFLINE_INCOME_OP_SCHOOL_TOP_LUCKY_BAG: False}
        pushMessage = gameglobal.rds.ui.pushMessage
        for offlineIncome in self.incomes:
            pushDict[offlineIncome.opcode] = True
            if offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_GUILD_DISMISS:
                pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_OFFLINE_INCOME)
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_BID_REFEND:
                pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_CONSIGN_BID_REFEND)
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_PROFIT:
                pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_CONSIGN_PROFIT)
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_WORLD_CONSIGN_BID_REFEND:
                pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WORLD_CONSIGN_BID_REFEND)
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_DESTORY_REFEND:
                pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_CONSIGN_DESTORY_REFEND)
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_BONUS_GIVE_FREE_COIN:
                pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_BONUS_GIVE_FREE_COIN)
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_QUIZZES_BIND_COIN:
                pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_QUIZZES_GIVE_COIN)
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_COUNTRY_CONSIGN_PROFIT:
                pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_CONSIGN_PROFIT)
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_CBG_ROLE:
                import gamelog
                gamelog.debug('ypc@ OFFLINE_INCOME_OP_CBG_ROLE push!')
                pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CBG_GET_COIN)
            elif offlineIncome.opcode == gametypes.OFFLINE_INCOME_OP_SCHOOL_TOP_LUCKY_BAG:
                pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_SCHOOL_TOP_COIN)

        if not pushDict[gametypes.OFFLINE_INCOME_OP_GUILD_DISMISS]:
            pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_OFFLINE_INCOME)
        if not pushDict[gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_BID_REFEND]:
            pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_CONSIGN_BID_REFEND)
        if not pushDict[gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_PROFIT]:
            pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_CONSIGN_PROFIT)
        if not pushDict[gametypes.OFFLINE_INCOME_OP_WORLD_CONSIGN_BID_REFEND]:
            pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WORLD_CONSIGN_BID_REFEND)
        if not pushDict[gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_DESTORY_REFEND]:
            pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_CONSIGN_DESTORY_REFEND)
        if not pushDict[gametypes.OFFLINE_INCOME_OP_BONUS_GIVE_FREE_COIN]:
            pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_BONUS_GIVE_FREE_COIN)
        if not pushDict[gametypes.OFFLINE_INCOME_OP_QUIZZES_BIND_COIN]:
            pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_QUIZZES_GIVE_COIN)
        if not pushDict[gametypes.OFFLINE_INCOME_OP_COUNTRY_CONSIGN_PROFIT]:
            pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_WING_WORLD_CONSIGN_PROFIT)
        if not pushDict[gametypes.OFFLINE_INCOME_OP_CBG_ROLE]:
            pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_CBG_GET_COIN)
        if not pushDict[gametypes.OFFLINE_INCOME_OP_SCHOOL_TOP_LUCKY_BAG]:
            pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_SCHOOL_TOP_COIN)
