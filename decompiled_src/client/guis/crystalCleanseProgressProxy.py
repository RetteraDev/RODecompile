#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/crystalCleanseProgressProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from guis import uiUtils
from gamestrings import gameStrings
import clientUtils
from cdata import hand_in_item_crystal_data as HIICD
CLEANSE_REWARD_ALL_NUMS = 4

class CrystalCleanseProgressProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CrystalCleanseProgressProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CRYSTAL_CLEANSE_PROGRESS, self.hide)

    def reset(self):
        self.activityID = 0
        self.HIID_ID = 0
        self.HIICD_ID = 0
        self.helpID = 0
        self.curPersonAllSubmitNums = 0
        self.personAllSubmitNumsLimit = 0
        self.curAllRounds = 0
        self.allRounds = 0
        self.hasGotReward = False
        self.bonusID = []
        self.hintTxt = ''

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CRYSTAL_CLEANSE_PROGRESS:
            self.widget = widget
            self.initUIData()
            self.initUI()

    def initUIData(self):
        allData = HIICD.data.get(self.HIICD_ID, {})
        self.bonusID = allData.get('bonus', ())
        name = allData.get('name', ())
        hintStr = gameglobal.rds.ui.crystalDefenceMain.getDescFromCID(self.HIID_ID, 'cleanseProgressHint')
        if hintStr:
            self.hintTxt = hintStr % name

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CRYSTAL_CLEANSE_PROGRESS)

    def show(self, data):
        if not self.widget:
            self.activityID = data['actID']
            self.HIID_ID = data['HIID_ID']
            self.HIICD_ID = data['HIICD_ID']
            self.helpID = data['helpID']
            self.curPersonAllSubmitNums = data['curSubmitNums']
            self.personAllSubmitNumsLimit = data['handInTotalRewardLimit']
            self.curAllRounds = data['curAllRounds']
            self.allRounds = data['allRounds']
            self.hasGotReward = data['hasGotReward']
            self.uiAdapter.loadWidget(uiConst.WIDGET_CRYSTAL_CLEANSE_PROGRESS)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.helpBtn.helpKey = self.helpID
        self.widget.helpBtn.textField.visible = False
        self.widget.title.text = gameglobal.rds.ui.crystalDefenceMain.getDescFromCID(self.HIID_ID, 'crystalCleanseProgressTitle')
        self.widget.hint.text = self.hintTxt
        self.widget.personSubmitAllNums.visible = True
        self.widget.personSubmitAllNums.htmlText = gameglobal.rds.ui.crystalDefenceMain.getDescFromCID(self.HIID_ID, 'crystalCleanseGetRewardHint') % (str(self.curPersonAllSubmitNums) + '/' + str(self.personAllSubmitNumsLimit))
        if self.hasGotReward == 1:
            self.widget.getRewardBtn.enabled = False
            self.widget.getRewardBtn.label = gameStrings.HAVE_GOT_REWARD
        elif self.hasGotReward == 0:
            if self.curAllRounds >= self.allRounds and self.curPersonAllSubmitNums >= self.personAllSubmitNumsLimit:
                self.widget.getRewardBtn.enabled = True
                self.widget.getRewardBtn.label = gameStrings.GET_REWARD
                self.widget.getRewardBtn.addEventListener(events.BUTTON_CLICK, self.handleClickGetRewardBtn, False, 0, True)
            else:
                self.widget.getRewardBtn.enabled = False
                self.widget.getRewardBtn.label = gameStrings.UNABLE_TO_GET_REWARD
        elif self.hasGotReward == -1:
            self.widget.getRewardBtn.enabled = False
            self.widget.getRewardBtn.label = gameStrings.UNABLE_TO_GET_REWARD
        self.widget.submitProgressBar.currentValue = self.curAllRounds
        self.widget.submitProgressBar.maxValue = self.allRounds
        for index in xrange(CLEANSE_REWARD_ALL_NUMS):
            rewardItemMC = getattr(self.widget, 'reward%d' % index)
            if rewardItemMC:
                rewardItemMC.dragable = False
                rewardItemMC.visible = False

        rewardMcIdx = 0
        itemDataList = clientUtils.genItemBonus(self.bonusID)
        for itemData in itemDataList:
            if rewardMcIdx < CLEANSE_REWARD_ALL_NUMS:
                itemId = itemData[0]
                itemCount = itemData[1]
                rewardItemMC = getattr(self.widget, 'reward%d' % rewardMcIdx)
                if rewardItemMC:
                    rewardMcIdx += 1
                    rewardItemMC.visible = True
                    rewardItemMC.setItemSlotData(uiUtils.getGfxItemById(itemId, count=itemCount))

    def handleClickGetRewardBtn(self, *args):
        if self.hasGotReward:
            content = gameglobal.rds.ui.crystalDefenceMain.getDescFromCID(self.HIID_ID, 'crystalCleanseHasGotMsg')
            BigWorld.player().showTopMsg(content)
        elif self.curPersonAllSubmitNums < self.personAllSubmitNumsLimit:
            content = gameglobal.rds.ui.crystalDefenceMain.getDescFromCID(self.HIID_ID, 'crystalCleanseSubmitLimitMsg')
            BigWorld.player().showTopMsg(content)
        else:
            p = BigWorld.player()
            p.base.getHandInItemTotalRoundReward(self.activityID, self.HIICD_ID)

    def refreshForGetReward(self, actID, HIICD_ID):
        if self.activityID == actID and self.HIICD_ID == HIICD_ID:
            self.hasGotReward = 1
            self.initUI()

    def showHelpByKey(self, helpKeyId):
        gameglobal.rds.ui.showHelpByKey(helpKeyId)
