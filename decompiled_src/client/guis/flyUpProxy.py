#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/flyUpProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
from uiProxy import UIProxy
from uiTabProxy import UITabProxy
from cdata import game_msg_def_data as GMDD

class FlyUpProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(FlyUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FLYUP, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FLYUP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def _getTabList(self):
        return [{'tabIdx': uiConst.FLY_UP_TAB_CHALLENGE,
          'tabName': 'challengeBtn',
          'view': 'FlyUpChallengeWidget',
          'proxy': 'flyUpChallenge'}, {'tabIdx': uiConst.FLY_UP_TAB_BONUS,
          'tabName': 'bonusBtn',
          'view': 'FlyUpBonusWidget',
          'proxy': 'flyUpBonus'}]

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FLYUP)

    def show(self):
        if utils.enableFlyUp():
            BigWorld.player().showGameMsg(GMDD.data.USER_ACCOUNT_BIND_NOT_OPEN, ())
            return
        if not self.widget:
            self.showTabIndex = 1
            self.uiAdapter.loadWidget(uiConst.WIDGET_FLYUP)

    def initUI(self):
        self.initTabUI()
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
