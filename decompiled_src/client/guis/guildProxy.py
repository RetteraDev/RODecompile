#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildProxy.o
from gamestrings import gameStrings
import time
import copy
import BigWorld
from Scaleform import GfxValue
import time, datetime
import gameglobal
import gametypes
import ui
import uiConst
import const
import uiUtils
import formula
import utils
import commGuild
import gamelog
import npcConst
import gameconfigCommon
from gamestrings import gameStrings
from item import Item
import commTournament
from helpers.guild import getGTNSD
from data import sys_config_data as SCD
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import UIProxy
from guis.asObject import ASObject
from callbackHelper import Functor
from helpers import capturePhoto
from helpers import charRes
from helpers import avatarMorpher
from data import state_data as SD
from data import guild_config_data as GCD
from data import game_msg_data as GMD
from data import guild_building_data as GBD
from data import guild_building_upgrade_data as GBUD
from data import guild_level_data as GLD
from data import guild_building_marker_data as GBMD
from data import guild_scale_data as GSCD
from data import guild_technology_data as GTD
from data import guild_resident_pskill_data as GRPD
from data import guild_challenge_data as GCHD
from data import guild_tournament_data as GTOD
from data import cross_guild_tournament_data as CGTD
from data import guild_info_activity_data as GIAD
from data import cross_guild_tournament_schedule_data as CGTSD
from cdata import game_msg_def_data as GMDD
from cdata import guild_func_prop_def_data as GFNPDD
from cdata import guild_challenge_punish_data as GCPD
from data import guild_info_activity_tips_data as GIATD
from data import guild_info_fuli_data as GIFD
from data import quest_loop_data as QLD
from data import consumable_item_data as CID
from data import bonus_history_check_data as BHCD
from data import cross_clan_war_config_data as CCWCD
from data import digong_clanwar_config_data as DCCD
from data import battle_field_data as BFD
from data import new_guild_tournament_schedule_data as NGTSD
from cdata import rank_guild_tournament_star_data as RGTSD
MENU_DIRECTION_LIMIT_NUM = 10
SORT_TYPE_LV = 1
SORT_TYPE_SCHOOL = 2
SORT_TYPE_POST = 3
SORT_TYPE_COIN = 4
SORT_TYPE_LOCAL = 5
SORT_TYPE_GROUP = 6
SORT_TYPE_TIME = 7

def sort_by_level(a, b):
    return cmp(a.level, b.level)


def sort_by_school(a, b):
    return cmp(a.school, b.school)


def sort_by_roleId(a, b):
    pa = gametypes.GUILD_PRIVILEGES.get(a.roleId, {}).get('sortv', 0)
    pb = gametypes.GUILD_PRIVILEGES.get(b.roleId, {}).get('sortv', 0)
    return cmp(pa, pb)


def sort_by_contrib(a, b):
    return cmp(a.contrib, b.contrib)


def sort_by_spaceNo(a, b):
    return cmp(a.spaceNo, b.spaceNo)


def sort_by_groupId(a, b):
    sortA = (-1 if a.groupId > 0 else 1, a.groupId)
    sortB = (-1 if b.groupId > 0 else 1, b.groupId)
    return cmp(sortA, sortB)


def sort_by_time(a, b):
    if a.online != b.online:
        return cmp(a.online, b.online)
    if a.online:
        return cmp(a.level, b.level)
    return cmp(a.tLastOnline, b.tLastOnline)


def sort_technologyPanel(a, b):
    if a['techSortId'] != b['techSortId']:
        return cmp(a['techSortId'], b['techSortId'])
    return cmp(a['buildingId'], b['buildingId'])


SORT_MAP = {SORT_TYPE_LV: (sort_by_level, False),
 SORT_TYPE_SCHOOL: (sort_by_school, False),
 SORT_TYPE_POST: (sort_by_roleId, True),
 SORT_TYPE_COIN: (sort_by_contrib, False),
 SORT_TYPE_LOCAL: (sort_by_spaceNo, False),
 SORT_TYPE_GROUP: (sort_by_groupId, False),
 SORT_TYPE_TIME: (sort_by_time, True)}
STATISTICS_SORT_BUILD = 1
STATISTICS_SORT_BUSINESS = 2
STATISTICS_SORT_WINE = 3
STATISTICS_SORT_TIRED = 4
STATISTICS_SORT_RUN = 5
STATISTICS_SORT_WAR = 6
STATISTICS_SORT_LEAGUEMATCH = 7
STATISTICS_SORT_SIGN_IN = 8
STATISTICS_SORT_WEEK_ACTIVATION = 9
STATISTICS_SORT_CONTRIB = 10
DAY_ITEMS = 1
WEEK_ITEMS = 2
MATCH_TYPE_GROUP_SCORE = 1
MATCH_TYPE_KICK = 2

def statistics_sort_by_build(a, b):
    return cmp(a['build'], b['build'])


def statistics_sort_by_business(a, b):
    return cmp(a['business'], b['business'])


def statistics_sort_by_wine(a, b):
    return cmp(a['wine'], b['wine'])


def statistics_sort_by_tired(a, b):
    return cmp(a['tired'], b['tired'])


def statistics_sort_by_run(a, b):
    return cmp(a['run'], b['run'])


def statistics_sort_by_war(a, b):
    return cmp(a['war'], b['war'])


def statistics_sort_by_leagueMatch(a, b):
    return cmp(a['leagueMatch'], b['leagueMatch'])


def statistics_sort_by_signIn(a, b):
    return cmp(a['signIn'], b['signIn'])


def statistics_sort_by_weekActivation(a, b):
    return cmp(a['weekActivation'], b['weekActivation'])


def statistics_sort_by_contrib(a, b):
    return cmp(a['contrib'], b['contrib'])


STATISTICS_SORT_MAP = {STATISTICS_SORT_BUILD: (statistics_sort_by_build, False),
 STATISTICS_SORT_BUSINESS: (statistics_sort_by_business, False),
 STATISTICS_SORT_WINE: (statistics_sort_by_wine, False),
 STATISTICS_SORT_TIRED: (statistics_sort_by_tired, False),
 STATISTICS_SORT_RUN: (statistics_sort_by_run, False),
 STATISTICS_SORT_WAR: (statistics_sort_by_war, False),
 STATISTICS_SORT_LEAGUEMATCH: (statistics_sort_by_leagueMatch, False),
 STATISTICS_SORT_SIGN_IN: (statistics_sort_by_signIn, False),
 STATISTICS_SORT_WEEK_ACTIVATION: (statistics_sort_by_weekActivation, False),
 STATISTICS_SORT_CONTRIB: (statistics_sort_by_contrib, False)}

class GuildProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildProxy, self).__init__(uiAdapter)
        self.modelMap = {'getAuthorization': self.onGetAuthorization,
         'getGuildTabState': self.onGetGuildTabState,
         'getGuildBuildingTabState': self.onGetGuildBuildingTabState,
         'getDisabledGuildTab': self.onGetDisabledGuildTab,
         'getOverviewInfo': self.onGetOverviewInfo,
         'changeAnnouncement': self.onChangeAnnouncement,
         'goGuildSpace': self.onGoGuildSpace,
         'levelGuild': self.onLevelGuild,
         'callMember': self.onCallMember,
         'dismissGuild': self.onDismissGuild,
         'clanManage': self.onClanManage,
         'getOverviewTabInfo': self.onGetOverviewTabInfo,
         'changeMenifest': self.onChangeMenifest,
         'setIgnoreGuildMerge': self.onSetIgnoreGuildMerge,
         'checkGuildMergeState': self.onGuildMergeState,
         'getMemberInfo': self.onGetMemberInfo,
         'setSort': self.onSetSort,
         'applyGuild': self.onApplyGuild,
         'groupSetting': self.onGroupSetting,
         'kickoutGuild': self.onKickoutGuild,
         'changePost': self.onChangePost,
         'isShowOffLineChange': self.onIsShowOffLineChange,
         'author': self.onAuthor,
         'updateMemberGroup': self.onUpdateMemberGroup,
         'inCrossServerSXY': self.onInCrossServerSXY,
         'crossServerSXYSet': self.onCrossServerSXYSet,
         'getBuildInfo': self.onGetBuildInfo,
         'donate': self.onDonate,
         'donateWithCoin': self.onDonateWithCoin,
         'upScale': self.onUpScale,
         'buyLand': self.onBuyLand,
         'clickBuildLevelUp': self.onClickBuildLevelUp,
         'clickBuildBtn': self.onClickBuildBtn,
         'openGuildStorage': self.onOpenGuildStorage,
         'cancelAssartBtn': self.onCancelAssartBtn,
         'cancelBuildBtn': self.onCancelBuildBtn,
         'checkHouseAssartState': self.onCheckHouseAssartState,
         'getManageTabBtnState': self.onGetManageTabBtnState,
         'getTechnologyBaseInfo': self.onGetTechnologyBaseInfo,
         'getTechnologyInfo': self.onGetTechnologyInfo,
         'techResearch': self.onTechResearch,
         'getZhanQiInfo': self.onGetZhanQiInfo,
         'showArmorSetting': self.onShowArmorSetting,
         'showFlagSetting': self.onShowFlagSetting,
         'selectStatisticsMode': self.onSelectStatisticsMode,
         'setStatisticsSort': self.onSetStatisticsSort,
         'getEnemyInfo': self.onGetEnemyInfo,
         'searchClan': self.onSearchClan,
         'searchGuild': self.onSearchGuild,
         'saveEnemy': self.onSaveEnemy,
         'getClanGuilds': self.onGetClanGuilds,
         'getGuildListTips': self.onGetGuildListTips,
         'openRewardSalaryHistory': self.onOpenRewardSalaryHistory,
         'assignRewardPayment': self.onAssignRewardPayment,
         'getEnableClan': self.onGetEnableClan,
         'getChallengeInfo': self.onGetChallengeInfo,
         'challengeSearch': self.onChallengeSearch,
         'challenge': self.onChallenge,
         'acceptChallenge': self.onAcceptChallenge,
         'rejectChallenge': self.onRejectChallenge,
         'surrenderChallenge': self.onSurrenderChallenge,
         'enterChallenge': self.onEnterChallenge,
         'initChallenge': self.onInitChallenge,
         'unRegisterChallenge': self.onUnRegisterChallenge,
         'getTournamentInfo': self.onGetTournamentInfo,
         'getWWTournamentInfo': self.onGetWWTournamentInfo,
         'showTournamentResult': self.onShowTournamentResult,
         'showTournamentRank': self.onShowTournamentRank,
         'showTournamentApply': self.onShowTournamentApply,
         'applyTrain': self.onApplyTrain,
         'showWWTournamentRank': self.onShowWWTournamentRank,
         'showWWTournamentResult': self.onShowWWTournamentResult,
         'getCrossTournamentInfo': self.onGetCrossTournamentInfo,
         'showCrossTournamentResult': self.onShowCrossTournamentResult,
         'showCrossTournamentFinalResult': self.onShowCrossTournamentFinalResult,
         'showCrossTournamentApply': self.onShowCrossTournamentApply,
         'isShowYixin': self.onIsShowYixin,
         'isLeader': self.onIsLeader,
         'isBindYixin': self.onIsBindYixin,
         'sendMsgToAll': self.onSendMsgToAll,
         'addYixinGroup': self.onAddYixinGroup,
         'subscribeSetting': self.onSubscribeSetting,
         'getActivityInfo': self.onGetActivityInfo,
         'backHome': self.onBackHome,
         'autoFindPath': self.onAutoFindPath,
         'getItemTipData': self.onGetItemTipData,
         'getFuLiTipData': self.onGetFuLiTipData,
         'openPanel': self.onOpenPanel,
         'itemGo': self.onItemGo,
         'initCrossClanWar': self.onInitCrossClanWar,
         'unRegisterCrossClanWar': self.onUnRegisterCrossClanWar,
         'setRankTournamentCraft': self.onSetTournamentCraft,
         'setRankTournamentBf': self.onSetTournamentBf,
         'lvRewardBtnClick': self.onLvRewardBtnClick,
         'lvRankBtnClick': self.onLvRankBtnClick,
         'showRankTournamentApply': self.onShowRankTournamentApply,
         'getEnableRankTournament': self.onGetEnableRankTournament,
         'gtnLiveBtnClick': self.onGtnLiveBtnClick,
         'gtnCheerBtnClick': self.onGtnCheerBtnClick}
        self.mediator = None
        self.tabIdx = uiConst.GUILDINFO_TAB_OVERVIEW
        self.sortType = SORT_TYPE_TIME
        self.ascendSorted = True
        self.isShowOffLine = True
        self.flagGen = None
        self.armorGen = None
        self.statisticsSortType = STATISTICS_SORT_CONTRIB
        self.statisticsAscendSorted = False
        self.intervalType = 0
        self.sitInChair = 0
        self.residentNpcId = 0
        self.residentTemplateId = 0
        self.bNeedTreat = False
        self.techReverse = {}
        self.searchClanTimer = None
        self.searchGuildTimer = None
        self.clanNameMap = {}
        self.guildNameMap = {}
        self.clanGuildList = {}
        self.searchClanCache = {}
        self.searchGuildCache = {}
        self.bonusHistory = {}
        self.challengeTimer = None
        self.challengeSearchTimer = None
        self.challengeSearchCache = {}
        self.version = 0
        self.challengeResultlist = []
        self.buffVersion = 0
        self.buffResultlist = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD:
            self.mediator = mediator
            BigWorld.player().registerEvent(const.EVENT_YIXIN_BIND_SUCCESS, self.yixinStateChange)
            BigWorld.player().registerEvent(const.EVENT_YIXIN_UNBIND_SUCCESS, self.yixinStateChange)
            initData = {}
            initData['enableWWGuildTournament'] = gameglobal.rds.configData.get('enableWWGuildTournament', False)
            initData['enableNewCrossGuildTournament'] = self.isEnableNewCrossTournament()
            initData['tabIdx'] = self.tabIdx
            return uiUtils.dict2GfxDict(initData, True)

    def show(self, tabIdx = uiConst.GUILDINFO_TAB_ACTIVITY):
        p = BigWorld.player()
        if hasattr(p, 'gmMode') and p.gmMode == const.GM_MODE_OBSERVER:
            pass
        elif not p.guildNUID:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
            return
        if not p.checkMapLimitUI(gametypes.MAP_LIMIT_UI_GUILD):
            return
        self.tabIdx = tabIdx
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD)
        if p.guild and p.guild.clanWarFlagMorpher:
            try:
                clanWarFlagMorpher = eval(p.guild.clanWarFlagMorpher)
                if utils.isDownloadImage(clanWarFlagMorpher[2]):
                    p.downloadNOSFile(const.IMAGES_DOWNLOAD_RELATIVE_DIR, clanWarFlagMorpher[2], gametypes.NOS_FILE_PICTURE, p.onGuildFlagIconDownloadNOSFile, ())
            except Exception as e:
                gamelog.error('@hjx guildProxy show:', e)

    def showAssignTab(self, tabIdx):
        p = BigWorld.player()
        if not p.guildNUID:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
            return
        if self.mediator:
            self.mediator.Invoke('setTabIndex', GfxValue(tabIdx))
        else:
            self.show(tabIdx)

    def clearWidget(self):
        self.resetHeadGen()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD)
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_YIXIN_BIND_SUCCESS, self.yixinStateChange)
                BigWorld.player().unRegisterEvent(const.EVENT_YIXIN_UNBIND_SUCCESS, self.yixinStateChange)
        gameglobal.rds.ui.guildArmor.hide()
        self.uiAdapter.crossClanWar.unRegisterPanel()
        self.uiAdapter.clanChallenge.unRegisterPanel()

    def reset(self):
        self.tabIdx = uiConst.GUILDINFO_TAB_OVERVIEW
        self.sortType = SORT_TYPE_TIME
        self.ascendSorted = True
        self.flagGen = None
        self.armorGen = None
        self.statisticsSortType = STATISTICS_SORT_CONTRIB
        self.statisticsAscendSorted = False
        self.intervalType = 0
        self.stopSearchClanTimer()
        self.stopSearchGuildTimer()
        self.clanNameMap = {}
        self.guildNameMap = {}
        self.clanGuildList = {}
        self.searchClanCache = {}
        self.searchGuildCache = {}
        self.stopChallengeTimer()
        self.stopChallengeSearchTimer()
        self.challengeSearchCache = {}

    def onGetAuthorization(self, *arg):
        self.updateAuthorization()

    def onGetGuildTabState(self, *arg):
        info = {'visibleChallengeBtn': gameglobal.rds.configData.get('enableGuildChallenge', False),
         'visibleTournamentBtn': gameglobal.rds.configData.get('enableGuildTournament', False),
         'visibleCrossTournamentBtn': gameglobal.rds.configData.get('enableCrossGuildTournament', False),
         'visibleCrososClanWarBtn': gameglobal.rds.configData.get('enableCrossClanWar', False)}
        return uiUtils.dict2GfxDict(info, True)

    def onGetGuildBuildingTabState(self, *arg):
        enableGuildBuildingTab = gameglobal.rds.configData.get('enableGuildBuildingTab', True)
        return GfxValue(enableGuildBuildingTab)

    def checkAuthorization(self, action, bNotify = True):
        p = BigWorld.player()
        if not p.guild:
            bNotify and p.showGameMsg(GMDD.data.GUILD_NOT_EXIST, ())
            return False
        if p.guild.state != gametypes.GUILD_STATE_ACTIVE and action in gametypes.GUILD_ACTIVE_ACTIONS:
            bNotify and p.showGameMsg(GMDD.data.GUILD_NOT_ACTIVE, ())
            return False
        if not hasattr(p.guild, 'memberMe'):
            return False
        if not self._hasPrivilege(p.guild.memberMe.roleId, action):
            return False
        return True

    def _hasPrivilege(self, roleId, action):
        p = BigWorld.player()
        if p.guild:
            privileges = p.guild.privileges
            if privileges:
                privileges = privileges.get(roleId)
                if privileges and action in privileges:
                    return True
            if action in gametypes.GUILD_CUSTOM_PRIVILEGES:
                return False
        pdata = gametypes.GUILD_PRIVILEGES.get(roleId)
        return action in pdata['privileges']

    def getAuthorizationDict(self):
        p = BigWorld.player()
        info = {}
        info['bAnnoun'] = self.checkAuthorization(gametypes.GUILD_ACTION_UPDATE_ANNOUNCEMENT)
        info['bDismiss'] = self.checkAuthorization(gametypes.GUILD_ACTION_DISMISS)
        info['bKickout'] = self.checkAuthorization(gametypes.GUILD_ACTION_KICKOUT_MEMBER)
        info['bAppoint'] = self.checkAuthorization(gametypes.GUILD_ACTION_APPOINT)
        info['bQuery'] = self.checkAuthorization(gametypes.GUILD_ACTION_QUERY_APPLY)
        info['bFlag'] = self.checkAuthorization(gametypes.GUILD_ACTION_UPDATE_FLAG)
        if gameglobal.rds.configData.get('enableClan', False):
            info['bClanManage'] = bool(BigWorld.player().guild and BigWorld.player().clanNUID and BigWorld.player().guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER)
        else:
            info['bClanManage'] = False
        info['bEnemy'] = self.checkAuthorization(gametypes.GUILD_ACTION_PK_ENEMY)
        info['bChallenge'] = self.checkAuthorization(gametypes.GUILD_ACTION_GUILD_CHALLENGE)
        info['isLeader'] = False
        for groupId in gametypes.GUILD_TOURNAMENT_GUILD_GROUP:
            if p.guild.isGroupLeader(groupId, p.gbId):
                info['isLeader'] = True
                break

        return info

    def updateAuthorization(self):
        gameglobal.rds.ui.guildGrowth.updateAuthorization()
        if self.mediator:
            self.mediator.Invoke('updateAuthorization', uiUtils.dict2GfxDict(self.getAuthorizationDict(), True))

    def onGetOverviewTabInfo(self, *arg):
        p = BigWorld.player()
        guild = p.guild
        if guild == None:
            return uiUtils.dict2GfxDict({}, True)
        else:
            info = {}
            info['announcement'] = guild.announcement
            menifest = uiUtils.textToHtml(guild.menifest)
            info['menifest'] = menifest
            return uiUtils.dict2GfxDict(info, True)

    def onGetOverviewInfo(self, *arg):
        p = BigWorld.player()
        guild = p.guild
        creatDate = ''
        if guild:
            tplSec = time.localtime(guild.tBuild)
            creatDate = str(tplSec[0]) + gameStrings.TEXT_GUILDPROXY_497 + str(tplSec[1]) + gameStrings.TEXT_GUILDPROXY_497_1 + str(tplSec[2]) + gameStrings.TEXT_PLAYRECOMMPROXY_848_6
        else:
            return uiUtils.dict2GfxDict({}, True)
        eventList = []
        for event in guild.event:
            try:
                eventList.append(self.formatEvent(event))
            except:
                pass

        info = {}
        info['eventList'] = eventList
        info['guildName'] = guild.name
        info['leaderText'] = guild.leaderRole
        info['nuidText'] = guild.dbID
        info['createrText'] = guild.creatorRole
        info['creatDataText'] = creatDate
        info['scaleText'] = GSCD.data.get(guild.scale).get('name', '')
        info['lvText'] = guild.level
        info['menberText'] = str(len(guild.member)) + '/' + str(guild.maxMember)
        info['prosperityText'] = format(guild.prosperity, ',')
        info['cashText'] = format(guild.bindCash, ',')
        info['cashTips'] = '%s/%s' % (info['cashText'], format(guild._getMaxBindCash(), ','))
        info['woodText'] = format(guild.wood, ',')
        info['woodTips'] = '%s/%s' % (info['woodText'], format(guild._getMaxWood(), ','))
        info['mojingText'] = format(guild.mojing, ',')
        info['mojingTips'] = '%s/%s' % (info['mojingText'], format(guild._getMaxMojing(), ','))
        info['xirangText'] = format(guild.xirang, ',')
        info['xirangTips'] = '%s/%s' % (info['xirangText'], format(guild._getMaxXirang(), ','))
        info['announcement'] = guild.announcement
        menifest = uiUtils.textToHtml(guild.menifest)
        info['menifest'] = menifest
        icon, color = uiUtils.getGuildFlag(p.guildFlag)
        if utils.isDownloadImage(icon) and p.guildFlagIconStatus != gametypes.NOS_FILE_STATUS_APPROVED:
            icon = GCD.data.get('zhanQiHuiJiPic', ['2001'])[0]
        info['IconPath'] = uiUtils.getGuildIconPath(icon)
        info['flagColor'] = color
        now = utils.getNow()
        leftTime = int(guild.tMaintainDestroy - now)
        if guild.tMaintainDestroy > 0 and leftTime > 0:
            info['destroyText'] = uiUtils.formatTime(leftTime)
        else:
            info['destroyText'] = ''
        info['autoResignText'] = self.getGuildLeaderAutoResignText(now)
        if p.guildMemberSkills.has_key(uiConst.GUILD_SKILL_DZG):
            info['goGuildSpaceBtnEnabled'] = True
        else:
            info['goGuildSpaceBtnEnabled'] = False
            info['goGuildSpaceBtnTip'] = GCD.data.get('goGuildSpaceBtnTip', gameStrings.TEXT_GUILDPROXY_554)
        info['prestigeVisible'] = gameglobal.rds.configData.get('enableGuildPrestigeTopRank', False)
        info['prestigeText'] = format(guild.prestige, ',')
        info['prestigeHelpKey'] = GCD.data.get('prestigeHelpKey', 0)
        info['guildMergeSetVisible'] = p.isGuildLeader() and gameglobal.rds.configData.get('enableGuildMerger', False)
        info['ignoreRecommendGuildMerger'] = getattr(p, 'ignoreRecommendGuildMerger', False)
        return uiUtils.dict2GfxDict(info, True)

    def getGuildLeaderAutoResignText(self, now):
        if not gameglobal.rds.configData.get('enableClientGuildLeaderAutoResign', False):
            return ''
        p = BigWorld.player()
        if not p.guild:
            return
        leftTime = int(getattr(p.guild, 'leaderAutoResignTime', 0) - now)
        if leftTime > 0:
            return uiUtils.formatTime(leftTime)
        else:
            return ''

    def onChangeAnnouncement(self, *arg):
        gameglobal.rds.ui.guildAnnouncement.show()

    def onChangeMenifest(self, *arg):
        gameglobal.rds.ui.guildMenifest.show()

    @ui.callInCD(2.2)
    def onSetIgnoreGuildMerge(self, *args):
        selected = args[3][0].GetBool()
        BigWorld.player().cell.applyUpdateIgnoreGuildMergerFlag(selected)

    def onGuildMergeState(self, *args):
        p = BigWorld.player()
        stateEndTime = p.guild.guildMergerVal.tStateEnd
        timeStr = utils.formatTimeStr(max(0, stateEndTime - utils.getNow()), 'h:m', True, 2, 2, 2)
        if not gameglobal.rds.configData.get('enableGuildMerger', False):
            str = ''
        elif p.guild.guildMergerVal.state in (gametypes.GUILD_MERGER_STATE_PREPARE, gametypes.GUILD_MERGER_STATE_COMFIRM):
            str = GCD.data.get('guildMergePrepareState', '%s') % timeStr
        elif p.guild.guildMergerVal.state == gametypes.GUILD_MERGER_STATE_SHOW:
            str = GCD.data.get('guildMergeShowState', '%s') % timeStr
        else:
            str = ''
        gamelog.info('jbx:guildMergeLeftTimeStr', str)
        return GfxValue(ui.gbk2unicode(str))

    def updateAnnouncement(self):
        if self.mediator:
            self.mediator.Invoke('updateAnnouncement', GfxValue(gbk2unicode(BigWorld.player().guild.announcement)))

    def updateMenifest(self):
        p = BigWorld.player()
        if self.mediator:
            menifest = uiUtils.textToHtml(p.guild.menifest)
            self.mediator.Invoke('updateMenifest', GfxValue(gbk2unicode(menifest)))

    def onGoGuildSpace(self, *arg):
        gameglobal.rds.ui.skill.useGuildSkill(uiConst.GUILD_SKILL_DZG)

    def onLevelGuild(self, *arg):
        p = BigWorld.player()
        if not p.guild:
            return
        contribDecMinJoinTime = GCD.data.get('awayContribDecMinJoinTime', const.GUILD_AWAY_CONTRIB_DEC_MIN_JOIN_TIME)
        guildCdMsg = gameStrings.TEXT_GUILDPROXY_621 + str(GCD.data.get('joinCD', const.GUILD_JOIN_CD / const.TIME_INTERVAL_HOUR)) + gameStrings.TEXT_GUILDPROXY_621_1
        if utils.getNow() - p.guild.memberMe.tJoin > contribDecMinJoinTime:
            contribDecRate = GCD.data.get('awayContribDecRate', const.GUILD_AWAY_CONTRIB_DEC_RATE)
            contribDecMax = GCD.data.get('awayContribDecMax', const.GUILD_AWAY_CONTRIB_DEC_MAX)
            msg = gameStrings.TEXT_GUILDPROXY_625 % (int(contribDecRate * 100), contribDecMax) + guildCdMsg + gameStrings.TEXT_GUILDPROXY_625_1
        else:
            msg = gameStrings.TEXT_GUILDPROXY_627 + guildCdMsg + gameStrings.TEXT_GUILDPROXY_627_1
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.leaveGuild)

    def leaveGuild(self):
        BigWorld.player().cell.leaveGuild()
        self.hide()

    def onCallMember(self, *arg):
        if gameglobal.rds.configData.get('enableGuildGather', False):
            gameglobal.rds.ui.guildCallMember.show()
        else:
            BigWorld.player().showGameMsg(GMDD.data.STILL_UNDER_DEVELOPING, ())

    def onDismissGuild(self, *arg):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_GUILDPROXY_641, self.dismissGuild)

    def dismissGuild(self):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableInventoryLock', False):
            p.getCipher(p.cell.guildDismiss, ())
        else:
            p.cell.guildDismiss('')

    def onClanManage(self, *arg):
        BigWorld.player().cell.queryClan()

    def formatEvent(self, event):
        p = BigWorld.player()
        eventSec = time.localtime(event.tWhen)
        eventDate = str(eventSec[0]) + '-' + str(eventSec[1]) + '-' + str(eventSec[2])
        if GMD.data.get(event.msgId, None):
            eventMsg = p.formatMsg(GMD.data.get(event.msgId, None).get('text', ''), event.args)
        else:
            eventMsg = ''
        return [eventMsg, eventDate]

    def addEvent(self, event):
        if self.mediator:
            self.mediator.Invoke('addEvent', uiUtils.array2GfxAarry(self.formatEvent(event), True))

    def onGetMemberInfo(self, *arg):
        self.refreshMemberInfo()

    def refreshMemberInfo(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            allMembers = guild.member.values()
            onlineMembers = [ member for member in allMembers if member.online ]
            if self.isShowOffLine:
                guildMembers = allMembers
            else:
                guildMembers = onlineMembers
            members = sorted(guildMembers, cmp=SORT_MAP[self.sortType][0], reverse=SORT_MAP[self.sortType][1] if self.ascendSorted else not SORT_MAP[self.sortType][1])
            memberList = []
            memberLen = len(members)
            for i in xrange(memberLen):
                memberInfo = self.createMemberInfo(members[i])
                if memberLen > MENU_DIRECTION_LIMIT_NUM and i > MENU_DIRECTION_LIMIT_NUM and i + MENU_DIRECTION_LIMIT_NUM > memberLen:
                    memberInfo['menuDirection'] = 'up'
                else:
                    memberInfo['menuDirection'] = 'down'
                memberList.append(memberInfo)

            info = {}
            info['memberList'] = memberList
            info['sortType'] = self.sortType
            info['ascendSorted'] = self.ascendSorted
            info['isShowOffLine'] = self.isShowOffLine
            info['vitalityText'] = gameStrings.TEXT_GUILDPROXY_701 % guild.vitality
            info['vitalityTip'] = GCD.data.get('vitalityTip', '')
            info['memberNumText'] = gameStrings.TEXT_GUILDPROXY_703 % (len(onlineMembers), len(allMembers))
            self.mediator.Invoke('refreshMemberInfo', uiUtils.dict2GfxDict(info, True))
            self.updateGroupInfo()

    def updateMember(self, gbId):
        if self.mediator:
            member = BigWorld.player().guild.member[gbId]
            memberInfo = self.createMemberInfo(member)
            self.mediator.Invoke('updateMember', uiUtils.dict2GfxDict(memberInfo, True))

    def createMemberInfo(self, member):
        p = BigWorld.player()
        memberInfo = {}
        memberInfo['gbId'] = str(member.gbId)
        memberInfo['nameText'] = member.role
        memberInfo['lvText'] = member.level
        memberInfo['schoolText'] = const.SCHOOL_DICT.get(member.school, '')
        memberInfo['postText'] = gametypes.GUILD_ROLE_DICT.get(member.roleId, '')
        memberInfo['coinText'] = str(member.contrib) + '/' + str(member.contribTotal)
        memberInfo['spaceText'] = formula.whatAreaName(member.spaceNo, member.areaId)
        if p.guild.isGroupLeader(member.groupId, member.gbId):
            memberInfo['groupId'] = gametypes.GUILD_TOURNAMENT_GUILD_FAKE_REVERSE_GROUP.get(member.groupId, 0)
        else:
            memberInfo['groupId'] = member.groupId
        memberInfo['timeText'] = self.getLastOnline(member.online, member.tLastOnline)
        memberInfo['businessFlag'] = member.gbId in BigWorld.player().guild.businessMan
        memberInfo['backIcon'] = False
        memberInfo['online'] = bool(member.online)
        return memberInfo

    def updateGroupInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            groupList = [{'label': '',
              'groupId': 0}]
            groups = [ x for x in guild.group.itervalues() if x.groupId not in gametypes.GUILD_TOURNAMENT_GUILD_GROUP ]
            groups.sort(key=lambda x: x.tWhen)
            if gameglobal.rds.configData.get('enableGuildTournament', False):
                tgroups = [ x for x in guild.group.itervalues() if x.groupId in gametypes.GUILD_TOURNAMENT_GUILD_GROUP ]
                groups.extend(tgroups)
            for group in groups:
                groupList.append({'label': group.name,
                 'groupId': group.groupId})

            self.mediator.Invoke('updateGroupInfo', uiUtils.array2GfxAarry(groupList, True))

    def getLastOnline(self, online, tLastOnline):
        if online:
            return gameStrings.TEXT_FRIENDPROXY_293_1
        p = BigWorld.player()
        interval = int(p.getServerTime() - tLastOnline)
        if tLastOnline == 0:
            return gameStrings.TEXT_GUILDPROXY_754
        elif interval < 3600:
            return gameStrings.TEXT_GUILDPROXY_756
        elif interval < 86400:
            return str(interval / 3600) + gameStrings.TEXT_GUILDPROXY_758
        elif interval < 2592000:
            return str(interval / 86400) + gameStrings.TEXT_GUILDPROXY_760
        elif interval < 946080000:
            return str(interval / 2592000) + gameStrings.TEXT_GUILDPROXY_762
        else:
            return str(interval / 31536000) + gameStrings.TEXT_GUILDPROXY_764

    def onSetSort(self, *arg):
        if self.sortType == int(arg[3][0].GetString()) and self.ascendSorted == arg[3][1].GetBool():
            return
        self.sortType = int(arg[3][0].GetString())
        self.ascendSorted = arg[3][1].GetBool()
        self.refreshMemberInfo()

    def onApplyGuild(self, *arg):
        gameglobal.rds.ui.guildMember.getGuildApplyList(True)

    def onGroupSetting(self, *arg):
        gameglobal.rds.ui.guildGroup.show()

    def onKickoutGuild(self, *arg):
        gbId = int(arg[3][0].GetString())
        role = unicode2gbk(arg[3][1].GetString())
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_GUILDPROXY_782 % role, Functor(self.kickoutGuild, gbId, role))

    def kickoutGuild(self, gbId, role):
        BigWorld.player().cell.kickoutGuildMember(gbId, role)

    def onChangePost(self, *arg):
        gameglobal.rds.ui.guildPost.show(int(arg[3][0].GetString()))

    def onIsShowOffLineChange(self, *arg):
        isShowOffLine = arg[3][0].GetBool()
        if self.isShowOffLine == isShowOffLine:
            return
        self.isShowOffLine = isShowOffLine
        self.refreshMemberInfo()

    def onAuthor(self, *arg):
        gameglobal.rds.ui.guildAuthorization.show()

    def onUpdateMemberGroup(self, *arg):
        gbId = int(arg[3][0].GetString())
        role = unicode2gbk(arg[3][1].GetString())
        groupId = int(arg[3][2].GetNumber())
        BigWorld.player().cell.updateGuildMemberGroup(gbId, role, groupId)

    def onInCrossServerSXY(self, *args):
        inTimeRange = False
        if DCCD.data.get('gsxyCreateTime', '') and DCCD.data.get('gsxyEndTime', ''):
            inTimeRange = utils.inCrontabRange(DCCD.data.get('gsxyCreateTime', ''), DCCD.data.get('gsxyEndTime', ''))
        return GfxValue(gameconfigCommon.enableGSXY() and inTimeRange)

    def onCrossServerSXYSet(self, *args):
        self.uiAdapter.crossServerSXYSet.show()

    def onGetBuildInfo(self, *arg):
        self.refreshBuildInfo()
        self.refreshResourceInfo()
        self.refreshBuildProsperity()

    def refreshBuildInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            info = {}
            guildBuildList = []
            for markerId in guild.marker.iterkeys():
                buildInfo = self.createBuildInfo(markerId)
                if buildInfo:
                    guildBuildList.append(buildInfo)

            info['guildBuildList'] = guildBuildList
            if self.getHouseAssartState(uiConst.GUILD_BUILDING_PANEL_HOUSE2, False):
                info['houseBtn2Name'] = gameStrings.TEXT_GUILDPROXY_835
            else:
                info['houseBtn2Name'] = gameStrings.TEXT_GUILDPROXY_837
            info['remoteStorage'] = guild.getAbility(GFNPDD.data.REMOTE_STORAGE)
            info['hasSpace'] = guild.hasSpace
            info['spacePrice'] = GCD.data.get('spacePrice', const.GUILD_SPACE_PRICE)
            self.mediator.Invoke('refreshBuildInfo', uiUtils.dict2GfxDict(info, True))
            self.refreshExploreStateInfo()
            self.refreshCurBuildInfo()

    def refreshSingleBuildInfo(self, markerId):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            info = {}
            if self.getHouseAssartState(uiConst.GUILD_BUILDING_PANEL_HOUSE2, False):
                info['houseBtn2Name'] = gameStrings.TEXT_GUILDPROXY_835
            else:
                info['houseBtn2Name'] = gameStrings.TEXT_GUILDPROXY_837
            info['populationText'] = '%d/%d' % (guild._getPopulation(), guild._getMaxPopulation())
            info['popNumText'] = len(guild.hiredResident)
            info['buildInfo'] = self.createBuildInfo(markerId)
            self.mediator.Invoke('refreshSingleBuildInfo', uiUtils.dict2GfxDict(info, True))
            self.refreshCurBuildInfo()

    def createBuildInfo(self, markerId):
        guild = BigWorld.player().guild
        marker = guild.marker.get(markerId)
        buildingNUID = marker.buildingNUID if marker else None
        buildValue = guild.building.get(buildingNUID) if buildingNUID else None
        markerBaseData = GBMD.data.get(markerId, {})
        if markerBaseData.get('needShow', 0) == 0:
            return
        else:
            if buildValue:
                buildingId = buildValue.buildingId
            else:
                buildingIds = markerBaseData.get('buildingId', 0)
                if isinstance(buildingIds, tuple) and len(buildingIds) > 1:
                    buildingId = buildingIds[0]
                else:
                    buildingId = buildingIds
            if not gameglobal.rds.configData.get('enableGuildShop', False):
                if buildingId == gametypes.GUILD_BUILDING_TREASURE_SHOP_ID:
                    return
            baseData = GBD.data.get(buildingId, {})
            level = buildValue and buildValue.level or 0
            if not marker.isDevFinished():
                name = gameStrings.TEXT_GUILDPROXY_837
                tips = markerBaseData.get('desc', '')
            elif buildValue and buildValue.level > 0:
                name = gameStrings.TEXT_FISHGROUP_126 % (baseData.get('name', ''), buildValue.level)
                tips = baseData.get('description', '')
            else:
                name = gameStrings.TEXT_GUILDBUILDUPGRADEPROXY_199 % baseData.get('name', '')
                tips = markerBaseData.get('desc', '')
            buildInfo = {}
            buildInfo['markerId'] = str(markerId)
            buildInfo['buildingId'] = buildingId
            buildInfo['name'] = name
            buildInfo['tips'] = tips
            buildInfo['level'] = level
            panelMcPos = markerBaseData.get('panelMcPos', (0, 0))
            buildInfo['x'] = panelMcPos[0]
            buildInfo['y'] = panelMcPos[1]
            panelAreaType = markerBaseData.get('panelAreaType', 0)
            buildInfo['panelAreaType'] = panelAreaType
            imgPathList = ()
            if panelAreaType == uiConst.GUILD_BUILDING_PANEL_MAIN:
                imgPathList = baseData.get('imgPathList', ())
            elif panelAreaType in (uiConst.GUILD_BUILDING_PANEL_HOUSE1, uiConst.GUILD_BUILDING_PANEL_HOUSE2):
                imgPathList = markerBaseData.get('imgPathList', ())
                if level == 0:
                    needLevel = max(GBUD.data.get((buildingId, 1), {}).get('masterBuildingLevel', 0), markerBaseData.get('glevel', 0))
                    if guild.level < needLevel:
                        return
            listLen = len(imgPathList)
            if listLen == 0:
                return
            if listLen > level:
                imgPath = str(imgPathList[level])
                if level > 0 and buildingId in (gametypes.GUILD_BUILDING_FARMHOUSE_ID, gametypes.GUILD_BUILDING_HOUSE_ID) and isinstance(markerBaseData.get('buildingId', 0), tuple):
                    imgPath += '_%d' % buildingId
            else:
                imgPath = str(imgPathList[listLen - 1])
            buildInfo['imgPath'] = commGuild.getGuildBuildingImgPath(imgPath)
            return buildInfo

    def refreshResourceInfo(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            info = {}
            info['level'] = guild.level
            info['levelTitleTips'] = gameStrings.TEXT_GUILDPROXY_949
            info['cash'] = format(guild.bindCash, ',')
            info['cashTips'] = '%s/%s' % (info['cash'], format(guild._getMaxBindCash(), ','))
            info['wood'] = format(guild.wood, ',')
            info['woodTips'] = '%s/%s' % (info['wood'], format(guild._getMaxWood(), ','))
            info['mojing'] = format(guild.mojing, ',')
            info['mojingTips'] = '%s/%s' % (info['mojing'], format(guild._getMaxMojing(), ','))
            info['xirang'] = format(guild.xirang, ',')
            info['xirangTips'] = '%s/%s' % (info['xirang'], format(guild._getMaxXirang(), ','))
            info['repairRate'] = '%d%%' % (guild._getMaintainFeeRate() * 100)
            info['repairRateTips'] = GCD.data.get('maintainFeeTips', '')
            info['populationText'] = '%d/%d' % (guild._getPopulation(), guild._getMaxPopulation())
            info['popNumText'] = len(guild.hiredResident)
            mojingFee, xirangFee, woodFee, cashFee = commGuild.calcMaintainFee(guild)
            info['cashFee'] = format(cashFee, ',')
            info['woodFee'] = format(woodFee, ',')
            info['mojingFee'] = format(mojingFee, ',')
            info['xirangFee'] = format(xirangFee, ',')
            now = utils.getNow()
            leftTime = int(guild.tMaintainDestroy - now)
            if guild.tMaintainDestroy > 0 and leftTime > 0:
                info['destroyText'] = uiUtils.formatTime(leftTime)
            else:
                info['destroyText'] = ''
            info['autoResignText'] = self.getGuildLeaderAutoResignText(now)
            info['prestigeText'] = format(guild.prestige, ',')
            self.mediator.Invoke('refreshResourceInfo', uiUtils.dict2GfxDict(info, True))

    def refreshBuildProsperity(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            info = {}
            info['scale'] = 'lv%d' % guild.scale
            currentValue = 100.0
            upScaleBtnEnabled = True
            if guild.scale >= const.GUILD_SCALE_MAX:
                scaleProgressBarText = gameStrings.TEXT_GUILDPROXY_996 % format(guild.prosperity, ',')
                upScaleBtnEnabled = False
            else:
                progressMax = GSCD.data.get(guild.scale + 1).get('prosperity', 0)
                if progressMax and progressMax > guild.prosperity:
                    currentValue = currentValue * guild.prosperity / progressMax
                    upScaleBtnEnabled = False
                scaleProgressBarText = gameStrings.TEXT_GUILDPROXY_1004 % (format(guild.prosperity, ','), format(progressMax, ','))
            info['scaleProgressBarText'] = scaleProgressBarText
            info['scaleCurrentValue'] = currentValue
            info['upScaleBtnEnabled'] = upScaleBtnEnabled and self.checkAuthorization(gametypes.GUILD_ACTION_UPGRADE, False)
            nextScaleData = GSCD.data.get(guild.scale + 1, {})
            scaleTips = ''
            if nextScaleData:
                scaleName = gameStrings.TEXT_GUILDPROXY_1012 % nextScaleData.get('name', '')
                scaleTips = gameStrings.TEXT_GUILDPROXY_1013 % (uiUtils.toHtml(scaleName, '#E5BE67'), format(nextScaleData.get('prosperity', 0), ','))
                costItems = nextScaleData.get('costItems', None)
                if costItems:
                    for itemId, needNum in costItems:
                        scaleTips += gameStrings.TEXT_GUILDPROXY_1017 % (uiUtils.getItemColorName(itemId), format(needNum, ','))

            info['scaleTips'] = scaleTips
            self.mediator.Invoke('refreshBuildProsperity', uiUtils.dict2GfxDict(info, True))

    def refreshExploreStateInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            info = []
            for areaValue in guild.area.itervalues():
                areaInfo = {}
                areaInfo['areaName'] = 'area%d' % areaValue.areaId
                if areaValue.isExtFinished():
                    areaInfo['isFinish'] = True
                else:
                    areaInfo['isFinish'] = False
                info.append(areaInfo)

            self.mediator.Invoke('refreshExploreStateInfo', uiUtils.array2GfxAarry(info, True))

    def refreshCurBuildInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            info = {}
            guildAssartList = []
            isAssartNum = 0
            for markerId in guild.marker.iterkeys():
                marker = guild.marker.get(markerId)
                if marker and marker.inDev():
                    markerData = GBMD.data.get(markerId, {})
                    isAssartNum += 1
                    buildInfo = {}
                    buildInfo['markerId'] = str(markerId)
                    buildInfo['name'] = markerData.get('name', 0)
                    progressMax = markerData.get('progress', 0)
                    currentValue = 100.0
                    if progressMax >= marker.progress:
                        currentValue = currentValue * marker.progress / progressMax
                        buildInfo['progressBarText'] = '%s/%s' % (format(marker.progress, ','), format(progressMax, ','))
                    else:
                        buildInfo['progressBarText'] = '%s/%s' % (format(progressMax, ','), format(progressMax, ','))
                    buildInfo['currentValue'] = currentValue
                    guildAssartList.append(buildInfo)

            info['assartState'] = '%d/%d' % (isAssartNum, guild._getMaxConcurrentDevNum())
            info['guildAssartList'] = guildAssartList
            guildBuildList = []
            isUpgradeNum = 0
            for markerId in guild.marker.iterkeys():
                buildingNUID = guild.marker[markerId].buildingNUID
                buildValue = guild.building.get(buildingNUID) if buildingNUID else None
                if buildValue and buildValue.inUpgrading():
                    if buildValue and buildValue.level > 0:
                        level = gameStrings.TEXT_GUILDPROXY_1076 % (buildValue.level, buildValue.level + 1)
                    else:
                        level = gameStrings.TEXT_GUILDPROXY_1078
                    isUpgradeNum += 1
                    buildInfo = {}
                    buildInfo['markerId'] = str(markerId)
                    buildInfo['name'] = GBD.data.get(buildValue.buildingId, {}).get('name', '')
                    buildInfo['level'] = level
                    progressMax = GBUD.data.get((buildValue.buildingId, buildValue.level + 1), {}).get('progress', 0)
                    currentValue = 100.0
                    if progressMax >= buildValue.progress:
                        currentValue = currentValue * buildValue.progress / progressMax
                        buildInfo['progressBarText'] = '%s/%s' % (format(buildValue.progress, ','), format(progressMax, ','))
                    else:
                        buildInfo['progressBarText'] = '%s/%s' % (format(progressMax, ','), format(progressMax, ','))
                    buildInfo['currentValue'] = currentValue
                    guildBuildList.append(buildInfo)

            info['upgradeState'] = '%d/%d' % (isUpgradeNum, guild._getMaxConcurrentBuildingNum())
            info['guildBuildList'] = guildBuildList
            self.mediator.Invoke('refreshCurBuildInfo', uiUtils.dict2GfxDict(info, True))

    def onDonate(self, *arg):
        gameglobal.rds.ui.guildDonate.show()

    def onDonateWithCoin(self, *args):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableGuildDonateWithCoin', False):
            p.showGameMsg(GMDD.data.DONATEWITHCOIN_CONFIG_DISABLE, ())
            return
        donateCoinList = GCD.data.get('donateWithCoin', ())
        if not donateCoinList or p.guildDonateByCoinCntDaily >= len(donateCoinList):
            p.showGameMsg(GMDD.data.DONATEWITHCOIN_MORE_THAN_MAX, ())
            return
        curDonateTime = p.guildDonateByCoinCntDaily + 1
        coinCnt, contribNum, guildCash = donateCoinList[curDonateTime - 1]
        msg = uiUtils.getTextFromGMD(GMDD.data.DONATE_WITH_COIN_MSG, '%d %d %d %d') % (curDonateTime,
         coinCnt,
         contribNum,
         guildCash)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.confirmDonateWithCoin)

    def confirmDonateWithCoin(self):
        p = BigWorld.player()
        p.getCipher(p.cell.guildDonateWithCoin)

    def onUpScale(self, *arg):
        gameglobal.rds.ui.guildScaleUpgrade.show()

    def onBuyLand(self, *arg):
        msg = gameStrings.TEXT_GUILDPROXY_1126 % GCD.data.get('spacePrice', const.GUILD_SPACE_PRICE)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, BigWorld.player().cell.buyGuildSpace)

    def onClickBuildLevelUp(self, *arg):
        markerId = int(arg[3][0].GetString())
        marker = BigWorld.player().guild.marker.get(markerId)
        if marker:
            if marker.isDevFinished():
                gameglobal.rds.ui.guildBuildSelect.show(marker.markerId)
            else:
                gameglobal.rds.ui.guildAssart.show(marker.markerId)

    def onClickBuildBtn(self, *arg):
        markerId = int(arg[3][0].GetString())
        if gameglobal.rds.configData.get('enableRemoteGuildBuilding', False):
            self.openGuildBuilding(markerId)

    def openGuildBuilding(self, markerId = 0, buildingNUID = 0, npcEntityId = 0):
        p = BigWorld.player()
        guild = p.guild
        if markerId:
            buildingNUID = guild.marker[markerId].buildingNUID
        buildValue = guild.building.get(buildingNUID) if buildingNUID else None
        if buildValue and buildValue.level > 0:
            buildingId = buildValue.buildingId
            markerId = buildValue.markerId
        else:
            return
        npc = BigWorld.entities.get(npcEntityId)
        if npc:
            gameglobal.rds.ui.funcNpc.openDirectly(p.id, npc.npcId, npcConst.NPC_FUNC_GUILD)
        if buildingId == gametypes.GUILD_BUILDING_MASTER_ID:
            gameglobal.rds.ui.guildResidentManager.show(markerId, needHideAllGuildBuilding=True)
        elif buildingId == gametypes.GUILD_BUILDING_RESTAURANT_ID:
            gameglobal.rds.ui.guildResidentManager.show(markerId, needHideAllGuildBuilding=True)
        elif buildingId == gametypes.GUILD_BUILDING_STORAGE_ID:
            gameglobal.rds.ui.guildStorage.show(markerId, npcId=npcEntityId)
        elif buildingId == gametypes.GUILD_BUILDING_GROWTH_ID:
            gameglobal.rds.ui.guildGrowth.show(markerId)
        elif buildingId == gametypes.GUILD_BUILDING_ACTIVITY_ID:
            gameglobal.rds.ui.guildActivity.show(markerId)
        elif buildingId == gametypes.GUILD_BUILDING_ASTROLOGY_ID:
            gameglobal.rds.ui.guildFindStar.show(markerId)
        elif buildingId == gametypes.GUILD_BUILDING_LUMBERYARD_ID:
            gameglobal.rds.ui.guildSawmill.show(markerId)
        elif buildingId == gametypes.GUILD_BUILDING_MINE_ID:
            gameglobal.rds.ui.guildSawmill.show(markerId)
        elif buildingId == gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID:
            gameglobal.rds.ui.guildFactory.show(markerId)
        elif buildingId == gametypes.GUILD_BUILDING_FACTORY_FACILITY_ID:
            gameglobal.rds.ui.guildFactory.show(markerId)

    def onOpenGuildStorage(self, *arg):
        self.openGuildBuilding(commGuild.getMarkerIdByBuildingId(BigWorld.player().guild, gametypes.GUILD_BUILDING_STORAGE_ID))

    def onCancelAssartBtn(self, *arg):
        markerId = int(arg[3][0].GetString())
        gameglobal.rds.ui.guildAssart.clearNpcId()
        gameglobal.rds.ui.guildAssart.cancelAssarting(markerId)

    def onCancelBuildBtn(self, *arg):
        markerId = int(arg[3][0].GetString())
        marker = BigWorld.player().guild.marker.get(markerId)
        if marker:
            gameglobal.rds.ui.guildBuildUpgrade.clearNpcId()
            gameglobal.rds.ui.guildBuildUpgrade.cancelUpgradeBuilding(marker.buildingNUID)

    def onCheckHouseAssartState(self, *arg):
        areaId = int(arg[3][0].GetNumber())
        return GfxValue(self.getHouseAssartState(areaId, True))

    def getHouseAssartState(self, areaId, userClick):
        p = BigWorld.player()
        guild = p.guild
        for markerId in guild.marker.iterkeys():
            markerBaseData = GBMD.data.get(markerId, {})
            if markerBaseData.has_key('children') and markerBaseData.get('panelAreaType', 0) == areaId:
                marker = guild.marker.get(markerId)
                if marker and marker.isDevFinished():
                    return True
                if userClick:
                    gameglobal.rds.ui.guildAssart.show(marker.markerId)
                    return False

        return False

    def onGetManageTabBtnState(self, *arg):
        info = {}
        info['GMFlag'] = gameglobal.rds.configData.get('enableGuildBuildingTab', True)
        info['hasSpace'] = BigWorld.player().guild.hasSpace if BigWorld.player().guild else False
        info['spaceTips'] = gameStrings.TEXT_GUILDPROXY_1219
        return uiUtils.dict2GfxDict(info, True)

    def onGetTechnologyBaseInfo(self, *arg):
        guild = BigWorld.player().guild
        info = {}
        info['scale'] = guild.scale
        topInfo = []
        for scale, values in GSCD.data.iteritems():
            topInfoItem = {}
            topInfoItem['scale'] = scale
            topInfoItem['name'] = values.get('name', '')
            buffList = []
            buffIds = values.get('buffIds', ())
            for buffId in buffIds:
                sdData = SD.data.get(buffId, {})
                buffInfo = {}
                buffInfo['buffIcon'] = 'state/40/%d.dds' % sdData.get('iconId', 0)
                buffInfo['buffDesc'] = '%s<br>%s' % (sdData.get('name', ''), sdData.get('desc', ''))
                buffList.append(buffInfo)

            topInfoItem['buffList'] = buffList
            topInfo.append(topInfoItem)

        topInfo.sort(key=lambda x: x['scale'])
        info['topInfo'] = topInfo
        techList = []
        buildMap = {}
        self.techReverse = {}
        enableWingWorldGuildRoleOptimization = gameglobal.rds.configData.get('enableWingWorldGuildRoleOptimization', False)
        for techId, techData in GTD.data.iteritems():
            techInfo = {}
            techInfo['techId'] = techId
            techInfo['name'] = techData.get('name', '')
            techInfo['progress'] = techData.get('progress', 0)
            techInfo['desc'] = techData.get('desc' if not enableWingWorldGuildRoleOptimization else 'desc2', '')
            preTechId = techData.get('preTechId', 0)
            techInfo['preTechId'] = preTechId
            if preTechId:
                if preTechId not in self.techReverse:
                    self.techReverse[preTechId] = []
                self.techReverse[preTechId].append(techId)
            techInfo['pos'] = techData.get('pos', (0, 0))
            techInfo['iconPath'] = 'guildTech/40/%d.dds' % techData.get('icon', 0)
            pskillId = techData.get('pskillId', 0)
            skillName = GRPD.data.get((pskillId, 1), {}).get('name', '')
            if skillName != '':
                techInfo['pskillDesc'] = gameStrings.TEXT_GUILDPROXY_1267 % skillName
            scale = techData.get('scale', 0)
            buildingId = techData.get('buildingId', 0)
            if buildMap.has_key(buildingId):
                buildMap[buildingId] = max(buildMap[buildingId], techInfo['pos'][1] + 1)
            else:
                buildMap[buildingId] = techInfo['pos'][1] + 1
            techInfo['buildingId'] = buildingId
            techInfo['scale'] = scale
            techList.append(techInfo)

        info['techList'] = techList
        leftInfo = []
        for buildingId, height in buildMap.iteritems():
            itemInfo = {}
            baseData = GBD.data.get(buildingId, {})
            itemInfo['buildingId'] = buildingId
            itemInfo['name'] = baseData.get('name', '')
            itemInfo['techTips'] = baseData.get('techTips', '')
            itemInfo['height'] = height
            itemInfo['techSortId'] = baseData.get('techSortId', 0)
            leftInfo.append(itemInfo)

        leftInfo.sort(cmp=sort_technologyPanel)
        info['leftInfo'] = leftInfo
        return uiUtils.dict2GfxDict(info, True)

    def onGetTechnologyInfo(self, *arg):
        self.refreshTechnologyInfo()
        self.refreshTechnologyTopBar()

    def refreshTechnologyInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            info = []
            for techInfo in guild.technology.itervalues():
                itemInfo = {}
                itemInfo['techId'] = techInfo.techId
                itemInfo['state'] = techInfo.state
                baseInfo = GTD.data.get(techInfo.techId, {})
                if techInfo.state == 0:
                    if baseInfo.get('scale', 0) <= guild.scale:
                        preTechId = baseInfo.get('preTechId', 0)
                        if preTechId:
                            preInfo = guild.technology.get(preTechId, None)
                            if preInfo and preInfo.isAvail():
                                itemInfo['state'] = 1
                        else:
                            itemInfo['state'] = 1
                itemInfo['inResearching'] = techInfo.inResearching()
                currentValue = 100.0
                progressMax = baseInfo.get('progress', 0)
                if progressMax != 0 and progressMax > techInfo.progress:
                    currentValue = currentValue * techInfo.progress / progressMax
                itemInfo['currentValue'] = currentValue
                itemInfo['progressBarText'] = '%s/%s' % (format(techInfo.progress, ','), format(progressMax, ','))
                info.append(itemInfo)

            self.mediator.Invoke('refreshTechnologyInfo', uiUtils.array2GfxAarry(info, True))

    def refreshSingleTechnologyInfo(self, techId, needRecursion):
        if self.mediator:
            guild = BigWorld.player().guild
            techInfo = guild.technology.get(techId, None)
            if techInfo:
                itemInfo = {}
                itemInfo['techId'] = techInfo.techId
                itemInfo['state'] = techInfo.state
                baseInfo = GTD.data.get(techInfo.techId, {})
                if techInfo.state == 0:
                    if baseInfo.get('scale', 0) <= guild.scale:
                        preTechId = baseInfo.get('preTechId', 0)
                        if preTechId:
                            preInfo = guild.technology.get(preTechId, None)
                            if preInfo and preInfo.isAvail():
                                itemInfo['state'] = 1
                        else:
                            itemInfo['state'] = 1
                itemInfo['inResearching'] = techInfo.inResearching()
                currentValue = 100.0
                progressMax = baseInfo.get('progress', 0)
                if progressMax != 0 and progressMax > techInfo.progress:
                    currentValue = currentValue * techInfo.progress / progressMax
                itemInfo['currentValue'] = currentValue
                itemInfo['progressBarText'] = '%s/%s' % (format(techInfo.progress, ','), format(progressMax, ','))
                self.mediator.Invoke('refreshSingleTechnologyInfo', uiUtils.dict2GfxDict(itemInfo, True))
            if needRecursion and techId in self.techReverse:
                for fid in self.techReverse[techId]:
                    self.refreshSingleTechnologyInfo(fid, False)

    def refreshTechnologyTopBar(self):
        if self.mediator:
            guild = BigWorld.player().guild
            info = {}
            currentValue = 100.0
            upScaleBtnEnabled = True
            upScaleBtnVisible = True
            if guild.scale >= const.GUILD_SCALE_MAX:
                scaleProgressBarText = gameStrings.TEXT_GUILDPROXY_996 % format(guild.prosperity, ',')
                upScaleBtnEnabled = False
                upScaleBtnVisible = False
            else:
                progressMax = GSCD.data.get(guild.scale + 1).get('prosperity', 0)
                progressPreMax = GSCD.data.get(guild.scale).get('prosperity', 0)
                progressDif = progressMax - progressPreMax
                if progressMax and progressMax > guild.prosperity and progressDif > 0:
                    currentValue = currentValue * (guild.prosperity - progressPreMax) / progressDif
                    upScaleBtnEnabled = False
                currentValue = (guild.scale - 1 + currentValue / 100.0) * (100.0 / const.GUILD_SCALE_MAX)
                scaleProgressBarText = gameStrings.TEXT_GUILDPROXY_1004 % (format(guild.prosperity, ','), format(progressMax, ','))
            info['scale'] = guild.scale
            info['scaleProgressBarText'] = scaleProgressBarText
            info['scaleCurrentValue'] = currentValue
            info['upScaleBtnEnabled'] = upScaleBtnEnabled and self.checkAuthorization(gametypes.GUILD_ACTION_UPGRADE, False)
            info['upScaleBtnVisible'] = upScaleBtnVisible
            self.mediator.Invoke('refreshTechnologyTopBar', uiUtils.dict2GfxDict(info, True))

    def onTechResearch(self, *arg):
        techId = int(arg[3][0].GetNumber())
        if self.checkAuthorization(gametypes.GUILD_ACTION_RESEARCH):
            gameglobal.rds.ui.guildTechResearch.show(techId)
        else:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_AUTHORIZATION_FAILED, ())

    def onGetZhanQiInfo(self, *arg):
        self.initHeadGen()
        self.takePhoto3D()

    def initHeadGen(self):
        if not self.flagGen:
            self.flagGen = capturePhoto.GuildZhanQiPhotoGen.getInstance('gui/taskmask.tga', 422)
        self.flagGen.initFlashMesh()
        if not self.armorGen:
            self.armorGen = capturePhoto.GuildZhanPaoPhotoGen.getInstance('gui/taskmask.tga', 422)
        self.armorGen.initFlashMesh()

    def takePhoto3D(self, modelId = gameglobal.CLAN_WAR_FLAG_DEFAULT_MODEL, tintMs = None, photoAction = None):
        if not self.flagGen:
            self.flagGen = capturePhoto.GuildZhanQiPhotoGen.getInstance('gui/taskmask.tga', 422)
        self.flagGen.startCapture(modelId, tintMs, ('1101',))
        if not self.armorGen:
            self.armorGen = capturePhoto.GuildZhanPaoPhotoGen.getInstance('gui/taskmask.tga', 422)
        p = BigWorld.player()
        mpr = charRes.MultiPartRes()
        mpr.queryByAttribute(p.realPhysique, p.realAspect, False, p.avatarConfig, True)
        res = mpr.getPrerequisites()
        self.armorGen.startCaptureEntAndRes(p, res)

    def resetHeadGen(self):
        if self.flagGen:
            self.flagGen.endCapture()
        if self.armorGen:
            self.armorGen.endCapture()

    def updateFlag(self):
        p = BigWorld.player()
        if self.mediator and p.guildNUID and p.guildFlag:
            icon, color = uiUtils.getGuildFlag(p.guildFlag)
            self.mediator.Invoke('updateFlag', (GfxValue(uiUtils.getGuildIconPath(icon)), GfxValue(color)))

    def dyeArmorPhoto(self, color):
        if self.armorGen:
            model = self.armorGen.adaptor.attachment
            if model:
                player = BigWorld.player()
                aspect = copy.deepcopy(player.realAspect)
                equipId = aspect.clanWarArmor
                aspect.set(gametypes.EQU_PART_CLAN_WAR_ARMOR, equipId, color)
                mpr = charRes.MultiPartRes()
                mpr.queryByAttribute(player.realPhysique, aspect, False, player.avatarConfig, True)
                dyesDict = mpr.getDyeDict(aspect, False, True)
                m = avatarMorpher.SimpleModelMorpher(model, player.realPhysique.sex, player.realPhysique.school, player.realPhysique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, dyesDict)
                m.readConfig(player.realAvatarConfig)
                m.applyDyeMorph(True)

    def onShowArmorSetting(self, *arg):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_ARMOR_SETTING)

    def onShowFlagSetting(self, *arg):
        gameglobal.rds.ui.zhanQi.show()

    def onSelectStatisticsMode(self, *arg):
        intervalType = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if not p.guild:
            return
        p.cell.queryGuildStats(intervalType, p.guild.statsVer.get(intervalType, 0))

    def refreshStatisticsInfo(self, intervalType):
        if self.mediator:
            enableGuildRewardSalary = gameglobal.rds.configData.get('enableGuildRewardSalary', False)
            isGuildLeader = BigWorld.player().guild.leaderGbId == BigWorld.player().gbId
            self.intervalType = intervalType
            p = BigWorld.player()
            guild = p.guild
            guildMembers = guild.stats.get(intervalType, {})
            memberList = []
            now = utils.getNow()
            for gbId, member in guild.member.iteritems():
                value = guildMembers.get(gbId, None)
                memberInfo = {}
                memberInfo['nameText'] = member.role
                memberInfo['gbId'] = gbId
                memberInfo['showSalaryOption'] = enableGuildRewardSalary and isGuildLeader
                memberInfo['assigned'] = False
                memberInfo['matchJoinCondintion'] = now - member.tJoin - const.GUILD_PAY_JOIN_TIME >= 0
                memberInfo['online'] = member.online
                if value:
                    memberInfo['build'] = value.action.get(gametypes.GUILD_STATS_BUILD, 0)
                    memberInfo['business'] = value.action.get(gametypes.GUILD_STATS_ACTION_TRADE, 0)
                    memberInfo['wine'] = value.action.get(gametypes.GUILD_STATS_ACTION_MAKE_WINE, 0)
                    memberInfo['tired'] = value.action.get(gametypes.GUILD_STATS_ACTION_TIRED, 0)
                    memberInfo['run'] = value.action.get(gametypes.GUILD_STATS_ACTION_LOOP, 0)
                    memberInfo['war'] = value.action.get(gametypes.GUILD_STATS_ACTION_CLANWAR, 0)
                    memberInfo['leagueMatch'] = 0
                    memberInfo['signIn'] = value.action.get(gametypes.GUILD_STATS_SIGN_IN, 0)
                    memberInfo['weekActivation'] = value.action.get(gametypes.GUILD_STATS_WEEK_ACTIVATION, 0) / 1000
                    memberInfo['contrib'] = value.contrib
                else:
                    memberInfo['build'] = 0
                    memberInfo['business'] = 0
                    memberInfo['wine'] = 0
                    memberInfo['tired'] = 0
                    memberInfo['run'] = 0
                    memberInfo['war'] = 0
                    memberInfo['leagueMatch'] = 0
                    memberInfo['signIn'] = 0
                    memberInfo['weekActivation'] = 0
                    memberInfo['contrib'] = 0
                memberList.append(memberInfo)

            memberList.sort(cmp=STATISTICS_SORT_MAP[self.statisticsSortType][0], reverse=STATISTICS_SORT_MAP[self.statisticsSortType][1] if self.statisticsAscendSorted else not STATISTICS_SORT_MAP[self.statisticsSortType][1])
            info = {}
            info['memberList'] = memberList
            info['sortType'] = self.statisticsSortType
            info['ascendSorted'] = self.statisticsAscendSorted
            info['mode'] = self.intervalType
            info['enableAssignSalary'] = enableGuildRewardSalary and isGuildLeader
            info['enableGuildSignIn'] = gameglobal.rds.configData.get('enableGuildSignIn', False)
            self.mediator.Invoke('refreshStatisticsInfo', uiUtils.dict2GfxDict(info, True))

    def onSetStatisticsSort(self, *arg):
        if self.statisticsSortType == int(arg[3][0].GetString()) and self.statisticsAscendSorted == arg[3][1].GetBool():
            return
        self.statisticsSortType = int(arg[3][0].GetString())
        self.statisticsAscendSorted = arg[3][1].GetBool()
        self.refreshStatisticsInfo(self.intervalType)

    def onGetEnemyInfo(self, *arg):
        self.refreshEnemyInfo()
        p = BigWorld.player()
        if not p.guild:
            return
        p.cell.queryGuildPkEnemy(p.guild.pkEnemyVer)

    def refreshEnemyInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            clanIdx = 0
            clanList = list(guild.clanEnemy)
            guildIdx = 0
            guildList = list(guild.guildEnemy)
            clanInfoList = []
            guildInfoList = []
            maxLevel = len(GLD.data)
            lastClanEnemyNum = 0
            lastGuildEnemyNum = 0
            for i in xrange(1, maxLevel + 1):
                ldata = GLD.data.get(i, {})
                clanEnemyNum = ldata.get('clanEnemyNum', 0)
                if lastClanEnemyNum < clanEnemyNum:
                    clanInfo = {}
                    if guild.level < i:
                        clanInfo['enabled'] = False
                        clanInfo['text'] = uiUtils.toHtml(gameStrings.TEXT_GUILDPROXY_1557 % i, '#F43804')
                    else:
                        clanInfo['enabled'] = True
                        if len(clanList) <= clanIdx:
                            clanInfo['text'] = ''
                        else:
                            clan = guild.clanEnemy.get(clanList[clanIdx], None)
                            if clan:
                                clanInfo['text'] = clan[0]
                                self.clanNameMap[clanInfo['text']] = clanList[clanIdx]
                                self.clanGuildList[clanList[clanIdx]] = clan[1]
                            else:
                                clanInfo['text'] = ''
                    clanInfoList.append(clanInfo)
                    clanIdx += 1
                    lastClanEnemyNum = clanEnemyNum
                guildEnemyNum = ldata.get('guildEnemyNum', 0)
                if lastGuildEnemyNum < guildEnemyNum or not gameglobal.rds.configData.get('enableClan', False):
                    guildInfo = {}
                    if guild.level < i:
                        guildInfo['enabled'] = False
                        guildInfo['text'] = uiUtils.toHtml(gameStrings.TEXT_GUILDPROXY_1557 % i, '#F43804')
                    else:
                        guildInfo['enabled'] = True
                        if len(guildList) <= guildIdx:
                            guildInfo['text'] = ''
                        else:
                            guildInfo['text'] = guild.guildEnemy.get(guildList[guildIdx], '')
                            self.guildNameMap[guildInfo['text']] = {'guildNUID': guildList[guildIdx]}
                    guildInfoList.append(guildInfo)
                    guildIdx += 1
                    lastGuildEnemyNum = guildEnemyNum

            info = {}
            info['clanInfoList'] = clanInfoList
            info['guildInfoList'] = guildInfoList
            info['bEnemy'] = self.checkAuthorization(gametypes.GUILD_ACTION_PK_ENEMY)
            self.mediator.Invoke('refreshEnemyInfo', uiUtils.dict2GfxDict(info, True))

    def stopSearchClanTimer(self):
        if self.searchClanTimer:
            BigWorld.cancelCallback(self.searchClanTimer)
            self.searchClanTimer = None

    def onSearchClan(self, *arg):
        queryStr = unicode2gbk(arg[3][0].GetString())
        mcName = arg[3][1].GetString()
        mcIdx = int(mcName[-1:])
        self.stopSearchClanTimer()
        if queryStr in self.searchClanCache:
            self.searchClanBack(queryStr, self.searchClanCache[queryStr], mcIdx)
        else:
            self.searchClanTimer = BigWorld.callback(1, Functor(self.callbackSearchClan, queryStr, mcIdx))

    def callbackSearchClan(self, queryStr, mcIdx):
        BigWorld.player().cell.searchClan(queryStr, mcIdx)

    def searchClanBack(self, queryStr, data, mcIdx):
        if self.mediator:
            self.searchClanCache[queryStr] = data
            names = []
            for dataItem in data:
                names.append(dataItem[1])
                self.clanNameMap[dataItem[1]] = dataItem[0]

            info = {}
            info['names'] = names
            info['mcIdx'] = mcIdx
            self.mediator.Invoke('refreshSearchClanInfo', uiUtils.dict2GfxDict(info, True))

    def stopSearchGuildTimer(self):
        if self.searchGuildTimer:
            BigWorld.cancelCallback(self.searchGuildTimer)
            self.searchGuildTimer = None

    def onSearchGuild(self, *arg):
        queryStr = unicode2gbk(arg[3][0].GetString())
        mcName = arg[3][1].GetString()
        mcIdx = int(mcName[-1:])
        self.stopSearchGuildTimer()
        if queryStr in self.searchGuildCache:
            self.searchGuildBack(queryStr, self.searchGuildCache[queryStr], mcIdx)
        else:
            self.searchGuildTimer = BigWorld.callback(1, Functor(self.callbackSearchGuild, queryStr, mcIdx))

    def callbackSearchGuild(self, queryStr, mcIdx):
        BigWorld.player().cell.searchGuild(queryStr, mcIdx)

    def searchGuildBack(self, queryStr, data, mcIdx):
        if self.mediator:
            self.searchGuildCache[queryStr] = data
            names = []
            for dataItem in data:
                names.append(dataItem[1])
                self.guildNameMap[dataItem[1]] = {'guildNUID': dataItem[0]}

            info = {}
            info['names'] = names
            info['mcIdx'] = mcIdx
            self.mediator.Invoke('refreshSearchGuildInfo', uiUtils.dict2GfxDict(info, True))

    def onSaveEnemy(self, *arg):
        p = BigWorld.player()
        if not p.guild:
            return
        enableGuildEnemy = gameglobal.rds.configData.get('enableGuildEnemy', False)
        if not enableGuildEnemy:
            p.showGameMsg(GMDD.data.GUILD_ENEMY_CLOSED, ())
            return
        clanNum = int(arg[3][0].GetNumber())
        clanList = arg[3][1]
        guildNum = int(arg[3][2].GetNumber())
        guildList = arg[3][3]
        clanNUIDs = []
        for i in xrange(clanNum):
            name = unicode2gbk(clanList.GetElement(i).GetString())
            if name == '':
                continue
            clanNUID = self.clanNameMap.get(name, 0)
            if clanNUID != 0:
                clanNUIDs.append(clanNUID)
            else:
                p.showGameMsg(GMDD.data.CLAN_NAME_NOT_EXIST, (name,))
                return

        guildNUIDs = []
        for i in xrange(guildNum):
            name = unicode2gbk(guildList.GetElement(i).GetString())
            if name == '':
                continue
            guildNUID = self.guildNameMap.get(name, {}).get('guildNUID', 0)
            if guildNUID != 0:
                guildNUIDs.append(guildNUID)
            else:
                p.showGameMsg(GMDD.data.GUILD_NAME_NOT_EXIST, (name,))
                return

        newGuildEnemy, newClanEnemy = set(guildNUIDs), set(clanNUIDs)
        oldGuildEnemy, oldClanEnemy = p.guild.enemyGuildNUIDs, p.guild.enemyClanNUIDs
        if not oldGuildEnemy:
            guildToAdd = newGuildEnemy
            guildToDel = ()
        else:
            guildToAdd = newGuildEnemy.difference(oldGuildEnemy)
            guildToDel = oldGuildEnemy.difference(newGuildEnemy)
        if not oldClanEnemy:
            clanToAdd = newClanEnemy
            clanToDel = ()
        else:
            clanToAdd = newClanEnemy.difference(oldClanEnemy)
            clanToDel = oldClanEnemy.difference(newClanEnemy)
        if not guildToAdd and not guildToDel and not clanToAdd and not clanToDel:
            p.showGameMsg(GMDD.data.GUILD_PK_ENEMY_NO_CHANGE, ())
            return
        guildToAddLen = len(guildToAdd)
        clanToAddLen = len(clanToAdd)
        bindCash = commGuild.calcPkEnemyCost(guildToAddLen, clanToAddLen)
        if bindCash > 0:
            if gameglobal.rds.configData.get('enableClan', False):
                msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_ENEMY_CHANGE_HINT, '%d %d %s') % (guildToAddLen, clanToAddLen, format(bindCash, ','))
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_GUILD_ENEMY_CHANGE_HINT, '%d %s') % (guildToAddLen, format(bindCash, ','))
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.updateGuildPkEnemy, guildNUIDs, clanNUIDs))
        else:
            p.cell.updateGuildPkEnemy(guildNUIDs, clanNUIDs)

    def onGetClanGuilds(self, *arg):
        clanName = unicode2gbk(arg[3][0].GetString())
        clanNUID = self.clanNameMap.get(clanName, 0)
        if clanNUID == 0:
            return
        if clanNUID not in self.clanGuildList:
            self.clanGuildList[clanNUID] = []
            BigWorld.player().cell.getClanGuilds(clanNUID, 0)

    def updateClanGuilds(self, clanNUID, data, useFor):
        self.clanGuildList[clanNUID] = data

    def onGetGuildListTips(self, *arg):
        clanName = unicode2gbk(arg[3][0].GetString())
        clanNUID = self.clanNameMap.get(clanName, 0)
        noData = False
        guildList = []
        if clanNUID == 0 or clanNUID not in self.clanGuildList:
            noData = True
        else:
            for guildName, guildMemberNum in self.clanGuildList[clanNUID]:
                guildInfo = {}
                guildInfo['guildName'] = guildName
                guildInfo['guildMemberNum'] = guildMemberNum
                guildList.append(guildInfo)

        info = {}
        info['noData'] = noData
        info['guildList'] = guildList
        return uiUtils.dict2GfxDict(info, True)

    def onOpenRewardSalaryHistory(self, *arg):
        gbId = arg[3][0].GetString()
        role = arg[3][1].GetString()
        gameglobal.rds.ui.guildRewardSalaryHistory.show(gbId, role)

    def onAssignRewardPayment(self, *arg):
        members = arg[3][0].GetString()
        if members == '':
            memberArr = []
        else:
            memberArr = members.split(',')
        gameglobal.rds.ui.guildRewardSalaryAssign.show(memberArr)

    def onGetChallengeInfo(self, *arg):
        self.refreshChallengeInfo(True)

    def refreshChallengeInfo(self, needRefreshChallengeList):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            info = {}
            info['challengeHint'] = GCD.data.get('challengeHint', '')
            challengeInfo = guild.challengeInfo
            state = uiConst.GUILD_CHALLENGE_ERROR
            status = challengeInfo.get('status', 0)
            if status in (gametypes.GUILD_CHALLENGE_STATUS_DEFAULT, gametypes.GUILD_CHALLENGE_STATUS_APPLYING):
                state = uiConst.GUILD_CHALLENGE_CHALLENGE
            elif status == gametypes.GUILD_CHALLENGE_STATUS_APPLIED:
                state = uiConst.GUILD_CHALLENGE_BECHALLENGE
                info['enemyGuildName'] = gameStrings.TEXT_GUILDPROXY_1789 % challengeInfo.get('enemyName', '')
                locationList = []
                for fbNo, fbValue in GCHD.data.iteritems():
                    locationInfo = {}
                    numLimit = fbValue.get('numLimit', 0) / 2
                    locationInfo['label'] = fbValue.get('name', '%s') % ('%dvs%d' % (numLimit, numLimit))
                    locationInfo['fbNo'] = fbNo
                    locationList.append(locationInfo)

                info['locationList'] = locationList
                info['enableRejectGuildChallenge'] = gameglobal.rds.configData.get('enableRejectGuildChallenge', False)
            elif status in (gametypes.GUILD_CHALLENGE_STATUS_PREPARE, gametypes.GUILD_CHALLENGE_STATUS_START):
                state = uiConst.GUILD_CHALLENGE_FIGHTING
                if status == gametypes.GUILD_CHALLENGE_STATUS_PREPARE:
                    info['titleField'] = gameStrings.TEXT_GUILDPROXY_1803
                    info['canEnter'] = False
                else:
                    info['titleField'] = gameStrings.TEXT_GUILDPROXY_1806
                    info['canEnter'] = True
                info['guildName'] = challengeInfo.get('enemyName', '')
                fbValue = GCHD.data.get(challengeInfo.get('fbNo', 0), {})
                info['location'] = fbValue.get('name', '%s') % ''
                numLimit = fbValue.get('numLimit', 0) / 2
                info['challengeScale'] = '%d vs %d' % (numLimit, numLimit)
                info['memberNum'] = '%d vs %d' % (challengeInfo.get('memberNum', 0), challengeInfo.get('enemyMemberNum', 0))
                info['enterBtnNum'] = len(fbValue.get('campPos', {}).get('1', []))
            info['state'] = state
            self.mediator.Invoke('refreshChallengeInfo', uiUtils.dict2GfxDict(info, True))
            self.stopChallengeTimer()
            self.onChallengeTimer()
            if needRefreshChallengeList:
                self.refreshChallengeListInfo(self.version, self.challengeResultlist)
                self.getGuildChallengeResult()

    @ui.callFilter(6, False)
    def getGuildChallengeResult(self):
        BigWorld.player().cell.queryGuildChallengeResult(self.version)
        BigWorld.player().cell.queryMyGuildChallengeResult(self.buffVersion)

    def refreshChallengeListInfo(self, version, data):
        self.version = version
        self.challengeResultlist = data
        if self.mediator:
            resultList = []
            for dataItem in data:
                resultInfo = {}
                resultInfo['names'] = gameStrings.TEXT_GUILDPROXY_1839 % (dataItem.get('srcGuildName', ''), dataItem.get('tgtGuildName', ''))
                fbNo = dataItem.get('fbNo', 0)
                if fbNo == 0:
                    resultInfo['location'] = gameStrings.TEXT_GUILDPROXY_1842
                else:
                    fbValue = GCHD.data.get(fbNo, {})
                    numLimit = fbValue.get('numLimit', 0) / 2
                    resultInfo['location'] = fbValue.get('name', '%s') % ('%dvs%d' % (numLimit, numLimit))
                resultInfo['winner'] = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_660 % dataItem.get('winGuildName', '')
                resultList.append(resultInfo)

            info = {}
            info['resultList'] = resultList
            self.mediator.Invoke('refreshChallengeListInfo', uiUtils.dict2GfxDict(info, True))

    def refreshBuffListInfo(self, version, data):
        self.buffVersion = version
        self.buffResultlist = data
        self.stopChallengeTimer()
        self.onChallengeTimer()

    def stopChallengeTimer(self):
        if self.challengeTimer:
            BigWorld.cancelCallback(self.challengeTimer)
            self.challengeTimer = None

    def onChallengeTimer(self):
        if self.mediator:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            challengeInfo = guild.challengeInfo
            serverTime = p.getServerTime()
            info = {}
            needTimer = False
            status = challengeInfo.get('status', 0)
            if status in (gametypes.GUILD_CHALLENGE_STATUS_DEFAULT, gametypes.GUILD_CHALLENGE_STATUS_APPLYING):
                applyChallengeInterval = GCD.data.get('applyChallengeInterval', 0)
                guildChallengeResponseLimit = GCD.data.get('guildChallengeResponseLimit', 30)
                challengeTimestamp = challengeInfo.get('challengeTimestamp', 0)
                leftTime = int(challengeTimestamp + applyChallengeInterval - serverTime)
                if leftTime <= 0:
                    info['challengeCDTime'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                else:
                    info['challengeCDTime'] = uiUtils.formatTime(leftTime)
                    needTimer = True
                leftTime = int(challengeTimestamp + guildChallengeResponseLimit - serverTime)
                if leftTime <= 0:
                    info['challengeSuccessTime'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                    info['challengeSuccess'] = False
                else:
                    info['challengeSuccessTime'] = uiUtils.formatTime(leftTime)
                    info['challengeSuccess'] = status != gametypes.GUILD_CHALLENGE_STATUS_DEFAULT
                    needTimer = True
                info['buffVisible'] = False
                buffList = []
                for dataItem in self.buffResultlist:
                    leftTime = int(dataItem.get('endTimestamp', 0) + const.TIME_INTERVAL_DAY - serverTime)
                    if leftTime <= 0:
                        continue
                    ratio = int(GCPD.data.get((dataItem.get('winLv', 0), dataItem.get('loseLv', 0)), {}).get('ratio', 0) * 100)
                    if ratio == 0:
                        continue
                    buffInfo = {}
                    winGuildName = dataItem.get('winGuildName', '')
                    if winGuildName == guild.name:
                        buffInfo['flag'] = 'win'
                        loseGuildName = dataItem.get('srcGuildName', '')
                        if loseGuildName == winGuildName:
                            loseGuildName = dataItem.get('tgtGuildName', '')
                        buffInfo['title'] = gameStrings.TEXT_GUILDPROXY_1911 % (loseGuildName, ratio)
                    else:
                        buffInfo['flag'] = 'lose'
                        buffInfo['title'] = gameStrings.TEXT_GUILDPROXY_1914 % (winGuildName, ratio)
                    buffInfo['time'] = uiUtils.formatTime(leftTime)
                    buffList.append(buffInfo)
                    info['buffVisible'] = True
                    needTimer = True

                info['buffList'] = buffList
            elif status == gametypes.GUILD_CHALLENGE_STATUS_APPLIED:
                guildChallengeResponseLimit = GCD.data.get('guildChallengeResponseLimit', 30)
                leftTime = int(challengeInfo.get('srcChallengeTimestamp', 0) + guildChallengeResponseLimit - serverTime)
                if leftTime <= 0:
                    info['challengeResponseTime'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                    info['challengeResponse'] = False
                else:
                    info['challengeResponseTime'] = uiUtils.formatTime(leftTime)
                    info['challengeResponse'] = True
                    needTimer = True
            elif status == gametypes.GUILD_CHALLENGE_STATUS_PREPARE:
                fbValue = GCHD.data.get(challengeInfo.get('fbNo', 0), {})
                leftTime = int(challengeInfo.get('tOccupy', 0) + fbValue.get('readyTime', 0) - serverTime)
                if leftTime <= 0:
                    info['challengeOccupyTime'] = gameStrings.TEXT_BATTLEFIELDPROXY_1605
                    info['challengeOccupy'] = False
                else:
                    info['challengeOccupyTime'] = uiUtils.formatTime(leftTime)
                    info['challengeOccupy'] = True
                    needTimer = True
            self.mediator.Invoke('refreshChallengeTime', uiUtils.dict2GfxDict(info, True))
            if needTimer:
                self.challengeTimer = BigWorld.callback(1, self.onChallengeTimer)

    def stopChallengeSearchTimer(self):
        if self.challengeSearchTimer:
            BigWorld.cancelCallback(self.challengeSearchTimer)
            self.challengeSearchTimer = None

    def onChallengeSearch(self, *arg):
        queryStr = unicode2gbk(arg[3][0].GetString())
        self.stopChallengeSearchTimer()
        if queryStr in self.challengeSearchCache:
            self.challengeSearchBack(queryStr, self.challengeSearchCache[queryStr])
        else:
            self.challengeSearchTimer = BigWorld.callback(1, Functor(self.callbackChallengeSearch, queryStr))

    def callbackChallengeSearch(self, queryStr):
        BigWorld.player().cell.queryAllGuildLimitInfo(queryStr)

    def challengeSearchBack(self, queryStr, data):
        if self.mediator:
            self.challengeSearchCache[queryStr] = data
            names = []
            for dataItem in data:
                guildNUID = dataItem.get('guildNUID', 0)
                guildName = dataItem.get('guildName', '')
                guildLv = dataItem.get('guildLv', 0)
                names.append(guildName)
                self.guildNameMap[guildName] = {'guildNUID': guildNUID,
                 'guildLv': guildLv}

            info = {}
            info['names'] = names
            self.mediator.Invoke('refreshChallengeSearchInfo', uiUtils.dict2GfxDict(info, True))

    def challengeBuffIsValid(self, timestamp):
        isValid = False
        applyValidTimeStart = GCD.data.get('applyValidTimeStart', ())
        applyValidTimeEnd = GCD.data.get('applyValidTimeEnd', ())
        if len(applyValidTimeStart) != len(applyValidTimeEnd):
            return False
        for index in xrange(len(applyValidTimeStart)):
            if utils.inSimpleTimeRange(applyValidTimeStart[index], applyValidTimeEnd[index], timestamp):
                isValid = True
                break

        return isValid

    def onChallenge(self, *arg):
        guildName = unicode2gbk(arg[3][0].GetString())
        guildInfo = self.guildNameMap.get(guildName, {})
        guildNUID = guildInfo.get('guildNUID', 0)
        guildLv = guildInfo.get('guildLv', 0)
        p = BigWorld.player()
        if not p.guild:
            return
        if guildNUID == p.guildNUID:
            p.showGameMsg(GMDD.data.APPLY_GUILD_CHALLENGE_FAILED_SELF_GUILD, ())
            return
        if guildNUID != 0:
            if self.challengeBuffIsValid(p.getServerTime()):
                winRatio = int(GCPD.data.get((p.guild.level, guildLv), {}).get('ratio', 0) * 100)
                loseRatio = int(GCPD.data.get((guildLv, p.guild.level), {}).get('ratio', 0) * 100)
                msg = uiUtils.getTextFromGMD(GMDD.data.APPLY_GUILD_CHALLENGE_DETAIL_INFO_PUNISH, '%s %d %d %d') % (guildName,
                 guildLv,
                 winRatio,
                 loseRatio)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.applyGuildChallenge, guildNUID, guildName))
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.APPLY_GUILD_CHALLENGE_DETAIL_INFO, '%s %d') % (guildName, guildLv)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.applyGuildChallenge, guildNUID, guildName))
        else:
            p.showGameMsg(GMDD.data.GUILD_NAME_NOT_EXIST, (guildName,))

    def onAcceptChallenge(self, *arg):
        fbNo = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if not p.guild:
            return
        challengeInfo = p.guild.challengeInfo
        enemyGuildNUID = challengeInfo.get('enemyGuildNUID', 0)
        fbValue = GCHD.data.get(fbNo, {})
        if enemyGuildNUID and fbValue:
            numLimit = fbValue.get('numLimit', 0) / 2
            location = fbValue.get('name', '%s') % ('%dvs%d' % (numLimit, numLimit))
            if self.challengeBuffIsValid(challengeInfo.get('srcChallengeTimestamp', 0)):
                guildLv = challengeInfo.get('enemyGuildLv', 0)
                winRatio = int(GCPD.data.get((p.guild.level, guildLv), {}).get('ratio', 0) * 100)
                loseRatio = int(GCPD.data.get((guildLv, p.guild.level), {}).get('ratio', 0) * 100)
                msg = uiUtils.getTextFromGMD(GMDD.data.ACCEPT_GUILD_CHALLENGE_PUNISH, '%s %s %d %d') % (location,
                 challengeInfo.get('enemyName', ''),
                 winRatio,
                 loseRatio)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.acceptGuildChallenge, enemyGuildNUID, fbNo))
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.ACCEPT_GUILD_CHALLENGE, '%s %s') % (location, challengeInfo.get('enemyName', ''))
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.acceptGuildChallenge, enemyGuildNUID, fbNo))

    def onRejectChallenge(self, *arg):
        p = BigWorld.player()
        if not p.guild:
            return
        challengeInfo = p.guild.challengeInfo
        enemyGuildNUID = challengeInfo.get('enemyGuildNUID', 0)
        if enemyGuildNUID:
            msg = uiUtils.getTextFromGMD(GMDD.data.REJECT_GUILD_CHALLENGE, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.rejectGuildChallenge, enemyGuildNUID))

    def onSurrenderChallenge(self, *arg):
        p = BigWorld.player()
        if not p.guild:
            return
        challengeInfo = p.guild.challengeInfo
        enemyGuildNUID = challengeInfo.get('enemyGuildNUID', 0)
        if enemyGuildNUID:
            if self.challengeBuffIsValid(challengeInfo.get('srcChallengeTimestamp', 0)):
                guildLv = challengeInfo.get('enemyGuildLv', 0)
                loseRatio = int(GCPD.data.get((guildLv, p.guild.level), {}).get('ratio', 0) * 100)
                msg = uiUtils.getTextFromGMD(GMDD.data.SURRENDER_GUILD_CHALLENGE_PUNISH, '%s %d') % (challengeInfo.get('enemyName', ''), loseRatio)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.surrenderGuildChallenge, enemyGuildNUID))
            else:
                msg = uiUtils.getTextFromGMD(GMDD.data.SURRENDER_GUILD_CHALLENGE, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.surrenderGuildChallenge, enemyGuildNUID))

    def onInitChallenge(self, *args):
        self.uiAdapter.clanChallenge.initPanel(args[3][0])

    def onUnRegisterChallenge(self, *args):
        self.uiAdapter.clanChallenge.unRegisterPanel()

    def onEnterChallenge(self, *arg):
        name = arg[3][0].GetString()
        index = int(name[-1:])
        p = BigWorld.player()
        if not p.guild:
            return
        p.cell.enterGuildChallenge(p.guild.challengeInfo.get('fbNo', 0), index)

    def checkChallengePushMsg(self):
        if not gameglobal.rds.configData.get('enableGuildChallenge', False):
            return
        guild = BigWorld.player().guild
        if guild and guild.challengeInfo.get('status', 0) == gametypes.GUILD_CHALLENGE_STATUS_APPLIED:
            if self.checkAuthorization(gametypes.GUILD_ACTION_GUILD_CHALLENGE):
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_CHALLENGE)
                gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_CHALLENGE, {'click': Functor(self.showAssignTab, uiConst.GUILDINFO_TAB_CHALLENGE)})
                return
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_CHALLENGE)

    def onGetTournamentInfo(self, *arg):
        self.refreshTournamentInfo()
        self.getTournamentSimpleInfo()
        self.getRankTournamentSimpleInfo()

    def onGetWWTournamentInfo(self, *arg):
        self.getTournamentSimpleInfo()
        self.getRankTournamentSimpleInfo()
        self.queryRankTournamentGuildInfo()
        self.refreshWWTournamentInfo()

    def getWeekOffset(self, nowDay, targetDay):
        if targetDay >= nowDay:
            offset = targetDay - nowDay
        else:
            offset = 7 - nowDay + targetDay
        return offset

    def isEnableRound34(self):
        return self.getEnableRankTournament()

    def refreshWWTournamentInfo(self):
        if not self.mediator:
            return
        if self.getEnableRankTournament():
            self.refreshRankTournamentInfo()
            self.refreshGtnInspireCoolDown()
        else:
            self.refreshBaseWWTournamentInfo()

    def refreshBaseWWTournamentInfo(self):
        p = BigWorld.player()
        timeData = getGTNSD().data
        infor = {}
        now = utils.getNow()
        localTime = time.localtime(now)
        infor['weekDay'] = time.strftime('%w', localTime)
        firstRoundDay = int(timeData.get(5, {}).get('crontab', '').split(' ')[-1]) + 1
        offset = self.getWeekOffset(int(infor['weekDay']), firstRoundDay)
        infor['roundDate'] = time.strftime('%Y-%m-%d', time.localtime(now + offset * 24 * 3600))
        infor['prepare0'] = timeData.get(5, {}).get('readyTime', '')
        infor['start0'] = timeData.get(5, {}).get('startTime', '')
        infor['end0'] = timeData.get(5, {}).get('endTime', '')
        infor['prepare1'] = timeData.get(6, {}).get('readyTime', '')
        infor['start1'] = timeData.get(6, {}).get('startTime', '')
        infor['end1'] = timeData.get(6, {}).get('endTime', '')
        infor['currState'] = ''
        trainApplyCrontab = timeData.get(9, {}).get('crontab', '')
        trainApplyTime = utils.getDisposableCronTabTimeStamp(trainApplyCrontab)
        infor['trainApplyTime'] = time.strftime('%H:%M', time.localtime(trainApplyTime))
        trainStartCrontab = timeData.get(10, {}).get('crontab', '')
        trainStartTime = utils.getDisposableCronTabTimeStamp(trainStartCrontab)
        infor['trainStartTime'] = time.strftime('%H:%M', time.localtime(trainStartTime))
        trainEndTime = trainStartTime + 1500
        infor['trainEndTime'] = time.strftime('%H:%M', time.localtime(trainEndTime))
        guildTournament = p.guildTournament.get(gametypes.GUILD_TOURNAMENT_GROUP_QL)
        infor['isInTrainApply'] = guildTournament.trainingState == gametypes.GUILD_TOURNAMENT_TRAINING_STATE_APPLY
        infor['isInTrainStart'] = guildTournament.trainingState == gametypes.GUILD_TOURNAMENT_TRAINING_STATE_MATCH
        nowLocalTime = time.localtime(now)
        trainLocalEndTime = time.localtime(trainEndTime)
        infor['isInTrainEnd'] = not infor['isInTrainApply'] and not infor['isInTrainStart'] and nowLocalTime.tm_mday == trainLocalEndTime.tm_mday and nowLocalTime.tm_hour * 60 + nowLocalTime.tm_min > trainLocalEndTime.tm_hour * 60 + trainLocalEndTime.tm_min
        infor['trainApplyTxt'] = gameStrings.TRAIN_APPLY_TXT
        infor['trainStartTxt'] = gameStrings.TRAIN_START_TXT
        infor['trainEndTxt'] = gameStrings.TRAIN_END_TXT
        infor['trainGroupRule'] = GMD.data.get(GMDD.data.GUILD_TOURNAMENT_TRAIN_GROUP_RULE, {}).get('text', '')
        infor['trainPeopleNumRule'] = GMD.data.get(GMDD.data.GUILD_TOURNAMENT_TRAIN_PEOPLE_NUM_RULE, {}).get('text', '')
        infor['trainConditionRule'] = GMD.data.get(GMDD.data.GUILD_TOURNAMENT_TRAIN_CONDITION_RULE, {}).get('text', '')
        if not gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
            infor['groupRule'] = GMD.data.get(GMDD.data.GUILD_TOURNAMENT_GROUP_RULE, '').get('text', '')
            infor['peopleNumRule'] = GMD.data.get(GMDD.data.GUILD_TOURNAMENT_PEOPLE_NUM_RULE, '').get('text', '')
            infor['conditionRule'] = GMD.data.get(GMDD.data.GUILD_TOURNAMENT_CONDITION_RULE, '').get('text', '')
        else:
            infor['groupRule'] = GMD.data.get(GMDD.data.GUILD_TOURNAMENT_GROUP_RULE_MULTI, '').get('text', '')
            infor['peopleNumRule'] = GMD.data.get(GMDD.data.GUILD_TOURNAMENT_PEOPLE_NUM_RULE_MULTI, '').get('text', '')
            infor['conditionRule'] = GMD.data.get(GMDD.data.GUILD_TOURNAMENT_CONDITION_RULE_MULTI, '').get('text', '')
        if p.worldWar.isLucky():
            infor['isLucky'] = True
        else:
            infor['isLucky'] = False
        infor['enableWorldWar'] = gameglobal.rds.configData.get('enableWorldWar', False)
        infor['disableWorldWarText'] = gameStrings.TEXT_GUILDPROXY_2175
        infor['luckyText'] = gameStrings.TEXT_GUILDPROXY_2176
        for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
            groupInfor = {}
            groupInfor['subGroupId'] = gametypes.GUILD_TOURNAMENT_SUBGROUP_BH
            groupInfor['inforBtnEnabled'] = True
            groupInfor['inforBtnTxt'] = gameStrings.TEXT_GUILDPROXY_2183
            groupInfor['inforText'] = ''
            groupInfor['rankMatchVisible'] = False
            groupInfor['rankMatchText'] = ''
            groupInfor['wwBtnForceVisible'] = False
            bTournament = p.guild and p.guild.memberMe.roleId in gametypes.GUILD_ROLE_LEADERS
            guildTournament = p.guildTournament.get(groupId)
            if guildTournament.state in gametypes.GUILD_TOURNAMNET_NO_INFORMATION_STATES:
                groupInfor['inforBtnEnabled'] = False
                groupInfor['inforBtnTxt'] = gameStrings.TEXT_GUILDPROXY_2192
            if guildTournament.state in gametypes.GUILD_TOURNAMENT_BTN_ENTER_STATES or guildTournament.canEnter:
                groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2195
                if self.isWWTournamentApplyedByGroupId(guildTournament):
                    groupInfor['wwBtnForceVisible'] = True
                groupInfor['tip'] = ''
                if groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
                    if guildTournament.getSubGroup(0).canEnter or guildTournament.getSubGroup(1).canEnter:
                        member = p.guild.member.get(p.gbId)
                        if member.groupId == gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH:
                            if guildTournament.getSubGroup(0).canEnter:
                                groupInfor['enabled'] = True
                            else:
                                groupInfor['enabled'] = False
                            groupInfor['subGroupId'] = gametypes.GUILD_TOURNAMENT_SUBGROUP_BH
                        elif member.groupId == gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH_2:
                            if guildTournament.getSubGroup(1).canEnter:
                                groupInfor['enabled'] = True
                            else:
                                groupInfor['enabled'] = False
                            groupInfor['subGroupId'] = gametypes.GUILD_TOURNAMENT_SUBGROUP_BH2
                        else:
                            groupInfor['enabled'] = False
                elif guildTournament.canEnter:
                    groupInfor['enabled'] = True
                else:
                    groupInfor['enabled'] = False
            elif guildTournament.state in gametypes.GUILD_TOURNAMENT_BTN_FINISHED_STATES:
                groupInfor['enabled'] = False
                groupInfor['inforText'] = gameStrings.TEXT_GUILDPROXY_2223
                groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2223
                groupInfor['tip'] = ''
            elif guildTournament.isSeed and guildTournament.hasApplied and groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
                groupInfor['enabled'] = False
                groupInfor['inforText'] = gameStrings.TEXT_GUILDPROXY_2229
                groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2229
                groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2231
            elif guildTournament.state != gametypes.GUILD_TOURNAMENT_STATE_APPLY_NORMAL and guildTournament.state != gametypes.GUILD_TOURNAMENT_STATE_APPLY_SEED:
                groupInfor['enabled'] = False
                groupInfor['inforText'] = gameStrings.TEXT_GUILDPROXY_2235
                groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2235
                groupInfor['tip'] = ''
            elif gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
                isLeaderBH = p.guild.isGroupLeader(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH, p.gbId)
                isLeaderBH2 = p.guild.isGroupLeader(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH_2, p.gbId)
                if groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
                    if guildTournament.getSubGroup(0).hasApplied and guildTournament.getSubGroup(1).hasApplied:
                        groupInfor['inforText'] = gameStrings.TEXT_GUILDPROXY_2244
                        groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2244
                        groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2246
                        groupInfor['enabled'] = False
                    elif guildTournament.getSubGroup(0).hasApplied and not guildTournament.getSubGroup(1).hasApplied:
                        if bTournament or isLeaderBH2:
                            groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2250
                            groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2250
                            groupInfor['subGroupId'] = gametypes.GUILD_TOURNAMENT_SUBGROUP_BH2
                            groupInfor['enabled'] = True
                        else:
                            groupInfor['inforText'] = gameStrings.TEXT_GUILDPROXY_2255
                            groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2255
                            groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2255
                            groupInfor['enabled'] = False
                    elif not guildTournament.getSubGroup(0).hasApplied and guildTournament.getSubGroup(1).hasApplied:
                        if bTournament or isLeaderBH:
                            groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2261
                            groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2261
                            groupInfor['enabled'] = True
                        else:
                            groupInfor['inforText'] = gameStrings.TEXT_GUILDPROXY_2265
                            groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2265
                            groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2265
                            groupInfor['enabled'] = False
                    else:
                        groupInfor = self.dealWithGuildTournamentWithoutApplied(guildTournament, groupId, groupInfor)
                elif guildTournament.hasApplied:
                    groupInfor['enabled'] = False
                    groupInfor['inforText'] = gameStrings.TEXT_GUILDPROXY_2244
                    groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2244
                    groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2246
                else:
                    groupInfor = self.dealWithGuildTournamentWithoutApplied(guildTournament, groupId, groupInfor)
            elif guildTournament.hasApplied:
                groupInfor['enabled'] = False
                groupInfor['inforText'] = gameStrings.TEXT_GUILDPROXY_2244
                groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2244
                groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2246
            else:
                groupInfor = self.dealWithGuildTournamentWithoutApplied(guildTournament, groupId, groupInfor)
            if gameglobal.rds.configData.get('enableGuildTournamentTraining', False):
                groupInfor['trainVisible'] = True
                groupInfor['trainEnable'] = True
                if guildTournament.trainingState == gametypes.GUILD_TOURNAMENT_TRAINING_STATE_CLOSE:
                    if guildTournament.state != gametypes.GUILD_TOURNAMENT_STATE_APPLY_NORMAL or self.isWWTournamentApplyedSuccess():
                        groupInfor['inforText'] = gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_CLOSE_TXT if not groupInfor['inforText'] else groupInfor['inforText']
                        groupInfor['trainVisible'] = False
                    else:
                        groupInfor['trainText'] = gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_CLOSE_TXT
                        groupInfor['trainVisible'] = True
                        groupInfor['trainEnable'] = False
                elif self.isWWTournamentApplyedSuccess():
                    groupInfor['inforText'] = gameStrings.GUILD_WW_TOURNAMENT_APPLYED_TXT
                    groupInfor['trainVisible'] = False
                elif guildTournament.trainingState == gametypes.GUILD_TOURNAMENT_TRAINING_STATE_APPLY:
                    applyState, applyTxt = self.getTrainApplyState()
                    if applyState == gametypes.GUILD_WW_TRAIN_NOT_APPLYED:
                        groupInfor['trainText'] = gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_APPLY_TXT
                        groupInfor['trainVisible'] = True
                    else:
                        groupInfor['trainVisible'] = False
                        groupInfor['inforText'] = applyTxt
                else:
                    applyState, applyTxt = self.getTrainApplyState()
                    if applyState == gametypes.GUILD_WW_TRAIN_QL_APPLYED:
                        if groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
                            groupInfor['trainText'] = gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_MATCH_TXT
                            groupInfor['trainVisible'] = True
                        else:
                            groupInfor['trainVisible'] = False
                            groupInfor['inforText'] = applyTxt
                    elif applyState == gametypes.GUILD_WW_TRAIN_BH_APPLYED:
                        if groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
                            groupInfor['trainText'] = gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_MATCH_TXT
                            groupInfor['trainVisible'] = True
                        else:
                            groupInfor['trainVisible'] = False
                            groupInfor['inforText'] = applyTxt
                    else:
                        groupInfor['trainVisible'] = False
                        groupInfor['inforText'] = applyTxt
            infor['group%d' % groupId] = groupInfor

        infor['infoTabLabel'] = gameStrings.GUILD_WW_TOURNAMENT_INFO_TAB
        infor['trainTabLabel'] = gameStrings.GUILD_WW_TOURNAMENT_TRAIN_TAB
        self.mediator.Invoke('refreshTournamentInfo', uiUtils.dict2GfxDict(infor, True))

    def getCraftList(self, targetCraft):
        if targetCraft == gametypes.NEW_GTN_STRATEGY_WIN:
            return [(0, gameStrings.TEXT_BATTLEFIELDPROXY_1605), (gametypes.NEW_GTN_STRATEGY_MUST_WIN, gameStrings.TEXT_GUILDPROXY_2338)]
        return [(0, gameStrings.TEXT_BATTLEFIELDPROXY_1605), (gametypes.NEW_GTN_STRATEGY_WIN, gameStrings.TEXT_GUILDPROXY_2339), (gametypes.NEW_GTN_STRATEGY_MUST_WIN, gameStrings.TEXT_GUILDPROXY_2338)]

    def getRankTournamentRankGroupRankText(self, groupInfo):
        rankKey = groupInfo.getRankStarKey()
        rankInfo = RGTSD.data.get(rankKey, {})
        if not rankInfo:
            return gameStrings.GUILD_TOURNAMENT_NO_LEVEL
        return rankInfo.get('name', '')

    @ui.callInCD(0.5)
    def refreshRankTournamentInfo(self):
        if not self.getEnableRankTournament():
            return
        elif not self.mediator:
            return
        else:
            p = BigWorld.player()
            infor = {}
            icon, color = uiUtils.getGuildFlag(p.guildFlag)
            infor['guildIcon'] = uiUtils.getGuildIconPath(icon)
            infor['hostId'] = p.getOriginHostId()
            infor['guildName'] = p.guild.name
            infor['strategyEnabled'] = False
            infor['seasonText'] = self.getCurrSeasonText()
            infor['lvMatchTabLabel'] = gameStrings.GUILD_WW_TOURNAMENT_LV_MATCH_TAB
            qlRankTournamentInfo = p.crossRankGtn.get(gametypes.GUILD_TOURNAMENT_GROUP_QL, {})
            bhRankTournamentInfo = p.crossRankGtn.get(gametypes.GUILD_TOURNAMENT_GROUP_BH, {})
            qlGroupName = gametypes.GUILD_TOURNAMENT_GROUP_NAME.get(gametypes.GUILD_TOURNAMENT_GROUP_QL, '')
            bhGroupName = gametypes.GUILD_TOURNAMENT_GROUP_NAME.get(gametypes.GUILD_TOURNAMENT_GROUP_BH, '')
            if qlRankTournamentInfo.rank:
                infor['rankText0'] = gameStrings.GUILD_TOURNAMENT_RANK_TEXT % (qlGroupName, qlRankTournamentInfo.rank)
            else:
                infor['rankText0'] = gameStrings.GUILD_TOURNAMENT_NO_RANK_TEXT % (qlGroupName,)
            if bhRankTournamentInfo.rank:
                infor['rankText1'] = gameStrings.GUILD_TOURNAMENT_RANK_TEXT % (bhGroupName, bhRankTournamentInfo.rank)
            else:
                infor['rankText1'] = gameStrings.GUILD_TOURNAMENT_NO_RANK_TEXT % (bhGroupName,)
            infor['award0'] = qlRankTournamentInfo.bonus
            infor['award1'] = bhRankTournamentInfo.bonus
            for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
                rankTournament = p.crossRankGtn.get(groupId)
                groupInfor = {}
                groupInfor['inforText'] = ''
                groupInfor['stateText'] = ''
                groupRankText = self.getRankTournamentRankGroupRankText(rankTournament)
                groupInfor['rankText'] = gameStrings.GUILD_TOURNAMENT_RANK_DESC % (groupRankText, str(rankTournament.groupScore))
                if rankTournament.state:
                    if rankTournament.state in gametypes.NEW_GTN_MATCH_STATES:
                        if rankTournament.state == gametypes.NEW_GTN_STATE_GAME_START:
                            currRound = rankTournament.roundNum
                        else:
                            currRound = rankTournament.roundNum + 1
                        stateDetail = '%s(%s)' % (gametypes.NEW_GTN_STATE_NAME.get(rankTournament.state, ''), gameStrings.MATCH_ROUND % currRound)
                        groupInfor['stateText'] = gameStrings.GUILD_TOURNAMENT_STATE % stateDetail
                    else:
                        groupInfor['stateText'] = gameStrings.GUILD_TOURNAMENT_STATE % gametypes.NEW_GTN_STATE_NAME.get(rankTournament.state, '')
                groupInfor['rankMatchEnable'] = True
                groupInfor['enableLive'] = False
                groupInfor['enableCheer'] = False
                if rankTournament.state == gametypes.NEW_GTN_STATE_APPLY:
                    groupInfor['rankMatchVisible'] = True
                    groupInfor['rankMatchText'] = gameStrings.GUILD_TOURNAMENT_RANK_STATE_APPLY_TXT
                    guildCrossTournament = p.crossRankGtn.get(groupId)
                    if guildCrossTournament != None and (guildCrossTournament.isCandidate or guildCrossTournament.hasApplied):
                        groupInfor['rankMatchText'] = gameStrings.GUILD_TOURNAMENT_RANK_STATE_APPLYED
                        groupInfor['rankMatchEnable'] = False
                elif rankTournament.state == gametypes.NEW_GTN_STATE_GAME_START:
                    groupInfor['rankMatchVisible'] = True
                    groupInfor['rankMatchText'] = gameStrings.GUILD_TOURNAMENT_RANK_STATE_MATCH_TXT
                    guildCrossTournament = p.crossRankGtn.get(groupId)
                    groupInfor['rankMatchEnable'] = False
                    if guildCrossTournament != None and guildCrossTournament.canEnter:
                        groupInfor['rankMatchEnable'] = True
                    if guildCrossTournament != None and (guildCrossTournament.isCandidate or guildCrossTournament.hasApplied):
                        groupInfor['enableLive'] = True
                        groupInfor['enableCheer'] = True
                infor['group%d' % groupId] = groupInfor

            infor['groupInfo'] = []
            infor['detailList'] = GCD.data.get('rankTournamentTipList', (('', ''), ('', ''), ('', '')))
            for i in xrange(4):
                matchItem = {}
                if i % 2 == 0:
                    groupId = gametypes.GUILD_TOURNAMENT_GROUP_QL
                else:
                    groupId = gametypes.GUILD_TOURNAMENT_GROUP_BH
                if i >= 2:
                    roundNum = 2
                else:
                    roundNum = 1
                rankTournamentInfo = p.crossRankGtn.get(groupId, {})
                matchInfo = rankTournamentInfo.matchInfo.get(roundNum, {})
                isFirst = matchInfo.get('gPair', (0, 0))[0] == p.guildNUID
                enermyNUID = matchInfo.get('gPair', (0, 0))[1] if isFirst else matchInfo.get('gPair', (0, 0))[0]
                isSkip = False
                if matchInfo.get('gPair', None):
                    isSkip = enermyNUID == 0
                targetGroupId = groupId
                matchItem['teamName'] = gametypes.GUILD_TOURNAMENT_GROUP_NAME.get(groupId, '')
                matchItem['numText'] = gameStrings.GUILD_TOURNAMENT_RANK_MATCH_ROUND_TEXT_GROUP % (matchItem['teamName'], uiUtils.convertIntToChn(roundNum))
                matchItem['timeText'] = self.getRankTournamentRoundTime(roundNum)
                matchItem['isApply'] = rankTournamentInfo.isCandidate or rankTournamentInfo.hasApplied
                if matchItem['isApply']:
                    matchItem['guildName'] = uiUtils.toHtml(p.guild.name, '#FF8C00')
                else:
                    color = '#FF0000' if rankTournamentInfo.state == gametypes.NEW_GTN_STATE_APPLY else '#696969'
                    matchItem['guildName'] = uiUtils.toHtml(gameStrings.GUILD_NOT_SIGNED, color)
                if isSkip:
                    matchItem['guildName1'] = gameStrings.GUILD_TOURNAMENT_SKIP
                else:
                    matchItem['guildName1'] = matchInfo.get('nameTwo', '') or gameStrings.WING_WORLD_NO_CAMP_LEADER if isFirst else matchInfo.get('nameOne', '') or gameStrings.WING_WORLD_NO_CAMP_LEADER
                matchItem['bfList'] = self.getBfList(groupId)
                matchItem['teamName1'] = gametypes.GUILD_TOURNAMENT_GROUP_NAME.get(targetGroupId, '')
                matchItem['craftId'] = matchInfo.get('strategyOne', 0) if isFirst else matchInfo.get('strategyTwo', 0)
                matchItem['craftId1'] = matchInfo.get('strategyTwo', 0) if isFirst else matchInfo.get('strategyOne', 0)
                matchItem['craftList'] = self.getCraftList(matchItem['craftId1'])
                baseScore = min(matchInfo.get('bonusOne', 0), matchInfo.get('bonusTwo', 0))
                isWin = matchInfo.get('winGuildNUID', 0) == p.guildNUID
                if matchInfo.get('winGuildNUID', 0):
                    finalAward = matchInfo.get('finalBonus', 0)
                    if finalAward:
                        if isWin:
                            matchItem['award'] = '+%d' % finalAward
                        else:
                            matchItem['award'] = '-%d' % finalAward
                    else:
                        matchItem['award'] = '-'
                elif not matchInfo.get('winGuildNUID', 0) and not isSkip:
                    matchItem['award'] = self.calcAward(baseScore, matchItem['craftId'], matchItem['craftId1'])
                else:
                    matchItem['award'] = '-'
                if matchInfo.get('fbNo', 0) in matchItem['bfList']:
                    matchItem['bfId'] = matchItem['bfList'].index(matchInfo.get('fbNo', 0))
                else:
                    matchItem['bfId'] = 0
                winGuildNUID = matchInfo.get('winGuildNUID', 0)
                matchItem['winner'] = 0
                if winGuildNUID:
                    matchItem['winner'] = 1 if winGuildNUID == p.guildNUID else 2
                if rankTournamentInfo.state == gametypes.NEW_GTN_STATE_GAME_START_READY:
                    matchItem['canEditBf'] = self.canEditBf(matchInfo) and roundNum > rankTournamentInfo.roundNum
                    matchItem['canEditCraft'] = self.canEditCraft(matchInfo) and roundNum > rankTournamentInfo.roundNum
                else:
                    matchItem['canEditBf'] = False
                    matchItem['canEditCraft'] = False
                infor['groupInfo'].append(matchItem)

            self.mediator.Invoke('refreshRankTournamentInfo', uiUtils.dict2GfxDict(infor, True))
            return

    def getRankTournamentRoundTime(self, roundNum):
        for data in NGTSD.data.itervalues():
            if data.get('round', 0) == roundNum:
                return data.get('readyTime', '')

        return ''

    def canEditBf(self, matchInfo):
        if not matchInfo:
            return False
        if matchInfo.get('winGuildNUID', 0):
            return False
        return True

    def canEditCraft(self, matchInfo):
        if not matchInfo:
            return False
        if matchInfo.get('winGuildNUID', 0):
            return False
        if not matchInfo.get('bonusOne', 0) or not matchInfo.get('bonusTwo', 0):
            return False
        return True

    def calcAward(self, baseScore, myCraftId, targetCraftId):
        if not baseScore:
            return '-'
        craftRatio = 1
        crafts = [myCraftId, targetCraftId]
        if gametypes.NEW_GTN_STRATEGY_WIN in crafts and gametypes.NEW_GTN_STRATEGY_MUST_WIN in crafts:
            craftRatio = 3
        elif gametypes.NEW_GTN_STRATEGY_WIN in crafts:
            craftRatio = 1.5
        elif gametypes.NEW_GTN_STRATEGY_MUST_WIN in crafts:
            craftRatio = 2
        awardText = '%d-%d' % (baseScore * craftRatio, baseScore * craftRatio * 3)
        return awardText

    def getBfList(self, groupId):
        bfList = []
        bfIds = GTOD.data.get(groupId, {}).get('fbNoList', [])
        for bfId in bfIds:
            bfItem = (bfId, BFD.data.get(bfId, {}).get('name', ''))
            bfList.append(bfItem)

        return bfList

    def getCurrSeasonText(self):
        seasonStart, seasonEnd = utils.getQuarterSecondRange()
        startStr = time.strftime('%Y.%m.%d', time.localtime(seasonStart))
        endStr = time.strftime('%m.%d', time.localtime(seasonEnd))
        return gameStrings.GUILD_TOURNAMENT_RANK_MATCH_SEASON % (startStr, endStr)

    def getTrainApplyState(self):
        p = BigWorld.player()
        guildTournamentQL = p.guildTournament.get(gametypes.GUILD_TOURNAMENT_GROUP_QL)
        guildTournamentBH = p.guildTournament.get(gametypes.GUILD_TOURNAMENT_GROUP_BH)
        if not guildTournamentQL.trainingAppliesByNuid and not guildTournamentBH.trainingAppliesByNuid:
            return (gametypes.GUILD_WW_TRAIN_NOT_APPLYED, gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_NOT_APPLYED_TXT)
        if guildTournamentQL.trainingAppliesByNuid:
            playerGbIds = self.getTrainPlayerGbIds(guildTournamentQL)
            if not playerGbIds:
                return (gametypes.GUILD_WW_TRAIN_OUT, gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_OUT_MATCH_TXT)
            elif p.gbId in playerGbIds:
                return (gametypes.GUILD_WW_TRAIN_QL_APPLYED, gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_APPLYED_QL_TXT)
            else:
                return (gametypes.GUILD_WW_TRAIN_OTHER_GROUP_APPLYED, gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_NOT_MATCH_TXT)
        if guildTournamentBH.trainingAppliesByNuid:
            playerGbIds = self.getTrainPlayerGbIds(guildTournamentBH)
            if not playerGbIds:
                return (gametypes.GUILD_WW_TRAIN_OUT, gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_OUT_MATCH_TXT)
            elif p.gbId in playerGbIds:
                return (gametypes.GUILD_WW_TRAIN_BH_APPLYED, gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_APPLYED_BH_TXT)
            else:
                return (gametypes.GUILD_WW_TRAIN_OTHER_GROUP_APPLYED, gameStrings.GUILD_TOURNAMENT_TRAINING_STATE_NOT_MATCH_TXT)

    def getTrainPlayerGbIds(self, guildTournament):
        p = BigWorld.player()
        for k, v in guildTournament.trainingAppliesByNuid.iteritems():
            if p.guildNUID == k[0]:
                return v

    def isWWTournamentApplyedSuccess(self):
        p = BigWorld.player()
        for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
            guildTournament = p.guildTournament.get(groupId)
            if self.isWWTournamentApplyedByGroupId(guildTournament, True):
                return True

        return False

    def isWWTournamentApplyedByGroupId(self, guildTournament, isNeedSuccess = False):
        if guildTournament.hasApplied:
            if isNeedSuccess:
                return guildTournament.isInMatches
            return True
        return False

    def dealWithGuildTournamentWithoutApplied(self, guildTournament, groupId, groupInfor):
        p = BigWorld.player()
        bTournament = p.guild and p.guild.memberMe.roleId in gametypes.GUILD_ROLE_LEADERS
        if gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
            if groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
                if bTournament:
                    groupInfor['enabled'] = True
                    groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2594
                    groupInfor['tip'] = ''
                else:
                    isLeaderBH = p.guild.isGroupLeader(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH, p.gbId)
                    if isLeaderBH:
                        groupInfor['enabled'] = True
                        groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2594
                        groupInfor['tip'] = ''
                    else:
                        isLeaderBH = p.guild.isGroupLeader(gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH_2, p.gbId)
                        if isLeaderBH:
                            groupInfor['enabled'] = True
                            groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2606
                            groupInfor['subGroupId'] = gametypes.GUILD_TOURNAMENT_SUBGROUP_BH2
                            groupInfor['tip'] = ''
                        else:
                            groupInfor['enabled'] = False
                            groupInfor['text'] = gameStrings.TEXT_ACTIVITYFACTORY_137
                            groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2612
            elif bTournament:
                groupInfor['enabled'] = True
                groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2616
                groupInfor['tip'] = ''
            else:
                groupInfor['enabled'] = False
                groupInfor['text'] = gameStrings.TEXT_ACTIVITYFACTORY_137
                groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2612
        elif bTournament:
            groupInfor['enabled'] = True
            groupInfor['text'] = gameStrings.TEXT_GUILDPROXY_2616
            groupInfor['tip'] = ''
        else:
            groupInfor['enabled'] = False
            groupInfor['text'] = gameStrings.TEXT_ACTIVITYFACTORY_137
            groupInfor['tip'] = gameStrings.TEXT_GUILDPROXY_2612
        return groupInfor

    def refreshTournamentInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
                baseData = GTOD.data.get(groupId, {})
                if not baseData:
                    continue
                guildTournament = p.guildTournament.get(groupId)
                groupInfo = {}
                if gameglobal.rds.configData.get('enableGuildTournamentTestBF', False):
                    num = baseData.get('testMaxNum', 0)
                else:
                    num = baseData.get('maxNum', 0)
                groupInfo['num'] = num
                groupInfo['level'] = '%d - %d' % (baseData.get('minLv', 0), baseData.get('maxLv', 0))
                groupInfo['scheduleDesc'] = baseData.get('scheduleDesc', '')
                groupInfo['applyConditionDesc'] = baseData.get('applyConditionDesc', '')
                groupInfo['status'] = gametypes.GUILD_TOURNAMENT_STATE_NAME.get(guildTournament.state, '')
                if guildTournament.state == gametypes.GUILD_TOURNAMENT_STATE_APPLY_SEED:
                    if guildTournament.isSeed:
                        groupInfo['status'] += gameStrings.TEXT_GUILDPROXY_2657 if guildTournament.hasApplied else gameStrings.TEXT_GUILDPROXY_2657_1
                elif guildTournament.state in (gametypes.GUILD_TOURNAMENT_STATE_APPLY_NORMAL, gametypes.GUILD_TOURNAMENT_STATE_APPLY_END):
                    groupInfo['status'] += gameStrings.TEXT_GUILDPROXY_2657 if guildTournament.hasApplied else gameStrings.TEXT_GUILDPROXY_2657_1
                for scheduleData in getGTNSD().data.itervalues():
                    roundNum = scheduleData.get('round', 0)
                    if roundNum <= 0:
                        continue
                    dayTime = utils.getWeekSecond() + int(scheduleData.get('crontab', '0 0 * * 0')[-1]) * const.TIME_INTERVAL_DAY
                    groupInfo['dayTime%d' % roundNum] = utils.formatDate(dayTime)
                    groupInfo['readyTime%d' % roundNum] = scheduleData.get('readyTime', '')
                    groupInfo['startTime%d' % roundNum] = scheduleData.get('startTime', '')
                    groupInfo['endTime%d' % roundNum] = scheduleData.get('endTime', '')

                if guildTournament.state == gametypes.GUILD_TOURNAMENT_STATE_MATCH or guildTournament.canEnter:
                    groupInfo['btnLabel'] = gameStrings.TEXT_GUILDPROXY_2672
                else:
                    groupInfo['btnLabel'] = gameStrings.TEXT_GUILDPROXY_2674
                bTournament = p.guild and p.guild.memberMe.roleId in gametypes.GUILD_ROLE_LEADERS
                groupInfo['btnVisible'] = bTournament
                if guildTournament.state == gametypes.GUILD_TOURNAMENT_STATE_APPLY_SEED:
                    if bTournament:
                        if guildTournament.hasApplied:
                            groupInfo['btnLabel'] = gameStrings.TEXT_GUILDPROXY_2244
                            groupInfo['btnEnabled'] = False
                        else:
                            groupInfo['btnEnabled'] = guildTournament.isSeed
                    else:
                        groupInfo['btnEnabled'] = False
                elif guildTournament.state == gametypes.GUILD_TOURNAMENT_STATE_APPLY_NORMAL:
                    if bTournament:
                        if guildTournament.hasApplied:
                            groupInfo['btnLabel'] = gameStrings.TEXT_GUILDPROXY_2244
                            groupInfo['btnEnabled'] = False
                        else:
                            groupInfo['btnEnabled'] = True
                    else:
                        groupInfo['btnEnabled'] = False
                elif guildTournament.canEnter:
                    groupInfo['btnEnabled'] = True
                    groupInfo['btnVisible'] = True
                else:
                    groupInfo['btnEnabled'] = False
                    groupInfo['btnVisible'] = True if bTournament else guildTournament.state == gametypes.GUILD_TOURNAMENT_STATE_MATCH
                info['group%d' % groupId] = groupInfo

            self.mediator.Invoke('refreshTournamentInfo', uiUtils.dict2GfxDict(info, True))

    @ui.callFilter(2, False)
    def getTournamentSimpleInfo(self):
        p = BigWorld.player()
        p.queryGuildTournamentSimple()

    @ui.callInCD(2)
    def getRankTournamentSimpleInfo(self):
        p = BigWorld.player()
        if self.getEnableRankTournament():
            p.queryNewGuildTournamentSimple()
            p.cell.requestGuildTournamentBattleInfo()
            p.cell.queryNgtApplyInfo()

    @ui.callInCD(2)
    def queryRankTournamentGuildInfo(self):
        p = BigWorld.player()
        if self.getEnableRankTournament():
            p.cell.queryNewGuildTournamentRankInfo()

    def onShowTournamentResult(self, *arg):
        groupId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.guildTournamentResult.show(groupId)

    def onShowTournamentRank(self, *arg):
        groupId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.guildTournamentRank.show(groupId)

    def onShowWWTournamentRank(self, *arg):
        gameglobal.rds.ui.guildWWTournamentRank.groupId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.guildWWTournamentRank.queryRankInfo()

    def onShowWWTournamentResult(self, *arg):
        p = BigWorld.player()
        groupId = int(arg[3][0].GetNumber())
        tournamentResult = p.worldWar.tournamentResult
        p.cell.queryWWTournament(groupId, tournamentResult.groupVer[groupId], tournamentResult.guildVer)
        gameglobal.rds.ui.guildWWTournamentResult.readyToShow()

    def onApplyTrain(self, *arg):
        groupId = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        guildTournament = p.guildTournament.get(groupId)
        if guildTournament.trainingState == gametypes.GUILD_TOURNAMENT_TRAINING_STATE_APPLY:
            p.cell.applyGuildTournamentTraining(groupId)
        else:
            p.cell.enterGuildTournamentTraining(groupId)

    def onShowTournamentApply(self, *arg):
        groupId = int(arg[3][0].GetNumber())
        subGroupId = 0
        if gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
            subGroupId = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        guildTournament = p.guildTournament.get(groupId)
        canEnter = guildTournament.canEnter
        if gameglobal.rds.configData.get('enableGuildTournamentMultiGroup', False):
            canEnter = guildTournament.getSubGroup(subGroupId).canEnter
        if guildTournament and canEnter:
            p.cell.enterGuildTournament(groupId)
            gameglobal.rds.ui.bFScoreAward.setBFInfo(groupId, uiConst.BF_SCORE_AWARD_GUILD_TOURNAMENT)
        else:
            if guildTournament.state in gametypes.GUILD_TOURNAMENT_BTN_ENTER_STATES:
                p.showGameMsg(GMDD.data.GUILD_TOURNAMENT_ENTER_NOT_AVALIABLE, (const.YOU,))
            gameglobal.rds.ui.guildTournamentApply.show(groupId, subGroupId)

    def onGetCrossTournamentInfo(self, *arg):
        self.refreshCrossTournamentInfo()
        self.getCrossTournamentSimpleInfo()

    def refreshCrossTournamentInfo(self):
        if self.isEnableNewCrossTournament():
            self.refreshNewCrossTournamentInfo()
        else:
            self.refreshOldCrossTournamentInfo()

    def getGroupRangeTime(self):
        startTime = ''
        endTime = ''
        for scheduleData in CGTSD.data.itervalues():
            roundNum = scheduleData.get('round', 0)
            scheduleState = scheduleData.get('state', 0)
            if scheduleState == gametypes.CROSS_GTN_STATE_GROUP_MATCH:
                weekNum = scheduleData.get('weekNum', 0)
                nowWeekNum = commTournament.getWeekNum()
                weekSecond = utils.getWeekSecond() + (weekNum - nowWeekNum) * const.TIME_INTERVAL_WEEK
                dayTime = weekSecond + int(scheduleData.get('crontab', '0 0 * * 0')[-1]) * const.TIME_INTERVAL_DAY
                if startTime == '':
                    startTime = utils.formatCustomTime(dayTime, '%m.%d')
                endTime = utils.formatCustomTime(dayTime, '%m.%d')

        return '%s-%s' % (startTime, endTime)

    def getCirculatarRangeTime(self):
        startTime = ''
        endTime = ''
        for scheduleData in CGTSD.data.itervalues():
            roundNum = scheduleData.get('round', 0)
            scheduleState = scheduleData.get('state', 0)
            if scheduleState == gametypes.CROSS_GTN_STATE_CIRCULAR_MATCH:
                weekNum = scheduleData.get('weekNum', 0)
                nowWeekNum = commTournament.getWeekNum()
                weekSecond = utils.getWeekSecond() + (weekNum - nowWeekNum) * const.TIME_INTERVAL_WEEK
                dayTime = weekSecond + int(scheduleData.get('crontab', '0 0 * * 0')[-1]) * const.TIME_INTERVAL_DAY
                if startTime == '':
                    startTime = utils.formatCustomTime(dayTime, '%m.%d')
                endTime = utils.formatCustomTime(dayTime, '%m.%d')

        return '%s-%s' % (startTime, endTime)

    def getFinalRangeTime(self):
        startTime = ''
        endTime = ''
        for scheduleData in CGTSD.data.itervalues():
            roundNum = scheduleData.get('round', 0)
            scheduleState = scheduleData.get('state', 0)
            if scheduleState == gametypes.CROSS_GTN_STATE_PLAYOFF_MATCH:
                weekNum = scheduleData.get('weekNum', 0)
                nowWeekNum = commTournament.getWeekNum()
                weekSecond = utils.getWeekSecond() + (weekNum - nowWeekNum) * const.TIME_INTERVAL_WEEK
                dayTime = weekSecond + int(scheduleData.get('crontab', '0 0 * * 0')[-1]) * const.TIME_INTERVAL_DAY
                if startTime == '':
                    startTime = utils.formatCustomTime(dayTime, '%m.%d')
                endTime = utils.formatCustomTime(dayTime, '%m.%d')

        return '%s-%s' % (startTime, endTime)

    def refreshOldCrossTournamentInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
                baseData = CGTD.data.get(groupId, {})
                if not baseData:
                    continue
                guildCrossTournament = p.crossGtn.get(groupId)
                groupInfo = {}
                if gameglobal.rds.configData.get('enableGuildTournamentTestBF', False):
                    num = baseData.get('testMaxNum', 0)
                else:
                    num = baseData.get('maxNum', 0)
                groupInfo['num'] = num
                groupInfo['level'] = '%d - %d' % (baseData.get('minLv', 0), baseData.get('maxLv', 0))
                groupInfo['scheduleDesc'] = baseData.get('scheduleDesc', '')
                groupInfo['applyConditionDesc'] = baseData.get('applyConditionDesc', '')
                groupInfo['status'] = gametypes.CROSS_GTN_STATE_NAME.get(guildCrossTournament.state, '')
                if guildCrossTournament.state < gametypes.CROSS_GTN_STATE_GROUP_MATCH_FINISHED:
                    groupInfo['scheduleTitle'] = gameStrings.TEXT_GUILDPROXY_2858
                else:
                    groupInfo['scheduleTitle'] = gameStrings.TEXT_GUILDPROXY_2860
                for scheduleData in CGTSD.data.itervalues():
                    roundNum = scheduleData.get('round', 0)
                    scheduleState = scheduleData.get('state', 0)
                    if roundNum <= 0:
                        continue
                    if guildCrossTournament.state < gametypes.CROSS_GTN_STATE_GROUP_MATCH_FINISHED and scheduleState != gametypes.CROSS_GTN_STATE_GROUP_MATCH:
                        continue
                    if guildCrossTournament.state >= gametypes.CROSS_GTN_STATE_GROUP_MATCH_FINISHED and scheduleState != gametypes.CROSS_GTN_STATE_PLAYOFF_MATCH:
                        continue
                    weekNum = scheduleData.get('weekNum', 0)
                    nowWeekNum = guildCrossTournament.getWeekNum()
                    weekSecond = utils.getWeekSecond() + (weekNum - nowWeekNum) * const.TIME_INTERVAL_WEEK
                    dayTime = weekSecond + int(scheduleData.get('crontab', '0 0 * * 0')[-1]) * const.TIME_INTERVAL_DAY
                    groupInfo['dayTime%d' % roundNum] = utils.formatDate(dayTime)
                    groupInfo['readyTime%d' % roundNum] = scheduleData.get('readyTime', '')
                    groupInfo['startTime%d' % roundNum] = scheduleData.get('startTime', '')
                    groupInfo['endTime%d' % roundNum] = scheduleData.get('endTime', '')

                if guildCrossTournament.canEnter:
                    groupInfo['btnEnabled'] = True
                else:
                    groupInfo['btnEnabled'] = False
                info['group%d' % groupId] = groupInfo

            self.mediator.Invoke('refreshCrossTournamentInfo', uiUtils.dict2GfxDict(info, True))

    def refreshNewCrossTournamentInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            if p.isInCrossGuildTournamentCirCular():
                info['state0Info'] = (gameStrings.MATCH_CIRCUL, self.getCirculatarRangeTime())
            else:
                info['state0Info'] = (gameStrings.MATCH_GROUP, self.getGroupRangeTime())
            info['state1Info'] = (gameStrings.MATCH_KICK_2, self.getFinalRangeTime())
            for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
                baseData = CGTD.data.get(groupId, {})
                if not baseData:
                    continue
                guildCrossTournament = p.crossGtn.get(groupId)
                if guildCrossTournament.state in gametypes.CROSS_GTN_PLAYOFF_STATES:
                    info['currentState'] = MATCH_TYPE_KICK
                else:
                    info['currentState'] = MATCH_TYPE_GROUP_SCORE
                groupInfo = {}
                if gameglobal.rds.configData.get('enableGuildTournamentTestBF', False):
                    num = baseData.get('testMaxNum', 0)
                else:
                    num = baseData.get('maxNum', 0)
                groupInfo['num'] = num
                groupInfo['level'] = '%d - %d' % (baseData.get('minLv', 0), baseData.get('maxLv', 0))
                groupInfo['scheduleDesc'] = baseData.get('scheduleDesc', '')
                groupInfo['applyConditionDesc'] = baseData.get('applyConditionDesc', '')
                groupInfo['status'] = gametypes.CROSS_GTN_STATE_NAME.get(guildCrossTournament.state, '')
                groupInfo['groupName'] = gametypes.GUILD_TOURNAMENT_GROUP_NAME.get(groupId, '')
                if guildCrossTournament.canEnter:
                    groupInfo['btnEnabled'] = True
                else:
                    groupInfo['btnEnabled'] = False
                for matchType in (MATCH_TYPE_GROUP_SCORE, MATCH_TYPE_KICK):
                    scheduleInfo = self.getScheduleInfo(guildCrossTournament, matchType)
                    groupInfo['schedule%d' % matchType] = scheduleInfo

                info['group%d' % groupId] = groupInfo

            self.mediator.Invoke('refreshCrossTournamentInfo', uiUtils.dict2GfxDict(info, True))

    def getScheduleInfo(self, guildCrossTournament, matchType):
        scheduleInfo = {}
        p = BigWorld.player()
        if matchType == MATCH_TYPE_GROUP_SCORE:
            if p.isInCrossGuildTournamentCirCular():
                scheduleInfo['scheduleTitle'] = gameStrings.MATCH_CIRCUL + gameStrings.TIME_SCHEDULE
            else:
                scheduleInfo['scheduleTitle'] = gameStrings.MATCH_GROUP + gameStrings.TIME_SCHEDULE
        else:
            scheduleInfo['scheduleTitle'] = gameStrings.MATCH_KICK_2 + gameStrings.TIME_SCHEDULE
        for scheduleData in CGTSD.data.itervalues():
            roundNum = scheduleData.get('round', 0)
            scheduleState = scheduleData.get('state', 0)
            if roundNum <= 0:
                continue
            if matchType == MATCH_TYPE_GROUP_SCORE:
                if p.isInCrossGuildTournamentCirCular():
                    if scheduleState != gametypes.CROSS_GTN_STATE_CIRCULAR_MATCH:
                        continue
                elif scheduleState != gametypes.CROSS_GTN_STATE_GROUP_MATCH:
                    continue
            if matchType == MATCH_TYPE_KICK and scheduleState != gametypes.CROSS_GTN_STATE_PLAYOFF_MATCH:
                continue
            weekNum = scheduleData.get('weekNum', 0)
            nowWeekNum = guildCrossTournament.getWeekNum()
            weekSecond = utils.getWeekSecond() + (weekNum - nowWeekNum) * const.TIME_INTERVAL_WEEK
            dayTime = weekSecond + int(scheduleData.get('crontab', '0 0 * * 0')[-1]) * const.TIME_INTERVAL_DAY
            scheduleInfo['dayTime%d' % roundNum] = utils.formatDate(dayTime)
            scheduleInfo['readyTime%d' % roundNum] = scheduleData.get('readyTime', '')
            scheduleInfo['startTime%d' % roundNum] = scheduleData.get('startTime', '')
            scheduleInfo['endTime%d' % roundNum] = scheduleData.get('endTime', '')

        return scheduleInfo

    @ui.callFilter(2, False)
    def getCrossTournamentSimpleInfo(self):
        p = BigWorld.player()
        guildCrossTournamentQL = p.crossGtn.get(gametypes.GUILD_TOURNAMENT_GROUP_QL)
        guildCrossTournamentBH = p.crossGtn.get(gametypes.GUILD_TOURNAMENT_GROUP_BH)
        if guildCrossTournamentQL != None and guildCrossTournamentBH != None:
            p.cell.queryCrossGtnSimple(guildCrossTournamentQL.simpleVer, guildCrossTournamentBH.simpleVer)

    def onShowCrossTournamentResult(self, *arg):
        groupId = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if p.isInCrossGuildTournamentCirCular():
            gameglobal.rds.ui.guildCrossScoreTResult.show(groupId)
        else:
            gameglobal.rds.ui.guildCrossTResult.show(groupId)

    def onShowCrossTournamentFinalResult(self, *arg):
        groupId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.guildCrossTFinalResult.show(groupId)

    def onShowCrossTournamentApply(self, *arg):
        groupId = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        guildCrossTournament = p.crossGtn.get(groupId)
        if guildCrossTournament != None and guildCrossTournament.canEnter:
            p.cell.enterCrossGtn(groupId)
            if guildCrossTournament.state < gametypes.CROSS_GTN_STATE_GROUP_MATCH_FINISHED:
                bFState = uiConst.BF_SCORE_AWARD_CROSS_GTN_GROUP
            else:
                bFState = uiConst.BF_SCORE_AWARD_CROSS_GTN_PLAYOFF
            gameglobal.rds.ui.bFScoreAward.setBFInfo(groupId, bFState)

    def yixinStateChange(self, params):
        if self.mediator:
            self.mediator.Invoke('setYixinEnable', GfxValue(BigWorld.player().yixinOpenId))

    def onIsShowYixin(self, *arg):
        isShowYixin = bool(gameglobal.rds.configData.get('enableYixin', False) and BigWorld.player().guild and BigWorld.player().guild.yixinTeamId)
        return GfxValue(isShowYixin)

    def onIsLeader(self, *args):
        ret = bool(BigWorld.player().guild and BigWorld.player().guild.memberMe.roleId == gametypes.GUILD_ROLE_LEADER)
        return GfxValue(ret)

    def onIsBindYixin(self, *args):
        return GfxValue(BigWorld.player().yixinOpenId)

    def onSendMsgToAll(self, *arg):
        gameglobal.rds.ui.yixinGuildSendMsg.toggle()

    def onAddYixinGroup(self, *arg):
        BigWorld.player().cell.joinGuildYixin()

    def onSubscribeSetting(self, *arg):
        gameglobal.rds.ui.yixinSetting.toggle()

    def checkResidentNpcOption(self, npcId):
        if npcId == self.residentNpcId and self.bNeedTreat:
            return False
        else:
            return True

    def refreshProsperityInfo(self):
        self.refreshBuildProsperity()
        self.refreshTechnologyTopBar()

    def refreshAllResidentProxy(self, residentNUID = 0):
        gameglobal.rds.ui.guildAssart.setInitData()
        gameglobal.rds.ui.guildBuildUpgrade.setInitData()
        gameglobal.rds.ui.guildResident.refreshInfo(residentNUID)
        gameglobal.rds.ui.guildResidentRec.refreshInfo()
        gameglobal.rds.ui.guildResidentHired.refreshInfo()
        gameglobal.rds.ui.guildDispatchInto.refreshInfo()
        gameglobal.rds.ui.guildResidentManager.refreshInfo()
        gameglobal.rds.ui.guildTechResearch.refreshInfo()
        gameglobal.rds.ui.guildFactory.refreshInfo()
        gameglobal.rds.ui.guildProduce.refreshInfo()
        gameglobal.rds.ui.guildSawmill.refreshInfo()

    def hideAllGuildBuilding(self):
        guild = BigWorld.player().guild
        if guild:
            markerId = commGuild.getMarkerIdByBuildingId(guild, gametypes.GUILD_BUILDING_MASTER_ID)
            gameglobal.rds.ui.guildResidentManager.hideByMarkerId(markerId)
            markerId = commGuild.getMarkerIdByBuildingId(guild, gametypes.GUILD_BUILDING_RESTAURANT_ID)
            gameglobal.rds.ui.guildResidentManager.hideByMarkerId(markerId)
        if gameglobal.rds.ui.guildStorage.mediator:
            gameglobal.rds.ui.guildStorage.hide()
        if gameglobal.rds.ui.guildGrowth.mediator:
            gameglobal.rds.ui.guildGrowth.hide()
        if gameglobal.rds.ui.guildActivity.mediator:
            gameglobal.rds.ui.guildActivity.hide()
        if gameglobal.rds.ui.guildFindStar.mediator:
            gameglobal.rds.ui.guildFindStar.hide()
        if gameglobal.rds.ui.guildSawmill.mediator:
            gameglobal.rds.ui.guildSawmill.hide()
        if gameglobal.rds.ui.guildFactory.mediator:
            gameglobal.rds.ui.guildFactory.hide()

    def onGetActivityInfo(self, *arg):
        p = BigWorld.player()
        info = {}
        info['gxLable'] = str(p.guildContrib) + '/' + str(p.guildContribTotal)
        info['backIconData'] = {'iconPath': 'skill/icon64/9804.dds'}
        info['dayItemLen'] = 6
        info['weekItemLen'] = 2
        info['itemOffsetHeight'] = 0
        info['itemOffsetWidth'] = 5
        info['bFlag'] = 1
        info['guildEnterNpc'] = GCD.data.get('GuildEnterNpc', (11015272,))[0]
        if p.guildMemberSkills.has_key(uiConst.GUILD_SKILL_DZG):
            info['goGuildSpaceBtnEnabled'] = True
        else:
            info['goGuildSpaceBtnEnabled'] = False
            info['goGuildSpaceBtnTip'] = GCD.data.get('goGuildSpaceBtnTip', gameStrings.TEXT_GUILDPROXY_554)
        activityList = []
        for gid, rdata in GIAD.data.iteritems():
            gameconfigName = rdata.get('gameconfigName', '')
            if gameconfigName and not gameglobal.rds.configData.get(gameconfigName, False):
                continue
            activityList.append(self.getItemsByType(gid, rdata))

        activityList.sort(key=lambda x: x['sortId'])
        info['activityList'] = activityList
        fuliList = []
        for key, btnName, clickType, tipsId, gameconfigName in GCD.data.get('fuliBtnInfoList', ()):
            if gameconfigName and not gameglobal.rds.configData.get(gameconfigName, False):
                continue
            if key == 'ghcc':
                serverProgressMsId = SCD.data.get('serverExpAddProgressId', 0)
                if gameconfigCommon.enableServerExpAddLimit() and serverProgressMsId and not p.checkServerProgress(serverProgressMsId, False):
                    continue
            if clickType == 'checkTipsBeforeShow':
                isLockState = self.isLockedState(tipsId)
                if isLockState:
                    clickType = 'showTips'
                else:
                    clickType = 'showPanel'
            elif clickType == 'showTips':
                isLockState = self.isLockedState(tipsId)
            else:
                isLockState = False
            fuliList.append({'key': key,
             'btnName': btnName,
             'clickType': clickType,
             'tipsId': tipsId,
             'isLockState': isLockState})

        info['fuliList'] = fuliList
        return uiUtils.dict2GfxDict(info, True)

    def getItemsByType(self, itemId, rData):
        funcType = rData.get('funcType', 0)
        if funcType < 2:
            itemDesc = gameStrings.GUILD_ACTIVITY_ITEM_DAY_TEXT % self.getDoCnt(itemId)
        else:
            itemDesc = gameStrings.GUILD_ACTIVITY_ITEM_WEEK_TEXT % self.getDoCnt(itemId)
        itemShow = {'itemId': itemId,
         'funcType': funcType,
         'iconData': uiUtils.getGfxItemById(rData.get('actIcon', 0)),
         'isLocked': self.isLockedState(itemId),
         'isFinish': self.checkItemIsFinish(itemId),
         'itemName': rData.get('actName', ''),
         'itemDesc': itemDesc,
         'sortId': rData.get('sortId', 0)}
        showPanelKey = rData.get('showPanelKey', '')
        if showPanelKey == 'ghqd':
            itemShow['label'] = gameStrings.GUILD_ACTIVITY_ITEM_SIGN_IN_LABEL
            itemShow['clickType'] = 'showPanel'
            itemShow['clickKey'] = '' if itemShow['isFinish'] else showPanelKey
        else:
            itemShow['label'] = gameStrings.GUILD_ACTIVITY_ITEM_GO_LABEL
            itemShow['clickType'] = 'go'
            itemShow['clickKey'] = self.getNpcSeekId(itemId)
        itemShow['isShowMembersBtn'] = rData.get('isShowMembersBtn', 0)
        itemShow['openProxyKey'] = rData.get('openProxyKey', '')
        return itemShow

    def isLockedState(self, tipsId):
        guild = BigWorld.player().guild
        if not guild:
            return True
        aData = GIATD.data.get(tipsId, {})
        attachBuildId = aData.get('attachBuildId', -1)
        if attachBuildId < 0:
            return False
        if not guild.hasSpace:
            return True
        lv = guild.getBuildingLevelById(attachBuildId)
        attachBuildLv = aData.get('attachBuildLv', 0)
        if lv >= attachBuildLv:
            return False
        return True

    def getNpcSeekId(self, playRecommId):
        tipsId = GIAD.data.get(playRecommId, {}).get('tipsId', 0)
        return GIATD.data.get(tipsId, {}).get('npcSeedId')

    def getFuLiDoCnt(self, playRecommId):
        tipsId = GIFD.data.get(playRecommId, {}).get('tipsId')
        aData = GIATD.data.get(tipsId, {})
        dayCntType = aData.get('dayCntType', 0)
        if dayCntType == 1:
            doCnt = '%d/%s' % (self.checkItemCnt(aData, playRecommId), str(aData.get('dayCnt', 1)))
        elif dayCntType == 2:
            doCnt = str(self.checkItemCnt(aData, playRecommId))
        else:
            doCnt = aData.get('dayCnt', '')
        return doCnt

    def checkItemCnt(self, aData, playRecommId):
        needCnt = aData.get('needCnt')
        if not needCnt:
            return 1
        p = BigWorld.player()
        doCnt = 0
        needCntType = needCnt[0]
        if needCntType == 1:
            for questLoopId in needCnt[1:]:
                if not p.questLoopInfo.has_key(questLoopId):
                    return 0
                qldd = QLD.data.get(questLoopId, {})
                maxLoopCnt = qldd.get('maxLoopCnt', 1)
                if p.questLoopInfo[questLoopId].loopCnt < maxLoopCnt:
                    return p.questLoopInfo[questLoopId].loopCnt

            doCnt = p.questLoopInfo[questLoopId].loopCnt
        else:
            if needCntType == 2:
                return 0
            if needCntType == 3:
                if needCnt[1] == gametypes.GUILD_ACTIVITY_MATCH:
                    doCnt = int(gameglobal.rds.ui.guildActivity.getActivitySate() == -1)
                elif needCnt[1] == gametypes.GUILD_BUILDING_ASTROLOGY_ID:
                    doCnt = p.dailyAstrologyCount
                elif needCnt[1] == gametypes.GUILD_BUILDING_GROWTH_ID:
                    doCnt = str(len([ x for x in p.guildWSPractice if x and utils.isSameDay(x.tStart) and x.isFinished() ])) + '/' + str(len([ x for x in p.guildWSPractice if x ]))
                elif needCnt[1] == gametypes.GUILD_ACTIVITY_RUN_MAN:
                    doCnt = int(self.checkItemIsFinish(playRecommId))
                elif needCnt[1] == gametypes.GUILD_ACTIVITY_ROUND_TABLE:
                    doCnt = int(utils.isSameDay(getattr(p, 'lastOpenRoundTableTimeInfo', {}).get(gametypes.ROUND_TABLE_TYPE_GUILD, 0), utils.getNow()))
                elif needCnt[1] == gametypes.GUILD_ACTIVITY_ROBBER:
                    cid = SCD.data.get('activityRobberBox', 0)
                    doCnt = self.bonusHistory.get(cid, 0)
                else:
                    doCnt = int(p.guild._getActivity(needCnt[1]).getState() == gametypes.GUILD_ACTIVITY_END)
            elif needCntType == 4:
                lv = p.lv
                for questLoops in needCnt[1:]:
                    if lv < questLoops[0] or lv > questLoops[1]:
                        continue
                    else:
                        for questLoopId in questLoops[2:]:
                            if not p.questLoopInfo.has_key(questLoopId):
                                return 0
                            qldd = QLD.data.get(questLoopId, {})
                            maxLoopCnt = qldd.get('maxLoopCnt', 1)
                            if p.questLoopInfo[questLoopId].loopCnt < maxLoopCnt:
                                return p.questLoopInfo[questLoopId].loopCnt

                        doCnt = p.questLoopInfo[questLoopId].loopCnt

            elif needCntType == 5:
                doCnt = 1 if p.guildSignIn else 0
            elif needCntType == 6:
                doCnt = 1 if p.guildBonfire else 0
            elif needCntType == 7:
                doCnt = p.guildFubenRoundNum.get(needCnt[1], 0)
        return doCnt

    def getItemUseCnt(self, itemId):
        cdata = CID.data.get(itemId, {})
        if not cdata.has_key('useLimit'):
            return 0
        useLimit = cdata['useLimit']
        group = cdata['useLimitGroup'] if cdata.has_key('useLimitGroup') else 0
        key = (gametypes.ITEM_USE_CHECK_GROUP, group) if group > 0 else (gametypes.ITEM_USE_CHECK_SINGLE, itemId)
        if key not in self.itemUseHistory:
            return 0
        history = self.itemUseHistory[key]
        used = 0
        for limitType, limitNum in useLimit:
            num = min(utils.getUseLimitByLv(itemId, self.lv, limitType, limitNum), limitNum)
            if limitType == gametypes.ITEM_USE_LIMIT_TYPE_FOREVER:
                used = history.get(limitType, 0)
                if used >= num:
                    used = num
                    break

        return used

    def onBackHome(self, *arg):
        gameglobal.rds.ui.skill.useGuildSkill(uiConst.GUILD_SKILL_DZG)

    def onAutoFindPath(self, *arg):
        seekId = int(arg[3][0].GetNumber())
        if not seekId:
            return
        uiUtils.findPosWithAlert(seekId)

    def onGetItemTipData(self, *args):
        playRecommId = int(args[3][0].GetNumber())
        giadd = GIAD.data
        tipsId = giadd.get(playRecommId, {}).get('tipsId')
        seekId = self.getNpcSeekId(playRecommId)
        giatdd = GIATD.data
        aData = giatdd.get(tipsId, {})
        aData['name'] = giadd.get(playRecommId, {}).get('actName', gameStrings.TEXT_GAME_1747)
        aData['funcType'] = giadd.get(playRecommId, {}).get('funcType', 1)
        displayType = aData.get('displayType', ())
        ret = self.uiAdapter.playRecomm.genLvUpItemInfo(aData, displayType, playRecommId, True)
        isLocked = self.isLockedState(tipsId)
        if isLocked:
            ret['alertMsgDesc'] = self.getLockedDesc(aData)
        needHidePath = aData.get('needHidePath', 0)
        if isLocked and needHidePath:
            return uiUtils.dict2GfxDict(ret, True)
        if seekId:
            try:
                entryInfo = {}
                entryInfo['entryName'] = aData.get('npcName')
                entryInfo['entryTrackId'] = seekId
                entryInfo['enableFly'] = True
                entryInfo['entryIcon'] = 'tzg'
                entryInfo['isGuild'] = True
                ret['entryList'].append(entryInfo)
            except:
                pass

        return uiUtils.dict2GfxDict(ret, True)

    def getLockedDesc(self, aData):
        attachBuildId = aData.get('attachBuildId', -1)
        desName = GBD.data.get(attachBuildId, {}).get('name', aData['name'])
        attachBuildLv = aData.get('attachBuildLv', 0)
        return gameStrings.GUILDITEM_LOCKED_DESC % (desName, attachBuildLv)

    def genLvUpItemInfo(self, aData, dType, prId, playRecommId):
        ret = {}
        lv = BigWorld.player().lv
        ret.update(aData)
        ret['enableGroup'] = False
        ret['memberNum'] = aData.get('num', '')
        ret['entryList'] = []
        ret['rewardInfo'] = self.getRewardInfo(aData)
        ret['funcType'] = 1
        if playRecommId < 20000:
            ret['dayCnt'] = self.getDoCnt(playRecommId)
        else:
            ret['dayCnt'] = self.getFuLiDoCnt(playRecommId)
        defaultDesc = gameStrings.TEXT_GUILDPROXY_3361
        if ret['funcType'] != 1:
            defaultDesc = gameStrings.TEXT_GUILDPROXY_3363
        ret['dayCntDesc'] = aData.get('dayCntDesc', defaultDesc)
        ret['reCommendCnt'] = aData.get('reCommendCnt', '')
        ret['reCommendJob'] = aData.get('reCommendJob', '')
        return ret

    def getDoCnt(self, playRecommId):
        tipsId = GIAD.data.get(playRecommId, {}).get('tipsId', 0)
        aData = GIATD.data.get(tipsId, {})
        dayCntType = aData.get('dayCntType', 0)
        if dayCntType == 1:
            doCnt = '%d/%s' % (self.checkItemCnt(aData, playRecommId), str(aData.get('dayCnt', 1)))
        elif dayCntType == 2:
            doCnt = str(self.checkItemCnt(aData, playRecommId))
        elif dayCntType == 3:
            doCnt = self.getGuildPuzzleCnt(aData)
        else:
            doCnt = aData.get('dayCnt', '')
        return doCnt

    def getRewardInfo(self, aData):
        bonusIcon = []
        bonusItem = []
        rInfo = {}
        if aData.get('rewardDesc'):
            rInfo['type'] = 'guildContribution'
            rInfo['desc'] = aData.get('rewardDesc')
            bonusIcon.append(rInfo)
        for itemId in aData.get('rewardShow', ()):
            bonusItem.append(uiUtils.getGfxItemById(itemId, 1, appendInfo={'isMain': True}))

        ret = {}
        ret['bonusIcon'] = bonusIcon
        ret['bonusItem'] = bonusItem
        return ret

    def onGetFuLiTipData(self, *args):
        playRecommId = int(args[3][0].GetNumber())
        gifdd = GIFD.data
        tipsId = gifdd.get(playRecommId, {}).get('tipsId')
        giatdd = GIATD.data
        aData = giatdd.get(tipsId, {})
        seekId = aData.get('npcSeedId')
        aData['name'] = gifdd.get(playRecommId, {}).get('fuliName', gameStrings.TEXT_GAME_1747)
        displayType = aData.get('displayType', ())
        ret = self.uiAdapter.playRecomm.genLvUpItemInfo(aData, displayType, playRecommId, True)
        isLocked = self.isLockedState(tipsId)
        if isLocked:
            ret['alertMsgDesc'] = self.getLockedDesc(aData)
        needHidePath = aData.get('needHidePath', 0)
        if isLocked and needHidePath:
            return uiUtils.dict2GfxDict(ret, True)
        if seekId:
            entryInfo = {}
            entryInfo['entryName'] = aData.get('npcName')
            entryInfo['entryTrackId'] = seekId
            entryInfo['enableFly'] = True
            entryInfo['entryIcon'] = 'tzg'
            ret['entryList'].append(entryInfo)
        return uiUtils.dict2GfxDict(ret, True)

    def checkItemIsFinish(self, playRecommId):
        giadData = GIAD.data.get(playRecommId, {})
        tipsId = giadData.get('tipsId', 0)
        aData = GIATD.data.get(tipsId, {})
        needCnt = aData.get('needCnt')
        if not needCnt:
            return True
        needCntType = needCnt[0]
        p = BigWorld.player()
        if needCntType == 1:
            for questLoopId in needCnt[1:]:
                if not p.questLoopInfo.has_key(questLoopId):
                    return False
                qldd = QLD.data.get(questLoopId, {})
                maxLoopCnt = qldd.get('maxLoopCnt', 1)
                if p.questLoopInfo[questLoopId].loopCnt < maxLoopCnt:
                    return False

        else:
            if needCntType == 2:
                return False
            if needCntType == 3:
                if needCnt[1] == gametypes.GUILD_ACTIVITY_MATCH:
                    return gameglobal.rds.ui.guildActivity.getActivitySate() == -1
                elif needCnt[1] == gametypes.GUILD_ACTIVITY_RUN_MAN:
                    runManType = giadData.get('funcType')
                    return p.runMan.getRoute(runManType).isFinished()
                elif needCnt[1] == gametypes.GUILD_ACTIVITY_ROBBER:
                    cid = SCD.data.get('activityRobberBox', 0)
                    doCnt = self.bonusHistory.get(cid, 0)
                    return doCnt >= BHCD.data.get(cid, {}).get('times', 1)
                elif needCnt[1] == gametypes.GUILD_ACTIVITY_PUZZLE:
                    curCnt = p.guildPuzzleCnt
                    maxCnt = int(aData.get('dayCnt', '1'))
                    return curCnt >= maxCnt
                else:
                    return p.guild._getActivity(needCnt[1]).getState() == gametypes.GUILD_ACTIVITY_END
            elif needCntType == 4:
                lv = p.lv
                meetLv = False
                for questLoops in needCnt[1:]:
                    if lv < questLoops[0] or lv > questLoops[1]:
                        continue
                    else:
                        meetLv = True
                        for questLoopId in questLoops[2:]:
                            if not p.questLoopInfo.has_key(questLoopId):
                                return False
                            qldd = QLD.data.get(questLoopId, {})
                            maxLoopCnt = qldd.get('maxLoopCnt', 1)
                            if p.questLoopInfo[questLoopId].loopCnt < maxLoopCnt:
                                return False

                if not meetLv:
                    return False
            else:
                if needCntType == 5:
                    return p.guildSignIn
                if needCntType == 6:
                    return p.guildBonfire
                if needCntType == 7:
                    maxCnt = int(aData.get('dayCnt', '1'))
                    curCnt = p.guildFubenRoundNum.get(needCnt[1], 0)
                    return curCnt >= maxCnt
        return True

    def refreshGuildActivityInfo(self):
        if self.mediator:
            self.mediator.Invoke('refreshActivityInfo')

    def refreshGuildInfo(self):
        self.refreshMemberInfo()
        self.refreshResourceInfo()
        self.refreshGuildActivityInfo()

    def getCompositeShopId(self, info):
        p = BigWorld.player()
        for eventId, shopId in info:
            if not eventId or p.checkServerProgress(eventId, False):
                return shopId

        return 0

    def onOpenPanel(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        if not p.guild:
            return
        if key == 'zbf':
            buildLv = p.guild.getBuildingLevelById(gametypes.GUILD_BUILDING_TREASURE_SHOP_ID)
            zbfInfo = GCD.data.get('guildCompositeShopZBFInfo', {})
            uiUtils.closeCompositeShop()
            p.base.openPrivateShop(0, self.getCompositeShopId(zbfInfo.get(buildLv, [(0, 0)])))
        elif key == 'qxf':
            buildLv = p.guild.getBuildingLevelById(gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID)
            qxfInfo = GCD.data.get('guildCompositeShopQXFInfo', {})
            uiUtils.closeCompositeShop()
            p.base.openPrivateShop(0, self.getCompositeShopId(qxfInfo.get(buildLv, [(0, 0)])))
        elif key == 'ghcc':
            gameglobal.rds.ui.guildInherit.show()
        elif key == 'ghpm':
            gameglobal.rds.ui.guildAuction.show(uiConst.GUILD_AUCTION_TAB_GUILD)
        elif key == 'ghhb':
            gameglobal.rds.ui.guildRedPacket.show()
        elif key == 'ghqd':
            gameglobal.rds.ui.guildSignInV2.show()
        elif key == 'gmbFb':
            gameglobal.rds.ui.guildMembersFbRank.show()
        elif key == 'guildSkill':
            gameglobal.rds.ui.clanWarSkill.show()

    def onItemGo(self, *arg):
        seekId = int(arg[3][0].GetNumber())
        uiUtils.gotoTrack(seekId)
        gameglobal.rds.uiLog.addFlyLog(seekId)

    def isGuildActiveFinish(self, playRecommId):
        tipsId = GIAD.data.get(playRecommId, {}).get('tipsId', 0)
        aData = GIATD.data.get(tipsId, {})
        dayCntType = aData.get('dayCntType', 0)
        if dayCntType == 1:
            doCnt = self.checkItemCnt(aData, playRecommId)
        elif dayCntType == 2:
            doCnt = self.checkItemCnt(aData, playRecommId)
        else:
            doCnt = aData.get('dayCnt', '')
        if doCnt > 0:
            return True
        return False

    def onGetEnableClan(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableClan', False))

    def setBonusHistory(self, data):
        _, res = data
        for cid, value in res.iteritems():
            if cid not in self.bonusHistory:
                self.bonusHistory[cid] = 0
            if self.bonusHistory[cid] != value:
                self.bonusHistory[cid] = value

    def getGuildPuzzleCnt(self, aData):
        p = BigWorld.player()
        curCnt = p.guildPuzzleCnt
        maxCnt = aData.get('dayCnt', '1')
        return '%d/%s' % (curCnt, maxCnt)

    def onGetDisabledGuildTab(self, *args):
        p = BigWorld.player()
        disGuildTabs = []
        isWingWorld = False
        if p.crossServerFlag == const.CROSS_SERVER_STATE_IN and p.inWingCity():
            isWingWorld = True
            disGuildTabs = SCD.data.get('crossServerDisabledGuildTabs', [2,
             3,
             4,
             5,
             6,
             7])
        disGuildTabs = {tabId:gameStrings.GUILD_TAB_IN_CROSS_TIP for tabId in disGuildTabs}
        return uiUtils.array2GfxAarry([disGuildTabs, isWingWorld])

    def onInitCrossClanWar(self, *args):
        self.uiAdapter.crossClanWar.initPanel(args[3][0])

    def onUnRegisterCrossClanWar(self, *args):
        self.uiAdapter.crossClanWar.unRegisterPanel()

    def onSetTournamentCraft(self, *args):
        itemIdx = int(args[3][0].GetNumber())
        craftId = int(args[3][1].GetNumber())
        if craftId == 0:
            return
        if craftId == gametypes.NEW_GTN_STRATEGY_WIN:
            confirmMsg = GCD.data.get('guildCraftConfirmMsgBS', gameStrings.GUILD_WW_TOURNAMENT_CRAFT_CONFIRM_BS)
            confirmBuffs = GCD.data.get('guildCraftConfirmMsgBuffIds', [])
        else:
            confirmMsg = GCD.data.get('guildCraftConfirmMsgCJBS', gameStrings.GUILD_WW_TOURNAMENT_CRAFT_CONFIRM_CJBS)
            confirmBuffs = GCD.data.get('guildCraftConfirmMsgBuffIds', [])
        gameglobal.rds.ui.descriptionWithBuff.show(gameStrings.GUILD_TOURNAMENT_STRAGY_TITLE, confirmMsg, confirmBuffs, Functor(self.confirmSetCraft, itemIdx, craftId))
        self.refreshRankTournamentInfo()

    def confirmSetCraft(self, itemIdx, craftId):
        p = BigWorld.player()
        if itemIdx % 2 == 0:
            groupId = gametypes.GUILD_TOURNAMENT_GROUP_QL
        else:
            groupId = gametypes.GUILD_TOURNAMENT_GROUP_BH
        if itemIdx >= 2:
            roundNum = 2
        else:
            roundNum = 1
        p.cell.chooseNewGuildTournamentStrategy(groupId, 0, craftId, 0, roundNum)

    def onSetTournamentBf(self, *args):
        itemIdx = int(args[3][0].GetNumber())
        bfId = int(args[3][1].GetNumber())
        p = BigWorld.player()
        if itemIdx % 2 == 0:
            groupId = gametypes.GUILD_TOURNAMENT_GROUP_QL
        else:
            groupId = gametypes.GUILD_TOURNAMENT_GROUP_BH
        if itemIdx >= 2:
            roundNum = 2
        else:
            roundNum = 1
        p.cell.chooseNewGuildTournamentStrategy(groupId, 0, 0, bfId, roundNum)
        self.refreshRankTournamentInfo()

    def onLvRewardBtnClick(self, *args):
        gameglobal.rds.ui.generalReward.show(GCD.data.get('rankTournamentRewardKey', 0))

    def onLvRankBtnClick(self, *args):
        gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_NGT_RANK)

    def onShowRankTournamentApply(self, *args):
        p = BigWorld.player()
        groupId = int(args[3][0].GetNumber())
        rankTournament = p.crossRankGtn.get(groupId)
        if rankTournament != None and rankTournament.canEnter:
            p.cell.enterNewGTN(groupId)
            gameglobal.rds.ui.bFScoreAward.setBFInfo(groupId, uiConst.BF_SCORE_AWARD_GUILD_TOURNAMENT)
        else:
            msg = GCD.data.get('rankTournamentApplyConfirm', gameStrings.GUILD_WW_TOURNAMENT_APPLY_CONFIRM)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.doApply, groupId), yesBtnText=gameStrings.CONFIRM, noCallback=None, noBtnText=gameStrings.CANCEL)

    @ui.checkInventoryLock()
    def doApply(self, groupId):
        p = BigWorld.player()
        p.cell.applyNewGuildTournament(groupId, 0)

    def onGetEnableRankTournament(self, *args):
        enable = self.getEnableRankTournament()
        return GfxValue(enable)

    def getEnableRankTournament(self):
        p = BigWorld.player()
        enable = False
        if gameglobal.rds.configData.get('enableNewGuildTournament', True):
            enable = True
            eventIds = GCD.data.get('serverEventId', [])
            for eventIdInfo in eventIds:
                eventId = eventIdInfo[1]
                if not p.isServerProgressFinished(eventId):
                    enable = False
                    break
                finishTime = p.getServerProgressFinishTime(eventId)
                if utils.isSameWeek(finishTime, utils.getNow()):
                    enable = False
                    break

        return enable

    def isEnableNewCrossTournament(self):
        return True

    def onGtnLiveBtnClick(self, *args):
        groupId = int(args[3][0].GetNumber())
        p = BigWorld.player()
        p.cell.enterNewGTNWithLive(groupId, p.guild.nuid)

    def onGtnCheerBtnClick(self, *args):
        groupId = int(args[3][0].GetNumber())
        p = BigWorld.player()
        p.cell.requireInspireGuildTournamentMembers()

    def refreshGtnInspireCoolDown(self):
        countTime = gameglobal.rds.ui.bFGuildTournamentLive.getCoolDownDurationTime()
        totalTime = GCD.data.get('inspireGuildTournamentCd', 0)
        if self.mediator:
            self.mediator.Invoke('setGtnInspireCoolDown', (GfxValue(countTime), GfxValue(totalTime)))
