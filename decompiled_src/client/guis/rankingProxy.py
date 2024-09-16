#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rankingProxy.o
from gamestrings import gameStrings
import time
import BigWorld
from Scaleform import GfxValue
import zlib
import cPickle
import gameglobal
import const
import gametypes
import clientUtils
import formula
import utils
import copy
import events
import gamelog
from guis import ui
from guis import uiConst
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import UIProxy
from guis import uiUtils
from gameStrings import gameStrings
from data import school_data as SD
from data import top_fb_data as TFD
from data import guild_top_reward_data as GTRD
from cdata import top_reward_data as TRD
from cdata import game_msg_def_data as GMDD
from cdata import fb_top_server_data as FTSD
from data import title_data as TD
from data import group_fb_rank_reward_data as GFRRD
from data import mail_template_data as MTD
from data import sys_config_data as SCD
from cdata import endless_challenge_season_list_data as ECSLD
from data import rankingV2_common_data as RV2CD
from data import rank_common_data as RCD
from data import rank_common_format_data as RCFD
from data import new_server_activity_data as NSAD
from guis.asObject import ASObject
from guis import rankPanelUtils
from guis.asObject import TipManager
from guis import rankCommonUtils
from callbackHelper import Functor
from guis import voidLunHuiHelper
GUILD_TAB_IDX = 16
TEAM_TAB_IDX = 15
HUANJING_TAB_IDX = 13
SOCIETY_TAB_IDX = 9
CARRYTOPID_FAMER = 1
CARRYTOPID_ROLE = 2
CARRYTOPID_HUANJING = 3
CARRYTOPID_FUBEN = 4
CARRYTOPID_GUILD = 5
CARRYTOPID_SHEJIAO = 6

class RankingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RankingProxy, self).__init__(uiAdapter)
        self.modelMap = {'requestSociety': self.onRequestSociety,
         'requestFuben': self.onRequestFuben,
         'requestAchieve': self.onRequestAchieve,
         'requestGuild': self.onRequestGuild,
         'requestCombat': self.onRequestCombat,
         'requestLv': self.onRequestLv,
         'requestEquip': self.onRequestEquip,
         'requestTeam': self.onRequestTeam,
         'requestHuanjing': self.onRequestHuanjing,
         'getMySchool': self.onGetMySchool,
         'getMySchoolId': self.onGetMySchoolId,
         'getMyLvStr': self.onGetMyLvStr,
         'initFubenList': self.onInitFubenList,
         'initTeamFubenList': self.onInitTeamFubenList,
         'updateRankList': self.onUpdateRankList,
         'openRewardPanel': self.onOpenRewardPanel,
         'openTeamDetailPanel': self.onOpenTeamDetailPanel,
         'getTeamDetailData': self.onGetTeamDetailData,
         'closeTeamDetailPanel': self.closeTeamDetailPanel,
         'getLaseWeekRankList': self.onGetLaseWeekRankList,
         'openLaseWeekRankList': self.onOpenLaseWeekRankList,
         'closeLaseWeekRankList': self.onCloseLaseWeekRankList,
         'updateTeamFbRank': self.onUpdateTeamFbRank,
         'enableTeamFuben': self.enableTeamFuben,
         'requestShejiao': self.onRequestShejiao,
         'enableShejiao': self.onEnableShejiao,
         'getAwardInfo': self.onGetAwardInfo,
         'closeRankAward': self.onCloseRankAward,
         'getTopReward': self.onGetTopReward,
         'setCurSchool': self.onSetCurSchool,
         'enableGuibaoRank': self.onEnableGuibaoRank,
         'enableApprenticeValRank': self.onEnableApprenticeValRank,
         'enableGuildKindnessRank': self.onEnableGuildKindnessRank,
         'enablePersonalZone': self.onEnablePersonalZone,
         'enableGuildRobberRank': self.onEnableGuildRobberRank,
         'enableHomeWealthRank': self.onEnableHomeWealthRank,
         'updateHuanjingRank': self.onUpdateHuanjingRank,
         'initHuanjingCurseasonFbdata': self.onInitHuanjingCurseasonFbdata,
         'enableHuanjing': self.onEnableHuanjing,
         'enableGuildFishingRank': self.onEnableGuildFishingRank,
         'enableGuildBaiFengYanRank': self.onEnableGuildBaiFengYanRank,
         'enableGuildMonsterClanWarRank': self.onEnableMonsterClanWarRank,
         'enableGuildPrestigeRank': self.onEnableGuildPrestigeRank,
         'enableGuildMatchOptimize': self.onEnableGuildMatchOptimize,
         'enableGuildLady': self.onEnableGuildLady,
         'handleTabChangeEvent': self.handleTabChangeEvent,
         'initSchoolMenu': self.initSchoolMenu,
         'cachePanelInfo': self.cachePanelInfo,
         'requestSprite': self.onRequestSprite,
         'showSpriteDetailTip': self.onShowSpriteDetailTip,
         'requestCommonRank': self.onRequestCommonRank,
         'showCommonAward': self.showCommonAward,
         'getMyLv': self.onGetMyLv,
         'getDefaultDropdownIdx': self.getDefaultDropdownIdx}
        self.mediator = None
        self.teamDetailMed = None
        self.rewardMed = None
        self.evalMed = None
        self.lastRewardMed = None
        self.proxyId = 0
        self.displayType = uiConst.RANK_TYPE_OTHER
        self.tabId = 0
        self.fbId = 0
        self.mySchoolIdx = 0
        self.schoolList = SD.data.keys()
        self.socialLvInfo = {}
        self.achieveInfo = {}
        self.fubenInfo = {}
        self.guildInfo = {}
        self.combatInfo = {}
        self.lvInfo = {}
        self.equipInfo = {}
        self.teamInfo = {}
        self.teamDetailInfo = {}
        self.lastWeekRankInfo = {}
        self.lastWeekRankList = {}
        self.shejiaoInfo = {}
        self.huanjingCurInfo = {}
        self.huanjingHeroInfo = {}
        self.huanjingFriendInfo = {}
        self.commonRankInfo = {}
        self.spriteInfo = {}
        self.spriteDetailInfo = {}
        self.huanjingUpdateTimer = None
        self.huanjingCurSeason = 0
        self.rewardType = 0
        self.rewardFbNo = 0
        self.teamId = 0
        self.teamName = ''
        self.teamfbNo = 0
        self.teamDataType = 0
        self.teamInfoUuid = {}
        self.lastWeekRankFbNo = 0
        self.myLastWeekRank = 0
        self.teamUpdateTimer = None
        self.teamRankEval = {}
        self.fbTeamTimer = None
        self.awardType = None
        self.awardStype = None
        self.curSchool = 0
        self.lvInterval = ()
        self.rankTeamFbNo = 0
        self.guildActivity = 0
        self.cachedPanelInfo = {}
        self.cachedVariableArray = ['currentFbNo',
         'shejiaoType',
         'currentHuanjingFbNo',
         'tabIndex',
         'guildActivity',
         'gender']
        self.rankIdDict = {const.PROXY_KEY_TOP_FB_TIME: gametypes.TOP_TYPE_FB,
         const.PROXY_KEY_TOP_GUILD_MATCH: gametypes.TOP_TYPE_GUILD_MATCH,
         const.PROXY_KEY_TOP_GUILD_HUNT: gametypes.TOP_TYPE_GUILD_HUNT,
         const.PROXY_KEY_TOP_GUILD_ROBBER_RANK: gametypes.TOP_TYPE_GUILD_ROBBER,
         const.PROXY_KEY_TOP_GUILD_PROSPERITY: gametypes.TOP_TYPE_GUILD_PROPERITY,
         const.PROXY_KEY_TOP_COMBAT_SCORE: gametypes.TOP_TYPE_COMBAT_SCORE,
         const.PROXY_KEY_GROUP_FB_RANK: gametypes.TOP_TYPE_GROUP_FB_RANK,
         const.PROXY_KEY_GROUP_ZHENYAO_RANK: gametypes.TOP_TYPE_GROUP_ZHENYAO_RANK,
         const.PROXY_KEY_ENDLESS_CHALLENGE: gametypes.TOP_TYPE_ENDLESS_CHALLENGE,
         const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY: gametypes.TOP_TYPE_GUILD_FISH_ACTIVITY,
         const.PROXY_KEY_TOP_GUILD_CHICKEN_MEAL: gametypes.TOP_TYPE_GUILD_CHICKEN_MEAL,
         const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR: gametypes.TOP_TYPE_GUILD_MONSTER_CLAN_WAR,
         const.PROXY_KEY_TOP_GUILD_YMF: gametypes.TOP_TYPE_GUILD_YMF,
         const.PROXY_KEY_WING_WORLD_OPEN_DONATE: gametypes.TOP_TYPE_WING_WORLD_OPEN_DONATE_RANK,
         const.PROXY_KEY_WING_WORLD_BOSS_DAMAGE: gametypes.TOP_TYPE_WING_WORLD_BOSS_DAMAGE_RANK,
         const.PROXY_KEY_NPC_FAVOR: gametypes.TOP_TYPE_NPC_FAVOR}
        self.topTypeDict = {gametypes.TOP_TYPE_FB: const.PROXY_KEY_TOP_FB_TIME,
         gametypes.TOP_TYPE_GUILD_MATCH: const.PROXY_KEY_TOP_GUILD_MATCH,
         gametypes.TOP_TYPE_GUILD_HUNT: const.PROXY_KEY_TOP_GUILD_HUNT,
         gametypes.TOP_TYPE_GUILD_ROBBER: const.PROXY_KEY_TOP_GUILD_ROBBER_RANK,
         gametypes.TOP_TYPE_GUILD_PROPERITY: const.PROXY_KEY_TOP_GUILD_PROSPERITY,
         gametypes.TOP_TYPE_COMBAT_SCORE: const.PROXY_KEY_TOP_COMBAT_SCORE,
         gametypes.TOP_TYPE_GROUP_FB_RANK: const.PROXY_KEY_GROUP_FB_RANK,
         gametypes.TOP_TYPE_GUILD_FISH_ACTIVITY: const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY,
         gametypes.TOP_TYPE_GUILD_CHICKEN_MEAL: const.PROXY_KEY_TOP_GUILD_CHICKEN_MEAL,
         gametypes.TOP_TYPE_GUILD_MONSTER_CLAN_WAR: const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR,
         gametypes.TOP_TYPE_NPC_FAVOR: const.PROXY_KEY_NPC_FAVOR}
        self.huanjingRankIdDict = {const.PROXY_KEY_ENDLESS_CHALLENGE, const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND, const.PROXY_KEY_ENDLESS_CHALLENGE_HERO}
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANKING_TEAM_DETAIL, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANKING_LAST_WEEK_LIST, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANKING, self.hide)
        self.updateBtnCooldownTimeDic = {}
        self.commonRankConfig = {}
        self._awardInfoFunc = None
        self.cardExtraInfo = {}

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RANKING:
            self.initCommonRankConfig()
            gamelog.debug('ypc@ commonRankConfig = ', self.commonRankConfig)
            if self.fbTeamTimer == None:
                nextWeek = utils.getNextCrontabTime('0 0 * * 0', utils.getNow()) - utils.getNow()
                self.fbTeamTimer = BigWorld.callback(nextWeek, self.resetFbTeamData)
            self.mediator = mediator
            self.relayoutTabButtons()
            self.initTabDropdownMenu()
            self.schoolMenu = rankPanelUtils.SchoolMenuUtil()
            self.cachedPanelInfo['myRankBtnTip'] = gbk2unicode(SCD.data.get('myRankBtnTip', ''))
            return uiUtils.dict2GfxDict({'cachedPanelInfo': uiUtils.dict2GfxDict(self.cachedPanelInfo),
             'commonInitData': uiUtils.dict2GfxDict(self.commonRankConfig, True)})
        elif widgetId == uiConst.WIDGET_RANK_AWARD:
            self.rewardMed = mediator
            return GfxValue(1)
        elif widgetId == uiConst.WIDGET_RANK_AWARD_V2:
            self.rewardMed = mediator
            return GfxValue(2)
        else:
            if widgetId == uiConst.WIDGET_RANKING_TEAM_DETAIL:
                self.teamDetailMed = mediator
            else:
                if widgetId == uiConst.WIDGET_RANKING_TEAM_EVAL:
                    self.evalMed = mediator
                    return uiUtils.dict2GfxDict(self._getTeamRankEval())
                if widgetId == uiConst.WIDGET_RANKING_LAST_WEEK_LIST:
                    self.lastRewardMed = mediator
                    return uiUtils.dict2GfxDict({'fbNo': self.lastWeekRankFbNo})
            return

    def cachePanelInfo(self, *args):
        cachedVarDic = ASObject(args[3][0])
        for varName in self.cachedVariableArray:
            self.cachedPanelInfo[varName] = cachedVarDic.__getattr__(varName)

    def initTabDropdownMenu(self):
        self.asMediator = ASObject(self.mediator)
        self.asWidget = self.asMediator.getWidget()
        self.curDropdownMenu = None
        self.asWidget.roleBtn.dropdown = self.asWidget.roleDropdown
        self.asWidget.guildBtn.dropdown = self.asWidget.guildDropdown
        self.asWidget.shejiaoBtn.dropdown = self.asWidget.shejiaoDropdown
        self.asWidget.famerBtn.dropdown = self.asWidget.famerDropdown
        self.dropdownBtns = [self.asWidget.roleBtn,
         self.asWidget.guildBtn,
         self.asWidget.shejiaoBtn,
         self.asWidget.famerBtn]
        self.asWidget.huanjingDropdown.visible = False
        self.asWidget.fubenDropdown.visible = False
        isHuanjingDropdown = False
        isFubenDropdown = False
        for tData in self.commonRankConfig.values():
            carrytopIdLv1 = tData['CarrytopIdLv1']
            if isinstance(carrytopIdLv1, int):
                if carrytopIdLv1 == CARRYTOPID_HUANJING:
                    isHuanjingDropdown = True
                if carrytopIdLv1 == CARRYTOPID_FUBEN:
                    isFubenDropdown = True
            elif isinstance(carrytopIdLv1, tuple):
                for i in carrytopIdLv1:
                    if i == CARRYTOPID_HUANJING:
                        isHuanjingDropdown = True
                    if i == CARRYTOPID_FUBEN:
                        isFubenDropdown = True

        if isHuanjingDropdown:
            self.asWidget.huanjingDropdown.visible = True
            self.asWidget.huanjingBtn.dropdown = self.asWidget.huanjingDropdown
            self.dropdownBtns.append(self.asWidget.huanjingBtn)
        if isFubenDropdown:
            self.asWidget.fubenDropdown.visible = True
            self.asWidget.fubenBtn.dropdown = self.asWidget.fubenDropdown
            self.dropdownBtns.append(self.asWidget.fubenBtn)
        for btn in self.dropdownBtns:
            btn.addEventListener(events.MOUSE_ROLL_OVER, self.handleTabDropdownRollOver, False, 0, False)
            btn.addEventListener(events.MOUSE_ROLL_OUT, self.handleTabDropdownRollOut, False, -1, False)
            btn.dropdown.visible = False
            btn.dropdown.showCount = 0
            btn.dropdown.x = btn.x
            btn.dropdown.y = btn.y + btn.height
            btn.dropdown.addEventListener(events.MOUSE_ROLL_OVER, self.handleTabDropdownRollOver, False, 0, False)
            btn.dropdown.addEventListener(events.MOUSE_ROLL_OUT, self.handleTabDropdownRollOut, False, -1, False)
            for i in xrange(0, btn.dropdown.numChildren):
                item = btn.dropdown.getChildAt(i)
                if item.label is not None:
                    item.allowDeselect = True
                    item.addEventListener(events.MOUSE_CLICK, self.handleTabDropdownMenuItemClick, False, -1, False)

    def initSchoolMenu(self, *args):
        noAllType = args[3][0].GetBool()
        self.schoolMenu.unregister()
        self.schoolMenu.register(self.asWidget.schoolDropdown, self.onSchoolMenuChange, rankPanelUtils.getDefaultSchoolMenuData() if noAllType else rankPanelUtils.getCompleteMenuData())

    def handleTabDropdownRollOver(self, *args):
        e = ASObject(args[3][0])
        self.__showDrodownMenu(self.__getDropdownMenuFromEventTarget(e))

    def handleTabDropdownRollOut(self, *args):
        e = ASObject(args[3][0])
        self.__hideDropdownMenu(self.__getDropdownMenuFromEventTarget(e))

    def handleTabDropdownMenuItemClick(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.selected = True
        self.__hideDropdownMenu(e.currentTarget.parent)

    def __getDropdownMenuFromEventTarget(self, e):
        if e.currentTarget.dropdown is not None:
            return e.currentTarget.dropdown
        else:
            return e.currentTarget

    def __showDrodownMenu(self, dropdownMenu):
        dropdownMenu.showCount += 1
        dropdownMenu.parent.setChildIndex(dropdownMenu, dropdownMenu.parent.numChildren - 1)
        dropdownMenu.visible = True
        self.curDropdownMenu = dropdownMenu

    def __hideDropdownMenu(self, dropdownMenu):
        dropdownMenu.showCount -= 1
        if dropdownMenu.showCount <= 0:
            dropdownMenu.visible = False
            dropdownMenu.showCount = 0

    def handleTabChangeEvent(self, *args):
        if self.curDropdownMenu is not None and self.curDropdownMenu.visible:
            self.curDropdownMenu.parent.setChildIndex(self.curDropdownMenu, self.curDropdownMenu.parent.numChildren - 1)
        if self.asMediator.getCurrentView().updateBtn is not None:
            self.asMediator.getCurrentView().updateBtn.addEventListener(events.MOUSE_CLICK, self.handleUpdateBtnClick, False, 0, False)

    def onSchoolMenuChange(self):
        self.mediator.Invoke('handleSchoolMenuChangeEvent', GfxValue(self.schoolMenu.menuData[self.schoolMenu.menuMc.selectedIndex]['schoolId']))

    def show(self, tabId = 0, displayType = uiConst.RANK_TYPE_OTHER, fbNo = 0, isCommonRank = False, initDropdownIdx = 0):
        self.tabId = tabId
        self.displayType = displayType
        self.fbId = fbNo
        if self.displayType == uiConst.RANK_TYPE_OTHER and self.tabId == HUANJING_TAB_IDX and not gameglobal.rds.configData.get('enableEndlessChallenge', False):
            self.tabId = SOCIETY_TAB_IDX
        if self.tabId != 0:
            self.cachedPanelInfo['tabIndex'] = self.tabId
        if fbNo != 0:
            self.cachedPanelInfo['currentFbNo'] = fbNo
        self.cachedPanelInfo['isCommonRank'] = isCommonRank
        self.cachedPanelInfo['initDropdownIdx'] = initDropdownIdx
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANKING)

    def showTeamRankPanel(self, rankTeamFbNo = 0):
        self.displayType = uiConst.RANK_TYPE_OTHER
        self.rankTeamFbNo = rankTeamFbNo
        self.tabId = TEAM_TAB_IDX
        self.cachedPanelInfo['tabIndex'] = TEAM_TAB_IDX
        if rankTeamFbNo != 0:
            self.cachedPanelInfo['currentFbNo'] = rankTeamFbNo
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANKING)

    def showGuildRankPanel(self, guildActivity = 0):
        self.displayType = uiConst.RANK_TYPE_OTHER
        self.guildActivity = guildActivity
        self.tabId = GUILD_TAB_IDX
        self.cachedPanelInfo['tabIndex'] = GUILD_TAB_IDX
        if guildActivity != 0:
            self.cachedPanelInfo['guildActivity'] = guildActivity
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANKING)

    def showHuanjingRankPanel(self, rankProxy):
        if not gameglobal.rds.configData.get('enableEndlessChallenge', False):
            return
        self.displayType = uiConst.RANK_TYPE_OTHER
        self.tabId = HUANJING_TAB_IDX
        self.fbId = rankProxy
        self.cachedPanelInfo['tabIndex'] = HUANJING_TAB_IDX
        self.cachedPanelInfo['currentHuanjingFbNo'] = rankProxy
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANKING)

    def clearWidget(self):
        if self.teamDetailMed:
            self._closeTeamDetail()
            return
        elif self.lastRewardMed:
            self._closeLastWeekRankPanel()
            return
        else:
            self.mediator = None
            self.tabId = 0
            self.displayType = 0
            self.fbId = 0
            self.guildActivity = 0
            self.rankTeamFbNo = 0
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RANKING)
            if self.uiAdapter.funcNpc.isOnFuncState():
                self.uiAdapter.funcNpc.close()
            self.cachedPanelInfo = {}
            return

    def clearAllData(self):
        self.mediator = None
        self.teamDetailMed = None
        self.rewardMed = None
        self.evalMed = None
        self.lastRewardMed = None
        self.proxyId = 0
        self.displayType = uiConst.RANK_TYPE_OTHER
        self.tabId = 0
        self.fbId = 0
        self.mySchoolIdx = 0
        self.schoolList = SD.data.keys()
        self.socialLvInfo = {}
        self.achieveInfo = {}
        self.fubenInfo = {}
        self.guildInfo = {}
        self.combatInfo = {}
        self.lvInfo = {}
        self.equipInfo = {}
        self.teamInfo = {}
        self.teamDetailInfo = {}
        self.lastWeekRankInfo = {}
        self.lastWeekRankList = {}
        self.huanjingCurInfo = {}
        self.huanjingHeroInfo = {}
        self.huanjingFriendInfo = {}
        self.huanjingUpdateTimer = None
        self.huanjingCurSeason = 0
        self.rewardType = 0
        self.rewardFbNo = 0
        self.teamId = 0
        self.teamName = ''
        self.teamfbNo = 0
        self.teamDataType = 0
        self.teamInfoUuid = {}
        self.lastWeekRankFbNo = 0
        self.myLastWeekRank = 0
        self.teamUpdateTimer = None
        self.teamRankEval = {}
        self.shejiaoInfo = {}
        self.spriteInfo = {}
        self.cachedPanelInfo = {}
        self.updateBtnCooldownTimeDic = {}

    def reset(self):
        super(self.__class__, self).reset()
        self.resetData()

    def resetData(self):
        self.proxyId = 0
        self.displayType = uiConst.RANK_TYPE_OTHER
        self.tabId = 0
        self.fbId = 0
        self.mySchoolIdx = 0
        self.rewardType = 0
        self.rewardFbNo = 0
        self._awardInfoFunc = None

    def onGetMySchool(self, *arg):
        self.mySchoolIdx = BigWorld.player().realSchool
        school = SD.data[self.mySchoolIdx]['name'] if self.mySchoolIdx in self.schoolList else ''
        return GfxValue(gbk2unicode(school))

    def onGetMySchoolId(self, *arg):
        schoolIdx = BigWorld.player().realSchool
        return GfxValue(schoolIdx)

    def onGetMyLv(self, *args):
        p = BigWorld.player()
        return GfxValue(p.lv)

    def onGetMyLvStr(self, *arg):
        return GfxValue(self._getPlayerTopRankKey())

    def _getPlayerTopRankKey(self):
        p = BigWorld.player()
        if 1 <= p.lv <= 59:
            if self.proxyId in self.huanjingRankIdDict:
                return '50_59'
        return uiUtils.getPlayerTopRankKey()

    def _getRankingLvKey(self, key):
        if key == gametypes.ALL_LV_TOP_RANK_KEY:
            return key
        else:
            return key[0:len(key) - 2]

    def _generateTestData(self, proxyID, info):
        ret = {}
        ret['rankType'] = self.proxyId
        ret['list'] = []
        ret['myRank'] = 0
        schoolNames = [gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_1597,
         gameStrings.TEXT_RANKINGPROXY_517,
         gameStrings.TEXT_RANKINGPROXY_517_1,
         gameStrings.TEXT_RANKINGPROXY_517_2,
         gameStrings.TEXT_RANKINGPROXY_517_3,
         gameStrings.TEXT_RANKINGPROXY_517_4,
         gameStrings.TEXT_RANKINGPROXY_517_5]
        schoolCount = len(schoolNames)
        selfIndex = 4
        for index in xrange(1, 20):
            obj = {}
            obj['index'] = index
            obj['roleName'] = gameStrings.TEXT_RANKINGPROXY_525 + str(index)
            if proxyID == const.PROXY_KEY_TOP_LEVEL:
                obj['val'] = '123_456_1234567890'
            else:
                obj['val'] = '1234567890'
            obj['school'] = schoolNames[index % schoolCount]
            obj['isSelf'] = index == selfIndex
            obj['finishTime'] = '1234567890'
            if obj['isSelf']:
                obj['myRank'] = index
                ret['myRank'] = index
            t = time.localtime(BigWorld.player().getServerTime())
            obj['now'] = gameStrings.TEXT_FORMULA_1568 % (t.tm_year, t.tm_mon, t.tm_mday)
            ret['list'].append(obj)

        if proxyID == const.PROXY_KEY_TOP_COMBAT_SCORE:
            ret['myTotalCombat'] = BigWorld.player().combatScoreList[const.COMBAT_SCORE]
        return uiUtils.dict2GfxDict(ret, True)

    def updateSpriteDetailInfo(self, uuid, info):
        self.spriteDetailInfo[uuid] = info

    def _generateData(self, proxyID, info):
        ret = {}
        ret['rankType'] = self.proxyId
        ret['list'] = []
        ret['myRank'] = 0
        clanWarRank = 1
        myName = BigWorld.player().realRoleName
        myGuildName = BigWorld.player().guildName
        for i, item in enumerate(info):
            obj = {}
            if proxyID == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
                if i == 0:
                    clanWarRank = 1
                elif item[2][0] != info[i - 1][2][0]:
                    clanWarRank += 1
                index = clanWarRank
            else:
                index = i + 1
            if proxyID == const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND:
                roleName = item[3]
            elif proxyID == const.PROXY_KEY_TOP_SPRITE_COMBAT_SCORE:
                roleName = item[2]
                self.spriteDetailInfo[item[0]] = item
                obj['spriteUUID'] = item[0]
            else:
                roleName = item[1]
            if proxyID in (const.PROXY_KEY_TOP_GUILD_PROSPERITY,
             const.PROXY_KEY_TOP_CLAN_WAR_SCORE,
             const.PROXY_KEY_TOP_GUILD_MATCH,
             const.PROXY_KEY_TOP_GUILD_HUNT,
             const.PROXY_KEY_TOP_GUILD_ROBBER_RANK,
             const.PROXY_KEY_TOP_GUILD_KINDNESS,
             const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY,
             const.PROXY_KEY_TOP_GUILD_CHICKEN_MEAL,
             const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR,
             const.PROXY_KEY_TOP_GUILD_PRESTIGE,
             const.PROXY_KEY_TOP_GUILD_LADY_RANK):
                isSelf = myGuildName == roleName
            else:
                isSelf = myName == roleName
            if proxyID == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
                val = item[2][0]
            elif proxyID == const.PROXY_KEY_TOP_GUILD_PROSPERITY:
                val = item[2]
            elif proxyID in (const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY, const.PROXY_KEY_TOP_GUILD_CHICKEN_MEAL, const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR):
                val = item[2][0]
            elif proxyID == const.PROXY_KEY_TOP_GUILD_KINDNESS:
                val = item[2] / 100
            elif proxyID in (const.PROXY_KEY_TOP_GUILD_HUNT, const.PROXY_KEY_TOP_GUILD_ROBBER_RANK):
                val = utils.formatTimeStr(item[2], 'h:m:s', True, 2, 2, 2)
            elif proxyID == const.PROXY_KEY_TOP_LEVEL:
                val = str(item[3][3]) + '_' + str(item[3][0]) + '_' + str(item[3][1])
            elif proxyID in (const.PROXY_KEY_TOP_FB_TIME, const.PROXY_KEY_ENDLESS_CHALLENGE):
                val = item[3][0]
            elif proxyID in (const.PROXY_KEY_TOP_GUILD_MATCH, const.PROXY_KEY_TOP_GUILD_PRESTIGE):
                if type(item[2]) is tuple:
                    val = item[2][0]
                else:
                    val = item[2]
            elif proxyID == const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND:
                val = item[0]
            elif proxyID == const.PROXY_KEY_TOP_GUILD_LADY_RANK:
                val = item[3][0]
            elif proxyID == const.PROXY_KEY_TOP_SPRITE_COMBAT_SCORE:
                val = item[6]
            else:
                val = item[3]
            val = int(val) if type(val) == type(1) or type(val) == type(1.0) else val
            if proxyID == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
                finishTime = item[2][2]
            elif proxyID == const.PROXY_KEY_TOP_GUILD_MATCH:
                if gameglobal.rds.configData.get('enableGuildMatchOptimize', False):
                    if type(item[2]) is tuple:
                        finishTime = utils.formatTimeStr(-item[2][1], 'm:s', True, 2, 2)
                    else:
                        finishTime = ''
                else:
                    finishTime = ''
            elif proxyID in (const.PROXY_KEY_TOP_GUILD_HUNT,
             const.PROXY_KEY_TOP_GUILD_ROBBER_RANK,
             const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY,
             const.PROXY_KEY_TOP_GUILD_CHICKEN_MEAL,
             const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR):
                finishTime = item[1]
            elif proxyID == const.PROXY_KEY_TOP_FB_TIME:
                finishTime = item[3][1]
            elif proxyID == const.PROXY_KEY_ENDLESS_CHALLENGE:
                finishTime = utils.formatTimeStr(-item[3][1], 'h:m:s', True, 2, 2, 2)
            elif proxyID == const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND:
                finishTime = utils.formatTimeStr(-item[1], 'h:m:s', True, 2, 2, 2)
            elif proxyID == const.PROXY_KEY_TOP_SPRITE_COMBAT_SCORE:
                finishTime = item[8]
            else:
                finishTime = 0
            if proxyID == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
                school = item[2][1]
            elif proxyID in (const.PROXY_KEY_TOP_GUILD_PROSPERITY,
             const.PROXY_KEY_TOP_GUILD_MATCH,
             const.PROXY_KEY_TOP_GUILD_HUNT,
             const.PROXY_KEY_TOP_GUILD_ROBBER_RANK,
             const.PROXY_KEY_TOP_GUILD_KINDNESS,
             const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY,
             const.PROXY_KEY_TOP_GUILD_CHICKEN_MEAL,
             const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR):
                school = item[3]
            elif proxyID == const.PROXY_KEY_TOP_GUILD_PRESTIGE:
                school = item[4]
            elif proxyID == const.PROXY_KEY_TOP_GUILD_LADY_RANK:
                school = item[3][2]
            else:
                schoolKey = item[3] if proxyID == const.PROXY_KEY_TOP_SPRITE_COMBAT_SCORE else item[2]
                school = SD.data[schoolKey]['name'] if schoolKey in self.schoolList else 'unknown'
            obj['index'] = index
            obj['roleName'] = roleName
            obj['val'] = val
            obj['school'] = school
            obj['isSelf'] = isSelf
            obj['finishTime'] = finishTime
            if isSelf:
                obj['myRank'] = index
                if ret['myRank'] == 0:
                    ret['myRank'] = index
            t = time.localtime(BigWorld.player().getServerTime())
            obj['now'] = gameStrings.TEXT_FORMULA_1568 % (t.tm_year, t.tm_mon, t.tm_mday)
            ret['list'].append(obj)

        if proxyID == const.PROXY_KEY_TOP_COMBAT_SCORE:
            ret['myTotalCombat'] = BigWorld.player().combatScoreList[const.COMBAT_SCORE]
        return uiUtils.dict2GfxDict(ret, True)

    def refreshLvSelected(self, lvKey):
        if self.mediator:
            ASObject(self.mediator).lvKey = lvKey

    def _getRewardInfo(self, proxyID, fbNo = 0):
        if self.lastWeekRankInfo.has_key(proxyID):
            if fbNo == 0:
                return self.lastWeekRankInfo[proxyID]
            elif self.lastWeekRankInfo[proxyID].has_key(fbNo):
                return self.lastWeekRankInfo[proxyID][fbNo]
            else:
                return [0,
                 0,
                 0,
                 0]
        else:
            return [0,
             0,
             0,
             0]

    def _setRewardInfo(self, proxyID, fbNo = 0, rankInfo = (0, 0, 0, 0)):
        if self.lastWeekRankInfo.has_key(proxyID):
            if fbNo == 0:
                self.lastWeekRankInfo[proxyID] = rankInfo
            elif self.lastWeekRankInfo[proxyID].has_key(fbNo):
                self.lastWeekRankInfo[proxyID][fbNo] = rankInfo

    def onUpdateRankList(self, *arg):
        proxyId = int(arg[3][0].GetNumber())
        lvKey = arg[3][1].GetString()
        p = BigWorld.player()
        if proxyId == const.PROXY_KEY_TOP_PERSONAL_ZONE_GIFT:
            p.base.getTopZoneGift(self.shejiaoInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_PERSONAL_ZONE_POPULARITY:
            p.base.getTopZonePopularity(self.shejiaoInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_HOME_WEALTH:
            p.base.getTopHomeWealth(self.shejiaoInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_HAOQI:
            p.cell.refreshTopHaoqiScore(self.shejiaoInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_RENPIN:
            p.cell.refreshTopRenpinScore(self.shejiaoInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_APPEARANCE_POINT:
            ver = 0
            if self.shejiaoInfo.has_key(const.PROXY_KEY_TOP_ACHIEVE_POINTS):
                ver = self.shejiaoInfo[const.PROXY_KEY_TOP_ACHIEVE_POINTS]['ver']
            p.base.getTopAppearancePoint(ver)
            return
        elif proxyId == const.PROXY_KEY_TOP_APPRENTICE_VAL:
            p.base.getTopApprenticeVal(self.shejiaoInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_GUILD_LADY_RANK:
            p.cell.refreshTopGuildLadyRank(self.shejiaoInfo.get(proxyId, {}).get('ver', 0))
            return
        elif proxyId == const.PROXY_KEY_TOP_GUILD_KINDNESS:
            p.cell.getTopGuildKindness(self.guildInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY:
            p.cell.refreshTopGuildFishActivityScore(self.guildInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_GUILD_CHICKEN_MEAL:
            p.cell.refreshTopGuildChickenMealScore(self.guildInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR:
            p.cell.refreshTopGuildMonsterClanWarScore(self.guildInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_GUILD_PRESTIGE:
            p.cell.refreshTopGuildPrestige(self.guildInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_TOTAL_GONGJI_FAME:
            p.cell.refreshTopTotalPopularity(self.shejiaoInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_SPRITE_COMBAT_SCORE:
            self.requestSpriteData(lvKey)
            return
        elif proxyId == const.PROXY_KEY_TOP_TOTAL_POPULARITY_FEMALE:
            p.base.getTopTotalPopularityFemale(self.shejiaoInfo.get(proxyId, {}).get('ver'))
            return
        elif proxyId == const.PROXY_KEY_TOP_TOTAL_POPULARITY_MALE:
            p.base.getTopTotalPopularityMale(self.shejiaoInfo.get(proxyId, {}).get('ver'))
            return
        else:
            if proxyId == const.PROXY_KEY_TOP_EQUIP_SCORE:
                p.cell.refreshTopEquipScores(self.equipInfo.get(lvKey, {}).get('ver', 0))
                if self.equipInfo.has_key(lvKey):
                    self.updateEquipData(self.equipInfo[lvKey].get('ver', 0), self.equipInfo[lvKey].get('info', []), lvKey)
            elif proxyId == const.PROXY_KEY_TOP_LEVEL:
                p.base.getTopXiuWeiLevelTopData(self.lvInfo.get('ver', 0), '')
                if self.lvInfo != None:
                    self.updateLvData(self.lvInfo.get('ver', 0), self.lvInfo.get('info', []))
            elif proxyId == const.PROXY_KEY_TOP_ACHIEVE_POINTS:
                p.cell.refreshTopAchPoints(self.achieveInfo.get(lvKey, {}).get('ver', 0))
                if self.achieveInfo.has_key(lvKey):
                    rewardInfo = self._getRewardInfo(const.PROXY_KEY_TOP_ACHIEVE_POINTS)
                    self.updateAchieveData(self.achieveInfo[lvKey].get('ver', 0), self.achieveInfo[lvKey].get('info', []), rewardInfo, lvKey)
            elif proxyId == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
                p.cell.refreshTopClanWarScore(self.guildInfo.get(const.PROXY_KEY_TOP_CLAN_WAR_SCORE, {}).get('ver', 0))
            elif proxyId == const.PROXY_KEY_TOP_SOCAIL_LEVEL:
                p.cell.refreshTopSocLevel(self.socialLvInfo.get(lvKey, {}).get('ver', 0))
                if self.socialLvInfo.has_key(lvKey):
                    self.updateSocietyData(self.socialLvInfo[lvKey].get('ver', 0), self.socialLvInfo[lvKey].get('info', []), lvKey)
            elif proxyId == const.PROXY_KEY_TOP_COMBAT_SCORE:
                if lvKey != 'allLv':
                    lvKey += '_' + str(0)
                p.cell.refreshCombatScore(self.combatInfo.get(lvKey, {}).get('ver', 0))
                if self.combatInfo.has_key(lvKey):
                    rewardInfo = self._getRewardInfo(const.PROXY_KEY_TOP_COMBAT_SCORE)
                    self.updateCombatData(self.combatInfo[lvKey].get('ver', 0), self.combatInfo[lvKey].get('info', 0), rewardInfo, lvKey)
            return

    def onOpenRewardPanel(self, *arg):
        rankId = int(arg[3][0].GetNumber())
        awardStype = int(arg[3][1].GetNumber())
        useNewAwardPanel = len(arg[3]) >= 3 and arg[3][2].GetBool()
        self.openRewardPanel(rankId, awardStype, (), useNewAwardPanel)

    def openRewardPanel(self, rankId, awardStype, lvInterval = (), useNewAwardPanel = False, awardInfoFunc = None):
        self.closeAwardPanel()
        self.awardType = self.rankIdDict[rankId] if self.rankIdDict.has_key(rankId) else 0
        self.awardStype = awardStype
        self.lvInterval = lvInterval
        self._awardInfoFunc = awardInfoFunc
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANK_AWARD_V2 if useNewAwardPanel else uiConst.WIDGET_RANK_AWARD)

    def onGetLaseWeekRankList(self, *arg):
        fbNo = int(arg[3][0].GetNumber())
        if self.proxyId == const.PROXY_KEY_GROUP_FB_RANK:
            if self.lastWeekRankList.has_key(const.PROXY_KEY_GROUP_FB_RANK):
                self.updateLastWeekRankList(self.lastWeekRankList[const.PROXY_KEY_GROUP_FB_RANK].get(fbNo, []), fbNo)
            BigWorld.player().cell.groupFubenTopBakDataQuery(fbNo)

    def onRequestSociety(self, *arg):
        lvKey = arg[3][0].GetString()
        self.proxyId = const.PROXY_KEY_TOP_SOCAIL_LEVEL
        if lvKey == '':
            lvKey = self._getPlayerTopRankKey()
        p = BigWorld.player()
        cacheData = self.socialLvInfo.get(lvKey, {})
        ver = cacheData.get('ver', 0)
        self.updateSocietyData(ver, cacheData.get('info', []), lvKey)
        p.base.getTopSocLevel(ver, lvKey)

    def updateSocietyData(self, ver, info, lvKeyStr):
        self.socialLvInfo[lvKeyStr] = {}
        self.socialLvInfo[lvKeyStr]['ver'] = ver
        self.socialLvInfo[lvKeyStr]['info'] = info
        self.refreshSocietyView(info)
        self.refreshLvSelected(lvKeyStr)
        gamelog.debug('ypc@updateSocietyData ver = ', ver)

    def refreshSocietyView(self, info):
        if self.mediator:
            ret = self._generateData(const.PROXY_KEY_TOP_SOCAIL_LEVEL, info)
            p = BigWorld.player()
            info = {}
            info['lv'] = gameStrings.TEXT_RANKINGPROXY_880 + str(p.socLv)
            info['time'] = rankCommonUtils._getDeadlineTime()
            self.mediator.Invoke('refreshSocietyView', (ret, uiUtils.dict2GfxDict(info, True)))
            self.refreshUpdateBtnState()

    def initializeFubenInfo(self):
        if self.fubenInfo == None:
            self.fubenInfo = {}
            for x in TFD.data:
                fbNo = TFD.data.get(x, {}).get('fbNo', 0)
                key = '%d' % fbNo
                self.fubenInfo[key] = [0, []]
                for idx in SD.data:
                    key = '%d_%d' % (fbNo, idx)
                    self.fubenInfo[key] = [0, []]

    def onInitFubenList(self, *arg):
        ret = self._getFbList()
        return uiUtils.array2GfxAarry(ret, True)

    def _getFbList(self, *arg):
        fbNames = []
        fbData = TFD.data
        fbServerData = FTSD.data
        for idx in fbData:
            fbNo = fbData.get(idx, {}).get('fbNo', 0)
            reward = fbData.get(idx, {}).get('reward', 0)
            showCategory = fbServerData.get(fbNo, {}).get('isByClass', 0)
            limitMax = fbServerData.get(fbNo, {}).get('limitLvMax', 0)
            if limitMax != 0:
                lvMax = uiUtils.getTextFromGMD(GMDD.data.CRAZYMODE_ITEM_NEED_TIP, gameStrings.TEXT_RANKINGPROXY_914) % limitMax
            else:
                lvMax = ''
            fbNames.append([idx,
             fbNo,
             reward,
             showCategory,
             lvMax])

        fbNames.sort()
        ret = []
        for idx, fbName in enumerate(fbNames):
            obj = {}
            detailName = formula.getFbDetailName(fbName[1])
            obj['id'] = fbName[0]
            obj['name'] = detailName
            obj['reward'] = fbName[2]
            obj['showCategory'] = fbName[3]
            obj['lvMax'] = fbName[4]
            obj['fbNo'] = fbName[1]
            ret.append(obj)

        return ret

    def onInitTeamFubenList(self, *arg):
        teamFbConst = const.GROUP_FB_TOP_TYPE_MAP.keys()
        ret = []
        excludeFbNos = NSAD.data.get('jingSuFubens', {}).keys()
        for fbNo in teamFbConst:
            if fbNo in excludeFbNos:
                continue
            obj = {}
            detailName = formula.getFbDetailName(fbNo)
            obj['name'] = detailName
            obj['fbNo'] = fbNo
            ret.append(obj)

        return uiUtils.array2GfxAarry(ret, True)

    @ui.callInCD(1)
    def onRequestFuben(self, *arg):
        self.initializeFubenInfo()
        self.proxyId = const.PROXY_KEY_TOP_FB_TIME
        school = int(arg[3][0].GetNumber())
        fbNo = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        if school == 0:
            key = '%d' % fbNo
        else:
            key = '%d_%d' % (fbNo, school)
        fubenVer = 0
        info = []
        lastWeekRank = self._getRewardInfo(const.PROXY_KEY_TOP_FB_TIME, fbNo)
        if self.fubenInfo.has_key(key):
            fubenVer = self.fubenInfo[key][0]
            info = self.fubenInfo[key][2]
        self.updateFubenData(fubenVer, info, lastWeekRank, fbNo, key)
        p.base.getTopFbTimes(fubenVer, fbNo, key)

    def updateFubenData(self, ver, info, lastWeekRankInfo, fbNo, lvKeyStr):
        self.fubenInfo[lvKeyStr] = [ver, fbNo, info]
        if not self.lastWeekRankInfo.has_key(const.PROXY_KEY_TOP_FB_TIME):
            self.lastWeekRankInfo[const.PROXY_KEY_TOP_FB_TIME] = {}
        self.lastWeekRankInfo[const.PROXY_KEY_TOP_FB_TIME][fbNo] = lastWeekRankInfo
        self.refreshFubenData(info, lastWeekRankInfo)

    def refreshFubenData(self, info, lastWeekRankInfo):
        if self.mediator:
            ret = self._generateData(const.PROXY_KEY_TOP_FB_TIME, info)
            rewardInfo = {}
            rewardInfo['rank'] = lastWeekRankInfo[1] if lastWeekRankInfo[1] else 0
            rewardInfo['enable'] = lastWeekRankInfo[3] if lastWeekRankInfo[3] else 0
            rewardInfo['time'] = rankCommonUtils._getDeadlineTime()
            self.mediator.Invoke('refreshFubenView', (ret, uiUtils.dict2GfxDict(rewardInfo, True)))

    def onRequestAchieve(self, *arg):
        lvKey = arg[3][0].GetString()
        if lvKey == '':
            lvKey = self._getPlayerTopRankKey()
        p = BigWorld.player()
        self.proxyId = const.PROXY_KEY_TOP_ACHIEVE_POINTS
        cachedData = self.achieveInfo.get(lvKey, {})
        ver = cachedData.get('ver', 0)
        lastWeekRank = self._getRewardInfo(const.PROXY_KEY_TOP_ACHIEVE_POINTS)
        self.updateAchieveData(ver, cachedData.get('info', []), lastWeekRank, lvKey)
        p.base.getTopAchievePoints(ver, lvKey)

    def updateAchieveData(self, ver, info, lastWeekRankInfo, lvKeyStr):
        self.achieveInfo[lvKeyStr] = {}
        self.achieveInfo[lvKeyStr]['ver'] = ver
        self.achieveInfo[lvKeyStr]['info'] = info
        self.lastWeekRankInfo[const.PROXY_KEY_TOP_ACHIEVE_POINTS] = lastWeekRankInfo
        self.refreshAchieveView(info)
        self.refreshLvSelected(lvKeyStr)

    def refreshAchieveView(self, info):
        if self.mediator:
            ret = self._generateData(const.PROXY_KEY_TOP_ACHIEVE_POINTS, info)
            rewardInfo = {}
            rewardInfo['time'] = rankCommonUtils._getDeadlineTime()
            self.mediator.Invoke('refreshAchieveView', (ret, uiUtils.dict2GfxDict(rewardInfo, True)))
            self.refreshUpdateBtnState()

    def onRequestGuild(self, *arg):
        iType = int(arg[3][0].GetNumber())
        self.proxyId = iType
        ver = 0
        if self.guildInfo.has_key(iType):
            ver = self.guildInfo[iType]['ver']
            rewardInfo = self._getRewardInfo(iType)
            self.refreshGuildData(iType, self.guildInfo[iType]['info'], rewardInfo)
        else:
            self.refreshGuildData(iType, [], (0, 0, 0, 0))
        p = BigWorld.player()
        if iType == const.PROXY_KEY_TOP_GUILD_PROSPERITY:
            p.cell.getTopGuildProsperity(ver)
        elif iType == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
            p.base.getTopClanWarScore(ver)
        elif iType == const.PROXY_KEY_TOP_GUILD_MATCH:
            p.cell.getTopGuildMatch(ver)
        elif iType == const.PROXY_KEY_TOP_GUILD_HUNT:
            p.cell.getTopGuildHunt(ver)
        elif iType == const.PROXY_KEY_TOP_GUILD_ROBBER_RANK:
            p.cell.getTopGuildRobber(ver)
        elif iType == const.PROXY_KEY_TOP_GUILD_KINDNESS:
            p.cell.getTopGuildKindness(ver)
        elif iType == const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY:
            p.cell.getTopGuildFishActivity(ver)
        elif iType == const.PROXY_KEY_TOP_GUILD_CHICKEN_MEAL:
            p.cell.getTopGuildChickenMeal(ver)
        elif iType == const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR:
            p.cell.getTopGuildMonsterClanWar(ver)
        elif iType == const.PROXY_KEY_TOP_GUILD_PRESTIGE:
            p.cell.getTopGuildPrestige(ver)

    def updateGuildData(self, iType, ver, info, lastWeekRankInfo = []):
        self.lastWeekRankInfo[iType] = lastWeekRankInfo
        self.guildInfo[iType] = {'ver': ver,
         'info': info}
        self.refreshGuildData(iType, info, lastWeekRankInfo)

    def refreshGuildData(self, iType, info, lastWeekRankInfo):
        if self.mediator:
            ret = self._generateData(iType, info)
            rewardInfo = {}
            rewardInfo['rank'] = lastWeekRankInfo[1] if len(lastWeekRankInfo) > 0 and lastWeekRankInfo[1] else 0
            rewardInfo['enable'] = lastWeekRankInfo[3] if len(lastWeekRankInfo) > 0 and lastWeekRankInfo[3] else 0
            rewardInfo['time'] = rankCommonUtils._getDeadlineTime()
            rewardInfo['val'] = ''
            p = BigWorld.player()
            if iType == const.PROXY_KEY_TOP_GUILD_PROSPERITY:
                rewardInfo['val'] = gameStrings.TEXT_RANKINGPROXY_1076 % (p.guild.prosperity if p.guild else 0)
            elif iType == const.PROXY_KEY_TOP_GUILD_MATCH:
                rewardInfo['val'] = gameStrings.TEXT_RANKINGPROXY_1078 % (p.guild.matchScore if p.guild else 0)
            elif iType == const.PROXY_KEY_TOP_GUILD_KINDNESS:
                rewardInfo['val'] = gameStrings.TEXT_RANKINGPROXY_1080 % (p.guild.kindness / 100 if p.guild else 0)
            elif iType == const.PROXY_KEY_TOP_GUILD_FISH_ACTIVITY:
                rewardInfo['val'] = gameStrings.TEXT_RANKINGPROXY_1082 % (p.guild.fishActivityScore if p.guild else 0)
            elif iType == const.PROXY_KEY_TOP_GUILD_CHICKEN_MEAL:
                rewardInfo['val'] = gameStrings.TEXT_RANKINGPROXY_1084 % (p.guild.chickenMealScore if p.guild else 0)
            elif iType == const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR:
                rewardInfo['val'] = gameStrings.TEXT_RANKINGPROXY_1086 % (p.guild.monsterClanWarScore if p.guild else 0)
            elif iType == const.PROXY_KEY_TOP_GUILD_PRESTIGE:
                rewardInfo['val'] = gameStrings.TEXT_RANKINGPROXY_1088 % (p.guild.prestige if p.guild else 0)
            self.mediator.Invoke('refreshGuildView', (GfxValue(iType), ret, uiUtils.dict2GfxDict(rewardInfo, True)))
            self.refreshUpdateBtnState()

    def onRequestCombat(self, *arg):
        self.proxyId = const.PROXY_KEY_TOP_COMBAT_SCORE
        lvKey = arg[3][0].GetString()
        if lvKey == '':
            lvKey = self._getPlayerTopRankKey()
        if lvKey != gametypes.ALL_LV_TOP_RANK_KEY:
            lvKey += str('_' + str(0))
        p = BigWorld.player()
        cachedData = self.combatInfo.get(lvKey, {})
        ver = cachedData.get('ver', 0)
        rewardInfo = self._getRewardInfo(const.PROXY_KEY_TOP_COMBAT_SCORE)
        self.updateCombatData(ver, cachedData.get('info', []), rewardInfo, lvKey)
        p.base.getTopCombatScore(ver, lvKey)

    def updateCombatData(self, ver, info, lastWeekRankInfo, lvKeyStr):
        self.combatInfo[lvKeyStr] = {'ver': ver,
         'info': info}
        self.lastWeekRankInfo[const.PROXY_KEY_TOP_COMBAT_SCORE] = lastWeekRankInfo
        self.refreshCombatView(info, lastWeekRankInfo, lvKeyStr)
        lvkey = self._getRankingLvKey(lvKeyStr)
        self.refreshLvSelected(lvkey)

    def refreshCombatView(self, info, lastWeekRankInfo, lvKey):
        if self.mediator:
            ret = self._generateData(const.PROXY_KEY_TOP_COMBAT_SCORE, info)
            rewardInfo = {}
            rewardInfo['rank'] = lastWeekRankInfo[1] if lastWeekRankInfo[1] else 0
            rewardInfo['enable'] = lastWeekRankInfo[3] if lastWeekRankInfo[3] else 0
            rewardInfo['time'] = rankCommonUtils._getDeadlineTime()
            self.mediator.Invoke('refreshCombatView', (ret, uiUtils.dict2GfxDict(rewardInfo, True), GfxValue(lvKey)))
            self.refreshUpdateBtnState()

    def onRequestLv(self, *arg):
        self.proxyId = const.PROXY_KEY_TOP_LEVEL
        p = BigWorld.player()
        lvVer = self.lvInfo.get('ver', 0)
        self.updateLvData(lvVer, self.lvInfo.get('info', []))
        p.base.getTopXiuWeiLevelTopData(lvVer, '')

    def updateLvData(self, ver, info):
        self.lvInfo = {'ver': ver,
         'info': info}
        self.refreshLvView(info)

    def refreshLvView(self, info):
        if self.mediator:
            ret = self._generateData(const.PROXY_KEY_TOP_LEVEL, info)
            p = BigWorld.player()
            rewardInfo = {}
            rewardInfo['time'] = rankCommonUtils._getDeadlineTime()
            rewardInfo['xiuweiLevel'] = gameStrings.RANKINGV2_XIUWEI_LEVEL + str(p.xiuweiLevel)
            rewardInfo['lv'] = gameStrings.TEXT_RANKINGPROXY_1152 + str(p.lv)
            self.mediator.Invoke('refreshLvView', (ret, uiUtils.dict2GfxDict(rewardInfo, True)))
            self.refreshUpdateBtnState()

    def onRequestEquip(self, *arg):
        self.proxyId = const.PROXY_KEY_TOP_EQUIP_SCORE
        lvKey = arg[3][0].GetString()
        if lvKey == '':
            lvKey = self._getPlayerTopRankKey()
        p = BigWorld.player()
        ver = 0
        if self.equipInfo.has_key(lvKey):
            ver = self.equipInfo[lvKey].get('ver', 0)
            self.updateEquipData(ver, self.equipInfo[lvKey].get('info', []), lvKey)
        else:
            self.updateEquipData(ver, [], lvKey)
        p.base.getTopEquipScore(ver, lvKey)

    def updateEquipData(self, ver, info, lvKeyStr):
        self.equipInfo[lvKeyStr] = {'ver': ver,
         'info': info}
        self.refreshEquipView(info)
        self.refreshLvSelected(lvKeyStr)

    def refreshEquipView(self, info):
        if self.mediator:
            ret = self._generateData(const.PROXY_KEY_TOP_EQUIP_SCORE, info)
            p = BigWorld.player()
            rewardInfo = {}
            rewardInfo['score'] = gameStrings.TEXT_RANKINGPROXY_1184 + str(p.equipment.calcAllEquipScore(p.suitsCache))
            rewardInfo['time'] = rankCommonUtils._getDeadlineTime()
            self.mediator.Invoke('refreshEquipView', (ret, uiUtils.dict2GfxDict(rewardInfo, True)))
            self.refreshUpdateBtnState()

    def onRequestTeam(self, *arg):
        fbNo = int(arg[3][0].GetNumber())
        self.proxyId = const.PROXY_KEY_GROUP_FB_RANK
        ver = 0
        info = []
        if self.teamInfo.has_key(fbNo):
            info = self.teamInfo[fbNo]['info']
            ver = self.teamInfo[fbNo]['ver']
        self.updateTeamData(ver, info, fbNo)
        self.callTeamData(ver, fbNo)

    @ui.callInCD(30)
    def callTeamData(self, ver, fbNo):
        BigWorld.player().cell.groupFubenTopDataQuery(fbNo, ver)
        BigWorld.player().cell.groupFubenLastWeekRankQuery(fbNo)

    def updateTeamData(self, ver, data, fbNo):
        self.teamInfo[fbNo] = {'ver': ver,
         'info': data}
        myRank = 0
        myRanks = []
        data.sort(key=lambda k: k['fTimestamp'], reverse=True)
        data.sort(key=lambda k: k['finishTime'])
        data.sort(key=lambda k: k['score'], reverse=True)
        ret = []
        for i in xrange(len(data)):
            teamData = data[i]
            index = i + 1
            if teamData['hasMe']:
                myRanks.append({'index': index})

        if len(myRanks) > 0:
            myRank = myRanks[0]['index']
        for i in xrange(len(data)):
            teamObj = {}
            teamData = data[i]
            uuidStr = '%d' % teamData['nuid']
            self.teamInfoUuid[uuidStr] = teamData['nuid']
            teamObj['teamId'] = teamData['nuid']
            teamObj['index'] = i + 1
            teamObj['roleName'] = teamData['groupName']
            teamObj['finishTime'] = utils.formatTimeStr(teamData['finishTime'], 'h:m:s', True, 2, 2, 2)
            teamObj['val'] = teamData['score']
            teamObj['isSelf'] = teamObj['index'] == myRank
            ret.append(teamObj)

        self.refreshTeamView(myRank, ret)

    def refreshTeamView(self, myRank, ret):
        if self.mediator:
            info = {}
            info['rank'] = myRank
            info['timeTxt'] = rankCommonUtils._getDeadlineTime()
            info['rankType'] = self.proxyId
            self.mediator.Invoke('refreshTeamView', (uiUtils.dict2GfxDict(info, True), uiUtils.array2GfxAarry(ret, True)))
            self.refreshUpdateBtnState()

    def onOpenTeamDetailPanel(self, *arg):
        uuidStr = arg[3][0].GetString()
        self.teamfbNo = arg[3][2].GetNumber()
        self.teamName = unicode2gbk(arg[3][1].GetString())
        self.teamDataType = int(arg[3][3].GetNumber())
        self.openTeamDetail(self.teamfbNo, uuidStr, self.teamName, self.teamDataType)

    def openTeamDetail(self, fbNo, uuid, teamName, teamDataType = 0, fromRank = uiConst.GROUP_FUBEN_DETAIL_COMMON):
        if self.teamInfoUuid.has_key(uuid):
            self.teamId = self.teamInfoUuid[uuid]
        else:
            return
        self.teamName = teamName
        self.teamfbNo = fbNo
        self.teamDataType = teamDataType
        if self.teamDetailInfo.has_key(self.teamId):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANKING_TEAM_DETAIL)
        elif fromRank == uiConst.GROUP_FUBEN_DETAIL_COMMON:
            BigWorld.player().cell.groupFubenMemberDetailQuery(self.teamfbNo, self.teamDataType, self.teamId)
        elif fromRank == uiConst.GROUP_FUBEN_DETAIL_ZHENYAO:
            BigWorld.player().base.reqZhenyaoGroupInfo(self.teamId)

    def onGetTeamDetailData(self, *arg):
        ret = []
        if self.teamDetailInfo.has_key(self.teamId):
            ret = self._genTeamDetailData(self.teamDetailInfo[self.teamId])
        else:
            BigWorld.player().cell.groupFubenMemberDetailQuery(self.teamfbNo, self.teamDataType, self.teamId)
        return uiUtils.dict2GfxDict(ret, True)

    def updateTeamDetail(self, data):
        self.teamDetailInfo[self.teamId] = data
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANKING_TEAM_DETAIL)

    def _genTeamDetailData(self, data):
        ret = {}
        ret['teamName'] = self.teamName
        ret['list'] = []
        for i in xrange(len(data)):
            teamData = data[i]
            teamObj = {}
            teamObj['isLeader'] = teamData['isHeader']
            teamObj['playerName'] = teamData['roleName']
            teamObj['school'] = SD.data[teamData['school']]['name'] if teamData['school'] in self.schoolList else gameStrings.TEXT_GAME_1747
            teamObj['lv'] = teamData['level']
            ret['list'].append(teamObj)

        return ret

    def closeTeamDetailPanel(self, *arg):
        self._closeTeamDetail()

    def _closeTeamDetail(self):
        self.teamDetailMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RANKING_TEAM_DETAIL)

    def onOpenLaseWeekRankList(self, *arg):
        self.lastWeekRankFbNo = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANKING_LAST_WEEK_LIST)

    def onCloseLaseWeekRankList(self, *arg):
        self._closeLastWeekRankPanel()

    def _closeLastWeekRankPanel(self):
        self.lastRewardMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RANKING_LAST_WEEK_LIST)

    def updateLastWeekRankList(self, data, fbNo):
        ret = {}
        ret['proxyId'] = self.proxyId
        ret['list'] = []
        if self.proxyId == const.PROXY_KEY_GROUP_FB_RANK:
            if not self.lastWeekRankList.has_key(const.PROXY_KEY_GROUP_FB_RANK):
                self.lastWeekRankList[const.PROXY_KEY_GROUP_FB_RANK] = {}
            self.lastWeekRankList[const.PROXY_KEY_GROUP_FB_RANK][fbNo] = data
        data.sort(key=lambda k: k['rank'])
        for i in xrange(len(data)):
            teamObj = {}
            teamData = data[i]
            uuidStr = '%d' % teamData['nuid']
            self.saveTeamUuid(uuidStr, teamData['nuid'])
            teamObj['teamId'] = teamData['nuid']
            teamObj['index'] = teamData['rank']
            teamObj['roleName'] = teamData['groupName']
            teamObj['finishTime'] = utils.formatTimeStr(teamData['finishTime'], 'h:m:s', True, 2, 2, 2)
            teamObj['val'] = teamData['score']
            teamObj['isSelf'] = 0
            ret['list'].append(teamObj)

        if self.lastRewardMed:
            self.lastRewardMed.Invoke('updateView', uiUtils.dict2GfxDict(ret, True))

    def saveTeamUuid(self, uuidStr, nuid):
        self.teamInfoUuid[uuidStr] = nuid

    def showTeamRankEval(self, score, oldRank, curRank):
        if curRank > 0 and oldRank > 0:
            curRank = min(oldRank, curRank)
        elif curRank <= 0:
            curRank = oldRank
        self.teamRankEval = {'score': score,
         'oldRank': oldRank,
         'curRank': curRank}
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANKING_TEAM_EVAL)
        BigWorld.callback(60, self.autoCloseTeamRankEval)

    def autoCloseTeamRankEval(self):
        if self.evalMed:
            self.hideTeamRankEval()

    def hideTeamRankEval(self):
        self.evalMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RANKING_TEAM_EVAL)

    def _getTeamRankEval(self):
        ret = {}
        ret['score'] = self.teamRankEval.get('score', 0)
        ret['newRank'] = self.teamRankEval.get('curRank', 0)
        ret['oldRank'] = self.teamRankEval.get('oldRank', 0)
        return ret

    def _createRwardInfo(self, awardType, awardStype):
        if awardType == gametypes.TOP_TYPE_GROUP_FB_RANK or awardType == gametypes.TOP_TYPE_GROUP_ZHENYAO_RANK:
            return self._createTeamFbRewardInfo(awardStype)

    def _createTeamFbRewardInfo(self, fbNo):
        awardItems = []
        title, items = self._getTopAward(fbNo)
        for item in items:
            iconPath = uiUtils.getItemIconFile64(item[0])
            color = uiUtils.getItemColor(item[0])
            awardItems.append([iconPath,
             item[1],
             color,
             item[0]])

        titleStr = TD.data.get(title, {}).get('name', '')
        if titleStr:
            titleStr = gameStrings.TEXT_RANKINGPROXY_1399 % titleStr
        awardList = []
        tData = GFRRD.data.get(fbNo, {})
        for td in tData:
            lv = td.get('lv', ())
            if lv == self.lvInterval:
                desc = td.get('desc', '')
                title = TD.data.get(td.get('title', 0), {}).get('name', '')
                mailTempId = td.get('mailTemplateId', 0)
                bonusId = MTD.data.get(mailTempId, {}).get('bonusId', 0)
                p = BigWorld.player()
                if 'schoolTitles' in td:
                    schoolTitles = td.get('schoolTitles')
                    if p.school in schoolTitles:
                        title = TD.data.get(schoolTitles[p.school], {}).get('name', '')
                if 'schoolBonusIds' in td:
                    schoolBonusIds = td.get('schoolBonusIds')
                    if p.school in schoolBonusIds:
                        bonusId = schoolBonusIds[p.school]
                items = clientUtils.genItemBonus(bonusId)
                if not items:
                    items = ()
                itemList = []
                for item in items:
                    iconPath = uiUtils.getItemIconFile64(item[0])
                    color = uiUtils.getItemColor(item[0])
                    itemList.append([iconPath,
                     item[1],
                     color,
                     item[0]])

                awardList.append([desc, title, itemList])

        cash = BigWorld.player().cash
        desc = ''
        if self.awardType == gametypes.TOP_TYPE_GROUP_ZHENYAO_RANK:
            desc = gameStrings.TEXT_RANKINGPROXY_1438
        ret = [self.myLastWeekRank,
         False,
         awardItems,
         titleStr,
         awardList,
         cash,
         self.awardType,
         desc]
        return ret

    def _getTopAward(self, fbNo):
        rank = self.myLastWeekRank
        tData = GFRRD.data.get(fbNo, {})
        for td in tData:
            minRank = td['minRank']
            maxRank = td['maxRank']
            if not minRank <= rank <= maxRank:
                continue
            title = td.get('title', 0)
            mailTempId = td.get('mailTemplateId', 0)
            bonusId = MTD.data.get(mailTempId, {}).get('bonusId', 0)
            p = BigWorld.player()
            if 'schoolTitles' in td:
                schoolTitles = td.get('schoolTitles')
                if p.school in schoolTitles:
                    title = schoolTitles[p.school]
            if 'schoolBonusIds' in td:
                schoolBonusIds = td.get('schoolBonusIds')
                if p.school in schoolBonusIds:
                    bonusId = schoolBonusIds[p.school]
            items = clientUtils.genItemBonus(bonusId)
            if not items:
                items = ()
            return (title, items)

        return (0, [])

    def onUpdateTeamFbRank(self, *arg):
        if self.teamUpdateTimer == None:
            fbNo = int(arg[3][0].GetNumber())
            self.proxyId = const.PROXY_KEY_GROUP_FB_RANK
            ver = 0
            if self.teamInfo.has_key(fbNo):
                ver = self.teamInfo[fbNo]['ver']
            BigWorld.player().cell.groupFubenTopDataQuery(fbNo, ver)

    def enableTeamFuben(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableGroupFubenRank', False))

    def resetFbTeamData(self):
        self.teamInfo = {}
        self.teamDetailInfo = {}
        self.lastWeekRankList = {}
        self.myLastWeekRank = 0

    def onEnableShejiao(self, *arg):
        value = gameglobal.rds.configData.get('enableHaoqiVal', True) and gameglobal.rds.configData.get('enableRenpinVal', True)
        return GfxValue(value)

    def onRequestShejiao(self, *arg):
        iType = int(arg[3][0].GetNumber())
        self.proxyId = iType
        ver = 0
        if self.shejiaoInfo.has_key(iType):
            ver = self.shejiaoInfo[iType]['ver']
            rewardInfo = self._getRewardInfo(iType)
            self.refreshShejiaoData(iType, self.shejiaoInfo[iType]['info'], rewardInfo)
        else:
            self.refreshShejiaoData(iType, [], (0, 0, 0, 0))
        p = BigWorld.player()
        if iType == const.PROXY_KEY_TOP_RENPIN:
            p.base.getTopRenpin(ver)
        elif iType == const.PROXY_KEY_TOP_HAOQI:
            p.base.getTopHaoqi(ver)
        elif iType == const.PROXY_KEY_TOP_APPEARANCE_POINT:
            p.base.getTopAppearancePoint(ver)
        elif iType == const.PROXY_KEY_TOP_APPRENTICE_VAL:
            p.base.getTopApprenticeVal(ver)
        elif iType == const.PROXY_KEY_TOP_PERSONAL_ZONE_GIFT:
            p.base.getTopZoneGift(ver)
        elif iType == const.PROXY_KEY_TOP_PERSONAL_ZONE_POPULARITY:
            p.base.getTopZonePopularity(ver)
        elif iType == const.PROXY_KEY_TOP_HOME_WEALTH:
            p.base.getTopHomeWealth(ver)
        elif iType == const.PROXY_KEY_TOP_GUILD_LADY_RANK:
            p.cell.getTopGuildLadyRank(ver)
        elif iType == const.PROXY_KEY_TOP_TOTAL_GONGJI_FAME:
            p.base.getTotalGongjiTopRank(ver)
        elif iType == const.PROXY_KEY_TOP_TOTAL_POPULARITY_MALE:
            p.base.getTopTotalPopularityMale(ver)
        elif iType == const.PROXY_KEY_TOP_TOTAL_POPULARITY_FEMALE:
            p.base.getTopTotalPopularityFemale(ver)

    def updateShejiaoData(self, iType, ver, info, lastWeekRankInfo = []):
        self.lastWeekRankInfo[iType] = lastWeekRankInfo
        self.shejiaoInfo[iType] = {'ver': ver,
         'info': info}
        self.refreshShejiaoData(iType, info, lastWeekRankInfo)

    def refreshShejiaoData(self, iType, info, lastWeekRankInfo):
        if self.mediator:
            ret = self._generateData(iType, info)
            rewardInfo = {}
            if self.proxyId == const.PROXY_KEY_TOP_RENPIN:
                rewardInfo['point'] = gameStrings.RANKINGV2_GONGJI + str(getattr(BigWorld.player(), 'renpinValThisWeek', 0))
            elif self.proxyId == const.PROXY_KEY_TOP_HAOQI:
                rewardInfo['point'] = gameStrings.RANKINGV2_HAOQI + str(getattr(BigWorld.player(), 'haoqiValThisWeek', 0))
            elif self.proxyId == const.PROXY_KEY_TOP_APPEARANCE_POINT:
                rewardInfo['point'] = gameStrings.RANKINGV2_GUIBAO + str(getattr(BigWorld.player(), 'appearanceItemCollectPoint', 0))
            elif self.proxyId == const.PROXY_KEY_TOP_APPRENTICE_VAL:
                rewardInfo['point'] = gameStrings.RANKINGV2_SHITU + str(BigWorld.player().apprenticeVal.get('weeklyVal', 0))
            elif self.proxyId == const.PROXY_KEY_TOP_GUILD_LADY_RANK:
                rewardInfo['lastWeekRank'] = lastWeekRankInfo[1] if len(lastWeekRankInfo) > 1 else 0
                lastWeekVal = lastWeekRankInfo[2] if len(lastWeekRankInfo) > 2 and lastWeekRankInfo[2] else 0
                rewardInfo['point'] = gameStrings.RANKINGV2_LAST_WEEK_RENQI + str(lastWeekVal[0] if type(lastWeekVal) is tuple else 0)
            else:
                rewardInfo['point'] = ''
            rewardInfo['time'] = rankCommonUtils._getDeadlineTime()
            self.mediator.Invoke('refreshShejiaoView', (GfxValue(iType), ret, uiUtils.dict2GfxDict(rewardInfo, True)))
            self.refreshUpdateBtnState()

    def onGetAwardInfo(self, *arg):
        ret = self._createAwardInfo()
        return uiUtils.array2GfxAarry(ret, True)

    def _createAwardInfo(self):
        if self._awardInfoFunc:
            return self._awardInfoFunc()
        if self.awardType == gametypes.TOP_TYPE_GROUP_FB_RANK or self.awardType == gametypes.TOP_TYPE_GROUP_ZHENYAO_RANK:
            return self._createRwardInfo(self.awardType, self.awardStype)
        topType = self.topTypeDict.get(self.awardType, 0)
        awardInfo = self._getRewardInfo(topType, self.awardStype)
        lastRank = awardInfo[1]
        awardBtnEnabled = not awardInfo[3] if lastRank > 0 else False
        if self.awardType == gametypes.TOP_TYPE_FB:
            awardBtnEnabled = not awardInfo[3] and self._getFbMaxRewardRank(self.awardStype) >= lastRank if lastRank > 0 else False
        awardItems = []
        title, items = self.getTopAward()
        for item in items:
            iconPath = uiUtils.getItemIconFile64(item[0])
            color = uiUtils.getItemColor(item[0])
            awardItems.append([iconPath,
             item[1],
             color,
             item[0],
             uiUtils.getGfxItemById(item[0]),
             item[1]])

        titleStr = TD.data.get(title, {}).get('name', '')
        if titleStr:
            titleStr = gameStrings.TEXT_RANKINGPROXY_1399 % titleStr
        awardList = []
        if self.awardType == gametypes.TOP_TYPE_FB:
            tData = TRD.data.get((self.awardType, self.awardStype, 0), {})
        elif self.awardType == gametypes.TOP_TYPE_ENDLESS_CHALLENGE:
            fbNo = self.awardStype + self.huanjingCurSeason
            tData = TRD.data.get((self.awardType, fbNo, 0), {})
        elif self.awardType == gametypes.TOP_TYPE_GUILD_FISH_ACTIVITY:
            tData = GTRD.data.get((self.awardType, self.awardStype, 0), {})
        elif self.awardType == gametypes.TOP_TYPE_GUILD_MONSTER_CLAN_WAR:
            tData = GTRD.data.get((self.awardType, self.awardStype, 0), {})
        elif self.awardType == gametypes.TOP_TYPE_GUILD_YMF:
            tData = GTRD.data.get((self.awardType, self.awardStype, 0), {})
        else:
            tData = TRD.data.get((self.awardType, self.awardStype, 0), {})
        for td in tData:
            desc = td.get('desc', '')
            title = TD.data.get(td.get('title', 0), {}).get('name', '')
            if self.awardType == gametypes.TOP_TYPE_ENDLESS_CHALLENGE:
                mailTempId = td.get('mailTemplateId', 0)
                bonusId = MTD.data.get(mailTempId, {}).get('bonusId', 0)
            else:
                bonusId = td.get('bonusId', 0)
            p = BigWorld.player()
            if 'schoolTitles' in td:
                schoolTitles = td.get('schoolTitles')
                if p.school in schoolTitles:
                    title = TD.data.get(schoolTitles[p.school], {}).get('name', '')
            if 'schoolBonusIds' in td:
                schoolBonusIds = td.get('schoolBonusIds')
                if p.school in schoolBonusIds:
                    bonusId = schoolBonusIds[p.school]
            items = clientUtils.genItemBonus(bonusId)
            if self.awardType == gametypes.TOP_TYPE_GUILD_FISH_ACTIVITY:
                items = td.get('showBonus', ())
            elif self.awardType == gametypes.TOP_TYPE_GUILD_MONSTER_CLAN_WAR:
                items = td.get('showBonus', ())
            elif self.awardType == gametypes.TOP_TYPE_GUILD_YMF:
                items = td.get('showBonus', ())
            if not items:
                items = ()
            itemList = []
            for item in items:
                iconPath = uiUtils.getItemIconFile64(item[0])
                color = uiUtils.getItemColor(item[0])
                itemList.append([iconPath,
                 item[1],
                 color,
                 item[0],
                 uiUtils.getGfxItemById(item[0], item[1])])

            awardList.append([desc, title, itemList])

        cash = BigWorld.player().cash
        desc = ''
        ret = [lastRank,
         awardBtnEnabled,
         awardItems,
         titleStr,
         awardList,
         cash,
         self.awardType,
         desc]
        return ret

    def getTopAward(self):
        if self.awardType == None or self.awardStype == None:
            return (0, [])
        else:
            if self.awardType == gametypes.TOP_TYPE_FB:
                if TRD.data.has_key((self.awardType, self.awardStype, BigWorld.player().realSchool)):
                    tData = TRD.data[self.awardType, self.awardStype, BigWorld.player().realSchool]
                else:
                    tData = TRD.data.get((self.awardType, self.awardStype, 0), {})
            elif self.awardType == gametypes.TOP_TYPE_GUILD_FISH_ACTIVITY:
                tData = GTRD.data.get((self.awardType, self.awardStype, 0), {})
            elif self.awardType == gametypes.TOP_TYPE_GUILD_MONSTER_CLAN_WAR:
                tData = GTRD.data.get((self.awardType, self.awardStype, 0), {})
            elif self.awardType == gametypes.TOP_TYPE_GUILD_YMF:
                tData = GTRD.data.get((self.awardType, self.awardStype, 0), {})
            else:
                tData = TRD.data.get((self.awardType, self.awardStype, 0), {})
            topType = self.topTypeDict.get(self.awardType, 0)
            awardInfo = self._getRewardInfo(topType, self.awardStype)
            rank = awardInfo[1]
            value = awardInfo[2]
            for td in tData:
                minRank, maxRank = td['rankRange']
                if not minRank <= rank <= maxRank:
                    continue
                if td.has_key('limitVal') and value < td['limitVal']:
                    continue
                title = td.get('title', 0)
                bonusId = td.get('bonusId', 0)
                p = BigWorld.player()
                if 'schoolTitles' in td:
                    schoolTitles = td.get('schoolTitles')
                    if p.school in schoolTitles:
                        title = schoolTitles[p.school]
                if 'schoolBonusIds' in td:
                    schoolBonusIds = td.get('schoolBonusIds')
                    if p.school in schoolBonusIds:
                        bonusId = schoolBonusIds[p.school]
                items = clientUtils.genItemBonus(bonusId)
                if self.awardType == gametypes.TOP_TYPE_GUILD_FISH_ACTIVITY:
                    items = td.get('showBonus', ())
                if not items:
                    items = ()
                return (title, items)

            return (0, [])

    def closeAwardPanel(self):
        if self.rewardMed is None:
            return
        else:
            widget = ASObject(self.rewardMed).getWidget()
            if not widget or not hasattr(widget, 'widgetId'):
                return
            widgetId = widget.widgetId
            self.rewardMed = None
            self.awardType = None
            self.awardStype = None
            self.lvInterval = ()
            gameglobal.rds.ui.unLoadWidget(widgetId)
            return

    def onCloseRankAward(self, *arg):
        self.closeAwardPanel()

    def onGetTopReward(self, *arg):
        if self.awardType == gametypes.TOP_TYPE_FB:
            BigWorld.player().cell.getTopReward(self.awardType, self.awardStype)
        else:
            BigWorld.player().cell.getTopReward(self.awardType, self.awardStype)

    def refreshAwardPanel(self):
        ret = self._createAwardInfo()
        if self.rewardMed != None:
            self.rewardMed.Invoke('setAwardInfo', uiUtils.array2GfxAarry(ret, True))

    def onSetCurSchool(self, *arg):
        self.curSchool = int(arg[3][0].GetNumber())

    def _getFbMaxRewardRank(self, fbNo):
        p = BigWorld.player()
        tData = TRD.data.get((gametypes.TOP_TYPE_FB, fbNo, p.school), TRD.data.get((gametypes.TOP_TYPE_FB, fbNo, 0)))
        return max((td['rankRange'][1] for td in tData))

    def onEnableGuibaoRank(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableAppearanceRank', False))

    def onEnableApprenticeValRank(self, *arg):
        return GfxValue(BigWorld.player().enableNewApprentice())

    def onEnableGuildKindnessRank(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableGuildKindness', False))

    def onEnablePersonalZone(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enablePersonalZone', False))

    def onEnableGuildRobberRank(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableGuildRobber', False))

    def onEnableHomeWealthRank(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableHome', False) and gameglobal.rds.configData.get('enableRankingHomeWealth', False))

    def onEnableGuildFishingRank(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableGuildFishActivity', False))

    def onEnableGuildBaiFengYanRank(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableGuildChickenMeal', False))

    def onEnableMonsterClanWarRank(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableGuildMonsterClanWar', False))

    def onEnableGuildPrestigeRank(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableGuildPrestigeTopRank', False))

    def onEnableGuildMatchOptimize(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableGuildMatchOptimize', False))

    def onEnableGuildLady(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableGuildLady', False))

    def onEnableHuanjing(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableEndlessChallenge', False))

    def onRequestHuanjing(self, *args):
        p = BigWorld.player()
        rankType = args[3][0].GetNumber()
        lvKey = args[3][1].GetString()
        self.proxyId = rankType
        if lvKey == '':
            lvKey = self._getPlayerTopRankKey()
        school = int(args[3][2].GetNumber())
        if self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE:
            cacheData = self.huanjingCurInfo.get(lvKey, {})
            self.refreshHuanjingView(cacheData.get('info', []))
            self.refreshLvSelected(lvKey)
            p.base.getTopEndlessChallenge(cacheData.get('ver', 0), lvKey)
        elif self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE_HERO:
            info = self.huanjingHeroInfo.get(lvKey, {}).get(school, {})
            gamelog.debug('ypc@ self.huanjingHeroInfo = ', self.huanjingHeroInfo)
            self.refreshHuanjingView(info)
            if school not in self.huanjingHeroInfo.get(lvKey, {}):
                p.base.queryHistoryEndlessTopInfo(lvKey, school)
        elif self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND:
            self.refreshHuanjingView(self.huanjingFriendInfo.get(lvKey, {}))
            BigWorld.player().base.getFriendEndlessChallengeTopRank(lvKey)

    def updateHuanjingData(self, info):
        lvKey = info.get('lvKey')
        dataInfo = info.get('info')
        if self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE:
            self.huanjingCurSeason = info.get('season')
            self.huanjingSortData(dataInfo)
            self.huanjingCurInfo[lvKey] = {}
            self.huanjingCurInfo[lvKey]['ver'] = info.get('ver')
            self.huanjingCurInfo[lvKey]['info'] = dataInfo
            self.refreshHuanjingView(dataInfo)
        if self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE_HERO:
            school = info.get('school')
            self.huanjingHeroInfo = {}
            lvData = self.huanjingHeroInfo.setdefault(lvKey, {})
            for s, schoolInfo in dataInfo.iteritems():
                self.huanjingSortData(schoolInfo)
                lvData[s] = schoolInfo

            self.refreshHuanjingView(dataInfo.get(school, []))
        if self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND:
            self.huanjingSortData(dataInfo)
            self.huanjingFriendInfo[lvKey] = dataInfo
            self.refreshHuanjingView(dataInfo)
        self.refreshLvSelected(lvKey)

    def refreshHuanjingView(self, info):
        if not self.mediator:
            return
        if self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE:
            ret = self._generateData(const.PROXY_KEY_ENDLESS_CHALLENGE, info)
            otherInfo = {}
            otherInfo['time'] = ECSLD.data.get(self.huanjingCurSeason, {}).get('stopDate', rankCommonUtils._getDeadlineTime())
            self.mediator.Invoke('refreshHuanjingView', (ret, uiUtils.dict2GfxDict(otherInfo, True)))
        elif self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND:
            ret = self._generateData(const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND, info)
            self.mediator.Invoke('refreshHuanjingView', ret)
        elif self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE_HERO:
            ret = {}
            ret['rankType'] = self.proxyId
            ret['list'] = []
            ret['myRank'] = 0
            myName = BigWorld.player().realRoleName
            for data in info:
                obj = {}
                obj['desc'] = data['desc']
                topInfo = data['topData']
                for i, item in enumerate(topInfo):
                    obj[i] = {}
                    obj[i]['index'] = item[0]
                    obj[i]['roleName'] = item[1]
                    isSelf = myName == item[1]
                    obj[i]['finishTime'] = utils.formatTimeStr(item[2], 'h:m:s', True, 2, 2, 2)
                    obj[i]['val'] = item[3]
                    obj[i]['isSelf'] = isSelf

                ret['list'].append(obj)

            self.mediator.Invoke('refreshHuanjingView', uiUtils.dict2GfxDict(ret, True))
            self.refreshUpdateBtnState()

    def huanjingSortData(self, info):
        if self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE:
            info.sort(reverse=True, key=lambda k: (k[-1][0], k[-1][1], k[-1][2]))
        if self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE_HERO:
            for i in info:
                i['topData'].sort(key=lambda k: k[0])

            info.sort(key=lambda k: k['season'])
        if self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND:
            info.sort(reverse=True, key=lambda k: (k[0], k[1], k[2]))

    def onUpdateHuanjingRank(self, *args):
        if self.huanjingUpdateTimer == None:
            p = BigWorld.player()
            lvKey = args[3][1].GetString()
            school = int(args[3][2].GetNumber())
            if self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE:
                lvKeyVer = self.huanjingCurInfo.get(lvKey, {}).get('ver', 0)
                p.base.getTopEndlessChallenge(lvKeyVer, lvKey)
            elif self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE_HERO:
                p.base.queryHistoryEndlessTopInfo(lvKey, school)
            elif self.proxyId == const.PROXY_KEY_ENDLESS_CHALLENGE_FRIEND:
                p.base.getFriendEndlessChallengeTopRank(lvKey)

    def onInitHuanjingCurseasonFbdata(self, *args):
        ret = {}
        fbData = SCD.data.get('endlessChallengeRankInfo', {})
        for k, v in fbData.items():
            ret[k] = {'season': v.get('fbNo', 0) * 1000,
             'week': v.get('fbNo', 0) * 1000 + 900}

        ret['descText'] = SCD.data.get('rankHuanjingDescText', '')
        return uiUtils.dict2GfxDict(ret, True)

    def setTab(self, tabId):
        self.tabId = tabId
        self.mediator.Invoke('setTabIndex', GfxValue(tabId))

    def onRequestSprite(self, *args):
        self.requestSpriteData(args[3][0].GetString())

    def requestSpriteData(self, lvKey):
        lvKey = self.getServerLvKey(lvKey)
        self.proxyId = const.PROXY_KEY_TOP_SPRITE_COMBAT_SCORE
        ver = self.spriteInfo.get(lvKey, {}).get('ver', 0)
        self.updateSpriteData(lvKey, ver, self.spriteInfo.get(lvKey, {}).get('info', []))
        BigWorld.player().base.getTopSpriteCombatScore(ver, lvKey)

    def updateSpriteData(self, lvKey, ver, info):
        self.spriteInfo[lvKey] = {'ver': ver,
         'info': info}
        self.refreshSpriteView(info)

    def refreshSpriteView(self, info):
        if self.mediator:
            ret = self._generateData(const.PROXY_KEY_TOP_SPRITE_COMBAT_SCORE, info)
            ret.SetMember('time', GfxValue(gbk2unicode(rankCommonUtils._getDeadlineTime())))
            self.mediator.Invoke('refreshSpriteView', ret)
            self.refreshUpdateBtnState()

    def getSpriteTipDataByUUID(self, spriteUUID):
        detailInfo = self.spriteDetailInfo.get(spriteUUID)
        if detailInfo is None:
            gamelog.debug("@ljh can\'t find sprite detail info by spriteUUID: %s" % spriteUUID)
            return {}
        else:
            info = {}
            info['spriteId'] = detailInfo[5]
            extraData = detailInfo[10]
            info['bindType'] = extraData[const.SPRITE_DICT_INDEX_bindType]
            info['skills'] = {'naturals': extraData[const.SPRITE_DICT_INDEX_naturals],
             'bonus': extraData[const.SPRITE_DICT_INDEX_bonus]}
            info['name'] = detailInfo[6]
            info['props'] = {'lv': detailInfo[7],
             'famiEffLv': extraData[const.SPRITE_DICT_INDEX_famiEffLv],
             'famiEffAdd': extraData[const.SPRITE_DICT_INDEX_famiEffAdd],
             'familiar': extraData[const.SPRITE_DICT_INDEX_famiEffLv] - extraData[const.SPRITE_DICT_INDEX_famiEffAdd]}
            return gameglobal.rds.ui.summonedWarSpriteMine.getSpriteTipByInfo(info)

    def getSpriteDetailTipDataByUUID(self, spriteUUID):
        detailInfo = self.spriteDetailInfo.get(spriteUUID)
        if detailInfo is None:
            gamelog.debug("@dxk can\'t find sprite detail info by spriteUUID: %s" % spriteUUID)
            return {}
        else:
            return gameglobal.rds.ui.summonedWarSprite.getSpriteDetailTipData(detailInfo, True, rtype='rank')

    def getServerLvKey(self, clientLvKey):
        if clientLvKey != gametypes.ALL_LV_TOP_RANK_KEY:
            clientLvKey += str('_' + str(0))
        return clientLvKey

    def relayoutTabButtons(self):
        self.asMediator = ASObject(self.mediator)
        self.asWidget = self.asMediator.getWidget()
        self.asWidget.teamBtn.visible = False
        hideCount = 0
        if not gameglobal.rds.configData.get('enableEndlessChallenge', False):
            self.asWidget.huanjingBtn.visible = False
            hideCount += 1
        if not (gameglobal.rds.configData.get('enableHaoqiVal', True) and gameglobal.rds.configData.get('enableRenpinVal', True)):
            self.asWidget.shejiaoBtn.visible = False
            hideCount += 1
        tabBtnWidth = self.asWidget.famerBtn.width + 2
        nextX = self.asWidget.famerBtn.x + tabBtnWidth / 2 * hideCount
        firstClassTabButtons = ['famerBtn',
         'roleBtn',
         'huanjingBtn',
         'fubenBtn',
         'guildBtn',
         'shejiaoBtn']
        for btnName in firstClassTabButtons:
            btn = self.asWidget.__getattr__(btnName)
            if btn.visible:
                btn.x = nextX
                nextX += tabBtnWidth

    def startUpdateBtnCooldownTimer(self):
        self.updateBtnCooldownTimeDic[self.proxyId] = 61
        BigWorld.callback(0, Functor(self.__updateBtnTimerCallback, self.proxyId))

    def __updateBtnTimerCallback(self, *args):
        proxyId = args[0]
        self.updateBtnCooldownTimeDic[proxyId] -= 1
        if self.updateBtnCooldownTimeDic[proxyId] > 0:
            BigWorld.callback(1, Functor(self.__updateBtnTimerCallback, proxyId))
        if self.proxyId == proxyId:
            self.setUpdateBtnState(self.updateBtnCooldownTimeDic[proxyId])

    def refreshUpdateBtnState(self):
        self.setUpdateBtnState(self.updateBtnCooldownTimeDic.get(self.proxyId, 0))

    def setUpdateBtnState(self, cooldownTime):
        currentView = self.asMediator.getCurrentView()
        if not currentView:
            return
        else:
            updateBtn = currentView.updateBtn
            if updateBtn is None:
                return
            updateBtn.enabled = cooldownTime == 0
            if cooldownTime > 0:
                updateBtn.label = gameStrings.REFRESH_BTN_LABEL_CD % cooldownTime
            else:
                updateBtn.label = gameStrings.REFRESH_BTN_LABEL
            return

    def handleUpdateBtnClick(self, *args):
        self.startUpdateBtnCooldownTimer()

    def onShowSpriteDetailTip(self, *args):
        spriteUUID = args[3][0].GetString()
        detailInfo = self.spriteDetailInfo.get(spriteUUID)
        if detailInfo:
            spriteTip = TipManager.getTargetTip()
            if spriteTip:
                gameglobal.rds.ui.summonedWarSprite.showSpriteDetailTip(detailInfo[10], 'rank', spriteTip.x, spriteTip.y)
            else:
                gameglobal.rds.ui.summonedWarSprite.showSpriteDetailTip(detailInfo[10], 'rank')

    def onRequestCommonRank(self, *args):
        p = BigWorld.player()
        topId = args[3][0].GetNumber()
        lvKey = args[3][1].GetString()
        print 'jbx:lvKey', lvKey
        schoolId = args[3][2].GetNumber()
        dropDownKey = args[3][3].GetNumber()
        config = self.commonRankConfig.get(topId, {})
        key, serverKey = rankCommonUtils.genCacheKeyAndServerKey(config, lvKey, schoolId, dropDownKey)
        if key not in self.commonRankInfo:
            self.commonRankInfo[key] = {}
        elif 'cache' in self.commonRankInfo[key]:
            cacheData = self.commonRankInfo[key]['cache']
            gamelog.debug('ypc@ cacheData ', cacheData)
            if cacheData.get('playerGbId', 0) and cacheData.get('playerGbId', 0) != p.gbId:
                self.commonRankInfo[key] = {}
            elif self.mediator:
                self.mediator.Invoke('refreshCommonRankView', uiUtils.dict2GfxDict(cacheData, True))
        else:
            gamelog.debug('ypc@ RequestCommonRank self.commonRankInfo[key]', self.commonRankInfo[key])
        ver = self.commonRankInfo[key].get('ver', 0)
        p.base.queryTopUniversal(topId, ver, serverKey)
        gamelog.debug('ypc@ RequestCommonRank ', topId, ver, lvKey, schoolId, key, serverKey, dropDownKey)

    def updateCommnonRankData(self, data):
        gamelog.debug('ypc@ server data = ', data)
        ret = {}
        if gametypes.TOP_UNIVERSAL_TOP_ID not in data:
            return
        topId = data[gametypes.TOP_UNIVERSAL_TOP_ID]
        if topId in self.commonRankConfig:
            serverKey = data.get(gametypes.TOP_UNIVERSAL_KEY, '')
            cachekey = rankCommonUtils.getRankCommonCacheKey(topId, serverKey)
            ver = data.get(gametypes.TOP_UNIVERSAL_VERSION, 0)
            myInfo = data.get(gametypes.TOP_UNIVERSAL_MY_INFO, {})
            datalist = data.get(gametypes.TOP_UNIVERSAL_DATA_LIST, [])
            sortRule = data.get(gametypes.TOP_UNIVERSAL_SORT, ())
            config = copy.copy(self.commonRankConfig.get(topId, {}))
            rankCommonUtils.setRankCommonExtraInfo(config, topId, serverKey)
            gamelog.debug('ypc@ updateCommnonRankData config = ', config)
            if topId == gametypes.TOP_TYPE_CARD_COMBAT_SCORE:
                if sortRule:
                    datalist = rankCommonUtils._getSortedCommonRankData(datalist, sortRule)
                    sortRule = False
                index = 1
                for data in datalist:
                    tmpData = data.get(gametypes.TOP_UNIVERSAL_CARD_COMBAT_SCORE, ())
                    gbId = data.get(gametypes.TOP_UNIVERSAL_GBID, ())
                    cardScore, topName, cardZipData = tmpData
                    cardData = cPickle.loads(zlib.decompress(cardZipData))
                    data[gametypes.TOP_UNIVERSAL_CARD_COMBAT_SCORE] = int(cardScore)
                    self.cardExtraInfo[str(gbId)] = cardData
                    index += 1

            ret = rankCommonUtils.getRankDataByConfig(config, datalist, myInfo, sortRule, serverKey)
            self.commonRankInfo[cachekey] = {}
            self.commonRankInfo[cachekey]['ver'] = ver
            self.commonRankInfo[cachekey]['cache'] = ret
            if self.mediator:
                self.mediator.Invoke('refreshCommonRankView', uiUtils.dict2GfxDict(ret, True))
            gamelog.debug('ypc@ RequestCommonRank ', topId, ver, cachekey, serverKey)
        elif topId in RCD.data:
            gameglobal.rds.ui.rankCommon.updateCommnonRankData(data)
        gameglobal.rds.ui.npcRelationshipXindong.updateRankData(data)

    def isCommonRank(self, topId):
        for x in self.commonRankConfig.values():
            if topId == x['TopId']:
                return True

        return False

    def commonRankSort(self, info):
        info.sort(key=lambda k: k[3])

    def showCommonAward(self, *args):
        topId = args[3][0].GetNumber()
        key = args[3][1].GetString()
        lvKey = args[3][2].GetString()
        schoolId = args[3][3].GetNumber()
        dropdownIdx = args[3][4].GetNumber()
        if topId == gametypes.TOP_TYPE_GUILD_BOSS_FOR_ELITE:
            gameglobal.rds.ui.rankingAwardPreview.show()
            return
        if topId == gametypes.TOP_TYPE_TEAM_ENDLESS:
            if key == 'Rewardname1Info':
                gameglobal.rds.ui.rankCommon.hide()
                gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_FRIEND_TEAM_ENDLESS, customDropdownKey=voidLunHuiHelper.getInstance().getRankDropDownKey())
            else:
                lvIdx = int(lvKey.split('_')[-1])
                awardKey = (gametypes.TOP_TYPE_TEAM_ENDLESS, lvIdx, 0)
                rewards = rankCommonUtils.getCommonAwardInfo(awardKey)
                gamelog.debug('ypc@rewards = ', rewards)
                gameglobal.rds.ui.rankingAwardCommon.showAwardCommon(rewards)
            return
        if topId == gametypes.TOP_TYPE_SPRITE_CHALLENGE:
            if key == 'Rewardname1Info':
                gameglobal.rds.ui.rankCommon.hide()
                gameglobal.rds.ui.rankCommon.showRankCommon(gametypes.TOP_TYPE_SPRITE_CHALLENGE_FRIEND)
            else:
                gameglobal.rds.ui.spriteChallengeReward.show()
            return
        awardKey = RV2CD.data.get(topId, {}).get(key, ())
        rewards = rankCommonUtils.getCommonAwardInfo(awardKey)
        gamelog.debug('ypc@rewards = ', rewards)
        gameglobal.rds.ui.rankingAwardCommon.showAwardCommon(rewards)

    def initCommonRankConfig(self):
        self.commonRankConfig = {}
        for topId in RV2CD.data:
            if topId == gametypes.TOP_TYPE_TEAM_ENDLESS:
                if not gameglobal.rds.configData.get('enableTeamEndless', False):
                    continue
            if topId == gametypes.TOP_TYPE_SPRITE_CHALLENGE:
                if not gameglobal.rds.configData.get('enableSpriteChallenge', False):
                    continue
            data = copy.deepcopy(RV2CD.data.get(topId))
            self.commonRankConfig[topId] = data

        for rankCfg in self.commonRankConfig.values():
            allColData = []
            for cfgIndex in rankCfg.get('GeneralColConfigs', []):
                realIndex = cfgIndex
                if type(cfgIndex) is tuple:
                    realIndex = cfgIndex[0]
                colCfg = RCFD.data.get(realIndex, {})
                if not colCfg.get('isHide', False):
                    name = colCfg.get('name', '')
                    width = colCfg.get('Width', 0)
                    dataIndex = colCfg.get('ServerIndex', 0)
                    allColData.append({'Name': name,
                     'Width': width,
                     'DataIndex': dataIndex,
                     'ConfigIndex': cfgIndex})

            rankCfg['AllColData'] = allColData
            if 'customDropdown' in rankCfg:
                dropdownData = []
                for label, ddData in rankCfg.get('customDropdown', ()):
                    dropdownData.append({'label': label,
                     'ddData': ddData})

                rankCfg['commDropdown'] = dropdownData

    def getCardSuitTipData(self, index):
        cardData = self.cardExtraInfo.get(index, {})
        data = self.uiAdapter.cardSystem.getCardSuitTipData(cardData)
        return uiUtils.dict2GfxDict(data, True)

    def getDefaultDropdownIdx(self, *args):
        topId = int(args[3][0].GetNumber())
        if topId == gametypes.TOP_TYPE_TEAM_ENDLESS:
            dropDownKey = voidLunHuiHelper.getInstance().getRankDropDownKey()
            dropDownIdx = 0
            dropVal = RV2CD.data.get(topId, {}).get('customDropdown', ())
            for i, val in enumerate(dropVal):
                if dropDownKey in val:
                    dropDownIdx = i
                    break

            return GfxValue(dropDownIdx)
        return GfxValue(0)
