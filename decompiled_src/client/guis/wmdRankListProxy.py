#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wmdRankListProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
from operator import itemgetter
import gameglobal
import utils
import gametypes
from guis import ui
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from cdata import wmd_guild_reward_data as WGRD
from data import bonus_data as BD
from data import wmd_config_data as WCD

class WmdRankListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WmdRankListProxy, self).__init__(uiAdapter)
        self.modelMap = {'getPersonalRank': self.onGetPersonalRank,
         'getGuildRank': self.onGetGuildRank,
         'getKillRank': self.onGetKillRank}
        self.mediator = None
        self.type = -1
        self.personalData = []
        self.guildData = []
        self.myGuildData = []
        self.killData = []
        self.timerId = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_WMD_RANK_LIST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if self.timerId == None:
            nextWeek = utils.getNextCrontabTime('0 0 * * 0', utils.getNow()) - utils.getNow()
            self.timerId = BigWorld.callback(nextWeek, self.clearData)
        if widgetId == uiConst.WIDGET_WMD_RANK_LIST:
            self.mediator = mediator
            ret = {}
            ret['type'] = self.type
            if self.type == uiConst.WMD_SHANGJIN_RANK:
                ret['title'] = uiUtils.getTextFromGMD(GMDD.data.WMD_SHANGJIN_RANK_TITLE, gameStrings.TEXT_ACTIVITYFACTORY_345)
                ret['tip'] = uiUtils.getTextFromGMD(GMDD.data.WMD_SHANGJIN_RANK_UPDATE_TIP, gameStrings.TEXT_WMDRANKLISTPROXY_47)
            elif self.type == uiConst.WMD_KILL_RANK:
                ret['title'] = uiUtils.getTextFromGMD(GMDD.data.WMD_KILL_RANK_TITLE, gameStrings.TEXT_WMDRANKLISTPROXY_49)
                ret['tip'] = uiUtils.getTextFromGMD(GMDD.data.WMD_KILL_RANK_UPDATE_TIP, gameStrings.TEXT_WMDRANKLISTPROXY_47)
            return uiUtils.dict2GfxDict(ret, True)
        else:
            return

    def openShangjinRank(self):
        isCommonRank = gameglobal.rds.configData.get('enableNewWmdRankListConfig', False)
        if isCommonRank:
            self.uiAdapter.rankCommon.showRankCommon(gametypes.TOP_TYPE_WMD_MEMBER_SCORE)
        else:
            self.type = uiConst.WMD_SHANGJIN_RANK
            self.show()

    def openKillRank(self):
        isCommonRank = gameglobal.rds.configData.get('enableNewWmdRankListConfig', False)
        if isCommonRank:
            self.uiAdapter.rankCommon.showRankCommon(gametypes.TOP_TYPE_WMD_MEMBER_KILL)
        else:
            self.type = uiConst.WMD_KILL_RANK
            self.show()

    def show(self):
        open = WCD.data.get('wmdRankSwitcher', 0)
        if not open:
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WMD_RANK_LIST)

    def reset(self):
        self.mediator = None
        self.type = -1

    def clearData(self):
        self.personalData = []
        self.guildData = []
        self.myGuildData = []
        self.killData = []

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.funcNpc.close()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WMD_RANK_LIST)

    def onGetPersonalRank(self, *arg):
        self.updatePersonalData(self.personalData)
        self._requestPersonalData()

    def onGetGuildRank(self, *arg):
        self.updateGuildData(self.guildData)
        self._requestGuildData()

    def onGetKillRank(self, *arg):
        self.updateKillData(self.killData)
        self._requestKillData()

    @ui.callInCD(5)
    def _requestPersonalData(self):
        p = BigWorld.player()
        if len(self.personalData) == 0:
            version = 0
        else:
            version = self.personalData[0]
        p.cell.getWMDGuildMemberRank(version)

    @ui.callInCD(5)
    def _requestGuildData(self):
        p = BigWorld.player()
        if len(self.guildData) == 0:
            version = 0
        else:
            version = self.guildData[0]
        p.cell.getWMDGuildRank(version)

    @ui.callInCD(5)
    def _requestKillData(self):
        p = BigWorld.player()
        if len(self.killData) == 0:
            version = 0
        else:
            version = self.killData[0]
        p.cell.getWMDKilldRank(version)

    def updatePersonalData(self, data):
        if data == None:
            return
        elif len(data) == 0:
            return
        else:
            ret = []
            self.personalData = data
            memberList = self._sortWMDData(data[1])
            for i in xrange(len(memberList)):
                member = memberList[i]
                itemObj = {}
                itemObj['rank'] = i + 1
                itemObj['playerName'] = member[0]
                itemObj['score'] = member[2]
                itemObj['guildName'] = ''
                ret.append(itemObj)

            if self.mediator:
                self.mediator.Invoke('updatePersonalView', uiUtils.array2GfxAarry(ret, True))
            return

    def updateGuildData(self, data):
        if data == None:
            return
        elif len(data) == 0:
            return
        else:
            ret = []
            self.guildData = data
            guildList = self._sortWMDData(data[1])
            dataLen = min(len(guildList), uiConst.WMD_MAX_RANK_LENGTH)
            self.myGuildData = data[2]
            for i in xrange(dataLen):
                guildItem = guildList[i]
                itemObj = {}
                rank = i + 1
                itemObj['rank'] = rank
                itemObj['guildNUID'] = guildItem[0]
                itemObj['guildName'] = guildItem[1]
                itemObj['score'] = guildItem[2]
                itemObj['timeStamp'] = guildItem[3]
                itemObj['items'] = self._getItemsByRank(rank)
                ret.append(itemObj)

            if self.mediator:
                self.mediator.Invoke('updateGuildView', uiUtils.array2GfxAarry(ret, True))
            self.myGuildData = self.correctMyGuildData()
            self.updateMyGuildData()
            return

    def updateMyGuildData(self):
        myguildData = {}
        myguildData['data'] = []
        if len(self.myGuildData) > 0:
            if len(self.myGuildData) > 1 and len(self.myGuildData[1]) > 0:
                myguildData['data'].append(self.convertMyGuildData(self.myGuildData[1], False))
            if len(self.myGuildData) > 0 and len(self.myGuildData[0]) > 0:
                myguildData['data'].append(self.convertMyGuildData(self.myGuildData[0], True))
            if len(self.myGuildData) > 2 and len(self.myGuildData[2]) > 0:
                myguildData['data'].append(self.convertMyGuildData(self.myGuildData[2], False))
        isInGuild = BigWorld.player().guildNUID != 0
        myguildData['guildTip'] = uiUtils.getTextFromGMD(GMDD.data.YCWZ_TIP_GUILD_RANK_OUT_OF_LIST, gameStrings.TEXT_WMDRANKLISTPROXY_203) if isInGuild else uiUtils.getTextFromGMD(GMDD.data.YCWZ_TIP_NONE_GUILD, gameStrings.TEXT_GM_COMMAND_GUILD_545)
        if self.mediator:
            self.mediator.Invoke('updateMyGuildView', uiUtils.dict2GfxDict(myguildData, True))

    def convertMyGuildData(self, data, isMyGuild):
        itemObj = {}
        if len(data) > 0:
            itemObj['guildNUID'] = data[0]
            itemObj['guildName'] = uiUtils.toHtml(data[1], color='#a65b11') if isMyGuild else data[1]
            itemObj['score'] = uiUtils.toHtml(data[2], color='#a65b11') if isMyGuild else data[2]
            itemObj['rank'] = uiUtils.toHtml(data[3], color='#a65b11') if isMyGuild else data[3]
            itemObj['items'] = self._getItemsByRank(data[3])
        return itemObj

    def _sortWMDData(self, data):
        if len(data) < 1:
            return []
        temp = sorted(data, key=itemgetter(3))
        list = sorted(temp, key=itemgetter(2), reverse=True)
        return list

    def _getItemsByRank(self, rank):
        itemData = WGRD.data
        leaderBonusId = 0
        memBonusId = 0
        for key in itemData:
            obj = itemData[key]
            minRange = obj['id1']
            maxRange = obj['id2']
            if minRange <= rank <= maxRange:
                leaderBonusId = obj['leaderBonusId']
                memBonusId = obj['bonusId']
                break

        leaderBonus = BD.data.get(leaderBonusId, {}).get('fixedBonus', [])
        leaderBonus = utils.filtItemByConfig(leaderBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        memBonus = BD.data.get(memBonusId, {}).get('fixedBonus', [])
        memBonus = utils.filtItemByConfig(memBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        items = []
        if len(leaderBonus) > 0:
            for item in leaderBonus:
                if item[0] == 1:
                    data = uiUtils.getGfxItemById(item[1], item[2])
                    items.append(data)
                    break

        if len(memBonus) > 0:
            for item in memBonus:
                if item[0] == 1:
                    data = uiUtils.getGfxItemById(item[1], item[2])
                    items.append(data)
                    break

        return items

    def correctMyGuildData(self):
        if len(self.myGuildData) == 0:
            return []
        correctedData = self.myGuildData
        guildList = self._sortWMDData(self.guildData[1])
        dataLen = min(len(guildList), uiConst.WMD_MAX_RANK_LENGTH)
        myGuildNUID = BigWorld.player().guildNUID
        myRankInfo = []
        preGuildInfo = []
        nextGuildInfo = []
        for i in xrange(dataLen):
            if i == uiConst.WMD_MAX_RANK_LENGTH + 1:
                continue
            guildItem = guildList[i]
            rank = i + 1
            guildNUID = guildItem[0]
            if myGuildNUID == guildNUID:
                myRankInfo = list(guildList[i])
                myRankInfo[3] = rank
                if i > 0:
                    preGuildInfo = list(guildList[i - 1])
                    preGuildInfo[3] = rank - 1
                else:
                    preGuildInfo = []
                if i < dataLen - 1:
                    nextGuildInfo = list(guildList[i + 1])
                    nextGuildInfo[3] = rank + 1
                else:
                    nextGuildInfo = []
                correctedData = (myRankInfo, preGuildInfo, nextGuildInfo)
                break

        if len(myRankInfo) == 0 and len(preGuildInfo) == 0 and len(nextGuildInfo) == 0:
            correctedData = []
        return correctedData

    def updateKillData(self, data):
        if len(data) == 0:
            return
        ret = []
        self.killData = data
        memberList = self._sortWMDData(data[1])
        for i in xrange(len(memberList)):
            member = memberList[i]
            itemObj = {}
            itemObj['rank'] = i + 1
            itemObj['playerName'] = member[0]
            itemObj['score'] = member[2]
            itemObj['guildName'] = member[1]
            ret.append(itemObj)

        if self.mediator:
            self.mediator.Invoke('updatePersonalView', uiUtils.array2GfxAarry(ret, True))
