#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildJobProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
import commQuest
import utils
import npcConst
from guis import uiConst
from guis import uiUtils
from data import quest_data as QD
from data import quest_loop_data as QLD
from cdata import quest_reward_data as QRD
from data import guild_quest_config_data as GQCD
from cdata import business_lv_config_data as BLCD

class GuildJobProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildJobProxy, self).__init__(uiAdapter)
        self.modelMap = {'openJobDetail': self.onOpenGuildJobDetail,
         'getJobDetail': self.onGetGuildJobDetail,
         'acceptGuildJob': self.onAcceptGuildJob,
         'closeDetailPage': self.onCloseDetailPage}
        self.mediator = None
        self.detailMed = None
        self.questInfo = {}
        self.detailQuestId = 0
        self.readyShow = False
        self.npcId = 0
        self.npcEnt = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_JOB_BOARD:
            self.mediator = mediator
            return uiUtils.dict2GfxDict(self._createGuildBoardContent(), True)
        if widgetId == uiConst.WIDGET_GUILD_JOB_DETAIL:
            self.detailMed = mediator

    def showGuildBoard(self, npcId, npcEnt):
        self.readyShow = True
        self.npcId = npcId
        self.npcEnt = npcEnt
        self.questGuildData()

    def showGuildDetail(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_JOB_DETAIL)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.detailMed:
            self.closeGuildJobDetail()
            return
        else:
            self.mediator = None
            self.readyShow = False
            self.questInfo = {}
            self.npcId = 0
            self.npcEnt = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_JOB_BOARD)
            gameglobal.rds.ui.funcNpc.close()
            return

    def closeGuildJobDetail(self):
        self.detailMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_JOB_DETAIL)

    def onCloseDetailPage(self, *arg):
        self.closeGuildJobDetail()

    def questGuildData(self):
        BigWorld.player().displayGuildQuestBoard(250, 1)

    def updateGuildJobBoard(self, questInfo):
        self.questInfo = questInfo
        if self.npcId and self.npcEnt:
            gameglobal.rds.ui.funcNpc.openDirectly(self.npcId, self.npcEnt.npcId, npcConst.NPC_FUNC_GUILD_JOB)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_JOB_BOARD)

    def updateView(self):
        ret = self._createGuildBoardContent()
        if self.mediator:
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(ret, True))

    def _createGuildBoardContent(self):
        ret = {}
        updateTime = self._getGuildJobRefreshTime()
        ret['updateTime'] = gameStrings.TEXT_GUILDJOBPROXY_90 % (self._convertTimeFormat(updateTime[0]), self._convertTimeFormat(updateTime[1]))
        ret['items'] = []
        for key in self.questInfo:
            if self.questInfo[key].get('leftCount', 0) == 0:
                continue
            if not self.checkQuestLoopMatchGuildLimit(key):
                continue
            itemObj = {}
            itemObj['questId'] = key
            questLoopData = QLD.data.get(key, {})
            itemObj['title'] = questLoopData.get('name', '')
            itemObj['progress'] = gameStrings.TEXT_GUILDJOBPROXY_103 % (self.questInfo[key]['loopCnt'], self.questInfo[key]['maxLoopCnt']) if self.questInfo[key]['loopCnt'] < self.questInfo[key]['maxLoopCnt'] else gameStrings.TEXT_GUILDJOBPROXY_103_1
            itemObj['availableNum'] = gameStrings.TEXT_GUILDJOBPROXY_104 % (self.questInfo[key]['leftCount'] if self.questInfo[key].has_key('leftCount') else 0)
            itemObj['totalNum'] = gameStrings.TEXT_GUILDJOBPROXY_105 % (self.questInfo[key]['totalCount'] if self.questInfo[key].has_key('totalCount') else 0)
            ret['items'].append(itemObj)

        return ret

    def _convertTimeFormat(self, timeInt):
        timeStr = str(timeInt)
        if len(timeStr) == 2:
            return timeStr
        else:
            return '0%s' % timeStr

    def _getGuildJobRefreshTime(self):
        refreshTimes = GQCD.data.get('refreshTimes', [0])
        now = utils.getNow()
        minute = utils.getMinuteInt(now)
        hour = utils.getHourInt(now)
        defaultTime = refreshTimes[0]
        for refreshTime in refreshTimes:
            refreshHour = refreshTime / 100
            refreshMinute = refreshTime % 100
            if refreshHour > hour:
                return [refreshHour, refreshMinute]
            if refreshHour == hour and refreshMinute > minute:
                return [refreshHour, refreshMinute]

        refreshHour = defaultTime / 100
        refreshMinute = defaultTime % 100
        return [refreshHour, refreshMinute]

    def onOpenGuildJobDetail(self, *arg):
        self.detailQuestId = int(arg[3][0].GetNumber())
        self.showGuildDetail()

    def onGetGuildJobDetail(self, *arg):
        ret = self._createGuildJobDetail(self.detailQuestId)
        return uiUtils.dict2GfxDict(ret, True)

    def _createGuildJobDetail(self, questLoopId):
        ret = {}
        questLoopData = QLD.data.get(questLoopId, {})
        questId = questLoopData.get('quests', [0])[0]
        questData = QD.data.get(questId, {})
        questTitle = questLoopData.get('name', '')
        qusetDesc = questLoopData.get('desc', '')
        award = []
        rewardMode = questData.get('reward', 0)
        rewardType = QRD.data.get(rewardMode, {}).get('cashRewardType', 1)
        rewardStr = ''
        if rewardType == 1:
            rewardStr = gameStrings.TEXT_GUILDJOBPROXY_161
        else:
            rewardStr = gameStrings.TEXT_GUILDJOBPROXY_163
        exp, money, _, _ = commQuest.calcReward(BigWorld.player(), questId)
        money = int(money) if money else 0
        exp = int(exp) if exp else 0
        guildContribution = questData.get('guildContribution', 0)
        if money > 0:
            award.append({'value': money,
             'tip': rewardStr})
        if exp > 0:
            award.append({'value': exp,
             'tip': gameStrings.TEXT_GUILDJOBPROXY_174})
        if guildContribution > 0:
            award.append({'value': guildContribution,
             'tip': gameStrings.TEXT_GUILDJOBPROXY_176})
        items = commQuest.genQuestRewardItems(BigWorld.player(), questId)
        loopCnt = self.questInfo.get(questLoopId, {}).get('loopCnt', 0)
        maxLoopCnt = self.questInfo.get(questLoopId, {}).get('maxLoopCnt', 0)
        ret['progress'] = gameStrings.TEXT_GUILDJOBPROXY_103 % (loopCnt, maxLoopCnt) if loopCnt < maxLoopCnt else gameStrings.TEXT_GUILDJOBPROXY_103_1
        ret['questTitle'] = questTitle
        ret['qusetDesc'] = qusetDesc
        ret['award'] = award
        ret['items'] = self._createItemList(items)
        ret['canGetQuest'] = loopCnt < maxLoopCnt
        return ret

    def _createItemList(self, items):
        ret = []
        for itemData in items:
            itemObj = uiUtils.getGfxItemById(itemData[0], count=itemData[1])
            ret.append(itemObj)

        return ret

    def onAcceptGuildJob(self, *arg):
        if self.detailQuestId > 0:
            BigWorld.player().acceptGuildQuestLoop(self.detailQuestId)
            self.closeGuildJobDetail()
            self.hide()

    def checkQuestLoopMatchGuildLimit(self, questLoopId):
        td = QLD.data.get(questLoopId, {})
        owner = BigWorld.player()
        if td.has_key('acGuildLv'):
            if owner.guild is None or owner.guild.level < td['acGuildLv']:
                return False
        if td.has_key('acGuildBuildMarkers'):
            if owner.guild is None:
                return False
            for markerId, lv in td['acGuildBuildMarkers']:
                if owner.guild.isBuildingFinished(markerId):
                    continue
                if not owner.guild.marker[markerId].inBuilding(owner.guild):
                    continue
                marker = owner.guild.marker.get(markerId)
                building = marker.getBuilding(owner.guild)
                if building is None or building.level != lv:
                    continue
                break
            else:
                return False

        if td.has_key('acGuildBuildMarkersLv'):
            if owner.guild is None:
                return False
            for markerId, lv in td['acGuildBuildMarkersLv']:
                marker = owner.guild.marker.get(markerId)
                building = marker.getBuilding(owner.guild)
                if building is not None and building.level >= lv:
                    break
            else:
                return False

        if td.has_key('acGuildDevMarkers'):
            if owner.guild is None:
                return False
            for markerId, minProgress, maxProgress in td['acGuildDevMarkers']:
                if not owner.guild.marker or not owner.guild.marker.has_key(markerId):
                    return False
                if owner.guild.isDevFinished(markerId):
                    return False
                if not owner.guild.marker[markerId].inDev():
                    return False
                if owner.guild.marker[markerId].progress <= minProgress or owner.guild.marker[markerId].progress > maxProgress:
                    return False

        if td.has_key('acGuildAreas'):
            if owner.guild is None:
                return False
            for areaId in td['acGuildAreas']:
                if owner.guild.isAreaExtFinished(areaId):
                    return False

        if td.has_key('businessLv'):
            businessLv = td['businessLv']
            blcd = BLCD.data[businessLv]
            if not hasattr(owner.guild, 'bindCash') or owner.guild.bindCash < blcd['baseFame']:
                return False
            if owner.guild.getSelfContrib() < 0:
                return False
        return True
