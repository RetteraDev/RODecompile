#Embedded file name: /WORKSPACE/data/entities/client/summonedbeast.o
import BigWorld
import utils
import gameglobal
import gametypes
import copy
from Monster import Monster
from helpers import action
from data import pet_skill_data as PSD
from data import summon_beast_data as SBD

class SummonedBeast(Monster):
    IsMonster = False
    IsSummonedBeast = True
    IsSummoned = True

    def __init__(self):
        super(SummonedBeast, self).__init__()
        self.applyTints = []
        self.petSkills = {}

    def getItemData(self):
        itemData = super(SummonedBeast, self).getItemData()
        sbData = copy.copy(itemData)
        sbAppData = self.getSBAppearanceData()
        sbData.update(sbAppData)
        return sbData

    def initAppearanceBornActionName(self):
        sbAppData = self.getSBAppearanceData()
        if sbAppData and sbAppData.has_key('bornActionName'):
            self.bornActionName = sbAppData['bornActionName']

    def getSBAppearanceData(self):
        ownerId = getattr(self, 'ownerId', 0)
        owner = BigWorld.entities.get(ownerId)
        if owner and hasattr(owner, 'skillAppearancesDetail'):
            return owner.skillAppearancesDetail.getSummonedBeastAppearanceData(self.beastId, self.skillId)
        return {}

    def getModelScale(self):
        sbModelScale = super(SummonedBeast, self).getModelScale()
        scale = self.getItemData().get('modelScale', None)
        if scale:
            if type(scale) == tuple:
                x, y, z = float(scale[0]), float(scale[1]), float(scale[2])
            else:
                x, y, z = float(scale), float(scale), float(scale)
            self.model.scale = (x, y, z)
            sbModelScale = (x, y, z)
        return sbModelScale

    def getOpacityValue(self):
        master = BigWorld.entities.get(self.ownerId)
        if self.isPet() and master:
            if not getattr(master, 'isRealModel', True):
                return (gameglobal.OPACITY_HIDE, False)
            return master.getOpacityValue()
        opacityVal = super(SummonedBeast, self).getOpacityValue()
        if opacityVal[0] == gameglobal.OPACITY_FULL:
            if master and master.beHide:
                return (gameglobal.OPACITY_HIDE, False)
        return opacityVal

    def getEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if hasattr(self, 'ownerId') and BigWorld.entity(self.ownerId):
                return BigWorld.entity(self.ownerId).getEffectLv()
            else:
                return getattr(BigWorld.player(), 'monsterEffectLv', gameglobal.EFFECT_MID)
        else:
            return gameglobal.EFFECT_MID

    def onUsePetSkillAfterMove(self, skillId):
        petSkillData = PSD.data.get(skillId, {})
        petAction = petSkillData.get('petAction')
        petEffect = petSkillData.get('petEffect')
        playSeq = []
        playSeq.append((petAction,
         petEffect,
         action.PET_ACTION,
         0,
         1.0,
         None))
        self.fashion.playActionWithFx(playSeq, action.PET_ACTION, None, 0, 0, 0, priority=self.getSkillEffectPriority())

    def onUpdatePetSkills(self, skillId, skillDict):
        self.petSkills[skillId] = skillDict

    def isPet(self):
        return self.mode == gametypes.SB_MODE_FOLLOW

    def enterWorld(self):
        super(SummonedBeast, self).enterWorld()
        if self.isPet() and self.ownerId == BigWorld.player().id:
            if not gameglobal.rds.ui.beastActionBar.mediator:
                gameglobal.rds.ui.beastActionBar.show()
        self.initAppearanceBornActionName()

    def onRunToMaster(self):
        runStopAction = SBD.data.get(self.beastId, {}).get('runStopAction')
        if runStopAction:
            try:
                self.model.action(runStopAction)()
            except:
                pass

    def set_petSkillState(self, old):
        if self.petSkillState == gametypes.PET_SKILL_DEFAULT and old != gametypes.PET_SKILL_DEFAULT:
            self.fashion.stopAllActions()

    def leaveWorld(self):
        super(SummonedBeast, self).leaveWorld()
        pet = BigWorld.player()._getPet()
        if not pet or pet == self:
            gameglobal.rds.ui.beastActionBar.hide()

    def getClientSkillInfo(self, skillId, skillLv):
        if getattr(self, 'ownerId', 0):
            owner = BigWorld.entity(self.ownerId)
            if owner:
                return owner.getClientSkillInfo(skillId, skillLv)
        return super(SummonedBeast, self).getClientSkillInfo(skillId, skillLv)
