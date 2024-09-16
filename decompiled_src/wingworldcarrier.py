#Embedded file name: /WORKSPACE/data/entities/client/wingworldcarrier.o
import BigWorld
import Math
import const
import gameglobal
from sMath import distance2D
from sfx import sfx
import gametypes
import gameconfigCommon
from Monster import Monster
from data import wing_world_carrier_data as WWCD

class WingWorldCarrier(Monster):
    IsWingWorldCarrier = True
    IsMonster = False

    def __init__(self):
        super(WingWorldCarrier, self).__init__()
        self.trapId = None
        self.oldWingWorldCarrier = {}
        self.applyTints = []
        self.obstacleModel = None
        self.hpFx = []
        self.hpStatus = -1

    @property
    def wingWorldCamp(self):
        if gameconfigCommon.enableWingWorldWarCamp():
            return self.ownerHostId
        return 0

    def enterWorld(self):
        super(WingWorldCarrier, self).enterWorld()
        itemData = self.getCarrierData()
        self.trapId = BigWorld.addPot(self.matrix, itemData.get('fKeyRadius', 3.0), self.trapCallback)
        self.oldIsBecomeLadder = self.wingWorldCarrier.isBecomeLadder

    def leaveWorld(self):
        super(WingWorldCarrier, self).leaveWorld()
        if self.trapId:
            gameglobal.rds.ui.pressKeyF.delEnt(self.id, const.F_WING_WORLD_CARRIR)
            BigWorld.delPot(self.trapId)
        for entId, index in self.oldWingWorldCarrier.iteritems():
            if entId not in self.wingWorldCarrier:
                ent = BigWorld.entities.get(entId)
                if ent and ent.inWorld:
                    ent.modelServer.leaveWingWorldCarrier(self)

        self.delObstacleModel()
        player = BigWorld.player()
        if self.oldWingWorldCarrier.get(player.id) == const.WING_WORLD_CARRIER_MAJOR_IDX and self.oldWingWorldCarrier.isBecomeLadder:
            player.isLockYaw = False

    def getObstacleModelIdx(self):
        if self.wingWorldCarrier.isBecomeLadder:
            return '1'
        return ''

    def afterModelFinish(self):
        super(WingWorldCarrier, self).afterModelFinish()
        itemData = self.getCarrierData()
        if itemData.get('useAvatarDropFilter', False):
            self.filter = BigWorld.AvatarDropFilter()
        else:
            self.filter = BigWorld.AvatarFilter()
        feetDist = itemData.get('feetDist', 0)
        if feetDist:
            self.filter.enableBodyPitch = True
            self.filter.feetDist = feetDist
        self.createObstacleModel()
        self.calHpStatus()

    def trapCallback(self, enteredTrap, handle):
        if enteredTrap:
            if not self.inWorld:
                return
            opValue = self.getOpacityValue()
            if opValue[0] != gameglobal.OPACITY_FULL:
                return
            p = BigWorld.player()
            selfSideId = p.wingWorldCamp if p.isWingWorldCampMode() else p.getOriginHostId()
            if p.wingWorldCarrier.get(p.id, 0):
                return
            if self.ownerHostId != selfSideId:
                return
            if not p.stateMachine.checkStatus_check(const.CT_ENTER_WING_WORLD_CARRIER, exclude=('ZAIJU_ST',), bMsg=False):
                return
            gameglobal.rds.ui.pressKeyF.addEnt(self.id, const.F_WING_WORLD_CARRIR)
        else:
            gameglobal.rds.ui.pressKeyF.delEnt(self.id, const.F_WING_WORLD_CARRIR)

    def refreshTrapCallback(self):
        p = BigWorld.player()
        itemData = self.getCarrierData()
        radius = itemData.get('fKeyRadius', 3.0)
        if distance2D(p.position, self.position) <= radius:
            self.trapCallback(1, None)
        else:
            self.trapCallback(0, None)

    def getFKey(self):
        return self.getCarrierData().get('fKeyId', 154)

    def use(self):
        p = BigWorld.player()
        p.ap.setYaw(self.yaw)
        p.cell.applyEnterWingWorldCarrier(self.id)

    def set_wingWorldCarrier(self, old):
        self.oldWingWorldCarrier = old
        self.refreshCarrier()
        self.refreshObstacleModel()
        player = BigWorld.player()
        if self.wingWorldCarrier.get(player.id) == const.WING_WORLD_CARRIER_MAJOR_IDX and self.wingWorldCarrier.isBecomeLadder:
            player.isLockYaw = True
        elif self.oldWingWorldCarrier.get(player.id) == const.WING_WORLD_CARRIER_MAJOR_IDX and self.oldWingWorldCarrier.isBecomeLadder:
            player.isLockYaw = False

    def refreshCarrier(self):
        for entId, index in self.oldWingWorldCarrier.iteritems():
            if entId not in self.wingWorldCarrier:
                ent = BigWorld.entities.get(entId)
                if ent and ent.inWorld:
                    ent.modelServer.leaveWingWorldCarrier(self)

        for entId, index in self.wingWorldCarrier.iteritems():
            ent = BigWorld.entities.get(entId)
            if not ent or not ent.inWorld:
                return
            ent.modelServer.enterWingWorldCarrier()

    def getCarrierData(self):
        return WWCD.data.get(self.carrierNo, {})

    def getRiderScale(self):
        return 1

    def getModelScale(self):
        scale = self.getCarrierData().get('scale', 1)
        return (scale, scale, scale)

    def set_hp(self, old):
        super(WingWorldCarrier, self).set_hp(old)
        p = BigWorld.player()
        if p.wingWorldCarrier.carrierEntId == self.id:
            gameglobal.rds.ui.zaijuV2.refreshHpAndMp(self.hp, self.mhp, self.mp, self.mmp)
        self.calHpStatus()

    def set_mhp(self, old):
        super(WingWorldCarrier, self).set_mhp(old)
        p = BigWorld.player()
        if p.wingWorldCarrier.carrierEntId == self.id:
            gameglobal.rds.ui.zaijuV2.refreshHpAndMp(self.hp, self.mhp, self.mp, self.mmp)

    def set_mp(self, old):
        super(WingWorldCarrier, self).set_mp(old)
        p = BigWorld.player()
        if p.wingWorldCarrier.carrierEntId == self.id:
            gameglobal.rds.ui.zaijuV2.refreshHpAndMp(self.hp, self.mhp, self.mp, self.mmp)

    def set_mmp(self, old):
        super(WingWorldCarrier, self).set_mmp(old)
        p = BigWorld.player()
        if p.wingWorldCarrier.carrierEntId == self.id:
            gameglobal.rds.ui.zaijuV2.refreshHpAndMp(self.hp, self.mhp, self.mp, self.mmp)

    def setGuard(self, isGuard):
        if isGuard:
            self.fashion.setMonsterCombatCaps(self.am)
        else:
            self.fashion.setMonsterIdleCaps(self.am)

    def createObstacleModel(self):
        data = self.getCarrierData()
        idx = self.getObstacleModelIdx()
        modelId = data.get('obstacleModel%s' % idx, None)
        scale = 1
        if modelId:
            modelName = 'char/%d/%d.model' % (modelId, modelId)
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((scale, scale, scale))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if not self.inWorld:
            return
        self.obstacleModel = model
        self.refreshObstacleModel()

    def delObstacleModel(self):
        if self.obstacleModel and self.obstacleModel.inWorld:
            self.delModel(self.obstacleModel)
        self.obstacleModel = None

    def setTargetCapsUse(self, canUse):
        super(WingWorldCarrier, self).setTargetCapsUse(canUse)
        if canUse:
            player = BigWorld.player()
            if player.isOnWingWorldCarrier() and player.wingWorldCarrier.carrierEntId == self.id:
                self.targetCaps = []

    def refreshObstacleModel(self):
        player = BigWorld.player()
        if self.oldIsBecomeLadder != self.wingWorldCarrier.isBecomeLadder:
            self.delObstacleModel()
            self.createObstacleModel()
            self.oldIsBecomeLadder = self.wingWorldCarrier.isBecomeLadder
        elif self.obstacleModel:
            if self.wingWorldCarrier.get(player.id):
                if self.obstacleModel.inWorld:
                    self.delModel(self.obstacleModel)
            elif not self.obstacleModel.inWorld:
                try:
                    self.addModel(self.obstacleModel)
                    self.obstacleModel.setEntity(self.id)
                except Exception as e:
                    player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, ['jbx:refreshObstacleModel,Error' + str(self.obstacleModel) + e.message], 0, {})

    def releaseHpEffect(self):
        if self.hpFx:
            for fx in self.hpFx:
                fx.stop()

        self.hpFx = []

    def attachHpEffect(self, effId):
        self.releaseHpEffect()
        self.hpFx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
         self.getBasicEffectPriority(),
         self.model,
         effId,
         sfx.EFFECT_LIMIT))

    def calHpStatus(self):
        itemData = self.getCarrierData()
        hpEffect = itemData.get('hpEffect', ())
        if hpEffect:
            tempHpRatio = self.hp * 1.0 / self.mhp
            for index, (hpRatio, effect) in enumerate(hpEffect):
                if tempHpRatio < hpRatio:
                    if index != self.hpStatus:
                        self.attachHpEffect(effect)
                        self.hpStatus = index
                        break

    def resetTopLogo(self):
        if not self.inWorld or not self.model or not self.topLogo:
            return
        if self.inWorld and self.model and self.topLogo and not gameglobal.gHideMonsterName:
            self.topLogo.hideName(False)
            self.topLogo.hideTitleName(False)
            self._hideQuestIcon(False)
