#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cbgRuleProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import cbg_config_data as CCD
from guis import cbgUtils
import gamelog

class CbgRuleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CbgRuleProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CBG_RULE, self.hide)

    def reset(self):
        self.title = ''
        self.content = ''
        self.confirmCallback = None
        self.type = cbgUtils.CBG_RULE_TYPE_REGIST

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CBG_RULE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CBG_RULE)
        self.reset()

    def show(self, type, confirmCallback = None):
        self.type = type
        self.confirmCallback = confirmCallback
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CBG_RULE, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmClick, False, 0, True)
        self.widget.scrollWnd.barAlwaysVisible = True

    def refreshInfo(self):
        if not self.widget:
            return
        if self.type == cbgUtils.CBG_RULE_TYPE_REGIST:
            title = CCD.data.get('roleRegistRuleTitle', '')
            content = CCD.data.get('roleRegistRuleText', '')
        elif self.type == cbgUtils.CBG_RULE_TYPE_SALE:
            title = CCD.data.get('roleSellRuleTitle', '')
            content = CCD.data.get('roleSellRuleText', '')
        elif self.type == cbgUtils.CBG_RULE_TYPE_REGIST_SIMPLE:
            title = CCD.data.get('roleRegistRuleTitleSimple', '')
            content = CCD.data.get('roleRegistRuleTextSimple', '')
        elif self.type == cbgUtils.CBG_RULE_TYPE_SALE_SIMPLE:
            title = CCD.data.get('roleSellRuleTitleSimple', '')
            content = CCD.data.get('roleSellRuleTextSimple', '')
        else:
            return
        self.widget.title.txt.text = title
        minHeight = self.widget.scrollWnd.canvasMask.height
        self.widget.scrollWnd.canvas.explain.htmlText = content
        self.widget.scrollWnd.canvas.explain.height = max(self.widget.scrollWnd.canvas.explain.textHeight, minHeight)
        self.widget.scrollWnd.refreshHeight(self.widget.scrollWnd.canvas.explain.height)

    def handleConfirmClick(self, *args):
        gamelog.debug('ypc@ cbgRule handleConfirmClick!', self.confirmCallback)
        if self.confirmCallback:
            self.confirmCallback()
        self.hide()
