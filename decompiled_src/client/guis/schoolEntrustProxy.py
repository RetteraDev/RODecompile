#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolEntrustProxy.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
import ui
import utils
import clientUtils
import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from asObject import Tweener
from asObject import ASUtils
from asObject import ASObject
from asObject import TipManager
from gameStrings import gameStrings
from callbackHelper import Functor
from cdata import school_entrust_reverse_data as SERD
from data import sys_config_data as SCD
from data import quest_loop_data as QLD
NORMAL_COLOR = '#174C66'
FEW_COLOR = '#451602'
SCHOOL_ENTRUST_LIST_NUM = 4
BUILD_LIST_NUM = 6
BUILD_ACCURACY = 1
DAILY_ACC_TIMES = 5
ENTRUST_NUM = 4
ENTRUST_LEFT_TIMES = 10
COMBAR_PHASE = [0,
 33,
 275,
 517,
 759,
 1000]

class SchoolEntrustProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolEntrustProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.entrustInfo = {}
        self.accTimesEffect = {}
        self.buildBarEffect = {}
        self.lightCallBack = None
        self.lightBarCallBack = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_ENTRUST, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_ENTRUST:
            self.widget = widget
            self.initUI()

    def show(self, entrustInfo):
        self.entrustInfo.update(entrustInfo)
        if self.widget:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SCHOOL_ENTRUST)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SCHOOL_ENTRUST)
        self.widget = None
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.entrustInfo = {}
        self.cancelCallBack()
        self.cancelLightCallBack()
        self.cancelLightBarCallBack()

    def initUI(self):
        self.initData()
        self.initState()

    def initData(self):
        pass

    def initState(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        p = BigWorld.player()
        self.widget.title.textField.text = SCD.data.get('schoolEntrustTitle', {}).get(p.school, '')
        self.widget.rightContent.comMc.comProgressBar.maxValue = 1000
        self.widget.rightContent.comMc.comProgressBar.currentValue = 0
        self.widget.rightContent.comMc.comProgressBar.addEventListener(events.PROCESSING_END, self.handleComProgressBarProcessingEnd, False, 0, True)
        for x in xrange(0, DAILY_ACC_TIMES):
            node = getattr(self.widget.rightContent.comMc.comProgressBar, 'node' + str(x), None)
            if node:
                node.visible = False
            lightPoint = getattr(self.widget.rightContent.comMc.comProgressBar, 'lightPoint' + str(x), None)
            if lightPoint:
                lightPoint.visible = False

        bgStr = SERD.data.get(p.school, {}).get('schoolImg', [])
        self.widget.leftContent.bgMc.gotoAndStop(bgStr)
        curBuildValue = self.entrustInfo.get('schoolScore', 0)
        buildNodeInfos = SERD.data.get(p.school, {}).get('buildNodeInfo', [])
        lastBuildValue = 0
        for x in xrange(0, BUILD_LIST_NUM):
            buildId, buildValue, buildMailId, buildTips = (0, 0, 0, '')
            if x:
                buildId, buildValue, buildMailId, buildTips, isHideValue = buildNodeInfos[x - 1]
            buildBar = getattr(self.widget.leftContent.buildBarMc, 'buildBar' + str(x), None)
            if buildBar:
                buildBar.maxValue = BUILD_ACCURACY * (buildValue - lastBuildValue)
                buildBar.currentValue = 0
            buildNode = getattr(self.widget.leftContent.buildBarMc, 'buildNode' + str(x), None)
            if buildNode:
                buildNode.visible = False
            buildValueTxt = getattr(self.widget.leftContent, 'buildValue' + str(x), None)
            if buildValueTxt:
                if isHideValue:
                    buildValueTxt.text = buildTips
                else:
                    buildValueTxt.text = ''.join((buildTips, '\n', str(buildValue))) if buildTips and buildValue else ''
            lastBuildValue = buildValue

        for x in xrange(0, SCHOOL_ENTRUST_LIST_NUM):
            entrustMc = getattr(self.widget.rightContent, 'entrustMc' + str(x), None)
            if entrustMc:
                entrustMc.idx = x
                entrustMc.addEventListener(events.MOUSE_CLICK, self.handleEntrustMcClick, False, 0, True)
                entrustMc.questPaper.icon.gotoAndStop('type' + str(x + 1))

        self.hideTroubleEffectVisible()
        self.refreshInfo()

    def refreshInfo(self, bInit = False):
        if self.hasBaseData():
            p = BigWorld.player()
            self.setResetTime()
            dailyAccTimes = SERD.data.get(p.school, {}).get('dailyAccTimes', 0)
            alreadyAccTimes = self.entrustInfo.get('acceptCount', 0)
            accTimes = dailyAccTimes - alreadyAccTimes
            self.widget.rightContent.accTimeTxt.text = accTimes
            curbuildValue = self.entrustInfo.get('schoolScore', 0)
            self.widget.leftContent.curBuidMc.buildValueTxt.text = curbuildValue
            self.widget.leftContent.curBuidMc.visible = False
            self.widget.leftContent.leftTitleTxt.htmlText = SERD.data.get(p.school, {}).get('imageTitleTxt', [])
            buildNodeInfos = SERD.data.get(p.school, {}).get('buildNodeInfo', [])
            lastBuildValue = 0
            for x in xrange(0, BUILD_LIST_NUM):
                buildId, buildValue, buildMailId, buildTips = (0, 0, 0, '')
                if x:
                    buildId, buildValue, buildMailId, buildTips, isHideValue = buildNodeInfos[x - 1]
                buildBar = getattr(self.widget.leftContent.buildBarMc, 'buildBar' + str(x), None)
                if buildBar:
                    buildBar.currentValue = BUILD_ACCURACY * (curbuildValue - lastBuildValue)
                buildNode = getattr(self.widget.leftContent.buildBarMc, 'buildNode' + str(x), None)
                if buildNode:
                    if buildBar:
                        if buildBar.currentValue >= buildBar.maxValue:
                            buildNode.visible = True
                        else:
                            buildNode.visible = False
                    else:
                        buildNode.visible = True
                lastBuildValue = buildValue

            completeCount = self.entrustInfo.get('completeCount', 0)
            acceptCount = self.entrustInfo.get('acceptCount', 0)
            self.widget.rightContent.comMc.receiveBtn.enabled = completeCount >= dailyAccTimes and not self.entrustInfo.get('rewardState', 0)
            self.widget.rightContent.comMc.receiveBtn.label = gameStrings.SCHOOL_ENTRUST_REWARD_RECEIVE if not self.entrustInfo.get('rewardState', 0) else gameStrings.SCHOOL_ENTRUST_REWARD_ALREADY
            self.accBarStartWithProgress(completeCount, False)
            itemId = SERD.data.get(p.school, {}).get('rewardItemId', 0)
            gfxItem = uiUtils.getGfxItemById(itemId, 1)
            self.widget.rightContent.comMc.comRewardSlot.setItemSlotData(gfxItem)
            self.startTroubleEffect(completeCount)
            self.updateTime()

    def updatePaperInfo(self):
        entrustQuestInfo = self.entrustInfo.get('entrustInfo', {})
        acceptTimeInfo = self.entrustInfo.get('acceptTimeInfo', [0,
         0,
         0,
         0])
        for x in xrange(0, SCHOOL_ENTRUST_LIST_NUM):
            entrustMc = getattr(self.widget.rightContent, 'entrustMc' + str(x), None)
            if entrustMc:
                qLvInfo = entrustQuestInfo.get(x + 1, [])
                leftTimes = len(qLvInfo)
                if leftTimes > 0:
                    entrustMc.gotoAndStop('has')
                    qInfo = qLvInfo[0]
                    questLoopId = qInfo.get('questLoopId', 0)
                    entrustMc.qId = questLoopId
                    entrustMc.eId = qInfo.get('entrustId', 0)
                    lastAccTime = acceptTimeInfo[x]
                    qData = QLD.data.get(questLoopId, {})
                    accCd = qData.get('schoolEntrustAccCD', 0)
                    entrustMc.questPaper.questTitle.text = qData.get('name', '')
                    color = NORMAL_COLOR if leftTimes >= ENTRUST_LEFT_TIMES else FEW_COLOR
                    leftStr = gameStrings.SCHOOL_ENTRUST_LEFT_NUM_TEXT % leftTimes
                    entrustMc.questPaper.reaminTimes.htmlText = uiUtils.toHtml(leftStr, color)
                    iconType = qData.get('entrustIcon', 1)
                    starLv = qData.get('entrustStarLv', 1)
                    entrustMc.questPaper.starLv.gotoAndStop('star' + str(starLv))
                    entrustMc.questPaper.icon.gotoAndStop('type' + str(iconType))
                    passTime = utils.getNow() - lastAccTime
                    if lastAccTime and passTime < accCd:
                        entrustMc.questPaper.buildvalue.gotoAndStop('cd')
                        cdTime = uiUtils.formatTime(accCd - passTime)
                        entrustMc.questPaper.buildvalue.cdTime.text = gameStrings.SCHOOL_ENTRUST_ACC_CD_TEXT % cdTime
                    else:
                        entrustMc.questPaper.buildvalue.gotoAndStop('nocd')
                        entrustMc.questPaper.buildvalue.addValue.text = '+' + str(qData.get('buildValue', 0))
                else:
                    entrustMc.gotoAndStop('empty')

    def accBarStartWithProgress(self, phase, isProcessing):
        if self.widget.rightContent.comMc.comProgressBar.currentValue != COMBAR_PHASE[phase]:
            self.widget.rightContent.comMc.comProgressBar.currentValue = COMBAR_PHASE[phase]
            if isProcessing:
                self.widget.rightContent.comMc.comProgressBar.isProcessing = True
                self.widget.rightContent.comMc.comProgressBar.addEventListener(events.EVENT_ENTER_FRAME, self.handleComProgressBarEnterFrame, False, 0, True)
                self.accTimesEffect[phase] = True
            else:
                self.widget.rightContent.comMc.comProgressBar.isProcessing = False
                self.setComProgress(COMBAR_PHASE[phase])

    def cancelCallBack(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def updateTime(self):
        if self.hasBaseData():
            p = BigWorld.player()
            self.setResetTime()
            self.updatePaperInfo()
            self.cancelCallBack()
            self.timer = BigWorld.callback(1, self.updateTime)
        else:
            self.cancelCallBack()

    def setResetTime(self):
        lastDailyRefreshTime = self.entrustInfo.get('lastDailyRefreshTime', 0)
        if not lastDailyRefreshTime:
            self.widget.rightContent.resetTime.visible = False
        else:
            self.widget.rightContent.resetTime.visible = True
            nowTime = utils.getNow()
            dailyRefreshCrontab = SCD.data.get('schoolEntrustDailyRefreshCrontab', '10 0,2,4,6,8,10,12,14,16,17,18,19,20,22 * * *')
            nextTime = utils.getNextCrontabTime(dailyRefreshCrontab)
            self.widget.rightContent.resetTime.text = gameStrings.SCHOOL_ENTRUST_RESET_DESC % uiUtils.formatTime(nextTime - nowTime)

    def hasBaseData(self):
        if self.widget:
            return True
        else:
            return False

    def openSchoolEntrust(self):
        p = BigWorld.player()
        p.cell.querySchoolEntrustInfo()

    @ui.callFilter(5)
    def _onRefreshBtnClick(self, e):
        p = BigWorld.player()
        p.cell.refreshSchoolEntrustInfo()

    def _onReceiveBtnClick(self, e):
        p = BigWorld.player()
        p.cell.getSchoolEntrustReward()

    def handleEntrustMcClick(self, *arg):
        e = ASObject(arg[3][0])
        t = e.currentTarget
        gameglobal.rds.ui.schoolEntrustBuild.show(t.qId, t.eId, t.idx + 1)

    def handleComProgressBarEnterFrame(self, *arg):
        gamelog.debug('@zq handleComProgressBarEnterFrame')
        if self.hasBaseData():
            self.setComProgress(self.widget.rightContent.comMc.comProgressBar.currentValue)

    def setComProgress(self, value):
        for i, v in enumerate(COMBAR_PHASE):
            node = getattr(self.widget.rightContent.comMc.comProgressBar, 'node' + str(i - 1), None)
            if node:
                if self.widget.rightContent.comMc.comProgressBar.processingValue >= v:
                    node.visible = True
                else:
                    node.visible = False

    def handleComProgressBarProcessingEnd(self, *arg):
        if self.hasBaseData():
            self.widget.rightContent.comMc.comProgressBar.removeEventListener(events.EVENT_ENTER_FRAME, self.handleComProgressBarEnterFrame)
            self.setComProgress(self.widget.rightContent.comMc.comProgressBar.currentValue)
            self.widget.rightContent.comMc.comProgressBar.isProcessing = False

    def startTroubleEffect(self, phase):
        if phase and self.hasBaseData() and not self.buildBarEffect.get(phase, None):
            self.widget.rightContent.comMc.comProgressBar.lightBar.visible = True
            lightPoint = getattr(self.widget.rightContent.comMc.comProgressBar, 'lightPoint' + str(phase - 1), None)
            node = getattr(self.widget.rightContent.comMc.comProgressBar, 'node' + str(phase - 1), None)
            self.widget.rightContent.comMc.comProgressBar.lightBar.gotoAndPlay(0)
            if lightPoint:
                lightPoint.visible = True
                lightPoint.gotoAndPlay(0)
            self.widget.lightMc.visible = True
            if node:
                _x, _y = ASUtils.local2Global(node, 0, 0)
                _x, _y = ASUtils.global2Local(self.widget, _x, _y)
                self.widget.lightMc.gotoAndPlay('light')
                self.widget.lightMc.x = _x
                self.widget.lightMc.y = _y
                buildNode = getattr(self.widget.leftContent.buildBarMc, 'buildNode0', None)
                if buildNode:
                    tx, ty = ASUtils.local2Global(buildNode, 0, 0)
                    tx, ty = ASUtils.global2Local(self.widget, tx, ty)
                    Tweener.addTween(self.widget.lightMc, {'x': tx,
                     'y': ty,
                     'time': 0.7,
                     'transition': 'easeinsine',
                     'onComplete': self.flyCompleted})
            self.buildBarEffect[phase] = True

    def hideTroubleEffectVisible(self):
        if self.hasBaseData():
            self.widget.lightMc.visible = False
            self.widget.leftContent.buildBarMc.beginLightMc.visible = False
            self.widget.leftContent.buildBarMc.lightBar.visible = False
            for x in xrange(0, DAILY_ACC_TIMES):
                lightPoint = getattr(self.widget.rightContent.comMc.comProgressBar, 'lightPoint' + str(x), None)
                if lightPoint:
                    lightPoint.visible = False

    def flyCompleted(self, *arg):
        if self.hasBaseData():
            self.widget.lightMc.gotoAndPlay('boom')
            self.widget.leftContent.buildBarMc.beginLightMc.visible = True
            self.widget.leftContent.buildBarMc.beginLightMc.gotoAndPlay(0)
            self.cancelLightCallBack()
            self.lightCallBack = ASUtils.callbackAtFrame(self.widget.leftContent.buildBarMc.beginLightMc, 15, self.lightBarCB)

    def lightBarCB(self, *arg):
        if self.hasBaseData():
            self.widget.leftContent.buildBarMc.lightBar.visible = True
            self.widget.leftContent.buildBarMc.lightBar.gotoAndPlay(0)
            self.lightBarCallBack = ASUtils.callbackAtFrame(self.widget.leftContent.buildBarMc.lightBar, 15, self.finalEffectCB)

    def cancelLightCallBack(self):
        if self.lightCallBack:
            ASUtils.cancelCallBack(self.lightCallBack)
            self.lightCallBack = None

    def cancelLightBarCallBack(self):
        if self.lightBarCallBack:
            ASUtils.cancelCallBack(self.lightBarCallBack)
            self.lightBarCallBack = None

    def finalEffectCB(self, *arg):
        if self.hasBaseData():
            self.hideTroubleEffectVisible()
