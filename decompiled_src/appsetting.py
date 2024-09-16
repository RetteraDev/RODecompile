#Embedded file name: /WORKSPACE/data/entities/client/appsetting.o
import os
import ResMgr
import BigWorld
import C_ui
import Sound
import Pixie
import const
import gameglobal
import gametypes
import keys
import gamelog
import clientcom
import formula
from guis import hotkeyProxy
from guis import ime
from helpers import navigator
from helpers import loadingProgress
from helpers import ufo
from helpers import ccManager
from sfx import screenEffect
from sfx import sfx
from data import map_config_data as MCD
from cdata import game_msg_def_data as GMDD
vsdDataOld = {'minimalist': {'HQS': 0,
                'DL': 0,
                'SHADOW': 0,
                'SSAO': 0,
                'FXAA': 0,
                'DOF': 0,
                'REF': 0,
                'VSYNC': 0,
                'HQLS': 0,
                'SUNSHAFT': 0,
                'HEAT': 0,
                'SHARP': 1,
                'PLAYEREFF': 0,
                'AVATAREFF': -1,
                'ENEMYAVATAREFF': -1,
                'MONSTEREFF': -1,
                'NPCEFF': -1,
                'ENVIRONMENTEFF': -1,
                'motionBlur': 0,
                'screenEffect': 0,
                'animateCamera': 1,
                'cameraShake': 0,
                'disableSkillHover': 1,
                'hitFreeze': 0,
                'showBloodLabel': 1,
                'modelShake': 0,
                'bloom': 1,
                'setViewFactor': 0,
                'forceSkipMipMap': 0,
                'setTerrainRenderLevel': 0,
                'modelLODScale': 0,
                'wsEffect': 0,
                'textureLODSizeLimit': 0,
                'darkAngle': 0,
                'ModelShowNum': 0,
                'effShowNum': 0,
                'foregroundFPS': 60,
                'backgroundFPSSlider': 10,
                'enableMinimalist': 1,
                'enablePhysics': 0,
                'enableMemorySetting': 0,
                'skinLight': 50},
 'lowest': {'HQS': 0,
            'DL': 0,
            'SHADOW': 0,
            'SSAO': 0,
            'FXAA': 0,
            'DOF': 0,
            'REF': 0,
            'VSYNC': 0,
            'HQLS': 0,
            'SUNSHAFT': 0,
            'HEAT': 0,
            'SHARP': 1,
            'PLAYEREFF': 0,
            'AVATAREFF': -1,
            'ENEMYAVATAREFF': -1,
            'MONSTEREFF': -1,
            'NPCEFF': -1,
            'ENVIRONMENTEFF': -1,
            'motionBlur': 0,
            'screenEffect': 0,
            'animateCamera': 1,
            'cameraShake': 0,
            'disableSkillHover': 1,
            'hitFreeze': 0,
            'showBloodLabel': 1,
            'modelShake': 0,
            'bloom': 0,
            'setViewFactor': 0,
            'forceSkipMipMap': 1,
            'setTerrainRenderLevel': 0,
            'modelLODScale': 0,
            'wsEffect': 0,
            'textureLODSizeLimit': 0,
            'darkAngle': 0,
            'ModelShowNum': 0,
            'effShowNum': 0,
            'foregroundFPS': 60,
            'backgroundFPSSlider': 10,
            'enableMinimalist': 0,
            'enablePhysics': 0,
            'enableMemorySetting': 0,
            'skinLight': 50},
 'low': {'HQS': 1,
         'DL': 0,
         'SHADOW': 1,
         'SSAO': 0,
         'FXAA': 2,
         'DOF': 0,
         'REF': 1,
         'VSYNC': 0,
         'HQLS': 1,
         'SUNSHAFT': 1,
         'HEAT': 0,
         'SHARP': 1,
         'PLAYEREFF': 1,
         'AVATAREFF': -1,
         'ENEMYAVATAREFF': 0,
         'MONSTEREFF': 0,
         'NPCEFF': -1,
         'ENVIRONMENTEFF': -1,
         'motionBlur': 1,
         'screenEffect': 1,
         'animateCamera': 1,
         'cameraShake': 1,
         'disableSkillHover': 1,
         'hitFreeze': 0,
         'showBloodLabel': 1,
         'modelShake': 1,
         'bloom': 0,
         'setViewFactor': 1,
         'forceSkipMipMap': 1,
         'setTerrainRenderLevel': 1,
         'modelLODScale': 1,
         'wsEffect': 1,
         'textureLODSizeLimit': 1,
         'darkAngle': 0,
         'ModelShowNum': 0,
         'effShowNum': 0,
         'foregroundFPS': 60,
         'backgroundFPSSlider': 10,
         'enableMinimalist': 0,
         'enablePhysics': 0,
         'enableMemorySetting': 1,
         'skinLight': 50},
 'high': {'HQS': 1,
          'DL': 1,
          'SHADOW': 3,
          'SSAO': 0,
          'FXAA': 3,
          'DOF': 1,
          'REF': 3,
          'VSYNC': 0,
          'HQLS': 3,
          'SUNSHAFT': 2,
          'HEAT': 1,
          'SHARP': 1,
          'PLAYEREFF': 2,
          'AVATAREFF': 1,
          'ENEMYAVATAREFF': 1,
          'MONSTEREFF': 1,
          'NPCEFF': 1,
          'ENVIRONMENTEFF': 1,
          'motionBlur': 1,
          'screenEffect': 1,
          'animateCamera': 1,
          'cameraShake': 1,
          'disableSkillHover': 1,
          'hitFreeze': 1,
          'showBloodLabel': 1,
          'modelShake': 1,
          'bloom': 1,
          'setViewFactor': 3,
          'forceSkipMipMap': 3,
          'setTerrainRenderLevel': 3,
          'modelLODScale': 2,
          'wsEffect': 1,
          'textureLODSizeLimit': 2,
          'darkAngle': 1,
          'ModelShowNum': 1,
          'effShowNum': 1,
          'foregroundFPS': 60,
          'backgroundFPSSlider': 10,
          'enableMinimalist': 0,
          'enablePhysics': 1,
          'enableMemorySetting': 1,
          'skinLight': 50},
 'mid': {'HQS': 1,
         'DL': 0,
         'SHADOW': 2,
         'SSAO': 0,
         'FXAA': 3,
         'DOF': 0,
         'REF': 2,
         'VSYNC': 0,
         'HQLS': 2,
         'SUNSHAFT': 1,
         'HEAT': 1,
         'SHARP': 1,
         'PLAYEREFF': 2,
         'AVATAREFF': 0,
         'ENEMYAVATAREFF': 0,
         'MONSTEREFF': 0,
         'NPCEFF': 0,
         'ENVIRONMENTEFF': 0,
         'motionBlur': 1,
         'screenEffect': 1,
         'animateCamera': 1,
         'cameraShake': 1,
         'disableSkillHover': 1,
         'hitFreeze': 1,
         'showBloodLabel': 1,
         'modelShake': 1,
         'bloom': 1,
         'setViewFactor': 3,
         'forceSkipMipMap': 3,
         'setTerrainRenderLevel': 3,
         'modelLODScale': 2,
         'wsEffect': 1,
         'textureLODSizeLimit': 1,
         'darkAngle': 0,
         'ModelShowNum': 1,
         'effShowNum': 1,
         'foregroundFPS': 60,
         'backgroundFPSSlider': 10,
         'enableMinimalist': 0,
         'enablePhysics': 1,
         'enableMemorySetting': 1,
         'skinLight': 50},
 'ultra': {'HQS': 1,
           'DL': 1,
           'SHADOW': 4,
           'SSAO': 0,
           'FXAA': 4,
           'DOF': 1,
           'REF': 4,
           'VSYNC': 0,
           'HQLS': 4,
           'SUNSHAFT': 4,
           'HEAT': 1,
           'SHARP': 1,
           'PLAYEREFF': 2,
           'AVATAREFF': 1,
           'ENEMYAVATAREFF': 1,
           'MONSTEREFF': 1,
           'NPCEFF': 1,
           'ENVIRONMENTEFF': 1,
           'motionBlur': 1,
           'screenEffect': 1,
           'animateCamera': 1,
           'cameraShake': 1,
           'disableSkillHover': 1,
           'hitFreeze': 1,
           'showBloodLabel': 1,
           'modelShake': 1,
           'bloom': 1,
           'setViewFactor': 4,
           'forceSkipMipMap': 4,
           'setTerrainRenderLevel': 4,
           'modelLODScale': 4,
           'wsEffect': 1,
           'textureLODSizeLimit': 4,
           'darkAngle': 1,
           'ModelShowNum': 2,
           'effShowNum': 2,
           'foregroundFPS': 60,
           'backgroundFPSSlider': 10,
           'enableMinimalist': 0,
           'enablePhysics': 1,
           'enableMemorySetting': 1,
           'skinLight': 50}}
vsdDataNew = {'minimalist': {'HQS': 0,
                'DL': 0,
                'SHADOW': 0,
                'SSAO': 0,
                'FXAA': 0,
                'DOF': 0,
                'REF': 0,
                'VSYNC': 0,
                'HQLS': 0,
                'SUNSHAFT': 0,
                'HEAT': 0,
                'SHARP': 1,
                'PLAYEREFF': 0,
                'AVATAREFF': -1,
                'ENEMYAVATAREFF': -1,
                'MONSTEREFF': -1,
                'NPCEFF': -1,
                'ENVIRONMENTEFF': -1,
                'motionBlur': 0,
                'screenEffect': 0,
                'animateCamera': 1,
                'cameraShake': 0,
                'disableSkillHover': 1,
                'hitFreeze': 0,
                'showBloodLabel': 1,
                'modelShake': 0,
                'bloom': 1,
                'setViewFactor': 0,
                'forceSkipMipMap': 0,
                'setTerrainRenderLevel': 0,
                'modelLODScale': 0,
                'wsEffect': 0,
                'textureLODSizeLimit': 0,
                'darkAngle': 0,
                'ModelShowNum': 0,
                'effShowNum': 0,
                'foregroundFPS': 60,
                'backgroundFPSSlider': 10,
                'enableMinimalist': 1,
                'enablePhysics': 0,
                'enableMemorySetting': 0,
                'skinLight': 50},
 'lowest': {'HQS': 0,
            'DL': 0,
            'SHADOW': 0,
            'SSAO': 0,
            'FXAA': 0,
            'DOF': 0,
            'REF': 0,
            'VSYNC': 0,
            'HQLS': 0,
            'SUNSHAFT': 0,
            'HEAT': 0,
            'SHARP': 1,
            'PLAYEREFF': 0,
            'AVATAREFF': -1,
            'ENEMYAVATAREFF': -1,
            'MONSTEREFF': -1,
            'NPCEFF': -1,
            'ENVIRONMENTEFF': -1,
            'motionBlur': 0,
            'screenEffect': 0,
            'animateCamera': 1,
            'cameraShake': 0,
            'disableSkillHover': 1,
            'hitFreeze': 0,
            'showBloodLabel': 1,
            'modelShake': 0,
            'bloom': 0,
            'setViewFactor': 0,
            'forceSkipMipMap': 1,
            'setTerrainRenderLevel': 0,
            'modelLODScale': 0,
            'wsEffect': 0,
            'textureLODSizeLimit': 0,
            'darkAngle': 0,
            'ModelShowNum': 0,
            'effShowNum': 0,
            'foregroundFPS': 60,
            'backgroundFPSSlider': 10,
            'enableMinimalist': 0,
            'enablePhysics': 0,
            'enableMemorySetting': 0,
            'skinLight': 50},
 'low': {'HQS': 1,
         'DL': 0,
         'SHADOW': 1,
         'SSAO': 0,
         'FXAA': 2,
         'DOF': 0,
         'REF': 1,
         'VSYNC': 0,
         'HQLS': 1,
         'SUNSHAFT': 1,
         'HEAT': 0,
         'SHARP': 1,
         'PLAYEREFF': 1,
         'AVATAREFF': -1,
         'ENEMYAVATAREFF': 0,
         'MONSTEREFF': 0,
         'NPCEFF': -1,
         'ENVIRONMENTEFF': -1,
         'motionBlur': 1,
         'screenEffect': 1,
         'animateCamera': 1,
         'cameraShake': 1,
         'disableSkillHover': 1,
         'hitFreeze': 0,
         'showBloodLabel': 1,
         'modelShake': 1,
         'bloom': 0,
         'setViewFactor': 1,
         'forceSkipMipMap': 1,
         'setTerrainRenderLevel': 1,
         'modelLODScale': 1,
         'wsEffect': 1,
         'textureLODSizeLimit': 1,
         'darkAngle': 0,
         'ModelShowNum': 0,
         'effShowNum': 0,
         'foregroundFPS': 60,
         'backgroundFPSSlider': 10,
         'enableMinimalist': 0,
         'enablePhysics': 0,
         'enableMemorySetting': 1,
         'skinLight': 50},
 'high': {'HQS': 1,
          'DL': 1,
          'SHADOW': 3,
          'SSAO': 0,
          'FXAA': 3,
          'DOF': 1,
          'REF': 3,
          'VSYNC': 0,
          'HQLS': 3,
          'SUNSHAFT': 2,
          'HEAT': 1,
          'SHARP': 1,
          'PLAYEREFF': 2,
          'AVATAREFF': 1,
          'ENEMYAVATAREFF': 1,
          'MONSTEREFF': 1,
          'NPCEFF': 1,
          'ENVIRONMENTEFF': 1,
          'motionBlur': 1,
          'screenEffect': 1,
          'animateCamera': 1,
          'cameraShake': 1,
          'disableSkillHover': 1,
          'hitFreeze': 1,
          'showBloodLabel': 1,
          'modelShake': 1,
          'bloom': 1,
          'setViewFactor': 3,
          'forceSkipMipMap': 3,
          'setTerrainRenderLevel': 3,
          'modelLODScale': 2,
          'wsEffect': 1,
          'textureLODSizeLimit': 2,
          'darkAngle': 1,
          'ModelShowNum': 1,
          'effShowNum': 1,
          'foregroundFPS': 60,
          'backgroundFPSSlider': 10,
          'enableMinimalist': 0,
          'enablePhysics': 1,
          'enableMemorySetting': 1,
          'skinLight': 50},
 'mid': {'HQS': 1,
         'DL': 1,
         'SHADOW': 2,
         'SSAO': 0,
         'FXAA': 3,
         'DOF': 0,
         'REF': 2,
         'VSYNC': 0,
         'HQLS': 2,
         'SUNSHAFT': 1,
         'HEAT': 1,
         'SHARP': 1,
         'PLAYEREFF': 2,
         'AVATAREFF': 0,
         'ENEMYAVATAREFF': 0,
         'MONSTEREFF': 0,
         'NPCEFF': 0,
         'ENVIRONMENTEFF': 0,
         'motionBlur': 1,
         'screenEffect': 1,
         'animateCamera': 1,
         'cameraShake': 1,
         'disableSkillHover': 1,
         'hitFreeze': 1,
         'showBloodLabel': 1,
         'modelShake': 1,
         'bloom': 1,
         'setViewFactor': 2,
         'forceSkipMipMap': 2,
         'setTerrainRenderLevel': 2,
         'modelLODScale': 2,
         'wsEffect': 1,
         'textureLODSizeLimit': 1,
         'darkAngle': 0,
         'ModelShowNum': 1,
         'effShowNum': 1,
         'foregroundFPS': 60,
         'backgroundFPSSlider': 10,
         'enableMinimalist': 0,
         'enablePhysics': 1,
         'enableMemorySetting': 1,
         'skinLight': 50},
 'ultra': {'HQS': 1,
           'DL': 1,
           'SHADOW': 4,
           'SSAO': 0,
           'FXAA': 4,
           'DOF': 1,
           'REF': 4,
           'VSYNC': 0,
           'HQLS': 4,
           'SUNSHAFT': 4,
           'HEAT': 1,
           'SHARP': 1,
           'PLAYEREFF': 2,
           'AVATAREFF': 1,
           'ENEMYAVATAREFF': 1,
           'MONSTEREFF': 1,
           'NPCEFF': 1,
           'ENVIRONMENTEFF': 1,
           'motionBlur': 1,
           'screenEffect': 1,
           'animateCamera': 1,
           'cameraShake': 1,
           'disableSkillHover': 1,
           'hitFreeze': 1,
           'showBloodLabel': 1,
           'modelShake': 1,
           'bloom': 1,
           'setViewFactor': 4,
           'forceSkipMipMap': 4,
           'setTerrainRenderLevel': 4,
           'modelLODScale': 4,
           'wsEffect': 1,
           'textureLODSizeLimit': 4,
           'darkAngle': 1,
           'ModelShowNum': 2,
           'effShowNum': 2,
           'foregroundFPS': 60,
           'backgroundFPSSlider': 10,
           'enableMinimalist': 0,
           'enablePhysics': 1,
           'enableMemorySetting': 1,
           'skinLight': 50}}
BASEX = 0
BASEY = 0
OFFSETX = 23
OFFSETY = 19
INTERVALX = 185
INTERVALY = 27
Obj = None
ENABLE_WAIFU_SETTING = True

def repairSection(filename):
    ResMgr.purge(filename, True)
    os.remove(filename)
    return ResMgr.openSection(filename, True)


class AppSetting(object):

    def __init__(self):
        super(AppSetting, self).__init__()
        self.__sect = ResMgr.openSection('../game/tianyu.xml')
        self.__confSect = ResMgr.openSection('../game/conf.xml', True)
        try:
            self.__confSect.writeString('TestIfMeABinSection', 'hello')
            self.__confSect.deleteSection('TestIfMeABinSection')
        except TypeError:
            self.__confSect = repairSection('../game/conf.xml')

        self.__settingItem = {}
        self.exportDict = {}

    def applySetting(self):
        pass

    def __getitem__(self, key):
        keyEle = key.split('/')
        which = keyEle.pop(0)
        path = '/'
        path = path.join(keyEle)
        if which == 'tw2':
            return self.__sect.readString(path)
        if which == 'conf':
            return self.__confSect.readString(path)
        raise ValueError, 'has no specail config file!'

    def __setitem__(self, key, value):
        keyEle = key.split('/')
        which = keyEle.pop(0)
        path = '/'
        path = path.join(keyEle)
        if self.get(key, 0) != value:
            self.exportDict[keyEle[-1]] = value
        if which == 'tw2':
            gamelog.error("Error:tw2.xml is readonly, can\'t write")
            raise ValueError, "tw2.xml can\'t write"
        elif which == 'conf':
            self.__confSect.writeString(path, str(value))
        else:
            gamelog.error('has no specail config file!')

    def get(self, key, default):
        __type = type(default)
        ret = Obj[key]
        if ret == '':
            ret = default
        try:
            return __type(ret)
        except:
            return default

    def appendSetting(self, setting):
        ret = self.__settingItem.get(setting.getKey(), None)
        if ret == None:
            self.__settingItem[setting.getKey()] = setting
        else:
            raise KeyError, 'setting is exists'

    def present(self, uiParent):
        for setting in self.__settingItem.itervalues():
            if setting._uiParent == uiParent:
                setting.present(uiParent)

    def load(self):
        for setting in self.__settingItem.itervalues():
            setting.load()

    def save(self):
        try:
            for setting in self.__settingItem.itervalues():
                setting.save()

            if self.__confSect:
                self.__confSect.save()
        except IOError:
            pass

    def update(self):
        for setting in self.__settingItem.itervalues():
            setting.update()

    def apply(self):
        for setting in self.__settingItem.itervalues():
            setting.apply()

    def default(self):
        for setting in self.__settingItem.itervalues():
            setting.default()

    def changeMode(self):
        for setting in self.__settingItem.itervalues():
            if setting.changeMode():
                return True

        return False


class SysSetting(AppSetting):

    def __init__(self):
        super(SysSetting, self).__init__()
        self.__first = True

    def applySetting(self):
        try:
            factor = self.get(keys.SET_VIEWFACTOR, 1.0)
            if factor < 0.5:
                factor = 0.5
            elif factor > 1.5:
                factor = 1.5
        except ValueError:
            factor = 1.0

        if BigWorld.player() != None:
            gamelog.debug('set view factor', factor)
            self.apply()

    def apply(self):
        super(SysSetting, self).apply()
        if self.changeMode() or self.__first:
            gamelog.debug('Script call $B.forceChangeMode................')
            BigWorld.forceChangeMode()
            self.__first = False


Obj = SysSetting()

class SettingBase(object):

    def __init__(self, key):
        super(SettingBase, self).__init__()
        self._key = key
        self._value = None
        self._uiParent = None
        self._needPresent = True
        Obj.appendSetting(self)

    def getValue(self):
        return self._value

    def save(self):
        if self._value != None:
            gamelog.debug('%s setting save' % self._key)
            Obj[self._key] = int(self._value)

    def load(self):
        self._value = Obj.get(self._key, -1)
        if self._value == -1:
            self.default()
        self._value = self.validate(self._value)

    def apply(self):
        pass

    def present(self, uiParent):
        pass

    def default(self):
        pass

    def notice(self, msg, sender):
        pass

    def update(self):
        pass

    def getKey(self):
        return self._key

    def presented(self, uiParent):
        self._uiParent = uiParent
        self._needPresent = False

    def needPresent(self):
        return self._needPresent

    def validate(self, value):
        return value

    def changeMode(self):
        return False


class SoundSetting(SettingBase):

    def __init__(self):
        super(SoundSetting, self).__init__('conf/Audio/sound')
        self.defaultValue = [100,
         70,
         1,
         70,
         1,
         80,
         1,
         70,
         1,
         80,
         1,
         70,
         1,
         1,
         0,
         70,
         1,
         70,
         1,
         256,
         0,
         0,
         1,
         70,
         70]
        self._value = self.defaultValue[:]
        self.func = [self.setSoundVolume,
         Sound.setAmbientVolume,
         Sound.enableAmbient,
         Sound.setStaticVolume,
         Sound.enableStatic,
         self.setFxVolume,
         self.enableFx,
         self.setNpcVolume,
         self.enableNpc,
         Sound.setUiVolume,
         Sound.enableUi,
         Sound.setMusicVolume,
         Sound.enableMusic,
         Sound.enableReverb,
         self.enableBgSound,
         self.setCreatureVolume,
         self.enableCreature,
         self.setSystemVolume,
         self.enableSystem,
         self.setQuality,
         self.setPrefer,
         self.setPlayOtherSpriteSound,
         self.setVoiceMode,
         self.setVoiceInVolume,
         self.setVoiceOutVolume]
        self.categoryVolumeKeys = {gametypes.CATEGORY_MASTER: 'conf/Audio/SoundVolume',
         gametypes.CATEGORY_AMBIENT: 'conf/Audio/AmbientVolume',
         gametypes.CATEGORY_STATIC: 'conf/Audio/StaticVolume',
         gametypes.CATEGORY_CHAR: 'conf/Audio/FxVolume',
         gametypes.CATEGORY_CREATURE: 'conf/Audio/CreatureVolume',
         gametypes.CATEGORY_NPC: 'conf/Audio/VoiceVolume',
         gametypes.CATEGORY_UI: 'conf/Audio/UiVolume',
         gametypes.CATEGORY_MUSIC: 'conf/Audio/MusicVolume',
         gametypes.CATEGORY_SYSTEM: 'conf/Audio/SystemVolume'}
        self.categoryEnableKeys = {gametypes.CATEGORY_AMBIENT: 'conf/Audio/AmbientEnable',
         gametypes.CATEGORY_STATIC: 'conf/Audio/StaticEnable',
         gametypes.CATEGORY_CHAR: 'conf/Audio/FxEnable',
         gametypes.CATEGORY_CREATURE: 'conf/Audio/CreatureEnable',
         gametypes.CATEGORY_NPC: 'conf/Audio/VoiceEnable',
         gametypes.CATEGORY_UI: 'conf/Audio/UiEnable',
         gametypes.CATEGORY_MUSIC: 'conf/Audio/MusicEnable',
         gametypes.CATEGORY_SYSTEM: 'conf/Audio/SystemEnable'}

    def apply(self, data = None):
        gamelog.debug('apply music', self._value, data)
        if data:
            for i, item in enumerate(data):
                if item != self._value[i]:
                    self.func[i](item)

        else:
            for i, item in enumerate(self._value):
                self.func[i](item)

    def setVoiceMode(self, value):
        if value:
            ccManager.instance().stopCapture(const.CC_SESSION_TEAM)
        else:
            ccManager.instance().startCapture(const.CC_SESSION_TEAM)

    def setVoiceInVolume(self, value):
        ccManager.instance().setCaptureVolume(value)

    def setVoiceOutVolume(self, value):
        ccManager.instance().setPlaybackVolume(value)

    def setSoundVolume(self, value):
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            Sound.setSoundVolume(value)
            if hasattr(Sound, 'setRawfileVolume'):
                Sound.setRawfileVolume(value)

    def setFxVolume(self, value):
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            Sound.setCategoryVolume(gametypes.CATEGORY_CHAR, value)

    def enableFx(self, value):
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            Sound.enableCategory(gametypes.CATEGORY_CHAR, value)

    def setNpcVolume(self, value):
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            Sound.setCategoryVolume(gametypes.CATEGORY_NPC, value)
            if hasattr(Sound, 'setRawfileVolume'):
                Sound.setRawfileVolume(min(value, Sound.getSoundVolume()))

    def enableNpc(self, value):
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            Sound.enableCategory(gametypes.CATEGORY_NPC, value)
            if hasattr(Sound, 'setRawfileVolume'):
                if value:
                    Sound.setRawfileVolume(min(Sound.getCategoryVolume(gametypes.CATEGORY_NPC), Sound.getSoundVolume()))
                else:
                    Sound.setRawfileVolume(0)

    def setCreatureVolume(self, value):
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            Sound.setCategoryVolume(gametypes.CATEGORY_CREATURE, value)

    def enableCreature(self, value):
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            Sound.enableCategory(gametypes.CATEGORY_CREATURE, value)

    def setSystemVolume(self, value):
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            Sound.setCategoryVolume(gametypes.CATEGORY_SYSTEM, value)

    def enableSystem(self, value):
        if gameglobal.rds.GameState != gametypes.GS_LOADING:
            Sound.enableCategory(gametypes.CATEGORY_SYSTEM, value)

    def setQuality(self, value):
        Obj['conf/Audio/Quality'] = int(value)

    def setPrefer(self, value):
        Obj['conf/Audio/Prefer'] = int(value)

    def setPlayOtherSpriteSound(self, value):
        Obj['conf/Audio/PlayOtherSpriteSound'] = int(value)

    def enableBgSound(self, value):
        Sound.enableMute(not value)

    def default(self):
        self._value = self.defaultValue[:]

    def getDefault(self):
        return self.defaultValue[:]

    def save(self):
        Obj['conf/Audio/SoundVolume'] = int(self._value[0])
        Obj['conf/Audio/AmbientVolume'] = int(self._value[1])
        Obj['conf/Audio/AmbientEnable'] = int(self._value[2])
        Obj['conf/Audio/StaticVolume'] = int(self._value[3])
        Obj['conf/Audio/StaticEnable'] = int(self._value[4])
        Obj['conf/Audio/FxVolume'] = int(self._value[5])
        Obj['conf/Audio/FxEnable'] = int(self._value[6])
        Obj['conf/Audio/VoiceVolume'] = int(self._value[7])
        Obj['conf/Audio/VoiceEnable'] = int(self._value[8])
        Obj['conf/Audio/UiVolume'] = int(self._value[9])
        Obj['conf/Audio/UiEnable'] = int(self._value[10])
        Obj['conf/Audio/MusicVolume'] = int(self._value[11])
        Obj['conf/Audio/MusicEnable'] = int(self._value[12])
        Obj['conf/Audio/ReverbEnable'] = int(self._value[13])
        Obj['conf/Audio/MuteEnable'] = int(self._value[14])
        Obj['conf/Audio/CreatureVolume'] = int(self._value[15])
        Obj['conf/Audio/CreatureEnable'] = int(self._value[16])
        Obj['conf/Audio/SystemVolume'] = int(self._value[17])
        Obj['conf/Audio/SystemEnable'] = int(self._value[18])
        Obj['conf/Audio/softwareChannels'] = int(self._value[19])
        Obj['conf/Audio/Prefer'] = int(self._value[20])
        Obj['conf/Audio/PlayOtherSpriteSound'] = int(self._value[21])
        Obj['conf/Audio/VoiceMode'] = int(self._value[22])
        Obj['conf/Audio/VoiceInVolume'] = int(self._value[23])
        Obj['conf/Audio/VoiceOutVolume'] = int(self._value[24])

    def load(self):
        t = Obj.get('conf/Audio/SoundVolume', -1)
        self._value[0] = (t, 100)[t == -1]
        t = Obj.get('conf/Audio/AmbientVolume', -1)
        self._value[1] = (t, 70)[t == -1]
        t = Obj.get('conf/Audio/AmbientEnable', -1)
        self._value[2] = (t, 1)[t == -1]
        t = Obj.get('conf/Audio/StaticVolume', -1)
        self._value[3] = (t, 70)[t == -1]
        t = Obj.get('conf/Audio/StaticEnable', -1)
        self._value[4] = (t, 1)[t == -1]
        t = Obj.get('conf/Audio/FxVolume', -1)
        self._value[5] = (t, 80)[t == -1]
        t = Obj.get('conf/Audio/FxEnable', -1)
        self._value[6] = (t, 1)[t == -1]
        t = Obj.get('conf/Audio/VoiceVolume', -1)
        self._value[7] = (t, 80)[t == -1]
        t = Obj.get('conf/Audio/VoiceEnable', -1)
        self._value[8] = (t, 1)[t == -1]
        t = Obj.get('conf/Audio/UiVolume', -1)
        self._value[9] = (t, 80)[t == -1]
        t = Obj.get('conf/Audio/UiEnable', -1)
        self._value[10] = (t, 1)[t == -1]
        t = Obj.get('conf/Audio/MusicVolume', -1)
        self._value[11] = (t, 70)[t == -1]
        t = Obj.get('conf/Audio/MusicEnable', -1)
        self._value[12] = (t, 1)[t == -1]
        t = Obj.get('conf/Audio/ReverbEnable', -1)
        self._value[13] = (t, 0)[t == -1]
        t = Obj.get('conf/Audio/MuteEnable', -1)
        self._value[14] = (t, 0)[t == -1]
        t = Obj.get('conf/Audio/CreatureVolume', -1)
        self._value[15] = (t, 70)[t == -1]
        t = Obj.get('conf/Audio/CreatureEnable', -1)
        self._value[16] = (t, 1)[t == -1]
        t = Obj.get('conf/Audio/SystemVolume', -1)
        self._value[17] = (t, 70)[t == -1]
        t = Obj.get('conf/Audio/SystemEnable', -1)
        self._value[18] = (t, 1)[t == -1]
        t = Obj.get('conf/Audio/softwareChannels', -1)
        self._value[19] = (t, 256)[t == -1]
        t = Obj.get('conf/Audio/Prefer', -1)
        self._value[20] = (t, 0)[t == -1]
        t = Obj.get('conf/Audio/PlayOtherSpriteSound', -1)
        self._value[21] = (t, 0)[t == -1]
        t = Obj.get('conf/Audio/VoiceMode', -1)
        self._value[22] = (t, 1)[t == -1]
        t = Obj.get('conf/Audio/VoiceInVolume', -1)
        self._value[23] = (t, 70)[t == -1]
        t = Obj.get('conf/Audio/VoiceOutVolume', -1)
        self._value[24] = (t, 70)[t == -1]

    def isFxEnable(self):
        return self._value[6]

    def isMusicEnable(self):
        return self._value[12]

    def isAmbientEnable(self):
        return self._value[2]

    def isStaticEnable(self):
        return self._value[4]

    def getVolumeByCategory(self, category):
        if category and self.categoryVolumeKeys.has_key(category):
            return Obj.get(self.categoryVolumeKeys[category], 0)
        return 0

    def getEnableByCategory(self, category):
        if category and self.categoryEnableKeys.has_key(category):
            return Obj.get(self.categoryEnableKeys[category], 1)
        return 1

    def isUiEnable(self):
        return self._value[10]

    def isMuteOtherSprite(self):
        return not self._value[21]

    def applyOrigin(self, data):
        gamelog.debug('applyOrigin music', self._value, data)
        if data:
            for i, item in enumerate(data):
                if item != self._value[i]:
                    self.func[i](self._value[i])


class DebugSetting(SettingBase):

    def __init__(self):
        super(DebugSetting, self).__init__('debugSettting')
        self.default()

    def default(self):
        self._value = self.getDefault()

    def getDefault(self):
        return [1,
         1,
         0,
         0,
         0,
         1,
         0,
         0]

    def showMonsterTopLogo(self, show):
        gameglobal.gHideMonsterTopLogo = not show
        ent = BigWorld.entities.values()
        for e in ent:
            if e.IsMonster:
                e.topLogo.hideName(gameglobal.gHideMonsterTopLogo)

    def showEntityId(self, show):
        gameglobal.showEntityID = show
        p = BigWorld.player()
        if p:
            p.topLogo.showEntityId(show)

    def showAirWall(self, show):
        if not BigWorld.isPublishedVersion():
            BigWorld.setWatcher('Render/Show HideModels', show)

    def switchSea(self, param):
        pass

    def switchShortcutToPostion(self, isShortcutToPostion):
        if isShortcutToPostion:
            BigWorld.player().shortcutToPostion = True
        else:
            BigWorld.player().shortcutToPostion = False
        BigWorld.player().shortcutToPostionSkillId = 1

    def openPathTrace(self, isOpen, first = True):
        navigator.gShowTrace = isOpen
        if not isOpen:
            if first:
                navigator.getNav().initShowPoint()
            else:
                navigator.getNav().endShowPoint()

    def openUIPathTrace(self, isOpen, first = True):
        navigator.gShowUIPathTrace = isOpen
        if isOpen:
            if not first:
                navigator.getNav().doInitShowNavs()

    def turnOffSysLog(self, off):
        if not BigWorld.isPublishedVersion():
            offLv = 5 if off else 0
            BigWorld.setWatcher('debug/filterThreshold', offLv)

    def turnOffScriptLog(self, off):
        gamelog.LOG_LEVEL = gamelog.ERROR if off else gamelog.DEBUG

    def apply(self, data = None):
        gamelog.debug('songjiang apply deubg', self._value, data)
        if data:
            l = len(data)
            for i in xrange(l):
                if data[i] != self._value[i]:
                    if i == 0:
                        self.showMonsterTopLogo(data[i])
                    elif i == 1:
                        self.showEntityId(data[i])
                    elif i == 2:
                        self.showAirWall(data[i])
                    elif i == 3:
                        self.switchSea(data[i])
                    elif i == 4:
                        self.openPathTrace(data[i], False)
                    elif i == 5:
                        gameglobal.ENABLE_SHAKE_CAMERA = data[i]
                    elif i == 6:
                        self.turnOffSysLog(data[i])
                    elif i == 7:
                        self.turnOffScriptLog(data[i])

            return
        self.showMonsterTopLogo(self._value[0])
        self.showEntityId(self._value[1])
        self.showAirWall(self._value[2])
        self.switchSea(self._value[3])
        self.openPathTrace(self._value[4])
        self.turnOffSysLog(self._value[6])
        self.turnOffScriptLog(self._value[7])

    def load(self):
        self._value[0] = Obj.get('conf/Debug/showMonsterName', self._value[0])
        self._value[1] = Obj.get('conf/Debug/showEntityId', self._value[1])
        self._value[2] = Obj.get('conf/Debug/showAirWall', self._value[2])
        self._value[4] = Obj.get('conf/Debug/openPathTrace', self._value[4])
        self._value[5] = Obj.get('conf/Debug/showShakeCamera', self._value[5])
        self._value[6] = Obj.get('conf/Debug/turnOffSysLog', self._value[6])
        self._value[7] = Obj.get('conf/Debug/turnOffScriptLog', self._value[7])

    def save(self):
        Obj['conf/Debug/showMonsterName'] = int(self._value[0])
        Obj['conf/Debug/showEntityId'] = int(self._value[1])
        Obj['conf/Debug/showAirWall'] = int(self._value[2])
        Obj['conf/Debug/openPathTrace'] = int(self._value[4])
        Obj['conf/Debug/showShakeCamera'] = int(self._value[5])
        Obj['conf/Debug/turnOffSysLog'] = int(self._value[6])
        Obj['conf/Debug/turnOffScriptLog'] = int(self._value[7])


class GameSetting(SettingBase):

    def __init__(self):
        super(GameSetting, self).__init__('gameSettting')
        self._value = [0]

    def apply(self, data = None):
        GameSettingObj.switchAvatarPhysics(gameglobal.KEYBOARD_MODE)
        loadingProgress.gOptimizeLoading = self._value[0]
        gameglobal.JOIN_TEAM_OPEN_CC = bool(Obj.get(keys.SET_TEAM_OPEN_CC, 0))
        gameglobal.JOIN_ZHANCHANG_OPEN_CC = bool(Obj.get(keys.SET_ZHANCHANG_OPEN_CC, 0))

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def default(self):
        self._value = [0]

    def getDefault(self):
        return [0]

    def update(self, value):
        for i, item in enumerate(value):
            self.value[i] = item

    def save(self):
        Obj[keys.SET_LOADING_OPTIMIZE] = int(self._value[0])

    def saveHideValue(self):
        Obj[keys.SET_CAMERA_POSITION] = int(gameglobal.rds.cam.getCurrentScrollNum())
        Obj.save()

    def load(self):
        t = Obj.get(keys.SET_LOADING_OPTIMIZE, 1)
        self._value[0] = t

    def setMaxScrollRange(self, keyboardValue, mouseValue):
        p = BigWorld.player()
        if p.getOperationMode() == gameglobal.KEYBOARD_MODE:
            gameglobal.rds.cam.setMaxScrollRange(keyboardValue)
        else:
            gameglobal.rds.cam.setMaxScrollRange(mouseValue)

    def setShortCut(self, mode, oldMode):
        enableOperationShortCut = gameglobal.rds.configData.get('enableOperationShortCut', False)
        if not enableOperationShortCut:
            return
        if not BigWorld.player().isNewRoleForOperation():
            return
        isInitOperation = gameglobal.rds.ui.actionbar.isInitOperation()
        if isInitOperation:
            return
        isFirstTimeOperation = gameglobal.rds.ui.actionbar.isFirstTimeOperation(mode)
        if isFirstTimeOperation:
            gameglobal.rds.ui.actionbar.switchClientShortCut(mode, oldMode)
            gameglobal.rds.ui.actionbar.setFirstTimeOperation(mode, 1)

    def switchAvatarPhysics(self, physicsMode):
        oldMode = BigWorld.player().getOperationMode()
        self.setShortCut(physicsMode, oldMode)
        p = BigWorld.player()
        if hasattr(p, 'stateMachine') and not p.stateMachine.checkStatus(const.CT_SWITCH_OPMODE):
            BigWorld.player().showTopMsg('此状态下不能切换操作模式')
            return False
        lockOperationMode = getattr(p, 'lockOperationMode', None)
        if lockOperationMode and physicsMode != lockOperationMode[0]:
            BigWorld.player().showTopMsg('此状态下不能切换操作模式')
            return False
        gameglobal.rds.ui.subTarget.hideSubTargetUnitFrame()
        if physicsMode == gameglobal.MOUSE_MODE:
            p.setPhysics(physicsMode)
            BigWorld.player().showTopMsg('切换为鼠标操作模式')
            p.guideSkillCancelMode = gameglobal.GUIDESKILL_CANCEL_NOMAL
            gameglobal.rds.ui.actionbar.showMouseIcon(False)
            gameglobal.rds.ui.systemButton.setActionModeIndicator(False, 0)
        elif physicsMode == gameglobal.ACTION_MODE:
            p.setPhysics(physicsMode)
            BigWorld.player().showTopMsg('切换为动作操作模式')
            p.guideSkillCancelMode = gameglobal.GUIDESKILL_CANCEL_NOMAL
            gameglobal.rds.ui.actionbar.showMouseIcon(True)
            key = BigWorld.player().operation.get(gameglobal.ACTION_PLUS, {}).get(gameglobal.PLUS_SHOW_CURSOR_KEY)
            gameglobal.rds.ui.systemButton.setActionModeIndicator(True, key)
            gameglobal.rds.ui.subTarget.showSubTargetUnitFrame()
        else:
            p.setPhysics(physicsMode)
            BigWorld.player().showTopMsg('切换为键盘操作模式')
            gameglobal.rds.ui.actionbar.showMouseIcon(False)
            gameglobal.rds.ui.systemButton.setActionModeIndicator(False, 0)
        keyArr = hotkeyProxy.getInstance().shortKey.getKeyDescArray()
        gameglobal.rds.ui.actionbar.setSlotKeyText(keyArr)
        gameglobal.rds.ui.zaiju.setSlotKeyText(keyArr)
        gameglobal.rds.ui.zaijuV2.refreshSkillSlotsBind()
        gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_IN_SKILL_RANGE)
        return True


def _resolutionChanged(newW, newH, newWindowed):
    w, h, windowed, _ = BigWorld.getScreenState()
    if BigWorld.realFullScreen():
        windowed = 2
    if newW != w or newH != h or newWindowed != windowed:
        return True
    else:
        return False


def setScreenSize(w = None, h = None, isWindow = None, needSave = False):
    if not w:
        w = Obj.get(keys.SET_WIDTH, gameglobal.DEFAULT_SCREEN_WIDTH)
        h = Obj.get(keys.SET_HEIGHT, gameglobal.DEFAULT_SCREEN_HEIGHT)
        isWindow = Obj.get(keys.SET_WINDOW, 1)
    if _resolutionChanged(w, h, isWindow):
        fxaSample = BigWorld.getFXAASample()
        if isWindow == 0:
            BigWorld.realFullScreen(False)
            C_ui.setVideoMode(w, h, 32, 60, False, fxaSample, True)
        elif isWindow == 1:
            BigWorld.realFullScreen(False)
            C_ui.setVideoMode(w, h, 32, 60, True, fxaSample, True)
        elif isWindow == 2:
            BigWorld.realFullScreen(True)
            C_ui.setVideoMode(w, h, 32, 60, False, fxaSample, True)
    if gameglobal.rds.configData.get('enableCustomIme', False):
        ime.onRecreateDevice()
    if needSave:
        saveScreenSize(w, h, isWindow)


def saveScreenSize(w, h, isWindow):
    Obj[keys.SET_WIDTH] = int(w)
    Obj[keys.SET_HEIGHT] = int(h)
    Obj[keys.SET_WINDOW] = int(isWindow)
    Obj.save()


def getShaderIndex():
    ret = Obj.get(keys.SET_SHADER_INDEX, 0)
    return ret


def lockShaderIndex(index):
    p = BigWorld.player()
    setShaderIndex(index, False, True, False)
    p.lockShaderIndex = True


def restoreShader():
    p = BigWorld.player()
    p.lockShaderIndex = False
    if getattr(p, 'recoredShaderIndex', None):
        index, needSave, needApply = p.recoredShaderIndex
        setShaderIndex(index, needSave, needApply)


def setShaderIndex(index = None, needSave = True, needApply = True, needRecorde = True):
    if index == None:
        needSave = False
        index = getShaderIndex()
    param = [((False,
       0,
       0,
       0), None, None),
     ((True,
       -0.2,
       -0.07,
       0.05), 'soft', 0.7),
     ((True,
       -0.7,
       -0.02,
       0.05), None, 0.8),
     ((True,
       -0.15,
       0,
       0.07), 'clear', 0.7),
     ((True,
       -0.4,
       0.01,
       0.03), 'classic', 0.7),
     ((True,
       -0.4,
       0.05,
       0.1), 'dark', None),
     ((True,
       -0.2,
       -0.03,
       -0.1), 'abao', None)]
    p = BigWorld.player()
    if p and needRecorde:
        p.recoredShaderIndex = (index, needSave, needApply)
    if getattr(p, 'lockShaderIndex', False):
        return
    if needApply and not getattr(p, 'forbidApplyShader', False):
        if param[index][0]:
            BigWorld.colorVibrance(param[index][0][0], param[index][0][1], param[index][0][2], param[index][0][3])
        if param[index][1]:
            BigWorld.setColorGrading('env/colormap/style/' + param[index][1] + '.tga', 1)
        else:
            BigWorld.setColorGrading('', 1)
        if param[index][2]:
            BigWorld.setBloom(True, param[index][2])
    if needSave:
        Obj[keys.SET_SHADER_INDEX] = index


def isNewConfig():
    return hasattr(BigWorld, 'useNewVideoConfig') and hasattr(BigWorld, 'setSharpen') and gameglobal.rds.configData.get('enableNewVideoConfig', True)


def useNewSettings(originalDict, videoQualityLv):
    if isNewConfig():
        if originalDict['HQLS'] == 1:
            originalDict['HQLS'] = 3
        if videoQualityLv == 2 or videoQualityLv == 0:
            BigWorld.setInnerScreenSize(0.75)
            BigWorld.setSharpen(1, 1)
        else:
            BigWorld.setInnerScreenSize(1)
            BigWorld.setSharpen(0, 0)
    else:
        BigWorld.setInnerScreenSize(1)
        if hasattr(BigWorld, 'setSharpen'):
            BigWorld.setSharpen(0, 0)


def getNewData():
    if isNewConfig():
        return vsdDataNew
    else:
        return vsdDataOld


class VideoQualitySetting(SettingBase):

    def __init__(self):
        super(VideoQualitySetting, self).__init__('videoQualitySetting')
        self.saveFile = 'conf/screen/'
        self.setScale = 1
        self.lvParam = ['lowest',
         'low',
         'mid',
         'high',
         'ultra']
        self.otherParam = ['defaultSet', 'videoQualityLv']
        self.settingParam = ['HQS',
         'DL',
         'SHADOW',
         'SSAO',
         'FXAA',
         'DOF',
         'REF',
         'VSYNC',
         'HQLS',
         'SUNSHAFT',
         'HEAT']
        self.shadowEffect = [0,
         0,
         1,
         2,
         3]
        self.effectParam = ['PLAYEREFF',
         'AVATAREFF',
         'MONSTEREFF',
         'NPCEFF',
         'ENEMYAVATAREFF']
        self.specialParam = ['motionBlur',
         'screenEffect',
         'animateCamera',
         'cameraShake',
         'disableSkillHover',
         'hitFreeze',
         'showBloodLabel',
         'modelShake',
         'bloom',
         'wsEffect',
         'darkAngle',
         'caustics',
         'foregroundFPS',
         'backgroundFPSSlider',
         'showEquipEnhanceEffect',
         'enablePhysics',
         'enableMemorySetting',
         'enableMinimalist',
         'skinLight']
        self.lodParam = ['setViewFactor',
         'setTerrainRenderLevel',
         'forceSkipMipMap',
         'modelLODScale',
         'textureLODSizeLimit',
         'ModelShowNum',
         'effShowNum']
        if BigWorld.isWow64():
            self.lodFactor = [[(0.33, 0.5),
              (0.33, 0.5),
              (0.39, 0.75),
              (0.39, 0.9),
              (0.46, 1.0)],
             [(3, 100),
              (3, 200),
              (4, 350),
              (4, 500),
              (4, 700)],
             [(1, 30, 20),
              (1, 60, 40),
              (0, 85, 70),
              (0, 105, 110),
              (0, 105, 135)],
             [0.5, 0.75, 1.0],
             [0.25, 0.5, 1.0],
             [20, 50, 80],
             [100, 300, 800]]
        else:
            self.lodFactor = [[(0.33, 0.5),
              (0.33, 0.5),
              (0.33, 0.75),
              (0.39, 0.9),
              (0.39, 1.0)],
             [(3, 100),
              (3, 200),
              (4, 350),
              (4, 500),
              (4, 700)],
             [(1, 30, 20),
              (1, 60, 40),
              (0, 90, 70),
              (0, 90, 70),
              (0, 90, 70)],
             [0.5, 0.75, 1.0],
             [0.25, 0.5, 1.0],
             [10, 30, 60],
             [100, 300, 800]]
        self.lodDict = dict(zip(self.lodParam, self.lodFactor))
        self.shadowDist = [8.0,
         16.0,
         16.0,
         24.0,
         64.0]
        self._value = self.getDefault()
        self.originalData = self._value
        self.needShadowUfo = False
        self.effectCacheNumber = [100, 200, 400]
        self.oldFloraMaxDrawingDist = 0
        self.oldFloraDensity = 0

    def getParamIndex(self, paramStr):
        i = 0
        paramsTuple = (self.otherParam,
         self.settingParam,
         self.effectParam,
         self.specialParam,
         self.lodParam)
        for params in paramsTuple:
            if paramStr in params:
                return i + params.index(paramStr)
            i += len(params)

        return -1

    def setTextureLODSizeLimit(self):
        lodIndex = self.originalData[len(self.otherParam) + len(self.settingParam) + len(self.effectParam) + len(self.specialParam):]
        forceSkipMipMapSize = self.lodDict[self.lodParam[2]][lodIndex[2]][0]
        charSize = self.lodDict[self.lodParam[2]][lodIndex[2]][2]
        sceneSize = self.lodDict[self.lodParam[2]][lodIndex[2]][1]
        BigWorld.forceSkipMipMap(forceSkipMipMapSize)
        BigWorld.textureLODSizeLimit('scene', sceneSize)
        BigWorld.textureLODSizeLimit('char', charSize)

    def isMinimalist(self, data):
        if not data:
            return False
        index = self.getParamIndex('enableMinimalist')
        return data[index]

    def getMinimalist(self):
        return self.isMinimalist(self.originalData)

    def apply(self, data = None):
        p = BigWorld.player()
        self.originalData = data if data else self._value
        enableMinimalist = self.isMinimalist(self.originalData)
        if enableMinimalist:
            self.originalData = self.getDefault('minimalist')
        if gameglobal.rds.GameState == gametypes.GS_START:
            return
        originalDict = {}
        assert self.otherParam == ['defaultSet', 'videoQualityLv']
        self.setScale = 0.5 if enableMinimalist and not p.inWingWarCity() else 1
        setScale = self.setScale
        videoQualityLv = self.getRealVideoQualityLv(self.originalData[1])

        def getSettingByVQLv(settings):
            assert len(settings) == 5
            return settings[videoQualityLv]

        BigWorld.enableDrawControl(True)
        BigWorld.enableSkipSkeletonUpdate(getSettingByVQLv([True,
         True,
         True,
         True,
         False]))
        BigWorld.renderTerrainUFO(getSettingByVQLv([False,
         True,
         True,
         True,
         True]))
        BigWorld.simplifiedSkeletonCalcDist(getSettingByVQLv([16.0,
         24.0,
         48.0,
         64.0,
         80.0]))
        BigWorld.setAnimationLevel(getSettingByVQLv([0,
         0,
         1,
         1,
         1]))
        BigWorld.skeletonRecalcInterval(getSettingByVQLv([0.1,
         0.0,
         0.0,
         0.0,
         0.0]))
        newFloraMaxDrawingDist = getSettingByVQLv([150,
         250,
         500,
         500,
         500]) * setScale
        newFloraDensity = getSettingByVQLv([0.3,
         0.5,
         1.0,
         1.0,
         1.0]) * setScale
        if not formula.inDotaBattleField(getattr(p, 'mapID', 0)):
            BigWorld.setFloraMaxDrawingDist(newFloraMaxDrawingDist)
            BigWorld.setFloraDensity(newFloraDensity)
        self.oldFloraMaxDrawingDist = newFloraMaxDrawingDist
        self.oldFloraDensity = newFloraDensity
        oldShowEquipEnhanceEff = gameglobal.SHOW_EQUIP_ENHANCE_EFF
        p = BigWorld.player()
        p.selfEffectLv, p.otherAvatarEffectLv, p.monsterEffectLv, p.npcEffectLv, p.enemyAvatarEffectLv, gameglobal.ENABLE_MOTION_BLUR, gameglobal.ENABLE_SKILL_SCREEN_EFFECT, gameglobal.ENABLE_ANIMATE_CAMERA, gameglobal.ENABLE_SHAKE_CAMERA, gameglobal.ENABLE_SKILL_HOVER_EFFECT, gameglobal.ENABLE_BE_HIT_FREEZE, gameglobal.showBloodLabel, gameglobal.modelShake, unBloom, gameglobal.showWsEffect, darkAngle, caustics, gameglobal.FORGROUND_FPS, gameglobal.BACKGROUND_FPS, gameglobal.SHOW_EQUIP_ENHANCE_EFF, enablePhysics, enableMemorySetting, enableMinimalist, skinLight = self.originalData[len(self.otherParam) + len(self.settingParam):len(self.otherParam) + len(self.settingParam) + len(self.effectParam) + len(self.specialParam)]
        p.spaceEffectLv = p.npcEffectLv
        lodIndex = self.originalData[len(self.otherParam) + len(self.settingParam) + len(self.effectParam) + len(self.specialParam):]
        self.setSkinLight(skinLight)
        forceSkipMipMapSize = self.lodDict[self.lodParam[2]][lodIndex[2]][0]
        charSize = self.lodDict[self.lodParam[2]][lodIndex[2]][2]
        sceneSize = self.lodDict[self.lodParam[2]][lodIndex[2]][1]
        BigWorld.forceSkipMipMap(forceSkipMipMapSize)
        BigWorld.textureLODSizeLimit('scene', sceneSize)
        BigWorld.textureLODSizeLimit('char', charSize)
        terrainRenderLevel = self.lodDict[self.lodParam[1]][lodIndex[1]][0]
        terrainNormalMapViewDist = self.lodDict[self.lodParam[1]][lodIndex[1]][1]
        BigWorld.setTerrainRenderLevel(terrainRenderLevel)
        BigWorld.terrainNormalMapViewDist(terrainNormalMapViewDist)
        for i, item in enumerate(self.settingParam):
            if item == 'DOF':
                if hasattr(BigWorld, 'enableU3DOF'):
                    BigWorld.enableU3DOF(self.originalData[i + len(self.otherParam)])
            else:
                originalDict[item] = self.originalData[i + len(self.otherParam)]

        if originalDict['HQLS'] >= 4:
            originalDict['SSAO'] = 1
        originalDict['VSYNC'] = 0
        originalDict['HQLS'] = self.shadowEffect[originalDict['HQLS']]
        originalDict['SHADOW'] = originalDict['HQLS']
        player = BigWorld.player()
        if getattr(player, 'mapID', 0) == const.SPACE_NO_WING_WORLD_ISLAND:
            originalDict['SHADOW'] = 0
        originalDict['VQLV'] = videoQualityLv
        useNewSettings(originalDict, videoQualityLv)
        self.setVideoParams(originalDict)
        BigWorld.setDynamicShadowDist(getSettingByVQLv(self.shadowDist))
        gameglobal.rds.ui.littleMap.enableMapBlend(False)
        clientcom.resetLimitFps()
        BigWorld.setAnisotropyLevel(getSettingByVQLv([1.0,
         2.0,
         4.0,
         8.0,
         16.0]))
        BigWorld.setBloom(not unBloom)
        screenEffect.showDarkAngle(darkAngle)
        BigWorld.enableCaustics(caustics)
        Pixie.globalSceneDrawLevel(p.spaceEffectLv)
        shadowQuality = self.shadowEffect[self.originalData[10]]
        if self.originalData[10] > 0 and shadowQuality >= gameglobal.VEDIO_QUALITY_LOWEST and videoQualityLv in (gameglobal.VEDIO_QUALITY_LOW, gameglobal.VEDIO_QUALITY_MID):
            self.needShadowUfo = True
        else:
            self.needShadowUfo = False
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            self.refreshUFO(self.originalData)
        self.resetEquipEnhanceEff(oldShowEquipEnhanceEff, gameglobal.SHOW_EQUIP_ENHANCE_EFF)
        self.setPhysics(enablePhysics)
        self.setMemorySetting(enableMemorySetting, data)
        self.setMinimalistSetting(enableMinimalist)
        self.resetShadowAvatarNum()
        self.resetAvatarModelNoDrawDist(lodIndex[5])
        sfx.gEffectMgr.effCounter.maxSumEffectCount = self.lodDict[self.lodParam[6]][lodIndex[6]] * setScale
        sfx.gEffectMgr.effectCache.MAX_CACHE_COUNT = self.effectCacheNumber[lodIndex[6]] * setScale
        BigWorld.setViewFactor(self.lodDict[self.lodParam[0]][lodIndex[0]][0] * setScale)
        BigWorld.modelLODScale(self.lodDict[self.lodParam[0]][lodIndex[0]][1])
        self.setAvatarModelCnt()
        if formula.inDotaBattleField(getattr(p, 'mapID', 0)):
            BigWorld.setFloraDensity(1.0)
        lodLoadLevel = videoQualityLv + 1
        if enableMinimalist:
            lodLoadLevel = 0
        BigWorld.setLODLoadLevel(lodLoadLevel)

    def setVideoParams(self, params):
        print 'setVideoParams', params
        BigWorld.setVideoParams(params)

    def getShadowDist(self):
        lv = self.getVideoQualityLv()
        realLv = self.getRealVideoQualityLv(lv)
        if realLv < len(self.shadowDist):
            return self.shadowDist[realLv]
        return self.shadowDist[0]

    def setAvatarModelCnt(self):
        avatarCntOptimize = clientcom.needAvatarCntOptimize()
        if avatarCntOptimize:
            gameglobal.AVATAR_MODEL_CNT = min(gameglobal.AVATAR_MODEL_CNT, gameglobal.AVATAR_OPTIMIZE_MODEL_CNT)
            return gameglobal.AVATAR_MODEL_CNT
        lodIndex = self.originalData[len(self.otherParam) + len(self.settingParam) + len(self.effectParam) + len(self.specialParam):]
        gameglobal.AVATAR_MODEL_CNT = self.lodDict[self.lodParam[5]][lodIndex[5]] * self.setScale
        return gameglobal.AVATAR_MODEL_CNT

    def setSkinLight(self, value):
        if hasattr(BigWorld, 'setJsSkinCompensate'):
            BigWorld.setJsSkinCompensate(value * 0.02 - 1)

    def resetAvatarModelNoDrawDist(self, videoQualityLv):
        try:
            spaceNo = getattr(BigWorld.player(), 'spaceNo', 0)
            mapId = formula.getMapId(spaceNo)
            dist = MCD.data.get(mapId, {}).get('AvatarModelNoDrawDist', gameglobal.AVATAR_MODEL_NO_DRAW_DISTS.get(videoQualityLv, 60))
            BigWorld.setAvatarModelNoDrawDist(dist)
        except:
            pass

    def resetShadowAvatarNum(self):
        try:
            videoQualityLv = self.getRealVideoQualityLv(self.getVideoQualityLv())
            if videoQualityLv >= 3:
                BigWorld.SetShadowAvatarNum(40)
            else:
                BigWorld.SetShadowAvatarNum(20)
        except:
            pass

    def resetEquipEnhanceEff(self, oldShowEquipEnhanceEff, new):
        if oldShowEquipEnhanceEff != new:
            ents = BigWorld.entities.values()
            avatars = []
            for ent in ents:
                if ent and ent.__class__.__name__ in 'Avatar, PlayerAvatar':
                    avatars.append(ent)

            if oldShowEquipEnhanceEff:
                for avatar in avatars:
                    avatar.releaseEquipEnhanceEffects()

            else:
                for avatar in avatars:
                    avatar.refreshEquipEnhanceEffects()

    def setPhysics(self, enablePhysics):
        gameglobal.gDisableBulletPhy = not enablePhysics
        p = BigWorld.player()
        clientcom.setModelPhysics(p.model)

    def setMemorySetting(self, enableMemorySetting, data):
        if BigWorld.isWow64():
            return
        if enableMemorySetting:
            self.lodFactor[5] = [10, 20, 40]
            self.lodFactor[0] = [(0.33, 0.5),
             (0.33, 0.5),
             (0.45, 0.75),
             (0.45, 0.75),
             (0.45, 0.75)]
        else:
            self.lodFactor[5] = [10, 30, 60]
            self.lodFactor[0] = [(0.33, 0.5),
             (0.45, 0.5),
             (0.45, 0.75),
             (0.67, 1.0),
             (0.67, 1.0)]
        self.showMessage(enableMemorySetting, data)

    def showMessage(self, enableMemorySetting, data):
        if not data:
            return
        if enableMemorySetting:
            msg = '内存优化选项可能会导致间歇的卡顿,在重启游戏后生效'
        else:
            msg = '内存优化关闭会加大部分内存的消耗,在重启游戏后生效'
        gameglobal.rds.ui.systemTips.show(msg)

    def setMinimalistSetting(self, enableMinimalist):
        if hasattr(BigWorld, 'enableMinimalist'):
            BigWorld.enableMinimalist(enableMinimalist)

    def getViewFactor(self):
        lodIndex = self.originalData[len(self.otherParam) + len(self.settingParam) + len(self.effectParam) + len(self.specialParam)]
        return self.lodDict['setViewFactor'][lodIndex][0] * self.setScale

    def setWsEffect(self, value):
        self._value[len(self.otherParam) + len(self.settingParam) + 14] = value

    def default(self):
        self._value = self.getDefault()

    def getDefault(self, lv = 'mid'):
        vsdData = getNewData()
        if lv not in vsdData:
            return
        midValue = vsdData.get(lv, {})
        videoQualityLv = 0
        if lv in self.lvParam:
            videoQualityLv = self.lvParam.index(lv)
        ret = [1, videoQualityLv]
        for item in self.settingParam:
            ret.append(midValue.get(item, 0))

        for item in self.effectParam:
            ret.append(midValue.get(item, 0))

        for item in self.specialParam:
            ret.append(midValue.get(item, 0))

        for item in self.lodParam:
            ret.append(midValue.get(item, 0))

        return ret

    def update(self, value):
        tmp = list(value)
        self._value = tmp

    def save(self):
        index = 0
        for i, item in enumerate(self.otherParam):
            Obj[self.saveFile + item] = self._value[i + index]

        index += len(self.otherParam)
        for i, item in enumerate(self.settingParam):
            Obj[self.saveFile + item] = self._value[i + index]

        index += len(self.settingParam)
        for i, item in enumerate(self.effectParam):
            Obj[self.saveFile + item] = self._value[i + index]

        index += len(self.effectParam)
        for i, item in enumerate(self.specialParam):
            Obj[self.saveFile + item] = self._value[i + index]

        index += len(self.specialParam)
        for i, item in enumerate(self.lodParam):
            Obj[self.saveFile + item] = self._value[i + index]

    def load(self):
        videoQualityLv = self.getRealVideoQualityLv(self.getVideoQualityLv())
        midValue = self.getVideoQuality(videoQualityLv)
        i = 0
        for item in self.otherParam:
            self._value[i] = Obj.get(self.saveFile + item, midValue[i])
            i += 1

        for item in self.settingParam:
            self._value[i] = Obj.get(self.saveFile + item, midValue[i])
            i += 1

        for item in self.effectParam:
            self._value[i] = Obj.get(self.saveFile + item, midValue[i])
            i += 1

        for item in self.specialParam:
            self._value[i] = Obj.get(self.saveFile + item, midValue[i])
            i += 1

        for item in self.lodParam:
            self._value[i] = Obj.get(self.saveFile + item, midValue[i])
            i += 1

        gameglobal.gDisableBulletPhy = not Obj.get(self.saveFile + 'enablePhysics', 0)

    def isDofEnable(self):
        return self._value[7]

    def isDofForceEnable(self):
        player = BigWorld.player()
        mcd = MCD.data.get(getattr(player, 'mapID', 0), {})
        if mcd.get('enableU3DOF', 0):
            return True
        return self.isDofEnable()

    def getAvatarCntWithVQ(self):
        return self.setAvatarModelCnt()

    def getVideoQuality(self, videoQuality):
        lv = self.lvParam[videoQuality]
        return self.getDefault(lv)

    def refreshUFO(self, data):
        if not gameglobal.NEW_UFO_RULE:
            return
        ens = BigWorld.entities.values()
        for en in ens:
            if not hasattr(en, 'fashion') or not en.fashion:
                continue
            if en.fashion.ufo and en.fashion.ufo.ufoType == ufo.UFO_SHADOW:
                if not self.needShadowUfo:
                    en.fashion.attachUFO(ufo.UFO_NULL)
            elif not en.fashion.ufo or en.fashion.ufo.ufoType == ufo.UFO_NULL:
                if self.needShadowUfo:
                    en.fashion.attachUFO(ufo.UFO_SHADOW)

    def getVideoQualityLv(self):
        return Obj.get(self.saveFile + self.otherParam[1], 2)

    def setMemoryRate(self, rate):
        Obj[self.saveFile + 'memoryDBRate'] = rate

    def getRealVideoQualityLv(self, videoQualityLv):
        return videoQualityLv


SoundSettingObj = SoundSetting()
VideoQualitySettingObj = VideoQualitySetting()
DebugSettingObj = DebugSetting()
GameSettingObj = GameSetting()
