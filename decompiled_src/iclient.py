#Embedded file name: /WORKSPACE/data/entities/client/iclient.o
import math
import Math
import BigWorld
import const
import gameglobal
import gametypes
import utils
import clientcom
import formula
import keys
from callbackHelper import Functor
from guis import topLogo
from helpers import tintalt
from helpers import fashion
from helpers import ufo
from sfx import sfx
from sfx import screenEffect
from helpers import action
from data import empty_zaiju_data as EZD
from data import monster_model_client_data as MMCD
from data import npc_model_client_data as NMCD
from data import item_data as ID
from data import transport_data as TD
from data import dialogs_data as DD
from data import jiguan_client_data as JCD
from data import obstacle_data as OCD
from data import treasure_box_data as TBD
from data import effect_lv_data as ELD
from data import life_skill_collection_data as LSCD
from data import foot_dust_data as FDD
from data import carrousel_data as CD
from data import interactive_data as ITAD
from data import relive_board_data as RBD
from data import zaiju_data as ZJD
import gamelog

class IClient(BigWorld.Entity):

    @classmethod
    def classname(cls):
        return cls.__name__

    IsCombatUnit = False
    IsNaiveCombatUnit = False
    IsMonster = False
    IsAvatar = False
    IsCreation = False
    IsSummonedBeast = False
    IsObstacle = False
    IsFragileObject = False
    IsPot = False
    IsVirtualCalcUnit = False
    IsClanWarUnit = False
    IsPuppet = False
    IsVirtualMonster = False
    IsAvatarRobot = False
    IsBox = False
    IsSummonedSprite = False
    IsIsolatedCreation = False
    IsThrownCreation = False
    IsSummoned = False
    IsWingCityWarBuilding = False
    IsWingWorldCarrier = False
    IsMonsterCreation = False
    IsBattleFieldCqzzFlag = False
    IsAvatarOrPuppet = False

    @property
    def tCamp(self):
        if hasattr(self, 'tempCamp'):
            return self.tempCamp
        return 0

    def __init__(self):
        super(IClient, self).__init__()
        self.topLogo = utils.MyNone
        self.allModels = []
        self.fashion = None
        self.beHide = False
        self.attachFx = {}
        self.addRanged = False
        self.topLogoOffset = 0.0
        self.isMoving = False
        self.isVerticalMoving = False
        self.skillRanges = {}
        self.tintStateType = [0, None]
        self.tintDelCallBack = None
        self.isInHover = False
        self.tintIdMapTintName = {}
        self.isRealModel = True
        self.followModel = []
        self.extraObstacleModel = None
        self.tintAvatarTas = {}
        self.tintAvatarName = {}
        self.zoomInHandler = None
        self.attachedDataEffects = []
        self.cloneHPs = []
        self.entityMoveQueue = []
        self.entityLantecyLimit = 2
        self.entityMoveCalTime = 5

    def stopAttachedDataEffects(self):
        if self.attachedDataEffects:
            for ef in self.attachedDataEffects:
                if ef:
                    ef.stop()

            self.attachedDataEffects = []

    def needMoveNotifier(self):
        return False

    def canSwim(self):
        return False

    def canFly(self):
        return False

    def inFlyTypeWing(self):
        return False

    def inFlyTypeFlyRide(self):
        return False

    def inFlyTypeFlyZaiju(self):
        return False

    def inRiding(self):
        return False

    def checkNeiYiBuff(self):
        return False

    def getBodySize(self):
        return gametypes.DEFAULT_BODY_SIZE

    def prerequisites(self):
        return []

    def setRenderFlag(self, flag):
        model = self.model
        if model == None or self.fashion == None:
            return
        model.renderFlag = flag

    def autoSetRenderFlag(self):
        flag = gameglobal.AMBIENT_INC
        p = BigWorld.player()
        if not clientcom.getPlayerAvatar():
            return
        if self == p.target or self == p.targetLocked:
            flag = gameglobal.AMBIENT_MAX
        if self == p.targetLocked:
            p.setTargetUfo(self, ufo.UFO_NORMAL)
        self.setRenderFlag(flag)

    def getTopLogoHeight(self):
        if not hasattr(self.model, 'bonesBoundingBoxSize'):
            height = self.model.height
        elif self.model.bonesBoundingBoxSize[1] <= 0:
            height = self.model.height
        else:
            height = self.model.bonesBoundingBoxSize[1]
        if utils.instanceof(self, 'DroppedItem'):
            data = ID.data.get(self.itemId, {})
            if data != None:
                self.topLogoOffset = data.get('heightOffset', 0.2)
            else:
                raise Exception('item data is not found' + str(self.itemId))
        elif hasattr(self, 'charType'):
            if utils.instanceof(self, 'Transport'):
                data = TD.data.get(self.charType, {})
            else:
                data = MMCD.data.get(self.charType, {})
            if data != None:
                self.topLogoOffset = data.get('heightOffset', 0.2)
        elif hasattr(self, 'npcId'):
            data = NMCD.data.get(self.npcId, {})
            if data != None:
                self.topLogoOffset = data.get('heightOffset', 0.2)
            else:
                raise Exception('npc is not found' + str(self.npcId))
        elif utils.instanceof(self, 'JiGuan'):
            self.topLogoOffset = JCD.data.get(self.jiguanId, {}).get('logoOffset', 0.0)
        elif utils.instanceof(self, 'Obstacle'):
            self.topLogoOffset = OCD.data.get(self.oid, {}).get('logoOffset', 0.0)
        elif utils.instanceofTypes(self, ('TreasureBox', 'MultiPlayerTreasureBox', 'BattleFieldPUBGTreasureBox')):
            self.topLogoOffset = TBD.data.get(self.treasureBoxId, {}).get('topLogoHeight', 0.0)
        elif utils.instanceof(self, 'LifeCsmItem'):
            self.topLogoOffset = LSCD.data.get(self._getItemId(), {}).get('logoOffset', 0.0)
        elif utils.instanceof(self, 'Carrousel'):
            self.topLogoOffset = CD.data.get(self.carrouselId, {}).get('heightOffset', 0.0)
        elif utils.instanceof(self, 'EmptyZaiju'):
            self.topLogoOffset = EZD.data.get(self.zaijuNo, {}).get('heightOffset', 0.0)
        elif utils.instanceof(self, 'InteractiveObject'):
            self.topLogoOffset = ITAD.data.get(self.objectId, {}).get('heightOffset', 0.0)
        elif utils.instanceof(self, 'Firework'):
            self.topLogoOffset = -99
        elif utils.instanceof(self, 'ReliveBoard'):
            self.topLogoOffset = RBD.data.get(self.rbType).get('heightOffset', 1.0)
        if getattr(self.model, 'floatage', False):
            self.topLogoOffset = self.topLogoOffset + self.model.floatage.floatHeight
        if self.topLogoOffset < 0 and gameglobal.rds.showDebugTopLogo:
            self.topLogoOffset = 1
        return height * self.model.scale[1] + self.topLogoOffset

    def canSelected(self):
        return self.targetCaps

    def canOutline(self):
        return True

    def canChangeDiffuseInFocus(self):
        return True

    def canChangeTgtCursorInFocus(self):
        return True

    def enterWorld(self):
        self.fashion = fashion.Fashion(self.id)
        self.initYaw = self.yaw
        self.setEntityFilter()
        model = sfx.getDummyModel(False)
        self.fashion.setupModel(model)

    def setEntityFilter(self):
        self.filter = BigWorld.AvatarDropFilter()

    def leaveWorld(self):
        self.isMoving = False
        if self.fashion != None:
            self.fashion.attachUFO(ufo.UFO_NULL)
            self.fashion.release()
            self.fashion = None
        if self.topLogo != None:
            self.topLogo.release()
            self.topLogo = utils.MyNone
        tintalt.ta_reset(self.allModels)
        self.removeAllFx()
        self.allModels = []
        self.tintStateType = [0, None]
        if self.tintDelCallBack:
            BigWorld.cancelCallback(self.tintDelCallBack)
            self.tintDelCallBack = None
        self.tintIdMapTintName = {}
        self.tintAvatarTas = {}
        self.tintAvatarName = {}
        self.followModel = []
        if self.extraObstacleModel:
            try:
                self.delModel(self.extraObstacleModel)
            except:
                pass

            self.extraObstacleModel = None

    def hide(self, bHide, retainTopLogo = False):
        self.beHide = bHide
        if getattr(self, 'fashion', None):
            self.fashion.hide(bHide, retainTopLogo)

    def getTopLogoFadeStart(self):
        return gameglobal.guiFadeStart * 0.9

    def enterTopLogoRange(self, rangeDist = -1):
        if self.topLogo == None:
            h = self.getTopLogoHeight()
            if h > 0:
                enableNotCreateTopLogoForHide = gameglobal.rds.configData.get('enableNotCreateTopLogoForHide', False)
                if hasattr(self, 'getOpacityValue') and enableNotCreateTopLogoForHide:
                    opacityValue = self.getOpacityValue()
                    if opacityValue[0] in gameglobal.OPACITY_HIDE_TOPLOGO and not opacityValue[1] and not BigWorld.player().isInBfDota():
                        return
                self.topLogo = topLogo.TopLogo(self.id)
        if self.topLogo != None and self.beHide:
            self.topLogo.hide(True)

    def leaveTopLogoRange(self, rangeDist = -1):
        if BigWorld.player().targetLocked == self:
            BigWorld.player().unlockTarget()
        if hasattr(self, 'topLogo') and self.topLogo != None:
            self.topLogo.release()
            self.topLogo = utils.MyNone
        if hasattr(self, 'questLogo') and self.questLogo:
            self.questLogo.release()
            self.questLogo = None

    def enterInteractiveRange(self, rangeDist = -1):
        pass

    def leaveInteractiveRange(self, rangeDist = -1):
        pass

    def enterLoadModelRange(self, rangeDist = -1):
        pass

    def leaveLoadModelRange(self, rangeDist = -1):
        pass

    def use(self):
        gameglobal.rds.ui.registerClear(self)

    def getEffectHeadFashion(self):
        return None

    def getEffectBodyFashion(self):
        return None

    def getEffectStateModel(self):
        return None

    def isShowFashion(self):
        return False

    def isShowFashionWeapon(self):
        return False

    def isShowClanWar(self):
        return False

    def isHideFashionHead(self):
        return False

    def loadImmediately(self):
        return False

    def getFadeDistance(self):
        return gameglobal.globalModelFadeDist

    def getModelScale(self):
        scale = gameglobal.globalModelScale
        return (scale, scale, scale)

    def resetTopLogo(self):
        if not self.inWorld or not self.model or not self.topLogo:
            return
        h = self.getTopLogoHeight()
        if h < 0:
            if self.topLogo:
                self.topLogo.release()
                self.topLogo = utils.MyNone
        elif self.topLogo:
            self.topLogo.setHeight(h)
            self.topLogo.bindVisible()

    def createExtraObstacleModel(self):
        if not hasattr(self, 'getItemData'):
            return
        modelId = self.getItemData().get('extraObstacleModel')
        if modelId:
            modelName = 'char/%d/%d.model' % (modelId, modelId)
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((1, 1, 1))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadExtraObstacleModel)

    def _onLoadExtraObstacleModel(self, model):
        if not self.inWorld:
            return
        if not model:
            return
        model.setCollide(True)
        model.setPicker(True)
        self.extraObstacleModel = model
        self.addModel(model)

    def afterModelFinish(self):
        if not self.inWorld or gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            return
        if not self.topLogo:
            self.enterTopLogoRange()
        elif hasattr(self, 'isInCoupleRideAsRider') and self.isInCoupleRideAsRider():
            BigWorld.callback(0.1, self.resetTopLogo)
        else:
            self.resetTopLogo()
        if gameglobal.gHideTopLogo and getattr(self, 'topLogo', None) and not self.beHide:
            self.topLogo.hide(True)

    def getFx(self, effectId):
        return self.attachFx.get(effectId, None)

    def addFx(self, effectId, fx):
        if fx:
            self.attachFx[effectId] = fx

    def removeFx(self, effectId):
        if self.attachFx.has_key(effectId):
            sfx.detachEffect(self.model, effectId, self.attachFx[effectId])
            del self.attachFx[effectId]

    def removeAllFx(self):
        if not self.inWorld:
            return
        for effectId in self.attachFx.keys():
            self.removeFx(effectId)

        self.attachFx = {}

    def leaveDlgRange(self, unUsedDist):
        pass

    def getTgtAngle(self, tgt):
        if tgt == None:
            return 0.0
        tPos = tgt.position - self.position
        deltaYaw = self.yaw - tPos.yaw
        angle = deltaYaw * 180 / math.pi
        if angle > 180:
            angle = angle - 360
        if angle < -180:
            angle = angle + 360
        return angle

    def refreshRealModelState(self):
        p = BigWorld.player()
        if self.isRealModel:
            return
        if not getattr(self.model, 'visible', True):
            return
        if not getattr(self.model, 'dummyModel', True):
            return
        spell = self.fashion and self.fashion.doingActionType() == action.PROGRESS_SPELL_ACTION
        if p.isInMyTeam(self) or p.isEnemy(self) or p.targetLocked and p.targetLocked.id == self.id or self.IsMonster or spell:
            self.reloadModel()

    def checkCollideWithPlayer(self):
        player = BigWorld.player()
        model = self.model
        if not model or not self.inWorld or player.isAscending or not player.ap:
            return
        if clientcom.isIntersectWithPlayer(model):
            beginPos = Math.Vector3(player.position.x, model.pickbdbox[1][1] + 1.0, player.position.z)
            diffHeight = model.pickbdbox[1][1] - player.position.y + 2
            result = BigWorld.findRectDropPoint(player.spaceID, beginPos, 0.8, 0.8, diffHeight)
            if result != None and result[0][1] > player.position[1]:
                player.ap.beginForceMove(result[0])

    def inMoving(self):
        return self.isMoving

    def needBlackShadow(self):
        return True

    def getEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            return getattr(BigWorld.player(), 'monsterEffectLv', gameglobal.EFFECT_MID)
        else:
            return gameglobal.EFFECT_MID

    def getClanWarEffectLv(self, lv):
        if BigWorld.getFps() < gameglobal.LIMIT_EFFECTLV_FPS:
            if lv >= 1:
                return lv - 1
            else:
                return lv
        else:
            return lv

    def getSkillEffectLv(self):
        effectLv = self.getEffectLv()
        return ELD.data.get('monster', {}).get('content', {}).get(effectLv)[0]

    def getBeHitEffectLv(self):
        effectLv = self.getEffectLv()
        return ELD.data.get('monster', {}).get('content', {}).get(effectLv)[1]

    def getBuffEffectLv(self):
        effectLv = self.getEffectLv()
        return ELD.data.get('monster', {}).get('content', {}).get(effectLv)[2]

    def getEquipEffectLv(self):
        effectLv = self.getEffectLv()
        return ELD.data.get('monster', {}).get('content', {}).get(effectLv)[3]

    def getBasicEffectLv(self):
        effectLv = self.getEffectLv()
        return ELD.data.get('monster', {}).get('content', {}).get(effectLv)[4]

    def getSkillEffectPriority(self):
        return gameglobal.EFF_MONSTER_SKILL_PRIORITY

    def getBeHitEffectPriority(self, host):
        return gameglobal.EFF_MONSTER_BEHIT_PRIORITY

    def getBuffEffectPriority(self, host):
        return gameglobal.EFF_MONSTER_BUFF_PRIORITY

    def getEquipEffectPriority(self):
        return gameglobal.EFF_MONSTER_EQUIP_PRIORITY

    def getBasicEffectPriority(self):
        return gameglobal.EFF_MONSTER_BASIC_PRIORITY

    def chatToView(self, msgId, duration = const.POPUP_MSG_SHOW_DURATION):
        if hasattr(self, 'getOpacityValue') and self.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        dd = DD.data.get(msgId, {})
        msg = dd.get('details')
        duration = dd.get('interval', duration)
        soundId = dd.get('soundId', 0)
        if soundId:
            gameglobal.rds.sound.playSound(soundId, self)
        if msg:
            BigWorld.player().chatToNPC(self.roleName, msg, self.id, duration)

    def onTargetCursor(self, enter):
        pass

    def isAvatarMonster(self):
        return False

    def inBoothing(self):
        return False

    def inFishing(self):
        return False

    def inFishingReady(self):
        return False

    def inFishingHold(self):
        return False

    def inDaZuo(self):
        return False

    def showTargetUnitFrame(self):
        return True

    def getProxy(self):
        p = BigWorld.player()
        if p:
            return p.buildingProxy.proxies.get(self.id, None)

    def getRTViceData(self):
        fddData = None
        if hasattr(self, 'isRidingTogetherAsVice') and self.isRidingTogetherAsVice():
            if hasattr(self, 'tride'):
                header = self.tride.getHeader()
                if header:
                    modelID = getattr(header.fashion, 'modelID', 0)
                    fddData = FDD.data.get(modelID, {})
        return fddData

    def getModelHeight(self):
        viceData = self.getRTViceData()
        if not self.model or getattr(self.model, 'dummyModel', False) and not viceData:
            return 2.0
        fddData = FDD.data.get(self.fashion.modelID, {})
        if viceData:
            fddData = viceData
        modelHeight = fddData.get('modelHeight', None)
        if modelHeight:
            return modelHeight * self.model.scale[1]
        if self.model.bonesBoundingBoxSize[1] <= 0:
            height = self.model.height
        else:
            height = self.model.bonesBoundingBoxSize[1]
        return height * self.model.scale[1]

    def needAttachUFO(self):
        return True

    def isUrgentLoad(self):
        return False

    def entitiesInRange(self, rangeLength, eType = None, centerPose = None):
        returnList = []
        entities = BigWorld.entities.values()
        if entities:
            for e in entities:
                if eType and e.__class__.__name__ != eType:
                    continue
                if e and e.position.flatDistTo(self.position) <= rangeLength:
                    returnList.append(e)

        return returnList

    def entitiesInRangeCube(self, width, length, arg3, arg4, centerPos, vec):
        rangeLength = math.sqrt(width * width + length * length)
        return self.entitiesInRange(rangeLength)

    def entitiesInRangeFOV(self, radii, radian, arg3, centerPos, vec):
        return self.entitiesInRange(radii)

    def getMaxTgtBodySize(self):
        return const.DEFAULT_AVATAR_BODY_SIZE

    def isCUAlive(self, target):
        return getattr(target, 'life', gametypes.LIFE_DEAD) == gametypes.LIFE_ALIVE

    def updateModelFreeze(self, freezeTime, freezeType = None):
        if self.model and self.model.inWorld:
            self.model.freezeTime = freezeTime
            if freezeType:
                self.model.freezeType = freezeType
        if getattr(self, 'inFly', 0) == gametypes.IN_FLY_TYPE_WING and hasattr(self.modelServer, 'wingFlyModel'):
            wingModel = getattr(self.modelServer.wingFlyModel, 'model', None)
            if wingModel:
                wingModel.freezeTime = freezeTime
                if freezeType:
                    wingModel.freezeType = freezeType
        if hasattr(self.modelServer, 'rideModel'):
            rideModel = self.modelServer.rideModel
            if rideModel:
                rideModel.freezeTime = freezeTime
                if freezeType:
                    rideModel.freezeType = freezeType

    def inFuben(self, fbNo_ = 0):
        if not hasattr(self, 'spaceNo'):
            return False
        if self.spaceNo <= 0:
            gamelog.error('@PGF:spaceNo Error', self.spaceNo, self.position, self)
            return False
        if formula.spaceInWorld(self.spaceNo) or formula.spaceInMultiLine(self.spaceNo):
            return False
        fbNo = formula.getFubenNo(self.spaceNo)
        if fbNo_ and fbNo_ != fbNo:
            return False
        return True

    def inDuelZone(self, checkFbNo = 0):
        fbNo = formula.getFubenNo(self.spaceNo)
        if checkFbNo and checkFbNo != fbNo:
            return False
        return formula.inDuelZone(fbNo)

    def inPubgZone(self, checkFbNo = 0):
        fbNo = formula.getFubenNo(self.spaceNo)
        if checkFbNo and checkFbNo != fbNo:
            return False
        return formula.inPUBG(fbNo)

    def inMLSpace(self, mlgNo_ = 0):
        if not hasattr(self, 'spaceNo'):
            return False
        if not formula.spaceInMultiLine(self.spaceNo):
            return False
        if mlgNo_ and formula.getMLGNo(self.spaceNo) != mlgNo_:
            return False
        return True

    def playCameraPush(self, effectData):
        if not gameglobal.ENABLE_ANIMATE_CAMERA:
            return
        params = effectData.get('cameraPush', None)
        if params and gameglobal.ENABLE_ANIMATE_CAMERA:
            screenEffect.playCameraPush(params)

    def playZoomIn(self, effectData):
        if not self.inWorld:
            return
        enableCameraZoomIn = gameglobal.rds.configData.get('enableCameraZoomIn', False)
        if not enableCameraZoomIn:
            return
        resetZoomIn = effectData.get('resetZoomIn', None)
        if resetZoomIn:
            if self.zoomInHandler:
                BigWorld.cancelCallback(self.zoomInHandler)
            gameglobal.rds.cam.restoreCameraFov(resetZoomIn)
            return
        params = effectData.get('cameraZoomIn', None)
        if not params:
            return
        interpolation = params[0]
        changeTime = params[1]
        holdTime = params[2]
        recoveryRate = params[2]
        fov = gameglobal.rds.cam.getAdaptiveFov()
        rampFov = fov + interpolation
        if rampFov <= 0 or rampFov >= math.pi:
            return
        BigWorld.projection().rampFov(rampFov, changeTime)
        defaultFov = gameglobal.rds.cam.getDefaultFov()
        recoveryTime = abs(defaultFov - rampFov) / recoveryRate
        if self.zoomInHandler:
            BigWorld.cancelCallback(self.zoomInHandler)
        self.zoomInHandler = BigWorld.callback(changeTime + holdTime, Functor(gameglobal.rds.cam.restoreCameraFov, recoveryTime))

    def playMotionBlur(self, effectData):
        params = effectData.get('screenBlur', None)
        if params and gameglobal.ENABLE_MOTION_BLUR:
            BigWorld.motionBlurFilter(None, 0, float(params[0]), float(params[1]))

    def playSpecialShakeCamera(self, effectData):
        params = effectData.get('shakeCamera', None)
        if params:
            try:
                duration1 = float(params[0])
                duration2 = float(params[1])
                threshold = float(params[2])
                rotationAmp = float(params[3])
                strength = gameglobal.SHAKE_CAMERA_STRENGTH
                amp = tuple([ i * strength / 10.0 for i in params[4] ])
                frequency = float(params[5])
                controlPts = params[6]
                screenEffect.newSway(duration1, duration2, threshold, rotationAmp, amp, frequency, controlPts, BigWorld.player(), gameglobal.SWAY_PRIORITY_HIGH)
            except:
                pass

    def setExtraDirection(self):
        try:
            data = self.getItemData()
            extraDir = data.get('extraDir', None)
            if extraDir:
                extraRoll = extraDir[0]
                extraPitch = extraDir[1]
                extraYaw = extraDir[2]
                self.filter.setRoll(extraRoll)
                self.filter.setPitch(extraPitch)
                self.filter.setYaw(extraYaw)
        except:
            pass

    def isSceneObj(self):
        return False

    def needSetStaticStates(self):
        return False

    def doEmotion(self, emotion):
        if not self.topLogo:
            return
        self.topLogo.stopBigEmote()
        self.topLogo.showBigEmote(emotion)

    def getUFOLod(self):
        return gameglobal.UFO_DIST

    def setTargetCapsUse(self, canUse):
        if canUse:
            if hasattr(self, 'getOpacityValue'):
                opacityValue = self.getOpacityValue()
                if opacityValue[0] != gameglobal.OPACITY_HIDE:
                    self.targetCaps = [keys.CAP_CAN_USE]
                elif getattr(self, 'hidingPower', None):
                    self.targetCaps = [keys.CAP_CAN_USE]
                else:
                    self.targetCaps = []
            else:
                self.targetCaps = [keys.CAP_CAN_USE]
        else:
            self.targetCaps = []

    def refreshOpacityState(self):
        if not self.inWorld:
            return
        if gameglobal.HIDE_ALL_MODELS:
            self.hide(True)
            return
        if hasattr(self, 'getOpacityValue'):
            opValue = self.getOpacityValue()
            if opValue[0] == gameglobal.OPACITY_HIDE:
                self.hide(True)
            elif opValue[0] == gameglobal.OPACITY_HIDE_WITHOUT_NAME:
                self.hide(True)
            elif opValue[0] == gameglobal.OPACITY_TRANS:
                self.hide(False)
            elif opValue[0] == gameglobal.OPACITY_HIDE_INCLUDE_ATTACK:
                self.hide(True)
            else:
                self.hide(False)

    def getCombatSpeedIncreseRatio(self):
        r0, r1 = getattr(self, 'combatSpeedIncreseRatio', (0.0, 0.0))
        if not self.IsSummonedSprite:
            if r1 >= 1:
                return 1.0
            return 1.0 / (1 - r1)
        else:
            return 1.0 + r0

    def fadeToReal(self, fadeTime):
        if not self.model:
            return
        if not hasattr(self.model, 'fadeShader') or not self.model.fadeShader:
            fadeShader = BigWorld.BlendFashion()
            self.model.fadeShader = fadeShader
        self.model.fadeShader.current(0)
        self.model.fadeShader.changeTime(fadeTime)
        self.model.fadeShader.dest(255)
        if self.modelServer:
            self.modelServer.fadeToReal(fadeTime)

    def realToFade(self, fadeTime):
        if not self.model:
            return
        if not hasattr(self.model, 'fadeShader') or not self.model.fadeShader:
            fadeShader = BigWorld.BlendFashion()
            self.model.fadeShader = fadeShader
        self.model.fadeShader.current(255)
        self.model.fadeShader.changeTime(fadeTime)
        self.model.fadeShader.dest(0)
        if self.modelServer:
            self.modelServer.fadeToReal(fadeTime)

    def clearFade(self):
        if not self.model:
            return
        if hasattr(self.model, 'fadeShader') and self.model.fadeShader:
            self.model.fadeShader.current(128)
            self.model.fadeShader.changeTime(0.1)
            self.model.fadeShader.dest(255)

    def clearFreezeEffect(self):
        pass

    def getMatchScale(self, modelScale):
        scale = 1
        if self.__class__.__name__ in ('Avatar', 'PlayerAvatar', 'Puppet'):
            if self.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
                scale = ZJD.data.get(self.bianshen[1]).get('modelScale', 1)
        else:
            scale = modelScale
        return scale

    def notifyEntityMove(self, value):
        time = BigWorld.time()
        self.entityMoveQueue.append(time)
        for i, timeStamp in enumerate(self.entityMoveQueue):
            if time - timeStamp <= self.entityMoveCalTime:
                self.entityMoveQueue = self.entityMoveQueue[i:]
                break

        if len(self.entityMoveQueue) > 1:
            if time - self.entityMoveQueue[-2] > self.entityLantecyLimit:
                if self.topLogo:
                    self.topLogo.name = '%s:%d:%.1f' % (self.roleName, self.id, time - self.entityMoveQueue[-2])
                    self.topLogo.setLogoColor('#FF0000')
            else:
                lantecy = (self.entityMoveQueue[-1] - self.entityMoveQueue[0]) / (len(self.entityMoveQueue) - 1)
                if self.topLogo:
                    if lantecy >= self.entityLantecyLimit:
                        color = '#a00000'
                    else:
                        color = int(80 * lantecy)
                        color = '#%x0000' % color
                    self.topLogo.name = '%s:%d' % (self.roleName, self.id)
                    self.topLogo.setLogoColor(color)
