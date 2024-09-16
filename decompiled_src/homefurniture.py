#Embedded file name: /WORKSPACE/data/entities/client/homefurniture.o
import BigWorld
import Math
import clientcom
import const
import copy
import gamelog
import gameglobal
import utils
from appearance import Appearance
from equipment import Equipment
from helpers import strmap
from item import Item
from guis import uiConst
from guis import ui
from guis import cursor
from guis import uiUtils
from iClient import IClient
from helpers import modelServer
from helpers import editorHelper
from physique import Physique
from sfx import sfx
from sMath import inRange3D
from helpers.dyeMorpher import FurnitureDyeMorpher
from data import item_furniture_data as IFD
from data import interactive_data as IAD
from cdata import furniture_model_index_data as FIMD
from cdata import furniture_func_data as FFD
from cdata import game_msg_def_data as GMDD
MODEL_TYPE_TEMPLATE = 1

class HomeFurniture(IClient):

    def __init__(self):
        super(HomeFurniture, self).__init__()
        self.itemData = None
        self.showName = self.getItemData().get('name', '')
        self.roleName = self.showName
        self.obstacleModel = None
        self.equips = Equipment()
        self.modelServer = None
        self.trapId = None
        self.inFly = 0
        self.bianshen = (0, 0)
        self.fState = False
        self.dynamicObstacle = False
        self.actionId = 0
        self.mhp = 10000
        self.hp = 10000
        self.mp = 10000
        self.mmp = 10000
        self.lastFUseTime = 0

    @staticmethod
    def getModelPath(itemId):
        data = IFD.data.get(itemId, {})
        model = data.get('model', 0)
        if model in FIMD.data:
            path = FIMD.data.get(model, {}).get('modelPath', '')
            return {'fullPath': path}
        return {'model': model}

    def getItemData(self):
        if self.itemData:
            return self.itemData
        data = dict(IFD.data.get(self.furnitureId, {}))
        model = data.get('model', 0)
        if model in FIMD.data:
            data['fullPath'] = FIMD.data.get(model, {}).get('modelPath', '')
            data.pop('model', None)
        self.itemData = data
        return data

    def getName(self):
        return self.itemData.get('name', '')

    def needBlackShadow(self):
        return False

    def weaponInHandState(self):
        return 0

    def getWeapon(self, isLeft):
        if isLeft:
            return self.realAspect.leftFashionWeapon
        return self.realAspect.rightFashionWeapon

    def getWeaponEnhLv(self, isLeft):
        if isLeft:
            return self.realAspect.leftFashionWeaponEnhLv()
        return self.realAspect.rightFashionWeaponEnhLv()

    def afterModelFinish(self):
        super(HomeFurniture, self).afterModelFinish()
        self.filter = BigWorld.ClientFilter()
        if gameglobal.rds.configData.get('enableFurnitureRotatePitch', False) and hasattr(self.filter, 'enableRotatePitch'):
            self.filter.enableRotatePitch = True
        if not self.isAvatarFurniture():
            self.createObstacleModel()
        self.refreshOpacityState()
        self.refreshTargetCaps()
        self.model.setModelNeedHide(0, 0.1)
        effects = self.getItemData().get('effects', [])
        for eff in effects:
            fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             eff,
             sfx.EFFECT_UNLIMIT))
            if fxs:
                self.addFx(eff, fxs)

        showAction = self.getDefaultShowAction()
        if showAction:
            try:
                self.model.action(showAction)()
            except Exception as e:
                gamelog.debug('m.l@homeFurniture.afterModelFinish action error', e.message)

        self.addFurnitureLight()

    def createObstacleModel(self):
        data = self.getItemData()
        dynamicObstacle = data.get('dynamicObstacle', 0)
        self.dynamicObstacle = dynamicObstacle
        obstacleModel = data.get('obstacleModel', 0)
        scale = data.get('obstacleScale', 1)
        modelName = None
        if obstacleModel:
            if obstacleModel in FIMD.data:
                modelName = FIMD.data.get(obstacleModel, {}).get('modelPath', '')
            else:
                modelName = 'char/%i/%i.model' % (obstacleModel, obstacleModel)
        else:
            modelName = data.get('fullPath', None)
            if not modelName and data.has_key('model'):
                modelName = 'char/%i/%i.model' % (data['model'], data['model'])
        if modelName:
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((scale, scale, scale))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if not self.inWorld:
            return
        if model:
            self.obstacleModel = model
            self.addModel(model)
            self.obstacleModel.visible = False
            self.obstacleModel.setUserData(self.id)
            self.refreshCollide()

    def getTopLogoHeight(self):
        self.topLogoOffset = self.getItemData().get('heightOffset', 0)
        height = 0
        if not hasattr(self.model, 'bonesBoundingBoxSize'):
            height = self.model.height
        elif self.model.bonesBoundingBoxSize[1] <= 0:
            height = self.model.height
        else:
            height = self.model.bonesBoundingBoxSize[1]
        return height * self.model.scale[1] + self.topLogoOffset

    def enterWorld(self):
        super(HomeFurniture, self).enterWorld()
        if self.isAvatarFurniture() or self.isPlayerClone():
            self.modelServer = modelServer.AvatarModelServer(self)
            self.fashion.loadDummyModel()
            self.loadPhysiqueInfo()
        else:
            itemData = self.getItemData()
            model = itemData.get('model', 0)
            if model > const.MODEL_AVATAR_BORDER:
                self.modelServer = modelServer.AvatarModelServer(self)
                data = clientcom._getModelData(model)
                self.modelServer.bodyUpdateFromData(data)
            else:
                self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        if self.isPickFurniture():
            maxClickRadius = self.getItemData().get('maxClickRadius', 2)
            self.trapId = BigWorld.addPot(self.matrix, maxClickRadius, self.trapCallback)
        loopSound = self.getItemData().get('loopSound', 0)
        if loopSound:
            gameglobal.rds.sound.playBossMusic(loopSound, True)

    def triggerTrap(self, enteredTrap):
        if not self.isPickFurniture():
            return
        maxClickRadius = self.getItemData().get('maxClickRadius', 2)
        if not maxClickRadius:
            return
        if not inRange3D(maxClickRadius, BigWorld.player().position, self.position):
            return
        if not self.inWorld:
            return
        self.trapCallback(enteredTrap, 0)

    def updateAvatarConfig(self, avatarConfig):
        a = strmap.strmap(avatarConfig)
        hairDyes = a.map.get('hairDyes')
        if not hairDyes:
            playerAC = strmap.strmap(BigWorld.player().avatarConfig)
            playerHair = playerAC.map.get('hairDyes')
            a.set('hairDyes', playerHair)
            a.set('dyeMode', 1)
        return str(a)

    def loadPhysiqueInfo(self):
        if self.getItemData().get('advancedModel', False):
            if not self.physique:
                self.physique = copy.deepcopy(BigWorld.player().physique)
            if not self.avatarConfig:
                self.avatarConfig = BigWorld.player().avatarConfig
        equips, aspect, physique, avatarConfig, actionId, itemPlusInfo = editorHelper.instance().getPhysiqueInfo(self.ownerUUID)
        self.actionId = actionId
        if not equips and not aspect and not physique and not avatarConfig:
            if not self.avatarConfig:
                self.avatarConfig = self.updateAvatarConfig(avatarConfig)
            self.loadAvatarModel()
            return
        self.updatePhysiqueInfo(equips, aspect, physique, avatarConfig, actionId, itemPlusInfo)

    def leaveWorld(self):
        super(HomeFurniture, self).leaveWorld()
        if self.obstacleModel:
            self.delModel(self.obstacleModel)
            self.obstacleModel = None
        self.itemData = None
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        gameglobal.rds.ui.pressKeyF.delEnt(self.id, const.F_FURNITURE)
        if editorHelper.instance().selectedEnt == self:
            editorHelper.instance().lockTarget(None)
        if self.modelServer:
            self.modelServer.release()
        loopSound = self.getItemData().get('loopSound', 0)
        if loopSound:
            gameglobal.rds.sound.playBossMusic(loopSound, False)

    def setCollide(self, value):
        if not self.inWorld:
            return
        if self.obstacleModel:
            self.obstacleModel.setCollide(value)

    def getModelScale(self):
        data = self.getItemData()
        scale = data.get('modelScale', 1.0)
        return (scale, scale, scale)

    def canPutOver(self, ent):
        arrangeLv = self.getItemData().get('arrangeLv', 0)
        parentArrangeLv = IFD.data.get(ent.furnitureId, {}).get('arrangeLv', 0)
        return arrangeLv > parentArrangeLv or arrangeLv == parentArrangeLv and parentArrangeLv == -1

    def getOpacityValue(self):
        ins = editorHelper.instance()
        if ins and not ins.editMode and self.ownerUUID in ins.interactiveObjectMap:
            return (gameglobal.OPACITY_HIDE, False)
        if self.isAvatarFurniture:
            if gameglobal.rds.ui.modelFittingRoom.mediator:
                return (gameglobal.OPACITY_HIDE, False)
        return (gameglobal.OPACITY_FULL, True)

    @property
    def realAspect(self):
        return self.aspect

    @property
    def realPhysique(self):
        return self.physique

    @property
    def realAvatarConfig(self):
        return self.avatarConfig

    @property
    def realSchool(self):
        return self.physique.school

    @property
    def npcId(self):
        return self.furnitureId

    def isShowFashion(self):
        return True

    def isShowFashionWeapon(self):
        return True

    def isAvatarFurniture(self):
        isAvatar = IFD.data.get(self.furnitureId, {}).get('type', 0) == const.HOME_FURNITURE_TYPE_AVATAR
        return isAvatar

    def isPlayerClone(self):
        return IFD.data.get(self.furnitureId, {}).get('playerClone', 0)

    def withEquip(self):
        if not self.equips:
            return False
        for i in self.equips:
            if i:
                return True

        return False

    def use(self):
        if editorHelper.instance().editMode:
            return
        if self.isAvatarFurniture():
            gameglobal.rds.ui.target.showRightMenu(uiConst.MENU_MODEL_FITTING)
        elif self.isFuncFurniture():
            defaultChatId = FFD.data.get(self.furnitureId, {}).get('chat', [])
            gameglobal.rds.ui.funcNpc.openFunc(self.id, self.furnitureId, defaultChatId, self.processFunc)
        else:
            data = IFD.data.get(self.furnitureId, {})
            if data.get('canOpenZone', 0):
                ins = editorHelper.instance()
                if ins.ownerGbID:
                    p = BigWorld.player()
                    p.getPersonalSysProxy().openZoneOther(ins.ownerGbID)
            else:
                self.triggerActionEffect()

    def processFunc(self, funcType, funcParam):
        if not self.inWorld:
            return
        player = BigWorld.player()
        player.cell.useHomeFurniture(self.ownerUUID, self.furnitureId, funcType)

    def triggerActionEffect(self, needCD = True):
        if not self.inWorld:
            return
        data = IFD.data.get(self.furnitureId, {})
        fUseCD = data.get('fUseCD', 0)
        if needCD and self.lastFUseTime + fUseCD > utils.getNow():
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.HOME_FURNITURE_USE_CD, ())
            return
        if data.has_key('fEffects') or data.has_key('fActions'):
            if data.has_key('fEffects'):
                self.turnOnEffects()
            if data.has_key('fActions'):
                self.switchActions()
            self.fState = not self.fState
            if needCD:
                self.lastFUseTime = utils.getNow()

    def turnOnEffects(self):
        effects = self.getItemData().get('effects', [])
        fEffects = self.getItemData().get('fEffects', [])
        offEff, onEff = effects, fEffects
        if self.fState:
            offEff, onEff = fEffects, effects
        for eff in offEff:
            self.removeFx(eff)

        for eff in onEff:
            fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             eff,
             sfx.EFFECT_UNLIMIT))
            if fxs:
                self.addFx(eff, fxs)

    def switchActions(self):
        fAction = self.getItemData().get('fActions', ())
        fSounds = self.getItemData().get('fSound', (0, 0))
        if not self.fState:
            self.fashion.playActionSequence(self.model, fAction[0], self.resetFstate)
            gameglobal.rds.sound.playSound(fSounds[0], self, True)
        else:
            self.fashion.playActionSequence(self.model, fAction[1], None)
            gameglobal.rds.sound.playSound(fSounds[1], self, True)

    def resetFstate(self):
        self.fState = True
        self.triggerActionEffect(False)

    def updatePhysiqueInfo(self, equips, aspect, physique, avatarConfig, actionId = 0, itemPlusInfo = {}):
        equipment = Equipment()
        if equips:
            for part, value in equips.iteritems():
                equipment[part] = Item(value)

        uiUtils.setItemPlusInfo(equipment, itemPlusInfo)
        self.equips = equipment
        self.aspect = aspect if aspect else Appearance({})
        self.physique = Physique(physique)
        self.avatarConfig = avatarConfig
        self.actionId = actionId
        self.loadAvatarModel()

    def getShowActions(self):
        return IFD.data.get(self.furnitureId, {}).get('showActions', ())

    def getDefaultShowAction(self):
        showActions = self.getShowActions()
        if self.actionId and len(showActions) > self.actionId:
            return showActions[self.actionId]
        if showActions:
            return showActions[0]
        if self.isAvatarFurniture():
            return '1101'

    def loadAvatarModel(self):
        if (not self.equips or self.equips.noEquip()) and not self.aspect and not self.physique and not self.avatarConfig:
            return
        if self.getItemData().get('advancedModel', False):
            if not self.physique:
                self.physique = copy.deepcopy(BigWorld.player().physique)
            if not self.avatarConfig:
                self.avatarConfig = BigWorld.player().avatarConfig
        if self.modelServer == None:
            self.modelServer = modelServer.AvatarModelServer(self)
        self.modelServer.bodyUpdateStatus = modelServer.BODY_UPDATE_STATUS_NORMAL
        self.modelServer.bodyUpdate()
        self.modelServer.weaponUpdate()
        self.modelServer.wearUpdate()
        self.setTargetCapsUse(True)

    def afterWeaponUpdate(self, weapon):
        if weapon.followModelBias > 0:
            self.afterWearUpdate(weapon)

    def afterWearUpdate(self, wear):
        if self == gameglobal.rds.ui.fittingRoom.homeFurniture:
            model = gameglobal.rds.ui.fittingRoom.fittingModel
            clientcom.cloneEntityAllAttachments(self, model, True)

    def refreshOpacityState(self):
        super(HomeFurniture, self).refreshOpacityState()
        if not self.inWorld:
            return
        if getattr(self, 'obstacleModel', None):
            self.obstacleModel.visible = False
            self.refreshCollide()

    def isPickFurniture(self):
        data = IFD.data.get(self.furnitureId, {})
        if data.has_key('fEffects') or data.has_key('fActions') or data.get('canOpenZone', 0):
            return True
        return self.isFuncFurniture()

    def isFuncFurniture(self):
        functions = FFD.data.get(self.furnitureId, {}).get('functions', [])
        if len(functions):
            return True
        return False

    def filterFunctions(self):
        functions = FFD.data.get(self.furnitureId, {}).get('functions', [])
        return functions

    def getFKey(self):
        return IFD.data.get(self.furnitureId, {}).get('fKeyId', 154)

    def trapCallback(self, enteredTrap, handle):
        if enteredTrap:
            if not self.inWorld:
                return
            opValue = self.getOpacityValue()
            if opValue[0] != gameglobal.OPACITY_FULL:
                return
            if editorHelper.instance().editMode:
                return
            gameglobal.rds.ui.pressKeyF.addEnt(self.id, const.F_FURNITURE)
        else:
            gameglobal.rds.ui.pressKeyF.delEnt(self.id, const.F_FURNITURE)

    def isWallAttached(self):
        return IFD.data.get(self.furnitureId, {}).get('wallAttached', 0) == 1

    def isRoofAttached(self):
        return IFD.data.get(self.furnitureId, {}).get('wallAttached', 0) == 2

    def canSelected(self):
        if editorHelper.instance().editMode or self.isAvatarFurniture() or self.isPickFurniture():
            return True
        return False

    def refreshTargetCaps(self):
        self.setTargetCapsUse(self.canSelected())

    def canCollide(self):
        opValue = self.getOpacityValue()
        if opValue[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE, gameglobal.OPACITY_HIDE_WITHOUT_NAME):
            return False
        if not editorHelper.instance().editMode and not self.dynamicObstacle:
            return False
        return True

    def refreshCollide(self):
        self.setCollide(self.canCollide())

    def getControlPointPos(self):
        if not self.inWorld:
            return
        nodeName = IFD.data.get(self.furnitureId, {}).get('controlPoint', None)
        if nodeName and self.model:
            node = self.model.node(nodeName)
            if node:
                return node.position

    def onTargetCursor(self, enter):
        if not self.isPickFurniture():
            return
        if editorHelper.instance().editMode and enter:
            return
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                ui.set_cursor(cursor.pickup_home)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    def clearCloneAttachment(self, model):
        if not model:
            return
        cloneHPs = getattr(self, 'cloneHPs', [])
        if cloneHPs:
            try:
                for hp in cloneHPs:
                    if hp:
                        model.setHP(hp, None)

            except Exception as e:
                gamelog.debug('m.l@HomeFurniture.clearCloneAttachment', e.message)

    def canRotatePitch(self):
        return self.getItemData().get('canRotatePitch', False)

    def isShowYuanLing(self):
        return True

    def addFurnitureLight(self):
        lightParam = self.getItemData().get('lightParam')
        if lightParam:
            morpher = FurnitureDyeMorpher()
            morpher.setModel(self.model)
            morpher.read(lightParam)
            morpher.apply()

    def enterTopLogoRange(self, rangeDist = -1):
        pass

    def leaveDlgRange(self, unUsedDist):
        if self.isHomeStorageItem(self.furnitureId):
            gameglobal.rds.ui.homeTermsStorage.hide()

    def isHomeStorageItem(self, fId):
        fd = IFD.data.get(fId)
        if fd:
            ioi = fd.get('interactiveObjectId', 0)
            if ioi:
                if IAD.data.get(ioi, {}).get('isHomeStorage', False):
                    return True
        return False


def test(id = 369115):
    p = BigWorld.player()
    return BigWorld.createEntity('HomeFurniture', p.spaceID, 0, p.position, (0, 0, 1), {'furnitureId': id})
