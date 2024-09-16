#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleLoopChargeProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
import utils
import clientUtils
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis import uiUtils
from data import sys_config_data as SCD
from data import coin_charge_reward_data as CCRD
MAX_ITEM_CNT = 4
MAX_LOOP_CHARGE_MAX_CNT = 4
COUNT_TYPE_CHARGE = 1
COUNT_TYPE_CONSUME = 2
TIANQUAN_ITEM_ID = 3
RAFFLE_ITEM_ID = 442388

class ActivitySaleLoopChargeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleLoopChargeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rewardKeyVal = None
        self.overdueRewardKeyVal = None
        self.countType = COUNT_TYPE_CHARGE
        self.reset()

    def reset(self):
        self.pushId = 0
        self.timer = None

    def initLoopCharge(self, widget):
        self.widget = widget
        self.delTimer()
        if not self.getRewardKeyVal():
            return
        self.initUI()
        self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.accmulateCharge.list.itemRenderer = 'ActivitySaleLoopCharge_ItemRender'
        self.widget.accmulateCharge.list.lableFunction = self.lableFunction
        self.widget.openBoxBtn.addEventListener(events.BUTTON_CLICK, self.handleOpenBoxBtnClick, False, 0, True)
        canRaffle = self.getRewardKeyVal()[1].has_key('raffleItemSetInfo')
        self.widget.openBoxBtn.visible = canRaffle
        self.widget.txt0.visible = canRaffle
        self.widget.txtRemain.visible = canRaffle
        self.widget.chargeBtn.addEventListener(events.BUTTON_CLICK, self.handleChargeBtnClick, False, 0, True)
        self.widget.icon.fitSize = True
        iconPath = 'activitySale/%s.dds' % self.getRewardKeyVal()[1].get('activitySaleLoopChargeBg', 'activitysalepointsbgv1')
        self.widget.icon.loadImage(iconPath)
        self.timerFunc()
        self.addTimer()

    def unRegisterLoopCharge(self):
        self.widget = None
        self.reset()

    def getRedPointVisible(self):
        return self.getRewardCnt() > 0

    def canOpen(self):
        if not gameglobal.rds.configData.get('enableChargeRewardLoop', False):
            return False
        rewardkeyVal = self.getRewardKeyVal()
        if not rewardkeyVal:
            return False
        if self.overdueRewardKeyVal and rewardkeyVal[0] == self.overdueRewardKeyVal[0] and self.getRewardCnt() <= 0:
            return False
        return True

    def getRewardKeyVal(self):
        if not gameglobal.rds.configData.get('enableChargeRewardLoop', False):
            return
        now = utils.getNow()
        if self.rewardKeyVal:
            val = self.rewardKeyVal[1]
            beginTime = utils.getTimeSecondFromStr(val.get('beginTime', ''))
            endTime = utils.getTimeSecondFromStr(val.get('endTime', ''))
            if now >= beginTime and now <= endTime:
                return self.rewardKeyVal
            self.rewardKeyVal = None
        for key, val in CCRD.data.iteritems():
            beginTime = utils.getTimeSecondFromStr(val.get('beginTime', ''))
            endTime = utils.getTimeSecondFromStr(val.get('endTime', ''))
            whiteList = val.get('whiteList', None)
            if whiteList and utils.getHostId() not in whiteList:
                continue
            if now >= beginTime and now <= endTime:
                self.rewardKeyVal = (key, val)
                break
            if now >= beginTime and now <= endTime + 604800:
                self.overdueRewardKeyVal = (key, val)

        if self.rewardKeyVal:
            return self.rewardKeyVal
        else:
            return self.overdueRewardKeyVal

    def genChargeRewardItemInfo(self, myRewardInfo, index, rewardInfo, chooseReward):
        if rewardInfo[0] > 0:
            self.countType = COUNT_TYPE_CHARGE
        if rewardInfo[1] > 0:
            self.countType = COUNT_TYPE_CONSUME
        chargeNum = myRewardInfo[1] if self.countType == COUNT_TYPE_CHARGE else myRewardInfo[2]
        needCount = rewardInfo[0] if rewardInfo[0] else rewardInfo[1]
        ret = {}
        rewardList = []
        if rewardInfo[2] > 0:
            rewardList.append(uiUtils.getGfxItemById(TIANQUAN_ITEM_ID, rewardInfo[2]))
        bonusId = rewardInfo[3]
        ret['satisfied'] = chargeNum >= needCount
        if bonusId:
            bonusItems = clientUtils.genItemBonus(bonusId, True)
            for itemId, count in bonusItems:
                rewardList.append(uiUtils.getGfxItemById(itemId, count))

        ret['needCount'] = needCount
        ret['itemList'] = rewardList
        if len(rewardList) < MAX_ITEM_CNT and rewardInfo[-1] > 0:
            rewardList.append(uiUtils.getGfxItemById(RAFFLE_ITEM_ID, rewardInfo[-1]))
        if len(chooseReward) > index:
            if len(chooseReward[index]) > 0 and chooseReward[index][1] > 0:
                ret['rewardBtnVisible'] = True
            else:
                ret['rewardBtnVisible'] = False
        else:
            ret['rewardBtnVisible'] = False
        choosedRewardFlag = len(myRewardInfo) >= 5 and index in myRewardInfo[4]
        if choosedRewardFlag:
            ret['rewardBtnEnable'] = False
            ret['rewardBtnLabel'] = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
            ret['isChooseReward'] = False
        else:
            ret['rewardBtnEnable'] = True
            if myRewardInfo[1] >= rewardInfo[0] and myRewardInfo[2] >= rewardInfo[1]:
                ret['rewardBtnLabel'] = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_151
                ret['isChooseReward'] = True
            else:
                ret['rewardBtnLabel'] = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_154
                ret['isChooseReward'] = False
        ret['index'] = index
        return ret

    def getMyRewardInfo(self):
        rewardKeyVal = self.getRewardKeyVal()
        if not rewardKeyVal:
            return ()
        p = BigWorld.player()
        for info in p.chargeRewardInfo:
            if info[0] == rewardKeyVal[0]:
                return info

        return (rewardKeyVal[0],
         0,
         0,
         [],
         [],
         [0,
          0,
          0,
          0])

    def clearAll(self):
        self.rewardKeyVal = None
        self.overdueRewardKeyVal = None
        self.countType = COUNT_TYPE_CHARGE

    def getAccmulateInfo(self):
        accmulateInfo = {}
        infoList = []
        rewardKeyVal = self.getRewardKeyVal()
        myRewardInfo = None
        if not rewardKeyVal:
            return accmulateInfo
        else:
            myRewardInfo = self.getMyRewardInfo()
            for index, rewardInfo in enumerate(rewardKeyVal[1].get('chargeCoins', [])):
                chooseReward = rewardKeyVal[1].get('rewardsForChoose', [])
                infoList.append(self.genChargeRewardItemInfo(myRewardInfo, index, rewardInfo, chooseReward))

            accmulateInfo['infoList'] = infoList
            accmulateInfo['chargedNum'] = myRewardInfo[1] if self.countType == COUNT_TYPE_CHARGE else myRewardInfo[2]
            gamelog.info('jbx:getAccmulateInfo', accmulateInfo)
            return accmulateInfo

    def getLoopChargeInfo(self):
        rewardKeyVal = self.getRewardKeyVal()
        myRewardInfo = self.getMyRewardInfo()
        if not rewardKeyVal or not myRewardInfo:
            return
        chargeNum = 0
        loopChargeInfo = {}
        chargeCoinsLoop = rewardKeyVal[1].get('chargeCoinsLoop', ())
        if chargeCoinsLoop:
            chargeNum = myRewardInfo[1] if chargeCoinsLoop[0] else myRewardInfo[2]
            needCount = chargeCoinsLoop[0] if chargeCoinsLoop[0] else chargeCoinsLoop[1]
            minLimitNum = chargeCoinsLoop[2]
            if minLimitNum >= 0:
                loopChargeInfo['visible'] = chargeNum >= minLimitNum
                loopChargeInfo['tipsVisible'] = chargeNum < minLimitNum
                loopChargeInfo['needCount'] = needCount
                loopChargeInfo['chargeNum'] = max(0, chargeNum - minLimitNum)
                itemList = []
                for itemId, cnt in clientUtils.genItemBonus(chargeCoinsLoop[3], True):
                    itemList.append(uiUtils.getGfxItemById(itemId, cnt))

                loopChargeInfo['itemList'] = itemList
            else:
                loopChargeInfo['visible'] = False
                loopChargeInfo['tipsVisible'] = False
        else:
            loopChargeInfo['visible'] = False
            loopChargeInfo['tipsVisible'] = False
        gamelog.info('jbx:getLoopChargeInfo', loopChargeInfo)
        return loopChargeInfo

    def refreshLoopCharge(self):
        gamelog.info('jbx:refreshLoopCharge')
        loopChargeInfo = self.getLoopChargeInfo()
        self.widget.loopCharge.visible = loopChargeInfo['visible']
        self.widget.txtTips.visible = loopChargeInfo['tipsVisible']
        self.widget.txtTips.text = self.getRewardKeyVal()[1].get('loopChargeTips', '')
        if self.widget.loopCharge.visible:
            self.widget.loopCharge.txtGain.text = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_227 % loopChargeInfo['needCount']
            for i in xrange(MAX_LOOP_CHARGE_MAX_CNT):
                slotMc = getattr(self.widget.loopCharge, 'item%d' % i)
                if i >= len(loopChargeInfo['itemList']):
                    slotMc.visible = False
                else:
                    slotMc.visible = True
                    slotMc.usedFlag.visible = False
                    slotMc.slot.dragable = False
                    slotMc.slot.setItemSlotData(loopChargeInfo['itemList'][i])

            needCount = loopChargeInfo['needCount']
            chargeNum = loopChargeInfo['chargeNum']
            currentValue = chargeNum - chargeNum / needCount * needCount
            self.widget.loopCharge.progressBar.maxValue = needCount
            self.widget.loopCharge.progressBar.currentValue = currentValue
            self.widget.loopCharge.txtValue.text = '%d/%d' % (currentValue, needCount)
            self.widget.loopCharge.loopChargeDesc.text = gameStrings.ACTIVITY_SALE_LOOP_CHARGE_CHARGE if self.countType == COUNT_TYPE_CHARGE else gameStrings.ACTIVITY_SALE_LOOP_CHARGE_CONSUME

    def lableFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        gamelog.info('jbx:lableFunction', itemData, itemMc, itemData.needCount)
        itemMc.txtValue.text = str(int(itemData.needCount))
        itemMc.txtType.text = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_250 if self.countType == COUNT_TYPE_CHARGE else gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_250_1
        itemMc.rewardBtn.visible = itemData.rewardBtnVisible
        itemMc.rewardBtn.enabled = itemData.rewardBtnEnable
        itemMc.rewardBtn.label = itemData.rewardBtnLabel
        itemMc.rewardBtn.index = itemData.index
        itemMc.rewardBtn.isChooseReward = itemData.isChooseReward
        itemMc.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleRewardBtnClick, False, 0, True)
        for i in range(MAX_ITEM_CNT):
            slotMc = getattr(itemMc, 'item%d' % i)
            if i < len(itemData.itemList):
                slotMc.visible = True
                slotMc.slot.dragable = False
                slotMc.slot.setItemSlotData(itemData.itemList[i])
                ASUtils.setHitTestDisable(slotMc.usedFlag, True)
                slotMc.usedFlag.visible = itemData.satisfied
            else:
                slotMc.visible = False

    def getRewardCnt(self):
        myRewardInfo = self.getMyRewardInfo()
        if not myRewardInfo or len(myRewardInfo) < 6:
            return 0
        return myRewardInfo[5][2] - myRewardInfo[5][1]

    def refreshInfo(self):
        if not self.widget:
            return
        gamelog.info('jbx:refreshInfo')
        self.refreshAccmulateInfo()
        self.refreshLoopCharge()
        rewardCnt = self.getRewardCnt()
        self.widget.txtRemain.text = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_281 % rewardCnt
        self.uiAdapter.activitySale.refreshInfo()

    def refreshAccmulateInfo(self):
        gamelog.info('jbx:refreshAccmulateInfo')
        accmulateInfo = self.getAccmulateInfo()
        if accmulateInfo['infoList']:
            self.widget.accmulateCharge.visible = True
            if self.countType == COUNT_TYPE_CHARGE:
                self.widget.accmulateCharge.txtTotal.text = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_290 % accmulateInfo['chargedNum']
            else:
                self.widget.accmulateCharge.txtTotal.text = gameStrings.TEXT_ACTIVITYSALELOOPCHARGEPROXY_292 % accmulateInfo['chargedNum']
            self.widget.accmulateCharge.list.dataArray = accmulateInfo['infoList']
            self.widget.accmulateCharge.list.validateNow()
        else:
            self.widget.accmulateCharge.visible = False

    def handleOpenBoxBtnClick(self, *args):
        gamelog.info('jbx:handleOpenBoxBtnClick')
        self.uiAdapter.raffle.show(None, self.getRewardKeyVal()[1]['raffleItemSetInfo'])

    def handleChargeBtnClick(self, *args):
        gamelog.info('jbx:handleChargeBtnClick')
        self.uiAdapter.tianyuMall.onOpenChargeWindow()

    def pushChargeRewardInfo(self):
        gamelog.info('jbx:pushChargeRewardInfo')
        if not self.canOpen():
            return
        crId, crData = self.getRewardKeyVal()
        if not crId:
            return
        self.pushId = crData.get('pushId', 11203)
        if self.uiAdapter.pushMessage.msgInfoDict.has_key(self.pushId):
            return
        if not self.rewardKeyVal and self.getRewardCnt() <= 0:
            return
        if BigWorld.player().lv < SCD.data.get('activitySaleMinLv', 0):
            return
        canRaffle = crData.has_key('raffleItemSetInfo')
        if not canRaffle:
            myRewardInfo = self.getMyRewardInfo()
            if myRewardInfo:
                for index, rewardInfo in enumerate(crData.get('chargeCoins', [])):
                    if index not in myRewardInfo[3]:
                        break
                else:
                    return

        gameglobal.rds.ui.pushMessage.addPushMsg(self.pushId)
        gameglobal.rds.ui.pushMessage.setCallBack(self.pushId, {'click': self.onPushClick})

    def onPushClick(self):
        self.uiAdapter.activitySale.show(uiConst.ACTIVITY_SALE_TAB_LOOP_CHARGE)
        gameglobal.rds.ui.pushMessage.removePushMsg(self.pushId)

    def handleRewardBtnClick(self, *args):
        if not self.canOpen():
            return
        target = ASObject(args[3][0]).currentTarget
        index = target.index
        isChooseReward = target.isChooseReward
        gameglobal.rds.ui.chooseReward.show(index, isChooseReward)

    def addTimer(self):
        if not self.timer:
            self.timer = BigWorld.callback(1, self.timerFunc, -1)

    def timerFunc(self):
        if not self.widget:
            self.delTimer()
            return
        rewardVal = self.getRewardKeyVal()[1] if self.getRewardKeyVal() else {}
        endTime = utils.getTimeSecondFromStr(rewardVal.get('endTime', ''))
        left = 0
        if endTime >= utils.getNow():
            left = endTime - utils.getNow()
            self.widget.leftTimeTxt.text = utils.formatDurationShortVersion(left)
        else:
            if gameglobal.rds.ui.chooseReward.widget:
                gameglobal.rds.ui.chooseReward.hide()
            self.refreshInfo()

    def delTimer(self):
        self.timer and BigWorld.cancelCallback(self.timer)
        self.timer = None
