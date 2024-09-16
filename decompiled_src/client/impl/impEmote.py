#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impEmote.o
from gamestrings import gameStrings
import BigWorld
import Math
import gameglobal
import gametypes
import const
import random
import gamelog
import utils
import commcalc
import clientcom
from callbackHelper import Functor
from helpers import weaponModel
from helpers import action
from helpers import tintalt as TA
from sfx import fireworks
from sfx import sfx
from guis import ui
from guis import uiConst
from helpers import blackEffectManager
from data import emote_data as ED
from data import couple_emote_data as CED
from data import couple_emote_basic_data as CEBD
from data import fireworks_effect_data as FWED
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD

class ImpEmote(object):
    FRIENDNESS_LIMIT = 1000

    def doItemEmote(self, emoteId, vpage, vpos):
        self.emoteItemPage = vpage
        self.emoteItemPos = vpos
        self.doEmote(emoteId)

    def doEmote(self, emoteId, callback = None):
        data = ED.data.get(int(emoteId))
        if data:
            eType = data.get('type')
            funcType = data.get('funcType', 0)
            blackEff = data.get('blackEff', 0)
            if eType == const.EMOTE_TYPE_EMOTION:
                if self.topLogo:
                    self.topLogo.showEmote(emoteId)
            elif eType in (const.EMOTE_TYPE_ACTION, const.EMOTE_TYPE_PHOTO):
                if funcType == uiConst.EMOTE_FUNTYPE_WEAR:
                    self.doWearEmote(emoteId)
                    return
                if funcType == uiConst.EMOTE_FUNTYPE_EFFECT_CONNECT:
                    self.doEffectConnectEmote(emoteId)
                    return
                if funcType == uiConst.EMOTE_FUNTYPE_YUANLING:
                    self.doWearEmote(emoteId, 'yuanLing')
                    return
                actionId = data.get('res')
                actionId2 = data.get('res2')
                if actionId:
                    schoolActionId = str(self.school) + '_' + actionId
                    if schoolActionId in self.fashion.getActionNameList():
                        actionId = schoolActionId
                if actionId2:
                    schoolActionId2 = str(self.school) + '_' + actionId2
                    if schoolActionId2 in self.fashion.getActionNameList():
                        actionId2 = schoolActionId2
                modelId = self.fashion.modelID
                effect = data.get('effect', {}).get(modelId, ())
                self.switchWeaponState(gametypes.WEAPON_HANDFREE, True)
                self.fashion.disableFootIK(True)
                self.fashion.stopAllActions()
                if self.fashion.isPlayer:
                    self.modelServer.poseManager.stopPoseModel()
                actType = action.SOCIAL_ACTION if eType == const.EMOTE_TYPE_ACTION else action.PHOTO_ACTION
                seq = [(actionId,
                  effect,
                  actType,
                  0,
                  1.0,
                  None)]
                if actionId2:
                    seq.append((actionId2,
                     effect,
                     actType,
                     0,
                     1.0,
                     None))
                self.fashion.playActionWithFx(seq, actType, Functor(self.emoteActionDone, callback))
                attachItem = data.get('item', {}).get(modelId, ())
                if attachItem:
                    socialActionModel = self.modelServer.socialActionModel
                    socialActionModel.equipItem(attachItem)
                    if socialActionModel.state == weaponModel.ATTACHED:
                        self.modelServer.socialActionModel.detach()
                    socialActionModel.attach(self.model, haveAct=True)
                if getattr(self, 'actionCallback', 0):
                    BigWorld.cancelCallback(self.actionCallback)
                    self.actionCallback = 0
                if data.get('duration') and hasattr(self, 'emoteItemPage'):
                    self.actionCallback = BigWorld.callback(data.get('duration'), Functor(self.cell.useItemAfterEmote, self.emoteItemPage, self.emoteItemPos))
                if utils.instanceof(self, 'PlayerAvatar') and blackEff:
                    self.setBlackScreenEff(blackEffectManager.SRC_EMOTE, True)
            elif eType == const.EMOTE_TYPE_COUPLE_EMOTION:
                if not self.isInCoupleRide():
                    return
                res = data.get('res')
                if not res:
                    return
                self.playCoupleEmotionAction(res)
            elif eType == const.EMOTE_TYPE_RIDE:
                actionId = data.get('res')
                self.playRiderAction(actionId)
            elif eType == const.EMOTE_TYPE_WUHUN:
                self._showWuhunEffect()
            elif eType == const.EMOTE_TYPE_FACE:
                self.startFaceEmoteById(emoteId)
                duration = data.get('duration', 4)
                BigWorld.callback(duration, self.faceEmoteTimeOut)
            if self == BigWorld.player() and self.targetLocked and getattr(self.targetLocked, 'IsAvatar', False):
                self.faceTo(self.targetLocked, True)

    def doWearEmote(self, emoteId, wearName = 'headdress'):
        data = ED.data.get(int(emoteId))
        entId = self.lockedId
        ent = BigWorld.entity(entId)
        if not ent or not getattr(ent, 'IsAvatar', False) or not ent.inWorld:
            return
        if not clientcom.isCoupleWear(getattr(self.aspect, wearName), getattr(ent.aspect, wearName)):
            return
        actionId = data.get('res')
        actionId2 = data.get('res2')
        seq = []
        if actionId:
            seq.append(actionId)
        if actionId2:
            seq.append(actionId2)
        seq.append('1101')
        getattr(self.modelServer, wearName).doActions(seq)
        getattr(ent.modelServer, wearName).doActions(seq)

    def doEffectConnectEmote(self, emoteId):
        data = ED.data.get(int(emoteId))
        entId = self.lockedId
        ent = BigWorld.entity(entId)
        if not ent or not getattr(ent, 'IsAvatar', False) or not ent.inWorld:
            return
        elif not clientcom.isCoupleWear(self.aspect.facewear, ent.aspect.facewear):
            return
        else:
            self.faceTo(ent)
            effect = data.get('effect', None)
            if effect and self.model and ent.model:
                startNode = self.model.node('HP_face')
                endNode = ent.model.node('HP_face')
                if startNode and endNode:
                    distance = SCD.data.get('EMOTE_EFFECT_CONNECT_DIST', 5)
                    self.wearEffectConnect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (self.getSkillEffectLv(),
                     startNode,
                     effect,
                     endNode,
                     distance,
                     self.getSkillEffectPriority()))
                    ent.wearEffectConnect = self.wearEffectConnect
            return

    def beDoEmote(self, targetId, emoteId):
        data = ED.data.get(emoteId, {})
        eType = data.get('type')
        funcType = data.get('funcType', 0)
        ent = BigWorld.entity(targetId)
        if not ent or not getattr(ent, 'IsAvatar', False) or not ent.inWorld:
            return
        self.showGameMsg(GMDD.data.DO_EMTOE_TO_YOU, (ent.roleName, data.get('name', '')))
        if funcType == uiConst.EMOTE_FUNTYPE_EFFECT_CONNECT:
            if not clientcom.isCoupleWear(self.aspect.facewear, ent.aspect.facewear):
                return
            self.faceTo(ent)

    def _showWuhunEffect(self, showMsg = True):
        if not self.isRealModel:
            return
        opaVal = self.getOpacityValue()[0]
        if opaVal in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        effectId = self.realAspect.wuHun
        if effectId:
            fresnelColorInfo = SCD.data.get('WU_HUN_FRESNEL_INFO', {}).get(self.school, [])
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             effectId,
             sfx.EFFECT_LIMIT,
             gameglobal.EFFECT_LAST_TIME))
            if fresnelColorInfo:
                color, time = fresnelColorInfo
                weaponModel = self.modelServer._getAllWeaponModel()
                models = []
                for weapon in weaponModel:
                    models.extend(weapon.getModels())

                TA.ta_addGaoLiang(models, color, time + 5)
                BigWorld.callback(time, self.endWuhunEffect)
        elif showMsg:
            self.showGameMsg(GMDD.data.SHEN_BING_NO_EQUIP, ())

    @ui.callFilter(6, False)
    def showWuhunEffect(self, showMsg = True):
        self._showWuhunEffect(showMsg)

    def endWuhunEffect(self):
        if not self.inWorld:
            return
        weaponModel = self.modelServer._getAllWeaponModel()
        models = []
        for weapon in weaponModel:
            models.extend(weapon.getModels())

        TA.ta_delGaoLiang(models)

    def emoteActionDone(self, callback = None):
        if utils.instanceof(self, 'PlayerAvatar'):
            self.setBlackScreenEff(blackEffectManager.SRC_EMOTE, False)
        if self.modelServer.socialActionModel.state == weaponModel.ATTACHED:
            self.modelServer.socialActionModel.detach()
        if callback:
            callback()

    def emoteActionCancel(self):
        if utils.instanceof(self, 'PlayerAvatar'):
            self.setBlackScreenEff(blackEffectManager.SRC_EMOTE, False)
        self.emoteActionDone()
        if getattr(self, 'actionCallback', 0):
            BigWorld.cancelCallback(self.actionCallback)
            self.actionCallback = 0

    def playCoupleEmotionAction(self, res):
        other = BigWorld.entity(self.getOtherIDInCoupleEmote())
        if self.coupleEmote[2] == self.id:
            man = other
            woman = self
        else:
            man = self
            woman = other
        if not man or not woman:
            return
        else:
            coupleKye = man.getCoupleKey()
            if not coupleKye:
                return
            key = list(coupleKye)
            key.append(int(res))
            coupleEmoteData = CED.data.get(tuple(key), {})
            actionId = coupleEmoteData.get('socialAction')
            beActionId = coupleEmoteData.get('socialBeAction')
            if man.canFly() or woman.canFly():
                actionId = coupleEmoteData.get('socialActionInFly')
                beActionId = coupleEmoteData.get('socialBeActionInFly')
            if actionId and beActionId:
                man.fashion.playSingleAction(actionId, action.SOCIAL_ACTION)
                playSeq = [beActionId]
                man.fashion.playActionSequence(man.modelServer.coupleModel, playSeq, None)
            return

    @ui.callFilter(1, True)
    def wantToDoEmote(self, emoteId):
        ed = ED.data.get(emoteId, {})
        eType = ed.get('type')
        funcType = ed.get('funcType', 0)
        gscdIndex = ed.get('gscdIndex', 0)
        if gscdIndex:
            gameglobal.rds.ui.skill.slotUseSkill(4, gscdIndex)
            return
        if not gameglobal.rds.ui.emote.checkEmotePlay(emoteId):
            self.showGameMsg(GMDD.data.COUPLE_EMOTE_NO_FIT_EQUIP, ())
            return
        if funcType == uiConst.EMOTE_FUNTYPE_COUPLE_EMOTE and eType == const.EMOTE_TYPE_ACTION:
            coupleEmoteId = int(ED.data.get(emoteId, {}).get('res', 0))
            if not coupleEmoteId:
                coupleEmoteId = gametypes.COUPLE_EMOTE_TYPE_PRINCESS_HUG
            self.applyForCoupleEmote(coupleEmoteId)
        else:
            if eType == const.EMOTE_TYPE_ACTION:
                if not self.stateMachine.checkStatus(const.CT_SOCIAL_ACTION):
                    return
                if funcType in (uiConst.EMOTE_FUNTYPE_WEAR, uiConst.EMOTE_FUNTYPE_YUANLING):
                    ent = self.targetLocked
                    if not ent or not getattr(ent, 'IsAvatar', False) or not ent.inWorld:
                        return
                    partName = 'headdress' if funcType == uiConst.EMOTE_FUNTYPE_WEAR else 'yuanLing'
                    if not clientcom.isCoupleWear(getattr(self.aspect, partName, 0), getattr(ent.aspect, partName, 0)):
                        self.showGameMsg(GMDD.data.NOT_MATCHED_WEAR, ())
                        return
                if funcType == uiConst.EMOTE_FUNTYPE_EFFECT_CONNECT:
                    ent = self.targetLocked
                    if not ent or not getattr(ent, 'IsAvatar', False) or not ent.inWorld:
                        return
                    if not clientcom.isCoupleWear(self.aspect.facewear, ent.aspect.facewear):
                        self.showGameMsg(GMDD.data.NOT_MATCHED_WEAR, ())
                        return
                    distance = SCD.data.get('EMOTE_EFFECT_CONNECT_DIST', 5)
                    if (self.position - ent.position).length > distance:
                        self.showGameMsg(GMDD.data.WEAR_EMOTE_OUT_OF_DIST, ())
                        return
            elif eType == const.EMOTE_TYPE_COUPLE_EMOTION:
                if not self.stateMachine.checkStatus(const.CT_COUPLE_EMOTION):
                    return
                coupleKey = self.getCoupleKey()
                if coupleKey and coupleKey[0] in (gameglobal.COUPLE_SEX_MAN_MAN, gameglobal.COUPLE_SEX_WOMAN_WOMAN):
                    if utils.isAbilityOn() and not self.getAbilityData(gametypes.ABILITY_JIN_LAN):
                        self.showGameMsg(GMDD.data.COUPLE_EMOTE_KISS_SAME_SEX_NOT_ALLOWED, ())
                        return
            else:
                if eType == const.EMOTE_TYPE_WUHUN:
                    self.wantToShowWuhunEffect(emoteId)
                    return
                if eType == const.EMOTE_TYPE_RIDE:
                    if not self.stateMachine.checkStatus(const.CT_EMOTE_RIDE_ACTION):
                        return
                elif eType == const.EMOTE_TYPE_FACE:
                    if gameglobal.rds.ui.emote.isFaceEmoteExpire(int(emoteId)):
                        return
                    if not self.stateMachine.checkStatus(const.CT_FACE_EMOTE):
                        return
                elif eType == const.EMOTE_TYPE_PHOTO:
                    if not self.stateMachine.checkStatus(const.CT_PHOTO_ACTION):
                        return
                elif eType == const.EMOTE_TYPE_EMOTION:
                    if not self.stateMachine.checkStatus(const.CT_TOPLOGO_EMOTE_ACTION):
                        return
            self.cell.doEmote(int(emoteId))

    @ui.callFilter(6, False)
    def wantToShowWuhunEffect(self, emoteId):
        if not self.realAspect.wuHun:
            self.showGameMsg(GMDD.data.SHEN_BING_NO_EQUIP, ())
        else:
            self.cell.doEmote(int(emoteId))

    def isInCoupleEmote(self, data = None):
        if data is None:
            emoteInfo = getattr(self, 'coupleEmote', (0, 0, 0))
            if len(emoteInfo) == 0:
                return 0
        else:
            emoteInfo = data
        if self.id == emoteInfo[1]:
            return 1
        elif self.id == emoteInfo[2]:
            return 2
        else:
            return 0

    def getOtherIDInCoupleEmote(self, data = None):
        if data is None:
            data = getattr(self, 'coupleEmote', (0, 0, 0))
        if len(data) == 0:
            return 0
        state = self.isInCoupleEmote(data)
        if not state:
            return 0
        elif data is not None:
            return data[3 - state]
        else:
            return self.coupleEmote[3 - state]

    def coupleRequest(self, emoteId, who, friendness):
        ent = BigWorld.entities.get(who)
        if not ent:
            return
        if self.inFightForLoveFb() and self.gbId in self.fightForLoveResult.values() and ent.gbId in self.fightForLoveResult.values():
            self.onCoupleEmoteAccept(emoteId, who)
            return
        gamelog.info('@szh coupleRequest', who, friendness, self.autoCoupleEmote, ent.gbId)
        if self.autoCoupleEmote and ent.gbId in self.members.keys():
            self.onCoupleEmoteAccept(emoteId, who)
            return
        if gameglobal.REFUSE_COUPLE_EMOTE_APPLY:
            BigWorld.player().cell.rejectCoupleEmote(emoteId, who, True)
            return
        cebd = CEBD.data.get(emoteId, {})
        friendnessLimit = cebd.get('friendnessLimit', ImpEmote.FRIENDNESS_LIMIT)
        if friendness > friendnessLimit:
            BigWorld.player().cell.acceptCoupleEmote(emoteId, who)
            return
        coupleEmoteRequestMsg = SCD.data.get('coupleEmoteRequestMsg', gameStrings.TEXT_IMPEMOTE_394)
        emoteName = cebd.get('name', '')
        msg = coupleEmoteRequestMsg % (ent.roleName, emoteName)
        if self.showCoupleEmoteRequest:
            gameglobal.rds.ui.messageBox.dismiss(self.showCoupleEmoteRequest)
        self.showCoupleEmoteRequest = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onCoupleEmoteAccept, emoteId, who), noCallback=Functor(self.onCoupleEmoteReject, emoteId, who), isModal=False)

    def onCoupleEmoteReject(self, emoteId, hugId):
        BigWorld.player().cell.rejectCoupleEmote(emoteId, hugId, False)

    def onCoupleEmoteAccept(self, emoteId, hugId):
        BigWorld.player().cell.acceptCoupleEmote(emoteId, hugId)

    def coupleEmoteApplyAcceptedForBebug(self, hugId):
        pass

    def coupleEmoteApplyAccepted(self, emoteId, beHugId):
        BigWorld.callback(0.1, Functor(self._coupleEmoteApplyAccepted, emoteId, beHugId))

    def _coupleEmoteApplyAccepted(self, emoteId, beHugId):
        gameStrings.TEXT_IMPEMOTE_414
        beHug = BigWorld.entities.get(beHugId)
        if not beHug or not beHug.inWorld:
            return
        if not self.stateMachine.checkCoupleEmote(emoteId, beHugId):
            return
        targetYaw = (beHug.position - self.position).yaw
        dist = (beHug.position - self.position).length - 0.8
        destPos = Math.Vector3(utils.getRelativePosition(self.position, targetYaw, 0, dist))
        BigWorld.player().ap.seekPath(destPos, Functor(self.onArriveBeHug, emoteId, beHugId, destPos, beHug.position))

    def onArriveBeHug(self, emoteId, beHugId, destPos, beHugPos, status):
        BigWorld.player().ap.forwardMagnitude = 0
        BigWorld.player().ap.updateVelocity()
        BigWorld.player().cell.doCoupleEmote(emoteId, beHugId, beHugPos)

    def coupleEmoteApplyCanceled(self, hugId):
        BigWorld.player().ap.ccamera.target = BigWorld.player().matrix
        if self.showCoupleEmoteRequest:
            gameglobal.rds.ui.messageBox.dismiss(self.showCoupleEmoteRequest)

    def doFullScreenMsg(self, srcName, giftId, giftNum):
        gameglobal.rds.ui.familiarFireworks.show(srcName, giftId, giftNum)

    def doFullScreenFireworks(self, fireworksId):
        gameglobal.rds.ui.fullScreenFirework.show(fireworksId)

    def doFireworks(self, fireworksId, previewDuration):
        if not self.inWorld:
            return
        elif self.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE, gameglobal.OPACITY_HIDE_WITHOUT_NAME):
            return
        elif BigWorld.player().isBlockFirework():
            return
        else:
            data = FWED.data.get(fireworksId, {})
            attachType = data.get('attachType', 0)
            if not attachType:
                return
            previewFireworksFxs = []
            if attachType == gameglobal.FIREWORKS_TYPE_BODY:
                effects = data.get('effects', ())
                if not effects:
                    return
                needRandom = data.get('needRandom', None)
                effectIds = [random.choice(effects)] if needRandom else effects
                height = data.get('height', 0)
                duration = data.get('duration', 5)
                if previewDuration > 0:
                    duration = min(duration, previewDuration)
                for effectId in effectIds:
                    fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                     self.getBasicEffectPriority(),
                     self.model,
                     effectId,
                     sfx.EFFECT_LIMIT_MISC,
                     duration))
                    if not fxs:
                        continue
                    for fx in fxs:
                        if not fx:
                            continue
                        fx.bias = (0, height, 0)
                        if previewDuration > 0:
                            previewFireworksFxs.append(fx)

            else:
                positions = data.get('position', ())
                if positions:
                    for pos in positions:
                        fw = fireworks.Launcher.getObjByPostion(fireworksId, self.id, previewDuration, pos)
                        fw.launch()

                else:
                    fw = fireworks.Launcher.getObj(fireworksId, self.id, previewDuration)
                    fw.launch()
            if previewDuration > 0:
                if hasattr(self, 'previewFireworksFxs'):
                    for fx in self.previewFireworksFxs:
                        if fx and hasattr(fx, 'stop'):
                            fx.stop()

                self.previewFireworksFxs = previewFireworksFxs
            return

    def changeZonePriority(self, skyboxName, weight):
        if self == BigWorld.player():
            BigWorld.setZonePriority(skyboxName, weight)

    def flashNotice(self, flashNum, soundId):
        if self == BigWorld.player():
            if flashNum:
                BigWorld.flashWindow(flashNum)
            if soundId:
                gameglobal.rds.sound.playSound(soundId)

    def getGuildConnectNode(self, ent, key):
        nodeName = GCD.data.get('guildConnectEndNode', 'Scene Root')
        node = None
        try:
            node = ent.model.node(nodeName)
            if not node:
                node = ent.model.node('Scene Root')
        except:
            pass

        return node

    def releaseGuildConnectEffect(self, guildConnectEffect, soloEffs):
        gameglobal.removeGuildConnectorEffect(guildConnectEffect, soloEffs)
        if guildConnectEffect:
            guildConnectEffect.release()
            guildConnectEffect = None
        if soloEffs:
            for ef in soloEffs:
                if ef:
                    ef.stop()

            soloEffs = None

    def playGuildConnectEffect(self, entId, duration):
        target = BigWorld.entities.get(entId, None)
        if not target:
            return
        else:
            if gameglobal.isGuildConnectFull():
                if self == BigWorld.player() or target == BigWorld.player():
                    pass
                else:
                    return
            soloEffs = []
            startNode = self.getGuildConnectNode(self, 'guildConnectStartNode')
            endNode = self.getGuildConnectNode(target, 'guildConnectEndNode')
            effs = GCD.data.get('guildConnectEffs', [2317])
            if not effs or not startNode or not endNode:
                return
            idx = getattr(self, 'guildActivityIcon', 10000) // 10000 - 1
            if idx < 0:
                return
            connEff = effs[idx]
            guildConnectEffect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (self.getSkillEffectLv(),
             startNode,
             connEff,
             endNode,
             80,
             self.getSkillEffectPriority()))
            soloEffIds = GCD.data.get('guildSoloEffs', [2318])
            soloEffId = soloEffIds[idx]
            effLv = self.getSkillEffectLv()
            effPrior = self.getBasicEffectLv()
            ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effLv,
             effPrior,
             self.model,
             soloEffId,
             sfx.EFFECT_LIMIT_MISC,
             duration))
            if ef:
                soloEffs.extend(ef)
            ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effLv,
             effPrior,
             target.model,
             soloEffId,
             sfx.EFFECT_LIMIT_MISC,
             duration))
            if ef:
                soloEffs.extend(ef)
            gameglobal.cacheGuildConnectorEffect(guildConnectEffect, soloEffs)
            self.guildConnectEffectCB = BigWorld.callback(duration, Functor(self.releaseGuildConnectEffect, guildConnectEffect, soloEffs))
            return

    def clearAllGuildConnector(self):
        gameglobal.clearGuildConnector()

    def transformFaceEmote(self, faceEmote):
        gamelog.debug('@hjx face emote#transformFaceEmote:', faceEmote)
        self.faceEmoteExpire = faceEmote

    def getEmoteEnableFlags(self, emoteId):
        return commcalc.getBit(self.emoteEnableFlags, emoteId)

    def syncCoupleEmoteSkillCD(self, skillCDInfo):
        self.cpEmoteSkillCD = skillCDInfo

    def getSocialEmoteEnableFlags(self, emoteId):
        return commcalc.getBit(self.socialEmoteEnableFlags, emoteId)
