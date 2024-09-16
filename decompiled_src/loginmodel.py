#Embedded file name: /WORKSPACE/data/entities/client/loginmodel.o
import BigWorld
import const
import utils
import gametypes
import gameglobal
import physique
import clientcom
import formula
from appearance import Appearance
from helpers import fashion
from helpers import modelServer
from helpers import weaponModel
from helpers import vertexMorpher
from helpers import tintalt
from helpers import outlineHelper
from helpers import action
from helpers import charRes
from helpers import preload
from iClient import IClient
from callbackHelper import Functor
from sfx import keyboardEffect
from data import zaiju_data as ZD
from data import duel_config_data as DCD

class FashionEx(fashion.Fashion):

    def __init__(self, owner):
        super(FashionEx, self).__init__(owner)
        self.sfx = []

    def stopSfx(self):
        pass


class LoginModel(IClient):

    def __init__(self):
        super(LoginModel, self).__init__()
        self.roleName = ''
        self.scale = (1.0, 1.0, 1.0)
        self.csd = {}
        self.avatarConfig = None
        self.aspect = Appearance(dict())
        self.physique = physique.Physique(dict())
        self.attachWeapon = False
        self.focusSoundHandle = 0
        self.modelServer = None
        self.zjd = {}
        self.actionTimer = None
        self.isDefaultModel = 0

    @property
    def realSchool(self):
        return self.school

    @property
    def inCombat(self):
        return 0

    def needMoveNotifier(self):
        return False

    def isNewXrjmRole(self):
        if not self.csd:
            return False
        if self.csd.get('showModel', 0) and not self.applyAvatarConfig:
            return True
        return False

    def isLoginNewDefaultRole(self):
        if not self.csd:
            return False
        if self.csd.get('showModel', 0) and not self.applyAvatarConfig:
            return True
        return False

    def getItemData(self):
        if self.isLoginNewDefaultRole():
            return clientcom.getLoginModelNewPath(self.school)
        if self.inDotaBattleField():
            data = {}
            zaijuId = gameglobal.rds.ui.bfDotaChooseHeroRight.chooseHeroId
            self.zjd = ZD.data.get(zaijuId, {})
            data['scale'] = self.zjd.get('modelScale', 1.0)
            data['model'] = self.zjd['modelId']
            return data
        data = {'school': self.school,
         'multiPart': True,
         'transModelId': True,
         'bodyType': self.bodyType,
         'sex': self.gender}
        data['head'] = self.csd.get('head', 0)
        data['shoe'] = self.csd.get('shoe', 0)
        data['leg'] = self.csd.get('leg', 0)
        data['body'] = self.csd.get('body', 0)
        data['hand'] = self.csd.get('hand', 0)
        parts = utils.getFashionAspectSlots(data['body']) if data['body'] else []
        if gametypes.EQU_PART_FASHION_HEAD in parts:
            data['head'] = data['body']
        hair, avatarConfig = gameglobal.rds.loginScene.fetchAvatarConfig(self.school, self.gender, self.bodyType, 0, self.applyAvatarConfig)
        data['hair'] = hair
        data['avatarConfig'] = avatarConfig
        dyesDict = {}
        for part in charRes.PARTS_ASPECT:
            equipId = data.get(part, -1)
            if equipId == -1:
                continue
            dyesDict[part] = utils.getEquipDyeList(equipId)

        data['dyesDict'] = dyesDict
        self.avatarConfig = avatarConfig
        return data

    def inDotaBattleField(self):
        p = BigWorld.player()
        return p and formula.inDotaBattleField(getattr(p, 'mapID', 0))

    def enterWorld(self):
        self.csd = gameglobal.rds.loginScene.getCharShowData(self.school, self.gender, self.bodyType)
        self.fashion = FashionEx(self.id)
        self.fashion.loadDummyModel()
        self.filter = BigWorld.ClientFilter()
        itemDada = self.getItemData()
        if not self.inDotaBattleField():
            self.scale = (1.0, 1.0, 1.0)
        else:
            self.scale = (itemDada['scale'], itemDada['scale'], itemDada['scale'])
        p = BigWorld.player()
        path = itemDada.get('fullPath', None)
        if path and path in preload.gPreloadMap and not preload.gPreloadMap[path].attached:
            self.fashion.setupModel(preload.gPreloadMap[self.getItemData().get('fullPath')])
            self.firstFetchFinished = True
            self.afterModelFinish()
        else:
            self.modelServer = modelServer.SimpleModelServer(self, True)
        self._initUserField()
        self.equipWeapon()

    def showTargetUnitFrame(self):
        return False

    def _initUserField(self):
        if self.inDotaBattleField():
            return
        self.aspect.set(gametypes.EQU_PART_WEAPON_ZHUSHOU, self.csd.get('zhuShou', 0))
        self.aspect.set(gametypes.EQU_PART_WEAPON_FUSHOU, self.csd.get('fuShou', 0))
        self.physique.bodyType = self.bodyType
        self.physique.school = self.school
        self.physique.sex = self.gender

    def needSetStaticStates(self):
        return True

    def afterModelFinish(self):
        self.model.visible = False
        self.model.setModelNeedHide(False, 0.1)
        self.model.expandVisibilityBox(1000)
        if gameglobal.rds.loginScene.inSelectZeroStage():
            self.filter.position = self.originalPos
            self.filter.yaw = self.originalYaw
        self.model.scale = self.scale
        self.setTargetCapsUse(not self.inDotaBattleField())
        self.bodyApply()
        if self.isNewXrjmRole():
            avatarConfig = clientcom._getModelData(const.MODEL_AVATAR_BORDER + self.school)
            clientcom.setAvatarConfig(None, avatarConfig, self.model, False, True)
        BigWorld.callback(0.5, Functor(clientcom.setModelPhysics, self.model))
        try:
            self.showWeapon(self.attachWeapon)
        except:
            pass

        if self.isNewXrjmRole():
            if gameglobal.rds.loginScene.inCreateSelectNewStage():
                gameglobal.rds.loginScene.playSchoolIntroAni(self)
        BigWorld.callback(0.1, self.refreshOpacity)
        if self.visibility == gameglobal.OPACITY_FULL and (gameglobal.rds.loginScene.inSelectOneStage() or gameglobal.rds.loginScene.inSelectTwoStage()):
            self.playChooseSound()
        gameglobal.rds.loginScene.loadingDec()
        if self.isNewXrjmRole():
            if gameglobal.rds.loginScene.inSelectZeroStage():
                gameglobal.rds.loginScene.effectManager.addEffect(self)

    def fetchPlaneCallback(self, model):
        gameglobal.PLANE_MODEL = model
        self.reAttachPlane()

    def setCameraToSelf(self):
        zaijuId = gameglobal.rds.ui.bfDotaChooseHeroRight.chooseHeroId
        faceDir = DCD.data.get('bf_dota_hero_face_dir', (1, 0, 0))
        self.filter.yaw = faceDir[2]
        dis, height, offX = ZD.data.get(zaijuId, {}).get('cameraPosData', (10, 0.8, 0))
        gameglobal.rds.loginScene.setCameraToEntity(self.id, dis=dis, modelHeight=height, offX=offX)

    def reAttachPlane(self):
        if not gameglobal.PLANE_MODEL:
            return
        p = BigWorld.player()
        bfDotaChooseHeroBottom = gameglobal.rds.ui.bfDotaChooseHeroBottom
        filterChooseHeroSound = p.filterChooseHeroSound
        bornActionName = DCD.data.get('hero_born_action', '1451')
        idleActionName = DCD.data.get('hero_idle_action', '1450')
        for zaijuId, entitiy in bfDotaChooseHeroBottom.zaiju2EntityMap.iteritems():
            soundId = ZD.data.get(zaijuId, {}).get('chooseSoundId', 0)
            gameglobal.rds.sound.stopSound(soundId)
            if zaijuId == gameglobal.rds.ui.bfDotaChooseHeroRight.chooseHeroId:
                if filterChooseHeroSound:
                    p.filterChooseHeroSound = False
                else:
                    gameglobal.rds.sound.playSound(soundId)
                if gameglobal.PLANE_MODEL_PARENT_NODE and gameglobal.PLANE_MODEL in gameglobal.PLANE_MODEL_PARENT_NODE.attachments:
                    gameglobal.PLANE_MODEL_PARENT_NODE.detach(gameglobal.PLANE_MODEL)
                entitiy.model.root.attach(gameglobal.PLANE_MODEL)
                gameglobal.PLANE_MODEL_PARENT_NODE = entitiy.model.root
                entitiy.fashion.hide(False)
            else:
                entitiy.fashion.hide(True)
                entitiy.fashion._stopCueSoundAndEffect(bornActionName)
                entitiy.fashion._stopCueSoundAndEffect(idleActionName)

    def refreshOpacity(self, visibility = None):
        if visibility in (gameglobal.OPACITY_HIDE, gameglobal.OPACITY_FULL):
            self.visibility = visibility
        if getattr(self, 'firstFetchFinished', False):
            if self.visibility == gameglobal.OPACITY_HIDE and not self.inDotaBattleField():
                self.fashion.hide(True)
            elif self.inDotaBattleField():
                self.setCameraToSelf()
                bornActionName = DCD.data.get('hero_born_action', '1451')
                idleActionName = DCD.data.get('hero_idle_action', '1450')
                self.fashion.playActionSequence(self.model, [bornActionName, idleActionName], None)
                if gameglobal.PLANE_MODEL:
                    BigWorld.callback(0.1, self.reAttachPlane)
                else:
                    clientcom.fetchModel(gameglobal.DEFAULT_THREAD, self.fetchPlaneCallback, DCD.data.get('DOTA_PLANE_MODEL_ID', 50040))
            else:
                self.fashion.hide(False)
            if hasattr(self.model, 'blender'):
                if self.visibility == gameglobal.OPACITY_HIDE:
                    self.model.blender.dest(0)
                else:
                    self.model.blender.dest(255)

    def bodyApply(self):
        if self.avatarConfig:
            m = vertexMorpher.AvatarFaceMorpher(self.id)
            m.readConfig(self.avatarConfig)
            m.apply()

    def showModel(self):
        self.model.visible = True

    def leaveWorld(self):
        super(LoginModel, self).leaveWorld()
        self.avatarConfig = None
        if self.modelServer:
            if hasattr(self.modelServer, 'leftWeaponModel'):
                self.modelServer.leftWeaponModel.release()
                self.modelServer.leftWeaponModel = None
            if hasattr(self.modelServer, 'rightWeaponModel'):
                self.modelServer.rightWeaponModel.release()
                self.modelServer.rightWeaponModel = None
            self.modelServer.release()
            self.modelServer = None

    def targetFocus(self, entity):
        gameglobal.rds.loginScene.chooseModel = self
        if gameglobal.rds.loginScene.inSelectZeroStage():
            outlineHelper.setTarget(self)
            self.setTaTint(True)
            focusSound = self.csd.get('focusSound', 986)
            self.focusSoundHandle = gameglobal.rds.sound.playSound(focusSound)
            if self.isNewXrjmRole():
                self.tryAction(gameglobal.STAGE_ZERA_FOCUS_ACTION)
                gameglobal.rds.loginScene.effectManager.focusEffect(entity, True)
        keyboardEffect.addSelectCharKBE(self.school)

    def targetBlur(self, entity):
        gameglobal.rds.loginScene.chooseModel = None
        if gameglobal.rds.loginScene.inSelectZeroStage():
            self.setTaTint(False)
        outlineHelper.setTarget(None)
        focusSound = self.csd.get('focusSound', 986)
        gameglobal.rds.sound.stopSound(focusSound, self.focusSoundHandle)
        self.focusSoundHandle = 0
        if self.isNewXrjmRole() and gameglobal.rds.loginScene.inSelectZeroStage():
            try:
                self.model.action(gameglobal.STAGE_ZERA_FOCUS_ACTION).stop()
                self.model.action(gameglobal.STAGE_ZERO_SHOW_ACTION)()
            except:
                pass

            gameglobal.rds.loginScene.effectManager.focusEffect(entity, False)

    def canOutline(self):
        return not self.inDotaBattleField()

    def use(self):
        super(LoginModel, self).use()

    def equipWeapon(self):
        if self.isNewXrjmRole() or self.isLoginNewDefaultRole():
            return
        self.threadID = gameglobal.getLoadThread()
        self.modelServer.leftWeaponModel = weaponModel.WeaponModel(self.id, self.threadID)
        self.modelServer.rightWeaponModel = weaponModel.WeaponModel(self.id, self.threadID)
        self.modelServer.rightWeaponModel.equipItem(self.aspect.rightWeapon)
        self.modelServer.leftWeaponModel.equipItem(self.aspect.leftWeapon)

    def refreshWeaponState(self, attach = True):
        if self.isNewXrjmRole():
            return
        if attach:
            if self.realSchool in (const.SCHOOL_GUANGREN, const.SCHOOL_YANTIAN):
                self.modelServer.leftWeaponModel.hangUp(self.model, False)
                self.modelServer.rightWeaponModel.attach(self.model, False, True)
            else:
                self.modelServer.leftWeaponModel.attach(self.model, False)
                self.modelServer.rightWeaponModel.attach(self.model, False)
        else:
            self.modelServer.leftWeaponModel.hangUp(self.model, False)
            self.modelServer.rightWeaponModel.hangUp(self.model, False)

    def afterWeaponUpdate(self, weapon):
        if weapon.models:
            weaponModel = [ item[0] for item in weapon.models ]

    def afterWearUpdate(self, wear):
        pass

    def playShowAction(self):
        showActions = self.csd.get('showActions', None)
        if showActions:
            showActions = list(showActions)
            for i, act in enumerate(showActions):
                if len(act) == 1:
                    showActions[i] = (act[0], tuple())
                showActions[i] += (action.UNKNOWN_ACTION,
                 1,
                 1.0,
                 None)

            self.fashion.playActionWithFx(showActions, 0)

    def showWeapon(self, attach = True):
        if self.isNewXrjmRole() or self.inDotaBattleField():
            return
        if getattr(self, 'firstFetchFinished', False):
            self.refreshWeaponState(attach)
            showAction = self.csd.get('showActions', '')
            if self.model:
                if attach:
                    self.tryAction(showAction)
                else:
                    self.tryStopAction(showAction)
        else:
            self.attachWeapon = attach

    def playChooseSound(self):
        soundIdx = self.csd.get('chooseSound', 0)
        gameglobal.rds.sound.playSound(soundIdx)

    def tryAction(self, act):
        try:
            self.model.action(act)()
        except:
            pass

    def tryStopAction(self, act):
        try:
            self.model.action(act).stop()
        except:
            pass

    def setTaTint(self, isLight):
        tint = 'default' if isLight else 't1'
        tintalt.ta_set_static(self.allModels, tint)
