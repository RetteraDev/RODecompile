#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerSummonSprite.o
import BigWorld
import math
import gameglobal
import gamelog
import gametypes
import logicInfo
import utils
import skillDataInfo
import const
from sfx import flyEffect
from guis import hotkeyProxy
from guis import hotkey
from gameclass import SkillInfo
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import summon_sprite_data as SSPD
from data import skill_general_data as SGD

class ImpPlayerSummonSprite(object):

    def suggestSpriteMoveBack(self):
        if self.summonedSpriteInWorld and not self.summonedSpriteInWorld.inFly:
            spritePos = self.summonedSpriteInWorld.position
            spriteYaw = self.summonedSpriteInWorld.yaw
            direction = self.summonedSpriteInWorld.position - self.position
            SSPData = SSPD.data.get(self.summonedSpriteInWorld.spriteId, {})
            safeDist = SSPData.get('ownerSafeDist', 1.5)
            if direction.length < safeDist:
                diffYaw = utils.adjustDir(direction.yaw - spriteYaw)
                if diffYaw > math.pi / 2 and diffYaw < math.pi or diffYaw > -math.pi and diffYaw < -math.pi / 2:
                    backMoveSpeed = SSPData.get('backMoveSpeed', 2)
                    suggestPos = utils.getRelativePosition(spritePos, spriteYaw, 180, safeDist - direction.length)
                    self.base.suggestSpriteMoveEffect(gametypes.SP_SGST_MOVETYPE_BACKWARD, suggestPos, backMoveSpeed, gametypes.SPRITE_ACTION_TYPE_BACKWARD)
                    gamelog.debug('m.l@ImpPlayerSummonSprite.suggestSpriteMoveBack', suggestPos)

    def suggestSpriteRushStop(self):
        if self.summonedSpriteInWorld and self.summonedSpriteInWorld.spriteState:
            self.summonedSpriteInWorld.spriteState.handleAction(gametypes.SPRITE_STATE_ACTION_TYPE_RUSH_STOP)

    def suggestSpriteFly(self, fly, checkAvatarFly = True):
        if getattr(self, 'suggestFlyCallback', None):
            BigWorld.cancelCallback(self.suggestFlyCallback)
        if self.summonedSpriteInWorld:
            if fly and not self.summonedSpriteInWorld.inFly or not fly and self.summonedSpriteInWorld.inFly:
                self.cell.suggestSpriteFly(fly, checkAvatarFly)
            gamelog.debug('m.l@ImpPlayerSummonSprite.suggestSpriteFly', fly, self.summonedSpriteInWorld.inFly, checkAvatarFly)

    def delaySuggestSpriteFly(self, fly, suggestSpriteFly = True):
        if self.summonedSpriteInWorld:
            if getattr(self, 'suggestFlyCallback', None):
                BigWorld.cancelCallback(self.suggestFlyCallback)
            self.suggestFlyCallback = BigWorld.callback(3, Functor(self.suggestSpriteFly, fly, suggestSpriteFly))

    def suggestOwnerEnterVehicle(self):
        if self.summonedSpriteInWorld:
            if getattr(self, 'suggestLeaveVehicle', None):
                BigWorld.cancelCallback(self.suggestLeaveVehicle)
            self.cell.spriteMasterPlaceOnVehicle(True)

    def delaySuggestOwnerLeaveVehicle(self):
        if self.summonedSpriteInWorld:
            if getattr(self, 'suggestLeaveVehicle', None):
                BigWorld.cancelCallback(self.suggestLeaveVehicle)
            self.suggestLeaveVehicle = BigWorld.callback(3, Functor(self.cell.suggestSpriteFly, False, True))

    def suggestSpriteMoveToPos(self, nextPos, speed):
        if self.summonedSpriteInWorld:
            self.base.suggestSpriteMove(gametypes.SP_SGST_MOVETYPE_FORWARD, nextPos, speed)
            gamelog.debug('m.l@ImpPlayerSummonSprite. suggestSpriteMoveToPos', nextPos, speed)

    def suggestSpriteMoveToPosNow(self, nextPos, speed):
        if self.summonedSpriteInWorld:
            if self.summonedSpriteInWorld.inFly:
                self.base.suggestSpriteMove(gametypes.SP_SGST_MOVETYPE_FORWARD_NOW, nextPos, speed)
            else:
                self.base.suggestSpriteMove(gametypes.SP_SGST_MOVETYPE_NAVIGATE, nextPos, speed)

    def suggestSpriteMoveEffect(self, moveType, tgtPos, speed, effectId):
        if self.summonedSpriteInWorld:
            self.base.suggestSpriteMoveEffect(moveType, tgtPos, speed, effectId)
            gamelog.debug('m.l@ImpPlayerSummonSprite.suggestSpriteMoveEffect', moveType, tgtPos, speed, effectId)

    def suggestSpriteClientEffect(self, effectType, effectId):
        if self.summonedSpriteInWorld:
            self.base.suggestSpriteClientEffect(effectType, effectId)
            gamelog.debug('m.l@ImpPlayerSummonSprite.suggestSpriteClientEffect')

    def suggestSpriteTeleportToMe(self):
        if self.summonedSpriteInWorld:
            spriteData = SSPD.data.get(self.summonedSpriteInWorld.spriteId, {})
            teleportDist = spriteData.get('teleportDist', 1.5)
            suggestPos = utils.getRelativePosition(self.position, self.yaw, 90, teleportDist)
            self.base.suggestSpriteMoveEffect(gametypes.SP_SGST_MOVETYPE_TELEPORT, suggestPos, 0, 0)
            BigWorld.callback(0.1, Functor(self.summonedSpriteInWorld.playSuggetActionEffct, gametypes.SPRITE_ACTION_TYPE_TELEPORT_BACK))
            gamelog.debug('m.l@ImpPlayerSummonSprite.suggestSpriteTeleportToMe', suggestPos)

    def spriteTeleportBack(self, isDown):
        if not isDown:
            return
        if not gameglobal.rds.configData.get('enableSummonedSprite', False):
            return
        nextTime = logicInfo.spriteTeleportSkillCoolDown
        if nextTime and utils.getNow() < nextTime:
            self.showGameMsg(GMDD.data.SPRITE_TELEPORT_IN_CD, ())
            return
        if self.summonedSpriteInWorld and self.inCombat:
            BigWorld.player().base.useSpriteBackSkill()
        else:
            BigWorld.player().suggestSpriteTeleportToMe()
        gameglobal.rds.ui.summonedSpriteUnitFrameV2.playTeleportActived()
        gamelog.debug('m.l@ImpPlayerSummonSprite.spriteTeleportBack')

    def spriteUseManualSkill(self, isDown):
        if not isDown:
            return
        if not gameglobal.rds.configData.get('enableSummonedSprite', False):
            return
        if not self.summonedSpriteInWorld:
            return
        if self.summonedSpriteInWorld.mode == gametypes.SP_MODE_NOATK:
            return
        nextTime = logicInfo.spriteManualSkillCoolDown
        if nextTime and utils.getNow() < nextTime:
            self.showGameMsg(GMDD.data.SPRITE_MANUAL_SKILL_IN_CD, ())
            return
        awakeSkill = utils.getAwakeSkillBySprite()
        gamelog.debug('m.l@ImpPlayerSummonSprite.spriteUseManualSkill', awakeSkill)
        p = BigWorld.player()
        if self.spriteBattleIndex and awakeSkill:
            famiEfflv = p.summonSpriteList[self.spriteBattleIndex].get('props', {}).get('famiEffLv', 1)
            lv = utils.getEffLvBySpriteFamiEffLv(famiEfflv, 'awake', const.DEFAULT_SKILL_LV_SPRITE)
            skillInfo = SkillInfo(awakeSkill, lv)
            skillDataInfo.checkTargetRelationRequest(skillInfo, True, checkSprite=True)
            if SGD.data.get((awakeSkill, lv), {}).get('isCheckSpriteCollide', 0):
                targetId = self.summonedSpriteInWorld.targetId
                if not targetId and self.targetLocked and hasattr(self.targetLocked, 'id'):
                    targetId = self.targetLocked.id
                tgt = BigWorld.entities.get(targetId)
                if tgt and flyEffect._checkCollide(self.summonedSpriteInWorld.position, tgt.position):
                    self.showGameMsg(GMDD.data.SPRITE_TARGET_HAS_COLLIDE, ())
                    return
        if awakeSkill:
            p.base.useSpriteAwakeSkill()
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.playManualSkillActived()

    def getSpriteTeleportHKDesc(self):
        _, _, hotKeyDesc = hotkeyProxy.getKeyContent(hotkey.KEY_SPRITE_TELEPORT_BACK)
        return hotKeyDesc

    def getSpriteManualSkillHKDesc(self):
        _, _, hotKeyDesc = hotkeyProxy.getKeyContent(hotkey.KEY_SPRITE_MANUAL_SKILL)
        return hotKeyDesc

    def getSpriteTeleportHKBriefDesc(self):
        _, _, hotKeyDesc = hotkeyProxy.getKeyBriefContent(hotkey.KEY_SPRITE_TELEPORT_BACK)
        return hotKeyDesc

    def getSpriteManualSkillHKBriefDesc(self):
        _, _, hotKeyDesc = hotkeyProxy.getKeyBriefContent(hotkey.KEY_SPRITE_MANUAL_SKILL)
        return hotKeyDesc

    def onUseActionBarSpriteItem(self, index, spriteId):
        """
        \xe7\x8e\xa9\xe5\xae\xb6\xe6\x8c\x89\xe4\xb8\x8b\xe5\xbf\xab\xe6\x8d\xb7\xe6\xa0\x8f\xe7\x9a\x84\xe6\x88\x98\xe7\x81\xb5\xe6\x97\xb6
        :param index: \xe6\x88\x98\xe7\x81\xb5index
        :param spriteId:\xe6\x88\x98\xe7\x81\xb5id
        """
        spriteInfo = self.summonSpriteList.get(index)
        if spriteInfo:
            if index in self.summonedSpriteLifeList:
                self.showGameMsg(GMDD.data.SUMMONED_SPRITE_CALLOUT_DEAD_FAIL, ())
            elif utils.getSpriteBattleState(index):
                self.showGameMsg(GMDD.data.SUMMONED_SPRITE_CALLOUT_FAIL_IN_BATTLE, ())
            else:
                gameglobal.rds.ui.summonedWarSpriteMine.callOutSprite(index)
        else:
            self.showGameMsg(GMDD.data.SUMMONED_SPRITE_CALLOUT_FAILED, ())

    def clearChangeToFollowCB(self):
        if self.changeToFollowStateCB:
            BigWorld.cancelCallback(self.changeToFollowStateCB)
            self.changeToFollowStateCB = None

    def spriteChangeToFollow(self, source = None):
        if self.summonedSpriteInWorld:
            moveChangeToFollowDelay = SCD.data.get('spriteMoveChangeToFollowDelay', 0.5)
            if source == gametypes.SPRITE_MOVE_CHANGE_TO_FOLLOW_TYPE_DASH:
                moveChangeToFollowDelay = SCD.data.get('spriteMoveChangeToFollowDashDelay', 0)
                self.clearChangeToFollowCB()
                gamelog.debug('m.l@PlayerAvatar.spriteChangeToFollow dash', moveChangeToFollowDelay)
            self.changeToFollowStateCB = BigWorld.callback(moveChangeToFollowDelay + self.summonedSpriteInWorld.getBornLeftTime(), self.summonedSpriteInWorld.changeToFollowState)

    def spriteOwnerMoving(self, isMoving):
        if self.summonedSpriteInWorld:
            if self.vehicle and not isMoving:
                return
            if isMoving:
                self.spriteChangeToFollow()
            else:
                self.suggestSpriteMoveBack()
                self.clearChangeToFollowCB()
                self.summonedSpriteInWorld.changeToStayState()
