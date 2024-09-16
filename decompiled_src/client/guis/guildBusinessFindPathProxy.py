#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBusinessFindPathProxy.o
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy
from data import seeker_data as SD
from data import guild_business_seeker_data as GBSD

class GuildBusinessFindPathProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBusinessFindPathProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BUSINESS_FIND_PATH, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_BUSINESS_FIND_PATH:
            self.mediator = mediator
            self.refreshInfo()

    def show(self):
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BUSINESS_FIND_PATH)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BUSINESS_FIND_PATH)

    def refreshInfo(self):
        if self.mediator:
            info = {}
            for key in uiConst.GUILD_BUSINESS_AREA:
                info['area%d' % key] = uiConst.GUILD_BUSINESS_AREA[key]

            locationList = []
            for value in GBSD.data.itervalues():
                itemInfo = {}
                seekList = []
                for seekId in value.get('seekId', ()):
                    seekData = SD.data.get(seekId, {})
                    seekInfo = {}
                    seekInfo['seekId'] = seekId
                    seekInfo['npcName'] = "<u><a href=\'event:seek:%s\'>%s</a></u>" % (seekId, seekData.get('name', ''))
                    seekInfo['tips'] = "%s<font color = \'#2E7339\'>(%s)</font>" % (gameglobal.rds.ui.questLog.getMapName(str(seekId)), gameglobal.rds.ui.questLog.getPosition(str(seekId)))
                    seekList.append(seekInfo)

                itemInfo['seekList'] = seekList
                itemInfo['area'] = value.get('area', 0)
                itemInfo['location'] = value.get('location', 0)
                itemInfo['locationDesc'] = value.get('locationDesc', '')
                locationList.append(itemInfo)

            info['locationList'] = locationList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
