#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServiceLotteryProxy.o
import BigWorld
import utils
import time
import const
import clientUtils
import events
import gameglobal
import commNewServerActivity
from uiProxy import UIProxy
from guis import uiUtils
from gamestrings import gameStrings
from data import new_server_activity_data as NSAD
from data import lottery_data as LD
BG_IOCN_PATH = 'newServiceActivities/%d.dds'

class NewServiceLotteryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewServiceLotteryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.lotteryId = 0
        self.lotteryTime = 0
        self.callback = None

    def reset(self):
        self.lotteryId = 0
        self.lotteryTime = 0
        self.callback = None

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initUI(self):
        if not self.widget:
            return
        self.widget.mainMc.numberBtn.addEventListener(events.BUTTON_CLICK, self.handleNumberBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        lotteryId = NSAD.data.get('lotteryId', 0)
        todayIssueTime = commNewServerActivity.getLotteryTodayIssueTime(lotteryId)
        p = BigWorld.player()
        p.base.queryNSLotteryIssueData(lotteryId, todayIssueTime)

    def updateLeftTime(self):
        if not self.widget:
            self.stopCallback()
            return
        curTime = self.lotteryTime - utils.getNow()
        if curTime < 0:
            self.widget.mainMc.leftTime.text = gameStrings.NEW_SERVICE_LOTTERY_ALREADY_PRIZE
            self.stopCallback()
            return
        self.widget.mainMc.leftTime.text = utils.formatTimeStr(curTime)
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.callback = BigWorld.callback(1, self.updateLeftTime)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def updateLotteryData(self, lotteryId, lotteryTime, data):
        if not self.widget:
            return
        self.lotteryId = lotteryId
        self.lotteryTime = lotteryTime
        rankList = sorted(data.keys())
        if rankList:
            firstDict = data.get(rankList[0], {})
            winnerName = firstDict.values()
            szPlayerName = gameStrings.NEW_SERVICE_LOTTERY_PLAYER_NAME % (winnerName[0], winnerName[0])
        else:
            szPlayerName = gameStrings.NEW_SERVICE_LOTTERY_NONE_PLAYER
        self.widget.mainMc.todayDate.text = time.strftime('%Y/%m/%d', time.localtime(utils.getNow()))
        ldData = LD.data.get(lotteryId, {})
        lotteryTime = ldData.get('lotteryTime', '')
        lotteryTime = utils.getTimeSecondFromStr(lotteryTime)
        lotteryInterval = ldData.get('lotteryInterval', 0)
        prizeInfo = ldData.get('prizeInfo', [])
        issueTime = commNewServerActivity.getLotteryTodayIssueTime(self.lotteryId)
        lotteryIndex = commNewServerActivity.getLotteryIndexByNextTime(issueTime, lotteryTime, lotteryInterval)
        rankDesc, bonusIds, _, _ = prizeInfo[0]
        bonusId = bonusIds[lotteryIndex] if len(bonusIds) > lotteryIndex else 0
        iconPathList = ldData.get('iconPathList', [])
        iconId = iconPathList[lotteryIndex] if len(iconPathList) > lotteryIndex else 0
        iconPath = BG_IOCN_PATH % iconId
        self.widget.mainMc.bgIcon.fitSize = True
        self.widget.mainMc.bgIcon.loadImage(iconPath)
        itemBonus = clientUtils.genItemBonus(bonusId)
        itemId = itemBonus[0][0] if itemBonus else 0
        itemNum = itemBonus[0][1] if itemBonus else 0
        self.widget.mainMc.slot.fitSize = True
        self.widget.mainMc.slot.dragable = False
        self.widget.mainMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, count=itemNum))
        self.widget.mainMc.playerName.htmlText = szPlayerName
        lotteryStartTime = ldData.get('lotteryStartTime', '')
        strStart = time.strftime('%Y.%m.%d', time.localtime(utils.getTimeSecondFromStr(lotteryStartTime)))
        lotteryEndTime = ldData.get('lotteryEndTime', '')
        strEnd = time.strftime('%Y.%m.%d', time.localtime(utils.getTimeSecondFromStr(lotteryEndTime)))
        self.widget.mainMc.activityDate.text = '%s-%s' % (strStart, strEnd)
        szConsumeDesc = ''
        lotteryPriceByCharge = NSAD.data.get('lotteryPriceByCharge', {}).get(lotteryId, -1)
        if lotteryPriceByCharge != -1:
            szConsumeDesc += NSAD.data.get('lotteryPriceByChargeDesc', '') + '\n'
        lotteryPriceByConsume = NSAD.data.get('lotteryPriceByConsume', {}).get(lotteryId, -1)
        if lotteryPriceByConsume != -1:
            szConsumeDesc += NSAD.data.get('lotteryPriceByConsumeDesc', '') + '\n'
        lotteryPriceByActivation = NSAD.data.get('lotteryPriceByActivation', {}).get(lotteryId, -1)
        if lotteryPriceByActivation != -1:
            szConsumeDesc += NSAD.data.get('lotteryPriceByActivationDesc', '')
        self.widget.mainMc.consumeDesc.text = szConsumeDesc
        self.updateLeftTime()

    def handleNumberBtnClick(self, *args):
        p = BigWorld.player()
        nextIssueTime = commNewServerActivity.getNSLotteryNextTime(self.lotteryId)
        version = gameglobal.rds.ui.newServiceLotterySelf.getEndLotteryTimeVersion()
        gameglobal.rds.ui.newServiceLotterySelf.setLotteryId(self.lotteryId)
        gameglobal.rds.ui.newServiceLotterySelf.show(True)
        p.base.queryNSLotterySelfData(self.lotteryId, nextIssueTime, version)
