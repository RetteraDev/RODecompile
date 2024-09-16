#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/lotteryProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import uiUtils
import utils
import gametypes
import const
import events
import ui
from uiProxy import SlotDataProxy
from data import bonus_data as BD
from data import lottery_data as LD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
LOTTERY_NORMAL = 1
LOTTERY_AWARD = 2

class LotteryProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(LotteryProxy, self).__init__(uiAdapter)
        self.bindType = 'lottery'
        self.type = 'lottery'
        self.modelMap = {'getInitInfo': self.onGetInitInfo,
         'getHistoryInfo': self.onGetHistoryInfo,
         'confirm': self.onConfirm,
         'removeItem': self.onRemoveItem}
        self.mediator = None
        self.lotteryState = LOTTERY_NORMAL
        self.resPos = (const.CONT_NO_PAGE, const.CONT_NO_POS)
        self.lotteryId = 0
        self.issueTime = 0
        self.timer = None
        self.historyResult = {}
        uiAdapter.registerEscFunc(uiConst.WIDGET_LOTTERY, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_LOTTERY:
            self.mediator = mediator
            self.refreshAwardInfo(lotteryId=self.lotteryId)
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_LOTTERY)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def reset(self):
        self.lotteryState = LOTTERY_NORMAL
        self.removeItem(False)
        self.lotteryId = 0
        self.issueTime = 0
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def show(self, lotteryId):
        if not LD.data.has_key(lotteryId):
            return
        if not self.mediator:
            self.lotteryId = lotteryId
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_LOTTERY)

    def setHistoryInfo(self, data):
        lotteryId, issueTime, result = data
        self.historyResult[lotteryId, issueTime] = result.get(issueTime)
        if self.lotteryId == lotteryId:
            self.refreshHistoryInfo(issueTime)

    def onGetInitInfo(self, *arg):
        self.refreshInitInfo()

    def refreshInitInfo(self):
        if self.mediator:
            ld = LD.data.get(self.lotteryId)
            if not ld:
                return
            info = {}
            info['title'] = ld.get('lotteryTitle', '')
            info['lotteryHint'] = ld.get('lotteryHint', '')
            info['helpIconKey'] = ld.get('helpIconKey', 0)
            info['lotteryBgPath'] = 'lottery/%d.dds' % ld.get('lotteryBg', 0)
            curPeriodTime = self.getCurPeriodTime(self.lotteryId)
            info['awardTitle'] = gameStrings.TEXT_LOTTERYPROXY_96
            if curPeriodTime <= 0:
                info['leftTime'] = '--:--:--'
                info['curPeriod'] = gameStrings.TEXT_LOTTERYPROXY_99
            else:
                info['leftTime'] = ''
                info['curPeriod'] = gameStrings.TEXT_LOTTERYPROXY_102 % utils.formatDate(curPeriodTime, delimiter='/')
            prizeInfo = ld.get('prizeInfo', [])
            tabList = []
            for prize in prizeInfo:
                tabInfo = {}
                tabInfo['label'] = prize[0]
                tabList.append(tabInfo)

            tabList.reverse()
            info['tabList'] = tabList
            periodList = []
            lotteryTime = ld.get('lotteryTime')
            lotteryInterval = ld.get('lotteryInterval')
            if lotteryTime and lotteryInterval:
                lotteryTime = utils.getTimeSecondFromStr(lotteryTime)
                lotteryEndTime = ld.get('lotteryEndTime')
                now = int(BigWorld.player().getServerTime())
                if lotteryEndTime:
                    lotteryEndTime = utils.getTimeSecondFromStr(lotteryEndTime)
                else:
                    lotteryEndTime = now
                prizeInterval = ld.get('prizeInterval', 0)
                prizeInfoLen = len(prizeInfo)
                if prizeInfoLen > 0:
                    totalPrizeTime = (prizeInfoLen - 1) * prizeInterval
                else:
                    totalPrizeTime = 0
                time = lotteryTime
                while time + totalPrizeTime < now and time + totalPrizeTime <= lotteryEndTime:
                    periodInfo = {}
                    periodInfo['label'] = utils.formatDate(time, delimiter='/')
                    periodInfo['issueTime'] = time
                    periodList.append(periodInfo)
                    time += lotteryInterval

                periodList.reverse()
                retainLotteryIssueNum = SCD.data.get('retainLotteryIssueNum', gametypes.RETAIN_HISTORY_ISSUES)
                if len(periodList) > retainLotteryIssueNum:
                    periodList = periodList[:retainLotteryIssueNum]
            info['periodList'] = periodList
            info['hasHistory'] = len(periodList) > 0
            self.mediator.Invoke('refreshInitInfo', uiUtils.dict2GfxDict(info, True))
            self.stopTimer()
            if curPeriodTime > 0:
                self.updateTime()

    def updateTime(self):
        if self.mediator:
            nextPrizeTime, prizeName = self.getNextPrizeTime(self.lotteryId)
            info = {}
            if nextPrizeTime <= 0:
                info['awardTitle'] = gameStrings.TEXT_LOTTERYPROXY_96
                info['leftTime'] = '--:--:--'
                BigWorld.callback(1, self.refreshInitInfo)
            else:
                leftTime = nextPrizeTime - int(BigWorld.player().getServerTime())
                if leftTime <= 0:
                    BigWorld.callback(1, self.refreshInitInfo)
                    leftTime = 0
                if prizeName != '':
                    info['awardTitle'] = gameStrings.TEXT_LOTTERYPROXY_169 % prizeName
                else:
                    info['awardTitle'] = gameStrings.TEXT_LOTTERYPROXY_96
                info['leftTime'] = utils.formatTimeStr(leftTime, 'h:m:s', True, 2, 2, 2)
            self.mediator.Invoke('updateTime', uiUtils.dict2GfxDict(info, True))
            if nextPrizeTime > 0:
                self.timer = BigWorld.callback(1, self.updateTime)

    def getCurPeriodTime(self, lotteryId):
        now = int(BigWorld.player().getServerTime())
        ld = LD.data.get(self.lotteryId, {})
        lotteryEndTime = ld.get('lotteryEndTime')
        if lotteryEndTime:
            lotteryEndTime = utils.getTimeSecondFromStr(lotteryEndTime)
            if lotteryEndTime < now:
                return 0
        lotteryTime = ld.get('lotteryTime')
        if not lotteryTime:
            return 0
        lotteryInterval = ld.get('lotteryInterval')
        if not lotteryInterval:
            return 0
        lotteryTime = utils.getTimeSecondFromStr(lotteryTime)
        nextTime = utils.getLotteryNextTime(now, lotteryTime, lotteryInterval)
        if nextTime == lotteryTime:
            return nextTime
        curTime = nextTime - lotteryInterval
        prizeInterval = ld.get('prizeInterval', 0)
        prizeInfoLen = len(ld.get('prizeInfo', []))
        if prizeInfoLen > 0:
            totalPrizeTime = (prizeInfoLen - 1) * prizeInterval
        else:
            totalPrizeTime = 0
        if now <= curTime + totalPrizeTime:
            return curTime
        return nextTime

    def getNextPrizeTime(self, lotteryId):
        now = int(BigWorld.player().getServerTime())
        ld = LD.data.get(self.lotteryId, {})
        lotteryEndTime = ld.get('lotteryEndTime')
        if lotteryEndTime:
            lotteryEndTime = utils.getTimeSecondFromStr(lotteryEndTime)
            if lotteryEndTime < now:
                return (0, '')
        lotteryTime = ld.get('lotteryTime')
        if not lotteryTime:
            return (0, '')
        lotteryInterval = ld.get('lotteryInterval')
        if not lotteryInterval:
            return (0, '')
        prizeInterval = ld.get('prizeInterval', 0)
        prizeInfo = ld.get('prizeInfo', [])
        prizeInfoLen = len(prizeInfo)
        lotteryTime = utils.getTimeSecondFromStr(lotteryTime)
        nextTime = utils.getLotteryNextTime(now, lotteryTime, lotteryInterval)
        if nextTime == lotteryTime:
            return (nextTime, prizeInfo[0][0])
        curTime = nextTime - lotteryInterval
        for i in xrange(prizeInfoLen):
            if now <= curTime:
                return (curTime, prizeInfo[i][0])
            curTime += prizeInterval

        return (nextTime, prizeInfo[0][0])

    def onGetHistoryInfo(self, *arg):
        issueTime = int(arg[3][0].GetNumber())
        historyTab = int(arg[3][1].GetNumber())
        self.historyTab = len(LD.data.get(self.lotteryId, {}).get('prizeInfo', [])) - historyTab
        if issueTime == 0:
            self.refreshHistoryInfo(self.issueTime)
            return
        self.issueTime = issueTime
        self.refreshHistoryInfo(self.issueTime)
        BigWorld.player().cell.queryLotteryResult(self.lotteryId, self.issueTime)

    def addAwardInfo(self, info, bonusId):
        fixedBonus = BD.data.get(bonusId, {}).get('fixedBonus', [])
        fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
        info['awardType'] = 'item'
        bonusList = []
        for bType, itemId, itemNum in fixedBonus:
            bonusInfo = {}
            if bType != gametypes.BONUS_TYPE_ITEM:
                info['awardType'] = 'other'
                if bType == gametypes.BONUS_TYPE_MONEY:
                    bonusInfo['bonusType'] = 'bindCash'
                elif bType == gametypes.BONUS_TYPE_MALL_CASH:
                    bonusInfo['bonusType'] = 'tianQuan'
                else:
                    break
                bonusInfo['value'] = format(itemNum, ',')
                info['bonusInfo'] = bonusInfo
                break
            bonusInfo = uiUtils.getGfxItemById(itemId, itemNum)
            bonusList.append(bonusInfo)

        info['bonusList'] = bonusList

    def refreshHistoryInfo(self, issueTime):
        if self.issueTime != issueTime:
            return
        if self.mediator:
            info = {}
            prizeInfo = LD.data.get(self.lotteryId, {}).get('prizeInfo', [])
            if self.historyTab > len(prizeInfo):
                bonusId = 0
            else:
                bonusId = prizeInfo[self.historyTab - 1][1]
            self.addAwardInfo(info, bonusId)
            if info.has_key('bonusInfo'):
                info['bonusInfo']['value'] = gameStrings.TEXT_LOTTERYPROXY_303 % info['bonusInfo']['value']
            result = self.historyResult.get((self.lotteryId, self.issueTime))
            if result:
                result = result.get(self.historyTab)
            playerList = []
            if result:
                for i in xrange(len(result)):
                    playerInfo = {}
                    if result[i][1] != '':
                        playerInfo['playerName'] = result[i][1]
                        playerInfo['getFlag'] = 'get'
                    else:
                        playerInfo['playerName'] = utils.getDisplayLotteryNo(result[i][0])
                        playerInfo['getFlag'] = 'no'
                    playerInfo['bgVisible'] = i % 2 == 0
                    playerList.append(playerInfo)

            info['playerList'] = playerList
            self.mediator.Invoke('refreshHistoryInfo', uiUtils.dict2GfxDict(info, True))

    def refreshAwardInfo(self, flag = 0, lotteryId = 0, rank = 0):
        if self.mediator:
            info = {}
            if self.lotteryState == LOTTERY_NORMAL:
                info['awardType'] = 'normal'
                srcItem = BigWorld.player().inv.getQuickVal(self.resPos[0], self.resPos[1])
                if srcItem:
                    info['itemInfo'] = uiUtils.getGfxItem(srcItem, location=const.ITEM_IN_BAG)
                    if flag == gametypes.LOTTERY_CHECK_INVALID:
                        awradState = uiUtils.getTextFromGMD(GMDD.data.LOTTERY_CHECK_INVALID_HINT, '')
                    elif flag == gametypes.LOTTERY_CHECK_NO_PRIZE:
                        awradState = uiUtils.getTextFromGMD(GMDD.data.LOTTERY_CHECK_NO_PRIZE_HINT, '')
                    elif flag == gametypes.LOTTERY_CHECK_NOT_DRAW:
                        awradState = uiUtils.getTextFromGMD(GMDD.data.LOTTERY_CHECK_NOT_DRAW_HINT, '')
                    elif flag == gametypes.LOTTERY_CHECK_EXPIRED:
                        awradState = uiUtils.getTextFromGMD(GMDD.data.LOTTERY_CHECK_EXPIRED_HINT, '')
                    elif flag == gametypes.LOTTERY_CHECK_WIN:
                        prizeInfo = LD.data.get(lotteryId, {}).get('prizeInfo', [])
                        if rank > len(prizeInfo):
                            awardStr = ''
                        else:
                            awardStr = prizeInfo[rank - 1][0]
                        awradState = uiUtils.getTextFromGMD(GMDD.data.LOTTERY_CHECK_WIN_HINT, '%s') % awardStr
                    elif flag == gametypes.LOTTERY_CHECK_REWARDED:
                        awradState = uiUtils.getTextFromGMD(GMDD.data.LOTTERY_CHECK_REWARDED_HINT, '')
                    else:
                        awradState = ''
                else:
                    info['itemInfo'] = {}
                    awradState = uiUtils.getTextFromGMD(GMDD.data.LOTTERY_NO_ITEM_HINT, '')
                info['awradState'] = awradState
                info['getAwardHint'] = LD.data.get(lotteryId, {}).get('getAwardHint', '')
                info['btnEnabled'] = flag == gametypes.LOTTERY_CHECK_WIN
            else:
                prizeInfo = LD.data.get(lotteryId, {}).get('prizeInfo', [])
                if rank > len(prizeInfo):
                    bonusId = 0
                else:
                    bonusId = prizeInfo[rank - 1][1]
                self.addAwardInfo(info, bonusId)
                self.lotteryState = LOTTERY_NORMAL
            self.mediator.Invoke('refreshAwardInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(self.resPos[0], self.resPos[1])
        if srcItem:
            p.cell.getRewardByLottery(self.resPos[0], self.resPos[1])

    def onRemoveItem(self, *arg):
        if self.lotteryState != LOTTERY_NORMAL:
            return
        self.removeItem(True)

    def getSlotID(self, key):
        return (0, 0)

    def setItem(self, srcBar, srcSlot):
        if self.lotteryState != LOTTERY_NORMAL:
            return
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(srcBar, srcSlot)
        if srcItem.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        self.removeItem(False)
        self.resPos = (srcBar, srcSlot)
        gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
        p.cell.queryLottery(self.resPos[0], self.resPos[1])

    def removeItem(self, needRefresh):
        if self.resPos[0] != const.CONT_NO_PAGE:
            page, pos = self.resPos
            self.resPos = (const.CONT_NO_PAGE, const.CONT_NO_POS)
            gameglobal.rds.ui.inventory.updateSlotState(page, pos)
        if needRefresh:
            self.refreshAwardInfo(lotteryId=self.lotteryId)

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if item.isLottery() and item.getLotteryId() == self.lotteryId:
                return (page, pos) == self.resPos
            else:
                return True
        else:
            return False

    @ui.uiEvent(uiConst.WIDGET_LOTTERY, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            self.setInventoryItem(nPage, nItem)
            return

    def setInventoryItem(self, nPageSrc, nItemSrc):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if srcItem:
            if srcItem.isLottery():
                self.setItem(nPageSrc, nItemSrc)

    def onGetRewardByLottery(self, page, pos, lotteryId, issueTime, nuid, flag, rank):
        if self.resPos != (page, pos):
            return
        if flag == gametypes.LOTTERY_CHECK_WIN:
            self.lotteryState = LOTTERY_AWARD
            self.refreshAwardInfo(lotteryId=lotteryId, rank=rank)
            BigWorld.player().showGameMsg(GMDD.data.LOTTERY_GET_AWARD_SUCCESS, ())
        else:
            self.lotteryState = LOTTERY_NORMAL
            self.refreshAwardInfo(flag=flag, lotteryId=lotteryId)

    def onQueryLottery(self, page, pos, lotteryId, issueTime, nuid, flag, rank):
        if self.resPos != (page, pos):
            return
        self.refreshAwardInfo(flag=flag, lotteryId=lotteryId, rank=rank)
