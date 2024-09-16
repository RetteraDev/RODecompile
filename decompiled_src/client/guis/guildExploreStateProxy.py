#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildExploreStateProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from data import guild_area_data as GARD

class GuildExploreStateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildExploreStateProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_EXPLORE_AREA, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_EXPLORE_AREA:
            self.mediator = mediator
            self.refreshInfo()

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_EXPLORE_AREA)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_EXPLORE_AREA)

    def refreshInfo(self):
        if self.mediator:
            guild = BigWorld.player().guild
            info = {}
            for areaValue in guild.area.itervalues():
                areaId = areaValue.areaId
                baseinfo = GARD.data.get(areaId, {})
                info['titleField%d' % areaId] = gameStrings.TEXT_GUILDEXPLORESTATEPROXY_39 % baseinfo.get('name', '')
                if baseinfo.get('open', 0) == 0:
                    info['valueField%d' % areaId] = gameStrings.TEXT_GUILDEXPLORESTATEPROXY_41
                elif areaValue.isExtFinished():
                    info['valueField%d' % areaId] = gameStrings.TEXT_GUILDEXPLORESTATEPROXY_43
                elif guild.level < baseinfo.get('level', 0):
                    info['valueField%d' % areaId] = gameStrings.TEXT_GUILDEXPLORESTATEPROXY_45 % baseinfo.get('level', 0)
                else:
                    info['valueField%d' % areaId] = '%d/%d' % (areaValue.ext, baseinfo.get('ext', 0))

            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
