#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/guildCrossTRankProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
from uiProxy import UIProxy

class GuildCrossTRankProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildCrossTRankProxy, self).__init__(uiAdapter)
        self.modelMap = {'getRankInfo': self.onGetRankInfo}
        self.mediator = None
        self.groupId = 0
        self.currentTabIndex = -1
        self.secondTabIndex = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_RANK, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_RANK:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_RANK)

    def reset(self):
        self.groupId = 0
        self.currentTabIndex = -1
        self.secondTabIndex = -1

    def show(self, groupId):
        self.groupId = groupId
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_CROSS_TOURNAMENT_RANK)

    def queryRankInfo(self):
        pass

    def onGetRankInfo(self, *arg):
        currentTabIndex = int(arg[3][0].GetNumber())
        secondTabIndex = int(arg[3][1].GetNumber())
        if self.currentTabIndex == currentTabIndex and self.secondTabIndex == secondTabIndex:
            return
        self.currentTabIndex = currentTabIndex
        self.secondTabIndex = secondTabIndex
        self.refreshInfo(self.groupId)
        self.queryRankInfo()

    def refreshInfo(self, groupId):
        if self.groupId != groupId:
            return
        if self.mediator:
            p = BigWorld.player()
            guildTournament = p.guildTournament.get(self.groupId)
            if not guildTournament:
                return
            info = {}
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
