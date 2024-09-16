#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/rankProxy.o
import time
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import gamelog
import gametypes
import clientUtils
import formula
import utils
from guis import ui
from guis import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import uiUtils
from item import Item
from data import school_data as SD
from data import top_fb_data as TFD
from cdata import top_reward_data as TRD
from data import title_data as TD
from cdata import game_msg_def_data as GMDD
from cdata import fb_top_server_data as FTSD

class RankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RankProxy, self).__init__(uiAdapter)
        self.modelMap = {'getHuntBtnStatus': self.onGetHuntBtnStatus,
         'getRankInfo': self.onGetRankInfo,
         'closeRankList': self.onCloseRankList,
         'refreshRankInfo': self.onRefreshRankInfo,
         'getTab': self.onGetTab,
         'getFbData': self.onGetFbData,
         'getTopReward': self.onGetTopReward,
         'showAwardPanel': self.onShowAwardPanel,
         'closeRankAward': self.onCloseRankAward,
         'getAwardInfo': self.onGetAwardInfo,
         'getShowType': self.onGetShowType,
         'getDetailText': self.onGetDetailText,
         'clickRankLv': self.onClickRankLv,
         'getPlayerSchool': self.onGetPlayerSchool,
         'getDefaultFubenId': self.onGetDefaultFubenId,
         'getFightAwardInfo': self.onGetFightAwardInfo,
         'showFightAward': self.onShowFightAward,
         'closeFightAward': self.onCloseFightAward,
         'setCurSchool': self.onSetCurSchool}
        self.schoolList = SD.data.keys()
        self.mediator = None
        self.awardMediator = None
        self.lvVer = 0
        self.moneyVer = {}
        self.fubenVer = {}
        self.fubenIgnoreTime = dict(zip([ self._getFbNo(x) for x in TFD.data.keys() ], [ TFD.data.get(x, {}).get('ignoreTime', 0) for x in TFD.data.keys() ]))
        self.arenaVer = {}
        self.crossArenaVer = {}
        self.equipVer = {}
        self.achPointsVer = {}
        self.clanWarVer = 0
        self.socialLvVer = {}
        self.prosperityVer = 0
        self.matchVer = 0
        self.huntVer = 0
        self.lvInfo = []
        self.moneyInfo = {}
        self.lastWeekMoneyRankInfo = ()
        self.lastWeekFubenRankInfo = {}
        self.lastWeekGuildProsperityRankInfo = ()
        self.lastWeekGuildMatchRankInfo = ()
        self.lastWeekGuildHuntRankInfo = ()
        self.lastWeekCombatRankInfo = ()
        self.fubenInfo = None
        self.arenaInfo = {}
        self.crossArenaInfo = {}
        self.equipInfo = {}
        self.achPointsInfo = {}
        self.clanWarInfo = []
        self.socialLvInfo = {}
        self.prosperityInfo = []
        self.matchInfo = []
        self.huntInfo = []
        self.lvKey = '1_59'
        self.fightRankInfo = {}
        self.fightRankVer = {}
        self.isShow = False
        self.tab = 0
        self.proxyId = 0
        self.fbIdx = 0
        self.fbNo = 0
        self.awardType = None
        self.awardStype = None
        self.showType = uiConst.RANK_TYPE_OTHER
        self.mySchool = 0
        self.curSchool = 0
        self.selectedSchool = 0
        self.fightAwardData = []
        self.fubenId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANK_LIST, self.closeRankList)
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANK_AWARD, self.closeAwardPanel)
        uiAdapter.registerEscFunc(uiConst.WIDGET_FIGHTAWARD_LIST, self.closeFightAward)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RANK_LIST:
            self.mediator = mediator
        elif widgetId == uiConst.WIDGET_RANK_AWARD:
            self.awardMediator = mediator

    def initFubenInfo(self):
        if self.fubenInfo == None:
            self.fubenInfo = {}
            for x in TFD.data:
                fbNo = TFD.data.get(x, {}).get('fbNo', 0)
                key = '%d' % fbNo
                self.fubenInfo[key] = []
                self.fubenVer[key] = 0
                for idx in SD.data:
                    key = '%d_%d' % (fbNo, idx)
                    self.fubenInfo[key] = []
                    self.fubenVer[key] = 0

    def onGetHuntBtnStatus(self, *arg):
        return GfxValue(gameglobal.rds.configData.get('enableGuildActivityHunt', False))

    def onGetFbData(self, *arg):
        fbNames = []
        fbData = TFD.data
        fbServerData = FTSD.data
        for idx in fbData:
            fbNo = fbData.get(idx, {}).get('fbNo', 0)
            reward = fbData.get(idx, {}).get('reward', 0)
            showCategory = fbServerData.get(fbNo, {}).get('isByClass', 0)
            limitMax = fbServerData.get(fbNo, {}).get('limitLvMax', 0)
            if limitMax != 0:
                lvMax = uiUtils.getTextFromGMD(GMDD.data.CRAZYMODE_ITEM_NEED_TIP, '%d等级以上玩家成绩不计入该排行榜') % limitMax
            else:
                lvMax = ''
            fbNames.append([idx,
             fbNo,
             reward,
             showCategory,
             lvMax])

        fbNames.sort()
        gamelog.debug('zt: onGetFbData', fbNames)
        ar = self.movie.CreateArray()
        for idx, fbName in enumerate(fbNames):
            obj = self.movie.CreateObject()
            detailName = formula.getFbDetailName(fbName[1])
            obj.SetMember('id', GfxValue(fbName[0]))
            obj.SetMember('name', GfxValue(gbk2unicode(detailName)))
            obj.SetMember('reward', GfxValue(fbName[2]))
            obj.SetMember('showCategory', GfxValue(fbName[3]))
            obj.SetMember('lvMax', GfxValue(gbk2unicode(fbName[4])))
            obj.SetMember('fbNo', GfxValue(fbName[1]))
            ar.SetElement(idx, obj)

        return ar

    def getPlayerTopRankKey(self):
        p = BigWorld.player()
        if 1 <= p.lv <= 59:
            return '1_59'
        if 60 <= p.lv <= 69:
            return '60_69'
        if 70 <= p.lv <= 79:
            return '70_79'
        return '1_59'

    @ui.callInCD(1)
    def onClickRankLv(self, *arg):
        lvKey = arg[3][0].GetString()
        self.setRankListData(self.tab, lvKey)

    @ui.callInCD(1)
    def onGetRankInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        self.tab = idx
        if idx == 3:
            self.initFubenInfo()
            self.fbNo = int(arg[3][1].GetNumber())
            self.selectedSchool = int(arg[3][2].GetNumber())
        lvKey = self.getPlayerTopRankKey()
        self.setRankListData(idx, lvKey)

    def setRankListData(self, idx, lvKey):
        p = BigWorld.player()
        if idx == 0:
            self.proxyId = const.PROXY_KEY_TOP_EQUIP_SCORE
            if self.equipInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_EQUIP_SCORE, self.equipVer[lvKey], self.equipInfo[lvKey], lvKeyStr=lvKey)
            p.base.getTopEquipScore(self.equipVer.get(lvKey, 0), lvKey)
        elif idx == 1:
            self.proxyId = const.PROXY_KEY_TOP_LEVEL
            if self.lvInfo != None:
                self.setRankList(const.PROXY_KEY_TOP_LEVEL, self.lvVer, self.lvInfo)
            p.base.getTopLevel(self.lvVer)
        elif idx == 2:
            self.proxyId = const.PROXY_KEY_TOP_ARENA_SCORE
            if self.arenaInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_ARENA_SCORE, self.arenaVer[lvKey], self.arenaInfo[lvKey], lvKeyStr=lvKey)
            p.base.getTopArenaScoreTimer(self.arenaVer.get(lvKey, 0), lvKey)
        elif idx == 3:
            self.proxyId = const.PROXY_KEY_TOP_FB_TIME
            fbNo = self.fbNo
            if fbNo != -1:
                if self.selectedSchool == 0:
                    key = '%d' % fbNo
                else:
                    key = '%d_%d' % (fbNo, self.selectedSchool)
                if self.fubenInfo.has_key(key) and self.fubenInfo[key] != None:
                    lastWeekRankInfo = () if fbNo not in self.lastWeekFubenRankInfo else self.lastWeekFubenRankInfo[fbNo]
                    self.setRankList(const.PROXY_KEY_TOP_FB_TIME, self.fubenVer[key], self.fubenInfo[key], lastWeekRankInfo, fbNo, key)
                if self.fubenVer.has_key(key) and self.fubenVer[key]:
                    fubenVer = self.fubenVer[key]
                else:
                    fubenVer = 0
                p.base.getTopFbTimes(fubenVer, fbNo, key)
        elif idx == 4:
            self.proxyId = const.PROXY_KEY_TOP_ACHIEVE_POINTS
            if self.achPointsInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_ACHIEVE_POINTS, self.achPointsVer[lvKey], self.achPointsInfo[lvKey], lvKeyStr=lvKey)
            p.base.getTopAchievePoints(self.achPointsVer.get(lvKey, 0), lvKey)
        elif idx == 5:
            self.proxyId = const.PROXY_KEY_TOP_MONEY
            if self.moneyInfo.has_key(lvKey) and self.lastWeekMoneyRankInfo:
                self.setRankList(const.PROXY_KEY_TOP_MONEY, self.moneyVer[lvKey], self.moneyInfo[lvKey], self.lastWeekMoneyRankInfo, lvKeyStr=lvKey)
            p.base.getTopMoney(self.moneyVer.get(lvKey, 0), lvKey)
        elif idx == 6:
            self.proxyId = const.PROXY_KEY_TOP_CLAN_WAR_SCORE
            if self.clanWarInfo != None:
                self.setRankList(const.PROXY_KEY_TOP_CLAN_WAR_SCORE, self.clanWarVer, self.clanWarInfo)
            p.base.getTopClanWarScore(self.clanWarVer)
        elif idx == 7:
            self.proxyId = const.PROXY_KEY_TOP_SOCAIL_LEVEL
            if self.socialLvInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_SOCAIL_LEVEL, self.socialLvVer[lvKey], self.socialLvInfo[lvKey], lvKeyStr=lvKey)
            p.base.getTopSocLevel(self.socialLvVer.get(lvKey, 0), lvKey)
        elif idx == 8:
            self.proxyId = const.PROXY_KEY_TOP_GUILD_PROSPERITY
            if self.prosperityInfo != None:
                self.setRankList(const.PROXY_KEY_TOP_GUILD_PROSPERITY, self.prosperityVer, self.prosperityInfo, self.lastWeekGuildProsperityRankInfo)
            p.cell.getTopGuildProsperity(self.prosperityVer)
        elif idx == 9:
            self.proxyId = const.PROXY_KEY_TOP_GUILD_MATCH
            if self.matchInfo != None:
                self.setRankList(const.PROXY_KEY_TOP_GUILD_MATCH, self.matchVer, self.matchInfo, self.lastWeekGuildMatchRankInfo)
            p.cell.getTopGuildMatch(self.matchVer)
        elif idx == 10:
            if lvKey != gametypes.ALL_LV_TOP_RANK_KEY:
                lvKey += str('_' + str(self.selectedSchool))
            p.base.getTopCombatScore(self.fightRankVer.get(lvKey, 0), lvKey)
            self.proxyId = const.PROXY_KEY_TOP_COMBAT_SCORE
            if self.fightRankInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_COMBAT_SCORE, self.fightRankVer[lvKey], self.fightRankInfo[lvKey], lvKeyStr=lvKey)
        elif idx == 11:
            self.proxyId = const.PROXY_KEY_TOP_GLOBAL_ARENA_SCORE
            if self.crossArenaInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_GLOBAL_ARENA_SCORE, self.crossArenaVer[lvKey], self.crossArenaInfo[lvKey], lvKeyStr=lvKey)
            p.base.getGlboalTopArenaScore(self.crossArenaVer.get(lvKey, 0), lvKey)
        elif idx == 12:
            self.proxyId = const.PROXY_KEY_TOP_GUILD_HUNT
            if self.huntInfo != None:
                self.setRankList(const.PROXY_KEY_TOP_GUILD_HUNT, self.huntVer, self.huntInfo, self.lastWeekGuildHuntRankInfo)
            p.cell.getTopGuildHunt(self.huntVer)

    def onCloseRankList(self, *arg):
        self.closeRankList()

    def openRankList(self, tab = 0, showType = uiConst.RANK_TYPE_OTHER, fubenId = 0):
        gamelog.debug('jinjj-------------', tab, showType)
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_RANK):
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANK_LIST)
        self.isShow = True
        self.tab = tab
        self.showType = showType
        self.fubenId = fubenId

    def closeRankList(self, quitNpcFunc = True):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RANK_LIST)
        self.isShow = False
        self.mediator = None
        self.showType = uiConst.RANK_TYPE_OTHER
        if quitNpcFunc and self.uiAdapter.funcNpc.isOnFuncState():
            self.uiAdapter.funcNpc.close()

    def getFbMaxRewardRank(self, fbNo):
        p = BigWorld.player()
        tData = TRD.data.get((gametypes.TOP_TYPE_FB, fbNo, p.school), TRD.data.get((gametypes.TOP_TYPE_FB, fbNo, 0)))
        return max((td['rankRange'][1] for td in tData))

    def setRankList(self, proxyID, ver, info, lastWeekRankInfo = (), fbNo = None, lvKeyStr = '1_59'):
        self.lvKey = lvKeyStr
        if proxyID == const.PROXY_KEY_TOP_MONEY:
            self.moneyVer[lvKeyStr] = ver
            if info and type(info[0][3]) == type(1):
                info = self.setTopMoneyTitle(info)
            self.moneyInfo[lvKeyStr] = info
            if lastWeekRankInfo:
                self.lastWeekMoneyRankInfo = lastWeekRankInfo
                rewardBtnEnabled = 0 if lastWeekRankInfo[3] else 1
            else:
                rewardBtnEnabled = 0
            self.setGetRewardBtnEnabled(rewardBtnEnabled)
        elif proxyID == const.PROXY_KEY_TOP_LEVEL:
            self.lvVer = ver
            self.lvInfo = info
        elif proxyID == const.PROXY_KEY_TOP_COMBAT_SCORE:
            self.fightRankVer[lvKeyStr] = ver
            self.fightRankInfo[lvKeyStr] = info
            if lastWeekRankInfo:
                self.lastWeekCombatRankInfo = lastWeekRankInfo
                rewardBtnEnabled = 0 if lastWeekRankInfo[3] else 1
            else:
                rewardBtnEnabled = 0
            self.setGetRewardBtnEnabled(rewardBtnEnabled)
        elif proxyID == const.PROXY_KEY_TOP_FB_TIME:
            if self.fubenInfo == None:
                self.initFubenInfo()
            self.fubenVer[lvKeyStr] = ver
            if info and type(info[0][3][1]) == type(1) and fbNo:
                info = self.setTopFbTime(fbNo, info)
            if fbNo:
                self.fubenInfo[lvKeyStr] = info
                self.lastWeekFubenRankInfo[fbNo] = lastWeekRankInfo
        elif proxyID == const.PROXY_KEY_TOP_EQUIP_SCORE:
            self.equipVer[lvKeyStr] = ver
            self.equipInfo[lvKeyStr] = info
        elif proxyID == const.PROXY_KEY_TOP_ACHIEVE_POINTS:
            self.achPointsVer[lvKeyStr] = ver
            self.achPointsInfo[lvKeyStr] = info
        elif proxyID == const.PROXY_KEY_TOP_ARENA_SCORE:
            self.arenaVer[lvKeyStr] = ver
            self.arenaInfo[lvKeyStr] = info
        elif proxyID == const.PROXY_KEY_TOP_GLOBAL_ARENA_SCORE:
            self.crossArenaVer[lvKeyStr] = ver
            self.crossArenaInfo[lvKeyStr] = info
        elif proxyID == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
            self.clanWarVer = ver
            self.clanWarInfo = info
        elif proxyID == const.PROXY_KEY_TOP_SOCAIL_LEVEL:
            self.socialLvVer[lvKeyStr] = ver
            self.socialLvInfo[lvKeyStr] = info
        elif proxyID == const.PROXY_KEY_TOP_GUILD_PROSPERITY:
            self.prosperityVer = ver
            self.prosperityInfo = info
            if lastWeekRankInfo:
                self.lastWeekGuildProsperityRankInfo = lastWeekRankInfo
                rewardBtnEnabled = 0 if lastWeekRankInfo[3] else 1
            else:
                rewardBtnEnabled = 0
            self.setGetRewardBtnEnabled(rewardBtnEnabled)
        elif proxyID == const.PROXY_KEY_TOP_GUILD_MATCH:
            self.matchVer = ver
            self.matchInfo = info
            if lastWeekRankInfo:
                self.lastWeekGuildMatchRankInfo = lastWeekRankInfo
                rewardBtnEnabled = 0 if lastWeekRankInfo[3] else 1
            else:
                rewardBtnEnabled = 0
            self.setGetRewardBtnEnabled(rewardBtnEnabled)
        elif proxyID == const.PROXY_KEY_TOP_GUILD_HUNT:
            self.huntVer = ver
            self.huntInfo = info
            if lastWeekRankInfo:
                self.lastWeekGuildHuntRankInfo = lastWeekRankInfo
                rewardBtnEnabled = 0 if lastWeekRankInfo[3] else 1
            else:
                rewardBtnEnabled = 0
            self.setGetRewardBtnEnabled(rewardBtnEnabled)
        if self.selectedSchool == 0:
            fbKey = '%d' % self.fbNo
        else:
            fbKey = '%d_%d' % (self.fbNo, self.selectedSchool)
        if self.proxyId != proxyID or proxyID == const.PROXY_KEY_TOP_FB_TIME and fbKey != lvKeyStr:
            return
        self._setRankList(proxyID, info)
        if lvKeyStr.count('_') == 2:
            self.setLvGroupSelected(lvKeyStr.rsplit('_', 1)[0])
        else:
            self.setLvGroupSelected(lvKeyStr)
        if proxyID != const.PROXY_KEY_TOP_MONEY:
            self.doSetRewardText('')
        else:
            self._setRewardText()

    def setLvGroupSelected(self, lvKey):
        if self.mediator:
            self.mediator.Invoke('setLvGroupSelected', GfxValue(lvKey))

    def setGetRewardBtnVisible(self, flag):
        if self.mediator:
            self.mediator.Invoke('setGetRewardBtnVisible', GfxValue(flag))

    def setGetRewardBtnEnabled(self, flag):
        if self.mediator:
            self.mediator.Invoke('setGetRewardBtnEnabled', GfxValue(flag))

    def _setRewardText(self):
        rewardText = ''
        if self.lastWeekMoneyRankInfo:
            hasReward, lastWeedRank, _, isRewarded = self.lastWeekMoneyRankInfo
            if hasReward == const.TOP_HAS_REWARD:
                if lastWeedRank != 0:
                    if isRewarded:
                        rewardText = '上周名次:%d, 奖励已领取' % (lastWeedRank,)
                    else:
                        rewardText = '上周名次:%d, 请领取奖励' % (lastWeedRank,)
                else:
                    rewardText = '未上榜'
            gamelog.debug('@hjx rank#_setRewardText:', hasReward, rewardText)
        self.doSetRewardText(rewardText)

    def doSetRewardText(self, rewardText):
        if self.mediator:
            self.mediator.Invoke('setRewardContent', GfxValue(gbk2unicode(str(rewardText))))

    def _setRankList(self, proxyID, info):
        ret = self.movie.CreateArray()
        pos = 0
        clanWarRank = 1
        for i, item in enumerate(info):
            ar = self.movie.CreateArray()
            if proxyID == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
                if i == 0:
                    clanWarRank = 1
                elif item[2][0] != info[i - 1][2][0]:
                    clanWarRank += 1
                index = clanWarRank
            else:
                index = i + 1
            roleName = item[1]
            if proxyID == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
                val = item[2][0]
                finishTime = item[2][2]
                school = item[2][1]
            elif proxyID == const.PROXY_KEY_TOP_GUILD_PROSPERITY:
                val = item[2]
                finishTime = item[1]
                school = item[3]
            elif proxyID == const.PROXY_KEY_TOP_GUILD_MATCH:
                val = item[2]
                finishTime = item[1]
                school = item[3]
            elif proxyID == const.PROXY_KEY_TOP_GUILD_HUNT:
                val = utils.formatTimeStr(item[2], 'h:m:s', True, 2, 2, 2)
                finishTime = item[1]
                school = item[3]
            elif proxyID == const.PROXY_KEY_TOP_LEVEL:
                val = str(item[3][0]) + '_' + str(item[3][3]) + '_' + str(item[3][1][4])
                school = SD.data[item[2]]['name'] if item[2] in self.schoolList else '未知'
                finishTime = 0
            else:
                val = item[3][0] if proxyID in (const.PROXY_KEY_TOP_FB_TIME, const.PROXY_KEY_TOP_GLOBAL_ARENA_SCORE) else item[3]
                school = SD.data[item[2]]['name'] if item[2] in self.schoolList else '未知'
                finishTime = item[3][1] if proxyID == const.PROXY_KEY_TOP_FB_TIME else 0
            val = int(val) if type(val) == type(1) or type(val) == type(1.0) else val
            if proxyID == const.PROXY_KEY_TOP_CLAN_WAR_SCORE or proxyID == const.PROXY_KEY_TOP_GUILD_PROSPERITY or proxyID == const.PROXY_KEY_TOP_GUILD_MATCH or proxyID == const.PROXY_KEY_TOP_GUILD_HUNT:
                isSelf = BigWorld.player().guildName == roleName
            elif proxyID == const.PROXY_KEY_TOP_GLOBAL_ARENA_SCORE:
                isSelf = BigWorld.player().gbId == item[0]
            else:
                isSelf = BigWorld.player().roleName == roleName
            if proxyID == const.PROXY_KEY_TOP_GLOBAL_ARENA_SCORE:
                roleName = '【%s】%s' % (utils.getServerName(item[3][2]), roleName)
            gamelog.debug('zt: setRankList', index, roleName, str(val), isSelf, finishTime, school)
            ar.SetElement(0, GfxValue(index))
            ar.SetElement(1, GfxValue(gbk2unicode(roleName)))
            if proxyID in (const.PROXY_KEY_TOP_CLAN_WAR_SCORE,
             const.PROXY_KEY_TOP_GUILD_PROSPERITY,
             const.PROXY_KEY_TOP_GUILD_MATCH,
             const.PROXY_KEY_TOP_GUILD_HUNT):
                ar.SetElement(2, GfxValue(school))
            else:
                ar.SetElement(2, GfxValue(gbk2unicode(school)))
            ar.SetElement(3, GfxValue(gbk2unicode(str(val))))
            ar.SetElement(4, GfxValue(isSelf))
            if proxyID == const.PROXY_KEY_TOP_FB_TIME:
                ar.SetElement(5, GfxValue(gbk2unicode(finishTime)))
            elif proxyID == const.PROXY_KEY_TOP_CLAN_WAR_SCORE:
                ar.SetElement(5, GfxValue(finishTime))
            else:
                ar.SetElement(5, GfxValue(''))
            ar.SetElement(6, GfxValue(str(item[0])))
            ret.SetElement(i, ar)
            pos = i

        if info:
            pos += 1
            ret.SetElement(pos, GfxValue(gbk2unicode(SD.data[BigWorld.player().school]['name'])))
        t = time.localtime(BigWorld.player().getServerTime())
        ret.SetElement(pos + 1, GfxValue(gbk2unicode('%d年%d月%d日' % (t.tm_year, t.tm_mon, t.tm_mday))))
        ret.SetElement(pos + 2, GfxValue(self.lastWeekMoneyRankInfo[1] if self.lastWeekMoneyRankInfo else 0))
        if proxyID == const.PROXY_KEY_TOP_FB_TIME:
            ret.SetElement(pos + 2, GfxValue(self.lastWeekFubenRankInfo[self.fbNo][1] if self.fbNo in self.lastWeekFubenRankInfo and self.lastWeekFubenRankInfo[self.fbNo] else 0))
        elif proxyID == const.PROXY_KEY_TOP_GUILD_PROSPERITY:
            ret.SetElement(pos + 2, GfxValue(self.lastWeekGuildProsperityRankInfo[1] if self.lastWeekGuildProsperityRankInfo else 0))
        elif proxyID == const.PROXY_KEY_TOP_GUILD_MATCH:
            ret.SetElement(pos + 2, GfxValue(self.lastWeekGuildMatchRankInfo[1] if self.lastWeekGuildMatchRankInfo else 0))
        elif proxyID == const.PROXY_KEY_TOP_GUILD_HUNT:
            ret.SetElement(pos + 2, GfxValue(self.lastWeekGuildHuntRankInfo[1] if self.lastWeekGuildHuntRankInfo else 0))
        if self.mediator != None:
            self.mediator.Invoke('setRankList', ret)

    def onRefreshRankInfo(self, *arg):
        idx = int(arg[3][0].GetNumber())
        self.tab = idx
        lvKey = self.getPlayerTopRankKey()
        p = BigWorld.player()
        if p.bindCash + p.cash < 100:
            BigWorld.player().showTopMsg('金钱不足100')
            p.chatToEventEx('金钱不足100', const.CHANNEL_COLOR_RED)
            return
        if idx == 0:
            p.cell.refreshTopEquipScores(self.equipVer.get(lvKey, 0))
            if self.equipInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_EQUIP_SCORE, self.equipVer[lvKey], self.equipInfo[lvKey], lvKeyStr=lvKey)
        elif idx == 1:
            p.cell.refreshTopLevel(self.lvVer)
            if self.lvInfo != None:
                self.setRankList(const.PROXY_KEY_TOP_LEVEL, self.lvVer, self.lvInfo)
        elif idx == 2:
            pass
        elif idx == 3:
            pass
        elif idx == 4:
            p.cell.refreshTopAchPoints(self.achPointsVer.get(lvKey, 0))
            if self.achPointsInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_ACHIEVE_POINTS, self.achPointsVer[lvKey], self.achPointsInfo[lvKey], lvKeyStr=lvKey)
        elif idx == 5:
            p.cell.refreshTopMoney(self.moneyVer.get(lvKey, 0))
            if self.moneyInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_MONEY, self.moneyVer[lvKey], self.moneyInfo[lvKey], self.lastWeekMoneyRankInfo, lvKeyStr=lvKey)
        elif idx == 6:
            p.cell.refreshTopClanWarScore(self.clanWarVer)
        elif idx == 7:
            p.cell.refreshTopSocLevel(self.socialLvVer.get(lvKey, 0))
            if self.socialLvInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_SOCAIL_LEVEL, self.socialLvVer[lvKey], self.socialLvInfo[lvKey], lvKeyStr=lvKey)
        elif idx == 10:
            lvKey += '_' + str(p.school)
            p.cell.refreshCombatScore(self.fightRankVer.get(lvKey, 0))
            if self.fightRankInfo.has_key(lvKey):
                self.setRankList(const.PROXY_KEY_TOP_COMBAT_SCORE, self.fightRankVer[lvKey], self.fightRankInfo[lvKey], lvKeyStr=lvKey)
        elif idx == 11:
            pass
        elif idx == 12:
            pass

    def getRankTitle(self, idx, money):
        if idx == 1 and money >= 5000000:
            return '富甲天下'
        if idx <= 2 and money >= 1000000:
            return '富可敌国'
        if idx <= 3 and money >= 500000:
            return '富甲一方'
        if idx <= 4 and money >= 200000:
            return '财源八荒'
        if idx <= 5 and money >= 100000:
            return '钟鸣鼎食'
        if idx <= 6 and money >= 50000:
            return '挥金如土'
        if idx <= 8 and money >= 20000:
            return '一掷千金'
        if idx <= 10 and money >= 10000:
            return '锦衣玉食'
        if idx <= 15 and money >= 5000:
            return '腰缠万贯'
        if idx <= 20 and money >= 2000:
            return '财源广进'
        if idx <= 100:
            return '日进斗金'

    def setTopMoneyTitle(self, info):
        for i, item in enumerate(info):
            item[3] = self.getRankTitle(i + 1, item[3])

        return info

    def _getFbNo(self, fbDataId):
        if TFD.data.has_key(fbDataId):
            return TFD.data[fbDataId]['fbNo']
        return -1

    def setTopFbTime(self, fbNo, info):
        for item in info:
            if self.fubenIgnoreTime[int(fbNo)]:
                item[3] = (item[3][0], '--:--:--')
                continue
            second = int(item[3][1])
            ar = []
            hour = str(int(second / 3600))
            ar.append(('0' if len(hour) == 1 else '') + hour)
            second = int(second % 3600)
            minute = str(int(second / 60))
            ar.append(('0' if len(minute) == 1 else '') + minute)
            second = str(int(second % 60))
            ar.append(('0' if len(second) == 1 else '') + second)
            item[3] = (item[3][0], ':'.join(ar))

        return info

    def onGetTab(self, *arg):
        return GfxValue(self.tab)

    def onGetTopReward(self, *arg):
        if self.awardType == gametypes.TOP_TYPE_FB:
            BigWorld.player().cell.getTopReward(self.awardType, TFD.data[self.awardStype]['fbNo'])
        else:
            BigWorld.player().cell.getTopReward(self.awardType, self.awardStype)

    def onShowAwardPanel(self, *arg):
        self.closeAwardPanel()
        self.awardType = int(arg[3][0].GetNumber())
        self.awardStype = int(arg[3][1].GetNumber())
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RANK_AWARD)

    def closeAwardPanel(self):
        self.awardMediator = None
        self.awardType = None
        self.awardStype = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RANK_AWARD)

    def reset(self):
        super(self.__class__, self).reset()
        self.resetData()

    def resetData(self):
        self.fubenVer = {}
        self.fubenIgnoreTime = dict(zip([ self._getFbNo(x) for x in TFD.data.keys() ], [ TFD.data.get(x, {}).get('ignoreTime', 0) for x in TFD.data.keys() ]))
        self.lastWeekFubenRankInfo = {}
        self.lastWeekGuildMatchRankInfo = ()
        self.matchVer = 0
        self.fubenInfo = None
        self.fbIdx = 0
        self.fbNo = 0
        self.mySchool = 0
        self.selectedSchool = 0
        self.fubenId = 0

    def onCloseRankAward(self, *arg):
        self.closeAwardPanel()

    def clearWidget(self):
        self.closeRankList()
        self.closeAwardPanel()
        self.closeFightAward()

    def _createAwardInfo(self):
        if self.awardType == gametypes.TOP_TYPE_GROUP_FB_RANK:
            return gameglobal.rds.ui.ranking._createRwardInfo(self.awardType, self.awardStype)
        awardBtnEnabled = False
        lastRank = 0
        if self.awardType == gametypes.TOP_TYPE_MONEY:
            lastRank = self.lastWeekMoneyRankInfo[1] if self.lastWeekMoneyRankInfo else 0
            if self.lastWeekMoneyRankInfo and lastRank != 0:
                awardBtnEnabled = not self.lastWeekMoneyRankInfo[3]
        elif self.awardType == gametypes.TOP_TYPE_FB:
            if not TFD.data.has_key(self.awardStype):
                lastRank = 0
                awardBtnEnabled = 0
            else:
                lastRank = self.lastWeekFubenRankInfo[TFD.data[self.awardStype]['fbNo']][1] if TFD.data[self.awardStype]['fbNo'] in self.lastWeekFubenRankInfo and self.lastWeekFubenRankInfo[TFD.data[self.awardStype]['fbNo']] else 0
                if TFD.data[self.awardStype]['fbNo'] in self.lastWeekFubenRankInfo and lastRank != 0:
                    awardBtnEnabled = not self.lastWeekFubenRankInfo[TFD.data[self.awardStype]['fbNo']][3] and self.getFbMaxRewardRank(TFD.data[self.awardStype]['fbNo']) >= lastRank
        elif self.awardType == gametypes.TOP_TYPE_GUILD_MATCH:
            lastRank = self.lastWeekGuildMatchRankInfo[1] if self.lastWeekGuildMatchRankInfo else 0
            if self.lastWeekGuildMatchRankInfo and lastRank != 0:
                awardBtnEnabled = not self.lastWeekGuildMatchRankInfo[3]
        elif self.awardType == gametypes.TOP_TYPE_GUILD_HUNT:
            lastRank = self.lastWeekGuildHuntRankInfo[1] if self.lastWeekGuildHuntRankInfo else 0
            if self.lastWeekGuildHuntRankInfo and lastRank != 0:
                awardBtnEnabled = not self.lastWeekGuildHuntRankInfo[3]
        elif self.awardType == gametypes.TOP_TYPE_GUILD_PROPERITY:
            lastRank = self.lastWeekGuildProsperityRankInfo[1] if self.lastWeekGuildProsperityRankInfo else 0
            if self.lastWeekGuildProsperityRankInfo and lastRank != 0:
                awardBtnEnabled = not self.lastWeekGuildProsperityRankInfo[3]
        elif self.awardType == gametypes.TOP_TYPE_COMBAT_SCORE:
            lastRank = self.lastWeekCombatRankInfo[1] if self.lastWeekCombatRankInfo else 0
            if self.lastWeekCombatRankInfo and lastRank != 0:
                awardBtnEnabled = not self.lastWeekCombatRankInfo[3]
        elif self.awardType == gametypes.TOP_TYPE_GROUP_FB_RANK:
            awardBtnEnabled = False
            lastRank = 0
        awardItems = []
        title, items = self.getTopAward()
        for item in items:
            iconPath = uiUtils.getItemIconFile64(item[0])
            color = uiUtils.getItemColor(item[0])
            awardItems.append([iconPath,
             item[1],
             color,
             item[0]])

        titleStr = TD.data.get(title, {}).get('name', '')
        if titleStr:
            titleStr = '获得称号【%s】' % titleStr
        awardList = []
        if self.awardType == gametypes.TOP_TYPE_FB:
            tData = TRD.data.get((self.awardType, TFD.data[self.awardStype]['fbNo'], 0), {})
        else:
            tData = TRD.data.get((self.awardType, self.awardStype, 0), {})
        for td in tData:
            desc = td.get('desc', '')
            title = TD.data.get(td.get('title', 0), {}).get('name', '')
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
        ret = [lastRank,
         awardBtnEnabled,
         awardItems,
         titleStr,
         awardList,
         cash,
         self.awardType]
        return ret

    def onGetAwardInfo(self, *arg):
        ret = self._createAwardInfo()
        return uiUtils.array2GfxAarry(ret, True)

    def getTopAward(self):
        if self.awardType == None or self.awardStype == None:
            return (0, [])
        if self.awardType == gametypes.TOP_TYPE_FB:
            if TRD.data.has_key((self.awardType, TFD.data[self.awardStype]['fbNo'], self.mySchool)):
                tData = TRD.data[self.awardType, TFD.data[self.awardStype]['fbNo'], self.mySchool]
            else:
                tData = TRD.data.get((self.awardType, TFD.data[self.awardStype]['fbNo'], 0), {})
        else:
            tData = TRD.data.get((self.awardType, self.awardStype, 0), {})
        if self.awardType == gametypes.TOP_TYPE_MONEY:
            if self.lastWeekMoneyRankInfo:
                rank = self.lastWeekMoneyRankInfo[1]
                value = self.lastWeekMoneyRankInfo[2]
            else:
                return (0, [])
        elif self.awardType == gametypes.TOP_TYPE_GUILD_MATCH:
            if self.lastWeekGuildMatchRankInfo:
                rank = self.lastWeekGuildMatchRankInfo[1]
                value = self.lastWeekGuildMatchRankInfo[2]
            else:
                return (0, [])
        elif self.awardType == gametypes.TOP_TYPE_GUILD_HUNT:
            if self.lastWeekGuildHuntRankInfo:
                rank = self.lastWeekGuildHuntRankInfo[1]
                value = self.lastWeekGuildHuntRankInfo[2]
            else:
                return (0, [])
        elif self.awardType == gametypes.TOP_TYPE_GUILD_PROPERITY:
            if self.lastWeekGuildProsperityRankInfo:
                rank = self.lastWeekGuildProsperityRankInfo[1]
                value = self.lastWeekGuildProsperityRankInfo[2]
            else:
                return (0, [])
        elif self.awardType == gametypes.TOP_TYPE_FB:
            if self.fbNo in self.lastWeekFubenRankInfo and self.lastWeekFubenRankInfo[self.fbNo]:
                rank = self.lastWeekFubenRankInfo[self.fbNo][1]
                value = self.lastWeekFubenRankInfo[self.fbNo][2]
            else:
                return (0, [])
        elif self.awardType == gametypes.TOP_TYPE_COMBAT_SCORE:
            if self.lastWeekCombatRankInfo:
                rank = self.lastWeekCombatRankInfo[1]
                value = self.lastWeekCombatRankInfo[2]
            else:
                return (0, [])
        elif self.awardType == gametypes.TOP_TYPE_GROUP_FB_RANK:
            rank = 1
            value = 100
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
            if not items:
                items = ()
            return (title, items)

        return (0, [])

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        itemId = int(key.split('.')[1])
        item = Item(itemId)
        return gameglobal.rds.ui.inventory.GfxToolTip(item)

    def refreshAwardPanel(self):
        ret = self._createAwardInfo()
        if self.awardMediator != None:
            self.awardMediator.Invoke('setAwardInfo', uiUtils.array2GfxAarry(ret, True))

    def onGetShowType(self, *arg):
        info = {}
        info['showType'] = self.showType
        info['crossArenaVisible'] = gameglobal.rds.configData.get('enableCrossServerArena', False)
        info['enableNewArenaRank'] = gameglobal.rds.configData.get('enableNewArenaRank', False)
        return uiUtils.dict2GfxDict(info)

    def onGetDefaultFubenId(self, *arg):
        return GfxValue(self.fubenId)

    def onGetDetailText(self, *arg):
        key = arg[3][0].GetString()
        p = BigWorld.player()
        ret = ''
        if key == 'socialLvBtn':
            ret = '社会等级:' + str(p.socLv)
        elif key == 'arenaBtn':
            ret = '竞技场等级:' + str(p.arenaInfo.arenaScore)
        elif key == 'wealthBtn':
            ret = '财富等级:'
        elif key == 'clanWarBtn' or key == 'prosperityBtn':
            ret = '繁荣度:' + str(p.guild.prosperity if p.guild else 0)
        elif key == 'subClanWar':
            ret = '总积分:' + str(p.guild.clanWarScore if p.guild else 0)
        elif key == 'matchScore':
            ret = '众里寻他积分:' + str(p.guild.matchScore if p.guild else 0)
        elif key == 'hunt':
            ret = ''
        elif key == 'equipBtn':
            ret = '装备评分:' + str(p.equipment.calcAllEquipScore(p.suitsCache))
        elif key == 'lvBtn':
            ret = '等级:' + str(p.lv)
        elif key == 'skillEnhancePoint':
            ret = '技能修炼点:' + str(utils.getTotalSkillEnhancePoint(p))
        return GfxValue(gbk2unicode(ret))

    def onGetPlayerSchool(self, *arg):
        self.mySchool = BigWorld.player().realSchool
        return GfxValue(self.mySchool)

    def onGetFightAwardInfo(self, *arg):
        return uiUtils.array2GfxAarry(sorted(self.fightAwardData, key=lambda k: k[3], reverse=True), True)

    def showFightAwardList(self, data):
        self.fightAwardData = data[1]
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FIGHTAWARD_LIST)

    def onShowFightAward(self, *arg):
        BigWorld.player().base.getTopCombatScoreBak(self.curSchool)

    def closeFightAward(self):
        self.fightAwardData = []
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FIGHTAWARD_LIST)

    def onCloseFightAward(self, *arg):
        self.closeFightAward()

    def onSetCurSchool(self, *arg):
        self.curSchool = int(arg[3][0].GetNumber())
