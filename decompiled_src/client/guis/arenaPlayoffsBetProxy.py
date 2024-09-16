#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaPlayoffsBetProxy.o
import BigWorld
import gameglobal
import uiConst
from callbackHelper import Functor
from uiTabProxy import UITabProxy

class ArenaPlayoffsBetProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(ArenaPlayoffsBetProxy, self).__init__(uiAdapter)
        self.betIdDict = {}
        self.teamsDict = {}
        self.betResultDict = {}
        self.finalDuelResultDict = {}
        self.candidateDict = {}
        self.betFailedCashDict = {}
        self.myBetDict = {}
        self.tipResultDict = {}
        self.newReawrdDict = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENA_PLAYOFFS_BET, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ARENA_PLAYOFFS_BET:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)

    def clearWidget(self):
        super(ArenaPlayoffsBetProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENA_PLAYOFFS_BET)

    def reset(self):
        super(ArenaPlayoffsBetProxy, self).reset()
        self.uiAdapter.arenaPlayoffsBetTop4.reset()
        self.uiAdapter.arenaPlayoffsBetDay.reset()
        if not self.uiAdapter.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_PUSH_ARENA_PLAYOFFS_BET):
            self.newReawrdDict = {}

    def clearAll(self):
        self.myBetDict = {}
        self.tipResultDict = {}
        self.newReawrdDict = {}
        self.uiAdapter.arenaPlayoffsBetTop4.clearAll()
        self.uiAdapter.arenaPlayoffsBetDay.clearAll()

    def getArenaPlayoffsBetDayInfo(self):
        if gameglobal.rds.configData.get('enablePlayoffsBetDayNew', False):
            return {'tabIdx': uiConst.ARENA_PLAYOFFS_BET_TAB_DAY,
             'tabName': 'dayBtn',
             'view': 'ArenaPlayoffsBetDayNewWidget',
             'proxy': 'arenaPlayoffsBetDayNew'}
        else:
            return {'tabIdx': uiConst.ARENA_PLAYOFFS_BET_TAB_DAY,
             'tabName': 'dayBtn',
             'view': 'ArenaPlayoffsBetDayWidget',
             'proxy': 'arenaPlayoffsBetDay'}

    def _getTabList(self):
        return [{'tabIdx': uiConst.ARENA_PLAYOFFS_BET_TAB_TOP4,
          'tabName': 'top4Btn',
          'view': 'ArenaPlayoffsBetTop4Widget',
          'proxy': 'arenaPlayoffsBetTop4'},
         self.getArenaPlayoffsBetDayInfo(),
         {'tabIdx': uiConst.ARENA_PLAYOFFS_BET_TAB_PEAK,
          'tabName': 'peakBtn',
          'view': 'ArenaPlayoffsBetPeakWidget',
          'proxy': 'arenaPlayoffsBetPeak'},
         {'tabIdx': uiConst.ARENA_PLAYOFFS_BET_TAB_MYSELF,
          'tabName': 'myselfBtn',
          'view': 'ArenaPlayoffsBetMyselfWidget',
          'proxy': 'arenaPlayoffsBetMyself'}]

    def show(self, showTabIndex):
        if not gameglobal.rds.configData.get('enableArenaPlayoffsBet', False):
            return
        self.showTabIndex = showTabIndex
        if self.widget:
            self.widget.setTabIndex(self.showTabIndex)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENA_PLAYOFFS_BET)

    @property
    def isArenaScore(self):
        p = BigWorld.player()
        return p.isBalancePlayoffs()

    @property
    def isArena5v5(self):
        p = BigWorld.player()
        return p.isPlayoffs5V5()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()

    def refreshInfo(self):
        if not self.widget:
            return
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    def refreshTotalAmountInfo(self):
        if not self.widget:
            return
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshTotalAmountInfo'):
            proxy.refreshTotalAmountInfo()

    def initBetIdDict(self, betIdDict):
        self.betIdDict = betIdDict

    def updateBetIdDict(self, lvKey, info):
        self.betIdDict[lvKey] = info
        if self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_TOP4:
            self.uiAdapter.arenaPlayoffsBetTop4.refreshInfoInCD(lvKey)
        elif self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_DAY:
            self.uiAdapter.arenaPlayoffsBetDay.refreshInfoInCD(lvKey)

    def updateTeams(self, lvKey, version, info):
        self.teamsDict[lvKey] = {'version': version,
         'info': info}
        if self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_TOP4:
            self.uiAdapter.arenaPlayoffsBetTop4.refreshInfoInCD(lvKey)
        elif self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_DAY:
            self.uiAdapter.arenaPlayoffsBetDay.refreshInfoInCD(lvKey)
        elif self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_MYSELF:
            self.uiAdapter.arenaPlayoffsBetMyself.refreshInfoInCD()

    def updateBetResult(self, lvKey, bType, betId, betDuelInfo, lastSeasonRestCash):
        if not self.betResultDict.has_key(lvKey):
            self.betResultDict[lvKey] = {}
        self.betResultDict[lvKey][bType, betId] = {'betDuelInfo': betDuelInfo,
         'lastSeasonRestCash': lastSeasonRestCash}
        if self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_TOP4:
            self.uiAdapter.arenaPlayoffsBetTop4.refreshBetInfo(lvKey)
        elif self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_DAY:
            self.uiAdapter.arenaPlayoffsBetDay.refreshBetInfo(lvKey)

    def updateFinalDuelResult(self, lvKey, info):
        teamList = info.get('data', {}).get(1, [])
        if not teamList:
            return
        result = []
        for team0, team1 in teamList:
            result.append(team0.get('nuid', 0))
            result.append(team1.get('nuid', 0))

        result.sort()
        if self.finalDuelResultDict.get(lvKey, []) == result:
            return
        self.finalDuelResultDict[lvKey] = result
        self.uiAdapter.arenaPlayoffsBetTop4.reset()
        self.uiAdapter.arenaPlayoffsBetTop4.clearAll()
        if self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_TOP4:
            self.uiAdapter.arenaPlayoffsBetTop4.refreshInfoInCD(lvKey)

    def updateCandidate(self, lvKey, bType, betId, betDuelInfo):
        if not self.candidateDict.has_key(lvKey):
            self.candidateDict[lvKey] = {}
        self.candidateDict[lvKey][bType, betId] = betDuelInfo
        if self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_DAY:
            self.uiAdapter.arenaPlayoffsBetDay.refreshInfoInCD(lvKey)

    def updateBetFailedCash(self, version, lastSeasonRestCashInfo, betFailedAccumulateCashInfo, lastDuelRestCashDict):
        self.betFailedCashDict = {'version': version,
         'lastSeasonRestCashInfo': lastSeasonRestCashInfo,
         'betFailedAccumulateCashInfo': betFailedAccumulateCashInfo,
         'lastDuelRestCashDict': lastDuelRestCashDict}
        if self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_TOP4:
            self.uiAdapter.arenaPlayoffsBetTop4.refreshBetInfo()
        elif self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_DAY:
            self.uiAdapter.arenaPlayoffsBetDay.refreshBetInfo()
        elif self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_PEAK:
            self.uiAdapter.arenaPlayoffsBetPeak.refreshInfoInCD()

    def updateMyBet(self, version, info):
        self.myBetDict = {'version': version,
         'info': info}
        if self.currentTabIndex == uiConst.ARENA_PLAYOFFS_BET_TAB_MYSELF:
            self.uiAdapter.arenaPlayoffsBetMyself.refreshInfoInCD()

    def updateTipResultDict(self, lvKey, bType, betId, idx, resultList):
        self.tipResultDict[lvKey, bType, betId, idx] = resultList

    def notifyBetRewardPushMsg(self, lvKey, bType, betId):
        self.newReawrdDict[lvKey, bType, betId] = True
        callBackDict = {'click': Functor(self.show, uiConst.ARENA_PLAYOFFS_BET_TAB_MYSELF)}
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_ARENA_PLAYOFFS_BET, callBackDict)
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_ARENA_PLAYOFFS_BET)

    def notifyBetStartPushMsg(self):
        if not gameglobal.rds.configData.get('enableArenaPlayoffsBet', False):
            return
        if not self.uiAdapter.arenaPlayoffsBetTop4.checkBetStart() and not self.uiAdapter.arenaPlayoffsBetDay.checkBetStart():
            return
        callBackDict = {'click': self.showNowStartTab}
        self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_ARENA_PLAYOFFS_BET_START, callBackDict)
        self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_ARENA_PLAYOFFS_BET_START)

    def showNowStartTab(self):
        if self.uiAdapter.arenaPlayoffsBetTop4.checkBetStart():
            self.show(uiConst.ARENA_PLAYOFFS_BET_TAB_TOP4)
        elif self.uiAdapter.arenaPlayoffsBetDay.checkBetStart():
            self.show(uiConst.ARENA_PLAYOFFS_BET_TAB_DAY)
        else:
            self.show(uiConst.ARENA_PLAYOFFS_BET_TAB_TOP4)
