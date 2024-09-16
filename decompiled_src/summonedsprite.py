#Embedded file name: /WORKSPACE/data/entities/client/summonedsprite.o
import BigWorld
import Math
import const
import utils
import gameglobal
import gamelog
import gametypes
import random
import math
import formula
import copy
from gameclass import Singleton
from iCombatUnit import IMonsterCombatUnit
from callbackHelper import Functor
from helpers import action
from helpers import tintalt
from Monster import Monster
from helpers import seqTask
from sfx import sfx
from helpers import tintalt as TA
from data import summon_sprite_data as SPD
from data import sprite_monster_data as SMD
from data import sprite_client_action_data as SCAD
from data import sys_config_data as SYSCD
from data import summon_sprite_skin_data as SSSKIND
from data import summon_sprite_foot_dust_data as SSFDD
from data import monster_model_client_data as MMCD
ANSWER_FOLLOW_ENTER_NEXT_TIME = 0
DEFAULT_SPRITE_POP_DIST = 0.5
THETA_RANGE = {gametypes.SPRITE_FOLLOW_POS_TYPE_NONE: (-180, 180),
 gametypes.SPRITE_FOLLOW_POS_TYPE_FORWARD: (-45, 45),
 gametypes.SPRITE_FOLLOW_POS_TYPE_LEFT: (-135, -45),
 gametypes.SPRITE_FOLLOW_POS_TYPE_RIGHT: (45, 135),
 gametypes.SPRITE_FOLLOW_POS_TYPE_BACK: (135, 225)}

class SpriteState(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.sprite = None

    def setSprite(self, sprite):
        self.sprite = sprite

    def handleAction(self, action):
        gamelog.debug('m.l@SpriteState.handleAction')

    def enter(self):
        pass

    def leave(self):
        pass


class SpriteDefaultState(SpriteState):

    def handleAction(self, action):
        pass

    def enter(self):
        gamelog.debug('m.l@SpriteDefaultState.enter')

    def leave(self):
        gamelog.debug('m.l@SpriteDefaultState.leave')


class SpriteStayState(SpriteState):

    def enter(self):
        gamelog.debug('m.l@SpriteStayState.enter')
        self.sprite.answerSpriteStayEnter()

    def leave(self):
        gamelog.debug('m.l@SpriteStayState.leave')
        self.sprite.stopFindStayPot()
        self.sprite.stopSpriteLingerTick()

    def handleAction(self, action):
        if not self.sprite:
            return
        if not getattr(self.sprite, 'spriteId', None):
            return
        if action == gametypes.SPRITE_STATE_ACTION_TYPE_RUSH_STOP:
            p = BigWorld.player()
            spriteData = SPD.data.get(self.sprite.spriteId, {})
            rushSpeed = spriteData.get('rushSpeed', 8)
            suggestPos = self.sprite.lastNextSuggestPos
            effectType = gametypes.SPRITE_ACTION_TYPE_FLY_RUSH_STOP if self.sprite.inFly else gametypes.SPRITE_ACTION_TYPE_RUSH_STOP
            p.base.suggestSpriteClientEffect(gametypes.SP_SGST_MOVETYPE_EFFECT_NOW, effectType)
            gamelog.debug('m.l@SpriteStayState.handleAction suggest rush stop', suggestPos, rushSpeed, effectType)


class SpriteFollowState(SpriteState):

    def handleAction(self, action):
        if not self.sprite:
            return
        if not getattr(self.sprite, 'inFly', None):
            return
        if action == gametypes.SPRITE_STATE_ACTION_TYPE_RUSH_STOP:
            p = BigWorld.player()
            effectType = gametypes.SPRITE_ACTION_TYPE_FLY_RUSH_STOP if self.sprite.inFly else gametypes.SPRITE_ACTION_TYPE_RUSH_STOP
            p.base.suggestSpriteClientEffect(gametypes.SP_SGST_MOVETYPE_EFFECT_NOW, effectType)

    def enter(self):
        global ANSWER_FOLLOW_ENTER_NEXT_TIME
        if ANSWER_FOLLOW_ENTER_NEXT_TIME and utils.getNow() < ANSWER_FOLLOW_ENTER_NEXT_TIME:
            gamelog.debug('@SpriteFollowState.enter in answer CD', ANSWER_FOLLOW_ENTER_NEXT_TIME)
            self.sprite.startSpriteFollowTick()
        else:
            ANSWER_FOLLOW_ENTER_NEXT_TIME = utils.getNow() + SYSCD.data.get('spriteAnswerFollowEnterNextTime', 10)
            spriteData = SPD.data.get(self.sprite.spriteId, {})
            delayTime = spriteData.get('spriteAnswerFollowDelayTime', 0)
            gamelog.debug('@SpriteFollowState.enter will answer', delayTime)
            self.sprite.clearBornChangeToStayCB()
            self.sprite.anserSpriteFollowEnter()
            if delayTime:
                BigWorld.callback(delayTime, self.sprite.startSpriteFollowTick)
            else:
                self.sprite.startSpriteFollowTick()

    def leave(self):
        gamelog.debug('@SpriteFollowState.leave')
        self.sprite.stopSpriteFollowTick()


spriteDefaultState = SpriteDefaultState.getInstance()
spriteFollowState = SpriteFollowState.getInstance()
spriteStayState = SpriteStayState.getInstance()
STATE_LIST = [spriteDefaultState, spriteFollowState, spriteStayState]

class SummonedSprite(Monster):
    IsMonster = False
    IsSummonedSprite = True
    IsSummoned = True

    def __init__(self):
        super(SummonedSprite, self).__init__()
        self.bodyModel = None
        self.transformModel = None
        self.transformBackActionPlaying = False
        self.applyTints = []
        self.flyKeepEffs = []
        self.flyMoveEffs = []
        self.groundMoveEffs = []
        self.suggestMoveActionWhenStop = None
        self.followTickCallback = None
        self.lingerTickCallback = None
        self.spriteState = None
        self.lastNextSuggestPos = None
        self.lastFollowTheta = None
        self.lastFollowDist = None
        self.findStayPotCB = None
        self.bornChangeToStayCB = None
        self.bornEffEndTime = 0
        self.transformBackCallback = None
        self.updateTargetCallback = None
        self.ownerAttackTargets = []
        self.modelServer = None
        self.spriteDustCallback = None

    def getOpacityValue(self):
        opacityVal = super(SummonedSprite, self).getOpacityValue()
        p = BigWorld.player()
        master = BigWorld.entities.get(self.ownerId)
        if master and master != p:
            if gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_DEFINE_SELF:
                if hasattr(master, 'inHiding') and master.inHiding():
                    opacityVal = (gameglobal.OPACITY_HIDE, False)
                elif p.targetLocked == self:
                    opacityVal = (gameglobal.OPACITY_FULL, True)
                elif gameglobal.HIDE_MODE_CUSTOM_SHOW_FRIEND_SPRITE and master.gbId in p._getMembers():
                    opacityVal = (gameglobal.OPACITY_FULL, gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO)
                elif gameglobal.HIDE_MODE_CUSTOM_SHOW_ENEMY_SPRITE and p.isEnemy(master):
                    opacityVal = (gameglobal.OPACITY_FULL, gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO)
                else:
                    opacityVal = (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.HIDE_MODE_CUSTOM_SHOW_TOPLOGO)
            elif gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_ALL_PLAYER_AND_ATTACK:
                opacityVal = (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
            elif gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_ALL_PLAYER:
                opacityVal = (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
        if opacityVal[0] == gameglobal.OPACITY_FULL:
            if master and master.isShowClanWar():
                if master != p:
                    if p.targetLocked == self:
                        opacityVal = (gameglobal.OPACITY_FULL, True)
                    else:
                        opacityVal = (gameglobal.OPACITY_HIDE_WITHOUT_NAME, True)
        if gameglobal.rds.ui.cameraTable.isHideSprites():
            opacityVal = (gameglobal.OPACITY_HIDE, False)
        if getattr(master, 'assassinationTeleport', 0):
            if master.gbId != BigWorld.player().gbId:
                return (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, False)
        return opacityVal

    def refreshOpacityState(self):
        super(IMonsterCombatUnit, self).refreshOpacityState()

    def getEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if hasattr(self, 'ownerId') and BigWorld.entity(self.ownerId):
                return BigWorld.entity(self.ownerId).getEffectLv()
            else:
                return getattr(BigWorld.player(), 'monsterEffectLv', gameglobal.EFFECT_MID)
        else:
            return gameglobal.EFFECT_MID

    def enterWorld(self):
        super(SummonedSprite, self).enterWorld()
        owner = BigWorld.entity(self.ownerId)
        p = BigWorld.player()
        if self.callOutType not in (gametypes.SPRITE_CALLOUT_TYPE_SPECIAL_EFFECT,):
            if owner == p:
                owner.summonedSpriteInWorld = self
                gameglobal.rds.ui.summonedSpriteUnitFrameV2.resetZhaoHuan(True, self)
                if getattr(self, 'bornActionName', None):
                    smData = SMD.data.get(self.charType, {})
                    bornTime = smData.get('bornTime', 4)
                    self.bornChangeToStayCB = BigWorld.callback(bornTime, self.changeToStayState)
                    BigWorld.callback(bornTime, self.afterBornActionDone)
                else:
                    self.changeToStayState()
                    self.afterBornActionDone()
                if not hasattr(self, 'shouldSuggest'):
                    self.updateSpriteLockTarget()
                gameglobal.rds.ui.summonedSpriteUnitFrameV2.updateCombat(self.inCombat)
        if owner:
            owner.spriteObjId = self.id
            gameglobal.rds.spriteOwnerDict[self.ownerId] = self.id
        elif not owner:
            gameglobal.rds.spriteOwnerDict[self.ownerId] = self.id
        self.preLoadTransformModel()

    def afterBornActionDone(self):
        if not self.inWorld:
            return
        owner = BigWorld.entity(self.ownerId)
        p = BigWorld.player()
        if owner == p:
            if p.inSwim or p.inFly:
                p.suggestSpriteFly(True, False)

    def clearBornChangeToStayCB(self):
        if self.bornChangeToStayCB:
            BigWorld.cancelCallback(self.bornChangeToStayCB)
            self.bornChangeToStayCB = None

    def playBornEff(self):
        spriteData = SPD.data.get(self.spriteId, {})
        smData = SMD.data.get(self.charType, {})
        bornEffs = spriteData.get('bornEffs', 0)
        lastTime = smData.get('bornTime', gameglobal.EFFECT_LAST_TIME)
        self.bornEffEndTime = utils.getNow() + lastTime
        if bornEffs:
            for bornEff in bornEffs:
                effs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
                 self.getSkillEffectPriority(),
                 self.model,
                 bornEff,
                 sfx.EFFECT_LIMIT,
                 lastTime))
                if effs:
                    modelScale = spriteData.get('bornEffScale', 1)
                    for ef in effs:
                        if ef:
                            ef.scale(modelScale)

    def playDieEff(self):
        spriteData = SPD.data.get(self.spriteId, {})
        dieEffs = spriteData.get('dieEffs', 0)
        if dieEffs:
            for dieEff in dieEffs:
                effs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
                 self.getSkillEffectPriority(),
                 self.model,
                 dieEff,
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))
                if effs:
                    modelScale = self.getItemData().get('modelScale', 1)
                    for ef in effs:
                        if ef:
                            ef.scale(modelScale)

        destroyDelay = SMD.data.get(self.charType, {}).get('destroyDelay', 10)
        delay = destroyDelay - spriteData.get('deadTintTime', 0)
        BigWorld.callback(delay, self.playDieTint)

    def playDieTint(self):
        if not self.inWorld:
            return
        spriteData = SPD.data.get(self.spriteId, {})
        deadTint = spriteData.get('deadTint', 0)
        if deadTint:
            tintTime = spriteData.get('deadTintTime', 0)
            self.addTint(deadTint, self.allModels, tintTime, tintType=tintalt.DIETINT)

    def getOwnerSafeDist(self):
        spriteData = SPD.data.get(self.spriteId, {})
        return spriteData.get('ownerSafeDist', 1.5)

    def getSpriteModelId(self, modelId):
        skinData = SSSKIND.data.get((self.spriteId, self.skinId), {})
        spriteModelId = skinData.get(modelId, 0)
        return spriteModelId

    def changeSpriteSkinModelSucc(self):
        if not self.inWorld:
            return
        transformedModel = self.getSpriteModelId('transformModelIdAfter')
        if self.transformed and transformedModel:
            spriteData = SPD.data.get(self.spriteId, {})
            scale = spriteData.get('transformModelScale', 1)
            self.loadTransformModel(transformedModel, scale)
        else:
            spriteModel = self.getSpriteModelId('transformModelIdBefore')
            modelPath = gameglobal.getSimpleModelPath(spriteModel)
            skinData = SSSKIND.data.get((self.spriteId, self.skinId), {})
            tintMs = skinData.get('materialsBefore', 'Default')
            self.fashion.loadSinglePartModel(modelPath, tintMs)

    def preLoadTransformModel(self):
        spriteData = SPD.data.get(self.spriteId, {})
        transformModelId = self.getSpriteModelId('transformModelIdAfter')
        if transformModelId:
            scale = spriteData.get('transformModelScale', 1)
            self.loadTransformModel(transformModelId, scale)

    def onRunToMaster(self):
        runStopAction = SPD.data.get(self.spriteId, {}).get('runStopAction')
        if runStopAction:
            try:
                self.model.action(runStopAction)()
            except:
                pass

    def onDoEmote(self, sEmoteID):
        gamelog.info('@smj onDoEmote', sEmoteID)
        if not self.inWorld:
            return
        try:
            self.fashion.playSingleAction(str(sEmoteID), action.EMOTE_ACTION)
        except:
            pass

    def onSpecialSpriteEvent(self, entId, relation, eventType, chatId):
        p = BigWorld.player()
        p.chatTextFromSprite(const.SSPRITE_TALK_RANGE_NEARBY, self.roleName, self.id, p.roleName, p.gbId, chatId, None)

    def leaveWorld(self):
        if getattr(self, 'modelServer', None):
            self.fashion.stopAllActions()
        super(SummonedSprite, self).leaveWorld()
        self.bodyModel = None
        self.transformModel = None
        self.flyKeepEffs = []
        self.flyMoveEffs = []
        self.groundMoveEffs = []
        self.stopFindStayPot()
        self.stopSpriteLingerTick()
        self.stopSpriteFollowTick()
        self.stopUpdateSpriteTarget()
        self.stopSpriteDustCallback()
        owner = BigWorld.entity(self.ownerId)
        if owner == BigWorld.player():
            if gameglobal.rds.ui.summonedSpriteUnitFrameV2.summonedSprite == self:
                gameglobal.rds.ui.summonedSpriteUnitFrameV2.resetZhaoHuan(False)
            if owner.summonedSpriteInWorld and self.id == owner.summonedSpriteInWorld.id:
                owner.summonedSpriteInWorld = None
        elif owner:
            owner.spriteObjId = 0
        seqTask.modelMemoryCtrl().decSummonedSprite()
        if self.ownerId in gameglobal.rds.spriteOwnerDict:
            gameglobal.rds.spriteOwnerDict.pop(self.ownerId)

    def getItemData(self):
        md = MMCD.data.get(self.charType, None)
        if not md:
            return {'model': gameglobal.defaultModelID,
             'dye': 'Default'}
        md = copy.copy(md)
        normalModel = self.getSpriteModelId('transformModelIdBefore')
        if normalModel:
            md['model'] = normalModel
        return md

    def onDismiss(self):
        self.stopSpriteLingerTick()
        if self.life == gametypes.LIFE_ALIVE:
            self.playSuggetActionEffct(gametypes.SPRITE_ACTION_TYPE_GO_BACK)

    def onResummon(self):
        pass

    def set_mode(self, old):
        owner = BigWorld.entity(self.ownerId)
        if owner == BigWorld.player():
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.changeState(self.mode)

    def set_transformed(self, old):
        gamelog.debug('SummonedSprite.set_transformed a', old, self.transformed)
        if not self.isRealModel:
            return
        spriteData = SPD.data.get(self.spriteId, {})
        transformModelId = self.getSpriteModelId('transformModelIdAfter')
        if transformModelId:
            if self.transformBackCallback:
                BigWorld.cancelCallback(self.transformBackCallback)
                self.transformBackCallback = None
            if self.transformed:
                self.fashion.stopAllActions()
                if self.model != self.transformModel:
                    transStartAction = spriteData.get('transStartAction', None)
                    if self.transformModel:
                        self.playTransformAction()
                        scale = spriteData.get('transformModelScale', 1)
                        self.transformModel.scale = (scale, scale, scale)
                    if self.getOpacityValue()[0] not in gameglobal.OPACITY_HIDE_TOPLOGO:
                        if self.bodyModel and not self.bodyModel.attached:
                            self.addModel(self.bodyModel)
                            self.addSpriteTinitMs(self.bodyModel, 'materialsBefore')
                        self.fashion.playActionSequence(self.bodyModel, [transStartAction], Functor(self.deleteSecModel, self.bodyModel))
                self.resetTopLogo()
            elif self.inFly:
                self._realTransformBack()
            else:
                delay = SYSCD.data.get('spriteTransformBackDelay', 1)
                self.transformBackCallback = BigWorld.callback(delay, self._realTransformBack)

    def _realTransformBack(self):
        if not self.inWorld:
            return
        if self.model != self.transformModel:
            return
        if not self.bodyModel:
            return
        spriteData = SPD.data.get(self.spriteId, {})
        transBackStartAction = spriteData.get('transBackStartAction', None)
        self.playTransformBackAction()
        if self.getOpacityValue()[0] not in gameglobal.OPACITY_HIDE_TOPLOGO:
            if self.transformModel and not self.transformModel.attached:
                self.addModel(self.transformModel)
                self.addSpriteTinitMs(self.transformModel, 'materialsAfter')
            self.fashion.playActionSequence(self.transformModel, [transBackStartAction], Functor(self.deleteSecModel, self.transformModel))
        self.resetTopLogo()

    def deleteSecModel(self, model):
        try:
            if self.inWorld and model.inWorld and model.attached:
                self.delModel(model)
        except:
            pass

    def playTransformAction(self):
        if self.transformModel and self.model != self.transformModel:
            spriteData = SPD.data.get(self.spriteId, {})
            transEndAction = spriteData.get('transEndAction', '7106')
            if not self.transformModel.attached:
                self.fashion.setupModel(self.transformModel, True)
                self.addSpriteTinitMs(self.transformModel, 'materialsAfter')
                self.refreshOpacityState()
            if self.getOpacityValue()[0] in gameglobal.OPACITY_HIDE_TOPLOGO:
                return
            effects = spriteData.get('transformEffs', [])
            if effects:
                for effect in effects:
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                     self.getBasicEffectPriority(),
                     self.transformModel,
                     effect,
                     sfx.EFFECT_LIMIT))

            self.fashion.playActionSequence2(self.transformModel, [(transEndAction,
              None,
              0,
              0)])

    def playTransformBackAction(self):
        if self.bodyModel and self.model != self.bodyModel:
            spriteData = SPD.data.get(self.spriteId, {})
            transBackEndAction = spriteData.get('transBackEndAction', None)
            if not self.bodyModel.attached:
                self.fashion.setupModel(self.bodyModel, True)
                self.addSpriteTinitMs(self.bodyModel, 'materialsBefore')
                self.refreshOpacityState()
            if self.getOpacityValue()[0] in gameglobal.OPACITY_HIDE_TOPLOGO:
                return
            effects = spriteData.get('transformBackEffs', 0)
            if effects:
                for effect in effects:
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                     self.getBasicEffectPriority(),
                     self.bodyModel,
                     effect,
                     sfx.EFFECT_LIMIT))

            self.fashion.playSingleAction(transBackEndAction, action.SUMMON_SPRITE_TRANSFORM_ACTION, 0, self.afterTranformBack)

    def afterTranformBack(self):
        if self.inFly:
            self.setInFly(True)

    def loadTransformModel(self, transformModelId, scale):
        skinData = SSSKIND.data.get((self.spriteId, self.skinId), {})
        tintMs = skinData.get('materialsAfter', 'Default')
        modelPath = gameglobal.getSimpleModelPath(transformModelId)
        self.fashion.loadSinglePartModel(modelPath, tintMs, callback=Functor(self.transformModelFinished, scale))

    def transformModelFinished(self, scale, model):
        if not self.inWorld:
            return
        if not model:
            return
        self.addSpriteTinitMs(model, 'materialsAfter')
        self.transformModel = model
        if self.transformed:
            self.fashion.setupModel(model, True)
            model.scale = (scale, scale, scale)

    def afterModelFinish(self):
        if not self.inWorld:
            return
        super(SummonedSprite, self).afterModelFinish()
        self.addSpriteTinitMs(self.model, 'materialsBefore')
        self.bodyModel = self.model
        if self.transformed:
            self.set_transformed(False)

    def addSpriteTinitMs(self, model, materials):
        skinData = SSSKIND.data.get((self.spriteId, self.skinId), {})
        tintMs = skinData.get(materials, 'Default')
        if tintMs and tintMs != 'Default':
            TA.ta_set_static([model], tintMs)

    def playSpriteDustEffect(self):
        if not self.inWorld:
            return
        p = BigWorld.player()
        dustData = SSFDD.data.get((self.spriteId, self.dustId), {})
        if self.getOpacityValue()[0] not in gameglobal.OPACITY_HIDE_TOPLOGO:
            effects = dustData.get('footDustEffects', [])
            eScale = dustData.get('footDustEffectScale', 1.0)
            if self.model and effects:
                for effect in effects:
                    efs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (p.getEquipEffectLv(),
                     p.getEquipEffectPriority(),
                     self.model,
                     effect,
                     sfx.EFFECT_LIMIT_MISC,
                     self.position,
                     0,
                     self.model.yaw))
                    if efs:
                        for ef in efs:
                            ef and ef.scale(eScale)

        if self.spriteDustCallback:
            self.stopSpriteDustCallback()
        footDustEffectCD = dustData.get('footDustEffectCD', 1)
        self.spriteDustCallback = BigWorld.callback(footDustEffectCD, self.playSpriteDustEffect)

    def stopSpriteDustCallback(self):
        if self.spriteDustCallback:
            BigWorld.cancelCallback(self.spriteDustCallback)
        self.spriteDustCallback = None

    def setEntityFilter(self):
        if self.inFly:
            self.filter = BigWorld.AvatarFilter()
        else:
            self.filter = BigWorld.AvatarDropFilter()
            self.filter.popDist = SYSCD.data.get('spriteDropFilterPopDist', DEFAULT_SPRITE_POP_DIST)

    def set_hp(self, old):
        super(SummonedSprite, self).set_hp(old)
        self.updateHpInfo()

    def set_mhp(self, old):
        super(SummonedSprite, self).set_mhp(old)
        self.updateHpInfo()

    def set_mmp(self, old):
        super(SummonedSprite, self).set_mmp(old)
        self.updateMpInfo()

    def set_mp(self, old):
        super(SummonedSprite, self).set_mp(old)
        self.updateMpInfo()

    def updateHpInfo(self):
        owner = BigWorld.entity(self.ownerId)
        if owner == BigWorld.player():
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.updateSummonedSpriteHP(self)

    def updateMpInfo(self):
        owner = BigWorld.entity(self.ownerId)
        if owner == BigWorld.player():
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.updateSummonedSpriteMP(self)

    def set_lv(self, old):
        super(SummonedSprite, self).set_lv(old)
        owner = BigWorld.entity(self.ownerId)
        if owner == BigWorld.player():
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.updateSummonedSpriteLV(self)

    @property
    def inFly(self):
        if not self.inWorld:
            return
        return self.statusL2 / 10 == gametypes.SP_ST_L1_FLY

    def set_statusL2(self, old):
        gamelog.debug('m.l@smj set_statusL2 from %d to %d' % (old, self.statusL2), self.id)
        if self.statusL2 / 10 == gametypes.SP_ST_L1_FLY:
            if old / 10 != gametypes.SP_ST_L1_FLY:
                self.setInFly(True)
        elif old / 10 == gametypes.SP_ST_L1_FLY:
            self.setInFly(False)
        owner = BigWorld.entity(self.ownerId)
        if owner == BigWorld.player():
            stateText = SYSCD.data.get('spriteStateDescs', {}).get(self.statusL2, 'Î´Öª')
            text = '×´Ì¬£º(%d£¬%s)' % (self.statusL2, stateText)
            gameglobal.rds.ui.summonedSpriteGM.setStateText(text)

    def gotoSpriteState(self, newState):
        gamelog.debug('m.l@SummonedSprite.gotoSpriteState', self.id, self.spriteState, newState)
        if self.spriteState != newState:
            if self.spriteState:
                self.spriteState.leave()
            newState.setSprite(self)
            self.spriteState = newState
            self.spriteState.enter()
        else:
            gamelog.debug('m.l@SummonedSprite.gotoSpriteState switch to same state!')

    def changeToFollowState(self):
        global spriteFollowState
        gamelog.debug('m.l@SummonedSprite.changeToFollowState')
        if not self.inWorld:
            return
        if self.statusL2 == gametypes.SP_ST_L2_LEAVE_BACK:
            return
        owner = BigWorld.entity(self.ownerId)
        if owner == BigWorld.player():
            ownerInMoving = owner.inMoving()
            if not ownerInMoving:
                if owner.tride.inRide():
                    header = BigWorld.entity(owner.tride.header)
                    if header:
                        if header.inMoving():
                            ownerInMoving = True
                if owner.attachSkillData:
                    attachEnt = BigWorld.entities.get(owner.attachSkillData[0], None)
                    if attachEnt:
                        ownerInMoving = attachEnt.inMoving()
                if owner.vehicle:
                    ownerInMoving = True
            if not ownerInMoving:
                return
        if self.inCombat:
            return
        self.gotoSpriteState(spriteFollowState)

    def changeToStayState(self):
        global spriteStayState
        gamelog.debug('m.l@SummonedSprite.changeToStayState')
        if not self.inWorld:
            return
        if self.inCombat:
            return
        self.gotoSpriteState(spriteStayState)

    def changeToDefaultState(self):
        global spriteDefaultState
        gamelog.debug('m.l@SummonedSprite.changeToDefaultState')
        self.gotoSpriteState(spriteDefaultState)

    def set_life(self, old):
        super(SummonedSprite, self).set_life(old)
        owner = BigWorld.entity(self.ownerId)
        if self.life == gametypes.LIFE_DEAD:
            self.playDieEff()
        if owner == BigWorld.player():
            if self.callOutType not in (gametypes.SPRITE_CALLOUT_TYPE_SPECIAL_EFFECT,):
                if self.life == gametypes.LIFE_DEAD and getattr(owner, 'inCombat', False):
                    owner.summonedSpriteLifeList.append(owner.lastSpriteBattleIndex)
                    gameglobal.rds.ui.summonedWarSpriteMine.updateSpriteLifeState()
                    gameglobal.rds.ui.actionbar.refreshSummonedSprite(owner.lastSpriteBattleIndex)
                    gameglobal.rds.ui.summonedWarSpriteFight.refreshInfo()

    def playFlyKeepEff(self):
        spriteData = SPD.data.get(self.spriteId, {})
        flyKeepEffs = spriteData.get('flyKeepEffs', None)
        if flyKeepEffs and not self.flyKeepEffs:
            for flyKeepEff in flyKeepEffs:
                eff = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 flyKeepEff,
                 sfx.EFFECT_LIMIT))
                if eff:
                    self.flyKeepEffs += eff

    def releaseFlyKeepEff(self):
        if self.flyKeepEffs:
            for eff in self.flyKeepEffs:
                if eff:
                    eff.stop()

            self.flyKeepEffs = []

    def resetFlyEff(self):
        if self.inFly:
            self.releaseFlyKeepEff()
            self.playFlyKeepEff()
        else:
            self.releaseFlyKeepEff()

    def resetMoveEff(self, inMoving, forceReset = False):
        if not inMoving or forceReset:
            self.releaseGroundMoveEff()
            self.releaseFlyMoveEff()
        if inMoving:
            if self.inFly:
                self.playFlyMoveEff()
            else:
                self.playGroundMoveEff()

    def playMoveEff(self):
        if self.inFly:
            self.playFlyMoveEff()
        else:
            self.playGroundMoveEff()

    def releaseMoveEff(self):
        if self.inFly:
            self.releaseFlyMoveEff()
        else:
            self.releaseGroundMoveEff()

    def playFlyMoveEff(self):
        spriteData = SPD.data.get(self.spriteId, {})
        flyMoveEffs = spriteData.get('flyMoveEffs', None)
        if flyMoveEffs and not self.flyMoveEffs:
            for flyMoveEff in flyMoveEffs:
                eff = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 flyMoveEff,
                 sfx.EFFECT_LIMIT))
                if eff:
                    self.flyMoveEffs += eff

    def releaseFlyMoveEff(self):
        if self.flyMoveEffs:
            for eff in self.flyMoveEffs:
                if eff:
                    eff.stop()

            self.flyMoveEffs = []

    def playGroundMoveEff(self):
        spriteData = SPD.data.get(self.spriteId, {})
        groundMoveEffs = spriteData.get('groundMoveEffs', None)
        if groundMoveEffs and not self.groundMoveEffs:
            for groundMoveEff in groundMoveEffs:
                eff = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 groundMoveEff,
                 sfx.EFFECT_LIMIT))
                if eff:
                    self.groundMoveEffs += eff

    def releaseGroundMoveEff(self):
        if self.groundMoveEffs:
            for eff in self.groundMoveEffs:
                if eff:
                    eff.stop()

            self.groundMoveEffs = []

    def setInFly(self, inFly):
        self.isFlyMonster = inFly
        self.resetMoveEff(self.inMoving(), True)
        self.resetFlyEff()
        self.fashion.autoSetStateCaps()
        if inFly:
            self.filter = BigWorld.AvatarFilter()
            self.setInFlyCaps()
        else:
            self.filter = BigWorld.AvatarDropFilter()
            self.filter.popDist = SYSCD.data.get('spriteDropFilterPopDist', DEFAULT_SPRITE_POP_DIST)
        if inFly and self.transformModel:
            if self.transformModel == self.model:
                self._realTransformBack()

    def playSuggetActionEffct(self, effectId):
        if not self.inWorld:
            return
        if not self.model or self.model.visible == False:
            return
        info = SCAD.data.get((effectId, self.spriteId), {})
        action = info.get('action', None)
        if action:
            try:
                self.model.action(action)()
                effects = info.get('effects', None)
                effectScale = info.get('effectScale', 1)
                if effects:
                    for eff in effects:
                        effs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                         self.getBasicEffectPriority(),
                         self.model,
                         eff,
                         sfx.EFFECT_LIMIT))
                        if effs:
                            for ef in effs:
                                if ef:
                                    ef.scale(effectScale)

            except Exception as e:
                gamelog.warning('m.l@SummonedSprite.playSuggetActionEffct', e.message)

    def handleSuggestActionSpecial(self, effectId):
        if effectId == gametypes.SPRITE_ACTION_TYPE_LINGER:
            self.suggestMoveActionWhenStop = effectId
            return True
        if effectId in (gametypes.SPRITE_ACTION_TYPE_RUSH_STOP, gametypes.SPRITE_ACTION_TYPE_FLY_RUSH_STOP):
            self.suggestMoveActionWhenStop = effectId
            return True
        return False

    def playLingerSuggestAction(self):
        spriteData = SPD.data.get(self.spriteId, {})
        lingerDirType = spriteData.get('lingerDirType', 0)
        direction = self.getLingerDirection(lingerDirType)
        actionId = None
        if direction:
            BigWorld.player().base.suggestSpriteTurn(direction)
        lingerActions = None
        if self.inFly:
            lingerActions = spriteData.get('lingerFlyActions', [])
        else:
            lingerActions = spriteData.get('lingerActions', [])
        if lingerActions:
            actionIds = [ a[0] for a in lingerActions ]
            probs = [ a[1] for a in lingerActions ]
            actionId = utils.chooseWithProps(actionIds, probs, sum(probs))
            self.fashion.playAction([actionId], action.SUMMON_SPRITE_LINGER)
        gamelog.debug('m.l@SummonedSprite.playLingerSuggestAction', lingerDirType, direction, self.position, actionId)

    def getLingerDirection(self, lingerDirType):
        if lingerDirType == gametypes.SPRITE_LINGER_DIR_TYPE_NONE:
            return None
        if lingerDirType == gametypes.SPRITE_LINGER_DIR_TYPE_FACE_PLAYER_POS:
            return Math.Vector3(0, 0, (BigWorld.player().position - self.position).yaw)
        if lingerDirType == gametypes.SPRITE_LINGER_DIR_TYPE_FACE_PLAYER_DIR:
            return Math.Vector3(0, 0, BigWorld.player().yaw)
        if lingerDirType == gametypes.SPRITE_LINGER_DIR_TYPE_BACK_PLAYER_POS:
            return Math.Vector3(0, 0, (self.position - BigWorld.player().position).yaw)
        if lingerDirType == gametypes.SPRITE_LINGER_DIR_TYPE_BACK_PLAYER_DIR:
            return Math.Vector3(0, 0, BigWorld.player().yaw - math.pi)

    def onSuggestMoved(self, effectId):
        if effectId > 0:
            gamelog.debug('m.l@SummonedSprite.onSuggestMoved', effectId)
            if not self.handleSuggestActionSpecial(effectId):
                self.playSuggetActionEffct(effectId)
        else:
            gamelog.warning('m.l@SummonedSprite.onSpriteSuggestMove error cause', effectId)

    def movingNotifier(self, isMoving, moveSpeed = 1.0):
        super(SummonedSprite, self).movingNotifier(isMoving, moveSpeed)
        self.resetMoveEff(isMoving, False)
        if not isMoving:
            self.playSuggestMoveActionWhenStop()
            self.stopSpriteDustCallback()
        else:
            if self.fashion._doingActionType in (action.SUMMON_SPRITE_LINGER, action.EMOTE_ACTION):
                self.fashion.stopAllActions()
            if not self.inFly:
                self.playSpriteDustEffect()
            else:
                self.stopSpriteDustCallback()

    def playSuggestMoveActionWhenStop(self):
        if self.suggestMoveActionWhenStop:
            if self.suggestMoveActionWhenStop in (gametypes.SPRITE_ACTION_TYPE_RUSH_STOP, gametypes.SPRITE_ACTION_TYPE_FLY_RUSH_STOP):
                self.playRushStop(self.suggestMoveActionWhenStop)
            if self.suggestMoveActionWhenStop == gametypes.SPRITE_ACTION_TYPE_LINGER:
                spriteData = SPD.data.get(self.spriteId, {})
                if random.random() < spriteData.get('lingerActionProb', 0.5):
                    self.playLingerSuggestAction()
        self.suggestMoveActionWhenStop = None

    def playRushStop(self, effectId):
        gamelog.debug('m.l@SummonedSprite.playRushStop', effectId)
        self.playSuggetActionEffct(effectId)

    def set_inCombat(self, old):
        super(self.__class__, self).set_inCombat(old)
        owner = BigWorld.entity(self.ownerId)
        p = BigWorld.player()
        if owner == p:
            if self.mode != gametypes.SP_MODE_NOATK:
                gameglobal.rds.ui.summonedSpriteUnitFrameV2.updateCombat(self.inCombat)
            if self.inCombat:
                self.updateSpriteTopLogo()
        elif owner:
            if self.inCombat:
                self.updateOhterSpriteTopLogo()

    def enterTopLogoRange(self, rangeDist = -1):
        super(self.__class__, self).enterTopLogoRange(rangeDist)
        owner = BigWorld.entity(self.ownerId)
        p = BigWorld.player()
        if owner == p:
            self.updateSpriteTopLogo()
        elif owner:
            self.updateOhterSpriteTopLogo()

    def resetTopLogo(self):
        super(self.__class__, self).resetTopLogo()
        if not self.inWorld:
            return
        if not hasattr(self, 'ownerId'):
            return
        owner = BigWorld.entity(self.ownerId)
        p = BigWorld.player()
        if owner == p:
            self.updateSpriteTopLogo()
        elif owner:
            self.updateOhterSpriteTopLogo()

    def updateSpriteTopLogo(self):
        if not self.inWorld:
            return
        p = BigWorld.player()
        if not p.isInBfDota() and hasattr(self, 'topLogo') and self.topLogo:
            self.topLogo.hideName(gameglobal.gHideSpriteName)
            if self.inCombat:
                self.topLogo.showBlood(not gameglobal.gHideSpriteBlood)

    def updateOhterSpriteTopLogo(self):
        if not self.inWorld:
            return
        p = BigWorld.player()
        if not p.isInBfDota() and hasattr(self, 'topLogo') and self.topLogo:
            if gameglobal.rds.ui.battleOfFortProgressBar.checkBattleFortNewFlag():
                self.topLogo.hideName(True)
            else:
                self.topLogo.hideName(gameglobal.gHideOtherSpriteName)
            if self.inCombat:
                self.topLogo.showBlood(not gameglobal.gHideOtherSpriteBlood)

    def updateSpriteLockTarget(self):
        if not self.inWorld:
            return
        self.stopUpdateSpriteTarget()
        self.shouldSuggest = True
        if not self.inWorld or self.inFly:
            self.shouldSuggest = False
        p = BigWorld.player()
        if not p.inCombat:
            self.shouldSuggest = False
        if self.shouldSuggest:
            targetId = None
            if p.targetLocked and p.isEnemy(p.targetLocked):
                targetId = p.targetLocked.id
            else:
                minDist = 99999
                for entId in self.ownerAttackTargets:
                    ent = BigWorld.entities.get(entId)
                    if ent:
                        dist = (ent.position - p.position).length
                        if dist < minDist:
                            targetId = entId

            if targetId:
                p.base.spriteMasterLockTgt(targetId)
                gamelog.debug('m.l@SummonedSprite.updateSpriteLockTarget B', targetId)
        if self.ownerAttackTargets:
            self.ownerAttackTargets = []
        self.updateTargetCallback = BigWorld.callback(3, self.updateSpriteLockTarget)

    def addTarget(self, ent):
        if not self.inWorld:
            return
        if self.ownerId != BigWorld.player().id:
            return
        if ent.id not in self.ownerAttackTargets and BigWorld.player().isEnemy(ent):
            self.ownerAttackTargets.append(ent.id)

    def stopUpdateSpriteTarget(self):
        if self.updateTargetCallback:
            BigWorld.cancelCallback(self.updateTargetCallback)
        self.updateTargetCallback = None

    def startSpriteFollowTick(self):
        if not self.inWorld:
            return
        if self.spriteState != spriteFollowState:
            return
        spriteData = SPD.data.get(self.spriteId, {})
        self.suggestNextFollowPos()
        tickDelay = spriteData.get('followNormalTickTime', 0.7)
        if BigWorld.player().isDashing or BigWorld.player().vehicle:
            tickDelay = spriteData.get('followDashTickTime', 0.4)
        self.followTickCallback = BigWorld.callback(tickDelay, self.startSpriteFollowTick)

    def getTheta(self):
        p = BigWorld.player()
        if p.physics.velocity.length > 0:
            if p.physics.velocity[0] < 0:
                if p.physics.velocity[2] < 0:
                    return -135
                if p.physics.velocity[2] == 0:
                    return -90
                if p.physics.velocity[2] > 0:
                    return -45
            elif p.physics.velocity[0] > 0:
                if p.physics.velocity[2] < 0:
                    return 135
                if p.physics.velocity[2] == 0:
                    return 90
                if p.physics.velocity[2] > 0:
                    return 45
            elif p.physics.velocity[0] == 0:
                if p.physics.velocity[2] > 0:
                    return 0
                if p.physics.velocity[2] < 0:
                    return 180
        return 0

    def getNextPlayerPos(self):
        p = BigWorld.player()
        pos = p.position
        theta = self.getTheta()
        v = Math.Vector3(getattr(p.physics, 'velocity', (0, 0, 0)))
        if not v:
            if p.attachSkillData and p.attachSkillData[0]:
                attachEnt = BigWorld.entities.get(p.attachSkillData[0], None)
                if attachEnt and attachEnt.velocity:
                    v = Math.Vector3(attachEnt.velocity)
            elif p.tride.inRide():
                header = BigWorld.entity(p.tride.header)
                if header and header.velocity:
                    v = Math.Vector3(header.velocity)
        if p.vehicle:
            try:
                v += getattr(p.vehicle, 'velocity', Math.Vector3(0, 0, 0))
            except:
                pass

            yRatio = 1
            if v[1] > 0:
                yDelta = 0.6
            pos = pos + (v[0], v[1] * yRatio, v[2])
        velocity = Math.Vector3(v[0], 0, v[2])
        nextPlayerPos = utils.getRelativePosition(pos, p.yaw, theta, min(velocity.length, p.physics.maxVelocity))
        return nextPlayerPos

    def getPreferedTheTaDist(self, followRangeMin, followRangeMax, customFollowPosType, suggestType):
        global THETA_RANGE
        if suggestType == gametypes.SPRITE_SUGGEST_POS_TYPE_FOLLOW:
            if not self.lastFollowTheta or not self.lastFollowDist:
                return (None, None)
            dist = self.lastFollowDist
            minDist = max(dist - (followRangeMax - followRangeMin) / 4.0, followRangeMin)
            maxDist = min(dist + (followRangeMax - followRangeMin) / 4.0, followRangeMax)
            dist = minDist + random.random() * (maxDist - minDist)
            ranges = THETA_RANGE.get(customFollowPosType, (-180, 180))
            theta = self.lastFollowTheta
            minTheta = max(theta - (ranges[1] - ranges[0]) / 4.0, ranges[0])
            maxTheta = min(theta + (ranges[1] - ranges[0]) / 4.0, ranges[1])
            theta = minTheta + random.random() * (maxTheta - minTheta)
            return (theta, dist)
        return (None, None)

    def getNormalSuggestThetaDist(self, followRangeMin, followRangeMax, customFollowPosType):
        dist = followRangeMin + random.random() * (followRangeMax - followRangeMin)
        ranges = THETA_RANGE.get(customFollowPosType, (-180, 180))
        theta = random.randint(ranges[0], ranges[1])
        return (theta, dist)

    def getSuggestPos(self, playerPos, followRangeMin, followRangeMax, customFollowPosType, suggestType = None):
        theta, dist = self.getNormalSuggestThetaDist(followRangeMin, followRangeMax, customFollowPosType)
        if suggestType == gametypes.SPRITE_SUGGEST_POS_TYPE_FOLLOW:
            preferTheta, preferDist = self.getPreferedTheTaDist(followRangeMin, followRangeMax, customFollowPosType, suggestType)
            theta = preferTheta if preferTheta else theta
            dist = preferDist if preferDist else dist
            self.lastFollowTheta = theta
            self.lastFollowDist = dist
        nextSuggestPos = utils.getRelativePosition(playerPos, BigWorld.player().yaw, theta, dist)
        if formula.spaceInHomeRoom(BigWorld.player().spaceNo):
            collidePoint = BigWorld.collide(BigWorld.player().spaceID, self.position, nextSuggestPos)
            if collidePoint:
                direction = Math.Vector3(self.position - collidePoint[0])
                direction.normalise()
                nextSuggestPos = collidePoint[0] - direction * self.bodySize
        return nextSuggestPos

    def getSpriteFollowNextPos(self, playerPos):
        spriteData = SPD.data.get(self.spriteId, {})
        followRangeMin = spriteData.get('followRangeMin', 2)
        followRangeMax = spriteData.get('followRangeMax', 10)
        customFollowPosType = spriteData.get('customFollowPosType', gametypes.SPRITE_FOLLOW_POS_TYPE_RIGHT)
        suggestPos = self.getSuggestPos(playerPos, followRangeMin, followRangeMax, customFollowPosType, suggestType=gametypes.SPRITE_SUGGEST_POS_TYPE_FOLLOW)
        if not self.inFly:
            res = BigWorld.findDropPoint(self.spaceID, Math.Vector3(suggestPos[0], suggestPos[1] + 5, suggestPos[2]))
            if res:
                if abs(res[0][1] - BigWorld.player().position[1]) > 0.4 * BigWorld.player().getModelHeight():
                    return BigWorld.player().position
                suggestPos = res[0]
                suggestPos.y = suggestPos.y + 2
        return suggestPos

    def getSpriteStayPos(self, playerPos):
        spriteData = SPD.data.get(self.spriteId, {})
        followRangeMin = spriteData.get('stayRangeMin', 2)
        followRangeMax = spriteData.get('stayRangeMax', 10)
        customFollowPosType = spriteData.get('customStayPosType', gametypes.SPRITE_FOLLOW_POS_TYPE_RIGHT)
        return self.getSuggestPos(playerPos, followRangeMin, followRangeMax, customFollowPosType)

    def inPreferedPosition(self, playerPos):
        spriteData = SPD.data.get(self.spriteId, {})
        followRangeMin = spriteData.get('followRangeMin', 2)
        followRangeMax = spriteData.get('followRangeMax', 10)
        diffLength = (self.position - playerPos).length
        if diffLength < followRangeMin or diffLength > followRangeMax:
            return False
        p = BigWorld.player()
        diffYaw = utils.adjustDir((self.position - p.position).yaw - p.yaw)
        customFollowPosType = spriteData.get('customFollowPosType', gametypes.SPRITE_FOLLOW_POS_TYPE_RIGHT)
        if customFollowPosType == gametypes.SPRITE_FOLLOW_POS_TYPE_NONE:
            return True
        if customFollowPosType == gametypes.SPRITE_FOLLOW_POS_TYPE_FORWARD:
            if diffYaw < -math.pi / 4 or diffYaw > math.pi / 4:
                return False
        elif customFollowPosType == gametypes.SPRITE_FOLLOW_POS_TYPE_LEFT:
            if diffYaw > -math.pi / 4 or diffYaw < -3 * math.pi / 4:
                return False
        elif customFollowPosType == gametypes.SPRITE_FOLLOW_POS_TYPE_RIGHT:
            if diffYaw < math.pi / 4 or diffYaw > 3 * math.pi / 4:
                return False
        elif customFollowPosType == gametypes.SPRITE_FOLLOW_POS_TYPE_BACK:
            if not (diffYaw < -3 * math.pi / 4 and diffYaw > -math.pi or diffYaw > 3 * math.pi / 4 and diffYaw < math.pi):
                return False
        return True

    def suggestNextFollowPos(self):
        nextPlayerPos = self.getNextPlayerPos()
        if nextPlayerPos:
            nextSuggestPos = self.getSpriteFollowNextPos(nextPlayerPos)
            speed = (nextSuggestPos - self.position).length
            self.lastNextSuggestPos = nextSuggestPos
            BigWorld.player().suggestSpriteMoveToPosNow(nextSuggestPos, speed)

    def stopSpriteFollowTick(self):
        if not self.inWorld:
            return
        if self.followTickCallback:
            BigWorld.cancelCallback(self.followTickCallback)
        self.followTickCallback = None
        self.lastFollowDist = None
        self.lastFollowTheta = None

    def handleAction(self, actionType):
        self.spriteState.handleAction(actionType)

    def getEnterFollowTurnDir(self, turnType):
        if turnType == gametypes.SPRITE_ENTER_FOLLOW_TURN_TYPE_NO:
            return None
        if turnType == gametypes.SPRITE_ENTER_FOLLOW_TURN_TYPE_FACE_PLAYER:
            return self.position - BigWorld.player().position
        if turnType == gametypes.SPRITE_ENTER_FOLLOW_TURN_TYPE_PLAYER_DIR:
            return Math.Vector3(0, 0, BigWorld.player().yaw)

    def anserSpriteFollowEnter(self):
        p = BigWorld.player()
        chatId = None
        spriteData = SPD.data.get(self.spriteId, {})
        chats = spriteData.get('enterFollowChats', [])
        if chats:
            chatIds = [ a[0] for a in chats ]
            probs = [ a[1] for a in chats ]
            chatId = utils.chooseWithProps(chatIds, probs, sum(probs))
            p.chatTextFromSprite(const.SSPRITE_TALK_RANGE_MASTER, self.roleName, self.id, p.roleName, p.gbId, chatId, None)
        if self.fashion._doingActionType == action.EMOTE_ACTION:
            self.fashion.stopAction()
        turnType = spriteData.get('enterFollowTurnType', 0)
        direction = self.getEnterFollowTurnDir(turnType)
        gamelog.debug('m.l@SummonedSprite.anserSpriteFollowEnter', chatId, direction)
        if direction:
            p.base.suggestSpriteTurn(direction)

    def stopFindStayPot(self):
        if not self.inWorld:
            return
        if self.findStayPotCB:
            BigWorld.cancelCallback(self.findStayPotCB)
        self.findStayPotCB = None

    def answerSpriteStayEnter(self):
        spriteData = SPD.data.get(self.spriteId, {})
        delayTime = spriteData.get('spriteFindStyPotDelayTime', 0)
        gamelog.debug('m.l@SummonedSprite.answerSpriteStayEnter', delayTime)
        if delayTime:
            self.findStayPotCB = BigWorld.callback(delayTime, self.findStayPot)
        else:
            self.findStayPot()

    def findStayPot(self):
        if not self.inWorld:
            return
        if self.spriteState != spriteStayState:
            return
        if self.getBornLeftTime() > 0:
            return
        p = BigWorld.player()
        stayPos = self.getSpriteStayPos(p.position)
        spriteData = SPD.data.get(self.spriteId, {})
        gotoStayPosSpeed = spriteData.get('gotoStayPosSpeed', 5)
        gamelog.debug('m.l@SummonedSprite.findStayPot', stayPos, gotoStayPosSpeed)
        p.suggestSpriteMoveToPos(stayPos, gotoStayPosSpeed)
        lingerGapTime = spriteData.get('lingerGapTime', 10)
        self.lingerTickCallback = BigWorld.callback(lingerGapTime, self.startSpriteLingerTick)

    def getSpriteLingerPos(self, playerPos):
        spriteData = SPD.data.get(self.spriteId, {})
        followRangeMin = spriteData.get('lingerRangeMin', 1.5)
        followRangeMax = spriteData.get('lingerRangeMax', 5)
        lingerRangeProb = spriteData.get('lingerRangeProb', 1)
        dist = utils.chooseWithProps([followRangeMin, followRangeMax], [lingerRangeProb, 1], lingerRangeProb + 1)
        customFollowPosType = spriteData.get('customLingerPosType', gametypes.SPRITE_FOLLOW_POS_TYPE_RIGHT)
        return self.getSuggestPos(playerPos, dist, dist, customFollowPosType)

    def lingerToSomewhere(self):
        p = BigWorld.player()
        if self.fashion._doingActionType in (action.BORED_ACTION,
         action.BORN_IDLE_ACTION,
         action.EMOTE_ACTION,
         action.SUMMON_SPRITE_LINGER):
            return
        if p.fashion._doingActionType == action.SOCIAL_ACTION:
            return
        if self.getBornLeftTime() > 0:
            return
        lingerPos = self.getSpriteLingerPos(p.position)
        spriteData = SPD.data.get(self.spriteId, {})
        lingerSpeed = spriteData.get('lingerSpeed', 5)
        p.suggestSpriteMoveEffect(gametypes.SP_SGST_MOVETYPE_FORWARD, lingerPos, lingerSpeed, gametypes.SPRITE_ACTION_TYPE_LINGER)
        gamelog.debug('m.l@SummonedSprite.lingerToSomewhere', lingerPos)

    def startSpriteLingerTick(self):
        if not self.inWorld:
            return
        if self.spriteState != spriteStayState:
            return
        self.lingerToSomewhere()
        spriteData = SPD.data.get(self.spriteId, {})
        lingerStayTime = spriteData.get('lingerGapTime', 8)
        self.lingerTickCallback = BigWorld.callback(lingerStayTime, self.startSpriteLingerTick)

    def stopSpriteLingerTick(self):
        if not self.inWorld:
            return
        if not getattr(self, 'lingerTickCallback', None):
            return
        if self.lingerTickCallback:
            BigWorld.cancelCallback(self.lingerTickCallback)
        self.lingerTickCallback = None

    def getBornLeftTime(self):
        return max(0, getattr(self, 'bornEffEndTime', 0) - utils.getNow())

    def getOwner(self, default = None):
        return BigWorld.entities.get(self.ownerId, self)

    def getModelScale(self):
        if self.model == self.transformModel:
            spriteData = SPD.data.get(self.spriteId, {})
            scale = spriteData.get('transformModelScale', 1)
            val = (scale, scale, scale)
        else:
            val = super(SummonedSprite, self).getModelScale()
        return val

    def set_skinId(self, oldSkinId):
        gamelog.debug('@xzh set_skinId', oldSkinId, self.skinId)
        self.changeSpriteSkinModelSucc()

    def set_dustId(self, oldDustId):
        gamelog.debug('@xzh set_dustId', oldDustId, self.dustId)
        self.playSpriteDustEffect()
