#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildDonateReserveProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiUtils
import uiConst
import commGuild
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import ui

class GuildDonateReserveProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildDonateReserveProxy, self).__init__(uiAdapter)
        self.modelMap = {'setCash': self.onSetCash,
         'getCash': self.onGetCash,
         'donateReserve': self.onDonateReserve}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_DONATE_RESERVE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_DONATE_RESERVE:
            self.mediator = mediator

    def show(self):
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_DONATE_RESERVE)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_DONATE_RESERVE)

    def onSetCash(self, *arg):
        cash = int(arg[3][0].GetNumber())
        coin = int(arg[3][1].GetNumber())
        self.updateLuxuryValue(cash, coin)

    def onGetCash(self, *arg):
        p = BigWorld.player()
        info = {}
        info['cashMax'] = p.cash
        info['coinMax'] = p.unbindCoin
        return uiUtils.dict2GfxDict(info, True)

    @ui.checkInventoryLock()
    def onDonateReserve(self, *arg):
        cash = int(arg[3][0].GetNumber())
        coin = int(arg[3][1].GetNumber())
        cmsg = ''
        if cash != 0:
            cmsg += gameStrings.TEXT_GUILDDONATERESERVEPROXY_56 % uiUtils.convertNumStr(0, cash, False, True)
        if coin != 0:
            if cmsg != '':
                cmsg += gameStrings.TEXT_CHATPROXY_403
            cmsg += gameStrings.TEXT_GUILDDONATERESERVEPROXY_60 % uiUtils.convertNumStr(0, coin, False, True)
        msg = gameStrings.TEXT_GUILDDONATERESERVEPROXY_61 % cmsg
        p = BigWorld.player()
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.base.guildDonateReserve, cash, coin, p.cipherOfPerson))

    def updateLuxuryValue(self, cash, coin):
        if self.mediator:
            luxuryValue = commGuild.calcLuxury(cash, coin)
            self.mediator.Invoke('updateLuxuryValue', GfxValue(luxuryValue))
