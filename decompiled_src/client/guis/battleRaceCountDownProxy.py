#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/battleRaceCountDownProxy.o
import BigWorld
import gameglobal
import uiConst
from helpers import tickManager
from uiProxy import UIProxy
from data import battle_field_data as BFD
from gamestrings import gameStrings

class BattleRaceCountDownProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BattleRaceCountDownProxy, self).__init__(uiAdapter)
        self.widget = None
        self.tickId = 0
        self.reset()

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BATTLE_RACE_COUNT_DOWN:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = 0
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BATTLE_RACE_COUNT_DOWN)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BATTLE_RACE_COUNT_DOWN)

    def formateTime(self, time):
        minute = int(time / 60)
        sec = time - minute * 60
        return '%02d:%02d' % (minute, sec)

    def refreshTimer(self):
        p = BigWorld.player()
        if not p.bfTimeRec or not p.bfTimeRec.has_key('tReady'):
            self.widget.countDownMc.visible = False
        else:
            self.widget.countDownMc.visible = True
            totalTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
            countTime = max(totalTime - (p.getServerTime() - p.bfTimeRec['tReady']), 0)
            self.widget.countDownMc.countDownTime.time.textField.text = self.formateTime(countTime)

    def initUI(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = tickManager.addTick(1, self.refreshTimer)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.countDownMc.wave.text = gameStrings.BATTLE_RACE_COUNTDOWN_TEXT
