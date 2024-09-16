#Embedded file name: /WORKSPACE/data/entities/client/helpers/weaponmodel.o
import BigWorld
import gameglobal
import keys
import gamelog
import seqTask
import const
import clientcom
import gametypes
import appSetting
import callbackHelper
from helpers import tintalt
from helpers import attachedModelCueFashion
from sfx import sfx
from data import weapon_client_data as WCD
from data import equip_data as ED
from data import item_data as ID
from data import sys_config_data as SCD
DATA_ERROR = 0
DETACHED = 1
ATTACHED = 2
HANG_UP = 3
WEAPONIDLE = 4
ATTACHED_RIGHT = 5
ATTACHED_MID_WEAPON_ALL = 6
ATTACHED_MID_WEAPON_LEFT = 7
ATTACHED_MID_WEAPON_RIGHT = 8
FOLLOW_IDLE_ACTION = '1101'
FOLLOW_SPECIAL_IDLE_ACTION = '1102'
ZHUSHOU_RIGHT_ATTACH_NODE = 'HP_chain_Attach_R'
ZHUSHOU_LEFT_ATTACH_NODE = 'HP_chain_Attach_L'
DETACH_LEFT = 1
DETACH_RIGHT = 2

class WeaponModel(object):
    __metaclass__ = attachedModelCueFashion.AttachedModelCueFashionMeta

    def __init__(self, entityID, threadID):
        self.state = DATA_ERROR
        self.entityID = entityID
        self.threadID = threadID
        self.equipType = 0
        self.ownerModel = None
        self.models = []
        self.attachHasAni = False
        self.weaponEffect = []
        self.weaponID = 0
        self.loadID = 0
        self.delayID = 0
        self.tintEnhanced = False
        self.orginDye = None
        self.model = None
        self.attachType = ATTACHED
        self.isFollow = False
        self.followModel = None
        self.followModelBias = -0.5
        self.isRightWeapon = False
        self.notSyncRighthWeapon = False
        self.fuShouModelLeft = None
        self.fuShouModelRight = None
        self.effectForbidden = False
        self.freezedEffs = []

    def freezeEffect(self, freezeTime):
        if self.weaponEffect:
            for ef in self.weaponEffect:
                if ef:
                    ef.pause(freezeTime)
                    self.freezedEffs.append(ef)

    def clearFreezeEffect(self):
        if self.freezedEffs:
            for eff in self.freezedEffs:
                if eff:
                    eff.pause(0)

        self.freezedEffs = []

    def setAttachType(self, attachType):
        self.attachType = attachType

    def setEffectForbidden(self, value):
        self.effectForbidden = value

    def setBias(self, value):
        self.followModelBias = value

    def setRightWeapon(self, value):
        self.isRightWeapon = value

    def getRightWeaponSate(self):
        ent = BigWorld.entity(self.entityID)
        if self.notSyncRighthWeapon:
            return DATA_ERROR
        if not self.isRightWeapon:
            ent = BigWorld.entity(self.entityID)
            if ent and ent.inWorld:
                weaponState = getattr(ent, 'weaponState', gametypes.WEAPON_HANDFREE)
                if weaponState in (gametypes.WEAPON_DOUBLEATTACH, gametypes.WEAPON_DOUBLEATTACH_ALL):
                    return ATTACHED
        return self.state

    def updateWeaponAction(self, haveAct = False):
        ent = BigWorld.entity(self.entityID)
        if self.attachHasAni:
            if self.state in (ATTACHED, HANG_UP) and self.followModel:
                if ent.inRiding():
                    BigWorld.callback(0.1, self.calFollowBiasPos)
                else:
                    bias = (self.followModelBias, 1.5, -0.5)
                    if self.ownerModel:
                        bias = (self.followModelBias, self.ownerModel.height, -0.5)
                    if self.followModel.motors:
                        self.followModel.motors[0].biasPos = bias
        else:
            for m in self.models:
                actionSeq = []
                if self.state in (ATTACHED, ATTACHED_RIGHT) or self.state == HANG_UP and self.getRightWeaponSate() == ATTACHED:
                    if haveAct and m[14]:
                        actionSeq.append(m[14])
                    if m[12]:
                        actionSeq.append(m[12])
                else:
                    if haveAct and m[15]:
                        actionSeq.append(m[15])
                    if m[13]:
                        actionSeq.append(m[13])
                if ent and ent.inWorld:
                    ent.fashion.playActionSequence(m[0], actionSeq, None, releaseFx=False)

    def calFollowBiasPos(self):
        ent = BigWorld.entity(self.entityID)
        if ent and ent.inWorld:
            try:
                ridePos = clientcom.getPositionByNode(ent.modelServer.bodyModel.node('HP_ride'))
                diff = ridePos - ent.position
                scale = ent.model.scale
                diff /= scale[0]
                diffZ = diff[1]
                diff[1] = 0
                diffXY = diff.length
                if self.followModel:
                    self.followModel.motors[0].biasPos = (self.followModelBias, 1 + diffZ, -0.5 + diffXY)
            except:
                if self.followModel:
                    self.followModel.motors[0].biasPos = (self.followModelBias, 3, 0)

    def clearWeaponEffect(self):
        gamelog.debug('clearWeaponEffect', self.weaponEffect)
        if self.weaponEffect:
            for fx in self.weaponEffect:
                fx.stop()

            self.weaponEffect = []

    def hide(self, hide):
        for m in self.models:
            if len(m) > 0:
                m[0].visible = not hide

    def fadeToReal(self, fadeTime):
        try:
            for m in self.models:
                if len(m) > 0:
                    model = m[0]
                    if not hasattr(model, 'fadeShader') or not model.fadeShader:
                        fadeShader = BigWorld.BlendFashion()
                        model.fadeShader = fadeShader
                    model.fadeShader.current(0)
                    model.fadeShader.changeTime(fadeTime)
                    model.fadeShader.dest(255)

        except:
            pass

    def realToFade(self, fadeTime):
        try:
            for m in self.models:
                if len(m) > 0:
                    model = m[0]
                    if not hasattr(model, 'fadeShader') or not model.fadeShader:
                        fadeShader = BigWorld.BlendFashion()
                        model.fadeShader = fadeShader
                    model.fadeShader.current(255)
                    model.fadeShader.changeTime(fadeTime)
                    model.fadeShader.dest(0)

        except:
            pass

    def updateWeaponEffect(self):
        if self.effectForbidden:
            return
        entity = BigWorld.entity(self.entityID)
        if not entity:
            return
        if hasattr(entity, 'getOpacityValue') and entity.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        self.clearWeaponEffect()
        for modelInfo in self.models:
            gamelog.debug('modelInfo', modelInfo)
            effects = list(modelInfo[6])
            if self.state in (ATTACHED, ATTACHED_RIGHT):
                effects.extend(modelInfo[10])
            elif self.state == HANG_UP:
                if self.getRightWeaponSate() == ATTACHED:
                    effects.extend(modelInfo[10])
                else:
                    effects.extend(modelInfo[11])
            if effects:
                for effect in effects:
                    fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                     entity.getEquipEffectPriority(),
                     modelInfo[0],
                     effect,
                     sfx.EFFECT_LIMIT_MISC))
                    if fx:
                        self.weaponEffect.extend(fx)

    def resetWeaponModel(self):
        models = []
        for m in self.models:
            models.append(m[0])
            if hasattr(m[0], 'distFadeShader'):
                m[0].distFadeShader = None

        tintalt.ta_reset(models)
        entity = BigWorld.entity(self.entityID)
        if entity and entity.inWorld:
            for model in models:
                if model in getattr(entity, 'allModels', []):
                    entity.allModels.remove(model)

        self.models = []

    def release(self):
        self.loadID += 1
        self.delayID += 1
        if self.state != DATA_ERROR and self.state != DETACHED:
            self.detach()
        if self.followModel:
            if len(self.followModel.motors) > 0:
                self.followModel.motors = []
            self.followModel = None
        self.weaponID = 0
        self.resetWeaponModel()
        self.state = DATA_ERROR
        self.ownerModel = None
        self.equipType = 0
        self.attachHasAni = False
        self.clearWeaponEffect()
        self.cancelLoaders()
        self.isFollow = False
        self.notSyncRighthWeapon = False

    def cancelLoaders(self):
        self.loadID += 1
        self.delayID += 1

    def getEnhanceTint(self, itemId, subIdIndex, enhLv):
        data = ED.data.get(itemId, {})
        enhanceTint = data.get('enhanceTint', [])
        tint = None
        for item in enhanceTint:
            if enhLv >= item[0] and len(item) > subIdIndex + 1:
                tint = item[subIdIndex + 1]

        return tint

    def getEnhanceEffect(self, itemId, subIdIndex, enhLv):
        data = ED.data.get(itemId, {})
        effect = list(data.get('effect', []))
        enhanceEffect = data.get('enhanceEffect', [])
        addedEffect = None
        for item in enhanceEffect:
            if enhLv >= item[0] and len(item) > subIdIndex + 1:
                addedEffect = item[subIdIndex + 1]

        if addedEffect:
            effect.append(addedEffect)
        return effect

    def equipItem(self, itemId, subIdIndex = 0, enhLv = 0):
        if itemId == 0:
            return
        entity = BigWorld.entity(self.entityID)
        if not entity:
            return
        if not getattr(entity, 'isRealModel', True):
            return
        self.release()
        self.loadID += 1
        self.delayID += 1
        self.weaponID = itemId
        modelInfo = self.getAttachments(itemId, subIdIndex, enhLv)
        if ED.data.has_key(itemId):
            subIdList = ED.data[itemId].get('subId', [])
            if subIdList and subIdIndex < len(subIdList) and WCD.data.has_key(subIdList[subIdIndex]):
                weaponData = WCD.data[subIdList[subIdIndex]]
                for itemData in weaponData:
                    self.attachHasAni = itemData.get('hasAni', False)
                    self.equipType = itemData.get('actType', 0)
                    enhanceTint = self.getEnhanceTint(itemId, subIdIndex, enhLv)
                    if enhanceTint:
                        self.tintEnhanced = True
                    self.isFollow = itemData.get('isFollow', False)
                    self.notSyncRighthWeapon = itemData.get('notSyncRighthWeapon', False)

        else:
            gamelog.error('zf:equipItem:Error Can not find weapon in data ', itemId)
            return
        self.maxCount = len(modelInfo)
        for a in modelInfo:
            fullModelPath = a[0]
            dye = a[1]
            if a[8]:
                dye = a[8]
            res = [fullModelPath, ('*', dye)]
            seqTask.BkgModelLoader(entity, self.threadID, res, callbackHelper.Functor(self._modelLoadFinish, a), self.loadID)

        self.state = DETACHED

    def getAttachments(self, itemId, subIdIndex = 0, enhLv = 0, physique = None):
        attachments = []
        entity = BigWorld.entity(self.entityID)
        if ED.data.has_key(itemId):
            ed = ED.data[itemId]
            subIdList = ed.get('subId', [])
            accordingType = ID.data.get(itemId, {}).get('accordingType', gametypes.USE_ACCORD_BY_SCHOOL)
            if subIdList and subIdIndex < len(subIdList) and WCD.data.has_key(subIdList[subIdIndex]):
                modelId = ed.get('modelId', 0)
                weaponData = WCD.data[subIdList[subIdIndex]]
                for itemData in weaponData:
                    wcdSubId = itemData.get('subId', 0)
                    if accordingType == gametypes.USE_ACCORD_BY_SCHOOL:
                        school = getattr(entity, 'realSchool', 0)
                        if physique:
                            school = physique.school
                        weaponName = '_'.join((str(modelId), '0%s' % school, wcdSubId))
                    elif accordingType == gametypes.USE_ACCORD_BY_BODY_TYPE:
                        weaponName = '_'.join((str(modelId), '00', wcdSubId))
                    modelPath = 'item/model/' + str(modelId) + '/' + weaponName + '.model'
                    attachHP = itemData.get('attachHp', None)
                    attachHP2 = itemData.get('attachHp2', None)
                    hangHP = itemData.get('hangHp', None)
                    if physique:
                        scaleKey = clientcom.getAvatarWeaponModelScaleByPhysique(physique)
                    else:
                        scaleKey = clientcom.getAvatarWeaponModelScale(entity)
                    if gameglobal.rds.isSinglePlayer:
                        hangScale = attachScale = itemData.get('m1Scale', 1.0)
                    else:
                        hangScale = attachScale = itemData.get(scaleKey, 1.0)
                    effect = self.getEnhanceEffect(itemId, subIdIndex, enhLv)
                    dye = clientcom.getMatrialsName(entity, ed)
                    enhanceTint = self.getEnhanceTint(itemId, subIdIndex, enhLv)
                    hasAni = itemData.get('hasAni', False)
                    attachEff = itemData.get('attachEff', [])
                    hangUpEff = itemData.get('hangUpEff', [])
                    attachIdleAction = itemData.get('attachIdleAction', None)
                    hangUpIdleAction = itemData.get('hangUpIdleAction', None)
                    attachAction = itemData.get('attachAction', None)
                    hangUpAction = itemData.get('hangUpAction', None)
                    attachments.append((modelPath,
                     dye,
                     attachHP,
                     hangHP,
                     attachScale,
                     hangScale,
                     effect,
                     attachHP2,
                     enhanceTint,
                     hasAni,
                     attachEff,
                     hangUpEff,
                     attachIdleAction,
                     hangUpIdleAction,
                     attachAction,
                     hangUpAction))

        return attachments

    def _modelLoadFinish(self, info, loadID, model):
        gamelog.debug('_modelLoadFinish:', info, loadID, model)
        if not model:
            gamelog.error('zf5:Error _modelLoadFinish, model is None', loadID)
            return
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        self.model = model
        self.model.entityId = self.entityID
        if getattr(entity, 'school', 0) == const.SCHOOL_YECHA:
            if hasattr(model, 'resideActions'):
                yeChaActions = SCD.data.get('yeChaPreloadActions', ['171131',
                 '171132',
                 '171133',
                 '171134'])
                model.resideActions(*yeChaActions)
        if loadID == self.loadID:
            self.maxCount -= 1
            self.orginDye = info[1]
            attachHP = info[2]
            hangHP = info[3]
            attachScale = info[4]
            hangScale = info[5]
            effect = info[6]
            attachHP2 = info[7]
            enhanceTint = info[8]
            hasAni, attachEff, hangUpEff, attachIdleAction, hangUpIdleAction, attachAction, hangUpAction = info[9:]
            modelItem = [model,
             None,
             attachHP,
             hangHP,
             attachScale,
             hangScale,
             effect,
             attachHP2,
             enhanceTint,
             hasAni,
             attachEff,
             hangUpEff,
             attachIdleAction,
             hangUpIdleAction,
             attachAction,
             hangUpAction]
            self.models.append(modelItem)
            entity.allModels.append(model)
            if gameglobal.rds.GameState > gametypes.GS_LOGIN:
                shader = BigWorld.BlendFashion(2)
                qualityLv = max(int(appSetting.VideoQualitySettingObj.getVideoQualityLv()), 1)
                dist = gameglobal.ATTACHMODEL_FADE_DIST * qualityLv
                if entity.__class__.__name__ == 'AvatarMonster':
                    if dist < 40:
                        dist = 40
                shader.distance(dist)
                model.distFadeShader = shader
            weaponData = ED.data.get(self.weaponID, {})
            dye = clientcom.getMatrialsName(entity, weaponData)
            if enhanceTint:
                dye = enhanceTint
            if dye:
                tintalt.ta_set_static_states(model, dye, needBuildName=False)
            gamelog.debug('_modelLoadFinish:self.state', self.state, self.models)
            if self.isFollow:
                self.followModel = model
                entModelScale = entity.getItemData().get('modelScale', 1) if hasattr(entity, 'getItemData') else 1
                model.scale = (attachScale * entModelScale, attachScale * entModelScale, attachScale * entModelScale)
                model.expandVisibilityBox(10)
                follow = BigWorld.Follow()
                follow.target = entity.matrix
                bias = (self.followModelBias, 1.5, -0.5)
                if self.ownerModel:
                    bias = (self.followModelBias, self.ownerModel.height, -0.5)
                follow.biasPos = bias
                if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
                    follow.biasTolerance = 0.5
                else:
                    follow.biasTolerance = 2
                follow.speedHalflife = 1
                follow.proximityCallback = self.apprach
                if hasattr(follow, 'lineAttach'):
                    follow.lineAttach = True
                if hasattr(follow, 'fixedSpeed'):
                    follow.fixedSpeed = 2.0
                model.addMotor(follow)
                am = BigWorld.ActionMatcher(entity)
                am.matchActionOnly = True
                am.patience = 12.5
                am.boredNotifier = self.bored
                model.addMotor(am)
                if self.state in (ATTACHED, HANG_UP):
                    self.showFollowModel(True)
                else:
                    self.showFollowModel(False)
            elif self.state == ATTACHED:
                if self.ownerModel:
                    try:
                        self.ownerModel.setHP(attachHP, model)
                        modelItem[1] = attachHP
                        self.ownerModel.node(attachHP).scale(attachScale)
                    except:
                        gamelog.debug('zf5:error attach weapon model failed!!!!!!!!!!!!!!!!!', self.ownerModel.sources)
                        self.state = DETACHED

                else:
                    gamelog.debug('zf5:ownerModel is None, detach model ')
                    self.state = DETACHED
            elif self.state == HANG_UP:
                if self.ownerModel and hangHP:
                    try:
                        if hasattr(entity, 'showBackWaist') and entity.showBackWaist and self.isMutexPart(hangHP):
                            modelItem[1] = None
                        else:
                            self.ownerModel.setHP(hangHP, model)
                            modelItem[1] = hangHP
                            self.ownerModel.node(hangHP).scale(hangScale)
                    except:
                        self.state = DETACHED

                else:
                    self.state = DETACHED
            elif self.state == ATTACHED_RIGHT:
                if self.ownerModel:
                    try:
                        if attachHP.find('right') != -1:
                            self.ownerModel.setHP(attachHP, model)
                            modelItem[1] = attachHP
                            self.ownerModel.node(attachHP).scale(attachScale)
                        else:
                            self.ownerModel.setHP(hangHP, model)
                            modelItem[1] = hangHP
                            self.ownerModel.node(hangHP).scale(hangScale)
                    except:
                        self.state = DETACHED

                self.state = ATTACHED_RIGHT
            self.setSoundCallback(entity, model)
        if self.maxCount == 0:
            self.updateWeaponAction()
            self.updateWeaponEffect()
            self.updateWeaponVisible()
            if self.state == ATTACHED:
                self.updateWeaponFashionTintByAttach()
            entity.afterWeaponUpdate(self)

    def setSoundCallback(self, entity, model):
        if not model or not model.inWorld:
            return
        if self.followModelBias > 0 or self.isFollow:
            model.soundCallback(self.actionCueCallback)
        elif entity and entity.fashion and model:
            model.soundCallback(entity.fashion.actionCueCallback)

    def apprach(self, isMoving, speed = 0):
        if self.followModel and isMoving:
            self.followModel.action(FOLLOW_SPECIAL_IDLE_ACTION).stop()

    def bored(self, actionName, scale):
        entity = BigWorld.entity(self.entityID)
        if entity.inMoving():
            return
        if actionName != FOLLOW_IDLE_ACTION:
            return
        self.followModel.action(FOLLOW_SPECIAL_IDLE_ACTION)()
        self.followModel.motors[1].patience = 12.5
        self.followModel.motors[1].fuse = 0

    def detach(self, isNeedSetCaps = True, detachType = None):
        self.delayID += 1
        if not self.ownerModel or self.state == DATA_ERROR:
            return False
        if self.isFollow:
            self.showFollowModel(False)
        else:
            for m in self.models:
                try:
                    if m[1]:
                        if detachType and detachType == DETACH_LEFT:
                            if m[1].find('left') == -1:
                                continue
                        if detachType and detachType == DETACH_RIGHT:
                            if m[1].find('right') == -1:
                                continue
                        self.ownerModel.setHP(m[1], None)
                        node = self.ownerModel.node(m[1])
                        if node:
                            node.scale(1)
                        m[1] = None
                    if m[2].find('left') != -1:
                        m[0].setHP(ZHUSHOU_LEFT_ATTACH_NODE, None)
                    elif m[2].find('right') != -1:
                        m[0].setHP(ZHUSHOU_RIGHT_ATTACH_NODE, None)
                except:
                    pass

        if self.fuShouModelLeft:
            self.fuShouModelLeft.setHP(ZHUSHOU_LEFT_ATTACH_NODE, None)
        if self.fuShouModelRight:
            self.fuShouModelRight.setHP(ZHUSHOU_RIGHT_ATTACH_NODE, None)
        self.state = DETACHED
        entity = BigWorld.entity(self.entityID)
        if entity and not getattr(entity, 'isOnlyClient', False):
            entity.afterWeaponUpdate(self)
        return True

    def detachRightToLeft(self):
        if self.fuShouModelRight:
            self.fuShouModelRight.setHP(ZHUSHOU_RIGHT_ATTACH_NODE, None)
        if self.fuShouModelLeft:
            self.fuShouModelLeft.setHP(ZHUSHOU_LEFT_ATTACH_NODE, None)

    def attach(self, model, isNeedSetCaps = True, isRightHand = False, haveAct = False, attachType = None):
        newState = ATTACHED_RIGHT if isRightHand and self.attachType == ATTACHED_RIGHT else ATTACHED
        if attachType:
            newState = attachType
        if self.state == DATA_ERROR or self.state == newState or not model:
            return
        if self.ownerModel and model != self.ownerModel:
            self.detach()
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.fashion:
            return
        delayActTime = 0
        self.delayID += 1
        if delayActTime > 0:
            BigWorld.callback(delayActTime, callbackHelper.Functor(self._realAttach, self.delayID, entity, model, newState, haveAct))
        else:
            self._realAttach(self.delayID, entity, model, newState, haveAct)

    def getWeaponModelPart(self, right = True):
        for a in self.models:
            if right:
                if a[2].find('right') != -1:
                    return a[0]
            elif a[2].find('left') != -1:
                return a[0]

    def attachMidWeaponAll(self):
        ent = BigWorld.entity(self.entityID)
        if not ent or not ent.inWorld:
            return
        for a in self.models:
            try:
                self.ownerModel.setHP(a[2], a[0])
                a[1] = a[2]
                node = self.ownerModel.node(a[1])
                if node:
                    node.scale(a[4])
            except:
                gamelog.error('zf:error2 attach weapon model failed ', self.models)

    def attachMidWeaponLeft(self):
        ent = BigWorld.entity(self.entityID)
        if not ent or not ent.inWorld:
            return
        for a in self.models:
            try:
                if a[2].find('left') != -1:
                    self.ownerModel.setHP(a[2], a[0])
                    a[1] = a[2]
                node = self.ownerModel.node(a[1])
                if node:
                    node.scale(a[4])
            except:
                gamelog.error('zf:error2 attach weapon model failed ', self.models)

    def attachMidWeaponRight(self):
        ent = BigWorld.entity(self.entityID)
        if not ent or not ent.inWorld:
            return
        for a in self.models:
            try:
                if a[2].find('right') != -1:
                    self.ownerModel.setHP(a[2], a[0])
                    a[1] = a[2]
                if a[1]:
                    self.ownerModel.node(a[1]).scale(a[4])
            except Exception as e:
                gamelog.error('m.l@attachMidWeaponRight except', self.models, e.message)

    def _realAttach(self, delayID, entity, model, newState = ATTACHED, haveAct = False):
        if self.delayID != delayID or not entity.inWorld:
            return
        self.delayID += 1
        self.ownerModel = model
        oldState = self.state
        if self.state != newState:
            for m in self.models:
                if m[1]:
                    try:
                        self.ownerModel.setHP(m[1], None)
                    except:
                        gamelog.error('zf:error2 attach weapon model failed ', self.models)

                    m[1] = None

        if self.isFollow:
            self.state = newState
            self.showFollowModel(True)
        elif newState == ATTACHED:
            for a in self.models:
                try:
                    self.ownerModel.setHP(a[2], a[0])
                    a[1] = a[2]
                    self.ownerModel.node(a[1]).scale(a[4])
                except:
                    gamelog.error('zf:error2 attach weapon model failed ', self.models)

            self.state = ATTACHED
        elif newState == ATTACHED_RIGHT:
            for a in self.models:
                try:
                    if a[2].find('right') != -1:
                        self.ownerModel.setHP(a[2], a[0])
                        a[1] = a[2]
                    else:
                        self.ownerModel.setHP(a[3], a[0])
                        a[1] = a[3]
                    self.ownerModel.node(a[1]).scale(a[4])
                except:
                    gamelog.error('zf:error2 attach weapon model failed ', self.models)

            self.state = ATTACHED_RIGHT
        elif newState == ATTACHED_MID_WEAPON_ALL:
            self.attachMidWeaponAll()
            self.state = ATTACHED_MID_WEAPON_ALL
        elif newState == ATTACHED_MID_WEAPON_LEFT:
            self.attachMidWeaponLeft()
            self.state = ATTACHED_MID_WEAPON_LEFT
        elif newState == ATTACHED_MID_WEAPON_RIGHT:
            self.attachMidWeaponRight()
            self.state = ATTACHED_MID_WEAPON_RIGHT
        self.setSoundCallback(entity, self.model)
        self.updateWeaponAction(haveAct)
        self.updateWeaponEffect()
        self.updateWeaponVisible()
        self.updateWeaponFashionTintByAttach()
        if not getattr(entity, 'isOnlyClient', False) and oldState not in (HANG_UP, self.state):
            entity.afterWeaponUpdate(self)
        if getattr(entity, 'buffModelScale', []) and getattr(entity, 'clientStateEffect'):
            entity.clientStateEffect.restoreBufActState()

    def updateWeaponVisible(self):
        entity = BigWorld.entity(self.entityID)
        if not entity:
            return
        if hasattr(entity, 'refreshWeaponVisible'):
            entity.refreshWeaponVisible()

    def hangUp(self, model, isNeedSetCaps = True, haveAct = False):
        gamelog.debug('zf:hangUp ', self.entityID, self.state, self.models)
        if self.state in (DATA_ERROR,):
            return False
        if self.ownerModel and model != self.ownerModel:
            gamelog.debug('zf:hangUp,model changed ', self.entityID)
            self.detach()
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.fashion or not model:
            gamelog.error('zf:hangUp failed ')
            return False
        delayActTime = 0
        gamelog.debug('bgf@weapoModel hangUp2', delayActTime)
        self.delayID += 1
        if delayActTime > 0:
            BigWorld.callback(delayActTime, callbackHelper.Functor(self._realHang, self.delayID, entity, model, haveAct))
        else:
            self._realHang(self.delayID, entity, model, haveAct)

    def _realHang(self, delayID, entity, model, haveAct = False):
        if self.delayID != delayID or not entity.inWorld:
            return
        self.ownerModel = model
        self.delayID += 1
        oldState = self.state
        success = self.state != HANG_UP
        if self.state != HANG_UP:
            for m in self.models:
                if m[1]:
                    try:
                        self.ownerModel.setHP(m[1], None)
                    except:
                        gamelog.error('zf:error attach weapon model failed ', self.models)

                    m[1] = None

        if self.isFollow:
            self.state = HANG_UP
            self.showFollowModel(True)
        elif self.state != HANG_UP:
            for a in self.models:
                try:
                    if hasattr(entity, 'showBackWaist') and entity.showBackWaist and self.isMutexPart(a[3]):
                        a[1] = None
                    else:
                        self.ownerModel.setHP(a[3], a[0])
                        a[1] = a[3]
                        self.ownerModel.node(a[3]).scale(a[5])
                except:
                    gamelog.error('zf:error attach weapon model failed ', self.models)

            self.state = HANG_UP
        self.setSoundCallback(entity, self.model)
        self.updateWeaponAction(haveAct)
        self.updateWeaponEffect()
        self.updateWeaponVisible()
        self.updateWeaponFashionTintByHang()
        if not getattr(entity, 'isOnlyClient', False) and oldState not in (ATTACHED, ATTACHED_RIGHT, self.state):
            entity.afterWeaponUpdate(self)
        return success

    def updateWeaponFashionTintByHang(self):
        if ED.data.has_key(self.weaponID):
            attachFashionTint = ED.data[self.weaponID].get('attachFashionTint', '')
            if attachFashionTint:
                entity = BigWorld.entity(self.entityID)
                for model in self.models:
                    tintalt.ta_set_static([model[0]], clientcom.getMatrialsName(entity, ED.data[self.weaponID]))

        else:
            gamelog.error('zf:equipItem:Error Can not find weapon in data ', self.weaponID)
            return

    def updateWeaponFashionTintByAttach(self):
        if ED.data.has_key(self.weaponID):
            attachFashionTint = ED.data[self.weaponID].get('attachFashionTint', '')
            if attachFashionTint:
                for model in self.models:
                    tintalt.ta_set_static([model[0]], attachFashionTint)

        else:
            gamelog.error('zf:equipItem:Error Can not find weapon in data ', self.weaponID)
            return

    def hangUpDirectly(self, model):
        self.ownerModel = model
        if self.state == ATTACHED:
            for m in self.models:
                if m[1]:
                    self.ownerModel.setHP(m[1], None)
                    m[1] = None

        if self.state != HANG_UP:
            for a in self.models:
                if a[3]:
                    try:
                        self.ownerModel.setHP(a[3], a[0])
                        a[1] = a[3]
                        self.ownerModel.node(a[3]).scale(a[5])
                    except:
                        gamelog.error('zf:error attach weapon model failed ', self.models)

            self.state = HANG_UP
            self.updateWeaponAction()
            self.updateWeaponEffect()

    def attachDirectly(self, model):
        self.ownerModel = model
        if self.state == HANG_UP:
            for m in self.models:
                if m[1]:
                    self.ownerModel.setHP(m[1], None)
                    m[1] = None

        if self.state != ATTACHED:
            for a in self.models:
                try:
                    self.ownerModel.setHP(a[2], a[0])
                    a[1] = a[2]
                    self.ownerModel.node(a[1]).scale(a[4])
                except:
                    gamelog.error('zf:error2 attach weapon model failed ', self.models)

            self.state = ATTACHED
            self.updateWeaponAction()
            self.updateWeaponEffect()

    def getWeaponMatchCaps(self, weaponType):
        entity = BigWorld.entity(self.entityID)
        if hasattr(entity, 'bianshen') and entity._isOnZaijuOrBianyao():
            return [keys.CAPS_HAND_FREE]
        else:
            return [weaponType]

    def isAttached(self):
        return self.state in (ATTACHED, ATTACHED_RIGHT)

    def isHangUped(self):
        return self.state == HANG_UP

    def isDetached(self):
        return self.state == DETACHED

    def showFollowModel(self, isShow = True):
        if not self.followModel:
            return
        ent = BigWorld.entity(self.entityID)
        if ent and ent.inWorld:
            if isShow:
                for a in self.models:
                    a[1] = a[2]

                if self.followModel not in ent.followModel:
                    ent.followModel.append(self.followModel)
                if not self.followModel.inWorld:
                    ent.addModel(self.followModel)
                if ent.model:
                    self.followModel.visible = ent.model.visible
            else:
                for a in self.models:
                    a[1] = None

                if self.followModel in ent.followModel:
                    ent.followModel.remove(self.followModel)
                if self.followModel.inWorld:
                    ent.delModel(self.followModel)

    def isMutexPart(self, hp):
        return True

    def updateBackWaist(self, show = True):
        if self.isHangUped():
            if self.isFollow:
                return
            for a in self.models:
                if self.isMutexPart(a[3]):
                    try:
                        if show:
                            self.ownerModel.setHP(a[3], a[0])
                            a[1] = a[3]
                            self.ownerModel.node(a[3]).scale(a[5])
                        elif a[1]:
                            self.ownerModel.setHP(a[1], None)
                            a[1] = None
                            node = self.ownerModel.node(a[1])
                            if node:
                                node.scale(1)
                    except:
                        gamelog.error('zf:error attach weapon model failed ', self.models)

            if show:
                self.updateWeaponEffect()
                self.updateWeaponAction()

    def getModels(self):
        model = []
        for item in self.models:
            model.append(item[0])

        return model

    def getPhotoAction(self, key = None, data = None):
        return None
