#Embedded file name: I:/bag/tmp/tw2/res/entities\common/pairPuzzleInfo.o
from userInfo import UserInfo
from pairPuzzle import PairPuzzle

class PairPuzzleInfo(UserInfo):

    def createObjFromDict(self, dict):
        puzzle = PairPuzzle(pairPuzzleGbId=dict['pairPuzzleGbId'], pairPuzzleBox=dict['pairPuzzleBox'], pairPuzzleNUID=dict['pairPuzzleNUID'], allPuzzles=dict['allPuzzles'], currPuzzleIdx=dict['currPuzzleIdx'], puzzleState=dict['puzzleState'])
        return puzzle

    def getDictFromObj(self, obj):
        return {'pairPuzzleGbId': obj.pairPuzzleGbId,
         'pairPuzzleBox': obj.pairPuzzleBox,
         'pairPuzzleNUID': obj.pairPuzzleNUID,
         'allPuzzles': obj.allPuzzles,
         'currPuzzleIdx': obj.currPuzzleIdx,
         'puzzleState': obj.puzzleState}

    def isSameType(self, obj):
        return type(obj) is PairPuzzle


instance = PairPuzzleInfo()
