#Embedded file name: I:/bag/tmp/tw2/res/entities\client/MultiplayMovingPlatform.o
import BigWorld
import gameglobal
import gamelog
import gametypes
import const
from helpers import action
from sfx import sfx
from MovingPlatform import MovingPlatform
from data import multi_carrier_data as MCD
from data import sys_config_data as SYSCD

class MultiplayMovingPlatform(MovingPlatform):

    def __init__(self):
        super(MultiplayMovingPlatform, self).__init__()
        self.satisfactinEffect = []

    def enterWorld(self):
        super(MultiplayMovingPlatform, self).enterWorld()

    def getBoredActionNames(self):
        carrierData = MCD.data.get(self.multiCarrierNo, {})
        return carrierData.get('satisfactionBordAction', {}).get(self.carrierSatisfaction, [])

    def use(self):
        p = BigWorld.player()
        if self.isValidUse():
            carrierData = MCD.data.get(self.multiCarrierNo, {})
            triggerStates = carrierData.get('triggerArgs', {})
            for key, value in triggerStates.iteritems():
                triggerType = key[0]
                triggerId = key[1]
                fkey = value[1]
                if triggerType == gametypes.PLATFORM_TRIGGER_TYPE_STATE:
                    if p.hasState(triggerId):
                        p.cell.applyTiggerCarrierNearby()
                        gamelog.debug('-----m.l@MultiplayMovingPlatform.use trigger', triggerType, triggerId, fkey)
                        return
                if triggerType == gametypes.PLATFORM_TRIGGER_TYPE_ZAIJU:
                    if p.bianshen[1] == triggerId:
                        p.cell.applyTiggerCarrierNearby()
                        gamelog.debug('-----m.l@MultiplayMovingPlatform.use trigger', triggerType, triggerId, fkey)
                        return

            if p.carrier.isNoneState():
                maxPlaceNum = MCD.data.get(self.multiCarrierNo, {}).get('maxPlaceNum', 0)
                if not maxPlaceNum:
                    return
                if maxPlaceNum != const.MULTI_CARRIER_SINGLE_NUM and p.id == p.groupHeader:
                    multiCarrierReadyConfirmMsg = SYSCD.data.get('multiCarrierReadyConfirmMsg', '您将发起队伍就位确认?')
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(multiCarrierReadyConfirmMsg, yesCallback=lambda : p.cell.applyCreateCarrier(self.id))
                else:
                    p.cell.applyCreateCarrier(self.id)
                gamelog.debug('-----m.l@MultiplayMovingPlatform.use leader', self.id)
            elif p.carrier.isReadyState() and not p.carrier.get(p.id):
                p._comfirmInviteCheckCarrierReady()
                gamelog.debug('-----m.l@MultiplayMovingPlatform.use member')
            elif p.carrier.isRunningState() and not p.carrier.get(p.id):
                selectedNodeUI = MCD.data.get(self.multiCarrierNo, {}).get('selectedNodeUI', 0)
                if selectedNodeUI:
                    gameglobal.rds.ui.multiCarrierNodeSelect.show()
                else:
                    BigWorld.player().cell.applyEnterCarrier()
                gamelog.debug('-----m.l@MultiplayMovingPlatform.use running goback')
            gamelog.debug('-----m.l@MultiplayMovingPlatform.use no call')

    def set_isSuspended(self, old):
        gamelog.debug('m.l@MultiplayMovingPlatform.set_isSuspended', old, self.isSuspended, BigWorld.player().id)
        self.resetPlayerGoSkillShine()

    def set_isNearbyPlayerEnough(self, old):
        gamelog.debug('m.l@MultiplayMovingPlatform.set_isNearbyPlayerEnough', old, self.isNearbyPlayerEnough, BigWorld.player().id)
        self.resetPlayerGoSkillShine()

    def resetPlayerGoSkillShine(self):
        p = BigWorld.player()
        if self.isSuspended and self.isNearbyPlayerEnough:
            if p.carrier.isRunningState() and p.carrier.carrierEntId == self.id and p.carrier.has_key(p.id):
                gameglobal.rds.ui.zaijuV2.showPauseShine(True)
            else:
                gameglobal.rds.ui.zaijuV2.showPauseShine(False)
        else:
            gameglobal.rds.ui.zaijuV2.showPauseShine(False)

    def resetCaps(self):
        carrierData = MCD.data.get(self.multiCarrierNo, {})
        satisfactionCaps = carrierData.get('satisfactionCaps', {}).get(self.carrierSatisfaction, [1, 10])
        self.am.matchCaps = list(satisfactionCaps)

    def getTopLogoSource(self):
        carrierData = MCD.data.get(self.multiCarrierNo, {})
        topLogoNode = carrierData.get('topLogoNode', None)
        source = self.matrix
        try:
            source = self.model.node(topLogoNode)
        except:
            gamelog.error('m.l@MultiplayMovingPlatform.getTopLogoSource node error', topLogoNode)

        return source

    def resetTopLogo(self):
        if not self.inWorld or not self.topLogo:
            return
        super(MultiplayMovingPlatform, self).resetTopLogo()
        if self.topLogo.gui:
            self.topLogo.gui.source = self.getTopLogoSource()
        if self.topLogo.guiAni:
            self.topLogo.guiAni.source = self.getTopLogoSource()

    def getTopLogoHeight(self):
        return MCD.data.get(self.multiCarrierNo, {}).get('heightOffset', 0.1)

    def playActions(self, actNames):
        if type(actNames) != tuple or len(actNames) < 1:
            return
        if not self.fashion:
            return
        self.fashion.stopAction()
        self.fashion.playAction(list(actNames), action.EMOTE_ACTION)

    def chatToView(self, msgId, duration = const.POPUP_MSG_SHOW_DURATION):
        if not self.inWorld:
            return
        super(MultiplayMovingPlatform, self).chatToView(msgId, duration)

    def playSound(self, soundId):
        if not self.inWorld:
            return
        BigWorld.player().playSound(soundId, self.position)

    def releaseSatisfactinEffect(self):
        for eff in self.satisfactinEffect:
            if eff:
                eff.stop()

        self.satisfactinEffect = []

    def playSatisfactinEffect(self):
        carrierData = MCD.data.get(self.multiCarrierNo, {})
        satisfactionEff = carrierData.get('satisfactionEffs', {}).get(self.carrierSatisfaction, None)
        if satisfactionEff:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             self.model,
             satisfactionEff,
             sfx.EFFECT_LIMIT,
             -1))
            if fx:
                self.satisfactinEffect.extend(fx)

    def resetSatisfactinEffect(self):
        self.releaseSatisfactinEffect()
        self.playSatisfactinEffect()

    def set_carrierSatisfaction(self, old):
        self.resetCaps()
        self.resetSatisfactinEffect()

    def set_carrier(self, old):
        self.refreshCarrier()

    def refreshCarrier(self):
        if self.carrier:
            for entId, index in self.carrier.iteritems():
                ent = BigWorld.entities.get(entId)
                if not ent or not ent.inWorld:
                    return
                ent.modelServer.enterCarrier()

    def hasTrigger(self):
        p = BigWorld.player()
        carrierData = MCD.data.get(self.multiCarrierNo, {})
        triggerStates = carrierData.get('triggerArgs', {})
        for key, value in triggerStates.iteritems():
            triggerType = key[0]
            triggerId = key[1]
            if triggerType == gametypes.PLATFORM_TRIGGER_TYPE_STATE:
                if p.hasState(triggerId):
                    return True
            if triggerType == gametypes.PLATFORM_TRIGGER_TYPE_ZAIJU:
                if p.bianshen[1] == triggerId:
                    return True

        return False

    def getFKey(self):
        p = BigWorld.player()
        carrierData = MCD.data.get(self.multiCarrierNo, {})
        triggerStates = carrierData.get('triggerArgs', {})
        for key, value in triggerStates.iteritems():
            triggerType = key[0]
            triggerId = key[1]
            fkey = value[1]
            if triggerType == gametypes.PLATFORM_TRIGGER_TYPE_STATE:
                if p.hasState(triggerId):
                    return fkey
            if triggerType == gametypes.PLATFORM_TRIGGER_TYPE_ZAIJU:
                if p.bianshen[1] == triggerId:
                    return fkey

        return super(MultiplayMovingPlatform, self).getFKey()

    def playEffect(self, effectId, targetPos = None, pitch = 0, yaw = 0, roll = 0, maxDelayTime = -1, scale = 1.0):
        model = self.model
        model.entityId = self.id
        if targetPos is None:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             model,
             effectId,
             sfx.EFFECT_LIMIT,
             maxDelayTime))
        else:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             model,
             effectId,
             sfx.EFFECT_LIMIT,
             targetPos,
             pitch,
             yaw,
             roll,
             maxDelayTime))
        if fx:
            for fxItem in fx:
                fxItem.scale(scale, scale, scale)

    def afterModelFinish(self):
        super(MultiplayMovingPlatform, self).afterModelFinish()
        self.resetCaps()
        self.resetSatisfactinEffect()
        if self.carrier.isRunningState():
            for entId, idx in self.carrier.iteritems():
                ent = BigWorld.entities.get(entId, None)
                if ent and ent.inWorld:
                    ent.modelServer.enterCarrier()

    def leaveWorld(self):
        super(MultiplayMovingPlatform, self).leaveWorld()
        if self.carrier:
            carrierEntId = self.carrier.carrierEntId
            carrierEnt = BigWorld.entities.get(carrierEntId, None)
            for eId, idx in self.carrier.iteritems():
                ent = BigWorld.entities.get(eId)
                if ent and ent.inWorld:
                    ent.modelServer.leaveCarrier(carrierEnt)

        self.satisfactinEffect = []

    def checkTrapCallback(self):
        carrierData = MCD.data.get(self.multiCarrierNo, {})
        if len(self.carrier) >= carrierData.get('maxPlaceNum', 0):
            if not self.hasTrigger():
                return True
        return super(MultiplayMovingPlatform, self).checkTrapCallback()

    def getOpacityValue(self):
        if self.isMarriage():
            return (gameglobal.OPACITY_FULL, True)
        if not self.isValidUse() and gameglobal.gHideOtherPlayerFlag == gameglobal.HIDE_DEFINE_SELF:
            return (gameglobal.OPACITY_HIDE, False)
        return super(MultiplayMovingPlatform, self).getOpacityValue()
