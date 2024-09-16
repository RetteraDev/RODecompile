#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildCrossTResultProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import utils
import const
import gametypes
import datetime
from uiProxy import UIProxy
from data import cross_guild_tournament_schedule_data as CGTSD
from data import region_server_config_data as RSCD
MAX_GROUP_NUM = 4
MAX_GUILD_NUM = 4
MAX_ROUND_NUM = 3
MAX_MATCH_NUM = 2

class GuildCrossTResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildCrossTResultProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRankInfo': self.onGetRankInfo,
         'getScheduleInfo': self.onGetScheduleInfo,
         'clickLive': self.onClickLive}
        self.mediator = None
        self.groupId = 0
        self.currentTabIndex = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_RESULT, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_RESULT:
            self.mediator = mediator
            self.queryInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_RESULT)

    def reset(self):
        self.groupId = 0
        self.currentTabIndex = 0

    def show(self, groupId):
        self.groupId = groupId
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
            self.refreshInfo(self.groupId)
            self.queryInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_RESULT)

    def queryInfo(self):
        p = BigWorld.player()
        crossGuildTournament = p.crossGtn.get(self.groupId)
        p.cell.queryCrossGtn(self.groupId, crossGuildTournament.ver)

    def onGetRankInfo(self, *arg):
        self.currentTabIndex = uiConst.GUILD_CT_TAB_RANK
        self.refreshRankInfo(self.groupId)

    def onGetScheduleInfo(self, *arg):
        self.currentTabIndex = uiConst.GUILD_CT_TAB_SCHEDULE
        self.refreshScheduleInfo(self.groupId)

    def refreshInfo(self, groupId):
        if self.currentTabIndex == uiConst.GUILD_CT_TAB_RANK:
            self.refreshRankInfo(groupId)
        elif self.currentTabIndex == uiConst.GUILD_CT_TAB_SCHEDULE:
            self.refreshScheduleInfo(groupId)

    def refreshRankInfo(self, groupId):
        if self.groupId != groupId:
            return
        else:
            if self.mediator:
                p = BigWorld.player()
                crossGuildTournament = p.crossGtn.get(self.groupId)
                if crossGuildTournament is None:
                    return
                info = {}
                for i in xrange(MAX_GROUP_NUM):
                    groupInfo = {}
                    groupInfo['groupName'] = self.getGroupName(i)
                    guildList = []
                    if len(crossGuildTournament.groupGuildNUIDs) > i:
                        nuidList = crossGuildTournament.groupGuildNUIDs[i]
                        for j in xrange(MAX_GUILD_NUM):
                            guildNUID = nuidList[j] if len(nuidList) > j else 0
                            guildInfo = self.createGuildInfo(crossGuildTournament, guildNUID)
                            guildList.append(guildInfo)

                    else:
                        for j in xrange(MAX_GUILD_NUM):
                            guildInfo = self.createGuildInfo(crossGuildTournament, 0)
                            guildList.append(guildInfo)

                    guildList.sort(key=lambda x: x['score'], reverse=True)
                    lastScore = -1
                    rankIdx = 0
                    for guildInfo in guildList:
                        guildInfo['rank'] = 'none'
                        if guildInfo['guildName'] == '':
                            guildInfo['score'] = ''
                            guildInfo['rank'] = 'none'
                        else:
                            if guildInfo['score'] != lastScore:
                                lastScore = guildInfo['score']
                                rankIdx += 1
                            guildInfo['rank'] = 'rank%d' % rankIdx

                    groupInfo['guildList'] = guildList
                    info['groupInfo%d' % i] = groupInfo

                self.mediator.Invoke('refreshRankInfo', uiUtils.dict2GfxDict(info, True))
            return

    def getLiveBtnVisible(self, crossGuildTournament, roundNum):
        if crossGuildTournament.groupRoundNum != roundNum:
            return 0
        else:
            p = BigWorld.player()
            if p.gtnLiveType == gametypes.BATTLE_FIELD_DOMAIN_CROSS_GTN and crossGuildTournament.state == gametypes.CROSS_GTN_STATE_GROUP_MATCH:
                return 1
            return 0

    def onClickLive(self, *args):
        guildNUID = int(args[3][0].GetString())
        if guildNUID == 0 or self.groupId == 0:
            return
        p = BigWorld.player()
        p.cell.enterCrossWithLive(self.groupId, guildNUID)
        gameglobal.rds.ui.bFScoreAward.setBFInfo(self.groupId, uiConst.BF_SCORE_AWARD_CROSS_GTN_GROUP)

    def refreshScheduleInfo(self, groupId):
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
                    if roundNum <= 0 or scheduleData.get('state', 0) != gametypes.CROSS_GTN_STATE_GROUP_MATCH:
                        continue
                    weekNum = scheduleData.get('weekNum', 0)
                    nowWeekNum = crossGuildTournament.getWeekNum()
                    weekSecond = utils.getWeekSecond() + (weekNum - nowWeekNum) * const.TIME_INTERVAL_WEEK
                    dayTime = weekSecond + int(scheduleData.get('crontab', '0 0 * * 0')[-1]) * const.TIME_INTERVAL_DAY
                    info['roundName%d' % roundNum] = self.getRoundName(roundNum)
                    info['dayField%d' % roundNum] = datetime.datetime.fromtimestamp(dayTime).strftime('%m-%d')
                    info['timeField%d' % roundNum] = scheduleData.get('readyTime', '')

                for i in xrange(MAX_GROUP_NUM):
                    groupInfo = {}
                    groupInfo['groupName'] = self.getGroupName(i)
                    for j in xrange(MAX_ROUND_NUM):
                        roundInfo = {}
                        guildNUIDs = crossGuildTournament._getGroupMatchPairs(i, j + 1)
                        for k in xrange(MAX_MATCH_NUM):
                            matchInfo = {}
                            guildInfo0 = self.createGuildInfo(crossGuildTournament, guildNUIDs[k][0])
                            guildInfo1 = self.createGuildInfo(crossGuildTournament, guildNUIDs[k][1])
                            score = crossGuildTournament.groupMatchResult.get(guildNUIDs[k])
                            if score and j < crossGuildTournament.groupRoundNum:
                                if score[0] > score[1]:
                                    guildInfo0['state'] = 'win'
                                    guildInfo1['state'] = 'lose'
                                else:
                                    guildInfo0['state'] = 'lose'
                                    guildInfo1['state'] = 'win'
                                if guildInfo0['guildName'] == '' or guildInfo1['guildName'] == '':
                                    guildInfo0['score'] = ''
                                    guildInfo1['score'] = ''
                                else:
                                    guildInfo0['score'] = format(score[0], ',')
                                    guildInfo1['score'] = format(score[1], ',')
                            else:
                                guildInfo0['state'] = 'ready'
                                guildInfo1['state'] = 'ready'
                                guildInfo0['score'] = ''
                                guildInfo1['score'] = ''
                            matchInfo['guild0'] = guildInfo0
                            matchInfo['guild1'] = guildInfo1
                            matchInfo['liveBtnVisible'] = self.getLiveBtnVisible(crossGuildTournament, j + 1)
                            roundInfo['matchInfo%d' % k] = matchInfo

                        groupInfo['roundInfo%d' % j] = roundInfo

                    info['groupInfo%d' % i] = groupInfo

                self.mediator.Invoke('refreshScheduleInfo', uiUtils.dict2GfxDict(info, True))
            return

    def getGroupName(self, idx):
        if idx == 0:
            return gameStrings.TEXT_GUILDCROSSTRESULTPROXY_209
        elif idx == 1:
            return gameStrings.TEXT_GUILDCROSSTRESULTPROXY_211
        elif idx == 2:
            return gameStrings.TEXT_GUILDCROSSTRESULTPROXY_213
        else:
            return gameStrings.TEXT_GUILDCROSSTRESULTPROXY_215

    def getRoundName(self, roundNum):
        if roundNum == 1:
            return gameStrings.TEXT_GUILDCROSSTRESULTPROXY_219
        elif roundNum == 2:
            return gameStrings.TEXT_GUILDCROSSTRESULTPROXY_221
        else:
            return gameStrings.TEXT_GUILDCROSSTRESULTPROXY_223

    def createGuildInfo(self, crossGuildTournament, guildNUID):
        info = {}
        guildInfo = crossGuildTournament.guild.get(guildNUID)
        if guildInfo is None:
            info['guildName'] = ''
            info['serverName'] = ''
            info['score'] = -1
            info['tips'] = ''
            info['guildNUID'] = 0
        else:
            if guildNUID == BigWorld.player().guildNUID:
                info['guildName'] = uiUtils.toHtml(guildInfo.guildName, '#7ACC29')
            else:
                info['guildName'] = guildInfo.guildName
            info['serverName'] = RSCD.data.get(guildInfo.hostId, {}).get('serverName', '')
            info['score'] = guildInfo.groupScore
            info['tips'] = gameStrings.TEXT_GUILDCROSSTRESULTPROXY_242 % (guildInfo.guildName, info['serverName'], format(info['score'], ','))
            info['guildNUID'] = guildNUID
        return info
