#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/flashProxy.o
import BigWorld
import uiConst
import clientUtils
from uiProxy import UIProxy

class FlashProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FlashProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_PLYAY_FLASH, self.hide)
        self.reset()
        self.flash = None
        self.urlPath = None
        self.width = 400
        self.height = 300
        self.swfPath = 'gui/widgets/FlashWidget' + uiAdapter.getUIExt()
        self.insName = 'unitFlash'

    def show(self, urlPath):
        self.urlPath = urlPath
        if not self.mediator:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PLYAY_FLASH)
        else:
            self.startPlay()

    def startPlay(self):
        if self.urlPath:
            try:
                self.flash = BigWorld.PyFlash(self.urlPath)
                self.flash.drawToFlash(self.swfPath, self.insName, self.width, self.height)
            except Exception as e:
                clientUtils.reportEngineException(e.message)

    def reset(self):
        self.mediator = None

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PLYAY_FLASH)
        self.urlPath = None
        self.flash = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PLYAY_FLASH:
            self.mediator = mediator
            self.startPlay()
