#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServerTopRankGuildProxy.o
from gamestrings import gameStrings
import BigWorld
import utils
import uiUtils
import gameglobal
import gametypes
from guis.asObject import ASObject
from uiProxy import UIProxy
from guis import events
from guis import uiConst
from gamestrings import gameStrings
PRIVIEGE_DAY_TO_SECOND = 86400
PRIVIEGE_HOUR_TO_SECOND = 3600
from cdata import ns_guild_prestige_act_bonus_data as NGPABD
from data import bonus_data as BD

class NewServerTopRankGuildProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServerTopRankGuildProxy, self).__init__(uiAdapter)
        self.widget = None

    def reset(self):
        pass

    def initPanel(self, widget):
        self.widget = widget
        self.timer = None
        self.initUI()
        p = BigWorld.player()
        p.base.getNSGuildPrestigeRank()

    def unRegisterPanel(self):
        self.widget = None
        self.allValueList = None
        self.cleanTimer()

    def initUI(self):
        if not self.widget:
            return
        self.guildTopRankData = self.getOriginData()
        self.allValueList = sorted(self.guildTopRankData, key=lambda value: value[0])
        self.initListProp()
        self.updateTimer()

    def getOriginData(self):
        if getattr(self, 'guildTopRankData', []):
            return getattr(self, 'guildTopRankData', [])
        return []

    def setDataAndRefresh(self, data):
        self.guildTopRankData = data
        self.initUI()

    def initListProp(self):
        if not self.widget:
            return
        serverOpenTime = gameglobal.rds.configData.get('serverLatestMergeTime', 0) or utils.getServerOpenTime()
        stage = utils.getGuildPrestigeEnableStageAndOneDay(serverOpenTime)
        if stage > 0:
            self.widget.banner.loadImage('newServerTopRank/00%s.dds' % stage)
        self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.onGuildRankClick, False, 0, True)
        self.widget.listView.column = 1
        self.widget.listView.itemWidth = 554
        self.widget.listView.itemHeight = 68
        self.widget.listView.itemRenderer = 'NewServerTopRankTab0_GuildNode'
        self.widget.listView.labelFunction = self.guildNodeFunc
        self.widget.listView.dataArray = self.getGuildBonus()
        self.widget.listView.validateNow()

    def getGuildBonus(self):
        serverOpenTime = gameglobal.rds.configData.get('serverLatestMergeTime', 0) or utils.getServerOpenTime()
        bonusList = []
        stage = utils.getGuildPrestigeEnableStageAndOneDay(serverOpenTime)
        configData = utils.getNSPrestigeActivityConfigData()
        if stage <= 0:
            return bonusList
        bonusMap = configData.get('rankBonus%s' % stage, {})
        for k, v in bonusMap.items():
            bonusList.append((k, v))

        return sorted(bonusList, key=lambda value: value[0][0])

    def guildNodeFunc(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        guildName = ''
        if data[0][0] == data[0][1]:
            item.rankText.text = gameStrings.NEW_SERVER_TOP_RANK % data[0][0]
            if data[0][0] <= len(self.allValueList):
                guildInfo = self.allValueList[data[0][0] - 1]
                if guildInfo and guildInfo[2]:
                    guildName = guildInfo[2]
        else:
            item.rankText.text = gameStrings.NEW_SERVER_TOP_RANK % (str(data[0][0]) + '-' + str(data[0][1]))
        if guildName:
            item.guildName.visible = True
            item.labelText.visible = True
            item.guildName.text = guildName
        else:
            item.guildName.visible = False
            item.labelText.visible = False
        bonusList = self.getItemByBonusId(data[1])
        allFixedItems = []
        for bonusId in bonusList:
            fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            for fixedItem in fixedBonus:
                if fixedItem[1] not in allFixedItems:
                    allFixedItems.append(fixedItem[1])

        for i in range(0, 5):
            itemNode = getattr(item, 'item%s' % i)
            if itemNode.slot:
                itemNode.slot.dragable = False
                if i + 1 > len(allFixedItems):
                    itemNode.visible = False
                else:
                    itemNode.visible = True
                    info = uiUtils.getGfxItemById(allFixedItems[i])
                    itemNode.slot.setItemSlotData(info)

    def getItemByBonusId(self, bonusId):
        itemList = []
        bonusInfo = NGPABD.data.get(bonusId)
        if not bonusInfo:
            return itemList
        for value in bonusInfo:
            if value.get('bonusId'):
                itemList.append(value.get('bonusId'))

        return itemList

    def updateTimer(self):
        serverOpenTime = gameglobal.rds.configData.get('serverLatestMergeTime', 0) or utils.getServerOpenTime()
        configData = utils.getNSPrestigeActivityConfigData()
        stage = utils.getGuildPrestigeEnableStageAndOneDay(serverOpenTime)
        enableTime = configData.get('enableTime%s' % stage)
        if not enableTime:
            self.cleanTimer()
            leftTime = 0
        else:
            periodType, nWeeksOffset, nLastWeeks = enableTime
            tStart, tEnd = utils.calcTimeDuration(periodType, serverOpenTime, nWeeksOffset, nLastWeeks)
            if tStart <= utils.getNow() <= tEnd:
                leftTime = tEnd - utils.getNow()
            else:
                leftTime = 0
        if leftTime > PRIVIEGE_DAY_TO_SECOND:
            timeText = utils.formatTimeStr(leftTime, formatStr=gameStrings.TEXT_NEWSERVERTOPRANKCOMBATSCOREANDLVPROXY_262)
        elif PRIVIEGE_HOUR_TO_SECOND <= leftTime <= PRIVIEGE_DAY_TO_SECOND:
            timeText = utils.formatTimeStr(leftTime, formatStr=gameStrings.TEXT_NEWSERVERTOPRANKCOMBATSCOREANDLVPROXY_265)
        else:
            timeText = utils.formatTimeStr(leftTime, formatStr=gameStrings.TEXT_NEWSERVERTOPRANKCOMBATSCOREANDLVPROXY_267)
        if self.widget:
            if leftTime == 0:
                self.widget.timeText.text = gameStrings.NEW_SERVER_TOP_RANK_END
            else:
                self.widget.timeText.text = gameStrings.LEFT_TIME % timeText
        if leftTime > 0:
            self.timer = BigWorld.callback(1, self.updateTimer)
        elif stage != utils.getGuildPrestigeLastStage():
            p = BigWorld.player()
            p.base.getNSGuildPrestigeRank()
            BigWorld.callback(2, self.initListProp)
            self.timer = BigWorld.callback(1, self.updateTimer)
        else:
            self.cleanTimer()

    def onGuildRankClick(self, *args):
        GUILD_TAB_IDX = 5
        ranking = gameglobal.rds.ui.ranking
        if ranking.mediator:
            ranking.setTab(uiConst.NEW_RANK_GUILD)
        else:
            ranking.show(uiConst.NEW_RANK_GUILD)

    def cleanTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None
