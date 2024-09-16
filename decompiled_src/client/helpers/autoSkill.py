#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/autoSkill.o
import BigWorld
import gamelog
import gameglobal
import logicInfo
import gametypes
import skillDataInfo
from gameclass import SkillInfo
from callbackHelper import Functor
from data import school_data as SD
from data import zaiju_data as ZD
AUTOSKILL_INTERVAL = 0.9
ATUOSKILL_TYPE_NONE = 0
AUTOSKILL_TYPE_MOUSE = 1
AUTOSKILL_TYPE_KEYBOARD = 2

class AutoSkillMgr(object):

    def __init__(self, player):
        self.timer = None
        self.skillMacroTimer = None
        self.target = None
        self.player = player
        data = SD.data.get(self.player.school, {})
        self.skillId = data.get('autoSkill', 0)
        self.skillMacroId = data.get('autoSkillMacroId', 0)
        self.dist = data.get('autoSkillDist', 4)
        self.inteval = None
        self.mode = ATUOSKILL_TYPE_NONE

    def init(self, oldZaijuId = 0):
        if oldZaijuId and self.player.isInBfDota():
            autoSkillId, autoSkilllv = ZD.data.get(oldZaijuId, {}).get('skills', [])[0]
            self.player.skills.pop(autoSkillId, None)
        data = SD.data.get(self.player.school, {})
        self.skillId = data.get('autoSkill', 0)
        self.skillMacroId = data.get('autoSkillMacroId', 0)
        self.dist = data.get('autoSkillDist', 4)

    def resetDotaZaijuAutoSkill(self, zaijuId):
        if self.player.isInBfDota():
            cfgData = ZD.data.get(zaijuId, {})
            autoSkillId, autoSkilllv = cfgData.get('skills', [])[0]
            self.skillId = autoSkillId
            self.player.skills[autoSkillId] = skillDataInfo.SkillInfoVal(autoSkillId, autoSkilllv)
            self.dist = cfgData.get('autoSkillDist', 4)

    def switchToMouseMode(self):
        self.mode = AUTOSKILL_TYPE_MOUSE

    def switchToKeyboardMode(self):
        self.mode = AUTOSKILL_TYPE_KEYBOARD

    def isMouseMode(self):
        return self.mode == AUTOSKILL_TYPE_MOUSE

    def isKeyboardMode(self):
        return self.mode == AUTOSKILL_TYPE_KEYBOARD

    def stop(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def stopSkillMacro(self):
        if self.skillMacroTimer:
            BigWorld.cancelCallback(self.skillMacroTimer)
            self.skillMacroTimer = None

    def inSkillMacroTimer(self):
        return self.skillMacroTimer != None

    def start(self):
        if self.player.checkInAutoQuest() or self.player.groupFollowAutoAttackFlag:
            self.startSkillMacro()
            return
        self.stopSkillMacro()
        target = self.player.targetLocked
        if self.player.getOperationMode() == gameglobal.ACTION_MODE:
            if self.player.inMeiHuo or self.player.inChaoFeng:
                pass
            else:
                return
        if target and target.inWorld:
            if target == self.target and self.timer:
                return
            self.target = target
            self.stop()
            self.timer = BigWorld.callback(0, Functor(self._autoAttack, True))

    def startTimer(self):
        self.stopSkillMacro()
        if gameglobal.AUTOSKILL_FLAG:
            target = self.player.targetLocked
            if self.player.getOperationMode() == gameglobal.ACTION_MODE:
                return
            if target and target.inWorld:
                if target == self.target and self.timer:
                    return
                self.target = target
                if self._checkAtuoTimer():
                    self.stop()
                    self.timer = BigWorld.callback(self.inteval, self._autoAttack)

    def startSkillMacro(self):
        target = self.player.targetLocked
        if target and target.inWorld:
            if target == self.target and self.skillMacroTimer:
                return
            self.target = target
            self.stopSkillMacro()
            self.skillMacroTimer = BigWorld.callback(0, Functor(self._autoSkillMacroAttack, True))

    def _checkAtuoTimer(self):
        target = self.player.targetLocked
        operationMode = self.player.getOperationMode()
        dist = (target.position - self.player.position).length
        skillInfoVal = self.player.skills.get(self.skillId, None)
        if not skillInfoVal:
            return False
        skillInfo = SkillInfo(self.skillId, skillInfoVal.level)
        if not self.inteval or self.player.isInBfDota():
            self.inteval = skillDataInfo.getRecoverTime(skillInfo, 0) + 0.1
        if operationMode == gameglobal.KEYBOARD_MODE and self.isKeyboardMode():
            if not self.player.isFace(target):
                gamelog.debug('autoAttack@not face target')
                return False
            if dist > self.getDistWithBodySize():
                gamelog.debug('autoAttack@target too far')
                return False
        return True

    def _checkAutoAttack(self, skillInfo):
        if not self._checkAtuoTimer():
            gamelog.debug('autoAttack@checkAtuoTimer')
            return False
        if logicInfo.commonCooldownWeaponSkill[0] + 0.9 > BigWorld.time() and logicInfo.commonCooldownWeaponSkill[2] != self.skillId:
            gamelog.debug('autoAttack@gcd block', logicInfo.commonCooldownWeaponSkill[0])
            return False
        wpSkillTypes = skillInfo.getSkillData('wpSkillType', None)
        if wpSkillTypes:
            weaponSkillTypes = (self.player.weaponTypes['leftWeapon'], self.player.weaponTypes['rightWeapon'])
            for item in weaponSkillTypes:
                if item not in wpSkillTypes:
                    gamelog.debug('autoAttack@no weapon')
                    return False

        if not skillDataInfo.checkSelfRequest(skillInfo):
            gamelog.debug('autoAttack@self check')
            return False
        return True

    def getDistWithBodySize(self):
        if self.player.targetLocked:
            return self.dist + self.player.targetLocked.getBodySize()
        else:
            return self.dist

    def _autoAttack(self, firstAttack = False):
        if self.skillId not in self.player.skills:
            return
        target = self.player.targetLocked
        skillLv = self.player.skills[self.skillId].level
        skillInfo = SkillInfo(self.skillId, skillLv)
        if not self.inteval or self.player.isInBfDota():
            self.inteval = skillDataInfo.getRecoverTime(skillInfo, 0) + 0.1
        noTarget = skillInfo.getSkillData('noTgt', 0)
        operationMode = self.player.getOperationMode()
        if not (target and target.inWorld):
            gamelog.debug('autoAttack@target leave world')
            self.timer = None
            return
        if target != self.target:
            gamelog.debug('autoAttack@target changed')
            self.timer = None
            return
        if not self.player.isEnemy(target):
            gamelog.debug("autoAttack@target can\'t be attack")
            self.timer = None
            return
        if hasattr(target, 'life') and target.life == gametypes.LIFE_DEAD:
            gamelog.debug('autoAttack@target is dead')
            self.timer = None
            return
        canAttack = self._checkAutoAttack(skillInfo)
        if canAttack:
            if target:
                if not self.player.isFace(target):
                    gamelog.debug('autoAttack@face to target')
                    self.player.faceTo(target)
            if noTarget and operationMode == gameglobal.MOUSE_MODE or operationMode == gameglobal.KEYBOARD_MODE and self.isMouseMode():
                realDist = self.player.position.distTo(target.position)
                if realDist > self.getDistWithBodySize():
                    gamelog.debug('autoAttack@chase to target')
                    self.player.chaseEntity(target, self.dist - 1)
                    canAttack = False
        self.player.useSkillByKeyDown(True, skillInfo) if canAttack else None
        if not (firstAttack and not canAttack) and not (not gameglobal.AUTOSKILL_FLAG and self.isKeyboardMode()):
            self.timer = BigWorld.callback(self.inteval, self._autoAttack)
        else:
            self.timer = None

    def _autoSkillMacroAttack(self, firstAttack = False):
        target = self.player.targetLocked
        if not (target and target.inWorld):
            self.skillMacroTimer = None
            return
        inAutoQuest = self.player.checkInAutoQuest()
        if target != self.target:
            if inAutoQuest and hasattr(target, 'charType') and target.charType in self.player.getQuestSimpleFindPosNeedMonsterIdList() or self.player.groupFollowAutoAttackFlag:
                self.target = target
        if target != self.target:
            self.skillMacroTimer = None
            return
        if not self.player.isEnemy(target):
            self.skillMacroTimer = None
            return
        if hasattr(target, 'life') and target.life == gametypes.LIFE_DEAD:
            self.skillMacroTimer = None
            return
        if self.player.inFly and self.player.stateMachine.checkCloseWingFly():
            self.player.leaveWingFly()
        if target and not self.player.isFace(target):
            self.player.faceTo(target)
        canAttack = inAutoQuest or self.player.groupFollowAutoAttackFlag
        if canAttack:
            realDist = self.player.position.distTo(target.position)
            if realDist > self.getDistWithBodySize():
                self.player.chaseEntity(target, self.dist - 1)
                canAttack = False
        if canAttack:
            macroList = gameglobal.rds.ui.skillMacroOverview.getInforFromTemplateId(self.skillMacroId)
            gameglobal.rds.ui.skillMacroOverview.executeCommandStart(macroList, True, True, autoAttack=True)
        if canAttack or self.player.groupFollowAutoAttackFlag:
            self.skillMacroTimer = BigWorld.callback(0.15, self._autoSkillMacroAttack)
        else:
            self.skillMacroTimer = None

    def getTarget(self):
        if not self.player.groupHeaderTargets:
            return None
        targetId = self.player.groupHeaderTargets[-1]
        target = BigWorld.entity(targetId)
        if not target or not target.inWorld:
            for targetId in self.player.groupHeaderTargets:
                target = BigWorld.entity(targetId)
                if target and target.inWorld:
                    return target

        else:
            return target

    def release(self):
        self.stop()
        self.target = None
        self.skillId = None
        self.dist = None
        self.player = None
        self.inteval = None
        self.mode = ATUOSKILL_TYPE_NONE
