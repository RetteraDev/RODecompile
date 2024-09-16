#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMenifestProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import uiUtils
import richTextUtils
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import UIProxy
from helpers import taboo
from cdata import game_msg_def_data as GMDD

class GuildMenifestProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMenifestProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm,
         'initData': self.onInitData}
        self.uiAdapter = uiAdapter
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MENIFEST, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_MENIFEST:
            self.mediator = mediator

    def show(self):
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_MENIFEST)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_MENIFEST)

    def onConfirm(self, *arg):
        menifestText = unicode2gbk(arg[3][0].GetString())
        result, menifestText = taboo.checkDisbWord(menifestText)
        if not result:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_MENIFEST_TABOO, ())
            return
        result, menifestText = taboo.checkBWorld(menifestText)
        if not result:
            BigWorld.player().showGameMsg(GMDD.data.GUILD_MENIFEST_TABOO, ())
            return
        if taboo.checkMonitorWord(menifestText) or richTextUtils.isSysRichTxt(menifestText):
            BigWorld.player().showGameMsg(GMDD.data.GUILD_MENIFEST_TABOO, ())
            return
        menifestText = uiUtils.htmlToText(menifestText)
        BigWorld.player().cell.updateGuildMenifest(menifestText)

    def onInitData(self, *arg):
        menifest = uiUtils.textToHtml(BigWorld.player().guild.menifest)
        return GfxValue(gbk2unicode(menifest))
