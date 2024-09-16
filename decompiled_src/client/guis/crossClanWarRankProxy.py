#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/crossClanWarRankProxy.o
import BigWorld
import utils
import gameconfigCommon
from gamestrings import gameStrings
import const
import gametypes
from guis.asObject import ASObject
import uiConst
import events
from guis.asObject import TipManager
from uiProxy import UIProxy
from data import region_server_config_data as RSCD
from data import cross_clan_war_config_data as CCWCD
GUILD_RANK = 0
MY_RANK = 1
MY_RANK_DAMAGE = 2
MY_RANK_CURE = 3
GUILD_SCORE_RANK = 11
PLAYER_KILL_TAB_IDX = 12
PLAYER_DAMAGE_TAB_IDX = 13
PLAYER_CURE_TAB_IDX = 14
GUILD_KILL_RANK = 15

class CrossClanWarRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CrossClanWarRankProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CROSS_CLAN_WAR_RANK, self.hide)

    def reset(self):
        self.myRankIndex = GUILD_RANK

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CROSS_CLAN_WAR_RANK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CROSS_CLAN_WAR_RANK)

    def show(self, targetHostId = None):
        if not targetHostId:
            targetHostId = utils.getHostId()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CROSS_CLAN_WAR_RANK)
            BigWorld.player().cell.getClanWarPlayerRank()
            BigWorld.player().cell.getClanWarGuildRank()
            BigWorld.player().cell.getClanWarGuildRecordScoreRank()
            BigWorld.player().cell.getClanWarPlayerInfo(targetHostId)
            BigWorld.player().cell.getGuildZaijuUsedList(0)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.mainMc.clanRankBtn.addEventListener(events.BUTTON_CLICK, self.handleShowClanRank, False, 0, True)
        self.widget.mainMc.clanRankKillBtn.addEventListener(events.BUTTON_CLICK, self.handleShowClanKillRank, False, 0, True)
        self.widget.mainMc.myRankBtn.addEventListener(events.BUTTON_CLICK, self.handleShowPlayerRank, False, 0, True)
        self.widget.mainMc.myDamageRankBtn.addEventListener(events.BUTTON_CLICK, self.handleShowPlayerRank, False, 0, True)
        self.widget.mainMc.myCureRankBtn.addEventListener(events.BUTTON_CLICK, self.handleShowPlayerRank, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        if self.myRankIndex == GUILD_RANK:
            self.handleShowClanRank()
        elif self.myRankIndex == MY_RANK:
            self.handleShowPlayerRank('myRankBtn')
        elif self.myRankIndex == MY_RANK_DAMAGE:
            self.handleShowPlayerRank('myDamageRankBtn')
        else:
            self.myRankIndex = MY_RANK_CURE
            self.handleShowPlayerRank('myCureRankBtn')

    def handleShowClanKillRank(self, *args):
        self.widget.mainMc.rank.gotoAndStop('clanRank')
        self.widget.mainMc.rank.rankCanvas.txtScoreName.text = gameStrings.CROSS_CLAN_WAR_KILL_CNT
        self.widget.mainMc.rank.rankCanvas.rankList.itemRenderer = 'CrossClanWarRank_ClanRankItem'
        self.widget.mainMc.rank.rankCanvas.rankList.lableFunction = self.clanRankLabelFunction
        self.widget.mainMc.rank.rankCanvas.rankList.itemHeight = 56
        self.widget.mainMc.rank.rankCanvas.myClanRank.visible = False
        self.widget.mainMc.myRankBtn.selected = False
        self.widget.mainMc.myRankBtn.selected = False
        self.widget.mainMc.myDamageRankBtn.selected = False
        self.widget.mainMc.myCureRankBtn.selected = False
        self.widget.mainMc.clanRankBtn.selected = False
        self.widget.mainMc.clanRankKillBtn.selected = True
        self.myRankIndex = GUILD_KILL_RANK
        self.refreshClanWarGuildRank()

    def handleShowClanRank(self, *args):
        self.widget.mainMc.rank.gotoAndStop('clanRank')
        self.myRankIndex = GUILD_SCORE_RANK
        self.widget.mainMc.rank.rankCanvas.txtScoreName.text = gameStrings.CROSS_CLAN_WAR_RECORD_SCORE
        self.widget.mainMc.rank.rankCanvas.rankList.itemRenderer = 'CrossClanWarRank_ClanRankItem'
        self.widget.mainMc.rank.rankCanvas.rankList.lableFunction = self.clanRankLabelFunction
        self.widget.mainMc.rank.rankCanvas.rankList.itemHeight = 56
        self.widget.mainMc.rank.rankCanvas.myClanRank.visible = False
        self.widget.mainMc.myRankBtn.selected = False
        self.widget.mainMc.myDamageRankBtn.selected = False
        self.widget.mainMc.myCureRankBtn.selected = False
        self.widget.mainMc.clanRankKillBtn.selected = False
        self.widget.mainMc.clanRankBtn.selected = True
        self.widget.mainMc.clanRankKillBtn.selected = False
        self.refreshClanWarGuildRank()

    def handleShowPlayerRank(self, *args):
        self.widget.mainMc.clanRankBtn.selected = False
        self.widget.mainMc.myRankBtn.selected = False
        self.widget.mainMc.myDamageRankBtn.selected = False
        self.widget.mainMc.myCureRankBtn.selected = False
        self.widget.mainMc.clanRankKillBtn.selected = False
        if len(args) == 1:
            targetName = args[0]
        else:
            event = ASObject(args[3][0])
            targetName = event.currentTarget.name
        if targetName == 'myRankBtn':
            self.widget.mainMc.rank.gotoAndStop('myRank')
            self.myRankIndex = MY_RANK
            self.widget.mainMc.myRankBtn.selected = True
        elif targetName == 'myDamageRankBtn':
            self.widget.mainMc.rank.gotoAndStop('myDamageRank')
            self.myRankIndex = MY_RANK_DAMAGE
            self.widget.mainMc.myDamageRankBtn.selected = True
        elif targetName == 'myCureRankBtn':
            self.widget.mainMc.rank.gotoAndStop('myCureRank')
            self.myRankIndex = MY_RANK_CURE
            self.widget.mainMc.myCureRankBtn.selected = True
        self.widget.mainMc.rank.rankCanvas.myRank.visible = False
        self.widget.mainMc.rank.rankCanvas.rankList.itemRenderer = 'CrossClanWarRank_PlayerRankItem'
        self.widget.mainMc.rank.rankCanvas.rankList.lableFunction = self.playerRankLabelFunction
        self.widget.mainMc.rank.rankCanvas.rankList.itemHeight = 26
        self.refreshClanWarPlayerRank()

    def _addRankToList(self, rankList, maxNum):

        def mapFun(rankData, index, maxNum):
            if index <= maxNum:
                return list(rankData) + [index]
            else:
                return list(rankData) + [gameStrings.CROSS_CLAN_WAR_NOT_IN_RANK]

        result = map(mapFun, rankList, [ x + 1 for x in xrange(len(rankList)) ], [maxNum] * len(rankList))
        for info in result:
            if self.myRankIndex == GUILD_KILL_RANK:
                info[5] = RSCD.data.get(info[6], {}).get('serverName', '')
            else:
                info[5] = RSCD.data.get(info[5], {}).get('serverName', '')

        return result

    def testClanWarGuildData(self):
        clanWarGuildRank = []
        clanWarGuildRank.append(('guild1', 1, 10, 10006))
        clanWarGuildRank.append(('guild5', 2, 50, 10006))
        clanWarGuildRank.append(('guild3', 3, 30, 10006))
        clanWarGuildRank.append(('guild4', 4, 40, 10006))
        clanWarGuildRank.append(('guild2', 5, 20, 10006))
        BigWorld.player().crossClanWarRecordRank = clanWarGuildRank
        self.refreshClanWarGuildRank()

    def getClanWarGuildRankData(self):
        clanWarGuildRank = {}
        p = BigWorld.player()
        if self.myRankIndex == GUILD_SCORE_RANK:
            rankData = getattr(p, 'crossClanWarRecordRank', [])
            rankData.sort(cmp=lambda x, y: cmp((y[2], y[4]), (x[2], x[4])))
            rankData = self._addRankToList(rankData, const.TOP_CLAN_NUM)
        else:
            rankData = getattr(p, 'clanWarGuildRank', [])
            rankData.sort(cmp=lambda x, y: cmp(y[5], x[5]))
            rankData = self._addRankToList(rankData, const.TOP_CLAN_NUM)
        if len(rankData) > const.TOP_CLAN_NUM:
            clanWarGuildRank = {'allRank': rankData[0:const.TOP_CLAN_NUM],
             'selfRank': rankData[const.TOP_CLAN_NUM],
             ' myClanRankNum': gameStrings.CROSS_CLAN_WAR_NOT_IN_RANK}
        else:
            clanWarGuildRank = {'allRank': rankData,
             'myClanRankNum': gameStrings.CROSS_CLAN_WAR_NOT_IN_RANK}
            myGuildName = BigWorld.player().guildName
            if myGuildName:
                for index, item in enumerate(rankData):
                    if item and myGuildName == item[0]:
                        clanWarGuildRank['selfRank'] = item
                        clanWarGuildRank['myClanRankNum'] = str(index + 1)
                        break

        return clanWarGuildRank

    def refreshClanWarGuildRank(self):
        if not self.widget:
            return
        rankData = self.getClanWarGuildRankData()
        if self.widget.mainMc.rank.currentLabel == 'clanRank':
            self.widget.mainMc.rank.rankCanvas.rankList.dataArray = rankData['allRank']
            if rankData.has_key('selfRank'):
                self.widget.mainMc.rank.rankCanvas.myClanRank.visible = True
                self.doClanRankLabelFunction(rankData['selfRank'], self.widget.mainMc.rank.rankCanvas.myClanRank)
            else:
                self.widget.mainMc.rank.rankCanvas.myClanRank.visible = False

    def testClanWarPlayerRankData(self):
        clanWarPlayerRank = []
        clanWarPlayerRank.append(('role5', 5, 55, 555, 5, 5, 'guile5'))
        clanWarPlayerRank.append(('role1', 1, 11, 111, 1, 1, 'guile1'))
        clanWarPlayerRank.append(('role3', 3, 33, 333, 3, 3, 'guile3'))
        clanWarPlayerRank.append((BigWorld.player().roleName,
         2,
         22,
         222,
         2,
         2,
         'guile2'))
        clanWarPlayerRank.append(('role5', 4, 44, 444, 4, 4, 'guile4'))
        BigWorld.player().clanWarPlayerRank = clanWarPlayerRank
        self.refreshClanWarPlayerRank()

    def getClanWarPlayerRankData(self):
        playerRankData = {}
        p = BigWorld.player()
        rankData = getattr(p, 'clanWarPlayerRank', {}).get(self.myRankIndex, [])
        if self.myRankIndex == MY_RANK:
            rankData.sort(cmp=lambda x, y: cmp(y[1], x[1]))
        elif self.myRankIndex == MY_RANK_DAMAGE:
            rankData.sort(cmp=lambda x, y: cmp(y[3], x[3]))
        elif self.myRankIndex == MY_RANK_CURE:
            rankData.sort(cmp=lambda x, y: cmp(y[4], x[4]))
        rankData = self._addRankToList(rankData, const.TOP_CLAN_MEMBER_NUM)
        if len(rankData) > const.TOP_CLAN_MEMBER_NUM:
            playerRankData = {'allRank': rankData[0:const.TOP_CLAN_MEMBER_NUM]}
        else:
            playerRankData = {'allRank': rankData}
        myRoleName = BigWorld.player().realRoleName
        for item in rankData:
            if myRoleName == item[0]:
                playerRankData['selfRank'] = item
                break

        return playerRankData

    def refreshClanWarPlayerRank(self):
        rankData = self.getClanWarPlayerRankData()
        if self.widget.mainMc.rank.currentLabel == 'myRank' or self.widget.mainMc.rank.currentLabel == 'myCureRank' or self.widget.mainMc.rank.currentLabel == 'myDamageRank':
            self.widget.mainMc.rank.rankCanvas.rankList.dataArray = rankData['allRank']
            if rankData.has_key('selfRank'):
                self.widget.mainMc.rank.rankCanvas.myRank.visible = True
                self.doPlayerRankLabelFunction(rankData['selfRank'], self.widget.mainMc.rank.rankCanvas.myRank)
            else:
                self.widget.mainMc.rank.rankCanvas.myRank.visible = False

    def clanRankLabelFunction(self, *args):
        obj = ASObject(args[3][0])
        item = ASObject(args[3][1])
        self.doClanRankLabelFunction(obj, item)

    def processScore(self, score):
        score = int(score)
        try:
            if score > 10000:
                return gameStrings.CROSS_CLAN_WAR_SCORE % (score * 1.0 / 10000)
            return str(score)
        except Exception as e:
            msg = 'jbx:processScore Error %s' % str(score)
            BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})

    def doClanRankLabelFunction(self, obj, item):
        item.rankTxt.playerName.text = obj[0]
        item.rankTxt.playerNum.text = obj[1]
        item.rankTxt.killEnemy.text = self.processScore(obj[2])
        item.rankTxt.bonusSlot.visible = False
        if self.myRankIndex == GUILD_SCORE_RANK:
            item.rankTxt.score.text = obj[5]
            TipManager.addTip(item.rankTxt.killEnemy, CCWCD.data.get('crossClanWarScoreTips', 'crossClanWarScoreTips') % (obj[3], obj[2] - obj[3]))
        else:
            item.rankTxt.score.text = obj[5]
        if type(obj) != list:
            item.rankTxt.rank.text = obj[obj.length - 1]
        else:
            item.rankTxt.rank.text = obj[-1]

    def playerRankLabelFunction(self, *args):
        obj = ASObject(args[3][0])
        item = ASObject(args[3][1])
        self.doPlayerRankLabelFunction(obj, item)

    def doPlayerRankLabelFunction(self, obj, item):
        item.rankTxt.playerName.text = obj[0]
        if self.myRankIndex == MY_RANK:
            item.rankTxt.score.text = self.processScore(obj[1])
        elif self.myRankIndex == MY_RANK_DAMAGE:
            item.rankTxt.score.text = self.processScore(obj[3])
        elif self.myRankIndex == MY_RANK_CURE:
            item.rankTxt.score.text = self.processScore(obj[4])
        item.rankTxt.clan.text = obj[6]
        if type(obj) != list:
            rank = int(obj[obj.length - 1])
        else:
            rank = obj[-1]
        item.rankTxt.rank.text = rank
