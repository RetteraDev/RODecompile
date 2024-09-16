#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/outlineHelper.o
import BigWorld
import gametypes
import const
import gameglobal
import utils
import Avatar
from data import sys_config_data as SCD
gAvatar = None

def initOutlineParam():
    try:
        outlineGlowScale = SCD.data.get('outlineGlowScale', 2)
        outlineMinValue = SCD.data.get('outlineMinValue', 0.5)
        fadeTimeScale = SCD.data.get('fadeTimeScale', 1)
        BigWorld.setOutlineGlowScale(outlineGlowScale)
        BigWorld.setOutlineMinValue(outlineMinValue)
        BigWorld.setFadeTimeScale(fadeTimeScale)
    except:
        pass


initOutlineParam()

def getAvatar():
    global gAvatar
    if not gAvatar:
        gAvatar = Avatar
    return gAvatar


def enableOutline(model, color):
    if not model:
        return
    if hasattr(BigWorld, 'setOutlineGlowScale'):
        model.outlineParam = color
    else:
        model.outlineColor = color


def disableOutline(model):
    if not model:
        return
    model.outlineColor = 0


def getOutlineColor(target):
    selColor = 4278574181L
    if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
        selColor = 12891279
    elif gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
        p = BigWorld.player()
        if p.isEnemy(target):
            if getattr(target, 'atkType', const.MONSTER_ATK_TYPE_NO_ATK) == const.MONSTER_ATK_TYPE_ACTIVE_RANGE_ATK or hasattr(target, 'avatarInstance'):
                selColor = 4294521109L
            else:
                targetOwner = target
                if target.IsCreation:
                    if hasattr(target, 'ownerId') and BigWorld.entity(target.ownerId):
                        targetOwner = BigWorld.entity(target.ownerId)
                if hasattr(targetOwner, 'inCombat') and targetOwner.inCombat:
                    selColor = 4294521109L
                elif targetOwner.IsCombatUnit and targetOwner.IsEmptyZaiju:
                    selColor = 4294521109L
                else:
                    selColor = 4293631496L
    return selColor


currEnemyTarget = None

def setTarget(target):
    global currEnemyTarget
    nowLockedTargets = getNowLockedTargets()
    if currEnemyTarget and currEnemyTarget.model:
        if currEnemyTarget not in nowLockedTargets:
            disableOutline(currEnemyTarget.model)
    currEnemyTarget = None
    if target in nowLockedTargets:
        return
    if target and getattr(target, 'model', None):
        selColor = getOutlineColor(target)
        currEnemyTarget = target
        enableOutline(currEnemyTarget.model, selColor)


currLockedTargets = set([])

def getNowLockedTargets():
    nowTargets = set([])
    if not gameglobal.OUTLINIE_FOR_LOCK_TARGET:
        return nowTargets
    p = BigWorld.player()
    if utils.instanceof(p, 'PlayerAvatar'):
        if p.getOperationMode() == gameglobal.ACTION_MODE:
            if p.ap.lockAim:
                nowTargets.add(p.targetLocked)
                nowTargets.add(p.optionalTargetLocked)
                nowTargets.add(p.ap.backupTarget)
        else:
            nowTargets.add(p.targetLocked)
    return nowTargets


def setLockedTarget():
    global currLockedTargets
    if not gameglobal.OUTLINIE_FOR_LOCK_TARGET:
        return
    nowLockedTargets = getNowLockedTargets()
    needDisable = set(currLockedTargets) - set(nowLockedTargets)
    needEnable = set(nowLockedTargets) - set(currLockedTargets)
    for target in needDisable:
        if target and target.model:
            disableOutline(target.model)
        currLockedTargets.remove(target)

    for target in needEnable:
        if target and target.model and hasattr(target, 'canOutline') and target.canOutline():
            selColor = getOutlineColor(target)
            enableOutline(target.model, selColor)
            currLockedTargets.add(target)


def clearLockedTarget():
    global currLockedTargets
    for target in currLockedTargets:
        if target and target.model:
            disableOutline(target.model)

    currLockedTargets = set([])


def checkModelChange(entity):
    p = BigWorld.player()
    en = getattr(p, 'targetLocked', None)
    if entity and entity.model:
        disableOutline(entity.model)
    if en == entity and en != p and entity.canOutline():
        setTarget(entity)
