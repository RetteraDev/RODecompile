#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/spriteChallengeRewardQueryProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from gamestrings import gameStrings
from guis.asObject import ASObject
from data import sprite_challenge_reward_floor_rank_query_reverse_data as SCRFRQRD
MAX_REWARDS_NUM = 16

class SpriteChallengeRewardQueryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SpriteChallengeRewardQueryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rank = None
        self.progress = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SPRITE_CHALLENGE_REWARD_QUERY, self.hide)

    def reset(self):
        self.rank = None
        self.progress = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SPRITE_CHALLENGE_REWARD_QUERY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SPRITE_CHALLENGE_REWARD_QUERY)

    def show(self, rank, progress):
        self.rank = rank
        self.progress = progress
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SPRITE_CHALLENGE_REWARD_QUERY)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.itemRenderer = 'SpriteChallengeRewardQuery_rewardItem'
        self.widget.scrollWndList.dataArray = []
        self.widget.scrollWndList.lableFunction = self.itemFunction
        self.widget.scrollWndList.itemHeightFunction = self.itemHeightFunction
        self.widget.scrollWndList.itemHeight = 40

    def itemHeightFunction(self, *args):
        itemData = ASObject(args[3][0])
        key = tuple(itemData.key)
        tReward = SCRFRQRD.data.get(self.rank, {}).get(key, {}).get('edsAwdItem', ())
        if len(tReward) > MAX_REWARDS_NUM / 2:
            return GfxValue(80)
        return GfxValue(40)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        key = tuple(itemData.key)
        rewardData = SCRFRQRD.data.get(self.rank, {})
        tReward = rewardData.get(key, {}).get('edsAwdItem', ())
        if key[1] == -1:
            progressText = gameStrings.VOID_DREAMLAND_DIFFLEVLE_BTN_LABEL_ABOVE % str(key[0])
        else:
            progressText = gameStrings.VOID_DREAMLAND_DIFFLEVLE_BTN_LABEL % ('%d-%d' % (key[0], key[1]))
        if itemData.bright:
            itemMc.rewardBright.visible = True
            itemMc.rewardDark.visible = False
            rewardItem = itemMc.rewardBright
        else:
            itemMc.rewardBright.visible = False
            itemMc.rewardDark.visible = True
            rewardItem = itemMc.rewardDark
        rewardItem.progressText.text = progressText
        for i in range(MAX_REWARDS_NUM):
            slot = rewardItem.getChildByName('slot%d' % i)
            if i < len(tReward):
                slot.visible = True
                slot.dragable = False
                tInfo = tReward[i]
                slot.setItemSlotData(uiUtils.getGfxItemById(tInfo[0], tInfo[1]))
            else:
                slot.visible = False

    def _onSureBtnClick(self, e):
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        indexPosY = 0
        itemList = []
        rewardData = SCRFRQRD.data.get(self.rank, {})
        for idx, key in enumerate(sorted(rewardData.keys())):
            itemInfo = {}
            itemInfo['key'] = key
            itemInfo['bright'] = False
            if self.progress >= key[0] and self.progress <= key[1] or self.progress >= key[0] and key[1] == -1:
                itemInfo['bright'] = True
                indexPosY = idx
            itemList.append(itemInfo)

        self.widget.scrollWndList.dataArray = itemList
        self.widget.scrollWndList.validateNow()
        pos = self.widget.scrollWndList.getIndexPosY(indexPosY)
        self.widget.scrollWndList.scrollTo(pos)
