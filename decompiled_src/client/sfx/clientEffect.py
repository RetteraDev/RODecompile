#Embedded file name: I:/bag/tmp/tw2/res/entities\client\sfx/clientEffect.o
import math
import BigWorld
import Math
import gameglobal
import gamelog
import sfx
import skillDataInfo
from callbackHelper import Functor

def playClientCircleEffect(skillId, skillLv, owner, nodeName, angle = 360.0, radii = 1.0, speed = 1.0, force = 1.0, keepTime = 5.0, offset = 2.0):
    node = owner.model.node(nodeName)
    rootnode = owner.model.node('HP_root')
    if hasattr(BigWorld, 'addCircleForce'):
        BigWorld.addPythonCircleForce(node, rootnode, radii, speed, force, keepTime, offset)


def playClientSquareEffect(skillId, skillLv, owner, nodeName, length = 2.0, width = 2.0, moveDir = (0, 0, 1), speed = 1.0, force = 1.0):
    position = owner.position
    node = owner.model.node(nodeName)
    if node:
        position = node.position
    xDir = Math.Vector3(math.sin(owner.yaw), 0, math.cos(owner.yaw))
    if not moveDir[2] == 0:
        moveDir = Math.Vector3(-math.cos(owner.yaw), 0, math.sin(owner.yaw)) * moveDir[2]
    elif not moveDir[0] == 0:
        moveDir = xDir * moveDir[0]
        xDir = Math.Vector3(-math.cos(owner.yaw), 0, math.sin(owner.yaw))
    if hasattr(BigWorld, 'addSquareForce'):
        BigWorld.addSquareForce(position, xDir, moveDir, length, width, speed, force)


def playClientEffect3(skillPlayer, targetID, skillInfo, clientSkillInfo, damageResult, instant, playAction):
    owner = BigWorld.entity(skillPlayer.owner)
    startNodeName = skillDataInfo.getFlySrcNode(clientSkillInfo)
    effectConnector = []
    if startNodeName:
        startNode = owner.model.node(startNodeName)
    else:
        startNode = owner.getHitNodeRandom()
    effects = skillPlayer.getFlyEffect(clientSkillInfo)
    if not effects:
        effects = []
    target = BigWorld.entity(targetID)
    if target and target != owner and effects:
        endNode = target.getHitNodeRandom()
        if startNode and endNode:
            for ef in effects:
                effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (owner.getSkillEffectLv(),
                 startNode,
                 ef,
                 endNode,
                 50,
                 owner.getSkillEffectPriority()))
                effectConnector.append(effect)

            startNode = endNode
    if damageResult:
        for pair in damageResult:
            BigWorld.callback(0.2, Functor(skillPlayer.processDamageById, skillInfo, clientSkillInfo, pair))
            if pair.eid == targetID:
                continue
            target = BigWorld.entity(pair.eid)
            if target and target != owner:
                endNode = target.getHitNodeRandom()
                if not startNode or not endNode:
                    continue
                for ef in effects:
                    effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (owner.getSkillEffectLv(),
                     startNode,
                     ef,
                     endNode,
                     50,
                     owner.getSkillEffectPriority()))
                    effectConnector.append(effect)

                startNode = endNode

    BigWorld.callback(2, Functor(_releaseEffectConnector, effectConnector))


def playClientEffect5(skillPlayer, targetID, skillInfo, clientSkillInfo, damageResult, instant, playAction):
    owner = BigWorld.entity(skillPlayer.owner)
    startNodeName = skillDataInfo.getFlySrcNode(clientSkillInfo)
    effectConnector = []
    if startNodeName:
        startNode = owner.model.node(startNodeName)
    else:
        startNode = owner.getHitNodeRandom()
    effects = skillPlayer.getFlyEffect(clientSkillInfo)
    if not effects:
        effects = []
    target = BigWorld.entity(targetID)
    if damageResult:
        for pair in damageResult:
            BigWorld.callback(0.2, Functor(skillPlayer.processDamageById, skillInfo, clientSkillInfo, pair))
            if pair.eid == targetID:
                continue
            target = BigWorld.entity(pair.eid)
            if target and target != owner:
                endNode = target.getHitNodeRandom()
                if not startNode or not endNode:
                    continue
                for ef in effects:
                    effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (owner.getSkillEffectLv(),
                     startNode,
                     ef,
                     endNode,
                     50,
                     owner.getSkillEffectPriority()))
                    effectConnector.append(effect)

    BigWorld.callback(2, Functor(_releaseEffectConnector, effectConnector))


def delayPlayClientEffect6(skillPlayer, targetID, skillInfo, clientSkillInfo, damageResult, instant, playAction):
    owner = BigWorld.entity(skillPlayer.owner)
    startNodeName = skillDataInfo.getFlySrcNode(clientSkillInfo)
    effectConnector = []
    if startNodeName:
        startNode = owner.model.node(startNodeName)
    else:
        startNode = owner.getHitNodeRandom()
    effects = skillPlayer.getFlyEffect(clientSkillInfo)
    if not effects:
        effects = []
    if damageResult:
        for pair in damageResult:
            target = BigWorld.entity(pair.eid)
            if target and target != owner:
                endNode = target.getHitNodeRandom()
                if not startNode or not endNode:
                    continue
                for ef in effects:
                    effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (owner.getSkillEffectLv(),
                     startNode,
                     ef,
                     endNode,
                     50,
                     owner.getSkillEffectPriority()))
                    effectConnector.append(effect)

                startNode = endNode

    BigWorld.callback(2, Functor(_releaseEffectConnector, effectConnector))


def _releaseEffectConnector(effectConnector):
    for ec in effectConnector:
        gamelog.debug('_releaseEffectConnector')
        if ec:
            ec.detach()


playClientEffectFuncMap = {3: playClientEffect3,
 5: playClientEffect5,
 6: delayPlayClientEffect6}
