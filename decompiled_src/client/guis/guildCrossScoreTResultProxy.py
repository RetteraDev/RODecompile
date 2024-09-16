#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildCrossScoreTResultProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
import utils
import gametypes
from guis import uiUtils
from guis import events
from data import region_server_config_data as RSCD
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings

class GuildCrossScoreTResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildCrossScoreTResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.matchCache = []
        self.rankCache = []
        self.currentRound = 0
        self.groupId = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_CROSS_TORNAMENT_SCORE, self.hide)

    def reset(self):
        self.groupId = 0
        self.currentRound = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_CROSS_TORNAMENT_SCORE:
            self.widget = widget
            self.initUI()
            self.refreshInfo(self.groupId)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_CROSS_TORNAMENT_SCORE)

    def show(self, groupId):
        self.groupId = groupId
        self.queryInfo()
        self.currentRound = self.getCurrRound()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_CROSS_TORNAMENT_SCORE)
        else:
            self.refreshInfo(groupId)

    def queryInfo(self):
        p = BigWorld.player()
        crossGuildTournament = p.crossGtn.get(self.groupId)
        p.cell.queryCrossGtn(self.groupId, crossGuildTournament.ver)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick)
        self.widget.rankWnd.closeBtn.addEventListener(events.BUTTON_CLICK, self.onRankCloseBtnClick)
        self.widget.matchList.labelFunction = self.matchItemLabelFunc
        self.widget.matchList.itemRenderer = 'GuildCrossScoreTResult_Match_item'
        self.widget.matchList.dataArray = []
        self.widget.rankWnd.rankList.labelFunction = self.rankItemLabelFunc
        self.widget.rankWnd.rankList.itemRenderer = 'GuildCrossScoreTResult_Rank_item'
        self.widget.rankWnd.rankList.dataArray = []

    def onRoundDropIdxChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if itemMc.selectedIndex != -1:
            self.currentRound = itemMc.selectedIndex + 1
            self.refreshInfo(self.groupId)

    def getRoundList(self):
        p = BigWorld.player()
        crossGuildTournament = p.crossGtn.get(self.groupId)
        currRound = crossGuildTournament.circularRoundNum
        roundList = []
        for i in xrange(0, currRound):
            label = gameStrings.MATCH_ROUND % (i + 1)
            roundList.append({'label': label})

        return roundList

    def getCurrRound(self):
        p = BigWorld.player()
        crossGuildTournament = p.crossGtn.get(self.groupId)
        currRound = crossGuildTournament.circularRoundNum
        return currRound

    def matchItemLabelFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        guildInfo0 = itemData.guildInfo0
        guildInfo1 = itemData.guildInfo1
        itemMc.host0.text = guildInfo0.serverName
        itemMc.host1.text = guildInfo1.serverName
        itemMc.guild0.htmlText = guildInfo0.guildName
        itemMc.guild1.htmlText = guildInfo1.guildName
        itemMc.win0.visible = False
        itemMc.win1.visible = False
        if itemData.winner == 1:
            itemMc.win0.visible = True
        elif itemData.winner == 2:
            itemMc.win1.visible = True
        itemMc.playBtn.visible = itemData.canOb
        itemMc.playBtn.data = guildInfo0.guildNUID
        itemMc.playBtn.addEventListener(events.BUTTON_CLICK, self.onPlayBtnClick)

    def rankItemLabelFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        rank = itemData.rank
        if rank <= 2:
            itemMc.rankIcon.visible = True
            itemMc.rankIcon.gotoAndStop('rank%d' % (rank + 1))
            itemMc.rankText.text = ''
        else:
            itemMc.rankIcon.visible = False
            itemMc.rankText.text = rank + 1
        itemMc.guildName.htmlText = itemData.guildName
        itemMc.score.htmlText = itemData.score

    def onRankCloseBtnClick(self, *args):
        self.widget.rankWnd.visible = False

    def onRankBtnClick(self, *args):
        self.widget.rankWnd.visible = not self.widget.rankWnd.visible

    def onPlayBtnClick(self, *args):
        e = ASObject(args[3][0])
        guildNUID = e.currentTarget.data
        guildNUID = int(guildNUID)
        if guildNUID == 0 or self.groupId == 0:
            return
        p = BigWorld.player()
        p.cell.enterCrossWithLive(self.groupId, guildNUID)

    def onQueryCrossGtn(self, groupId):
        if groupId != self.groupId:
            return
        self.currentRound = self.getCurrRound()
        self.refreshInfo(self.groupId)

    def refreshInfo(self, groupId):
        if not self.widget:
            return
        if self.groupId != groupId:
            return
        self.widget.roundDrop.removeEventListener(events.INDEX_CHANGE, self.onRoundDropIdxChange)
        ASUtils.setDropdownMenuData(self.widget.roundDrop, self.getRoundList())
        self.widget.roundDrop.selectedIndex = self.currentRound - 1
        self.widget.roundDrop.addEventListener(events.INDEX_CHANGE, self.onRoundDropIdxChange)
        self.widget.matchList.dataArray = self.getMatchList(self.currentRound)
        self.widget.rankWnd.rankList.dataArray = self.getRankList()

    def getRankList(self):
        p = BigWorld.player()
        guildList = []
        crossGuildTournament = p.crossGtn.get(self.groupId)
        for guildNUID in crossGuildTournament.guild:
            guildInfo = self.createGuildInfo(crossGuildTournament, guildNUID)
            guildList.append(guildInfo)

        guildList.sort(key=lambda x: x['score'], reverse=True)
        for i, guildInfo in enumerate(guildList):
            guildInfo['rank'] = i

        return guildList

    def getMatchList(self, currRound):
        p = BigWorld.player()
        ret = []
        crossGuildTournament = p.crossGtn.get(self.groupId)
        isCurrRound = False
        if currRound == crossGuildTournament.circularRoundNum:
            isCurrRound = True
        roundInfo = crossGuildTournament.circularTroopNUID
        historyInfo = crossGuildTournament.circularMatchResult.get(currRound, {})
        if roundInfo or historyInfo:
            if isCurrRound:
                for NUIDPair in roundInfo:
                    guildNUID0, guildNUID1 = NUIDPair
                    guildInfo0 = self.createGuildInfo(crossGuildTournament, guildNUID0)
                    guildInfo1 = self.createGuildInfo(crossGuildTournament, guildNUID1)
                    winner = 0
                    matchItem = {'guildInfo0': guildInfo0,
                     'guildInfo1': guildInfo1,
                     'canOb': self.getLiveBtnVisible(crossGuildTournament, currRound),
                     'winner': winner}
                    ret.append(matchItem)

            for NUIDPair in historyInfo:
                guildNUID0, guildNUID1 = NUIDPair
                guildInfo0 = self.createGuildInfo(crossGuildTournament, guildNUID0)
                guildInfo1 = self.createGuildInfo(crossGuildTournament, guildNUID1)
                matchInfo = historyInfo[NUIDPair]
                winner = 1 if matchInfo[0] > matchInfo[1] else 2
                if matchInfo[0] == matchInfo[1]:
                    winner = 0
                matchItem = {'guildInfo0': guildInfo0,
                 'guildInfo1': guildInfo1,
                 'canOb': False,
                 'winner': winner}
                ret.append(matchItem)

        return ret

    def getLiveBtnVisible(self, crossGuildTournament, currRound):
        if currRound != crossGuildTournament.circularRoundNum:
            return 0
        else:
            p = BigWorld.player()
            if p.gtnLiveType == gametypes.BATTLE_FIELD_DOMAIN_CROSS_GTN and crossGuildTournament.state == gametypes.CROSS_GTN_STATE_CIRCULAR_MATCH:
                return 1
            return 0

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
            info['score'] = guildInfo.circularScore
            info['guildNUID'] = guildNUID
        return info
