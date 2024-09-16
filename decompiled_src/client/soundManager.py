#Embedded file name: I:/bag/tmp/tw2/res/entities\client/soundManager.o
import Sound
import BigWorld
import const
import gamelog
import appSetting
import gametypes
import gameglobal
from sMath import distance3D
from helpers import soundVolGradient
from gameclass import Singleton
from data import ui_sound_data as USD
from data import sys_config_data as SYSCD
WM_MUSIC_TAG = 60000
WM_AMBIENT_TAG = 70000
SM_SCENARIO = 0
SM_DYING = 1
SM_BOSS = 2
SM_PHASE = 3
MAP = [SM_SCENARIO,
 SM_DYING,
 SM_BOSS,
 SM_PHASE]
fxTypeDict = SYSCD.data.get('FxTypeDict', {})

class StateMusicSlot(object):

    def __init__(self):
        self.music = None
        self.ambient = None
        self.active = False
        self.playing = False

    def play(self):
        if self.music:
            Sound.playStateMusic(self.music)
        if self.ambient:
            Sound.playAmbient(self.ambient)
        self.playing = True

    def stop(self):
        self.playing = False
        Sound.stopStateMusic()
        Sound.playAmbient('')


class StateMusic(object):

    def __init__(self):
        self.slot = []
        for i in MAP:
            self.slot.append(StateMusicSlot())

    def setState(self, state, status, musicPath, ambientPath = ''):
        self.slot[state].active = status
        self.slot[state].music = musicPath
        self.slot[state].ambient = ambientPath
        if status:
            for i in xrange(state):
                if self.slot[i].active == True:
                    return
            else:
                if self.slot[state].playing == False:
                    self.slot[state].play()
        elif self.slot[state].playing == True:
            self.slot[state].stop()
            for i in xrange(state, len(MAP)):
                if self.slot[i].active == True:
                    self.slot[i].play()
                    return

    def clearState(self):
        for i in self.slot:
            i.active = False
            i.stop()


class SoundManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(SoundManager, self).__init__()
        self.sdHandles = {}
        self.voiceHandle = None
        self.rawfileHandle = None
        self.stateMusic = StateMusic()
        self.lastUseSkill = {}
        self.playerSoundScale = SYSCD.data.get('playerSoundScale', 1.0)
        self.otherSoundScale = SYSCD.data.get('otherSoundScale', 0.5)
        self.voiceQueue = []
        self.voicePriority = 0
        self.rawfilePriority = 0
        self.callbackHandle = None
        self.curStateMusic = None

    def playSound(self, idx, owner = None, interrupt = True, position = (0, 0, 0)):
        if gameglobal.rds.GameState >= gametypes.GS_LOADING:
            player = BigWorld.player()
            if getattr(player, 'isStraightLvUp', False):
                return
        data = USD.data.get(idx, None)
        gamelog.debug('playSound', idx)
        if data:
            type = data['type']
            path = data['path']
            soundId = None
            try:
                if not owner or not owner.inWorld:
                    owner = BigWorld.player()
                if not position:
                    position = (0, 0, 0)
                if int(distance3D(position, (0, 0, 0))) == 0 and owner:
                    position = owner.position
                if type == const.SOUND_UI:
                    self.sdHandles[idx] = Sound.playSimple(path)
                    soundId = self.sdHandles[idx]
                elif type == const.SOUND_FX:
                    self.sdHandles[idx] = self.playFx(path, position, True, owner)
                    soundId = self.sdHandles[idx]
                elif type == const.SOUND_VOICE:
                    priority = data.get('priority', 0)
                    delayPlay = data.get('delayPlay', 0)
                    if self.voiceHandle and Sound.isPlaying(self.voiceHandle):
                        if not interrupt:
                            return 0
                        if priority >= self.voicePriority:
                            Sound.stopVoice(self.voiceHandle)
                        else:
                            if delayPlay:
                                self.voiceQueue.append(idx)
                                self.delayPlay()
                            return 0
                    self.voicePriority = priority
                    self.voiceHandle = Sound.playVoice(path, position)
                    self.sdHandles[idx] = self.voiceHandle
                    soundId = self.voiceHandle
                elif type == const.SOUND_CUE:
                    self.sdHandles[idx] = Sound.beginCue(path)
                    soundId = self.sdHandles[idx]
                elif type == const.SOUND_RAW:
                    if hasattr(Sound, 'playRawfile'):
                        priority = data.get('priority', 0)
                        delayPlay = data.get('delayPlay', 0)
                        if self.rawfileHandle and Sound.isRawfilePlaying(self.rawfileHandle):
                            if not interrupt:
                                return 0
                            if priority >= self.rawfilePriority:
                                Sound.stopRawfile(self.rawfileHandle)
                            else:
                                if delayPlay:
                                    self.voiceQueue.append(idx)
                                    self.delayPlay()
                                return 0
                        self.rawfilePriority = priority
                        self.rawfileHandle = Sound.playRawfile(path)
                        self.sdHandles[idx] = self.rawfileHandle
                        soundId = self.rawfileHandle
                elif type == const.SOUND_MUSIC:
                    self.playMusic(idx)
                    return
                if soundId:
                    mixDatas = data.get('mixCategorys', None)
                    if mixDatas:
                        for category, desVolumeScale, duration, recoverTime in mixDatas:
                            volume = appSetting.SoundSettingObj.getVolumeByCategory(category)
                            if volume and volume > 0:
                                origVolume = volume / 100.0
                                desVolume = origVolume * desVolumeScale
                                Sound.addMix(category, origVolume, desVolume, duration, recoverTime)

            except:
                gamelog.error('≤•∑≈…˘“Ù ß∞‹ ', type, path)

            return soundId

    def playMusic(self, idx):
        data = USD.data.get(idx, None)
        if data:
            mPath = data.get('path', '')
            mType = data.get('type', 0)
            if mPath and mType == const.SOUND_MUSIC:
                Sound.playStateMusic(mPath)
                self.curStateMusic = idx

    def stopMusic(self, idx):
        if self.curStateMusic == idx or idx == -1:
            Sound.stopStateMusic()
            self.curStateMusic = None

    def playAmbient(self, idx):
        data = USD.data.get(idx, None)
        if data:
            mPath = data.get('path', '')
            mType = data.get('type', 0)
            if mPath and mType == const.SOUND_AMBIENT:
                Sound.playAmbient(mPath)

    def haveSdHandle(self, idx):
        if self.sdHandles.has_key(idx):
            return True
        return False

    def stopNpcVoice(self):
        if self.voiceHandle and Sound.isPlaying(self.voiceHandle):
            Sound.stopVoice(self.voiceHandle)

    def stopSound(self, idx, soundId = None):
        data = USD.data.get(idx, None)
        if data:
            type = data['type']
            if self.sdHandles.has_key(idx):
                if not soundId:
                    soundId = self.sdHandles[idx]
            if type == const.SOUND_MUSIC:
                self.stopMusic(idx)
            if soundId:
                if type == const.SOUND_FX:
                    Sound.stopFx(soundId)
                elif type == const.SOUND_UI:
                    Sound.stopSimple(soundId)
                elif type == const.SOUND_VOICE:
                    Sound.stopVoice(soundId)
                elif type == const.SOUND_CUE:
                    Sound.endCue(soundId)
                elif type == const.SOUND_RAW:
                    if hasattr(Sound, 'stopRawfile'):
                        Sound.stopRawfile(soundId)
                if self.sdHandles.has_key(idx) and soundId == self.sdHandles[idx]:
                    del self.sdHandles[idx]

    def playPhaseMusic(self, spaceNo, status):
        musicIdx = WM_MUSIC_TAG + spaceNo
        musicPath = USD.data.get(musicIdx, {}).get('path', '')
        ambientIdx = WM_AMBIENT_TAG + spaceNo
        ambientPath = USD.data.get(ambientIdx, {}).get('path', '')
        if musicPath or ambientPath:
            self.stateMusic.setState(SM_PHASE, status, musicPath, ambientPath)
        elif not status:
            self.stateMusic.setState(SM_PHASE, status, None)

    def playBossMusic(self, idx, status):
        data = USD.data.get(idx, None)
        if data and data['path']:
            self.stateMusic.setState(SM_BOSS, status, data['path'])

    def playScenarioMusic(self):
        pass

    def stopStateMusic(self):
        self.stateMusic.clearState()

    def playHitFx(self, path, param, hitWeaponTime, owner, scale = 1):
        if owner.inWorld:
            soundScale = 1.0
            if owner.fashion.isPlayer:
                soundScale = self.playerSoundScale
            else:
                soundScale = self.otherSoundScale
            Sound.playHitFx(path, self._getFxType(path), param, hitWeaponTime, owner.position, soundScale * scale, False)

    def playFx(self, path, position, needInstance, owner = None, scale = 1):
        soundScale = 1.0
        if owner and owner.inWorld:
            soundScale = 1.0
            if owner.fashion and owner.fashion.isPlayer:
                soundScale = self.playerSoundScale
            else:
                soundScale = self.otherSoundScale
        return Sound.playFx(path, self._getFxType(path), position, needInstance, None, soundScale * scale)

    def _getFxType(self, path):
        for key, fxPaths in fxTypeDict.items():
            for fxPathPre in fxPaths:
                if path.startswith(fxPathPre):
                    return key

        return 0

    def switchCategoryInCombat(self, inCombat):
        categorys = SYSCD.data.get('combatCategoryScale', {})
        fadeTimes = SYSCD.data.get('combatCategoryScaleTime', [0, 0])
        for category, scale in categorys.items():
            if not appSetting.SoundSettingObj.getEnableByCategory(category):
                continue
            realScale = scale if inCombat else 1
            fadeTime = fadeTimes[0] if inCombat else fadeTimes[1]
            nowSettingVolume = appSetting.SoundSettingObj.getVolumeByCategory(category)
            if fadeTime == 0:
                volume = nowSettingVolume * realScale
                if category == gametypes.CATEGORY_AMBIENT:
                    soundVolGradient.fadeAmbientVol(volume)
                elif category == gametypes.CATEGORY_STATIC:
                    soundVolGradient.fadeStaticVol(volume)
                elif category == gametypes.CATEGORY_MUSIC:
                    soundVolGradient.fadeMusicVol(volume)
                elif category == gametypes.CATEGORY_UI:
                    soundVolGradient.fadeUiVol(volume)
                else:
                    Sound.setCategoryVolume(category, volume)
            else:
                realScale = scale if inCombat else 1
                volume = nowSettingVolume * realScale
                nowVolume = 0
                if category == gametypes.CATEGORY_AMBIENT:
                    nowVolume = Sound.getAmbientVolume()
                elif category == gametypes.CATEGORY_STATIC:
                    nowVolume = Sound.getStaticVolume()
                elif category == gametypes.CATEGORY_MUSIC:
                    nowVolume = Sound.getMusicVolume()
                elif category == gametypes.CATEGORY_UI:
                    nowVolume = Sound.getUiVolume()
                step = float(abs(nowVolume - volume)) / (fadeTime * 10)
                interval = 0.1
                if step == 0:
                    step = 1
                if step < 1:
                    interval = 0.1 / step
                    step = 1
                if category == gametypes.CATEGORY_AMBIENT:
                    soundVolGradient.fadeAmbientVol(volume, step, interval)
                elif category == gametypes.CATEGORY_STATIC:
                    soundVolGradient.fadeStaticVol(volume, step, interval)
                elif category == gametypes.CATEGORY_MUSIC:
                    soundVolGradient.fadeMusicVol(volume, step, interval)
                elif category == gametypes.CATEGORY_UI:
                    soundVolGradient.fadeUiVol(volume, step, interval)
                else:
                    Sound.setCategoryVolume(category, volume)

    def delayPlay(self):
        if not self.voiceQueue:
            return
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
        self.callbackHandle = BigWorld.callback(1, self._delayPlay)

    def _delayPlay(self):
        if not self.voiceQueue:
            return
        priority = 0
        playIdx = 0
        for idx in self.voiceQueue:
            data = USD.data.get(idx, None)
            if data.get('priority', 0) > priority:
                playIdx = idx
                priority = data.get('priority', 0)

        if playIdx:
            if self.playSound(playIdx, None, False):
                self.voiceQueue.remove(playIdx)
            self.callbackHandle = BigWorld.callback(1, self._delayPlay)

    def stopDelayPlay(self):
        self.voiceQueue = []
        self.stopNpcVoice()
        if self.rawfileHandle and Sound.isRawfilePlaying(self.rawfileHandle):
            Sound.stopRawfile(self.rawfileHandle)

    def playRawfileByPath(self, path):
        if self.rawfileHandle and Sound.isRawfilePlaying(self.rawfileHandle):
            Sound.stopRawfile(self.rawfileHandle)
        self.rawfileHandle = Sound.playRawfile(path)
        return self.rawfileHandle
