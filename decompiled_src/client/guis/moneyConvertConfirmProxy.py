#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/moneyConvertConfirmProxy.o
import gameglobal
import uiConst
from ui import gbk2unicode
from uiProxy import UIProxy
from Scaleform import GfxValue
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class MoneyConvertConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MoneyConvertConfirmProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickConfirm': self.onClickConfirm,
         'getData': self.onGetData,
         'cancel': self.onCancel}
        self.mediator = None
        self.isSelected = False
        self.yesCallback = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_MONEY_CONVERT_COMFIRM:
            self.mediator = mediator

    def show(self, yesCallback, isModal = False):
        self.yesCallback = yesCallback
        if not self.mediator:
            if not self.isSelected:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MONEY_CONVERT_COMFIRM, isModal=isModal)
            else:
                self.yesCallback()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MONEY_CONVERT_COMFIRM)

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.yesCallback = None

    def onClickConfirm(self, *arg):
        self.isSelected = arg[3][0].GetBool()
        self.yesCallback()
        self.hide()

    def doYes(self):
        self.mediator.Invoke('doConfirm', ())

    def onGetData(self, *arg):
        return GfxValue(gbk2unicode(GMD.data.get(GMDD.data.BINDCASH_IS_NOT_ENOUGH, {}).get('text')))

    def onCancel(self, *arg):
        self.hide()
