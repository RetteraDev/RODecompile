#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaPlayoffs5v5FinalProxy.o
import BigWorld
import gameglobal
import utils
import copy
import uiConst
import datetime
from guis.asObject import ASObject
from guis import events
from guis import arenaPlayoffsProxy
from gamestrings import gameStrings
from data import arena_5v5_group_duel_data as A5GDD
from uiProxy import UIProxy
DAY_MAX = 4
DAY_ARENA_DUEL_TEAM_NUMS = [8,
 4,
 2,
 1]

class ArenaPlayoffs5v5FinalProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaPlayoffs5v5FinalProxy, self).__init__(uiAdapter)
        self.widget = None
        self.selectLvIndex = 1
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PVP_PLAYOFFS_5V5_FINAL, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PVP_PLAYOFFS_5V5_FINAL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            gameglobal.rds.ui.arenaPlayoffs.select5V5FinalResult(self.selectLvIndex)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PVP_PLAYOFFS_5V5_FINAL)

    def show(self, selectLvIndex = 4):
        if selectLvIndex not in (4, 5):
            selectLvIndex = 4
        self.selectLvIndex = selectLvIndex
        gameglobal.rds.ui.arenaPlayoffs.select5V5FinalResult(self.selectLvIndex)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PVP_PLAYOFFS_5V5_FINAL)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        keyIndexs = gameglobal.rds.ui.arenaPlayoffs.getKeyIndexs()
        for i in xrange(1, 3):
            rBtn = self.widget.getChildByName('lv%dBtn' % (i + 1))
            if rBtn:
                rBtn.visible = True
                rBtn.data = keyIndexs[i]
                rBtn.selected = self.selectLvIndex == keyIndexs[i]
                rBtn.addEventListener(events.EVENT_SELECT, self.handleSelectLv)

    def handleSelectLv(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.selected:
            selectLvIndex = int(e.currentTarget.data)
            self.selectLvIndex = selectLvIndex
            gameglobal.rds.ui.arenaPlayoffs.select5V5FinalResult(selectLvIndex)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshDayLabel()
        self.refreshFinalResult()

    def refreshDayLabel(self):
        dayLabels = self.getPlayoffs5v5DayLabel()
        for i in xrange(DAY_MAX):
            self.setDayLabel(self.widget.getChildByName('day%d' % i), dayLabels[i])

    def getArenaFinalSchedule(self):
        schedule = gameglobal.rds.ui.pvpPlayoffs5V5.getArenaPlayOffSchedule()
        macthDateTime = schedule['kickOutStartTime']
        schedules = []
        for key in sorted(A5GDD.data.keys()):
            val = A5GDD.data[key]
            lvKey = utils.lv2ArenaPlayoffs5v5Teamkey(BigWorld.player().lv)
            if val.get('type') == arenaPlayoffsProxy.TYPE_FINAL_DUEL and lvKey == key[1]:
                scheduleInfo = copy.deepcopy(A5GDD.data[key])
                startTimeStr = val.get('startTime', '%d.%d.%d.19.0.0')
                endTimeStr = val.get('endTime', '%d.%d.%d.20.20.0')
                startTime = startTimeStr % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
                endTime = endTimeStr % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
                scheduleInfo['startTime'] = startTime
                scheduleInfo['endTime'] = endTime
                schedules.append(scheduleInfo)

        return schedules

    def getPlayoffs5v5DayLabel(self):
        schedule = gameglobal.rds.ui.pvpPlayoffs5V5.getArenaPlayOffSchedule()
        dayLabels = []
        macthDateTime = schedule['kickOutStartTime']
        for key in sorted(A5GDD.data.keys()):
            val = A5GDD.data[key]
            lvKey = utils.lv2ArenaPlayoffs5v5Teamkey(BigWorld.player().lv)
            if val.get('type') == arenaPlayoffsProxy.TYPE_FINAL_DUEL and lvKey == key[1]:
                startTimeStr = val.get('startTime', '%d.%d.%d.19.0.0')
                endTimeStr = val.get('endTime', '%d.%d.%d.20.20.0')
                startTime = startTimeStr % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
                endTime = endTimeStr % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
                dayLabels.append({'week': '%d.%d' % (macthDateTime.month, macthDateTime.day),
                 'date': val.get('date', ''),
                 'state': gameglobal.rds.ui.arenaPlayoffs.getTimeState(startTime, endTime)})

        return dayLabels

    def refreshFinalResult(self):
        finalDuelResult = gameglobal.rds.ui.arenaPlayoffs.getFinalDuelResult()
        teamData = finalDuelResult.get('teams', [])
        for i in xrange(DAY_MAX):
            for j in xrange(DAY_ARENA_DUEL_TEAM_NUMS[i]):
                teamInfo = {}
                if len(teamData) > i:
                    if len(teamData[i]) > j:
                        teamInfo = teamData[i][j]
                teamMc = self.widget.getChildByName('team%d%d' % (i, j + 1))
                self.setTeamInfo(teamMc, teamInfo)
                if j % 2 == 0:
                    self.setLineResult(self.widget.getChildByName('line%d%d' % (i, int(j / 2))), teamInfo)
                    cameraMc = self.widget.getChildByName('camera%d%d' % (i, int(j / 2)))
                    if cameraMc:
                        if teamInfo and teamInfo.get('canView', False):
                            cameraMc.visible = True
                        else:
                            cameraMc.visible = False
                        if cameraMc.visible:
                            cameraMc.data = teamInfo
                            cameraMc.addEventListener(events.MOUSE_CLICK, self.handleViewArena)

    def handleViewArena(self, *args):
        e = ASObject(args[3][0])
        data = e.currentTarget.data
        nuid = data.nuid
        gameglobal.rds.ui.arenaPlayoffs.enterArena5v5WithLive(nuid, False)

    def setLineResult(self, lineMc, teamInfo):
        if lineMc:
            if teamInfo and teamInfo.get('duelDone', False):
                lineMc.visible = True
            else:
                lineMc.visible = False
            if lineMc.visible:
                lineMc.gotoAndStop('state%d' % (1 if teamInfo.get('win', False) else 0))

    def setTeamInfo(self, teamMc, teamInfo):
        if teamMc:
            if teamInfo:
                teamMc.teamName.htmlText = teamInfo.get('teamName', '')
                teamMc.unknownIcon.visible = False
                if teamMc.winIcon:
                    teamMc.winIcon.visible = teamInfo.get('duelDone', False)
                    teamMc.winIcon.gotoAndStop('state%d' % (1 if teamInfo.get('win', False) else 0))
                for i in xrange(3):
                    starMc = teamMc.getChildByName('star%d' % i)
                    if starMc:
                        starMc.visible = i + 1 <= teamInfo.get('winCnt', 0)
                        starMc.gotoAndStop('state%d' % (1 if i + 1 <= teamInfo.get('winCnt', 0) else 0))

                teamMc.data = teamInfo
                teamMc.addEventListener(events.MOUSE_CLICK, self.handleClickItem, False, 0, True)
            else:
                teamMc.teamName.htmlText = ''
                teamMc.unknownIcon.visible = True
                if teamMc.winIcon:
                    teamMc.winIcon.visible = False
                for i in xrange(3):
                    starMc = teamMc.getChildByName('star%d' % i)
                    if starMc:
                        starMc.visible = False
                        starMc.gotoAndStop('state0')

                teamMc.data = None
                teamMc.removeEventListener(events.MOUSE_CLICK, self.handleClickItem)

    def handleClickItem(self, *args):
        e = ASObject(args[3][0])
        data = e.currentTarget.data
        lvKey = gameglobal.rds.ui.arenaPlayoffs.selFinalLvKey
        gameglobal.rds.ui.arenaPlayoffs.showArenaPlayoffsTeamInfo(long(data.nuid), data.hostId, '', 0, lvKey)

    def setDayLabel(self, daymc, labelInfo):
        if daymc and labelInfo:
            daymc.gotoAndPlay('state%s' % str(labelInfo['state']))
            daymc.week.htmlText = labelInfo['week']
            daymc.date.htmlText = labelInfo['date']
