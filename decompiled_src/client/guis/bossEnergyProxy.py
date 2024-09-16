#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bossEnergyProxy.o
import BigWorld
import gameglobal
import gametypes
import uiUtils
import uiConst
import events
import const
import utils
from guis.asObject import TipManager
from uiProxy import UIProxy
from callbackHelper import Functor
from guis import ui
from guis.asObject import ASObject

class BossEnergyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BossEnergyProxy, self).__init__(uiAdapter)
        self.xOffset = 0
        self.yOffset = 30
        self.originLocation = [0, 0]
        self.bossID2Data = {}
        self.bossIDArray = []
        self.count = 0

    @ui.scenarioCallFilter()
    def show(self, bossID, energyName, energyColor, initMp):
        multiID = self.uiAdapter.loadWidget(uiConst.WIDGET_BOSS_ENERGY)
        self.bossID2Data[str(bossID)] = {'multiID': multiID,
         'energyName': energyName,
         'energyColor': energyColor,
         'initMp': initMp,
         'widget': None}

    def _registerASWidget(self, widgetId, widget):
        for key, value in self.bossID2Data.iteritems():
            if widget.multiID == value.get('multiID', 0):
                value['widget'] = widget
                widget.energyName.text = value.get('energyName', '')
                cf = widget.enegyProgress.bar.transform.colorTransform
                cf.color = value.get('energyColor', '')
                widget.enegyProgress.bar.transform.colorTransform = cf
                widget.enegyProgress.currentValue = value.get('initMp', 0)
                if self.bossIDArray.count(None) == 0:
                    self.bossIDArray.append(str(key))
                else:
                    index = self.bossIDArray.index(None)
                    self.bossIDArray[index] = str(key)
                if self.count == 0:
                    widget.addEventListener(events.EVENT_WIDGET_REFLOWED, self.recordLocation, False, 0, True)
                else:
                    widget.addEventListener(events.EVENT_WIDGET_REFLOWED, self.updatePosition, False, 0, True)
                self.count = self.count + 1
                break

    def recordLocation(self, *args):
        widget = ASObject(args[3][0]).currentTarget
        self.originLocation = [widget.x, widget.y]

    def updatePosition(self, *args):
        widget = ASObject(args[3][0]).currentTarget
        bossID = ''
        for key, value in self.bossID2Data.iteritems():
            temp = value.get('widget', None)
            if temp and temp == widget:
                bossID = key

        index = self.bossIDArray.index(bossID)
        widget.x = self.originLocation[0] + index * self.xOffset
        widget.y = self.originLocation[1] + index * self.yOffset

    def hideUI(self, bossID):
        multiID = self.bossID2Data.get(str(bossID), {}).get('multiID', None)
        if not multiID:
            return
        else:
            if str(bossID) in self.bossIDArray:
                index = self.bossIDArray.index(str(bossID))
                self.bossIDArray[index] = None
            del self.bossID2Data[str(bossID)]
            self.count = self.count - 1
            self.uiAdapter.unLoadWidget(multiID)
            return

    def setEnergy(self, bossID, mpPresent):
        widget = self.bossID2Data.get(str(bossID), {}).get('widget', None)
        if not widget or not widget.enegyProgress:
            return
        else:
            widget.enegyProgress.currentValue = mpPresent
            return
