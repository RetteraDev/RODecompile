#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPUBG.o
import BigWorld
import random
import math
import gamelog
import gameglobal
import gametypes
import utils
import const
import keys
import pubgUtils
from helpers import cellCmd
from item import Item
from gamestrings import gameStrings
from guis import events
from callbackHelper import Functor
from guis import topLogo
from guis import menuManager
from guis import uiDrag
from guis import uiConst
from guis import uiUtils
from appSetting import Obj as AppSettings
from helpers import gasCirclePUBG
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import battle_field_data as BFD
from data import duel_config_data as DCD
from cdata import pubg_safe_area_data as PSAD
from cdata import pubg_airline_data as PAD
from cdata import skill_qte_reverse_data as SQRD
from cdata import pubg_init_skill_reverse_data as PISRD
from cdata import pubg_rank_points_data as PRPD

class ImpPUBG(object):

    def notifyEnterPUBG(self, fbNo):
        gamelog.debug('@zmk notifyEnterPUBG:', fbNo)
        self.showBattleFieldConfirmMsg(fbNo)

    def pubgRefreshSafeArea(self, stage, stamp, nowPos, nextPos):
        p = BigWorld.player()
        gamelog.debug('@zmk pubgRefreshSafeArea:', stage, stamp, nowPos, nextPos)
        poisonDataList = [stage,
         stamp,
         nowPos,
         nextPos]
        self.setCurPoisonCircleData(poisonDataList)
        if stage != 0:
            BigWorld.callback(PSAD.data.get(stage, {}).get('holdTime', 0), lambda : p.showGameMsg(GMDD.data.wuyetaosha_yindao_6, ()))
        if stage == 1:
            p.showGameMsg(GMDD.data.wuyetaosha_yindao_5, ())

    def pubgSyncState(self, state, extra):
        gamelog.debug('@zmk pubgSyncState:', state, extra)
        p = BigWorld.player()
        p.curPUBGStateProgress = state
        p.refreshAllSkillUIInPubg()
        if state == pubgUtils.PUBG_STATE_PROGRESS_NONE or not p.isInPUBG():
            p.curPUBGStateProgress = state
        elif state == pubgUtils.PUBG_STATE_PROGRESS_PREPARE:
            nextPos = DCD.data.get('pubgInitialCenterPos')
            p.pubgRefreshSafeArea(0, utils.getNow(), None, nextPos)
            gameglobal.rds.ui.questTrack.resetQuestTrackOpacity()
            gameglobal.rds.ui.pubgHover.show()
            gameglobal.rds.ui.pubgHover.setAdjustBtnVisible(True)
            gameglobal.rds.ui.pubgHover.showPubgGuildTip(pubgUtils.PUBG_GUILD_TIP_PREPARE)
        elif state == pubgUtils.PUBG_STATE_PROGRESS_WAIT_AIRPLANE:
            p.curAirPlaneData['lineNo'] = extra.get('lineNo', 0)
            p.setCurAirPlaneData(True)
            p.curPUBGNumsData[pubgUtils.PUBG_ALL_NUM_IDX] = extra.get('pubgAllNums', 80)
            p.curPUBGNumsData[pubgUtils.PUBG_LEFT_NUM_IDX] = extra.get('pubgAllNums', 80)
            p.generalTeammateNoInPUBG()
            gameglobal.rds.ui.teamComm.refreshMemberInfo()
            gameglobal.rds.ui.questTrack.resetQuestTrackOpacity()
            gameglobal.rds.ui.pubgHover.setAdjustBtnVisible(False)
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.hide()
            p.refreshCameraFarPlane()
            gCircle = gasCirclePUBG.getInstance()
            gCircle.init()
            gameglobal.rds.ui.littleMap.setPUBGUIMc(isInPUBG=p.isInPUBG())
        elif state == pubgUtils.PUBG_STATE_PROGRESS_FLY_AIRPLANE:
            airplaneStartStamp = extra.get('stamp', utils.getNow())
            p.curAirPlaneData['startStamep'] = airplaneStartStamp
            p.generalTeammateNoInPUBG()
            gameglobal.rds.ui.teamComm.refreshMemberInfo()
            gameglobal.rds.ui.littleMap.setPUBGUIMc(isInPUBG=p.isInPUBG())
            gCircle = gasCirclePUBG.getInstance()
            gCircle.init()
            p.setSkyZoneInPUBGAtFixTime()
            p.setSoundInPUBGAtFixTime()
            self.refreshOpacityState()
            self.checkPlaneState()
        elif state == pubgUtils.PUBG_STATE_PROGRESS_FLY_AIRPLANE_CAN_DROP:
            p.generalTeammateNoInPUBG()
            gameglobal.rds.ui.teamComm.refreshMemberInfo()
            gameglobal.rds.ui.pubgHover.showPubgGuildTip(pubgUtils.PUBG_GUILD_TIP_ONPLANE)
            p.showGameMsg(GMDD.data.wuyetaosha_yindao_4, ())
        elif state == pubgUtils.PUBG_STATE_PROGRESS_FLY_AIRPLANE_FORCE_DROP:
            pass
        elif state == pubgUtils.PUBG_STATE_PROGRESS_FLY_START:
            gameglobal.rds.ui.littleMap.setPUBGUIMc(isInPUBG=p.isInPUBG())
            gameglobal.rds.ui.pubgHover.showPubgGuildTip(pubgUtils.PUBG_GUILD_TIP_DROPPING)
        elif state == pubgUtils.PUBG_STATE_PROGRESS_FLY_FALL_ON_THE_GROUND:
            gameglobal.rds.ui.pubgHover.showPubgGuildTip(pubgUtils.PUBG_GUILD_TIP_ON_GROUND)
        elif state == pubgUtils.PUBG_STATE_PROGRESS_FLY_ALL_END:
            gCircle = gasCirclePUBG.getInstance()
            gCircle.clear()

    def pubgNotifyBoss(self, monsterId, state, position):
        gamelog.debug('@zmk pubgNotifyBoss:', monsterId, state, position)
        p = BigWorld.player()
        if p.curBossInPUBG is None:
            p.curBossInPUBG = dict()
        if monsterId in p.curBossInPUBG:
            if state == pubgUtils.BOSS_ALIVE:
                p.curBossInPUBG[monsterId] = list(position)
            elif state == pubgUtils.BOSS_DIE:
                p.curBossInPUBG.pop(monsterId)
        elif state == pubgUtils.BOSS_ALIVE:
            p.curBossInPUBG[monsterId] = list(position)
        gameglobal.rds.ui.map.refreshBossInPubg()
        gameglobal.rds.ui.littleMap.refreshBossInPubg()

    def pubgNotifyTreasureBox(self, tType, tStamp):
        p = BigWorld.player()
        if p.curTreasureBoxInPUBG is None:
            p.curTreasureBoxInPUBG = dict()
        if tType == pubgUtils.TREASURE_BOX_APPEAR:
            p.curTreasureBoxInPUBG['startStamp'] = tStamp
        elif tType == pubgUtils.TREASURE_BOX_DISAPPEAR:
            p.curTreasureBoxInPUBG.clear()
        gameglobal.rds.ui.map.refreshTreasureBoxInPubg()
        gameglobal.rds.ui.littleMap.refreshTreasureBoxInPubg()

    def pubgOnAddTreasureBoxBuff(self, buffType, startStamp):
        p = BigWorld.player()
        intervalStamp = DCD.data.get('pubgCreateTreasureBoxInterval', 300) + startStamp - utils.getNow()
        if intervalStamp > 1:
            p.showGameMsg(GMDD.data.PUBG_PLAYER_GET_TREASURE_BOX_BUFF, (intervalStamp,))

    def notifySafeAreaState(self, sType):
        if sType == pubgUtils.IN_SAFE_AREA:
            gameglobal.rds.sound.playSound(998)
        elif sType == pubgUtils.NOT_IN_SAFE_AREA:
            gameglobal.rds.sound.playSound(997)

    def pubgSyncTreasureBuffPosition(self, position):
        p = BigWorld.player()
        if p.curTreasureBoxInPUBG is None:
            p.curTreasureBoxInPUBG = dict()
        p.curTreasureBoxInPUBG['posInWorld'] = list(position)
        gameglobal.rds.ui.map.refreshTreasureBoxInPubg()
        gameglobal.rds.ui.littleMap.refreshTreasureBoxInPubg()

    def pubgNotifyDisaster(self, position, startStamp):
        gamelog.debug('@zmk pubgNotifyDisaster:', position, startStamp)
        p = BigWorld.player()
        if p.curDisasterDataInPUBG is None:
            p.curDisasterDataInPUBG = dict()
        p.curDisasterDataInPUBG['posInWorld'] = position
        p.curDisasterDataInPUBG['startStamp'] = startStamp
        self.setDisasterDataInPubg()

    def set_pubgUnlockedSkills(self, old):
        BigWorld.player().refreshAllSkillUIInPubg()

    def onUnlockPubgSkill(self, skillId):
        p = BigWorld.player()
        if not p.pubgUnlockedSkills.get(skillId, False):
            p.pubgUnlockedSkills[skillId] = True
        BigWorld.player().refreshAllSkillUIInPubg()

    def onLearnPubgSkill(self, skillId, skillLv):
        p = BigWorld.player()
        if p.isInPUBG():
            if p.pubgSkills is None:
                p.pubgSkills = dict()
            pubgSkillInfo = p.getSkillInfo(skillId, skillLv)
            p.pubgSkills[skillId] = pubgSkillInfo
        gameglobal.rds.ui.pubgGeneralSkill.refreshInfo()

    def syncPubgSkillData(self, skillInfo):
        p = BigWorld.player()
        if p.isInPUBG():
            p.pubgSkills = dict()
            if skillInfo:
                for skillId, skillLv in skillInfo.iteritems():
                    self.onLearnPubgSkill(skillId, skillLv)

        gameglobal.rds.ui.pubgGeneralSkill.refreshInfo()

    def onUsePubgSkillsSucc(self, skillId, nextTime):
        gameglobal.rds.ui.pubgGeneralSkill.refreshSkillSlot(skillId)

    def pubgNotifyBattleFieldResult(self, res):
        p = BigWorld.player()
        gameglobal.rds.ui.pubgEnding.show(res)

    def pubgNotifyBattleField(self, nType):
        p = BigWorld.player()
        if not p.isCanJoinPUBG():
            return
        gameglobal.rds.ui.pvPPanel.refreshTab()
        if nType == pubgUtils.NOTIFY_OPEN_BATTLE_FIELD:
            p.setPUBGNewOpenMsgCallBack()
            p.pushPUBGNewOpenMsg()
        elif nType == pubgUtils.NOTIFY_CLOSE_BATTLE_FIELD:
            p.removePUBGNewOpenMsg()

    def pubgQueryStatistics(self, pubgRankPointsRewardMark, pubgExtra):
        p = BigWorld.player()
        p.playerRankPointMarkData = pubgRankPointsRewardMark
        p.playerAllBattleData = pubgExtra
        gameglobal.rds.ui.pvpPUBG.initAll()

    def pubgNoptifyDuel(self, res):
        p = BigWorld.player()
        if res == pubgUtils.LOSE_DUEL_FLAG:
            p.showGameMsg(GMDD.data.wuyetaosha_yindao_8, ())
        elif res == pubgUtils.WIN_DUEL_FLAG:
            p.showGameMsg(GMDD.data.wuyetaosha_yindao_7, ())

    def pubgNotifyKill(self, deathType, remain, killerInfo, killeeInfo):
        p = BigWorld.player()
        p.curPUBGNumsData[pubgUtils.PUBG_LEFT_NUM_IDX] = remain
        deadRoleName = killeeInfo.get(pubgUtils.PUBG_NOTIFY_MSG_ROLENAME, None)
        deadGbId = killeeInfo.get(pubgUtils.PUBG_NOTIFY_MSG_GBID, None)
        if not deadGbId:
            return
        else:
            if deathType == pubgUtils.DEATH_BY_AVATAR:
                killRoleName = killerInfo.get(pubgUtils.PUBG_NOTIFY_MSG_ROLENAME, None)
                killGbId = killerInfo.get(pubgUtils.PUBG_NOTIFY_MSG_GBID, None)
                if killGbId == p.gbId:
                    p.showGameMsg(GMDD.data.PUBG_PLAYER_KILL_OTHER, (deadRoleName,))
                elif deadGbId == p.gbId:
                    pass
                elif p.checkTeamMateInPUBG(killGbId):
                    p.showGameMsg(GMDD.data.PUBG_TEAMMATE_KILL_OTHER, (killRoleName, deadRoleName))
                elif p.checkTeamMateInPUBG(deadGbId):
                    p.showGameMsg(GMDD.data.PUBG_OTHER_KILL_TEAMMATE, (deadRoleName, killRoleName))
                else:
                    p.showGameMsg(GMDD.data.PUBG_OTHER_KILL_OTHER, (killRoleName, deadRoleName))
            elif deathType == pubgUtils.DEATH_BY_POISON:
                if deadGbId == p.gbId:
                    pass
                if p.checkTeamMateInPUBG(deadGbId):
                    p.showGameMsg(GMDD.data.PUBG_POISON_KILL_TEAMMATE, (deadRoleName,))
                else:
                    p.showGameMsg(GMDD.data.PUBG_POISON_KILL_OTHER, (deadRoleName,))
            elif deathType == pubgUtils.DEATH_BY_OFFLINE:
                pass
            else:
                p.showGameMsg(GMDD.data.PUBG_OTHER_SITUATION_KILL_OTHER, (deadRoleName,))
            gameglobal.rds.ui.littleMap.setPUBGUIMc(isInPUBG=p.isInPUBG())
            return

    def pubgNotifyRemain(self, rType, cnt):
        p = BigWorld.player()
        if rType == pubgUtils.REMAIN_TYPE_PREPARE_AREA:
            p.curPUBGNumsData[pubgUtils.PUBG_LEFT_NUM_IN_PLANE_IDX] = cnt
        elif rType == pubgUtils.REMAIN_TYPE_PLANE:
            p.curPUBGNumsData[pubgUtils.PUBG_LEFT_NUM_IN_PLANE_IDX] = cnt
        gameglobal.rds.ui.littleMap.setPUBGUIMc(isInPUBG=p.isInPUBG())

    def pubgRefreshKillCnt(self, cnt):
        p = BigWorld.player()
        p.curPUBGNumsData[pubgUtils.PUBG_KILL_NUM_IDX] = cnt
        gameglobal.rds.ui.littleMap.setPUBGUIMc(isInPUBG=p.isInPUBG())

    def pubgNotifyTeamDie(self, gbId, position):
        p = BigWorld.player()
        if gbId in p.curTeamMemberInPUBG:
            p.curTeamMemberInPUBG[gbId]['isDead'] = True
            p.curTeamMemberInPUBG[gbId]['deadPos'] = position
        gameglobal.rds.ui.teamComm.refreshMemberInfo()

    def pubgSwitchRegen(self, isOpen):
        gamelog.debug('@zmk pubgSwitchRegen:', isOpen)
        p = BigWorld.player()
        p.isCanRegenMpInPUBG = isOpen
        p._setMpRegen(p.mp)

    def isCanJoinPUBG(self):
        if not gameglobal.rds.configData.get('enablePUBG', False):
            return False
        return True

    def isCanJoinTimingPUBG(self):
        if not gameglobal.rds.configData.get('enableTimingPUBG', False):
            return False
        return True

    def isInPUBG(self):
        p = BigWorld.player()
        if not self.isCanJoinPUBG():
            return False
        if p.inFubenTypes((const.FB_TYPE_BATTLE_FIELD_PUBG, const.FB_TYPE_BATTLE_FIELD_TIMING_PUBG)):
            return True
        if hasattr(self, 'tempPUBG') and self.tempPUBG:
            return True
        return False

    def isPUBGFbNo(self, fbNo):
        if fbNo in (const.FB_NO_BATTLE_FIELD_PUBG, const.FB_NO_BATTLE_FIELD_TIMING_PUBG):
            return True
        return False

    def isBianShenZaiJuInPUBG(self, entity):
        p = BigWorld.player()
        if not entity or not p.isInPUBG():
            return False
        avatarEntity = entity
        if hasattr(entity, 'IsAvatar') and entity.IsAvatar:
            avatarEntity = entity
        elif hasattr(entity, 'IsSummonedSprite') and entity.IsSummonedSprite and hasattr(entity, 'getOwner'):
            avatarEntity = entity.getOwner()
        elif hasattr(entity, 'IsSummonedBeast') and entity.IsSummonedBeast and hasattr(entity, 'ownerId'):
            avatarEntity = BigWorld.entity(entity.ownerId)
        if hasattr(avatarEntity, '_isOnZaiju') and avatarEntity._isOnZaiju():
            if avatarEntity._getZaijuNo() in DCD.data.get('pubgPretendZaijuIdList', []):
                return True
        return False

    def inPUBGPlane(self):
        pubgPlaneZaijuNo = DCD.data.get('pubgPlaneZaijuNo', 0)
        return self._isOnZaiju() and self._getZaijuNo() == pubgPlaneZaijuNo

    def inPUBGParachute(self):
        pubgParachuteZaijuNo = DCD.data.get('pubgParachuteZaijuNo', 0)
        return self._isOnZaiju() and self._getZaijuNo() == pubgParachuteZaijuNo

    def refreshPUBGPlaneForceMoveState(self):
        pubgOnPlaneBuffId = DCD.data.get('pubgOnPlaneBuffId', 0)
        planeBuffData = self.statesServerAndOwn.get(pubgOnPlaneBuffId, {})
        if planeBuffData:
            self.clientStateEffect.delForceMove(pubgOnPlaneBuffId)
            self.clientStateEffect.addForceMove(pubgOnPlaneBuffId)

    def leavePUBG(self, warningMsg = True, pubgEnding = False):
        p = BigWorld.player()
        if p.isInPUBG():
            if p.inFightObserve() and not pubgEnding:
                if warningMsg:
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.PUBG_FIGHT_OBSERVE_LEAVE_CHECK_HINT, yesCallback=Functor(p.realLeavePUBG, p.cell.pubgSingleDuel))
                else:
                    p.cell.pubgSingleDuel()
            elif warningMsg:
                msg = uiUtils.getTextFromGMD(GMDD.data.QUIT_BATTLE_FIELD_MSG)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.realLeavePUBG, p.cell.pubgQuitBattleField))
            else:
                p.cell.pubgQuitBattleField()

    def realLeavePUBG(self, leaveCall):
        leaveCall and leaveCall()
        gCircle = gasCirclePUBG.getInstance()
        gCircle.clear()

    def checkPlaneState(self):
        p = BigWorld.player()
        if not p:
            return
        if pubgUtils.PUBG_STATE_PROGRESS_FLY_AIRPLANE <= p.curPUBGStateProgress < pubgUtils.PUBG_STATE_PROGRESS_FLY_FALL_ON_THE_GROUND:
            if self.inPUBGPlane() and not self.ap.forwardMagnitude:
                self.refreshPUBGPlaneForceMoveState()
            if self.inPUBGParachute():
                self.ap.updateVelocity()
            BigWorld.callback(0.1, self.checkPlaneState)

    def onPUBGLoaded(self, fbNo):
        p = BigWorld.player()
        if p.curPUBGStateProgress == pubgUtils.PUBG_STATE_PROGRESS_PREPARE:
            p.showGameMsg(GMDD.data.wuyetaosha_yindao_1, ())
            BigWorld.callback(pubgUtils.PUBG_YINDAO_MSG_TIME_INTERVAL, lambda : p.showGameMsg(GMDD.data.wuyetaosha_yindao_2, ()))
            readyTimeInPUBG = BFD.data.get(fbNo, {}).get('readyTime', 60)
            if hasattr(p, 'deltaOfArena'):
                realReadyTimeInPUBG = readyTimeInPUBG - p.deltaOfArena
            else:
                realReadyTimeInPUBG = readyTimeInPUBG
            BigWorld.callback(realReadyTimeInPUBG - pubgUtils.PUBG_YINDAO_MSG_THIRD_AHEAD_TIME, lambda : p.showGameMsg(GMDD.data.wuyetaosha_yindao_3, ()))
            gameglobal.rds.ui.baoDian.autoShowIntro(uiConst.BAODIAN_TYPE_PUBG)
        gameglobal.rds.ui.littleMap.setPUBGUIMc(isInPUBG=p.isInPUBG())

    def onLeavePUBG(self):
        gamelog.debug('@zmk onLeavePUBG')
        p = BigWorld.player()
        p.autoPickSetting = {}
        p.autoFilterSetting = {}
        p.autoPickEnable = True
        p.curPoisonCircleData = []
        p.curPUBGStateProgress = pubgUtils.PUBG_STATE_PROGRESS_NONE
        p.curPUBGNumsData = [0,
         0,
         0,
         0,
         0]
        p.allTeammateMapMark.clear()
        p.curAirPlaneData = {}
        p.curDisasterDataInPUBG = dict()
        p.curDisasterEndCBInPUBG = None
        p.curBossInPUBG = {}
        p.curTreasureBoxInPUBG = {}
        p.curTeamMemberInPUBG = {}
        p.pubgSkills = {}
        p.curCanEquipListInPUBG = []
        p.curEquippingInPUBGCB = False
        p.skyZoneDataInPUBGCB = None
        p.playSoundInPUBGCB = None
        p.resetSkyZoneInPUBG()
        p.resetSoundInPUBG()
        gameglobal.rds.ui.pubgHover.hide()
        gameglobal.rds.ui.pubgKillAssist.hide()
        gameglobal.rds.ui.littleMap.setPUBGUIMc(isInPUBG=False)
        gameglobal.rds.ui.map.refreshAllMarksIconInPUBG()
        gameglobal.rds.ui.map.setBoundAreaInPubg(None)
        gameglobal.rds.ui.littleMap.refreshAllMarksIconInPUBG()
        gameglobal.rds.ui.littleMap.resetPlayerIcon()
        gCircle = gasCirclePUBG.getInstance()
        gCircle and gCircle.clear()
        self.refreshCameraFarPlane()

    def testPubgSkill(self):
        p = BigWorld.player()
        p.tempPUBG = True
        p.pubgSkills[9508] = p.getSkillInfo(9508, 1)
        p.pubgSkills[9509] = p.getSkillInfo(9509, 1)
        p.pubgSkills[9510] = p.getSkillInfo(9510, 1)
        gameglobal.rds.ui.pubgGeneralSkill.show()

    def testPubgUnlockSkill(self):
        p = BigWorld.player()
        p.onUnlockPubgSkill(1701)
        p.onUnlockPubgSkill(1720)
        p.onUnlockPubgSkill(1721)
        p.onUnlockPubgSkill(1722)
        p.onUnlockPubgSkill(1723)
        p.onUnlockPubgSkill(1705)
        p.onUnlockPubgSkill(1715)

    def testPubgPoison1(self):
        nextPos = DCD.data.get('pubgInitialCenterPos')
        self.pubgRefreshSafeArea(0, utils.getNow(), None, nextPos)

    def testPubgPoison2(self, nextStage, xzOffset = 100):
        p = BigWorld.player()
        nextPositon = [p.curPoisonCircleData[3][0] - xzOffset, p.curPoisonCircleData[3][1], p.curPoisonCircleData[3][2] + xzOffset]
        self.pubgRefreshSafeArea(nextStage, utils.getNow(), p.curPoisonCircleData[3], nextPositon)

    def textAirPlane(self):
        p = BigWorld.player()
        p.pubgSyncState(2, {'stamp': utils.getNow(),
         'lineNo': 2})

    def setCurAirPlaneData(self, isShow):
        p = BigWorld.player()
        if isShow:
            airLineNo = p.curAirPlaneData.get('lineNo', 0)
            airlineData = PAD.data.get(airLineNo, {})
            if airLineNo and airlineData:
                gameglobal.rds.ui.map.setAirPlaneLinePath([airlineData['startPos'], airlineData['endPos']])
                gameglobal.rds.ui.littleMap.setAirPlaneLinePath([airlineData['startPos'], airlineData['endPos']])
                BigWorld.callback(p.getAirplaneFlyTime(), Functor(p.setCurAirPlaneData, False))
        else:
            gameglobal.rds.ui.map.setAirPlaneLinePath(None)
            gameglobal.rds.ui.littleMap.setAirPlaneLinePath(None)

    def getCurAirPlanePos(self):
        p = BigWorld.player()
        airLineNo = p.curAirPlaneData.get('lineNo', 0)
        startStamep = p.curAirPlaneData.get('startStamep', utils.getNow())
        airlineData = PAD.data.get(airLineNo, {})
        if airLineNo and airlineData:
            curFlyTime = utils.getNow() - startStamep
            startPos = airlineData['startPos']
            endPos = airlineData['endPos']
            speed = airlineData['speed']
            dirVec = [ endPos[i] - startPos[i] for i in xrange(len(startPos)) ]
            dirNorm = math.sqrt(sum((a ** 2 for a in dirVec)))
            curPosOffset = [ float(a / dirNorm * speed * curFlyTime) for a in dirVec ]
            curPos = [ startPos[i] + curPosOffset[i] for i in xrange(len(startPos)) ]
            return curPos
        return [0, 0, 0]

    def getAirplaneFlyTime(self):
        p = BigWorld.player()
        waitFlyTime = DCD.data.get('pubgPlaneWaitInterval', 15)
        airLineNo = p.curAirPlaneData.get('lineNo', 0)
        airlineData = PAD.data.get(airLineNo, {})
        if airLineNo and airlineData:
            startPos = airlineData['startPos']
            endPos = airlineData['endPos']
            speed = airlineData['speed']
            dirVec = [ endPos[i] - startPos[i] for i in xrange(len(startPos)) ]
            dis = math.sqrt(sum([ a ** 2 for a in dirVec ]))
            return float(dis / speed) + waitFlyTime
        return 0

    def isCanDropInAirPlane(self):
        p = BigWorld.player()
        airLineNo = p.curAirPlaneData.get('lineNo', 0)
        startStamep = p.curAirPlaneData.get('startStamep', utils.getNow())
        airlineData = PAD.data.get(airLineNo, {})
        if airLineNo and airlineData:
            if utils.getNow() - startStamep >= airlineData['jumpTime']:
                return True
        return False

    def setCurPoisonCircleData(self, poisonDataList):
        p = BigWorld.player()
        p.curPoisonCircleData = poisonDataList
        gameglobal.rds.ui.littleMap.setPlayerIconInPUBG()
        gameglobal.rds.ui.map.setCurPoisonCircle()
        gameglobal.rds.ui.littleMap.refreshPoisonInPubg()
        gameglobal.rds.ui.littleMap.setPUBGUIMc(isInPUBG=p.isInPUBG())

    def getCurPoisonCircleRadius(self, nextCenterStage, nextCenterStamp):
        if nextCenterStage == 0:
            return DCD.data.get('pubgInitialCircleRadius', 5000)
        nextPoisonStageData = PSAD.data.get(nextCenterStage, {})
        nextPoisonHoldTime = nextPoisonStageData.get('holdTime', 0)
        nextPoisonShrinkTime = nextPoisonStageData.get('shrinkTime', 0)
        nextPoisonAreaRadius = self.getNextSafeCircleRadius(nextCenterStage)
        lastPoisonAreaRadius = self.getLastSafeCircleRadius(nextCenterStage)
        nowStamp = utils.getNow(False)
        if nowStamp - nextCenterStamp <= nextPoisonHoldTime:
            return lastPoisonAreaRadius
        nextShrinkTimePassTime = float(nextPoisonShrinkTime - (nowStamp - nextCenterStamp - nextPoisonHoldTime))
        if nextShrinkTimePassTime >= 0:
            curPoisonAreaRealRadius = nextPoisonAreaRadius + (lastPoisonAreaRadius - nextPoisonAreaRadius) * (nextShrinkTimePassTime / nextPoisonShrinkTime)
            return curPoisonAreaRealRadius
        else:
            return nextPoisonAreaRadius

    def getCurPoisonCirclePos(self, nextCenterStage, nextCenterStamp, curCenterPos, nextCenterPos):
        if nextCenterStage == 0:
            return nextCenterPos
        nextPoisonStageData = PSAD.data.get(nextCenterStage, {})
        nextPoisonHoldTime = nextPoisonStageData.get('holdTime', 0)
        nextPoisonShrinkTime = nextPoisonStageData.get('shrinkTime', 0)
        nowStamp = utils.getNow(False)
        if nowStamp - nextCenterStamp <= nextPoisonHoldTime:
            return [curCenterPos[0], curCenterPos[1], curCenterPos[2]]
        nextShrinkTimePassTime = float(nowStamp - nextCenterStamp - nextPoisonHoldTime)
        if nextShrinkTimePassTime < nextPoisonShrinkTime:
            timePassRatio = nextShrinkTimePassTime / nextPoisonShrinkTime
            xOffset = (nextCenterPos[0] - curCenterPos[0]) * timePassRatio
            zOffset = (nextCenterPos[2] - curCenterPos[2]) * timePassRatio
            realX = curCenterPos[0] + xOffset
            realZ = curCenterPos[2] + zOffset
            return [realX, nextCenterPos[1], realZ]
        else:
            return [nextCenterPos[0], nextCenterPos[1], nextCenterPos[2]]

    def getNextSafeCircleRadius(self, nextCenterStage):
        if nextCenterStage == 0:
            return DCD.data.get('pubgInitialCircleRadius', 5000)
        nextSafeAreaRadius = PSAD.data.get(nextCenterStage, {}).get('radius', 0)
        return nextSafeAreaRadius

    def getLastSafeCircleRadius(self, nextCenterStage):
        if nextCenterStage - 1 == 0:
            return DCD.data.get('pubgInitialCircleRadius', 5000)
        lastSafeAreaRadius = PSAD.data.get(nextCenterStage - 1, {}).get('radius', 0)
        return lastSafeAreaRadius

    def getPoisonCircleData(self, nextCenterStage, nextCenterStamp):
        result = dict()
        if nextCenterStage == 0:
            result['poisonState'] = pubgUtils.PUBG_POISON_STATE_END
            result['leftTime'] = 0
            result['allTime'] = 0
        else:
            curPoisonStageData = PSAD.data.get(nextCenterStage, {})
            curTimeStamp = utils.getNow()
            startTimeStamp = nextCenterStamp
            holdTime = curPoisonStageData.get('holdTime', 0)
            shrinkTime = curPoisonStageData.get('shrinkTime', 0)
            if curTimeStamp - startTimeStamp < holdTime:
                result['poisonState'] = pubgUtils.PUBG_POISON_STATE_HOLD
                result['leftTime'] = holdTime - (curTimeStamp - startTimeStamp)
                result['allTime'] = holdTime
            elif curTimeStamp - startTimeStamp - holdTime < shrinkTime:
                result['poisonState'] = pubgUtils.PUBG_POISON_STATE_SHRINK
                result['leftTime'] = shrinkTime - (curTimeStamp - startTimeStamp - holdTime)
                result['allTime'] = shrinkTime
            else:
                result['poisonState'] = pubgUtils.PUBG_POISON_STATE_END
                result['leftTime'] = 0
                result['allTime'] = 0
        result['leftTimeStr'] = utils.formatTimeStr(result['leftTime'], formatStr='m:s', zeroShow=True, sNum=2)
        return result

    def setDisasterDataInPubg(self):
        p = BigWorld.player()
        if p.curDisasterEndCBInPUBG:
            BigWorld.cancelCallback(p.curDisasterEndCBInPUBG)
        disasterInterval = DCD.data.get('pubgDestroyDisasterInterval', 1)
        p.curDisasterEndCBInPUBG = BigWorld.callback(disasterInterval, self.setDisasterEndInPubg)
        gameglobal.rds.ui.map.refreshDisasterIconInPUBG()
        gameglobal.rds.ui.littleMap.refreshDisasterIconInPUBG()

    def setDisasterEndInPubg(self):
        p = BigWorld.player()
        if p.curDisasterEndCBInPUBG:
            BigWorld.cancelCallback(p.curDisasterEndCBInPUBG)
            p.curDisasterEndCBInPUBG = None
        p.curDisasterDataInPUBG = dict()
        gameglobal.rds.ui.map.refreshDisasterIconInPUBG()
        gameglobal.rds.ui.littleMap.refreshDisasterIconInPUBG()

    def generalTeammateNoInPUBG(self):
        p = BigWorld.player()
        if p.isInPUBG() and p.curPUBGStateProgress >= pubgUtils.PUBG_STATE_PROGRESS_FLY_AIRPLANE:
            if not p.curTeamMemberInPUBG:
                p.curTeamMemberInPUBG = dict()
            gbIdList = p.members.keys()
            gbIdList.sort()
            for idx, gbId in enumerate(gbIdList):
                if not p.curTeamMemberInPUBG.get(gbId, None):
                    p.curTeamMemberInPUBG[gbId] = dict()
                p.curTeamMemberInPUBG[gbId]['idxInMap'] = idx + 1
                p.curTeamMemberInPUBG[gbId]['isDead'] = False

    def getMyTeammateNo(self):
        p = BigWorld.player()
        return p.getTeammateNoInPUBG(p.gbId)

    def getTeammateNoInPUBG(self, gbId):
        p = BigWorld.player()
        if p.isInPUBG():
            if p.curPUBGStateProgress >= pubgUtils.PUBG_STATE_PROGRESS_WAIT_AIRPLANE and p.curTeamMemberInPUBG.get(gbId, None):
                return p.curTeamMemberInPUBG[gbId].get('idxInMap', 0)
            else:
                return 0
        else:
            return 0

    def checkTeammateDeadInPUBG(self, gbId):
        p = BigWorld.player()
        return p.curTeamMemberInPUBG.get(gbId, {}).get('isDead', False)

    def getDeadTeammatePosInPUBG(self, gbId):
        p = BigWorld.player()
        return p.curTeamMemberInPUBG.get(gbId, {}).get('deadPos', (0, 0, 0))

    def getAllTeammateNoByGbId(self):
        pass

    def getOtherAliveTeamMateGbIdsInPUBG(self):
        p = BigWorld.player()
        entDataList = []
        for gbId, mInfo in p.members.iteritems():
            if gbId != p.gbId:
                idx = gameglobal.rds.ui.teamComm._getTeamIndex(mInfo['id'])
                hp = gameglobal.rds.ui.teamComm.getPyHp(idx, mInfo['id'])
                if hp > 0 and not p.checkTeammateDeadInPUBG(gbId):
                    entDataList.append([hp, gbId])

        entDataList.sort(cmp=lambda x, y: y[0] - x[0])
        idList = []
        for entData in entDataList:
            idList.append(entData[1])

        return idList

    def getOtherAliveTeamMateEntIdsInPUBG(self):
        p = BigWorld.player()
        entDataList = []
        for gbId, mInfo in p.members.iteritems():
            if gbId != p.gbId:
                idx = gameglobal.rds.ui.teamComm._getTeamIndex(mInfo['id'])
                hp = gameglobal.rds.ui.teamComm.getPyHp(idx, mInfo['id'])
                if hp > 0 and not p.checkTeammateDeadInPUBG(gbId):
                    entDataList.append([hp, mInfo['id']])

        entDataList.sort(cmp=lambda x, y: y[0] - x[0])
        idList = []
        for entData in entDataList:
            idList.append(entData[1])

        return idList

    def getTeamMateGbIdByEntIdInPUBG(self, entId):
        p = BigWorld.player()
        for gbId, mInfo in p.members.iteritems():
            if gbId != p.gbId:
                if mInfo['id'] == entId:
                    return gbId

        return 0

    def getMaxHpTeamMateGbIdInPUBG(self):
        p = BigWorld.player()
        idList = p.getOtherAliveTeamMateGbIdsInPUBG()
        if idList:
            return idList[0]
        else:
            return 0

    def getMaxHpTeamMateEntIdInPUBG(self):
        p = BigWorld.player()
        idList = p.getOtherAliveTeamMateEntIdsInPUBG()
        if idList:
            return idList[0]
        else:
            return 0

    def checkTeamMateInPUBG(self, gbId):
        p = BigWorld.player()
        if gbId in p.members:
            return True
        return False

    def checkTeamMateInPUBGByEndId(self, entId):
        p = BigWorld.player()
        for gbId, mInfo in p.members.iteritems():
            if mInfo['id'] == entId:
                return True

        return False

    def setTeammateMapMarkInPUBG(self, gbId, posX, posZ, littmeMapNo):
        p = BigWorld.player()
        if gbId not in p.allTeammateMapMark:
            p.allTeammateMapMark[gbId] = {}
        p.allTeammateMapMark[gbId]['posInWorld'] = [posX, 0, posZ]
        p.allTeammateMapMark[gbId]['littleMapNo'] = littmeMapNo
        gameglobal.rds.ui.map.refreshAllMarksIconInPUBG()
        gameglobal.rds.ui.littleMap.refreshAllMarksIconInPUBG()

    def pickNearItemsInPUBG(self, openAutoPickWidget = False):
        entities = gameglobal.rds.ui.pressKeyF.itemEnt
        gameglobal.rds.ui.pressKeyF.removeType(const.F_DROPPEDITEM)
        pubgAutoPick = gameglobal.rds.ui.pubgAutoPick
        if pubgAutoPick.isPUBGAutoPickOpening or openAutoPickWidget:
            if pubgAutoPick.isPUBGAutoPickInTreasureBox:
                return
            pubgAutoPick.show(entities)

    def checkCanPickAllItemsInPUBG(self):
        p = BigWorld.player()
        pubgAutoPick = gameglobal.rds.ui.pubgAutoPick
        if p.isInPUBG() and pubgAutoPick.isPUBGAutoPickOpening:
            pubgAutoPick.handlePickBtnClick(None)
            return True
        else:
            return False

    def pickTreasureBoxInPUBG(self, boxId, items):
        pubgAutoPick = gameglobal.rds.ui.pubgAutoPick
        if pubgAutoPick.isPUBGAutoPickInTreasureBox or not pubgAutoPick.isPUBGAutoPickOpening:
            pubgAutoPick.show(items, boxId=boxId)

    def closeTreasureBoxInPUBG(self, boxId):
        gameglobal.rds.ui.pubgAutoPick.hideByBoxId(boxId)

    def updateTreasureBoxInPUBG(self, boxId, itemUUID):
        if isinstance(itemUUID, list) or isinstance(itemUUID, tuple):
            gameglobal.rds.ui.pubgAutoPick.refreshAllByBoxId(boxId, itemUUID)
        elif isinstance(itemUUID, str):
            gameglobal.rds.ui.pubgAutoPick.refreshAllByBoxId(boxId, [itemUUID])

    def checkAutoPickTypeEnable(self, autoPickType):
        p = BigWorld.player()
        return p.autoPickSetting.get(autoPickType, 1)

    def setAutoPickTypeEnable(self, autoPickType, isEnabled):
        p = BigWorld.player()
        p.autoPickSetting[autoPickType] = isEnabled

    def checkEnableAutoPick(self):
        return BigWorld.player().autoPickEnable

    def setEnableAutoPick(self, enable):
        BigWorld.player().autoPickEnable = enable

    def checkPickFilterTypeEnable(self, filterType):
        p = BigWorld.player()
        return p.autoFilterSetting.get(filterType, 1)

    def setPickFilterTypeEnable(self, filterType, isEnabled):
        p = BigWorld.player()
        p.autoFilterSetting[filterType] = isEnabled

    def setUseItemAutoInPubg(self, kind, item, page, pos, isNew):
        p = BigWorld.player()
        if p.isInPUBG() and isNew:
            if item.type == Item.BASETYPE_EQUIP:
                if item.equipType in (Item.EQUIP_BASETYPE_WEAPON, Item.EQUIP_BASETYPE_ARMOR, Item.EQUIP_BASETYPE_JEWELRY):
                    part = p.getBestMainEquipPart(item)
                    if item.canEquip(p, part) == Item.EQUIPABLE:
                        p.curCanEquipListInPUBG.append([page, pos, item])
                    if not p.curEquippingInPUBGCB:
                        p.curEquippingInPUBGCB = BigWorld.callback(pubgUtils.SET_EQUIP_ITEM_AUTO_INTERVAL, p.realSetEquipItemAutoInPubg)
            if item.type == Item.BASETYPE_CONSUMABLE:
                if item.cstype in (Item.SUBTYPE_2_PUBG_SKILL_BOOK_LEARN, Item.SUBTYPE_2_PUBG_SKILL_BOOK_UNLOCK):
                    for idx in xrange(item.cwrap):
                        p.useBagItem(page, pos, fromBag=kind)

    def realSetEquipItemAutoInPubg(self):
        p = BigWorld.player()
        if not p:
            return
        else:
            p.curEquippingInPUBGCB and BigWorld.cancelCallback(p.curEquippingInPUBGCB)
            p.curEquippingInPUBGCB = None
            tempCanEquipDict = dict()
            for page, pos, item in p.curCanEquipListInPUBG:
                tempToCompareList = []
                dstPos = gametypes.EQU_PART_NONE
                partList = item.whereEquip()
                for part in partList:
                    if p.equipment.isEmpty(part):
                        if part in tempCanEquipDict:
                            tempToCompareList.append(tempCanEquipDict[part])
                        else:
                            dstPos = part
                            break
                    elif part in tempCanEquipDict:
                        tempToCompareList.append(tempCanEquipDict[part])
                    else:
                        tempToCompareList.append({'dstPos': part,
                         'item': p.equipment.get(part)})

                if tempToCompareList:
                    tempToCompareList.append({'item': item})
                    tempToCompareList.sort(cmp=p.setEquipItemAutoCmpInPUBG)
                    if tempToCompareList[-1]['item'].id != item.id:
                        dstPos = tempToCompareList[-1]['dstPos']
                if dstPos != gametypes.EQU_PART_NONE:
                    tempCanEquipDict[dstPos] = {'page': page,
                     'pos': pos,
                     'dstPos': dstPos,
                     'item': item}

            del p.curCanEquipListInPUBG[:]
            if tempCanEquipDict:
                result = []
                for value in tempCanEquipDict.itervalues():
                    result.append([value['page'], value['pos'], value['dstPos']])

                cellCmd.exchangeCrossInvEquList(result)
            return

    def setEquipItemAutoCmpInPUBG(self, itemData1, itemData2):
        return itemData2['item'].quality - itemData1['item'].quality

    def isPubgCommSkillLock(self, skillId):
        p = BigWorld.player()
        if p.isInPUBG():
            if p._isOnZaijuOrBianyao():
                return False
            else:
                if SQRD.data.has_key(skillId):
                    realSkillId = SQRD.data.get(skillId)
                else:
                    realSkillId = skillId
                if p.pubgUnlockedSkills and p.pubgUnlockedSkills.get(realSkillId, False):
                    return False
                return True
        return False

    def isPubgSkill(self, skillId):
        pubgBFGeneralSkills = DCD.data.get('pubgBFGeneralSkills', {})
        if skillId in pubgBFGeneralSkills:
            return True
        return False

    def checkCanUsePubgSkill(self, skillId):
        p = BigWorld.player()
        if not (p.pubgSkills and skillId in p.pubgSkills):
            p.showGameMsg(GMDD.data.PUBG_NOT_LEARN_PUBG_SKILL, ())
            return False
        return True

    def refreshAllSkillUIInPubg(self):
        gameglobal.rds.ui.actionbar.refreshActionbar()
        gameglobal.rds.ui.actionbar.setSpecialSlotShine()
        gameglobal.rds.ui.skill.refreshSkillList()
        gameglobal.rds.ui.skill.refreshNormalSkill()
        gameglobal.rds.ui.skill.refreshPSkill()
        gameglobal.rds.ui.skill.refreshWsPanel()

    def testSkyZonePUBG(self):
        p = BigWorld.player()
        zoneName, basePri, tgtPri = DCD.data.get('pubgsetSkyZonePriority')
        BigWorld.setZonePriority(zoneName, tgtPri)

    def testResetSkyZonePUBG(self):
        p = BigWorld.player()
        zoneName, basePri, tgtPri = DCD.data.get('pubgsetSkyZonePriority')
        BigWorld.setZonePriority(zoneName, basePri)

    def setSkyZoneInPUBGAtFixTime(self):
        p = BigWorld.player()
        zoneName, basePri, tgtPri = DCD.data.get('pubgsetSkyZonePriority')
        skyZoneTime = DCD.data.get('pubgsetSkyZoneTime', 0)
        if skyZoneTime > 0:
            p.skyZoneDataInPUBGCB = BigWorld.callback(skyZoneTime, Functor(p.realSetSkyZoneInPUBG, zoneName, tgtPri))

    def resetSkyZoneInPUBG(self):
        p = BigWorld.player()
        zoneName, basePri, tgtPri = DCD.data.get('pubgsetSkyZonePriority')
        if not p.skyZoneDataInPUBGCB:
            BigWorld.setZonePriority(zoneName, basePri)
        else:
            BigWorld.cancelCallback(p.skyZoneDataInPUBGCB)
            p.skyZoneDataInPUBGCB = None

    def realSetSkyZoneInPUBG(self, zoneName, tgtPri):
        p = BigWorld.player()
        p.skyZoneDataInPUBGCB and BigWorld.cancelCallback(p.skyZoneDataInPUBGCB)
        p.skyZoneDataInPUBGCB = None
        if p.isInPUBG() and zoneName and tgtPri:
            BigWorld.setZonePriority(zoneName, tgtPri)

    def setSoundInPUBGAtFixTime(self):
        p = BigWorld.player()
        pubgPlaySoundId = DCD.data.get('pubgPlaySoundId', 0)
        pubgPlaySoundTime = DCD.data.get('pubgPlaySoundTime', 0)
        if pubgPlaySoundTime > 0:
            p.playSoundInPUBGCB = BigWorld.callback(pubgPlaySoundTime, Functor(p.realSetSoundInPUBG, pubgPlaySoundId))

    def resetSoundInPUBG(self):
        p = BigWorld.player()
        pubgPlaySoundId = DCD.data.get('pubgPlaySoundId', 0)
        if not pubgPlaySoundId:
            return
        else:
            if not p.playSoundInPUBGCB:
                gameglobal.rds.sound.stopSound(pubgPlaySoundId)
            else:
                BigWorld.cancelCallback(p.playSoundInPUBGCB)
                p.playSoundInPUBGCB = None
            return

    def realSetSoundInPUBG(self, pubgPlaySoundId):
        p = BigWorld.player()
        p.playSoundInPUBGCB and BigWorld.cancelCallback(p.playSoundInPUBGCB)
        p.playSoundInPUBGCB = None
        if p.isInPUBG() and pubgPlaySoundId:
            gameglobal.rds.sound.playSound(pubgPlaySoundId)

    def getCurRankNameInPUBG(self):
        p = BigWorld.player()
        detail = {}
        if hasattr(p, 'pubgRankPoints'):
            detail = p.getRankDataInPUBGByRankPoint(p.pubgRankPoints)
        return detail.get('des', gameStrings.PUBG_PVP_BATTLE_FIELD_V2_RANK_DEFAULT_DES)

    def getRankDataInPUBGByRankPoint(self, rankPoint):
        for lv, detail in PRPD.data.iteritems():
            if detail['rank1'] <= rankPoint <= detail['rank2']:
                return detail

        return {}

    def getRankLvInPUBGByRankPoint(self, rankPoint):
        for lv, detail in PRPD.data.iteritems():
            if detail['rank1'] <= rankPoint <= detail['rank2']:
                return lv

        return 1

    def getRankDataInPUBGByLv(self, lv):
        return PRPD.data.get(lv, {})

    def pushPUBGNewOpenMsg(self):
        pushId = DCD.data.get('pubgNewOpenPushId', 0)
        if pushId:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)

    def removePUBGNewOpenMsg(self):
        pushId = DCD.data.get('pubgNewOpenPushId', 0)
        if pushId:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def setPUBGNewOpenMsgCallBack(self):
        pushId = DCD.data.get('pubgNewOpenPushId', 0)
        if pushId:
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': lambda : (gameglobal.rds.ui.pvPPanel.show(uiConst.PVP_BG_V2_TAB_PUBG) if gameglobal.rds.ui.pvpPUBG.isPUBGValid() else gameglobal.rds.ui.pvPPanel.show(uiConst.PVP_BG_V2_TAB_TODAY_BATTLE_FIELD))})
