#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yunChuiQuizzesPushProxy.o
import BigWorld
import uiConst
import events
import utils
import gamelog
import gameglobal
from gamestrings import gameStrings
from guis.asObject import ASUtils
from uiProxy import UIProxy
from callbackHelper import Functor
ACTIVITY_CLOSE = 0
ACTIVITY_APPLY = 1
ACTIVITY_PREPARE = 2
ACTIVITY_START = 3
ACTIVITY_ROUND_END = 4
ACTIVITY_END = 5
from data import quizzes_config_data as QCD

class YunChuiQuizzesPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YunChuiQuizzesPushProxy, self).__init__(uiAdapter)
        self.timer = 0
        self.widget = None
        self.reset()

    def reset(self):
        self.activityState = 0
        self.nextStageTimestamp = 0
        self.curActivityId = 0
        self.curRound = 0
        self.successNum = 0

    def clearAll(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_YUNCHUI_QUIZZES_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_YUNCHUI_QUIZZES_PUSH)

    def setCurActivityId(self, curActivityId):
        self.curActivityId = curActivityId
        if self.widget:
            self.widget.hintEff.visible = True
            self.widget.hintEff.gotoAndPlay(1)
        if self.activityState == ACTIVITY_CLOSE or self.activityState == ACTIVITY_APPLY:
            self.hide()
        else:
            self.show()

    def getActivityId(self):
        return self.curActivityId

    def setCurRound(self, curRound):
        if self.widget:
            self.widget.hintEff.visible = True
            self.widget.hintEff.gotoAndPlay(1)
        self.curRound = curRound

    def setActivityState(self, activityState, nextStageTimestamp):
        BigWorld.player().base.queryQuizzesActivityId()
        self.activityState = activityState
        self.nextStageTimestamp = nextStageTimestamp

    def show(self):
        if not gameglobal.rds.configData.get('enableQuizzes', False):
            return
        if self.curActivityId and not self.widget:
            self.timer = 0
            self.uiAdapter.loadWidget(uiConst.WIDGET_YUNCHUI_QUIZZES_PUSH)

    def initUI(self):
        ASUtils.setHitTestDisable(self.widget.hintEff, True)
        ASUtils.setHitTestDisable(self.widget.pushIcon.touMing, True)
        self.widget.hintEff.visible = False
        self.widget.pushIcon.tipsText.gotoAndPlay('on')
        self.widget.pushIcon.expandBtn.visible = False
        self.widget.pushIcon.tipsText.textMc.closeBtn.addEventListener(events.MOUSE_CLICK, self.onCloseTipClick, False, 0, True)
        self.widget.pushIcon.expandBtn.addEventListener(events.MOUSE_CLICK, self.onExpandTipClick, False, 0, True)
        self.widget.pushIcon.icon.addEventListener(events.MOUSE_CLICK, self.onOpenQuiz, False, 0, True)
        self.widget.pushIcon.endBtn.addEventListener(events.MOUSE_CLICK, self.onOpenQuiz, False, 0, True)
        self.widget.pushIcon.prepareBtn.addEventListener(events.MOUSE_CLICK, self.onOpenQuiz, False, 0, True)
        self.widget.pushIcon.countdown.visible = True
        data = QCD.data.get(self.curActivityId, {})
        intervalStart = self.nextStageTimestamp - utils.getNow()
        self.countdown(intervalStart)
        ASUtils.callbackAtFrame(self.widget.pushIcon, 10, self.setEffectHitTestEnable)

    def setEffectHitTestEnable(self, *args):
        if not self.widget or self.widget.pushIcon.bgEff:
            return
        ASUtils.setHitTestDisable(self.widget.pushIcon.bgEff, True)

    def onCloseTipClick(self, *args):
        self.widget.pushIcon.tipsText.gotoAndPlay('off')
        self.widget.pushIcon.expandBtn.visible = True

    def onExpandTipClick(self, *args):
        self.widget.pushIcon.tipsText.gotoAndPlay('on')
        self.widget.pushIcon.expandBtn.visible = False
        self.widget.pushIcon.tipsText.textMc.desc.htmlText = self.getData()[1]

    def onOpenQuiz(self, *args):
        self.widget.hintEff.visible = False
        self.widget.hintEff.gotoAndStop(1)
        BigWorld.player().base.queryQuizzesInfo()

    def onOpenQuizResult(self, *args):
        BigWorld.player().base.queryQuizzesOverInfo()

    def getData(self):
        timeStr, scoreStr = (0, 0)
        data = QCD.data.get(self.curActivityId, {})
        intervalJoin = data.get('intervalJoin')
        intervalStart = data.get('intervalStart')
        applyEndTime = utils.getPreCrontabTime(data.get('beginDate')) + intervalJoin + intervalStart
        now = utils.getNow()
        if self.activityState == ACTIVITY_PREPARE:
            beginTimeTxt = utils.formatTimeEx(utils.getDisposableCronTabTimeStamp(data.get('beginDate')) + intervalStart + intervalJoin)[0:5]
            scoreStr = gameStrings.YUNCHUI_QUIZZES_STARTTIME % beginTimeTxt
        else:
            timeStr = utils.formatTimeStr(0, 'm:s', True, 2, 2)
            if self.activityState == ACTIVITY_START or self.activityState == ACTIVITY_ROUND_END:
                if self.curRound:
                    scoreStr = gameStrings.YUNCHUI_QUIZZES_PUSH_QUES_NUM % self.curRound
            if self.activityState == ACTIVITY_END:
                scoreStr = gameStrings.YUNCHUI_QUIZZES_PUSH_SUCCESS_NUM % self.successNum
        return (timeStr, scoreStr)

    def refreshInfo(self):
        if not self.widget:
            return
        _, scoreStr = self.getData()
        if self.activityState == ACTIVITY_CLOSE:
            self.hide()
            return
        self.widget.pushIcon.countdown.visible = self.activityState == ACTIVITY_PREPARE
        self.widget.pushIcon.endBtn.visible = self.activityState == ACTIVITY_END
        self.widget.pushIcon.icon.visible = self.activityState == ACTIVITY_START or self.activityState == ACTIVITY_ROUND_END
        self.widget.pushIcon.prepareBtn.visible = self.activityState == ACTIVITY_PREPARE
        if not scoreStr:
            self.widget.pushIcon.tipsText.visible = False
        else:
            self.widget.pushIcon.tipsText.visible = True
            self.widget.pushIcon.tipsText.textMc.desc.htmlText = scoreStr
        BigWorld.callback(0.5, self.refreshInfo)

    def countdown(self, leftTime):
        if not self.widget:
            return
        if leftTime > 0:
            timeStr = utils.formatTimeStr(leftTime, 'm:s', True, 2, 2)
            self.widget.pushIcon.countdown.textField.text = timeStr
            leftTime -= 1
            BigWorld.callback(1, Functor(self.countdown, leftTime))
