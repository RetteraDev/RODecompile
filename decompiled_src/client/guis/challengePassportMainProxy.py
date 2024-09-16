#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/challengePassportMainProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import ui
import clientUtils
import utils
import gametypes
from uiProxy import UIProxy
from asObject import ASObject
from asObject import ASUtils
from asObject import TipManager
from helpers import challengePassportHelper
from guis import uiUtils
from guis.ui import gbk2unicode
from gamestrings import gameStrings
from cdata import challenge_passport_season_data as CPSD
from data import challenge_passport_config_data as CPCD
from data import challenge_passport_target_data as CPTD
from data import mall_item_data as MID
from callbackHelper import Functor

class ChallengePassportMainProxy(UIProxy):
    TAB_REWARD = 0
    TAB_CHALLENGE = 1
    EVENT_MOVE_LEFT = 'moveLeft'
    EVENT_MOVE_RIGHT = 'moveRight'
    EVENT_MOVE_UP = 'moveUp'
    EVENT_MOVE_DOWN = 'moveDown'
    EVENT_POSITION_CHANGED = 'positionChanged'
    SCROLL_HORIZONTAL = 'horizontal'
    SCROLL_VERTICAL = 'vertical'

    def __init__(self, uiAdapter):
        super(ChallengePassportMainProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CHALLENGEPASSPORT_MAIN, self.handleCloseClick)

    def reset(self):
        self.selectTabBtn = None
        self.selectTabName = ''
        self.uplistData = []
        self.downlistData = []
        self.menuData = []
        self.currentSeasonWeekType = 2

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CHALLENGEPASSPORT_MAIN:
            self.widget = widget
            self.initUI()
            self.refreshInfo(True)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CHALLENGEPASSPORT_MAIN)
        self.reset()

    def show(self):
        if not gameglobal.rds.configData.get('enableChallengePassport', False):
            return
        if not uiUtils.isInChallengePassport():
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CHALLENGEPASSPORT_MAIN)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.closeGroup.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseClick, False, 0, True)
        self.widget.rewardTab.addEventListener(events.BUTTON_CLICK, self.handleTabChangeClick, False, 0, True)
        self.widget.challengeTab.addEventListener(events.BUTTON_CLICK, self.handleTabChangeClick, False, 0, True)
        self.widget.rewardPanel.leftArrow.addEventListener(events.BUTTON_CLICK, self.handleRewardMoveLeft, False, 0, True)
        self.widget.rewardPanel.rightArrow.addEventListener(events.BUTTON_CLICK, self.handleRewardMoveRight, False, 0, True)
        self.widget.rewardPanel.studyBtn.addEventListener(events.BUTTON_CLICK, self.handleStudyBtnClick, False, 0, True)
        self.widget.rewardPanel.unlockBtn.addEventListener(events.BUTTON_CLICK, self.handleUnlockBtnClick, False, 0, True)
        self.widget.rewardPanel.chargeTip.buyUnlockHit.addEventListener(events.MOUSE_CLICK, self.handleUnlockBtnClick, False, 0, True)
        self.widget.rewardPanel.uplist.itemRenderer = 'PassportPicture_UpListItem'
        self.widget.rewardPanel.uplist.lableFunction = self._uplistLabelFunction
        self.widget.rewardPanel.downlist.addEventListener(self.EVENT_POSITION_CHANGED, self.handleDownlistPositionChange, False, 0, True)
        self.widget.rewardPanel.downlist.itemRenderer = 'PassportPicture_DownListItem'
        self.widget.rewardPanel.downlist.lableFunction = self._downlistLabelFunction
        self.widget.rewardPanel.gainChallengeBtn.addEventListener(events.BUTTON_CLICK, self.handleTabChangeClick, False, 0, True)
        self.widget.helpBtn.addEventListener(events.MOUSE_CLICK, self.handleHelpBtnClick, False, 0, True)
        self.widget.rewardPanel.fixedGroup.downItem.list.addEventListener(events.MOUSE_WHEEL, self.handleDownlistWheel, False, 0, True)
        TipManager.addTip(self.widget.rewardPanel.unlockBtn, gameStrings.CHALLENGE_PASSPORT_UNLOCK_TIP)
        for i in xrange(1, 6):
            darkMc = self.widget.rewardPanel.exp.getChildByName('dark%d' % i)
            lightMc = self.widget.rewardPanel.exp.getChildByName('light%d' % i)
            darkMc.addEventListener(events.BUTTON_CLICK, self.handleTabChangeClick, False, 0, True)
            lightMc.addEventListener(events.BUTTON_CLICK, self.handleTabChangeClick, False, 0, True)
            TipManager.addTip(darkMc, gameStrings.CHALLENGE_PASSPORT_LISHIZHANG_TIP)
            TipManager.addTip(lightMc, gameStrings.CHALLENGE_PASSPORT_LISHIZHANG_TIP)

        self.uplistData, self.downlistData = self._getListDataArray()
        self.widget.challengePanel.daily.list.itemRenderer = 'PassportPicture_TargetListItem'
        self.widget.challengePanel.daily.list.lableFunction = self._targetlistLabelFunction
        self.widget.challengePanel.weekly.list.itemRenderer = 'PassportPicture_TargetListItem'
        self.widget.challengePanel.weekly.list.lableFunction = self._targetlistLabelFunction
        self.widget.challengePanel.season.list.itemRenderer = 'PassportPicture_TargetListItem'
        self.widget.challengePanel.season.list.lableFunction = self._targetlistLabelFunction
        self.menuData = []
        currentWeekType = uiUtils.getCurrentChallengePassportWeek()
        currentWeekSelect = 0
        for i, weekType in enumerate(gametypes.CHALLENGE_PASSPORT_TYPE_WEEK):
            if currentWeekType == weekType:
                currentWeekSelect = i
            self.menuData.append({'label': gameStrings.CHALLENGE_PASSPORT_WEEK % uiUtils.convertIntToChn(i + 1),
             'weekType': weekType})

        self.widget.challengePanel.weekDropdown.addEventListener(events.INDEX_CHANGE, self.handleWeekDropdownIndexChange, False, 0, True)
        ASUtils.setDropdownMenuData(self.widget.challengePanel.weekDropdown, self.menuData)
        self.widget.challengePanel.weekDropdown.selectedIndex = currentWeekSelect
        self.widget.gotoAndPlay('open')
        self._changeTab(self.widget.rewardTab.name)

    def refreshInfo(self, firstShow = False):
        if not self.widget:
            return
        self.currentSeasonWeekType = uiUtils.getCurrentChallengePassportWeek()
        self._refreshTitle()
        self._refreshPanel()
        if firstShow:
            p = BigWorld.player()
            minLv = p.challengePassportData.getMinNotTakenLevel()
            self.widget.rewardPanel.uplist.moveToPosition(minLv - 1)
            self.widget.rewardPanel.downlist.moveToPosition(minLv - 1)

    def checkRedPointVisible(self):
        p = BigWorld.player()
        return p.challengePassportData.hasRewardNotTaken()

    @ui.callFilter(2, False)
    def handleCloseClick(self, *args):
        self.widget.closeGroup.closeBtn.removeEventListener(events.BUTTON_CLICK, self.handleCloseClick)
        self.widget.gotoAndPlay('close')
        ASUtils.callbackAtFrame(self.widget, 79, self.__onHide)

    def __onHide(self, *args):
        self.hide()

    def handleTabChangeClick(self, *args):
        if not self.widget or not self.widget.challengeTab:
            return
        e = ASObject(args[3][0])
        target = e.currentTarget
        if target.name.startswith('dark') or target.name.startswith('light') or target.name == 'gainChallengeBtn':
            targetName = self.widget.challengeTab.name
        else:
            targetName = target.name
        self._changeTab(targetName)

    def handleRewardMoveLeft(self, *args):
        self._moveUpAndDownList(self.EVENT_MOVE_LEFT)

    def handleRewardMoveRight(self, *args):
        self._moveUpAndDownList(self.EVENT_MOVE_RIGHT)

    def handleStudyBtnClick(self, *args):
        coinNeed = CPCD.data.get('challengePassportLvCoinNeed', 10)
        text = gameStrings.CHALLENGE_PASSPORT_BUY_LEVEL_WARNING % uiUtils.toHtml(str(coinNeed), '#DC143C')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(text, self._realRequestBuyLevel)

    def _realRequestBuyLevel(self):
        p = BigWorld.player()
        p.challengePassportData.requestBuyLevel()

    def handleUnlockBtnClick(self, *args):
        itemPrice = CPCD.data.get('challengePassportChargeCoinNeed', 10)
        msg = gameStrings.CHALLENGE_PASSPORT_BUY_CONFIRM % itemPrice
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.confirmUnlockBuy)

    @ui.checkInventoryLock()
    def confirmUnlockBuy(self):
        p = BigWorld.player()
        p.base.challengePassportBuyCharge()

    def handleDownlistWheel(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        num = target.canvas.numChildren
        fixedItem = self.widget.rewardPanel.fixedGroup.downItem
        ASUtils.DispatchSimpleEvent(fixedItem.list, self.EVENT_MOVE_UP if e.delta > 0 else self.EVENT_MOVE_DOWN)
        for i in xrange(num):
            child = target.canvas.getChildAt(i)
            if e.delta > 0:
                ASUtils.DispatchSimpleEvent(child.list, self.EVENT_MOVE_UP)
            else:
                ASUtils.DispatchSimpleEvent(child.list, self.EVENT_MOVE_DOWN)

    def handleDownlistWheelNew(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        ASUtils.DispatchSimpleEvent(target, self.EVENT_MOVE_UP if e.delta > 0 else self.EVENT_MOVE_DOWN)

    def handleDownlistPositionChange(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        endPosition = target.endDisplayPosition
        displayUpData, displayDownData = self._getNearestDisplayData(endPosition - 1)
        if displayUpData and displayDownData:
            self.widget.rewardPanel.fixedGroup.visible = True
            asobjectUpdata = ASObject(uiUtils.dict2GfxDict(displayUpData, True))
            asobjectDowndata = ASObject(uiUtils.dict2GfxDict(displayDownData))
            self._setUplistItemData(self.widget.rewardPanel.fixedGroup.upItem, asobjectUpdata, True)
            self._setDownlistItemData(self.widget.rewardPanel.fixedGroup.downItem, asobjectDowndata, True)
        else:
            self.widget.rewardPanel.fixedGroup.visible = False

    def handleItemGetBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        p = BigWorld.player()
        if target.itemLevel and target.itemLevel > 0:
            p.challengePassportData.requestReceiveBonus(target.itemLevel)

    def handleWeekDropdownIndexChange(self, *args):
        if not self.widget:
            return
        selectedIndex = self.widget.challengePanel.weekDropdown.selectedIndex
        self._refreshTargetGroupData(self.menuData[selectedIndex].get('weekType', 0))

    def handleHelpBtnClick(self, *args):
        gameglobal.rds.ui.challengePassportAppoint2.show()

    @ui.uiEvent(uiConst.WIDGET_CHALLENGEPASSPORT_MAIN, events.EVNET_CHALLENGE_PASSPORT_DATA_CHANGE)
    def onDataChange(self, event):
        self.refreshInfo()

    def _changeTab(self, btnName):
        if not self.widget:
            return
        if self.selectTabName == btnName:
            return
        self.selectTabName = btnName
        if btnName == self.widget.rewardTab.name:
            self.widget.challengeTab.selected = False
            self.widget.rewardTab.selected = True
            self.widget.challengePanel.visible = False
            self.widget.rewardPanel.visible = True
        elif btnName == self.widget.challengeTab.name:
            self.widget.challengeTab.selected = True
            self.widget.rewardTab.selected = False
            self.widget.challengePanel.visible = True
            self.widget.rewardPanel.visible = False
        self._refreshPanel()

    def _refreshPanel(self):
        if not self.widget:
            return
        if self.widget.rewardPanel.visible:
            self._refreshRewardPanel()
        elif self.widget.challengePanel.visible:
            self._refreshChallengePanel()

    def _refreshRewardPanel(self):
        p = BigWorld.player()
        level = int(p.challengePassportData.lv)
        exp = int(p.challengePassportData.exp)
        isCharge = p.challengePassportData.isCharge
        self.widget.rewardPanel.level.text = '%d' % level
        self.widget.rewardPanel.exp.gotoAndStop('exp%d' % exp)
        self.widget.rewardPanel.lockIcon.visible = not isCharge
        self.widget.rewardPanel.unlockBtn.visible = not isCharge
        self.widget.rewardPanel.chargeTip.visible = not isCharge
        self.widget.rewardPanel.uplist.dataArray = self.uplistData
        self.widget.rewardPanel.uplist.validateNow()
        self.widget.rewardPanel.downlist.dataArray = self.downlistData
        self.widget.rewardPanel.downlist.validateNow()

    def _refreshChallengePanel(self):
        self._refreshTargetGroupData(gametypes.CHALLENGE_PASSPORT_TYPE_DAY)
        self._refreshTargetGroupData(gametypes.CHALLENGE_PASSPORT_TYPE_SEASON)
        selectedIndex = self.widget.challengePanel.weekDropdown.selectedIndex
        self._refreshTargetGroupData(self.menuData[selectedIndex].get('weekType', 0))
        self.addMissionTip()

    def addMissionTip(self):
        TipManager.addTip(self.widget.challengePanel.tipIcon, gameStrings.PASSPORT_FINISH_TIP)

    def _refreshTitle(self):
        season = uiUtils.getCurrentChallengePassportSeason()
        seasonData = CPSD.data.get(season, {})
        self.widget.clothPic.gotoAndStop(seasonData.get('clothName', ''))
        self.widget.clothName.gotoAndStop(seasonData.get('clothName', ''))
        if season == -1:
            beginTime = uiUtils.getNewServerSeasonBegin()
            endTime = uiUtils.getNewServerSeasonEnd()
            seasonDesc = gameStrings.CHALLENGE_PASSPORT_SEASON_NEW
        else:
            beginTime = utils.getDateStrFromStr(seasonData.get('beginTime', ''))
            endTime = utils.getDateStrFromStr(seasonData.get('endTime', ''))
            seasonDesc = gameStrings.CHALLENGE_PASSPORT_SEASON % uiUtils.convertIntToChn(season)
        limitItems = seasonData.get('challengePassportMaxSeasonItemIds', ())
        self.widget.titleGroup.visible = True
        self.widget.titleGroup.season.text = seasonDesc
        self.widget.titleGroup.date.text = '%s-%s' % (beginTime, endTime)
        if len(limitItems) == 4:
            self.widget.titleGroup.gotoAndStop('item4')
        else:
            self.widget.titleGroup.gotoAndStop('item3')
        for i, itemId in enumerate(limitItems):
            itemMc = self.widget.titleGroup.getChildByName('limited%d' % (i + 1))
            if itemMc:
                itemMc.slot.enabled = True
                itemMc.slot.dragable = False
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, 0))

    def _uplistLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self._setUplistItemData(itemMc, itemData)

    def _downlistLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self._setDownlistItemData(itemMc, itemData)

    def _downlistItemLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        p = BigWorld.player()
        isCharge = p.challengePassportData.isCharge
        itemId = itemData.itemId
        itemCount = itemData.itemCount
        isTaken = itemData.isTaken
        itemMc.slot.dragable = False
        itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
        itemMc.getFlag.visible = isTaken and isCharge

    def _targetlistLabelFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        p = BigWorld.player()
        targetId = itemData.targetId
        weekType = itemData.weekType
        config = CPTD.data.get(targetId, {})
        exp = config.get('exp', 0)
        desc = config.get('desc', '')
        finishCnt = config.get('finishCnt', 1)
        totalProgress = config.get('totalProgress', 0)
        currentProgress = challengePassportHelper.getTargetCurrentProgress(targetId)
        targetLoopFinishCnt = p.challengePassportData.getTargetFinishTimes(targetId)
        isDone = challengePassportHelper.isTargetDone(targetId)
        isOpenWeek = weekType <= self.currentSeasonWeekType
        if isOpenWeek:
            progText = '(%d/%d)' % (min(currentProgress, totalProgress), totalProgress)
            expText = '%d' % exp
        else:
            desc = '? ? ? ? ?'
            progText = '(%d/%s)' % (min(currentProgress, totalProgress), '??')
            expText = '??'
        itemMc.gotoAndStop('undone' if not isDone else 'done')
        if config.get('groupId', 0) and weekType == self.currentSeasonWeekType:
            itemMc.refreshBtn.visible = True
            groupId = config.get('groupId', 0)
            targetTime = p.challengePassportData.optionalTarget.get(groupId, {}).get('times', 0)
            totalTime = CPCD.data.get('challengePassportRefreshOptionalTargetTimes', 0)
            itemMc.refreshBtn.groupId = groupId
            itemMc.refreshBtn.targetTime = targetTime
            itemMc.refreshBtn.totalTime = totalTime
            if targetTime >= totalTime or isDone:
                itemMc.refreshBtn.enabled = False
            else:
                itemMc.refreshBtn.enabled = True
            itemMc.refreshBtn.addEventListener(events.BUTTON_CLICK, self.onRefreshBtnClick, False, 0, True)
        else:
            itemMc.refreshBtn.visible = False
        itemMc.desc.text = desc
        if itemMc.desc.textWidth > itemMc.desc.width:
            itemMc.desc.htmlText = uiUtils.toHtml(desc, color=itemMc.desc.textColor, fontSize=10)
        else:
            itemMc.desc.htmlText = uiUtils.toHtml(desc, color=itemMc.desc.textColor, fontSize=11)
        itemMc.progress.text = progText
        itemMc.roundTime.visible = False
        itemMc.exp.text = expText
        itemMc.icon.bonusType = 'passport'
        if isOpenWeek:
            itemMc.loopFlag.visible = finishCnt > 1
            TipManager.addTip(itemMc.loopFlag, gameStrings.CHALLENGE_PASSPORT_LOOP_TARGET_TIP % (finishCnt, targetLoopFinishCnt))
        else:
            itemMc.loopFlag.visible = False

    def onRefreshBtnClick(self, *args):
        e = ASObject(args[3][0])
        groupId = e.currentTarget.groupId
        targetTime = e.currentTarget.targetTime
        totalTime = e.currentTarget.totalTime
        msg = gameStrings.CHALLENGE_PASSPORT_TASK_REFRESH_CONFIRM % (totalTime, targetTime + 1)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.onConfirmRefresh, groupId))

    def onConfirmRefresh(self, groupId):
        p = BigWorld.player()
        p.base.challengePassportRefreshOptionalTarget(groupId)

    def _getListDataArray(self):
        lvConfig = challengePassportHelper.getChallengePassportLvData()
        upData = []
        downData = []
        for lv, data in lvConfig.iteritems():
            upData.append({'lv': lv,
             'bonusId': data.get('freeBonus', -1)})
            downData.append({'lv': lv,
             'bonusId': data.get('chargeBonus', -1)})

        upData.sort(key=lambda x: x['lv'])
        downData.sort(key=lambda x: x['lv'])
        return (upData, downData)

    def _getNearestDisplayData(self, position):
        CPLvData = challengePassportHelper.getChallengePassportLvData()
        if not self.uplistData:
            return ({'lv': 0,
              'bonusId': -1}, {'lv': 0,
              'bonusId': -1})
        else:
            for i, data in enumerate(self.uplistData):
                lv = data.get('lv', 0)
                if lv >= position + 1 and CPLvData.get(lv, {}).get('isDisplay', False):
                    return (self.uplistData[i], self.downlistData[i])
            else:
                return (None, None)

            return None

    def _setUplistItemData(self, itemMc, itemData, isFixed = False):
        lv = itemData.lv
        if lv:
            if type(lv) is float:
                lv = int(lv)
        else:
            lv = 0
        bonusId = itemData.bonusId
        p = BigWorld.player()
        bonusPool = p.challengePassportData.bonusPool
        isTaken = lv in bonusPool
        itemMc.getBtn.itemLevel = lv
        if isFixed or isTaken or lv > p.challengePassportData.lv or bonusId < 0 and not p.challengePassportData.isCharge:
            itemMc.desc.visible = True
            itemMc.getBtn.visible = False
            itemMc.getBtn.itemLevel = -1
            itemMc.desc.text = gameStrings.CHALLENGE_PASSPORT_LEVEL % lv
        else:
            itemMc.desc.visible = False
            itemMc.getBtn.visible = True
            itemMc.getBtn.enabled = True
            itemMc.getBtn.addEventListener(events.BUTTON_CLICK, self.handleItemGetBtnClick, False, 0, True)
        if itemMc.getBtn.visible:
            itemMc.getBtn.validateNow()
        if lv > p.challengePassportData.lv and not isFixed:
            itemMc.activeBg.visible = False
        else:
            itemMc.activeBg.visible = True
        itemMc.item1.visible = False
        itemMc.item2.visible = False
        if bonusId > 0:
            bonusList = clientUtils.genItemBonus(bonusId)
            for i, itemInfo in enumerate(bonusList):
                itemId, itemCount = itemInfo
                itemSlot = itemMc.getChildByName('item%d' % (i + 1))
                if itemSlot:
                    itemSlot.visible = True
                    itemSlot.slot.dragable = False
                    itemSlot.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
                    itemSlot.getFlag.visible = isTaken

    def _setDownlistItemData(self, itemMc, itemData, isFixed = False):
        lv = itemData.lv
        bonusId = itemData.bonusId
        p = BigWorld.player()
        isTaken = lv in p.challengePassportData.bonusPool
        itemMc.list.scrollMode = self.SCROLL_VERTICAL
        itemMc.list.itemRenderer = 'PassportPicture_DownListItemItem'
        itemMc.list.lableFunction = self._downlistItemLabelFunction
        itemMc.list.interval = 5
        itemMc.list.addEventListener(events.MOUSE_WHEEL, self.handleDownlistWheelNew, False, 0, True)
        bonusList = clientUtils.genItemBonus(bonusId)
        itemMc.list.positionOffset = 0 if len(bonusList) <= 2 else 1
        itemMc.list.dataArray = [ {'itemId': itemId,
         'itemCount': itemCount,
         'isFixed': isFixed,
         'isTaken': isTaken} for itemId, itemCount in bonusList ]
        if isFixed or p.challengePassportData.isCharge and lv <= p.challengePassportData.lv:
            itemMc.activeBg.visible = True
        else:
            itemMc.activeBg.visible = False
        itemMc.list.validateNow()

    def _refreshTargetGroupData(self, targetType):
        groupMc = self._getTargetGroupMcByType(targetType)
        if not groupMc:
            return
        allDoneExp, allExp, numAllTarget, numDoneTarget, targetList = challengePassportHelper.getTargetsInfoByType(targetType)
        if targetType in gametypes.CHALLENGE_PASSPORT_TYPE_WEEK:
            weekType = targetType
            isOpenWeek = weekType <= self.currentSeasonWeekType
        else:
            weekType = self.currentSeasonWeekType
            isOpenWeek = True
        groupMc.list.dataArray = [ {'weekType': weekType,
         'targetId': tid} for tid in targetList ]
        groupMc.list.validateNow()
        groupMc.progress.currentValue = numDoneTarget
        groupMc.progress.maxValue = numAllTarget
        if isOpenWeek:
            labelText = '%d/%d' % (allDoneExp, allExp)
        else:
            labelText = '%d/%s' % (allDoneExp, '??')
        groupMc.totalProgress.icon.bonusType = 'passport'
        groupMc.totalProgress.label.text = labelText
        finishRewardBonusId = CPSD.data.get('bonusId', {}).get(targetType, 0)
        bonusList = clientUtils.genItemBonus(finishRewardBonusId)
        if bonusList:
            itemId, itemCount = bonusList[0]
            groupMc.itemSlot.visible = True
            groupMc.itemSlot.slot.setItemSlotData(uiUtils.getGfxItemById(itemId, itemCount))
        else:
            groupMc.itemSlot.visible = False

    def _getTargetGroupMcByType(self, targetType):
        if targetType == gametypes.CHALLENGE_PASSPORT_TYPE_DAY:
            return self.widget.challengePanel.daily
        elif targetType in gametypes.CHALLENGE_PASSPORT_TYPE_WEEK:
            return self.widget.challengePanel.weekly
        elif targetType == gametypes.CHALLENGE_PASSPORT_TYPE_SEASON:
            return self.widget.challengePanel.season
        else:
            return None

    def _moveUpAndDownList(self, moveEvent):
        uplist = self.widget.rewardPanel.uplist
        downlist = self.widget.rewardPanel.downlist
        num = downlist.canvas.numChildren
        for i in xrange(num):
            child = downlist.canvas.getChildAt(i)
            child.list.resetCanvas()

        ASUtils.DispatchSimpleEvent(uplist, moveEvent)
        ASUtils.DispatchSimpleEvent(downlist, moveEvent)
        fixedItem = self.widget.rewardPanel.fixedGroup.downItem
        fixedItem.list.resetCanvas()
