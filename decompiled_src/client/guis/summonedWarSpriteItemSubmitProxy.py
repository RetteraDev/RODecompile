#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteItemSubmitProxy.o
import BigWorld
import uiConst
import gameglobal
import summonSpriteExplore
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
from data import item_data as ID
from cdata import game_msg_def_data as GMDD

class SummonedWarSpriteItemSubmitProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteItemSubmitProxy, self).__init__(uiAdapter)
        self.widget = None
        self.posIdx = -1
        self.needItemNum = 0
        self.myItemNum = 0
        self.itemId = 0
        self.submitedNum = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_ITEM_SUBMIT, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_ITEM_SUBMIT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_ITEM_SUBMIT)

    def reset(self):
        self.posIdx = -1
        self.needItemNum = 0
        self.myItemNum = 0
        self.itemId = 0
        self.submitedNum = 0

    def show(self, posIdx):
        self.posIdx = posIdx
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_ITEM_SUBMIT, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn

    def refreshInfo(self):
        if not self.widget:
            return
        if self.posIdx == -1:
            return
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        value = exploreSprite.carryItem.get(self.posIdx, {})
        self.submitedNum = self.getSubmitedNum(exploreSprite.carryItem)
        self.itemId = value.get('itemId', 0)
        self.needItemNum = value.get('itemNum', 0)
        self.myItemNum = uiUtils.getItemCountInInvAndMaterialAndHierogramBag(p.id, self.itemId)
        itemName = uiUtils.getItemColorName(self.itemId)
        if self.myItemNum >= self.needItemNum:
            self.widget.lessMc.visible = False
            self.widget.submitMc.visible = True
            self.updateSunmitMc(self.widget.submitMc, itemName)
        else:
            self.widget.lessMc.visible = True
            self.widget.submitMc.visible = False
            self.updateLessMc(self.widget.lessMc, exploreSprite.askGuildForHelpTimes, itemName)

    def getSubmitedNum(self, carryItem):
        submitedNum = 0
        for value in carryItem.values():
            isPrepare = value.get('isPrepare', 0)
            if isPrepare:
                submitedNum += 1

        return submitedNum

    def _onBtn0Click(self, e):
        p = BigWorld.player()
        if self.myItemNum >= self.needItemNum:
            p.base.exploreSpriteCommitItemByMyself(self.posIdx)
        else:
            name = ID.data.get(self.itemId, {}).get('name', '')
            gameglobal.rds.ui.tabAuctionConsign.show(searchItemName=name)
        self.hide()

    def _onBtn1Click(self, e):
        p = BigWorld.player()
        if self.myItemNum >= self.needItemNum:
            self.hide()
        else:
            p.base.exploreSpriteAskGuildForHelp(self.posIdx)

    def updateSunmitMc(self, submitMc, itemName):
        self.widget.titleName.textField.text = gameStrings.SPRITE_EXPLORE_SUBMIT_TITLE
        submitMc.itemSlot.slot.fitSize = True
        submitMc.itemSlot.slot.dragable = False
        count = uiUtils.toHtml('%d/%d' % (self.myItemNum, self.needItemNum), '#d9cfb6')
        itemInfo = uiUtils.getGfxItemById(self.itemId, count)
        submitMc.itemSlot.slot.setItemSlotData(itemInfo)
        self.widget.btn0.label = gameStrings.SPRITE_EXPLORE_SUBMIT_BTN_SURE
        self.widget.btn1.label = gameStrings.SPRITE_EXPLORE_SUBMIT_BTN_CANCEL

    def updateLessMc(self, lessMc, askGuildForHelpTimes, itemName):
        self.widget.titleName.textField.text = gameStrings.SPRITE_EXPLORE_LESS_TITLE
        lessMc.itemSlot.slot.fitSize = True
        lessMc.itemSlot.slot.dragable = False
        count = uiUtils.toHtml('%d/%d' % (self.myItemNum, self.needItemNum), '#d34024')
        itemInfo = uiUtils.getGfxItemById(self.itemId, count)
        lessMc.itemSlot.slot.setItemSlotData(itemInfo)
        self.widget.btn0.label = gameStrings.SPRITE_EXPLORE_LESS_BTN_SHOP
        self.widget.btn1.label = gameStrings.SPRITE_EXPLORE_LESS_BTN_HELP % (askGuildForHelpTimes, 3)
        limitAskNum = summonSpriteExplore.getExploreSpriteAskForHelpLimit()
        if self.submitedNum < limitAskNum:
            self.widget.btn1.disabled = True
            btnTip = uiUtils.getTextFromGMD(GMDD.data.EXPLORE_SPRITE_ASK_HELP_LIMIT_TIP, '%d') % limitAskNum
            TipManager.addTip(self.widget.btn1, btnTip)
        else:
            self.widget.btn1.disabled = False
            TipManager.removeTip(self.widget.btn1)
