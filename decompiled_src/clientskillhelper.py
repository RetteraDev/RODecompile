#Embedded file name: /WORKSPACE/data/entities/client/helpers/clientskillhelper.o
import BigWorld
import gamelog
import gametypes
import combatUtils
from callbackHelper import Functor
from data import skill_movement_data as SMD
from skillDataInfo import ClientSkillInfo
from gameclass import SkillInfo, PSkillInfo, StateInfo, CombatCreationInfo, SkillEffectInfo

class ClientSkillHelper(object):

    def __init__(self):
        super(ClientSkillHelper, self).__init__()
        self.timers = {}

    def clientUseSkill(self, owner, skillId, skilllv, tgtId = 0):
        if owner.skillPlayer:
            self.stopTimers(owner)
            owner.skillPlayer.stopSpell()
            targetId = tgtId if tgtId else owner.id
            skillInfo = SkillInfo(skillId, skilllv)
            preCast = skillInfo.getSkillData('preCast', 0)
            if preCast:
                gamelog.debug('dxk@clientUseSkill use precast skill', skillId)
                owner.skillPlayer.castSkill(targetId, skillInfo.num, skillInfo.lv, instant=True)
            tgt = owner
            if tgtId and BigWorld.entity(tgtId):
                tgt = BigWorld.entity(tgtId)
            if skillInfo.hasSkillData('tgtNowPos'):
                skillInfo.targetPosition = (tgt.position[0], tgt.position[1], tgt.position[2])
            castType = skillInfo.getSkillData('castType', gametypes.SKILL_FIRE_NORMAL)
            spellTime = combatUtils.getFinalSpellTime(owner, skillInfo)
            if castType == gametypes.SKILL_FIRE_CHARGE:
                gamelog.debug('dxk@clientUseSkill use charge skill', skillId)
                self.clientStartCharge(owner, tgt, skillId, skilllv)
                self.setTimer(1, owner, Functor(self.doCharge, owner, skillInfo, tgt))
                self.setTimer(3, owner, Functor(self.endSpell, owner, skillInfo, tgt))
            elif spellTime == 0:
                gamelog.debug('dxk@clientUseSkill use instant skill', skillId)
                self.clientCastSkillNow(owner, skillInfo, tgt, True)
                self.setTimer(3, owner, Functor(self.endSpell, owner))
            else:
                gamelog.debug('dxk@clientUseSkill use spell skill', skillId)
                self.clientStartSpell(owner, tgt, skillId, skilllv, spellTime, tgt.position)
                self.setTimer(spellTime, owner, Functor(self.clientDoSpell, owner, skillInfo, tgt))
                self.setTimer(3, owner, Functor(self.endSpell, owner))
        else:
            gamelog.error('dxk@ClientSkillHelper owner has no skillPlayerProperty')

    def clientStartSpell(self, owner, tgt, skillId, skilllv, time, targetPos, keep = 0):
        clientPlaySkillInfo = self.createDefaultPlayInfo()
        owner.skillPlayer.startSpell(tgt, skillId, skilllv, time, targetPos, keep, clientPlaySkillInfo=clientPlaySkillInfo)

    def createDefaultPlayInfo(self):
        return {'isClientPlay': True}

    def doCharge(self, owner, skillInfo, target):
        self.clientCastSkillNow(owner, skillInfo, target, False)

    def clientDoSpell(self, owner, skillInfo, target):
        self.clientCastSkillNow(owner, skillInfo, target, False)

    def endSpell(self, owner):
        owner.skillPlayer.stopSpell()

    def clientCastSkillNow(self, owner, skillInfo, target, instant):
        if not hasattr(skillInfo, 'chargeStage'):
            skillInfo.chargeStage = 0
        castType = skillInfo.getSkillData('castType', 0)
        if castType == gametypes.SKILL_FIRE_GUIDED:
            skillInfo.guideSkill = True
        moveId = skillInfo.getSkillData('moveid', 0)
        moveTime = 0
        clientPlaySkillInfo = self.createDefaultPlayInfo()
        if moveId:
            moveParam = (SMD.data.get(moveId, {}).get('clientRefId', None), None, None)
            clientPlaySkillInfo.update({'moveId': moveId,
             'moveTime': moveTime,
             'moveParam': moveParam})
        owner.skillPlayer.castSkill(target.id, skillInfo.num, skillInfo.lv, damageResult=None, instant=instant, moveId=moveId, moveTime=moveTime, clientPlaySkillInfo=clientPlaySkillInfo)

    def clientStartCharge(self, owner, target, skillId, skilllv):
        clientPlaySkillInfo = self.createDefaultPlayInfo()
        owner.skillPlayer.startCharge(target, skillId, skilllv, clientPlaySkillInfo=clientPlaySkillInfo)

    def stopTimers(self, owner):
        if self.timers.has_key(owner):
            for timer in self.timers[owner]:
                if timer:
                    BigWorld.cancelCallback(timer)

            self.timers[owner] = []

    def setTimer(self, time, owner, func):
        if not self.timers.has_key(owner):
            self.timers[owner] = []
        self.timers[owner].append(BigWorld.callback(time, func))


skillHelperInst = None

def getInstance():
    global skillHelperInst
    if skillHelperInst:
        return skillHelperInst
    else:
        skillHelperInst = ClientSkillHelper()
        return skillHelperInst
