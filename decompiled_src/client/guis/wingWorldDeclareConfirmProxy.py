#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldDeclareConfirmProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
import gamelog
import utils
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import region_server_config_data as RSCD
from data import wing_world_city_data as WWCD
from data import wing_world_config_data as WWCFD

class WingWorldDeclareConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldDeclareConfirmProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_DECLARE_CONFIM, self.hide)

    def reset(self):
        self.targetCityId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_DECLARE_CONFIM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_DECLARE_CONFIM)

    def show(self, targetCityId):
        self.targetCityId = targetCityId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_DECLARE_CONFIM)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.yesBtn.addEventListener(events.BUTTON_CLICK, self.handelYesBtnClick, False, 0, True)
        self.widget.noBtn.addEventListener(events.BUTTON_CLICK, self.handleNoBtnClick, False, 0, True)
        self.widget.txt0.visible = False
        for i in xrange(3):
            getattr(self.widget, 'iconCost%d' % i).visible = False
            getattr(self.widget, 'txtCost%d' % i).visible = False

    def handelYesBtnClick(self, *args):
        gamelog.info('jbx:handelYesBtnClick')
        BigWorld.player().cell.wingWorldDeclare(self.targetCityId)
        self.hide()

    def handleNoBtnClick(self, *args):
        gamelog.info('jbx:handelNoBtnClick')
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.txtCityName.text = WWCD.data.get(self.targetCityId, {}).get('name', '')
        cityLevel = WWCD.data.get(self.targetCityId, {}).get('level', 1)
        self.widget.txtLv.text = WWCFD.data.get('cityLevelDesc', {}).get(cityLevel, str(cityLevel))
        p = BigWorld.player()
        ownerHosdId = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, self.targetCityId).ownerHostId
        countryName = utils.getCountryName(ownerHosdId)
        desc = gameStrings.WING_WORLD_CAMP_DESC_NAME if p.isWingWorldCampMode() else gameStrings.WING_WORLD_COUNTRY_NAME
        self.widget.txtCountryName.text = desc % countryName if countryName else gameStrings.WING_WORLD_COUNTRY_NAME_NONE
