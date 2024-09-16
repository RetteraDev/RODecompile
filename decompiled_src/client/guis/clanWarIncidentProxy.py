#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/clanWarIncidentProxy.o
import BigWorld
import gametypes
import gamelog
import const
import uiConst
import utils
import events
import clientUtils
import time
import datetime
import calendar
import ui
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from data import cross_clan_war_config_data as CCWCD
from data import clan_war_event_limit_data as CWELD
from data import clan_war_fort_data as CWFD
TAB_LIMIT_EVENT = 0
TAB_ADD_EVENT = 1

class ClanWarIncidentProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClanWarIncidentProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLAN_WAR_INCIDENT, self.hide)

    def reset(self):
        self.widget = None
        self.clanWarAddEvents = None
        self.clanWarLimitEvents = None
        self.selectedTab = TAB_LIMIT_EVENT

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CLAN_WAR_INCIDENT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CLAN_WAR_INCIDENT)

    def setAddEventData(self, data):
        self.clanWarAddEvents = data
        self.refreshInfo()

    def setLimitEventData(self, data):
        self.clanWarLimitEvents = data
        self.refreshInfo()

    @ui.callInCD()
    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CLAN_WAR_INCIDENT)
        BigWorld.player().cell.queryClanWarLimitEvent()

    def initUI(self):
        eventSeasonStartCrontab = CCWCD.data.get('eventSeasonStartCrontab')
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.tabBtn0.addEventListener(events.BUTTON_CLICK, self.handleLimitBtnClick, False, 0, True)
        self.widget.tabBtn1.addEventListener(events.BUTTON_CLICK, self.handleAddBtnClick, False, 0, True)
        self.widget.scrollWndList.itemRenderer = 'ClanWarIncident_item'
        self.widget.scrollWndList.itemHeight = 96
        self.widget.scrollWndList.labelFunction = self.labelFunction
        starTime = utils.formatDate(utils.getPreCrontabTime(eventSeasonStartCrontab))
        endTime = utils.formatDate(utils.getNextCrontabTime(eventSeasonStartCrontab) - 1)
        self.widget.timeDesc.text = gameStrings.CLAN_WAR_INCIDENT_TIME_DESC % (starTime, endTime)
        self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.handleClickRankBtn, False, 0, True)

    def labelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.txtTitle.htmlText = itemData.title
        itemMc.txtDesc.htmlText = itemData.desc
        itemMc.score.txtScore.text = itemData.recordScore
        if self.selectedTab == TAB_ADD_EVENT:
            if itemData.isOccupied:
                itemMc.gotoAndStop('dark')
                itemMc.guildName.desc.htmlText = gameStrings.CLAN_WAR_INCIDENT_GUILD_NAME_DESC_1
            else:
                itemMc.gotoAndStop('light')
                itemMc.guildName.desc.htmlText = gameStrings.CLAN_WAR_INCIDENT_GUILD_NAME_DESC_2
            itemMc.lastWeek.visible = False
            itemMc.endTime.visible = False
            itemMc.guildName.txtName.visible = False
        else:
            if itemData.isFinish:
                itemMc.gotoAndStop('dark')
            else:
                itemMc.gotoAndStop('light')
            itemMc.lastWeek.visible = itemData.isLastWeek
            itemMc.endTime.visible = True
            itemMc.endTime.htmlText = itemData.startTimeDesc
            itemMc.guildName.txtName.visible = True
            itemMc.guildName.desc.text = gameStrings.CLAN_WAR_INCIDENT_GUILD_NAME_DESC_3
            itemMc.guildName.txtName.text = itemData.guildName

    def handleAddBtnClick(self, *args):
        self.selectedTab = TAB_ADD_EVENT
        BigWorld.player().cell.queryClanWarAddEvent()

    def handleLimitBtnClick(self, *args):
        self.selectedTab = TAB_LIMIT_EVENT
        BigWorld.player().cell.queryClanWarLimitEvent()

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.tabBtn0.selected = self.selectedTab == TAB_LIMIT_EVENT
        self.widget.tabBtn1.selected = self.selectedTab == TAB_ADD_EVENT
        tNow = utils.getNow()
        dataArray = []
        if self.selectedTab == TAB_ADD_EVENT:
            self.widget.tips.tipsDesc.text = CCWCD.data.get('clanWarAddEventsTips')
            addFortIds = set()
            if self.clanWarAddEvents:
                for val in self.clanWarAddEvents:
                    if not utils.isSameMonth(tNow, val[-1]):
                        continue
                    addFortIds |= val[-2]

            addFortData = CWFD.data
            for fortId, value in addFortData.iteritems():
                info = {}
                info['title'] = gameStrings.CLAN_WAR_INCIDENT_ITEM_TITLE % value.get('showName')
                info['desc'] = value.get('desc')
                info['recordScore'] = value.get('eventScore')
                info['isOccupied'] = fortId in addFortIds
                dataArray.append(info)

        else:
            self.widget.tips.tipsDesc.text = CCWCD.data.get('clanWarLimitEventsTips')
            limitFortEvents = {}
            eventSeasonStartCrontab = CCWCD.data.get('eventSeasonStartCrontab')
            eventSeasonStartTime = utils.getPreCrontabTime(eventSeasonStartCrontab)
            eventSeasonEndTime = utils.getNextCrontabTime(eventSeasonStartCrontab)
            totalWeeks = self.getWeeks(eventSeasonStartTime, eventSeasonEndTime)
            deltaDay = (calendar.SATURDAY - datetime.datetime.fromtimestamp(eventSeasonStartTime).weekday()) % 7
            firstEventStartTime = eventSeasonStartTime + const.TIME_INTERVAL_DAY * deltaDay
            nowWeekIndex = utils.getIntervalWeek(utils.getNow(), firstEventStartTime) + 1
            if self.clanWarLimitEvents:
                for data in self.clanWarLimitEvents:
                    name = data[1]
                    hostName = utils.getServerName(data[2])
                    eventTime = data[3]
                    weekIndex = utils.getIntervalWeek(eventTime, firstEventStartTime) + 1
                    if data[2] and utils.getHostId() != data[2]:
                        limitFortEvents[weekIndex] = name + '-' + hostName
                    else:
                        limitFortEvents[weekIndex] = name

            for index in xrange(totalWeeks):
                weekIndex = index + 1
                value = CWELD.data.get(weekIndex)
                info = {}
                fortId = value.get('fortId')
                name = CWFD.data.get(fortId).get('showName')
                info['title'] = value.get('name')
                info['desc'] = value.get('desc')
                info['recordScore'] = value.get('score')
                if weekIndex in limitFortEvents.keys():
                    guildName = limitFortEvents[weekIndex]
                    info['guildName'] = guildName
                else:
                    info['guildName'] = gameStrings.CLAN_WAR_INCIDENT_NO_GUILD
                eventWeekEndTime = firstEventStartTime + (weekIndex - 1) * const.TIME_INTERVAL_WEEK + 22 * const.TIME_INTERVAL_HOUR
                isFinish = utils.getNow() > eventWeekEndTime
                info['isFinish'] = isFinish
                info['isLastWeek'] = weekIndex == nowWeekIndex
                if isFinish:
                    info['startTimeDesc'] = gameStrings.CLAN_WAR_INCIDENT_START_TIME_DESC_1
                    info['isFinish'] = True
                else:
                    endTimeDesc = time.strftime(gameStrings.CLAN_WAR_INCIDENT_DATE, time.localtime(eventWeekEndTime))
                    info['startTimeDesc'] = gameStrings.CLAN_WAR_INCIDENT_START_TIME_DESC_2 % endTimeDesc
                dataArray.append(info)
                dataArray.sort(key=lambda x: x.get('isFinish'))

        self.widget.scrollWndList.dataArray = dataArray

    def getTime(self, cront):
        endTime = utils.getNextCrontabTime(cront)
        if utils.getYearInt(endTime) != utils.getYearInt(utils.getNow()):
            endTime = utils.getPreCrontabTime(cront)
        return endTime

    def getWeeks(self, start, end):
        deltaDay = (calendar.SATURDAY - datetime.datetime.fromtimestamp(start).weekday()) % 7
        firstEventStartTime = start + const.TIME_INTERVAL_DAY * deltaDay
        endTimeLocal = time.localtime(end - 1)
        endMonth = endTimeLocal.tm_mon
        endYear = endTimeLocal.tm_year
        monthInfo = calendar.monthrange(endYear, endMonth)
        monthLastDay = datetime.datetime.strptime('%s-%s-%s' % (endYear, endMonth, monthInfo[1]), '%Y-%m-%d').date()
        monthLastDayWeek = int(monthLastDay.strftime('%w'))
        monthLastSaturday = monthLastDay
        if monthLastDayWeek != 6:
            deltaDays = monthLastDayWeek + 1
            monthLastSaturday = monthLastDay - datetime.timedelta(days=deltaDays)
        finalEventStartTime = time.mktime(monthLastSaturday.timetuple())
        return utils.getIntervalWeek(firstEventStartTime, finalEventStartTime) + 1

    def handleClickRankBtn(self, *args):
        self.uiAdapter.rankCommon.showRankCommon(gametypes.TOP_TYPE_CLAN_WAR_EVENT)
