#Embedded file name: I:/bag/tmp/tw2/res/entities\common/pairPuzzle.o
from userSoleType import UserSoleType
from userListType import UserListType
import gametypes

class PairPuzzle(UserSoleType):

    def __init__(self, pairPuzzleGbId = 0, pairPuzzleBox = None, pairPuzzleNUID = 0, allPuzzles = [], currPuzzleIdx = 0, puzzleState = 0):
        self.initData(pairPuzzleGbId, pairPuzzleBox, pairPuzzleNUID, allPuzzles, currPuzzleIdx, puzzleState)

    def initData(self, pairPuzzleGbId = 0, pairPuzzleBox = None, pairPuzzleNUID = 0, allPuzzles = [], currPuzzleIdx = 0, puzzleState = 0):
        self.pairPuzzleGbId = pairPuzzleGbId
        self.pairPuzzleBox = pairPuzzleBox
        self.pairPuzzleNUID = pairPuzzleNUID
        self.allPuzzles = allPuzzles
        self.currPuzzleIdx = currPuzzleIdx
        self.puzzleState = puzzleState

    def _lateReload(self):
        super(PairPuzzle, self)._lateReload()
        for v in self.allPuzzles:
            v.reloadScript()

    def resetAll(self):
        self.pairPuzzleGbId = 0
        self.pairPuzzleBox = None
        self.pairPuzzleNUID = 0
        self.allPuzzles = []
        self.currPuzzleIdx = 0
        self.puzzleState = 0

    def getPuzzleValByIdx(self, puzzleIdx):
        try:
            return self.allPuzzles[puzzleIdx]
        except IndexError:
            return None

    def getPuzzleCurrVal(self):
        return self.getPuzzleValByIdx(self.currPuzzleIdx)

    def isAllPuzzleCompleted(self):
        for puzzleVal in self.allPuzzles:
            if not puzzleVal.isPuzzleCompleted():
                return False

        return True

    def isInPairPuzzleState(self):
        return self.puzzleState == gametypes.PAIR_PUZZLE_PEER_STATE_BUILDED


class PairPuzzlesList(UserListType):

    def __init__(self, roleName = '', otherRoleName = ''):
        self.roleName = roleName
        self.otherRoleName = otherRoleName


class PairPuzzleVal(UserSoleType):

    def __init__(self, puzzleId = 0, puzzleDescType = 0, puzzleSelfAnswer = None, puzzleOtherAnswer = None, puzzleResult = 0):
        self.puzzleId = puzzleId
        self.puzzleDescType = puzzleDescType
        self.puzzleSelfAnswer = puzzleSelfAnswer
        self.puzzleOtherAnswer = puzzleOtherAnswer
        self.puzzleResult = puzzleResult

    def _lateReload(self):
        super(PairPuzzleVal, self)._lateReload()

    def isPuzzleCompleted(self):
        if self.puzzleSelfAnswer is not None and self.puzzleOtherAnswer is not None:
            return True
        return False

    def clearAnswer(self):
        self.puzzleSelfAnswer = None
        self.puzzleOtherAnswer = None
