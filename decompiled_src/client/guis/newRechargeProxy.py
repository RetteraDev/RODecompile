#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newRechargeProxy.o
from gamestrings import gameStrings
import time
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
import gametypes
import utils
import base64
import const
from guis import events
from guis.uiProxy import UIProxy
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from helpers import remoteInterface
from helpers.eventDispatcher import Event
import qrcode
from guis import ui
from guis import neteaseAppVipHelper
from ui import unicode2gbk
from ui import gbk2unicode
from data import coin_charge_activity_data as CCAD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from gamestrings import gameStrings
QUICK_CHECK_TIME = 12
LONG_CHECK_TIME = 300
QUICK_CHECK_INTERVAL = 3.1
LONG_CHECK_INTERVAL = 5
FILL_ORDER_TIMEOUT = 10
PAY_FAIL_WARN_LIMIT = 3
EASYPAY_EXCHANGE_ERR_STATE = -1
EASYPAY_SELECTED_NUM_STATE = 0
EASYPAY_FILL_ORDER_ING_STATE = 1
EASYPAY_FILL_ORDER_DONE_STATE = 2
EASYPAY_CHECK_ONE_STATE = 3
EASYPAY_CHECK_TWO_STATE = 4
EASYPAY_ERR_STATE = 5
EASYPAY_CHECK_SUCCESS_STATE = 6
ALIPAY_EXCHANGE_ERR_STATE = -1
ALIPAY_SELECTED_NUM_STATE = 0
ALIPAY_FILL_ORDER_ING_STATE = 1
ALIPAY_WAITING_QRCODE_STATE = 2
ALIPAY_QRCODE_DONE_STATE = 3
ALIPAY_CHECK_ONE_STATE = 4
ALIPAY_CHECK_TWO_STATE = 5
ALIPAY_ERR_STATE = 6
ALIPAY_CHECK_SUCCESS_STATE = 7
WECHAT_EXCHANGE_ERR_STATE = -1
WECHAT_SELECTED_NUM_STATE = 0
WECHAT_FILL_ORDER_ING_STATE = 1
WECHAT_WAITING_QRCODE_STATE = 2
WECHAT_QRCODE_DONE_STATE = 3
WECHAT_CHECK_ONE_STATE = 4
WECHAT_CHECK_TWO_STATE = 5
WECHAT_ERR_STATE = 6
WECHAT_CHECK_SUCCESS_STATE = 7
JIANGJUNLING_EXCHANGE_ERR_STATE = -1
JIANGJUNLING_SELECTED_NUM_STATE = 0
JIANGJUNLING_GET_QRCODE_UUID_STATE = 1
JIANGJUNLING_GENERATING_QRCODE_STATE = 2
JIANGJUNLING_GENERATED_QRCODE_STATE = 3
JIANGJUNLING_CHECK_ONE_STATE = 4
JIANGJUNLING_CHECK_TWO_STATE = 5
JIANGJUNLING_ERR_STATE = 6
JIANGJUNLING_CHECK_SUCCESS_STATE = 7
PAY_TYPE_EASYPAY = 1
PAY_TYPE_ALIPAY = 2
PAY_TYPE_WECHAT = 3
PAY_TYPE_JIANGJUNLING = 4
payTypeDict = {1: 'easyPay',
 2: 'aliPay',
 3: 'weChat',
 4: 'jiangjunling'}
FILL_ORDER_FAILED_DESC = {100: gameStrings.TEXT_EASYPAYPROXY_74,
 101: gameStrings.TEXT_EASYPAYPROXY_75,
 102: gameStrings.TEXT_EASYPAYPROXY_76,
 104: gameStrings.TEXT_EASYPAYPROXY_77,
 105: gameStrings.TEXT_EASYPAYPROXY_78,
 106: gameStrings.TEXT_EASYPAYPROXY_79,
 107: gameStrings.TEXT_EASYPAYPROXY_80,
 120: gameStrings.TEXT_EASYPAYPROXY_81,
 121: gameStrings.TEXT_EASYPAYPROXY_82,
 310: gameStrings.TEXT_EASYPAYPROXY_83,
 311: gameStrings.TEXT_EASYPAYPROXY_84,
 312: gameStrings.TEXT_EASYPAYPROXY_85,
 313: gameStrings.TEXT_EASYPAYPROXY_86,
 320: gameStrings.TEXT_EASYPAYPROXY_87}
QRCODE_RECHARGE_STR_CONST = {1: gameStrings.TEXT_NEWRECHARGEPROXY_118,
 2: gameStrings.TEXT_NEWRECHARGEPROXY_119,
 3: gameStrings.TEXT_NEWRECHARGEPROXY_120,
 4: gameStrings.TEXT_NEWRECHARGEPROXY_121,
 5: gameStrings.TEXT_NEWRECHARGEPROXY_122,
 6: gameStrings.TEXT_NEWRECHARGEPROXY_123,
 7: gameStrings.TEXT_NEWRECHARGEPROXY_124,
 8: gameStrings.TEXT_NEWRECHARGEPROXY_125,
 9: gameStrings.TEXT_NEWRECHARGEPROXY_126,
 10: gameStrings.TEXT_NEWRECHARGEPROXY_127,
 11: gameStrings.TEXT_NEWRECHARGEPROXY_128,
 12: gameStrings.TEXT_NEWRECHARGEPROXY_129,
 13: gameStrings.TEXT_BASE_ACCOUNT_4751,
 14: gameStrings.TEXT_NEWRECHARGEPROXY_131,
 15: gameStrings.TEXT_NEWRECHARGEPROXY_132,
 16: gameStrings.TEXT_NEWRECHARGEPROXY_133,
 17: gameStrings.TEXT_NEWRECHARGEPROXY_134,
 18: gameStrings.TEXT_NEWRECHARGEPROXY_135,
 19: gameStrings.TEXT_NEWRECHARGEPROXY_136,
 20: gameStrings.TEXT_NEWRECHARGEPROXY_137,
 21: gameStrings.TEXT_NEWRECHARGEPROXY_138,
 22: gameStrings.TEXT_EASYPAYPROXY_84,
 23: gameStrings.TEXT_NEWRECHARGEPROXY_140,
 24: gameStrings.TEXT_NEWRECHARGEPROXY_141,
 25: gameStrings.TEXT_NEWRECHARGEPROXY_142}
ECARD_PLATFORM = 'ty'
EL_VERSION = 1
ELS_EXCHANGE_POINTS1 = 1
ELS_ORDER_FILLED = 2
ELS_ORDER_PAYING = 3
ELS_QUERY_POINTS = 4
ELS_EXCHANGE_POINTS2 = 5
ELM_WEB_CHARGE = 1
ELM_NEW_QUICKPAY = 2
ELM_BALANCE_CHARGE = 3
ELM_QUICKPAY_CHARGE = 4
ELM_ALIPAY_CHARGE = 5
ELM_WECHAT_QRCODE_CHARGE = 6
ELM_JIANGJUNLING_QRCODE_CHARGE = 7
ELR_CLOSE = 1
ELR_RESET = 2
ELR_SUCCESS = 3
ELR_TIMEOUT = 4
ER_SUCCESS = 1
ER_FAILED = 2
PAY_LOG_STATE_DICT = {EASYPAY_SELECTED_NUM_STATE: 0,
 EASYPAY_FILL_ORDER_ING_STATE: ELS_EXCHANGE_POINTS1,
 EASYPAY_FILL_ORDER_DONE_STATE: ELS_ORDER_PAYING,
 EASYPAY_CHECK_ONE_STATE: ELS_QUERY_POINTS,
 EASYPAY_CHECK_TWO_STATE: ELS_QUERY_POINTS,
 EASYPAY_ERR_STATE: 0,
 EASYPAY_CHECK_SUCCESS_STATE: ELS_EXCHANGE_POINTS2,
 ALIPAY_SELECTED_NUM_STATE: 0,
 ALIPAY_FILL_ORDER_ING_STATE: ELS_EXCHANGE_POINTS1,
 ALIPAY_WAITING_QRCODE_STATE: ELS_ORDER_FILLED,
 ALIPAY_QRCODE_DONE_STATE: ELS_ORDER_PAYING,
 ALIPAY_CHECK_ONE_STATE: ELS_QUERY_POINTS,
 ALIPAY_CHECK_TWO_STATE: ELS_QUERY_POINTS,
 ALIPAY_ERR_STATE: 0,
 ALIPAY_CHECK_SUCCESS_STATE: ELS_EXCHANGE_POINTS2,
 WECHAT_SELECTED_NUM_STATE: 0,
 WECHAT_FILL_ORDER_ING_STATE: ELS_EXCHANGE_POINTS1,
 WECHAT_WAITING_QRCODE_STATE: ELS_ORDER_FILLED,
 WECHAT_QRCODE_DONE_STATE: ELS_ORDER_PAYING,
 WECHAT_CHECK_ONE_STATE: ELS_QUERY_POINTS,
 WECHAT_CHECK_TWO_STATE: ELS_QUERY_POINTS,
 WECHAT_ERR_STATE: 0,
 WECHAT_CHECK_SUCCESS_STATE: ELS_EXCHANGE_POINTS2,
 JIANGJUNLING_SELECTED_NUM_STATE: 0,
 JIANGJUNLING_GET_QRCODE_UUID_STATE: ELS_EXCHANGE_POINTS1,
 JIANGJUNLING_GENERATING_QRCODE_STATE: ELS_ORDER_FILLED,
 JIANGJUNLING_GENERATED_QRCODE_STATE: ELS_ORDER_PAYING,
 JIANGJUNLING_CHECK_ONE_STATE: ELS_QUERY_POINTS,
 JIANGJUNLING_CHECK_TWO_STATE: ELS_QUERY_POINTS,
 JIANGJUNLING_ERR_STATE: 0,
 JIANGJUNLING_CHECK_SUCCESS_STATE: ELS_EXCHANGE_POINTS2}
GET_SIGNATURE_TYPE_ALI_QRCODE = 1
GET_SIGNATURE_TYPE_WECHAT_QRCODE = 2
GET_SIGNATURE_TYPE_ALI_CHECK_BILL = 3
GET_SIGNATURE_TYPE_WECHAT_CHECK_BILL = 4
CHECK_PAY_OFF = 3
EXCHANGE_TIMEOUT = 10

class NewRechargeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewRechargeProxy, self).__init__(uiAdapter)
        self.modelMap = {'getCurPayType': self.onGetCurPayType,
         'setCurPayType': self.onSetCurPayType,
         'getMyPointsInfo': self.onGetMyPointsInfo,
         'getUsePointHint': self.onGetUsePointHint,
         'confirmOrder': self.onConfirmOrder,
         'openQuickPay': self.onOpenQuickPay,
         'returnQuickPay': self.onReturnQuickPay,
         'getMoneyNum': self.onGetMoneyNum,
         'openCardCharge': self.onOpenCardCharge,
         'openWebCharge': self.onOpenWebCharge,
         'gotoHelpWeb': self.onGotoHelpWeb,
         'gotoPayQueryWeb': self.onGotoPayQueryWeb,
         'sendAuthCode': self.onSendAuthCode,
         'checkAuthCodeQuickPay': self.onCheckAuthCodeQuickPay,
         'openAlipayRecharge': self.onOpenAlipayRecharge,
         'completeCharge': self.onCompleteCharge,
         'refreshQrcode': self.refreshQrcode,
         'initSelectedBtn': self.onInitSelectedBtn,
         'getInitConstStr': self.onGetInitConstStr,
         'getChargeActivityInfo': self.onGetChargeActivityInfo}
        self.waitingForFillOrder = False
        self.caHistory = {}
        self.easyPayLog = {}
        self.payFailedCount = 0
        self.reset()
        self.addEvent(events.EVENT_POINTS_EXCHANGE_DONE, self.onExchangeTianbiDone, isGlobal=True)
        self.addEvent(events.EVENT_POINTS_EXCHANGE_FAILED, self.onExchangeTianbiFailed, isGlobal=True)
        self.addEvent(events.EVENT_NEW_EASYPAY_FILL_ORDER_DONE, self.onEasyPayFillOrderDone, isGlobal=True)
        self.addEvent(events.EVENT_POINTS_CHANGE, self.onPointsChanged, isGlobal=True)
        uiAdapter.registerEscFunc(uiConst.WIDGET_NEW_RECHARGE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_NEW_RECHARGE:
            self.mediator = mediator

    def show(self, assignCoin = 0, isRebetChecked = False):
        if not isRebetChecked:
            if self.checkNeteaseRebetInfo():
                return
        self.reset()
        self.assignCoin = assignCoin
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NEW_RECHARGE, True)
        BigWorld.player().queryRealNameChargeLimit()

    def checkNeteaseRebetInfo(self):
        if not gameglobal.rds.configData.get('enableNeteaseGameMembershipRights', False):
            return False
        if neteaseAppVipHelper.getInstance().hasRebet():
            msg = gameStrings.APPVIP_REBET_CONFIRM_MSG
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.confrimRebet, yesBtnText=gameStrings.APPVIP_RECHARGET)
            return True
        return False

    def confrimRebet(self):
        p = BigWorld.player()
        p.base.applyMembershipInGame(gametypes.RIGHT_TYPE_RECV_RECHARGE_GIFT)
        self.show(isRebetChecked=True)

    def clearWidget(self):
        self.saveEasyPayLog()
        self.reset()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NEW_RECHARGE)

    def reset(self):
        self.assignCoin = 0
        self.curPayType = 'aliPay'
        self.waitingPayType = ''
        self.easyPayLog = {}
        self.aliPayInfo = {'payPhase': 0}
        self.weChatInfo = {'payPhase': 0}
        self.jiangjunlingInfo = {'payPhase': 0}
        self.easyPayInfo = {'payPhase': 0}
        if self.waitingPayType:
            _payInfo = self.getWaitingPayInfo()
            if _payInfo.get('waitingHandler', None):
                BigWorld.cancelCallback(_payInfo['waitingHandler'])
            if _payInfo.get('checkHandler', None):
                BigWorld.cancelCallback(_payInfo['checkHandler'])
            if _payInfo.get('checkBillHandler', None):
                BigWorld.cancelCallback(_payInfo['checkBillHandler'])
            self.waitingPayType = ''

    def onInitSelectedBtn(self, *args):
        return GfxValue(gbk2unicode('aliPay'))

    def onGetInitConstStr(self, *args):
        ret = QRCODE_RECHARGE_STR_CONST
        return uiUtils.dict2GfxDict(ret, True)

    def onOpenCardCharge(self, *arg):
        gameglobal.rds.ui.recharge.show()

    def onOpenWebCharge(self, *arg):
        p = BigWorld.player()
        url = 'http://ecard.163.com/script/index'
        if p:
            p.autoLoginUrl = url
            p.base.exchangeTicketByCookie()
        else:
            BigWorld.openUrl(url)

    def onGetCurPayType(self, *args):
        return GfxValue(gbk2unicode(self.curPayType))

    def onSetCurPayType(self, *args):
        payType = unicode2gbk(args[3][0].GetString())
        self.switchPayType(payType)

    def switchPayType(self, payType):
        self.curPayType = payType
        self.clearWaitingState()
        self.aliPayInfo = {'payPhase': 0}
        self.weChatInfo = {'payPhase': 0}
        self.jiangjunlingInfo = {'payPhase': 0}
        self.easyPayInfo = {'payPhase': 0}
        if self.assignCoin:
            self._confirmOrder(self.assignCoin, False, 0)
            self.assignCoin = 0
        else:
            self.refreshCurTypeInfo()

    def clearWaitingState(self):
        if self.waitingPayType:
            _payInfo = self.getWaitingPayInfo()
            if _payInfo.get('waitingHandler', None):
                BigWorld.cancelCallback(_payInfo['waitingHandler'])
            if _payInfo.get('checkHandler', None):
                BigWorld.cancelCallback(_payInfo['checkHandler'])
            if _payInfo.get('checkBillHandler', None):
                BigWorld.cancelCallback(_payInfo['checkBillHandler'])
            self.waitingPayType = ''

    def refreshCurTypeInfo(self):
        ret = {}
        ret['curPayType'] = self.curPayType
        ret['aliPayInfo'] = self.aliPayInfo
        ret['weChatInfo'] = self.weChatInfo
        ret['jiangjunlingInfo'] = self.jiangjunlingInfo
        ret['easyPayInfo'] = self.easyPayInfo
        if self.mediator:
            self.mediator.Invoke('refreshCurTypeInfo', uiUtils.dict2GfxDict(ret, True))

    def onGetMyPointsInfo(self, *args):
        return gameglobal.rds.ui.tianyuMall.onGetMyPointsInfo()

    def onGetUsePointHint(self, *args):
        enabled = args[3][0].GetBool()
        if enabled:
            hint = uiUtils.getTextFromGMD(GMDD.data.EASY_PAY_USE_POINT_HINT, gameStrings.TEXT_EASYPAYPROXY_812)
        else:
            hint = uiUtils.getTextFromGMD(GMDD.data.EASY_PAY_USE_POINT_GREY_HINT, gameStrings.TEXT_EASYPAYPROXY_815)
        return GfxValue(gbk2unicode(hint))

    def getCurPayInfo(self):
        if self.curPayType == 'easyPay':
            return self.easyPayInfo
        if self.curPayType == 'aliPay':
            return self.aliPayInfo
        if self.curPayType == 'weChat':
            return self.weChatInfo
        if self.curPayType == 'jiangjunling':
            return self.jiangjunlingInfo
        return {}

    def getWaitingPayInfo(self):
        if self.waitingPayType == 'easyPay':
            return self.easyPayInfo
        if self.waitingPayType == 'aliPay':
            return self.aliPayInfo
        if self.waitingPayType == 'weChat':
            return self.weChatInfo
        if self.waitingPayType == 'jiangjunling':
            return self.jiangjunlingInfo
        return {}

    @ui.callFilter(3)
    def onConfirmOrder(self, *args):
        buyCoinAll = int(args[3][0].GetNumber())
        usePoint = args[3][1].GetBool()
        caId = int(args[3][2].GetNumber())
        self._confirmOrder(buyCoinAll, usePoint, caId)

    @ui.callFilter(3)
    def refreshQrcode(self, *args):
        _payInfo = self.getWaitingPayInfo()
        buyCoinAll = _payInfo['buyCoinAll']
        usePoint = _payInfo['usePoint']
        caId = _payInfo['caId']
        _payInfo['qrcode_gen'] = False
        self._confirmOrder(buyCoinAll, usePoint, caId)

    def _confirmOrder(self, buyCoinAll, usePoint, caId):
        if not self.checkConfirmOrder(buyCoinAll, usePoint, caId):
            return
        p = BigWorld.player()
        if not buyCoinAll > 0:
            p.showGameMsg(GMDD.data.PAY_NUM_CAN_NOT_BE_ZERO, ())
            return
        myPoints = p.standbyPoints + p.commonPoints + p.specialPoints
        _payInfo = self.getCurPayInfo()
        _payInfo['buyCoinAll'] = buyCoinAll
        _payInfo['usePoint'] = usePoint
        _payInfo['caId'] = caId
        tmpT = time.localtime(utils.getNow())
        _payInfo['confirmOrderBeginTime'] = ''.join(('%04d' % tmpT.tm_year,
         '%02d' % tmpT.tm_mon,
         '%02d' % tmpT.tm_mday,
         '%02d' % tmpT.tm_hour,
         '%02d' % tmpT.tm_min,
         '%02d' % tmpT.tm_sec))
        if self.curPayType == 'easyPay':
            _payInfo['payPhase'] = EASYPAY_FILL_ORDER_ING_STATE
            self.waitingPayType = 'easyPay'
        elif self.curPayType == 'aliPay':
            _payInfo['payPhase'] = ALIPAY_FILL_ORDER_ING_STATE
            self.waitingPayType = 'aliPay'
        elif self.curPayType == 'weChat':
            _payInfo['payPhase'] = WECHAT_FILL_ORDER_ING_STATE
            self.waitingPayType = 'weChat'
        elif self.curPayType == 'jiangjunling':
            _payInfo['payPhase'] = JIANGJUNLING_GET_QRCODE_UUID_STATE
            if _payInfo['buyCoinAll'] % 50 != 0:
                p.showGameMsg(GMDD.data.JAINGJUNLING_PAY_FIFTY_MULTIPLE, ())
                return
            self.waitingPayType = 'jiangjunling'
        self.refreshCurTypeInfo()
        if _payInfo['usePoint'] and myPoints > 0:
            exchangePoints = min(myPoints, _payInfo['buyCoinAll'])
            _payInfo['exchangePoints'] = exchangePoints
            self.doExchangePoints(exchangePoints)
        else:
            _payInfo['chargeCoin'] = _payInfo['buyCoinAll']
            _payInfo['chargePoints'] = self.getFixedChargeNum(_payInfo['chargeCoin'])
            if self.waitingPayType == 'jiangjunling':
                _payInfo['buy_amount'] = _payInfo['chargeCoin']
                _payInfo['total_price'] = self.getMoneyNum(_payInfo['buyCoinAll'], _payInfo['usePoint'])
                p.base.getEKeyScanToPayUUID()
            elif self.waitingPayType == 'weChat':
                _payInfo['buy_amount'] = _payInfo['chargeCoin']
                _payInfo['total_price'] = self.getMoneyNum(_payInfo['buyCoinAll'], _payInfo['usePoint'])
                _payInfo['payPhase'] = WECHAT_WAITING_QRCODE_STATE
                _payInfo['qrcode_path'] = ''
                content = ''.join((ECARD_PLATFORM,
                 p.roleURS,
                 '1',
                 str(_payInfo['buy_amount'])))
                p.base.getSHA1RSASignature(PAY_TYPE_WECHAT, GET_SIGNATURE_TYPE_WECHAT_QRCODE, content)
                self.refreshCurTypeInfo()
            else:
                self.easyPayFillOrder(_payInfo['chargePoints'])

    def checkConfirmOrder(self, buyCoinAll, usePoint, caId):
        if not gameglobal.rds.configData.get('enableRealNameChargeLimit', False):
            return True
        p = BigWorld.player()
        if p.realNameState == const.REALNAME_STATE_INVALID:
            p.showGameMsg(GMDD.data.CHARGE_REAL_NAME_INVALID, ())
            return False
        if p.realNameState == const.REALNAME_STATE_NOT_CONFIRM:
            p.showGameMsg(GMDD.data.CHARGE_REAL_NAME_NOT_PASS, ())
            return False
        if p.realNameState == const.REALNAME_STATE_TEEN:
            age = p.curPlayerAge
            monthRechargeLimit = p.monthRechargeLimit
            for k, val in SCD.data.get('PUPIL_CHARGE_LIMIT', {}).iteritems():
                if age >= k:
                    continue
                countLimit, monthLimit, msgId = val
                if buyCoinAll > countLimit:
                    msgId and p.showGameMsg(msgId, (countLimit, monthLimit))
                    return False
                if buyCoinAll > monthRechargeLimit:
                    msgId and p.showGameMsg(msgId, (countLimit, monthLimit))
                    return False

        return True

    def getFixedChargeNum(self, origNum):
        return origNum

    def easyPayFillOrder(self, buyCount):
        _payInfo = self.getWaitingPayInfo()
        _payInfo['waitingForFillOrder'] = True
        if _payInfo.get('waitingHandler', None):
            BigWorld.cancelCallback(_payInfo['waitingHandler'])
        _payInfo['waitingHandler'] = BigWorld.callback(FILL_ORDER_TIMEOUT, self.onFillOrderTimeOut)
        BigWorld.player().base.getQuickPaySignature(buyCount)

    def onFillOrderTimeOut(self):
        _payInfo = {}
        _payInfo = self.getWaitingPayInfo()
        if not _payInfo.get('waitingForFillOrder', False):
            return
        self.payFailedCount += 1
        if self.payFailedCount >= PAY_FAIL_WARN_LIMIT:
            self.payFailedCount = 0
            msg = gameStrings.TEXT_EASYPAYPROXY_805 % (PAY_FAIL_WARN_LIMIT, FILL_ORDER_TIMEOUT)
            BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})

    def onEasyPayFillOrderDone(self, event):
        if gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            if self.mediator:
                p = BigWorld.player()
                _payInfo = {}
                _payInfo = self.getWaitingPayInfo()
                _payInfo.update(event.data)
                _payInfo['waitingForFillOrder'] = False
                self.payFailedCount = 0
                if _payInfo.get('waitingHandler', None):
                    BigWorld.cancelCallback(_payInfo['waitingHandler'])
                    _payInfo['waitingHandler'] = None
                else:
                    return
                status = _payInfo.get('status', -1)
                if status not in (200, 313):
                    self.dealErrState(status)
                elif self.waitingPayType == 'easyPay':
                    if _payInfo.get('interfaceType', 0) in (3, 4, 5):
                        _payInfo['payPhase'] = EASYPAY_FILL_ORDER_DONE_STATE
                        self.calcQuickPayListFormat()
                        self.refreshCurTypeInfo()
                    else:
                        _payInfo['payPhase'] = EASYPAY_ERR_STATE
                        self.refreshCurTypeInfo()
                elif self.waitingPayType == 'aliPay':
                    _payInfo['payPhase'] = ALIPAY_WAITING_QRCODE_STATE
                    _payInfo['qrcode_path'] = ''
                    content = ''.join((ECARD_PLATFORM,
                     _payInfo['user_name'],
                     '1',
                     str(_payInfo['buy_amount'])))
                    p.base.getSHA1RSASignature(PAY_TYPE_ALIPAY, GET_SIGNATURE_TYPE_ALI_QRCODE, content)
                    self.refreshCurTypeInfo()
                elif self.waitingPayType == 'weChat':
                    _payInfo['payPhase'] = WECHAT_WAITING_QRCODE_STATE
                    _payInfo['qrcode_path'] = ''
                    content = ''.join((ECARD_PLATFORM,
                     _payInfo['user_name'],
                     '1',
                     str(_payInfo['buy_amount'])))
                    p.base.getSHA1RSASignature(PAY_TYPE_WECHAT, GET_SIGNATURE_TYPE_WECHAT_QRCODE, content)
                    self.refreshCurTypeInfo()
                elif self.waitingPayType == 'jiangjunling':
                    pass

    def onGetSHA1RSASignature(self, _type, _id, signed):
        if self.mediator:
            _payInfo = {}
            _payInfo = self.getWaitingPayInfo()
            p = BigWorld.player()
            if payTypeDict[_type] == 'aliPay' and self.waitingPayType == 'aliPay':
                if _id == GET_SIGNATURE_TYPE_ALI_QRCODE:
                    if _payInfo.get('buy_amount', None):
                        remoteInterface.getAliPayQrcodeData(p.roleURS, _payInfo['buy_amount'], signed, self.onGetAliPayQrcodeData)
                elif _id == GET_SIGNATURE_TYPE_ALI_CHECK_BILL:
                    if _payInfo.get('confirmOrderBeginTime', None) and _payInfo.get('confirmOrderEndTime', None):
                        remoteInterface.queryAliPayBill(p.roleURS, _payInfo['confirmOrderBeginTime'], _payInfo['confirmOrderEndTime'], signed, self.onQueryAliPayBill)
            elif payTypeDict[_type] == 'weChat' and self.waitingPayType == 'weChat':
                if _id == GET_SIGNATURE_TYPE_WECHAT_QRCODE:
                    if _payInfo.get('buy_amount', None):
                        remoteInterface.getWeChatPayQrcode(p.roleURS, _payInfo['buy_amount'], signed, self.onGetWeChatPayQrcode)
                elif _id == GET_SIGNATURE_TYPE_WECHAT_CHECK_BILL:
                    _payInfo['checkSign'] = signed
                    self.checkQrcodeBillState()

    def calcQuickPayListFormat(self):
        self.easyPayInfo['quickPayListFormat'] = []
        quickPayList = self.easyPayInfo.get('quickPayList', [])
        for qp in quickPayList:
            attr = qp.split(',')
            for i in range(len(attr)):
                if i == 1:
                    a = attr[i].decode('unicode_escape')
                    attr[i] = a.encode('gbk')

            self.easyPayInfo['quickPayListFormat'].append(attr)

    def doExchangePoints(self, pointsToBuy):
        p = BigWorld.player()
        now = p.getServerTime()
        _payInfo = {}
        _payInfo = self.getWaitingPayInfo()
        if _payInfo.get('exchanging', False):
            if now - _payInfo.get('exchangStartTime', 0) < EXCHANGE_TIMEOUT:
                p.showGameMsg(GMDD.data.EXCHANGE_PENDING, ())
                return
        _payInfo['exchanging'] = True
        _payInfo['exchangStartTime'] = now
        _payInfo['exchangePending'] = 0
        commonPoints = p.commonPoints + p.specialPoints
        caId = _payInfo.get('caId', 0)
        if commonPoints > 0:
            if pointsToBuy > commonPoints:
                _payInfo['exchangePending'] = pointsToBuy - commonPoints
                pointsToBuy = commonPoints
            else:
                _payInfo['exchangePending'] = 0
            p.base.buyCoinUseCommonPoint(pointsToBuy, caId)
        else:
            _payInfo['exchangePending'] = 0
            p.base.buyCoinUseStandbyPoint(pointsToBuy, caId)

    def onExchangeTianbiDone(self):
        if gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            if self.mediator:
                _payInfo = {}
                _payInfo = self.getWaitingPayInfo()
                gamelog.debug('@zq onExchangeTianbiDone', _payInfo.get('exchangePending', 0))
                if _payInfo.get('exchangePending', 0) > 0:
                    caId = _payInfo.get('caId', 0)
                    BigWorld.player().base.buyCoinUseStandbyPoint(_payInfo.get('exchangePending', 0), caId)
                    _payInfo['exchangePending'] = 0
                else:
                    _payInfo['exchanging'] = False
                    self.onExchangePointsComplete()

    def onExchangePointsComplete(self):
        _payInfo = {}
        _payInfo = self.getWaitingPayInfo()
        chargeCoin = _payInfo.get('buyCoinAll', 0) - _payInfo.get('exchangePoints', 0)
        p = BigWorld.player()
        if _payInfo.get('chargeDone', False):
            chargeCoin -= _payInfo.get('chargeCoin', 0)
        gamelog.debug('@zq onExchangePointsComplete', chargeCoin)
        if chargeCoin > 0:
            _payInfo['chargeCoin'] = chargeCoin
            _payInfo['chargePoints'] = self.getFixedChargeNum(chargeCoin)
            if self.waitingPayType == 'weChat':
                _payInfo['buy_amount'] = _payInfo['chargeCoin']
                _payInfo['payPhase'] = WECHAT_WAITING_QRCODE_STATE
                _payInfo['qrcode_path'] = ''
                content = ''.join((ECARD_PLATFORM,
                 p.roleURS,
                 '1',
                 str(_payInfo['buy_amount'])))
                p.base.getSHA1RSASignature(PAY_TYPE_WECHAT, GET_SIGNATURE_TYPE_WECHAT_QRCODE, content)
                self.refreshCurTypeInfo()
            else:
                self.easyPayFillOrder(_payInfo['chargePoints'])
        else:
            self.easyPayLog['result'] = ER_SUCCESS
            self.saveEasyPayLog()
            _payInfo['payPhase'] = self.getWaitingSuccessType()
            self.refreshCurTypeInfo()
            self.clearWaitingState()

    def getWaitingSuccessType(self):
        if self.waitingPayType == 'easyPay':
            return EASYPAY_CHECK_SUCCESS_STATE
        if self.waitingPayType == 'aliPay':
            return ALIPAY_CHECK_SUCCESS_STATE
        if self.waitingPayType == 'weChat':
            return WECHAT_CHECK_SUCCESS_STATE
        if self.waitingPayType == 'jiangjunling':
            return JIANGJUNLING_CHECK_SUCCESS_STATE

    def getExchangeErrType(self):
        if self.waitingPayType == 'easyPay':
            return EASYPAY_EXCHANGE_ERR_STATE
        if self.waitingPayType == 'aliPay':
            return ALIPAY_EXCHANGE_ERR_STATE
        if self.waitingPayType == 'weChat':
            return WECHAT_EXCHANGE_ERR_STATE
        if self.waitingPayType == 'jiangjunling':
            return JIANGJUNLING_EXCHANGE_ERR_STATE

    def onExchangeTianbiFailed(self):
        if gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            if self.mediator:
                gamelog.debug('@zq onExchangeTianbiFailed')
                _payInfo = {}
                _payInfo = self.getWaitingPayInfo()
                _payInfo['exchanging'] = False
                _payInfo['exchangStartTime'] = 0
                _payInfo['exchangePending'] = 0
                _payInfo['payPhase'] = self.getExchangeErrType()
                self.refreshCurTypeInfo()

    def onOpenQuickPay(self, *arg):
        remoteInterface.redirectWangYiBaoToRegisterqp(self.easyPayInfo['sid'], self.easyPayInfo['orderId'])
        self.webChargeConfirmMsgBox()

    def webChargeConfirmMsgBox(self):
        msg = gameStrings.TEXT_EASYPAYPROXY_726
        yesText = gameStrings.TEXT_EASYPAYPROXY_727
        noText = gameStrings.TEXT_EASYPAYPROXY_728
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onChargeDone), yesText, None, noText)

    def onChargeDone(self):
        _payInfo = {}
        _payInfo = self.getWaitingPayInfo()
        if _payInfo.get('checkBillHandler', None):
            BigWorld.cancelCallback(_payInfo['checkBillHandler'])
        _payInfo['chargeDone'] = True
        _payInfo['startQueryTime'] = utils.getNow()
        _payInfo['payPhase'] = self.getWaitingPayCheck1()
        self.refreshCurTypeInfo()
        self.onRechargePointsCheck1()

    def getWaitingPayCheck1(self):
        if self.waitingPayType == 'easyPay':
            return EASYPAY_CHECK_ONE_STATE
        if self.waitingPayType == 'aliPay':
            return ALIPAY_CHECK_ONE_STATE
        if self.waitingPayType == 'weChat':
            return WECHAT_CHECK_ONE_STATE
        if self.waitingPayType == 'jiangjunling':
            return JIANGJUNLING_CHECK_ONE_STATE

    def onRechargePointsCheck1(self):
        _payInfo = {}
        _payInfo = self.getWaitingPayInfo()
        checkState = self.getWaitingPayCheck1()
        if _payInfo.get('payPhase', -1) != checkState or _payInfo.get('pointChange', False):
            if _payInfo.get('checkHandler', None):
                BigWorld.cancelCallback(_payInfo['checkHandler'])
            return
        else:
            now = utils.getNow()
            if now - _payInfo['startQueryTime'] < QUICK_CHECK_TIME:
                BigWorld.player().base.queryDianKa()
                _payInfo['checkHandler'] = BigWorld.callback(QUICK_CHECK_INTERVAL, self.onRechargePointsCheck1)
            else:
                if _payInfo.get('checkHandler', None):
                    BigWorld.cancelCallback(_payInfo['checkHandler'])
                _payInfo['LONG_CHECK_TIME'] = LONG_CHECK_TIME
                self.refreshCurTypeInfo()
                _payInfo['startQueryTime'] = now
                _payInfo['payPhase'] = self.getWaitingPayCheck2()
                self.refreshCurTypeInfo()
                self.onRechargePointsCheck2()
            return

    def getWaitingPayCheck2(self):
        if self.waitingPayType == 'easyPay':
            return EASYPAY_CHECK_TWO_STATE
        if self.waitingPayType == 'aliPay':
            return ALIPAY_CHECK_TWO_STATE
        if self.waitingPayType == 'weChat':
            return WECHAT_CHECK_TWO_STATE
        if self.waitingPayType == 'jiangjunling':
            return JIANGJUNLING_CHECK_TWO_STATE

    def onRechargePointsCheck2(self):
        _payInfo = {}
        _payInfo = self.getWaitingPayInfo()
        checkState = self.getWaitingPayCheck2()
        if _payInfo.get('payPhase', -1) != checkState or _payInfo.get('pointChange', False):
            if _payInfo.get('checkHandler', None):
                BigWorld.cancelCallback(_payInfo['checkHandler'])
            return
        else:
            now = utils.getNow()
            if now - _payInfo['startQueryTime'] < LONG_CHECK_TIME:
                BigWorld.player().base.queryDianKa()
                _payInfo['checkHandler'] = BigWorld.callback(LONG_CHECK_INTERVAL, self.onRechargePointsCheck2)
            else:
                if _payInfo.get('checkHandler', None):
                    BigWorld.cancelCallback(_payInfo['checkHandler'])
                _payInfo['startQueryTime'] = 0
                if self.waitingPayType == 'easyPay':
                    _payInfo['payPhase'] = EASYPAY_ERR_STATE
                elif self.waitingPayType == 'aliPay':
                    _payInfo['payPhase'] = ALIPAY_ERR_STATE
                elif self.waitingPayType == 'weChat':
                    _payInfo['payPhase'] = WECHAT_ERR_STATE
                elif self.waitingPayType == 'jiangjunling':
                    _payInfo['payPhase'] = JIANGJUNLING_ERR_STATE
                self.refreshCurTypeInfo()
                self.easyPayLog['stage'] = ELS_QUERY_POINTS
                self.saveEasyPayLog()
            return

    def onReturnQuickPay(self, *args):
        recordLog = args[3][0].GetBool()
        if recordLog:
            self.saveEasyPayLog()
        self.switchPayType(self.curPayType)

    def onGetMoneyNum(self, *args):
        buyCoinAll = int(args[3][0].GetNumber())
        usePoint = args[3][1].GetBool()
        priceNum = self.getMoneyNum(buyCoinAll, usePoint)
        return GfxValue(priceNum)

    def getMoneyNum(self, buyCoinAll, usePoint):
        p = BigWorld.player()
        exchangePoints = 0
        if usePoint:
            myPoints = p.standbyPoints + p.commonPoints + p.specialPoints
            exchangePoints = min(myPoints, buyCoinAll)
        priceNum = (buyCoinAll - exchangePoints) / 10.0
        return priceNum

    def onSendAuthCode(self, *args):
        interfaceType = int(args[3][0].GetNumber())
        quickPayId = args[3][1].GetString()
        self.easyPayInfo['userPayType'] = interfaceType
        remoteInterface.quickPaySendAuthCode(self.easyPayInfo['sid'], self.easyPayInfo['bill_id'], interfaceType, quickPayId, self.onSendAuthCodeDone)

    def onSendAuthCodeDone(self, rStatus, content):
        if self.mediator:
            if not content:
                return
            if rStatus != 200:
                return
            self.easyPayInfo.update(content)
            status = content.get('status', -1)
            if status == 200:
                tips = ''
            else:
                self.dealErrState(status)

    def onPointsChanged(self):
        if self.mediator:
            _payInfo = {}
            _payInfo = self.getWaitingPayInfo()
            p = BigWorld.player()
            myPoints = p.standbyPoints + p.commonPoints + p.specialPoints
            if myPoints < _payInfo.get('chargeCoin', myPoints + 1):
                return
            if self.waitingPayType:
                _payInfo['chargeDone'] = True
                _payInfo['pointChange'] = True
                self.doExchangePoints(_payInfo['chargeCoin'])

    @ui.callFilter(3)
    def onCheckAuthCodeQuickPay(self, *arg):
        authCode = arg[3][0].GetString()
        quickPayId = arg[3][1].GetString()
        bankCode = arg[3][2].GetString()
        remoteInterface.quickPayCompleteQuickPay(self.easyPayInfo['sid'], self.easyPayInfo['bill_id'], authCode, quickPayId, bankCode, self.easyPayInfo.get('chargeId', ''), self.easyPayInfo.get('oriMerchSeq', ''), self.onCheckAuthCodeDone)

    def onCheckAuthCodeDone(self, rStatus, content):
        if self.mediator:
            if not content:
                return
            if rStatus != 200:
                return
            self.easyPayInfo.update(content)
            if not self.mediator:
                return
            status = content.get('status', -1)
            if status != 200:
                self.dealErrState(status)
            else:
                self.onChargeDone()

    def onGotoHelpWeb(self, *arg):
        BigWorld.openUrl('http://pay.163.com/jsp/cardintro.jsp')

    def onGotoPayQueryWeb(self, *arg):
        p = BigWorld.player()
        url = 'https://epay.163.com/servlet/controller?operation=queryTradeView'
        if p:
            p.autoLoginUrl = url
            p.base.exchangeTicketByCookie()
        else:
            BigWorld.openUrl(url)

    def getErrType(self):
        if self.waitingPayType == 'easyPay':
            return EASYPAY_ERR_STATE
        if self.waitingPayType == 'aliPay':
            return ALIPAY_ERR_STATE
        if self.waitingPayType == 'weChat':
            return WECHAT_ERR_STATE
        if self.waitingPayType == 'jiangjunling':
            return JIANGJUNLING_ERR_STATE

    def dealErrState(self, errCode):
        _payInfo = self.getWaitingPayInfo()
        errType = self.getErrType()
        if self.waitingPayType == 'easyPay':
            if _payInfo['payPhase'] == EASYPAY_FILL_ORDER_DONE_STATE:
                if errCode in (311, 312, 106):
                    if self.mediator:
                        content = uiUtils.toHtml(FILL_ORDER_FAILED_DESC[errCode], '#cc2929')
                        self.mediator.Invoke('setCheckCodeErr', GfxValue(gbk2unicode(content)))
                else:
                    _payInfo['payPhase'] = errType
                    self.refreshCurTypeInfo()
        else:
            _payInfo['payPhase'] = errType
            self.refreshCurTypeInfo()
        gamelog.debug('@zq errCode', errCode)

    def onNewQuickPayFillOrder(self, rStatus, content, payType):
        if self.mediator:
            if not content:
                return
            if rStatus != 200:
                return
            content['payType'] = payType
            fEvent = Event(events.EVENT_NEW_EASYPAY_FILL_ORDER_DONE, content)
            gameglobal.rds.ui.dispatchEvent(fEvent)
            return

    def onGetQuickPaySignature(self, useName, amount, fillTime, signature):
        if self.mediator:
            _payInfo = {}
            _payInfo = self.getWaitingPayInfo()
            _payInfo['signature'] = signature
            remoteInterface.newQuickPayFillOrder(useName, amount, fillTime, signature, self.onNewQuickPayFillOrder, self.waitingPayType)

    def onGetAliPayQrcodeData(self, rStatus, content):
        if self.mediator:
            if not content:
                return
            if rStatus != 200:
                return
            status = content.get('status', -1)
            if status != 200:
                self.dealErrState(status)
            else:
                userName = self.aliPayInfo.get('user_name', '')
                self.aliPayInfo.update(content)
                self.aliPayInfo['user_name'] = userName
                remoteInterface.getAliPayQrcode(self.aliPayInfo.get('qrcode_img_url', ''), self.onGetAliPayQrcode)

    def onGetAliPayQrcode(self, rStatus, content):
        if self.mediator:
            if not content:
                return
            if rStatus != 200:
                return
            self.aliPayInfo['payPhase'] = ALIPAY_QRCODE_DONE_STATE
            self.aliPayInfo['qrcode_path'] = base64.encodestring(content)
            self.aliPayInfo['qrcode_gen'] = True
            self.aliPayInfo['refreshQrcodeTime'] = 3600
            self.refreshCurTypeInfo()
            self.checkQrcodeBillState()

    def onQueryAliPayBill(self, rStatus, content):
        if self.mediator:
            if not content:
                return
            if rStatus != 200:
                return
            if self.aliPayInfo.get('checkBillHandler', None):
                BigWorld.cancelCallback(self.aliPayInfo['checkBillHandler'])
            data = content.get('data', [])
            for item in data:
                if item.get('bank_gate', '') == 'AlipayAll.AlipayScan':
                    self.onChargeDone()
                    return

            self.aliPayInfo['checkBillHandler'] = BigWorld.callback(CHECK_PAY_OFF, self.checkQrcodeBillState)

    def onQueryWechatBill(self, rStatus, content):
        if self.mediator:
            if not content:
                return
            if rStatus != 200:
                return
            if self.weChatInfo.get('checkBillHandler', None):
                BigWorld.cancelCallback(self.weChatInfo['checkBillHandler'])
            if content.get('bill_info', {}).get('status', 0) == 3:
                self.onChargeDone()
                return
            self.weChatInfo['checkBillHandler'] = BigWorld.callback(CHECK_PAY_OFF, self.checkQrcodeBillState)

    def onQueryJiangjunlingBill(self, rStatus, content):
        if self.mediator:
            if not content:
                return
            if rStatus != 200:
                return
            if self.jiangjunlingInfo.get('checkBillHandler', None):
                BigWorld.cancelCallback(self.jiangjunlingInfo['checkBillHandler'])
            if content.get('record', {}).get('status', 0) == 1:
                self.onChargeDone()
                return
            self.weChatInfo['checkBillHandler'] = BigWorld.callback(CHECK_PAY_OFF, self.checkQrcodeBillState)

    def checkQrcodeBillState(self):
        _payInfo = self.getWaitingPayInfo()
        p = BigWorld.player()
        if self.waitingPayType == 'aliPay':
            tmpT = time.localtime(utils.getNow())
            endTime = ''.join(('%04d' % tmpT.tm_year,
             '%02d' % tmpT.tm_mon,
             '%02d' % tmpT.tm_mday,
             '%02d' % tmpT.tm_hour,
             '%02d' % tmpT.tm_min,
             '%02d' % tmpT.tm_sec))
            _payInfo['confirmOrderEndTime'] = endTime
            if _payInfo.get('confirmOrderBeginTime', None):
                content = ''.join((_payInfo['confirmOrderBeginTime'],
                 _payInfo['confirmOrderEndTime'],
                 p.roleURS,
                 ECARD_PLATFORM))
                p.base.getSHA1RSASignature(PAY_TYPE_ALIPAY, GET_SIGNATURE_TYPE_ALI_CHECK_BILL, content)
        elif self.waitingPayType == 'weChat':
            checkSign = _payInfo.get('checkSign', '')
            if checkSign:
                if _payInfo.get('bill_id', None):
                    remoteInterface.queryWeChatPay(p.roleURS, _payInfo['bill_id'], checkSign, self.onQueryWechatBill)
            elif _payInfo.get('bill_id', None):
                content = ''.join((ECARD_PLATFORM,
                 p.roleURS,
                 str(_payInfo['bill_id']),
                 'gbk'))
                p.base.getSHA1RSASignature(PAY_TYPE_WECHAT, GET_SIGNATURE_TYPE_WECHAT_CHECK_BILL, content)
        elif self.waitingPayType == 'jiangjunling':
            checkSign = _payInfo.get('checkSign', '')
            if checkSign:
                if _payInfo.get('qrcode_uuid', None):
                    remoteInterface.queryJiangjunlingPay(p.roleURS, _payInfo['qrcode_uuid'], checkSign, self.onQueryJiangjunlingBill)
            elif _payInfo.get('qrcode_uuid', None):
                p.base.getEKeyMD5Signature(_payInfo['qrcode_uuid'])

    def onGetWeChatPayQrcode(self, rStatus, content):
        if self.mediator:
            if not content:
                return
            if rStatus != 200:
                return
            status = content.get('status', -1)
            if status != 200:
                self.dealErrState(status)
            else:
                self.weChatInfo['payPhase'] = ALIPAY_QRCODE_DONE_STATE
                self.weChatInfo.update(content)
                self.weChatInfo['qrcode_path'] = self.weChatInfo.get('qrcode_data', '')
                self.weChatInfo['qrcode_gen'] = True
                self.weChatInfo['refreshQrcodeTime'] = 900
                self.refreshCurTypeInfo()
                self.checkQrcodeBillState()

    def onOpenAlipayRecharge(self, *arg):
        remoteInterface.redirectWangYiBaoToPay(self.aliPayInfo['sid'], self.aliPayInfo['bill_id'], True)
        self.webChargeConfirmMsgBox()

    def onJiangjunlingQRCode(self, codeUUID):
        if self.mediator:
            codeMaker = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=3, border=2)
            code = '{\"s\":\"game\",\"a\":\"ecardpay\",\"l\":{\"p\":\"ty\"},\"d\":{\"urs\":\"%s\",\"type\":1,\"amount\":%d,\"uuid\":\"%s\"},\"e\":%d}' % (gameglobal.rds.loginUserName,
             self.jiangjunlingInfo['buyCoinAll'],
             codeUUID,
             utils.getNow() + 600)
            codeMaker.add_data(code)
            codeMaker.make(fit=True)
            img = codeMaker.make_image()
            pngUrl = img.convert('RGB').tostring('jpeg', 'RGB', 90)
            if pngUrl:
                _buffer = base64.encodestring(pngUrl)
                self.jiangjunlingInfo['payPhase'] = JIANGJUNLING_GENERATED_QRCODE_STATE
                self.jiangjunlingInfo['qrcode_path'] = _buffer
                self.jiangjunlingInfo['qrcode_gen'] = True
                self.jiangjunlingInfo['refreshQrcodeTime'] = 600
                self.jiangjunlingInfo['qrcode_uuid'] = codeUUID
                self.refreshCurTypeInfo()
                self.checkQrcodeBillState()

    def onCompleteCharge(self, *args):
        self.onChargeDone()

    def chargeAcitivityConfig(self):
        return gameglobal.rds.configData.get('enableChargeActivity', False)

    def onGetChargeActivityInfo(self, *arg):
        ret = {}
        ret['switch'] = self.chargeAcitivityConfig()
        ccadd = CCAD.data
        caDict = {}
        for k, v in ccadd.iteritems():
            caInfo = {}
            caInfo.update(v)
            caInfo['caId'] = k
            caInfo['showIcon'] = True
            caInfo['canUse'] = self.checkChargeActivityUsable(k)
            frameList = caDict.setdefault(v.get('framId', 0), [])
            frameList.append(caInfo)

        for v in caDict.values():
            v.sort(self.acSortFunc)

        caList = []
        for k, v in caDict.iteritems():
            if not v:
                continue
            caList.append(v[0])

        caList = caList[:3]
        ret['caList'] = caList
        return uiUtils.dict2GfxDict(ret, True)

    def acSortFunc(self, item1, item2):
        if item1['canUse'] < item2['canUse']:
            return 1
        elif item1['canUse'] > item2['canUse']:
            return -1
        elif item1['caId'] < item2['caId']:
            return 1
        else:
            return -1

    def checkChargeActivityUsable(self, acId):
        if not self.chargeAcitivityConfig():
            return False
        acData = CCAD.data.get(acId, {})
        if acData.get('bonusCoin', 0) <= 0 and acData.get('mallCash', 0) <= 0 and acData.get('mailTemplateId', 0) <= 0:
            return False
        elif acData.get('hideInUI', 0) > 0:
            return False
        now = utils.getNow()
        beginTime = acData.get('beginTime', '')
        if beginTime and now < utils.getTimeSecondFromStr(beginTime):
            return False
        endTime = acData.get('endTime', '')
        if endTime and now > utils.getTimeSecondFromStr(endTime):
            return False
        whiteList = acData.get('whiteList', None)
        if whiteList and utils.getHostId() not in whiteList:
            return False
        elif self.caHistory.has_key(acId):
            return self.caHistory.get(acId, (0, 0))[1] > 0
        else:
            return int(acData.get('times', '0')) > 0

    def checkChargeActivityInfo(self):
        if not self.chargeAcitivityConfig():
            return False
        ccadd = CCAD.data
        for k, v in ccadd.iteritems():
            if self.checkChargeActivityUsable(k):
                return True

        return False

    def genChargeActivityEtcInfo(self):
        ret = {}
        ret['caId'] = 0
        ret['frameId'] = 0
        ret['chargeCoin'] = gameStrings.TEXT_EASYPAYPROXY_538
        ret['bonusDesc'] = ''
        ret['showIcon'] = False
        ret['canUse'] = True
        return ret

    def saveEasyPayLog(self):
        if not self.waitingPayType:
            return
        else:
            _payInfo = {}
            _payInfo = self.getWaitingPayInfo()
            if not _payInfo:
                return
            _stage = self.easyPayLog.get('stage', None)
            self.easyPayLog['stage'] = _stage if _stage else self.getPayTypeStage()
            self.easyPayLog['total_price'] = _payInfo.get('total_price', 0)
            self.easyPayLog['buy_amount'] = _payInfo.get('buy_amount', 0)
            self.easyPayLog['bill_id'] = _payInfo.get('bill_id', 0)
            self.easyPayLog['amount'] = _payInfo.get('amount', 0)
            self.easyPayLog['buy_coin1'] = _payInfo.get('exchangePoints', 0)
            self.easyPayLog['method'] = self.getPayTypeMethod()
            self.easyPayLog['version'] = EL_VERSION
            self.easyPayLog.setdefault('result', ER_FAILED)
            if gameglobal.rds.configData.get('enableEasyPayLog', False):
                LOG_FIELD = ['result',
                 'stage',
                 'total_price',
                 'buy_amount',
                 'bill_id',
                 'amount',
                 'buy_coin1',
                 'method']
                log_data = map(lambda k: str(self.easyPayLog.get(k, 0)), LOG_FIELD)
                BigWorld.player().base.recordClientLog(gametypes.CLIENT_RECORD_TYPE_EASYPAY, log_data)
                gamelog.debug('@zq saveEasyPayLog', log_data)
            self.easyPayLog = {}
            return

    def getPayTypeMethod(self):
        if self.waitingPayType == 'easyPay':
            return ELM_QUICKPAY_CHARGE
        if self.waitingPayType == 'aliPay':
            return ELM_ALIPAY_CHARGE
        if self.waitingPayType == 'weChat':
            return ELM_WECHAT_QRCODE_CHARGE
        if self.waitingPayType == 'jiangjunling':
            return ELM_JIANGJUNLING_QRCODE_CHARGE
        return 0

    def getPayTypeStage(self):
        if not self.waitingPayType:
            return 0
        _payInfo = {}
        _payInfo = self.getWaitingPayInfo()
        return PAY_LOG_STATE_DICT.get(_payInfo.get('payPhase', 0), 0)

    def onGetEKeyMD5Signature(self, qrCodeUUID, signature):
        if self.mediator:
            _payInfo = {}
            _payInfo = self.getWaitingPayInfo()
            if _payInfo.get('qrcode_uuid', '') == qrCodeUUID:
                _payInfo['checkSign'] = signature
                self.checkQrcodeBillState()
