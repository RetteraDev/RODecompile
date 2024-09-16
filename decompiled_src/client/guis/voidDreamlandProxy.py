#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidDreamlandProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import clientUtils
import const
import utils
import gamelog
from uiTabProxy import UITabProxy
from guis import uiUtils
from callbackHelper import Functor
from gamestrings import gameStrings
from guis import tipUtils
from appSetting import Obj as AppSettings
import keys
from guis.asObject import MenuManager
from guis.asObject import TipManager
from guis.asObject import ASObject
from data import sys_config_data as SCD
from data import bonus_history_check_data as BHCD
from data import endless_challenge_reward_floor_query_reverse_data as ECRFQRD
from cdata import game_msg_def_data as GMDD
from cdata import endless_challenge_reward_reverse_data as ECRRD
from cdata import endless_challenge_weekly_buff_reverse_data as ECWBRD
from cdata import endless_challenge_season_list_data as ECSLD
MAX_SLOT_NUM = 6
MAX_DROP_REWARDS_NUM = 8
MAX_AVAILABLE_FLOOR = 10
GRADE_SECTION0 = 60
GRADE_SECTION1 = 70
TAB_INDEX0 = 0
TAB_INDEX1 = 1
TAB_INDEX2 = 2

class VoidDreamlandProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(VoidDreamlandProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        self.currSelectProgress = -1
        self.currSelectItem = None
        self.season = -1
        self.rewardInfo = {}
        self.challengeCount = -1
        self.weeklyInterval = 0
        self.challengeLevelItemList = []
        self.curfinishMaxProgress = 0
        self.levelToStage = []
        self.initLevelToStage()
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_DREAMLAND, self.hide)

    def initLevelToStage(self):
        self.levelToStage = []
        endlessAvailableLv = SCD.data.get('endlessAvailableLv', ())
        for lvRange in endlessAvailableLv:
            self.levelToStage.append('%d_%d' % (lvRange[0], lvRange[1]))

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_DREAMLAND:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)
            gameglobal.rds.sound.playSound(gameglobal.SD_4)

    def show(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableEndlessChallenge', False):
            p.showGameMsg(GMDD.data.SERVICE_TEMPORARY_UNAVAILABLE, ())
            return
        self.showTabIndex = self.getMyGradeTabIndex(p.lv)
        if self.widget:
            self.widget.setTabIndex(self.showTabIndex)
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VOID_DREAMLAND)
        self.uiAdapter.pushMessage.removePushMsg(uiConst.PUSH_TYPE_VOID_DREAM_LAND_SEASON)

    def clearWidget(self):
        super(VoidDreamlandProxy, self).clearWidget()
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_VOID_DREAMLAND)
        gameglobal.rds.sound.playSound(gameglobal.SD_5)

    def reset(self):
        super(VoidDreamlandProxy, self).reset()
        self.currSelectProgress = -1
        self.currSelectItem = None
        self.season = -1
        self.rewardInfo = {}
        self.challengeCount = -1
        self.weeklyInterval = 0
        self.curfinishMaxProgress = 0

    def _getTabList(self):
        return [{'tabIdx': TAB_INDEX0,
          'tabName': 'tabCopper',
          'view': 'VoidDreamland_tabLevelMc',
          'pos': (3, 115)}, {'tabIdx': TAB_INDEX1,
          'tabName': 'tabSilver',
          'view': 'VoidDreamland_tabLevelMc',
          'pos': (3, 115)}, {'tabIdx': TAB_INDEX2,
          'tabName': 'tabGold',
          'view': 'VoidDreamland_tabLevelMc',
          'pos': (3, 115)}]

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.refreshTabName()
        self.initTabUI()

    def getMyGradeTabIndex(self, lv):
        if lv < GRADE_SECTION0:
            return TAB_INDEX0
        elif lv < GRADE_SECTION1:
            return TAB_INDEX1
        else:
            return TAB_INDEX2

    def onTabChanged(self, *args):
        super(VoidDreamlandProxy, self).onTabChanged(*args)
        self.currentView.scrollWndList.scrollbar.addEventListener(events.SCROLL, self.handleScroll, False, 0, True)
        self.updateTabInfoMc()

    def _onBackgroundClick(self, e):
        if not gameglobal.rds.ui.voidDreamlandRule.widget:
            gameglobal.rds.ui.voidDreamlandRule.show()

    def _onBeginGameClick(self, e):
        if self.currSelectProgress == -1:
            return
        rank = self.levelToStage[self.currentTabIndex]
        if self.currSelectProgress == self.curfinishMaxProgress:
            gameglobal.rds.ui.voidDreamlandGodHelp.show(rank, self.currSelectProgress, self.challengeCount)
            return
        p = BigWorld.player()
        if self.challengeCount > 0:
            p.cell.applyFubenOfEndless(rank, self.currSelectProgress, self.currSelectProgress < self.curfinishMaxProgress)
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.VOID_DREAMLANG_NONT_CHALLENGE_COUNT, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.applyFubenOfEndless, rank, self.currSelectProgress, self.currSelectProgress < self.curfinishMaxProgress))

    def _onRewardQueryClick(self, e):
        rank = self.levelToStage[self.currentTabIndex]
        gameglobal.rds.ui.voidDreamlandRewardQuery.show(rank, self.currSelectProgress)

    def _onWeekBuffBtnClick(self, e):
        rank = self.levelToStage[self.currentTabIndex]
        gameglobal.rds.ui.voidDreamlandWeekBuff.show(rank, self.weeklyInterval)

    def handleScroll(self, *args):
        if self.widget:
            MenuManager.getInstance().hideMenu()

    def handleRewardBoxClick(self, *args):
        e = ASObject(args[3][0])
        rewardBoxState = e.currentTarget.parent.rewardBoxState
        progress = e.currentTarget.parent.diffIdx
        if rewardBoxState == -1:
            self.showRewardInfoTips(e.target, progress)
        elif rewardBoxState == 0:
            p = BigWorld.player()
            p.base.getEndlessProgressReward(self.levelToStage[self.currentTabIndex], progress)

    def handleDiffLevelBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        btnName = e.currentTarget.name
        if btnName == 'diffLevelBtnNormal':
            self.currentView.beginGame.enabled = True
        elif btnName == 'diffLevelBtnDisable':
            self.currentView.beginGame.enabled = False
        if self.currSelectProgress == itemMc.diffIdx:
            return
        if self.currSelectItem:
            self.currSelectItem.selected = False
        self.currSelectProgress = itemMc.diffIdx
        self.currSelectItem = itemMc
        itemMc.selected = True
        self.updateDropRewardMc(itemMc.diffIdx)

    def updateDropRewardMc(self, diffIdx):
        rewardMc = self.currentView.rewardMc
        rewardMc.diffText.text = diffIdx
        rank = self.levelToStage[self.currentTabIndex]
        data = ECRFQRD.data.get((rank, diffIdx), {})
        if not data:
            data = ECRFQRD.data.get((rank, -1), {})
        tReardInfo = data.get('edsAwdItem', ())
        for i in range(MAX_DROP_REWARDS_NUM):
            slot = rewardMc.rewardSlots.getChildByName('slot%d' % i)
            if i < len(tReardInfo):
                slot.visible = True
                slot.dragable = False
                tInfo = tReardInfo[i]
                slot.setItemSlotData(uiUtils.getGfxItemById(tInfo[0], tInfo[1]))
            else:
                slot.visible = False

    def updateTabInfoMc(self):
        p = BigWorld.player()
        p.base.queryEndlessChallengeInfo(self.levelToStage[self.currentTabIndex])
        self.currSelectProgress = -1
        self.currentView.scrollWndList.itemRenderer = 'VoidDreamland_diffLevelItem'
        self.currentView.scrollWndList.dataArray = []
        self.currentView.scrollWndList.lableFunction = self.itemFunction

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.diffLevelBtnNormal.visible = itemData.availableProgress >= itemData.diffIdx
        itemMc.diffLevelBtnDisable.visible = itemData.availableProgress < itemData.diffIdx
        if itemMc.diffLevelBtnNormal.visible:
            diffLevelBtn = itemMc.diffLevelBtnNormal
            diffLevelBtn.selected = False
            if self.currSelectProgress == -1 and itemData.nextDiff == itemData.diffIdx or self.currSelectProgress == itemData.diffIdx:
                diffLevelBtn.selected = True
                self.currentView.beginGame.enabled = True
        else:
            diffLevelBtn = itemMc.diffLevelBtnDisable
            diffLevelBtn.selected = False
            if self.currSelectProgress == -1 and itemData.nextDiff == -1 and itemData.diffIdx == 1 or self.currSelectProgress == itemData.diffIdx:
                diffLevelBtn.selected = True
                self.currentView.beginGame.enabled = False
        diffLevelBtn.validateNow()
        diffLevelBtn.mouseChildren = True
        diffLevelBtn.diffIdx = itemData.diffIdx
        diffLevelBtn.label = gameStrings.VOID_DREAMLAND_DIFFLEVLE_BTN_LABEL % str(itemData.diffIdx)
        if itemData.showRewardBox:
            diffLevelBtn.rewardState.visible = True
            diffLevelBtn.rewardBoxState = itemData.finishState
            diffLevelBtn.rewardState.gotoAndStop('noneGet')
            diffLevelBtn.rewardState.addEventListener(events.MOUSE_CLICK, self.handleRewardBoxClick, False, 0, True)
            if itemData.finishState == 0:
                diffLevelBtn.rewardState.gotoAndStop('canGet')
            elif itemData.finishState == 1:
                diffLevelBtn.rewardState.gotoAndStop('alreadyGet')
        else:
            diffLevelBtn.rewardState.visible = False
        if itemData.isGodHelp:
            diffLevelBtn.patternIcon.gotoAndStop('godHelp')
        else:
            diffLevelBtn.patternIcon.gotoAndStop('normal')
        playerIconMaxNum = 3
        for i in xrange(playerIconMaxNum):
            playerIcon = diffLevelBtn.playerList.getChildByName('playerIcon%d' % i)
            if i < len(itemData.playerList):
                p = BigWorld.player()
                tPlayer = itemData.playerList[i]
                if str(p.gbId) == tPlayer[4]:
                    playerIcon.gotoAndStop('wo')
                else:
                    playerIcon.gotoAndStop('bieren')
                photo = tPlayer[0]
                if uiUtils.isDownloadImage(photo):
                    photo = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + photo + '.dds'
                if not photo:
                    photo = p.friend.getDefaultPhoto(tPlayer[1], tPlayer[2])
                playerIcon.visible = True
                playerIcon.icon.clear()
                playerIcon.icon.fitSize = True
                playerIcon.icon.loadImage(photo)
                TipManager.addTip(playerIcon, tPlayer[3], tipUtils.TYPE_DEFAULT_BLACK)
            else:
                playerIcon.visible = False

        if diffLevelBtn.selected:
            self.currSelectProgress = itemData.diffIdx
            self.currSelectItem = diffLevelBtn
            self.updateDropRewardMc(itemData.diffIdx)
        diffLevelBtn.addEventListener(events.MOUSE_DOWN, self.handleDiffLevelBtnClick, False, 0, True)

    def updatelevelItemData(self, challengeInfo):
        if not self.widget:
            return
        rank = challengeInfo.get('rank', '')
        if rank != self.levelToStage[self.currentTabIndex]:
            return
        self.season = challengeInfo.get('season', 0)
        self.weeklyInterval = challengeInfo.get('weeklyInterval', 0)
        self.rewardInfo = self.getRewardInfo()
        maxProgress = max(challengeInfo.get('maxProgress', 0) + MAX_AVAILABLE_FLOOR, SCD.data.get('endlessDefaultFloorLimit', 0))
        friendEndlessInfo = challengeInfo.get('friendEndlessInfo', {})
        finishProgress = challengeInfo.get('finishProgress', {})
        availableProgress = challengeInfo.get('availableProgress', 0)
        if finishProgress:
            self.curfinishMaxProgress = sorted(finishProgress.keys())[-1]
        self.challengeLevelItemList = []
        for i in range(1, maxProgress + 1)[::-1]:
            playerList = []
            finishState = -1
            if i in friendEndlessInfo:
                playerList = friendEndlessInfo[i]
                playerList.sort(key=lambda x: x[5])
            if i in finishProgress:
                finishState = finishProgress[i]
            itemInfo = {}
            itemInfo['diffIdx'] = i
            itemInfo['playerList'] = playerList
            itemInfo['finishState'] = finishState
            itemInfo['availableProgress'] = availableProgress
            if self.showTabIndex == self.currentTabIndex:
                itemInfo['nextDiff'] = min(len(finishProgress) + 1, maxProgress)
            else:
                itemInfo['nextDiff'] = -1
            if i in self.rewardInfo:
                itemInfo['showRewardBox'] = True
            else:
                itemInfo['showRewardBox'] = False
            if i <= self.curfinishMaxProgress:
                itemInfo['isGodHelp'] = True
            else:
                itemInfo['isGodHelp'] = False
            self.challengeLevelItemList.append(itemInfo)

        self.currentView.scrollWndList.dataArray = self.challengeLevelItemList
        self.currentView.scrollWndList.validateNow()
        nextDiff = min(len(finishProgress) + 1, maxProgress)
        indexPosY = max(maxProgress - nextDiff, 0)
        pos = self.currentView.scrollWndList.getIndexPosY(indexPosY)
        self.currentView.scrollWndList.scrollTo(pos)
        weekInfo = ECWBRD.data.get(rank, {}).get(self.weeklyInterval, {})
        if weekInfo:
            self.currentView.weekBuffBtn.label = weekInfo.get('name', '')
            self.currentView.weekBuffBtn.enabled = True
        else:
            self.currentView.weekBuffBtn.label = gameStrings.VOID_DREAMLAND_BUFF_BTN_UNACTIVATION
            self.currentView.weekBuffBtn.enabled = False

    def updateRewardBoxState(self, rank, progress):
        if not self.widget:
            return
        if rank != self.levelToStage[self.currentTabIndex]:
            return
        for itemInfo in self.challengeLevelItemList:
            if itemInfo['showRewardBox'] and itemInfo['diffIdx'] == progress:
                itemInfo['finishState'] = 1

        self.currentView.scrollWndList.dataArray = self.challengeLevelItemList

    def getRewardInfo(self):
        rank = self.levelToStage[self.currentTabIndex]
        rankInfo = SCD.data.get('endlessChallengeRankInfo', {})
        fbNo = rankInfo.get(rank, {}).get('fbNo', 0)
        if self.season == -1:
            return
        return ECRRD.data.get((self.season, fbNo), {})

    def showRewardInfoTips(self, target, progress):
        if progress in self.rewardInfo:
            bonusId = self.rewardInfo[progress]
        else:
            bonusId = 0
        if not bonusId:
            return
        itemBonus = clientUtils.genItemBonus(bonusId)
        if not itemBonus:
            return
        rewardTipsPanel = self.widget.getInstByClsName('VoidDreamland_rewardTips')
        itemList = []
        for item in itemBonus:
            itemList.append([item[0], item[1]])

        for i in range(MAX_SLOT_NUM):
            item = rewardTipsPanel.getChildByName('slot%d' % i)
            if i < len(itemList):
                item.visible = True
                tInfo = itemList[i]
                item.slot.setItemSlotData(uiUtils.getGfxItemById(tInfo[0], tInfo[1]))
            else:
                item.visible = False

        itemSlotFirst = rewardTipsPanel.getChildByName('slot0')
        rewardTipsPanel.tipBg.width = 30 + len(itemList) * (itemSlotFirst.width + 2)
        rewardTipsPanel.textField.x = (rewardTipsPanel.tipBg.width - rewardTipsPanel.textField.width) * 1.0 / 2 + 8
        menuParent = self.currentView.scrollWndList.canvas
        itemMcCurr = target.parent.parent.parent
        MenuManager.getInstance().showMenu(target, rewardTipsPanel, {'x': itemMcCurr.x + target.parent.x + target.parent.width,
         'y': itemMcCurr.y}, True, menuParent)

    def getBonusCheckId(self):
        rank = self.levelToStage[self.currentTabIndex]
        rankInfo = SCD.data.get('endlessChallengeRankInfo', {})
        bonusCheckId = rankInfo.get(rank, {}).get('bonusCheckId', 0)
        return bonusCheckId

    def updateLeftChallengeCount(self, data):
        if not self.widget:
            return
        bonusCheckId = self.getBonusCheckId()
        maxChallengeCount = BHCD.data.get(bonusCheckId, {}).get('times', 0)
        challengeCount = maxChallengeCount
        _, res = data
        for cid, value in res.iteritems():
            if cid == bonusCheckId:
                challengeCount = max(maxChallengeCount - value, 0)
                break

        self.currentView.boxKeyNum.text = '%d' % challengeCount
        tips = SCD.data.get('endlessKeyTips', '%d') % challengeCount
        TipManager.addTip(self.currentView.boxKeyNum, tips)
        TipManager.addTip(self.currentView.keyIcon, tips)
        self.challengeCount = challengeCount

    def tryAddPushInfo(self):
        if not gameglobal.rds.configData.get('enableEndlessChallenge', False):
            return
        else:
            p = BigWorld.player()
            if p.lv < 50:
                return
            currentSeason = 0
            startTimeStr, endTimeStr = (None, None)
            try:
                for id, info in ECSLD.data.iteritems():
                    sTime, eTime = info.get('beginTime', None), info.get('stopTime', None)
                    if sTime and eTime and utils.inCrontabRangeWithYear(sTime, eTime):
                        startTimeStr, endTimeStr = sTime, eTime
                        currentSeason = id
                        break

                if not currentSeason:
                    return
                if not endTimeStr:
                    return
                endTime = utils.getNextCrontabTime(endTimeStr)
            except Exception as e:
                return

            if endTime - 259200 < utils.getNow() < endTime:
                lastCheckTime = 0
                userSaveTimeStrList = AppSettings.get(keys.SET_VOID_DREAM_LAND_CHECK_TIME, '').split(',')
                saveData = {}
                for userData in userSaveTimeStrList:
                    if not userData:
                        continue
                    gbIdStr, timeStr = userData.split('_')
                    saveData[int(gbIdStr)] = int(timeStr)
                    if int(gbIdStr) == p.gbId:
                        lastCheckTime = int(timeStr)
                        break

                if utils.isSameDay(lastCheckTime, utils.getNow()):
                    return
                if len(saveData) >= 5:
                    saveData.pop(saveData.keys()[0])
                saveData[p.gbId] = utils.getNow()
                saveStrList = [ '%d_%d' % (gbId, saveData[gbId]) for gbId in saveData ]
                AppSettings[keys.SET_VOID_DREAM_LAND_CHECK_TIME] = ','.join(saveStrList)
                AppSettings.save()
                self.uiAdapter.pushMessage.addPushMsg(uiConst.PUSH_TYPE_VOID_DREAM_LAND_SEASON)
                self.uiAdapter.pushMessage.setCallBack(uiConst.PUSH_TYPE_VOID_DREAM_LAND_SEASON, {'click': self.show})
            return

    def refreshTabName(self):
        fromLv, toLv = self.levelToStage[2].split('_')
        if gameglobal.rds.configData.get('enableNewLv89', False):
            toLv = 89
        self.widget.tabGold.label = gameStrings.VOID_DREAMLAND_LEVEL_LABEL % (fromLv, toLv)
