#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMergeBonfireProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
from gamestrings import gameStrings
from guis import ui
from uiProxy import UIProxy
from guis.asObject import ASUtils
from data import game_msg_data as GMD
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD

class GuildMergeBonfireProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMergeBonfireProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MERGE_BONFIRE, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_MERGE_BONFIRE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_MERGE_BONFIRE)

    def addPushMsg(self):
        if not self.uiAdapter.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_GUILD_MERGE_BONFIRE):
            self.uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GUILD_MERGE_BONFIRE, {'click': self.show})
            self.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_MERGE_BONFIRE)

    def delPushMsg(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_MERGE_BONFIRE)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_MERGE_BONFIRE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        p = BigWorld.player()
        guildName = getattr(p, 'guildNameFromMerger', '')
        self.widget.txtDesc.htmlText = GCD.data.get('guildMergeBonfireDesc', '%s') % guildName
        self.widget.radioBtn0.selected = False
        self.widget.txtFreeDesc.htmlText = GCD.data.get('bonfireFreeDesc', '')
        self.widget.radioBtn1.selected = True
        self.widget.txtConsumeCoin.htmlText = GCD.data.get('bonfireConsumeCoinDesc', '')
        ASUtils.setHitTestDisable(self.widget.txtRadion0, True)
        ASUtils.setHitTestDisable(self.widget.txtRadion1, True)
        self.widget.txtRewards.htmlText = GCD.data.get('guildMergeBonfireRewards', '')
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def handleConfirmBtnClick(self, *args):
        gamelog.info('jbx:handleConfirmBtnClick')
        p = BigWorld.player()
        if self.widget.radioBtn0.selected:
            p.cell.applyClapForGuildMergerMember(True)
        else:
            coinNum = GCD.data.get('clapForGuildMergerMemberCost', 10)
            if p.unbindCoin + p.bindCoin + p.freeCoin < coinNum:
                p.showGameMsg(GMDD.data.NOT_ENOUGH_COIN, ())
            else:
                text = GMD.data.get(GMDD.data.GUILD_MERGE_BONFIRE_CONFIRM, {}).get('text', '')
                self.uiAdapter.messageBox.showYesNoMsgBox(text, self.yesCallback)

    def hide(self, addPushMsg = True):
        super(GuildMergeBonfireProxy, self).hide(True)
        if addPushMsg:
            self.addPushMsg()
        else:
            self.delPushMsg()

    @ui.checkInventoryLock()
    def yesCallback(self):
        BigWorld.player().cell.applyClapForGuildMergerMember(False)
