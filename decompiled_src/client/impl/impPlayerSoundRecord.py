#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerSoundRecord.o
import os
import BigWorld
import Sound
import gamelog
import gameglobal
import const
import gametypes
from guis import soundRecordStateProxy
from gamestrings import gameStrings
from helpers import seqTask
from callbackHelper import Functor
import appSetting
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
STATE_RECORD_SUCCESS = 200
STATE_RECORD_FAILED = 100
STATE_RECORD_UNINIT_ERROR = 101
STATE_RECORD_CLIENT_PLAYING = 102
STATE_RECORD_CLIENT_CAPTURING = 103
STATE_RECORD_DEVICE_INIT_ERROR = 104
STATE_RECORD_CLIENT_NOT_EXIST = 105
STATE_RECORD_THREAD_ERROR = 300

class ImpPlayerSoundRecord(object):

    def startSoundRecord(self, callback = None):
        if not self.enableSoundRecord():
            return
        hasDevice = Sound.querySoundRecordDriver()
        if not hasDevice:
            gameglobal.rds.ui.soundRecordState.setState(soundRecordStateProxy.STATE_NO_DEVICE)
            return
        if Sound.isSoundRecording():
            self.showGameMsg(GMDD.data.SOUND_IS_RECORDING, ())
            return
        time = SCD.data.get('SOUND_RECORD_TIME', 10)
        gameglobal.rds.ui.soundRecordState.setState(soundRecordStateProxy.STATE_RECORDING, time)
        Sound.stopPlayAmr()
        Sound.startSoundRecord(Functor(self.soundRecordFinishCallback, callback), 180)
        BigWorld.callback(0.1, self.reduceSoundVolume)

    def soundRecordFinishCallback(self, callback, resCode, filePath, fileSize, duration):
        gamelog.debug('bgf@ImpPlayerSoundRecord soundRecordFinishCallback', resCode, filePath, fileSize, duration)
        if duration <= 1.0:
            gameglobal.rds.ui.soundRecordState.hide()
            self.showGameMsg(GMDD.data.SOUND_RECORD_TOO_SHORT, ())
            try:
                os.remove(filePath)
            except:
                pass

            return
        gameglobal.rds.ui.soundRecordState.hide()
        if resCode == STATE_RECORD_SUCCESS:
            self._soundRecordFinishCallback(callback, filePath, fileSize, duration)
        else:
            gameglobal.rds.ui.topMessage.showTopMsg(gameStrings.MSG_SOUND_RECORD_FAILED % resCode)

    def endSoundRecord(self):
        if not self.enableSoundRecord():
            return
        if Sound.isSoundRecording():
            Sound.endSoundRecord()
        self.normalSoundVolume()

    def enableSoundRecord(self):
        isExe64 = hasattr(BigWorld, 'isExe64') and BigWorld.isExe64()
        enable = gameglobal.rds.configData.get('enableSoundRecord', False) and hasattr(Sound, 'querySoundRecordDriver') and not isExe64
        return enable

    def soundRecordTimeOut(self):
        self.showGameMsg(GMDD.data.SOUND_RECORD_TIMEOUT, ())
        self.endSoundRecord()

    def _soundRecordFinishCallback(self, callback, filePath, fileSize, duration):
        filePath = os.path.split(filePath)[-1]
        if callback:
            callback(filePath, fileSize, duration)

    def uploadSoundRecord(self, filePath, callback = None):
        seqTask.addNOSSeqTask(gametypes.SOUND_FILE_UPLOAD, (filePath, {}), (self.uploadSoundRecordCallback, [callback]))

    def uploadSoundRecordCallback(self, filePath, key, callback):
        gamelog.debug('bgf@ImpPlayerSoundRecord uploadSoundRecordCallback', filePath, key)
        if callback:
            callback(filePath, key)

    def getTranslation(self, key = '6154e295372cd0980b48bcd46f67790f', callback = None):
        seqTask.addNOSSeqTask(gametypes.SOUND_FILE_TRANSLATE, (key, {}), (self.getTranslationCallback, [callback]))

    def getTranslationCallback(self, key, content, callback = None):
        gamelog.debug('bgf@ImpPlayerSoundRecord getTranslationCallback', key, content)
        if callback:
            callback(key, content)

    def downloadSoundRecord(self, key = '6154e295372cd0980b48bcd46f67790f', callback = None):
        gamelog.debug('bgf@ImpPlayerSoundRecord downloadSoundRecord', key)
        seqTask.addNOSSeqTask(gametypes.SOUND_FILE_DOWNLOAD, (key, {}), (self.downloadSoundRecordCallback, [callback]))

    def downloadSoundRecordCallback(self, key, callback = None):
        gamelog.debug('bgf@ImpPlayerSoundRecord downloadSoundRecordCallback', key)
        if callback:
            callback(key)

    def recordUploadTranslateSound(self, callback = None):

        def uploadCallback(duration, filePath, key):
            self.getTranslation(key, Functor(callback, duration))

        def recordCallback(filePath, fileSize, duration):
            self.uploadSoundRecord(filePath, Functor(uploadCallback, duration))

        self.startSoundRecord(recordCallback)

    def playSoundRecord(self, key, playStartCallback = None, playFinishCallback = None):
        if not self.enableSoundRecord():
            return
        path = '%s/%s.amr' % (const.SOUND_DOWNLOAD_DIR, key)
        gamelog.debug('bgf@ImpPlayerSoundRecord playSoundRecord', path)
        Sound.playAmr(path, Functor(self.playSoundRecordFinishCallback, playFinishCallback))
        if playStartCallback:
            playStartCallback()
        BigWorld.callback(0.1, self.reduceSoundVolume)

    def playSoundRecordFinishCallback(self, playFinishCallback, resCode, filePath):
        gamelog.debug('bgf@ImpPlayerSoundRecord playSoundRecordFinishCallback', resCode, filePath)
        if playFinishCallback:
            playFinishCallback()
        self.normalSoundVolume()

    def downloadPlaySound(self, key, playStartCallback = None, playFinishCallback = None):

        def downloadCallback(key):
            self.playSoundRecord(key, playStartCallback, playFinishCallback)

        self.downloadSoundRecord(key, downloadCallback)

    def addSoundRecordNum(self, chatAdd, friendAdd):
        if not hasattr(self, 'soundRecordNum'):
            self.soundRecordNum = [0, 0]
        if chatAdd:
            self.soundRecordNum[0] += 1
        if friendAdd:
            self.soundRecordNum[1] += 1

    def startChatLogSoundRecord(self, isDown):
        if isDown:
            gameglobal.rds.ui.chat.onStartSoundRecord()
        else:
            gameglobal.rds.ui.chat.onEndSoundRecord()

    def startChatToFriendSoundRecord(self, isDown):
        if isDown:
            if gameglobal.rds.ui.chatToFriend.friendMeds:
                gameglobal.rds.ui.chatToFriend.onStartSoundRecord()
            elif gameglobal.rds.ui.groupChat.widget:
                gameglobal.rds.ui.groupChat.handleStartSoundRecord()
        elif gameglobal.rds.ui.chatToFriend.friendMeds:
            gameglobal.rds.ui.chatToFriend.onEndSoundRecord()
        elif gameglobal.rds.ui.groupChat.widget:
            gameglobal.rds.ui.groupChat.handleEndSoundRecord()

    def reduceSoundVolume(self):
        soundSetting = appSetting.SoundSettingObj
        volume = soundSetting.getVolumeByCategory(gametypes.CATEGORY_MASTER)
        soundSetting.setSoundVolume(volume * 0.1)

    def normalSoundVolume(self):
        soundSetting = appSetting.SoundSettingObj
        volume = soundSetting.getVolumeByCategory(gametypes.CATEGORY_MASTER)
        soundSetting.setSoundVolume(volume)

    def isSoundRecordReviewed(self, key):
        if hasattr(self, 'reviewedSoundRecord'):
            return key in self.reviewedSoundRecord
        return False

    def addReviewedSoundRecord(self, key):
        if not hasattr(self, 'reviewedSoundRecord'):
            self.reviewedSoundRecord = set()
        self.reviewedSoundRecord.add(key)
