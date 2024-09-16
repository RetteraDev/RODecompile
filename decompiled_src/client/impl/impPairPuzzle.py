#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPairPuzzle.o
import BigWorld
import pairPuzzle
import gameglobal
import gamelog

class ImpPairPuzzle(object):

    def onUpdatePairPuzzleAnswers(self, pairPuzzleVal):
        gamelog.debug('cgy#onUpdatePairPuzzleAnswers: ', type(pairPuzzleVal), pairPuzzleVal)
        gameglobal.rds.ui.pairPuzzle.updatePuzzleVal(pairPuzzleVal)

    def onPairPuzzleStart(self, pairPuzzlesList):
        gamelog.debug('cgy#onPairPuzzleStart: ', pairPuzzlesList)
        gameglobal.rds.ui.pairPuzzle.setPuzzleData(pairPuzzlesList)
