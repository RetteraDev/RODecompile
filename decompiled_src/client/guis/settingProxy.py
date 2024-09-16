#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/settingProxy.o
from gamestrings import gameStrings
import BigWorld
import C_ui
import Sound
from Scaleform import GfxValue
import uiConst
import uiUtils
import appSetting
import gameglobal
import gamelog
from uiProxy import UIProxy
from ui import gbk2unicode
from appSetting import Obj as AppSettings

class SettingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SettingProxy, self).__init__(uiAdapter)
        self.nowtick = 0
        self.lefttick = 0
        self.Mode = uiConst.MODE_Inactive
        self.modelMap = {'enableSound': self.onEnableSound,
         'setSoundVal': self.onSetSoundVal,
         'getSoundConfig': self.onGetSoundConfig,
         'commonSetting': self.commonSetting,
         'defaultSetting': self.defaultSetting,
         'onConfirm': self.onConfirm,
         'onCancel': self.onCancel,
         'onApply': self.onApply,
         'getVideoConfig': self.onGetVideoConfig,
         'getGameConfig': self.onGetGameConfig,
         'getDebugConfig': self.onGetDebugConfig,
         'getDebugContent': self.onGetDebugContent,
         'debugClick': self.onDebugClick,
         'getResolution': self.getResolution,
         'setVideoQuality': self.onSetVideoQuality,
         'registerVideo': self.onRegisterVideo}
        self.soundConfig = []
        self.debugFuncList = [[gameStrings.TEXT_DEBUGSETTINGPROXY_25, None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_25_1, None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_25_2, None],
         [gameStrings.TEXT_SETTINGPROXY_43, None],
         [gameStrings.TEXT_SETTINGPROXY_43_1, None],
         ['Sea', None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_26, None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_27, None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_27_1, None],
         [gameStrings.TEXT_DEBUGSETTINGPROXY_27_2, None]]
        self.isShow = False
        self.mapFunc = {'sound': (self.soundConfirm, self.soundCancel),
         'debug': (self.debugConfirm, self.debugCancel),
         'video': (self.videoConrirm, self.videoCancel, self.videoApply),
         'game': (self.gameConfirm, self.gameCancel)}
        uiAdapter.registerEscFunc(uiConst.WIDGET_SYS_SETTING, self.close)
        uiAdapter.registerEscFunc(uiConst.WIDGET_SOUND_SETTING, self.closeSoundProxy)
        uiAdapter.registerEscFunc(uiConst.WIDGET_DEBUG_SETTING, 'unLoadWidget')
        uiAdapter.registerEscFunc(uiConst.WIDGET_VIDEO_SETTING, 'unLoadWidget')
        uiAdapter.registerEscFunc(uiConst.WIDGET_GAME_SETTING, 'unLoadWidget')
        self.videoMc = None

    def onEnableSound(self, *arg):
        gamelog.debug('syssetting', arg[3][0].GetString(), arg[3][1].GetBool())
        option = arg[3][0].GetString()
        val = arg[3][1].GetBool()
        if option == 'ambientCheck':
            Sound.enableAmbient(val)
        elif option == 'fxCheck':
            Sound.enableFx(val)
        elif option == 'musicCheck':
            Sound.enableMusic(val)
        elif option == 'uiCheck':
            Sound.enableUi(val)

    def onSetSoundVal(self, *arg):
        gamelog.debug('syssetting', arg[3][0].GetString(), arg[3][1].GetNumber())
        option = arg[3][0].GetString()
        val = arg[3][1].GetNumber()
        if option == 'masterSlider':
            Sound.setSoundVolume(val)
        elif option == 'ambientSlider':
            Sound.setAmbientVolume(val)
        elif option == 'fxSlider':
            Sound.setFxVolume(val)
        elif option == 'musicSlider':
            Sound.setMusicVolume(val)
        elif option == 'uiSlider' and appSetting.SoundSettingObj.isUiEnable():
            Sound.setUiVolume(val)

    def onGetSoundConfig(self, *arg):
        gamelog.debug('onGetSoundConfig', appSetting.SoundSettingObj._value)
        ar = self.movie.CreateArray()
        i = 0
        for item in appSetting.SoundSettingObj._value:
            gamelog.debug('onGetSoundConfig', item)
            ar.SetElement(i, GfxValue(item))
            i = i + 1

        return ar

    def onGetVideoConfig(self, *arg):
        ar = self.movie.CreateArray()
        w, h, windowed, _ = BigWorld.getScreenState()
        ar.SetElement(0, GfxValue(w))
        ar.SetElement(1, GfxValue(h))
        ar.SetElement(2, GfxValue(windowed))
        i = 3
        for item in appSetting.VideoQualitySettingObj._value:
            ar.SetElement(i, GfxValue(item))
            i = i + 1

        return ar

    def onGetGameConfig(self, *arg):
        ar = self.movie.CreateArray()
        for index, value in enumerate(appSetting.GameSettingObj.getValue()):
            ar.SetElement(index, GfxValue(value))

        return ar

    def commonSetting(self, *arg):
        btnName = arg[3][0].GetString()
        gamelog.debug('bgf:commonSetting', btnName)
        if btnName == 'continueGame':
            self.close()
        elif btnName == 'quitGame':
            uiUtils.onQuit()
        elif btnName == 'gotoLogin':
            gameglobal.rds.ui.returnLoginView()
        elif btnName == 'videoBtn':
            self.uiAdapter.loadWidget(uiConst.WIDGET_VIDEO_SETTING)
        elif btnName == 'soundBtn':
            self.uiAdapter.loadWidget(uiConst.WIDGET_SOUND_SETTING)
        elif btnName == 'gameBtn':
            self.uiAdapter.loadWidget(uiConst.WIDGET_GAME_SETTING)
        elif btnName == 'controlBtn':
            self.uiAdapter.hotkey.show()
        elif btnName == 'debugBtn' and not BigWorld.isPublishedVersion():
            self.uiAdapter.loadWidget(uiConst.WIDGET_DEBUG_SETTING)
        elif btnName == 'quitBtn':
            self.close()
        gameglobal.rds.sound.playSound(gameglobal.SD_6)

    def _getAllData(self, *arg):
        tag = arg[3][0].GetString()
        array = arg[3][1].GetString().split(',')
        array = [ int(x) for x in array ]
        if tag == 'video':
            if array[2] == 0:
                array[0], array[1] = BigWorld.getScreenSize()
        return (tag, array)

    def onConfirm(self, *arg):
        tag, data = self._getAllData(*arg)
        gamelog.debug('bgf:onConfirm', tag, data)
        self.mapFunc[tag][0](data)
        AppSettings.save()
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def onApply(self, *arg):
        tag, data = self._getAllData(*arg)
        self.mapFunc[tag][2](data)
        AppSettings.save()
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def onCancel(self, *arg):
        tag, data = self._getAllData(*arg)
        gamelog.debug('bgf:onCancel', tag, data)
        self.mapFunc[tag][1](data)
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def onGetDebugConfig(self, *arg):
        arr = self.movie.CreateArray()
        i = 0
        for item in appSetting.DebugSettingObj._value:
            arr.SetElement(i, GfxValue(item))
            i += 1

        return arr

    def onDebugClick(self, *arg):
        index = int(arg[3][0].GetString())
        selected = arg[3][1].GetBool()
        gamelog.debug('debug wy:', index, selected)

    def onGetDebugContent(self, *arg):
        gamelog.debug('onGetDebugContent')
        arr = self.movie.CreateArray()
        if self.debugFuncList == None:
            return arr
        else:
            i = 0
            for item in self.debugFuncList:
                arr.SetElement(i, GfxValue(gbk2unicode(item[0])))
                i += 1

            return arr

    def show(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_SYS_SETTING)
        self.isShow = True

    def close(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SYS_SETTING)
        self.isShow = False

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

    def getResolution(self, *arg):
        resolutionList = C_ui.getVideoModes()
        currentResolution = BigWorld.getScreenState()
        resolutionSet = set()
        for item in resolutionList:
            resolutionSet.add((item[0], item[1]))

        resolutionList = list(resolutionSet)
        resolutionList.sort(self._sortRule)
        arr = self.movie.CreateArray()
        i = 0
        if (currentResolution[0], currentResolution[1]) not in resolutionSet:
            arr.SetElement(2 * i, GfxValue(currentResolution[0]))
            arr.SetElement(2 * i + 1, GfxValue(currentResolution[1]))
            i += 1
        for item in resolutionList:
            arr.SetElement(2 * i, GfxValue(item[0]))
            arr.SetElement(2 * i + 1, GfxValue(item[1]))
            i += 1

        return arr

    def soundConfirm(self, data):
        appSetting.SoundSettingObj._value = data
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_SOUND_SETTING)))

    def soundCancel(self, data):
        appSetting.SoundSettingObj.applyOrigin(data)
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_SOUND_SETTING)))

    def debugConfirm(self, data):
        appSetting.DebugSettingObj.apply(data)
        appSetting.DebugSettingObj._value = data
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_DEBUG_SETTING)))

    def debugCancel(self, data):
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_DEBUG_SETTING)))

    def videoConrirm(self, data):
        appSetting.setScreenSize(data[0], data[1], data[2])
        appSetting.VideoQualitySettingObj.apply(data[3:])
        appSetting.VideoQualitySettingObj._value = data[3:]
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_VIDEO_SETTING)))

    def videoCancel(self, data):
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_VIDEO_SETTING)))

    def videoApply(self, data):
        appSetting.setScreenSize(data[0], data[1], data[2])
        appSetting.VideoQualitySettingObj.apply(data[3:])
        appSetting.VideoQualitySettingObj._value = data[3:]

    def videoDefault(self):
        appSetting.setScreenSize(gameglobal.DEFAULT_SCREEN_WIDTH, gameglobal.DEFAULT_SCREEN_HEIGHT, 1)
        videoArray = appSetting.VideoQualitySettingObj.getDefault()
        appSetting.VideoQualitySettingObj.apply(videoArray)

    def gameConfirm(self, data):
        gamelog.debug('hjx debug gameSet gameConfirm:', data)
        appSetting.GameSettingObj.apply(data)
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_GAME_SETTING)))

    def gameCancel(self, data):
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_GAME_SETTING)))

    def defaultSetting(self, *arg):
        tag = arg[3][0].GetString()
        self.mapFunc[tag][2]()
        AppSettings.default()

    def closeSoundProxy(self):
        appSetting.SoundSettingObj.apply()
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_SOUND_SETTING)))

    def onSetVideoQuality(self, *arg):
        quality = int(arg[3][0].GetString())
        retArray = appSetting.VideoQualitySettingObj.getVideoQuality(quality)
        obj = self.movie.CreateArray()
        for i, item in enumerate(retArray[2:]):
            obj.SetElement(i, GfxValue(item))

        if self.videoMc:
            self.videoMc.Invoke('setSliderValue', obj)

    def onRegisterVideo(self, *arg):
        self.videoMc = arg[3][0]

    def reset(self):
        self.isShow = False
