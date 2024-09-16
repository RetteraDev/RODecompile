#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/celebrityGloryPalaceProxy.o
import BigWorld
CEFModule = None
try:
    import CEFManager as CEFModule
except:
    CEFModule = None

import gameglobal
import uiConst
import events
import cefUIManager
from helpers import CEFControl
from uiProxy import UIProxy
from data import hall_of_fame_config_data as HOFCD

class CelebrityGloryPalaceProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CelebrityGloryPalaceProxy, self).__init__(uiAdapter)
        self.widget = None
        self.width = 776
        self.height = 377
        self.swfPath = 'gui/widgets/CelebrityGloryPalaceWidget' + uiAdapter.getUIExt()
        self.insName = 'CelebrityGloryPalace_celebrity_unitWeb'
        self.oldX = 0
        self.oldY = 0
        self.url = HOFCD.data.get('gloryWebUrl', '')
        uiAdapter.registerEscFunc(uiConst.WIDGET_CELEBRITY_GLORY, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CELEBRITY_GLORY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        cefUIManager.getInstance().unregisterCefUI(uiConst.WIDGET_CELEBRITY_GLORY)
        CEFModule.setVisible(False)
        CEFModule.setPosition(0, 0)
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CELEBRITY_GLORY)

    def show(self):
        if not gameglobal.rds.configData.get('enableHallOfFame', False):
            self.hide()
            return
        if not CEFModule:
            return
        if not CEFModule.isCefProcessRunning():
            swShow = gameglobal.SW_HIDE if BigWorld.isPublishedVersion() else gameglobal.SW_SHOW
            CEFModule.openCefProcess(gameglobal.CEF_PROCESS_NAME, self.width, self.height, swShow)
        if not cefUIManager.getInstance().registerCefUI(uiConst.WIDGET_CELEBRITY_GLORY, closeFunc=self.hide, forceOpen=True):
            return
        if self.widget:
            self.startPlay()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CELEBRITY_GLORY)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.startPlay()

    def startPlay(self):
        CEFModule.setConnBindedCallback(self.connectionBindedCallback)
        CEFModule.setTextureChangeCallback(self.textureChangeCallback)
        self.refreshDrawToFlash()
        self.oldX = int(self.widget.x + self.widget.picture.x)
        self.oldY = int(self.widget.y + self.widget.picture.y)
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)
        CEFModule.initImgBuff()
        CEFModule.setPosition(self.oldX, self.oldY)
        CEFModule.resize(self.width, self.height)
        CEFModule.setVisible(True)
        CEFModule.loadURL(self.url)
        CEFModule.setCefRequestCallback(self.handleCEFRequest)

    def handleCEFRequest(self, request, requestLen):
        pass

    def onEnterFrame(self, *args):
        x = int(self.widget.x + self.widget.picture.x * self.widget.scaleX)
        y = int(self.widget.y + self.widget.picture.y * self.widget.scaleY)
        if self.oldX != x or self.oldY != y:
            CEFModule.setPosition(x, y)
            self.oldX = x
            self.oldY = y
            scale = CEFControl.getDPIScale()
            CEFModule.setScale(self.widget.scaleX / scale, self.widget.scaleY / scale)

    def refreshDrawToFlash(self):
        CEFModule.drawToFlash(self.swfPath, self.insName, 0, 0, self.width, self.height)

    def textureChangeCallback(self, width, height):
        self.refreshDrawToFlash()

    def connectionBindedCallback(self, bind):
        CEFModule.loadURL(self.url)
        CEFModule.resize(self.width, self.height)
        self.refreshDrawToFlash()
