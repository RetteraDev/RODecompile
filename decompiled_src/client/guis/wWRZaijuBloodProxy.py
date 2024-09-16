#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wWRZaijuBloodProxy.o
import BigWorld
import gameglobal
import gametypes
import events
from guis import asObject
from guis import uiUtils
from guis import uiConst
from uiProxy import UIProxy
from gameStrings import gameStrings
HEIGHT_OFFSET = 2

class WWRZaijuBloodProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WWRZaijuBloodProxy, self).__init__(uiAdapter)
        self.widget = None
        self._zaijuEnt = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_WWR_ZAIJU_BLOOD, self.clearWidget)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initPanel()
        self.refreshPanel()

    def initPanel(self):
        self.widget.bloodShowPlane.visible = True
        self.widget.bloodHidePlane.visible = False
        self.widget.bloodShowPlane.minButton.addEventListener(events.MOUSE_CLICK, self.handleClickMin)
        self.widget.bloodHidePlane.addEventListener(events.MOUSE_CLICK, self.handleClickShow)

    def refreshPanel(self):
        self.addBloodItem()

    def clearBloodItem(self):
        bloodItem = self.widget.bloodShowPlane.getChildByName('zaijuEnt')
        self.widget.bloodShowPlane.removeChild(bloodItem)

    def addBloodItem(self):
        if not hasattr(self._zaijuEnt, 'hp'):
            self.clearWidget()
        if not self.widget:
            return
        bloodItem = self.widget.bloodShowPlane.getChildByName('zaijuEnt')
        if not bloodItem:
            bloodItem = self.widget.getInstByClsName('WWRZaijuBlood_GroupBlood_Item')
            bloodItem.name = 'zaijuEnt'
            bloodItem.x = 0
            bloodItem.y = self.widget.bloodShowPlane.minButton.height + HEIGHT_OFFSET
            bloodItem.addEventListener(events.MOUSE_CLICK, self.handleClickBloodItem)
            bloodItem.unused.visible = False
            bloodItem.selected.visible = False
            bloodItem.over.visible = False
            bloodItem.zaijuBlood.zaijuName.text = gameStrings.WWR_ZAIJU_NAME
            self.widget.bloodShowPlane.addChild(bloodItem)
        bloodValue = float(self._zaijuEnt.hp) / float(self._zaijuEnt.mhp) * 100
        bloodItem.zaijuBlood.zaijuBloodT.text = str('%.1f' % bloodValue) + '%'
        bloodItem.zaijuBlood.blood.currentValue = self._zaijuEnt.hp
        bloodItem.zaijuBlood.blood.maxValue = self._zaijuEnt.mhp

    def show(self, zaijuEnt = None):
        p = BigWorld.player()
        camp = p.worldWar.getCurrCamp()
        self._zaijuEnt = zaijuEnt
        if self.widget:
            self.refreshPanel()
        else:
            if camp == gametypes.WORLD_WAR_CAMP_ATTACK:
                return
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WWR_ZAIJU_BLOOD)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WWR_ZAIJU_BLOOD)
        self.widget = None
        self._zaijuEnt = None

    def handleClickBloodItem(self, *args):
        if self._zaijuEnt:
            uiUtils.onTargetSelect(self._zaijuEnt)

    def handleClickMin(self, *args):
        if self.widget:
            self.widget.bloodShowPlane.visible = False
            self.widget.bloodHidePlane.visible = True

    def handleClickShow(self, *args):
        if self.widget:
            self.widget.bloodShowPlane.visible = True
            self.widget.bloodHidePlane.visible = False
