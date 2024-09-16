#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/mallWebProxy.o
import BigWorld
CEFModule = None
try:
    import CEFManager as CEFModule
except:
    CEFModule = None

import gameglobal
import uiConst
import clientcom
import cefUIManager
from helpers import CEFControl
from uiProxy import UIProxy
from data import sys_config_data as SCD

class MallWebProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MallWebProxy, self).__init__(uiAdapter)
        self.modelMap = {'enterFrame': self.onEnterFrame}
        self.mediator = None
        self.width = 1000
        self.height = 600
        self.swfPath = 'gui/widgets/MallWebWidget' + uiAdapter.getUIExt()
        self.insName = 'unitWebMall'
        self.oldX = 0
        self.oldY = 0
        self.url = SCD.data.get('MALL_WEB_URL', '')
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MALL_WEB, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MALL_WEB:
            self.mediator = mediator
            self.startPlay()

    def reset(self):
        self.preUrl = ''

    def clearWidget(self):
        cefUIManager.getInstance().unregisterCefUI(uiConst.WIDGET_MALL_WEB)
        CEFModule.setVisible(False)
        CEFModule.setPosition(0, 0)
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MALL_WEB)

    def canShow(self):
        if not gameglobal.rds.configData.get('enableShowMallWeb', 0):
            return False
        return True

    def show(self):
        if not self.canShow():
            return
        if not CEFModule:
            return
        if not CEFModule.isCefProcessRunning():
            swShow = gameglobal.SW_HIDE if BigWorld.isPublishedVersion() else gameglobal.SW_SHOW
            CEFModule.openCefProcess(gameglobal.CEF_PROCESS_NAME, self.width, self.height, swShow)
        if not cefUIManager.getInstance().registerCefUI(uiConst.WIDGET_MALL_WEB, closeFunc=self.hide, forceOpen=True):
            return
        if self.mediator:
            self.startPlay()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MALL_WEB)

    def getWidgetScale(self):
        widget = self.mediator.Invoke('getWidget')
        scaleX = widget.GetMember('scaleX').GetNumber()
        scaleY = widget.GetMember('scaleY').GetNumber()
        return (scaleX, scaleY)

    def getOffset(self):
        widget = self.mediator.Invoke('getWidget')
        widgetX = widget.GetMember('x').GetNumber()
        widgetY = widget.GetMember('y').GetNumber()
        iconX = widget.GetMember('picture').GetMember('x').GetNumber()
        iconY = widget.GetMember('picture').GetMember('y').GetNumber()
        scaleX, scaleY = self.getWidgetScale()
        return (int(iconX + widgetX * scaleX), int(iconY + widgetY * scaleY))

    def startPlay(self):
        CEFModule.setConnBindedCallback(self.connectionBindedCallback)
        CEFModule.setTextureChangeCallback(self.textureChangeCallback)
        self.refreshDrawToFlash()
        self.oldX, self.oldY = self.getOffset()
        CEFModule.initImgBuff()
        CEFModule.setPosition(self.oldX, self.oldY)
        CEFModule.resize(self.width, self.height)
        CEFModule.setVisible(True)
        CEFModule.loadURL(self.url)
        CEFModule.setCefRequestCallback(self.handleCEFRequest)

    def onEnterFrame(self, *args):
        x, y = self.getOffset()
        if self.oldX != x or self.oldY != y:
            CEFModule.setPosition(x, y)
            self.oldX = x
            self.oldY = y
            scale = CEFControl.getDPIScale()
            scaleX, scaleY = self.getWidgetScale()
            CEFModule.setScale(scaleX / scale, scaleY / scale)

    def refreshDrawToFlash(self):
        CEFModule.drawToFlash(self.swfPath, self.insName, 0, 0, self.width, self.height)

    def textureChangeCallback(self, width, height):
        self.refreshDrawToFlash()

    def connectionBindedCallback(self, bind):
        CEFModule.loadURL(self.url)
        CEFModule.resize(self.width, self.height)
        self.refreshDrawToFlash()

    def handleCEFRequest(self, request, requestLen):
        if len(request) != requestLen:
            return
        if request == self.url:
            self.url = request
            return
        index = request.find('mallId=')
        if index != -1:
            mallId = 0
            if index != -1:
                try:
                    mallId = int(request[index + 7:])
                except:
                    pass

                gameglobal.rds.ui.tianyuMall.mallBuyConfirm(mallId, 1, 'mallWeb.0')
                CEFModule.loadURL(self.preUrl)
        elif request.find('http://gift.163.com/product_dtl') != -1:
            clientcom.openFeedbackUrl(request)
            CEFModule.loadURL(self.preUrl)
        else:
            self.preUrl = request
