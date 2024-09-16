#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/innerIEProxy.o
import BigWorld
CEFModule = None
try:
    import CEFManager as CEFModule
except:
    CEFModule = None

import events
import uiConst
import gameglobal
from guis import uiUtils
import cefUIManager
from uiProxy import UIProxy
import gamelog
from guis.asObject import ASObject
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import ftb_config_data as FCD
from gamestrings import gameStrings

class InnerIEProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InnerIEProxy, self).__init__(uiAdapter)
        self.modelMap = {'getInitData': self.onGetInitData,
         'goForward': self.onGoForward,
         'goBack': self.onGoBack,
         'refresh': self.onRefresh,
         'notifyChange': self.onNotifyChange,
         'btnClick': self.onBtnClick,
         'enterFrame': self.onEnterFrame}
        uiAdapter.registerEscFunc(uiConst.WIDGET_IE, self.hide)
        self.reset()
        self.urlPath = None
        self.oldX = 0
        self.oldY = 0
        self.pngWidth = 400
        self.pngHeight = 300
        self.width = 400
        self.height = 300
        self.code = 3
        self.swfPath = 'gui/widgets/IEWidget' + uiAdapter.getUIExt()
        self.insName = 'IE_UnitIE'
        self.enableKeyEvent = False
        self.enableGoBack = False
        self.canGoBack = True
        self.bInput = False
        self.currentUrlPath = None
        self.alphaColor = -1
        self.urlChangeCallback = None
        self.skinType = uiConst.IE_SKIN_TYPE_NORMAL

    def show(self, urlPath = 'http://tianyu.163.com/index.html', code = 0, width = 640, height = 480, enableKeyEvent = False, canGoBack = True, enableGoBack = False, bInput = False, skinType = uiConst.IE_SKIN_TYPE_NORMAL, alphaColor = -1, urlChangeCallback = None):
        self.urlPath = urlPath
        self.currentUrlPath = urlPath
        isChange = self.width != width or self.height != height or self.skinType != skinType
        self.width = width
        self.height = height
        self.code = code
        self.enableKeyEvent = enableKeyEvent
        self.enableGoBack = enableGoBack
        self.canGoBack = canGoBack
        self.bInput = bInput
        self.alphaColor = -1
        self.urlChangeCallback = urlChangeCallback
        self.skinType = skinType
        if not CEFModule:
            return
        else:
            if not CEFModule.isCefProcessRunning():
                swShow = gameglobal.SW_HIDE if BigWorld.isPublishedVersion() else gameglobal.SW_SHOW
                CEFModule.openCefProcess(gameglobal.CEF_PROCESS_NAME, self.pngWidth, self.pngHeight, swShow)
            if not self.mediator:
                if not cefUIManager.getInstance().registerCefUI(uiConst.WIDGET_IE, closeFunc=None, forceOpen=True):
                    return
                self.uiAdapter.loadWidget(uiConst.WIDGET_IE)
            else:
                if isChange:
                    self.mediator.Invoke('initLayout')
                self.startPlay()
            return

    def getOffset(self):
        widget = self.mediator.Invoke('getWidget')
        widgetX = widget.GetMember('x').GetNumber()
        widgetY = widget.GetMember('y').GetNumber()
        iconX = widget.GetMember('picture').GetMember('x').GetNumber()
        iconY = widget.GetMember('picture').GetMember('y').GetNumber()
        scaleX, scaleY = self.getWidgetScale()
        return (int(iconX + widgetX * scaleX), int(iconY + widgetY * scaleY))

    def textureChangeCallback(self, width, height):
        self.refreshDrawToFlash()

    def startPlay(self):
        if self.urlPath:
            CEFModule.setConnBindedCallback(self.connectionBindedCallback)
            CEFModule.setTextureChangeCallback(self.textureChangeCallback)
            self.refreshDrawToFlash()
            self.oldX, self.oldY = self.getOffset()
            CEFModule.initImgBuff()
            CEFModule.setPosition(self.oldX, self.oldY)
            CEFModule.setScale(self.width / 400.0, self.height / 300.0)
            CEFModule.resize(self.width, self.height)
            CEFModule.setVisible(True)
            CEFModule.loadURL(self.urlPath)
            CEFModule.resize(self.width, self.height)
            CEFModule.setCefRequestCallback(self.handleCEFRequest)

    def refreshDrawToFlash(self):
        CEFModule.resize(self.width, self.height)
        CEFModule.drawToFlash(self.swfPath, self.insName, 0, 0, self.pngWidth, self.pngHeight)

    def connectionBindedCallback(self, bind):
        CEFModule.loadURL(self.urlPath)
        CEFModule.resize(self.width, self.height)
        self.refreshDrawToFlash()

    def handleCEFRequest(self, request, requestLen):
        self.currentUrlPath = request
        if self.urlChangeCallback:
            self.urlChangeCallback(request, requestLen)

    def onURLChange(self, urlPath):
        if self.code == uiConst.IE_FORBID_TRANSFER:
            self.onGoBack()
        elif self.code == uiConst.IE_ONLY_TRANSFER_TY:
            if urlPath.find('tianyu.163.com') == -1:
                self.onGoBack()
        self.currentUrlPath = urlPath
        if self.urlChangeCallback:
            self.urlChangeCallback(urlPath)

    def loadUrl(self, url):
        CEFModule.loadURL(url)
        CEFModule.resize(self.width, self.height)

    def getWidgetScale(self):
        widget = self.mediator.Invoke('getWidget')
        scaleX = widget.GetMember('scaleX').GetNumber()
        scaleY = widget.GetMember('scaleY').GetNumber()
        return (scaleX, scaleY)

    def reset(self):
        self.mediator = None

    def clearWidget(self):
        cefUIManager.getInstance().unregisterCefUI(uiConst.WIDGET_IE)
        CEFModule.setVisible(False)
        CEFModule.setPosition(0, 0)
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_IE)
        self.urlPath = None
        self.enableGoBack = False
        self.enableKeyEvent = False
        self.canGoBack = True
        gameglobal.rds.ui.bInput = False
        self.currentUrlPath = None
        if self.urlChangeCallback:
            gameglobal.rds.ui.dispatchEvent(events.EVENT_INNER_IE_HIDE)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_IE:
            self.mediator = mediator
            self.startPlay()

    def setVisible(self, visible):
        if self.mediator:
            self.mediator.Invoke('getWidget').SetVisible(visible)

    def onGetInitData(self, *arg):
        ret = {'width': self.width,
         'height': self.height,
         'type': self.skinType}
        return uiUtils.dict2GfxDict(ret)

    def onGoForward(self, *arg):
        CEFModule.goForward()

    def onGoBack(self, *arg):
        CEFModule.goBack()

    def onRefresh(self, *arg):
        self.loadUrl(self.currentUrlPath)

    def onEnterFrame(self, *arg):
        x = int(arg[3][0].GetNumber())
        y = int(arg[3][1].GetNumber())
        self.setCEFPosition(x, y)

    def setCEFPosition(self, x, y):
        topWidgetId = self.uiAdapter.getTopWidgetId()[0]
        if topWidgetId != uiConst.WIDGET_IE:
            x, y = BigWorld.getScreenSize()
        if self.oldX != x or self.oldY != y:
            CEFModule.setPosition(x, y)
            self.oldX = x
            self.oldY = y

    def onNotifyChange(self, *arg):
        x = int(arg[3][0].GetNumber())
        y = int(arg[3][1].GetNumber())
        w = int(arg[3][2].GetNumber())
        h = int(arg[3][3].GetNumber())
        self.setCEFPosition(x, y)
        CEFModule.setScale(w / 400.0, h / 300.0)
        if self.width != w or self.height != h:
            self.show(self.urlPath, self.code, w, h, self.enableKeyEvent, self.canGoBack, self.enableGoBack, self.bInput, self.skinType, self.alphaColor, self.urlChangeCallback)

    def onBtnClick(self, *args):
        btnName = args[3][0].GetString()
        if btnName == 'addTimeBtn':
            gameglobal.rds.ui.ftbAddTime.show()
