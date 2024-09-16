#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMatchProxy.o
import gameglobal
import BigWorld
import gametypes
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from data import guild_tournament_data as GTD

class GuildMatchProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMatchProxy, self).__init__(uiAdapter)
        self.modelMap = {'getLeftInfo': self.onGetLeftInfo,
         'getRightInfo': self.onGetRightInfo,
         'clickEnter': self.onClickEnter,
         'clickCancel': self.onClickCancel}
        self.mediator = None
        self.matchId = 0
        self.showMatches = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MATCH_WIDGET, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_MATCH_WIDGET:
            self.mediator = mediator

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_MATCH_WIDGET)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_MATCH_WIDGET)

    def reset(self):
        self.mediator = None
        self.matchId = 0
        self.showMatches = []

    def onGetLeftInfo(self, *args):
        p = BigWorld.player()
        leftInfo = []
        for id in p.guildTournament.keys():
            matchName = GTD.data.get(id, {}).get('name', '')
            if matchName:
                leftInfo.append({'matchName': matchName,
                 'matchId': id})

        return uiUtils.array2GfxAarry(leftInfo, True)

    def onGetRightInfo(self, *args):
        p = BigWorld.player()
        self.matchId = args[3][0].GetNumber()
        guildTournament = p.guildTournament[self.matchId]
        rightInfo = self.getRightInfo(self.matchId)
        p.cell.queryGuildTournament(self.matchId, guildTournament.ver)
        return uiUtils.array2GfxAarry(rightInfo, True)

    def getRightInfo(self, matchId):
        ret = []
        p = BigWorld.player()
        guildTournament = p.guildTournament[matchId]
        matches = guildTournament.matches
        if guildTournament.state == gametypes.GUILD_TOURNAMENT_STATE_FINISHED:
            return ret
        if guildTournament.state != gametypes.GUILD_TOURNAMENT_STATE_MATCH:
            return ret
        if not matches:
            return ret
        curNum = guildTournament.roundNum - 1
        if curNum < 0:
            return ret
        guilds = guildTournament.guild
        guildIds = matches[curNum]
        for index in xrange(0, len(guildIds), 2):
            if index + 1 >= len(guildIds):
                continue
            matchInfo = {}
            guildId1 = matches[curNum][index]
            guildId2 = matches[curNum][index + 1]
            if not guildId1 or not guildId2:
                continue
            guildName1 = guilds.get(guildId1, '')
            guildName2 = guilds.get(guildId2, '')
            if not guildName1 or not guildName2:
                continue
            matchInfo['guildName1'] = guildName1
            matchInfo['guildName2'] = guildName2
            matchInfo['serverName1'] = ''
            matchInfo['serverName2'] = ''
            ret.append(matchInfo)
            self.showMatches.append([guildId1, guildId2])

        return ret

    def refreshInfo(self, matchId):
        if self.matchId != matchId:
            return
        rightInfo = self.getRightInfo(matchId)
        self.mediator.Invoke('refreshRight', uiUtils.array2GfxAarry(rightInfo, True))

    def onClickEnter(self, *args):
        index = args[3][0].GetNumber()
        p = BigWorld.player()
        if index >= len(self.showMatches):
            return
        p.cell.enterGuildTournamentWithLive(self.matchId, self.showMatches[index][0])

    def onClickCancel(self, *args):
        self.hide()
