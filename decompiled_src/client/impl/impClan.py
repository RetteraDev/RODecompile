#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impClan.o
import BigWorld
import gameglobal
import gametypes
from guis import uiConst
from cdata import game_msg_def_data as GMDD

class ImpClan(object):

    def updateClan(self, clanNUID, clanName):
        self.clanNUID = clanNUID
        self.clanName = clanName

    def onOpenCreateClan(self, npcId):
        pass

    def onOpenClanList(self, npcId, queryFor):
        npc = BigWorld.entities.get(npcId)
        if npc:
            npc.cell.queryClanList(queryFor)

    def onInviteClanMember(self, clanNUID, clanName, guildName):
        self.showGameMsg(GMDD.data.CLAN_INVITED, (clanName,))
        dataList = tuple(gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_CLAN_INVITE_MEMBER))
        for item in dataList:
            if item['data'] == (clanNUID, clanName, guildName):
                return

        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_CLAN_INVITE_MEMBER, {'data': (clanNUID, clanName, guildName)})

    def onClanInviteRejected(self, guildNUID, guildName):
        self.showGameMsg(GMDD.data.CLAN_INVITE_REJECTED, guildName)

    def onClanApplied(self, clanNUID, clanName):
        self.showGameMsg(GMDD.data.CLAN_APPLY_JOIN_OK, (clanName,))

    def onClanApplyRejected(self, clanNUID, clanName):
        self.showGameMsg(GMDD.data.CLAN_APPLY_REJECTED, (clanName,))

    def onClanAddGuild(self, data):
        guildNUID, guildName, leaderRole = data
        self.onClanDelApply(guildNUID)
        self.showGameMsg(GMDD.data.CLAN_JOIN_OTHER, (guildName,))

    def onClanDelGuild(self, guildNUID):
        pass

    def onClanAddApply(self, data):
        guildNUID, guildName, leaderRole = data
        self.showGameMsg(GMDD.data.CLAN_APPLY, (guildName,))

    def onClanDelApply(self, guildNUID):
        pass

    def onGetAllClan(self, data):
        queryFor, clanListData = data

    def onGetClan(self, data):
        pass

    def onGetClanApply(self, data):
        pass

    def onGetClanAllGuild(self, data):
        gameglobal.rds.ui.clanWar.setClanAllGuildList(data)

    def onGetDeclareWarAllGuild(self, data):
        gameglobal.rds.ui.clanWar.setClanAllGuildList(data)

    def onDismissClan(self):
        pass

    def onLeaveClan(self):
        pass

    def refreshClanApplyList(self):
        pass

    def set_clanNUID(self, old):
        if self.inClanWar and old != self.clanNUID:
            if BigWorld.player() == self:
                self._updateClanWarTopLogo()
            else:
                BigWorld.player()._updateClanWarTopLogoByEntId(self.id)
        if BigWorld.player() == self:
            gameglobal.rds.ui.chat.updatePadChannels()

    def onSearchGuild(self, queryStr, data, useFor):
        gameglobal.rds.ui.guild.searchGuildBack(queryStr, data, useFor)

    def onSearchClan(self, queryStr, data, useFor):
        gameglobal.rds.ui.guild.searchClanBack(queryStr, data, useFor)

    def onGetClanGuilds(self, clanNUID, data, useFor):
        gameglobal.rds.ui.guild.updateClanGuilds(clanNUID, data, useFor)
