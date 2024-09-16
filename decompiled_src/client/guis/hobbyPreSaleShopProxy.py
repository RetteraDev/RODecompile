#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/hobbyPreSaleShopProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import const
import utils
from uiProxy import UIProxy
from guis.asObject import ASObject
from gameStrings import gameStrings
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import hobby_presale_schedule_data as HPSD
from data import hobby_presale_config_data as HPCD
MAX_PRESALE_GOODS = 3
TIME_LIMIT_CD = 10

class HobbyPreSaleShopProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HobbyPreSaleShopProxy, self).__init__(uiAdapter)
        self.widget = None
        self.hobbyReservedList = []
        self.resvringGoodsCD = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_HOBBY_PRESALE_SHOP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_HOBBY_PRESALE_SHOP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_HOBBY_PRESALE_SHOP)

    def reset(self):
        self.hobbyReservedList = []

    def show(self, hobbyReservedList):
        self.hobbyReservedList = hobbyReservedList or []
        if gameglobal.rds.ui.hobbyPreSaleRule.widget:
            gameglobal.rds.ui.hobbyPreSaleRule.hide()
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_HOBBY_PRESALE_SHOP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        currScheduleItems = self.getCurrScheduleItems()
        p = BigWorld.player()
        nIdex = 0
        for goodsId in sorted(currScheduleItems.keys()):
            goodsMc = self.widget.getChildByName('goods%d' % nIdex)
            tInfo = currScheduleItems[goodsId]
            path = 'advertisement/%s.dds' % tInfo.get('photo', '')
            goodsMc.icon.clear()
            goodsMc.icon.loadImage(path)
            bReserved = self.checkGoodsReserved(goodsId)
            deposit = HPCD.data.get('deposit', {})
            myYunChui = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
            strDeposit = str(deposit)
            btnCD = 0
            if goodsId in self.resvringGoodsCD:
                btnCD = utils.getNow() - self.resvringGoodsCD[goodsId]
            if bReserved:
                goodsMc.order.label = gameStrings.HOBBY_PRESALE_ALREADY_RESERVE
                goodsMc.order.enabled = False
            elif btnCD > 0 and btnCD <= TIME_LIMIT_CD:
                goodsMc.order.label = gameStrings.HOBBY_PRESALE_RESERVEING
                goodsMc.order.enabled = False
            elif myYunChui < deposit:
                strDeposit = "<font color=\'#FF0000\'>%s</font>" % deposit
                goodsMc.order.label = gameStrings.HOBBY_PRESALE_RESERVE
                goodsMc.order.enabled = False
            else:
                goodsMc.order.label = gameStrings.HOBBY_PRESALE_RESERVE
                goodsMc.order.enabled = True
            goodsMc.orderCash.htmlText = strDeposit
            goodsMc.orderIcon.bonusType = 'yunChui'
            goodsMc.goodsName = tInfo.get('name', '')
            goodsMc.goodsId = goodsId
            goodsMc.deposit = deposit
            goodsMc.order.addEventListener(events.MOUSE_CLICK, self.handleReserveClick, False, 0, True)
            nIdex = nIdex + 1

    def handleReserveClick(self, *args):
        e = ASObject(args[3][0])
        goodsMc = e.currentTarget.parent
        msg = GMD.data.get(GMDD.data.HOBBY_PRESALE_CONSUME_YUNCHUI_RESERVE, {}).get('text', '') % (goodsMc.deposit, goodsMc.goodsName)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onSureBuy, e.currentTarget, goodsMc.goodsId))

    def onSureBuy(self, orderBtn, goodsId):
        orderBtn.label = gameStrings.HOBBY_PRESALE_RESERVEING
        orderBtn.enabled = False
        self.resvringGoodsCD[goodsId] = utils.getNow()
        BigWorld.callback(TIME_LIMIT_CD, Functor(self.updateOrderBtnState, orderBtn, goodsId))
        endTime = HPSD.data.get(goodsId, {}).get('endTime', 0)
        nowTime = utils.getNow()
        if nowTime > utils.getTimeSecondFromStr(endTime):
            msg = HPCD.data.get('endTimeRrviewMsg', '')
            gameglobal.rds.ui.messageBox.showMsgBox(msg, self.hide)
        else:
            msg = HPCD.data.get('waitingRrviewMsg', '')
            gameglobal.rds.ui.messageBox.showMsgBox(msg, self.hide)
            p = BigWorld.player()
            p.cell.applyExternalMallCode(goodsId)

    def getCurrScheduleItems(self):
        currBatch = 1
        nowTime = utils.getNow()
        timeList = HPCD.data.get('presaleTimeCfg', {})
        for batch in timeList:
            beginTime = timeList[batch][0]
            endTime = timeList[batch][1]
            if nowTime >= utils.getTimeSecondFromStr(beginTime) and nowTime <= utils.getTimeSecondFromStr(endTime):
                currBatch = batch
                break

        scheduleData = {}
        for goodsId in HPSD.data:
            tInfo = HPSD.data.get(goodsId, {})
            batch = tInfo.get('batch', 0)
            if batch == currBatch:
                scheduleData[goodsId] = tInfo

        return scheduleData

    def checkGoodsReserved(self, goodsId):
        for tInfo in self.hobbyReservedList:
            if tInfo.get('itemId', 0) == goodsId:
                return True

        return False

    def updateOrderBtnState(self, orderBtn, goodsId):
        if not self.widget:
            return
        nowTime = utils.getNow()
        for i, id in enumerate(self.resvringGoodsCD):
            if goodsId != id:
                continue
            bReserved = self.checkGoodsReserved(goodsId)
            time = self.resvringGoodsCD[goodsId]
            if not bReserved and nowTime - time >= TIME_LIMIT_CD:
                orderBtn.label = gameStrings.HOBBY_PRESALE_RESERVE
                orderBtn.enabled = True

    def setResetResveringGoodsCd(self, goodsId):
        if goodsId in self.resvringGoodsCD:
            self.resvringGoodsCD.pop(goodsId)
