#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/gmMessageProxy.o
import base64
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy

class GmMessageProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GmMessageProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickConfirmBtn': self.onClickConfirmBtn,
         'initData': self.onInitData}
        self.mediator = None
        self.title = None
        self.desc = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SECRECY:
            self.mediator = mediator

    def show(self, title, desc):
        self.title = title
        self.desc = desc
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GM_MESSAGE, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GM_MESSAGE)

    def reset(self):
        super(self.__class__, self).reset()
        self.title = None
        self.desc = None

    def onInitData(self, *arg):
        try:
            title = base64.b64decode(self.title)
            desc = base64.b64decode(self.desc)
        except:
            title = self.title
            desc = self.desc

        data = [title, desc]
        return uiUtils.array2GfxAarry(data)

    def onClickConfirmBtn(self, *arg):
        self.hide()
