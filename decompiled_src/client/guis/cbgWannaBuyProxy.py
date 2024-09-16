#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cbgWannaBuyProxy.o
from gamestrings import gameStrings
import BigWorld
import math
import gameglobal
import uiConst
import events
import utils
import const
from uiProxy import UIProxy
from gamestrings import gameStrings
from asObject import ASUtils
from asObject import ASObject
from asObject import TipManager
from asObject import MenuManager
from guis import cbgUtils
from guis import ui
from data import cbg_config_data as CCD
import gamelog
ITEM_NUM_PER_PAGE = 6
ONSALE_ROLE_NUM_PER_PAGE = 8
ROLE_DATA_FILTER_DEFAULT = 0
ROLE_DATA_FILTER_COMBAT = 1
ROLE_DATA_FILTER_PRICE = 2

class CbgWannaBuyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CbgWannaBuyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CBG_WANNA_BUY, self.hide)

    def reset(self):
        self.currentPanel = None
        self.currentTabBtn = None
        self.buyInfo = {}
        self.onSaleRoleInfo = []
        self.currentSortKey = ROLE_DATA_FILTER_DEFAULT
        self.currentSortKeyReverse = False
        self.currentSchoolExclude = []
        self.roleListData = []
        self.selectedRoleItem = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CBG_WANNA_BUY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CBG_WANNA_BUY)
        self.reset()

    def unRegisterPanel(self):
        self.widget = None
        self.currentPanel = None
        self.currentTabBtn = None
        self.buyInfo = {}
        self.selectedRoleItem = None

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CBG_WANNA_BUY)

    def initUI(self):
        gamelog.debug('ypc@ cbgWannaBuyProxy initUI!')
        self.widget.gotobuyBtn.addEventListener(events.BUTTON_CLICK, self.handleGotoWeb, False, 0, True)
        self.widget.roleTab.addEventListener(events.BUTTON_CLICK, self.handleChangeTabClick, False, 0, True)
        self.widget.roleTab.selected = False
        self.widget.rolePanel.visible = False
        self.widget.rolePanel.counter.addEventListener(events.EVENT_COUNT_CHANGE, self.handleRolePageChange, False, 0, True)
        self.widget.rolePanel.counter.minCount = 1
        self.widget.rolePanel.counter.maxCount = 1
        self.widget.rolePanel.combatTitle.addEventListener(events.BUTTON_CLICK, self.handleCombatSortClick, False, 0, True)
        self.widget.rolePanel.combatTitle.sortIcon.visible = False
        self.widget.rolePanel.priceTitle.addEventListener(events.BUTTON_CLICK, self.handlePriceSortClick, False, 0, True)
        self.widget.rolePanel.priceTitle.sortIcon.visible = False
        self.widget.rolePanel.schoolFilter.addEventListener(events.BUTTON_CLICK, self.handleSchoolFilterClick, False, 0, True)
        self.widget.rolePanel.schoolFilterPanel.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleSchoolExcludeConfirmClick, False, 0, True)
        self.widget.rolePanel.schoolFilterPanel.visible = False
        for i in xrange(ONSALE_ROLE_NUM_PER_PAGE):
            childItem = self.widget.rolePanel.treasureList.getChildByName('roleItem%d' % i)
            childItem.addEventListener(events.MOUSE_CLICK, self.handleRoleItemSelected, False, 0, True)

        self.currentSortKey = ROLE_DATA_FILTER_DEFAULT
        self.currentSortKeyReverse = False
        self.currentSchoolExclude = []
        self.widget.moneyTab.addEventListener(events.BUTTON_CLICK, self.handleChangeTabClick, False, 0, True)
        self.widget.moneyTab.selected = False
        self.widget.moneyPanel.visible = False
        self.widget.moneyPanel.counter.addEventListener(events.EVENT_COUNT_CHANGE, self.handleMoneyPageChange, False, 0, True)
        self.widget.moneyPanel.counter.minCount = 1
        self.widget.moneyPanel.counter.maxCount = 1
        self._handleChangeTabClick(self.widget.moneyTab)
        self.queryAllData()
        self.queryAllRoleData()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshMoney()
        self.refreshRole()

    def refreshMoney(self):
        gamelog.debug('ypc@ cbgBuy refreshMoney!')
        self.buyInfo = gameglobal.rds.ui.cbgMain.genTreasureBuyInfo()
        trList = self.buyInfo.get('infoList', [])
        listNum = len(trList)
        self.widget.moneyPanel.noOrderHint.visible = listNum <= 0
        self.widget.moneyPanel.treasureList.visible = listNum > 0
        self.widget.moneyPanel.counter.maxCount = max(self._getTotalPageNum(listNum), 1)
        self.onMoneyListChangePage(0)
        self.refreshMyMoney()

    def onMoneyListChangePage(self, page):
        trList = self.buyInfo.get('infoList', [])
        listNum = len(trList)
        if page + 1 > self._getTotalPageNum(listNum):
            gamelog.debug('ypc@ cbgBuy onMoneyListChangePage page error! page = ', page)
            return
        start = page * ITEM_NUM_PER_PAGE
        end = min(start + ITEM_NUM_PER_PAGE - 1, listNum - 1)
        curList = trList[start:end + 1]
        for i in range(ITEM_NUM_PER_PAGE):
            item = self.widget.moneyPanel.treasureList.getChildByName('item%d' % i)
            if not item:
                continue
            if i > end - start:
                item.visible = False
                continue
            data = curList[i]
            item.visible = True
            textColor = cbgUtils.COLOR_ORANGE
            item.iconSlot.setItemSlotData(data)
            item.cashIcon.visible = data['itemType'] == cbgUtils.CBG_ITEM_TYPE_CASH
            item.itemName.text = data['itemName']
            item.rmbValue.text = gameStrings.TEXT_CBGWANNABUYPROXY_157 % (float(data['price']) / cbgUtils.CBG_RMB_UNIT)
            item.singlePrice.text = '%.04f' % float(data['singlePrice']) + gameStrings.CBG_BUY_UNIT
            item.leftTime.text = utils.formatTimeStr(data['tExpire'], gameStrings.CBG_BUY_TIME_FORMAT)
            item.itemName.textColor = textColor
            item.rmbValue.textColor = textColor
            item.leftTime.textColor = textColor
            item.singlePrice.textColor = textColor

    def onRoleListDataChange(self):
        self.roleListData = self._getSortedRoleListData()
        self.onRoleListChangePage(0)

    def onRoleListChangePage(self, page):
        gamelog.debug('ypc@ cbgBuy onRoleListChangePage!', page)
        if not self.roleListData:
            self.widget.rolePanel.noOrderHint.visible = True
            self.widget.rolePanel.treasureList.visible = False
            self.widget.rolePanel.counter.maxCount = 1
            return
        listNum = len(self.roleListData)
        self.widget.rolePanel.noOrderHint.visible = listNum <= 0
        self.widget.rolePanel.treasureList.visible = listNum > 0
        self.widget.rolePanel.counter.maxCount = max(self._getRoleTotalPageNum(listNum), 1)
        if listNum <= 0:
            return
        if page + 1 > self._getRoleTotalPageNum(listNum):
            gamelog.debug('ypc@ cbgBuy onRoleListChangePage page error! page = ', page)
            return
        self.widget.rolePanel.counter.count = page + 1
        start = page * ONSALE_ROLE_NUM_PER_PAGE
        end = min(start + ONSALE_ROLE_NUM_PER_PAGE - 1, listNum - 1)
        curList = self.roleListData[start:end + 1]
        for i in range(ONSALE_ROLE_NUM_PER_PAGE):
            item = self.widget.rolePanel.treasureList.getChildByName('roleItem%d' % i)
            if not item:
                continue
            if i > end - start:
                item.visible = False
                continue
            data = curList[i]
            vendeeName = data['vendeeName']
            item.visible = True
            textColor = cbgUtils.COLOR_ORANGE
            item.schoolIcon.gotoAndStop(uiConst.SCHOOL_FRAME_DESC.get(data['school'], 'shengtang'))
            item.roleName.text = data['roleName']
            item.roleName.textColor = textColor
            item.price.text = gameStrings.TEXT_CBGWANNABUYPROXY_157 % (float(data['price']) / cbgUtils.CBG_RMB_UNIT)
            item.price.textColor = textColor
            item.leftTime.text = gameStrings.CBG_BUY_ROLE_LIST_TIME_FORMAT % data['leftDays']
            item.leftTime.textColor = textColor
            item.combat.text = int(data['combat'])
            item.combat.textColor = textColor
            item.sex.text = gameStrings.CBG_BUY_ROLE_SEX_MAN if data['sex'] == const.SEX_MALE else gameStrings.CBG_BUY_ROLE_SEX_WOMAN
            item.sex.textColor = textColor
            item.level.text = int(data['level'])
            item.level.textColor = textColor
            item.targetFlag.visible = not not vendeeName
            item.highlight.visible = False
            TipManager.addTip(item.targetFlag, gameStrings.CBG_BUY_SPECIFIED_FRIEND + vendeeName)
            roleGbId = data.get('roleGbId', 0)
            if roleGbId:
                MenuManager.getInstance().registerMenuById(item, uiConst.MENU_ENTITY, {'roleName': data['roleName'],
                 'gbId': roleGbId})

    def _getTotalPageNum(self, dataNum):
        return max(math.ceil(float(dataNum) / ITEM_NUM_PER_PAGE), 1)

    def _getRoleTotalPageNum(self, dataNum):
        return max(math.ceil(float(dataNum) / ONSALE_ROLE_NUM_PER_PAGE), 1)

    def refreshRole(self):
        if not self.widget or not self.widget.rolePanel:
            return
        gamelog.debug('ypc@ cbgBuy refreshRole!')
        self.onRoleListDataChange()

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def refreshMyMoney(self):
        myMoneyInfo = gameglobal.rds.ui.cbgMain.getMyMoneyInfo()
        self.widget.cashVal.text = ASUtils.convertMoneyStr(myMoneyInfo[cbgUtils.MALL_ITEMBOX_MONEY_TYPE_CASH])

    def handleChangeTabClick(self, *args):
        if not self.widget:
            return
        e = ASObject(args[3][0])
        target = e.currentTarget
        self._handleChangeTabClick(target)

    def _handleChangeTabClick(self, target):
        if not target:
            return
        if self.currentPanel:
            self.currentPanel.visible = False
        if self.currentTabBtn:
            self.currentTabBtn.selected = False
        if target.name == 'moneyTab':
            self.widget.moneyPanel.visible = True
            self.currentPanel = self.widget.moneyPanel
            self.widget.moneyTab.selected = True
            self.currentTabBtn = self.widget.moneyTab
        elif target.name == 'roleTab':
            self.widget.rolePanel.visible = True
            self.currentPanel = self.widget.rolePanel
            self.widget.roleTab.selected = True
            self.currentTabBtn = self.widget.roleTab

    def handleMoneyPageChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        curPage = max(itemMc.count - 1, 0)
        self.onMoneyListChangePage(curPage)

    def handleRolePageChange(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        curPage = max(itemMc.count - 1, 0)
        self.onRoleListChangePage(curPage)

    def handleGotoWeb(self, *args):
        gameglobal.rds.ui.cbgMain.openTreasureWeb()

    @ui.callFilter(5, False)
    def queryAllData(self, *arg):
        BigWorld.player().base.queryAllCbgData()

    @ui.callFilter(5, False)
    def queryAllRoleData(self, *args):
        BigWorld.player().base.queryCbgRoleData()

    def _getSortedRoleListData(self, *args):
        dataList = gameglobal.rds.ui.cbgMain.getCbgOnSaleRoleData()
        if self.currentSortKey == ROLE_DATA_FILTER_DEFAULT:
            self.currentSortKeyReverse = True
        sortedList = sorted(dataList, cmp=self.__roleDataCmp)
        retList = []
        for sdata in sortedList:
            if sdata['school'] in self.currentSchoolExclude:
                continue
            retList.append(sdata)

        return retList

    def __roleDataCmp(self, x, y):
        if self.currentSortKey == ROLE_DATA_FILTER_COMBAT:
            sortKey = 'combat'
        elif self.currentSortKey == ROLE_DATA_FILTER_PRICE:
            sortKey = 'price'
        elif self.currentSortKey == ROLE_DATA_FILTER_DEFAULT:
            sortKey = 'leftTime'
        else:
            return 0
        if not x['isTarget'] and not y['isTarget']:
            return self.__getCmpReturn(x[sortKey], y[sortKey], self.currentSortKeyReverse)
        elif x['isTarget'] and y['isTarget']:
            return self.__getCmpReturn(x['leftTime'], y['leftTime'], True)
        else:
            return self.__getCmpReturn(x['isTarget'], y['isTarget'], True)

    def __getCmpReturn(self, x, y, reverse):
        greater = -1 if reverse else 1
        less = 1 if reverse else -1
        equal = 0
        if x > y:
            return greater
        elif x < y:
            return less
        else:
            return equal

    def handleCombatSortClick(self, *args):
        self.widget.rolePanel.priceTitle.sortIcon.visible = False
        self.widget.rolePanel.combatTitle.sortIcon.visible = True
        if self.currentSortKey == ROLE_DATA_FILTER_COMBAT:
            self.currentSortKeyReverse = not self.currentSortKeyReverse
            self.widget.rolePanel.combatTitle.sortIcon.gotoAndStop('down' if self.currentSortKeyReverse else 'up')
        else:
            self.currentSortKey = ROLE_DATA_FILTER_COMBAT
            self.currentSortKeyReverse = True
            self.widget.rolePanel.combatTitle.sortIcon.gotoAndStop('down')
        self.onRoleListDataChange()

    def handlePriceSortClick(self, *args):
        self.widget.rolePanel.combatTitle.sortIcon.visible = False
        self.widget.rolePanel.priceTitle.sortIcon.visible = True
        if self.currentSortKey == ROLE_DATA_FILTER_PRICE:
            self.currentSortKeyReverse = not self.currentSortKeyReverse
            self.widget.rolePanel.priceTitle.sortIcon.gotoAndStop('down' if self.currentSortKeyReverse else 'up')
        else:
            self.currentSortKey = ROLE_DATA_FILTER_PRICE
            self.currentSortKeyReverse = True
            self.widget.rolePanel.priceTitle.sortIcon.gotoAndStop('down')
        self.onRoleListDataChange()

    def handleSchoolFilterClick(self, *args):
        gamelog.debug('ypc@ handleSchoolFilterClick!')
        if self.widget.rolePanel.schoolFilterPanel.visible:
            self.widget.rolePanel.schoolFilterPanel.visible = False
            return
        gamelog.debug('ypc@ handleSchoolFilterClick!')
        self.widget.rolePanel.schoolFilterPanel.visible = True
        schoolNames = uiConst.SCHOOL_FRAME_DESC_NO_ALL.copy()
        for sid, sname in schoolNames.iteritems():
            child = self.widget.rolePanel.schoolFilterPanel.getChildByName(sname)
            if not child:
                continue
            selected = True
            for exclude in self.currentSchoolExclude:
                if sid == exclude:
                    selected = False
                    break

            child.selected = selected

    def handleSchoolExcludeConfirmClick(self, *args):
        self.currentSchoolExclude = []
        schoolNames = uiConst.SCHOOL_FRAME_DESC_NO_ALL.copy()
        for sid, sname in schoolNames.iteritems():
            child = self.widget.rolePanel.schoolFilterPanel.getChildByName(sname)
            if not child:
                continue
            if not child.selected:
                self.currentSchoolExclude.append(sid)

        self.widget.rolePanel.schoolFilterPanel.visible = False
        self.onRoleListDataChange()

    def handleRoleItemSelected(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if not target.highlight:
            return
        if self.selectedRoleItem:
            self.selectedRoleItem.highlight.visible = False
        self.selectedRoleItem = target
        self.selectedRoleItem.highlight.visible = True
