#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildMembersFbSortProxy.o
import BigWorld
import uiConst
import gameglobal
import utils
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis import events
from guis import uiUtils
from guis.asObject import ASObject
from cdata import game_msg_def_data as GMDD

class GuildMembersFbSortProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildMembersFbSortProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rankData = []
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_MEMBERS_FB_SORT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GUILD_MEMBERS_FB_SORT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GUILD_MEMBERS_FB_SORT)

    def reset(self):
        self.rankData = []

    def show(self, rankData):
        self.rankData = rankData
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_GUILD_MEMBERS_FB_SORT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.sortMc.previewBtn.addEventListener(events.BUTTON_CLICK, self.handlePreviewBtnClick, False, 0, True)
        self.widget.sortMc.previewBtn.visible = gameglobal.rds.configData.get('enableGuildFubenTopReward', False)
        self.widget.sortMc.list.itemRenderer = 'GuildMembersFbSort_CommonRankItem'
        self.widget.sortMc.list.itemHeight = 35
        self.widget.sortMc.list.dataArray = []
        self.widget.sortMc.list.lableFunction = self.itemFunction
        self.widget.rule.htmlText = uiUtils.getTextFromGMD(GMDD.data.GUILD_MEMBERS_FB_SORT_RULE, '')

    def refreshInfo(self):
        if not self.widget:
            return
        rankList = []
        for i, value in enumerate(self.rankData[1]):
            itemInfo = {}
            itemInfo['guildRank'] = value[0]
            itemInfo['guildName'] = value[1]
            itemInfo['bossNum'] = value[2]
            itemInfo['consumeTime'] = utils.formatTimeStr(value[3], 'h:m:s', True, 2, 2, 2)
            itemInfo['combatScore'] = int(value[4])
            rankList.append(itemInfo)

        self.widget.sortMc.list.dataArray = rankList
        self.widget.sortMc.list.validateNow()
        self.widget.sortMc.rank.text = self.rankData[2][0] if self.rankData[2][0] else gameStrings.RANK_NOT_IN_TEXT

    def handlePreviewBtnClick(self, *args):
        gameglobal.rds.ui.rankingAwardPreview.show()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.guildRank <= 3:
            itemMc.rank.visible = False
            itemMc.top3Icon.visible = True
            itemMc.top3Icon.gotoAndStop('top%d' % itemData.guildRank)
        else:
            itemMc.rank.visible = True
            itemMc.top3Icon.visible = False
            itemMc.rank.text = str(itemData.guildRank)
        itemMc.data1.text = itemData.guildName
        itemMc.data3.text = itemData.bossNum
        itemMc.data4.text = itemData.consumeTime
        itemMc.data5.text = itemData.combatScore
