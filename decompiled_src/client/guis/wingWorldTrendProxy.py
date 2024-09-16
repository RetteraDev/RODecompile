#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldTrendProxy.o
import BigWorld
import gametypes
import const
import uiConst
import utils
import events
import gameglobal
import clientUtils
import wingWorldUtils
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis import uiUtils
from guis.asObject import ASUtils
from data import wing_world_trend_data as WWTD
from data import wing_world_city_data as WWCTD
from data import region_server_config_data as RSCD
from data import wing_world_config_data as WWCD
from cdata import wing_world_schedule_data as WWSD
REWARD_TYPES_CNT = 3
GUILD_REWARD_MAX_CNT = 3
PERSONAL_REWRD_MAX_CNT = 2
CAMP_REWARD_MAX_CNT = 3
SORT_TYPE_NOW = 0
SORT_TYPE_WILL = 1
SORT_TYPE_FINISHEND = 2
SORT_TYPE_OVER_TIME = 3

class WingWorldTrendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldTrendProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.stage2CrontStr = {}
        groupId = RSCD.data.get(BigWorld.player().getOriginHostId(), {}).get('wingWorldGroupId', 0)
        for _, cfgData in WWSD.data.iteritems():
            if cfgData.get('stype', 0) == wingWorldUtils.getWorldTrendCrontabType(groupId):
                self.stage2CrontStr[cfgData['state']] = cfgData['crontab']

        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_TREND, self.hide)

    def reset(self):
        self.trendId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_TREND:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_TREND)

    def show(self):
        if not self.widget:
            self.uiAdapter.wingWorldOverView.updateCountryEventFlag(True)
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_TREND)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.itemRenderer = 'WingWorldTrend_ItemRender'
        self.widget.scrollWndList.labelFunction = self.labelFunction
        self.setRewrdMcVisible(False)
        self.widget.reward.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseRewardMcClick, False, 0, True)

    def labelFunction(self, *args):
        p = BigWorld.player()
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        ASUtils.setMcEffect(itemMc, 'gray' if itemData.sortType[0] == SORT_TYPE_OVER_TIME else 'normal')
        itemMc.bg.gotoAndStop('jinxiongzhong' if itemData.sortType[0] == SORT_TYPE_NOW else 'jiangkaiqi')
        itemMc.txtTitle.htmlText = itemData.title
        itemMc.txtEndTime.x = itemMc.txtTitle.x + itemMc.txtTitle.textWidth + 20
        endTime = int(itemData.endTime)
        itemMc.txtEndTime.text = gameStrings.WING_WORLD_TREND_TIME % (utils.getMonthInt(endTime), utils.getMonthDayInt(endTime))
        itemMc.txtDesc.htmlText = itemData.desc
        itemMc.txtCompleteHosts.text = itemData.completeHost
        itemMc.complete.visible = itemData.isComplete
        if endTime - const.TIME_INTERVAL_WEEK < utils.getNow() < endTime:
            itemMc.lastWeek.visible = True
        else:
            itemMc.lastWeek.visible = False
        if p.isWingWorldCampMode():
            if WWTD.data.get(itemData.stage, {}).get('rewardId', 0):
                itemMc.showRewardBtn.visible = True
            else:
                itemMc.showRewardBtn.visible = False
        itemMc.showRewardBtn.data = itemData.stage
        itemMc.showRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleShowRewardBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        dataArray = []
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            for state, cfgData in WWTD.data.iteritems():
                if cfgData.get('trendType', 0) != 1:
                    continue
                info = {}
                info['title'] = cfgData.get('title', 'title')
                endTime = self.getTime(self.stage2CrontStr[state])
                info['endTime'] = endTime
                targetCityLv, needCnt = cfgData.get('limitTarget', (1, 1))
                completeCampIds = self.getCompleteCampIds(state)
                info['stage'] = state
                campNames = ','.join([ utils.getWingCampName(campId) for campId in completeCampIds ])
                if not campNames:
                    info['completeHost'] = gameStrings.WING_WORLD_TREND_NO_CAMPS
                else:
                    info['completeHost'] = gameStrings.WING_WORLD_TREND_CAMPS % campNames
                if needCnt > 1:
                    if p.wingWorldCamp in completeCampIds:
                        info['desc'] = cfgData.get('desc', str(needCnt) + '/%d') % needCnt
                    else:
                        info['desc'] = cfgData.get('desc', '%d/' + str(needCnt)) % self.getOwnCampCnt(targetCityLv)
                else:
                    info['desc'] = cfgData.get('desc', 'desc')
                if utils.getNow() > endTime:
                    info['sortType'] = (SORT_TYPE_OVER_TIME, endTime)
                elif p.wingWorldCamp in completeCampIds:
                    info['sortType'] = (SORT_TYPE_FINISHEND, endTime)
                elif not self.stage2CrontStr.has_key(state - 1) or self.stage2CrontStr.has_key(state - 1) and utils.getNow() > self.getTime(self.stage2CrontStr[state - 1]):
                    info['sortType'] = (SORT_TYPE_NOW, endTime)
                else:
                    info['sortType'] = (SORT_TYPE_WILL, endTime)
                info['isComplete'] = p.wingWorldCamp in completeCampIds
                dataArray.append(info)

        else:
            originHostId = BigWorld.player().getOriginHostId()
            for state, cfgData in WWTD.data.iteritems():
                if cfgData.get('trendType', 0) != 0:
                    continue
                info = {}
                info['title'] = cfgData.get('title', 'title')
                endTime = self.getTime(self.stage2CrontStr[state])
                info['endTime'] = endTime
                targetCityLv, needCnt = cfgData.get('limitTarget', (1, 1))
                completeHostIds = self.getCompleteHostIds(state)
                hostNames = ''
                info['stage'] = state
                for hostId in completeHostIds:
                    if hostNames:
                        hostNames += ','
                    hostNames += RSCD.data.get(hostId, {}).get('serverName', '')

                if not hostNames:
                    info['completeHost'] = gameStrings.WING_WORLD_TREND_NO_HOSTS
                else:
                    info['completeHost'] = gameStrings.WING_WORLD_TREND_HOSTS % hostNames
                if needCnt > 1:
                    if originHostId in completeHostIds:
                        info['desc'] = cfgData.get('desc', str(needCnt) + '/%d') % needCnt
                    else:
                        info['desc'] = cfgData.get('desc', '%d/' + str(needCnt)) % self.getOwnCityCnt(targetCityLv)
                else:
                    info['desc'] = cfgData.get('desc', 'desc')
                if utils.getNow() > endTime:
                    info['sortType'] = (SORT_TYPE_OVER_TIME, endTime)
                elif originHostId in completeHostIds:
                    info['sortType'] = (SORT_TYPE_FINISHEND, endTime)
                elif not self.stage2CrontStr.has_key(state - 1) or self.stage2CrontStr.has_key(state - 1) and utils.getNow() > self.getTime(self.stage2CrontStr[state - 1]):
                    info['sortType'] = (SORT_TYPE_NOW, endTime)
                else:
                    info['sortType'] = (SORT_TYPE_WILL, endTime)
                info['isComplete'] = originHostId in completeHostIds
                dataArray.append(info)

        dataArray.sort(cmp=lambda a, b: cmp(a['sortType'], b['sortType']))
        self.widget.scrollWndList.dataArray = dataArray

    def getTime(self, cront):
        endTime = utils.getNextCrontabTime(cront)
        if utils.getYearInt(endTime) != utils.getYearInt(utils.getNow()):
            endTime = utils.getPreCrontabTime(cront)
        return endTime

    def setRewrdMcVisible(self, visible):
        if not self.widget:
            return
        self.widget.reward.visible = visible
        if visible:
            self.refreshRewrd()

    def getOwnCityCnt(self, targetCityLv):
        country = BigWorld.player().wingWorld.country.getOwn()
        cnt = 0
        for hostId in country.ownedCityIds:
            if WWCTD.data.get(hostId, {}).get('level', 0) == targetCityLv:
                cnt += 1

        return cnt

    def getOwnCampCnt(self, targetCityLv):
        camp = BigWorld.player().wingWorld.country.getOwnCamp()
        cnt = 0
        for hostId in camp.ownedCityIds:
            if WWCTD.data.get(hostId, {}).get('level', 0) == targetCityLv:
                cnt += 1

        return cnt

    def getCompleteCampIds(self, trendId):
        campIds = []
        for campId in gametypes.WING_WORLD_CAMPS:
            campVal = BigWorld.player().wingWorld.country.getCamp(campId)
            if trendId in campVal.trendIds:
                campIds.append(campId)

        return campIds

    def getCompleteHostIds(self, trendId):
        hostIds = []
        p = BigWorld.player()
        for hostId, countryVal in p.wingWorld.country.iteritems():
            if not p.wingWorld.country.isNormalHostId(hostId):
                continue
            if trendId in countryVal.trendIds:
                hostIds.append(hostId)

        return hostIds

    def refreshOldReward(self):
        self.widget.reward.txtTips.htmlText = WWCD.data.get('trendRewardDesc', 'trendRewardDesc')
        for typeId in xrange(REWARD_TYPES_CNT):
            rewardMc = self.widget.reward.getChildByName('reward%d' % typeId)
            rewardMc.txtName.text = gameStrings.WING_WORLD_MANAGER_GUILDS[typeId]
            bonusIds = wingWorldUtils.getGuildWorldTrendRewardInfo(self.trendId, typeId + 1)[0]
            guildRewards = []
            for bonusId in bonusIds:
                guildRewards.extend(clientUtils.genItemBonusEx(bonusId))

            personalBonus = wingWorldUtils.getPersonalWorldTrendRewardInfo(self.trendId, typeId + 1)
            personalRewards = clientUtils.genItemBonusEx(personalBonus)
            for index in xrange(GUILD_REWARD_MAX_CNT):
                itemMc = getattr(rewardMc, 'item%d' % index)
                if index < len(guildRewards):
                    itemMc.visible = True
                    itemMc.slot.dragable = False
                    itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(guildRewards[index][0], guildRewards[index][1]))
                else:
                    itemMc.visible = False

            for index in xrange(PERSONAL_REWRD_MAX_CNT):
                itemMc = getattr(rewardMc, 'personalItem%d' % index)
                if index < len(personalRewards):
                    itemMc.visible = True
                    itemMc.slot.dragable = False
                    itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(personalRewards[index][0], personalRewards[index][1]))
                else:
                    itemMc.visible = False

    def refreshCampReward(self):
        self.widget.reward.txtTips.htmlText = WWCD.data.get('trendCampRewardDesc', 'trendCampRewardDesc')
        self.widget.reward.rewardList.itemRenderer = 'WingWorldTrend_RewardItem'
        self.widget.reward.rewardList.itemHeight = 56
        self.widget.reward.rewardList.lableFunction = self.campRewardLabelFunc
        trendIds = WWTD.data.get(self.trendId, {}).get('campReward', {}).keys()
        trendIds.sort()
        self.widget.reward.rewardList.dataArray = trendIds

    def campRewardLabelFunc(self, *args):
        typeId = args[3][0].GetNumber()
        rewardMc = ASObject(args[3][1])
        descTitles = WWCD.data.get('campTrendRewardTitles', {})
        rewardMc.txtName.text = descTitles.get(typeId, '')
        bonusId = wingWorldUtils.getWorldTrendCampRewardInfo(self.trendId, typeId)
        campRewards = clientUtils.genItemBonusEx(bonusId)
        bonusId1 = wingWorldUtils.getWorldTrendCamp1RewardInfo(self.trendId, typeId)
        camp1Rewards = clientUtils.genItemBonusEx(bonusId1)
        for index in xrange(CAMP_REWARD_MAX_CNT):
            itemMc = getattr(rewardMc, 'item%d' % index)
            if index < len(campRewards):
                itemMc.visible = True
                itemMc.slot.dragable = False
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(campRewards[index][0], campRewards[index][1]))
            else:
                itemMc.visible = False

        for index in xrange(CAMP_REWARD_MAX_CNT):
            itemMc = getattr(rewardMc, 'personalItem%d' % index)
            if index < len(camp1Rewards):
                itemMc.visible = True
                itemMc.slot.dragable = False
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(camp1Rewards[index][0], camp1Rewards[index][1]))
            else:
                itemMc.visible = False

    def refreshRewrd(self):
        if not self.widget or not self.widget.reward.visible:
            return
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            self.widget.reward.gotoAndStop('camp')
            self.refreshCampReward()
        else:
            self.widget.reward.gotoAndStop('normal')
            self.refreshOldReward()

    def handleCloseRewardMcClick(self, *args):
        self.setRewrdMcVisible(False)

    def handleShowRewardBtn(self, *args):
        e = ASObject(args[3][0])
        trendId = int(e.currentTarget.data)
        self.trendId = trendId
        p = BigWorld.player()
        if p.isWingWorldCampMode():
            rewardId = WWTD.data.get(self.trendId, {}).get('rewardId', 0)
            if rewardId:
                gameglobal.rds.ui.generalReward.show(rewardId)
            return
        self.setRewrdMcVisible(trendId)
