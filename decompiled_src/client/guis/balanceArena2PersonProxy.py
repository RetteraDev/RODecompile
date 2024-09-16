#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArena2PersonProxy.o
import BigWorld
import gameglobal
import uiConst
from guis.asObject import ASObject
from uiProxy import UIProxy
import gamelog
from guis.uiTab2Proxy import UITab2Proxy
from data import duel_config_data as DCD
TAB_ONE_IDX = 0
TAB_TWO_IDX = 1

class BalanceArena2PersonProxy(UITab2Proxy):

    def __init__(self, uiAdapter):
        super(BalanceArena2PersonProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        pass

    def initPanel(self, widget):
        super(BalanceArena2PersonProxy, self).initPanel(widget)
        self.widget = widget
        self.initUI()
        self.refreshInfo()
        p = BigWorld.player()
        if self.isInZhanDui():
            self.selectSubTab(1)
        else:
            self.selectSubTab(0)

    def isInZhanDui(self):
        p = BigWorld.player()
        if hasattr(p, 'doubleArenaTeamInfo') and p.doubleArenaTeamInfo:
            return True
        return False

    def unRegisterPanel(self):
        super(BalanceArena2PersonProxy, self).unRegisterPanel()
        self.widget = None

    def _getTabList(self):
        return [{'tabIdx': TAB_ONE_IDX,
          'btnName': 'overviewBtn',
          'clsName': 'BalanceArena2Person_overviewTab',
          'pos': (28, 108),
          'proxy': 'balanceArena2PersonOverview'}, {'tabIdx': TAB_TWO_IDX,
          'btnName': 'matchBtn',
          'clsName': 'BalanceArena2Person_matchTab',
          'pos': (13, 100),
          'proxy': 'balanceArena2PersonMatch'}]

    def initUI(self):
        self.widget.netUrl.htmlText = DCD.data.get('doubleArenaLinkText', '')

    def refreshInfo(self):
        if not self.widget:
            return
