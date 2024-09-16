#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteExplorePlanProxy.o
import BigWorld
import clientUtils
import events
import uiConst
import gameglobal
import utils
import summonSpriteExplore
import gametypes
from uiProxy import UIProxy
from guis import uiUtils
from gamestrings import gameStrings
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from data import sys_config_data as SCD
from cdata import home_config_data as HCD
from cdata import game_msg_def_data as GMDD

class SummonedWarSpriteExplorePlanProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteExplorePlanProxy, self).__init__(uiAdapter)
        self.widget = None

    def reset(self):
        pass

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        self.widget.submitBtn.visible = False
        self.widget.submitBtn.addEventListener(events.BUTTON_CLICK, self.handleSubmitBtnClick, False, 0, True)
        self.widget.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshBtnClick, False, 0, True)
        self.widget.gotoBtn.addEventListener(events.BUTTON_CLICK, self.handleGotoBtnClick, False, 0, True)
        desc = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_EXPLORE_PALN_DESC, '')
        self.widget.needDesc.htmlText = desc
        refreshTimesLimit = gameglobal.rds.ui.summonedWarSpriteExplore.getSpriteExploreRefreshTimes()
        self.widget.refreshBtn.visible = True if refreshTimesLimit else False

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        isCarryItem = exploreSprite.isCarryItem
        pendingBonusId = exploreSprite.pendingBonusId
        if isCarryItem:
            self.widget.finishMc.visible = True
            finishDesc = gameStrings.SPRITE_EXPLORE_FINISH_NONE_GETED if pendingBonusId else gameStrings.SPRITE_EXPLORE_FINISH_GETED
            self.widget.finishMc.textField.text = finishDesc
            self.widget.itemMc.visible = False
            self.widget.msgIcon.visible = False
            self.widget.desc0.visible = False
        else:
            self.widget.finishMc.visible = False
            self.widget.itemMc.visible = True
            self.widget.msgIcon.visible = True
            self.widget.desc0.visible = True
            self.updateItemSlot()
        self.updateRewardSlot()

    def handleGotoBtnClick(self, *args):
        p = BigWorld.player()
        lastTime = p.myHome.lastUseBackHomeSkillTime
        total = HCD.data.get('backHomeSkillCD', 1800)
        if utils.getNow() - lastTime < total:
            p.showGameMsg(GMDD.data.ENTER_ROOM_FAILED_SKILL_CD, ())
            return
        p.useGoHomeRoomSkill()

    def handleRefreshBtnClick(self, *args):
        gameglobal.rds.ui.summonedWarSpriteItemRefresh.show()

    def handleSubmitBtnClick(self, *args):
        if not gameglobal.rds.ui.summonedWarSpriteFastSubmit.getCheckOnceData(uiConst.CHECK_ONCE_TYPE_SPRITE_FAST_SUBMIT):
            gameglobal.rds.ui.summonedWarSpriteFastSubmit.show(uiConst.CHECK_ONCE_TYPE_SPRITE_FAST_SUBMIT)
        else:
            canSubmitItmes = self.getCanSubmitItems()
            p = BigWorld.player()
            p.base.exploreSpriteQuickCommitItem(canSubmitItmes)

    def handleItemSlotClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        posIdx = target.posIdx
        gameglobal.rds.ui.summonedWarSpriteItemSubmit.show(posIdx)

    def getCanSubmitItems(self):
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        carryItem = exploreSprite.carryItem
        itemPos = []
        for posIdx, value in carryItem.iteritems():
            isPrepare = value.get('isPrepare', 0)
            if not isPrepare:
                itemId = value.get('itemId', 0)
                itemNum = value.get('itemNum', 0)
                myItemNum = uiUtils.getItemCountInInvAndMaterialAndHierogramBag(p.id, itemId)
                if myItemNum and itemNum and myItemNum >= itemNum:
                    itemPos.append(posIdx)

        return itemPos

    def updateItemSlot(self):
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        carryItem = exploreSprite.carryItem
        canSubmitItem = False
        for posIdx, value in carryItem.iteritems():
            itemSlot = getattr(self.widget.itemMc, 'itemSlot%d' % posIdx, None)
            if not itemSlot:
                continue
            itemSlot.posIdx = posIdx
            itemId = value.get('itemId', 0)
            itemNum = value.get('itemNum', 0)
            isPrepare = value.get('isPrepare', 0)
            bonusRate = p.vipRevise(gametypes.VIP_SERVICE_SPRITE_EXPLORE_ITEM_RATE, value.get('bonusRate', 0))
            itemSlot.slot.fitSize = True
            itemSlot.slot.dragable = False
            itemInfo = uiUtils.getGfxItemById(itemId)
            itemSlot.slot.setItemSlotData(itemInfo)
            szRate = '+%d%%' % (bonusRate,)
            ASUtils.setHitTestDisable(itemSlot.addIcon, True)
            if isPrepare:
                itemSlot.addIcon.visible = False
                itemSlot.submitT.visible = True
                itemSlot.numValT.visible = False
                itemSlot.preValT.htmlText = uiUtils.toHtml(szRate, color='#018F04')
                itemSlot.removeEventListener(events.MOUSE_CLICK, self.handleItemSlotClick)
            else:
                itemSlot.addIcon.visible = True
                itemSlot.submitT.visible = False
                itemSlot.numValT.visible = True
                myItemNum = uiUtils.getItemCountInInvAndMaterialAndHierogramBag(p.id, itemId)
                itemSlot.numValT.text = '%d/%d' % (myItemNum, itemNum)
                itemSlot.preValT.htmlText = uiUtils.toHtml(szRate, color='#99866B')
                itemSlot.addEventListener(events.MOUSE_CLICK, self.handleItemSlotClick, False, 0, True)
                if not canSubmitItem:
                    canSubmitItem = myItemNum >= itemNum
            preValTip = gameStrings.SPRITE_EXPLORE_FINISH_EXTRA_ADD % bonusRate
            TipManager.addTip(itemSlot.preValT, preValTip)

    def updateRewardSlot(self):
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        bonusId = exploreSprite.bonusId
        option = exploreSprite.option
        itemId = summonSpriteExplore.getItemIdByBonusId(option, bonusId)
        itemInfo = uiUtils.getGfxItemById(itemId)
        self.widget.rewardSlot.fitSize = True
        self.widget.rewardSlot.dragable = False
        self.widget.rewardSlot.setItemSlotData(itemInfo)
