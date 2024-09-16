#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/deadPlayBack.o
import BigWorld
import gametypes
import gameglobal
import const
import formula
import time
import skillDataInfo
from gameclass import SkillInfo
from gameclass import Singleton
import utils
from data import state_data as SD
from cdata import game_msg_def_data as GMDD
from data import fb_data as FD
from data import skill_general_data as SGD

class ResultFromSkill(object):

    def __init__(self):
        self.skillId = 0
        self.skillLv = 0
        self.result = None


class ResultFromState(object):

    def __init__(self):
        self.stateId = 0
        self.stateSrc = 0
        self.stateTgt = 0
        self.addHp = 0
        self.reduceHp = 0
        self.addMp = 0
        self.reduceMp = 0
        self.skillLv = 0
        self.fromSkillId = 0
        self.dmgType = 0
        self.stateSrcName = ''


def getInstance():
    return deadPlayBack.getInstance()


class deadPlayBack(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.combatMsgList = []
        self.calc = 10
        self.callBackRet = None

    def onTimer(self):
        self.removeCombatMsgNow()
        if self.isNeedDoneFB():
            self.callBackRet = BigWorld.callback(self.calc, self.onTimer)
        else:
            self.resetTimer()

    def resetTimer(self):
        if self.callBackRet:
            BigWorld.cancelCallback(self.callBackRet)
            self.combatMsgList = []
            self.callBackRet = None

    def receiveCombatResult(self, results):
        if gameglobal.gDisableDeadPlayBack:
            return
        if not self.isNeedDoneFB():
            return
        tgtId = results.tgtId
        skillId = results.skillId
        skillLv = results.skillLv
        self.takeResult(tgtId, skillId, skillLv, results.resultSet, None)

    def isNeedDoneFB(self):
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_ALL_FB):
            fbNo = formula.getFubenNo(p.spaceNo)
            if FD.data[fbNo].get('canPlayBack', 1):
                return True
            else:
                return False
        else:
            return False

    def takeResult(self, tgtId, skillId, skillLv, results, tgtPos = None, mfId = None, mfType = None, mfLv = None):
        if gameglobal.gDisableDeadPlayBack:
            return
        if not self.isNeedDoneFB():
            return
        if not self.callBackRet:
            self.callBackRet = BigWorld.callback(self.calc, self.onTimer)
        if utils.isMonsterSkill(skillId):
            skillLv = const.MONSTER_SKILL_LV
        skillLv = min(const.MAX_SKILL_LEVEL, skillLv)
        skillData = SGD.data.get((skillId, skillLv), {})
        if not skillData:
            return
        rfs = ResultFromSkill()
        rfs.skillId = skillId
        rfs.skillLv = skillLv
        rfs.results = results
        for result in results:
            rfs = ResultFromSkill()
            rfs.skillId = skillId
            rfs.skillLv = skillLv
            rfs.result = result
            for item in rfs.result.results:
                item.srcRole = self._getTgtName(item.srcId)

            p = BigWorld.player()
            if result.eid == p.id:
                self.addCombatData(rfs)

    def takeResultFromState(self, stateId, stateSrc, stateTgt, addHp, reduceHp, addMp, reduceMp, fromSkillId, stateLv, dmgType):
        if gameglobal.gDisableDeadPlayBack:
            return
        if not self.isNeedDoneFB():
            return
        if not self.callBackRet:
            self.callBackRet = BigWorld.callback(self.calc, self.onTimer)
        result = ResultFromState()
        result.stateId = stateId
        result.stateSrcName = self._getTgtName(stateSrc)
        result.stateSrc = stateSrc
        result.stateTgt = stateTgt
        result.addHp = addHp
        result.reduceHp = reduceHp
        result.addMp = addMp
        result.reduceMp = reduceMp
        result.fromSkillId = fromSkillId
        result.dmgType = dmgType
        result.skillLv = stateLv
        p = BigWorld.player()
        if result.stateTgt == p.id:
            self.addCombatData(result)

    def addCombatData(self, result):
        currentTime = time.time()
        self.combatMsgList.append({'currentTime': currentTime,
         'result': result})
        self.removeCombatMsgNow()

    def doCalcData(self):
        if gameglobal.gDisableDeadPlayBack:
            return
        if not self.isNeedDoneFB():
            return
        BigWorld.callback(0.2, self._doCalcData)

    def _doCalcData(self):
        msgLen = len(self.combatMsgList)
        i = msgLen
        lastHit = None
        totalAddHp = 0
        totalReduceHp = 0
        totalAddHpPerson = {}
        totalReduceHpPerson = {}
        maxReduceHp = 0
        maxReduceResult = None
        msgList = []
        while i > 0:
            i = i - 1
            combatResult = self.combatMsgList[i]['result']
            happenedTime = self.combatMsgList[i]['currentTime']
            battleMsgs = self.analysisResult(combatResult)
            msgList.append((happenedTime, battleMsgs))
            if battleMsgs != None:
                for battleMsg in battleMsgs:
                    if battleMsg[5] > 0:
                        totalReduceHp = totalReduceHp + battleMsg[5]
                        if totalReduceHpPerson.has_key(battleMsg[0]):
                            totalReduceHpPerson[battleMsg[0]] = totalReduceHpPerson[battleMsg[0]] + battleMsg[5]
                        if lastHit == None:
                            lastHit = battleMsg
                        skillID = battleMsg[9]
                        if skillID > 0:
                            skillLv = battleMsg[10]
                            skillInfo = SkillInfo(skillID, skillLv)
                            threatProportion = skillInfo.getSkillData('threatProportion', 1)
                        else:
                            threatProportion = 1
                        if battleMsg[5] * threatProportion > maxReduceHp:
                            maxReduceHp = battleMsg[5] * threatProportion
                            maxReduceResult = battleMsg
                    if battleMsg[6] > 0:
                        totalAddHp = totalAddHp + battleMsg[6]
                        if totalAddHpPerson.has_key(battleMsg[0]):
                            totalAddHpPerson[battleMsg[0]] = totalAddHpPerson[battleMsg[0]] + battleMsg[6]
                        else:
                            totalAddHpPerson[battleMsg[0]] = battleMsg[6]

        p = BigWorld.player()
        msg = []
        msg.append(totalReduceHp)
        msg.append(totalAddHp)
        msg.append(lastHit)
        msg.append(maxReduceResult)
        msg.append(msgList)
        gameglobal.rds.ui.fbDeadData.getMsg(msg)
        if msgLen > 0 and lastHit is not None:
            roleNameList = []
            for key in p.members:
                if p.members[key].get('roleName', '') != p.realRoleName and p.members[key].get('isOn', ''):
                    roleNameList.append(p.members[key].get('roleName', ''))

            if len(roleNameList) > 0:
                p.cell.getTeamEquipment(roleNameList)
            else:
                p.resTeamEquipment(p.combatScoreList[const.COMBAT_SCORE])
        self.combatMsgList = []

    def showMsg(self, titleID, skillResult):
        p = BigWorld.player()
        if skillResult:
            p.showGameMsg(titleID, ())
            if skillResult[13] == 0:
                if skillResult[1][1] != None and skillResult[1][1] != '':
                    p.showGameMsg(GMDD.data.COMBAT_MSG_WHOS_WHO_CAST, (skillResult[1][1], skillResult[1][0], skillResult[4]))
                else:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_WHO_CAST, (skillResult[1][0], skillResult[4]))
            elif skillResult[1][1] != None and skillResult[1][1] != '':
                p.showGameMsg(GMDD.data.COMBAT_MSG_WHOS_WHO_RECAST, (skillResult[1][1], skillResult[1][0], skillResult[4]))
            else:
                p.showGameMsg(GMDD.data.COMBAT_MSG_WHO_RECAST, (skillResult[1][0], skillResult[4]))
            per = round(float(skillResult[5]) * 100.0 / p.mhp)
            p.showGameMsg(GMDD.data.COMBAT_MSG_COST_DMG, (skillResult[5], per))
            if skillResult[13] == 0:
                skillID = skillResult[9]
                skillLv = skillResult[10]
                if skillID != -1:
                    skillInfo = SkillInfo(skillID, skillLv)
                    skillStrategy = skillInfo.getSkillData('skillStrategy', '')
                    if skillStrategy:
                        p.showGameMsg(GMDD.data.COMBAT_MSG_SKILL_STRATEGY, skillStrategy)
                    else:
                        p.showGameMsg(GMDD.data.COMBAT_MSG_SKILL_NO_STRATEGY, ())
                else:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_SKILL_NO_STRATEGY, ())
            else:
                p.showGameMsg(GMDD.data.COMBAT_MSG_SKILL_RECAST_STRATEGY, ())

    def _analysisCommonResult(self, combatResult):
        if combatResult.skillId != -1:
            skillId = combatResult.skillId
            skillInfo = SkillInfo(skillId, combatResult.skillLv)
            skillName = skillDataInfo.getSkillName(skillInfo)
            skillData = skillDataInfo.ClientSkillInfo(skillId, combatResult.skillLv, 0)
            icon = skillData.getSkillData('icon', None)
        else:
            skillName = const.COMBAT_NORMAL_ATTACK
            icon = -1
            skillId = combatResult.skillId
        battleMsgs = []
        if combatResult.result.results:
            for item in combatResult.result.results:
                currentAllDmg = 0
                currentHealHp = 0
                for dmg in item.dmgs:
                    currentAllDmg = currentAllDmg + dmg

                currentHealHp = item.hps
                if item.ars == gametypes.DMGPOWER_CRIT:
                    powerDesc = const.COMBAT_MSG_CRITAL
                else:
                    powerDesc = const.COMBAT_MSG_NORMAL
                dmgSource = item.dmgSource
                dmgTypeName = const.COMBAT_MSG_MAG
                srcRole = item.srcRole
                tgtRole = self._getTgtName(combatResult.result.eid)
                battleMsgs.append((item.srcId,
                 srcRole,
                 combatResult.result.eid,
                 tgtRole,
                 skillName,
                 currentAllDmg,
                 currentHealHp,
                 0,
                 icon,
                 skillId,
                 combatResult.skillLv,
                 powerDesc,
                 dmgTypeName,
                 dmgSource))

        return battleMsgs

    def analysisResult(self, combatResult):
        if isinstance(combatResult, ResultFromState):
            return self._analysisStateResult(combatResult)
        else:
            return self._analysisCommonResult(combatResult)

    def _analysisStateResult(self, combatResult):
        srcRole = combatResult.stateSrcName
        tgtRole = self._getTgtName(combatResult.stateTgt)
        stateData = SD.data.get(combatResult.stateId, {})
        stateName = stateData.get('name', '')
        reduceHp = combatResult.reduceHp
        addHp = combatResult.addHp
        iconId = SD.data.get(combatResult.stateId, {}).get('iconId', '')
        dmgTypeName = const.COMBAT_MSG_MAG
        powerDesc = const.COMBAT_MSG_NORMAL
        if combatResult.dmgType == gametypes.DMGTYPE_HP_STATE_PHYSICS:
            dmgTypeName = const.COMBAT_MSG_PHY
        else:
            dmgTypeName = const.COMBAT_MSG_MAG
        return [(combatResult.stateSrc,
          srcRole,
          combatResult.stateTgt,
          tgtRole,
          stateName,
          reduceHp,
          addHp,
          1,
          iconId,
          combatResult.fromSkillId,
          combatResult.skillLv,
          powerDesc,
          dmgTypeName,
          0)]

    def _getTgtName(self, tgtId):
        tgt = BigWorld.entities.get(tgtId)
        p = BigWorld.player()
        if tgt:
            tgtOwnerRole = ''
            tgtRole = tgt.id == p.id and const.YOU or tgt.roleName
            if tgt.IsSummonedBeast:
                owner = BigWorld.entities.get(tgt.ownerId)
                if owner:
                    tgtOwnerRole = owner.roleName
            if hasattr(tgt, 'monsterStrengthType'):
                if tgt.monsterStrengthType in gametypes.MONSTER_BOSS_TYPE:
                    tgtRole = tgtRole + '(Boss)'
            return (tgtRole, tgtOwnerRole)
        else:
            return ('', '')

    def removeCombatMsgNow(self):
        currentTime = time.time()
        self.combatMsgList = filter(lambda x: currentTime - x['currentTime'] <= self.calc, self.combatMsgList)
