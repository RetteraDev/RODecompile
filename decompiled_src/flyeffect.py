#Embedded file name: /WORKSPACE/data/entities/client/sfx/flyeffect.o
import math
import BigWorld
import C_ui
import Math
import const
import utils
import gametypes
import gameglobal
import gamelog
import sfx
import clientUtils
from sMath import distance3D
from sMath import distance2D
from callbackHelper import Functor
from guis import cursor
from guis import hotkey as HK
from helpers import action as ACT
from data import skill_movement_data as SMD
from data import sys_config_data as SYSCD
bDropPoint = False
gDropPoint = None
motionBlurTime = 0.8
motionBlurScale = 0.2

def kickFly(skillPlayer, skillInfo, clientSkillInfo, playAction = True, moveInfo = None, moveId = 0):
    if not SMD.data.has_key(moveId):
        return
    md = SMD.data[moveId]
    speed = md.get('angleType', 0)
    dist = md.get('distance', 0)
    skillID = skillInfo.num
    player = BigWorld.player()
    owner = BigWorld.entity(skillPlayer.owner)
    if not skillPlayer.damageResult.has_key(skillID) or not skillPlayer.damageResult[skillID]:
        return
    for res in skillPlayer.damageResult[skillID][0]:
        if res.eid == player.id and player != owner:
            player.physics.setSpringForce(0, speed, 0, 0, float(dist) / speed)

    skillPlayer.processDamageAll(skillInfo, clientSkillInfo)


def finishKickBackFly(owner):
    if not owner or not owner.inWorld:
        return
    if owner == BigWorld.player():
        setMoveControl(owner, False)
        owner.ap.setSpeed(owner.speed[gametypes.SPEED_MOVE] / 60.0)
        owner.ap._endForceMove(True)
        owner.updateActionKeyState()
    else:
        owner.am.moveNotifier = owner.fashion.movingNotifier


def getTargetAngle(targetPos):
    player = BigWorld.player()
    posx = targetPos[0] - player.position[0]
    posz = targetPos[2] - player.position[2]
    sin = posx * math.cos(player.yaw) - math.sin(player.yaw) * posz
    cos = posx * math.sin(player.yaw) + posz * math.cos(player.yaw)
    return math.atan2(sin, cos)


def avatarDanDaoFly(dstPos, realDist, speed, moveData, callback):
    player = BigWorld.player()
    verticalSpeed = moveData.get('danDaoVerticalSpeed', 15)
    player.ap.setUpSpeedMultiplier()
    player.updateModelFreeze(-1.0)
    upDirSin = 0 if BigWorld.camera().direction[1] < 0 else BigWorld.camera().direction[1]
    if upDirSin > 0 and upDirSin < 1:
        verticalSpeed = verticalSpeed + speed * upDirSin
        speed = speed * (1 - upDirSin * upDirSin)
    angle = getTargetAngle(dstPos)
    zLocalSpeed = speed * math.cos(angle)
    xLocalSpeed = speed * math.sin(angle)
    speedBase = utils.getMoveSpeedBase(player)
    if HK.HKM[HK.KEY_FORWARD].isAnyDown():
        zLocalSpeed = zLocalSpeed + speedBase
    elif HK.HKM[HK.KEY_BACKWARD].isAnyDown():
        zLocalSpeed = zLocalSpeed - speedBase
    elif HK.HKM[HK.KEY_MOVELEFT].isAnyDown():
        xLocalSpeed = xLocalSpeed - speedBase
    elif HK.HKM[HK.KEY_MOVERIGHT].isAnyDown():
        xLocalSpeed = xLocalSpeed + speedBase
    player.physics.velocity = Math.Vector3(xLocalSpeed, verticalSpeed, zLocalSpeed)
    player.physics.maxTopVelocity = Math.Vector3(xLocalSpeed, verticalSpeed, zLocalSpeed)
    player.physics.maxVelocity = speed + verticalSpeed
    player.physics.gravity = 10
    canRotateCursor = moveData.get('canRotateCursor', False)
    if canRotateCursor:
        player.physics.keepJumpVelocity = False
    else:
        player.ap.dcursor.canRotate = False
        player.physics.keepJumpVelocity = True
    player.physics.jump(True, True)
    try:
        moveStarAction = moveData.get('moveStarAction', None)
        if moveStarAction:
            actions = [moveStarAction]
            moveLoopAction = moveData.get('moveLoopAction', None)
            if moveLoopAction:
                actions.append(moveLoopAction)
            player.fashion.playActionSequence(player.model, actions, None, 1, 0, releaseFx=False)
        else:
            fallAction = player.fashion.action.getFallRunDownAction(player.fashion)
            player.fashion.stopAllActions()
            player.model.action(fallAction)()
    except:
        pass

    BigWorld.player().inDanDao = True
    BigWorld.player().danDaoUseDir = canRotateCursor
    player.resetHorizontalMove()
    player.avatarDanDaoCB = Functor(danDaoOver, callback)
    player.avatarDanDaoCancelCB = BigWorld.callback(5, cancelAvatarDanDao)


def cancelAvatarDanDao():
    p = BigWorld.player()
    if hasattr(p, 'avatarDanDaoCB') and p.avatarDanDaoCB:
        p.avatarDanDaoCB()
        p.avatarDanDaoCB = None
        p.clearAvatarDanDaoCancelCB()


def danDaoOver(callback):
    player = BigWorld.player()
    player.physics.jump(False)
    player.ap.afterJumpEnd()
    player.physics.keepJumpVelocity = False
    player.fashion.stopAllActions()
    BigWorld.player().inDanDao = False
    BigWorld.player().danDaoUseDir = False
    player.resetHorizontalMove()
    if callback:
        callback()


def _findDropPoint(pos):
    p = BigWorld.player()
    pos = BigWorld.findDropPoint(p.spaceID, Math.Vector3(pos[0], pos[1] + 5.0, pos[2]))
    if pos:
        pos = pos[0]
        return pos


def _checkCollide(startPos, endPos, ignoreMatKind = 0, getPos = None):
    heightArray = (1.1, 1.6, 2.1, 2.6)
    p = BigWorld.player()
    for h in heightArray:
        if ignoreMatKind > 0:
            dropPos = BigWorld.collide(p.spaceID, (startPos[0], startPos[1] + h, startPos[2]), (endPos[0], endPos[1] + h, endPos[2]), ignoreMatKind)
        else:
            dropPos = BigWorld.collide(p.spaceID, (startPos[0], startPos[1] + h, startPos[2]), (endPos[0], endPos[1] + h, endPos[2]))
        if dropPos:
            if isinstance(getPos, list):
                getPos.append(dropPos[0][0])
                getPos.append(dropPos[0][1])
                getPos.append(dropPos[0][2])
            return True

    return False


def _updateCursor():
    if cursor.oldCursorPosValid():
        cursor.setInAndRestoreOldPos()
        C_ui.cursor_show(True)


def _approachTowardTarget(owner, isUnPin, success):
    if not owner or not owner.inWorld:
        return
    gamelog.debug('_approachTowardTarget:', owner.id, success)
    if hasattr(owner.model, 'beholded') and owner.model.beholded:
        owner.model.beholded = False
        owner.updateModelFreeze(-1.0)
    if owner == BigWorld.player():
        ap = owner.ap
        ap._endForceMove(success)
        ap.setSpeed(owner.speed[gametypes.SPEED_MOVE] / 60.0)
        if isUnPin:
            setMoveControl(owner, False)
        if getattr(owner, 'castSkillBusy', None):
            owner.castSkillBusy = False
        owner.updateActionKeyState()
        owner.isAscending = False
    else:
        owner.am.moveNotifier = owner.fashion.movingNotifier
        if owner.IsAvatar and hasattr(owner, 'fashion'):
            owner.fashion.stopAction()
            apEffectEx = getattr(owner, 'apEffectEx', None)
            if apEffectEx:
                apEffectEx.movingNotifier(0)


def poujun(skillPlayer, skillInfo, clientSkillInfo, playAction = True, moveInfo = None, moveId = 0):
    owner = BigWorld.entity(skillPlayer.owner)
    oldGravity = 0
    if owner == BigWorld.player():
        oldGravity = owner.physics.gravity
        owner.setGravity(SYSCD.data.get('dashGravity', gametypes.DASH_GRAVITY))
    skillPlayer.startMove(skillInfo, clientSkillInfo)
    skillPlayer.processDamageAll(skillInfo, clientSkillInfo)
    if owner == BigWorld.player():
        owner.setGravity(oldGravity)


def getMyThrustPoint(startPos, endPos, testHeight = (0.5, 1.0, 1.5, 2.0), ingoreMaterKind = 0):
    direction = startPos - endPos
    spaceID = BigWorld.player().spaceID
    if testHeight:
        for i in testHeight:
            testStartPos = startPos + Math.Vector3(0, i, 0)
            testEndPos = endPos + Math.Vector3(0, i, 0)
            dropPos = BigWorld.collide(spaceID, testStartPos, testEndPos, ingoreMaterKind)
            if dropPos != None:
                return

    direction.normalise()
    thrustPos = endPos + direction
    return thrustPos


def _approachZhanSha(skillPlayer, owner, moveData, skillInfo, clientSkillInfo, success, playAction, yaw, gravity, reached):
    gamelog.debug('flyeffect:_approachZhanSha ', skillInfo, success, playAction, reached)
    skillPlayer.processDamageAll(skillInfo, clientSkillInfo)
    _approachTowardTarget(owner, False, success)
    _finishZhanSha(skillPlayer, owner, moveData, skillInfo, clientSkillInfo, yaw, playAction, gravity)


def _finishZhanSha(skillPlayer, owner, moveData, skillInfo, clientSkillInfo, yaw, playAction = True, gravity = 10.0):
    setMoveControl(owner, False)
    if owner == BigWorld.player():
        owner.setGravity(gravity)
        owner.updateActionKeyState()
        needFaceYaw = moveData.get('needFaceYaw', False)
        followCameraTime = moveData.get('followCameraTime', 0.0)
        if needFaceYaw and owner.targetLocked:
            direction = owner.targetLocked.position - owner.position
            needFaceTime = moveData.get('needFaceTime', 0.2)
            BigWorld.callback(needFaceTime, Functor(owner.faceToDirWidthCamera, direction.yaw))
        if followCameraTime > 0.0:
            delayReset = moveData.get('delayResetCamera', 0.1)
            BigWorld.callback(delayReset, resetCameraTime)
    if playAction:
        skillPlayer.moveCast(skillInfo, clientSkillInfo, None)


def resetCameraTime():
    BigWorld.camera().followMovementHalfLife = 0.0


def setMoveControl(owner, inMove):
    if owner == BigWorld.player():
        gamelog.debug('----lihang@flyEffect.setMoveControl inMove', inMove)
        owner.inForceMove = inMove
        if inMove:
            owner.ap.intoForceMove()
        else:
            owner.ap.leaveForceMove()


def hitFly(skillPlayer, skillInfo, clientSkillInfo, playAction = True, moveTime = 0, damageData = 0, hold = False):
    target = BigWorld.entity(damageData.eid)
    if not target:
        return
    if not target.inWorld:
        return
    if not getattr(target, 'fashion'):
        return
    if not (target.IsMonster or target.IsSummoned):
        skillPlayer.processDamageById(skillInfo, clientSkillInfo, damageData)
        return
    if hold and not target.fashion.inStateAction():
        target.updateModelFreeze(moveTime, gameglobal.FREEZE_TYPE_MOVE)
    hitFlyActs = clientSkillInfo.getSkillData('hitFlyAct', None)
    gamelog.debug('jorsef2:hitFly', hitFlyActs, clientSkillInfo.skillData, moveTime, damageData)
    if hitFlyActs:
        if moveTime:
            scale = 0.5 / moveTime
        else:
            scale = 1.0
        if target.fashion.doingActionType() not in [ACT.FUKONG_LOOP_ACTION,
         ACT.TIAOGAO_LOOP_ACTION,
         ACT.JIDAO_LOOP_ACTION,
         ACT.FAINT_LOOP_ACTION,
         ACT.FUKONG_STOP_ACTION,
         ACT.TIAOGAO_STOP_ACTION,
         ACT.JIDAO_STOP_ACTION,
         ACT.FAINT_STOP_ACTION,
         ACT.FUKONG_START_ACTION,
         ACT.TIAOGAO_START_ACTION,
         ACT.JIDAO_START_ACTION,
         ACT.FAINT_START_ACTION]:
            target.fashion.setDoingActionType(ACT.HITFLY_ACTION)
            target.fashion.playActionSequence(target.model, hitFlyActs, None, scale, 60)
        skillPlayer.processDamageById(skillInfo, clientSkillInfo, damageData)
        BigWorld.callback(moveTime, Functor(_finishHitFly, skillPlayer, skillInfo, clientSkillInfo, hitFlyActs, damageData))
        return
    skillPlayer.processDamageById(skillInfo, clientSkillInfo, damageData)


def _finishHitFly(skillPlayer, skillInfo, clientSkillInfo, hitFlyActs, damageData):
    target = BigWorld.entity(damageData.eid)
    if not target:
        return
    gamelog.debug('jorsef2: _finishHitFly', hasattr(target, 'downCliff') and target.downCliff)
    if not (hasattr(target, 'downCliff') and target.downCliff):
        for hitFlyAct in hitFlyActs:
            if hitFlyAct in target.fashion.getActionNameList():
                target.fashion.stopActionByName(target.model, hitFlyAct)

    if target.life == gametypes.LIFE_DEAD:
        gamelog.debug('jorsef2: target die!!')
        if not (hasattr(target, 'downCliff') and target.downCliff):
            target.playDieAction()
        return
    stopAct = clientSkillInfo.getSkillData('hitFlyStopAct', None)
    gamelog.debug('bgf:hitFly1', stopAct)
    if stopAct:
        stopAct = stopAct[1]
        if stopAct in target.fashion.getActionNameList():
            target.fashion.setDoingActionType(ACT.HITFLY_STOP_ACTION)
            target.fashion.playActionSequence(target.model, (stopAct,), None)
        else:
            BigWorld.player().chatToEventEx('怪物没有击飞结束动作', const.CHANNEL_COLOR_RED)


def monsterSkill(skillPlayer, skillInfo, clientSkillInfo, playAction = True, moveTime = 0, damageData = 0, moveId = 0):
    owner = BigWorld.entity(skillPlayer.owner)
    if owner.fashion.doingActionType() in [ACT.HIT_DIEFLY_ACTION]:
        return
    if owner.IsMonster or getattr(owner, 'IsAvatarRobot', False) or getattr(owner, 'IsPuppet', False):
        flag = skillPlayer.monsterMove(moveTime, skillInfo, clientSkillInfo)
    else:
        flag = False
    if not flag:
        hitFly(skillPlayer, skillInfo, clientSkillInfo, playAction, moveTime, damageData)


def getRelativePosition(selfPos, selfYaw, theta, dist):
    x = selfPos[0] + dist * math.sin(selfYaw + theta * math.pi / 180)
    z = selfPos[2] + dist * math.cos(selfYaw + theta * math.pi / 180)
    return (x, selfPos[1], z)


def getMoveDir(md):
    angleType = md.get('angleType', None)
    moveDir = None
    if angleType == gametypes.MOVEMENT_SKILL_SRC_WASD:
        if HK.HKM[HK.KEY_MOVELEFT].isAnyDown():
            if HK.HKM[HK.KEY_FORWARD].isAnyDown():
                moveDir = gameglobal.MOVE_DIR_FORWARD
            elif HK.HKM[HK.KEY_BACKWARD].isAnyDown():
                moveDir = gameglobal.MOVE_DIR_BACK
            else:
                moveDir = gameglobal.MOVE_DIR_LEFT
        elif HK.HKM[HK.KEY_MOVERIGHT].isAnyDown():
            if HK.HKM[HK.KEY_FORWARD].isAnyDown():
                moveDir = gameglobal.MOVE_DIR_FORWARD
            elif HK.HKM[HK.KEY_BACKWARD].isAnyDown():
                moveDir = gameglobal.MOVE_DIR_BACK
            else:
                moveDir = gameglobal.MOVE_DIR_RIGHT
        elif HK.HKM[HK.KEY_BACKWARD].isAnyDown():
            moveDir = gameglobal.MOVE_DIR_BACK
    return moveDir


def _initiativeToPostion(skillPlayer, skillInfo, clientSkillInfo, speed, dstPos, moveData, playAction = True):
    owner = BigWorld.entity(skillPlayer.owner)
    if not owner or not owner.inWorld:
        return
    success = False
    setMoveControl(owner, True)
    if owner == BigWorld.player():
        followCameraTime = moveData.get('followCameraTime', 0.0)
        if followCameraTime > 0.0:
            BigWorld.camera().followMovementHalfLife = followCameraTime
        moveDir = getMoveDir(moveData)
        skillPlayer.startMove(skillInfo, clientSkillInfo, moveDir)
        if dstPos:
            ap = owner.ap
            ap.setSpeed(speed)
            owner.physics.maxVelocity = 0
            success = True
            if moveData.get('avatarDanDaoFly'):
                hold = moveData.get('hold', False)
                avatarDanDaoFly(dstPos, 0, speed, moveData, Functor(_approachTowardTarget, owner, hold, 1))
            else:
                oldGravity = owner.physics.gravity
                owner.setGravity(SYSCD.data.get('dashGravity', gametypes.DASH_GRAVITY))
                cPos = []
                _checkCollide((owner.position.x, owner.position.y, owner.position.z), (dstPos.x, dstPos.y, dstPos.z), getPos=cPos)
                if cPos:
                    dstPos = Math.Vector3(cPos)
                newPoint = _findDropPoint(dstPos) if not owner.inFly and not owner.inSwim else None
                if newPoint and moveData.get('angle', 0) != gametypes.MOVEMENT_SKILL_ANGLE_UP:
                    dstPos = newPoint
                ap.beginForceMoveWithCallback(dstPos, Functor(_approachZhanSha, skillPlayer, owner, moveData, skillInfo, clientSkillInfo, success, playAction, owner.yaw, oldGravity), True, False)
                if gameglobal.ENABLE_SKILL_SCREEN_EFFECT and owner.getEffectLv() >= gameglobal.EFFECT_MID:
                    BigWorld.motionBlurFilter(None, 0, motionBlurTime, motionBlurScale)
        else:
            gamelog.warning('_initiativeToPostion:靠近目标受阻挡')
    skillPlayer.processDamageAll(skillInfo, clientSkillInfo)
    if not skillPlayer.target or not skillPlayer.target.inWorld:
        return
    dist = (skillPlayer.target.position - owner.position).length
    if not success:
        delayTime = 0.1
        BigWorld.callback(delayTime, Functor(skillPlayer.startMove, skillInfo, clientSkillInfo))
        BigWorld.callback(dist / speed + 2 * delayTime, Functor(_finishZhanSha, skillPlayer, owner, moveData, skillInfo, clientSkillInfo, owner.yaw, playAction))


def _passiveToPostion(skillPlayer, skillInfo, clientSkillInfo, moveData, speed, dstPos, realDist, moveParam, playAction = True):
    skillID = skillInfo.num
    player = BigWorld.player()
    owner = BigWorld.entity(skillPlayer.owner)
    gamelog.debug('_passiveToPostion', owner.id, player.id, dstPos)
    if not skillPlayer.damageResult.has_key(skillID) or not skillPlayer.damageResult[skillID]:
        return
    for res in skillPlayer.damageResult[skillID][0]:
        if not getattr(res, 'moveId', 0):
            continue
        if res.eid == player.id:
            if hasattr(player, 'immuneControl') and player.immuneControl() and not moveData.get('ignoreImmune', 0):
                continue
            forcePosition = dstPos
            if moveParam:
                if moveParam[1] or not moveData.get('useTargetPos', False):
                    forcePosition = moveParam[1]
                distanceFix = moveParam[2]
            dstPos = utils.__getDstPos(moveData, owner, player, player, forcePosition, distanceFix)
            gamelog.debug('get _passiveToPostion', owner.position, player.position, dstPos, forcePosition, moveData)
            hold = moveData.get('hold', False)
            if hold:
                if hasattr(player, 'fashion'):
                    if player.fashion.doingActionType() in (ACT.GUIDE_ACTION,):
                        player.skillPlayer.stopGuideEffect()
                    player.fashion.stopAction()
                    player.fashion.breakJump()
                    player.fashion.breakFall()
                setMoveControl(player, True)
                if not player.fashion.inStateAction():
                    player.updateModelFreeze(99999.0, gameglobal.FREEZE_TYPE_MOVE)
                player.model.beholded = True
            ap = player.ap
            ap.setSpeed(speed)
            player.physics.maxVelocity = 0
            gamelog.debug('jorsef: begin force move', player.id)
            if moveData.get('avatarDanDaoFly'):
                avatarDanDaoFly(dstPos, realDist, speed, moveData, Functor(_approachTowardTarget, player, hold, 1))
            else:
                needCollide = True
                if moveData:
                    needCollide = moveData.get('needCollide', True)
                if not needCollide:
                    if _checkCollide(player.position, dstPos, gameglobal.IGNORE_COLLIDE):
                        _approachTowardTarget(player, hold, 1)
                        return
                ap.beginForceMoveWithCallback(dstPos, Functor(_approachTowardTarget, player, hold), needCollide)
        else:
            en = BigWorld.entities.get(res.eid)
            if not en or not en.inWorld or not en.model:
                continue
            if hasattr(en, 'immuneControl') and en.immuneControl() and not moveData.get('ignoreImmune', 0):
                continue
            hold = moveData.get('hold', False)
            if hold:
                if hasattr(en, 'fashion') and en.fashion.doingActionType() in (ACT.GUIDE_ACTION,):
                    en.skillPlayer.stopSpell()
                if not en.fashion.inStateAction():
                    en.updateModelFreeze(99999.0, gameglobal.FREEZE_TYPE_MOVE)
                en.model.beholded = True
            en.filter.clientYawMinDist = 0.0
            if hasattr(en.filter, 'keepYawTime'):
                en.filter.keepYawTime = 999999
            changeYawByHost = moveData.get('changeYawByHost', None)
            yaw = (player.position - en.position).yaw
            if changeYawByHost == gameglobal.STATE_CAHGNE_YAW_TYPE_SAME:
                yaw = (en.position - player.position).yaw
            else:
                yaw = (player.position - en.position).yaw
            en.filter.setYaw(yaw)
            en.am.moveNotifier = None
            apEffectEx = getattr(en, 'apEffectEx', None)
            if apEffectEx:
                apEffectEx.movingNotifier(1)
            BigWorld.callback(float(realDist / speed) + 0.5, Functor(_approachTowardTarget, en, False, 1))

    if skillID != const.ISOLATED_CREATEION_MOVE_SKILL_ID:
        skillPlayer.processDamageAll(skillInfo, clientSkillInfo)


def _commonToPostion(skillPlayer, skillInfo, clientSkillInfo, moveData, dstPos, realDist, initiative, moveParam):
    gamelog.debug('@_commonToPostion', skillPlayer.owner, moveData, dstPos, realDist, initiative)
    speed = moveData.get('speed', 0)
    time = moveData.get('moveTime', 0)
    gamelog.debug('@_commonToPostion1', speed, time, initiative)
    if not speed and time:
        speed = realDist / time
    elif not speed and not time:
        return
    if speed == 0:
        return
    if initiative:
        _initiativeToPostion(skillPlayer, skillInfo, clientSkillInfo, speed, dstPos, moveData)
    else:
        _passiveToPostion(skillPlayer, skillInfo, clientSkillInfo, moveData, speed, dstPos, realDist, moveParam)


def _teleportforwardCheck(owner, targetPos):
    d = 1
    delta = 0.5
    count = 0
    pos = owner.position
    dist = distance3D(targetPos, owner.position)
    yaw = (targetPos - owner.position).yaw
    gamelog.debug('_teleportforwardCheck', targetPos, pos, dist, yaw)
    while count < dist / d:
        tPoint = pos + d * Math.Vector3(math.sin(yaw), 0, math.cos(yaw))
        tPoint = _findDropPoint(tPoint) if not owner.inFly else tPoint
        if tPoint:
            h = tPoint[1] - pos[1]
            if h >= d or h <= -5:
                break
            tempPoint = Math.Vector3(tPoint[0], tPoint[1], tPoint[2])
            if h >= 0:
                pass
            else:
                tempPoint = Math.Vector3(tPoint[0], pos[1], tPoint[2])
            tempPoint1 = tempPoint + delta * Math.Vector3(math.sin(yaw), 0, math.cos(yaw))
            tempPoint2 = tempPoint - delta * Math.Vector3(math.sin(yaw), 0, math.cos(yaw))
            yaw1 = yaw + math.pi * 0.5
            tempPoint3 = tempPoint + delta * Math.Vector3(math.sin(yaw1), 0, math.cos(yaw1))
            tempPoint4 = tempPoint - delta * Math.Vector3(math.sin(yaw1), 0, math.cos(yaw1))
            if _checkCollide(pos, tempPoint) or _checkCollide(pos, tempPoint1) or _checkCollide(pos, tempPoint2) or _checkCollide(tempPoint, tempPoint3) or _checkCollide(tempPoint, tempPoint4):
                break
            pos = tPoint
            count += 1
        else:
            break

    return pos


def _teleportbackwardCheck(owner, targetPos):
    d = 1
    delta = 0.5
    count = 0
    pos = owner.position
    dist = distance3D(targetPos, owner.position)
    yaw = (targetPos - owner.position).yaw
    distPos = pos + dist * Math.Vector3(math.sin(yaw), 0, math.cos(yaw))
    gamelog.debug('_teleportbackwardCheck', targetPos, pos, distPos, dist, yaw)
    while count <= dist / d:
        tPoint = _findDropPoint(distPos)
        gamelog.debug('_teleportbackwardCheck0', pos, tPoint)
        if tPoint and not _checkCollide(pos, tPoint):
            tPoint1 = tPoint + delta * Math.Vector3(math.sin(yaw), 0, math.cos(yaw))
            tPoint2 = tPoint - delta * Math.Vector3(math.sin(yaw), 0, math.cos(yaw))
            yaw1 = yaw + math.pi * 0.5
            tPoint3 = tPoint + delta * Math.Vector3(math.sin(yaw1), 0, math.cos(yaw1))
            tPoint4 = tPoint - delta * Math.Vector3(math.sin(yaw1), 0, math.cos(yaw1))
            if not _checkCollide(pos, tPoint1) and not _checkCollide(pos, tPoint2) and not _checkCollide(tPoint, tPoint3) and not _checkCollide(tPoint, tPoint4):
                h = tPoint[1] - pos[1]
                if h <= 2 and h >= -math.sqrt((tPoint[2] - pos[2]) * (tPoint[2] - pos[2]) + (tPoint[0] - pos[0]) * (tPoint[0] - pos[0])):
                    return tPoint
        distPos = distPos - d * Math.Vector3(math.sin(owner.yaw), 0, math.cos(owner.yaw))
        count += 1

    return pos


def _getTeleportPos(owner, targetPos, initiative):
    pos = None
    if initiative:
        pos1 = _teleportforwardCheck(owner, targetPos)
        pos2 = _teleportbackwardCheck(owner, targetPos)
        nearPoint = (pos1 - owner.position).length > (pos2 - owner.position).length
        pos = pos1 if nearPoint else pos2
    else:
        pos = targetPos
    if owner.inFly:
        pos = Math.Vector3(pos[0], owner.position[1], pos[2])
    return pos


def _commonTeleport(skillPlayer, targetPos, initiative):
    gamelog.debug('_commonTeleport', skillPlayer.owner, targetPos)
    owner = BigWorld.entity(skillPlayer.owner)
    if owner != BigWorld.player():
        return
    pos = _getTeleportPos(owner, targetPos, initiative)
    if pos != owner.position and distance2D(pos, owner.position) > 1:
        owner.cell.setTeleportPos(pos)
        owner.startTeleportMove()


def commonSkillMove(skillPlayer, skillInfo, clientSkillInfo, playAction, moveParam, moveId = 0):
    gamelog.debug('commonSkillMove', skillPlayer.owner, moveId)
    player = BigWorld.player()
    if player.life == gametypes.LIFE_DEAD:
        return
    skillSrc = BigWorld.entities.get(skillPlayer.owner)
    skillTgt = skillPlayer.target
    if not SMD.data.has_key(moveId):
        return
    md = SMD.data[moveId]
    moveUnit = md.get('moveUnit')
    tp = md.get('type')
    forcePosition = skillPlayer.targetPos
    gamelog.debug('11111forcePosition', forcePosition, moveParam, md)
    if moveParam:
        if moveParam[1] or not md.get('useTargetPos', False):
            forcePosition = moveParam[1]
        distanceFix = moveParam[2]
    src = skillSrc if moveUnit == gametypes.MOVEMENT_SKILL_MOVE_SELF else skillTgt
    dstPos = utils.__getDstPos(md, skillSrc, skillTgt, src, forcePosition, distanceFix)
    gamelog.debug('get dstPos', dstPos, moveUnit)
    if not dstPos or not src:
        return
    realDist = distance3D(dstPos, src.position)
    moveSelf = moveUnit == gametypes.MOVEMENT_SKILL_MOVE_SELF
    if tp == gametypes.MOVEMENT_SKILL_TYPE_MOVE:
        if player.inTeleportMove():
            player.setTeleportMoveCallback(Functor(commonSkillMove, skillPlayer, skillInfo, clientSkillInfo, playAction, moveParam, moveId))
        else:
            _commonToPostion(skillPlayer, skillInfo, clientSkillInfo, md, dstPos, realDist, moveSelf, moveParam)
    elif tp == gametypes.MOVEMENT_SKILL_TYPE_TELEPORT:
        _commonTeleport(skillPlayer, dstPos, moveSelf)


def playFlyEffect(skillPlayer):
    wf = WeaponFlyer()
    wf.start(skillPlayer)


class WeaponFlyer(object):

    def __init__(self):
        self.weaponModelList = []
        self.owner = None

    def start(self, skillPlayer):
        BigWorld.callback(1.0, Functor(self.realDoFly, skillPlayer, 'right'))
        self.owner = BigWorld.entity(skillPlayer.owner)
        BigWorld.callback(6.0, self.foreRelease)

    def foreRelease(self):
        if not getattr(self.owner, 'inWorld', False):
            return
        if len(self.weaponModelList) > 0:
            for wp in self.weaponModelList:
                self.owner.delModel(wp)

        self.owner.isFlyLeftWeapon = False
        self.owner.isFlyRightWeapon = False
        self.owner.refreshWeaponVisible()

    def realDoFly(self, skillPlayer, hand):
        owner = BigWorld.entity(skillPlayer.owner)
        target = skillPlayer.target
        modelServerWeaponModel = getattr(getattr(owner, 'modelServer', None), hand + 'WeaponModel', None)
        if owner is None or target is None or modelServerWeaponModel is None or getattr(owner, 'model', None) is None:
            return
        if hand == 'left':
            owner.isFlyLeftWeapon = True
        elif hand == 'right':
            owner.isFlyRightWeapon = True
        modelServerWeaponModel.hide(True)
        weaponModel = self.getWeaponModel(owner, modelServerWeaponModel)
        if weaponModel is None:
            return
        owner.addModel(weaponModel)
        self.weaponModelList.append(weaponModel)
        if owner.model.node('HP_hand_%s_item1' % hand) is None or getattr(target, 'getHitNodeRandom', None) is None or target.getHitNodeRandom() is None:
            return
        self.doFly(weaponModel, Math.Matrix(owner.model.node('HP_hand_%s_item1' % hand)), target.getHitNodeRandom(), Functor(self.flyBack, owner, target, weaponModel, hand))

    def releaseWeapon(self, owner, weaponModel, hand):
        self.owner.delModel(weaponModel)
        self.weaponModelList.remove(weaponModel)
        if hand == 'left':
            self.owner.isFlyLeftWeapon = False
        elif hand == 'right':
            self.owner.isFlyRightWeapon = False
        self.owner.refreshWeaponVisible()

    def flyBack(self, owner, target, weaponModel, hand):
        releaseFunc = Functor(self.releaseWeapon, owner, weaponModel, hand)
        if getattr(owner, 'model', None) is None or owner.model.node('HP_hand_%s_item1' % hand) is None or getattr(target, 'getHitNodeRandom', None) is None or target.getHitNodeRandom() is None:
            return
        self.doFly(weaponModel, Math.Matrix(target.getHitNodeRandom()), owner.model.node('HP_hand_%s_item1' % hand), releaseFunc)

    def doFly(self, weaponModel, ownerMatrix, targetNode, callback = None):
        weaponModel.position = ownerMatrix.position
        flyer = sfx.FlyToNodeEx(weaponModel, callback)
        flyer.start(ownerMatrix.position, targetNode, speed=20, rotateSpeed=20)

    def getWeaponModel(self, owner, modelServerWeaponModel):
        try:
            return clientUtils.model(*modelServerWeaponModel.models[0][0].sources)
        except:
            return None


flyPeriodFuncMap = {1000: commonSkillMove,
 1001: kickFly,
 1002: poujun,
 99999: monsterSkill}
