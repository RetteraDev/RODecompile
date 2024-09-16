#Embedded file name: /WORKSPACE/data/entities/client/summonedavatarmonster.o
import random
import copy
import BigWorld
import gametypes
import gameglobal
import commcalc
import clientcom
import const
from SummonedBeast import SummonedBeast
from helpers import fashion
from helpers import modelServer
from helpers import vertexMorpher
from helpers import tintalt
from helpers import modelRobber
from data import monster_data as MD
from data import monster_action_data as MAD

class SummonedAvatarMonster(SummonedBeast):
    IsMonster = False
    IsSummonedBeast = True
    IsSummoned = True
    IsSummonedAvatarMonster = True

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
        super(SummonedAvatarMonster, self).__init__()
        self.bufActState = None
        self.buffModelScale = None
        self.buffIdModelScale = None
        self.weaponState = gametypes.WEAPON_HANDFREE
        self.inWeaponCallback = None
        self.avatarInfo = None

    def isAvatarMonster(self):
        return True

    def weaponInHandState(self):
        return self.weaponState

    def isGuarding(self):
        return self.inCombat

    def isShowFashion(self):
        return not not commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_FASHION)

    def __checkAspectPhysique(self):
        if self.aspect.body and self.aspect.hand and self.physique.bodyType:
            return True
        return False

    def enterWorld(self):
        self.modelServer = modelServer.AvatarMonsterModelServer(self)
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.playBossMusic(True)
        if MD.data.get(self.charType, {}).get('groupMonster') == 1:
            gameglobal.rds.ui.monsterBlood.addMonster(self.id, self.roleName, self.hp, self.mhp)
            if gameglobal.rds.ui.monsterBlood.mediator == None:
                gameglobal.rds.ui.monsterBlood.show()
        if MD.data.get(self.charType, {}).get('needFightBlood'):
            gameglobal.rds.ui.fightObserve.addMonster(self)
            if gameglobal.rds.ui.fightObserve.monsterBloodMediator == None:
                gameglobal.rds.ui.fightObserve.showMonsterBlood()
        if not (self.hideNpcId and modelRobber.getInstance().tryRobAvatarModel(self)):
            self.modelServer.setUrgent(True)
            if self.__checkAspectPhysique():
                itemData = self.getItemData()
                modelId = itemData.get('model', 0)
                if modelId > const.MODEL_AVATAR_BORDER:
                    filePath = '%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, modelId)
                    clientcom.ConfigCache.fetchConfig(filePath, self._onLoadAvatarConfig)
                else:
                    self.weaponState = gametypes.WEAPON_HANDFREE
                    if hasattr(self, 'ownerId') and self.ownerId == BigWorld.player().id:
                        if BigWorld.player()._isSchoolSwitch():
                            self.avatarConfig = BigWorld.player().realAvatarConfig
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

    def leaveWorld(self):
        super(SummonedAvatarMonster, self).leaveWorld()
        self.playBossMusic(False)
        self.avatarInfo = None
        self.tintAvatarTas = {}
        if MD.data.get(self.charType, {}).get('groupMonster') == 1:
            gameglobal.rds.ui.monsterBlood.removeMonster(self.id)
        if MD.data.get(self.charType, {}).get('needFightBlood'):
            gameglobal.rds.ui.fightObserve.removeMonster(self)

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
        self.filter = BigWorld.AvatarDropFilter()
        self.modelServer.bodyModel = self.model
        clientcom.fetchTintEffectsContents(self.id, self.afterSetTintEffects)

    def afterSetTintEffects(self, ownerId, tintAvatarTas, tintAvatarName, tintEffects):
        if not self.inWorld:
            return
        clientcom.tintSectionsToCache(self, tintAvatarTas, tintAvatarName, tintEffects)
        self.modelServer.bodyUpdate()
        self.modelServer.weaponUpdate()
        self.tintAvatarTas = {}

    def afterModelFinish(self):
        m = vertexMorpher.AvatarFaceMorpher(self.id)
        m.readConfig(self.avatarConfig)
        m.apply()
        if not getattr(self, 'isOnlyClient', False):
            super(SummonedAvatarMonster, self).afterModelFinish()

    def _playInCombatAction(self):
        pass

    def set_inCombat(self, oldInCombat):
        if self.inCombat:
            if self.weaponState == gametypes.WEAPON_HANDFREE:
                self.switchWeaponState(gametypes.WEAPON_DOUBLEATTACH, False)
        else:
            self.switchWeaponState(gametypes.WEAPON_HANDFREE)
        super(SummonedAvatarMonster, self).set_inCombat(oldInCombat)

    def switchWeaponState(self, weaponState, haveAct = True, forceSwitch = False):
        if self.weaponState != weaponState or forceSwitch:
            self.weaponState = weaponState
            self.modelServer.refreshWeaponStateWithAct(haveAct)

    def addTint(self, tintId, allModels, duration = 0, host = None, delay = 0.0, tintType = tintalt.UNKNOWTINT, force = False):
        if tintId >= 1100:
            return
        super(SummonedAvatarMonster, self).addTint(tintId, allModels, duration, host, delay, tintType)

    def reloadModel(self):
        self.modelServer.bodyUpdateStatus = modelServer.BODY_UPDATE_STATUS_NORMAL
        clientcom.fetchTintEffectsContents(self.id, self.afterSetTintEffects)

    def afterWeaponUpdate(self, weapon):
        if getattr(self, 'hidingPower', None):
            self.resetHiding()

    def afterWearUpdate(self, wear):
        if getattr(self, 'hidingPower', None):
            self.resetHiding()

    def _getDieDeadActionName(self):
        data = self.getItemData()
        actGroupid = data.get('actGroupid', 0)
        if actGroupid:
            mad = MAD.data.get(actGroupid, None)
            if mad:
                dieActions = MAD.data.get(actGroupid, {}).get('dieAct', None)
                deadActions = MAD.data.get(actGroupid, {}).get('deadAct', None)
                if dieActions and deadActions:
                    dice = random.randint(0, len(dieActions) - 1)
                    return (dieActions[dice], deadActions[dice])
        return (self.fashion.getDieActionName(), self.fashion.getDeadActionName())

    def getSkillEffectLv(self):
        lv = super(SummonedAvatarMonster, self).getSkillEffectLv()
        lv = self.getClanWarEffectLv(lv)
        return lv

    def getBeHitEffectLv(self):
        lv = super(SummonedAvatarMonster, self).getBeHitEffectLv()
        lv = self.getClanWarEffectLv(lv)
        return lv

    def getBuffEffectLv(self):
        lv = super(SummonedAvatarMonster, self).getBuffEffectLv()
        lv = self.getClanWarEffectLv(lv)
        return lv

    def getEquipEffectLv(self):
        lv = super(SummonedAvatarMonster, self).getEquipEffectLv()
        lv = self.getClanWarEffectLv(lv)
        return lv

    def getBasicEffectLv(self):
        lv = super(SummonedAvatarMonster, self).getBasicEffectLv()
        lv = self.getClanWarEffectLv(lv)
        return lv

    def enterTopLogoRange(self, rangeDist = -1):
        if self.getOpacityValue()[0] == gameglobal.OPACITY_HIDE:
            return
        super(SummonedAvatarMonster, self).enterTopLogoRange(rangeDist)
        if self.topLogo and self.fashion:
            h = self.getTopLogoHeight()
            if h > 0:
                self.topLogo.setHeight(h)

    def leaveTopLogoRange(self, rangeDist = -1):
        super(SummonedAvatarMonster, self).leaveTopLogoRange(rangeDist)
