#Embedded file name: /WORKSPACE/data/entities/client/gameconfigutils.o
import BigWorld
import Scaleform
import gameglobal
import clientcom
from sfx import sfx
import const
import utils
from guis import events
from guis import uiConst
from helpers import ccManager
from helpers import envSDKHelper
from globalFriend import GlobalFriend

def updateClientConfigFromAccount(config):
    if config.has_key('enableMiniClient') and not config['enableMiniClient']:
        import miniclient
        miniclient.disableReport()
    if config.get('enableNewSchoolYeCha', False):
        uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST = uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST_NEW
    if config.get('enablePushMessageV2', False):
        gameglobal.rds.ui.pushMessage = gameglobal.rds.ui.pushMessageV2
    if config.get('enableKeyboardEffect', False):
        hasattr(BigWorld, 'controlKeyboard') and BigWorld.controlKeyboard()
    if config.get('enableEnvSDK', False):
        envSDKHelper.getInstance().initSDK()


def updateClientConfigFromAvatar(config):
    if config.has_key('offMall') or config.has_key('mallUseableMinLv'):
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
        gameglobal.rds.ui.tianyuMall.onUpdateClientCfg()
    elif config.has_key('enableExtendChatBox'):
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
    elif config.has_key('isCCVersion'):
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
        gameglobal.rds.ui.surfaceSettingV2.onUpdateClientCfg()
    elif config.has_key('enableCCBox'):
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
        gameglobal.rds.ui.surfaceSettingV2.onUpdateClientCfg()
    elif config.has_key('enableInventoryLock'):
        gameglobal.rds.ui.surfaceSettingV2.onUpdateClientCfg()
        gameglobal.rds.ui.inventory.onUpdateClientCfg()
    elif config.has_key('enableDelegation'):
        gameglobal.rds.ui.keySettingV2.updateSwitchAndUI()
    elif config.has_key('enableSemantics'):
        gameglobal.rds.ui.surfaceSettingV2.onUpdateClientCfg()
    elif config.has_key('enableYixin'):
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
        if not config['enableYixin']:
            gameglobal.rds.ui.yixinBind.closeWidget()
            gameglobal.rds.ui.yixinRewards.closeWidget()
    elif config.has_key('enableCustomerService'):
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
    elif config.has_key('enableVip'):
        gameglobal.rds.ui.tianyuMall.onUpdateClientCfg()
    elif config.has_key('enableBindItemConvert'):
        gameglobal.rds.ui.inventory.setBindConfig()
    elif config.has_key('enableCrossServerLaba'):
        gameglobal.rds.ui.chat.updatePadChannels()
        if config['enableCrossServerLaba'] == False:
            gameglobal.rds.ui.chat.resetLaba()
    elif config.has_key('enableYuanguLaba'):
        gameglobal.rds.ui.chat.updatePadChannels()
    elif config.has_key('enableNewGuild'):
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GUILD_TUTORIAL_UPDATE)
    elif config.has_key('offCoinMarket'):
        gameglobal.rds.ui.tianyuMall.onUpdateClientCfg()
    elif config.has_key('enableMiniClient'):
        if not config['enableMiniClient']:
            import miniclient
            miniclient.disableReport()
    elif config.has_key('enableYixinImage'):
        if not config['enableYixinImage']:
            gameglobal.rds.ui.yixinImage.closeWidget()
    elif config.has_key('enableCoinConsign'):
        gameglobal.rds.ui.consign.enableCoinConsign()
    elif config.has_key('enableCBG'):
        gameglobal.rds.ui.cbgMain.onUpdateClientCfg()
    elif config.has_key('enableAlipay'):
        gameglobal.rds.ui.easyPay.onUpdateClientCfg('enableAlipay')
    elif config.has_key('enableChargeActivity'):
        gameglobal.rds.ui.easyPay.onUpdateClientCfg('enableChargeActivity')
    elif config.has_key('enableCustomIme'):
        gameglobal.rds.ui.ime.enableIme()
    elif config.has_key('enableUIGCControl'):
        gameglobal.rds.ui.enableUIGCControl()
    elif config.has_key('enableCCShine'):
        gameglobal.rds.ui.topBar.checkTopBarCanShine()
    elif config.has_key('disableUIInActionMode'):
        if not gameglobal.rds.configData.get('disableUIInActionMode'):
            gameglobal.rds.ui.setUIHitEnabled(True, True)
    elif config.has_key('enableActivityStateBonus'):
        gameglobal.rds.ui.player.onUpdateActivityStateBonus()
    elif config.has_key('enableCameraShare'):
        if not gameglobal.rds.configData.get('enableNewCamera', False):
            gameglobal.rds.ui.camera.refreshCameraShare()
        else:
            gameglobal.rds.ui.cameraV2.refreshCameraShare()
    elif config.has_key('enableMonsterBlood'):
        if not gameglobal.rds.configData.get('enableMonsterBlood'):
            gameglobal.rds.ui.monsterBlood.hide()
    elif config.has_key('enableInvSearch'):
        gameglobal.rds.ui.inventory.enableInvSearch()
    elif config.has_key('enableBoothCustom'):
        gameglobal.rds.ui.booth.refreshCustom()
    elif config.has_key('memoryDBRate'):
        try:
            BigWorld.player().saveMemoryDBConfig()
        except:
            pass

    elif config.has_key('enableCollectItem'):
        if not gameglobal.rds.configData.get('enableCollectItem'):
            gameglobal.rds.ui.xinmoRecord.removeXinmoRecordMsg()
    elif config.has_key('enableCollectItemMessagePush'):
        if not gameglobal.rds.configData.get('enableCollectItemMessagePush'):
            gameglobal.rds.ui.crystalDefenceMain.removeNewUpdateMsg()
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ACTIVITY_GUIDE_OPEN)
    elif config.has_key('enableRandomTreasureBagMainMessagePush'):
        if not gameglobal.rds.configData.get('enableRandomTreasureBagMainMessagePush'):
            gameglobal.rds.ui.randomTreasureBagMain.removeNewUpdateMsg()
    elif config.has_key('enableLuckyLottery'):
        if not gameglobal.rds.configData.get('enableLuckyLottery'):
            gameglobal.rds.ui.activitySaleLuckyLottery.removeLuckylotteryPushMsg()
            gameglobal.rds.ui.activitySale.refreshInfo()
    elif config.has_key('enableAssEmployerPush'):
        if not gameglobal.rds.configData.get('enableAssEmployerPush'):
            gameglobal.rds.ui.assassinationTombstone.removeNewUpdateMsg()
    elif config.has_key('enableUnbindEquip'):
        if not gameglobal.rds.configData.get('enableUnbindEquip', False):
            gameglobal.rds.ui.inventory.disableUnBind()
    elif config.has_key('enableDisassembleEquip'):
        if not gameglobal.rds.configData.get('enableDisassembleEquip', False):
            gameglobal.rds.ui.inventory.disableDisassemble()
    elif config.has_key('enableAppearanceRank'):
        gameglobal.rds.ui.friend.friendsScoInfo = {}
    elif config.has_key('enableActivityHallIcon'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    elif config.has_key('enableRewardGiftActivityIcons'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    elif config.has_key('enableActivitySale'):
        gameglobal.rds.ui.activitySale.refreshInfo()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    elif config.has_key('enableDailyWelfareActivityOptimize'):
        gameglobal.rds.ui.activitySale.refreshInfo()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    elif config.has_key('enableNewbiePay'):
        gameglobal.rds.ui.activitySale.refreshInfo()
        gameglobal.rds.ui.activitySaleNewbiePay.refreshInfo()
    elif config.has_key('enableWelfare'):
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
        gameglobal.rds.ui.welfare.refreshInfo()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        gameglobal.rds.ui.topBar.refreshActivityIcon()
    elif config.has_key('enableNewRewardHall'):
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
    elif config.has_key('enableGuideGoal'):
        gameglobal.rds.ui.topBar.refreshActivityIcon()
        gameglobal.rds.ui.welfare.refreshInfo()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    elif config.has_key('enableAward'):
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
    elif config.has_key('enableGuildTutorialNew'):
        gameglobal.rds.ui.questTrack.updateGuildTutorialLoader()
    elif config.has_key('enableNewSchoolYeCha'):
        gameglobal.rds.ui.pvpEnhance.refreshInfo()
    elif config.has_key('enableSummonedSprite'):
        if config.get('enableSummonedSprite'):
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.show()
        else:
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.hide()
    elif config.has_key('enableExcitementClientShow'):
        gameglobal.rds.ui.excitementIcon.refreshInfo()
    elif config.has_key('enableQuestLoopChain'):
        gameglobal.rds.ui.questTrack.showFindBeastTrack(False)
        if config.get('enableQuestLoopChain'):
            gameglobal.rds.ui.findBeastRecover.pushFindBeastRecoverMsg()
        else:
            gameglobal.rds.ui.findBeastRecover.removeFindBeastRecoverMsg(True)
        gameglobal.rds.ui.playRecommActivation.refreshRecomm(uiConst.PLAY_RECOMMV2_TAB_DAILY_ACTIVITY_SUB_TAB)
    elif config.has_key('enableMissTianyu'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    elif config.has_key('enableHpMpPool'):
        gameglobal.rds.ui.player.resetHpMpPool()
    elif config.has_key('enableIMOptimize'):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FRIEND_V2)
        gameglobal.rds.ui.friend.hide()
    elif config.has_key('enableWeekActivation') or config.has_key('enableWeekPrivilegeBuy'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        gameglobal.rds.ui.activitySale.refreshInfo()
    elif config.has_key('enableNewServerTopRankAct') or config.has_key('enableNewServerGuildPrestige'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        if gameglobal.rds.ui.newServerTopRankMain.widget:
            gameglobal.rds.ui.newServerTopRankMain.updateInfo()
    if config.get('enableGlobalFriend', False):
        p = BigWorld.player()
        if not hasattr(p, 'globalFriends'):
            p.globalFriends = GlobalFriend.createInstance({'groupInfo': {},
             'friends': {}})
    if config.has_key('enableLoginReward'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    if config.has_key('enableSecretChannel'):
        gameglobal.rds.ui.chat.refreshChannel()
        gameglobal.rds.ui.chat.updatePadChannels()
    if config.has_key('enableCrossClanWarLaba'):
        gameglobal.rds.ui.chat.refreshChannel()
        gameglobal.rds.ui.chat.updatePadChannels()
    if config.has_key('enableHallOfFame'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    if config.has_key('enableGatherInputCache'):
        enableGatherInputCache = config.get('enableGatherInputCache', -1)
        if hasattr(BigWorld, 'setEnableGatherInputCacheNew'):
            if enableGatherInputCache <= 0:
                BigWorld.setEnableGatherInputCacheNew(False)
            else:
                import gametypes
                if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
                    BigWorld.setEnableGatherInputCacheNew(True)
                    BigWorld.setGatherInputTime(enableGatherInputCache)
    if config.has_key('enableHideHallOfFameBtn'):
        gameglobal.rds.ui.celebrityRank.updateHofLock()
    if config.has_key('enableHallOfFameDisableTabBtn'):
        gameglobal.rds.ui.celebrityRank.updateFameTabBtnState(not config.get('enableHallOfFameDisableTabBtn', False))
    if config.has_key('enableGuildConsign'):
        gameglobal.rds.ui.guildAuctionGuild.updateOpenPushMsg()
    if config.has_key('enableWorldConsign'):
        gameglobal.rds.ui.guildAuctionWorld.updateOpenPushMsg()
    if hasattr(BigWorld, 'enableReportASError'):
        enableReportASError = config.get('enableReportASError', False)
        if not BigWorld.isPublishedVersion():
            BigWorld.enableReportASError(enableReportASError)
    if config.has_key('enableBuffListener'):
        gameglobal.rds.ui.buffListenerShow.refreshInfo()
    if config.has_key('enablePYQ'):
        gameglobal.rds.ui.topBar.onUpdateClientCfg()
    if config.has_key('enableFlowbackGroup'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    if config.has_key('enableDeepLearningDataApply'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    if config.has_key('enableFriendRecall'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    if config.has_key('enableWorldWarLaba'):
        gameglobal.rds.ui.chat.updatePadChannels()
        if gameglobal.rds.ui.chat.curChannel == const.CHAT_CHANNEL_WORLD_WAR:
            gameglobal.rds.ui.chat.setCurChannel(const.CHAT_CHANNEL_VIEW)
    if config.has_key('enableCCSpeak'):
        if config['enableCCSpeak'] == False:
            ccManager.instance().logoutSession(const.CC_SESSION_TEAM)
    if config.has_key('enableWingWorldCarrierBuild'):
        if config.get('enableWingWorldCarrierBuild', False):
            gameglobal.rds.ui.wingWorldCarrierNarrow.isShowWingWorldCarrierNarrow()
        else:
            gameglobal.rds.ui.wingWorldCarrierNarrow.hide()
            gameglobal.rds.ui.wingWorldCarrierConstruct.hide()
    if config.has_key('enableOneKeyConfig'):
        gameglobal.rds.ui.actionbar.setOneKeyConfigBtn()
    if config.has_key('enableHistoryConsumed'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    if config.has_key('enableNewServerActivity'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    if config.has_key('enableLRUCache'):
        if clientcom.enableLRUCache():
            sfx.gEffectMgr.oldEffectCache.realClearEffectCache()
        else:
            sfx.gEffectMgr.LRUEffectCache.realClearEffectCache()
    if config.has_key('enableClanWarChallenge'):
        gameglobal.rds.ui.guild.hide()
    if config.has_key('enableEnvSDK') and config.get('enableEnvSDK', False):
        envSDKHelper.getInstance().initSDK()
    if config.has_key('enableFbAvoidDieItem'):
        num = BigWorld.player().fbAvoidDieItemCnt
        gameglobal.rds.ui.player.setFbAvoidDieCnt(num)
    if config.has_key('enableTopChatRoom'):
        gameglobal.rds.ui.topBar.refreshTopBarWidgets()
    if config.has_key('enableBet'):
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
    if config.has_key('enableNewSchoolTianZhao'):
        if clientcom.enableNewSchoolTianZhao():
            const.SCHOOL_SET = utils.AddInArray(const.SCHOOL_SET, const.SCHOOL_TIANZHAO)
            const.ALL_SCHOOLS = utils.AddInArray(const.ALL_SCHOOLS, const.SCHOOL_TIANZHAO)
            uiConst.JOB_LABELS = utils.AddInArray(uiConst.JOB_LABELS, uiConst.SCHOOL_FRAME_DESC[const.SCHOOL_TIANZHAO])
        else:
            const.SCHOOL_SET = utils.DelInArray(const.SCHOOL_SET, const.SCHOOL_TIANZHAO)
            const.ALL_SCHOOLS = utils.DelInArray(const.ALL_SCHOOLS, const.SCHOOL_TIANZHAO)
            uiConst.JOB_LABELS = utils.DelInArray(uiConst.JOB_LABELS, uiConst.SCHOOL_FRAME_DESC[const.SCHOOL_TIANZHAO])
