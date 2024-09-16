#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildTournamentResultProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import const
import utils
from uiProxy import UIProxy
from helpers.guild import getGTNSD

class GuildTournamentResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildTournamentResultProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        self.groupId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_TOURNAMENT_RESULT, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_TOURNAMENT_RESULT:
            self.mediator = mediator
            self.refreshInfo(self.groupId)
            self.queryInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_TOURNAMENT_RESULT)

    def reset(self):
        self.groupId = 0

    def show(self, groupId):
        self.groupId = groupId
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo(self.groupId)
            self.queryInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_TOURNAMENT_RESULT)

    def queryInfo(self):
        p = BigWorld.player()
        guildTournament = p.guildTournament.get(self.groupId)
        p.cell.queryGuildTournament(self.groupId, guildTournament.ver)

    def refreshInfo(self, groupId):
        if self.groupId != groupId:
            return
        if self.mediator:
            p = BigWorld.player()
            guildTournament = p.guildTournament.get(self.groupId)
            if not guildTournament:
                return
            info = {}
            for scheduleData in getGTNSD().data.itervalues():
                roundNum = scheduleData.get('round', 0)
                if roundNum <= 0:
                    continue
                dayTime = utils.getWeekSecond() + int(scheduleData.get('crontab', '0 0 * * 0')[-1]) * const.TIME_INTERVAL_DAY
                info['dayTime%d' % roundNum] = utils.formatDate(dayTime)

            top4 = guildTournament.getTop4()
            info['firstPrize'] = guildTournament.guild.get(top4[0], '')
            info['secondPrize'] = guildTournament.guild.get(top4[1], '')
            info['thirdPrize'] = guildTournament.guild.get(top4[2], '')
            info['fourthPrize'] = guildTournament.guild.get(top4[3], '')
            for i in xrange(const.GUILD_TOURNAMENT_MAX_CANDIDATES / 2):
                info['firstRoundResult%d' % i] = 'none'

            self.createMatchInfo(guildTournament, info, 'first', 0, const.GUILD_TOURNAMENT_MAX_CANDIDATES)
            for i in xrange(const.GUILD_TOURNAMENT_MAX_CANDIDATES / 4):
                info['secondRoundResult%d' % i] = 'none'

            self.createMatchInfo(guildTournament, info, 'second', 1, const.GUILD_TOURNAMENT_MAX_CANDIDATES / 2)
            for i in xrange(const.GUILD_TOURNAMENT_MAX_CANDIDATES / 8):
                info['thirdRoundResult%d' % i] = 'none'

            self.createMatchInfo(guildTournament, info, 'third', 2, const.GUILD_TOURNAMENT_MAX_CANDIDATES / 4)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def createMatchInfo(self, guildTournament, info, headString, roundNum, maxCandidates):
        matches = guildTournament.matches
        if len(matches) > roundNum and len(matches[roundNum]) == maxCandidates:
            if len(matches) > roundNum + 1 and len(matches[roundNum + 1]) >= maxCandidates / 2:
                for i in xrange(maxCandidates):
                    roundInfo = {}
                    if matches[roundNum][i] == 0:
                        roundInfo['state'] = 'none'
                    elif matches[roundNum + 1][i / 2] == 0:
                        roundInfo['state'] = 'ready'
                    elif matches[roundNum][i] == matches[roundNum + 1][i / 2]:
                        roundInfo['state'] = 'win'
                        if i % 2 == 0:
                            info['%sRoundResult%d' % (headString, i / 2)] = 'w1'
                        else:
                            info['%sRoundResult%d' % (headString, i / 2)] = 'w2'
                    else:
                        roundInfo['state'] = 'lose'
                    if matches[roundNum][i] == BigWorld.player().guildNUID:
                        roundInfo['name'] = uiUtils.toHtml(guildTournament.guild.get(matches[roundNum][i], ''), '#7ACC29')
                    else:
                        roundInfo['name'] = guildTournament.guild.get(matches[roundNum][i], '')
                    info['%sRound%d' % (headString, i)] = roundInfo

            else:
                for i in xrange(maxCandidates):
                    roundInfo = {}
                    roundInfo['state'] = 'ready'
                    if matches[roundNum][i] == BigWorld.player().guildNUID:
                        roundInfo['name'] = uiUtils.toHtml(guildTournament.guild.get(matches[roundNum][i], ''), '#7ACC29')
                    else:
                        roundInfo['name'] = guildTournament.guild.get(matches[roundNum][i], '')
                    info['%sRound%d' % (headString, i)] = roundInfo

        else:
            for i in xrange(maxCandidates):
                roundInfo = {}
                roundInfo['state'] = 'none'
                roundInfo['name'] = ''
                info['%sRound%d' % (headString, i)] = roundInfo
