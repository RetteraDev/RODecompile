#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rankingAwardPreviewProxy.o
import BigWorld
import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from data import sys_config_data as SCD

class RankingAwardPreviewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RankingAwardPreviewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANKING_AWARD_PREVIEW, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RANKING_AWARD_PREVIEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RANKING_AWARD_PREVIEW)

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_RANKING_AWARD_PREVIEW)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.awardView.itemRenderer = 'RankingAwardPreview_RankAwardItem'
        self.widget.awardView.dataArray = []
        self.widget.awardView.lableFunction = self.itemFunction

    def refreshInfo(self):
        if not self.widget:
            return
        rewardList = SCD.data.get('guildAuctionRewardView', [])
        itemList = []
        for i in xrange(len(rewardList)):
            itemInfo = {}
            itemInfo['num'] = i
            itemInfo['desc'] = rewardList[i]['titleName']
            itemInfo['itemId'] = rewardList[i]['rewardId']
            itemInfo['itemNum'] = rewardList[i]['num']
            itemList.append(itemInfo)

        self.widget.awardView.dataArray = itemList
        self.widget.awardView.validateNow()

    def itemFunction(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        itemMc.num.gotoAndStop('type_%d' % (itemData.num + 1))
        itemMc.desc.text = itemData.desc
        itemInfo = uiUtils.getGfxItemById(itemData.itemId, itemData.itemNum)
        itemMc.rewardIcon.slot.setItemSlotData(itemInfo)
