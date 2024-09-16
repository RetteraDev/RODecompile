#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/schoolTopRuleProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy

class SchoolTopRuleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SchoolTopRuleProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SCHOOL_TOP_RULE, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SCHOOL_TOP_RULE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SCHOOL_TOP_RULE)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SCHOOL_TOP_RULE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        BigWorld.callback(0, self.delayInitUI)

    def delayInitUI(self):
        if not self.widget:
            return
        self.widget.historyList.canvas.contentText.htmlText = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' * 100
        self.widget.historyList.canvas.contentText.height = self.widget.historyList.canvas.contentText.textHeight + 10
        self.widget.historyList.refreshHeight(self.widget.historyList.canvas.contentText.height)

    def refreshInfo(self):
        if not self.widget:
            return
