#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBuildSelectRemoveProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import gametypes
from uiProxy import UIProxy
from data import guild_building_marker_data as GBMD
from cdata import game_msg_def_data as GMDD

class GuildBuildSelectRemoveProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBuildSelectRemoveProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickBuildRemove': self.onClickBuildRemove}
        self.mediator = None
        self.areaId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BUILD_SELECT_REMOVE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_BUILD_SELECT_REMOVE:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BUILD_SELECT_REMOVE)

    def reset(self):
        self.areaId = 0

    def show(self, markerId):
        if not gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_BUILDING):
            BigWorld.player().showGameMsg(GMDD.data.GUILD_AUTHORIZATION_FAILED, ())
            return
        markerBaseData = GBMD.data.get(markerId, {})
        if not markerBaseData:
            return
        self.areaId = markerBaseData.get('panelAreaType', 0)
        if self.areaId in (uiConst.GUILD_BUILDING_PANEL_HOUSE1, uiConst.GUILD_BUILDING_PANEL_HOUSE2):
            if self.mediator:
                self.refreshInfo()
                self.mediator.Invoke('swapPanelToFront')
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BUILD_SELECT_REMOVE)
        else:
            gameglobal.rds.ui.guildBuildRemove.show(markerId)

    def refreshInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            if not guild:
                return
            if self.areaId not in (uiConst.GUILD_BUILDING_PANEL_HOUSE1, uiConst.GUILD_BUILDING_PANEL_HOUSE2):
                return
            guildBuildList = []
            for markerId in guild.marker.iterkeys():
                if self.areaId != GBMD.data.get(markerId, {}).get('panelAreaType', 0):
                    continue
                buildInfo = gameglobal.rds.ui.guild.createBuildInfo(markerId)
                if buildInfo:
                    guildBuildList.append(buildInfo)

            info = {}
            info['areaId'] = self.areaId
            info['guildBuildList'] = guildBuildList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onClickBuildRemove(self, *arg):
        markerId = int(arg[3][0].GetString())
        gameglobal.rds.ui.guildBuildRemove.show(markerId)
