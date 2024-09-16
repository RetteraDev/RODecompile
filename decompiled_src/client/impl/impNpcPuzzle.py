#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcPuzzle.o
import gameglobal

class ImpNpcPuzzle(object):

    def getOpacityValueByPuzzle(self, opacityVal):
        if opacityVal[0] == gameglobal.OPACITY_HIDE:
            return opacityVal
        visibility = opacityVal[0]
        if self.isPuzzleClose:
            visibility = gameglobal.OPACITY_HIDE
        return (visibility, opacityVal[1])

    def set_isPuzzleClose(self, old):
        self.refreshOpacityState()
