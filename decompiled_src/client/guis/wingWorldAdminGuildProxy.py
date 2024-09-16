#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldAdminGuildProxy.o
import BigWorld
import const
import uiConst
import wingWorldUtils
from uiProxy import UIProxy

class WingWorldAdminGuildProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldAdminGuildProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_ADMIN_GUILD, self.hide)

    def reset(self):
        self.cityId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_ADMIN_GUILD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_ADMIN_GUILD)

    def show(self, cityId):
        if not cityId:
            if self.widget:
                return
            return
        self.cityId = cityId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_ADMIN_GUILD)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        city = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, self.cityId)
        adminGuildmap = city.adminGuildMap
        typeAList = []
        typeBList = []
        typeCList = []
        for guldNuild, val in adminGuildmap.iteritems():
            level = wingWorldUtils.calcCityAdminLevel(val.rank)
            level == const.WING_WORLD_ADMIN_GUILD_LEVEL_1 and typeAList.append(val)
            level == const.WING_WORLD_ADMIN_GUILD_LEVEL_2 and typeBList.append(val)
            level == const.WING_WORLD_ADMIN_GUILD_LEVEL_3 and typeCList.append(val)

        lenA = len(typeAList)
        lenB = len(typeBList)
        lenC = len(typeCList)
        typeAList.sort(cmp=lambda a, b: cmp(a.rank, b.rank))
        typeBList.sort(cmp=lambda a, b: cmp(a.rank, b.rank))
        typeCList.sort(cmp=lambda a, b: cmp(a.rank, b.rank))
        for i in xrange(wingWorldUtils.getCityAdminGuildLevelCnt(const.WING_WORLD_ADMIN_GUILD_LEVEL_1)):
            textMc = self.widget.getChildByName('typeA%d' % i)
            if i < lenA:
                textMc.text = typeAList[i].guildName
            else:
                textMc.text = ''

        for i in xrange(wingWorldUtils.getCityAdminGuildLevelCnt(const.WING_WORLD_ADMIN_GUILD_LEVEL_2)):
            textMc = self.widget.getChildByName('typeB%d' % i)
            if not textMc:
                continue
            if i < lenB:
                textMc.text = typeBList[i].guildName
            else:
                textMc.text = ''

        for i in xrange(wingWorldUtils.getCityAdminGuildLevelCnt(const.WING_WORLD_ADMIN_GUILD_LEVEL_3)):
            textMc = self.widget.getChildByName('typeC%d' % i)
            if not textMc:
                continue
            if i < lenC:
                textMc.text = typeCList[i].guildName
            else:
                textMc.text = ''
