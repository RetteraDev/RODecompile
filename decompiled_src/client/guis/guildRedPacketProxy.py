#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildRedPacketProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import utils
import const
import gametypes
import events
import ui
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASObject
from data import guild_level_data as GLD
from data import guild_config_data as GCD
from cdata import game_msg_def_data as GMDD

class GuildRedPacketProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildRedPacketProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RED_PACKET, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_RED_PACKET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_RED_PACKET)

    def show(self):
        if not gameglobal.rds.configData.get('enableGuildRedPacket', False):
            BigWorld.player().showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        if gameglobal.rds.configData.get('enableGuildMerger', False):
            self.uiAdapter.guildRedPacketV2.show()
            return
        if self.widget:
            self.widget.swapPanelToFront()
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_RED_PACKET)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        for i in xrange(const.GUILD_SIGN_IN_RED_PACKET_MAX_NUM):
            itemMc = getattr(self.widget, 'redPacket%d' % i, None)
            if not itemMc:
                return
            itemMc.sendBtn.redPacketIdx = i + 1
            itemMc.sendBtn.addEventListener(events.BUTTON_CLICK, self.handleClickSendBtn, False, 0, True)

        self.widget.hint.htmlText = uiUtils.getTextFromGMD(GMDD.data.GUILD_RED_PACKET_PANEL_HINT, '')

    @ui.callInCD(0.5)
    def refreshInfoInCD(self):
        if gameglobal.rds.configData.get('enableGuildMerger', False):
            self.uiAdapter.guildRedPacketV2.refreshInfoInCD()
            return
        self.refreshInfo()

    def refreshInfo(self):
        if gameglobal.rds.configData.get('enableGuildMerger', False):
            self.uiAdapter.guildRedPacketV2.refreshInfo()
            return
        elif not self.widget:
            return
        else:
            p = BigWorld.player()
            guild = p.guild
            if not guild:
                return
            signInNum = guild.signInNum
            self.widget.signIn.signInNum.text = signInNum
            self.widget.signIn.signInBtn.enabled = False if p.guildSignIn else True
            onlineNum = sum(((1 if member.online else 0) for member in guild.member.itervalues()))
            self.widget.online.text = gameStrings.GUILD_RED_PACKET_ONLINE_STR % onlineNum
            coef = utils.getGuildRedPacketOnlineCoef(onlineNum)
            self.widget.buff.text = gameStrings.GUILD_RED_PACKET_BUFF_STR % int(round((1 + coef) * 100))
            signInNumForRedPacket = GLD.data.get(guild.level, {}).get('signInNumForRedPacket')
            if not signInNumForRedPacket or len(signInNumForRedPacket) != const.GUILD_SIGN_IN_RED_PACKET_MAX_NUM:
                return
            hasAuthorization = self.uiAdapter.guild.checkAuthorization(gametypes.GUILD_ACTION_RED_PACKET)
            for i, needNum in enumerate(signInNumForRedPacket):
                itemMc = getattr(self.widget, 'redPacket%d' % i, None)
                if not itemMc:
                    return
                if i != 0 and signInNum < signInNumForRedPacket[i - 1]:
                    itemMc.progress.gotoAndStop(0)
                    itemMc.sendBtn.visible = False
                    itemMc.desc.htmlText = gameStrings.GUILD_RED_PACKET_NEED_STR % signInNumForRedPacket[i]
                elif guild.redPacket.isSent(i + 1):
                    itemMc.progress.gotoAndStop(50)
                    itemMc.sendBtn.visible = False
                    itemMc.desc.htmlText = gameStrings.GUILD_RED_PACKET_DONE_STR
                elif signInNum >= signInNumForRedPacket[i]:
                    itemMc.progress.gotoAndStop(50)
                    if hasAuthorization:
                        itemMc.sendBtn.visible = True
                        itemMc.desc.htmlText = ''
                    else:
                        itemMc.sendBtn.visible = False
                        itemMc.desc.htmlText = gameStrings.GUILD_RED_PACKET_WAIT_STR
                else:
                    itemMc.progress.gotoAndStop(int(signInNum * 50.0 / signInNumForRedPacket[i]))
                    itemMc.sendBtn.visible = False
                    itemMc.desc.htmlText = gameStrings.GUILD_RED_PACKET_PROGRESS_STR % (signInNum, signInNumForRedPacket[i])

            return

    def handleClickSendBtn(self, *args):
        e = ASObject(args[3][0])
        BigWorld.player().cell.sendGuildSignInRedPacket(e.currentTarget.redPacketIdx)

    def _onSignInBtnClick(self, e):
        self.uiAdapter.guildSignInV2.show()

    def _onPoolBtnClick(self, e):
        self.uiAdapter.guildRedPacketPool.show()

    def _onHistoryBtnClick(self, e):
        self.uiAdapter.guildRedPacketHistory.show()

    def hideRelateUI(self):
        if gameglobal.rds.configData.get('enableGuildMerger', False):
            self.uiAdapter.guildRedPacketV2.hideRelateUI()
            return
        self.uiAdapter.guildRedPacketHistory.hideGuildRedPacketPushMsg()
        if self.uiAdapter.guildSignInV2.widget:
            self.uiAdapter.guildSignInV2.hide()
        if self.uiAdapter.guildRedPacketPool.widget:
            self.uiAdapter.guildRedPacketPool.hide()
        if self.uiAdapter.guildRedPacketHistory.widget:
            self.uiAdapter.guildRedPacketHistory.hide()
        if self.uiAdapter.guildRedPacketRec.widget:
            self.uiAdapter.guildRedPacketRec.hide()
        if self.widget:
            self.hide()
