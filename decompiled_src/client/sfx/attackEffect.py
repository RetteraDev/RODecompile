#Embedded file name: I:/bag/tmp/tw2/res/entities\client\sfx/attackEffect.o
import random
import BigWorld
import gamelog
import gameglobal
import utils
import sfx
from callbackHelper import Functor
from data import creation_client_data as CD

def magicFieldHurt(attacker, mfId, mfType, lv, results, skillInfo, clientSkillInfo):
    creationData = CD.data[mfType]
    clientRefId = creationData.get('clientRefId', None)
    gamelog.debug('magicFieldHurt:', mfType, attacker.id, clientRefId, skillInfo.num, skillInfo.lv)
    magic = BigWorld.entity(mfId)
    if mfHurtFuncMap.has_key(clientRefId):
        mfHurtFuncMap[clientRefId](attacker, magic, results, creationData, skillInfo, clientSkillInfo)
        return True
    p = BigWorld.player()
    beAttackNum = len(results)
    for resultSet in results:
        ent = BigWorld.entity(resultSet.eid)
        if ent != None:
            needShake = utils.isResultCrit(resultSet)
            extInfo = {gameglobal.CRIT_CAM_SHAKE: needShake}
            extInfo[gameglobal.IGNORE_HIT_EFFECT] = True
            if attacker == p:
                extInfo['mfStateKit'] = p.mfStateKit
                ent.disturbSkillDamage(beAttackNum, attacker, resultSet, skillInfo, clientSkillInfo, True, extInfo, False, None)
            else:
                ent.disturbSkillDamage(beAttackNum, attacker, resultSet, skillInfo, clientSkillInfo, True, extInfo, False, None)
            isDmg, isHeal = getDmgHeal(resultSet)
            host = magic if magic else attacker
            if isDmg:
                triggerHitEffect = creationData.get('triggerHitEffect', None)
                playTriggerHitEffect(ent, host, triggerHitEffect)
            elif isHeal:
                triggerHitEffect = creationData.get('triggerHitHealEffect', None)
                playTriggerHitEffect(ent, host, triggerHitEffect)
            creationData = CD.data.get(mfType, {})
            if (isDmg or isHeal) and gameglobal.ENABLE_PLAYER_HIT_EFFECT:
                effectData = ent.getPlayerHitEffDataByCreation(creationData, resultSet)
                if effectData and (attacker and attacker == BigWorld.player() or ent == BigWorld.player()):
                    hitEffectDelay = effectData.get('hitEffectDelay', 0)
                    if hitEffectDelay:
                        BigWorld.callback(hitEffectDelay, Functor(ent.playAllHitEffect, effectData))
                    else:
                        ent.playAllHitEffect(effectData)

    return False


def playTriggerHitEffect(ent, attacker, triggerHitEffect):
    if triggerHitEffect:
        triggerHitEffect = list(triggerHitEffect)
        playType = triggerHitEffect.pop(0)
        if playType == 0:
            triggerHitEffect = [random.choice(triggerHitEffect)]
        strHitNode = gameglobal.HIT_NODE_MAP[gameglobal.NORMAL_HIT]
        ent.playHitEffect(attacker, triggerHitEffect, strHitNode)


def getDmgHeal(resultSet):
    isDmg = False
    isHeal = False
    if not resultSet or not resultSet.results:
        if getattr(resultSet, 'realDmg'):
            isDmg = True
            return (isDmg, isHeal)
        return (isDmg, isHeal)
    for pair in resultSet.results:
        realHost = BigWorld.entity(pair.srcId)
        if realHost:
            if pair.hps > 0:
                isHeal = True
            if pair.dmgs and sum(pair.dmgs) > 0:
                isDmg = True

    return (isDmg, isHeal)


def playClientEffect1(attacker, magic, results, creationData, skillInfo, clientSkillInfo):
    startNodeName = 'HP_head1'
    startNode = attacker.model.node(startNodeName)
    if not startNode:
        return
    effects = None
    effectData = creationData.get('flyEff', None)
    if effectData:
        effectData = list(effectData)
        num = effectData.pop(0)
        if num == 0:
            effects = [random.choice(effectData)]
        else:
            effects = effectData
    if not effects:
        return
    effectConnector = []
    beAttackNum = len(results)
    for resultSet in results:
        target = BigWorld.entity(resultSet.eid)
        if target != None:
            needShake = utils.isResultCrit(resultSet)
            extInfo = {gameglobal.CRIT_CAM_SHAKE: needShake}
            target.disturbSkillDamage(beAttackNum, attacker, resultSet, skillInfo, clientSkillInfo, True, extInfo)
            endNode = target.getHitNodeRandom()
            for ef in effects:
                if attacker != target:
                    effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (attacker.getSkillEffectLv(),
                     startNode,
                     ef,
                     endNode,
                     50,
                     attacker.getSkillEffectPriority()))
                    effectConnector.append(effect)

    BigWorld.callback(2, Functor(_releaseEffectConnector, effectConnector))


def playClientEffectRandomConnect(attacker, magic, results, creationData, skillInfo, clientSkillInfo):
    if not magic or not magic.inWorld:
        return
    magicPosition = magic.position
    startPosOffset = creationData.get('startPosOffset', (0, 0, 0))
    startPosition = magicPosition + startPosOffset
    motionMaxTime = creationData.get('motionMaxTime', 0)
    targetList = {}
    for resultSet in results:
        target = BigWorld.entity(resultSet.eid)
        if targetList.has_key(resultSet.eid):
            targetList[resultSet.eid].append(resultSet)
        else:
            targetList[resultSet.eid] = [resultSet]

    trueBeAttackNum = len(targetList)
    for eid in targetList:
        target = BigWorld.entity(eid)
        if trueBeAttackNum > 1:
            castAfterTime = random.uniform(0, motionMaxTime)
            BigWorld.callback(castAfterTime, Functor(_actEffectAndHit, trueBeAttackNum, targetList[eid], skillInfo, clientSkillInfo, attacker, creationData, target, startPosition))
        else:
            _actEffectAndHit(trueBeAttackNum, targetList[eid], skillInfo, clientSkillInfo, attacker, creationData, target, startPosition)


def _delModel(testModel):
    sfx.gDummyModelMgr.giveBack(testModel, True)


def _showDmgOnTarget(resultSetList, skillInfo, clientSkillInfo, attacker, target):
    for resultSet in resultSetList:
        if target and target.id == resultSet.eid:
            needShake = utils.isResultCrit(resultSet)
            extInfo = {gameglobal.CRIT_CAM_SHAKE: needShake}
            target.disturbSkillDamage(1, attacker, resultSet, skillInfo, clientSkillInfo, True, extInfo)


def _actEffectAndHit(beAttackNum, resultSetList, skillInfo, clientSkillInfo, attacker, creationData, target, startPosition):
    if not attacker or not attacker.inWorld:
        return
    effectData = creationData.get('flyEff', None)
    if effectData:
        effectData = list(effectData)
        num = effectData.pop(0)
        if num == 0:
            effects = [random.choice(effectData)]
        else:
            effects = effectData
    effRate = creationData.get('effRate', 1)
    playEffect = random.random() < effRate
    if not effects or playEffect == False:
        _showDmgOnTarget(resultSetList, skillInfo, clientSkillInfo, attacker, target)
        return
    shootKeepTime = creationData.get('shootKeepTime', 2)
    effectNumDifTime = creationData.get('effectNumDifTime', 0)
    if effectNumDifTime == 0:
        _showDmgOnTarget(resultSetList, skillInfo, clientSkillInfo, attacker, target)
    else:
        BigWorld.callback(effectNumDifTime, Functor(_showDmgOnTarget, resultSetList, skillInfo, clientSkillInfo, attacker, target))
    effectConnector = []
    for ef in effects:
        if attacker != target:
            if not target or not target.inWorld:
                continue
            endNode = target.getHitNodeRandom()
            effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR2, (attacker.getSkillEffectLv(),
             startPosition,
             ef,
             endNode,
             50,
             attacker.getSkillEffectPriority()))
            effectConnector.append(effect)

    BigWorld.callback(shootKeepTime, Functor(_releaseEffectConnector, effectConnector))


def _releaseEffectConnector(effectConnector):
    for ec in effectConnector:
        if ec:
            ec.detach()


mfHurtFuncMap = {1: playClientEffect1,
 2: playClientEffectRandomConnect}
