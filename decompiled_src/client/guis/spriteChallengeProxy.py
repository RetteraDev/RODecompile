#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spriteChallengeProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
import gametypes
from uiTabProxy import UITabProxy
from guis.asObject import MenuManager
from guis.asObject import ASObject
from guis.asObject import TipManager
from gamestrings import gameStrings
from guis import events
from guis import spriteChallengeHelper
from guis import tipUtils
from guis import uiUtils
import clientUtils
from cdata import sprite_challenge_reward_reverse_data as SCRRD
from data import sprite_challenge_reward_floor_query_reverse_data as SCRFQRD
from data import sprite_challenge_config_data as SCCD
from data import state_data as SD
from guis.asObject import ASUtils
TAB_INDEX0 = 0
TAB_INDEX1 = 1
MAX_SLOT_NUM = 6
LEVEL_ITEM_HEIGHT = 80
levelToStage = [gametypes.SPRITE_CHALLENGE_LV_45, gametypes.SPRITE_CHALLENGE_LV_79]
GRADE_SECTION = 70
MAX_FRIEND_RANK_NUM = 3
MAX_DROP_REWARDS_NUM = 8

class SpriteChallengeProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(SpriteChallengeProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPRITE_CHALLENGE, self.hide)

    def reset(self):
        super(SpriteChallengeProxy, self).reset()
        self.currSelectProgress = -1
        self.currSelectItem = None
        self.rewardInfo = {}

    def _getTabList(self):
        return [{'tabIdx': TAB_INDEX0,
          'tabName': 'tabSilver',
          'view': 'SpriteChallenge_tabLevelMc',
          'pos': (3, 115)}, {'tabIdx': TAB_INDEX1,
          'tabName': 'tabGold',
          'view': 'SpriteChallenge_tabLevelMc',
          'pos': (3, 115)}]

    def onTabChanged(self, *args):
        super(SpriteChallengeProxy, self).onTabChanged(*args)
        self.currentView.scrollWndList.scrollbar.addEventListener(events.SCROLL, self.handleScroll, False, 0, True)
        self.updateTabInfoMc()
        self.queryServerInfo()

    def refreshTabEnabled(self):
        pass

    def onRewardQueryClick(self, *args):
        gameglobal.rds.ui.spriteChallengeRewardQuery.show(levelToStage[self.currentTabIndex], self.currSelectProgress)

    def onRankBtnClick(self, *args):
        gameglobal.rds.ui.ranking.show(gametypes.TOP_TYPE_SPRITE_CHALLENGE, isCommonRank=True)

    def onBeginGameClick(self, *args):
        selectProgress = self.currSelectProgress
        if self.currSelectProgress == -1:
            selectProgress = spriteChallengeHelper.getInstance().getAvailableLv(spriteChallengeHelper.getInstance().getSelfLvKey())
        gameglobal.rds.ui.spriteChallengeSelect.show(selectProgress, True)

    def onRankRewardBtnClick(self, *args):
        gameglobal.rds.ui.spriteChallengeReward.show()

    def handleScroll(self, *args):
        if self.widget:
            MenuManager.getInstance().hideMenu()

    def getMyGradeTabIndex(self):
        index = levelToStage.index(spriteChallengeHelper.getInstance().getSelfLvKey())
        if index >= 0:
            return index
        return 0

    def updateTabInfoMc(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.currSelectProgress = -1
        self.currentView.scrollWndList.itemRenderer = 'SpriteChallenge_diffLevelItem'
        self.currentView.scrollWndList.itemHeight = LEVEL_ITEM_HEIGHT
        self.currentView.scrollWndList.dataArray = []
        self.currentView.scrollWndList.lableFunction = self.itemFunction
        self.currentView.beginGame.addEventListener(events.BUTTON_CLICK, self.onBeginGameClick)
        self.currentView.rankRewardBtn.addEventListener(events.BUTTON_CLICK, self.onRankRewardBtnClick)
        self.currentView.rewardMc.rewardQuery.addEventListener(events.BUTTON_CLICK, self.onRewardQueryClick)
        self.refreshRemainRewardTime()
        self.updatelevelItemData()

    def refreshRemainRewardTime(self):
        if not self.widget:
            return
        lvKey = levelToStage[self.currentTabIndex]
        remainTime = spriteChallengeHelper.getInstance().getRemainRewardTime()
        self.currentView.boxKeyNum.text = remainTime
        tipText = SCCD.data.get('SpriteChallengeRewardRemainTip', 'remain:%d')
        TipManager.addTip(self.currentView.keyIcon, tipText % remainTime)
        gameglobal.rds.ui.spriteChallengeResult.refreshRewardMc()
        gameglobal.rds.ui.spriteChallengeResult.refreshBoxState()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SPRITE_CHALLENGE:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(SpriteChallengeProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SPRITE_CHALLENGE)
        gameglobal.rds.sound.playSound(gameglobal.SD_5)

    def show(self):
        self.showTabIndex = self.getMyGradeTabIndex()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SPRITE_CHALLENGE)
        else:
            self.refreshInfo()

    def queryServerInfo(self):
        p = BigWorld.player()
        lvKey = levelToStage[self.currentTabIndex]
        lvKeyStr = spriteChallengeHelper.getInstance().getLvKeyStrByLvType(lvKey)
        p.base.querySpriteChallengeInfo(lvKeyStr)
        p.base.getLastSpriteList()
        spriteChallengeHelper.getInstance().queryBonusInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        self.widget.rankBtn.addEventListener(events.BUTTON_CLICK, self.onRankBtnClick)
        self.addEvent(events.EVENT_SPRITE_CHALLENGE_CHANGED, self.updateTabInfoMc)
        self.initTabIndex()

    def isValidLevel(self, index):
        lvKey = levelToStage[index]
        p = BigWorld.player()
        level = p.lv
        endlessAvailableLv = SCCD.data.get('spriteChallengeAvailableLv', {})
        lvRange = endlessAvailableLv.get(lvKey)
        if lvRange[0] <= level <= spriteChallengeHelper.getInstance().convertMaxLv(lvRange[1]):
            return True
        return False

    def updatelevelItemData(self):
        self.challengeLevelItemList = []
        self.rewardInfo = self.getRewardInfo()
        key = levelToStage[self.currentTabIndex]
        maxProgress = spriteChallengeHelper.getInstance().getMaxShowProgress(key)
        currProgress = spriteChallengeHelper.getInstance().getCurrentProgress(key)
        availableLv = spriteChallengeHelper.getInstance().getAvailableLv(key)
        for i in range(maxProgress)[::-1]:
            itemInfo = {}
            level = i + 1
            finishState = spriteChallengeHelper.getInstance().getOnceRewardState(key, level)
            itemInfo['diffIdx'] = level
            itemInfo['finishState'] = finishState
            if level in self.rewardInfo:
                itemInfo['showRewardBox'] = True
            else:
                itemInfo['showRewardBox'] = False
            if self.isValidLevel(self.currentTabIndex):
                itemInfo['nextDiff'] = availableLv
                itemInfo['availableProgress'] = availableLv
            else:
                itemInfo['nextDiff'] = currProgress
                itemInfo['availableProgress'] = currProgress
            self.challengeLevelItemList.append(itemInfo)

        self.currentView.scrollWndList.dataArray = self.challengeLevelItemList
        self.currentView.scrollWndList.validateNow()
        if not self.isValidLevel(self.currentTabIndex):
            self.currentView.beginGame.enabled = False
        nextDiff = min(availableLv, maxProgress)
        indexPosY = max(maxProgress - nextDiff, 0)
        pos = self.currentView.scrollWndList.getIndexPosY(indexPosY)
        self.currentView.scrollWndList.scrollTo(pos)

    def onGetFriendSpriteChallengeRank(self):
        if not self.widget:
            return
        self.currentView.scrollWndList.dataArray = self.challengeLevelItemList
        self.currentView.scrollWndList.validateNow()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        lvKey = levelToStage[self.currentTabIndex]
        isEnable = itemData.availableProgress >= itemData.diffIdx and self.isValidLevel(self.currentTabIndex)
        itemMc.diffLevelBtnNormal.visible = isEnable
        itemMc.diffLevelBtnDisable.visible = not isEnable
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
        buffId = spriteChallengeHelper.getInstance().getBuffByDiffIdx(lvKey, itemData.diffIdx)
        if not buffId:
            diffLevelBtn.buffIcon.visible = False
        else:
            cfg = SD.data.get(buffId, {})
            iconId = cfg.get('iconId', 'notFound')
            iconPath = 'state/22/%s.dds' % iconId
            diffLevelBtn.buffIcon.fitSize = True
            diffLevelBtn.buffIcon.loadImage(iconPath)
            diffLevelBtn.buffIcon.visible = True
            TipManager.addTipByType(diffLevelBtn.buffIcon, tipUtils.TYPE_BUFF, buffId, False, 'upLeft')
        diffLevelBtn.validateNow()
        diffLevelBtn.mouseChildren = True
        diffLevelBtn.diffIdx = itemData.diffIdx
        diffLevelBtn.label = gameStrings.VOID_DREAMLAND_DIFFLEVLE_BTN_LABEL % str(itemData.diffIdx)
        if itemData.showRewardBox:
            diffLevelBtn.rewardState.visible = True
            diffLevelBtn.rewardBoxState = itemData.finishState
            if itemData.finishState == gametypes.SPRITE_CHALLENGE_STATE_ENABLE:
                diffLevelBtn.rewardState.gotoAndStop('canGet')
            elif itemData.finishState == gametypes.SPRITE_CHALLENGE_STATE_DEFAULT:
                diffLevelBtn.rewardState.gotoAndStop('noneGet')
            else:
                diffLevelBtn.rewardState.gotoAndStop('alreadyGet')
            diffLevelBtn.rewardState.addEventListener(events.MOUSE_CLICK, self.handleRewardBoxClick, False, 0, True)
        else:
            diffLevelBtn.rewardState.visible = False
        if diffLevelBtn.selected:
            self.currSelectProgress = itemData.diffIdx
            self.currSelectItem = diffLevelBtn
            self.updateDropRewardMc(itemData.diffIdx)
        self.setFriendsRankInfo(diffLevelBtn.playerList, lvKey, itemData.diffIdx)
        diffLevelBtn.addEventListener(events.MOUSE_DOWN, self.handleDiffLevelBtnClick, False, 0, True)

    def setFriendsRankInfo(self, listMc, lvKey, diffIdx):
        currProgress = spriteChallengeHelper.getInstance().getCurrentProgress(lvKey)
        p = BigWorld.player()
        playerList = []
        if diffIdx == currProgress:
            pInfo = {'name': p.roleName,
             'photo': p._getFriendPhoto(p)}
            playerList.append(pInfo)
        gbIds = spriteChallengeHelper.getInstance().getFriendRankGbIds(lvKey, diffIdx)
        for gbId in gbIds:
            if gbId == p.gbId:
                continue
            friendVal = p.friend.get(gbId)
            if friendVal:
                info = {'name': friendVal.name,
                 'photo': p._getFriendPhoto(friendVal)}
                playerList.append(info)

        for i in xrange(MAX_FRIEND_RANK_NUM):
            playerMc = listMc.getChildByName('playerIcon%d' % i)
            if i < len(playerList):
                info = playerList[i]
                name = info.get('name', '')
                photo = info.get('photo', '')
                if uiUtils.isDownloadImage(photo):
                    playerMc.icon.imgType = uiConst.IMG_TYPE_NOS_FILE
                    playerMc.icon.fitSize = True
                    playerMc.icon.setContentUnSee()
                    playerMc.icon.url = photo
                else:
                    playerMc.icon.clear()
                    playerMc.icon.fitSize = True
                    playerMc.icon.loadImage(photo)
                playerMc.visible = True
                TipManager.addTip(playerMc, name, tipUtils.TYPE_DEFAULT_BLACK)
            else:
                playerMc.visible = False

    def handleRewardBoxClick(self, *args):
        e = ASObject(args[3][0])
        rewardBoxState = e.currentTarget.parent.rewardBoxState
        progress = e.currentTarget.parent.diffIdx
        if rewardBoxState == gametypes.SPRITE_CHALLENGE_STATE_DEFAULT:
            self.showRewardInfoTips(e.target, progress)
        elif rewardBoxState == gametypes.SPRITE_CHALLENGE_STATE_ENABLE:
            p = BigWorld.player()
            p.base.getSpriteChallengeProgressReward(spriteChallengeHelper.getInstance().getLvKeyStrByLvType(levelToStage[self.currentTabIndex]), progress)

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
        rewardTipsPanel = self.widget.getInstByClsName('SpriteChallenge_rewardTips')
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

    def handleDiffLevelBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        btnName = e.currentTarget.name
        if btnName == 'diffLevelBtnNormal':
            self.currentView.beginGame.enabled = True
        elif btnName == 'diffLevelBtnDisable':
            self.currentView.beginGame.enabled = False
        if not self.isValidLevel(self.currentTabIndex):
            self.currentView.beginGame.enabled = False
        if self.currSelectProgress == itemMc.diffIdx:
            return
        if self.currSelectItem:
            self.currSelectItem.selected = False
        self.currSelectProgress = itemMc.diffIdx
        self.currSelectItem = itemMc
        itemMc.selected = True

    def updateDropRewardMc(self, diffIdx):
        rewardMc = self.currentView.rewardMc
        rewardMc.diffText.text = diffIdx
        key = levelToStage[self.currentTabIndex]
        data = SCRFQRD.data.get((key, diffIdx), {})
        if not data:
            data = SCRFQRD.data.get((key, -1), {})
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

    def getRewardInfo(self):
        key = self.getRewardKey()
        return SCRRD.data.get(key, {})

    def getRewardKey(self):
        return (spriteChallengeHelper.getInstance().getCurrentSeasonLocal(levelToStage[self.currentTabIndex]), levelToStage[self.currentTabIndex])

    def refreshTabName(self):
        lvKeyStr = spriteChallengeHelper.getInstance().getLvKeyStrByLvType(levelToStage[0])
        fromLv, toLv = lvKeyStr.split('_')
        self.widget.tabSilver.label = gameStrings.SRPTIE_CHALLENGE_TAB_NAME % (fromLv, toLv)
        lvKeyStr = spriteChallengeHelper.getInstance().getLvKeyStrByLvType(levelToStage[1])
        fromLv, toLv = lvKeyStr.split('_')
        if gameglobal.rds.configData.get('enableNewLv89', False):
            toLv = 89
        self.widget.tabGold.label = gameStrings.SRPTIE_CHALLENGE_TAB_NAME % (fromLv, toLv)

    def initTabIndex(self):
        if self.currentTabIndex < 0:
            self.widget.setTabIndex(self.getMyGradeTabIndex())

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshTabName()
        self.updateTabInfoMc()
        self.refreshTabEnabled()
