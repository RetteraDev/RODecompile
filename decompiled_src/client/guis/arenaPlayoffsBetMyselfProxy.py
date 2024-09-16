#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaPlayoffsBetMyselfProxy.o
from gamestrings import gameStrings
import BigWorld
import uiUtils
import tipUtils
import gametypes
import ui
import const
import time
import copy
import uiConst
import gameglobal
from callbackHelper import Functor
from uiProxy import UIProxy
from asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import duel_config_data as DCD
from data import arena_playoffs_bet_time_data as APBTD
from data import arena_playoffs_5v5_bet_time_data as AP5BTD

class ArenaPlayoffsBetMyselfProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaPlayoffsBetMyselfProxy, self).__init__(uiAdapter)
        self.widget = None
        self.betList = []

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.queryInfo()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None

    def initUI(self):
        self.widget.mainMc.scrollWndList.itemRenderer = 'ArenaPlayoffsBetMyself_ScrollWndItem'
        self.widget.mainMc.scrollWndList.lableFunction = self.itemFunction
        self.widget.mainMc.scrollWndList.itemHeight = 24
        self.widget.mainMc.totalAmountIcon.bonusType = 'wudao'
        self.widget.mainMc.totalGainAmountIcon.bonusType = 'wudao'
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_ARENA_PLAYOFFS_BET)

    def queryInfo(self):
        p = BigWorld.player()
        time = 0
        for lvKey in gametypes.CROSS_ARENA_PLAYOFFS_LV_KEYS:
            version = self.uiAdapter.arenaPlayoffsBet.teamsDict.get(lvKey, {}).get('version', 0)
            BigWorld.callback(time, Functor(p.cell.queryArenaPlayoffsTeamsOfLvKey, version, lvKey))
            time += 1.2

        version = self.uiAdapter.arenaPlayoffsBet.myBetDict.get('version', 0)
        p.cell.queryMyArenaPlayoffsBet(version)

    def refreshTotalAmountInfo(self):
        self.widget.mainMc.totalAmount.text = format(BigWorld.player().getFame(const.ARENA_PLAYOFFS_BET_FAME_ID), ',')

    @ui.callInCD(0.5)
    def refreshInfoInCD(self):
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.mainMc.betLimit.text = gameStrings.TEXT_ARENAPLAYOFFSBETMYSELFPROXY_74 % (p.arenaPlayoffsBetCnt, DCD.data.get('ARENA_PLAYOFFS_BET_CNT_LIMIT', 0))
        myBetDictInfo = self.uiAdapter.arenaPlayoffsBet.myBetDict.get('info', {})
        totalGainAmount = 0
        self.betList = []
        for key, myBetDictDetail in myBetDictInfo.iteritems():
            myBetList = myBetDictDetail.get('itemList', [])
            newFlagVisible = self.uiAdapter.arenaPlayoffsBet.newReawrdDict.get(key, False)
            for i, myBetItem in enumerate(myBetList):
                lvKey = key[0]
                betKey = (key[1], key[2])
                betInfo = {}
                betInfo['idx'] = i
                betInfo['key'] = key
                apbtData = APBTD.data.get(betKey, {})
                if gameglobal.rds.ui.arenaPlayoffsBet.isArena5v5:
                    apbtData = AP5BTD.data.get(betKey, {})
                betInfo['content'] = gameStrings.TEXT_ARENAPLAYOFFSBETMYSELFPROXY_93 % (lvKey.replace('_', '-'), apbtData.get('descName', ''), i + 1)
                betInfo['betAmount'] = format(myBetItem.get('cash', 0), ',')
                status = myBetItem.get('status', 0)
                if status in (gametypes.ARENA_PLAYOFFS_BET_STATUS_SUCC, gametypes.ARENA_PLAYOFFS_BET_STATUS_REWARDED):
                    betInfo['state'] = uiUtils.toHtml(gameStrings.TEXT_ARENAPLAYOFFSBETMYSELFPROXY_98, color='#E59545')
                    rewardCash = myBetItem.get('rewardCash', 0)
                    betInfo['rewardAmount'] = format(rewardCash, ',')
                    betInfo['rewardAmountIconVisible'] = True
                    betInfo['newFlagVisible'] = newFlagVisible
                    totalGainAmount += rewardCash
                elif status == gametypes.ARENA_PLAYOFFS_BET_STATUS_FAILED:
                    betInfo['state'] = gameStrings.TEXT_ARENAPLAYOFFSBETMYSELFPROXY_106
                    betInfo['rewardAmount'] = '     -'
                    betInfo['rewardAmountIconVisible'] = False
                    betInfo['newFlagVisible'] = False
                else:
                    betInfo['state'] = gameStrings.TEXT_ARENAPLAYOFFSBETMYSELFPROXY_112
                    betInfo['rewardAmount'] = '     -'
                    betInfo['rewardAmountIconVisible'] = False
                    betInfo['newFlagVisible'] = False
                self.betList.append(betInfo)

        for i, betInfo in enumerate(self.betList):
            betInfo['bg'] = 'light' if i % 2 else 'dark'

        self.widget.mainMc.scrollWndList.dataArray = self.betList
        self.widget.mainMc.totalGainAmount.text = format(totalGainAmount, ',')
        self.refreshTotalAmountInfo()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        ASUtils.setMcData(itemMc, 'data', itemData)
        self.updateItem(itemMc)

    def updateItem(self, itemMc):
        if not itemMc:
            return
        itemMc.content.text = itemMc.data.content
        itemMc.betAmount.text = itemMc.data.betAmount
        itemMc.rewardAmount.text = itemMc.data.rewardAmount
        itemMc.state.htmlText = itemMc.data.state
        itemMc.newFlag.visible = itemMc.data.newFlagVisible
        itemMc.betAmountIcon.bonusType = 'wudao'
        itemMc.betAmountIcon.validateNow()
        itemMc.rewardAmountIcon.visible = itemMc.data.rewardAmountIconVisible
        if itemMc.data.rewardAmountIconVisible:
            itemMc.rewardAmountIcon.bonusType = 'wudao'
            itemMc.rewardAmountIcon.validateNow()
        bType = int(itemMc.data.key[1])
        typeArg = (itemMc.data.key[0],
         itemMc.data.key[1],
         itemMc.data.key[2],
         itemMc.data.idx)
        if bType == gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL:
            TipManager.addTipByType(itemMc, tipUtils.TYPE_ARENA_PLAYOFFS_BET_TOP4, typeArg, False, 'bottomCenter')
        elif bType == gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL:
            TipManager.addTipByType(itemMc, tipUtils.TYPE_ARENA_PLAYOFFS_BET_DAY, typeArg, False, 'bottomCenter')
        itemMc.bg.gotoAndStop(itemMc.data.bg)

    def getTop4Tip(self, lvKey, bType, betId, idx):
        self.queryTipsInfo(lvKey, bType, betId, idx)
        myBetList = self.uiAdapter.arenaPlayoffsBet.myBetDict.get('info', {}).get((lvKey, bType, betId), {}).get('itemList', [])
        if idx >= len(myBetList):
            return
        teamsInfo = self.uiAdapter.arenaPlayoffsBet.teamsDict.get(lvKey, {}).get('info', {})
        myBetItem = myBetList[idx]
        status = myBetItem.get('status', 0)
        teamNUIDs = copy.deepcopy(myBetItem.get('val', []))
        teamNUIDs.reverse()
        resultList = copy.deepcopy(self.uiAdapter.arenaPlayoffsBet.tipResultDict.get((lvKey,
         bType,
         betId,
         idx), []))
        resultList.reverse()
        info = {}
        teamList = []
        for i in xrange(4):
            teamInfo = {}
            teamInfo['goldFlagVisible'] = True if i == 0 else False
            if i == 0:
                teamInfo['rankName'] = gameStrings.TEXT_DUELUTILS_406
            elif i == 1:
                teamInfo['rankName'] = gameStrings.TEXT_ARENAPLAYOFFSBETMYSELFPROXY_186
            else:
                teamInfo['rankName'] = gameStrings.TEXT_ARENAPLAYOFFSBETMYSELFPROXY_188
            teamNUID = 0 if i >= len(teamNUIDs) else teamNUIDs[i]
            teamInfo['teamName'] = teamsInfo.get(teamNUID, {}).get('teamName', '')
            if status in (gametypes.ARENA_PLAYOFFS_BET_STATUS_SUCC, gametypes.ARENA_PLAYOFFS_BET_STATUS_REWARDED):
                teamInfo['betFlag'] = 'win'
            elif i >= len(resultList):
                teamInfo['betFlag'] = 'empty'
            else:
                teamInfo['betFlag'] = 'win' if resultList[i] else 'lose'
            teamList.append(teamInfo)

        info['teamList'] = teamList
        info['betTime'] = gameStrings.TEXT_ARENAPLAYOFFSBETMYSELFPROXY_200 % time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(myBetItem.get('tWhen', 0)))
        return uiUtils.dict2GfxDict(info, True)

    def getDayTip(self, lvKey, bType, betId, idx):
        self.queryTipsInfo(lvKey, bType, betId, idx)
        myBetDictDetail = self.uiAdapter.arenaPlayoffsBet.myBetDict.get('info', {}).get((lvKey, bType, betId), {})
        myBetList = myBetDictDetail.get('itemList', [])
        if idx >= len(myBetList):
            return
        teamsInfo = self.uiAdapter.arenaPlayoffsBet.teamsDict.get(lvKey, {}).get('info', {})
        candidateList = myBetDictDetail.get('candidate', [])
        myBetItem = myBetList[idx]
        status = myBetItem.get('status', 0)
        scoreList = myBetItem.get('val', [])
        scoreLen = min(len(scoreList), len(candidateList))
        resultList = self.uiAdapter.arenaPlayoffsBet.tipResultDict.get((lvKey,
         bType,
         betId,
         idx), [])
        info = {}
        teamList = []
        for i in xrange(scoreLen):
            teamInfo = {}
            teamInfo['teamName0'] = teamsInfo.get(candidateList[i][0], {}).get('teamName', '')
            teamInfo['teamName1'] = teamsInfo.get(candidateList[i][1], {}).get('teamName', '')
            teamInfo['score'] = 'blue' if scoreList[i][0] > scoreList[i][1] else 'red'
            if status in (gametypes.ARENA_PLAYOFFS_BET_STATUS_SUCC, gametypes.ARENA_PLAYOFFS_BET_STATUS_REWARDED):
                teamInfo['betFlag'] = 'win'
            elif i >= len(resultList):
                teamInfo['betFlag'] = 'empty'
            else:
                teamInfo['betFlag'] = 'win' if resultList[i] else 'lose'
            teamList.append(teamInfo)

        info['teamList'] = teamList
        info['betTime'] = gameStrings.TEXT_ARENAPLAYOFFSBETMYSELFPROXY_200 % time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(myBetItem.get('tWhen', 0)))
        return uiUtils.dict2GfxDict(info, True)

    def queryTipsInfo(self, lvKey, bType, betId, idx):
        myBetDictDetail = self.uiAdapter.arenaPlayoffsBet.myBetDict.get('info', {}).get((lvKey, bType, betId), {})
        myBetList = myBetDictDetail.get('itemList', [])
        if idx >= len(myBetList):
            return
        myBetItem = myBetList[idx]
        status = myBetItem.get('status', 0)
        if status != gametypes.ARENA_PLAYOFFS_BET_STATUS_FAILED:
            return
        if self.uiAdapter.arenaPlayoffsBet.tipResultDict.has_key((lvKey,
         bType,
         betId,
         idx)):
            return
        p = BigWorld.player()
        if bType == gametypes.ARENA_PLAYOFFS_BET_TYPE_FINAL:
            teamNUIDs = myBetItem.get('val', [])
            p.cell.queryArenaPlayoffsFinalBetResult(betId, lvKey, bType, teamNUIDs, idx)
        elif bType == gametypes.ARENA_PLAYOFFS_BET_TYPE_DUEL:
            candidateList = myBetDictDetail.get('candidate', [])
            scoreList = myBetItem.get('val', [])
            team1NUIDs = [ candidate[0] for candidate in candidateList ]
            team2NUIDs = [ candidate[1] for candidate in candidateList ]
            scoreList1 = [ score[0] for score in scoreList ]
            scoreList2 = [ score[1] for score in scoreList ]
            p.cell.queryArenaPlayoffsDailyBetResult(betId, lvKey, bType, team1NUIDs, team2NUIDs, scoreList1, scoreList2, idx)
