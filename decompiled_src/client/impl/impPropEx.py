#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPropEx.o
import math
import copy
import BigWorld
import ResMgr
import gamelog
import gameglobal
import utils
import const
import gametypes
import gameCommonBitset
from gamestrings import gameStrings
from guis import events
from guis import uiConst
from helpers.eventDispatcher import Event
from helpers import editorHelper
from helpers.skillAppearancesUtils import SkillAppearancesDetail
from data import sys_config_data as SCD
from data import activity_state_config_data as ASCD
from data import junjie_config_data as JCD
from cdata import game_msg_def_data as GMDD
alias = ResMgr.openSection('entities/defs/alias.xml')
ocli = alias.openSection('OWN_CLIENT_VAL')
acli = alias.openSection('ALL_CLIENTS_VAL')
OCLI_PROPS = ocli.openSection('Properties').keys()
ACLI_PROPS = acli.openSection('Properties').keys()
del acli
del ocli
del alias

class ImpPropEx(object):

    def onSetOwnClientMiscProperty(self, attr, value):
        setFunc = getattr(self, 'set_%s' % attr, None)
        if setFunc:
            if attr in gametypes.MISC_VAR_OCLI_SET_FUNC_ARG_OLD:
                oldValue = self.OCLI[0]['MISC_VAR_OCLI'].get(attr, gametypes.MISC_VAR_OCLI_SET_FUNC_ARG_OLD[attr])
                self.OCLI[0]['MISC_VAR_OCLI'][attr] = value
                setFunc(oldValue)
            else:
                self.OCLI[0]['MISC_VAR_OCLI'][attr] = value
                setFunc()

    def get_onlineTimeWeekly(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_ONLINE_TIME_WEEKLY)

    def set_onlineTimeWeekly(self):
        pass

    onlineTimeWeekly = property(get_onlineTimeWeekly, '', '', '')

    def get_wwArmyImpeachVoted(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_WW_ARMY_IMPEACH_VOTED)

    def set_wwArmyImpeachVoted(self, value):
        self.onSetOwnClientMiscProperty(gametypes.MISC_VAR_OCLI_WW_ARMY_IMPEACH_VOTED, value)

    wwArmyImpeachVoted = property(get_wwArmyImpeachVoted, set_wwArmyImpeachVoted, '', '')

    def get_hieroExchangeTargetNum(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_HIERO_EXCHANGE_TARGET_NUM, 0)

    def set_hieroExchangeTargetNum(self, oldValue = None):
        pass

    hieroExchangeTargetNum = property(get_hieroExchangeTargetNum, set_hieroExchangeTargetNum, '', '')

    def get_hieroExchangeSourceNum(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_HIERO_EXCHANGE_SOURCE_NUM, 0)

    def set_hieroExchangeSourceNum(self, oldValue = None):
        gameglobal.rds.ui.equipChangeRuneToItem.refreshItemCnt()

    hieroExchangeSourceNum = property(get_hieroExchangeSourceNum, set_hieroExchangeSourceNum, '', '')

    def get_guildSignIn(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_GUILD_SIGN_IN)

    def set_guildSignIn(self):
        gameglobal.rds.ui.guildRedPacket.refreshInfo()
        gameglobal.rds.ui.guild.refreshGuildActivityInfo()
        gameglobal.rds.ui.playRecommActivation.refreshDailyRecommItems()

    guildSignIn = property(get_guildSignIn, '', '', '')

    def get_guildBonfire(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_GUILD_BONFIRE)

    def set_guildBonfire(self):
        pass

    def get_groupBuyInfo(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_GUILD_BONFIRE)

    def set_groupBuyInfo(self):
        pass

    guildBonfire = property(get_guildBonfire, '', '', '')

    def get_guildDonateCoinOpCntDaily(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_GUILD_DONATE_COIN_CNT_DAILY, 0)

    def set_guildDonateCoinOpCntDaily(self):
        pass

    guildDonateByCoinCntDaily = property(get_guildDonateCoinOpCntDaily, '', '', '')

    def get_targetFallenRedGuards(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_GUILD_TARGET_FALLEN_RED_GUARD_FLAGS, {})

    def set_targetFallenRedGuards(self):
        pass

    targetFallenRedGuards = property(get_targetFallenRedGuards, '', '', '')

    def get_zhanXunRewardWeekly(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_ZHAN_XUN_REWARD_WEKKLY)

    def set_zhanXunRewardWeekly(self):
        gamelog.debug('@hjx zhanxun#set_zhanXunRewardWeekly:', self.zhanXunRewardWeekly)
        gameglobal.rds.ui.roleInformationJunjie.initWeekReward()

    zhanXunRewardWeekly = property(get_zhanXunRewardWeekly, set_zhanXunRewardWeekly, '', '')

    def get_dailyActivationRewardDict(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_DAILY_ACTIVATION_REWARD_DICT, {})

    def set_dailyActivationRewardDict(self):
        gamelog.debug('@hjx partner#set_dailyActivationRewardDict:', self.dailyActivationRewardDict)
        gameglobal.rds.ui.partnerMain.refreshRewardMc()
        gameglobal.rds.ui.systemButton.showPartnerNotify()

    dailyActivationRewardDict = property(get_dailyActivationRewardDict, set_dailyActivationRewardDict, '', '')

    def get_arenaChallengeNotifyEnterTimestamp(self):
        return self.OCLI[0]['arenaChallengeNotifyEnterTimestamp']

    def set_arenaChallengeNotifyEnterTimestamp(self, old, new, part):
        gamelog.debug('@hjx arenaChallenge#set_arenaChallengeNotifyEnterTimestamp:', old, new)

    arenaChallengeNotifyEnterTimestamp = property(get_arenaChallengeNotifyEnterTimestamp, '', '', '')

    def get_wwscoreLastWeek(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_CPRI_WWSCORE_LAST_WEEK, 0)

    wwscoreLastWeek = property(get_wwscoreLastWeek, '', '', '')

    def get_obSpaceNo(self):
        if not hasattr(self, 'OCLI'):
            return 0
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_OB_SPACENO)

    def set_obSpaceNo(self):
        if self.obSpaceNo == 0:
            if self.isInBfDota() or self.inClanChallengeOb() or self.isInPUBG():
                gameglobal.rds.ui.fightObserve.closeActionBar()
                self.resetCamera()
        elif self.isInBfDota() or self.inClanChallengeOb() or self.isInPUBG():
            gameglobal.rds.ui.fightObserve.showActionBar()
            gameglobal.rds.ui.showEnterObserveModeState()
        self.refreshOpacityState()

    obSpaceNo = property(get_obSpaceNo, set_obSpaceNo, '', '')

    def get_digongPuzzleInfo(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_PUZZLE_DIGONG)

    digongPuzzleInfo = property(get_digongPuzzleInfo, '', '', '')

    def get_freeSchoolTransferCnt(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_FREE_SCHOOL_TRANSFER_CNT, 0)

    freeSchoolTransferCnt = property(get_freeSchoolTransferCnt, '', '', '')

    def get_noviceCheckInBM(self):
        value = self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_NOVICE_CHECKIN_BM, 0)
        return value

    def set_noviceCheckInBM(self):
        self.applyNoviceCheckInRewardSucc()

    noviceCheckInBM = property(get_noviceCheckInBM, set_noviceCheckInBM, '', '')

    def get_yaojingqitanCostType(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_YJQT_COST_TYPE, 1)

    def set_yaojingqitanCostType(self):
        self.onSelectYaoJingQitanCost()

    yaojingqitanCostType = property(get_yaojingqitanCostType, set_yaojingqitanCostType, '', '')

    def get_lastOpenRoundTableTime(self):
        return self.OCLI[0]['lastOpenRoundTableTime']

    lastOpenRoundTableTime = property(get_lastOpenRoundTableTime, '', '', '')

    def get_ymfScore(self):
        return self.OCLI[0]['ymfScore']

    ymfScore = property(get_ymfScore, '', '', '')

    def get_ymfScoreAward(self):
        return self.OCLI[0]['ymfScoreAward']

    ymfScoreAward = property(get_ymfScoreAward, '', '', '')

    def get_mentorRejectOpt(self):
        return self.OCLI[0]['mentorRejectOpt']

    mentorRejectOpt = property(get_mentorRejectOpt, '', '', '')

    def get_apprenticeRejectOpt(self):
        return self.OCLI[0]['apprenticeRejectOpt']

    apprenticeRejectOpt = property(get_apprenticeRejectOpt, '', '', '')

    def get_useIconUploadItemFlag(self):
        return self.OCLI[0]['useIconUploadItemFlag']

    useIconUploadItemFlag = property(get_useIconUploadItemFlag, '', '', '')

    def get_clanWarReliveStamp(self):
        return self.OCLI[0]['clanWarReliveStamp']

    clanWarReliveStamp = property(get_clanWarReliveStamp, '', '', '')

    def get_battleFieldFinalRewardApplied(self):
        return self.OCLI[0]['battleFieldFinalRewardApplied']

    battleFieldFinalRewardApplied = property(get_battleFieldFinalRewardApplied, '', '', '')

    def get_qumoExp(self):
        return self.OCLI[0]['qumoExp']

    qumoExp = property(get_qumoExp, '', '', '')

    def get_zhanXunActivityBonusApplied(self):
        return self.OCLI[0]['zhanXunActivityBonusApplied']

    zhanXunActivityBonusApplied = property(get_zhanXunActivityBonusApplied, '', '', '')

    def get_totalJunJie(self):
        return self.OCLI[0]['totalJunJie']

    totalJunJie = property(get_totalJunJie, '', '', '')

    def get_jueWeiLv(self):
        return self.OCLI[0]['jueWeiLv']

    jueWeiLv = property(get_jueWeiLv, '', '', '')

    def get_materialBagEnabled(self):
        return self.OCLI[0]['materialBagEnabled']

    materialBagEnabled = property(get_materialBagEnabled, '', '', '')

    def set_materialBagEnabled(self, old, new, part):
        gameglobal.rds.ui.meterialBag.refreshActive()

    def get_marriageNUID(self):
        return self.OCLI[0]['marriageNUID']

    marriageNUID = property(get_marriageNUID, '', '', '')

    def set_marriageNUID(self, old, new, part):
        if old == 0 and new:
            gameglobal.rds.ui.marryPlanOrder.hide()

    def get_engageNUID(self):
        return self.OCLI[0]['engageNUID']

    engageNUID = property(get_engageNUID, '', '', '')

    def set_engageNUID(self, old, new, part):
        if old and not new:
            engageMessageId = getattr(self, 'engageMessageId', None)
            if engageMessageId:
                gameglobal.rds.ui.messageBox.dismiss(engageMessageId, needDissMissCallBack=False)
                self.engageMessageId = None
            engageRejectMessageId = getattr(self, 'engageRejectMessageId', None)
            if engageRejectMessageId:
                gameglobal.rds.ui.messageBox.dismiss(engageRejectMessageId, needDissMissCallBack=False)
                self.engageRejectMessageId = None
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_MARRY_PROPOSE)

    def get_famousGeneralLv(self):
        return self.OCLI[0]['famousGeneralLv']

    famousGeneralLv = property(get_famousGeneralLv, '', '', '')

    def set_famousGeneralLv(self, old, new, part):
        gameglobal.rds.ui.roleInformationJunjie.initUI()
        gameglobal.rds.ui.qumoLevelUp.showFamousPop()

    def get_famousGeneralVal(self):
        return self.OCLI[0]['famousGeneralVal']

    famousGeneralVal = property(get_famousGeneralVal, '', '', '')

    def set_famousGeneralVal(self, old, new, part):
        pass

    def get_invitePoint(self):
        return self.OCLI[0]['invitePoint']

    invitePoint = property(get_invitePoint, '', '', '')

    def set_invitePoint(self, old, new, part):
        fEvent = Event(events.EVENT_INVITE_POINT_CHANGE, new)
        gameglobal.rds.ui.dispatchEvent(fEvent)

    def get_inviteFriendRewardRecord(self):
        return self.OCLI[0]['inviteFriendRewardRecord']

    inviteFriendRewardRecord = property(get_inviteFriendRewardRecord, '', '', '')

    def set_inviteFriendRewardRecord(self, old, new, part):
        pass

    def get_inviteFriendConsumeRecord(self):
        return self.OCLI[0]['inviteFriendConsumeRecord']

    inviteFriendConsumeRecord = property(get_inviteFriendConsumeRecord, '', '', '')

    def set_inviteFriendConsumeRecord(self, old, new, part):
        pass

    def get_chatWorldExTime(self):
        return self.OCLI[0]['chatWorldExTime']

    chatWorldExTime = property(get_chatWorldExTime, '', '', '')

    def get_arenaAwardFlag(self):
        return self.OCLI[0]['arenaAwardFlag']

    arenaAwardFlag = property(get_arenaAwardFlag, '', '', '')

    def get_arenaAwardFlagNoReset(self):
        return self.OCLI[0]['arenaAwardFlagNoReset']

    arenaAwardFlagNoReset = property(get_arenaAwardFlagNoReset, '', '', '')

    def get_zhanXunReward(self):
        return self.OCLI[0]['zhanXunReward']

    zhanXunReward = property(get_zhanXunReward, '', '', '')

    def get_itemRecallLimit(self):
        return self.OCLI[0]['itemRecallLimit']

    itemRecallLimit = property(get_itemRecallLimit, '', '', '')

    def get_quickJoinTimestamp(self):
        return self.OCLI[0]['quickJoinTimestamp']

    quickJoinTimestamp = property(get_quickJoinTimestamp, '', '', '')

    def get_activityAchieveScore(self):
        return self.OCLI[0]['activityAchieveScore']

    activityAchieveScore = property(get_activityAchieveScore, '', '', '')

    def get_rewardedActivityTypes(self):
        return self.OCLI[0]['rewardedActivityTypes']

    rewardedActivityTypes = property(get_rewardedActivityTypes, '', '', '')

    def get_zhanXunExtraBonus(self):
        return self.OCLI[0]['zhanXunExtraBonus']

    zhanXunExtraBonus = property(get_zhanXunExtraBonus, '', '', '')

    def get_weeklyQumoCollectPointsForActivity(self):
        return self.OCLI[0]['weeklyQumoCollectPointsForActivity']

    weeklyQumoCollectPointsForActivity = property(get_weeklyQumoCollectPointsForActivity, '', '', '')

    def get_playedFubenAniScripts(self):
        return self.OCLI[0]['playedFubenAniScripts']

    playedFubenAniScripts = property(get_playedFubenAniScripts, '', '', '')

    def get_charSnapshotTime(self):
        return self.OCLI[0]['charSnapshotTime']

    charSnapshotTime = property(get_charSnapshotTime, '', '', '')

    def get_flowbackBonus(self):
        return self.OCLI[0]['flowbackBonus']

    flowbackBonus = property(get_flowbackBonus, '', '', '')

    def get_gainBackflowVpDaily(self):
        return self.OCLI[0]['gainBackflowVpDaily']

    gainBackflowVpDaily = property(get_gainBackflowVpDaily, '', '', '')

    def get_gainOverflowExpDaily(self):
        return self.OCLI[0]['gainOverflowExpDaily']

    gainOverflowExpDaily = property(get_gainOverflowExpDaily, '', '', '')

    def get_doubleQumo(self):
        return self.OCLI[0]['doubleQumo']

    doubleQumo = property(get_doubleQumo, '', '', '')

    def get_doubleQumoExp(self):
        return self.OCLI[0]['doubleQumoExp']

    doubleQumoExp = property(get_doubleQumoExp, '', '', '')

    def get_apprenticeNBInfo(self):
        return self.OCLI[0]['apprenticeNBInfo']

    apprenticeNBInfo = property(get_apprenticeNBInfo, '', '', '')

    def get_weeklyPuzzleNpcNo(self):
        return self.OCLI[0]['weeklyPuzzleNpcNo']

    weeklyPuzzleNpcNo = property(get_weeklyPuzzleNpcNo, '', '', '')

    def get_weeklyPuzzleCnt(self):
        return self.OCLI[0]['weeklyPuzzleCnt']

    weeklyPuzzleCnt = property(get_weeklyPuzzleCnt, '', '', '')

    def get_weeklyPuzzleInfo(self):
        return self.OCLI[0]['weeklyPuzzleInfo']

    weeklyPuzzleInfo = property(get_weeklyPuzzleInfo, '', '', '')

    def get_triggerPuzzleNpcNo(self):
        return self.OCLI[0]['triggerPuzzleNpcNo']

    triggerPuzzleNpcNo = property(get_triggerPuzzleNpcNo, '', '', '')

    def get_puzzleTriggerInfo(self):
        return self.OCLI[0]['puzzleTriggerInfo']

    puzzleTriggerInfo = property(get_puzzleTriggerInfo, '', '', '')

    def get_dailyGuildDgtCnt(self):
        return self.OCLI[0]['dailyGuildDgtCnt']

    dailyGuildDgtCnt = property(get_dailyGuildDgtCnt, '', '', '')

    def get_worldChallengeInfo(self):
        return self.OCLI[0]['worldChallengeInfo']

    worldChallengeInfo = property(get_worldChallengeInfo, '', '', '')

    def get_useArenaSkillScheme(self):
        return self.OCLI[0]['useArenaSkillScheme']

    useArenaSkillScheme = property(get_useArenaSkillScheme, '', '', '')

    def get_arenaSkillPoint(self):
        return self.OCLI[0]['arenaSkillPoint']

    arenaSkillPoint = property(get_arenaSkillPoint, '', '', '')

    def get_arenaSkillEnhancePoint(self):
        return self.OCLI[0]['arenaSkillEnhancePoint']

    arenaSkillEnhancePoint = property(get_arenaSkillEnhancePoint, '', '', '')

    def get_activation(self):
        return self.OCLI[0]['activation']

    def set_activation(self, old, new, part):
        gameglobal.rds.ui.playRecommActivation.refreshDailyActivation()
        if gameglobal.rds.ui.playRecommActivation.checkCanGetAward():
            gameglobal.rds.ui.playRecommPushIcon.notifyIncompleteItems()
            if getattr(gameglobal.rds.ui, 'playRecommTopPush', None):
                gameglobal.rds.ui.playRecommTopPush.notifyIncompleteItems()

    activation = property(get_activation, '', '', '')

    def get_autoUseBattleFieldShopIndex(self):
        return self.OCLI[0]['autoUseBattleFieldShopIndex']

    def set_autoUseBattleFieldShopIndex(self, old, new, part):
        pass

    autoUseBattleFieldShopIndex = property(get_autoUseBattleFieldShopIndex, '', '', '')

    def get_arenaPlayoffsBetCnt(self):
        return self.OCLI[0]['arenaPlayoffsBetCnt']

    def set_arenaPlayoffsBetCnt(self, old, new, part):
        if gameglobal.rds.ui.arenaPlayoffsBet.widget:
            gameglobal.rds.ui.arenaPlayoffsBet.show(uiConst.ARENA_PLAYOFFS_BET_TAB_MYSELF)

    arenaPlayoffsBetCnt = property(get_arenaPlayoffsBetCnt, '', '', '')

    def get_socialEmoteEnableFlags(self):
        return self.OCLI[0]['socialEmoteEnableFlags']

    def set_socialEmoteEnableFlags(self, old, new, part):
        gameglobal.rds.ui.skill.refreshEmotePanel()

    socialEmoteEnableFlags = property(get_socialEmoteEnableFlags, '', '', '')

    def get_arenaChallengeStatus(self):
        return self.OCLI[0]['arenaChallengeStatus']

    def set_arenaChallengeStatus(self, old, new, part):
        gamelog.debug('@hjx arenaChallenge#set_arenaChallengeStatus:', old, new)
        if old == gametypes.CROSS_ARENA_CHALLENGE_STATUS_DEFAULT and new == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_BY:
            pass
        elif old == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLYING and new == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_SUCC:
            pass
        elif old == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLYING and new == gametypes.CROSS_ARENA_CHALLENGE_STATUS_DEFAULT:
            pass
        elif old == gametypes.CROSS_ARENA_CHALLENGE_STATUS_DEFAULT and new == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLYING:
            self.showGameMsgEx(GMDD.data.ARENA_CHALLENGE_SENDAPPLY_SUCCESS, ())
        else:
            gameglobal.rds.ui.arenaChallengeDeclartion.removeAllArenaMsg()

    arenaChallengeStatus = property(get_arenaChallengeStatus, '', '', '')

    def get_weekActivation(self):
        return self.OCLI[0]['weekActivation']

    def set_weekActivation(self, old, new, part):
        gameglobal.rds.ui.playRecommActivation.updateWeekActivationPushMsg()
        gameglobal.rds.ui.playRecommActivation.refreshWeekActivation()
        gameglobal.rds.ui.activitySaleWeekActivation.refreshInfo()
        gameglobal.rds.ui.activitySale.refreshInfo()

    weekActivation = property(get_weekActivation, '', '', '')

    def get_lastWeekActivation(self):
        return self.OCLI[0]['lastWeekActivation']

    def set_lastWeekActivation(self, old, new, part):
        pass

    lastWeekActivation = property(get_lastWeekActivation, '', '', '')

    def get_activationInfo(self):
        return self.OCLI[0]['activationInfo']

    def set_activationInfo(self, old, new, part):
        gameglobal.rds.ui.playRecomm.refreshInfo()

    activationInfo = property(get_activationInfo, '', '', '')

    def get_activationLv(self):
        return self.OCLI[0]['activationLv']

    def set_activationLv(self, old, new, part):
        gameglobal.rds.ui.playRecommActivation.refreshDailyActivation()

    activationLv = property(get_activationLv, '', '', '')

    def get_activationRewards(self):
        return self.OCLI[0]['activationRewards']

    def set_activationRewards(self, old, new, part):
        gameglobal.rds.ui.playRecommActivation.refreshDailyActivation()
        gameglobal.rds.ui.playRecommActivation.refreshWeekActivation()
        gameglobal.rds.ui.playRecommPushIcon.notifyIncompleteItems()

    activationRewards = property(get_activationRewards, '', '', '')

    def get_weekActivationRewards(self):
        return self.OCLI[0]['weekActivationRewards']

    def set_weekActivationRewards(self, old, new, part):
        gameglobal.rds.ui.playRecommActivation.refreshWeekActivation()
        gameglobal.rds.ui.playRecommActivation.updateWeekActivationPushMsg()

    weekActivationRewards = property(get_weekActivationRewards, '', '', '')

    def get_dynamicShopTradeLimit(self):
        return self.OCLI[0]['dynamicShopTradeLimit']

    def set_dynamicShopTradeLimit(self, old, new, part):
        gameglobal.rds.ui.selfAdaptionShop.refreshInfoWithoutSetDataArray()

    dynamicShopTradeLimit = property(get_dynamicShopTradeLimit, '', '', '')

    def get_expXiuWeiPool(self):
        return self.OCLI[0]['expXiuWeiPool']

    expXiuWeiPool = property(get_expXiuWeiPool, '', '', '')

    def get_expXiuWeiTotal(self):
        return self.OCLI[0]['expXiuWeiTotal']

    expXiuWeiTotal = property(get_expXiuWeiTotal, '', '', '')

    def get_isAppBind(self):
        return self.OCLI[0]['isAppBind']

    isAppBind = property(get_isAppBind, '', '', '')

    def get_kejuInfo(self):
        return self.OCLI[0]['kejuInfo']

    kejuInfo = property(get_kejuInfo, '', '', '')

    def get_lastKejuMonsterTime(self):
        return self.OCLI[0]['lastKejuMonsterTime']

    lastKejuMonsterTime = property(get_lastKejuMonsterTime, '', '', '')

    def get_freezeCash(self):
        return self.OCLI[0]['freezeCash']

    freezeCash = property(get_freezeCash, '', '', '')

    def get_maxFreezeCash(self):
        return self.OCLI[0]['maxFreezeCash']

    maxFreezeCash = property(get_maxFreezeCash, '', '', '')

    def get_freezeCashBail(self):
        return self.OCLI[0]['freezeCashBail']

    freezeCashBail = property(get_freezeCashBail, '', '', '')

    def get_appearanceItemCollectPoint(self):
        return self.OCLI[0]['appearanceItemCollectPoint']

    appearanceItemCollectPoint = property(get_appearanceItemCollectPoint, '', '', '')

    def set_appearanceItemCollectSet(self, old, new, part):
        gameglobal.rds.ui.guibaoge.refreshView()

    def get_appearanceItemCollectSet(self):
        return self.OCLI[0]['appearanceItemCollectSet']

    appearanceItemCollectSet = property(get_appearanceItemCollectSet, '', '', '')

    def set_freezeCash(self, old, new, part):
        gameglobal.rds.ui.inventory.updateFrozenPunishVisible()

    def get_yabiaoCnt(self):
        return self.OCLI[0]['yabiaoCnt']

    def set_yabiaoCnt(self, old, new, part):
        gameglobal.rds.ui.worldWar.refreshWWIconState()

    yabiaoCnt = property(get_yabiaoCnt, '', '', '')

    def get_ownClientPersistentFlags(self):
        return self.OCLI[0]['ownClientPersistentFlags']

    def set_ownClientPersistentFlags(self, old, new, part):
        val = old ^ new
        index = int(math.log(val, 2))
        gamelog.debug('@hjx flags:', old, new, val, index)
        if index == gameCommonBitset.AVT_OWN_CLIENT_PERSISTENT_FLAG_DWORD_APP_BIND_REWARDED:
            gameglobal.rds.ui.accountBind.refreshLevel()
            gameglobal.rds.ui.accountBind.refreshAppBind()
            self.updateRewardHallInfo(uiConst.REWARD_ANQUAN)
        elif index == gameCommonBitset.AVT_OWN_CLIENT_PERSISTENT_FLAG_DWORD_WEIXIN_BIND_REWARDED:
            gameglobal.rds.ui.accountBind.refreshLevel()
            gameglobal.rds.ui.accountBind.refreshWeiXinBind()
            self.updateRewardHallInfo(uiConst.REWARD_ANQUAN)
        elif index == gameCommonBitset.AVT_OWN_CLIENT_PERSISTENT_FLAG_DWORD_WORLD_REFRESH_QUEST_REWARDED:
            gameglobal.rds.ui.playRecommActivation.refreshDailyRecommItems()

    ownClientPersistentFlags = property(get_ownClientPersistentFlags, '', '', '')

    def get_appBindStatus(self):
        return self.OCLI[0]['appBindStatus']

    def set_appBindStatus(self, old, new, part):
        gameglobal.rds.ui.accountBind.refreshLevel()
        gameglobal.rds.ui.accountBind.refreshAppBind()

    appBindStatus = property(get_appBindStatus, '', '', '')

    def get_weixinBindStatus(self):
        return self.OCLI[0]['weixinBindStatus']

    def set_weixinBindStatus(self, old, new, part):
        gameglobal.rds.ui.accountBind.refreshLevel()
        gameglobal.rds.ui.accountBind.refreshWeiXinBind()

    weixinBindStatus = property(get_weixinBindStatus, '', '', '')

    def get_maxEquipEnhanceVal(self):
        return self.OCLI[0]['maxEquipEnhanceVal']

    def set_maxEquipEnhanceVal(self, old, new, part):
        gameglobal.rds.ui.equipSoul.refreshDetailInfo()

    maxEquipEnhanceVal = property(get_maxEquipEnhanceVal, '', '', '')

    def get_currEquipSoulSchemeNo(self):
        return self.OCLI[0]['currEquipSoulSchemeNo']

    def set_currEquipSoulSchemeNo(self, old, new, part):
        self.equipSoul = copy.deepcopy(self.equipSoulSchemeInfo.get(self.currEquipSoulSchemeNo, {}).get('schemeData', {}))
        gameglobal.rds.ui.schemeSwitch.refreshInfo()
        gameglobal.rds.ui.equipSoul.changeScheme()

    currEquipSoulSchemeNo = property(get_currEquipSoulSchemeNo, '', '', '')

    def get_arenaPlayoffsTeamNUID(self):
        return self.OCLI[0]['arenaPlayoffsTeamNUID']

    def set_arenaPlayoffsTeamNUID(self, old, new, part):
        gameglobal.rds.ui.arenaPlayoffs.onArenaPlayoffsTeamInfoChanged()
        if old > 0 and self.arenaPlayoffsTeamNUID == 0:
            self.arenaPlayoffsTeam = {}
            self.arenaPlayoffsMember = {}

    arenaPlayoffsTeamNUID = property(get_arenaPlayoffsTeamNUID, '', '', '')

    def get_arenaPlayoffsTeamLvKey(self):
        return self.OCLI[0]['arenaPlayoffsTeamLvKey']

    def set_arenaPlayoffsTeamLvKey(self, old, new, part):
        gameglobal.rds.ui.arenaPlayoffs.onArenaPlayoffsTeamInfoChanged()

    arenaPlayoffsTeamLvKey = property(get_arenaPlayoffsTeamLvKey, '', '', '')

    def get_arenaPlayoffsTeamHeader(self):
        return self.OCLI[0]['arenaPlayoffsTeamHeader']

    def set_arenaPlayoffsTeamHeader(self, old, new, part):
        gameglobal.rds.ui.arenaPlayoffs.onArenaPlayoffsTeamInfoChanged()

    arenaPlayoffsTeamHeader = property(get_arenaPlayoffsTeamHeader, '', '', '')

    def get_arenaPlayoffsCandidateState(self):
        return self.OCLI[0]['arenaPlayoffsCandidateState']

    def set_arenaPlayoffsCandidateState(self, old, new, part):
        pass

    arenaPlayoffsCandidateState = property(get_arenaPlayoffsCandidateState, '', '', '')

    def get_yabiaoData(self):
        return self.OCLI[0]['yabiaoData']

    yabiaoData = property(get_yabiaoData, '', '', '')

    def set_yabiaoData(self, old, new, part):
        gameglobal.rds.ui.yaBiao.refreshYabiaoView()
        gameglobal.rds.ui.topBar.refreshTopBarWidgets()
        if not self.yabiaoData or not self.yabiaoData.get(gametypes.YABIAO_WHOLE, True):
            gameglobal.rds.ui.littleMap.delYabiaoZaiju()

    def get_itemCommitInfo(self):
        return self.OCLI[0]['itemCommitInfo']

    def set_itemCommitInfo(self, old, new, part):
        gameglobal.rds.ui.worldWar.refreshWWIconState()

    itemCommitInfo = property(get_itemCommitInfo, '', '', '')

    def get_remainCostPvpEnhNum(self):
        return self.OCLI[0]['remainCostPvpEnhNum']

    remainCostPvpEnhNum = property(get_remainCostPvpEnhNum, '', '', '')

    def set_remainCostPvpEnhNum(self, old, new, part):
        gameglobal.rds.ui.pvpEnhance.refreshDetailInfo()

    def get_remainFreePvpEnhNum(self):
        return self.OCLI[0]['remainFreePvpEnhNum']

    remainFreePvpEnhNum = property(get_remainFreePvpEnhNum, '', '', '')

    def set_remainFreePvpEnhNum(self, old, new, part):
        gameglobal.rds.ui.pvpEnhance.refreshDetailInfo()

    def get_addRemainPvpEnhTimes(self):
        return self.OCLI[0]['addRemainPvpEnhTimes']

    addRemainPvpEnhTimes = property(get_addRemainPvpEnhTimes, '', '', '')

    def set_addRemainPvpEnhTimes(self, old, new, part):
        gameglobal.rds.ui.pvpEnhance.refreshDetailInfo()

    def get_resetPvpEnhWeekly(self):
        return self.OCLI[0]['resetPvpEnhWeekly']

    resetPvpEnhWeekly = property(get_resetPvpEnhWeekly, '', '', '')

    def set_resetPvpEnhWeekly(self, old, new, part):
        gameglobal.rds.ui.pvpEnhance.refreshDetailInfo()

    def get_totalPvpEnhVal(self):
        return self.OCLI[0]['totalPvpEnhVal']

    totalPvpEnhVal = property(get_totalPvpEnhVal, '', '', '')

    def get_pairPuzzleNpcNo(self):
        if not self.inWorld:
            return 0
        return self.OCLI[0]['pairPuzzleNpcNo']

    pairPuzzleNpcNo = property(get_pairPuzzleNpcNo, '', '', '')

    def set_pairPuzzleNpcNo(self, old, new, part):
        if self.pairPuzzleNpcNo == 0:
            gameglobal.rds.ui.pairPuzzle.realHide()

    def set_totalPvpEnhVal(self, old, new, part):
        if self.totalPvpEnhVal > old:
            gameglobal.rds.ui.pvpEnhance.resetSuccess(self.totalPvpEnhVal - old)
        gameglobal.rds.ui.pvpEnhance.refreshDetailInfo()

    def set_safeMode(self, old, new, part):
        if len(part) >= 3 and part[-3] == 0:
            safemode = self.OCLI[0]['safeMode'].fixedDict['onSafeMode']
            if safemode:
                self.showSafeMode()
                self.setSafeModeState()
            else:
                self.quitSafeMode()

    def set_ymfScore(self, old, new, part):
        gameglobal.rds.ui.yumufengScore.updateView()
        gameglobal.rds.ui.ymfScoreV2.refreshInfo()
        maxScore = SCD.data.get('ymfMaxScore', 100)
        gameglobal.rds.tutorial.onYmfScoreByPercent(old.get(self.pvpTempCamp, 0), self.ymfScore.get(self.pvpTempCamp, 0), maxScore)

    def set_ymfScoreAward(self, old, new, part):
        gameglobal.rds.ui.yumufengScore.updateView()
        gameglobal.rds.ui.ymfScoreV2.refreshInfo()

    def set_qumoExp(self, old, new, part):
        gameglobal.rds.ui.addNoviceHintPushMessage()

    def set_totalJunJie(self, old, new, part):
        gameglobal.rds.ui.addNoviceHintPushMessage()

    def set_jueWeiLv(self, old, new, part):
        pass

    def set_chatWorldExTime(self, old, new, part):
        new = self.chatWorldExTime
        newLabaId = []
        for labaId in new.keys():
            if labaId not in old.keys():
                newLabaId.append(labaId)
            elif old[labaId] < new[labaId]:
                newLabaId.append(labaId)

        if len(newLabaId):
            gameglobal.rds.ui.changeLaba.show(newLabaId)

    def set_zhanXunReward(self, old, new, part):
        gameglobal.rds.ui.roleInfo.refreshJunjiePanel()
        gameglobal.rds.ui.roleInformationJunjie.initWeekReward()
        self.checkZhanXunBonus()
        self.updateRewardHallInfo(uiConst.REWARD_JUNJIE)

    def set_arenaAwardFlag(self, old, new, part):
        gameglobal.rds.ui.arenaRankAward.refreshSeasonInfo()

    def set_arenaAwardFlagNoReset(self, old, new, part):
        gameglobal.rds.ui.arenaRankAward.refreshLifeTimeInfo()

    def set_activityAchieveScore(self, old, new, part):
        if gameglobal.rds.ui.welfareMergeServer.activityScoreId:
            gameglobal.rds.ui.welfareMergeServer.refreScorePanel()

    def set_rewardedActivityTypes(self, old, new, part):
        if gameglobal.rds.ui.welfareMergeServer.activityScoreId:
            gameglobal.rds.ui.welfareMergeServer.refreScorePanel()

    def set_zhanXunExtraBonus(self, old, new, part):
        gameglobal.rds.ui.roleInfo.refreshJunjiePanel()
        self.checkZhanXunBonus()

    def set_zhanXunActivityBonusApplied(self, old, new, part):
        gameglobal.rds.ui.roleInfo.refreshJunjiePanel()
        self.checkZhanXunBonus()
        self.updateRewardHallInfo(uiConst.REWARD_JUNJIE)
        gameglobal.rds.ui.roleInformationJunjie.initWeekReward()

    def set_weeklyQumoCollectPointsForActivity(self, old, new, part):
        gameglobal.rds.ui.roleInfo.refreshQumoPanel()
        gameglobal.rds.ui.roleInformationQumo.initWeekReward()
        self.checkQumoBonus()
        self.updateRewardHallInfo(uiConst.REWARD_QUMO)

    def set_flowbackBonus(self, old, new, part):
        pass

    def set_useArenaSkillScheme(self, old, new, part):
        pass

    def get_monsterClanWarKillCnt(self):
        return self.OCLI[0]['monsterClanWarKillCnt']

    monsterClanWarKillCnt = property(get_monsterClanWarKillCnt, '', '', '')

    def set_monsterClanWarKillCnt(self, old, new, part):
        if old == 0 and new > 0:
            gameglobal.rds.ui.monsterClanWarActivity.forceOpenMonsterClanWarPushTips()
        gameglobal.rds.ui.monsterClanWarActivity.updateMonsterClanWarPushTips()

    def get_monsterClanWarBossDmg(self):
        return self.OCLI[0]['monsterClanWarBossDmg']

    monsterClanWarBossDmg = property(get_monsterClanWarBossDmg, '', '', '')

    def set_monsterClanWarBossDmg(self, old, new, part):
        gameglobal.rds.ui.monsterClanWarActivity.updateMonsterClanWarPushTips()

    def get_monsterClanWarFame(self):
        return self.OCLI[0]['monsterClanWarFame']

    monsterClanWarFame = property(get_monsterClanWarFame, '', '', '')

    def set_monsterClanWarFame(self, old, new, part):
        gameglobal.rds.ui.monsterClanWarActivity.updateMonsterClanWarPushTips()

    def get_monsterClanWarRewardTime(self):
        return self.OCLI[0]['monsterClanWarRewardTime']

    monsterClanWarRewardTime = property(get_monsterClanWarRewardTime, '', '', '')

    def set_monsterClanWarRewardTime(self, old, new, part):
        gameglobal.rds.ui.monsterClanWarActivity.updateMonsterClanWarPushTips()
        if old == 0 and new > 0:
            gameglobal.rds.ui.monsterClanWarActivity.updateView()
        if old > 0 and new == 0:
            gameglobal.rds.ui.monsterClanWarActivity.closeMonsterClanWarPushTips()

    def setPath_OCLI(self, part, old, new):
        gamelog.debug('jjh@Avatar.setPath_OCLI:', part, old, new)
        if part[-1] == 0:
            prop = OCLI_PROPS[part[-2]]
            func = getattr(self, 'set_' + prop, None)
            if func:
                func(old, new, part)

    def checkZhanXunBonus(self):
        getAwardBtnEnabled = False
        if not hasattr(self, 'zxActivityId'):
            zxActivityId = 0
        else:
            zxActivityId = self.zxActivityId
        curZhanXunFame = self.getFame(const.ZHAN_XUN_FAME_ID)
        lv = self.junJieLv
        hasActGet = False
        if zxActivityId:
            zxData = ASCD.data.get(zxActivityId, {}).get('rewardZXInfo', {}).get(self.junJieLv, None)
            if zxData:
                needPoint = zxData[0]
                if curZhanXunFame > needPoint:
                    if not self.zhanXunActivityBonusApplied:
                        hasActGet = True
        nowLevelData = JCD.data.get(lv, {})
        rewardZXScores = nowLevelData.get('rewardZXScores', [])
        rewardZXBonusList = nowLevelData.get('rewardZXBonusList', [])
        if len(rewardZXScores) == len(rewardZXBonusList):
            for i in xrange(len(rewardZXScores)):
                if curZhanXunFame >= rewardZXScores[i]:
                    getAwardBtnEnabled = True
                    for key, value in self.zhanXunReward.iteritems():
                        if key[1] == i:
                            if value:
                                getAwardBtnEnabled = False

        if hasActGet == False and getAwardBtnEnabled == False:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_JUNJIE_EX_ACT)

    def checkQumoBonus(self):
        canGetReward = False
        gongxianPoint = [180, 300, 560]
        gongxianData = SCD.data.get('pointsToFame', [])
        if len(gongxianData) > 0:
            gongxianPoint[0] = gongxianData[0][0]
            gongxianPoint[1] = gongxianData[1][0]
            gongxianPoint[2] = gongxianData[2][0]
        gotGongxian = self.weeklyQumoCollectPoints if self.weeklyQumoCollectPoints else []
        if len(gotGongxian) == 0 and self.weeklyQumoPoints >= gongxianPoint[0]:
            canGetReward = True
        elif len(gotGongxian) == 1 and self.weeklyQumoPoints >= gongxianPoint[1]:
            canGetReward = True
        elif len(gotGongxian) == 2 and self.weeklyQumoPoints >= gongxianPoint[2]:
            canGetReward = True
        else:
            canGetReward = False
        if not self.canGetQumoActBonus() and not canGetReward:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_QUMO_EX_ACT)

    def canGetQumoActBonus(self):
        if not hasattr(self, 'qumoActivityId'):
            qumoActId = 0
        else:
            qumoActId = self.qumoActivityId
        if qumoActId:
            qmDataList = ASCD.data.get(qumoActId, {}).get('pointsToFame', {})
            coverBonus = []
            for qmData in qmDataList:
                qmBonusItem = {}
                qmBonusItem['actBonusGongxianNeed'] = qmData[0]
                if qmBonusItem['actBonusGongxianNeed'] <= self.weeklyQumoPoints:
                    coverBonus.append(qmBonusItem['actBonusGongxianNeed'])

            if len(coverBonus):
                canGetQumoActBonus = False
                weeklyQumoCollectPointsForActivity = self.weeklyQumoCollectPointsForActivity
                for canGetPoint in coverBonus:
                    canGet = True
                    for wcItem in weeklyQumoCollectPointsForActivity:
                        getedPoint = wcItem[0]
                        if getedPoint == canGetPoint:
                            canGet = False

                    if canGet:
                        canGetQumoActBonus = True
                        break

            else:
                canGetQumoActBonus = False
            return canGetQumoActBonus
        else:
            return False

    def get_attachSkillData(self):
        return self.ACLI[0]['attachSkillData']

    attachSkillData = property(get_attachSkillData, '', '', '')

    def set_attachSkillData(self, old, new, part):
        if len(part) > 2:
            if part[-3] == 4:
                targetId = self.id
                srcId = new
                if new:
                    self.modelServer.enterAttachSkill(srcId, targetId)
                else:
                    self.modelServer.leaveAttachSkill(srcId, targetId)
            elif part[-3] == 0:
                srcId = self.id
                targetId = new
                if new:
                    self.modelServer.enterAttachSkill(srcId, targetId)
                else:
                    self.modelServer.leaveAttachSkill(srcId, targetId)

    def get_bindCoupleEffecct(self):
        return self.ACLI[0]['bindCoupleEffecct']

    bindCoupleEffecct = property(get_bindCoupleEffecct, '', '', '')

    def set_bindCoupleEffecct(self, old, new, part):
        if new:
            self.modelServer.showCoupleEmoteEffect()
        else:
            self.modelServer.releaseCoupleEmoteEffects()

    def get_curBoothToplogoId(self):
        curBoothToplogoId = self.ACLI[0]['curBoothToplogoId']
        return curBoothToplogoId

    curBoothToplogoId = property(get_curBoothToplogoId, '', '', '')

    def set_curBoothToplogoId(self, old, new, part):
        if self.inBoothing() and hasattr(self, 'topLogo'):
            self.topLogo.setBoothBg()
            if self == BigWorld.player():
                gameglobal.rds.ui.booth.refreshCustomWin()

    def get_curBoothModelId(self):
        curBoothModelId = self.ACLI[0]['curBoothModelId']
        return curBoothModelId

    curBoothModelId = property(get_curBoothModelId, '', '', '')

    def set_curBoothModelId(self, old, new, part):
        if self.inBoothing():
            self.switchBoothAspect()
            if self == BigWorld.player():
                gameglobal.rds.ui.booth.refreshCustomWin()

    def get_curFaceEmoteId(self):
        curFaceEmoteId = self.ACLI[0]['curFaceEmoteId']
        return curFaceEmoteId

    curFaceEmoteId = property(get_curFaceEmoteId, '', '', '')

    def set_curFaceEmoteId(self, old, new, part):
        if self == BigWorld.player():
            gameglobal.rds.ui.emote.setFaceEmote()
        self.setFaceEmoteId()

    def get_curEffectTitleId(self):
        curEffectTitleId = self.ACLI[0]['curEffectTitleId']
        return curEffectTitleId

    curEffectTitleId = property(get_curEffectTitleId, '', '', '')

    def set_curEffectTitleId(self, old, new, part):
        if gameglobal.rds.configData.get('enableEffectTitle'):
            if BigWorld.player() == self:
                gameglobal.rds.ui.roleInfo.updateEffectTitle()
                hideFlag = gameglobal.gHidePlayerTitle
            else:
                hideFlag = gameglobal.gHideAvatarTitle
            if hasattr(self, 'topLogo') and self.topLogo:
                if new > 0 and not hideFlag:
                    self.topLogo.showTitleEffect(new)
                else:
                    self.topLogo.removeTitleEffect()

    def get_curEffectTitleLv(self):
        curEffectTitleLv = self.ACLI[0]['curEffectTitleLv']
        return curEffectTitleLv

    curEffectTitleLv = property(get_curEffectTitleLv, '', '', '')

    def set_curEffectTitleLv(self, old, new, part):
        pass

    def get_teamShengSiChangStatus(self):
        teamShengSiChangStatus = self.OCLI[0]['teamShengSiChangStatus']
        return teamShengSiChangStatus

    teamShengSiChangStatus = property(get_teamShengSiChangStatus, '', '', '')

    def set_teamShengSiChangStatus(self, old, new, part):
        gamelog.debug('@hjx team ssc#set_teamShengSiChangStatus:', old, new)
        gameglobal.rds.ui.teamSSCState.onUpdateStateText()
        if new == gametypes.TEAM_SHENG_SI_CHANG_STATUS_CONFIRMING:
            gameglobal.rds.ui.playRecommActivation.refreshItemTip()
        elif new == gametypes.TEAM_SHENG_SI_CHANG_STATUS_CONFIRMED:
            gameglobal.rds.ui.teamSSCMsgBox.confirmEnterSucc()

    def get_effectTitle(self):
        effectTitle = self.OCLI[0]['effectTitle']
        return effectTitle

    effectTitle = property(get_effectTitle, '', '', '')

    def set_effectTitle(self, old, new, part):
        pass

    def get_intimacyTgtName(self):
        intimacyTgtName = self.ACLI[0]['intimacyTgtName']
        return intimacyTgtName

    intimacyTgtName = property(get_intimacyTgtName, '', '', '')

    def set_intimacyTgtName(self, old, new, part):
        pass

    def get_marriageTgtName(self):
        marriageTgtName = self.ACLI[0]['marriageTgtName']
        return marriageTgtName

    marriageTgtName = property(get_marriageTgtName, '', '', '')

    def set_marriageTgtName(self, old, new, part):
        pass

    def get_marriageTitleSex(self):
        marriageTitleSex = self.ACLI[0]['marriageTitleSex']
        return marriageTitleSex

    marriageTitleSex = property(get_marriageTitleSex, '', '', '')

    def set_marriageTitleSex(self, old, new, part):
        pass

    def get_engageTgtName(self):
        engageTgtName = self.ACLI[0]['engageTgtName']
        return engageTgtName

    engageTgtName = property(get_engageTgtName, '', '', '')

    def set_engageTgtName(self, old, new, part):
        if not old and new:
            engageMessageId = getattr(self, 'engageMessageId', None)
            if engageMessageId:
                gameglobal.rds.ui.messageBox.dismiss(engageMessageId, needDissMissCallBack=False)
                self.engageMessageId = None
            engageRejectMessageId = getattr(self, 'engageRejectMessageId', None)
            if engageRejectMessageId:
                gameglobal.rds.ui.messageBox.dismiss(engageRejectMessageId, needDissMissCallBack=False)
                self.engageRejectMessageId = None
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_MARRY_PROPOSE)

    def set_showAidTitleArgs(self, old, new, part):
        pass

    def get_showAidTitleArgs(self):
        return self.ACLI[0]['showAidTitleArgs']

    showAidTitleArgs = property(get_showAidTitleArgs, '', '', '')

    def set_wingWorldCamp(self, old, new, part):
        self.onSetWingWorldCamp(old)

    def get_wingWorldCamp(self):
        return self.ACLI[0]['wingWorldCamp']

    wingWorldCamp = property(get_wingWorldCamp, '', '', '')

    def set_actAppearances(self, old, new, part):
        self.apEffectEx.resetEffect()
        gameglobal.rds.ui.actEffectAppearance.refreshInfo()

    def get_actAppearances(self):
        return self.ACLI[0]['actAppearances']

    actAppearances = property(get_actAppearances, '', '', '')

    def set_groupScoreQL(self, old, new, part):
        if self.topLogo:
            self.topLogo.updateTopLogoInfo()

    def get_groupScoreQL(self):
        return self.ACLI[0]['groupScoreQL']

    groupScoreQL = property(get_groupScoreQL, '', '', '')

    def set_groupScoreBH(self, old, new, part):
        if self.topLogo:
            self.topLogo.updateTopLogoInfo()

    def get_groupScoreBH(self):
        return self.ACLI[0]['groupScoreBH']

    groupScoreBH = property(get_groupScoreBH, '', '', '')

    def get_haoqiVal(self):
        haoqiVal = self.OCLI[0]['haoqiVal']
        return haoqiVal

    haoqiVal = property(get_haoqiVal, '', '', '')

    def set_haoqiVal(self, old, new, part):
        gameglobal.rds.ui.topBar.setValueByName('haoqiVal')

    def get_renpinVal(self):
        renpinVal = self.OCLI[0]['renpinVal']
        return renpinVal

    renpinVal = property(get_renpinVal, '', '', '')

    def get_dieNumInBoarder(self):
        dieNumInBoarder = self.OCLI[0]['dieNumInBoarder']
        return dieNumInBoarder

    dieNumInBoarder = property(get_dieNumInBoarder, '', '', '')

    def set_renpinVal(self, old, new, part):
        gameglobal.rds.ui.topBar.setValueByName('renpinVal')

    def setPath_ACLI(self, part, old, new):
        gamelog.debug('zs@Avatar.setPath_ACLI:', self.id, part, old, new)
        if part[-1] == 0:
            prop = ACLI_PROPS[part[-2]]
            func = getattr(self, 'set_' + prop, None)
            if func:
                func(old, new, part)

    def get_renpinValThisWeek(self):
        renpinValThisWeek = self.OCLI[0]['renpinValThisWeek']
        return renpinValThisWeek

    renpinValThisWeek = property(get_renpinValThisWeek, '', '', '')

    def get_haoqiValThisWeek(self):
        haoqiValThisWeek = self.OCLI[0]['haoqiValThisWeek']
        return haoqiValThisWeek

    haoqiValThisWeek = property(get_haoqiValThisWeek, '', '', '')

    def get_guildMemberShopRefreshCnt(self):
        guildMemberShopRefreshCnt = self.OCLI[0]['guildMemberShopRefreshCnt']
        return guildMemberShopRefreshCnt

    def set_guildMemberShopRefreshCnt(self, old, new, part):
        gameglobal.rds.ui.guildShop.refreshExtraAble()

    guildMemberShopRefreshCnt = property(get_guildMemberShopRefreshCnt, '', '', '')

    def get_puzzleChoiceFlag(self):
        puzzleChoiceFlag = self.OCLI[0]['puzzleChoiceFlag']
        return puzzleChoiceFlag

    puzzleChoiceFlag = property(get_puzzleChoiceFlag, '', '', '')

    def get_updateBonusFlag(self):
        updateBonusFlag = self.OCLI[0]['updateBonusFlag']
        return updateBonusFlag

    def set_updateBonusFlag(self, old, new, part):
        gameglobal.rds.ui.ziXunInfo.refreshRewardPanel()
        gameglobal.rds.ui.topBar.onUpdateClientCfg()

    updateBonusFlag = property(get_updateBonusFlag, '', '', '')

    def get_wbPersonalReward(self):
        val = self.OCLI[0]['wbPersonalReward']
        return val

    wbPersonalReward = property(get_wbPersonalReward, '', '', '')

    def get_wbCountryReward(self):
        val = self.OCLI[0]['wbCountryReward']
        return val

    wbCountryReward = property(get_wbCountryReward, '', '', '')

    def get_wbTaskReward(self):
        val = self.OCLI[0]['wbTaskReward']
        return val

    wbTaskReward = property(get_wbTaskReward, '', '', '')

    def get_wwArmyVotes(self):
        val = self.OCLI[0]['wwArmyVotes']
        return val

    def set_wwArmyVotes(self, old, new, part):
        gameglobal.rds.ui.worldWar.refreshVoteList()

    wwArmyVotes = property(get_wwArmyVotes, '', '', '')

    def get_wwArmyPostId(self):
        val = self.ACLI[0]['wwArmyPostId']
        return val

    def set_wwArmyPostId(self, old, new, part):
        p = BigWorld.player()
        if self.wwArmyPostId:
            if p.inWorldWarEx():
                self.topLogo.refreshGuildIconInWorldWarEx()
        post = p.worldWar.getArmyByGbId(p.gbId)
        if post:
            post.postId = self.wwArmyPostId

    wwArmyPostId = property(get_wwArmyPostId, '', '', '')

    def get_recentEnterWWType(self):
        val = self.OCLI[0]['recentEnterWWType']
        return val

    recentEnterWWType = property(get_recentEnterWWType, '', '', '')

    def get_lastReliveInfo(self):
        val = self.OCLI[0]['lastReliveInfo']
        return val

    lastReliveInfo = property(get_lastReliveInfo, '', '', '')

    def get_autoCoupleEmote(self):
        val = self.ACLI[0]['autoCoupleEmote']
        return val

    autoCoupleEmote = property(get_autoCoupleEmote, '', '', '')

    def get_emoteEnableFlags(self):
        emoteEnableFlags = self.OCLI[0]['emoteEnableFlags']
        return emoteEnableFlags

    emoteEnableFlags = property(get_emoteEnableFlags, '', '', '')

    def set_emoteEnableFlags(self, old, new, part):
        gameglobal.rds.ui.skill.refreshEmotePanel()

    def get_enterWorldTime(self):
        if not self.inWorld:
            return 0
        val = self.OCLI[0]['enterWorldTime']
        return val

    enterWorldTime = property(get_enterWorldTime, '', '', '')

    def get_noviceSignInBM(self):
        val = self.OCLI[0]['noviceSignInBM']
        return val

    noviceSignInBM = property(get_noviceSignInBM, '', '', '')

    def get_noviceDailyOnline(self):
        val = self.OCLI[0]['noviceDailyOnline']
        return val

    noviceDailyOnline = property(get_noviceDailyOnline, '', '', '')

    def set_noviceDailyOnline(self, old, new, part):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        if gameglobal.rds.ui.welfare.mediator:
            gameglobal.rds.ui.welfare.refreshInfo()

    def get_wwArmyMark(self):
        val = self.OCLI[0]['wwArmyMark']
        return val

    wwArmyMark = property(get_wwArmyMark, '', '', '')

    def set_wwArmyMark(self, old, new, part):
        pass

    def get_combatScoreDisplayFlag(self):
        if not self.inWorld:
            return 0
        val = self.OCLI[0]['combatScoreDisplayFlag']
        return val

    combatScoreDisplayFlag = property(get_combatScoreDisplayFlag, '', '', '')

    def get_myHome(self):
        val = self.OCLI[0]['home']
        return val

    def set_home(self, old, new, part):
        if new.fittingRoomLv > old.fittingRoomLv or new.erooms != old.erooms:
            gameglobal.rds.ui.roomEnlarge.enlargeRoomSuccess()
            if new.fittingRoomLv > old.fittingRoomLv:
                editorHelper.instance().lvUpFittingRoom()

    myHome = property(get_myHome, '', '', '')

    def get_overflowExp(self):
        return self.OCLI[0]['overflowExp']

    overflowExp = property(get_overflowExp, '', '', '')

    def get_wbHireHostId(self):
        return self.ACLI[0]['wbHireHostId']

    def set_wbHireHostId(self, old, new, part):
        return gameglobal.rds.ui.worldWar.refreshWWBattleScore()

    wbHireHostId = property(get_wbHireHostId, '', '', '')

    def get_wbApplyHireHostId(self):
        return self.OCLI[0]['wbApplyHireHostId']

    def set_wbApplyHireHostId(self, old, new, part):
        gameglobal.rds.ui.worldWar.refreshServerList()

    wbApplyHireHostId = property(get_wbApplyHireHostId, '', '', '')

    def get_dailyWenquanExp(self):
        return self.dailyStats.get(('exp', 393), 0)

    dailyWenquanExp = property(get_dailyWenquanExp, '', '', '')

    def get_dailyWenquanSocExp(self):
        return self.dailyStats.get(('socExp', 393), 0)

    dailyWenquanSocExp = property(get_dailyWenquanSocExp, '', '', '')

    def get_usedYuanShenDanDaily(self):
        return self.OCLI[0]['usedYuanShenDanDaily']

    usedYuanShenDanDaily = property(get_usedYuanShenDanDaily, '', '', '')

    def get_lastOpenRoundTableTimeInfo(self):
        return self.OCLI[0]['lastOpenRoundTableTimeInfo']

    lastOpenRoundTableTimeInfo = property(get_lastOpenRoundTableTimeInfo, '', '', '')

    def get_curPursuePvpEnhNum(self):
        return self.OCLI[0]['curPursuePvpEnhNum']

    curPursuePvpEnhNum = property(get_curPursuePvpEnhNum, '', '', '')

    def get_maxPursuePvpEnhNum(self):
        return self.OCLI[0]['maxPursuePvpEnhNum']

    maxPursuePvpEnhNum = property(get_maxPursuePvpEnhNum, '', '', '')

    def get_bfDotaTalentSkillIndexList(self):
        return self.OCLI[0]['bfDotaTalentSkillIndexList']

    bfDotaTalentSkillIndexList = property(get_bfDotaTalentSkillIndexList, '', '', '')

    def get_rebalancing(self):
        return self.OCLI[0]['rebalancing']

    def set_rebalancing(self, old, new, part):
        gameglobal.rds.ui.skill.refreshHaoHangDirectionPanel()

    rebalancing = property(get_rebalancing, '', '', '')

    def get_rebalanceMode(self):
        return self.ACLI[0]['rebalanceMode']

    def set_rebalanceMode(self, old, new, part):
        gameglobal.rds.ui.skill.refreshHaoHangDirectionPanel()
        gameglobal.rds.ui.player.refreshUnitType()

    rebalanceMode = property(get_rebalanceMode, '', '', '')

    def get_excitementDoneList(self):
        return self.OCLI[0]['excitementDoneList']

    def set_excitementDoneList(self, old, new, part):
        pass

    excitementDoneList = property(get_excitementDoneList, '', '', '')

    def get_guildPuzzleCnt(self):
        try:
            return self.OCLI[0]['MISC_VAR_OCLI'].get('gpuzzleCnt', 0)
        except:
            return 0

    guildPuzzleCnt = property(get_guildPuzzleCnt, '', '', '')

    def get_partnerNUID(self):
        return self.ACLI[0]['partnerNUID']

    partnerNUID = property(get_partnerNUID, '', '', '')

    def set_partnerNUID(self, old, new, part):
        gamelog.debug('@hjx partner#set_partnerNUID:', old, new)
        if old > 0 and new == 0:
            self.partner = {}
        gameglobal.rds.ui.systemButton.showPartnerNotify()

    def get_hpPool(self):
        return self.OCLI[0]['hpPool']

    def set_hpPool(self, old, new, part):
        gameglobal.rds.ui.player.setHpPool(new)
        gameglobal.rds.ui.player.addHpToolTip()

    hpPool = property(get_hpPool, '', '', '')

    def get_mpPool(self):
        return self.OCLI[0]['mpPool']

    def set_mpPool(self, old, new, part):
        gameglobal.rds.ui.player.setMpPool(new)
        gameglobal.rds.ui.player.addMpToolTip()

    mpPool = property(get_mpPool, '', '', '')

    def get_useItemWish(self):
        return self.OCLI[0]['useItemWish']

    useItemWish = property(get_useItemWish, '', '', '')

    def set_flowbackGroupBonus(self, old, new, part):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        if gameglobal.rds.ui.backflow.widget:
            gameglobal.rds.ui.backflowCatchExp.updateRedPot()
            gameglobal.rds.ui.backflowPriviege.updateRedPot()
            gameglobal.rds.ui.backflowDiscount.updateRedPot()
            gameglobal.rds.ui.backflowDiscount.updateRechargeRewards()

    def get_flowbackGroupBonus(self):
        return self.OCLI[0]['flowbackGroupBonus']

    flowbackGroupBonus = property(get_flowbackGroupBonus, '', '', '')

    def get_wingWorldArmyVoteGbId(self):
        val = self.OCLI[0]['wingWorldArmyVoteGbId']
        return val

    def set_wingWorldArmyVoteGbId(self, old, new, part):
        p = BigWorld.player()
        gameglobal.rds.ui.wingWorldVote.refreshVoteBtns(new)
        p.cell.queryWingWorldArmy(p.wingWorld.armyVer, p.wingWorld.armyOnlineVer)

    wingWorldArmyVoteGbId = property(get_wingWorldArmyVoteGbId, '', '', '')

    def get_wingWorldPostId(self):
        val = self.ACLI[0]['wingWorldPostId']
        return val

    def set_wingWorldPostId(self, old, new, part):
        pass

    wingWorldPostId = property(get_wingWorldPostId, '', '', '')

    def get_wingWorldCampPostId(self):
        val = self.ACLI[0]['wingWorldCampPostId']
        return val

    def set_wingWorldCampPostId(self, old, new, part):
        pass

    wingWorldCampPostId = property(get_wingWorldCampPostId, '', '', '')

    def get_lastGuildNameFromMerger(self):
        val = self.ACLI[0]['lastGuildNameFromMerger']
        return val

    def set_lastGuildNameFromMerger(self, old, new, part):
        pass

    lastGuildNameFromMerger = property(get_lastGuildNameFromMerger, '_', '_', '')

    def set_groupPurchaseInfo(self, old, new, part):
        pass

    def get_groupPurchaseInfo(self):
        return self.OCLI[0]['groupPurchaseInfo']

    groupPurchaseInfo = property(get_groupPurchaseInfo, '', '', '')

    def get_wingWorldArmyMark(self):
        val = self.OCLI[0]['wingWorldArmyMark']
        return val

    wingWorldArmyMark = property(get_wingWorldArmyMark, '', '', '')

    def set_wingWorldArmyMark(self, old, new, part):
        gamelog.info('jbx:set_wingWorldArmyMark')
        gameglobal.rds.ui.wingWorldOverView.refreshArmyMark()

    def set_huntGhostInfo(self, old, new, part):
        gameglobal.rds.ui.huntGhost.refreshHuntGhostInfo()

    def get_huntGhostInfo(self):
        return self.OCLI[0]['huntGhostInfo']

    huntGhostInfo = property(get_huntGhostInfo, '', '', '')

    def set_randomLotteryInfo(self, old, new, part):
        pass

    def get_randomLotteryInfo(self):
        return self.OCLI[0]['randomLotteryInfo']

    randomLotteryInfo = property(get_randomLotteryInfo, '', '', '')

    def set_invisibleTreasureBoxInfo(self, old, new, part):
        pass

    def get_invisibleTreasureBoxInfo(self):
        return self.OCLI[0]['invisibleTreasureBoxInfo']

    invisibleTreasureBoxInfo = property(get_invisibleTreasureBoxInfo, '', '', '')

    def set_randomBagLotteryInfo(self, old, new, part):
        if hasattr(self, 'getPlayerAllTreasureBagData'):
            self.getPlayerAllTreasureBagData()

    def get_randomBagLotteryInfo(self):
        return self.OCLI[0]['randomBagLotteryInfo']

    randomBagLotteryInfo = property(get_randomBagLotteryInfo, '', '', '')

    def set_combatScoreRewardInfo(self, old, new, part):
        gamelog.info('jbx:set_combatScoreRewardInfo', self.combatScoreRewardInfo)
        gameglobal.rds.ui.playRecommStronger.refreshInfo()

    def get_combatScoreRewardInfo(self):
        return self.OCLI[0]['combatScoreRewardInfo']

    combatScoreRewardInfo = property(get_combatScoreRewardInfo, '', '', '')

    def set_guildGrowthNoRegress(self, old, new, part):
        gameglobal.rds.ui.guildGrowth.refreshInfo()

    def get_guildGrowthNoRegress(self):
        return self.OCLI[0]['guildGrowthNoRegress']

    guildGrowthNoRegress = property(get_guildGrowthNoRegress, '', '', '')

    def set_guildGressLearnContribData(self, old, new, part):
        pass

    def get_guildGressLearnContribData(self):
        return self.OCLI[0]['guildGressLearnContribData']

    guildGressLearnContribData = property(get_guildGressLearnContribData, '', '', '')

    def set_freeScore(self, old, new, part):
        gameglobal.rds.ui.avoidDoingActivity.updateFreeScore(old, new)

    def get_freeScore(self):
        return self.OCLI[0]['freeScore']

    freeScore = property(get_freeScore, '', '', '')

    def get_activePropTitleTypeEx(self):
        return self.OCLI[0]['activePropTitleTypeEx']

    activePropTitleTypeEx = property(get_activePropTitleTypeEx, '', '', '')

    def set_activePropTitleTypeEx(self, old, new, part):
        pass

    def get_useWingWorldSkillScheme(self):
        return self.OCLI[0]['useWingWorldSkillScheme']

    def set_useWingWorldSkillScheme(self, old, new, part):
        pass

    useWingWorldSkillScheme = property(get_useWingWorldSkillScheme, '', '', '')

    def get_wingWorldSkillPoint(self):
        return self.OCLI[0]['wingWorldSkillPoint']

    def set_wingWorldSkillPoint(self, old, new, part):
        pass

    wingWorldSkillPoint = property(get_wingWorldSkillPoint, '', '', '')

    def get_wingWorldSkillEnhancePoint(self):
        return self.OCLI[0]['wingWorldSkillEnhancePoint']

    def set_wingWorldSkillEnhancePoint(self, old, new, part):
        pass

    wingWorldSkillEnhancePoint = property(get_wingWorldSkillEnhancePoint, '', '', '')

    def set_totalDailySignInCnt(self, old, new, part):
        pass

    def get_totalDailySignInCnt(self):
        return self.OCLI[0]['totalDailySignInCnt']

    totalDailySignInCnt = property(get_totalDailySignInCnt, '', '', '')

    def set_wingWorldAttendedWar(self):
        gamelog.debug('@hxm set_wingWorldAttendedWar')

    def get_wingWorldAttendedWar(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_WING_WORLD_ATTENDED_WAR, False)

    wingWorldAttendedWar = property(get_wingWorldAttendedWar, '', '', '')

    def set_wingWorldTotalContributeCache(self, old):
        new = self.wingWorldTotalContributeCache
        diff = new - old
        if diff:
            gameglobal.rds.ui.showDefaultLabel(gameStrings.WING_WORLD_CONTRIBUTE, diff, '#47E036')
            self.showGameMsg(GMDD.data.WING_WORLD_CONTRIBUTE_ADD, (diff, new))
        gamelog.debug('@hxm set_wingWorldTotalContributeCache')

    def get_wingWorldTotalContributeCache(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_WING_WORLD_TOTAL_CONTRIBUTE, 0)

    wingWorldTotalContributeCache = property(get_wingWorldTotalContributeCache, '', '', '')

    def set_wingWorldEnterSkillLastUseTime(self):
        gamelog.debug('@hxm set_wingWorldEnterSkillLastUseTime')

    def get_wingWorldEnterSkillLastUseTime(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_WING_WORLD_ENTER_SKILL_LAST_USE_TIME, 0)

    wingWorldEnterSkillLastUseTime = property(get_wingWorldEnterSkillLastUseTime, '', '', '')

    def set_wingWarCityLastTeleportTime(self):
        gamelog.debug('@hxm set_wingWarCityLastTeleportTime')

    def get_wingWarCityLastTeleportTime(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_WING_WAR_CITY_LAST_TELEPORT_TIME, 0)

    wingWarCityLastTeleportTime = property(get_wingWarCityLastTeleportTime, '', '', '')

    def set_wingWarCityLastTeleportCityId(self):
        gamelog.debug('@hxm set_wingWarCityLastTeleportCityId')

    def get_wingWarCityLastTeleportCityId(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_WING_WAR_CITY_LAST_TELEPORT_CITY_ID, 0)

    wingWarCityLastTeleportCityId = property(get_wingWarCityLastTeleportCityId, '', '', '')

    def get_bWingWorldYabiaoAttacker(self):
        val = self.ACLI[0]['bWingWorldYabiaoAttacker']
        return val

    def set_bWingWorldYabiaoAttacker(self, old, new, part):
        gamelog.info('jbx:set_bWingWorldYabiaoAttacker', self.bWingWorldYabiaoAttacker)
        if utils.getNow() < self.bWingWorldYabiaoAttacker:
            self.addYabiaoAttackerEffect()
        else:
            self.delYaBiaoAttackerEffect()

    bWingWorldYabiaoAttacker = property(get_bWingWorldYabiaoAttacker, '', '', '')

    def get_inDyingState(self):
        val = self.ACLI[0]['inDyingState']
        return val

    def set_inDyingState(self, old, new, part):
        pass

    inDyingState = property(get_inDyingState, '', '', '')

    def get_fightForLoveNUID(self):
        return self.OCLI[0]['fightForLoveNUID']

    fightForLoveNUID = property(get_fightForLoveNUID, '', '', '')

    def set_fightForLoveNUID(self, old, new, part):
        self.refreshFFLCreaterEnterPushMessage()

    def get_fightForLoveStatus(self):
        return self.OCLI[0]['fightForLoveStatus']

    fightForLoveStatus = property(get_fightForLoveStatus, '', '', '')

    def set_fightForLoveStatus(self, old, new, part):
        pass

    def get_fightForLoveCreaterRole(self):
        return self.ACLI[0]['fightForLoveCreaterRole']

    fightForLoveCreaterRole = property(get_fightForLoveCreaterRole, '', '', '')

    def set_fightForLoveCreaterRole(self, old, new, part):
        pass

    def get_fightForLoveTitleInfo(self):
        return self.ACLI[0]['fightForLoveTitleInfo']

    fightForLoveTitleInfo = property(get_fightForLoveTitleInfo, '', '', '')

    def set_fightForLoveTitleInfo(self, old, new, part):
        pass

    def get_arenaInfoEx(self):
        return self.OCLI[0]['arenaInfoEx']

    arenaInfoEx = property(get_arenaInfoEx, '', '', '')

    def set_arenaInfoEx(self, old, new, part):
        gameglobal.rds.ui.pvPPanel.refreshTab()
        gameglobal.rds.ui.arenaRankAward.refreshSeasonInfo()

    def get_lastSeasonArenaScore(self):
        return self.OCLI[0]['lastSeasonArenaScore']

    lastSeasonArenaScore = property(get_lastSeasonArenaScore, '', '', '')

    def get_lastSeasonArenaScoreEx(self):
        return self.OCLI[0]['lastSeasonArenaScoreEx']

    lastSeasonArenaScoreEx = property(get_lastSeasonArenaScoreEx, '', '', '')

    def get_arenaAwardFlagEx(self):
        return self.OCLI[0]['arenaAwardFlagEx']

    arenaAwardFlagEx = property(get_arenaAwardFlagEx, '', '', '')

    def set_arenaAwardFlagEx(self, old, new, part):
        gameglobal.rds.ui.arenaRankAward.refreshSeasonInfo()

    def get_arenaAwardFlagNoResetEx(self):
        return self.OCLI[0]['arenaAwardFlagNoResetEx']

    arenaAwardFlagNoResetEx = property(get_arenaAwardFlagNoResetEx, '', '', '')

    def set_arenaAwardFlagNoResetEx(self, old, new, part):
        gameglobal.rds.ui.arenaRankAward.refreshLifeTimeInfo()

    def get_wingWorldZhanXunRankInLastWeek(self):
        return self.OCLI[0]['wingWorldZhanXunRankInLastWeek']

    wingWorldZhanXunRankInLastWeek = property(get_wingWorldZhanXunRankInLastWeek, '', '', '')
    arenaAwardFlagNoResetEx = property(get_arenaAwardFlagNoResetEx, '', '', '')

    def set_randomTurnOverCardInfo(self, old, new, part):
        gamelog.debug('yedawang### set_randomTurnOverCardInfo', self.randomTurnOverCardInfo)
        gameglobal.rds.ui.activitySaleTurnOverCard.onSetRandomTurnOverCardInfo()

    def get_randomTurnOverCardInfo(self):
        return self.OCLI[0]['randomTurnOverCardInfo']

    randomTurnOverCardInfo = property(get_randomTurnOverCardInfo, '', '', '')

    def set_randomCardDrawInfo(self, old, new, part):
        gamelog.debug('zmm### set_randomCardDrawInfo', self.randomCardDrawInfo)
        gameglobal.rds.ui.activitySaleRandomCardDraw.onSetRandomCardDrawInfo()

    def get_randomCardDrawInfo(self):
        return self.OCLI[0]['randomCardDrawInfo']

    randomCardDrawInfo = property(get_randomCardDrawInfo, '', '', '')

    def set_rewardCatchUpInfo(self, old, new, part):
        gamelog.debug('zmm### set_rewardCatchUpInfo', self.rewardCatchUpInfo)

    def get_rewardCatchUpInfo(self):
        return self.OCLI[0]['rewardCatchUpInfo']

    rewardCatchUpInfo = property(get_rewardCatchUpInfo, '', '', '')

    def set_ntStatus(self, old, new, part):
        pass

    def get_ntStatus(self):
        return self.OCLI[0]['ntStatus']

    ntStatus = property(get_ntStatus, '', '', '')

    def set_ntWeekHelp(self, old, new, part):
        pass

    def get_ntWeekHelp(self):
        return self.OCLI[0]['ntWeekHelp']

    ntWeekHelp = property(get_ntWeekHelp, '', '', '')

    def set_ntPartnerGbId(self, old, new, part):
        pass

    def get_ntPartnerGbId(self):
        return self.OCLI[0]['ntPartnerGbId']

    ntPartnerGbId = property(get_ntPartnerGbId, '', '', '')

    def set_valentineInfo(self, old, new, part):
        pass

    def get_valentineInfo(self):
        return self.OCLI[0]['valentineInfo']

    valentineInfo = property(get_valentineInfo, '', '', '')

    def set_lunZhanYunDianInfo(self, old, new, part):
        pass

    def get_lunZhanYunDianInfo(self):
        return self.OCLI[0]['lunZhanYunDianInfo']

    lunZhanYunDianInfo = property(get_lunZhanYunDianInfo, '', '', '')

    def get_skillAppearances(self):
        return self.ACLI[0]['skillAppearances']

    skillAppearances = property(get_skillAppearances, '', '', '')

    def set_skillAppearances(self, old, new, part):
        if hasattr(self, 'skillAppearancesDetail'):
            self.skillAppearancesDetail.updateData()
        gamelog.debug('ypc@ skillAppearances ', new)
        if self.id == BigWorld.player().id:
            evt = Event(events.EVENT_SKILL_APPERANCE, {'changed': old != new})
            gameglobal.rds.ui.dispatchEvent(evt)

    def get_currSelectWsSchemeNo(self):
        return self.OCLI[0]['currSelectWsSchemeNo']

    currSelectWsSchemeNo = property(get_currSelectWsSchemeNo, '', '', '')

    def set_currSelectWsSchemeNo(self, old, new, part):
        pass

    def get_schoolTopVoteInfo(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_SCHOOL_TOP_VOTE_INFO, [])

    def set_schoolTopVoteInfo(self):
        pass

    schoolTopVoteInfo = property(get_schoolTopVoteInfo, '', '', '')

    def get_schoolTopBroadcastServiceNum(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_SCHOOL_TOP_BROADCAST_SERVICE_NUM, 0)

    def set_schoolTopBroadcastServiceNum(self):
        pass

    schoolTopBroadcastServiceNum = property(get_schoolTopBroadcastServiceNum, '', '', '')

    def get_newServerActivityAchieveRewardFlag(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_NEW_SERVER_ACTIVITY_ACHIEVE_REWARD_FLAG, False)

    def set_newServerActivityAchieveRewardFlag(self):
        pass

    newServerActivityAchieveRewardFlag = property(get_newServerActivityAchieveRewardFlag, '', '', '')

    def get_arenaScorePlayerScore(self):
        return self.OCLI[0]['arenaScorePlayerScore']

    arenaScorePlayerScore = property(get_arenaScorePlayerScore, '', '', '')

    def get_crossClanWarTitleInfo(self):
        return self.ACLI[0]['crossClanWarTitleInfo']

    crossClanWarTitleInfo = property(get_crossClanWarTitleInfo, '', '', '')

    def set_crossClanWarTitleInfo(self, old, new, part):
        pass

    def get_newFlagZhanxunDaily(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_NEW_FLAG_ZHANXUN_DAILY, {})

    def set_newFlagZhanxunDaily(self):
        pass

    newFlagZhanxunDaily = property(get_newFlagZhanxunDaily, '', '', '')

    def get_newFlagZhanxunReward(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_NEW_FLAG_ZHANXUN_REWARD, {})

    def set_newFlagZhanxunReward(self):
        pass

    newFlagZhanxunReward = property(get_newFlagZhanxunReward, '', '', '')

    def get_guildGrowthVolumnRewardInfo(self):
        return self.OCLI[0]['guildGrowthVolumnRewardInfo']

    guildGrowthVolumnRewardInfo = property(get_guildGrowthVolumnRewardInfo, '', '', '')

    def get_useCrossBFSkillScheme(self):
        return self.OCLI[0]['useCrossBFSkillScheme']

    useCrossBFSkillScheme = property(get_useCrossBFSkillScheme, '', '', '')

    def get_crossBFSkillPoint(self):
        return self.OCLI[0]['crossBFSkillPoint']

    crossBFSkillPoint = property(get_crossBFSkillPoint, '', '', '')

    def get_crossBFSkillEnhancePoint(self):
        return self.OCLI[0]['crossBFSkillEnhancePoint']

    crossBFSkillEnhancePoint = property(get_crossBFSkillEnhancePoint, '', '', '')

    def set_lingShiNextTime(self, old, new, part):
        gameglobal.rds.ui.actionbar.updateSlots()

    def get_lingShiNextTime(self):
        return self.OCLI[0]['lingShiNextTime']

    lingShiNextTime = property(get_lingShiNextTime, '', '', '')

    def get_weeklyFame(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_WEEKLY_FAME, {})

    def set_weeklyFame(self):
        pass

    weeklyFame = property(get_weeklyFame, '', '', '')

    def get_validBalanceArenaWeeklyCnt(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_VALID_BALANCE_ARENA_WEEKLY_CNT, 0)

    def set_validBalanceArenaWeeklyCnt(self):
        pass

    validBalanceArenaWeeklyCnt = property(get_validBalanceArenaWeeklyCnt, '', '', '')

    def set_learnSkillEnhanceScore(self, old, new, part):
        gameglobal.rds.ui.skill.refreshXiuLianScore()

    def get_learnSkillEnhanceScore(self):
        return self.OCLI[0]['learnSkillEnhanceScore']

    learnSkillEnhanceScore = property(get_learnSkillEnhanceScore, '', '', '')

    def set_aidTitleInfo(self, old, new, part):
        pass

    def get_aidTitleInfo(self):
        return self.OCLI[0]['aidTitleInfo']

    aidTitleInfo = property(get_aidTitleInfo, '', '', '')

    def get_guanYinFirstEquip(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_GUANYIN_FIRST_EQUIP, 0)

    def set_guanYinFirstEquip(self):
        pass

    guanYinFirstEquip = property(get_guanYinFirstEquip, '', '', '')

    def get_mapGameFameRecord(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_FAME_RECORD, 0)

    def set_mapGameFameRecord(self):
        pass

    mapGameFameRecord = property(get_mapGameFameRecord, '', '', '')

    def get_mapGameRewardRecord(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_REWARD_RECORD, {})

    def set_mapGameRewardRecord(self):
        gameglobal.rds.ui.mapGameMap.refreshRewardRecord()

    mapGameRewardRecord = property(get_mapGameRewardRecord, '', '', '')

    def get_mapGameBossReward(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_BOSS_REWARD_RECORD, {})

    def set_mapGameBossReward(self):
        gameglobal.rds.ui.mapGameDamage.refreshInfo()

    mapGameBossReward = property(get_mapGameBossReward, '', '', '')

    def get_mapGameBossDamage(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_BOSS_DAMAGE, {})

    def set_mapGameBossDamage(self):
        gameglobal.rds.ui.mapGameDamage.refreshInfo()

    mapGameBossDamage = property(get_mapGameBossDamage, '', '', '')

    def get_mapGameFirstOpen(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_FIRST_OPEN, False)

    def set_mapGameFirstOpen(self):
        pass

    mapGameFirstOpen = property(get_mapGameFirstOpen, '', '', '')

    def get_wingWorldPower(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_WING_WORLD_POWER, 0)

    def set_wingWorldPower(self):
        pass

    wingWorldPower = property(get_wingWorldPower, '', '', '')

    def get_loopQuestWeightLimit(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_LOOP_QUEST_WEIGHT_LIMIT, 0)

    def set_loopQuestWeightLimit(self):
        pass

    loopQuestWeightLimit = property(get_loopQuestWeightLimit, '', '', '')

    def get_wwcAutoFollow(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_WWC_AUTO_FOLLOW, 0)

    def set_wwcAutoFollow(self):
        BigWorld.player().addWWCampAutoFollowGuildPush()

    wwcAutoFollow = property(get_wwcAutoFollow, '', '', '')

    def get_freezeGuildContri(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_FREEZE_GUILD_CONTRI, 0)

    def set_freezeGuildContri(self):
        pass

    freezeGuildContri = property(get_freezeGuildContri, '', '', '')

    def set_activityCollectInfo(self, old, new, part):
        gameglobal.rds.ui.activitySaleCollect.refreshBonusInfo()

    def get_activityCollectInfo(self):
        return self.OCLI[0]['activityCollectInfo']

    activityCollectInfo = property(get_activityCollectInfo, '', '', '')

    def get_pubgRankPoints(self):
        return self.OCLI[0]['pubgRankPoints']

    pubgRankPoints = property(get_pubgRankPoints, '', '', '')

    def get_subGuanYinInfo(self):
        return self.OCLI[0]['subGuanYinInfo']

    subGuanYinInfo = property(get_subGuanYinInfo, '', '', '')

    def get_mapGameCamp(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_CAMP, 0)

    def set_mapGameCamp(self):
        if gameglobal.rds.configData.get('enableMapGameV2'):
            gameglobal.rds.ui.mapGameMapV2.setGameCamp()

    mapGameCamp = property(get_mapGameCamp, '', '', '')

    def get_mapGameGraveEndFlashState(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_GRAVE_END_FLASH_STATE, 0)

    def set_mapGameGraveEndFlashState(self):
        pass

    mapGameGraveEndFlashState = property(get_mapGameGraveEndFlashState, '', '', '')

    def get_mapGameGraveEndState(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_GRAVE_END_STATE, 0)

    def set_mapGameGraveEndState(self):
        gameglobal.rds.ui.mapGameMapV2.onChangeGraveState()

    mapGameGraveEndState = property(get_mapGameGraveEndState, '', '', '')

    def get_mapGameEventReward(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_EVENT_REWARD, [])

    def set_mapGameEventReward(self):
        if gameglobal.rds.configData.get('enableMapGameV2'):
            gameglobal.rds.ui.mapGameMapV2.refreshInfo()

    mapGameEventReward = property(get_mapGameEventReward, '', '', '')

    def get_mapGameSpriteDispatch(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_SPRITE_LAST_DISPATCH, {})

    def set_mapGameSpriteDispatch(self):
        pass

    mapGameSpriteDispatch = property(get_mapGameSpriteDispatch, '', '', '')

    def get_mapGameGridDispatch(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_MAP_GAME_GRID_LAST_DISPATCH, {})

    def set_mapGameGridDispatch(self):
        pass

    mapGameGridDispatch = property(get_mapGameGridDispatch, '', '', '')

    def get_freezeFameDict(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_FREEZE_FAME_DICT, {})

    def set_freezeFameDict(self):
        pass

    freezeFameDict = property(get_freezeFameDict, '', '', '')

    def get_pubgStaticWeekly(self):
        return self.OCLI[0]['MISC_VAR_OCLI'].get(gametypes.MISC_VAR_OCLI_PUBG_STATIC_WEEKLY, (0, 0))

    def set_pubgStaticWeekly(self):
        pass

    pubgStaticWeekly = property(get_pubgStaticWeekly, '', '', '')

    def set_luckyLotteryInfo(self, old, new, part):
        pass

    def get_luckyLotteryInfo(self):
        return self.OCLI[0]['luckyLotteryInfo']

    luckyLotteryInfo = property(get_luckyLotteryInfo, '', '', '')
