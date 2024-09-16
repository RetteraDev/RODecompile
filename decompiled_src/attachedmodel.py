#Embedded file name: /WORKSPACE/data/entities/client/helpers/attachedmodel.o
import BigWorld
import gameglobal
import gametypes
import keys
import const
import gamelog
import clientcom
import seqTask
import utils
from callbackHelper import Functor
from sfx import sfx
from helpers import tintalt
from helpers import charRes
from helpers import action
from helpers import tuZhuangDyeMorpher
from helpers import attachedModelCueFashion
from data import equip_data as ED
from data import horsewing_data as HWCD
from data import zaiju_data as ZD
from data import special_life_skill_equip_data as SLSED
from data import weapon_client_data as WCD
from data import life_skill_equip_data as LSED
from data import couple_emote_data as CED
from data import wear_show_data as WSD
from data import sys_config_data as SCD
from cdata import tuzhuang_equip_data as TED
from data import buff_item_attach_data as BIAD
DATA_ERROR = -1
DETACHED = 0
ATTACHED_RIGHT = 2
ATTACHED_LEFT = 4
ATTACHED_ROOT = 8
ATTACHED = ATTACHED_RIGHT | ATTACHED_LEFT | ATTACHED_ROOT
HANG_UP = 16
ZAIJU_REPLACE = 0
ZAIJU_ATTACH = 1
ZAIJU_NONE = 2
ZAIJU_BEATTACHED = 3
ZAIJU_ATTACH_NO_ACTION = 0
ZAIJU_ATTACH_ACTION = 1
WEAR_ATTACH_NO_ACTION = 0
WEAR_ATTACH_ACTION = 1
WEAR_ATTACH_ACTION_AS_ENTITY = 2
WEAR_ATTACH_ACTION_JUST_SKILL = 3
WEAR_ATTACH_ACTION_TYPE = [WEAR_ATTACH_ACTION, WEAR_ATTACH_ACTION_AS_ENTITY]

class AttachedModel(object):
    __metaclass__ = attachedModelCueFashion.AttachedModelCueFashionMeta

    def __init__(self, entityID, threadID):
        super(AttachedModel, self).__init__()
        self.state = DATA_ERROR
        self.entityID = entityID
        self.threadID = threadID
        self.ownerModel = None
        self.equipID = 0
        self.models = []
        self.loadID = 0
        self.loader = None
        self.model = None
        self.callback = None
        self.defaultAction = None
        self.topLogoKey = 0
        self.key = 0
        self.dyeTint = None
        self.attachEff = []
        self.detachEff = []
        self.mountEffects = []
        self.attachedEffects = []
        self.freezedEffs = []
        self.attachModel = {}
        self.attachEffs = []

    def freezeEffect(self, freezeTime):
        for fx in self.mountEffects:
            if fx:
                fx.pause(freezeTime)
                self.freezedEffs.append(fx)

        for fx in self.attachedEffects:
            if fx:
                fx.pause(freezeTime)
                self.freezedEffs.append(fx)

    def clearFreezeEffect(self):
        if self.freezedEffs:
            for eff in self.freezedEffs:
                if eff:
                    eff.pause(0)

        self.freezedEffs = []

    def clearAttachedEffects(self):
        if self.attachedEffects:
            self.attachedEffects = []

    def addAttachedEffects(self, effs):
        if effs:
            self.attachedEffects.extend(effs)

    def clearMountEffects(self):
        if self.mountEffects:
            self.mountEffects = []

    def addMountEffects(self, effs):
        if effs:
            self.mountEffects.extend(effs)

    def getAttachments(self, key, data = None):
        return None

    def isAttached(self):
        return self.state == ATTACHED

    def isHangUped(self):
        return self.state == HANG_UP

    def isDetached(self):
        return self.state == DETACHED

    def refreshMountEffect(self, attach = True):
        ent = BigWorld.entity(self.entityID)
        if not ent or not ent.fashion.opacity:
            return None
        effects = []
        self.clearMountEffects()
        if attach:
            for effId in self.attachEff:
                effects = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (ent.getEquipEffectLv(),
                 ent.getEquipEffectPriority(),
                 ent.model,
                 effId,
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))
                self.addMountEffects(effects)

        else:
            for effId in self.detachEff:
                effects = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (ent.getEquipEffectLv(),
                 ent.getEquipEffectPriority(),
                 ent.model,
                 effId,
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))
                self.addMountEffects(effects)

    def release(self):
        gamelog.debug('release.......', self.entityID, self.equipID, self.state)
        self.loadID += 1
        if self.state not in (DETACHED, DATA_ERROR):
            self.detach()
        self.state = DATA_ERROR
        self.resetAttachModel()
        self.ownerModel = None
        self.equipID = 0
        self.attachModel = {}
        self.callback = None
        self.cancelTask()

    def resetAttachModel(self):
        models = []
        for m in self.models:
            models.append(m[0])

        tintalt.ta_reset(models)
        if self.model:
            tintalt.ta_reset([self.model])
        entity = BigWorld.entity(self.entityID)
        if entity and entity.inWorld:
            for model in models:
                if model in getattr(entity, 'allModels', []):
                    entity.allModels.remove(model)

        self.model = None
        self.models = []

    def detach(self):
        gamelog.debug('detach ', self.entityID, self.equipID, self.ownerModel)
        if not self.ownerModel or self.state == DATA_ERROR:
            return False
        try:
            for m in self.models:
                self.ownerModel.setHP(m[1], None)
                if m[2] != 1:
                    node = self.ownerModel.node(m[1])
                    if node:
                        node.scale(1.0)

        except:
            pass

        self.state = DETACHED
        return True

    def attachEffect(self, model, effect):
        entity = BigWorld.entity(self.entityID)
        for ef in effect:
            effs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getBasicEffectLv(),
             entity.getBasicEffectPriority(),
             model,
             ef,
             sfx.EFFECT_LIMIT_MISC,
             -1,
             0,
             True))
            self.addAttachedEffects(effs)

    def attach(self, model):
        gamelog.debug('attach model.....', self, self.entityID, self.equipID, self.ownerModel, self.state, model, self.models)
        if self.state == DATA_ERROR or not model:
            gamelog.error('attach failed , DATA_ERROR  ', model)
            return False
        if self.ownerModel and model != self.ownerModel:
            gamelog.error('attach,model changed ', self.entityID, self.equipID)
            self.detach()
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.fashion or not model:
            gamelog.error('hangUp failed ')
            return False
        success = self.state != ATTACHED
        self.ownerModel = model
        if self.state != ATTACHED:
            self.clearAttachedEffects()
            for m in self.models:
                try:
                    self.ownerModel.setHP(m[1], m[0])
                    if m[2] != 1:
                        self.ownerModel.node(m[1]).scale(m[2])
                    if m[3]:
                        self.attachEffect(m[0], m[3])
                    if m[4]:
                        try:
                            if self.defaultAction:
                                m[0].action(self.defaultAction)()
                        except:
                            gamelog.error('Error can not play attachments action ')

                except:
                    gamelog.error('error attach equip model failed!!!!!!!!!!!!!!!!!')

            self.state = ATTACHED
        return success

    def equipItem(self, attachments, callback = None):
        entity = BigWorld.entity(self.entityID)
        if not entity:
            gamelog.error('Error .......... AttachedModel no entity', self.entityID)
            return
        if not getattr(entity, 'isRealModel', True):
            return
        if attachments == self.equipID and self.model:
            gamelog.debug('AttachedModel equipItem, no changed ', attachments)
            if callback:
                callback(self.model)
            elif self.callback:
                self.callback(self.model)
            return
        self.release()
        self.callback = callback
        self.loadID += 1
        self.equipID = attachments
        if len(attachments) == 0:
            gamelog.error('No thing to attach ', attachments)
            return
        self.maxCount = len(attachments)
        for a in attachments:
            fullModelPath = a[0]
            gamelog.debug('AttachedModel part: ', a, fullModelPath)
            if gameglobal.rds.isSinglePlayer:
                if not clientcom.isFileExist(fullModelPath):
                    gamelog.error('打不开资源%s' % fullModelPath)
                    continue
            res = None
            if tuZhuangDyeMorpher.checkDyes(a[1]):
                dyeMorpher = tuZhuangDyeMorpher.TuZhuangDyeMorpher(a[0])
                dyeMorpher.read(a[1], self.dyeTint)
                res = [fullModelPath, dyeMorpher.getDynamicTint()]
            else:
                if utils.instanceof(self, 'WearAttachModel'):
                    dye = a[8] if a[8] else a[1]
                else:
                    dye = a[6] if a[6] else a[1]
                res = [fullModelPath, ('*', dye)]
            self.loader = seqTask.BkgModelLoader(entity, self.threadID, res, Functor(self._modelLoadFinish, a), self.loadID)

        self.state = DETACHED

    def getEnhanceEffect(self, itemId, subIdIndex, enhLv):
        data = ED.data.get(itemId, {})
        effect = list(data.get('effect', []))
        enhanceEffect = data.get('enhanceEffect', [])
        addedEffect = None
        for item in enhanceEffect:
            if enhLv >= item[0] and len(item) > subIdIndex + 1:
                addedEffect = item[subIdIndex + 1:]

        if addedEffect:
            for eff in addedEffect:
                if eff not in effect:
                    effect.append(eff)

        return effect

    def getEnhanceTint(self, itemId, subIdIndex, enhLv):
        data = ED.data.get(itemId, {})
        enhanceTint = data.get('enhanceTint', [])
        tint = None
        for item in enhanceTint:
            if enhLv >= item[0] and len(item) > subIdIndex + 1:
                tint = item[subIdIndex + 1]

        return tint

    def _modelLoadFinish(self, data, loadID, model):
        gamelog.debug('AttachedModel _modelLoadFinish.......', self, loadID, model, self.state, self.ownerModel, data)
        if not model:
            gamelog.error('Error AttachedModel _modelLoadFinish, model is None', loadID, self.equipID)
            return
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        if loadID == self.loadID:
            self.maxCount -= 1
            dye = data[1]
            hp = data[2]
            scale = data[3]
            length = len(data)
            effects = data[4] if length > 4 else ()
            hasAni = data[5] if length > 5 else False
            tint = data[6] if length > 6 else None
            self.models.append([model,
             hp,
             scale,
             effects,
             hasAni,
             tint if tint else dye])
            self.model = model
            self.model.entityId = self.entityID
            entity.allModels.append(model)
            gamelog.debug('bgf:ownerModel', self.ownerModel, self.state)
            if self.ownerModel and self.state == ATTACHED:
                try:
                    self.ownerModel.setHP(hp, model)
                    if scale != 1:
                        self.ownerModel.node(hp).scale(scale)
                    if effects:
                        self.clearAttachedEffects()
                        self.attachEffect(model, effects)
                except:
                    gamelog.error('error attach equip model failed!!!!!!!!!!!!!!!!!')
                    self.state = DETACHED

                if hasAni:
                    try:
                        if self.defaultAction:
                            model.action(self.defaultAction)()
                    except:
                        gamelog.error('Error can not play attachments action ')

                if not tuZhuangDyeMorpher.checkDyes(dye):
                    dye = tint if tint else dye
                    if dye:
                        tintalt.ta_set_static_states(model, dye, needBuildName=False)
            else:
                self.state = DETACHED
            gamelog.debug('_modelLoadFinish', self.callback)
            if self.callback:
                self.callback(model)

    def cancelTask(self):
        if self.loader:
            self.loader.cancel()
            self.loader = None


class WingFlyAttachModel(AttachedModel):

    def __init__(self, entityID, threadID):
        super(WingFlyAttachModel, self).__init__(entityID, threadID)
        self.effect = []
        self.dyeList = None
        self.isHideBackWearInFly = False

    def release(self):
        super(WingFlyAttachModel, self).release()
        self.effect = []
        self.isHideBackWearInFly = False

    def freezeEffect(self, freezeTime):
        super(WingFlyAttachModel, self).freezeEffect(freezeTime)
        for fx in self.effect:
            if fx:
                fx.pause(freezeTime)
                self.freezedEffs.append(fx)

    def attachEffect(self, model, effect):
        entity = BigWorld.entity(self.entityID)
        for ef in effect:
            fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getBasicEffectLv(),
             entity.getBasicEffectPriority(),
             model,
             ef,
             sfx.EFFECT_LIMIT_MISC,
             -1,
             0,
             True))
            if fxs:
                self.effect.extend(fxs)

    def clearEffect(self):
        for eff in self.effect:
            eff.stop()

        self.effect = []

    def updateEffect(self, key, enhLv, dyeList):
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.fashion:
            return
        if not self.models:
            self.equipItem(key, enhLv)
            return
        data = ED.data.get(key, {})
        effectId = self.getEnhanceEffect(key, 0, enhLv)
        tint = self.getEnhanceTint(key, 0, enhLv)
        dye = clientcom.getMatrialsName(entity, data) if not tint else tint
        self.clearAttachedEffects()
        for i, m in enumerate(self.models):
            model, hp, scale, oldEffectId, hasAni, oldTint = m
            self.models[i] = (model,
             hp,
             scale,
             effectId,
             hasAni,
             tint)
            if self.isAttached():
                self.clearEffect()
                if effectId:
                    self.attachEffect(model, effectId)
            if dyeList:
                if tuZhuangDyeMorpher.checkDyes(dyeList):
                    dyeMorpher = tuZhuangDyeMorpher.TuZhuangDyeMorpher(model)
                    dyeMorpher.read(dyeList, self.dyeTint)
                    dyeMorpher.syncApply()
                else:
                    tintalt.ta_set_static([model], dyeList)
            elif dye:
                tintalt.ta_set_static([model], dye)

    def equipItem(self, key, enhLv = 0, dyeList = []):
        self.key = key
        data = ED.data.get(key, {})
        if data:
            attachments = self.getAttachments(key, data, enhLv)
            subId = data.get('subId', [0])[0]
            wingFlyData = HWCD.data.get(subId, None)
            self.topLogoKey = subId
            self.dyeTint = TED.data.get(key, {}).get('dyeTint', None)
            self.dyeList = dyeList
            self.isHideBackWearInFly = data.get('isHideBackWearInFly', False)
            for itemData in wingFlyData:
                self.defaultAction = itemData.get('defaultAction', None)
                self.attachEff = []
                attachEff = itemData.get('attachEff', [])
                self.attachEff.extend(list(attachEff))
                self.detachEff = []
                detachEff = itemData.get('detachEff', [])
                self.detachEff.extend(list(detachEff))

            super(WingFlyAttachModel, self).equipItem(attachments, self.afterWingFlyModelFinished)
        else:
            self.release()

    def getAttachments(self, key, data = None, enhLv = 0, dyeList = []):
        if data == None:
            data = ED.data.get(key, {})
        attachments = []
        if data:
            entity = BigWorld.entity(self.entityID)
            modelId = data.get('modelId', None)
            subId = data.get('subId', [0])[0]
            wingFlyData = HWCD.data.get(subId, None)
            gamelog.debug('wingFlyData:3', self.topLogoKey)
            for itemData in wingFlyData:
                modelPath = 'char/%s/%s.model' % (modelId, modelId)
                dye = clientcom.getMatrialsName(entity, data)
                if dyeList:
                    dye = dyeList
                hp = itemData.get('attachHp', 'HP_back')
                scaleKey = clientcom.getAvatarWeaponModelScale(entity)
                scale = itemData.get(scaleKey, 1.0)
                effects = self.getEnhanceEffect(key, 0, enhLv)
                hasAni = True
                tint = self.getEnhanceTint(key, 0, enhLv)
                attachments.append((modelPath,
                 dye,
                 hp,
                 scale,
                 effects,
                 hasAni,
                 tint))

        return attachments

    def attach(self, attachModel):
        entity = BigWorld.entity(self.entityID)
        super(WingFlyAttachModel, self).attach(attachModel)
        try:
            am = self.model.motors[0]
        except:
            am = BigWorld.ActionMatcher(entity)
            am.matchCaps = [keys.CAPS_FLY]
            am.footTwistSpeed = 0.0
            if self.model:
                self.model.motors = (am,)

        if attachModel and hasattr(self.ownerModel, 'motors') and len(self.ownerModel.motors):
            utils.addMotorsChild(self.ownerModel.motors, am)
        if entity.fashion and self.model:
            self.model.soundCallback(self.actionCueCallback)
        self.resetWingDriveActionMap()
        if hasattr(entity, 'resetAmActionSpeed'):
            entity.resetAmActionSpeed()

    def detach(self):
        entity = BigWorld.entity(self.entityID)
        super(WingFlyAttachModel, self).detach()
        self.clearEffect()
        if self.ownerModel:
            am = self.getOwnerActionMatcher()
            if am:
                am.footTwistSpeed = entity.modelServer.oldFootTwistSpeed
        self.resetWingDriveActionMap()

    def getOwnerActionMatcher(self):
        if self.ownerModel and self.ownerModel.motors:
            for m in self.ownerModel.motors:
                if m and m.__class__.__name__ == 'ActionMatcher':
                    return m

    def getActionMatcher(self):
        if self.model and len(self.model.motors) >= 1:
            for m in self.model.motors:
                if m and m.__class__.__name__ == 'ActionMatcher':
                    return m

    def afterWingFlyModelFinished(self, model):
        entity = BigWorld.entity(self.entityID)
        data = ED.data.get(self.key, {})
        dye = clientcom.getMatrialsName(entity, data)
        if model:
            tintalt.ta_set_static_states(model, dye, needBuildName=False)
        if self.dyeList:
            if tuZhuangDyeMorpher.checkDyes(self.dyeList):
                dyeMorpher = tuZhuangDyeMorpher.TuZhuangDyeMorpher(model)
                dyeMorpher.read(self.dyeList, self.dyeTint)
                dyeMorpher.syncApply()
            else:
                tintalt.ta_set_static([model], self.dyeList)
        entity.fashion.wingFlyActionList = model.actionNameList()
        entity.modelServer._wingFlyModelFinished(self.key, model)
        if entity.fashion and model:
            model.soundCallback(entity.fashion.actionCueCallback)
        entity.modelServer.refreshWingFlyState(False)
        if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            self.attach(entity.model)
            self.model.action(gameglobal.rds.loginScene.wingActionId)()

    def resetWingDriveActionMap(self):
        try:
            entity = BigWorld.entity(self.entityID)
            if hasattr(entity, 'isInCoupleRideAsHorse') and entity.isInCoupleRideAsHorse():
                coupleEmoteData = CED.data.get(entity.getCoupleKey(), {})
                driveActionMap = coupleEmoteData.get('driveActionMap', ())
                if self.model and len(self.model.motors) >= 1:
                    self.model.motors[0].driveActionMap = driveActionMap
            elif self.model and len(self.model.motors) >= 1:
                carryActionList = SCD.data.get('flyCarryActions', [])
                self.model.motors[0].driveActionMap = carryActionList
        except:
            gamelog.debug('-----m.l resetWingDriveActionMap error')


class BeastAttachModel(AttachedModel):

    def __init__(self, entityID, threadID):
        super(BeastAttachModel, self).__init__(entityID, threadID)
        self.scale = 1.0
        self.zaijuMode = ZAIJU_ATTACH
        self.topLogoKey = 0
        self.isRealHorse = 0
        self.chairIdleAction = None
        self.flyRideIdleAction = None
        self.zaijuAction = ZAIJU_ATTACH_NO_ACTION
        self.effectInAir = []
        self.faceIdleAction = None

    def freezeEffect(self, freezeTime):
        super(BeastAttachModel, self).freezeEffect(freezeTime)
        for fx in self.effectInAir:
            if fx:
                fx.pause(freezeTime)
                self.freezedEffs.append(fx)

    def isZaijuReplace(self):
        return self.zaijuMode == ZAIJU_REPLACE

    def releaseEffectInAir(self):
        for ef in self.effectInAir:
            if ef:
                ef.stop()

        self.effectInAir = []

    def getFlyRideMatrialsName(self, equipData):
        entity = BigWorld.entity(self.entityID)
        if entity.inFlyTypeFlyRide():
            return clientcom.getFlyRideMatrialsName(equipData)
        else:
            return clientcom.getMatrialsName(entity, equipData)

    def refreshFlyRideMatrials(self):
        equipData = ED.data.get(self.key, {})
        flyRideMaterial = clientcom.getFlyRideMatrialsName(equipData)
        if flyRideMaterial:
            dye = self.getFlyRideMatrialsName(equipData)
            if dye:
                tintalt.ta_set_static([self.model], dye)

    def refreshEffectInAir(self):
        self.releaseEffectInAir()
        entity = BigWorld.entity(self.entityID)
        equipData = ED.data.get(self.key, {})
        effects = equipData.get('effectInAir', ())
        if effects:
            for ef in effects:
                ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getBasicEffectLv(),
                 entity.getBasicEffectPriority(),
                 self.model,
                 ef,
                 sfx.EFFECT_LIMIT_MISC,
                 -1,
                 0,
                 True))
                if ef:
                    self.effectInAir.extend(ef)

    def equipItem(self, key, showEffect = True, enhLv = 0, dyeList = []):
        data = ED.data.get(key, {})
        self.zaijuMode = ZAIJU_ATTACH
        self._equipItem(key, data, showEffect, enhLv, dyeList)

    def getAttachments(self, key, data = None, enhLv = 0, dyeList = []):
        attachments = []
        if not data:
            data = ED.data.get(key, {})
        if data:
            modelId = data.get('modelId', None)
            subId = data.get('subId', [0])
            if isinstance(subId, tuple) or isinstance(subId, list):
                subId = subId[0]
            horseData = HWCD.data.get(subId, None)
            entity = BigWorld.entity(self.entityID)
            if horseData is None:
                modelPath = 'char/%d/%d.model' % (modelId, modelId)
                dye = clientcom.getMatrialsName(entity, data)
                scale = data.get('modelScale', 1.0)
                effects = self.getEnhanceEffect(key, 0, enhLv)
                self.attachEff = []
                self.detachEff = []
                attachments.append((modelPath,
                 dye,
                 None,
                 scale,
                 effects,
                 False,
                 None))
                return attachments
            for index, itemData in enumerate(horseData):
                modelId = self.getHorseModelId(key, modelId, index)
                if not modelId:
                    continue
                modelPath = 'char/%d/%d.model' % (modelId, modelId)
                dye = clientcom.getMatrialsName(entity, data)
                if dyeList:
                    dye = dyeList
                hp = itemData.get('attachHp', 'HP_ride')
                scaleKey = clientcom.getAvatarWeaponModelScale(entity)
                scale = itemData.get(scaleKey, 1.0)
                effects = self.getEnhanceEffect(key, 0, enhLv)
                hasAni = itemData.get('hasAni', 0)
                self.defaultAction = itemData.get('defaultAction', None)
                tint = self.getEnhanceTint(key, 0, enhLv)
                attachments.append((modelPath,
                 dye,
                 hp,
                 scale,
                 effects,
                 hasAni,
                 tint))

        return attachments

    def getHorseModelId(self, zaijuId, modelId, index):
        models = ZD.data.get(zaijuId, {}).get('models', [])
        if not models:
            return modelId
        if index < len(models):
            return models[index]
        return modelId

    def _equipItem(self, key, data, showEffect = True, enhLv = 0, dyeList = []):
        if not data:
            self.release()
        self.key = key
        entity = BigWorld.entity(self.entityID)
        modelId = data.get('modelId', 0)
        if modelId > const.MODEL_AVATAR_BORDER:
            self.scale = data.get('modelScale', 1.0)
            clientcom.fetchModel(self.threadID, Functor(self.afterBeastModelFinished, showEffect), modelId)
            return
        attachments = []
        subId = data.get('subId', [0])
        if isinstance(subId, tuple) or isinstance(subId, list):
            subId = subId[0]
        self.topLogoKey = subId
        self.faceIdleAction = data.get('faceIdleAction', None)
        self.dyeTint = TED.data.get(key, {}).get('dyeTint', None)
        horseData = HWCD.data.get(subId, None)
        attachments = self.getAttachments(key, data, enhLv, dyeList)
        if horseData is None:
            self.scale = data.get('modelScale', 1.0)
            self.attachEff = []
            self.detachEff = []
            super(BeastAttachModel, self).equipItem(attachments, Functor(self.afterBeastModelFinished, showEffect))
            return
        for itemData in horseData:
            scaleKey = clientcom.getAvatarWeaponModelScale(entity)
            self.scale = itemData.get(scaleKey, 1.0)
            self.defaultAction = itemData.get('defaultAction', None)
            self.attachEff = []
            attachEff = itemData.get('attachEff', [])
            self.attachEff.extend(list(attachEff))
            self.detachEff = []
            detachEff = itemData.get('detachEff', [])
            self.detachEff.extend(list(detachEff))
            self.isRealHorse = itemData.get('realHorse', 0)
            self.chairIdleAction = itemData.get('chairIdleAction', None)
            self.flyRideIdleAction = itemData.get('flyRideIdleAction', None)
            self.zaijuAction = itemData.get('zaijuAction', ZAIJU_ATTACH_NO_ACTION)

        super(BeastAttachModel, self).equipItem(attachments, Functor(self.afterBeastModelFinished, showEffect))

    def release(self):
        super(BeastAttachModel, self).release()
        entity = BigWorld.entity(self.entityID)
        try:
            if entity.inWorld:
                entity.modelServer.rideModel.setHP('HP_ride', None)
                entity.modelServer.rideModel = None
        except:
            pass

    def equipZaiju(self, key, data, showEffect = True, enhLv = 0, dyeList = []):
        self.key = key
        bsType = data.get('BsType', 1)
        if bsType in (ZAIJU_REPLACE, ZAIJU_ATTACH, ZAIJU_BEATTACHED):
            self.zaijuMode = bsType
            self._equipItem(key, data, showEffect, enhLv, dyeList)
            return True
        return False

    def needAttached(self):
        return self.zaijuMode == ZAIJU_ATTACH

    def afterBeastModelFinished(self, showEffect, model):
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        dye = self.models[0][5] if len(self.models) > 0 and len(self.models[0]) > 5 else 'DefaultMatter'
        if model and dye != 'DefaultMatter':
            tintalt.ta_set_static_states(model, dye, needBuildName=False)
        if self.zaijuMode == ZAIJU_BEATTACHED:
            entity.modelServer.realAttachZaiju(self.key, showEffect)
        else:
            entity.modelServer._rideModelFinish(self.key, showEffect, model)
        if hasattr(entity, 'refreshItemClientEffect') and hasattr(entity, 'itemClientEffectCache'):
            entity.refreshItemClientEffect([], entity.itemClientEffectCache.keys())
        self.releaseAttaches()
        self.handleAttaches(entity, model)

    def releaseAttachEffs(self):
        if self.attachEffs:
            for eff in self.attachEffs:
                if eff:
                    eff.stop()

            self.attachEffs = []

    def releaseAttaches(self):
        if self.attachModel:
            for i in self.attachModel:
                self.attachModel[i] = None

            self.attachModel = {}
        self.releaseAttachEffs()

    def refreshAttachEffs(self):
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        attaches = ZD.data.get(self.key, {}).get('attaches', None)
        if not attaches:
            return
        self.releaseAttachEffs()
        for attach in attaches:
            modelPrefix = ''
            if len(attach) == 6:
                attachHp, attachModel, attachEff, attachScale, attachEffScale, modelPrefix = attach
            else:
                attachHp, attachModel, attachEff, attachScale, attachEffScale = attach
            if attachEffScale <= 0:
                attachEffScale = 1
            if attachEff:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                 entity.getEquipEffectPriority(),
                 entity.model,
                 attachEff,
                 sfx.EFFECT_LIMIT_MISC))
                if fx:
                    for fxItem in fx:
                        fxItem.scale(attachEffScale, attachEffScale, attachEffScale)

                    self.attachEffs.extend(fx)

    def handleAttaches(self, entity, bodyModel):
        attaches = ZD.data.get(self.key, {}).get('attaches', None)
        if not attaches or not bodyModel:
            return
        for attach in attaches:
            modelPrefix = ''
            if len(attach) == 6:
                attachHp, attachModel, attachEff, attachScale, attachEffScale, modelPrefix = attach
            else:
                attachHp, attachModel, attachEff, attachScale, attachEffScale = attach
            if not modelPrefix:
                modelPrefix = 'item/model'
            if attachEffScale <= 0:
                attachEffScale = 1
            if attachScale <= 0:
                attachScale = 1
            if attachEff:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                 entity.getEquipEffectPriority(),
                 bodyModel,
                 attachEff,
                 sfx.EFFECT_LIMIT_MISC))
                if fx:
                    for fxItem in fx:
                        fxItem.scale(attachEffScale, attachEffScale, attachEffScale)

                    self.attachEffs.extend(fx)
            if attachModel and attachHp:
                if self.attachModel.has_key(attachHp):
                    model = self.attachModel[attachHp][0]
                    bodyModel.setHP(attachHp, None)
                    bodyModel.setHP(attachHp, model)
                    bodyModel.node(attachHp).scale(attachScale, attachScale, attachScale)
                    self.attachModel[attachHp] = (model, attachScale)
                else:
                    modelPath = '%s/%s' % (modelPrefix, attachModel)
                    callback = Functor(self._afterAttachModelFinished, bodyModel, attachHp, attachScale, modelPath, modelPrefix)
                    charRes.getSimpleModel(modelPath, None, callback)

    def _afterAttachModelFinished(self, bodyModel, attachHp, attachScale, modelPath, modelPrefix, model):
        if not model or not bodyModel:
            return
        try:
            bodyModel.setHP(attachHp, None)
            bodyModel.setHP(attachHp, model)
            bodyModel.node(attachHp).scale(attachScale, attachScale, attachScale)
            self.attachModel[attachHp] = (model, attachScale)
        except Exception as e:
            if BigWorld.isPublishedVersion():
                return
            entInfo = 'attachModel %d:' % self.key
            if not model.node(attachHp):
                raise Exception('%s model %s hpPoint %s' % (entInfo, modelPath, attachHp))
            elif not self.model.node(attachHp):
                raise Exception('%s model %s hpPoint %s' % (entInfo, bodyModel.sources[0], attachHp))

    def getAttachedModel(self):
        models = []
        for attachHp, info in self.attachModel.iteritems():
            if info:
                models.append(info[0])

        return models

    def attach(self, model):
        owner = BigWorld.entity(self.entityID)
        zd = ZD.data.get(self.key, {})
        if owner and owner.inWorld and zd.has_key('onAction'):
            actionIds = zd['onAction']
            callback = owner.updateActionKeyState if owner.fashion.isPlayer else None
            owner.fashion.playAction(actionIds, action.ZAIJU_ON_ACTION, callback)
        super(BeastAttachModel, self).attach(model)
        if owner and owner.inWorld:
            if self.zaijuMode == ZAIJU_BEATTACHED:
                caps = zd.get('caps', keys.CAPS_ZAIJU)
                owner.fashion.setStateCaps([keys.CAPS_HAND_FREE, caps])
                for m in self.models:
                    if m and m[0]:
                        attModel = m[0]
                        try:
                            am = attModel.motors[0]
                            gamelog.debug('zfride:set transparence.........', am)
                        except:
                            am = BigWorld.ActionMatcher(owner)
                            am.matchCaps = [caps]
                            attModel.motors = (am,)

                        am.matcherCoupled = False
                        utils.addMotorsChild(model.motors, am)

            else:
                owner.fashion.setStateCaps([keys.CAPS_RIDE])

    def detach(self):
        owner = BigWorld.entity(self.entityID)
        if not owner or not owner.inWorld or not owner.fashion:
            return
        if self.zaijuMode == ZAIJU_BEATTACHED:
            super(BeastAttachModel, self).detach()
        self.model = None
        self.releaseAttaches()
        caps = ZD.data.get(self.key, {}).get('caps', None)
        if caps and owner.am:
            owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND]
        owner.fashion.setStateCaps([keys.CAPS_GROUND])


class FishingAttachModel(AttachedModel):

    def __init__(self, entityID, threadID):
        super(FishingAttachModel, self).__init__(entityID, threadID)
        self.syncID = 0

    def equipItem(self, syncID, key):
        self.syncID = syncID
        entity = BigWorld.entity(self.entityID)
        data = SLSED.data.get(key, {})
        if data:
            modelId = data.get('modelId', None)
            subId = data.get('subId', [0])[0]
            if subId:
                weaponData = WCD.data.get(subId, {})
                for itemData in weaponData:
                    wcdSubId = itemData.get('subId', 0)
                    weaponName = '_'.join((str(modelId), '00', wcdSubId))
                    modelPath = 'item/model/' + str(modelId) + '/' + weaponName + '.model'
                    attachHP = itemData.get('attachHp', None)
                    scaleKey = clientcom.getAvatarWeaponModelScale(entity)
                    scale = itemData.get(scaleKey, 1.0)

        else:
            modelPath = 'item/model/79998/79998_00_r1.model'
            attachHP = 'HP_hand_right_item1'
            scale = 1.0
        dye = 'Default'
        effects = []
        hasAni = 0
        attachments = [(modelPath,
          dye,
          attachHP,
          scale,
          effects,
          hasAni,
          None)]
        super(FishingAttachModel, self).equipItem(attachments, Functor(self.afterFishingModelFinished, syncID))

    def afterFishingModelFinished(self, syncID, model):
        if syncID != self.syncID:
            return
        entity = BigWorld.entity(self.entityID)
        if entity.fashion and model:
            model.soundCallback(entity.fashion.actionCueCallback)
        entity.fishingMgr.realStart(syncID)


class BuffItemAttachModel(AttachedModel):
    FIXED_PATH_PREFIX = 'char/10000/model/'

    def __init__(self, entityID, threadID):
        super(BuffItemAttachModel, self).__init__(entityID, threadID)
        self.equipType = None
        self.actionWear = False

    def isActionWear(self):
        return self.actionWear

    def getAttachments(self, key, data = None, enhLv = 0):
        attachments = []
        entity = BigWorld.entity(self.entityID)
        if data:
            attachType = data.get('type', 0)
            self.defaultAction = data.get('defaultAction', '')
            equipType = data.get('equipType', None)
            self.actionWear = data.get('isActionWear', False)
            if equipType:
                self.equipType = equipType
            if attachType == 1:
                modelPath = data.get('modelPath', '')
                subId = data.get('subId', [0])[0]
                weaponData = WCD.data.get(subId, {})
                modelId = data.get('modelId', None)
                part = data.get('part', '')
                if modelId:
                    dye = 'Default'
                    for itemData in weaponData:
                        wcdSubId = itemData.get('subId', 0)
                        if not modelPath:
                            weaponName = '_'.join((str(modelId), '00', wcdSubId))
                            modelPath = self.FIXED_PATH_PREFIX + part + '/' + str(modelId) + '/' + weaponName + '.model'
                        attachHP = itemData.get('attachHp', None)
                        attachEff = itemData.get('attachEff', [])
                        scaleKey = clientcom.getAvatarWeaponModelScale(entity)
                        scale = itemData.get(scaleKey, 1.0)
                        attachments.append((modelPath,
                         dye,
                         attachHP,
                         scale,
                         attachEff,
                         1,
                         None))

            else:
                modelPath = data.get('modelPath', '')
                if modelPath:
                    dye = 'Default'
                    attachHP = data.get('attachHp', None)
                    scale = data.get('scale', 1.0)
                    attachments.append((modelPath,
                     dye,
                     attachHP,
                     scale,
                     [],
                     1,
                     None))
        return attachments

    def equipItem(self, key, enhLv = 0):
        data = BIAD.data.get(key, {})
        attachments = self.getAttachments(key, data)
        super(BuffItemAttachModel, self).equipItem(attachments, None)

    def detach(self):
        super(BuffItemAttachModel, self).detach()
        self.equipType = None
        self.actionWear = False


class LifeSkillAttachModel(AttachedModel):

    def __init__(self, entityID, threadID):
        super(LifeSkillAttachModel, self).__init__(entityID, threadID)

    def getAttachments(self, key, data = None, enhLv = 0):
        if data == None:
            data = LSED.data.get(key, {})
        attachments = []
        if data:
            modelId = data.get('modelId', None)
            subId = data.get('subId', [0])[0]
            entity = BigWorld.entity(self.entityID)
            if subId:
                weaponData = WCD.data.get(subId, {})
                for itemData in weaponData:
                    wcdSubId = itemData.get('subId', 0)
                    weaponName = '_'.join((str(modelId), '00', wcdSubId))
                    modelPath = 'item/model/' + str(modelId) + '/' + weaponName + '.model'
                    dye = clientcom.getMatrialsName(entity, data)
                    attachHP = itemData.get('attachHp', None)
                    scaleKey = clientcom.getAvatarWeaponModelScale(entity)
                    scale = itemData.get(scaleKey, 1.0)
                    attachments.append((modelPath,
                     dye,
                     attachHP,
                     scale,
                     [],
                     0,
                     None))

        return attachments

    def equipItem(self, key, enhLv = 0):
        data = LSED.data.get(key, {})
        attachments = self.getAttachments(key, data)
        super(LifeSkillAttachModel, self).equipItem(attachments, None)

    def attach(self, model, attachType = ATTACHED):
        gamelog.debug('attach model.....', self, self.entityID, self.equipID, self.ownerModel, self.state, model, self.models)
        if self.state == DATA_ERROR or not model:
            gamelog.error('attach failed , DATA_ERROR  ', model)
            return False
        if self.ownerModel and model != self.ownerModel:
            gamelog.error('attach,model changed ', self.entityID, self.equipID)
            self.detach()
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.fashion or not model:
            gamelog.error('hangUp failed ')
            return False
        success = self.state != ATTACHED
        newState = self.state | attachType
        self.ownerModel = model
        if self.state != ATTACHED:
            self.clearAttachedEffects()
            for m in self.models:
                if m[1].find('right') != -1 and newState & ATTACHED_RIGHT or m[1].find('left') != -1 and newState & ATTACHED_LEFT or (m[1].find('root') != -1 or m[1].find('Root') != -1) and newState & ATTACHED_ROOT or newState == ATTACHED:
                    try:
                        self.ownerModel.setHP(m[1], m[0])
                        if m[2] != 1:
                            self.ownerModel.node(m[1]).scale(m[2])
                        if m[3]:
                            for ef in m[3]:
                                effs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getBasicEffectLv(),
                                 entity.getBasicEffectPriority(),
                                 m[0],
                                 ef,
                                 sfx.EFFECT_LIMIT,
                                 -1,
                                 0,
                                 True))
                                self.addAttachedEffects(effs)

                        if m[4]:
                            try:
                                if self.defaultAction:
                                    m[0].action(self.defaultAction)()
                            except:
                                gamelog.error('Error can not play attachments action ')

                    except:
                        gamelog.error('error attach equip model failed!!!!!!!!!!!!!!!!!')

            self.state = newState
        return success

    def detach(self, attachType = DETACHED):
        gamelog.debug('detach ', self.entityID, self.equipID, self.ownerModel, attachType)
        if not self.ownerModel or self.state == DATA_ERROR:
            return False
        newState = attachType & self.state
        for m in self.models:
            if m[1].find('right') != -1 and ~newState & ATTACHED_RIGHT or m[1].find('left') != -1 and ~newState & ATTACHED_LEFT or (m[1].find('root') != -1 or m[1].find('Root') != -1) and ~newState & ATTACHED_ROOT or newState == DETACHED:
                try:
                    self.ownerModel.setHP(m[1], None)
                    if m[2] != 1:
                        node = self.ownerModel.node(m[1])
                        if node:
                            node.scale(1.0)
                except:
                    pass

        self.state = newState
        return True

    def _modelLoadFinish(self, data, loadID, model):
        gamelog.debug('AttachedModel _modelLoadFinish.......', self, loadID, model, self.state, self.ownerModel, data)
        if not model:
            gamelog.error('Error AttachedModel _modelLoadFinish, model is None', loadID, self.equipID)
            return
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        if loadID == self.loadID:
            self.maxCount -= 1
            dye = data[1]
            hp = data[2]
            scale = data[3]
            length = len(data)
            if length > 5:
                effects = data[4]
                hasAni = data[5]
            elif length > 4:
                effects = data[4]
                hasAni = False
            else:
                effects = ()
                hasAni = False
            if dye:
                tintalt.ta_set_static_states(model, dye, needBuildName=False)
            self.models.append([model,
             hp,
             scale,
             effects,
             hasAni])
            self.model = model
            self.model.entityId = self.entityID
            entity.allModels.append(model)
            gamelog.debug('bgf:ownerModel', self.ownerModel, self.state)
            if self.ownerModel and self.state not in (DETACHED, DATA_ERROR):
                if hp.find('right') != -1 and self.state & ATTACHED_RIGHT or hp.find('left') != -1 and self.state & ATTACHED_LEFT or (hp.find('root') != -1 or hp.find('Root') != -1) and self.state & ATTACHED_ROOT or self.state == ATTACHED:
                    try:
                        self.ownerModel.setHP(hp, model)
                        if scale != 1:
                            self.ownerModel.node(hp).scale(scale)
                        if effects:
                            self.clearAttachedEffects()
                            for ef in effects:
                                effs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getBasicEffectLv(),
                                 entity.getBasicEffectPriority(),
                                 model,
                                 ef,
                                 sfx.EFFECT_LIMIT_MISC,
                                 -1,
                                 0,
                                 True))
                                self.addAttachedEffects(effs)

                    except:
                        gamelog.error('error attach equip model failed!!!!!!!!!!!!!!!!!')
                        self.state = DETACHED

                    if hasAni:
                        try:
                            if self.defaultAction:
                                model.action(self.defaultAction)()
                        except:
                            gamelog.error('Error can not play attachments action ')

            else:
                self.state = DETACHED
            if self.callback:
                self.callback(model)


class WearAttachModel(AttachedModel):
    FIXED_PATH_PREFIX = 'char/10000/model/'

    def __init__(self, entityID, threadID, part = None, fixedHP = None, subTag = None, charPath = False):
        super(WearAttachModel, self).__init__(entityID, threadID)
        self.part = part
        self.fixedHP = fixedHP
        self.subTag = subTag
        self.equipType = 0
        self.isAttachedWear = 0
        self.skills = []
        self.weaponEffect = []
        self.charPath = charPath
        self.isEffectWear = False
        self.hasPhy = False
        self.boredActionMovingType = 0
        self.isHideBackWearInFly = False

    def freezeEffect(self, freezeTime):
        super(WearAttachModel, self).freezeEffect(freezeTime)
        for fx in self.weaponEffect:
            if fx:
                fx.pause(freezeTime)
                self.freezedEffs.append(fx)

    def equipItem(self, key):
        entity = BigWorld.entity(self.entityID)
        data = ED.data.get(key, {})
        attachments = []
        self.key = key
        if data:
            attachments = self.getAttachments(key, data)
            self.isAttachedWear = data.get('attachedWear', 0)
            self.isEffectWear = not data.get('modelId', None)
            self.hasPhy = data.get('hasPhy', 0)
            self.boredActionMovingType = data.get('boredActionMovingType', 0)
            self.isHideBackWearInFly = data.get('isHideBackWearInFly', False)
            showWearId = data.get('showWearId', 0)
            wsd = WSD.data.get(showWearId, {})
            if wsd:
                key = clientcom.getAvatarKey(entity)
                self.skills = wsd.get(key + 'Skills', [])
                self.equipType = wsd.get(key + 'ActType', 0)
            else:
                self.skills = []
                self.equipType = 0
        if not self.isEffectWear:
            super(WearAttachModel, self).equipItem(attachments, None)
        else:
            self.release()
            self.state = DETACHED
            self.models = attachments

    def getPhotoAction(self, key = None, data = None):
        return gameglobal.IDLEACT1

    def getAttachments(self, key, data = None, physique = None):
        entity = BigWorld.entity(self.entityID)
        if not data:
            data = ED.data.get(key, {})
        attachments = []
        if data:
            modelId = data.get('modelId', None)
            if self.charPath:
                if not physique:
                    physique = entity.physique
                bodyType = charRes.transBodyType(physique.sex, physique.bodyType)
                modelPath = charRes.getPartPath(bodyType, self.part, modelId, False, self.part) if modelId else None
                dye = clientcom.getMatrialsName(entity, data) if modelId else None
                attachHP = self.fixedHP
                hangHP = self.fixedHP
                attachScale = hangScale = 1.0
                effect = data.get('effect', [])
                subId = data.get('subId', [0])[0]
                attachEff = []
                attachTint = None
                if subId:
                    weaponData = WCD.data.get(subId, {})
                    scaleKey = clientcom.getAvatarWeaponModelScale(entity)
                    if weaponData:
                        itemData = weaponData[0]
                        hangScale = attachScale = itemData.get(scaleKey, 1.0)
                        attachEff = itemData.get('attachEff', [])
                        attachTint = itemData.get('attachTint', None)
                        attachHP = itemData.get('attachHp', None)
                        hangHP = itemData.get('hangHp', None)
                        attachBodyEff = itemData.get('attachBodyEff', [])
                tint = dye
                attachments.append((modelPath,
                 dye,
                 attachHP,
                 hangHP,
                 attachScale,
                 hangScale,
                 effect,
                 0,
                 tint,
                 attachEff,
                 attachTint,
                 attachBodyEff))
            else:
                subId = data.get('subId', [0])[0]
                if subId:
                    weaponData = WCD.data.get(subId, {})
                    for itemData in weaponData:
                        wcdSubId = itemData.get('subId', 0)
                        if self.subTag:
                            wcdSubId = self.subTag
                        weaponName = '_'.join(('%05d' % modelId, '00', wcdSubId))
                        modelPath = self.FIXED_PATH_PREFIX + self.part + '/%05d/' % modelId + weaponName + '.model' if modelId else None
                        dye = clientcom.getMatrialsName(entity, data) if modelId else None
                        attachHP = itemData.get('attachHp', None)
                        hangHP = itemData.get('hangHp', None)
                        scaleKey = clientcom.getAvatarWeaponModelScale(entity)
                        hangScale = attachScale = itemData.get(scaleKey, 1.0)
                        effect = data.get('effect', ())
                        attachEff = itemData.get('attachEff', ())
                        attachTint = itemData.get('attachTint', None)
                        attachBodyEff = itemData.get('attachBodyEff', [])
                        if self.fixedHP:
                            hangHP = self.fixedHP
                        tint = dye
                        attachments.append((modelPath,
                         dye,
                         attachHP,
                         hangHP,
                         attachScale,
                         hangScale,
                         effect,
                         0,
                         tint,
                         attachEff,
                         attachTint,
                         attachBodyEff))

        return attachments

    def attach(self, model):
        gamelog.debug('attach model.....', self, self.entityID, self.equipID, self.ownerModel, self.state, model, self.models)
        if self.state == DATA_ERROR or not model:
            gamelog.error('attach failed , DATA_ERROR  ', model)
            return False
        if self.ownerModel and model != self.ownerModel:
            gamelog.error('attach,model changed ', self.entityID, self.equipID)
            self.detach()
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.fashion or not model:
            gamelog.error('attach failed ')
            return False
        if self.state != ATTACHED:
            for m in self.models:
                if m[1]:
                    self.ownerModel.setHP(m[1], None)
                    m[1] = None

        success = self.state != ATTACHED
        self.ownerModel = model
        if self.state != ATTACHED:
            self.clearAttachedEffects()
            for m in self.models:
                try:
                    self.ownerModel.setHP(m[2], m[0])
                    m[1] = m[2]
                    if m[4] != 1.0:
                        self.ownerModel.node(m[1]).scale(m[4])
                except:
                    gamelog.error('error attach equip model failed!!!!!!!!!!!!!!!!!')

            self.state = ATTACHED
            for m in self.models:
                self.addActionMatcher(m[0])

            self.updateWeaponEffect()
            entity.afterWearUpdate(self)
            if entity.isShowClanWar():
                entity.modelServer.showOtherwears(False)
            else:
                entity.modelServer.showOtherwears(True)
        return success

    def isMutexPart(self, hp):
        if hp.find('back') != -1 or hp.find('waist_left') != -1 or hp.find('waist_right') != -1:
            return True
        return False

    def updateBackWaist(self, show = True):
        if self.isHangUped():
            for a in self.models:
                if self.isMutexPart(a[3]):
                    if show:
                        try:
                            gamelog.debug('hangup:_realHang4-2:', a[3], a[0])
                            self.ownerModel.setHP(a[3], a[0])
                            a[1] = a[3]
                            if a[5] != 1.0:
                                self.ownerModel.node(a[3]).scale(a[5])
                        except:
                            gamelog.error('zf:error attach weapon model failed ', self.models)

                    elif a[1]:
                        self.ownerModel.setHP(a[1], None)
                        a[1] = None
                        node = self.ownerModel.node(a[1])
                        if node:
                            node.scale(1)

            if show:
                self.updateWeaponEffect()

    def _modelLoadFinish(self, data, loadID, model):
        gamelog.debug('AttachedModel _modelLoadFinish.......', self, loadID, model, self.state, self.ownerModel, data)
        if not model:
            gamelog.error('Error AttachedModel _modelLoadFinish, model is None', loadID, self.equipID)
            return
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        if loadID == self.loadID:
            self.maxCount -= 1
            data = list(data)
            data[0] = model
            dye = data[1]
            data[1] = None
            self.models.append(data)
            self.model = model
            self.model.entityId = self.entityID
            entity.allModels.append(model)
            if dye:
                tintalt.ta_set_static_states(model, dye, needBuildName=False)
            gamelog.debug('bgf:ownerModel', self.ownerModel, self.state, data)
            model, _, attachHP, hangHP, attachScale, hangScale, effects, hasAni, _, _, _, _ = data
            if gameglobal.rds.GameState > gametypes.GS_LOGIN:
                shader = BigWorld.BlendFashion(2)
                shader.distance(gameglobal.ATTACHMODEL_FADE_DIST)
                model.distFadeShader = shader
            if self.hasPhy and entity == BigWorld.player() and gameglobal.rds.wearPhysX:
                sources = model.sources[0]
                phyPath = sources.split('.')[0] + '.physx'
                physx = gameglobal.rds.wearPhysX.PhysxNodes(phyPath)
                model.physx = physx
            if self.ownerModel:
                if self.state == ATTACHED:
                    try:
                        self.ownerModel.setHP(attachHP, model)
                        data[1] = attachHP
                        if attachScale != 1:
                            self.ownerModel.node(attachHP).scale(attachScale)
                    except:
                        gamelog.error('error attach equip model failed!!!!!!!!!!!!!!!!!')
                        self.state = DETACHED

                elif self.state == HANG_UP:
                    try:
                        if hasattr(entity, 'showBackWaist') and not entity.showBackWaist and self.isMutexPart(hangHP):
                            data[1] = None
                        else:
                            self.ownerModel.setHP(hangHP, model)
                            data[1] = hangHP
                            if attachScale != 1:
                                self.ownerModel.node(hangHP).scale(hangScale)
                    except:
                        gamelog.error('error attach equip model failed!!!!!!!!!!!!!!!!!')
                        self.state = DETACHED

                else:
                    self.state = DETACHED
                if hasAni:
                    pass
            else:
                self.state = DETACHED
            self.addActionMatcher(model)
            gamelog.debug('_modelLoadFinish', self.callback)
            if self.maxCount == 0:
                self.updateWeaponEffect()
                if entity.isShowClanWar():
                    entity.modelServer.showOtherwears(False)
                else:
                    entity.modelServer.showOtherwears(True)
                    self.refreshOpacityState()
                if self.callback:
                    self.callback(model)
                entity.afterWearUpdate(self)

    def addActionMatcher(self, model):
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        if model and model.inWorld:
            if self.state == HANG_UP:
                try:
                    model.action('1101')()
                except:
                    pass

            model.soundCallback(self.actionCueCallback)

    def isActionWear(self):
        return self.isAttachedWear == WEAR_ATTACH_ACTION

    def isActionAsEntityWear(self):
        return self.isAttachedWear == WEAR_ATTACH_ACTION_AS_ENTITY

    def isActionJustSkillWear(self):
        return self.isAttachedWear == WEAR_ATTACH_ACTION_JUST_SKILL

    def detach(self):
        gamelog.debug('detach ', self.entityID, self.equipID, self.ownerModel)
        if not self.ownerModel or self.state == DATA_ERROR:
            return False
        for m in self.models:
            if m[1]:
                self.ownerModel.setHP(m[1], None)
                node = self.ownerModel.node(m[1])
                if node:
                    node.scale(1)
                m[1] = None

        if self.isEffectWear:
            self.clearWeaponEffect()
        self.state = DETACHED
        entity = BigWorld.entity(self.entityID)
        entity.afterWearUpdate(self)
        return True

    def hangUp(self, model):
        gamelog.debug('hangUp model.....', self, self.entityID, self.equipID, self.ownerModel, self.state, model, self.models)
        if self.state == DATA_ERROR or not model:
            gamelog.error('hangUp failed , DATA_ERROR  ', model)
            return False
        if self.ownerModel and model != self.ownerModel:
            gamelog.error('hangUp,model changed ', self.entityID, self.equipID)
            self.detach()
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.fashion or not model:
            gamelog.error('hangUp failed ')
            return False
        if self.isEffectWear:
            return self.hangUpEffect(model)
        return self.hangUpModel(model)

    def hangUpEffect(self, model):
        entity = BigWorld.entity(self.entityID)
        self.ownerModel = model
        self.state = HANG_UP
        self.updateWeaponEffect()
        entity.afterWearUpdate(self)
        return True

    def hangUpModel(self, model):
        if self.state != HANG_UP:
            for m in self.models:
                if m[1]:
                    self.ownerModel.setHP(m[1], None)
                    m[1] = None

        success = self.state != HANG_UP
        self.ownerModel = model
        if self.state != HANG_UP:
            BigWorld.callback(0.2, self._realHangUp)
        return success

    def _realHangUp(self):
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        for m in self.models:
            try:
                if hasattr(entity, 'showBackWaist') and not entity.showBackWaist and self.isMutexPart(m[3]):
                    m[1] = None
                    m[0].tpos()
                else:
                    self.ownerModel.setHP(m[3], m[0])
                    m[0].tpos()
                    m[1] = m[3]
                    if m[5] != 1.0:
                        self.ownerModel.node(m[1]).scale(m[5])
            except:
                gamelog.error('error hangUp equip model failed!!!!!!!!!!!!!!!!!')

        self.state = HANG_UP
        for m in self.models:
            self.addActionMatcher(m[0])

        self.updateWeaponEffect()
        entity.afterWearUpdate(self)
        if entity.isShowClanWar():
            entity.modelServer.showOtherwears(False)
        else:
            entity.modelServer.showOtherwears(True)
            self.refreshOpacityState()

    def release(self):
        for m in self.models:
            model = m[0]
            if model and len(model.motors) > 0:
                model.motors = []
            if hasattr(model, 'distFadeShader'):
                model.distFadeShader = None

        self.clearWeaponEffect()
        super(WearAttachModel, self).release()

    def clearWeaponEffect(self):
        if self.weaponEffect:
            for fx in self.weaponEffect:
                fx.stop()

            self.weaponEffect = []

    def updateWeaponEffect(self):
        entity = BigWorld.entity(self.entityID)
        if not entity:
            return
        self.clearWeaponEffect()
        for modelInfo in self.models:
            if self.state == ATTACHED:
                effects = list(modelInfo[6]) + list(modelInfo[9])
                attachBodyEff = modelInfo[11]
                BigWorld.callback(1.5, Functor(self.updateBodyEff, attachBodyEff))
            else:
                effects = modelInfo[6]
            if effects:
                for effect in effects:
                    model = modelInfo[0] if not self.isEffectWear else self.ownerModel
                    fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                     entity.getEquipEffectPriority(),
                     model,
                     effect,
                     sfx.EFFECT_LIMIT_MISC))
                    if fx:
                        self.weaponEffect.extend(fx)

    def updateBodyEff(self, attachBodyEff):
        entity = BigWorld.entity(self.entityID)
        if not entity:
            return
        if self.state == ATTACHED and attachBodyEff and self.ownerModel:
            for effect in attachBodyEff:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                 entity.getEquipEffectPriority(),
                 self.ownerModel,
                 effect,
                 sfx.EFFECT_LIMIT_MISC))
                if fx:
                    self.weaponEffect.extend(fx)

    def getOpacityValue(self):
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return False
        if self.part == 'back':
            if getattr(entity, 'inFly', 0) == gametypes.IN_FLY_TYPE_WING:
                if entity.modelServer and entity.modelServer.wingFlyModel.isHideBackWearInFly:
                    return False
                if self.isHideBackWearInFly:
                    return False
        return True

    def refreshOpacityState(self):
        val = self.getOpacityValue()
        for item in self.models:
            model = item[0]
            if model:
                model.visible = val
