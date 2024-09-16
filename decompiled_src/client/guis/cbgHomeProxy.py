#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cbgHomeProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import utils
import events
import const
from gamestrings import gameStrings
from uiProxy import UIProxy
from asObject import ASObject
from asObject import ASUtils
from guis import cbgUtils
from guis import ui
from callbackHelper import Functor
import gamelog
STATE_DESC = {1: gameStrings.CBG_HOME_JISHOUZHONG,
 2: gameStrings.CBG_HOME_YICHUSHOU,
 3: gameStrings.CBG_HOME_YICHEXIAO,
 4: gameStrings.CBG_HOME_YICHENGJIAO,
 5: gameStrings.CBG_HOME_GUANBI}

class CbgHomeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CbgHomeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CBG_HOME, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CBG_HOME:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CBG_HOME)

    def unRegisterPanel(self):
        self.widget = None

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CBG_HOME)

    def initUI(self):
        gamelog.debug('ypc@ cbgHomeProxy initUI!')
        self.widget.homePanel.treasureList.itemRenderer = 'CBGHomeWidget_Treasure_HomeListItem'
        self.widget.homePanel.treasureList.dataArray = []
        self.widget.homePanel.treasureList.lableFunction = self.renderTreasureItem
        self.widget.homePanel.adIcon.addEventListener(events.MOUSE_CLICK, self.handleIconClick, False, 0, True)

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        homeInfo = gameglobal.rds.ui.cbgMain.genTreasureHomeInfo()
        trList = homeInfo.get('infoList', [])
        lenTrList = len(trList)
        self.widget.homePanel.treasureList.visible = lenTrList > 0
        if lenTrList > 0:
            self.widget.homePanel.treasureList.dataArray = trList
            self.widget.homePanel.treasureList.scrollToHead()
        self.refreshMyMoney()

    def _onConfirmBtnClick(self, e):
        print 'onConfirmBtnClick:', e.target, e.type

    def getCbgEntityId(self):
        return gameglobal.rds.ui.cbgMain.entId

    def renderTreasureItem(self, *args):
        data = ASObject(args[3][0])
        item = ASObject(args[3][1])
        if not data:
            return
        item.jobIcon.visible = False
        item.roleName.visible = False
        item.iconSlot.visible = False
        item.cashIcon.visible = False
        item.roleName.visible = False
        item.itemName.visible = False
        if data.goodsType == const.CBG_GOODS_TYPE_CASH:
            item.cashIcon.visible = data.itemType == const.CBG_ITEM_TYPE_CASH
            item.iconSlot.visible = True
            item.itemName.visible = True
        elif data.goodsType == const.CBG_GOODS_TYPE_ROLE:
            item.jobIcon.visible = True
            item.roleName.visible = True
        elif data.goodsType == const.CBG_GOODS_TYPE_ITEM:
            item.itemName.visible = True
            item.iconSlot.visible = True
        showTime = False
        if data.tradeType == cbgUtils.CBG_SEARCH_TYPE_BUY:
            textColor = cbgUtils.COLOR_PURPLE
            item.tradeType.text = gameStrings.CBG_HOME_SHOUGOU
            item.takeBtn.label = gameStrings.CBG_HOME_SHOUQU
            item.state.text = gameStrings.CBG_HOME_WEILINGQU
            item.timeField1.text = ''
            item.timeField2.text = '/'
            item.timeField2.y = 12
        else:
            textColor = cbgUtils.COLOR_ORANGE
            item.tradeType.text = gameStrings.CBG_HOME_CHUSHOU
            item.takeBtn.label = gameStrings.CBG_HOME_CHEXIAO
            item.state.text = STATE_DESC[data.opType]
            showTime = data.opType == cbgUtils.CBG_OP_TYPE_SELL
            if data.opType == cbgUtils.CBG_OP_TYPE_SELL and data.tExpire <= 0:
                item.state.text = gameStrings.CBG_HOME_GUOQI
                showTime = False
        if showTime:
            item.timeField1.text = gameStrings.CBG_HOME_SHENGYU
            item.timeField2.text = utils.formatTimeStr(data.tExpire, gameStrings.CBG_HOME_TIME_FORMAT)
            item.timeField2.y = 22
        else:
            item.timeField1.text = ''
            item.timeField2.text = '/'
            item.timeField2.y = 12
        price = data.price
        useBidPrice = False
        useBidPrice = useBidPrice or data.opType == cbgUtils.CBG_OP_TYPE_SOLD
        useBidPrice = useBidPrice or data.opType == cbgUtils.CBG_OP_TYPE_TAKEAWAY
        useBidPrice = useBidPrice or data.opType == cbgUtils.CBG_OP_TYPE_FINISH
        useBidPrice = useBidPrice and data.bidPrice
        if useBidPrice:
            price = data.bidPrice
        item.iconSlot.setItemSlotData(data)
        item.itemName.text = data.itemName
        item.rmbValue.text = gameStrings.TEXT_CBGHOMEPROXY_153 + '%.02f' % (float(price) / cbgUtils.CBG_RMB_UNIT)
        item.itemName.textColor = textColor
        item.tradeType.textColor = textColor
        item.rmbValue.textColor = textColor
        item.state.textColor = textColor
        item.timeField1.textColor = textColor
        item.timeField2.textColor = textColor
        item.shangjiaBtn.visible = False
        item.getBtn.visible = False
        item.takeBtn.visible = data.canOper
        item.takeBtn.data = data
        if not item.takeBtn.hasEventListener(events.BUTTON_CLICK):
            item.takeBtn.addEventListener(events.BUTTON_CLICK, self.btnClickListener, False, 0, True)
        item.roleName.text = ''
        if data.goodsType == const.CBG_GOODS_TYPE_ROLE:
            item.roleName.text = data.roleName
            schoolFrameName = uiConst.SCHOOL_FRAME_DESC.get(data.roleSchool)
            gamelog.debug('ypc@ renderTreasureItem ', data.roleName, data.roleSchool, schoolFrameName)
            item.jobIcon.gotoAndStop(schoolFrameName)

    def btnClickListener(self, *args):
        e = ASObject(args[3][0])
        gamelog.debug('ypc@ btnClickListener!')
        if e.target.name == 'takeBtn':
            data = e.target.data
            tradeType = data.tradeType
            cbgId = data.cbgId
            if tradeType == const.CBG_SEARCH_TYPE_OWN:
                msg = gameStrings.CBG_HOME_MSG_TIP_1
            else:
                msg = gameStrings.CBG_HOME_MSG_TIP_2
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmCancelCbgItem, tradeType, cbgId))

    def handleIconClick(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx != events.LEFT_BUTTON:
            return
        gameglobal.rds.ui.cbgMain.openTreasureWeb()

    @ui.checkInventoryLock()
    def onConfirmCancelCbgItem(self, tradeType, cbgId):
        p = BigWorld.player()
        if not self.getCbgEntityId():
            return
        ent = BigWorld.entities.get(self.getCbgEntityId())
        if not ent:
            return
        if tradeType == const.CBG_SEARCH_TYPE_OWN:
            ent.cell.takeBackCBGCash(cbgId, p.cipherOfPerson)
        else:
            ent.cell.takeAwayCBGCash(cbgId, p.cipherOfPerson)

    def refreshMyMoney(self):
        myMoneyInfo = gameglobal.rds.ui.cbgMain.getMyMoneyInfo()
        self.widget.homePanel.cashVal.text = ASUtils.convertMoneyStr(myMoneyInfo[cbgUtils.MALL_ITEMBOX_MONEY_TYPE_CASH])
