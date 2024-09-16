#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleCollectProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import events
import gameConfigUtils
import clientUtils
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from item import Item
from data import consumable_item_data as CID
from data import item_data as ID
from data import sys_config_data as SCD
from data import activity_collect_data as ACD
from data import mall_item_data as MID
MAX_ITEM_NUM = 6
MAX_BONUS_NUM = 3

class ActivitySaleCollectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleCollectProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.widget = None
        self.timer = None

    def initCollect(self, widget):
        self.widget = widget
        self.delTimer()
        BigWorld.player().cell.getActivityCollectInfo()
        self.initUI()

    def initUI(self):
        if not self.widget:
            return
        self.widget.rechargeBtn.addEventListener(events.BUTTON_CLICK, self.handleClickRechage, False, 0, True)
        self.refreshPanel()
        self.addEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshCoin)
        self.refreshCoin()
        self.timerFunc()
        self.addTimer()

    def unRegisterCollect(self):
        self.widget = None
        self.reset()

    def refreshPanel(self):
        if not self.widget:
            return
        activityData = self.getActivityData()
        if not activityData:
            return
        self.widget.helpIcon.helpKey = activityData.get('helpId', 0)
        bgImage = activityData.get('bgImage', '')
        self.widget.bg.loadImage('activitySale/%s.dds' % bgImage)
        showItemList = activityData.get('showItemList', ())
        itemListLen = len(showItemList)
        for i in xrange(MAX_ITEM_NUM):
            itemMc = self.widget.getChildByName('item%d' % i)
            if i >= itemListLen:
                itemMc.visible = False
                continue
            else:
                itemMc.visible = True
            itemInfo = showItemList[i]
            itemMc.slot.fitsize = True
            itemMc.slot.dragable = False
            itemMc.slot.itemId = itemInfo[0]
            itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemInfo[0], itemInfo[1]))
            itemMc.slot.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)

        mallId = activityData.get('mallId', 0)
        priceVal = MID.data.get(mallId, {}).get('priceVal', 0)
        self.widget.buyBtn.moneyIcon.bonusType = 'tianBi'
        self.widget.buyBtn.label = str(priceVal)
        self.widget.buyBtn.mallId = mallId
        self.widget.buyBtn.addEventListener(events.BUTTON_CLICK, self.handleClickBuyBtn, False, 0, True)
        self.refreshBonusInfo()
        self.uiAdapter.activitySale.refreshInfo()

    def refreshBonusInfo(self):
        if not self.widget:
            return
        progresStart = self.widget.progressBar.x
        progressLen = self.widget.progressBar.width
        activityData = self.getActivityData()
        if not activityData:
            return
        activityInfo = BigWorld.player().activityCollectInfo
        buyMallFlag = activityInfo.get('buyMallFlag', 0)
        self.widget.buyBtn.disabled = buyMallFlag
        self.widget.buyBtn.moneyIcon.visible = not buyMallFlag
        self.widget.buyBtn.desc.visible = not buyMallFlag
        if buyMallFlag:
            self.widget.buyBtn.label = gameStrings.ACTIVITY_SALE_COLLECT_BOUGHT
        else:
            mallId = activityData.get('mallId', 0)
            priceVal = MID.data.get(mallId, {}).get('priceVal', 0)
            self.widget.buyBtn.label = str(priceVal)
        bonusIds = activityData.get('bonusIds', ())
        rewardMarginEnd = activityData.get('rewardMarginEnd', 0)
        rewardMargins = activityData.get('rewardMargins', (0, 0, 0))
        bonusDesc = activityData.get('bonusDesc', [])
        rewardConditions = activityData.get('rewardConditions', (0, 0, 1))
        totalProgress = activityInfo.get('totalProgress', 0)
        finishRewardMargins = activityInfo.get('finishRewardMargins', [])
        for i in xrange(MAX_BONUS_NUM):
            rewardMargin = rewardMargins[i]
            isReceived = rewardMargin in finishRewardMargins
            rewardCondition = rewardConditions[i]
            if rewardCondition:
                canReceive = totalProgress >= rewardMargin and not isReceived and buyMallFlag
            else:
                canReceive = totalProgress >= rewardMargin and not isReceived
            tipsMc = self.widget.getChildByName('tip%d' % i)
            bonusMc = self.widget.getChildByName('bonus%d' % i)
            if i >= len(bonusIds):
                tipsMc.visible = False
                bonusMc.visible = False
                continue
            else:
                tipsMc.visible = True
                bonusMc.visible = True
                bonusInfo = clientUtils.genItemBonusEx(bonusIds[i], mustItem=False)
                tipsMc.x = progresStart + progressLen * rewardMargins[i] / rewardMarginEnd - 10
                tipsMc.gotoAndStop('light')
                bonusMc.x = tipsMc.x - 22
                bonusMc.canReceive.visible = canReceive
                bonusMc.effect.visible = canReceive
                ASUtils.setHitTestDisable(bonusMc.yesIcon, True)
                bonusMc.yesIcon.visible = isReceived
                bonusMc.slot.fitsize = True
                bonusMc.slot.dragable = False
                if bonusInfo:
                    bonusMc.slot.setItemSlotData(uiUtils.getGfxItemById(bonusInfo[0][0], bonusInfo[0][1]))
                bonusMc.desc.htmlText = bonusDesc[i]
                bonusMc.data = rewardMargins[i]
                bonusMc.slot.addEventListener(events.MOUSE_CLICK, self.handleClickBonus, False, 0, True)

        self.widget.progressBar.currentValue = totalProgress
        self.widget.progressBar.maxValue = rewardMarginEnd
        self.refreshCoin()
        self.uiAdapter.activitySale.refreshInfo()

    def handleClickBuyBtn(self, *args):
        e = ASObject(args[3][0])
        mallId = e.currentTarget.mallId
        if mallId:
            gameglobal.rds.ui.tianyuMall.mallBuyConfirm(mallId, 1, 'collect.0')

    def handleClickRechage(self, *args):
        BigWorld.player().openRechargeFunc()

    def handleClickBonus(self, *args):
        e = ASObject(args[3][0])
        progress = e.currentTarget.parent.data
        BigWorld.player().cell.receiveActivityCollectReward(progress)

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(1, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        activityData = self.getActivityData()
        endTime = activityData.get('crontabEnd', '0 8 30 4 * 2020')
        left = 0
        if utils.getDisposableCronTabTimeStamp(endTime) >= utils.getNow():
            left = utils.getDisposableCronTabTimeStamp(endTime) - utils.getNow()
        self.widget.leftTimeTxt.text = utils.formatDurationShortVersion(left)

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None

    def refreshCoin(self):
        if not self.widget:
            return
        p = BigWorld.player()
        tianbi = format(p.unbindCoin + p.bindCoin + p.freeCoin, ',')
        unBindTianbi = uiUtils.toHtml(gameStrings.ACTIVITY_SALE_COLLECT_COIN % format(p.unbindCoin, ','), '#79c725')
        self.widget.moneyTxt.htmlText = '%s%s' % (tianbi, unBindTianbi)

    def canOpen(self):
        flag = False
        if not gameglobal.rds.configData.get('enableActivityCollect', False):
            return flag
        activityData = self.getActivityData()
        beginTime = activityData.get('crontabStart', '')
        endTime = activityData.get('crontabEnd', '')
        if beginTime and endTime and utils.getDisposableCronTabTimeStamp(beginTime) <= utils.getNow() < utils.getDisposableCronTabTimeStamp(endTime):
            flag = True
        return flag

    def getRedPointVisible(self):
        canReceive = False
        activityData = self.getActivityData()
        activityInfo = BigWorld.player().activityCollectInfo
        rewardMargins = activityData.get('rewardMargins', (0, 0, 0))
        rewardConditions = activityData.get('rewardConditions', (0, 0, 1))
        buyMallFlag = activityInfo.get('buyMallFlag', 0)
        totalProgress = activityInfo.get('totalProgress', 0)
        finishRewardMargins = activityInfo.get('finishRewardMargins', [])
        for i in xrange(MAX_BONUS_NUM):
            rewardMargin = rewardMargins[i]
            isReceived = rewardMargin in finishRewardMargins
            rewardCondition = rewardConditions[i]
            if rewardCondition:
                canReceive = totalProgress >= rewardMargin and not isReceived and buyMallFlag
            else:
                canReceive = totalProgress >= rewardMargin and not isReceived
            if canReceive:
                return canReceive

        return canReceive

    def handleShowFit(self, *args):
        e = ASObject(args[3][0])
        itemId = int(e.currentTarget.itemId)
        if e.buttonIdx == uiConst.LEFT_BUTTON:
            cidData = CID.data.get(itemId, {})
            sType = cidData.get('sType', 0)
            if sType == Item.SUBTYPE_2_GET_SELECT_ITEM:
                gameglobal.rds.ui.itemChoose.show(itemId, showType=0)
            else:
                self.uiAdapter.fittingRoom.addItem(Item(itemId))

    def pushCollectMessage(self):
        if BigWorld.player().lv < SCD.data.get('activitySaleMinLv', 0):
            return
        data = self.getActivityData()
        pushId = data.get('pushId', uiConst.MESSAGE_TYPE_COLLECT_ACTIVITY)
        if pushId not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': self.onPushMsgClick})

    def onPushMsgClick(self):
        if not self.widget:
            gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_COLLECT)
        self.removeCollectPushMsg()

    def removeCollectPushMsg(self):
        data = self.getActivityData()
        pushId = data.get('pushId', uiConst.MESSAGE_TYPE_COLLECT_ACTIVITY)
        if pushId in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(pushId)

    def getActivityData(self):
        activityId = self.getCurActivityId()
        activityData = ACD.data.get(activityId, {})
        return activityData

    def getCurActivityId(self):
        hostId = utils.getHostId()
        for id, value in ACD.data.iteritems():
            hostIds = value.get('hostIds', ())
            beginTime = value.get('crontabStart', '')
            endTime = value.get('crontabEnd', '')
            if not hostIds or hostId in hostIds:
                if beginTime and endTime and utils.getDisposableCronTabTimeStamp(beginTime) <= utils.getNow() <= utils.getDisposableCronTabTimeStamp(endTime):
                    return id

        return 0
