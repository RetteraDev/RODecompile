#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/crossClanWarHistoryProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import utils
import events
from gamestrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import ASUtils
from uiProxy import UIProxy
from data import cross_clan_war_config_data as CCWCD
from data import region_server_config_data as RSCD
from data import clan_war_fort_data as CWFD

class CrossClanWarHistoryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CrossClanWarHistoryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CROSS_CLAN_WAR_HISTORY, self.hide)

    def reset(self):
        self.filterType = uiConst.CROSS_CLAN_WAR_HISTORY_FILTER_TYPE_SELF
        self.crossClanWarHistory = []

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CROSS_CLAN_WAR_HISTORY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CROSS_CLAN_WAR_HISTORY)

    def show(self, filterType):
        if not self.widget:
            self.filterType = filterType
            self.uiAdapter.loadWidget(uiConst.WIDGET_CROSS_CLAN_WAR_HISTORY)
            BigWorld.player().cell.getClanWarRecordInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.itemRenderTest.alpha = 0
        ASUtils.setHitTestDisable(self.widget.itemRenderTest, True)
        self.widget.scrollWndList.itemRenderer = 'CrossClanWarHistory_ItemRender'
        self.widget.scrollWndList.labelFunction = self.lableFunction
        self.widget.scrollWndList.itemHeightFunction = self.itemHeightFunction

    def itemHeightFunction(self, *args):
        crossClanWarHistory = self.crossClanWarHistory
        index = int(args[3][0].GetNumber())
        if index >= len(crossClanWarHistory):
            return
        itemData = crossClanWarHistory[index]
        self.widget.itemRenderTest.content.htmlText = self.getDesc(itemData)
        return GfxValue(self.widget.itemRenderTest.content.textHeight + 5)

    def getDesc(self, itemData):
        p = BigWorld.player()
        tWhen = int(itemData[0])
        fortInfo = itemData[1]
        rank = itemData[2]
        attendance = itemData[3]
        killCnt = itemData[4]
        crossHost = itemData[5]
        timeStr = utils.formatDatetime(tWhen)
        guildName = p.guild.name
        serverName = self.uiAdapter.crossClanWar.getServerName(crossHost)
        fortNameList = []
        buildingNameList = []
        for fortId in fortInfo:
            name = CWFD.data.get(fortId, {}).get('showName', '1')
            if CWFD.data.get(fortId, {}).get('type', 1) == 1:
                fortNameList.append(name)
            else:
                buildingNameList.append(name)

        fortNameStr = ','.join(fortNameList) if fortNameList else gameStrings.TEXT_BATTLEFIELDPROXY_1605
        buildingNameStr = ','.join(buildingNameList) if buildingNameList else gameStrings.TEXT_BATTLEFIELDPROXY_1605
        if crossHost and crossHost != utils.getHostId():
            return CCWCD.data.get('attackHistoryAttackDesc', gameStrings.TEXT_CROSSCLANWARHISTORYPROXY_87) % (timeStr,
             guildName,
             serverName,
             attendance,
             killCnt,
             fortNameStr,
             buildingNameStr,
             rank)
        else:
            return CCWCD.data.get('attackHistoryDefDesc', gameStrings.TEXT_CROSSCLANWARHISTORYPROXY_96) % (timeStr,
             guildName,
             attendance,
             killCnt,
             fortNameStr,
             buildingNameStr,
             rank)

    def lableFunction(self, *args):
        crossClanWarHistory = self.crossClanWarHistory
        index = int(args[3][0].GetNumber())
        if index >= len(crossClanWarHistory):
            return
        itemData = crossClanWarHistory[index]
        itemMc = ASObject(args[3][1])
        itemMc.content.htmlText = self.getDesc(itemData)

    def test(self):
        now = utils.getNow()
        crossClanWarHistory = []
        guildNuid = BigWorld.player().guild.nuid
        fortListSelf = {10: guildNuid,
         11: guildNuid,
         12: guildNuid,
         13: guildNuid,
         14: guildNuid,
         15: guildNuid}
        guildNuid = 0
        fotListOthers = {10: guildNuid,
         11: guildNuid,
         12: guildNuid,
         13: guildNuid,
         14: guildNuid,
         15: guildNuid}
        crossClanWarHistory.append((now - 432000,
         fortListSelf,
         9,
         100,
         100,
         29031))
        crossClanWarHistory.append((now - 345600,
         fortListSelf,
         9,
         100,
         100,
         0))
        crossClanWarHistory.append((now - 259200,
         fotListOthers,
         9,
         100,
         100,
         29031))
        crossClanWarHistory.append((now - 172800,
         fortListSelf,
         9,
         100,
         100,
         0))
        crossClanWarHistory.append((now - 86400,
         fotListOthers,
         9,
         100,
         100,
         29031))
        BigWorld.player().crossClanWarHistory = crossClanWarHistory * 5

    def checkFilter(self, historyInfo):
        tWhen, fortInfo, rank, attendance, killCnt, crossHost = historyInfo
        if not rank and not attendance and not killCnt:
            return False
        elif self.filterType == uiConst.CROSS_CLAN_WAR_HISTORY_FILTER_TYPE_SELF:
            return not historyInfo[5] or historyInfo[5] == utils.getHostId()
        else:
            return historyInfo[5] != utils.getHostId()

    def refreshInfo(self):
        if not self.widget:
            return
        crossClanWarHistory = getattr(BigWorld.player(), 'crossClanWarHistory', [])
        self.crossClanWarHistory = [ historyInfo for historyInfo in crossClanWarHistory if self.checkFilter(historyInfo) ]
        self.crossClanWarHistory.sort(cmp=lambda a, b: cmp(b[0], a[0]))
        self.widget.scrollWndList.dataArray = range(len(self.crossClanWarHistory))
