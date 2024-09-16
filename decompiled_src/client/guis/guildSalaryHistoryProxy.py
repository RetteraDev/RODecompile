#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildSalaryHistoryProxy.o
from gamestrings import gameStrings
import time
import BigWorld
from uiProxy import UIProxy
import gameglobal
import gametypes
import const
import utils
from guis import uiConst
from guis import uiUtils

class GuildSalaryHistoryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildSalaryHistoryProxy, self).__init__(uiAdapter)
        self.modelMap = {'requestHistory': self.onRequestHistory,
         'requestHistoryDetail': self.onRequestHistoryDetail}
        self.mediator = None
        self.mtype = 0
        self.serialNUID = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_SALARY_HISTORY, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_SALARY_HISTORY:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_SALARY_HISTORY)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.funcNpc.close()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_SALARY_HISTORY)

    def onRequestHistory(self, *arg):
        p = BigWorld.player()
        ret = []
        cashGroup = p.guild.payroll[gametypes.GUILD_PAY_TYPE_CASH].group
        coinGroup = p.guild.payroll[gametypes.GUILD_PAY_TYPE_COIN].group
        bindcashGroup = p.guild.payroll[gametypes.GUILD_PAY_TYPE_BIND_CASH].group if p.guild.payroll.has_key(gametypes.GUILD_PAY_TYPE_BIND_CASH) else []
        for serialNUID in cashGroup:
            cashObj = {}
            cashObj['label'] = time.strftime('%Y/%m/%d', time.localtime(cashGroup[serialNUID].tWhen))
            cashObj['time'] = cashGroup[serialNUID].tWhen
            cashObj['type'] = gametypes.GUILD_PAY_TYPE_CASH
            cashObj['serialNUID'] = cashGroup[serialNUID].serialNUID
            ret.append(cashObj)

        for serialNUID in coinGroup:
            coinObj = {}
            coinObj['label'] = time.strftime('%Y/%m/%d', time.localtime(coinGroup[serialNUID].tWhen))
            coinObj['time'] = coinGroup[serialNUID].tWhen
            coinObj['type'] = gametypes.GUILD_PAY_TYPE_COIN
            coinObj['serialNUID'] = coinGroup[serialNUID].serialNUID
            ret.append(coinObj)

        for serialNUID in bindcashGroup:
            bindCashObj = {}
            bindCashObj['label'] = time.strftime('%Y/%m/%d', time.localtime(bindcashGroup[serialNUID].tWhen))
            bindCashObj['time'] = bindcashGroup[serialNUID].tWhen
            bindCashObj['type'] = gametypes.GUILD_PAY_TYPE_BIND_CASH
            bindCashObj['serialNUID'] = bindcashGroup[serialNUID].serialNUID
            ret.append(bindCashObj)

        ret = sorted(ret, key=lambda x: x['time'])
        for index in xrange(len(ret)):
            ret[index]['label'] = gameStrings.TEXT_GUILDSALARYHISTORYPROXY_74 % (index + 1, ret[index]['label'])

        return uiUtils.array2GfxAarry(ret, True)

    def onRequestHistoryDetail(self, *arg):
        self.mtype = int(arg[3][0].GetNumber())
        self.serialNUID = long(arg[3][1].GetString())
        BigWorld.player().queryGuildPayroll(self.mtype, self.serialNUID)
        self.updateSalaryDetailHistory()

    def updateSalaryDetailHistory(self):
        p = BigWorld.player()
        ret = []
        data = p.guild.payroll.get(self.mtype, None)
        history = data.group.get(self.serialNUID, None)
        guildMember = p.guild.member
        now = utils.getNow()
        if history != None:
            for payment in history.payments:
                obj = {}
                member = guildMember.get(payment.gbId)
                if member == None:
                    continue
                obj['playerName'] = member.role
                obj['role'] = gametypes.GUILD_ROLE_DICT[member.roleId]
                obj['lv'] = member.level
                obj['school'] = const.SCHOOL_DICT[member.school]
                obj['salary'] = payment.amount
                if payment.tPaid == 0:
                    if history.tExpire < now:
                        obj['time'] = gameStrings.TEXT_GUILDREWARDSALARYHISTORYPROXY_73
                    else:
                        obj['time'] = gameStrings.TEXT_ROLECARDPROXY_791
                else:
                    obj['time'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(payment.tPaid))
                obj['mtype'] = self.mtype
                obj['salaryType'] = gameStrings.TEXT_GUILDREWARDSALARYHISTORYPROXY_68 if payment.salaryType == gametypes.GUILD_SALARY_TYPE_NORMAL else gameStrings.TEXT_GUILDREWARDSALARYHISTORYPROXY_68_1
                obj['assignTime'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(payment.tWhen))
                ret.append(obj)

            ret = sorted(ret, key=lambda x: x['assignTime'])
        if self.mediator:
            self.mediator.Invoke('updateHistoryList', uiUtils.array2GfxAarry(ret, True))
