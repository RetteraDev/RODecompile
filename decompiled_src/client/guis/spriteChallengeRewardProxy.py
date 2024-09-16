#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spriteChallengeRewardProxy.o
import BigWorld
import gameglobal
import uiConst
import clientUtils
from guis.asObject import ASObject
from guis import events
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis import spriteChallengeHelper
from guis import uiUtils
from cdata import top_reward_data as TRD
from data import mail_template_data as MTD
TAB_WEEK = 0
TAB_SEASON = 1
MAX_REWARD_ITEM_NUM = 6
DAY_HOURS = 24
HOUR_SECONDS = 3600

class SpriteChallengeRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SpriteChallengeRewardProxy, self).__init__(uiAdapter)
        self.widget = None
        self.currentTab = TAB_WEEK
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPRITE_CHALLENGE_REWARD, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SPRITE_CHALLENGE_REWARD:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SPRITE_CHALLENGE_REWARD)
        self.currentTab = TAB_WEEK

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SPRITE_CHALLENGE_REWARD)
        self.queryServerInfo()

    def queryServerInfo(self):
        p = BigWorld.player()
        p.base.getSpriteChallengeTopRank()
        p.base.getWeekSpriteChallengeTopRank()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.rewardList.itemRenderer = 'SpriteChallengeReward_rewardItem'
        self.widget.rewardList.labelFunction = self.rewardItemLabelFunc
        self.widget.tab0.addEventListener(events.EVENT_SELECT, self.onTabBtnSelected)
        self.widget.tab1.addEventListener(events.EVENT_SELECT, self.onTabBtnSelected)

    def rewardItemLabelFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        p = BigWorld.player()
        if self.currentTab == TAB_WEEK:
            rank = getattr(p, 'spriteChallengeWeekTopRank', 0)
        else:
            rank = getattr(p, 'spriteChallengeTopRank', 0)
        if itemData.rankRange[0] <= rank <= itemData.rankRange[1]:
            itemMc.gotoAndStop('over')
        else:
            itemMc.gotoAndStop('up')
        itemMc.rank.text = itemData.desc
        rewardList = self.getItemListByMailId(itemData.mailTemplateId)
        for i in xrange(MAX_REWARD_ITEM_NUM):
            rewardMc = itemMc.getChildByName('item%d' % i)
            if i < len(rewardList):
                itemId, itemNum = rewardList[i]
                rewardMc.visible = True
                rewardMc.slot.dragable = False
                rewardMc.slot.setItemSlotData(uiUtils.getGfxItemById(int(itemId), count=itemNum))
            else:
                rewardMc.visible = False

    def getItemListByMailId(self, mailId):
        mailInfo = MTD.data.get(mailId, {})
        bonusId = mailInfo.get('bonusId', 0)
        if bonusId:
            return clientUtils.genItemBonus(bonusId)
        return []

    def onTabBtnSelected(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget.selected:
            tabIndex = int(e.currentTarget.name[-1])
            if self.currentTab != tabIndex:
                self.currentTab = tabIndex
                self.refreshInfo()

    def refreshRank(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if self.currentTab == TAB_WEEK:
            rankTip = gameStrings.SPRITE_CHALLENGE_RANK_WEEK_TIP
            rank = getattr(p, 'spriteChallengeWeekTopRank', 0)
        else:
            rankTip = gameStrings.SPRITE_CHALLENGE_RANK_SEASON_TIP
            rank = getattr(p, 'spriteChallengeTopRank', 0)
        if gameglobal.rds.configData.get('enableSpriteChallengeUnRealRank', False):
            rankText = spriteChallengeHelper.getInstance().getFakeRankStr(rank)
        else:
            rankText = rank if rank else ''
        if not rankText:
            rankText = gameStrings.WING_WORLD_XINMO_RANK_SELF_INFO_NO_INFO
        self.widget.myRank.text = gameStrings.SPRITE_CHALLENGE_RANK_TEXT % rankText
        self.widget.tip.text = rankTip

    def refreshInfo(self):
        if not self.widget:
            return
        if self.currentTab == TAB_WEEK:
            self.widget.tab0.selected = True
        else:
            self.widget.tab1.selected = True
        if not spriteChallengeHelper.getInstance().inSpriteChallengeSeason():
            self.widget.myRank.visible = False
            self.widget.timeArea.visible = False
        else:
            self.widget.timeArea.visible = True
            self.widget.myRank.visible = True
            self.refreshTime()
            self.refreshRank()
        self.refreshRewards()

    def refreshTime(self):
        if self.currentTab == TAB_WEEK:
            self.widget.timeArea.timeTitle.text = gameStrings.SPRITE_CHALLENGE_WEEK_TITLE
            leftTime = spriteChallengeHelper.getInstance().getWeekRewardLeftTime()
            self.refreshLeftTime(leftTime)
        else:
            self.widget.timeArea.timeTitle.text = gameStrings.SPRITE_CHALLENGE_SEASON_TITLE
            leftTime = spriteChallengeHelper.getInstance().getSeasonRewardLeftTime()
            self.refreshLeftTime(leftTime)

    def refreshRewards(self):
        if self.currentTab == TAB_SEASON:
            awardKey = spriteChallengeHelper.getInstance().getSeasonAwardKey()
        else:
            awardKey = spriteChallengeHelper.getInstance().getWeekAwardKey()
        rewardInfo = TRD.data.get(awardKey, [])
        if not gameglobal.rds.configData.get('enableSpriteChallengeUnRealRank', False):
            if self.currentTab == TAB_WEEK:
                rewardInfo = rewardInfo[:4]
        self.widget.rewardList.dataArray = rewardInfo

    def refreshLeftTime(self, leftTime):
        if not self.widget:
            return
        hourLeft = int(leftTime / HOUR_SECONDS) + 1
        dayLeft = int(hourLeft / DAY_HOURS)
        hourLeft = int(hourLeft % DAY_HOURS)
        self.widget.timeArea.dayText.text = dayLeft
        self.widget.timeArea.hourText.text = hourLeft
