#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pairPuzzleProxy.o
import random
import BigWorld
import gameglobal
import uiConst
import events
import const
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import puzzle_data as PD
from data import npc_puzzle_data as NPD
from data import sys_config_data as SCD

class PairPuzzleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PairPuzzleProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PAIR_PUZZLE, self.hide)
        self.reset()

    def reset(self):
        self.pairPuzzlesList = []
        self.puzzleIndex = 0
        self.closeCallback = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PAIR_PUZZLE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def hide(self, destroy = True):
        if self.pairPuzzlesList:
            puzzleVal = self.getPuzzleVal()
            if puzzleVal.puzzleSelfAnswer == None:
                msg = SCD.data.get('PAIR_PUZZLE_QUIT', gameStrings.PAIR_PUZZLE_QUIT)
            else:
                msg = SCD.data.get('PAIR_PUZZLE_QUIT1', gameStrings.PAIR_PUZZLE_QUIT1)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.confirmQuit)
        else:
            self.confirmQuit()

    def confirmQuit(self):
        if self.pairPuzzlesList:
            player = BigWorld.player()
            player.cell.abandonNpcPairPuzzle()
        else:
            self.realHide()

    def realHide(self):
        self.clearWidget()
        self.reset()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PAIR_PUZZLE)
        if self.closeCallback:
            BigWorld.cancelCallback(self.closeCallback)
        self.closeCallback = None

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PAIR_PUZZLE)
        else:
            self.refreshInfo()

    def initUI(self):
        pass

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            self.updateDisplay(None, self.getPuzzleVal())
            return

    def setPuzzleData(self, puzzleList):
        self.pairPuzzlesList = puzzleList
        self.puzzleIndex = 0
        self.show()

    def updatePuzzleVal(self, puzzleVal):
        if self.puzzleIndex < len(self.pairPuzzlesList):
            oldVal = self.pairPuzzlesList[self.puzzleIndex]
            self.pairPuzzlesList[self.puzzleIndex] = puzzleVal
            self.updateDisplay(oldVal, puzzleVal)
            if puzzleVal.isPuzzleCompleted():
                player = BigWorld.player()
                time = NPD.data.get(player.pairPuzzleNpcNo, {}).get('intervalTime', 0)
                if self.puzzleIndex + 1 < len(self.pairPuzzlesList):
                    BigWorld.callback(time, self.nextPairPuzzle)
                else:
                    self.closeCallback = BigWorld.callback(5, self.hide)

    def nextPairPuzzle(self):
        self.puzzleIndex += 1
        if self.puzzleIndex < len(self.pairPuzzlesList):
            self.show()

    def getPuzzleVal(self):
        if self.puzzleIndex < len(self.pairPuzzlesList):
            return self.pairPuzzlesList[self.puzzleIndex]
        else:
            return None

    def updateDisplay(self, oldVal, newVal):
        if not self.widget:
            return
        else:
            widget = self.widget
            player = BigWorld.player()
            if not oldVal or oldVal.puzzleId != newVal.puzzleId:
                puzzleId = newVal.puzzleId
                puzzleDescType = newVal.puzzleDescType
                if self.isSameRight():
                    widget.title.titleText.htmlText = SCD.data.get('PAIR_PUZZLE_TITLE_YINYUAN', gameStrings.PAIR_PUZZLE_TITLE_YINYUAN)
                else:
                    widget.title.titleText.htmlText = SCD.data.get('PAIR_PUZZLE_TITLE_SHITU', gameStrings.PAIR_PUZZLE_TITLE_SHITU)
                pd = PD.data.get(puzzleId, {})
                if puzzleDescType and pd.get('desc1', ''):
                    desc = pd.get('desc1', '')
                else:
                    desc = pd.get('desc', '')
                self.setDisplayMode(isAnswer=True)
                widget.content.htmlText = desc
                widget.answerTip.htmlText = SCD.data.get('PAIR_PUZZLE_ANSWER_TIP', gameStrings.PAIR_PUZZLE_ANSWER_TIP)
                answers = range(pd.get('initAnswer', 4))
                if pd.get('aRandom', 0):
                    random.shuffle(answers)
                for i, index in enumerate(answers):
                    mc = getattr(widget, 'ans%d' % i)
                    mc.label = pd.get('a%d' % index, '')
                    mc.data = index

                for i in xrange(i + 1, 4):
                    getattr(widget, 'ans%d' % i).visible = False

            else:
                puzzleResult = newVal.puzzleResult
                puzzleId = newVal.puzzleId
                pd = PD.data.get(puzzleId, {})
                puzzleSelfAnswer = newVal.puzzleSelfAnswer
                puzzleOtherAnswer = newVal.puzzleOtherAnswer
                if puzzleSelfAnswer != None:
                    self.setDisplayMode(False)
                    widget.result1.nameTxt.htmlText = player.roleName
                    self.showPlayerIcon(player.friend.photo, player.school, player.physique.sex, widget.result1.playerIcon.icon)
                    result = pd.get('a%d' % puzzleSelfAnswer, '')
                    widget.result1.resultTxt.htmlText = result
                    memberInfo = self.getMemberInfo()
                    widget.result2.nameTxt.htmlText = memberInfo.get('roleName', '')
                    widget.result2.resultTxt.htmlText = SCD.data.get('PAIR_PUZZLE_WAIT_OTHER', gameStrings.PAIR_PUZZLE_WAIT_OTHER)
                    self.showPlayerIcon('', memberInfo.get('school', const.SCHOOL_SHENTANG), memberInfo.get('sex', const.SEX_MALE), widget.result2.playerIcon.icon)
                    if puzzleOtherAnswer != None:
                        result = pd.get('a%d' % puzzleOtherAnswer, '')
                        widget.result2.resultTxt.htmlText = result
                if puzzleResult:
                    if puzzleResult == const.PUZZLE_RIGHE:
                        if not self.isSameRight():
                            widget.result1.resultIcon.visible = True
                            widget.result2.resultIcon.visible = True
                            widget.result1.resultIcon.gotoAndStop('right')
                            widget.result2.resultIcon.gotoAndStop('right')
                        descLabel = 'PAIR_PUZZLE_RIGHT_ANSWER' if self.isSameRight() else 'PAIR_PUZZLE_RIGHT_ANSWER1'
                        widget.memberContent.htmlText = SCD.data.get(descLabel, getattr(gameStrings, descLabel))
                        widget.answerTag.visible = True
                        widget.answerTag.gotoAndStop('right')
                    elif puzzleResult == const.PUZZLE_WRONG:
                        if not self.isSameRight():
                            rightAnswerIndex = pd.get('rightAnswer', 0)
                            result = pd.get('a%d' % rightAnswerIndex, '')
                            self.showResultIcon(puzzleSelfAnswer, rightAnswerIndex, widget.result1.resultIcon)
                            self.showResultIcon(puzzleOtherAnswer, rightAnswerIndex, widget.result2.resultIcon)
                            widget.memberContent.htmlText = SCD.data.get('PAIR_PUZZLE_WORNG_ANSWER1', gameStrings.PAIR_PUZZLE_WORNG_ANSWER1) % result
                        else:
                            widget.memberContent.htmlText = SCD.data.get('PAIR_PUZZLE_WORNG_ANSWER', gameStrings.PAIR_PUZZLE_WORNG_ANSWER)
                        widget.answerTag.visible = True
                        widget.answerTag.gotoAndStop('wrong')
            return

    def getMemberInfo(self):
        player = BigWorld.player()
        for gbId, value in player.members.iteritems():
            if gbId != player.gbId:
                return value

        return {}

    def _onAns0Click(self, *args):
        data = self.widget.ans0.data
        self._onAnsClick(data)

    def _onAns1Click(self, *args):
        data = self.widget.ans1.data
        self._onAnsClick(data)

    def _onAns2Click(self, *args):
        data = self.widget.ans2.data
        self._onAnsClick(data)

    def _onAns3Click(self, *args):
        data = self.widget.ans3.data
        self._onAnsClick(data)

    def _onCloseBtnClick(self, *args):
        self.hide()

    def _onAnsClick(self, answerId):
        answerId = int(answerId)
        player = BigWorld.player()
        puzzleVal = self.getPuzzleVal()
        if puzzleVal:
            puzzleId = puzzleVal.puzzleId
            player.cell.answerPairPuzzle(self.puzzleIndex, puzzleId, answerId)

    def setDisplayMode(self, isAnswer = True):
        widget = self.widget
        widget.memberContent.htmlText = ''
        widget.answerTip.htmlText = ''
        if isAnswer:
            widget.content.htmlText = ''
        widget.capTainContent.htmlText = ''
        widget.answerTag.visible = False
        widget.result1.visible = not isAnswer
        widget.result2.visible = not isAnswer
        widget.ans0.visible = isAnswer
        widget.ans1.visible = isAnswer
        widget.ans2.visible = isAnswer
        widget.ans3.visible = isAnswer
        if not isAnswer:
            widget.result1.resultIcon.visible = False
            widget.result2.resultIcon.visible = False
            widget.result1.playerIcon.status.visible = False
            widget.result2.playerIcon.status.visible = False

    def isSameRight(self):
        player = BigWorld.player()
        return NPD.data.get(player.pairPuzzleNpcNo, {}).get('pairPuzzleSameRight', 0)

    def showResultIcon(self, myResult, rightResult, icon):
        icon.visible = True
        icon.gotoAndStop('right' if myResult == rightResult else 'wrong')

    def showPlayerIcon(self, ddsPath, school, sex, icon):
        icon.imgType = uiConst.IMG_TYPE_NOS_FILE
        icon.fitSize = True
        if not ddsPath:
            ddsPath = 'headIcon/%s.dds' % str(school * 10 + sex)
        icon.url = ddsPath
