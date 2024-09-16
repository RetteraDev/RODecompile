#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArenaPlayoffsPushProxy.o
import BigWorld
from guis import generalPushProxy
from guis import uiConst
import gameglobal

class BalanceArenaPlayoffsPushProxy(generalPushProxy.GeneralPushItemProxy):

    def __init__(self, uiAdapter):
        super(BalanceArenaPlayoffsPushProxy, self).__init__(uiAdapter)

    def onClickItem(self, *args):
        self.uiAdapter.pvPPanel.pvpPanelShow(uiConst.PVP_BG_V2_TAB_BALANCE_PLAYOFFS)

    def isPushItemEnabled(self, state):
        enabled = gameglobal.rds.configData.get('enableArenaScore', False)
        p = BigWorld.player()
        if p.isInArenaScoreStateJiFen():
            return enabled
        if p.isInArenaScoreStateWuDao() and p.arenaPlayoffsTeamNUID:
            return enabled
        return False
