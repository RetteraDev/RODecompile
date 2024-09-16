#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidDreamlandRewardQueryProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from gamestrings import gameStrings
from guis.asObject import ASObject
MAX_REWARDS_NUM = 16
from data import endless_challenge_reward_floor_rank_query_reverse_data as ECRFRQRD

class VoidDreamlandRewardQueryProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoidDreamlandRewardQueryProxy, self).__init__(uiAdapter)
        self.widget = None
        self.rank = None
        self.progress = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_DREAMLAND_REWARD_QUERY, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_DREAMLAND_REWARD_QUERY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self, rank, progress):
        self.rank = rank
        self.progress = progress
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_VOID_DREAMLAND_REWARD_QUERY)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VOID_DREAMLAND_REWARD_QUERY)

    def reset(self):
        self.rank = None
        self.progress = None

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.scrollWndList.itemRenderer = 'VoidDreamlandRewardQuery_rewardItem'
        self.widget.scrollWndList.dataArray = []
        self.widget.scrollWndList.lableFunction = self.itemFunction
        self.widget.scrollWndList.itemHeightFunction = self.itemHeightFunction
        self.widget.scrollWndList.itemHeight = 40

    def _onSureBtnClick(self, e):
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        indexPosY = 0
        itemList = []
        rewardData = ECRFRQRD.data.get(self.rank, {})
        for idx, key in enumerate(sorted(rewardData.keys())):
            tReward = rewardData.get(key, {}).get('edsAwdItem', ())
            if key[1] == -1:
                progressText = gameStrings.VOID_DREAMLAND_DIFFLEVLE_BTN_LABEL_ABOVE % str(key[0])
            else:
                progressText = gameStrings.VOID_DREAMLAND_DIFFLEVLE_BTN_LABEL % ('%d-%d' % (key[0], key[1]))
            itemInfo = {}
            itemInfo['index'] = idx
            itemInfo['progressText'] = progressText
            itemInfo['tReward'] = tReward
            itemInfo['bright'] = False
            if self.progress >= key[0] and self.progress <= key[1] or self.progress >= key[0] and key[1] == -1:
                itemInfo['bright'] = True
                indexPosY = idx
            itemList.append(itemInfo)

        self.widget.scrollWndList.dataArray = itemList
        self.widget.scrollWndList.validateNow()
        pos = self.widget.scrollWndList.getIndexPosY(indexPosY)
        self.widget.scrollWndList.scrollTo(pos)

    def itemHeightFunction(self, *args):
        data = ASObject(args[3][0])
        if len(data.tReward) > MAX_REWARDS_NUM / 2:
            return GfxValue(80)
        return GfxValue(40)

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        if itemData.bright:
            itemMc.rewardBright.visible = True
            itemMc.rewardDark.visible = False
            rewardItem = itemMc.rewardBright
        else:
            itemMc.rewardBright.visible = False
            itemMc.rewardDark.visible = True
            rewardItem = itemMc.rewardDark
        rewardItem.progressText.text = itemData.progressText
        for i in range(MAX_REWARDS_NUM):
            slot = rewardItem.getChildByName('slot%d' % i)
            if i < len(itemData.tReward):
                slot.visible = True
                slot.dragable = False
                tInfo = itemData.tReward[i]
                slot.setItemSlotData(uiUtils.getGfxItemById(tInfo[0], tInfo[1]))
            else:
                slot.visible = False
