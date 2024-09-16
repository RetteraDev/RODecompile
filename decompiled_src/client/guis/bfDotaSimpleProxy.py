#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaSimpleProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import utils
import const
from uiProxy import UIProxy
from guis import ui

class BfDotaSimpleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaSimpleProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.enterBFTimeStamp = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_BF_DOTA_SIMPLE, self.hide)

    def reset(self):
        self.timer = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BF_DOTA_SIMPLE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            self.updateTime()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_DOTA_SIMPLE)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_SIMPLE)

    def initUI(self):
        self.widget.mainMc.iconKill.gotoAndStop('kill')
        self.widget.mainMc.iconDeath.gotoAndStop('death')
        self.widget.mainMc.iconAssist.gotoAndStop('assist')
        self.widget.mainMc.iconLastHit.gotoAndStop('lastHit')

    @ui.callInCD(0.2)
    @ui.uiEvent(uiConst.WIDGET_BF_DOTA_SIMPLE, events.EVNET_BF_DUEL_STATE_CHAGNE)
    def refreshInfo(self, event = None):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.mainMc.selfSideKill.text = str(p.getBfOwnStas(const.BF_DOTA_OWN_STATS_MYSIDE_KILL_TYPE))
        self.widget.mainMc.enemySideKill.text = str(p.getBfOwnStas(const.BF_DOTA_OWN_STATS_OTHERSIDE_KILL_TYPE))
        self.widget.mainMc.txtKill.text = str(p.getBfOwnStas(const.BF_DOTA_OWN_STATS_KILL_TYPE))
        self.widget.mainMc.txtDeath.text = str(p.getBfOwnStas(const.BF_DOTA_OWN_STATS_DIE_TYPE))
        self.widget.mainMc.txtAssist.text = str(p.getBfOwnStas(const.BF_DOTA_OWN_STATS_ASSIST_TYPE))
        self.widget.mainMc.txtLastHit.text = str(getattr(p, 'battleFieldDotaTotalCash', 0))

    def updateTime(self):
        if not self.widget:
            return
        pastTime = utils.getNow() - self.enterBFTimeStamp
        self.widget.mainMc.txtTime.text = utils.formatTimeStr(pastTime, 'm:s', sNum=2, mNum=2, zeroShow=True)
        self.timer = BigWorld.callback(1, self.updateTime)
