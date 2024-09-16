#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cbgWannaSellProxy.o
import BigWorld
import gameglobal
import gametypes
import uiConst
import events
import utils
import math
import const
import datetime
from uiProxy import UIProxy
from asObject import ASObject
from asObject import ASUtils
from guis import ui
from guis import cbgUtils
from data import cbg_config_data as CCD
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
import gamelog
TIP_NUM = 5
TIP_START_Y = 39

class CbgWannaSellProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CbgWannaSellProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CBG_WANNA_SELL, self.hide)

    def reset(self):
        self.currentPanel = None
        self.currentTabBtn = None
        self.sellInfo = {}
        self.myMoneyInfo = {}
        self.lastPrice = ''
        self.lastCash = ''
        self.lastRolePrice = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CBG_WANNA_SELL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.currentPanel = None
        self.currentTabBtn = None
        self.sellInfo = {}
        self.lastPrice = ''
        self.lastCash = ''
        self.lastRolePrice = ''
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CBG_WANNA_SELL)

    def unRegisterPanel(self):
        self.widget = None
        self.currentPanel = None
        self.currentTabBtn = None
        self.sellInfo = {}
        self.lastPrice = ''
        self.lastRolePrice = ''

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CBG_WANNA_SELL)

    def initUI(self):
        gamelog.debug('ypc@ cbgWannaSellProxy initUI!')
        self.widget.roleTab.addEventListener(events.BUTTON_CLICK, self.handleChangeTabClick, False, 0, True)
        self.widget.roleTab.selected = False
        self.widget.rolePanel.visible = False
        self.widget.rolePanel.selected = False
        self.widget.moneyTab.addEventListener(events.BUTTON_CLICK, self.handleChangeTabClick, False, 0, True)
        self.widget.moneyTab.selected = False
        self.widget.moneyPanel.visible = False
        self.widget.moneyPanel.cashInput.textField.restrict = '0-9'
        self.widget.moneyPanel.priceInput.textField.restrict = '0-9.'
        self.widget.moneyPanel.cashInput.addEventListener(events.EVENT_CHANGE, self.inputChangeListner, False, 0, True)
        self.widget.moneyPanel.priceInput.addEventListener(events.EVENT_CHANGE, self.inputChangeListner, False, 0, True)
        self.widget.moneyPanel.targetCheckBox.addEventListener(events.EVENT_SELECT, self.checkBoxSelectListener, False, 0, True)
        self.widget.moneyPanel.friendList.addEventListener(events.INDEX_CHANGE, self.listIndexChangeListner, False, 0, True)
        self.widget.moneyPanel.confirmBtn.addEventListener(events.BUTTON_CLICK, self.btnClickListener, False, 0, True)
        self.widget.moneyPanel.afterTax.text = '0.00' + gameStrings.CBG_UNIT_YUAN
        self._handleChangeTabClick(self.widget.moneyTab)

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshMoney()
        self.refreshRole()

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

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

    def refreshMoney(self):
        self.sellInfo = gameglobal.rds.ui.cbgMain.genTreasureSellInfo()
        tips = CCD.data.get('sellTips', ())
        for i in range(5):
            tipMc = self.widget.moneyPanel.getChildByName('tips%d' % i)
            if i < len(tips) and i >= 0:
                tipMc.htmlText = tips[i]
            else:
                tipMc.htmlText = ''

        self.widget.moneyPanel.cashInput.defaultText = gameStrings.CBG_SELL_INPUT_TIP_1 % str(self.sellInfo['cashRange'][0])
        self.widget.moneyPanel.cashInput.maxChars = self.sellInfo['cashMaxChars']
        self.widget.moneyPanel.priceInput.defaultText = gameStrings.CBG_SELL_INPUT_TIP_2 % str(self.sellInfo['priceRange'][0])
        self.widget.moneyPanel.priceInput.maxChars = self.sellInfo['priceMaxChars']
        fList = self.sellInfo['friendList']
        self.widget.moneyPanel.friendList.data = fList
        if len(fList) > 0:
            self.widget.moneyPanel.friendList.defaultText = gameStrings.CBG_SELL_FRIENDLIST_DEFAULT_1
        else:
            self.widget.moneyPanel.friendList.defaultText = gameStrings.CBG_SELL_FRIENDLIST_DEFAULT_2
        self.checkBoxSelectListener()
        self.treasureSellCheck()
        self.upateMoneyAfterTax()
        self.refreshMyMoney()

    def refreshRole(self):
        gamelog.debug('ypc@ cbgWannaSell refreshRole!')
        p = BigWorld.player()
        if not hasattr(p, 'roleSaleData'):
            return
        if p.roleSaleData.saleStatus == gametypes.ROLE_SALE_STATUS_DEFAULT:
            self.gotoPreRegistStage()
        elif p.roleSaleData.saleStatus == gametypes.ROLE_SALE_STATUS_REGISTER:
            if not gameglobal.rds.ui.cbgMain.checkSaleTime():
                gamelog.debug('ypc@ gotoRegistingStage')
                self.gotoRegistingStage()
            else:
                gamelog.debug('ypc@ gotoPostRegistStage')
                self.gotoPostRegistStage()

    def gotoPostRegistStage(self):
        self.widget.rolePanel.removeEventListener(events.EVENT_ENTER_FRAME, self.handleRegistStateCheck)
        BigWorld.callback(0.1, self._realGotoPostRegistStage)

    def _realGotoPostRegistStage(self):
        if not self.widget:
            return
        self.widget.rolePanel.gotoAndStop('postRegist')
        self.widget.rolePanel.scrollWnd.canvas.explain.htmlText = CCD.data.get('roleSellExplainProRegist', '')
        self._refreshScrollWnd()
        self.widget.rolePanel.deadline.textfield.text = self._getSaleDeadlineTxt()
        self.widget.rolePanel.warning.htmlText = self._getRoleSaleWarningText()
        self.widget.rolePanel.sellBtn.addEventListener(events.BUTTON_CLICK, self.handleSellBtnClick, False, 0, True)
        self.widget.rolePanel.priceInput.textField.restrict = '0-9.'
        self.widget.rolePanel.priceInput.addEventListener(events.EVENT_CHANGE, self.roleInputChangeListner, False, 0, True)
        self.widget.rolePanel.friendList.addEventListener(events.INDEX_CHANGE, self.roleListIndexChangeListner, False, 0, True)
        self.widget.rolePanel.targetCheckBox.enabled = True
        if gameglobal.rds.configData.get('enableCBGRoleDefaultFriendTarget', False):
            self.widget.rolePanel.targetCheckBox.selected = True
            self.widget.rolePanel.targetCheckBox.enabled = False
        if gameglobal.rds.configData.get('enableCBGRoleNotFriendTarget', False):
            self.widget.rolePanel.targetCheckBox.selected = False
            self.widget.rolePanel.targetCheckBox.enabled = False
        self.widget.rolePanel.targetCheckBox.addEventListener(events.EVENT_SELECT, self.roleCheckBoxSelectListener, False, 0, True)
        self.widget.rolePanel.priceInput.maxChars = CCD.data.get('rolePriceMaxChars', 15)
        self._updatePriceDefaultInput()
        self.widget.rolePanel.sellRule.addEventListener(events.MOUSE_CLICK, self.handleSellRuleClick, False, 0, True)
        self.widget.rolePanel.sellRule.textField.htmlText = gameStrings.CBG_SELL_SELL_RULE_TEXT
        fList = self._getLvFilterFriendList()
        self.widget.rolePanel.friendList.data = fList
        if len(fList) > 0:
            self.widget.rolePanel.friendList.defaultText = gameStrings.CBG_SELL_FRIENDLIST_DEFAULT_1
        else:
            self.widget.rolePanel.friendList.defaultText = gameStrings.CBG_SELL_FRIENDLIST_DEFAULT_2
            self.widget.rolePanel.targetCheckBox.enabled = False
            self.widget.rolePanel.friendList.enabled = False
        dayRange = CCD.data.get('roleSaleDaysRange', (3, 7))
        saleDaysList = [ {'label': str(i),
         'days': i} for i in range(dayRange[0], dayRange[1] + 1) ]
        self.widget.rolePanel.dayRange.data = saleDaysList
        self.widget.rolePanel.dayRange.defaultText = gameStrings.CBG_SELL_CHOOSE_DAY_RANGE
        self.widget.rolePanel.dayRange.selectedIndex = len(saleDaysList) - 1
        self.widget.rolePanel.dayRange.addEventListener(events.INDEX_CHANGE, self.roleListIndexChangeListner, False, 0, True)
        self._onRoleCheckBoxChanged()
        self.roleSellCheck()
        self.upateRoleAfterTax()
        gamelog.debug('ypc@ gotoPostRegistStage end!')

    def _getLvFilterFriendList(self):
        p = BigWorld.player()
        friendGroups = p.getFriendGroupOrder()
        friendList = []
        for gbId, friendInfo in p.friend.iteritems():
            if friendInfo.group not in friendGroups:
                continue
            flevel = friendInfo.getSimpleDict().get('level', 0)
            if flevel <= 1:
                continue
            info = {}
            info['gbId'] = gbId
            info['label'] = friendInfo.getFullName()
            friendList.append(info)

        return friendList

    def _refreshScrollWnd(self):
        self.widget.rolePanel.scrollWnd.barAlwaysVisible = True
        minHeight = self.widget.rolePanel.scrollWnd.canvasMask.height
        textHeight = self.widget.rolePanel.scrollWnd.canvas.explain.textHeight
        self.widget.rolePanel.scrollWnd.canvas.explain.height = max(textHeight, minHeight)
        self.widget.rolePanel.scrollWnd.refreshHeight(self.widget.rolePanel.scrollWnd.canvas.explain.height)

    def gotoRegistingStage(self):
        self.widget.rolePanel.gotoAndStop('registing')
        self.widget.rolePanel.scrollWnd.canvas.explain.htmlText = CCD.data.get('roleSellExplainRegisting', '')
        self._refreshScrollWnd()
        self.widget.rolePanel.deadline.textfield.htmlText = self._getRegistDeadlineTxt()
        self.widget.rolePanel.warning.htmlText = self._getRegistWarningText()
        self.widget.rolePanel.cancelRegBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelRegistBtnClick, False, 0, True)
        self.widget.rolePanel.addEventListener(events.EVENT_ENTER_FRAME, self.handleRegistStateCheck, False, 0, True)
        self.widget.rolePanel.registRule.addEventListener(events.MOUSE_CLICK, self.handleSellRuleClick, False, 0, True)
        self.widget.rolePanel.registRule.textField.htmlText = gameStrings.CBG_SELL_SELL_RULE_TEXT

    def gotoPreRegistStage(self):
        self.widget.rolePanel.gotoAndStop('preRegist')
        self.widget.rolePanel.scrollWnd.canvas.explain.htmlText = CCD.data.get('roleSellExplainPreRegist', '')
        self._refreshScrollWnd()
        self.widget.rolePanel.registBtn.addEventListener(events.BUTTON_CLICK, self.handleRegistBtnClick, False, 0, True)
        self.widget.rolePanel.registRule.addEventListener(events.MOUSE_CLICK, self.handleRegistRuleClick, False, 0, True)
        self.widget.rolePanel.registRule.textField.htmlText = gameStrings.CBG_SELL_REGIST_RULE_TEXT

    def handleRegistBtnClick(self, *args):
        if not self.checkRegistAvailable():
            return
        gamelog.debug('ypc@ request applyRegisterSaleRole!')
        gameglobal.rds.ui.cbgMain.startRegistRole()

    def handleRegistRuleClick(self, *args):
        gameglobal.rds.ui.cbgRule.show(cbgUtils.CBG_RULE_TYPE_REGIST_SIMPLE)

    def handleSellRuleClick(self, *args):
        gameglobal.rds.ui.cbgRule.show(cbgUtils.CBG_RULE_TYPE_SALE_SIMPLE)

    @ui.callFilter(1, True)
    def handleCancelRegistBtnClick(self, *args):
        gameglobal.rds.ui.cbgMain.requestCancelRegist()

    def handleRegistStateCheck(self, *args):
        if gameglobal.rds.ui.cbgMain.checkSaleTime():
            self.gotoPostRegistStage()

    def handleSellBtnClick(self, *args):
        friendGbId = 0
        friendName = ''
        if self.widget.rolePanel.targetCheckBox.selected and self.widget.rolePanel.friendList.selectedIndex >= 0:
            friendData = self.widget.rolePanel.friendList.selectedData
            friendGbId = long(friendData.gbId)
            friendName = friendData.label
        days = self.widget.rolePanel.dayRange.selectedData.days
        price = self.widget.rolePanel.priceInput.text
        price = float(price) if price else 0.0
        gameglobal.rds.ui.cbgMain.startSellRole({'days': days,
         'friendGbId': friendGbId,
         'price': price * 100,
         'friendName': friendName})

    def inputChangeListner(self, *args):
        e = ASObject(args[3][0])
        name = e.target.name
        if name == 'cashInput':
            if not self.checkValidNumber(self.widget.moneyPanel.cashInput):
                self.widget.moneyPanel.cashInput.text = self.lastCash
                return
            maxNum = min(self.sellInfo['cashRange'][1], int(self.myMoneyInfo[cbgUtils.MALL_ITEMBOX_MONEY_TYPE_CASH] / cbgUtils.CBG_TRADE_UNIT))
            colorKeys = self.sellInfo['cashColorKeys']
            colorVals = self.sellInfo['cashColorVals']
            defColor = self.sellInfo['defaultCashColor']
            self.lastCash = self.widget.moneyPanel.cashInput.text
        elif name == 'priceInput':
            if not self.checkValidNumber(self.widget.moneyPanel.priceInput):
                self.widget.moneyPanel.priceInput.text = self.lastPrice
                return
            maxNum = self.sellInfo['priceRange'][1]
            colorKeys = self.sellInfo['priceColorKeys']
            colorVals = self.sellInfo['priceColorVals']
            defColor = self.sellInfo['defaultPriceColor']
            self.lastPrice = self.widget.moneyPanel.priceInput.text
        else:
            return
        num = float(e.target.text) if e.target.text else 0.0
        if num > maxNum:
            num = maxNum
            e.target.text = str(num)
        e.target.textField.textColor = self.priceTextColor(num, colorKeys, colorVals, defColor)
        self.treasureSellCheck()
        self.upateMoneyAfterTax()

    def checkBoxSelectListener(self, *args):
        self.widget.moneyPanel.friendList.enabled = self.widget.moneyPanel.targetCheckBox.selected
        self.treasureSellCheck()

    def listIndexChangeListner(self, *args):
        self.treasureSellCheck()

    def btnClickListener(self, *args):
        e = ASObject(args[3][0])
        name = e.target.name
        if name == 'confirmBtn':
            roleData = None
            roleName = ''
            roleGbId = ''
            if self.widget.moneyPanel.targetCheckBox.selected and self.widget.moneyPanel.friendList.selectedIndex >= 0:
                roleData = self.widget.moneyPanel.friendList.selectedData
                roleName = roleData.label
                roleGbId = roleData.gbid
            cash = self.widget.moneyPanel.cashInput.text
            cash = int(cash) if cash else 0
            price = self.widget.moneyPanel.priceInput.text
            price = float(price) if price else 0.0
            gameglobal.rds.ui.cbgMain.openConfirmWidget(cash, price, roleName, roleGbId)

    def refreshMyMoney(self):
        self.myMoneyInfo = gameglobal.rds.ui.cbgMain.getMyMoneyInfo()
        self.widget.moneyPanel.cashVal.text = ASUtils.convertMoneyStr(self.myMoneyInfo[cbgUtils.MALL_ITEMBOX_MONEY_TYPE_CASH])
        self.treasureSellCheck()

    def checkValidNumber(self, input):
        text = input.text
        dotCount = text.count('.')
        if dotCount > 1:
            return False
        if dotCount == 1:
            if text.index('.') < len(text) - 3:
                return False
        gamelog.debug('ypc@ input is', text)
        return True

    def priceTextColor(self, price, colorKeys, colorVals, defColor):
        if not colorKeys or not colorVals:
            return defColor
        if len(colorKeys) != len(colorVals):
            return defColor
        for i in range(len(colorKeys)):
            if price >= colorKeys[i][0]:
                if price < colorKeys[i][1]:
                    return colorVals[i]

        return defColor

    def treasureSellCheck(self):
        if not self.sellInfo:
            return
        cash = self.widget.moneyPanel.cashInput.text
        price = self.widget.moneyPanel.priceInput.text
        if not cash or not price:
            self.widget.moneyPanel.confirmBtn.enabled = False
            return
        cash = float(cash)
        price = float(price)
        singlePrice = 0.0
        if price == 0 or not price or cash == 0:
            singlePrice = 0
        else:
            singlePrice = price / cash
        singlePrice = round(singlePrice * 10000) / 10000
        self.widget.moneyPanel.singlePriceTips.text = '%.04f' % singlePrice + gameStrings.CBG_SELL_SELL_UNIT
        if singlePrice > 0 and singlePrice < self.sellInfo['minPrice']:
            self.widget.moneyPanel.singlePriceTips.textColor = 13379881
        else:
            self.widget.moneyPanel.singlePriceTips.textColor = 16777191
        enableSell = True
        enableSell = enableSell and cash >= self.sellInfo['cashRange'][0]
        enableSell = enableSell and cash <= self.sellInfo['cashRange'][1]
        enableSell = enableSell and price >= self.sellInfo['priceRange'][0]
        enableSell = enableSell and price <= self.sellInfo['priceRange'][1]
        enableSell = enableSell and cash * cbgUtils.CBG_TRADE_UNIT <= self.myMoneyInfo[cbgUtils.MALL_ITEMBOX_MONEY_TYPE_CASH]
        enableSell = enableSell and not self.widget.moneyPanel.targetCheckBox.selected or self.widget.moneyPanel.targetCheckBox.selected and self.widget.moneyPanel.friendList.selectedIndex >= 0
        self.widget.moneyPanel.confirmBtn.enabled = enableSell

    def roleSellCheck(self):
        cash = self.widget.rolePanel.priceInput.text
        if not cash:
            gamelog.debug('ypc@ roleSellCheck 0')
            self.widget.rolePanel.sellBtn.enabled = False
            return
        cash = float(cash)
        enableSell = True
        if cash <= 0:
            gamelog.debug('ypc@ roleSellCheck 1')
            enableSell = False
        priceRange = self._getCurrentRoleSellRange()
        if cash < priceRange[0] or cash > priceRange[1]:
            gamelog.debug('ypc@ roleSellCheck 2')
            enableSell = False
        if self.widget.rolePanel.targetCheckBox.selected and self.widget.rolePanel.friendList.selectedIndex < 0:
            gamelog.debug('ypc@ roleSellCheck 3')
            enableSell = False
        if self.widget.rolePanel.dayRange.selectedIndex < 0:
            gamelog.debug('ypc@ roleSellCheck 4')
            enableSell = False
        self.widget.rolePanel.sellBtn.enabled = enableSell

    def sellCashDone(self):
        self.widget.moneyPanel.cashInput.text = ''
        self.widget.moneyPanel.priceInput.text = ''
        self.upateMoneyAfterTax()

    def _getRegistDeadlineTxt(self):
        p = BigWorld.player()
        now = utils.getNow()
        registDays = CCD.data.get('roleSaleRegisterDays', 14)
        deadline = registDays * const.TIME_INTERVAL_DAY
        left = max(p.roleSaleData.saleStatusTime + deadline - now, 0)
        return gameStrings.CBG_SELL_DEADLINE_REGIST % self._getCurrentLeftTime(left)

    def _getSaleDeadlineTxt(self):
        p = BigWorld.player()
        now = utils.getNow()
        registDays = CCD.data.get('roleSaleRegisterDays', 14)
        saleDays = CCD.data.get('roleSaleCanPutOnSaleDays', 14)
        deadline = (registDays + saleDays) * const.TIME_INTERVAL_DAY
        left = max(p.roleSaleData.saleStatusTime + deadline - now, 0)
        return gameStrings.CBG_SELL_DEADLINE_SALE % self._getCurrentLeftTime(left)

    def _getCurrentLeftTime(self, leftTime):
        if leftTime > const.TIME_INTERVAL_DAY:
            return str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_DAY))) + gameStrings.COMMON_DAY
        elif leftTime > const.TIME_INTERVAL_HOUR:
            return str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_HOUR))) + gameStrings.COMMON_HOUR
        elif leftTime > const.TIME_INTERVAL_MINUTE:
            return str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_MINUTE))) + gameStrings.COMMON_MINUTE
        else:
            return gameStrings.COMMON_LESSTHAN_ONE_MINUTE

    def _getRegistWarningText(self):
        p = BigWorld.player()
        template = CCD.data.get('roleRegistTimeWarning', '')
        registDays = CCD.data.get('roleSaleRegisterDays', 14)
        end = datetime.datetime.fromtimestamp(p.roleSaleData.saleStatusTime + registDays * const.TIME_INTERVAL_DAY)
        return template % (end.year,
         end.month,
         end.day,
         end.hour,
         end.minute)

    def _getRoleSaleWarningText(self):
        p = BigWorld.player()
        template = CCD.data.get('roleSellTimeWarning', '')
        registDays = CCD.data.get('roleSaleRegisterDays', 14)
        saleDays = CCD.data.get('roleSaleCanPutOnSaleDays', 14)
        end = datetime.datetime.fromtimestamp(p.roleSaleData.saleStatusTime + (registDays + saleDays) * const.TIME_INTERVAL_DAY)
        return template % (end.year,
         end.month,
         end.day,
         end.hour,
         end.minute)

    def checkRegistAvailable(self):
        p = BigWorld.player()
        if p.roleSaleData.saleStatus != gametypes.ROLE_SALE_STATUS_DEFAULT:
            return False
        return True

    def checkCancelRegistAvailable(self):
        return True

    def roleCheckBoxSelectListener(self, *args):
        gamelog.debug('ypc@ roleCheckBoxSelectListener! ', self.widget.rolePanel.targetCheckBox.selected)
        if self.widget.rolePanel.targetCheckBox.selected:
            self._setCheckBoxSelectedSafe(False)
            cost = CCD.data.get('roleSaleFriendTargetCoinCost', 5000)
            if self._isCoinEnought():
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.CBG_ROLE_TARGET_FRIEND_WARNING % int(cost), yesCallback=self._onConfirmRoleBoxChanged)
            else:
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.CBG_ROLE_TARGET_FRIEND_MONEY_NOT_ENOUGH % int(cost), yesCallback=self._openChargeWindow)
        else:
            self.widget.rolePanel.friendList.enabled = self.widget.rolePanel.targetCheckBox.selected
            self._onRoleCheckBoxChanged()

    def _onConfirmRoleBoxChanged(self):
        self._setCheckBoxSelectedSafe(True)
        self._onRoleCheckBoxChanged()

    def _setCheckBoxSelectedSafe(self, selected):
        self.widget.rolePanel.targetCheckBox.removeEventListener(events.EVENT_SELECT, self.roleCheckBoxSelectListener)
        self.widget.rolePanel.targetCheckBox.selected = selected
        self.widget.rolePanel.targetCheckBox.addEventListener(events.EVENT_SELECT, self.roleCheckBoxSelectListener, False, 0, True)

    def _onRoleCheckBoxChanged(self):
        self.widget.rolePanel.friendList.enabled = self.widget.rolePanel.targetCheckBox.selected
        self._updatePriceDefaultInput()
        self.roleSellCheck()

    def _openChargeWindow(self):
        gameglobal.rds.ui.tianyuMall.onOpenChargeWindow()

    def roleInputChangeListner(self, *args):
        e = ASObject(args[3][0])
        if e.target.name != 'priceInput':
            return
        if not self.checkValidNumber(e.target):
            self.widget.rolePanel.priceInput.text = self.lastRolePrice
            return
        maxNum = self._getCurrentRoleSellRange()[1]
        colorKeys = CCD.data.get('rolePriceColorList', {}).keys()
        colorVals = CCD.data.get('rolePriceColorList', {}).values()
        defColor = CCD.data.get('defaultCashColor', 12563609)
        self.lastRolePrice = self.widget.rolePanel.priceInput.text
        num = float(e.target.text) if e.target.text else 0.0
        if num > maxNum:
            num = maxNum
            e.target.text = str(num)
        e.target.textField.textColor = self.priceTextColor(num, colorKeys, colorVals, defColor)
        self.roleSellCheck()
        self.upateRoleAfterTax()

    def roleListIndexChangeListner(self, *args):
        self.roleSellCheck()

    def upateMoneyAfterTax(self):
        taxRate = CCD.data.get('taxRate', 0.0488)
        taxRange = CCD.data.get('taxRange', (0.01, 1000))
        price = self.widget.moneyPanel.priceInput.text
        price = float(price) if price else 0.0
        tax = math.ceil(price * taxRate * 100) / 100
        tax = max(tax, taxRange[0])
        tax = min(tax, taxRange[1])
        self.widget.moneyPanel.afterTax.text = '%0.2f' % max(0, price - tax) + gameStrings.CBG_UNIT_YUAN

    def upateRoleAfterTax(self):
        if not self.widget or self.widget.rolePanel.currentLabel != 'postRegist':
            return
        price = self.widget.rolePanel.priceInput.text
        price = float(price) if price else 0.0
        self.widget.rolePanel.afterTax.text = '%.02f' % self.genRoleAfterTax(price) + gameStrings.CBG_UNIT_YUAN

    def genRoleAfterTax(self, price):
        taxRate = CCD.data.get('roleTaxRate', 0.09)
        taxRange = CCD.data.get('roleTaxRange', (60, 1000))
        tax = math.ceil(price * taxRate * 100) / 100
        tax = max(tax, taxRange[0])
        tax = min(tax, taxRange[1])
        return max(0, price - tax)

    def _getCurrentRoleSellRange(self):
        if not self.widget.rolePanel.targetCheckBox.selected:
            return CCD.data.get('roleSalePriceRangeYuan', (10, 999999))
        else:
            return CCD.data.get('roleSalePriceRangeYuanWhenSpecifiedBuyer', (10, 999999))

    def _updatePriceDefaultInput(self):
        if not self.widget:
            return
        self.widget.rolePanel.priceInput.defaultText = gameStrings.CBG_SELL_INPUT_TIP_2 % str(self._getCurrentRoleSellRange()[0])

    def _isCoinEnought(self):
        p = BigWorld.player()
        own = p.unbindCoin + p.bindCoin
        cost = CCD.data.get('roleSaleFriendTargetCoinCost', 5000)
        return cost <= own
