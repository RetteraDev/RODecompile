#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/playTipsProxy.o
from Scaleform import GfxValue
import gameglobal
import uiConst
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import UIProxy

class PlayTipsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PlayTipsProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_PLAYTIPS:
            self.mediator = mediator

    def show(self, str, time):
        if self.uiAdapter.isHideAllUI():
            return
        else:
            if self.mediator != None:
                str = uiUtils.generateStr(str)
                self.mediator.Invoke('setVisible', GfxValue(True))
                self.mediator.Invoke('showPlayTips', (GfxValue(gbk2unicode(str)), GfxValue(time)))
            return

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PLAYTIPS)
