#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidDreamlandGodHelpProxy.o
import BigWorld
import gameglobal
import uiConst
from guis import uiUtils
from callbackHelper import Functor
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class VoidDreamlandGodHelpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoidDreamlandGodHelpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rank = 0
        self.currSelectProgress = 0
        self.challengeCount = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_DREAMLAND_GOD_HELP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_DREAMLAND_GOD_HELP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self, rank, currSelectProgress, challengeCount):
        self.rank = rank
        self.currSelectProgress = currSelectProgress
        self.challengeCount = challengeCount
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VOID_DREAMLAND_GOD_HELP, True)

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_VOID_DREAMLAND_GOD_HELP)

    def reset(self):
        self.rank = 0
        self.currSelectProgress = 0
        self.challengeCount = 0

    def _onChallengeBtnClick(self, e):
        self.selectToChallengeWay(False)

    def _onGodHelpBtnClick(self, e):
        self.selectToChallengeWay(True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return

    def selectToChallengeWay(self, isGodHelp):
        p = BigWorld.player()
        if self.challengeCount > 0:
            p.cell.applyFubenOfEndless(self.rank, self.currSelectProgress, isGodHelp)
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.VOID_DREAMLANG_NONT_CHALLENGE_COUNT, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.applyFubenOfEndless, self.rank, self.currSelectProgress, isGodHelp))
