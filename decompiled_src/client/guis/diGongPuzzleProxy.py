#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/diGongPuzzleProxy.o
import BigWorld
import gameglobal
import time
from guis.uiProxy import UIProxy
from guis import uiConst
from data import puzzle_data as PD
ANSWERS_NUM_MAX = 3

class DiGongPuzzleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DiGongPuzzleProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.widget = None
        self.mediator = None
        self.timer = None
        self.bLeftSound = False
        self.playerAnswer = -1
        self.setData(0, [], 0, {})

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_DIGONG_PUZZLE:
            self.widget = widget
            if self.puzzleId:
                self.updataState()

    def show(self, puzzleId = 0, answers = [], delay = 0, info = {}):
        self.setData(puzzleId, answers, delay, info)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DIGONG_PUZZLE)

    def clearWidget(self):
        self.mediator = None
        self.widget = None
        self.reset()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DIGONG_PUZZLE)

    def reset(self):
        self.playerAnswer = -1
        self.bLeftSound = False
        gameglobal.rds.sound.stopSound(4824)
        self.setData(0, [], 0, {})
        self.stopTimer()

    def updateInfo(self, puzzleId, answers, delay, info):
        self.setData(puzzleId, answers, delay, info)
        self.updataState()

    def updataState(self):
        self.bLeftSound = False
        self.stopTimer()
        self.updateTime()
        self.updateQuestionInfo()
        self.refreshCurAns()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def updateTime(self):
        if self.widget:
            if self.leftTime > 5:
                timeStr = time.strftime('%M:%S', time.localtime(self.leftTime))
                self.widget.timeMc.gotoAndPlay('normal')
                self.widget.timeMc.timeMcc.timeTxt.text = timeStr
                self.timer = BigWorld.callback(1, self.updateTime)
                self.leftTime = self.leftTime - 1
            elif self.leftTime > 0 and self.leftTime <= 5:
                timeStr = time.strftime('%M:%S', time.localtime(self.leftTime))
                self.widget.timeMc.gotoAndPlay('light')
                self.widget.timeMc.lightTimeMc.timeMcc.timeTxt.text = timeStr
                self.timer = BigWorld.callback(1, self.updateTime)
                self.leftTime = self.leftTime - 1
                if not self.bLeftSound:
                    gameglobal.rds.sound.playSound(4824)
                    self.bLeftSound = True
            else:
                self.bLeftSound = False
                gameglobal.rds.sound.stopSound(4824)
                self.widget.timeMc.gotoAndPlay('normal')
                self.leftTime = 0
                self.widget.timeMc.timeMcc.timeTxt.text = '00:00'

    def stepTimeOver(self):
        self.bLeftSound = False
        gameglobal.rds.sound.stopSound(4824)
        pData = PD.data.get(self.puzzleId, {})
        _rightAns = pData.get('rightAnswer', 0)
        p = BigWorld.player()
        if len(p.digongPuzzleInfo) >= 7:
            self.playerAnswer = p.digongPuzzleInfo[6]
        self.setAnswerRightWrong()
        if self.playerAnswer == -1:
            pass
        elif self.answers[self.playerAnswer] == _rightAns:
            gameglobal.rds.sound.playSound(4822)
        else:
            gameglobal.rds.sound.playSound(4823)
        i = 0
        for v in self.answers:
            if i == ANSWERS_NUM_MAX:
                break
            if v == _rightAns:
                getattr(self.widget, 'answerMc' + str(i)).gotoAndPlay('right')
            else:
                getattr(self.widget, 'answerMc' + str(i)).gotoAndPlay('wrong')
            i = i + 1

        self.refreshCurAns()
        self.setAnswerContent()

    def setData(self, puzzleId, answers, delay, info):
        self.puzzleId = puzzleId
        self.answers = answers
        self.leftTime = delay
        self.info = info

    def updateQuestionInfo(self):
        if self.puzzleId and self.widget:
            pData = PD.data.get(self.puzzleId, {})
            desc = pData.get('desc', '')
            self.widget.questionMc.questionMcc.gotoAndPlay('play')
            self.widget.questionMc.questionMcc.descMc.descTxt.text = desc
            for i in xrange(ANSWERS_NUM_MAX):
                getattr(self.widget, 'answerMc' + str(i)).gotoAndPlay('normal')
                getattr(self.widget, 'answerMc' + str(i)).curAnsMc.visible = False

            self.setAnswerContent()
            self.setAnswerRightWrong()

    def setAnswerContent(self):
        if self.puzzleId and self.widget:
            pData = PD.data.get(self.puzzleId, {})
            pAnswers = []
            for key in self.answers:
                _ans = pData.get('a' + str(key), '')
                pAnswers.append(_ans)

            i = 0
            for v in pAnswers:
                if i == ANSWERS_NUM_MAX:
                    break
                getattr(self.widget, 'answerMc' + str(i)).ansTxt.text = v
                i = i + 1

    def setAnswerRightWrong(self):
        burn0 = 0
        burn1 = 0
        burn2 = 0
        burn3 = 0
        if self.info:
            questionNum = self.info.get('question_number', 0)
            questionMaxNum = self.info.get('question_sum', 0)
            self.widget.numMc.numTxt.text = str(questionNum) + '/' + str(questionMaxNum)
            burn1 = self.info.get('burn_1', 0)
            burn2 = self.info.get('burn_2', 0)
            burn3 = self.info.get('burn_3', 0)
        roundTotalRight = 0
        roundTotalWrong = 0
        roundContinueRight = 0
        p = BigWorld.player()
        if p.digongPuzzleInfo:
            roundTotalRight = p.digongPuzzleInfo[1]
            roundTotalWrong = p.digongPuzzleInfo[3]
            roundContinueRight = p.digongPuzzleInfo[0]
        self.widget.rightNumMc.numTxt.text = roundTotalRight
        self.widget.wrongNumMc.numTxt.text = roundTotalWrong
        if roundContinueRight >= burn0 and roundContinueRight < burn1:
            self.widget.rightComboMc.gotoAndPlay('burn0')
            self.widget.rightComboMc.burnNumMc.numTxt.text = roundContinueRight
        elif roundContinueRight >= burn1 and roundContinueRight < burn2:
            self.widget.rightComboMc.gotoAndPlay('burn1')
            self.widget.rightComboMc.burnNumMc.numTxt.text = roundContinueRight
        elif roundContinueRight >= burn2 and roundContinueRight < burn3:
            self.widget.rightComboMc.gotoAndPlay('burn2')
            self.widget.rightComboMc.burnNumMc.burnNumMcc.numTxt.text = roundContinueRight
        else:
            self.widget.rightComboMc.gotoAndPlay('burn3')
            self.widget.rightComboMc.burnNumMc.burnNumMcc.numTxt.text = roundContinueRight

    def refreshCurAns(self, ans = None):
        if ans != None:
            self.playerAnswer = ans
        if self.widget:
            for i in xrange(ANSWERS_NUM_MAX):
                getattr(self.widget, 'answerMc' + str(i)).curAnsMc.visible = False

            if self.playerAnswer != -1:
                getattr(self.widget, 'answerMc' + str(self.playerAnswer)).curAnsMc.visible = True
