#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fightForLoveApplyProxy.o
import BigWorld
import events
import gametypes
import const
import gameglobal
import uiConst
import ui
from guis import uiUtils
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import fight_for_love_config_data as FFLCD
from cdata import item_fame_score_cost_data as IFSCD

class FightForLoveApplyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FightForLoveApplyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FIGHT_FOR_LOVE_APPLY, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FIGHT_FOR_LOVE_APPLY:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FIGHT_FOR_LOVE_APPLY)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FIGHT_FOR_LOVE_APPLY)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        bannerName = ''.join(('fightforlove/', FFLCD.data.get('bannerImage', ''), '.dds'))
        self.widget.bannerImage.fitSize = True
        self.widget.bannerImage.loadImage(bannerName)
        self.widget.descContent.htmlText = FFLCD.data.get('activityDesc', '')
        self.widget.ruleContent.htmlText = FFLCD.data.get('activityRule', '')
        startCron = FFLCD.data.get('startCrons', '')
        endCrons = FFLCD.data.get('endCrons', '')
        self.widget.moneyIcon.bonusType = 'yunChui'
        self.widget.dikouCheckBox.selected = True
        self.widget.dikouCheckBox.addEventListener(events.EVENT_SELECT, self.handleSelectCheckBtn, False, 0, True)
        seekId = FFLCD.data.get('npcSeekId', '')
        self.widget.posFindtext.htmlText = gameStrings.FIGHT_FOR_LOVE_SEEK_TXT % (seekId,)
        self.refreshInfo()

    def refreshInfo(self):
        if not self.hasBaseData():
            return
        dikouInfo = self.getCostInfo()
        self.widget.moneyText.htmlText = dikouInfo.get('dikouStr', '')
        startTimeDesc = FFLCD.data.get('startTimeDesc', '')
        self.widget.timeDesc.text = startTimeDesc
        self.refreshRewardMc()
        self.refreshConsume()

    def refreshRewardMc(self):
        if not self.hasBaseData():
            return
        self.widget.removeAllInst(self.widget.itemCanvas)
        rewardItems = FFLCD.data.get('rewardItem', ())
        for i, (itemId, num) in enumerate(rewardItems):
            slotItem = self.widget.getInstByClsName('M12_InventorySlot')
            slotItem.x = i * 60
            self.widget.itemCanvas.addChild(slotItem)
            itemInfo = uiUtils.getGfxItemById(itemId, num)
            slotItem.dragable = False
            slotItem.setItemSlotData(itemInfo)

    def refreshConsume(self):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        costItemId, costNum = FFLCD.data.get('itemCost', (0, 0))
        itemInfo = uiUtils.getGfxItemById(costItemId, costNum)
        count = p.inv.countItemInPages(costItemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
        numStr = uiUtils.convertNumStr(count, costNum)
        itemInfo['count'] = numStr
        self.widget.costItem.dragable = False
        self.widget.costItem.setItemSlotData(itemInfo)

    def getCostInfo(self):
        dikouInfo = {}
        costItemId, costNum = FFLCD.data.get('itemCost', (0, 0))
        if costItemId:
            p = BigWorld.player()
            dikouInfo['costItemId'] = costItemId
            dikouInfo['costNum'] = costNum
            dikouData = IFSCD.data.get(costItemId, {})
            dikouInfo['dikouUnit'] = dikouData.get(const.YUN_CHUI_JI_FEN_FAME_ID, 0)
            ownCount = p.inv.countItemInPages(costItemId, gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
            dikouNum = max(costNum - ownCount, 0)
            yunchuiOwn = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
            yunchuiNeed = dikouNum * dikouInfo['dikouUnit']
            dikouStr = uiUtils.convertNumStr(yunchuiOwn, yunchuiNeed, enoughColor='#FFC961')
            dikouInfo['dikouStr'] = dikouStr
        return dikouInfo

    def handleSelectCheckBtn(self, *arg):
        if not self.hasBaseData():
            return
        self.refreshInfo()

    def hasBaseData(self):
        if not self.widget:
            return False
        return True

    def _onChargeBtnClick(self, e):
        self.uiAdapter.tianBiToYunChui.show()

    @ui.checkInventoryLock()
    def _onApplyBtnClick(self, e):
        if not self.hasBaseData():
            return
        p = BigWorld.player()
        isUseYunChuiScore = self.widget.dikouCheckBox.selected
        p.cell.createFightForLove(isUseYunChuiScore, p.cipherOfPerson)
