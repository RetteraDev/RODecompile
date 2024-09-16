#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fengyinShowProxy.o
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
from data import sys_config_data as SCD
WING_WORLD_URL_PATH = 'https://ty.163.com/2018/clientpppup_fyzl/index.html?worldId=1'

class FengyinShowProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FengyinShowProxy, self).__init__(uiAdapter)
        self.widget = None
        self.width = 720
        self.height = 544
        self.swfPath = 'gui/widgets/FengyinShowWidget' + uiAdapter.getUIExt()
        self.insName = 'FengyinShow_unitWeb'
        self.oldX = 0
        self.oldY = 0
        self.url = ''
        self.mapId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FENGYIN_SHOW, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FENGYIN_SHOW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        cefUIManager.getInstance().unregisterCefUI(uiConst.WIDGET_FENGYIN_SHOW)
        CEFModule.setVisible(False)
        CEFModule.setPosition(0, 0)
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FENGYIN_SHOW)

    def reset(self):
        self.mapId = 0

    def show(self, mapId):
        if not CEFModule:
            return
        if not CEFModule.isCefProcessRunning():
            swShow = gameglobal.SW_HIDE if BigWorld.isPublishedVersion() else gameglobal.SW_SHOW
            CEFModule.openCefProcess(gameglobal.CEF_PROCESS_NAME, self.width, self.height, swShow)
        if not cefUIManager.getInstance().registerCefUI(uiConst.WIDGET_FENGYIN_SHOW, closeFunc=self.hide):
            return
        self.mapId = mapId
        if self.widget:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FENGYIN_SHOW)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.mainMc.closeBtn
        self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if p.inWingCity():
            self.url = WING_WORLD_URL_PATH
        else:
            self.url = '%s%s' % (SCD.data.get('yazhiweburl', ''), str(self.mapId))
        self.startPlay()

    def startPlay(self):
        CEFModule.setConnBindedCallback(self.connectionBindedCallback)
        CEFModule.setTextureChangeCallback(self.textureChangeCallback)
        self.refreshDrawToFlash()
        self.oldX = int(self.widget.x + self.widget.mainMc.picture.x)
        self.oldY = int(self.widget.y + self.widget.mainMc.picture.y)
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
        x = int(self.widget.x + self.widget.mainMc.picture.x * self.widget.scaleX)
        y = int(self.widget.y + self.widget.mainMc.picture.y * self.widget.scaleY)
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
