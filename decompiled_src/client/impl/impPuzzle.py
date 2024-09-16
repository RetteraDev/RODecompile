#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPuzzle.o
import gamelog
import gameglobal
import gametypes
import const
from cdata import game_msg_def_data as GMDD

class ImpPuzzle(object):

    def onAnswerPuzzle(self, puzzleId, answerId, result):
        if result == gametypes.NPC_PUZZLE_ANSWER_WRONG:
            gameglobal.rds.ui.puzzle.puzzleAnswerUpdateByNpc(const.PUZZLE_WRONG)
        elif result == gametypes.NPC_PUZZLE_ANSWER_RIGHT:
            gameglobal.rds.ui.puzzle.puzzleAnswerUpdateByNpc(const.PUZZLE_RIGHE)

    def onAnswerPuzzleTrigger(self, puzzleId, answerId, result):
        if result == gametypes.NPC_PUZZLE_ANSWER_WRONG:
            gameglobal.rds.ui.puzzle.puzzleAnswerUpdateByNpc(const.PUZZLE_WRONG)
        elif result == gametypes.NPC_PUZZLE_ANSWER_RIGHT:
            gameglobal.rds.ui.puzzle.puzzleAnswerUpdateByNpc(const.PUZZLE_RIGHE)
        elif result == gametypes.NPC_PUZZLE_ANSWER_FAIL:
            gameglobal.rds.ui.puzzle.hideByTriggerFail()

    def onAcceptPuzzle(self, result):
        if result == gametypes.NPC_PUZZLE_ACC_SUC:
            gameglobal.rds.ui.puzzle.refreshSetPuzzleInfo()
        elif result == gametypes.NPC_PUZZLE_ACC_FAIL_BY_LIMIT:
            gameglobal.rds.ui.npcPanel.hideNpcFullScreen()

    def onAcceptPuzzleTrigger(self, result):
        if result == gametypes.NPC_PUZZLE_ACC_SUC:
            gameglobal.rds.ui.puzzle.refreshSetPuzzleInfo()
        elif result == gametypes.NPC_PUZZLE_ACC_FAIL_BY_LIMIT:
            gameglobal.rds.ui.npcPanel.hideNpcFullScreen()

    def onPuzzleFinish(self, result):
        self.showGameMsg(GMDD.data.NPC_PUZZLE_FINISHED, ())

    def onPuzzleFinishTrigger(self, result):
        pass

    def onKejuStart(self, kejuType, kejuNo):
        gamelog.info('@szh onKejuStart', kejuType, kejuNo)
        gameglobal.rds.ui.kejuGuide.show()

    def onKejuEnd(self, kejuType, kejuNo):
        gamelog.info('@szh onKejuEnd', kejuType, kejuNo)
        gameglobal.rds.ui.kejuGuide.hidePush()
        if gameglobal.rds.ui.kejuGuide.mediator:
            gameglobal.rds.ui.kejuGuide.hide()

    def onKejuRoundFinish(self, kejuType, kejuNo):
        gamelog.info('@szh onKejuRoundFinish', kejuType, kejuNo)
        gameglobal.rds.ui.puzzle.updateRoundFinish()

    def onAnswerKeju(self, kejuType, puzzleId, answerId, res):
        gamelog.info('@szh onAnswerKeju', kejuType, puzzleId, answerId, res)
        if gameglobal.rds.ui.puzzle.mediator:
            gameglobal.rds.ui.puzzle.puzzleAnswerUpdateByKeJu()

    def onUseItemRmWrongAnswer(self, kejuType, rmId):
        if gameglobal.rds.ui.puzzle.mediator:
            gameglobal.rds.ui.puzzle.setWrongAnswer()
        gamelog.info('@szh onUseItemRmWrongAnswer', kejuType, rmId)

    def onPushQuiz(self, puzzleId, answers, delay, info):
        gamelog.debug('@zq onPushQuiz', puzzleId, answers, delay, info)
        if gameglobal.rds.ui.diGongPuzzle.widget:
            gameglobal.rds.ui.diGongPuzzle.updateInfo(puzzleId, answers, delay, info)
        else:
            gameglobal.rds.ui.diGongPuzzle.show(puzzleId, answers, delay, info)
        gameglobal.rds.sound.playSound(4825)

    def set_digongPuzzleInfo(self):
        gamelog.debug('@PGF:set_digongPuzzleInfo', self.digongPuzzleInfo)
        if gameglobal.rds.ui.diGongPuzzle.widget:
            gameglobal.rds.ui.diGongPuzzle.stepTimeOver()

    def onUpdatePairPuzzleAnswers(self, pairPuzzleVal):
        gamelog.debug('cgy#onUpdatePairPuzzleAnswers: ', pairPuzzleVal)

    def onPairPuzzleStart(self, pairPuzzlesList):
        gamelog.debug('cgy#onPairPuzzleStart: ', pairPuzzlesList)
