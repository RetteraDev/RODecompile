#Embedded file name: /WORKSPACE/data/entities/client/movingplatform.o
import BigWorld
import Sound
import Math
import clientcom
import gameglobal
import gamelog
import npcConst
import clientUtils
from iNpc import INpc
from helpers import modelServer
from helpers import scenario
from callbackHelper import Functor
from sMath import pi
from sfx import sfx
from iDisplay import IDisplay
from data import moving_platform_data as MPD
from data import npc_data as ND
from cdata import teleport_data as TD

class MovingPlatform(INpc, IDisplay):
    DELTAYAWCNT = 20

    def __init__(self):
        super(MovingPlatform, self).__init__()
        self.targetYaw = self.yaw
        self.deltaYaw = 0.0
        self.handleCallback = None
        self.lastMoving = False
        self.soundCallBack = None
        self.soundHandle = None
        self.aniModel = None
        self.aniAction = None
        self.isMoving = False
        self.noCollideModel = None
        self.attachedNpcs = []
        self.trapId = None
        self.musicTrapId = None
        self.keepEffs = []

    def getItemData(self):
        itemData = MPD.data.get(self.platNo, {})
        modelId = itemData.get('model')
        itemData['collide'] = not itemData.get('noCollide', False)
        itemData['dynamicObstacle'] = not itemData.get('noCollide', False)
        itemData['dye'] = 'Default'
        itemData['model'] = modelId
        itemData['modelShow'] = 1
        return itemData

    def needBlackShadow(self):
        data = self.getItemData()
        noBlackUfo = data.get('noBlackUfo', False)
        return not noBlackUfo

    def needFKey(self):
        return self.getItemData().get('needFKey', False)

    def needNotifyMusic(self):
        return self.getItemData().get('needNotifyMusic', True)

    def isMarriage(self):
        return self.getItemData().get('isMarriage', False)

    def enterWorld(self):
        super(MovingPlatform, self).enterWorld()
        self.filter = BigWorld.AvatarFilter()
        itemData = self.getItemData()
        player = BigWorld.player()
        if player and itemData.get('sight'):
            proxy = self.getProxy()
            if proxy == None:
                player.buildingProxy.sightEnter(player.spaceID, self.id, self.createProxyData())
            else:
                proxy.entityEnterWorld(self.createProxyData(), False)
        else:
            gamelog.debug('@PGF:MovingPlatform.enter world,  player is None', self.id)
        if self.needFKey():
            fKeyDist = itemData.get('fKeyDist', 2)
            self.trapId = BigWorld.addPot(self.matrix, fKeyDist, self.trapCallback)
        if self.needNotifyMusic():
            notifyMusicDist = itemData.get('notifyMusicDist', 2)
            self.musicTrapId = BigWorld.addPot(self.matrix, notifyMusicDist, self.trapMusicCallback)

    def _addNoCollideModel(self):
        data = MPD.data.get(self.platNo, {})
        modelId = data.get('noCollideModel', 0)
        if modelId:
            clientcom.fetchModel(gameglobal.URGENT_THREAD, self.onGetNoCollideModel, modelId)

    def onGetNoCollideModel(self, model):
        if not self.inWorld:
            return
        if model:
            self.noCollideModel = model
            BigWorld.player().addModel(model)
            self.noCollideModel.position = self.position
            self.noCollideModel.yaw = self.yaw
            scale = self.getItemData().get('scale')
            model.scale = (scale, scale, scale)

    def onAniModelLoaded(self, model):
        if not self.inWorld:
            return
        if not self.aniModel:
            am = BigWorld.ActionMatcher(self)
            am.turnModelToEntity = 1
            am.matcherCoupled = 1
            am.inheritOnRecouple = 1
            am.bodyTwistSpeed = 150
            am.maxMatchDist = 80
            am.matchCaps = []
            am.moveNotifier = self.movingNotifier
            am.moveNotifierSpeed = 0.2
            model.motors = (am,)
            model.soundCallback(self.fashion.actionCueCallback)
            self.aniModel = model
            self.addModel(self.aniModel)
            self.aniModel.position = self.position
            self.aniModel.yaw = self.yaw
            player = BigWorld.player()
            if player and self.getItemData().get('sight'):
                proxy = self.getProxy()
                if proxy == None:
                    player.buildingProxy.sightEnter(player.spaceID, self.id, self.createProxyData())
                else:
                    proxy.entityEnterWorld(self.createProxyData(), True)
                    self.isMoving = proxy.getExtraDataByKey('moving')
            else:
                gamelog.debug('@PGF:MovingPlatform.afterModelFinish,  player is None', self.id)
            self.playActWithAniModel()

    def createProxyData(self):
        proxyData = {'cls': self.classname(),
         'pos': self.position,
         'dir': (0, 0, self.yaw),
         'extra': {'platNo': self.platNo,
                   'pos': self.position,
                   'dir': (0, 0, self.yaw)}}
        return proxyData

    def afterModelFinish(self):
        super(MovingPlatform, self).afterModelFinish()
        self.refreshOpacityState()
        itemData = MPD.data.get(self.platNo, {})
        if itemData.get('useAvatarDropFilter', False):
            self.filter = BigWorld.AvatarDropFilter()
        else:
            self.filter = BigWorld.AvatarFilter()
        if itemData.has_key('feetDist'):
            self.filter.enableBodyPitch = True
            self.filter.feetDist = itemData['feetDist']
        needChangeDir = self.getItemData().get('changeDir', False)
        if needChangeDir:
            self.filter.enableClientYawDecay = True
            self.filter.clientYawMinDist = 0.0
        else:
            self.filter.clientYawMinDist = gameglobal.CLIENT_MIN_YAW_DIST
        self.filter.suckPop = False
        self.model.vehicleID = self.id
        if hasattr(self.model, 'setEntity'):
            self.model.setEntity(self.id)
        self.setTargetCapsUse(False)
        if self.getItemData().get('sight'):
            modelServer.loadModelByItemData(self.id, gameglobal.URGENT_THREAD, self.onAniModelLoaded, {'model': self.getItemData().get('sightModel')}, False, True)
        self._attachClientNpc()
        self._addNoCollideModel()
        self.playKeepEffs()

    def playKeepEffs(self):
        self.releaseKeepEffs()
        keepEffs = self.getItemData().get('keepEffs', [])
        try:
            for effId in keepEffs:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
                 self.getSkillEffectPriority(),
                 self.model,
                 effId,
                 sfx.EFFECT_LIMIT,
                 -1))
                if fx:
                    self.keepEffs.extend(fx)

        except Exception as e:
            gamelog.debug('m.l@MovingPlatform.playKeepEffs error', e.message)

    def releaseKeepEffs(self):
        if self.keepEffs:
            for eff in self.keepEffs:
                if eff:
                    eff.stop()

            self.keepEffs = []

    def leaveWorld(self):
        super(MovingPlatform, self).leaveWorld()
        p = BigWorld.player()
        if self.soundCallBack:
            BigWorld.cancelCallback(self.soundCallBack)
        if self.soundHandle:
            Sound.stopFx(self.soundHandle)
        if self.aniModel:
            self.delModel(self.aniModel)
            self.aniModel = None
        proxy = self.getProxy()
        if proxy:
            proxy.entityLeaveWorld(self.createProxyData())
        self._detachClientNpc()
        try:
            if self.noCollideModel:
                p.delModel(self.noCollideModel)
                self.noCollideModel = None
        except:
            pass

        itemData = self.getItemData()
        if self.needFKey() and gameglobal.rds.ui.pressKeyF.movingPlatform and gameglobal.rds.ui.pressKeyF.movingPlatform.id == self.id:
            BigWorld.player().movingPlatformTrapCallback(())
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        if self.musicTrapId:
            BigWorld.delPot(self.musicTrapId)
            self.musicTrapId = None
            notifyMusicId = itemData.get('notifyMusicId', 0)
            p.notifyMusicCallBack(False, notifyMusicId)
        self.releaseKeepEffs()

    def checkCollideWithPlayer(self):
        pass

    def refreshOpacityState(self):
        opacityVal, _ = self.getOpacityValue()
        if opacityVal == gameglobal.OPACITY_FULL:
            self.hide(False)
        else:
            self.hide(True)

    def getOpacityValue(self):
        opacityVal = super(MovingPlatform, self).getOpacityValue()
        if gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_END:
            scenarioIns = scenario.Scenario.PLAY_INSTANCE if scenario.Scenario.PLAY_INSTANCE else scenario.Scenario.INSTANCE
            if scenarioIns.hideMovingPlat:
                return (gameglobal.OPACITY_HIDE, False)
        return opacityVal

    def setYaw(self, yaw, rotateTime):
        if self.yaw != yaw:
            rotate = self.yaw - yaw
            rotate = rotate + 2 * pi if rotate < -pi else (rotate - 2 * pi if rotate > pi else rotate)
            tgt = self.yaw - rotate
            p = BigWorld.player()
            if p.vehicle and p.vehicle.id == self.id:
                self.filter.setYaw(tgt, rotateTime * 0.9)
            else:
                self.filter.setYaw(tgt)

    def needMoveNotifier(self):
        return True

    def activate(self):
        itemData = MPD.data.get(self.platNo, {})
        sound = itemData.get('sound')
        time = itemData.get('looptime')
        if sound and time:
            self.playSound(sound, time, 0)

    def playSound(self, sound, time, index = 0):
        if not self.inWorld:
            return
        gameglobal.rds.sound.playFx(sound[0], self.position, False, self)
        if self.soundCallBack:
            BigWorld.cancelCallback(self.soundCallBack)
        if self.soundHandle:
            Sound.stopFx(self.soundHandle)
        self.soundHandle = gameglobal.rds.sound.playFx(sound[index], self.position, True, self)
        if index <= 1:
            self.soundCallBack = BigWorld.callback(time[index], Functor(self.playSound, sound, time, index + 1))

    def playActWithAniModel(self):
        if not self.aniModel:
            return
        try:
            if self.isMoving:
                self.aniModel.action('1110')()
            else:
                self.aniModel.action('1101')()
        except:
            pass

    def movingNotifier(self, isMoving, moveSpeed = 1.0):
        self.isMoving = isMoving
        self.playActWithAniModel()

    def checkPlayerPos(self):
        p = BigWorld.player()
        vehicleDirection = (self.roll, self.pitch, self.yaw)
        m = Math.Matrix()
        m.setRotateYPR(Math.Vector3(vehicleDirection[2], vehicleDirection[1], vehicleDirection[0]))
        m.invert()
        x, y, z = m.applyPoint(Math.Vector3(p.position - self.position))
        bounds = self.getItemData().get('bounds', None)
        if not bounds:
            return 0
        for bound in bounds:
            if len(bound) != 6:
                gamelog.info('@PGF:MovingPlatform.checkPlayerPos, wrong bounds data', self.id, self.platNo, bounds)
                continue
            if bound[0] < x < bound[1] and bound[2] < y < bound[3] and bound[4] < z < bound[5]:
                return bound[3]

        return 0

    @clientUtils.callFilter(1.0, False)
    def doAfterCollideWithPlayer(self):
        functions = self.getItemData().get('functions', [])
        for funcName, func, funcId in functions:
            if func == npcConst.NPC_FUNC_TELEPORT:
                d = TD.data.get(funcId, None)
                if d == None:
                    continue
                teleport = d.get('teleport')
                spaceNo = teleport[0][1]
                BigWorld.player().npcTeleportByClientNpc(self.platNo, spaceNo, 0)

    def _attachClientNpc(self):
        if self.attachedNpcs:
            return
        data = self.getItemData()
        for attachedNpcs in data.get('attachedNpcs', ()):
            npcId, offset, direction = attachedNpcs
            notFollowHost = ND.data.get(npcId, {}).get('notFollowHost', False)
            if notFollowHost:
                properties = {'npcId': npcId,
                 'hostId': self.id,
                 'hostNo': self.platNo}
                self.attachedNpcs.append(BigWorld.createEntity('ClientNpc', self.spaceID, 0, self.position, direction, properties))
            else:
                properties = {'npcId': npcId,
                 'hostId': self.id,
                 'hostNo': self.platNo,
                 'offset': offset}
                self.attachedNpcs.append(BigWorld.createEntity('ClientNpc', self.spaceID, self.id, self.position, direction, properties))

    def _detachClientNpc(self):
        if not self.attachedNpcs:
            return
        for attachedNpcId in self.attachedNpcs:
            BigWorld.destroyEntity(attachedNpcId)

        self.attachedNpcs = []

    def playEffect(self, effectId, targetPos = None, pitch = 0, yaw = 0, roll = 0, maxDelayTime = -1, scale = 1.0):
        if not self.attachedNpcs:
            return
        ent = BigWorld.entities.get(self.attachedNpcs[0], None)
        if not ent or not ent.inWorld:
            return
        model = ent.model
        if targetPos is None:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             model,
             effectId,
             sfx.EFFECT_LIMIT,
             maxDelayTime))
        else:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             model,
             effectId,
             sfx.EFFECT_LIMIT,
             targetPos,
             pitch,
             yaw,
             roll,
             maxDelayTime))
        if fx:
            for fxItem in fx:
                fxItem.scale(scale, scale, scale)

    def flashNotice(self, flashNum, soundId):
        if flashNum:
            BigWorld.flashWindow(flashNum)
        if soundId:
            gameglobal.rds.sound.playSound(soundId)

    def doClientNpcEvent(self, info):
        for entityId in self.attachedNpcs:
            npc = BigWorld.entities.get(entityId)
            for npcId, eventType, eventArg in info:
                if npc and npc.npcId == npcId:
                    if type(eventArg) != tuple:
                        eventArg = (eventArg,)
                    if eventType == 1:
                        npc.fashion.stopAction()
                        npc.fashion.playAction(eventArg)
                    elif eventType == 2:
                        npc.chatToView(*eventArg)

    def canUseSkill(self):
        if self.inWorld:
            itemData = MPD.data.get(self.platNo, {})
            return itemData.get('canUseSkill', False) and not self.checkMovingByVelocity()
        return False

    def checkMovingByVelocity(self):
        return self.velocity.length > 0

    def use(self):
        pass

    def isValidUse(self):
        if hasattr(self, 'groupNUID') and self.groupNUID and self.groupNUID != BigWorld.player().groupNUID:
            gamelog.error('m.l@MovingPlatform.isValidUse groupNUID wrong', self.groupNUID, BigWorld.player().groupNUID)
            return False
        return True

    def getFKey(self):
        return self.getItemData().get('fKeyId', 2001)

    def checkTrapCallback(self):
        return False

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        if p.carrier.carrierEntId == self.id and p.isOnCarrier():
            return
        opValue = self.getOpacityValue()
        if enteredTrap:
            if opValue[0] != gameglobal.OPACITY_FULL:
                return
            if hasattr(self, 'groupNUID') and self.groupNUID and self.groupNUID != p.groupNUID:
                return
            if self.checkTrapCallback():
                return
        if enteredTrap:
            p.movingPlatformTrapCallback((self,))
        else:
            p.movingPlatformTrapCallback([])

    def trapMusicCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        itemData = self.getItemData()
        notifyMusicId = itemData.get('notifyMusicId', 0)
        if enteredTrap:
            p.notifyMusicCallBack(True, notifyMusicId)
        else:
            p.notifyMusicCallBack(False, notifyMusicId)

    def getModelScale(self):
        scale = self.getItemData().get('scale', 1)
        return (scale, scale, scale)

    def getRiderScale(self):
        riderScale = self.getItemData().get('riderScale', 0)
        if riderScale:
            riderScale /= self.getItemData().get('scale', 1)
        return riderScale
