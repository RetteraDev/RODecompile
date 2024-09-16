#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildSignInProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import ui
import const
from uiProxy import UIProxy
from data import guild_level_data as GLD
from cdata import game_msg_def_data as GMDD

class GuildSignInProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildSignInProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_SIGN_IN, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_SIGN_IN:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_SIGN_IN)

    def show(self):
        self.uiAdapter.guildSignInV2.show()
        return
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableGuildSignIn', False):
            p.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        if not p.guild:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
            return
        if self.widget:
            self.widget.swapPanelToFront()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_SIGN_IN)

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.cashBtn.groupName = 'signIn'
        self.widget.cashBtn.addEventListener(events.BUTTON_CLICK, self.handleClickCashBtn, False, 0, True)
        self.widget.coinBtn.groupName = 'signIn'
        self.widget.coinBtn.addEventListener(events.BUTTON_CLICK, self.handleClickCoinBtn, False, 0, True)
        if gameglobal.rds.configData.get('enableGuildPrestigeTopRank', False):
            self.widget.cashBtn.prestigeTitle.visible = True
            self.widget.cashBtn.prestige.visible = True
            self.widget.coinBtn.prestigeTitle.visible = True
            self.widget.coinBtn.prestige.visible = True
        else:
            self.widget.cashBtn.prestigeTitle.visible = False
            self.widget.cashBtn.prestige.visible = False
            self.widget.coinBtn.prestigeTitle.visible = False
            self.widget.coinBtn.prestige.visible = False
        self.widget.cashBtn.selected = True

    def refreshInfo(self):
        if not self.widget:
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        gldData = GLD.data.get(guild.level, {})
        self.widget.cashBtn.cost.text = gldData.get('signInCash', 0)
        self.widget.cashBtn.contrib.text = '+%d' % gldData.get('signInCashContrib', 0)
        self.widget.cashBtn.prestige.text = '+%d' % gldData.get('signInCashPrestige', 0)
        self.widget.coinBtn.cost.text = gldData.get('signInCoin', 0)
        self.widget.coinBtn.contrib.text = '+%d' % gldData.get('signInCoinContrib', 0)
        self.widget.coinBtn.prestige.text = '+%d' % gldData.get('signInCoinPrestige', 0)

    def handleClickCashBtn(self, *args):
        self.widget.cashBtn.selected = True

    def handleClickCoinBtn(self, *args):
        self.widget.coinBtn.selected = True

    @ui.checkInventoryLock()
    def _onConfirmBtnClick(self, e):
        p = BigWorld.player()
        if self.widget.cashBtn.selected:
            p.cell.guildSignInWithCash(0)
        elif self.widget.coinBtn.selected:
            p.cell.guildSignInWithCoin(p.cipherOfPerson)
        self.hide()
