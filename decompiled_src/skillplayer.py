#Embedded file name: /WORKSPACE/data/entities/client/helpers/skillplayer.o
import random
import inspect
import BigWorld
import Math
import utils
import const
import gamelog
import gameglobal
import gametypes
import clientcom
import skillDataInfo
import logicInfo
import combatProto
import formula
from gameclass import SkillInfo
from callbackHelper import Functor
from sfx import sfx
from sfx import flyEffect
from sfx import clientEffect
from sfx import screenEffect
from sfx import fenShenEffect
from helpers import action
from helpers import tintalt
from helpers import impSkillPlayerFly
from impSkillPlayerGetData import ImpSkillPlayerGetData
from impSkillPlayerFly import ImpSkillPlayerFly
from impSkillPlayerCue import ImpSkillPlayerCue
from cdata import game_msg_def_data as GMDD
from data import skill_movement_data as SMD
from data import skill_fenshen_appearance_data as SFAD
MONSTER_SKILL = 99999
SKILL_CLIENT_ARG_MAP = {gameglobal.SE_SPELLSTART: gametypes.SKILL_CLIENT_ARG_SPELLSTART,
 gameglobal.SE_SPELL: gametypes.SKILL_CLIENT_ARG_SPELL,
 gameglobal.SE_CAST: gametypes.SKILL_CLIENT_ARG_CAST,
 gameglobal.SE_CASTSTOP: gametypes.SKILL_CLIENT_ARG_CASTSTOP}

class SkillPlayerMeta(type):

    def __init__(cls, name, bases, dic):
        super(SkillPlayerMeta, cls).__init__(name, bases, dic)
        inherits = (ImpSkillPlayerGetData, ImpSkillPlayerFly, ImpSkillPlayerCue)
        for inherit in inherits:
            SkillPlayerMeta._moduleMixin(cls, name, inherit)

    def _moduleMixin(cls, name, module):
        for name, fun in inspect.getmembers(module, inspect.ismethod):
            setattr(cls, name, fun.im_func)

        for name, memb in inspect.getmembers(module):
            if name == '__module__':
                continue
            if memb.__class__.__name__ in const.BUILTIN_OBJS:
                setattr(cls, name, memb)


class SkillPlayer(object):
    __metaclass__ = SkillPlayerMeta

    def __init__(self, owner):
        self.owner = owner
        self.target = None
        self.skillID = None
        self.skillLevel = None
        self.keepTime = 0
        self.castActionCue = []
        self.castCurveCue = []
        self.castEffect = []
        self.noLoopEffectCallBackTimer = []
        self.guidCastEffects = []
        self.spellWarnEffects = []
        self.flyBias = 0
        self.targetPos = None
        self.targetPosFx = []
        self.shakeCameraCB = []
        self.guideStopPos = None
        self.castLoop = False
        self.delayDamageCalc = 0
        self.flyerSync = {}
        self.damageResult = {}
        self.flyTargets = {}
        self.useAttackPoint = False
        self.skillStart = False
        self.stateKit = -1
        self.skillKit = -1
        self.castIndex = [-1, 0, -1]
        self.effectConnector = {}
        self.spellConnector = None
        self.guideLoopCallback = None
        self.monsterMoveCallback = None
        self.chargeStages = None
        self.chargeNowStage = -1
        self.chargeStageCallbacks = []
        self.chargingEffects = []
        self.endWeaponState = 0
        self.inWeaponBuff = None
        self.curveCallbacks = []
        self.hasPlayedWeaponAction = False
        self.animateInfo = None
        self.weaponEffects = []
        self.freezedEffs = []

    def release(self):
        self.target = None
        self.skillID = None
        self.skillLevel = None
        self.keepTime = 0
        self.castActionCue = []
        self.castCurveCue = []
        self.flyBias = 0
        self.targetPos = None
        self.castLoop = False
        self.stopGuideEffect()
        self.__stopSpellWarnEffect()
        self.__stopSpellConnector()
        self._releaseChargeEff()
        self.shakeCameraCB = []
        self.guideStopPos = None
        self.delayDamageCalc = 0
        self.flyerSync.clear()
        self.damageResult.clear()
        self.flyTargets.clear()
        self.useAttackPoint = False
        self.skillStart = False
        self.stateKit = -1
        self.skillKit = -1
        self.stateIndex = [-1, -1, -1]
        self.curveCallbacks = []
        self.chargeNowStage = -1
        self.chargeStages = None
        self.cancelChargeStageCallback()
        self.cancelMonsterMoveCallback()
        self.animateInfo = []

    def releaseWeaponEffect(self):
        if self.weaponEffects:
            for ef in self.weaponEffects:
                if ef:
                    ef.stop()

            self.weaponEffects = []

    def playFenShen(self, skillInfo, clientSkillInfo):
        owner = BigWorld.entity(self.owner)
        skillId = skillInfo.num
        fenshenIds = []
        if hasattr(owner, 'skillAppearancesDetail'):
            appId = owner.skillAppearancesDetail.getCurrentAppearance(skillId)
            if appId != -1:
                fenshenIds = SFAD.data.get((skillId, appId), {}).get('createFenshenForcePosition', ())
        gamelog.debug('ypc@ fenshenIds', fenshenIds)
        if not fenshenIds:
            datas = skillInfo.getSkillData('createFenshenForcePosition', ())
            fenshenIds = [ d[0] for d in datas ]
        if not fenshenIds:
            return
        for info in fenshenIds:
            fenShenEffect.startFenShen(self.owner, info, owner.position, owner.position, owner.yaw)

    def playCountdown(self, skillInfo, clientSkillInfo, castType):
        skillCountdown = clientSkillInfo.getSkillData('skillCountdown', None)
        if not skillCountdown:
            return
        skillName = skillDataInfo.getSkillName(skillInfo)
        duration = skillCountdown.get(castType, 0)
        if duration <= 0:
            return
        gameglobal.rds.ui.skillCountdown.showCountdown(self.owner, skillName, castType, duration, clientSkillInfo.getSkillData('fadeOutTime', 0))

    def stopCountdown(self, skillInfo, clientSkillInfo):
        gameglobal.rds.ui.skillCountdown.closeCountdown(self.owner)
        needBeBreakHint = clientSkillInfo.getSkillData('needBeBreakHint', 0)
        if not needBeBreakHint:
            return
        gameglobal.rds.ui.skillBeBreak.show(self.owner, clientSkillInfo.getSkillData('beBreakFadeOutTime', 0))

    def playWeaponEffect(self, model, effectIds):
        self.releaseWeaponEffect()
        if not model or not effectIds:
            return 'Scene Root'
        owner = BigWorld.entity(self.owner)
        for ef in effectIds:
            effs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
             owner.getSkillEffectPriority(),
             model,
             ef,
             sfx.EFFECT_LIMIT,
             gameglobal.EFFECT_LAST_TIME))
            if effs:
                self.weaponEffects.extend(effs)

    def playWeaponAction(self, skillInfo, clientSkillInfo, needUpdateWeaponAction = True):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if self.hasPlayedWeaponAction:
            return
        weaponAction = self.getActionName(gameglobal.S_WEAPON_ACTION, skillInfo, changeCastNo=False, clientSkillInfo=clientSkillInfo)
        weaponEffs = skillDataInfo.getSkillEffects(clientSkillInfo, gameglobal.S_WEAPON_ACTION)
        if not weaponAction:
            return
        if hasattr(owner.modelServer, 'leftWeaponModel'):
            if owner.modelServer.leftWeaponModel.attachHasAni:
                model = owner.modelServer.leftWeaponModel.model
                callBack = None
                if needUpdateWeaponAction:
                    callBack = owner.modelServer.leftWeaponModel.updateWeaponAction
                if model and model.inWorld:
                    if tuple(model.queue) == ('1101',):
                        self.hasPlayedWeaponAction = True
                        owner.fashion.playActionSequence(model, [weaponAction], Functor(self.afterWeaponAction, callBack), 1, 0, releaseFx=False)
                    self.playWeaponEffect(model, weaponEffs)
        if hasattr(owner.modelServer, 'rightWeaponModel'):
            if owner.modelServer.rightWeaponModel.attachHasAni:
                model = owner.modelServer.rightWeaponModel.model
                callBack = None
                if needUpdateWeaponAction:
                    callBack = owner.modelServer.rightWeaponModel.updateWeaponAction
                if model and model.inWorld:
                    if tuple(model.queue) == ('1101',):
                        self.hasPlayedWeaponAction = True
                        owner.fashion.playActionSequence(model, [weaponAction], Functor(self.afterWeaponAction, callBack), 1, 0)
                        self.playWeaponEffect(model, weaponEffs)

    def afterWeaponAction(self, callback):
        self.releaseWeaponEffect()
        self.hasPlayedWeaponAction = False
        if callback:
            callback()

    def playFollowAvatarModelAction(self, actions):
        enableNewSchoolSummon = gameglobal.rds.configData.get('enableNewSchoolSummon', False)
        if not enableNewSchoolSummon:
            return
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if hasattr(owner.modelServer, 'avatarFollowModel') and owner.modelServer.avatarFollowModel:
            model = owner.modelServer.avatarFollowModel.model
            if model and model.inWorld:
                owner.fashion.playActionSequence(model, actions, None, 1, 0)

    def pushDamage(self, skillID, damageResult):
        if not damageResult:
            return
        if self.damageResult.has_key(skillID):
            self.damageResult[skillID].append(damageResult)
        else:
            self.damageResult[skillID] = [damageResult]

    def updateSkillState(self, skillInfo, skillcd, skillGcd, instant = True):
        owner = BigWorld.entity(self.owner)
        if not gameglobal.rds.isSinglePlayer:
            skillId = skillInfo.num
            t = BigWorld.time()
            if instant:
                if skillGcd <= 0.0:
                    skillGcd = skillDataInfo.getCommonCoolDown(skillInfo, 0)
                logicInfo.commonCooldownWeaponSkill = (skillGcd + t, skillGcd, skillId)
            if skillcd <= 0.0:
                skillcd = skillDataInfo.getRecoverTime(skillInfo, 0)
            gameglobal.rds.ui.actionbar.cancelCooldownCallback(skillId)
            cdExpire = logicInfo.cooldownSkill.get(skillId, (0, 0))[0]
            if t > cdExpire:
                logicInfo.cooldownSkill[skillId] = (skillcd + t, skillcd)
            if skillInfo.hasSkillData('cdAssoSkills'):
                cdAssoSkills = skillInfo.getSkillData('cdAssoSkills')
                for sId in cdAssoSkills:
                    sk = owner.skills.get(sId) if owner.skills.has_key(sId) else owner.wsSkills.get(sId)
                    sk = sk if sk else owner.zaijuSkills.get(sId)
                    if not sk:
                        continue
                    sInfo = owner.getSkillInfo(sId, sk.level)
                    skillcd = skillDataInfo.getRecoverTime(sInfo, 0)
                    cdExpire = logicInfo.cooldownSkill.get(sId, (0, 0))[0]
                    if t > cdExpire:
                        logicInfo.cooldownSkill[skillId] = (skillcd + t, skillcd)

            gameglobal.rds.ui.actionbar.cancelAllCallback()
            gameglobal.rds.ui.actionbar.updateSlots()
            gameglobal.rds.ui.buffSkill.updateCooldown()
            if hasattr(gameglobal.rds, 'tutorial'):
                gameglobal.rds.tutorial.onUseSkill(skillId)
            if owner == BigWorld.player():
                owner.tLastMoving = utils.getNow()

    def updateCastDelayOnlySkillState(self, skillInfo, skillcd):
        if not gameglobal.rds.isSinglePlayer:
            skillId = skillInfo.num
            t = BigWorld.time()
            logicInfo.cooldownSkill[skillId] = (skillcd + t, skillcd)
            if skillcd <= 0.0:
                skillcd = skillDataInfo.getRecoverTime(skillInfo, 0)
                logicInfo.cooldownSkill[skillId] = (skillcd + t, skillcd)

    def playBeCastedEffect(self, skillId, skillLevel, clientSkillInfo, start = True, targetId = 0):
        owner = BigWorld.entity(self.owner)
        if not skillId or not skillLevel:
            return
        beCastedEffect = skillDataInfo.getBeCastedEffect(clientSkillInfo)
        if beCastedEffect:
            beCastType = beCastedEffect[0]
            beCastEffs = beCastedEffect[1]
            if beCastEffs:
                if start and beCastType == gameglobal.BE_CAST_EFFECT_START or not start and beCastType == gameglobal.BE_CAST_EFFECT_RESULT:
                    if not owner.model:
                        return
                    for effId in beCastEffs:
                        owner.model.hostId = owner.id
                        sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
                         owner.getSkillEffectPriority(),
                         owner.model,
                         effId,
                         sfx.EFFECT_LIMIT,
                         gameglobal.EFFECT_LAST_TIME))

                elif not start and beCastType == gameglobal.BE_CAST_EFFECT_RESULT_ONLY_TARGET:
                    if self.owner == targetId:
                        for effId in beCastEffs:
                            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
                             owner.getSkillEffectPriority(),
                             owner.model,
                             effId,
                             sfx.EFFECT_LIMIT,
                             gameglobal.EFFECT_LAST_TIME))

    def startSpell(self, target, skillID, skillLevel, keepTime, targetPos, keep = 0, clientPlaySkillInfo = None):
        self.target = target
        self.skillID = skillID
        self.skillLevel = skillLevel
        self.keepTime = keepTime
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if not owner.fashion:
            raise Exception('owner no fashion: ' + str(type(owner)) + '. skillID: ' + str(skillID))
        owner.fashion.stopAction()
        skillInfo = SkillInfo(skillID, skillLevel)
        clientSkillInfo = owner.getClientSkillInfo(skillID, skillLevel)
        self.playCountdown(skillInfo, clientSkillInfo, const.COUNTDOWN_CAST_TYPE_SPELL)
        self.playFenShen(skillInfo, clientSkillInfo)
        if owner == BigWorld.player():
            self.showSpellScreenEffect(clientSkillInfo)
        self.switchWeapon(clientSkillInfo)
        playSeq = []
        weaponActions = []
        spellActionStart, effectsStart, tintEffect = self.getActionWithEffect(gameglobal.S_SPELLSTART, skillInfo, clientSkillInfo=clientSkillInfo)
        effScale = self._getSkillEffectScale(skillID, gameglobal.SE_SPELLSTART, clientSkillInfo)
        preSpellSkill = skillDataInfo.isPreSpellSkill(skillInfo)
        if spellActionStart and spellActionStart not in owner.fashion.action.actionList:
            spellActionStart = None
        if spellActionStart:
            if preSpellSkill:
                actType = action.STARTPRESPELL_ACTION
            else:
                actType = action.STARTSPELL_ACTION
            playSeq.append((spellActionStart,
             effectsStart,
             actType,
             0,
             1.0,
             tintEffect,
             effScale))
            weaponActions.append(spellActionStart)
        blend = True
        spellActionName, effects, tintEffect = self.getActionWithEffect(gameglobal.S_SPELL, skillInfo, clientSkillInfo=clientSkillInfo)
        s_spellPlayData = []
        if spellActionName and spellActionName not in owner.fashion.action.actionList:
            spellActionName = None
        if spellActionName:
            if preSpellSkill:
                actType = action.PRESPELLING_ACTION
            else:
                actType = action.SPELL_ACTION
            if skillDataInfo.isSpellActLoop(clientSkillInfo):
                s_spellPlayData = (spellActionName,
                 effects,
                 actType,
                 0,
                 1.0,
                 tintEffect,
                 effScale)
                weaponActions.append(spellActionName)
            else:
                spellTime = keepTime
                duration = owner.fashion.getActionTime(spellActionName)
                if spellTime:
                    playRate = duration / spellTime
                else:
                    playRate = 1.0
                gamelog.debug('playRate:', playRate)
                s_spellPlayData = (spellActionName,
                 effects,
                 actType,
                 0,
                 playRate,
                 tintEffect,
                 effScale)
                weaponActions.append(spellActionName)
        if s_spellPlayData:
            spellEffDelay = clientSkillInfo.getSkillData('spellEffDelay', None)
            if spellEffDelay:
                BigWorld.callback(spellEffDelay, Functor(self.__delayPlayEffect, owner, [s_spellPlayData], action.SPELL_ACTION, None, blend, 0, keep, owner.getSkillEffectPriority()))
            else:
                playSeq.append(s_spellPlayData)
        gamelog.debug('startSpell@playSeq', playSeq, keep)
        p = BigWorld.player()
        if not clientPlaySkillInfo:
            if owner == p:
                if owner.getSkillSpellingType() != action.S_SPELLING_CAN_MOVE:
                    owner.ap.stopMove()
        if not (hasattr(owner, 'inFlyTypeFlyRide') and owner.inFlyTypeFlyRide() or hasattr(owner, 'inFlyTypeFlyZaiju') and owner.inFlyTypeFlyZaiju()):
            owner.fashion.stopAllActions()
        if playSeq:
            owner.fashion.playActionWithFx(playSeq, action.SPELL_ACTION, None, blend, 0, keep, priority=owner.getSkillEffectPriority())
        self.playWeaponAction(skillInfo, clientSkillInfo)
        self.playFollowAvatarModelAction(weaponActions)
        if not clientPlaySkillInfo:
            if owner == p:
                if owner.getOperationMode() == gameglobal.MOUSE_MODE:
                    owner.faceTo(target)
                self._cycleCheckBlock()
                if not gameglobal.rds.isSinglePlayer:
                    t = BigWorld.time()
                    commonTotal = skillDataInfo.getCommonCoolDown(skillInfo, 0)
                    commonCooldown = (commonTotal + t, commonTotal, self.skillID)
                    logicInfo.commonCooldownWeaponSkill = commonCooldown
                    gameglobal.rds.ui.actionbar.updateSlots()
                if not preSpellSkill and not skillDataInfo.hideSpellBar(clientSkillInfo):
                    desc = skillDataInfo.getSkillName(skillInfo)
                    gameglobal.rds.ui.castbar.startCastBar(keepTime, desc)
            elif owner.IsMonster:
                faceTarget = clientSkillInfo.getSkillData('faceTargetInSpell', 0)
                if faceTarget and hasattr(target, 'matrix') and keepTime > 0:
                    owner.filter.faceTarget = target.matrix
                    BigWorld.callback(keepTime + 0.2, self._cancelFaceTarget)
            castbarShowType = clientSkillInfo.getSkillData('tgtNeedSpellBar', 0)
            noInterrupt = skillInfo.getSkillData('beBreakType', gametypes.SKILL_BE_BREAK_TYPE_ALL) == gametypes.SKILL_BE_BREAK_TYPE_SHOWNONE
            if castbarShowType and not preSpellSkill:
                name = skillDataInfo.getSkillName(skillInfo)
                if not owner.IsSummonedSprite:
                    gameglobal.rds.ui.target.startTargetCastbar(name, keepTime, False, owner, noInterrupt)
                if owner.topLogo and owner.IsSummonedSprite:
                    owner.topLogo.startCastbar(name, keepTime)
        self.__playSpellWarnEffect(clientSkillInfo, target, targetPos)
        self.__playSpellConnectEffect(clientSkillInfo, target)
        self.playSkillVoiceInSpell(clientSkillInfo)

    def __playSpellConnectEffect(self, clientSkillInfo, target):
        if target and target.id != self.owner:
            owner = BigWorld.entity(self.owner)
            startNode = None
            endNode = None
            start, end, effect = skillDataInfo.getSpellConnector(clientSkillInfo)
            gamelog.debug('__playSpellConnectEffect', start, end, effect)
            if effect:
                startNode = owner.model.node(start)
                endNode = target.model.node(end)
                if not startNode:
                    startNode = owner.getHitNodeRandom()
                if not endNode:
                    endNode = target.getHitNodeRandom()
                if owner != target:
                    self.spellConnector = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (owner.getSkillEffectLv(),
                     startNode,
                     effect,
                     endNode,
                     50,
                     owner.getSkillEffectPriority()))

    def __stopSpellConnector(self):
        if self.spellConnector:
            self.spellConnector.release()
        self.spellConnector = None

    def __playFlyDestStopEffect(self, clientSkillInfo):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        effects = skillDataInfo.getSkillEffects(clientSkillInfo, gameglobal.S_FLYDEST_STOP)
        if effects and self.guideStopPos:
            for effect in effects:
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (owner.getSkillEffectLv(),
                 owner.getSkillEffectPriority(),
                 None,
                 effect,
                 sfx.EFFECT_LIMIT_MISC,
                 self.guideStopPos,
                 0,
                 0,
                 0,
                 gameglobal.EFFECT_LAST_TIME))

        self.guideStopPos = None

    def __playGuideStopEffect(self, clientSkillInfo):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        effects = skillDataInfo.getSkillEffects(clientSkillInfo, gameglobal.S_GUIDE_STOP)
        if effects:
            for effect in effects:
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
                 owner.getSkillEffectPriority(),
                 owner.model,
                 effect,
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))

    def __playSpellWarnEffect(self, clientSkillInfo, target, targetPos):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        spellWarnEffectData = skillDataInfo.getSpellWarnEffect(clientSkillInfo)
        gamelog.debug('lihang@__playSpellWarnEffect', spellWarnEffectData, targetPos, owner.id)
        if spellWarnEffectData:
            if skillDataInfo.getSpellWarnEffectDisplayType(clientSkillInfo):
                if BigWorld.player().isFriend(owner):
                    if target and target.id != self.owner:
                        for effect in spellWarnEffectData:
                            ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
                             owner.getSkillEffectPriority(),
                             target.model,
                             effect,
                             sfx.EFFECT_UNLIMIT,
                             gameglobal.EFFECT_LAST_TIME))
                            if ef:
                                self.spellWarnEffects.extend(ef)

                    else:
                        for effect in spellWarnEffectData:
                            ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (owner.getSkillEffectLv(),
                             owner.getSkillEffectPriority(),
                             owner.model,
                             effect,
                             sfx.EFFECT_UNLIMIT,
                             targetPos,
                             0,
                             0,
                             0,
                             gameglobal.EFFECT_LAST_TIME))
                            if ef:
                                self.spellWarnEffects.extend(ef)

            elif target and target.id != self.owner:
                for effect in spellWarnEffectData:
                    ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (target.getSkillEffectLv(),
                     target.getSkillEffectPriority(),
                     target.model,
                     effect,
                     sfx.EFFECT_UNLIMIT,
                     gameglobal.EFFECT_LAST_TIME))
                    if ef:
                        self.spellWarnEffects.extend(ef)

            else:
                for effect in spellWarnEffectData:
                    ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (owner.getSkillEffectLv(),
                     owner.getSkillEffectPriority(),
                     owner.model,
                     effect,
                     sfx.EFFECT_UNLIMIT,
                     targetPos,
                     0,
                     0,
                     0,
                     gameglobal.EFFECT_LAST_TIME))
                    if ef:
                        self.spellWarnEffects.extend(ef)

    def __stopSpellWarnEffect(self):
        gamelog.debug('lihang@__stopSpellWarnEffect')
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        for fx in self.spellWarnEffects:
            if fx:
                fx.stop()

        self.spellWarnEffects = []

    def _cancelFaceTarget(self):
        owner = BigWorld.entity(self.owner)
        if owner == None or not owner.inWorld:
            return
        owner.filter.faceTarget = None

    def _cycleCheckBlock(self):
        player = BigWorld.player()
        target = self.target
        if player and target and target.inWorld and player.fashion.doingActionType() in [action.SPELL_ACTION, action.GUIDE_ACTION]:
            if not target.IsFragileObject and not clientcom.checkAttackThrough(player.spaceID, player.position, target.position, target.getTopLogoHeight(), target.getBodySize()):
                player.ap.cancelskill()
                if not gameglobal.rds.ui.cameraTable.isShow:
                    player.showGameMsg(GMDD.data.BLOCKED_BY_WALL, ())
            else:
                BigWorld.callback(1, self._cycleCheckBlock)

    def startCharge(self, target, skillID, skillLevel, clientPlaySkillInfo = None):
        self.target = target
        self.skillID = skillID
        self.skillLevel = skillLevel
        owner = BigWorld.entity(self.owner)
        owner.fashion.stopAction()
        skillInfo = owner.getSkillInfo(skillID, skillLevel)
        clientSkillInfo = owner.getClientSkillInfo(skillID, skillLevel)
        self.switchWeapon(clientSkillInfo)
        p = BigWorld.player()
        if owner == p:
            owner.ap.stopMove()
            if owner.getOperationMode() == gameglobal.MOUSE_MODE:
                owner.faceTo(target)
        playSeq = []
        weaponActions = []
        spellActionStart, effectsStart, tintEffect = self.getActionWithEffect(gameglobal.S_SPELLSTART, skillInfo, clientSkillInfo=clientSkillInfo)
        effScale = self._getSkillEffectScale(skillID, gameglobal.SE_SPELLSTART, clientSkillInfo)
        if spellActionStart and spellActionStart not in owner.fashion.action.actionList:
            spellActionStart = None
        if spellActionStart:
            playSeq.append((spellActionStart,
             effectsStart,
             action.CHARGE_START_ACTION,
             0,
             1.0,
             tintEffect,
             effScale))
            weaponActions.append(spellActionStart)
        spellActionName, effects, tintEffect = self.getActionWithEffect(gameglobal.S_SPELL, skillInfo, clientSkillInfo=clientSkillInfo)
        chargeStages = skillDataInfo.getChargeStgs(skillInfo)
        if spellActionName and spellActionName not in owner.fashion.action.actionList:
            spellActionName = None
        if spellActionName:
            if skillDataInfo.isSpellActLoop(clientSkillInfo):
                playSeq.append((spellActionName,
                 effects,
                 action.CHARGE_ACTION,
                 0,
                 1.0,
                 tintEffect,
                 effScale))
                weaponActions.append(spellActionName)
            else:
                spellTime = 0.0
                spellTime += chargeStages[len(chargeStages) - 1]
                duration = owner.fashion.getActionTime(spellActionName)
                if spellTime:
                    playRate = duration / spellTime
                else:
                    playRate = 1.0
                gamelog.debug('playRate:', playRate, duration, spellTime)
                playSeq.append((spellActionName,
                 effects,
                 action.CHARGE_ACTION,
                 0,
                 playRate,
                 tintEffect,
                 effScale))
                weaponActions.append(spellActionName)
        blend = False
        owner.fashion.playActionWithFx(playSeq, action.CHARGE_ACTION, None, blend, keep=10, priority=owner.getSkillEffectPriority())
        self.playWeaponAction(skillInfo, clientSkillInfo)
        self.playFollowAvatarModelAction(weaponActions)
        self.chargeNowStage = -1
        self.chargeStages = skillDataInfo.getChargeStgs(skillInfo)
        for stage, sTime in enumerate(self.chargeStages):
            cb = BigWorld.callback(sTime - 0.1, Functor(self.chargeStageCallback, stage))
            self.chargeStageCallbacks.append(cb)

        p = BigWorld.player()
        if not clientPlaySkillInfo:
            if owner == p:
                self._cycleCheckBlock()
                desc = skillDataInfo.getSkillName(skillInfo)
                desc = skillDataInfo.getSkillName(skillInfo)
                gameglobal.rds.ui.castbar.startChargeBar(chargeStages, desc)
                if not gameglobal.rds.isSinglePlayer:
                    btime = BigWorld.time()
                    commonTotal = skillDataInfo.getCommonCoolDown(skillInfo, 0)
                    commonTotal = max(0.0, commonTotal)
                    commonCooldown = (commonTotal + btime, commonTotal, skillID)
                    if skillID in owner.skills:
                        logicInfo.commonCooldownWeaponSkill = commonCooldown
                        gameglobal.rds.ui.actionbar.updateSlots()

    def chargeStageCallback(self, nowStage):
        if not self.skillID and not self.skillLevel:
            return
        self.chargeNowStage = nowStage
        self._releaseChargeEff()
        self.playChargeStageEff(nowStage, gameglobal.SKILL_CHARGE_EFF_EXPLODE)
        self.playChargeStageEff(nowStage, gameglobal.SKILL_CHARGE_EFF_ING)
        gameglobal.rds.ui.castbar.showChargeSeperatorShine(nowStage)

    def playChargeStageEff(self, nowStage, effType):
        owner = BigWorld.entity(self.owner)
        effs = self._getChargeEffByStage(nowStage, effType)
        if effs:
            for ef in effs:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
                 owner.getSkillEffectPriority(),
                 owner.model,
                 ef,
                 sfx.EFFECT_LIMIT))
                if fx:
                    self.chargingEffects += fx

    def cancelChargeStageCallback(self):
        for cb in self.chargeStageCallbacks:
            BigWorld.cancelCallback(cb)

        self.chargeStageCallbacks = []

    def cancelMonsterMoveCallback(self):
        if self.monsterMoveCallback:
            BigWorld.cancelCallback(self.monsterMoveCallback)
        self.monsterMoveCallback = None
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld or not owner.IsMonster:
            return
        if getattr(owner, 'life', None) == gametypes.LIFE_DEAD:
            return
        owner.refreshOpacityState()

    def _getChargeEffByStage(self, stage, effType):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return None
        clientSkillInfo = owner.getClientSkillInfo(self.skillID, self.skillLevel)
        effs = clientSkillInfo.getSkillData('chargeStgEffs', ())
        if effs and len(effs) > stage:
            if effType == gameglobal.SKILL_CHARGE_EFF_EXPLODE:
                return effs[stage][0]
            if effType == gameglobal.SKILL_CHARGE_EFF_ING:
                return effs[stage][1]
            if effType == gameglobal.SKILL_CHARGE_EFF_CAST:
                return effs[stage][2]

    def _releaseChargeEff(self):
        if self.chargingEffects:
            for e in self.chargingEffects:
                e.stop()

            self.chargingEffects = []

    def releaseEffectConnector(self):
        if self.effectConnector:
            for e in self.effectConnector.values():
                if e:
                    e.release()

            self.effectConnector = {}

    def stopSpell(self):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if getattr(owner, 'castSkillBusy', None):
            owner.castSkillBusy = False
        self.target = None
        if not self.skillID:
            self.releaseEffectConnector()
            if BigWorld.player() == owner:
                gameglobal.rds.ui.castbar.notifyCastInterrupt()
            return False
        skillInfo = owner.getSkillInfo(self.skillID, self.skillLevel)
        clientSkillInfo = owner.getClientSkillInfo(self.skillID, self.skillLevel)
        if getattr(owner, 'spellInfo', None):
            self.stopCountdown(skillInfo, clientSkillInfo)
        if self.guideLoopCallback:
            BigWorld.cancelCallback(self.guideLoopCallback)
            self.guideLoopCallback = None
        if owner.fashion.doingActionType() in (action.DEAD_ACTION,
         action.STARTSPELL_ACTION,
         action.SPELL_ACTION,
         action.CHARGE_ACTION,
         action.GUIDE_ACTION,
         action.ROLL_ACTION,
         action.ROLLSTOP_ACTION,
         action.DASH_START_ACTION) or getattr(owner, 'isJumping', False):
            self.__stopGuideEffect(False)
        if BigWorld.player() == owner:
            gameglobal.rds.ui.castbar.notifyCastInterrupt()
            BigWorld.player().isChargeKeyDown = False
            owner.isGuiding = const.GUIDE_TYPE_NONE
            owner.updateActionKeyState()
            self.stopSpellScreenEffect()
        if BigWorld.player().targetLocked == owner:
            gameglobal.rds.ui.target.notifyTargetCastInterrupt()
        if owner.IsSummonedSprite and owner.topLogo:
            owner.topLogo.notifyCastbarInterrupt()
        self.releaseEffectConnector()
        self.__stopSpellWarnEffect()
        self.__stopSpellConnector()
        self._releaseChargeEff()
        self.cancelChargeStageCallback()
        self.refreshWeapon()
        self.cutCurveEff(skillInfo, clientSkillInfo)
        self.targetPos = None

    def endSpell(self):
        self.stopSpellHelper()

    def stopSpellHelper(self):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return False
        self.target = None
        if not self.skillID:
            return False
        skillInfo = owner.getSkillInfo(self.skillID, self.skillLevel)
        clientSkillInfo = owner.getClientSkillInfo(self.skillID, self.skillLevel)
        castEffectTime = skillDataInfo.getCastEffectTime(clientSkillInfo)
        owner.fashion._releaseTintFx()
        if getattr(owner, 'castSkillBusy', None):
            owner.castSkillBusy = False
        self.refreshWeapon()
        if castEffectTime:
            return
        guideActNotLoop = clientSkillInfo.getSkillData('guideActNotLoop', 0)
        castType = skillDataInfo.getCastType(skillInfo)
        if castType == gameglobal.CAST_TYPE_GUIDE and not guideActNotLoop:
            owner.fashion.stopAction()
            skillInfo = SkillInfo(self.skillID, self.skillLevel)
            playSeq = []
            guideStopActionName, guideStopEffects, tintEffect = self.getActionWithEffect(gameglobal.S_CASTSTOP, skillInfo, clientSkillInfo=clientSkillInfo)
            effScale = self._getSkillEffectScale(self.skillID, gameglobal.SE_CASTSTOP, clientSkillInfo)
            playSeq.append((guideStopActionName,
             guideStopEffects,
             action.GUIDESTOP_ACTION,
             0,
             1.0,
             tintEffect,
             effScale))
            if not owner.inMoving():
                owner.fashion.playActionWithFx(playSeq, action.GUIDESTOP_ACTION, Functor(owner.fashion._releaseTintFx), True, priority=owner.getSkillEffectPriority())
        p = BigWorld.player()
        if p == owner:
            skillInfo = SkillInfo(self.skillID, self.skillLevel)
            preSpellSkill = skillDataInfo.isPreSpellSkill(skillInfo)
            if not preSpellSkill:
                gameglobal.rds.ui.castbar.easeOutCastbar()
            p.spellingType = action.S_DEFAULT
            p.isGuiding = const.GUIDE_TYPE_NONE
            p.isChargeKeyDown = False
            if p.getOperationMode() == gameglobal.MOUSE_MODE:
                p.ap.isAutoTurnYaw = False
            p.updateActionKeyState()
        if p.targetLocked == owner:
            gameglobal.rds.ui.target.notifyTargetCastInterrupt()
        if owner.IsSummonedSprite and owner.topLogo:
            owner.topLogo.notifyCastbarInterrupt()
        if self.effectConnector:
            for e in self.effectConnector.values():
                if e:
                    e.release()

            self.effectConnector = {}
        self.__stopSpellWarnEffect()
        self.__stopSpellConnector()
        if not owner.IsMonster:
            if self.guideLoopCallback:
                BigWorld.cancelCallback(self.guideLoopCallback)
                self.guideLoopCallback = None
            self.__stopGuideEffect(True)
        self._releaseChargeEff()
        self.cancelChargeStageCallback()
        return True

    def switchWeapon(self, clientSkillInfo):
        owner = BigWorld.entity(self.owner)
        if owner.inWorld and (owner.IsAvatar or owner.isAvatarMonster()) and getattr(owner, 'bianshen', (0, 0))[0] != gametypes.BIANSHEN_ZAIJU:
            attachType = skillDataInfo.getSkillWeapon(clientSkillInfo)
            owner.switchWeaponState(attachType, False)
            if owner == BigWorld.player():
                owner.invokeWeaponTimer()
            self.endWeaponState = skillDataInfo.getSkillEndWeapon(clientSkillInfo)
            if self.endWeaponState == attachType:
                self.endWeaponState = 0

    def refreshWeapon(self):
        owner = BigWorld.entity(self.owner)
        if owner and owner.inWorld and (owner.IsAvatar or owner.isAvatarMonster()):
            if self.endWeaponState:
                owner.switchWeaponState(self.endWeaponState, False)
                if owner == BigWorld.player():
                    owner.invokeWeaponTimer()
                self.endWeaponState = 0

    def castSkill(self, targetID, skillID, skillLevel, damageResult = None, instant = False, playAction = True, moveId = None, moveTime = 0.0, moveClientRefInfo = None, guideCastTime = 0, clientPlaySkillInfo = None):
        gamelog.debug('@PGF:castSkill:', targetID, skillID, damageResult, moveId, moveTime, moveClientRefInfo, guideCastTime)
        owner = BigWorld.entity(self.owner)
        if owner == None or owner.fashion == None:
            return
        if owner.fashion.doingActionType() in [action.HIT_DIEFLY_ACTION]:
            return
        if owner == BigWorld.player():
            self.stopSpellScreenEffect()
        skillInfo = owner.getSkillInfo(skillID, skillLevel)
        clientSkillInfo = owner.getClientSkillInfo(skillID, skillLevel)
        if not clientPlaySkillInfo:
            self.playCountdown(skillInfo, clientSkillInfo, const.COUNTDOWN_CAST_TYPE_GUIDE)
        self.castLoop = skillDataInfo.getCastLoop(clientSkillInfo)
        self.__stopSpellConnector()
        self._releaseChargeEff()
        self.cancelChargeStageCallback()
        if getattr(owner, 'castSkillBusy', None):
            owner.castSkillBusy = False
        switchWeaponInCue = clientSkillInfo.getSkillData('switchWeaponInCue', False)
        if not switchWeaponInCue:
            self.switchWeapon(clientSkillInfo)
        target = BigWorld.entity(targetID)
        if not target:
            target = owner
        self.target = target
        if self.skillID != skillID:
            self.skillID = skillID
        if self.skillLevel != skillLevel:
            self.skillLevel = skillLevel
        keepAct = clientSkillInfo.getSkillData('keepAct', 0)
        keep = 0.5 if keepAct == 1 else 0
        groundStick = clientSkillInfo.getSkillData('groundStick', 0)
        if groundStick == 1 and self.targetPos != None and owner.fashion.isPlayer:
            dropPoint = BigWorld.findDropPoint(BigWorld.player().spaceID, Math.Vector3(self.targetPos[0], self.targetPos[1] + 3.0, self.targetPos[2]))
            if dropPoint:
                self.targetPos = dropPoint[0]
        self.pushDamage(skillID, damageResult)
        p = BigWorld.player()
        if owner == p:
            owner.spellingType = action.S_DEFAULT
            commonTotal = skillDataInfo.getCommonCoolDown(skillInfo, 0)
            BigWorld.callback(commonTotal, self.useHoldingSkill)
        castType = skillDataInfo.getCastType(skillInfo)
        if not clientPlaySkillInfo:
            if castType == gameglobal.CAST_TYPE_GUIDE and owner == p:
                p.isGuiding = const.GUIDE_TYPE_NO_MOVE
                moveMode = skillDataInfo.getCastMoveType(skillInfo)
                if moveMode == gametypes.CAST_MOVE_TYPE_CAN_MOVE:
                    p.isGuiding = const.GUIDE_TYPE_MOVE
                if p.getOperationMode() == gameglobal.MOUSE_MODE:
                    p.ap.updateYawByMouse()
                castTime = skillInfo.getSkillData('castTime', 0)
                skillName = skillInfo.getSkillData('name', '')
                castDelay = skillInfo.getSkillData('castDelay', 0)
                if not skillDataInfo.isHideCastBar(skillInfo):
                    gameglobal.rds.ui.castbar.startCountDown(castTime + castDelay, skillName)
        if castType == gameglobal.CAST_TYPE_GUIDE and owner.IsMonster:
            castbarShowType = clientSkillInfo.getSkillData('tgtNeedGuideBar', 0)
            castTime = skillInfo.getSkillData('castTime', 0)
            castDelay = skillInfo.getSkillData('castDelay', 0)
            castName = skillInfo.getSkillData('name', 0)
            noInterrupt = skillInfo.getSkillData('beBreakType', gametypes.SKILL_BE_BREAK_TYPE_ALL) == gametypes.SKILL_BE_BREAK_TYPE_SHOWNONE
            if not clientPlaySkillInfo:
                if castbarShowType:
                    gameglobal.rds.ui.target.startTargetCastbar(castName, castTime + castDelay, True, owner, noInterrupt)
                    if owner.topLogo and owner.IsSummonedSprite:
                        owner.topLogo.startCastbar(castName, castTime + castDelay, True)
        chargeSkill = skillDataInfo.isChargeSkill(skillInfo)
        if chargeSkill:
            self.playChargeStageEff(self.chargeNowStage, gameglobal.SKILL_CHARGE_EFF_CAST)
        self.playSkillVoiceInCast(clientSkillInfo)
        castActionName, castEffects, tintEffect = self.getActionWithEffect(gameglobal.S_CAST, skillInfo, clientSkillInfo=clientSkillInfo)
        effScale = self._getSkillEffectScale(skillID, gameglobal.SE_CAST, clientSkillInfo)
        castTime = skillInfo.getSkillData('castTime', 0)
        if castType == gameglobal.CAST_TYPE_GUIDE:
            castTime += skillInfo.getSkillData('castDelay', 0)
        castTime = guideCastTime if guideCastTime > castTime else castTime
        if castTime and castEffects:
            for ef in castEffects:
                sfx.updateEffectKeepTime(ef, castTime)

        castEffectTime = skillDataInfo.getCastEffectTime(clientSkillInfo)
        self.castActionCue = []
        castActionDuration = 0
        gamelog.debug('getCastActionName', castActionName)
        if not owner.IsMonster and owner.fashion.doingActionType() in [action.SPELL_ACTION, action.BORED_ACTION]:
            if not (hasattr(owner, 'inFlyTypeFlyRide') and owner.inFlyTypeFlyRide() or hasattr(owner, 'inFlyTypeFlyZaiju') and owner.inFlyTypeFlyZaiju()):
                owner.fashion.stopAllActions()
        if castActionName and castActionName not in owner.fashion.action.actionList:
            castActionName = None
        if castActionName:
            owner.fashion.stopAction()
            actObj = None
            try:
                actObj = owner.model.action(castActionName)
                self.parseActionCue(actObj)
                castActionDuration = owner.fashion.getActionTime(castActionName)
            except:
                gamelog.error('zf9:parseActionCue failed...........', castActionName)

            moveMode = skillDataInfo.getCastMoveType(skillInfo)
            gamelog.debug('moveMode:', moveMode, castType)
            blend = True
            if moveMode == action.S_BLEND:
                if owner == p:
                    owner.castSkillBusy = False
                    owner.updateActionKeyState()
            elif moveMode == action.S_SLIDE:
                if owner == p:
                    owner.castSkillBusy = True
                    owner.ap.stopMove()
            playSeq = []
            weaponActions = []
            castActType = self.getMoveType(gameglobal.S_CAST, skillInfo)
            if castType == gameglobal.CAST_TYPE_GUIDE:
                if castEffectTime:
                    playSeq.append((castActionName,
                     None,
                     action.GUIDE_ACTION,
                     castActType,
                     1.0,
                     tintEffect))
                    weaponActions.append(castActionName)
                else:
                    playSeq.append((castActionName,
                     castEffects,
                     action.GUIDE_ACTION,
                     castActType,
                     1.0,
                     tintEffect,
                     effScale))
                    weaponActions.append(castActionName)
            else:
                castType = action.CAST_ACTION
                if moveMode == action.S_BLEND:
                    castType = action.CAST_MOVING_ACTION
                playSeq.append((castActionName,
                 castEffects,
                 castType,
                 castActType,
                 1.0,
                 tintEffect,
                 effScale))
                weaponActions.append(castActionName)
            castStopActionName, castStopEffects, tintEffect = self.getActionWithEffect(gameglobal.S_CASTSTOP, skillInfo, clientSkillInfo=clientSkillInfo)
            effScale = self._getSkillEffectScale(skillID, gameglobal.SE_CASTSTOP, clientSkillInfo)
            if castStopActionName and castStopActionName not in owner.fashion.action.actionList:
                castStopActionName = None
            if castStopActionName:
                act = None
                actionType = action.CASTSTOP_ACTION
                try:
                    act = owner.model.action(castStopActionName)
                    gamelog.debug('castStopActionName:', actionType, act.blended, castStopActionName)
                except:
                    pass

                guideActNotLoop = clientSkillInfo.getSkillData('guideActNotLoop', 0)
                if guideActNotLoop or castType != gameglobal.CAST_TYPE_GUIDE:
                    playSeq.append((castStopActionName,
                     castStopEffects,
                     actionType,
                     0,
                     1.0,
                     tintEffect,
                     effScale))
                    weaponActions.append(castStopActionName)
                owner.castStopActionName = castStopActionName
            gamelog.debug('castSkill@playSeq', playSeq)
            owner.fashion.breakModelHitFreeze()
            info = self.getActionExtraInfo(owner, skillInfo)
            owner.fashion.playActionWithFx(playSeq, action.CAST_ACTION, Functor(self.endCast, skillInfo, clientSkillInfo), blend, None, keep, priority=owner.getSkillEffectPriority(), extraInfo=info)
            self.playFollowAvatarModelAction(weaponActions)
            waterHeight = self.isInWaterUseSkill(owner)
            if waterHeight:
                castWaterEffect = clientSkillInfo.getSkillData('castWaterEffect', None)
                if castWaterEffect:
                    position = Math.Vector3(owner.position[0], owner.position[1] + abs(waterHeight), owner.position[2])
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
                     owner.getSkillEffectPriority(),
                     owner.model,
                     castWaterEffect,
                     sfx.EFFECT_LIMIT,
                     gameglobal.EFFECT_LAST_TIME,
                     position))
            if castEffectTime:
                self.castEffect = castEffects
                self.playGuideNoLoopEffect(skillInfo, castEffectTime)
            self.playWeaponAction(skillInfo, clientSkillInfo)
            if castType == gameglobal.CAST_TYPE_GUIDE and owner == p:
                self._cycleCheckBlock()
        else:
            for fx in castEffects:
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
                 owner.getSkillEffectPriority(),
                 owner.model,
                 fx,
                 sfx.EFFECT_LIMIT,
                 -1,
                 target.position))

            self.endCast(skillInfo, clientSkillInfo)
        if owner == p:
            self.showScreenEffect(clientSkillInfo)
        skillUI = clientSkillInfo.getSkillData('skillUIEffect', 0)
        skillAvatar = clientSkillInfo.getSkillData('skillAvatar', 0)
        if (skillUI or skillAvatar) and owner == p:
            if not clientPlaySkillInfo:
                gameglobal.rds.ui.showSkillEffect(skillAvatar, skillUI)
        blackEffect = clientSkillInfo.getSkillData('blackEffect', None)
        if blackEffect and gameglobal.ENABLE_SKILL_SCREEN_EFFECT:
            inTime = float(blackEffect[0])
            blackTime = float(blackEffect[1])
            outTime = float(blackEffect[2])
            percent = float(blackEffect[3])
            blackType = float(blackEffect[4])
            onlyPlayer = int(blackEffect[5])
            if onlyPlayer and owner == p or not onlyPlayer:
                if owner.getEffectLv() >= gameglobal.EFFECT_MID:
                    if blackType == 0:
                        tintalt.ta_add(owner.allModels, 'tiliang', [1.0], inTime + blackTime + outTime)
                    else:
                        models = []
                        for id, e in BigWorld.entities.items():
                            if not hasattr(e, 'allModels'):
                                continue
                            models += e.allModels

                        tintalt.ta_add(models, 'tiliang', [1.0], inTime + blackTime + outTime)
                    BigWorld.setBlackTime(inTime, blackTime, outTime, percent, percent, percent)
        if skillInfo.getSkillData('spellTime') == 0:
            owner.calcIndicator(targetID, skillID, skillLevel)
        castDelay = skillDataInfo.getCastDelay(owner, skillInfo)
        needPlayClientEffType = skillDataInfo.isNeedPlayClientEffect(clientSkillInfo)
        if needPlayClientEffType == gameglobal.FLYER_DELAY_CHAIN and castDelay > 0:
            return
        if clientEffect.playClientEffectFuncMap.has_key(needPlayClientEffType):
            clientEffect.playClientEffectFuncMap[needPlayClientEffType](self, targetID, skillInfo, clientSkillInfo, damageResult, instant, playAction)
            return
        flyType = 0
        if moveClientRefInfo:
            flyType = moveClientRefInfo[0]
            if flyType == MONSTER_SKILL:
                self.parseMonsterMove(moveId, skillInfo, clientSkillInfo, playAction, moveTime)
            else:
                self.flyPeriod(skillInfo, clientSkillInfo, castActionDuration, playAction, flyType, moveId, moveClientRefInfo)
            return
        if moveTime > 0:
            self.parseMonsterMove(moveId, skillInfo, clientSkillInfo, playAction, moveTime)
            return
        if damageResult:
            damageResult = self.processMonsterHitFly(skillInfo, clientSkillInfo, damageResult)
            for pair in damageResult:
                en = BigWorld.entity(pair.eid)
                if not en:
                    continue
                if pair.eid != BigWorld.player().id:
                    continue
                flyType = pair.moveParam[0]
                if hasattr(en, 'avatarInstance'):
                    if not moveId:
                        moveId = pair.moveId
                    md = SMD.data.get(moveId, None)
                    if md and md.get('moveUnit') == gametypes.MOVEMENT_SKILL_MOVE_TGT:
                        self.flyPeriod(skillInfo, clientSkillInfo, castActionDuration, playAction, flyType, moveId, pair.moveParam)
                        return
                    if en.id == self.owner:
                        self.flyPeriod(skillInfo, clientSkillInfo, castActionDuration, playAction, flyType, moveId, pair.moveParam)
                        return

        if clientPlaySkillInfo and clientPlaySkillInfo.has_key('moveParam'):
            moveParam = clientPlaySkillInfo.get('moveParam')
            if moveParam:
                flyType = moveParam[0]
                self.flyPeriod(skillInfo, clientSkillInfo, castActionDuration, playAction, flyType, moveId, moveParam)
        self.flyPeriod(skillInfo, clientSkillInfo, castActionDuration, playAction)

    def getActionExtraInfo(self, owner, skillInfo):
        extraInfo = {}
        if owner.IsSummonedSprite:
            if skillInfo.getSkillData('affectedBySpriteCombatSpeedIncrease', None):
                if owner.getCombatSpeedIncreseRatio() != 1.0:
                    extraInfo['affectedBySpriteCombatSpeedIncrease'] = owner.getCombatSpeedIncreseRatio()
        return extraInfo

    def parseMonsterMove(self, moveId, skillInfo, clientSkillInfo, playAction, moveTime, damageData = None):
        smData = SMD.data.get(moveId, {})
        moveUnit = smData.get('moveUnit', gametypes.MOVEMENT_SKILL_MOVE_SELF)
        if moveUnit == gametypes.MOVEMENT_SKILL_MOVE_SELF:
            BigWorld.callback(0.1, Functor(self.monsterMove, moveTime, skillInfo, clientSkillInfo))
        elif moveUnit == gametypes.MOVEMENT_SKILL_MOVE_TGT:
            if not damageData:
                damageData = combatProto.PBResultSet(self.target.id)
            hold = smData.get('hold', 0)
            flyEffect.hitFly(self, skillInfo, clientSkillInfo, playAction, moveTime, damageData, hold)

    def isInWaterUseSkill(self, owner):
        if getattr(owner, 'inSwim', False):
            return None
        p = BigWorld.player()
        waterHeight = BigWorld.findWaterFromPoint(p.spaceID, owner.position)
        if not waterHeight:
            return None
        return waterHeight[0]

    def playGuideNoLoopEffect(self, skillInfo, castEffectTime):
        skillCastTime = skillDataInfo.getCastTime(skillInfo)
        gamelog.debug('playGuideNoLoopEffect')
        castCnt = int(round(skillCastTime / castEffectTime + 0.5))
        callBcakTime = []
        playEffectTime = 0.0
        callBcakTime.append(playEffectTime)
        for i in xrange(0, castCnt - 1):
            playEffectTime += castEffectTime
            callBcakTime.append(playEffectTime)

        gamelog.debug('playGuideNoLoopEffect', callBcakTime, skillCastTime)
        for playEffectTime in callBcakTime:
            self.noLoopEffectCallBackTimer.append(BigWorld.callback(playEffectTime, self.__playGuideEffect))

        self.guideLoopCallback = BigWorld.callback(skillCastTime, self.__stopGuideEffect)

    def playSkillVoiceInSpell(self, clientSkillInfo):
        if not gameglobal.rds.configData.get('enableDotaBf', False):
            return
        p = BigWorld.player()
        if not formula.inDotaBattleField(p.mapID):
            return
        type, voiceId = clientSkillInfo.getSkillData('skillVoice', (0, 0))
        if type == const.SKILL_VOICE_IN_SPELL and voiceId:
            owner = BigWorld.entities.get(self.owner)
            if owner and owner.id == p.id:
                gameglobal.rds.sound.playSound(voiceId, position=owner.position)

    def playSkillVoiceInCast(self, clientSkillinfo):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableDotaBf', False):
            return
        if not formula.inDotaBattleField(p.mapID):
            return
        type, voiceId = clientSkillinfo.getSkillData('skillVoice', (0, 0))
        if type == const.SKILL_VOICE_IN_CAST and voiceId:
            owner = BigWorld.entities.get(self.owner)
            if owner and owner.id == BigWorld.player().id:
                gameglobal.rds.sound.playSound(voiceId, position=owner.position)

    def __playGuideEffect(self):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        for fx in self.castEffect:
            ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (owner.getSkillEffectLv(),
             owner.getSkillEffectPriority(),
             owner.model,
             fx,
             sfx.EFFECT_LIMIT,
             -1))
            if ef:
                self.guidCastEffects += ef

    def __delayPlayEffect(self, owner, actions, actType, callback, blend, targetPos, keep, priority):
        if not owner or not owner.inWorld:
            return
        owner.fashion.playActionWithFx(actions, actType, callback, blend, targetPos, keep, priority=priority)

    def __stopGuideEffect(self, success = True):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        if not self.skillID or not self.skillLevel:
            return
        self.castEffect = []
        skillInfo = SkillInfo(self.skillID, self.skillLevel)
        clientSkillInfo = owner.getClientSkillInfo(self.skillID, self.skillLevel)
        self.__playFlyDestStopEffect(clientSkillInfo)
        BigWorld.callback(0.1, self.stopGuideEffect)
        if self.noLoopEffectCallBackTimer:
            for timer in self.noLoopEffectCallBackTimer:
                BigWorld.cancelCallback(timer)

            self.noLoopEffectCallBackTimer = []
        p = BigWorld.player()
        if p == owner:
            preSpellSkill = skillDataInfo.isPreSpellSkill(skillInfo)
            if not preSpellSkill:
                gameglobal.rds.ui.castbar.easeOutCastbar()
        self.__playGuideStopEffect(clientSkillInfo)
        if success:
            if owner.fashion.doingActionType() == action.GUIDE_ACTION or getattr(owner, 'isJumping', False):
                owner.fashion.stopAction()
                playSeq = []
                if owner.inMoving():
                    return
                guideStopActionName, guideStopEffects, tintEffect = self.getActionWithEffect(gameglobal.S_CASTSTOP, skillInfo, clientSkillInfo=clientSkillInfo)
                if guideStopActionName and guideStopActionName not in owner.fashion.action.actionList:
                    guideStopActionName = None
                if guideStopActionName:
                    playSeq.append((guideStopActionName,
                     guideStopEffects,
                     action.GUIDESTOP_ACTION,
                     0,
                     1.0,
                     tintEffect))
                owner.fashion.playActionWithFx(playSeq, action.GUIDESTOP_ACTION, self.useHoldingSkill, True, priority=owner.getSkillEffectPriority())
        else:
            owner.fashion.stopAction()
        if owner.fashion.isPlayer:
            owner.spellingType = action.S_DEFAULT
            owner.isGuiding = const.GUIDE_TYPE_NONE
            owner.updateActionKeyState()
            if owner.getOperationMode() == gameglobal.MOUSE_MODE:
                owner.ap.isAutoTurnYaw = False
            owner.updateActionKeyState()

    def stopGuideEffect(self):
        for fx in self.guidCastEffects:
            if fx:
                fx.stop()

        for fx in self.targetPosFx:
            if fx:
                fx.stop()

        self.guidCastEffects = []
        self.targetPosFx = []
        for cb in self.shakeCameraCB:
            if cb:
                BigWorld.cancelCallback(cb)

        self.shakeCameraCB = []

    def useHoldingSkill(self):
        owner = BigWorld.entity(self.owner)
        if owner:
            if BigWorld.player() == owner:
                owner.updateUseSkillKeyState()

    def hasRestorableDelayCd(self, owner, skillInfo, castDelayOnly = False, hasFlyDelay = False):
        if not skillInfo or not skillInfo.skillData:
            return False
        elif not skillInfo.getSkillData('restoreDelayCd', 0):
            return False
        moveDelay = skillInfo.getSkillData('movedelay', 0)
        moveSpeed = skillInfo.getSkillData('moveSpeed', 0)
        if moveDelay or moveSpeed:
            return False
        castDelay = skillDataInfo.getCastDelay(owner, skillInfo)
        flyNoDelay = skillInfo.getSkillData('flyNoDelay', 0)
        flySpeed = skillInfo.getSkillData('flySpeed', 0)
        if castDelayOnly:
            return castDelay > 0 and not flySpeed
        elif hasFlyDelay:
            return not flyNoDelay and flySpeed > 0
        else:
            return castDelay > 0 or not flyNoDelay and flySpeed > 0

    def stopCast(self, skillId, skillLv, targetId):
        p = BigWorld.player()
        owner = BigWorld.entity(self.owner)
        skillInfo = SkillInfo(skillId, skillLv)
        clientSkillInfo = owner.getClientSkillInfo(skillId, skillLv)
        self.stopCountdown(skillInfo, clientSkillInfo)
        skillClientInfo = skillDataInfo.ClientSkillInfo(skillId, skillLv, 2)
        if owner.fashion.doingActionType() != action.CAST_ACTION:
            if p == owner and self.hasRestorableDelayCd(owner, skillClientInfo):
                gameglobal.rds.ui.actionbar.clearCooldownSkill(skillId)
            return
        preCast = skillClientInfo.getSkillData('preCast', 0)
        if preCast:
            if p == owner and self.hasRestorableDelayCd(owner, skillClientInfo):
                gameglobal.rds.ui.actionbar.clearCooldownSkill(skillId)
            return
        self.refreshWeapon()
        if p == owner:
            p.isGuiding = const.GUIDE_TYPE_NONE
            if self.hasRestorableDelayCd(owner, skillClientInfo):
                gameglobal.rds.ui.actionbar.clearCooldownSkill(skillId)
        if owner.fashion != None:
            owner.fashion.breakJump()
            owner.fashion.breakFall()
            owner.fashion.stopAction()
        if self.effectConnector:
            for e in self.effectConnector.values():
                e.release()

            self.effectConnector = {}
        if getattr(owner, 'castSkillBusy', None):
            owner.castSkillBusy = False

    def endCast(self, skillInfo, clientSkillInfo):
        owner = BigWorld.entity(self.owner)
        if owner == None:
            return
        owner.fashion._releaseFx()
        if getattr(owner, 'castSkillBusy', None):
            owner.castSkillBusy = False
        self.refreshWeapon()
        if owner == BigWorld.player():
            castStopActionName = self.getActionName(gameglobal.S_CASTSTOP, skillInfo, False, clientSkillInfo=clientSkillInfo)
            if castStopActionName and castStopActionName not in owner.fashion.action.actionList:
                castStopActionName = None
            startMoveAction = self.getActionName(gameglobal.S_MOVE, skillInfo, False, clientSkillInfo=clientSkillInfo)
            if startMoveAction and startMoveAction not in owner.fashion.action.actionList:
                startMoveAction = None
            if not startMoveAction:
                owner.updateUseSkillKeyState()
                owner.updateActionKeyState()

    def getMoveActionType(self, moveDir):
        if not moveDir:
            return gameglobal.S_MOVE
        if moveDir == gameglobal.MOVE_DIR_FORWARD:
            return gameglobal.S_MOVE
        if moveDir == gameglobal.MOVE_DIR_LEFT:
            return gameglobal.S_MOVE_LEFT
        if moveDir == gameglobal.MOVE_DIR_RIGHT:
            return gameglobal.S_MOVE_RIGHT
        if moveDir == gameglobal.MOVE_DIR_BACK:
            return gameglobal.S_MOVE_BACK
        return gameglobal.S_MOVE

    def getMoveStopActionType(self, moveDir):
        if not moveDir:
            return gameglobal.S_MOVESTOP
        if moveDir == gameglobal.MOVE_DIR_FORWARD:
            return gameglobal.S_MOVESTOP
        if moveDir == gameglobal.MOVE_DIR_LEFT:
            return gameglobal.S_MOVESTOP_LEFT
        if moveDir == gameglobal.MOVE_DIR_RIGHT:
            return gameglobal.S_MOVESTOP_RIGHT
        if moveDir == gameglobal.MOVE_DIR_BACK:
            return gameglobal.S_MOVESTOP_BACK
        return gameglobal.S_MOVESTOP

    def startMove(self, skillInfo, clientSkillInfo, moveDir = None):
        self.skillID = skillInfo.num
        self.skillLevel = skillInfo.lv
        owner = BigWorld.entity(self.owner)
        if owner == None or not owner.inWorld:
            return
        if hasattr(owner, 'fashion'):
            owner.fashion.stopAllActions()
            owner.fashion.breakJump()
            owner.fashion.breakFall()
        if hasattr(owner, 'ap'):
            owner.ap.stopMove()
        playSeq = []
        moveActionType = self.getMoveActionType(moveDir)
        moveStopActionType = self.getMoveStopActionType(moveDir)
        startMoveAction, startMoveEffects, tintEffect = self.getActionWithEffect(moveActionType, skillInfo, clientSkillInfo=clientSkillInfo)
        if startMoveAction and startMoveAction not in owner.fashion.action.actionList:
            startMoveAction = None
        if startMoveAction:
            moveType = self.getMoveType(gameglobal.S_MOVE, skillInfo)
            if BigWorld.player() == owner:
                distPlayAction, startMoveOptionAction = clientSkillInfo.getSkillData('moveOptionAct', [0, None])
                if startMoveOptionAction and owner.targetLocked and owner.position.distTo(owner.targetLocked.position) >= distPlayAction:
                    playSeq.append((startMoveOptionAction,
                     startMoveEffects,
                     action.MOVING_ACTION,
                     moveType,
                     1.0,
                     tintEffect))
            playSeq.append((startMoveAction,
             startMoveEffects,
             action.MOVING_ACTION,
             moveType,
             1.0,
             tintEffect))
            startMoveStopAction, startMoveStopEffects, tintEffect = self.getActionWithEffect(moveStopActionType, skillInfo, clientSkillInfo=clientSkillInfo)
            deltimeTime = owner.fashion.getActionTime(startMoveAction)
            if owner == BigWorld.player():
                BigWorld.callback(deltimeTime + 0.15, owner.fashion.forceUpdateMovingNotifier)
            if startMoveStopAction and startMoveStopAction not in owner.fashion.action.actionList:
                startMoveStopAction = None
            if startMoveStopAction:
                moveStopType = self.getMoveType(gameglobal.S_MOVESTOP, skillInfo)
                playSeq.append((startMoveStopAction,
                 startMoveStopEffects,
                 action.MOVINGSTOP_ACTION,
                 moveStopType,
                 1.0,
                 tintEffect))
            if getattr(owner, 'castSkillBusy', None):
                owner.castSkillBusy = True
            owner.fashion.playActionWithFx(playSeq, action.MOVING_ACTION, Functor(self.endMove, skillInfo, clientSkillInfo), True, priority=owner.getSkillEffectPriority())
            gamelog.debug('startMove:playSeq:', playSeq)
        self.playWeaponAction(skillInfo, clientSkillInfo)

    def endMove(self, skillInfo, clientSkillInfo):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        self.refreshWeapon()
        if owner == BigWorld.player():
            MoveCastAction = self.getActionName(gameglobal.S_AFTERMOVE, skillInfo, False, clientSkillInfo=clientSkillInfo)
            if not MoveCastAction:
                gamelog.debug('endMoveskill')
                owner.updateUseSkillKeyState()
                owner.updateActionKeyState()

    def moveCast(self, skillInfo, clientSkillInfo = None, result = None, playAction = True):
        self.skillID = skillInfo.num
        self.skillLevel = skillInfo.lv
        owner = BigWorld.entity(self.owner)
        if owner == None or not owner.inWorld:
            return
        moveCastAction, moveCastEffects, tintEffect = self.getActionWithEffect(gameglobal.S_AFTERMOVE, skillInfo, clientSkillInfo=clientSkillInfo)
        if not owner or not owner.inWorld:
            return
        if not moveCastAction:
            if result != None:
                self.pushDamage(skillInfo.num, result)
            if self.castActionCue:
                self.processDamageByAttackPoint(skillInfo, clientSkillInfo)
            else:
                self.processDamageAll(skillInfo, clientSkillInfo)
            return
        if hasattr(owner, 'fashion'):
            owner.fashion.stopAction()
            owner.fashion.breakJump()
            owner.fashion.breakFall()
        if hasattr(owner, 'ap'):
            owner.ap.stopMove()
        if owner.life == gametypes.LIFE_DEAD:
            self.processDamageAll(skillInfo, clientSkillInfo)
            return
        actions = []
        playSeq = []
        if moveCastAction and moveCastAction not in owner.fashion.action.actionList:
            moveCastAction = None
        if moveCastAction:
            act = None
            try:
                act = owner.model.action(moveCastAction)
            except:
                pass

            if act:
                self.parseActionCue(act)
            actions.append(moveCastAction)
            moveType = 0
            playSeq.append((moveCastAction,
             moveCastEffects,
             action.AFTERMOVE_ACTION,
             moveType,
             1.0,
             tintEffect))
            moveCastStopAction, moveCastStopEffects, tintEffect = self.getActionWithEffect(gameglobal.S_AFTERMOVESTOP, skillInfo, clientSkillInfo=clientSkillInfo)
            if moveCastStopAction:
                actions.append(moveCastStopAction)
                playSeq.append((moveCastStopAction,
                 moveCastStopEffects,
                 action.AFTERMOVESTOP_ACTION,
                 0,
                 1.0,
                 tintEffect))
            if getattr(owner, 'castSkillBusy', None):
                owner.castSkillBusy = True
            owner.fashion.playActionWithFx(playSeq, action.AFTERMOVE_ACTION, Functor(self.endMoveCast, skillInfo, clientSkillInfo), True, priority=owner.getSkillEffectPriority())
        gamelog.debug('moveCast:playSeq', playSeq)
        self.playWeaponAction(skillInfo, clientSkillInfo)
        if result != None:
            self.pushDamage(skillInfo.num, result)
        if self.castActionCue:
            self.processDamageByAttackPoint(skillInfo, clientSkillInfo)
        else:
            self.processDamageAll(skillInfo, clientSkillInfo)

    def endMoveCast(self, skillInfo, clientSkillInfo):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if getattr(owner, 'castSkillBusy', None):
            owner.castSkillBusy = False
        self.refreshWeapon()
        if owner == BigWorld.player():
            gamelog.debug('endMovecastskill')
            owner.updateUseSkillKeyState()
            owner.updateActionKeyState()

    def noFlyProcessDamage(self, skillInfo, clientSkillInfo):
        gamelog.debug('bgf@noFlyProcessDamage', self.useAttackPoint)
        if self.useAttackPoint:
            self.processDamageByAttackPoint(skillInfo, clientSkillInfo)
        else:
            self.processDamageAll(skillInfo, clientSkillInfo)

    def _getShowHitEffIndexes(self, clientSkillInfo, damageResult):
        if not damageResult or not clientSkillInfo:
            return []
        else:
            maxHitEffNum = clientSkillInfo.getSkillData('maxHitEffNum', 0)
            if maxHitEffNum <= 0:
                return []
            num = len(damageResult)
            if maxHitEffNum >= num:
                return []
            li = range(num)
            random.shuffle(li)
            return li[0:maxHitEffNum]

    def _isShowHitEff(self, indexes, index):
        if not indexes:
            return True
        return index in indexes

    def processDamageAll(self, skillInfo, clientSkillInfo, tgtID = None, strHitNodeName = None, needTgtSpt = False, needPop = True):
        if not skillInfo:
            skillID = self.skillID
        else:
            skillID = skillInfo.num
        parent = BigWorld.entity(self.owner)
        if parent == None:
            return
        if not self.damageResult.has_key(skillID) or not self.damageResult[skillID]:
            return
        gamelog.debug('bgf:damageResult', self.damageResult[skillID], tgtID)
        self._flyerCheck(skillInfo.num)
        replaceResult = []
        findIndex = 0
        if needTgtSpt == False:
            damageResult = self.damageResult[skillID][0]
        else:
            find = False
            for results in self.damageResult[skillID]:
                replaceResult = []
                for idx, resultSet in enumerate(results):
                    if resultSet.eid == tgtID:
                        find = True
                        damageResult = results
                    else:
                        replaceResult.append(resultSet)

                if find == True:
                    break
                findIndex = findIndex + 1

            if find == False:
                findIndex = 0
                damageResult = self.damageResult[skillID][0]
        showHitEffIndexes = self._getShowHitEffIndexes(clientSkillInfo, damageResult)
        gamelog.debug('--------showHitEffIndexes', showHitEffIndexes)
        beAttackNum = len(damageResult)
        for idx, resultSet in enumerate(damageResult):
            ent = BigWorld.entity(resultSet.eid)
            gamelog.debug('bgf:damageResult 1', resultSet.eid)
            if ent != None:
                if tgtID == None or tgtID and tgtID == resultSet.eid or getattr(BigWorld.entities.get(tgtID, None), 'masterMonsterID', 0) == resultSet.eid:
                    needHitEff = self._isShowHitEff(showHitEffIndexes, idx)
                    needShake = utils.isResultCrit(resultSet)
                    extInfo = {gameglobal.CRIT_CAM_SHAKE: needShake}
                    ent.disturbSkillDamage(beAttackNum, parent, resultSet, skillInfo, clientSkillInfo, True, extInfo, needHitEff, strHitNodeName)
                else:
                    gamelog.error("ERROR:can\'t find entity id ", resultSet.eid)
            else:
                gamelog.error("ERROR:can\'t find entity id ", resultSet.eid)

        if needTgtSpt == False:
            if self.popFlyTargets(skillID, tgtID):
                self.damageResult[skillID].pop(0)
        elif needPop == True and self.popFlyTargets(skillID, tgtID) or needPop == False:
            if len(replaceResult) == 0:
                self.damageResult[skillID].remove(damageResult)
            else:
                self.damageResult[skillID][findIndex] = replaceResult

    def processMoveDamage(self, skillInfo, clientSkillInfo, damageResult, playAction = True):
        gamelog.debug('bgf:processMoveDamage', skillInfo, damageResult)
        moveId = skillDataInfo.isMovingSkill(skillInfo)
        owner = BigWorld.entity(self.owner)
        if moveId and owner and not owner.IsMonster and playAction:
            self.moveCast(skillInfo, clientSkillInfo, damageResult, playAction)
            return True
        damageResult = self.processMonsterHitFly(skillInfo, clientSkillInfo, damageResult)
        gamelog.debug('bgf:processMoveDamage2', damageResult)
        retVal = False
        for pair in damageResult:
            retVal |= self._flyPeriodFunc(skillInfo, clientSkillInfo, [pair], playAction, pair.moveParam, pair.moveId)

        return retVal

    def mfProcessMoveDamage(self, skillInfo, clientSkillInfo, damageResult, playAction = True):
        gamelog.debug('bgf:processMoveDamage', skillInfo, damageResult)
        damageResult = self.processMonsterHitFly(skillInfo, clientSkillInfo, damageResult)
        gamelog.debug('bgf:processMoveDamage2', damageResult)
        retVal = False
        for pair in damageResult:
            self.target = BigWorld.entities.get(pair.eid, None)
            retVal |= self._flyPeriodFunc(skillInfo, clientSkillInfo, [pair], playAction, pair.moveParam, pair.moveId)

        return retVal

    def isSkillResultMove(self, damageResult):
        for pair in damageResult:
            flyType = pair.moveParam[0]
            if flyType > 0 and pair.moveId:
                return True

        return False

    def processFenShenDamage(self, fenshenInfo):
        if not fenshenInfo or len(fenshenInfo) <= 0:
            return
        for info in fenshenInfo:
            fenshenId = info[0]
            fenshenPosition = info[1]
            targetPosition = info[2]
            targetYaw = info[3]
            fenShenEffect.startFenShen(self.owner, fenshenId, fenshenPosition, targetPosition, targetYaw)

    def _flyPeriodFunc(self, skillInfo, clientSkillInfo, damageResult, playAction, moveParam, moveId):
        flyType = moveParam[0]
        gamelog.debug('flyPeriodFuncMap', flyType, moveId, playAction, moveParam, damageResult)
        if flyType > 0:
            self.pushDamage(skillInfo.num, damageResult)
            if flyEffect.flyPeriodFuncMap.has_key(flyType):
                flyEffect.flyPeriodFuncMap[flyType](self, skillInfo, clientSkillInfo, playAction, moveParam, moveId)
            return True
        return False

    def monsterMove(self, moveTime, skillInfo, clientSkillInfo):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if owner.fashion.doingActionType() in [action.HIT_DIEFLY_ACTION]:
            return
        beLocked = False
        if clientSkillInfo and clientSkillInfo.getSkillData('hideAtMove', 0):
            beLocked = BigWorld.player().targetLocked.id == owner.id if BigWorld.player().targetLocked else False
            owner.hide(True)
        playSeq = []
        delayPlaySeq = []
        startMoveAction, startMoveEffects, tintEffect = self.getActionWithEffect(gameglobal.S_MOVE, skillInfo, clientSkillInfo=clientSkillInfo)
        if startMoveAction:
            moveType = self.getMoveType(gameglobal.S_MOVE, skillInfo)
            playAction = (startMoveAction,
             startMoveEffects,
             action.MOVING_ACTION,
             moveType,
             1.0,
             tintEffect)
            delayTime = clientSkillInfo.getSkillData('movingEffDelay', 0)
            if delayTime > 0:
                delayPlaySeq.append(playAction)
            else:
                playSeq.append(playAction)
            priority = owner.getSkillEffectPriority()
            owner.fashion.playActionWithFx(playSeq, action.MOVING_ACTION, None, True, priority=priority)
            if delayPlaySeq:
                BigWorld.callback(delayTime, Functor(self.__delayPlayEffect, owner, delayPlaySeq, action.MOVING_ACTION, None, True, 0, 0, priority))
            self.monsterMoveCallback = BigWorld.callback(moveTime, Functor(self.monsterStopMove, skillInfo, clientSkillInfo, beLocked))
            return True
        return False

    def monsterStopMove(self, skillInfo, clientSkillInfo, beLocked):
        owner = BigWorld.entity(self.owner)
        if not owner or not owner.inWorld:
            return
        if clientSkillInfo.getSkillData('hideAtMove', 0):
            owner.refreshOpacityState()
            if beLocked:
                p = BigWorld.player()
                if not p.targetLocked:
                    p.lockTarget(owner)
        if owner.fashion.doingActionType() in [action.HIT_DIEFLY_ACTION]:
            return
        if self.monsterMoveCallback:
            BigWorld.cancelCallback(self.monsterMoveCallback)
            self.monsterMoveCallback = None
        if hasattr(owner, 'fashion'):
            if owner.fashion.doingActionType() in [action.HITBACK_ACTION] or owner.model.freezeTime > 0.0:
                return
            startMoveAction, startMoveEffects, tintEffect = self.getActionWithEffect(gameglobal.S_MOVE, skillInfo, clientSkillInfo=clientSkillInfo)
            owner.fashion.stopActionByName(owner.model, startMoveAction)
            owner.fashion._releaseFxByIDs(startMoveEffects, tintEffect[0] if tintEffect else None)
        if owner.life == gametypes.LIFE_DEAD:
            return
        playSeq = []
        keepAct = clientSkillInfo.getSkillData('keepAct', 0)
        keep = 0.5 if keepAct == 1 else 0
        startMoveStopAction, startMoveStopEffects, tintEffect = self.getActionWithEffect(gameglobal.S_MOVESTOP, skillInfo, clientSkillInfo=clientSkillInfo)
        if startMoveStopAction:
            moveStopType = self.getMoveType(gameglobal.S_MOVESTOP, skillInfo)
            playSeq.append((startMoveStopAction,
             startMoveStopEffects,
             action.MOVINGSTOP_ACTION,
             moveStopType,
             1.0,
             tintEffect))
        moveCastAction, moveCastEffects, tintEffect = self.getActionWithEffect(gameglobal.S_AFTERMOVE, skillInfo, clientSkillInfo=clientSkillInfo)
        try:
            if moveCastAction:
                act = owner.model.action(moveCastAction)
                if act:
                    self.parseActionCue(act)
                playSeq.append((moveCastAction,
                 moveCastEffects,
                 action.MOVING_ACTION,
                 0,
                 1.0,
                 tintEffect))
                moveCastStopAction, moveCastStopEffects, tintEffect = self.getActionWithEffect(gameglobal.S_AFTERMOVESTOP, skillInfo, clientSkillInfo=clientSkillInfo)
                if moveCastStopAction:
                    playSeq.append((moveCastStopAction,
                     moveCastStopEffects,
                     action.AFTERMOVESTOP_ACTION,
                     0,
                     1.0,
                     tintEffect))
            if hasattr(owner, 'fashion') and playSeq:
                owner.fashion.playActionWithFx(playSeq, action.MOVING_ACTION, None, True, 0, keep, priority=owner.getSkillEffectPriority())
        except:
            gamelog.error('error:monsterStopMove', moveCastAction, owner.id, owner.model.sources)

    def processDamageById(self, skillInfo, clientSkillInfo, damageData):
        parent = BigWorld.entity(self.owner)
        if parent == None:
            return
        ent = BigWorld.entity(damageData.eid)
        if ent != None:
            needSplitDamage = True
            if damageData and damageData.kill:
                needSplitDamage = False
            ent.skillDamage(parent, damageData, skillInfo, clientSkillInfo, needSplitDamage)

    def processMonsterHitFly(self, skillInfo, clientSkillInfo, damageResult):
        leftDamage = []
        while damageResult:
            pair = damageResult.pop(0)
            moveTime = pair.moveTime
            flyType = pair.moveParam[0]
            if moveTime:
                flyType = MONSTER_SKILL
            if flyType == MONSTER_SKILL:
                self.parseMonsterMove(pair.moveId, skillInfo, clientSkillInfo, True, moveTime, pair)
            else:
                leftDamage.append(pair)

        for pair in leftDamage:
            damageResult.append(pair)

        return damageResult

    def processGuideFlyerDamage(self, skillInfo, clientSkillInfo, damageResult, targetId):
        if targetId and not self.target:
            self.target = BigWorld.entities.get(targetId, None)
        needFlyDelay = skillInfo.getSkillData('needFlyDelay', 0)
        if damageResult != None:
            self.pushDamage(skillInfo.num, damageResult)
        self.flyPeriod(skillInfo, clientSkillInfo, 0, needCastDelay=False)
        if needFlyDelay:
            flyerFlag = self._flyerCheck(skillInfo.num)
            if flyerFlag == impSkillPlayerFly.FLYER_APPROACH:
                self.noFlyProcessDamage(skillInfo, clientSkillInfo)

    def showScreenEffect(self, clientSkillInfo):
        effect = skillDataInfo.getScreenEffect(clientSkillInfo)
        owner = BigWorld.entity(self.owner)
        if effect and owner.getEffectLv() >= gameglobal.EFFECT_MID:
            screenEffect.startEffect(gameglobal.EFFECT_TAG_CAST_SKILL, effect)

    def showSpellScreenEffect(self, clientSkillInfo):
        effect = skillDataInfo.getSpellScreenEffect(clientSkillInfo)
        if effect == None:
            return
        owner = BigWorld.entity(self.owner)
        if effect and owner.getEffectLv() >= gameglobal.EFFECT_MID:
            screenEffect.startEffect(gameglobal.EFFECT_TAG_SPELL, effect)

    def stopSpellScreenEffect(self):
        screenEffect.delEffect(gameglobal.EFFECT_TAG_SPELL)

    def freezeEffect(self, freezeTime):
        for fx in self.guidCastEffects:
            if fx:
                fx.pause(freezeTime)
                self.freezedEffs.append(fx)

        for fx in self.spellWarnEffects:
            if fx:
                fx.pause(freezeTime)
                self.freezedEffs.append(fx)

        if self.effectConnector:
            for e in self.effectConnector.values():
                if e:
                    e.pause(freezeTime)
                    self.freezedEffs.append(e)

        if self.spellConnector:
            self.spellConnector.pause(freezeTime)
            self.freezedEffs.append(self.spellConnector)

    def clearFreezeEffect(self):
        if self.freezedEffs:
            for eff in self.freezedEffs:
                if eff:
                    eff.pause(0)

        self.freezedEffs = []

    def _getSkillEffectScale(self, skillId, stage, originSkillInfo):
        owner = BigWorld.entity(self.owner)
        if not owner or not hasattr(owner, 'skillClientArgs') or stage not in SKILL_CLIENT_ARG_MAP or skillId not in owner.skillClientArgs:
            return originSkillInfo.getSkillData(stage, 1.0)
        scale = owner.skillClientArgs.get(skillId, {}).get(SKILL_CLIENT_ARG_MAP[stage], 0.0)
        scale += 1.0
        return max(scale, 0)
