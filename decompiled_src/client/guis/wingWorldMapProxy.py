#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldMapProxy.o
import BigWorld
import gameglobal
import wingWorldUtils
from gamestrings import gameStrings
import uiConst
import events
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis import uiUtils
from uiProxy import UIProxy
from data import wing_world_city_data as WWCTD
from data import seeker_data as SD
from data import wing_world_country_title_data as WWCTTD
from data import region_server_config_data as RSCD
CITY_MAX_CNT = 15
MAP_STATE_EXPAND = 1
MAP_STATE_NOT_EXPAND = 2

class WingWorldMapProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldMapProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.dstCityId = 0
        self.state = MAP_STATE_EXPAND
        self.selectedCityId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_MAP, self.hide)

    def reset(self):
        self.mapIconList = []
        self.selectedIconMc = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_MAP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_MAP)

    def show(self):
        if not gameglobal.rds.configData.get('enableWingWorldMap', False):
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_MAP)
            p = BigWorld.player()
            p.cell.queryWingWorldResume(p.wingWorld.state, p.wingWorld.briefVer, p.wingWorld.countryVer, p.wingWorld.cityVer, p.wingWorld.campVer)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.hideMc.addEventListener(events.MOUSE_CLICK, self.handleHideMcClick, False, 0, True)
        for i in xrange(CITY_MAX_CNT):
            textMc = getattr(self.widget, 'txtCity%d' % (i + 1))
            ASUtils.setHitTestDisable(textMc, True)
            textMc.text = WWCTD.data.get(i + 1, {}).get('name', '  ')[:2]
            cityMc = getattr(self.widget, 'ciyt%d' % (i + 1))
            ASUtils.setHitTestDisable(cityMc, True)

        selfCountryColor, alpah = RSCD.data.get(BigWorld.player().getOriginHostId(), {}).get('wingWorldCountryColor', ('FFFFFF', 0.5))
        ASUtils.addColorMask(self.widget.countryColor, selfCountryColor, alpah)

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshExpandState()

    def refreshSelected(self):
        if not self.widget:
            return
        if not self.selectedCityId:
            self.widget.gotoAndStop('normal')
        else:
            self.widget.gotoAndStop('selected')
            p = BigWorld.player()
            if wingWorldUtils.getCityOwnerHostId(self.selectedCityId) == p.getOriginHostId():
                self.widget.naviBtn.visible = True
                self.widget.transBtn.visible = True
                self.widget.onlyNaviBtn.visible = False
            else:
                self.widget.naviBtn.visible = False
                self.widget.transBtn.visible = False
                self.widget.onlyNaviBtn.visible = True
            self.widget.naviBtn.addEventListener(events.BUTTON_CLICK, self.handleNaviBtnClick, False, 0, True)
            self.widget.onlyNaviBtn.addEventListener(events.BUTTON_CLICK, self.handleNaviBtnClick, False, 0, True)
            self.widget.transBtn.addEventListener(events.BUTTON_CLICK, self.handleTransBtnClick, False, 0, True)
            self.widget.txtCityName.text = WWCTD.data.get(self.selectedCityId, {}).get('name', '')

    def refreshExpandState(self):
        if not self.widget:
            return
        if self.state == MAP_STATE_NOT_EXPAND:
            self.widget.hideMc.gotoAndStop('left')
        else:
            self.widget.hideMc.gotoAndStop('right')
        for childIdx in xrange(self.widget.numChildren):
            mc = self.widget.getChildAt(childIdx)
            if mc.name != 'hideMc':
                mc.visible = self.state == MAP_STATE_EXPAND

        if self.state == MAP_STATE_EXPAND:
            self.refreshSelected()
            self.refreshCityMap()

    def getButtonTips(self, cityId):
        ownerHostId = wingWorldUtils.getCityOwnerHostId(cityId)
        p = BigWorld.player()
        if ownerHostId:
            country = p.wingWorld.country.getCountry(ownerHostId)
            countryLevel = WWCTTD.data.get(country.titleLevel, {}).get('titleName', '')
            countryName = RSCD.data.get(ownerHostId, {}).get('serverName', '')
            leaderName = p.wingWorld.getCityKingName(ownerHostId)
            return gameStrings.WING_WORLD_MAP_TIPS % (countryLevel, countryName, leaderName)
        else:
            return ''

    def refreshCityMap(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            for iconMc in self.mapIconList:
                self.widget.removeChild(iconMc)

            self.mapIconList = []
            for cityId, cfgData in WWCTD.data.iteritems():
                iconMc = None
                cityMc = self.widget.getChildByName('city%d' % cityId)
                ownerHostId = wingWorldUtils.getCityOwnerHostId(cityId)
                if ownerHostId:
                    iconMc = self.widget.getInstByClsName('WingWorldMap_Button%d' % RSCD.data.get(ownerHostId, {}).get('iconType', 1))
                    TipManager.addTip(iconMc, self.getButtonTips(cityId))
                else:
                    iconMc = self.widget.getInstByClsName('WingWorldMap_Button7')
                    TipManager.removeTip(iconMc)
                iconMc.self.visible = cityId == p.getWingCityId()
                self.widget.addChild(iconMc)
                if cityId == self.selectedCityId:
                    if self.selectedIconMc:
                        self.selectedIconMc.selected = False
                    iconMc.selected = True
                    self.selectedIconMc = iconMc
                else:
                    iconMc.selected = False
                iconMc.name = 'city%d' % cityId
                iconMc.data = cityId
                self.mapIconList.append(iconMc)
                pos = cfgData.get('expandMapPos', cfgData.get('pos'))
                iconMc.x = pos[0] / 600.0 * 300
                iconMc.y = pos[1] / 540.0 * 300
                iconMc.addEventListener(events.MOUSE_CLICK, self.handleIconClick, False, 0, True)
                if not ownerHostId:
                    cityMc.visible = False
                else:
                    cityMc.visible = True
                    color, alpha = RSCD.data.get(ownerHostId, {}).get('wingWorldCountryColor', ('ffffff', 0.5))
                    ASUtils.addColorMask(cityMc, color, alpha)

            return

    def handleIconClick(self, *args):
        e = ASObject(args[3][0])
        cityId = int(e.currentTarget.data)
        if cityId != self.selectedCityId:
            if self.selectedIconMc:
                self.selectedIconMc.selected = False
            self.selectedCityId = cityId
            self.selectedIconMc = e.currentTarget
            self.selectedIconMc.selected = True
            self.refreshSelected()

    def handleHideMcClick(self, *args):
        if self.state == MAP_STATE_NOT_EXPAND:
            self.state = MAP_STATE_EXPAND
        else:
            self.state = MAP_STATE_NOT_EXPAND
        self.refreshExpandState()

    def getSeekId(self):
        return WWCTD.data.get(self.selectedCityId, {}).get('mapSeekId', WWCTD.data.get(self.selectedCityId, {}).get('seekId', 0))

    def handleNaviBtnClick(self, *args):
        uiUtils.findPosById(self.getSeekId())

    def handleTransBtnClick(self, *args):
        npcId = SD.data.get(self.getSeekId(), {}).get('npcId', 0)
        BigWorld.player().cell.teleportToStone(npcId)
