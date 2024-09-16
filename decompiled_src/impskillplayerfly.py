#Embedded file name: /WORKSPACE/data/entities/client/helpers/impskillplayerfly.o
import math
import random
import BigWorld
import Math
import gamelog
import gameglobal
import gametypes
import skillDataInfo
import utils
import clientcom
from callbackHelper import Functor
from sfx import sfx
from sfx import clientEffect
FLYER_NONE = -1
FLYER_START = 1
FLYER_APPROACH = 2
PLAYER_MODEL_POSITION = 1
RIGHT_WEAPON_POSITION = 2
LEFT_WEAPON_POSITION = 3

class ImpSkillPlayerFly(object):

    def _flyerStart(self, skillID):
        if self.flyerSync.has_key(skillID):
            self.flyerSync[skillID].append(FLYER_START)
        else:
            self.flyerSync[skillID] = [FLYER_START]

    def _flyerApproach(self, skillID):
        data = self.flyerSync.get(skillID, None)
        if data:
            for i, value in enumerate(data):
                if value == FLYER_START:
                    data[i] = FLYER_APPROACH
                    break

    def _flyerCheck(self, skillID):
        data = self.flyerSync.get(skillID, None)
        if data and len(data):
            if data[0] == FLYER_APPROACH:
                data.pop(0)
                return FLYER_APPROACH
            else:
                return FLYER_START
        return FLYER_NONE

    def pushFlyTargets(self, skillID, flyTargets):
        if not flyTargets:
            return
        if self.flyTargets.has_key(skillID):
            if len(self.flyTargets[skillID]) >= 5:
                self.flyTargets[skillID].pop(0)
            self.flyTargets[skillID].append(flyTargets)
        else:
            self.flyTargets[skillID] = [flyTargets]

    def popFlyTargets(self, skillID, tgt):
        if not tgt:
            return True
        if skillID not in self.flyTargets:
            return False
        needRm = -1
        flag = False
        for i in range(0, len(self.flyTargets[skillID])):
            flyTargets = self.flyTargets[skillID][i]
            if tgt in flyTargets:
                flyTargets.remove(tgt)
                if len(flyTargets) == 0:
                    needRm = i
                    flag = True
                break

        if -1 < needRm < len(self.flyTargets[skillID]):
            self.flyTargets[skillID].pop(needRm)
        return flag

    def flyPeriod(self, skillInfo, clientSkillInfo, castActionDuration, playAction = True, flyType = 0, moveId = 0, moveInfo = None, needCastDelay = True):
        owner = BigWorld.entity(self.owner)
        if owner == None:
            return
        skillID = skillInfo.num
        flyEffects = self.getFlyEffect(clientSkillInfo)
        if flyType > 0:
            gamelog.debug('lihang@flyPeriod', moveInfo, moveId)
            self._flyPeriodFunc(skillInfo, clientSkillInfo, None, playAction, moveInfo, moveId)
            if self.target and flyEffects:
                self._defaultFlyPeriod(skillInfo, clientSkillInfo, self.target, flyEffects, needCastDelay=needCastDelay)
            return
        target = self.target
        flySpeed = skillDataInfo.getFlySpeed(skillInfo)
        gamelog.debug('bgf:fly', flyEffects, target, flySpeed, self.targetPos)
        if flyEffects == None or flySpeed == 0:
            effect = skillDataInfo.getSkillEffects(clientSkillInfo, gameglobal.S_FLYDEST)
            targetPos = self.targetPos
            if skillDataInfo.needFlyDestGround(clientSkillInfo):
                targetPos = self._calGroundPos(self.targetPos)
            if effect and targetPos:
                for ef in effect:
                    fxDelayTime = skillDataInfo.getCastTime(skillInfo)
                    if not fxDelayTime:
                        fxDelayTime = 10
                    else:
                        fxDelayTime = fxDelayTime + 1
                    fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (owner.getSkillEffectLv(),
                     owner.getSkillEffectPriority(),
                     None,
                     ef,
                     sfx.EFFECT_LIMIT,
                     targetPos,
                     0,
                     0,
                     0,
                     fxDelayTime))
                    if fx:
                        self.targetPosFx.extend(fx)
                        shakeCameras = skillDataInfo.getFlyDestShakeCameras(clientSkillInfo)
                        sfx.playShakeCamera(shakeCameras, self.owner)

            self.noFlyProcessDamage(skillInfo, clientSkillInfo)
            self.guideStopPos = targetPos
            self.targetPos = None
            return
        tgts = []
        if playAction and skillInfo.num in self.damageResult:
            for i in xrange(0, len(self.damageResult[skillID])):
                result = self.damageResult[skillID][len(self.damageResult[skillID]) - 1 - i]
                for pair in result:
                    tgts.append(pair.eid)

                if target and (target.id in tgts or owner.id == target.id):
                    break
                else:
                    tgts = []

        forceSkillClientCalc = gameglobal.rds.configData.get('forceSkillClientCalc', False)
        singleFly = skillDataInfo.isSingleFlyResult(clientSkillInfo)
        if forceSkillClientCalc and self.target and singleFly:
            tgts = [self.target.id]
        if target and target.id not in tgts:
            tgts.append(target.id)
        self.releaseEffectConnectorExcept(tgts)
        if self.targetPos:
            targetPos = self.targetPos
            if skillDataInfo.needFlyDestGround(clientSkillInfo):
                targetPos = self._calGroundPos(self.targetPos)
            self._defaultFlyTargetPos(skillInfo, clientSkillInfo, targetPos, flyEffects)
        else:
            self.pushFlyTargets(skillID, tgts)
            for idx, tgtID in enumerate(tgts):
                tgt = BigWorld.entities.get(tgtID)
                curveNeedProcessDmg = idx == 0
                self._defaultFlyPeriod(skillInfo, clientSkillInfo, tgt, flyEffects, curveNeedProcessDmg, needCastDelay=needCastDelay)

        self.targetPos = None

    def _defaultFlyTargetPos(self, skillInfo, clientSkillInfo, targetPos, effects):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        self.delayDamageCalc += 1
        attachedEffects = []
        flySpeed = skillDataInfo.getFlySpeed(skillInfo)
        flyType = skillDataInfo.getFlyType(clientSkillInfo)
        rotateFlySpeed = Math.Vector3(0.0, 0.0, 0.0)
        curvature = 0
        zroll = 0
        startNode = None
        startNodeName = skillDataInfo.getFlySrcNode(clientSkillInfo)
        startPos = None
        if startNodeName:
            startNode = owner.model.node(startNodeName)
        else:
            startNode = owner.model.node(gameglobal.HIT_NODE_MAP[gameglobal.NORMAL_HIT])
        if startNode:
            mat = Math.Matrix(startNode)
            startPos = mat.applyToOrigin()
        if startPos == None:
            position = clientcom.getModeNodePosition(owner.model, gameglobal.RIGHT_HAND_NODE_NAME)
            bias = position.y - owner.position.y if position else 0
            startPos = owner.position + Math.Vector3(0, bias, 0)
        if flyType == gameglobal.FLYER_CURVE:
            curvature = skillDataInfo.getCurvature(clientSkillInfo)
            zroll = skillDataInfo.getFlyZroll(clientSkillInfo)
            rotateFlySpeed = Math.Vector3(skillDataInfo.getRotateFlySpeed(clientSkillInfo))
            flySpeed *= 1.05
        elif flyType == gameglobal.FLYER_RANDOM:
            rotateFlySpeed = Math.Vector3(random.randint(0, 10), random.randint(0, 10), random.randint(0, 10))
            zroll = random.randint(-10, 10) * 0.1
            curvature = 0.15 + random.randint(0, 10) * 0.01
        model = sfx.getDummyModel()
        model.visible = False
        model.position = self.targetPos
        targetNode = model.node('Scene Root')
        BigWorld.callback(5, Functor(sfx.giveBackDummyModel, model))
        flyer = sfx.FlyToNode(Functor(self.endFly, skillInfo, clientSkillInfo, attachedEffects, None, None))
        for ef in effects:
            attached = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
             owner.getSkillEffectPriority(),
             flyer.model,
             ef,
             sfx.EFFECT_LIMIT,
             -1,
             targetPos))

        if attached != None:
            for ae in attached:
                attachedEffects.append(ae)

        self._flyerStart(skillInfo.num)
        castDelay = skillDataInfo.getCastDelay(owner, skillInfo)
        flyDestEff = skillDataInfo.getSkillEffects(clientSkillInfo, gameglobal.S_FLYDEST)
        if targetNode:
            shakeCameras = skillDataInfo.getFlyDestShakeCameras(clientSkillInfo)
            BigWorld.callback(castDelay, Functor(flyer.start, startPos, targetNode, curvature, zroll, flySpeed, attachedEffects, 0, True, rotateFlySpeed, flyDestEff, None, shakeCameras, owner))

    def delayFlyerStart(self, clientSkillInfo, flyer, targetNode, curvature, zroll, flySpeed, attachedEffects, acceleration, flyAccFlag, rotateFlySpeed, flyDestEff, flyTarget, shakeCameras, target, isSucker = False):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        startNode = None
        startNodeName = skillDataInfo.getFlySrcNode(clientSkillInfo)
        startPos = None
        if startNodeName:
            flySrcNodeType = skillDataInfo.getFlySrcNodeType(clientSkillInfo)
            if flySrcNodeType == gametypes.FLY_SRC_NODE_TYPE_LEFT_WEAPON:
                if owner.modelServer.leftWeaponModel and owner.modelServer.leftWeaponModel.model:
                    try:
                        startNode = owner.modelServer.leftWeaponModel.model.node(startNodeName)
                    except:
                        pass

            if not startNode:
                startNode = owner.model.node(startNodeName)
        else:
            startNode = owner.model.node(gameglobal.HIT_NODE_MAP[gameglobal.NORMAL_HIT])
        if startNode:
            mat = Math.Matrix(startNode)
            startPos = mat.applyToOrigin()
        if startPos == None:
            position = clientcom.getModeNodePosition(owner.model, gameglobal.RIGHT_HAND_NODE_NAME)
            bias = position.y - owner.position.y if position else 0
            startPos = owner.position + Math.Vector3(0, bias, 0)
        flyer.start(startPos, targetNode, curvature, zroll, flySpeed, attachedEffects, acceleration, flyAccFlag, rotateFlySpeed, flyDestEff, flyTarget, shakeCameras, target, isSucker)
        hideWeaponInFlyNode = skillDataInfo.hideWeaponInFlyNode(clientSkillInfo)
        if hideWeaponInFlyNode:
            owner.showLeftWeaponModels(False, True)
            owner.showRightWeaponModels(False, True)

    def releaseEffectConnectorExcept(self, tgts):
        if tgts and self.effectConnector:
            needRemove = set([])
            for tgtId in self.effectConnector.keys():
                if tgtId not in tgts:
                    needRemove.add(tgtId)

            for tgtId in needRemove:
                e = self.effectConnector.pop(tgtId)
                if e:
                    e.release()

    def _defaultFlyPeriod(self, skillInfo, clientSkillInfo, target, effects, curveNeedProcessDmg = True, needCastDelay = True):
        if not target or not target.inWorld:
            return
        if not getattr(target, 'fashion'):
            return
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        if len(self.castCurveCue) > 0:
            self._flyerStart(skillInfo.num)
            self._cueCurveFly(skillInfo, clientSkillInfo, target, effects, curveNeedProcessDmg)
            return
        self.delayDamageCalc += 1
        attachedEffects = []
        flySpeed = skillDataInfo.getFlySpeed(skillInfo)
        flyType = skillDataInfo.getFlyType(clientSkillInfo)
        isSucker = skillDataInfo.isSuckerFlyer(clientSkillInfo)
        rotateFlySpeed = Math.Vector3(0.0, 0.0, 0.0)
        curvature = 0
        zroll = 0
        startNode = None
        startNodeName = skillDataInfo.getFlySrcNode(clientSkillInfo)
        endNodeName = skillDataInfo.getFlyEndNode(clientSkillInfo)
        gamelog.debug('zfflySpeed:flySpeed:', flySpeed, flyType, startNodeName, endNodeName)
        startPos = None
        endNode = None
        if startNodeName:
            flySrcNodeType = skillDataInfo.getFlySrcNodeType(clientSkillInfo)
            if flySrcNodeType == gametypes.FLY_SRC_NODE_TYPE_LEFT_WEAPON:
                if owner.modelServer.leftWeaponModel and owner.modelServer.leftWeaponModel.model:
                    try:
                        startNode = owner.modelServer.leftWeaponModel.model.node(startNodeName)
                    except:
                        pass

            if not startNode:
                startNode = owner.model.node(startNodeName)
        else:
            startNode = owner.model.node(gameglobal.HIT_NODE_MAP[gameglobal.NORMAL_HIT])
        if startNode:
            mat = Math.Matrix(startNode)
            startPos = mat.applyToOrigin()
        if endNodeName:
            endNode = target.model.node(endNodeName)
        if not endNode:
            endNode, endNodeName = target.getHitNodePairRandom(owner)
        if startPos == None:
            position = clientcom.getModeNodePosition(owner.model, gameglobal.RIGHT_HAND_NODE_NAME)
            bias = position.y - owner.position.y if position else 0
            startPos = owner.position + Math.Vector3(0, bias, 0)
        if flyType == gameglobal.FLYER_CURVE:
            curvature = skillDataInfo.getCurvature(clientSkillInfo)
            zroll = skillDataInfo.getFlyZroll(clientSkillInfo)
            rotateFlySpeed = Math.Vector3(skillDataInfo.getRotateFlySpeed(clientSkillInfo))
            flySpeed *= 1.05
        elif flyType == gameglobal.FLYER_RANDOM:
            rotateFlySpeed = Math.Vector3(random.randint(0, 10), random.randint(0, 10), random.randint(0, 10))
            zroll = random.randint(-10, 10) * 0.1
            curvature = 0.15 + random.randint(0, 10) * 0.01
        elif flyType == gametypes.FLYER_CONNECTION:
            if not self.effectConnector.has_key(target.id) and getattr(target, 'firstFetchFinished', True):
                skillMinRange, skillMaxRange = skillDataInfo.getSkillRange(skillInfo)
                for ef in effects:
                    gamelog.debug('skillMaxRange:', skillMaxRange, startNode, endNode)
                    if owner != target:
                        self.effectConnector[target.id] = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (owner.getSkillEffectLv(),
                         startNode,
                         ef,
                         endNode,
                         skillMaxRange + 30,
                         owner.getSkillEffectPriority()))

            self.processDamageAll(skillInfo, clientSkillInfo)
            self.delayDamageCalc -= 1
            return
        targetNode, flyTarget, endNodeName = self._calTargetNode(target, endNode, endNodeName)
        gamelog.debug('_defaultFlyPeriod endNodeName', endNodeName)
        if isSucker == gameglobal.FLYER_FLY_TO_PLAYER:
            flyer = sfx.FlyToNode(Functor(self.endFly, skillInfo, clientSkillInfo, attachedEffects, target.id, startNodeName))
        else:
            flyer = sfx.FlyToNode(Functor(self.endFly, skillInfo, clientSkillInfo, attachedEffects, target.id, endNodeName))
        if isSucker == gameglobal.FLYER_FLY_TO_PLAYER:
            self.processDamageAll(skillInfo, clientSkillInfo, target.id, None, True, False)
        targetPos = target.position
        attached = None
        if owner != flyTarget:
            for ef in effects:
                attached = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
                 owner.getSkillEffectPriority(),
                 flyer.model,
                 ef,
                 sfx.EFFECT_LIMIT,
                 -1,
                 targetPos))

        if attached != None:
            for ae in attached:
                attachedEffects.append(ae)

        gamelog.debug('zf119:fly to node ', attachedEffects, self.flyBias, attached)
        self._flyerStart(skillInfo.num)
        castDelay = skillDataInfo.getCastDelay(owner, skillInfo)
        if skillInfo.getSkillData('flyNoDelay', 0) and not needCastDelay:
            castDelay = 0
        flyDestEff = skillDataInfo.getSkillEffects(clientSkillInfo, gameglobal.S_FLYDEST)
        if targetNode:
            shakeCameras = skillDataInfo.getFlyDestShakeCameras(clientSkillInfo)
            if isSucker == gameglobal.FLYER_FLY_TO_PLAYER:
                if startNode != None:
                    BigWorld.callback(castDelay, Functor(flyer.start, startNode, targetNode, curvature, zroll, flySpeed, attachedEffects, 0, True, rotateFlySpeed, flyDestEff, flyTarget, shakeCameras, target, True))
                else:
                    BigWorld.callback(castDelay, Functor(self.delayFlyerStart, clientSkillInfo, flyer, targetNode, curvature, zroll, flySpeed, attachedEffects, 0, True, rotateFlySpeed, flyDestEff, flyTarget, shakeCameras, target, True))
            elif isSucker == gameglobal.FLYER_FLY_TO_TARGET:
                BigWorld.callback(castDelay, Functor(self.delayFlyerStart, clientSkillInfo, flyer, targetNode, curvature, zroll, flySpeed, attachedEffects, 0, True, rotateFlySpeed, flyDestEff, flyTarget, shakeCameras, target))

    def _cueCurveFly(self, skillInfo, clientSkillInfo, target, effects, curveNeedProcessDmg = True):
        if not target.inWorld:
            return
        if not getattr(target, 'fashion'):
            return
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        flyDestEff = skillDataInfo.getSkillEffects(clientSkillInfo, gameglobal.S_FLYDEST)
        curves = len(self.castCurveCue)
        self.curveCallbacks = []
        for idx in xrange(0, curves):
            curve = self.castCurveCue[idx]
            delayTime = curve[0]
            hitPercent = curve[1][0]
            curvature = curve[1][1]
            zroll = curve[1][2]
            self.delayDamageCalc += 1
            attachedEffects = []
            flast = idx == curves - 1
            isSucker = skillDataInfo.isSuckerFlyer(clientSkillInfo)
            targetNode, flyTarget, strHitNodeName = self._calTargetNode(target)
            gamelog.debug('_cueCurveFly strHitNodeName', strHitNodeName)
            flyer = sfx.FlyToNode(Functor(self._endFlyMulti, skillInfo, clientSkillInfo, attachedEffects, hitPercent, flast, target.id, strHitNodeName, curveNeedProcessDmg))
            if isSucker != gameglobal.FLYER_FLY_TO_TARGET:
                self.processCurveDamageAll(skillInfo, clientSkillInfo, hitPercent, False, target.id, strHitNodeName, curveNeedProcessDmg, True, False)
            targetPos = target.position
            flyType = skillDataInfo.getFlyType(clientSkillInfo)
            if flyType == gameglobal.FLYER_MULTI:
                if idx < len(effects):
                    ef = effects[idx]
                    attached = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
                     owner.getSkillEffectPriority(),
                     flyer.model,
                     ef,
                     sfx.EFFECT_LIMIT,
                     -1,
                     targetPos))
                    if attached != None:
                        for ae in attached:
                            attachedEffects.append(ae)

            else:
                for ef in effects:
                    if delayTime > 0:
                        BigWorld.callback(delayTime, Functor(self.attachCurvesEffects, flyer, ef, targetPos, attachedEffects))
                    else:
                        self.attachCurvesEffects(flyer, ef, targetPos, attachedEffects)

            flySpeed = skillDataInfo.getFlySpeed(skillInfo)
            gamelog.debug('_cueCurveFly', flySpeed, flyType, self.targetPos)
            nodeInfo = (curve[1][3], curve[1][4], curve[1][5])
            shakeCameras = skillDataInfo.getFlyDestShakeCameras(clientSkillInfo)
            handle = BigWorld.callback(delayTime, Functor(self._cueCurveRealFly, target, flyer, nodeInfo, curvature, zroll, flySpeed, attachedEffects, flyDestEff, targetNode, flyTarget, shakeCameras, owner, isSucker))
            self.curveCallbacks.append(handle)

    def attachCurvesEffects(self, flyer, ef, targetPos, attachedEffects):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        attached = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
         owner.getSkillEffectPriority(),
         flyer.model,
         ef,
         sfx.EFFECT_LIMIT,
         -1,
         targetPos))
        if attached != None:
            for ae in attached:
                attachedEffects.append(ae)

    def _calFlyNode(self, nodeInfo):
        owner = BigWorld.entity(self.owner)
        if owner and nodeInfo:
            startNode = nodeInfo[0]
            nodeType = nodeInfo[1]
            cordOffset = nodeInfo[2]
            models = []
            if nodeType == PLAYER_MODEL_POSITION:
                models = [owner.model]
            elif nodeType == RIGHT_WEAPON_POSITION:
                models = owner.fashion.getWeaponModels(gameglobal.WEAPON_RIGHT)
            elif nodeType == LEFT_WEAPON_POSITION:
                models = owner.fashion.getWeaponModels(gameglobal.WEAPON_LEFT)
            for model in models:
                node = model.node(startNode)
                if node:
                    gamelog.debug('@_calFlyNode', nodeInfo)
                    return self._getFlyStartPosition(owner, node, cordOffset)

            return owner.position + Math.Vector3(0, 1.5 + self.flyBias, 0)

    def _getFlyStartPosition(self, owner, node, cordOffset):
        x = y = z = 0
        postion = clientcom.getPositionByNode(node)
        if cordOffset and len(cordOffset) == 3:
            x, y, z = float(cordOffset[0]), float(cordOffset[1]), float(cordOffset[2])
        if x or y or z:
            vect = postion - owner.position + Math.Vector3(x, y, z)
            deltaYaw = vect.yaw + owner.yaw
            newVect = Math.Vector3(vect.length * math.sin(deltaYaw), vect.y, vect.length * math.cos(deltaYaw))
            gamelog.debug('@_getFlyStartPosition', cordOffset, owner.position, postion, vect, newVect)
            return newVect + owner.position
        else:
            return postion

    def _calTargetNode(self, target, endNode = None, endNodeName = None):
        owner = BigWorld.entity(self.owner)
        targetNode = None
        flyTarget = None
        if target and target.inWorld and owner:
            if self.targetPos:
                model = sfx.getDummyModel()
                model.visible = False
                model.position = self.targetPos
                targetNode = model.node('Scene Root')
                BigWorld.callback(5, Functor(sfx.giveBackDummyModel, model))
                self.targetPos = None
            else:
                if endNode:
                    targetNode = endNode
                else:
                    targetNode, endNodeName = target.getHitNodePairRandom(owner)
                flyTarget = target
        return (targetNode, flyTarget, endNodeName)

    def _cueCurveRealFly(self, target, flyer, nodeInfo, curvature, zroll, flySpeed, attachedEffects, flyDestEff, targetNode, flyTarget, shakeCameras, owner, isSucker = gameglobal.FLYER_FLY_TO_TARGET):
        startPos = self._calFlyNode(nodeInfo)
        if startPos and targetNode:
            if isSucker == gameglobal.FLYER_FLY_TO_TARGET:
                flyer.start(startPos, targetNode, curvature, zroll, flySpeed, attachedEffects, flyDestEff=flyDestEff, flyTarget=flyTarget, shakeCameras=shakeCameras, owner=owner)
            else:
                flyer.start(startPos, targetNode, curvature, zroll, flySpeed, attachedEffects, flyDestEff=flyDestEff, flyTarget=flyTarget, shakeCameras=shakeCameras, owner=owner, isSucker=True)

    def _endFlyMulti(self, skillInfo, clientSkillInfo, effects, hitPercent, flast, tgtID, strHitNodeName, curveNeedProcessDmg = True):
        gamelog.debug('_endFlyMulti', self, skillInfo.num, curveNeedProcessDmg)
        if self.curveCallbacks:
            self.curveCallbacks.pop(0)
        if self.delayDamageCalc > 0:
            self.delayDamageCalc -= 1
        if flast:
            self._flyerApproach(skillInfo.num)
        isSucker = skillDataInfo.isSuckerFlyer(clientSkillInfo)
        if isSucker == gameglobal.FLYER_FLY_TO_TARGET:
            self.processCurveDamageAll(skillInfo, clientSkillInfo, hitPercent, flast, tgtID, strHitNodeName, curveNeedProcessDmg)
        else:
            self.processCurveDamageAll(skillInfo, clientSkillInfo, hitPercent, flast, self.owner, strHitNodeName, curveNeedProcessDmg, True, True)

    def cutCurveEff(self, skillInfo, clientSkillInfo):
        l = len(self.curveCallbacks)
        for i in xrange(l):
            if self.delayDamageCalc > 0:
                self.delayDamageCalc -= 1
            BigWorld.cancelCallback(self.curveCallbacks[i])

        self.curveCallbacks = []
        self._flyerApproach(self.skillID)
        self.processCurveDamageAll(skillInfo, clientSkillInfo)

    def endFly(self, skillInfo, clientSkillInfo, effects, tgtID, strHitNodeName):
        gamelog.debug('endFly', effects)
        if self.delayDamageCalc > 0:
            self.delayDamageCalc -= 1
        self._flyerApproach(skillInfo.num)
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        self.targetPos = None
        isSucker = skillDataInfo.isSuckerFlyer(clientSkillInfo)
        if isSucker != gameglobal.FLYER_FLY_TO_PLAYER:
            self.processDamageAll(skillInfo, clientSkillInfo, tgtID, strHitNodeName)
        else:
            self.processDamageAll(skillInfo, clientSkillInfo, self.owner, strHitNodeName, True, True)
        for e in effects:
            e.delayGiveBack = True
            e.stop()

    def __delModelFromPlayer(self, model):
        if model and model.inWorld:
            BigWorld.player().delModel(model)
            model = None

    def _calGroundPos(self, pos):
        if not pos:
            return
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return pos
        if not owner.fashion.isPlayer:
            return pos
        gPos = BigWorld.findDropPoint(BigWorld.player().spaceID, pos + (0, 1, 0))
        if gPos:
            return gPos[0]
        return pos

    def processCurveDamageAll(self, skillInfo, clientSkillInfo, hitPercent = 100, fLast = True, tgtID = None, strHitNodeName = None, curveNeedProcessDmg = True, needTgtSpt = False, needPop = True):
        skillID = skillInfo.num
        parent = BigWorld.entity(self.owner)
        if parent == None:
            return
        if not self.damageResult.has_key(skillID) or not self.damageResult[skillID]:
            return
        if curveNeedProcessDmg:
            replaceResult = []
            findIndex = 0
            if needTgtSpt == False:
                damageResult = self.damageResult[skillID][0]
            else:
                find = False
                for results in self.damageResult[skillID]:
                    replaceResult = []
                    for idx, resultSet in enumerate(results):
                        if resultSet.eid == tgtID:
                            find = True
                            damageResult = results
                        else:
                            replaceResult.append(resultSet)

                    if find == True:
                        break
                    findIndex = findIndex + 1

                if find == False:
                    findIndex = 0
                    damageResult = self.damageResult[skillID][0]
            beAttackNum = len(damageResult)
            for resultSet in damageResult:
                if needTgtSpt == True:
                    if resultSet.eid != tgtID:
                        continue
                ent = BigWorld.entity(resultSet.eid)
                gamelog.debug('@PGF:curveDamageAll', resultSet.eid, tgtID)
                if ent != None:
                    damageSum = 0
                    hpSum = 0
                    for pair in resultSet.results:
                        damageSum += sum(pair.dmgs)
                        hpSum += pair.hps

                    hitNum = damageSum * hitPercent / 100
                    hpNum = hpSum * hitPercent / 100
                    if self.checkRedundantResult(resultSet.eid, hpNum, skillID):
                        continue
                    self._realAttackPoint(beAttackNum, hitNum, hpNum, resultSet, skillInfo, clientSkillInfo, strHitNodeName)

        if needTgtSpt == False:
            if fLast:
                if self.popFlyTargets(skillID, tgtID):
                    self._flyerCheck(skillID)
                    if len(self.damageResult[skillID]) > 0:
                        self.damageResult[skillID].pop(0)
        elif fLast:
            if needPop == True and self.popFlyTargets(skillID, tgtID) or needPop == False:
                self._flyerCheck(skillID)
                if len(replaceResult) == 0:
                    self.damageResult[skillID].remove(damageResult)
                else:
                    self.damageResult[skillID][findIndex] = replaceResult

    def checkRedundantResult(self, eid, hpNum, skillID):
        if eid == BigWorld.player().id and hpNum and self.flyTargets.get(skillID):
            re = []
            for tgts in self.flyTargets.get(skillID):
                if tgts:
                    re.extend(tgts)

            if eid not in re:
                return True
        return False

    def processDelayDamageAll(self, skillInfo = None, skillClientInfo = None, damageResult = None):
        gamelog.debug('bgf:processDelayDamageAll', self.delayDamageCalc)
        if not skillInfo:
            skillID = self.skillID
        else:
            skillID = skillInfo.num
        needPlayClientEffType = skillDataInfo.isNeedPlayClientEffect(skillClientInfo)
        if clientEffect.playClientEffectFuncMap.has_key(needPlayClientEffType):
            clientEffect.playClientEffectFuncMap[needPlayClientEffType](self, 0, skillInfo, skillClientInfo, damageResult, False, False)
        damTime, damBL = skillDataInfo.getSplitDamageData(skillClientInfo)
        flyerFlag = self._flyerCheck(skillID)
        if flyerFlag == FLYER_START and not damTime and not damBL:
            self.pushDamage(skillID, damageResult)
            return
        self.pushDamage(skillID, damageResult)
        parent = BigWorld.entity(self.owner)
        if parent == None:
            return
        if not self.damageResult.has_key(skillID) or not self.damageResult[skillID]:
            return
        damageResult = self.damageResult[skillID].pop(0)
        showHitEffIndexes = self._getShowHitEffIndexes(skillInfo, damageResult)
        gamelog.debug('--------showHitEffIndexes', showHitEffIndexes)
        beAttackNum = len(damageResult)
        for idx, resultSet in enumerate(damageResult):
            ent = BigWorld.entity(resultSet.eid)
            if ent != None:
                needHitEff = self._isShowHitEff(showHitEffIndexes, idx)
                needShake = utils.isResultCrit(resultSet)
                extInfo = {gameglobal.CRIT_CAM_SHAKE: needShake}
                ent.disturbSkillDamage(beAttackNum, parent, resultSet, skillInfo, skillClientInfo, True, extInfo, needHitEff, None)
            else:
                gamelog.error("ERROR:can\'t find entity id ", resultSet.eid)
