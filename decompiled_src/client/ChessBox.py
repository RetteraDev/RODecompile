#Embedded file name: I:/bag/tmp/tw2/res/entities\client/ChessBox.o
import math
import BigWorld
import formula
import gameglobal
from iClient import IClient
from iDisplay import IDisplay
from sfx import sfx
from data import chess_box_data as CBD
from data import multiline_digong_data as MDD

class ChessBox(IClient, IDisplay):
    RADII = 1.0

    def __init__(self):
        super(ChessBox, self).__init__()
        self.attachedEffectId = None
        self.noSelected = True
        self.trapId = None
        self.enable = True

    def getItemData(self):
        return {}

    def needBlackShadow(self):
        return False

    def afterModelFinish(self):
        super(ChessBox, self).afterModelFinish()
        self.onChangePlayerChessBoxNo()

    def getTopLogoHeight(self):
        return CBD.data.get(self.chessBoxId, {}).get('heightOffset', 2)

    def onChangePlayerChessBoxNo(self):
        player = BigWorld.player()
        src, dst, triggered = player.chessBoxNo
        _, _, yaw = CBD.data.get(self.chessBoxId, {}).get('effectDirection', (0, 0, 0))
        effectId = 0
        if triggered:
            mlgNo = formula.getMLGNo(BigWorld.player().spaceNo)
            maxChessBoxNum = MDD.data.get(mlgNo, {}).get('maxChessBoxNums', 65)
            if self.chessBoxId == dst and self.chessBoxId != maxChessBoxNum:
                effectId = 3063
        elif not triggered:
            if self.chessBoxId == dst:
                effectId = 3064
            elif src != dst and self.chessBoxId == src:
                effectId = 3063
            elif src < self.chessBoxId < dst:
                effectId = 3061
            elif src > self.chessBoxId > dst:
                effectId = 3062
                yaw += math.pi
        if self.attachedEffectId > 0:
            if self.attachedEffectId != effectId:
                self.removeFx(self.attachedEffectId)
                self.attachedEffectId = 0
            else:
                return
        if effectId > 0:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             None,
             effectId,
             sfx.EFFECT_LIMIT_MISC,
             self.position,
             0,
             yaw,
             0,
             sfx.EFFECT_UNLIMIT))
            if fx:
                self.addFx(effectId, fx)
                self.attachedEffectId = effectId

    def enterWorld(self):
        super(ChessBox, self).enterWorld()
        self.filter = BigWorld.DumbFilter()
        self.onChangePlayerChessBoxNo()
        self.radii = CBD.data.get(self.chessBoxId, {}).get('radii', ChessBox.RADII)
        self._enableTrap(True)

    def _enableTrap(self, flag):
        if flag:
            if self.enable:
                self.trapId = BigWorld.addPot(self.matrix, self.radii, self.trapCallback)
        elif self.trapId:
            BigWorld.delPot(self.trapId)
            self.trapId = None

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if enteredTrap:
            p = BigWorld.player()
            if (self.position - p.position).lengthSquared > self.radii * self.radii:
                return
            if p.chessBoxNo[1] != self.chessBoxId or p.chessBoxNo[2]:
                return
            self.cell.triggerTrap()

    def leaveWorld(self):
        super(ChessBox, self).leaveWorld()
        if self.attachedEffectId > 0:
            self.removeFx(self.attachedEffectId)
            self.attachedEffectId = 0
        self._enableTrap(False)
