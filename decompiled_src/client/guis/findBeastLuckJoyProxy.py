#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/findBeastLuckJoyProxy.o
import BigWorld
from Scaleform import GfxValue
import gametypes
import gameglobal
import ui
import events
import uiConst
import uiUtils
from callbackHelper import Functor
from gamestrings import gameStrings
from guis import asObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from guis.asObject import MenuManager
from uiProxy import UIProxy
from data import group_luck_joy_data as GLJD
from data import item_data as ID
from data import sys_config_data as SCD
LUCK_JOY_ITEM_ID = 1
LEADER_CHOICE_TIME = 2
MEMBER_CHOICE_TIME = 1
LEAF_CNT = 8
STONE_CNT = 6
LEAF_STONE_EFFECTS = ('xishou', 'normal', 'good', 'bad')
COUNT_DOWN_FRAME = ('open', 'tween', 'close')
COUNT_DOWN_OPEN_STATE = 0
COUNT_DOWN_TWEEN_STATE = 1
COUNT_DOWN_CLOSE_STATE = 2
MAX_NUMBER = 15
COLOR_SELF = '#e59545'
SWF_W = 1280
SWF_H = 720
GOOD_DEFAULT_ID = 4047
BAD_DEFAULT_ID = 4048

class FindBeastLuckJoyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FindBeastLuckJoyProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_FIND_BEAST_LUCKJOY, self.hide)
        self.widget = None
        self.chatLogIsMaxmize = False
        self.reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FIND_BEAST_LUCKJOY:
            self.widget = widget
            self.initUI()
            self.initListener()
            self.initTimer()

    def clearWidget(self):
        if not gameglobal.rds.ui.assign.diceMediator:
            self.uiAdapter.setVisRecord(uiConst.WIDGET_ASSIGN_DICE, False)
        if BigWorld.player():
            BigWorld.player().motionUnpin()
        self.widget = None
        self.uiAdapter.restoreUI()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FIND_BEAST_LUCKJOY)
        self.chatLogIsMaxmize = self.chatLogIsMaxmize or not gameglobal.rds.ui.chat.isHide
        self.chatLogIsMaxmize and gameglobal.rds.ui.chat.showView()
        self.callbackTimeHandle and BigWorld.cancelCallback(self.callbackTimeHandle)

    def reset(self):
        self.leafSlotInfos = [None] * LEAF_CNT
        self.stoneSlotInfos = [None] * STONE_CNT
        self.callbackTimeHandle = None
        self.goodIdx = None
        self.startTime = None
        self.curNumber = None
        self.countDownState = None

    def show(self):
        if not self.widget:
            BigWorld.player().motionPin()
            self.uiAdapter.loadWidget(uiConst.WIDGET_FIND_BEAST_LUCKJOY)

    def initTimer(self):
        self.setCountDownState(COUNT_DOWN_OPEN_STATE)
        self.maxTime = GLJD.data.get(LUCK_JOY_ITEM_ID).get('time1', MAX_NUMBER)
        self.startTime = BigWorld.player().getServerTime()
        self.refreshTimer()

    def refreshBg(self):
        if not self.widget:
            return
        self.uiAdapter.hideAllUI()
        self.uiAdapter.setWidgetVisible(uiConst.WIDGET_FIND_BEAST_LUCKJOY, True)
        self.widget.visible = True
        self.handleResize()
        if gameglobal.rds.ui.assign.diceMediator:
            self.uiAdapter.setWidgetVisible(uiConst.WIDGET_ASSIGN_DICE, True)
        BigWorld.callback(1, self.showChatLog)

    def showChatLog(self):
        self.uiAdapter.setWidgetVisible(uiConst.WIDGET_CHAT_LOG, True)
        self.chatLogIsMaxmize = not gameglobal.rds.ui.chat.isHide
        self.uiAdapter.chat.hideView()

    def handleResize(self, *args):
        scalex = SWF_W * 1.0 / self.widget.stage.stageWidth
        scaley = SWF_H * 1.0 / self.widget.stage.stageHeight
        scaleMax = max(scalex, scaley, 1)
        windowX, windowY = ASUtils.global2Local(self.widget, 0, 0)
        windowW = self.widget.stage.stageWidth * scaleMax
        windowH = self.widget.stage.stageHeight * scaleMax
        self.widget.sunShineMc.x = windowX
        self.widget.sunShineMc.y = windowY
        self.widget.sunShineMc.width = windowW
        self.widget.sunShineMc.height = windowH

    def initUI(self):
        p = BigWorld.player()
        self.widget.visible = False
        self.slotTreasureLv = GLJD.data.get(LUCK_JOY_ITEM_ID).get('treasureLv', 0)
        self.goodIconId = GLJD.data.get(LUCK_JOY_ITEM_ID).get('iconGood', GOOD_DEFAULT_ID)
        self.badIconId = GLJD.data.get(LUCK_JOY_ITEM_ID).get('iconBad', BAD_DEFAULT_ID)
        treeMc = self.widget.treeMc
        self.leaves = [treeMc.leaf0,
         treeMc.leaf1,
         treeMc.leaf2,
         treeMc.leaf3,
         treeMc.leaf4,
         treeMc.leaf5,
         treeMc.leaf6,
         treeMc.leaf7]
        self.leafSlots = [treeMc.leafSlot0,
         treeMc.leafSlot1,
         treeMc.leafSlot2,
         treeMc.leafSlot3,
         treeMc.leafSlot4,
         treeMc.leafSlot5,
         treeMc.leafSlot6,
         treeMc.leafSlot7]
        self.stoneSlots = [self.widget.stoneSlot0,
         self.widget.stoneSlot1,
         self.widget.stoneSlot2,
         self.widget.stoneSlot3,
         self.widget.stoneSlot4,
         self.widget.stoneSlot5]
        for leaf in self.leaves:
            TipManager.addTip(leaf, GfxValue(ui.gbk2unicode(gameStrings.FINDBEAST_LUCKJOY_CLICK_TIP)))

        for leafEffect in self.leafSlots:
            leafEffect.visible = False

        for stoneIcon in self.stoneSlots:
            stoneIcon.visible = False

        self.widget.hintMc.closeMc.visible = False
        self.choiceTime = LEADER_CHOICE_TIME if p.isTeamLeader() else MEMBER_CHOICE_TIME
        self.widget.hintMc.leaderHintTextField.text = gameStrings.FINDBEAST_LUCKJOY_HINT_LEADER
        self.setSelfHintText(self.choiceTime)
        self.setHitTestDisable()
        self.showPreInitLeaf()

    def showPreInitLeaf(self):
        for item in self.leafSlotInfos:
            item and self.refreshLeafSlot(item.get('slot'), item.get('idx'), item.get('name'))

    def setSelfHintText(self, choiceTime):
        if self.choiceTime < 1:
            self.widget.timeMc.textMc.selfHintTextField.htmlText = gameStrings.FINDBEAST_LUCKJOY_HINT_SELF_END
        else:
            self.widget.timeMc.textMc.selfHintTextField.htmlText = gameStrings.FINDBEAST_LUCKJOY_HINT_SELF % choiceTime

    def setHitTestDisable(self):
        ASUtils.setHitTestDisable(self.widget.sunShineMc, True)
        ASUtils.setHitTestDisable(self.widget.smogMc1, True)
        ASUtils.setHitTestDisable(self.widget.smogMc2, True)
        ASUtils.setHitTestDisable(self.widget.smogMc3, True)

    def initListener(self):
        self.widget.addEventListener(events.EVENT_RESIZE, self.handleResize, False, 0, True)
        self.widget.hintMc.closeMc.addEventListener(events.MOUSE_CLICK, self.handleCloseClick, False, 0, True)
        for leaf in self.leaves:
            leaf.addEventListener(events.MOUSE_CLICK, self.handleLeafClick, False, 0, True)

    def handleLeafClick(self, *args):
        p = BigWorld.player()
        e = asObject.ASObject(args[3][0])
        name = e.currentTarget.name
        idx = int(name[-1])
        p.cell.chooseGroupLuckJoyAward(p.groupLuckJoy.nuid, idx)

    def handleCloseClick(self, *args):
        self.hide()

    def refreshLeafSlot(self, slot, idx, name):
        slotInfo = {'name': name,
         'slot': slot,
         'idx': idx}
        self.leafSlotInfos[idx] = slotInfo
        if not self.widget:
            return
        if not self.leaves[idx].visible:
            return
        self.leaves[idx].visible = False
        self.leafSlots[idx].visible = True
        self.leafSlots[idx].gotoAndStop(LEAF_STONE_EFFECTS[slot.tp])
        self.leafSlots[idx].icon.gotoAndPlay('show')
        self.leafSlots[idx].icon.leafEffectMc.gotoAndPlay('show')
        mc = self.leafSlots[idx].icon.icon
        self.addSlotImgAndCnt(mc, slot)
        isSelf = BigWorld.player().gbId == slot.gbId
        if isSelf:
            self.choiceTime -= 1
            self.setSelfHintText(self.choiceTime)
        if name:
            frame = 'ziji' if isSelf else 'bieren'
            ASUtils.setHitTestDisable(self.leafSlots[idx], True)
            self.leafSlots[idx].icon.nameMc.nameBg.gotoAndStop(frame)
            self.leafSlots[idx].icon.nameMc.nameMc.textField.htmlText = uiUtils.toHtml(name, COLOR_SELF) if isSelf else name
        else:
            ASUtils.setHitTestDisable(self.leafSlots[idx], False)
            self.leafSlots[idx].icon.leafEffectMc.visible = False
            self.leafSlots[idx].icon.nameMc.visible = False
        name and BigWorld.callback(2, Functor(self.refreshStoneSlot, slotInfo))

    def openEnd(self, restSlotInfos):
        if not self.widget:
            return
        for slotInfo in restSlotInfos:
            self.refreshLeafSlot(slotInfo.get('slot'), slotInfo.get('idx'), slotInfo.get('name'))

        for idx, slotInfo in enumerate(self.leafSlotInfos):
            if not slotInfo or slotInfo.get('name'):
                continue
            mcIcon = self.leafSlots[idx].icon.icon
            self.addTipsBySlotType(mcIcon, slotInfo.get('slot'))

        self.widget.hintMc.closeMc.visible = True
        self.setCountDownState(COUNT_DOWN_TWEEN_STATE)
        BigWorld.callback(4, self.playDisappearTween)

    def refreshStoneSlot(self, leafSlotInfo):
        slotInfo = leafSlotInfo.copy()
        if not self.widget:
            return
        elif not slotInfo:
            return
        else:
            leafIdx = slotInfo.get('idx')
            slot = slotInfo.get('slot')
            name = slotInfo.get('name')
            self.leafSlots[leafIdx].icon.gotoAndPlay('hide')
            self.leafSlots[leafIdx].icon.leafEffectMc.gotoAndPlay('hide')
            if not name:
                return
            elif None not in self.stoneSlotInfos:
                return
            stoneIdx = self.stoneSlotInfos.index(None)
            slotInfo['idx'] = None
            self.stoneSlotInfos[stoneIdx] = slotInfo
            if slot.tp == gametypes.GROUP_LUCK_JOY_AWARD_TYPE_GOOD:
                self.goodIdx = stoneIdx
            self.stoneSlots[stoneIdx].gotoAndStop(LEAF_STONE_EFFECTS[slot.tp])
            self.stoneSlots[stoneIdx].visible = True
            self.stoneSlots[stoneIdx].mouseChildren = False
            self.stoneSlots[stoneIdx].icon.gotoAndPlay(1)
            mc = self.stoneSlots[stoneIdx].icon.icon
            if slot.tp == gametypes.GROUP_LUCK_JOY_AWARD_TYPE_NORMAL:
                effMc = self.stoneSlots[stoneIdx].icon.effectMc.liziMc
                treasureLv = ID.data.get(slot.itemId, {}).get('treasureLv', 0)
                effMc.visible = False if treasureLv < self.slotTreasureLv else True
            self.addSlotImgAndCnt(mc, slot)
            self.addTipsBySlotType(self.stoneSlots[stoneIdx], slot)
            self.setPlayerInfo(slot, stoneIdx, name)
            menuParam = {'roleName': name,
             'gbId': slot.gbId}
            MenuManager.getInstance().registerMenuById(self.stoneSlots[stoneIdx], uiConst.MENU_CHAT, menuParam)
            return

    def setCountDownState(self, idx):
        self.countDownState = COUNT_DOWN_FRAME[idx]

    def refreshTimer(self):
        self.callbackTimeHandle and BigWorld.cancelCallback(self.callbackTimeHandle)
        if not self.widget:
            return
        curTime = BigWorld.player().getServerTime()
        curNumber = self.maxTime - int(curTime - self.startTime)
        if self.countDownState == COUNT_DOWN_FRAME[COUNT_DOWN_CLOSE_STATE] and curNumber == 0:
            self.hide()
            return
        if self.countDownState == COUNT_DOWN_FRAME[COUNT_DOWN_TWEEN_STATE]:
            self.widget.timeMc.textMc.selfHintTextField.visible = False
            self.widget.timeMc.visible = False
        elif curNumber != self.curNumber:
            if curNumber > MAX_NUMBER:
                self.widget.timeMc.visible = False
            else:
                curNumber = max(curNumber, 0)
                self.curNumber = curNumber
                curNumber and self.widget.timeMc.numberMc.gotoAndStop('n' + str(curNumber))
                self.widget.timeMc.visible = curNumber != 0
                self.widget.timeMc.textMc.gotoAndStop(self.countDownState)
        self.callbackTimeHandle = BigWorld.callback(0.1, self.refreshTimer)

    def playDisappearTween(self):
        if not self.widget:
            return
        else:
            if self.goodIdx is not None:
                icon = self.stoneSlots[self.goodIdx].icon.icon
                goodX = icon.x
                goodY = icon.y
                x = goodX + icon.width / 2
                y = goodY + icon.height / 2
                gX, gY = ASUtils.local2Global(icon, x, y)
                self.playXiShouTween()
                for idx, slotInfo in enumerate(self.stoneSlotInfos):
                    if not slotInfo:
                        continue
                    slot = slotInfo.get('slot')
                    if not slot:
                        continue
                    if slot.tp != gametypes.GROUP_LUCK_JOY_AWARD_TYPE_NORMAL:
                        continue
                    self.cloneAndMoveIcon(idx, slot, gX, gY)

            else:
                self.moveTweenEnd()
            return

    def playXiShouTween(self):
        self.stoneSlots[self.goodIdx].gotoAndStop(LEAF_STONE_EFFECTS[0])
        self.stoneSlots[self.goodIdx].icon.icon.icon.cntText.visible = False
        slot = self.stoneSlotInfos[self.goodIdx].get('slot')
        name = self.stoneSlotInfos[self.goodIdx].get('name')
        self.setPlayerInfo(slot, self.goodIdx, name)

    def moveTweenEnd(self, *args):
        if not self.widget:
            return
        else:
            self.setCountDownState(COUNT_DOWN_CLOSE_STATE)
            self.maxTime = GLJD.data.get(LUCK_JOY_ITEM_ID).get('time2', MAX_NUMBER)
            self.startTime = BigWorld.player().getServerTime()
            if self.goodIdx is None:
                return
            self.stoneSlots[self.goodIdx].gotoAndStop(LEAF_STONE_EFFECTS[gametypes.GROUP_LUCK_JOY_AWARD_TYPE_GOOD])
            slot = self.stoneSlotInfos[self.goodIdx].get('slot')
            name = self.stoneSlotInfos[self.goodIdx].get('name')
            mc = self.stoneSlots[self.goodIdx].icon.icon
            self.addSlotImgAndCnt(mc, slot)
            self.setPlayerInfo(slot, self.goodIdx, name)
            return

    def cloneAndMoveIcon(self, idx, slot, gX, gY):
        iconMc = self.widget.getInstByClsName('FindBeastLuckJoy_slotNormal')
        iconMc.icon.fitSize = True
        iconPath = uiUtils.getItemIconFile64(slot.itemId)
        iconMc.icon.loadImage(iconPath)
        iconMc.cntText.visible = False
        iconMc.x = self.stoneSlots[idx].icon.icon.x
        iconMc.y = self.stoneSlots[idx].icon.icon.y
        self.stoneSlots[idx].icon.addChild(iconMc)
        endX, endY = ASUtils.global2Local(self.stoneSlots[idx].icon.icon, gX, gY)
        param = {'time': 1.5,
         'x': endX,
         'y': endY,
         'scaleX': 0,
         'scaleY': 0}
        ASUtils.addTweener(iconMc, param, self.moveTweenEnd)

    def setPlayerInfo(self, slot, idx, name):
        p = BigWorld.player()
        isSelf = p.gbId == slot.gbId
        thePlayer = p.members.get(slot.gbId)
        playerMc = self.stoneSlots[idx].icon.playerMc
        if thePlayer is None:
            playerMc.visible = False
        else:
            playerMc.leaderMc.visible = thePlayer.get('isHeader')
            lvText = uiUtils.toHtml(thePlayer.get('level'), COLOR_SELF) if isSelf else thePlayer.get('level')
            playerMc.lvTextField.htmlText = lvText
            schoolName = uiConst.SCHOOL_FRAME_DESC.get(thePlayer.get('school'))
            playerMc.schoolMc.gotoAndStop(schoolName)
            frame = 'ziji' if isSelf else 'bieren'
            playerMc.bgMc.gotoAndStop(frame)
            playerMc.nameTextField.htmlText = uiUtils.toHtml(name, COLOR_SELF) if isSelf else name

    def addTipsBySlotType(self, mc, slot):
        if not mc or not slot:
            return
        if slot.tp == gametypes.GROUP_LUCK_JOY_AWARD_TYPE_NORMAL:
            TipManager.addItemTipById(mc, slot.itemId)
        elif slot.tp == gametypes.GROUP_LUCK_JOY_AWARD_TYPE_GOOD:
            TipManager.addTip(mc, GfxValue(ui.gbk2unicode(SCD.data.get('findBeastLuckJoyString', {}).get('goodTips'))))
        elif slot.tp == gametypes.GROUP_LUCK_JOY_AWARD_TYPE_BAD:
            TipManager.addTip(mc, GfxValue(ui.gbk2unicode(SCD.data.get('findBeastLuckJoyString', {}).get('badTips'))))

    def addSlotImgAndCnt(self, mc, slot):
        if not mc or not slot:
            return
        mc.icon.fitSize = True
        if slot.tp == gametypes.GROUP_LUCK_JOY_AWARD_TYPE_NORMAL:
            iconPath = uiUtils.getItemIconFile64(slot.itemId)
            mc.icon.loadImage(iconPath)
        elif slot.tp == gametypes.GROUP_LUCK_JOY_AWARD_TYPE_GOOD:
            iconPath = self.getLeafIconPath(self.goodIconId)
            mc.icon.loadImage(iconPath)
        elif slot.tp == gametypes.GROUP_LUCK_JOY_AWARD_TYPE_BAD:
            iconPath = self.getLeafIconPath(self.badIconId)
            mc.icon.loadImage(iconPath)
        if slot.cnt <= 1:
            mc.cntText.visible = False
        else:
            mc.cntText.visible = True
            mc.cntText.text = slot.cnt

    def getLeafIconPath(self, iconId):
        return uiConst.ITEM_ICON_IMAGE_RES_64 + str(iconId) + '.dds'
