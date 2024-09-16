#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/shaXingProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
from ui import gbk2unicode
from guis import uiConst
from guis import uiUtils
from uiProxy import DataProxy
from data import sys_config_data as SCD
TYPE_WAIT = 0
TYPE_NOT_CHOOSE = 1

class ShaXingProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(ShaXingProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeResult': self.onCloseResult,
         'closeWaitWidget': self.onCloseWaitWidget}
        self.type = 'shaXing'
        self.mediator = None
        self.waitMed = None
        self.isWin = False
        self.seconds = 0
        self.type = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SHA_XING_RESULT:
            self.mediator = mediator
            self.playResult(self.isWin)
        elif widgetId == uiConst.WIDGET_SHA_XING_WAIT:
            self.waitMed = mediator
            waitText = SCD.data.get('shaXingWaitMsg', gameStrings.TEXT_SHAXINGPROXY_38)
            notChooseText = SCD.data.get('shaXingchooseGroupFailMsg', gameStrings.TEXT_SHAXINGPROXY_39)
            ret = {'type': self.type,
             'seconds': self.seconds,
             'waitText': waitText,
             'notChooseText': notChooseText}
            return uiUtils.dict2GfxDict(ret, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()

    def closeWaitWidget(self):
        if self.type == TYPE_WAIT:
            self.waitMed = None
            self.type = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHA_XING_WAIT)

    def closeNotChooseWidget(self):
        self.waitMed = None
        self.type = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHA_XING_WAIT)

    def showWait(self, seconds, waitText):
        self.seconds = seconds
        self.type = TYPE_WAIT
        if self.waitMed:
            ret = {'seconds': self.seconds,
             'waitText': waitText}
            self.waitMed.Invoke('playWait', uiUtils.dict2GfxDict(ret, True))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SHA_XING_WAIT)
        BigWorld.callback(seconds, self.closeWaitWidget)

    def showNotChoose(self, msg):
        self.type = TYPE_NOT_CHOOSE
        if self.waitMed:
            self.waitMed.Invoke('playNotChoosed', GfxValue(gbk2unicode(msg)))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SHA_XING_WAIT)

    def showShaXingResult(self, isWin):
        self.isWin = isWin
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SHA_XING_RESULT)

    def onCloseResult(self, *arg):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHA_XING_RESULT)

    def onCloseWaitWidget(self, *arg):
        self.waitMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHA_XING_WAIT)

    def playResult(self, isWin):
        if self.mediator:
            if isWin:
                self.mediator.Invoke('playWin')
            else:
                self.mediator.Invoke('playDefeat')
