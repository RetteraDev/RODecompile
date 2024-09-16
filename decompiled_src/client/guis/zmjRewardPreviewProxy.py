#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zmjRewardPreviewProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import clientUtils
from asObject import ASObject
from uiProxy import UIProxy
from data import zmj_fuben_config_data as ZFCD
from data import mail_template_data as MTD
from cdata import top_reward_data as TRD
ZMJ_TOP_REWARD_KEY = (117, 0, 0)
SLOT_NUM_MAX = 5

class ZmjRewardPreviewProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ZmjRewardPreviewProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ZMJ_REWARD_PREVIEW, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ZMJ_REWARD_PREVIEW:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZMJ_REWARD_PREVIEW)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ZMJ_REWARD_PREVIEW)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.rewardList.column = 1
        self.widget.rewardList.itemHeight = 50
        self.widget.rewardList.itemRenderer = 'ZmjRewardPreview_DataItem'
        self.widget.rewardList.labelFunction = self.rewardItemFunc
        self.widget.rewardList.dataArray = []

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.rewardList.dataArray = self.genRewardListData()
        self.widget.rewardList.validateNow()

    def genRewardListData(self):
        topRewardData = TRD.data.get(ZMJ_TOP_REWARD_KEY, [])
        listData = []
        for rData in topRewardData:
            name = rData.get('desc', '')
            mailTemplateId = rData.get('mailTemplateId', '')
            itemIds = self.getMailBonusItemIds(mailTemplateId)
            info = {'desc': rData.get('desc', ''),
             'bonus': itemIds}
            listData.append(info)

        rewardData = ZFCD.data.get('highFbTotalMaxDmgRewardsNotInTop', [])
        for ratio, lowRank, highRank, dmgFix, mailId, mailStr in rewardData:
            itemIds = self.getMailBonusItemIds(mailId)
            info = {'desc': mailStr,
             'bonus': itemIds}
            listData.append(info)

        return listData

    def getMailBonusItemIds(self, mailId):
        bonusId = MTD.data.get(mailId, {}).get('bonusId', 0)
        itemIds = clientUtils.genItemBonus(bonusId)
        return itemIds

    def rewardItemFunc(self, *arg):
        info = ASObject(arg[3][0])
        itemMc = ASObject(arg[3][1])
        if itemMc and info:
            itemMc.descTxt.text = info.desc
            for i in xrange(SLOT_NUM_MAX):
                slot = getattr(itemMc, 'slot' + str(i), None)
                slot.visible = False

            for i, (itemId, num) in enumerate(info.bonus):
                slot = getattr(itemMc, 'slot' + str(i), None)
                itemInfo = uiUtils.getGfxItemById(itemId, num)
                slot.slot.setItemSlotData(itemInfo)
                slot.slot.dragable = False
                slot.visible = True
