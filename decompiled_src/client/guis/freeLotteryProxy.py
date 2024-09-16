#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/freeLotteryProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
from uiProxy import UIProxy
from data import sys_config_data as SCD
URL_PATH = 'http://m3.rrzcp8.com/activity/group/viewPage.html?activityId=tgnty'

class FreeLotteryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FreeLotteryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.testId = '123@163.com'
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FREE_LOTTERY, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FREE_LOTTERY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FREE_LOTTERY)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FREE_LOTTERY)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        iconPath = 'freeLottery/%s.dds' % SCD.data.get('freeLotteryIconPath', 'test')
        self.widget.bgIcon.fitSize = True
        self.widget.bgIcon.loadImage(iconPath)
        self.widget.bgIcon.addEventListener(events.MOUSE_CLICK, self.handleGotoClick, False, 0, True)
        self.widget.timeDesc.htmlText = SCD.data.get('freeLotteryDesc', '')
        self.widget.gotoBtn.addEventListener(events.BUTTON_CLICK, self.handleGotoClick, False, 0, True)
        self.widget.helpIcon.visible = False

    def refreshInfo(self):
        if not self.widget:
            return

    def handleGotoClick(self, *args):
        gamelog.info('jbx:handleGotoClick', self.testId)
        BigWorld.player().base.commitWebLotteryExchange()

    def openUrl(self):
        gamelog.info('jbx:openUrl', URL_PATH)
        BigWorld.openUrl(URL_PATH)
