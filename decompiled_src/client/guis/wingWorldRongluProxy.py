#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldRongluProxy.o
import BigWorld
import const
import uiConst
import events
import gamelog
import gametypes
import gameglobal
from uiProxy import UIProxy
from guis import uiUtils
from data import wing_world_config_data as WWCD
from data import item_data as ITEMS
from guis.asObject import ASUtils
from asObject import ASObject
from guis.asObject import Tweener
from gamestrings import gameStrings
SLOT_COUNT = 16
MAX_ITEM_PER_ROUND = 3
FORGE_TIME_PER_TIME = 180
BACKGROUND_SOUND_ID = 71000

class WingWorldRongluProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldRongluProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WING_WORLD_RONGLU, self.hide)
        self.stepperValue = 0
        self.isDisplaying = False
        self.targetRound = 0
        self.currentRound = 0
        self.emptySlotIndex = 0
        self.showItemsStage = False
        self.lastRoundStartTime = 0
        self.isEnd = False

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WING_WORLD_RONGLU:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_RONGLU)
        self.stepperValue = 0
        self.isDisplaying = False
        self.emptySlotIndex = 0
        self.showItemsStage = False
        self.isEnd = False
        gameglobal.rds.sound.stopSound(BACKGROUND_SOUND_ID)

    def show(self):
        p = BigWorld.player()
        if not p.guild:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_RONGLU)
        else:
            p.base.getWingWorldForgeData()

    def initUI(self):
        self.widget.gotoAndPlay('open')
        self.widget.defaultCloseBtn = self.widget.closeBtn
        for i in range(0, SLOT_COUNT):
            slot = self.getSlotByIndex(i)
            slot.dragable = False
            slot.enable = True
            slot.setItemSlotData(None)

        self.widget.startBtn.addEventListener(events.BUTTON_CLICK, self.handleForgeStart, False, 0, True)
        self.widget.continueBtn.addEventListener(events.BUTTON_CLICK, self.onContinueClick, False, 0, True)
        self.widget.resultGroup.visible = False
        self.widget.continueBtn.visible = False
        self.widget.processbar.visible = False
        self.widget.processbar.lableVisible = False
        self.widget.forgeTimes.text = ''
        self.widget.resName0.text = WWCD.data.get('restype1', '')
        self.widget.resName1.text = WWCD.data.get('restype2', '')
        self.widget.resName2.text = WWCD.data.get('restype3', '')
        self.widget.resCount0.text = str(0)
        self.widget.resCount1.text = str(0)
        self.widget.resCount2.text = str(0)
        self.widget.resCost.text = str(WWCD.data.get('forgeResCost', 1000))
        BigWorld.player().base.getWingWorldForgeData()
        gameglobal.rds.sound.playSound(BACKGROUND_SOUND_ID)

    def refreshInfo(self):
        if not self.widget:
            return

    def onEnterFrame(self, *args):
        p = BigWorld.player()
        if not p.wingWorldForgeData:
            return
        self.widget.processbar.visible = self.widget.currentFrame >= 16
        self.widget.resultGroup.visible = self.widget.currentFrame >= 60
        self.widget.continueBtn.visible = self.widget.currentFrame >= 60
        if self.currentRound > self.targetRound:
            self.currentRound = self.targetRound
        if self.isEnd and not self.isDisplaying and self.widget.currentFrame >= 16:
            self.widget.gotoAndPlay('waiting')
        if not self.isDisplaying and self.currentRound < self.targetRound:
            self.widget.gotoAndPlay('start')
            self.isDisplaying = True
            self.lastRoundTime = p.getServerTime()
            self.showItemsStage = False
        if self.isDisplaying and self.widget.currentFrame in range(16, 45):
            interval = WWCD.data.get('ronglujiange', 0)
            nowTime = BigWorld.player().getServerTime()
            self.widget.processbar.visible = True
            self.widget.processbar.currentValue = float(nowTime - self.lastRoundTime) / interval * self.widget.processbar.maxValue
            if nowTime - self.lastRoundTime >= interval:
                self.showItemsStage = True
                self.widget.gotoAndPlay('result')
        if self.widget.currentFrame >= 60:
            self.widget.processbar.currentValue = self.widget.processbar.maxValue
        if self.isDisplaying and self.showItemsStage and self.widget.currentFrame >= 60:
            self.showItemsStage = False
            self.showDisplayItems()
            self.currentRound += 1
        if self.isDisplaying and self.widget.currentFrame >= self.widget.totalFrames:
            if self.currentRound < self.targetRound or self.currentRound == self.getLastRound():
                self.moveDisplayItems()
                self.isDisplaying = False
                self.widget.resultGroup.visible = False

    def handleForgeStart(self, *args):
        p = BigWorld.player()
        p.base.startWingWorldForge()

    def onStepperValueChange(self, *args):
        self.stepperValue = self.widget.stepper.value

    def onContinueClick(self, *args):
        p = BigWorld.player()
        if p.wingWorldForgeData.round == p.wingWorldForgeData.maxRound:
            self.moveDisplayItems()
        else:
            p.base.startGenBonusInForge()

    def onSlotMoveCompleted(self, *args):
        slot = ASObject(args[3][0])
        if not self.widget or not slot:
            return
        slotIndex = int(args[3][1].GetNumber())
        self.widget.removeToCache(slot)
        dstSlot = self.getSlotByIndex(slotIndex)
        if dstSlot and dstSlot.parent:
            dstSlot.parent.gotoAndPlay('flash')
            dstSlot.setItemSlotData(slot.data)

    def onForgeStart(self):
        pass

    def onForgeEnd(self):
        if not self.widget:
            return
        self.isEnd = True
        self.widget.startBtn.enabled = True
        self.refreshUI()

    def onUpdateRound(self):
        p = BigWorld.player()
        self.targetRound = p.wingWorldForgeData.round

    def refreshState(self):
        gamelog.debug('ypc@ refreshState')
        self.isDisplaying = False
        p = BigWorld.player()
        if not self.widget or not p.wingWorldForgeData or not p.guild:
            return
        self.isEnd = p.wingWorldForgeData.state == const.WINGWORLD_FORGE_STATE_END
        self.targetRound = self.currentRound = p.wingWorldForgeData.round
        self.genItems = []
        for roundItems in p.wingWorldForgeData.genItems:
            for itemId, itemCount in roundItems:
                self.genItems.append({'id': itemId,
                 'count': itemCount})

        gamelog.debug('ypc@ self.genItems = ', self.genItems)
        self.refreshUI()
        self.refreshItems()

    def refreshItems(self):
        p = BigWorld.player()
        if p.wingWorldForgeData.state == const.WINGWORLD_FORGE_STATE_NONE or p.wingWorldForgeData.state == const.WINGWORLD_FORGE_STATE_END:
            self.widget.startBtn.enabled = True
        else:
            self.widget.startBtn.enabled = False
            if self.currentRound > 0:
                visibleItems = self.getVisibleItems()
                self.emptySlotIndex = 0
                for item in visibleItems:
                    if self.emptySlotIndex >= SLOT_COUNT:
                        self.emptySlotIndex = -1
                        break
                    itemInfo = uiUtils.getGfxItemById(item['id'], item['count'])
                    self.getSlotByIndex(self.emptySlotIndex).setItemSlotData(itemInfo)
                    self.emptySlotIndex += 1

    def refreshUI(self):
        p = BigWorld.player()
        self.widget.resLv0.text = gameStrings.WING_WORLD_RONGLU_LEVEL % p.wingWorldForgeData.level
        self.widget.resLv1.text = gameStrings.WING_WORLD_RONGLU_LEVEL % p.wingWorldForgeData.level
        self.widget.resLv2.text = gameStrings.WING_WORLD_RONGLU_LEVEL % p.wingWorldForgeData.level
        self.widget.forgeTimes.text = str(p.wingWorldForgeData.genTimesWeekly) + '/' + str(WWCD.data.get('rongluResLimit', 0))
        res1Num, res2Num, res3Num, jyItemId, jyItemCount, jyLimit = self.getResNumAndLimit()
        self.widget.resCount0.text = str(res1Num)
        self.widget.resCount1.text = str(res2Num)
        self.widget.resCount2.text = str(res3Num)
        if not self.widget.hasEventListener(events.EVENT_ENTER_FRAME):
            self.widget.addEventListener(events.EVENT_ENTER_FRAME, self.onEnterFrame, False, 0, True)

    def getResNumAndLimit(self):
        p = BigWorld.player()
        res1Num = p.wingWorldForgeData.carryRes.get(gametypes.WING_RESOURCE_TYPE_OBSIDIAN, 0)
        res2Num = p.wingWorldForgeData.carryRes.get(gametypes.WING_RESOURCE_TYPE_CATEYE, 0)
        res3Num = p.wingWorldForgeData.carryRes.get(gametypes.WING_RESOURCE_TYPE_DIAMOND, 0)
        jyItemId = WWCD.data.get('jingyuanItemId', -1)
        jyItemCount = p.guild.otherRes.get(jyItemId, 0)
        cost = max(WWCD.data.get('forgeResCost', 1000), 1)
        jyLimit = min(res1Num / cost, res2Num / cost, res3Num / cost, jyItemCount)
        return (res1Num,
         res2Num,
         res3Num,
         jyItemId,
         jyItemCount,
         jyLimit)

    def getSlotByIndex(self, index):
        if index < SLOT_COUNT / 2:
            return self.widget.rightGroup.getChildByName('slot%d' % index).slot
        else:
            return self.widget.leftGroup.getChildByName('slot%d' % (index % (SLOT_COUNT / 2))).slot

    def getDisplayedItems(self):
        start = self.currentRound * MAX_ITEM_PER_ROUND
        end = start + MAX_ITEM_PER_ROUND
        return self.genItems[start:end]

    def getVisibleItems(self):
        end = self.currentRound * MAX_ITEM_PER_ROUND
        return self.genItems[0:end]

    def getLastRound(self):
        p = BigWorld.player()
        if p.wingWorldForgeData:
            return p.wingWorldForgeData.maxRound
        return 0

    def moveDisplayItems(self):
        for i in range(0, MAX_ITEM_PER_ROUND):
            srcSlot = self.widget.resultGroup.getChildByName('item%d' % (MAX_ITEM_PER_ROUND - i - 1))
            if not srcSlot or not srcSlot.data:
                continue
            bMoved = srcSlot.data.get('itemId', -1) in WWCD.data.get('rongludispalyitem', ())
            if srcSlot.visible and self.emptySlotIndex != -1 and bMoved:
                tempSlot = self.widget.getInstByClsName('M12_InventorySlot64x64')
                dstSlot = self.getSlotByIndex(self.emptySlotIndex)
                srcx, srcy = ASUtils.local2Global(srcSlot, srcSlot.x, srcSlot.y)
                dstx, dsty = ASUtils.local2Global(dstSlot, dstSlot.x, dstSlot.y)
                tmpx, tmpy = ASUtils.global2Local(self.widget, srcx, srcy)
                tempSlot.x = tmpx
                tempSlot.y = tmpy
                tempSlot.setItemSlotData(srcSlot.data)
                self.widget.addChild(tempSlot)
                Tweener.addTween(tempSlot, {'x': dstx,
                 'y': dsty,
                 'time': 1.1,
                 'transition': 'easeInQuart',
                 'onComplete': self.onSlotMoveCompleted,
                 'onCompleteParams': (tempSlot, self.emptySlotIndex)})
                self.emptySlotIndex += 1
                if self.emptySlotIndex >= SLOT_COUNT:
                    self.emptySlotIndex = -1
            srcSlot.visible = False

    def showDisplayItems(self):
        displayedItems = self.getDisplayedItems()
        self.widget.resultGroup.gotoAndStop('count%d' % len(displayedItems))
        for i in range(0, len(displayedItems)):
            itemInfo = uiUtils.getGfxItemById(displayedItems[i]['id'], displayedItems[i]['count'])
            itemSlot = self.widget.resultGroup.getChildByName('item%d' % i)
            itemSlot.visible = True
            itemSlot.dragable = False
            itemSlot.setItemSlotData(itemInfo)
