#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zhanJuProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import utils
import uiUtils
import gametypes
import gameglobal
import uiConst
import const
from uiProxy import UIProxy
from data import monster_clan_war_client_data as MCWCD
from data import monster_clan_war_config_data as MCWCFD
from data import activity_basic_data as ABD
MONSTER_CLAN_WAR_START = 1
MONSTER_CLAN_WAR_END = 2
MONSTER_CLAN_WAR_PREPARE = 3

class ZhanJuProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZhanJuProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'findPath': self.onFindPath,
         'clickRank': self.onClickRank,
         'gotoGuildRank': self.onGotoGuildRank}
        self.reset()
        self.startTime = 0
        self.prepareTime = 0
        self.activityState = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZHANJU, self.hide)

    def reset(self):
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ZHANJU)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ZHANJU)

    def _asWidgetClose(self, widgetId, multiID):
        self.hide()

    def getInitData(self):
        hideIdList = []
        info = {}
        data = {}
        data['time'] = self.getShowTime()
        data['status'] = self.getActivityState()
        data['info'] = info
        data['tipText'] = MCWCFD.data.get('ZHANJU_ACTION_TIPS', gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_23)
        monsterData = BigWorld.player().clientPersistentNotifyList.get(gametypes.CLIENT_PERSISTENT_NOTIFY_MAP_MONSTER_CLAN_WAR, [])
        if not monsterData:
            return data
        for item in monsterData:
            iconData = MCWCD.data.get(item, {})
            hideId = iconData.get('hideId')
            hideIdList.append(hideId)
            info[item] = iconData

        for delId in hideIdList:
            if info.has_key(delId):
                info.pop(delId)

        return data

    def getShowTime(self):
        status = self.getActivityState()
        if status == MONSTER_CLAN_WAR_PREPARE:
            time = self.getPrepareTime()
        elif status == MONSTER_CLAN_WAR_START:
            time = utils.getNow() - self.startTime
        else:
            time = -1
        return time

    def updateView(self):
        if self.mediator:
            self.mediator.Invoke('updateView', uiUtils.dict2GfxDict(self.getInitData(), True))

    def updateStartTime(self, time):
        self.activityState = MONSTER_CLAN_WAR_START
        self.startTime = time
        self.updateStatus(self.getShowTime())

    def updatePrepareTime(self, time):
        self.activityState = MONSTER_CLAN_WAR_PREPARE
        self.prepareTime = time
        self.updateStatus(self.getShowTime())

    def updateEndTime(self):
        self.activityState = MONSTER_CLAN_WAR_END
        self.updateStatus(self.getShowTime())

    def updateStatus(self, time):
        if self.mediator:
            self.mediator.Invoke('updateStatus', (GfxValue(time), GfxValue(self.getActivityState())))

    def onInitData(self, *args):
        return uiUtils.dict2GfxDict(self.getInitData(), True)

    def onFindPath(self, *args):
        posId = str(long(args[3][0].GetNumber()))
        uiUtils.findPosById(posId)

    def onClickRank(self, *args):
        gameglobal.rds.ui.monsterClanWarActivity.show()

    def onGotoGuildRank(self, *args):
        if not gameglobal.rds.configData.get('enableGuildMonsterClanWar', False):
            return
        gameglobal.rds.ui.ranking.showGuildRankPanel(const.PROXY_KEY_TOP_GUILD_MONSTER_CLAN_WAR)

    def getActivityState(self):
        return self.activityState

    def getStartTime(self):
        data = ABD.data.get(uiConst.MONSTER_CLAN_ACTIVITY_ID, {})
        startTimes = data.get('startTimes', None)
        if startTimes:
            return utils.getNextCrontabTime(startTimes[0])
        else:
            return 0

    def getPrepareTime(self):
        return self.getStartTime() - utils.getNow()
