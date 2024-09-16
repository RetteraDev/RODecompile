#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerProperty.o
from gamestrings import gameStrings
import sys
import time
import BigWorld
import Sound
import gametypes
import gameglobal
import const
import commcalc
import formula
import math
import gameCommonBitset
import commActivity
import skillDataInfo
import utils
import gamelog
import keys
import clientUtils
from InteractiveObject import InteractiveObject
from gameclass import SkillInfo
from gamestrings import gameStrings
from callbackHelper import Functor
from helpers import ufo
from helpers import protect
from helpers import cellCmd
from helpers import outlineHelper
from helpers import qingGong
from helpers import action
from helpers import ccControl
from helpers import navigator
from helpers.eventDispatcher import Event
from helpers import ccManager
from appSetting import Obj as AppSettings
from guis import uiUtils
from guis import events
from guis import ui
from guis import uiConst
from guis import chickenFoodFactory
from guis import groupDetailFactory
from helpers import aspectHelper
from sfx import sfx
from sfx import screenEffect
from sfx import keyboardEffect
from data import vip_service_data as VSDD
from data import message_desc_data as MSGDD
from data import zaiju_data as ZJD
from data import avatar_lv_data as ALD
from data import special_award_data as SAD
from data import school_switch_general_data as SSGD
from data import fishing_lv_data as FLD
from data import sys_config_data as SCD
from data import explore_lv_data as ELD
from data import feedback_data as FDK
from data import vp_level_data as VLD
from data import fame_data as FD
from data import life_skill_event_notify_data as LSEND
from data import kuiling_config_data as KCD
from data import effect_lv_data as EFLD
from cdata import game_msg_def_data as GMDD
from cdata import vp_stage_data as VSD
from data import tutorial_config_data as TCD
from data import teleport_spell_data as TSD
from data import state_data as SD
from data import ability_tree_phase_data as ATPD
from cdata import migrate_config_data as MCD
from data import business_config_data as BCD
from data import interactive_data as ID
from data import interactive_type_data as ITD
from data import couple_emote_basic_data as CEBD
from data import school_transfer_config_data as STCD
from data import npc_data as ND
from data import multi_carrier_data as MCDD
from data import wing_world_carrier_data as WWCD
from data import marriage_config_data as MCDDD
from cdata import personal_zone_config_data as PZCD
from skillDataInfo import ClientSkillInfo
import miniclient

class ImpPlayerProperty(object):

    def set_qinggongState(self, old):
        super(self.__class__, self).set_qinggongState(old)
        self._setEpRegen()
        if self.qinggongState != gametypes.QINGGONG_STATE_DEFAULT:
            if not hasattr(gameglobal.rds, 'tutorial'):
                return
            gameglobal.rds.tutorial.onQingGongState(self.qinggongState)
            gameglobal.rds.tutorial.onCheckQingGongState(self.qinggongState)
            if self.getOperationMode() == gameglobal.ACTION_MODE:
                self.ap.reset()
        elif hasattr(self.am, 'applyRunRoll'):
            if BigWorld.player().enableApplyModelRoll():
                self.am.maxModelRoll = gameglobal.MAX_RUN_MODEL_ROLL
                self.am.rollRunHalfLife = gameglobal.ROLL_RUN_HALFLIFE
        self.recordQingGongTime(self.qinggongState)
        self.recordSprint()
        if self.isPathfinding:
            navigator.getNav().setFakeFly(True)
        if old in (gametypes.QINGGONG_STATE_FAST_RUN, gametypes.QINGGONG_STATE_MOUNT_DASH) or old in gametypes.QINGGONG_WINGFLY_STATES:
            if self.qinggongState == gametypes.QINGGONG_STATE_DEFAULT:
                self.suggestSpriteRushStop()
        if self.qinggongState:
            qinggongDatat = self.getQingGongData(self.qinggongState)
            if qinggongDatat.get('suggestSpriteFly', False):
                self.suggestSpriteFly(True, False)
        if self.qinggongState != gametypes.QINGGONG_STATE_DEFAULT:
            keyboardEffect.addQinggongEffect()
        else:
            keyboardEffect.removeQinggongEffect()

    def recordSprint(self):
        if not self.inFuben():
            return
        if self.qinggongState in (gametypes.QINGGONG_STATE_FAST_SLIDING, gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND):
            self.sprintCount = self.sprintCount + 1
            if self.sprintCount == 3:
                self.cell.recordSprintLog()
        if self.qinggongState == 0:
            self.sprintCount = 0

    def enableApplyModelRoll(self):
        return False

    def set_inGroupFollow(self, old):
        self.setDelayGroupFollowState(False)
        if self.inGroupFollow:
            self.beginGroupFollow()
            gameglobal.rds.ui.disIndicator.show()
        else:
            gameglobal.rds.ui.disIndicator.hide()
        self._setSpeedFunc()

    def set_tCallTeamMemberExpire(self, old):
        gameglobal.rds.ui.teamComm.refreshCallMemberInfo()

    def isBlockFirework(self):
        try:
            return bool(int(AppSettings[keys.SET_BLOCK_FIREWORK]))
        except:
            return False

        return False

    def isEnableRandWing(self):
        try:
            return bool(int(AppSettings[keys.SET_ENABLE_RAND_WING]))
        except:
            return False

        return False

    def isShowHp(self):
        try:
            return bool(int(AppSettings[keys.SET_HP_SHOW]))
        except:
            return False

        return False

    def set_camp(self, old):
        super(self.__class__, self).set_camp(old)
        self._refreshAllNearByEntities()
        gameglobal.rds.ui.actionbar.checkSkillStatOnPropModified()
        ent = BigWorld.entities.values()
        for e in ent:
            if not hasattr(e, 'topLogo'):
                continue
            if e.topLogo:
                e.topLogo.updateRoleName(e.topLogo.name)

    def set_tempCamp(self, old):
        super(self.__class__, self).set_tempCamp(old)
        self._refreshAllNearByEntities()
        ent = BigWorld.entities.values()
        for e in ent:
            if not hasattr(e, 'topLogo'):
                continue
            if e.topLogo and hasattr(e, 'roleName'):
                e.topLogo.updateRoleName(e.topLogo.name)

    def set_curSocSchool(self, old):
        if self.curSocSchool == 0 and old != 0:
            gameglobal.rds.ui.roleInfo.removeSocialSkill(old)
            gameglobal.rds.ui.roleInfo.updateSocialPanel()
            gameglobal.rds.ui.roleInfo.updateSocialJob()

    def set_socProp(self, old):
        gameglobal.rds.ui.roleInfo.updateSocialPanel()

    def set_socExp(self, old):
        gameglobal.rds.ui.showLifeSkillLabel(uiConst.LIFE_SKILL_NUM_TYPE_SOCIAL_EXP, self.socExp - old)
        gameglobal.rds.ui.roleInfo.updateSocialExp()

    def set_socLv(self, old):
        p = BigWorld.player()
        oldYuLi = p.getCurYueLiVal(old)
        newYuLi = p.getCurYueLiVal()
        self.checkLifeSkillBreak(oldYuLi, newYuLi)
        gameglobal.rds.ui.showLifeSkillLabel(uiConst.LIFE_SKILL_NUM_TYPE_SOCIAL_LV, self.socLv)
        gameglobal.rds.ui.roleInfo.updateSocialLv()
        gameglobal.rds.ui.lifeSkillNew.refreshPanel()
        gameglobal.rds.ui.addNoviceHintPushMessage()

    def checkLifeSkillBreak(self, oldYuLi, newYuLi):
        reqValue = 0
        for id, data_item in ATPD.data.iteritems():
            reqValue += data_item.get('reqValue', 0)
            if oldYuLi < reqValue and newYuLi >= reqValue:
                gameglobal.rds.ui.lifeSkillBreak.show(id)
                break

    def set_signal(self, old):
        self.serverSignal = self.signal
        self.clientSetSignal(old)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CLIENT_SIGNAL_CHANGED)

    def clientSetSignal(self, old):
        aspectHelper.getInstance().hackSignal()
        super(self.__class__, self).set_signal(old)
        if commcalc.getSingleBit(old, gametypes.SIGNAL_SHOW_BACK) != commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_BACK):
            gameglobal.rds.ui.roleInfo.takeWearPhoto(None)

    def set_life(self, old):
        super(self.__class__, self).set_life(old)
        p = BigWorld.player()
        self.isWaitSkillReturn = False
        self.skillPlayer.castLoop = False
        self.castSkillBusy = False
        self.isGuiding = const.GUIDE_TYPE_NONE
        self.isAscending = False
        self.physics.endAccelerate()
        if self.life == gametypes.LIFE_DEAD:
            if self.playDyingEffect:
                screenEffect.delEffect(gameglobal.EFFECT_TAG_HP)
                self.playDyingEffect = False
                if self.playDyingSoundId > 0:
                    Sound.stopFx(self.playDyingSoundId)
                    self.playDyingSoundId = 0
            gameglobal.rds.ui.pressKeyF.hide()
            if gameglobal.rds.ui.breathbar.mediator:
                gameglobal.rds.ui.breathbar.mc.SetVisible(False)
            self.showGameMsg(GMDD.data.DIE, ())
            if self.inFubenTypes(const.FB_TYPE_ARENA):
                gameglobal.rds.sound.playSound(gameglobal.SD_64)
            gameglobal.rds.ui.player.setHp(0)
            if formula.inHuntBattleField(p.mapID) and not getattr(p, 'bfSideIndex', -1) == const.BATTLE_FIELD_HUNT_PROTECT_SIDE_INDEX:
                soundId = SCD.data.get('HUNT_SOUND_DIE', 5111)
                gameglobal.rds.sound.playSound(soundId)
        elif self.life == gametypes.LIFE_ALIVE:
            if gameglobal.rds.ui.deadAndRelive.isShow:
                gameglobal.rds.ui.deadAndRelive.hide()
            if self.inFubenTypes(const.FB_TYPE_ARENA):
                gameglobal.rds.sound.playSound(gameglobal.SD_66)
            if formula.inDotaBattleField(self.mapID):
                self.resetCamera()
                gameglobal.rds.ui.fightObserve.closeActionBar()
            self.qinggongMgr.state = qingGong.STATE_IDLE
        gameglobal.rds.ui.actionbar.checkSkillStatOnPropModified()
        self.clearDropForBlood()
        if old == gametypes.LIFE_ALIVE and self.life == gametypes.LIFE_DEAD:
            gameglobal.rds.tutorial.onDye()
        if gameglobal.rds.ui.fbDeadData.mediator:
            gameglobal.rds.ui.fbDeadData.hide()
        if gameglobal.rds.ui.fbDeadDetailData.mediator:
            gameglobal.rds.ui.fbDeadDetailData.hide()
        protect.nepActionRoleDeadAlive(1)
        self.wingWorldWarKillCnt = 0

    def set_arenaInfo(self, old):
        gameglobal.rds.ui.pvPPanel.refreshTab()
        gameglobal.rds.ui.arenaRankAward.refreshSeasonInfo()

    def _updateDeadAndRelive(self):
        gameglobal.rds.ui.deadAndRelive.setReliveNearBtnEnable(self.canReliveNear)
        gameglobal.rds.ui.deadAndRelive.tip = '' if self.canReliveNear else gameStrings.TEXT_AVATAR_1730

    def set_canReliveNear(self, old):
        if gameglobal.rds.ui.deadAndRelive.isShow:
            BigWorld.callback(5, self._updateDeadAndRelive)

    def set_followSpeed(self, old):
        self.set_speed(old)

    def set_speed(self, old):
        self._setSpeedFunc()

    def _setSpeedFunc(self):
        if self.ap != None:
            self.ap.setSpeed(self.speed[gametypes.SPEED_MOVE] / 60.0)
            if self.isRealGroupFollow() and self.isGroupSyncSpeed():
                pass
            elif self.bianshen[0]:
                horseSpeed = utils.getHorseSpeedBase(self) * self.getSpeedData().get('runFactor', 1.0)
                self.ap.setSpeed(horseSpeed)

    def set_weaponState(self, old):
        super(self.__class__, self).set_weaponState(old)
        if self.weaponState == gametypes.WEAR_BACK_ATTACH:
            gameglobal.rds.ui.actionbar.setRideShine(True, uiConst.SHOW_BACK_WEAR)
        elif self.weaponState == gametypes.WEAR_WAIST_ATTACH:
            gameglobal.rds.ui.actionbar.setRideShine(True, uiConst.SHOW_WAIST_WEAR)
        else:
            gameglobal.rds.ui.actionbar.setRideShine(False, uiConst.SHOW_BACK_WEAR)
            gameglobal.rds.ui.actionbar.setRideShine(False, uiConst.SHOW_WAIST_WEAR)
        if self.life == gametypes.LIFE_DEAD or self.weaponState == gametypes.WEAPON_HANDFREE:
            if old in (gametypes.WEAR_BACK_ATTACH, gametypes.WEAR_WAIST_ATTACH):
                BigWorld.player().hideZaijuUI()
                gameglobal.rds.ui.vehicleSkill.hide()

    def set_groupType(self, old):
        if self.isInTeam() and self.groupHeader:
            if not self.isInPUBG():
                if self.groupHeader == self.id:
                    gameglobal.rds.tutorial.onTeamActivate(const.TEAM_TUTORIAL_TYPE_HEADER)
                else:
                    gameglobal.rds.tutorial.onTeamActivate(const.TEAM_TUTORIAL_TYPE_MEMBER)
        if old != gametypes.GROUP_TYPE_RAID_GROUP and self.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
            gameglobal.rds.ui.group.showGroupTeam()
            gameglobal.rds.ui.team.close()
            ccManager.instance().logoutSession(const.CC_SESSION_TEAM)
        if old == gametypes.GROUP_TYPE_TEAM_GROUP and self.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
            gameglobal.rds.ui.chat.teamToGroup()
            gameglobal.rds.ui.memberDetailsV2.hide()
        if old == gametypes.GROUP_TYPE_NON_GROUP and self.groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
            gameglobal.rds.ui.team.refreshJoinTeam()
            if self.isTeamLeader():
                gameglobal.rds.ui.memberDetailsV2.show()
        self._refreshAllTeamer()
        gameglobal.rds.ui.chat.updatePadChannels()
        gameglobal.rds.ui.teamComm.refreshMemberInfo()
        gameglobal.rds.ui.refreshTeamLogoOrIdentity(self.id)
        gameglobal.rds.ui.playRecommActivation.refreshDailyRecommItems()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_GROUP_STATE)

    def set_groupNUID(self, old):
        super(self.__class__, self).set_groupNUID(old)
        if old > 0 and self.groupNUID == 0:
            ccManager.instance().logoutSession(const.CC_SESSION_TEAM)
            self.unloadWidgets()
            gameglobal.rds.sound.playSound(gameglobal.SD_29)
            self.refreshMonsterBloodColor()
            gameglobal.rds.ui.group.clearOnLeave()
            if hasattr(self, 'groupMark'):
                for key, value in self.groupMark.items():
                    ent = BigWorld.entities.get(key)
                    if ent:
                        ent.topLogo.removeTeamLogo()

                self.groupMark = {}
            self.othersInfo.clear()
            self.onResetMapMark()
            self.showQuickJoinGroup()
            leftMemid = []
            for key in self.members.keys():
                mid = self.members.get(key, {}).get('id', 0)
                leftMemid.append(mid)
                teamer = BigWorld.entity(mid)
                if teamer and teamer != self and getattr(teamer, 'IsAvatar', False):
                    BigWorld.callback(0, teamer.resetHiding)

            self.checkApplyGroupWithQuitGroupAuto()
            self.checkAcceptGroupWithQuitGroupAuto()
            self.removeTeamGuideBuff()
            self.closePartnerConfirm()
            gameglobal.rds.ui.playRecommActivation.refreshDailyRecommItems()
        if gameglobal.rds.ui.pressKeyF.monster:
            gameglobal.rds.ui.pressKeyF.monster.triggerTrap(True)
            if not gameglobal.rds.ui.pressKeyF.isMonster:
                gameglobal.rds.ui.pressKeyF.monster = None
        elif old == 0 and self.groupNUID > 0:
            self.applyer = []
            self._refreshMembers()
            gameglobal.rds.sound.playSound(gameglobal.SD_28)
            gameglobal.rds.ui.pushMessage.removeTeamPushMsg()
            self.refreshMonsterBloodColor()
            gameglobal.rds.ui.teamComm.setAssignInfo()
            gameglobal.rds.ui.quickJoin.onJoinGroupSucc()
            self.topLogo.updateRoleName(self.topLogo.name)
            self.resetWithQuitGroupAutoInfo()
            if utils.enableGroupDetailForcely() and self.inviteGroupFailedInfo.has_key('tgtRoleNameSet'):
                for tgtRoleName in self.inviteGroupFailedInfo['tgtRoleNameSet']:
                    self.inviteGroup(tgtRoleName)

                self.inviteGroupFailedInfo.pop('tgtRoleNameSet', None)
            gameglobal.rds.ui.questTrack.refreshLeaveHint(False)
        elif old > 0 and self.groupNUID > 0:
            ccManager.instance().logoutSession(const.CC_SESSION_TEAM)
            ccControl.leaveTeam(str(old))
            ccControl.joinTeam(str(self.groupNUID))
            self.doChangeTeamInCC(old, self.groupNUID)
            gameglobal.rds.ui.assign.closeTeambag()
            gameglobal.rds.ui.assign.reset()
        for tgt in BigWorld.entities.values():
            if utils.isOccupied(tgt):
                tgt.refreshOpacityState()
            if getattr(tgt, 'ybStatus', False):
                tgt.refreshYabiaoEffect()

        if self.groupNUID == 0:
            self.groupType = 0
            self.headerGbId = 0
            self.detailInfo = {}
            delMemIds = []
            for mgbid in self.members.keys():
                d = self.members[mgbid].get('id', 0)
                if d and d != self.id:
                    delMemIds.append(d)

            if delMemIds:
                self.cell.reqModTeamSubscribees([], delMemIds)
            self.members = {}
            self.smallTeamGbIds = []
            self.memberGuideQuests = {}
            gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_GROUP_MEMBER, uiConst.GROUP_BE_KICKED_OUT)
            self.onQuestInfoModifiedAtClient(const.QD_JIEQI, exData={'refreshAll': 1})
            self.applyer = []
            self.refreshMemberPos()
            self._refreshMemberBuffState(1)
            gameglobal.rds.ui.teamComm._resetPlayerProperty()
            gameglobal.rds.ui.teamComm.setAssignInfo()
            gameglobal.rds.ui.assign.closeTeambag()
            gameglobal.rds.ui.assign.closeDice()
            gameglobal.rds.ui.assign.closeAuction()
            gameglobal.rds.ui.assign.reset()
            gameglobal.rds.ui.assign.curGiveUp = False
            gameglobal.rds.ui.assign.auctionStep = -1
            gameglobal.rds.ui.assign.curAuctionPrice = 0
            gameglobal.rds.ui.assign.curAuctionPlayer = ''
            gameglobal.rds.ui.assign.setMaxAuctionTime()
            gameglobal.rds.ui.group.closeGroupInfoPanel()
            gameglobal.rds.ui.questTrack.refreshLeaveHint(True)
            gameglobal.rds.ui.huntGhost.onCancelGhost()
            for memid in leftMemid:
                if memid:
                    en = BigWorld.entity(memid)
                    p = BigWorld.player()
                    en and en.topLogo.updateRoleName(en.topLogo.name)
                    gameglobal.rds.ui.refreshTeamLogoOrIdentity(memid)

            self.inviteGroupFailedInfo.pop('tgtRoleNameSet', None)
            self.refreshTeamGuideBuff()
        gameglobal.rds.ui.refreshTeamLogoOrIdentity(self.id)
        self._refreshAllTeamer()
        gameglobal.rds.ui.chat.updatePadChannels()

    def set_groupIndex(self, old):
        super(self.__class__, self).set_groupIndex(old)
        self._refreshAllTeamer()

    def set_groupMatchStatus(self, old):
        gameglobal.rds.ui.fubenLogin.refreshFubenBtn()

    def set_fbAwardMultiple(self, old):
        gamelog.debug('hjx debug fuben#set_fbAwardMultiple:', self.fbAwardMultiple)
        if self.fbAwardMultiple == 0:
            return
        gameglobal.rds.ui.fuben.addAwardMultiple()

    def setExpXiuWei(self, value, old, srcId):
        self.expXiuWei = value
        gameglobal.rds.ui.roleInfo.refreshExpXiuWei()
        if self.expXiuWei > old:
            gameglobal.rds.ui.showRewardLabel(self.expXiuWei - old, const.REWARD_LABEL_YUANSHEN)

    def refreshMonsterBloodColor(self):
        inDota = formula.inDotaBattleField(getattr(self, 'mapID', 0))
        for ent in BigWorld.entities.values():
            if hasattr(ent, 'topLogo') and ent.topLogo and ent.IsMonster and ent.monsterOwnerGroupNUID != 0:
                if inDota:
                    ent.topLogo.setMonsterColorInDota(ent)
                elif self.groupNUID == ent.monsterOwnerGroupNUID or self.inFightForLoveFb():
                    ent.topLogo.setMonsterColor(True)
                else:
                    ent.topLogo.setMonsterColor(False)

    def isShowFeedbackIcon(self):
        triggerLvs = FDK.data.keys()
        if len(triggerLvs) == 0:
            return False
        if self.lv < min(triggerLvs):
            return False
        minIndex = 0
        for index, lv in enumerate(triggerLvs):
            if self.lv < lv:
                minIndex = index - 1
                break

        lv = triggerLvs[minIndex]
        if self.lvTriggerFlag.has_key(lv) and self.lvTriggerFlag[lv]:
            return False
        return True

    def isShowFeedbackWidget(self):
        triggerLvs = FDK.data.keys()
        if self.lv not in triggerLvs:
            return False
        if self.lvTriggerFlag.has_key(self.lv) and self.lvTriggerFlag[self.lv]:
            return False
        return True

    def set_lv(self, old):
        if getattr(self, 'isStraightLvUp', False):
            return
        else:
            miniclient.setCharLevel(self.lv)
            super(self.__class__, self).set_lv(old)
            gamelog.debug('@hjx bag#set_lv:', old, self.lv)
            gameglobal.rds.ui.expbar.setLevel(self.lv)
            gameglobal.rds.ui.expbar.setExp(self.exp)
            gameglobal.rds.ui.player.setLv(self.lv)
            gameglobal.rds.tutorial.onLevelUp(self.lv)
            self.showLvUpEffect()
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()
            gameglobal.rds.ui.inventory.updateMoneyBtn()
            gameglobal.rds.ui.storage.updateCurrentPageSlotState()
            gameglobal.rds.ui.actionbar.updateItemActionBar()
            canOpenRune = self.checkExcitementFeature(gametypes.EXCITEMENT_FEATURE_HIEROGRAM)
            openRuneLv = SCD.data.get('OPENRUNELV', 30)
            if self.lv >= openRuneLv and old < openRuneLv and canOpenRune:
                gameglobal.rds.ui.roleInfo.openRune()
            openQumoLv = SCD.data.get('OpenQumoLv', 30)
            if self.lv >= openQumoLv and old < openQumoLv:
                gameglobal.rds.ui.roleInfo.openQumo()
            openJunjieLv = SCD.data.get('OpenJunjieLv', 40)
            if self.lv >= openJunjieLv and old < openJunjieLv:
                gameglobal.rds.ui.roleInfo.openJunjie()
            openSocialLv = SCD.data.get('OpenSocialLv', 15)
            if self.lv >= openSocialLv and old < openSocialLv:
                gameglobal.rds.ui.roleInfo.openSocial()
            gameglobal.rds.ui.topBar.refreshActivityIcon()
            if gameglobal.rds.ui.topBar.isNeedRefreshLv(self.lv):
                gameglobal.rds.ui.topBar.refreshTopBarWidgets()
            self.updateRewardHallInfo(uiConst.REWARD_SHENJI)
            self.showGameMsg(GMDD.data.LEVEL_UP, (self.lv,))
            self.lvUpEquipPush()
            if self.isShowFeedbackWidget():
                gameglobal.rds.ui.feedback.showFeedback()
            gameglobal.rds.ui.roleInfo.refreshLvUpBtn()
            gameglobal.rds.ui.roleInfo.refreshJingjieInfo()
            gameglobal.rds.ui.roleInfoJingjie.refreshDetailInfo()
            gameglobal.rds.ui.skill.refreshSkillPracticeInfo(gameglobal.rds.ui.skill.skillId)
            gameglobal.rds.ui.skill.refreshAirSkillPanel()
            gameglobal.rds.ui.skill.refreshSkillList()
            gameglobal.rds.ui.questTrack.refreshRegionList()
            p = BigWorld.player()
            lvLimit = SCD.data.get('dailyAttendLv', 5)
            mallUseableMinLv = gameglobal.rds.ui.tianyuMall.getMallUseableMinLv()
            oldCheck = old >= mallUseableMinLv
            newCheck = self.lv >= mallUseableMinLv
            ziXunMinLv = SCD.data.get('ziXunMinLv', 0)
            pyqOpenLv = PZCD.data.get('pyqOpenLv', 0)
            if oldCheck != newCheck or (old >= pyqOpenLv) != (self.lv >= pyqOpenLv) or (old >= ziXunMinLv) != (self.lv >= ziXunMinLv):
                gameglobal.rds.ui.topBar.onUpdateClientCfg()
            spriteLv = SCD.data.get('showSprite', 17)
            if self.lv == spriteLv:
                gameglobal.rds.ui.spriteAni.show()
            for wsVal in self.wsSkills.itervalues():
                gameglobal.rds.ui.skill.checkWsProficiency(wsVal.skillId, wsVal.proficiency)

            appenticeLvLimit = TCD.data.get('appenticeLvLimit', 59)
            if self.lv == appenticeLvLimit and hasattr(self, 'mentorGbId') and self.mentorGbId > 0:
                gameglobal.rds.tutorial.onBeApprentice()
            gameglobal.rds.ui.topBar.checkTopBarCanShine()
            lvupEvent = Event(events.EVENT_ROLE_SET_LV, {'lv': self.lv,
             'oldLv': old})
            if self.lv >= SCD.data.get('importantRecommMinLv', 20):
                self.cell.queryImportantPlayRecommendInfo()
            gameglobal.rds.ui.newGuiderOperationHint.showOrHide()
            gameglobal.rds.ui.dispatchEvent(lvupEvent)
            migratePushLv = MCD.data.get('migratePushLv', 40)
            if self.lv >= migratePushLv:
                gameglobal.rds.ui.migrateServer.pushMigrate()
            gameglobal.rds.ui.addNoviceHintPushMessage()
            gameglobal.rds.ui.newbieGuide.checkLvLock()
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
            gameglobal.rds.ui.chat.updatePadChannels()
            if gameglobal.rds.configData.get('enableFriendInviteActivity', False) and self.lv == SCD.data.get('SummonFriendAcitityLv', 35):
                gameglobal.rds.ui.summonFriend.pushSummon()
            enableLvUpTip = gameglobal.rds.configData.get('enableLvUpTip', True)
            if enableLvUpTip:
                offsetH, offsetV = SCD.data.get('LvUpTipPos', (0, 0))
                gameglobal.rds.ui.showScreenUI('widgets/LvUpTip.swf', 46, True, offsetH, offsetV)
            if gameglobal.rds.configData.get('enableLowLvFreeSchoolTransfer', False):
                pushLv = STCD.data.get('lowLvFreeSchoolTransferPushLv', 20)
                if self.lv >= pushLv and old < pushLv:
                    gameglobal.rds.ui.schoolTransferSelect.addLowLvFreePush()
            if gameglobal.rds.configData.get('enableHierogram', False):
                gameglobal.rds.ui.roleInformationHierogram.refreshInfo()
                gameglobal.rds.ui.runeView.updatePskill()
                gameglobal.rds.ui.roleInfo.refreshHieroNotify()
                gameglobal.rds.ui.systemButton.showRoleInfoNotify()
            if self.inPreBreakLvDuration():
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_BREAK_LV_UP, {'click': self.searchBreakLvUp})
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_BREAK_LV_UP)
            gameglobal.rds.ui.memberDetailsV2.refreshMembers()
            gameglobal.rds.ui.accountBind.addPushMsg()
            for id in self.transportIdSet:
                entity = BigWorld.entities.get(id, None)
                if entity:
                    entity.refreshOpacityState()

            gameglobal.rds.ui.systemButton.relayoutByLv(self.lv, old)
            gameglobal.rds.ui.excitementIcon.refreshInfo()
            gameglobal.rds.ui.excitementDetail.refreshInfo()
            gameglobal.rds.ui.questTrack.showFindBeastTrack(False)
            groupDetailFactory.getActAvlInstance().refresh()
            gameglobal.rds.ui.player.resetHpMpPool()
            gameglobal.rds.ui.playRecommActivation.updateWeekActivationPushMsg()
            gameglobal.rds.ui.baiDiShiLianPush.tryStartTimer()
            gameglobal.rds.ui.wingWorldPush.checkState()
            self.checkPushNpc()
            return

    def set_questFlag(self, old):
        gameglobal.rds.ui.excitementIcon.refreshInfo()
        gameglobal.rds.ui.excitementDetail.refreshInfo()

    def searchBreakLvUp(self):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_BREAK_LV_UP)
        gameglobal.rds.ui.help.show(SCD.data.get('DESC_HELP_FOR_BREAK_LV_UP', ''))

    def set_ws(self, old):
        p = BigWorld.player()
        gameglobal.rds.ui.actionbar.setWS(p.ws, p.mws)
        gameglobal.rds.ui.actionbar.showWuShuangAnimation()
        gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_LACK_ENERGY)
        gameglobal.rds.ui.actionbar.changeWsBarState(self.ws[0] and self.ws[0] != old and self.ws[1] and self.ws[1] != old or self.inCombat)

    def set_hp(self, old):
        gamelog.debug('jorsef: impPlayerProperty#set_hp', old, self.hp, type(self.hp))
        super(self.__class__, self).set_hp(old)
        if hasattr(gameglobal.rds, 'tutorial') and self.mhp != 0:
            gameglobal.rds.tutorial.onHpByPercent(old, self.hp, self.mhp)
        gameglobal.rds.ui.player.setHp(self.hp)
        gameglobal.rds.ui.player.setMhp(self.mhp)
        if getattr(self, 'topLogo', None):
            if self.mhp != 0:
                self.topLogo.onUpdateHp()
        if gameglobal.rds.ui.zaiju.isShow:
            gameglobal.rds.ui.zaiju.setHpAndMp([self.hp,
             self.mhp,
             self.mp,
             self.mmp])
        elif gameglobal.rds.ui.zaijuV2.widget:
            gameglobal.rds.ui.zaijuV2.refreshPlayerHpAndMp(self.hp, self.mhp, self.mp, self.mmp)
        gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_LACK_ENERGY)
        gameglobal.rds.ui.roleInfo.refreshHpMp()
        if self.playDyingCallback:
            BigWorld.cancelCallback(self.playDyingCallback)
            self.playDyingCallback = None
        self.playDyingCallback = BigWorld.callback(0.1, self.showHpEffect)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_HP_CHANGE)
        gameglobal.rds.ui.spriteAni.propTipMsgHp(old)
        keyboardEffect.updateHpEffect()

    def set_hpHole(self, old):
        gamelog.debug('@yj: impPlayerProperty#set_hpHole', old, self.hpHole)
        if getattr(self, 'topLogo', None):
            if self.mhp != 0 and old != self.hpHole:
                self.topLogo.onUpdateHp()

    def set_mhp(self, old):
        super(self.__class__, self).set_mhp(old)
        if self.playDyingCallback:
            BigWorld.cancelCallback(self.playDyingCallback)
            self.playDyingCallback = None
        self.playDyingCallback = BigWorld.callback(0.1, self.showHpEffect)
        gameglobal.rds.ui.zaijuV2.refreshPlayerHpAndMp(self.hp, self.mhp, self.mp, self.mmp)

    def getRealHp(self, v = None):
        return self.hp

    def getRealMp(self, v = None):
        return self.mp

    def onUpdateTargetLockedInfo(self, hp, mp):
        pass

    def set_hpOthers(self, old):
        pass

    def set_mpOthers(self, old):
        pass

    def set_hpPercent(self, old):
        pass

    def set_mpPercent(self, old):
        pass

    def showHpEffect(self):
        if not hasattr(self, 'hp'):
            return
        hpRate = SCD.data.get('hpRate', 0.2)
        if gameglobal.rds.GameState > gametypes.GS_LOGIN and gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_PLAYING_TRACK_CAMERA and self.hp and self.life == gametypes.LIFE_ALIVE and float(self.hp) / self.mhp < hpRate:
            if not self.playDyingEffect:
                effectId = SCD.data.get('screenEffectHp', 1016)
                screenEffect.startEffect(gameglobal.EFFECT_TAG_HP, effectId)
                self.playDyingEffect = True
                path = 'fx/char/Shared/xintiao'
                self.playDyingSoundId = gameglobal.rds.sound.playFx(path, self.position, True, self)
        elif self.playDyingEffect and float(self.hp) / self.mhp > hpRate:
            screenEffect.delEffect(gameglobal.EFFECT_TAG_HP)
            self.playDyingEffect = False
            if self.playDyingSoundId > 0:
                Sound.stopFx(self.playDyingSoundId)
                self.playDyingSoundId = 0

    def set_flags(self, old):
        if self.isMoving and self._getFlag(gametypes.FLAG_REMOVE_STATE_ON_MOVE):
            self.cell.removeStateOnMove()

    def set_qumoLv(self, old):
        qumoLv = self.qumoLv
        if qumoLv > old:
            gameglobal.rds.ui.qumoLevelUp.showQumoPop()

    def set_publicFlags(self, old):
        if not commcalc.getBitDword(self.publicFlags, gametypes.FLAG_NOT_CONTROLLABLE) and commcalc.getBitDword(old, gametypes.FLAG_NOT_CONTROLLABLE) or not commcalc.getBitDword(self.publicFlags, gametypes.FLAG_NO_SKILL) and commcalc.getBitDword(old, gametypes.FLAG_NO_SKILL):
            self.updateUseSkillKeyState()
            self.updateActionKeyState()
        gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_NO_SKILL)
        super(self.__class__, self).set_publicFlags(old)

    def _canAddTianLei(self):
        if self.shengSiChangStatus == gametypes.SHENG_SI_CHANG_STATUS_START or self.sscStage == gametypes.DUEL_PHASE_RUNNING:
            return True
        else:
            return False

    def set_inCombat(self, oldInCombat):
        if not self.isInBfDota() and hasattr(self, 'topLogo') and self.topLogo and not gameglobal.gHidePlayerBlood:
            self.topLogo.showBlood(self.inCombat)
        if not self.isShowHp():
            gameglobal.rds.ui.player.changeHpTextShow(self.inCombat)
        if self.inCombat:
            if self.isDoingAction:
                cellCmd.cancelAction(const.CANCEL_ACT_IN_COMBAT)
            if gameglobal.rds.ui.shop.inRepair:
                gameglobal.rds.ui.shop.clearRepairState()
                gameglobal.rds.ui.messageBox.dismiss(uiConst.MESSAGEBOX_SHOP, False)
            self.qinggongMgr.setState(qingGong.STATE_IN_COMBAT_IDLE, True)
            self.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
            if self.weaponState in (gametypes.WEAR_BACK_ATTACH, gametypes.WEAR_WAIST_ATTACH):
                self.innerUpdateBackWear(True, False, False)
            if gameglobal.rds.ui.fullscreenFittingRoom.mediator:
                gameglobal.rds.ui.fullscreenFittingRoom.hide()
        else:
            if self.inFly:
                self.qinggongMgr.setState(qingGong.STATE_WINGFLY_IDLE, True)
            else:
                self.qinggongMgr.setState(qingGong.STATE_IDLE, True)
            self.isWaitSkillReturn = False
            spriteList = self.summonedSpriteLifeList + self.spriteBattleCallBackList
            self.summonedSpriteLifeList = []
            self.spriteBattleCallBackList = []
            gameglobal.rds.ui.summonedWarSpriteMine.updateSpriteLifeState()
            gameglobal.rds.ui.actionbar.refreshSummonedSprite(self.lastSpriteBattleIndex)
            gameglobal.rds.ui.summonedWarSpriteFight.refreshInfo()
            for index in spriteList:
                gameglobal.rds.ui.actionbar.refreshSummonedSprite(index)

            if self.checkInAutoQuest():
                if self.checkPathfinding():
                    self.cancelPathfinding()
                self.delayQuestSimpleFindPos()
            elif self.checkPathfinding() and gameglobal.rds.configData.get('enableRestartPathFindAfterCombat', False):
                type = self.lastPathFindInfo.get('type')
                if type == uiConst.RESTART_FIND_POS_TYPE_BY_ID:
                    self.cancelPathfinding()
                    seekId = self.lastPathFindInfo.get('seekId', 0)
                    uiUtils.findPosById(seekId)
                elif type == uiConst.RESTART_FIND_POS_TYPE_BY_POS:
                    self.cancelPathfinding()
                    spaceNo = self.lastPathFindInfo.get('spaceNo', 0)
                    pos = self.lastPathFindInfo.get('pos', 0)
                    uiUtils.findPosByPos(spaceNo, pos)
        gameglobal.rds.ui.player.setCombatVisible(self.inCombat)
        if self.summonedSpriteInWorld and self.summonedSpriteInWorld.mode == gametypes.SP_MODE_NOATK:
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.updateCombat(self.inCombat)
        self._setMpRegen(self.mp)
        gameglobal.rds.ui.actionbar.checkSkillStatOnPropModified()
        gameglobal.rds.littlemap.resetDeltaTime()
        gameglobal.rds.ui.actionbar.changeWsBarState(self.ws[0] and self.ws[1] or self.inCombat)
        gameglobal.rds.ui.qinggongBar.changeQinggongBarState(self.ep == self.mep, self.inCombat)
        gameglobal.rds.sound.switchCategoryInCombat(self.inCombat)
        Sound.setMusicParam('BATTLE', self.inCombat)
        if not oldInCombat and self.inCombat:
            obj = BigWorld.entities.get(self.interactiveObjectEntId)
            if obj and isinstance(obj, InteractiveObject):
                quitInteractiveWithBeHit = ID.data.get(obj.objectId, {}).get('quitInteractiveWithBeHit', 0)
                if quitInteractiveWithBeHit:
                    self.doQuitInteractive()
        super(self.__class__, self).set_inCombat(oldInCombat)

    def doQuitInteractive(self):
        self.cell.quitInteractive()

    def set_regenSpeed(self, old):
        self._setMpRegen(old)

    def set_regenRatioSpeed(self, old):
        self._setMpRegen(self.mp)

    def set_ep(self, old):
        BigWorld.callback(0.1, self._setEpRegen)
        if self.ep == self.mep:
            self.lastEpRegenTime = 0.0
        else:
            self.lastEpRegenTime = time.time()
        mep = self.mep
        reStartDashEpValue = SCD.data.get('reStartDashEpValue', 0.5)
        if mep and self.ep * 1.0 / mep > reStartDashEpValue and self.isPathfinding and self.qinggongMgr.checkCanQingGongPathFinding() and not self.canFly() and not self.isDashing and gameglobal.rds.configData.get('enableQingGongPathFinding', False) and not self.isGroupSyncSpeed():
            if AppSettings.get(keys.SET_QINGGONG_PATHFINDING, 1):
                if self.inFlyTypeWing():
                    qingGong.enterWingFlyDash(qingGong.GO_WINGFLY_DASH, self.qinggongMgr, shieldPathFinding=True)
                else:
                    qingGong.switchToDash(self, shieldPathFinding=True)
        gameglobal.rds.ui.qinggongBar.changeQinggongBarState(self.ep == self.mep, self.inCombat)

    def set_qingGongFlags(self, old):
        pass

    def _setEpRegen(self):
        gameglobal.rds.ui.player.setEp(self.ep)
        gameglobal.rds.ui.qinggongBar.setEp(self.ep)
        gameglobal.rds.ui.player.setMep(self.mep)
        if self.inCombat:
            v = self.combatEpRegen
        else:
            v = self.nonCombatEpRegenFix
        if self.qinggongState in gametypes.QINGGONG_CNT_COST:
            costData = qingGong.getQinggongData(self.qinggongState, self.inCombat)
            _, _, _, cntCost = costData
            v -= cntCost / 2.0
        if v > 0 and self.life != gametypes.LIFE_DEAD:
            t = (self.mep - self.ep) * 1.0 / v
            gameglobal.rds.ui.player.tweenEp(t, const.EP_ADD_NOINCOMBAT)
            gameglobal.rds.ui.qinggongBar.tweenEp(t, const.EP_ADD_NOINCOMBAT)
        elif v < 0 and self.life != gametypes.LIFE_DEAD:
            t = self.ep * 1.0 / -v
            gameglobal.rds.ui.player.tweenEp(t, const.EP_REDUCE)
            gameglobal.rds.ui.qinggongBar.changeQinggongBarState(False, self.inCombat)
            BigWorld.callback(2.0, self.updateQinggongState)
            gameglobal.rds.ui.qinggongBar.tweenEp(t, const.EP_REDUCE)
        else:
            gameglobal.rds.ui.player.stopTweenEp()
            gameglobal.rds.ui.qinggongBar.stopTweenEp()

    def updateQinggongState(self):
        if not self.inWorld:
            return
        gameglobal.rds.ui.qinggongBar.changeQinggongBarState(self.ep == self.mep, self.inCombat)

    def _setMpRegen(self, old):
        p = BigWorld.player()
        gameglobal.rds.ui.player.setSp(self.mp)
        gameglobal.rds.ui.player.setMsp(self.mmp)
        if gameglobal.rds.ui.zaiju.isShow:
            gameglobal.rds.ui.zaiju.setHpAndMp([self.hp,
             self.mhp,
             self.mp,
             self.mmp])
        elif gameglobal.rds.ui.zaijuV2.widget:
            gameglobal.rds.ui.zaijuV2.refreshPlayerHpAndMp(self.hp, self.mhp, self.mp, self.mmp)
        gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_LACK_ENERGY)
        if self.inDaZuo() or not p.isCanRegenMpInPUBG:
            gameglobal.rds.ui.player.stopTweenMp()
        else:
            v = self.regenSpeed[2] + self.regenRatioSpeed[2] * self.mmp
            if self.inCombat == False:
                v += self.regenSpeed[3] + self.regenRatioSpeed[3] * self.mmp
            if v > 0 and self.life != gametypes.LIFE_DEAD:
                t = (self.mmp - self.mp) / v
                gameglobal.rds.ui.player.tweenMp(t)
            else:
                gameglobal.rds.ui.player.stopTweenMp()

    def set_mp(self, old):
        super(self.__class__, self).set_mp(old)
        self.lastRegenTime = time.time()
        self._setMpRegen(old)
        gameglobal.rds.ui.roleInfo.refreshHpMp()
        gameglobal.rds.ui.spriteAni.propTipMsgMp(old)
        gameglobal.rds.ui.zaijuV2.refreshPlayerHpAndMp(self.hp, self.mhp, self.mp, self.mmp)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_MP_CHANGE)

    def set_mmp(self, old):
        gameglobal.rds.ui.zaijuV2.refreshPlayerHpAndMp(self.hp, self.mhp, self.mp, self.mmp)

    def set_ammoNum(self, old):
        gameglobal.rds.ui.actionbar.checkSkillStatOnPropModified()
        gameglobal.rds.ui.actionbar.setSchoolCenter()
        BigWorld.callback(0.2, gameglobal.rds.ui.roleInfo.refreshInfo)

    def set_ammoType(self, old):
        if not hasattr(self, 'modelServer'):
            return
        gamelog.debug('ypc@ set_ammoType change! old, new, ', old, self.ammoType)
        self.modelServer.onAmmoTypeChange()
        gameglobal.rds.ui.actionbar.setSchoolCenter()

    def set_tride(self, old):
        super(self.__class__, self).set_tride(old)
        p = BigWorld.player()
        if p.tride.inRide():
            gameglobal.rds.ui.rideTogether.show()
            gameglobal.rds.ui.mounts.show()
        else:
            gameglobal.rds.ui.rideTogether.clearWidget()
            if not p.isOnRideTogetherHorse():
                gameglobal.rds.ui.mounts.clearWidget()
        gameglobal.rds.ui.rideTogether.refreshRTlist()
        gameglobal.rds.ui.skill.refreshOtherSkillPanel()
        gameglobal.rds.ui.actionbar.refreshAllItembar()
        gameglobal.rds.ui.actionbar.refreshActionbar()
        gameglobal.rds.ui.mounts.refreshView()
        gameStrings.TEXT_IMPPLAYERPROPERTY_1039
        shine = p.tride.inRide()
        shine |= p.isOnRideTogetherHorse()
        gameglobal.rds.ui.actionbar.setRideShine(shine, uiConst.HORSE_RIDING)

    def set_carrier(self, old):
        gamelog.debug('-----m.l@ImpPlayerProperty.set_carrier', self.id, old, self.carrier)
        super(self.__class__, self).set_carrier(old)
        p = BigWorld.player()
        if self.carrier.carrierState in (gametypes.MULTI_CARRIER_STATE_CHECK_READY, gametypes.MULTI_CARRIER_STATE_RUNNING):
            forbiddenMultiUI = MCDD.data.get(self.carrier.carrierNo, {}).get('forbiddenMultiUI', 0)
            if not forbiddenMultiUI:
                gameglobal.rds.ui.multiCarrier.show(self.carrier.carrierNo)
            if self.carrier.has_key(self.id) and gameglobal.rds.ui.pressKeyF.isMovingPlatform:
                gameglobal.rds.ui.pressKeyF.isMovingPlatform = False
                gameglobal.rds.ui.pressKeyF.movingPlatform = None
                gameglobal.rds.ui.pressKeyF.removeType(const.F_MOVING_PLATFORM)
        else:
            gameglobal.rds.ui.multiCarrier.hide()
        if self.carrier.carrierState in (gametypes.MULTI_CARRIER_STATE_RUNNING, gametypes.MULTI_CARRIER_STATE_NONE):
            npcEnts = p.entitiesInRange(80, 'Npc')
            for ent in npcEnts:
                if ent and ent.inWorld:
                    nd = ND.data.get(ent.npcId, {})
                    if nd.has_key('multiCarrierHideList'):
                        ent.refreshOpacityState()

        gameglobal.rds.ui.multiCarrierNodeSelect.refreshInfo()
        if self.carrier.isReachCreateNum() and self.isTeamLeader():
            self.onMultiCarrierReadyFull(self.carrier.carrierNo)
        if self.checkMarriageCarrierMsg():
            self.addMarriagePrompt(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER)
        elif not self.checkMarriageCarrierMsg(True):
            self.removeMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER)

    def set_wingWorldCarrier(self, old):
        super(self.__class__, self).set_wingWorldCarrier(old)
        entId = self.wingWorldCarrier.carrierEntId
        carrier = BigWorld.entity(entId)
        if self.isOnWingWorldCarrier():
            gameglobal.rds.ui.pressKeyF.delEnt(entId, const.F_WING_WORLD_CARRIR)
            gameglobal.rds.ui.multiCarrier.show(self.wingWorldCarrier.carrierNo, uiConst.MUTLI_CARRIER_WING_WORLD)
            if carrier:
                carrier.setTargetCapsUse(False)
                if self.targetLocked == carrier:
                    self.unlockTarget()
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_PLAYER_UF, False)
            gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_PLAYER_UF, False)
            if WWCD.data.get(self.wingWorldCarrier.carrierNo, {}).get('forceActionMode', 0):
                self.lockOperationMode = (gameglobal.ACTION_MODE, self.getOperationMode())
                uiUtils.setAvatarPhysics(gameglobal.ACTION_MODE)
        else:
            entId = old.carrierEntId
            carrier = BigWorld.entity(entId)
            if carrier:
                carrier.refreshTrapCallback()
                carrier.setTargetCapsUse(True)
            gameglobal.rds.ui.multiCarrier.hide()
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_PLAYER_UF, True)
            gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_PLAYER_UF, True)
            if getattr(self, 'lockOperationMode', None):
                oldMode = self.lockOperationMode[1]
                self.lockOperationMode = None
                uiUtils.setAvatarPhysics(oldMode)
        self.resetPhysicsModel()

    def set_currentCandyCnt(self, old):
        gameglobal.rds.ui.littleScoreInfo.refreshFrame()

    def preloadZaiJuActionsAndEffects(self, skills):
        if not skills:
            return
        skillEffects = []
        skillActions = []
        for skillData in skills:
            clientSkillInfo = ClientSkillInfo(skillData[0], skillData[1])
            skillEffects.extend(skillDataInfo.getSkillEffect(clientSkillInfo))
            skillActions.extend(skillDataInfo.getSkillAction(clientSkillInfo))

        self.preloadEffect(skillEffects)
        self.preloadAction(skillActions)

    def set_bianshen(self, old):
        if not self.isJumping:
            self.restoreGravity()
        self.physics.fall = True
        super(self.__class__, self).set_bianshen(old)
        if not self.bianshen:
            return
        if self.bianshen[0] == gametypes.BIANSHEN_HUMAN:
            if old[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
                if gameglobal.rds.ui.zaiju.mediator:
                    self.hideZaijuUI(uiConst.ZAIJU_SHOW_TYPE_ZAIJU)
                if not formula.inHuntBattleField(BigWorld.player().mapID):
                    self.hideZaijuUI(uiConst.ZAIJU_SHOW_TYPE_ZAIJU)
                    chickenFoodFactory.getInstance().refreshCookingUI()
                self.hideZaijuUI(uiConst.ZAIJU_SHOW_TYPE_EXIT)
                gameglobal.rds.ui.vehicleSkill.hide()
                self.zaijuSkills.clear()
                if old[0] == gametypes.BIANSHEN_BIANYAO:
                    self._refreshYaoliState()
                gameglobal.rds.ui.actionbar.setSchoolCenter()
                self.autoSkill.init(old[1])
            else:
                gameglobal.rds.ui.actionbar.setRideShine(False, uiConst.HORSE_RIDING)
                gameglobal.rds.ui.skill.setRideShine(0, False)
                gameglobal.rds.ui.mounts.clearWidget()
        elif self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            gameglobal.rds.ui.actionbar.setRideShine(True, uiConst.HORSE_RIDING)
            gameglobal.rds.ui.skill.setRideShine(0, True)
            if BigWorld.player().isOnRideTogetherHorse():
                gameglobal.rds.ui.mounts.show()
        elif self.bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
            if old[0] == gametypes.BIANSHEN_RIDING_RB:
                gameglobal.rds.ui.actionbar.setRideShine(False, uiConst.HORSE_RIDING)
                gameglobal.rds.ui.skill.setRideShine(0, False)
            zjd = ZJD.data.get(self._getZaijuNo(), {})
            skills = list(zjd.get('skills', ())) + list(zjd.get('icons', ()))
            if zjd.get('preloadActsAndSfxs', False):
                self.preloadZaiJuActionsAndEffects(zjd.get('skills', ()))
            if zjd.get('replaceBar', 1) == 0:
                if formula.inHuntBattleField(BigWorld.player().mapID):
                    if gameglobal.rds.ui.vehicleSkill.widget:
                        gameglobal.rds.ui.vehicleSkill.refreshFrame()
                    else:
                        gameglobal.rds.ui.vehicleSkill.show()
                else:
                    self.showZaijuUI(skills)
                    chickenFoodFactory.getInstance().refreshCookingUI()
                if formula.inDotaBattleField(BigWorld.player().mapID):
                    self.onAvatarEnterDotaZaiju()
            else:
                if not formula.inHuntBattleField(BigWorld.player().mapID):
                    self.showZaijuUI(showType=uiConst.ZAIJU_SHOW_TYPE_EXIT)
                gameglobal.rds.ui.vehicleSkill.hide()
            for skillId, skillLv in skills:
                self.zaijuSkills[skillId] = skillDataInfo.SkillInfoVal(skillId, skillLv)

            if self.bianshen[0] == gametypes.BIANSHEN_BIANYAO and old[0] == gametypes.BIANSHEN_HUMAN:
                self._refreshYaoliState()
                gameglobal.rds.tutorial.onInYaoHua()
            gameglobal.rds.ui.actionbar.setSchoolCenter()
        self.castSkillBusy = False
        self.ap.recalcSpeed()
        self.ap.resetCameraAndDcursorRotate()
        self.physics.collideWithWater = self.isCollideWithWater()
        self.physics.dcControlPitch = self.needDcControlPitch()
        self.clearHoldingSkills()
        gameglobal.rds.ui.buffSkill.refreshVisible()
        self.ap.resetCameraPitchRange()

    def set_battleFieldDotaLv(self, old):
        super(self.__class__, self).set_battleFieldDotaLv(old)
        gameglobal.rds.ui.zaijuV2.refreshLv()
        gameglobal.rds.ui.bfDotaItemAndProp.refreshAttrs()
        self.playBfDotaLvUpEff()

    def set_battleFieldDotaExp(self, old):
        if not self.isInBfDota() or not self.bianshen[1]:
            return
        gameglobal.rds.ui.zaijuV2.refreshExp()

    def set_vehicleId(self, old):
        if old and not self.vehicleId:
            self.onLeaveVehicle(old)
            if self.summonedSpriteInWorld and not self.inFly and self.summonedSpriteInWorld.inFly:
                self.cell.spriteMasterPlaceOnVehicle(False)
        if not old and self.vehicleId:
            self.onEnterVehicle(old)

    def _refreshYaoliState(self):
        for e in BigWorld.entities.values():
            hasattr(e, 'refreshOpacityState') and e.refreshOpacityState()

        if self.targetLocked and self.targetLocked != self:
            ufoType = ufo.UFO_NORMAL
            target = self.targetLocked
            if self.isEnemy(target):
                ufoType = self.getTargetUfoType(target)
            self.setTargetUfo(target, ufoType)
        ent = BigWorld.entities.values()
        for e in ent:
            if not hasattr(e, 'topLogo'):
                continue
            if e.topLogo:
                e.topLogo.updateRoleName(e.topLogo.name)

        if self.target:
            if not (self.getOperationMode() == gameglobal.ACTION_MODE and not self.ap.showCursor):
                outlineHelper.setTarget(self.target)

    def set_skillPoint(self, old):
        gameglobal.rds.ui.skill.setSkillPoint()
        gameglobal.rds.ui.skill.refreshNormalSkill()
        gameglobal.rds.ui.systemButton.showSkillPoint()

    def set_battleFieldDotaSkillPoint(self, old):
        gameglobal.rds.ui.zaijuV2.refreshSkillPoints()

    def set_battleFieldDotaCash(self, old):
        gameglobal.rds.ui.bfDotaItemAndProp.refreshCash()
        gameglobal.rds.ui.bfDotaShopPush.refreshInfo()

    def set_battleFieldDotaTotalCash(self, old):
        if hasattr(self, 'bfDotaTotalCashDict'):
            self.bfDotaTotalCashDict[self.gbId] = self.battleFieldDotaTotalCash
        gameglobal.rds.ui.bfDotaDetail.refreshInfo()
        gameglobal.rds.ui.bfDotaSimple.refreshInfo()

    def set_schoolSwitchNo(self, old):
        super(self.__class__, self).set_schoolSwitchNo(old)
        if self.schoolSwitchNo > 0:
            self.skills.clear()
            self.wsSkills.clear()
            validSkills = [ x for x, needShow in SSGD.data[self.schoolSwitchNo].get('skillShows', []) if needShow ]
            for skillId, skillLv in SSGD.data[self.schoolSwitchNo].get('skills', []):
                if skillId in validSkills:
                    self.skills[skillId] = skillDataInfo.SkillInfoVal(skillId, skillLv)

            for wsSkillId, wsSkillLv in SSGD.data[self.schoolSwitchNo].get('wsskills', []):
                self.wsSkills[wsSkillId] = skillDataInfo.SkillInfoVal(wsSkillId, wsSkillLv)
                wsSkillInfo = SkillInfo(wsSkillId, wsSkillLv)
                if wsSkillInfo.hasSkillData('wsNeed1'):
                    self.wsSkills[wsSkillId].wsType = 1
                    self.wsSkills[wsSkillId].isWsSkill = True
                elif wsSkillInfo.hasSkillData('wsNeed2'):
                    self.wsSkills[wsSkillId].wsType = 2
                    self.wsSkills[wsSkillId].isWsSkill = True
                self.wsSkills[wsSkillId].enable = True
                self.wsSkills[wsSkillId].slots = []
                self.wsSkills[wsSkillId].proficiency = {}

            gameglobal.rds.ui.player.refreshUnitType()
            gameglobal.rds.ui.actionbar.refreshActionbarColor()
            if gameglobal.rds.ui.skill.mediator:
                gameglobal.rds.ui.skill.hide()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.hide()
            if gameglobal.rds.ui.mail.mediator or gameglobal.rds.ui.mail.mailMediator:
                gameglobal.rds.ui.mail.hide()
            if gameglobal.rds.ui.consign.mediator:
                gameglobal.rds.ui.consign.hide()
            if gameglobal.rds.ui.skill.lifeMediator:
                gameglobal.rds.ui.skill.closeLifeSkill()
            if gameglobal.rds.ui.skill.generalMediator:
                gameglobal.rds.ui.skill.closeGeneralSkill()
            if gameglobal.rds.ui.questLog.mediator:
                gameglobal.rds.ui.questLog.hide()
            if gameglobal.rds.ui.team.mediator:
                gameglobal.rds.ui.team.hide()
            if gameglobal.rds.ui.friend.mediator:
                gameglobal.rds.ui.friend.hide(False)
            if gameglobal.rds.ui.ranking.mediator:
                gameglobal.rds.ui.ranking.hide()
            if gameglobal.rds.ui.roleInfo.mediator:
                gameglobal.rds.ui.roleInfo.hide()
            gameglobal.rds.ui.actionbar.setRideShine(False, uiConst.HORSE_RIDING)
            gameglobal.rds.ui.equipRepair.setEquipState()
            gameglobal.rds.ui.roleInfo.schoolSwitchPotential()
            if self.ammoType == 0 or self.ammoNum == 0:
                gameglobal.rds.ui.bullet.hide()
        else:
            gameglobal.rds.ui.player.refreshUnitType()
            gameglobal.rds.ui.actionbar.refreshActionbarColor()
            self.topLogo.updateRoleName(self.topLogo.name)
            gameglobal.rds.ui.actionbar.setRideShine(False, uiConst.HORSE_RIDING)
            gameglobal.rds.ui.equipRepair.setEquipState()
            gameglobal.rds.ui.roleInfo.updateAllPotential()
            gameglobal.rds.ui.roleInfo.updatePotBtnVisible()
            if gameglobal.rds.ui.roleInfo.mediator:
                gameglobal.rds.ui.roleInfo.hide()
            if self.ammoType == 0 or self.ammoNum == 0:
                gameglobal.rds.ui.bullet.hide()
        gameglobal.rds.ui.actionbar.skillInfoCache.clear()

    def set_inFly(self, old):
        self.wingStateTime = (self.inFly, time.time())
        super(self.__class__, self).set_inFly(old)
        gameglobal.rds.ui.actionbar.setRideShine(self.inFlyTypeWing(), uiConst.WING_FLYING)
        gameglobal.rds.ui.skill.setRideShine(1, self.inFlyTypeWing())
        self.ap.moveAfterJump = False
        if self.inFlyTypeFlyRide() and self.qinggongState == gametypes.QINGGONG_STATE_MOUNT_DASH:
            qingGong.enterWingFlyDash(qingGong.GO_WINGFLY_DASH, self.qinggongMgr)
        if not self.inFly:
            self.ap.stopMove()
            self.ap.endFlyAccelerate(True)
            self.updateActionKeyState()
            self.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
            if self.fashion.doingActionType() != action.JUMP_ACTION:
                self.ap.setUpSpeedMultiplier()
                self.ap.flyUp(False, False)
        inAirBattle = gameglobal.rds.ui.skill.inAirBattleState()
        gameglobal.rds.ui.airbar.showAirbar(inAirBattle)
        gameglobal.rds.ui.fightObserve.resetObserveMode()
        if self.isInBfDota():
            self.refreshVehicleInDota()
        if not old and self.inFly:
            if self.summonedSpriteInWorld:
                self.suggestSpriteFly(True, False)
            gameglobal.rds.tutorial.onInFly()
        elif old and not self.inFly:
            if self.spriteObjId:
                self.suggestSpriteFly(False)
        if self.inFly:
            keyboardEffect.exchangeAllSlotEffect(keyboardEffect.NOT_FLY_SKILL_TYPES, keyboardEffect.FLY_SKILL_TYPES)
        else:
            keyboardEffect.exchangeAllSlotEffect(keyboardEffect.FLY_SKILL_TYPES, keyboardEffect.NOT_FLY_SKILL_TYPES)

    def refreshVehicleInDota(self):
        if self.inFly:
            if self.vehicleId:
                self.leaveVehicle(self.vehicleId)

    def set_daZuoState(self, old):
        super(self.__class__, self).set_daZuoState(old)

    def set_teleportSpell(self, old):
        super(self.__class__, self).set_teleportSpell(old)

    def enterTeleportSpell(self, spellId, callback):
        self.ap.stopMove()
        self.cell.enterTeleportSpell(spellId)
        data = TSD.data.get(spellId)
        duration = data.get('duration')
        self.teleportCB = BigWorld.callback(duration, Functor(self.teleportSpellCallback, callback))

    def teleportSpellCallback(self, callback):
        self.cancelTeleportSpell()
        if callback:
            callback()

    def cancelTeleportSpell(self):
        self.cell.leaveTeleportSpell()
        if self.fashion._doingActionType in (action.TELEPORT_SPELL_ACTION,):
            self.fashion.stopAction()
        self.releaseTeleportEffect()

    def set_fishingExp(self, old):
        gameglobal.rds.ui.lifeSkillNew.addFishingPushMsg()
        if gameglobal.rds.ui.skill.lifeMediator:
            gameglobal.rds.ui.skill.refreshFishingSkillPanel()
        gameglobal.rds.ui.lifeSkillNew.refreshPanel()

    def set_fishingLv(self, old):
        if FLD.data.has_key(self.fishingLv):
            self.showGameMsg(GMDD.data.FISHING_LV_UP, (FLD.data[self.fishingLv].get('name', ''), self.fishingLv))
            if gameglobal.rds.ui.skill.lifeMediator:
                gameglobal.rds.ui.skill.refreshFishingSkillPanel()
            gameglobal.rds.ui.lifeSkillNew.refreshPanel()
            lvupEvent = Event(events.EVENT_LIFE_SKILL_UPDATE, {})
            gameglobal.rds.ui.dispatchEvent(lvupEvent)

    def set_wushuang1(self, old):
        if gameglobal.rds.ui.skill.wushuangSkillPanelMc:
            BigWorld.callback(0.5, gameglobal.rds.ui.skill.refreshSpecialSkillWithoutIcon)

    def set_wushuang2(self, old):
        if gameglobal.rds.ui.skill.wushuangSkillPanelMc:
            BigWorld.callback(0.5, gameglobal.rds.ui.skill.refreshSpecialSkillWithoutIcon)

    def set_junJieVal(self, old):
        gameglobal.rds.ui.roleInfo.refreshJunjiePanel()

    def set_junJieLv(self, old):
        gameglobal.rds.ui.roleInfo.refreshJunjiePanel()
        jingJie = self.junJieLv
        gameglobal.rds.ui.roleInformationJunjie.initUI()
        if jingJie > old:
            gameglobal.rds.ui.qumoLevelUp.showJunjiePop()

    def set_zhanXunBonusApplied(self, old):
        gameglobal.rds.ui.roleInfo.refreshJunjiePanel()

    def set_compositeShopItemBuyLimit(self, old):
        if gameglobal.rds.ui.compositeShop.isOpen:
            gameglobal.rds.ui.compositeShop.refreshBuyLimitInfo()
        gameglobal.rds.ui.yunChuiShop.refresh()

    def getFame(self, fameId):
        if self.fame.has_key(fameId):
            return self.fame[fameId]
        return utils.getFameInitVal(fameId, self.school)

    def getFameMaxVal(self, fameId):
        return FD.data.get(fameId, {}).get('maxVal', 1)

    @property
    def isHadNewFame(self):
        for _, value in self.isNewFameRecord.iteritems():
            if value:
                return True

        return False

    def fameUpdate(self, fameId, value, nWeek, mWeek, nDay, extraValue, mLastWeekExtra, fameTransferParam):
        gamelog.debug('@zs fameUpdate', fameId, value, nWeek, mWeek)
        if not hasattr(self, 'fame'):
            self.fame = {}
        if not self.fame.has_key(fameId) and value > 0 and FD.data.get(fameId, {}).get('display', 0) == gametypes.FAME_SHOW_IN_HONORPANEL:
            self.isNewFameRecord[fameId] = True
            gameglobal.rds.ui.systemButton.showRoleInfoNotify()
            gameglobal.rds.ui.tweenMc.tweenFame(fameId)
        diff = value - self.getFame(fameId)
        oldValue = self.getFame(fameId)
        self.fame[fameId] = value
        self.fameWeek[fameId] = (nWeek, mWeek)
        self.fameDay[fameId] = nDay
        gameglobal.rds.ui.roleInfoFame.updateFame(fameId)
        if fameId == const.JUN_ZI_FAME_ID:
            gameglobal.rds.ui.arena.setFame(value)
            gameglobal.rds.ui.battleField.setFame(value)
            gameglobal.rds.ui.roleInfo.setJunZiWeekVal(nWeek)
            gameglobal.rds.ui.roleInformationJunjie.setJunZiWeekVal(nWeek)
            gameglobal.rds.ui.roleInformationJunjie.initJunzi()
            gameglobal.rds.ui.roleInfo.refreshJunjiePanel()
        elif fameId == const.ZHAN_XUN_FAME_ID:
            gameglobal.rds.ui.roleInfo.refreshJunjiePanel()
            self.updateRewardHallInfo(uiConst.REWARD_JUNJIE)
        elif fameId == const.ARENA_PLAYOFFS_BET_FAME_ID:
            gameglobal.rds.ui.arenaPlayoffsBet.refreshTotalAmountInfo()
        elif fameId == const.ABILITY_FAME_TANSUO:
            gameglobal.rds.ui.lifeSkillNew.refreshPanel()
        elif fameId == const.ABILITY_FAME_WEIWANG:
            gameglobal.rds.ui.lifeSkillNew.refreshPanel()
        elif fameId == const.FAME_TYPE_ORG:
            gameglobal.rds.ui.delegationBook.updateFame(fameId, oldValue, value)
        elif fameId == const.QUMO_FAME_ID:
            gameglobal.rds.ui.roleInfo.updateQumoFame(value, nWeek, mWeek, mLastWeekExtra)
            gameglobal.rds.ui.roleInformationQumo.updateQumoFame(value, nWeek, mWeek, mLastWeekExtra)
        elif fameId == BCD.data.get('businessFameId', 0):
            gameglobal.rds.ui.guildBusinessShop.refreshShopInfo()
            gameglobal.rds.ui.guildBusinessShop.refreshPackageInfo()
            gameglobal.rds.ui.guildBusinessBag.updateOtherInfo()
        elif fameId == const.APPERANCE_ITEM_COLLECT_FAME_ID:
            gameglobal.rds.ui.guibaoge.refreshView()
        elif fameId == const.YUN_CHUI_JI_FEN_FAME_ID:
            gameglobal.rds.ui.inventory.updataMoney()
            gameglobal.rds.ui.yunChuiShop.setCash()
            gameglobal.rds.ui.yunChuiShop.refreshBuyItemData()
            gameglobal.rds.ui.activityShop.refreshBuySetting()
            gameglobal.rds.ui.equipChangeInlay.refreshAll()
            gameglobal.rds.ui.equipChangeUnlock.refreshAll()
            gameglobal.rds.ui.equipChangeEnhance.refreshConsumeInfo()
            gameglobal.rds.ui.generalBet.refreshCash()
        elif fameId in (gametypes.RECOMMEND_WENQUAN_JIULI, gametypes.RECOMMEND_WENQUAN_SHILIANG):
            if gameglobal.rds.ui.wenQuanDetail.isShow:
                gameglobal.rds.ui.wenQuanDetail.updateValue()
        elif fameId == const.XING_CHEN_ZHI_LIN_FAME_ID:
            gameglobal.rds.ui.equipSoul.refreshEnergyInfo()
        elif fameId == const.REFORGE_EQUIP_JUEXING_FAME_ID:
            gameglobal.rds.ui.equipChangeJuexingRebuild.refreshConsumeInfo()
        if gameglobal.rds.ui.compositeShop.isOpen:
            gameglobal.rds.ui.compositeShop.refreshBuyItemDisplayData()
        for val in KCD.data.itervalues():
            if fameId == val.get('fameId', -1):
                gameglobal.rds.ui.lifeSkillNew.refreshPanel()
                break

        fameName = FD.data.get(fameId, {}).get('name', '')
        if diff > 0:
            label = FD.data[fameId].get('label', 0)
            if label:
                if label != const.DEFAULT_LABEL_FAME:
                    gameglobal.rds.ui.showRewardLabel(diff, label + const.REWARD_LABEL_FAME)
                else:
                    gameglobal.rds.ui.showDefaultLabel(fameName, diff, '#47E036')
            if fameTransferParam:
                transFameId, transFameVal = fameTransferParam
                transFameName = FD.data.get(transFameId, {}).get('name', '')
                self.showGameMsg(GMDD.data.FAME_TOKEN_ADD_TRANSFORM, (fameName,
                 diff,
                 transFameName,
                 transFameVal))
            elif not FD.data.get(fameId, {}).get('notifyAddFromServer', 0):
                if extraValue > 0:
                    msgId = getattr(GMDD.data, 'FAME_INCREASE_%d_EXTRA' % fameId, 0)
                    if msgId:
                        self.showGameMsg(msgId, (diff, extraValue))
                    elif clientUtils.notifyFame(fameId):
                        self.showGameMsg(GMDD.data.FAME_INCREASE, (fameName, diff, extraValue))
                else:
                    msgId = getattr(GMDD.data, 'FAME_INCREASE_%d' % fameId, 0)
                    if msgId:
                        self.showGameMsg(msgId, diff)
                    elif clientUtils.notifyFame(fameId):
                        self.showGameMsg(GMDD.data.FAME_INCREASE, (fameName, diff))
            if (uiConst.LIFE_SKILL_EVENT_FAME, fameId) in LSEND.data:
                gameglobal.rds.ui.dynamicResult.showResult(uiConst.LIFE_SKILL_EVENT_FAME, fameId)
            if fameId == const.REWARD_WASTE_CRYSTAL_1_FAME_ID:
                gameglobal.rds.ui.showRewardLabel(diff, const.REWARD_LABEL_WASTE_CRYSTAL_1)
            elif fameId == const.REWARD_WASTE_CRYSTAL_2_FAME_ID:
                gameglobal.rds.ui.showRewardLabel(diff, const.REWARD_LABEL_WASTE_CRYSTAL_2)
            elif fameId == const.REWARD_WASTE_CRYSTAL_3_FAME_ID:
                gameglobal.rds.ui.showRewardLabel(diff, const.REWARD_LABEL_WASTE_CRYSTAL_3)
            elif fameId == const.REWARD_WASTE_SUMMON_SPRITE_CRYSTAL:
                gameglobal.rds.ui.showRewardLabel(diff, const.REWARD_LABEL_SUMMON_SPRITE_WASTE_CRYSTAL)
        elif diff < 0 and clientUtils.notifyFame(fameId):
            self.showGameMsg(GMDD.data.FAME_DECREASE, (fameName, -diff))
        if gameglobal.rds.ui.purchaseShop.mediator:
            gameglobal.rds.ui.purchaseShop.refreshFameData()
        gameglobal.rds.ui.roleInfoHonor.fameUpdate()
        gameglobal.rds.ui.topBar.setValueByName('fame_' + str(fameId))
        fEvent = Event(events.EVENT_FAME_UPDATE, fameId)
        gameglobal.rds.ui.dispatchEvent(fEvent)

    def set_weeklyQumoCollectPoints(self, old):
        if gameglobal.rds.ui.roleInfo.mediator:
            gameglobal.rds.ui.roleInfo.refreshQumoPanel()
        if gameglobal.rds.ui.roleInformationQumo.widget:
            gameglobal.rds.ui.roleInformationQumo.initWeekReward()
        self.checkQumoBonus()
        self.updateRewardHallInfo(uiConst.REWARD_QUMO)

    def fameSend(self, fameInfo):
        gamelog.debug('@zs fameSend', fameInfo)
        self.fame = {}
        for fameId, value in fameInfo.iteritems():
            self.fame[fameId] = value[0]
            self.fameWeek[fameId] = (value[1], value[2])
            self.fameDay[fameId] = value[3]
            if fameId == const.JUN_ZI_FAME_ID:
                gameglobal.rds.ui.arena.setFame(value[0])
                gameglobal.rds.ui.battleField.setFame(value[0])
                gameglobal.rds.ui.roleInfo.setJunZiWeekVal(value[1])
                gameglobal.rds.ui.roleInformationJunjie.setJunZiWeekVal(value[1])
            if fameId == const.QUMO_FAME_ID:
                gameglobal.rds.ui.roleInfo.updateQumoFame(value[0], value[1], value[2], value[4])
                gameglobal.rds.ui.roleInformationQumo.updateQumoFame(value[0], value[1], value[2], value[4])

    def socSchoolSend(self, ssInfo):
        self.socSchools = {}
        for key, value in ssInfo.iteritems():
            self.socSchools[key] = value

        gameglobal.rds.ui.roleInfo.updateSocialPanel()
        gameglobal.rds.ui.roleInfo.updateSocialJob()

    def _updatePkTopLogo(self, players = []):
        tList = []
        if not players:
            for en in BigWorld.entities.values():
                if en.__class__.__name__ == 'Avatar' and en.topLogo:
                    tList.append(en)
                elif en.__class__.__name__ == 'ClanWarReliveBoard' and not self.clanWarStatus and en.topLogo:
                    tList.append(en)

        else:
            tList = players
        for en in tList:
            if not en.topLogo:
                continue
            if en.IsClanWarUnit:
                en.topLogo.updateRoleName(en.topLogo.name)
            elif not self.isInClanWar() or not en.isInClanWar():
                en.topLogo.updateRoleName(en.topLogo.name)

        if self.targetLocked and self.targetLocked.IsAvatar:
            target = self.targetLocked
            ufoType = ufo.UFO_NORMAL
            if self.isEnemy(target):
                ufoType = self.getTargetUfoType(target)
            self.setTargetUfo(target, ufoType)
        if self.targetLocked and self.targetLocked in players:
            gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_SKILL_TGT)

    def set_pkProtectMode(self, old):
        for en in BigWorld.entities.values():
            if en.__class__.__name__ == 'Avatar' and en.topLogo:
                en.topLogo.updateRoleName(en.topLogo.name)

        if self.targetLocked and self.targetLocked.IsAvatar:
            target = self.targetLocked
            ufoType = ufo.UFO_NORMAL
            if self.isEnemy(target):
                ufoType = self.getTargetUfoType(target)
            self.setTargetUfo(target, ufoType)

    def set_pkMode(self, old):
        super(self.__class__, self).set_pkMode(old)
        self.topLogo.updatePkTopLogo()
        self._updatePkTopLogo()
        if self.pkMode in (const.PK_MODE_KILL, const.PK_MODE_HOSTILE):
            self.lastSwitchPKModeStamp = utils.getNow()

    def set_pkProtectLv(self, old):
        pass

    def set_pkDefenseGbIdList(self, old):
        gamelog.debug('@zspk set_pkDefenseGbIdList', self.pkDefenseGbIdList)
        oldSet = set(self.oldPkDefenseGbIdList)
        newSet = set(self.pkDefenseGbIdList)
        diff = newSet - oldSet
        diff |= oldSet - newSet
        self.oldPkDefenseGbIdList = self.pkDefenseGbIdList
        players = []
        for en in BigWorld.entities.values():
            if en.__class__.__name__ == 'Avatar' and en.topLogo and en.gbId in diff:
                players.append(en)

        self._updatePkTopLogo(players)

    def set_inClanWar(self, old):
        super(self.__class__, self).set_inClanWar(old)
        for en in BigWorld.entities.values():
            if en.__class__.__name__ == 'Avatar' and en.topLogo:
                en.topLogo.updateRoleName(en.topLogo.name)

        self.filter.applySlide = self.inClanWar
        if self.inClanWar and not self.isShowClanWarExcludeSelf():
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.ARMOR_MODE_TEXT, uiUtils.enabledClanWarArmorMode, isModal=False)
        if old and not self.inClanWar:
            gameglobal.rds.ui.littleMap.refreshNpcPos()
        if not old and self.inClanWar:
            gameglobal.rds.tutorial.onInClanWar()
            gameglobal.rds.ui.crossClanWarInfo.show()

    def set_lastClanWarEndTime(self, old):
        gameglobal.rds.ui.topBar.refreshFbStart()

    def set_clanWarStatus(self, old):
        gameglobal.rds.ui.fangkadian.setArmorBtnVisible(True)
        gameglobal.rds.ui.topBar.refreshFbStart()
        Sound.setMusicParam('WAR', self.clanWarStatus)
        if not self.clanWarStatus and old:
            gameglobal.rds.ui.clanWar.clanWarEnd()
            for guildNUID in self.declareWarGuild:
                for en in BigWorld.entities.values():
                    if getattr(en, 'topLogo', None) and (en.IsAvatar and en.guildNUID == guildNUID or getattr(en, 'guildNUID', 0) == guildNUID):
                        en.topLogo.updateRoleName(en.topLogo.name)

            self.declareWarGuild.clear()
            gameglobal.rds.ui.crossClanWarInfo.hide()

    def set_seqLoginDays(self, old):
        gamelog.debug('@hjx refreshDetail:', self.seqLoginDays)
        if hasattr(gameglobal.rds, 'tutorial'):
            spAwdId = -1
            for key, value in SAD.data.items():
                if value.get('type', 1) == gametypes.SPECIAL_AWARD_SEQLOGIN and value.get('value', -1) == self.seqLoginDays:
                    spAwdId = key
                    break

            if spAwdId != -1:
                actId = commActivity.getActivityIdByRef(spAwdId, gametypes.ACTIVITY_REF_BONUS)
                if actId:
                    gameglobal.rds.tutorial.onFinishActivity(actId)

    def set_enterTimeOfDay(self, old):
        gamelog.debug('@hjx act#set_enterTimeOfDay:')
        if gameglobal.rds.ui.roleInfo.titleNewTime == 0:
            gameglobal.rds.ui.roleInfo.titleNewTime = self.enterTimeOfDay
        self.checkOnlineTime()

    def set_enterTimeOfDayNoPersist(self, old):
        self._checkOpenServerBonus()

    def set_mapMarkers(self, old):
        gameglobal.rds.ui.map.updateMarks()

    def _canPay(self, total):
        return total <= self.cash + self.bindCash

    def _canPayCash(self, total):
        return total <= self.cash

    def enoughFame(self, need):
        for fId, val in need:
            if not self.fame.has_key(fId):
                fameVal = utils.getFameInitVal(fId, self.school)
                if fameVal < val:
                    return False
            elif self.fame[fId] < val:
                return False

        return True

    def set_labour(self, old):
        if self.labour != old:
            gameglobal.rds.ui.topBar.setValueByName('workPoint')
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_LABOUR)

    def set_mLabour(self, old):
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_LABOUR)

    def set_mental(self, old):
        if self.mental != old:
            gameglobal.rds.ui.topBar.setValueByName('brainPoint')
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_MENTAL)

    def set_mMental(self, old):
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_MENTAL)

    def set_inDying(self, old):
        super(self.__class__, self).set_inDying(old)
        self.ap.apEffectEx.set_inDying(old)

    def set_currTitle(self, old):
        super(self.__class__, self).set_currTitle(old)
        self.topLogo.hideAvatarTitle(gameglobal.gHidePlayerTitle)
        gameglobal.rds.ui.roleInfo.updateTitle()
        BigWorld.callback(0.2, gameglobal.rds.ui.roleInfo.refreshInfo)

    def set_activeTitleType(self, old):
        super(self.__class__, self).set_activeTitleType(old)
        self.topLogo.hideAvatarTitle(gameglobal.gHidePlayerTitle)
        gameglobal.rds.ui.roleInfo.updateTitle()
        BigWorld.callback(0.2, gameglobal.rds.ui.roleInfo.refreshInfo)

    def setExp(self, value, old, srcId):
        upExp = ALD.data.get(self.lv, {}).get('upExp', sys.maxint)
        pushLvUp = old < upExp and value >= upExp
        self.exp = value
        gameglobal.rds.ui.expbar.setExp(self.exp)
        gameglobal.rds.ui.roleInfo.addManualLvUpPush(self.lv, pushLvUp)
        gameglobal.rds.ui.roleInfo.refreshInfo()
        if self.exp > old:
            if gameglobal.rds.ui.chickenFoodEating.isActive:
                pass
            else:
                gameglobal.rds.ui.showRewardLabel(self.exp - old, const.REWARD_LABEL_EXP)
        gameglobal.rds.ui.roleInfo.refreshLvUpBtn(pushLvUp)
        uiUtils.onFullExpTrigger(self)
        gameglobal.rds.ui.excitementIcon.refreshInfo()

    def showSpecialQuestsExp(self, targetId, incExp, times, exp):
        self.exp = exp
        gameglobal.rds.ui.expbar.setExp(self.exp)
        gameglobal.rds.ui.roleInfo.refreshInfo()
        sfx.showSpecialQuestsExp(targetId, incExp, times)

    def setCash(self, value, old, srcId):
        self.cash = value
        gameglobal.rds.ui.shop.refreshMoney()
        gameglobal.rds.ui.inventory.updataMoney()
        gameglobal.rds.ui.fuben.refreshFubenReward()
        gameglobal.rds.ui.topBar.setValueByName('cash')
        gameglobal.rds.ui.consign.updateCash()
        gameglobal.rds.ui.tianyuMall.onSendMoneyCallback()
        if gameglobal.rds.ui.assign.auctionMediator:
            gameglobal.rds.ui.assign.setAuctionEnabled()
        if self.cash > old:
            gameglobal.rds.ui.showRewardLabel(self.cash - old, const.REWARD_LABEL_CASH)
        gameglobal.rds.ui.resourceMarket.refreshPanel()
        gameglobal.rds.ui.skill.refreshDetailInfo()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CASH_CHANGED)

    def setBindCash(self, value, old, srcId):
        self.bindCash = value
        gameglobal.rds.ui.shop.refreshMoney()
        gameglobal.rds.ui.inventory.updataMoney()
        gameglobal.rds.ui.fuben.refreshFubenReward()
        gameglobal.rds.ui.topBar.setValueByName('bindCash')
        gameglobal.rds.ui.skill.refreshDetailInfo()
        if self.bindCash > old:
            gameglobal.rds.ui.showRewardLabel(self.bindCash - old, const.REWARD_LABEL_BINDCASH)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_BIND_CASH_CHANGED)

    def setStorageCash(self, value, old):
        self.storageCash = value
        gameglobal.rds.ui.storage.updateStorageCash(self.storageCash)

    def setBirthTime(self, birthTime):
        self.birthTime = birthTime

    def setOnlineTime(self, onlineTime):
        self.onlineTime = onlineTime

    def setDelayExp(self, value, old, targetId):
        upExp = ALD.data.get(self.lv, {}).get('upExp', sys.maxint)
        pushLvUp = old < upExp and value >= upExp
        self.exp = value
        gameglobal.rds.ui.expbar.setExp(self.exp)
        gameglobal.rds.ui.roleInfo.addManualLvUpPush(self.lv, pushLvUp)
        gameglobal.rds.ui.roleInfo.refreshInfo()
        if self.exp >= old:
            gameglobal.rds.ui.expMap[targetId] = self.exp - old
        uiUtils.onFullExpTrigger(self)

    def setDelayCash(self, value, old, targetId):
        self.cash = value
        gameglobal.rds.ui.shop.refreshMoney()
        gameglobal.rds.ui.inventory.updataMoney()
        gameglobal.rds.ui.fuben.refreshFubenReward()
        gameglobal.rds.ui.topBar.setValueByName('cash')
        gameglobal.rds.ui.consign.updateCash()
        if self.cash >= old:
            gameglobal.rds.ui.cashMap[targetId] = self.cash - old

    def setDelayBindCash(self, value, old, targetId):
        self.bindCash = value
        gameglobal.rds.ui.shop.refreshMoney()
        gameglobal.rds.ui.inventory.updataMoney()
        gameglobal.rds.ui.fuben.refreshFubenReward()
        gameglobal.rds.ui.topBar.setValueByName('bindCash')
        if self.bindCash >= old:
            gameglobal.rds.ui.bindCashMap[targetId] = self.bindCash - old
        gameglobal.rds.ui.roleInfo.refreshLvUpBtn()

    def resSetPropValData(self, propVal):
        pass

    def resSetRadarData(self, radarData):
        gameglobal.rds.ui.showEquipLabel(radarData, True)

    def set_isolateType(self, old):
        if self.isolateType != gametypes.ISOLATE_TYPE_NONE:
            self.hidePlayerNearby(gameglobal.HIDE_ALL_PLAYER)
        elif self.isolateType == gametypes.ISOLATE_TYPE_NONE:
            self.hidePlayerNearby(gameglobal.HIDE_NOBODY)

    def onSendLvUpRewardData(self, rewardData):
        self.lvUpRewardData = rewardData
        self.updateRewardHallInfo(uiConst.REWARD_SHENJI)

    def set_comboCnt(self, old):
        if gameglobal.rds.ui.dying.isOpen:
            gameglobal.rds.ui.continuousHit.endHit(gametypes.COMBO_TYPE_DAMAGE)
            gameglobal.rds.ui.continuousHit.endHit(gametypes.COMBO_TYPE_HEAL)
            return
        if gameglobal.rds.ui.continuousHit.demageHit != self.comboCnt[gametypes.COMBO_TYPE_DAMAGE]:
            gameglobal.rds.ui.continuousHit.demageHit = self.comboCnt[gametypes.COMBO_TYPE_DAMAGE]
            if gameglobal.rds.ui.continuousHit.demageHit == 0:
                gameglobal.rds.ui.continuousHit.endHit(gametypes.COMBO_TYPE_DAMAGE)
            elif gameglobal.rds.ui.continuousHit.demageHit >= 2:
                gameglobal.rds.ui.continuousHit.hit(gametypes.COMBO_TYPE_DAMAGE, gameglobal.rds.ui.continuousHit.demageHit)
        if gameglobal.rds.ui.continuousHit.healHit != self.comboCnt[gametypes.COMBO_TYPE_HEAL]:
            gameglobal.rds.ui.continuousHit.healHit = self.comboCnt[gametypes.COMBO_TYPE_HEAL]
            if gameglobal.rds.ui.continuousHit.healHit == 0:
                gameglobal.rds.ui.continuousHit.endHit(gametypes.COMBO_TYPE_HEAL)
            elif gameglobal.rds.ui.continuousHit.healHit >= 2:
                gameglobal.rds.ui.continuousHit.hit(gametypes.COMBO_TYPE_HEAL, gameglobal.rds.ui.continuousHit.healHit)

    def set_exploreLv(self, old):
        exploreLvDesc = ELD.data.get(self.exploreLv, {}).get('name', '')
        self.showGameMsg(GMDD.data.EXPLORE_LV_UP, (exploreLvDesc, self.exploreLv))
        gameglobal.rds.ui.skill.refreshExploreSkill()

    def set_xiangyaoExp(self, old):
        gameglobal.rds.ui.skill.refreshExploreSkill()

    def set_xunbaoExp(self, old):
        gameglobal.rds.ui.skill.refreshExploreSkill()

    def set_zhuizongExp(self, old):
        gameglobal.rds.ui.skill.refreshExploreSkill()

    def set_maxVp(self, old):
        if gameglobal.rds.ui.roleInfo.mediator:
            gameglobal.rds.ui.roleInfo.refreshInfo()
        gameglobal.rds.ui.expbar.setLevel(self.realLv)
        gameglobal.rds.ui.player.setMaxVp(self.maxVp)
        vpStage = self.getVpStage()
        gameglobal.rds.ui.player.setVpStage(vpStage)
        gameglobal.rds.ui.expbar.refreshXiuYingBar()

    def set_baseVp(self, old):
        if gameglobal.rds.ui.roleInfo.mediator:
            gameglobal.rds.ui.roleInfo.refreshInfo()
        gameglobal.rds.ui.expbar.setLevel(self.realLv)
        gameglobal.rds.ui.player.setBaseVp(self.baseVp)
        vpStage = self.getVpStage()
        gameglobal.rds.ui.player.setVpStage(vpStage)
        gameglobal.rds.ui.expbar.refreshXiuYingBar()

    def set_savedVp(self, old):
        if gameglobal.rds.ui.roleInfo.mediator:
            gameglobal.rds.ui.roleInfo.refreshInfo()
        gameglobal.rds.ui.expbar.setLevel(self.realLv)
        gameglobal.rds.ui.player.setSavedVp(self.savedVp)
        vpStage = self.getVpStage()
        gameglobal.rds.ui.player.setVpStage(vpStage)
        gameglobal.rds.ui.expbar.refreshXiuYingBar()

    def set_yaoliPoint(self, old):
        gameglobal.rds.ui.player.setYaoliPoint(self.yaoliPoint)

    def set_doubleExpPointInML(self, old):
        gameglobal.rds.ui.player.setDoubleExp(self.doubleExpPointInML)

    def set_jingJie(self, old):
        super(self.__class__, self).set_jingJie(old)
        if gameglobal.rds.ui.roleInfo.mediator:
            gameglobal.rds.ui.roleInfo.refreshJingjieInfo()
            gameglobal.rds.ui.roleInfoJingjie.refreshLeftInfo()
        gameglobal.rds.ui.player.setJingJie(self.jingJie)
        gameglobal.rds.ui.skill.refreshSkillPracticeInfo(gameglobal.rds.ui.skill.skillId)
        gameglobal.rds.ui.skill.refreshSkillEnhanceLv()
        gameglobal.rds.ui.skill.refreshXiuLianPoint()
        gameglobal.rds.tutorial.onBreakJingJie(self.jingJie)
        jingJie = self.jingJie
        if jingJie > old:
            gameglobal.rds.ui.qumoLevelUp.showJingjiePop()
            gameglobal.rds.ui.player.setYaoliMPoint(self.getYaoliMPoint())
            gameglobal.rds.ui.player.setDoubleMExp(self.getYaoliMPoint())

    def getVpStage(self):
        vData = VLD.data.get(self.lv, {})
        if not vData:
            return 0
        stages = vData.get('vpStages')
        stage = 0
        if self.baseVp + self.savedVp:
            for i, stageMaxVal in enumerate(stages):
                if self.baseVp + self.savedVp <= stageMaxVal:
                    stage = i + 1
                    break

        return stage

    def getAllVpStageAndExp(self):
        vData = VLD.data.get(self.lv, {})
        stages = list(vData.get('vpStages', []))
        stages = [0] + stages
        ret = {}
        for i in xrange(1, len(stages)):
            if stages[i - 1] + 1 >= stages[i]:
                break
            ret[i] = ((stages[i - 1] + 1, stages[i]), VSD.data.get(i, {}).get('expParam', 0))

        ret[0] = (0, VSD.data.get(0, {}).get('expParam', 0))
        return ret

    def getVpLvData(self):
        stage = self.getVpStage()
        data = VSD.data.get(stage, {})
        expParam = data.get('expParam', 1)
        transformRatio = data.get('transformRatio', 0)
        return (expParam, transformRatio)

    def _checkVpTransformToExp(self, vData, vp):
        return int(vp)

    def getAvailableVp(self, vp):
        vData = VLD.data.get(self.lv, {})
        if not vData:
            return 0
        if not utils.isSameDay(self.lastTransformVpTime):
            self.transformedVp = 0
        transformLimit = vData.get('transformLimit', 0)
        if transformLimit == 0:
            return 0
        vp = min(transformLimit - self.transformedVp, vp)
        return vp

    def getVpTransformToExp(self, vp):
        vData = VLD.data.get(self.lv, {})
        if not vData:
            return 0
        vp = self.getAvailableVp(vp)
        if vp <= 0:
            return 0
        transformRatio = vData.get('transformRatio', 0)
        if transformRatio == 0:
            return 0
        return int(vp * transformRatio)

    def set_battleFieldScore(self, old):
        gameglobal.rds.ui.battleField.refreshBattleFieldScore()
        gameglobal.rds.ui.battleField.refreshShopList()

    def set_zhanYi(self, old):
        gameglobal.rds.ui.actionbar.setSchoolCenter()

    def set_zhanYiLv(self, old):
        gameglobal.rds.ui.actionbar.setSchoolCenter()

    def set_fortStateId(self, old):
        addData = []
        delData = []
        if self.fortStateId != old and self.fortStateId != 0:
            path = str(SD.data.get(self.fortStateId, {}).get('iconId', 'notFound')) + '.dds'
            iconType = SD.data.get(self.fortStateId, {}).get('iconShowType', 3)
            addData = [{'id': self.fortStateId,
              'srcId': 0,
              'type': iconType,
              'iconPath': path,
              'timer': -100,
              'count': 1}]
        if self.fortStateId != old and old != 0:
            path = str(SD.data.get(old, {}).get('iconId', 'notFound')) + '.dds'
            iconType = SD.data.get(old, {}).get('iconShowType', 3)
            delData = [{'id': old,
              'srcId': 0,
              'type': iconType,
              'iconPath': path,
              'timer': -100,
              'count': 0}]
        gameglobal.rds.ui.player.changeStateIcon(addData, delData)

    def getApplyTimeKey(self, applyType, eId):
        return str(applyType) + '_' + str(eId)

    def setApplyTime(self, applyType, eId):
        key = self.getApplyTimeKey(applyType, eId)
        self.applyTimeDict[key] = time.time()

    def checkApplyTime(self, applyType, eId):
        key = self.getApplyTimeKey(applyType, eId)
        lastTime = self.applyTimeDict.get(key, 0)
        if time.time() - lastTime < SCD.data.get('applyLimitTime', 30):
            return False
        return True

    def checkMentorOrApprentice(self, target):
        targetGbId = getattr(target, 'gbId')
        if self.enableNewApprentice():
            if targetGbId in self.apprenticeInfo.keys():
                return True
            if hasattr(self, 'apprenticeGbIds'):
                apprenticeGbIds = [ i[0] for i in self.apprenticeGbIds ]
                if targetGbId in apprenticeGbIds:
                    return True
        elif gameglobal.rds.ui.mentor.enableApprentice():
            if hasattr(self, 'mentorGbId') and self.mentorGbId == targetGbId:
                return True
            if hasattr(self, 'apprenticeGbIds') and targetGbId in self.apprenticeGbIds:
                return True
        return False

    def applyOtherCheck(self, emoteId, target):
        data = CEBD.data.get(emoteId, {})
        needMentor = data.get('needMentor', None)
        if needMentor:
            if not self.checkMentorOrApprentice(target):
                self.showGameMsg(GMDD.data.APPLY_COUPLE_EMOTE_NOT_MENTOR_OR_APPRENTICE, ())
                return False
        return True

    def applyForCoupleEmote(self, emoteId):
        if not self.coupleEmote:
            if not self.targetLocked:
                self.showGameMsg(GMDD.data.NO_COUPLE_EMOTE_TARGET, ())
                return False
            tid = self.targetLocked.id
            if not self.stateMachine.checkCoupleEmote(emoteId, tid):
                return
            if not self.applyOtherCheck(emoteId, self.targetLocked):
                return
            applyType = gameglobal.APPLY_LIMIT_TYPE_COUPLE_EMOTE
            if not self.checkApplyTime(applyType, tid):
                self.showGameMsg(GMDD.data.APPLY_TIME_LIMIT_COUPLE_EMOTE, ())
                return
            self.setApplyTime(applyType, tid)
            self.cell.applyForCoupleEmote(emoteId, self.targetLocked.id, self.targetLocked.gbId)
        else:
            self.cell.cancelCoupleEmote()

    def inviteRideTogether(self, targetId):
        applyType = gameglobal.APPLY_LIMIT_TYPE_TRIDE_INVITE
        if not self.checkApplyTime(applyType, targetId):
            self.showGameMsg(GMDD.data.APPLY_TIME_LIMIT_TRIDE_INVITE, ())
            return
        if not self.stateMachine.checkRideTogetherMajor(targetId):
            return
        self.setApplyTime(applyType, targetId)
        self.cell.inviteRideTogether(targetId)

    def applyForRideTogether(self, targetId):
        applyType = gameglobal.APPLY_LIMIT_TYPE_TRIDE_APPLY
        if not self.checkApplyTime(applyType, targetId):
            self.showGameMsg(GMDD.data.APPLY_TIME_LIMIT_TRIDE_APPLY, ())
            return
        if not self.stateMachine.checkRideTogetherMinor(targetId):
            return
        self.setApplyTime(applyType, targetId)
        self.cell.applyRideTogether(targetId)

    def cancelRideTogether(self):
        if self.tride.inRide():
            self.cell.cancelRideTogether()

    def removeRideTogether(self, targetId):
        if self.tride.inRide():
            self.cell.removeRideTogether(targetId)

    def _checkRideTogetherEntValid(self, key):
        ent = BigWorld.entities.get(key)
        if not ent:
            return False
        if not ent.inWorld:
            return False
        if ent.clientLoadingState:
            return False
        if self.clientLoadingState:
            return False
        dist = (self.position - ent.position).length
        if dist > 20:
            return False
        if self.tride.isMajor(self.id) and ent.isWaitingRideTogether:
            return False
        return True

    def set_isWaitingRideTogether(self, old):
        if self.tride.inRide() and not self.tride.isMajor(self.id):
            if old == 0:
                self.physics.followTarget = None
            else:
                header = self.tride.getHeader()
                if header:
                    self.physics.followTarget = header.matrix

    def _checkWaitForRideTogetherLoading(self):
        if self.tride.inRide():
            if self.tride.isMajor(self.id):
                for key in self.tride.iterkeys():
                    if not self._checkRideTogetherEntValid(key):
                        BigWorld.callback(0.5, self._checkWaitForRideTogetherLoading)
                        return

            elif not self._checkRideTogetherEntValid(self.tride.header):
                BigWorld.callback(0.5, self._checkWaitForRideTogetherLoading)
                return
        self._cancelWaitForRideTogetherLoading()

    def _cancelWaitForRideTogetherLoading(self, bManually = False):
        if not self.isWaitingRideTogether:
            return
        self.cell.enableCycleRideTogetherCheck(bManually)

    def serverCancelWaitForRideTogetherLoading(self):
        self.allTogetherRiderReady = True
        if hasattr(self, 'waitBoxId') and self.waitBoxId:
            gameglobal.rds.ui.messageBox.dismiss(msgBoxId=self.waitBoxId)
            self.waitBoxId = 0

    def continueRideTogetherNavigate(self):
        if self.tride.inRide():
            return getattr(self, 'allTogetherRiderReady', False)
        else:
            return True

    def _showWaitingMessageBoxOfRideTogether(self):
        self.waitBoxId = gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_IMPPLAYERPROPERTY_2266, callback=lambda : self._cancelWaitForRideTogetherLoading(True), yesBtnText=gameStrings.TEXT_IMPPLAYERPROPERTY_2268)

    def startProgressLoading(self):
        self.cell.setClientLoadingState(True)

    def endProgressLoading(self):
        self.cell.setClientLoadingState(False)

    def waitForRideTogetherLoading(self):
        if self.tride.inRide():
            self._showWaitingMessageBoxOfRideTogether()
            self.allTogetherRiderReady = False
            BigWorld.callback(0.5, self._checkWaitForRideTogetherLoading)

    def set_statesServerAndOwn(self, old):
        if len(old) > 0:
            gameglobal.rds.ui.buffNotice.oldState = old
        self.flagStates = filter(lambda state: state[2] == -1 or state[2] + state[3] > self.getServerTime(), self.flagStates)
        super(self.__class__, self).set_statesServerAndOwn(old)
        gameglobal.rds.ui.roleInfo.refreshInfo()
        gameglobal.rds.ui.actionbar.showToggleShine(old)
        gameglobal.rds.ui.actionbar.setSchoolCenter()
        gameglobal.rds.ui.castbar.startBuffCountDown(old)
        self.stateAttrCache = None
        self.clientEffectIcon()
        if gameglobal.rds.ui.wenQuanDetail.shouldUpdate():
            gameglobal.rds.ui.wenQuanDetail.updateState(old)
        for key in self.statesServerAndOwn.iterkeys():
            if not old.has_key(key):
                gameglobal.rds.tutorial.onGetState(key)

    def addConditionalPropStateIcon(self):
        oldState = dict(self.statesServerAndOwn)
        self.set_statesServerAndOwn(oldState)

    def delConditionalStateIcon(self):
        conditionalFakeIconIds = SCD.data.get('conditionalFakeIconIds', ())
        oldState = dict(self.statesServerAndOwn)
        bChange = False
        for iconId in conditionalFakeIconIds:
            if iconId in self.statesServerAndOwn:
                del self.statesServerAndOwn[iconId]
                bChange = True

        if bChange:
            self.set_statesServerAndOwn(oldState)

    def set_kuilingOrg(self, old):
        if old == 0 and self.kuilingOrg > 0:
            gameglobal.rds.ui.lifeSkill.lifeSkillFactory.createKuiLingIns(self.kuilingOrg)
            gameglobal.rds.ui.lifeSkill.setCurLifeSkill(uiConst.PANEL_TYPE_KUI_LING)
        gameglobal.rds.ui.lifeSkillNew.refreshPanel()

    def set_kuilingQuests(self, old):
        gameglobal.rds.ui.lifeSkillNew.refreshPanel()

    def set_mapAreaId(self, old):
        gameglobal.rds.ui.team.refreshTeamDetails()

    def set_clientDBID(self, old):
        BigWorld.setWindowTitle(2, '@%d' % (self.clientDBID,))

    def set_groupAssignWay(self, old):
        gameglobal.rds.ui.teamComm.setAssignInfo()
        gameglobal.rds.ui.assign.refreshDicePanel()

    def set_groupAssignQuality(self, old):
        gameglobal.rds.ui.teamComm.setAssignInfo()

    def set_skillEnhancePoint(self, old):
        gameglobal.rds.ui.skill.refreshSkillPracticeInfo(gameglobal.rds.ui.skill.skillId)
        gameglobal.rds.ui.skill.refreshSkillEnhanceLv()
        gameglobal.rds.ui.skill.refreshXiuLianPoint()
        self.updateRewardHallInfo(uiConst.REWARD_XIULIAN)

    def set_totalLearnSkillEnhanceScore(self, old):
        gameglobal.rds.ui.skill.refreshXiuLianScore()

    def set_abilityData(self, old):
        super(self.__class__, self).set_abilityData(old)
        k = utils.getAbilityKey(gametypes.ABILITY_YAOLI_MAX_ADD, 0)
        if not old.has_key(k):
            oldMaxYaoli = 0
        else:
            oldMaxYaoli = old[k]
        if oldMaxYaoli != self.getAbilityData(gametypes.ABILITY_YAOLI_MAX_ADD):
            gameglobal.rds.ui.player.setYaoliMPoint(self.getYaoliMPoint())
            gameglobal.rds.ui.player.setDoubleMExp(self.getYaoliMPoint())
        if self.isAbilityUpdated(old, gametypes.ABILITY_LS_COLLECTION_SUB_ON):
            self.refreshLifeCsmItemTopLogo()
        gameglobal.rds.ui.lifeSkillNew.refreshPanel()

    def set_pkPunishTime(self, old):
        self.topLogo.updatePkTopLogo()
        gameglobal.rds.ui.topBar.setValueByName('killPoint')
        gameglobal.rds.ui.player.updatePKState(self.pkMode)

    def refreshLifeCsmItemTopLogo(self):
        ents = BigWorld.entities.values()
        if ents:
            for e in ents:
                if e.__class__.__name__ == 'LifeCsmItem':
                    e.resetTopLogo()
                    if e.topLogo:
                        e.topLogo.updateRoleName(e.getColorName())
                    if e == self.targetLocked:
                        if e.showTargetUnitFrame():
                            gameglobal.rds.ui.target.showTargetUnitFrame()

    def isAbilityUpdated(self, old, abilityType):
        newAbilitys = set(self.abilityData.keys()) - set(old.keys())
        if newAbilitys:
            for key in newAbilitys:
                ability = utils.getAbilityTypeFromKey(key)
                if ability == abilityType:
                    return True

        return False

    def set_carnivalBonusInfo(self, old):
        if not self.carnivalBonusInfo:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GET_CARNIVAL_REWARD)
        if self.carnivalBonusInfo and old != self.carnivalBonusInfo:
            activityId, itemBonus, pushId = self.carnivalBonusInfo
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GET_CARNIVAL_REWARD)
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_CARNIVAL_REWARD, {'data': itemBonus})

    def set_avatarOwnClientFlags(self, old):
        val = old ^ self.avatarOwnClientFlags
        index = int(math.log(val, 2))
        gamelog.debug('@lhb set_avatarOwnClientFlags index ', index)
        if index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_USING_LIFE_SKILL:
            if hasattr(self, 'set_usingLifeSkill'):
                self.set_usingLifeSkill(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_REPAIRING_LIFE_EQUIPMENT:
            if hasattr(self, 'set_repairingLifeEquipment'):
                self.set_repairingLifeEquipment(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_HAS_INV_PASSWORD:
            if hasattr(self, 'set_hasInvPassword'):
                self.set_hasInvPassword(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_HAS_PHONE_BINDING:
            if hasattr(self, 'set_hasPhoneBinding'):
                self.set_hasPhoneBinding(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_IS_QUEST_ZAIJU:
            if hasattr(self, 'set_isQuestZaiju'):
                self.set_isQuestZaiju(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_HAS_INTIMACY_TGT:
            if hasattr(self, 'set_hasIntimacyTgt'):
                self.set_hasIntimacyTgt(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_IS_FB_GUIDE_MODE:
            if hasattr(self, 'set_isFbGuideMode'):
                self.set_isFbGuideMode(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_CLAN_WAR_STATUS:
            if hasattr(self, 'set_clanWarStatus'):
                self.set_clanWarStatus(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_WORLD_AREA_VALID:
            if hasattr(self, 'set_worldAreaValid'):
                self.set_worldAreaValid(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_CAN_RELIVE_BY_GUILD:
            if hasattr(self, 'set_canReliveByGuild'):
                self.set_canReliveByGuild(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_GUILD_BUSINESS:
            if hasattr(self, 'set_guildBusiness'):
                self.set_guildBusiness(commcalc.getBitDword(old, index))
        elif index == gameCommonBitset.AVT_OWN_CLIENT_FLAG_DWORD_IS_FB_ASSITER:
            if hasattr(self, 'set_isFbAssister'):
                self.set_isFbAssister(commcalc.getBitDword(old, index))

    def getInteractiveObjTId(self):
        if self.interactiveObjectEntId:
            obj = BigWorld.entities.get(self.interactiveObjectEntId)
            if obj and obj.inWorld:
                return obj.objectId

    def set_interactiveObjectEntId(self, old):
        super(self.__class__, self).set_interactiveObjectEntId(old)
        if self.interactiveObjectEntId:
            gameglobal.rds.ui.interactiveActionBar.show()
            interOjb = self.getInteractiveObj()
            if interOjb and interOjb.inWorld and interOjb.getType():
                if ITD.data.has_key(interOjb.getType()) and not ITD.data.get(interOjb.getType(), {}).get('hideUI', False):
                    rewardTotalTime = interOjb.getItemData().get('rewardTotalTime', 120)
                    gameglobal.rds.ui.interactiveObj.showRewardWidget(rewardTotalTime)
            obj = BigWorld.entities.get(self.interactiveObjectEntId)
            if obj and obj.inWorld:
                if obj.ownerGbId == self.gbId:
                    gameglobal.rds.ui.interactiveObj.showKickWidget()
                gameglobal.rds.ui.interactiveObjMounts.show()
            if gameglobal.rds.ui.pressKeyF.isInteractive == True:
                self.inInteractiveObjTemp = gameglobal.rds.ui.pressKeyF.interactiveObj
                gameglobal.rds.ui.pressKeyF.isInteractive = False
                gameglobal.rds.ui.pressKeyF.interactiveObj = None
                gameglobal.rds.ui.pressKeyF.removeType(const.F_INTERACTIVE)
        else:
            gameglobal.rds.ui.interactiveActionBar.hide()
            gameglobal.rds.ui.interactiveObj.closeRewardWidget()
            gameglobal.rds.ui.interactiveObj.closeKickWidget()
            gameglobal.rds.ui.interactiveObjMounts.hide()
            if getattr(self, 'inInteractiveObjTemp', None) and self.inInteractiveObjTemp.inWorld:
                self.interactiveTrapCallback((self.inInteractiveObjTemp,))
            self.inInteractiveObjTemp = None
            if gameglobal.rds.ui.miniGame.widget:
                gameglobal.rds.ui.miniGame.hide()
        gameglobal.rds.cam.reset()

    def getYaoliMPoint(self):
        return SCD.data.get('maxYaoLi', 20000) + self.getAbilityData(gametypes.ABILITY_YAOLI_MAX_ADD) + utils.getAddYaoliPointByJingjie(self)

    def getFameLv(self, fameId):
        fd = FD.data.get(fameId)
        if not fd:
            return 0
        if self.fame.has_key(fameId):
            fv = self.fame[fameId]
        else:
            fv = FD.data[fameId].get('initVal', 0)
        lvUpNeed = fd.get('lvUpNeed')
        if not lvUpNeed:
            return 0
        maxLv = len(lvUpNeed)
        lv = 1
        for i in range(1, maxLv + 1):
            v = lvUpNeed.get(i)
            if fv >= v:
                lv = i + 1

        return min(lv, maxLv)

    def onCipherModified(self, cipher):
        self.cipherOfPerson = cipher
        gameglobal.rds.cipherOfPerson = self.cipherOfPerson
        gameglobal.rds.ui.userAccountBind.refreshPasswordPanel()
        gameglobal.rds.ui.accountBind.refreshPassword()
        gameglobal.rds.ui.accountBind.refreshLevel()

    def onCipherValidate(self, r, cipher):
        if r:
            self.cipherOfPerson = cipher
            if hasattr(self, 'onGetCipherCallback') and self.onGetCipherCallback:
                self.onGetCipherCallback(cipher, *self.onGetCipherCallbackArgs)
                self.onGetCipherCallback = None
                self.onGetCipherCallbackArgs = None
        else:
            self.cipherOfPerson = ''
            _cancelCallback = getattr(self, 'onGetCipherCancelCallback', None)
            if _cancelCallback:
                _cancelCallback()
        self.onGetCipherCancelCallback = None
        gameglobal.rds.cipherOfPerson = self.cipherOfPerson

    def getCipher(self, callbackMethod, callbackArgs = (), cancelCallback = None):
        if self.hasInvPassword and not self.cipherOfPerson:
            self.onGetCipherCallback = callbackMethod
            self.onGetCipherCallbackArgs = callbackArgs
            self.onGetCipherCancelCallback = cancelCallback
            gameglobal.rds.ui.inventoryPassword.show(0, 0, 0, isUsedForCipher=True, cancelCallback=cancelCallback)
        else:
            callbackMethod(self.cipherOfPerson, *callbackArgs)

    def getEffectLv(self):
        return getattr(self, 'selfEffectLv', gameglobal.EFFECT_MID)

    def getSkillEffectLv(self):
        effectLv = self.getEffectLv()
        return EFLD.data.get('player', {}).get('content', {}).get(effectLv)[0]

    def getBeHitEffectLv(self):
        effectLv = self.getEffectLv()
        return EFLD.data.get('player', {}).get('content', {}).get(effectLv)[1]

    def getBuffEffectLv(self):
        effectLv = self.getEffectLv()
        return EFLD.data.get('player', {}).get('content', {}).get(effectLv)[2]

    def getEquipEffectLv(self):
        effectLv = self.getEffectLv()
        return EFLD.data.get('player', {}).get('content', {}).get(effectLv)[3]

    def getBasicEffectLv(self):
        effectLv = self.getEffectLv()
        return EFLD.data.get('player', {}).get('content', {}).get(effectLv)[4]

    def getSkillEffectPriority(self):
        return gameglobal.EFF_PLAYER_SKILL_PRIORITY

    def getBeHitEffectPriority(self, host):
        return gameglobal.EFF_PLAYER_BEHIT_PRIORITY

    def getBuffEffectPriority(self, host):
        return gameglobal.EFF_PLAYER_BUFF_PRIORITY

    def getEquipEffectPriority(self):
        return gameglobal.EFF_PLAYER_EQUIP_PRIORITY

    def getBasicEffectPriority(self):
        return gameglobal.EFF_PLAYER_BASIC_PRIORITY

    def getVpVip(self, tag):
        if tag != 0 and tag != 3:
            return 0
        package = []
        for key in self.vipAddedPackage:
            package.append(BigWorld.player().vipAddedPackage[key].get('services', []))

        package.append(BigWorld.player().vipBasicPackage.get('services', []))
        vData = VLD.data.get(BigWorld.player().lv, {})
        value = 0
        nowValue = []
        for items in package:
            for service in items:
                if service[1] > BigWorld.player().getServerTime():
                    propId = VSDD.data.get(service[0], {}).get('propID', 0)
                    isInvalid = VSDD.data.get(service[0], {}).get('invalid', 0)
                    if isInvalid == 0:
                        if tag == 0 and propId == gametypes.VIP_SERVICE_WUXING_REGEN:
                            nowValue.append(self.vipRevise(propId, vData['dailyVp'], True))
                            continue
                        if tag == 3 and propId == gametypes.VIP_SERVICE_WUXING_STORE:
                            nowValue.append(self.vipRevise(propId, 0, True))
                            continue

        if nowValue:
            if tag == 0:
                value = max(nowValue) - vData['dailyVp']
            elif tag == 3:
                value = max(nowValue)
        return value

    def set_vpStorage(self, old):
        gameglobal.rds.ui.roleInfo.refreshVpKey()
        gameglobal.rds.ui.expbar.refreshXiuYingBar()

    def set_vpAdd(self, old):
        gameglobal.rds.ui.expbar.refreshXiuYingBar()

    def set_vpStorageExpireTime(self, old):
        gameglobal.rds.ui.roleInfo.refreshVpKey()
        gameglobal.rds.ui.expbar.refreshXiuYingBar()

    def set_skillAdd(self, old):
        gameglobal.rds.ui.actionbar.checkSkillStatOnPropModified()

    def justShowCipher(self):
        if gameglobal.rds.configData.get('enableInventoryLock', False):
            if self.hasInvPassword and not self.cipherOfPerson:
                gameglobal.rds.ui.inventoryPassword.show(0, 0, 0, isUsedForCipher=True)

    def setAccountTotalCoin(self, val):
        self.accountTotalCoin = val

    def set_hasPhoneBinding(self, old):
        gameglobal.rds.ui.userAccountBind.updatePhoneBindInfo()
        gameglobal.rds.ui.accountBind.refreshPhoneBind()
        gameglobal.rds.ui.userAccountBind.refreshAccountLevel()
        gameglobal.rds.ui.accountBind.refreshLevel()
        self.updateRewardHallInfo(uiConst.REWARD_ANQUAN)

    def set_hasPhoneRewardReceived(self, old):
        gameglobal.rds.ui.userAccountBind.updatePhoneBindInfo()
        gameglobal.rds.ui.accountBind.refreshPhoneBind()
        self.updateRewardHallInfo(uiConst.REWARD_ANQUAN)

    def set_bindPhoneNum(self, old):
        gameglobal.rds.ui.userAccountBind.updatePhoneBindInfo()
        gameglobal.rds.ui.accountBind.refreshPhoneBind()
        gameglobal.rds.ui.accountBind.refreshLevel()
        self.updateRewardHallInfo(uiConst.REWARD_ANQUAN)

    def set_hasEkeyRewardReceived(self, old):
        gameglobal.rds.ui.userAccountBind.updateEKeyBindInfo()
        gameglobal.rds.ui.accountBind.refreshEKeyBind()
        self.updateRewardHallInfo(uiConst.REWARD_ANQUAN)

    def set_securityTypeOfCell(self, old):
        gameglobal.rds.ui.userAccountBind.updateEKeyBindInfo()
        gameglobal.rds.ui.accountBind.refreshEKeyBind()
        gameglobal.rds.ui.userAccountBind.refreshAccountLevel()

    def set_hasInvPassword(self, old):
        gamelog.debug('@lhb set_hasInvPassword old', old)
        self.updateRewardHallInfo(uiConst.REWARD_ANQUAN)
        gameglobal.rds.ui.accountBind.refreshLevel()
        gameglobal.rds.ui.accountBind.refreshPassword()

    def set_hasCipherRewardReceived(self, old):
        self.updateRewardHallInfo(uiConst.REWARD_ANQUAN)

    def set_gmFollow(self, old):
        self.refreshFollowAvatarClient()
        gameglobal.rds.ui.topBar.switchTopBar(True)
        gameglobal.rds.ui.teamComm.refreshMemberInfo()

    def initDisturb(self, info):
        gamelog.debug('@hjx disturb#initDisturb:', info)
        self.disturb = info

    def addDisturb(self, dType, ratio):
        gamelog.debug('@hjx disturb#addDisturb:', dType, ratio)
        self.disturb[dType] = ratio

    def removeDisturb(self, dType):
        gamelog.debug('@hjx disturb#removeDisturb:', dType)
        self.disturb.pop(dType, None)

    def set_dmgStartTime(self, old):
        gameglobal.rds.ui.fubenStat.show(uiConst.STAT_TYPE_ONLY_DPS)

    def set_dmgTotal(self, old):
        gameglobal.rds.ui.fubenStat.show(uiConst.STAT_TYPE_ONLY_DPS)

    def set_signInCnt(self, old):
        gameglobal.rds.ui.welfareEveryDayReward.refresh()

    @ui.checkInventoryLock()
    def applyUndisturb(self, maxHour, needCoin):
        msg = MSGDD.data.get('applyUndisturbMsg', gameStrings.TEXT_IMPPLAYERPROPERTY_2709)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg % (maxHour, needCoin), Functor(self._doApplyUndisturb), yesBtnText=gameStrings.TEXT_IMPPLAYERPROPERTY_2711, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def _doApplyUndisturb(self):
        self.cell.doApplyUndisturb()

    def set_primaryProp(self, old):
        if not gameglobal.rds.ui.roleInfo.mediator:
            return
        BigWorld.callback(0.5, gameglobal.rds.ui.roleInfo.refreshInfo)

    def set_currentWorkingAchieveScoreActivities(self, old):
        gameglobal.rds.ui.topBar.refreshActivityIcon()

    def set_virussafe(self, old):
        pass

    def getMaxVirussafe(self):
        v = SCD.data.get('maxVirussafeVal', 100)
        return int(round(v))

    def updateFameBonusInfo(self, data):
        if not hasattr(self, 'fameBonusInfo'):
            self.fameBonusInfo = {}
        self.fameBonusInfo.update(data)

    def getLifeEquipEffect(self, key, default = 0):
        return self.lifeEquipEffects.get(key, default)

    def set_summonedPets(self, old):
        if self.summonedPets:
            pet = self._getPet()
            if pet and pet.inWorld:
                gameglobal.rds.ui.beastActionBar.show()
        else:
            gameglobal.rds.ui.beastActionBar.hide()

    def useItemOfPreDefinedLaba(self, page, pos, labaId, useType):
        gameglobal.rds.ui.labaConfirm.show(labaId, useType, page, pos)

    def setPlayRecommendFinishedActivities(self, playRecommendedFinishedActivities):
        gameglobal.rds.ui.playRecommActivation.setPlayRecommendedFinishedActivities(playRecommendedFinishedActivities)

    def setSecondEscPlayScenario(self, secondEscPlayScenarioFlag):
        self.secondEscPlayScenarioFlag = secondEscPlayScenarioFlag

    def getTianBi(self):
        return self.unbindCoin + self.bindCoin + self.freeCoin

    def onResetDaily(self):
        self.dailyStats.clear()
        self._resetPrivateShopDaily()

    def sendDailyStats(self, data):
        self.dailyStats.update(data)
        gameglobal.rds.ui.wenQuanDetail.updateValue()

    def getBreakStartLv(self):
        manualBreakEvents = SCD.data.get('manualLevelBreakthroughEvents', {})
        if not manualBreakEvents or not manualBreakEvents.has_key('levelRange'):
            return 59
        for minLv, maxLv in manualBreakEvents['levelRange']:
            if minLv >= self.lv:
                return minLv

        return 59

    def getBreakEndLv(self):
        manualBreakEvents = SCD.data.get('manualLevelBreakthroughEvents', {})
        if not manualBreakEvents or not manualBreakEvents.has_key('levelRange'):
            return 69
        for minLv, maxLv in manualBreakEvents['levelRange']:
            if minLv >= self.lv:
                return maxLv

        return 69

    def breakLvUp(self):
        self.cell.manualLvBreakthrough()

    def inPreBreakLvDuration(self):
        if not gameglobal.rds.configData.get('enableLevelBreakthrough', False):
            return False
        breakStartLv = self.getBreakStartLv()
        return breakStartLv - 5 < self.lv < breakStartLv

    def isInLvBreak(self):
        if not gameglobal.rds.configData.get('enableLevelBreakthrough', False):
            return False
        breakStartLv = self.getBreakStartLv()
        if self.lv == breakStartLv:
            ald = ALD.data.get(breakStartLv, {})
            if getattr(self, 'exp', 0) >= ald.get('upExp', 0):
                return True
        return False

    def canLvBreak(self):
        if self.isInLvBreak():
            return self.getLvBreakUp() + self.getBreakStartLv() >= self.getBreakEndLv()
        return False

    def getLvBreakUp(self):
        if self.isInLvBreak():
            breakStartLv = self.getBreakStartLv()
            breakEndLv = self.getBreakEndLv()
            totalExp = 0
            for i, lv in enumerate(xrange(breakStartLv, breakEndLv)):
                ald = ALD.data.get(lv, {})
                upExp = ald.get('upExp', 0)
                totalExp += upExp
                if getattr(self, 'exp', 0) < totalExp:
                    step = i + (self.exp - (totalExp - upExp)) * 1.0 / upExp
                    return step
            else:
                return i + 1

        return 0

    def getLvBreakStep(self):
        lv = self.getLvBreakUp()
        if lv:
            return (lv - 1) * 1.0 / (self.getBreakEndLv() - self.getBreakStartLv() - 1)
        return 0

    def sendEquipSoulInfo(self, data):
        gameglobal.rds.ui.equipSoul.setActiveEffect(data)
        self.equipSoul.update(data)
        gameglobal.rds.ui.equipSoul.refreshTabInfo()

    def set_itemUseHistory(self, old):
        gameglobal.rds.ui.equipSoulStar.refreshInfo()

    def set_groupHeader(self, old):
        gameglobal.rds.ui.refreshTeamLogoOrIdentity(self.id)
        if self.groupHeader == self.id and self.hasInFollowMember():
            self.cell.startGroupHeaderFollowSync()
        self.syncGroupFollowHeaderPosCheck()
        if self.carrier.carrierState in (gametypes.MULTI_CARRIER_STATE_CHECK_READY, gametypes.MULTI_CARRIER_STATE_RUNNING):
            forbiddenMultiUI = MCDD.data.get(self.carrier.carrierNo, {}).get('forbiddenMultiUI', 0)
            if not forbiddenMultiUI:
                gameglobal.rds.ui.multiCarrier.show(self.carrier.carrierNo)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_GROUP_HEADER)

    def set_carrierSatisfaction(self, old):
        gameglobal.rds.ui.questTrack.refreshFindBeastExpText()

    def set_marriageStage(self, old):
        if self.marriageStage in (gametypes.MARRIAGE_STAGE_PREPARE,
         gametypes.MARRIAGE_STAGE_START,
         gametypes.MARRIAGE_STAGE_ENTER_HALL,
         gametypes.MARRIAGE_STAGE_PARADE,
         gametypes.MARRIAGE_STAGE_ENTER_RES):
            gameglobal.rds.ui.marryProcess.show()
        else:
            gameglobal.rds.ui.marryProcess.hide()
            self.removeMarriageProgressMessage()
        if self.checkMarriageHallMaidMsg():
            self.addMarriagePrompt(uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL)
        elif not self.checkMarriageHallMaidMsg(True):
            self.removeMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_MAID_HALL)
        if self.checkMarriageCarrierMsg():
            self.addMarriagePrompt(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER)
        elif not self.checkMarriageCarrierMsg(True):
            self.removeMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_APPLY_CARRIER)
        if self.checkMarriageRoomMaidMsg():
            self.addMarriagePrompt(uiConst.MESSAGE_TYPE_MARRIAGE_ROOM)
        elif not self.checkMarriageRoomMaidMsg(True):
            self.removeMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_ROOM)
        if not self.marriageStage == gametypes.MARRIAGE_STAGE_ENTER_HALL:
            self.removeMarriageMessage(uiConst.MESSAGE_TYPE_MARRIAGE_PARADE)

    def set_combatScoreList(self, old):
        if self.combatScoreList:
            gameglobal.rds.ui.cardCollection.refreshScore()
            gameglobal.rds.ui.cardSlot.refreshScore()
            gameglobal.rds.ui.summonedWarSpriteXiuLian.updateTotalScore()

    def set_skillClientArgs(self, old):
        gamelog.debug('ypc@ set_skillClientArgs!', old, self.skillClientArgs)

    def set_isFbAssister(self, old):
        gamelog.debug('@xzh set_isFbAssister', old, self.isFbAssister)

    def set_questVars(self, old):
        gameglobal.rds.ui.questTrack._onQuestInfoChanged()

    def set_chatAnonymity(self, old):
        super(self.__class__, self).set_chatAnonymity(old)
        gameglobal.rds.ui.huntGhost.refreshMaskState()
