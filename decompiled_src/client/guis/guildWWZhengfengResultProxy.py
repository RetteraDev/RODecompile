#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildWWZhengfengResultProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import utils
from uiProxy import UIProxy
MAX_TEAM_NUM = 6

class GuildWWZhengfengResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildWWZhengfengResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.roundNum = 1
        self.panel = None
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
        if not hasattr(self, 'teamInfo'):
            return
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
        self.panel.serverNameOfEnemy.text = utils.getServerName(self.teamInfo[int(not self.mineHostIdx)][0])

    def setGroupBg(self):
        for i in range(0, MAX_TEAM_NUM):
            if i % 2 == 0:
                self.panel.getChildByName('group' + str(i)).groupBg.gotoAndStop('shengbg')
            else:
                self.panel.getChildByName('group' + str(i)).groupBg.gotoAndStop('qianbg')

    def setGroup(self, side):
        p = BigWorld.player()
        if side:
            nameColor = 'Chengse'
            groupIdxs = self.mineGroupIdxs
            hostIdx = self.mineHostIdx
        else:
            nameColor = 'Hongse'
            groupIdxs = self.enemyGroupIdxs
            hostIdx = not self.mineHostIdx
        for result in self.teamInfo[hostIdx][1]:
            if result[0] == self.roundNum:
                groups = result[1]
                for group in groups:
                    if group[0] == 0 and group[1] == 0:
                        pass
                    else:
                        groupIdxs.append(group[4])
                    hostId = self.teamInfo[hostIdx][0]
                    if group[0]:
                        winGuildNuid = p.worldWar.tournamentResult.get(hostId).isFinished(self.groupId, self.roundNum, group[0])
                    else:
                        winGuildNuid = p.worldWar.tournamentResult.get(hostId).isFinished(self.groupId, self.roundNum, group[1])
                    if side:
                        match = self.panel.getChildByName('group' + str(group[4])).groupM
                    else:
                        match = self.panel.getChildByName('group' + str(group[4])).groupE
                    self.setTeamIcon(match, group[0], group[1], group[4])
                    match.guildNameL.gotoAndStop(nameColor)
                    match.guildNameR.gotoAndStop(nameColor)
                    self.setTeamName(match, group[0], group[1])
                    self.setXunZhang(match, group[0], group[1], winGuildNuid)
                    self.setRankChange(match, group[0], group[1], winGuildNuid, group[4])

    def clearGroups(self):
        for i in range(0, MAX_TEAM_NUM):
            if i not in self.mineGroupIdxs:
                self.panel.getChildByName('group' + str(i)).groupM.visible = False
            if self.isLucky or len(self.teamInfo) == 1:
                continue
            if i not in self.enemyGroupIdxs:
                self.panel.getChildByName('group' + str(i)).groupE.visible = False

    def setRankChange(self, match, guildNuidL, guildNuidR, winGuildNuid, idx):
        if idx == 4 or idx == 5:
            if winGuildNuid:
                if winGuildNuid == guildNuidL:
                    match.rankChangeL.visible = False
                    match.rankChangeR.visible = True
                    match.rankChangeR.gotoAndStop('Hongse')
                else:
                    match.rankChangeR.visible = False
                    match.rankChangeL.visible = True
                    match.rankChangeL.gotoAndStop('Hongse')
            else:
                match.rankChangeL.visible = False
                match.rankChangeR.visible = False
        else:
            match.rankChangeL.visible = False
            match.rankChangeR.visible = False
        if not guildNuidL:
            match.rankChangeL.visible = False
        if not guildNuidR:
            match.rankChangeR.visible = False

    def setTeamIcon(self, match, guildNuidL, guildNuidR, idx):
        if idx <= 1:
            match.teamIconL.gotoAndStop('Xian')
            match.teamIconR.gotoAndStop('Xian')
        elif idx > 1 and idx <= 3:
            match.teamIconL.gotoAndStop('Shou')
            match.teamIconR.gotoAndStop('Shou')
        elif idx > 3:
            match.teamIconL.gotoAndStop('Yu')
            match.teamIconR.gotoAndStop('Yu')
        if not guildNuidL:
            match.teamIconL.gotoAndStop('Hui')
        if not guildNuidR:
            match.teamIconR.gotoAndStop('Hui')

    def setXunZhang(self, match, guildNuidL, guildNuidR, winGuildNuid):
        if not winGuildNuid:
            match.winL.visible = False
            match.winR.visible = False
            return
        if guildNuidL == winGuildNuid and winGuildNuid:
            match.winL.gotoAndStop('XunZhang')
        else:
            match.winL.gotoAndStop('AoCao')
        if guildNuidR == winGuildNuid and winGuildNuid:
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
        self.isLucky = p.worldWar.isLucky()
        if not gameglobal.rds.configData.get('enableWorldWar', False):
            self.isLucky = True
        self.teamInfo = p.worldWar.tournamentResult.getDTOByGroup(self.groupId)
        if self.isLucky or len(self.teamInfo) == 1:
            self.panel = self.widget.panelLucky
            self.widget.panel.visible = False
        else:
            self.panel = self.widget.panel
            self.widget.panelLucky.visible = False
        self.refreshPanel()

    def refreshInfo(self):
        if not self.widget:
            return
