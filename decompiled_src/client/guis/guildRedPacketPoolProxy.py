#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildRedPacketPoolProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import uiUtils
import const
import ui
from uiTabProxy import UITabProxy
from guis.asObject import ASObject
from data import achievement_data as AD
from cdata import game_msg_def_data as GMDD
TAB_INDEX_MYSELF = 0
TAB_INDEX_VIEW = 1

class GuildRedPacketPoolProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(GuildRedPacketPoolProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_RED_PACKET_POOL, self.hide)

    def reset(self):
        super(GuildRedPacketPoolProxy, self).reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_RED_PACKET_POOL:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)

    def clearWidget(self):
        super(GuildRedPacketPoolProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_RED_PACKET_POOL)

    def _getTabList(self):
        return [{'tabIdx': TAB_INDEX_MYSELF,
          'tabName': 'tabBtn0',
          'view': 'GuildRedPacketPool_Myself'}, {'tabIdx': TAB_INDEX_VIEW,
          'tabName': 'tabBtn1',
          'view': 'GuildRedPacketPool_View'}]

    def show(self):
        if not gameglobal.rds.configData.get('enableGuildRedPacket', False):
            BigWorld.player().showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        if self.widget:
            self.widget.swapPanelToFront()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_RED_PACKET_POOL)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()

    def onTabChanged(self, *args):
        super(GuildRedPacketPoolProxy, self).onTabChanged(*args)
        self.currentView.scrollWndList.dataArray = []
        self.currentView.scrollWndList.itemHeight = 30
        if self.currentTabIndex == TAB_INDEX_MYSELF:
            self.currentView.scrollWndList.itemRenderer = 'GuildRedPacketPool_MyselfItem'
            self.currentView.scrollWndList.lableFunction = self.myselfItemFunction
            self.currentView.hint.htmlText = uiUtils.getTextFromGMD(GMDD.data.GUILD_RED_PACKET_POOL_PANEL_MYSELF_HINT, '')
        else:
            self.currentView.scrollWndList.itemRenderer = 'GuildRedPacketPool_ViewItem'
            self.currentView.scrollWndList.lableFunction = self.viewItemFunction
            self.currentView.hint.htmlText = uiUtils.getTextFromGMD(GMDD.data.GUILD_RED_PACKET_POOL_PANEL_VIEW_HINT, '')
        self.refreshInfo()
        self.queryInfoInCD(False)

    @ui.callInCD(2.5)
    def queryInfoInCD(self, needWidget):
        if needWidget and not self.widget:
            return
        self.queryInfo()

    def queryInfo(self):
        p = BigWorld.player()
        if not p.guild:
            return
        p.cell.queryGuildAchieveRedPacketPool(p.guild.redPacket.poolVer)

    @ui.callInCD(0.5)
    def refreshInfoInCD(self):
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        if self.currentTabIndex == TAB_INDEX_MYSELF:
            self.refreshMyselfInfo()
        else:
            self.refreshViewInfo()

    def refreshMyselfInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        poolList = []
        for redPacket in guild.redPacket.achieveRedPacketPool:
            if redPacket.gbId != p.gbId:
                continue
            poolList.append({'achieveId': redPacket.achieveId})

        self.currentView.scrollWndList.dataArray = poolList
        self.currentView.scrollWndList.validateNow()

    def refreshViewInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        poolList = []
        for redPacket in guild.redPacket.achieveRedPacketPool:
            if redPacket.gbId == p.gbId:
                continue
            poolList.append({'gbId': redPacket.gbId,
             'achieveId': redPacket.achieveId})

        self.currentView.scrollWndList.dataArray = poolList
        self.currentView.scrollWndList.validateNow()

    def myselfItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        guild = BigWorld.player().guild
        if not guild:
            return
        achieveId = int(itemData.achieveId)
        itemMc.redPacketSource.text = uiUtils.getRedPacketSourceName(const.RED_PACKET_TYPE_ACHIEVE, achieveId)
        itemMc.redPacketValueIcon.bonusType = 'yunChui'
        redPacketData = AD.data.get(achieveId, {}).get('redPacket', (0, 0))
        itemMc.redPacketValue.text = redPacketData[0]
        itemMc.redPacketNum.text = redPacketData[1]
        itemMc.sendBtn.data = achieveId
        itemMc.sendBtn.addEventListener(events.BUTTON_CLICK, self.handleClickSendBtn, False, 0, True)

    def viewItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        guild = BigWorld.player().guild
        if not guild:
            return
        else:
            achieveId = int(itemData.achieveId)
            itemMc.redPacketSource.text = uiUtils.getRedPacketSourceName(const.RED_PACKET_TYPE_ACHIEVE, achieveId)
            itemMc.redPacketValueIcon.bonusType = 'yunChui'
            redPacketData = AD.data.get(achieveId, {}).get('redPacket', (0, 0))
            itemMc.redPacketValue.text = redPacketData[0]
            itemMc.redPacketNum.text = redPacketData[1]
            gbId = long(itemData.gbId)
            member = guild.member.get(gbId, None) if guild else None
            itemMc.playerName.text = member.role if member else ''
            return

    def handleClickSendBtn(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        guild = p.guild
        if not guild:
            return
        achieveId = int(e.currentTarget.data)
        p.cell.sendGuildAchieveRedPacket(achieveId)
