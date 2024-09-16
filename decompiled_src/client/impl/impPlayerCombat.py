#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerCombat.o
from gamestrings import gameStrings
import math
import cPickle
import zlib
import time
import BigWorld
import gametypes
import gameglobal
import gamelog
import utils
import const
import keys
import formula
import skillDataInfo
import clientcom
import logicInfo
import commcalc
import relationCommon
import combatUtils
import commQuest
from guis import ui
from sMath import inRange3D, distance2D
from gameclass import SkillInfo, PSkillInfo, StateInfo, CombatCreationInfo, SkillEffectInfo
from skillDataInfo import ClientSkillInfo
from gameclass import SkillQteInfoVal
from skillEnhanceCommon import CSkillEnhanceVal
from guis import hotkey as HK
from guis import uiConst
from guis import uiUtils
from item import Item
from helpers import cellCmd
from helpers import action as ACT
from helpers import tintalt
from helpers import navigator
from gameclass import DictZipper
from callbackHelper import Functor
from sfx import cameraEffect
from sfx import keyboardEffect
from guis.messageBoxProxy import MBButton
from data import skill_panel_data as SPD
from data import sys_config_data as SCD
from data import map_config_data as MCD
from data import state_data as SD
from data import qinggong_cost_data as QCD
from data import game_msg_data as GMD
from data import item_data as ID
from data import skill_general_data as SGD
from data import duel_config_data as DCD
from data import zaiju_data as ZJD
from data import wing_world_city_data as WWCD
from cdata import pskill_skillEffect_reverse_data as PSERD
from cdata import pskill_state_reverse_data as PSTRD
from cdata import pskill_creation_reverse_data as PCRD
from cdata import pskill_reverse_data as PSRD
from cdata import game_msg_def_data as GMDD
from cdata import prop_def_data as PDD
from data import skill_enhance_data as SED
from data import quest_marker_data as QMD
import SummonedSprite

class ImpPlayerCombat(object):
    TAB_DIS_LIMIT = 80

    def beginAttack(self, target):
        self.lockTarget(target)
        self.autoSkill.switchToMouseMode()
        self.autoSkill.start()

    def useSkillCheck(self, skillInfo):
        skillId = skillInfo.num
        if self.getOperationMode() == gameglobal.MOUSE_MODE:
            entity = self.targetLocked
            if entity and entity.inWorld:
                skillTargetType, skillTargetValue = self.getSkillTargetType(skillInfo)
                if skillTargetValue:
                    if self.isEnemy(entity) and skillTargetType in (gametypes.SKILL_TARGET_FRIEND, gametypes.SKILL_TARGET_SELF_FRIEND) or self.isFriend(entity) and skillTargetType in (gametypes.SKILL_TARGET_ENERMY, gametypes.SKILL_TARGET_SELF_ENERMY) or self == entity and skillTargetType in (gametypes.SKILL_TARGET_NOT_SELF,):
                        return
                if hasattr(entity, 'life') and entity.life != gametypes.LIFE_ALIVE:
                    if self.ap.isChasing and self.ap.chasingEntity == entity:
                        self.ap.stopMove()
                if logicInfo.isSkillCooldowning(skillId):
                    self._showSkillNotReadyMsg(skillId)
                    return False
                skillMinDist, skillMaxDist = skillDataInfo.getSkillRange(skillInfo)
                if not skillMaxDist:
                    return False
                dist = self.position.distTo(entity.position)
                if dist > skillMaxDist - 1:
                    if not self.ap.isChasing and not self.ap.isKeyBoardMove():
                        self.skillId = skillId
                        self.skillLevel = skillInfo.lv
                        self.autoUseSkill = True
                        self.chaseEntity(entity, skillMaxDist - 1.0)
                        return True
                elif skillInfo.getSkillData('facePos', 0) > 0:
                    if not self.isFace(entity):
                        self.faceTo(entity, True, True)
        return False

    def canBeAttack(self, target, ignoreLive = False, ignoreTargetLive = False):
        if getattr(target, 'IsOreSpawnPoint', False) == True:
            return False
        elif target.IsCreation:
            return self.isEnemy(target)
        elif not ignoreTargetLive and hasattr(target, 'life') and target.life != gametypes.LIFE_ALIVE:
            return False
        elif not ignoreLive and self.life != gametypes.LIFE_ALIVE:
            return False
        elif not getattr(target, 'fashion', None):
            return False
        elif hasattr(target, 'getOpacityValue') and not target.getOpacityValue()[1]:
            return False
        elif utils.instanceof(target, 'Puppet'):
            return True
        elif not self.isEnemy(target):
            return False
        elif hasattr(self, 'inLiveOfGuildTournament') and self.inLiveOfGuildTournament > 0:
            return False
        elif not self.checkTempGroupFollow():
            return False
        elif not self.stateMachine.checkStatus_check(const.CT_ATTACK):
            gamelog.debug('checkStatus:faild')
            return False
        else:
            return True

    def canBeTab(self, target, ignoreLive = False, ignoreTargetLive = False):
        if not ignoreTargetLive and hasattr(target, 'life') and target.life != gametypes.LIFE_ALIVE:
            return False
        elif not ignoreLive and self.life != gametypes.LIFE_ALIVE:
            return False
        elif not getattr(target, 'fashion', None):
            return False
        if hasattr(target, 'getOpacityValue') and not target.getOpacityValue()[1]:
            qieCuoTarget = getattr(self, 'qieCuoTarget', None)
            if qieCuoTarget and self.qieCuoTarget == getattr(target, 'id', 0):
                pass
            elif getattr(target, 'inHidingReveal', None):
                pass
            else:
                return False
        if not self.isEnemy(target):
            return False
        else:
            return True

    def isEnemy(self, tgt):
        if not tgt:
            return False
        src = self
        if src.id == tgt.id:
            return False
        if not tgt.IsCombatUnit:
            return False
        if tgt.IsSummoned:
            if relationCommon._checkCannotBeAtkType(tgt.beAtkType, src):
                return False
            master = BigWorld.entities.get(tgt.ownerId)
            if master:
                tgt = master
            else:
                for data in self.members.values():
                    if tgt.ownerId == data.get('id', 0):
                        return False

        return relationCommon.isEnemy_Avatar(src, tgt)

    def isFriend(self, tgt):
        if not tgt:
            return False
        src = self
        if not tgt.IsCombatUnit:
            return False
        if tgt.IsSummoned:
            master = BigWorld.entities.get(tgt.ownerId)
            if master:
                tgt = master
        if self.id == tgt.id:
            return True
        return relationCommon.isFriend_Avatar(src, tgt)

    def getMaxTgtBodySize(self):
        if self.targetLocked and hasattr(self.targetLocked, 'bodySize'):
            return self.targetLocked.bodySize
        else:
            return const.DEFAULT_AVATAR_BODY_SIZE

    def _mlSpaceForceWithMonster(self, tgt):
        return tgt.IsAvatar and tgt._isInBianyao() or tgt.IsMonster

    def startSpell(self, targetId, skillId, skillLevel, time, targetPos, yaw):
        self.isWaitSkillReturn = False
        super(self.__class__, self).startSpell(targetId, skillId, skillLevel, time, targetPos, yaw)
        self.spellingType = self.getSkillSpellingTypeBySkill(skillId, skillLevel)

    def startCharge(self, targetId, skillId, skillLevel):
        self.isWaitSkillReturn = False
        self.isChargeKeyDown = True
        super(self.__class__, self).startCharge(targetId, skillId, skillLevel)
        gamelog.debug('jorsef: startCharge', targetId, skillId, skillLevel)
        waitingReleaseInfo = getattr(self, 'waitingReleaseInfo', {})
        chargeSkillId = waitingReleaseInfo.get('chargeSkillId', 0)
        chargeSkillLv = waitingReleaseInfo.get('chargeSkillLv', 0)
        if skillId == chargeSkillId and skillLevel == chargeSkillLv:
            self.releaseCharge()
            self.waitingReleaseInfo = {}

    def stopSpell(self, success):
        gamelog.debug('jorsef: stopSpell', self.isGuiding)
        if self.isGuiding != const.GUIDE_TYPE_NONE:
            keyboardEffect.removeGuideEffect()
        self.isWaitSkillReturn = False
        super(self.__class__, self).stopSpell(success)
        self.spellingType = ACT.S_DEFAULT
        self.isGuiding = const.GUIDE_TYPE_NONE
        if self.getOperationMode() == gameglobal.MOUSE_MODE:
            self.ap.isAutoTurnYaw = False

    def useskill(self, target = None, isDebug = False):
        gamelog.debug('@zf:useskill', self.fashion.doingActionType())
        if self.inWenQuanState:
            self.showGameMsg(GMDD.data.IN_WENQUAN_USESKILL, ())
            return
        else:
            skillInfo = self.getSkillInfo(self.skillId, self.skillLevel)
            clientSkillInfo = ClientSkillInfo(self.skillId, self.skillLevel)
            if hasattr(self, 'skillPlayer'):
                self.skillPlayer.skillKit = skillDataInfo.getSkillKit(clientSkillInfo)
                self.skillPlayer.skillStart = True
            if self.physics.isSliding:
                return
            self.mouseOptimizeNoTarget(skillInfo)
            self.actionOptimizeNoTarget(skillInfo)
            preCast = skillInfo.getSkillData('preCast', 0)
            targetLocked = None == target and self.targetLocked or target
            if preCast:
                if self.isWaitSkillReturn:
                    return False
                if commcalc.getBitDword(self.publicFlags, gametypes.FLAG_NOT_CONTROLLABLE) or commcalc.getBitDword(self.publicFlags, gametypes.FLAG_NOT_MOVABLE):
                    return
                if targetLocked:
                    targetId = targetLocked.id
                else:
                    targetId = 0
                self.skillPlayer.castSkill(targetId, self.skillId, self.skillLevel, instant=True)
                self.skillPlayer.updateSkillState(skillInfo, 0.0, 0.0, True)
            if self.getOperationMode() == gameglobal.MOUSE_MODE:
                moveMode = skillDataInfo.getCastMoveType(skillInfo)
                if self.ap.isAutoMoving and moveMode != ACT.S_BLEND:
                    self.ap.stopAutoMove()
                    self.ap.stopSeek()
            gamelog.debug('useskill', preCast)
            noTarget = skillInfo.getSkillData('noTgt', 0)
            if self.autoSkill.isKeyboardMode():
                if not gameglobal.AUTOSKILL_FLAG:
                    self.autoSkill.stop()
                elif self.skillId == self.autoSkill.skillId:
                    self.autoSkill.startTimer()
                elif not noTarget:
                    BigWorld.callback(1.0, self.autoSkill.startTimer)
            if skillDataInfo.isNeedTarget(skillInfo):
                self._cellUseSkill(self.skillId, self.skillLevel, targetLocked, isDebug)
                self.actionOptimizeForTarget(skillInfo)
            else:
                self._cellUseSkill(self.skillId, self.skillLevel, self, isDebug)
            if skillDataInfo.isGuideSkill(skillInfo):
                gameglobal.rds.ui.actionbar.addGuideEffect(self.skillId)
            gameglobal.rds.tutorial.onUseSkillEndCheck(self.skillId)
            return

    def _cellUseSkill(self, skillId, skillLv, target, isDebug = False):
        if self.skillPlayer.animateInfo:
            animateCamera, actionId, skillList = self.skillPlayer.animateInfo
            if skillId in skillList:
                try:
                    self.fashion.playAction([actionId], callback=Functor(cellCmd.useSkill, skillId, skillLv, target, isDebug))
                    gameglobal.rds.ui.actionbar.showWSShine()
                    cameraEffect.startAnimateCamera(':'.join((str(animateCamera[0]), animateCamera[1], animateCamera[2])))
                    gameglobal.rds.sound.playSound(gameglobal.SD_585)
                except:
                    cellCmd.useSkill(skillId, skillLv, target, isDebug)

            else:
                cellCmd.useSkill(skillId, skillLv, target, isDebug)
            return
        cellCmd.useSkill(skillId, skillLv, target, isDebug)

    def inNoCostAndCDSkillState(self):
        return getattr(self, 'noMpSpecialStateCnt', 0) > 0

    def mfResult(self, mfId, mfType, lv, results, srcSkillId, srcSkillLv, rPosList):
        super(self.__class__, self).mfResult(mfId, mfType, lv, results, srcSkillId, srcSkillLv, rPosList)
        self.isWaitSkillReturn = False
        self._lockClosestTarget(results)

    def guideSkillResult(self, targetId, guideSkillId, lv, results, targetPos = None):
        super(self.__class__, self).guideSkillResult(targetId, guideSkillId, lv, results, targetPos)
        self.isWaitSkillReturn = False
        self._lockClosestTarget(results)

    def skillResult(self, sr):
        gamelog.debug('zf209:PlayerAvatar sr', sr.resultSet)
        self.isWaitSkillReturn = False
        super(self.__class__, self).skillResult(sr)
        self._lockClosestTarget(sr.resultSet)

    def _lockClosestTarget(self, resultSet):
        if self.targetLocked != None:
            return
        else:
            minDist = 100
            ltEnt = None
            for result in resultSet:
                ent = BigWorld.entity(result.eid)
                if result.realDmg <= 0:
                    continue
                if ent != None and ent != self:
                    dist = self.position.flatDistTo(ent.position)
                    if dist < minDist:
                        minDist = dist
                        ltEnt = ent

            if ltEnt:
                self.lockTarget(ltEnt)
            return

    def getNearestTargetForActionPhysics(self, targetLocked):
        gameStrings.TEXT_IMPPLAYERCOMBAT_421
        entities = BigWorld.inCameraEntity(80)
        length = 1000
        retEnt = None
        for ent in entities:
            if not hasattr(ent, 'IsCombatUnit') or not ent.IsCombatUnit:
                continue
            if ent == self:
                continue
            if getattr(ent, 'noSelected', None):
                continue
            if not getattr(ent, 'fashion', None):
                continue
            if getattr(ent, 'life') == gametypes.LIFE_DEAD:
                continue
            if targetLocked == ent or self == ent:
                continue
            if not self.ap.needSelect(ent):
                continue
            le = (ent.position - self.position).length
            if le < length:
                length = le
                retEnt = ent

        return retEnt

    def selectNearAttackable(self, down, forceSelect = False):
        if down:
            return
        else:
            ents = BigWorld.inCameraEntity(80)
            if ents == None or len(ents) <= 0:
                return
            if self._isTabForbidInActionPhysics():
                return
            if gameglobal.TAB_NOT_TO_SELECT_SPRITE:
                ents = [ ent for ent in ents if not isinstance(ent, SummonedSprite.SummonedSprite) ]
            if self.getOperationMode() == gameglobal.ACTION_MODE:
                backupTarget = self.ap.backupTarget
                if backupTarget:
                    if not gameglobal.TAB_NOT_TO_SELECT_SPRITE or not isinstance(backupTarget, SummonedSprite.SummonedSprite):
                        self.lockTarget(backupTarget)
                        self.ap.onTargetFocus(backupTarget, True)
                        self.ap.backupTarget = None
                        return
                if self.targetLocked:
                    if not self.ap.lockAim and (not gameglobal.TAB_NOT_TO_SELECT_SPRITE or not isinstance(self.targetLocked, SummonedSprite.SummonedSprite)):
                        self.lockTarget(self.targetLocked)
                        self.ap.onTargetFocus(self.targetLocked, True)
                    else:
                        opTarget = self.getNearestTarget(ents)
                        if opTarget:
                            self.lockTarget(opTarget)
                            self.ap.onTargetFocus(opTarget, True)
                    return
                opTarget = self.getNearestTarget(ents)
                if opTarget:
                    self.lockTarget(opTarget)
                    self.ap.onTargetFocus(opTarget, True)
                if not forceSelect:
                    return
            else:
                ret = self.getNearestTarget(ents)
                if ret:
                    self.lockTarget(ret)
                    self.ap.onTargetFocus(ret, True)
            return

    def checkTabTargetValid(self, ent, dist):
        myPos = self.position
        if not hasattr(ent, 'IsCombatUnit') or not ent.IsCombatUnit:
            return False
        elif not self.canBeTab(ent):
            gamelog.debug('jorsef: target can not be tab', ent.id)
            return False
        elif not hasattr(ent, 'life'):
            return False
        elif ent.life == gametypes.LIFE_DEAD:
            return False
        elif ent == self:
            return False
        elif getattr(ent, 'noSelected', None):
            return False
        elif not getattr(ent, 'fashion', None):
            return False
        elif (ent.position - myPos).length > dist:
            return False
        diffYaw = self.getDiffyaw(ent)
        arc = SCD.data.get('tabTargetYaw', 120) * math.pi / 360.0
        if not (diffYaw > -arc and diffYaw < arc):
            return False
        elif not clientcom.checkAttackThrough(self.spaceID, myPos, ent.position, ent.getTopLogoHeight(), ent.getBodySize()):
            return False
        elif getattr(ent, 'IsSummonedSprite', None) and gameglobal.TAB_NOT_TO_SELECT_SPRITE:
            return False
        elif not getattr(ent, 'targetCaps', []):
            return False
        else:
            return True

    def getTargetFromCandidates(self):
        if formula.inDotaBattleField(self.mapID):
            return self.getTargetFromCandidatesByAvatar()
        else:
            return self.getTargetFromCandidatesByDis()

    def getTargetFromCandidatesByDis(self):
        num = len(self.tabTargetCandidates)
        blockDist = SCD.data.get('tabTargetDist', ImpPlayerCombat.TAB_DIS_LIMIT)
        idx = self.tabTargetIdx
        for i in xrange(idx, num):
            ent = self.tabTargetCandidates[i]
            self.tabTargetIdx = self.tabTargetIdx + 1
            if ent:
                if self.checkTabTargetValid(ent, blockDist):
                    if ent == self.targetLocked:
                        continue
                    return ent

    def getTargetFromCandidatesByAvatar(self):
        num = len(self.tabTargetCandidates)
        blockDist = SCD.data.get('tabTargetDist', ImpPlayerCombat.TAB_DIS_LIMIT)
        idx = self.tabTargetIdx
        avatarList = []
        for tabIdx in xrange(self.tabTargetIdx, num):
            ent = self.tabTargetCandidates[tabIdx]
            if getattr(ent, 'IsAvatar', False) and self.checkTabTargetValid(ent, blockDist):
                avatarList.append((tabIdx, ent))

        if avatarList:
            avatarList.sort(cmp=lambda x, y: cmp(x[1].hp, y[1].hp))
            self.tabTargetIdx = avatarList[0][0] + 1
            return avatarList[0][1]
        else:
            for i in xrange(idx, num):
                ent = self.tabTargetCandidates[i]
                self.tabTargetIdx = self.tabTargetIdx + 1
                if ent:
                    if self.checkTabTargetValid(ent, blockDist):
                        if ent == self.targetLocked:
                            continue
                        return ent

            return None

    def regenCandidates(self):
        candidates = []
        ents = BigWorld.inCameraEntity(80)
        if ents == None or len(ents) <= 0:
            return
        else:
            blockDist = SCD.data.get('tabTargetDist', ImpPlayerCombat.TAB_DIS_LIMIT)
            for ent in ents:
                if self.checkTabTargetValid(ent, blockDist):
                    candidates.append((ent, (ent.position - self.position).length))

            if candidates:
                candidates.sort(lambda x, y: cmp(x[1], y[1]))
                self.tabTargetCandidates = [ x[0] for x in candidates ]
            else:
                self.tabTargetCandidates = []
            return

    def needRegenCandidates(self):
        if self.tabTargetIdx >= len(self.tabTargetCandidates):
            return True
        now = time.time()
        if now - self.lastTabTime > SCD.data.get('tabTargetLastTime', 3):
            return True
        return False

    def getNearestTarget(self, ents):
        return self.getNearestTargetNew(ents)

    def getNearestTargetNew(self, ents):
        if self.needRegenCandidates():
            self.regenCandidates()
            self.tabTargetIdx = 0
            self.lastTabTime = time.time()
            target = self.getTargetFromCandidates()
            return target
        else:
            target = self.getTargetFromCandidates()
            if not target:
                self.regenCandidates()
                target = self.getTargetFromCandidates()
            if not target:
                target = self.targetLocked
            self.lastTabTime = time.time()
            return target

    def getNearestTargetForMeiHuo(self, ents):
        dist = 6400
        myPos = self.position
        ret = None
        blockEntity = None
        blockDist = 6400
        for ent in ents:
            if not hasattr(ent, 'IsCombatUnit') or not ent.IsCombatUnit:
                continue
            if not self.canBeTab(ent):
                gamelog.debug('jorsef: target can not be tab', ent.id)
                continue
            if not hasattr(ent, 'life'):
                continue
            if ent.life == gametypes.LIFE_DEAD:
                continue
            if ent == self:
                continue
            if getattr(ent, 'noSelected', None):
                continue
            if not getattr(ent, 'fashion', None):
                continue
            if self.targetLocked == ent:
                continue
            v = ent.position - myPos
            d = v.lengthSquared
            if d > dist:
                continue
            if clientcom.checkAttackThrough(self.spaceID, myPos, ent.position, ent.getTopLogoHeight(), ent.getBodySize()):
                dist = d
                ret = ent
            elif d < blockDist:
                blockDist = d
                blockEntity = ent

        if ret == None:
            ret = self.targetLocked
        if ret == None and blockEntity:
            ret = blockEntity
        return ret

    def getDiffyaw(self, ent):
        targetYaw = (ent.position - self.position).yaw
        if self.yaw >= 0 and targetYaw >= 0 or self.yaw < 0 and targetYaw < 0:
            diffYaw = self.yaw - targetYaw
        else:
            diffYaw = abs(self.yaw) + abs(targetYaw)
        diffYaw = abs(diffYaw)
        if diffYaw > math.pi:
            diffYaw = math.pi * 2 - diffYaw
        return diffYaw

    def _isTabForbidInActionPhysics(self):
        gamelog.debug('_isTabForbidInActionPhysics', self.getOperationMode(), self.fashion.doingActionType())
        if self.getOperationMode() == gameglobal.ACTION_MODE:
            if self.fashion.doingActionType() in [ACT.SPELL_ACTION, ACT.GUIDE_ACTION, ACT.CHARGE_ACTION]:
                return True

    def useMarkerNpc(self, markerId):
        if not self.stateMachine.checkStatus(const.CT_USE_MARKER_NPC):
            return
        else:
            markerNpcList = [ e for e in BigWorld.entities.values() if getattr(e, 'npcId', 0) == markerId ]
            markerNpc = None
            for e in markerNpcList:
                if not markerNpc or distance2D(e.position, self.position) < distance2D(markerNpc.position, self.position):
                    markerNpc = e

            if markerNpc and not self.isFace(markerNpc):
                self.faceTo(markerNpc, False, True)
                BigWorld.callback(0.5, Functor(BigWorld.player().cell.onClickItemNearMarker, markerId))
            else:
                BigWorld.player().cell.onClickItemNearMarker(markerId)
            return

    def pickNearByItems(self, isDown):
        p = BigWorld.player()
        if not self._checkTeleportCD(2, False):
            return
        else:
            movingPlatform = gameglobal.rds.ui.pressKeyF.movingPlatform
            if movingPlatform:
                if self.carrier.carrierEntId and movingPlatform.id != self.carrier.carrierEntId:
                    p.showGameMsg(GMDD.data.MULTI_CARRIER_DIFF_CARRIER_GO_BACK, ())
                    return
            gameglobal.rds.ui.dynamicFCastBar.recordHoldPressUpTime(isDown, p.getServerTime())
            if isDown:
                gameglobal.rds.ui.questTrack.showPathFindingIcon(False)
                gameglobal.rds.ui.explore.fKeyDown()
                if gameglobal.rds.ui.pickUp.mediator:
                    gameglobal.rds.ui.pickUp.onPickAllItem(None)
                    return
                if gameglobal.rds.ui.pressKeyF.type == const.F_NONE:
                    gameglobal.rds.ui.buffSkill.pressFKey()
                    return
                if p.checkCanPickAllItemsInPUBG():
                    return
                if gameglobal.rds.ui.pressKeyF.type == const.F_MARKERNPC:
                    if gameglobal.rds.ui.npcSlot.params and len(gameglobal.rds.ui.npcSlot.params):
                        markerId = gameglobal.rds.ui.npcSlot.params[0]
                        holdTime = QMD.data.get(markerId, {}).get('holdTime', 0)
                        indirectTime = QMD.data.get(markerId, {}).get('indirectTime', ())
                        if not holdTime and not indirectTime:
                            self.useMarkerNpc(markerId)
                        elif holdTime:
                            gameglobal.rds.ui.dynamicFCastBar.startHoldPress(p.getServerTime(), holdTime, markerId)
                        elif indirectTime:
                            gameglobal.rds.ui.dynamicFCastBar.startIndirectPress(p.getServerTime(), indirectTime, markerId)
                if gameglobal.rds.ui.pressKeyF.type == const.F_ORE_SPAWN_POINT:
                    if gameglobal.rds.ui.pressKeyF.oreSpawnPoint:
                        gameglobal.rds.ui.pressKeyF.oreSpawnPoint.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_DROPPEDITEM:
                    if self.checkPickItems():
                        self.pickDroppedItems()
                if gameglobal.rds.ui.pressKeyF.type == const.F_ROUND_TABLE:
                    pickNearDist = const.NPC_USE_DIST
                    selectedBox = None
                    for box in BigWorld.entities.values():
                        if utils.instanceof(box, 'RoundTable') and box.getOpacityValue()[0] == gameglobal.OPACITY_FULL and box.isLeaveWorld == False and (box.position - self.position).lengthSquared < pickNearDist * pickNearDist:
                            if not selectedBox or (box.position - self.position).lengthSquared < (selectedBox.position - self.position).lengthSquared:
                                selectedBox = box

                    if selectedBox is not None:
                        selectedBox.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_INTERACTIVE:
                    pickNearDist = SCD.data.get('interactiveObjLength', 5)
                    selectedBox = None
                    for box in BigWorld.entities.values():
                        if utils.instanceof(box, 'InteractiveObject') and box.isLeaveWorld == False and (box.position - self.position).lengthSquared < pickNearDist * pickNearDist:
                            if not selectedBox or (box.position - self.position).lengthSquared < (selectedBox.position - self.position).lengthSquared:
                                selectedBox = box

                    if selectedBox is not None:
                        selectedBox.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_NORMALNPC:
                    chooseNpc = gameglobal.rds.ui.pressKeyF.getTalkNpc()
                    if chooseNpc:
                        chooseNpc.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_TRANSPORT:
                    if p.inWingWarCity():
                        gameglobal.rds.ui.map.openMap(True, uiConst.MAP_TYPE_TRANSPORT)
                        return
                    pickNearDist = const.TRANSPORT_USE_DIST
                    transport = None
                    for t in BigWorld.entities.values():
                        if utils.instanceof(t, 'Transport') and t.isLeaveWorld == False and (t.position - self.position).lengthSquared < pickNearDist * pickNearDist:
                            if not transport or (t.position - self.position).lengthSquared < (transport.position - self.position).lengthSquared:
                                transport = t

                    if transport is not None:
                        transport.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_JIGUAN:
                    p = BigWorld.player()
                    jiguanEnt = (ent for ent in BigWorld.entities.values() if utils.instanceof(ent, 'JiGuan'))
                    candidates = [ ((p.position - jiguan.position).length, jiguan) for jiguan in jiguanEnt if not jiguan.locked and (jiguan.ownerId == 0 or jiguan.ownerId == p.id) ]
                    jiguan = min(candidates)[1] if len(candidates) > 0 else None
                    if jiguan:
                        jiguan.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_AVATAR:
                    p = BigWorld.player()
                    interactiveAvatars = gameglobal.rds.ui.pressKeyF.interactiveAvatars
                    if interactiveAvatars:
                        trapAvatar = gameglobal.rds.ui.pressKeyF.getHuntBFTrapInfo()
                        if trapAvatar:
                            p.cell.rescueBattleFieldHuntByMate(trapAvatar.id)
                        elif hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
                            dist = 10000
                            chooseAvatar = None
                            p = BigWorld.player()
                            for avatar in interactiveAvatars:
                                tempDist = (p.position - avatar.position).length
                                if tempDist < dist:
                                    dist = tempDist
                                    chooseAvatar = avatar

                            BigWorld.player().lockTarget(chooseAvatar)
                            BigWorld.player().ap.showCursor = True
                            BigWorld.player().ap._resumeCursor(True, False)
                            if chooseAvatar:
                                chooseAvatar.interactive()
                if gameglobal.rds.ui.pressKeyF.type == const.F_CLANWARCREATION or gameglobal.rds.ui.pressKeyF.type == const.F_CLANWARMARKER:
                    p = BigWorld.player()
                    p.useClanWarItem(gameglobal.rds.ui.pressKeyF.clanWarCreationId)
                if gameglobal.rds.ui.pressKeyF.type == const.F_DESTROYABLE:
                    p = BigWorld.player()
                    p.destroyClanWarBuilding(gameglobal.rds.ui.pressKeyF.clanWarCreationId)
                if gameglobal.rds.ui.pressKeyF.type == const.F_ZAIJU:
                    pickNearDist = SCD.data.get('pickUpLength', 4)
                    zaiju = None
                    for t in BigWorld.entities.values():
                        if utils.instanceof(t, 'EmptyZaiju') and t.inWorld and (t.position - self.position).lengthSquared <= pickNearDist * pickNearDist:
                            if not zaiju or (t.position - self.position).lengthSquared < (zaiju.position - self.position).lengthSquared:
                                zaiju = t

                    if zaiju is not None:
                        zaiju.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_LifeCsmItem:
                    pickNearDist = SCD.data.get('pickUpLength', 4)
                    item = None
                    for t in BigWorld.entities.values():
                        if utils.instanceof(t, 'LifeCsmItem') and t.inWorld and (t.position - self.position).lengthSquared <= pickNearDist * pickNearDist:
                            if not item or (t.position - self.position).lengthSquared < (item.position - self.position).lengthSquared:
                                item = t

                    if item is not None:
                        item.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_KISS:
                    self.wantToDoEmote(const.EMOTE_KISS_ID)
                if gameglobal.rds.ui.pressKeyF.type == const.F_TRIDE_ACTION:
                    trideSpecialAction = self.getTRideSpecialAction()
                    if trideSpecialAction:
                        self.wantToDoEmote(trideSpecialAction)
                if gameglobal.rds.ui.pressKeyF.type == const.F_MONSTER:
                    monster = getattr(gameglobal.rds.ui.pressKeyF, 'monster')
                    hunt_monster_id = DCD.data.get('hunt_monster_id', 0)
                    if monster:
                        if formula.inHuntBattleField(p.mapID) and hunt_monster_id == monster.charType:
                            p.cell.clickBattleFieldSubmitCandy(monster.id)
                        else:
                            eventIndex = getattr(monster, 'triggerEventIndex', -1)
                            if eventIndex >= 0:
                                self.cell.triggerMonsterEvent(monster.id, eventIndex)
                                if eventIndex != commQuest.getGroupActionMonsterEventIndex(monster.charType):
                                    BigWorld.callback(0.5, Functor(monster.checkFKey))
                if gameglobal.rds.ui.pressKeyF.type == const.F_GUILDBUILDINGMARKER:
                    p = BigWorld.player()
                    p.createGuildBuilding(gameglobal.rds.ui.pressKeyF.guildBuildingMarkerId)
                if gameglobal.rds.ui.pressKeyF.type == const.F_GUILDSIT:
                    p = BigWorld.player()
                    p.reqGuildSitInChair(gameglobal.rds.ui.pressKeyF.guildEntityId)
                if gameglobal.rds.ui.pressKeyF.type == const.F_GUILDTREAT:
                    p = BigWorld.player()
                    p.reqGuildTreatResident(gameglobal.rds.ui.pressKeyF.guildEntityId)
                if gameglobal.rds.ui.pressKeyF.type == const.F_BATTLE_FIELD_FLAG:
                    if gameglobal.rds.ui.pressKeyF.battleFieldFlag:
                        gameglobal.rds.ui.pressKeyF.battleFieldFlag.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_MOVING_PLATFORM:
                    if gameglobal.rds.ui.pressKeyF.movingPlatform:
                        gameglobal.rds.ui.pressKeyF.movingPlatform.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_BUSINESS_ITEM:
                    pickNearDist = SCD.data.get('pickNearQuestBoxLength', 6)
                    businessItem = None
                    for entity in BigWorld.entities.values():
                        if utils.instanceof(entity, 'BusinessItem') and entity.isLeaveWorld == False and (entity.position - self.position).lengthSquared < pickNearDist * pickNearDist:
                            if not businessItem or (entity.position - self.position).lengthSquared < (businessItem.position - self.position).lengthSquared:
                                businessItem = entity

                    if businessItem is not None:
                        businessItem.use()
                if gameglobal.rds.ui.pressKeyF.type == const.F_OCCUPY:
                    tgt = BigWorld.entities.get(gameglobal.rds.ui.pressKeyF.targetId)
                    if tgt:
                        tgt.cell.startOccupy()
                if gameglobal.rds.ui.pressKeyF.type != const.F_NONE:
                    ent = gameglobal.rds.ui.pressKeyF.getEnt()
                    if ent:
                        ent.use()
            return

    def checkPickItems(self):
        if self.isUseSkill():
            return False
        if self.fashion.doingActionType() in [ACT.ROLL_ACTION, ACT.MOVINGSTOP_ACTION, ACT.AFTERMOVESTOP_ACTION]:
            return False
        if self.inDuelZone():
            if not self.inFubenTypes((const.FB_TYPE_BATTLE_FIELD_HUNT,)) and not self.isInPUBG():
                return False
        return self.stateMachine.checkStatus(const.CT_PICK_ITEM)

    def pickDroppedItems(self):
        p = BigWorld.player()
        pickNearDist = SCD.data.get('pickNearLength', 4)
        entities = BigWorld.entities.values()
        entities = filter(lambda entity: entity.__class__.__name__ == 'DroppedItem' and (entity.position - self.position).lengthSquared < pickNearDist * pickNearDist and entity.getOpacityValue()[0] == gameglobal.OPACITY_FULL and entity.isLeaveWorld == False, entities)
        if p.isInPUBG():
            p.pickNearItemsInPUBG(openAutoPickWidget=True)
        else:
            itemBoxsIds = []
            itemBoxItemIds = set()
            pickNearNum = SCD.data.get('pickNearNum', 2)
            for entity in entities:
                if ID.data.get(entity.itemId, {}).get('pickOneOnSingleTry') and entity.itemId in itemBoxItemIds:
                    continue
                itemBoxsIds.append(entity.id)
                itemBoxItemIds.add(entity.itemId)
                if pickNearNum <= len(itemBoxsIds):
                    break

            self.cell.pickNearItem(itemBoxsIds)

    def actionAfterLock(self, target):
        gamelog.debug('actionAfterLock:1', target.id)
        if not target:
            return
        if self.stateMachine.checkMove():
            if hasattr(target, 'noNeedChase') and target.noNeedChase():
                pass
            else:
                self.chaseEntity(target, self.getChaseDist(target))

    def useSkillByKey(self, idx, isDown):
        utils.recusionLog(7)
        self._skill(0, idx, isDown)

    def useSkillByKeyInDota(self, idx, isDown):
        utils.recusionLog(7)
        gameglobal.rds.ui.zaijuV2.useSkill(0, idx, isDown, byBfDota=True)

    def handleLearnSkillKey(self, isDown):
        gameglobal.rds.ui.zaijuV2.onLearnSkillKey(isDown)

    def handleReturnHomeKey(self, isDown):
        if isDown and formula.inDotaBattleField(getattr(self, 'mapID', 0)) and not getattr(self, 'isInBfDotaChooseHero', False):
            self.cell.onGoHome()

    def handleOpenDotaShop(self, isDown):
        if getattr(self, 'isShowEnd', False) or getattr(self, 'backToBfEnd', False) or getattr(self, 'isInBfDotaChooseHero', False):
            return
        if isDown:
            if not gameglobal.rds.ui.bfDotaShop.widget:
                gameglobal.rds.ui.bfDotaItemAndProp.doOpenShopClick()
            elif gameglobal.rds.ui.bfDotaShop.widget.visible:
                gameglobal.rds.ui.bfDotaShop.setVisible(False)
            else:
                gameglobal.rds.ui.bfDotaShop.setVisible(True)

    def openWingWorldUI(self, isDown):
        if isDown and self.canOpenWingWorldUI():
            if gameglobal.rds.ui.wingWorld.widget:
                gameglobal.rds.ui.wingWorld.hide()
            else:
                gameglobal.rds.ui.wingWorld.show()

    def handleLittleMapMarkInDota(self, key, isDown):
        if not isDown:
            return
        gameglobal.rds.ui.littleMap.InvokeProcessBfDotaClick(key)

    def hanldeShortCutBuy(self, idx, isDown):
        if isDown:
            gameglobal.rds.ui.bfDotaShopPush.shortCutBuy(idx)

    def handleShowDotaDetail(self, isDonw):
        if self.isShowEnd:
            return
        if self.isInBfDotaChooseHero:
            return
        if getattr(self, 'backToBfEnd', False):
            return
        if isDonw:
            gameglobal.rds.ui.bfDotaDetail.show()
        else:
            gameglobal.rds.ui.bfDotaDetail.setVisible(False)

    def handleShowDotaProp(self, isDonw):
        if isDonw:
            bfDotaItemAndPropProxy = gameglobal.rds.ui.bfDotaItemAndProp
            bfDotaItemAndPropProxy.setPropsVisible(not bfDotaItemAndPropProxy.isShowProp)

    def useItemByKey(self, idx, isDown):
        if idx < uiConst.MAX_ITEMBAR_SLOT:
            gameglobal.rds.ui.actionbar.useItem(uiConst.ITEM_ACTION_BAR, idx, isDown)
        else:
            gameglobal.rds.ui.actionbar.useItem(uiConst.ITEM_ACTION_BAR2, idx - uiConst.MAX_ITEMBAR_SLOT, isDown)

    def useItemByKeyInDota(self, idx, isDown):
        gameglobal.rds.ui.bfDotaItemAndProp.useItem(idx, isDown, byBfDota=True)

    def useQteSkillByKey(self, idx, isDown):
        gameglobal.rds.ui.qteNotice.useSkill(idx, isDown)

    def dragUI(self, isDown):
        if isDown:
            gameglobal.rds.ui.dragButton.dragHotKeyDown()

    def getRecursionLog(self):
        return utils.logList

    def _skill(self, idBar, idSlot, isDown):
        utils.recusionLog(8)
        zaiju = gameglobal.rds.ui.zaiju
        zaijuV2 = gameglobal.rds.ui.zaijuV2
        if self._isOnZaijuOrBianyao() or zaiju.isShow and zaiju.zaijuType == uiConst.ZAIJU_TYPE_WEAR or zaijuV2.widget and zaijuV2.zaijuType == uiConst.ZAIJU_TYPE_WEAR:
            if idSlot >= uiConst.MAX_ZAIJU_SLOT:
                if gameglobal.rds.ui.zaijuV2.widget:
                    zaijuV2.useSkill(idBar, idSlot, isDown)
                return
            if gameglobal.rds.configData.get('enableZaijuV2', False) and not gameglobal.rds.ui.vehicleSkill.widget:
                zaijuV2.useSkill(idBar, idSlot, isDown)
            else:
                zaiju.useSkill(idBar, idSlot, isDown)
        elif gameglobal.rds.ui.skill.inAirBattleState():
            gameglobal.rds.ui.airbar.useItem(uiConst.AIR_SKILL_BAR, idSlot, isDown)
        elif self.inInteractiveObj() and gameglobal.rds.ui.interactiveActionBar.mediator:
            gameglobal.rds.ui.interactiveActionBar.useSkill(idBar, idSlot, isDown)
        else:
            if getattr(self, 'isInBfDotaChooseHero', False):
                return
            gameglobal.rds.ui.actionbar.useItem(idBar, idSlot, isDown)

    def selfInjure(self, what, delta):
        if what == gametypes.CLIENT_HURT_BY_ENV:
            self.showGameMsg(GMDD.data.HURT_BY_ENV, (delta,))
        elif what == gametypes.CLIENT_HURT_DIE:
            self.showGameMsg(GMDD.data.FALL_DIE, (delta,))
        elif what == gametypes.CLIENT_HURT_FALL:
            self.showGameMsg(GMDD.data.FALL_DAMAGE, (delta,))
        self.otherDamage(delta)

    def isFace(self, tgt):
        if tgt == None:
            return
        elif self.id == tgt.id:
            return True
        else:
            deltaYaw = math.pi / 3
            tPos = tgt.position - self.position
            deltaYaw = math.fabs(self.yaw - tPos.yaw)
            if deltaYaw > math.pi:
                deltaYaw = math.pi * 2 - deltaYaw
            gamelog.debug('bgf:isFace:', deltaYaw, math.pi * 2 - deltaYaw)
            return deltaYaw <= math.pi / 3

    @ui.callInCD(0.3)
    def dealPlayerStateIcon(self, newSet):
        oldSet = getattr(self, 'oldPlayerStateSet', set())
        addSet = newSet - oldSet
        delSet = oldSet - newSet
        self.oldPlayerStateSet = newSet
        self._changePlayerStateIcon(addSet, delSet)

    def addPlayerAllStateIcon(self):
        p = BigWorld.player()
        newState = p.statesServerAndOwn
        newStateMap = self._getStateTimeMap(newState)
        flagState = p.flagStates
        newStateMap.update(self._getFlagStateTimeMap(flagState))
        newSet = newStateMap.items()
        newSet.sort(key=lambda k: k[1][1])
        newSet = set([ (item[0][0],
         item[0][1],
         item[1][2],
         item[1][0],
         item[1][1]) for item in newSet ])
        self.oldPlayerStateSet = set()
        self.dealPlayerStateIcon(newSet)

    def _getFlagStateTimeMap(self, state):
        timeMap = {}
        for item in state:
            if item[0] == 0:
                continue
            timeOld = timeMap[item[0], item[4]][0] if timeMap.get((item[0], item[4]), None) else None
            timeNew = item[3]
            if not timeOld or timeOld < timeNew:
                timeMap[item[0], item[4]] = [item[6],
                 item[3],
                 item[2],
                 item[4]]

        return timeMap

    def _getStateTimeMap(self, state):
        timeMap = {}
        for key, value in state.items():
            for st in value:
                timeOld = timeMap[key, st[gametypes.STATE_INDEX_SRCID]][gametypes.STATE_INDEX_LASTTIME] if timeMap.has_key((key, st[gametypes.STATE_INDEX_SRCID])) else None
                timeNew = st[gametypes.STATE_INDEX_LASTTIME]
                if not timeOld or timeOld < timeNew:
                    timeMap[key, st[gametypes.STATE_INDEX_SRCID]] = st

        return timeMap

    def _changePlayerStateIcon(self, addSet, delSet):
        addSet, delSet = self.updateMergeBuff(addSet, delSet)
        tempLeftDelBuffIdSet = set()
        delPlayerData = []
        delNoticeData = []
        delDeNoticeData = []
        for stateId, srcId, lastTime, layerNum, startTime in delSet:
            isHide = SD.data.get(stateId, {}).get('iconUnshow', 0)
            if isHide:
                continue
            data = self._getStateData(stateId, srcId, lastTime, layerNum, startTime, False)
            iconType = SD.data.get(stateId, {}).get('iconShowType', 3)
            if iconType in (uiConst.TYPE_DEBUFF_LAST, uiConst.TYPE_BUFF_LAST, uiConst.TYPE_BUFF_FUNC):
                delPlayerData.append(data)
            elif iconType == 1:
                delDeNoticeData.append(data)
            else:
                delNoticeData.append(data)
            if data['count'] > 0:
                tempLeftDelBuffIdSet.add(stateId)

        addPlayerData = []
        addNoticeData = []
        addDeNoticeData = []
        for stateId, srcId, lastTime, layerNum, startTime in addSet:
            isHide = SD.data.get(stateId, {}).get('iconUnshow', 0)
            if isHide:
                continue
            data = self._getStateData(stateId, srcId, lastTime, layerNum, startTime, True)
            iconType = SD.data.get(stateId, {}).get('iconShowType', 3)
            if iconType in (uiConst.TYPE_DEBUFF_LAST, uiConst.TYPE_BUFF_LAST, uiConst.TYPE_BUFF_FUNC):
                addPlayerData.append(data)
            else:
                data['isNew'] = stateId not in tempLeftDelBuffIdSet
                if iconType == 1:
                    addDeNoticeData.append(data)
                else:
                    addNoticeData.append(data)

        if addPlayerData or delPlayerData:
            gameglobal.rds.ui.player.changeStateIcon(addPlayerData, delPlayerData)
        getMergeBuffDesc = self.getMergeBuffDesc()
        gameglobal.rds.ui.player.changeMergeIcon(getMergeBuffDesc)
        if addNoticeData or delNoticeData:
            gameglobal.rds.ui.buffNotice.changeStateIcon(addNoticeData, delNoticeData, 2)
        if addDeNoticeData or delDeNoticeData:
            gameglobal.rds.ui.buffNotice.changeStateIcon(addDeNoticeData, delDeNoticeData, 1)

    def _matchState(self, buffId, srcId, stateId, stateSrc):
        data = SD.data.get(int(buffId), None)
        separateShow = data.get('separateShow', 0)
        if separateShow:
            return int(buffId) == stateId and int(srcId) == stateSrc
        else:
            return int(buffId) == stateId

    def _getStateData(self, stateId, srcId, lastTime, layerNum, startTime, isPlus):
        p = BigWorld.player()
        retData = {}
        iconType = SD.data.get(stateId, {}).get('iconShowType', 3)
        separateShow = SD.data.get(stateId, {}).get('separateShow', 0)
        noNA = SD.data.get(stateId, {}).get('noNA', 0)
        if iconType in (uiConst.TYPE_BUFF_FUNC, uiConst.TYPE_BUFF_QUEST):
            iconType = uiConst.TYPE_BUFF_LAST
        if not separateShow:
            srcId = p.id
        retData['type'] = iconType
        retData['srcId'] = srcId
        retData['id'] = stateId
        data = SD.data.get(stateId, None)
        if data != None:
            iconId = data.get('iconId', 'notFound')
            retData['iconPath'] = str(iconId) + '.dds'
            retData['timer'] = lastTime - (p.getServerTime() - startTime)
            if retData['timer'] > lastTime:
                retData['timer'] = lastTime
            if retData['timer'] > 36000 and not noNA or lastTime == -1:
                retData['timer'] = -100
            if isPlus:
                if not separateShow:
                    retData['count'] = self.getNoSepStateCount(stateId)
                else:
                    retData['count'] = layerNum
            elif not separateShow:
                retData['count'] = self.getNoSepStateCount(stateId)
            else:
                retData['count'] = self.getNoSepStateCountBySrcId(stateId, srcId)
        return retData

    def getNoSepStateCount(self, stateId):
        p = BigWorld.player()
        states = getattr(p, 'statesServerAndOwn', {})
        count = 0
        for state in states.get(stateId, []):
            count += state[gametypes.STATE_INDEX_LAYER]

        return count

    def getNoSepStateCountBySrcId(self, stateId, srcId):
        p = BigWorld.player()
        states = getattr(p, 'statesServerAndOwn', {})
        count = 0
        for state in states.get(stateId, []):
            if srcId == state[gametypes.STATE_INDEX_SRCID]:
                count += state[gametypes.STATE_INDEX_LAYER]

        return count

    def _delPlayerStateIcon(self, state):
        gameglobal.rds.ui.player.delStateIcon(state)

    def isUseSkill(self):
        if self.castSkillBusy:
            return True
        if self.fashion.doingActionType() in [ACT.CAST_ACTION,
         ACT.MOVING_ACTION,
         ACT.AFTERMOVE_ACTION,
         ACT.CAST_MOVING_ACTION]:
            return True
        return False

    def pickItem(self, itemBox):
        it = Item(itemBox.itemId, itemBox.itemNum)
        pickUpDist = SCD.data.get('pickUpLength', 4)
        if not inRange3D(pickUpDist, self.position, itemBox.model.position):
            self.showGameMsg(GMDD.data.ITEM_PICK_FAR, ())
            return
        if it.type != Item.BASETYPE_MONEY and not self.checkPickItems():
            return
        enableGemOwner = gameglobal.rds.configData.get('enableGemOwner', True)
        if itemBox.srcEntType == 'Monster' and it.type == it.BASETYPE_EQUIP_GEM and enableGemOwner:
            it.setOwner(self.gbId, self.roleName)
        if it.type in (Item.BASETYPE_MONEY, Item.BASETYPE_FUBEN) or utils.isGroupPick(self, itemBox):
            pg, ps = const.INV_PAGE_NUM + 1, 0
        else:
            pg, ps = self.realInv.searchBestInPages(it.id, it.cwrap, it)
            if ps == const.CONT_NO_POS:
                self.showGameMsg(GMDD.data.ITEM_PICK_FULL, (it.name,))
                return
        itemBox.cell.pickItem(pg, ps, False)

    def getOptionalTargetLocked(self, skillInfo):
        if hasattr(self, 'getOperationMode') and self.getOperationMode() == gameglobal.ACTION_MODE and self.optionalTargetLocked and self.optionalTargetLocked.inWorld:
            isDamageSkill = skillDataInfo.isEnemySkill(skillInfo)
            isHealSkill = skillDataInfo.isFriendSkill(skillInfo)
            isEnemy = self.isEnemy(self.targetLocked)
            isCastSelfKeyDown = HK.isCastSelfKeyDown()
            if not isCastSelfKeyDown and (isEnemy and isHealSkill or not isEnemy and isDamageSkill):
                if getattr(self.optionalTargetLocked, 'IsCombatUnit', False):
                    return self.optionalTargetLocked

    def checkSkillCanUse(self, skillInfo, target = None, needBlockMsg = False, autoAttack = False):
        skillId = skillInfo.num
        p = BigWorld.player()
        if p.isPubgCommSkillLock(skillId):
            if not needBlockMsg:
                self.showGameMsg(GMDD.data.PUBG_NOT_UNLOCK_SKILL, ())
            return False
        enableSocialSkill = MCD.data.get(formula.getMapId(self.spaceNo), {}).get('enableSocialSkill', 1)
        if not enableSocialSkill and skillInfo.getSkillData('skillCategory') == const.SKILL_CATEGORY_SOCIAL:
            if not needBlockMsg:
                self.showGameMsg(GMDD.data.SOCIAL_SKILL_CAST_FAILED_IN_DUEL, ())
            return False
        if not skillDataInfo.checkSkillRequest(skillInfo, tgt=target, needBlockMsg=needBlockMsg):
            return False
        if commcalc.getBitDword(self.publicFlags, gametypes.FLAG_NO_SKILL):
            self.chatToEventEx(gameStrings.TEXT_IMPPLAYERCOMBAT_1397, const.CHANNEL_COLOR_RED)
            return False
        if logicInfo.isSkillCooldowning(skillId) and not self.inNoCostAndCDSkillState():
            self._showSkillNotReadyMsg(skillId, needBlockMsg=needBlockMsg)
            return False
        if self.isGuiding and not skillDataInfo.needBreakSelfSpell(self.skillPlayer.skillID, skillInfo):
            if not needBlockMsg:
                self.chatToEventEx(gameStrings.TEXT_IMPPLAYERCOMBAT_1405, const.CHANNEL_COLOR_RED)
            return False
        if self.isForceMove:
            if skillDataInfo.ignoreForceMove(skillInfo):
                pass
            else:
                self.chatToEventEx(gameStrings.TEXT_IMPPLAYERCOMBAT_1411, const.CHANNEL_COLOR_RED)
                return False
        elif self.spellingType or not logicInfo.isUseableSkill(skillId) and not p.inNoCostAndCDSkillState():
            if self.spellingType:
                self._showSkillNotReadyMsg(skillId, needBlockMsg=needBlockMsg)
                if skillId == self.skillPlayer.skillID:
                    self.showGameMsg(GMDD.data.USE_SAME_SPELL_SKILL, ())
                    return False
                return False
            else:
                self._showSkillNotReadyMsg(skillId, False, needBlockMsg=needBlockMsg)
                if not needBlockMsg:
                    self.chatToEventEx(gameStrings.TEXT_IMPL_IMPCOMBAT_10504, const.CHANNEL_COLOR_RED)
                return False
        skillNeedTgtPos = skillInfo.getSkillData('tgtPos', 0)
        if not skillNeedTgtPos and not skillDataInfo.checkCollide(skillInfo):
            if not needBlockMsg:
                self.showGameMsg(GMDD.data.BLOCKED_BY_WALL, ())
            return False
        moveMode = skillDataInfo.getCastMoveType(skillInfo)
        spellSkill = skillInfo.getSkillData('spellTime', 0)
        castType = skillInfo.getSkillData('castType', 0)
        checkType = const.CT_CAST_UN_MOVE
        if spellSkill:
            checkType = const.CT_SPELL_SKILL
        elif castType == gameglobal.CAST_TYPE_CHARGE:
            checkType = const.CT_CHARGE_SKILL
        elif castType == gameglobal.CAST_TYPE_GUIDE:
            checkType = const.CT_GUIDE_SKILL
        elif castType == gameglobal.CAST_TYPE_MOVE:
            checkType = const.CT_MOVE_SKILL
        elif moveMode == ACT.S_BLEND:
            checkType = const.CT_CAST_MOVE
        if skillNeedTgtPos and not self.circleEffect.isShowingEffect and not gameglobal.INTELLIGENT_CAST:
            checkType = const.CT_SHOW_SKILL_CIRCLE
            if commcalc.getBitDword(self.publicFlags, gametypes.FLAG_NOT_CONTROLLABLE):
                self.chatToEventEx(gameStrings.TEXT_IMPPLAYERCOMBAT_1466, const.CHANNEL_COLOR_RED)
                return False
        exclude = []
        if skillDataInfo.ignoreForceMove(skillInfo):
            exclude.append('FORCE_MOVE_ST')
        if skillInfo.getSkillData('allowPathFinding', False):
            exclude.append('AUTO_PATHFINDING_ST')
        if skillInfo.getSkillData('allowMoveOnPin'):
            exclude.extend(['CAST_UN_MOVE_ST', 'UNMOVE_ST'])
        if checkType in (const.CT_SPELL_SKILL,
         const.CT_CAST_MOVE,
         const.CT_CAST_UN_MOVE,
         const.CT_GUIDE_SKILL,
         const.CT_MOVE_SKILL,
         const.CT_CHARGE_SKILL):
            srcType = const.DELAY_GROUP_FOLLOW_AUTOATTACK if autoAttack else const.DELAY_GROUP_FOLLOW_MANUAL
            if not self.checkTempGroupFollow(srcType=srcType):
                return False
        if not self.stateMachine.checkStatus(checkType, exclude):
            self.chatToEventEx(gameStrings.TEXT_IMPPLAYERCOMBAT_1482, const.CHANNEL_COLOR_RED)
            return False
        return True

    def afterCheckSkillCanUse(self, skillId, skillLevel):
        if self.spellingType:
            if skillId != self.skillPlayer.skillID:
                cellCmd.cancelSkill()
        if self.isUseQingGong:
            if self.isDashing and not self.isJumping:
                self.ap.switchToRun()

    def checkSkill(self, skillInfo, target = None, autoAttack = False):
        if self.checkSkillCanUse(skillInfo, target, autoAttack=autoAttack):
            self.afterCheckSkillCanUse(skillInfo.num, skillInfo.lv)
            return True
        return False

    def getSkillSpellingType(self):
        skillInfo = SkillInfo(self.skillId, self.skillLevel)
        spellSkill = skillDataInfo.getSpellTime(skillInfo)
        if spellSkill:
            spellType = skillDataInfo.isPreSpellSkill(skillInfo)
            if spellType:
                return ACT.S_PRESPELLING
            elif skillDataInfo.isSpellSkillCanMove(skillInfo):
                return ACT.S_SPELLING_CAN_MOVE
            else:
                return ACT.S_SPELLING
        spellCharge = skillDataInfo.isChargeSkill(skillInfo)
        if spellCharge:
            return ACT.S_SPELLCHARGE
        return ACT.S_DEFAULT

    def getSkillSpellingTypeBySkill(self, skillId, skillLevel):
        skillInfo = SkillInfo(skillId, skillLevel)
        spellSkill = skillDataInfo.getSpellTime(skillInfo)
        if spellSkill:
            spellType = skillDataInfo.isPreSpellSkill(skillInfo)
            if spellType:
                return ACT.S_PRESPELLING
            elif skillDataInfo.isSpellSkillCanMove(skillInfo):
                return ACT.S_SPELLING_CAN_MOVE
            else:
                return ACT.S_SPELLING
        spellCharge = skillDataInfo.isChargeSkill(skillInfo)
        if spellCharge:
            return ACT.S_SPELLCHARGE
        return ACT.S_DEFAULT

    def isAnySkillKeyDown(self):
        skillKeys = [keys.KEY_1,
         keys.KEY_2,
         keys.KEY_3,
         keys.KEY_4,
         keys.KEY_5,
         keys.KEY_6,
         keys.KEY_7,
         keys.KEY_8,
         keys.KEY_9,
         keys.KEY_0]
        for key in skillKeys:
            if HK.HKM[key].isAnyDown():
                return True

        return False

    def _runCircleEffect(self, skillInfo, needCircle):
        gamelog.debug('_runCircleEffect', needCircle, self.circleEffect.isShowingEffect, self.shortcutToPostionSkillId, self.shortcutToPostion)
        if needCircle and self.checkSkill(skillInfo):
            if self.mouseOptimizePosition():
                pass
            elif self.shortcutToPostion and self.shortcutToPostionSkillId == self.skillId and self.circleEffect.isShowingEffect:
                self.circleEffect.run()
            else:
                if self.skillId != self.circleEffect.skillID:
                    self.circleEffect.cancel()
                self.circleEffect.start(self.skillId, self.skillLevel)

    def _arrowEffectOptimize(self, skillInfo, showCircleEffect = True):
        if self.getOperationMode() == gameglobal.MOUSE_MODE and showCircleEffect:
            if not skillDataInfo.isNeedTarget(skillInfo) and self.checkSkill(skillInfo) and skillDataInfo.getCircleShape(skillInfo):
                if self.shortcutToPostion and self.shortcutToPostionSkillId == self.skillId and self.circleEffect.isShowingEffect:
                    self.circleEffect.run()
                else:
                    self.circleEffect.cancel()
                    circleShape = skillDataInfo.getCircleShape(skillInfo)
                    self.circleEffect.start(self.skillId, self.skillLevel, fxMode=gameglobal.CIRCLE_EFFECT_FX_MODE_DIRECTION, circleShape=circleShape)
                return True
        return False

    def useSkillByKeyDown(self, isDown, skillInfo, needBlockMsg = False, autoAttack = False):
        self.skillId = skillInfo.num
        self.skillLevel = skillInfo.lv
        needCircle = skillDataInfo.isSkillneedCircle(skillInfo)
        if isDown and hasattr(self, 'getOperationMode') and self.getOperationMode() == gameglobal.ACTION_MODE:
            if skillDataInfo.needTarget(skillInfo) or not self.optionalTargetLocked:
                self.ap.lockOptionalTarget()
        isSpellCharge = skillDataInfo.isChargeSkill(skillInfo)
        if isDown:
            if self.skillId == self.skillLog[0] and BigWorld.time() - self.skillLog[1] <= const.SKILL_INTERVAL:
                return
            if gameglobal.BREAK_GUIDE_SKILL and self.isGuiding:
                isGuideSkill = skillDataInfo.isGuideSkill(skillInfo)
                nowSkillID = getattr(self.skillPlayer, 'skillID', 0)
                if isGuideSkill and nowSkillID and int(self.skillId) == int(nowSkillID):
                    cellCmd.cancelSkill()
                    return
            self.lastUseSkillId = self.skillId
            if not self.isChargeKeyDown and self.holdingSkill(skillInfo):
                return
            if not isSpellCharge:
                if self.getOperationMode() == gameglobal.MOUSE_MODE:
                    if not needCircle and self.useSkillCheck(skillInfo):
                        return
                if not self.checkSkill(skillInfo, autoAttack=autoAttack):
                    return
                if not needCircle:
                    self.circleEffect.cancel()
                    isSkillNeedChooseCursor = skillDataInfo.isSkillNeedChooseCursor(skillInfo)
                    isCastSelfKeyDown = HK.isCastSelfKeyDown()
                    if isSkillNeedChooseCursor and gameglobal.NEED_CHOOSE_EFFECT and not isCastSelfKeyDown:
                        self.chooseEffect.cancel()
                        self.chooseEffect.start(self.skillId, self.skillLevel)
                    else:
                        if self._arrowEffectOptimize(skillInfo, not gameglobal.INTELLIGENT_CAST):
                            return
                        self.useskill()
                else:
                    self._runCircleEffect(skillInfo, needCircle)
                return
            self.waitingReleaseInfo = {}
            if self.isChargeKeyDown:
                self.chargeSkillId = skillInfo.num
                self.chargeSkillLv = skillInfo.lv
                self.isChargeKeyDown = False
                if not self.lockedId:
                    self.lockedId = self.id
                cellCmd.castChargeSkill()
                gameglobal.rds.ui.castbar.easeOutCastbar()
                return
            self.chargeSkillId = skillInfo.num
            self.chargeSkillLv = skillInfo.lv
            if self.getOperationMode() == gameglobal.MOUSE_MODE:
                if not needCircle and self.useSkillCheck(skillInfo):
                    return
            gamelog.debug('useSkillByKeyDown1', self.isChargeKeyDown)
            if not self.checkSkill(skillInfo, autoAttack=autoAttack):
                return
            if needCircle:
                if self.shortcutToPostion and self.shortcutToPostionSkillId == self.skillId and self.circleEffect.isShowingEffect:
                    self.circleEffect.run()
                else:
                    self.circleEffect.cancel()
                    self.circleEffect.start(self.skillId, self.skillLevel)
            else:
                self.useskill()
        else:
            if isSpellCharge:
                if self.isChargeKeyDown:
                    self.releaseCharge()
                else:
                    self.waitingReleaseInfo = {'chargeSkillId': skillInfo.num,
                     'chargeSkillLv': skillInfo.lv}
            if self.lastUseSkillId != self.skillId:
                return
            if not self.isAnySkillKeyDown():
                self.lastUseSkillId = None

    def holdingSkill(self, skillInfo):
        p = BigWorld.player()
        inGcd = logicInfo.commonCooldownWeaponSkill[0] > BigWorld.time()
        inSkillAction = p.fashion.doingActionType() in ACT.HOLDING_SKILL_ACTION
        if inGcd or inSkillAction:
            isSpellCharge = skillDataInfo.isChargeSkill(skillInfo)
            isGuideSkill = skillDataInfo.isGuideSkill(skillInfo)
            if isSpellCharge or isGuideSkill:
                p.addHoldingSkills(skillInfo)
                return True
        return False

    def useHoldingSkill(self):
        skillInfo = self.getHoldingSkillForCast()
        if skillInfo:
            self.useSkillByKeyDown(True, skillInfo)

    def releaseCharge(self):
        gamelog.debug('releaseCharge')
        if not self.isChargeKeyDown or not self.chargeSkillId:
            return
        else:
            self.isChargeKeyDown = False
            skillInfo = SkillInfo(self.chargeSkillId, self.chargeSkillLv)
            needCircle = skillDataInfo.isSkillneedCircle(skillInfo)
            isSpellCharge = skillDataInfo.isChargeSkill(skillInfo)
            if not self.isAnySkillKeyDown():
                self.lastUseSkillId = None
            if not isSpellCharge:
                if needCircle:
                    self.circleEffect.cancel()
                    if not self.checkSkillCanUse(skillInfo):
                        return
                    self.circleEffect.start(self.skillId, self.skillLevel)
                return
            if not self.lockedId:
                self.lockedId = self.id
            cellCmd.castChargeSkill()
            gameglobal.rds.ui.castbar.easeOutCastbar()
            return

    def useSkillByMouseUp(self, isDown, skillInfo, autoAttack = False):
        self.skillId = skillInfo.num
        self.skillLevel = skillInfo.lv
        needCircle = skillDataInfo.isSkillneedCircle(skillInfo)
        isSpellCharge = skillDataInfo.isChargeSkill(skillInfo)
        if isDown:
            if not self.isChargeKeyDown and self.holdingSkill(skillInfo):
                return
            return
        if isSpellCharge:
            if self.isChargeKeyDown:
                self.chargeSkillId = skillInfo.num
                self.chargeSkillLv = skillInfo.lv
                self.isChargeKeyDown = False
                if not self.lockedId:
                    self.lockedId = self.id
                cellCmd.castChargeSkill()
                gameglobal.rds.ui.castbar.easeOutCastbar()
                self.hideWidgetForActionPhysics()
                return
            else:
                self.chargeSkillId = skillInfo.num
                self.chargeSkillLv = skillInfo.lv
                if self.getOperationMode() == gameglobal.MOUSE_MODE:
                    if not needCircle and self.useSkillCheck(skillInfo):
                        return
                if not self.checkSkill(skillInfo, autoAttack=autoAttack):
                    return
                if needCircle:
                    self.circleEffect.cancel()
                    self.circleEffect.start(self.skillId, self.skillLevel)
                else:
                    self.useskill()
                self.hideWidgetForActionPhysics()
                if hasattr(self, 'getOperationMode') and self.getOperationMode() == gameglobal.ACTION_MODE:
                    gameglobal.rds.ui.chat.closeInput()
                return
        if self.getOperationMode() == gameglobal.MOUSE_MODE:
            if not needCircle and self.useSkillCheck(skillInfo):
                return
        if not self.checkSkill(skillInfo, autoAttack=autoAttack):
            return
        if needCircle:
            self.circleEffect.cancel()
            self.circleEffect.start(self.skillId, self.skillLevel)
        else:
            if self._arrowEffectOptimize(skillInfo, True):
                return
            self.useskill()
        self.hideWidgetForActionPhysics()

    def hideWidgetForActionPhysics(self):
        p = BigWorld.player()
        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            gameglobal.rds.ui.chat.closeInput()
            p.ap.showCursor = False
            p.ap.reset()
            p.ap.hideWidget()

    def sendSkillInfo(self, skills):
        for skillId, enable, lv, enhanceData in skills:
            self.skills[skillId] = skillDataInfo.SkillInfoVal(skillId, lv)
            skillInfo = SkillInfo(skillId, lv)
            wsType = skillInfo.getSkillData('wsType', 1)
            self.skills[skillId].wsType = wsType
            if skillInfo.hasSkillData('wsNeed1') or skillInfo.hasSkillData('wsNeed2'):
                self.skills[skillId].isWsSkill = True
            self.skills[skillId].enable = enable
            for part, enhanceDict in enhanceData.iteritems():
                self.skills[skillId].enhanceData[part] = CSkillEnhanceVal(**enhanceDict)

        gameglobal.rds.ui.actionbar.refreshActionbar()

    def sendSocialSkillInfo(self, skills):
        for skillId, enable, lv in skills:
            self.skills[skillId] = skillDataInfo.SkillInfoVal(skillId, lv)
            self.skills[skillId].enable = enable
            self.skills[skillId].isSocialSkill = True

    def sendFlagState(self, states):
        self.flagStateCommon.clear()
        for flagState in states:
            stateId, stateLv, lastTime, flagTime, src, flagStateId, flagCnt = flagState
            self.flagStateCommon.markFlagState(self, flagStateId, lastTime, flagCnt)
            self.flagStateCommon[flagStateId].time = flagTime

        self.flagStates = [ flagState for flagState in states ]
        self.clientEffectIcon()

    def sendFamousGeneralAward(self, awardInfo):
        gameglobal.rds.ui.roleInformationJunjie.awardInfo = awardInfo
        gameglobal.rds.ui.roleInformationJunjie.initFamousSkillArea()

    def sendPSkillInfo(self, pskId, subSrc, enable, level, pData):
        if not self.pskills.has_key(pskId):
            self.pskills[pskId] = skillDataInfo.PSkillSubDict()
        self.pskills[pskId][subSrc] = skillDataInfo.PSkillVal(pskId, level)
        self.pskills[pskId][subSrc].enable = enable
        self.pskills[pskId][subSrc].pData = pData
        gameglobal.rds.ui.actionbar.skillInfoCache.clear()

    def batchUpdatePSkillEnable(self, enablePsks, disablePsks):
        for pskId in enablePsks:
            self._updatePSkillEnable(pskId, True)

        for pskId in disablePsks:
            self._updatePSkillEnable(pskId, False)

        gameglobal.rds.ui.actionbar.skillInfoCache.clear()

    def updatePSkillEnable(self, pskId, enable):
        self._updatePSkillEnable(pskId, enable)
        gameglobal.rds.ui.actionbar.skillInfoCache.clear()

    def _updatePSkillEnable(self, pskId, enable):
        if not self.pskills.has_key(pskId):
            return
        for psk in self.pskills[pskId].itervalues():
            psk.enable = enable

    def sendTriggerPSkillInfo(self, pskId, level, enable):
        self.triggerPSkills[pskId] = skillDataInfo.PSkillVal(pskId, level, enable)

    def batchUpdateTriggerPSkillEnable(self, enablePsks, disablePsks):
        for pskId in enablePsks:
            self.updateTriggerPSkillEnable(pskId, True)

        for pskId in disablePsks:
            self.updateTriggerPSkillEnable(pskId, False)

    def updateTriggerPSkillEnable(self, pskId, enable):
        if pskId in self.triggerPSkills:
            self.triggerPSkills[pskId].enable = enable

    def updatePSkillNextTriggerTime(self, pskId, nextTriggerTime):
        if pskId not in self.triggerPSkills:
            return
        self.triggerPSkills[pskId].nextTriggerTime = nextTriggerTime
        gameglobal.rds.ui.bfDotaItemAndProp.refreshItemCooldown()
        gameglobal.rds.ui.actionbar.updateSlot(pskId)

    def updatePSkillTriggerInvalidTime(self, pskId, triggerInvalidTime):
        if pskId not in self.triggerPSkills:
            return
        self.triggerPSkills[pskId].triggerInvalidTime = triggerInvalidTime

    def sendWsSkillInfo(self, res):
        self.wsSkills.clear()
        for key, val in res.items():
            self.wsSkills[key] = skillDataInfo.SkillInfoVal(key, val[0])
            skillInfo = SkillInfo(key, val[0])
            wsType = skillInfo.getSkillData('wsType', 1)
            self.wsSkills[key].wsType = wsType
            if skillInfo.hasSkillData('wsNeed1') or skillInfo.hasSkillData('wsNeed2'):
                self.wsSkills[key].isWsSkill = True
            self.wsSkills[key].enable = val[1]
            self.wsSkills[key].slots = val[2]
            self.wsSkills[key].proficiency = val[3]
            self.wsSkills[key].daoHeng = val[4]
            self.wsSkills[key].lingli = val[5]

        gameglobal.rds.ui.actionbar.refreshActionbar(False)

    def sendZaijuSkillInfo(self, isPSkill, info):
        gamelog.debug('jorsef: get zaiju skill info: ', isPSkill, info)
        zaijuSkillIds = [ skVal[0] for skVal in info ]
        coolDownSkills = [ key for key in logicInfo.cooldownSkill.keys() ]
        for skillId in coolDownSkills:
            if skillId not in zaijuSkillIds and skillId not in self.getSkills().keys():
                logicInfo.cooldownSkill.pop(skillId)

        gameglobal.rds.ui.zaiju.setServerSkills(info)
        gameglobal.rds.ui.zaijuV2.setServerSkills(info, isPSkill)
        if isPSkill:
            pass

    def sendLearnedPSkillInfos(self, skillInfos):
        if not skillInfos:
            return
        for skillInfo in skillInfos:
            self.sendLearnedPSkillInfo(*skillInfo)

    def sendLearnedPSkillInfo(self, pskId, lv, enable):
        if lv == 0:
            del self.learnedPSkills[pskId]
        else:
            self.learnedPSkills[pskId] = skillDataInfo.PSkillVal(pskId, lv)
            self.learnedPSkills[pskId].enable = enable
        gameglobal.rds.ui.skill.refreshPSkillById(pskId)
        if gameglobal.rds.ui.roleInfo.mediator:
            gameglobal.rds.ui.roleInfo.refreshInfo()
        gameglobal.rds.ui.skill.skillInfoManager.clear()
        gameglobal.rds.ui.skill.refreshPSkill()

    def sendAirPSkill(self, pskId, lv, enable):
        if lv == 0:
            del self.airPSkills[pskId]
        else:
            self.airPSkills[pskId] = skillDataInfo.PSkillVal(pskId, lv)
            self.airPSkills[pskId].enable = enable

    def updateCalcEntities(self, creationId, ids):
        if not ids:
            return
        creation = BigWorld.entities.get(creationId)
        if creation and getattr(creation, 'ownerId', 0) == self.id:
            creation.calcEntities.extend(ids)

    def clearSkillInfo(self):
        self.skills.clear()

    def skillStart(self, targetId, skillId, skillLevel, instant, targetPos):
        self.isWaitSkillReturn = False
        super(self.__class__, self).skillStart(targetId, skillId, skillLevel, instant, targetPos)

    def skillStartWithMove(self, targetId, skillId, skillLevel, moveId, moveTime, moveClientRefInfo, instant, targetPos):
        self.isWaitSkillReturn = False
        super(self.__class__, self).skillStartWithMove(targetId, skillId, skillLevel, moveId, moveTime, moveClientRefInfo, instant, targetPos)

    def mySkills(self):
        return self.skills

    def updateSkillInfos(self, skillInfos):
        if not skillInfos:
            return
        for skillInfo in skillInfos:
            self.updateSkillInfo(*skillInfo)

    def updateSkillInfo(self, skillId, enable, lv, enhanceData):
        if self.skills.has_key(skillId):
            if lv == 0:
                del self.skills[skillId]
            else:
                self.skills[skillId].level = lv
                self.skills[skillId].enable = enable
                for part, enhanceDict in enhanceData.iteritems():
                    self.skills[skillId].enhanceData[part] = CSkillEnhanceVal(**enhanceDict)

                if gameglobal.rds.configData.get('enableRemoveSkillEnhance', False):
                    rmParts = set()
                    for part, enhVal in self.skills[skillId].enhanceData.iteritems():
                        if part not in enhanceData:
                            rmParts.add(part)

                    for rmPt in rmParts:
                        self.skills[skillId].enhanceData.pop(rmPt, None)

            gameglobal.rds.ui.skill.refreshNormalSkillById(skillId)
            gameglobal.rds.ui.skill.refreshSkillPracticeInfo(gameglobal.rds.ui.skill.skillId)
            gameglobal.rds.ui.skill.refreshSkillEnhanceLv()
        else:
            self.skills[skillId] = skillDataInfo.SkillInfoVal(skillId, lv)
            skillInfo = SkillInfo(skillId, lv)
            wsType = skillInfo.getSkillData('wsType', 1)
            self.skills[skillId].wsType = wsType
            if skillInfo.hasSkillData('wsNeed1') or skillInfo.hasSkillData('wsNeed2'):
                self.skills[skillId].isWsSkill = True
            self.skills[skillId].enable = enable
            for part, enhanceDict in enhanceData.iteritems():
                self.skills[skillId].enhanceData[part] = CSkillEnhanceVal(**enhanceDict)

            gameglobal.rds.ui.skill.newSkills.append(skillId)
            gameglobal.rds.ui.skill.refreshNormalSkillById(skillId)
            if self.lv != 1:
                gameglobal.rds.ui.skillGuide.show(skillId)
            gameglobal.rds.ui.skillPush.setSkillData(skillId, self.skills[skillId].isWsSkill)
        gameglobal.rds.ui.skill.skillInfoManager.clear()
        gameglobal.rds.ui.skill.refreshPSkill()
        gameglobal.rds.ui.skill.refreshNormalSkill()
        gameglobal.rds.ui.skill.refreshXiuLianPoint()
        gameglobal.rds.ui.actionbar.initSkillStat(skillId)
        gameglobal.rds.ui.actionbar.checkSkillStatOnPropModified()

    def getQingGongSkillLv(self, qType):
        if gametypes.LEARN_ALL_GQINGGONG:
            return 1
        flag = gametypes.QINGGONG_TYPE_TO_FLAG[qType]
        skillVal = self.qingGongSkills.get(flag)
        if not skillVal:
            return None
        else:
            return skillVal.level

    def getQingGongData(self, qType):
        lv = self.getQingGongSkillLv(qType)
        return QCD.data.get((qType, lv), {})

    def clearQingGongSkillInfo(self):
        self.qingGongSkills.clear()

    def sendQingGongSkillInfo(self, skillId, enable, lv):
        self.qingGongSkills[skillId] = skillDataInfo.QingGongSkillInfoVal(skillId, lv)
        self.qingGongSkills[skillId].enable = enable

    def updateQingGongSkillInfo(self, skillId, enable, lv):
        if self.qingGongSkills.has_key(skillId):
            if lv == 0:
                del self.qingGongSkills[skillId]
            else:
                self.qingGongSkills[skillId].level = lv
                self.qingGongSkills[skillId].enable = enable
        else:
            self.qingGongSkills[skillId] = skillDataInfo.QingGongSkillInfoVal(skillId, lv)
            self.qingGongSkills[skillId].enable = enable
        gameglobal.rds.ui.skill.refreshQingGongPanel()

    def setWSData(self, skillId, enable, lv, slots, proficiency, daoHeng, lingli, wsType = 0, isInit = False):
        if isInit:
            self.wsSkills[skillId] = skillDataInfo.SkillInfoVal(skillId, lv, enable)
            skillInfo = SkillInfo(skillId, lv)
            self.wsSkills[skillId].isWsSkill = skillInfo.hasSkillData('wsNeed1') or skillInfo.hasSkillData('wsNeed2')
            self.wsSkills[skillId].wsType = wsType
        self.wsSkills[skillId].slots = slots
        self.wsSkills[skillId].proficiency = proficiency
        self.wsSkills[skillId].daoHeng = daoHeng
        self.wsSkills[skillId].level = lv
        self.wsSkills[skillId].enable = enable
        self.wsSkills[skillId].lingli = lingli

    def updateWsSkillInfo(self, skillId, enable, lv, slots, proficiency, daoHeng, lingli):
        gamelog.debug('zt: update ws skill info', skillId, enable, lv, slots, proficiency, daoHeng)
        lastLv = 0
        if not self.wsSkills.has_key(skillId):
            skillInfo = SkillInfo(skillId, lv)
            wsType = skillInfo.getSkillData('wsType', 1)
            self.setWSData(skillId, enable, lv, slots, proficiency, daoHeng, lingli, wsType, True)
            if gameglobal.rds.ui.skill.wushuangSkillPanelMc != None:
                gameglobal.rds.ui.skill.refreshSpecialSkillById(skillId, wsType)
            selectedWs = []
            wsVal = self.wushuang[wsType]
            currSchemeNo = gameglobal.rds.ui.actionbar.currSchemeNo
            if currSchemeNo == uiConst.SHORT_CUT_CASE_1:
                selectedWs = wsVal.selectedWs
            elif currSchemeNo == uiConst.SHORT_CUT_CASE_2:
                selectedWs = wsVal.selectedWs1
            elif currSchemeNo == uiConst.SHORT_CUT_CASE_3:
                selectedWs = wsVal.selectedWs2
            if skillId not in selectedWs:
                self.cell.addWsSkill(skillId)
                skillCnt = len(selectedWs)
                for i in range(skillCnt):
                    if gameglobal.rds.ui.skill.equipSkills[wsType - 1][i] == 0:
                        gameglobal.rds.ui.skill.setItem(skillId, uiConst.SKILL_PANEL_SPECIAL_RIGHT, skillCnt * (wsType - 1) + i)
                        break

            clientSkillInfo = ClientSkillInfo(skillId, lv)
            self.preloadEffect(skillDataInfo.getSkillEffect(clientSkillInfo))
            self.preloadAction(skillDataInfo.getSkillAction(clientSkillInfo))
        else:
            lastLv = self.wsSkills[skillId].level
            self.setWSData(skillId, enable, lv, slots, proficiency, daoHeng, lingli, isInit=False)
            if gameglobal.rds.ui.skill.wushuangSkillPanelMc != None:
                gameglobal.rds.ui.skill.refreshSpecialSkillWithoutIcon()
        if gameglobal.rds.ui.skill.detailMediator != None:
            gameglobal.rds.ui.skill.refreshDetailInfo()
        if gameglobal.rds.ui.skill.daoHangDirMediator != None:
            gameglobal.rds.ui.skill.refreshHaoHangDirectionPanel()
        gameglobal.rds.ui.skill.checkWsProficiency(skillId, proficiency)
        if lv > lastLv:
            skillInfo = SkillInfo(skillId, lv)
            mwsAdd = int(skillDataInfo.getWuShuangMwsAdd(skillInfo) / 100)
            if lastLv > 0:
                skillInfoLast = SkillInfo(skillId, lastLv)
                mwsAddLast = int(skillDataInfo.getWuShuangMwsAdd(skillInfoLast) / 100)
                diff = mwsAdd - mwsAddLast
            else:
                diff = mwsAdd
            type = 'wsType' + str(self.wsSkills[skillId].wsType)
            typeName = SPD.data.get(self.school, {}).get(type, '')
            self.showGameMsg(GMDD.data.WUSHUANG_LIMIT_UP, (str(typeName) + '  ', diff))
            gameglobal.rds.ui.actionbar.skillInfoCache.clear()
            gameglobal.rds.ui.guildWuShuangSelect.refreshInfo()
        if lv == 1:
            gameglobal.rds.ui.skill.refreshSpecialSkill()

    def updateWsSelect(self, skillId, select):
        gameglobal.rds.ui.skill.wushuangSkillSelectDone(skillId, select)

    def removePSkill(self, pskId, subSrc):
        if not subSrc:
            self.pskills.pop(pskId, None)
        else:
            if not self.pskills.has_key(pskId):
                return
            self.pskills[pskId].removePSkill(pskId, subSrc)
        gameglobal.rds.ui.actionbar.skillInfoCache.clear()

    def removeTriggerPSkill(self, pskillId):
        self.triggerPSkills.pop(pskillId, None)

    def skillTimeUpdate(self, skill, level, remainTime, cdStorage):
        super(self.__class__, self).skillTimeUpdate(skill, level, remainTime, cdStorage)
        gamelog.debug('@smj: skillTimeUpdate:', skill, remainTime, cdStorage)
        bwTime = BigWorld.time()
        recoverTime = skillDataInfo.getRecoverTime(SkillInfo(skill, level), 0)
        logicInfo.cooldownSkill[skill] = (remainTime + bwTime, recoverTime)
        gameglobal.rds.ui.actionbar.updateSlot(skill)
        if utils.isCDStorageSkill(skill, level):
            logicInfo.cdStorageSkill[skill] = [remainTime + bwTime, cdStorage]
            gameglobal.rds.ui.zaijuV2.refreshCdStoreage(skill)
        gameglobal.rds.ui.buffSkill.updateCooldown()

    def batchSkillTimeUpdate(self, data):
        gamelog.debug('jorsef: batchSkillTimeUpdate:', data)
        for skill, level, remainTime, cdStorage in data:
            self.skillTimeUpdate(skill, level, remainTime, cdStorage)

    def updateUseSkillKeyState(self):
        gamelog.debug('@zf:updateUseSkillKeyState', gameglobal.rds.bar, gameglobal.rds.soltId)
        if gameglobal.rds.bar != None and gameglobal.rds.soltId != None:
            skillId = skillLv = 0
            if self._isOnZaijuOrBianyao():
                if gameglobal.rds.ui.zaiju.mediator:
                    skillId, skillLv = gameglobal.rds.ui.zaiju.getSkillInfo(gameglobal.rds.soltId)
                else:
                    skillId, skillLv = gameglobal.rds.ui.zaijuV2.getSkillInfo(gameglobal.rds.soltId)
            else:
                skillId = gameglobal.rds.ui.actionbar.getShortCut(gameglobal.rds.bar, gameglobal.rds.soltId, [0, 0])[1]
                skillLv = gameglobal.rds.ui.actionbar._getSkillLv(skillId)
            if SGD.data.has_key((skillId, skillLv)):
                gameglobal.rds.ui.actionbar.useSkill(gameglobal.rds.bar, gameglobal.rds.soltId, True, autoUseSkill=True)
        else:
            self.useHoldingSkill()

    def stopCast(self, skillId, skillLv, targetId, stopAction):
        self.isWaitSkillReturn = False
        super(self.__class__, self).stopCast(skillId, skillLv, targetId, stopAction)

    def reliveByOtherRequest(self, srcId, timeInterval, srcRole):
        gamelog.debug('@zs impPlayerCombat.reliveByOtherRequest', srcId, timeInterval)
        t = BigWorld.entities.get(srcId)
        if t == None and not srcRole:
            self.cell.confirmRelive(gametypes.RELIVE_TYPE_BY_SKILL, 0)
            return
        else:
            if self.inFubenType(const.FB_TYPE_ARENA_ROUND) or self.inFubenType(const.FB_TYPE_ARENA_WING_WORLD_XINMO):
                gameglobal.rds.ui.deadAndRelive.show(False, False, True, [srcRole or t.roleName, timeInterval])
            else:
                gameglobal.rds.ui.deadAndRelive.beRelived(srcRole or t.roleName, timeInterval)
            return

    def onConfirmReliveByOther(self, ok):
        self.cell.confirmRelive(gametypes.RELIVE_TYPE_BY_SKILL, ok)
        if ok:
            BigWorld.callback(0.5, Functor(self.reliveResult, False))

    def pullByOtherRequest(self, sRoleName, timeInterval):
        gamelog.debug('@zs impPlayerCombat.pullByOtherRequest', sRoleName, timeInterval)
        msg = GMD.data.get(GMDD.data.PULL_BY_SKILL, {}).get('text', gameStrings.TEXT_IMPPLAYERCOMBAT_2221)
        msg = msg % sRoleName
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, lambda : self._confirmPullBySkill(1)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, lambda : self._confirmPullBySkill(0))]
        gameglobal.rds.ui.messageBox.show(True, gameStrings.TEXT_MONITOR_1277_1, msg, buttons, repeat=int(timeInterval))

    def _confirmPullBySkill(self, ok):
        BigWorld.player().cell.confirmPullBySkill(not not ok)

    def hasState(self, stateId, stateLayer = 0):
        if stateId in self.getStates() and (not stateLayer or sum((val[gametypes.STATE_INDEX_LAYER] for val in self.getStates()[stateId])) == stateLayer):
            return True
        if len(self.flagStates):
            states = [ t[0] for t in self.flagStates ]
            if stateId in states:
                if not stateLayer:
                    return True
                else:
                    return states.count(stateId) == stateLayer
        return False

    def calcStateAttrCache(self):
        self.stateAttrCache = set()
        for stateId in self.getStates().keys():
            stateInfo = StateInfo(stateId, 1)
            attrs = stateInfo.getStateData('allAttrIds', [])
            self.stateAttrCache.update(attrs)

    def hasStateAttr(self, attrId):
        if self.stateAttrCache == None:
            self.calcStateAttrCache()
        return attrId in self.stateAttrCache

    def getStateAttrs(self):
        if self.stateAttrCache == None:
            self.calcStateAttrCache()
        return self.stateAttrCache

    def inManDownState(self):
        return commcalc.getBitDword(self.flags, gametypes.FLAG_MAN_DOWN)

    def getSkillTargetType(self, skillInfo):
        skillTargetType, skillTargetValue = skillInfo.getSkillTargetType()
        state = skillInfo.getSkillData('tgtSelectState')
        if state and self.hasState(state):
            strategy = skillInfo.getSkillData('tgtSelectStrategy')
            key, value = strategy
            skillTargetType, skillTargetValue = gametypes.SKILL_TGT_DICT.get(key), value
        return (skillTargetType, skillTargetValue)

    def selectTeamerByIndex(self, down, index):
        if down:
            return
        memberId = []
        if self.inFubenTypes(const.FB_TYPE_ARENA):
            memberId = getattr(gameglobal.rds.ui.teamComm, 'memberId', [])
        elif self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            memberId = getattr(gameglobal.rds.ui.teamComm, 'memberId', [])
        elif self.isInTeamOrGroup():
            memberId = getattr(gameglobal.rds.ui.teamComm, 'memberId', [])
        gamelog.debug('selectTeamerByIndex', memberId)
        if not memberId:
            return
        if index < len(memberId):
            teamer = BigWorld.entity(memberId[index])
            if teamer and teamer.inWorld:
                self.lockTarget(teamer, lockAim=True, quickLock=True)

    def selectTeamerByTab(self, down):
        if down:
            return
        memberId = []
        if self.inFubenTypes(const.FB_TYPE_ARENA):
            memberId = getattr(gameglobal.rds.ui.teamComm, 'memberId', [])
        elif self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            memberId = getattr(gameglobal.rds.ui.teamComm, 'memberId', [])
        elif self.isInTeamOrGroup():
            memberId = getattr(gameglobal.rds.ui.teamComm, 'memberId', [])
        memNum = len(memberId)
        for idx in xrange(self.selectTeamerByTabIdx + 1, self.selectTeamerByTabIdx + memNum + 1):
            index = idx % memNum
            member = BigWorld.entities.get(memberId[index])
            if member and member.inWorld:
                self.selectTeamerByTabIdx = index
                self.lockTarget(member, lockAim=True)
                break

    def selectTeamer0(self, down):
        self.selectTeamerByIndex(down, 0)

    def selectTeamer1(self, down):
        self.selectTeamerByIndex(down, 1)

    def selectTeamer2(self, down):
        self.selectTeamerByIndex(down, 2)

    def selectTeamer3(self, down):
        self.selectTeamerByIndex(down, 3)

    def selectTeamerMe(self, down):
        self.lockTarget(self, lockAim=True)

    def selectTeamerMeSprite(self, down):
        if getattr(self, 'summonedSpriteInWorld', None):
            self.lockTarget(self.summonedSpriteInWorld)

    def checkPkProtectMode(self, protectMode):
        if protectMode not in const.ALL_PK_PROTECT_MODE:
            return False
        return commcalc.getBitDword(self.pkProtectMode, protectMode) > 0

    def getMapConfigPKProtectMode(self):
        return MCD.data.get(formula.getMapId(self.spaceNo), {}).get('pkProtectMode', ())

    def getMapConfigPKProtectLevel(self):
        return MCD.data.get(formula.getMapId(self.spaceNo), {}).get('pkProtectLevel', 0)

    def autoSetMapPkProtectConfig(self):
        pkMode = self.getMapConfigPKProtectMode()
        if pkMode:
            self.cell.setPkProtectMode(const.PK_PROTECT_MODE_GROUP, 1 in pkMode)
            self.cell.setPkProtectMode(const.PK_PROTECT_MODE_GUILD, 2 in pkMode)
            self.cell.setPkProtectMode(const.PK_PROTECT_MODE_GREEN, 3 in pkMode)
            self.cell.setPkProtectMode(const.PK_PROTECT_MODE_CLAN, 4 in pkMode)
        lvMode = self.getMapConfigPKProtectLevel()
        if lvMode:
            self.cell.setPkProtectLv(lvMode)

    def mouseOptimizeNoTarget(self, skillInfo):
        if self.getOperationMode() == gameglobal.MOUSE_MODE and gameglobal.INTELLIGENT_CAST:
            needTarget = skillDataInfo.isNeedTarget(skillInfo)
            graph1 = skillDataInfo.getGraph1(skillInfo)
            graph2 = skillDataInfo.getGraph2(skillInfo)
            graph3 = skillDataInfo.getGraph3(skillInfo)
            graph4 = skillDataInfo.getGraph4(skillInfo)
            graph = (graph1,
             graph2,
             graph3,
             graph4)
            skillRange = 0
            for item in graph:
                if item and item[1] > skillRange:
                    skillRange = item[1]

            if not needTarget and skillRange >= 2 and skillRange <= 6:
                result = self.circleEffect.getScreenPosInWorld(True)
                if result[0]:
                    direction = result[0] - self.position
                    self.faceToDir(direction.yaw, True, True)
                    return True
        return False

    def specialCheckForActionPhysics(self):
        return self.circleEffect.specialCheckForActionPhysics(self.skillId, self.skillLevel)

    def mouseOptimizePosition(self):
        if gameglobal.INTELLIGENT_CAST:
            check = self.specialCheckForActionPhysics()
            if check:
                self.showGameMsg(GMDD.data.DIST_TOO_FAR, ())
                if self.getOperationMode() == gameglobal.ACTION_MODE:
                    self.circleEffect.playIndicatorEff(check[0], True)
                return True
            self.circleEffect.cancel()
            self.circleEffect.start(self.skillId, self.skillLevel)
            self.circleEffect.run()
            return True
        return False

    def actionOptimizeForTarget(self, skillInfo):
        if self.getOperationMode() == gameglobal.ACTION_MODE:
            needTarget = skillDataInfo.isNeedTarget(skillInfo)
            if needTarget:
                self.ap.backToCamera()

    def actionOptimizeNoTarget(self, skillInfo):
        if self.getOperationMode() == gameglobal.ACTION_MODE:
            needTarget = skillDataInfo.isNeedTarget(skillInfo)
            if not needTarget:
                self.ap.backToCamera()

    def beHit(self, host, damage = None, callback = None, forceBeHitAct = False, clientSkillInfo = None):
        super(self.__class__, self).beHit(host, damage, callback, forceBeHitAct, clientSkillInfo)
        self.cancelTransportSpell(const.CANCEL_ACT_BE_HIT)
        self.cancelTreasureBoxSpell(const.CANCEL_ACT_BE_HIT)

    def getAllSkillEffects(self):
        skillEffects = []
        for skillInfo in self.skills.itervalues():
            clientSkillInfo = ClientSkillInfo(skillInfo.skillId, skillInfo.level)
            skillEffects.extend(skillDataInfo.getSkillEffect(clientSkillInfo))

        return skillEffects

    def getAllSkillEffectByZaijuId(self, zaijuId):
        skillEffects = []
        zaijuSkills = ZJD.data.get(zaijuId, {}).get('skills', [])
        for skillId, lv in zaijuSkills:
            clientSkillInfo = ClientSkillInfo(skillId, lv)
            skillEffects.extend(skillDataInfo.getSkillEffect(clientSkillInfo))

        return skillEffects

    def getAllSkillActions(self):
        skillActions = []
        for skillInfo in self.skills.itervalues():
            clientSkillInfo = ClientSkillInfo(skillInfo.skillId, skillInfo.level)
            skillActions.extend(skillDataInfo.getSkillAction(clientSkillInfo))

        return skillActions

    def getAllSkillActionsByZaijuId(self, zaijuId):
        skillActions = []
        zaijuSkills = ZJD.data.get(zaijuId, {}).get('skills', [])
        for skillId, lv in zaijuSkills:
            clientSkillInfo = ClientSkillInfo(skillId, lv)
            skillActions.extend(skillDataInfo.getSkillAction(clientSkillInfo))

        return skillActions

    def getAllQingGongActions(self):
        weapons = clientcom.getAllWeaponModel(self)
        capIndexSet = set()
        capIndexSet.add(keys.CAPS_HAND_FREE - 1)
        for item in weapons:
            capIndexSet.add(item.equipType - 1)

        qingGongActions = set([])
        qingGongActions = qingGongActions.union(set(ACT.getActionFromFlag('normalActions', self.fashion.action, capIndexSet)))
        if gametypes.PRELOAD_QINGGONG_ACTIONS:
            qingGongActions = qingGongActions.union(gametypes.PRELOAD_QINGGONG_ACTIONS)
        for qingGongFlag in gametypes.QINGGONG_SKILL_CANLEARN:
            if gametypes.LEARN_ALL_GQINGGONG:
                isLearned = True
            else:
                isLearned = True if self.qingGongSkills.has_key(qingGongFlag) else False
            if isLearned:
                qingGongActions = qingGongActions.union(set(ACT.getActionFromFlag(qingGongFlag, self.fashion.action, capIndexSet)))

        return qingGongActions

    def getPSkillInfo(self, psk):
        if psk == None:
            return
        else:
            lv = psk.level
            num = psk.id
            res = PSkillInfo(num, lv, psk.pData)
            return res

    def myPSkills(self):
        return self.pskills

    def hasPSkills(self, skillId):
        skills = self.myPSkills()
        return skills and skills.has_key(skillId) or False

    def myTriggerPSkills(self):
        return self.triggerPSkills

    def hasTriggerSkills(self, skillId):
        skills = self.myTriggerPSkills()
        return skills and skills.has_key(skillId) or False

    def checkPSkillTrigger(self, pskInfo, trigger, param):
        return combatUtils.checkPSkillTrigger(self, pskInfo, trigger, param, True)

    def getAllAffectPSkillInfo(self, dataType, dataId):
        if dataType == const.DATA_TYPE_SKILL_INFO:
            skillId = dataId
            pskills = PSRD.data.get(skillId, [])
        elif dataType == const.DATA_TYPE_SKILL_EFFECT_INFO:
            skillEffectId = dataId
            pskills = PSERD.data.get(skillEffectId, [])
        elif dataType == const.DATA_TYPE_STATE_INFO:
            stateId = dataId
            pskills = PSTRD.data.get(stateId, [])
        elif dataType == const.DATA_TYPE_COMBAT_CREATION_INFO:
            creationId = dataId
            pskills = PCRD.data.get(creationId, [])
        if not pskills:
            return []
        res = []
        for pskId in pskills:
            if self.myPSkills().has_key(pskId):
                psks = self.myPSkills()[pskId]
                for psk in psks.values():
                    pskInfo = self.getPSkillInfo(psk)
                    if pskInfo and psk.enable:
                        res.append((psk, pskInfo))

        return res

    def getSkillInfo(self, skillId, lv):
        skillInfo = SkillInfo(skillId, lv)
        skillInfo = commcalc.calcDataInfoAffectedByPSkill(self, skillInfo, const.DATA_TYPE_SKILL_INFO, skillId)
        if skillInfo.hijackData:
            fixLv = skillInfo.hijackData.get('skillCalcLvAdd')
            if fixLv:
                newLv = min(skillInfo.lv + fixLv, const.MAX_SKILL_LEVEL)
                newSkillInfo = SkillInfo(skillId, newLv)
                newSkillInfo.hijackData = skillInfo.hijackData
                return newSkillInfo
        return skillInfo

    def getCombatCreationInfo(self, cid, clv, srcSkillId, hijackData = None):
        creationInfo = CombatCreationInfo(cid, clv, srcSkillId)
        creationInfo = commcalc.calcDataInfoAffectedByPSkill(self, creationInfo, const.DATA_TYPE_COMBAT_CREATION_INFO, srcSkillId)
        return creationInfo

    def getSkillEffectInfo(self, effectId, effectLv, srcSkillId):
        skillEffectInfo = SkillEffectInfo(effectId, effectLv)
        skillEffectInfo = commcalc.calcDataInfoAffectedByPSkill(self, skillEffectInfo, const.DATA_TYPE_SKILL_EFFECT_INFO, srcSkillId)
        return skillEffectInfo

    def handleCombatMsg(self, msgs):
        if not isinstance(msgs, list):
            msgs = [msgs]
        for msgId, params in msgs:
            self.showGameMsg(msgId, params)

    def _showSkillNotReadyMsg(self, skillId, needSound = True, needBlockMsg = False):
        if skillId in gameglobal.rds.sound.lastUseSkill and time.time() - gameglobal.rds.sound.lastUseSkill[skillId] < SCD.data.get('successSoundCD', 0.5):
            if not needBlockMsg:
                self.showGameMsgEx(GMDD.data.SKILL_NOT_READY, (), False)
        elif not needBlockMsg:
            self.showGameMsgEx(GMDD.data.SKILL_NOT_READY, (), needSound)

    def getPrimaryPropBaseValue(self, propId):
        if self._isSchoolSwitch() or propId not in PDD.data.PRIMARY_PROPERTIES:
            return 0
        if propId == PDD.data.PROPERTY_ATTR_PW:
            v = self.primaryProp.bpow
        elif propId == PDD.data.PROPERTY_ATTR_INT:
            v = self.primaryProp.bint
        elif propId == PDD.data.PROPERTY_ATTR_PHY:
            v = self.primaryProp.bphy
        elif propId == PDD.data.PROPERTY_ATTR_SPR:
            v = self.primaryProp.bspr
        elif propId == PDD.data.PROPERTY_ATTR_AGI:
            v = self.primaryProp.bagi
        return v

    def skillQte(self, srcSkId, qteSkills, interval, lastTime, triggerTime, switchOn):
        if switchOn:
            lv = 1
            if self.wsSkills.has_key(srcSkId):
                lv = self.wsSkills[srcSkId].level
            elif self.skills.has_key(srcSkId):
                lv = self.skills[srcSkId].level
            for skId in qteSkills:
                self.skills[skId] = skillDataInfo.SkillInfoVal(skId, lv)
                self.skills[skId].enable = True

            self.skillQteData[srcSkId] = SkillQteInfoVal(srcSkId, interval, lastTime, triggerTime, qteSkills)
            if len(qteSkills):
                if gameglobal.rds.ui.zaijuV2.widget:
                    keyText = gameglobal.rds.ui.zaijuV2.changeIcon(srcSkId, qteSkills[0])
                else:
                    keyText = gameglobal.rds.ui.actionbar.changeIcon(srcSkId, qteSkills[0])
                existSkills = gameglobal.rds.ui.qteNotice.qteInfo
                qteInfo = [[qteSkills[0],
                  keyText,
                  lastTime,
                  self.getServerTime()]]
                for idx, skillId in enumerate(qteSkills[1:]):
                    keyText = gameglobal.rds.ui.qteNotice.getHotKeyDes(idx + 1)
                    qteInfo.append([skillId,
                     keyText,
                     lastTime,
                     self.getServerTime()])

                existSkills[srcSkId] = qteInfo
                if gameglobal.rds.ui.qteNotice.mediator:
                    gameglobal.rds.ui.qteNotice.setQteVisible(True)
                    gameglobal.rds.ui.qteNotice.refreshQteNotice(existSkills)
                if gameglobal.rds.configData.get('enableAutoUseQteSkills', False):
                    delay = 0.3
                    if logicInfo.commonCooldownWeaponSkill[0]:
                        if logicInfo.commonCooldownWeaponSkill[0] - BigWorld.time() > delay:
                            delay = logicInfo.commonCooldownWeaponSkill[0] - BigWorld.time() + 0.01
                    BigWorld.callback(delay, self.autoUseQteSkills)
        else:
            self.skillQteData.pop(srcSkId, None)
            gameglobal.rds.ui.actionbar.changeIcon(srcSkId, srcSkId)
            gameglobal.rds.ui.zaijuV2.changeIcon(srcSkId, srcSkId)
            gameglobal.rds.ui.qteNotice.removeQteInfo(srcSkId)
            if gameglobal.rds.ui.qteNotice.mediator and len(gameglobal.rds.ui.qteNotice.qteInfo) == 0:
                gameglobal.rds.ui.qteNotice.setQteVisible(False)

    def getZaijuSkillId(self, slot):
        if slot is None:
            return 0
        else:
            skills = ZJD.data.get(self.bianshen[1], {}).get('skills', [])
            if slot < len(skills):
                return skills[slot][0]
            return 0

    def autoUseQteSkills(self):
        skillId = None
        if self.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            skillId = self.getZaijuSkillId(gameglobal.rds.soltId)
        else:
            info = gameglobal.rds.ui.actionbar.getShortCut(gameglobal.rds.bar, gameglobal.rds.soltId, [0, 0])
            if not info:
                return
            skillId = info[1]
        val = self.skillQteData.get(skillId, None)
        if val and val.qteSkills:
            qteSkill = val.qteSkills[0]
            gameglobal.rds.ui.actionbar.useSkillById(qteSkill, True, True, False)

    def beUseSkillRequest(self, sRoleName, skillId, level, timeInterval):
        gamelog.debug('@zs impPlayerCombat.beUseSkillRequest', sRoleName, timeInterval)
        skInfo = SkillInfo(skillId, level)
        msg = skInfo.getSkillData('confirmMsg', gameStrings.TEXT_IMPPLAYERCOMBAT_2654)
        msg = msg % sRoleName
        buttons = [MBButton(gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, lambda : self._confirmBeUsekill(1)), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, lambda : self._confirmBeUsekill(0))]
        gameglobal.rds.ui.messageBox.show(True, gameStrings.TEXT_MONITOR_1277_1, msg, buttons, repeat=int(timeInterval))

    def _confirmBeUsekill(self, ok):
        BigWorld.player().cell.onConfirmBeUseSkill(not not ok)

    def updateAirSkill(self, skillId, lv, enable, exp):
        if self.airSkills.has_key(skillId):
            if lv == 0:
                del self.airSkills[skillId]
            else:
                self.airSkills[skillId].level = lv
                self.airSkills[skillId].enable = enable
                self.airSkills[skillId].exp = exp
        else:
            self.airSkills[skillId] = skillDataInfo.SkillInfoVal(skillId, lv)
            self.airSkills[skillId].enable = enable
            self.airSkills[skillId].exp = exp
            gameglobal.rds.ui.skill.onLearnNewAirSkill(skillId)
        gameglobal.rds.ui.skill.refreshAirSkillById(skillId)
        gameglobal.rds.ui.skill.airSkillActiveDone(skillId, enable)
        gameglobal.rds.ui.skill.refreshDetailInfo()
        gameglobal.rds.ui.skill.refreshAirSkillbar()
        gameglobal.rds.ui.airbar.refreshAirSkillBar()

    def addHoldingSkills(self, skillInfo):
        skillID = getattr(self.skillPlayer, 'skillID', 0)
        if skillID and not self.bianshen[0]:
            nowSkillInfo = gameglobal.rds.ui.actionbar._getSkillInfo(skillID)
            if nowSkillInfo and skillDataInfo.isGuideSkill(nowSkillInfo):
                return
        if skillInfo:
            self.holdingSkills.append(skillInfo)

    def clearHoldingSkills(self):
        self.holdingSkills = []

    def getHoldingSkillForCast(self):
        if self.holdingSkills:
            skillIdForCast = self.holdingSkills.pop()
            self.holdingSkills = []
            return skillIdForCast
        else:
            return None

    def begingDropForBlood(self, dropType):
        gameStrings.TEXT_IMPPLAYERCOMBAT_2707
        if self.canFly():
            return
        self.dropForBlood = (dropType, self.position.y)

    def clearDropForBlood(self):
        self.dropForBlood = (0, 0)

    def refreshPkToplogo(self):
        if self.inFuben():
            for en in BigWorld.entities.values():
                if en.IsAvatar and en.topLogo:
                    en.topLogo.hidePkTopLogo()

        else:
            for en in BigWorld.entities.values():
                if en.IsAvatar and en.topLogo:
                    en.topLogo.updatePkTopLogo()

    def addInDyingEntityId(self, entityId):
        gamelog.debug('----addInDyingEntityId', entityId)
        enterInDying = True if self.inDyingEntities else False
        if entityId not in self.inDyingEntities:
            self.inDyingEntities.append(entityId)
            if not enterInDying:
                self.playInDyingEffect()

    def removeInDyingEntityId(self, entityId):
        gamelog.debug('----removeInDyingEntityId', entityId)
        hadDying = len(self.inDyingEntities) > 0
        if entityId in self.inDyingEntities:
            self.inDyingEntities.remove(entityId)
        if not self.inDyingEntities and hadDying:
            self.stopInDyingEffect()

    def clearInDyingEntity(self):
        gamelog.debug('----clearInDyingEntity')
        if self.inDyingEntities:
            self.inDyingEntities = []
            self.stopInDyingEffect()

    def hasInDyingAround(self):
        return self.inDyingEntities

    def playInDyingEffect(self):
        if self.getEffectLv() < gameglobal.EFFECT_MID:
            return
        gamelog.debug('----playInDyingEffect', self.inDyingEntities, gameglobal.IN_DYING_TINT_FOR_PLAYER)
        BigWorld.setBlackTime(1, gameglobal.IN_DYING_BLACK_TIME, 1, 0.5, 0.5, 0.5)
        p = BigWorld.player()
        p.addTint(gameglobal.IN_DYING_TINT_FOR_PLAYER, p.allModels)

    def stopInDyingEffect(self):
        p = BigWorld.player()
        gamelog.debug('----stopInDyingEffect', p.tintStateType[1], self.inDyingEntities)
        BigWorld.setBlackTime(0, 0, 0, 0.5, 0.5, 0.5)
        if hasattr(p, 'tintStateType') and p.tintStateType[1]:
            tintalt.ta_del(p.allModels, p.tintStateType[1])
            p.restoreTintStateType()

    def weaponInHand(self, isDown):
        if isDown:
            p = BigWorld.player()
            if p.fashion.doingActionType() in (ACT.SHOW_WEAPON_ACTION, ACT.HANG_WEAPON_ACTION):
                return
            if self.weaponState == gametypes.WEAPON_HANDFREE:
                if not p.stateMachine.checkStatus(const.CT_WEAPON_IN_HAND):
                    return
                if self.inWeaponCallback:
                    BigWorld.cancelCallback(self.inWeaponCallback)
                self.fashion.stopAllActions()
                self.switchWeaponState(gametypes.WEAPON_DOUBLEATTACH)
            else:
                if self.inCombat:
                    return
                if not p.stateMachine.checkStatus(const.CT_WEAPON_HAND_FREE):
                    return
                self.fashion.stopAllActions()
                self.switchWeaponState(gametypes.WEAPON_HANDFREE)

    def isCombatUnit(self, target):
        if target == None:
            return False
        elif hasattr(target, 'life') and target.life == gametypes.LIFE_DEAD:
            return False
        else:
            return getattr(target, 'IsCombatUnit', False)

    def getSkills(self):
        return DictZipper(self.wsSkills, self.skills, self.airSkills)

    def sendAirSkillInfo(self, skills):
        for skillId, enable, lv, exp in skills:
            self.airSkills[skillId] = skillDataInfo.SkillInfoVal(skillId, lv)
            self.airSkills[skillId].enable = enable
            self.airSkills[skillId].exp = exp

    def set_skillPointSchemeIndex(self, old):
        self.dispatchEvent(const.EVENT_UPDATE_SKILL_SCHEME, ())
        gameglobal.rds.ui.skill.setSchemeName()

    def skillPointSchemeSend(self, schemes):
        if not hasattr(self, 'skillPointScheme') or not self.skillPointScheme:
            self.skillPointScheme = schemes
        else:
            for newVal in schemes:
                for i, oldVal in enumerate(self.skillPointScheme):
                    if oldVal[0] == newVal[0]:
                        self.skillPointScheme[i] = newVal
                        break
                else:
                    self.skillPointScheme.append(newVal)

        self.dispatchEvent(const.EVENT_UPDATE_SKILL_SCHEME, ())
        gameglobal.rds.ui.skill.setSchemeName()
        gameglobal.rds.ui.skill.updateArenaSkillInfo()

    def getSkillSchemeConvertById(self, schemeNo):
        schemeOld = self.getSkillSchemeById(schemeNo)
        scheme = {}
        if schemeOld:
            scheme['schemeName'] = schemeOld[2]
            scheme['status'] = schemeOld[3]
            scheme['expireTime'] = schemeOld[4]
        return scheme

    def getSkillSchemeById(self, schemeNo):
        scheme = None
        for i in xrange(0, len(self.skillPointScheme)):
            if self.skillPointScheme[i][0] == schemeNo:
                scheme = self.skillPointScheme[i]

        return scheme

    def getSpecialSkillPoint(self):
        if gameglobal.rds.configData.get('enableWingWorldSkillScheme', False) and gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_WINGWORLD:
            return self.getWWSkillPoint()
        elif gameglobal.rds.configData.get('enableCrossBFSkillScheme', False) and gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_CROSS_BF:
            return self.getCrossBFkillPoint()
        else:
            return self.getArenaSkillPoint()

    def getArenaSkillPoint(self):
        gamelog.info('jbx:getArenaSkillPoint')
        skillScheme = self.getSkillSchemeById(const.SKILL_SCHEME_ARENA)
        if skillScheme:
            return skillScheme[1]
        return {}

    def getCrossBFkillPoint(self):
        gamelog.info('jbx:getCrossBFkillPoint')
        skillScheme = self.getSkillSchemeById(const.SKILL_SCHEME_CROSS_BF)
        if skillScheme:
            return skillScheme[1]
        return {}

    def getWWSkillPoint(self):
        gamelog.info('jbx:getWWSkillPoint')
        skillScheme = self.getSkillSchemeById(const.SKILL_SCHEME_WINGWORLD)
        if skillScheme:
            return skillScheme[1]
        return {}

    def getArenaSkills(self):
        skillPointScheme = self.getSpecialSkillPoint()
        ret = {}
        for skillId, skillVal in self.skills.iteritems():
            schemeSkillVal = skillPointScheme.get(skillId, {})
            ret[skillId] = skillDataInfo.SkillInfoVal(skillId, schemeSkillVal.get('level', 1))
            for i in xrange(const.MAX_XIULIAN_ROW):
                for j in xrange(const.MAX_XIULIAN_COLUMN):
                    part = int('%d%d' % (i + 1, j + 1))
                    if not SED.data.has_key((skillId, part)):
                        continue
                    enhData = SED.data[skillId, part]
                    if skillVal.hasLearned(part) or enhData.get('initLearn', 0):
                        enhanceVal = CSkillEnhanceVal(const.SKILL_ENHANCE_STATE_INACTIVE, 0, 0)
                        enhancePoint = schemeSkillVal.get('enhanceData', {}).get(part, {}).get('enhancePoint', 0)
                        if enhancePoint:
                            enhanceVal.enhancePoint = enhancePoint
                            enhanceVal.state = const.SKILL_ENHANCE_STATE_ACTIVE
                        ret[skillId].enhanceData[part] = enhanceVal

        return ret

    def _soulArenaSkill(self):
        if gameglobal.rds.ui.skill.isEditMode:
            return self.getArenaSkills()
        return self.skills

    arenaSkill = property(_soulArenaSkill, '', '', '')

    def _soulArenaLv(self):
        skillProxy = gameglobal.rds.ui.skill
        if skillProxy.isEditMode:
            if not gameglobal.rds.configData.get('enableWingWorldSkillScheme', False):
                schemeData = utils.getArenaSkillSchemeData(self.realLv)
                return schemeData.get('toLv', self.realLv)
            if self.skillPointSchemeIndex == const.SKILL_SCHEME_ARENA or gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_ARENA:
                schemeData = utils.getArenaSkillSchemeData(self.realLv)
                return schemeData.get('toLv', self.realLv)
            if self.skillPointScheme == const.SKILL_SCHEME_WINGWORLD or gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_WINGWORLD:
                schemeData = utils.getWingWorldSkillSchemaData(self.getWingWorldGroupId())
                return schemeData.get('toLv', self.realLv)
            if self.skillPointScheme == const.SKILL_SCHEME_CROSS_BF or gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_CROSS_BF:
                schemeData = utils.getCrossBFSkillSchemaData(self.lv)
                return schemeData.get('toLv', self.realLv)
        return self.realLv

    arenaLv = property(_soulArenaLv, '', '', '')

    def _soulArenaJingJie(self):
        skillProxy = gameglobal.rds.ui.skill
        if skillProxy.isEditMode:
            if not gameglobal.rds.configData.get('enableWingWorldSkillScheme', False):
                schemeData = utils.getArenaSkillSchemeData(self.realLv)
                return schemeData.get('arenaJingjie', self.jingJie)
            if self.skillPointSchemeIndex == const.SKILL_SCHEME_ARENA or gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_ARENA:
                schemeData = utils.getArenaSkillSchemeData(self.realLv)
                return schemeData.get('arenaJingjie', self.jingJie)
            if self.skillPointScheme == const.SKILL_SCHEME_WINGWORLD or gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_WINGWORLD:
                schemeData = utils.getWingWorldSkillSchemaData(self.getWingWorldGroupId())
                return schemeData.get('wingJingjie', self.jingJie)
            if self.skillPointScheme == const.SKILL_SCHEME_CROSS_BF or gameglobal.rds.ui.skillSchemeV2.editorIndex == const.SKILL_SCHEME_CROSS_BF:
                schemeData = utils.getCrossBFSkillSchemaData(self.lv)
                return schemeData.get('jingJie', self.jingJie)
        return self.jingJie

    arenaJingJie = property(_soulArenaJingJie, '', '', '')

    def getAllSkillScheme(self):
        allSchemes = {}
        for i in xrange(0, len(self.skillPointScheme)):
            schemeList = self.skillPointScheme[i]
            scheme = {}
            schemeNo = schemeList[0]
            if schemeList[2]:
                scheme['schemeName'] = schemeList[2]
            else:
                scheme['schemeName'] = self.getSkillSchemeName(schemeNo)
            scheme['status'] = schemeList[3]
            scheme['expireTime'] = schemeList[4]
            allSchemes[schemeNo] = scheme

        if not self.skillPointScheme:
            allSchemes[0] = {'status': 0,
             'expireTime': 0,
             'schemeName': self.getSkillSchemeName(0)}
        return allSchemes

    def getSkillSchemeName(self, schemeNo):
        scheme = self.getSkillSchemeById(schemeNo)
        if scheme:
            if not scheme[2]:
                return self.getSkillSchemeDefaultName(schemeNo)
            else:
                return scheme[2]
        else:
            return self.getSkillSchemeDefaultName(schemeNo)

    def getSkillSchemeDefaultName(self, schemeNo):
        if schemeNo < 3:
            idx = schemeNo + 1
            schemeName = gameStrings.TEXT_IMPPLAYERCOMBAT_2986 % idx
        else:
            schemeName = gameStrings.TEXT_IMPPLAYERCOMBAT_2988
        return schemeName

    def checkSkillSchemeOutOfDate(self, schemeNo):
        scheme = self.getSkillSchemeById(schemeNo)
        if scheme:
            if scheme[4]:
                if schemeNo == 0:
                    return False
                elif scheme[4] == 0 or scheme[4] >= self.getServerTime():
                    return False
                else:
                    return True
            elif schemeNo in (0, const.SKILL_SCHEME_ARENA, const.SKILL_SCHEME_CROSS_BF):
                return False
            else:
                return True

        else:
            return True

    def updatePropScheme(self, schemeNo, scheme, schemeName, status, expireTime):
        gamelog.debug('@jinjj updatePropScheme', schemeNo, scheme, schemeName, status, expireTime)
        if not hasattr(self, 'propScheme'):
            self.propScheme = {}
        if schemeName == '':
            schemeName = self.getSchemeDefaultName(schemeNo)
        scheme = {'scheme': list(scheme),
         'schemeName': schemeName,
         'status': status,
         'expireTime': expireTime}
        self.propScheme[schemeNo] = scheme
        self.dispatchEvent(const.EVENT_UPDATE_PROP_SCHEME, (schemeNo, scheme))

    def getSchemeDefaultName(self, schemeNo):
        if schemeNo == 0:
            schemeName = gameStrings.TEXT_IMPPLAYERCOMBAT_3025
        elif schemeNo == 1 or schemeNo == 2:
            schemeName = gameStrings.TEXT_IMPPLAYERCOMBAT_3027 % schemeNo
        else:
            schemeName = gameStrings.TEXT_IMPPLAYERCOMBAT_3029
        return schemeName

    def getSchemeName(self, schemeNo):
        scheme = self.getPropSchemeById(schemeNo)
        if scheme:
            if not scheme['schemeName']:
                return self.getSchemeDefaultName(schemeNo)
            else:
                return scheme['schemeName']
        else:
            return self.getSchemeDefaultName(schemeNo)

    def getAllPropScheme(self):
        return getattr(self, 'propScheme', {})

    def getPropSchemeById(self, schemeNo):
        allProps = self.getAllPropScheme()
        if allProps.has_key(schemeNo):
            return allProps[schemeNo]
        else:
            return {}

    def checkSchemeOutOfDate(self, schemeNo):
        scheme = self.getPropSchemeById(schemeNo)
        if scheme:
            if scheme.has_key('expireTime'):
                if scheme['expireTime'] == 0 or scheme['expireTime'] >= self.getServerTime():
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True

    def set_curPropScheme(self, old):
        gamelog.debug('set_curPropScheme', self.curPropScheme, old)
        scheme = self.getPropSchemeById(self.curPropScheme)
        if self.curPropScheme != old:
            BigWorld.player().showGameMsg(GMDD.data.UPDATE_PROP_CHEME_SUCCESS, self.getSchemeName(self.curPropScheme))
        self.dispatchEvent(const.EVENT_UPDATE_PROP_SCHEME, (self.curPropScheme, scheme))

    def propSchemeSend(self, data):
        for i in data:
            self.updatePropScheme(i[0], i[1], i[2], i[3], i[4])

    def updatePvpEnhance(self, data):
        gameglobal.rds.ui.pvpEnhance.updateInfo(data)

    def switchAvatarRelationByCamp(self, enable):
        relationCommon.switchAvatarRelationByCamp(enable)

    def getBeast(self):
        ents = utils.getEntityList('SummonedBeast')
        for ent in ents:
            if ent.ownerId == self.id:
                return ent

    def onSetWSSchemeNameRes(self, isOK, schemeID, newName):
        if isOK:
            if not self.WSSchemeInfo.has_key(schemeID):
                self.WSSchemeInfo[schemeID] = {}
            self.WSSchemeInfo[schemeID]['schemeName'] = newName
            gameglobal.rds.ui.schemeSwitch.refreshInfo()
            if schemeID == self.getCurWSSchemeNo():
                gameglobal.rds.ui.skill.refreshWSSchemeInfo()

    def onSwitchWSSchemeRes(self, isOK, newSchemeID):
        if isOK:
            self.WSSchemeInfo['schemeNo'] = newSchemeID
            gameglobal.rds.ui.schemeSwitch.refreshInfo()
            gameglobal.rds.ui.skill.refreshWSSchemeInfo()
            if gameglobal.rds.configData.get('enableWSSchemeHotKeys', False):
                self.base.getWSSchemeHotKeys(newSchemeID)

    def onGetWSSchemeHotKeys(self, schemeID, data):
        if not gameglobal.rds.configData.get('enableWSSchemeHotKeys', False):
            return
        if schemeID != self.getCurWSSchemeNo():
            return
        try:
            newShortCut = cPickle.loads(zlib.decompress(data))
        except:
            newShortCut = {}

        if not newShortCut:
            return
        gameglobal.rds.ui.skill.wsSkillChangeFromShortCut(newShortCut)

    def getCurWSSchemeNo(self):
        return self.WSSchemeInfo.get('schemeNo', 0)

    def getCurWSSchemeName(self):
        return self.getWSSchemeName(self.getCurWSSchemeNo())

    def getWSSchemeName(self, schemeNo):
        schemeName = self.WSSchemeInfo.get(schemeNo, {}).get('schemeName', '')
        if schemeName == '':
            schemeName = uiUtils.getDefaultSchemeName(uiConst.SCHEME_SWITCH_WUSHUANG, schemeNo)
        return schemeName

    def getWSSchemeExpireTime(self, schemeNo):
        return self.WSSchemeInfo.get(schemeNo, {}).get('expireTime', 0)

    def onGetWSSchemesInfo(self, currSchemeID, timeExtra1, timeExtra2, timeSpecial, nameDefault, nameExtra1, nameExtra2, nameSpecial):
        self.WSSchemeInfo = {'schemeNo': currSchemeID,
         const.WUSHUANG_SCHEME_ID_DEFAULT: {'schemeName': nameDefault,
                                            'expireTime': 0},
         const.WUSHUANG_SCHEME_ID_EXTRA_1: {'schemeName': nameExtra1,
                                            'expireTime': timeExtra1},
         const.WUSHUANG_SCHEME_ID_EXTRA_2: {'schemeName': nameExtra2,
                                            'expireTime': timeExtra2},
         const.WUSHUANG_SCHEME_ID_SPECIAL: {'schemeName': nameSpecial,
                                            'expireTime': timeSpecial}}

    def onRenewalWSSchemeTimeRes(self, isOK, schemeID, timeEndBefore, timeEndAfter):
        if isOK:
            if not self.WSSchemeInfo.has_key(schemeID):
                self.WSSchemeInfo[schemeID] = {}
            self.WSSchemeInfo[schemeID]['expireTime'] = timeEndAfter
            gameglobal.rds.ui.schemeSwitch.refreshInfo()

    def equipSoulSchemeSend(self, data):
        for schemoNo, scheme, name, _, expireTime in data:
            self.equipSoulSchemeInfo[schemoNo] = {'name': name,
             'expireTime': expireTime,
             'schemeData': scheme}

    def onThrownIsolatedCreationPos(self, pos):
        print '@smj onThrownIsolatedCreationPos', pos

    def onThrownIsolatedCreationEff(self, data):
        print '@smj onThrownIsolatedCreationEff'

    def pathFindingTo(self, seekPos, spaceNo):
        navigator.getNav().pathFinding((seekPos[0],
         seekPos[1],
         seekPos[2],
         spaceNo))

    def inHighLoadScene(self):
        return self.inClanWar or formula.spaceInWorldWarEx(self.spaceNo) or formula.spaceInWingWarCity(self.spaceNo)

    def inTeleportMove(self):
        return getattr(self, 'teleportMoveHandle', None)

    def startTeleportMove(self):
        self.stopTeleportMove()
        self.teleportMoveHandle = BigWorld.callback(gameglobal.rds.configData.get('teleportMoveDelayTime', 0.3), self.finishTeleportMove)

    def stopTeleportMove(self):
        if getattr(self, 'teleportMoveHandle', None):
            BigWorld.cancelCallback(self.teleportMoveHandle)
            self.teleportMoveHandle = None

    def finishTeleportMove(self):
        self.stopTeleportMove()
        if getattr(self, 'teleportMoveCallback', None):
            self.teleportMoveCallback()
            self.teleportMoveCallback = None

    def setTeleportMoveCallback(self, callback):
        self.teleportMoveCallback = callback

    def skillResultPB(self, bytes):
        super(self.__class__, self).skillResultPB(bytes)
        import combatProto
        skillResult = combatProto.skillResultProtoClient(bytes)
        if skillResult is None:
            return
        else:
            castDelayClientThreshold = utils.getSkillDelayCastStatParams() and utils.getSkillDelayCastStatParams()[-1] or 0
            if castDelayClientThreshold > 0 and skillResult.timeStamp > 0:
                tNow = BigWorld.player().getServerTime()
                gamelog.debug('@zhoukun, Avatar skillResultPB,', tNow, skillResult.timeStamp, castDelayClientThreshold)
                if tNow - skillResult.timeStamp > castDelayClientThreshold:
                    self.skillCastDelayInfo.append(tNow - skillResult.timeStamp)
                    if self.skillCastDelayCallback:
                        BigWorld.cancelCallback(self.skillCastDelayCallback)
                        self.skillCastDelayCallback = None
                    self.skillCastDelayCallback = BigWorld.callback(3.0, self._reportSkillCastDelay)
            return

    def _reportSkillCastDelay(self):
        if self.skillCastDelayInfo:
            BigWorld.player().cell.reportSkillCastDelay(self.skillCastDelayInfo)
        self.skillCastDelayInfo = []
        self.skillCastDelayCallback = None

    def set_dmgStats(self, old):
        gamelog.debug('@dxk set_dmgStats', self.dmgStats)
