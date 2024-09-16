#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildCrossTFinalResultProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import utils
import const
import gametypes
from uiProxy import UIProxy
from data import cross_guild_tournament_schedule_data as CGTSD
from data import region_server_config_data as RSCD
MAX_ROUND_MATCH_NUM = 2

class GuildCrossTFinalResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildCrossTFinalResultProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickLive': self.onClickLive}
        self.mediator = None
        self.groupId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_FINAL_RESULT, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_FINAL_RESULT:
            self.mediator = mediator
            self.refreshInfo(self.groupId)
            self.queryInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_FINAL_RESULT)

    def reset(self):
        self.groupId = 0

    def show(self, groupId):
        self.groupId = groupId
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo(self.groupId)
            self.queryInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_FINAL_RESULT)

    def onClickLive(self, *args):
        guildNUID = int(args[3][0].GetString())
        if guildNUID == 0 or self.groupId == 0:
            return
        p = BigWorld.player()
        p.cell.enterCrossWithLive(self.groupId, guildNUID)
        gameglobal.rds.ui.bFScoreAward.setBFInfo(self.groupId, uiConst.BF_SCORE_AWARD_CROSS_GTN_PLAYOFF)

    def queryInfo(self):
        p = BigWorld.player()
        crossGuildTournament = p.crossGtn.get(self.groupId)
        p.cell.queryCrossGtn(self.groupId, crossGuildTournament.ver)

    def refreshInfo(self, groupId):
        if self.groupId != groupId:
            return
        else:
            if self.mediator:
                p = BigWorld.player()
                crossGuildTournament = p.crossGtn.get(self.groupId)
                if crossGuildTournament is None:
                    return
                info = {}
                for scheduleData in CGTSD.data.itervalues():
                    roundNum = scheduleData.get('round', 0)
                    if roundNum <= 0 or scheduleData.get('state', 0) != gametypes.CROSS_GTN_STATE_PLAYOFF_MATCH:
                        continue
                    weekNum = scheduleData.get('weekNum', 0)
                    nowWeekNum = crossGuildTournament.getWeekNum()
                    weekSecond = utils.getWeekSecond() + (weekNum - nowWeekNum) * const.TIME_INTERVAL_WEEK
                    dayTime = weekSecond + int(scheduleData.get('crontab', '0 0 * * 0')[-1]) * const.TIME_INTERVAL_DAY
                    info['dayTime%d' % roundNum] = utils.formatDate(dayTime)

                for i in xrange(MAX_ROUND_MATCH_NUM):
                    self.createMatchInfo(crossGuildTournament, info, 'first', 0, i)

                for i in xrange(MAX_ROUND_MATCH_NUM):
                    self.createMatchInfo(crossGuildTournament, info, 'second', 1, i)

                for i in xrange(MAX_ROUND_MATCH_NUM):
                    self.createMatchInfo(crossGuildTournament, info, 'third', 2, i)

                self.createMatchInfo(crossGuildTournament, info, 'fourth', 3, 0)
                self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            return

    def getLiveBtnVisible(self, crossGuildTournament, roundNum):
        p = BigWorld.player()
        if crossGuildTournament.playoffRoundNum != roundNum:
            return 0
        elif p.gtnLiveType == gametypes.BATTLE_FIELD_DOMAIN_CROSS_GTN and crossGuildTournament.state == gametypes.CROSS_GTN_STATE_PLAYOFF_MATCH:
            return 1
        else:
            return 0

    def createMatchInfo(self, crossGuildTournament, info, headString, roundNum, matchNum):
        playoffMatches = crossGuildTournament.playoffMatches
        playoffMatchResult = crossGuildTournament.playoffMatchResult
        roundInfo = {}
        if len(playoffMatches) > roundNum and len(playoffMatches[roundNum]) >= (matchNum + 1) * 2:
            guild1 = playoffMatches[roundNum][matchNum * 2]
            guild2 = playoffMatches[roundNum][matchNum * 2 + 1]
            roundInfo['leftGuildInfo'] = self.createGuildInfo(crossGuildTournament, guild1, True)
            roundInfo['rightGuildInfo'] = self.createGuildInfo(crossGuildTournament, guild2, True)
            roundInfo['liveBtnVisible'] = self.getLiveBtnVisible(crossGuildTournament, roundNum + 1)
            if len(playoffMatchResult) > roundNum:
                winner = 0
                score = playoffMatchResult[roundNum].get((guild1, guild2))
                if score:
                    if score[0] > score[1]:
                        winner = guild1
                        roundInfo['winnerInfo'] = self.createGuildInfo(crossGuildTournament, guild1, False)
                        roundInfo['result'] = 'w1'
                        roundInfo['leftGuildInfo']['state'] = 'win'
                        roundInfo['rightGuildInfo']['state'] = 'lose'
                    else:
                        winner = guild2
                        roundInfo['winnerInfo'] = self.createGuildInfo(crossGuildTournament, guild2, False)
                        roundInfo['result'] = 'w2'
                        roundInfo['leftGuildInfo']['state'] = 'lose'
                        roundInfo['rightGuildInfo']['state'] = 'win'
                    roundInfo['leftGuildInfo']['score'] = format(score[0], ',')
                    roundInfo['rightGuildInfo']['score'] = format(score[1], ',')
                else:
                    roundInfo['winnerInfo'] = {'state': 'none',
                     'rank': 'none'}
                    roundInfo['result'] = 'none'
                if roundNum == 3 and matchNum == 0:
                    if winner != 0:
                        roundInfo['winnerInfo']['rank'] = 'rank1'
                        if winner == guild1:
                            roundInfo['rightGuildInfo']['rank'] = 'rank2'
                        else:
                            roundInfo['leftGuildInfo']['rank'] = 'rank2'
                elif roundNum == 2 and matchNum == 1:
                    if winner != 0:
                        if winner == guild1:
                            roundInfo['rightGuildInfo']['rank'] = 'rank3'
                        else:
                            roundInfo['leftGuildInfo']['rank'] = 'rank3'
                elif roundNum == 1 and matchNum == 1:
                    if winner != 0:
                        if winner == guild1:
                            roundInfo['rightGuildInfo']['rank'] = 'rank4'
                        else:
                            roundInfo['leftGuildInfo']['rank'] = 'rank4'
            else:
                roundInfo['winnerInfo'] = {'state': 'none',
                 'rank': 'none'}
                roundInfo['result'] = 'none'
            if roundNum == 2 and matchNum == 0:
                roundInfo['winnerInfo'] = self.createGuildInfo(crossGuildTournament, guild1, False)
                roundInfo['result'] = 'none'
        else:
            roundInfo['winnerInfo'] = {'state': 'none',
             'rank': 'none'}
            roundInfo['leftGuildInfo'] = {'state': 'none',
             'rank': 'none'}
            roundInfo['rightGuildInfo'] = {'state': 'none',
             'rank': 'none'}
            roundInfo['result'] = 'none'
            roundInfo['liveBtnVisible'] = 0
        if roundNum == 2 and matchNum == 0:
            roundInfo['state'] = 'empty'
        else:
            roundInfo['state'] = 'normal'
        info['%sRound%d' % (headString, matchNum)] = roundInfo

    def createGuildInfo(self, crossGuildTournament, guildNUID, needScore):
        info = {}
        info['state'] = 'ready'
        info['rank'] = 'none'
        info['score'] = '0' if needScore else ''
        info['guildNUID'] = guildNUID
        guildInfo = crossGuildTournament.guild.get(guildNUID)
        if guildInfo is None:
            info['guildName'] = ''
            info['serverName'] = ''
        else:
            if guildNUID == BigWorld.player().guildNUID:
                info['guildName'] = uiUtils.toHtml(guildInfo.guildName, '#7ACC29')
            else:
                info['guildName'] = guildInfo.guildName
            info['serverName'] = RSCD.data.get(guildInfo.hostId, {}).get('serverName', '')
        return info
