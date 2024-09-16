#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleNewbiePayProxy.o
import BigWorld
import utils
import events
import uiUtils
import uiConst
import gameglobal
import clientUtils
from uiProxy import UIProxy
from gamestrings import gameStrings
from callbackHelper import Functor
from data import newbie_activity_data as NAD
from cdata import game_msg_def_data as GMDD

class ActivitySaleNewbiePayProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleNewbiePayProxy, self).__init__(uiAdapter)
        self.widget = None
        self.newbieInfo = None
        self.finishTime = 0
        self.timer = None
        self.endTimer = None
        self.reset()

    def reset(self):
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def stopEndTimer(self):
        if self.endTimer:
            BigWorld.cancelCallback(self.endTimer)
            self.endTimer = None

    def clearAll(self):
        self.newbieInfo = None
        self.finishTime = 0
        self.stopEndTimer()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        self.widget.mainMc.item.slot.dragable = False
        self.widget.mainMc.timeHint.leftTime.text = ''
        self.widget.mainMc.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        if not self.newbieInfo:
            return
        nadData = NAD.data.get(getattr(self.newbieInfo, 'aId', 0), {})
        if not nadData:
            return
        itemBonus = clientUtils.genItemBonus(nadData.get('rewardDetail', 0))
        itemId, itemNum = itemBonus[0]
        itemInfo = uiUtils.getGfxItemById(itemId, itemNum)
        self.widget.mainMc.item.slot.setItemSlotData(itemInfo)
        self.widget.mainMc.chargeValue.text = str(getattr(self.newbieInfo, 'tCharge', 0))
        bgPath = 'newbiePay/%s.dds' % str(nadData.get('activityImages', ''))
        self.widget.mainMc.bg.loadImage(bgPath)
        self.stopTimer()
        self.updateTime()

    def updateTime(self):
        if not self.widget:
            return
        leftTime = self.finishTime - utils.getNow()
        if leftTime <= 0:
            leftTime = 0
        self.widget.mainMc.timeHint.leftTime.text = gameStrings.LEFT_TIME % uiUtils.formatTime(leftTime)
        if leftTime <= 0:
            return
        self.timer = BigWorld.callback(1, self.updateTime)

    def handleClickConfirmBtn(self, *args):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableQrcodeRecharge', False):
            p.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        if self.finishTime < utils.getNow():
            p.showGameMsg(GMDD.data.ACTIVITY_SALE_NEWBIE_PAY_OVER_TIME, ())
            return
        assignCoin = NAD.data.get(getattr(self.newbieInfo, 'aId', 0), {}).get('needCharge', 0)
        self.uiAdapter.newRecharge.show(assignCoin=assignCoin)

    def updateNewbieInfo(self, newbieInfo):
        needPush = False
        if self.newbieInfo:
            if getattr(self.newbieInfo, 'aId', 0) != getattr(newbieInfo, 'aId', 0):
                needPush = True
            if self.finishTime < utils.getNow() and getattr(newbieInfo, 'remainTime', 0) > 0:
                needPush = True
        else:
            needPush = True
        self.newbieInfo = newbieInfo
        remainTime = getattr(self.newbieInfo, 'remainTime', 0)
        pushMsg = self.uiAdapter.pushMessage
        if getattr(self.newbieInfo, 'isReward', 0):
            pushMsg.removePushMsg(uiConst.MESSAGE_TYPE_ACTIVITY_SALE_NEWBIE_PAY)
        elif needPush and not self.widget:
            pushMsg.removePushMsg(uiConst.MESSAGE_TYPE_ACTIVITY_SALE_NEWBIE_PAY)
            callBackDict = {'click': Functor(self.uiAdapter.activitySale.show, uiConst.ACTIVITY_SALE_TAB_NEWBIE_PAY)}
            pushMsg.setCallBack(uiConst.MESSAGE_TYPE_ACTIVITY_SALE_NEWBIE_PAY, callBackDict)
            data = {'startTime': utils.getNow(),
             'totalTime': remainTime,
             'data': []}
            pushMsg.addPushMsg(uiConst.MESSAGE_TYPE_ACTIVITY_SALE_NEWBIE_PAY, data=data)
        self.finishTime = utils.getNow() + remainTime
        self.refreshInfo()
        self.uiAdapter.activitySale.refreshInfo()
        if remainTime > 0:
            self.stopEndTimer()
            self.endTimer = BigWorld.callback(remainTime + 1, self.uiAdapter.activitySale.refreshInfo)

    def canOpenTab(self):
        if not gameglobal.rds.configData.get('enableNewbiePay', False):
            return (False, False)
        if not self.newbieInfo:
            return (False, False)
        if getattr(self.newbieInfo, 'isReward', 0) or self.finishTime < utils.getNow():
            return (False, False)
        return (True, True)
