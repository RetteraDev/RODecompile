#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/exactQteProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from ui import gbk2unicode
import hotkey as HK
from callbackHelper import Functor
from data import qte_data as QTED

class ExactQteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ExactQteProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'qteSuccess': self.onQteSuccess,
         'qteFail': self.onQteFail}
        self.mediator = None
        self.qteId = None
        self.qteResult = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EXACT_QTE:
            self.mediator = mediator

    def setData(self, msg, timeOut):
        self.msg, self.msgExtra = self._formatstr(msg)
        self.timeOut = timeOut

    def _formatstr(self, m):
        if m is None:
            return
        else:
            data = m.split('$')
            msgExtra = (data[0], data[-1])
            ret = []
            for item in data[1:-1]:
                if item.find(',') != -1:
                    t = eval(item)
                    if t[0] == uiConst.USE_TIPS_TYPE_KEY:
                        detial = HK.HKM[t[1]]
                        keyName = detial.getDesc()
                        if not keyName:
                            keyName = detial.getDesc(2)
                        ret.append(keyName)
                else:
                    ret.append(item)

            return (''.join(ret), msgExtra)

    def show(self, id):
        if self.mediator:
            self.hide(False)
        self.qteId = id
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EXACT_QTE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EXACT_QTE)

    def reset(self):
        super(self.__class__, self).reset()
        if self.qteId:
            if QTED.data[self.qteId].get('hideUI', 0):
                gameglobal.rds.ui.setQTEHideUI(False)
            gameglobal.rds.ui.inQTE = False
        self.qteId = None
        self.msg = None
        self.timeOut = None
        self.qteResult = None

    def onInitData(self, *arg):
        movie = arg[0]
        obj = movie.CreateObject()
        if self.qteId:
            qteData = QTED.data.get(self.qteId, {})
            obj.SetMember('exactDev', GfxValue(qteData['exactDev']))
            obj.SetMember('interval', GfxValue(qteData['interval']))
            obj.SetMember('exactTime', GfxValue(qteData['exactTime']))
            obj.SetMember('desc', GfxValue(''))
        elif self.msg:
            obj.SetMember('exactDev', GfxValue(0))
            obj.SetMember('interval', GfxValue(0))
            obj.SetMember('exactTime', GfxValue(self.timeOut))
            obj.SetMember('desc', GfxValue(gbk2unicode(self.msg)))
            obj.SetMember('descExtra', uiUtils.array2GfxAarry(self.msgExtra, True))
        if self.qteResult != None:
            BigWorld.callback(0.1, Functor(self.onTutorialEnd, self.qteResult))
        return obj

    def onQteSuccess(self, *arg):
        BigWorld.player().uploadQTEInfo(self.qteId, True)
        self.reset()

    def onQteFail(self, *arg):
        BigWorld.player().uploadQTEInfo(self.qteId, False)
        self.reset()

    def onTutorialEnd(self, success = True):
        if self.mediator:
            self.mediator.Invoke('tutorialEnd', GfxValue(success))
        else:
            self.qteResult = success
