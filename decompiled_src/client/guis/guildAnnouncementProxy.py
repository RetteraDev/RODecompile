#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildAnnouncementProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import UIProxy
from helpers import taboo
from guis import richTextUtils
from cdata import game_msg_def_data as GMDD

class GuildAnnouncementProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildAnnouncementProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'initData': self.onInitData}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_ANNOUNCEMENT, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_ANNOUNCEMENT:
            self.mediator = mediator

    def show(self):
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_ANNOUNCEMENT)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_ANNOUNCEMENT)

    def onConfirm(self, *arg):
        announcement = unicode2gbk(arg[3][0].GetString())
        result, announcement = taboo.checkDisbWord(announcement)
        if richTextUtils.isSysRichTxt(announcement):
            BigWorld.player().showGameMsg(GMDD.data.GUILD_ANNOUNCEMENT_TABOO, ())
            return
        if not result:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_ANNOUNCEMENT_TABOO, ())
            return
        result, announcement = taboo.checkBWorld(announcement)
        if not result:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_ANNOUNCEMENT_TABOO, ())
            return
        if taboo.checkMonitorWord(announcement):
            BigWorld.player().showGameMsg(GMDD.data.GUILD_ANNOUNCEMENT_TABOO, ())
            return
        BigWorld.player().cell.updateGuildAnnouncement(announcement)
        self.hide()

    def onInitData(self, *arg):
        return GfxValue(gbk2unicode(BigWorld.player().guild.announcement))
