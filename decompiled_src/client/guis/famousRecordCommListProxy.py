#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/famousRecordCommListProxy.o
import BigWorld
import gameglobal
import gametypes
import uiUtils
import uiConst
import events
import const
import utils
from uiProxy import UIProxy
import datetime
from guis import asObject
from guis.asObject import ASObject
from gameStrings import gameStrings
from guis.asObject import TipManager
from guis.asObject import ASUtils
from data import famous_general_lv_data as FGLD
MAX_ITEM_NUM = 5
ITEM_Y_OFFSET = 30

class FamousRecordCommListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FamousRecordCommListProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rankInfo = {}
        self.num = 1
        self.minPage = 0
        self.maxPage = 0
        self.isReach = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_FAMOUS_RECORD_COMM_LIST, self.hidePanel)

    def hidePanel(self):
        self.clearWidget()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        self.rankInfo = {}
        self.num = 1
        self.minPage = 0
        self.maxPage = 0
        self.isReach = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAMOUS_RECORD_COMM_LIST)

    def show(self, num = -1, data = {}, isReach = False):
        if self.widget:
            self.clearWidget()
        else:
            self.isReach = isReach
            if num >= 0:
                self.num = num
            if data:
                self.refreshRankInfo(data)
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAMOUS_RECORD_COMM_LIST)
            else:
                BigWorld.player().cell.queryFamousRecordRankInfo(num, self.rankInfo.get(num, {}).get('ver', 0))

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.refreshPanel()

    def refreshPanel(self, data = {}):
        if data:
            self.refreshRankInfo(data)
        if not self.widget:
            return
        page = self.widget.pageArea.page
        dataArray = []
        length = len(self.rankInfo.get(self.num, {}).get('rank', []))
        pageCnt = length / MAX_ITEM_NUM if not length % MAX_ITEM_NUM else length / MAX_ITEM_NUM + 1
        pageNum = 1
        self.maxPage = pageCnt - 1 if pageCnt else 0
        for i in xrange(0, pageCnt):
            dataArray.append('%d/%d' % (pageNum, pageCnt))
            pageNum += 1

        if not pageCnt:
            dataArray.append('0/0')
        ASUtils.setDropdownMenuData(page, dataArray)
        page.addEventListener(events.INDEX_CHANGE, self.handlePageChange)
        page.selectedIndex = 0
        page.invalidateData()
        page.validateNow()
        self.changePage(0)
        self.refreshTime()
        self.widget.pageArea.maxPage.addEventListener(events.MOUSE_CLICK, self.handleMaxPage)
        self.widget.pageArea.minPage.addEventListener(events.MOUSE_CLICK, self.handleMinPage)
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleHidePanel)

    def refreshTime(self):
        recordInfo = gameglobal.rds.ui.famousRecord.recordInfo
        if self.num == recordInfo.get('currentRound', 0):
            days = gameglobal.rds.ui.famousRecord.getLastDays(recordInfo.get('currentWeek', 0), self.num, self.isReach)
            now = utils.getNow()
            endTime = datetime.datetime.fromtimestamp(now) + datetime.timedelta(days)
            self.widget.time.text = endTime.strftime('%Y-%m-%d 12:00')
        else:
            self.widget.time.visible = False
            self.widget.timeTxt.visible = False
            self.widget.timeIcon.visible = False

    def refreshRankInfo(self, data):
        self.rankInfo[self.num] = {}
        self.rankInfo[self.num]['ver'] = data[0]
        rank = data[1]
        self.rankInfo[self.num]['rank'] = sorted(rank, cmp=self.sortRank, reverse=True)

    def sortRank(self, item0, item1):
        if item0[3][0] > item1[3][0]:
            return 1
        if item0[3][0] < item1[3][0]:
            return -1
        if item0[3][1] > item1[3][1]:
            return 1
        if item0[3][1] < item1[3][1]:
            return -1
        if item0[3][2] > item1[3][2]:
            return 1
        if item0[3][2] < item1[3][2]:
            return -1
        if item0[3][3] < item1[3][3]:
            return 1
        if item0[3][3] > item1[3][3]:
            return -1
        return 1

    def changePage(self, index):
        posY = 0
        itemNum = 0
        for i in xrange(index * MAX_ITEM_NUM, index * MAX_ITEM_NUM + MAX_ITEM_NUM):
            rank = self.rankInfo.get(self.num, {}).get('rank', [])
            if i < len(rank):
                item = self.widget.canvas.getChildByName('item%d' % itemNum)
                if not item:
                    item = self.widget.getInstByClsName('FamousRecordCommList_Item')
                    item.name = 'item%d' % itemNum
                    item.x = 0
                    item.y = posY
                    self.widget.canvas.addChild(item)
                item.roleName.text = rank[i][1]
                item.rank.text = i + 1
                item.lv.text = FGLD.data.get(rank[i][3][0], {}).get('name', '')
                posY += 30
                itemNum += 1

        if itemNum < MAX_ITEM_NUM:
            for i in xrange(itemNum, MAX_ITEM_NUM):
                item = self.widget.canvas.getChildByName('item%d' % i)
                if item:
                    self.widget.canvas.removeChild(item)
                else:
                    break

    def handleHidePanel(self, *args):
        self.clearWidget()

    def handlePageChange(self, *args):
        index = ASObject(args[3][0]).index
        self.changePage(index)

    def handleMaxPage(self, *args):
        self.widget.pageArea.page.selectedIndex = self.maxPage

    def handleMinPage(self, *args):
        self.widget.pageArea.page.selectedIndex = self.minPage
