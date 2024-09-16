#Embedded file name: /WORKSPACE/data/entities/client/inpc.o
import BigWorld
import gameglobal
import utils
import clientcom
import const
from sfx import sfx
from iClient import IClient
from helpers import fashion
from helpers import modelServer
from helpers import ufo
from helpers import tintalt
from helpers import vertexMorpher
from guis import ui
from guis import cursor
from data import npc_model_client_data as NMCD
from data import effect_lv_data as ELD
from data import sys_config_data as SCD
from data import npc_data as ND
HP_EFFECT = 'HP_head1'

class INpc(IClient):

    def __init__(self):
        super(INpc, self).__init__()
        self.firstFetchFinished = False
        self.modelServer = None
        self.npcInstance = True
        self.questOrder = None
        self.fetchOrder = None
        self._fetchID = 0
        self.topLogo = None
        self.idleActName = None
        self.noSelected = False
        self.bornActionName = None
        self.trapEventId = None
        self.taskEffect = None
        self.notLoadModelRange = False
        self.lastVoiceTime = 0

    @property
    def isMultiModel(self):
        if hasattr(self, 'physique') and self.physique.bodyType and not hasattr(self.physique, 'source'):
            return True
        return False

    def getItemData(self):
        return {'model': gameglobal.defaultModelID,
         'dye': 'Default'}

    def prerequisites(self):
        return []

    def canBeUse(self):
        p = BigWorld.player()
        useDist = p.getUseRange(self) + 1
        dist = p.position.distTo(self.position)
        if dist <= useDist:
            self.use()
            return True
        return False

    def getEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            return getattr(BigWorld.player(), 'npcEffectLv', gameglobal.EFFECT_MID)
        else:
            return gameglobal.EFFECT_MID

    def getSkillEffectLv(self):
        effectLv = self.getEffectLv()
        return ELD.data.get('npc', {}).get('content', {}).get(effectLv)[0]

    def getBeHitEffectLv(self):
        effectLv = self.getEffectLv()
        return ELD.data.get('npc', {}).get('content', {}).get(effectLv)[1]

    def getBuffEffectLv(self):
        effectLv = self.getEffectLv()
        return ELD.data.get('npc', {}).get('content', {}).get(effectLv)[2]

    def getEquipEffectLv(self):
        effectLv = self.getEffectLv()
        return ELD.data.get('npc', {}).get('content', {}).get(effectLv)[3]

    def getBasicEffectLv(self):
        effectLv = self.getEffectLv()
        return ELD.data.get('npc', {}).get('content', {}).get(effectLv)[4]

    def getEquipEffectPriority(self):
        if BigWorld.player().isRealInFuben():
            return gameglobal.EFF_PLAYER_EQUIP_PRIORITY
        return gameglobal.EFF_NPC_EQUIP_PRIORITY

    def getBasicEffectPriority(self):
        if BigWorld.player().isRealInFuben():
            return gameglobal.EFF_PLAYER_BASIC_PRIORITY
        return gameglobal.EFF_NPC_BASIC_PRIORITY

    def isUrgentLoad(self):
        return False

    def afterModelFinish(self):
        super(INpc, self).afterModelFinish()
        if self.fashion == None:
            return
        if self.model != None and len(self.model.motors) > 0:
            self.model.motors[0].footTwistSpeed = 0
        if not self.forbidUse() or self.forbidUse() and hasattr(self, '_isMarkerNpc') and self._isMarkerNpc():
            self.noSelected = False
        else:
            self.noSelected = True
        self.setTargetCapsUse(not self.noSelected)
        self.hide(self.beHide)
        self.filter.setYaw(self.initYaw)

    def getTopLogoFadeStart(self):
        return gameglobal.guiFadeEnd * 0.9

    def enterTopLogoRange(self, rangeDist = -1):
        super(INpc, self).enterTopLogoRange(rangeDist)
        if hasattr(self, 'getOpacityValue'):
            opacityValue = self.getOpacityValue()
            if opacityValue[0] == gameglobal.OPACITY_HIDE and hasattr(self, 'topLogo'):
                if self.topLogo:
                    self.topLogo.hide(True)

    def leaveTopLogoRange(self, rangeDist = -1):
        super(INpc, self).leaveTopLogoRange(rangeDist)

    def enterLoadModelRange(self, rangeDist = -1):
        if not self.isLoadModelWhenEnterWorld():
            self.notLoadModelRange = False
            self.reloadModel()

    def reloadModel(self):
        if self.modelServer:
            self.modelServer.release()
            self.modelServer = None
        if self.isMultiModel:
            self.modelServer = modelServer.MultiModelServer(self)
            clientcom.fetchTintEffectsContents(self.id, self.afterSetTintEffects)
        else:
            self.modelServer = modelServer.SimpleModelServer(self, True)

    def leaveLoadModelRange(self, rangeDist = -1):
        if not self.isLoadModelWhenEnterWorld():
            self.notLoadModelRange = True
            self.showTaskIndicator(None)
            model = sfx.getDummyModel(False)
            self.fashion.setupModel(model)
            if self.modelServer:
                self.modelServer.release()
                self.modelServer = None

    def showTaskIndicator(self, effectId):
        model = self.model
        try:
            if self.modelServer.rideModel:
                model = self.modelServer.rideModel.ride
        except:
            pass

        if self.taskEffect:
            if self.taskEffect[0] == effectId:
                return
            sfx.detachEffect(model, self.taskEffect[0], self.taskEffect[1], True)
            taskEffectId = self.taskEffect[0]
            if gameglobal.TASKINDICATOR_CACHE.has_key(taskEffectId):
                if len(gameglobal.TASKINDICATOR_CACHE[taskEffectId]) <= gameglobal.TASKINDICATOR_CNT:
                    gameglobal.TASKINDICATOR_CACHE[taskEffectId].append(self.taskEffect[1][0])
            else:
                gameglobal.TASKINDICATOR_CACHE[taskEffectId] = [self.taskEffect[1][0]]
            self.taskEffect = None
        if effectId:
            effectFx = None
            if not getattr(model, 'dummyModel', False) and gameglobal.TASKINDICATOR_CACHE.has_key(effectId):
                if len(gameglobal.TASKINDICATOR_CACHE[effectId]) > 0:
                    effectFx = gameglobal.TASKINDICATOR_CACHE[effectId].pop()
            if not effectFx:
                effectFx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 model,
                 effectId,
                 sfx.EFFECT_UNLIMIT,
                 sfx.KEEPEFFECTTIME))
            else:
                try:
                    node = sfx.getEffectNode(model, effectId)
                    node[0].attach(effectFx)
                    effectFx.setAttachMode(0, 1, 0)
                    effectFx.force()
                    effectFx = [effectFx]
                except:
                    effectFx = [effectFx]

            if effectFx:
                self.taskEffect = [effectId, effectFx]
                nmData = NMCD.data.get(self.npcId, {})
                offset = nmData.get('indicatorOffset', 0)
                taskIndicatorScale = nmData.get('taskIndicatorScale', None)
                if offset:
                    for e in effectFx:
                        if e:
                            e.bias = (0, offset, 0)

                if taskIndicatorScale:
                    for e in effectFx:
                        if e:
                            e.scale(taskIndicatorScale)

    def resetTopLogo(self):
        if self.inWorld and self.fashion and self.topLogo:
            self.topLogo.setHeight(self.getTopLogoHeight())
            return

    def enterWorld(self):
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.filter = BigWorld.DumbFilter()
        self.filter.clientYawMinDist = 0.0
        self.initYaw = self.yaw
        if self.isLoadModelWhenEnterWorld():
            if self.isMultiModel:
                self.modelServer = modelServer.MultiModelServer(self)
                self.modelServer.setUrgent(self.isUrgentLoad())
                clientcom.fetchTintEffectsContents(self.id, self.afterSetTintEffects)
            elif hasattr(self, 'isUseAvatarModelServer') and self.isUseAvatarModelServer():
                self.modelServer = modelServer.AvatarModelServer(self)
                self.modelServer.bodyUpdateFromData(getattr(self, 'avatarInfo', {}))
                self.modelServer.weaponUpdate()
                if self.inFlyTypeWing():
                    self.modelServer.wingFlyModelUpdate()
            else:
                self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        else:
            self.notLoadModelRange = True

    def afterSetTintEffects(self, ownerId, tintAvatarTas, tintAvatarName, tintEffects):
        if not self.inWorld:
            return
        clientcom.tintSectionsToCache(self, tintAvatarTas, tintAvatarName, tintEffects)
        self.modelServer.bodyUpdate()
        if self.getItemData().get('extraTint', None):
            self.modelServer.setWeaponEffectForbidden(True)
        self.modelServer.weaponUpdate()

    def isLoadModelWhenEnterWorld(self):
        return True
        if hasattr(self, 'isScenario') and self.isScenario in (gameglobal.SCENARIO_PLAY_NPC, gameglobal.SCENARIO_EDIT_NPC):
            return True
        if self.__class__.__name__ in ('Npc', 'Dawdler') and hasattr(self, 'npcId'):
            data = NMCD.data.get(self.npcId, {})
            return data.get('loadModelWhenEnterWorld', 0)
        return True

    def checkDistSqr(self, ds):
        p = BigWorld.player()
        if p.position.distSqrTo(self.position) > ds:
            return False
        return True

    def leaveWorld(self):
        self.showTaskIndicator(None)
        if self.fashion != None:
            self.fashion.attachUFO(ufo.UFO_NULL)
            self.fashion.release()
            self.fashion = None
        if self.topLogo != None:
            self.topLogo.release()
            self.topLogo = utils.MyNone
        if self.modelServer:
            self.modelServer.release()
            self.modelServer = None
        tintalt.ta_reset(self.allModels)
        self.removeAllFx()
        self.allModels = []
        self.model = None

    def setAvatarConfig(self, avatarConfig):
        m = vertexMorpher.AvatarFaceMorpher(self.id)
        m.readConfig(avatarConfig)
        m.apply()

    def setBornAction(self, bornActionName):
        if not bornActionName:
            return
        self.bornActionName = bornActionName
        if self.firstFetchFinished:
            self.fashion.playSingleAction(self.bornActionName)
            self.bornActionName = None

    def onTargetCursor(self, enter):
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                if (self.position - BigWorld.player().position).length > cursor.TALK_DISTANCE:
                    ui.set_cursor(cursor.talk_dis)
                else:
                    ui.set_cursor(cursor.talk)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    def leaveDlgRange(self, unUsedDist):
        gameglobal.rds.ui.clearNPCDlg(self)

    def needBlackShadow(self):
        return True

    def set_roleName(self, old):
        if self.topLogo != None:
            nameString = self.roleName
            if gameglobal.showEntityID and not BigWorld.isPublishedVersion():
                nameString += ':' + str(self.id)
            self.topLogo.nameString = nameString
            self.topLogo.name = nameString
            self.topLogo.updateRoleName(nameString)

    def forbidUse(self):
        if hasattr(self, 'npcId'):
            data = NMCD.data.get(self.npcId, {})
            if data.get('forbidUse', 0):
                return True
            npcData = ND.data.get(self.npcId, {})
            campRequire = npcData.get('campRequire', 0)
            p = BigWorld.player()
            if campRequire and campRequire != p.tempCamp:
                return True
        return False

    def getSeekDist(self):
        if hasattr(self, 'npcId'):
            nd = NMCD.data.get(self.npcId, {})
            return nd.get('seekDist', 0)
        return 0

    def checkTrapEventValid(self, eventData):
        if eventData[0] == gameglobal.VOICE_FLAG:
            soundCd = SCD.data.get('npcVoiceCd', 0)
            now = utils.getNow()
            if now - self.lastVoiceTime < soundCd:
                return False
            self.lastVoiceTime = now
        return super(INpc, self).checkTrapEventValid(eventData)

    def inRiding(self):
        return self.modelServer.state == modelServer.STATE_HORSE

    def canOutline(self):
        return not self.getItemData().get('notOutline', 0)
