#Embedded file name: I:/bag/tmp/tw2/res/entities\client/iClanWarCreation.o
import Math
import BigWorld
import clientcom
from helpers import ufo

class IClanWarCreation(object):

    def set_inClanWar(self, old):
        self.refreshStateUI()

    def set_beAtkType(self, old):
        self.refreshStateUI()

    def refreshStateUI(self):
        if self.topLogo:
            self.topLogo.updateRoleName(self.topLogo.name)

    def refreshUfo(self):
        if hasattr(BigWorld.player(), 'targetLocked') and BigWorld.player().targetLocked == self:
            ufoType = ufo.UFO_NORMAL
            if BigWorld.player().isEnemy(self):
                ufoType = BigWorld.player().getTargetUfoType(self)
            if self.topLogo:
                self.topLogo.showSelector(*ufo.SELECTOR_ARGS_MAP[ufoType])

    def isIntersectWithPlayer(self, model):
        pos = BigWorld.player().position
        minbd = model.pickbdbox[0] - Math.Vector3(0.5, 2, 0.5)
        maxbd = model.pickbdbox[1] + Math.Vector3(0.5, 0, 0.5)
        return clientcom.isInBoundingBox(minbd, maxbd, pos)

    def checkCollideWithPlayer(self, dist = 2.0):
        model = self.obstacleModel
        player = BigWorld.player()
        if not model or not model.inWorld or not model.collidable or not player.ap:
            return
        if self.isIntersectWithPlayer(model):
            invMatrix = Math.Matrix(model.matrix)
            invMatrix.invert()
            localPos = invMatrix.applyPoint(player.position)
            if localPos.x < 0:
                dstPos = Math.Vector3(0, 0, -dist)
            else:
                dstPos = Math.Vector3(0, 0, dist)
            mat = Math.Matrix(model.matrix)
            dstPos = mat.applyPoint(dstPos)
            player.ap.beginForceMove(dstPos, False)
