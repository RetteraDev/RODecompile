#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTopFubenEvalProxy.o
import BigWorld
from guis import uiConst
from guis import uiUtils
from guis import menuManager
import events
from gamestrings import gameStrings
from uiProxy import UIProxy

class SchoolTopFubenEvalProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTopFubenEvalProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TOP_FUBEN_EVAL, self.hide)

    def reset(self):
        self.rank = 0
        self.dps = 0
        self.lastDps = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TOP_FUBEN_EVAL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TOP_FUBEN_EVAL)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FUBEN_EVAL_BG)

    def show(self, rank, dps, lastDps):
        if not self.widget:
            self.rank = rank
            self.dps = dps
            self.lastDps = lastDps
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TOP_FUBEN_EVAL)
            self.uiAdapter.loadWidget(uiConst.WIDGET_FUBEN_EVAL_BG)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.showRank.addEventListener(events.BUTTON_CLICK, self.handleShowRankClick, False, 0, True)
        self.widget.exitBtn.addEventListener(events.BUTTON_CLICK, self.handleExitBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.txtScore.text = self.dps
        self.widget.txtRank.text = self.rank
        self.widget.txtLastDps.htmlText = gameStrings.SCHOOL_TOP_DPS % uiUtils.toHtml(str(max(0, self.dps - self.lastDps)), '#74C424')

    def handleShowRankClick(self, *args):
        self.uiAdapter.rankCommon.showRankCommon(109)

    def handleExitBtnClick(self, *args):
        self.hide()
        menuManager.getInstance().leaveFuben()
