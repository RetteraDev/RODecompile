#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildQuickJoinProxy.o
import BigWorld
import gameglobal
import uiConst
import const
from uiProxy import UIProxy
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD

class GuildQuickJoinProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildQuickJoinProxy, self).__init__(uiAdapter)
        self.modelMap = {'applyGuild': self.onApplyGuild,
         'createGuild': self.onCreateGuild}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_QUICK_JOIN, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_QUICK_JOIN:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_QUICK_JOIN)

    def show(self):
        p = BigWorld.player()
        joinLv = GCD.data.get('joinLv', const.GUILD_JOIN_LV)
        if p.lv < joinLv:
            p.showGameMsg(GMDD.data.GUILD_JOIN_LV, (p.roleName, joinLv))
            return
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_QUICK_JOIN)

    def gotoHide(self):
        if self.mediator:
            self.mediator.Invoke('gotoHide')

    def onApplyGuild(self, *arg):
        gameglobal.rds.ui.applyGuild.getGuildData(0)
        self.gotoHide()

    def onCreateGuild(self, *arg):
        p = BigWorld.player()
        createLv = GCD.data.get('createLv', const.GUILD_CREATE_LV)
        if p.lv < createLv:
            p.showGameMsg(GMDD.data.GUILD_CREATE_LV, (createLv,))
            return
        gameglobal.rds.ui.createGuild.show(0)
        self.gotoHide()
