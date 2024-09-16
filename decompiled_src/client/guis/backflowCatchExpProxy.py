#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/backflowCatchExpProxy.o
import BigWorld
import utils
import events
import uiConst
import clientUtils
import const
from uiProxy import UIProxy
from asObject import ASObject
from guis import uiUtils
from gameStrings import gameStrings
from asObject import ASUtils
from asObject import RedPotManager
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import flowback_group_target_data as FGTD
from cdata import flowback_group_target_reward_data as FGTRD
from cdata import flowback_group_data as FGD
REWARD_BONUSID_NUM = 6

class BackflowCatchExpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BackflowCatchExpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.callback = None
        self.endTime = 0

    def reset(self):
        self.callback = None
        self.endTime = 0

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.widget.catchExpPanel.getPointRewardBtn.addEventListener(events.MOUSE_CLICK, self.handleGetPointRewardBtnClick, False, 0, True)
        self.widget.catchExpPanel.scrollWndList.itemHeight = 80
        self.widget.catchExpPanel.scrollWndList.itemRenderer = 'BackflowCatchExp_goalItem'
        self.widget.catchExpPanel.scrollWndList.dataArray = []
        self.widget.catchExpPanel.scrollWndList.lableFunction = self.itemFunction
        self.widget.catchExpPanel.descText1.text = SCD.data.get('backflowDesc', '')
        self.widget.catchExpPanel.descT2.text = SCD.data.get('backflowFinishTargetPointDesc', '')

    def handleGetPointRewardBtnClick(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        p.cell.receiveFlowbackGroupTargetPointReward(True)

    def handleGoalBtnClick(self, *args):
        e = ASObject(args[3][0])
        goalBtn = e.currentTarget
        linkText = goalBtn.parent.linkText
        goalBtn.linkText = linkText

    def handleGetRewardBtnClick(self, *args):
        e = ASObject(args[3][0])
        targetId = e.currentTarget.parent.targetId
        if targetId:
            p = BigWorld.player()
            p.cell.receiveFlowbackTargetReward(targetId, True)

    def refreshInfo(self):
        if not self.widget:
            return
        self.endTime = self.getCatchExpEndTime()
        self.updateLeftTime()
        self.updateBar()
        self.updateTargetRewards()
        self.updateTargetTask()

    def updateIconAndVal(self, cashIcon, valText, value, bonusType):
        cashIcon.visible = True if value else False
        valText.visible = True if value else False
        cashIcon.bonusType = bonusType
        valText.text = value

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.targetId = itemData.targetId
        itemMc.linkText = FGTD.data.get(itemData.targetId, {}).get('linkText', '')
        itemMc.itemTitleT.text = itemData.targetTitle
        itemMc.itemDescT.text = itemData.targetDesc
        self.updateIconAndVal(itemMc.cashIcon0, itemMc.cashValT0, itemData.rewardExp, 'exp')
        self.updateIconAndVal(itemMc.cashIcon1, itemMc.cashValT1, itemData.rewardBindCash, 'bindCash')
        self.updateIconAndVal(itemMc.cashIcon2, itemMc.cashValT2, itemData.targetPoint, 'huiliu')
        itemBonus = clientUtils.genItemBonus(itemData.bonusId)
        itemId, num = itemBonus[0] if itemBonus else (0, 0)
        if itemId:
            itemMc.slot.visible = True
            itemInfo = uiUtils.getGfxItemById(itemId, num)
            itemMc.slot.fitSize = True
            itemMc.slot.dragable = False
            itemMc.slot.setItemSlotData(itemInfo)
        else:
            itemMc.slot.visible = False
        state = itemData.rewardState
        if state == const.FLOWBACK_STATE_NO_COMPLETE:
            itemMc.goalBtn.visible = True
            itemMc.goalBtn.label = gameStrings.BACK_FLOW_TARGET_LABEL_GO_FINISH if itemMc.linkText else gameStrings.BACK_FLOW_TARGET_LABEL_WAIT_FINISH
            itemMc.goalBtn.enabled = True if itemMc.linkText else False
            itemMc.finishedPic.visible = False
            itemMc.getRewardBtn.visible = False
            itemMc.goalBtn.addEventListener(events.BUTTON_CLICK, self.handleGoalBtnClick, False, 0, True)
        elif state == const.FLOWBACK_STATE_COMPLETE_NO_REWARD:
            itemMc.goalBtn.visible = False
            itemMc.finishedPic.visible = False
            itemMc.getRewardBtn.visible = True
            itemMc.getRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleGetRewardBtnClick, False, 0, True)
        elif state == const.FLOWBACK_STATE_COMPLETE_AND_ALREADY_REWARD:
            itemMc.finishedPic.visible = True
            itemMc.goalBtn.visible = False
            itemMc.getRewardBtn.visible = False

    def updateLeftTime(self):
        if not self.widget:
            self.stopCallback()
            return
        curTime = utils.getNow()
        leftTime = max(0, self.endTime - curTime)
        day = max(0, utils.formatDurationLeftDay(leftTime))
        hour = max(0, utils.formatDurationLeftHour(leftTime))
        minute = max(0, utils.formatDurationLeftMin(leftTime))
        srtTime = gameStrings.BACK_FLOW_LEFT_TIME % (day, hour, minute)
        self.widget.catchExpPanel.leftTimeText.htmlText = gameStrings.BACK_FLOW_LEFT_TIME_TITLE % uiUtils.toHtml(srtTime, '#d34024')
        if leftTime <= 0:
            self.stopCallback()
            return
        self.callback = BigWorld.callback(1, self.updateLeftTime)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def updateBar(self):
        p = BigWorld.player()
        totalExp = p.flowbackGroupBonus.totalExp
        restExp = p.flowbackGroupBonus.restExp
        catchExpPanel = self.widget.catchExpPanel
        catchExpPanel.expBar.maxValue = totalExp
        catchExpPanel.expBar.currentValue = restExp
        catchExpPanel.expIcon.bonusType = 'exp'
        catchExpPanel.expValT.text = restExp
        totalBindCash = p.flowbackGroupBonus.totalBindCash
        restBindCash = p.flowbackGroupBonus.restBindCash
        catchExpPanel.bincCashBar.maxValue = totalBindCash
        catchExpPanel.bincCashBar.currentValue = restBindCash
        catchExpPanel.bindCashIcon.bonusType = 'bindCash'
        catchExpPanel.bindCashValT.text = restBindCash

    def updateTargetRewards(self):
        catchExpPanel = self.widget.catchExpPanel
        p = BigWorld.player()
        targetPoints = p.flowbackGroupBonus.targetPoints
        flowbackGroupType = p.flowbackGroupBonus.flowbackGroupType
        targetPointsRewards = p.flowbackGroupBonus.targetPointsRewards
        groupData = self.getGroupTargetRewardData(flowbackGroupType)
        bonusIds = groupData.get('bonusIds', ())
        points = groupData.get('points', ())
        percents = groupData.get('percents', ())
        catchExpPanel.activeValT.text = targetPoints
        for i in range(REWARD_BONUSID_NUM):
            rewardItem = catchExpPanel.getChildByName('rewardItem%d' % i)
            pointPic = catchExpPanel.fillCashMc.getChildByName('pointPic%d' % i)
            pointIcon = catchExpPanel.fillCashMc.getChildByName('pointIcon%d' % i)
            pointValT = catchExpPanel.fillCashMc.getChildByName('pointValT%d' % i)
            arrow = catchExpPanel.fillCashMc.getChildByName('arrow%d' % i)
            pointIcon.bonusType = 'huiliu'
            bonusId = bonusIds[i] if i < len(bonusIds) else 0
            itemBonus = clientUtils.genItemBonus(bonusId)
            itemId, num = itemBonus[0] if itemBonus else (0, 0)
            itemInfo = uiUtils.getGfxItemById(itemId, num)
            rewardItem.slot.fitSize = True
            rewardItem.slot.dragable = False
            rewardItem.slot.setItemSlotData(itemInfo)
            rewardItem.getedPic.visible = False
            ASUtils.setHitTestDisable(rewardItem.getedPic, True)
            rewardItem.sfx.visible = False
            ASUtils.setHitTestDisable(rewardItem.sfx, True)
            rewardItem.slot.setSlotState(uiConst.ITEM_NORMAL)
            if bonusId in targetPointsRewards:
                rewardItem.getedPic.visible = True
                rewardItem.slot.setSlotState(uiConst.ITEM_GRAY)
            else:
                iPoint = points[i] if i < len(points) else 0
                rewardItem.sfx.visible = True if targetPoints >= iPoint else False
            point = points[i] if i < len(points) else 0
            pointValT.text = point
            if targetPoints < point:
                pointPic.gotoAndStop('disable')
            else:
                pointPic.gotoAndStop('up')
            tipMsg = gameStrings.BACK_FLOW_CATCH_UP_POINT_PERCENT_TIP % percents[i]
            TipManager.addTip(pointPic, tipMsg)
            if targetPoints >= points[i]:
                arrow.gotoAndStop('dislight')
            elif i > 0 and targetPoints > points[i - 1] or i == 0 and targetPoints > 0:
                arrow.gotoAndStop('half')
            else:
                arrow.gotoAndStop('light')

        getedRewards = len(targetPointsRewards)
        nextPoint = 0
        if getedRewards + 1 <= len(points):
            nextPoint = points[getedRewards]
        catchExpPanel.getPointRewardBtn.enabled = True if targetPoints and nextPoint and targetPoints >= nextPoint else False

    def getGroupTargetRewardData(self, flowbackGroupType):
        for v in FGTRD.data:
            dictInfo = FGTRD.data[v]
            if dictInfo.get('type', 0) == flowbackGroupType:
                return dictInfo

        return {}

    def updateTargetTask(self):
        p = BigWorld.player()
        targetsStateInfo = p.flowbackGroupBonus.targetsStateInfo
        targetList = self.getTargetList(targetsStateInfo)
        itemList = []
        for i, targetId in enumerate(targetList):
            expFormula = FGTD.data.get(targetId, {}).get('expFormula', 0)
            bindCashFormula = FGTD.data.get(targetId, {}).get('bindCashFormula', 0)
            targetPoint = FGTD.data.get(targetId, {}).get('targetPoint', 0)
            bonusId = FGTD.data.get(targetId, {}).get('bonusId', 0)
            targetTitle = FGTD.data.get(targetId, {}).get('targetTitle', '')
            targetDesc = FGTD.data.get(targetId, {}).get('targetDesc', '')
            ctx = {'lv': p.lv}
            rewardExp = 0
            rewardBindCash = 0
            if expFormula:
                rewardExp = int(expFormula(ctx))
            if bindCashFormula:
                rewardBindCash = int(bindCashFormula(ctx))
            itemInfo = {}
            itemInfo['index'] = i
            itemInfo['targetId'] = targetId
            itemInfo['targetTitle'] = targetTitle
            itemInfo['targetDesc'] = targetDesc
            itemInfo['rewardExp'] = rewardExp
            itemInfo['rewardBindCash'] = rewardBindCash
            itemInfo['bonusId'] = bonusId
            itemInfo['targetPoint'] = targetPoint
            itemInfo['rewardState'] = targetsStateInfo[targetId]
            itemList.append(itemInfo)

        self.widget.catchExpPanel.scrollWndList.dataArray = itemList
        self.widget.catchExpPanel.scrollWndList.validateNow()

    def getTargetList(self, targetsStateInfo):
        finishList = []
        canGetRewardList = []
        noFinishList = []
        for i, targetId in enumerate(sorted(targetsStateInfo.keys(), reverse=True)):
            rewardState = targetsStateInfo[targetId]
            if rewardState == const.FLOWBACK_STATE_COMPLETE_AND_ALREADY_REWARD:
                finishList.append(targetId)
            elif rewardState == const.FLOWBACK_STATE_COMPLETE_NO_REWARD:
                canGetRewardList.append(targetId)
            else:
                noFinishList.append(targetId)

        return canGetRewardList + noFinishList + finishList

    def getCatchExpEndTime(self):
        p = BigWorld.player()
        days = FGD.data.get(p.flowbackGroupBonus.flowbackGroupType, {}).get('duration', 0)
        endTime = p.flowbackGroupBonus.startTime + days * const.TIME_INTERVAL_DAY
        return endTime

    def checkRedPoint(self):
        p = BigWorld.player()
        flowbackGroupType = p.flowbackGroupBonus.flowbackGroupType
        targetPoints = p.flowbackGroupBonus.targetPoints
        targetPointsRewards = p.flowbackGroupBonus.targetPointsRewards
        groupData = self.getGroupTargetRewardData(flowbackGroupType)
        points = groupData.get('points', ())
        getedRewards = len(targetPointsRewards)
        nextPoint = 0
        if getedRewards + 1 <= len(points):
            nextPoint = points[getedRewards]
        isRedPot1 = True if targetPoints and nextPoint and targetPoints >= nextPoint else False
        targetsStateInfo = p.flowbackGroupBonus.targetsStateInfo
        isRedPot2 = False
        for i, targetId in enumerate(targetsStateInfo):
            state = targetsStateInfo[targetId]
            if state == const.FLOWBACK_STATE_COMPLETE_NO_REWARD:
                isRedPot2 = True
                break

        return (isRedPot1 or isRedPot2) and not self.checkTimeEnd()

    def updateRedPot(self):
        RedPotManager.updateRedPot(uiConst.BACK_FLOW_CATCH_EXP_RED_POT)

    def checkTimeEnd(self):
        endTime = self.getCatchExpEndTime()
        curTime = utils.getNow()
        leftTime = endTime - curTime
        if leftTime <= 0:
            return True
        return False
