#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qrCodeInstallAPPProxy.o
import uiConst
from uiProxy import UIProxy

class QrCodeInstallAPPProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QrCodeInstallAPPProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_TIANYU_APP_QRCODE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TIANYU_APP_QRCODE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TIANYU_APP_QRCODE)

    def show(self):
        if self.widget:
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_TIANYU_APP_QRCODE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        pass
