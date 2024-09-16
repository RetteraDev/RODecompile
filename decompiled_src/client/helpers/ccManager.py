#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/ccManager.o
import json
import httplib
import time
import hashlib
import urllib
import math
import BigWorld
import appSetting
import const
import gamelog
import gameglobal
import gametypes
from helpers import minicc
from gameclass import Singleton
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
CC_SESSION_STATUS_NONE = 0
CC_SESSION_STATUS_CREATE = 1
CC_SESSION_STATUS_LOGIN = 2

def instance():
    return ccManager.getInstance()


class Session(object):

    def __init__(self, sessionId = 0):
        self.status = CC_SESSION_STATUS_NONE
        self.info = None
        self.sessionId = sessionId

    def isReady(self):
        return self.info and self.status == CC_SESSION_STATUS_CREATE

    def isLogin(self):
        return self.status == CC_SESSION_STATUS_LOGIN


class ccManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.reset()

    def reset(self):
        self.sessions = {}
        self.sessions[const.CC_SESSION_TEAM] = Session(const.CC_SESSION_TEAM)
        self.micCallback = None
        self.outputDebugMsg = True
        self.isStartUp = False

    def handleCCNotify(self, jsonData):
        eType = jsonData['type']
        eResult = jsonData['result']
        if self.outputDebugMsg:
            gamelog.debug('bgf@ccManager handleCCNotify', eType, eResult, jsonData)
        if eType == 'start-mini':
            if eResult == 0:
                self.createSession(const.CC_SESSION_TEAM)
                self.isStartUp = True
            else:
                gamelog.error('bgf@ccManager start-mini failed, result %d' % eResult)
        elif eType == 'connect-change':
            if eResult == -100:
                pass
            elif eResult == -107:
                pass
            elif eResult == -103 or eResult == -104 or eResult == -105 or eResult == -106 or eResult == -109:
                p = BigWorld.player()
                p.base.registerNewCCOfTeam(p.groupNUID)
        elif eType == 'device-change':
            if eResult == -302:
                self.setPlaybackDevice(-1)
            elif eResult == -303:
                self.setCaptureDevice(-1)
        elif eType == 'start-capture':
            sessionId = jsonData['session-id']
            if eResult == 0:
                pass
            else:
                gamelog.error('bgf@ccManager start-capture %d failed, result %d' % (sessionId, eResult))
        elif eType == 'stop-capture':
            sessionId = jsonData['session-id']
            if eResult == 0:
                pass
            else:
                gamelog.error('bgf@ccManager stop-capture %d failed, result %d' % (sessionId, eResult))
        elif eType == 'get-capture-energy':
            if eResult >= 0:
                gameglobal.rds.ui.soundSettingV2.setTestMicData(eResult)
        elif eType == 'create-session':
            if eResult == const.CC_SESSION_TEAM:
                self.sessions[const.CC_SESSION_TEAM].status = CC_SESSION_STATUS_CREATE
                self.setCaptureDevice(-1)
                self.setPlaybackDevice(-1)
                self.muteCapture(1, const.CC_SESSION_TEAM)
                self.mutePlayBack(1, const.CC_SESSION_TEAM)
                self.tryLoginSessionTeam()
        elif eType == 'login-session':
            sessionId = jsonData['session-id']
            if eResult == 0:
                self.sessions[sessionId].status = CC_SESSION_STATUS_LOGIN
            else:
                gamelog.error('bgf@ccManager login-session %d failed, result %d' % (sessionId, eResult))
            if sessionId == const.CC_SESSION_TEAM:
                self.setCaptureVolume(appSetting.SoundSettingObj._value[23])
                self.setPlaybackVolume(appSetting.SoundSettingObj._value[24])
                self.setVoiceMode()
        elif eType == 'logout-session':
            if eResult == 0:
                sessionId = jsonData['session-id']
                self.sessions[sessionId].status = CC_SESSION_STATUS_CREATE

    def createSession(self, sessionId = 0):
        minicc.create_session(sessionId)

    def logoutSession(self, sessionId = 0):
        self.stopCapture(sessionId)
        self.muteCapture(1, const.CC_SESSION_TEAM)
        self.mutePlayBack(0, const.CC_SESSION_TEAM)
        gameglobal.rds.ui.voiceSetting.resetMode()
        minicc.logout_session(sessionId)

    def destroySession(self, sessionId = 0):
        minicc.destory_session(sessionId)

    def getPlaybackDeviceList(self):
        minicc.get_playback_device_list()

    def getCaptuteDeviceList(self):
        minicc.get_capture_device_list()

    def setCaptureDevice(self, deviceId):
        minicc.set_capture_device(deviceId)

    def setPlaybackDevice(self, deviceId):
        minicc.set_playback_device(deviceId)

    def testMic(self, start, sessionId = 0):
        minicc.test_mic(start, sessionId)
        if start:
            self.startMicCallback(sessionId)
        else:
            self.stopMicCallback()

    def getCaptureEnergy(self, sessionId = 0):
        minicc.get_capture_energy(sessionId)

    def setVoiceMode(self):
        mode = appSetting.SoundSettingObj._value[22]
        if mode:
            pass
        else:
            self.startCapture(const.CC_SESSION_TEAM)

    def startUp(self):
        if hasattr(self, 'isStartUp') and self.isStartUp:
            return True
        return False

    def init(self):
        self.reset()
        minicc.init(self.handleCCNotify)

    def release(self):
        self.stopCallback()
        for sessionId in const.CC_SESSION_ALL:
            self.destroySession(sessionId)

        self.reset()
        minicc.reset()

    def getSpeakingList(self, sessionId = 0):
        minicc.get_speaking_list(sessionId)

    def registerTeamInfo(self, info):
        if not hasattr(self, 'sessions'):
            return
        self.sessions[const.CC_SESSION_TEAM].info = info
        self.tryLoginSessionTeam()

    def tryLoginSessionTeam(self):
        p = BigWorld.player()
        if not self.sessions[const.CC_SESSION_TEAM].isReady() and not self.sessions[const.CC_SESSION_TEAM].isLogin() or p.groupType != gametypes.GROUP_TYPE_TEAM_GROUP:
            return
        value = json.dumps(self.sessions[const.CC_SESSION_TEAM].info)
        minicc.login_session(value, const.CC_SESSION_TEAM)

    def stopCallback(self):
        self.stopMicCallback()

    def startMicCallback(self, sessionId = 0):
        self.stopMicCallback()
        self.getCaptureEnergy(sessionId)
        self.micCallback = BigWorld.callback(0.1, Functor(self.startMicCallback, sessionId))

    def stopMicCallback(self):
        if self.micCallback:
            BigWorld.cancelCallback(self.micCallback)
        self.micCallback = None

    def muteCapture(self, mute, sessionId = 0):
        minicc.mute_capture(mute, sessionId)

    def mutePlayBack(self, mute, sessionId = 0):
        minicc.mute_playback(mute, sessionId)

    def startCapture(self, sessionId = 0):
        if self.sessions[sessionId].isLogin():
            minicc.start_capture(sessionId)

    def stopCapture(self, sessionId = 0):
        if self.sessions[sessionId].isLogin():
            minicc.stop_capture(sessionId)

    def setCaptureVolume(self, vol):
        if not minicc.mini_cc:
            return
        if vol >= 0:
            minicc.set_capture_volume(int(math.ceil(vol * 2.55)))

    def setPlaybackVolume(self, vol):
        if not minicc.mini_cc:
            return
        if vol >= 0:
            minicc.set_playback_volume(int(math.ceil(vol * 2.55)))

    def enablePitch(self, enable, origin, target, adjustment = 0):
        minicc.enable_pitch(enable, origin, target, adjustment)
