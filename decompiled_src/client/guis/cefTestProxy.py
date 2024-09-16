#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cefTestProxy.o
import BigWorld
import CEFManager
import gamelog
import gameglobal
import events
from guis.asObject import ASObject
from uiProxy import UIProxy
from guis import uiConst
from helpers import CEFControl
SPRITTE_HEIGHT = 24

class CefTestProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CefTestProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CEF_TEST, self.onClose)
        self.width = 1105
        self.height = 623
        self.swfPath = 'gui/widgets/CefTestWidget' + uiAdapter.getUIExt()
        self.insName = 'CefTest_unit4d'
        self.oldX = 0
        self.oldY = 0
        self.url = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CEF_TEST:
            self.widget = widget
            self.initUI()

    def refreshDrawToFlash(self):
        CEFManager.drawToFlash(self.swfPath, self.insName, 0, 0, self.width, self.height)

    def onClose(self, *arg):
        self.hide()

    def textureChangeCallback(self, width, height):
        self.refreshDrawToFlash()

    def connectionBindedCallback(self, bind):
        gamelog.debug('m.l@CefTestProxy.connectionBindedCallback', bind)
        CEFManager.loadURL(self.url)
        CEFManager.resize(self.width, self.height)
        self.refreshDrawToFlash()

    def clearWidget(self):
        self.widget = None
        CEFManager.setVisible(False)
        CEFManager.setPosition(0, 0)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CEF_TEST)
        self.reset()

    def show(self, url):
        self.url = url
        CEFManager.setConnBindedCallback(self.connectionBindedCallback)
        CEFManager.setTextureChangeCallback(self.textureChangeCallback)
        if not CEFManager.isCefProcessRunning():
            swShow = gameglobal.SW_HIDE if BigWorld.isPublishedVersion() else gameglobal.SW_SHOW
            CEFManager.openCefProcess(gameglobal.CEF_PROCESS_NAME, self.width, self.height, swShow)
        CEFManager.resize(self.width, self.height)
        self.reset()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CEF_TEST)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.refreshDrawToFlash()
        self.oldX = int(self.widget.x + self.widget.photo.x)
        self.oldY = int(self.widget.y + self.widget.photo.y)
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)
        if hasattr(CEFManager, 'initImgBuff'):
            CEFManager.initImgBuff()
        CEFManager.setPosition(self.oldX, self.oldY)
        CEFManager.resize(self.width, self.height)
        CEFManager.setVisible(True)
        CEFManager.loadURL(self.url)
        self.widget.goBackBtn.addEventListener(events.BUTTON_CLICK, self.handleGoBackClick, False, 0, True)
        self.widget.goForwardBtn.addEventListener(events.BUTTON_CLICK, self.handleGoForwadClick, False, 0, True)
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshClick, False, 0, True)
        self.widget.gotoBtn.addEventListener(events.BUTTON_CLICK, self.handleGotoClick, False, 0, True)
        self.widget.resizeBtn.addEventListener(events.BUTTON_CLICK, self.handleResizeClick, False, 0, True)
        if hasattr(CEFManager, 'setCefRequestCallback'):
            CEFManager.setCefRequestCallback(CEFControl.handleCEFRequest)

    def handleGoBackClick(self, *args):
        e = ASObject(args[3][0])
        CEFManager.goBack()

    def handleGoForwadClick(self, *args):
        CEFManager.goForward()

    def handleRefreshClick(self, *args):
        CEFManager.refresh()

    def handleGotoClick(self, *args):
        url = self.widget.urlInput.text
        CEFManager.loadURL(url)
        gamelog.debug('m.l@CefTestProxy.handleGotoClick', url)

    def handleResizeClick(self, *args):
        width = int(self.widget.widthInput.text)
        height = int(self.widget.heightInput.text)
        self.resize(width, height)

    def resize(self, width, height):
        self.width = width
        self.height = height
        CEFManager.resize(self.width, self.height)
        gamelog.debug('m.l@CefTestProxy.resize', width, height)

    def getDPIScale(self):
        if 'win10' in BigWorld.getOSDesc().lower() or 'win8' in BigWorld.getOSDesc().lower():
            return BigWorld.getScreenDPI()[0] / 96.0
        return 1.0

    def onEnterFrame(self, *args):
        x = int(self.widget.x + self.widget.photo.x * self.widget.scaleX)
        y = int(self.widget.y + self.widget.photo.y * self.widget.scaleY)
        if self.oldX != x or self.oldY != y:
            CEFManager.setPosition(x, y)
            self.oldX = x
            self.oldY = y
            scale = self.getDPIScale()
            CEFManager.setScale(self.widget.scaleX / scale, self.widget.scaleY / scale)

    def reset(self):
        pass
