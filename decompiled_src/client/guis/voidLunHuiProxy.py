#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidLunHuiProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import clientUtils
import gametypes
from guis.asObject import TipManager
from guis import tipUtils
from guis.asObject import MenuManager
from uiTabProxy import UITabProxy
from uiProxy import UIProxy
from guis import events
from guis.asObject import ASObject
from data import sys_config_data as SCD
from guis import voidLunHuiHelper
from gamestrings import gameStrings
from data import team_endless_config_data as TECD
from cdata import team_endless_reward_reverse_data as TERRD
from data import team_endless_reward_floor_query_reverse_data as TERFQRD
TAB_INDEX0 = 0
TAB_INDEX1 = 1
MAX_SLOT_NUM = 6
GRADE_SECTION = 70
MAX_DROP_REWARDS_NUM = 8
LEVEL_ITEM_HEIGHT = 80
MAX_FRIEND_RANK_NUM = 3
levelToStage = [gametypes.TEAM_ENDLESS_LV_69, gametypes.TEAM_ENDLESS_LV_79]

class VoidLunHuiProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(VoidLunHuiProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_LUNHUI, self.hide)

    def reset(self):
        super(VoidLunHuiProxy, self).reset()
        self.currSelectProgress = -1
        self.currSelectItem = None
        self.rewardInfo = {}

    def _getTabList(self):
        return [{'tabIdx': TAB_INDEX0,
          'tabName': 'tabSilver',
          'view': 'VoidLunHui_tabLevelMc',
          'pos': (3, 115)}, {'tabIdx': TAB_INDEX1,
          'tabName': 'tabGold',
          'view': 'VoidLunHui_tabLevelMc',
          'pos': (3, 115)}]

    def onTabChanged(self, *args):
        super(VoidLunHuiProxy, self).onTabChanged(*args)
        self.currentView.scrollWndList.scrollbar.addEventListener(events.SCROLL, self.handleScroll, False, 0, True)
        self.updateTabInfoMc()

    def onRewardQueryClick(self, *args):
        rank = levelToStage[self.currentTabIndex]
        gameglobal.rds.ui.voidLunHuiRewardQuery.show(rank, self.currSelectProgress)

    def onBackgroundClick(self, *args):
        gameglobal.rds.ui.ranking.show(gametypes.TOP_TYPE_TEAM_ENDLESS, isCommonRank=True)

    def onBeginGameClick(self, *args):
        p = BigWorld.player()
        rank = levelToStage[self.currentTabIndex]
        fbId = voidLunHuiHelper.getInstance().getThisWeekFbId(rank)
        p.base.inviteEnterTeamEndless(fbId, self.currSelectProgress)

    def onWeekBuffBtnClick(self, *args):
        rank = levelToStage[self.currentTabIndex]
        gameglobal.rds.ui.voidLunHuiCiZhui.show(rank)

    def getMyGradeTabIndex(self, lv):
        if lv < GRADE_SECTION:
            return TAB_INDEX0
        else:
            return TAB_INDEX1

    def handleScroll(self, *args):
        if self.widget:
            MenuManager.getInstance().hideMenu()

    def updateTabInfoMc(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.currSelectProgress = -1
        self.currentView.scrollWndList.itemRenderer = 'VoidLunHui_diffLevelItem'
        self.currentView.scrollWndList.itemHeight = LEVEL_ITEM_HEIGHT
        self.currentView.scrollWndList.dataArray = []
        self.currentView.scrollWndList.lableFunction = self.itemFunction
        self.currentView.beginGame.addEventListener(events.BUTTON_CLICK, self.onBeginGameClick)
        self.currentView.weekBuffBtn.addEventListener(events.BUTTON_CLICK, self.onWeekBuffBtnClick)
        self.currentView.rewardMc.rewardQuery.addEventListener(events.BUTTON_CLICK, self.onRewardQueryClick)
        lvKey = levelToStage[self.currentTabIndex]
        remainTime = voidLunHuiHelper.getInstance().getRemainRewardTime(lvKey)
        self.currentView.boxKeyNum.text = remainTime
        self.updatelevelItemData()
        tipText = TECD.data.get('teamEndlessRewardRemainTip', 'remain:%d')
        TipManager.addTip(self.currentView.keyIcon, tipText % remainTime)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_LUNHUI:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)
            self.refreshInfo()

    def clearWidget(self):
        super(VoidLunHuiProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VOID_LUNHUI)
        gameglobal.rds.sound.playSound(gameglobal.SD_5)

    def show(self):
        p = BigWorld.player()
        self.showTabIndex = self.getMyGradeTabIndex(p.lv)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_VOID_LUNHUI)
        else:
            self.widget.setTabIndex(self.showTabIndex)
        p.base.queryFriendTeamEndlessRank()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        self.widget.background.addEventListener(events.BUTTON_CLICK, self.onBackgroundClick)
        self.addEvent(events.EVENT_TEAMENDLESS_CHANGED, self.updateTabInfoMc)

    def isValidLevel(self, index):
        p = BigWorld.player()
        level = p.lv
        if level < 69:
            return False
        elif level == 69:
            return index == 0
        else:
            return index == 1

    def updatelevelItemData(self):
        self.challengeLevelItemList = []
        self.rewardInfo = self.getRewardInfo()
        key = levelToStage[self.currentTabIndex]
        maxProgress = voidLunHuiHelper.getInstance().getMaxProgress(key)
        currProgress = voidLunHuiHelper.getInstance().getCurrentProgress(key)
        availableLv = voidLunHuiHelper.getInstance().getAvailableLv(key)
        for i in range(maxProgress)[::-1]:
            itemInfo = {}
            level = i + 1
            finishState = voidLunHuiHelper.getInstance().getOnceRewardState(key, level)
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
                itemInfo['nextDiff'] = availableLv
                itemInfo['availableProgress'] = availableLv
            self.challengeLevelItemList.append(itemInfo)

        self.currentView.scrollWndList.dataArray = self.challengeLevelItemList
        self.currentView.scrollWndList.validateNow()
        if not self.isValidLevel(self.currentTabIndex):
            self.currentView.beginGame.enabled = False
        nextDiff = min(availableLv, maxProgress)
        indexPosY = max(maxProgress - nextDiff, 0)
        pos = self.currentView.scrollWndList.getIndexPosY(indexPosY)
        self.currentView.scrollWndList.scrollTo(pos)

    def onGetFriendTeamEndlessRank(self):
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
        diffLevelBtn.validateNow()
        diffLevelBtn.mouseChildren = True
        diffLevelBtn.diffIdx = itemData.diffIdx
        diffLevelBtn.label = gameStrings.VOID_DREAMLAND_DIFFLEVLE_BTN_LABEL % str(itemData.diffIdx)
        if itemData.showRewardBox:
            diffLevelBtn.rewardState.visible = True
            diffLevelBtn.rewardBoxState = itemData.finishState
            diffLevelBtn.rewardState.gotoAndStop('noneGet')
            diffLevelBtn.rewardState.addEventListener(events.MOUSE_CLICK, self.handleRewardBoxClick, False, 0, True)
            if itemData.finishState == gametypes.TEAM_ENDLESS_REWARD_STATE_ENABLE:
                diffLevelBtn.rewardState.gotoAndStop('canGet')
            elif itemData.finishState == gametypes.TEAM_ENDLESS_REWARD_STATE_TAKEN:
                diffLevelBtn.rewardState.gotoAndStop('alreadyGet')
        else:
            diffLevelBtn.rewardState.visible = False
        if diffLevelBtn.selected:
            self.currSelectProgress = itemData.diffIdx
            self.currSelectItem = diffLevelBtn
            self.updateDropRewardMc(itemData.diffIdx)
        self.setFriendsRankInfo(diffLevelBtn.playerList, lvKey, itemData.diffIdx)
        diffLevelBtn.addEventListener(events.MOUSE_DOWN, self.handleDiffLevelBtnClick, False, 0, True)

    def setFriendsRankInfo(self, listMc, lvKey, diffIdx):
        currProgress = voidLunHuiHelper.getInstance().getCurrentProgress(lvKey)
        p = BigWorld.player()
        playerList = []
        if diffIdx == currProgress:
            pInfo = {'name': p.roleName,
             'photo': p._getFriendPhoto(p)}
            playerList.append(pInfo)
        if hasattr(p, 'friendTeamEndlessRank'):
            gbIds = p.friendTeamEndlessRank.get(lvKey, {}).get(diffIdx, [])
            for gbId in gbIds:
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
        if rewardBoxState == gametypes.TEAM_ENDLESS_REWARD_STATE_DEFAULT:
            self.showRewardInfoTips(e.target, progress)
        elif rewardBoxState == gametypes.TEAM_ENDLESS_REWARD_STATE_ENABLE:
            p = BigWorld.player()
            p.base.takeTeamEndlessOnceReward(levelToStage[self.currentTabIndex], progress)

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
        rewardTipsPanel = self.widget.getInstByClsName('VoidLunHui_rewardTips')
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
        self.updateDropRewardMc(itemMc.diffIdx)

    def updateDropRewardMc(self, diffIdx):
        rewardMc = self.currentView.rewardMc
        rewardMc.diffText.text = diffIdx
        key = levelToStage[self.currentTabIndex]
        data = TERFQRD.data.get((key, diffIdx), {})
        if not data:
            data = TERFQRD.data.get((key, -1), {})
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
        key = levelToStage[self.currentTabIndex]
        return TERRD.data.get(key, {})

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshTabName()

    def refreshTabName(self):
        fromLv = 70
        toLv = 79
        if gameglobal.rds.configData.get('enableNewLv89', False):
            toLv = 89
        self.widget.tabGold.label = gameStrings.SRPTIE_CHALLENGE_TAB_NAME % (fromLv, toLv)
