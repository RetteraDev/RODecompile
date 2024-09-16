#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaSignalProxy.o
import BigWorld
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from data import duel_config_data as DCD
SIGNAL_TYPE_FRAME_MAP = {uiConst.SIGNAL_TYPE_GATHER: 'gather',
 uiConst.SIGNAL_TYPE_ATK: 'atk',
 uiConst.SIGNAL_TYPE_RETREAT: 'retreat',
 uiConst.SIGNAL_TYPE_DEFENCE: 'defence'}

class BfDotaSignalProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaSignalProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.timer = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BF_DOTA_SIGNAL:
            self.widget = widget
            self.widget.visible = False

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_DOTA_SIGNAL)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_SIGNAL)

    def refreshSignalInfo(self, gbId, type):
        p = BigWorld.player()
        if not self.widget:
            return
        if type not in SIGNAL_TYPE_FRAME_MAP:
            return
        self.widget.visible = True
        self.widget.mainMC.gotoAndPlay(1)
        iconPath = uiUtils.getZaijuLittleHeadIconPathById(p.bfDotaZaijuRecord.get(gbId, 0))
        frameLabel = SIGNAL_TYPE_FRAME_MAP[type]
        self.widget.mainMC.photo.icon.fitSize = True
        self.widget.mainMC.photo.icon.loadImage(iconPath)
        self.widget.mainMC.iconMC.gotoAndStop(frameLabel)
        self.widget.mainMC.iconMC2.gotoAndStop(frameLabel)
        self.widget.mainMC.txtMC.gotoAndStop(frameLabel)
        self.widget.mainMC.txtMC2.gotoAndStop(frameLabel)
        BigWorld.callback(DCD.data.get('bfDotaSignalShowTime', 3), self.setVisibleFalse)

    def setVisibleFalse(self):
        if self.widget:
            self.widget.visible = False

    def test(self):
        p = BigWorld.player()
        for i in xrange(5):
            p.bfDotaZaijuRecord[i] = 10000 + i
            type = i % 3 + 1
            self.addSignalInfo(i, type)
