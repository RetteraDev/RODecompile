#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/keySettingV2Proxy.o
import BigWorld
import gameglobal
import utils
import events
import const
import appSetting
import hotkeyProxy
import formula
import gamelog
import keys
import uiConst
import gameStrings
from uiProxy import UIProxy
from guis import asObject
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from gameStrings import gameStrings
from ui import gbk2unicode
from guis import hotkey as HK
from sfx import keyboardEffect
from cdata import game_msg_def_data as GMDD
BTN_NAME = ['moveBtn',
 'hotBtn',
 'uiBtn',
 'teamBtn',
 'actionBtn']

class KeySettingV2Proxy(UIProxy):
    KEY_MOUSE_MIDDLE = 258
    KEY_MOUSE_FUNC3 = 259
    KEY_MOUSE_FUNC4 = 260
    KEY_MOUSE_FUNC5 = 261
    KEY_MOUSE_FUNC6 = 262
    KEY_MOUSE_FUNC7 = 263
    KEY_MOUSE_ROLLUP = 264
    KEY_MOUSE_ROLLDOWN = 265

    def __init__(self, uiAdapter):
        super(KeySettingV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.mainMc = None
        self.scrollWindowList = None
        self.canvas = None
        self.oneSwitch = None
        self.data = []
        self.selectedTanBtn = None
        self.hotKeyManager = hotkeyProxy.HotKeyManager.getInstance()
        self.selectedKey = None
        self.selectedIdx = 0

    def setSelectIdx(self, idx):
        self.selectedIdx = idx

    def initPanel(self, widget):
        p = BigWorld.player()
        self.hotKeyManager.contorlKey.switchDefaultKey(p.getOperationMode())
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI)
        self.widget = widget
        self.mainMc = self.widget.mainMc
        self.scrollWindowList = self.mainMc.scrollWindowList
        self.canvas = self.scrollWindowList.canvas
        self.scrollWindowList.column = 1
        self.scrollWindowList.itemRenderer = 'KeySettingV2_itemRender'
        self.scrollWindowList.labelFunction = self.listLabelFunction
        mode = BigWorld.player().getOperationMode()
        if mode == 0:
            self.mainMc.currentModeText.text = gameStrings.KEYSETTING_TEXT1
        elif mode == 1:
            self.mainMc.currentModeText.text = gameStrings.KEYSETTING_TEXT2
        elif mode == 2:
            self.mainMc.currentModeText.text = gameStrings.KEYSETTING_TEXT3
        self.mainMc.chageModeBtn.addEventListener(events.BUTTON_CLICK, self.handleChangeModeBtnClick)
        self.mainMc.unlockBtn.addEventListener(events.BUTTON_CLICK, self.handleUnlockKeyClick)
        self.mainMc.defaultBtn.addEventListener(events.BUTTON_CLICK, self.handleDefaultBtnClick)
        self.mainMc.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick)
        self.mainMc.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick)
        self.mainMc.moveBtn.data = 0
        self.mainMc.moveBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick)
        self.mainMc.hotBtn.data = 1
        self.mainMc.hotBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick)
        self.mainMc.uiBtn.data = 2
        self.mainMc.uiBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick)
        self.mainMc.teamBtn.data = 3
        self.mainMc.teamBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick)
        self.mainMc.actionBtn.data = 4
        self.mainMc.actionBtn.addEventListener(events.BUTTON_CLICK, self.handleTabBtnClick)
        for name in BTN_NAME:
            btn = getattr(self.mainMc, name)
            btn.selected = False

        self.selectedTanBtn = getattr(self.mainMc, BTN_NAME[self.selectedIdx])
        self.selectedTanBtn.selected = True
        self.selectedIdx = 0
        self.refreshSwitch()
        self.data = self.getKeyData()
        self.refreshUI(self.selectedTanBtn.data)

    def handleChangeModeBtnClick(self, *args):
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_CONTROL)

    def handleUnlockKeyClick(self, *args):
        e = ASObject(args[3][0])
        if self.selectedKey:
            self.changeKey(int(-1), int(0), self.selectedKey.pos[0], self.selectedKey.pos[1], e.currentTarget.parent.forbidChange)

    def handleDefaultBtnClick(self, *args):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg=gameStrings.KEYSETTING_TEXT4, title='', yesCallback=self._defaultSetting)

    def getModePlusKeys(self, mode):
        if mode == gameglobal.KEYBOARD_MODE:
            return gameglobal.KEYBOARD_PLUS_KEYS
        if mode == gameglobal.MOUSE_MODE:
            return gameglobal.MOUSE_PLUS_KEYS
        if mode == gameglobal.ACTION_MODE:
            return gameglobal.ACTION_PLUS_KEYS

    def getModePlus(self, mode):
        if mode == gameglobal.KEYBOARD_MODE:
            return gameglobal.KEYBOARD_PLUS
        if mode == gameglobal.MOUSE_MODE:
            return gameglobal.MOUSE_PLUS
        if mode == gameglobal.ACTION_MODE:
            return gameglobal.ACTION_PLUS

    def _defaultSetting(self):
        p = BigWorld.player()
        operationMode = p.getSavedOperationMode()
        plus = self.getModePlus(operationMode)
        data = []
        for item in self.getModePlusKeys(operationMode):
            if item == gameglobal.PLUS_AIMCROSS_KEY:
                data.append(p.operation.get(plus, {}).get(item, 9))
            else:
                data.append(p.operation.get(plus, {}).get(item, 0))

        HK.setDefaultHotkey()
        self.hotKeyManager.saveHotKey()
        self.refreshDataAndUI()
        BigWorld.player().reload()
        operationMode = p.getSavedOperationMode()
        plus = self.getModePlus(operationMode)
        HK.setCastSelfKey(data[0])
        p.operation[plus][gameglobal.PLUS_SELF_KEY] = data[0]
        if operationMode == gameglobal.ACTION_MODE and len(data) > 1:
            HK.setShowCursorKey(data[1])
            p.operation[plus][gameglobal.PLUS_SHOW_CURSOR_KEY] = data[1]
            gameglobal.rds.ui.systemButton.setActionModeIndicator(True, data[1])
        if operationMode == gameglobal.ACTION_MODE and len(data) > 2:
            p.operation[plus][gameglobal.PLUS_AIMCROSS_KEY] = data[2]
            gameglobal.rds.ui.changeAimCross(data[2])
        keyboardEffect.refreshHotkeyEffect()
        if gameglobal.rds.ui.assign.auctionMediator:
            gameglobal.rds.ui.assign.setAuctionHotKey()
        if gameglobal.rds.ui.assign.diceMediator:
            gameglobal.rds.ui.assign.setDiceHotKey()

    def handleConfirmBtnClick(self, *args):
        p = BigWorld.player()
        keyDef = HK.HKM[HK.KEY_PICK_ITEM]
        if not keyDef.key and not keyDef.key2:
            BigWorld.player().showTopMsg(gameStrings.KEYSETTING_TEXT5)
            return
        if not p._isOnZaijuOrBianyao() or formula.inDotaBattleField(getattr(p, 'mapID', 0)):
            self.hotKeyManager.saveHotKey()
            BigWorld.player().reload()
        gameglobal.rds.ui.gameSetting.hide()
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        if gameglobal.rds.ui.assign.auctionMediator:
            gameglobal.rds.ui.assign.setAuctionHotKey()
        if gameglobal.rds.ui.assign.diceMediator:
            gameglobal.rds.ui.assign.setDiceHotKey()
        if gameglobal.rds.ui.summonedSpriteUnitFrameV2.widget:
            gameglobal.rds.ui.summonedSpriteUnitFrameV2.setHotKeyText()
        keyboardEffect.refreshHotkeyEffect()

    def handleCancelBtnClick(self, *args):
        gameglobal.rds.ui.gameSetting.hide()
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def handleTabBtnClick(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if self.selectedKey:
            self.selectedKey.selected = False
            self.selectedKey = None
        if self.selectedTanBtn and target != self.selectedTanBtn:
            self.selectedTanBtn.selected = False
            self.selectedTanBtn = target
            self.selectedTanBtn.selected = True
            self.refreshUI(self.selectedTanBtn.data)

    def listLabelFunction(self, *args):
        data = ASObject(args[3][0])
        itemMC = ASObject(args[3][1])
        inBfDota = formula.inDotaBattleField(getattr(BigWorld.player(), 'mapID', 0))
        itemMC.data = data.tag
        itemMC.textField.text = data.name
        itemMC.key1.pos = data.pos1
        itemMC.key2.pos = data.pos2
        itemMC.key1.fixedSize = True
        itemMC.key2.fixedSize = True
        itemMC.key2.visible = not inBfDota
        itemMC.key1.textField.text = data.key1
        itemMC.key2.textField.text = data.key2
        itemMC.forbidChange = data.forbidChange
        itemMC.key1.addEventListener(events.MOUSE_DOWN, self.handleKeyMouseDown)
        itemMC.key2.addEventListener(events.MOUSE_DOWN, self.handleKeyMouseDown)
        itemMC.key1.gotoAndStop(0)
        itemMC.key2.gotoAndStop(0)

    def _setKey(self, keyCode, comkey):
        if self.selectedKey:
            self.selectedKey.removeEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyUp)
            self.selectedKey.removeEventListener(events.MOUSE_WHEEL, self.handleMouseWheel)
            self.selectedKey.textField.htmlText = self.selectedKey.textField.text
            self.selectedKey.selected = False
            self.selectedKey.gotoAndStop(0)
            self.changeKey(int(keyCode), int(comkey), self.selectedKey.pos[0], int(self.selectedKey.pos[1]), self.selectedKey.parent.forbidChange)
        self.selectedKey = None

    def selectKey(self, key):
        self.selectedKey = key
        self.selectedKey.textField.htmlText = '<b>' + self.selectedKey.textField.text
        self.selectedKey.selected = True
        self.selectedKey.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyUp)
        self.selectedKey.addEventListener(events.MOUSE_WHEEL, self.handleMouseWheel)

    def unselectKey(self):
        self.selectedKey.removeEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleKeyUp)
        self.selectedKey.removeEventListener(events.MOUSE_WHEEL, self.handleMouseWheel)
        self.selectedKey.textField.htmlText = self.selectedKey.textField.text
        self.selectedKey.selected = False
        self.selectedKey.gotoAndStop(0)
        self.selectedKey = None

    def handleKeyMouseDown(self, *args):
        e = ASObject(args[3][0])
        target = e.currentTarget
        if self.selectedKey:
            if self.selectedKey != target:
                self.unselectKey()
                self.selectKey(target)
            elif e.buttonIdx >= events.MIDDLE_BUTTON and e.buttonIdx <= events.MOUSE_FUNC7:
                self._setKey(e.buttonIdx + self.KEY_MOUSE_MIDDLE - events.MIDDLE_BUTTON, 0)
        else:
            self.selectKey(target)

    def handleKeyUp(self, *args):
        e = ASObject(args[3][0])
        comkey = self.getComKey(e.shiftKey, e.ctrlKey, e.altKey)
        self._setKey(e.keyCode, comkey)

    def getComKey(self, shiftKey, ctrlKey, altKey):
        if shiftKey:
            return 1
        if ctrlKey:
            return 2
        if altKey:
            return 4
        return 0

    def handleMouseWheel(self, *args):
        e = ASObject(args[3][0])
        b = self.KEY_MOUSE_ROLLDOWN
        if e.delta > 0:
            b = self.KEY_MOUSE_ROLLUP
        self._setKey(b, 0)
        e.stopImmediatePropagation()

    def changeKey(self, keyCode, mods, tag, pos, forbidChange):
        if forbidChange:
            BigWorld.player().showGameMsg(GMDD.data.DOTA_KEY_FORBID_CHANGE, ())
            return
        gamelog.debug('bgf:onChangeKey', keyCode, mods, tag, pos)
        if keyCode == -1:
            self.unlockKey(tag, pos)
            return
        if (keyCode, mods) in hotkeyProxy.excludeComKey:
            return
        if tag == 'hotBtn' and BigWorld.player()._isOnZaijuOrBianyao() and not formula.inDotaBattleField(getattr(BigWorld.player(), 'mapID', 0)):
            BigWorld.player().showTopMsg(gameStrings.KEYSETTING_TEXT6)
            return
        charCode = hotkeyProxy.decodeKeyCode(keyCode)
        if tag == 'moveBtn' and keyCode in (keys.KEY_MOUSE_ROLLUP, keys.KEY_MOUSE_ROLLDOWN):
            BigWorld.player().showTopMsg(gameStrings.KEYSETTING_TEXT7)
            return
        if utils.isInternationalVersion():
            gameCode = gameglobal.rds.lastKey
        else:
            gameCode = hotkeyProxy.getGameKey(keyCode)
        gamelog.debug('bgf:onChangeKey1', keyCode, charCode, gameCode)
        keyCol = pos / 10
        keyRow = pos % 10 + 1
        if self.hotKeyManager.keyMap[tag].defaultKey[keyCol]['key'] not in (HK.KEY_CHANGE_CURSOR,) and gameCode in (keys.KEY_LALT, keys.KEY_LSHIFT, keys.KEY_LCONTROL):
            BigWorld.player().showTopMsg(gameStrings.KEYSETTING_TEXT8)
            return
        if not gameCode:
            return
        keydef = HK.keyDef(gameCode, 1, mods)
        sameArray = self.hotKeyManager.searchSameKey(gameCode, mods)
        if len(sameArray):
            gamelog.debug('bgf:onChangeKey', sameArray)
            BigWorld.player().showTopMsg(gameStrings.KEYSETTING_TEXT9 % (keydef.getDesc(1), sameArray[0][1]))
            for item in sameArray:
                HK.HKM[item[2]].clearPart(item[3])

        else:
            BigWorld.player().showTopMsg(gameStrings.KEYSETTING_TEXT10)
        if self.hotKeyManager.keyMap[tag].defaultKey[keyCol]['key'] == HK.KEY_CHANGE_CURSOR:
            if gameCode == keys.KEY_LALT:
                mods = 4
            elif gameCode == keys.KEY_LCONTROL:
                mods = 2
            elif gameCode == keys.KEY_LSHIFT:
                mods = 1
        self.hotKeyManager.set(tag, keyCol, keyRow, gameCode, mods)
        text = self.hotKeyManager.getSingleKeyDesc(tag, keyCol, keyRow)
        self.setKeyContent(tag, pos, text)

    def unlockKey(self, tag, pos):
        keyCol = pos / 10
        keyRow = pos % 10 + 1
        self.hotKeyManager.set(tag, keyCol, keyRow, 0, 0)
        BigWorld.player().showTopMsg(gameStrings.KEYSETTING_TEXT11)
        text = self.hotKeyManager.getSingleKeyDesc(tag, keyCol, keyRow)
        self.setKeyContent(tag, pos, text)

    def setKeyContent(self, tag, pos, text):
        self.refreshDataAndUI()

    def getIdx(self, tag):
        for i in xrange(len(self.data)):
            if self.data[i][0]['tag'] == tag:
                return i

        return 0

    def refreshSwitch(self):
        self.oneSwitch = gameglobal.rds.configData.get('enableDelegation', False)

    def getKeyData(self):
        array = self.hotKeyManager.getKeyDesc()
        retArray = []
        for subArray in array:
            tag = subArray[0][1]
            obj = []
            for i, item in enumerate(subArray):
                data = {'name': item[0],
                 'key1': item[1],
                 'key2': item[2],
                 'forbidChange': item[3],
                 'tag': tag}
                obj.append(data)

            retArray.append(obj)

        return retArray

    def refreshUI(self, tabIndex):
        cnt = 0
        data = self.data[int(tabIndex)]
        dataArray = []
        for i, value in enumerate(data):
            if i == 0:
                continue
            if value['name'] == gameStrings.KEYSETTING_TEXT12:
                if not self.oneSwitch:
                    continue
            value['pos1'] = [value['tag'], cnt * 10 + 0]
            value['pos2'] = [value['tag'], cnt * 10 + 1]
            cnt = cnt + 1
            dataArray.append(value)

        self.scrollWindowList.dataArray = dataArray

    def updateSwitchAndUI(self):
        if not self.widget:
            return
        self.refreshSwitch()
        self.refreshUI(self.selectedTanBtn.data)

    def refreshDataAndUI(self):
        self.data = self.getKeyData()
        self.refreshUI(self.selectedTanBtn.data)

    def unRegisterPanel(self):
        p = BigWorld.player()
        if not p._isOnZaijuOrBianyao():
            HK.loadHotkey(p.hotkeyData)
            p.reload()
        if p and utils.instanceof(p, 'PlayerAvatar'):
            p.unlockKey(gameglobal.KEY_POS_UI)
            p.updateActionKeyState()
        self.scrollWindowList.dataArray = []
        self.widget = None
        self.widget = None
        self.mainMc = None
        self.scrollWindowList = None
        self.canvas = None
        self.oneSwitch = None
        self.data = []
        self.selectedTanBtn = None
        self.selectedKey = None
