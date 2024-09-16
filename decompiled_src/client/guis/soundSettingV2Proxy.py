#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/soundSettingV2Proxy.o
import BigWorld
import const
import gameglobal
import utils
import events
import Sound
import gametypes
import appSetting
import copy
import math
import hotkeyProxy
from guis import hotkey as HK
from gameStrings import gameStrings
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from uiProxy import UIProxy
from appSetting import Obj as AppSettings
from helpers import ccManager
import uiConst
from data import sys_config_data as SCD

class SoundSettingV2Proxy(UIProxy):
    SLIDER_ARRAY = ['masterSlider',
     'ambientSlider',
     'staticSlider',
     'fxSlider',
     'creatureSlider',
     'npcSlider',
     'systemSlider',
     'uiSlider',
     'musicSlider']
    CHECK_BOX_ARRAY = ['ambientCheck',
     'staticCheck',
     'fxCheck',
     'creatureCheck',
     'npcCheck',
     'systemCheck',
     'uiCheck',
     'musicCheck',
     'reverbCheck',
     'muteCheck',
     'muteOtherSpriteCheck']
    PREFER_TYPE_NONE = 0
    PREFER_TYPE_BATTLE = 1
    PREFER_TYPE_MUSIC = 2
    PREFER_TYPE_STORY = 3
    PREFER_TYPE_CHAT = 4
    PREFER_TEMPLATE = [[0.4,
      0.4,
      1,
      1,
      0.8,
      1,
      0.5,
      0.8],
     [0.7,
      0.7,
      0.8,
      0.8,
      0.7,
      1,
      1,
      0.7],
     [0.5,
      0.5,
      0.8,
      0.8,
      1,
      1,
      0.6,
      0.8],
     [0.2,
      0.2,
      0.35,
      0.35,
      0.2,
      0.2,
      0.2,
      0.2]]
    QUALITY_MAP = {'0': 256,
     '1': 128,
     '2': 64}
    QUALITY_MAP_REVERSE = {'256': 0,
     '128': 1,
     '64': 2}

    def __init__(self, uiAdapter):
        super(SoundSettingV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.canvas = None
        self.data = []
        self.needSetPrefer = True
        self.voiceSetting = False

    def setVoiceSetting(self):
        self.voiceSetting = True

    def initPanel(self, widget):
        self.widget = widget
        self.canvas = self.widget.canvas
        ASUtils.setDropdownMenuData(self.canvas.preferMenu, gameStrings.SOUNDSETTING_PREFER_MENU_DATA)
        self.canvas.preferMenu.addEventListener(events.INDEX_CHANGE, self.handlePreferMenu)
        ASUtils.setDropdownMenuData(self.canvas.qualityMenu, gameStrings.SOUNDSETTING_QUALITY_MENU_DATA)
        self.canvas.volumeCanvas.visible = not self.voiceSetting
        self.canvas.voiceCanvas.visible = self.voiceSetting
        self.canvas.volumeBtn.selected = not self.voiceSetting
        self.canvas.voiceBtn.selected = self.voiceSetting
        self.voiceSetting = False
        self.canvas.volumeBtn.addEventListener(events.BUTTON_CLICK, self.handleVolumeBtnClick)
        self.canvas.voiceBtn.addEventListener(events.BUTTON_CLICK, self.handleVoiceBtnClick)
        for name in self.SLIDER_ARRAY:
            slider = getattr(self.canvas.volumeCanvas, name, None)
            if slider:
                slider.minimum = 0
                slider.maximum = 100
                slider.validateNow()
                slider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange)

        for index, name in enumerate(self.CHECK_BOX_ARRAY):
            checkBox = getattr(self.canvas.volumeCanvas, name, None)
            if checkBox:
                checkBox.addEventListener(events.EVENT_SELECT, self.handleCheckBoxSelect)

        voiceSlider = ['volumeInSlider', 'volumeOutSlider']
        for name in voiceSlider:
            slider = getattr(self.canvas.voiceCanvas, name, None)
            if slider:
                slider.minimum = 0
                slider.maximum = 100
                slider.validateNow()
                slider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange)

        voiceRadio = ['freeModeRadio', 'keyModeRadio']
        for name in voiceRadio:
            radioBox = getattr(self.canvas.voiceCanvas, name, None)
            if radioBox:
                radioBox.addEventListener(events.EVENT_SELECT, self.handleRadioBoxSelect)

        keyTextMc = self.canvas.voiceCanvas.keyModeMc
        keyTextMc.addEventListener(events.MOUSE_DOWN, self.handleKeyTextMc)
        TipManager.addTip(keyTextMc, SCD.data.get('keyVoiceTextTip', ''))
        key, mod, desc = hotkeyProxy.getAsKeyContent(HK.KEY_VOICE)
        keyTextMc.textField.text = desc
        ccManager.instance().testMic(1, const.CC_SESSION_TEAM)
        self.canvas.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick)
        self.canvas.applyBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyBtnClick)
        self.canvas.defaultBtn.addEventListener(events.BUTTON_CLICK, self.handleDefaultBtnClick)
        self.canvas.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancleBtnClick)
        TipManager.addTip(self.canvas.volumeCanvas.masterLabel, gameStrings.SOUNDSETTING_TIPS_ARRAY[0])
        for index, name in enumerate(self.CHECK_BOX_ARRAY):
            checkBox = getattr(self.canvas.volumeCanvas, name, None)
            if checkBox and index + 1 < len(gameStrings.SOUNDSETTING_TIPS_ARRAY):
                TipManager.addTip(checkBox, gameStrings.SOUNDSETTING_TIPS_ARRAY[index + 1])

        TipManager.addTip(self.canvas.volumeCanvas.reverbCheck, gameStrings.SOUNDSETTING_TEXT1)
        TipManager.addTip(self.canvas.volumeCanvas.muteCheck, gameStrings.SOUNDSETTING_TEXT2)
        TipManager.addTip(self.canvas.qualityLabel, gameStrings.SOUNDSETTING_TEXT3)
        self.data = self.getSoundConfigData()
        self.refreshUI(self.data)
        self.canvas.applyBtn.enabled = False
        self.canvas.volumeCanvas.muteOtherSpriteCheck.visible = gameglobal.rds.configData.get('enableSummonedSprite', False)

    def handleKeyTextMc(self, *args):
        gameglobal.rds.ui.keySettingV2.setSelectIdx(4)
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_KEY)

    def setTestMicData(self, data):
        if not self.widget:
            return
        self.canvas.voiceCanvas.testInSlider.currentValue = math.ceil(data / 2.55)

    def handleVolumeBtnClick(self, *args):
        self.canvas.volumeBtn.selected = True
        self.canvas.voiceBtn.selected = False
        self.canvas.volumeCanvas.visible = True
        self.canvas.voiceCanvas.visible = False

    def handleVoiceBtnClick(self, *args):
        self.canvas.volumeBtn.selected = False
        self.canvas.voiceBtn.selected = True
        self.canvas.volumeCanvas.visible = False
        self.canvas.voiceCanvas.visible = True

    def handleRadioBoxSelect(self, *args):
        target = ASObject(args[3][0]).currentTarget
        radioBoxName = target.name
        if target.selected:
            if radioBoxName == 'freeModeRadio':
                ccManager.instance().startCapture(const.CC_SESSION_TEAM)
                self.canvas.voiceCanvas.keyModeMc.enabled = False
            elif radioBoxName == 'keyModeRadio':
                ccManager.instance().stopCapture(const.CC_SESSION_TEAM)
                self.canvas.voiceCanvas.keyModeMc.enabled = True

    def handlePreferMenu(self, *args):
        selectedIndex = ASObject(args[3][0]).currentTarget.selectedIndex
        if selectedIndex == -1 or selectedIndex == self.PREFER_TYPE_NONE:
            return
        else:
            self.needSetPrefer = False
            for i, name in enumerate(self.SLIDER_ARRAY):
                slider = getattr(self.canvas.volumeCanvas, name, None)
                if slider:
                    slider.value = int(slider.maximum * self.PREFER_TEMPLATE[selectedIndex - 1][i - 1])

            self.needSetPrefre = True
            self.canvas.applyBtn.enabled = True
            return

    def handleSliderValueChange(self, *args):
        target = ASObject(args[3][0]).currentTarget
        sliderName = target.name
        val = int(target.value)
        if sliderName == 'masterSlider':
            Sound.setSoundVolume(val)
            if hasattr(Sound, 'setRawfileVolume'):
                Sound.setRawfileVolume(val)
        elif sliderName == 'ambientSlider':
            Sound.setAmbientVolume(val)
        elif sliderName == 'staticSlider':
            Sound.setStaticVolume(val)
        elif sliderName == 'fxSlider':
            Sound.setCategoryVolume(gametypes.CATEGORY_CHAR, val)
        elif sliderName == 'npcSlider':
            Sound.setCategoryVolume(gametypes.CATEGORY_NPC, val)
            if hasattr(Sound, 'setRawfileVolume'):
                Sound.setRawfileVolume(min(val, Sound.getSoundVolume()))
        elif sliderName == 'uiSlider' and appSetting.SoundSettingObj.isUiEnable():
            Sound.setUiVolume(val)
        elif sliderName == 'musicSlider':
            Sound.setMusicVolume(val)
        elif sliderName == 'creatureSlider':
            Sound.setCategoryVolume(gametypes.CATEGORY_CREATURE, val)
        elif sliderName == 'systemSlider':
            Sound.setCategoryVolume(gametypes.CATEGORY_SYSTEM, val)
        elif sliderName == 'volumeInSlider':
            ccManager.instance().setCaptureVolume(val)
        elif sliderName == 'volumeOutSlider':
            ccManager.instance().setPlaybackVolume(val)
        sliderTextName = sliderName[0:-6] + 'Text'
        sliderText = getattr(self.canvas.volumeCanvas, sliderTextName, {})
        if sliderText:
            sliderText.text = str(val)
        else:
            sliderText = getattr(self.canvas.voiceCanvas, sliderTextName, {})
            if sliderText:
                sliderText.text = str(val)
        if self.needSetPrefer:
            self.canvas.preferMenu.selectedIndex = self.PREFER_TYPE_NONE
        self.canvas.applyBtn.enabled = True

    def handleCheckBoxSelect(self, *args):
        target = ASObject(args[3][0]).target
        sliderCheckBoxName = target.name
        sliderCheckBoxSelected = target.selected
        if sliderCheckBoxName == 'ambientCheck':
            Sound.enableAmbient(sliderCheckBoxSelected)
        elif sliderCheckBoxName == 'staticCheck':
            Sound.enableStatic(sliderCheckBoxSelected)
        elif sliderCheckBoxName == 'fxCheck':
            Sound.enableCategory(gametypes.CATEGORY_CHAR, sliderCheckBoxSelected)
        elif sliderCheckBoxName == 'npcCheck':
            Sound.enableCategory(gametypes.CATEGORY_NPC, sliderCheckBoxSelected)
            if hasattr(Sound, 'setRawfileVolume'):
                if sliderCheckBoxSelected:
                    Sound.setRawfileVolume(min(Sound.getCategoryVolume(gametypes.CATEGORY_NPC), Sound.getSoundVolume()))
                else:
                    Sound.setRawfileVolume(0)
        elif sliderCheckBoxName == 'uiCheck':
            Sound.enableUi(sliderCheckBoxSelected)
        elif sliderCheckBoxName == 'musicCheck':
            Sound.enableMusic(sliderCheckBoxSelected)
        elif sliderCheckBoxName == 'reverbCheck':
            Sound.enableReverb(sliderCheckBoxSelected)
        elif sliderCheckBoxName == 'muteCheck':
            appSetting.SoundSettingObj.enableBgSound(sliderCheckBoxSelected)
        elif sliderCheckBoxName == 'creatureCheck':
            Sound.enableCategory(gametypes.CATEGORY_CREATURE, sliderCheckBoxSelected)
        elif sliderCheckBoxName == 'systemCheck':
            Sound.enableCategory(gametypes.CATEGORY_SYSTEM, sliderCheckBoxSelected)
        sliderName = sliderCheckBoxName[0:-5] + 'Slider'
        slider = getattr(self.canvas.volumeCanvas, sliderName, None)
        if slider:
            slider.enabled = sliderCheckBoxSelected

    def handleConfirmBtnClick(self, *args):
        self.ui2Data(self.data)
        appSetting.SoundSettingObj._value = copy.deepcopy(self.data)
        AppSettings.save()
        gameglobal.rds.sound.playSound(gameglobal.SD_2)
        gameglobal.rds.ui.gameSetting.hide()

    def handleApplyBtnClick(self, *args):
        self.ui2Data(self.data)
        appSetting.SoundSettingObj._value = copy.deepcopy(self.data)
        AppSettings.save()

    def handleDefaultBtnClick(self, *args):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.SOUNDSETTING_TEXT4, self._defaultSetting)

    def _defaultSetting(self):
        appSetting.SoundSettingObj.default()
        appSetting.SoundSettingObj.apply()
        self.data = self.getSoundConfigData()
        self.refreshUI(self.data)

    def handleCancleBtnClick(self, *args):
        self.ui2Data(self.data)
        appSetting.SoundSettingObj.applyOrigin(self.data)
        gameglobal.rds.sound.playSound(gameglobal.SD_3)
        gameglobal.rds.ui.gameSetting.hide()

    def getSoundConfigData(self):
        return copy.deepcopy(appSetting.SoundSettingObj._value)

    def refreshUI(self, data):
        self.canvas.volumeCanvas.masterSlider.value = data[0]
        self.canvas.volumeCanvas.ambientSlider.value = data[1]
        self.canvas.volumeCanvas.staticSlider.value = data[3]
        self.canvas.volumeCanvas.fxSlider.value = data[5]
        self.canvas.volumeCanvas.creatureSlider.value = data[15]
        self.canvas.volumeCanvas.npcSlider.value = data[7]
        self.canvas.volumeCanvas.uiSlider.value = data[9]
        self.canvas.volumeCanvas.musicSlider.value = data[11]
        self.canvas.volumeCanvas.systemSlider.value = data[17]
        self.canvas.volumeCanvas.ambientCheck.selected = data[2]
        self.canvas.volumeCanvas.staticCheck.selected = data[4]
        self.canvas.volumeCanvas.fxCheck.selected = data[6]
        self.canvas.volumeCanvas.creatureCheck.selected = data[16]
        self.canvas.volumeCanvas.npcCheck.selected = data[8]
        self.canvas.volumeCanvas.uiCheck.selected = data[10]
        self.canvas.volumeCanvas.musicCheck.selected = data[12]
        self.canvas.volumeCanvas.systemCheck.selected = data[18]
        self.canvas.volumeCanvas.reverbCheck.selected = data[13]
        self.canvas.volumeCanvas.muteCheck.selected = data[14]
        self.canvas.volumeCanvas.muteOtherSpriteCheck.selected = data[21]
        self.canvas.volumeCanvas.ambientSlider.enabled = data[2]
        self.canvas.volumeCanvas.staticSlider.enabled = data[4]
        self.canvas.volumeCanvas.fxSlider.enabled = data[6]
        self.canvas.volumeCanvas.creatureSlider.enabled = data[16]
        self.canvas.volumeCanvas.npcSlider.enabled = data[8]
        self.canvas.volumeCanvas.uiSlider.enabled = data[10]
        self.canvas.volumeCanvas.musicSlider.enabled = data[12]
        self.canvas.volumeCanvas.systemSlider.enabled = data[18]
        self.canvas.voiceCanvas.freeModeRadio.selected = not data[22]
        self.canvas.voiceCanvas.keyModeRadio.selected = data[22]
        self.canvas.voiceCanvas.volumeInSlider.value = data[23]
        self.canvas.voiceCanvas.volumeOutSlider.value = data[24]
        self.canvas.qualityMenu.selectedIndex = self.QUALITY_MAP_REVERSE[str(int(data[19]))]
        self.canvas.preferMenu.selectedIndex = data[20]

    def ui2Data(self, data):
        data[0] = int(self.canvas.volumeCanvas.masterSlider.value)
        data[1] = int(self.canvas.volumeCanvas.ambientSlider.value)
        data[3] = int(self.canvas.volumeCanvas.staticSlider.value)
        data[5] = int(self.canvas.volumeCanvas.fxSlider.value)
        data[15] = int(self.canvas.volumeCanvas.creatureSlider.value)
        data[7] = int(self.canvas.volumeCanvas.npcSlider.value)
        data[9] = int(self.canvas.volumeCanvas.uiSlider.value)
        data[11] = int(self.canvas.volumeCanvas.musicSlider.value)
        data[17] = int(self.canvas.volumeCanvas.systemSlider.value)
        data[2] = int(self.canvas.volumeCanvas.ambientCheck.selected)
        data[4] = int(self.canvas.volumeCanvas.staticCheck.selected)
        data[6] = int(self.canvas.volumeCanvas.fxCheck.selected)
        data[16] = int(self.canvas.volumeCanvas.creatureCheck.selected)
        data[8] = int(self.canvas.volumeCanvas.npcCheck.selected)
        data[10] = int(self.canvas.volumeCanvas.uiCheck.selected)
        data[12] = int(self.canvas.volumeCanvas.musicCheck.selected)
        data[18] = int(self.canvas.volumeCanvas.systemCheck.selected)
        data[13] = int(self.canvas.volumeCanvas.reverbCheck.selected)
        data[14] = int(self.canvas.volumeCanvas.muteCheck.selected)
        data[19] = int(self.QUALITY_MAP[str(int(self.canvas.qualityMenu.selectedIndex))])
        data[20] = int(self.canvas.preferMenu.selectedIndex)
        data[21] = int(self.canvas.volumeCanvas.muteOtherSpriteCheck.selected)
        data[22] = int(self.canvas.voiceCanvas.keyModeRadio.selected)
        data[23] = int(self.canvas.voiceCanvas.volumeInSlider.value)
        data[24] = int(self.canvas.voiceCanvas.volumeOutSlider.value)

    def unRegisterPanel(self):
        appSetting.SoundSettingObj.apply()
        self.widget = None
        ccManager.instance().testMic(0, const.CC_SESSION_TEAM)
