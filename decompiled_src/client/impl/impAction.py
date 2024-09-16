#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impAction.o
import BigWorld
import Sound
import gameglobal
import gametypes
import const
import gamelog
import utils
import commQuest
import clientcom
import commcalc
import gameconfigCommon
from helpers.scenario import Scenario
from helpers import tintalt
from helpers import action
from helpers import action as ACT
from helpers import cellCmd
from sfx import sfx
from callbackHelper import Functor
from guis import uiUtils
from guis import uiConst
from helpers import black
from data import emotion_action_data as EAD
from data import scenario_data as SCND
from data import physics_config_data as PCD
from data import sys_config_data as SYSCD
from data import teleport_spell_data as TSD
from data import emote_data as ED
from data import equip_data as EQD
from data import foot_dust_data as FDD
from data import zaiju_data as ZJD
from cdata import game_msg_def_data as GMDD

class ImpAction(object):

    def prepareForProgress(self, isStart = True):
        if isStart:
            self.oldWeaponState = self.weaponState
            self.weaponState = gametypes.WEAPON_HANDFREE
            self.modelServer.refreshWeaponStateWithAct(False)
            self.weaponState = self.oldWeaponState
        else:
            self.modelServer.refreshWeaponStateWithAct(False)

    def startActionProgress(self, period, spellID, objId, isForce, yaw, equipId):
        gamelog.debug('jorsef: Avatar#startActionProgress', period, spellID, objId, isForce, equipId)
        self.isDoingAction = True
        self.prepareForProgress(True)
        self.spellTargetId = objId
        self._startActionProgress(period, spellID, objId, isForce, yaw)
        if equipId:
            self.modelServer.lifeSkillModel.equipItem(equipId)
        else:
            self.modelServer.lifeSkillModel.release()

    def _startActionProgress(self, period, spellID, objId, isForce, yaw):
        if not self.inWorld:
            return
        else:
            tempGroupFollowSpellId = SYSCD.data.get('tempGroupFollowSpellId', ())
            if utils.instanceof(self, 'PlayerAvatar') and spellID in tempGroupFollowSpellId:
                self.checkTempGroupFollow()
            ead = EAD.data.get(spellID, {})
            if ead and self.inWorld:
                model = self.model
                if self.inRiding() and hasattr(self.model, 'ride'):
                    model = self.model.ride
                actions = []
                startActions = ead.get('startActions', ())
                if startActions:
                    actions.extend(startActions)
                loopActions = ead.get('loopActions', ())
                if loopActions:
                    actions.extend(loopActions)
                playSeq = []
                spellEff = list(ead.get('spellEff', []))
                loopEff = list(ead.get('loopEff', []))
                tintEffect = ead.get('tint', None)
                for i, act in enumerate(actions):
                    scaleKey = clientcom.getAvatarWeaponModelScale(self)
                    effSizeScale = ead.get(scaleKey, 1.0)
                    if i == 0:
                        playSeq.append((act,
                         spellEff,
                         action.PROGRESS_SPELL_ACTION,
                         0,
                         1,
                         tintEffect,
                         effSizeScale))
                    else:
                        playSeq.append((act,
                         loopEff,
                         action.PROGRESS_SPELL_ACTION,
                         0,
                         1,
                         tintEffect,
                         effSizeScale))

                ignoreAction = ead.get('ignoreAction', False)
                if not ignoreAction:
                    self.fashion.stopAction()
                    self.fashion.playActionWithFx(playSeq, action.PROGRESS_SPELL_ACTION, None, False, priority=self.getSkillEffectPriority())
                if self.modelServer.wingFlyModel:
                    model = self.modelServer.wingFlyModel.model
                    if model and model.inWorld:
                        model.action('21101')()
                bubble = ead.get('bubbleMsg')
                if bubble:
                    msg = uiUtils.parseBubbleMsg(bubble[0])
                    chatToView = ead.get('chatToView', 0)
                    if chatToView:
                        if self == BigWorld.player():
                            self.cell.chatToView(msg + ':role', bubble[1])
                    else:
                        self.popupMsg(self.id, msg, bubble[1])
                emoteId = ead.get('emoteId')
                if emoteId and ED.data.get(emoteId, {}).get('type') == const.EMOTE_TYPE_EMOTION:
                    self.doEmote(emoteId)
            return

    def set_inSpellAction(self, old):
        if self.inSpellAction:
            ead = EAD.data.get(self.inSpellAction, {})
            self.spellScale = ead.get('modelScale', 1)
            showModel = ead.get('showModel', 0)
            if showModel:
                self.refreshRealModelState()
        else:
            self.spellScale = 1
        self.refreshModelScale()

    def endActionProgress(self, success, oldSpellID):
        gamelog.debug('endActionProgress')
        self.isDoingAction = False
        if self.actionProgressCallback:
            BigWorld.cancelCallback(self.actionProgressCallback)
            self.actionProgressCallback = None
        self._endActionProgress(success, oldSpellID)

    def _endActionProgress(self, success, oldSpellID):
        if not self.inWorld:
            return
        gamelog.debug('_endActionProgress', success, oldSpellID)
        ead = EAD.data.get(oldSpellID, {})
        self.spellScale = 1
        if ead and self.inWorld and self.model:
            if self.life != gametypes.LIFE_DEAD:
                model = self.model
                if self.inRiding():
                    if hasattr(self.model, 'ride'):
                        model = self.model.ride
                endActions = ead.get('endActions', ())
                if self.fashion.doingActionType() not in (action.FALLEND_ACTION,
                 action.JIDAO_START_ACTION,
                 action.JIDAO_LOOP_ACTION,
                 action.JIDAO_STOP_ACTION):
                    self.fashion.stopAction()
                if success and endActions:
                    self.fashion.playAction(endActions, ACT.PICK_END_ACTION, self._afterEndActionProgress)
                    BigWorld.callback(0, Functor(self.qinggongMgr.playWingFlyModelAction, endActions))
                else:
                    self._afterEndActionProgress()
                if self.fashion.boredAct:
                    self.fashion.stopActionByName(model, self.fashion.boredAct)

    def _afterEndActionProgress(self):
        if not self.inWorld:
            return
        self.refreshModelScale()
        self._detachLifeSkillEquip()
        self.prepareForProgress(False)
        self.refreshWeaponVisible()
        if self.stateModelScale:
            for key, value in self.stateModelScale.items():
                if type(value) == tuple and len(value) == 2 and type(value[0]) == str:
                    self.clientStateEffect.addModelScale(key)

        self.clientStateEffect.restoreBufActState()

    def _detachLifeSkillEquip(self):
        if not self.modelServer.lifeSkillModel.isDetached():
            self.modelServer.lifeSkillModel.detach()

    def stopRollAction(self):
        if self != BigWorld.player():
            self.fashion.stopAllActions()

    def playSound(self, soundId, position):
        gamelog.debug('@szh: playSound ', soundId)
        gameglobal.rds.sound.playSound(soundId, self, position=position)

    def setMusicParam(self, param, value):
        Sound.setMusicParam(param, value)

    def isInPlayScenarioWithGroupSingleEsc(self):
        if hasattr(self, 'inScriptFlag') and self.inScriptFlag:
            return True
        return False

    def isInPlayScenario(self):
        if hasattr(self, 'realInScriptFlag') and self.realInScriptFlag:
            return True
        return False

    def isTeammateInPlayScenarioWithGroupSingleEsc(self):
        p = BigWorld.player()
        for memberData in p.members.itervalues():
            entId = memberData['id']
            if p.id == entId:
                continue
            ent = BigWorld.entity(entId)
            if ent and ent.isInPlayScenarioWithGroupSingleEsc():
                return True

        return False

    def scenarioStopPlay(self):
        scenarioIns = Scenario.PLAY_INSTANCE if Scenario.PLAY_INSTANCE else Scenario.INSTANCE
        if scenarioIns and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.QUIT_SCENARIO_PLAY, ())
            scenarioIns.stopPlay()

    def scenarioPlay(self, scenName, scenarioFun = 0):
        scenarioId = 0
        expBonus = 0
        storyPoint = 0
        secondEsc = 0
        for tscenarioId, data in SCND.data.iteritems():
            if data.get('name') == scenName and data.get('secondEsc'):
                secondEsc = 1
                scenarioId = tscenarioId
                break
            elif data.get('name') == scenName and data.get('questId'):
                questId = data.get('questId')
                expBonus, _, _, _ = commQuest.calcReward(self, questId)
                expBonus = int(expBonus * data.get('multi', 0))
                storyPoint = data.get('storyPoint', 0)
                scenarioId = tscenarioId
                break

        if scenarioFun == gametypes.SCENARIO_PALY_FINISH_FUN_TYPE0:
            if scenarioId and storyPoint:
                self._scenarioPlay(scenName, scenarioId, lambda : self.onQuestPlayScenario(scenarioId), ('quest', expBonus))
            elif scenarioId and secondEsc:
                self._scenarioPlay(scenName, scenarioId, lambda : self.onSecondEscPlayScenario(scenarioId))
            else:
                self._scenarioPlay(scenName, scenarioId)
        elif scenarioFun == gametypes.SCENARIO_PALY_FINISH_FUN_TYPE1:
            self._scenarioPlay(scenName, scenarioId, lambda : self.countDownPlayFunctor())

    def _scenarioPlay(self, scenName, scenarioId = 0, finishCallback = None, finishCallbackFor = None, copyForActor = None, notHideEnt = []):
        if gameglobal.rds.GameState == gametypes.GS_LOADING and self.inFuben():
            BigWorld.player().cell.scenarioGroupEsc()
            return
        if self.inGroupFollow and gameconfigCommon.enableCallTeamMember():
            BigWorld.player().cell.scenarioGroupEsc()
            return
        scen = Scenario.getInstanceInPlay()
        scen.scenarioId = scenarioId
        isSucc = scen.loadScript(scenName, False)
        if isSucc is True:
            scen.play(finishCallback=finishCallback, finishCallbackFor=finishCallbackFor, copyForActor=copyForActor, notHideEnt=notHideEnt)
        else:
            gamelog.debug('@szh: scen does not exist', scenName)

    def countDownPlayFunctor(self):
        black.fade(0, 1, 0.1)
        gameglobal.rds.ui._doReturnToLogin()

    def partnerScenarioPlay(self):
        copyAct = []
        ents = BigWorld.entities.items()
        if self.partner:
            for eid, e in ents:
                gbId = getattr(e, 'gbId', None)
                if gbId in self.partner:
                    copyAct.append(e)
                if len(copyAct) >= len(self.partner):
                    break

            copyAct.sort(key=lambda k: self.partner.get(k.gbId, {}).get('orderIndex', 0))
        name = 'jieban%s.xml' % str(len(self.partner))
        self._scenarioPlay(name, finishCallback=self.partnerScenarioPlayCallBack, copyForActor=copyAct)

    def partnerScenarioPlayCallBack(self):
        pass

    def marriageScenarioPlay(self):
        if self.marriageBeInvitedInfo and self.inMarriageHall():
            copyAct = []
            ents = BigWorld.entities.items()
            wifeGbId = self.marriageBeInvitedInfo.get('wifeGbId', 0)
            hunsbandGbId = self.marriageBeInvitedInfo.get('hunsbandGbId', 0)
            for eid, e in ents:
                gbId = getattr(e, 'gbId', None)
                if gbId == wifeGbId or gbId == hunsbandGbId:
                    copyAct.append(e)

            name = 'jiehun.xml'
            if len(copyAct) == const.MARRIAGE_PEOPLE_NUM:
                beginTime = utils.getNow()
                self._scenarioPlay(name, finishCallback=Functor(self.marriageScenarioPlayCallBack, beginTime), copyForActor=copyAct)
            else:
                self.marriageScenarioPlayCallBack(None)

    def marriageScenarioPlayCallBack(self, beginTime):
        if not beginTime:
            return
        else:
            endTime = utils.getNow()
            gfeInst = getattr(gameglobal.rds, 'gfe', None)
            if gfeInst:
                gfeInst.takeVideoByMarriageScenario(-(endTime - beginTime - 1) * 1000, 0)
            return

    def marriageAmericanScenarioPlay(self):
        if self.marriageBeInvitedInfo and self.inMarriageHall():
            marriageAct = []
            ents = BigWorld.entities.items()
            wifeGbId = self.marriageBeInvitedInfo.get('wifeGbId', 0)
            hunsbandGbId = self.marriageBeInvitedInfo.get('hunsbandGbId', 0)
            for eid, e in ents:
                gbId = getattr(e, 'gbId', None)
                if gbId == wifeGbId or gbId == hunsbandGbId:
                    marriageAct.append(e)

            name = 'xshl.xml'
            beginTime = utils.getNow()
            self._scenarioPlay(name, finishCallback=Functor(self.marriageAmericanScenarioPlayCallBack, beginTime), notHideEnt=marriageAct)

    def marriageAmericanScenarioPlayCallBack(self, beginTime):
        endTime = utils.getNow()
        gfeInst = getattr(gameglobal.rds, 'gfe', None)
        if gfeInst:
            gfeInst.takeVideoByMarriageScenario(-(endTime - beginTime - 1) * 1000, 0)

    def marriageGreatScenarioPlay(self):
        if self.marriageBeInvitedInfo and self.inMarriageHall():
            copyAct = []
            ents = BigWorld.entities.items()
            wifeGbId = self.marriageBeInvitedInfo.get('wifeGbId', 0)
            hunsbandGbId = self.marriageBeInvitedInfo.get('hunsbandGbId', 0)
            for eid, e in ents:
                gbId = getattr(e, 'gbId', None)
                if gbId == wifeGbId or gbId == hunsbandGbId:
                    copyAct.append(e)

            name = 'sshl_zx.xml'
            if len(copyAct) == const.MARRIAGE_PEOPLE_NUM:
                beginTime = utils.getNow()
                self._scenarioPlay(name, finishCallback=Functor(self.marriageGreatScenarioPlayCallBack, beginTime), copyForActor=copyAct)
                if self.gbId == wifeGbId or self.gbId == hunsbandGbId:
                    BigWorld.callback(uiConst.MARRIAGE_WEAR_RING_TIME, self.wearRingMomentFunc)
            else:
                self.marriageGreatScenarioPlayCallBack(None)

    def fightForLoveScenarioPlay(self, createrGbId, winnerGbId):
        if self.inFightForLoveFb():
            copyAct = []
            ents = BigWorld.entities.items()
            for eid, e in ents:
                gbId = getattr(e, 'gbId', None)
                if gbId == winnerGbId:
                    copyAct.append(e)
                if gbId == createrGbId:
                    copyAct.insert(0, e)

            name = 'bwzq_nv3_na3.xml'
            if len(copyAct) == 2:
                beginTime = utils.getNow()
                for ent in copyAct:
                    if ent and ent.inWorld and ent.topLogo:
                        ent.topLogo.removeFFLScore()

                self._scenarioPlay(name, finishCallback=Functor(self.fightForLoveScenarioPlayCallBack, copyAct), notHideEnt=copyAct)
                BigWorld.callback(const.FFL_SCENARIO_SCREENSHOT_DELAY, Functor(gameglobal.rds.ui.camera.onTakePhoto, True))
                BigWorld.callback(const.FFL_SCENARIO_TXT_DELAY, gameglobal.rds.ui.fightForLoveScenarioTxt.show)
            else:
                self.fightForLoveScenarioPlayCallBack([])

    def fightForLoveScenarioPlayCallBack(self, copyAct):
        self.unlockKey(gameglobal.KEY_FIGHT_FOR_LOVE)
        gameglobal.rds.ui.fightForLoveScenarioTxt.hide()
        for ent in copyAct:
            if ent and ent.inWorld:
                ent.refreshToplogoTitle()

    def wearRingMomentFunc(self):
        self.pauseScenarioInEvent()
        gameglobal.rds.ui.marryRing.show()

    def pauseScenarioInEvent(self):
        scen = Scenario.getInstanceInPlay()
        if scen:
            scen.pausePlayInEvent()

    def continuePlayScenario(self):
        scen = Scenario.getInstanceInPlay()
        if scen:
            scen.continuePlay(False, True)

    def marriageGreatScenarioPlayCallBack(self, beginTime):
        self.cell.marriageGreatPledgeOk()
        if not beginTime:
            return
        else:
            endTime = utils.getNow()
            gfeInst = getattr(gameglobal.rds, 'gfe', None)
            if gfeInst:
                gfeInst.takeVideoByMarriageScenario(-(endTime - beginTime - 1) * 1000, 0)
            return

    def onQuestPlayScenario(self, scenarioId):
        gameglobal.rds.ui.scenarioBox.dismiss()
        self.cell.onQuestPlaySenario(scenarioId)

    def onSecondEscPlayScenario(self, scenarioId):
        self.base.onSecondEscPlayScenario(scenarioId)

    def canSecondEsc(self, scen):
        if not scen:
            return False
        if not scen.scenarioId:
            return False
        if SCND.data.get(scen.scenarioId, {}).get('secondEsc') and commcalc.getBit(self.secondEscPlayScenarioFlag, scen.scenarioId):
            return True
        return False

    def getEscMsg(self, scen):
        if not scen:
            return GMDD.data.SCENARIO_NOT_ESCAPE
        if not scen.scenarioId:
            return GMDD.data.SCENARIO_NOT_ESCAPE
        if SCND.data.get(scen.scenarioId, {}).get('secondEsc'):
            return GMDD.data.SCENARIO_SECOND_ESCAPE
        return GMDD.data.SCENARIO_NOT_ESCAPE

    def modelDelTint(self, entityId, part, func):
        gamelog.debug('zt: modelDelTint', entityId, part, func)
        if not part:
            part = None
        entity = BigWorld.entities.get(entityId)
        if entity is not None and entity.model is not None:
            if part and getattr(entity.model, part, None) or part == None:
                tintalt.ta_del([entity.model], func, part)

    def motionPin(self):
        pass

    def motionUnpin(self):
        pass

    def __checkActionNeedType(self):
        for act in self.model.queue:
            if act in self.fashion.getAlphaBeHitActions():
                return action.S_BLEND

        if self.fashion._doingActionType in (action.CAST_ACTION,
         action.ATTACK_ACTION,
         action.AFTERMOVESTOP_ACTION,
         action.MOVING_ACTION,
         action.GUIDE_ACTION,
         action.GUIDESTOP_ACTION,
         action.MOVINGSTOP_ACTION,
         action.COUPLE_EMOTE_NORMAL_ACTION,
         action.CAST_MOVING_ACTION,
         action.FISHING_ACTION,
         action.SPELL_ACTION,
         action.STARTSPELL_ACTION,
         action.FISHING_READY_ACTION,
         action.CASTSTOP_ACTION,
         action.HORSE_WHISTLE_ACTION,
         action.WING_FLY_UP_ACTION,
         action.WING_FLY_DOWN_ACTION):
            return action.S_BLEND
        if self.fashion._doingActionType in (action.UNKNOWN_ACTION,
         action.IDLE_ACTION,
         action.BORED_ACTION,
         action.ROLLSTOP_ACTION,
         action.FALLEND_ACTION,
         action.STANDUP_ACTION,
         action.PICK_ITEM_ACTION,
         action.BEHIT_ACTION,
         action.WING_LAND_TO_FLY_ACTION,
         action.CHARGE_START_ACTION,
         action.CHARGE_ACTION,
         action.CHAT_ACTION,
         action.PICK_END_ACTION,
         action.LEAVE_HORSE_END_ACTION,
         action.DA_ZUO_ACTION,
         action.WING_TAKE_OFF_ACTION,
         action.MAN_DOWN_START_ACTION,
         action.MAN_DOWN_STOP_ACTION,
         action.DASH_START_ACTION,
         action.FAST_DOWN_ACTION,
         action.SOCIAL_ACTION,
         action.WING_LAND_END_ACTION,
         action.SOCIAL_ACTION,
         action.SHOW_WEAPON_ACTION,
         action.HANG_WEAPON_ACTION,
         action.RUN_TO_IDEL_ACTION,
         action.NORMAL_READY_ACTION,
         action.PROGRESS_SPELL_ACTION,
         action.PICK_END_ACTION,
         action.APPRENTICE_TRAIN_END_ACTION,
         action.TELEPORT_SPELL_ACTION,
         action.PHOTO_ACTION,
         action.PET_ACTION):
            return action.S_BREAK
        return action.S_SLIDE

    def jumpActionEnableAlpha(self):
        movingType = self.__checkActionNeedType()
        if movingType == action.S_BLEND or getattr(self.skillPlayer, 'castLoop', None):
            seq = self.fashion.playedAction.get(self.fashion.actionKey, None)
            if seq != None and seq.active == True and seq.blend:
                for i in seq.action:
                    i.enableAlpha(True)

    def _checkNeedPlayStartAction(self, moveSpeed):
        if gameglobal.gDisablePlayStartAction:
            return False
        if not self.fashion.isPlayer:
            return False
        if self.bufActState:
            return False
        if self.ap.rightwardMagnitude and self.ap.leftwardMagnitude:
            return False
        if moveSpeed > self.ap.runFwdSpeed + 0.5:
            return False
        if self.startMovingTime - self.endMovingTime < gameglobal.NEEDPLAYSTARTACTION:
            return False
        if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            if self.fashion._doingActionType == action.RUN_TO_IDEL_ACTION or self.ap.backwardMagnitude:
                return False
        if self.fashion._doingActionType not in [action.UNKNOWN_ACTION, action.CASTSTOP_ACTION, action.RUN_TO_IDEL_ACTION]:
            return False
        if self.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            return ZJD.data.get(self.bianshen[1], {}).get('enableMoveStart', False)
        if not self.stateMachine.checkStatus(const.CT_PLAY_STARTACTION):
            return False
        return True

    def _checkNeedPlayRunToIdel(self):
        if self == BigWorld.player():
            if self.backMove:
                self.fashion.setIdleType(gametypes.IDLE_TYPE_NORMAL)
                return False
        if gameglobal.gDisablePlayStartAction:
            return False
        if not self.fashion.isPlayer:
            return False
        if self.vehicle:
            return False
        if self.endMovingTime - self.startMovingTime < gameglobal.NEEDPLAYSTARTACTION:
            return False
        if BigWorld.time() - self.lastStopMoveTime < 1:
            return False
        if self.fashion.doingActionType() != action.UNKNOWN_ACTION:
            return False
        if self.bufActState:
            return False
        if not self.stateMachine.checkStatus(const.CT_PLAY_STARTACTION):
            return False
        return True

    def isMoveChanged(self, isMoving, vertical):
        if vertical:
            if isMoving:
                if self.isMoving:
                    return False
                else:
                    return True
            elif self.isMoving:
                return False
            else:
                return True

        elif isMoving:
            if self.isVerticalMoving:
                return False
            else:
                return True
        else:
            if self.isVerticalMoving:
                return False
            return True

    def verticalMoveNotifier(self, isVerticalMove):
        self.isVerticalMoving = isVerticalMove
        self.refreshWingHorseIdleEffect()
        self.updateFlyTailEffect()
        if self.qinggongState not in gametypes.QINGGONG_STATE_WINGFLY_SET:
            if self.isMoveChanged(isVerticalMove, True):
                self.refreshHorseWingEffect(True)

    def playStartToRun(self):
        try:
            if self.ap.rightwardMagnitude:
                self.endMovingTime = self.startMovingTime
                StartToRunRightAction = self.fashion.getStartToRunRightAction()
                if StartToRunRightAction:
                    self.model.action(StartToRunRightAction)()
            elif self.ap.leftwardMagnitude:
                self.endMovingTime = self.startMovingTime
                StartToRunLeftAction = self.fashion.getStartToRunLeftAction()
                if StartToRunLeftAction:
                    self.model.action(StartToRunLeftAction)()
            else:
                StartToRunAction = self.fashion.getStartToRunAction()
                if StartToRunAction:
                    self.playActionWithRider(StartToRunAction, 0, None, 1)
        except Exception as e:
            gamelog.debug('m.l@playStartToRun', e.message)

    def playActionWithRider(self, actionName, actionType, callback, withMove = 0):
        if actionName:
            try:
                self.fashion.playSingleAction(actionName, actionType, 0, callback, withMove)
                if hasattr(self.model, 'ride') and self.model.ride:
                    self.model.ride.action(actionName)()
                self.playRideTogetherAction(actionName)
            except Exception as e:
                gamelog.debug('m.l@playActionWithRider', e.message)

    def playStraightToLeft(self):
        try:
            straightToLeftAction = self.fashion.getStraightToLeftAction()
            self.playActionWithRider(straightToLeftAction, action.TURN_ACTION, None)
        except Exception as e:
            gamelog.debug('m.l@playStraightToLeft', e.message)

    def playStraightToRight(self):
        try:
            straightToRightAction = self.fashion.getStraightToRightAction()
            self.playActionWithRider(straightToRightAction, action.TURN_ACTION, None)
        except Exception as e:
            gamelog.debug('m.l@playStraightToRight', e.message)

    def playLeftToRight(self):
        try:
            leftToRightAction = self.fashion.getLeftToRightAction()
            self.playActionWithRider(leftToRightAction, action.TURN_ACTION, None)
        except Exception as e:
            gamelog.debug('m.l@playLeftToRight', e.message)

    def playRightToLeft(self):
        try:
            rightToLeftAction = self.fashion.getRightToLeftAction()
            self.playActionWithRider(rightToLeftAction, action.TURN_ACTION, None)
        except Exception as e:
            gamelog.debug('m.l@playRightToLeft', e.message)

    def playLeftToStraight(self):
        try:
            leftToStraightAction = self.fashion.getLeftToStraightAction()
            self.playActionWithRider(leftToStraightAction, action.TURN_ACTION, None)
        except Exception as e:
            gamelog.debug('m.l@playLeftToStraight', e.message)

    def playRightToStraight(self):
        try:
            rightToStraightAction = self.fashion.getRightToStraightAction()
            self.playActionWithRider(rightToStraightAction, action.TURN_ACTION, None)
        except Exception as e:
            gamelog.debug('m.l@playRightToStraight', e.message)

    def inMotorRunStop(self):
        enableSideStop = FDD.data.get(self.fashion.modelID, {}).get('enableSideStop')
        if enableSideStop:
            return True
        return False

    def movingNotifier(self, isMoving, moveSpeed = 1.0):
        self.isMoving = isMoving
        self.refreshWingHorseIdleEffect()
        self.updateFlyTailEffect()
        if self.modelServer:
            self.modelServer.playFashionIdleEffect()
        if self.qinggongState not in gametypes.QINGGONG_STATE_WINGFLY_SET:
            if self.isMoveChanged(isMoving, False):
                self.refreshHorseWingEffect()
        self.updateTriderSpriteState(isMoving)
        if self.am.jumping or hasattr(self, 'physics') and self.physics.jumping:
            return
        else:
            movingType = self.__checkActionNeedType()
            if isMoving:
                if self.modelServer:
                    self.modelServer.stopWearBoredAction()
                self.breakBeHitAction()
                self.startMovingTime = BigWorld.time()
                if self._checkNeedPlayStartAction(moveSpeed):
                    self.playStartToRun()
                if movingType == action.S_BLEND or getattr(self.skillPlayer, 'castLoop', None):
                    seq = self.fashion.playedAction.get(self.fashion.actionKey, None)
                    if seq != None and seq.active == True and seq.blend:
                        for i in seq.action:
                            i.enableAlpha(True)
                            i.enableDummyTrack(False)

                    for actName in self.model.queue:
                        act = self.model.action(actName)
                        if act.blended:
                            act.enableAlpha(True)
                            act.enableDummyTrack(False)
                        elif self.fashion._doingActionType in (action.CASTSTOP_ACTION,):
                            castStopActionName = getattr(self, 'castStopActionName', None)
                            if castStopActionName == actName:
                                self.fashion.stopActionByName(self.model, castStopActionName)

                elif movingType == action.S_BREAK:
                    if self.fashion.isPlayer and self.spellingType:
                        self.ap.cancelskill()
                    if self.fashion.doingActionType() == action.FALLEND_ACTION:
                        self.fashion.stopActionByName(self.model, self.fashion.fallEndAction)
                        if self.inRidingHorse() and hasattr(self.model, 'ride') and not self.inFlyTypeFlyRide():
                            self.fashion.stopActionByName(self.model.ride, self.fashion.fallEndAction)
                    elif self.fashion.doingActionType() in (action.ROLLSTOP_ACTION, action.LEAVE_HORSE_END_ACTION, action.BORED_ACTION):
                        self.fashion.stopModelAction(self.model)
                        if hasattr(self, 'qinggongMgr'):
                            self.qinggongMgr.stopWingFlyModelAction()
                    elif self.fashion.doingActionType() in (action.PROGRESS_SPELL_ACTION, action.PICK_END_ACTION):
                        self.fashion.stopAction()
                        self._afterEndActionProgress()
                    else:
                        rideAttached = self.modelServer.rideAttached
                        chairIdleAction = rideAttached.chairIdleAction if rideAttached else None
                        if self.fashion.doingActionType() == action.SOCIAL_ACTION:
                            self.fashion.disableFootIK(False)
                        if not self.qinggongMgr.rushTop and not self.inFlyTypeFlyRide():
                            if not getattr(self, 'inDanDao', False):
                                if not chairIdleAction:
                                    if not self.inMotorRunStop():
                                        self.fashion.stopAllActions()
                                    if hasattr(self, 'qinggongMgr'):
                                        self.qinggongMgr.stopWingFlyModelAction()
                                else:
                                    self.fashion.stopAction()
                        if self.inRidingHorse() and hasattr(self.model, 'ride') and not self.inFlyTypeFlyRide():
                            if not chairIdleAction:
                                if not self.inMotorRunStop():
                                    self.fashion.stopModelAction(self.model)
                                    self.fashion.stopModelAction(self.model.ride)
                        if self.isGuildSitInChair():
                            self.guildLeaveChair()
                        self._detachLifeSkillEquip()
                    if getattr(self, 'castSkillBusy', None):
                        self.castSkillBusy = False
                for actName in self.model.queue:
                    manDownStopAction = self.fashion.action.getManDownStopAction(self.fashion)
                    if self.fashion.fallEndAction == actName or actName == manDownStopAction:
                        self.fashion.stopActionByName(self.model, actName)
                        if self.fashion.fallEndAction == actName:
                            self.fashion.fallEndAction = None
                    flyStopActionName = self.fashion.getWingFlyStopAction()
                    if flyStopActionName == actName:
                        self.fashion.stopActionByName(self.model, actName)
                    horseEnterHorseAction = self.fashion.getHorseEnterHorseAction()
                    if horseEnterHorseAction == actName:
                        self.fashion.stopActionByName(self.model, actName)

                if self.canFly():
                    wingFlyStartToIdleAction = self.fashion.action.getWingFlyStartToIdleAction(self.fashion)
                    wingModel = self.modelServer.wingFlyModel.model
                    if wingModel:
                        for actName in wingModel.queue:
                            if actName == wingFlyStartToIdleAction:
                                self.fashion.stopActionByName(self.model, actName)
                                self.fashion.stopActionByName(wingModel, actName)

                    if self.inFlyTypeFlyRide():
                        bodyModel = self.modelServer.bodyModel
                        if bodyModel:
                            flyStopActionName = self.fashion.getWingFlyStopAction()
                            WingFlyRushStartAction = self.fashion.getWingFlyRushStartAction()
                            for actName in bodyModel.queue:
                                if actName in (flyStopActionName, WingFlyRushStartAction):
                                    self.fashion.stopActionByName(bodyModel, actName)
                                    self.stopRideTogetherAction(actName)

                self.playNormalReadyAction()
                gamelog.debug('#movingNotifier:', self.id, self)
                if self.fashion.doingActionType() not in (action.CHARGE_ACTION, action.GUIDE_ACTION, action.MOVING_ACTION):
                    self.skillPlayer.refreshWeapon()
                self.fashion.footTriggerMgr.releaseFootIdleEffect()
            else:
                self.endMovingTime = BigWorld.time()
                if self._checkNeedPlayRunToIdel():
                    runToIdleAction = self.fashion.getRunToIdleAction()
                    needRunToIdleWithMove = self.needRunToIdleWithMove()
                    self.playActionWithRider(runToIdleAction, action.RUN_TO_IDEL_ACTION, self.runToIdleCallback, needRunToIdleWithMove)
                    self.fashion.setIdleType(gametypes.IDLE_TYPE_RUN_STOP)
                    if self.inMotorRunStop():
                        self.am.turnModelToEntity = False
                if movingType == action.S_BLEND:
                    seq = self.fashion.playedAction.get(self.fashion.actionKey, None)
                    if seq != None and seq.active == True and seq.blend:
                        for i in seq.action:
                            i.enableAlpha(False)

                    for actName in self.model.queue:
                        try:
                            act = self.model.action(actName)
                            if act.blended:
                                act.enableAlpha(False)
                        except:
                            pass

                self.stopNormalFlyReadyAction()
                self.fashion.footTriggerMgr.playFootIdleEffect()
                self.stopMoveBoredAction()
                self.lastStopMoveTime = BigWorld.time()
            p = BigWorld.player()
            if p.attachSkillData and p.summonedSpriteInWorld and p.attachSkillData[0] == self.id:
                p.spriteOwnerMoving(isMoving)
            return

    def needRunToIdleWithMove(self):
        if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            return FDD.data.get(self.fashion.modelID, {}).get('runToIdleWithMove', 0)
        return False

    def runToIdleCallback(self):
        self.fashion.setIdleType(gametypes.IDLE_TYPE_RUN_STOP)

    def stopMoveBoredAction(self):
        if not getattr(self.fashion, 'action', None):
            return
        else:
            try:
                if self.fashion.doingActionType() == action.BORED_ACTION:
                    moveBoredActions = SYSCD.data.get('moveBoredActions', ['11116', '31114', '11117'])
                    for actName in self.model.queue:
                        if actName in moveBoredActions:
                            self.fashion.stopActionByName(self.model, actName)

            except:
                pass

            return

    def stopRideTogetherAction(self, actionName):
        if self.inRidingHorse() and hasattr(self, 'tride') and self.tride.inRide():
            for key in self.tride.keys():
                idx = self.tride.get(key)
                model = self.modelServer.getRideTogetherModelByIdx(idx)
                if model:
                    self.fashion.stopActionByName(model, actionName)

    def _checkNeedPlayNormalStartAction(self):
        if self.qinggongState:
            return
        if self.bufActState:
            return False
        if not self.fashion.isPlayer:
            return False
        if self.inFly:
            if not self.stateMachine.checkStatus(const.CT_PLAY_NORMAL_FLY_STARTACTION):
                return False
        if self.bianshen[0] and not self.inFly:
            if not self.stateMachine.checkStatus(const.CT_PLAY_NORMAL_HORSE_STARTACTION):
                return False
        return True

    def isCombineMove(self):
        magnitude = 0
        p = BigWorld.player()
        mags = [p.ap.forwardMagnitude,
         p.ap.backwardMagnitude,
         p.ap.upwardMagnitude,
         p.ap.rightwardMagnitude,
         p.ap.leftwardMagnitude]
        for mag in mags:
            if mag != 0:
                magnitude = magnitude + 1

        return magnitude

    def getNormalReadyAction(self):
        p = BigWorld.player()
        magnitude = self.isCombineMove()
        if magnitude > 1:
            return None
        else:
            if p.ap.forwardMagnitude:
                if p.inFly:
                    return self.fashion.getNormalFlyForwardStartAction()
                if p.bianshen[0]:
                    return self.fashion.getNormalHorseForwardStartAction()
            if p.ap.backwardMagnitude:
                if p.inFly:
                    return self.fashion.getNormalFlyBackwardStartAction()
                if p.bianshen[0]:
                    return self.fashion.getNormalHorseBackwardStartAction()
            if p.ap.upwardMagnitude > 0:
                return self.fashion.getNormalFlyUpStartAction()
            if p.ap.upwardMagnitude < 0:
                return self.fashion.getNormalFlyDownStartAction()
            if p.ap.rightwardMagnitude:
                if p.inFly:
                    return self.fashion.getNormalFlyRightStartAction()
                if p.bianshen[0]:
                    return self.fashion.getNormalHorseRightStartAction()
            if p.ap.leftwardMagnitude:
                if p.inFly:
                    return self.fashion.getNormalFlyLeftStartAction()
                if p.bianshen[0]:
                    return self.fashion.getNormalHorseLeftStartAction()
            return None

    def playNormalReadyAction(self):
        if self._checkNeedPlayNormalStartAction():
            normalStartAction = self.getNormalReadyAction()
            if normalStartAction:
                self.fashion.playAction([normalStartAction], action.NORMAL_READY_ACTION)

    def stopNormalFlyReadyAction(self):
        if self.fashion.doingActionType() == action.NORMAL_READY_ACTION:
            self.fashion.stopAction()

    def unloadWidget(self, widgetId):
        if widgetId in gameglobal.rds.ui.escFunc:
            gameglobal.rds.ui.escFunc[widgetId][0]()

    def uiAction(self, proxyName, func, args):
        gamelog.debug('@zhp uiAction', proxyName, func, args)
        if hasattr(gameglobal.rds.ui, proxyName):
            proxy = getattr(gameglobal.rds.ui, proxyName)
            if hasattr(proxy, func):
                if args == None:
                    getattr(proxy, func)()
                elif isinstance(args, tuple):
                    getattr(proxy, func)(*args)
                else:
                    getattr(proxy, func)(args)

    def npcUIPush(self, npcId, chatId):
        gameglobal.rds.ui.autoQuest.openDirectly(npcId, chatId, False)

    def startAction(self, type):
        if type == const.ACTION_PICK_ITEM:
            self._playPickAction()

    def _playPickAction(self):
        pickItemAction = self.fashion.getPickActionName()
        model = self.model
        blend = False
        if self.inMoving():
            blend = True
        if self.inRiding():
            model = self.model.ride
            blend = True
        self.fashion.playActionSequence2(model, [(pickItemAction,
          None,
          0,
          ACT.PICK_ITEM_ACTION)], ACT.PICK_ITEM_ACTION, 1, 0, blend)

    def cancelTransportSpell(self, cause = const.CANCEL_ACT_ANY_WAY):
        spellId = getattr(self, 'spellTargetId', 0)
        if spellId:
            ent = BigWorld.entities.get(spellId)
            if ent and utils.instanceof(ent, 'Transport'):
                cellCmd.cancelAction(cause)

    def cancelTreasureBoxSpell(self, cause = const.CANCEL_ACT_ANY_WAY):
        spellId = getattr(self, 'spellTargetId', 0)
        if spellId:
            ent = BigWorld.entities.get(spellId)
            if ent and utils.instanceof(ent, 'TreasureBox'):
                cellCmd.cancelAction(cause)

    def playDebugEffect(self, effectId, lastTime, effectLv):
        gameglobal.rds.ui.debug.playEffect(effectId, lastTime, effectLv)

    def debugChangeWingSpeed(self, speed):
        if getattr(self, 'gmMode', False):
            PCD.data['flyHorizonSpeed'] = speed

    def clearSkillCds(self):
        gameglobal.rds.ui.actionbar.clearCooldown()

    def getReplaceSkillEffs(self, itemId, skillId):
        eData = EQD.data.get(itemId, {})
        wearReplaceSkillEffs = eData.get('wearReplaceSkillEffs', {}).get(skillId, ())
        return wearReplaceSkillEffs

    def doUseWearSkill(self, skillId, skillLv, equipPart):
        playSeq = []
        clientSkillInfo = self.getClientSkillInfo(skillId, skillLv)
        act = clientSkillInfo.getSkillData('castAct', [0, None])[1]
        eff = clientSkillInfo.getSkillData('castEff', [0, None])[1:]
        castTime = clientSkillInfo.getSkillData('castEffectTime', 0)
        replaceSkillEffs = None
        callback = None
        _partDict = {gametypes.EQU_PART_FASHION_CAPE: 'fashionCape'}
        if equipPart in _partDict:
            itemId = getattr(self.aspect, _partDict.get(equipPart), 0)
            if not itemId:
                return
            replaceSkillEffs = self.getReplaceSkillEffs(itemId, skillId)
            if replaceSkillEffs:
                eff = replaceSkillEffs
            if castTime and eff:
                for ef in eff:
                    sfx.updateEffectKeepTime(ef, castTime)

            if act:
                self.fashion.playActionSequence(self.model, (act,), None)
            for effId in eff:
                self.removeFx(effId)
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 effId,
                 sfx.EFFECT_LIMIT_MISC))
                if fx:
                    self.addFx(effId, fx)

        else:
            wear = self.modelServer.getShowWear(equipPart)
            if not wear:
                return
            replaceSkillEffs = self.getReplaceSkillEffs(wear.key, skillId)
            if replaceSkillEffs:
                eff = replaceSkillEffs
            if act:
                playSeq.append((act,
                 eff,
                 action.SHOW_WEAR_ACTION,
                 0,
                 1,
                 0))
                if wear.isActionJustSkillWear():
                    if self.weaponInHandState() == gametypes.WEAR_BACK_ATTACH:
                        self.modelServer.attachWear('backwear')
                        callback = Functor(self.callbackHangUpWear, 'backwear')
                    elif self.weaponInHandState() == gametypes.WEAR_WAIST_ATTACH:
                        self.modelServer.attachWear('waistwear')
                        callback = Functor(self.callbackHangUpWear, 'waistwear')
                    else:
                        callback = None
                else:
                    callback = None
                self.fashion.playActionWithFx(playSeq, action.SHOW_WEAR_ACTION, callback, False, priority=self.getSkillEffectPriority())
            for item in wear.models:
                model = item[0]
                try:
                    if act:
                        model.action(act)()
                    else:
                        for effId in eff:
                            self.removeFx(effId)
                            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                             self.getBasicEffectPriority(),
                             model,
                             effId,
                             sfx.EFFECT_LIMIT_MISC))
                            if fx:
                                self.addFx(effId, fx)

                except:
                    pass

    def callbackHangUpWear(self, wear):
        if wear in ('backwear', 'waistwear') and self.fashion.doingActionType() != action.SHOW_WEAR_ACTION:
            self.modelServer.hangUpWear(wear)

    def releaseTeleportEffect(self):
        if self.teleportSpellEffs:
            for ef in self.teleportSpellEffs:
                if ef:
                    ef.stop()

            self.teleportSpellEffs = []

    def playTeleportSpell(self):
        self.releaseTeleportEffect()
        data = TSD.data.get(gameglobal.TELEPORT_SPELL_ENTER_FUBEN)
        teleportAction = data.get('action')
        effect = data.get('effect')
        try:
            self.model.action(teleportAction)()
        except:
            pass

        fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
         self.getBasicEffectPriority(),
         self.model,
         effect,
         sfx.EFFECT_LIMIT_MISC,
         gameglobal.EFFECT_LAST_TIME))
        if fxs:
            self.teleportSpellEffs.extend(fxs)

    def stopTeleportSpell(self):
        if self == BigWorld.player():
            if self.teleportCB:
                BigWorld.cancelCallback(self.teleportCB)
        self.releaseTeleportEffect()

    def triggerFlyEffect(self, position, speed, acceleration, flyEff = [], flyDestEff = []):
        a = sfx.FlyToNode(None)
        a.start(position, self.model.root, 0.2, 0, speed, None, acceleration, False, flyDestEff=flyDestEff)
        a.addFlyEffect(flyEff)

    def graveScenarioPlay(self, msg):
        name = 'mapgamegrave.xml'
        self._scenarioPlay(name, finishCallback=Functor(gameglobal.rds.ui.mapGameFinish.show, False, msg))
