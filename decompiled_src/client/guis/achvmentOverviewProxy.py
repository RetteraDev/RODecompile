#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/achvmentOverviewProxy.o
import BigWorld
import gameglobal
import tipUtils
import clientUtils
import formula
from guis import uiConst
from guis import events
from guis import uiUtils
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import achievement_point_lv_data as APLD
from data import achievement_data as AD
from data import achievement_class_data as ACD
from data import achieve_chunkname_relation_data as ACRD
from data import achieve_spaceno_relation_data as ASRD
from data import activities_weekly_data as AWD
from data import stats_target_data as STD
SUB_TAB_WEEKLY = 0
SUB_TAB_OVERVIEW = 1
SUB_TAB_ALMOSTDONE = 2
SUB_TAB_CHUNKACHV = 3
MAIN_STAGE_TYPE = 0
MIN_STAGE_IDX = 1
COLUMN_NUM_OVERVIEW = 4
COLUMN_NUM_COMMON = 2
MAX_COMMON_ITEM_SHOW = 8
AWARD_ICON_X_OFFSET = 10
COLOR_UNACHIEVE = '#969696'
COLOR_ACHIEVED = '#ffc961'
EXPAND_NONE = 0
EXPAND_NONE_SHOW_PROGRESS = 1
CLASS_BG_PATH = 'achieve/%d.dds'
TITLE_ICON_PATH = 'achvment/110/%d.dds'
TAB_FOUR_BTN_XPOS = [26,
 150,
 274,
 398]
TAB_THREE_BTN_XPOS = [0,
 26,
 150,
 274]

class AchvmentOverviewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(AchvmentOverviewProxy, self).__init__(uiAdapter)
        self.weeklyInfo = {}
        self.version = -1
        self.reset()

    def reset(self):
        self.widget = None
        self.startTabIdx = 0
        self.currentSubTab = -1
        self.oldSelSubTab = -1
        self.achieves = {}
        self.achieveFilterData = {}
        self.classProgress = {}
        self.hasProgressAchieves = {}

    def clearAll(self):
        self.weeklyInfo = {}
        self.version = -1

    def initPanel(self, widget):
        BigWorld.player().getActivitiesWeeklyAwardInfo()
        self.widget = widget.mainMc
        self.initData()
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.subTabBtns = []
        self.subTabPanel = []

    def initUI(self):
        self.initSubTab()
        self.widget.stageAwardBtn.addEventListener(events.BUTTON_CLICK, self.onStageAwardBtnClick, False, 0, True)

    def initData(self):
        self.achieves = gameglobal.rds.ui.achvment.achieves
        self.achieveFilterData = gameglobal.rds.ui.achvment.achieveFilterData
        self.classProgress = gameglobal.rds.ui.achvment.classProgress
        self.hasProgressAchieves = self.genHasProgressAchieves()

    def genHasProgressAchieves(self):
        return {achieveId:info for achieveId, info in self.achieveFilterData.iteritems() if info.get('expandType', EXPAND_NONE) == EXPAND_NONE_SHOW_PROGRESS}

    def refreshInfo(self):
        self.refreshAchievePoint()
        self.refreshTab(self.currentSubTab)

    def refreshAchievePoint(self):
        currentPoint, maxPoint = gameglobal.rds.ui.achvment.getAchievementPoint()
        stage = self.getCurrentPointStage(currentPoint)
        self.widget.titleMc.gotoAndStop('a%d' % stage)
        self.widget.titleIcon.fitSize = True
        titleIconId = APLD.data.get((MAIN_STAGE_TYPE, stage), {}).get('rewardTitleIcon', 0)
        self.widget.titleIcon.loadImage(TITLE_ICON_PATH % titleIconId)
        nextStageCeilPoint = APLD.data.get((MAIN_STAGE_TYPE, stage + 1), {}).get('achievePointRange', 1)
        self.widget.achieveNumTf.text = currentPoint
        self.widget.achieveProgressbar.currentValue = currentPoint * 100.0 / int(nextStageCeilPoint)

    def getCurrentPointStage(self, currentPoint):
        mainStages = {k[1]:v.get('achievePointRange', 0) for k, v in APLD.data.iteritems() if k[0] == MAIN_STAGE_TYPE}
        sortedData = sorted(mainStages.iteritems(), key=lambda d: int(d[1]), reverse=True)
        for stageIdx, stageFloor in sortedData:
            if currentPoint >= int(stageFloor):
                return stageIdx

        return MIN_STAGE_IDX

    def initSubTab(self):
        self.widget.overviewTabBtn.addEventListener(events.BUTTON_CLICK, self.onOverviewTabBtnClick, False, 0, True)
        self.widget.almostDoneTabBtn.addEventListener(events.BUTTON_CLICK, self.onAlmostDoneTabBtnClick, False, 0, True)
        self.widget.chunkAchvTabBtn.addEventListener(events.BUTTON_CLICK, self.onChunkAchvTabBtnClick, False, 0, True)
        self.widget.weeklyTabBtn.addEventListener(events.BUTTON_CLICK, self.onWeeklyTabBtnClick, False, 0, True)
        self.subTabBtns = {SUB_TAB_OVERVIEW: self.widget.overviewTabBtn,
         SUB_TAB_ALMOSTDONE: self.widget.almostDoneTabBtn,
         SUB_TAB_CHUNKACHV: self.widget.chunkAchvTabBtn}
        self.subTabPanel = {SUB_TAB_OVERVIEW: self.widget.overviewPanel,
         SUB_TAB_ALMOSTDONE: self.widget.almostDonePanel,
         SUB_TAB_CHUNKACHV: self.widget.chunkAchvPanel}
        if self.checkWeeklyPanelShow():
            self.subTabBtns[SUB_TAB_WEEKLY] = self.widget.weeklyTabBtn
            self.subTabPanel[SUB_TAB_WEEKLY] = self.widget.weeklyPanel
            self.widget.weeklyTabBtn.visible = True
            self.widget.weeklyPanel.visible = True
            self.startTabIdx = 0
            for idx, btn in self.subTabBtns.iteritems():
                btn.x = TAB_FOUR_BTN_XPOS[idx]

        else:
            self.widget.weeklyTabBtn.visible = False
            self.widget.weeklyPanel.visible = False
            self.startTabIdx = SUB_TAB_OVERVIEW
            for idx, btn in self.subTabBtns.iteritems():
                btn.x = TAB_THREE_BTN_XPOS[idx]

        for idx, panel in self.subTabPanel.iteritems():
            panel.visible = bool(self.currentSubTab == idx)

        self.selectSubTab(self.currentSubTab)

    def checkWeeklyPanelShow(self):
        isEnable = gameglobal.rds.configData.get('activitiesWeeklyReward', False)
        mileStoneId = SCD.data.get('mileStoneForActivitiesWeeklyEnable', 10003)
        return BigWorld.player().checkServerProgress(mileStoneId, False) and isEnable

    def selectSubTab(self, idx):
        if idx < self.startTabIdx or idx > len(self.subTabPanel):
            idx = self.startTabIdx
        if idx == self.currentSubTab:
            return
        self.currentSubTab = idx
        self.subTabBtns[self.currentSubTab].selected = True
        self.subTabPanel[self.currentSubTab].visible = True
        if self.startTabIdx <= self.oldSelSubTab <= len(self.subTabPanel):
            self.subTabBtns[self.oldSelSubTab].selected = False
            self.subTabPanel[self.oldSelSubTab].visible = False
        self.oldSelSubTab = self.currentSubTab

    def refreshTab(self, tabIdx):
        if tabIdx < self.startTabIdx or tabIdx > len(self.subTabPanel):
            tabIdx = self.startTabIdx
        if tabIdx == SUB_TAB_OVERVIEW:
            self.refreshOverviewTab(tabIdx)
        elif tabIdx == SUB_TAB_ALMOSTDONE or tabIdx == SUB_TAB_CHUNKACHV:
            self.refreshCommonTab(tabIdx)
        elif tabIdx == SUB_TAB_WEEKLY:
            self.refreshWeeklyTab(tabIdx)

    def refreshOverviewTab(self, tabIdx):
        listData = self.getTabData(tabIdx)
        mainMc = self.subTabPanel[tabIdx]
        mainMc.achieveTf.text = gameStrings.ACHIEVEMENT_ACHIEVED_TEXT % len(self.achieves)
        mainMc.achieveProgressTf.text = gameStrings.ACHIEVEMENT_ACHIEVED_PROGRESS_TEXT % (100.0 * len(self.achieves) / len(self.achieveFilterData))
        mainMc.listView.itemHeight = 80
        mainMc.listView.itemWidth = 200
        mainMc.listView.column = COLUMN_NUM_OVERVIEW
        mainMc.listView.itemRenderer = 'AchvmentOverviewPanel_OverviewListItem'
        mainMc.listView.labelFunction = self.overviewListLabelFunc
        mainMc.listView.dataArray = listData
        mainMc.listView.validateNow()

    def refreshCommonTab(self, tabIdx):
        listData = self.getTabData(tabIdx)
        mainMc = self.subTabPanel[tabIdx]
        mainMc.column = COLUMN_NUM_COMMON
        mainMc.itemRenderer = 'AchvmentOverviewPanel_CommonItem'
        mainMc.labelFunction = self.commonLabelFunc
        mainMc.dataArray = listData
        mainMc.validateNow()

    def refreshWeeklyTab(self, tabIdx):
        mainMc = self.widget.weeklyPanel
        mainMc.hintTf.htmlText = SCD.data.get('AchievementWeekly_HintText', 'AchievementWeekly_HintText')
        mainMc.mc0.visible = False
        mainMc.mc1.visible = False
        mainMc.mc2.visible = False
        for idx, key in enumerate(self.weeklyInfo.iterkeys()):
            mc = getattr(mainMc, 'mc%d' % idx, None)
            mc and self.refreshWeeklyMc(mc, key)

    def refreshWeeklyMc(self, mc, key):
        data = AWD.data.get(key, {})
        bonusId = data.get('bonusId', 0)
        achieveId = data.get('achievementId', 0)
        name = data.get('name', '')
        info = self.weeklyInfo.get(key)
        isActivityDone = info.get('isDone', False)
        isGotReward = info.get('rewardInfo', False)
        mc.visible = True
        cupMc = mc.cupMc
        cupMc.achieveId = achieveId
        cupMc.gotoAndStop('achieved' if isActivityDone else 'unachieve')
        cupMc.nameTf.text = name
        cupMc.stateTf.text = gameStrings.ACHVMENT_WEEKLY_DONE if isActivityDone else '%d/%d' % (info.get('curCnt', 0), info.get('finishCnt', 0))
        cupMc.addEventListener(events.MOUSE_CLICK, self.onWeeklyPanelCupClick, False, 0, True)
        TipManager.addTip(cupMc, gameStrings.ACHVMENT_WEEKLY_TIP)
        slot = mc.slot
        rewardItems = clientUtils.genItemBonus(bonusId)
        if rewardItems:
            itemId, cnt = rewardItems[0]
            state = uiConst.ITEM_NORMAL if isActivityDone else uiConst.ITEM_GRAY
            slot.dragable = False
            slot.setItemSlotData(uiUtils.getGfxItemById(itemId, cnt, appendInfo={'state': state}))
        btn = mc.btn
        btn.enabled = isActivityDone and not isGotReward
        btn.key = key
        btn.addEventListener(events.MOUSE_CLICK, self.onWeeklyPanelBtnClick, False, 0, True)
        btn.label = gameStrings.ACHVMENT_WEEKLY_AWARD_ALREADYGOT if isGotReward else gameStrings.ACHVMENT_WEEKLY_AWARD_GET

    def updateActivitiesWeeklyAwardInfo(self, info, version):
        if self.version != version:
            self.weeklyInfo = {}
        self.version = version
        for key, value in info.iteritems():
            self.weeklyInfo.setdefault(key, {})
            if value:
                self.weeklyInfo[key].update(value)
                self.weeklyInfo[key]['isDone'] = True
            else:
                self.weeklyInfo[key]['isDone'] = False

        BigWorld.player().getActivityStats()
        if not self.widget:
            return
        if self.currentSubTab == SUB_TAB_WEEKLY:
            self.refreshTab(self.currentSubTab)

    def updateActivityStats(self, statsInfo):
        for key, info in self.weeklyInfo.iteritems():
            statIds = AWD.data.get(key, {}).get('statIds', ())
            if not statIds:
                continue
            statId = statIds[0]
            data = STD.data.get(statId, {})
            prop = data.get('property')
            info['curCnt'] = statsInfo.get(prop, 0)
            info['finishCnt'] = data.get('finishNum', 0)

        if not self.widget:
            return
        if self.currentSubTab == SUB_TAB_WEEKLY:
            self.refreshTab(self.currentSubTab)

    def getTabData(self, tabIdx):
        if tabIdx == SUB_TAB_OVERVIEW:
            return self.genOverviewData()
        if tabIdx == SUB_TAB_ALMOSTDONE:
            return self.genAlmostDoneData()
        if tabIdx == SUB_TAB_CHUNKACHV:
            return self.genChunkAchvData()
        if tabIdx == SUB_TAB_WEEKLY:
            return self.weeklyInfo
        return ()

    def genOverviewData(self):
        return sorted(ACD.data.iterkeys())

    def genAlmostDoneData(self):
        progressRet = {}
        for achieveId, info in self.hasProgressAchieves.iteritems():
            if achieveId in self.achieves:
                continue
            achieveCnt, totalCnt = gameglobal.rds.ui.achvment.getAchieveProgress(achieveId)
            if not achieveCnt:
                continue
            progressRet[achieveId] = achieveCnt * 1.0 / totalCnt

        ret = sorted(progressRet.iterkeys(), key=lambda aId: progressRet[aId], reverse=True)
        if len(ret) > MAX_COMMON_ITEM_SHOW:
            return ret[:MAX_COMMON_ITEM_SHOW]
        return ret

    def genChunkAchvData(self):
        p = BigWorld.player()
        chunkName = BigWorld.ChunkInfoAt(p.position)
        if chunkName in ACRD.data:
            ret = sorted(ACRD.data.get(chunkName, ()))
        else:
            mapId = formula.getMapId(p.spaceNo)
            ret = sorted(ASRD.data.get(mapId, ()))
        return [ achieveId for achieveId in ret if achieveId not in self.achieves ]

    def overviewListLabelFunc(self, *args):
        item = ASObject(args[3][1])
        classId = int(args[3][0].GetNumber())
        item.classId = classId
        ASUtils.setHitTestDisable(item.nameTf, True)
        ASUtils.setHitTestDisable(item.progressTf, True)
        ASUtils.setHitTestDisable(item.progressbar, True)
        item.nameTf.text = ACD.data.get(classId, {}).get('name')
        achieveCnt, totalCnt = self.classProgress.get(classId, (0, 0))
        item.progressTf.text = '%d/%d' % (achieveCnt, totalCnt)
        item.progressbar.currentValue = achieveCnt
        item.progressbar.maxValue = totalCnt
        item.addEventListener(events.MOUSE_CLICK, self.onClassifyItemClick, False, 0, True)
        item.bg.bg.fitSize = True
        item.bg.bg.loadImage(CLASS_BG_PATH % ACD.data.get(classId, {}).get('newIcon', 1))

    def commonLabelFunc(self, *args):
        item = ASObject(args[3][1])
        achieveId = int(args[3][0].GetNumber())
        item.achieveId = achieveId
        data = AD.data.get(achieveId, {})
        ASUtils.setHitTestDisable(item.nameTf, True)
        ASUtils.setHitTestDisable(item.descTf, True)
        ASUtils.setHitTestDisable(item.icon, True)
        ASUtils.setHitTestDisable(item.progressMc, True)
        item.nameTf.text = data.get('name')
        item.descTf.text = data.get('desc')
        rewardTitle = data.get('rewardTitle')
        bonusId = data.get('bonusId')
        hasAward = bool(rewardTitle or bonusId)
        item.awardMc.visible = hasAward
        if hasAward:
            item.awardMc.x = item.nameTf.x + item.nameTf.textWidth + AWARD_ICON_X_OFFSET
            awardText = gameglobal.rds.ui.achvment.getAwardString(rewardTitle, bonusId)
            TipManager.addTip(item.awardMc, awardText, tipUtils.TYPE_DEFAULT_BLACK)
        expandType = data.get('expandType', EXPAND_NONE)
        isAchieved = bool(achieveId in self.achieves)
        item.icon.gotoAndStop(str(isAchieved))
        color = COLOR_ACHIEVED if isAchieved else COLOR_UNACHIEVE
        item.progressMc.achievePointTf.htmlText = uiUtils.toHtml(data.get('rewardPoint', 0), color)
        item.progressMc.achievedTf.visible = isAchieved
        item.progressMc.progressTf.visible = not isAchieved and expandType == EXPAND_NONE_SHOW_PROGRESS
        if expandType == EXPAND_NONE_SHOW_PROGRESS and not isAchieved:
            achieveCnt, totalCnt = gameglobal.rds.ui.achvment.getAchieveProgress(achieveId)
            item.progressMc.progressTf.text = '%d/%d' % (achieveCnt, totalCnt)
            item.progressMc.currentValue = achieveCnt * 100.0 / totalCnt
        else:
            item.progressMc.currentValue = 100 * int(isAchieved)
        item.addEventListener(events.MOUSE_CLICK, self.onAchieveItemClick, False, 0, True)

    def onClassifyItemClick(self, *args):
        e = ASObject(args[3][0])
        classId = e.currentTarget.classId
        subClassIdInfos = ACD.data.get(classId, {}).get('newvalue', ())
        subClassId = sorted(subClassIdInfos.keys())[0]
        gameglobal.rds.ui.achvment.link2AchvmentDetailView(subClassId=subClassId)

    def onAchieveItemClick(self, *args):
        e = ASObject(args[3][0])
        achieveId = e.currentTarget.achieveId
        gameglobal.rds.ui.achvment.link2AchvmentDetailView(achieveId=achieveId)

    def onOverviewTabBtnClick(self, *args):
        self.selectSubTab(SUB_TAB_OVERVIEW)
        self.refreshTab(self.currentSubTab)

    def onAlmostDoneTabBtnClick(self, *args):
        self.selectSubTab(SUB_TAB_ALMOSTDONE)
        self.refreshTab(self.currentSubTab)

    def onChunkAchvTabBtnClick(self, *args):
        self.selectSubTab(SUB_TAB_CHUNKACHV)
        self.refreshTab(self.currentSubTab)

    def onWeeklyTabBtnClick(self, *args):
        self.selectSubTab(SUB_TAB_WEEKLY)
        self.refreshTab(self.currentSubTab)

    def onStageAwardBtnClick(self, *args):
        gameglobal.rds.ui.achvmentStageAward.show()

    def onWeeklyPanelCupClick(self, *args):
        e = ASObject(args[3][0])
        achieveId = e.currentTarget.achieveId
        gameglobal.rds.ui.achvment.link2AchvmentDetailView(achieveId=achieveId)

    def onWeeklyPanelBtnClick(self, *args):
        e = ASObject(args[3][0])
        key = e.currentTarget.key
        BigWorld.player().base.getActivitiesWeeklyAward(key)
