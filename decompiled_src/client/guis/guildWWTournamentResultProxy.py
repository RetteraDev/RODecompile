#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildWWTournamentResultProxy.o
from gamestrings import gameStrings
import BigWorld
import time
import gameglobal
import uiConst
import gametypes
from guis.asObject import ASObject
from callbackHelper import Functor
from uiProxy import UIProxy
from helpers.guild import getGTNSD
FIRST_TOURNAMENT_PATH = 'widgets/GuildWWZhengfengResultWidget.swf'
SECOND_TOURNAMENT_NORMAL_PATH = 'widgets/GuildWWDuoshuaiResultWidget.swf'
THIRD_TOURNAMENT_PATH = 'widgets/GuildWWFinalResultWidget.swf'
TOURNAMENT_STATE = {'firstBefore': 0,
 'firstRunning': 1,
 'firstToSecond': 2,
 'secondRunning': 3,
 'secondToThird': 4,
 'thirdRunning': 5,
 'thirdEnd': 6}
ARRANGE_ID = 4
FIRST_TOURNAMENT_ID = 5
SECOND_TOURNAMENT_ID = 6
THIRD_TOURNAMENT_ID = 7
FIRST_TAB_INDEX = 0
SECOND_TAB_INDEX = 1
THIRD_TAB_INDEX = 2
TAB_VIEW_MAP = {FIRST_TAB_INDEX: 'guildWWZhengfengResult',
 SECOND_TAB_INDEX: 'guildWWDuoshuaiResult',
 THIRD_TAB_INDEX: 'guildWWFinalResult'}

class GuildWWTournamentResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildWWTournamentResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.refreshStateTimeId = 0
        self.calTimeId = 0
        self.isReadyToShow = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_WW_TOURNAMENT_RESULT, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.refreshGtnState()
        self.widget = widget
        self.state = TOURNAMENT_STATE['firstBefore']
        self.gtnState = TOURNAMENT_STATE['firstBefore']
        self.getConfigTime()
        self.setState()
        self.setGtnState()
        self.initUI()
        self.calTime()

    def calTime(self, once = False):
        if not self.widget:
            return
        p = BigWorld.player()
        oldState = self.state
        self.setState()
        nowState = self.state
        tournamentTime = self.widget.tournamentTime.tournamentTimeT
        if oldState != nowState:
            if self.refreshStateTimeId:
                BigWorld.cancelCallback(self.refreshStateTimeId)
            self.refreshStateTimeId = BigWorld.callback(5, Functor(self.refreshGtnState, True))
        if self.tabIdx == 0:
            if nowState == TOURNAMENT_STATE['firstBefore']:
                timeLeft = self.setLeftTime(self.firstStartTime)
                tournamentTime.text = gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_76 % timeLeft
            elif nowState == TOURNAMENT_STATE['firstRunning']:
                tournamentTime.text = gameStrings.TEXT_GAMETYPES_5171
            else:
                tournamentTime.text = gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_80
        elif self.tabIdx == 1:
            if nowState == TOURNAMENT_STATE['firstToSecond']:
                timeLeft = self.setLeftTime(self.secondStartTime)
                tournamentTime.text = gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_76 % timeLeft
            elif nowState == TOURNAMENT_STATE['secondRunning']:
                tournamentTime.text = gameStrings.TEXT_GAMETYPES_5171
            else:
                tournamentTime.text = gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_80
        elif nowState == TOURNAMENT_STATE['secondToThird']:
            timeLeft = self.setLeftTime(self.thirdStartTime)
            tournamentTime.text = gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_76 % timeLeft
        elif nowState == TOURNAMENT_STATE['thirdRunning']:
            tournamentTime.text = gameStrings.TEXT_GAMETYPES_5171
        else:
            tournamentTime.text = gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_80
        if not once:
            if self.widget:
                if self.calTimeId:
                    BigWorld.cancelCallback(self.calTimeId)
                self.calTimeId = BigWorld.callback(1, self.calTime)

    def setLeftTime(self, deadLine):
        timeLeftStr = ''
        now = self.getLocalTime()
        timeLeft = deadLine - now['totalTime']
        if timeLeft < 0:
            return '0'
        days = timeLeft // 86400
        hours = timeLeft // 3600
        minutes = timeLeft % 3600 // 60
        seconds = timeLeft % 3600 % 60
        if hours >= 24:
            timeLeftStr = gameStrings.TEXT_FASHIONPROPTRANSFERPROXY_229 % days
        elif hours > 2:
            timeLeftStr = gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_116 % hours
        elif hours == 1:
            timeLeftStr = gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_118 % (hours, minutes)
        else:
            timeLeftStr = gameStrings.TEXT_GUILDWWTOURNAMENTRESULTPROXY_120 % (hours, minutes, seconds)
        return timeLeftStr

    def initUI(self):
        p = BigWorld.player()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if p.worldWar.isLucky() or not gameglobal.rds.configData.get('enableWorldWar', False):
            self.widget.tabButtons = [self.widget.firstTournament, self.widget.secondTournament]
            self.widget.tabViewPaths = [FIRST_TOURNAMENT_PATH, SECOND_TOURNAMENT_NORMAL_PATH]
            self.widget.thirdTournament.enabled = False
            self.widget.thirdTournament.visible = False
            self.widget.thirdTournamentHint.visible = False
            self.tabButtonsLen = 2
        else:
            self.widget.tabButtons = [self.widget.firstTournament, self.widget.secondTournament, self.widget.thirdTournament]
            self.widget.tabViewPaths = [FIRST_TOURNAMENT_PATH, SECOND_TOURNAMENT_NORMAL_PATH, THIRD_TOURNAMENT_PATH]
            self.tabButtonsLen = 3
        self.tabHints = [self.widget.firstTournamentHint, self.widget.secondTournamentHint, self.widget.thirdTournamentHint]
        self.widget.onTabChanged = self.onTabChanged
        self.tabIdx = FIRST_TAB_INDEX
        self.refreshTabHint()
        self.setTabBtnByState()
        self.setTabPanelByState()

    def refreshPanel(self):
        if not self.widget:
            return
        self.setGtnState()
        self.setTabBtnByState()
        self.setTabPanelByState()

    def refreshCurrentPanel(self):
        if not self.widget:
            return
        if hasattr(self, 'tabIdx'):
            tabIdx = self.tabIdx
        else:
            tabIdx = FIRST_TAB_INDEX
        currentProxy = self.getTabViewProxy(tabIdx)
        if currentProxy:
            currentProxy.refreshPanel()

    def getLocalTime(self):
        p = BigWorld.player()
        localTime = time.localtime(p.getServerTime())
        now = {}
        now['days'] = int(time.strftime('%w', localTime))
        now['hours'] = int(time.strftime('%H', localTime))
        now['minutes'] = int(time.strftime('%M', localTime))
        now['seconds'] = int(time.strftime('%S', localTime))
        now['totalTime'] = now['days'] * 3600 * 24 + now['hours'] * 3600 + now['minutes'] * 60 + now['seconds']
        return now

    def getConfigTime(self):
        data = getGTNSD().data
        arrangeTime = str.split(data.get(ARRANGE_ID, {}).get('crontab', ''), ' ')
        firstBeginTime = str.split(data.get(FIRST_TOURNAMENT_ID, {}).get('crontab', ''), ' ')
        firstTime = data.get(FIRST_TOURNAMENT_ID, {})
        secondTime = data.get(SECOND_TOURNAMENT_ID, {})
        thirdTime = data.get(THIRD_TOURNAMENT_ID, {})
        self.tournamentDay = int(firstBeginTime[-1]) + 1
        self.arrangeTotalTime = (int(arrangeTime[-1]) + 1) * 24 * 3600 + int(arrangeTime[1]) * 3600 + int(arrangeTime[0]) * 60
        self.firstStartTime = self.getTournamentTime(firstTime.get('startTime', ''))
        self.firstEndTime = self.getTournamentTime(firstTime.get('endTime', ''))
        self.secondStartTime = self.getTournamentTime(secondTime.get('startTime', ''))
        self.secondEndTime = self.getTournamentTime(secondTime.get('endTime', ''))
        self.thirdStartTime = self.getTournamentTime(thirdTime.get('startTime', ''))
        self.thirdEndTime = self.getTournamentTime(thirdTime.get('endTime', ''))

    def getTournamentTime(self, timeStr):
        time = str.split(timeStr, ':')
        hour = int(time[0])
        minutes = int(time[1])
        return self.tournamentDay * 24 * 3600 + hour * 3600 + minutes * 60

    def setState(self):
        now = self.getLocalTime()
        if now['totalTime'] < self.firstStartTime:
            self.state = TOURNAMENT_STATE['firstBefore']
        elif now['totalTime'] >= self.firstStartTime and now['totalTime'] < self.firstEndTime:
            self.state = TOURNAMENT_STATE['firstRunning']
        elif now['totalTime'] < self.secondStartTime and now['totalTime'] >= self.firstEndTime:
            self.state = TOURNAMENT_STATE['firstToSecond']
        elif now['totalTime'] >= self.secondStartTime and now['totalTime'] < self.secondEndTime:
            self.state = TOURNAMENT_STATE['secondRunning']
        elif now['totalTime'] >= self.secondEndTime and now['totalTime'] < self.thirdStartTime:
            self.state = TOURNAMENT_STATE['secondToThird']
        elif now['totalTime'] >= self.thirdStartTime and now['totalTime'] < self.thirdEndTime:
            self.state = TOURNAMENT_STATE['thirdRunning']
        elif now['totalTime'] >= self.thirdEndTime:
            self.state = TOURNAMENT_STATE['thirdEnd']

    def setGtnState(self):
        p = BigWorld.player()
        guildTournament = p.guildTournament.get(self.groupId)
        roundNum = guildTournament.roundNum
        gtnState = guildTournament.state
        self.gtnState = TOURNAMENT_STATE['firstBefore']
        if gtnState == gametypes.GUILD_TOURNAMENT_STATE_READY or gtnState == gametypes.GUILD_TOURNAMENT_STATE_WW_READY or gtnState == gametypes.GUILD_TOURNAMENT_STATE_GROUP:
            if roundNum == 0:
                self.gtnState = TOURNAMENT_STATE['firstBefore']
            elif roundNum == 1:
                self.gtnState = TOURNAMENT_STATE['firstToSecond']
            else:
                self.gtnState = TOURNAMENT_STATE['secondToThird']
        elif gtnState == gametypes.GUILD_TOURNAMENT_STATE_FINISHED:
            self.gtnState = TOURNAMENT_STATE['thirdEnd']
        elif roundNum == 1:
            self.gtnState = TOURNAMENT_STATE['firstRunning']
        elif roundNum == 2:
            self.gtnState = TOURNAMENT_STATE['secondRunning']
        else:
            self.gtnState = TOURNAMENT_STATE['thirdRunning']

    def setTabBtnByState(self):
        if self.gtnState == TOURNAMENT_STATE['firstBefore']:
            self.refreshTabHint()
            self.refreshTabBtnDisable([SECOND_TAB_INDEX, THIRD_TAB_INDEX])
        elif self.gtnState == TOURNAMENT_STATE['firstRunning']:
            self.refreshTabHint()
            self.refreshTabBtnDisable([SECOND_TAB_INDEX, THIRD_TAB_INDEX])
        elif self.gtnState == TOURNAMENT_STATE['firstToSecond']:
            self.refreshTabHint(SECOND_TAB_INDEX)
            self.refreshTabBtnDisable([THIRD_TAB_INDEX])
        elif self.gtnState == TOURNAMENT_STATE['secondRunning']:
            self.refreshTabHint()
            self.refreshTabBtnDisable([THIRD_TAB_INDEX])
        elif self.gtnState == TOURNAMENT_STATE['secondToThird']:
            self.refreshTabHint(THIRD_TAB_INDEX)
            self.refreshTabBtnDisable()
        elif self.gtnState == TOURNAMENT_STATE['thirdRunning']:
            self.refreshTabHint()
            self.refreshTabBtnDisable()

    def setTabPanelByState(self):
        if self.gtnState == TOURNAMENT_STATE['firstBefore'] or self.gtnState == TOURNAMENT_STATE['firstRunning']:
            self.widget.setTabIndex(FIRST_TAB_INDEX)
        elif self.gtnState == TOURNAMENT_STATE['firstToSecond'] or self.gtnState == TOURNAMENT_STATE['secondRunning']:
            self.widget.setTabIndex(SECOND_TAB_INDEX)
        elif self.gtnState == TOURNAMENT_STATE['secondToThird'] or self.gtnState == TOURNAMENT_STATE['thirdRunning']:
            self.widget.setTabIndex(THIRD_TAB_INDEX)

    def setTabBtnSelected(self):
        for i in range(0, self.tabButtonsLen):
            if i == self.tabIdx:
                self.widget.tabButtons[i].selected = True
            else:
                self.widget.tabButtons[i].selected = False

    def refreshTabBtnDisable(self, indexs = []):
        for i in range(0, self.tabButtonsLen):
            if i in indexs:
                self.widget.tabButtons[i].enabled = False
            else:
                self.widget.tabButtons[i].enabled = True

    def refreshTabHint(self, index = -1):
        for i in range(0, len(self.tabHints)):
            if i == index:
                self.tabHints[i].visible = True
            else:
                self.tabHints[i].visible = False

    def refreshGtnState(self, isFullRefresh = False):
        p = BigWorld.player()
        guildTournament = p.guildTournament.get(self.groupId)
        p.cell.queryGuildTournament(self.groupId, guildTournament.ver)
        if isFullRefresh:
            tournamentResult = p.worldWar.tournamentResult
            p.cell.queryWWTournament(self.groupId, tournamentResult.groupVer[self.groupId], tournamentResult.guildVer)

    def show(self, groupId):
        self.groupId = groupId
        if not self.widget:
            if not self.isReadyToShow:
                return
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_WW_TOURNAMENT_RESULT)
        else:
            self.refreshCurrentPanel()

    def readyToShow(self):
        self.isReadyToShow = True

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_WW_TOURNAMENT_RESULT)
        self.widget = None
        self.state = TOURNAMENT_STATE['firstBefore']
        self.gtnState = TOURNAMENT_STATE['firstBefore']
        self.isReadyToShow = False
        self.clearTimeCalBack()
        self.unRegisterCurrPanel()

    def clearTimeCalBack(self):
        if self.refreshStateTimeId:
            BigWorld.cancelCallback(self.refreshStateTimeId)
            self.refreshStateTimeId = 0
        if self.calTimeId:
            BigWorld.cancelCallback(self.calTimeId)
            self.calTimeId = 0

    def unRegisterCurrPanel(self):
        lastProxy = self.getTabViewProxy(self.tabIdx)
        if lastProxy and hasattr(lastProxy, 'unRegisterPanel'):
            lastProxy.unRegisterPanel()

    def getTabViewProxy(self, index):
        return getattr(self.uiAdapter, TAB_VIEW_MAP.get(index, ''), None)

    def onTabChanged(self, *args):
        currentTabIndex = int(args[3][0].GetNumber())
        currentView = ASObject(args[3][1])
        if currentTabIndex != self.tabIdx:
            self.unRegisterCurrPanel()
            self.tabIdx = currentTabIndex
        currentProxy = self.getTabViewProxy(self.tabIdx)
        if currentProxy and hasattr(currentProxy, 'initPanel'):
            currentProxy.initPanel(currentView, self.groupId)
        self.setTabBtnSelected()
        self.calTime(True)
