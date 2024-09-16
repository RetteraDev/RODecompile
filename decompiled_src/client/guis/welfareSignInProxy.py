#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareSignInProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gamelog
import clientUtils
import utils
import formula
from gamestrings import gameStrings
from asObject import ASObject
from guis.asObject import TipManager
from uiProxy import UIProxy
from guis import uiUtils
from asObject import ASUtils
from data import activity_signin_bonus_data as ASBD
from cdata import activity_resignin_config_data as ARCD
from data import activity_signin_type_data as ASTD
from data import sys_config_data as SCD
from data import bonus_data as BD
from data import bonus_set_data as BSD
ITEMS_NUM_PER_PAGE = 7

class WelfareSignInProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareSignInProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.widget = None
        self.activityId = -1
        self.currSignTimes = 0
        self.accuBonusList = []
        self.currPage = 1
        self.specialRewards = []
        self.canResignCnt = 0

    def initSignIn(self, widget, activityId):
        self.widget = ASObject(widget)
        self.activityId = int(activityId.GetNumber())
        self.initUI()
        self.refreshInfo()

    def initUI(self):
        if not self.widget:
            return
        data = ASTD.data.get(self.activityId, {})
        frameName = data.get('frameName')
        self.widget.gotoAndStop(frameName)
        self.widget.dailyRewardDesc.text = data.get('dailyRewardDesc', gameStrings.NEW_SIGNIN_DAILY_REWARD_DESC)
        self.widget.signTimesDesc.text = data.get('signTimesDesc', gameStrings.NEW_SIGNIN_SIGN_TIMES_DESC)
        self.widget.specialRewardDesc.text = data.get('specialRewardDesc', gameStrings.NEW_SIGNIN_SPECIAL_REWARD_DESC)
        self.widget.leftTimeDesc.text = data.get('leftTimeDesc', gameStrings.NEW_SIGNIN_LEFT_TIME_DESC)
        self.widget.confirmBtn.label = data.get('signInDesc', gameStrings.NEW_SIGNIN_SIGN_DESC)
        self.widget.reSignBtn.label = data.get('reSignInDesc', gameStrings.NEW_SIGNIN_RESIGN_DESC)
        self.widget.surpriseDay.desc.text = data.get('surpriseDesc')
        self.widget.pageStepper.prevBtn.addEventListener(events.MOUSE_CLICK, self.handleClickPreBtn, False, 0, True)
        self.widget.pageStepper.nextBtn.addEventListener(events.MOUSE_CLICK, self.handleClickNextBtn, False, 0, True)
        self.widget.pageStepper.numInput.enabled = False
        self.widget.pageStepper.numInput.textField.restrict = '0-9'
        self.widget.pageStepper.maxCount = len(data.get('accuBonus', {})) / ITEMS_NUM_PER_PAGE + 1
        self.widget.pageStepper.numInput.textField.text = 1
        self.refreshResignTip()
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.reSignBtn.addEventListener(events.BUTTON_CLICK, self.handleReSignBtnClick, False, 0, True)
        signStartDay = data.get('startDay', 20150801)
        activityCnt = data.get('duration', 21)
        toDaySec = uiUtils._getSec(signStartDay) + (activityCnt - 1) * uiConst.ONE_DAT_TIME
        signEndDay = formula.toYearDesc(toDaySec, 1)
        self.widget.leftTime.text = signEndDay
        self.refreshInfo()

    def refreshResignTip(self):
        data = ASTD.data.get(self.activityId, {})
        newSignInInfo = getattr(BigWorld.player(), 'newSignInInfo', {})
        dayIndex = self._getDayIndex()
        resign = ARCD.data.get(self.activityId, {})
        MaxResignCnt = resign.get('reSignInCnt', 0)
        hasSignedToday = self.hasSignedToday()
        if hasSignedToday:
            notResignCnt = dayIndex + 1 - self.currSignTimes
        else:
            notResignCnt = dayIndex - self.currSignTimes
        if notResignCnt < 0:
            notResignCnt = 0
        resignCnt = getattr(newSignInInfo.get(self.activityId, {}), 'resignCnt', 0)
        self.canResignCnt = min(notResignCnt, MaxResignCnt - resignCnt)
        TipManager.addTip(self.widget.reSignBtn, data.get('reSignTip', gameStrings.NEW_SIGNIN_RESIGN_TIP) % (notResignCnt, self.canResignCnt))

    def unRegistSignIn(self):
        self.widget = None
        self.reset()

    def refreshInfo(self):
        if not self.widget:
            return
        data = ASTD.data.get(self.activityId, {})
        signInfo = BigWorld.player().newSignInInfo
        signDates = getattr(signInfo.get(self.activityId, {}), 'dates', [])
        specialTimes = data.get('specialTimes', (5, 10))
        isStateChange = False
        if self.currSignTimes == len(signDates) - 1 and len(signDates) in specialTimes:
            isStateChange = True
        self.currSignTimes = len(signDates)
        self.widget.signTimes.text = gameStrings.NEW_SIGNIN_SIGN_TIMES % self.currSignTimes
        currentState = 0
        for state, times in enumerate(specialTimes):
            if self.currSignTimes < times:
                currentState = state
                break
            elif self.currSignTimes >= specialTimes[-1]:
                currentState = len(specialTimes)

        if isStateChange:
            self.widget.flowerMC.gotoAndPlay('transition%d' % (currentState - 1))
            if currentState == 1:
                target = self.widget.flowerMC.flower1
            elif currentState == 2:
                target = self.widget.flowerMC.flower2
            ASUtils.callbackAtFrame(target, 35, self.afterChangeState, currentState)
        else:
            self.widget.flowerMC.gotoAndPlay('state%d' % currentState)
        uniqueBonus = ASTD.data.get(self.activityId, {}).get('uniqueBonus', ())
        totalDays = uniqueBonus[0]
        self.widget.finalRewardDesc.text = data.get('finalRewardDesc', gameStrings.NEW_SIGNIN_FINAL_REWARD_DESC) % totalDays
        receivedUniqueBonus = self.currSignTimes >= totalDays
        bonusId = uniqueBonus[1]
        bonusList = clientUtils.genItemBonus(bonusId)
        if len(bonusList) == 1:
            bonus = bonusList[0]
            self.widget.reward.gotoAndStop('one')
            itemId = bonus[0]
            itemCount = bonus[1]
            itemMc = self.widget.reward.item
            itemMc.slot.itemId = itemId
            itemMc.slot.dragable = False
            itemMc.yes.visible = receivedUniqueBonus
            itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
        elif len(bonusList) == 2:
            self.widget.reward.gotoAndStop('two')
            for i, bonus in enumerate(bonusList):
                itemId = bonus[0]
                itemCount = bonus[1]
                itemMc = getattr(self.widget.reward, 'item%d' % i)
                itemMc.slot.itemId = itemId
                itemMc.slot.dragable = False
                itemMc.yes.visible = receivedUniqueBonus
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))

        if self.currSignTimes:
            accuBonus = data.get('accuBonus')
            self.accuBonusList = []
            keyList = sorted(accuBonus.keys())
            timesIndex = len(keyList) - 1
            for i, key in enumerate(keyList):
                if self.currSignTimes < key:
                    timesIndex = i
                    break

            self.currPage = timesIndex / ITEMS_NUM_PER_PAGE + 1
        else:
            self.currPage = 1
        self.refreshDailyReward()
        exactDayBonusList = {}
        startDay = data.get('startDay', 20180816)
        exactSignDay = utils.diffYearMonthDayInt(utils.getYearMonthDayInt(), startDay) + 1
        for key in ASBD.data:
            if key[0] == self.activityId:
                days = key[1]
                if exactSignDay == days:
                    itemMc = self.widget.surpriseDay
                    itemMc.desc.text = data.get('surpriseDesc')
                    TipManager.addTip(itemMc, data.get('surpriseTip', gameStrings.NEW_SIGNIN_SURPRISE_TIP))
                    bonusId = ASBD.data[key].get('randomBonus', 0)
                    displayItems = BD.data.get(bonusId, {}).get('displayItems', ())
                    if displayItems:
                        itemData = {}
                        itemData['bonusId'] = displayItems[0][0]
                        itemData['minBonusNum'] = displayItems[0][1]
                    else:
                        itemBonus = BD.data.get(bonusId, {}).get('bonusIds', [])[0]
                        itemData = BSD.data.get(itemBonus, {})[0]
                    if itemData:
                        itemId = itemData.get('bonusId', 0)
                        itemCount = itemData.get('minBonusNum', 0)
                        itemMc.slot.itemId = itemId
                        itemMc.slot.dragable = False
                        itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
                if ASBD.data[key].has_key('exactDayBonus'):
                    exactDayBonusList[days] = ASBD.data[key]['exactDayDispalyItemId']

        dayList = sorted(exactDayBonusList.keys())
        nextExactDay = 0
        for exactDay in dayList:
            if exactSignDay <= exactDay:
                nextExactDay = exactDay
                break

        if not nextExactDay:
            nextExactDay = dayList[-1]
        receivedExactDayBonus = getattr(signInfo.get(self.activityId, {}), 'exactDayBonus', [])
        itemMc = self.widget.appointedDay
        bonusId = exactDayBonusList[nextExactDay]
        itemMc.slot.itemId = bonusId
        itemMc.slot.dragable = False
        itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(bonusId))
        itemMc.yes.visible = nextExactDay in receivedExactDayBonus
        toDaySec = uiUtils._getSec(startDay) + (nextExactDay - 1) * uiConst.ONE_DAT_TIME
        signEndDay = formula.toYearDesc(toDaySec, 1)
        itemMc.desc.text = signEndDay[6:]
        self.refreshResignTip()

    def afterChangeState(self, *args):
        state = int(ASObject(args[3][0])[0])
        if self.widget:
            self.widget.flowerMC.gotoAndPlay('state%d' % state)

    def refreshDailyReward(self):
        data = ASTD.data.get(self.activityId, {})
        self.widget.pageStepper.count = self.currPage
        accuBonus = data.get('accuBonus')
        self.accuBonusList = []
        keyList = sorted(accuBonus.keys())
        for i, key in enumerate(keyList):
            itemInfo = {}
            itemInfo['days'] = key
            itemInfo['bonusId'] = accuBonus[key]
            if self.currSignTimes >= key:
                itemInfo['isSignIn'] = True
            else:
                itemInfo['isSignIn'] = False
            self.accuBonusList.append(itemInfo)

        showAccuBonusList = self.accuBonusList[ITEMS_NUM_PER_PAGE * (self.currPage - 1):ITEMS_NUM_PER_PAGE * self.currPage]
        for index in xrange(ITEMS_NUM_PER_PAGE):
            itemMc = getattr(self.widget.dailyReward, 'day%d' % index)
            if index < len(showAccuBonusList):
                itemMc.visible = True
                item = showAccuBonusList[index]
                itemMc.num.text = item['days']
                itemBonus = clientUtils.genItemBonus(item['bonusId'])
                itemId = itemBonus[0][0]
                itemCount = itemBonus[0][1]
                itemMc.slot.itemId = itemId
                itemMc.slot.dragable = False
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
                if item['isSignIn']:
                    itemMc.yes.visible = True
                else:
                    itemMc.yes.visible = False
            else:
                itemMc.visible = False

    def handleConfirmBtnClick(self, *args):
        BigWorld.player().cell.applyActivitySignIn(self.activityId)

    def handleReSignBtnClick(self, *args):
        gameglobal.rds.ui.activityReSignIn.show(self.canResignCnt, True, self.activityId)

    def _getDayIndex(self):
        startDay = ASTD.data.get(self.activityId, {}).get('startDay', 0)
        if not startDay:
            return False
        dayIdx = utils.diffYearMonthDayInt(int(uiUtils.zonetime(utils.getNow(), SCD.data.get('curZone', '8'))), int(startDay))
        duration = ASTD.data.get(self.activityId, {}).get('duration', 21)
        dayIdx = max(0, dayIdx)
        dayIdx = min(dayIdx, duration - 1)
        return dayIdx

    def hasSignedToday(self):
        if not self.activityId:
            return True
        else:
            newSignInInfo = getattr(BigWorld.player(), 'newSignInInfo', {}).get(self.activityId, None)
            if newSignInInfo:
                return newSignInInfo.hasSignedToday()
            return True

    def handleClickPreBtn(self, *args):
        self.currPage -= 1
        self.refreshDailyReward()

    def handleClickNextBtn(self, *args):
        self.currPage += 1
        self.refreshDailyReward()

    def onGetSignInBonus(self, randomRewardItems = [], exactRewardItems = []):
        if not self.widget:
            return
        self.specialRewards = randomRewardItems + exactRewardItems
        if self.specialRewards:
            item = self.specialRewards[0]
            self.showReward(item)

    def showReward(self, item):
        resultMc = self.widget.getInstByClsName('WelfareSignIn_resultMc')
        resultMc.name = 'resultMc'
        self.widget.addChild(resultMc)
        resultMc.visible = False
        resultMc.x = 471
        resultMc.y = 170
        itemId = item[0]
        itemCount = item[1]
        resultMc.slot.dragable = False
        resultMc.slot.itemId = itemId
        resultMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
        resultMc.play()
        resultMc.visible = True
        self.specialRewards.remove(item)
        ASUtils.callbackAtFrame(resultMc, 96, self.afterShowReward)

    def afterShowReward(self, *args):
        if not self.widget:
            return
        resultMc = self.widget.getChildByName('resultMc')
        if resultMc:
            resultMc.visible = False
            self.widget.removeChild(resultMc)
        if self.specialRewards:
            item = self.specialRewards[0]
            self.showReward(item)
