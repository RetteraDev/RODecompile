#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArena2PersonPushProxy.o
import BigWorld
from guis import generalPushProxy
from guis import uiConst
from data import duel_config_data as DCD
import gameglobal

class BalanceArena2PersonPushProxy(generalPushProxy.GeneralPushItemProxy):

    def __init__(self, uiAdapter):
        super(BalanceArena2PersonPushProxy, self).__init__(uiAdapter)

    def onClickItem(self, *args):
        self.uiAdapter.pvPPanel.pvpPanelShow(uiConst.PVP_BG_V2_TAB_BALANCE_ARENA_2PERSON)

    def isPushItemEnabled(self, state):
        enabled = gameglobal.rds.configData.get('enableDoubleArena', False)
        p = BigWorld.player()
        if p.lv < DCD.data.get('dArenaTeamMateLvLimit', 40):
            return False
        if p.isInDoubleArenaState16():
            return enabled and getattr(p, 'doubleArenaTeamInfo', {})
        return enabled
