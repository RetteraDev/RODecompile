#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildSignInV2Proxy.o
import BigWorld
import gameglobal
import uiConst
import events
import ui
import const
import utils
import gamelog
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from data import guild_level_data as GLD
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD

class GuildSignInV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildSignInV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_SIGN_IN_V2, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_SIGN_IN_V2:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_SIGN_IN_V2)

    def show(self):
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
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_SIGN_IN_V2)

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.cashBtn.groupName = 'signIn'
        self.widget.cashBtn.addEventListener(events.BUTTON_CLICK, self.handleClickCashBtn, False, 0, True)
        self.widget.cashBtn2.groupName = 'signIn'
        self.widget.cashBtn2.addEventListener(events.BUTTON_CLICK, self.handleClickCashBtn, False, 0, True)
        self.widget.coinBtn.groupName = 'signIn'
        self.widget.coinBtn.addEventListener(events.BUTTON_CLICK, self.handleClickCoinBtn, False, 0, True)
        if gameglobal.rds.configData.get('enableGuildPrestigeTopRank', False):
            self.widget.cashBtn.prestigeTitle.visible = True
            self.widget.cashBtn.prestige.visible = True
            self.widget.cashBtn2.prestigeTitle.visible = True
            self.widget.cashBtn2.prestige.visible = True
            self.widget.coinBtn.prestigeTitle.visible = True
            self.widget.coinBtn.prestige.visible = True
        else:
            self.widget.cashBtn.prestigeTitle.visible = False
            self.widget.cashBtn.prestige.visible = False
            self.widget.cashBtn2.prestigeTitle.visible = False
            self.widget.cashBtn2.prestige.visible = False
            self.widget.coinBtn.prestigeTitle.visible = False
            self.widget.coinBtn.prestige.visible = False
        self.widget.cashBtn.selected = True

    def refreshInfo(self):
        if not self.widget:
            return
        guild = BigWorld.player().guild
        if not guild or not hasattr(guild, 'level'):
            return
        gldData = GLD.data.get(guild.level, {})
        signInCashWithIdx = gldData.get('signInCashWithIdx', {})
        signInCashPrestigeWithIdx = gldData.get('signInCashPrestigeWithIdx', {})
        signInCashContribWithIdx = gldData.get('signInCashContribWithIdx', {})
        p = BigWorld.player()
        isBeMerged = getattr(p, 'lastGuildNameFromMerger', '') and p.lastGuildNameFromMerger != p.guild.name
        if gameglobal.rds.configData.get('enableGuildMerger', False) and isBeMerged:
            guildMergeActivityStartTime = getattr(p, 'guildMergeActivityStartTime', 0)
            if not guildMergeActivityStartTime:
                isInActivity = False
            else:
                isInActivity = guildMergeActivityStartTime < utils.getNow() < guildMergeActivityStartTime + GCD.data.get('signInGuildMergerDura', const.TIME_INTERVAL_DAY * 7)
        else:
            isInActivity = False
        self.widget.cashBtn.cost.text = signInCashWithIdx.get(0, 2000)
        self.widget.cashBtn.contrib.text = '+%d' % signInCashContribWithIdx.get(0, 100)
        self.widget.cashBtn.prestige.text = '+%d' % signInCashPrestigeWithIdx.get(0, 100)
        self.widget.cashBtn.discountMc.visible = isInActivity
        self.widget.cashBtn.discountMc.txt.text = gameStrings.GUILD_MERGE_SIGN_IN_FREE
        self.widget.cashBtn2.cost.text = signInCashWithIdx.get(1, 2000)
        self.widget.cashBtn2.contrib.text = '+%d' % signInCashContribWithIdx.get(1, 100)
        self.widget.cashBtn2.prestige.text = '+%d' % signInCashPrestigeWithIdx.get(1, 100)
        self.widget.cashBtn2.discountMc.visible = isInActivity
        self.widget.coinBtn.cost.text = gldData.get('signInCoin', 0)
        self.widget.coinBtn.contrib.text = '+%d' % gldData.get('signInCoinContrib', 0)
        self.widget.coinBtn.prestige.text = '+%d' % gldData.get('signInCoinPrestige', 0)
        self.widget.coinBtn.discountMc.visible = isInActivity

    def handleClickCashBtn(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.selected = True

    def handleClickCoinBtn(self, *args):
        self.widget.coinBtn.selected = True

    @ui.checkInventoryLock()
    def _onConfirmBtnClick(self, e):
        p = BigWorld.player()
        if not self.widget:
            return
        if self.widget.cashBtn.selected:
            gamelog.info('jbx:guildSignInWithCash', 0)
            p.cell.guildSignInWithCash(0)
        elif self.widget.cashBtn2.selected:
            gamelog.info('jbx:guildSignInWithCash', 1)
            p.cell.guildSignInWithCash(1)
        elif self.widget.coinBtn.selected:
            p.cell.guildSignInWithCoin(p.cipherOfPerson)
        self.hide()
