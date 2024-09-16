#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yunChuiQuizzesProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import events
import gametypes
import gameglobal
import utils
import clientUtils
import math
import gamelog
import time
import random
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis import uiUtils
from callbackHelper import Functor
from helpers import capturePhoto
from helpers import taboo
from guis import richTextUtils
from guis.asObject import TipManager
from guis import ui
from data import item_data as ID
from data import sys_config_data as SCD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import quizzes_config_data as QCD
from data import quizzes_question_data as QQD
QUESTION_ANSWER_NUM = 4
DANMU_TYPE_NORMAL = 'normal'
DANMU_TYPE_WORLD = 'shijie'
DANMU_TYPE_BUGLE = 'haojiao'
CHAT_CHANNEL_QUIZZES_NORMAL = 48
CHAT_CHANNEL_QUIZZES_WORLD = 49
CHAT_CHANNEL_QUIZZES_HAOJIAO = 50
ACT_TYPE_NORMAL = 1
ACT_TYPE_FISH = 2
optionMap = {0: 'A: ',
 1: 'B: ',
 2: 'C: ',
 3: 'D: '}

class YunChuiQuizzesProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YunChuiQuizzesProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.npcComment = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_YUNCHUI_QUIZZES, self.hide)

    def reset(self):
        self.curActivityId = 0
        self.danMuType = CHAT_CHANNEL_QUIZZES_NORMAL
        self.curRound = 0
        self.myAnswerId = 100
        self.quizzesInfo = {}
        self.openBarrage = True
        self.isLive = True
        self.isSuccess = False
        self.isJoined = True
        self.usedResurgence = False
        self.failedRound = -1
        self.timer = None
        self.headGen = None
        self.result = []
        self.widget = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_YUNCHUI_QUIZZES:
            self.widget = widget
            self.delTimer()
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.delTimer()
        self.reset()
        gameglobal.rds.ui.barrage.hide()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_YUNCHUI_QUIZZES)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_YUNCHUI_QUIZZES)
        else:
            self.initUI()
            self.refreshInfo()

    def setQuizzesInfo(self, activityId, quizzesInfo):
        self.curActivityId = activityId
        self.quizzesInfo = quizzesInfo
        self.refreshInfo()

    def getCurRound(self):
        return self.curRound

    def setCurRound(self, curRound):
        self.curRound = curRound

    def setCurActivityId(self, curActivityId):
        self.curActivityId = curActivityId

    def afterQuizzesOver(self):
        if self.widget:
            self.hide()
        self.npcComment = []

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.resultEffectMc.visible = False
        self.widget.progressBar.visible = False
        self.widget.notification.visible = False
        self.widget.content.visible = False
        self.widget.finalReward.visible = False
        self.widget.money.count.text = 0
        self.widget.left.count.text = 0
        self.widget.normal.groupName = 'danmu'
        self.widget.normal.selected = True
        self.widget.normal.data = CHAT_CHANNEL_QUIZZES_NORMAL
        self.widget.normal.addEventListener(events.BUTTON_CLICK, self.handleSelectType, False, 0, True)
        self.widget.world.groupName = 'danmu'
        self.widget.world.data = CHAT_CHANNEL_QUIZZES_WORLD
        self.widget.world.addEventListener(events.BUTTON_CLICK, self.handleSelectType, False, 0, True)
        self.widget.bugle.groupName = 'danmu'
        self.widget.bugle.data = CHAT_CHANNEL_QUIZZES_HAOJIAO
        self.widget.bugle.addEventListener(events.BUTTON_CLICK, self.handleSelectType, False, 0, True)
        self.widget.sendBtn.addEventListener(events.BUTTON_CLICK, self.handleClickSendBtn, False, 0, True)
        self.widget.shieldBtn.visible = False
        self.widget.shieldBtn.addEventListener(events.BUTTON_CLICK, self.handleClickShieldBtn, False, 0, True)
        self.widget.openBtn.addEventListener(events.BUTTON_CLICK, self.handleClickOpenBtn, False, 0, True)
        self.widget.roleMc.addEventListener(events.MOUSE_CLICK, self.handlePhotoAreaClick, False, 0, True)
        self.widget.tfInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleInputKeyUp, 0, uiConst.AS_INT_MIN_VALUE)
        self.widget.npcText.visible = False
        self.widget.fishIcon.visible = False
        self.widget.normalIcon.visible = False
        self.widget.progressBar.resurgence.visible = False
        if self.isFishQuizzes():
            self.npcComment = SCD.data.get('fishQuizzesNpcComment').get('commentList')
        else:
            self.npcComment = SCD.data.get('quizzesNpcComment').get('commentList')
        random.shuffle(self.npcComment)

    def setApplyNum(self, joinedNum):
        joinedTxt = self.getRemainTxt(joinedNum)
        self.widget.left.count.text = joinedTxt

    def refreshInfo(self):
        if not self.widget or not self.quizzesInfo:
            return
        else:
            activityStage = self.quizzesInfo.get(gametypes.QUIZZES_INFO_ACTIVITY_STAGE)
            if self.curActivityId == 0 or activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_NOT_OPEN or activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_OPEN:
                BigWorld.player().showGameMsg(GMDD.data.QUIZZES_NOT_READY, ())
                self.hide()
                return
            self.updateSpritePhoto3D()
            gameglobal.rds.ui.barrage.show()
            data = QCD.data.get(self.curActivityId, {})
            title = data.get('title', '')
            if self.isFishQuizzes():
                self.widget.fishIcon.visible = True
                self.widget.title.text = title if title else gameStrings.YUNCHUI_QUIZZES_TITLE_FISH
            else:
                self.widget.normalIcon.visible = True
                self.widget.title.text = title if title else gameStrings.YUNCHUI_QUIZZES_TITLE_NORMAL
            self.widget.titleIcon.x = 139 + self.widget.title.textWidth
            questionNum = data.get('questionNum', 12)
            for i in xrange(questionNum):
                answeredTip = getattr(self.widget.progressBar, 'tip%d' % i)
                answeredTip.visible = False

            for i in xrange(questionNum - 1):
                answeredLine = getattr(self.widget.progressBar, 'line%d' % i)
                answeredLine.visible = False

            if self.isFishQuizzes():
                self.widget.rewardTitle.text = SCD.data.get('yunChuiFishRewardTitle')
            else:
                self.widget.rewardTitle.text = SCD.data.get('yunChuiQuizzesRewardTitle') % questionNum
            shareReward = data.get('shareReward')
            fixedBonus = data.get('fixedBonus')
            rewardType = shareReward[0]
            rewardNum = shareReward[1]
            bonusType = self.getBonusType(rewardType)
            self.widget.money.desc.text = data.get('shareRewardTitle')
            self.widget.money.visible = bool(rewardNum)
            self.widget.money.icon.bonusType = bonusType
            self.widget.money.count.text = rewardNum
            fixedItemBonus = clientUtils.genItemBonus(fixedBonus)
            fixedBonusId = fixedItemBonus[0][0]
            fixedBonusCount = fixedItemBonus[0][1]
            itemMc = self.widget.award.item0
            itemMc.slot.dragable = False
            itemMc.slot.itemId = fixedBonusId
            itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(fixedBonusId, fixedBonusCount))
            specialQues = data.get('specialBonus')
            for index, tip in specialQues.iteritems():
                specialIconMc = self.widget.getInstByClsName('YunChuiQuizzes_specialIcon')
                self.widget.progressBar.addChild(specialIconMc)
                specialIconMc.x = 18 + 38 * (index - 1)
                specialIconMc.y = -4
                TipManager.addTip(specialIconMc, tip)

            activityStage = self.quizzesInfo.get(gametypes.QUIZZES_INFO_ACTIVITY_STAGE)
            quizzesState = self.quizzesInfo.get(gametypes.QUIZZES_INFO_QUIZZES_STATE)
            if quizzesState == gametypes.QUIZZES_STATE_FAILED or quizzesState == gametypes.QUIZZES_STATE_NOT_JOIN:
                self.isLive = False
                if quizzesState == gametypes.QUIZZES_STATE_NOT_JOIN:
                    self.isJoined = False
            if self.isFishQuizzes():
                self.widget.progressBar.resurgence.visible = False
            else:
                self.widget.progressBar.resurgence.visible = True
                self.usedResurgence = self.quizzesInfo.get(gametypes.QUIZZES_INFO_REVIVED_INDEX)
                self.refreshResurgence(self.usedResurgence)
            self.widget.progressBar.canvas.x = 18
            self.widget.progressBar.canvas.width = 21 + (questionNum - 1) * 38
            if activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_READY:
                BigWorld.player().base.queryQuizzesJoinedNum()
                self.widget.notification.visible = True
                self.refreshTopBar()
                if self.isJoined:
                    self.widget.progressBar.state.gotoAndStop('yibaoming')
                else:
                    self.widget.progressBar.state.gotoAndStop('weibaoming')
                beginTime = data.get('beginDate')
                intervalJoin = data.get('intervalJoin')
                intervalStart = data.get('intervalStart')
                beginTimeTxt = utils.formatTimeEx(utils.getDisposableCronTabTimeStamp(beginTime) + intervalStart + intervalJoin)[0:5]
                self.widget.notification.startTime.text = beginTimeTxt
                if self.isFishQuizzes():
                    notification = SCD.data.get('fishNotification', ' ')
                else:
                    notification = SCD.data.get('notification', ' ')
                self.widget.notification.rule.htmlText = notification
                leftTime = self.quizzesInfo.get(gametypes.QUIZZES_INFO_NEXT_STAGE_TIMESTAMP, 0) - utils.getNow()
                self.showPrepareCountDown(leftTime)
            elif activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_ROUND_START or activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_ROUND_OVER:
                self.widget.content.visible = True
                remainNum = self.quizzesInfo.get(gametypes.QUIZZES_INFO_REMAIN_NUM)
                remainTxt = self.getRemainTxt(remainNum)
                self.widget.left.count.text = remainTxt
                self.curRound = self.quizzesInfo.get(gametypes.QUIZZES_INFO_CUR_ROUND, 0)
                npcInterval = SCD.data.get('quizzesNpcComment').get('interval', 2)
                if self.curRound % npcInterval == 1:
                    self.widget.npcText.desc.tf.text = self.npcComment[self.curRound / npcInterval]
                    self.widget.npcText.visible = True
                    self.widget.npcText.play()
                else:
                    self.widget.npcText.visible = False
                specialQuesList = data.get('specialBonus').keys()
                self.widget.content.title.text = gameStrings.YUNCHUI_QUIZZES_TITLE % self.curRound
                failedRound = self.quizzesInfo.get(gametypes.QUIZZES_INFO_FAILED_QUESTION_INDEX, -1)
                self.failedRound = failedRound
                self.refreshTopBar()
                self.refreshQuizState()
                endTime = self.quizzesInfo.get(gametypes.QUIZZES_INFO_NEXT_STAGE_TIMESTAMP, 0)
                if activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_ROUND_START:
                    self.widget.content.countDownDesc.text = gameStrings.YUNCHUI_QUIZZES_ANSWER
                    self.widget.content.preCountDown.visible = False
                    self.widget.content.ansCountDown.visible = True
                    self.widget.content.ansCountDown.maxValue = data.get('answerTime')
                    self.showAnsCountDown(endTime)
                    self.showAnsSecondCountDown(endTime)
                commitedAnswerId = -1
                if quizzesState == gametypes.QUIZZES_STATE_WAIT_QUESTION or quizzesState == gametypes.QUIZZES_STATE_DOING:
                    commitedAnswerId = self.quizzesInfo.get(gametypes.QUIZZES_INFO_COMMITED_ANSWER_ID)
                questionDesc = self.quizzesInfo.get(gametypes.QUIZZES_INFO_QUESTION_DESC)
                optionDesc = self.quizzesInfo.get(gametypes.QUIZZES_INFO_OPTION_DESC)
                if self.curRound in specialQuesList:
                    questionDesc = gameStrings.YUNCHUI_QUIZZES_SPECIAL_TITLE + questionDesc
                self.widget.content.problem.text = questionDesc
                for i in xrange(len(optionDesc)):
                    answerMc = getattr(self.widget.content, 'answer%d' % i)
                    answerMc.index = i
                    if answerMc.answerBtn.textField.numLines == 1:
                        answerMc.answerBtn.labels = [optionMap[i] + optionDesc[i], '']
                    else:
                        answerMc.answerBtn.labels = ['', optionMap[i] + optionDesc[i]]
                    answerMc.yes.visible = False
                    answerMc.no.visible = False
                    answerMc.people.visible = False
                    answerMc.progressBar.visible = False
                    answerMc.selectMc.visible = False
                    if commitedAnswerId >= 0 and commitedAnswerId <= 3:
                        ASUtils.setHitTestDisable(answerMc, True)
                        if i == commitedAnswerId:
                            answerMc.selectMc.visible = True
                    elif self.isLive:
                        answerMc.addEventListener(events.MOUSE_CLICK, self.handleClickAnswer, False, 0, True)
                    else:
                        ASUtils.setHitTestDisable(answerMc, True)
                        answerMc.answerBtn.disabled = True

                if activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_ROUND_OVER:
                    self.widget.content.ansCountDown.visible = False
                    self.widget.content.preCountDown.visible = True
                    self.widget.content.countDownDesc.text = gameStrings.YUNCHUI_QUIZZES_PREPARE
                    self.widget.content.preCountDown.maxValue = data.get('readyTime')
                    self.showPreCountDown(endTime)
                    self.showPreSecondCountDown(endTime)
                    optionSelectedNum = self.quizzesInfo.get(gametypes.QUIZZES_INFO_OPTION_SELECTED_NUM)
                    answerResult = self.quizzesInfo.get(gametypes.QUIZZES_INFO_ANSWER_RESULT)
                    rightAnswerId = self.quizzesInfo.get(gametypes.QUIZZES_INFO_RIGHT_ANSWER_ID)
                    self.myAnswerId = self.quizzesInfo.get(gametypes.QUIZZES_INFO_COMMITED_ANSWER_ID)
                    answerNum = sum(optionSelectedNum)
                    answerType = QQD.data.get(data.get('questions')[self.curRound - 1]).get('answerType')
                    if answerType == gametypes.QUIZZES_ANSWER_TYPE_MOST:
                        mostAnswerId = optionSelectedNum.index(max(optionSelectedNum))
                        if mostAnswerId != rightAnswerId:
                            optionSelectedNum[rightAnswerId], optionSelectedNum[mostAnswerId] = optionSelectedNum[mostAnswerId], optionSelectedNum[rightAnswerId]
                    elif answerType == gametypes.QUIZZES_ANSWER_TYPE_LEAST or answerType == gametypes.QUIZZES_ANSWER_TYPE_RAND:
                        b = sorted([ x for x in optionSelectedNum if x > 0 ])
                        if b:
                            leastAnswerId = optionSelectedNum.index(b[0] if b else None)
                            if leastAnswerId != rightAnswerId:
                                optionSelectedNum[rightAnswerId], optionSelectedNum[leastAnswerId] = optionSelectedNum[leastAnswerId], optionSelectedNum[rightAnswerId]
                    for i in xrange(len(optionSelectedNum)):
                        answerMc = getattr(self.widget.content, 'answer%d' % i)
                        progressBar = answerMc.progressBar
                        progressBar.maxValue = answerNum
                        progressBar.currentValue = 0
                        self.showAnswerResult(optionSelectedNum[i], progressBar)
                        answerMc.people.text = str(int(optionSelectedNum[i] * 100)) + '%'
                        answerMc.people.visible = True
                        answerMc.progressBar.visible = True
                        answerMc.yes.visible = False
                        answerMc.no.visible = False
                        if i == rightAnswerId:
                            answerMc.yes.visible = True
                        if answerResult == gametypes.QUIZZES_ANSWER_WRONG or answerResult == gametypes.QUIZZES_ANSWER_WRONG_CONTINUE:
                            if i == self.myAnswerId:
                                answerMc.no.visible = True
                        if not self.isLive:
                            ASUtils.setHitTestDisable(answerMc, True)

            elif activityStage == gametypes.QUIZZES_ACTIVITY_STAGE_OVER:
                answerResult = self.quizzesInfo.get(gametypes.QUIZZES_INFO_ANSWER_RESULT)
                succeedNum = self.quizzesInfo.get(gametypes.QUIZZES_INFO_REMAIN_NUM)
                failedNum = self.quizzesInfo.get(gametypes.QUIZZES_INFO_FAILED_NUM)
                specialReward = self.quizzesInfo.get(gametypes.QUIZZES_INFO_SPECIAL_REWARD)
                self.onQuizzesOver(specialReward, succeedNum, failedNum, answerResult)
            return

    def onQuizzesRoundStart(self, data):
        if not self.widget:
            return
        QCDdata = QCD.data.get(self.curActivityId, {})
        self.widget.notification.visible = False
        self.widget.content.visible = True
        self.widget.content.countDownDesc.text = gameStrings.YUNCHUI_QUIZZES_ANSWER
        self.widget.resultEffectMc.visible = False
        specialQuesList = QCDdata.get('specialBonus').keys()
        self.curRound = data[0]
        npcInterval = SCD.data.get('quizzesNpcComment').get('interval', 2)
        if self.curRound % npcInterval == 1:
            self.widget.npcText.desc.tf.text = self.npcComment[self.curRound / npcInterval]
            self.widget.npcText.visible = True
            self.widget.npcText.play()
        else:
            self.widget.npcText.visible = False
        self.widget.content.title.text = gameStrings.YUNCHUI_QUIZZES_TITLE % self.curRound
        self.widget.content.preCountDown.visible = False
        self.widget.content.ansCountDown.maxValue = QCDdata.get('answerTime')
        self.widget.content.ansCountDown.visible = True
        answerTime = QCDdata.get('answerTime', 10)
        endTime = time.time() + answerTime
        self.showAnsCountDown(endTime)
        self.showAnsSecondCountDown(utils.getNow() + answerTime)
        self.refreshTopBar()
        self.refreshQuizState()
        questionDesc = data[1]
        optionDesc = data[2]
        if self.curRound in specialQuesList:
            questionDesc = gameStrings.YUNCHUI_QUIZZES_SPECIAL_TITLE + questionDesc
        self.widget.content.problem.text = questionDesc
        for i in xrange(len(optionDesc)):
            answerMc = getattr(self.widget.content, 'answer%d' % i)
            if answerMc.answerBtn.textField.numLines == 1:
                answerMc.answerBtn.labels = [optionMap[i] + optionDesc[i], '']
            else:
                answerMc.answerBtn.labels = ['', optionMap[i] + optionDesc[i]]
            answerMc.yes.visible = False
            answerMc.no.visible = False
            answerMc.people.visible = False
            answerMc.progressBar.visible = False
            answerMc.selectMc.visible = False
            answerMc.index = i
            if self.isLive:
                ASUtils.setHitTestDisable(answerMc, False)
                answerMc.addEventListener(events.MOUSE_CLICK, self.handleClickAnswer, False, 0, True)
            else:
                ASUtils.setHitTestDisable(answerMc, True)
                answerMc.answerBtn.disabled = True

    def onQueryQuizzesRoundResult(self, answerResult, remainNum, optionsSelectedNum, rightAnswerId, myAnswerId, nextStageStamp):
        if not self.widget:
            return
        else:
            data = QCD.data.get(self.curActivityId, {})
            remainTxt = self.getRemainTxt(remainNum)
            self.widget.left.count.text = remainTxt
            self.widget.content.countDownDesc.text = gameStrings.YUNCHUI_QUIZZES_PREPARE
            self.widget.content.ansCountDown.visible = False
            self.widget.content.preCountDown.maxValue = data.get('readyTime')
            self.widget.content.preCountDown.visible = True
            self.showPreCountDown(nextStageStamp)
            self.showPreSecondCountDown(nextStageStamp)
            if answerResult == gametypes.QUIZZES_ANSWER_NOT_RESULT:
                self.widget.resultEffectMc.visible = False
            else:
                self.widget.resultEffectMc.visible = True
                if answerResult == gametypes.QUIZZES_ANSWER_WRONG:
                    self.widget.resultEffectMc.resultEffect.gotoAndStop('eliminate')
                    self.isLive = False
                    self.failedRound = self.curRound - 1
                elif answerResult == gametypes.QUIZZES_ANSWER_RIGHT:
                    self.widget.resultEffectMc.resultEffect.gotoAndStop('promotion')
                elif answerResult == gametypes.QUIZZES_ANSWER_WRONG_CONTINUE:
                    self.usedResurgence = self.curRound - 1
                    self.widget.resultEffectMc.resultEffect.gotoAndStop('error')
            self.refreshResurgence(self.usedResurgence)
            self.widget.resultEffectMc.play()
            self.refreshTopBar()
            self.refreshQuizState()
            answerNum = sum(optionsSelectedNum)
            answerType = QQD.data.get(data.get('questions')[self.curRound - 1]).get('answerType')
            if answerType == gametypes.QUIZZES_ANSWER_TYPE_MOST:
                mostAnswerId = optionsSelectedNum.index(max(optionsSelectedNum))
                if mostAnswerId != rightAnswerId:
                    optionsSelectedNum[rightAnswerId], optionsSelectedNum[mostAnswerId] = optionsSelectedNum[mostAnswerId], optionsSelectedNum[rightAnswerId]
            elif answerType == gametypes.QUIZZES_ANSWER_TYPE_LEAST or answerType == gametypes.QUIZZES_ANSWER_TYPE_RAND:
                b = sorted([ x for x in optionsSelectedNum if x > 0 ])
                if b:
                    leastAnswerId = optionsSelectedNum.index(b[0] if b else None)
                    if leastAnswerId != rightAnswerId:
                        optionsSelectedNum[rightAnswerId], optionsSelectedNum[leastAnswerId] = optionsSelectedNum[leastAnswerId], optionsSelectedNum[rightAnswerId]
            for i in xrange(len(optionsSelectedNum)):
                answerMc = getattr(self.widget.content, 'answer%d' % i)
                progressBar = answerMc.progressBar
                progressBar.maxValue = answerNum
                progressBar.currentValue = 0
                self.showAnswerResult(optionsSelectedNum[i], progressBar)
                answerMc.people.text = str(int(optionsSelectedNum[i] * 100)) + '%'
                answerMc.people.visible = True
                answerMc.progressBar.visible = True
                answerMc.selectMc.visible = False
                ASUtils.setHitTestDisable(answerMc, True)
                if i == rightAnswerId:
                    answerMc.yes.visible = True
                if answerResult == gametypes.QUIZZES_ANSWER_WRONG or answerResult == gametypes.QUIZZES_ANSWER_WRONG_CONTINUE:
                    if i == myAnswerId:
                        answerMc.no.visible = True

            self.widget.notification.visible = False
            self.widget.content.visible = True
            return

    def refreshTopBar(self):
        self.widget.progressBar.visible = True
        if self.curRound > 0:
            currentTip = getattr(self.widget.progressBar, 'tip%d' % (self.curRound - 1))
            currentTip.visible = True
            currentTip.gotoAndStop('current')
        if self.curRound > 1:
            for i in xrange(self.curRound - 1):
                answeredTip = getattr(self.widget.progressBar, 'tip%d' % i)
                answeredLine = getattr(self.widget.progressBar, 'line%d' % i)
                if self.isJoined:
                    answeredTip.gotoAndStop('correct')
                else:
                    answeredTip.gotoAndStop('guanzhan')
                answeredTip.visible = True
                answeredLine.visible = True

        if self.failedRound >= 0:
            failedTip = getattr(self.widget.progressBar, 'tip%d' % self.failedRound)
            failedTip.gotoAndStop('error')
            questionNum = QCD.data.get(self.curActivityId, {}).get('questionNum', 12)
            if self.failedRound < questionNum - 1:
                failedLine = getattr(self.widget.progressBar, 'line%d' % self.failedRound)
            for i in xrange(self.failedRound + 1, self.curRound - 1):
                tip = getattr(self.widget.progressBar, 'tip%d' % i)
                tip.gotoAndStop('guanzhan')

    def getBonusType(self, type):
        if type == SCD.data.get('quizzesRewardBindCoin', 1):
            bonusType = 'tianBi'
        elif type == SCD.data.get('quizzesRewardCash', 2):
            bonusType = 'cash'
        elif type == SCD.data.get('quizzesRewardBindCash', 3):
            bonusType = 'bindCash'
        elif type == SCD.data.get('quizzesRewardFame', 4):
            bonusType = 'yunChui'
        return bonusType

    def onQuizzesOver(self, specialReward, succeedNum, failedNum, answerResult):
        if not self.widget or not self.curActivityId:
            return
        self.result = (specialReward,
         succeedNum,
         failedNum,
         answerResult)
        self.widget.notification.visible = False
        self.widget.progressBar.visible = False
        self.widget.content.visible = False
        succeedTxt = self.getRemainTxt(succeedNum)
        self.widget.left.count.text = succeedTxt
        finalRewardMc = self.widget.finalReward
        finalRewardMc.visible = True
        data = QCD.data.get(self.curActivityId, {})
        shareReward = data.get('shareReward')
        rewardType = shareReward[0]
        rewardNum = shareReward[1]
        bonusType = self.getBonusType(rewardType)
        if answerResult == gametypes.QUIZZES_ANSWER_RIGHT or answerResult == gametypes.QUIZZES_ANSWER_WRONG_CONTINUE:
            self.isSuccess = True
        else:
            self.isSuccess = False
        isFishQuizzes = self.isFishQuizzes()
        if self.isSuccess:
            finalRewardMc.content.gotoAndStop('success')
            if isFishQuizzes:
                finalRewardMc.content.title.text = data.get('successTitle', gameStrings.YUNCHUI_QUIZZES_FISH_SUCCESS_TITLE)
                finalRewardMc.content.successDesc.text = data.get('successDesc1', gameStrings.YUNCHUI_QUIZZES_FISH_SUCCESS_DESC1)
                finalRewardMc.content.desc2.text = data.get('successDesc2', gameStrings.YUNCHUI_QUIZZES_FISH_SUCCESS_DESC2)
                finalRewardMc.content.moneyIcon.visible = False
            else:
                finalRewardMc.content.successDesc.text = gameStrings.YUNCHUI_QUIZZES_SUCCESSDESC % succeedNum
                averageMoney = math.ceil(float(rewardNum) / succeedNum)
                finalRewardMc.content.moneyIcon.visible = True
                finalRewardMc.content.moneyIcon.bonusType = bonusType
                finalRewardMc.content.desc2.text = gameStrings.YUNCHUI_QUIZZES_SHARE_BONUS_DESC % averageMoney
                finalRewardMc.content.moneyIcon.x = 117 - len(str(int(averageMoney))) * 5
        else:
            finalRewardMc.content.gotoAndStop('fail')
            finalRewardMc.content.failed.visible = self.isJoined
            if succeedNum:
                if isFishQuizzes:
                    finalRewardMc.content.failed.text = data.get('failTitle', gameStrings.YUNCHUI_QUIZZES_FISH_FAIL_TITLE)
                    finalRewardMc.content.failDesc1.text = data.get('failDesc1', gameStrings.YUNCHUI_QUIZZES_FISH_FAIL_DESC1)
                    finalRewardMc.content.desc2.text = data.get('failDesc2', gameStrings.YUNCHUI_QUIZZES_FISH_FAIL_DESC2)
                    finalRewardMc.content.moneyIcon.visible = False
                else:
                    finalRewardMc.content.failDesc1.text = gameStrings.YUNCHUI_QUIZZES_FAILEDDESC % succeedNum
                    finalRewardMc.content.moneyIcon.visible = True
                    averageMoney = math.ceil(float(rewardNum) / succeedNum)
                    finalRewardMc.content.moneyIcon.bonusType = bonusType
                    finalRewardMc.content.desc2.text = gameStrings.YUNCHUI_QUIZZES_SHARE_BONUS_DESC % averageMoney
                    finalRewardMc.content.moneyIcon.x = 117 - len(str(int(averageMoney))) * 5
            else:
                finalRewardMc.content.moneyIcon.visible = False
                if isFishQuizzes:
                    finalRewardMc.content.failed.text = data.get('noFishTitle', gameStrings.YUNCHUI_QUIZZES_FISH_NOFISH_TITLE)
                    finalRewardMc.content.failDesc1.text = data.get('noFishDesc1', gameStrings.YUNCHUI_QUIZZES_FISH_NOFISH_DESC1)
                    finalRewardMc.content.desc2.text = data.get('noFishDesc2', gameStrings.YUNCHUI_QUIZZES_FISH_NOFISH_DESC2)
                else:
                    finalRewardMc.content.failDesc1.text = gameStrings.YUNCHUI_QUIZZES_NO_SUCCESS_DESC
                    finalRewardMc.content.desc2.text = gameStrings.YUNCHUI_QUIZZES_NO_REWARD_DESC
        fixedBonus = data.get('fixedBonus')
        fixedItemBonus = clientUtils.genItemBonus(fixedBonus)
        fixedBonusId = fixedItemBonus[0][0]
        fixedBonusCount = fixedItemBonus[0][1]
        itemMc = finalRewardMc.content.item
        itemMc.slot.dragable = False
        itemMc.slot.itemId = fixedBonusId
        itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(fixedBonusId, fixedBonusCount))
        if specialReward:
            finalRewardMc.content.selectMc.visible = True
            finalRewardMc.content.selectMc.btn0.gotoAndStop('select')
            finalRewardMc.content.selectMc.btn1.gotoAndStop('up')
            finalRewardMc.content.preBtn.visible = False
            finalRewardMc.content.nextBtn.visible = True
            finalRewardMc.content.preBtn.addEventListener(events.MOUSE_CLICK, self.handleClickPreBtn, False, 0, True)
            finalRewardMc.content.nextBtn.addEventListener(events.MOUSE_CLICK, self.handleClickNextBtn, False, 0, True)
        else:
            finalRewardMc.content.selectMc.visible = False
            finalRewardMc.content.preBtn.visible = False
            finalRewardMc.content.nextBtn.visible = False
        finalRewardMc.play()

    def handleClickPreBtn(self, *args):
        succeedNum = self.result[1]
        self.widget.finalReward.content.item.visible = True
        if self.widget:
            finalRewardMc = self.widget.finalReward
            finalRewardMc.content.preBtn.visible = False
            finalRewardMc.content.nextBtn.visible = True
            finalRewardMc.content.selectMc.btn1.gotoAndStop('up')
            finalRewardMc.content.selectMc.btn0.gotoAndStop('select')
            data = QCD.data.get(self.curActivityId, {})
            shareReward = data.get('shareReward')
            rewardType = shareReward[0]
            rewardNum = shareReward[1]
            bonusType = self.getBonusType(rewardType)
            isFishQuizzes = self.isFishQuizzes()
            if self.isSuccess:
                finalRewardMc.content.gotoAndStop('success')
                if isFishQuizzes:
                    finalRewardMc.content.title.text = data.get('successTitle ', gameStrings.YUNCHUI_QUIZZES_FISH_SUCCESS_TITLE)
                    finalRewardMc.content.successDesc.text = data.get('successDesc1', gameStrings.YUNCHUI_QUIZZES_FISH_SUCCESS_DESC1)
                    finalRewardMc.content.desc2.text = data.get('successDesc2', gameStrings.YUNCHUI_QUIZZES_FISH_SUCCESS_DESC2)
                    finalRewardMc.content.moneyIcon.visible = False
                else:
                    finalRewardMc.content.successDesc.text = gameStrings.YUNCHUI_QUIZZES_SUCCESSDESC % succeedNum
                    averageMoney = math.ceil(float(rewardNum) / succeedNum)
                    finalRewardMc.content.moneyIcon.visible = True
                    finalRewardMc.content.moneyIcon.bonusType = bonusType
                    finalRewardMc.content.desc2.text = gameStrings.YUNCHUI_QUIZZES_SHARE_BONUS_DESC % averageMoney
                    finalRewardMc.content.moneyIcon.x = 117 - len(str(int(averageMoney))) * 5
            else:
                finalRewardMc.content.gotoAndStop('fail')
                finalRewardMc.content.failed.visible = self.isJoined
                if succeedNum:
                    if isFishQuizzes:
                        finalRewardMc.content.failed.text = data.get('failTitle', gameStrings.YUNCHUI_QUIZZES_FISH_FAIL_TITLE)
                        finalRewardMc.content.failDesc1.text = data.get('failDesc1', gameStrings.YUNCHUI_QUIZZES_FISH_FAIL_DESC1)
                        finalRewardMc.content.desc2.text = data.get('failDesc2', gameStrings.YUNCHUI_QUIZZES_FISH_FAIL_DESC2)
                        finalRewardMc.content.moneyIcon.visible = False
                    else:
                        finalRewardMc.content.failDesc1.text = gameStrings.YUNCHUI_QUIZZES_FAILEDDESC % succeedNum
                        finalRewardMc.content.moneyIcon.visible = True
                        averageMoney = math.ceil(float(rewardNum) / succeedNum)
                        finalRewardMc.content.moneyIcon.bonusType = bonusType
                        finalRewardMc.content.desc2.text = gameStrings.YUNCHUI_QUIZZES_SHARE_BONUS_DESC % averageMoney
                        finalRewardMc.content.moneyIcon.x = 117 - len(str(int(averageMoney))) * 5
                else:
                    finalRewardMc.content.moneyIcon.visible = False
                    if isFishQuizzes:
                        finalRewardMc.content.failed.text = data.get('noFishTitle', gameStrings.YUNCHUI_QUIZZES_FISH_NOFISH_TITLE)
                        finalRewardMc.content.failDesc1.text = data.get('noFishDesc1', gameStrings.YUNCHUI_QUIZZES_FISH_NOFISH_DESC1)
                        finalRewardMc.content.desc2.text = data.get('noFishDesc2', gameStrings.YUNCHUI_QUIZZES_FISH_NOFISH_DESC2)
                    else:
                        finalRewardMc.content.failDesc1.text = gameStrings.YUNCHUI_QUIZZES_NO_SUCCESS_DESC
                        finalRewardMc.content.desc2.text = gameStrings.YUNCHUI_QUIZZES_NO_REWARD_DESC
            fixedBonus = data.get('fixedBonus')
            fixedItemBonus = clientUtils.genItemBonus(fixedBonus)
            fixedBonusId = fixedItemBonus[0][0]
            fixedBonusCount = fixedItemBonus[0][1]
            itemMc = finalRewardMc.content.item
            itemMc.slot.dragable = False
            itemMc.slot.itemId = fixedBonusId
            itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(fixedBonusId, fixedBonusCount))

    def handleClickNextBtn(self, *args):
        if self.widget:
            self.widget.finalReward.content.preBtn.visible = True
            self.widget.finalReward.content.nextBtn.visible = False
            self.widget.finalReward.content.selectMc.btn0.gotoAndStop('up')
            self.widget.finalReward.content.selectMc.btn1.gotoAndStop('select')
        self.widget.finalReward.content.gotoAndStop('special')
        data = QCD.data.get(self.curActivityId, {})
        isFishQuizzes = self.isFishQuizzes()
        if isFishQuizzes:
            self.widget.finalReward.content.specialDesc.text = gameStrings.YUNCHUI_QUIZZES_FISH_SPECIALDESC
            self.widget.finalReward.content.specialDesc2.visible = False
            self.widget.finalReward.content.specialDesc3.visible = True
            self.widget.finalReward.content.item.visible = False
            self.widget.finalReward.content.moneyIcon.visible = False
        else:
            specialQuesList = data.get('specialBonus').keys()
            specialBouns = QQD.data.get(data.get('questions')[specialQuesList[0] - 1]).get('fixedBonus')
            self.widget.finalReward.content.specialDesc.text = gameStrings.YUNCHUI_QUIZZES_SPECIALDESC % specialQuesList[0]
            if self.result:
                specialReward = self.result[0]
                if specialReward:
                    for index, reward in specialReward.iteritems():
                        questions = QCD.data.get(self.curActivityId).get('questions')
                        if questions:
                            questionId = questions[index]
                        shareReward = QQD.data.get(questionId).get('shareReward')
                        if reward:
                            specialType = shareReward[0]
                            bonusType = self.getBonusType(specialType)
                            self.widget.finalReward.content.moneyIcon.visible = True
                            self.widget.finalReward.content.moneyIcon.bonusType = bonusType
                            self.widget.finalReward.content.specialDesc2.visible = True
                            if specialBouns:
                                self.widget.finalReward.content.specialDesc2.text = gameStrings.YUNCHUI_QUIZZES_SHARE_BONUS_DESC % reward
                                self.widget.finalReward.content.moneyIcon.x = 116 - len(str(reward)) * 5
                            else:
                                self.widget.finalReward.content.specialDesc2.text = gameStrings.YUNCHUI_QUIZZES_SHARE_DESC % reward
                                self.widget.finalReward.content.moneyIcon.x = 151 - len(str(reward)) * 5
                        elif specialBouns:
                            self.widget.finalReward.content.moneyIcon.visible = False
                            self.widget.finalReward.content.specialDesc2.text = gameStrings.YUNCHUI_QUIZZES_BONUS_DESC

            if specialBouns:
                specialItemBonus = clientUtils.genItemBonus(specialBouns)
                specialBonusId = specialItemBonus[0][0]
                specialBonusCount = specialItemBonus[0][1]
                self.widget.finalReward.content.specialDesc3.visible = False
                specialItemMc = self.widget.finalReward.content.item
                specialItemMc.visible = True
                specialItemMc.slot.dragable = False
                specialItemMc.slot.itemId = specialBonusId
                specialItemMc.slot.setItemSlotData(uiUtils.getGfxItemById(specialBonusId, specialBonusCount))
            else:
                self.widget.finalReward.content.item.visible = False
                self.widget.finalReward.content.specialDesc3.visible = True

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(1, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        data = QCD.data.get(self.curActivityId, {})
        startTime = data.get('beginDate', '')
        intervalJoin = data.get('intervalJoin', 0)
        intervalStart = data.get('intervalStart', 300)
        left = utils.getPreCrontabTime(startTime) + intervalJoin + intervalStart - utils.getNow()
        if left < 0:
            left = 0
        self.widget.notification.countDown.text = utils.formatDurationShortVersion(left)
        if left == 0:
            self.delTimer()
            self.widget.notification.countDown.text = gameStrings.YUNCHUI_QUIZZES_COUNTDOWN_ZERO

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None

    def showPrepareCountDown(self, leftTime):
        if not self.widget:
            return
        if leftTime > 0:
            leftTime -= 1
            self.widget.notification.countDown.text = utils.formatDurationShortVersion(leftTime)
            BigWorld.callback(1, Functor(self.showPrepareCountDown, leftTime))
        if leftTime <= 0:
            self.widget.notification.countDown.text = gameStrings.YUNCHUI_QUIZZES_COUNTDOWN_ZERO

    def showAnsCountDown(self, endTime):
        if not self.widget:
            return
        if endTime >= utils.getNow():
            leftTime = endTime - time.time()
            self.widget.content.ansCountDown.currentValue = leftTime
            BigWorld.callback(0.02, Functor(self.showAnsCountDown, endTime))

    def showPreCountDown(self, endTime):
        if not self.widget:
            return
        if endTime >= utils.getNow():
            leftTime = endTime - time.time()
            self.widget.content.preCountDown.currentValue = leftTime
            BigWorld.callback(0.02, Functor(self.showPreCountDown, endTime))

    def showAnsSecondCountDown(self, endTime):
        if not self.widget:
            return
        if endTime >= utils.getNow():
            leftTime = endTime - utils.getNow()
            self.widget.content.ansCountDown.second.text = leftTime
            BigWorld.callback(1, Functor(self.showAnsSecondCountDown, endTime))

    def showPreSecondCountDown(self, endTime):
        if not self.widget:
            return
        if endTime >= utils.getNow():
            leftTime = endTime - utils.getNow()
            self.widget.content.preCountDown.second.text = leftTime
            BigWorld.callback(1, Functor(self.showPreSecondCountDown, endTime))

    def showAnswerResult(self, peopleRate, progressBar):
        if not self.widget:
            return
        if progressBar.currentValue < peopleRate:
            progressBar.currentValue += 0.01
            BigWorld.callback(0.01, Functor(self.showAnswerResult, peopleRate, progressBar))
        else:
            progressBar.currentValue = peopleRate

    def handleClickAnswer(self, *args):
        target = ASObject(args[3][0]).currentTarget
        target.selectMc.visible = True
        self.myAnswerId = target.index
        for i in xrange(QUESTION_ANSWER_NUM):
            answerMc = getattr(self.widget.content, 'answer%d' % i)
            ASUtils.setHitTestDisable(answerMc, True)

        BigWorld.player().base.commitQuizzesAnswer(self.curRound, self.myAnswerId)

    def handleClickSendBtn(self, *args):
        msg = self.widget.tfInput.text
        msgLen = self.str_len(msg)
        if not msg:
            return
        if msgLen > SCD.data.get('MAX_QUIZZES_BARRAGE_MSG_LENGTH', 30):
            BigWorld.player().showGameMsg(GMDD.data.SEND_FAILED_MSG_OVER_FLOW, ())
            return
        if richTextUtils.isSysRichTxt(msg):
            BigWorld.player().showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return
        nowMsg = msg
        isNormal, nowMsg = taboo.checkDisbWord(nowMsg)
        if not isNormal:
            BigWorld.player().showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return
        isNormal, nowMsg = taboo.checkBWorld(nowMsg)
        if not isNormal:
            BigWorld.player().showGameMsg(GMDD.data.FONT_LIB_MONITOR_MASK, ())
            return
        if self.danMuType == CHAT_CHANNEL_QUIZZES_WORLD or self.danMuType == CHAT_CHANNEL_QUIZZES_HAOJIAO:
            msg = GMD.data.get(GMDD.data.QUIZZES_USE_DANMU_ITEM, {}).get('text', gameStrings.TEXT_YUNCHUIQUIZZESPROXY_884)
            if not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_QUIZZES_DANMU_ITEM, False):
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(BigWorld.player().cell.chatToQuizzes, nowMsg, self.danMuType), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_QUIZZES_DANMU_ITEM)
            else:
                BigWorld.player().cell.chatToQuizzes(nowMsg, self.danMuType)
        else:
            BigWorld.player().cell.chatToQuizzes(nowMsg, self.danMuType)

    def handleSelectType(self, *args):
        target = ASObject(args[3][0]).currentTarget
        target.selected = True
        self.danMuType = target.data

    def handleClickOpenBtn(self, *args):
        self.openBarrage = False
        self.widget.shieldBtn.visible = True
        self.widget.openBtn.visible = False
        gameglobal.rds.ui.barrage.hide()

    def handleClickShieldBtn(self, *args):
        self.openBarrage = True
        self.widget.shieldBtn.visible = False
        self.widget.openBtn.visible = True
        gameglobal.rds.ui.barrage.show()

    def onChatToQuizzes(self, channel, msg):
        if channel == CHAT_CHANNEL_QUIZZES_HAOJIAO:
            type = DANMU_TYPE_BUGLE
        elif channel == CHAT_CHANNEL_QUIZZES_WORLD:
            type = DANMU_TYPE_WORLD
        else:
            type = DANMU_TYPE_NORMAL
        if self.widget and self.openBarrage:
            gameglobal.rds.ui.barrage.addBarrageMsg(msg, False, type)
            self.widget.tfInput.text = ''

    def updateSpritePhoto3D(self):
        self.initHeadGen()
        self.takePhoto3D()

    def initHeadGen(self):
        if not self.headGen:
            self.headGen = capturePhoto.QuizzesAvatarPhotoGen.getInstance('gui/taskmask.tga', 215)
        self.headGen.initFlashMesh()

    def takePhoto3D(self):
        modelId = QCD.data.get(self.curActivityId, {}).get('examiner')
        if not self.headGen:
            self.headGen = capturePhoto.QuizzesAvatarPhotoGen.getInstance('gui/taskmask.tga', 215)
        self.headGen.startCapture(modelId, None, ('1101',))

    def handlePhotoAreaClick(self, *args):
        if not self.headGen:
            return
        model = self.headGen.adaptor.attachment
        try:
            aq = model.action('1102')()
            getattr(aq, '1101')()
        except:
            pass

    def str_len(self, str):
        utf8_l = len(str.decode('gbk'))
        return utf8_l

    def getRemainTxt(self, remainNum):
        leftMargins = SCD.data.get('leftMargins', (100, 200, 500, 1000, 3000, 5000, 8000, 10000))
        if remainNum <= leftMargins[0]:
            remainTxt = remainNum
        elif remainNum > leftMargins[-1]:
            remainTxt = '>' + str(leftMargins[-1]) + gameStrings.TEXT_YUNCHUIQUIZZESPROXY_959
        else:
            for i in xrange(len(leftMargins) - 1):
                if leftMargins[i] < remainNum <= leftMargins[i + 1]:
                    remainTxt = '>' + str(leftMargins[i]) + gameStrings.TEXT_YUNCHUIQUIZZESPROXY_959

        return remainTxt

    def refreshResurgence(self, usedRound):
        if usedRound < 0:
            self.widget.progressBar.resurgence.gotoAndStop('up')
        else:
            self.widget.progressBar.resurgence.gotoAndStop('disable')
            self.widget.progressBar.resurgence.resurgenceDesc.text = gameStrings.YUNCHUI_QUIZZES_RESURGENCE % (usedRound + 1)
        cardId = SCD.data.get('quizzesReviveCardId', 441700)
        cardNum = BigWorld.player().inv.countItemInPages(cardId)
        TipManager.addTip(self.widget.progressBar.resurgence.card, gameStrings.YUNCHUI_QUIZZES_CARD_NUM % cardNum)

    def refreshQuizState(self):
        if not self.isJoined:
            self.widget.progressBar.state.gotoAndStop('guanzhan')
        elif self.isLive:
            self.widget.progressBar.state.gotoAndStop('dati')
        else:
            self.widget.progressBar.state.gotoAndStop('taotai')

    def calOptionPosY(self, textFieldMc):
        y = 10
        if textFieldMc.numLines == 1:
            y = 19
        elif textFieldMc.numLines == 2:
            y = 10
        return y

    @ui.callInCD(0.1)
    def handleInputKeyUp(self, *args):
        e = ASObject(args[3][0])
        if int(e.keyCode) == uiConst.AS_KEY_CODE_ENTER:
            self.handleClickSendBtn()

    def isFishQuizzes(self):
        data = QCD.data.get(self.curActivityId, {})
        actType = data.get('actType', 1)
        return actType == ACT_TYPE_FISH
