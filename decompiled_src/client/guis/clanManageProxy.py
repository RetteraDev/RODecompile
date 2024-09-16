#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/clanManageProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
import uiUtils
import gametypes
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import UIProxy
from helpers import taboo
from callbackHelper import Functor
from data import guild_config_data as GCD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class ClanManageProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClanManageProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'dismiss': self.onDismiss,
         'leave': self.onLeave,
         'reject': self.onReject,
         'kick': self.onKick,
         'accept': self.onAccept,
         'reName': self.onReName,
         'inviteGuild': self.onInviteGuild,
         'queryClanAllGuild': self.onQueryClanAllGuild,
         'getClanCash': self.onGetClanCash}
        self.mediator = None
        self.applyDict = {}
        self.guildDict = {}
        self.leaderGuildNUID = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLAN_MANAGE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CLAN_MANAGE:
            self.mediator = mediator

    def show(self, data):
        if not gameglobal.rds.configData.get('enableClan', False):
            BigWorld.player().showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        p = BigWorld.player()
        if p.clanNUID and p.guildNUID and p.guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER and not self.mediator:
            for applyGuild in data[2]:
                self.applyDict[applyGuild[0]] = applyGuild

            for guild in data[1]:
                self.guildDict[guild[0]] = guild

            self.leaderGuildNUID = data[0]
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CLAN_MANAGE)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CLAN_MANAGE)

    def reset(self):
        self.applyDict = {}
        self.guildDict = {}
        self.leaderGuildNUID = 0

    def onInitData(self, *arg):
        p = BigWorld.player()
        if not (p.guildNUID and p.clanNUID and p.guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER):
            self.hide()
            return
        self.updateGuildList()
        clanData = [p.clanName,
         self.guildDict[self.leaderGuildNUID][1],
         GCD.data.get('clanRenameFee', const.CLAN_RENAME_FEE),
         self.leaderGuildNUID == p.guildNUID]
        return uiUtils.array2GfxAarry(clanData, True)

    def onGetClanCash(self, *arg):
        return GfxValue(BigWorld.player().guild.bindCash)

    def onDismiss(self, *arg):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox('确定解散联盟（一天之内只能加入或创建联盟一次）?', self._onConfirmDismiss)

    def _onConfirmDismiss(self):
        BigWorld.player().cell.dismissClan()

    def onLeave(self, *arg):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox('确定离开联盟（一天之内只能加入或创建联盟一次）?', self._onConfirmLeave)

    def _onConfirmLeave(self):
        BigWorld.player().cell.leaveClan()

    def onReName(self, *arg):
        p = BigWorld.player()
        name = unicode2gbk(arg[3][0].GetString())
        result, _ = taboo.checkNameDisWord(name)
        if not result:
            p.showGameMsg(GMDD.data.CLAN_NAME_TABOO, ())
            return
        nameLength = int(arg[3][1].GetString())
        if nameLength < const.CLAN_NAME_MIN_LEN / 2:
            p.showGameMsg(GMDD.data.CLAN_INVALID_NAME, (const.CLAN_NAME_MIN_LEN / 2, const.CLAN_NAME_MAX_LEN / 2))
            return
        p.cell.renameClan(name)

    def onQueryClanAllGuild(self, *arg):
        BigWorld.player().cell.queryClanAllGuild()

    def onInviteGuild(self, *arg):
        BigWorld.player().cell.inviteClanMember(int(arg[3][0].GetString()))

    def onAccept(self, *arg):
        BigWorld.player().cell.acceptClanApply(int(arg[3][0].GetString()))

    def onReject(self, *arg):
        BigWorld.player().cell.rejectClanApply(int(arg[3][0].GetString()))

    def onKick(self, *arg):
        BigWorld.player().cell.kickoutClanMember(int(arg[3][0].GetString()))

    def updateInviteGuild(self, data):
        if self.mediator:
            inviteGuildData = []
            for item in data:
                if item[0] not in self.guildDict:
                    inviteGuildData.append((str(item[0]), item[1], item[2]))

            self.mediator.Invoke('updateInviteGuild', uiUtils.array2GfxAarry(inviteGuildData, True))

    def updateGuildList(self):
        if self.mediator:
            guildData = []
            for id in self.applyDict:
                guildData.append((str(self.applyDict[id][0]),
                 self.applyDict[id][1] + '[申请]',
                 self.applyDict[id][2],
                 True))

            for id in self.guildDict:
                guildData.append((str(self.guildDict[id][0]),
                 self.guildDict[id][1],
                 self.guildDict[id][2],
                 False))

            self.mediator.Invoke('updateGuildList', uiUtils.array2GfxAarry(guildData, True))

    def updateCash(self):
        if self.mediator:
            self.mediator.Invoke('updateCash', GfxValue(BigWorld.player().guild.bindCash))

    def updateName(self):
        if self.mediator:
            self.mediator.Invoke('updateName', GfxValue(gbk2unicode(BigWorld.player().clanName)))

    def clickPushInvite(self):
        inviteData = gameglobal.rds.ui.pushMessage.getLastData(uiConst.MESSAGE_TYPE_CLAN_INVITE_MEMBER).get('data', None)
        if inviteData:
            clanNUID, clanName, guildName = inviteData
            clanJoinFee = GCD.data.get('clanJoinFee', const.CLAN_JOIN_FEE)
            text = GMD.data.get(GMDD.data.CLAN_INVITE_CONFIRM).get('text')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(text % (guildName, clanName, clanJoinFee), Functor(self.acceptClanInvite, clanNUID), '加入', None, '取消')
            gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_CLAN_INVITE_MEMBER, {'data': inviteData})

    def acceptClanInvite(self, clanNUID):
        BigWorld.player().cell.acceptClanInvite(clanNUID)
