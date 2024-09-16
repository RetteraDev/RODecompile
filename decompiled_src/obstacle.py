#Embedded file name: /WORKSPACE/data/entities/client/obstacle.o
import BigWorld
import Math
import utils
import gameglobal
import gametypes
import combatProto
import clientcom
from iClient import IClient
from helpers import fashion
from helpers import modelServer
from helpers import ufo
from callbackHelper import Functor
from sfx import flyEffect
from iAbstractCombatUnit import IAbstractCombatUnit
from data import obstacle_data as OCD

class Obstacle(IClient, IAbstractCombatUnit):
    IsObstacle = True
    TOPLOGO_OFFSET = 0.5
    COLLIDE_CNT = 10

    def __init__(self):
        super(Obstacle, self).__init__()
        self.firstFetchFinished = False
        self.topLogoOffset = OCD.data.get(self.oid, {}).get('logoOffset', Obstacle.TOPLOGO_OFFSET)
        self.collideCnt = 0
        self.obstacleModel = None
        self.lastDamageTime = 0.0
        self.damageIntervalTime = OCD.data.get(self.oid, {}).get('damageInterval', 0.3)

    def enterWorld(self):
        super(Obstacle, self).enterWorld()
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.initYaw = self.yaw
        self.modelServer = modelServer.SimpleModelServer(self)
        self.isLeaveWorld = False
        self.roleName = OCD.data.get(self.oid, {}).get('name', '')

    def getItemData(self):
        return OCD.data.get(self.oid, {'model': gameglobal.defaultModelID})

    def leaveWorld(self):
        if hasattr(self, 'modelServer') and self.modelServer:
            self.modelServer.release()
            self.modelServer = None
        if self.fashion != None:
            self.fashion.attachUFO(ufo.UFO_NULL)
            self.fashion.release()
            self.fashion = None
        if self.topLogo != None:
            self.topLogo.release()
            self.topLogo = utils.MyNone
        self.isLeaveWorld = True
        self.removeAllFx()
        self.delObstacleFollower()
        super(Obstacle, self).leaveWorld()

    def _initZhongBaiAction(self, data):
        initZhongBaiAction = data.get('initZhongBaiAction', False)
        if initZhongBaiAction:
            self.startZhongBaiAction()

    def startZhongBaiAction(self):
        castDelay = self.getItemData().get('castDelay', 0)
        BigWorld.callback(castDelay, self.playZhongBaiAction)

    def afterModelFinish(self):
        super(Obstacle, self).afterModelFinish()
        self.setTargetCapsUse(False)
        self.addObstacleFollow()
        self.firstFetchFinished = True
        self.checkCollideWithPlayer()
        scale = OCD.data.get(self.oid, {}).get('scale', 0)
        self.model.scale = (scale, scale, scale)
        if OCD.data.get(self.oid, {}).get('mirror', 0):
            oldScale = self.model.scale
            self.model.scale = (-oldScale[0], oldScale[1], oldScale[2])
        self._initZhongBaiAction(self.getItemData())
        self.filter = BigWorld.AvatarFilter()
        self.setExtraDirection()
        if self.isSceneObj():
            self.model.isSceneObj = True

    def startAction(self):
        if not self.firstFetchFinished:
            return
        if self.obstacleModel and not self.obstacleModel.attached:
            self.addModel(self.obstacleModel)
            self.obstacleModel.matrix = self.model.node('HP_head2')
        actionName = OCD.data.get(self.oid, {}).get('action0', None)
        if actionName and actionName in self.fashion.getActionNameList():
            self.model.action(actionName)()

    def playZhongBaiAction(self):
        if not self.inWorld:
            return
        data = self.getItemData()
        zhongBaiAction = data.get('zhongBaiAction', None)
        if zhongBaiAction and zhongBaiAction in self.fashion.getActionNameList():
            self.model.action(zhongBaiAction)()

    def stopZhongBaiAction(self):
        self.fashion.stopAllActions()

    def addObstacleFollow(self):
        self.obstacleModel = None
        modelId = OCD.data.get(self.oid, {}).get('obstacleModel', None)
        if not modelId:
            return
        scaleMatrix = Math.Matrix()
        if OCD.data.get(self.oid, {}).get('mirror', 0):
            scaleMatrix.setScale((-1.0, 1.0, 1.0))
        else:
            scaleMatrix.setScale((1.0, 1.0, 1.0))
        mp = Math.MatrixProduct()
        mp.a = scaleMatrix
        mp.b = self.matrix
        modelPath = 'char/' + str(modelId) + '/' + str(modelId) + '.model'
        BigWorld.fetchObstacleModel(modelPath, mp, True, self.realFollow)

    def realFollow(self, model):
        if not self.inWorld:
            return
        if model:
            self.obstacleModel = model
            self.addModel(self.obstacleModel)
            followNodeName = OCD.data.get(self.oid, {}).get('followNodeName', None)
            if followNodeName:
                followNode = self.model.node(followNodeName)
            else:
                followNode = self.model.node('HP_head2')
            self.obstacleModel.matrix = followNode
            self.obstacleModel.setEntity(self.id)
            self.oldPosition = self.obstacleModel.position
            self.checkCollideWithPlayer()

    def delObstacleFollower(self):
        if self.obstacleModel and self.obstacleModel.attached:
            self.delModel(self.obstacleModel)
        self.obstacleModel = None

    def doDamage(self):
        player = BigWorld.player()
        if not player.inWorld:
            return
        time = BigWorld.time()
        if time - self.lastDamageTime > self.damageIntervalTime:
            self.lastDamageTime = time
            self.cell.calcObstacleDmg([player.id])

    def obstacleResultPB(self, bytes):
        self.obstacleResult(*combatProto.mfResultProtoClient(bytes))

    def obstacleResult(self, obId, obType, lv, results, srcSkillId, srcSkillLv, rPosList):
        for resultSet in results:
            beAttack = BigWorld.entity(resultSet.eid)
            host = None
            for pair in resultSet.results:
                host = BigWorld.entity(pair.srcId)
                if not beAttack or not beAttack.inWorld:
                    continue
                if not beAttack.IsCombatUnit:
                    return
                beAttack.damage(host, pair.dmgs, pair.damageAbsorb, pair.mps, pair.ars)
                if pair.hps:
                    beAttack.damage(host, (pair.hps,), [], pair.mps, gametypes.UI_BE_HEAL)
                beAttack.beHit(host, (sum(pair.dmgs), pair.ars))

            if resultSet.kill:
                if not beAttack or not beAttack.inWorld:
                    continue
                if not beAttack.IsCombatUnit:
                    return
                beAttack.die(host)
            else:
                self.processMoveDamage(resultSet.eid)

    def checkCollideWithPlayer(self):
        player = BigWorld.player()
        if not self.inWorld:
            return
        if not self.obstacleModel or not self.obstacleModel.inWorld or not self.obstacleModel.collidable:
            return
        followNodeName = OCD.data.get(self.oid, {}).get('followNodeName', None)
        if followNodeName:
            return
        model = self.obstacleModel
        delta = model.position.distTo(self.oldPosition)
        if self.isIntersectWithPlayer(model):
            if delta > 2.0:
                self.oldPosition = model.position
                self.doDamage()
            else:
                self.collideCnt += 1
                if self.collideCnt > Obstacle.COLLIDE_CNT:
                    self.collideCnt = 0
                    self.cell.calcObstacleDmg([player.id])
        BigWorld.callback(0.1, self.checkCollideWithPlayer)

    def isIntersectWithPlayer(self, model):
        pos = BigWorld.player().position
        minbd = model.pickbdbox[0] - Math.Vector3(0.5, 2, 0.5)
        maxbd = model.pickbdbox[1] + Math.Vector3(0.5, 0, 0.5)
        return clientcom.isInBoundingBox(minbd, maxbd, pos)

    def processMoveDamage(self, entityId):
        player = BigWorld.player()
        if player.id != entityId:
            return
        if player.life == gametypes.LIFE_DEAD:
            return
        if player.isAscending:
            return
        theta = OCD.data.get(self.oid, {}).get('theta', -90.0)
        dist = OCD.data.get(self.oid, {}).get('dist', 5.0)
        speed = OCD.data.get(self.oid, {}).get('speed', 6.0)
        player.physics.collide = False
        realDist = dist - player.position.flatDistTo(self.position)
        dstPos = flyEffect.getRelativePosition(player.position, self.yaw, theta, realDist)
        dstPos = Math.Vector3(dstPos[0], dstPos[1], dstPos[2])
        ap = player.ap
        ap.setSpeed(speed)
        player.physics.maxVelocity = 0
        ap.beginForceMoveWithCallback(dstPos, Functor(self._approachDstPos))

    def _approachDstPos(self, success):
        player = BigWorld.player()
        if not player or not player.inWorld:
            return
        player.physics.collide = True
        player.isAscending = False
        ap = player.ap
        ap.setSpeed(player.speed[gametypes.SPEED_MOVE] / 60.0)
        ap._endForceMove(success)
        player.updateActionKeyState()

    def needBlackShadow(self):
        return not self.getItemData().get('noBlackUfo', False)

    def stopAction(self):
        if self.obstacleModel and self.obstacleModel.attached:
            self.delModel(self.obstacleModel)

    def isSceneObj(self):
        if getattr(self.model, 'isSceneObj', False):
            return self.getItemData().get('isSceneObj', False)
        return False
