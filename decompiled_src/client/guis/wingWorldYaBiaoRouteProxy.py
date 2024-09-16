#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldYaBiaoRouteProxy.o
import BigWorld
import wingWorldUtils
import uiConst
import events
import const
import gamelog
import utils
from helpers import navigator
from callbackHelper import Functor
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis import uiUtils
from data import wing_world_city_data as WWCD
from data import region_server_config_data as RSCD
from data import game_msg_data as GMD
from data import seeker_data as SD
from cdata import game_msg_def_data as GMDD
CITY_MAX_CNT = 15
GOTO_TYPE_NONE = 0
GOTO_TYPE_PORT = 1
GOTO_TYPE_NAVI = 2

class WingWorldYaBiaoRouteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldYaBiaoRouteProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_YABIAO_ROUTE, self.hide)

    def reset(self):
        self.selectedMc = None
        self.gotoType = GOTO_TYPE_NONE

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_YABIAO_ROUTE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_YABIAO_ROUTE)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_YABIAO_ROUTE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        ASUtils.setHitTestDisable(self.widget.txtTitle, True)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        p = BigWorld.player()
        cityIdx = 0
        for i in xrange(CITY_MAX_CNT):
            if not WWCD.data.get(i + 1, {}).get('canGoto', 1):
                continue
            else:
                cityIdx += 1
            cityMc = getattr(self.widget, 'city%d' % (cityIdx - 1))
            cityMc.visible = True
            cfgData = WWCD.data.get(i + 1, {})
            cityVal = p.wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, i + 1)
            cityOwner = utils.getCountryName(cityVal.ownerHostId) if cityVal.ownerHostId else gameStrings.WING_WORLD_CITY_NO_OWNER
            labels = [cfgData.get('name', ''), cfgData.get('level', ''), cityOwner]
            cityMc.data = i + 1
            cityMc.labels = labels
            cityMc.addEventListener(events.BUTTON_CLICK, self.handleButtonClick, False, 0, True)

        while cityIdx < CITY_MAX_CNT:
            cityMc = getattr(self.widget, 'city%d' % cityIdx)
            cityMc.visible = False
            cityIdx += 1

        self.widget.naviBtn.addEventListener(events.BUTTON_CLICK, self.handleNaviBtnClick, False, 0, True)
        self.widget.naviBtn.label = gameStrings.WING_WORLD_YABIAO_RETURN

    def handleNaviBtnClick(self, *args):
        p = BigWorld.player()
        neightborCityId = wingWorldUtils.getDefaultNeighborCityId(p.getOriginHostId())
        pos = WWCD.data.get(neightborCityId, {}).get('naviBornIslandPos', None)
        if pos:
            spaceNo = pos[-1]
            if p.canPathFindingWingWorld(spaceNo, False):
                from helpers import wingWorld
                wingWorld.pathFinding((pos[0],
                 pos[1],
                 pos[2],
                 spaceNo), endDist=0.5, showMsg=False, fromGroupFollow=False)
            else:
                navigator.getNav().pathFinding((pos[0],
                 pos[1],
                 pos[2],
                 spaceNo), None, None, True, 0.5, self.uiAdapter.map.onArrive)

    def handleButtonClick(self, *args):
        e = ASObject(args[3][0])
        gamelog.info('jbx:handleButtonClick', e.currentTarget.data)
        if self.selectedMc and self.selectedMc.data == e.currentTarget.data:
            return
        if self.selectedMc:
            self.selectedMc.selected = False
        self.selectedMc = e.currentTarget
        self.selectedMc.selected = True
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        selectedCityId = int(self.selectedMc.data) if self.selectedMc else 0
        self.widget.confirmBtn.label = gameStrings.WING_WORLD_NOT_CONNECTD
        self.gotoType = GOTO_TYPE_NAVI
        self.widget.confirmBtn.enabled = bool(selectedCityId)

    def handleConfirmBtnClick(self, *args):
        selectedCityId = int(self.selectedMc.data) if self.selectedMc else 0
        if selectedCityId:
            cityName = WWCD.data.get(selectedCityId, {}).get('name', '')
            if self.gotoType == GOTO_TYPE_NAVI:
                self.gotoNavigation(selectedCityId)
            else:
                msg = GMD.data.get(GMDD.data.WING_WORLD_YABIAO_PORT_CONFIRM, {}).get('text', '') % cityName
                self.uiAdapter.messageBox.showYesNoMsgBox(msg, Functor(self.gotoTransPort, selectedCityId))

    def gotoTransPort(self, cityId):
        seekId = WWCD.data.get(cityId, {}).get('seekId', 0)
        npcId = SD.data.get(seekId, {}).get('npcId', 0)
        BigWorld.player().cell.teleportToStone(npcId)
        gamelog.info('jbx:applySetWingWorldYabiaoDstCity', cityId)
        BigWorld.player().cell.applySetWingWorldYabiaoDstCity(cityId)
        self.hide()

    def gotoNavigation(self, cityId):
        seekId = WWCD.data.get(cityId, {}).get('seekId', '')
        uiUtils.findPosById(seekId)
        gamelog.info('jbx:applySetWingWorldYabiaoDstCity', cityId)
        BigWorld.player().cell.applySetWingWorldYabiaoDstCity(cityId)
        self.hide()
