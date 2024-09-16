#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArena2PersonMatchProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from guis.balanceArena2PersonRequireProxy import BalanceArena2PersonRequireProxy
from guis.balanceArena2PersonTeamProxy import BalanceArena2PersonTeamProxy
from uiProxy import UIProxy

class BalanceArena2PersonMatchProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceArena2PersonMatchProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.requirePanel = None
        self.teamPanel = None

    def isInZhanDui(self):
        p = BigWorld.player()
        if hasattr(p, 'doubleArenaTeamInfo') and p.doubleArenaTeamInfo:
            return True
        return False

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()
        self.addEvent(events.EVENT_CHANGE_ARENA_STATE, self.refreshInfo)

    def unRegisterPanel(self):
        self.widget = None
        if self.teamPanel:
            self.teamPanel.unRegisterPanel()
            self.teamPanel = None
        if self.requirePanel:
            self.requirePanel.unRegisterPanel()
            self.requirePanel = None

    def initUI(self):
        pass

    def refreshInfo(self):
        if not self.widget:
            return
        if self.isInZhanDui():
            self.widget.teamMc.visible = True
            self.widget.requireMc.visible = False
            if not self.teamPanel:
                self.teamPanel = BalanceArena2PersonTeamProxy()
                self.teamPanel.initPanel(self.widget.teamMc)
            else:
                self.teamPanel.refreshInfo()
        else:
            self.widget.teamMc.visible = False
            self.widget.requireMc.visible = True
            if not self.requirePanel:
                self.requirePanel = BalanceArena2PersonRequireProxy()
                self.requirePanel.initPanel(self.widget.requireMc)
            else:
                self.requirePanel.refreshInfo()
