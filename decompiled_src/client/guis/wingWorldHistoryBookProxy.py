#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldHistoryBookProxy.o
import BigWorld
from gamestrings import gameStrings
import uiConst
from guis.asObject import ASObject
from guis.asObject import ASUtils
import events
from uiProxy import UIProxy
from data import wing_world_data as WWD

class WingWorldHistoryBookProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldHistoryBookProxy, self).__init__(uiAdapter)
        self.widget = None
        self.callbackId = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_HISTORY_BOOK, self.hide)

    def reset(self):
        self.selectedBatchNum = 0
        self.selectedMc = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_HISTORY_BOOK:
            self.widget = widget
            ASUtils.callbackAtFrame(self.widget, self.widget.totalFrames, self.reInit)
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.callbackId = 0
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_HISTORY_BOOK)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_HISTORY_BOOK)
        BigWorld.player().cell.queryWingWorldSeasonHistoryBook()

    def initUI(self):
        p = BigWorld.player()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.mainMc.pageList.validateNow()
        self.widget.mainMc.pageList.hasTweens = False
        self.widget.mainMc.pageList.pageItemFunc = self.pageItemFun
        self.widget.mainMc.pageList.childItem = 'WingWorldHistoryBook_PageViewItemRender'
        self.widget.mainMc.pageList.childWidth = 48
        self.widget.mainMc.group1.visible = False
        self.widget.mainMc.group2.visible = False
        self.widget.mainMc.group3.addEventListener(events.BUTTON_CLICK, self.handleGroupClick, False, 0, True)
        self.widget.mainMc.group3.label = WWD.data.get(p.getWingGroupId(), {}).get('name', '')
        self.widget.mainMc.scrollList.itemRenderer = 'WingWorldHistoryBook_ScrollListItemRender'
        self.widget.mainMc.scrollList.labelFunction = self.lableFunction
        self.widget.mainMc.pageList.data = []
        self.widget.mainMc.txtServerName.text = ''
        self.widget.mainMc.txtKinderName.text = ''
        self.widget.mainMc.history.text = ''
        self.widget.mainMc.scrollList.dataArray = []

    def reInit(self, *args):
        if not self.widget or not self.widget.stage:
            return
        self.reset()
        self.initUI()
        self.refreshInfo()

    def lableFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.txtCityName.text = itemData[0]
        itemMc.txtGuildName.text = itemData[1]
        itemMc.txtLeaderName.text = itemData[2]

    def handleGroupClick(self, *args):
        pass

    def pageItemFun(self, *args):
        itemMc = ASObject(args[3][0])
        itemData = ASObject(args[3][1])
        itemMc.itemData = itemData
        itemMc.addEventListener(events.COMPONENT_STATE_CHANGE, self.handleItemStateChange, False, 0, True)
        itemMc.addEventListener(events.BUTTON_CLICK, self.handlePageItemClick, False, 0, True)
        itemMc.batchNum.gotoAndStop('batchNum%d' % itemData[0])
        if int(itemData[0]) == self.selectedBatchNum:
            itemMc.selected = True
            if self.selectedMc:
                self.selectedMc.selected = False
            self.selectedMc = itemMc
        else:
            itemMc.selected = False

    def handlePageItemClick(self, *args):
        e = ASObject(args[3][0])
        itemData = e.currentTarget.itemData
        if int(itemData[0]) != self.selectedBatchNum:
            if self.selectedMc:
                self.selectedMc.selected = False
            self.selectedMc = e.currentTarget
            self.selectedMc.selected = True
            self.selectedBatchNum = int(itemData[0])
            self.refreshBatchInfo()

    def handleItemStateChange(self, *args):
        e = ASObject(args[3][0])
        itemData = e.currentTarget.itemData
        e.currentTarget.batchNum.gotoAndStop('batchNum%d' % itemData[0])

    def getHistoryInfo(self, batchNum):
        for batchInfo in getattr(BigWorld.player(), 'historyBook', ()):
            if batchInfo[0][0] == batchNum:
                return batchInfo

    def getBatchList(self):
        historyBook = getattr(BigWorld.player(), 'historyBook', ())
        if not historyBook:
            return []
        batchList = []
        wingGroupId = BigWorld.player().getWingGroupId()
        for batchInfo in historyBook:
            if not batchInfo[1] and not batchInfo[2]:
                continue
            if batchInfo[0][1] == wingGroupId:
                batchList.append((batchInfo[0][0], batchInfo[0][1]))

        return batchList

    def refreshBatchInfo(self):
        if self.selectedBatchNum > 0:
            batchInfo = self.getHistoryInfo(self.selectedBatchNum)
            if not batchInfo:
                return
            hostName, guildName, kingName, joinCnt, winCnt = batchInfo[1] if batchInfo[1] else ('', '', '', 0, 0)
            isWingWorldCamp = False
            if len(batchInfo) > 3:
                isWingWorldCamp = batchInfo[3]
            if isWingWorldCamp:
                for i in xrange(3):
                    self.widget.mainMc.getChildByName('attr%d' % i).text = gameStrings.WING_WORLD_CAMP_HISTORY_ATTR_NAMES[i]

                self.widget.mainMc.desc.text = gameStrings.WING_WORLD_CAMP_HISTORY_DESC
            else:
                for i in xrange(3):
                    self.widget.mainMc.getChildByName('attr%d' % i).text = gameStrings.WING_WORLD_HISTORY_ATTR_NAMES[i]

                self.widget.mainMc.desc.text = gameStrings.WING_WORLD_HISTORY_DESC
            cityList = batchInfo[2]
            if not hostName:
                self.widget.mainMc.txtServerName.text = gameStrings.WING_WORLD_NO_KING_COUNTRY
            else:
                self.widget.mainMc.txtServerName.text = gameStrings.WING_WORLD_KING_COUNTRY_NAME % hostName
            if not guildName:
                self.widget.mainMc.txtKinderName.text = gameStrings.WING_WORLD_NO_KING_COUNTRY_KING_NAME
            else:
                self.widget.mainMc.txtKinderName.text = gameStrings.WING_WORLD_KING_COUNTRY_KING_NAME % (guildName, kingName)
            self.widget.mainMc.history.text = gameStrings.WING_WORLD_HISTORY_OVER_VIEW % (joinCnt, winCnt)
            self.widget.mainMc.scrollList.dataArray = cityList

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        batchList = self.getBatchList()
        if not self.selectedBatchNum and batchList:
            self.selectedBatchNum = batchList[-1][0]
        self.widget.mainMc.pageList.data = batchList
        self.refreshBatchInfo()
        if len(batchList) > 8:
            self.widget.mainMc.pageList.validateNow()
            self.widget.mainMc.pageList.jumpToIndex(len(batchList) - 1)
