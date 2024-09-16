#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildSalaryAssignProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
import gametypes
import const
import utils
from guis import ui
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import guild_config_data as GCD

class GuildSalaryAssignProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildSalaryAssignProxy, self).__init__(uiAdapter)
        self.modelMap = {'changeTab': self.onChangeTab,
         'payGuildMembers': self.onPayGuildMembers,
         'getInitExpireType': self.onGetInitExpireType,
         'refreshView': self.updateView,
         'getTabEnable': self.onGetTabEnable,
         'changeType': self.onChangeType}
        self.mediator = None
        self.guildMemberData = None
        self.guildGroupMemberData = None
        self.curCashType = gametypes.GUILD_PAY_TYPE_CASH
        self.roleRate = {}
        self.dataType = uiConst.GUILD_SALARY_LIST_BY_ROLE
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_SALARY_ASSIGN, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_SALARY_ASSIGN:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_SALARY_ASSIGN)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.funcNpc.close()
        self.mediator = None
        self.curCashType = gametypes.GUILD_PAY_TYPE_CASH
        self.dataType = uiConst.GUILD_SALARY_LIST_BY_ROLE
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_SALARY_ASSIGN)

    def onChangeTab(self, *arg):
        self.curCashType = int(arg[3][0].GetNumber())
        self.updateView()

    def onChangeType(self, *arg):
        self.dataType = int(arg[3][0].GetNumber())
        self.updateView()

    def updateView(self, *arg):
        self.initGuildSalaryData()

    def onGetTabEnable(self, *arg):
        enableGuildPayCash = gameglobal.rds.configData.get('enableGuildPayCash', False)
        enableGuildPayCoin = gameglobal.rds.configData.get('enableGuildPayCoin', False)
        ret = [enableGuildPayCash, enableGuildPayCoin]
        return uiUtils.array2GfxAarry(ret)

    def requestRoleRate(self):
        BigWorld.player().cell.queryGuildPayrollSettings(self.curCashType, 0)

    def refreshRate(self, mtype, payroll, ver):
        self.roleRate[mtype] = [ver, payroll]
        self.initGuildSalaryData()

    @ui.checkInventoryLock()
    def onPayGuildMembers(self, *arg):
        p = BigWorld.player()
        if p.gbId != p.guild.leaderGbId:
            p.showGameMsg(GMDD.data.GUILD_SALARY_ASSIGN_NO_RIGHT, ())
        cashType = int(arg[3][0].GetNumber())
        expireType = int(arg[3][1].GetNumber())
        salaryTotal = int(arg[3][2].GetNumber())
        settings = arg[3][3]
        payments = arg[3][4]
        settingsLen = int(arg[3][5].GetNumber())
        paymentsLen = int(arg[3][6].GetNumber())
        settingConverted = self.convertSettings(settings, settingsLen)
        paymentsConverted = self.convertPayments(payments, paymentsLen)
        if self.dataType == uiConst.GUILD_SALARY_LIST_BY_ROLE:
            BigWorld.player().cell.payGuildMembers(cashType, expireType, salaryTotal, settingConverted, paymentsConverted, BigWorld.player().cipherOfPerson)
        elif self.dataType == uiConst.GUILD_SALARY_LIST_BY_ZHANDUI:
            BigWorld.player().cell.payGuildGroupMembers(cashType, expireType, salaryTotal, settingConverted, paymentsConverted, BigWorld.player().cipherOfPerson)

    def convertSettings(self, data, length):
        ret = []
        for index in xrange(length):
            temp = data.GetElement(index)
            obj = {}
            roleId = int(temp.GetMember('roleId').GetNumber())
            percent = int(temp.GetMember('percent').GetNumber())
            if self.dataType == uiConst.GUILD_SALARY_LIST_BY_ROLE:
                obj['roleId'] = roleId
            elif self.dataType == uiConst.GUILD_SALARY_LIST_BY_ZHANDUI:
                obj['groupId'] = roleId
            obj['percent'] = percent
            ret.append(obj)

        return ret

    def convertPayments(self, data, length):
        ret = []
        for index in xrange(length):
            temp = data.GetElement(index)
            obj = {}
            gbId = long(temp.GetMember('gbId').GetString())
            amount = int(temp.GetMember('amount').GetNumber())
            obj['gbId'] = gbId
            obj['amount'] = amount
            ret.append(obj)

        return ret

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

    def initGuildMembers(self):
        p = BigWorld.player()
        self.guildMemberData = {}
        temp = p.guild.member
        for memberId in temp:
            member = temp[memberId]
            if not self.guildMemberData.has_key(member.roleId):
                self.guildMemberData[member.roleId] = []
            self.guildMemberData[member.roleId].append(member)

    def initGuildGroupMember(self):
        p = BigWorld.player()
        self.guildGroupMemberData = {}
        temp = p.guild.member
        for memberId in temp:
            member = temp[memberId]
            if not self.guildGroupMemberData.has_key(member.groupId) and member.groupId > 0:
                self.guildGroupMemberData[member.groupId] = []
            if member.groupId > 0:
                self.guildGroupMemberData[member.groupId].append(member)

    def refreshView(self):
        if self.mediator:
            self.mediator.Invoke('refreshViewByOperation')

    def initGuildSalaryData(self):
        ret = {}
        p = BigWorld.player()
        ret['storage'] = 0
        if self.curCashType == gametypes.GUILD_PAY_TYPE_CASH:
            ret['storage'] = p.guild.reserveCash if hasattr(p.guild, 'reserveCash') else 0
        elif self.curCashType == gametypes.GUILD_PAY_TYPE_COIN:
            ret['storage'] = p.guild.reserveCoin if hasattr(p.guild, 'reserveCoin') else 0
        elif self.curCashType == gametypes.GUILD_PAY_TYPE_BIND_CASH:
            ret['storage'] = p.guild.reserveBindCash if hasattr(p.guild, 'reserveBindCash') else 0
        ret['total'] = 0
        ret['assigned'] = 0
        self.initGuildMembers()
        self.initGuildGroupMember()
        if self.dataType == uiConst.GUILD_SALARY_LIST_BY_ROLE:
            ret['roles'] = self._getRolesData()
        elif self.dataType == uiConst.GUILD_SALARY_LIST_BY_ZHANDUI:
            ret['roles'] = self._getGroupsData()
        ret['roles'].sort(key=lambda x: x['roleId'])
        self.guildCashCacheData = ret
        if self.mediator:
            self.mediator.Invoke('initGuildSalaryPanel', uiUtils.dict2GfxDict(ret, True))

    def _getRolesData(self):
        roles = []
        now = utils.getNow()
        for roleId in self.guildMemberData:
            roleObj = {}
            roleObj['roleId'] = roleId
            roleObj['roleName'] = gametypes.GUILD_ROLE_DICT[roleId]
            roleObj['rate'] = 0
            roleObj['totalCash'] = 0
            roleObj['assignedCash'] = 0
            roleObj['members'] = []
            for member in self.guildMemberData[roleId]:
                memberObj = {}
                memberObj['roleId'] = roleId
                memberObj['gbId'] = member.gbId
                memberObj['role'] = member.role
                memberObj['school'] = const.SCHOOL_DICT[member.school]
                memberObj['level'] = member.level
                memberObj['contrib'] = '%d' % member.contribTotal
                memberObj['salary'] = 0
                memberObj['enable'] = now - member.tJoin - const.GUILD_PAY_JOIN_TIME >= 0
                if self.curCashType == gametypes.GUILD_PAY_TYPE_CASH:
                    memberObj['maxSalary'] = GCD.data.get('maxCashSalary', 3000)
                elif self.curCashType == gametypes.GUILD_PAY_TYPE_COIN:
                    memberObj['maxSalary'] = GCD.data.get('maxCoinSalary', 3000)
                elif self.curCashType == gametypes.GUILD_PAY_TYPE_BIND_CASH:
                    memberObj['maxSalary'] = GCD.data.get('maxBindCashSalary', 3000)
                roleObj['members'].sort(key=lambda x: x['contrib'], reverse=True)
                roleObj['members'].append(memberObj)

            roles.append(roleObj)

        return roles

    def _getGroupName(self, gId):
        groups = BigWorld.player().guild.group
        for index in groups:
            if groups[index].groupId == gId:
                return groups[index].name

        return ''

    def _getGroupsData(self):
        groups = []
        now = utils.getNow()
        for groupId in self.guildGroupMemberData:
            roleObj = {}
            roleObj['roleId'] = groupId
            roleObj['roleName'] = self._getGroupName(groupId)
            roleObj['rate'] = 0
            roleObj['totalCash'] = 0
            roleObj['assignedCash'] = 0
            roleObj['members'] = []
            for member in self.guildGroupMemberData[groupId]:
                memberObj = {}
                memberObj['groupId'] = groupId
                memberObj['gbId'] = member.gbId
                memberObj['role'] = member.role
                memberObj['school'] = const.SCHOOL_DICT[member.school]
                memberObj['level'] = member.level
                memberObj['contrib'] = '%d' % member.contribTotal
                memberObj['salary'] = 0
                memberObj['enable'] = now - member.tJoin - const.GUILD_PAY_JOIN_TIME >= 0
                if self.curCashType == gametypes.GUILD_PAY_TYPE_CASH:
                    memberObj['maxSalary'] = GCD.data.get('maxCashSalary', 3000)
                elif self.curCashType == gametypes.GUILD_PAY_TYPE_COIN:
                    memberObj['maxSalary'] = GCD.data.get('maxCoinSalary', 3000)
                elif self.curCashType == gametypes.GUILD_PAY_TYPE_BIND_CASH:
                    memberObj['maxSalary'] = GCD.data.get('maxBindCashSalary', 3000)
                roleObj['members'].sort(key=lambda x: x['contrib'], reverse=True)
                roleObj['members'].append(memberObj)

            groups.append(roleObj)

        return groups

    def getRoleRate(self, roleId):
        if self.roleRate.has_key(self.curCashType):
            payRoll = self.roleRate[self.curCashType][1]
            for data in payRoll:
                if len(data) > 0 and data[0] == roleId:
                    return data[1]

        return 0
