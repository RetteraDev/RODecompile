#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldCampTrendProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import utils
import gametypes
import wingWorldUtils
from guis.asObject import ASObject
from guis import events
from data import region_server_config_data as RSCD
from data import wing_world_trend_data as WWTD
from cdata import wing_world_schedule_data as WWSD
from gamestrings import gameStrings
from uiProxy import UIProxy
import const
STAGE_NUM = 3

class WingWorldCampTrendProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldCampTrendProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currentStage = 0
        self.tempRankKey = 0
        self.reset()
        self.stages = []
        self.stage2CrontStr = {}
        groupId = RSCD.data.get(BigWorld.player().getOriginHostId(), {}).get('wingWorldGroupId', 0)
        for _, cfgData in WWSD.data.iteritems():
            if cfgData.get('stype', 0) == wingWorldUtils.getWorldTrendCrontabType(groupId):
                self.stage2CrontStr[cfgData['state']] = cfgData['crontab']

        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_CAMP_TREND, self.hide)

    def reset(self):
        self.currentStage = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_CAMP_TREND:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_CAMP_TREND)
        self.reset()

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_CAMP_TREND)

    def initUI(self):
        self.initStageInfo()
        self.currentStage = self.getCurrentStage()
        if self.currentStage < 0:
            self.currentStage = self.stages[0][0]
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def initStageInfo(self):
        groupId = RSCD.data.get(BigWorld.player().getOriginHostId(), {}).get('wingWorldGroupId', 0)
        for _, cfgData in WWSD.data.iteritems():
            if cfgData.get('stype', 0) == wingWorldUtils.getWorldTrendCrontabType(groupId):
                self.stage2CrontStr[cfgData['state']] = cfgData['crontab']

        stages = []
        for state, cfgData in WWTD.data.iteritems():
            if cfgData.get('trendType', 0) != 1:
                continue
            endTime = self.getTime(self.stage2CrontStr[state])
            stages.append((state, endTime))
            if len(stages) >= STAGE_NUM:
                break

        stages.sort(cmp=self.sortFunc)
        self.stages = stages

    def getCurrentStage(self):
        currStage = -1
        for stageInfo in self.stages:
            state, endTime = stageInfo
            if utils.getNow() < endTime:
                currStage = state
                break

        return currStage

    def sortFunc(self, stage1, stage2):
        return cmp(stage1[1], stage2[1])

    def getTime(self, cront):
        endTime = utils.getNextCrontabTime(cront)
        if endTime - utils.getNow() > 6 * const.TIME_INTERVAL_MONTH:
            endTime = utils.getPreCrontabTime(cront)
        return endTime

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshTab()
        self.refreshStageInfo()

    def refreshTab(self):
        self.widget.line0.gotoAndStop('over')
        self.widget.line1.gotoAndStop('over')
        for i in xrange(STAGE_NUM):
            if i >= len(self.stages):
                break
            stage, endTime = self.stages[i]
            stageInfo = WWTD.data.get(stage, {})
            stageMc = self.widget.getChildByName('stage%d' % i)
            btnMcName = 'btn'
            if stage == self.getCurrentStage():
                stageMc.gotoAndStop('current')
                if i < 2:
                    lineMc = self.widget.getChildByName('line%d' % i)
                    if lineMc:
                        lineMc.gotoAndStop('normal')
                btnMcName = 'btn'
            elif endTime < utils.getNow():
                stageMc.gotoAndStop('over')
                btnMcName = 'btn2'
            else:
                stageMc.gotoAndStop('next')
                btnMcName = 'btn1'
            btnMc = stageMc.getChildByName(btnMcName)
            btnMc.selected = stage == self.currentStage
            btnMc.label = stageInfo.get('title', '')
            btnMc.addEventListener(events.BUTTON_CLICK, self.onStageBtnClick)
            btnMc.stageId = stage

        self.widget.preBtn.addEventListener(events.BUTTON_CLICK, self.onPreBtnClick)
        self.widget.lastBtn.addEventListener(events.BUTTON_CLICK, self.onLastBtnClick)
        index = self.getCurrIdx()
        self.widget.preBtn.enabled = index != 0
        self.widget.lastBtn.enabled = index != 2

    def getCurrIdx(self):
        index = -1
        for sInfo in self.stages:
            index += 1
            stage, _ = sInfo
            if stage == self.currentStage:
                break

        return index

    def onPreBtnClick(self, *args):
        index = self.getCurrIdx()
        if index > 0:
            newIdx = index - 1
            self.currentStage = self.stages[newIdx][0]
            self.refreshInfo()

    def onLastBtnClick(self, *args):
        index = self.getCurrIdx()
        if index >= 0 and index < 2:
            newIdx = index + 1
            self.currentStage = self.stages[newIdx][0]
            self.refreshInfo()

    def refreshStageInfo(self):
        p = BigWorld.player()
        stage = self.currentStage
        index = self.getCurrIdx()
        endTime = self.getTime(self.stage2CrontStr[stage])
        self.widget.bg.gotoAndStop('stage%d' % index)
        stageInfo = WWTD.data.get(self.currentStage, {})
        rewardId = stageInfo.get('rewardId', 0)
        self.widget.rewardBtn.addEventListener(events.BUTTON_CLICK, self.onRewardBtnClick)
        self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick)
        self.widget.title.text = stageInfo.get('title', '')
        self.widget.desc.htmlText = stageInfo.get('desc', '')
        self.widget.detail.htmlText = stageInfo.get('detail', '')
        if rewardId:
            self.widget.rewardBtn.visible = True
        else:
            self.widget.rewardBtn.visible = False
        self.widget.endTime.htmlText = gameStrings.WING_WORLD_TREND_TIME % (utils.getMonthInt(endTime), utils.getMonthDayInt(endTime))
        self.widget.camp0Win.visible = False
        self.widget.camp1Win.visible = False
        self.widget.camp2Win.visible = False
        self.widget.score1.text = ''
        self.widget.score2.text = ''
        completeCamps = self.getCompleteCampIds(stage)
        if stage == self.getCurrentStage():
            self.widget.stageState.htmlText = gameStrings.TEXT_WINGWORLDCAMPTRENDPROXY_185
            groupId = RSCD.data.get(BigWorld.player().getOriginHostId(), {}).get('wingWorldGroupId', 0)
            score1 = p.wingWorld.country.getCamp(gametypes.WING_WORLD_WAR_CAMP_WHITE).getCityScore(groupId, True)
            score2 = p.wingWorld.country.getCamp(gametypes.WING_WORLD_WAR_CAMP_BLACK).getCityScore(groupId, True)
            self.widget.score1.text = score1
            self.widget.score2.text = score2
        elif endTime < utils.getNow():
            self.widget.stageState.htmlText = gameStrings.TEXT_WINGWORLDCAMPTRENDPROXY_192
            if completeCamps:
                if gametypes.WING_WORLD_WAR_CAMP_WHITE in completeCamps:
                    if gametypes.WING_WORLD_WAR_CAMP_BLACK not in completeCamps:
                        self.widget.camp1Win.visible = True
                    else:
                        self.widget.camp0Win.visible = True
                elif gametypes.WING_WORLD_WAR_CAMP_BLACK in completeCamps:
                    self.widget.camp2Win.visible = True
        else:
            self.widget.stageState.htmlText = gameStrings.TEXT_WINGWORLDCAMPTRENDPROXY_202

    def getCompleteCampIds(self, trendId):
        campIds = []
        for campId in gametypes.WING_WORLD_CAMPS:
            campVal = BigWorld.player().wingWorld.country.getCamp(campId)
            if trendId in campVal.trendIds:
                campIds.append(campId)

        return campIds

    def getTrendDropdownKey(self):
        if not self.stages:
            self.initStageInfo()
        currStage = self.getCurrentStage()
        if currStage < 0:
            currStage = self.stages[0][0]
        index = -1
        for sInfo in self.stages:
            index += 1
            stage, _ = sInfo
            if stage == currStage:
                break

        if index == -1:
            return index
        return index + 1

    def onRankBtnClick(self, *args):
        index = self.getCurrIdx()
        self.tempRankKey = index + 1
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_WING_WORLD_SEASON_CONTRI, customDropdownKey=index + 1)

    def onRewardBtnClick(self, *args):
        rewardId = WWTD.data.get(self.currentStage, {}).get('rewardId', 0)
        if rewardId:
            gameglobal.rds.ui.generalReward.show(rewardId)

    def onStageBtnClick(self, *args):
        e = ASObject(args[3][0])
        stage = e.currentTarget.stageId
        self.currentStage = stage
        self.refreshInfo()
