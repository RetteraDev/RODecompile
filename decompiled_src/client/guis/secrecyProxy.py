#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/secrecyProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
from appSetting import Obj as AppSettings
from ui import gbk2unicode
from uiProxy import UIProxy

class SecrecyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SecrecyProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickCancelBtn': self.onClickCancelBtn,
         'clickConfirmBtn': self.onClickConfirmBtn,
         'initData': self.onInitData}
        self.mediator = None
        self.version = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SECRECY:
            self.mediator = mediator

    def show(self, version):
        self.version = version
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SECRECY, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SECRECY)

    def reset(self):
        super(self.__class__, self).reset()
        self.version = None

    def onInitData(self, *arg):
        try:
            f = open('../license.txt')
            text = f.read()
            f.close()
        except IOError:
            text = gameStrings.TEXT_SECRECYPROXY_47

        return GfxValue(gbk2unicode(text))

    def onClickConfirmBtn(self, *arg):
        AppSettings['conf/version'] = self.version
        AppSettings.save()
        self.hide()
        gameglobal.rds.ui.loginWin.realShow()

    def onClickCancelBtn(self, *arg):
        BigWorld.quit()
