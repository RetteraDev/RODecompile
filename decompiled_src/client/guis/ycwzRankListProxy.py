#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ycwzRankListProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
import gametypes
import utils
from guis import uiConst
from guis import uiUtils
from Scaleform import GfxValue
from ui import gbk2unicode
from data import bonus_data as BD
from cdata import game_msg_def_data as GMDD
from cdata import top_reward_data as TRD

class YcwzRankListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YcwzRankListProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRewardRuleList': self.onGetRewardRuleList,
         'getSeasonList': self.onGetSeasonList,
         'getHistoryList': self.onGetHistoryList,
         'getCurrentList': self.onGetCurrentList,
         'getCurrentSeason': self.onGetCurrentSeason,
         'getTitle': self.onGetYCWZTitle,
         'getRewardTip': self.onGetRewardTip,
         'getWarTimesTip': self.onGetWarTimesTip}
        self.mediator = None
        self.monthStr = [['01', '02', '03'],
         ['04', '05', '06'],
         ['07', '08', '09'],
         ['10', '11', '12']]
        self.rewardData = None
        self.seasonList = None
        self.historyList = None
        self.currentList = None
        self.roundAttendTimes = 0
        self.seasonAttendTimes = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_YCWZ_RANK_LIST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_YCWZ_RANK_LIST:
            self.mediator = mediator

    def show(self):
        if gameglobal.rds.configData.get('enableYunchuiTopRank', False):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YCWZ_RANK_LIST)

    def reset(self):
        self.mediator = None

    def clearData(self):
        self.rewardData = None
        self.seasonList = None
        self.historyList = None
        self.currentList = None

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.funcNpc.close()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YCWZ_RANK_LIST)

    def onGetSeasonList(self, *arg):
        if self.seasonList != None:
            self.updateSeasonList(self.seasonList)
        BigWorld.player().cell.getYunChuiTopHistory()

    def onGetHistoryList(self, *arg):
        key = arg[3][0].GetString()
        ver = 0
        if self.historyList != None and self.historyList.has_key(key):
            self.updateHistoryData(self.historyList[key])
        BigWorld.player().cell.getYunChuiTopRank(ver, key)

    def onGetCurrentList(self, *arg):
        if self.currentList == None:
            ver = 0
        else:
            ver = self.currentList[0]
        if self.currentList != None:
            self.updateCurrentData(self.currentList)
        else:
            self.updateCurrentData([0,
             [],
             [],
             '0'])
        BigWorld.player().cell.getYunChuiTopRank(ver, '0')

    def updateCurrentData(self, data):
        self.currentList = data
        currentList = self.currentList[1]
        ret = []
        for guildData in currentList[:20]:
            obj = {}
            obj['rank'] = guildData[0]
            obj['guildNUID'] = guildData[1]
            obj['guildName'] = guildData[2]
            scores = []
            for roundData in guildData[4]:
                score = '%d' % roundData[0] if roundData != None else '-'
                scores.append(score)

            scores = scores[::-1]
            obj['scores'] = scores
            ret.append(obj)

        if self.mediator:
            self.mediator.Invoke('updateCurrentView', uiUtils.array2GfxAarry(ret, True))
        self.updateMyCurrentData()

    def updateHistoryData(self, data):
        if len(data) == 0:
            return
        else:
            if self.historyList == None:
                self.historyList = {}
            key = data[3]
            self.historyList[key] = data
            historylist = data[1]
            ret = []
            for historyItem in historylist:
                obj = {}
                obj['rank'] = historyItem[0]
                obj['guildName'] = historyItem[2]
                ret.append(obj)

            ret.sort(key=lambda k: k['rank'])
            if self.mediator:
                self.mediator.Invoke('updateHistoryList', uiUtils.array2GfxAarry(ret, True))
            return

    def updateMyCurrentData(self):
        ret = []
        currentList = self.currentList[1]
        myGuildNUID = BigWorld.player().guildNUID
        for i in xrange(len(currentList)):
            guildNUID = currentList[i][1]
            if myGuildNUID == guildNUID:
                if i - 1 >= 0:
                    ret.append(currentList[i - 1])
                ret.append(currentList[i])
                if i + 1 < len(currentList):
                    ret.append(currentList[i + 1])

        isInGuild = BigWorld.player().guildNUID != 0
        guildRet = {}
        guildRet['data'] = []
        for guildData in ret:
            obj = {}
            obj['rank'] = guildData[0]
            obj['guildNUID'] = guildData[1]
            isMyGuild = guildData[1] == myGuildNUID
            obj['guildName'] = uiUtils.toHtml(guildData[2], color='#a65b11') if isMyGuild else guildData[2]
            scores = []
            for roundData in guildData[4]:
                score = '%d' % roundData[0] if roundData != None else '-'
                scoreStr = uiUtils.toHtml(score, color='#a65b11') if isMyGuild else score
                scores.append(scoreStr)

            scores = scores[::-1]
            obj['scores'] = scores
            guildRet['data'].append(obj)

        if len(currentList) == 0:
            guildRet['guildTip'] = uiUtils.getTextFromGMD(GMDD.data.YCWZ_TIP_NONE_RANK_RESULT, gameStrings.TEXT_YCWZRANKLISTPROXY_172)
        else:
            guildRet['guildTip'] = uiUtils.getTextFromGMD(GMDD.data.YCWZ_TIP_GUILD_RANK_OUT_OF_LIST, gameStrings.TEXT_WMDRANKLISTPROXY_203) if isInGuild else uiUtils.getTextFromGMD(GMDD.data.YCWZ_TIP_NONE_GUILD, gameStrings.TEXT_GM_COMMAND_GUILD_545)
        if self.mediator:
            self.mediator.Invoke('updateMyGuildData', uiUtils.dict2GfxDict(guildRet, True))

    def onGetRewardRuleList(self, *arg):
        enableYunChuiRankGuildMemberAward = gameglobal.rds.configData.get('enableYunChuiRankGuildMemberAward', False)
        if self.rewardData == None:
            curYear = utils.getYearInt()
            curSeason = self._getCurrentSeason()
            curSeaonArr = self.monthStr[curSeason]
            curSeaonStr = '0%d' % (curSeason + 1)
            ret = []
            for i in xrange(len(curSeaonArr)):
                monthKey = '%d%s' % (curYear, curSeaonArr[i])
                if enableYunChuiRankGuildMemberAward:
                    key = (gametypes.TOP_TYPE_YUNCHUI_GUILD_SCORE, gametypes.YUNCHUI_REWARD_SUBKEY_GUILD_MEMBER, uiConst.YCWZ_REWARD_ROUND)
                else:
                    key = (gametypes.TOP_TYPE_YUNCHUI_GUILD_SCORE, int(monthKey), uiConst.YCWZ_REWARD_ROUND)
                data = TRD.data.get(key, [])
                rewards = self.generateRewards(data)
                ret.append(rewards)

            seasonKey = '%d%s' % (curYear, curSeaonStr)
            if enableYunChuiRankGuildMemberAward:
                key = (gametypes.TOP_TYPE_YUNCHUI_GUILD_SCORE, gametypes.YUNCHUI_REWARD_SUBKEY_GUILD_MEMBER, 1)
            else:
                key = (gametypes.TOP_TYPE_YUNCHUI_GUILD_SCORE, int(seasonKey), uiConst.YCWZ_REWARD_SEASON)
            data = TRD.data.get(key, [])
            rewards = self.generateRewards(data)
            ret.append(rewards)
            self.rewardData = self.generateRewardsData(ret)
        if self.mediator:
            self.mediator.Invoke('setRewardRulePage', uiUtils.array2GfxAarry(self.rewardData, True))

    def generateItems(self, bonudId):
        items = []
        bonus = BD.data.get(bonudId, {}).get('fixedBonus', [])
        bonus = utils.filtItemByConfig(bonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        for item in bonus:
            if item[0] == 1:
                data = uiUtils.getGfxItemById(item[1], item[2])
                items.append(data)

        return items

    def generateRewardsData(self, listData):
        if len(listData) == 0:
            return
        ret = []
        fRound = listData[0]
        sRound = listData[1]
        tRound = listData[2]
        totalRound = listData[3]
        dataLen = max(len(fRound), len(sRound), len(tRound), len(totalRound))
        for i in xrange(dataLen):
            itemObj = {}
            rank = i + 1
            itemObj['rank'] = rank
            itemObj['fRound'] = fRound.get(rank, [])
            itemObj['sRound'] = sRound.get(rank, [])
            itemObj['tRound'] = tRound.get(rank, [])
            itemObj['totalRound'] = totalRound.get(rank, [])
            ret.append(itemObj)

        return ret

    def generateRewards(self, listData):
        rewardList = {}
        for data in listData:
            rankRange = data['rankRange']
            bonudId = data['bonusId']
            if rankRange[0] == rankRange[1]:
                rewardList[rankRange[0]] = self.generateItems(bonudId)
            else:
                for i in xrange(rankRange[0], rankRange[1] + 1):
                    rewardList[i] = self.generateItems(bonudId)

        return rewardList

    def updateSeasonList(self, data):
        self.seasonList = sorted(data, reverse=True)
        ret = []
        for season in self.seasonList:
            obj = {}
            obj['key'] = season
            obj['label'] = gameStrings.TEXT_YCWZRANKLISTPROXY_271 % season
            ret.append(obj)

        if self.mediator:
            self.mediator.Invoke('updateSeasonlist', uiUtils.array2GfxAarry(ret, True))

    def onGetCurrentSeason(self, *arg):
        curYear = utils.getYearInt()
        curSeason = self._getCurrentSeason()
        curSeaonStr = '0%d' % curSeason
        return GfxValue('%d%s' % (curYear, curSeaonStr))

    def _getCurrentSeason(self):
        curMonth = utils.getMonthInt()
        curSeason = (curMonth - 1) / 3
        return curSeason

    def onGetYCWZTitle(self, *arg):
        page = int(arg[3][0].GetNumber())
        if gameglobal.rds.loginManager.isGtLogonMode():
            serverName = gameglobal.rds.loginManager.titleName()
        else:
            serverName = ''
        curYear = utils.getYearInt()
        curSeason = self._getCurrentSeason()
        curSeaonStr = '0%d' % (curSeason + 1)
        season = '%d%s' % (curYear, curSeaonStr)
        if page == 0:
            return GfxValue(gbk2unicode(uiUtils.getTextFromGMD(GMDD.data.YCWZ_CURRENT_SEASON_TITLE, gameStrings.TEXT_YCWZRANKLISTPROXY_301) % (serverName, season)))
        if page == 1:
            return GfxValue(gbk2unicode(uiUtils.getTextFromGMD(GMDD.data.YCWZ_HISTORY_SEASON_TITLE, gameStrings.TEXT_YCWZRANKLISTPROXY_303) % serverName))
        if page == 2:
            return GfxValue(gbk2unicode(uiUtils.getTextFromGMD(GMDD.data.YCWZ_REWARD_TITLE, gameStrings.TEXT_YCWZRANKLISTPROXY_305) % serverName))

    def onGetRewardTip(self, *arg):
        tip = uiUtils.getTextFromGMD(GMDD.data.YCWZ_REWARD_RULE_TIP, gameStrings.TEXT_YCWZRANKLISTPROXY_308)
        return GfxValue(gbk2unicode(tip))

    def onGetWarTimesTip(self, *arg):
        tip = uiUtils.getTextFromGMD(GMDD.data.YCWZ_WAR_TIMES_TIP, gameStrings.TEXT_YCWZRANKLISTPROXY_312) % (self.roundAttendTimes, self.seasonAttendTimes)
        return GfxValue(gbk2unicode(tip))

    def setClanWarAttendInfo(self, clanWarAttendInfo):
        self.roundAttendTimes = clanWarAttendInfo[0]
        self.seasonAttendTimes = clanWarAttendInfo[1]
        if self.mediator:
            self.mediator.Invoke('refreshAttendance')
