#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/easyPayProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gamelog
import gametypes
import utils
import subprocess
from collections import deque
from guis import events
from guis import ui
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from helpers import remoteInterface
from Scaleform import GfxValue
from ui import gbk2unicode
from uiProxy import UIProxy
from appSetting import Obj as AppSettings
from data import sys_config_data as SCD
from data import coin_charge_activity_data as CCAD
from cdata import game_msg_def_data as GMDD
ES_ERROR = 0
ES_SUCCESS = 1
ES_FAILED = 2
ES_INIT = 3
ES_EASY_PAY_START = 4
ES_FILLING_ORDER = 5
ES_EXCHANGING = 6
ES_CHARGING = 7
ES_ORDER_READY = 8
ES_QUERY_POINT_1 = 9
ES_QUERY_POINT_2 = 10
ES_CHECK_AUTH_CODE = 11
CAN_CLOSE_WIDGET_STATE = [ES_ERROR,
 ES_SUCCESS,
 ES_FAILED,
 ES_INIT,
 ES_ORDER_READY]
EP_EVENT_START = 0
EP_EVENT_EXCHANGE_START = 1
EP_EVENT_EXCHANGE_COMPLETE = 2
EP_EVENT_EXCHANGE_FAILED = 3
EP_EVENT_RESET = 4
EP_EVENT_WAIT_TIMEOUT = 5
EP_EVENT_FILL_ORDER = 6
EP_EVENT_END = 7
EP_EVENT_ORDER_FILLED = 8
EP_EVENT_QUERY_POINT_1 = 9
EP_EVENT_CHARGE_POINT_ATTACH = 10
EP_EVENT_ORDER_FILL_ERR = 11
EP_EVENT_SEND_AUTH_CODE = 12
EP_EVENT_AUTH_CODE_RESULT = 13
ep_state_table_strict = {0: [0,
     0,
     0,
     0,
     3,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0],
 1: [0,
     0,
     0,
     0,
     3,
     0,
     0,
     1,
     0,
     0,
     0,
     0,
     0,
     0],
 2: [0,
     0,
     0,
     0,
     3,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0],
 3: [4,
     0,
     3,
     3,
     3,
     0,
     0,
     3,
     0,
     0,
     0,
     0,
     0,
     0],
 4: [4,
     6,
     4,
     4,
     3,
     0,
     5,
     1,
     0,
     0,
     0,
     0,
     0,
     0],
 5: [0,
     0,
     5,
     5,
     3,
     2,
     5,
     0,
     8,
     0,
     0,
     2,
     0,
     0],
 6: [0,
     6,
     4,
     2,
     0,
     2,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0],
 7: [0,
     0,
     7,
     7,
     0,
     2,
     0,
     0,
     0,
     0,
     0,
     0,
     0,
     0],
 8: [0,
     0,
     0,
     0,
     3,
     0,
     0,
     0,
     0,
     9,
     0,
     0,
     11,
     0],
 9: [0,
     0,
     0,
     0,
     3,
     10,
     0,
     0,
     0,
     0,
     6,
     0,
     0,
     0],
 10: [0,
      0,
      0,
      0,
      3,
      2,
      0,
      0,
      0,
      0,
      6,
      0,
      0,
      0],
 11: [0,
      0,
      0,
      0,
      0,
      8,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      8]}
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
SEND_AUTH_CODE_CD = 60
SEND_AUTH_CODE_CD_FADE = 10
QUICK_CHECK_TIME = 12
LONG_CHECK_TIME = 300
QUICK_CHECK_INTERVAL = 3.1
LONG_CHECK_INTERVAL = 5
FILL_ORDER_TIMEOUT = 10
PAY_FAIL_WARN_LIMIT = 3
WARN_COLOR = '#cc2929'
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
ELR_CLOSE = 1
ELR_RESET = 2
ELR_SUCCESS = 3
ELR_TIMEOUT = 4
ER_SUCCESS = 1
ER_FAILED = 2

class EasyPayStateManager(object):

    def __init__(self):
        self.reset()

    def setResultCallBack(self, succFunc, failFuc):
        self.successFunc = succFunc
        self.failedFunc = failFuc

    def reset(self):
        self.state = ES_INIT
        self.stateHistory = deque(maxlen=50)

    def canCloseWidget(self):
        return self.state in CAN_CLOSE_WIDGET_STATE

    def easyPayEvent(self, epEvent):
        oldState = self.state
        self.state = ep_state_table_strict[self.state][epEvent]
        stateTrans = (oldState, self.state, epEvent)
        self.stateHistory.append(stateTrans)
        gamelog.debug('kjianjun, easypay state change, %d -> %d (%d)' % stateTrans)
        if self.state == ES_ERROR:
            self.failedFunc(epEvent)
        elif self.state == ES_SUCCESS:
            self.successFunc()
        elif self.state == ES_FAILED:
            self.failedFunc(epEvent)
        return self.state


class EasyPayProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EasyPayProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeEasyPay': self.onCloseEasyPay,
         'openCardCharge': self.onOpenCardCharge,
         'openWebCharge': self.onOpenWebCharge,
         'queryPointsInfo': self.onQueryPointsInfo,
         'getMyPointsInfo': self.onGetMyPointsInfo,
         'getEasyPayInfo': self.onGetEasyPayInfo,
         'getAlipayConfig': self.onGetAlipayConfig,
         'getChargeActivityInfo': self.onGetChargeActivityInfo,
         'easyBuyCoin': self.onEasyBuyCoin,
         'ecardRecharge': self.onEcardRecharge,
         'ePayRecharge': self.onEPayRecharge,
         'aliPayRecharge': self.onAlipayRecharge,
         'openQuickPay': self.onOpenQuickPay,
         'gotoHomePage': self.onGotoHomePage,
         'waitingTimeOut': self.onWaitingTimeOut,
         'gotoHelpWeb': self.onGotoHelpWeb,
         'gotoPayQueryWeb': self.onGotoPayQueryWeb,
         'sendAuthCode': self.onSendAuthCode,
         'getSendAuthCDLeftTime': self.onGetSendAuthCDLeftTime,
         'checkAuthCode': self.onCheckAuthCode,
         'checkAuthCodeQuickPay': self.onCheckAuthCodeQuickPay,
         'getUsePointHint': self.onGetUsePointHint}
        self.mediator = None
        self.easyPayInfo = {}
        self.caHistory = {}
        self.easyPayLog = {}
        self.lastSendAuthCodeTime = [0, 0]
        self.epStateMgr = EasyPayStateManager()
        self.easyPayWidgetId = uiConst.WIDGET_EASY_PAY
        self.waitingForFillOrder = False
        self.waitingHandler = None
        self.payFailedCount = 0
        self.addEvent(events.EVENT_POINTS_EXCHANGE_FAILED, self.onExchangeTianbiFailed, isGlobal=True)
        self.addEvent(events.EVENT_POINTS_EXCHANGE_COMPLETE, self.onExchangePointsComplete, isGlobal=True)
        self.addEvent(events.EVENT_EASYPAY_FILL_ORDER_DONE, self.onEasyPayFillOrderDone, isGlobal=True)
        self.addEvent(events.EVENT_POINTS_CHANGE, self.onPointsChanged, isGlobal=True)
        self.epStateMgr.setResultCallBack(self.onEasyPaySuccess, self.onEasyPayFailed)
        uiAdapter.registerEscFunc(self.easyPayWidgetId, self.close)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.easyPayWidgetId:
            self.mediator = mediator

    def show(self):
        if utils.getGameLanuage() in ('en',):
            projectId = uiUtils.getProjectId()
            cmd = 'start mycomgames://demandgamingform/%s' % projectId
            subprocess.Popen(cmd, shell=True)
            return
        if utils.isInternationalVersion():
            chargeUrl = SCD.data.get('chargeUrl')
            if chargeUrl:
                BigWorld.openUrl(chargeUrl)
            return
        if self.mediator:
            self.uiAdapter.setWidgetVisible(self.easyPayWidgetId, True)
        else:
            gameglobal.rds.ui.loadWidget(self.easyPayWidgetId, True, True)

    def close(self):
        if not self.epStateMgr.canCloseWidget():
            self.uiAdapter.setWidgetVisible(self.easyPayWidgetId, False)
            return
        if self.epStateMgr.state == ES_ORDER_READY:
            msg = gameStrings.TEXT_EASYPAYPROXY_243
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmQuitEasyPay))
        else:
            self.onConfirmQuitEasyPay()

    def alipayConfig(self):
        return gameglobal.rds.configData.get('enableAlipay', False)

    def chargeAcitivityConfig(self):
        return gameglobal.rds.configData.get('enableChargeActivity', False)

    def onUpdateClientCfg(self, key):
        if not self.mediator:
            return
        if key == 'enableAlipay':
            self.mediator.Invoke('refreshAlipayConifg')
        elif key == 'enableChargeActivity':
            self.mediator.Invoke('refreshChargeActivityConfig')

    def onConfirmQuitEasyPay(self):
        if self.epStateMgr.state == ES_ORDER_READY:
            leftTime = self.getSendAuthCDLeftTime()
            self.lastSendAuthCodeTime = map(lambda x, y: y - max(x - SEND_AUTH_CODE_CD_FADE, 0), leftTime, self.lastSendAuthCodeTime)
        self.saveEasyPayLog(ELR_CLOSE)
        super(EasyPayProxy, self).hide(True)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(self.easyPayWidgetId)
        self.mediator = None

    def reset(self):
        self.easyPayInfo = {}
        self.easyPayLog = {}
        self.epStateMgr.reset()
        self.mediator = None

    @ui.uiEvent(uiConst.WIDGET_EASY_PAY, events.EVENT_POINTS_CHANGE)
    def onEventPointsChange(self):
        if self.mediator:
            self.mediator.Invoke('refreshMyPointsInfo')

    def onExchangeTianbiFailed(self):
        if not gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            self.epStateMgr.easyPayEvent(EP_EVENT_EXCHANGE_FAILED)

    def onEasyPaySuccess(self):
        if not gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            self.easyPayLog['result'] = ER_SUCCESS
            self.saveEasyPayLog(ELR_SUCCESS)
            if self.mediator:
                self.mediator.Invoke('showEasyPayResult', GfxValue(True))

    def onEasyPayFailed(self, fEvent):
        if not gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            self.easyPayInfo['failedReason'] = self.getFailedReason(fEvent)
            self.easyPayLog['result'] = ER_FAILED
            if self.mediator:
                self.mediator.Invoke('showEasyPayResult', GfxValue(False))

    def clearAll(self):
        self.caHistory = {}

    def onExchangePointsComplete(self):
        if not gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            self.epStateMgr.easyPayEvent(EP_EVENT_EXCHANGE_COMPLETE)
            chargeCoin = self.easyPayInfo.get('buyCoinAll', 0) - self.easyPayInfo.get('exchangePoints', 0)
            if self.easyPayInfo.get('chargeDone', False):
                chargeCoin -= self.easyPayInfo.get('chargeCoin', 0)
            if chargeCoin > 0:
                self.easyPayInfo['chargeCoin'] = chargeCoin
                self.easyPayInfo['chargePoints'] = self.getFixedChargeNum(chargeCoin)
                self.easyPayFillOrder(self.easyPayInfo['chargePoints'])
            else:
                self.epStateMgr.easyPayEvent(EP_EVENT_END)

    def easyPayFillOrder(self, buyCount):
        self.easyPayLog['stage'] = ELS_ORDER_FILLED
        self.waitingForFillOrder = True
        if self.waitingHandler:
            BigWorld.cancelCallback(self.waitingHandler)
        self.waitingHandler = BigWorld.callback(FILL_ORDER_TIMEOUT, self.onFillOrderTimeOut)
        self.epStateMgr.easyPayEvent(EP_EVENT_FILL_ORDER)
        BigWorld.player().base.getQuickPaySignature(buyCount)

    def onEasyPayFillOrderDone(self, event):
        if not gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            self.easyPayInfo.update(event.data)
            self.waitingForFillOrder = False
            self.payFailedCount = 0
            if self.waitingHandler:
                BigWorld.cancelCallback(self.waitingHandler)
                self.waitingHandler = None
            status = self.easyPayInfo.get('status', -1)
            if status not in (200, 313):
                self.epStateMgr.easyPayEvent(EP_EVENT_ORDER_FILL_ERR)
            elif self.easyPayInfo.get('interfaceType', 0) == 0:
                self.epStateMgr.easyPayEvent(EP_EVENT_ORDER_FILL_ERR)
            else:
                self.epStateMgr.easyPayEvent(EP_EVENT_ORDER_FILLED)
                self.easyPayInfo['authCodeSendFlag'] = [False, False]
                self.easyPayLog['total_price'] = event.data.get('total_price', 0)
                self.easyPayLog['buy_amount'] = event.data.get('buy_amount', 0)
                self.easyPayLog['bill_id'] = event.data.get('bill_id', 0)
                self.easyPayLog['amount'] = float(event.data.get('amount', 0))
                if self.mediator:
                    self.mediator.Invoke('showDetailPage')

    def onPointsChanged(self):
        if self.epStateMgr.state not in (ES_QUERY_POINT_1, ES_QUERY_POINT_2):
            return
        p = BigWorld.player()
        myPoints = p.standbyPoints + p.commonPoints + p.specialPoints
        if myPoints < self.easyPayInfo.get('chargeCoin', myPoints + 1):
            return
        self.showWaiting()
        self.easyPayLog['stage'] = ELS_EXCHANGE_POINTS2
        self.easyPayInfo['chargeDone'] = True
        self.epStateMgr.easyPayEvent(EP_EVENT_CHARGE_POINT_ATTACH)
        gameglobal.rds.ui.tianyuMall.doExchangePoints(self.easyPayInfo['chargeCoin'])

    def getFixedChargeNum(self, origNum):
        return origNum

    def getFailedReason(self, fEvent):
        if fEvent == EP_EVENT_ORDER_FILL_ERR:
            status = self.easyPayInfo.get('status', -1)
            ret = FILL_ORDER_FAILED_DESC.get(status, gameStrings.TEXT_EASYPAYPROXY_393)
        elif fEvent == EP_EVENT_EXCHANGE_FAILED:
            ret = gameStrings.TEXT_EASYPAYPROXY_395
        elif fEvent == EP_EVENT_WAIT_TIMEOUT:
            ret = gameStrings.TEXT_EASYPAYPROXY_397
        else:
            ret = gameStrings.TEXT_EASYPAYPROXY_393
        return ret

    def onCloseEasyPay(self, *arg):
        self.close()

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

    def onQueryPointsInfo(self, *arg):
        gameglobal.rds.ui.tianyuMall.onQueryPointsInfo()

    def onGetMyPointsInfo(self, *arg):
        gameglobal.rds.ui.tianyuMall.onGetMyPointsInfo()

    def onGetEasyPayInfo(self, *arg):
        self.easyPayInfo['quickPayListFormat'] = []
        quickPayList = self.easyPayInfo.get('quickPayList', [])
        for qp in quickPayList:
            attr = qp.split(',')
            for i in range(len(attr)):
                pass

            self.easyPayInfo['quickPayListFormat'].append(attr)

        return uiUtils.dict2GfxDict(self.easyPayInfo, True)

    def onGetAlipayConfig(self, *arg):
        return GfxValue(self.alipayConfig())

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
        caList.append(self.genChargeActivityEtcInfo())
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

    @ui.callFilter(3)
    def onEasyBuyCoin(self, *arg):
        p = BigWorld.player()
        myPoints = p.standbyPoints + p.commonPoints + p.specialPoints
        self.easyPayInfo['buyCoinAll'] = int(arg[3][0].GetNumber())
        self.easyPayInfo['usePoint'] = arg[3][1].GetBool()
        self.easyPayInfo['caId'] = int(arg[3][2].GetNumber())
        if self.checkChargeActivityUsable(self.easyPayInfo['caId']):
            caData = CCAD.data.get(self.easyPayInfo['caId'], {})
            bonus = caData.get('bonusCoin', 0)
            basePrice = caData.get('chargeCoin', 0)
            self.easyPayInfo['caInfo'] = gameStrings.TEXT_EASYPAYPROXY_557 % (bonus, bonus + basePrice)
        else:
            self.easyPayInfo['caInfo'] = ''
        self.showWaiting()
        self.epStateMgr.easyPayEvent(EP_EVENT_START)
        if self.easyPayInfo['usePoint'] and myPoints > 0:
            exchangePoints = min(myPoints, self.easyPayInfo['buyCoinAll'])
            self.easyPayInfo['exchangePoints'] = exchangePoints
            self.easyPayLog['stage'] = ELS_EXCHANGE_POINTS1
            self.easyPayLog['buy_coin1'] = exchangePoints
            self.epStateMgr.easyPayEvent(EP_EVENT_EXCHANGE_START)
            gameglobal.rds.ui.tianyuMall.doExchangePoints(exchangePoints)
        else:
            self.easyPayInfo['chargeCoin'] = self.easyPayInfo['buyCoinAll']
            self.easyPayInfo['chargePoints'] = self.getFixedChargeNum(self.easyPayInfo['chargeCoin'])
            self.easyPayFillOrder(self.easyPayInfo['chargePoints'])

    def onGotoHomePage(self, *arg):
        self.epStateMgr.easyPayEvent(EP_EVENT_RESET)
        self.saveEasyPayLog(ELR_RESET)
        self.easyPayInfo = {}
        self.easyPayLog = {}

    def onWaitingTimeOut(self, *arg):
        self.epStateMgr.easyPayEvent(EP_EVENT_WAIT_TIMEOUT)
        if self.epStateMgr.state == ES_ORDER_READY and self.mediator:
            tips = uiUtils.toHtml(gameStrings.TEXT_EASYPAYPROXY_589, WARN_COLOR)
            self.mediator.Invoke('showAuthCodeCheckResult', GfxValue(gbk2unicode(tips)))

    def showWaiting(self, show = True, timeOut = 0):
        if not self.mediator:
            return
        self.mediator.Invoke('showWaiting', (GfxValue(show), GfxValue(timeOut)))

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

    def onSendAuthCode(self, *arg):
        interfaceType = int(arg[3][0].GetNumber())
        quickPayId = arg[3][1].GetString()
        self.easyPayInfo['userPayType'] = interfaceType
        cdIndex = 0 if self.easyPayInfo.get('userPayType', 1) == 1 else 1
        self.lastSendAuthCodeTime[cdIndex] = utils.getNow()
        self.easyPayInfo.setdefault('authCodeSendFlag', [False, False])[cdIndex] = True
        self.mediator.Invoke('showAuthCodeSendResult', (GfxValue(200), GfxValue('')))
        remoteInterface.quickPaySendAuthCode(self.easyPayInfo['sid'], self.easyPayInfo['bill_id'], interfaceType, quickPayId, self.onSendAuthCodeDone)

    def onSendAuthCodeDone(self, rStatus, content):
        if not content:
            return
        if rStatus != 200:
            return
        self.easyPayInfo.update(content)
        status = self.easyPayInfo.get('status', -1)
        if status == 200:
            tips = ''
        else:
            reason = FILL_ORDER_FAILED_DESC.get(status, gameStrings.TEXT_EASYPAYPROXY_638)
            tips = uiUtils.toHtml(reason, WARN_COLOR)
        if not self.mediator:
            return
        self.mediator.Invoke('showAuthCodeSendResult', (GfxValue(status), GfxValue(gbk2unicode(tips))))

    def getSendAuthCDLeftTime(self):
        return map(lambda x: SEND_AUTH_CODE_CD - (utils.getNow() - x), self.lastSendAuthCodeTime)

    def onGetSendAuthCDLeftTime(self, *arg):
        return uiUtils.array2GfxAarry(self.getSendAuthCDLeftTime(), True)

    def onCheckAuthCode(self, *arg):
        authCode = int(arg[3][0].GetString())
        self.easyPayLog['stage'] = ELS_ORDER_PAYING
        self.easyPayLog['method'] = ELM_BALANCE_CHARGE
        self.showWaiting()
        self.epStateMgr.easyPayEvent(EP_EVENT_SEND_AUTH_CODE)
        remoteInterface.quichPayCompleteBalancePay(self.easyPayInfo['sid'], self.easyPayInfo['bill_id'], authCode, self.onCheckAuthCodeDone)

    def onCheckAuthCodeQuickPay(self, *arg):
        authCode = int(arg[3][0].GetString())
        quickPayId = arg[3][1].GetString()
        bankCode = arg[3][2].GetString()
        self.easyPayLog['stage'] = ELS_ORDER_PAYING
        self.easyPayLog['method'] = ELM_QUICKPAY_CHARGE
        self.showWaiting()
        self.epStateMgr.easyPayEvent(EP_EVENT_SEND_AUTH_CODE)
        remoteInterface.quickPayCompleteQuickPay(self.easyPayInfo['sid'], self.easyPayInfo['bill_id'], authCode, quickPayId, bankCode, self.easyPayInfo.get('chargeId', ''), self.easyPayInfo.get('oriMerchSeq', ''), self.onCheckAuthCodeDone)

    def onCheckAuthCodeDone(self, rStatus, content):
        if not content:
            return
        if rStatus != 200:
            return
        self.easyPayInfo.update(content)
        self.epStateMgr.easyPayEvent(EP_EVENT_AUTH_CODE_RESULT)
        if not self.mediator:
            return
        status = self.easyPayInfo.get('status', -1)
        if status != 200:
            reason = FILL_ORDER_FAILED_DESC.get(status, gameStrings.TEXT_EASYPAYPROXY_638)
            tips = uiUtils.toHtml(reason, WARN_COLOR)
            self.mediator.Invoke('showAuthCodeCheckResult', GfxValue(gbk2unicode(tips)))
        else:
            self.mediator.Invoke('showAuthCodeCheckResult', GfxValue(''))
            self.onChargeDone()

    def onEcardRecharge(self, *arg):
        remoteInterface.redirectWangYiBaoToPay(self.easyPayInfo['sid'], self.easyPayInfo['bill_id'])
        self.webChargeConfirmMsgBox()
        self.easyPayLog['stage'] = ELS_ORDER_PAYING
        self.easyPayLog['method'] = ELM_WEB_CHARGE

    def onEPayRecharge(self, *arg):
        remoteInterface.redirectWangYiBaoToPay(self.easyPayInfo['sid'], self.easyPayInfo['bill_id'])
        self.webChargeConfirmMsgBox()
        self.easyPayLog['stage'] = ELS_ORDER_PAYING
        self.easyPayLog['method'] = ELM_WEB_CHARGE

    def onAlipayRecharge(self, *arg):
        remoteInterface.redirectWangYiBaoToPay(self.easyPayInfo['sid'], self.easyPayInfo['bill_id'], True)
        self.webChargeConfirmMsgBox()
        self.easyPayLog['stage'] = ELS_ORDER_PAYING
        self.easyPayLog['method'] = ELM_ALIPAY_CHARGE

    def onOpenQuickPay(self, *arg):
        remoteInterface.redirectWangYiBaoToRegisterqp(self.easyPayInfo['sid'], self.easyPayInfo['orderId'])
        self.webChargeConfirmMsgBox()
        self.easyPayLog['stage'] = ELS_ORDER_PAYING
        self.easyPayLog['method'] = ELM_NEW_QUICKPAY

    def webChargeConfirmMsgBox(self):
        msg = gameStrings.TEXT_EASYPAYPROXY_726
        yesText = gameStrings.TEXT_EASYPAYPROXY_727
        noText = gameStrings.TEXT_EASYPAYPROXY_728
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onChargeDone), yesText, None, noText)

    def onChargeDone(self):
        self.epStateMgr.easyPayEvent(EP_EVENT_QUERY_POINT_1)
        self.showWaiting(True, -1)
        self.easyPayInfo['chargeDone'] = True
        self.easyPayInfo['startQueryTime'] = utils.getNow()
        self.onRechargePointsCheck1()

    def onRechargePointsCheck1(self):
        if self.epStateMgr.state != ES_QUERY_POINT_1:
            if self.easyPayInfo.get('checkHandler', None):
                BigWorld.cancelCallback(self.easyPayInfo['checkHandler'])
            return
        else:
            self.easyPayLog['stage'] = ELS_QUERY_POINTS
            now = utils.getNow()
            if now - self.easyPayInfo['startQueryTime'] < QUICK_CHECK_TIME:
                BigWorld.player().base.queryDianKa()
                self.easyPayInfo['checkHandler'] = BigWorld.callback(QUICK_CHECK_INTERVAL, self.onRechargePointsCheck1)
            else:
                if self.easyPayInfo.get('checkHandler', None):
                    BigWorld.cancelCallback(self.easyPayInfo['checkHandler'])
                if self.mediator:
                    self.mediator.Invoke('showLongWaiting', GfxValue(LONG_CHECK_TIME))
                self.epStateMgr.easyPayEvent(EP_EVENT_WAIT_TIMEOUT)
                self.easyPayInfo['startQueryTime'] = now
                self.onRechargePointsCheck2()
            return

    def onRechargePointsCheck2(self):
        if self.epStateMgr.state != ES_QUERY_POINT_2:
            if self.easyPayInfo.get('checkHandler', None):
                BigWorld.cancelCallback(self.easyPayInfo['checkHandler'])
            return
        else:
            now = utils.getNow()
            if now - self.easyPayInfo['startQueryTime'] < LONG_CHECK_TIME:
                BigWorld.player().base.queryDianKa()
                self.easyPayInfo['checkHandler'] = BigWorld.callback(LONG_CHECK_INTERVAL, self.onRechargePointsCheck2)
            else:
                if self.easyPayInfo.get('checkHandler', None):
                    BigWorld.cancelCallback(self.easyPayInfo['checkHandler'])
                self.epStateMgr.easyPayEvent(EP_EVENT_WAIT_TIMEOUT)
                self.easyPayInfo['startQueryTime'] = 0
                self.saveEasyPayLog(ELR_TIMEOUT)
            return

    def saveEasyPayLog(self, reason):
        if not self.easyPayLog:
            return
        self.easyPayLog['version'] = EL_VERSION
        self.easyPayLog['reason'] = reason
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
        self.easyPayLog = {}

    def onFillOrderTimeOut(self):
        if not self.waitingForFillOrder:
            return
        self.payFailedCount += 1
        if self.payFailedCount >= PAY_FAIL_WARN_LIMIT:
            self.payFailedCount = 0
            msg = gameStrings.TEXT_EASYPAYPROXY_805 % (PAY_FAIL_WARN_LIMIT, FILL_ORDER_TIMEOUT)
            BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})

    def onGetUsePointHint(self, *arg):
        enabled = arg[3][0].GetBool()
        if enabled:
            hint = uiUtils.getTextFromGMD(GMDD.data.EASY_PAY_USE_POINT_HINT, gameStrings.TEXT_EASYPAYPROXY_812)
        else:
            hint = uiUtils.getTextFromGMD(GMDD.data.EASY_PAY_USE_POINT_GREY_HINT, gameStrings.TEXT_EASYPAYPROXY_815)
        return GfxValue(gbk2unicode(hint))
