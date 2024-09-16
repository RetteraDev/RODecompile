#Embedded file name: /WORKSPACE/data/entities/client/helpers/impskillplayercue.o
import BigWorld
import combatProto
import gamelog
import gameglobal
import utils
from callbackHelper import Functor

class ImpSkillPlayerCue(object):

    def parseActionCue(self, action):
        self.castActionCue = []
        result = action.haveCue(2)
        if result != None:
            gamelog.debug('zf:actionCueDebug cast action have cue:', result)
            for res in result:
                delayTime = res[0]
                data = res[1]
                for i in data:
                    if i[0] == 'e':
                        self.useAttackPoint = True
                        hitPercent = i[1:]
                        self.castActionCue.append((delayTime, int(hitPercent)))

        else:
            gamelog.error('zf:Warning, can not find cue in cast action ')
        self.castCurveCue = []
        result = action.haveCue(18)
        if result != None:
            for res in result:
                delayTime = res[0]
                data = res[1]
                for i in data:
                    val = i.split(':')
                    try:
                        offset = ''
                        if len(val) >= 6:
                            offset = val[5]
                        cordOffset = str(offset).split(',')
                        self.castCurveCue.append((delayTime, (int(val[0]),
                          float(val[1]),
                          float(val[2]),
                          str(val[3]),
                          int(val[4]),
                          cordOffset)))
                        gamelog.debug('castCurveCue', self.castCurveCue, cordOffset)
                    except:
                        raise Exception('@PGF:parseActionCue error for setting cue %s' % (action.name,))

            self.castCurveCue.sort(lambda x, y: cmp(x[0], y[0]))

    def getDamageCount(self, damageResult):
        count = 0
        if not damageResult:
            return count
        if len(damageResult) < 1:
            return count
        for resultSet in damageResult:
            if resultSet.eid != self.owner:
                count = count + 1

        return count

    def processDamageByAttackPoint(self, skillInfo, clientSkillInfo):
        if not skillInfo:
            skillID = self.skillID
        else:
            skillID = skillInfo.num
        self.useAttackPoint = False
        parent = BigWorld.entity(self.owner)
        if parent == None:
            return
        if not self.damageResult.has_key(skillID) or not self.damageResult[skillID]:
            return
        damageResult = self.damageResult[skillID].pop(0)
        beAttackNum = self.getDamageCount(damageResult)
        for resultSet in damageResult:
            ent = BigWorld.entity(resultSet.eid)
            if ent != None:
                damageSum = 0
                hpSum = 0
                for pair in resultSet.results:
                    damageSum += sum(pair.dmgs)
                    hpSum += pair.hps

                damageLeft = damageSum
                hpLeft = hpSum
                l = len(self.castActionCue)
                for i in xrange(l):
                    t = self.castActionCue[i]
                    hitNum = damageSum * t[1] / 100
                    hpNum = hpSum * t[1] / 100
                    if i == l - 1:
                        hitNum = damageLeft
                        hpNum = hpLeft
                    damageLeft -= hitNum
                    hpLeft -= hpNum
                    BigWorld.callback(t[0], Functor(self._realAttackPoint, beAttackNum, hitNum, hpNum, resultSet, skillInfo, clientSkillInfo, None, i))

            else:
                gamelog.error("zf119:ERROR:can\'t find entity id ", resultSet.eid)

        self.castActionCue = []

    def _realAttackPoint(self, beAttackNum, hitNum, hpNum, damageData, skillInfo, clientSkillInfo, strHitNodeName = None, attackNum = 0):
        if not damageData:
            return
        ent = BigWorld.entity(damageData.eid)
        parent = BigWorld.entity(self.owner)
        resultSet = combatProto.PBResultSet(damageData.eid)
        resultSet.results = []
        resultSet.moveId = damageData.moveId
        resultSet.moveTime = damageData.moveTime
        resultSet.moveParam = damageData.moveParam
        resultSet.kill = damageData.kill
        resultSet.controllStateData = []
        resultSet.realDmg = damageData.realDmg
        if damageData.controllStateData:
            for v in damageData.controllStateData:
                resultSet.controllStateData.append(v)

        if damageData.results:
            oldResult = damageData.results[0]
            result = combatProto.PBResult()
            result.srcId = oldResult.srcId
            result.dmgSource = oldResult.dmgSource
            result.dmgSourceId = oldResult.dmgSourceId
            result.dmgs = [hitNum]
            result.hps = hpNum
            result.mps = oldResult.mps
            result.eps = oldResult.eps
            result.ars = oldResult.ars
            result.seId = oldResult.seId
            result.damageAbsorb = oldResult.damageAbsorb
            result.healAbsorb = oldResult.healAbsorb
            resultSet.results.append(result)
        if ent:
            playCritCamShake = utils.isResultCrit(resultSet)
            extInfo = {gameglobal.CRIT_CAM_SHAKE: playCritCamShake}
            extInfo[gameglobal.FIRST_IN_SPLIT] = True if attackNum == 0 else False
            ent.disturbSkillDamage(beAttackNum, parent, resultSet, skillInfo, clientSkillInfo, False, extInfo, True, strHitNodeName)
