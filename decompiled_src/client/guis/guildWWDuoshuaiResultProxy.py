#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildWWDuoshuaiResultProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import utils
from uiProxy import UIProxy
MAX_TEAM_NUM = 5
XIAN_FENG = 0
SHOU_BEI = 1
YU_BEI = 2

class GuildWWDuoshuaiResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildWWDuoshuaiResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.panel = None
        self.roundNum = 2
        self.firstRoundNum = 1
        self.thirdRoundNum = 3
        self.mineGroupIdxs = []
        self.enemyGroupIdxs = []

    def initPanel(self, widget, groupId):
        self.groupId = groupId
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.panel = None
        self.mineGroupIdxs = []
        self.enemyGroupIdxs = []

    def refreshPanel(self):
        if not self.widget:
            return
        self.mineGroupIdxs = []
        self.enemyGroupIdxs = []
        if self.teamInfo:
            self.getMineHostIdx()
            self.setServerName()
            self.setGroupBg()
            self.setGroup(True)
            if not self.isLucky and len(self.teamInfo) != 1:
                self.setGroup(False)
        self.clearGroups()

    def getMineHostIdx(self):
        mineHostId = utils.getHostId()
        self.mineHostIdx = 0
        if self.teamInfo[0][0] == mineHostId:
            self.mineHostIdx = 0
        else:
            self.mineHostIdx = 1

    def setServerName(self):
        self.panel.serverNameOfMine.text = utils.getServerName(self.teamInfo[self.mineHostIdx][0])
        if self.isLucky or len(self.teamInfo) == 1:
            return
        self.panel.serverNameOfEnemy.text = utils.getServerName(self.teamInfo[not self.mineHostIdx][0])

    def setGroupBg(self):
        for i in range(0, MAX_TEAM_NUM):
            if i % 2 == 0:
                self.panel.getChildByName('group' + str(i)).groupBg.gotoAndStop('shengbg')
            else:
                self.panel.getChildByName('group' + str(i)).groupBg.gotoAndStop('qianbg')

    def setGroup(self, side):
        p = BigWorld.player()
        tournamentResult = p.worldWar.tournamentResult
        if side:
            groupIdxs = self.mineGroupIdxs
            hostIdx = self.mineHostIdx
            nameColor = 'Chengse'
        else:
            groupIdxs = self.enemyGroupIdxs
            hostIdx = not self.mineHostIdx
            nameColor = 'Hongse'
        hostId = self.teamInfo[hostIdx][0]
        for result in self.teamInfo[hostIdx][1]:
            if result[0] == self.roundNum:
                groups = result[1]
                for group in groups:
                    if group[0] == 0 and group[1] == 0:
                        pass
                    else:
                        groupIdxs.append(group[4])
                    firstRoundIdL = tournamentResult.get(hostId).getIdx(self.groupId, self.firstRoundNum, group[0])
                    firstRoundIdR = tournamentResult.get(hostId).getIdx(self.groupId, self.firstRoundNum, group[1])
                    if group[0]:
                        secondWinGuild = tournamentResult.get(hostId).isFinished(self.groupId, self.roundNum, group[0])
                    else:
                        secondWinGuild = tournamentResult.get(hostId).isFinished(self.groupId, self.roundNum, group[1])
                    if side:
                        match = self.panel.getChildByName('group' + str(group[4])).groupM
                    else:
                        match = self.panel.getChildByName('group' + str(group[4])).groupE
                    self.setTeamIcon(match, group[4], group[0], group[1], secondWinGuild, firstRoundIdL, firstRoundIdR)
                    self.setMatchIcon(match, group[4])
                    self.setMatchName(match, group[4])
                    match.guildNameL.gotoAndStop(nameColor)
                    match.guildNameR.gotoAndStop(nameColor)
                    self.setTeamName(match, group[0], group[1])
                    self.setXunZhang(match, group[0], group[1], secondWinGuild)
                    self.setRankChange(match, group[0], group[1], secondWinGuild, group[4], firstRoundIdL, firstRoundIdR)

        self.setResultTeamList(hostId, side)

    def setResultTeamList(self, hostId, side):
        p = BigWorld.player()
        tournamentResult = p.worldWar.tournamentResult
        firstRoundGuilds = tournamentResult.get(hostId).getGuildsNUIDByRound(self.firstRoundNum, self.groupId)
        secondRoundGuilds = tournamentResult.get(hostId).getGuildsNUIDByRound(self.roundNum, self.groupId)
        thirdRoundGuilds = tournamentResult.get(hostId).getGuildsNUIDByRound(self.thirdRoundNum, self.groupId)
        if side:
            roundIn = self.panel.roundInL
        else:
            roundIn = self.panel.roundInR
        if not thirdRoundGuilds:
            if side:
                roundIn.gotoAndStop('Liahang')
            else:
                roundIn.gotoAndStop('Hongse')
        else:
            xianfeng = gameStrings.TEXT_GUILDWWDUOSHUAIRESULTPROXY_134
            shoubei = gameStrings.TEXT_GUILDWWDUOSHUAIRESULTPROXY_135
            xianfengGuilds = []
            shoubeiGuilds = []
            resultGuildNUIDs = tournamentResult.getResultGuilds(hostId, self.groupId)
            for i in range(0, len(resultGuildNUIDs)):
                if i < 4:
                    xianfengGuilds.append(resultGuildNUIDs[i])
                else:
                    shoubeiGuilds.append(resultGuildNUIDs[i])

            for i in range(0, len(xianfengGuilds)):
                if i == len(xianfengGuilds) - 1:
                    xianfeng += tournamentResult.getGuildName(xianfengGuilds[i])
                else:
                    xianfeng += tournamentResult.getGuildName(xianfengGuilds[i]) + gameStrings.TEXT_CHATPROXY_403

            for i in range(0, len(shoubeiGuilds)):
                if i == len(shoubeiGuilds) - 1:
                    shoubei += tournamentResult.getGuildName(shoubeiGuilds[i])
                else:
                    shoubei += tournamentResult.getGuildName(shoubeiGuilds[i]) + gameStrings.TEXT_CHATPROXY_403

            roundIn.xianfengText.text = xianfeng
            roundIn.shoubeiText.text = shoubei

    def clearGroups(self):
        for i in range(0, MAX_TEAM_NUM):
            if i not in self.mineGroupIdxs:
                self.panel.getChildByName('group' + str(i)).groupM.visible = False
            if self.isLucky or len(self.teamInfo) == 1:
                continue
            if i not in self.enemyGroupIdxs:
                self.panel.getChildByName('group' + str(i)).groupE.visible = False

    def getFirstRoundStatus(self, idx):
        if idx <= 1:
            return XIAN_FENG
        elif idx > 1 and idx <= 3:
            return SHOU_BEI
        else:
            return YU_BEI

    def setRankChange(self, match, guildNuidL, guildNuidR, winGuildNuid, idx, firstRoundIdL, firstRoundIdR):
        firstRoundStatusL = self.getFirstRoundStatus(firstRoundIdL)
        firstRoundStatusR = self.getFirstRoundStatus(firstRoundIdR)
        if winGuildNuid:
            if idx == 0 or idx == 1 or idx == 2:
                winStatus = XIAN_FENG
            elif idx == 3 or idx == 4:
                winStatus = SHOU_BEI
            if idx == 0:
                lostStatus = XIAN_FENG
            elif idx == 1 or idx == 2:
                lostStatus = SHOU_BEI
            elif idx == 3 or idx == 4:
                lostStatus = YU_BEI
            if winGuildNuid == guildNuidL:
                winFirstRound = firstRoundStatusL
                lostFirstRound = firstRoundStatusR
                winRankChange = match.rankChangeL
                lostRankChange = match.rankChangeR
            else:
                winFirstRound = firstRoundStatusR
                lostFirstRound = firstRoundStatusL
                winRankChange = match.rankChangeR
                lostRankChange = match.rankChangeL
            if winFirstRound == winStatus:
                winRankChange.visible = False
            else:
                winRankChange.visible = True
                winRankChange.gotoAndStop('Lvse')
            if lostStatus == YU_BEI:
                lostRankChange.visible = True
                lostRankChange.gotoAndStop('Hongse')
            elif lostFirstRound == lostStatus:
                lostRankChange.visible = False
            else:
                lostRankChange.visible = True
                lostRankChange.gotoAndStop('Hongse')
        else:
            match.rankChangeL.visible = False
            match.rankChangeR.visible = False
        if not guildNuidL:
            match.rankChangeL.visible = False
        if not guildNuidR:
            match.rankChangeR.visible = False

    def setMatchName(self, match, idx):
        if idx == 0:
            match.matchName.gotoAndStop('Guanjun')
        elif idx == 1 or idx == 2:
            match.matchName.gotoAndStop('Siqiang')
        else:
            match.matchName.gotoAndStop('Lieqiang')

    def setMatchIcon(self, match, idx):
        if idx == 0:
            match.matchIcon.gotoAndStop('guanjun')
        else:
            match.matchIcon.gotoAndStop('vs')

    def setTeamIcon(self, match, idx, guildNuidL, guildNuidR, winGuildNuid, firstRoundIdL, firstRoundIdR):
        p = BigWorld.player()
        if idx == 0:
            if winGuildNuid:
                if winGuildNuid == guildNuidL:
                    match.teamIconL.gotoAndStop('First')
                    match.teamIconR.gotoAndStop('Second')
                else:
                    match.teamIconL.gotoAndStop('Second')
                    match.teamIconR.gotoAndStop('First')
            match.teamIconL.gotoAndStop('Xian')
            match.teamIconR.gotoAndStop('Xian')
        else:
            if firstRoundIdL == 4 or firstRoundIdL == 5:
                match.teamIconL.gotoAndStop('Yu')
            elif firstRoundIdL == 2 or firstRoundIdL == 3:
                match.teamIconL.gotoAndStop('Shou')
            else:
                match.teamIconL.gotoAndStop('Xian')
            if firstRoundIdR == 4 or firstRoundIdR == 5:
                match.teamIconR.gotoAndStop('Yu')
            elif firstRoundIdR == 2 or firstRoundIdR == 3:
                match.teamIconR.gotoAndStop('Shou')
            else:
                match.teamIconR.gotoAndStop('Xian')
        if not guildNuidL:
            match.teamIconL.gotoAndStop('Hui')
        if not guildNuidR:
            match.teamIconR.gotoAndStop('Hui')

    def setXunZhang(self, match, guildNuidL, guildNuidR, secondWinGuild):
        if not secondWinGuild:
            match.winL.visible = False
            match.winR.visible = False
            return
        if secondWinGuild == guildNuidL:
            match.winL.gotoAndStop('XunZhang')
        else:
            match.winL.gotoAndStop('AoCao')
        if secondWinGuild == guildNuidR:
            match.winR.gotoAndStop('XunZhang')
        else:
            match.winR.gotoAndStop('AoCao')
        if not guildNuidL:
            match.winL.visible = False
        if not guildNuidR:
            match.winR.visible = False

    def setTeamName(self, match, guildNuidL, guildNuidR):
        p = BigWorld.player()
        if guildNuidL and p.guildNUID == guildNuidL[0]:
            match.guildNameL.gotoAndStop('BaiZi')
        if guildNuidR and p.guildNUID == guildNuidR[0]:
            match.guildNameR.gotoAndStop('BaiZi')
        match.guildNameL.nameT.text = p.worldWar.tournamentResult.getGuildName(guildNuidL)
        match.guildNameR.nameT.text = p.worldWar.tournamentResult.getGuildName(guildNuidR)
        if not match.guildNameL.nameT.text:
            match.guildNameL.gotoAndStop('Huizi')
            match.guildNameL.nameT.text = gameStrings.TEXT_ARENAPLAYOFFSPROXY_565
        if not match.guildNameR.nameT.text:
            match.guildNameR.gotoAndStop('Huizi')
            match.guildNameR.nameT.text = gameStrings.TEXT_ARENAPLAYOFFSPROXY_565

    def initUI(self):
        p = BigWorld.player()
        self.teamInfo = p.worldWar.tournamentResult.getDTOByGroup(self.groupId)
        self.isLucky = p.worldWar.isLucky()
        if not gameglobal.rds.configData.get('enableWorldWar', False):
            self.isLucky = True
        if self.isLucky or len(self.teamInfo) == 1:
            self.panel = self.widget.panelLucky
            self.widget.panel.visible = False
        else:
            self.panel = self.widget.panel
            self.widget.panelLucky.visible = False
        self.refreshPanel()
