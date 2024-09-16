#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildRewardSalaryAssignProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
import gametypes
from guis import ui
from guis import uiConst
from guis import uiUtils
from data import guild_config_data as GCD

class GuildRewardSalaryAssignProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildRewardSalaryAssignProxy, self).__init__(uiAdapter)
        self.modelMap = {'changeTab': self.onChangeTab,
         'getTabData': self.onGetTabData,
         'getInitExpireType': self.onGetInitExpireType,
         'payGuildSalary': self.onPayGuildSalary}
        self.mediator = None
        self.curCashType = gametypes.GUILD_PAY_TYPE_CASH
        self.members = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_REWARD_SALARY_ASSIGN, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_REWARD_SALARY_ASSIGN:
            self.mediator = mediator

    def show(self, memberArr):
        self.members = memberArr
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_REWARD_SALARY_ASSIGN)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.curCashType = gametypes.GUILD_PAY_TYPE_CASH
        self.members = []
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_REWARD_SALARY_ASSIGN)

    def onChangeTab(self, *arg):
        self.curCashType = int(arg[3][0].GetNumber())

    def onGetTabData(self, *arg):
        ret = {}
        p = BigWorld.player()
        ret['count'] = len(self.members)
        ret['cash'] = 0
        if self.curCashType == gametypes.GUILD_PAY_TYPE_CASH:
            ret['cash'] = p.guild.reserveCash if hasattr(p.guild, 'reserveCash') else 0
        elif self.curCashType == gametypes.GUILD_PAY_TYPE_COIN:
            ret['cash'] = p.guild.reserveCoin if hasattr(p.guild, 'reserveCoin') else 0
        elif self.curCashType == gametypes.GUILD_PAY_TYPE_BIND_CASH:
            ret['cash'] = p.guild.reserveBindCash if hasattr(p.guild, 'reserveBindCash') else 0
        if self.curCashType == gametypes.GUILD_PAY_TYPE_CASH:
            ret['maxSalary'] = GCD.data.get('maxCashSalary', 3000)
        elif self.curCashType == gametypes.GUILD_PAY_TYPE_COIN:
            ret['maxSalary'] = GCD.data.get('maxCoinSalary', 3000)
        elif self.curCashType == gametypes.GUILD_PAY_TYPE_BIND_CASH:
            ret['maxSalary'] = GCD.data.get('maxBindCashSalary', 3000)
        return uiUtils.dict2GfxDict(ret, True)

    def onGetInitExpireType(self, *arg):
        expireType = gametypes.GUILD_PAY_EXPIRE
        ret = []
        for index in expireType:
            typeObj = {}
            typeObj['id'] = index
            typeObj['label'] = self._getTimeStr(expireType[index])
            ret.append(typeObj)

        return uiUtils.array2GfxAarry(ret, True)

    def _getTimeStr(self, sec):
        if sec == 3600:
            return gameStrings.TEXT_GUILDREWARDSALARYASSIGNPROXY_79
        if sec == 86400:
            return gameStrings.TEXT_GUILDREWARDSALARYASSIGNPROXY_81
        if sec == 259200:
            return gameStrings.TEXT_GUILDREWARDSALARYASSIGNPROXY_83
        if sec == 604800:
            return gameStrings.TEXT_GUILDREWARDSALARYASSIGNPROXY_85
        return ''

    @ui.checkInventoryLock()
    def onPayGuildSalary(self, *arg):
        expireType = int(arg[3][0].GetNumber())
        cash = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        payments = []
        for gbId in self.members:
            obj = {}
            obj['gbId'] = long(gbId)
            obj['amount'] = cash
            payments.append(obj)

        p.cell.payGuildIndividualMembers(self.curCashType, expireType, payments, p.cipherOfPerson)
        self.hide()
