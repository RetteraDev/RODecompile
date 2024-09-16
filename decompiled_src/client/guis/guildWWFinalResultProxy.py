#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildWWFinalResultProxy.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import gameglobal
import utils
from data import world_war_config_data as WWCD
from uiProxy import UIProxy
MAX_TEAM_NUM = 4

class GuildWWFinalResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildWWFinalResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.roundNum = 3
        self.mineServerGuilds = []
        self.enemyServerGuilds = []
        self.mineScore = 0
        self.enemyScore = 0
        self.groupIdxs = []

    def initPanel(self, widget, groupId):
        self.groupId = groupId
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.mineServerGuilds = []
        self.enemyServerGuilds = []
        self.mineScore = 0
        self.enemyScore = 0
        self.groupIdxs = []

    def refreshPanel(self):
        if not self.widget:
            return
        if self.teamInfo:
            mineHostId = utils.getHostId()
            self.mineHostIdx = 0
            if self.teamInfo[0][0] == mineHostId:
                self.mineHostIdx = 0
            else:
                self.mineHostIdx = 1
            self.getGuilds()
            self.setTitle()
            self.setGroup()
        self.clearGroup()

    def getGuilds(self):
        p = BigWorld.player()
        self.groupIdxs = []
        self.mineServerGuilds = []
        self.enemyServerGuilds = []
        if not self.teamInfo:
            return
        for result in self.teamInfo[0][1]:
            if result[0] == self.roundNum:
                groups = result[1]
                for group in groups:
                    mineGuildInfo = {}
                    enemyGuildInfo = {}
                    if p.worldWar.getCamp() == gametypes.WORLD_WAR_CAMP_ATTACK:
                        mineGuildInfo['nuid'] = group[0]
                        enemyGuildInfo['nuid'] = group[1]
                    else:
                        mineGuildInfo['nuid'] = group[1]
                        enemyGuildInfo['nuid'] = group[0]
                    mineGuildInfo['idx'] = group[4]
                    mineGuildInfo['winNuid'] = group[2]
                    enemyGuildInfo['idx'] = group[4]
                    enemyGuildInfo['winNuid'] = group[2]
                    self.mineServerGuilds.append(mineGuildInfo)
                    self.enemyServerGuilds.append(enemyGuildInfo)
                    self.groupIdxs.append(group[4])

    def setGroupBg(self):
        for i in range(0, MAX_TEAM_NUM):
            if i % 2 == 0:
                self.panel.matchPanel.getChildByName('group' + str(i)).groupBg.gotoAndStop('shengbg')
            else:
                self.panel.matchPanel.getChildByName('group' + str(i)).groupBg.gotoAndStop('qianbg')

    def setGroup(self):
        p = BigWorld.player()
        guildTournament = p.guildTournament.get(self.groupId)
        for i in range(0, MAX_TEAM_NUM):
            match = self.panel.matchPanel.getChildByName('group%d' % i).match
            if guildTournament.state == gametypes.GUILD_TOURNAMENT_STATE_FINISHED:
                if self.mineScore > self.enemyScore:
                    match.scoreR.gotoAndStop('Huise')
                else:
                    match.scoreL.gotoAndStop('Huise')

        for guild in self.mineServerGuilds:
            match = self.panel.matchPanel.getChildByName('group%d' % guild['idx']).match
            if not guild['nuid']:
                match.guildNameL.gotoAndStop('Huizi')
                match.guildNameL.nameT.text = gameStrings.TEXT_ARENAPLAYOFFSPROXY_565
                match.teamIconL.gotoAndStop('Hui')
            else:
                if guild['nuid'] and p.guildNUID == guild['nuid'][0]:
                    match.guildNameL.gotoAndStop('BaiZi')
                else:
                    match.guildNameL.gotoAndStop('Chengse')
                match.guildNameL.nameT.text = p.worldWar.tournamentResult.getGuildName(guild['nuid'])
            match.scoreL.scoreTxt.text = gameStrings.TEXT_GUILDWWFINALRESULTPROXY_111 % self.calGuildScore(guild)

        for guild in self.enemyServerGuilds:
            match = self.panel.matchPanel.getChildByName('group%d' % guild['idx']).match
            if not guild['nuid']:
                match.guildNameR.gotoAndStop('Huizi')
                match.guildNameR.nameT.text = gameStrings.TEXT_ARENAPLAYOFFSPROXY_565
                match.teamIconR.gotoAndStop('Hui')
            else:
                match.guildNameR.gotoAndStop('Hongse')
                match.guildNameR.nameT.text = p.worldWar.tournamentResult.getGuildName(guild['nuid'])
            match.scoreR.scoreTxt.text = gameStrings.TEXT_GUILDWWFINALRESULTPROXY_111 % self.calGuildScore(guild)

    def clearGroup(self):
        for i in range(0, MAX_TEAM_NUM):
            match = self.panel.matchPanel.getChildByName('group%d' % i).match
            if i not in self.groupIdxs:
                match.visible = False

    def setTitle(self):
        p = BigWorld.player()
        guildTournament = p.guildTournament.get(self.groupId)
        self.panel.title.winSignL.visible = False
        self.panel.title.winSignR.visible = False
        self.calTotalScore()
        if guildTournament.state == gametypes.GUILD_TOURNAMENT_STATE_FINISHED:
            self.panel.title.shineEffect.visible = True
            self.panel.title.jiangbeiEffect.visible = True
            if self.mineScore > self.enemyScore:
                self.panel.title.winSignL.visible = True
                self.panel.title.winSignR.visible = False
                self.panel.title.bgL.gotoAndStop('Shengli')
                self.panel.title.bgR.gotoAndStop('Shibai')
                self.panel.title.mineServerInfo.gotoAndStop('Shengliwenzi')
                self.panel.title.enemyServerInfo.gotoAndStop('Shibaiwenzi')
            else:
                self.panel.title.winSignL.visible = False
                self.panel.title.winSignR.visible = True
                self.panel.title.bgL.gotoAndStop('Shibai')
                self.panel.title.bgR.gotoAndStop('Shengli')
                self.panel.title.mineServerInfo.gotoAndStop('Shibaiwenzi')
                self.panel.title.enemyServerInfo.gotoAndStop('Shengliwenzi')
        else:
            self.panel.title.winSignL.visible = False
            self.panel.title.winSignR.visible = False
            self.panel.title.bgL.gotoAndStop('jinxingzhongzuo')
            self.panel.title.bgR.gotoAndStop('jinxingzhongzuo')
            self.panel.title.shineEffect.visible = False
            self.panel.title.jiangbeiEffect.visible = False
        self.panel.title.mineServerInfo.score.text = gameStrings.TEXT_GUILDWWFINALRESULTPROXY_160 % self.mineScore
        self.panel.title.enemyServerInfo.score.text = gameStrings.TEXT_GUILDWWFINALRESULTPROXY_160 % self.enemyScore
        self.setServerName()

    def calGuildScore(self, guild):
        score = 0
        if guild['winNuid']:
            if guild['winNuid'] == guild['nuid']:
                score += WWCD.data.get('tournamentScore', {}).get((self.groupId, guild['idx'] + 1), 0)
        return score

    def calTotalScore(self):
        self.mineScore = 0
        self.enemyScore = 0
        for guild in self.mineServerGuilds:
            self.mineScore += self.calGuildScore(guild)

        for guild in self.enemyServerGuilds:
            self.enemyScore += self.calGuildScore(guild)

    def setServerName(self):
        self.panel.title.mineServerInfo.nameT.text = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_660 % utils.getServerName(self.teamInfo[self.mineHostIdx][0])
        self.panel.title.enemyServerInfo.nameT.text = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_660 % utils.getServerName(self.teamInfo[not self.mineHostIdx][0])

    def initUI(self):
        p = BigWorld.player()
        self.panel = self.widget.panel
        self.teamInfo = p.worldWar.tournamentResult.getDTOByGroup(self.groupId)
        self.refreshPanel()

    def refreshInfo(self):
        if not self.widget:
            return
