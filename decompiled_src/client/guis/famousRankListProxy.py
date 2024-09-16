#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/famousRankListProxy.o
import BigWorld
import gameglobal
import gametypes
import uiUtils
import uiConst
import events
import const
import copy
import utils
import clientUtils
import clientcom
from uiProxy import UIProxy
import datetime
import calendar
import time
from guis import asObject
from guis.asObject import ASObject
from gameStrings import gameStrings
from guis.asObject import TipManager
from data import famous_general_lv_data as FGLD
from data import famous_general_config_data as FGCD
from data import mail_template_data as MTD
from data import famous_general_zhanxun_rank_data as FGZRD
import gamelog
ZHAN_XUN_TAB_IDX = 0
FAMOUS_TAB_IDX = 1
MOST_FAMOUS_TAB_IDX = 2
LV_NUM = 1
RANK_AREA_DICT = {ZHAN_XUN_TAB_IDX: 'FamousRankList_WeekZhanxunPanel',
 FAMOUS_TAB_IDX: 'FamousRankList_FamousPanel',
 MOST_FAMOUS_TAB_IDX: 'FamousRankList_MostFamousPanel'}
RANK_ITEM_DICT = {ZHAN_XUN_TAB_IDX: 'FamousRankList_WeekZhanxunItem',
 FAMOUS_TAB_IDX: 'FamousRankList_FamousItem',
 MOST_FAMOUS_TAB_IDX: 'FamousRankList_MostFamousItem'}
LV = 'allLv_%d'
MOST_FAMOUS_ALL_SCHOOL_MAX = 5
RANK_ITEM_HEIGHT_DICT = {ZHAN_XUN_TAB_IDX: 29,
 FAMOUS_TAB_IDX: 34,
 MOST_FAMOUS_TAB_IDX: 24}
MOST_FAMOUS_SCHOOL_NUM_LIMIT = 5

class FamousRankListProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FamousRankListProxy, self).__init__(uiAdapter)
        self.widget = None
        self.famousRankInfo = {}
        self.weekZhanxunInfo = {}
        self.famousRankItem = {}
        self.weekZhanxunItem = {}
        self.mostFamousInfo = {}
        self.mostFamousItem = {}
        self.tabIdx = 0
        self.oldTabIdx = 0
        self.myRank = -1
        self.schoolSelected = 0
        self.mostFamousRank = 1
        self.key = 'allLv_0'
        self.myPos = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_FAMOUS_RANK_LIST, self.hidePanel)

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()

    def show(self, tabIdx = 0):
        if not self.widget:
            self.tabIdx = tabIdx
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FAMOUS_RANK_LIST)
        else:
            self.clearWidget()

    def initUI(self):
        self.widget.allRank.selected = True
        if self.tabIdx == ZHAN_XUN_TAB_IDX:
            self.widget.weekZhanxunBtn.selected = True
        self.widget.weekZhanxunBtn.data = ZHAN_XUN_TAB_IDX
        self.widget.weekZhanxunBtn.addEventListener(events.MOUSE_CLICK, self.handleClickTab)
        if self.tabIdx == FAMOUS_TAB_IDX:
            self.widget.famousBtn.selected = True
        self.widget.famousBtn.data = FAMOUS_TAB_IDX
        self.widget.famousBtn.addEventListener(events.MOUSE_CLICK, self.handleClickTab)
        if self.tabIdx == MOST_FAMOUS_TAB_IDX:
            self.widget.mostFamousBtn.selected = True
        self.widget.mostFamousBtn.data = MOST_FAMOUS_TAB_IDX
        self.widget.mostFamousBtn.addEventListener(events.MOUSE_CLICK, self.handleClickTab)
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.handleHidePanel)
        self.widget.updateBtn.addEventListener(events.MOUSE_CLICK, self.handleUpdate)
        self.widget.myRank.enabled = False
        for i in xrange(0, len(const.SCHOOL_SET)):
            schoolBtn = self.widget.getChildByName('school%d' % const.SCHOOL_SET[i])
            schoolBtn.label = const.SCHOOL_DICT[const.SCHOOL_SET[i]]
            schoolBtn.icon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(const.SCHOOL_SET[i], 'yuxu'))
            schoolBtn.data = const.SCHOOL_SET[i]
            schoolBtn.addEventListener(events.MOUSE_CLICK, self.handleClickSchool)

        if clientcom.enableNewSchoolTianZhao():
            self.widget.getChildByName('school%d' % const.SCHOOL_TIANZHAO).visible = True
        else:
            self.widget.getChildByName('school%d' % const.SCHOOL_TIANZHAO).visible = False
        self.widget.allRank.data = 0
        self.widget.allRank.addEventListener(events.MOUSE_CLICK, self.handleClickSchool)
        self.requireForTopData()
        self.refreshPanel()
        self.initTime()
        self.refreshDesc()

    def refreshDesc(self):
        self.widget.desc.text = FGCD.data.get('famousRankRule', ['', '', ''])[self.tabIdx]

    def initTime(self):
        now = utils.getNow()
        timeFormat = utils.localtimeEx(now)
        dateTime = datetime.datetime(timeFormat.tm_year, timeFormat.tm_mon, timeFormat.tm_mday)
        oneDay = datetime.timedelta(days=1)
        while dateTime.weekday() != calendar.SUNDAY:
            dateTime += oneDay

        self.widget.stopTimeTxt.text = dateTime.strftime('%Y-%m-%d')

    def refreshPanel(self):
        rankArea = self.widget.getChildByName('rankArea')
        if rankArea:
            if self.oldTabIdx != self.tabIdx:
                self.widget.removeChild(rankArea)
                self.createRankArea()
        else:
            self.createRankArea()
        if self.tabIdx == ZHAN_XUN_TAB_IDX:
            self.widget.stopTimeTxt.visible = True
            self.widget.myRankText.visible = True
            self.setZhanxunRankPanel()
        elif self.tabIdx == FAMOUS_TAB_IDX:
            self.widget.stopTimeTxt.visible = False
            self.widget.myRankText.visible = False
            self.setFamousRankPanel()
        elif self.tabIdx == MOST_FAMOUS_TAB_IDX:
            self.widget.stopTimeTxt.visible = False
            self.widget.myRankText.visible = False
            self.setMostFamousRankPanel()
        self.refreshMyRankBtn()

    def refreshMyRankBtn(self):
        p = BigWorld.player()
        isFindMyRank = False
        index = 0
        rankItem = []
        if self.tabIdx == ZHAN_XUN_TAB_IDX:
            rankItem = self.weekZhanxunItem.get(self.key, [])
        elif self.tabIdx == FAMOUS_TAB_IDX:
            rankItem = self.famousRankItem.get(self.key, [])
        elif self.tabIdx == MOST_FAMOUS_TAB_IDX:
            rankItem = self.mostFamousItem.get(self.key, [])
        for item in rankItem:
            if item.get('gbId', 0) == p.gbId:
                isFindMyRank = True
                break
            else:
                index += 1

        if not isFindMyRank:
            self.widget.myRank.enabled = False
            self.myPos = 0
        else:
            self.widget.myRank.enabled = True
            self.widget.myRank.addEventListener(events.MOUSE_CLICK, self.handleClickMyRank)
            self.myPos = index * RANK_ITEM_HEIGHT_DICT[self.tabIdx]

    def createRankArea(self):
        rankArea = self.widget.getInstByClsName(RANK_AREA_DICT[self.tabIdx])
        rankArea.list.itemHeight = 29
        rankArea.x = 195
        rankArea.y = 180
        rankArea.name = 'rankArea'
        self.widget.addChild(rankArea)

    def setFamousRankPanel(self):
        rankArea = self.widget.getChildByName('rankArea')
        rankArea.list.itemRenderer = RANK_ITEM_DICT[self.tabIdx]
        rankArea.list.dataArray = self.famousRankItem.get(self.key, [])
        rankArea.list.lableFunction = self.famousItemFunction
        rankArea.list.itemHeight = 44

    def setZhanxunRankPanel(self):
        rankArea = self.widget.getChildByName('rankArea')
        rankArea.list.itemRenderer = RANK_ITEM_DICT[self.tabIdx]
        rankArea.list.dataArray = self.weekZhanxunItem.get(self.key, [])
        rankArea.list.lableFunction = self.zhanxunItemFunction
        rankArea.list.itemHeight = 29

    def setMostFamousRankPanel(self):
        rankArea = self.widget.getChildByName('rankArea')
        rankArea.list.itemRenderer = RANK_ITEM_DICT[self.tabIdx]
        rankArea.list.dataArray = self.mostFamousItem.get(self.key, [])
        rankArea.list.lableFunction = self.mostFamousItemFunction
        rankArea.list.itemHeight = 24

    def famousItemFunction(self, *args):
        p = BigWorld.player()
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        if long(data.gbId) == p.gbId:
            item.btn.selected = True
        else:
            item.btn.selected = False
        item.btn.fixedSize = True
        item.btn.rank.text = data.index
        item.btn.playerName.text = data.roleName
        item.btn.school.text = const.SCHOOL_DICT[data.school]
        famousLv = data.val[0]
        item.btn.famousLvName.text = FGLD.data.get(famousLv, {}).get('name', '')
        index = self.getFamousRankIndex(data.roleName)
        itemId = self.getFamousItemIdFromRank(index)
        if not itemId:
            item.bonus.visible = False
        else:
            item.bonus.visible = True
            TipManager.addItemTipById(item.bonus, itemId)
            itemInfo = uiUtils.getGfxItemById(itemId)
            item.bonus.setItemSlotData(itemInfo)
        item.bonus.validateNow()
        item.btn.dashLine.validateNow()

    def getFamousRankIndex(self, roleName):
        items = self.famousRankItem['allLv_0']
        for item in items:
            if item['roleName'] == roleName:
                return item['index']

    def getFamousItemIdFromRank(self, rank):
        bonusData = FGCD.data.get('famousGeneralLvRewardList', [])
        for item in bonusData:
            if rank >= item[0] and rank <= item[1]:
                bonusId = MTD.data.get(item[2], {}).get('bonusId', 0)
                itemBonus = clientUtils.genItemBonus(bonusId)
                return itemBonus[0][0]

        return 0

    def zhanxunItemFunction(self, *args):
        p = BigWorld.player()
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        if long(data.gbId) == p.gbId:
            item.selected = True
        else:
            item.selected = False
        item.fixedSize = True
        item.rank.text = data.index
        item.playerName.text = data.roleName
        item.zhanxunVal.text = data.val[0]
        index = self.getZhanxunRankIndex(data.roleName)
        item.weiWangVal.text = self.getWeiWangFromRank(index)
        item.dashLine.validateNow()

    def getZhanxunRankIndex(self, roleName):
        items = self.weekZhanxunItem['allLv_0']
        for item in items:
            if item['roleName'] == roleName:
                return item['index']

    def getWeiWangFromRank(self, rank):
        weiWangData = FGZRD.data
        for key, value in weiWangData.iteritems():
            if rank >= key[0] and rank <= key[1]:
                if gameglobal.rds.ui.roleInformationJunjie.extraExp:
                    rewardFamousGeneralVal = int(value.get('rewardFamousGeneralVal', 0) * gameglobal.rds.ui.roleInformationJunjie.extraExp)
                else:
                    rewardFamousGeneralVal = value.get('rewardFamousGeneralVal', 0)
                return rewardFamousGeneralVal

        return 0

    def mostFamousItemFunction(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        if data.seasonTxt:
            item.gotoAndStop('seasonName')
            item.item.rank.text = data.seasonTxt
            item.item.dashLine.validateNow()
            self.mostFamousRank = 1
        else:
            p = BigWorld.player()
            item.gotoAndStop(12)
            if long(data.gbId) == p.gbId:
                item.rankItem.selected = True
            else:
                item.rankItem.selected = False
            item.rankItem.fixedSize = True
            item.rankItem.rank.text = self.mostFamousRank
            self.mostFamousRank += 1
            item.rankItem.playerName.text = data.roleName
            lvName = FGLD.data.get(data.famousGeneralLv, {}).get('name', '')
            item.rankItem.lv.text = lvName
            item.rankItem.famousVal.text = data.famousGeneralVal
            item.rankItem.dashLine.validateNow()

    def refreshMostFamousRankInfo(self, data):
        if not self.widget:
            return
        self.mostFamousInfo = data
        self.getMostFamousItems()
        self.refreshPanel()

    def getMostFamousItems(self):
        selectedLv = self.key.replace('_%d' % self.schoolSelected, '')
        self.mostFamousItem[self.key] = []
        seasonTxtConfig = FGCD.data.get('seasonTimes', ())
        for idx, content in self.mostFamousInfo.iteritems():
            realIdx = idx - 1
            if realIdx < 0 or realIdx >= len(seasonTxtConfig):
                gamelog.debug('ypc@ getMostFamousItems config error! season idx = ', idx)
                continue
            if not content:
                continue
            seasonTxt = seasonTxtConfig[realIdx].split(' ')[0]
            self.mostFamousItem[self.key].append({'seasonTxt': seasonTxt})
            if selectedLv == 'allLv':
                items = self.getAllLvMostFamousItems(content)
            else:
                items = content.get(selectedLv, {})
            itemList = []
            if self.schoolSelected:
                rankItems = items.get(self.schoolSelected, {})
                for gbId, rankItem in rankItems.iteritems():
                    item = copy.deepcopy(rankItem)
                    item['gbId'] = gbId
                    itemList.append(item)

                itemList = sorted(itemList, cmp=self.sortMostFamousRank, reverse=True)
            else:
                for school, rankItems in items.iteritems():
                    for gbId, rankItem in rankItems.iteritems():
                        item = copy.deepcopy(rankItem)
                        item['gbId'] = gbId
                        itemList.append(item)

                itemList = sorted(itemList, cmp=self.sortMostFamousRank, reverse=True)
                if len(itemList) > MOST_FAMOUS_ALL_SCHOOL_MAX:
                    length = len(itemList)
                    for i in xrange(MOST_FAMOUS_ALL_SCHOOL_MAX, length):
                        itemList.pop()

            self.mostFamousItem[self.key].extend(itemList)

    def getAllLvMostFamousItems(self, content):
        items = {}
        itemArray = {}
        for key, value in content.iteritems():
            for school, item in value.iteritems():
                if not itemArray.get(school, {}):
                    itemArray[school] = []
                sortedItems = []
                for gbId, rankInfo in item.iteritems():
                    sortedItem = copy.deepcopy(rankInfo)
                    sortedItem['gbId'] = gbId
                    sortedItems.append(sortedItem)

                itemArray[school].extend(sortedItems)

        for key in itemArray.keys():
            itemArray[key] = sorted(itemArray[key], cmp=self.sortMostFamousRank, reverse=True)

        for school, values in itemArray.iteritems():
            if not items.get(school, {}):
                items[school] = {}
            for i in xrange(0, len(values)):
                if i < MOST_FAMOUS_SCHOOL_NUM_LIMIT:
                    items[school][values[i]['gbId']] = values[i]
                else:
                    break

        return items

    def sortMostFamousRank(self, item0, item1):
        if item0.get('famousGeneralLv', 0) > item1.get('famousGeneralLv', 0):
            return 1
        if item0.get('famousGeneralLv', 0) < item1.get('famousGeneralLv', 0):
            return -1
        if item0.get('famousGeneralVal', 0) > item1.get('famousGeneralVal', 0):
            return 1
        if item0.get('famousGeneralVal', 0) < item1.get('famousGeneralVal', 0):
            return -1
        if item0.get('combatPowner', 0) > item1.get('combatPowner', 0):
            return 1
        if item0.get('combatPowner', 0) < item1.get('combatPowner', 0):
            return -1
        if item0.get('timestamp', 0) > item1.get('timestamp', 0):
            return 1
        if item0.get('timestamp', 0) < item1.get('timestamp', 0):
            return -1
        return 0

    def refreshFamousRankInfo(self, data):
        if not self.widget:
            return
        itemData = data.get('data', [])
        if not itemData:
            return
        realKey = self.getRealKey()
        self.famousRankInfo[realKey] = data
        itemData = sorted(itemData, cmp=self.sortFamousRank, reverse=True)
        self.refreshItem(self.famousRankItem, itemData, self.key)
        self.refreshPanel()

    def refreshItem(self, itemDict, itemData, key):
        if key.find('allLv') != -1:
            for i in xrange(0, len(const.SCHOOL_SET)):
                tempItemData = []
                for item in itemData:
                    if item.get('school', 0) == const.SCHOOL_SET[i]:
                        tempItemData.append(copy.deepcopy(item))

                tempKey = 'allLv_%d' % const.SCHOOL_SET[i]
                self.refreshItemFromItemData(itemDict, tempItemData, tempKey)

            self.refreshItemFromItemData(itemDict, itemData, 'allLv_0')
        else:
            self.refreshItemFromItemData(itemDict, itemData, key)

    def refreshItemFromItemData(self, itemDict, itemData, key):
        itemDict[key] = []
        for i in xrange(0, len(itemData)):
            item = copy.deepcopy(itemData[i])
            item['index'] = i + 1
            itemDict[key].append(item)

    def sortFamousRank(self, item0, item1):
        val0 = item0.get('val', (0, 0))
        val1 = item1.get('val', (0, 0))
        if val0[0] > val1[0]:
            return 1
        if val0[0] < val1[0]:
            return -1
        if val0[1] > val1[1]:
            return 1
        if val0[1] < val1[1]:
            return -1
        if val0[2] > val1[2]:
            return 1
        if val0[2] < val1[2]:
            return -1
        if val0[3] < val1[3]:
            return 1
        if val0[3] > val1[3]:
            return -1
        return 1

    def sortZhanxunRank(self, item0, item1):
        val0 = item0.get('val', (0, 0))
        val1 = item1.get('val', (0, 0))
        if val0[0] > val1[0]:
            return 1
        if val0[0] < val1[0]:
            return -1
        if val0[1] > val1[1]:
            return 1
        if val0[1] < val1[1]:
            return -1
        return 1

    def refreshZhanxunRankInfo(self, data):
        if not self.widget:
            return
        itemData = data.get('data', [])
        itemData = sorted(itemData, cmp=self.sortZhanxunRank, reverse=True)
        if not itemData:
            return
        realKey = self.getRealKey()
        self.weekZhanxunInfo[realKey] = data
        self.refreshItem(self.weekZhanxunItem, itemData, self.key)
        self.refreshPanel()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.widget = None
        self.key = 'allLv_0'
        self.famousRankInfo = {}
        self.weekZhanxunInfo = {}
        self.mostFamousInfo = {}
        self.famousRankItem = {}
        self.weekZhanxunItem = {}
        self.mostFamousItem = {}
        self.tabIdx = 0
        self.schoolSelected = 0
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FAMOUS_RANK_LIST)

    def requireForTopData(self):
        p = BigWorld.player()
        key = self.getRealKey()
        if self.tabIdx == ZHAN_XUN_TAB_IDX:
            self.type = gametypes.TOP_TYPE_ZHAN_XUN
            p.base.getFamousGeneralTop(self.type, self.weekZhanxunInfo.get(self.schoolSelected, {}).get('version', 0), key)
        elif self.tabIdx == FAMOUS_TAB_IDX:
            self.type = gametypes.TOP_TYPE_FAMOUS_GENERAL_LV
            p.base.getFamousGeneralTop(self.type, self.famousRankInfo.get(self.schoolSelected, {}).get('version', 0), key)
        elif self.tabIdx == MOST_FAMOUS_TAB_IDX:
            p.cell.queryLastSeasonsBakInfo()

    def getRealKey(self):
        key = self.key
        if self.key.find('allLv') != -1:
            key = 'allLv'
        return key

    def hidePanel(self):
        self.clearWidget()

    def handleClickTab(self, *args):
        self.oldTabIdx = self.tabIdx
        e = ASObject(args[3][0])
        target = e.currentTarget
        self.tabIdx = int(target.data)
        if self.oldTabIdx != self.tabIdx:
            self.requireForTopData()
        self.refreshPanel()
        self.refreshDesc()

    def handleClickSchool(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        selectedSchool = int(target.data)
        self.schoolSelected = selectedSchool
        self.key = LV % selectedSchool
        if self.tabIdx == MOST_FAMOUS_TAB_IDX:
            self.getMostFamousItems()
            self.refreshPanel()
        else:
            if self.tabIdx == FAMOUS_TAB_IDX:
                if not self.famousRankItem.get(self.key, []):
                    self.requireForTopData()
            elif self.tabIdx == ZHAN_XUN_TAB_IDX:
                if not self.weekZhanxunItem.get(self.key, []):
                    self.requireForTopData()
            self.refreshPanel()

    def handleHidePanel(self, *args):
        self.clearWidget()

    def handleUpdate(self, *args):
        self.requireForTopData()

    def handleClickMyRank(self, *args):
        rankArea = self.widget.getChildByName('rankArea')
        rankArea.list.scrollTo(self.myPos)
