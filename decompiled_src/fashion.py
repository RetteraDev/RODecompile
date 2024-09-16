#Embedded file name: /WORKSPACE/data/entities/client/helpers/fashion.o
import random
import inspect
import BigWorld
import action
import monsterAction
import npcAction
import const
import keys
import ufo
import utils
import charRes
import gameglobal
import clientcom
import gamelog
import gametypes
import footTrigger
import appSetting
from sfx import sfx
from impJumpFashion import ImpJumpFashion
from impActionFashion import ImpActionFashion
from impFootFashion import ImpFootFashion
from impActionCueFashion import ImpActionCueFashion
from helpers import outlineHelper
from helpers import tintalt
from callbackHelper import Functor
from data import sys_config_data as SYSCD
from data import physics_config_data as PCD
from data import zaiju_data as ZD
from data import guild_job_data as JOBD
from data import avatar_action_config_data as AASD
from data import equip_data as ED
from data import foot_dust_data as FDD
from data import ride_together_data as RTD
BoundingBoxNodes = ('biped Head', 'biped Spine1', 'biped R Hand', 'biped L Hand', 'biped R Calf', 'biped L Calf', 'biped R Foot', 'biped L Foot', 'biped L Forearm', 'biped R Forearm', 'Scene Root', 'HP_head1')
LoginModelBoundingBoxNodes = ('biped Head', 'biped Spine1', 'biped R Hand', 'biped L Hand', 'biped R Calf', 'biped L Calf', 'biped R Foot', 'biped L Foot', 'biped L Forearm', 'biped R Forearm')

class ActionNameCache(object):

    def __init__(self):
        self.actionNameMap = {}
        self.sourcesActionMap = {}

    def getActionNameList(self, model):
        sources = ''
        if model:
            sources = model.sources[-1]
        if self.sourcesActionMap.has_key(sources):
            value = self.sourcesActionMap[sources]
            self.incRef(sources, value)
            return value
        actionNameList = []
        if model:
            actionNameList = model.actionNameList()
        actionNameSet = frozenset(actionNameList)
        self.incRef(sources, actionNameSet)
        return actionNameSet

    def decRef(self, modelPath, value):
        count = self.actionNameMap.get(value, 0)
        if count:
            count -= 1
            if count == 0:
                self.actionNameMap.pop(value, None)
                self.sourcesActionMap.pop(modelPath, None)
            else:
                self.actionNameMap[value] = count

    def incRef(self, modelPath, value):
        count = self.actionNameMap.get(value, 0)
        count += 1
        if count == 1:
            self.sourcesActionMap[modelPath] = value
        self.actionNameMap[value] = count


gActionNameCache = ActionNameCache()

class FashionMeta(type):

    def __init__(cls, name, bases, dic):
        super(FashionMeta, cls).__init__(name, bases, dic)
        inherits = (ImpJumpFashion,
         ImpActionFashion,
         ImpFootFashion,
         ImpActionCueFashion)
        for inherit in inherits:
            FashionMeta._moduleMixin(cls, name, inherit)

    def _moduleMixin(cls, name, module):
        for name, fun in inspect.getmembers(module, inspect.ismethod):
            setattr(cls, name, fun.im_func)

        for name, memb in inspect.getmembers(module):
            if name == '__module__':
                continue
            if memb.__class__.__name__ in const.BUILTIN_OBJS:
                setattr(cls, name, memb)


class Fashion(object):
    EMOTE_PROBABILITY = 100
    BORED_BY_CLIENT = 1
    BORED_BY_SERVER = 2
    __metaclass__ = FashionMeta

    def __init__(self, owner):
        self.owner = owner
        self.ufo = None
        self.dummyUFO = None
        self.oldUFO = ufo.UFO_SHADOW
        self.footprintID = 0
        self.modelPath = None
        self.turnModelToEntity = True
        self.weaponType = 0
        self.bodyTwistSpeed = 100
        self.isStartJump = False
        self.fallEndAction = None
        self.modelID = 0
        self.opacity = -1
        self.boredTime = SYSCD.data.get('boredTime', gameglobal.BORED_TIME)
        self.boredIdleProbability = SYSCD.data.get('boredIdleProb', gameglobal.BOREDIDLE_PROBABILITY)
        self.moveBoredIdleProbability = SYSCD.data.get('moveBoredIdleProbability', 30)
        self.wearBoredIdleProbability = SYSCD.data.get('wearBoredIdleProbability', 40)
        self.fashionBoredIdleProbability = SYSCD.data.get('fashionBoredIdleProbability', 30)
        self.boredIdleProbabilityForWuHun = SYSCD.data.get('boredIdleProbabilityForWuHun', 5)
        p = BigWorld.player()
        self.isPlayer = p and owner == p.id
        self.modelPath = ['', '', '']
        self.doingActionCount = 0
        self._doingActionType = action.UNKNOWN_ACTION
        self.playedFx = []
        self.playedTintFx = []
        self.playedAction = {}
        self.actionKey = 0
        self.actRandom = 1
        self.fallAutoJumpActRandom = 0
        self.footTriggerMgr = footTrigger.FootTriggerMgr(self.owner)
        self.trackerModel = None
        self.tracker = BigWorld.Tracker()
        self.tracker.maxLod = 40
        self.tracker.ignoreInvisible = True
        self.fobidHeadTrack = False
        self.headTracking = False
        self.nodeInfo = None
        self.directionProvider = None
        self.boredController = Fashion.BORED_BY_CLIENT
        self.weaponCallback = None
        self.boredAct = None
        self.rushActionIndex = 0
        self.wingFlyActionList = []
        self.dieActionGroupId = 0
        self.action = None
        self.idleType = gametypes.IDLE_TYPE_NORMAL
        self.cueSound = {}
        self.cueVoice = {}
        self.cueEffect = {}
        self.freezedEffs = []

    def release(self):
        owner = BigWorld.entity(self.owner)
        if self.action:
            gActionNameCache.decRef(self.modelPath[-1] if self.modelPath else '', self.action.actionList)
        if not owner or not owner.inWorld:
            return
        if owner.model != None:
            self.detachFootTrigger()
            self.attachUFO(ufo.UFO_NULL)
            if len(owner.model.motors) > 0:
                owner.model.motors = []
        if self.trackerModel != None:
            self.tracker.directionProvider = None
            self.trackerModel.tracker.nodeInfo = None
            self.trackerModel.tracker = None
            self.trackerModel = None
            self.headTracking = False
        if self.nodeInfo != None:
            self.nodeInfo = None
        if self.directionProvider != None:
            self.directionProvider = None
        self.action = None
        self.modelID = 0
        if hasattr(owner, 'am'):
            owner.am.boredNotifier = None
            owner.am.climbNotifier = None
            owner.am.fallNotifier = None
            owner.am.jumpNotifier = None
            owner.am.moveNotifier = None
            owner.am.startMovingNotifier = None
            owner.am = None
        self._releaseFx()
        self.actionKey = 0
        self.wingFlyActionList = []
        self.playedAction = {}
        self.footTriggerMgr.release()
        self.footTriggerMgr = None
        self.cueSound = {}
        self.cueVoice = {}
        self.cueEffect = {}

    def getModel(self):
        return BigWorld.entity(self.owner).model

    def calcModelID(self):
        try:
            modelPath = self.modelPath[-1]
            owner = BigWorld.entity(self.owner)
            if hasattr(owner, 'inRiding') and owner.inRiding():
                self.modelID = int(modelPath[5:10])
            elif modelPath[4] == '/':
                self.modelID = int(modelPath[5:10])
            elif modelPath.startswith('::/'):
                self.modelID = int(modelPath[modelPath.find('/', 3) + 1:][5:10])
            else:
                self.modelID = int(modelPath[6:10])
        except:
            pass

    def loadDummyModel(self, hasUFO = True):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        model = sfx.getDummyModel(False)
        model.dummyModel = True
        owner.model = model
        model.position = owner.position
        model.visible = True
        model.noAttachFx_ = True
        self.modelPath = model.sources
        self.modelID = 0
        am = BigWorld.ActionMatcher(owner)
        owner.am = am
        model.motors = (am,)
        self.dummyUFO = None
        owner.setTargetCapsUse(False)
        if hasattr(owner, 'monsterInstance'):
            if owner.isAvatarMonster():
                self.action = action.getActionGroup(self.modelID)
            else:
                self.action = monsterAction.getMonsterActionGroup(owner)
        elif hasattr(owner, 'npcInstance'):
            self.fobidHeadTrack = True
            self.action = npcAction.getNpcActionGroup(owner)
        else:
            self.action = action.getActionGroup(self.modelID)
        if self.action == None:
            gamelog.debug('get actiongroup is error:', owner.id)
            return
        if hasattr(self.action, 'actionList'):
            if self.action.actionList == None:
                self.action.actionList = gActionNameCache.getActionNameList(None)

    def setIdleType(self, idleType):
        if self.idleType != idleType:
            self.idleType = idleType
            owner = BigWorld.entity(self.owner)
            if owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                data = FDD.data.get(self.modelID, {})
                if data.get('enableIdlePlus', None):
                    self.autoSetStateCaps()

    def loadObstacleModel(self, modelName, matrix, dynamic = False, dye = None):
        BigWorld.fetchObstacleModel(modelName, matrix, dynamic, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if model == None:
            return
        owner = BigWorld.entity(self.owner)
        if owner.model != None:
            oldModel = owner.model
            owner.model = model
            if hasattr(oldModel, 'noAttachFx_'):
                oldModel.motors = ()
                oldModel.noAttachFx_ = False
                if self.dummyUFO:
                    oldModel.root.detach(self.dummyUFO.obj)
                    ufo.giveBack(self.dummyUFO)
                    self.dummyUFO = None
                sfx.giveBackDummyModel(oldModel, False)
        else:
            owner.model = model
        model.renderFlag = gameglobal.AMBIENT_INC
        owner.am = BigWorld.ActionMatcher(owner)
        self.modelPath = model.sources
        self.calcModelID()

    def loadSinglePartModel(self, modelName, dyeName = 'Default', callback = None):
        charRes.getSimpleModel(modelName, dyeName, Functor(self._afterSingleModelFinished, callback))

    def _afterSingleModelFinished(self, callback, model):
        if callback:
            callback(model)
        else:
            self.setupModel(model)

    def setModelNeedNoDraw(self, model):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if not model:
            return
        if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            return
        try:
            if owner.__class__.__name__ == 'Avatar':
                model.modelNeedNoDraw = True
        except:
            pass

    def clearTrail(self, model):
        if hasattr(model, 'trail'):
            model.trail = None

    def setupModel(self, newModel, needReset = True):
        if newModel == None:
            return
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        self.initAction()
        if self.ufo != None:
            oldUfo = self.ufo.ufoType
        else:
            oldUfo = ufo.UFO_SHADOW
        if owner.model != None:
            self.detachFootTrigger()
            self.attachUFO(ufo.UFO_NULL)
            if hasattr(owner.model, 'soundCallback'):
                owner.model.soundCallback(None)
        if hasattr(owner, 'getOpacityValue'):
            opValue = owner.getOpacityValue()
            if opValue[0] == gameglobal.OPACITY_HIDE:
                newModel.visible = False
        newModel.renderFlag = gameglobal.AMBIENT_INC
        oldCaps = []
        if owner.model != None:
            oldModel = owner.model
            if len(oldModel.motors) > 0 and oldModel.motors[0].__name__ == 'ActionMatcher':
                oldCaps = oldModel.motors[0].matchCaps
            if needReset:
                if not getattr(oldModel, 'dummyModel', False):
                    tintalt.ta_reset([oldModel])
                if oldModel in owner.allModels:
                    owner.allModels.remove(oldModel)
            gamelog.debug('@szh: in fashion model', owner.model.sources, newModel.sources)
            if newModel != oldModel:
                try:
                    owner.model = newModel
                except:
                    pass

                if owner.__class__.__name__ == 'Avatar' and owner.model:
                    owner.model.setModelNeedHide(True, 1.0)
            oldModel.visible = True
            self.clearTrail(oldModel)
            if self.isPlayer and hasattr(oldModel, 'footIK'):
                oldModel.footIK = None
            if hasattr(oldModel, 'floatage') and getattr(oldModel, 'floatage'):
                floatage = BigWorld.PyPoseControl()
                owner.model.floatage = floatage
                if hasattr(oldModel.floatage, 'floatHeight'):
                    floatage.floatHeight = oldModel.floatage.floatHeight
                oldModel.floatage = None
            if hasattr(oldModel, 'noAttachFx_'):
                oldModel.motors = ()
                oldModel.noAttachFx_ = False
                if self.dummyUFO:
                    oldModel.root.detach(self.dummyUFO.obj)
                    ufo.giveBack(self.dummyUFO)
                    self.dummyUFO = None
                sfx.giveBackDummyModel(oldModel, False)
            else:
                oldModel = None
        else:
            owner.model = newModel
        if hasattr(owner.model, 'enlargeShadowBoundingBox'):
            owner.model.enlargeShadowBoundingBox(gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[0], gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[1], gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[2], gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[3], gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[4], gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[5])
        if newModel not in owner.allModels:
            owner.allModels.append(newModel)
        newModel.yaw = owner.yaw
        newModel.position = owner.position
        newModel.entityId = self.owner
        oldModelPath = self.modelPath
        self.modelPath = newModel.sources
        self.setModelNeedNoDraw(newModel)
        newModel.soundCallback(self.actionCueCallback)
        self.calcModelID()
        if hasattr(owner, 'monsterInstance'):
            if owner.isAvatarMonster():
                self.action = action.getActionGroup(self.modelID)
            else:
                self.action = monsterAction.getMonsterActionGroup(owner)
        elif hasattr(owner, 'npcInstance'):
            self.action = npcAction.getNpcActionGroup(owner)
        else:
            self.action = action.getActionGroup(self.modelID)
        if self.action != None:
            if not getattr(owner, 'coupleLoadDummy', False):
                if oldModelPath:
                    gActionNameCache.decRef(oldModelPath[-1] if oldModelPath else '', self.action.actionList)
                self.action.actionList = gActionNameCache.getActionNameList(owner.model)
        if len(newModel.motors) > 0 and newModel.motors[0].__name__ == 'ActionMatcher':
            am = newModel.motors[0]
            am.matchCaps = oldCaps
            if self.modelID in clientcom.gRidableModels:
                am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_RIDE]
            if hasattr(owner, 'isInCoupleRide') and owner.isInCoupleRide():
                am.matchCaps = owner.modelServer.getCoupleMatchCaps()
        else:
            am = BigWorld.ActionMatcher(owner)
            am.matchCaps = oldCaps
            am.inheritOnRecouple = 1
            am.matchActualMovement = False
            if self.modelID in clientcom.gRidableModels:
                am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_RIDE]
                am.minFrequence = 1
            elif hasattr(owner, 'monsterInstance') and not owner.isAvatarMonster():
                if owner.isAvatarMonster():
                    matchCap = keys.CAPS_HAND_FREE
                    if owner.inCombat:
                        matchCap = self.getWeaponActType()
                    am.matchCaps = [matchCap, keys.CAPS_GROUND]
                idleCap = self.getCapsIdle()
                if not owner.isMultiPartMonster():
                    if not owner.inCombat:
                        self.setMonsterIdleCaps(am)
                    else:
                        self.setMonsterCombatCaps(am)
                else:
                    self.setMonsterIdleCaps(am)
            elif hasattr(owner, 'npcInstance'):
                if self.action:
                    idleCap = self.action.getActCaps()
                else:
                    idleCap = keys.CAPS_IDLE0
                if isinstance(idleCap, tuple):
                    am.matchCaps = list(idleCap)
                else:
                    am.matchCaps = [idleCap, keys.CAPS_GROUND]
            elif hasattr(owner, 'avatarInstance'):
                matchCap = keys.CAPS_HAND_FREE
                if owner.inCombat and not owner.bufActState:
                    matchCap = self.getWeaponActType()
                    am.matchCaps = [matchCap, keys.CAPS_GROUND]
                elif owner.canFly():
                    am.matchCaps = [matchCap, keys.CAPS_FLY]
                elif owner.canSwim():
                    am.matchCaps = [matchCap, keys.CAPS_SWIM]
                elif hasattr(owner, 'runOnWater') and owner.runOnWater:
                    am.matchCaps = [matchCap, keys.CAPS_RUN_ON_WATER]
                elif not owner.bufActState:
                    am.matchCaps = [matchCap, keys.CAPS_GROUND]
                if hasattr(owner, 'isInCoupleRide') and owner.isInCoupleRide():
                    am.matchCaps = owner.modelServer.getCoupleMatchCaps()
            else:
                am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND]
            newModel.motors = (am,)
        am.matcherCoupled = True
        am.applyTwistSmooth = True
        am.minFallDist = PCD.data.get('minFallDist', 0.1)
        am.fallNotifier = self.fall
        am.jumpNotifier = self.jump
        owner.am = am
        if owner.needMoveNotifier():
            am.moveNotifier = self.movingNotifier
            am.applyMoveSmooth = True
            if hasattr(am, 'verticalMoveNotifier'):
                am.verticalMoveNotifier = self.verticalMoveNotifier
        else:
            am.moveNotifier = None
            if hasattr(am, 'verticalMoveNotifier'):
                am.verticalMoveNotifier = None
        self.resetTurnBodyState()
        am.boredNotifier = self.bored
        am.patience = self.boredTime
        am.fuse = 0
        if hasattr(owner, 'getModelScale'):
            baseScale = getattr(owner, 'baseScale', 1)
            if not getattr(owner, 'stateModelScale', None):
                baseScale = 1
            newModel.scale = (owner.getModelScale()[0] * baseScale, owner.getModelScale()[1] * baseScale, owner.getModelScale()[2] * baseScale)
        else:
            gamelog.error('zf:Err:Failed to scale model..........', owner.id, self.modelPath)
        am.matchScale = owner.getMatchScale(newModel.scale[0])
        if self.isPlayer:
            am.applyTwistSmooth = False
            am.applyMoveSmooth = False
            if gameglobal.gEnableFootIK:
                newModel.footIK = BigWorld.FootIK()
                owner.resetFootIK()
            self.setupClimbMatcher(owner, newModel, True)
        elif getattr(owner, 'handClimb', False):
            self.setupClimbMatcher(owner, newModel, False)
        if hasattr(self.action, 'actionList') and len(self.action.actionList) > 0:
            clientcom.setModelIgnoreTpos(newModel)
        self.footTriggers = None
        self.setupFootTrigger()
        if hasattr(owner, 'getOpacityValue'):
            opVal = owner.getOpacityValue()
            if opVal[0] == gameglobal.OPACITY_FULL:
                self.attachUFO(oldUfo)
        else:
            self.attachUFO(oldUfo)
        if owner.__class__.__name__ == 'LoginModel':
            newModel.setBoundingBoxNodes(LoginModelBoundingBoxNodes)
        elif not getattr(owner, 'isMagicField', False):
            newModel.setBoundingBoxNodes(BoundingBoxNodes)
        if not getattr(owner, 'IsMonster', False):
            outlineHelper.checkModelChange(owner)
        self.resetModelRoll()
        if hasattr(owner, 'avatarInstance') and self.footTriggerMgr:
            self.footTriggerMgr.playFootIdleEffect()
        if FDD.data.get(self.modelID, {}).has_key('modelNotNeedHide'):
            modelNotNeedHide = FDD.data.get(self.modelID, {}).get('modelNotNeedHide', 0)
            owner.model.setModelNeedHide(not modelNotNeedHide, 1.0)

    def getCapsIdle(self):
        capsIdle = self.action.getCapsIdle(self)
        return capsIdle

    def setMonsterIdleCaps(self, am):
        idleCap = self.getCapsIdle()
        if isinstance(idleCap, tuple):
            am.matchCaps = list(idleCap)
        else:
            am.matchCaps = [idleCap, keys.CAPS_GROUND]

    def setMonsterCombatCaps(self, am):
        idleCap = self.action.getCapsCombat(self)
        if isinstance(idleCap, tuple):
            am.matchCaps = list(idleCap)
        else:
            am.matchCaps = [idleCap, keys.CAPS_GROUND_COMBAT]

    def getCapsIdleName(self):
        idleNames = ('1101', '1104', '1107')
        capsIdle = self.action.getCapsIdle(self)
        return idleNames[capsIdle - 1]

    def bored(self, actionName, scale):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        p = BigWorld.player()
        if (owner.position - p.position).lengthSquared > gameglobal.MAX_DISTANCE_BORED_ACTION * gameglobal.MAX_DISTANCE_BORED_ACTION:
            return
        owner.am.fuse = 0
        owner.am.patience = self.boredTime
        if owner.inMoving() and not owner.IsAvatar:
            return
        if hasattr(owner, 'inCombat') and not owner.inCombat and self.boredController == Fashion.BORED_BY_SERVER:
            return
        if getattr(owner, 'inCombat', False):
            return
        if getattr(owner, 'inGuard', False) or self.doingActionType() in [action.INCOMBAT_START_ACTION, action.BORED_ACTION]:
            return
        if owner.IsMonster and owner.bornStage > 0:
            return
        if actionName:
            actionName = actionName.split('_')[-1]
        if owner.IsAvatar and not (actionName in gameglobal.COND_CHECK_BORED_ACT or keys.CAPS_WEAR in owner.am.matchCaps):
            return
        if owner.IsAvatar:
            if random.randint(0, 100) < self.wearBoredIdleProbability:
                owner.modelServer.playWearBoredActionRandomly()
            if not owner.inMoving():
                if random.randint(0, 100) < owner.getFaceIdleFxProb():
                    owner.playFaceIdleFxs()
                if random.randint(0, 100) < self.fashionBoredIdleProbability:
                    owner.modelServer.playFashionBoredEffect()
            owner.checkRefineEquipmentFlagIdle()
        if self.isPlayer and gameglobal.rds.cam.currentScrollNum < 3:
            return
        if hasattr(owner.model, 'poser') and owner.model.poser.enableLookAt:
            return
        boredIdleProb = self.moveBoredIdleProbability if owner.IsAvatar and owner.inMoving() else self.boredIdleProbability
        if random.randint(0, 100) < boredIdleProb:
            if not self.action:
                return
            if self.isPlayer:
                self.headCtrlStop()
            self.playBoredAction(scale)
            apEffectEx = getattr(owner, 'apEffectEx', None)
            if apEffectEx:
                apEffectEx.playBoredAction()
        else:
            self.headCtrlStart()
        boredIdleProbForWuhun = self.boredIdleProbabilityForWuHun
        if owner.IsAvatar and random.randint(0, 100) < boredIdleProbForWuhun and not owner.inFly and not owner.inRiding():
            if not (hasattr(owner, 'isRidingTogetherAsVice') and owner.isRidingTogetherAsVice()):
                owner.showWuhunEffect(False)

    def checkHeadCtrl(self):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return False
        if not self.isPlayer:
            return False
        if owner.inCombat or owner.bsState or owner.inFly or owner.bianshen[0]:
            return False
        if owner.modelServer.headCtrl.isResuming or owner.modelServer.eyeBallCtrl.isResuming:
            return False
        if gameglobal.rds.cam.cc.direction.yaw == BigWorld.dcursor().yaw:
            return False
        return True

    def headCtrlStart(self):
        if gameglobal.gDisableFaceEmote:
            return
        if not self.checkHeadCtrl():
            return
        self.headTracking = True
        owner = BigWorld.entity(self.owner)
        owner.modelServer.headCtrl.headLookAtCamera()
        owner.modelServer.eyeBallCtrl.eyeLookAtCamera()

    def headCtrlStop(self):
        if gameglobal.gDisableFaceEmote:
            return
        if not self.headTracking:
            return
        self.headTracking = False
        owner = BigWorld.entity(self.owner)
        owner.modelServer.headCtrl.resetHeadCtrl()
        owner.modelServer.eyeBallCtrl.resetEyeCtrl()

    def setBoredController(self, source):
        self.boredController = source

    def specialIdleAction(self, owner):
        schoolBoredAction = None
        modelID = owner.fashion.modelID
        school = owner.school
        key = (modelID, school)
        typeData = AASD.data.get(key, {})
        typeIdle = typeData.get('idleType', gametypes.SPECIAL_IDLE_STATE_A)
        boredActions = self.getBoredActionNames()
        if boredActions:
            boredAction = random.choice(boredActions)
            if typeIdle == gametypes.SPECIAL_IDLE_STATE_A:
                self.boredAct = boredAction
            elif typeIdle == gametypes.SPECIAL_IDLE_STATE_SA:
                if boredAction and owner.IsAvatar:
                    if owner.isNeedSchoolBoredAction():
                        schoolBoredAction = str(getattr(owner, 'school', 0)) + '_' + boredAction
                        if schoolBoredAction in owner.fashion.getActionNameList():
                            self.boredAct = schoolBoredAction
                        else:
                            self.boredAct = boredAction
                    else:
                        self.boredAct = boredAction
                else:
                    self.boredAct = None
            elif typeIdle == gametypes.SPECIAL_IDLE_STATE_R:
                if boredAction and owner.IsAvatar:
                    if owner.isNeedSchoolBoredAction():
                        schoolBoredAction = str(getattr(owner, 'school', 0)) + '_' + boredAction
                        if schoolBoredAction:
                            randomBoredAction = random.choice([boredAction, schoolBoredAction])
                            self.boredAct = randomBoredAction
                        else:
                            self.boredAct = boredAction
                    else:
                        self.boredAct = boredAction
                else:
                    self.boredAct = None
        else:
            self.boredAct = None

    def skipCoupleRideBored(self, owner):
        return not RTD.data.get(owner.bianshen[1], {}).get('useCoupleBoredAct', False)

    def playBoredAction(self, scale_ = 1.0):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if owner.inMoving() and not owner.IsAvatar:
            return
        if hasattr(owner, 'inCombat') and not owner.inCombat and self.boredController == Fashion.BORED_BY_SERVER:
            return
        if getattr(owner, 'inGuard', False) or self.doingActionType() in [action.INCOMBAT_START_ACTION, action.BORED_ACTION]:
            return
        if hasattr(owner, 'isInCoupleRide') and owner.isInCoupleRide():
            return
        if getattr(owner, 'tride', None) and owner.tride.inRide() and self.skipCoupleRideBored(owner):
            return
        dawlderJobId = getattr(owner, 'jobId', 0)
        if dawlderJobId:
            jData = JOBD.data.get(dawlderJobId, {})
            if jData.get('forbidSpecialIdle', False):
                return
        if owner.IsMonster and owner.bornStage > 0:
            return
        if hasattr(owner, 'inDaZuo') and owner.inDaZuo() or hasattr(owner, 'isInCoupleRide') and owner.isInCoupleRide():
            return
        if owner.IsAvatar:
            self.specialIdleAction(owner)
        else:
            boredActions = self.getBoredActionNames()
            if boredActions:
                boredAction = random.choice(boredActions)
                if boredAction and owner.IsAvatar:
                    schoolBoredAction = str(getattr(owner, 'school', 0)) + '_' + boredAction
                    if schoolBoredAction in owner.fashion.getActionNameList():
                        self.boredAct = schoolBoredAction
                self.boredAct = boredAction
            else:
                self.boredAct = None
        if not owner.inMoving():
            scale_ = 1.0
        elif owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            scale_ = 1.0
        self.playSingleAction(self.boredAct, action.BORED_ACTION, 0, None, 0, scale_)
        if owner.IsAvatar and self.boredAct:
            owner.qinggongMgr.playWingFlyModelAction([self.boredAct], scale_)
            wear = owner.modelServer.getShowWear()
            wear.doAction(self.boredAct) if wear else None

    def incrRrushActionIndex(self):
        self.rushActionIndex = self.rushActionIndex + 1
        self.rushActionIndex = self.rushActionIndex % 3

    def getHorseWingActionIdx(self):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if not hasattr(owner, 'bianshen'):
            return
        if owner.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            idx = ZD.data.get(owner.bianshen[1], {}).get('zaijuActionIdx', None)
            if idx:
                return idx
        isInHorse = owner.inRiding() and owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
        if not isInHorse and not owner.inFly:
            return
        itemId = 0
        if owner.inFlyTypeWing():
            itemId = owner.modelServer.wingFlyModel.key
        else:
            itemId = owner.bianshen[1]
        if not itemId:
            return
        idx = ED.data.get(itemId, {}).get('horseWingActionIdx', None)
        return idx

    def hide(self, isHide, retainTopLogo = False):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        if not owner.model:
            return
        visible = not isHide
        owner.model.visible = visible
        if visible and hasattr(owner, 'clearFade'):
            owner.clearFade()
        if isHide:
            self.opacity = 0
            if hasattr(owner.model, 'soundCallback') and not getattr(owner, 'IsMonster', False):
                owner.model.soundCallback(None)
        else:
            self.opacity = 255
            if hasattr(owner.model, 'soundCallback'):
                owner.model.soundCallback(self.actionCueCallback)
        if owner.topLogo != None:
            if not retainTopLogo:
                if hasattr(owner, 'isOnWingWorldCarrier') and owner.isOnWingWorldCarrier():
                    owner.topLogo.hide(True)
                else:
                    owner.topLogo.hide(isHide)
            elif isHide:
                owner.topLogo.hide(False)
                owner.topLogo.hideChatMsg(True)
            else:
                owner.topLogo.hide(False)
        if getattr(owner, 'questLogo', None):
            if self.isPlayer:
                owner.questLogo.hide(isHide or not owner.showWorldGUI)
            else:
                owner.questLogo.hide(isHide)
        p = BigWorld.player()
        if isHide:
            owner.setTargetCapsUse(retainTopLogo)
            self.attachUFO(ufo.UFO_NULL)
            self.detachFootTrigger()
            if getattr(p, 'targetLocked', None) == owner:
                if hasattr(owner, 'isInCoupleRide') and owner.isInCoupleRide() or getattr(owner, 'tride', None) and owner.tride.inRide():
                    pass
                else:
                    p.unlockTarget()
        else:
            owner.setTargetCapsUse(True)
            self.setupFootTrigger()
            if getattr(p, 'targetLocked', None) and owner.id == p.targetLocked.id:
                p.updateTargetLockedUfo()
            else:
                self.attachUFO(ufo.UFO_SHADOW)
        if hasattr(owner, 'noSelected') and owner.noSelected:
            owner.setTargetCapsUse(False)
        if hasattr(owner, 'followModel') and owner.followModel:
            for fm in owner.followModel:
                fm.visible = owner.model.visible

    def getLeftWeaponModels(self):
        models = []
        owner = BigWorld.entity(self.owner)
        if not hasattr(owner.modelServer, 'leftWeaponModel'):
            return None
        weaponModel = owner.modelServer.leftWeaponModel
        if weaponModel:
            for i in weaponModel.models:
                if i[1]:
                    models.append(i[0])

        if len(models) == 0 and not hasattr(owner, 'avatarInstance'):
            models.append(owner.model)
        return models

    def getBackWearModels(self):
        models = []
        owner = BigWorld.entity(self.owner)
        if not hasattr(owner.modelServer, 'backwear'):
            return models
        backwear = owner.modelServer.backwear
        if backwear and backwear.models:
            for i in backwear.models:
                if i and len(i) > 1 and i[1]:
                    models.append(i[0])

        return models

    def getRightWeaponModels(self, weaponType = gameglobal.WEAPON_ALL):
        models = []
        owner = BigWorld.entity(self.owner)
        if not hasattr(owner.modelServer, 'rightWeaponModel'):
            return None
        weaponModel = owner.modelServer.rightWeaponModel
        if weaponModel:
            if weaponType == gameglobal.WEAPON_ALL:
                for i in weaponModel.models:
                    if i[1]:
                        models.append(i[0])

            elif weaponType == gameglobal.WEAPON_RIGHT:
                for i in weaponModel.models:
                    if i[1] and i[2].find('right') != -1:
                        models.append(i[0])

            elif weaponType == gameglobal.WEAPON_LEFT:
                for i in weaponModel.models:
                    if i[1] and i[2].find('left') != -1:
                        models.append(i[0])

        if len(models) == 0 and not hasattr(owner, 'avatarInstance'):
            models.append(owner.model)
        return models

    def getWeaponModels(self, weaponType = gameglobal.WEAPON_ALL):
        models = []
        owner = BigWorld.entity(self.owner)
        if hasattr(owner.modelServer, '_getWeaponModel'):
            weaponModel = owner.modelServer._getWeaponModel(owner.weaponState, weaponType)
            if weaponModel:
                if weaponType == gameglobal.WEAPON_ALL:
                    for i in weaponModel.models:
                        if i[1]:
                            models.append(i[0])

                elif weaponType == gameglobal.WEAPON_RIGHT:
                    for i in weaponModel.models:
                        if i[1] and i[2].find('right') != -1:
                            models.append(i[0])

                elif weaponType == gameglobal.WEAPON_LEFT:
                    for i in weaponModel.models:
                        if i[1] and i[2].find('left') != -1:
                            models.append(i[0])

        if len(models) == 0 and not hasattr(owner, 'avatarInstance'):
            models.append(owner.model)
        return models

    def getYuanLingModels(self):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld or not hasattr(owner, 'modelServer'):
            return []
        return [owner.modelServer.yuanLing.model]

    def setGuard(self, isGuard):
        owner = BigWorld.entity(self.owner)
        if self.action == None:
            return
        if hasattr(owner, 'setGuard'):
            owner.setGuard(isGuard)
            return
        if getattr(owner, 'buffCaps', None):
            owner.am.matchCaps = owner.buffCaps
            return
        if getattr(owner, 'bufActState', None) and not owner.inRiding():
            if hasattr(owner, 'runOnWater') and owner.runOnWater:
                owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_RUN_ON_WATER]
            elif hasattr(owner, '_isOnZaijuOrBianyao') and owner._isOnZaijuOrBianyao():
                zaijuCaps = self.getZaijuCaps()
                if not zaijuCaps:
                    owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_RIDE]
                elif isinstance(zaijuCaps, tuple) or isinstance(zaijuCaps, list):
                    owner.am.matchCaps = list(zaijuCaps)
                else:
                    owner.am.matchCaps = [keys.CAPS_HAND_FREE, zaijuCaps]
            else:
                temCaps = list(owner.bufActState)
                if keys.CAPS_RUN_ON_WATER in owner.bufActState and hasattr(owner, 'runOnWater') and not owner.runOnWater:
                    temCaps.remove(keys.CAPS_RUN_ON_WATER)
                    temCaps.append(keys.CAPS_GROUND)
                    owner.bufActState = temCaps
                owner.am.matchCaps = owner.bufActState
            return
        if hasattr(owner, '_isOnLoginScene') and owner._isOnLoginScene():
            return
        if hasattr(owner, '_isOnZaijuOrBianyao') and owner._isOnZaijuOrBianyao() and not self.getZaijuCaps():
            owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_RIDE]
            return
        if owner.IsMonster or owner.IsSummonedSprite or owner.IsSummonedBeast:
            if owner.isMultiPartMonster():
                return
            if not isGuard:
                if owner.isAvatarMonster():
                    newCaps = []
                    for caps in owner.am.matchCaps:
                        if utils.isSchoolAndNormalCaps(caps):
                            newCaps.append(caps)

                    if not newCaps:
                        newCaps.append(self.getWeaponActType())
                    newCaps.append(keys.CAPS_GROUND)
                    owner.am.matchCaps = newCaps
                else:
                    self.setMonsterIdleCaps(owner.am)
            elif owner.isAvatarMonster():
                self.setStateCaps([keys.CAPS_GROUND])
            else:
                self.setMonsterCombatCaps(owner.am)
            return
        if isGuard:
            if owner.canSwim():
                owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_SWIM]
                self.setStateCaps([keys.CAPS_GROUND_COMBAT, keys.CAPS_SWIM])
            elif hasattr(owner, 'runOnWater') and owner.runOnWater:
                owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_RUN_ON_WATER]
            else:
                newCaps = []
                for cap in owner.am.matchCaps:
                    if utils.isSchoolCaps(cap):
                        newCaps.append(cap)

                if not newCaps:
                    newCaps.append(self.getWeaponActType())
                if owner.canFly():
                    newCaps.append(keys.CAPS_FLY)
                else:
                    newCaps.append(keys.CAPS_GROUND)
                owner.am.matchCaps = newCaps
            if hasattr(owner, 'isInCoupleRide') and owner.isInCoupleRide():
                owner.am.matchCaps = owner.modelServer.getCoupleMatchCaps()
            if hasattr(owner, '_isOnZaijuOrBianyao') and owner._isOnZaijuOrBianyao():
                zaijuCaps = self.getZaijuCaps()
                if zaijuCaps:
                    if isinstance(zaijuCaps, tuple) or isinstance(zaijuCaps, list):
                        owner.am.matchCaps = list(zaijuCaps)
                    else:
                        owner.am.matchCaps = [keys.CAPS_HAND_FREE, zaijuCaps]
        else:
            if owner.canSwim():
                owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_SWIM]
            elif hasattr(owner, 'runOnWater') and owner.runOnWater:
                owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_RUN_ON_WATER]
            elif owner.canFly():
                weaponCaps = keys.CAPS_HAND_FREE
                for cap in owner.am.matchCaps:
                    if utils.isSchoolAndNormalCaps(cap):
                        weaponCaps = cap
                        break

                owner.am.matchCaps = [weaponCaps, keys.CAPS_FLY]
            elif hasattr(owner, 'inRidingHorse') and owner.inRidingHorse():
                self.setStateCaps([keys.CAPS_RIDE])
            else:
                self.setStateCaps([keys.CAPS_GROUND])
            if hasattr(owner, 'isInCoupleRide') and owner.isInCoupleRide():
                owner.am.matchCaps = owner.modelServer.getCoupleMatchCaps()
            if hasattr(owner, '_isOnZaijuOrBianyao') and owner._isOnZaijuOrBianyao():
                zaijuCaps = self.getZaijuCaps()
                if zaijuCaps:
                    if isinstance(zaijuCaps, tuple) or isinstance(zaijuCaps, list):
                        owner.am.matchCaps = list(zaijuCaps)
                    else:
                        owner.am.matchCaps = [keys.CAPS_HAND_FREE, zaijuCaps]

    def setDying(self, isDying):
        owner = BigWorld.entity(self.owner)
        if isDying:
            owner.am.matchCaps = [keys.CAPS_GROUND_COMBAT, keys.CAPS_DYING]
        else:
            owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND_COMBAT]

    def setMatcherCoupled(self, matcherCoupled):
        owner = BigWorld.entity(self.owner)
        if hasattr(owner, 'am'):
            owner.am.matcherCoupled = matcherCoupled

    def setHeadTracker(self, isTrack):
        if isTrack:
            if self.doingActionType() != action.INCOMBAT_START_ACTION:
                self.stopAction()
                self.setDoingActionType(action.ALERT_ACTION)
            self.setStateCaps([keys.CAPS_GROUND_COMBAT])
            self.beginHeadTracker()
        else:
            owner = BigWorld.entity(self.owner)
            if owner and not owner.inCombat and not self.hasMonsterIdleCaps():
                self.setStateCaps([keys.CAPS_GROUND])
            if self.doingActionType() == action.ALERT_ACTION:
                self.setDoingActionType(action.UNKNOWN_ACTION)
            self.stopHeadTracker()

    def hasMonsterIdleCaps(self):
        owner = BigWorld.entity(self.owner)
        if hasattr(owner, 'monsterInstance') and not owner.isAvatarMonster():
            idleCap = self.getCapsIdle()
            return isinstance(idleCap, tuple)
        return False

    def beginHeadTracker(self, showEmote = True):
        if self.fobidHeadTrack:
            return
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.firstFetchFinished or gameglobal.rds.isSinglePlayer:
            return
        if showEmote and random.randint(0, 100) < self.EMOTE_PROBABILITY:
            owner.topLogo.showBigEmote(owner.topLogo.EMOTE_M_SURPRISE)
        if self.headTracking:
            return
        self.headTracking = True
        if owner.getItemData().get('noGuardTrack', 0):
            return
        if self.trackerModel == None or self.trackerModel.tracker == None:
            self.trackerModel = owner.model
            if self.trackerModel == None:
                return
            self.trackerModel.tracker = self.tracker
        self.updateTracker()
        gamelog.debug('@PGF:fashion.beginHeadTracker 7', owner.id, self.tracker.nodeInfo)

    def stopHeadTracker(self):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if owner.topLogo != None:
            owner.topLogo.stopBigEmote()
        if not self.headTracking:
            return
        self.headTracking = False
        if self.trackerModel and self.trackerModel.tracker != None:
            self.trackerModel.tracker.directionProvider = None
            self.trackerModel.tracker.nodeInfo = None

    def updateTracker(self):
        owner = BigWorld.entity(self.owner)
        if hasattr(owner, 'lockedId'):
            target = BigWorld.entity(owner.lockedId)
        else:
            target = BigWorld.player()
        if owner == None or target == None:
            gamelog.error('@PGF:fashion.updateTrackerProvider: can not get owner or target', owner, target, owner.lockedId)
            return
        if not (self.trackerModel.node('biped Head') and self.trackerModel.node('biped Neck') and self.trackerModel.node('biped Spine1')):
            gamelog.error('bgf@Fashion:no Head or Neck or Spine1', self.trackerModel.sources, self.trackerModel.node('biped Head'), self.trackerModel.node('biped Neck'), self.trackerModel.node('biped Spine1'))
            return
        if self.nodeInfo == None:
            self.nodeInfo = BigWorld.TrackerNodeInfo(self.trackerModel, 'biped Head', [('biped Neck', -0.2), ('biped Spine1', 0.3)], 'None', -5.0, 5.0, -50.0, 50.0, 1000.0)
        if self.directionProvider == None:
            self.directionProvider = BigWorld.DiffDirProvider(owner.matrix, target.matrix)
        self.trackerModel.tracker.nodeInfo = self.nodeInfo
        self.trackerModel.tracker.directionProvider = self.directionProvider

    def setWeaponCaps(self, caps):
        owner = BigWorld.entity(self.owner)
        if not owner or not hasattr(owner, 'am') or not owner.am:
            return
        owner.am.patience = self.boredTime
        owner.am.fuse = 0
        if getattr(owner, 'bufActState', None):
            return
        oldCaps = owner.am.matchCaps
        if not oldCaps:
            oldCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND]
        newCaps = []
        for i in oldCaps:
            if not utils.isSchoolAndNormalCaps(i):
                newCaps.append(i)

        newCaps += caps
        if keys.CAPS_SWIM in newCaps:
            if getattr(owner, 'weaponState', False):
                if keys.CAPS_GROUND not in newCaps:
                    newCaps.append(keys.CAPS_GROUND)
            elif keys.CAPS_GROUND in newCaps:
                newCaps.remove(keys.CAPS_GROUND)
        owner.am.matchCaps = newCaps
        if hasattr(owner, '_isOnZaijuOrBianyao') and owner._isOnZaijuOrBianyao():
            zaijuCaps = self.getZaijuCaps()
            if not zaijuCaps:
                owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_RIDE]
            elif isinstance(zaijuCaps, tuple) or isinstance(zaijuCaps, list):
                owner.am.matchCaps = list(zaijuCaps)
            else:
                owner.am.matchCaps = [keys.CAPS_HAND_FREE, zaijuCaps]
        if self.isPlayer:
            if hasattr(owner, 'resetFootIK'):
                owner.resetFootIK()

    def setRideSpecialCaps(self):
        owner = BigWorld.entity(self.owner)
        if owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            data = FDD.data.get(self.modelID, {})
            if data.get('enableIdlePlus', None):
                if self.idleType == gametypes.IDLE_TYPE_NORMAL:
                    owner.am.matchCaps = [keys.CAPS_IDLE0, keys.CAPS_RIDE, keys.CAPS_HORSE_IDLE_2]
                elif self.idleType == gametypes.IDLE_TYPE_RUN_STOP:
                    owner.am.matchCaps = [keys.CAPS_IDLE0, keys.CAPS_RIDE]
                elif self.idleType == gametypes.IDLE_TYPE_SPRINT_STOP:
                    owner.am.matchCaps = [keys.CAPS_IDLE0, keys.CAPS_RIDE, keys.CAPS_HORSE_IDLE_3]

    def setStateCaps(self, caps):
        owner = BigWorld.entity(self.owner)
        owner.am.patience = self.boredTime
        owner.am.fuse = 0
        if getattr(owner, 'bufActState', None) and not owner.inRiding():
            return
        oldCaps = owner.am.matchCaps
        newCaps = []
        for i in oldCaps:
            if utils.isSchoolAndNormalCaps(i):
                newCaps.append(i)

        newCaps += caps
        owner.am.matchCaps = newCaps
        if hasattr(owner, 'inRiding') and owner.inRiding():
            owner.am.matchCaps = [keys.CAPS_IDLE0, keys.CAPS_RIDE]
            self.setRideSpecialCaps()
        if owner.canFly():
            owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_FLY]
        if hasattr(owner, 'isInCoupleRide') and owner.isInCoupleRide():
            owner.am.matchCaps = owner.modelServer.getCoupleMatchCaps()
        if hasattr(owner, '_isOnZaijuOrBianyao') and owner._isOnZaijuOrBianyao():
            zaijuCaps = self.getZaijuCaps()
            if not zaijuCaps:
                owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_RIDE]
            elif isinstance(zaijuCaps, tuple) or isinstance(zaijuCaps, list):
                owner.am.matchCaps = list(zaijuCaps)
            else:
                owner.am.matchCaps = [keys.CAPS_HAND_FREE, zaijuCaps]
        if self.isPlayer:
            model = owner.model
            if hasattr(model, 'footIK') and model.footIK:
                if len(caps) == 1 and caps[0] == keys.CAPS_GROUND:
                    model.footIK.enable = True
                else:
                    model.footIK.enable = False

    def getZaijuCaps(self):
        owner = BigWorld.entity(self.owner)
        return ZD.data.get(owner._getZaijuOrBianyaoNo(), {}).get('caps', None)

    def autoSetStateCaps(self):
        owner = BigWorld.entity(self.owner)
        if not (hasattr(owner, 'avatarInstance') or utils.instanceof(owner, 'InteractiveObject') or owner.IsSummonedSprite or utils.instanceof(owner, 'WingWorldCarrier')):
            return
        self.setGuard(owner.inCombat or self.getWeaponActType() != keys.CAPS_HAND_FREE)

    def getCaps(self):
        owner = BigWorld.entity(self.owner)
        return tuple(owner.am.matchCaps)

    def getWeaponMatchType(self):
        owner = BigWorld.entity(self.owner)
        if getattr(owner, 'bufActState', None):
            return self.getWeaponActType() - 1
        if keys.CAPS_WEAPON1 in owner.am.matchCaps:
            return 1
        if keys.CAPS_WEAPON2 in owner.am.matchCaps:
            return 2
        if keys.CAPS_WEAPON3 in owner.am.matchCaps:
            return 3
        if keys.CAPS_WEAPON4 in owner.am.matchCaps:
            return 4
        if keys.CAPS_WEAPON5 in owner.am.matchCaps:
            return 5
        if keys.CAPS_WEAPON6 in owner.am.matchCaps:
            return 6
        if keys.CAPS_WEAPON7 in owner.am.matchCaps:
            return 7
        if keys.CAPS_WEAPON8 in owner.am.matchCaps:
            return 8
        return 0

    def getWeaponActType(self):
        owner = BigWorld.entity(self.owner)
        if owner and owner.inWorld:
            if hasattr(owner, 'bianshen') and owner._isOnZaijuOrBianyao():
                return keys.CAPS_HAND_FREE
            if hasattr(owner.modelServer, '_getWeaponModel'):
                weaponModel = owner.modelServer._getWeaponModel(owner.weaponState)
                if weaponModel:
                    return weaponModel.equipType
        return keys.CAPS_HAND_FREE

    def attachUFO(self, ufoType):
        if gameglobal.NONEEDUFO:
            return
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if not owner.model:
            return
        if hasattr(owner, 'hidingPower') and owner.hidingPower:
            return
        ufoNode = owner.model.node('Scene Root')
        if self.ufo != None:
            if self.ufo.ufoType == ufoType:
                return
            if ufoNode and self.ufo.obj.inWorld and self.ufo.obj.attached:
                try:
                    ufoNode.detach(self.ufo.obj)
                    self.ufo.obj.scale(1.0)
                    self.ufo.obj.clear()
                except:
                    pass

            self.ufo = None
        if ufoType != ufo.UFO_NULL and self.opacity != 0:
            if ufoType == ufo.UFO_SHADOW:
                if gameglobal.NEW_UFO_RULE and not appSetting.VideoQualitySettingObj.needShadowUfo:
                    return
                if not owner.needBlackShadow():
                    return
            if ufoNode:
                self.ufo = ufo.getUFO(ufoType)
                bodySize = getattr(owner, 'bodySize', 1.0)
                if ufoType in ufo.UFO_TYPE_NOT_FX:
                    ufoSize = bodySize
                    self.ufo.obj.setSize(ufoSize)
                else:
                    ufoSize = bodySize / owner.model.scale[1]
                    if hasattr(self.ufo.obj, 'scale'):
                        self.ufo.obj.scale(ufoSize)
                    else:
                        self.ufo.obj.setSize(ufoSize)
                if not self.ufo.obj.attached:
                    if hasattr(owner.model, 'floatage'):
                        self.ufo.obj.bias = (0, -(owner.getModelHeight() + 1.0) / 2, 0)
                    else:
                        self.ufo.obj.bias = (0, 0, 0)
                    ufoNode.attach(self.ufo.obj)
                    if hasattr(self.ufo.obj, 'maxLod'):
                        self.ufo.obj.maxLod = owner.getUFOLod()
                    if hasattr(self.ufo.obj, 'force'):
                        self.ufo.obj.clear()
                        self.ufo.obj.force()

    def resetTurnBodyState(self):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if owner.am:
            if hasattr(owner, 'inMotorRunStop') and owner.inMotorRunStop() and getattr(owner, 'qinggongState', 0) not in gametypes.QINGGONG_WINGFLY_STATES:
                owner.am.turnModelToEntity = False
            else:
                owner.am.turnModelToEntity = True
            owner.am.bodyTwistSpeed = 100
            self.turnModelToEntity = owner.am.turnModelToEntity

    def setupClimbMatcher(self, owner, model, isPlayer):
        return
        cm = None
        for a in model.motors:
            if a.__name__ == 'ClimbMatcher':
                if not cm:
                    cm = a
                else:
                    model.delMotor(a)

        if not cm:
            cm = BigWorld.ClimbMatcher(owner)
            model.addMotor(cm)
            cm.setAction({'idle': '1931',
             'up': '1932',
             'down': '1933',
             'end': '1934',
             'jump': '1930'})
            if isPlayer:
                cm.materials = (140, 141, 142)
                cm.endClimbNotifier = owner.ap.endHandClimbNotifier
                cm.beginClimbNotifier = owner.ap.beginHandClimbNotifier
            else:
                cm.matchActionOnly = True
                owner.am.enable = False
        owner.cm = cm

    def disableFootIK(self, disable):
        owner = BigWorld.entity(self.owner)
        if not owner.inWorld or not owner.model:
            return
        if hasattr(owner.model, 'footIK'):
            owner.model.footIK.enable = not disable

    def setupObstacleModel(self, model):
        if model == None:
            gamelog.debug('Error load obstacle model failed ')
            return
        owner = BigWorld.entity(self.owner)
        if owner.model != None:
            oldModel = owner.model
            owner.model = model
            if hasattr(oldModel, 'noAttachFx_'):
                oldModel.motors = ()
                oldModel.noAttachFx_ = False
                if self.dummyUFO:
                    oldModel.root.detach(self.dummyUFO.obj)
                    ufo.giveBack(self.dummyUFO)
                    self.dummyUFO = None
                sfx.giveBackDummyModel(oldModel, False)
        else:
            owner.model = model
        self.modelPath = model.sources
        self.calcModelID()
        model.renderFlag = gameglobal.AMBIENT_INC

    def resetModelRoll(self):
        owner = BigWorld.entity(self.owner)
        if not owner.inWorld or not owner.model:
            return
        if not self.isPlayer:
            return
        am = owner.am
        if hasattr(am, 'applyRunRoll'):
            if BigWorld.player().enableApplyModelRoll() and owner.bianshen[0] not in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
                data = FDD.data.get(self.modelID, {})
                am.applyRunRoll = data.get('enableApplyModelRoll', False)
                am.maxModelRoll = data.get('modelRollValue', gameglobal.MAX_RUN_MODEL_ROLL)
                am.rollRunHalfLife = data.get('modelRollHalfLife', gameglobal.ROLL_RUN_HALFLIFE)
            else:
                am.applyRunRoll = False
