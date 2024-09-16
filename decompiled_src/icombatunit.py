#Embedded file name: /WORKSPACE/data/entities/client/icombatunit.o
import random
import math
import time
import copy
import BigWorld
import Math
import keys
import iClient
import gametypes
import gameglobal
import utils
import skillDataInfo
import combatProto
import clientcom
import const
import gamelog
import formula
import commcalc
from gameclass import SkillInfo
from skillDataInfo import ClientSkillInfo
from callbackHelper import Functor
from helpers import attachedModel
from helpers import fashion
from helpers import modelServer
from helpers import action as ACT
from helpers import skillPlayer
from helpers import ufo
from helpers import action
from helpers import tintalt
from helpers import combatMsg
from helpers import protect
from helpers import modelRobber
from helpers import lifeLinkManager
from sMath import limit
from helpers import deadPlayBack
from iAbstractCombatUnit import IAbstractCombatUnit
from iDisplay import IDisplay
from sfx import sfx
from sfx import stateFX
from sfx import auraFx
from sfx import attackEffect
from guis import ui
from guis import cursor
from guis import uiConst
from guis import uiUtils
from google.protobuf.message import DecodeError
from data import conditional_prop_data as CPD
from data import monster_model_client_data as MMCD
from data import creation_client_data as CD
from data import monster_bianshi_data as MBD
from data import state_data as SD
from data import state_client_data as SCD
from data import digong_boss_room_data as DBRD
from data import school_data as SCHD
from data import skill_creation_data
from data import map_config_data as MCD
from data import hit_effect_data as HED
from data import hit_effect_strong_data as HESD
from data import skill_fx_data as SFD
from data import sys_config_data as SYSCD
from data import equip_data as EQD
from data import zaiju_data as ZJD
from data import skill_zaiju_apprearance_data as SZAD
from data import skill_fenshen_appearance_data as SFAD
from data import avatar_beHit_sound_data as ABSD
from data import empty_zaiju_data as EZD
from data import sys_config_data as SCFD
from data import world_war_config_data as WWCD
from data import pskill_client_data as PSCD
from data import summon_sprite_data as SSPD
DYING_DELAY_LIST = set()
HIT_EFFECT_DURATION = 0.2
HIT_HITSOUND_DURATION = 0.1
HIT_CONFIG_SOUND_DURATION = SYSCD.data.get('hitSoundInterval', 0)
HIT_HITSOUND_COUNT = 50
ATK_TYPE_PLAYER_BLUE_SUB = 12
ATK_TYPE_PLAYER_BLUE_ADD = 13
ATK_TYPE_NORMAL_HTI = 100
ATK_TYPE_HEAL = 109
ATK_TYPE_HEAL_CRIT = 110
ATK_TYPE_SPRITE_MULTI1 = 1101
ATK_TYPE_SPRITE_MULTI2 = 1102
ATK_TYPE_SPRITE_COMBO = 1103
ATK_TYPE_SPRITE_MAGIC_ADD = 1104
ATK_TYPE_SPRITE_MAGIC_SUB = 1105
STATES_FUN_SET = set()

class ICombatUnit(iClient.IClient, IDisplay, IAbstractCombatUnit):
    IsCombatUnit = True
    IsEmptyZaiju = False

    def __init__(self):
        super(ICombatUnit, self).__init__()
        self.fashion = None
        self.skillPlayer = skillPlayer.SkillPlayer(self.id)
        self.states = []
        if hasattr(self, 'statesToAll'):
            self.states.extend(self.statesToAll)
        if hasattr(self, 'statesToSub'):
            self.states.extend(self.statesToSub)
        self.firstFetchFinished = False
        self.invisibleBySkill = False
        self.clientStateEffect = stateFX.EffectMgr(self.id)
        self.clientAuraEffect = auraFx.EffectMgr(self.id)
        self.topLogo = utils.MyNone
        self.attackActionName = ''
        self.effectOld = {'gm_hide': self.isGMHide()}
        self.statesOld = {}
        self.attackDelayTimer = 0
        self.speed = [0, 0, 0]
        self.killer = None
        self.hitStateType = action.UNKNOWN_STATE
        self.indicator = [False, 0]
        self.indicatorTimer = 0
        self.bsState = None
        self.beHitActionName = None
        self.hitEffTimestamp = {}
        self.stateModelScale = {}
        self.baseScale = 1
        self.spellScale = 1
        self.zaijuScale = 1
        self.revealCallback = None
        self.revealFadeCallback = None
        self.hidingPowerCallback = None
        self.hideLvSpan = gameglobal.DEFAULT_HIDE_LV_SPAN
        self.hitSoundTimestamp = {}
        self.hitConfigSoundTimestamp = 0
        self.oldModel = None
        self.bodyShakeFlyer = None
        self.lastSyncStateClientTime = BigWorld.time()
        self.statesClientPub = {}
        self.curTmpStates = {}
        self.daoDiStartAction = None
        self.daoDiLoopAction = None
        self.daoDiStateId = 0
        self.buffModelScale = None
        self.buffAttachModel = False
        if hasattr(self, 'states') and self.states:
            self.syncStatesClientPub(True)
        self.alertEffIds = [0, 0, []]
        self.inHidingReveal = False
        self.freezedEffs = []
        self.buffCaps = None
        self.deadLabelHadShown = False

    def needAddStateIcon(self):
        return True

    def isObstacleModel(self):
        return self.model and self.model.__class__.__name__ == 'PyModelObstacle'

    def syncSubProps(self):
        self.states = []
        self.states.extend(self.statesToAll)
        self.states.extend(self.statesToSub)

    def set_states(self, old):
        if not gameglobal.rds.configData.get('enableStatesNextFrame', True):
            self.set_old_states(old)
        else:
            self.set_new_states(old)

    def set_statesToAll(self, old):
        oldstates = self.states
        self.syncSubProps()
        self.set_states(oldstates)

    def set_statesToSub(self, old):
        oldstates = self.states
        self.syncSubProps()
        self.set_states(oldstates)

    def set_new_states(self, old):
        if self._set_states not in STATES_FUN_SET:
            BigWorld.callback(0.0, self.set_states_nextFrame)
            STATES_FUN_SET.add(self._set_states)

    def set_states_nextFrame(self):
        STATES_FUN_SET.remove(self._set_states)
        self._set_states(None)

    def set_old_states(self, old):
        self._set_states(old)

    def _set_states(self, old):
        if not self.inWorld:
            return
        if not self.fashion:
            return
        if not self.needSyncState():
            return
        if self.id == BigWorld.player().id:
            return
        self.lastSyncStateClientTime = BigWorld.time()
        if self.IsMonster and (getattr(self, 'visibleGbId', 0) > 0 and self.visibleGbId != BigWorld.player().gbId or getattr(self, 'visibleGroupNUID', 0) > 0 and self.visibleGroupNUID != BigWorld.player().groupNUID):
            return
        self.syncStatesClientPub()

    def needSyncState(self):
        p = BigWorld.player()
        if not clientcom.needDoOptimize():
            return True
        if hasattr(self, 'bianshen'):
            if self.bianshen[0] == gametypes.BIANSHEN_ZAIJU and self.bianshen[1] == WWCD.data.get('robZaijuNo', 6019):
                return True
        if self != p and self.IsAvatar and utils.getNow() <= getattr(self, 'stateForceSyncTime', 0):
            return True
        pos = p.position
        distToPlayer = (self.position - pos).length
        if distToPlayer > gameglobal.SYNCSTATE_DIST:
            return False
        if not gameglobal.rds.configData.get('enableStatesNextFrame', True):
            now = BigWorld.time()
            if now - self.lastSyncStateClientTime < gameglobal.SYNCSTATE_TIME:
                return False
        return True

    def syncStatesClientPub(self, isInit = False):
        now = BigWorld.player().getServerTime()
        res = {}
        for data in self.states:
            stateId, stateSrcId, layer, relativeEndTime = utils.loadStateValue(data)
            endTime = -1 if relativeEndTime == 0 else utils.getRealTimeFromServerBootTime(relativeEndTime)
            res.setdefault(stateId, []).append((layer,
             now,
             -1 if endTime == -1 else endTime - now,
             stateSrcId))

        for (stateId, stateSrcId), (endTime, layer) in self.curTmpStates.items():
            if endTime != -1 and endTime < now:
                self.curTmpStates.pop((stateId, stateSrcId))
            res.setdefault(stateId, []).append((layer,
             now,
             -1 if endTime == -1 else endTime - now,
             stateSrcId))

        self.statesClientPub = res
        if not isInit and not self.isRealModel:
            return
        self.clientEffectIcon()
        self.clientStateEffect.updateEffect(set(self.statesClientPub.keys()))
        self.statesOld = copy.deepcopy(self.statesClientPub)

    def addState(self, stateId, endTime, stateSrcId, layer):
        if not self.needSyncState():
            return
        self.curTmpStates[stateId, stateSrcId] = (endTime, layer)
        self.syncStatesClientPub()

    def removeState(self, stateId, stateSrcId):
        key = (stateId, stateSrcId)
        if key in self.curTmpStates:
            self.curTmpStates.pop(key)
        self.syncStatesClientPub()

    def enterTopLogoRange(self, rangeDist = -1):
        opValue = self.getOpacityValue()
        if not self.firstFetchFinished and not opValue[1]:
            return
        super(ICombatUnit, self).enterTopLogoRange(rangeDist)

    def afterModelFinish(self):
        super(ICombatUnit, self).afterModelFinish()
        if self.topLogo:
            self.topLogo.bindVisible()
        if self.hidingPower:
            self.model.bkgLoadTint = False
            self.resetHiding()
        self.refreshOpacityState()
        if hasattr(self, 'lifeLinkInfo'):
            lifeLinkManager.getInstance().update(self.id, self.lifeLinkInfo)

    def leaveWorld(self):
        global DYING_DELAY_LIST
        self.hitStateType = action.UNKNOWN_STATE
        self.oldModel = None
        DYING_DELAY_LIST.discard(self)
        self.tintStateType = [0, None]
        if self.tintDelCallBack:
            BigWorld.cancelCallback(self.tintDelCallBack)
            self.tintDelCallBack = None
        self.clientStateEffect.release(True)
        self.clientStateEffect = None
        self.skillPlayer.release()
        self.skillPlayer = None
        self.clientAuraEffect.release()
        self.clientAuraEffect = None
        if self.fashion != None:
            self.fashion.attachUFO(ufo.UFO_NULL)
            self.fashion.release()
            self.fashion = None
        if self.topLogo != None:
            self.topLogo.release()
            self.topLogo = utils.MyNone
        self.removeAllFx()
        tintalt.ta_reset(self.allModels)
        self.allModels = []
        player = BigWorld.player()
        if self.model != None and player != None and player != self and player.inWorld:
            self.model = None
        self.states = []
        self.effectOld = {}
        self.statesOld = {}
        if gameglobal.rds.ui.focusTarget.focusTarId == self.id:
            gameglobal.rds.ui.focusTarget.hide()
        lifeLinkManager.getInstance().removeEnt(self.id)

    def getTintModels(self, tintTypes):
        return self.allModels

    def needPlaySkill(self, skillId = None, skillLv = None):
        return True

    def needBlackShadow(self):
        return not self.getItemData().get('noBlackUfo', False)

    def faceTo(self, target, immediately = False):
        if not target:
            return
        if hasattr(self.filter, 'keepYawTime'):
            self.filter.keepYawTime = 999999
            self.filter.clientYawMinDist = 0.0
        self.filter.setYaw((target.position - self.position).yaw)

    def resetClientYawMinDist(self):
        if not self.inWorld:
            return
        if self.life == gametypes.LIFE_DEAD:
            self.filter.clientYawMinDist = gameglobal.CLIENT_DEAD_YAW_DIST
        else:
            self.filter.clientYawMinDist = gameglobal.CLIENT_MIN_YAW_DIST
        if hasattr(self.filter, 'keepYawTime'):
            self.filter.keepYawTime = 0.0

    def isSpriteBloodLabel(self, atkType, host):
        if host and host.IsSummonedSprite or self.IsSummonedSprite:
            p = BigWorld.player()
            if self == p or host == p:
                return False
            if not self.IsSummonedSprite and atkType in (ATK_TYPE_HEAL, ATK_TYPE_HEAL_CRIT):
                return False
            if self.IsSummonedSprite and atkType in (ATK_TYPE_SPRITE_MULTI1, ATK_TYPE_SPRITE_MULTI2):
                return False
            return True
        else:
            return False

    def showSpriteComboDamageLabel(self, host, result):
        comboNum = result.comboNum
        dmg = sum(result.dmgs) - result.comboDmg * comboNum
        interval = SYSCD.data.get('spriteComboDamageLabelInterval', 0.2)
        delay = interval
        for x in xrange(comboNum + 1):
            atkType = ATK_TYPE_SPRITE_MULTI1 if x < comboNum else ATK_TYPE_SPRITE_MULTI2
            BigWorld.callback(delay, Functor(self.bloodLabel, result.comboDmg, ATK_TYPE_NORMAL_HTI, 0, False, host))
            BigWorld.callback(delay, Functor(self.bloodLabel, dmg, atkType, 0, False, host))
            delay += interval
            dmg = dmg + result.comboDmg

    def bloodLabel(self, value, akType = 0, offset = 0, isSkill = False, host = None):
        gamelog.debug('wy:bloodLabel:', value, akType, isSkill)
        if self == BigWorld.player() and self.life == gametypes.LIFE_DEAD:
            return
        value = round(value)
        isSpriteHost = self.isSpriteBloodLabel(akType, host)
        if isSpriteHost:
            if self.model:
                node = self.model.node(gameglobal.HIT_NODE_MAP[gameglobal.NORMAL_HIT])
                if not node:
                    node = self.model.node('Scene Root')
            else:
                node = None
        else:
            node = self.getHitNodeRandom()
        if node == None:
            gamelog.error('Error can not find hit node ')
            return
        m = Math.Matrix(node)
        x, y = clientcom.worldPointToScreen(m.applyToOrigin())
        if not isSpriteHost or isSpriteHost and akType not in (ATK_TYPE_SPRITE_MULTI1, ATK_TYPE_SPRITE_MULTI2):
            if akType == gametypes.UI_BE_HEAL:
                x = x + random.randint(-1, 1) * 10
                y = y + random.randint(-1, 1) * 10
            else:
                seed = random.randint(0, 5)
                if seed == 1:
                    x += 20
                elif seed == 2:
                    y -= 20
                elif seed == 3:
                    x -= 20
                elif seed == 4:
                    y += 20
            x = x - 20
            y = y - 40
            if offset:
                y += random.choice([0, offset, 2 * offset])
                x += random.choice([-40, 0, 40])
        direction = self.getLableDirection(host, isSpriteHost, x)
        scale = self.getBloodLableScale(isSpriteHost)
        gameglobal.rds.ui.showBroodLabel(akType, value, x, y, direction, isSpriteHost, scale, self.id)
        p = BigWorld.player()
        if isSkill and self.IsMonster and hasattr(self, 'inDying') and self.inDying == True:
            if not p.bianshiDict.has_key(self.id):
                p.bianshiDict[self.id] = 0
            if akType == gametypes.UI_BE_OTHER_CRIT or akType == gametypes.UI_BE_OTHER_HIT:
                p.bianshiDict[self.id] += 2
                gameglobal.rds.ui.dying.showCritical()
            else:
                p.bianshiDict[self.id] += 1
            gameglobal.rds.ui.dying.hit(p.bianshiDict[self.id])

    def getLableDirection(self, host, isSpriteHost, x):
        if isSpriteHost and host:
            hostx, hosty = clientcom.worldPointToScreen(host.position)
            selfx, selfy = clientcom.worldPointToScreen(self.position)
            return selfx < hostx
        else:
            return x <= BigWorld.screenWidth() / 2

    def getBloodLableScale(self, isSpriteHost):
        scale = 1.0
        if isSpriteHost:
            length = (self.position - BigWorld.player().position).length
            if length < 5:
                return scale
            elif length < 35:
                scale = 1 - (length - 5) * 0.02
                return scale
            else:
                return 0
        return scale

    def isGMHide(self):
        return False

    def needMoveNotifier(self):
        return True

    def updateBodySlope(self):
        pass

    def getSkillInfo(self, skillId, lv):
        skillInfo = SkillInfo(skillId, lv)
        return skillInfo

    def _startSpell(self, targetId, skillId, skillLevel, time, targetPos, keep = 0):
        gamelog.debug('@PGF:startSpell:iCombatUnit startSpell', targetId, skillId, skillLevel, time, keep)
        self.spellInfo = (BigWorld.time(), time)
        en = BigWorld.entity(targetId)
        if en != None:
            self.skillPlayer.startSpell(en, skillId, skillLevel, time, targetPos, keep)
            self.calcIndicator(targetId, skillId, skillLevel)
        else:
            gamelog.debug('zf9:BigWorld.entity is none')

    def startSpell(self, targetId, skillId, skillLevel, time, targetPos, yaw):
        if not self.isRealModel:
            return
        if not self.needPlaySkill():
            return
        if not self._resultCheck():
            return
        self.resetClientYawMinDist()
        self._startSpell(targetId, skillId, skillLevel, time, targetPos)

    def skillStart(self, targetId, skillId, skillLevel, instant, targetPos):
        self._skillStart(targetId, skillId, skillLevel, 0, 0.0, None, instant, targetPos)

    def skillStartWithMove(self, targetId, skillId, skillLevel, moveId, moveTime, moveClientRefInfo, instant, targetPos):
        self._skillStart(targetId, skillId, skillLevel, moveId, moveTime, moveClientRefInfo, instant, targetPos)

    def _skillStart(self, targetId, skillId, skillLevel, moveId, moveTime, moveClientRefInfo, instant, targetPos):
        if not self.isRealModel:
            return
        if not self.needPlaySkill():
            return
        if not self._resultCheck():
            return
        self.resetClientYawMinDist()
        en = BigWorld.entity(targetId)
        if en != None:
            if targetPos and self.skillPlayer:
                self.skillPlayer.targetPos = Math.Vector3(targetPos[0], targetPos[1], targetPos[2])
            else:
                self.skillPlayer.targetPos = None
            self.skillPlayer.castSkill(targetId, skillId, skillLevel, None, instant, False, moveId, moveTime, moveClientRefInfo)
            clientSkillInfo = self.getClientSkillInfo(skillId, skillLevel)
            en.skillPlayer.playBeCastedEffect(skillId, skillLevel, clientSkillInfo, True)
            if self == BigWorld.player():
                skillInfo = self.getSkillInfo(skillId, skillLevel)
                if self.skillPlayer.hasRestorableDelayCd(self, skillInfo, True):
                    self.skillPlayer.updateCastDelayOnlySkillState(skillInfo, 0.0)
                else:
                    self.skillPlayer.updateSkillState(skillInfo, 0.0, 0.0, instant)

    def _skillAlert(self, alertEff, targetId, targetPos, skillId, skillStage, specifiedYaw = None):
        effId, stage, posType, xscale, zscale, duration, dist, angle, playRate = alertEff
        if stage != skillStage:
            return
        if BigWorld.player().inFuben():
            duration = limit(duration, 1, gameglobal.EFFECT_LAST_TIME_IN_FUEBN)
        else:
            duration = limit(duration, 1, 10)
        if posType == gameglobal.MONSTER_SKILL_ALERT_EFF_SELF:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             effId,
             sfx.EFFECT_LIMIT,
             duration))
        elif posType in (gameglobal.MONSTER_SKILL_ALERT_EFF_SELF_POS,
         gameglobal.MONSTER_SKILL_ALERT_EFF_POS,
         gameglobal.MONSTER_SKILL_ALERT_EFF_TARGET_POS,
         gameglobal.MONSTER_SKILL_ALERT_EFF_SELF_BIAS,
         gameglobal.MONSTER_SKILL_ALERT_EFF_TARGET_POS_CONNECTION_BIAS):
            pos = None
            if posType == gameglobal.MONSTER_SKILL_ALERT_EFF_SELF_POS:
                pos = self.position
            elif posType == gameglobal.MONSTER_SKILL_ALERT_EFF_POS:
                pos = targetPos
            elif posType == gameglobal.MONSTER_SKILL_ALERT_EFF_TARGET_POS:
                tgt = BigWorld.entities.get(targetId)
                if tgt:
                    pos = tgt.position
            elif posType == gameglobal.MONSTER_SKILL_ALERT_EFF_SELF_BIAS:
                pos = clientcom.getRelativePosition(self.position, self.yaw, angle, dist)
            elif posType == gameglobal.MONSTER_SKILL_ALERT_EFF_TARGET_POS_CONNECTION_BIAS:
                tgt = BigWorld.entities.get(targetId)
                if tgt:
                    diff = tgt.position - self.position
                    pos = clientcom.getRelativePosition(tgt.position, diff.yaw, angle, dist)
            if pos is not None:
                if pos == self.position:
                    yaw = self.yaw if specifiedYaw == None else specifiedYaw
                else:
                    yaw = (pos - self.position).yaw
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
                 self.getSkillEffectPriority(),
                 None,
                 effId,
                 sfx.EFFECT_LIMIT_MISC,
                 pos,
                 0,
                 yaw,
                 0,
                 duration))
        if fx:
            for fxItem in fx:
                fxItem.scale(xscale, 1, zscale)
                if playRate != 1 and playRate > 0.2:
                    fxItem.playRate(playRate)

            self.alertEffIds[0] = skillId
            self.alertEffIds[1] = stage
            self.alertEffIds[2].append(effId)
            self.addFx(effId, fx)

    def removeAlertEffFx(self, skillId, skillStage):
        if skillId != self.alertEffIds[0]:
            for effId in self.alertEffIds[2]:
                self.removeFx(effId)

            self.alertEffIds = [0, 0, []]
            return
        if self.alertEffIds[1] < skillStage:
            return
        for effId in self.alertEffIds[2]:
            self.removeFx(effId)

        self.alertEffIds = [0, 0, []]

    def skillAlert(self, targetId, skillId, skillLevel, targetPos, skillStage, specifiedYaw = None):
        try:
            clientSkillInfo = self.getClientSkillInfo(skillId, skillLevel)
        except:
            msg = '@PGF:skillAlert skill data error: skillId:%d, skillLv:%d, id:%d, charType:%d, targetId:%d' % (skillId,
             skillLevel,
             self.id,
             self.charType,
             targetId)
            raise Exception(msg)

        alertEff = clientSkillInfo.getSkillData('alertEff', None)
        if alertEff:
            try:
                self.removeAlertEffFx(skillId, skillStage)
                if type(alertEff[0]) not in (tuple, list):
                    self._skillAlert(alertEff, targetId, targetPos, skillId, skillStage, specifiedYaw)
                    return
                for eff in alertEff:
                    self._skillAlert(eff, targetId, targetPos, skillId, skillStage, specifiedYaw)

            except:
                gamelog.error('@PGF:IMonsterCombatUnit.startSpell: Error alertEff data', self.charType, skillId, alertEff)

    def calcIndicator(self, targetID, skillID, skillLevel):
        skillInfo = SkillInfo(skillID, skillLevel)
        showIndicator = skillInfo.getSkillData('showIndicator', 0)
        indicatorTime = skillInfo.getSkillData('indicatorTime', 0.0)
        if showIndicator == 1 and indicatorTime > 0:
            indicatorTarget = 0
            if skillInfo.hasSkillData('tgtSelf'):
                indicatorTarget = self.id
            if skillInfo.hasSkillData('tgtEnemyType'):
                indicatorTarget = targetID
            target = BigWorld.entities.get(indicatorTarget)
            if indicatorTarget != 0 and target != None:
                target.showIndicator(indicatorTime)

    def showIndicator(self, duration):
        if not self.inWorld or not self.topLogo:
            return
        if duration <= 0:
            return
        now = time.time()
        if self.indicator[0]:
            gcd = self.indicator[1]
            if now + duration > gcd:
                self.removeIndicator()
            else:
                return
        self.topLogo.showSkillIndicator()
        self.indicator[0] = True
        self.indicator[1] = now + duration
        self.indicatorTimer = BigWorld.callback(duration, Functor(self.removeIndicator))

    def removeIndicator(self):
        if not self.inWorld or not self.topLogo:
            return
        if not self.indicator[0]:
            return
        if self.indicatorTimer > 0:
            BigWorld.cancelCallback(self.indicatorTimer)
            self.indicatorTimer = 0
        self.topLogo.removeSkillIndicator()
        self.indicator[0] = False
        self.indicator[1] = 0

    def stopCast(self, skillId, skillLv, targetId, stopAction):
        pass

    def stopSkillMove(self, stopAction = True):
        pass

    def stopSpell(self, success):
        if success:
            self.skillPlayer.endSpell()
        else:
            self.skillPlayer.stopSpell()
        self.spellInfo = None

    def startGuideSkillTick(self, skillId, skillLv, tgtId, tgtPos):
        if not self._resultCheck():
            return
        self.resetClientYawMinDist()
        skillInfo = self.getSkillInfo(skillId, skillLv)
        clientSkillInfo = self.getClientSkillInfo(skillId, skillLv)
        needFlyDelay = skillInfo.getSkillData('needFlyDelay', 0)
        guideType = skillDataInfo.getGuideType(clientSkillInfo)
        self.skillPlayer.targetPos = tgtPos
        if guideType == gameglobal.GUIDE_FLYER and needFlyDelay:
            self.skillPlayer.processGuideFlyerDamage(skillInfo, clientSkillInfo, None, tgtId)

    def getOperationMode(self):
        return gameglobal.KEYBOARD_MODE

    def modelHighlight(self, host, hitTintData):
        if gameglobal.gDisableHighLight:
            return
        if not hitTintData:
            return
        if self.life == gametypes.LIFE_DEAD:
            return
        hitTintId = hitTintData[0]
        if self.tintStateType[0] > 1:
            return
        allModels = self.allModels
        if len(hitTintData) == 2:
            allModels = self.getTintModels(hitTintData[1])
        fresnelColor = skillDataInfo.getTintHitDataInfo(hitTintId)
        self.tintStateType[0] = 1
        self.tintStateType[1] = fresnelColor
        tintalt.ta_addHitGaoLiang(allModels, gameglobal.HIT_HIGHLIGHT_BEGINTIME, gameglobal.HIT_HIGHLIGHT_KEEPTIME, gameglobal.HIT_HIGHLIGHT_ENDTIME, fresnelColor, host, self)

    def addTint(self, tintId, allModels, duration = 0, host = None, delay = 0.0, tintType = tintalt.UNKNOWTINT, force = False):
        tintName, tintPrio, tint = skillDataInfo.getTintDataInfo(self, tintId)
        self.tintIdMapTintName[tintId] = (tintName, tintPrio, tint)
        if (self.tintStateType[0] > tintPrio or self.tintStateType[1] == tintName) and not force:
            return
        if self.tintStateType[1]:
            BigWorld.callback(delay, Functor(tintalt.ta_del, allModels, self.tintStateType[1], None, False, False, tintType))
            if self.tintStateType[0] <= tintPrio:
                self.restoreTintStateType()
        for model in allModels:
            tintalt.addExtraTint(model, tintName, [tint, BigWorld.shaderTime()], duration, None, False, False, host, self, tintType)

        if self.tintDelCallBack:
            BigWorld.cancelCallback(self.tintDelCallBack)
            self.tintDelCallBack = None
        self.tintStateType[0] = tintPrio
        self.tintStateType[1] = tintName
        if duration > 0:
            self.tintDelCallBack = BigWorld.callback(duration, Functor(self.restoreTint, tintPrio))

    def restoreTint(self, tintPrio):
        if self.tintStateType[0] <= tintPrio:
            self.restoreTintStateType()

    def restoreTintStateType(self):
        self.tintStateType[0] = 0
        if not self.tintStateType[1]:
            return
        if type(self.tintStateType[1]) == tuple:
            tintalt.ta_delGaoLiang(self.allModels)
        else:
            tintalt.ta_del(self.allModels, self.tintStateType[1])
        self.tintStateType[1] = None

    def attachEffect(self, effectId, pos, yaw, scale = 1.0):
        if not self.inWorld:
            return
        needKeepFx = SFD.data.get(effectId, {}).get('modelKeepFx', False)
        if needKeepFx:
            delayTime = gameglobal.INPOS_EFFECT_LAST_TIME
        else:
            delayTime = gameglobal.EFFECT_LAST_TIME
        if pos:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             None,
             effectId,
             sfx.EFFECT_UNLIMIT,
             pos,
             0,
             yaw,
             0,
             delayTime))
        else:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             self.model,
             effectId,
             sfx.EFFECT_LIMIT,
             delayTime))
        if fx:
            for fxItem in fx:
                if fxItem:
                    fxItem.scale(scale, scale, scale)

        return fx

    def getSkinMaterial(self):
        return gameglobal.SKIN_MATERIAL_NO

    def getBodyEquipMaterail(self):
        if hasattr(self, 'aspect'):
            equipData = EQD.data.get(self.aspect.body, None)
            if equipData:
                return SYSCD.data.get('soundMaterialDict', {}).get(equipData.get('materialType', None))

    def beHit(self, host, damage = None, callback = None, forceBeHitAct = False, clientSkillInfo = None):
        pass

    def breakBeHitAction(self):
        if self.beHitActionName:
            try:
                self.model.action(self.beHitActionName).stop()
            except:
                pass

            self.beHitActionName = None

    def needEnableAlpha(self):
        return self.fashion.doingActionType() == action.JIDAO_STOP_ACTION

    def beginDaoDiStartAction(self, startActions, sId, loopActions):
        self.daoDiStartAction = startActions
        self.daoDiLoopAction = loopActions
        self.daoDiStateId = sId

    def clearDaoDiAction(self):
        self.daoDiStartAction = None
        self.daoDiLoopAction = None
        self.daoDiStateId = 0

    def getDaoDiActionTime(self):
        duration = 0
        try:
            for ac in self.daoDiStartAction:
                duration += self.model.action(ac).duration

        except:
            pass

        return duration

    def playDaoDiStartAction(self):
        if not self.daoDiStartAction:
            return
        self.fashion.playAction(self.daoDiStartAction, action.JIDAO_START_ACTION)
        state = self.getStates().get(self.daoDiStateId)
        if state and state[0]:
            stateStartTime = state[0][gametypes.STATE_INDEX_STARTTIME]
            duration = state[0][gametypes.STATE_INDEX_LASTTIME]
            actionTime = self.getDaoDiActionTime()
            if stateStartTime + duration - time.time() > actionTime:
                self.clientStateEffect.resetStateLoopAction(actionTime, self.daoDiStateId, self.daoDiLoopAction, action.JIDAO_START_ACTION)

    def _getSkinMaterialSoundPath(self, hitWeaponType = None, skinMaterial = None):
        if hitWeaponType and skinMaterial:
            return 'hit' + str(hitWeaponType) + '_' + str(skinMaterial)
        else:
            return None

    def _playBeHitSkinMaterialSound(self, host, hitWeaponType = None, dmgPowerType = 0.0, kill = False):
        if dmgPowerType not in [gametypes.DMGPOWER_NORMAL,
         gametypes.DMGPOWER_CRIT,
         gametypes.DMGPOWER_AVOID,
         gametypes.DMGPOWER_BLOCK]:
            return
        if not host or not host.inWorld:
            return
        if self.getOpacityValue()[0] == gameglobal.OPACITY_HIDE_INCLUDE_ATTACK:
            return
        if self.inHiding() and self != BigWorld.player():
            return
        if host.fashion.isPlayer or self.fashion.isPlayer:
            skinMaterial = self.getBodyEquipMaterail()
            if not skinMaterial:
                skinMaterial = self.getSkinMaterial()
            soundPath = self._getSkinMaterialSoundPath(hitWeaponType, skinMaterial)
            if soundPath:
                path = 'fx/Weapon/' + soundPath
                hitWeaponTime = 0
                if dmgPowerType == gametypes.DMGPOWER_CRIT:
                    hitWeaponTime = 1
                if self._isHitMaterialSoundCanPlay(path):
                    gameglobal.rds.sound.playHitFx(path, 'param_skill', hitWeaponTime, self, 1)
        if dmgPowerType in gametypes.DMGPOWERS_NORMAL_CRIT:
            modelID = self.fashion.modelID
            beHitSoundData = ABSD.data.get(modelID)
            if beHitSoundData:
                rateKey = 'hitRate' if dmgPowerType == gametypes.DMGPOWER_NORMAL else 'critHitRate'
                hitRate = beHitSoundData.get(rateKey, 0)
                if self._isHitConfigSoundCanPlay(hitRate):
                    soundKey = 'hitSoundID' if dmgPowerType == gametypes.DMGPOWER_NORMAL else 'critHitSoundID'
                    gameglobal.rds.sound.playSound(beHitSoundData.get(soundKey, 0))

    def refreshStateEffect(self):
        if not self.firstFetchFinished:
            return
        self.refreshOpacityState()
        self.clientStateEffect.refresh()

    def _getStateTimeMap(self, state):
        timeMap = {}
        for key, value in state.items():
            for st in value:
                timeOld = timeMap[key, st[gametypes.STATE_INDEX_SRCID]][gametypes.STATE_INDEX_LASTTIME] if timeMap.has_key((key, st[gametypes.STATE_INDEX_SRCID])) else None
                timeNew = st[gametypes.STATE_INDEX_LASTTIME]
                if not timeOld or timeOld < timeNew:
                    timeMap[key, st[gametypes.STATE_INDEX_SRCID]] = st

        return timeMap

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

    def dealGroupStateIcon(self, newSet):
        if not BigWorld.player().inFuben():
            return
        if not gameglobal.rds.ui.group.groupMemMed:
            return
        newData = []
        i = 0
        for stateId, srcId, lastTime, layerNum, startTime in newSet:
            isHide = SD.data.get(stateId, {}).get('iconUnshow', 0)
            iconType = SD.data.get(stateId, {}).get('iconShowType', 3)
            unShowInTgt = SD.data.get(stateId, {}).get('unShowInTgt', 0)
            if unShowInTgt and srcId != BigWorld.player().id:
                continue
            if isHide or iconType != 1 and iconType != 3:
                continue
            data = self._getTargetStateData(self, stateId, srcId, lastTime, layerNum, startTime)
            newData.append(data)
            i = i + 1
            if i == 4:
                break

        gameglobal.rds.ui.group.setStateIcon(self.id, newData)

    def getTeamStateDataByEntId(self, entId):
        newData = []
        ent = BigWorld.entities.get(entId)
        if not ent:
            return newData
        p = BigWorld.player()
        if p == ent:
            newState = getattr(p, 'statesServerAndOwn', {})
        else:
            newState = getattr(ent, 'statesClientPub', {})
        flagState = self.flagStates if p == ent else []
        newStateMap = self._getStateTimeMap(newState)
        newStateMap.update(self._getFlagStateTimeMap(flagState))
        newSet = newStateMap.items()
        newSet.sort(key=lambda k: k[1][1])
        newSet = set([ (item[0][0],
         item[0][1],
         item[1][2],
         item[1][0],
         item[1][1]) for item in newSet ])
        i = 0
        for stateId, srcId, lastTime, layerNum, startTime in newSet:
            isHide = SD.data.get(stateId, {}).get('iconUnshow', 0)
            iconType = SD.data.get(stateId, {}).get('iconShowType', 3)
            unShowInTgt = SD.data.get(stateId, {}).get('unShowInTgt', 0)
            if unShowInTgt and srcId != BigWorld.player().id:
                continue
            if isHide or iconType != 1 and iconType != 3:
                continue
            data = self._getTargetStateData(ent, stateId, srcId, lastTime, layerNum, startTime)
            newData.append(data)
            i = i + 1
            if i == 4:
                break

        return newData

    def _needShowBossState(self):
        target = BigWorld.player().targetLocked
        if target.__class__.__name__ == 'VirtualMonster':
            master = BigWorld.entities.get(target.masterMonsterID)
        else:
            master = target
        if master and hasattr(master, 'charType'):
            showBlood = uiUtils._isNeedShowBossBlood(master.charType)
        else:
            showBlood = False
        return showBlood

    def _matchState(self, buffId, srcId, stateId, stateSrc):
        data = SD.data.get(int(buffId), None)
        separateShow = data.get('separateShow', 0)
        if separateShow:
            return int(buffId) == stateId and int(srcId) == stateSrc
        else:
            return int(buffId) == stateId

    def _getTargetStateData(self, ent, stateId, srcId, lastTime, layerNum, startTime):
        p = BigWorld.player()
        retData = {}
        iconType = SD.data.get(stateId, {}).get('iconShowType', 3)
        separateShow = SD.data.get(stateId, {}).get('separateShow', 0)
        special = SD.data.get(stateId, {}).get('isSpecial', 0)
        noNA = SD.data.get(stateId, {}).get('noNA', 0)
        if iconType in (uiConst.TYPE_BUFF_FUNC, uiConst.TYPE_BUFF_QUEST):
            iconType = uiConst.TYPE_BUFF_LAST
        originSrcId = srcId
        if not separateShow:
            srcId = p.id
        retData['type'] = iconType
        retData['srcId'] = srcId
        retData['id'] = stateId
        retData['special'] = special
        if not hasattr(ent, 'effect'):
            return retData
        data = SD.data.get(stateId, None)
        if data != None:
            retData['iconPath'] = str(data.get('iconId', 'notFound')) + '.dds'
            retData['timer'] = lastTime - (p.getServerTime() - startTime)
            if retData['timer'] > lastTime:
                retData['timer'] = lastTime
            if retData['timer'] > 36000 and not noNA or lastTime == -1:
                retData['timer'] = -100
            if not self._isHasState(ent, stateId, originSrcId):
                retData['count'] = 0
            elif not separateShow:
                retData['count'] = self.getTargetNoSepCount(stateId, ent)
            else:
                retData['count'] = layerNum
        return retData

    def _generateStatesData(self, target, set):
        statesData = []
        for stateId, srcId, lastTime, layerNum, startTime in set:
            isHide = SD.data.get(stateId, {}).get('iconUnshow', 0)
            unShowInTgt = SD.data.get(stateId, {}).get('unShowInTgt', 0)
            if unShowInTgt and srcId != BigWorld.player().id:
                continue
            if isHide:
                continue
            data = self._getTargetStateData(target, stateId, srcId, lastTime, layerNum, startTime)
            statesData.append(data)

        return statesData

    def dealTargetStateIcon(self, newSet, oldSet, isPart):
        addSet = newSet - oldSet
        delSet = oldSet - newSet
        target = BigWorld.player().targetLocked
        if not target:
            return
        if getattr(target, 'updateMergeBuff', None):
            addSet, delSet = target.updateMergeBuff(addSet, delSet)
        addTargetData = self._generateStatesData(target, addSet)
        delTargetData = self._generateStatesData(target, delSet)
        if addTargetData or delTargetData:
            if isPart:
                gameglobal.rds.ui.bossBlood.changePartStateIcon(addTargetData, delTargetData)
            else:
                gameglobal.rds.ui.target.changeStateIcon(addTargetData, delTargetData)

    def _getEntStates(self, ent):
        p = BigWorld.player()
        if p == ent:
            states = getattr(p, 'statesServerAndOwn', {})
        else:
            states = getattr(ent, 'statesClientPub', {})
        return states

    def getTargetNoSepCount(self, stateId, ent):
        states = self._getEntStates(ent)
        count = 0
        for state in states.get(stateId, []):
            count += state[gametypes.STATE_INDEX_LAYER]

        return count

    def _isHasState(self, ent, stateId, srcId = None):
        states = self._getEntStates(ent)
        hasKey = states.has_key(stateId)
        if hasKey and srcId:
            withSrc = False
            dataSet = states.get(stateId)
            for data in dataSet:
                if data[gametypes.STATE_INDEX_SRCID] == srcId:
                    withSrc = True
                    break

            return withSrc
        else:
            return hasKey

    def _isHasStateInclClientPub(self, ent, stateId):
        if stateId in getattr(ent, 'statesClientPub', {}) or stateId in getattr(ent, 'statesServerAndOwn', {}):
            return True
        return False

    def getState(self, ent, stateId):
        states = self._getEntStates(ent)
        return states.get(stateId, [])

    def _addTargetAllStateIcon(self, ent):
        if not self.needAddStateIcon():
            return
        newState = self._getEntStates(ent)
        p = BigWorld.player()
        newStateMap = self._getStateTimeMap(newState)
        flagState = p.flagStates if p == ent else []
        newStateMap.update(self._getFlagStateTimeMap(flagState))
        newSet = newStateMap.items()
        newSet.sort(key=lambda k: k[1][1])
        newSet = set([ (item[0][0],
         item[0][1],
         item[1][2],
         item[1][0],
         item[1][1]) for item in newSet ])
        if self._needShowBossState():
            self.dealTargetStateIcon(newSet, BigWorld.player().oldPartStateSet, True)
            BigWorld.player().oldPartStateSet = newSet
        else:
            self.dealTargetStateIcon(newSet, BigWorld.player().oldTargetStateSet, False)
            BigWorld.player().oldTargetStateSet = newSet

    def dealMasterStateIcon(self, ent, newSet, oldSet):
        if not self.needAddStateIcon():
            return
        addSet = newSet - oldSet
        delSet = oldSet - newSet
        self._changeMasterStateIcon(ent, addSet, delSet)

    def _changeMasterStateIcon(self, ent, addSet, delSet):
        addTargetData = []
        delTargetData = []
        for stateId, srcId, timeVal, layerNum, startTime in addSet:
            isHide = SD.data.get(stateId, {}).get('iconUnshow', 0)
            unShowInTgt = SD.data.get(stateId, {}).get('unShowInTgt', 0)
            if unShowInTgt and srcId != BigWorld.player().id:
                continue
            if isHide:
                continue
            data = self._getTargetStateData(ent, stateId, srcId, timeVal, layerNum, startTime)
            addTargetData.append(data)

        for stateId, srcId, timeVal, layerNum, startTime in delSet:
            isHide = SD.data.get(stateId, {}).get('iconUnshow', 0)
            if isHide:
                continue
            data = self._getTargetStateData(ent, stateId, srcId, timeVal, layerNum, startTime)
            delTargetData.append(data)

        if addTargetData or delTargetData:
            gameglobal.rds.ui.bossBlood.changeStateIcon(addTargetData, delTargetData)

    def _addMasterAllStateIcon(self, ent):
        newState = getattr(ent, 'statesClientPub', {})
        newStateMap = self._getStateTimeMap(newState)
        newSet = newStateMap.items()
        newSet.sort(key=lambda k: k[1][1])
        newSet = set([ (item[0][0],
         item[0][1],
         item[1][2],
         item[1][0],
         item[1][1]) for item in newSet ])
        self.dealMasterStateIcon(ent, newSet, BigWorld.player().oldMasterStateSet)
        BigWorld.player().oldMasterStateSet = newSet

    def forceUpdateEffect(self):
        self.clientStateEffect.effect = {}
        self.clientStateEffect.forceUpdate = True
        self.clientEffect({})
        self._forceUpdateStates()
        self.clientStateEffect.forceUpdate = False

    def _forceUpdateStates(self):
        if not self.inWorld:
            return
        oldState = {}
        newState = self.getStates()
        if oldState != newState:
            self.clientStateEffect.updateEffect(set(newState.keys()))
            stateIds = set(newState.keys()) ^ set(oldState.keys())
            for stateId in stateIds:
                states = newState.get(stateId, [])
                for state in states:
                    stateInfo = ClientSkillInfo(stateId, 0, 1)
                    isAffectSkill = stateInfo.getSkillData('affectSkill', 0)
                    if isAffectSkill:
                        gameglobal.rds.ui.actionbar.checkSkillStatOnPropModified()

    def clientEffect(self, old):
        if not self.isRealModel:
            return False
        if not hasattr(self, 'effect'):
            return
        if self.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        newMagic = set(self.effect.mf)
        oldMagic = set(old.get('mf', ()))
        delMagic = oldMagic - newMagic
        addMagic = newMagic - oldMagic
        if addMagic:
            if hasattr(self.model, 'noAttachFx_') and self.model.noAttachFx_:
                return
            for mfId, mfLv, sId, sLv, ownerId in addMagic:
                owner = None
                if ownerId:
                    owner = BigWorld.entities.get(ownerId)
                if owner and hasattr(owner, 'skillAppearancesDetail'):
                    data = owner.skillAppearancesDetail.getCreationAppearanceData(mfId)
                elif hasattr(self, 'skillAppearancesDetail'):
                    data = self.skillAppearancesDetail.getCreationAppearanceData(mfId)
                else:
                    data = CD.data.get(mfId, None)
                if data:
                    effect = data.get('keepEffect', ())
                    createionData = skill_creation_data.data.get(mfId, {})
                    lastTime = createionData.get('ttl', 0.0)
                    if effect:
                        for effId in effect[1:]:
                            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
                             self.getSkillEffectPriority(),
                             self.model,
                             effId,
                             sfx.EFFECT_LIMIT,
                             lastTime + gameglobal.EFFECT_LAST_TIME))
                            self.addFx(effId, fx)

        if delMagic:
            for mfId, mfLv, sId, sLv, ownerId in delMagic:
                owner = None
                if ownerId:
                    owner = BigWorld.entities.get(ownerId)
                if owner and hasattr(owner, 'skillAppearancesDetail'):
                    data = owner.skillAppearancesDetail.getCreationAppearanceData(mfId)
                elif hasattr(self, 'skillAppearancesDetail'):
                    data = self.skillAppearancesDetail.getCreationAppearanceData(mfId)
                else:
                    data = CD.data.get(mfId, None)
                if data:
                    if sId:
                        clientSkillInfo = self.getClientSkillInfo(sId, sLv)
                        if skillDataInfo.getCastLoop(clientSkillInfo):
                            self.skillPlayer.castLoop = False
                            self.fashion.stopAction()
                    effect = data.get('keepEffect', ())
                    if effect:
                        for effId in effect[1:]:
                            self.removeFx(effId)

        newAura = set(self.effect.aura)
        oldAura = set(old.get('aura', ()))
        delAura = oldAura - newAura
        addAura = newAura - oldAura
        for auraId in delAura:
            self.clientAuraEffect.removeAura(auraId)

        for auraId in addAura:
            self.clientAuraEffect.addAura(auraId)

    def clientBuffRefresh(self):
        p = BigWorld.player()
        if p == self:
            newState = getattr(p, 'statesServerAndOwn', {})
        else:
            newState = getattr(self, 'statesClientPub', {})
        flagState = self.flagStates if p == self else []
        newStateMap = self._getStateTimeMap(newState)
        newStateMap.update(self._getFlagStateTimeMap(flagState))
        newSet = newStateMap.items()
        newSet.sort(key=lambda k: k[1][1])
        newSet = set([ (item[0][0],
         item[0][1],
         item[1][2],
         item[1][0],
         item[1][1]) for item in newSet ])
        p.getOthersNewState(self, newSet, True)

    def isSkillEnhanceCntBuff(self, stateId):
        return gametypes.SKILL_STATE_SE_ENHANCE_PROP_BY_SKILL_CNT in SD.data.get(stateId, {}).get('allAttrIds', [])

    def genNewStateItemInfo(self, stateItem):
        stateId = stateItem[0][0]
        stateLayer = stateItem[1][0]
        if self.isSkillEnhanceCntBuff(stateId):
            stateLayer = getattr(self, 'stateSECount', {}).get(stateId, 0)
        return (stateItem[0][0],
         stateItem[0][1],
         stateItem[1][2],
         stateLayer,
         stateItem[1][1])

    def clientEffectIcon(self):
        if not self.needAddStateIcon():
            return
        p = BigWorld.player()
        if p == self:
            newState = getattr(p, 'statesServerAndOwn', {})
        else:
            newState = getattr(self, 'statesClientPub', {})
        flagState = self.flagStates if p == self else []
        newStateMap = self._getStateTimeMap(newState)
        tmpStateNeedIcon = {}
        if p == self:
            aura = WWCD.data.get('robAuraBuffID')
            if aura in getattr(p, 'statesClientPub', {}):
                tmpStateNeedIcon[aura] = getattr(p, 'statesClientPub', {}).get(aura)
            newStateMap.update(self._getStateTimeMap(tmpStateNeedIcon))
        newStateMap.update(self._getFlagStateTimeMap(flagState))
        newSet = newStateMap.items()
        newSet.sort(key=lambda k: k[1][1])
        newSet = set([ self.genNewStateItemInfo(item) for item in newSet ])
        master = None
        if self.IsAvatar and BigWorld.player().isInMyTeam(self):
            self.dealGroupStateIcon(newSet)
        if hasattr(p.targetLocked, 'masterMonsterID'):
            master = BigWorld.entities.get(p.targetLocked.masterMonsterID)
        if p == self:
            self.clientEmoteAct(newSet, p.oldPlayerStateSet)
            self.dealPlayerStateIcon(newSet)
        if master == self and hasattr(self, 'syncUnits') and self.syncUnits:
            self.dealMasterStateIcon(self, newSet, p.oldMasterStateSet)
            p.oldMasterStateSet = newSet
        elif p.targetLocked == self:
            if self._needShowBossState():
                self.dealTargetStateIcon(newSet, p.oldPartStateSet, True)
                p.oldPartStateSet = newSet
            else:
                self.dealTargetStateIcon(newSet, p.oldTargetStateSet, False)
                p.oldTargetStateSet = newSet
        elif not flagState:
            if p == self:
                self.dealPlayerStateIcon(newSet)
        p.getOthersNewState(self, newSet)

    def clientEmoteAct(self, newSet, oldSet):
        addSet = newSet - oldSet
        for buff in addSet:
            buffId = buff[0]
            emoteId = SCD.data.get(buffId, {}).get('emoteId', 0)
            if emoteId:
                self.wantToDoEmote(emoteId)
                return

    def set_effect(self, old):
        if not self.isRealModel and not getattr(self, 'inWenQuanState', False):
            return
        self.clientEffect(self.effectOld)
        self.effectOld = self.effect.deepcopy()

    def set_bannedSkils(self, old):
        gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_NO_SKILL)

    def set_statesServerAndOwn(self, old):
        if not self.isRealModel:
            return
        conditionalPropTips = getattr(self, 'conditionalPropTips', {})
        for pId, v in self.conditionalPropTips.iteritems():
            iconId = CPD.data.get(pId, {}).get('buffIconId', 0)
            if iconId not in self.statesServerAndOwn:
                self.statesServerAndOwn[iconId] = [(1,
                  utils.getNow(),
                  -1,
                  const.CONDITIONAL_FAKE_ICON_STATE_ID,
                  0)]

        self.clientEffectIcon()
        if self.firstFetchFinished:
            if self.statesClientAndOwn:
                self.statesServerAndOwn = dict(self.statesServerAndOwn)
                self.statesServerAndOwn.update(self.statesClientAndOwn)
            newState = self.statesServerAndOwn
            oldState = old
            if oldState != newState:
                self.clientStateEffect.updateEffect(set(newState.keys()))
                stateIds = set(newState.keys()) ^ set(oldState.keys())
                for stateId in stateIds:
                    states = self.statesServerAndOwn.get(stateId, [])
                    for state in states:
                        stateInfo = ClientSkillInfo(stateId, 0, 1)
                        isAffectSkill = stateInfo.getSkillData('affectSkill', 0)
                        if isAffectSkill:
                            gameglobal.rds.ui.actionbar.checkSkillStatOnPropModified()

        p = BigWorld.player()
        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            BigWorld.player().ap.aimCross.refreshStateIcon(self.id)
        self.statesOld = copy.deepcopy(self.getStates())

    def addBuffIconByClient(self, buffId):
        old = copy.deepcopy(self.statesServerAndOwn)
        if self.statesClientAndOwn.has_key(buffId):
            return
        now = utils.getNow()
        self.statesClientAndOwn[buffId] = [(1,
          now,
          -1,
          self.id,
          0)]
        self.set_statesServerAndOwn(old)

    def removeBuffIconByClient(self, buffId):
        if not self.statesClientAndOwn.has_key(buffId):
            return
        self.statesClientAndOwn.pop(buffId)
        if not self.statesServerAndOwn.has_key(buffId):
            return
        old = copy.copy(self.statesServerAndOwn)
        self.statesServerAndOwn.pop(buffId)
        self.set_statesServerAndOwn(old)

    def set_hp(self, old):
        if not self.isRealModel:
            return
        p = BigWorld.player()
        if p.targetLocked == self:
            gameglobal.rds.ui.target.setHp(self.hp)
            gameglobal.rds.ui.target.setMhp(self.mhp)
        if p.optionalTargetLocked == self:
            gameglobal.rds.ui.subTarget.setHp(self.hp)
            gameglobal.rds.ui.subTarget.setMhp(self.mhp)
        if p.targetLocked and hasattr(p.targetLocked, 'lockedId'):
            if p.targetLocked.lockedId == self.id:
                gameglobal.rds.ui.target.setTargetHp(self.hp)
                gameglobal.rds.ui.target.setTargetMhp(self.mhp)
            else:
                targetTarget = BigWorld.entities.get(p.targetLocked.lockedId)
                if targetTarget and targetTarget.__class__.__name__ == 'VirtualMonster' and targetTarget.masterMonsterID == self.id:
                    gameglobal.rds.ui.target.setTargetHp(self.hp)
                    gameglobal.rds.ui.target.setTargetMhp(self.mhp)
        if p.targetLocked and self._needShowBossState():
            if p.targetLocked.__class__.__name__ == 'VirtualMonster':
                master = BigWorld.entities.get(p.targetLocked.masterMonsterID)
            else:
                master = p.targetLocked
            if master and hasattr(master, 'lockedId') and master.lockedId == self.id:
                gameglobal.rds.ui.bossBlood.setTargetHp(self.hp)
                gameglobal.rds.ui.bossBlood.setTargetMhp(self.mhp)
        if gameglobal.rds.ui.multiBossBlood.mediator and hasattr(self, 'charType') and self.charType in gameglobal.rds.ui.multiBossBlood.bossCharType:
            gameglobal.rds.ui.multiBossBlood.updateBlood(self.charType, self.hp, self.mhp)
        if hasattr(self, 'topLogo') and self.topLogo:
            if self.mhp != 0:
                self.topLogo.onUpdateHp()
        if self.id == gameglobal.rds.ui.focusTarget.focusTarId or self.id == gameglobal.rds.ui.focusTarget.masterId:
            gameglobal.rds.ui.focusTarget.setHp(self.hp)
            gameglobal.rds.ui.focusTarget.setMhp(self.mhp)
        if gameglobal.rds.ui.focusTarget.tar2tarId == self.id or self.id == gameglobal.rds.ui.focusTarget.tar2tarMasterId:
            gameglobal.rds.ui.focusTarget.setTargetHp(self.hp)
            gameglobal.rds.ui.focusTarget.setTargetMhp(self.mhp)

    def set_mhp(self, old):
        if not self.isRealModel:
            return
        p = BigWorld.player()
        if p == self:
            gameglobal.rds.ui.player.setHp(self.hp)
            gameglobal.rds.ui.player.setMhp(self.mhp)
        if p.targetLocked == self:
            gameglobal.rds.ui.target.setHp(self.hp)
            gameglobal.rds.ui.target.setMhp(self.mhp)
        if p.optionalTargetLocked == self:
            gameglobal.rds.ui.subTarget.setHp(self.hp)
            gameglobal.rds.ui.subTarget.setMhp(self.mhp)
        if p.targetLocked and hasattr(p.targetLocked, 'lockedId'):
            if p.targetLocked.lockedId == self.id:
                gameglobal.rds.ui.target.setTargetHp(self.hp)
                gameglobal.rds.ui.target.setTargetMhp(self.mhp)
            else:
                targetTarget = BigWorld.entities.get(p.targetLocked.lockedId)
                if targetTarget and targetTarget.__class__.__name__ == 'VirtualMonster' and targetTarget.masterMonsterID == self.id:
                    gameglobal.rds.ui.target.setTargetHp(self.hp)
                    gameglobal.rds.ui.target.setTargetMhp(self.mhp)
        if p.targetLocked and self._needShowBossState():
            if p.targetLocked.__class__.__name__ == 'VirtualMonster':
                master = BigWorld.entities.get(p.targetLocked.masterMonsterID)
            else:
                master = p.targetLocked
            if master and hasattr(master, 'lockedId') and master.lockedId == self.id:
                gameglobal.rds.ui.bossBlood.setTargetHp(self.hp)
                gameglobal.rds.ui.bossBlood.setTargetMhp(self.mhp)
        if gameglobal.rds.ui.multiBossBlood.mediator and hasattr(self, 'charType') and self.charType in gameglobal.rds.ui.multiBossBlood.bossCharType:
            gameglobal.rds.ui.multiBossBlood.updateBlood(self.charType, self.hp, self.mhp)
        if hasattr(self, 'topLogo') and self.topLogo:
            if self.mhp != 0:
                self.topLogo.onUpdateHp()
        if self.id == gameglobal.rds.ui.focusTarget.focusTarId or self.id == gameglobal.rds.ui.focusTarget.masterId:
            gameglobal.rds.ui.focusTarget.setHp(self.hp)
            gameglobal.rds.ui.focusTarget.setMhp(self.mhp)
        if gameglobal.rds.ui.focusTarget.tar2tarId == self.id or self.id == gameglobal.rds.ui.focusTarget.tar2tarMasterId:
            gameglobal.rds.ui.focusTarget.setTargetHp(self.hp)
            gameglobal.rds.ui.focusTarget.setTargetMhp(self.mhp)

    def set_mp(self, old):
        if not self.isRealModel:
            return
        p = BigWorld.player()
        if p.targetLocked == self:
            gameglobal.rds.ui.target.setSp(self.mp)
            gameglobal.rds.ui.target.setMsp(self.mmp)
        if p.optionalTargetLocked == self:
            gameglobal.rds.ui.subTarget.setSp(self.mp)
            gameglobal.rds.ui.subTarget.setMsp(self.mmp)

    def set_mmp(self, old):
        if not self.isRealModel:
            return
        if self.IsCreation:
            return
        p = BigWorld.player()
        if p == self:
            gameglobal.rds.ui.player.setSp(self.mp)
            gameglobal.rds.ui.player.setMsp(self.mmp)
        if p.targetLocked == self:
            gameglobal.rds.ui.target.setSp(self.mp)
            gameglobal.rds.ui.target.setMsp(self.mmp)
        if p.optionalTargetLocked == self:
            gameglobal.rds.ui.subTarget.setSp(self.mp)
            gameglobal.rds.ui.subTarget.setMsp(self.mmp)

    def set_hpHole(self, old):
        if hasattr(self, 'topLogo') and self.topLogo:
            if self.mhp != 0:
                self.topLogo.onUpdateHp()

    def stopEpRegen(self):
        gameglobal.rds.ui.player.stopTweenEp()

    def getLongRangeHitNode(self, longRangehost):
        angle = self.getTgtAngle(longRangehost)
        gamelog.debug('getbeHitType:', angle)
        if self.hitStateType in [action.JIDAO_STATE, action.TIAOGAO_STATE, action.FUKONG_STATE]:
            return gameglobal.LIE_HIT
        elif angle >= -90.0 and angle < -30:
            return gameglobal.FRONT_RIGHT_LONG
        elif angle >= -30.0 and angle < 30:
            return gameglobal.FRONT_MID_LONG
        elif angle >= 30.0 and angle < 90:
            return gameglobal.FRONT_LEFT_LONG
        elif angle >= 90.0 and angle < 150:
            return gameglobal.BACK_LEFT_LONG
        elif angle >= 150.0 or angle < -150:
            return gameglobal.BACK_MID_LONG
        else:
            return gameglobal.BACK_RIGHT_LONG

    def getHitNodePairRandom(self, longRangehost = None):
        if not self.inWorld or not self.model:
            return None
        if longRangehost:
            hitType = self.getLongRangeHitNode(longRangehost)
            strHitNodeName = gameglobal.HIT_NODE_MAP[hitType]
            node = self.model.node(strHitNodeName)
            if node:
                return (node, strHitNodeName)
        index = random.randint(0, len(gameglobal.SHORT_RANGE_HIT_TUPLE) - 1)
        hitType = gameglobal.SHORT_RANGE_HIT_TUPLE[index]
        strHitNodeName = gameglobal.HIT_NODE_MAP[hitType]
        node = self.model.node(strHitNodeName)
        if node:
            return (node, strHitNodeName)
        strHitNodeName = gameglobal.HIT_NODE_MAP[gameglobal.NORMAL_HIT]
        node = self.model.node(strHitNodeName)
        if node:
            return (node, strHitNodeName)
        return (self.model.node('Scene Root'), None)

    def getHitNodeRandom(self, longRangehost = None):
        pair = self.getHitNodePairRandom(longRangehost)
        if pair:
            return pair[0]

    def _getDieDeadActionName(self):
        return (self.fashion.getDieActionName(), self.fashion.getDeadActionName())

    def checkPlayDieState(self):
        if not self.inWorld:
            return
        if self.life != gametypes.LIFE_DEAD:
            return
        actionType = self.fashion.doingActionType()
        if actionType == ACT.DEAD_ACTION:
            return
        dieActionName, dieIdleName = self._getDieDeadActionName()
        self.fashion.setDoingActionType(ACT.DEAD_ACTION)
        self._realPlayDieAction(dieActionName, dieIdleName, True)

    def playDieAction(self, needDieAction = True, forcePlayAction = False):
        if not self.inWorld or not self.fashion:
            return
        if self.life != gametypes.LIFE_DEAD:
            return
        actionType = self.fashion.doingActionType()
        if actionType == ACT.DEAD_ACTION or actionType in [ACT.FUKONG_START_ACTION,
         ACT.TIAOGAO_START_ACTION,
         ACT.JIDAO_START_ACTION,
         ACT.FAINT_START_ACTION,
         ACT.HIT_DIEFLY_ACTION] and not forcePlayAction:
            return
        needPlayAction = True
        gamelog.debug('jorsef2: playDieAction1', self.id, self.fashion.doingActionType())
        if self.fashion.doingActionType() in [ACT.JIDAO_LOOP_ACTION, ACT.TIAOGAO_LOOP_ACTION]:
            if self.IsMonster and hasattr(self, 'charType') and MMCD.data.get(self.charType, {}).get('dieActGround', None):
                needPlayAction = True
            else:
                needPlayAction = False
        gamelog.debug('jorsef3: playDieAction1', self.id, self.fashion.doingActionType(), needPlayAction)
        self.updateModelFreeze(-1.0)
        dieActionName, dieIdleName = self._getDieDeadActionName()
        if not needPlayAction:
            self.fashion.setDoingActionType(ACT.DEAD_ACTION)
            self.afterDieAction()
            if self.IsMonster and dieIdleName:
                self.playSpecialDie(dieIdleName)
            return
        self.fashion.attachUFO(ufo.UFO_SHADOW)
        if self.__class__.__name__ == 'EmptyZaiju':
            zaijuNo = getattr(self, 'zaijuNo', 0)
            itemData = EZD.data.get(zaijuNo, {})
            dieAction = itemData.get('dieAction', None)
            if dieAction:
                dieActionName = dieAction
            dieIdleAction = itemData.get('dieIdleAction', None)
            if dieIdleAction:
                dieIdleName = dieIdleAction
        self._realPlayDieAction(dieActionName, dieIdleName, needDieAction)

    def _realPlayDieAction(self, dieActionName, dieIdleName, needDieAction):
        palyActions = []
        if dieActionName and needDieAction:
            palyActions.append(dieActionName)
        if dieIdleName:
            palyActions.append(dieIdleName)
        gamelog.debug('jorsef3: playDieAction1', needDieAction)
        self.fashion.playAction(palyActions, ACT.DEAD_ACTION, self.afterDieAction)
        BigWorld.callback(0.2, self.checkPlayDieState)

    def afterDieAction(self):
        gamelog.debug('@zf:die: afterDieAction', self.id)
        if not self.inWorld or self.life != gametypes.LIFE_DEAD:
            return
        if self.model != None and len(self.model.motors) > 0:
            self.model.motors[0].matcherCoupled = False

    def attackAndLockTarget(self, targetId):
        p = BigWorld.player()
        if p.targetLocked != None or hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            return
        if len(self.targetCaps) > 0:
            p.lockTarget(self)

    def attackResultSimple(self, targetId, kill, nextAtkDelay = 0):
        self.attackResult(targetId, gametypes.DMGPOWER_NORMAL, [], nextAtkDelay)

    def otherDamage(self, hp, stateId = 0):
        if not self.isRealModel:
            return
        gamelog.debug('otherDamage', hp)
        if hp:
            node = self.getHitNodeRandom()
            if node != None:
                if stateId:
                    pairs = self.getSplitState(stateId, hp)
                    for pair in pairs:
                        if pair:
                            BigWorld.callback(pair[0], Functor(self.innerOtherDamage, pair[1]))

                else:
                    self.innerOtherDamage(hp)
            else:
                gamelog.error('Error can not find HP_hit in ', self.model.sources)

    def innerOtherDamage(self, hp):
        t = random.choice([0,
         0.1,
         0.15,
         0.2,
         0.25,
         0.3])
        if self == BigWorld.player():
            BigWorld.callback(t, Functor(self.bloodLabel, hp, 11, -30))
        else:
            BigWorld.callback(t, Functor(self.bloodLabel, hp, 111, -30))

    def getSplitState(self, stateId, damageSum):
        stateInfo = ClientSkillInfo(stateId, 1, 1)
        damTime = stateInfo.getSkillData('damTime', ())
        damBL = stateInfo.getSkillData('damBL', ())
        result = []
        l = len(damTime)
        damageLeft = damageSum
        if damTime and damBL and len(damTime) == len(damBL):
            for i in xrange(l):
                bl = float(damBL[i])
                hitNum = damageSum * bl
                if i == l - 1:
                    hitNum = damageLeft
                damageLeft -= hitNum
                result.append((damTime[i], hitNum))

        else:
            result.append((0, damageSum))
        return result

    def otherHeal(self, hp, stateId = 0):
        if not self.isRealModel:
            return
        gamelog.debug('jorsef: otherHeal')
        if hp:
            node = self.getHitNodeRandom()
            if node:
                if stateId:
                    pairs = self.getSplitState(stateId, hp)
                    for pair in pairs:
                        if pair:
                            BigWorld.callback(pair[0], Functor(self.bloodLabel, pair[1], 10))

                else:
                    BigWorld.callback(0.1, Functor(self.bloodLabel, hp, 10))

    def otherDamageMp(self, mp, stateId = 0):
        if not self.isRealModel:
            return
        if mp:
            node = self.getHitNodeRandom()
            if node != None:
                if stateId:
                    pairs = self.getSplitState(stateId, mp)
                    for pair in pairs:
                        if pair:
                            BigWorld.callback(pair[0], Functor(self.bloodLabel, pair[1], 12))

                else:
                    BigWorld.callback(0.1, Functor(self.bloodLabel, mp, 12))
            else:
                gamelog.error('Error can not find HP_hit in ', self.model.sources)

    def otherHealMp(self, mp, stateId = 0):
        if not self.isRealModel:
            return
        if mp:
            node = self.getHitNodeRandom()
            if node:
                if stateId:
                    pairs = self.getSplitState(stateId, mp)
                    for pair in pairs:
                        if pair:
                            BigWorld.callback(pair[0], Functor(self.bloodLabel, pair[1], 13))

                else:
                    BigWorld.callback(0.1, Functor(self.bloodLabel, mp, 13))

    def otherHealEp(self, ep):
        if not self.isRealModel:
            return
        if ep:
            node = self.getHitNodeRandom()
            if node:
                BigWorld.callback(0.1, Functor(self.bloodLabel, ep, 15))

    def _resultCheck(self):
        if not getattr(self, 'fashion', None):
            return False
        if self.life not in gametypes.LIFE_CAN_ATTACK:
            return False
        if not self.isRealModel:
            return False
        if not self.firstFetchFinished:
            return False
        opValue = self.getOpacityValue()
        if self.IsAvatar:
            if opValue[0] == gameglobal.OPACITY_HIDE_INCLUDE_ATTACK:
                return False
        elif opValue[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            if not self.inHiding():
                return False
        return True

    def _afterAttackResultCheck(self, target, firstAttack = False):
        p = BigWorld.player()
        if target and target.id == p.id:
            self.attackAndLockTarget(target.id)
        actionName = self.fashion.getAttackActionName()
        self.attackActionName = actionName
        action = None
        if actionName != None:
            try:
                action = self.model.action(actionName)
            except:
                gamelog.error("Error:Model %s can\'t find %s action" % (self.model.sources, actionName))
                return False

            self.fashion.playSingleAction(actionName, ACT.ATTACK_ACTION, 0, None, 0, 1, 0, True)
        else:
            return False
        if action is None:
            return False
        else:
            return action

    def attackResult(self, targetId, resultType, attackResult, nextAtkDelay = 0):
        if not self._resultCheck():
            return
        self.resetClientYawMinDist()
        target = BigWorld.entity(targetId)
        if target == None:
            return
        for resultSet in attackResult:
            if targetId == resultSet.eid and resultSet.kill and target.firstFetchFinished:
                DYING_DELAY_LIST.add(target)

        deadPlayBack.getInstance().takeResult(0, -1, 1, attackResult, None, 0, 0, 0)
        action = self._afterAttackResultCheck(target)
        if action:
            self.parseActionCue(action, target, resultType, attackResult, nextAtkDelay)
        self.nepLogKillMoster(attackResult)

    def parseActionCue(self, actObj, target, resultType, attackResult, nextAtkDelay = 0):
        result = actObj.haveCue(2)
        setCue = False
        if result != None:
            damageList = []
            delayList = []
            for res in result:
                delayTime = res[0]
                data = res[1]
                for i in data:
                    if i[0] == 'a':
                        try:
                            percent = int(i[1:]) * 0.01
                        except:
                            percent = 1

                        damageList.append(percent)
                        delayList.append(delayTime)
                        setCue = True

            if setCue:
                for resultSet in attackResult:
                    damageSum = 0
                    hpSum = 0
                    for pair in resultSet.results:
                        damageSum += sum(pair.dmgs)
                        hpSum += pair.hps

                    damageLeft = damageSum
                    hpLeft = hpSum
                    l = len(damageList)
                    for i in xrange(l):
                        hitNum = damageSum * damageList[i]
                        hpNum = hpSum * damageList[i]
                        if i == l - 1:
                            hitNum = damageLeft
                            hpNum = hpLeft
                        damageLeft -= hitNum
                        hpLeft -= hpNum
                        newResultData = self._genSkillData(hitNum, hpNum, resultSet)
                        BigWorld.callback(delayList[i], Functor(self.attackDamage, target, resultType, (newResultData,), nextAtkDelay))

        if not setCue:
            self.attackDamage(target, resultType, attackResult, nextAtkDelay)

    def attackResultPB(self, bytes):
        if not self.isRealModel:
            return
        if not self.needPlaySkill():
            return
        try:
            self.attackResult(*combatProto.attackResultProtoClient(bytes))
        except DecodeError:
            pass

    def damage(self, host, damageValue, damageAbsorb, mpsValue = 0, attackType = 0, isSkill = False, healAbsorb = None):
        if not self.inWorld or self.fashion == None:
            return
        p = BigWorld.player()
        node = self.getHitNodeRandom()
        if node == None:
            gamelog.error('zfhitnode: can not find HP_hit_default in model ', self.fashion.modelPath)
            return
        for value in damageValue:
            if value == 0:
                continue
            if host == p or host and (host.IsSummonedBeast and host.ownerId == p.id or host.IsSummonedSprite and host.ownerId == p.id):
                self.bloodLabel(-value, attackType + 100, isSkill=isSkill, host=host)
            elif self == p or self.IsSummonedBeast and self.ownerId == p.id or self.IsSummonedSprite and self.ownerId == p.id:
                self.bloodLabel(-value, attackType, isSkill=isSkill, host=host)
            elif hasattr(p, 'wingWorldCarrier'):
                carrierId = p.wingWorldCarrier.carrierEntId
                ent = BigWorld.entities.get(carrierId)
                if ent and ent == self:
                    self.bloodLabel(-value, attackType, isSkill=isSkill, host=host)

        for value in damageAbsorb:
            if value[0] == 0:
                continue
            if host == p or host and (host.IsSummonedBeast and host.ownerId == p.id or host.IsSummonedSprite and host.ownerId == p.id):
                self.bloodLabel(-value[0], gametypes.UI_BE_ABSORB + 100, isSkill=isSkill, host=host)
            elif self == p or self.IsSummonedBeast and self.ownerId == p.id or self.IsSummonedSprite and self.ownerId == p.id:
                self.bloodLabel(-value[0], gametypes.UI_BE_ABSORB, isSkill=isSkill, host=host)

        if not healAbsorb:
            healAbsorb = []
        for value in healAbsorb:
            if value[0] == 0:
                continue
            if value[1] != gametypes.SKILL_STATE_SE_HEAL_HOLE:
                continue
            if host == p or host and (host.IsSummonedBeast and host.ownerId == p.id or host.IsSummonedSprite and host.ownerId == p.id):
                self.bloodLabel(-value[0], gametypes.UI_BE_ABSORB_PURPLE + 100, isSkill=isSkill, host=host)
            elif self == p or self.IsSummonedBeast and self.ownerId == p.id or self.IsSummonedSprite and self.ownerId == p.id:
                self.bloodLabel(-value[0], gametypes.UI_BE_ABSORB_PURPLE, isSkill=isSkill, host=host)

        if mpsValue < 0:
            if host == p or host and host.IsSummonedSprite and host.ownerId == p.id:
                if self.IsSummonedSprite:
                    self.bloodLabel(mpsValue, ATK_TYPE_SPRITE_MAGIC_SUB, isSkill=isSkill, host=host)
                else:
                    self.bloodLabel(mpsValue, ATK_TYPE_PLAYER_BLUE_SUB, isSkill=isSkill, host=host)
            elif self == p or self.IsSummonedSprite and self.ownerId == p.id:
                if self.IsSummonedSprite:
                    self.bloodLabel(mpsValue, ATK_TYPE_SPRITE_MAGIC_SUB, isSkill=isSkill, host=host)
                else:
                    self.bloodLabel(mpsValue, ATK_TYPE_PLAYER_BLUE_SUB, isSkill=isSkill, host=host)

    def attackDamage(self, target, resultType, attackResult, nextAtkDelay = 0):
        if not self.inWorld or target == None or not target.inWorld:
            return
        if not self.firstFetchFinished:
            return
        for resultSet in attackResult:
            beAttack = BigWorld.entity(resultSet.eid)
            if beAttack and beAttack.hidingPower and beAttack.fashion.opacity == 0:
                continue
            isHeal = False
            dmgPowerType = gametypes.DMGPOWER_NORMAL
            for pair in resultSet.results:
                host = BigWorld.entity(pair.srcId)
                if pair.comboNum > 0:
                    beAttack.comboDamage(host, pair)
                else:
                    beAttack.damage(host, pair.dmgs, pair.damageAbsorb, pair.mps, pair.ars)
                if pair.hps:
                    beAttack.damage(host, (pair.hps,), [], pair.mps, gametypes.UI_BE_HEAL)
                beAttack.beHit(host, (sum(pair.dmgs), pair.ars))
                isHeal = isHeal or pair.hps
                dmgPowerType = pair.ars

            itemData = self.getItemData()
            hitWeaponData = itemData.get('hitWeaponType', None)
            if hitWeaponData and len(hitWeaponData) == 2:
                hitWeaponType = hitWeaponData[0]
                beAttack._playBeHitSkinMaterialSound(host, hitWeaponType, dmgPowerType, resultSet.kill)
            beAttack.playerHitEffect(host, None, {}, False, sum(pair.dmgs))
            effectId = beAttack.getStateFixHitEffect(True, isHeal)
            if effectId:
                beAttack.playHitEffect(host, effectId)
            if resultSet.kill:
                beAttack.die(host)
                host.afterDieEffect(beAttack)

    def afterDieEffect(self, target):
        if not target:
            return
        BigWorld.callback(0.2, Functor(sfx.soulFlyDemo, target, self.bodySize))

    def die(self, kill, clientSkillInfo = None):
        if self in DYING_DELAY_LIST:
            DYING_DELAY_LIST.discard(self)
            if getattr(self, 'hitFly', False):
                return
            if self.classname() == 'VirtualMonster':
                return
            if self.fashion.doingActionType() == ACT.DEAD_ACTION or self.life != gametypes.LIFE_DEAD:
                return
            p = BigWorld.player()
            if p.targetLocked == self:
                p.unlockTarget()
            if self.fashion == None:
                return
            if self.fashion.doingActionType() in (action.HITFLY_ACTION, action.DYING_ACTION):
                return
            self.stopSpell(False)
            if hasattr(self, 'downCliff') and self.downCliff:
                return
            self.playDieAction()

    def playDyingEffect(self):
        gamelog.debug('playDyingEffect', self.id)
        sfx.soulFlyDemo(self, self.bodySize, True)

    def skillResultPos(self, skillResult):
        self.skillResult(skillResult)

    def _damageSplit(self, damageData, damBL, damTime, host, skillInfo, clientSkillInfo, extInfo, showHitEff, strHitNodeName = None):
        damageSum = 0
        hpSum = 0
        if damageData.results:
            for pair in damageData.results:
                damageSum += sum(pair.dmgs)
                hpSum += pair.hps

        elif damageData.realDmg > 0:
            damageSum = damageData.realDmg
        else:
            hpSum = damageData.realDmg
        damageLeft = damageSum
        hpLeft = hpSum
        l = len(damTime)
        total = 100
        damCount = 0
        realT = 0
        for i in xrange(l):
            bl = float(damBL[i])
            t = float(damTime[i])
            total -= bl
            if total < 0:
                break
            hitNum = damageSum * bl
            hpNum = hpSum * bl
            extInfo_c = extInfo.copy()
            extInfo_c[gameglobal.FIRST_IN_SPLIT] = True if i == 0 else False
            if hitNum < 1 and hpNum < 1:
                newResultData = self._genSkillData(damageSum, hpSum, damageData)
                BigWorld.callback(float(damTime[i]), Functor(self.skillDamage, host, newResultData, skillInfo, clientSkillInfo, False, extInfo_c, showHitEff, strHitNodeName))
                return
            isSpriteHost = True if host and host.IsSummonedSprite or self.IsSummonedSprite else False
            if i == l - 1:
                hitNum = damageLeft
                hpNum = hpLeft
                t = float(damTime[i])
            elif isSpriteHost:
                t = float(damTime[i])
            else:
                seed = (float(damTime[i + 1]) - float(damTime[i])) / 2
                t = float(damTime[i]) + random.uniform(0, seed)
            damageLeft -= hitNum
            hpLeft -= hpNum
            gamelog.debug('skillDamage:_damageSplit', hitNum, bl, t)
            newResultData = self._genSkillData(hitNum, hpNum, damageData)
            realT = realT + t if isSpriteHost else t
            BigWorld.callback(realT, Functor(self.skillDamage, host, newResultData, skillInfo, clientSkillInfo, False, extInfo_c, showHitEff, strHitNodeName))
            damCount = int(damageSum - damageLeft)
            atkType = ATK_TYPE_SPRITE_MULTI1 if i < l - 1 else ATK_TYPE_SPRITE_MULTI2
            BigWorld.callback(realT, Functor(self.bloodLabel, -damCount, atkType, 0, True, host))

    def _genSkillData(self, hitNum, hpNum, damageData):
        resultSet = combatProto.PBResultSet(damageData.eid)
        resultSet.results = []
        resultSet.moveId = damageData.moveId
        resultSet.moveTime = damageData.moveTime
        resultSet.moveParam = damageData.moveParam
        resultSet.kill = damageData.kill
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
        return resultSet

    def skillDamage(self, host, damageResult, skillInfo, clientSkillInfo, needSplitDamage = True, extInfo = {}, showHitEff = True, strHitNodeName = None):
        if not self.inWorld:
            return
        if not self.firstFetchFinished or self.hidingPower and self.fashion.opacity == 0:
            return
        if not hasattr(self, 'skillPlayer'):
            return
        if not hasattr(self, 'fashion'):
            return
        p = BigWorld.player()
        if clientcom.needDoOptimize():
            needSplitDamage = False
        if needSplitDamage and (self == BigWorld.player() or host == p or getattr(host, 'ownerId', 0) == p.id or getattr(self, 'ownerId', 0) == p.id):
            if not host.inWorld or not hasattr(host, 'skillPlayer'):
                return
            stateKit = (host.skillPlayer.stateKit == -1 and [extInfo.get('mfStateKit', -1) % 10] or [host.skillPlayer.stateKit])[0]
            damTime, damBL = skillDataInfo.getSplitDamageData(clientSkillInfo)
            if stateKit != -1 and damTime and len(damTime) and damTime[0] == gameglobal.BUFF_CAST:
                if stateKit < len(damTime) - 1:
                    damTime = damTime[stateKit + 1]
                    damBL = damBL[stateKit + 1]
                else:
                    damTime = None
                    damBL = None
            if not damTime or not damBL or not damageResult.results:
                self.skillDamage(host, damageResult, skillInfo, clientSkillInfo, False, extInfo=extInfo, showHitEff=showHitEff, strHitNodeName=strHitNodeName)
                return
            if len(damageResult.results) > 0:
                self._damageSplit(damageResult, damBL, damTime, host, skillInfo, clientSkillInfo, extInfo, showHitEff, strHitNodeName)
            return
        self.refreshAimCrossFade()
        isDmg = False
        if not self._hideTeamMateInDying(host):
            hpNoChange = True
            isHeal = False
            dmtype = gametypes.DMGPOWER_NORMAL
            dmgPowerType = gametypes.DMGPOWER_NORMAL
            if damageResult.results:
                for pair in damageResult.results:
                    realHost = BigWorld.entity(pair.srcId)
                    dmgPowerType = pair.ars
                    if realHost:
                        if pair.hps or pair.healAbsorb:
                            ars = gametypes.UI_BE_HEAL
                            if pair.ars == gametypes.HEALPOWER_CRIT:
                                ars = pair.ars
                            self.damage(realHost, (pair.hps,), [], pair.mps, ars, True, pair.healAbsorb)
                            if pair.hps:
                                isHeal = True
                        if pair.dmgs and sum(pair.dmgs) > 0 or pair.damageAbsorb:
                            if pair.comboNum > 0:
                                self.comboDamage(host, pair)
                            else:
                                self.damage(realHost, pair.dmgs, pair.damageAbsorb, pair.mps, pair.ars, True)
                            hpNoChange = False
                        if pair.mps:
                            self.damage(realHost, pair.dmgs, pair.damageAbsorb, pair.mps, pair.ars, True)

            else:
                if damageResult.realDmg:
                    hpNoChange = False
                    self.beHit(host, (0, 0))
                if damageResult.realDmg < 0:
                    isHeal = True
            if not hpNoChange:
                hitWeaponData = skillDataInfo.getHitWeaponType(skillInfo)
                hitWeaponType = None
                hitWeaponTime = 0.0
                if hitWeaponData and len(hitWeaponData) == 2:
                    hitWeaponType = hitWeaponData[0]
                    hitWeaponTime = hitWeaponData[1]
                    if self.IsAvatar:
                        hitWeaponTime += 1.0
                self._playBeHitSkinMaterialSound(host, hitWeaponType, dmgPowerType, damageResult.kill)
                hitTintData = skillDataInfo.getHitTintId(self, skillInfo, clientSkillInfo, dmtype, host)
                if hitTintData:
                    self.modelHighlight(host, hitTintData)
                noNeedHit = skillDataInfo.getNoNeedHit(clientSkillInfo)
                if noNeedHit == gameglobal.NO_NEED_HIT_MONSTER and self.IsAvatar or noNeedHit == gameglobal.NO_NEED_HIT_AVATAR and self.IsMonster or not noNeedHit or self.needStateResistHit(noNeedHit, damageResult):
                    if damageResult.results:
                        pair = damageResult.results[0]
                        forceBeHitAct = skillInfo.getSkillData('forceHit', False)
                        if not damageResult.kill:
                            self.beHit(host, (sum(pair.dmgs), pair.ars), None, forceBeHitAct, clientSkillInfo)
                isCrit = extInfo.get(gameglobal.CRIT_CAM_SHAKE, False)
                self.playerHitEffect(host, clientSkillInfo, extInfo, isCrit, damageResult.realDmg)
            if host == self and hpNoChange and not isHeal:
                return
            if showHitEff:
                isDmg = not hpNoChange
                self.skillEffect(skillInfo, clientSkillInfo, host, dmtype, isDmg, isHeal, strHitNodeName)
        p = BigWorld.player()
        if self.IsAvatar and self.id == p.id and p.targetLocked == None and self != host:
            if gameglobal.rds.ui.actionbar.useSelfSkill != True:
                if p.getOperationMode() != gameglobal.ACTION_MODE and isDmg:
                    self.lockTarget(host)
        if host == p and self != host:
            if p.summonedSpriteInWorld:
                p.summonedSpriteInWorld.addTarget(self)
        if damageResult.kill:
            self.die(host, clientSkillInfo)

    def refreshAimCrossFade(self):
        p = BigWorld.player()
        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            if self == p.targetLocked or self == p.optionalTargetLocked:
                p.ap.refreshTargetFadeTimer()

    def refreshModelScale(self, model = None):
        if not getattr(self, 'inSpellAction', None):
            self.spellScale = 1
        if not getattr(self, 'stateModelScale', None):
            self.baseScale = 1
        if not model:
            model = self.model
        oldScale = model.scale
        bianshen = getattr(self, 'bianshen', None)
        if bianshen and bianshen[0] in (gametypes.BIANSHEN_RIDING_RB,):
            pass
        else:
            scale = self.baseScale * self.zaijuScale * self.spellScale
            if scale > 3:
                scale = 3
            elif scale < 0.5:
                scale = 0.5
            model.scale = scale * Math.Vector3(1, 1, 1)
        self.resetTopLogo()
        if self == BigWorld.player() and (oldScale - model.scale).length > 0.01:
            self.resetCamera()
            self.refreshOpacityState()

    def needStateResistHit(self, noNeedHit, damageResult):
        allAttrIds = set()
        for controllStateId, controllStateHit in damageResult.controllStateData:
            if controllStateHit or controllStateId == 0:
                continue
            allAttrIds = allAttrIds.union(set(SD.data.get(controllStateId, {}).get('allAttrIds', [])))

        controlSet = set([gametypes.SKILL_STATE_UNCONTROLLABLE])
        showId = allAttrIds.intersection(controlSet)
        if noNeedHit == gameglobal.NO_NEED_HIT_MONSTER and self.IsMonster and showId or noNeedHit == gameglobal.NO_NEED_HIT_AVATAR and self.IsAvatar and showId or noNeedHit == gameglobal.NO_NEED_HIT_ALL and showId or self.IsNaiveCombatUnit:
            return True
        return False

    def getPlayerHitEffect(self, clientSkillInfo, crit):
        playerHitEffect = 0
        if not clientSkillInfo:
            return playerHitEffect
        if crit:
            playerHitEffect = clientSkillInfo.getSkillData('playerCritHitEff', 0)
        else:
            playerHitEffect = clientSkillInfo.getSkillData('playerHitEff', 0)
        return playerHitEffect

    def getPlayerBeHitEffect(self, clientSkillInfo, crit, percent):
        playerHitEffect = 0
        if not clientSkillInfo:
            return playerHitEffect
        if crit:
            playerHitEffect = clientSkillInfo.getSkillData('playerCritBeHitEff', 0)
        else:
            playerHitEffect = clientSkillInfo.getSkillData('playerBeHitEff', 0)
        if playerHitEffect:
            return playerHitEffect
        effIds = None
        playerBeHitEffect = SYSCD.data.get('playerBeHitEffect', {})
        for percentPair in playerBeHitEffect.keys():
            if percentPair and len(percentPair) == 2:
                if percent > percentPair[0] and percent <= percentPair[1]:
                    effIds = playerBeHitEffect.get(percentPair, ())
                    break

        if effIds:
            return effIds[random.randint(0, len(effIds) - 1)]

    def playerHitEffect(self, host, clientSkillInfo, extInfo, crit, dmg):
        if not gameglobal.ENABLE_PLAYER_HIT_EFFECT:
            return
        if host == BigWorld.player():
            playerHitEffect = self.getPlayerHitEffect(clientSkillInfo, crit)
            if playerHitEffect:
                effectData = self.getHitEffectData(playerHitEffect)
                if not extInfo.has_key(gameglobal.FIRST_IN_SPLIT) or extInfo.get(gameglobal.FIRST_IN_SPLIT):
                    if not extInfo.get(gameglobal.IGNORE_HIT_EFFECT, None):
                        hitEffectDelay = effectData.get('hitEffectDelay', 0)
                        if hitEffectDelay:
                            BigWorld.callback(hitEffectDelay, Functor(self.playAllHitEffect, effectData))
                        else:
                            self.playAllHitEffect(effectData)
        elif self == BigWorld.player():
            percent = dmg * 1.0 / self.mhp * 100
            playerBeHitEffect = self.getPlayerBeHitEffect(clientSkillInfo, crit, percent)
            if playerBeHitEffect:
                effectData = self.getHitEffectData(playerBeHitEffect)
                if not extInfo.has_key(gameglobal.FIRST_IN_SPLIT) or extInfo.get(gameglobal.FIRST_IN_SPLIT):
                    if not extInfo.get(gameglobal.IGNORE_HIT_EFFECT, None):
                        hitEffectDelay = effectData.get('hitEffectDelay', 0)
                        if hitEffectDelay:
                            BigWorld.callback(hitEffectDelay, Functor(self.playAllHitEffect, effectData))
                        else:
                            self.playAllHitEffect(effectData)

    def getHitEffectData(self, hitEffectId):
        if gameglobal.STRONG_HIT:
            return HESD.data.get(hitEffectId, {})
        else:
            return HED.data.get(hitEffectId, {})

    def playAllHitEffect(self, effectData):
        self.playFreezeEffect(effectData)
        self.playCameraPush(effectData)
        self.playMotionBlur(effectData)
        self.playSpecialShakeCamera(effectData)
        self.playBodyShake(effectData)
        self.playZoomIn(effectData)

    def playBodyShake(self, effectData):
        if not self.inWorld:
            return
        if not gameglobal.modelShake:
            return
        if hasattr(self, 'atkType'):
            if self.atkType <= const.MONSTER_ATK_TYPE_NO_ATK:
                return
        params = effectData.get('shakeModel', None)
        if params:
            width = params[0]
            length = params[1]
            times = int(params[2])
            speed = params[3]
            attenuation = params[4]
            posList = self.getBodyShakePoint(width, length, times, attenuation)
            try:
                self.doShake(posList, speed)
            except:
                pass

    def inShake(self):
        return self.bodyShakeFlyer != None and self.bodyShakeFlyer.model

    def doShake(self, points, speed):
        if not self.inWorld or not self.model or self.life == gametypes.LIFE_DEAD:
            return
        if self.inShake():
            self.bodyShakeFlyer.release()
            self.bodyShakeFlyer = None
        self.bodyShakeFlyer = sfx.BodyShakeFlyer(self, points, speed)
        self.bodyShakeFlyer.start()

    def getBodyShakePoint(self, width, length, times, attenuation):
        bevel = math.sqrt(width * width + length * length)
        player = BigWorld.player()
        yaw = (player.position - self.position).yaw
        angle = math.atan(width * 1.0 / length) * 180 / math.pi
        posList = []
        for i in xrange(times):
            power = i * 4 if i != 0 else 1
            attenu = math.pow(attenuation, power)
            rightUp = utils.getRelativePosition(Math.Vector3(0, 0, 0), yaw, -180 + angle, bevel * attenu * math.pow(attenuation, 1))
            rightDown = utils.getRelativePosition(Math.Vector3(0, 0, 0), yaw, -angle, bevel * attenu * math.pow(attenuation, 3))
            leftUp = utils.getRelativePosition(Math.Vector3(0, 0, 0), yaw, 180 - angle, bevel * attenu * math.pow(attenuation, 2))
            leftDown = utils.getRelativePosition(Math.Vector3(0, 0, 0), yaw, angle, bevel * attenu * math.pow(attenuation, 4))
            posList.extend([rightUp,
             rightDown,
             leftUp,
             leftDown])

        return posList

    def genShakeWay(self, points, speed):
        way = []
        if points:
            for i in xrange(len(points)):
                if i < len(points) - 1:
                    way.append((points[i],
                     points[i + 1],
                     None,
                     speed,
                     0,
                     0))

            way.append((points[len(points) - 1],
             Math.Vector3(self.position),
             None,
             speed,
             0,
             0))
        return way

    def playFreezeEffect(self, effectData):
        if gameglobal.ENABLE_BE_HIT_FREEZE:
            freezeTime = effectData.get('freezeTime', 0.0)
            if freezeTime:
                p = BigWorld.player()
                if not p.inMoving():
                    if getattr(BigWorld.player().model, 'freezeTime', 0) <= 0:
                        BigWorld.player().updateModelFreeze(freezeTime, gameglobal.FREEZE_TYPE_HIT)
                        BigWorld.player().model.quenchTime = 0
                        BigWorld.player().freezeEffect(freezeTime)
                if not (self.IsAvatar or self.IsMonster and getattr(self, 'monsterStrengthType', None) in gametypes.MONSTER_BOSS_TYPE):
                    if getattr(self, 'life', gametypes.LIFE_ALIVE) == gametypes.LIFE_DEAD:
                        return
                    self.behitFreeze = (time.time() + freezeTime, freezeTime)

    def freezeEffect(self, freezeTime):
        try:
            self.skillPlayer.freezeEffect(freezeTime)
            if self.clientStateEffect:
                self.clientStateEffect.freezeEffect(freezeTime)
            if self.fashion:
                self.fashion.freezeEffect(freezeTime)
            for attachment in self.model.root.attachments:
                if attachment.__class__.__name__ == 'MetaParticleSystem':
                    attachment.pause(freezeTime)
                    self.freezedEffs.append(attachment)

            freezeEffectNodes = SYSCD.data.get('freezeEffectNodes', ())
            if freezeEffectNodes:
                for nodeName in freezeEffectNodes:
                    node = self.model.node(nodeName)
                    if node:
                        for attachment in self.model.node(nodeName).attachments:
                            if attachment.__class__.__name__ == 'MetaParticleSystem':
                                attachment.pause(freezeTime)
                                self.freezedEffs.append(attachment)

            if self.modelServer:
                self.modelServer.freezeEffect(freezeTime)
        except Exception as e:
            gamelog.debug('----m.l@iCombatUnit.freezeEffect', e.message)

    def clearFreezeEffect(self):
        try:
            if self.freezedEffs:
                for eff in self.freezedEffs:
                    if eff:
                        eff.pause(0)

            self.freezedEffs = []
            self.skillPlayer.clearFreezeEffect()
            self.fashion.clearFreezeEffect()
            if self.clientStateEffect:
                self.clientStateEffect.clearFreezeEffect()
            if self.modelServer:
                self.modelServer.clearFreezeEffect()
        except Exception as e:
            gamelog.debug('----m.l@iCombatUnit.clearFreezeEffect', e.message)

    def _hideTeamMateInDying(self, host):
        p = BigWorld.player()
        if host and host.id != p.id and p.isInMyTeam(host) and p.hasInDyingAround():
            gamelog.debug('----inDying hide team member behit', host.id, p.isInMyTeam(host))
            return True
        return False

    def _playCritCamShake(self, host):
        if not gameglobal.ENABLE_SHAKE_CAMERA:
            return
        if host and host.id != BigWorld.player().id:
            return
        cam = gameglobal.rds.cam.cc
        x = y = z = gameglobal.CRIT_CAM_SHAKE_STR
        cam.shake(0.15, (x, y, z))

    def disturbSkillDamage(self, beAttackNum, host, resultSet, skillInfo, clientSkillInfo, needSplitDamage = True, extInfo = {}, needHitEff = True, strHitNodeName = None):
        if resultSet and resultSet.kill:
            needSplitDamage = False
        if beAttackNum > 1 and (not gameglobal.ENABLE_PLAYER_HIT_EFFECT or not gameglobal.ENABLE_BE_HIT_FREEZE):
            disturb = random.uniform(0, 0.1)
            BigWorld.callback(disturb, Functor(self.skillDamage, host, resultSet, skillInfo, clientSkillInfo, needSplitDamage, extInfo, needHitEff, strHitNodeName))
        else:
            self.skillDamage(host, resultSet, skillInfo, clientSkillInfo, needSplitDamage, extInfo, needHitEff, strHitNodeName)

    def _isEffectShowing(self, effectId):
        lastHitEffTime = self.hitEffTimestamp.get(effectId, 0)
        if lastHitEffTime:
            if time.time() - lastHitEffTime <= HIT_EFFECT_DURATION:
                return True
            else:
                return False
        else:
            return False

    def _isHitMaterialSoundCanPlay(self, soundPath):
        lastHitSoundTime = self.hitSoundTimestamp.get(soundPath, 0)
        nowTime = time.time()
        canPlay = True
        if lastHitSoundTime:
            if nowTime - lastHitSoundTime <= HIT_HITSOUND_DURATION:
                canPlay = False
            else:
                self.hitSoundTimestamp[soundPath] = nowTime
        else:
            self.hitSoundTimestamp[soundPath] = nowTime
        if len(self.hitSoundTimestamp) > HIT_HITSOUND_COUNT:
            self.hitSoundTimestamp.clear()
        return canPlay

    def _isHitConfigSoundCanPlay(self, hitRate):
        nowTime = time.time()
        canPlay = False
        if nowTime - self.hitConfigSoundTimestamp >= HIT_CONFIG_SOUND_DURATION and random.random() <= hitRate:
            self.hitConfigSoundTimestamp = nowTime
            canPlay = True
        return canPlay

    def skillEffect(self, skillInfo, clientSkillInfo, host, dmtype, isDmg, isHeal, strHitNodeName = None):
        if strHitNodeName:
            strHitNode = strHitNodeName
        else:
            hitType = self.getbeHitType(host, dmtype)
            strHitNode = gameglobal.HIT_NODE_MAP[hitType]
        effectId = self.getSkillHitEffect(skillInfo, clientSkillInfo, host, isDmg, isHeal)
        if effectId:
            self.playHitEffect(host, effectId, strHitNode)

    def playHitEffect(self, host, fxs, strHitNode = None):
        if fxs:
            for fx in fxs:
                isEffectShowing = self._isEffectShowing(fx)
                if not isEffectShowing:
                    self.hitEffTimestamp[fx] = time.time()
                    effectLv = self.getBeHitEffectLv()
                    priority = self.getBeHitEffectPriority(host)
                    if host and host.inWorld:
                        effectLv = host.getBeHitEffectLv()
                        priority = host.getBeHitEffectPriority(host)
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_ONHIT, (effectLv,
                     priority,
                     self.model,
                     strHitNode,
                     fx,
                     host,
                     sfx.EFFECT_LIMIT,
                     gameglobal.EFFECT_LAST_TIME))

    def getSkillHitEffect(self, skillInfo, clientSkillInfo, host, isDmg, isHeal):
        fixedHitEff = self.getStateFixHitEffect(isDmg, isHeal)
        if fixedHitEff:
            return fixedHitEff
        else:
            stateNo = self.skillPlayer.getActEffectByHostState(host, clientSkillInfo)
            effectId = skillDataInfo.getSkillEffects(clientSkillInfo, gameglobal.S_HIT, stateNo, isHeal)
            return effectId

    def getStateFixHitEffect(self, isDmg = False, isHeal = False):
        fixedHitEff = None
        for stateId in self.getStates():
            scd = SCD.data.get(stateId, {})
            fhe = scd.get('fixedHitEff', None)
            if fhe:
                if fhe[0] == gametypes.BUFF_FIX_EFF_TYPE_ALL:
                    fixedHitEff = fhe[1]
                elif fhe[0] == gametypes.BUFF_FIX_EFF_TYPE_DMG and isDmg:
                    fixedHitEff = fhe[1]
                elif fhe[0] == gametypes.BUFF_FIX_EFF_TYPE_HEAL and isHeal:
                    fixedHitEff = fhe[1]

        return fixedHitEff

    def showCalcScopeDebug(self, args):
        if BigWorld.isPublishedVersion():
            return
        if not gametypes.ENABLE_CALC_SCOPCE_DEBUG:
            return
        if gametypes.CALC_SCOPCE_LIMIT_IDS:
            if self.id not in gametypes.CALC_SCOPCE_LIMIT_IDS:
                return
        if args:
            shapeType = args[0]
            if shapeType == gametypes.CALC_SCOPCE_TYPE_SPHERE:
                centerPos = args[1]
                radii = args[2]
                clientcom.drawCylinderDebug(centerPos, radii, radii, radii, 0.3)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_CYLINDER:
                centerPos = args[1]
                radii = args[2]
                height = args[3]
                depth = args[4]
                clientcom.drawCylinderDebug(centerPos, radii, height, depth, 0.3)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_CUBE:
                srcPosition = args[1]
                centerPos = args[2]
                width = args[3]
                depth = args[4]
                height = args[5]
                yaw = args[6]
                if not centerPos:
                    centerPos = srcPosition
                clientcom.drawCubeDebug(centerPos, width, depth, height, yaw, 0.5)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_RADIAN:
                srcPosition = args[1]
                centerPos = args[2]
                radii = args[3]
                radian = args[4]
                height = args[5]
                yaw = args[6]
                if not centerPos:
                    centerPos = srcPosition
                clientcom.drawRadianDebug(centerPos, radii, radian, height, yaw, 0.5)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_RING:
                centerPos = args[1]
                innerRadius = args[2]
                outerRadius = args[3]
                height = args[4]
                clientcom.drawRingDebug(centerPos, innerRadius, outerRadius, height, 0.5)

    def showScopeViewDebug(self, viewType, args):
        if BigWorld.isPublishedVersion():
            return
        if not utils.needShowScopeDebug(self, viewType):
            return
        if args:
            shapeType = args[0]
            if shapeType == gametypes.CALC_SCOPCE_TYPE_SPHERE:
                centerPos = args[1]
                radii = args[2]
                delay = args[3] if len(args) >= 4 else 0.3
                color = args[4] if len(args) >= 5 else None
                clientcom.drawCylinderDebug(centerPos, radii, radii, radii, delay, color)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_CYLINDER:
                centerPos = args[1]
                radii = args[2]
                height = args[3]
                depth = args[4]
                delay = args[5] if len(args) >= 6 else 0.3
                color = args[6] if len(args) >= 7 else None
                clientcom.drawCylinderDebug(centerPos, radii, height, depth, delay, color)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_CUBE:
                srcPosition = args[1]
                centerPos = args[2]
                width = args[3]
                depth = args[4]
                height = args[5]
                yaw = args[6]
                delay = args[7] if len(args) >= 8 else 0.5
                color = args[8] if len(args) >= 9 else None
                if not centerPos:
                    centerPos = srcPosition
                if viewType == gametypes.SCOPCE_TYPE_CALC_DEBUG:
                    clientcom.drawCubeDebug(centerPos, width, depth, height, yaw)
                else:
                    clientcom.drawCubeViewDebug(centerPos, width, depth, height, yaw, delay, color)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_RADIAN:
                srcPosition = args[1]
                centerPos = args[2]
                radii = args[3]
                radian = args[4]
                height = args[5]
                yaw = args[6]
                delay = args[7] if len(args) >= 8 else 0.5
                color = args[8] if len(args) >= 9 else None
                if not centerPos:
                    centerPos = srcPosition
                clientcom.drawRadianDebug(centerPos, radii, radian, height, yaw, delay, color)
            elif shapeType == gametypes.CALC_SCOPCE_TYPE_RING:
                centerPos = args[1]
                innerRadius = args[2]
                outerRadius = args[3]
                height = args[4]
                delay = args[5] if len(args) >= 6 else 0.5
                innterColor = args[6] if len(args) >= 7 else (0, 0, 255, 0)
                outerColor = args[7] if len(args) >= 8 else None
                clientcom.drawRingDebug(centerPos, innerRadius, outerRadius, height, delay, innterColor, outerColor)

    def playSkillIndicateEff(self, clientSkillInfo):
        skillIndicateEff = clientSkillInfo.getSkillData('skillIndicateEff', 0)
        if skillIndicateEff:
            skillIndicateEffScale = clientSkillInfo.getSkillData('skillIndicateEffScale', 1)
            effs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             skillIndicateEff,
             sfx.EFFECT_LIMIT,
             gameglobal.EFFECT_LAST_TIME))
            if effs:
                for eff in effs:
                    if eff:
                        eff.scale(skillIndicateEffScale)

    def skillResult(self, sr):
        if not self._resultCheck():
            return
        self.resetClientYawMinDist()
        p = BigWorld.player()
        self.spellInfo = None
        if not sr.skillId:
            return
        target = None
        clientSkillInfo = self.getClientSkillInfo(sr.skillId, sr.skillLv)
        p = BigWorld.player()
        for i in sr.resultSet:
            target = BigWorld.entity(i.eid)
            if target and i.kill and target.firstFetchFinished:
                DYING_DELAY_LIST.add(target)
            if target:
                target.skillPlayer.playBeCastedEffect(sr.skillId, sr.skillLv, clientSkillInfo, False)
            if self.id == p.groupHeader:
                if not hasattr(p, 'groupHeaderTargets'):
                    p.groupHeaderTargets = []
                if i.eid not in p.groupHeaderTargets:
                    p.groupHeaderTargets.append(i.eid)
                if len(p.groupHeaderTargets) > const.GROUP_HEADER_TARGET_CACHE_LIMIT:
                    p.groupHeaderTargets.pop(0)

        skillInfo = self.getSkillInfo(sr.skillId, sr.skillLv)
        if skillInfo.getSkillData('spellTime', 0) > 0 or skillInfo.getSkillData('castType', gametypes.SKILL_FIRE_NORMAL) == gametypes.SKILL_FIRE_CHARGE:
            if len(sr.resultSet) == 1:
                combatMsg.useSkill(self, target, sr.skillId, sr.skillLv)
            else:
                combatMsg.useSkillPos(self, sr.skillId, sr.skillLv)
        self.nepLogKillMoster(sr.resultSet)
        if self == p and not sr.resultSet:
            self.playSkillIndicateEff(clientSkillInfo)
        preCast = skillInfo.getSkillData('preCast', 0)
        target = BigWorld.entity(sr.tgtId)
        if target and sr.tgtId != self.id:
            beCastedEffect = skillDataInfo.getBeCastedEffect(clientSkillInfo)
            if beCastedEffect and beCastedEffect[0] == gameglobal.BE_CAST_EFFECT_RESULT_ONLY_TARGET:
                target.skillPlayer.playBeCastedEffect(sr.skillId, sr.skillLv, clientSkillInfo, False, sr.tgtId)
        if preCast:
            if self == p:
                gamelog.debug('iCombatUnit#self == p', sr)
                if not self.skillPlayer.processMoveDamage(skillInfo, clientSkillInfo, sr.resultSet, False):
                    self.skillPlayer.processDelayDamageAll(skillInfo, clientSkillInfo, sr.resultSet)
            else:
                self.skillPlayer.castSkill(sr.tgtId, sr.skillId, sr.skillLv, sr.resultSet, sr.isInstantSkill, sr.playAction, guideCastTime=sr.guideCastTime)
        elif sr.playAction:
            if sr.targetPos:
                self.skillPlayer.targetPos = Math.Vector3(sr.targetPos[0], sr.targetPos[1], sr.targetPos[2])
            else:
                self.skillPlayer.targetPos = None
            self.skillAlert(sr.tgtId, sr.skillId, sr.skillLv, sr.targetPos, gameglobal.S_CAST)
            fenshenInfo = self.parseFenshenInfoFromResultSet(sr.resultSet)
            self.updateFenshenInfoWithAppearance(sr.skillId, fenshenInfo)
            self.skillPlayer.processFenShenDamage(fenshenInfo)
            self.skillPlayer.castSkill(sr.tgtId, sr.skillId, sr.skillLv, sr.resultSet, sr.isInstantSkill, sr.playAction, guideCastTime=sr.guideCastTime)
            if self == p:
                self.skillPlayer.updateSkillState(skillInfo, sr.skillCD, sr.skillGCD, sr.isInstantSkill)
        else:
            fenshenInfo = self.parseFenshenInfoFromResultSet(sr.resultSet)
            self.updateFenshenInfoWithAppearance(sr.skillId, fenshenInfo)
            self.skillPlayer.processFenShenDamage(fenshenInfo)
            if not self.skillPlayer.processMoveDamage(skillInfo, clientSkillInfo, sr.resultSet, sr.playAction):
                self.skillPlayer.processDelayDamageAll(skillInfo, clientSkillInfo, sr.resultSet)
            if self == p and self.skillPlayer.hasRestorableDelayCd(self, skillInfo, True):
                self.skillPlayer.updateSkillState(skillInfo, sr.skillCD, sr.skillGCD, sr.isInstantSkill)

    def updateFenshenInfoWithAppearance(self, skillId, fenshenInfo):
        if not fenshenInfo:
            return
        if hasattr(self, 'skillAppearancesDetail'):
            appId = self.skillAppearancesDetail.getCurrentAppearance(skillId)
            if appId != -1:
                fenshenIds = SFAD.data.get((skillId, appId), {}).get('fenshenID', ())
                for i, info in enumerate(fenshenInfo):
                    if i < len(fenshenIds):
                        info[0] = fenshenIds[i]

    def parseFenshenInfoFromResultSet(self, resultSet):
        fenshenInfo = []
        if len(resultSet) <= 0:
            return []
        fenshenValEffects = []
        for resultSet in resultSet:
            fenshenValEffects = resultSet.fenshenVal
            if len(fenshenValEffects) > 0:
                break

        size = len(fenshenValEffects) / 4
        for i in xrange(0, size):
            fenshenId = fenshenValEffects[i * 4]
            fenshenPosition = fenshenValEffects[i * 4 + 1]
            targetPosition = fenshenValEffects[i * 4 + 2]
            targetYaw = fenshenValEffects[i * 4 + 3]
            fenshenInfo.append([fenshenId,
             fenshenPosition,
             targetPosition,
             targetYaw])

        return fenshenInfo

    def _processSkillFlagState(self, skillResult):
        for rr in skillResult.resultSet:
            if not rr.addFlagStates and not rr.dispellFlagStates:
                continue
            if self.id != rr.eid:
                continue
            for flagStateId in rr.dispellFlagStates:
                self.skillFlagState.removeFlagState(self, flagStateId)

            for flagStateId, lastTime in rr.addFlagStates:
                self.skillFlagState.markFlagState(self, flagStateId, lastTime)

    def getStates(self):
        if BigWorld.player().id == self.id and hasattr(self, 'statesServerAndOwn'):
            return self.statesServerAndOwn
        if hasattr(self, 'statesClientPub'):
            return self.statesClientPub
        return {}

    def skillResultPB(self, bytes):
        if not self.isRealModel:
            return
        if not self.needPlaySkill():
            return
        skillResult = combatProto.skillResultProtoClient(bytes)
        if skillResult is None:
            return
        deadPlayBack.getInstance().receiveCombatResult(skillResult)
        self._processSkillFlagState(skillResult)
        gamelog.debug('skillResultPB:', self.id, skillResult)
        if skillResult.targetPos:
            self.skillResultPos(skillResult)
        else:
            self.skillResult(skillResult)
        self.showControlState(skillResult)

    def pskillResultPB(self, bytes):
        if not self.isRealModel:
            return
        if not self.needPlaySkill():
            return
        pskillNum, pskillLv, pskillResult = combatProto.PSkillResultProtoClient(bytes)
        for resultSet in pskillResult:
            host = None
            beAttack = BigWorld.entity(resultSet.eid)
            if not beAttack or not beAttack.inWorld:
                return
            for pair in resultSet.results:
                host = BigWorld.entity(pair.srcId)
                if pair.comboNum > 0:
                    beAttack.comboDamage(host, pair)
                else:
                    beAttack.damage(host, pair.dmgs, pair.damageAbsorb, pair.mps, pair.ars)
                if pair.hps:
                    beAttack.damage(host, (pair.hps,), [], pair.mps, gametypes.UI_BE_HEAL)
                beAttack.beHit(host, (sum(pair.dmgs), pair.ars))

            if resultSet.kill:
                beAttack.die(host)
                if host:
                    host.afterDieEffect(beAttack)

        self.nepLogKillMoster(pskillResult)

    def fenshenResultPB(self, bytes):
        fenshenId, fenshenResult, skillId, skillLv = combatProto.fenshenResultProtoClient(bytes)
        print 'jorsef: fenshenResultPB', fenshenId, fenshenResult, skillId, skillLv

    def stateEffectResultPB(self, bytes):
        if not self.isRealModel:
            return
        if not self.needPlaySkill():
            return
        skillResult = combatProto.skillResultProtoClient(bytes)
        if skillResult is None:
            return
        deadPlayBack.getInstance().receiveCombatResult(skillResult)
        for resultSet in skillResult.resultSet:
            beAttack = BigWorld.entity(resultSet.eid)
            if not beAttack or not beAttack.inWorld:
                continue
            host = None
            for pair in resultSet.results:
                host = BigWorld.entity(pair.srcId)
                if pair.comboNum > 0:
                    beAttack.comboDamage(host, pair)
                else:
                    beAttack.damage(host, pair.dmgs, pair.damageAbsorb, pair.mps, pair.ars)
                if pair.hps:
                    beAttack.damage(host, (pair.hps,), [], pair.mps, gametypes.UI_BE_HEAL)
                beAttack.beHit(host, (sum(pair.dmgs), pair.ars))

            if resultSet.kill:
                beAttack.die(host)
                if host:
                    host.afterDieEffect(beAttack)

        self.nepLogKillMoster(skillResult.resultSet)

    def showControlState(self, skillResult):
        controlSet = set([gametypes.SKILL_STATE_UNCONTROLLABLE,
         gametypes.SKILL_STATE_NOT_SPELLABLE,
         gametypes.SKILL_STATE_UNMOVEABLE,
         gametypes.SKILL_STATE_RED_SUM_MOVE_SPEED,
         gametypes.SKILL_STATE_RED_MAX_MOVE_SPEED])
        for r in skillResult.resultSet:
            target = BigWorld.entity(r.eid)
            allAttrIds = set()
            for controllStateId, controllStateHit in r.controllStateData:
                if controllStateId == const.ANTI_MOVE_STATE_ID:
                    allAttrIds.add(gametypes.SKILL_STATE_UNCONTROLLABLE)
                    continue
                if controllStateHit or controllStateId == 0:
                    continue
                allAttrIds = allAttrIds.union(set(SD.data.get(controllStateId, {}).get('allAttrIds', [])))

            showId = allAttrIds.intersection(controlSet)
            for typeId in showId:
                if target:
                    target.bloodLabel(0, typeId)

    def comboDamage(self, host, result):
        isSpriteHost = True if host and host.IsSummonedSprite or self.IsSummonedSprite else False
        comboNum = result.comboNum
        if isSpriteHost:
            self.showSpriteComboDamageLabel(host, result)
        else:
            dmgs = [sum(result.dmgs) - result.comboDmg * comboNum]
            self.damage(host, dmgs, result.damageAbsorb, result.mps, result.ars)
        if comboNum <= 0:
            return
        spriteId = getattr(host, 'spriteId', -1)
        comboEffs = SSPD.data.get(spriteId, {}).get('comboEffs', [])
        effs = random.sample(comboEffs, min(comboNum, 2, len(comboEffs))) if comboEffs else []
        comboHitTime = SYSCD.data.get('spriteComboHitTime', 0.2)
        if host and host.inWorld:
            for i in xrange(comboNum):
                delay = comboHitTime + comboHitTime * i / comboNum
                if i < 2 and i < len(effs):
                    ef = effs[i]
                    if ef:
                        delay = comboHitTime + i
                        BigWorld.callback(delay, Functor(sfx.attachEffect, gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                         self.getBasicEffectPriority(),
                         host.model,
                         ef,
                         sfx.EFFECT_UNLIMIT)))

    def processDamageResultWithoutSkillId(self, results, mfType):
        for resultSet in results:
            beAttack = BigWorld.entity(resultSet.eid)
            host = None
            for pair in resultSet.results:
                host = BigWorld.entity(pair.srcId)
                if pair.comboNum > 0:
                    beAttack.comboDamage(host, pair)
                else:
                    beAttack.damage(host, pair.dmgs, pair.damageAbsorb, pair.mps, pair.ars)
                if pair.hps:
                    beAttack.damage(host, (pair.hps,), [], pair.mps, gametypes.UI_BE_HEAL)
                beAttack.beHit(host, (sum(pair.dmgs), pair.ars))

            if resultSet.kill:
                beAttack.die(host)
                if host:
                    host.afterDieEffect(beAttack)
            isDmg, isHeal = attackEffect.getDmgHeal(resultSet)
            if hasattr(self, 'skillAppearancesDetail'):
                creationData = self.skillAppearancesDetail.getCreationAppearanceData(mfType)
            else:
                creationData = CD.data.get(mfType, {})
            attacker = host if host else self
            if isDmg:
                triggerHitEffect = creationData.get('triggerHitEffect', None)
                attackEffect.playTriggerHitEffect(beAttack, attacker, triggerHitEffect)
            elif isHeal:
                triggerHitEffect = creationData.get('triggerHitHealEffect', None)
                attackEffect.playTriggerHitEffect(beAttack, attacker, triggerHitEffect)
            if gameglobal.ENABLE_PLAYER_HIT_EFFECT:
                effectData = self.getPlayerHitEffDataByCreation(creationData, resultSet)
                if effectData and (host and host == BigWorld.player() or self == BigWorld.player()):
                    hitEffectDelay = effectData.get('hitEffectDelay', 0)
                    if hitEffectDelay:
                        BigWorld.callback(hitEffectDelay, Functor(self.playAllHitEffect, effectData))
                    else:
                        self.playAllHitEffect(effectData)

        self.nepLogKillMoster(results)

    def getPlayerHitEffDataByCreation(self, creationData, resultSet):
        isCrit = utils.isResultCrit(resultSet)
        if isCrit:
            playerHitEffect = creationData.get('playerCritHitEff', 0)
        else:
            playerHitEffect = creationData.get('playerHitEff', 0)
        return self.getHitEffectData(playerHitEffect)

    def mfResultPB(self, bytes):
        if not self.isRealModel:
            return
        if not self.needPlaySkill():
            return
        try:
            self.mfResult(*combatProto.mfResultProtoClient(bytes))
        except:
            pass

    def mfResult(self, mfId, mfType, lv, results, srcSkillId, srcSkillLv, rPosList):
        deadPlayBack.getInstance().takeResult(0, srcSkillId, srcSkillLv, results, None, mfId, mfType, lv)
        if not self._resultCheck() and not self.skillPlayer.isSkillResultMove(results):
            return
        self.resetClientYawMinDist()
        if srcSkillId <= 0:
            self.processDamageResultWithoutSkillId(results, mfType)
            return
        skillInfo = self.getSkillInfo(srcSkillId, srcSkillLv)
        clientSkillInfo = self.getClientSkillInfo(srcSkillId, srcSkillLv)
        p = BigWorld.player()
        for resultSet in results:
            if resultSet.kill:
                target = BigWorld.entity(resultSet.eid)
                if target and target.firstFetchFinished:
                    DYING_DELAY_LIST.add(target)
            if resultSet.eid != self.id and resultSet.eid == p.id and resultSet.results:
                self.attackAndLockTarget(resultSet.eid)
                break

        if self == p:
            if self.skillPlayer.stateKit != -1:
                self.mfStateKit = srcSkillId * 10 + self.skillPlayer.stateKit
            elif self.mfStateKit / 10 != srcSkillId:
                self.mfStateKit = -1
        if not self.skillPlayer.mfProcessMoveDamage(skillInfo, clientSkillInfo, results):
            attackEffect.magicFieldHurt(self, mfId, mfType, lv, results, skillInfo, clientSkillInfo)
        self.nepLogKillMoster(results)

    def guideSkillResultPB(self, bytes):
        if not self.isRealModel:
            return
        targetId, guideSkillNo, lv, results, targetPos = combatProto.guideSkillResultProtoClient(bytes)
        if not self.needPlaySkill(skillId=guideSkillNo, skillLv=lv):
            return
        deadPlayBack.getInstance().takeResult(targetId, guideSkillNo, lv, results, targetPos)
        try:
            if targetPos:
                self.guideSkillResultPosition(targetId, guideSkillNo, lv, results, targetPos)
            else:
                self.guideSkillResult(targetId, guideSkillNo, lv, results)
        except DecodeError:
            pass

    def pskillTriggered(self, pskillId):
        pSkillData = PSCD.data.get(pskillId, {})
        triggerEff = pSkillData.get('triggerEff', None)
        if triggerEff:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             self.model,
             triggerEff,
             sfx.EFFECT_LIMIT,
             gameglobal.EFFECT_LAST_TIME))

    def guideSkillResultPosition(self, targetId, guideSkillId, lv, results, targetPos):
        self.guideSkillResult(targetId, guideSkillId, lv, results, targetPos)

    def nepLogKillMoster(self, results):
        if self.id != BigWorld.player().id:
            return
        if not results:
            return
        numDict = {}
        try:
            for resultSet in results:
                if resultSet and getattr(resultSet, 'kill', False):
                    eid = getattr(resultSet, 'eid', 0)
                    numDict[eid] = numDict.get(eid, 0) + 1

            if numDict:
                for k, v in numDict.iteritems():
                    protect.nepActionRoleActivity(protect.eNEActivity_KMonster, 0, k, v)

        except:
            pass

    def guideSkillResult(self, targetId, guideSkillId, lv, results, targetPos = None):
        if not self._resultCheck():
            return
        self.resetClientYawMinDist()
        skillInfo = self.getSkillInfo(guideSkillId, lv)
        clientSkillInfo = self.getClientSkillInfo(guideSkillId, lv)
        guideType = skillDataInfo.getGuideType(clientSkillInfo)
        self.skillPlayer.targetPos = targetPos
        if guideType == gameglobal.GUIDE_FLYER:
            self.skillPlayer.processGuideFlyerDamage(skillInfo, clientSkillInfo, results, targetId)
        elif not self.skillPlayer.processMoveDamage(skillInfo, clientSkillInfo, results):
            showHitEffIndexes = self.skillPlayer._getShowHitEffIndexes(clientSkillInfo, results)
            beAttackNum = len(results)
            for idx, resultSet in enumerate(results):
                target = BigWorld.entity(resultSet.eid)
                if target:
                    if resultSet.kill and target.firstFetchFinished:
                        DYING_DELAY_LIST.add(target)
                    needHit = self.skillPlayer._isShowHitEff(showHitEffIndexes, idx)
                    needShake = utils.isResultCrit(resultSet)
                    extInfo = {gameglobal.CRIT_CAM_SHAKE: needShake}
                    target.disturbSkillDamage(beAttackNum, self, resultSet, skillInfo, clientSkillInfo, True, extInfo, needHit, None)

        self.nepLogKillMoster(results)

    def set_hidingPower(self, old):
        self.resetHiding()

    def set_antiHidingPower(self, old):
        self.resetHiding()

    def manDownUpAction(self):
        manDownStartAction = self.fashion.action.getManDownStartAction(self.fashion)
        manDownStopAction = self.fashion.action.getManDownStopAction(self.fashion)
        self.fashion.playAction([manDownStartAction, manDownStopAction], action.MAN_DOWN_START_ACTION, self.overManDownUpAction, trigger=0)

    def doManDownUpAction(self):
        return self.fashion.doingActionType() == action.MAN_DOWN_START_ACTION

    def overManDownUpAction(self):
        if self == BigWorld.player():
            self.fashion.setDoingActionType(action.MAN_DOWN_STOP_ACTION)
            self.updateActionKeyState()

    def inHiding(self):
        return getattr(self, 'hidingPower', 0) > 0

    def resetHiding(self, refreshAttachOnly = False):
        if not self.inWorld:
            return
        self.clearFade()
        if self.revealCallback:
            BigWorld.cancelCallback(self.revealCallback)
        if self.revealFadeCallback:
            BigWorld.cancelCallback(self.revealFadeCallback)
        if self.hidingPowerCallback:
            BigWorld.cancelCallback(self.hidingPowerCallback)
        p = BigWorld.player()
        if self.hidingPower:
            if self == BigWorld.player() or self == BigWorld.player().summonedSpriteInWorld:
                self.refreshOpacityState()
                self.addHideTint(refreshAttachOnly=refreshAttachOnly)
            else:
                inBattleTeam = False
                ent = BigWorld.entities.get(self.ownerId, self) if self.IsSummonedSprite else self
                gbId = getattr(ent, 'gbId', 0)
                if BigWorld.player().inFubenTypes(const.FB_TYPE_BATTLE_FIELD) and BigWorld.player().battleFieldTeam and gbId in BigWorld.player().battleFieldTeam:
                    inBattleTeam = True
                inArenaTeam = False
                if hasattr(p, 'arenaTeam') and p.arenaTeam:
                    sideNUID = getattr(p, 'sideNUID', None)
                    if sideNUID and p.arenaTeam.get(gbId, {}).get('sideNUID', None) == sideNUID:
                        inArenaTeam = True
                if p.isFriend(ent) and (p.isInMyTeam(ent) or inBattleTeam or self.IsMonster or inArenaTeam):
                    if gameglobal.gHideOtherPlayerFlag != gameglobal.HIDE_ALL_PLAYER:
                        self.refreshOpacityState()
                        self.addHideTint(refreshAttachOnly=refreshAttachOnly)
                else:
                    self.addHideTint()
                    self.hidePower()
                    if self.model:
                        self.model.setFilterType('metaparticlesystem')
        else:
            self.model.bkgLoadTint = True
            self.delHideTint()
            self.fadeToReal(1)
            BigWorld.player().hidePlayerNearby(gameglobal.gHideOtherPlayerFlag)
            self.refreshOpacityState()
            if self.model:
                self.model.setFilterType('')

    def playRevealSound(self):
        soundId = SYSCD.data.get('revealSoundId', None)
        if soundId:
            gameglobal.rds.sound.playSound(soundId)

    def hidePower(self):
        if not self.inWorld:
            return
        if not self.hidingPower:
            self.refreshOpacityState()
            return
        rate = self.calcHideRate()
        hidingFadeTime = SYSCD.data.get('hidingFadeTime', gameglobal.HIDING_FADE_TIME)
        duration = SYSCD.data.get('hidingTime', gameglobal.HIDING_TIME)
        self.inHidingReveal = False
        if random.randint(0, 100) < rate:
            self.inHidingReveal = True
            self.fadeToReal(hidingFadeTime)
            self.hide(False)
            self.playRevealSound()
            if rate < 100:
                self.revealCallback = BigWorld.callback(duration, self.resumeHide)
            fadeTime = duration - hidingFadeTime if duration - hidingFadeTime > 0 else 0
            if fadeTime:
                self.revealFadeCallback = BigWorld.callback(fadeTime, Functor(self.hideRealToFade, hidingFadeTime))
        else:
            self.refreshOpacityState()
        self.hidingPowerCallback = BigWorld.callback(SYSCD.data.get('hidingPowerInterval', gameglobal.HIDING_POWER_INTERVAL), self.hidePower)

    def hideRealToFade(self, fadeTime):
        if not self.inWorld:
            return
        if not self.hidingPower:
            self.refreshOpacityState()
            return
        self.realToFade(fadeTime)

    def resumeHide(self):
        if not self.inWorld:
            return
        if not self.hidingPower:
            self.refreshOpacityState()
            return
        self.inHidingReveal = False
        self.hide(True)

    def addHideTint(self, refreshAttachOnly = False):
        if not self.model:
            return
        if getattr(self.model, 'dummyModel', False):
            return
        weaponModels = self.modelServer.getAllWeaponModels()
        attachedModels = self.modelServer.getAllAttachedModels()
        models = []
        if refreshAttachOnly:
            if weaponModels:
                models = models + weaponModels + attachedModels
        else:
            models = self.allModels
            if weaponModels:
                models = self.allModels + weaponModels + attachedModels
        if getattr(self, 'faceEmoteXmlInfo', {}).get('faceTexName', None):
            tintalt.ta_del(models, 'emotionHead%s' % self.realPhysique.sex, 'head')
        self.addTint(gameglobal.HIDE_REVEAL_TINT, models, force=True, host=self)

    def delHideTint(self):
        tintName, tintPrio, tint = skillDataInfo.getTintDataInfo(self, gameglobal.HIDE_REVEAL_TINT)
        tintalt.ta_del(self.allModels, tintName)
        if self.modelServer:
            weaponModels = self.modelServer.getAllWeaponModels()
            attachedModels = self.modelServer.getAllAttachedModels()
            models = weaponModels + attachedModels
            if weaponModels:
                tintalt.ta_del(models, tintName)
        if hasattr(self, 'tintStateType') and self.tintStateType[0] <= tintPrio:
            self.restoreTintStateType()

    def calcHideRate(self):
        p = BigWorld.player()
        antiHidingPower = p.antiHidingPower
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA):
            if self.IsAvatar:
                if self.vehicleId and p.vehicleId and self.vehicleId != p.vehicleId:
                    return -1
                if p.vehicleId and not self.vehicleId:
                    antiHidingPower = 0
        dist = (p.position - self.position).length
        lv = BigWorld.entities.get(self.ownerId, self).lv if self.IsSummonedSprite else self.lv
        rate = 40 - dist - 8 * self.hidingPower + 8 * int((lv + 3) / 4) + 2 * antiHidingPower
        return rate

    def afterReliveAction(self):
        pass

    def attachReliveEffect(self):
        pass

    def _getSummonActionName(self):
        return self.fashion.getSummonActionName()

    def set_life(self, old):
        self.updateBodySlope()
        p = BigWorld.player()
        self.resetTopLogo()
        if self.life == gametypes.LIFE_ALIVE:
            self.fashion.attachUFO(ufo.UFO_SHADOW)
            if hasattr(p, 'targetLocked') and self == p.targetLocked:
                self.fashion.attachUFO(ufo.UFO_SHADOW)
            if self.model != None and len(self.model.motors) > 0:
                self.model.motors[0].matcherCoupled = True
            if old == gametypes.LIFE_DEAD:
                self.skillPlayer.castLoop = False
                SummonActionName = self._getSummonActionName()
                if SummonActionName:
                    self.fashion.playAction([SummonActionName], action.STANDUP_ACTION, self.afterReliveAction)
                else:
                    self.fashion.stopAllActions()
                    self.afterReliveAction()
                self.attachReliveEffect()
            self.deadLabelHadShown = False
        elif self.life == gametypes.LIFE_DEAD:
            p = BigWorld.player()
            if p.targetLocked == self:
                p.unlockTarget()
            if hasattr(BigWorld.player(), 'getOperationMode') and BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
                if self == BigWorld.player().optionalTargetLocked:
                    BigWorld.player().ap.lockOptionalTarget(True)
                if self == BigWorld.player().targetLocked:
                    BigWorld.player().unlockTarget()
            if self.bodyShakeFlyer:
                self.bodyShakeFlyer.release()
            if self in DYING_DELAY_LIST:
                gamelog.debug('@zf:self in DYING_DELAY_LIST ', DYING_DELAY_LIST)
                return
            if self.fashion.doingActionType() in (action.HITFLY_ACTION, action.DYING_ACTION, action.HIT_DIEFLY_ACTION):
                return
            self.stopSpell(False)
            self.playDieAction()

    def set_inCombat(self, old):
        self.fashion.setGuard(self.inCombat)
        if self.firstFetchFinished:
            self.clientStateEffect.updateEffectInCombat(self.inCombat, set(self.getStates().keys()))
        BigWorld.player().updateTargetFocus(self)

    def set_camp(self, old):
        self.refreshRealModelState()
        self.refreshOpacityState()
        BigWorld.player().updateTargetFocus(self)

    def set_tempCamp(self, old):
        self.refreshRealModelState()
        self.refreshOpacityState()
        if hasattr(self, 'topLogo') and self.topLogo:
            self.topLogo.updateRoleName(self.topLogo.name)
        BigWorld.player().updateTargetFocus(self)

    def set_lockedId(self, old):
        gamelog.debug('@hjx target#set_lockedId111:', old, self.lockedId)
        if old == 0 and self.lockedId == 0:
            return
        if BigWorld.player().targetLocked == self:
            lockedId = getattr(self, 'lockedId', None)
            if lockedId != None:
                gameglobal.rds.ui.target.setTargetLockName(lockedId)
        if gameglobal.rds.ui.focusTarget.focusTarId == self.id:
            lockedId = getattr(self, 'lockedId', None)
            if lockedId != None:
                gameglobal.rds.ui.focusTarget.setTargetLockName(lockedId)

    def set_dmgAbsorbClient(self, old):
        if hasattr(self, 'topLogo') and self.topLogo:
            self.topLogo.onUpdateHp()

    def set_lifeLinkInfo(self, old):
        gamelog.debug('bgf@iCombatUnit set_lifeLinkInfo', self.lifeLinkInfo, old)
        lifeLinkManager.getInstance().update(self.id, self.lifeLinkInfo)

    def set_otherSkillAppearanceCache(self, old):
        gamelog.debug('ypc@ iCombatUnit set_otherSkillAppearanceCache', self.otherSkillAppearanceCache, old)

    def refreshOpacityState(self):
        if not self.inWorld:
            return
        if gameglobal.HIDE_ALL_MODELS:
            self.hide(True)
            return
        if gameglobal.rds.configData.get('enableNewCamera', False) and gameglobal.rds.ui.cameraTable.isHideFriends(getattr(self, 'gbId', 0)):
            self.hide(True)
            return
        if gameglobal.rds.configData.get('enableNewCamera', False) and gameglobal.rds.ui.cameraTable.isHideOthers(getattr(self, 'gbId', 0)):
            self.hide(True)
            return
        opValue = self.getOpacityValue()
        if opValue[0] == gameglobal.OPACITY_HIDE:
            self.hide(True, opValue[1])
        elif opValue[0] == gameglobal.OPACITY_HIDE_WITHOUT_NAME:
            self.hide(True, True)
        elif opValue[0] == gameglobal.OPACITY_TRANS:
            self.hide(False)
        elif opValue[0] == gameglobal.OPACITY_HIDE_INCLUDE_ATTACK:
            self.hide(True, opValue[1])
        else:
            self.hide(False)

    def getCUFlag(self, cu, f):
        if cu.IsCreation or cu.IsFragileObject or cu.IsObstacle:
            return False
        if f in gametypes.ALL_CLIENT_FLAG_SET:
            return commcalc.getBitDword(cu.publicFlags, f)

    def _hasHideFlag(self):
        return commcalc.getBitDword(self.publicFlags, gametypes.FLAG_HIDE)

    def getOpacityValue(self):
        opValues = super(ICombatUnit, self).getOpacityValue()
        if opValues[0] == gameglobal.OPACITY_HIDE:
            return opValues
        p = BigWorld.player()
        if self.hidingPower:
            ent = BigWorld.entities.get(self.ownerId, self) if self.IsSummonedSprite else self
            gbId = getattr(ent, 'gbId', 0)
            inBattleTeam = False
            if BigWorld.player().inFubenTypes(const.FB_TYPE_BATTLE_FIELD) and BigWorld.player().battleFieldTeam and gbId in BigWorld.player().battleFieldTeam:
                inBattleTeam = True
            inArenaTeam = False
            if hasattr(p, 'arenaTeam') and p.arenaTeam:
                sideNUID = getattr(p, 'sideNUID', None)
                if sideNUID and p.arenaTeam.get(gbId, {}).get('sideNUID', None) == sideNUID:
                    inArenaTeam = True
            if ent.id == BigWorld.player().id:
                pass
            elif p.isFriend(ent) and (p.isInMyTeam(ent) or inBattleTeam or inArenaTeam or self.IsMonster):
                if gameglobal.gHideOtherPlayerFlag != gameglobal.HIDE_ALL_PLAYER:
                    pass
            else:
                return (gameglobal.OPACITY_HIDE, False)
        if self._hasHideFlag() and self.id != p.id:
            return (gameglobal.OPACITY_HIDE, False)
        if utils.isOccupied(self) and not utils.hasOccupiedRelation(self, p):
            return (gameglobal.OPACITY_HIDE, False)
        if getattr(self, 'isBuffHideModel', False):
            return (gameglobal.OPACITY_HIDE, False)
        return (gameglobal.OPACITY_FULL, True)

    def chatToEventEx(self, msg, color):
        pass

    def showProtoRes(self, value, oneTime):
        p = BigWorld.player()
        curPlayerId = p.id
        curPlayerSpriteId = p.summonedSpriteInWorld.id if p.summonedSpriteInWorld else 0
        curPlayerWingCarrierId = p.wingWorldCarrier.carrierEntId
        for v in value:
            stateId, stateSrc, stateTgt, addHp, reduceHp, addMp, reduceMp, fromSkillId, stateLv, dmgType = v
            if addHp > 0:
                gamelog.debug('addHp')
                self.otherHeal(addHp, stateId)
                if stateTgt == curPlayerId or stateTgt == curPlayerSpriteId or stateTgt == curPlayerWingCarrierId:
                    combatMsg.singleStateCEEffect(stateSrc, stateTgt, stateId, addHp, 0, oneTime)
            if reduceHp > 0:
                gamelog.debug('reduceHp')
                self.otherDamage(reduceHp, stateId)
                combatMsg.singleStateCEEffect(stateSrc, stateTgt, stateId, -reduceHp, 0, oneTime)
            if addMp > 0:
                gamelog.debug('addMp')
                self.otherHealMp(addMp, stateId)
                if stateTgt == curPlayerId or stateTgt == curPlayerSpriteId or stateTgt == curPlayerWingCarrierId:
                    combatMsg.singleStateCEEffect(stateSrc, stateTgt, stateId, 0, addMp, oneTime)
            if reduceMp > 0:
                gamelog.debug('reduceMp')
                self.otherDamageMp(reduceMp, stateId)
                combatMsg.singleStateCEEffect(stateSrc, stateTgt, stateId, 0, -reduceMp, oneTime)
            deadPlayBack.getInstance().takeResultFromState(stateId, stateSrc, stateTgt, addHp, reduceHp, addMp, reduceMp, fromSkillId, stateLv, dmgType)

    def canNotChoose(self):
        p = BigWorld.player()
        skillInfo = BigWorld.player().getSkillInfo(p.chooseEffect.skillID, p.chooseEffect.skillLevel)
        dist = self.position.distTo(BigWorld.player().position)
        rangeMin = skillInfo.getSkillData('rangeMin', 0)
        if rangeMin and rangeMin > dist:
            return True
        rangeMax = skillInfo.getSkillData('rangeMax', 0)
        rangeMax = max(rangeMin, (rangeMax + p.skillAdd[2]) * (1 + p.skillAdd[3]))
        if rangeMax and rangeMax < dist:
            return True
        skillTargetType, skillTargetValue = p.getSkillTargetType(skillInfo)
        if skillTargetType == gametypes.SKILL_TARGET_FRIEND:
            if not p.isFriend(self):
                return True
        elif skillTargetType == gametypes.SKILL_TARGET_SELF_FRIEND:
            if not p.isFriend(self):
                return True
        if skillTargetValue != gametypes.OBJ_TYPE_DEAD_BODY and self.life == gametypes.LIFE_DEAD:
            return True
        if skillTargetValue == gametypes.OBJ_TYPE_DEAD_BODY and self.life != gametypes.LIFE_DEAD:
            return True
        return False

    def onTargetCursor(self, enter):
        gamelog.debug('jorsef: iCombatUnit#onTargetCursor', enter, self.id)
        if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE and BigWorld.player().chooseEffect.isShowingEffect:
            if enter:
                if ui.get_cursor_state() == ui.NORMAL_STATE:
                    ui.set_cursor_state(ui.CHOOSE_STATE)
                    if self.canNotChoose():
                        ui.set_cursor(cursor.choose_dis)
                    else:
                        ui.set_cursor(cursor.choose)
                    ui.lock_cursor()
            elif ui.get_cursor_state() == ui.CHOOSE_STATE:
                ui.reset_cursor()
            return
        if enter:
            relation = BigWorld.player().playerRelation(self)
            if relation == gametypes.RELATION_ENEMY:
                if ui.get_cursor_state() == ui.NORMAL_STATE:
                    ui.set_cursor_state(ui.TARGET_STATE)
                    ui.set_cursor(cursor.attack)
                    ui.lock_cursor()
                    self.cursorLock = True
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()
            self.cursorLock = False

    def startCharge(self, targetId, skillId, skillLevel):
        self.resetClientYawMinDist()
        if not self._resultCheck():
            return
        en = BigWorld.entity(targetId)
        if en != None:
            self.skillPlayer.startCharge(en, skillId, skillLevel)
        else:
            gamelog.debug('BigWorld.entity is none')

    def addRanges(self):
        if self == BigWorld.player():
            return
        useZaijuSkill = gameglobal.rds.ui.zaijuV2.widget and gameglobal.rds.ui.zaijuV2.showType in (uiConst.ZAIJU_SHOW_TYPE_ZAIJU, uiConst.ZAIJU_SHOW_TYPE_HERO)
        if useZaijuSkill:
            skillIds = gameglobal.rds.ui.zaijuV2.getTargetSkillList()
        else:
            skillIds = gameglobal.rds.ui.actionbar.getTargetSkillList()
        p = BigWorld.player()
        distSet = set()
        for skId in skillIds:
            if not useZaijuSkill and (skId == 0 or not p.getSkills().has_key(skId)):
                continue
            level = p.getSkills().get(skId).level if not useZaijuSkill else gameglobal.rds.ui.zaijuV2.getSkillLv(skId)
            skillInfo = p.getSkillInfo(skId, level)
            rangeMax = skillInfo.getSkillData('rangeMax', 0)
            rangeMax = max(0, (rangeMax + p.skillAdd[2]) * (1 + p.skillAdd[3]))
            if rangeMax:
                rangeMax += self.bodySize
                temp = round(rangeMax, 2)
                distSet.add(temp)
                self.skillRanges.setdefault(temp, []).append(skId)
            rangeMin = skillInfo.getSkillData('rangeMin', 0)
            if rangeMin != 0:
                rangeMin += self.bodySize
                temp = round(rangeMin, 2)
                distSet.add(temp)
                self.skillRanges.setdefault(temp, []).append(skId)

        innerRanges = []
        outerRanges = []
        for dist in distSet:
            innerRanges.append((dist, 'enterClientRange'))
            outerRanges.append((dist, 'leaveClientRange'))

        self.clientInnerRange = tuple(innerRanges)
        self.clientOuterRange = tuple(outerRanges)
        self.addRanged = True

    def delRanges(self):
        if self == BigWorld.player():
            return
        if not self.addRanged:
            return
        self.clientInnerRange = ()
        self.clientOuterRange = ()
        self.skillRanges.clear()
        self.addRanged = False

    def enterClientRange(self, dist):
        if not self.skillRanges.has_key(dist):
            gamelog.debug('@zs iClient.enterClientRange error', self.id, dist, self.skillRanges)
            return
        for skillId in self.skillRanges[dist]:
            gameglobal.rds.ui.actionbar.onEnterClientRangeNew(skillId, dist)
            gameglobal.rds.ui.zaijuV2.onEnterClientRangeNew(skillId, dist)

    def leaveClientRange(self, dist):
        if not self.skillRanges.has_key(dist):
            gamelog.debug('@zs iClient.leaveClientRange error', self.id, dist, self.skillRanges)
            return
        for skillId in self.skillRanges[dist]:
            gameglobal.rds.ui.actionbar.onLeaveClientRangeNew(skillId, dist)
            gameglobal.rds.ui.zaijuV2.onLeaveClientRangeNew(skillId, dist)

    def getbeHitType(self, host, damageType):
        angle = self.getTgtAngle(host)
        gamelog.debug('getbeHitType:', angle, damageType)
        if self.fashion.doingActionType() == ACT.FAINT_LOOP_ACTION:
            return gameglobal.FAINT_HIT
        if self.fashion.doingActionType() in (ACT.TIAOGAO_LOOP_ACTION,
         ACT.JIDAO_START_ACTION,
         ACT.JIDAO_LOOP_ACTION,
         ACT.FAINT_LOOP_ACTION):
            if damageType == gametypes.DMGPOWER_CRIT:
                return gameglobal.LIE_CRIT_HIT
            else:
                return gameglobal.LIE_HIT
        if damageType == gametypes.DMGPOWER_AVOID:
            return gameglobal.AVOID_HIT
        if damageType == gametypes.DMGPOWER_BLOCK:
            return gameglobal.BLOCK_HIT
        if angle >= -90.0 and angle < -30:
            if damageType == gametypes.DMGPOWER_CRIT:
                return gameglobal.FRONT_RIGHT_SHORT_CRIT
            else:
                return gameglobal.FRONT_RIGHT_SHORT
        elif angle >= -30.0 and angle < 30:
            if damageType == gametypes.DMGPOWER_CRIT:
                return gameglobal.FRONT_MID_SHORT_CRIT
            else:
                return gameglobal.FRONT_MID_SHORT
        elif angle >= 30.0 and angle < 90:
            if damageType == gametypes.DMGPOWER_CRIT:
                return gameglobal.FRONT_LEFT_SHORT_CRIT
            else:
                return gameglobal.FRONT_LEFT_SHORT
        elif angle >= 90.0 and angle < 150:
            if damageType == gametypes.DMGPOWER_CRIT:
                return gameglobal.BACK_LEFT_SHORT_CRIT
            else:
                return gameglobal.BACK_LEFT_SHORT
        elif angle >= 150.0 or angle < -150:
            if damageType == gametypes.DMGPOWER_CRIT:
                return gameglobal.BACK_MID_SHORT_CRIT
            else:
                return gameglobal.BACK_MID_SHORT
        else:
            if damageType == gametypes.DMGPOWER_CRIT:
                return gameglobal.BACK_RIGHT_SHORT_CRIT
            return gameglobal.BACK_RIGHT_SHORT
        return gameglobal.NORMAL_HIT

    def excludeStopAct(self):
        if self.fashion.doingActionType() in (ACT.CASTSTOP_ACTION,
         ACT.MOVINGSTOP_ACTION,
         ACT.AFTERMOVESTOP_ACTION,
         ACT.GUIDESTOP_ACTION):
            if hasattr(self, 'skillPlayer'):
                clientSkillInfo = ClientSkillInfo(self.skillPlayer.skillID, self.skillPlayer.skillLevel)
                return clientSkillInfo.getSkillData('excludeStopAct', 0)
        return 0

    def excludeCastAct(self):
        if self.fashion.doingActionType() in (ACT.SPELL_ACTION,
         ACT.GUIDE_ACTION,
         ACT.CAST_ACTION,
         ACT.CHARGE_ACTION,
         ACT.STARTSPELL_ACTION,
         ACT.CHARGE_START_ACTION,
         ACT.STARTPRESPELL_ACTION,
         ACT.PRESPELLING_ACTION):
            if hasattr(self, 'skillPlayer') and self.skillPlayer.skillID and self.skillPlayer.skillLevel:
                clientSkillInfo = ClientSkillInfo(self.skillPlayer.skillID, self.skillPlayer.skillLevel)
                return clientSkillInfo.getSkillData('excludeCastAct', 0)
        return 0

    def getClientSkillInfo(self, skillId, skillLv):
        return ClientSkillInfo(skillId, skillLv)

    def onFallGround(self):
        m = self.getBodyEquipMaterail()
        if not m:
            m = self.getSkinMaterial()
        terrain = BigWorld.getTerrainName(self.position)
        if not terrain:
            terrain = 'defalut'
        terrainMaterail = SYSCD.data.get('terrainMaterailDict', {}).get(terrain, 0)
        path = 'fx/bodyfall/land%d_%d' % (m, terrainMaterail)
        scale = 1
        if self.IsMonster:
            monsterShape = MMCD.data.get(self.charType, {}).get('monsterShape', 0)
            scale = SYSCD.data.get('fxScaleForMonsterTypes', {}).get(monsterShape, 1)
        gameglobal.rds.sound.playFx(path, self.position, False, self, scale)

    def _getFlag(self, key):
        if key in gametypes.ALL_CLIENT_FLAG_SET and hasattr(self, 'publicFlags'):
            return commcalc.getBitDword(self.publicFlags, key)
        elif hasattr(self, 'flags'):
            return commcalc.getBitDword(self.flags, key)
        else:
            return False

    def needSetStaticStates(self):
        return True


class IAvatarCombatUnit(ICombatUnit):

    def __init__(self):
        super(IAvatarCombatUnit, self).__init__()
        self.fly = 0
        self.floatFly = 0
        self.msFly = 0
        self.avatarInstance = True
        self.mfStateKit = -1

    def isSitting(self):
        return False

    def needPlaySkill(self, skillId = None, skillLv = None):
        pos = BigWorld.player().position
        distToPlayer = (self.position - pos).length
        spaceNo = getattr(BigWorld.player(), 'spaceNo', 0)
        mapId = formula.getMapId(spaceNo)
        needPlaySkillDist = MCD.data.get(mapId, {}).get('needPlaySkillDist', gameglobal.PLAYSKILL_DIST)
        needPlay = True
        if distToPlayer > needPlaySkillDist:
            if skillId:
                clientSkillInfo = self.getClientSkillInfo(skillId, skillLv)
                bloodLabelShowDist = clientSkillInfo.getSkillData('bloodLabelShowDist', gameglobal.PLAYSKILL_DIST)
                if distToPlayer > bloodLabelShowDist:
                    needPlay = False
            else:
                needPlay = False
        return needPlay

    def getSkinMaterial(self):
        sd = SCHD.data.get(self.realSchool)
        material = sd.get('skinMaterial', gameglobal.SKIN_MATERIAL_NO)
        return material

    def beHit(self, host, damage = None, callback = None, forceBeHitAct = False, clientSkillInfo = None):
        if not self.inWorld:
            return
        if not self.firstFetchFinished:
            return
        if not damage[0]:
            return
        fashionVal = self.fashion
        if BigWorld.player() == self:
            gameglobal.rds.ui.player.showBeHit()
            if gameglobal.rds.ui.shop.inRepair:
                gameglobal.rds.ui.shop.clearRepairState()
                gameglobal.rds.ui.messageBox.dismiss(uiConst.MESSAGEBOX_SHOP, False)
        if fashionVal.doingActionType() in (ACT.DEAD_ACTION, ACT.DYING_ACTION) or hasattr(self, 'jumping') and self.isJumping:
            return
        if self.life not in gametypes.LIFE_CAN_BEATTACK:
            return
        beHitAction = None
        if damage[1] == gametypes.DMGPOWER_AVOID:
            beHitAction = fashionVal.getBeHitActionName(gameglobal.AVOID_HIT)
        elif damage[1] == gametypes.DMGPOWER_BLOCK:
            beHitAction = fashionVal.getBeHitActionName(gameglobal.BLOCK_HIT)
        if not beHitAction:
            hitType = self.getbeHitType(host, damage[1])
            beHitAction = fashionVal.getBeHitActionName(hitType)
        if self.bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
            if self.modelServer.rideAttached.zaijuMode in (attachedModel.ZAIJU_BEATTACHED, attachedModel.ZAIJU_ATTACH):
                actions = ZJD.data.get(self.bianshen[1], {}).get('beHitAction', ())
                if actions:
                    beHitAction = random.choice(actions)
        if beHitAction == None:
            return
        if fashionVal.doingActionType() == action.JIDAO_START_ACTION and self.daoDiStartAction:
            self.playDaoDiStartAction()
            return
        try:
            act = self.model.action(beHitAction)
        except:
            return

        if fashionVal.doingActionType() in (ACT.UNKNOWN_ACTION,
         ACT.BEHIT_ACTION,
         ACT.STANDUP_ACTION,
         ACT.IDLE_ACTION,
         ACT.JUMP_ACTION,
         ACT.FALL_ACTION,
         ACT.EMOTE_ACTION,
         ACT.FALLEND_ACTION,
         ACT.PICK_ITEM_ACTION,
         ACT.FAINT_LOOP_ACTION,
         ACT.JIDAO_LOOP_ACTION,
         ACT.WING_FLY_UP_ACTION,
         ACT.WING_FLY_DOWN_ACTION,
         ACT.OPEN_WEAR_ACTION,
         ACT.CLOSE_WEAR_ACTION) or self.excludeStopAct():
            if self.inMoving() or self.isJumping or self.canFly() or self.needEnableAlpha():
                act.enableAlpha(1)
            self.beHitActionName = beHitAction
            act(0)

    def set_life(self, old):
        super(IAvatarCombatUnit, self).set_life(old)

    def afterModelFinish(self):
        gamelog.debug('afterModelFinish IAvatarCombatUnit')
        super(IAvatarCombatUnit, self).afterModelFinish()

    def getModelScale(self):
        return (1.0, 1.0, 1.0)

    def getTintModels(self, tintTypes):
        if tintTypes is None:
            return
        allmodels = []
        for i in tintTypes:
            models = []
            if i == const.BODYMODELS:
                models = [self.model]
            elif i == const.RIGHTMODELS:
                models = self.fashion.getRightWeaponModels()
            elif i == const.LEFTMODELS:
                models = self.fashion.getLeftWeaponModels()
            for m in models:
                allmodels.append(m)

        return allmodels

    def startSpell(self, targetId, skillId, skillLevel, time, targetPos, yaw):
        self.skillAlert(targetId, skillId, skillLevel, targetPos, gameglobal.S_SPELL, yaw)
        super(IAvatarCombatUnit, self).startSpell(targetId, skillId, skillLevel, time, targetPos, yaw)

    def startCharge(self, targetId, skillId, skillLevel):
        super(IAvatarCombatUnit, self).startCharge(targetId, skillId, skillLevel)

    def mfResult(self, mfId, mfType, lv, results, srcSkillId, srcSkillLv, rPosList):
        super(IAvatarCombatUnit, self).mfResult(mfId, mfType, lv, results, srcSkillId, srcSkillLv, rPosList)

    def guideSkillResult(self, targetId, guideSkillId, lv, results, targetPos = None):
        super(IAvatarCombatUnit, self).guideSkillResult(targetId, guideSkillId, lv, results, targetPos)

    def skillResult(self, sr):
        super(IAvatarCombatUnit, self).skillResult(sr)

    def getBodySize(self):
        return self.bodySize

    def getClientSkillInfo(self, skillId, skillLv):
        if hasattr(self, 'skillAppearancesDetail'):
            useSkillInfo = self.skillAppearancesDetail.getGeneralAppearanceSkillInfo(skillId, skillLv)
        else:
            useSkillInfo = ClientSkillInfo(skillId, skillLv)
        ret = self.skillPlayer.getSkillStateInfo(useSkillInfo, self)
        return ret

    def getClientStateAppearanceSkillInfo(self, skillId, appearanceId):
        pass

    def getZaijuDataWithCustom(self, zaijuId):
        data = ZJD.data.get(zaijuId, {})
        zaijuFromSkill = data.get('uniqueSkillId', None)
        if data and zaijuFromSkill:
            if hasattr(self, 'skillAppearancesDetail'):
                appId = self.skillAppearancesDetail.getCurrentAppearance(zaijuFromSkill)
                appData = SZAD.data.get((zaijuId, appId), {})
                if appData:
                    data = copy.copy(data)
                    data.update(appData)
        return data

    def getFenshenIdWithCustom(self, fenshenId):
        pass

    def getOpacityValue(self):
        if getattr(self, 'crossServerFlag', 0) == const.CROSS_SERVER_STATE_OUT:
            return (gameglobal.OPACITY_HIDE, False)
        opValues = super(IAvatarCombatUnit, self).getOpacityValue()
        if opValues[0] == gameglobal.OPACITY_HIDE:
            return opValues
        p = BigWorld.player()
        if p.__class__.__name__ == 'PlayerAccount' and gameglobal.rds.GameState > gametypes.GS_LOGIN:
            return (gameglobal.OPACITY_HIDE, False)
        if self.id != p.id and gameglobal.rds.GameState > gametypes.GS_LOGIN:
            spaceNo = getattr(BigWorld.player(), 'spaceNo', 0)
            mapId = formula.getMapId(spaceNo)
            if p.targetLocked == self:
                return (gameglobal.OPACITY_FULL, True)
            if p.isInCoupleRideAsRider() and p.coupleEmote[1] == self.id:
                return (gameglobal.OPACITY_FULL, True)
            if p.isRidingTogetherAsVice() and p.id in self.tride:
                return (gameglobal.OPACITY_FULL, True)
            if MCD.data.get(mapId, {}).get('hideAvatar', 0):
                return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
            if gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_NOT_GROUPER_WITHOUT_ENEMY and self.gbId not in p._getMembers() and not p.isEnemy(self):
                return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
            if gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_NOT_TEAMER_WITHOUT_ENEMY and (self.gbId in p._getMembers() and not utils.isSameTeam(self.groupIndex, p.groupIndex) or self.gbId not in p._getMembers()) and not p.isEnemy(self):
                return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
            if gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_ALL_WITHOUT_ENEMY and not p.isEnemy(self):
                return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
            if gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_ALL_WITHOUT_TOPLOGO:
                return (gameglobal.OPACITY_HIDE_WITHOUT_NAME, True)
            if gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_ALL_PLAYER:
                return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
            if gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_ALL_PLAYER_AND_ATTACK:
                return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
            if gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_DEFINE_SELF:
                if gameglobal.HIDE_MODE_CUSTOM_SHOW_GROUPER and self.gbId in p._getMembers():
                    return (gameglobal.OPACITY_FULL, gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO)
                elif gameglobal.HIDE_MODE_CUSTOM_SHOW_ENEMY and p.isEnemy(self):
                    return (gameglobal.OPACITY_FULL, gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO)
                elif gameglobal.HIDE_MODE_CUSTOM_SHOW_BOOTH and self.inBoothing():
                    return (gameglobal.OPACITY_FULL, gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO)
                elif gameglobal.HIDE_MODE_CUSTOM_SHOW_TEAMER and self.gbId in p._getMembers() and utils.isSameTeam(self.groupIndex, p.groupIndex):
                    return (gameglobal.OPACITY_FULL, gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO)
                else:
                    return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO)
        return (gameglobal.OPACITY_FULL, True)


class IMonsterCombatUnit(ICombatUnit):

    def __init__(self):
        super(IMonsterCombatUnit, self).__init__()
        self.monsterInstance = True
        self.changeType = None
        self._lockEff = None
        self.isFreezeAct = False
        self.dyingStage = 1
        self.needPlayInCombatAct = True
        self.needInCombatActCallback = None

    def prerequisites(self):
        return []

    def canOutline(self):
        return self.getItemData().get('canOutline', True)

    def needBlackShadow(self):
        return not self.getItemData().get('noBlackUfo', False)

    def needAttachUFO(self):
        return not self.getItemData().get('noUfo', False)

    def needHideName(self):
        return self.getItemData().get('hideName', False)

    def enterWorld(self):
        self.syncSubProps()
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.initYaw = self.yaw
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        if self.inDying and not gameglobal.rds.ui.dying.isOpen:
            gameglobal.rds.ui.dying.show(self.extendId, self.id)
        else:
            self.playBossMusic(True)

    def playBossMusic(self, status):
        soundIdx = self.getItemData().get('bossMusic', 0)
        if soundIdx:
            gameglobal.rds.sound.playBossMusic(soundIdx, status)

    def enterTopLogoRange(self, rangeDist = -1):
        super(IMonsterCombatUnit, self).enterTopLogoRange(rangeDist)
        gamelog.debug('bindVisible enterTopLogoRange')
        if self.topLogo:
            self.topLogo.bindVisible()

    def leaveTopLogoRange(self, rangeDist = -1):
        super(IMonsterCombatUnit, self).leaveTopLogoRange(rangeDist)

    def playerRelation(self, tgt):
        if tgt.fashion.isPlayer:
            return gametypes.RELATION_FRIENDLY
        elif self.canBeAttack(tgt):
            return gametypes.RELATION_ENEMY
        else:
            return gametypes.RELATION_FRIENDLY

    def onTargetCursor(self, enter):
        super(IMonsterCombatUnit, self).onTargetCursor(enter)

    def leaveWorld(self):
        if hasattr(self, 'modelServer') and self.modelServer:
            self.modelServer.release()
            self.modelServer = None
        super(IMonsterCombatUnit, self).leaveWorld()
        if self.extendId != 0:
            gameglobal.rds.ui.dying.close()
        self.playBossMusic(False)

    def getEffectStateModel(self):
        return None

    def getTintModels(self, tintTypes):
        return self.allModels

    def getItemData(self):
        md = MMCD.data.get(self.charType, None)
        if not BigWorld.player().isEnemy(self):
            isGraveState = gameglobal.rds.ui.mapGameMapV2.isGraveState()
            if isGraveState:
                if hasattr(self, 'getOpacityValue'):
                    opacityValue = self.getOpacityValue()
                    if opacityValue[0] == gameglobal.OPACITY_FULL:
                        md = copy.deepcopy(MMCD.data.get(self.charType, None))
                        md['extraTint'] = SCD.data.get('ghostmatte', 'refaction002')
                else:
                    md = copy.deepcopy(MMCD.data.get(self.charType, None))
                    md['extraTint'] = SCD.data.get('ghostmatte', 'refaction002')
        if not md:
            gamelog.error('getItemData: charType not found', self.charType)
            return {'model': gameglobal.defaultModelID,
             'dye': 'Default'}
        return md

    def addExtraTint(self):
        tint = self.getItemData().get('extraTint', None)
        if tint:
            tintalt.ta_add(self.allModels, tint)

    def getBodySize(self):
        return self.bodySize

    def changeModel(self, changeType):
        if self.changeType == changeType:
            return
        if self.modelServer:
            self.modelServer.release()
        self.modelServer = modelServer.SimpleModelServer(self)

    def afterModelFinish(self):
        if not self.inWorld or not self.fashion:
            return
        super(IMonsterCombatUnit, self).afterModelFinish()
        self.am.footTwistSpeed = 0
        self.filter.setYaw(self.initYaw)
        md = MMCD.data.get(self.charType, None)
        if md:
            if md.get('bodyRoll'):
                self.filter.enableBodyRoll = True
            self.isHardSchool = md.get('isHardSchool', False)
        self.refreshOpacityState()
        if md and md.get('initHide', 0) > 0 and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA or gameglobal.gHideMonsterFlag == gameglobal.HIDE_ALL_MONSTER:
            self.hide(True)
        self.set_life(self.life)
        self.fashion.setGuard(self.inCombat)
        if self.inGuard:
            self.fashion.setStateCaps([keys.CAPS_GROUND, keys.CAPS_GROUND_COMBAT])
            self.fashion.stopHeadTracker()
            self.set_inGuard(self.inGuard)
        if self.inDying:
            self.fashion.setDying(self.inDying)
        if hasattr(self, 'charType') and self.inCombat:
            gemini = MMCD.data.get(self.charType, {}).get('gemini', ())
            if gemini and not gameglobal.rds.ui.multiBossBlood.mediator:
                gameglobal.rds.ui.multiBossBlood.show(gemini)
        self.addExtraTint()

    def needMoveNotifier(self):
        return self.getItemData().get('idleGroupid', None) != None

    def movingNotifier(self, isMoving, moveSpeed = 1.0):
        self.isMoving = isMoving

    def attackResult(self, targetId, resultType, attackResult, nextAtkDelay = 0):
        super(IMonsterCombatUnit, self).attackResult(targetId, resultType, attackResult, nextAtkDelay)

    def use(self):
        player = BigWorld.player()
        player.beginAttack(self)

    def skillResult(self, skillResult):
        super(IMonsterCombatUnit, self).skillResult(skillResult)

    def startSpell(self, targetId, skillId, skillLevel, time, targetPos, yaw):
        self.skillAlert(targetId, skillId, skillLevel, targetPos, gameglobal.S_SPELL, yaw)
        self._startSpell(targetId, skillId, skillLevel, time, targetPos, 0.5)

    def skillStart(self, targetId, skillId, skillLevel, instant, targetPos):
        self._skillStart(targetId, skillId, skillLevel, 0, 0.0, None, instant, targetPos)

    def skillStartWithMove(self, targetId, skillId, skillLevel, moveId, moveTime, moveClientRefInfo, instant, targetPos):
        self._skillStart(targetId, skillId, skillLevel, moveId, moveTime, moveClientRefInfo, instant, targetPos)

    def _skillStart(self, targetId, skillId, skillLevel, moveId, moveTime, moveClientRefInfo, instant, targetPos):
        self.skillAlert(targetId, skillId, skillLevel, targetPos, gameglobal.S_CAST)
        super(IMonsterCombatUnit, self)._skillStart(targetId, skillId, skillLevel, moveId, moveTime, moveClientRefInfo, instant, targetPos)

    def stopSpell(self, success):
        if self.skillPlayer != None and self.skillPlayer.target != None:
            self.skillPlayer.target.removeIndicator()
        else:
            self.removeIndicator()
        super(IMonsterCombatUnit, self).stopSpell(success)

    def stopCast(self, skillId, skillLv, targetId, stopAction):
        super(IMonsterCombatUnit, self).stopCast(skillId, skillLv, targetId, stopAction)
        gamelog.debug('@PGF:stopCast:indicator', skillId, skillLv, targetId)
        if not self.inWorld or not self.fashion:
            return
        if stopAction:
            self.fashion.stopAction()
        self.skillPlayer.cancelMonsterMoveCallback()
        self._removeIndicatorByTarget(skillId, skillLv, targetId)

    def stopSkillMove(self, stopAction = True):
        if not self.inWorld or not self.skillPlayer or not self.fashion:
            return
        gamelog.debug('@PGF:Monster.stopSkillMove', self.skillPlayer.monsterMoveCallback, self.fashion.doingActionType(), stopAction)
        if stopAction:
            self.fashion.stopAction()
        self.skillPlayer.cancelMonsterMoveCallback()

    def _removeIndicatorByTarget(self, skillId, skillLv, targetId):
        skillInfo = SkillInfo(skillId, skillLv)
        if skillInfo == None:
            return
        showIndicator = skillInfo.getSkillData('showIndicator', 0)
        indicatorTime = skillInfo.getSkillData('indicatorTime', 0.0)
        if showIndicator == 1 and indicatorTime > 0:
            indicatorTarget = 0
            if skillInfo.hasSkillData('tgtSelf'):
                indicatorTarget = self.id
            if skillInfo.hasSkillData('tgtEnemyType'):
                indicatorTarget = targetId
            target = BigWorld.entities.get(indicatorTarget)
            if indicatorTarget != 0 and target != None:
                target.removeIndicator()

    def set_life(self, old):
        super(IMonsterCombatUnit, self).set_life(old)

    def attachReliveEffect(self):
        super(IMonsterCombatUnit, self).attachReliveEffect()
        if not self.inWorld:
            return
        itemData = self.getItemData()
        reliveEffHps = itemData.get('reliveEffHps')
        reliveEff = itemData.get('reliveEff')
        reliveEffScale = itemData.get('reliveEffScale', 1.0)
        if reliveEffHps and reliveEff:
            for attachHp in reliveEffHps:
                node = self.model.node(attachHp)
                if node == None:
                    gamelog.error('@PGF: attachReliveEffect attachHp node is not exit:', attachHp)
                    continue
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_ONNODE, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 attachHp,
                 reliveEff,
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))
                if fx:
                    for fxItem in fx:
                        fxItem.scale(reliveEffScale, reliveEffScale, reliveEffScale)

        elif reliveEff:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             reliveEff,
             sfx.EFFECT_LIMIT,
             gameglobal.EFFECT_LAST_TIME))
            if fx:
                for fxItem in fx:
                    fxItem.scale(reliveEffScale, reliveEffScale, reliveEffScale)

    def afterReliveAction(self):
        super(IMonsterCombatUnit, self).afterReliveAction()
        if hasattr(self, 'topLogo') and self.topLogo != None:
            self.topLogo.hide(False)

    def set_inCombat(self, old):
        if not self.inWorld or not self.fashion or not hasattr(self.fashion, 'action'):
            return
        self._playInCombatAction()
        p = BigWorld.player()
        if self == p.targetLocked and p.isEnemy(self):
            p.setTargetUfo(self, p.getTargetUfoType(self))
        super(IMonsterCombatUnit, self).set_inCombat(old)
        if hasattr(self, 'topLogo') and self.topLogo:
            if not p.isInBfDota():
                self.topLogo.showMonsterBlood(self.inCombat)
            if not self.inCombat and self.hideTopLogoOutCombat():
                self.topLogo.hideTitleName(True)
                self.topLogo.hideName(True)
            if self.inCombat:
                self.topLogo.hideTitleName(gameglobal.gHideMonsterTitle)
                self.topLogo.hideName(gameglobal.gHideMonsterName)
        if gameglobal.rds.ui.diGong.clockShow and p.inBossRoom():
            mlgNo = formula.getMLGNo(p.spaceNo)
            if self.charType == DBRD.data.get(mlgNo, {}).get('bossCharType'):
                gameglobal.rds.ui.diGong.closeDigongClock()
        if hasattr(self, 'charType') and self.inCombat:
            gemini = MMCD.data.get(self.charType, {}).get('gemini', ())
            if gemini and not gameglobal.rds.ui.multiBossBlood.mediator:
                gameglobal.rds.ui.multiBossBlood.show(gemini)
        self._monsterPopupMsgInEnterCombat()

    def _monsterPopupMsgInEnterCombat(self):
        if not gameglobal.rds.configData.get('enableMonsterTalkInCombat', False):
            return
        if not self.IsMonster or not self.inCombat or not (hasattr(self, 'topLogo') and self.topLogo):
            return
        talkInfo = SCFD.data.get('monsterEnterCombatTalk', ())
        if not talkInfo:
            return
        r = random.random()
        curRate = 0
        for rate, msg in talkInfo:
            curRate += rate
            if curRate > r:
                self.topLogo.setChatMsg(msg, const.POPUP_MSG_SHOW_DURATION)
                return

    def hideTopLogoOutCombat(self):
        return self.getItemData().get('hideTopLogoOutCombat', 0)

    def _playInCombatAction(self):
        if not self.inWorld or not self.fashion:
            return
        if self.life == gametypes.LIFE_DEAD or self.inDying:
            return
        if self.fashion.doingActionType() not in [ACT.UNKNOWN_ACTION, ACT.ALERT_ACTION, ACT.BORED_ACTION]:
            return
        if self.isObstacleModel():
            return
        inCombatStartAct = self.fashion.getInCombatStartActionName()
        gamelog.debug('@PGF:Monster', inCombatStartAct, self.inCombat)
        if (self.inCombat or self.inGuard) and inCombatStartAct != None and self.needPlayInCombatAct:
            self.fashion.stopActionByName(self.model, self.fashion.boredAct)
            self.fashion.playAction([inCombatStartAct], ACT.INCOMBAT_START_ACTION, None, 0)
        self.needPlayInCombatAct = True
        if self.needInCombatActCallback:
            BigWorld.cancelCallback(self.needInCombatActCallback)
            self.needInCombatActCallback = None

    def set_inGuard(self, old):
        if self.inGuard:
            self.needPlayInCombatAct = True
            self._playInCombatAction()
        else:
            self.needPlayInCombatAct = False
            if self.needInCombatActCallback:
                BigWorld.cancelCallback(self.needInCombatActCallback)
                self.needInCombatActCallback = None
            self.needInCombatActCallback = BigWorld.callback(0.1, Functor(self._resetNeedPlayInCombatAct))
        self.fashion.setHeadTracker(self.inGuard)

    def _resetNeedPlayInCombatAct(self):
        if not self.inWorld:
            return
        self.needInCombatActCallback = None
        if not self.needPlayInCombatAct:
            self.needPlayInCombatAct = True

    def set_inDying(self, old):
        if not self.firstFetchFinished or not self.inWorld or not self.fashion:
            return
        self.collideWithPlayer = False
        self.noSelected = False
        self.setTargetCapsUse(not self.noSelected)
        if self.inDying:
            self.fashion.stopAllActions()
            self.playDyingAction()
            gameglobal.rds.ui.dying.show(self.extendId, self.id)
            gameglobal.rds.ui.bossBlood.hideBossBlood()
            gameglobal.rds.ui.target.hideTargetUnitFrame()
            BigWorld.player().addInDyingEntityId(self.id)
        else:
            gameglobal.rds.ui.dying.close(True)
            BigWorld.player().removeInDyingEntityId(self.id)
        self.fashion.setDying(self.inDying)
        if old and not self.inDying:
            if self.life == gametypes.LIFE_DEAD:
                self.fashion.setDoingActionType(ACT.DYING_ACTION)
                self.playDieAction()
            else:
                p = BigWorld.player()
                if self.syncUnits:
                    self.noSelected = True
                else:
                    self.noSelected = False
                self.setTargetCapsUse(not self.noSelected)
                if p.targetLocked == self:
                    p.unlockTarget()
                    p.lockTarget(self)
                self.fashion.setStateCaps([keys.CAPS_GROUND_COMBAT])
                dyingDeadAct = self.fashion.getDyingDeadActionName()
                if dyingDeadAct:
                    self.fashion.stopActionByName(self.model, dyingDeadAct)
                dyingStandupAct = self.fashion.getDyingStandupActionName()
                if dyingStandupAct:
                    self.fashion.playAction([dyingStandupAct], ACT.DYING_ACTION, Functor(self.fashion.setDoingActionType, ACT.UNKNOWN_ACTION), 0)

    def set_syncUnits(self, old):
        if self.syncUnits:
            self.noSelected = True
        else:
            self.noSelected = False
        self.setTargetCapsUse(not self.noSelected)
        p = BigWorld.player()
        if p.targetLocked == self:
            p.unlockTarget()
            p.lockTarget(self)

    def playDieAction(self, needDieAction = True, forcePlayAction = False):
        if not self.inWorld:
            return
        if self.topLogo != None:
            self.topLogo.hide(True)
        if not self.model:
            return
        self.setTargetCapsUse(False)
        self.updateModelFreeze(-1.0)
        if self.killer:
            self.afterDieEffect(self)
            if MMCD.data[self.charType].get('faceKiller', 0):
                self.faceTo(self.killer)
        super(IMonsterCombatUnit, self).playDieAction(needDieAction, forcePlayAction)
        if self.fashion != None:
            self.fashion.attachUFO(ufo.UFO_NULL)

    def _realPlayDieAction(self, dieActionName, dieIdleName, needDieAction):
        if self.isObstacleModel():
            return
        if dieActionName and needDieAction:
            if dieIdleName:
                self.fashion.playAction([dieActionName, dieIdleName], ACT.DEAD_ACTION, Functor(self.playSpecialDie, dieIdleName), 0)
            else:
                self.fashion.playAction([dieActionName], ACT.DEAD_ACTION, self.afterDieAction)
        elif dieIdleName:
            self.fashion.playAction([dieIdleName], ACT.DEAD_ACTION)
            self.playSpecialDie(dieIdleName)
        else:
            self.afterDieAction()
        self._addTintByName('dieTint', self.getItemData())

    def _addTintByName(self, name, itemData):
        tintId = itemData.get(name + 'Id', 0)
        tintTime = itemData.get(name + 'Time', gameglobal.MONSTER_BORN_TINT_TIME)
        if tintId:
            if name == 'bornTint':
                self.bornFadeIn(tintId, 0.2)
                self.addTint(tintId, self.allModels, tintTime)
            else:
                self.addTint(tintId, self.allModels, tintTime)

    def getSkinMaterial(self):
        return MMCD.data.get(self.charType, {}).get('skinMaterial', 0)

    def modelHighlight(self, host, hitTintData):
        noModelHighLight = MMCD.data.get(self.charType, {}).get('noModelHighLight', 0)
        if noModelHighLight:
            return
        super(IMonsterCombatUnit, self).modelHighlight(host, hitTintData)

    def beHit(self, host, damage = None, callback = None, forceBeHitAct = False, clientSkillInfo = None):
        if not self.inWorld:
            return
        if self.life == gametypes.LIFE_DEAD:
            return
        monsterType = self.monsterStrengthType
        damageType = damage[1]
        castActions = (ACT.SPELL_ACTION,
         ACT.GUIDE_ACTION,
         ACT.CAST_ACTION,
         ACT.CHARGE_ACTION,
         ACT.STARTSPELL_ACTION,
         ACT.CHARGE_START_ACTION,
         ACT.STARTPRESPELL_ACTION,
         ACT.PRESPELLING_ACTION)
        stopActions = (ACT.CASTSTOP_ACTION,
         ACT.MOVINGSTOP_ACTION,
         ACT.AFTERMOVESTOP_ACTION,
         ACT.GUIDESTOP_ACTION)
        bufActions = (ACT.FUKONG_START_ACTION,
         ACT.FUKONG_LOOP_ACTION,
         ACT.FUKONG_STOP_ACTION,
         ACT.TIAOGAO_START_ACTION,
         ACT.TIAOGAO_LOOP_ACTION,
         ACT.TIAOGAO_STOP_ACTION,
         ACT.JIDAO_START_ACTION,
         ACT.JIDAO_LOOP_ACTION,
         ACT.JIDAO_STOP_ACTION)
        if self.inDying:
            if not self.fashion.doingActionType() == ACT.DYING_ACTION:
                dyingBeHitActNormal = self.fashion.getDyingBeHitActionNameNormal()
                dyingDeadAct = self.fashion.getDyingDeadActionName()
                if dyingBeHitActNormal != None and dyingDeadAct != None:
                    self.fashion.playAction([dyingBeHitActNormal, dyingDeadAct], ACT.BEHIT_ACTION, None, 0)
        elif self.fashion.doingActionType() in (ACT.IDLE_ACTION,
         ACT.BORED_ACTION,
         ACT.GUARD_ACTION,
         ACT.ALERT_ACTION,
         ACT.UNKNOWN_ACTION,
         ACT.INCOMBAT_START_ACTION) or self.fashion.doingActionType() in bufActions or self.fashion.doingActionType() in stopActions or self.fashion.doingActionType() in castActions or self.fashion.doingActionType() == ACT.ATTACK_ACTION or self.excludeStopAct():
            if self.life not in gametypes.LIFE_CAN_BEATTACK:
                gamelog.debug('zf8:beHit failed, not life', self.life)
                return
            if monsterType == gametypes.MONSTER_BOSS:
                return
            if monsterType in (gametypes.MONSTER_ELITE, gametypes.MONSTER_BOSS_WITH_HIT_ACTION) and self.excludeCastAct():
                return
            if gameglobal.rds.configData.get('enableHitActHpPercent', False) and not (monsterType == gametypes.MONSTER_VIVID and forceBeHitAct) and damage[0] < int(self.mhp * SYSCD.data.get('hitActHpPercent', 0)):
                return
            if damageType == gametypes.DMGPOWER_CRIT and self.fashion.doingActionType() == ACT.ATTACK_ACTION or self.excludeStopAct() or monsterType == gametypes.MONSTER_VIVID and forceBeHitAct and self.fashion.doingActionType() not in (ACT.TIAOGAO_START_ACTION,
             ACT.TIAOGAO_LOOP_ACTION,
             ACT.JIDAO_START_ACTION,
             ACT.JIDAO_LOOP_ACTION,
             ACT.FAINT_START_ACTION,
             ACT.FAINT_LOOP_ACTION):
                self.fashion.stopAllActions()
            if monsterType == gametypes.MONSTER_VIVID and forceBeHitAct:
                beHitAction = self.fashion.getForceBeHitActionName()
                hitType = self.getbeHitType(host, damageType)
                beHitAct = self.getVividAppointedBeHitAction(hitType, clientSkillInfo)
                if type(beHitAct) == int:
                    appointedBeHitAction = beHitAct
                elif type(beHitAct) == list or type(beHitAct) == tuple:
                    appointedBeHitAction = random.choice(self.getVividAppointedBeHitAction(hitType, clientSkillInfo))
                else:
                    appointedBeHitAction = self.getVividAppointedBeHitAction(hitType, clientSkillInfo)
                if appointedBeHitAction:
                    beHitAction = appointedBeHitAction
                if hitType in (gameglobal.LIE_HIT, gameglobal.LIE_CRIT_HIT, gameglobal.FAINT_HIT):
                    beHitAction = self.fashion.getBeHitActionName(hitType)
            else:
                hitType = self.getbeHitType(host, damageType)
                beHitAction = self.fashion.getBeHitActionName(hitType)
                appointedBeHitAction = self.getAppointedBeHitAction(hitType, clientSkillInfo)
                if appointedBeHitAction:
                    beHitAction = appointedBeHitAction
            if beHitAction == None:
                return
            if self.fashion.doingActionType() == action.JIDAO_START_ACTION and self.daoDiStartAction:
                self.playDaoDiStartAction()
                return
            try:
                act = self.model.action(beHitAction)
            except:
                return

            if self.inMoving() or self.needEnableAlpha():
                self.beHitActionName = beHitAction
                act.enableAlpha(True)
            act(0)

    def getVividAppointedBeHitAction(self, hitType, clientSkillInfo):
        if clientSkillInfo and hitType in gameglobal.FRONT_HIT_TUPLE:
            return clientSkillInfo.getSkillData('vividBeHitAction', None)

    def getAppointedBeHitAction(self, hitType, clientSkillInfo):
        if clientSkillInfo and hitType in gameglobal.FRONT_HIT_TUPLE:
            return clientSkillInfo.getSkillData('beHitAction', None)

    def clearFreezeAct(self, isNeedFreeze = False):
        if not self.inWorld or hasattr(self, 'model'):
            return
        self.isFreezeAct = isNeedFreeze
        if self.model.freezeTime > 0.25:
            return
        self.updateModelFreeze(-1.0)

    def playDyingBeHitAction(self):
        if self.fashion == None or self.fashion.doingActionType() == ACT.DYING_ACTION:
            return
        dyingBeHitAct = self.fashion.getDyingBeHitActionName()
        dyingDeadAct = self.fashion.getDyingDeadActionName()
        if dyingBeHitAct == None or dyingDeadAct == None:
            return
        self.fashion.playAction([dyingBeHitAct, dyingDeadAct], ACT.DYING_ACTION, Functor(self.fashion.setDoingActionType, ACT.DEAD_ACTION), 0)

    def notifyHitCount(self, stage, totalHit, hasBonus):
        p = BigWorld.player()
        if not gameglobal.rds.ui.dying.isOpen and self.inDying:
            gameglobal.rds.ui.dying.show(self.extendId, self.id)
            if p.targetLocked != None:
                gameglobal.rds.ui.bossBlood.setName(p.targetLocked.roleName + ' ±ÞÊ¬')
        info = MBD.data.get(self.extendId, None)
        if not info:
            return
        stageData = None
        for sd in info:
            if totalHit >= sd['hitRange'][0] and totalHit <= sd['hitRange'][1]:
                stageData = sd
                break

        if stageData == None:
            stageData = info[-1]
        hitRange = stageData['hitRange']
        curStageHitNum = min(totalHit - hitRange[0], hitRange[1] - hitRange[0] + 1)
        gameglobal.rds.ui.dying.setTeamHit(stage, curStageHitNum, hitRange[1] - hitRange[0] + 1, totalHit, hasBonus)
        gameglobal.rds.ui.bossBlood.hit()
        self.dyingStage = stage

    def playDyingAction(self):
        if not self.inWorld:
            return
        if self.fashion == None or self.fashion.doingActionType() == ACT.DYING_ACTION:
            return
        dyingDieAct = self.fashion.getDyingDieActionName()
        dyingDeadAct = self.fashion.getDyingDeadActionName()
        if dyingDieAct != None and dyingDeadAct != None:
            self.fashion.playAction([dyingDieAct, dyingDeadAct], ACT.DYING_ACTION, Functor(self.fashion.setDoingActionType, ACT.DEAD_ACTION), 0)
        else:
            gamelog.error('@PGF:dying: Error, can not find dying action')
        self.fashion.attachUFO(ufo.UFO_SHADOW)

    def die(self, killer, clientSkillInfo = None):
        self.killer = killer
        if hasattr(killer, 'id') and killer.id == BigWorld.player().id:
            gamelog.debug('hjx debug tutor monster die', killer.id, self.charType)
            gameglobal.rds.tutorial.onKillMonster(self.charType)
        if self.inDying:
            return
        super(IMonsterCombatUnit, self).die(killer)

    def playDieSpecialEffsAlone(self):
        itemData = self.getItemData()
        dieEffs = itemData.get('dieEffs', [])
        if not dieEffs:
            return
        immediateEffs = []
        for eff in dieEffs:
            delayEffs = []
            if eff[3]:
                delayEffs.append(eff)
                BigWorld.callback(eff[3], Functor(self._playDieSpecialEffsAlone, delayEffs))
            else:
                immediateEffs.append(eff)

        self._playDieSpecialEffsAlone(immediateEffs)

    def _playDieSpecialEffsAlone(self, effsInfo):
        for eff in effsInfo:
            dieEff = eff[0]
            dieEffHp = eff[1]
            dieEffScale = eff[2]
            if dieEffHp and dieEff:
                node = self.model.node(dieEffHp)
                if node == None:
                    gamelog.error('@PGF: _playDieSpecialEffsAlone attachHp node is not exit:', dieEffHp)
                    continue
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_ONNODE, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 dieEffHp,
                 dieEff,
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))
                if fx and dieEffScale > 0:
                    for fxItem in fx:
                        fxItem.scale(dieEffScale, dieEffScale, dieEffScale)

            elif dieEff:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 dieEff,
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))
                if fx and dieEffScale > 0:
                    for fxItem in fx:
                        fxItem.scale(dieEffScale, dieEffScale, dieEffScale)

        BigWorld.callback(0.5, Functor(self.removeAllFx))

    def playSpecialDie(self, deadActionName = '1521'):
        if not self.inWorld or not deadActionName or not self.fashion or not hasattr(self.fashion, 'modelID'):
            return
        itemData = self.getItemData()
        if self.dyingStage > 1:
            deadEffHps = gameglobal.BOSS_DYING_STAGE_2_HPS
            deadEff = gameglobal.BOSS_DYING_STAGE_2_EFF
            deadEffScale = gameglobal.BOSS_DYING_STAGE_2_SCALE
        else:
            deadEffHps = itemData.get('deadEffHps')
            deadEff = itemData.get('deadEff')
            deadEffScale = itemData.get('deadEffScale', 1.0)
        if deadEffHps and deadEff:
            for attachHp in deadEffHps:
                node = self.model.node(attachHp)
                if node == None:
                    gamelog.error('@PGF: playSpecialDie attachHp node is not exit:', attachHp)
                    continue
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_ONNODE, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 attachHp,
                 deadEff,
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))
                if fx:
                    for fxItem in fx:
                        fxItem.scale(deadEffScale, deadEffScale, deadEffScale)

        elif deadEff:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             deadEff,
             sfx.EFFECT_LIMIT,
             gameglobal.EFFECT_LAST_TIME))
            if fx:
                for fxItem in fx:
                    fxItem.scale(deadEffScale, deadEffScale, deadEffScale)

        if not modelRobber.getInstance().isMonsterRobber(self.id):
            if self.dyingStage > 1:
                deadTint = gameglobal.BOSS_DYING_STAGE_2_TINT
            else:
                deadTint = itemData.get('deadTint')
            if deadTint:
                self.addTint(deadTint, self.allModels, 0, tintType=tintalt.DIETINT)
        BigWorld.callback(0.5, Functor(self.removeAllFx))
        self.afterDieAction()

    def playHitFlyAct(self, pos, moveTime):
        hitFlyAct = self.fashion.getHitFlyActionName()
        self.fashion.playActionSequence(self.model, (hitFlyAct,), None)
        if moveTime > 0.0:
            BigWorld.callback(moveTime, Functor(self._finishHitFlyAct, hitFlyAct))
        self.fashion.stopActionByName(self.model, hitFlyAct)

    def refreshOpacityState(self):
        opValue = self.getOpacityValue()
        gamelog.debug('Monster@refreshOpacityState', opValue)
        if opValue[0] == gameglobal.OPACITY_HIDE:
            self._hide(True, const.BLEND_OUT_TINT_ID)
        elif opValue[0] == gameglobal.OPACITY_TRANS:
            self._hide(False, const.BLEND_OUT_TINT_ID)
            self.refreshRealModelState()
        else:
            self._hide(False)
            self.refreshRealModelState()

    def _hide(self, fHide = True, tintId = None):
        if not self.inWorld:
            return
        if tintId != None:
            self.addTint(tintId, self.allModels, 0)
        if fHide:
            if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
                self.hide(True)
            elif getattr(self, 'hidingPower', None):
                self.hide(True)
            else:
                BigWorld.callback(1.0, Functor(self.hide, True))
        else:
            if type(self.tintStateType[1]) == str and 'blendout' in self.tintStateType[1].lower():
                tintalt.ta_del(self.allModels, self.tintStateType[1])
                self.tintStateType[0] = 0
                self.tintStateType[1] = None
            self.hide(False)

    def calcDPS(self, dmg):
        pass

    def getOpacityValue(self):
        if gameglobal.gHideMonsterFlag == gameglobal.HIDE_ALL_MONSTER:
            return (gameglobal.OPACITY_HIDE, False)
        if gameglobal.gHideMonsterFlag == gameglobal.HIDE_NOT_SPECIAL_MONSTER:
            visibleGbId = getattr(self, 'visibleGbId', 0)
            if visibleGbId != BigWorld.player().gbId:
                return (gameglobal.OPACITY_HIDE, False)
        elif gameglobal.HIDE_ALL_MODELS or gameglobal.rds.ui.cameraTable.isHideMonsters():
            return (gameglobal.OPACITY_HIDE, False)
        return super(IMonsterCombatUnit, self).getOpacityValue()

    def set_randProps(self, old):
        p = BigWorld.player()
        if p.targetLocked == self:
            gameglobal.rds.ui.target.refreshRandProps()
            gameglobal.rds.ui.bossBlood.setBossTargetRandProps()
