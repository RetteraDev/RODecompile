#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tutorialQteProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
from guis import uiConst
from guis import uiUtils
from uiProxy import UIProxy
import hotkey as HK
from callbackHelper import Functor
from data import qte_data as QTED

class TutorialQteProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TutorialQteProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'qteSuccess': self.onQteSuccess,
         'qteFail': self.onQteFail}
        self.mediator = None
        self.qteId = None
        self.qteResult = None

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def setData(self, msg, timeOut):
        self.msg, self.msgExtra = self._formatstr(msg)
        self.timeOut = timeOut

    def _formatstr(self, m):
        if m is None:
            return
        else:
            data = m.split('$')
            msgExtra = data[1]
            ret = []
            if data[0].find(',') != -1:
                t = eval(data[0])
                if t[0] == uiConst.USE_TIPS_TYPE_KEY:
                    keyType, keyName = self._getKeyName(t[1])
                    ret.append(keyType)
                    ret.append(keyName)
            return (ret, msgExtra)

    def _getKeyName(self, key):
        detial = HK.HKM[key]
        keyName = detial.getBrief()
        if not keyName:
            keyName = detial.getBrief(2)
        keyType = 'common'
        if keyName[:2] == 'S+':
            keyType = 'Shift'
            if keyName == 'S+S':
                keyName = ''
            else:
                keyName = keyName[2:]
        elif keyName[:2] == 'C+':
            keyType = 'Ctrl'
            if keyName == 'C+C':
                keyName = ''
            else:
                keyName = keyName[2:]
        elif keyName[:2] == 'A+':
            keyType = 'Alt'
            if keyName == 'A+A':
                keyName = ''
            else:
                keyName = keyName[2:]
        return (keyType, keyName)

    def show(self, id):
        if self.mediator:
            self.hide(False)
        self.qteId = id
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TUTORIAL_QTE)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TUTORIAL_QTE)

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
        ret = {}
        ret['exactDev'] = 0
        ret['interval'] = 0
        ret['exactTime'] = self.timeOut
        ret['desc'] = self.msg
        ret['descExtra'] = self.msgExtra
        if self.qteResult != None:
            BigWorld.callback(0.1, Functor(self.onTutorialEnd, self.qteResult))
        return uiUtils.dict2GfxDict(ret, True)

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
