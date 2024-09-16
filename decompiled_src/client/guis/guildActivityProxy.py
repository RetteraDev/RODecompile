#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildActivityProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import uiConst
import const
import uiUtils
import utils
from ui import gbk2unicode
from uiProxy import UIProxy
from data import guild_activity_data as GAD
from cdata import game_msg_def_data as GMDD

class GuildActivityProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildActivityProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickManager': self.onClickManager,
         'getTabInfo': self.onGetTabInfo,
         'start': self.onStart,
         'nextRound': self.onNextRound,
         'gainGuildMatchItem': self.onGainGuildMatchItem,
         'checkGuildNextMatchRound': self.onCheckGuildNextMatchRound}
        self.mediator = None
        self.gainMed = None
        self.markerId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_ACTIVITY, self.hideActivityPanel)
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MATCH_ITEM, self.hideMatchItem)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_ACTIVITY:
            self.mediator = mediator
        elif widgetId == uiConst.WIDGET_GUILD_MATCH_ITEM:
            initData = {'item': {'iconPath': uiUtils.getItemIconFile64(BigWorld.player().guild.memberMe.matchItemId),
                      'itemId': BigWorld.player().guild.memberMe.matchItemId}}
            if BigWorld.player().guild.memberMe.matchItemId == const.GUILD_MATCH_INSTANT_ITEM_ID:
                initData['tipTxt'] = gameStrings.TEXT_GUILDACTIVITYPROXY_44
            else:
                initData['tipTxt'] = gameStrings.TEXT_GUILDACTIVITYPROXY_46 % self.getMyMatchName()
            self.gainMed = mediator
            return uiUtils.dict2GfxDict(initData, True)

    def show(self, markerId):
        if not self.mediator:
            self.markerId = markerId
            enableGuildActivity = gameglobal.rds.configData.get('enableGuildActivity', False)
            if enableGuildActivity:
                gameglobal.rds.ui.guild.hideAllGuildBuilding()
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_ACTIVITY)

    def clearWidget(self):
        self.mediator = None
        self.gainMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_ACTIVITY)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_MATCH_ITEM)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.markerId = 0

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_GUILD_ACTIVITY:
            self.hideActivityPanel()
        elif widgetId == uiConst.WIDGET_GUILD_MATCH_ITEM:
            self.hideMatchItem()

    def hideActivityPanel(self):
        self.markerId = 0
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_ACTIVITY)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def _getMatchList(self):
        result = []
        p = BigWorld.player()
        matches = p.guild.matches
        if matches:
            members = p.guild.member
            keys = matches.keys()
            keys1 = [ k for k in keys if matches[k] ]
            keys2 = [ k for k in keys if not matches[k] ]
            keys1.sort(lambda x, y: (cmp(x[0], y[0]) if matches[x] == matches[y] else cmp(matches[x], matches[y])))
            keys2.sort(lambda x, y: (cmp(x[0], y[0]) if matches[x] == matches[y] else cmp(matches[x], matches[y])))
            keys1.extend(keys2)
            keys = keys1
            idx = 1
            for matchkey in keys:
                matchValue = matches[matchkey]
                item = {}
                item['result'] = idx if matchValue else -1
                item['bgVisible'] = idx % 2 == 0
                item['name1'] = members[matchkey[0]].role if members.has_key(matchkey[0]) else gameStrings.TEXT_GUILDACTIVITYPROXY_103
                if item['name1'] == p.realRoleName:
                    item['name1'] = uiUtils.toHtml(item['name1'], '#2a7117')
                item['name2'] = members[matchkey[1]].role if members.has_key(matchkey[1]) else gameStrings.TEXT_GUILDACTIVITYPROXY_103
                if item['name2'] == p.realRoleName:
                    item['name2'] = uiUtils.toHtml(item['name2'], '#2a7117')
                result.append(item)
                idx += 1

        return result

    def refreshState(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            round = self.getActivitySate()
            if gameglobal.rds.configData.get('enableGuildMatchOptimize', False):
                totalRound = const.GUILD_MATCH_MAX_ROUND_OPTIMIZE
            else:
                totalRound = const.GUILD_MATCH_MAX_ROUND
            self.mediator.Invoke('updateRound', (GfxValue(guild.tMatchEnd),
             GfxValue(round),
             GfxValue(totalRound),
             GfxValue(guild.tMatchRoundEnd)))

    def getActivitySate(self):
        guild = BigWorld.player().guild
        if not guild:
            return -1
        state = guild.matchRound
        if guild.matchRound == 0 and guild.tMatchEnd > 0 and utils.isSameWeek(guild.tMatchEnd):
            state = -1
        return state

    def refreshList(self):
        if self.mediator:
            scoreStr = gameStrings.TEXT_GUILDACTIVITYPROXY_141 % BigWorld.player().guild.matchScore
            self.mediator.Invoke('updateList', (uiUtils.array2GfxAarry(self._getMatchList(), True), GfxValue(gbk2unicode(scoreStr))))

    def onGetTabInfo(self, *arg):
        actId = int(arg[3][0].GetNumber())
        guild = BigWorld.player().guild
        marker = guild.marker.get(self.markerId)
        buildValue = guild.building.get(marker.buildingNUID)
        buildLv = buildValue.level if buildValue else 0
        info = {}
        info['level'] = gameStrings.TEXT_GUILDACTIVITYPROXY_153 % buildLv
        info['desc'] = GAD.data.get(actId, {}).get('desc', '')
        info['tabState'] = self.getTabState(buildLv)
        if actId == gametypes.GUILD_ACTIVITY_MATCH:
            info['currentScore'] = gameStrings.TEXT_GUILDACTIVITYPROXY_141 % guild.matchScore
            info['round'] = self.getActivitySate()
            if gameglobal.rds.configData.get('enableGuildMatchOptimize', False):
                info['totalRound'] = const.GUILD_MATCH_MAX_ROUND_OPTIMIZE
            else:
                info['totalRound'] = const.GUILD_MATCH_MAX_ROUND
            info['endTime'] = guild.tMatchEnd
            info['roundEndTime'] = guild.tMatchRoundEnd
            info['mathList'] = self._getMatchList()
        elif actId == gametypes.GUILD_ACTIVITY_HUNT:
            self.refreshActivityState(gametypes.GUILD_ACTIVITY_HUNT)
        elif actId == gametypes.GUILD_ACTIVITY_MONSTER:
            self.refreshActivityState(gametypes.GUILD_ACTIVITY_MONSTER)
        return uiUtils.dict2GfxDict(info, True)

    def refreshActivityState(self, activityId):
        if self.mediator:
            activity = BigWorld.player().guild._getActivity(activityId)
            info = {}
            info['activityId'] = activityId
            info['state'] = activity.getState()
            if activityId == gametypes.GUILD_ACTIVITY_HUNT:
                info['currentScore'] = gameStrings.TEXT_GUILDACTIVITYPROXY_183 % (0 if info['state'] == gametypes.GUILD_ACTIVITY_READY else 1)
            else:
                info['currentScore'] = gameStrings.TEXT_GUILDACTIVITYPROXY_185 % (0 if info['state'] == gametypes.GUILD_ACTIVITY_READY else 1)
            self.mediator.Invoke('refreshActivityState', uiUtils.dict2GfxDict(info, True))

    def getTabState(self, buildLv):
        tabState = {}
        for activityId in gametypes.GUILD_ACTIVITY_LIST:
            needLv = GAD.data.get(activityId, {}).get('buildingLv', 0)
            tabState[activityId] = {}
            tabState[activityId]['enabled'] = buildLv >= needLv
            tabState[activityId]['tips'] = gameStrings.TEXT_GUILDACTIVITYPROXY_194 % needLv

        return tabState

    def onStart(self, *arg):
        currentTabIndex = int(arg[3][0].GetNumber())
        if currentTabIndex == 0:
            if gameglobal.rds.configData.get('enableGuildMatchOptimize', False):
                BigWorld.player().cell.startGuildMatch()
            else:
                gameglobal.rds.ui.guildActivityOpen.show(gametypes.GUILD_ACTIVITY_MATCH)
        elif currentTabIndex == 2:
            gameglobal.rds.ui.guildActivityOpen.show(gametypes.GUILD_ACTIVITY_MONSTER)

    def onNextRound(self, *arg):
        BigWorld.player().cell.nextGuildMatchRound()

    def showMatchItem(self):
        if BigWorld.player().guildNUID:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_MATCH_ITEM)
        else:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GET_GUILD_MATCH_ITEM)

    def hideMatchItem(self):
        self.gainMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_MATCH_ITEM)

    def onGainGuildMatchItem(self, *arg):
        p = BigWorld.player()
        if p.guildNUID:
            p.cell.gainGuildMatchItem()
        else:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GET_GUILD_MATCH_ITEM)
            self.hideMatchItem()

    def onCheckGuildNextMatchRound(self, *arg):
        BigWorld.player().cell.checkGuildNextMatchRound()

    def getMyMatchName(self):
        p = BigWorld.player()
        matches = p.guild.matches
        for gbIdPair in matches.keys():
            if p.gbId in gbIdPair:
                matchGbId = gbIdPair[1 - gbIdPair.index(p.gbId)]
                if matchGbId and p.guild.member.has_key(matchGbId):
                    return p.guild.member[matchGbId].role

        return ''

    def onClickManager(self, *arg):
        gameglobal.rds.ui.guildResidentManager.showOrHide(self.markerId)
