#Embedded file name: /WORKSPACE/data/entities/client/avatarmonster.o
import copy
import random
import BigWorld
import gametypes
import gameglobal
import commcalc
import clientcom
import const
import skillDataInfo
from Monster import Monster
from helpers import fashion
from helpers import modelServer
from helpers import vertexMorpher
from helpers import tintalt
from helpers import modelRobber
from data import monster_data as MD
from data import skill_fenshen_data as SFD
from data import monster_action_data as MAD
from data import sky_wing_challenge_config_data as SWCCD

class AvatarMonster(Monster):
    IsMonster = True
    IsSummonedBeast = False

    @property
    def realAspect(self):
        return self.aspect

    @property
    def realPhysique(self):
        return self.physique

    @property
    def realSchool(self):
        return self.school

    @property
    def realLv(self):
        return self.lv

    @property
    def realAvatarConfig(self):
        return self.avatarConfig

    def getWeapon(self, isLeft):
        if isLeft:
            return self.realAspect.leftWeapon
        return self.realAspect.rightWeapon

    def getWeaponEnhLv(self, isLeft):
        if isLeft:
            return self.realAspect.leftWeaponEnhLv()
        return self.realAspect.rightWeaponEnhLv()

    def __init__(self):
        super(AvatarMonster, self).__init__()
        self.bufActState = None
        self.buffModelScale = None
        self.buffIdModelScale = None
        self.weaponState = gametypes.WEAPON_HANDFREE
        self.inWeaponCallback = None
        self.avatarInfo = None
        self.dieActIndex = 0
        self.oldYaw = 0.0
        if self.aspectCharType:
            self.charType = self.aspectCharType

    def isAvatarMonster(self):
        return True

    def weaponInHandState(self):
        return self.weaponState

    def isGuarding(self):
        return self.inCombat

    def isShowFashion(self):
        return not not commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_FASHION)

    def _checkAspectPhysique(self):
        if self.aspect.body or self.aspect.hand or self.physique.bodyType:
            return True
        return False

    def enterWorld(self):
        if self.charType == SWCCD.data.get('challengeBossId', 0):
            self.updateTimerBlood()
        self.syncSubProps()
        self.modelServer = modelServer.AvatarMonsterModelServer(self)
        if hasattr(self, 'fenshenId'):
            self.modelServer.setUrgent(True)
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.playBossMusic(True)
        mdData = MD.data.get(self.charType, {})
        if mdData.get('energy') == 1:
            name = mdData.get('energyName')
            color = mdData.get('energyColor')
            gameglobal.rds.ui.bossEnergy.show(self.id, name, color, int(100 * self.mp / self.mmp))
        if mdData.get('groupMonster') == 1:
            gameglobal.rds.ui.monsterBlood.addMonster(self.id, self.roleName, self.hp, self.mhp)
            if gameglobal.rds.ui.monsterBlood.mediator == None:
                gameglobal.rds.ui.monsterBlood.show()
        if mdData.get('needFightBlood'):
            gameglobal.rds.ui.fightObserve.addMonster(self)
            if gameglobal.rds.ui.fightObserve.monsterBloodMediator == None:
                gameglobal.rds.ui.fightObserve.showMonsterBlood()
        self.addTrapEvent()
        if not (self.hideNpcId and modelRobber.getInstance().tryRobAvatarModel(self)):
            if self._checkAspectPhysique():
                itemData = self.getItemData()
                modelId = itemData.get('model', 0)
                if self.avatarConfig:
                    self.weaponState = gametypes.WEAPON_HANDFREE
                    self.afterEnterWorld()
                elif modelId > const.MODEL_AVATAR_BORDER:
                    filePath = '%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, modelId)
                    clientcom.ConfigCache.fetchConfig(filePath, self._onLoadAvatarConfig)
                else:
                    self.weaponState = gametypes.WEAPON_HANDFREE
                    self.afterEnterWorld()
            else:
                cloneEntity = BigWorld.entities.get(self.avatarId)
                if not cloneEntity:
                    cloneEntity = BigWorld.player()
                self.aspect = copy.deepcopy(cloneEntity.realAspect)
                self.school = cloneEntity.realSchool
                self.weaponState = cloneEntity.weaponState
                self.physique = copy.deepcopy(cloneEntity.realPhysique)
                self.signal = cloneEntity.signal
                self.avatarConfig = cloneEntity.realAvatarConfig
                self.afterEnterWorld()
            if getattr(self, 'isOnlyClient', False):
                self.noSelected = True
        if getattr(self, 'fallenRedGuardFlag', None) and gameglobal.rds.configData.get('enableKillFallenRedGuard', False):
            gameglobal.rds.ui.killFallenRedGuardRank.enterMonster(self.fallenRedGuardFlag)

    def leaveWorld(self):
        super(AvatarMonster, self).leaveWorld()
        self.playBossMusic(False)
        self.avatarInfo = None
        self.tintAvatarTas = {}
        self.delFenShenTintEffect()
        mdData = MD.data.get(self.charType, {})
        if mdData.get('energy') == 1:
            gameglobal.rds.ui.bossEnergy.hideUI(self.id)
        if mdData.get('groupMonster') == 1:
            gameglobal.rds.ui.monsterBlood.removeMonster(self.id)
        if mdData.get('needFightBlood'):
            gameglobal.rds.ui.fightObserve.removeMonster(self)
        self.delTrapEvent()
        if getattr(self, 'fallenRedGuardFlag', None):
            gameglobal.rds.ui.killFallenRedGuardRank.leaveMonster(self)

    def _onLoadAvatarConfig(self, avatarInfo):
        if not self.inWorld:
            return
        avatarConfig = avatarInfo.get('avatarConfig', '')
        self.avatarConfig = avatarConfig
        self.avatarInfo = avatarInfo
        self.weaponState = gametypes.WEAPON_HANDFREE
        self.realPhysique.sex = avatarInfo.get('sex', const.SEX_MALE)
        self.afterEnterWorld()

    def afterEnterWorld(self):
        self.inFly = BigWorld.player().inFly
        self.initYaw = self.yaw
        if self.isOnlyClient:
            self.filter = BigWorld.ClientFilter()
            self.filter.applyDrop = True
        else:
            self.filter = BigWorld.AvatarDropFilter()
        self.modelServer.bodyModel = self.model
        clientcom.fetchTintEffectsContents(self.id, self.afterSetTintEffects)

    def afterSetTintEffects(self, ownerId, tintAvatarTas, tintAvatarName, tintEffects):
        if not self.inWorld:
            return
        clientcom.tintSectionsToCache(self, tintAvatarTas, tintAvatarName, tintEffects)
        modelId = 0
        if self.fenshenId:
            sfdData = SFD.data.get(self.fenshenId, {})
            if self.physique.sex == const.SEX_MALE:
                modelId = sfdData.get('modelId', 24658)
            else:
                modelId = sfdData.get('modelId', 24657)
        if not modelId:
            self.modelServer.bodyUpdate()
            self.modelServer.weaponUpdate()
        else:
            clientcom.fetchModel(gameglobal.URGENT_THREAD, self.afterSimpleModelFinish, modelId)
        self.tintAvatarTas = {}

    def afterSimpleModelFinish(self, model):
        if not self.inWorld:
            return
        if not model:
            return
        self.fashion.setupModel(model)
        self.noSelected = True
        self.setTargetCapsUse(not self.noSelected)
        self.addFenShenTintEffect(self.allModels)
        sfdData = SFD.data.get(self.fenshenId, {})
        bornFormPlayer = sfdData.get('bornFormPlayer', False)
        scale = sfdData.get('scale', 1.5)
        self.model.scale = (scale, scale, scale)
        callback = self.destoryMySelf
        if bornFormPlayer:
            callback = None
            flySpeed = sfdData.get('flySpeed', 0.0)
            if flySpeed <= 0.0:
                flyTime = sfdData.get('flyTime', 1.0)
                dist = self.destPosition.distTo(self.position)
                flySpeed = dist / flyTime
            self.seekTo(flySpeed)
        self.playBornAction(callback)

    def afterModelFinish(self):
        self.oldYaw = self.yaw
        if hasattr(self, 'resetTopLogo'):
            self.resetTopLogo()
        m = vertexMorpher.AvatarFaceMorpher(self.id)
        m.readConfig(self.avatarConfig)
        m.apply()
        if not self.isOnlyClient:
            super(AvatarMonster, self).afterModelFinish()
        else:
            self.noSelected = True
            self.setTargetCapsUse(not self.noSelected)
            self.addFenShenTintEffect(self.allModels)
            sfdData = SFD.data.get(self.fenshenId, {})
            bornFormPlayer = sfdData.get('bornFormPlayer', False)
            callback = self.destoryMySelf
            if bornFormPlayer:
                callback = None
                flySpeed = sfdData.get('flySpeed', 0.0)
                if flySpeed <= 0.0:
                    flyTime = sfdData.get('flyTime', 1.0)
                    dist = self.destPosition.distTo(self.position)
                    flySpeed = dist / flyTime
                self.seekTo(flySpeed)
            self.playBornAction(callback)
        self.addExtraTint()

    def canOutline(self):
        if self.isOnlyClient:
            return False
        return True

    def addFenShenTintEffect(self, models):
        if not self.isOnlyClient:
            return
        tintName, tintPrio, tint = self.getTintDataInfo()
        allModels = []
        if tintName:
            for model in models:
                if getattr(model, 'tintName', None) == tintName:
                    continue
                model.tintName = tintName
                allModels.append(model)

            tintalt.ta_add(allModels, tintName, [tint, BigWorld.shaderTime()], 0.0, None, False, False, self, self, tintType=tintalt.AVATARTINT)

    def delFenShenTintEffect(self):
        if not self.isOnlyClient:
            return
        tintName, tintPrio, tint = self.getTintDataInfo()
        if tintName:
            for model in self.models:
                model.tintName = None

            tintalt.ta_del(self.models, tintName, isTaAddCall=True, tintType=tintalt.AVATARTINT)

    def getTintDataInfo(self):
        tintData = SFD.data.get(self.fenshenId, {}).get('tintData', None)
        if not tintData:
            return (None, None, None)
        tintFx = tintData[0]
        tintName, tintPrio, tint = skillDataInfo.getTintDataInfo(self, tintFx)
        return (tintName, tintPrio, tint)

    def getTintId(self):
        tintData = SFD.data.get(self.fenshenId, {}).get('tintData', None)
        if not tintData:
            return -1
        tintId = tintData[0]
        return tintId

    def seekTo(self, speed):
        self.filter.seek(self.destPosition, speed, self.seekFinish)

    def seekFinish(self, su):
        self.filter.yaw = self.oldYaw
        actions = list(SFD.data.get(self.fenshenId, {}).get('castAction', []))
        if actions:
            self.fashion.playActionSequence(self.model, actions, self.destoryMySelf)
        else:
            self.destoryMySelf()

    def playBornAction(self, callback):
        if self.isOnlyClient:
            actions = list(SFD.data.get(self.fenshenId, {}).get('flyAction', []))
            if actions:
                self.fashion.playActionSequence(self.model, actions, callback)

    def destoryMySelf(self):
        BigWorld.destroyEntity(self.id)

    def _playInCombatAction(self):
        pass

    def set_inCombat(self, oldInCombat):
        if self.inCombat:
            if self.weaponState == gametypes.WEAPON_HANDFREE:
                self.switchWeaponState(gametypes.WEAPON_DOUBLEATTACH, False)
        else:
            self.switchWeaponState(gametypes.WEAPON_HANDFREE)
        super(AvatarMonster, self).set_inCombat(oldInCombat)

    def switchWeaponState(self, weaponState, haveAct = True, forceSwitch = False):
        if self.weaponState != weaponState or forceSwitch:
            self.weaponState = weaponState
            self.modelServer.refreshWeaponStateWithAct(haveAct)

    def addTint(self, tintId, allModels, duration = 0, host = None, delay = 0.0, tintType = tintalt.UNKNOWTINT, force = False):
        if tintId >= 1100:
            return
        super(AvatarMonster, self).addTint(tintId, allModels, duration, host, delay, tintType, force=force)

    def reloadModel(self):
        self.modelServer.bodyUpdateStatus = modelServer.BODY_UPDATE_STATUS_NORMAL
        clientcom.fetchTintEffectsContents(self.id, self.afterSetTintEffects)

    def afterWeaponUpdate(self, weapon):
        if not self.inWorld:
            return
        if weapon and weapon.getModels():
            self.addFenShenTintEffect(weapon.getModels())
        if getattr(self, 'hidingPower', None):
            self.resetHiding()

    def afterWearUpdate(self, wear):
        if not self.inWorld:
            return
        if getattr(self, 'hidingPower', None):
            self.resetHiding()

    def _getDieDeadActionName(self):
        data = self.getItemData()
        actGroupid = data.get('actGroupid', 0)
        if actGroupid:
            mad = MAD.data.get(actGroupid, None)
            if mad:
                dieActions = MAD.data[actGroupid].get('dieAct', None)
                deadActions = MAD.data[actGroupid].get('deadAct', None)
                if dieActions and deadActions:
                    self.dieActIndex = random.randint(0, len(dieActions) - 1)
                    return (dieActions[self.dieActIndex], deadActions[self.dieActIndex])
        return (self.fashion.getDieActionName(), self.fashion.getDeadActionName())

    def _getSummonActionName(self):
        data = self.getItemData()
        actGroupid = data.get('actGroupid', 0)
        if actGroupid:
            mad = MAD.data.get(actGroupid, None)
            if mad:
                summonActions = MAD.data[actGroupid].get('summonAct', None)
                if summonActions:
                    if self.dieActIndex < len(summonActions):
                        return summonActions[self.dieActIndex]
                    return summonActions[0]
        return self.fashion.getSummonActionName()

    def getSkillEffectLv(self):
        lv = super(AvatarMonster, self).getSkillEffectLv()
        lv = self.getClanWarEffectLv(lv)
        return lv

    def getBeHitEffectLv(self):
        lv = super(AvatarMonster, self).getBeHitEffectLv()
        lv = self.getClanWarEffectLv(lv)
        return lv

    def getBuffEffectLv(self):
        lv = super(AvatarMonster, self).getBuffEffectLv()
        lv = self.getClanWarEffectLv(lv)
        return lv

    def getEquipEffectLv(self):
        lv = super(AvatarMonster, self).getEquipEffectLv()
        lv = self.getClanWarEffectLv(lv)
        return lv

    def getBasicEffectLv(self):
        lv = super(AvatarMonster, self).getBasicEffectLv()
        lv = self.getClanWarEffectLv(lv)
        return lv

    def getEffectLv(self):
        if getattr(self, 'isOnlyClient', False):
            return BigWorld.player().getEffectLv()
        lv = super(AvatarMonster, self).getEffectLv()
        return lv

    def chatToViewMsg(self, msg, duration):
        if not self.inWorld:
            return
        if msg:
            BigWorld.player().chatToNPC(self.roleName, msg, self.id, duration)

    def onTargetCursor(self, enter):
        if self.isOnlyClient:
            return
        super(AvatarMonster, self).onTargetCursor(enter)
