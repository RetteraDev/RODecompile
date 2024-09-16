#Embedded file name: /WORKSPACE/data/entities/client/helpers/foottrigger.o
import datetime
import BigWorld
import Pixie
import gameglobal
import gamelog
import gametypes
import callbackHelper
import utils
import const
import clientUtils
from sfx import sfx
from data import foot_dust_data as FDD
from data import foot_sound_data as FSD
from data import equip_data as ED
TERRAINSOUNDINFO = {'default': 0,
 'grass': 0,
 'small_grass': 0,
 'large_grass': 0,
 'water': 6,
 'gravel': 12,
 'wood': 18,
 'small_wood': 18,
 'large_wood': 18,
 'metal': 24,
 'snow': 30,
 'stone': 36,
 'small_stone': 36,
 'large_stone': 36,
 'sand': 42,
 'coin': 48}

class FootTriggerMgr(object):
    FOOTTRIGGER_MAXLOD = 20

    def __init__(self, owner):
        self.model = None
        self.owner = BigWorld.entity(owner)
        self.stampState = callbackHelper.State()
        self.footPair = []
        self.lastfootTime = datetime.datetime.now()
        self.footIdleEffects = []
        self.entity = None
        self.previewDustId = None
        self.previewLastTime = 0
        self.equipDustId = 0

    def release(self):
        if not self.model:
            return
        for footNode, footTrigger in self.footPair:
            attachs = footNode.attachments
            for a in attachs:
                if isinstance(a, BigWorld.FootTrigger):
                    footNode.detach(a)

        self.footPair = []
        self.owner = None
        self.model = None
        self.entity = None
        self.stampState.change()
        self.equipDustId = 0

    def setupFootTrigger(self, entity, modelID, model):
        self.release()
        data = FDD.data.get(modelID, None)
        if not data:
            return
        nodes = data.get('nodes')
        if nodes == None or len(nodes) < 2:
            return
        feet = []
        for node in nodes:
            n = model.node(node)
            if n == None:
                return
            feet.append(n)

        for i, node in enumerate(feet):
            footTrigger = BigWorld.FootTrigger(i, 'Footstep')
            footTrigger.footstepCallback = self.footCallback
            footTrigger.maxLod = self.FOOTTRIGGER_MAXLOD
            footTrigger.restHeight = 0.05
            node.attach(footTrigger)
            self.footPair.append((node, footTrigger))

        self.model = model
        self.entity = entity
        self.isAvatar = hasattr(entity, 'avatarInstance')

    def footCallback(self, speed, odd, isTerrain, texName, materialKind, pos):
        gamelog.debug('footCallback')
        if not self.model:
            return
        owner = self.entity
        if hasattr(owner, 'inHiding') and owner.inHiding() and owner != BigWorld.player():
            return
        if True:
            now = datetime.datetime.now()
            texName = 'default' if texName == '' else texName
            if now > self.lastfootTime + datetime.timedelta(microseconds=100000) and owner.inMoving():
                if owner.fashion.isPlayer:
                    self.__playAvatarFootSound(texName)
                    self.__playClothSound()
                else:
                    self.__playMonsterFootSound(texName)
                self.lastfootTime = now
                self.playDustEffect(texName, odd)

    def _loadDustEffect(self, dust):
        return clientUtils.pixieFetch(sfx.getPath(dust))

    def overrideCallback(self, func, keepTime):
        if not self.model:
            return
        self.stampState.change()
        if not self.model:
            return
        for footNode, footTrigger in self.footPair:
            footTrigger.footstepCallback = func
            footTrigger.maxLod = self.FOOTTRIGGER_MAXLOD

        BigWorld.callback(keepTime, self.stampState.functor(self._restoreFootprintCallback))

    def _restoreFootprintCallback(self):
        for footNode, footTrigger in self.footPair:
            footTrigger.footstepCallback = self.footCallback
            footTrigger.maxLod = self.FOOTTRIGGER_MAXLOD

    def __playAvatarFootSound(self, texName):
        if gameglobal.rds.configData.get('enableNewFootSound', False):
            self.playNewAvatarFootSound(texName)
            return
        owner = self.entity
        modelId = owner.fashion.modelID
        soundPath = 'fx/footstep/'
        soundData = FSD.data.get(modelId, {})
        dataKey = texName + 'Sound'
        soundfx = soundData.get(dataKey, None)
        if soundfx:
            if owner.isDashing:
                soundPath = soundPath + soundfx[1]
            else:
                soundPath = soundPath + soundfx[0]
            gameglobal.rds.sound.playFx(soundPath, owner.position, False, owner)

    def playNewAvatarFootSound(self, texName):
        owner = self.entity
        modelId = owner.fashion.modelID
        soundPath = 'fx/footsound/' + str(modelId)
        fxTime = TERRAINSOUNDINFO.get(texName, 0)
        if owner.isDashing:
            soundPath = soundPath + '_run'
        else:
            soundPath = soundPath + '_walk'
        gameglobal.rds.sound.playHitFx(soundPath, 'fxstyle', fxTime, owner)

    def __playMonsterFootSound(self, texName):
        pass

    def refreshEquipDust(self, owner):
        for key in gametypes.ASPECT_PART_DICT.keys():
            if key == 'footdust':
                continue
            eId = getattr(owner.aspect, key, None)
            if eId:
                dust = ED.data.get(eId, {}).get('footDust', None)
                if dust:
                    self.equipDustId = dust
                    return

    def getEquipFootDustData(self, modelID):
        owner = self.entity
        if not owner.IsAvatar:
            return FDD.data.get(modelID)
        if owner == BigWorld.player():
            footdust = getattr(owner.realAspect, 'footdust', None)
        else:
            footdust = getattr(owner.aspect, 'footdust', None)
        if self.previewDustId and utils.getNow() - self.previewLastTime <= 8:
            fdd = FDD.data.get(self.previewDustId)
            if not fdd:
                return FDD.data.get(modelID)
            else:
                return fdd
        elif not footdust:
            if not self.equipDustId:
                return FDD.data.get(modelID)
            else:
                return FDD.data.get(self.equipDustId)
        else:
            if owner.IsAvatar and owner.bianshen[0] != gametypes.BIANSHEN_HUMAN:
                return FDD.data.get(modelID)
            dustId = ED.data.get(footdust, {}).get('footDust', None)
            fdd = FDD.data.get(dustId)
            if not fdd:
                return FDD.data.get(modelID)
            return fdd

    def playFootIdleEffect(self):
        owner = self.entity
        if not owner:
            return
        if not self.isAvatar:
            return
        self.releaseFootIdleEffect()
        if owner.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            return
        if getattr(owner, 'inSwim', 0):
            return
        if getattr(owner, 'inFly', 0):
            return
        if owner.inMoving():
            return
        modelID = owner.fashion.modelID
        fdd = self.getEquipFootDustData(modelID)
        effects = fdd.get('footIdleEffect', [])
        if effects:
            for effect in effects:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getBasicEffectLv(),
                 owner.getBasicEffectPriority(),
                 owner.model,
                 effect,
                 sfx.EFFECT_LIMIT,
                 -1))
                if fx:
                    self.footIdleEffects.extend(fx)

    def releaseFootIdleEffect(self):
        if self.footIdleEffects:
            for fx in self.footIdleEffects:
                if fx:
                    fx.stop()

            self.footIdleEffects = []

    def refreshFootIdleEffect(self):
        self.releaseFootIdleEffect()
        self.playFootIdleEffect()

    def playDustEffect(self, texName, odd):
        owner = self.entity
        if not owner or not owner.inWorld:
            return
        if owner.IsAvatar and not owner.fashion.isPlayer:
            if owner == BigWorld.player() and getattr(owner.realAspect, 'footdust', None):
                pass
            elif getattr(owner.aspect, 'footdust', None):
                pass
            else:
                return
        modelID = owner.fashion.modelID
        if utils.instanceof(owner, 'Npc') and modelID > const.MODEL_AVATAR_BORDER:
            return
        fdd = self.getEquipFootDustData(modelID)
        self.realPlayDustEffect(fdd, texName, owner, odd)
        if hasattr(owner, 'isDashing') and owner.isDashing:
            self.realPlayDustEffect(FDD.data.get(owner.school), texName, owner, odd)

    def realPlayDustEffect(self, data, texName, owner, odd):
        footDustEffect = getattr(owner, 'footDustEffect', None)
        if getattr(owner, 'inCombat', False) and not footDustEffect:
            return
        if data:
            if footDustEffect:
                dusts = footDustEffect
            else:
                dusts = data.get(texName)
            if (dusts == None or len(dusts) == 0) and texName != 'default':
                dusts = data.get('default')
            effectId = None
            if dusts:
                effectId = dusts[0]
            if dusts and hasattr(owner, 'isDashing') and owner.isDashing and len(dusts) > 1:
                effectId = dusts[1]
            attachNodes = data.get('nodes', ('biped L Toe0', 'biped R Toe0'))
            attachNode = attachNodes[odd]
            gamelog.debug('zrz:', texName, effectId)
            if data.get('stayOrigin', None):
                if data.get('useFootPos', None):
                    footNode = owner.model.node(attachNode)
                    pos = footNode.position if footNode else owner.position
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (owner.getSkillEffectLv(),
                     owner.getSkillEffectPriority(),
                     None,
                     effectId,
                     sfx.EFFECT_LIMIT_MISC,
                     pos,
                     0,
                     0,
                     0,
                     gameglobal.EFFECT_LAST_TIME))
                else:
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getBasicEffectLv(),
                     gameglobal.EFF_PLAYER_EQUIP_PRIORITY,
                     owner.model,
                     effectId,
                     sfx.EFFECT_LIMIT_MISC,
                     gameglobal.EFFECT_LAST_TIME))
            else:
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_ONNODE, (owner.getBasicEffectLv(),
                 gameglobal.EFF_PLAYER_EQUIP_PRIORITY,
                 owner.model,
                 attachNode,
                 effectId,
                 sfx.EFFECT_LIMIT_MISC,
                 gameglobal.EFFECT_LAST_TIME))
            extraEffects = data.get('extraEffect', [])
            if extraEffects:
                for extraEffect in extraEffects:
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_ONNODE, (owner.getBasicEffectLv(),
                     gameglobal.EFF_PLAYER_EQUIP_PRIORITY,
                     owner.model,
                     attachNode,
                     extraEffect,
                     sfx.EFFECT_LIMIT_MISC,
                     gameglobal.EFFECT_LAST_TIME))

    def __playClothSound(self):
        owner = self.entity
        if not owner.isDashing:
            bodyEquipM = str(owner.getBodyEquipMaterail())
            if bodyEquipM:
                fxPath = 'fx/equip/cloth%s_%s' % (bodyEquipM, bodyEquipM)
                gameglobal.rds.sound.playFx(fxPath, owner.position, False, owner)

    def setPreviewDustId(self, dustId):
        self.previewDustId = dustId
        self.previewLastTime = utils.getNow()
