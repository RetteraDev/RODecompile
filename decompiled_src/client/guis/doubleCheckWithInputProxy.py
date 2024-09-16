#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/doubleCheckWithInputProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
from guis import uiUtils
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class CallbackFunc(object):

    def __init__(self, confirmCallback = None, confirmCallbackArgs = (), cancelCallback = None, cancelCallbackArgs = (), confirmCallback1 = None):
        self.confirmCallback = confirmCallback
        self.cancelCallback = cancelCallback
        self.confirmCallback1 = confirmCallback1

    def confirm(self):
        gameglobal.rds.ui.doubleCheckWithInput.hide()
        if self.confirmCallback is None:
            return
        else:
            self.confirmCallback()
            return

    def cancel(self):
        gameglobal.rds.ui.doubleCheckWithInput.hide()
        if self.cancelCallback is None:
            return
        else:
            self.cancelCallback()
            return

    def confirm1(self):
        gameglobal.rds.ui.doubleCheckWithInput.hide()
        if self.confirmCallback1 is None:
            return
        else:
            self.confirmCallback1()
            return


class DoubleCheckWithInputProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DoubleCheckWithInputProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm,
         'getPanelInfo': self.onGetPanelInfo,
         'clickConfirm1': self.onClickConfirm1}
        self.reset()
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_DOUBLE_CHECK_WITH_INPUT, self.hide)

    def reset(self):
        super(self.__class__, self).reset()
        self.msg = ''
        self.title = ''
        self.checkLabel = ''
        self.callbackIns = None
        self.canEnter = True
        self.labels = ()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DOUBLE_CHECK_WITH_INPUT:
            self.mediator = mediator

    def onGetPanelInfo(self, *arg):
        info = {}
        info['msg'] = self.msg
        info['title'] = self.title
        info['checkLabel'] = self.checkLabel
        info['labels'] = self.labels
        info['canEnter'] = self.canEnter
        return uiUtils.dict2GfxDict(info, True)

    def show(self, msg, checkLabel, title = gameStrings.TEXT_QUESTPROXY_495, confirmCallback = None, confirmCallbackArgs = (), cancelCallback = None, cancelCallbackArgs = ()):
        if self.mediator:
            return
        if self.callbackIns:
            return
        self.labels = (gameStrings.TEXT_DOUBLECHECKWITHINPUTPROXY_87, gameStrings.TEXT_ITEMRESUMEPROXY_73)
        self.msg = "<font color = \'#FFFFE7\'> %s </font>" % (msg,) + "<font color = \'#F43804\'>%s</font>" % (checkLabel,)
        self.checkLabel = checkLabel
        self.title = title
        self.callbackIns = CallbackFunc(confirmCallback, confirmCallbackArgs, cancelCallback, cancelCallbackArgs)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DOUBLE_CHECK_WITH_INPUT, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DOUBLE_CHECK_WITH_INPUT)

    def onClickClose(self, *arg):
        if self.callbackIns:
            self.callbackIns.cancel()

    def onClickConfirm(self, *arg):
        if arg[3][0].GetString().lower() == self.checkLabel.lower():
            if self.callbackIns:
                self.callbackIns.confirm()
        else:
            BigWorld.player().showGameMsg(GMDD.data.DISCARD_WORD_WRONG, ())
            self.hide()

    def onClickConfirm1(self, *arg):
        if arg[3][0].GetString().lower() == self.checkLabel.lower():
            if self.callbackIns:
                self.callbackIns.confirm1()
        else:
            BigWorld.player().showGameMsg(GMDD.data.DISCARD_WORD_WRONG, ())
            self.hide()

    def show3ButtonCheck(self, msg, checkLabel, title = gameStrings.TEXT_QUESTPROXY_495, labels = (gameStrings.TEXT_DOUBLECHECKWITHINPUTPROXY_121, gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, gameStrings.TEXT_PLAYRECOMMPROXY_494_1), confirmCallback1 = None, confirmCallback = None, cancelCallback = None, canEnter = True):
        if self.mediator:
            return
        if self.callbackIns:
            return
        self.labels = labels
        self.msg = "<font color = \'#FFFFE7\'> %s </font>" % (msg,) + "<font color = \'#F43804\'>%s</font>" % (checkLabel,)
        self.checkLabel = checkLabel
        self.title = title
        self.canEnter = canEnter
        self.callbackIns = CallbackFunc(confirmCallback, (), cancelCallback, (), confirmCallback1)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DOUBLE_CHECK_WITH_INPUT, True)
