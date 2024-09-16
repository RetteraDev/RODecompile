#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impRide.o
from gamestrings import gameStrings
import BigWorld
import gametypes
import gameglobal
import const
from helpers import action
from helpers import modelServer
from callbackHelper import Functor
from sfx import sfx
from data import equip_data as ED
from data import sys_config_data as SCD
from data import ride_together_data as RTD
from data import emotion_action_data as EAD
import utils

class ImpRide(object):

    def inRiding(self):
        return self.modelServer.state in (modelServer.STATE_HORSE, modelServer.STATE_BEAST)

    def isOnFlyRide(self):
        if self.inRiding():
            return ED.data.get(self.bianshen[1], {}).get('flyRide', False)
        return False

    def isOnSwimRide(self):
        if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            return ED.data.get(self.bianshen[1], {}).get('swimRide', False)
        return False

    def inRidingHorse(self):
        return self.modelServer.state == modelServer.STATE_HORSE

    def inRidingBeast(self):
        return self.modelServer.state == modelServer.STATE_BEAST

    def inModelReplace(self):
        return self.modelServer.state == modelServer.STATE_REPLACE

    def notifyPlayHorseAction(self, spellId, isRoar):
        if self.inRiding() and isRoar:
            actId = self.fashion.getHorseRoarJumpAction()
            if actId:
                self.fashion.playSingleAction(actId, action.IDLE_ACTION)
                if self.inRidingHorse() and self.model and hasattr(self.model, 'ride') and self.model.ride:
                    try:
                        self.model.ride.action(actId)()
                    except:
                        pass

                    self.playRideTogetherAction(actId)
        else:
            ead = EAD.data.get(spellId, {})
            actId = ead.get('startActions', ['1101'])[0]
            self.fashion.stopAllActions()
            self.fashion.playSingleAction(actId, action.HORSE_WHISTLE_ACTION, blend=True)

    def playRideTogetherAction(self, actionId):
        if self.tride.inRide():
            try:
                for key in self.tride.keys():
                    idx = self.tride.get(key)
                    model = self.modelServer.getRideTogetherModelByIdx(idx)
                    if model:
                        act = self.getRideTogetherActionName(actionId, idx)
                        if not getattr(self.modelServer.rideAttached, 'chairIdleAction', None):
                            model.action(act)()

            except:
                pass

    def getRideTogetherActionName(self, actionId, index):
        return actionId + '_' + str(index + 1)

    def inviteeRideTogether(self, mainID, gbId):
        if self.id != BigWorld.player().id:
            return
        else:
            ent = BigWorld.entities.get(mainID)
            if not ent:
                return
            if self.friend and self.friend.get(gbId, None):
                if self.friend[gbId].intimacyLv >= SCD.data.get('rideIntimacyLv', 5):
                    if self.stateMachine.checkStatus(const.CT_MINOR_RIDE):
                        BigWorld.player().cell.acceptInviteRideTogether(mainID)
                        return
            if self.autoCoupleEmote and ent.gbId in self.members.keys():
                BigWorld.player().cell.acceptInviteRideTogether(mainID)
                return
            msgTemplate = SCD.data.get('inviteRideTogetherMsg', gameStrings.TEXT_IMPRIDE_98)
            msg = msgTemplate % ent.roleName
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onInviteeRideTogetherAccept, mainID), noCallback=Functor(self.onInviteeRideTogetherReject, mainID), isModal=False)
            return

    def onInviteeRideTogetherAccept(self, mainID):
        invite = BigWorld.entities.get(mainID)
        if not invite:
            return
        if not self.stateMachine.checkStatus(const.CT_MINOR_RIDE):
            return False
        BigWorld.player().cell.acceptInviteRideTogether(mainID)

    def onInviteeRideTogetherReject(self, mainID):
        BigWorld.player().cell.refuseInviteRideTogether(mainID)

    def applyRideTogether(self, otherId):
        if self.id != BigWorld.player().id:
            return
        ent = BigWorld.entities.get(otherId)
        if not ent:
            return
        msgTemplate = SCD.data.get('applyRideTogetherMsg', gameStrings.TEXT_IMPRIDE_122)
        msg = msgTemplate % ent.roleName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onApplyRideTogetherAccept, otherId), noCallback=Functor(self.onApplyRideTogetherReject, otherId), isModal=False)

    def onApplyRideTogetherAccept(self, otherId):
        if not self.stateMachine.checkStatus(const.CT_MAJOR_RIDE):
            return False
        BigWorld.player().cell.acceptApplyRideTogether(otherId)

    def onApplyRideTogetherReject(self, otherId):
        BigWorld.player().cell.refuseApplyRideTogether(otherId)

    def resetTopLogoSource(self):
        try:
            if hasattr(self, 'isRidingTogether') and self.isRidingTogether():
                header = self.tride.getHeader()
                if header:
                    self.topLogo.gui.source = header.matrix
                else:
                    self.topLogo.gui.source = self.matrix
            elif hasattr(self, 'isInCoupleRideAsRider') and self.isInCoupleRideAsRider():
                other = BigWorld.entity(self.getOtherIDInCoupleEmote())
                if other:
                    self.topLogo.gui.source = other.matrix
                else:
                    self.topLogo.gui.source = self.matrix
            elif hasattr(self, 'inCarrousel') and self.inCarrousel():
                self.topLogo.gui.source = self.modelServer.bodyModel.node('biped Head')
            elif hasattr(self, 'inRoundTable') and self.inRoundTable():
                self.topLogo.gui.source = self.modelServer.bodyModel.node('biped Head')
            elif hasattr(self, 'inInteractiveObject') and self.inInteractiveObject():
                self.topLogo.gui.source = self.modelServer.bodyModel.node('biped Head')
            elif self.isGuildSitInChair():
                self.topLogo.gui.source = self.modelServer.bodyModel.node('biped Head')
            elif self.isCarrierRunning() and self.isOnCarrier():
                self.topLogo.gui.source = self.modelServer.bodyModel.root
                if self.topLogo.guiAni:
                    self.topLogo.guiAni.source = self.modelServer.bodyModel.root
            else:
                self.topLogo.gui.source = self.matrix
                if self.topLogo.guiAni:
                    self.topLogo.guiAni.source = self.matrix
        except:
            pass

    def getTopLogoSource(self):
        if self.isCarrierRunning() and self.isOnCarrier():
            return self.modelServer.bodyModel.root
        return self.matrix

    def resetTopLogo(self):
        if not self.inWorld or not self.model or not self.topLogo:
            return
        h = self.getTopLogoHeight()
        x = 0
        z = 0
        if self.topLogo:
            if hasattr(self, 'isRidingTogether') and self.isRidingTogether() or self.isOnRideTogetherHorse():
                x, h, z = self.getRidingTogetherBias()
            if hasattr(self, 'isInCoupleRideAsRider') and self.isInCoupleRideAsRider():
                x, h, z = self.getCoupleBias()
            if hasattr(self, 'inCarrousel') and self.inCarrousel():
                x, h, z = self.getCarrouselBias()
            if self.isGuildSitInChair():
                x, h, z = self.getGuildSitBias()
            self.topLogo.setHeight(h, x, z)
        if hasattr(self, 'refreshTopLogoName'):
            self.refreshTopLogoName()
        self.resetTopLogoSource()

    def getGuildSitBias(self):
        x = y = z = 0
        return (x, y, z)

    def getCarrouselBias(self):
        x = y = z = 0
        return (x, y, z)

    def getCoupleBias(self):
        x = y = z = 0
        other = BigWorld.entity(self.getOtherIDInCoupleEmote())
        if other and other.inWorld:
            yBias = 0.5 if not other.canFly() else 1.5
            model = self.modelServer.bodyModel
            if model and model.node('biped Head'):
                x = model.node('biped Head').position.x - other.position.x
                y = model.node('biped Head').position.y - other.position.y + yBias
                z = model.node('biped Head').position.z - other.position.z
        return (x, y, z)

    def getRidingTogetherBias(self):
        x = y = z = 0
        main = self.tride.getHeader() if self.tride else self
        try:
            idx = self.tride.get(self.id)
            if not self.tride:
                idx = 0
            flyRide = ED.data.get(main.bianshen[1], {}).get('flyRide', False)
            if not flyRide:
                if self.id == getattr(main, 'id', -1):
                    x, y, z = ED.data.get(main.bianshen[1], {}).get('trideMainTopLogoBias', (0, 5.5, 0))
                else:
                    x, y, z = ED.data.get(main.bianshen[1], {}).get('trideViceTopLogoBias', {1: (0, 5, 0),
                     2: (0.2, 2, 0.2)}).get(idx, (0, 0, 0))
            else:
                inFly = getattr(main, 'inFly', False)
                if not inFly:
                    if self.id == getattr(main, 'id', -1):
                        x, y, z = ED.data.get(main.bianshen[1], {}).get('trideMainTopLogoBias', (0, 5.5, 0))
                    else:
                        x, y, z = ED.data.get(main.bianshen[1], {}).get('trideViceTopLogoBias', {1: (0, 5, 0),
                         2: (0.2, 2, 0.2)}).get(idx, (0, 0, 0))
                elif self.id == getattr(main, 'id', -1):
                    x, y, z = ED.data.get(main.bianshen[1], {}).get('trideFlyMainTopLogoBias', (0, 6.5, 0))
                else:
                    x, y, z = ED.data.get(main.bianshen[1], {}).get('trideFlyViceTopLogoBias', {1: (0, 6, 0),
                     2: (0.2, 6, 0.2)}).get(idx, (0, 0, 0))
        except:
            pass

        return (x, y, z)

    def isOnRideTogetherHorse(self):
        if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            canRideTogether = RTD.data.get(self.bianshen[1], {}).get('canRideTogether', False)
            if canRideTogether:
                return True
        return False

    def getIdByTrideIdx(self, idx):
        if idx == 0:
            header = self.tride.header
            if not header and self.isOnRideTogetherHorse():
                header = self.id
            return header
        else:
            for k, v in self.tride.iteritems():
                if v == idx:
                    return k

            return 0

    def attachFlyTailEffect(self, update = True):
        if self.flyTailEffect in self.attachFx:
            return
        else:
            wingModel = self.modelServer.wingFlyModel.model
            if not wingModel:
                return
            fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             wingModel,
             self.flyTailEffect,
             sfx.EFFECT_LIMIT_MISC,
             -1,
             0,
             True))
            if fxs:
                self.addFx(self.flyTailEffect, fxs)
                for fx in fxs:
                    fx.overCallback(None)

            if update:
                self.updateFlyTailEffect()
            return

    def detachFlyTailEffect(self, effectId):
        info = sfx.gEffectInfoMap.getInfo(effectId)
        if effectId in self.attachFx:
            fxs = self.attachFx.pop(effectId)
            if info:
                nodeInfo = info[0]
                for item in nodeInfo:
                    nodeStr = item[1]
                    node = self.model.node(nodeStr)
                    for fx in fxs:
                        sfx.gEffectMgr.giveBack(effectId, fx, node, sfx.EFFECT_LIMIT_MISC)

    def updateFlyTailEffect(self, forceMove = False):
        inMoving = self.inMoving() or self.isVerticalMoving or forceMove
        fxs = self.attachFx.get(self.flyTailEffect, [])
        if not fxs and self.flyTailEffect and inMoving:
            self.attachFlyTailEffect(False)
        for fx in fxs:
            if inMoving:
                fx.force()
            else:
                fx.stop()

    def set_flyTailEffect(self, old):
        if self.flyTailEffect:
            self.attachFlyTailEffect()
        else:
            self.detachFlyTailEffect(old)

    def hasSharedWingMaxSpeed(self):
        if self.isValidVipProp(gametypes.VIP_SERVICE_SHARE_WING_SPEED):
            return True
        return self.wingShareSpeedExpireTime > utils.getNow()

    def hasSharedRideMaxSpeed(self):
        equip = self.equipment.get(gametypes.EQU_PART_RIDE)
        if equip != const.CONT_EMPTY_VAL and equip.isSwimRide():
            return False
        if self.isValidVipProp(gametypes.VIP_SERVICE_SHARE_RIDE_SPEED):
            return True
        return self.rideShareSpeedExpireTime > utils.getNow()

    def getCompoundWingSpeedSubId(self, inCombat = False):
        if BigWorld.player() != self:
            if inCombat:
                return self.compoundWingSpeedCombatSubId
            else:
                return self.compoundWingSpeedNonCombatSubId
        if self.hasSharedWingMaxSpeed():
            if inCombat:
                return self.maxCombatWingShareSpeed
            else:
                return self.maxNonCombatWingShareSpeed
        it = self.equipment.get(gametypes.EQU_PART_WINGFLY)
        if not it:
            return 0
        return it.getRideWingSpeedId(inCombat)

    def getCompoundRideSpeedSubId(self, inCombat = False):
        if BigWorld.player() != self:
            if inCombat:
                return self.compoundRideSpeedCombatSubId
            else:
                return self.compoundRideSpeedNonCombatSubId
        if self.hasSharedRideMaxSpeed():
            if inCombat:
                return self.maxCombatRideShareSpeed
            else:
                return self.maxNonCombatRideShareSpeed
        it = self.equipment.get(gametypes.EQU_PART_RIDE)
        if not it:
            return 0
        return it.getRideWingSpeedId(inCombat)

    def recalcAvatarSpeed(self):
        self.ap.recalcSpeed()
        self.resetAmActionSpeed()

    def set_rideShareSpeedExpireTime(self, old):
        self.refreshRideShare()

    def refreshRideTemp(self):
        gameglobal.rds.ui.wingAndMount.refreshAll(True)
        if getattr(self, 'rideSpeedTmpTimeCallBack', 0):
            BigWorld.cancelCallback(self.rideSpeedTmpTimeCallBack)
        itemList = []
        rideItem = BigWorld.player().equipment[gametypes.EQU_PART_RIDE]
        itemList.append(rideItem)
        for pos in xrange(0, BigWorld.player().rideWingBag.posCount):
            rideItem = BigWorld.player().rideWingBag.getQuickVal(const.RIDE_WING_BAG_PAGE_RIDE, pos)
            if rideItem:
                itemList.append(rideItem)

        leftTime = self.getItemListLeftTime(itemList)
        if leftTime > 0:
            self.rideSpeedTmpTimeCallBack = BigWorld.callback(leftTime, self.refreshRideSpeedTemp)

    def refreshRideSpeedTemp(self):
        gameglobal.rds.ui.wingAndMount.refreshAll(True)
        self.ap.recalcSpeed()
        self.rideSpeedTmpTimeCallBack = 0
        self.refreshRideTemp()

    def refreshWingTemp(self):
        gameglobal.rds.ui.wingAndMount.refreshAll(True)
        if getattr(self, 'wingSpeedTmpTimeCallBack', 0):
            BigWorld.cancelCallback(self.wingSpeedTmpTimeCallBack)
        itemList = []
        wingItem = BigWorld.player().equipment[gametypes.EQU_PART_WINGFLY]
        itemList.append(wingItem)
        for pos in xrange(0, BigWorld.player().rideWingBag.posCount):
            wingItem = BigWorld.player().rideWingBag.getQuickVal(const.RIDE_WING_BAG_PAGE_WING, pos)
            if wingItem:
                itemList.append(wingItem)

        leftTime = self.getItemListLeftTime(itemList)
        if leftTime > 0:
            self.wingSpeedTmpTimeCallBack = BigWorld.callback(leftTime, self.refreshWingSpeedTemp)

    def getItemListLeftTime(self, itemList):
        leftTime = 0
        for rideItem in itemList:
            speedSwitchExpireTime = getattr(rideItem, 'speedSwitchExpireTime', None)
            if speedSwitchExpireTime:
                nextTime = speedSwitchExpireTime - BigWorld.player().getServerTime()
                if leftTime == 0:
                    if nextTime > 0:
                        leftTime = nextTime
                elif leftTime > nextTime and nextTime > 0:
                    leftTime = nextTime
            else:
                continue

        return leftTime

    def refreshWingSpeedTemp(self):
        self.ap.recalcSpeed()
        self.wingSpeedTmpTimeCallBack = 0
        self.refreshWingTemp()

    def refreshRideShare(self):
        if self == BigWorld.player():
            gameglobal.rds.ui.wingAndMount.refreshAll(True)
            if getattr(self, 'rideSpeedShareTimeCallBack', 0):
                BigWorld.cancelCallback(self.rideSpeedShareTimeCallBack)
            hasTime = getattr(BigWorld.player(), 'rideShareSpeedExpireTime', None)
            vipLeftTime = BigWorld.player().getVipPropLeftTime(gametypes.VIP_SERVICE_SHARE_RIDE_SPEED)
            leftTime = hasTime - BigWorld.player().getServerTime()
            if vipLeftTime > leftTime:
                leftTime = vipLeftTime
            if leftTime > 0:
                self.rideSpeedShareTimeCallBack = BigWorld.callback(leftTime, self.refreshRideSpeed)

    def refreshRideSpeed(self):
        gameglobal.rds.ui.wingAndMount.refreshAll(True)
        self.ap.recalcSpeed()
        self.rideSpeedShareTimeCallBack = 0

    def set_wingShareSpeedExpireTime(self, old):
        self.refreshWingShare()

    def refreshWingShare(self):
        if self == BigWorld.player():
            gameglobal.rds.ui.wingAndMount.refreshAll(True)
            if getattr(self, 'wingSpeedShareTimeCallBack', 0):
                BigWorld.cancelCallback(self.wingSpeedShareTimeCallBack)
            hasTime = getattr(BigWorld.player(), 'wingShareSpeedExpireTime', None)
            vipLeftTime = BigWorld.player().getVipPropLeftTime(gametypes.VIP_SERVICE_SHARE_WING_SPEED)
            leftTime = hasTime - BigWorld.player().getServerTime()
            if vipLeftTime > leftTime:
                leftTime = vipLeftTime
            if leftTime > 0:
                self.wingSpeedShareTimeCallBack = BigWorld.callback(leftTime, self.refreshWingSpeed)

    def refreshWingSpeed(self):
        gameglobal.rds.ui.wingAndMount.refreshAll(True)
        if hasattr(self, 'ap'):
            self.ap.recalcSpeed()
        self.wingSpeedShareTimeCallBack = 0

    def playRiderAction(self, actionId):
        self.modelServer.playRiderAction(actionId)

    def stopRiderAction(self):
        self.modelServer.stopRiderAction()

    def getTRideSpecialAction(self):
        if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            return ED.data.get(self.bianshen[1], {}).get('trideSpecialAction', None)
        else:
            if self.tride.inRide():
                header = self.tride.getHeader()
                if header and header.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                    return ED.data.get(header.bianshen[1], {}).get('trideSpecialAction', None)
            return None
