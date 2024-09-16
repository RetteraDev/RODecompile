#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMemberLvSetProxy.o
import BigWorld
import uiConst
import gameglobal
from uiProxy import UIProxy
import gametypes

class GuildMemberLvSetProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMemberLvSetProxy, self).__init__(uiAdapter)
        self.modelMap = {'save': self.onSave,
         'cancel': self.onCancel}
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MEMBER_LV_SET, self.hide)
        self.mediator = None

    def show(self):
        if not self.mediator:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_MEMBER_LV_SET)

    def reset(self):
        self.mediator = None

    def clearWidget(self):
        if self.mediator:
            self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_MEMBER_LV_SET)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_MEMBER_LV_SET:
            self.mediator = mediator

    def onSave(self, *args):
        if args[3][0].GetString():
            lv = int(args[3][0].GetString())
        else:
            lv = 0
        BigWorld.player().cell.updateGuildAutoAccept(gametypes.GUILD_AUTO_ACCEPT_FLOWBACK, lv)
        gameglobal.rds.ui.guildMember.setAutoLv(lv)
        self.hide()

    def onCancel(self, *args):
        self.hide()
