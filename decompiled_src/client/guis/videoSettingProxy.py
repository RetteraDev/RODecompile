#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/videoSettingProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gametypes
import events
import const
import uiConst
import appSetting
import C_ui
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import TipManager
from callbackHelper import Functor
from gameStrings import gameStrings
from guis.asObject import ASUtils
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from appSetting import Obj as AppSettings
from helpers import tickManager
DI_IMG = 0
ZHONG_IMG = 1
HIGH_IMG = 2
QUALITY_IMAGE = [DI_IMG, ZHONG_IMG, HIGH_IMG]
KEY_FRAME_NAMES = ['di', 'zhong', 'gao']

class VideoSettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VideoSettingProxy, self).__init__(uiAdapter)
        self.indexOffset = 1
        self.CKBOXLABEL_NUM = 21
        self.CKBOXSHADER_NUM = 7
        self.SENIOR_ARRAY = ['ckBoxMotionBlur',
         'ckBoxScreenEffect',
         'ckBoxAnimateCamera',
         'ckBoxCamerShake',
         'ckBoxDisableSkillHover',
         'ckBoxShowBloodLabel',
         'ckBoxHitFreeze',
         'ckBoxModelShake',
         'ckBoxBloom',
         'ckBoxWsEffect',
         'ckBoxDarkAngle',
         'ckDOF',
         'ckBoxShowEquipEnhanceEffect',
         'ckBoxEnablePhysics',
         'ckBoxMemorySetting']
        self.widget = None
        self.mainMc = None
        self.scrollWindowContent = None
        self.videoConfigData = []
        self.tipsData = {}
        self.windowData = {}
        self.resolutionArray = []

    def initPanel(self, widget):
        self.widget = widget
        self.mainMc = self.widget.canvas
        self.scrollWindowContent = self.widget.canvas.scrollWindow.canvas
        self.mainMc.resolutionMenu.selectedIndex = 0
        self.resolutionArray = self.createResolutionArray()
        ASUtils.setDropdownMenuData(self.mainMc.resolutionMenu, self.resolutionArray)
        self.mainMc.windowMenu.selectedIndex = 0
        windowData = self.createWindowArray()
        ASUtils.setDropdownMenuData(self.mainMc.windowMenu, windowData)
        self.imgPageIndex = 0
        self.scrollWindowContent.ckQualityMin.groupName = 'qualityGroup'
        self.scrollWindowContent.ckQuality0.groupName = 'qualityGroup'
        self.scrollWindowContent.ckQuality1.groupName = 'qualityGroup'
        self.scrollWindowContent.ckQuality2.groupName = 'qualityGroup'
        self.scrollWindowContent.ckQuality3.groupName = 'qualityGroup'
        self.scrollWindowContent.ckQuality4.groupName = 'qualityGroup'
        self.scrollWindowContent.ckQualityCustom.groupName = 'qualityGroup'
        self.scrollWindowContent.ckQualityMin.addEventListener(events.BUTTON_CLICK, self.handleClickCkQualityMin, False, 0, True)
        self.scrollWindowContent.ckQuality0.addEventListener(events.BUTTON_CLICK, self.handleClickCkQuality, False, 0, True)
        self.scrollWindowContent.ckQuality1.addEventListener(events.BUTTON_CLICK, self.handleClickCkQuality, False, 0, True)
        self.scrollWindowContent.ckQuality2.addEventListener(events.BUTTON_CLICK, self.handleClickCkQuality, False, 0, True)
        self.scrollWindowContent.ckQuality3.addEventListener(events.BUTTON_CLICK, self.handleClickCkQuality, False, 0, True)
        self.scrollWindowContent.ckQuality4.addEventListener(events.BUTTON_CLICK, self.handleClickCkQuality, False, 0, True)
        self.scrollWindowContent.ckQualityCustom.addEventListener(events.BUTTON_CLICK, self.handleClickCkQualityCustom, False, 0, True)
        self.scrollWindowContent.ckShader0.groupName = 'shaderGroup'
        self.scrollWindowContent.ckShader1.groupName = 'shaderGroup'
        self.scrollWindowContent.ckShader2.groupName = 'shaderGroup'
        self.scrollWindowContent.ckShader3.groupName = 'shaderGroup'
        self.scrollWindowContent.ckShader4.groupName = 'shaderGroup'
        self.scrollWindowContent.ckShader5.groupName = 'shaderGroup'
        self.scrollWindowContent.ckShader6.groupName = 'shaderGroup'
        self.mainMc.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmClick, False, 0, True)
        self.mainMc.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelClick, False, 0, True)
        self.mainMc.applyBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyClick, False, 0, True)
        self.mainMc.defaultBtn.addEventListener(events.BUTTON_CLICK, self.handleDefaultClick, False, 0, True)
        self.scrollWindowContent.ckDOF.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxMotionBlur.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxScreenEffect.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxAnimateCamera.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxCamerShake.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxDisableSkillHover.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxHitFreeze.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxShowBloodLabel.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxModelShake.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxBloom.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxWsEffect.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxDarkAngle.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxShowEquipEnhanceEffect.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxEnablePhysics.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.ckBoxMemorySetting.addEventListener(events.BUTTON_CLICK, self.handleClickckFXCK, False, 0, True)
        self.scrollWindowContent.HQLSSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.FXAASlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.SkinLightSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.PlayerEffSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.AvatarEffSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.MonsterEffSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.NpcEffSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.EnemyAvatarEffSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.FloraDensitySlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.FloraLODScaleSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.ModelLODScaleSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.ModelShowNumSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.effShowNumSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.foregroundFPSSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.backgroundFPSSlider.addEventListener(events.EVENT_SLIDER_DRAG_END, self.handleSliderDragEnd, False, 0, True)
        self.scrollWindowContent.HQLSSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.FXAASlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.SkinLightSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.PlayerEffSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.AvatarEffSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.MonsterEffSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.NpcEffSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.EnemyAvatarEffSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.FloraDensitySlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.FloraLODScaleSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.ModelLODScaleSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.ModelShowNumSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.effShowNumSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.foregroundFPSSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.scrollWindowContent.backgroundFPSSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleSliderValueChange, False, 0, True)
        self.widget.pageRenderFunc = self.pageItemFunc
        self.callbackId = BigWorld.callback(0.1, self.setImgData)
        self.scrollWindowContent.HQLSSlider.disableWheel = True
        self.scrollWindowContent.FXAASlider.disableWheel = True
        self.scrollWindowContent.SkinLightSlider.disableWheel = True
        self.scrollWindowContent.PlayerEffSlider.disableWheel = True
        self.scrollWindowContent.AvatarEffSlider.disableWheel = True
        self.scrollWindowContent.MonsterEffSlider.disableWheel = True
        self.scrollWindowContent.NpcEffSlider.disableWheel = True
        self.scrollWindowContent.EnemyAvatarEffSlider.disableWheel = True
        self.scrollWindowContent.FloraDensitySlider.disableWheel = True
        self.scrollWindowContent.FloraLODScaleSlider.disableWheel = True
        self.scrollWindowContent.ModelLODScaleSlider.disableWheel = True
        self.scrollWindowContent.ModelShowNumSlider.disableWheel = True
        self.scrollWindowContent.effShowNumSlider.disableWheel = True
        self.scrollWindowContent.foregroundFPSSlider.disableWheel = True
        self.scrollWindowContent.backgroundFPSSlider.disableWheel = True
        self.windowData = self.getWindowData()
        self.getVideoConfigData()
        self.refreshUI()
        self.getTipsData()
        self.configTips()
        self.showImage()

    def showImage(self):
        self.mainMc.pageList.showIndicator = True
        self.mainMc.pageList.interval = 1.0
        self.mainMc.pageList.indicatorItemRenderName = 'VideoSettingV2_IndicatorFlag'

    def setImgData(self, *args):
        if not self.widget:
            return
        self.mainMc.pageList.data = QUALITY_IMAGE
        self.mainMc.pageList.indicator.update(self.imgPageIndex)
        self.mainMc.pageList.validateNow()
        BigWorld.cancelCallback(self.callbackId)

    def pageItemFunc(self, *args):
        if not self.widget:
            return
        convertMc = ASObject(args[3][0])
        if args[3][0].IsNull():
            convertMc = self.widget.getInstByClsName('VideoSettingV2_Qimage')
        direction = int(args[3][1].GetNumber())
        self.imgPageIndex = direction
        convertMc.gotoAndStop(KEY_FRAME_NAMES[self.imgPageIndex])
        self.mainMc.pageList.indicator.update(self.imgPageIndex)
        return convertMc

    def handleConfirmClick(self, *args):
        self.ui2VideoConfigData()
        appSetting.VideoQualitySettingObj.apply(self.videoConfigData[self.indexOffset:])
        appSetting.VideoQualitySettingObj._value = self.videoConfigData[self.indexOffset:]
        if gameglobal.rds.GameState != gametypes.GS_START:
            appSetting.setShaderIndex(self.videoConfigData[self.indexOffset - 1], True, True)
        else:
            appSetting.setShaderIndex(self.videoConfigData[self.indexOffset - 1], True, False)
        gameglobal.rds.ui.topBar.updateMode('renderMode')
        gameglobal.rds.ui.gameSetting.hide()
        AppSettings.save()
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def handleCancelClick(self, *args):
        gameglobal.rds.ui.gameSetting.hide()
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def handleApplyClick(self, *args):
        self.ui2VideoConfigData()
        appSetting.VideoQualitySettingObj.apply(self.videoConfigData[self.indexOffset:])
        appSetting.VideoQualitySettingObj._value = self.videoConfigData[self.indexOffset:]
        if gameglobal.rds.GameState != gametypes.GS_START:
            appSetting.setShaderIndex(self.videoConfigData[self.indexOffset - 1], True, True)
        else:
            appSetting.setShaderIndex(self.videoConfigData[self.indexOffset - 1], True, False)
        gameglobal.rds.ui.topBar.updateMode('renderMode')
        AppSettings.save()
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def handleDefaultClick(self, *args):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.VIDEO_SETTING_CHECK, self._defaultSetting)

    def _defaultSetting(self):
        appSetting.VideoQualitySettingObj.default()
        appSetting.VideoQualitySettingObj.apply()
        self.getVideoConfigData()
        self.refreshUI()

    def handleClickckFXCK(self, *args):
        self.scrollWindowContent.ckQualityCustom.selected = True

    def handleClickCkQualityMin(self, *args):
        self.togglePanel()

    def handleClickCkQualityCustom(self, *args):
        self.togglePanel()

    def handleClickCkQuality(self, *args):
        targetCKQuality = ASObject(args[3][0]).currentTarget
        targetName = targetCKQuality.name
        quality = appSetting.VideoQualitySettingObj.getRealVideoQualityLv(int(targetName[-1]))
        retArray = appSetting.VideoQualitySettingObj.getVideoQuality(quality)
        for i in range(0, len(retArray)):
            self.videoConfigData[self.indexOffset + i] = retArray[i]

        self.refreshUI()

    def getVideoConfigData(self):
        if len(self.videoConfigData) == 0:
            self.videoConfigData.append(appSetting.getShaderIndex())
            for item in appSetting.VideoQualitySettingObj._value:
                self.videoConfigData.append(item)

        else:
            self.videoConfigData[0] = appSetting.getShaderIndex()
            newData = appSetting.VideoQualitySettingObj._value
            for i in xrange(len(newData)):
                self.videoConfigData[self.indexOffset + i] = newData[i]

    def getWindowData(self):
        windowData = {}
        w, h, windowed, _ = BigWorld.getScreenState()
        if BigWorld.realFullScreen():
            windowed = 2
        windowData['width'] = w
        windowData['height'] = h
        windowData['window'] = windowed
        return windowData

    def togglePanel(self):
        value = not self.scrollWindowContent.ckQualityMin.selected
        for i in xrange(self.scrollWindowContent.numChildren):
            mc = self.scrollWindowContent.getChildAt(i)
            if mc.name[0:5] == 'ckBox' or mc.name[-6:len(mc.name)] == 'Slider':
                mc.enabled = value

    def refreshUI(self):
        if self.windowData.has_key('width') and self.windowData.has_key('height'):
            for i in xrange(len(self.resolutionArray)):
                if self.resolutionArray[i]['data'][0] == self.windowData['width'] and self.resolutionArray[i]['data'][1] == self.windowData['height']:
                    self.mainMc.resolutionMenu.selectedIndex = i
                    break

        if self.windowData.has_key('window'):
            self.mainMc.windowMenu.selectedIndex = self.windowData['window']
        getattr(self.scrollWindowContent, 'ckShader' + str(self.videoConfigData[0])).selected = True
        getattr(self.scrollWindowContent, 'ckQuality' + str(self.videoConfigData[2])).selected = True
        quality = appSetting.VideoQualitySettingObj.getRealVideoQualityLv(self.videoConfigData[2])
        dataArray = appSetting.VideoQualitySettingObj.getVideoQuality(quality)
        for i in xrange(len(dataArray)):
            if self.videoConfigData[i + self.indexOffset] != dataArray[i]:
                self.scrollWindowContent.ckQualityCustom.selected = True
                break

        self.scrollWindowContent.ckQualityMin.selected = self.videoConfigData[36]
        self.togglePanel()
        self.scrollWindowContent.FXAASlider.value = self.videoConfigData[7]
        self.scrollWindowContent.HQLSSlider.value = self.videoConfigData[11]
        self.scrollWindowContent.PlayerEffSlider.value = self.videoConfigData[14] + 1
        self.scrollWindowContent.AvatarEffSlider.value = self.videoConfigData[15] + 1
        self.scrollWindowContent.MonsterEffSlider.value = self.videoConfigData[16] + 1
        self.scrollWindowContent.NpcEffSlider.value = self.videoConfigData[17] + 1
        self.scrollWindowContent.EnemyAvatarEffSlider.value = self.videoConfigData[18] + 1
        self.scrollWindowContent.ckDOF.selected = self.videoConfigData[8]
        self.scrollWindowContent.ckBoxMotionBlur.selected = self.videoConfigData[19]
        self.scrollWindowContent.ckBoxScreenEffect.selected = self.videoConfigData[20]
        self.scrollWindowContent.ckBoxAnimateCamera.selected = self.videoConfigData[21]
        self.scrollWindowContent.ckBoxCamerShake.selected = self.videoConfigData[22]
        self.scrollWindowContent.ckBoxDisableSkillHover.selected = self.videoConfigData[23]
        self.scrollWindowContent.ckBoxHitFreeze.selected = self.videoConfigData[24]
        self.scrollWindowContent.ckBoxShowBloodLabel.selected = self.videoConfigData[25]
        self.scrollWindowContent.ckBoxModelShake.selected = self.videoConfigData[26]
        self.scrollWindowContent.ckBoxBloom.selected = self.videoConfigData[27]
        self.scrollWindowContent.ckBoxWsEffect.selected = self.videoConfigData[28]
        self.scrollWindowContent.ckBoxDarkAngle.selected = self.videoConfigData[29]
        self.scrollWindowContent.foregroundFPSSlider.value = self.videoConfigData[31]
        self.scrollWindowContent.backgroundFPSSlider.value = self.videoConfigData[32]
        self.scrollWindowContent.ckBoxShowEquipEnhanceEffect.selected = self.videoConfigData[33]
        self.scrollWindowContent.ckBoxEnablePhysics.selected = self.videoConfigData[34]
        self.scrollWindowContent.ckBoxMemorySetting.selected = self.videoConfigData[35]
        self.scrollWindowContent.SkinLightSlider.value = self.videoConfigData[37]
        self.scrollWindowContent.FloraDensitySlider.value = self.videoConfigData[38]
        self.scrollWindowContent.FloraLODScaleSlider.value = self.videoConfigData[39]
        self.scrollWindowContent.ModelLODScaleSlider.value = self.videoConfigData[40]
        self.scrollWindowContent.ModelShowNumSlider.value = self.videoConfigData[43]
        self.scrollWindowContent.effShowNumSlider.value = self.videoConfigData[44]

    def ui2VideoConfigData(self):
        index = self.mainMc.resolutionMenu.selectedIndex
        self.windowData['width'] = self.resolutionArray[index]['data'][0]
        self.windowData['height'] = self.resolutionArray[index]['data'][1]
        self.windowData['window'] = self.mainMc.windowMenu.selectedIndex
        self.showWarningMessage(self.windowData['width'], self.windowData['height'], self.windowData['window'])
        appSetting.setScreenSize(self.windowData['width'], self.windowData['height'], self.windowData['window'], True)
        for i in xrange(7):
            if getattr(self.scrollWindowContent, 'ckShader' + str(i)).selected:
                self.videoConfigData[0] = int(i)
                break

        for i in xrange(5):
            if getattr(self.scrollWindowContent, 'ckQuality' + str(i)).selected:
                self.videoConfigData[2] = int(i)
                break

        self.videoConfigData[36] = int(self.scrollWindowContent.ckQualityMin.selected)
        self.videoConfigData[7] = int(self.scrollWindowContent.FXAASlider.value)
        self.videoConfigData[11] = int(self.scrollWindowContent.HQLSSlider.value)
        self.videoConfigData[14] = int(self.scrollWindowContent.PlayerEffSlider.value - 1)
        self.videoConfigData[15] = int(self.scrollWindowContent.AvatarEffSlider.value - 1)
        self.videoConfigData[16] = int(self.scrollWindowContent.MonsterEffSlider.value - 1)
        self.videoConfigData[17] = int(self.scrollWindowContent.NpcEffSlider.value - 1)
        self.videoConfigData[18] = int(self.scrollWindowContent.EnemyAvatarEffSlider.value - 1)
        self.videoConfigData[8] = int(self.scrollWindowContent.ckDOF.selected)
        self.videoConfigData[19] = int(self.scrollWindowContent.ckBoxMotionBlur.selected)
        self.videoConfigData[20] = int(self.scrollWindowContent.ckBoxScreenEffect.selected)
        self.videoConfigData[21] = int(self.scrollWindowContent.ckBoxAnimateCamera.selected)
        self.videoConfigData[22] = int(self.scrollWindowContent.ckBoxCamerShake.selected)
        self.videoConfigData[23] = int(self.scrollWindowContent.ckBoxDisableSkillHover.selected)
        self.videoConfigData[24] = int(self.scrollWindowContent.ckBoxHitFreeze.selected)
        self.videoConfigData[25] = int(self.scrollWindowContent.ckBoxShowBloodLabel.selected)
        self.videoConfigData[26] = int(self.scrollWindowContent.ckBoxModelShake.selected)
        self.videoConfigData[27] = int(self.scrollWindowContent.ckBoxBloom.selected)
        self.videoConfigData[28] = int(self.scrollWindowContent.ckBoxWsEffect.selected)
        self.videoConfigData[29] = int(self.scrollWindowContent.ckBoxDarkAngle.selected)
        self.videoConfigData[31] = int(self.scrollWindowContent.foregroundFPSSlider.value)
        self.videoConfigData[32] = int(self.scrollWindowContent.backgroundFPSSlider.value)
        self.videoConfigData[33] = int(self.scrollWindowContent.ckBoxShowEquipEnhanceEffect.selected)
        self.videoConfigData[34] = int(self.scrollWindowContent.ckBoxEnablePhysics.selected)
        self.videoConfigData[35] = int(self.scrollWindowContent.ckBoxMemorySetting.selected)
        self.videoConfigData[37] = int(self.scrollWindowContent.SkinLightSlider.value)
        self.videoConfigData[38] = int(self.scrollWindowContent.FloraDensitySlider.value)
        self.videoConfigData[39] = int(self.scrollWindowContent.FloraLODScaleSlider.value)
        self.videoConfigData[40] = int(self.scrollWindowContent.ModelLODScaleSlider.value)
        self.videoConfigData[43] = int(self.scrollWindowContent.ModelShowNumSlider.value)
        self.videoConfigData[44] = int(self.scrollWindowContent.effShowNumSlider.value)

    def handleSliderDragEnd(self, *args):
        self.scrollWindowContent.ckQualityCustom.selected = True

    def handleSliderValueChange(self, *args):
        e = ASObject(args[3][0])
        targerSlider = ASObject(args[3][0]).currentTarget
        self.updateSliderText(targerSlider)
        e.stopImmediatePropagation()

    def updateSliderText(self, slider):
        sliderName = slider.name
        textName = sliderName[:-6] + 'Text'
        mc = self.scrollWindowContent.getChildByName(textName)
        if slider.maximum == 1:
            mc.text = gameStrings.VIDEO_SETTING_LV2[int(slider.value)]
        elif slider.maximum == 3:
            mc.text = gameStrings.VIDEO_SETTING_LV4[int(slider.value)]
        elif slider.maximum == 5:
            mc.text = gameStrings.VIDEO_SETTING_LV6[int(slider.value)]
        elif slider.maximum == 2:
            mc.text = gameStrings.VIDEO_SETTING_LV3[int(slider.value)]
        elif slider.maximum == 4:
            mc.text = gameStrings.VIDEO_SETTING_LV5[int(slider.value)]
        if sliderName == 'foregroundFPSSlider' or sliderName == 'backgroundFPSSlider':
            mc.text = slider.value
            if slider.value >= 61:
                mc.text = gameStrings.TEXT_VEHICLECHOOSEPROXY_123
        elif sliderName == 'SkinLightSlider':
            mc.text = slider.value

    def getTipsData(self):
        self.tipsData['labelTips'] = []
        self.tipsData['shaderTips'] = []
        self.tipsData['seniorTips'] = []
        for i in xrange(uiConst.VIDEO_SETTING_LABEL_NUM):
            self.tipsData['labelTips'].append(GMD.data.get(getattr(GMDD.data, 'VIDEO_SETTING_LABEL' + str(i), 0), {}).get('text', ''))

        for i in xrange(uiConst.VIDEO_SETTING_SHADER_NUM):
            self.tipsData['shaderTips'].append(GMD.data.get(getattr(GMDD.data, 'VIDEO_SETTING_SHADER' + str(i), 0), {}).get('text', ''))

        for i in xrange(uiConst.VIDEO_SETTING_SENIOR_NUM):
            self.tipsData['seniorTips'].append(GMD.data.get(getattr(GMDD.data, 'VIDEO_SETTING_SENIOR' + str(i), 0), {}).get('text', ''))

    def configTips(self):
        for i in range(0, self.CKBOXLABEL_NUM):
            if getattr(self.scrollWindowContent, 'ckLabel' + str(i)) != None:
                TipManager.addTip(getattr(self.scrollWindowContent, 'ckLabel' + str(i)), self.tipsData['labelTips'][i])

        for i in range(0, self.CKBOXSHADER_NUM):
            TipManager.addTip(getattr(self.scrollWindowContent, 'ckShader' + str(i)), self.tipsData['shaderTips'][i])

        for i in range(0, len(self.SENIOR_ARRAY)):
            TipManager.addTip(getattr(self.scrollWindowContent, self.SENIOR_ARRAY[i]), self.tipsData['seniorTips'][i])

    def updateMode(self):
        if self.widget:
            self.scrollWindowContent.getChildByName('ckShader' + str(appSetting.getShaderIndex())).selected = True

    def unRegisterPanel(self):
        self.widget = None
        self.mainMc = None
        self.scrollWindowContent = None
        self.videoConfigData = []
        self.tipsData = {}
        self.windowData = {}
        self.resolutionArray = []

    def createResolutionArray(self):
        resolutionList = C_ui.getVideoModes()
        resolutionSet = set()
        for item in resolutionList:
            resolutionSet.add((item[0], item[1]))

        resolutionList = list(resolutionSet)
        resolutionList.sort(self._sortRule)
        if len(resolutionList) > 0:
            self.maxResolution = resolutionList[-1]
        currentResolution = BigWorld.getScreenState()
        if (currentResolution[0], currentResolution[1]) not in resolutionSet:
            resolutionList.insert(0, (currentResolution[0], currentResolution[1]))
        resolutionArray = []
        for i in xrange(len(resolutionList)):
            width = resolutionList[i][0]
            height = resolutionList[i][1]
            showLabel = str(width) + ' x ' + str(height)
            if int(height) / int(width) < 0.6625:
                showLabel += gameStrings.SURFACESETTING_TEXT1
            resolutionArray.append({'label': showLabel,
             'data': [width, height],
             'index': i})

        return resolutionArray

    def createWindowArray(self):
        if hasattr(BigWorld, 'getCompileTimeString'):
            date = BigWorld.getCompileTimeString()
            date = date.split('@')[0]
        else:
            date = ''
        array = [gameStrings.WINDOW_CONFIG_3, gameStrings.WINDOW_CONFIG_4]
        if date >= '20171110':
            array.insert(0, gameStrings.WINDOW_CONFIG_1)
        else:
            array.insert(0, gameStrings.WINDOW_CONFIG_2)
        windowArray = []
        for i in xrange(len(array)):
            windowArray.append({'label': array[i]})

        return windowArray

    def showWarningMessage(self, w, h, isWindow):
        if not isWindow and appSetting._resolutionChanged(w, h, isWindow):
            oldW, oldH, oldwindowed, _ = BigWorld.getScreenState()
            func = Functor(appSetting.setScreenSize, oldW, oldH, oldwindowed, True)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg=gameStrings.SURFACESETTING_MSG, noCallback=func, noBtnText=gameStrings.SURFACESETTING_TEXT2, title=gameStrings.SURFACESETTING_TITLE, repeat=10, countDownFunctor=func)

    def _sortRule(self, x, y):
        xw, xh = x
        yw, yh = y
        if xw > yw:
            return 1
        if xw == yw:
            if xh > yh:
                return 1
            else:
                return -1
        else:
            return -1
