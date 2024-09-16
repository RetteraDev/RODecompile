#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldCreatePointProxy.o
import BigWorld
import uiConst
import gameglobal
import events
from uiProxy import UIProxy
from guis.asObject import ASObject
from data import wing_world_city_data as WWCD
CITY_MAP_ICON_PATH = 'wingWorld/ctiyMapIcon/%d.dds'

class WingWorldCreatePointProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldCreatePointProxy, self).__init__(uiAdapter)
        self.widget = None
        self.entityNo = 0
        self.selectedItem = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_CREATE_POINT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_CREATE_POINT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_CREATE_POINT)

    def reset(self):
        self.entityNo = 0
        self.selectedItem = None

    def show(self):
        if not gameglobal.rds.configData.get('enableWingWorld', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_WING_CREATE_POINT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        bornPointEntNo = gameglobal.rds.ui.wingWorldCarrierNarrow.bornPointEntNo
        if bornPointEntNo:
            self.entityNo = bornPointEntNo
        else:
            self.entityNo = p.wingWorldMiniMap.hostMinMap.defaultReliveBoardEntNo
        cityId = p.getWingWarCityId()
        cityInfo = WWCD.data.get(cityId, {})
        ctiyMapIcon = cityInfo.get('cityMapIcon', 0)
        self.widget.ctiyIcon.fitSize = True
        self.widget.ctiyIcon.loadImage(CITY_MAP_ICON_PATH % ctiyMapIcon)
        bornPoints = cityInfo.get('bornPoints', {})
        selfHostId = p.getOriginHostId()
        if p.isWingWorldCampMode():
            selfHostId = p.wingWorldCamp
        buildDic = p.wingWorldMiniMap.buildDic
        for entityNo, pos in bornPoints.iteritems():
            if entityNo in buildDic and buildDic[entityNo].ownHostId == selfHostId:
                pointBtn = self.widget.getInstByClsName('WingWorldCreatePoint_createPoint')
                pointBtn.selected = False
                self.widget.addChild(pointBtn)
                pointBtn.x = pos[0]
                pointBtn.y = pos[1]
                if entityNo == self.entityNo:
                    pointBtn.selected = True
                    self.selectedItem = pointBtn
                pointBtn.entityNo = entityNo
                pointBtn.addEventListener(events.BUTTON_CLICK, self.handlePointBtnClick, False, 0, True)

    def _onSureBtnClick(self, e):
        p = BigWorld.player()
        ver = gameglobal.rds.ui.wingWorldCarrierNarrow.getCarrierVersion()
        p.cell.setWingWorldWarCarrierBornPoint(self.entityNo, ver)
        self.hide()

    def handlePointBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        if self.entityNo and self.entityNo == itemMc.entityNo:
            return
        if self.selectedItem:
            self.selectedItem.selected = False
        itemMc.selected = True
        self.entityNo = itemMc.entityNo
        self.selectedItem = itemMc
