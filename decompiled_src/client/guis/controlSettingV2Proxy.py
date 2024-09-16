#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/controlSettingV2Proxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import utils
import events
import const
import copy
import appSetting
import hotkeyProxy
import gameStrings
import formula
from gameclass import Singleton
from uiProxy import UIProxy
from guis import asObject
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from gameStrings import gameStrings
from sfx import keyboardEffect
from guis import hotkey as HK
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SYSCD
from data import game_setting_data as GSD

class ControlSettingV2Proxy(UIProxy):
    KEY_BOARD_MODE = 0
    MOUSE_MODE = 1
    ACTION_MODE = 2
    MOUSE_SEPPD_SLOW = 0
    MOUSE_SPEED_MID = 1
    MOUSE_SPEED_FAST = 2

    def __init__(self, uiAdapter):
        super(ControlSettingV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.keyBoardContent = None
        self.mouseModeContent = None
        self.actionModeContent = None
        self.oldSelfKeyMenuIdx = None
        self.oldShowCursorMenuIdx = None
        self.currentMode = None
        self.aimCrossId = None
        self.hotKeyManager = hotkeyProxy.HotKeyManager.getInstance()

    def initPanel(self, widget):
        p = BigWorld.player()
        self.hotKeyManager.contorlKey.switchDefaultKey(p.getOperationMode())
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI)
        self.widget = widget
        self.keyBoardContent = self.widget.keyBoardCanvas.scrollWindow.canvas
        self.mouseModeContent = self.widget.mouseCanvas.scrollWindow.canvas
        self.actionModeContent = self.widget.actionCanvas.scrollWindow.canvas
        self.widget.btn3d.addEventListener(events.BUTTON_CLICK, self.handleModeBtnClick)
        self.widget.btn28d.addEventListener(events.BUTTON_CLICK, self.handleModeBtnClick)
        self.widget.btnAction.addEventListener(events.BUTTON_CLICK, self.handleModeBtnClick)
        self.widget.defaultBtn.addEventListener(events.BUTTON_CLICK, self.handleDefaultBtnClick)
        self.widget.applyBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyBtnClick)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick)
        selfkeyMenuArray = []
        for index, value in enumerate(HK.CAST_SELF_KEY_ARRAY):
            selfkeyMenuArray.append({'label': value[0],
             'data': value[1],
             'index': index})

        ASUtils.setDropdownMenuData(self.actionModeContent.selfKeyMenu, selfkeyMenuArray)
        showCursorMenuArray = []
        for index, value in enumerate(HK.SHOW_CURSOR_KEY_ARRAY):
            showCursorMenuArray.append({'label': value[0],
             'data': value[1],
             'index': index})

        ASUtils.setDropdownMenuData(self.actionModeContent.showCursorMenu, showCursorMenuArray)
        self.actionModeContent.rangeSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange)
        self.actionModeContent.aimHeightSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange)
        self.actionModeContent.shakeCameraSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange)
        self.actionModeContent.selfKeyMenu.addEventListener(events.INDEX_CHANGE, self.handleMenuIndexChange)
        self.actionModeContent.showCursorMenu.addEventListener(events.INDEX_CHANGE, self.handleMenuIndexChange)
        self.actionModeContent.changeAim.addEventListener(events.BUTTON_CLICK, self.handleChangeAimBtnClick)
        self.actionModeContent.rangeSlider.disableWheel = True
        self.actionModeContent.aimHeightSlider.disableWheel = True
        self.actionModeContent.shakeCameraSlider.disableWheel = True
        self.actionModeContent.selfKeyMenu.disableWheel = True
        self.actionModeContent.showCursorMenu.disableWheel = True
        self.actionModeContent.changeAim.disableWheel = True
        ASUtils.setDropdownMenuData(self.mouseModeContent.selfKeyMenu, selfkeyMenuArray)
        self.mouseModeContent.rangeSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange)
        self.mouseModeContent.shakeCameraSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange)
        self.mouseModeContent.selfKeyMenu.addEventListener(events.INDEX_CHANGE, self.handleMenuIndexChange)
        self.mouseModeContent.rangeSlider.disableWheel = True
        self.mouseModeContent.shakeCameraSlider.disableWheel = True
        self.mouseModeContent.selfKeyMenu.disableWheel = True
        ASUtils.setDropdownMenuData(self.keyBoardContent.selfKeyMenu, selfkeyMenuArray)
        self.keyBoardContent.rangeSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange)
        self.keyBoardContent.shakeCameraSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange)
        self.keyBoardContent.selfKeyMenu.addEventListener(events.INDEX_CHANGE, self.handleMenuIndexChange)
        self.keyBoardContent.rangeSlider.disableWheel = True
        self.keyBoardContent.shakeCameraSlider.disableWheel = True
        self.keyBoardContent.selfKeyMenu.disableWheel = True
        self.refreshUI(self.getControlConfigData(), self.getControlConfigDataPlus())

    def getControlConfigData(self):
        p = BigWorld.player()
        operationMode = p.getSavedOperationMode()
        return self.getOperationData(operationMode)

    def getOperationData(self, operationMode):
        p = BigWorld.player()
        ar = [operationMode]
        i = 1
        operationData = copy.deepcopy(p.operation[operationMode])
        for item in operationData:
            ar.append(item)
            i = i + 1

        return ar

    def getControlConfigDataPlus(self):
        p = BigWorld.player()
        operationMode = p.getSavedOperationMode()
        i = 0
        plus = self.getModePlus(operationMode)
        ar = []
        for item in self.getModePlusKeys(operationMode):
            if item == gameglobal.PLUS_AIMCROSS_KEY:
                ar.append(p.operation.get(plus, {}).get(item, 9))
            else:
                ar.append(p.operation.get(plus, {}).get(item, 0))
            i = i + 1

        return ar

    def getModePlus(self, mode):
        if mode == gameglobal.KEYBOARD_MODE:
            return gameglobal.KEYBOARD_PLUS
        if mode == gameglobal.MOUSE_MODE:
            return gameglobal.MOUSE_PLUS
        if mode == gameglobal.ACTION_MODE:
            return gameglobal.ACTION_PLUS

    def getModePlusKeys(self, mode):
        if mode == gameglobal.KEYBOARD_MODE:
            return gameglobal.KEYBOARD_PLUS_KEYS
        if mode == gameglobal.MOUSE_MODE:
            return gameglobal.MOUSE_PLUS_KEYS
        if mode == gameglobal.ACTION_MODE:
            return gameglobal.ACTION_PLUS_KEYS

    def getContentBlock(self, mode):
        contentBlockArray = [self.keyBoardContent, self.mouseModeContent, self.actionModeContent]
        return contentBlockArray[mode]

    def getCkBoxNum(self, mode):
        ckBoxNumArray = [10, 10, 11]
        return ckBoxNumArray[mode]

    def refreshUI(self, controlConfigData, controlConfigDataPlus):
        self.currentMode = controlConfigData[0]
        contentBlock = self.getContentBlock(self.currentMode)
        self.widget.btn3d.selected = False
        self.widget.btn28d.selected = False
        self.widget.btnAction.selected = False
        self.widget.keyBoardCanvas.visible = False
        self.widget.mouseCanvas.visible = False
        self.widget.actionCanvas.visible = False
        if self.currentMode == self.KEY_BOARD_MODE:
            self.widget.btn3d.selected = True
            self.widget.keyBoardCanvas.visible = True
        elif self.currentMode == self.MOUSE_MODE:
            self.widget.btn28d.selected = True
            self.widget.mouseCanvas.visible = True
        elif self.currentMode == self.ACTION_MODE:
            self.widget.btnAction.selected = True
            self.widget.actionCanvas.visible = True
        ckBoxNum = self.getCkBoxNum(self.currentMode)
        for i in xrange(1, 4):
            ckBox = getattr(contentBlock, 'ckBox' + str(i), None)
            if ckBox:
                ckBox.selected = controlConfigData[i]

        for i in xrange(8, 8 + (ckBoxNum - 3)):
            ckBox = getattr(contentBlock, 'ckBox' + str(i - 4), None)
            if ckBox:
                ckBox.selected = controlConfigData[i]

        if controlConfigData[4] == self.MOUSE_SEPPD_SLOW:
            contentBlock.ckBoxScrollSlow.selected = True
        elif controlConfigData[4] == self.MOUSE_SPEED_MID:
            contentBlock.ckBoxScrollMiddle.selected = True
        elif controlConfigData[4] == self.MOUSE_SPEED_FAST:
            contentBlock.ckBoxScrollQuick.selected = True
        contentBlock.rangeSlider.value = controlConfigData[5]
        contentBlock.rangeText.text = str(controlConfigData[5])
        contentBlock.shakeCameraSlider.value = controlConfigData[7] / 10.0
        contentBlock.shakeCameraSliderText.text = str(controlConfigData[7] / 10.0)
        if self.currentMode == self.ACTION_MODE:
            contentBlock.aimHeightSlider.value = controlConfigData[6]
            contentBlock.aimHeightRangeText.text = str(controlConfigData[6])
        contentBlock.selfKeyMenu.selectedIndex = controlConfigDataPlus[0]
        self.oldSelfKeyMenuIdx = contentBlock.selfKeyMenu.selectedIndex
        if self.currentMode == self.ACTION_MODE:
            contentBlock.showCursorMenu.selectedIndex = controlConfigDataPlus[1]
            self.oldShowCursorMenuIdx = contentBlock.showCursorMenu.selectedIndex
            contentBlock.aimName.text = gameStrings.TEXT_CONTROLSETTINGV2PROXY_228 + str(controlConfigDataPlus[2] + 1)
            self.aimCrossId = controlConfigDataPlus[2]

    def handleModeBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        newMode = int(target.data)
        if newMode != self.currentMode:
            self.changeMode(newMode)

    def changeMode(self, mode):
        p = BigWorld.player()
        if appSetting.GameSettingObj.switchAvatarPhysics(mode):
            p.applyModeOperation(mode)
            self.hotKeyManager.contorlKey.switchDefaultKey(mode)
            p.setSavedOperationMode(mode)
            if hasattr(p, 'ap'):
                p.ap.reset()
            operationArray = self.getOperationData(mode)
            self.refreshUI(operationArray, self.getControlConfigDataPlus())
            if mode != gameglobal.ACTION_MODE:
                BigWorld.player().optionalTargetLocked = None
        gameglobal.rds.ui.actionbar.setFirstTimeOperation(mode, 1)

    def handleSliderValueChange(self, *args):
        e = ASObject(args[3][0])
        contentBlock = self.getContentBlock(self.currentMode)
        if e.target.name == 'rangeSlider':
            contentBlock.rangeText.text = str(int(e.target.value))
        elif e.target.name == 'aimHeightSlider':
            contentBlock.aimHeightRangeText.text = str(int(e.target.value))
        elif e.target.name == 'shakeCameraSlider':
            contentBlock.shakeCameraSliderText.text = '%.1f' % e.target.value

    def handleMenuIndexChange(self, *args):
        contentBlock = self.getContentBlock(self.currentMode)
        if self.currentMode == self.ACTION_MODE and contentBlock.selfKeyMenu.selectedIndex == contentBlock.showCursorMenu.selectedIndex:
            contentBlock.selfKeyMenu.selectedIndex = self.oldSelfKeyMenuIdx
            contentBlock.showCursorMenu.selectedIndex = self.oldShowCursorMenuIdx
            BigWorld.player().showGameMsg(GMDD.data.SELF_KEY_SHOW_CURSOR_MUTEX, ())
            return
        if self.currentMode == self.ACTION_MODE:
            check = self.checkSelfKeyChangable()
            if not check:
                contentBlock.showCursorMenu.selectedIndex = self.oldShowCursorMenuIdx
                return
            self.oldShowCursorMenuIdx = contentBlock.showCursorMenu.selectedIndex
        self.oldSelfKeyMenuIdx = contentBlock.selfKeyMenu.selectedIndex

    def checkSelfKeyChangable(self):
        if BigWorld.player()._isOnZaijuOrBianyao() and not formula.inDotaBattleField(getattr(BigWorld.player(), 'mapID', 0)):
            BigWorld.player().showGameMsg(GMDD.data.SELF_KEY_BIANSHEN_NO_CHANGE, ())
            return False
        return True

    def handleChangeAimBtnClick(self, *args):
        gameglobal.rds.ui.changeAim.show()

    def refreshAimCrossId(self, id):
        self.aimCrossId = id
        self.getContentBlock(self.currentMode).aimName.text = gameStrings.CONTROLSETTING_TEXT1 + str(id + 1)

    def handleDefaultBtnClick(self, *args):
        p = BigWorld.player()
        operateMode = p.getOperationMode()
        operateData = list(GSD.data.get('keyboardMode', [0,
         0,
         1,
         1,
         10,
         0]))
        if operateMode == gameglobal.KEYBOARD_MODE:
            operateData = list(GSD.data.get('keyboardMode', [0,
             0,
             1,
             1,
             10,
             0]))
            p.operation[gameglobal.KEYBOARD_MODE] = operateData
            p.operation[gameglobal.KEYBOARD_PLUS] = dict(gameglobal.KEYBOARD_PLUS_DICT)
        elif operateMode == gameglobal.MOUSE_MODE:
            operateData = list(GSD.data.get('mouseMode', [0,
             0,
             1,
             1,
             12,
             0,
             1]))
            p.operation[gameglobal.MOUSE_MODE] = operateData
            p.operation[gameglobal.MOUSE_PLUS] = dict(gameglobal.MOUSE_PLUS_DICT)
        elif operateMode == gameglobal.ACTION_MODE:
            operateData = list(GSD.data.get('actionMode', [0,
             0,
             1,
             1,
             8,
             1]))
            p.operation[gameglobal.ACTION_MODE] = operateData
            p.operation[gameglobal.ACTION_PLUS] = dict(gameglobal.ACTION_PLUS_DICT)
        p.changeDefalutToSpecial()
        p.applyModeOperation(operateMode)
        self.refreshUI(self.getControlConfigData(), self.getControlConfigDataPlus())
        p.sendOperation()

    def handleConfirmBtnClick(self, *args):
        self.handleApplyBtnClick(args)
        gameglobal.rds.ui.gameSetting.hide()
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def handleApplyBtnClick(self, *args):
        dataOri = []
        dataPlusOri = []
        self.ui2Data(dataOri, dataPlusOri)
        p = BigWorld.player()
        data = [ int(float(x)) for x in dataOri ]
        plusData = [ int(float(x)) for x in dataPlusOri ]
        p.setSavedOperationMode(p.getOperationMode())
        self.operationApply(data)
        self.operationPlusApply(plusData)
        p.sendOperation()
        p.applyCommonOperation()
        if not p._isOnZaijuOrBianyao() or formula.inDotaBattleField(getattr(p, 'mapID', 0)):
            self.hotKeyManager.saveHotKey()
            p.reload()
        keyboardEffect.refreshHotkeyEffect()

    def operationApply(self, data):
        p = BigWorld.player()
        operationMode = p.getSavedOperationMode()
        _value = p.operation[operationMode]
        if data[0] != _value[0]:
            p.lockEnemy = data[0]
        if data[1] != _value[1]:
            appSetting.DebugSettingObj.switchShortcutToPostion(data[1])
        if data[2] != _value[2]:
            gameglobal.rds.ui.castbar.autoReleaseCharge = data[2]
        if data[3] != _value[3]:
            gameglobal.rds.cam.setScrollSpeed(data[3], -2)
        if data[4] != _value[4]:
            gameglobal.rds.cam.setMaxScrollRange(data[4])
        if data[5] != _value[5]:
            gameglobal.AIM_CROSS_HEIGHT = data[5]
            currentScrollNum = gameglobal.rds.cam.currentScrollNum
            BigWorld.player().ap.resetAimCrossPos(currentScrollNum)
        if data[6] != _value[6]:
            gameglobal.SHAKE_CAMERA_STRENGTH = data[6]
        if operationMode == gameglobal.KEYBOARD_MODE:
            if data[7] != _value[7]:
                gameglobal.AUTOSKILL_FLAG = data[7]
            if data[8] != _value[8]:
                gameglobal.MOVE_STOP_GUIDE = data[8]
            if data[9] != _value[9]:
                gameglobal.STRONG_HIT = data[9]
                self.applyStrongHit(data)
            if data[10] != _value[10]:
                gameglobal.BREAK_GUIDE_SKILL = data[10]
            if data[11] != _value[11]:
                gameglobal.INTELLIGENT_CAST = data[11]
            if len(_value) > 12 and data[12] != _value[12]:
                gameglobal.PLAY_INDICATOR_EFF = data[12]
            if data[13] != _value[13]:
                gameglobal.TAB_NOT_TO_SELECT_SPRITE = data[13]
        elif operationMode == gameglobal.MOUSE_MODE:
            if data[7] != _value[7]:
                gameglobal.INTELLIGENT_CAST = data[7]
            if data[8] != _value[8]:
                gameglobal.AUTOSKILL_FLAG = data[8]
            if data[9] != _value[9]:
                gameglobal.ENABLE_FREE_ROTATE_CAM = data[9]
                gameglobal.rds.cam.resetDcursorPitch()
            if data[10] != _value[10]:
                gameglobal.MOVE_STOP_GUIDE = data[10]
            if data[11] != _value[11]:
                gameglobal.STRONG_HIT = data[11]
                self.applyStrongHit(data)
            if len(data) > 12 and data[12] != _value[12]:
                gameglobal.BREAK_GUIDE_SKILL = data[12]
            if data[13] != _value[13]:
                gameglobal.TAB_NOT_TO_SELECT_SPRITE = data[13]
        elif operationMode == gameglobal.ACTION_MODE:
            if data[7] != _value[7]:
                gameglobal.OPTIONAL_TARGET = data[7]
                gameglobal.CAN_LOCK_TARGET_NPC = data[7]
            if data[8] != _value[8]:
                gameglobal.MOVE_STOP_GUIDE = data[8]
            if data[9] != _value[9]:
                gameglobal.NEED_CHOOSE_EFFECT = data[9]
            if data[10] != _value[10]:
                gameglobal.STRONG_HIT = data[10]
                self.applyStrongHit(data)
            if data[11] != _value[11]:
                gameglobal.BREAK_GUIDE_SKILL = data[11]
            if len(data) > 12 and data[12] != _value[12]:
                gameglobal.INTELLIGENT_CAST = data[12]
            if len(_value) > 13 and data[13] != _value[13]:
                gameglobal.PLAY_INDICATOR_EFF = data[13]
            if data[14] != _value[14]:
                gameglobal.TAB_NOT_TO_SELECT_SPRITE = data[14]
        p.operation[operationMode] = data

    def applyStrongHit(self, data):
        if gameglobal.STRONG_HIT:
            p = BigWorld.player()
            strongHitScrollRanges = SYSCD.data.get('strongHitScrollRanges', {})
            maxRange = strongHitScrollRanges.get(BigWorld.player().realSchool, 6)
            gameglobal.rds.cam.setMaxScrollRange(maxRange)
            data[gameglobal.MAX_SCROLL_RANGE_IDX] = maxRange
            if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
                height = SYSCD.data.get('strongHitAimHeight', 2)
                data[gameglobal.AIM_CROSS_HEIGHT_IDX] = height
                gameglobal.AIM_CROSS_HEIGHT = height
                currentScrollNum = gameglobal.rds.cam.currentScrollNum
                BigWorld.player().ap.resetAimCrossPos(currentScrollNum)

    def operationPlusApply(self, data):
        p = BigWorld.player()
        operationMode = p.getSavedOperationMode()
        plus = self.getModePlus(operationMode)
        _value = p.operation.get(plus, {})
        if _value.get(gameglobal.PLUS_SELF_KEY) != data[0]:
            HK.setCastSelfKey(data[0])
            p.operation[plus][gameglobal.PLUS_SELF_KEY] = data[0]
        if operationMode == gameglobal.ACTION_MODE and len(data) > 1:
            if _value.get(gameglobal.PLUS_SHOW_CURSOR_KEY) != data[1]:
                HK.setShowCursorKey(data[1])
                p.operation[plus][gameglobal.PLUS_SHOW_CURSOR_KEY] = data[1]
                gameglobal.rds.ui.systemButton.setActionModeIndicator(True, data[1])
        if operationMode == gameglobal.ACTION_MODE and len(data) > 2:
            if _value.get(gameglobal.PLUS_AIMCROSS_KEY) != data[2]:
                p.operation[plus][gameglobal.PLUS_AIMCROSS_KEY] = data[2]
                gameglobal.rds.ui.changeAimCross(data[2])

    def handleCancelBtnClick(self, *args):
        gameglobal.rds.ui.gameSetting.hide()
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def ui2Data(self, data, dataPlus):
        contentBlock = self.getContentBlock(self.currentMode)
        for i in xrange(1, 4):
            ckBox = getattr(contentBlock, 'ckBox' + str(i), None)
            data.append(int(ckBox.selected))

        if contentBlock.ckBoxScrollSlow.selected:
            data.append(self.MOUSE_SEPPD_SLOW)
        elif contentBlock.ckBoxScrollMiddle.selected:
            data.append(self.MOUSE_SPEED_MID)
        elif contentBlock.ckBoxScrollQuick.selected:
            data.append(self.MOUSE_SPEED_FAST)
        data.append(contentBlock.rangeSlider.value)
        if self.currentMode == self.ACTION_MODE:
            data.append(contentBlock.aimHeightSlider.value)
        else:
            data.append(0)
        data.append(contentBlock.shakeCameraSlider.value * 10)
        checkBoxNum = self.getCkBoxNum(self.currentMode)
        for i in xrange(4, checkBoxNum + 1):
            ckBox = getattr(contentBlock, 'ckBox' + str(i), None)
            data.append(int(ckBox.selected))

        dataPlus.append(int(contentBlock.selfKeyMenu.selectedIndex))
        if self.currentMode == self.ACTION_MODE:
            dataPlus.append(int(contentBlock.showCursorMenu.selectedIndex))
        if self.currentMode == self.ACTION_MODE:
            dataPlus.append(self.aimCrossId)

    def getAimCrossId(self):
        if self.widget:
            return self.aimCrossId
        else:
            return 0

    def unRegisterPanel(self):
        p = BigWorld.player()
        if not p._isOnZaijuOrBianyao():
            plus = self.getModePlus(p.getSavedOperationMode())
            HK.setShowCursorKey(p.operation[plus].get(gameglobal.PLUS_SHOW_CURSOR_KEY, 1))
            HK.setCastSelfKey(p.operation[plus].get(gameglobal.PLUS_SELF_KEY))
            p.reload()
        p.setSavedOperationMode(p.getOperationMode())
        p.sendOperation()
        p = BigWorld.player()
        if p and utils.instanceof(p, 'PlayerAvatar'):
            p.unlockKey(gameglobal.KEY_POS_UI)
            p.updateActionKeyState()
        self.widget = None
        self.keyBoardContent = None
        self.mouseModeContent = None
        self.actionModeContent = None
        self.oldSelfKeyMenuIdx = None
        self.oldShowCursorMenuIdx = None
        self.currentMode = None
        self.aimCrossId = None
