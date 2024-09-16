#Embedded file name: /WORKSPACE/data/entities/client/helpers/blackeffectmanager.o
import BigWorld
import navigator
import formula
import Math
import gamelog
from gameclass import Singleton
from callbackHelper import Functor
import utils
SRC_FITTINGROOM = 1
SRC_WARDROBE = 2
SRC_EMOTE = 3

def getInstance():
    return BlackEffectManager.getInstance()


class BlackEffectManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.effectDict = {}

    def setBlackScreenEff(self, srcId, enable):
        if not hasattr(BigWorld, 'fittingRoom'):
            return
        if enable:
            self._openFittingRoomEffect(srcId)
        else:
            self._closeFittingRoomEffect(srcId)

    def _openFittingRoomEffect(self, srcId):
        self.effectDict[srcId] = True
        BigWorld.fittingRoom(True, 0.03, 0.03, 0.04)

    def _closeFittingRoomEffect(self, srcId):
        if srcId in self.effectDict:
            del self.effectDict[srcId]
        if not self.effectDict:
            BigWorld.fittingRoom(False, 0.2, 0.2, 0.3)
