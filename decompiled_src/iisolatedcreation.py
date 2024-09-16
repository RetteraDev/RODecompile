#Embedded file name: /WORKSPACE/data/entities/client/iisolatedcreation.o
import BigWorld
import gametypes
import gamelog
import combatProto
import const
from iCreation import ICreation
from sfx import attackEffect
from data import creation_client_data as CCD
from data import isolated_creation_data as ICD

class IIsolatedCreation(ICreation):
    IsIsolatedCreation = True
    IsCombatCreation = False

    def __init__(self):
        self.data = dict(CCD.data.get(self.cid, {}))
        if ICD.data.has_key(self.cid):
            self.data.update(ICD.data.get(self.cid, {}))
        super(IIsolatedCreation, self).__init__()

    def initCreationData(self):
        self.data = dict(CCD.data.get(self.cid, {}))
        if ICD.data.has_key(self.cid):
            self.data.update(ICD.data.get(self.cid, {}))

    def mfResultPB(self, bytes):
        self.mfResult(*combatProto.mfResultProtoClient(bytes))

    def mfResult(self, mfId, mfType, lv, results, srcSkillId, srcSkillLv, rPosList):
        gamelog.debug('jorsef: get static isolated creation data:', mfId, mfType, lv, results, srcSkillId, srcSkillLv)
        for resultSet in results:
            host = None
            beAttack = BigWorld.entity(resultSet.eid)
            if not beAttack or not beAttack.inWorld:
                return
            for pair in resultSet.results:
                host = BigWorld.entity(pair.srcId)
                beAttack.damage(host, pair.dmgs, pair.damageAbsorb, pair.mps, pair.ars)
                if pair.hps:
                    beAttack.damage(host, (pair.hps,), [], pair.mps, gametypes.UI_BE_HEAL)
                beAttack.beHit(host, (sum(pair.dmgs), pair.ars))
                pair.dmgs = ()

            if resultSet.kill:
                beAttack.die(host)
                if host:
                    host.afterDieEffect(beAttack)
            isDmg, isHeal = attackEffect.getDmgHeal(resultSet)
            if isDmg:
                triggerHitEffect = self.data.get('triggerHitEffect', None)
                attackEffect.playTriggerHitEffect(beAttack, self, triggerHitEffect)
            elif isHeal:
                triggerHitEffect = self.data.get('triggerHitHealEffect', None)
                attackEffect.playTriggerHitEffect(beAttack, self, triggerHitEffect)

        if srcSkillId <= 0:
            srcSkillId = const.ISOLATED_CREATEION_MOVE_SKILL_ID
            srcSkillLv = 10
        skillInfo = self.getSkillInfo(srcSkillId, srcSkillLv)
        clientSkillInfo = self.getClientSkillInfo(srcSkillId, srcSkillLv)
        self.skillPlayer.mfProcessMoveDamage(skillInfo, clientSkillInfo, results)

    def canOutline(self):
        return False
