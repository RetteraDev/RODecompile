#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/suiXingYuProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import formula
import const
import utils
from uiProxy import UIProxy
from guis import uiConst
from guis import ui
from guis import uiUtils
from crontab import CronTab
from data import ore_spawn_point_data as OSPD
from data import sys_config_data as SYSD
from data import multiline_digong_data as MDD
from cdata import game_msg_def_data as GMDD

class SuiXingYuProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SuiXingYuProxy, self).__init__(uiAdapter)
        self.modelMap = {'endActivity': self.onEndActivity,
         'refreshResult': self.onRefreshResult,
         'showGuildRank': self.onShowGuildRank}
        self.resultVersion = 0
        self.rankVersion = 0
        self.rankData = None
        self.resultData = None
        self.endCallback = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUI_XING_YU_RESULT, self.hide)
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUI_XING_YU_GUILD_RESULT, self.hideGuildRank)

    def _registerMediator(self, widgetId, mediator):
        mlgNo = formula.getMLGNo(BigWorld.player().spaceNo)
        if widgetId == uiConst.WIDGET_SUI_XING_YU_RESULT:
            self.resultMed = mediator
            BigWorld.player().cell.getMLClanWarInfo(mlgNo, self.resultVersion)
            if self.resultData:
                return uiUtils.dict2GfxDict(self.resultData, True)
            self.onGetResultData([0,
             {},
             0,
             0,
             []])
        elif widgetId == uiConst.WIDGET_SUI_XING_YU_GUILD_RESULT:
            self.rankMed = mediator
            if not self.rankMlgNo:
                self.rankMlgNo = formula.getMLGNo(BigWorld.player().spaceNo)
            BigWorld.player().cell.getMLClanWarGuildRank(self.rankMlgNo, self.rankVersion)
            initData = {'rankData': self.rankData,
             'isInSuiXingYu': self.isPlayerInSuiXingYu()}
            if self.rankData:
                return uiUtils.dict2GfxDict(initData, True)
            else:
                self.onGetGuildRankData([0, []])
                return uiUtils.dict2GfxDict(initData, True)
        elif widgetId == uiConst.WIDGET_SUI_XING_YU_GUILD_RANK:
            self.guildRankMed = mediator
            BigWorld.player().cell.getMLClanWarGuildRank(mlgNo, self.rankVersion)
            if self.rankData:
                return uiUtils.array2GfxAarry(self.rankData, True)
            self.onGetGuildRankData([0, []])

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_SUI_XING_YU_GUILD_RANK:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SUI_XING_YU_GUILD_RANK)
        elif widgetId == uiConst.WIDGET_SUI_XING_YU_GUILD_RESULT:
            self.rankMlgNo = None
            self.hideGuildRank()
        else:
            UIProxy._asWidgetClose(self, widgetId, multiID)

    def intoMultoLine(self):
        if formula.getMLGNo(BigWorld.player().spaceNo) in const.ML_SPACE_NO_SXY:
            self.clearWidget()
            destroyTime = MDD.data.get(const.ML_GROUP_NO_CLANWAR, {}).get('destroyTime', 0)
            enableCT = CronTab(destroyTime)
            delay = enableCT.next(BigWorld.player().getServerTime())
            sxyCalcTime = SYSD.data.get('sxyCalcTime', 30)
            if self.endCallback:
                BigWorld.cancelCallback(self.endCallback)
                self.endCallback = None
            if delay - sxyCalcTime > 0:
                self.endCallback = BigWorld.callback(delay - sxyCalcTime, self.showGuildRank)
            self.showResult()

    def isSuiXingYuTime(self):
        data = MDD.data.get(const.ML_GROUP_NO_CLANWAR, {})
        if data:
            createTime = data.get('createTime', utils.CRON_ANY)
            destroyTime = data.get('destroyTime', utils.CRON_ANY)
            weekSet = data.get('weekSet', 0)
            return utils.inTimeRange(createTime, destroyTime, weekSet=weekSet)

    def leaveMultoLine(self):
        if self.endCallback:
            BigWorld.cancelCallback(self.endCallback)
            self.endCallback = None
        self.hide()

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SUI_XING_YU_GUILD_RESULT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SUI_XING_YU_RESULT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SUI_XING_YU_GUILD_RANK)

    def reset(self):
        self.resultMed = None
        self.rankMed = None
        self.guildRankMed = None
        self.rankMlgNo = None
        if BigWorld.player():
            BigWorld.player().unlockKey(gameglobal.KEY_POS_UI)

    def showGuildRank(self, mlgNo = None):
        if not BigWorld.player() or not utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            return
        if self.isPlayerInSuiXingYu():
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SUI_XING_YU_GUILD_RANK)
            if BigWorld.player():
                BigWorld.player().showGameMsg(GMDD.data.SUI_XING_YU_END_MSG, ())
        self.rankMlgNo = mlgNo
        if BigWorld.player().mapID != const.ML_GROUP_NO_GSXY:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SUI_XING_YU_GUILD_RESULT)

    def showGuildRankOrResult(self, mlgNo = None):
        if self.isSuiXingYuTime():
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SUI_XING_YU_GUILD_RANK)
        elif BigWorld.player().mapID != const.ML_GROUP_NO_GSXY:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SUI_XING_YU_GUILD_RESULT)
        self.rankMlgNo = mlgNo

    def hideGuildRank(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SUI_XING_YU_GUILD_RESULT)

    def isPlayerInSuiXingYu(self):
        return BigWorld.player() and formula.getMLGNo(BigWorld.player().spaceNo) in const.ML_SPACE_NO_SXY

    def showResult(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SUI_XING_YU_RESULT)

    def onEndActivity(self, *args):
        gameglobal.rds.ui.diGong.onDiGongButtonClick(None)

    @ui.callFilter(2, True)
    def onRefreshResult(self, *args):
        mlgNo = formula.getMLGNo(BigWorld.player().spaceNo)
        BigWorld.player().cell.getMLClanWarInfo(mlgNo, self.rankVersion)

    def onShowGuildRank(self, *args):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SUI_XING_YU_GUILD_RANK)

    def onGetResultData(self, data):
        self.resultVersion = data[0]
        result = {'guildName': BigWorld.player().guildName,
         'stoneNum': data[2],
         'rankNum': data[3] if data[3] > 0 else gameStrings.TEXT_CLANWARPROXY_421}
        playerRank = []
        stoneDatas = []
        result['playerRank'] = playerRank
        result['stoneDatas'] = stoneDatas
        result['suiXingYuTip'] = SYSD.data.get('suiXingYuTip', '')
        for rank, name, school, score, contri in data[4]:
            tmpData = {'rank': rank,
             'name': name,
             'school': formula.whatSchoolName(school),
             'stoneNum': score,
             'guildContribution': contri}
            if name == BigWorld.player().roleName:
                result['myRank'] = tmpData
            if rank <= const.ML_CLANWAR_TOP_MEMBER_NUM:
                playerRank.append(tmpData)

        for key, value in OSPD.data.items():
            if key not in data[1].keys():
                guildName = gameStrings.TEXT_SUIXINGYUPROXY_177
            else:
                guildInfo = data[1].get(key, (0, ''))
                if guildInfo[0] > 0:
                    guildName = guildInfo[1]
                else:
                    guildName = gameStrings.TEXT_CLANWARPROXY_111
            stoneDatas.append({'icon': 'oreSpawnPoint/%s.dds' % value.get('icon', ''),
             'name': value.get('name', ''),
             'guildName': guildName,
             'tips': value.get('tips', '')})

        self.resultData = result
        if self.resultMed:
            self.resultMed.Invoke('refreshPanel', uiUtils.dict2GfxDict(self.resultData, True))

    def onGetGuildRankData(self, data):
        self.rankVersion = data[0]
        result = []
        for guildRank, guildName, guildScore, guildBonus, leaderBonus in data[1]:
            if guildRank:
                bonus = [ uiUtils.getGfxItemById(itemId, leaderBonus.get(itemId)) for itemId in leaderBonus.keys() ] + [ uiUtils.getGfxItemById(itemId, guildBonus.get(itemId)) for itemId in guildBonus.keys() ]
                result.append({'rank': guildRank,
                 'guildName': guildName,
                 'stoneNum': guildScore,
                 'guildBonus': bonus})

        result.sort(key=lambda value: value.get('stoneNum', 0), reverse=True)
        for item in result:
            item['rank'] = result.index(item) + 1
            item['stoneNum'] = int(item['stoneNum'])

        self.rankData = result
        if self.rankMed:
            self.rankMed.Invoke('refreshPanel', uiUtils.array2GfxAarry(self.rankData, True))
        if self.guildRankMed:
            self.guildRankMed.Invoke('refreshPanel', uiUtils.array2GfxAarry(self.rankData, True))
