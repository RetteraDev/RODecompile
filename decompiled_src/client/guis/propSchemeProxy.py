#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/propSchemeProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import uiUtils
import const
import time
from ui import unicode2gbk
from uiProxy import UIProxy
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD

class PropSchemeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PropSchemeProxy, self).__init__(uiAdapter)
        self.modelMap = {'closePanel': self.onClosePanel,
         'getPropSchemes': self.onGetPropSchemes,
         'usePropScheme': self.onUsePropScheme,
         'getCurrentSchemeNum': self.getCurrentSchemeNum,
         'buyScheme': self.buyScheme,
         'setSchemeName': self.setSchemeName}
        self.mediator = None
        self.resetMediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_PROP_SCHEME, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        BigWorld.player().registerEvent(const.EVENT_UPDATE_PROP_SCHEME, self.onPropSchemeChange)

    def onPropSchemeChange(self, params):
        data = self.onGetPropSchemes(None)
        self.mediator.Invoke('setPropSchemes', data)

    def getCurrentSchemeNum(self, *args):
        return GfxValue(BigWorld.player().curPropScheme)

    def buyScheme(self, *args):
        idx = int(args[3][0].GetNumber())
        if idx == 1 or idx == 2:
            gameglobal.rds.ui.propSchemeResume.show(idx)
        else:
            gameglobal.rds.ui.tianyuMall.showMallTab(10001, 0)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_PROP_SCHEME)
        if BigWorld.player():
            if BigWorld.player().__class__.__name__ == 'PlayerAvatar':
                BigWorld.player().unRegisterEvent(const.EVENT_UPDATE_PROP_SCHEME, self.onPropSchemeChange)

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_PROP_SCHEME)

    def onClosePanel(self, *arg):
        self.hide()

    def onGetPropSchemes(self, *arg):
        p = BigWorld.player()
        now = p.getServerTime()
        scheme = p.getAllPropScheme()
        for i in xrange(4):
            if scheme.has_key(i):
                scheme[i]['nowTime'] = now
                if scheme[i]['expireTime']:
                    scheme[i]['expireTimeText'] = time.strftime('%Y.%m.%d  %H:%M', time.localtime(scheme[i]['expireTime']))
                else:
                    scheme[i]['expireTimeText'] = ''

        return uiUtils.dict2GfxDict(scheme, True)

    def onUsePropScheme(self, *arg):
        idx = int(arg[3][0].GetNumber())
        if idx == BigWorld.player().curPropScheme:
            self.clearWidget()
            return
        if BigWorld.player().checkSchemeOutOfDate(idx) == True:
            msg = uiUtils.getTextFromGMD(GMDD.data.SCHEME_SWITCH_OVERDUE, '')
            gameglobal.rds.ui.messageBox.showMsgBox(msg)
            scheme = BigWorld.player().getPropSchemeById(idx)
            BigWorld.player().dispatchEvent(const.EVENT_UPDATE_PROP_SCHEME, (idx, scheme))
            return
        if self.checkIsInAdd():
            msg = uiUtils.getTextFromGMD(GMDD.data.CHECK_PROP_NEED_SAVE, gameStrings.TEXT_PROPSCHEMEPROXY_102)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.trueConfirmAndSave, idx), yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noCallback=Functor(self.trueConfirm, idx), noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)
        else:
            self.trueConfirm(idx)

    def checkIsInAdd(self):
        if gameglobal.rds.ui.roleInfo.mediator and gameglobal.rds.ui.roleInfo.pointMinus > 0:
            return True
        else:
            return False

    def trueConfirmAndSave(self, idx):
        gameglobal.rds.ui.roleInfo.onPotConfirm(None)
        self.trueConfirm(idx)

    def trueConfirm(self, idx):
        gameglobal.rds.ui.roleInfo.resetAddPoint()
        gameglobal.rds.ui.roleInfo.updatePotBtnVisible()
        gameglobal.rds.ui.roleInfo.updateAllPotential()
        BigWorld.player().base.usePropScheme(idx)
        self.clearWidget()

    def setSchemeName(self, *args):
        idx = int(args[3][0].GetNumber())
        name = unicode2gbk(args[3][1].GetString())
        scheme = BigWorld.player().getPropSchemeById(idx)
        if scheme:
            if scheme['schemeName'] != name:
                BigWorld.player().base.updatePropSchemeName(idx, name)
