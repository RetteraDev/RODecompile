#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonedWarSpriteExploreProxy.o
import BigWorld
import uiConst
import events
import gameglobal
import summonSpriteExplore
import gametypes
from uiProxy import UIProxy
from guis import uiUtils
from helpers import capturePhoto
from gamestrings import gameStrings
from callbackHelper import Functor
from guis.asObject import TipManager
from guis.asObject import ASObject
from guis.asObject import ASUtils
from data import summon_sprite_skin_data as SSSKIND
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
PHOTO_RES_NAME = 'SummonedWarSpriteExplore_unitItem%d'
SPRITE_EXPLORE_BG = 'gui/photoGenBg/sprite_explore_bg_%d.dds'
SUM_BONUS_RATE_MAX = 100
SUBMIT_COUNT_MAX = 7
SUM_BONUS_RATE_LIMIT = 200

class SummonedWarSpriteExploreProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonedWarSpriteExploreProxy, self).__init__(uiAdapter)
        self.widget = None
        self.addIconIdx = -1
        self.exploreSpriteIdx = {}
        self.headGens = []
        self.sumBonusRate = 0
        self.submitedCount = 0
        self.recordCheckState = False
        self.firstOverRate = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE)
        self.endCapture()

    def clearAll(self):
        self.exploreSpriteIdx = {}
        self.recordCheckState = False
        self.firstOverRate = -1

    def reset(self):
        self.addIconIdx = -1
        self.headGens = []
        self.sumBonusRate = 0
        self.submitedCount = 0

    def show(self):
        if not gameglobal.rds.configData.get('enableExploreSprite', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_SUMMONED_WAR_SPRITE_EXPLORE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.itemMc.checkBox.addEventListener(events.BUTTON_CLICK, self.handleSelectCheckBox, False, 0, True)
        self.widget.itemMc.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshBtnClick, False, 0, True)
        self.widget.iconType0.bonusType = 'yljingyan'
        self.widget.bindCash.bonusType = 'bindCash'
        self.initHeadGen()

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateConsumeData()
        self.updateSpriteMc(0)
        self.updateSpriteMc(1)

    def _onStartBtnClick(self, e):
        indexs = list(self.exploreSpriteIdx.values())
        isCarryItem = self.widget.itemMc.checkBox.selected
        if isCarryItem and self.submitedCount < SUBMIT_COUNT_MAX:
            msg = uiUtils.getTextFromGMD(GMDD.data.SPRITE_EXPLORE_ITEM_NOT_FULL_MSG, '')
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.realSubmit, indexs, isCarryItem))
        else:
            self.realSubmit(indexs, isCarryItem)

    def realSubmit(self, indexs, isCarryItem):
        p = BigWorld.player()
        p.base.exploreSpriteStart(indexs, isCarryItem)
        self.hide()

    def handleSelectCheckBox(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        self.recordCheckState = target.selected
        refreshTimesLimit = self.getSpriteExploreRefreshTimes()
        self.widget.itemMc.refreshBtn.visible = True if refreshTimesLimit else False
        if not target.selected:
            self.widget.itemMc.preValT.visible = False
            self.widget.itemMc.preValTitle.visible = False
            self.widget.itemMc.limitDesc.visible = True
            if refreshTimesLimit:
                self.widget.itemMc.limitDesc.y = 1
            else:
                self.widget.itemMc.limitDesc.y = 15
        else:
            self.widget.itemMc.preValT.visible = True
            self.widget.itemMc.preValTitle.visible = True
            self.widget.itemMc.limitDesc.visible = False
            if refreshTimesLimit:
                self.widget.itemMc.preValT.y = 1
                self.widget.itemMc.preValTitle.y = 1
            else:
                self.widget.itemMc.preValT.y = 15
                self.widget.itemMc.preValTitle.y = 15
            if self.sumBonusRate > SUM_BONUS_RATE_MAX:
                tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_EXPLORE_RATE_OVER, '%d') % (self.sumBonusRate - SUM_BONUS_RATE_MAX)
            else:
                tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_EXPLORE_RATE_NORMAL, '%d') % self.sumBonusRate
            self.widget.itemMc.preValT.text = '%d%%' % self.sumBonusRate
            TipManager.addTip(self.widget.itemMc.preValT, tip)

    def getSpriteExploreRefreshTimes(self):
        p = BigWorld.player()
        timesLimit = SCD.data.get('exploreSpriteRefreshTimesLimit', 0)
        limit = p.vipRevise(gametypes.VIP_SERVICE_REFRESH_SPRITE_EXPLORE_BONUS, timesLimit)
        return limit

    def handleAddBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        spriteMc = target.parent
        self.addIconIdx = spriteMc.idx
        p = BigWorld.player()
        indexs = list(self.exploreSpriteIdx.values())
        sumIndex = len(p.summonSpriteList.keys())
        if len(indexs) == sumIndex:
            msg = gameStrings.SPRITE_EXPLORE_ADD_NONE
            gameglobal.rds.ui.messageBox.showMsgBox(msg)
        else:
            gameglobal.rds.ui.summonedWarSpriteSelect.show(indexs)

    def handleMouseOver(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        target.cancelBtn.visible = True
        target.spriteBg.visible = True

    def handleMouseOut(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        target.cancelBtn.visible = False
        target.spriteBg.visible = False

    def handleCancelBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        spriteMc = target.parent.parent
        self.exploreSpriteIdx.pop(spriteMc.idx)
        self.updateSpriteMc(spriteMc.idx)
        self.updateConsumeCash()
        self.updateStartBtn()

    def handleItemLeakedClick(self, *args):
        e = ASObject(args[3][0])
        itemSlot = e.currentTarget
        posIdx = itemSlot.posIdx
        gameglobal.rds.ui.summonedWarSpriteItemSubmit.show(posIdx)

    def updateConsumeData(self):
        if not self.widget:
            return
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        time = exploreSprite.exploreTime
        self.widget.consumeTime.text = uiUtils.formatTime(time)
        wealthLv = exploreSprite.wealthLv
        expVal, famiVal = summonSpriteExplore.getExploreSpriteReward(p.lv, wealthLv)
        self.widget.expT0.text = expVal
        self.widget.famiValT.text = famiVal
        per = SCD.data.get('spriteExplorePercent', 0.005)
        tipExp = gameStrings.SRPITE_EXPLORE_EXP_TIP % expVal
        TipManager.addTip(self.widget.expT0, tipExp)
        TipManager.addTip(self.widget.iconType0, tipExp)
        tipFami = gameStrings.SRPITE_EXPLORE_FAMI_TIP % famiVal
        TipManager.addTip(self.widget.famiValT, tipFami)
        TipManager.addTip(self.widget.famiIcon, tipFami)
        isCarryItem = exploreSprite.isCarryItem
        if isCarryItem:
            self.widget.desc0.visible = True
            self.widget.itemMc.visible = False
            self.widget.desc1.visible = False
            self.widget.msgIcon.visible = False
        else:
            self.widget.desc0.visible = False
            self.widget.itemMc.visible = True
            self.widget.desc1.visible = True
            self.widget.msgIcon.visible = True
            self.updateItemSlot()
            self.updateRewardSlot()
        self.updateConsumeCash()
        self.updateStartBtn()

    def updateConsumeCash(self):
        p = BigWorld.player()
        cashNeed = summonSpriteExplore.getExploreSpriteCost(p.lv) * len(self.exploreSpriteIdx.values())
        self.widget.bindCashT.htmlText = uiUtils.convertNumStr(p.cash + p.bindCash, cashNeed, False, enoughColor=None)

    def updateStartBtn(self):
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        nowExploredCntDay = exploreSprite.nowExploredCntDay
        totalExploredCntDay = exploreSprite.totalExploredCntDay
        self.widget.startBtn.disabled = False if self.exploreSpriteIdx else True
        self.widget.startBtn.label = gameStrings.SPRITE_EXPLORE_START_BTN_LABEL % (nowExploredCntDay, totalExploredCntDay)
        btnTip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_EXPLORE_START_BTN_TIP, '%d,%d') % (totalExploredCntDay, nowExploredCntDay)
        TipManager.addTip(self.widget.startBtn, btnTip)

    def checkCntDay(self, idx, spriteMc):
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        nowExploredCntDay = exploreSprite.nowExploredCntDay
        totalExploredCntDay = exploreSprite.totalExploredCntDay
        totalLimitRange = SCD.data.get('spriteExploreTotalTimes', [(50000, 4), (0, 3)])
        spriteMc.addBtn.disabled = False
        TipManager.removeTip(spriteMc.addBtn)
        if max(totalExploredCntDay - nowExploredCntDay, 0) == 1 and idx == 1:
            spriteMc.visible = False
        if max(totalExploredCntDay - nowExploredCntDay, 0) == 0:
            if idx == 1:
                spriteMc.visible = False
            elif totalExploredCntDay == totalLimitRange[1][1]:
                spriteMc.addBtn.disabled = True
                tip = gameStrings.SPRITE_TOTAL_LIMIT_THREE_DAY % int(totalLimitRange[0][0] / 1000)
                TipManager.addTip(spriteMc.addBtn, tip)
            elif totalExploredCntDay == totalLimitRange[0][1]:
                spriteMc.addBtn.disabled = True
                tip = gameStrings.SPRITE_TOTAL_LIMIT_FOUR_DAY
                TipManager.addTip(spriteMc.addBtn, tip)

    def updateSpriteMc(self, idx):
        spriteMc = getattr(self.widget, 'addSprite%d' % idx, None)
        if not spriteMc:
            return
        else:
            spriteMc.idx = idx
            if idx in self.exploreSpriteIdx:
                spriteMc.state = 'added'
                spriteMc.gotoAndStop(spriteMc.state)
                p = BigWorld.player()
                spriteInfo = p.summonSpriteList.get(self.exploreSpriteIdx[idx], {})
                spriteName = spriteInfo.get('name', '')
                spriteMc.photo.spriteName.text = spriteName
                spriteMc.photo.spriteBg.visible = False
                spriteMc.photo.cancelBtn.visible = False
                spriteMc.photo.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
                spriteMc.photo.addEventListener(events.MOUSE_OVER, self.handleMouseOver, False, 0, True)
                spriteMc.photo.addEventListener(events.MOUSE_OUT, self.handleMouseOut, False, 0, True)
                self.takePhoto3D(idx, self.exploreSpriteIdx[idx], spriteInfo)
            else:
                spriteMc.visible = True
                spriteMc.state = 'normal'
                spriteMc.gotoAndStop(spriteMc.state)
                spriteMc.addBtn.addEventListener(events.BUTTON_CLICK, self.handleAddBtnClick, False, 0, True)
                self.checkCntDay(idx, spriteMc)
            return

    def initHeadGen(self):
        self.headGens = []
        for idx in xrange(2):
            headGen = capturePhoto.SummonedWarSpriteExplorePhotoGen('gui/taskmask.tga', 260, PHOTO_RES_NAME % idx, SPRITE_EXPLORE_BG % idx, idx)
            headGen.initFlashMesh()
            self.headGens.append(headGen)

    def takePhoto3D(self, idx, spriteIndex, spriteInfo):
        p = BigWorld.player()
        spriteId = spriteInfo.get('spriteId', 0)
        skinId = 0
        if p.summonSpriteSkin.has_key(spriteId):
            skinId = p.summonSpriteSkin[spriteId].curUseDict.get(spriteIndex, 0)
        skinData = SSSKIND.data.get((spriteId, skinId), {})
        spriteModel = skinData.get('transformModelIdBefore', 0)
        materials = skinData.get('materialsBefore', 'Default')
        if self.headGens:
            self.headGens[idx].startCapture(spriteModel, materials, None)

    def endCapture(self):
        for photo in self.headGens:
            photo.endCapture()

    def updateItemSlot(self):
        p = BigWorld.player()
        self.sumBonusRate = 0
        self.submitedCount = 0
        exploreSprite = p.spriteExtraDict['exploreSprite']
        carryItem = exploreSprite.carryItem
        for posIdx, value in carryItem.iteritems():
            itemSlot = getattr(self.widget.itemMc, 'itemSlot%d' % posIdx, None)
            addIcon = getattr(self.widget.itemMc, 'addIcon%d' % posIdx, None)
            if not itemSlot:
                continue
            itemSlot.posIdx = posIdx
            itemId = value.get('itemId', 0)
            itemNum = value.get('itemNum', 0)
            isPrepare = value.get('isPrepare', 0)
            bonusRate = p.vipRevise(gametypes.VIP_SERVICE_SPRITE_EXPLORE_ITEM_RATE, value.get('bonusRate', 0))
            itemSlot.fitSize = True
            itemSlot.dragable = False
            itemInfo = uiUtils.getGfxItemById(itemId, itemNum)
            itemSlot.setItemSlotData(itemInfo)
            itemSlot.validateNow()
            ASUtils.setHitTestDisable(addIcon, True)
            if isPrepare:
                addIcon.visible = False
                self.sumBonusRate += bonusRate
                self.submitedCount += 1
                itemSlot.removeEventListener(events.MOUSE_CLICK, self.handleItemLeakedClick)
            else:
                ownNum = uiUtils.getItemCountInInvAndMaterialAndHierogramBag(p.id, itemId)
                if ownNum < itemNum:
                    strNum = uiUtils.toHtml(ownNum, '#FF0000')
                else:
                    strNum = uiUtils.toHtml(ownNum, '#FFFFE6')
                count = str('%s/%d' % (strNum, itemNum))
                addIcon.visible = True
                itemSlot.setValueAmountTxt(count)
                itemSlot.addEventListener(events.MOUSE_CLICK, self.handleItemLeakedClick, False, 0, True)

        self.sumBonusRate = min(self.sumBonusRate, SUM_BONUS_RATE_LIMIT)
        self.widget.itemMc.checkBox.enabled = self.sumBonusRate
        if self.sumBonusRate >= SUM_BONUS_RATE_MAX and self.firstOverRate == -1:
            self.firstOverRate = 1
        if self.firstOverRate == 1:
            self.recordCheckState = True
            self.firstOverRate = 0
        if self.submitedCount == SUBMIT_COUNT_MAX:
            self.recordCheckState = True
        refreshTimesLimit = self.getSpriteExploreRefreshTimes()
        self.widget.itemMc.refreshBtn.visible = True if refreshTimesLimit else False
        if self.recordCheckState:
            self.widget.itemMc.checkBox.selected = True
            self.widget.itemMc.limitDesc.visible = False
            self.widget.itemMc.preValT.visible = True
            self.widget.itemMc.preValTitle.visible = True
            if refreshTimesLimit:
                self.widget.itemMc.preValT.y = 1
                self.widget.itemMc.preValTitle.y = 1
            else:
                self.widget.itemMc.preValT.y = 15
                self.widget.itemMc.preValTitle.y = 15
            if self.sumBonusRate > SUM_BONUS_RATE_MAX:
                tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_EXPLORE_RATE_OVER, '%d') % (self.sumBonusRate - SUM_BONUS_RATE_MAX)
            else:
                tip = uiUtils.getTextFromGMD(GMDD.data.SUMMON_SPRITE_EXPLORE_RATE_NORMAL, '%d') % self.sumBonusRate
            self.widget.itemMc.preValT.text = '%d%%' % self.sumBonusRate
            TipManager.addTip(self.widget.itemMc.preValT, tip)
        else:
            self.widget.itemMc.checkBox.selected = False
            self.widget.itemMc.limitDesc.visible = True
            self.widget.itemMc.preValT.visible = False
            self.widget.itemMc.preValTitle.visible = False
            if refreshTimesLimit:
                self.widget.itemMc.limitDesc.y = 1
            else:
                self.widget.itemMc.limitDesc.y = 15

    def handleRefreshBtnClick(self, *args):
        gameglobal.rds.ui.summonedWarSpriteItemRefresh.show()

    def updateRewardSlot(self):
        p = BigWorld.player()
        exploreSprite = p.spriteExtraDict['exploreSprite']
        bonusId = exploreSprite.bonusId
        option = exploreSprite.option
        itemId = summonSpriteExplore.getItemIdByBonusId(option, bonusId)
        itemInfo = uiUtils.getGfxItemById(itemId)
        self.widget.itemMc.rewardSlot.fitSize = True
        self.widget.itemMc.rewardSlot.dragable = False
        self.widget.itemMc.rewardSlot.setItemSlotData(itemInfo)

    def updateSelectedPhoto(self, spriteIndex):
        if self.addIconIdx == -1:
            return
        self.exploreSpriteIdx[self.addIconIdx] = spriteIndex
        if not self.widget:
            return
        self.updateSpriteMc(self.addIconIdx)
        self.updateConsumeCash()
        self.updateStartBtn()

    def resetRecordState(self):
        self.recordCheckState = False
        self.firstOverRate = -1
