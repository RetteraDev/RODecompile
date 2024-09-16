#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildRedPacketHistoryProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import events
import gametypes
import ui
from uiProxy import UIProxy
from guis.asObject import ASObject
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD

def sort_history(a, b):
    if a['canGet'] > b['canGet']:
        return -1
    if a['canGet'] < b['canGet']:
        return 1
    if a['tWhen'] > b['tWhen']:
        return -1
    if a['tWhen'] < b['tWhen']:
        return 1
    return 0


class GuildRedPacketHistoryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildRedPacketHistoryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.clearAll()
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RED_PACKET_HISTORY, self.hide)

    def clearAll(self):
        self.historyList = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_RED_PACKET_HISTORY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            self.queryInfoInCD(False)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_RED_PACKET_HISTORY)

    def show(self):
        if not gameglobal.rds.configData.get('enableGuildRedPacket', False):
            BigWorld.player().showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        if self.widget:
            self.widget.swapPanelToFront()
            self.queryInfoInCD(False)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_RED_PACKET_HISTORY)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.dataArray = []
        self.widget.scrollWndList.itemRenderer = 'GuildRedPacketHistory_Item'
        self.widget.scrollWndList.lableFunction = self.itemFunction
        self.widget.scrollWndList.itemHeight = 30
        self.widget.hint.htmlText = uiUtils.getTextFromGMD(GMDD.data.GUILD_RED_PACKET_HISTORT_PANEL_HINT, '')

    @ui.callInCD(3)
    def queryInfoInCD(self, needWidget):
        if needWidget and not self.widget:
            return
        self.queryInfo()

    def queryInfo(self):
        p = BigWorld.player()
        if not p.guild:
            return
        p.cell.queryAllGuildRedPacket(p.guild.redPacket.ver)

    def updateHistoryListInfo(self, data):
        self.historyList = [ dto[0] for dto in data ]
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        historyList = []
        for sn in self.historyList:
            redPacket = guild.getRedPacket(sn)
            historyList.append({'sn': sn,
             'tWhen': redPacket.tWhen,
             'canGet': redPacket.state == gametypes.GUILD_RED_PACKET_STATE_AVAIL and redPacket.received == 0})

        historyList.sort(cmp=sort_history)
        self.widget.scrollWndList.dataArray = historyList
        self.widget.scrollWndList.validateNow()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        guild = BigWorld.player().guild
        if not guild:
            return
        sn = itemData.sn
        redPacket = guild.getRedPacket(sn)
        itemMc.redPacketSource.text = uiUtils.getRedPacketSourceName(redPacket.pType, redPacket.subType)
        itemMc.redPacketValueIcon.bonusType = 'yunChui'
        itemMc.redPacketValue.text = format(redPacket.amount, ',')
        itemMc.redPacketNum.text = redPacket.cnt
        if redPacket.isExpired():
            itemMc.redPacketState.text = gameStrings.GUILD_RED_PACKET_HISTORY_STATE_STR_OUT_TIME
            itemMc.redPacketBtn.visible = False
        elif redPacket.received > 0:
            itemMc.redPacketState.text = gameStrings.GUILD_RED_PACKET_HISTORY_STATE_STR_DONE
            itemMc.redPacketBtn.visible = True
            itemMc.redPacketBtn.label = gameStrings.GUILD_RED_PACKET_HISTORY_LABEL_SEARCH
        elif redPacket.state == gametypes.GUILD_RED_PACKET_STATE_AVAIL:
            itemMc.redPacketState.text = gameStrings.GUILD_RED_PACKET_HISTORY_STATE_STR_READY
            itemMc.redPacketBtn.visible = True
            itemMc.redPacketBtn.label = gameStrings.GUILD_RED_PACKET_HISTORY_LABEL_GET
        else:
            itemMc.redPacketState.text = gameStrings.GUILD_RED_PACKET_HISTORY_STATE_STR_NOT_GET
            itemMc.redPacketBtn.visible = True
            itemMc.redPacketBtn.label = gameStrings.GUILD_RED_PACKET_HISTORY_LABEL_SEARCH
        itemMc.redPacketBtn.data = sn
        itemMc.redPacketBtn.addEventListener(events.BUTTON_CLICK, self.handleClickBtn, False, 0, True)

    def handleClickBtn(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        sn = e.currentTarget.data
        redPacket = guild.getRedPacket(sn)
        if redPacket.isExpired():
            p.showGameMsg(GMDD.data.GUILD_RED_PACKET_NOT_EXIST, ())
        elif redPacket.received > 0:
            p.queryGuildRedPacket(sn)
        elif redPacket.state == gametypes.GUILD_RED_PACKET_STATE_AVAIL:
            self.uiAdapter.guildRedPacketRec.show(sn)
        else:
            p.queryGuildRedPacket(sn)

    def showGuildRedPacketPushMsg(self):
        if not gameglobal.rds.configData.get('enableGuildRedPacket', False):
            return
        pushMessage = self.uiAdapter.pushMessage
        pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GUILD_RED_PACKET)

    def hideGuildRedPacketPushMsg(self):
        self.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GUILD_RED_PACKET)
