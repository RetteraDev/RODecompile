#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildRedPacketRecProxy.o
import BigWorld
import gameglobal
import uiConst
import const
import gametypes
import uiUtils
import events
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class GuildRedPacketRecProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildRedPacketRecProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RED_PACKET_REC, self.hide)

    def reset(self):
        self.sn = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_RED_PACKET_REC:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_RED_PACKET_REC)

    def closeBySn(self, sn):
        if self.sn == sn:
            self.hide()

    def show(self, sn):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableGuildRedPacket', False):
            p.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        guild = p.guild
        if not guild:
            p.showGameMsg(GMDD.data.GUILD_NOT_JOINED, (const.YOU,))
            return
        redPacket = guild.getRedPacket(sn)
        if redPacket.isExpired():
            p.showGameMsg(GMDD.data.GUILD_RED_PACKET_NOT_EXIST, ())
            return
        self.sn = sn
        if self.widget:
            self.widget.swapPanelToFront()
            self.refreshInfo()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_RED_PACKET_REC)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        guild = BigWorld.player().guild
        if not guild:
            return
        redPacket = guild.getRedPacket(self.sn)
        sourceName = uiUtils.getRedPacketSourceName(redPacket.pType, redPacket.subType) or getattr(redPacket, 'msg', '')
        packetDetail = self.widget.packetDetail
        if redPacket.pType in (const.RED_PACKET_TYPE_GUILD, const.RED_PACKET_TYPE_GUILD_MERGER_CLAP):
            self.widget.title.gotoAndStop('signIn')
            if redPacket.received > 0:
                packetDetail.gotoAndStop('signInSucc')
                packetDetail.sourceTextField.text = sourceName
                packetDetail.bonusEffect.gotoAndPlay(1)
                packetDetail.bonusEffect.bonusMc.bonusIcon.bonusType = 'yunChui'
                packetDetail.bonusEffect.bonusMc.bonusNum.text = format(redPacket.received, ',')
                packetDetail.viewOther.addEventListener(events.MOUSE_CLICK, self.handleClickViewOther, False, 0, True)
            elif redPacket.state == gametypes.GUILD_RED_PACKET_STATE_AVAIL:
                packetDetail.gotoAndStop('signInReady')
                packetDetail.source.textField.text = sourceName
            else:
                packetDetail.gotoAndStop('signInFailed')
                packetDetail.sourceTextField.text = sourceName
                packetDetail.viewOther.addEventListener(events.MOUSE_CLICK, self.handleClickViewOther, False, 0, True)
            packetDetail.guildName.text = guild.name
        elif redPacket.pType == const.RED_PACKET_TYPE_ACHIEVE:
            self.widget.title.gotoAndStop('achieve')
            if redPacket.received > 0:
                packetDetail.gotoAndStop('achieveSucc')
                packetDetail.sourceTextField.text = sourceName
                packetDetail.bonusEffect.gotoAndPlay(1)
                packetDetail.bonusEffect.bonusMc.bonusIcon.bonusType = 'yunChui'
                packetDetail.bonusEffect.bonusMc.bonusNum.text = format(redPacket.received, ',')
                packetDetail.viewOther.addEventListener(events.MOUSE_CLICK, self.handleClickViewOther, False, 0, True)
            elif redPacket.state == gametypes.GUILD_RED_PACKET_STATE_AVAIL:
                packetDetail.gotoAndStop('achieveReady')
                packetDetail.source.textField.text = sourceName
            else:
                packetDetail.gotoAndStop('achieveFailed')
                packetDetail.sourceTextField.text = sourceName
                packetDetail.viewOther.addEventListener(events.MOUSE_CLICK, self.handleClickViewOther, False, 0, True)
            packetDetail.headIcon.fitSize = True
            if redPacket.photo.find('headIcon') == 0:
                packetDetail.headIcon.loadImage(redPacket.photo)
            else:
                packetDetail.headIcon.imgType = uiConst.IMG_TYPE_NOS_FILE
                packetDetail.headIcon.url = redPacket.photo
            packetDetail.roleName.text = redPacket.srcName

    def _onOpenBtnClick(self, e):
        BigWorld.player().receiveGuildRedPacket(self.sn)

    def handleClickViewOther(self, *args):
        BigWorld.player().queryGuildRedPacket(self.sn)
