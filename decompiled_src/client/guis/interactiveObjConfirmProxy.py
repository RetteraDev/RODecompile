#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/interactiveObjConfirmProxy.o
"""
Created on Jul 25, 2016
@author: wy1
"""
import gameglobal
import uiUtils
import uiConst
import keys
from uiProxy import UIProxy

class InteractiveObjConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InteractiveObjConfirmProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickEnterBtn': self.onClickEnterBtn,
         'clickCancelBtn': self.onClickCancelBtn}
        self.teamInfo = None
        self.confirmDetail = None
        self.callback = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_INTERACTIVE_CONFIRM, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        ret = {}
        ret['info'] = self.teamInfo
        ret['detail'] = self.confirmDetail
        return uiUtils.dict2GfxDict(ret, True)

    def setTeamInfo(self, info):
        self.teamInfo = info

    def setConfirmDetail(self, detail):
        self.confirmDetail = detail

    def setCallback(self, callback):
        self.callback = callback

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INTERACTIVE_CONFIRM)

    def onClickEnterBtn(self, *args):
        self.callback()
        self.clearWidget()

    def onClickCancelBtn(self, *args):
        self.clearWidget()

    def onClickKey(self, key):
        if key == keys.KEY_Y:
            self.onClickEnterBtn()
            return True
        if key == keys.KEY_N:
            self.onClickCancelBtn()
            return True

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INTERACTIVE_CONFIRM)
