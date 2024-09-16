#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBuildSelectProxy.o
import BigWorld
import gameglobal
import uiUtils
import uiConst
import commGuild
from uiProxy import UIProxy
from data import guild_building_data as GBD
from data import guild_building_upgrade_data as GBUD
from data import guild_building_marker_data as GBMD

class GuildBuildSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBuildSelectProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.markerId = 0
        self.buildingNUID = 0
        self.npcId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BUILD_SELECT, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_BUILD_SELECT:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BUILD_SELECT)

    def _getBuilding(self):
        if self.buildingNUID:
            return BigWorld.player().guild.building.get(self.buildingNUID)
        else:
            return None

    def _updateBuildingNUID(self):
        if self.markerId:
            marker = BigWorld.player().guild.marker.get(self.markerId)
            if marker:
                self.buildingNUID = marker.buildingNUID

    def show(self, markerId = 0, buildingNUID = 0, npcId = 0):
        self.markerId = markerId
        self.buildingNUID = buildingNUID
        self.npcId = npcId
        self._updateBuildingNUID()
        building = self._getBuilding()
        if not building and commGuild.isMultiBuildingMarker(self.markerId):
            if self.mediator:
                self.refreshInfo()
                self.mediator.Invoke('swapPanelToFront')
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BUILD_SELECT)
        else:
            gameglobal.rds.ui.guildBuildUpgrade.show(self.markerId, self.buildingNUID, self.npcId)

    def refreshInfo(self):
        if self.mediator:
            buildingIds = GBMD.data.get(self.markerId, {}).get('buildingId', None)
            if isinstance(buildingIds, tuple) and len(buildingIds) > 1:
                info = {}
                buildingId = buildingIds[0]
                baseData = GBD.data.get(buildingId, {})
                info['iconLeft'] = 'guildBuildUpgrade/%d.dds' % GBUD.data.get((buildingId, 1), {}).get('icon', 100)
                info['nameLeft'] = baseData.get('name', '')
                info['descriptionLeft'] = baseData.get('description', '')
                info['buildingIdLeft'] = buildingIds[0]
                buildingId = buildingIds[1]
                baseData = GBD.data.get(buildingId, {})
                info['iconRight'] = 'guildBuildUpgrade/%d.dds' % GBUD.data.get((buildingId, 1), {}).get('icon', 100)
                info['nameRight'] = baseData.get('name', '')
                info['descriptionRight'] = baseData.get('description', '')
                info['buildingIdRight'] = buildingIds[1]
                self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        buildingId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.guildBuildUpgrade.show(self.markerId, self.buildingNUID, self.npcId, buildingId)
        self.hide()
