#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpBattleRotationV2Proxy.o
from gamestrings import gameStrings
import uiConst
import events
from uiProxy import UIProxy
from data import duel_config_data as DCD
ROTATION_DATA = ({'day': gameStrings.TEXT_PVPBATTLEROTATIONV2PROXY_9,
  'time': '00:00~23:59',
  'name': gameStrings.TEXT_CONST_2968},
 {'day': gameStrings.TEXT_PVPBATTLEROTATIONV2PROXY_10,
  'time': '00:00~23:59',
  'name': gameStrings.TEXT_CONST_738},
 {'day': gameStrings.TEXT_PVPBATTLEROTATIONV2PROXY_11,
  'time': '00:00~23:59',
  'name': gameStrings.TEXT_CONST_2968},
 {'day': gameStrings.TEXT_PVPBATTLEROTATIONV2PROXY_12,
  'time': '00:00~23:59',
  'name': gameStrings.TEXT_CONST_738},
 {'day': gameStrings.TEXT_PVPBATTLEROTATIONV2PROXY_13,
  'time': '00:00~23:59',
  'name': gameStrings.TEXT_CONST_2968},
 {'day': gameStrings.TEXT_PVPBATTLEROTATIONV2PROXY_14,
  'time': '00:00~23:59',
  'name': gameStrings.TEXT_CONST_738},
 {'day': gameStrings.TEXT_PVPBATTLEROTATIONV2PROXY_15,
  'time': '00:00~23:59',
  'name': gameStrings.TEXT_CONST_2968})
ROTATION_MCS = ('Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')

class PvpBattleRotationV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpBattleRotationV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PVP_BATTLEROTATION_V2, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PVP_BATTLEROTATION_V2:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PVP_BATTLEROTATION_V2)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PVP_BATTLEROTATION_V2)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.okBtn.enabled = True
        self.widget.okBtn.addEventListener(events.BUTTON_CLICK, self.handleOkBtnClick, False, 0, True)
        self.initCycle()

    def initCycle(self):
        rotationData = DCD.data.get('pvpBattleSchedule', ROTATION_DATA)
        for i in xrange(7):
            data = rotationData[i]
            mc = self.widget.getChildByName(ROTATION_MCS[i])
            mc.text = data['day']
            time = self.widget.getChildByName('startTime%d' % i)
            time.text = data['time']
            name = self.widget.getChildByName('battleName%d' % i)
            name.text = data['name']

    def handleOkBtnClick(self, *args):
        self.clearWidget()

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type
