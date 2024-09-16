#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/shishenModeProxy.o
from gamestrings import gameStrings
import BigWorld
from uiProxy import UIProxy
import gameglobal
from guis import uiConst
from callbackHelper import Functor
from Scaleform import GfxValue
from guis import uiUtils
from data import sys_config_data as SCD

class ShishenModeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ShishenModeProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'selectMode': self.onSelectMode,
         'getCurrentMode': self.onGetCurrentMode,
         'getModeNames': self.onGetModeNames}
        self.mediator = None
        self.shishenAimMode = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_SHISHEN_MODE, self.onClose)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SHISHEN_MODE:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SHISHEN_MODE)

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SHISHEN_MODE)

    def onSelectMode(self, *arg):
        currentMode = gameglobal.rds.ui.currentShishenMode
        modeStr = SCD.data.get('fubenModeNames', ['',
         gameStrings.TEXT_QUESTTRACKPROXY_1748,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_1,
         gameStrings.TEXT_QUESTTRACKPROXY_1748_2,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_3])
        p = BigWorld.player()
        self.shishenAimMode = int(arg[3][0].GetNumber())
        if currentMode == 0:
            p.showTopMsg(gameStrings.TEXT_FUBENDEGREEPROXY_124)
            return
        if self.shishenAimMode == currentMode:
            BigWorld.player().showTopMsg(gameStrings.TEXT_FUBENDEGREEPROXY_127 % modeStr[self.shishenAimMode])
            return
        if currentMode > self.shishenAimMode:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_FUBENDEGREEPROXY_130 % modeStr[self.shishenAimMode], Functor(self.comfirmSetShishenMode))
        else:
            BigWorld.player().showTopMsg(gameStrings.TEXT_FUBENDEGREEPROXY_132)

    def comfirmSetShishenMode(self):
        if self.shishenAimMode == 0:
            return
        BigWorld.player().cell.setShishenMode(self.shishenAimMode)
        self.hide()

    def onGetCurrentMode(self, *arg):
        mode = gameglobal.rds.ui.currentShishenMode
        return GfxValue(mode)

    def onGetModeNames(self, *arg):
        modeStr = SCD.data.get('fubenModeNames', ['',
         gameStrings.TEXT_QUESTTRACKPROXY_1748,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_1,
         gameStrings.TEXT_QUESTTRACKPROXY_1748_2,
         gameStrings.TEXT_FUBENDEGREEPROXY_120_3])
        ret = [modeStr[1], modeStr[2], modeStr[3]]
        return uiUtils.array2GfxAarry(ret, True)
