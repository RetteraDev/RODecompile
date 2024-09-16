#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/rankCommonMiniProxy.o
import BigWorld
import gameglobal
import uiConst
import gametypes
import gamelog
import events
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import rank_common_data as RCD
from guis.asObject import ASObject
from guis.asObject import MenuManager
from callbackHelper import Functor

class RankCommonMiniProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RankCommonMiniProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANK_COMMON_MINI, self.hide)
        self.currentTopId = -1
        self.listColX = []
        self.listColWidth = []
        self.selectItem = None
        self.updateBtnCooldownTimeDic = {}

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RANK_COMMON_MINI:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RANK_COMMON_MINI)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_RANK_COMMON_MINI)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.currentList = self.widget.listGroup.list
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleUpdateBtnClick, False, 0, True)
        self.refreshCommonRank(self.currentTopId)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def showRankCommon(self, topId):
        self.currentTopId = topId
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_RANK_COMMON_MINI)
        else:
            self.refreshCommonRank(topId)

    def refreshCommonRankView(self, cacheData):
        if not self.widget:
            return
        myRankCommon = cacheData.get('myRank', -1)
        myLastRank = cacheData.get('lastRank', -1)
        datalist = cacheData.get('list', [])
        self.widget.myRank.htmlText = gameStrings.COMMON_RANK_MY_RANK % str(myRankCommon) if myRankCommon > 0 else gameStrings.COMMON_RANK_OUT_OF_RANK
        self.widget.lastRank.htmlText = gameStrings.COMMON_RANK_LASTWEEK_RANK % (str(myLastRank) if myLastRank > 0 else '')
        self.currentList.dataArray = datalist

    def refreshCommonRank(self, topId):
        if not self.widget or topId not in RCD.data:
            return
        self.currentTopId = topId
        config = RCD.data.get(topId, {})
        self.widget.rankTitle.text = config.get('Rankingname', '')
        allColData = config.get('AllColData', None)
        if allColData:
            self.currentList.itemHeight = 37
            self.currentList.itemRenderer = 'RankCommonMini_Item'
            self.currentList.lableFunction = self.commonRankItemFunction
            self.currentList.dataArray = []
            self.listColX = []
            self.listColWidth = []
            totalWidth = 0
            colNum = len(allColData)
            for cData in allColData:
                totalWidth += cData.get('Width', 100)

            interval = max(0, (511 - totalWidth) / (colNum + 1))
            curX = 48 + interval
            for i in range(0, 5):
                mc = self.widget.listGroup.getChildByName('rankcol%d' % (i + 1))
                if i < colNum:
                    colWidth = allColData[i].get('Width', 100)
                    mc.text = allColData[i].get('Name', '')
                    mc.x = curX
                    mc.width = colWidth
                    mc.visible = True
                    self.listColX.append(curX)
                    self.listColWidth.append(colWidth)
                    curX += colWidth + interval
                else:
                    mc.visible = False

        self.widget.refreshBtn.visible = config.get('refreshBtn', False)
        self.widget.bottomRule.htmlText = config.get('BottomDesc', '')
        if config.get('Newranking', 0):
            self.widget.myRank.visible = True
            self.widget.myRank.htmlText = gameStrings.COMMON_RANK_MY_RANK % ''
        if config.get('LastWeekranking', 0):
            self.widget.lastRank.visible = True
            self.widget.lastRank.htmlText = gameStrings.COMMON_RANK_LASTWEEK_RANK % ''
        self.refreshUpdateBtnState()

    def commonRankItemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        FORMAT_COLOR = "<font color = \'#a65b11\'>%s</font>"
        config = RCD.data.get(self.currentTopId, {})
        if config:
            index = getattr(itemData, 'index', 0)
            isSelf = getattr(itemData, 'isSelf', False)
            itemMc.rank.htmlText = FORMAT_COLOR % str(index) if isSelf else index
            roleName = ''
            allColConfig = config.get('AllColData', [])
            colNum = len(allColConfig)
            itemMc.rank.x = -15
            for i in range(1, 6):
                child = itemMc.getChildByName('data%d' % i)
                data = getattr(itemData, 'data%d' % i, '')
                if i <= colNum:
                    if allColConfig[i - 1].get('DataIndex', -1) == gametypes.TOP_UNIVERSAL_ROLE_NAME:
                        roleName = getattr(itemData, 'data%d' % i, '')
                    child.htmlText = FORMAT_COLOR % data if isSelf else data
                    child.x = self.listColX[i - 1] - 9
                    child.width = self.listColWidth[i - 1]
                    child.visible = True
                else:
                    child.visible = False

            itemMc.addEventListener(events.MOUSE_CLICK, self.onItemClick, False, 0, True)
            if roleName:
                MenuManager.getInstance().registerMenuById(itemMc, uiConst.MENU_RANK, {'roleName': roleName})

    def onItemClick(self, *args):
        gamelog.debug('ypc@onItemClick')
        e = ASObject(args[3][0])
        if self.selectItem:
            self.selectItem.gotoAndStop('up')
        self.selectItem = e.currentTarget
        self.selectItem.gotoAndStop('down')

    def startUpdateBtnCooldownTimer(self):
        self.updateBtnCooldownTimeDic[self.currentTopId] = 61
        BigWorld.callback(0, Functor(self.__updateBtnTimerCallback, self.currentTopId))

    def __updateBtnTimerCallback(self, *args):
        topId = args[0]
        self.updateBtnCooldownTimeDic[topId] -= 1
        if self.updateBtnCooldownTimeDic[topId] > 0:
            BigWorld.callback(1, Functor(self.__updateBtnTimerCallback, topId))
        if self.currentTopId == topId:
            self.setUpdateBtnState(self.updateBtnCooldownTimeDic[topId])

    def refreshUpdateBtnState(self):
        self.setUpdateBtnState(self.updateBtnCooldownTimeDic.get(self.currentTopId, 0))

    def setUpdateBtnState(self, cooldownTime):
        if not self.widget:
            return
        updateBtn = self.widget.refreshBtn
        updateBtn.enabled = cooldownTime == 0
        if cooldownTime > 0:
            updateBtn.label = gameStrings.REFRESH_BTN_LABEL_CD % cooldownTime
        else:
            updateBtn.label = gameStrings.REFRESH_BTN_LABEL

    def handleUpdateBtnClick(self, *args):
        self.startUpdateBtnCooldownTimer()
        gameglobal.rds.ui.rankCommon.requestCommonRank()
