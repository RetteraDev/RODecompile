#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPuppet.o
import gameglobal
import BigWorld
import Math
import sMath
import gamelog
import const
from sfx import flyEffect
from helpers import puppetNav
from data import skill_general_data as SGD

class ImpPuppet(object):

    def queryValidPosition(self, asyncId, nuid, entId, pos, oriPos):
        """
        :param asyncId:
        :param nuid
        :param entId:
        :param pos:
        :param oriPos:
        :return:
        TODO
        pos->newPos
        self.cell.onQueryValidPosition(asyncId, nuid, entId, newPos):
        """
        self.calcPuppetPosition(asyncId, nuid, entId, pos, oriPos)

    def transPuppetValidPosition(self, entId, targetPos, oriPos):
        heightArray = (0.6, 1.0, 1.4, 1.8, 2.2)
        oriPos = self._findDropPoint(oriPos)
        dPos = None
        length = 0
        for i, h in enumerate(heightArray):
            h2 = h
            destPos = BigWorld.collide(self.spaceID, (oriPos[0], oriPos[1] + h, oriPos[2]), (targetPos[0], oriPos[1] + h, targetPos[2]))
            if destPos:
                destLength = (Math.Vector3(oriPos[0], oriPos[1] + h, oriPos[2]) - destPos[0]).length
                if not length:
                    length = destLength
                    dPos = destPos[0]
                elif length > destLength:
                    length = destLength
                    dPos = destPos[0]

        if dPos:
            if length > const.PUPPET_POS_COLLIDE_OFFSET:
                oriPos2d = Math.Vector2(oriPos[0], oriPos[2])
                targetPos2d = Math.Vector2(dPos[0], dPos[2])
                dirVal = oriPos2d - targetPos2d
                dirVal.normalise()
                targetPos2d = targetPos2d + dirVal * const.PUPPET_POS_OFFSET
                dPos[0] = targetPos2d[0]
                dPos[2] = targetPos2d[1]
                return (True, self._findDropPoint(dPos))
            else:
                return (True, oriPos)
        return (False, self._findDropPoint(targetPos))

    def _findDropPoint(self, oriPos):
        pos = BigWorld.findDropPoint(self.spaceID, Math.Vector3(oriPos[0], oriPos[1] + 1.0, oriPos[2]))
        if pos:
            pos = pos[0]
            return pos
        return oriPos

    def calcPuppetPosition(self, asyncId, nuid, entId, targetPos, oriPos):
        pNavManager = puppetNav.getInstance()
        pNavManager.queryValidPosition(asyncId, nuid, entId, targetPos, self.validPositionCallback, oriPos)

    def validPositionCallback(self, result, data):
        gamelog.debug('@zq validPositionCallback', result, data)
        if result == puppetNav.NAV_SUCCESS:
            asyncId = data.get('asyncId', None)
            nuid = data.get('nuid', None)
            entId = data.get('entId', None)
            positions = data.get('positions', None)
            for i, pos in enumerate(positions):
                positions[i].y += const.PUPPET_POS_HEIGHT_OFFSET

            self.cell.onQueryValidPosition(asyncId, nuid, entId, positions)

    def testCalcPuppetPosition(self, entId):
        asyncId = 1
        nuid = 1
        en = BigWorld.entity(entId)
        if not en:
            return
        oriPos = en.position
        pNavManager = puppetNav.getInstance()
        pNavManager.queryValidPosition(asyncId, nuid, entId, self.position, self.testValidPositionCallback, oriPos)

    def testValidPositionCallback(self, result, data):
        gamelog.debug('@zq testValidPositionCallback', result, data)

    def queryRecastPosition(self, asyncId, nuid, entId, pos, oriPos):
        """
        :param asyncId:
        :param nuid:
        :param entId:
        :param pos:
        :param oriPos:
        :return:
        TODO
        pos->newPos
        self.cell.onQueryValidPosition(asyncId, nuid, entId, newPos):
        """
        isCollide, targetPos = self.transPuppetValidPosition(entId, pos, oriPos)
        result = True
        if isCollide:
            targetPos = Math.Vector3(targetPos)
            if sMath.distance2D(oriPos, targetPos) < const.PUPPET_POS_OFFSET:
                targetPos = oriPos
        self.cell.onQueryRecastPosition(asyncId, nuid, entId, targetPos, result)

    def checkUseSkill(self, asyncId, nuid, entId, skillId, srcPos, tgtPos):
        """
        :param asyncId:
        :param nuid:
        :param entId:
        :param skillId:
        :param srcPos:
        :param tgtPos:
        :return:
        """
        srcPos = Math.Vector3(srcPos)
        tgtPos = Math.Vector3(tgtPos)
        result = self._checkSkillCanUse(skillId, srcPos, tgtPos)
        self.cell.onCheckUseSkill(asyncId, nuid, entId, result)

    def _checkSkillCanUse(self, skillId, srcPos, tgtPos):
        skillData = SGD.data.get((skillId, 1), {})
        collideHeight = skillData.get('collideHeight', None)
        if collideHeight:
            thrustPos = flyEffect.getMyThrustPoint(srcPos, tgtPos, collideHeight, gameglobal.TREEMATTERKINDS)
            if not thrustPos:
                return False
        return True
