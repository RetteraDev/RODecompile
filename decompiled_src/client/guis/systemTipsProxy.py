#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/systemTipsProxy.o
from Scaleform import GfxValue
import gameglobal
import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy
from helpers import loadingProgress

class SystemTipsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SystemTipsProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SYSTEMTIPS:
            self.mediator = mediator

    def show(self, str, forceShow = False):
        if loadingProgress.instance().visible:
            return
        elif gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            return
        else:
            if not gameglobal.rds.configData.get('enableNewCamera', False):
                if gameglobal.rds.ui.camera.isShow and not forceShow:
                    return
            elif gameglobal.rds.ui.cameraV2.isShow and not forceShow:
                return
            if self.mediator != None:
                self.mediator.Invoke('setVisible', GfxValue(True))
                self.mediator.Invoke('showSystemTips', GfxValue(gbk2unicode(str)))
            return

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SYSTEMTIPS)
