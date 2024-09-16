#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/uiAdapter.o
from gamestrings import gameStrings
import math
import time
import random
import urlparse
import BigWorld
import Scaleform
from Scaleform import GfxValue
import Sound
import GUI
import Math
import game
import gameglobal
import ui
import littlemap
import const
import clientcom
import gametypes
import keys
import utils
import gamelog
import uiDrag
import npcConst
import formula
import debug
import wingWorldUtils
from helpers import cc
from helpers import sceneInfo
from helpers import cellCmd
from helpers import action
from helpers import capturePhoto
from helpers import navigator
from helpers import ccControl
from helpers import uiProfile
from helpers.eventDispatcher import EventDispatcher
from guis import uiConst, regExpUtils, uiUtils, tipUtils
from guis import cursor
from guis import events
from messageBoxProxy import MBButton
from guis import menuManager
from guis.asObject import MenuManager
from ui import gbk2unicode
from ui import unicode2gbk
from gameclass import Singleton
from appSetting import Obj as AppSettings
from item import Item
from guis import topLogo
from guis import pinyinConvert
from guis import ime
from guis import groupUtils
from guis import redPotUtils
from debug import storyEditDebugProxy
from callbackHelper import Functor
from sfx import screenRipple
from guis import asObject
from asObject import ASObject
from gameStrings import gameStrings
from guis.asObject import ASUtils
from helpers.GUITextFactory import GUITextFactory
import gameconfigCommon
from data import state_data as SD
from data import ui_weight_data as UWD
from data import ui_location_data as ULD
from data import skill_avatar_data as SAD
from data import skill_ui_effect_data as SUED
from data import zaiju_data as ZD
from data import qte_data as QTED
from data import clan_war_tip_data as CWTD
from data import fb_data as FD
from data import fight_for_love_config_data as FFLCD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import ui_help_data as UHD
from data import map_config_data as MCD
from data import bonus_data as BD
from data import game_msg_data as GMD
from data import mingpai_data as MPD
from data import prop_ref_data as PRD
from cdata import prop_ref_reverse_data as PRRD
from data import world_war_army_data as WWAD

def getInstance():
    return UIAdapter.getInstance()


AS_LOG_WARNING_CNT = 10
ENALBE_AS_LOG_WARNING = False
SPRITE_ICON_PATH = 'summonedSprite/icon/%s.dds'

class UIAdapter(EventDispatcher):
    __metaclass__ = Singleton

    def __init__(self):
        EventDispatcher.__init__(self)
        self.proxyList = ['pushMessageProxy',
         'chatProxy',
         'actionbarProxy',
         'castbarProxy',
         'inventoryProxy',
         'loginWinProxy',
         'loginSelectServerProxy',
         'doubleCheckWithInputProxy',
         'challengeProxy',
         'rolecardProxy',
         'shaXingProxy',
         'fightObserveProxy',
         'questProxy',
         'targetProxy',
         'subTargetProxy',
         'playerProxy',
         'secrecyProxy',
         'creatorProxy',
         'tinkerProxy',
         'fangkadianProxy',
         'inventoryLatchTimeProxy',
         'guildTechResearchProxy',
         'guildAstrologyChooseProxy',
         'interactiveObjProxy',
         'interactiveObjMountsProxy',
         'debugProxy',
         'generaldebugProxy',
         'lvUpGuideProxy',
         'breathbarProxy',
         'continuousHitProxy',
         'runeLvUpProxy',
         'applyGuildProxy',
         'runeForgingProxy',
         'fittingRoomProxy',
         'guildBuildRemoveProxy',
         'guildBuildSelectRemoveProxy',
         'modelFittingRoomProxy',
         'modelRoleInfoProxy',
         'systemButtonProxy',
         'notifyProxy',
         'systemButtonProxy',
         'helpProxy',
         'correctQteProxy',
         'exactQteProxy',
         'accumulateQteProxy',
         'compositeShopConfirmProxy',
         'callTeammateProxy',
         'guildFactoryProxy',
         'guildCrossTResultProxy',
         'guildCrossTFinalResultProxy',
         'gmWidgetProxy',
         'gmGroupWidgetProxy',
         'gmParameterWidgetProxy',
         'characterCreateProxy',
         'guildProxy',
         'runeReforgingProxy',
         'inventoryResetPasswordProxy',
         'guildProduceProxy',
         'characterDetailAdjustProxy',
         'npcPanelProxy',
         'fubenProxy',
         'shopProxy',
         'littleMapProxy',
         'gmChatProxy',
         'guildAssartProxy',
         'fameSalaryProxy',
         'guildChallengeFieldProxy',
         'bFScoreAwardProxy',
         'cefTestProxy',
         'topMessageProxy',
         'messageBoxProxy',
         'targetCircleProxy',
         'bossBloodProxy',
         'runeViewProxy',
         'runeFeedProxy',
         'createGuildProxy',
         'runeChongXiProxy',
         'guildAuthorizationProxy',
         'guildSawmillProxy',
         'guildBusinessFindPathProxy',
         'simpleQTEProxy',
         'expbarProxy',
         'npcSlotProxy',
         'pickUpProxy',
         'generalCastbarProxy',
         'teamBaseProxy',
         'teamProxy',
         'guildMemberProxy',
         'chatRoomPasswordProxy',
         'guildBillBoardProxy',
         'guildBusinessDelegateProxy',
         'summonedSpriteUnitFrameProxy',
         'summonedSpriteGMProxy',
         'towerDefenseProxy',
         'questLogProxy',
         'multiNpcChatProxy',
         'questTrackProxy',
         'debateProxy',
         'mapProxy',
         'skillProxy',
         'fubenLoginProxy',
         'multiBossBloodProxy',
         'storageCashProxy',
         'guildExtractProxy',
         'guildBusinessDelegatePublishProxy',
         'dyingProxy',
         'rankProxy',
         'arenaProxy',
         'dragButtonProxy',
         'hotkeyProxy',
         'introducerProxy',
         'zhanQiProxy',
         'duelMatchTimeProxy',
         'achievePushProxy',
         'guildPostProxy',
         'chatRoomCreateProxy',
         'indulgePushProxy',
         'newbieGuideExamProxy',
         'beastActionBarProxy',
         'fubenClockProxy',
         'funcNpcProxy',
         'targetRoleInfoProxy',
         'roleInfoHonorProxy',
         'teamCommProxy',
         'newGuiderOperaProxy',
         'guildAnnouncementProxy',
         'carnivalPushProxy',
         'serveFoodProxy',
         'guildExploreStateProxy',
         'guildCallMemberProxy',
         'interactiveActionBarProxy',
         'reliveMsgBoxProxy',
         'scenarioPlateProxy',
         'equipRepairProxy',
         'deadAndReliveProxy',
         'pressKeyFProxy',
         'tradeProxy',
         'chatRoomWindowProxy',
         'guildBuildUpgradeProxy',
         'guildScaleUpgradeProxy',
         'guildBuildSelectProxy',
         'guildActivityOpenProxy',
         'teamEnemyArenaProxy',
         'bulletProxy',
         'sackProxy',
         'assignProxy',
         'zaijuProxy',
         'payItemProxy',
         'questPhotoProxy',
         'qinggongBarProxy',
         'achievementProxy',
         'inventoryPasswordProxy',
         'guildArmorProxy',
         'guildBusinessBagProxy',
         'guildBusinessShopProxy',
         'arenaWaitProxy',
         'taskShareProxy',
         'compositeShopProxy',
         'playTipsProxy',
         'systemTipsProxy',
         'storageProxy',
         'guildResidentProxy',
         'guildResidentManagerProxy',
         'guildContrabandProxy',
         'surrenderProxy',
         'diGongProxy',
         'autoQuestProxy',
         'tradeRequestProxy',
         'activityPushProxy',
         'battleFieldProxy',
         'equipPushProxy',
         'bossInfoProxy',
         'chatToFriendProxy',
         'guildDispatchProxy',
         'guildDispatchIntoProxy',
         'vehicleChooseProxy',
         'scoreInfoProxy',
         'littleScoreInfoProxy',
         'vehicleSkillProxy',
         'zaijuV2Proxy',
         'bfDotaItemAndPropProxy',
         'bfDotaChooseHeroLeftProxy',
         'bfDotaChooseHeroRightProxy',
         'bfDotaChooseHeroBottomProxy',
         'uiStateManagerProxy',
         'friendProxy',
         'skillPushProxy',
         'systemSettingProxy',
         'debugSettingProxy',
         'boothProxy',
         'inventorySetPasswordProxy',
         'guildWuShuangProxy',
         'guildWuShuangSelectProxy',
         'kejuGuideProxy',
         'fishingProxy',
         'trainingNpcProxy',
         'trainingFubenEvalProxy',
         'fishingGameProxy',
         'fubenMessageProxy',
         'prosecuteProxy',
         'rideTogetherProxy',
         'dailyAttendProxy',
         'guildDonateReserveProxy',
         'guildTournamentRankProxy',
         'chargeRewardProxy',
         'fubenInfoProxy',
         'goHomeProxy',
         'addEnemyProxy',
         'levelUpProxy',
         'feedbackProxy',
         'yingXiaoFeedbackProxy',
         'itemQuestProxy',
         'buffNoticeProxy',
         'trainingAreaProxy',
         'guildRenameProxy',
         'guildActivityTimeProxy',
         'userBackProxy',
         'userBackAwardProxy',
         'fubenStatProxy',
         'mailProxy',
         'consignProxy',
         'emoteProxy',
         'noticeBoardProxy',
         'groupProxy',
         'trainingAreaAwardProxy',
         'exploreProxy',
         'shengSiChangProxy',
         'guildResidentRecProxy',
         'guildResidentHiredProxy',
         'guildTournamentResultProxy',
         'guildTournamentApplyProxy',
         'propSchemeProxy',
         'useTipsProxy',
         'equipFeedProxy',
         'equipFuncProxy',
         'lifeSkillProxy',
         'resourceMarketProxy',
         'battleFieldShopProxy',
         'lifeSkillGuideProxy',
         'diceQuestProxy',
         'cameraProxy',
         'guildResidentUpdateTiredProxy',
         'bindItemTradeProxy',
         'puzzleProxy',
         'qteNoticeProxy',
         'topBarProxy',
         'loginWinBottomProxy',
         'fubenGuideProxy',
         'clanWarProxy',
         'equipMixProxy',
         'playRecommProxy',
         'dynamicResultProxy',
         'delegationBookProxy',
         'yunchuijiProxy',
         'playRecommPushIconProxy',
         'loadingProxy',
         'dyeColorProxy',
         'oldFriendProxy',
         'jobBoardProxy',
         'applyRewardProxy',
         'regionQuestProxy',
         'abilityTreeProxy',
         'systemPushProxy',
         'huazhuangProxy',
         'daFuWengProxy',
         'guildDonateProxy',
         'guildStorageProxy',
         'fullscreenFittingRoomProxy',
         'guildMemberAssginProxy',
         'guildShopExtraProxy',
         'guildGrowthProxy',
         'scenarioBoxProxy',
         'dyePlaneProxy',
         'fashionBagProxy',
         'dyePanelProxy',
         'autoFetchFashionProxy',
         'easyPayProxy',
         'roundTableProxy',
         'roleLoadProxy',
         'achievementScoreProxy',
         'fbDeadDataProxy',
         'fbDeadDetailDataProxy',
         'spriteAniProxy',
         'bugFeedbkProxy',
         'guildActivityProxy',
         'inGameEvaluationProxy',
         'cCControlProxy',
         'cCCreateRoomProxy',
         'guildFindStarProxy',
         'accountBindProxy',
         'yaoPeiMixProxy',
         'yaoPeiFeedProxy',
         'yaoPeiLvUpProxy',
         'yaoPeiTransferProxy',
         'yaoPeiReforgeProxy',
         'yaoPeiReforgeResultProxy',
         'pvpEnhanceProxy',
         'unBindItemProxy',
         'mixFameJewelryProxy',
         'guanYinProxy',
         'guanYinAddSkillProxy',
         'qingGongJingSuProxy',
         'tianyuMallProxy',
         'mibaoProxy',
         'fameCollectProxy',
         'qingGongJingSuTimeProxy',
         'mountsProxy',
         'airbarProxy',
         'bookProxy',
         'yixinBindProxy',
         'yixinRewardsProxy',
         'yixinGuildSendMsgProxy',
         'yixinSettingProxy',
         'festivalPushProxy',
         'huazhuangPlusProxy',
         'hideModeSettingProxy',
         'equipSignProxy',
         'rechargeProxy',
         'guildGroupProxy',
         'shishenModeProxy',
         'propSchemeResumeProxy',
         'propResetProxy',
         'expandPayProxy',
         'itemSelectProxy',
         'shishenBoardProxy',
         'purchaseShopProxy',
         'purchaseSellProxy',
         'suiXingYuProxy',
         'equipEnhanceProxy',
         'equipEnhanceHistoryProxy',
         'equipEnhanceResultProxy',
         'moneyConvertConfirmProxy',
         'equipmentSlotProxy',
         'equipGemProxy',
         'skillSchemeProxy',
         'skillSchemeV2Proxy',
         'itemRecastProxy',
         'wingAndMountProxy',
         'wingAndMountUpgradeProxy',
         'queryLocationProxy',
         'yixinImageProxy',
         'expBonusProxy',
         'birdLetHotLineProxy',
         'isolateProxy',
         'valuableTradeProxy',
         'qumoLevelUpProxy',
         'equipRedemptionProxy',
         'equipMixNewProxy',
         'inviteFriendProxy',
         'itemResumeProxy',
         'yumufengScoreProxy',
         'mentorProxy',
         'gmMessageProxy',
         'customerServiceProxy',
         'customerServiceSecondProxy',
         'lifeSkillNewProxy',
         'clearPasswordProxy',
         'wmdRankListProxy',
         'ycwzRankListProxy',
         'userAccountBindProxy',
         'itemRecallProxy',
         'lifeSkillBreakProxy',
         'itemUseProxy',
         'barrageProxy',
         'guildSalaryAssignProxy',
         'dyeResetProxy',
         'guildSalaryReceiveProxy',
         'fubenDegreeProxy',
         'quickJoinProxy',
         'guildLuxuryRankProxy',
         'relivePosSelectProxy',
         'changeLabaProxy',
         'guildSalaryHistoryProxy',
         'baoDianProxy',
         'offlineIncomeProxy',
         'imeProxy',
         'equipCopyProxy',
         'zhanXunRankListProxy',
         'newGuiderOperationHintProxy',
         'summonFriendProxy',
         'summonFriendNewProxy',
         'itemBuyConfirmProxy',
         'guildRewardSalaryHistoryProxy',
         'guildRewardSalaryAssignProxy',
         'pvPPanelProxy',
         'arenaRankAwardProxy',
         'arenaRankListProxy',
         'pushNoticeProxy',
         'flashProxy',
         'migrateServerProxy',
         'characterCopyProxy',
         'changeAimProxy',
         'xiuLianAwardProxy',
         'getSkillPointProxy',
         'tutorialQteProxy',
         'qrCodeProxy',
         'monsterBloodProxy',
         'newServerActivityProxy',
         'skillGuideProxy',
         'newbieGuideProxy',
         'votePushProxy',
         'activityReSignInProxy',
         'focusTargetProxy',
         'customerServiceVipProxy',
         'completeInfoProxy',
         'diGongDetailProxy',
         'friendFlowBackProxy',
         'guildMemberLvSetProxy',
         'equipSuitProxy',
         'bottleProxy',
         'guildMatchProxy',
         'phaseFubenProxy',
         'fireWorkSenderProxy',
         'frozenPunishProxy',
         'xinmoRecordProxy',
         'xinmoBookProxy',
         'fashionPropTransferProxy',
         'guildJobProxy',
         'perFontTextProxy',
         'callFriendProxy',
         'guibaogeProxy',
         'yaBiaoProxy',
         'jieQiProxy',
         'worldWarProxy',
         'crossServerBagProxy',
         'lotteryProxy',
         'raffleProxy',
         'pinJiuProxy',
         'fubenAwardTimesProxy',
         'waBaoProxy',
         'guideGoalProxy',
         'waBaoResultProxy',
         'guildQuickJoinProxy',
         'activationProxy',
         'activitySaleProxy',
         'activitySaleFirstPayProxy',
         'activitySaleFirstBuyProxy',
         'activitySalePointsRewardProxy',
         'activitySaleBuyProxy',
         'activitySaleLevelBonusProxy',
         'equipChangeProxy',
         'equipChangeEnhanceProxy',
         'equipChangeEnhanceTransferProxy',
         'equipChangeSuitActivateProxy',
         'equipChangeJuexingRebuildProxy',
         'equipChangeJuexingStrengthProxy',
         'equipChangePrefixRebuildProxy',
         'equipChangeInlayProxy',
         'equipChangePrefixTransferProxy',
         'wenQuanDetailProxy',
         'sidiGuideProxy',
         'fubenQuestProxy',
         'huiZhangRepairProxy',
         'monsterClanWarActivityProxy',
         'fameCashExchangeProxy',
         'zhanJuProxy',
         'characterPrePayProxy',
         'ziXunInfoProxy',
         'holidayMessageBoxProxy',
         'innerIEProxy',
         'wishMadeProxy',
         'redPacketProxy',
         'tuZhuangProxy',
         'meterialBagProxy',
         'activityShopProxy',
         'wishMadeViewProxy',
         'itemPushUseProxy',
         'zhenyaoProxy',
         'callBackMessageBoxProxy',
         'fengWuZhiProxy',
         'rewardHallProxy',
         'fengWuZhiItemPushProxy',
         'fengWuZhiCluePushProxy',
         'bFReportChooseProxy',
         'bFReportReasonProxy',
         'sanCunProxy',
         'mentorExProxy',
         'realSenseProxy',
         'daShanProxy',
         'fubenBangDaiProxy',
         'manualEquipProxy',
         'dailySignInProxy',
         'friendRequestProxy',
         'pushBonusProxy',
         'spaceGiftGivingProxy',
         'spaceLabelSettingProxy',
         'feihuoLoginProxy',
         'spaceTouchProxy',
         'friendListProxy',
         'labaConfirmProxy',
         'spaceGiftBoxProxy',
         'fubenProgressProxy',
         'playerSelectProxy',
         'spaceHeadSettingProxy',
         'homeCheckHousesProxy',
         'spaceFuDaiProxy',
         'homeBuyHousesProxy',
         'arenaPlayoffsProxy',
         'homeEditorProxy',
         'homeSendToFloorProxy',
         'homePermissionProxy',
         'interactiveObjConfirmProxy',
         'equipChangeStarActivateProxy',
         'equipChangeStarLvUpProxy',
         'yunChuiShopProxy',
         'homeDoorPlateProxy',
         'guildRunnerProxy',
         'rewardGiftActivityIconsProxy',
         'welfareProxy',
         'welfareSevenDayLoginProxy',
         'activitySaleGiftBagProxy',
         'activitySaleMallBoxProxy',
         'activitySaleDailyGiftProxy',
         'guildMenifestProxy',
         'welfareSummerProxy',
         'welfareOnlineRewardProxy',
         'welfareMergeServerProxy',
         'welfareEveryDayRewardProxy',
         'diGongPuzzleProxy',
         'welfareRewardHallProxy',
         'welfareFudanRewardProxy',
         'homeEnterLinesProxy',
         'guildRobberActivityPushProxy',
         'arenaPlayoffsBetProxy',
         'arenaPlayoffsBetTop4Proxy',
         'arenaPlayoffsBetDayProxy',
         'arenaPlayoffsBetPeakProxy',
         'arenaPlayoffsBetMyselfProxy',
         'arenaPlayoffsBetConfirmProxy',
         'roleInformationHierogramProxy',
         'mallWebProxy',
         'zhancheInfoProxy',
         'guildWWZhengfengResultProxy',
         'guildWWTournamentResultProxy',
         'guildWWDuoshuaiResultProxy',
         'guildWWFinalResultProxy',
         'guildWWTournamentRankProxy',
         'equipSoulProxy',
         'equipSoulStarProxy',
         'activitySaleNewbiePayProxy',
         'welfareRewardRecoveryProxy',
         'activitySaleLoopChargeProxy',
         'roleInfoProxy',
         'roleInfoJingjieProxy',
         'roleInfoFameProxy',
         'guildPuzzleProxy',
         'famousRankListProxy',
         'famousSeasonIntroProxy',
         'famousLvupIntroProxy',
         'famousSeasonAnnounceProxy',
         'schoolTransferConditionProxy',
         'schoolTransferEquipConfirmProxy',
         'schoolTransferEquipProxy',
         'schoolTransferHintProxy',
         'schoolTransferSelectProxy',
         'newRechargeProxy',
         'chooseRewardProxy',
         'qrCodeMultiGraphProxy',
         'qrCodeInstallAPPProxy',
         'tabAuctionProxy',
         'tabAuctionConsignProxy',
         'tabAuctionCrossServerProxy',
         'worldWarRobInfoProxy',
         'worldWarRobOverviewProxy',
         'worldWarRobRankProxy',
         'worldWarRobResultProxy',
         'itemSourceInforProxy',
         'roomEnlargeProxy',
         'characterSharePreviewProxy',
         'chickenFoodAppearanceProxy',
         'chickenFoodBalanceProxy',
         'chickenFoodMainProxy',
         'chickenFoodOtherProxy',
         'chickenFoodSubmitProxy',
         'chickenFoodRankProxy',
         'fubenSourceProxy',
         'pvpMasteryCatchUpProxy',
         'yaoPeiFeedCatchUpProxy',
         'chickenFoodGuideProxy',
         'chickenFoodShowProxy',
         'xiuYingExpGetProxy',
         'homeTermsStorageProxy',
         'tabAuctionCrossServerRegionProxy',
         'skillMacroOverviewProxy',
         'skillMacroCreateProxy',
         'skillMacroInputProxy',
         'worldWarLvChooseProxy',
         'wWRZaijuBloodProxy',
         'schemeSwitchProxy',
         'schemeResumeProxy',
         'itemPreviewSelectProxy',
         'disIndicatorProxy',
         'groupFollowHeaderCallProxy',
         'questionnaireProxy',
         'systemMessageProxy',
         'roleInformationQumoProxy',
         'battleFieldHistoryProxy',
         'roleInformationJunjieProxy',
         'famousRecordProxy',
         'famousRecordCommListProxy',
         'summonedWarSpriteMineProxy',
         'summonedWarSpriteGuardProxy',
         'summonedWarSpriteBiographyProxy',
         'activitySaleWeekActivationProxy',
         'backflowCatchExpProxy',
         'backflowPriviegeProxy',
         'backflowDiscountProxy',
         'playRecommActivationProxy',
         'playRecommStrongerProxy',
         'playRecommLvUpProxy',
         'rankingProxy',
         'tianyuMallProxy',
         'yunChuiShopProxy',
         'activitySaleGroupBuyProxy',
         'activitySaleGroupBuyConfirmProxy',
         'wingWorldStrategyProxy',
         'summonFriendShopV2Proxy',
         'summonFriendInviteV2Proxy',
         'summonFriendBackV2Proxy',
         'activitySaleLotteryProxy',
         'wingWorldOverViewProxy',
         'wingWorldArmyProxy',
         'activitySaleLotteryConfirmProxy',
         'summonedWarSpriteExplorePlanProxy',
         'yunChuiQuizzesProxy',
         'yunChuiQuizzesApplyProxy',
         'yunChuiQuizzesPushProxy',
         'summonedWarSpriteXiuLianProxy',
         'activitySaleTurnOverCardProxy',
         'crystalDefenceMainProxy',
         'crystalCleanseProgressProxy']
        self.escFunc = {}
        path = 'gui/UI.swf'
        self.uiExt = '.swf'
        if self.isUIPublished():
            path = 'gui/UI.gfx'
            self.uiExt = '.gfx'
        self.movie = Scaleform.MovieDef(path).createInstance()
        self.movie.backgroundAlpha = 0.0
        self.movie.scaleMode = 'NoScale'
        self.proxies = []
        self.dataProxies = []
        self.dataProxyDict = {}
        if not self.lazyInitProxy():
            map(self._importModule, self.proxyList)
            self._registerProxies()
        else:
            self._initStartProxies()
        self._setcallback()
        self.tempWeightDict = {}
        self.modelMap = {'sendFirstMouseLocation': self.onFirstSendMouseLocation,
         'sendMouseLocation': self.onSendMouseLocation,
         'onCloseWindow': self.onCloseWindow,
         'getSlotTooltip': self.onGetToolTip,
         'getItemTooltip': self.onGetItemTooltip,
         'getBuffDetail': self.onGetStateDetail,
         'notifySlotDragStart': self.onNotifySlotDragStart,
         'notifySlotDragEnd': self.onNotifySlotDragEnd,
         'notifySlotUse': self.onNotifySlotUse,
         'notifyStateRelease': self.onNotifyStateRelease,
         'hideTooltip': self.onHideTooltip,
         'notifySlotMouseDown': self.onNotifySlotMouseDown,
         'getTutorialMsg': self.onGetTutorialMsg,
         'clickClose': self.onClickClose,
         'handleLeftMouseUp': self.onHandleLeftMouseUp,
         'handleRightMouseUp': self.onHandleRightMouseUp,
         'canEscQuit': self.onCanEscQuit,
         'setModalState': self.onSetModalState,
         'clickScreen': self.onClickScreen,
         'isDragable': self.onIsDragable,
         'unDrag': self.onUnDrag,
         'hideMenu': self.onHideMenu,
         'clickMenuItem': self.onClickMenuItem,
         'getNextSlotTooltip': self.onGetNextSlotTooltip,
         'widgetLoadCompeleted': self.onWidgetLoadCompeleted,
         'getWidegetIndex': self.onGetWidegetIndex,
         'replace': regExpUtils.replace,
         'findAll': regExpUtils.findAll,
         'getPinYin': self.onGetPinYin,
         'getWidgetSavingPos': self.onGetWidgetSavingPos,
         'getWidgetSavingHidden': self.onGetWidgetSavingHidden,
         'getWidgetCanShow': self.onGetWidgetCanShow,
         'getWidgetCanF11': self.onGetWidgetCanF11,
         'saveWidgetHidden': self.onSaveWidgetHidden,
         'getWidgetDragAble': self.onGetWidgetDragable,
         'getEnableF11Hide': self.onGetEnableF11Hide,
         'saveAllWidgetPos': self.saveAllDragWidgetPos,
         'getLayoutDict': self.onGetLayoutDict,
         'afterCurve': self.onAfterCurve,
         'getNoCloseInRestore': self.onGetNoCloseInRestore,
         'getServerTime': self.onGetServerTime,
         'getSaveWidgetPosInfo': self.onGetSaveWidgetPosInfo,
         'getScreenDPI': self.onGetScreenDPI,
         'getScaleData': self.onGetScaleData,
         'setScaleData': self.onSetScaleData,
         'widgetAdded': self.onWidgetAdded,
         'widgetRemoved': self.onWidgetRemoved,
         'slotMouseOver': self.onSlotMouseOver,
         'slotMouseOut': self.onSlotMouseOut,
         'clickMarkTarget': self.onClickMarkTarget,
         'isInGroup': self.onIsInGroup,
         'getBonusDict': self.onGetBonusDict,
         'linkClik': self.onLinkClick,
         'saveWidgetPos': self.onSaveWidgetPos,
         'setCursor': self.onSetCursor,
         'clickItems': self.onClickItems,
         'getFaceSizes': self.onGetFaceSizes,
         'setEditFlag': self.onSetEditFlag,
         'gotoTrackPlace': self.onGotoTrackPlace,
         'getHelpData': self.onGetHelpData,
         'showHelpByKey': self.onShowHelpByKey,
         'widgetLoadError': self.onWidgetLoadError,
         'getItemTipByTipInfo': tipUtils.onGetItemTipByInfo,
         'getTipDataByType': tipUtils.onGetTipDataByType,
         'getMenuDataById': menuManager.onGetMenuById,
         'getItemDataById': self.onGetItemDataById,
         'getSkillDataById': self.onGetSkillDataById,
         'getJobDataById': self.onGetJobDataById,
         'loadRemoteImg': self.onLoadRemoteImg,
         'getDefaultAim': self.onGetDefaultAim,
         'getBonusTip': self.onGetBonusTip,
         'getMingPaiDataById': self.onGetMingPaiDataById,
         'openRedPacket': self.onOpenRedPacket,
         'getWWArmPostById': self.onGetWWArmPostById,
         'getItemSearchIconData': self.onGetItemSearchIconData,
         'changeItemSearch': self.onChangeItemSearch,
         'getWidgetInfos': self.onGetWidgetInfos,
         'topWidgetChanged': self.onTopWidgetChanged,
         'registerVocieItem': self.onRegisterVocieItem,
         'clickVoiceItem': self.onClickVoiceItem,
         'isCacheWid': self.onIsCacheWid,
         'getString': self.onGetString,
         'openItemSourcePanel': self.onOpenItemSourcePanel,
         'getGameConfig': self.onGetGameConfig,
         'getGroupIdentityType': self.onGetGroupIdentityType,
         'selectFriend': self.onSelectFriend,
         'getAllCallBackEvents': self.onGetAllCallBackEvents,
         'handleEvent': self.onHandleEvent,
         'clickSoundRecordItem': self.onClickSoundRecordItem,
         'soundRecordIsReviewed': self.onSoundRecordIsReviewed,
         'getRedPotVisible': redPotUtils.onGetRedPotVisible,
         'getRedPotInfo': redPotUtils.onGetRedPotInfo,
         'handleRedPot': redPotUtils.onHandleRedPot,
         'reportClientException': self.onReportClientException,
         'getRedPacketSplitStr': self.onGetRedPacketSplitStr,
         'getIconDataById': self.onGetIconDataById,
         'getSpriteIconPath': self.onGetSpriteIconPath}
        self.bInEdit = False
        self.capUpKeys = [keys.KEY_1,
         keys.KEY_2,
         keys.KEY_3,
         keys.KEY_4,
         keys.KEY_5,
         keys.KEY_6,
         keys.KEY_7,
         keys.KEY_8,
         keys.KEY_9,
         keys.KEY_0]
        self.mc = None
        self.localX = 0
        self.localY = 0
        self.inQTE = False
        self.QTEHideUI = False
        self.inDrag = False
        self.inDragCommonItem = False
        self.inDragStorageItem = False
        self.inDragFashionBagItem = False
        self.inDragMaterialBagItem = False
        self.inDragSpriteMaterialBagItem = False
        self.inDragRuneInvItem = False
        self.tutorInfo = None
        self.tuTipMsg = None
        self.uiSoundMap = {}
        self.uiCommonOpenCloseSoundMap = {}
        self.commonPlaySound = (4, 5)
        self.msgPlaySound = (32, 5)
        self.uiPopUpMap = {}
        self.expMap = {}
        self.cashMap = {}
        self.bindCashMap = {}
        self.mpMap = {}
        self.hpMap = {}
        self.isPlayingVoice = None
        gameglobal.rds.littlemap = littlemap.LittleMap()
        self._initUISound()
        self.enableUI = True
        self.oldX = self.oldY = self.Yaw = None
        self.dragInvPageSrc = None
        self.dragInvItemSrc = None
        self.dragGuildStoragePageSrc = None
        self.dragGuildStorageItemSrc = None
        self.dragFashionBagPageSrc = None
        self.dragFashionBagItemSrc = None
        self.dragStoragePageSrc = None
        self.dragStorageItemSrc = None
        self.dragCrossInvPageSrc = None
        self.dragCrossInvItemSrc = None
        self.dragMaterialBagPageSrc = None
        self.dragMaterialBagItemSrc = None
        self.dragRuneInvPageSrc = None
        self.dragRuneInvItemSrc = None
        self.QTECallbackId = None
        self.params = [0.1,
         0.3,
         0.3,
         0.55]
        self.posArr = {}
        self.inSchoolSwitch = False
        self.currentShishenMode = 0
        self.isStopGC = False
        self.showCursorAfterWidget = False
        self.widProxyDict = dict(((x[0], x[2]) for x in uiConst.UI_INFO))
        self.profile = uiProfile.UIProfile()
        self.bInput = False
        self.widgetLoadedTime = {}
        self.callbackHandler = 0
        self.lockHideAllUI = False
        self.asLogList = []
        self.lastFrameCount = 0
        if not BigWorld.isPublishedVersion() and ENALBE_AS_LOG_WARNING:
            self.modelMap['logValidateNow'] = self.onLogValidateNow
        self.dataModel = None
        self.isStartRecodShowList = False
        self.recordShowSet = set()
        self.isNewBloodLabelSupport = hasattr(BigWorld, 'isNewBroodLabel') and BigWorld.isNewBroodLabel()
        self.GUITextFactory = GUITextFactory()

    def startRecordShowList(self):
        self.isStartRecodShowList = True
        self.recordShowSet = set()

    def stopRecordShowList(self):
        self.isStartRecodShowList = False
        if self.recordShowSet:
            recodList = list(self.recordShowSet)
            recodList.sort(cmp=lambda a, b: cmp(uiConst.RECORD_WIDGET_SORT_LIST.index(a[0]), uiConst.RECORD_WIDGET_SORT_LIST.index(b[0])))
            self.recordShowSet.remove(recodList[0])
            self.loadWidget(*recodList[0])

    def isUIPublished(self):
        if not hasattr(self, 'isUIPublishedProp'):
            self.isUIPublishedProp = clientcom.isFileExist('gui/UI.gfx')
        return self.isUIPublishedProp

    def getUIExt(self):
        return self.uiExt

    def onClickItems(self, *args):
        binding = args[3][0].GetString()
        itemId = int(args[3][1].GetNumber())
        if ui.get_cursor_state() == ui.SIGNEQUIP_STATE:
            if len(binding.split('.')) != 2:
                return
            res_kind_str, _ = binding.split('.')
            if res_kind_str[:4] != 'bag_':
                BigWorld.player().showGameMsg(GMDD.data.EQUIP_SIGN_IN_BAG, ())
        elif ui.get_cursor_state() in (ui.IDENTIFY_ITEM_STATE, ui.IDENTIFY_MANUAL_EQUIP_STATE):
            if len(binding.split('.')) != 2:
                return
            res_kind_str, _ = binding.split('.')
            if res_kind_str[:4] != 'bag_':
                BigWorld.player().showGameMsg(GMDD.data.IDENTIFY_ITEM_IN_BAG, ())
        elif ui.get_cursor_state() == ui.CHANGE_BIND_STATE:
            if len(binding.split('.')) != 2:
                return
            res_kind_str, _ = binding.split('.')
            if res_kind_str[:4] != 'bag_':
                BigWorld.player().showGameMsg(GMDD.data.BAG_NOT_SUPPORT_CHANGE_BIND, ())
        elif ui.get_cursor_state() == ui.ITEM_SEARCH_STATE:
            if gameglobal.rds.configData.get('enableNewItemSearch', False):
                self.itemSourceInfor.openPanel()
            elif itemId:
                self.help.showByItemId(itemId)

    def onOpenItemSourcePanel(self, *args):
        self.itemSourceInfor.openPanel()

    def _importModule(self, fileName):
        cls = self._getClsName(fileName)
        try:
            module = __import__('guis.' + fileName, fromlist=[cls])
            globals()[cls] = getattr(module, cls)
        except:
            gamelog.debug('Can not find %s, Please commit it!' % fileName)

    def _getClsName(self, fileName):
        ff = list(fileName)
        ff[0] = ff[0].upper()
        ff = ''.join(ff)
        return ff

    def _callback(self, cmd, arg):
        if cmd == 'isShippingBuild':
            arg.SetMember('isShipping', Scaleform.GfxValue(self.isUIPublished()))
            arg.SetMember('isPublished', Scaleform.GfxValue(BigWorld.isPublishedVersion()))
        elif 'gameDataModelInit' in cmd:
            model, module = cmd.split('.')
            gamelog.debug('callback1', module)
            if module != cmd:
                getattr(self, module).initDataModel(arg, module)
        elif cmd == 'dataBindingInit':
            self._dataBindingInit(arg)
        elif cmd == 'CurrentEdit':
            self.bInEdit = True
            if BigWorld.enableNtIme() and gameglobal.rds.configData.get('enableCustomIme', False):
                x, y = self.getImeEditPos(arg)
                ime.setCompPos(x, y)
        elif cmd == 'EditFocusOut':
            self.bInEdit = False
            if BigWorld.enableNtIme() and gameglobal.rds.configData.get('enableCustomIme', False):
                gameglobal.rds.ui.ime.hideIme()
        elif 'Sound' in cmd:
            if gameglobal.rds.GameState != gametypes.GS_LOADING:
                sound, actionVal, soundId = cmd.split('.')
                gameglobal.rds.sound.playSound(int(soundId))
        elif cmd == 'initOK':
            self.uiObj = arg
            asObject.initAsObject(self.uiObj)
            gameglobal.rds.loginManager.firstPage()
        elif cmd == 'ASTrace':
            gamelog.debug('[ASLog:]', ui.unicode2gbk(arg.GetString()))
        else:
            gamelog.debug('jjh@uiAdapter._callback', cmd)

    def getImeEditPos(self, edit):
        pos = edit.Invoke('getCursorPosition')
        x = pos.GetElement(0).GetNumber()
        y = pos.GetElement(1).GetNumber()
        return (x, y)

    def handleKeyEvent(self, down, key, vk, mods):
        if gameglobal.rds.GameState == gametypes.GS_LOGIN:
            return False
        if self.bInEdit and key in self.capUpKeys:
            return True
        if self.inQTE:
            return True
        if hasattr(self, 'tdHeadGen') and self.tdHeadGen.headGenMode:
            return self.tdHeadGen.handleKeyEvent(down, key, vk, mods)
        if hasattr(self, 'playerPhotoGen') and self.playerPhotoGen.isShow():
            return self.playerPhotoGen.handleKeyEvent(down, key, vk, mods)
        if gameglobal.rds.ui.chickenFoodEating.handleInputKey(down, key, vk, mods):
            return True
        return False

    def _setcallback(self):
        self.movie.setExternalInterfaceCallback(self._callback)

    def onFirstSendMouseLocation(self, *arg):
        gameglobal.rds.loginScene.initYaw(arg[3][0].GetNumber())

    def onSendMouseLocation(self, *arg):
        self.localX = arg[3][0].GetNumber()
        self.localY = arg[3][1].GetNumber()
        gameglobal.rds.loginScene.mouseRotate(self.localX, self.localY)

    def getImportedModule(self, name, cls):
        try:
            return __import__(name, fromlist=[cls])
        except:
            pass

    def __getattr__(self, item):
        if self.__dict__.has_key(item):
            return object.__getattribute__(self, item)
        else:
            proxy = item + 'Proxy'
            cls = self._getClsName(proxy)
            module = None
            if not module:
                module = self.getImportedModule('guis.' + proxy, cls)
            if not module:
                module = self.getImportedModule('debug.' + proxy, cls)
            if module:
                globals()[cls] = getattr(module, cls)
                setattr(self, item, globals()[cls](self))
                if proxy not in self.proxyList:
                    self.proxyList.append(proxy)
            return object.__getattribute__(self, item)

    def _initStartProxies(self):
        self.main = self
        self.proxyList = uiConst.GAME_START_INIT_PROXIES
        for name in self.proxyList:
            try:
                getattr(self, name[:-5])
            except Exception as e:
                gamelog.debug('[UI] Can not find %s, Please check commit!' % name, e)

    def _registerProxies(self):
        self.main = self
        for proxy in self.proxyList:
            try:
                cls = self._getClsName(proxy)
                setattr(self, proxy[:-5], globals()[cls](self))
            except Exception as e:
                gamelog.debug('[UI] Can not find %s, Please check commit!' % cls, e)

        self.storyEditDebug = storyEditDebugProxy.StoryEditDebugProxy(self)
        if not BigWorld.isPublishedVersion():
            self.actionDebug = actionDebugProxy.ActionDebugProxy(self)
            self.particleDebug = particleDebugProxy.ParticleDebugProxy(self)
            self.hardPointDebug = hardPointDebugProxy.HardPointDebugProxy(self)
            self.roleDebug = roleDebugProxy.RoleDebugProxy(self)
            self.tdHeadGen = tdHeadGenProxy.TdHeadGenProxy(self)
            self.bodyChange = bodyChangeProxy.BodyChangeProxy(self)
            self.equipFashionChange = equipFashionChangeProxy.EquipFashionChangeProxy(self)
            self.playerPhotoGen = playerPhotoGenProxy.PlayerPhotoGenProxy(self)
            self.dyeTest = dyeTestProxy.DyeTestProxy(self)
            self.pointGen = pointGenProxy.PointGenProxy(self)
            self.reloadData = reloadDataProxy.ReloadDataProxy(self)
            self.monsterAction = monsterActionProxy.MonsterActionProxy(self)
            self.npcAction = npcActionProxy.NpcActionProxy(self)
            self.fbGenMonster = fbGenMonsterProxy.FbGenMonsterProxy(self)
            self.actionFxEditor = actionFxEditorProxy.ActionFxEditorProxy(self)
            self.walkLineEdit = walkLineEditProxy.WalkLineEditProxy(self)
        for info in uiConst.UI_INFO:
            try:
                proxyName = '%sProxy' % info[2]
                if not hasattr(self, info[2]):
                    self._importModule(proxyName)
                    cls = self._getClsName(proxyName)
                    setattr(self, info[2], globals()[cls](self))
                    if proxyName not in self.proxyList:
                        self.proxyList.append(proxyName)
            except Exception as e:
                gamelog.debug('[UI] Can not find %s, Please check commit!' % cls, e)

    def reRegisterProxies(self):
        for proxy in self.proxyList:
            try:
                cls = self._getClsName(proxy)
                proxyName = proxy[:-5]
                if not hasattr(self, proxyName):
                    setattr(self, proxyName, globals()[cls](self))
            except Exception as e:
                gamelog.debug('[UI] Can not find %s, Please check commit!' % cls, e)

    def initDataModel(self, dataModel, whichModel):
        self.dataModel = dataModel
        for key in self.modelMap.keys():
            dataModel.SetMember(key, self.movie.CreateFunction(self.modelMap[key]))

    def _dataBindingInit(self, dataBinding):
        dataBinding.SetMember('createBindingImpl', self.movie.CreateFunction(self._onCreateBinding))
        dataBinding.SetMember('deleteBindingImpl', self.movie.CreateFunction(self._onDeleteBinding))

    def _onCreateBinding(self, *arg):
        key = arg[3][0].GetString()
        dataProxy = self.getDataProxy(key)
        if dataProxy:
            dataProxy.onCreateBinding(*arg)

    def _onDeleteBinding(self, *arg):
        key = arg[3][0].GetString()
        dataProxy = self.getDataProxy(key)
        if dataProxy:
            dataProxy.onDeleteBinding(*arg)

    def getDataProxy(self, key):
        proxy = self.dataProxyDict.get(key, None)
        if proxy:
            return proxy
        else:
            for dataProxy in self.dataProxies:
                if dataProxy.isType(key):
                    self.dataProxyDict[key] = dataProxy
                    return dataProxy

            return

    def onGetNextSlotTooltip(self, *arg):
        gamelog.debug('slottooltip', arg[3][0].GetString())
        tip = self.skill.onGetNextToolTip(*arg)
        return tip

    def onGetToolTip(self, *arg):
        if self.inDrag:
            return Scaleform.GfxValue('')
        else:
            gameglobal.rds.ui.assign.selectPos = None
            key = arg[3][0].GetString()
            tip = Scaleform.GfxValue(gbk2unicode(''))
            if key.find('actionbar') != -1:
                tip = self.actionbar.onGetToolTip(*arg)
            elif key.find('airbar') != -1:
                tip = self.airbar.onGetToolTip(*arg)
            elif key.find('FashionBag') != -1:
                tip = self.fashionBag.onGetToolTip(*arg)
            elif key.find('bag') != -1:
                tip = self.inventory.onGetToolTip(*arg)
                self.inventory.onDeleteNewIcon(*arg)
            elif key.find('booth') != -1:
                tip = self.booth.onGetToolTip(*arg)
            elif key.find('achievementScore') != -1:
                tip = self.achievementScore.onGetToolTip(*arg)
            elif key.find('trade') != -1:
                tip = self.trade.onGetToolTip(*arg)
            elif key.find('shop') != -1:
                tip = self.shop.onGetToolTip(*arg)
            elif key.find('pickUp') != -1:
                tip = self.pickUp.onGetToolTip(*arg)
            elif key.find('worldWar') != -1:
                tip = self.worldWar.onGetTooltip(*arg)
            elif key.find('wingWorld') != -1:
                tip = self.wingWorldArmySkill.onGetTooltip(*arg)
            elif key.find('clanWarSkill') != -1:
                tip = self.clanWarSkill.onGetTooltip(*arg)
            elif key.find('skillMacro') != -1:
                tip = self.skillMacroOverview.onGetToolTip(*arg)
            elif key.find('skill') != -1:
                tip = self.skill.onGetToolTip(*arg)
            elif key.find('lvUpGuide') != -1:
                tip = self.lvUpGuide.onGetToolTip(*arg)
            elif key.find('tarrole') != -1:
                tip = self.targetRoleInfo.onGetToolTip(*arg)
            elif key.find('assign') != -1:
                tip = self.assign.onGetToolTip(*arg)
            elif key.find('sack') != -1:
                tip = self.sack.onGetToolTip(*arg)
            elif key.find('fbLogin') != -1:
                tip = self.fubenLogin.onGetToolTip(*arg)
            elif key.find('payBag') != -1:
                tip = self.payItem.onGetToolTip(*arg)
            elif key.find('zaiju') != -1:
                tip = self.zaiju.onGetToolTip(*arg)
            elif key.find('zaiJuV2') != -1:
                tip = self.zaijuV2.onGetToolTip(*arg)
            elif key.find('compositeShop') != -1:
                tip = self.compositeShop.onGetToolTip(*arg)
            elif key.find('bianshi') != -1:
                tip = Scaleform.GfxValue(gbk2unicode(''))
            elif key.find('fashion') != -1:
                tip = self.roleInfo.onGetToolTip(*arg)
            elif key.find('storage') != -1:
                tip = self.storage.onGetToolTip(*arg)
            elif key.find('fishing') != -1:
                tip = self.fishing.onGetToolTip(*arg)
            elif key.find('searchList') != -1:
                tip = self.booth.onGetSearchListToolTip(*arg)
            elif key.find('bRecord') != -1:
                tip = self.booth.onGetRecordToolTip(*arg)
            elif key.find('runeView') != -1:
                tip = self.runeView.onGetToolTip(*arg)
            elif key.find('lvUpAward') != -1:
                tip = self.levelUp.onGetToolTip(*arg)
            elif key.find('trainingArea') != -1:
                tip = self.trainingArea.onGetToolTip(*arg)
            elif key.find('equipPush') != -1:
                tip = self.equipPush.onGetToolTip(*arg)
            elif key.find('activityPush') != -1:
                tip = self.activityPush.onGetToolTip(*arg)
            elif key.find('help') != -1:
                tip = self.help.onGetToolTip(*arg)
            elif key.find('mail') != -1:
                tip = self.mail.onGetToolTip(*arg)
            elif key.find('fishGame') != -1:
                tip = self.fishingGame.onGetToolTip(*arg)
            elif key.find('consign') != -1:
                tip = self.consign.onGetToolTip(*arg)
            elif key.find('tabAuctionConsign') != -1:
                tip = self.tabAuctionConsign.onGetToolTip(*arg)
            elif key.find('tabAuctionCrossServer') != -1:
                tip = self.tabAuctionCrossServer.onGetToolTip(*arg)
            elif key.find('trainingAward') != -1:
                tip = self.trainingAreaAward.onGetToolTip(*arg)
            elif key.find('explore') != -1:
                tip = self.explore.onGetToolTip(*arg)
            elif key.find('equipFeed') != -1:
                tip = self.equipFeed.onGetToolTip(*arg)
            elif key.find('runeLvUp') != -1:
                tip = self.runeLvUp.onGetToolTip(*arg)
            elif key.find('equipEResult') != -1:
                tip = self.equipEnhanceResult.onGetToolTip(*arg)
            elif key.find('equipCopy') != -1:
                tip = self.equipCopy.onGetToolTip(*arg)
            elif key.find('equipEnhance') != -1:
                tip = self.equipEnhance.onGetToolTip(*arg)
            elif key.find('fashionPropTransfer') != -1:
                tip = self.fashionPropTransfer.onGetToolTip(*arg)
            elif key.find('runeSlotXiLian') != -1:
                tip = self.roleInfo.onGetRuneSlotXiLianToolTip(*arg)
            elif key.find('runeChongXi') != -1:
                tip = self.runeChongXi.onGetToolTip(*arg)
            elif key.find('runeForging') != -1:
                tip = self.runeForging.onGetToolTip(*arg)
            elif key.find('runeReforging') != -1:
                tip = self.runeReforging.onGetToolTip(*arg)
            elif key.find('battlefield') != -1:
                tip = self.battleFieldShop.onGetToolTip(*arg)
            elif key.find('guildGrowth') != -1:
                tip = self.guildGrowth.onGetToolTip(*arg)
            elif key.find('guildResident') != -1:
                tip = self.guildResident.onGetToolTip(*arg)
            elif key.find('dyePlane') != -1:
                tip = self.dyePlane.onGetToolTip(*arg)
            elif key.find('huizhangRepair') != -1:
                tip = self.huiZhangRepair.onGetToolTip(*arg)
            elif key.find('wingAndMount') != -1:
                tip = self.wingAndMount.onGetToolTip(*arg)
            elif key.find('WAMUpGrade') != -1:
                tip = self.wingAndMountUpgrade.onGetToolTip(*arg)
            elif key.find('dyeReset') != -1:
                tip = self.dyeReset.onGetToolTip(*arg)
            elif key.find('emote') != -1:
                tip = self.emote.onGetToolTip(*arg)
            elif key.find('yaoPeiMix') != -1:
                tip = self.yaoPeiMix.onGetToolTip(*arg)
            elif key.find('yaoPeiFeed') != -1:
                tip = self.yaoPeiFeed.onGetToolTip(*arg)
            elif key.find('yaoPeiLvUp') != -1:
                tip = self.yaoPeiLvUp.onGetToolTip(*arg)
            elif key.find('yaoPeiTransfer') != -1:
                tip = self.yaoPeiTransfer.onGetToolTip(*arg)
            elif key.find('yaoPeiReforge') != -1:
                tip = self.yaoPeiReforge.onGetToolTip(*arg)
            elif key.find('yaoPeiReforgeResult') != -1:
                tip = self.yaoPeiReforgeResult.onGetToolTip(*arg)
            elif key.find('crossBag') != -1:
                tip = self.crossServerBag.onGetToolTip(*arg)
            elif key.find('wish') != -1:
                tip = self.wishMade.onGetToolTip(*arg)
            elif key.find('meterial') != -1:
                tip = self.meterialBag.onGetToolTip(*arg)
            elif key.find('itemPushUse') != -1:
                tip = self.itemPushUse.onGetToolTip(*arg)
            elif key.find('modelrole') != -1:
                tip = self.modelRoleInfo.onGetToolTip(*arg)
            elif key.find('hieroRole') != -1:
                tip = self.roleInformationHierogram.onGetToolTip(*arg)
            elif key.find('famousSkill') != -1:
                tip = self.roleInformationJunjie.onGetToolTip(*arg)
            elif key.find('spriteMaterial') != -1:
                tip = self.spriteMaterialBag.onGetToolTip(*arg)
            elif key.find('runeInv') != -1:
                tip = self.runeInv.onGetToolTip(*arg)
            return tip

    def onGetItemTooltip(self, *arg):
        try:
            itemId = int(arg[3][0].GetNumber())
            srcType = arg[3][1].GetString()
        except:
            return Scaleform.GfxValue('')

        if srcType == 'auction':
            it = self.assign.getAuctionItemById(itemId)
        elif srcType == 'roleInfoLifeSkillFish':
            item = Item(itemId)
            part = item.whereEquipFishing()
            it = BigWorld.player().fishingEquip[part]
        elif srcType == 'roleInfoLifeSkillExplore':
            item = Item(itemId)
            part = item.whereEquipExplore()
            it = BigWorld.player().exploreEquip[part]
        elif srcType == 'roleInfoLifeSkill':
            subType, part, isSpecial = uiUtils.whereLifeEquip(itemId)
            p = BigWorld.player()
            if not isSpecial:
                it = p.lifeEquipment.get(subType, part)
            else:
                if subType == gametypes.LIFE_SKILL_TYPE_FISHING:
                    equipInv = p.fishingEquip
                elif subType == gametypes.LIFE_SKILL_TYPE_EXPLORE:
                    equipInv = p.exploreEquip
                if equipInv:
                    it = equipInv[part]
            if it is None:
                it = Item(itemId)
        else:
            if srcType == 'equipCopy':
                return gameglobal.rds.ui.equipCopy.getTargetToolTip()
            if srcType == 'equipMixNew_mainMaterial':
                return gameglobal.rds.ui.equipMixNew.getMainMaterialToolTip(itemId)
            if srcType == 'equipMixNew_material':
                return gameglobal.rds.ui.equipMixNew.getMaterialToolTip(itemId)
            if srcType == 'equipMixNew_target':
                return gameglobal.rds.ui.equipMixNew.getTargetToolTip()
            if srcType == 'itemResume':
                it = gameglobal.rds.ui.itemResume.resumeItem
            else:
                if srcType == 'equipFuncTgt_mix':
                    return gameglobal.rds.ui.equipMix.getTargetToolTip()
                if srcType == 'equipFuncSrc':
                    binding = arg[3][2].GetString()
                    if binding and binding != 'equipLvUp':
                        startPos = binding.find('_')
                        endPos = binding.find('_', startPos + 1)
                        page = int(binding[startPos + 1:endPos])
                        pos = int(binding[endPos + 1:])
                        it = BigWorld.player().inv.getQuickVal(page, pos)
                        return gameglobal.rds.ui.inventory.GfxToolTip(it)
                    else:
                        return tipUtils.getItemTipById(itemId)
                else:
                    if srcType == 'mall':
                        return tipUtils.getItemTipById(itemId, const.ITEM_IN_MALL)
                    if srcType == 'mallVip':
                        return gameglobal.rds.ui.tianyuMall.formatVipTips(itemId)
                    if srcType == 'characterDetailAdjust':
                        it = Item(itemId)
                        return gameglobal.rds.ui.inventory.GfxToolTip(it, const.ITEM_IN_NONE)
                    if srcType == 'gemUnclok':
                        equipData = gameglobal.rds.ui.equipmentSlot
                        if equipData.item != None:
                            it = BigWorld.player().inv.getQuickVal(equipData.srcPos[0], equipData.srcPos[1])
                            return gameglobal.rds.ui.inventory.GfxToolTip(it)
                    else:
                        if srcType == 'equipGem':
                            key = arg[3][2].GetString()
                            return gameglobal.rds.ui.equipGem.onGetToolTip(key)
                        if 'equipChangeInlayV2' in srcType:
                            return gameglobal.rds.ui.equipChangeInlayV2.onGetToolTip(srcType)
                        if 'equipChangeInlay' in srcType:
                            return gameglobal.rds.ui.equipChangeInlay.onGetToolTip(srcType)
                        if 'equipChangeRune' in srcType:
                            return gameglobal.rds.ui.equipChangeRuneFeed.onGetToolTip(srcType)
                        if 'equipChangeUnlock' in srcType:
                            return gameglobal.rds.ui.equipChangeUnlock.onGetToolTip(srcType)
                        if 'activitySaleMallBox' == srcType:
                            return gameglobal.rds.ui.activitySaleMallBox.onGetToolTip(itemId)
                        if srcType == 'redemption':
                            key = arg[3][2].GetString()
                            return gameglobal.rds.ui.equipRedemption.onGetToolTip(key)
                        if srcType == 'purchaseShop':
                            it = Item(itemId)
                            return gameglobal.rds.ui.inventory.GfxToolTip(it, const.ITEM_IN_NONE)
                        if srcType == 'fameShop':
                            return tipUtils.getItemTipById(itemId, const.ITEM_IN_FAME_SHOP)
                        if srcType == 'valuableTrade':
                            key = arg[3][2].GetString()
                            return gameglobal.rds.ui.valuableTrade.onGetToolTip(key)
                        if srcType == 'FashionPropTransfer0' or srcType == 'FashionPropTransfer1':
                            return gameglobal.rds.ui.fashionPropTransfer.onGetToolTip(srcType, itemId)
                        if srcType == 'mail':
                            key = arg[3][2].GetString()
                            return gameglobal.rds.ui.mail.getToolTip(key)
                        if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
                            return tipUtils.getItemTipById(itemId, const.ITEM_IN_AVATAR_WING)
                        if srcType == 'unBindItem':
                            return gameglobal.rds.ui.inventory.GfxToolTip(gameglobal.rds.ui.unBindItem.item)
                        if srcType == 'hieroEquip':
                            it = BigWorld.player().hierogramDict.get('hieroEquip', Item(itemId))
                        elif srcType == 'bindFirstInInv':
                            it = Item(itemId)
                            if hasattr(BigWorld.player(), 'inv'):
                                result = BigWorld.player().inv.countItemChild(it.getParentId())
                            else:
                                result = [0]
                            if result[0] > 0:
                                toolTipItem = Item(result[1][0])
                                return gameglobal.rds.ui.inventory.GfxToolTip(toolTipItem)
                            else:
                                return tipUtils.getItemTipById(itemId)
                        else:
                            if srcType.find('modelrole') != -1:
                                part = int(srcType[9:])
                                return self.modelRoleInfo.onGetItemTip(part)
                            if srcType.find('emote') != -1:
                                return GfxValue(gbk2unicode(self.emote.getTip(itemId)))
                            if srcType.find('otherSkill') != -1:
                                return self.skill.getOtherSkillTip(itemId)
                            if srcType.find('spriteMaterialBag') != -1:
                                page = int(srcType.split('/')[1])
                                pos = int(srcType.split('/')[2])
                                return tipUtils.getItemTipByPagePos(page, pos, const.ITEM_IN_SPRITE_MATERIAL_BAG)
                            if srcType.find('achevment') != -1:
                                return tipUtils.getItemTipById(itemId, const.ITEM_IN_ACHEVEMENT)
                            if srcType.find('guibaoge') != -1:
                                return tipUtils.getItemTipById(itemId, const.ITEM_IN_GUIBAOGE)
                            if srcType.find('templateRole') != -1:
                                return self.balanceArenaPreview.getItemTipByIndex(int(srcType[12:]))
                            if srcType.find('templateUp') != -1:
                                return self.balanceTemplateUpload.getItemTipByIndex(int(srcType[10:]))
                            if srcType.find('fashion') != -1:
                                return self.myCloth.getItemTipInfoByPart(int(srcType[7:]))
                            if srcType.find('wardrobe') != -1:
                                return self.wardrobe.getItemTipInfoByUUID(srcType[8:], itemId)
                            if srcType == 'manuqlEquipLvUp':
                                return self.manualEquipLvUp.onGetToolTip()
                            return tipUtils.getItemTipById(itemId)
        return gameglobal.rds.ui.inventory.GfxToolTip(it)

    def onNotifySlotDragStart(self, *arg):
        self.inDrag = True
        p = BigWorld.player()
        if p.spellingType in [action.S_SPELLCHARGE]:
            cellCmd.cancelSkill()
            p.stopSpell(False)
        gameglobal.rds.bar = None
        gameglobal.rds.slotId = None
        p.circleEffect.cancel()
        srcId = arg[3][0].GetString()
        if not self.playDragItemSound(srcId):
            gameglobal.rds.sound.playSound(15)
        proxySrc = self.getDragProxy(srcId)
        if not proxySrc:
            return
        else:
            nPageSrc, nItemSrc = self.getDragSlotID(proxySrc, srcId)
            name = uiDrag.getDargStartMethod(proxySrc.type)
            if name:
                func = getattr(uiDrag, name, None)
                if func != None:
                    func(nPageSrc, nItemSrc)
            return

    def getTopWidgetId(self):
        result = self.uiObj.Invoke('getTopWidget', ())
        if result.GetElement(0) and result.GetElement(1):
            widgetId = result.GetElement(0).GetNumber()
            mWidgetId = result.GetElement(1).GetNumber()
            return (int(widgetId), int(mWidgetId))
        else:
            return (0, 0)

    def onNotifySlotDragEnd(self, *arg):
        if gameglobal.rds.ui.actionbar.isItemBarInEdit():
            gameglobal.rds.ui.actionbar.setAllItemSlotVisible(True)
            gameglobal.rds.ui.actionbar.validateSlotVisible()
        else:
            gameglobal.rds.ui.actionbar.validateSlotVisible()
        self.inDrag = False
        self.inDragCommonItem = False
        self.inDragStorageItem = False
        self.inDragFashionBagItem = False
        self.inDragMaterialBagItem = False
        self.inDragSpriteMaterialBagItem = False
        self.inDragRuneInvItem = False
        srcId = arg[3][0].GetString()
        destId = arg[3][1].GetString()
        p = BigWorld.player()
        proxySrc = self.getDragProxy(srcId)
        proxyDest = self.getDragProxy(destId)
        if proxySrc != None:
            nPageSrc, nItemSrc = self.getDragSlotID(proxySrc, srcId)
        else:
            return
        if nPageSrc == None or nItemSrc == None:
            return
        else:
            gameglobal.rds.sound.playSound(14)
            if proxySrc.type == 'skillPanel':
                if nPageSrc == 1 or nPageSrc == 2:
                    gameglobal.rds.ui.actionbar.setSpecialSlotsShine(False)
                    gameglobal.rds.ui.skill.setSpecialSlotsShine(False)
                    gameglobal.rds.ui.actionbar.setNormalSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                    gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                    gameglobal.rds.ui.airbar.setAirSlotsState(uiConst.SKILL_ICON_STAT_USEABLE)
                elif nPageSrc in (uiConst.SKILL_PANEL_COMMON,
                 uiConst.SKILL_PANEL_OTHER,
                 uiConst.SKILL_PANEL_LIFE,
                 uiConst.SKILL_PANEL_EXPLORE,
                 uiConst.SKILL_PANEL_GUILD,
                 uiConst.SKILL_PANEL_SOCIAL,
                 uiConst.SKILL_PANEL_INTIMACY,
                 uiConst.SKILL_PANEL_PUBG):
                    gameglobal.rds.ui.actionbar.setNormalSlotsShine(False)
                    gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                    gameglobal.rds.ui.airbar.setAirSlotsState(uiConst.SKILL_ICON_STAT_USEABLE)
                elif nPageSrc == uiConst.SKILL_PANEL_AIR_ORIG:
                    gameglobal.rds.ui.actionbar.setNormalSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                    gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                    gameglobal.rds.ui.airbar.setAirSlotsShine(False)
                gameglobal.rds.ui.actionbar.initAllSkillStat()
            elif proxySrc.type == 'skillPush':
                if nPageSrc == uiConst.SKILL_PUSH_NORMAL:
                    gameglobal.rds.ui.actionbar.setNormalSlotsShine(False)
                    gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                elif nPageSrc == uiConst.SKILL_PUSH_SPECIAL:
                    gameglobal.rds.ui.actionbar.setSpecialSlotsShine(False)
                    gameglobal.rds.ui.actionbar.setNormalSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
            elif proxySrc.type in ('bagslot', 'emote', 'lifeSkill', 'skillMacro', 'crossBagSlot'):
                gameglobal.rds.ui.actionbar.setNormalSlotsShine(False)
                gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                gameglobal.rds.ui.actionbar.setAllSlotAlpha(uiConst.SKILL_ICON_STAT_USEABLE)
            elif proxySrc.type == 'actionbar':
                if nPageSrc == uiConst.SKILL_ACTION_BAR:
                    gameglobal.rds.ui.actionbar.mc.Invoke('setDraging', GfxValue(False))
                elif nPageSrc == uiConst.ITEM_ACTION_BAR:
                    if gameglobal.rds.ui.actionbar.itemMc[0] != None:
                        gameglobal.rds.ui.actionbar.itemMc[0].Invoke('setDraging', GfxValue(False))
                elif nPageSrc == uiConst.ITEM_ACTION_BAR2:
                    if gameglobal.rds.ui.actionbar.itemMc[1] != None:
                        gameglobal.rds.ui.actionbar.itemMc[1].Invoke('setDraging', GfxValue(False))
                if nPageSrc in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
                    if nPageSrc == uiConst.SKILL_ACTION_BAR and nItemSrc < uiConst.WUSHUANG_SKILL_START_POS_LEFT or nPageSrc in (uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
                        gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                        gameglobal.rds.ui.actionbar.setNormalSlotsShine(False)
                        gameglobal.rds.ui.airbar.setAirSlotsState(uiConst.SKILL_ICON_STAT_USEABLE)
                    else:
                        gameglobal.rds.ui.actionbar.setSpecialSlotsShine(False)
                        gameglobal.rds.ui.actionbar.setNormalSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                elif nPageSrc == uiConst.EQUIP_ACTION_BAR:
                    gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                    gameglobal.rds.ui.actionbar.setNormalSlotsShine(False)
                gameglobal.rds.ui.actionbar.initAllSkillStat()
                if nPageSrc in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2) and proxySrc.isLock:
                    p.showGameMsg(GMDD.data.ACTIONBAR_LOCKED, ())
                    return
            else:
                if proxySrc.type == 'tarroleslot':
                    return
                if proxySrc.type == 'airbar':
                    gameglobal.rds.ui.actionbar.setNormalSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                    gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                    gameglobal.rds.ui.airbar.setAirSlotsShine(False)
                    if proxySrc.isLock:
                        p.showGameMsg(GMDD.data.ACTIONBAR_LOCKED, ())
                        return
                elif proxySrc.type == 'storage':
                    if nPageSrc != const.STORAGE_PAGE_BAG:
                        nPageSrc = self.dragStoragePageSrc
                    if destId == 'InMc' and p.storage.getQuickVal(nPageSrc, nItemSrc):
                        gameglobal.rds.ui.storage.addItem(p.storage.getQuickVal(nPageSrc, nItemSrc), nPageSrc, nItemSrc)
                        return
                elif proxySrc.type == 'guildStorage':
                    nPageSrc = self.dragGuildStoragePageSrc
                    nItemSrc = self.dragGuildStorageItemSrc
                elif proxySrc.type == 'FashionBag':
                    nPageSrc = self.dragFashionBagPageSrc
                    nItemSrc = self.dragFashionBagItemSrc
                    self.sItem = p.fashionBag.getQuickVal(nPageSrc, nItemSrc)
                elif proxySrc.type == 'meterial':
                    nPageSrc = self.dragMaterialBagPageSrc
                    nItemSrc = self.dragMaterialBagItemSrc
                    self.sItem = p.materialBag.getQuickVal(nPageSrc, nItemSrc)
                elif proxySrc.type == 'spriteMaterial':
                    nPageSrc = gameglobal.rds.ui.dragSpriteMaterialBagPageSrc
                    nItemSrc = gameglobal.rds.ui.dragSpriteMaterialBagItemSrc
                    self.sItem = p.spriteMaterialBag.getQuickVal(nPageSrc, nItemSrc)
                elif proxySrc.type == 'runeInv':
                    nPageSrc = self.dragRuneInvPageSrc
                    nItemSrc = self.dragRuneInvItemSrc
            if proxySrc.type == 'bagslot':
                if gameglobal.rds.ui.inventory.dropMBIds:
                    return
                if gameglobal.rds.ui.inventory.page != uiConst.BAG_PAGE_QUEST:
                    nPageSrc = self.dragInvPageSrc
                if nPageSrc == None:
                    return
                if nPageSrc == uiConst.BAG_PAGE_QUEST:
                    if proxyDest and proxyDest.type in ('mail', 'consign', 'guildDonate', 'tabAuctionConsign', 'tabAuctionCrossServer'):
                        p.showGameMsg(GMDD.data.ITEM_TRADE_NOTRADE, ())
                    return
                self.sItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
                if self.sItem and (nPageSrc, nItemSrc) in gameglobal.rds.ui.inventory.newItemSequence:
                    gameglobal.rds.ui.inventory.newItemSequence.remove((nPageSrc, nItemSrc))
                    gameglobal.rds.ui.inventory.setNewIconVisible(nItemSrc, False)
                if destId == 'InMc':
                    gameglobal.rds.ui.inventory.addItem(self.sItem, nPageSrc, nItemSrc)
                    return
            if proxySrc.type == 'crossBagSlot':
                nPageSrc = self.dragCrossInvPageSrc
                nItemSrc = self.dragCrossInvItemSrc
                self.sItem = p.crossInv.getQuickVal(nPageSrc, nItemSrc)
                if destId == 'InMc':
                    return
            if proxySrc.type == 'skillMacro':
                gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
                gameglobal.rds.ui.actionbar.setNormalSlotsShine(False)
                gameglobal.rds.ui.airbar.setAirSlotsState(uiConst.SKILL_ICON_STAT_USEABLE)
                if destId == 'InMc':
                    return
            if arg[3][1].IsNull() == False and destId != 'InMc':
                if proxyDest is None:
                    return
                nPageDes, nItemDes = self.getDragSlotID(proxyDest, destId)
                if proxyDest.type == 'bagslot':
                    if gameglobal.rds.ui.inventory.dropMBIds:
                        return
                    if nPageDes == uiConst.BAG_PAGE_QUEST:
                        return
                    dItem = p.inv.getQuickVal(nPageDes, nItemDes)
                    if dItem and (nPageDes, nItemDes) in gameglobal.rds.ui.inventory.newItemSequence:
                        gameglobal.rds.ui.inventory.newItemSequence.remove((nPageDes, nItemDes))
                        gameglobal.rds.ui.inventory.setNewIconVisible(nItemDes, False)
                if proxyDest.type == 'tarroleslot':
                    return
                if destId == srcId:
                    if nPageSrc == nPageDes:
                        return
                if proxyDest.type == 'actionbar':
                    if nPageDes == uiConst.ITEM_ACTION_BAR:
                        p.operation['commonSetting'][11] = 1
                        gameglobal.rds.ui.actionbar.setItemMcVisible(0, 1)
                        p.sendOperation()
                    elif nPageDes == uiConst.ITEM_ACTION_BAR2:
                        gameglobal.rds.ui.actionbar.setItemMcVisible(1, 1)
                        p.operation['commonSetting'][20] = 1
                        p.sendOperation()
                name = uiDrag.getDargEndMethod(proxySrc.type, proxyDest.type)
                if name:
                    func = getattr(uiDrag, name, None)
                    if func != None:
                        func(nPageSrc, nItemSrc, nPageDes, nItemDes)
            else:
                name = uiDrag.getDargEndMethod(proxySrc.type, None)
                if name:
                    func = getattr(uiDrag, name, None)
                    if func != None:
                        func(nPageSrc, nItemSrc)
            return

    def onNotifySlotUse(self, *arg):
        key = arg[3][0].GetString()
        proxy = self.getDataProxy(key)
        gamelog.debug('ypc@ uiAdapter onNotifySlotUse ', key, proxy)
        if proxy:
            ret = proxy.onNotifySlotUse(*arg)
            if ret:
                return GfxValue(ret)

    def onNotifySlotMouseDown(self, *arg):
        key = arg[3][0].GetString()
        proxy = self.getDataProxy(key)
        if proxy:
            proxy.onNotifySlotMouseDown(*arg)

    def _genarateWidgetData(self, widgetType, widgetArg, msg):
        self.tuTipMsg = msg
        self.tutorInfo = self.movie.CreateObject()
        self.tutorInfo.SetMember('type', Scaleform.GfxValue(widgetType))
        self.tutorInfo.SetMember('widgetId', Scaleform.GfxValue(int(widgetArg[0])))
        if int(widgetArg[0]) == uiConst.WIDGET_CHAT_TO_FRIEND:
            topMed = self.chatToFriend.getTopMediator()
            if topMed:
                widgetId = int(ASObject(topMed).getMultiID())
                self.tutorInfo.SetMember('widgetId', Scaleform.GfxValue(widgetId))
        self.tutorInfo.SetMember('posX', Scaleform.GfxValue(widgetArg[1][0]))
        self.tutorInfo.SetMember('posY', Scaleform.GfxValue(widgetArg[1][1]))
        self.tutorInfo.SetMember('iconType', Scaleform.GfxValue(widgetArg[5]))
        self.tutorInfo.SetMember('arrowDir', Scaleform.GfxValue(widgetArg[2]))
        self.tutorInfo.SetMember('effectSize', Scaleform.GfxValue(widgetArg[3]))
        self.tutorInfo.SetMember('depth', Scaleform.GfxValue(widgetArg[7]))
        self.tutorInfo.SetMember('relativePos', Scaleform.GfxValue(widgetArg[8]))

    def _genaratePicWidgetData(self, widgetType, widgetArg, msg):
        self.tuTipMsg = msg
        self.tutorInfo = self.movie.CreateObject()
        self.tutorInfo.SetMember('type', Scaleform.GfxValue(widgetType))
        self.tutorInfo.SetMember('widgetId', Scaleform.GfxValue(int(widgetArg[0])))
        self.tutorInfo.SetMember('posX', Scaleform.GfxValue(widgetArg[1][0]))
        self.tutorInfo.SetMember('posY', Scaleform.GfxValue(widgetArg[1][1]))
        self.tutorInfo.SetMember('iconPath', Scaleform.GfxValue('tutorPic/%d.dds' % widgetArg[2]))
        title = GMD.data.get(widgetArg[3], {}).get('text', '')
        self.tutorInfo.SetMember('title', Scaleform.GfxValue(gbk2unicode(title)))

    def resetWidgets(self):
        self.uiObj.Invoke('resetInstance')

    def onGetTutorialMsg(self, *arg):
        if self.tuTipMsg:
            return Scaleform.GfxValue(gbk2unicode(self.tuTipMsg))
        else:
            return Scaleform.GfxValue(gbk2unicode(''))

    def openTutorialWidget(self, componentId):
        self.uiObj.Invoke('openTutorialWidget', (self.tutorInfo, Scaleform.GfxValue(componentId)))

    def openPicTutorialWidget(self, componentId):
        self.uiObj.Invoke('openPicTutorialWidget', (self.tutorInfo, Scaleform.GfxValue(componentId)))

    def closeTutorialWidget(self, componentId):
        self.uiObj.Invoke('closeTutorialTip', Scaleform.GfxValue(componentId))

    def onClickClose(self, *arg):
        pass

    @ui.callAfterTime()
    def onHandleLeftMouseUp(self, *arg):
        nameList = []
        nameList.append(arg[3][0].GetString())
        nameList.append(arg[3][1].GetString())
        widgetID = int(arg[3][2].GetNumber())
        gamelog.debug('@hjx widgetName#left:', nameList, widgetID)
        gameglobal.rds.tutorial.onMouseLeftBtnUp(nameList)
        if widgetID in UWD.data.get('needLogClickList', []):
            gameglobal.rds.uiLog.addWidgetClickLog(widgetID, *nameList)

    @ui.callAfterTime()
    def onHandleRightMouseUp(self, *arg):
        nameList = []
        nameList.append(arg[3][0].GetString())
        nameList.append(arg[3][1].GetString())
        gamelog.debug('@hjx widgetName#right:', nameList)
        gameglobal.rds.tutorial.onMouseRightBtnUp(nameList)

    def onClickScreen(self, *arg):
        if gameglobal.rds.ui.shop and gameglobal.rds.ui.shop.inRepair:
            gameglobal.rds.ui.shop.clearRepairState()
        self.clearState()

    def onCloseWindow(self, *arg):
        widgetId = arg[3][0].GetNumber()
        if widgetId == uiConst.WIDGET_LOGIN_WIN:
            self.logWin.onCloseWindow(*arg)
        elif widgetId == uiConst.WIDGET_STORY_EDIT:
            self.storyEditDebug.onClose(*arg)
        elif widgetId == uiConst.WIDGET_NPC_ACTION:
            self.npcAction.hide(True)
        elif widgetId == uiConst.WIDGET_MONSTER_ACTION_DEBUG:
            self.monsterAction.hide(True)

    def onAddGroupMember(self, *arg):
        p = BigWorld.player()
        p.cell.applyTeam(p.targetLocked.roleName)

    def onGetStateDetail(self, *arg):
        buffId = int(arg[3][0].GetNumber())
        data = SD.data.get(buffId, None)
        detail = gameStrings.TEXT_BATTLEFIELDPROXY_1605
        if data != None:
            name = data.get('name', '')
            desc = data.get('desc', '')
            detail = name + '\n' + desc
        return Scaleform.GfxValue(gbk2unicode(detail))

    def onIsInGroup(self, *arg):
        ret = False
        p = BigWorld.player()
        if p.isInGroup():
            isHeader = p.members[p.gbId]['isHeader']
            isAssistant = p.members[p.gbId]['isAssistant']
            if isHeader or isAssistant:
                ret = True
        elif p.isInTeam():
            if p.groupHeader == p.id:
                ret = True
        return GfxValue(ret)

    def onHideMenu(self, *arg):
        self.uiObj.Invoke(('hideMenu', arg[3][0]))

    def hideMenu(self, mc):
        self.uiObj.Invoke('hideMenu', mc)

    def hideAllMenu(self):
        self.uiObj.Invoke('hideAllMenu')

    def onClickMenuItem(self, *arg):
        menuName = arg[3][0].GetString()
        menuId = int(arg[3][1].GetNumber())
        menuLabel = ui.unicode2gbk(arg[3][2].GetString())
        menuManager.getInstance().onMenuItemClick(menuName, menuId, menuLabel)

    def initHud(self):
        if self.isHideAllUI():
            return
        self.uiObj.Invoke('initHud')
        self.initPushMsgCallback()
        BigWorld.callback(1, self.recordInitPos)

    def initUIExceptActionbar(self):
        self.uiObj.Invoke('initUIExceptActionbar')

    def showMouse(self, bShow):
        self.uiObj.Invoke('showMouse', Scaleform.GfxValue(bShow))

    @ui.callInterval(0, 3, 1)
    def showBroodLabel(self, type, val, x, y, left = True, isSummonedSprite = False, scale = 1.0, entityId = None):
        if not gameglobal.showBloodLabel:
            return
        elif self.camera.isShow:
            return
        elif scale <= 0:
            return
        elif gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            return
        else:
            en = BigWorld.entities.get(entityId, None)
            if not en or not en.inWorld:
                return
            if en.life == gametypes.LIFE_DEAD:
                if en.deadLabelHadShown:
                    return
                en.deadLabelHadShown = True
            if self.isNewBloodLabelSupport and gameglobal.rds.configData.get('enableOptimizeShowBloodLabelV2', False):
                uiType = int(type)
                pblData = None
                if not isSummonedSprite and uiType in uiConst.PLAYER_BLOOD_LABEL_DATA:
                    pblData = uiConst.PLAYER_BLOOD_LABEL_DATA[uiType]
                if isSummonedSprite and uiType in uiConst.SPRITE_BLOOD_LABEL_DATA:
                    pblData = uiConst.SPRITE_BLOOD_LABEL_DATA[uiType]
                if pblData:
                    tx = self.GUITextFactory.getGUIText()
                    tx.visible = True
                    tx.text = pblData[5] + str(abs(int(val)))
                    tx.colour = Math.Vector4(pblData[0][0], pblData[0][1], pblData[0][2], pblData[0][3])
                    tx.drawPos = Math.Vector2(x, y)
                    tx.damageType = uiType
                    tx.drawSize = Math.Vector2(pblData[1][0], pblData[1][1])
                    tx.moveTime = pblData[2]
                    tx.font = pblData[3]
                    tx.initHeight = pblData[4]
                    tx.isSummonedSprite = bool(isSummonedSprite)
                    GUI.addRoot(tx)
                    return
            gfxValue = Scaleform.GfxValue(abs(int(val)))
            gfxx = Scaleform.GfxValue(x)
            gfxy = Scaleform.GfxValue(y)
            gfLeft = Scaleform.GfxValue(left)
            gfxtype = Scaleform.GfxValue(int(type))
            gfxSprite = Scaleform.GfxValue(bool(isSummonedSprite))
            gfxScale = Scaleform.GfxValue(float(scale))
            if gameglobal.rds.configData.get('enableOptimizeShowBroodLabel', False):
                self.uiObj.Invoke('addbroodLabelNew', (gfxtype,
                 gfxValue,
                 gfxx,
                 gfxy,
                 gfLeft,
                 gfxSprite,
                 gfxScale))
            else:
                self.uiObj.Invoke('addbroodLabel', (gfxtype,
                 gfxValue,
                 gfxx,
                 gfxy,
                 gfLeft,
                 gfxSprite,
                 gfxScale))
            return

    def testShowBroodLabel(self, num, delay, new):
        typeList = (15, 5, 7, 6, 11, 10, 12, 13, 14, 1, 4, 9, 0, 101, 100, 104, 115, 105, 107, 106, 111, 109)
        for i in range(0, num):
            val = random.randint(0, 100)
            type = typeList[random.randint(0, len(typeList) - 1)]
            left = random.randint(0, 1)
            x = random.randint(0, 1661)
            y = random.randint(0, 973)
            self.showBroodLabel(type, val, x, y, left)

        self.broodLabelHandle = BigWorld.callback(delay, Functor(self.testShowBroodLabel, num, delay, new))

    def stopShowBroodLabel(self):
        BigWorld.cancelCallback(self.broodLabelHandle)

    def getEntityUIPos(self, entity):
        isInWorld = False
        if getattr(entity.modelServer, 'bodyModel', None):
            isInWorld = entity.modelServer.bodyModel.inWorld
        if isInWorld:
            node = entity.modelServer.bodyModel.node('biped')
        else:
            node = entity.model.root
        if node == None:
            return (None, None)
        else:
            m = Math.Matrix(node)
            if not isInWorld:
                v = Math.Vector3(m.position)
                v.y = v.y + entity.model.height + 1
                m.applyPoint(v)
            x, y = clientcom.worldPointToScreen(m.applyToOrigin())
            return (x, y)

    def showDefaultLabel(self, defaultName, value, color = None):
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            return
        else:
            value = round(value)
            if value == 0:
                return
            x, y = self.getEntityUIPos(p)
            if x == None:
                return
            x += 80
            y = y + random.randint(-1, 3) * 20 - 50
            gfxx = Scaleform.GfxValue(x)
            gfxy = Scaleform.GfxValue(y)
            defaultStr = '%s +%s' % (defaultName, str(int(value)))
            if color:
                defaultStr = uiUtils.toHtml(defaultStr, color)
            gfxDefaultStr = Scaleform.GfxValue(gbk2unicode(defaultStr))
            self.uiObj.Invoke('addDefaultLabel', (gfxDefaultStr, gfxx, gfxy))
            return

    def showEquipLabel(self, radarData, hideReduce = False):
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            return
        else:
            node = p.model.node('biped')
            if node == None:
                return
            m = Math.Matrix(node)
            x, y = clientcom.worldPointToScreen(m.applyToOrigin())
            addX = x - 150
            reduX = x - 10
            addY = reduY = y + 30
            for id in range(0, 5):
                type = id + 1
                value = round(radarData[id])
                if value == 0:
                    continue
                if value > 0:
                    addX -= 30
                    addY -= 30
                    gfxx = Scaleform.GfxValue(addX)
                    gfxy = Scaleform.GfxValue(addY)
                elif hideReduce:
                    continue
                else:
                    reduX += 30
                    reduY -= 30
                    gfxx = Scaleform.GfxValue(reduX)
                    gfxy = Scaleform.GfxValue(reduY)
                gfxValue = Scaleform.GfxValue(int(value))
                gfxtype = Scaleform.GfxValue(int(type))
                self.uiObj.Invoke('addEquipLabel', (gfxtype,
                 gfxValue,
                 gfxx,
                 gfxy))

            return

    def showFishLabel(self, value, type):
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            return
        else:
            node = p.model.node('biped')
            if node == None:
                return
            value = round(value, 2)
            m = Math.Matrix(node)
            x, y = clientcom.worldPointToScreen(m.applyToOrigin())
            gfxValue = Scaleform.GfxValue(value)
            gfxx = Scaleform.GfxValue(x if type == uiConst.FISHING_NUMBER else x - 9)
            gfxy = Scaleform.GfxValue(y - 200)
            gfxtype = Scaleform.GfxValue(int(type))
            self.uiObj.Invoke('addFishLabel', (gfxtype,
             gfxValue,
             gfxx,
             gfxy))
            return

    def testLifeSkillLabel(self):
        self.showLifeSkillLabel(1, 5)
        self.showLifeSkillLabel(2, 5)
        self.showLifeSkillLabel(3, 5)

    def showLifeSkillLabel(self, sType, sVal):
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            return
        else:
            node = p.model.node('biped')
            if node == None:
                return
            sVal = round(sVal, 2)
            m = Math.Matrix(node)
            x, y = clientcom.worldPointToScreen(m.applyToOrigin())
            gfxValue = Scaleform.GfxValue(sVal)
            gfxx = Scaleform.GfxValue(x)
            gfxy = Scaleform.GfxValue(y - sType * 30)
            gfxtype = Scaleform.GfxValue(int(sType))
            self.uiObj.Invoke('addLifeSkillLabel', (gfxtype,
             gfxValue,
             gfxx,
             gfxy))
            return

    def showRewardLabel(self, value, type, entityId = 0):
        if self.camera.isShow:
            return
        else:
            if entityId == 0:
                entity = BigWorld.player()
            else:
                entity = BigWorld.entities.get(entityId, None)
            if not entity:
                return
            if entity.life == gametypes.LIFE_DEAD and not formula.inDotaBattleField(BigWorld.player().mapID):
                return
            value = round(value)
            if value == 0:
                return
            x, y = self.getEntityUIPos(entity)
            if x == None:
                return
            y = y + random.randint(-1, 3) * 20
            gfxValue = Scaleform.GfxValue(int(value))
            gfxx = Scaleform.GfxValue(x)
            gfxy = Scaleform.GfxValue(y)
            gfxtype = Scaleform.GfxValue(int(type))
            self.uiObj.Invoke('addRewardLabel', (gfxtype,
             gfxValue,
             gfxx,
             gfxy))
            return

    def setScale(self):
        self.uiObj.Invoke('setScale')

    def popSucc(self):
        self.uiObj.Invoke('popSucctip')

    def showMapName(self, name, fortName = None, fortType = None):
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            return
        gfxName = Scaleform.GfxValue('areaName/' + name + '.png')
        if fortName and fortType:
            gfxFortName = Scaleform.GfxValue(gbk2unicode(fortName))
            gfxFortType = Scaleform.GfxValue(fortType)
            self.uiObj.Invoke('showPromptText', (gfxName, gfxFortName, gfxFortType))
        else:
            self.uiObj.Invoke('showPromptText', gfxName)

    def showUndoneMark(self, isShow):
        self.uiObj.Invoke('showUndoneMark', GfxValue(isShow))

    def showPicTip(self, picId):
        path = 'picTip/' + str(picId) + '.dds'
        self.uiObj.Invoke('showPromptText', Scaleform.GfxValue(path))
        soundList = CWTD.data.get(picId, {}).get('musicId')
        if soundList:
            for sound in soundList:
                gameglobal.rds.sound.playSound(int(sound))

    def showStoryModeState(self, name):
        screenRipple.rippleScreen()
        self.uiObj.Invoke('showPromptText', Scaleform.GfxValue('storyMode/' + name + '.png'))

    def showEnterObserveModeState(self):
        self.uiObj.Invoke('showPromptText', Scaleform.GfxValue('fightObserve/enter.dds'))

    def loadUnitFrames(self):
        self.uiObj.Invoke('loadUnitFrames')

    def unLoadWidget(self, id):
        self.uiObj.Invoke('unloadTweener', Scaleform.GfxValue(id))
        self.playCloseSoundById(id)
        if id == uiConst.WIDGET_MAP:
            p = BigWorld.player()
            if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
                BigWorld.callback(0, self.hideCursorForActionPhysics)
        if id == uiConst.WIDGET_QUESTIONNAIRE:
            self.questionnaire.reset()
        if self.widgetLoadedTime.has_key(id):
            time = utils.getNow() - self.widgetLoadedTime.pop(id)
            gameglobal.rds.uiLog.addWidgetShowTimeLog(id, time)
        if BigWorld.player():
            if id in uiConst.RECORD_WIDGET_SORT_LIST and self.recordShowSet and not self.isStartRecodShowList:
                recodList = list(self.recordShowSet)
                recodList.sort(cmp=lambda a, b: cmp(uiConst.RECORD_WIDGET_SORT_LIST.index(a[0]), uiConst.RECORD_WIDGET_SORT_LIST.index(b[0])))
                self.recordShowSet.remove(recodList[0])
                self.loadWidget(*recodList[0])

    def playCloseSoundById(self, id):
        if id in self.uiSoundMap:
            gameglobal.rds.sound.playSound(self.uiSoundMap[id][1])
        if id in self.uiCommonOpenCloseSoundMap:
            gameglobal.rds.sound.playSound(self.commonPlaySound[1])
        if id / 10000 in (uiConst.WIDGET_MESSAGEBOX, uiConst.WIDGET_MESSAGEBOX_LOW):
            gameglobal.rds.sound.playSound(self.msgPlaySound[1])
        if id in self.uiPopUpMap:
            gameglobal.rds.sound.playSound(self.msgPlaySound[1])

    def setFilterWidget(self, filterWidget):
        ar = self.movie.CreateArray()
        for index, value in enumerate(filterWidget):
            ar.SetElement(index, Scaleform.GfxValue(value))

        return ar

    def unLoadAllWidget(self, filterWidget = [], includeLoading = False):
        try:
            gameglobal.rds.ui.hideAllMenu()
            BigWorld.endGrayFilter(1)
            self.showUndoneMark(False)
            sceneInfo.AreaInfo.getInstance().lastName = ''
            if uiConst.WIDGET_SHOP not in filterWidget:
                self.shop.hide()
            if uiConst.WIDGET_NPC_QUEST not in filterWidget:
                self.quest.close()
            if uiConst.WIDGET_ARENA_WAIT_BG not in filterWidget:
                self.arenaWait.closeArenaWait()
            if uiConst.WIDGET_COMPOSITE_SHOP not in filterWidget:
                self.compositeShop.closeShop()
            if uiConst.WIDGET_CHAT_TO_FRIEND not in filterWidget:
                self.chatToFriend.hide()
            if uiConst.WIDGET_BULLET not in filterWidget:
                self.bullet.hide()
            if uiConst.WIDGET_DEAD_RELIVE_BLOOD not in filterWidget:
                self.deadAndRelive.closeBloodBg()
            if uiConst.WIDGET_VP_TRANSFORM_TIP not in filterWidget:
                self.roleInfo.onCloseVpTransformTip()
            if uiConst.WIDGET_FULLSCREEN_FITTINGROOM not in filterWidget:
                self.fullscreenFittingRoom.hide()
            if uiConst.WIDGET_TUZHUANG not in filterWidget:
                self.tuZhuang.hide()
        except:
            pass

        self.uiObj.Invoke('unloadAllWidget', (self.setFilterWidget(filterWidget), GfxValue(includeLoading)))

    def _canLoad(self, widgetId, loadType = uiConst.UI_LOAD_TOP_LEVEL):
        if BigWorld.player() and getattr(BigWorld.player(), 'crossServerFlag', None) == const.CROSS_SERVER_STATE_IN:
            spaceNo = formula.getMapId(BigWorld.player().spaceNo)
            if widgetId in MCD.data.get(spaceNo, {}).get('crossServerBlackWidgt', ()):
                BigWorld.player().showGameMsg(GMDD.data.WIDGET_IN_BLACK_LIST, ())
                return False
        if self._isFullScreenWidget(widgetId):
            return True
        else:
            if self.map.isShow:
                canLoadWidgets = UWD.data.get('map', {}).get(loadType, [])
                if widgetId not in canLoadWidgets:
                    return False
            if self.quest.isShow or self.npcV2.isShow:
                canLoadWidgets = UWD.data.get('quest', {}).get(loadType, [])
                if widgetId not in canLoadWidgets:
                    return False
            if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
                canLoadWidgets = UWD.data.get('scenario', {}).get(loadType, [])
                if widgetId not in canLoadWidgets:
                    return False
            if self.fubenLogin.isShow:
                canLoadWidgets = UWD.data.get('fbApply', {}).get(loadType, [])
                if widgetId not in canLoadWidgets:
                    return False
            if self.QTEHideUI:
                if widgetId not in (uiConst.WIDGET_EXACT_QTE, uiConst.WIDGET_CORRECT_QTE, uiConst.WIDGET_ACCUMULATE_QTE):
                    return False
            return True

    def onGetNoCloseInRestore(self, *arg):
        ret = []
        isInScenario = gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA
        if self.map.isShow or self.quest.isShow or self.npcV2.isShow or isInScenario or self.fubenLogin.isShow or self.realNameCheck.widget:
            ret = UWD.data.get('noClose', {}).get(1, [])
        return uiUtils.array2GfxAarry(ret)

    def onGetServerTime(self, *arg):
        if hasattr(BigWorld.player(), 'getServerTime'):
            return GfxValue(BigWorld.player().getServerTime())
        else:
            return GfxValue(time.time())

    def onGetSaveWidgetPosInfo(self, *arg):
        return uiUtils.dict2GfxDict(UWD.data.get('dragAble', {}), True)

    def restoreGC(self):
        if gameglobal.rds.configData.get('enableCtrlWidgetGC', False):
            self.movie.SuspendGC(False)

    def loadWidget(self, id, isModal = False, isTabEnable = False, layoutType = 0):
        if self.isStartRecodShowList and id in uiConst.RECORD_WIDGET_SORT_LIST:
            self.recordShowSet.add((id,
             isModal,
             isTabEnable,
             layoutType))
            gamelog.info('jbx:recordWidget', id, isModal, isTabEnable, layoutType)
            return
        p = BigWorld.player()
        if p and hasattr(p, '_isSchoolSwitch') and p._isSchoolSwitch() and id in uiConst.SCHOOL_SWITCH_BLACK_LIST:
            return
        if not self._canLoad(id):
            return
        if id == uiConst.WIDGET_ROLE_INFO or id == uiConst.WIDGET_INVENTORY:
            if gameglobal.rds.configData.get('enableCtrlWidgetGC', False):
                self.movie.SuspendGC(True)
                BigWorld.callback(3, self.restoreGC)
        if gameglobal.rds.configData.get('enableUIProfile', False):
            self.profile.startLoadWidget(id)
        multiId = int(self.uiObj.Invoke('loadWidget', (Scaleform.GfxValue(id),
         Scaleform.GfxValue(isModal),
         Scaleform.GfxValue(isTabEnable),
         Scaleform.GfxValue(layoutType))).GetNumber())
        widgetIds = SCD.data.get('needShowCursorWidgetIds', ())
        if id in widgetIds:
            self.showCursorForActionPhysics()
        self.playOpenSoundById(id)
        if p and hasattr(p, 'statsTriggerAtClient'):
            p.statsTriggerAtClient('loadWidgetTrigger', (id,))
        return multiId

    def playOpenSoundById(self, id):
        if id in self.uiSoundMap:
            gameglobal.rds.sound.playSound(self.uiSoundMap[id][0])
        if id in self.uiCommonOpenCloseSoundMap:
            gameglobal.rds.sound.playSound(self.commonPlaySound[0])
        if id in self.uiPopUpMap:
            gameglobal.rds.sound.playSound(self.msgPlaySound[0])
        if id in (uiConst.WIDGET_MESSAGEBOX, uiConst.WIDGET_MESSAGEBOX_LOW):
            gameglobal.rds.sound.playSound(self.msgPlaySound[0])

    def hideAllUI(self):
        if self.lockHideAllUI:
            return
        self.uiObj.Invoke('hideAllUI')
        if hasattr(BigWorld.player(), 'ap') and hasattr(BigWorld.player().ap, 'aimCross'):
            BigWorld.player().ap.aimCross.hide()
            self.hideAimCross(True, True)
            self.hideAimCross(True, False)
            self.hideAimCross(False)
        self.hideAllMenu()
        ccControl.setCCVisible(0)

    def restoreUI(self):
        if gameglobal.rds.GameState == gametypes.GS_START:
            return
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.Invoke('forceVisibleByOther')
        self.uiObj.Invoke('restoreUI')
        if hasattr(BigWorld.player(), 'ap') and hasattr(BigWorld.player().ap, 'aimCross'):
            BigWorld.player().ap.aimCross.turnToAimState()
        ccControl.setCCVisible(1)

    def hideAllUIByLock(self):
        self.lockHideAllUI = True

    def restoreUIByUnLock(self):
        self.lockHideAllUI = False

    def openDialog(self, title, description, options):
        self.generaldebug.setFuncList(title, description, options)
        self.generaldebug.showGeneralDebugView()

    def onSetModalState(self, *arg):
        state = arg[3][0].GetBool()
        p = BigWorld.player()
        if hasattr(p, 'ap') and state == True:
            p.ap.stopMove()
        gameglobal.isModalDlgShow = state

    def onNotifyStateRelease(self, *arg):
        stateId = int(arg[3][0].GetNumber())
        entityId = int(arg[3][1].GetNumber())
        if entityId not in (BigWorld.player().id, -1):
            return
        elif stateId == const.LING_SHI_STATE_CLIENT_STATE:
            BigWorld.player().switchLingShiFlag()
            return
        else:
            data = SD.data.get(stateId, None)
            if stateId == const.PROTECT_STATE_ID and BigWorld.player().gmMode:
                gmModeConfig = const.GM_MODE_CONFIG.get(BigWorld.player().gmMode, {})
                if gmModeConfig.get('protect', False):
                    if BigWorld.player().gmMode == const.GM_MODE_LIVE_OBSERVER:
                        BigWorld.player().showDebugMessge(gameStrings.TEXT_UIADAPTER_1848)
                    else:
                        BigWorld.player().showDebugMessge(gameStrings.TEXT_UIADAPTER_1850)
                    return
            if data != None and data.has_key('removeable'):
                BigWorld.player().cell.cancelState(stateId)
            return

    def showSpecSkill(self, name):
        self.uiObj.Invoke('showSpecSkill', Scaleform.GfxValue(name))

    def registerClear(self, ent):
        ui.entityClickTime = int(BigWorld.time())
        ui.entityClicked = ent

    def clearNPCDlg(self, npc):
        if npc != ui.entityClicked:
            return
        else:
            ui.entityClicked = None
            gameglobal.rds.ui.npcPanel.clearNpcPanel()
            if gameglobal.rds.ui.quest.isShow:
                gameglobal.rds.ui.quest.close()
            if gameglobal.rds.ui.npcV2.isShow:
                gameglobal.rds.ui.npcV2.leaveStage()
            if gameglobal.rds.ui.equipEnhance.mediator:
                gameglobal.rds.ui.equipEnhance.clearAllWidget()
            if gameglobal.rds.ui.fashionPropTransfer.mediator:
                gameglobal.rds.ui.fashionPropTransfer.clearAllWidget()
            if gameglobal.rds.ui.shop.inRepair:
                gameglobal.rds.ui.shop.clearRepairState()
                gameglobal.rds.ui.messageBox.dismiss(uiConst.MESSAGEBOX_SHOP, False)
            if gameglobal.rds.ui.compositeShop.isOpen:
                gameglobal.rds.ui.compositeShop.closeShop()
            if gameglobal.rds.ui.trainingArea.isShow:
                gameglobal.rds.ui.trainingArea.onLeaveTrain(None)
            if gameglobal.rds.ui.trainingAreaAward.isShow:
                gameglobal.rds.ui.trainingAreaAward.hide(True)
            if gameglobal.rds.ui.consign.mediator:
                gameglobal.rds.ui.consign.hide()
            if gameglobal.rds.ui.jobBoard.mediator:
                gameglobal.rds.ui.jobBoard.hide()
            if gameglobal.rds.ui.jobBoard.detailMed:
                gameglobal.rds.ui.jobBoard.closeDetail()
            if gameglobal.rds.ui.createGuild.mediator:
                gameglobal.rds.ui.createGuild.hideByNpcId(npc.id)
            if gameglobal.rds.ui.applyGuild.mediator:
                gameglobal.rds.ui.applyGuild.hideByNpcId(npc.id)
            if gameglobal.rds.ui.guildResident.mediator:
                gameglobal.rds.ui.guildResident.hideByNpcId(npc.id)
            if gameglobal.rds.ui.guildBuildUpgrade.mediator:
                gameglobal.rds.ui.guildBuildUpgrade.hideByNpcId(npc.id)
            if gameglobal.rds.ui.shishenBoard.mediator:
                gameglobal.rds.ui.shishenBoard.hide()
            if gameglobal.rds.ui.purchaseShop.mediator:
                gameglobal.rds.ui.purchaseShop.hide()
            if gameglobal.rds.ui.purchaseSell.mediator:
                gameglobal.rds.ui.purchaseSell.hide()
            if gameglobal.rds.ui.equipMixNew.mediator:
                gameglobal.rds.ui.equipMixNew.clearWidget()
            if gameglobal.rds.ui.wmdRankList.mediator:
                gameglobal.rds.ui.wmdRankList.hide()
            if gameglobal.rds.ui.xinmoBook.mediator:
                gameglobal.rds.ui.xinmoBook.hide()
            if gameglobal.rds.ui.noticeBoard.med:
                gameglobal.rds.ui.noticeBoard.hide()
            if gameglobal.rds.ui.dyePlane.med:
                gameglobal.rds.ui.dyePlane.hide()
            if gameglobal.rds.ui.cbgMain.widget:
                gameglobal.rds.ui.cbgMain.hide()
            return

    def onHideTooltip(self, *arg):
        pass

    def isHideAllUI(self):
        ret = self.uiObj.Invoke('isHideAllUI').GetBool()
        return ret

    def isWidgetLoaded(self, widgetId):
        ret = self.uiObj.Invoke('isWidgetLoaded', (Scaleform.GfxValue(widgetId),)).GetBool()
        return ret

    def isWidgetLoading(self, widgetId):
        ret = self.uiObj.Invoke('isWidgetLoading', (Scaleform.GfxValue(widgetId),)).GetBool()
        return ret

    def closeTopByEsc(self):
        return self.uiObj.Invoke('closeTopWidgetByEsc').GetBool()

    def onCanEscQuit(self, *arg):
        widgetId = int(arg[3][0].GetNumber())
        widgetMultiId = int(arg[3][1].GetNumber())
        self.clearState()
        if widgetId in (uiConst.WIDGET_MESSAGEBOX, uiConst.WIDGET_MESSAGEBOX_LOW):
            needDissMissCallBack = self.messageBox.loadeds[widgetMultiId][3]
            canEsc = self.messageBox.loadeds[widgetMultiId][4]
            if canEsc:
                self.messageBox.dismiss(widgetMultiId, needDissMissCallBack=needDissMissCallBack)
                if len(gameglobal.rds.ui.trade.traderQueue):
                    gameglobal.rds.ui.trade.escForReject()
        elif widgetId == uiConst.WIDGET_PUZZLE:
            gameglobal.rds.ui.puzzle.hidePuzzle()
        elif widgetId in self.escFunc:
            if self.escFunc[widgetId][0] == 'unLoadWidget':
                self.unLoadWidget(widgetId)
            elif len(self.escFunc[widgetId]) == 1:
                self.escFunc[widgetId][0]()
            elif len(self.escFunc[widgetId]) == 2 and self.escFunc[widgetId][1]:
                self.escFunc[widgetId][0](widgetId, widgetMultiId)
        elif self.quest.isShow:
            self.npcPanel.hideNpcFullScreen()
        elif self.npcV2.isShow:
            self.npcV2.onClickExitBtn()

    def registerEscFunc(self, widgetId, closeFunc, withParam = False):
        if withParam:
            self.escFunc[widgetId] = [closeFunc, True]
        else:
            self.escFunc[widgetId] = [closeFunc]

    def showTips(self, msg, noBtn = False):
        gameglobal.rds.ui.characterDetailAdjust.showTips(msg, int(noBtn))

    def hideTips(self):
        gameglobal.rds.ui.characterDetailAdjust.closeTips()

    def playDragItemSound(self, proxyInfo):
        proxy = self.getDragProxy(proxyInfo)
        item = None
        p = BigWorld.player()
        if proxy and proxy.type in ('bagslot', 'actionbar', 'trade', 'sackslot', 'booth'):
            page, pos = self.getDragSlotID(proxy, proxyInfo)
            if proxy.type == 'bagslot':
                if page == uiConst.BAG_PAGE_QUEST:
                    item = BigWorld.player().questBag.getQuickVal(0, pos)
                else:
                    item = BigWorld.player().inv.getQuickVal(page, pos)
            elif proxy.type == 'actionbar':
                if page in (uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
                    if proxy.clientShortCut.has_key((page, pos)):
                        itemId = proxy.clientShortCut[page, pos][1]
                        bagPage, bagPos = BigWorld.player().inv.findItemInPages(itemId, includeExpired=True, includeLatch=True, includeShihun=True)
                        item = p.inv.getQuickVal(bagPage, bagPos)
                elif page == uiConst.EQUIP_ACTION_BAR:
                    item = p.equipment.get(pos)
            elif proxy.type == 'trade':
                if page == uiConst.TRADE_SLOTS_MINE:
                    item = self.trade.Items[page][pos]
            elif proxy.type == 'sackslot':
                if page == const.BAG_BAR_BIND_ID:
                    item = p.bagBar.getQuickVal(page, pos)
            elif proxy.type == 'booth':
                item = p.booth.getQuickVal(page, pos)
        if item:
            soundIdx = item.getDragItemSound()
            gamelog.debug('playDragItemSound', item, soundIdx)
            gameglobal.rds.sound.playSound(soundIdx)
            return True
        else:
            return False

    def playUseItemSound(self, item):
        if item:
            if gameglobal.rds.GameState != gametypes.GS_LOADING:
                soundIdx = item.getUseItemSound()
                gameglobal.rds.sound.playSound(soundIdx)

    def _initUISound(self):
        self.uiSoundMap = UWD.data.get('specialSoundMap', {})
        self.uiCommonOpenCloseSoundMap = UWD.data.get('commonSoundList', [])
        self.uiPopUpMap = UWD.data.get('msgPlaySoundList', [])
        self.commonPlaySound = (4, 5)
        self.msgPlaySound = (32, 5)

    def onIsDragable(self, *arg):
        stateArray = [ui.SIGNEQUIP_STATE,
         ui.DYE_STATE,
         ui.IDENTIFY_ITEM_STATE,
         ui.IDENTIFY_MANUAL_EQUIP_STATE]
        if gameglobal.rds.ui.shop.inRepair:
            return GfxValue(False)
        if ui.get_cursor_state() in stateArray:
            return GfxValue(False)
        return GfxValue(True)

    def onUnDrag(self, *arg):
        self.inDrag = False
        gameglobal.rds.ui.actionbar.setNormalSlotsShine(False)
        gameglobal.rds.ui.actionbar.setSpecialSlotState(uiConst.SKILL_ICON_STAT_USEABLE)
        gameglobal.rds.ui.actionbar.validateSlotVisible()
        gameglobal.rds.ui.actionbar.setAllSlotAlpha(uiConst.SKILL_ICON_STAT_USEABLE)
        gameglobal.rds.ui.actionbar.initAllSkillStat()

    def onClickMarkTarget(self, *arg):
        tag = arg[3][0].GetString()
        targetId = menuManager.getInstance().menuTarget.entityId
        if targetId:
            BigWorld.player().cell.markEntity(targetId, int(tag[1:]))

    def setRecordVisible(self):
        self.uiObj.Invoke('setRecordVisible')

    def returnLoginView(self):
        p = BigWorld.player()
        p.isReturnToLogin = True
        logoffDelay = SCD.data.get('logoffDelay', 10)
        buttons = [MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, self._unlogOff)]
        gameglobal.rds.needSendInfoToHttp = False
        gameglobal.rds.ui.messageBox.show(True, gameStrings.TEXT_PLAYRECOMMPROXY_495, gameStrings.TEXT_UIADAPTER_2063, buttons, repeat=logoffDelay, countDownFunctor=self._doReturnToLogin)
        gameglobal.isModalDlgShow = True
        p.cell.logOff()
        p.base.setOfflineType(gametypes.PLAYER_OFFLINE_TYPE_RETURN)
        p.ap.restore()
        self.loginSelectServer.onRefreshServerList()
        p.takeCharSnapshotBeforeQuit()

    def _unlogOff(self):
        p = BigWorld.player()
        if not p:
            return
        gameglobal.rds.needSendInfoToHttp = True
        p.isReturnToLogin = False
        gameglobal.isModalDlgShow = False
        p.cell.unlogOff()
        p.base.setOfflineType(gametypes.PLAYER_OFFLINE_TYPE_ERROR)

    def _doReturnToLogin(self):
        gameglobal.rds.loginManager.disconnectFromGame()

    def refreshPlayerPos(self, showAreaInfo = True):
        p = BigWorld.player()
        if p is None or not p.inWorld:
            return
        else:
            if self.callbackHandler:
                BigWorld.cancelCallback(self.callbackHandler)
            self.callbackHandler = BigWorld.callback(1, self.refreshPlayerPos)
            x = round(p.position[0])
            y = round(p.position[2])
            yaw = p.yaw
            self.map.setPlayerPos(x, y, yaw)
            self.littleMap.setPlayerPos(x, y, yaw)
            self.topBar.sendLatency()
            gameglobal.rds.ui.topBar.refreshFps()
            showAreaInfo and sceneInfo.AreaInfo.getInstance().showAreaInfo()
            enableUIGCControl = gameglobal.rds.configData.get('enableUIGCControl', True)
            if enableUIGCControl and self.isStopGC and BigWorld.getUIMem() > const.UI_MAX_MEM:
                self.stopGC(False)
            return

    def stopGC(self, stop):
        if hasattr(self.movie, 'StopGC'):
            self.movie.StopGC(stop)
            self.isStopGC = stop

    def enableUIGCControl(self):
        enableUIGCControl = gameglobal.rds.configData.get('enableUIGCControl', True)
        if not enableUIGCControl:
            self.stopGC(False)

    def setWidgetLevel(self, widgetId, level = -1):
        self.uiObj.Invoke('setWidgetLevel', (Scaleform.GfxValue(widgetId), Scaleform.GfxValue(level)))

    def setWidgetVisible(self, widgetId, isVisible):
        self.uiObj.Invoke('setWidgetVisible', (Scaleform.GfxValue(widgetId), Scaleform.GfxValue(isVisible)))
        self.uiObj.Invoke('setVisRecord', (Scaleform.GfxValue(widgetId), Scaleform.GfxValue(isVisible)))

    def setVisRecord(self, widgetId, isVisible):
        self.uiObj.Invoke('setVisRecord', (Scaleform.GfxValue(widgetId), Scaleform.GfxValue(isVisible)))

    def _isFullScreenWidget(self, widgetId):
        for item in uiConst.FULL_SCREEN_WIDGET:
            if isinstance(item, tuple):
                if widgetId in item:
                    return True
            elif widgetId == item:
                return True

        return False

    def isInFullScreenStatus(self):
        if self.map.isShow:
            return True
        if self.quest.isShow or self.npcV2.isShow:
            return True
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            return True
        if self.fubenLogin.isShow:
            return True
        if self.fullscreenFittingRoom.mediator:
            return True
        if self.tuZhuang.med:
            return True
        return False

    def onGetWidegetIndex(self, *arg):
        ar = arg[3][1]
        arr = []
        weightDict = UWD.data.get('weight', {}).copy()
        weightDict.update(self.tempWeightDict)
        widgetId = int(arg[3][0].GetString())
        if widgetId not in weightDict:
            return GfxValue(ar.GetArraySize())
        else:
            i = 0
            for id in range(0, ar.GetArraySize()):
                elementId = int(ar.GetElement(id).GetString())
                arr.append(elementId)
                if elementId == -1:
                    i += 1
                elif elementId not in weightDict:
                    break
                elif weightDict[elementId] <= weightDict[widgetId]:
                    i += 1
                else:
                    break

            return GfxValue(i)

    def setTempWeight(self, widgetId, level):
        if level >= 0:
            self.tempWeightDict[widgetId] = level
        elif self.tempWeightDict.has_key(widgetId):
            del self.tempWeightDict[widgetId]
            widget = self.getWidgetByID(widgetId)
            if widget and widget.swapPanelToFront:
                widget.swapPanelToFront()

    def onWidgetLoadCompeleted(self, *arg):
        widgetId = int(arg[3][0].GetNumber())
        ui.onWidgetLoaded(widgetId)
        widgetIds = SCD.data.get('needShowCursorWidgetIds', ())
        gameglobal.rds.ui.dispatchEvent(events.EVENT_WIDGET_LOAD_COMPLETE, widgetId)
        if widgetId in widgetIds:
            gameglobal.isWidgetNeedShowCursor = self.isWidgetNeedShowCursor()
            self.showCursorForActionPhysics()
        gameglobal.rds.tutorial.onLoadWidget(widgetId)
        if widgetId == uiConst.WIDGET_FIND_BEAST_LUCKJOY:
            gameglobal.rds.ui.findBeastLuckJoy.refreshBg()
        gameglobal.rds.tutorial.onLoadedWidgetTrigger(widgetId)
        if gameglobal.rds.configData.get('enableUIStatistisc', False):
            gameglobal.rds.uiLog.addUIOpenCntLog(widgetId)
        if widgetId in UWD.data.get('needLogOpenCntList', []):
            gameglobal.rds.uiLog.addWidgetOpenCntLog(widgetId)
        if widgetId in UWD.data.get('needLogShowTimeList', []):
            self.widgetLoadedTime[widgetId] = utils.getNow()
        if widgetId == uiConst.WIDGET_BF_FINAL_RESULT:
            p = BigWorld.player()
            p.showGetFameFailedMsg()
        if widgetId == uiConst.WIDGET_AIR_BATTLE_BAR:
            self.airbar.checkAvatarState()
        elif widgetId == uiConst.WIDGET_ACTION_BARS:
            self.actionbar.checkAvatarState()
        self.onTopWidgetChanged()
        if not self._isFullScreenWidget(widgetId):
            return
        if widgetId != uiConst.WIDGET_MAP:
            if self.map.isShow:
                self.map.realClose()
        if widgetId == uiConst.WIDGET_NPC_QUEST:
            self.loadWidget(uiConst.WIDGET_NPC_QUEST_BUTTON)
            if gameglobal.rds.ui.funcNpc.lastFuncType == npcConst.NPC_FUNC_FB_TRAINING:
                self.trainingNpc.refreshTrainingPanel()

    def onWidgetLoadError(self, *arg):
        widgetId = int(arg[3][0].GetNumber())
        if widgetId == uiConst.WIDGET_NPC_QUEST:
            p = BigWorld.player()
            p.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_UIADAPTER_2241,))
            if gameglobal.rds.ui.quest.isShow:
                self.closeQuestWindow()
            if gameglobal.rds.ui.npcV2.isShow:
                gameglobal.rds.ui.npcV2.leaveStage()

    def enterQuestScreen(self):
        p = BigWorld.player()
        if p.inBooth():
            p.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_UIADAPTER_2251,))
            return False
        if self.autoQuest.isShow():
            self.autoQuest.hide()
        if not gameglobal.rds.ui.enableUI:
            p.showUI(True)
        p.ap.stopMove(True)
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI)
        if self.map.isShow:
            self.map.realClose()
        self.hideAllUI()
        BigWorld.setDofTransitTime(0.5)
        BigWorld.setDepthOfField(True, 5, 0.15)
        p.hideTopLogo(True)
        if p.pkMode == const.PK_MODE_KILL or p.pkMode == const.PK_MODE_HOSTILE:
            p.topLogo.stopPKLogo()
        gameglobal.rds.sound.playSound(gameglobal.SD_92)
        return True

    def quitQuestScreen(self):
        p = BigWorld.player()
        p.unlockKey(gameglobal.KEY_POS_UI)
        self.restoreUI()
        self.chat.showView()
        BigWorld.resetDepthOfField()
        p.hideTopLogo(False)
        if p.pkMode == const.PK_MODE_KILL or p.pkMode == const.PK_MODE_HOSTILE:
            p.topLogo.updatePkTopLogo()
        gameglobal.rds.sound.playSound(gameglobal.SD_93)

    def openQuestWindow(self, npcType):
        if gameglobal.rds.configData.get('enableNpcV2', False) and not self.quest.isShow:
            self.npcV2.npcType = npcType
            self.npcV2.enterStage()
        else:
            self.quest.npcType = npcType
            if self.quest.mc:
                if self.quest.npcType == uiConst.NPC_QUEST:
                    self.quest.mc.Invoke('refreshNpcQuestPanel', self.quest.onGetQuestNames())
                elif self.quest.npcType == uiConst.NPC_FUNC:
                    self.quest.mc.Invoke('refreshNpcFuncPanel', self.funcNpc.onGetFuncNpcChatInfo())
                elif self.quest.npcType == uiConst.NPC_DEBATE:
                    self.quest.mc.Invoke('refreshNpcDebatePanel', self.debate.onGetDebateInfo())
                elif self.quest.npcType == uiConst.NPC_MULTI:
                    self.quest.mc.Invoke('refreshNpcMultiPanel', self.multiNpcChat.onGetMultiNpcChatInfo())
                elif self.quest.npcType == uiConst.NPC_TELEPORT:
                    self.quest.mc.Invoke('refreshNpcTeleportPanel', self.npcPanel.onGetTeleportInfo())
                elif self.quest.npcType == uiConst.NPC_TOWER:
                    self.quest.mc.Invoke('refreshTowerDefencePanel', self.npcPanel.onGetTowerDefenseInfo())
                elif self.quest.npcType == uiConst.NPC_FUNC_DIRECTLY:
                    self.quest.mc.Invoke('refreshNpcFuncDirectlyPanel', self.funcNpc.onGetFuncNpcDirectlyInfo())
                elif self.quest.npcType == uiConst.NPC_PRIZE:
                    self.quest.mc.Invoke('refreshNpcPrizePanel', self.funcNpc.onGetPrizeInfo())
                elif self.quest.npcType == uiConst.NPC_EXPLAIN:
                    self.quest.mc.Invoke('refreshNpcExplanationPanel', self.funcNpc.onGetExplanation())
                elif self.quest.npcType == uiConst.NPC_AWARD:
                    self.quest.mc.Invoke('refreshNpcCompensatePanel', self.funcNpc.onGetAward())
                elif self.quest.npcType == uiConst.NPC_FUBEN_DIFFICULTY:
                    self.quest.mc.Invoke('refreshNpcFubenDifficulty', self.funcNpc.onGetFubenDifficulty())
                elif self.quest.npcType == uiConst.NPC_FAME_SALARY:
                    self.quest.mc.Invoke('refreshNpcFameSalary', self.funcNpc.onGetFameSalaryInfo())
                elif self.quest.npcType == uiConst.NPC_BUSINESS_SPY:
                    self.quest.mc.Invoke('refreshBusinessSpy', self.funcNpc.onGetBusinessSpyInfo())
            elif not self.quest.isShow:
                if self.enterQuestScreen():
                    self.quest.isShow = True
                    self.setWidgetVisible(uiConst.WIDGET_NPC_QUEST, True)
                    self.loadWidget(uiConst.WIDGET_NPC_QUEST)

    def closeQuestWindow(self, showCursor = False):
        if self.quest.isShow:
            self.quitQuestScreen()
        self.quest.resetHeadGen()
        self.quest.isShow = False
        self.quest.mc = None
        self.funcNpc.mc = None
        p = BigWorld.player()
        if showCursor and p and hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            self.showCursorAfterWidget = showCursor
            BigWorld.callback(0.1, self.showCursorForActionPhysics)
        self.unLoadWidget(uiConst.WIDGET_NPC_QUEST)
        self.unLoadWidget(uiConst.WIDGET_NPC_QUEST_BUTTON)
        self.funcNpc.lastFuncType = 0
        self.funcNpc.buttonCallback = None
        if utils.instanceof(ui.entityClicked, 'Npc') or utils.instanceof(ui.entityClicked, 'Dawdler'):
            self.playLeaveAction(ui.entityClicked.id)
        if p and hasattr(p, '_isOnZaijuOrBianyao'):
            if p._isOnZaijuOrBianyao():
                zjd = ZD.data.get(p._getZaijuOrBianyaoNo(), {})
                skills = tuple(zjd.get('skills', ())) + tuple(zjd.get('icons', ()))
                if zjd.get('replaceBar', 1) == 0:
                    p.showZaijuUI(skills=skills)
                else:
                    p.showZaijuUI(showType=uiConst.ZAIJU_SHOW_TYPE_EXIT)
        gameglobal.rds.ui.itemPushUse.checkAndShow()

    def playLeaveAction(self, npcId):
        try:
            entNpc = BigWorld.entities.get(npcId, None)
        except:
            entNpc = None

        if entNpc and entNpc.inWorld and not getattr(entNpc, 'isMoving', False):
            if entNpc.fashion.action:
                actionName = entNpc.fashion.action.getLeaveAction()
                entNpc.fashion.playSingleAction(actionName)

    def getDefinitionByName(self, name):
        gfxName = Scaleform.GfxValue(name)
        definition = self.movie.invoke(('flash.utils.getDefinitionByName', gfxName))
        return definition

    def isMouseInUI(self):
        ret = self.uiObj.Invoke('isMouseInUI')
        return not ret.IsNull()

    def showPlayerPhoto(self, avatarType, actionId):
        capturePhoto.bigPhoto.setAvatarSwfPath(avatarType)
        capturePhoto.bigPhoto.startCapture(str(actionId))

    def closePlayerPhoto(self):
        self.uiObj.Invoke('closeBigPlayerPhoto')
        capturePhoto.bigPhoto.endCapture()

    def showSkillEffect(self, avatarId, uiEffectId):
        if not gameglobal.showWsEffect:
            return
        else:
            avatarData = SAD.data.get(avatarId)
            if avatarData != None:
                avatarType = 'widgets/skill/' + str(avatarData.get('showType')) + gameglobal.rds.ui.getUIExt()
                avatarAction = str(avatarData.get('action'))
                self.showPlayerPhoto(avatarType, avatarAction)
            uiEffectData = SUED.data.get(uiEffectId)
            if uiEffectData != None:
                uiEffectPath = 'widgets/skill/' + uiEffectData.get('skillUIEffectPath') + gameglobal.rds.ui.getUIExt()
                uiEffectType = uiEffectData.get('showType')
                if gameglobal.rds.configData.get('enableCtrlWidgetGC', False):
                    self.movie.SuspendGC(True)
                    BigWorld.callback(3, self.restoreGC)
                self.uiObj.Invoke('showSkillEffect', (Scaleform.GfxValue(uiEffectType), Scaleform.GfxValue(uiEffectPath)))
            return

    def onGetWidgetSavingPos(self, *arg):
        wid = arg[3][0].GetNumber()
        saveName = UWD.data.get('dragAble', {}).get(wid, {}).get('savename')
        if saveName:
            savingKey = keys.SET_UI_INFO + '/' + saveName
            result = [AppSettings.get(savingKey + '/pos/x', -1),
             AppSettings.get(savingKey + '/pos/y', -1),
             AppSettings.get(keys.SET_UI_SAVEPOS_WIDTH, -1),
             AppSettings.get(keys.SET_UI_SAVEPOS_HEIGHT, -1)]
            return uiUtils.array2GfxAarry(result)

    def getCurrentScaleInfo(self):
        data = self.uiObj.Invoke('getScaleInfo')
        return [data.GetElement(0).GetNumber(), data.GetElement(1).GetNumber(), data.GetElement(2).GetNumber()]

    def onGetWidgetSavingHidden(self, *arg):
        wid = arg[3][0].GetNumber()
        saveName = UWD.data.get('dragAble', {}).get(wid, {}).get('savename')
        if saveName:
            savingKey = keys.SET_UI_INFO + '/' + saveName
            result = AppSettings.get(savingKey + '/hidden', 0)
            return GfxValue(result)

    def onGetWidgetCanShow(self, *arg):
        wid = arg[3][0].GetNumber()
        if gameglobal.rds.ui.dragButton.isDragAble():
            return GfxValue(0)
        if gameglobal.rds.configData.get('enableF11Hide', False):
            if wid in UWD.data.get('canF11Hide', []):
                saveName = UWD.data.get('dragAble', {}).get(wid, {}).get('savename')
                if saveName:
                    savingKey = keys.SET_UI_INFO + '/' + saveName
                    result = AppSettings.get(savingKey + '/hidden', 0)
                    return GfxValue(result)
            else:
                return GfxValue(0)
        else:
            return GfxValue(0)

    def onGetWidgetCanF11(self, *args):
        wid = args[3][0].GetNumber()
        if wid in UWD.data.get('canF11Hide', []):
            return GfxValue(1)
        else:
            return GfxValue(0)

    def onSaveWidgetHidden(self, *args):
        dragAlbeWidgets = UWD.data.get('dragAble', {})
        for wid in dragAlbeWidgets.keys():
            wName = dragAlbeWidgets.get(wid, {}).get('savename')
            if wName:
                hid = ASUtils.getWidgetHidden(wid)
                AppSettings[keys.SET_UI_INFO + '/' + wName + '/hidden'] = int(hid)

    def onGetEnableF11Hide(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableF11Hide', False))

    def getWidgetPos(self, wid):
        pos = self.uiObj.Invoke('getWidgetOffSet', Scaleform.GfxValue(wid))
        return [pos.GetElement(0).GetNumber(), pos.GetElement(1).GetNumber()]

    def onSaveWidgetPos(self, *args):
        wid = args[3][0].GetNumber()
        dragAlbeWidgets = UWD.data.get('dragAble', {})
        if wid in dragAlbeWidgets.keys():
            wName = dragAlbeWidgets.get(wid, {}).get('savename')
            pos = self.getWidgetPos(wid)
            if not int(pos[0]) == -1 and not int(pos[1]) == -1:
                AppSettings[keys.SET_UI_INFO + '/' + wName + '/pos/x'] = int(pos[0])
                AppSettings[keys.SET_UI_INFO + '/' + wName + '/pos/y'] = int(pos[1])
            innerScreenSize = 1.0
            if hasattr(BigWorld, 'getInnerScreenSize'):
                innerScreenSize = BigWorld.getInnerScreenSize()
            w, h = [ x / innerScreenSize for x in BigWorld.windowSize() ]
            if AppSettings.get(keys.SET_UI_SAVEPOS_WIDTH, -1) != int(w) or AppSettings.get(keys.SET_UI_SAVEPOS_HEIGHT, -1) != int(h):
                self.saveAllDragWidgetPos()

    def saveAllDragWidgetPos(self, *arg):
        dragAlbeWidgets = UWD.data.get('dragAble', {})
        for wid in dragAlbeWidgets.keys():
            wName = dragAlbeWidgets.get(wid, {}).get('savename')
            if wName:
                pos = self.getWidgetPos(wid)
                if not int(pos[0]) == -1 and not int(pos[1]) == -1:
                    AppSettings[keys.SET_UI_INFO + '/' + wName + '/pos/x'] = int(pos[0])
                    AppSettings[keys.SET_UI_INFO + '/' + wName + '/pos/y'] = int(pos[1])

        innerScreenSize = 1.0
        if hasattr(BigWorld, 'getInnerScreenSize'):
            innerScreenSize = BigWorld.getInnerScreenSize()
        w, h = [ x / innerScreenSize for x in BigWorld.windowSize() ]
        AppSettings[keys.SET_UI_SAVEPOS_WIDTH] = int(w)
        AppSettings[keys.SET_UI_SAVEPOS_HEIGHT] = int(h)

    def resetSavePosWidget(self, *arg):
        dragAlbeWidgets = UWD.data.get('dragAble', {})
        for wid in dragAlbeWidgets.keys():
            wName = dragAlbeWidgets[wid].get('savename')
            if wName:
                AppSettings[keys.SET_UI_INFO + '/' + wName + '/pos/x'] = int(-1)
                AppSettings[keys.SET_UI_INFO + '/' + wName + '/pos/y'] = int(-1)

        AppSettings[keys.SET_UI_SAVEPOS_WIDTH] = int(-1)
        AppSettings[keys.SET_UI_SAVEPOS_HEIGHT] = int(-1)
        AppSettings.save()

    def onSetScaleData(self, *arg):
        scale = arg[3][0].GetNumber()
        mode = arg[3][1].GetNumber()
        toplogoScale = arg[3][3].GetNumber()
        chatScale = arg[3][4].GetNumber()
        AppSettings[keys.SET_UI_SCALEDATA_SCALE] = scale
        AppSettings[keys.SET_UI_SCALEDATA_MODE] = mode
        AppSettings[keys.SET_UI_SCALEDATA_TOPLOGO] = toplogoScale
        AppSettings[keys.SET_UI_SCALEDATA_CHAT] = chatScale

    def onGetScaleData(self, *arg):
        result = [AppSettings.get(keys.SET_UI_SCALEDATA_SCALE, 1.0), 1]
        return uiUtils.array2GfxAarry(result)

    def onGetWidgetDragable(self, *arg):
        wid = int(arg[3][0].GetNumber())
        return GfxValue(wid in uiConst.DRAGABLE_WIDGETS or ULD.data.get(wid, {}).get('dragAble', False))

    def onGetLayoutDict(self, *arg):
        return uiUtils.dict2GfxDict(ULD.data)

    def reloadUI(self):
        self.uiObj.Invoke('reloadUI')

    def initPushMsgCallback(self):
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_TRADE, {'click': self.tradeRequest.show,
         'refresh': self.tradeRequest.refresh})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_BIND_ITEM_TRADE, {'click': self.bindItemTrade.showRequest,
         'refresh': self.bindItemTrade.refreshRequest})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GET_REWARD, {'click': self.activityPush.show,
         'refresh': self.activityPush.refresh})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GET_ACHIEVE_REWARD, {'click': self.achievePush.show,
         'refresh': self.achievePush.refresh})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GET_CARNIVAL_REWARD, {'click': self.carnivalPush.show,
         'refresh': self.carnivalPush.refresh})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GET_FESTIVAL_REWARD, {'click': self.festivalPush.show,
         'refresh': self.festivalPush.refresh})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_APPLY_TEAM, {'click': self.team.showApply,
         'refresh': self.team.refreshApply})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_APPLY_TEAM_WITH_NON_GROUP, {'click': self.team.showApplyWithNonGroup,
         'refresh': self.team.refreshApplyWithNonGroup,
         'timeout': self.team.applyWithNonGroupTimeOut})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ARENA_MATCHED, {'click': self.arena.clickPushIcon})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_BF_MATCHED, {'click': self.battleField.clickPushIcon})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ADD_ENEMY, {'click': self.addEnemy.show,
         'refresh': self.addEnemy.refresh})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WS_LVL_UP, {'click': self.skill.wsExpPushClick})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WS_SKILL_LVL_UP_100, {'click': Functor(self.skill.wsProficiencyPushClick, uiConst.MESSAGE_TYPE_WS_SKILL_LVL_UP_100)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GET_EQUIP, {'click': self.equipPush.pushShow,
         'refresh': self.equipPush.refresh})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_FEEDBACK, {'click': self.feedback.clickPushIcon})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_YING_XIAO_FEEDBACK, {'click': self.yingXiaoFeedback.clickPushIcon})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GROUP_MATCHED, {'click': self.teamComm.clickPushIcon})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_APPLY, {'click': self.guildMember.clickApplyPush})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_CLAN_WAR_RESULT, {'click': self.clanWar.onResultPushClick})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_CHATROOM, {'click': self.chatRoomWindow.clickPushIcon})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_MANUAL_LV_UP, {'click': self.roleInfo.clickManualLvUpPush})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_RIDE_TOGETHER, {'click': self.skill.cancelRideTogether})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GET_GUILD_MATCH_ITEM, {'click': self.guildActivity.showMatchItem})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_BE_MENTOR, {'click': Functor(self.mentor.showMentorLetter, uiConst.MENTOR_LETTER_BAISHI)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_BE_APPRENTICE, {'click': Functor(self.mentor.showMentorLetter, uiConst.MENTOR_LETTER_SHOUTU)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_DISMISS_MENTOR_RELATION, {'click': self.mentor.showDismissMsg})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_LATENCY, {'click': self.showLatencyMsg})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SPC_GMT_HELP_PUSH, {'click': self.help.clickPushHelp})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SPC_GMT_NOTICE_PUSH, {'click': self.pushNotice.clickPushNotice})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ACTIVITY_QUEST, {'click': self.questLog.onClickActivityQuestPush})
        self.pushMessage.setCallBack(uiConst.MESSAGE_MAX_NOVICE_HINT, {'click': self.onClickCheckPlayerNovie})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_KEJU_PUZZLE, {'click': self.puzzle.kejuPuzzlePushClick})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_WUXING, {'click': self.clickWuXingPushNotice})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION1, {'click': self.clickCompensation1})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION2, {'click': self.clickCompensation2})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_CALL, {'click': self.clickCallFriendPush})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_NO_BID, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_NO_BID)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_APPLY_TARGET, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_APPLY_TARGET)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_MATCH_FAIL, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_MATCH_FAIL)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_MATCH_SUCC, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_MATCH_SUCC)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_BID_END, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_BID_END)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_BATTLE_QUEUE, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_BATTLE_QUEUE)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_QUEUE, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_QUEUE)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_BATTLE_YOUNG_QUEUE, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_BATTLE_YOUNG_QUEUE)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_ROB_YOUNG_QUEUE, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_ROB_YOUNG_QUEUE)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_ROB_QUEUE, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_ROB_QUEUE)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_BATTLE_OLD_QUEUE, {'click': Functor(self.worldWar.clickPush, uiConst.MESSAGE_TYPE_WW_BATTLE_OLD_QUEUE)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_DASHAN, {'click': self.daShan.show})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_BATTLE_STATE_APPLY, {'click': Functor(self.worldWar.clickWWBattlePush, uiConst.MESSAGE_TYPE_WW_BATTLE_STATE_APPLY)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_BATTLE_STATE_OPEN, {'click': Functor(self.worldWar.clickWWBattlePush, uiConst.MESSAGE_TYPE_WW_BATTLE_STATE_OPEN)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_ARMY_VOTE_NOTIFY, {'click': Functor(self.worldWar.clickWWArmyVotePush, uiConst.MESSAGE_TYPE_WW_ARMY_VOTE_NOTIFY)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_ARMY_VOTE_RESULT_NOTIFY, {'click': Functor(self.worldWar.clickWWArmyVotePush, uiConst.MESSAGE_TYPE_WW_ARMY_VOTE_RESULT_NOTIFY)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_BONUS, {'click': self.showPushData})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_ARMY_MARK_NOTIFY, {'click': self.worldWar.clickWWArmyMarkPush})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_BATTLE_RESULT_NOTIFY, {'click': Functor(self.worldWar.clickWWBattleResultPush, uiConst.MESSAGE_TYPE_WW_BATTLE_RESULT_NOTIFY)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_BATTLE_RESULT_NOTIFY_OLD, {'click': Functor(self.worldWar.clickWWBattleResultPush, uiConst.MESSAGE_TYPE_WW_BATTLE_RESULT_NOTIFY_OLD)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WW_BATTLE_RESULT_NOTIFY_YOUNG, {'click': Functor(self.worldWar.clickWWBattleResultPush, uiConst.MESSAGE_TYPE_WW_BATTLE_RESULT_NOTIFY_YOUNG)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_APPLY_SOLE_MENTOR, {'click': Functor(self.mentorEx.onApplySoleClick, uiConst.MESSAGE_TYPE_APPLY_SOLE_MENTOR)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_DISMISS_SOLE, {'click': Functor(self.mentorEx.onApplySoleClick, uiConst.MESSAGE_TYPE_DISMISS_SOLE)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_APPLY_SOLE_APPRENTICE, {'click': Functor(self.mentorEx.onApplySoleClick, uiConst.MESSAGE_TYPE_APPLY_SOLE_APPRENTICE)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_APPLY_GRADUATE, {'click': self.mentorEx.onClickGraduateExPush})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_APPRENTICE_QULIFICATION_EX, {'click': self.mentorEx.onClickApprenticeQulificationEx})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_MENTOR_QULIFICATION_EX, {'click': self.mentorEx.onClickMentorQulificationEx})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_GROUP_DUEL_START, {'click': Functor(self.arenaPlayoffs.onClickPlayoffsPush, uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_GROUP_DUEL_START)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_GROUP_DUEL_END, {'click': Functor(self.arenaPlayoffs.onClickPlayoffsPush, uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_GROUP_DUEL_END)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_FINAL_DUEL_START, {'click': Functor(self.arenaPlayoffs.onClickPlayoffsPush, uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_FINAL_DUEL_START)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_FINAL_DUEL_END, {'click': Functor(self.arenaPlayoffs.onClickPlayoffsPush, uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_FINAL_DUEL_END)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_GROUP_DUEL_START, {'click': Functor(self.arenaPlayoffs.onClickPlayoffsPush, uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_GROUP_DUEL_START)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_GROUP_DUEL_END, {'click': Functor(self.arenaPlayoffs.onClickPlayoffsPush, uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_GROUP_DUEL_END)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_FINAL_DUEL_START, {'click': Functor(self.arenaPlayoffs.onClickPlayoffsPush, uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_FINAL_DUEL_START)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_FINAL_DUEL_END, {'click': Functor(self.arenaPlayoffs.onClickPlayoffsPush, uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_FINAL_DUEL_END)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_LIFE_SKILL_LV_UP, {'click': self.clickLifeSkillLvUp})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PUSH_INIMACY_YEARLY_REWARD, {'click': self.friend.clickIntimacyRewardPushIcon})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_LOW_LV_FREE_SCHOOL_TRANSFER, {'click': self.schoolTransferSelect.clickLowLvFreePush})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_ROBBER_ACTIVITY_OPEN, {'click': self.guildRobberActivityPush.clickActivityOpenPush})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_ROBBER_ACTIVITY_END, {'click': self.guildRobberActivityPush.clickActivityEndPush})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ACHIEVEMENT_SHARE, {'click': self.qrCodeShareAchievement.show})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_TEAM_SSC_START, {'click': self.teamSSCMsgBox.clickConfirmMsg,
         'timeout': self.teamSSCMsgBox.confirmEnterTimeout})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_TEAM_SSC_ROUND_WIN, {'click': self.teamSSCMsgBox.clickRoundWinMsg,
         'timeout': self.teamSSCMsgBox.leaveTimeout})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_TEAM_SSC_INVITE_APPLY, {'click': self.teamSSCMsgBox.clickInviteApplyMsg,
         'timeout': self.teamSSCMsgBox.inviteApplyTimeout})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_AUCTION_GUILD_OPEN, {'click': Functor(self.guildAuction.show, uiConst.GUILD_AUCTION_TAB_GUILD)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_AUCTION_WORLD_OPEN, {'click': Functor(self.guildAuction.show, uiConst.GUILD_AUCTION_TAB_WORLD)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_OFFLINE_INCOME, {'click': Functor(self.offlineIncome.show, gametypes.OFFLINE_INCOME_OP_GUILD_DISMISS)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_CONSIGN_BID_REFEND, {'click': Functor(self.offlineIncome.show, gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_BID_REFEND)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_CONSIGN_PROFIT, {'click': Functor(self.offlineIncome.show, gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_PROFIT)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WORLD_CONSIGN_BID_REFEND, {'click': Functor(self.offlineIncome.show, gametypes.OFFLINE_INCOME_OP_WORLD_CONSIGN_BID_REFEND)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_CONSIGN_DESTORY_REFEND, {'click': Functor(self.offlineIncome.show, gametypes.OFFLINE_INCOME_OP_GUILD_CONSIGN_DESTORY_REFEND)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_RED_PACKET, {'click': self.guildRedPacketHistory.show})
        self.pushMessage.setCallBack(uiConst.MESSAGE_NEW_SERVER_REWARD_PUSH, {'click': Functor(self.newServiceActivities.show, gameglobal.rds.ui.newServiceActivities.getTheFirstShowTabIndex())})
        self.teamInviteV2.setPushMsgCallback()
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WING_WORLD_ANIM, {'click': self.wingWorld.onClickPushMsg})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ACHVEMENT_WEEK_AWARD, {'click': self.achvment.show})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_QUIZZES_GIVE_COIN, {'click': Functor(self.offlineIncome.show, gametypes.OFFLINE_INCOME_OP_QUIZZES_BIND_COIN)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_WING_WORLD_CONSIGN_PROFIT, {'click': Functor(self.offlineIncome.show, gametypes.OFFLINE_INCOME_OP_COUNTRY_CONSIGN_PROFIT)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_CBG_GET_COIN, {'click': Functor(self.offlineIncome.show, gametypes.OFFLINE_INCOME_OP_CBG_ROLE)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_SCHOOL_TOP_COIN, {'click': Functor(self.offlineIncome.show, gametypes.OFFLINE_INCOME_OP_SCHOOL_TOP_LUCKY_BAG)})
        self.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ENTER_WING_WOLRD_XINMO_ARENA, {'click': self.onClickEnterWingWorldXinmoArena})

    def onClickEnterWingWorldXinmoArena(self):
        p = BigWorld.player()
        p.onClickEnterWingWorldXinmoArena()

    def clickLifeSkillLvUp(self):
        gameglobal.rds.ui.lifeSkillNew.show()
        self.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_LIFE_SKILL_LV_UP)

    def showPushData(self):
        data = self.pushMessage.getLastData(uiConst.MESSAGE_TYPE_PUSH_BONUS).get('rewardList', [])
        self.pushBonus.addRewardData(data)
        self.pushBonus.show()

    def clickCallFriendPush(self):
        gameglobal.rds.ui.callBackMessageBox.show()

    def clickWuXingPushNotice(self):
        msg = GMD.data.get(GMDD.data.WUXING_GET_MSG, {}).get('text', gameStrings.TEXT_UIADAPTER_2679)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.roleInfo.onTraceRoad, gameStrings.TEXT_LIFESKILLNEWPROXY_1103, Functor(self.closeWuXingMsg), gameStrings.TEXT_AVATAR_6426_1)

    def closeWuXingMsg(self):
        self.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_WUXING)

    def clickCompensation1(self):
        if gameglobal.rds.configData.get('enalbeGetCompensationFromGUI', False) and not self.itemQuestV2.isCompInfoEmpty():
            self.itemQuestV2.show(uiConst.ITEM_QUEST_V2_TYPE_COMPENSATION_GBID, 0, 0, 0)
            return
        msg = GMD.data.get(GMDD.data.MESSAGE_TYPE_PUSH_COMPENSATION1, {}).get('text', gameStrings.TEXT_UIADAPTER_2689)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.traceRoad, SCD.data.get('MESSAGE_TYPE_PUSH_COMPENSATION1', '')), gameStrings.TEXT_LIFESKILLNEWPROXY_1103, Functor(self.closeCompensation1), gameStrings.TEXT_AVATAR_6426_1)

    def clickCompensation2(self):
        if gameglobal.rds.configData.get('enalbeGetCompensationFromGUI', False) and not self.itemQuestV2.isCompInfoEmpty():
            self.itemQuestV2.show(uiConst.ITEM_QUEST_V2_TYPE_COMPENSATION, 0, 0, 0)
            return
        msg = GMD.data.get(GMDD.data.MESSAGE_TYPE_PUSH_COMPENSATION2, {}).get('text', gameStrings.TEXT_UIADAPTER_2689)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.traceRoad, SCD.data.get('MESSAGE_TYPE_PUSH_COMPENSATION1', '')), gameStrings.TEXT_LIFESKILLNEWPROXY_1103, Functor(self.closeCompensation2), gameStrings.TEXT_AVATAR_6426_1)

    def traceRoad(self, seekid):
        uiUtils.findPosById(str(seekid))

    def closeCompensation1(self, compId = None):
        p = BigWorld.player()
        if not compId or not hasattr(p, 'compInfo') or len(p.compInfo) == 0:
            self.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION1)
        else:
            lastData = self.getPushMsgCompDataById(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION1, compId)
            if lastData:
                self.pushMessage.removeData(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION1, lastData)
            else:
                self.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION1)

    def closeCompensation2(self, compId = None):
        p = BigWorld.player()
        if not compId or not hasattr(p, 'compInfo') or len(p.compInfo) == 0:
            self.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION2)
        else:
            lastData = self.getPushMsgCompDataById(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION2, compId)
            if lastData:
                self.pushMessage.removeData(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION2, lastData)
            else:
                self.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PUSH_COMPENSATION2)

    def getPushMsgCompDataById(self, widgetId, compId):
        datalist = self.pushMessage.getDataList(widgetId)
        for item in datalist:
            if item and item['data'] and item['data'][4] == compId:
                return item

    def onClickCheckPlayerNovie(self):
        p = BigWorld.player()
        if gameglobal.rds.loginManager.serverMode() != gametypes.SERVER_MODE_NOVICE:
            uiUtils.getTextFromGMD(GMDD.data.ENHANCE_PROP_FAILED_COFIRM)
            return
        arr = []
        if p.lv >= gameglobal.rds.configData.get('noviceServerMaxPlayerLv'):
            arr.append(gameStrings.TEXT_UIADAPTER_2740)
        if p.socLv >= gameglobal.rds.configData.get('noviceServerMaxSocLv'):
            arr.append(gameStrings.TEXT_UIADAPTER_2743)
        if p.qumoExp >= gameglobal.rds.configData.get('noviceServerMaxQuMo'):
            arr.append(gameStrings.TEXT_UIADAPTER_2746)
        if p.totalJunJie >= gameglobal.rds.configData.get('noviceServerMaxJunJie'):
            arr.append(gameStrings.TEXT_UIADAPTER_2749)
        txt = gameStrings.TEXT_CHATPROXY_403.join(arr)
        if txt:
            hintTxt = uiUtils.getTextFromGMD(GMDD.data.NOVICE_SERVER_MAX_HINT, '%s') % txt
            gameglobal.rds.ui.messageBox.showMsgBox(hintTxt)

    def addNoviceHintPushMessage(self):
        p = BigWorld.player()
        if gameglobal.rds.loginManager.serverMode() != gametypes.SERVER_MODE_NOVICE:
            return
        if p.lv >= gameglobal.rds.configData.get('noviceServerMaxPlayerLv') or p.socLv >= gameglobal.rds.configData.get('noviceServerMaxSocLv') or p.qumoExp >= gameglobal.rds.configData.get('noviceServerMaxQuMo') or p.totalJunJie >= gameglobal.rds.configData.get('noviceServerMaxJunJie'):
            self.pushMessage.addPushMsg(uiConst.MESSAGE_MAX_NOVICE_HINT)

    def showLatencyMsg(self):
        p = BigWorld.player()
        data = self.pushMessage.getLastData(uiConst.MESSAGE_TYPE_LATENCY)
        self.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_LATENCY)
        p.showGameMsg(GMDD.data.UU_PUSH_MSG, data.get('latencyTime', 0))

    def showCurve(self, arr, curveType):
        BigWorld.callback(0.2, Functor(self._doShowCurve, arr, curveType))

    def _doShowCurve(self, arr, curveType):
        if not self.systemButton.mediator:
            return
        elif not self.uiObj:
            return
        else:
            if curveType == uiConst.ITEM_TO_INVENTORY:
                pos = self._getInventoryIconPos()
            elif curveType == uiConst.ITEM_TO_TEAMBAG:
                pos = self._getTeamBagIconPos()
            elif curveType == uiConst.ITEM_TO_DICEPANEL:
                pos = self._getDicePanelPos()
            elif curveType == uiConst.ITEM_TO_QUESTTRACK:
                pos = self._getQuestTrackPos()
            elif curveType == uiConst.ITEM_TO_AUCTION:
                pos = self._getAuctionPanelPos()
            ret = []
            for item in arr:
                iconPath = uiUtils.getItemIconFile40(item[2])
                midPos = self._getMiddlePos([item[0], item[1]], pos)
                ret.append([item[0],
                 item[1],
                 midPos[0],
                 midPos[1],
                 pos[0],
                 pos[1],
                 iconPath])

            ret = uiUtils.array2GfxAarry(ret)
            t = [0.5, 0.5]
            if self.params[2] != None:
                t[0] = self.params[2]
            if self.params[2] != None:
                t[1] = self.params[3]
            param = uiUtils.array2GfxAarry(t)
            self.uiObj.Invoke('showCurve', (ret, param))
            return

    def _getInventoryIconPos(self):
        if not self.systemButton.mediator:
            return None
        else:
            sysWidget = self.systemButton.mediator.Invoke('getWidget')
            x = sysWidget.GetMember('x').GetNumber()
            y = sysWidget.GetMember('y').GetNumber()
            iconX = sysWidget.GetMember('inventoryBtn').GetMember('x').GetNumber()
            iconY = sysWidget.GetMember('inventoryBtn').GetMember('y').GetNumber()
            return [x + iconX, y + iconY]

    def _getTeamBagIconPos(self):
        x, y = self._getInventoryIconPos()
        if self.teamComm.teamPlayerMed != None:
            teamBagIcon = self.teamComm.teamPlayerMed.Invoke('getWidget')
            x = teamBagIcon.GetMember('x').GetNumber()
            y = teamBagIcon.GetMember('y').GetNumber()
        return [x, y]

    def _getDicePanelPos(self):
        x, y = self._getInventoryIconPos()
        if self.assign.diceMediator != None:
            dicePanel = self.assign.diceMediator.Invoke('getWidget')
            if dicePanel and dicePanel.GetMember('x') != None:
                x = dicePanel.GetMember('x').GetNumber()
                y = dicePanel.GetMember('y').GetNumber()
        return [x, y]

    def _getQuestTrackPos(self):
        questTrack = self.questTrack.mediator.Invoke('getWidget')
        x = questTrack.GetMember('x').GetNumber()
        y = questTrack.GetMember('y').GetNumber()
        return [x, y + 100]

    def _getAuctionPanelPos(self):
        x, y = self._getInventoryIconPos()
        if self.assign.auctionMediator != None:
            auctionPanel = self.assign.auctionMediator.Invoke('getWidget')
            x = auctionPanel.GetMember('x').GetNumber()
            y = auctionPanel.GetMember('y').GetNumber()
        return [x, y]

    def _getMiddlePos(self, staPos, endPos):
        x = staPos[0]
        y = staPos[1] - 100
        if self.params[0] != None:
            x = endPos[0] - math.sqrt(math.fabs((endPos[0] - staPos[0]) * self.params[0]))
        if self.params[1] != None:
            y = (math.sqrt(math.fabs((endPos[1] - staPos[1]) * self.params[0])) - endPos[1]) * self.params[1]
        return [x, staPos[1] + y]

    def showSpecialCurve(self, itemList):
        pos = self._getInventoryIconPos()
        if not pos:
            return
        itemArr = []
        for itemId in itemList:
            itemArr.append([pos[0] - 70, pos[1] - 80, itemId])

        self.showCurve(itemArr, uiConst.ITEM_TO_INVENTORY)

    def setCurParams(self, a, b, t1, t2):
        self.params = [a,
         b,
         t1,
         t2]

    def onAfterCurve(self, *arg):
        p = BigWorld.player()
        if p.groupAssignWay == const.GROUP_ASSIGN_FREE:
            self.systemButton.showIndicator()

    def sendLink(self, msg):
        topIndex = 0
        groupChatRoom = None
        appenInputMsgFunc = None
        if gameglobal.rds.ui.chatToFriend.hasChatToFriend():
            med = gameglobal.rds.ui.chatToFriend.getTopMediator()
            if med:
                widget = ASObject(med).getWidget()
                index = widget.parent.getChildIndex(widget)
                if index > topIndex:
                    topIndex = index
                    appenInputMsgFunc = Functor(gameglobal.rds.ui.chatToFriend.appenInputMsg, msg)
        if gameglobal.rds.ui.groupChat.widget:
            widget = gameglobal.rds.ui.groupChat.widget
            index = widget.parent.getChildIndex(widget)
            if index > topIndex:
                topIndex = index
                appenInputMsgFunc = Functor(gameglobal.rds.ui.groupChat.appenInputMsg, msg)
        if gameglobal.rds.ui.groupChatRoom.widgetMaps:
            index, widget = gameglobal.rds.ui.groupChatRoom.getTopChatPanelWidget()
            if index > topIndex:
                appenInputMsgFunc = Functor(gameglobal.rds.ui.groupChatRoom.appenInputMsg, widget, msg)
        if appenInputMsgFunc:
            appenInputMsgFunc()
        elif gameglobal.rds.ui.booth.boothRecord:
            gameglobal.rds.ui.booth.setChatText(msg)
        else:
            gameglobal.rds.ui.chat.setChatText(msg)

    def _reloadClass(self, fileName):
        cls = self._getClsName(fileName)
        game.reloadClass(globals()[cls])

    def refreshUICode(self):
        map(self._reloadClass, self.proxyList)

    def showFishGroupTips(self, x, y, title, distance):
        self.uiObj.Invoke('showFishGroupTips', (GfxValue(x),
         GfxValue(y),
         GfxValue(gbk2unicode(title)),
         GfxValue(gbk2unicode(distance))))

    def hideFishGroupTips(self):
        self.uiObj.Invoke('hideFishGroupTips')

    def showCursorForActionPhysics(self):
        p = BigWorld.player()
        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            p.ap.restore(False)

    def hideCursorForActionPhysics(self):
        if not gameglobal.gIsAppActive:
            return
        if self.fullscreenFittingRoom.mediator:
            return
        p = BigWorld.player()
        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            if gameglobal.isWidgetNeedShowCursor:
                return
            if hasattr(p, 'ap'):
                BigWorld.player().ap.showCursor = False
                BigWorld.player().ap.reset()

    def isWidgetNeedShowCursor(self):
        widgetIds = SCD.data.get('needShowCursorWidgetIds', ())
        isAnyWidgetShowing = self.isAnyWidgetShowing(widgetIds)
        return isAnyWidgetShowing

    def getAimVisible(self):
        ret = self.uiObj.Invoke('getAimVisible', ())
        return ret.GetBool()

    def isAnyWidgetShowing(self, widgetIds):
        """widgetIds\xe4\xb8\xad\xe4\xbb\xbb\xe6\x84\x8fwidget\xe6\x98\xbe\xe7\xa4\xba\xe5\x8d\xb3\xe8\xbf\x94\xe5\x9b\x9etrue"""
        ret = self.uiObj.Invoke('isAnyWidgetShowing', uiUtils.array2GfxAarry(widgetIds))
        return ret.GetBool()

    def showAimCross(self, x, y, dis, type, isAim = True, color = 'red', lock = False):
        self.uiObj.Invoke('showAimCross', (GfxValue(x),
         GfxValue(y),
         GfxValue(dis),
         GfxValue(type),
         GfxValue(isAim),
         GfxValue(color),
         GfxValue(lock)))

    def setAimCrossPos(self, x, y, dis, type = None, isAim = True, color = 'red', lock = False):
        if type:
            self.uiObj.Invoke('setAimCrossPos', (GfxValue(x),
             GfxValue(y),
             GfxValue(dis),
             GfxValue(type),
             GfxValue(isAim),
             GfxValue(color),
             GfxValue(lock)))
        else:
            nullObj = GfxValue(1)
            nullObj.SetNull()
            self.uiObj.Invoke('setAimCrossPos', (GfxValue(x),
             GfxValue(y),
             GfxValue(dis),
             nullObj,
             GfxValue(isAim),
             GfxValue(color),
             GfxValue(lock)))

    def playAimLock(self, isAim = True, color = 'red', lockAim = True):
        self.uiObj.Invoke('playAimLock', (GfxValue(isAim), GfxValue(color), GfxValue(lockAim)))

    def hideAimCross(self, isAim = True, isGray = False):
        self.uiObj.Invoke('hideAimCross', (GfxValue(isAim), GfxValue(isGray)))

    def hideOptionalAimCross(self):
        self.uiObj.Invoke('hideAimCross', GfxValue(False))

    def showTargetDir(self, x, y, dis, direct):
        self.uiObj.Invoke('showTargetDir', (GfxValue(x),
         GfxValue(y),
         GfxValue(dis),
         GfxValue(direct)))

    def setAimCrossBuff(self, path, isAim, isGray = False):
        gfxPath = uiUtils.array2GfxAarry(path)
        self.uiObj.Invoke('setAimCrossBuff', (gfxPath, GfxValue(isAim), GfxValue(isGray)))

    def showIme(self, show):
        self.uiObj.Invoke('showIme', GfxValue(show))

    def showScreenUI(self, path, stopFrame, location = True, offsetH = 0, offsetV = 0):
        self.uiObj.Invoke('showSwfAni', (GfxValue(path),
         GfxValue(stopFrame),
         GfxValue(location),
         GfxValue(offsetH),
         GfxValue(offsetV)))

    def setImePos(self, x, y):
        self.uiObj.Invoke('setImePos', (GfxValue(x), GfxValue(y)))

    def hideTargetDir(self):
        self.uiObj.Invoke('hideTargetDir')

    def delTopLogo(self):
        ent = BigWorld.entities.values()
        for e in ent:
            if hasattr(e, 'topLogo') and e.topLogo:
                e.topLogo.release()
                e.topLogo = utils.MyNone

    def addTopLogo(self):
        ent = BigWorld.entities.values()
        for e in ent:
            e.topLogo = topLogo.TopLogo(e.id)

    def countTopLogo(self):
        i = 0
        ent = BigWorld.entities.values()
        for e in ent:
            if hasattr(e, 'topLogo') and e.topLogo:
                i = i + 1

    def removeTopLogo(self):
        i = 0
        ent = BigWorld.entities.values()
        for e in ent:
            if hasattr(e, 'topLogo') and e.topLogo:
                e.topLogo.release()
                e.topLogo = None
                i = i + 1

    def testAddTopLogo(self):
        for i in xrange(50):
            topLogo.TopLogoManager.getInstance().addTopLogo(i)

    def testdelTopLogo(self):
        for i in xrange(50):
            topLogo.TopLogoManager.getInstance().removeTopLogo(i)

    def refreshQuestIcon(self, charTypes, isShow):
        arr = ''
        for ent in BigWorld.entities.values():
            if (ent.IsMonster or ent.IsSummonedBeast) and ent.charType in charTypes:
                arr += str(ent.id) + ',' + str(int(isShow)) + '&'
                if ent.topLogo:
                    ent.topLogo.setGuiStateChange(True)

        topLogo.TopLogoManager.getInstance().refreshQuestIcon(arr[:-1])

    def createUIPosInfo(self):
        ret = {'typeA': {},
         'typeB': {},
         'typeC': {}}
        for typeKey, typeVal in self.posArr.items():
            for key, value in typeVal.items():
                curPos = self.getWidgetPos(key)
                if self.diffUIPos(typeKey, key, curPos):
                    ret[typeKey][key] = curPos

        return ret

    def recordInitPos(self):
        ID_TYPE_A = [uiConst.WIDGET_LITTLE_MAP,
         uiConst.WIDGET_ITEMBAR,
         uiConst.WIDGET_TASK_TRACKING,
         uiConst.WIDGET_PUSH_MESSSAGES,
         uiConst.WIDGET_FUBEN_TARGET,
         uiConst.WIDGET_FUBEN_ONE_RESULT,
         uiConst.WIDGET_FUBEN_TOTAL_RESULT,
         uiConst.WIDGET_ITEMBAR2]
        ID_TYPE_B = [uiConst.WIDGET_CHAT_LOG, uiConst.WIDGET_COMM_TEAM_PLAYER]
        ID_TYPE_C = [uiConst.WIDGET_FUBEN_CLOCK,
         uiConst.WIDGET_ARENA_STATS,
         uiConst.WIDGET_ARENA_TMP_RESULT,
         uiConst.WIDGET_ARENA_ENEMY_TEAM,
         uiConst.WIDGET_PLAYER_UF]
        typeA = {item:self.getWidgetPos(item) for item in ID_TYPE_A}
        typeB = {item:self.getWidgetPos(item) for item in ID_TYPE_B}
        typeC = {item:self.getWidgetPos(item) for item in ID_TYPE_C}
        self.posArr = {'typeA': typeA,
         'typeB': typeB,
         'typeC': typeC}

    def diffUIPos(self, type, widgetId, pos):
        if math.fabs(self.posArr[type][widgetId][0] - pos[0]) > 10 or math.fabs(self.posArr[type][widgetId][1] - pos[1]) > 10:
            return True
        return False

    def endQTE(self, id):
        if id in QTED.data:
            self.inQTE = False
            qteData = QTED.data[id]
            if qteData.get('hideUI', 0):
                self.setQTEHideUI(False)
            type = qteData['type']
            if self.QTECallbackId:
                BigWorld.cancelCallback(self.QTECallbackId)
                self.QTECallbackId = None
            if type == uiConst.QTE_TPYE_CORRECT and id == gameglobal.rds.ui.correctQte.qteId:
                gameglobal.rds.ui.correctQte.hide()
            elif type == uiConst.QTE_TPYE_EXACT and id == gameglobal.rds.ui.exactQte.qteId:
                gameglobal.rds.ui.exactQte.hide()
            elif type == uiConst.QTE_TPYET_ACCUMULATE and id == gameglobal.rds.ui.accumulateQte.qteId:
                gameglobal.rds.ui.accumulateQte.hide()

    def enterQTE(self, id):
        if id in QTED.data:
            self.inQTE = True
            qteData = QTED.data[id]
            if qteData.get('hideUI', 0):
                self.setQTEHideUI(True)
            type = qteData['type']
            delayTime = qteData.get('delayTime', 0)
            if type == uiConst.QTE_TPYE_CORRECT:
                self.QTECallbackId = BigWorld.callback(delayTime, Functor(gameglobal.rds.ui.correctQte.show, id))
            elif type == uiConst.QTE_TPYE_EXACT:
                self.QTECallbackId = BigWorld.callback(delayTime, Functor(gameglobal.rds.ui.exactQte.show, id))
            elif type == uiConst.QTE_TPYET_ACCUMULATE:
                self.QTECallbackId = BigWorld.callback(delayTime, Functor(gameglobal.rds.ui.accumulateQte.show, id))

    def setQTEHideUI(self, QTEHideUI):
        if self.QTEHideUI != QTEHideUI:
            self.QTEHideUI = QTEHideUI
            if self.QTEHideUI:
                self.hideAllUI()
            else:
                self.restoreUI()

    def testQuestNpc(self):
        self.openQuestWindow(uiConst.NPC_QUEST)
        BigWorld.callback(2, self.closeQuestNpc)

    def closeQuestNpc(self):
        self.closeQuestWindow()
        self.testQuestNpc()

    def onGetScreenDPI(self, *arg):
        dpi = 96
        if hasattr(BigWorld, 'getScreenDPI'):
            dpi = BigWorld.getScreenDPI()[0]
        return GfxValue(dpi)

    def onGetBonusDict(self, *arg):
        return uiUtils.dict2GfxDict(SCD.data.get('bonusDict', {}), True)

    def onLinkClick(self, *args):
        txt = ui.unicode2gbk(args[3][1].GetString())
        btnIdx = args[3][2].GetNumber()
        gamelog.debug('@zhp onLickClick', txt)
        self.doLinkClick(txt, btnIdx)

    def doLinkClick(self, txt, btnIdx):
        gamelog.info('jbx:txt, id', txt, btnIdx)
        try:
            p = BigWorld.player()
            if txt.startswith('uiShow'):
                eval('self.' + txt[len('uiShow:'):])
            elif txt.startswith('seek'):
                seekId = txt[len('seek') + 1:]
                if ',' in seekId:
                    seekId = '(%s)' % seekId
                uiUtils.findPosWithAlert(seekId)
            elif txt.startswith('http'):
                BigWorld.openUrl(txt)
            elif txt.startswith('findPos'):
                pos = txt[len('findPos') + 1:].split(',')
                if len(pos) == 4:
                    if p.canPathFindingWingWorld(int(pos[0]), False):
                        from helpers import wingWorld
                        wingWorld.pathFinding((float(pos[1]),
                         float(pos[2]),
                         float(pos[3]),
                         int(pos[0])), endDist=0.5, showMsg=False, fromGroupFollow=False)
                    else:
                        navigator.getNav().pathFinding((float(pos[1]),
                         float(pos[2]),
                         float(pos[3]),
                         float(pos[0])), None, None, True, 0.5)
            elif txt.startswith('cclink'):
                if self.isLowPerformace():
                    msg = SCD.data.get('ccLowPerformanceMsg', gameStrings.TEXT_UIADAPTER_3154)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doAnalysisCCLink, txt[6:]))
                else:
                    msg = SCD.data.get('ccNormalPerformanceMsg', gameStrings.TEXT_UIADAPTER_3157)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doAnalysisCCLink, txt[6:]))
            elif txt.startswith('swfpath'):
                swfpath = txt[7:]
                self.flash.show(swfpath)
            elif txt.startswith('sec_ask'):
                self.help.queryText(txt[len('sec_ask') + 1:], True, True)
            elif txt.startswith('qustionTxt'):
                self.help.setQuestionText(txt[len('qustionTxt') + 1:])
            elif txt.startswith('addFriend'):
                friendName = txt[len('addFriend') + 1:]
                hostId = 0
                if '_' in friendName:
                    friendName, hostId = friendName.split('_')
                if friendName.isdigit():
                    menuManager.getInstance().menuTarget.apply(gbId=long(friendName), hostId=int(hostId), menuId=0)
                else:
                    menuManager.getInstance().menuTarget.apply(roleName=friendName, hostId=int(hostId), menuId=0)
                menuManager.getInstance().addFriend()
            elif txt.startswith('notifyMLDoubleExp'):
                tExpire = BigWorld.player().vipBasicPackage.get('tExpire', 0)
                if tExpire and tExpire > utils.getNow():
                    totalTime = gameglobal.rds.ui.expBonus.getTotalRemainTime()
                    if totalTime > 0 and gameglobal.rds.ui.expBonus.isFreezed:
                        msg = GMD.data.get(GMDD.data.CONFIRM_TO_UNFREEZE_EXP_BONUS, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_79) % utils.formatTimeStr(totalTime, gameStrings.TEXT_EXPBONUSPROXY_79_1)
                        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.unfreezeExpBonusVip)
                    else:
                        gameglobal.rds.ui.expBonus.show(0, 10001, True)
                else:
                    gameglobal.rds.ui.tianyuMall.showVipTab()
            elif txt.startswith('shareZone-'):
                prefix, gbId, hostId = txt.split('-')
                gbId = int(gbId)
                hostId = int(hostId)
                p.getPersonalSysProxy().openZoneOther(gbId, None, const.PERSONAL_ZONE_SRC_LINK, hostId)
            elif txt.startswith('shareMoment-'):
                prefix, momentId = txt.split('-')
                self.personalZoneMoment.show(int(momentId))
            elif txt.startswith('shareHome-'):
                txtList = txt.split('-')
                if len(txtList) == 3:
                    txtList.append('0')
                prefix, roleName, gbId, hostId = txt.split('-')
                gbId = int(gbId)
                hostId = int(hostId)
                msg = gameStrings.MSG_TELEPORT_HOME % roleName
                self.messageBox.showYesNoMsgBox(msg, Functor(p.visitRoom, gbId, roleName, hostId))
            elif txt.startswith('marriageInvitation-'):
                prefix, mNUID, customMessage = txt.split('-')
                gameglobal.rds.ui.marryInvitationCard.openInvitationCard(mNUID, customMessage)
            elif txt.startswith('marriageUpgradePackage'):
                self.marrySettingBg.switchToUpgradePlan()
            elif txt.startswith('marriageHallGotoWorld'):
                p.cell.leaveMarriageHall()
            elif txt.startswith('marriagePackageSet'):
                p.cell.setMarriagePackageInfoApply()
            elif txt.startswith('shareZiXun-'):
                prefix, index, url = txt.split('-')
                self.ziXunInfo.show(int(index), {}, url)
            elif txt.startswith('openZoneByName'):
                _roleName = str(txt[14:])
                p.getPersonalSysProxy().openZoneOther(None, _roleName)
            elif txt.startswith('homeApartmentSeek'):
                seekId = int(txt[17:])
                uiUtils.findPosById(seekId)
                gameglobal.rds.ui.messageBox.dismiss()
            elif txt.startswith('guildRecruit'):
                nuid = int(txt[12:])
                p.cell.applyGuildJoin(nuid)
            elif txt.startswith('baishi'):
                name = txt[6:]
                menuManager.getInstance().menuTarget.apply(roleName=name)
                menuManager.getInstance().baishi()
            elif txt.startswith('shoutu'):
                name = txt[6:]
                menuManager.getInstance().menuTarget.apply(roleName=name)
                menuManager.getInstance().shoutu()
            elif txt.startswith('menuName'):
                if ',' in txt:
                    roleName, gbId, menuId, hostId = txt[len('menuName') + 1:].split(',')
                else:
                    roleName = txt[len('menuName')]
                    gbId = 0
                    menuId = 1
                    hostId = 0
                if btnIdx == uiConst.RIGHT_BUTTON:
                    self.showUserLinkMenu(roleName, int(gbId), int(hostId), int(menuId))
                elif btnIdx == uiConst.LEFT_BUTTON:
                    gameglobal.rds.ui.systemSingleTip.privateChat(roleName)
            elif txt.startswith('inviteGuild'):
                roleName = txt[11:]
                p.cell.inviteGuildMember(roleName)
            elif txt.startswith('webWuPinSearch'):
                self.useWebWuPinSearch()
            elif txt.startswith('naviMapPos'):
                posStr = txt[10:]
                posX, posY, posZ, mapName = posStr.split(',')
                spaceNo = formula.getMapId(p.spaceNo)
                if spaceNo != const.SPACE_NO_BIG_WORLD:
                    BigWorld.player().showGameMsg(GMDD.data.MAP_NOT_IN_BIG_WORLD, ())
                    return
                heightArray = (400, 300, 200, 100, 75, 50, 25)
                pos = (float(posX), float(posY), float(posZ))
                if pos[1] == navigator.UNKNOWN_Y:
                    for h in heightArray:
                        pos = BigWorld.findDropPoint(p.spaceID, Math.Vector3(pos[0], h, pos[2]))
                        if pos:
                            pos = pos[0]
                            break

                if p.life != gametypes.LIFE_DEAD:
                    ret = navigator.getNav().pathFinding((pos[0],
                     pos[1],
                     pos[2],
                     spaceNo), None, None, True, 0.5)
                    if ret == 1:
                        p.topLogo.setAutoPathingVisible(True)
            elif txt.startswith('welcomeNewMemberOfGuild'):
                newMemberStr = txt[len('welcomeNewMemberOfGuild'):]
                newMemberId, newMemberName = newMemberStr.split('_')
                p = BigWorld.player()
                p.cell.welcomeNewMember(int(newMemberId), newMemberName)
            elif txt.startswith('modelFitting'):
                nuid = long(txt[12:])
                BigWorld.player().cell.getFittingRoomItemDetail(nuid, '')
            elif txt.startswith('applyTeam'):
                name = txt[len('applyTeam'):]
                menuManager.getInstance().menuTarget.apply(roleName=name)
                menuManager.getInstance().applyTeam()
            elif txt.startswith('inviteTeam'):
                name = txt[len('inviteTeam'):]
                menuManager.getInstance().menuTarget.apply(roleName=name)
                menuManager.getInstance().inviteTeam()
            elif txt.startswith('singleChat'):
                name = txt[len('singleChat') + 1:]
                gameglobal.rds.ui.chat.updateChatTarge(name)
                gameglobal.rds.ui.chat.setCurChannel(const.CHAT_CHANNEL_SINGLE, '', True)
            elif txt.startswith('ret'):
                retCode = txt[len('ret'):]
                p.base.chatToItem(long(retCode), 'chat')
            elif txt.startswith('item'):
                pos = txt.find(':')
                if pos == -1:
                    itemId = txt[4:]
                    it = Item(int(itemId), 1, False)
                else:
                    itemId = txt[4:pos]
                    it = Item(int(itemId), 1, False)
                    itdata = txt[pos + 1:].split(':')
                    for i in range(0, len(itdata), 2):
                        attrv = itdata[i + 1]
                        if attrv.isdigit():
                            attrv = int(attrv)
                        setattr(it, itdata[i], attrv)

                gfxTipData = gameglobal.rds.ui.inventory.GfxToolTip(it)
                self.chat.showTooltip(const.CHAT_TIPS_ITEM, gfxTipData)
            elif txt.startswith('achv'):
                self.chat.showTooltip(const.CHAT_TIPS_ACHIEVEMENT, self.chat.achieveToolTip(txt[4:]))
            elif txt.startswith('friendLink'):
                friendName = txt[len('friendLink') + 1:]
                gameglobal.rds.ui.friend.chatToPlayer(friendName)
            elif txt.startswith('shareLive'):
                eval('self.arenaChallengeReview.show' + txt[len('shareLive:'):])
            elif txt.startswith('goGuildSceneViaGbId:'):
                gbIdStr = txt[len('goGuildSceneViaGbId:'):]
                p = BigWorld.player()
                if utils.isGbId(gbIdStr):
                    if long(gbIdStr) == p.gbId:
                        p.showGameMsg(GMDD.data.GUILD_ENTER_SCENE_CAN_NOT_VIA_SELF, ())
                    else:
                        p.cell.queryPlayerPosViaGbId(long(gbIdStr))
            elif txt.startswith('goGuildSceneViaPos:'):
                pos = txt[len('goGuildSceneViaPos:'):].split(',')
                if len(pos) == 4:
                    p = BigWorld.player()
                    p.onGetPlayerPositionInGuildScene(pos[0], (pos[1], pos[2], pos[3]))
            elif txt.startswith('uiId:'):
                uiId = int(txt.replace('uiId:', ''))
                self.loadWidget(uiId)
            elif txt[:10] == 'skillShare':
                p = BigWorld.player()
                rawMsg = txt[10:].split('hostId')
                skillPlayerName = rawMsg[0]
                hostId = int(rawMsg[1])
                if hostId != utils.getHostId():
                    p.showGameMsg(GMDD.data.SKILL_SHARE_NOT_AVALIABLE_CROSS, ())
                    return
                p.querySkillInfoByChat(skillPlayerName)
            elif txt[:8] == 'hieShare':
                p = BigWorld.player()
                rawMsg = txt[8:].split('hostId')
                skillPlayerName = rawMsg[0]
                hostId = int(rawMsg[1])
                if hostId != utils.getHostId():
                    p.showGameMsg(GMDD.data.HIEROGRAM_SHARE_NOT_AVALIABLE_CROSS, ())
                    return
                p.queryHierogramInfoByChat(skillPlayerName)
            elif txt.startswith('taunt:'):
                gbId = long(txt[len('taunt:'):])
                gameglobal.rds.ui.systemSingleTip.taunt(gbId)
            elif txt.startswith('congrats:'):
                gbId = long(txt[len('congrats:'):])
                gameglobal.rds.ui.systemSingleTip.congrats(gbId)
            elif txt.startswith('privateChat:'):
                name, gbId = txt[len('privateChat:'):].split(',')
                if btnIdx == uiConst.RIGHT_BUTTON:
                    menuData = gameglobal.rds.ui.systemSingleTip.getMenuData(name, gbId)
                    return uiUtils.dict2GfxDict({'menuData': menuData}, True)
                if btnIdx == uiConst.LEFT_BUTTON:
                    gameglobal.rds.ui.systemSingleTip.privateChat(name)
            elif txt.startswith('watchNativeGt:'):
                gtInfo = txt[len('watchNativeGt:'):]
                guildNUID, subGroupId = gtInfo.split('_')
                p = BigWorld.player()
                p.cell.enterGuildTournamentWithLive(int(subGroupId), long(guildNUID))
            elif txt.startswith('spriteBioToFuben:'):
                spriteId, bioId = txt[len('spriteBioToFuben:'):].split(',')
                isUnlock = gameglobal.rds.ui.summonedWarSpriteBiography.checkSpritePreBioIdsUnlock(int(spriteId), int(bioId))
                p = BigWorld.player()
                if isUnlock:
                    p.cell.applySpriteBioFuben(int(spriteId), int(bioId))
                else:
                    p.showGameMsg(GMDD.data.SPRITE_PRE_BIOIDS_UNLOCKED, ())
            elif txt.startswith('exploreSpriteHelp:'):
                gbId, index, itemId, itemNum, groupId, time, roleName = txt[len('exploreSpriteHelp:'):].split(',')
                p = BigWorld.player()
                p.cell.exploreSpriteHelpItem(int(gbId), int(index), int(itemId), int(itemNum), int(groupId), int(time), const.EXPLORE_SPRITE_HELP_CHECK, roleName)
            elif txt.startswith('wingWorldXinMoAnnal:'):
                roundNo, matchNo = txt[len('wingWorldXinMoAnnal:'):].split(',')
                p.base.queryWingWorldXinMoAnnal(int(roundNo), int(matchNo))
            elif txt.startswith('wingWorldXinMoUniqueBossAnnal:'):
                p.base.queryWingWorldXinMoUniqueBossAnnal()
            elif txt.startswith('gotoww'):
                gameglobal.rds.ui.wingWorldOverView.handleGotoWWLink()
            elif txt.startswith('dArenaCheer'):
                argStr = txt[len('dArenaCheer') + 1:]
                p.doCheer(argStr)
            elif txt.startswith('dArenaInviteMate'):
                p.inviteDoubleArenaMate()
            elif txt.startswith('applyFightForLove'):
                roleName, tOccupy, activityNUID = txt[len('applyFightForLove:'):].split(',')
                msg = FFLCD.data.get('applyConfirmMsg', '')
                readyTime = FFLCD.data.get('readyTime', 0)
                remainTime = max(readyTime + int(tOccupy), 0)
                nowTime = utils.getNow()
                if nowTime < remainTime:
                    _remainTime = gameStrings.FIGHT_FOR_LOVE_START_TIME % tuple(utils.formatDatetime(remainTime).split()[1].split(':'))

                    def applyFunc():
                        nowTime = utils.getNow()
                        if nowTime < remainTime:
                            p.cell.applyFightForLove(long(activityNUID))
                        else:
                            p.showGameMsg(GMDD.data.FFL_APPLY_FAILED_ALREADY_END, ())

                    msg = msg % (roleName, _remainTime)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(applyFunc))
                else:
                    p.showGameMsg(GMDD.data.FFL_APPLY_FAILED_ALREADY_END, ())
            elif txt.startswith('observeFightForLove'):
                activityNUID = txt[len('observeFightForLove:'):]
                msg = FFLCD.data.get('observeFightForLoveConfirm', '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.observeFightForLove, long(activityNUID)))
            elif txt.startswith('gotohbz'):
                gameglobal.rds.ui.guildInherit.handleGotoNPC()
            elif txt.startswith('schoolTopTest'):
                p.enterSchoolTopTest()
            elif txt.startswith('dPlayoffsCheer'):
                argStr = txt[len('dPlayoffsCheer') + 1:]
                p.doPlayoffsCheer(argStr)
            elif txt.startswith('guildMembersFbWatchWar'):
                guildNUID, fbNo = txt[len('guildMembersFbWatchWar:'):].split(',')
                p.cell.applyObverseGuildFuben(int(guildNUID), int(fbNo))
            elif txt.startswith('clanChallengeOb'):
                fortId, hostId = txt[len('clanChallengeOb:'):].split(',')
                p.cell.startObserveClanWarChallenge(int(fortId), int(hostId))
            elif txt.startswith('showPlayoffsReport'):
                gameglobal.rds.ui.arenaPlayoffs.showPlayoffsReport()
            elif txt.startswith('applyForFuben'):
                fubenId = int(txt[len('applyForFuben') + 1:])
                name = FD.data.get(fubenId, {}).get('name', '')
                primaryLevelName = FD.data.get(fubenId, {}).get('primaryLevelName', '')
                if primaryLevelName:
                    name = ''.join((name, gameStrings.COMMON_DIAN, primaryLevelName))
                modeName = FD.data.get(fubenId, {}).get('modeName', '')
                if modeName:
                    name = ''.join((name,
                     '(',
                     modeName,
                     ')'))
                msg = gameStrings.PLAYRECOMM_ENTER_FUBEN_CONFIRM % name
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.applyForFuben, fubenId), gameStrings.COMMON_CONFIRM)
        except Exception as e:
            msg = 'Exception in doLinkClick, txt:%s, btnIdx:%d, error:%s' % (str(txt), btnIdx, e.message)
            BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})

    def showUserLinkMenu(self, roleName, gbId, hostId, menuId):
        menuManager.getInstance().menuTarget.apply(roleName=roleName, gbId=long(gbId), hostId=int(hostId))
        menuData = menuManager.getInstance().getMenuListById(int(menuId))
        MenuManager.getInstance().showMenuByData(None, menuData)

    def useWebWuPinSearch(self):
        item = None
        if gameglobal.rds.ui.equipChangeJuexingRebuild.panelMc:
            item = gameglobal.rds.ui.equipChangeJuexingRebuild.getSelectItem()
        elif gameglobal.rds.ui.equipChangePrefixRebuild.panelMc:
            item = gameglobal.rds.ui.equipChangePrefixRebuild.getRebuildItem()
        elif gameglobal.rds.ui.equipChangePrefixTransfer.panelMc:
            item = gameglobal.rds.ui.equipChangePrefixTransfer.getTransferItem(0)
        if item and item.id:
            url = SCD.data.get('WEB_WUPIN_SEARCH', uiConst.WEB_WUPIN_SEARCH) % item.id
        else:
            url = SCD.data.get('WEB_INDEX_SEARCH', uiConst.WEB_INDEX_SEARCH)
        BigWorld.openUrl(url)

    def isLowPerformace(self):
        try:
            info = BigWorld.getPerformanceInfo()
            if not info:
                return False
            corenum = info.get('corenum', None)
            if corenum and int(corenum) <= SCD.data.get('lowPerformaceCoreNum', 2):
                return True
            availmem = info.get('availmem', None)
            phymem = info.get('phymem', None)
            if availmem and phymem and float(availmem) / float(phymem) < SCD.data.get('lowPerformaceAvailMem', 0.2):
                return True
            totalcpu = info.get('totalcpu', None)
            if totalcpu and float(totalcpu) > SCD.data.get('lowPerformaceTotalcpu', 80):
                return True
        except:
            return False

        return False

    def doAnalysisCCLink(self, roomId):
        if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            gamelog.debug('doAnalysisCCLink', roomId)
            if roomId.find('unknown') != -1:
                if getattr(gameglobal.rds, 'micCardRetCode', -1) == 0:
                    roomId, channelId = uiUtils.getCCRoom()
                else:
                    roomId, channelId = uiUtils.getDefaultCCRoom()
                roomId = '%d-%d' % (roomId, channelId)
                cc.joinRoom(roomId, '', None)
        else:
            BigWorld.player().doAnalysisLink(roomId)

    def setTopLogoFontSize(self, size):
        topLogo.TopLogoManager.getInstance().setFontSize(size)

    def setManualScale(self, scale, mode):
        self.uiObj.Invoke('setManualScale', (GfxValue(scale), GfxValue(mode)))
        self.saveAllDragWidgetPos(None)

    def onWidgetAdded(self, *arg):
        widgetId = int(arg[3][0].GetNumber())
        if widgetId == uiConst.WIDGET_LOADING:
            self.onTopWidgetChanged()
        elif widgetId == uiConst.WIDGET_PUSH_MESSAGES_V2:
            gameglobal.rds.ui.pushMessage.dragDataChanged()
        if gameglobal.rds.configData.get('enableUIProfile', False):
            self.profile.endLoadWidget(widgetId, arg[3][1])

    def onWidgetRemoved(self, *arg):
        widgetId = int(arg[3][0].GetNumber())
        widgetIds = SCD.data.get('needShowCursorWidgetIds', ())
        if widgetId in widgetIds:
            gameglobal.isWidgetNeedShowCursor = self.isWidgetNeedShowCursor()
            if self.showCursorAfterWidget:
                self.showCursorAfterWidget = False
            else:
                self.hideCursorForActionPhysics()
        if hasattr(gameglobal.rds, 'tutorial'):
            gameglobal.rds.tutorial.onUnloadWidget(widgetId)
        self.onTopWidgetChanged()

    def onSlotMouseOver(self, *arg):
        key = arg[3][0].GetString()
        if key.startswith('actionbar'):
            gameglobal.rds.ui.actionbar.onSlotMouseOver(*arg)
        elif key.startswith('airbar'):
            gameglobal.rds.ui.airbar.onSlotMouseOver(*arg)
        elif key.startswith('zaiJuV2'):
            gameglobal.rds.ui.zaijuV2.onSlotMouseOver(*arg)

    def onSlotMouseOut(self, *arg):
        key = arg[3][0].GetString()
        if key.startswith('actionbar'):
            gameglobal.rds.ui.actionbar.onSlotMouseOut(*arg)
        elif key.startswith('airbar'):
            gameglobal.rds.ui.airbar.onSlotMouseOut(*arg)
        elif key.startswith('zaiJuV2'):
            gameglobal.rds.ui.zaijuV2.onSlotMouseOut(*arg)

    def clearState(self):
        nowState = ui.get_cursor_state()
        gameglobal.rds.ui.inventory.clearState()
        gameglobal.rds.ui.roleInfo.clearState()
        gameglobal.rds.ui.guildStorage.clearState()
        state_arr = [ui.SIGNEQUIP_STATE,
         ui.RENEWAL_STATE,
         ui.IDENTIFY_ITEM_STATE,
         ui.ADD_STAR_EXP_STATE,
         ui.IDENTIFY_MANUAL_EQUIP_STATE,
         ui.CANCEL_ABILITY_STATE,
         ui.CANCEL_ABILITY_NODE_STATE,
         ui.CHANGE_BIND_STATE,
         ui.RENEWAL_STATE2,
         ui.RESET_FASHION_PROP,
         ui.ITEM_SEARCH_STATE]
        if ui.get_cursor_state() in state_arr:
            ui.reset_cursor()
        endState = ui.get_cursor_state()
        gameglobal.rds.ui.roleInfo.updateSlotState()
        if nowState != endState:
            return True
        else:
            return False

    def saveWidgetState(self, widgetId, pos):
        v = '%s_%s' % (int(pos[0]), int(pos[1]))
        k = keys.SET_SAVE_UI_STATE + '/widget_%s' % int(widgetId)
        if AppSettings.get(k, '') != v:
            AppSettings[k] = v

    def getWidgetState(self, widgetId):
        return AppSettings.get(keys.SET_SAVE_UI_STATE + '/widget_%s' % int(widgetId), '-1_-1')

    def checkStateAndLoad(self, wid, showByUser = False):
        if wid in uiConst.SAVE_WIDGET_STATE_AFTER_CLOSE:
            if showByUser:
                self.saveWidgetState(wid, (-1, -1))
            elif not self.getWidgetState(wid) == '-1_-1':
                return
        self.loadWidget(wid)

    def onSetCursor(self, *arg):
        cursorUp = arg[3][0].GetString()
        cursorDown = ''
        if len(arg[3]) > 1:
            cursorDown = arg[3][1].GetString()
        ui.set_cursor(cursorUp, cursorDown)

    def onGetFaceSizes(self, *arg):
        sizes = SCD.data.get('faceSizes')
        if sizes:
            return uiUtils.dict2GfxDict(sizes)

    def onSetEditFlag(self, *arg):
        flag = arg[3][0].GetBool()
        self.bInEdit = flag

    def onGotoTrackPlace(self, *arg):
        seekId = int(arg[3][0].GetNumber())
        uiUtils.gotoTrack(seekId)
        gameglobal.rds.uiLog.addFlyLog(seekId)

    def onGetHelpData(self, *args):
        helpId = int(args[3][0].GetNumber())
        data = UHD.data.get(helpId, {})
        txt = data.get('text', '')
        if txt:
            sType = data.get('type', 1)
            if sType == uiConst.HELPICON_TYPE_WEB_WUPIN_SEARCH:
                linkTxt = 'webWuPinSearch'
            elif sType == uiConst.HELPICON_TYPE_OPEN_URL:
                linkTxt = data.get('url', '')
            elif sType == uiConst.HELPICON_TYPE_OPEN_UI:
                linkTxt = 'uiId:%d' % data.get('uiId', 0)
            elif sType == uiConst.HELPICON_TYPE_OPEN_ACTIVITY_TIP:
                linkTxt = ''
            else:
                linkTxt = 'uiShow:help.show(\"%s\")' % data.get('keyword', '')
            txt = uiUtils.toHtml(txt, linkEventTxt=linkTxt)
        result = {'tip': data.get('tip', ''),
         'text': txt}
        return uiUtils.dict2GfxDict(result, True)

    def onShowHelpByKey(self, *args):
        targetMc = ASObject(args[3][0])
        helpId = int(args[3][1].GetNumber())
        self.showHelpByKey(helpId, targetMc)

    def showHelpByKey(self, helpId, targetMc = None):
        data = UHD.data.get(helpId, {})
        sType = data.get('type', 1)
        if sType == uiConst.HELPICON_TYPE_SPRITE:
            keyWord = data.get('keyword', '')
            if keyWord:
                if keyWord.find('@fbName') != -1:
                    p = BigWorld.player()
                    fbName = formula.whatFubenName(p.mapID)
                    keyWord = keyWord.replace('@fbName', fbName)
                self.help.show(keyWord)
        elif sType == uiConst.HELPICON_TYPE_BAODIAN:
            page = data.get('pagePos', (0, 0, 0))
            self.baoDian.show(page)
        elif sType == uiConst.HELPICON_TYPE_DFW_ROOM:
            lineNo = data.get('lineNo')
            if lineNo:
                self.daFuWeng.showVideoDesc(lineNo)
        elif sType == uiConst.HELPICON_TYPE_WEB_WUPIN_SEARCH:
            self.useWebWuPinSearch()
        elif sType == uiConst.HELPICON_TYPE_OPEN_URL:
            url = data.get('url', '')
            if url:
                BigWorld.openUrl(url)
        elif sType == uiConst.HELPICON_TYPE_OPEN_UI:
            uiId = data.get('uiId', 0)
            if uiId:
                self.loadWidget(uiId)
        elif sType == uiConst.HELPICON_TYPE_OPEN_ACTIVITY_TIP:
            self.showActivityTip(helpId, targetMc)

    def showActivityTip(self, helpId, targetMc):
        if not targetMc:
            return
        widgetMc = targetMc.parent
        prad, seekId, prid, funcType = UHD.data.get(helpId, {}).get('activityTipData', (1, 0, 10001, 2))
        tipData = self.playRecomm.getPlayTipData(prad, seekId, prid, funcType)
        tipsMc = widgetMc.getInstByClsName('Activity_Tip_TipMc')
        widgetMc.addChild(tipsMc)
        tipsMc.name = 'ActivityTipMc'
        tipsMc.x = -100
        tipsMc.y = 0 - tipsMc.bgImage.height
        tipsMc.visible = True
        tipsMc.tipData = tipData
        tipsMc.model = self.playRecomm.getPrModel()
        tipsMc.refMc = widgetMc
        ASUtils.setHitTestDisable(tipsMc, False)
        tipsMc.closeBtn.addEventListener(events.BUTTON_CLICK, self.hideActivityCallback, False, 0, True)
        tipsMc.addEventListener(events.EVENT_HIDE_ACTIVITY_TIP, self.hideActivityCallback, False, 0, True)

    def hideActivityCallback(self, *args):
        gamelog.info('jbx:hideActivityCallback')
        e = ASObject(args[3][0])
        tipsMc = e.currentTarget
        tipsMc.refMc.removeChild(tipsMc)

    def onGetItemDataById(self, *args):
        itemId = int(args[3][0].GetNumber())
        data = uiUtils.getGfxItemById(itemId)
        return uiUtils.dict2GfxDict(data)

    def onGetSkillDataById(self, *args):
        skillId = int(args[3][0].GetNumber())
        data = self.actionbar.getSkillGfxData(skillId)
        return uiUtils.dict2GfxDict(data)

    def onGetJobDataById(self, *args):
        jobId = int(args[3][0].GetNumber())
        data = {}
        data['tip'] = const.SCHOOL_DICT.get(jobId, '')
        data['label'] = uiConst.SCHOOL_FRAME_DESC.get(jobId, '')
        data['width'] = uiConst.INFO_JOB_ICON_SIZE[0]
        data['height'] = uiConst.INFO_JOB_ICON_SIZE[1]
        return uiUtils.dict2GfxDict(data, True)

    def onGetDefaultAim(self, *args):
        p = BigWorld.player()
        if hasattr(p, 'operation'):
            operationMode = p.getSavedOperationMode()
            plus = gameglobal.rds.ui.controlSettingV2.getModePlus(operationMode)
            aimId = p.operation.get(plus, {}).get(gameglobal.PLUS_AIMCROSS_KEY, 0)
            return GfxValue(aimId)
        else:
            return GfxValue(0)

    def changeAimCross(self, aimId):
        self.uiObj.Invoke('changeAimCross', GfxValue(aimId))

    def showHongBao(self, time):
        self.uiObj.Invoke('showHongBao', GfxValue(time))

    def onLoadRemoteImg(self, *args):
        url = unicode2gbk(args[3][0].GetString())
        imgType = int(args[3][1].GetNumber())
        serverId = int(args[3][2].GetNumber())
        if imgType == uiConst.IMG_TYPE_HTTP_IMG:
            directory = const.IMAGES_DOWNLOAD_UI_DIR
            try:
                parseResult = urlparse.urlsplit(url)
                host = parseResult.netloc
                port = parseResult.port if parseResult.port else 80
                path = parseResult.path
                fileName = path.split('/')[-1]
                BigWorld.ayncFileExist(directory + '/' + fileName, Functor(self._downloadFileAfterLocalCheck, url, host, port, path, directory, fileName))
            except:
                self.remoteLoadDoneBack(url, '', False)

        elif imgType == uiConst.IMG_TYPE_NOS_FILE:
            if uiUtils.isDownloadImage(url):
                if not BigWorld.player():
                    return
                p = BigWorld.player()
                if serverId and serverId != int(gameglobal.rds.gServerid):
                    p.downloadCrossNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, url, serverId, gametypes.NOS_FILE_PICTURE, self.onDownloadNosFile, (url,))
                else:
                    p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, url, gametypes.NOS_FILE_PICTURE, self.onDownloadNosFile, (url,))
            else:
                self.uiObj.Invoke('remoteImgLoadDone', (GfxValue(gbk2unicode(url)), GfxValue(url)))
                return

    def _downloadFileAfterLocalCheck(self, url, host, port, path, directory, fileName, isExist):
        if isExist:
            self.remoteLoadDoneBack(url, directory, fileName, True)
        elif hasattr(BigWorld, 'httpDownloadFileNew'):
            BigWorld.httpDownloadFileNew(host, port, path, directory, fileName, Functor(self.remoteLoadDoneBack, url, directory, fileName))
        else:
            BigWorld.httpDownloadFile(host, port, path, directory, fileName, Functor(self.remoteLoadDoneBack, url, directory, fileName))

    def remoteLoadDoneBack(self, url, directory, fileName, feedBack):
        gamelog.debug('@zhp loadDone', feedBack, url, directory, fileName)
        if self.movie:
            if feedBack:
                localFile = '../' + directory + '/' + fileName
            else:
                localFile = 'item/icon64/notFound.dds'
            self.uiObj.Invoke('remoteImgLoadDone', (GfxValue(gbk2unicode(url)), GfxValue(localFile)))

    def onDownloadNosFile(self, status, callbackArgs):
        url = callbackArgs
        if status == gametypes.NOS_FILE_STATUS_APPROVED:
            self.remoteLoadDoneBack(url, const.IMAGES_DOWNLOAD_DIR, url + '.dds', True)
        else:
            BigWorld.callback(0, Functor(self.uiObj.Invoke, 'remoteImgLoadFail', (GfxValue(gbk2unicode(url)), GfxValue(status))))

    def setUIHitEnabled(self, value, force = False):
        if not force and not gameglobal.rds.configData.get('disableUIInActionMode', False):
            return
        if self.uiObj:
            self.uiObj.Invoke('setEnabled', GfxValue(not bool(value)))

    def onGetBonusTip(self, *args):
        ret = {}
        bonusId = args[3][0].GetNumber()
        title = unicode2gbk(args[3][1].GetString())
        fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', ())
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        for i in range(0, len(fixedBonus)):
            ret[i] = tipUtils.getBonusInfo(fixedBonus, i)

        ret['num'] = len(fixedBonus)
        return tipUtils.tmpAttendTips(ret, title)

    def onGetPinYin(self, *args):
        value = unicode2gbk(args[3][0].GetString())
        pinYin = pinyinConvert.strPinyin(value)
        return GfxValue(gbk2unicode(pinYin))

    def onGetMingPaiDataById(self, *args):
        mpId = int(args[3][0].GetNumber())
        mpData = MPD.data.get(mpId, {})
        if mpData:
            data = {'iconPath': uiConst.MING_PAI_ICON_PATH_20 + str(mpData.get('icon', 0)) + '.dds',
             'tip': mpData.get('desc', '')}
            return uiUtils.dict2GfxDict(data, True)

    def onGetWWArmPostById(self, *args):
        postId = args[3][0].GetString()
        camp = 0
        armyData = wingWorldUtils.getNormalWingArmyData()
        if postId.find('-') != -1:
            postId, camp = postId.split('-')
            camp = int(camp)
            if not camp:
                return GfxValue(0)
            armyData = wingWorldUtils.getCampWingArmyData()
        camp = int(camp)
        postId = int(postId)
        postData = armyData.get(postId, {})
        if postData:
            if camp:
                iconPath = postData.get('icon1', 0) if camp == 1 else postData.get('icon2', 0)
                desc = postData.get('desc1', '') if camp == 1 else postData.get('desc2', 0)
            else:
                iconPath = postData.get('icon', 0)
                desc = postData.get('desc', '')
            data = {'iconPath': uiConst.WW_ARMY_POST_ICON_PATH + str(iconPath) + '.dds',
             'tip': desc}
            return uiUtils.dict2GfxDict(data, True)

    def onOpenRedPacket(self, *args):
        packetRichText = unicode2gbk(args[3][0].GetString())
        self.redPacket.clickRedPacket(packetRichText)

    def onGetItemSearchIconData(self, *args):
        data = {}
        data['visible'] = gameglobal.rds.configData.get('enableItemSearchIcon', False)
        data['tip'] = SCD.data.get('itemSearchIconTip', gameStrings.TEXT_UIADAPTER_3887)
        return uiUtils.dict2GfxDict(data, True)

    def onChangeItemSearch(self, *args):
        gameglobal.rds.ui.clearState()
        if ui.get_cursor_state() != ui.ITEM_SEARCH_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.ITEM_SEARCH_STATE)
            ui.set_cursor(cursor.itemSearch)
            ui.lock_cursor()

    def onGetWidgetInfos(self, *args):
        return uiUtils.array2GfxAarry(uiConst.UI_INFO)

    def onRegisterVocieItem(self, *args):
        voiceIcon = args[3][0]
        key = args[3][1].GetString()
        if self.isPlayingVoice:
            if self.isPlayingVoice[1] == key and Sound.isRawfilePlaying(self.isPlayingVoice[2]):
                self.isPlayingVoice[0].GotoAndStop('normal')
                voiceIcon.GotoAndStop('playing')
                self.isPlayingVoice[0] = voiceIcon

    def onClickVoiceItem(self, *args):
        voiceIcon = args[3][0]
        key = args[3][1].GetString()
        player = BigWorld.player()
        player.downloadAudioFile(const.AUDIOS_DOWNLOAD_RELATIVE_DIR, key, gametypes.NOS_FILE_MP3, self.afterVoiceDownloaded, (voiceIcon, key))

    def afterVoiceDownloaded(self, status, mc, key):
        if status != gametypes.NOS_FILE_STATUS_APPROVED:
            return
        path = '%s/%s.mp3' % (const.AUDIOS_DOWNLOAD_DIR, key)
        handle = gameglobal.rds.sound.playRawfileByPath(path)
        oldVoice = self.isPlayingVoice
        if oldVoice:
            oldVoice[0].GotoAndStop('normal')
            BigWorld.cancelCallback(self.isPlayingVoice[3])
        callbackHandle = BigWorld.callback(1, self.checkVoicePlayEnd)
        self.isPlayingVoice = [mc,
         key,
         handle,
         callbackHandle]
        mc.GotoAndStop('playing')

    def checkVoicePlayEnd(self):
        if not self.isPlayingVoice:
            return
        else:
            handle = self.isPlayingVoice[2]
            mc = self.isPlayingVoice[0]
            if not Sound.isRawfilePlaying(handle):
                mc.GotoAndStop('normal')
                self.isPlayingVoice = None
                return
            self.isPlayingVoice[3] = BigWorld.callback(1, self.checkVoicePlayEnd)
            return

    def onTopWidgetChanged(self, *args):
        self.dispatchEvent(events.EVENT_TOP_WIDGET_CHANGED)

    def onIsCacheWid(self, *args):
        if gameglobal.rds.configData.get('enableCacheUI', False):
            wid = int(args[3][0].GetNumber())
            return GfxValue(wid in uiConst.CACHE_WIDGETS)
        return GfxValue(False)

    def onGetString(self, *args):
        strName = unicode2gbk(args[3][0].GetString())
        try:
            value = str(getattr(gameStrings, strName, strName))
        except:
            value = strName

        return GfxValue(gbk2unicode(value))

    def onGetGameConfig(self, *args):
        configKey = unicode2gbk(args[3][0].GetString())
        return GfxValue(gameglobal.rds.configData.get(configKey, False))

    def onGetGroupIdentityType(self, *args):
        targetId = menuManager.getInstance().menuTarget.entityId
        markType = self.getGroupIdentityType(targetId, AppSettings.get(keys.SET_TEAM_TOP_LOGO_MARK, 1))
        return GfxValue(markType)

    def onSelectFriend(self, *args):
        selected = args[3][0].GetBool()
        gbId = long(args[3][1].GetString())
        self.selectFriend.selectFriend(selected, gbId)

    def getGroupIdentityType(self, entId, isHide):
        markType = ''
        try:
            entId = int(entId)
        except:
            entId = 0

        if not self.isGroupIdentityVisible(isHide):
            return ''
        else:
            p = BigWorld.player()
            if p.isInSSCorTeamSSC():
                return ''
            if p.inFightForLoveFb():
                return ''
            if entId:
                ent = BigWorld.entity(entId)
                if ent and getattr(ent, 'IsAvatar', False) and not getattr(ent, 'boothStat', None) == const.BOOTH_STAT_OPEN:
                    groupType = getattr(ent, 'groupType', None)
                    groupHeader = getattr(ent, 'groupHeader', None)
                    numOfTeamMember = getattr(ent, 'numOfTeamMember', None)
                    gbId = getattr(ent, 'gbId', None)
                    if ent.isInTeam():
                        if groupHeader and entId == groupHeader:
                            if ent.numOfTeamMember == const.TEAM_MAX_NUMBER:
                                markType = 'man'
                            else:
                                markType = 'weiman'
                        elif p.isInMyTeam(ent):
                            markType = 'duiyuan'
                    if ent.isInGroup():
                        if groupHeader and entId == groupHeader:
                            markType = 'tuanzhang'
                        elif hasattr(ent, 'gbId') and hasattr(p, 'gbId') and p.isInMyTeam(ent) and groupUtils.isInSameTeam(p.gbId, ent.gbId):
                            markType = 'duiyuan'
                else:
                    markType = ''
            return markType

    def isGroupIdentityVisible(self, isHide):
        p = BigWorld.player()
        enableTeamIdentity = gameglobal.rds.configData.get('enableTeamIdentity', False)
        isInBattleField = formula.spaceInBattleField(p.spaceNo)
        isInArena = formula.spaceInArena(p.spaceNo)
        fbNo = formula.getFubenNo(p.spaceNo)
        isInFuben = formula.spaceInFuben(p.spaceNo)
        if FD.data.get(fbNo, {}).get('numMax', 0) == 5 and isInFuben or not enableTeamIdentity or isInBattleField or not isHide or isInArena or gameglobal.rds.ui.cameraV2.isShow:
            return False
        return True

    def refreshTeamLogoOrIdentity(self, entId):
        ent = BigWorld.entity(entId)
        p = BigWorld.player()
        if ent and getattr(ent, 'topLogo', None) and hasattr(p, 'groupMark'):
            markId = p.groupMark.get(entId, uiConst.MENU_SPECIAL_MARK)
            markFlag = gameglobal.rds.ui.getGroupIdentityType(entId, AppSettings.get(keys.SET_TEAM_TOP_LOGO_MARK, 1))
            ent.topLogo.setTitleEffectHeight()
            if markId == uiConst.MENU_SPECIAL_MARK:
                ent.topLogo.removeTeamLogo()
                if markFlag:
                    ent.topLogo.setTeamIdentity(markFlag)
                else:
                    ent.topLogo.removeTeamIdentity()
            else:
                ent.topLogo.removeTeamIdentity()
                ent.topLogo.setTeamLogo(markId)

    def onGetAllCallBackEvents(self, *args):
        return uiUtils.array2GfxAarry(uiConst.EVENT_CALLBACK_NAMES.keys())

    def onHandleEvent(self, *args):
        proxyName = args[3][0].GetString()
        wid = int(args[3][1].GetNumber())
        eventType = args[3][2].GetString()
        targetName = args[3][3].GetString()
        funcName = uiConst.EVENT_CALLBACK_NAMES.get(eventType)
        if funcName:
            proxy = getattr(self, proxyName, None)
            if proxy:
                realFuncName = funcName % (targetName[0].upper() + targetName[1:])
                func = getattr(proxy, realFuncName, None)
                if func:
                    e = asObject.ASObject(args[3][4])
                    e.__dict__['wid'] = wid
                    func(e)

    def onClickSoundRecordItem(self, *args):
        mc = args[3][0]
        content = args[3][1].GetString()
        key = content.split('@')[0][6:]
        player = BigWorld.player()

        def startPlay():
            asMc = asObject.ASObject(mc)
            if asMc.icon:
                asMc.icon.gotoAndStop('playing')
            if asMc.unReadIcon:
                asMc.unReadIcon.visible = False
            p = BigWorld.player()
            p.addReviewedSoundRecord(key)

        def endPlay():
            asMc = asObject.ASObject(mc)
            if asMc.icon:
                asMc.icon.gotoAndStop('stop')

        player.downloadPlaySound(key, startPlay, endPlay)

    def onGetRedPacketSplitStr(self, *args):
        splitStr = SCD.data.get('redPacketSplit', '_')
        return GfxValue(gbk2unicode(splitStr))

    def onGetIconDataById(self, *args):
        iconType = args[3][0].GetString()
        bonusDict = SCD.data.get('bonusDict')
        data = {}
        data['tip'] = bonusDict.get(iconType)
        return uiUtils.dict2GfxDict(data, True)

    def onGetSpriteIconPath(self, *args):
        spriteId = args[3][0].GetNumber()
        spritePath = uiUtils.getSummonSpriteIconPath(spriteId)
        return GfxValue(gbk2unicode(spritePath))

    def onSoundRecordIsReviewed(self, *args):
        key = args[3][0].GetString().split('@')[0][6:]
        p = BigWorld.player()
        return GfxValue(p.isSoundRecordReviewed(key))

    def onReportClientException(self, *args):
        error = args[3][0].GetString()
        gamelog.info('jbx:reportClientException', error)
        BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [error], 0, {})

    def onLogValidateNow(self, *args):
        logInfo = args[3][0].GetString()
        self.asLogList.append(logInfo)
        if self.lastFrameCount != BigWorld.getCurFrameNum():
            if len(gameglobal.rds.ui.asLogList) >= AS_LOG_WARNING_CNT:
                gamelog.error('jbx: too many validateNow', gameglobal.rds.ui.asLogList)
            gameglobal.rds.ui.asLogList = []
            self.lastFrameCount = BigWorld.getCurFrameNum()

    def screenShot(self, photoName, leftTop = None, bottomRight = None):
        self.screenLeftTop = leftTop
        self.screenBottomRight = bottomRight
        BigWorld.screenShot(photoName, 3, 0)

    def needCutScreen(self):
        if hasattr(self, 'screenLeftTop') and self.screenLeftTop and hasattr(self, 'screenBottomRight') and self.screenBottomRight:
            return (self.screenLeftTop, self.screenBottomRight)
        else:
            return None

    def clearScreenCoord(self):
        self.screenLeftTop = None
        self.screenBottomRight = None

    def setWaterMarkPos(self, position, type = uiConst.WATERMARK_BOTTOM_RIGHT):
        x, y = position
        if type == uiConst.WATERMARK_BOTTOM_LEFT:
            x = x + uiConst.WATERMARK_LOGO_WIDTH + uiConst.WATERMARK_LOGO_OFFSET
            y = y + uiConst.WATERMARK_LOGO_HEIGHT * 0.5 - 2 * uiConst.WATERMARK_LOGO_OFFSET
        elif type == uiConst.WATERMARK_TOP_LEFT:
            x = x + uiConst.WATERMARK_LOGO_WIDTH + uiConst.WATERMARK_LOGO_OFFSET
            y = y + uiConst.WATERMARK_LOGO_HEIGHT + uiConst.WATERMARK_LOGO_OFFSET
        elif type == uiConst.WATERMARK_TOP_RIGHT:
            y = y + uiConst.WATERMARK_HEIGHT + uiConst.WATERMARK_LOGO_OFFSET
        if hasattr(BigWorld, 'setWaterMarkPositionBottomRight'):
            BigWorld.setWaterMarkPositionBottomRight((x, y))

    def hideWaterMark(self):
        self.setWaterMarkPos((-uiConst.WATERMARK_LOGO_WIDTH - uiConst.WATERMARK_LOGO_OFFSET, 0), uiConst.WATERMARK_TOP_LEFT)

    def lazyInitProxy(self):
        if not BigWorld.isPublishedVersion():
            return True
        return clientcom.enableUILazyInit()

    def getWidgetPath(self, uid):
        if self.uiObj:
            return self.uiObj.Invoke('getWidgetPath', GfxValue(uid)).GetString()
        return ''

    def getDragProxy(self, key):
        proxy = self.getDataProxy(key)
        if not proxy and key.count('.') == 2:
            proxyName = key.split('.')[0]
            proxy = getattr(self, proxyName, None)
        return proxy

    def getDragSlotID(self, proxy, key):
        page, index = (0, 0)
        if hasattr(proxy, 'getSlotID'):
            page, index = proxy.getSlotID(key)
        elif proxy and key.count('.') == 2:
            _, page, index = key.split('.')
        return (page, index)

    def getWidgetByID(self, uid):
        if self.uiObj:
            return ASObject(self.uiObj.Invoke('getWidgetByID', GfxValue(uid)))
        else:
            return None
