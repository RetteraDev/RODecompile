#Embedded file name: I:/bag/tmp/tw2/res/entities\client\sfx/fenShenEffect.o
import BigWorld
import Math
from callbackHelper import Functor
from data import skill_fenshen_data

def startFenShen(ownerId, fenshenId, fenshenPosition, targetPosition, targetYaw):
    owner = BigWorld.entity(ownerId)
    if not owner or not owner.inWorld:
        return
    fenShenData = skill_fenshen_data.data.get(fenshenId, None)
    if not fenShenData:
        return
    p = BigWorld.player()
    srcPos = Math.Vector3(fenshenPosition[0], fenshenPosition[1], fenshenPosition[2])
    targetPos = Math.Vector3(targetPosition[0], targetPosition[1], targetPosition[2])
    if not targetYaw:
        yaw = (targetPos - srcPos).yaw
    else:
        yaw = targetYaw
    bornTime = fenShenData.get('bornTime', 0.0)
    position = srcPos
    if fenShenData.get('bornFormPlayer', False):
        position = owner.position
    BigWorld.callback(bornTime, Functor(BigWorld.createEntity, 'AvatarMonster', p.spaceID, 0, position, (0, 0, yaw), {'avatarId': owner.id,
     'fenshenId': fenshenId,
     'destPosition': srcPos,
     'isOnlyClient': True}))
