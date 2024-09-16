#Embedded file name: I:/bag/tmp/tw2/res/entities\client\sfx/birdEffect.o
import math
import BigWorld
import Math
import gameglobal
import sfx
from helpers import charRes
from callbackHelper import Functor
from helpers import tintalt
from data import sys_config_data as SCD

def showBirdEffect(callback = None):
    charRes.getSimpleModel(gameglobal.BIRD_MODEL, 't1', Functor(_afterBirdFinished, callback))


def _afterBirdFinished(callback, model):
    if not model:
        return
    p = BigWorld.player()
    model.visible = False
    dModel = sfx.getDummyModel(True)
    am = BigWorld.ActionMatcher(p)
    am.enableYaw = False
    dModel.motors = (am,)
    dModel.root.attach(model)
    model.bias = (0, p.getModelHeight() + 1, 0)
    delayTime = 1.4
    if gameglobal.BIRD_FLY_ACTION in model.actionNameList():
        BigWorld.callback(0.1, Functor(flyActionAndAttachEffect, model, dModel))
        BigWorld.callback(delayTime, Functor(beginDropItem, model, callback))
        gameglobal.rds.sound.playSound(gameglobal.SD_260)


def flyActionAndAttachEffect(model, dModel):
    model.visible = True
    p = BigWorld.player()
    model.action(gameglobal.BIRD_FLY_ACTION)(0, Functor(birldApproach, model, dModel), 0)
    sfx.attachEffect(gameglobal.ATTACH_EFFECT_ONNODE, (p.getBasicEffectLv(),
     p.getBasicEffectPriority(),
     model,
     'biped',
     SCD.data.get('sfxBirdFly', gameglobal.BIRD_FLY_SFX),
     sfx.EFFECT_UNLIMIT,
     9))


def birldApproach(model, dModel):
    if model.inWorld and model in dModel.root.attachments:
        dModel.root.detach(model)
        tintalt.ta_reset([model])
        model = None
    if dModel.inWorld:
        sfx.giveBackDummyModel(dModel)
        dModel.motors = ()
        dModel = None


def beginDropItem(model, callback):
    charRes.getSimpleModel(gameglobal.ITEM_MODEL, 'Default', Functor(_afterItemFinished, callback, model))


def _afterItemFinished(callback, model, dropModel):
    if not model.inWorld or not dropModel:
        return
    pos0 = model.node('biped').position
    p = BigWorld.player()
    matrix3 = Math.Matrix()
    matrix3.setTranslate((0, p.getModelHeight() * 0.5, 0))
    pos1 = Math.MatrixProduct()
    pos1.a = matrix3
    pos1.b = p.matrix
    dropModel.scale = SCD.data.get('itemScale', (0.3, 0.3, 0.3))
    dropModel.visible = False
    p.addModel(dropModel)
    dropModel.position = pos0
    BigWorld.callback(0, Functor(_beginDropItem, pos0, pos1, callback, dropModel))


def _beginDropItem(pos0, pos1, callback, dropModel):
    dropModel.visible = True
    p = BigWorld.player()
    vel = p.physics.velocity
    vel = math.sqrt(vel[0] * vel[0] + vel[2] * vel[2])
    points = [(pos0,
      pos1,
      Functor(afterDropModel, callback, dropModel),
      vel + 10,
      0,
      0.2)]
    flyer = sfx.DroppedItemMultiPointFlyer(dropModel, points)
    flyer.mot.acceleration = 0.4
    flyer.mot.proximity = 0.1
    flyer.start()


def afterDropModel(callback, dropModel):
    p = BigWorld.player()
    if dropModel.inWorld:
        BigWorld.player().delModel(dropModel)
        dropModel = None
    callback() if callback else None
    tintalt.ta_addGaoLiang([p.model], SCD.data.get('itemColor', (0.2, 3.2, 0.2)), 0.2)
