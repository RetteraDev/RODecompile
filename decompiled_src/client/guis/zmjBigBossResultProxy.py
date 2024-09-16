#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjBigBossResultProxy.o
import BigWorld
import utils
import gameglobal
import uiConst
from uiProxy import UIProxy
from data import zmj_fuben_config_data as ZFCD

class ZmjBigBossResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjBigBossResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZMJ_BIG_BOSS_RESULT_WIDGET, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZMJ_BIG_BOSS_RESULT_WIDGET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZMJ_BIG_BOSS_RESULT_WIDGET)

    def show(self, resultInfo):
        self.resultInfo = resultInfo
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZMJ_BIG_BOSS_RESULT_WIDGET)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.confirmBtn
        zmjDmg = self.resultInfo.get('zmjDmg', 0)
        zmjTime = self.resultInfo.get('zmjTime', 0)
        zmjMaxDayDmg = self.resultInfo.get('zmjMaxDayDmg', 0)
        self.widget.bossImage.icon.loadImage(ZFCD.data.get('bigBossResultPath', 'zmjactivity/bossicon/30005.dds'))
        self.widget.timeMc.timeTxt.text = utils.formatTimeStr(int(zmjTime), 'h:m:s', True, sNum=2, mNum=2, hNum=2)
        self.widget.dmgMc.dmgTxt.text = zmjDmg
        self.widget.topDmgMc.topDmgTxt.text = zmjMaxDayDmg

    def refreshInfo(self):
        if not self.widget:
            return
