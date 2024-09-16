#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCharge.o
import gameglobal
import const
import npcConst
import gamelog
from guis import events
from guis import ui
from helpers import remoteInterface
from helpers.eventDispatcher import Event

class ImpCharge(object):

    def onQueryDianka(self, commonpoints, standbypoints, specialpoints):
        self.commonPoints = commonpoints
        self.standbyPoints = standbypoints
        self.specialPoints = specialpoints
        gameglobal.rds.ui.dispatchEvent(events.EVENT_POINTS_CHANGE)

    def onBuyCoinSucc(self):
        self.queryRealNameChargeLimit()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_POINTS_EXCHANGE_DONE)

    def onBuyCoinFaild(self):
        gameglobal.rds.ui.dispatchEvent(events.EVENT_POINTS_EXCHANGE_FAILED)

    def onDianKaChargeSucc(self):
        self.queryRealNameChargeLimit()

    def getCoinRefundSucc(self, pointType, amount):
        self.queryRealNameChargeLimit()
        if self.refundCoins.has_key(pointType):
            self.refundCoins[pointType] -= amount
        if pointType == const.POINT_TYPE_REFUND_PAY:
            if self.refundCoins.get(const.POINT_TYPE_REFUND_FREE, 0) > 0:
                self.base.getCoinRefund(const.POINT_TYPE_REFUND_FREE, self.refundCoins.get(const.POINT_TYPE_REFUND_FREE, 0))

    def onQueryCoinRefund(self, pointType, amount):
        self.refundCoins[pointType] = amount
        if len(self.refundCoins) == len(const.POINT_TYPE_DESC):
            if ui.entityClicked and self.refundCoins[const.POINT_TYPE_REFUND_PAY] + self.refundCoins[const.POINT_TYPE_REFUND_FREE] > 0:
                gameglobal.rds.ui.funcNpc.openAwardPanel(npcConst.NPC_FUNC_POINT_REFUND, ui.entityClicked.id)

    def hasCoinRefund(self, cType):
        if self.refundCoins.has_key(cType):
            return True
        return False

    def doQueryCoinRefund(self):
        if self.refundCoins.get(const.POINT_TYPE_REFUND_PAY, 0) > 0:
            self.base.getCoinRefund(const.POINT_TYPE_REFUND_PAY, self.refundCoins.get(const.POINT_TYPE_REFUND_PAY, 0))
        elif self.refundCoins.get(const.POINT_TYPE_REFUND_FREE, 0) > 0:
            self.base.getCoinRefund(const.POINT_TYPE_REFUND_FREE, self.refundCoins.get(const.POINT_TYPE_REFUND_FREE, 0))

    def onGetEKeyMD5Signature(self, qrCodeUUID, signature):
        gameglobal.rds.ui.newRecharge.onGetEKeyMD5Signature(qrCodeUUID, signature)

    def onGetEKeyScanToPayUUID(self, qrCodeUUID):
        gameglobal.rds.ui.newRecharge.onJiangjunlingQRCode(qrCodeUUID)

    def onGetSHA1RSASignature(self, type, id, signed):
        gameglobal.rds.ui.newRecharge.onGetSHA1RSASignature(type, id, signed)

    def onGetQuickPaySignature(self, amount, fillTime, signature):
        useName = getattr(self, 'roleURS', 'unknown')
        if gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            gameglobal.rds.ui.newRecharge.onGetQuickPaySignature(useName, amount, fillTime, signature)
        else:
            remoteInterface.quickPayFillOrder(useName, amount, fillTime, signature, self.onQuickPayFillOrder)

    def onQuickPayFillOrder(self, rStatus, content):
        if not content:
            return
        if rStatus != 200:
            return
        fEvent = Event(events.EVENT_EASYPAY_FILL_ORDER_DONE, content)
        gameglobal.rds.ui.dispatchEvent(fEvent)

    def onExchangeTicketByCookie(self, ticket):
        import BigWorld
        import urllib
        p = BigWorld.player()
        if not p or not p.autoLoginUrl:
            return
        url = 'https://reg.163.com/services/ticketlogin?'
        m = {'product': 'ty',
         'ticket': ticket,
         'url': p.autoLoginUrl}
        params = urllib.urlencode(m)
        url += params
        BigWorld.openUrl(url)

    def sendChargeActivityData(self, data):
        caHistroy = {}
        if gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            caHistroy = gameglobal.rds.ui.newRecharge.caHistory
        else:
            caHistroy = gameglobal.rds.ui.easyPay.caHistory
        for item in data:
            caId, lastTime, leftTimes = item
            caHistroy[caId] = (lastTime, leftTimes)

    def sendChargeRewardData(self, data):
        self.chargeRewardInfo = data
        gameglobal.rds.ui.chargeReward.onSendRewardInfo()
        gamelog.info('jbx:sendChargeRewardData', data)
        gameglobal.rds.ui.activitySale.refreshInfo()
        gameglobal.rds.ui.activitySaleLoopCharge.refreshInfo()
        gameglobal.rds.ui.activitySaleLoopCharge.pushChargeRewardInfo()

    def onGetFirstChargeRewardStat(self, stat, firstEnterGameTime):
        gameglobal.rds.ui.activitySaleFirstPay.updateFrameInfo(stat, firstEnterGameTime)

    def getFirstChargeRewardSucc(self, newStat):
        self.queryRealNameChargeLimit()
        gameglobal.rds.ui.activitySaleFirstPay.updateStat(newStat)

    def onQueryChargeLvRewardData(self, stat, data):
        gameglobal.rds.ui.activitySaleLevelBonus.updatePlayerInfo(stat, data)

    def openRechargeFunc(self):
        if gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            gameglobal.rds.ui.newRecharge.show()
        else:
            gameglobal.rds.ui.easyPay.show()

    def onUpdateNewbieActivityInfo(self, newbieInfo):
        if gameglobal.rds.configData.get('enableNewbiePay', False):
            gameglobal.rds.ui.activitySaleNewbiePay.updateNewbieInfo(newbieInfo)

    def onSetChargeRaffleDial(self, aId, dial):
        gameglobal.rds.ui.raffle.choose(0, 0, dial)
        gameglobal.rds.ui.activitySaleLoopCharge.refreshInfo()
        gamelog.info('jbx:onSetChargeRaffleDial', dial)

    def queryRealNameChargeLimit(self):
        self.base.queryRealNameChargeLimit()

    def onQueryRealNameChargeLimit(self, state, age, monthLimit):
        self.realNameState = state
        self.curPlayerAge = age
        self.monthRechargeLimit = monthLimit
