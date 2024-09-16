#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rewardRecoveryDiKouProxy.o
import BigWorld
import uiConst
import events
import gamelog
import gametypes
from gamestrings import gameStrings
from callbackHelper import Functor
from uiProxy import UIProxy
from guis import uiUtils
from guis import ui
from guis.asObject import ASUtils
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import reward_getback_data as RGD
from data import item_data as ID
TEXT_COLOR_RED = '#F43804'

class RewardRecoveryDiKouProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RewardRecoveryDiKouProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_REWARD_RECOVERY_DIKOU, self.hide)

    def reset(self):
        self.itemData = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_REWARD_RECOVERY_DIKOU:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_REWARD_RECOVERY_DIKOU)

    def show(self, itemData):
        if not itemData:
            return
        self.itemData = itemData
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_REWARD_RECOVERY_DIKOU)

    def initUI(self):
        p = BigWorld.player()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if not self.itemData.activityId:
            self.hide()
            return
        activityId = int(self.itemData['activityId'])
        configData = RGD.data.get(activityId, {})
        diKouItemId = configData.get('rewardGetBackConsumeItem', 0)
        itemName = ID.data.get(diKouItemId, {}).get('name', '')
        itemCount = p.inv.countItemInPages(diKouItemId, enableParentCheck=True)
        consumeCoin = self.itemData['originPrice']
        itemCount = min(consumeCoin, itemCount)
        realConsumeCoin = max(0, consumeCoin - itemCount)
        self.widget.itemSlot.setItemSlotData(uiUtils.getGfxItemById(diKouItemId))
        self.widget.itemSlot.validateNow()
        countDesc = '%d/%d' % (int(itemCount), int(consumeCoin))
        if realConsumeCoin:
            self.widget.txtDesc.htmlText = gameStrings.BAIDI_SHILIAN_DIKOU_NOT_ENOUGH % (itemName, realConsumeCoin)
            countDesc = uiUtils.toHtml(countDesc, TEXT_COLOR_RED)
        else:
            self.widget.txtDesc.htmlText = gameStrings.BAIDI_SHILIAN_DIKOU % (itemName, consumeCoin)
        self.widget.itemSlot.setValueAmountTxt(countDesc)
        ASUtils.autoSizeWithFont(self.widget.itemSlot.valueAmount, 14, self.widget.itemSlot.valueAmount.textWidth, 8)
        self.widget.cost.visible = False
        self.widget.txtDiKouDesc.text = gameStrings.BAIDI_SHILIAN_DIKOU_DESC % itemName
        self.widget.yesBtn.addEventListener(events.BUTTON_CLICK, self.handleYesBtnClick, False, 0, True)
        self.widget.noBtn.addEventListener(events.BUTTON_CLICK, self.handleNoBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    @ui.checkInventoryLock()
    def handleYesBtnClick(self, *args):
        if not self.widget.cost.visible:
            self.doGetReward()
        else:
            realConsumeCoin = int(self.widget.cost.txtValue.text)
            msg = GMD.data.get(GMDD.data.REWARD_RECOVERY_CONFIRM, {}).get('text', '%d') % realConsumeCoin
            self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.doGetReward)

    def doGetReward(self):
        if not self.itemData:
            return
        if not self.itemData['activityType'] == gametypes.REWARD_RECOVER_ACTIVITY_TYPE_XUN_LING:
            gamelog.info('jbx:getBackActivityRewardEx', int(self.itemData['activityId']), gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME2)
            fun = Functor(BigWorld.player().base.getBackActivityRewardEx, int(self.itemData['activityId']), gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_COIN)
            self.uiAdapter.welfareRewardRecovery.getBackActivityReward(fun, self.itemData)
        else:
            fun = Functor(BigWorld.player().cell.getBackQuestLoopChainExp, gametypes.QUEST_LOOP_CHAIN_GET_BACK_EXP_TYPE_COIN)
            self.uiAdapter.welfareRewardRecovery.getBackActivityReward(fun, self.itemData)
        self.hide()

    def handleNoBtnClick(self, *args):
        self.hide()
