#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cbgSellConfirmProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import math
from uiProxy import UIProxy
from guis import cbgUtils
from guis import uiUtils
from gamestrings import gameStrings
from asObject import ASObject
from data import cbg_config_data as CCD

class CbgSellConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CbgSellConfirmProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.showType = cbgUtils.CBG_CONFIRM_SHOW_TYPE_MONEY
        uiAdapter.registerEscFunc(uiConst.WIDGET_CBG_SELL_CONFIRM, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CBG_SELL_CONFIRM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CBG_SELL_CONFIRM)

    def show(self, showType):
        self.showType = showType
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CBG_SELL_CONFIRM, True, True)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = [self.widget.closeBtn, self.widget.cancelBtn]
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.btnClickListener)
        self.widget.rolePanel.ruleCheckBox.addEventListener(events.EVENT_SELECT, self.handleAgreeRoleSellRuleListner, False, 0, True)
        self.widget.rolePanel.rule.addEventListener(events.MOUSE_CLICK, self.handleRoleSellRuleClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        if self.showType == cbgUtils.CBG_CONFIRM_SHOW_TYPE_MONEY:
            self.widget.moneyPanel.visible = True
            self.widget.rolePanel.visible = False
            self.refreshMoneyInfo()
        elif self.showType == cbgUtils.CBG_CONFIRM_SHOW_TYPE_ROLE:
            self.widget.moneyPanel.visible = False
            self.widget.rolePanel.visible = True
            self.refreshRoleInfo()

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def refreshMoneyInfo(self):
        self.widget.confirmBtn.enabled = True
        moneyInfo = gameglobal.rds.ui.cbgMain.genTreasureMoneyConfirmInfo()
        cash = moneyInfo['cash'] / cbgUtils.CBG_TRADE_UNIT
        price = moneyInfo['price'] / cbgUtils.CBG_RMB_UNIT
        singlePrice = float(price / cash)
        colorKeys = moneyInfo['priceColorKeys']
        colorVals = moneyInfo['priceColorVals']
        defColor = moneyInfo['defaultPriceColor']
        colorKeysCash = moneyInfo['cashColorKeys']
        colorValsCash = moneyInfo['cashColorVals']
        defColorCash = moneyInfo['defaultCashColor']
        priceColor = '#' + hex(gameglobal.rds.ui.cbgWannaSell.priceTextColor(price, colorKeys, colorVals, defColor))
        cashColor = '#' + hex(gameglobal.rds.ui.cbgWannaSell.priceTextColor(cash, colorKeysCash, colorValsCash, defColorCash))
        self.widget.moneyPanel.iconSlot.setItemSlotData(moneyInfo)
        self.widget.moneyPanel.priceTips.htmlText = gameStrings.CBG_SELL_CONFIRM_STR_PRICE_TIPS % (str(priceColor), '%.02f' % price)
        self.widget.moneyPanel.cashTips.htmlText = gameStrings.CBG_SELL_CONFIRM_STR_CASH_TIPS % (str(cashColor), str(cash))
        self.widget.moneyPanel.singlePriceLabel.text = '%.04f' % singlePrice + gameStrings.CBG_SELL_CONFIRM_UNIT
        if moneyInfo['targetRoleName']:
            self.widget.moneyPanel.targetRoleNameLabel.text = moneyInfo['targetRoleName']
        else:
            self.widget.moneyPanel.targetRoleNameLabel.text = gameStrings.TEXT_BATTLEFIELDPROXY_1605
        tax = math.ceil(price * moneyInfo['taxRate'] * 100) / 100
        tax = max(tax, moneyInfo['taxRange'][0])
        tax = min(tax, moneyInfo['taxRange'][1])
        self.widget.moneyPanel.rateTipsLabel.text = gameStrings.TEXT_CBGHOMEPROXY_153 + '%.02f' % tax

    def refreshRoleInfo(self):
        self.widget.confirmBtn.enabled = False
        self.widget.rolePanel.ruleCheckBox.selected = False
        roleSaleInfo = gameglobal.rds.ui.cbgMain.roleSaleData
        if not roleSaleInfo:
            return
        targetFriend = roleSaleInfo.get('friendName', '')
        if targetFriend:
            self.widget.rolePanel.infoPanel.gotoAndStop('you')
            self.widget.rolePanel.infoPanel.friendName.htmlText = uiUtils.toHtml(roleSaleInfo.get('friendName', ''), '#FF0000')
            self.widget.rolePanel.infoPanel.cost.htmlText = uiUtils.toHtml(CCD.data.get('roleSaleFriendTargetCoinCost', 5000), '#FF0000')
        else:
            self.widget.rolePanel.infoPanel.gotoAndStop('wu')
        p = BigWorld.player()
        self.widget.rolePanel.infoPanel.roleName.htmlText = uiUtils.toHtml(p.roleName, '#FFFF00')
        price = float(roleSaleInfo.get('price')) / 100
        self.widget.rolePanel.infoPanel.price.htmlText = uiUtils.toHtml('%.02f' % price, '#FFFF00') + gameStrings.CBG_UNIT_YUAN
        self.widget.rolePanel.infoPanel.sellTime.htmlText = uiUtils.toHtml(roleSaleInfo.get('days', 0), '#FFFF00') + gameStrings.COMMON_DAY
        afterTax = gameglobal.rds.ui.cbgWannaSell.genRoleAfterTax(price)
        self.widget.rolePanel.infoPanel.earning.htmlText = uiUtils.toHtml('%.02f' % afterTax, '#FF0000') + gameStrings.CBG_UNIT_YUAN

    def btnClickListener(self, *args):
        if self.showType == cbgUtils.CBG_CONFIRM_SHOW_TYPE_MONEY:
            gameglobal.rds.ui.cbgMain.confirmSellItem()
        elif self.showType == cbgUtils.CBG_CONFIRM_SHOW_TYPE_ROLE:
            self.hide()
            gameglobal.rds.ui.cbgMain.realSellRole()

    def handleAgreeRoleSellRuleListner(self, *args):
        self._checkConfirmBtnState()

    def handleRoleSellRuleClick(self, *args):
        gameglobal.rds.ui.cbgRule.show(cbgUtils.CBG_RULE_TYPE_SALE_SIMPLE)

    def _checkConfirmBtnState(self):
        if not self.widget:
            return
        if self.widget.rolePanel.ruleCheckBox.selected:
            self.widget.confirmBtn.enabled = True
