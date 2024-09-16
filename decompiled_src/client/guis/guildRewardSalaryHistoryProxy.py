#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildRewardSalaryHistoryProxy.o
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

class GuildRewardSalaryHistoryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildRewardSalaryHistoryProxy, self).__init__(uiAdapter)
        self.modelMap = {'requestHistory': self.onRequestHistory}
        self.mediator = None
        self.gbId = 0
        self.role = ''
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_REWARD_SALARY_HISTORY, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_REWARD_SALARY_HISTORY:
            self.mediator = mediator

    def show(self, gbId, role):
        if gbId == 0 or role == '':
            return
        self.gbId = gbId
        self.role = role
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_REWARD_SALARY_HISTORY)

    def open(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_REWARD_SALARY_HISTORY)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.gbId = 0
        self.role = ''
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_REWARD_SALARY_HISTORY)

    def onRequestHistory(self, *arg):
        self.requestData()

    def requestData(self):
        BigWorld.player().cell.queryGuildMemberPayments(long(self.gbId), self.role)

    def updateData(self, data):
        guildNUID, gbId, mData = data
        p = BigWorld.player()
        guildMembers = p.guild.member
        ret = {}
        now = utils.getNow()
        if guildMembers.has_key(gbId):
            member = guildMembers[gbId]
            ret = {}
            ret['playerName'] = member.role
            ret['role'] = gametypes.GUILD_ROLE_DICT[member.roleId]
            ret['lv'] = member.level
            ret['school'] = const.SCHOOL_DICT[member.school]
            ret['list'] = []
            for salary in mData:
                obj = {}
                obj['type'] = gameStrings.TEXT_GUILDREWARDSALARYHISTORYPROXY_68 if salary[6] == gametypes.GUILD_SALARY_TYPE_NORMAL else gameStrings.TEXT_GUILDREWARDSALARYHISTORYPROXY_68_1
                obj['salary'] = salary[2]
                obj['assignTime'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(salary[3]))
                if salary[5] == 0:
                    if salary[4] < now:
                        obj['getTime'] = gameStrings.TEXT_GUILDREWARDSALARYHISTORYPROXY_73
                    else:
                        obj['getTime'] = gameStrings.TEXT_ROLECARDPROXY_791
                else:
                    obj['getTime'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(salary[5]))
                obj['cashType'] = salary[0]
                ret['list'].append(obj)

            ret['list'] = sorted(ret['list'], key=lambda x: x['assignTime'])
        if self.mediator:
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(ret, True))
