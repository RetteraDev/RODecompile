#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/inWaterStateSound.o
import BigWorld
import Math
import Sound
import gamelog
import gameglobal

def playerInWater(state):
    if state:
        gameglobal.rds.sound.playFx('fx/char/waterfx/water_fall_body', BigWorld.player().position, False, BigWorld.player())
    else:
        gameglobal.rds.sound.playFx('fx/char/waterfx/water_raise_body', BigWorld.player().position, False, BigWorld.player())


_waterIdle = None

def cameraInWater(state):
    global _waterIdle
    if state:
        gamelog.debug('InWaterStateSound: camera into water')
        _waterIdle = gameglobal.rds.sound.playFx('fx/char/waterfx/underwater', Math.Vector3(0, 0, 1), True)
    elif _waterIdle != None:
        gamelog.debug('InWaterStateSound: camera out water')
        Sound.stopFx(_waterIdle)
        _waterIdle = None


_callbackIsSet = False

def setInWaterCallback():
    global _callbackIsSet
    if _callbackIsSet:
        return
    Sound.setPlayerInWaterCallback(playerInWater)
    Sound.setCameraInWaterCallback(cameraInWater)
    _callbackIsSet = True
