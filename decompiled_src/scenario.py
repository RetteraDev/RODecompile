#Embedded file name: /WORKSPACE/data/entities/client/helpers/scenario.o
import time
import math
import Sound
import BigWorld
import ResMgr
import Math
import C_ui
import GUI
import gametypes
import gamelog
import const
import gameglobal
import clientcom
import keys
import appSetting
import clientUtils
from sfx import sfx
from sfx import screenRipple
from sfx import cameraEffect
from sfx import screenEffect
from sfx import physicsEffect
from callbackHelper import Functor
from guis import ui
from guis import events
from helpers import cameraControl as CC
from helpers import charRes
from helpers.black import fade
from helpers.black import fadein
from helpers.black import fadeout
from helpers import tintalt
from helpers import outlineHelper
from helpers import cgPlayer
from helpers import modelServer
from helpers import attachedModel
from appSetting import SoundSettingObj as soundSetting, Obj as AppSettings
import utils
from data import npc_model_client_data as NCD
PATH_NAME = 'gui/intro/'
CONST_FLOAT = -1000
gModelPool = {}
gfxHandle = []
gVoiceHandle = []
disableMusicFlag = False
disableSound = [False,
 False,
 False,
 False]
gChangeColorGrading = False
gCanEsc = False
gLockKey = True
avatarNpc = 10615
FADE_IN_TIME = 0.2
FADE_TIME = 1.0
FADE_OUT_TIME = 0.2
SCENARIO_TEXTURE_LIMIT = 200
FILM_EFFECT_BLACK = 0
FILM_EFFECT_MASK = 1
FILM_EFFECT_NONE = 2
FILM_EFFECT_MONOSPACE_MASK = 3
ANCHOR_CONFIG = (('TOP',
  1.0,
  PATH_NAME + 'top.dds',
  2.0 / 13), ('BOTTOM',
  -1.0,
  PATH_NAME + 'bottom.dds',
  4.0 / 13))
MONOSPACE_ANCHOR_CONFIG = (('TOP',
  1.0,
  PATH_NAME + 'newScreenMask.dds',
  2.0 * 0.07), ('BOTTOM',
  -1.0,
  PATH_NAME + 'newScreenMask.dds',
  2.0 * 0.07))

def initSoundFlag():
    global disableSound
    disableSound = [False,
     False,
     False,
     False]


def switchSound(data):
    soundCheckFunc = [soundSetting.isMusicEnable,
     soundSetting.isFxEnable,
     soundSetting.isStaticEnable,
     soundSetting.isAmbientEnable]
    soundFunc = [Sound.enableMusic,
     None,
     Sound.enableStatic,
     Sound.enableAmbient]
    for i, item in enumerate(data):
        if soundCheckFunc[i]():
            if soundFunc[i]:
                soundFunc[i](item)
                disableSound[i] = True
            else:
                disableSound[i] = not item


def restoreSound():
    soundFunc = [Sound.enableMusic,
     None,
     Sound.enableStatic,
     Sound.enableAmbient]
    for i, flag in enumerate(disableSound):
        if flag:
            if soundFunc[i]:
                soundFunc[i](True)


def scenarioIsForbidFx():
    ins = Scenario.INSTANCE
    if Scenario.PLAY_INSTANCE:
        ins = Scenario.PLAY_INSTANCE
    if ins and gameglobal.SCENARIO_PLAYING and disableSound[1]:
        return True
    return False


def stopFx():
    global gfxHandle
    for handle in gfxHandle:
        if isinstance(handle, tuple):
            BigWorld.callback(handle[1], Functor(Sound.stopFx, handle[0]))
        else:
            BigWorld.callback(1.0, Functor(Sound.stopFx, handle))

    gfxHandle = []


def stopVoice():
    global gVoiceHandle
    for handle in gVoiceHandle:
        if isinstance(handle, tuple):
            BigWorld.callback(handle[1], Functor(Sound.stopRawfile, handle[0]))
        else:
            BigWorld.callback(5.0, Functor(Sound.stopRawfile, handle))

    gVoiceHandle = []


class ModelCameraCounter(object):

    def __init__(self):
        self.counter = 0
        self.model = None
        self.modelPath = None
        self.actions = []

    def reset(self):
        self.counter = 0
        if self.model:
            if self.model.inWorld:
                BigWorld.player().delModel(self.model)
            self.model = None
        self.modelPath = None
        self.actions = []

    def register(self):
        self.counter += 1

    def callback(self, actionName):
        self.counter -= 1
        if self.counter == 0:
            CC.endCamera()

    def reloadModel(self, threadID, cbFunc):
        if self.model:
            self.afterResFinish(cbFunc, self.model)
            return
        if self.modelPath:
            clientUtils.fetchModel(threadID, Functor(self.afterResFinish, cbFunc), self.modelPath)

    def afterResFinish(self, cbFunc, model):
        if not model:
            return
        self.model = model
        if not self.model.inWorld:
            BigWorld.player().addModel(self.model)
        if hasattr(self.model, 'loadActionNow'):
            for act in self.actions:
                model.loadActionNow(act)

        self.model.expandVisibilityBox(1000)
        if cbFunc:
            cbFunc()


gCameraCounter = ModelCameraCounter()

class Scenario(object):
    NAME = 'name'
    TIME = 'time'
    PREFIX_PATH_NAME = 'intro/scenario/'
    INSTANCE = None
    PLAY_INSTANCE = None

    @staticmethod
    def getInstance():
        if Scenario.INSTANCE is None:
            Scenario.INSTANCE = Scenario(True)
        return Scenario.INSTANCE

    @staticmethod
    def getInstanceInPlay():
        if Scenario.PLAY_INSTANCE is None:
            Scenario.PLAY_INSTANCE = Scenario(False)
        return Scenario.PLAY_INSTANCE

    def __init__(self, editMode = False):
        self.name = ''
        self.actorDict = {}
        self.eventMgr = EventMgr()
        self.needPlay = False
        self.playParam = {}
        self.editMode = editMode
        self.syncID = 0
        self.rootSect = None
        self._cameraReady = False
        self._loadingDist = 0
        self.usePlayerCamera = 0
        self.originFov = None
        self.originNearPlane = None
        self.hideNPC = 0
        self.hideMovingPlat = 0
        self.hideTreasureBox = 0
        self.hideAvatar = 0
        self.hideAvatarExcepTeam = 0
        self.hideEntityTopLogo = 0
        self.hideTransport = 0
        self.hidePlayer = 0
        self.musicRatio = 1.0
        self.hideMonster = 0
        self.setModelNeedHide = 0
        self.oldBgMusicVolume = Sound.getMusicVolume()
        self.hideNPCLog = []
        self.hideTransportLog = []
        self.musicTimer = None
        self.canEsc = 0
        self.canGroupEsc = 0
        self.canGroupSingleEsc = 0
        self.passFade = 0
        self.shadowDist = 0
        self.yaw = CONST_FLOAT
        self.pitch = CONST_FLOAT
        self.cameraMove = []
        self.enableLODAll = 0
        self.fps = 0
        self.beginStamp = 0
        self.finishCallback = None
        self.finishCallbackFor = None
        self.confirmStopMsgBoxId = None
        self.preLoadEff = []
        self.preLoadModel = []
        self.hideNpcIds = []
        self.preLoadModelSec = None
        self.hideTopLogo = 0
        self.isTopLogoHidden = False
        self.isOtherTopLogoHidden = False
        self.scenarioId = 0
        self.copyForActor = []
        self.notHideEnt = []

    def getActor(self, npcName):
        return self.actorDict.get(npcName, None)

    def useCursorCamera(self, usePlayerCamera):
        self.usePlayerCamera = usePlayerCamera

    def setHideNPC(self, isTrue):
        self.hideNPC = isTrue

    def setHideMovingPlat(self, isTrue):
        self.hideMovingPlat = isTrue

    def setHideAvatar(self, isTrue):
        self.hideAvatar = isTrue

    def setYawAndPictch(self, yaw, pitch):
        self.yaw = yaw
        self.pitch = pitch

    def setHidePlayer(self, isTrue):
        self.hidePlayer = isTrue

    def setHideMonster(self, isTrue):
        self.hideMonster = isTrue

    def setCanEsc(self, isTrue):
        self.canEsc = isTrue

    def setPassFade(self, isTrue):
        self.passFade = isTrue

    def setHideTreasureBox(self, isTrue):
        self.hideTreasureBox = isTrue

    def setHideAvatarExcludeTeam(self, isTrue):
        self.hideAvatarExcepTeam = isTrue

    def setHideEntityTopLogo(self, isTrue):
        self.hideEntityTopLogo = isTrue

    def setHideTransport(self, isTrue):
        self.hideTransport = isTrue

    def setMusicRatio(self, ratio):
        self.musicRatio = ratio

    def adjustMusicVolume(self, fromVolume, toVolume):
        if self.musicRatio >= 0 and self.musicRatio < 1.0 and soundSetting.isMusicEnable():
            if self.musicTimer:
                BigWorld.cancelCallback(self.musicTimer)
                self.musicTimer = None
            step = (toVolume - fromVolume) / 20.0
            num = 1
            self._adjustMusicVolume(fromVolume, step, toVolume, num)

    def _adjustMusicVolume(self, fromVolume, step, toVolume, num):
        if num == 20:
            Sound.setMusicVolume(toVolume)
            return
        Sound.setMusicVolume(fromVolume + step * num)
        self.musicTimer = BigWorld.callback(0.1, Functor(self._adjustMusicVolume, fromVolume, step, toVolume, num + 1))

    def release(self, byStop = False):
        global gModelPool
        p = BigWorld.player()
        if self.editMode is False:
            if p:
                p.unlockKey(gameglobal.KEY_POS_SCENARIO)
                p.updateActionKeyState()
                p.cell.setInScriptFlag(False, 0)
                p.cell.setRealInScriptFlag(False)
                p.inFuben() and p.cell.judgeSciptFlag()
            if not self.usePlayerCamera:
                gameglobal.rds.ui.restoreUI()
        if gameglobal.SCENARIO_PLAYING:
            gameglobal.setLoadingDist(self._loadingDist)
        if hasattr(gameglobal, 'noviceScenarioName'):
            if self.name == Scenario.PREFIX_PATH_NAME + gameglobal.noviceScenarioName:
                gameglobal.rds.ui.newGuiderOpera.show()
        gameglobal.SCENARIO_PLAYING = gameglobal.SCENARIO_END
        if BigWorld.isWow64():
            appSetting.VideoQualitySettingObj.setTextureLODSizeLimit()
        self._setPlayedGroupScripts()
        self.clear()
        self._clearPreLoadModels()
        self.adjustMusicVolume(self.oldBgMusicVolume * self.musicRatio, self.oldBgMusicVolume)
        if self.hideNPC:
            self.restoreRealNPC()
        if self.hideMovingPlat:
            self.refreshMovingPlatform()
        if self.yaw != CONST_FLOAT:
            player = BigWorld.player()
            player.ap.setYawAndCamera(self.yaw)
            self.yaw = CONST_FLOAT
        if self.pitch != CONST_FLOAT:
            BigWorld.dcursor().pitch = self.pitch
            self.pitch = CONST_FLOAT
        if self.cameraMove:
            self.moveCamera()
        if self.hideEntityTopLogo:
            self.hideEntityTopLogoFunc(False)
        if self.hideTransport:
            self.restoreTransportFunc()
        if self.hideTreasureBox:
            self.restoreTreasureBoxNearby()
        if self.hideAvatar and not self.usePlayerCamera:
            if p:
                p.restorePlayerNearby()
            else:
                gameglobal.gHideOtherPlayerFlag = gameglobal.HIDE_NOBODY
        if self.shadowDist:
            value = appSetting.VideoQualitySettingObj.getShadowDist()
            self._setShadowValue(value)
        if self.hidePlayer and not self.usePlayerCamera:
            p.hide(False) if p else None
        if self.fps:
            clientcom.resetLimitFps()
        if self.hideMonster and not self.usePlayerCamera:
            if p:
                p.restoreMonsterNearby()
            else:
                gameglobal.gHideMonsterFlag = gameglobal.HIDE_NO_MONSTER
        if self.hideTopLogo:
            if p:
                if not self.isTopLogoHidden:
                    if hasattr(p, 'topLogo'):
                        p.topLogo.hide(False)
                if not self.isOtherTopLogoHidden:
                    for _gbId, mVal in p.members.iteritems():
                        if not mVal['isOn']:
                            continue
                        if mVal['id'] != p.id:
                            other = BigWorld.entities.get(mVal['id'])
                            if other and hasattr(other, 'topLogo'):
                                other.topLogo.hide(False)

        restoreSound()
        self._restoreProjection()
        for item in gModelPool.keys():
            gModelPool[item] = None
            del gModelPool[item]

        stopFx()
        stopVoice()
        if hasattr(BigWorld, 'forceUpdateZoneParams'):
            BigWorld.forceUpdateZoneParams()
        self._restoreColorGrading()
        gCameraCounter.reset()
        if not BigWorld.isCharLod():
            BigWorld.enableCharLod(True)
        BigWorld.enableSkipSkeletonUpdate(True)
        BigWorld.enableMultiThreadAnim(True)
        if hasattr(BigWorld, 'setCameraAnimModel'):
            BigWorld.setCameraAnimModel(None)
        if hasattr(BigWorld, 'drawAllSmallFlora'):
            BigWorld.drawAllSmallFlora(False)
        if self.enableLODAll:
            self.setEnableLODAll(False)
        if self.finishCallback:
            if not byStop:
                self.finishCallback()
            self.finishCallback = None
            self.finishCallbackFor = None
            if self.confirmStopMsgBoxId:
                gameglobal.rds.ui.messageBox.dismiss(self.confirmStopMsgBoxId)
                self.confirmStopMsgBoxId = None
        p.showSysCacheMsg()
        gameglobal.rds.ui.skillPush.showCacheNewSkill()
        ui.clearScenarioFuncCache()
        if not BigWorld.worldDrawEnabled():
            BigWorld.worldDrawEnabled(True)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_TYPE_SCENARIO_END)
        self.copyForActor = []
        self.notHideEnt = []

    def _clearPreLoadModels(self):
        p = BigWorld.player()
        for model in self.preLoadModel:
            if model and model.inWorld:
                try:
                    p.delModel(model)
                except:
                    pass

        self.preLoadModel = []

    def _restoreProjection(self):
        if self.originFov:
            BigWorld.projection().fov = self.originFov
            self.originFov = None
        if self.originNearPlane:
            BigWorld.projection().nearPlane = self.originNearPlane
            self.originNearPlane = None

    def _restoreColorGrading(self):
        global gChangeColorGrading
        if gChangeColorGrading:
            BigWorld.setColorGrading('', 1)
            gChangeColorGrading = False

    def _setProjection(self):
        self.originFov = BigWorld.projection().fov
        self.originNearPlane = BigWorld.projection().nearPlane

    def clear(self):
        BigWorld.player().clientControl = True
        BigWorld.player().updateActionKeyState()
        for a in self.actorDict.itervalues():
            a.release()

        self.actorDict.clear()
        self.eventMgr.release()
        self.rootSect = None
        ResMgr.purge(self.name)
        self.name = None
        self.resetState()
        self.syncID += 1

    def resetState(self):
        self.needPlay = False
        self.playParam = {}

    def reset(self):
        BigWorld.player().unlockKey(gameglobal.KEY_POS_SCENARIO)
        if not self.usePlayerCamera:
            gameglobal.rds.ui.restoreUI()
        for actor in self.actorDict.itervalues():
            actor.reset(True)

        self.eventMgr.reset()
        self.resetState()
        if gameglobal.SCENARIO_PLAYING:
            gameglobal.setLoadingDist(self._loadingDist)
            gameglobal.SCENARIO_PLAYING = gameglobal.SCENARIO_END
        p = BigWorld.player()
        if self.hideNPC:
            self.restoreRealNPC()
        if self.hideMovingPlat:
            self.refreshMovingPlatform()
        if self.hideTreasureBox:
            self.restoreTreasureBoxNearby()
        if self.yaw != CONST_FLOAT:
            player = BigWorld.player()
            player.ap.setYawAndCamera(self.yaw)
            self.yaw = CONST_FLOAT
        if self.pitch != CONST_FLOAT:
            BigWorld.dcursor().pitch = self.pitch
            self.pitch = CONST_FLOAT
        if self.cameraMove:
            self.moveCamera()
        if self.hideEntityTopLogo:
            self.hideEntityTopLogoFunc(False)
        if self.hideTransport:
            self.restoreTransportFunc()
        self.adjustMusicVolume(self.oldBgMusicVolume * self.musicRatio, self.oldBgMusicVolume)
        if self.hideAvatar and not self.usePlayerCamera:
            p.restorePlayerNearby()
        if self.shadowDist:
            value = appSetting.VideoQualitySettingObj.getShadowDist()
            self._setShadowValue(value)
        if self.hidePlayer and not self.usePlayerCamera:
            p.hide(False)
        if self.fps:
            clientcom.resetLimitFps()
        if self.hideMonster and not self.usePlayerCamera:
            p.restoreMonsterNearby()
        if self.hideTopLogo:
            if p:
                if not self.isTopLogoHidden:
                    if hasattr(p, 'topLogo'):
                        p.topLogo.hide(False)
                if not self.isOtherTopLogoHidden:
                    for _gbId, mVal in p.members.iteritems():
                        if not mVal['isOn']:
                            continue
                        if mVal['id'] != p.id:
                            other = BigWorld.entities.get(mVal['id'])
                            if other and hasattr(other, 'topLogo'):
                                other.topLogo.hide(False)

        restoreSound()
        self._restoreProjection()
        for item in gModelPool.keys():
            gModelPool[item] = None
            del gModelPool[item]

        stopFx()
        stopVoice()
        self._restoreColorGrading()
        gCameraCounter.reset()
        if not BigWorld.isCharLod():
            BigWorld.enableCharLod(True)
        BigWorld.enableSkipSkeletonUpdate(True)
        if hasattr(BigWorld, 'drawAllSmallFlora'):
            BigWorld.drawAllSmallFlora(False)
        if self.enableLODAll:
            self.setEnableLODAll(False)
        self.copyForActor = []
        self.notHideEnt = []

    def stopPlay(self):
        gamelog.debug('Scenario@stopPlay')
        fadeout()
        self.eventMgr.stopPlay()
        if not self.editMode:
            self.release(True)
        else:
            self.reset()

    def continuePlay(self, isEnd, success):
        self.eventMgr.continuePlay(isEnd, success)
        for actor in self.actorDict.values():
            actor.stopCueSound()

    def pausePlayInEvent(self):
        self.eventMgr.pausePlayInEvent()

    def _canGroupEsc(self):
        if not self.canGroupEsc:
            return False
        player = BigWorld.player()
        if not player:
            return False
        if player.playedFubenAniScripts:
            playedScripts = player.playedFubenAniScripts.split('#')
        else:
            playedScripts = AppSettings.get(keys.SET_PLAYED_SCRIPTS, '').split('#')
        name = self.name[len('intro/scenario/'):-len('.xml')]
        if name in playedScripts:
            return True
        return False

    def _canGroupSingleEsc(self):
        if not self.canGroupSingleEsc:
            return False
        return True

    def _setPlayedGroupScripts(self):
        if not self.canGroupEsc:
            return
        player = BigWorld.player()
        if not player:
            return
        if player.playedFubenAniScripts:
            playedScripts = player.playedFubenAniScripts.split('#')
        else:
            playedScripts = AppSettings.get(keys.SET_PLAYED_SCRIPTS, '').split('#')
            if AppSettings.get(keys.SET_PLAYED_SCRIPTS, ''):
                player.cell.setPlayedScriptNames(AppSettings.get(keys.SET_PLAYED_SCRIPTS, ''))
        try:
            name = self.name[len('intro/scenario/'):-len('.xml')]
            if name in playedScripts:
                return
            player.cell.setPlayedScriptNames(name)
        except:
            gamelog.error('@PGF:_setPlayedGroupScripts set appsettings error!!', self.name)

    def loadScript(self, oldName, mustExist = False):
        gamelog.debug('scenario@loadScript', time.time(), oldName)
        name = Scenario.PREFIX_PATH_NAME + oldName
        if self.name == name:
            return False
        if gameglobal.SCENARIO_PLAYING:
            self.stopPlay()
        startTime = time.clock()
        sect = ResMgr.openSection(name)
        if sect is None:
            if mustExist:
                if BigWorld.isPublishedVersion():
                    name = '../game/avatar/' + oldName
                    sect = ResMgr.openSection(name)
                    if not sect:
                        sect = ResMgr.root.createSection(name)
                        sect.save()
                else:
                    sect = ResMgr.root.createSection(name)
                    sect.save()
            else:
                return False
        self.clear()
        self.name = name
        self.rootSect = sect
        self.eventMgr.lifetime = sect.readFloat('lifetime')
        self.usePlayerCamera = sect.readInt('usePlayerCamera', 0)
        self.hideNPC = sect.readInt('hideNPC', 0)
        self.hideMovingPlat = sect.readInt('hideMovingPlat', 0)
        self.hideTreasureBox = sect.readInt('hideTreasureBox', 0)
        self.hideAvatar = sect.readInt('hideAvatar', 0)
        self.hideAvatarExcepTeam = sect.readInt('hideAvatarExcepTeam', 0)
        self.hideEntityTopLogo = sect.readInt('hideEntityTopLogo', 0)
        self.hideTransport = sect.readInt('hideTransport', 0)
        self.hidePlayer = sect.readInt('hidePlayer', 0)
        self.fps = sect.readInt('fps', 0)
        self.musicRatio = sect.readFloat('musicRatio', 1.0)
        self.hideMonster = sect.readFloat('hideMonster', 0)
        self.canEsc = sect.readInt('canEsc', 0)
        self.canGroupEsc = sect.readInt('canGroupEsc', 0)
        self.canGroupSingleEsc = sect.readInt('canGroupSingleEsc', 0)
        self.passFade = sect.readInt('passFade', 0)
        self.shadowDist = sect.readInt('shadowDist', 0)
        self.yaw = sect.readFloat('yaw', CONST_FLOAT)
        self.pitch = sect.readFloat('pitch', CONST_FLOAT)
        self.hideTopLogo = sect.readInt('hideTopLogo', 0)
        cameraMove = sect.readString('cameraMove', '')
        if cameraMove:
            dist, duration = cameraMove.split(',')
            self.cameraMove = [float(dist), float(duration)]
        self.setModelNeedHide = sect.readInt('setModelNeedHide', 0)
        self.enableLODAll = sect.readInt('enableLODAll', 0)
        actorsSect = sect.openSection('Actors')
        if actorsSect:
            for aSect in actorsSect.values():
                actor = Actor()
                actor.usePlayerCamera = self.usePlayerCamera
                actor.editMode = self.editMode
                actor.load(aSect)
                self.actorDict[aSect.name] = actor

        eventSect = sect.openSection('Event')
        if eventSect:
            self.eventMgr.load(eventSect)
        self.scanActorActions()
        self.preLoadEff = sect.readString('preloadEffs')
        if self.preLoadEff:
            effs = self.preLoadEff.split(',')
            for fxId in effs:
                if fxId.isdigit():
                    sfx.gEffectMgr.preloadFx(int(fxId), gameglobal.EFFECT_HIGH)

        self.preLoadModelSec = sect.openSection('preLoadModels')
        gamelog.debug('@szh : load Section takes', time.clock() - startTime, name)
        return True

    def scanActorActions(self):
        for event in self.eventMgr.eventList:
            actorEvent = event.actorEvent
            for actorName, actions in actorEvent.iteritems():
                for action in actions:
                    if action[0] == 'act':
                        actor = self.actorDict.get(actorName, None)
                        if actor:
                            actor.preLoadActs.append(action[1])

    def saveScript(self):
        if len(self.name) == 0:
            return False
        self.rootSect.deleteSection('lifetime')
        self.rootSect.writeString('lifetime', '%.1f' % self.eventMgr.lifetime)
        self.rootSect.writeInt('usePlayerCamera', self.usePlayerCamera)
        gamelog.debug('hideNPC, hideAvatar', self.hideNPC, self.hideAvatar)
        self.rootSect.writeInt('hideNPC', self.hideNPC)
        self.rootSect.writeInt('hideMovingPlat', self.hideMovingPlat)
        self.rootSect.writeInt('hideTreasureBox', self.hideTreasureBox)
        self.rootSect.writeInt('hideAvatar', self.hideAvatar)
        self.rootSect.writeInt('hideAvatarExcepTeam', self.hideAvatarExcepTeam)
        self.rootSect.writeInt('hideEntityTopLogo', self.hideEntityTopLogo)
        self.rootSect.writeInt('hideTransport', self.hideTransport)
        self.rootSect.writeInt('hidePlayer', self.hidePlayer)
        self.rootSect.writeInt('fps', self.fps)
        self.rootSect.writeFloat('musicRatio', self.musicRatio)
        self.rootSect.writeInt('hideMonster', self.hideMonster)
        self.rootSect.writeInt('canEsc', self.canEsc)
        self.rootSect.writeInt('setModelNeedHide', self.setModelNeedHide)
        self.rootSect.writeString('preloadEffs', self.preLoadEff)
        self.rootSect.writeInt('passFade', self.passFade)
        self.rootSect.writeInt('shadowDist', self.shadowDist)
        self.rootSect.writeString('yaw', '%.2f' % self.yaw)
        self.rootSect.writeString('pitch', '%.2f' % self.pitch)
        if self.cameraMove:
            self.rootSect.writeString('cameraMove', '%.2f,%.2f' % tuple(self.cameraMove))
        self.rootSect.writeInt('enableLODAll', self.enableLODAll)
        self.sweep()
        self.rootSect.deleteSection('Actors')
        actorsSect = self.rootSect.createSection('Actors')
        for actor in self.actorDict.itervalues():
            actor.save(actorsSect)

        if len(actorsSect.keys()) == 0:
            self.rootSect.deleteSection('Actors')
        self.rootSect.deleteSection('Event')
        eventSect = self.rootSect.createSection('Event')
        self.eventMgr.save(eventSect)
        self.rootSect.save()
        return True

    def sweep(self):
        actors = self.actorDict.keys()
        trivialEventList = []
        for event in self.eventMgr.eventList:
            if event.isEmpty():
                trivialEventList.append(event)
                continue
            for name in event.actorEvent.keys():
                if name in actors:
                    actors.remove(name)

        for event in trivialEventList:
            self.eventMgr.eventList.remove(event)

        for name in actors:
            actor = self.actorDict[name]
            del self.actorDict[name]
            actor.release()

    def refreshMovingPlatform(self):
        ent = BigWorld.entities.values()
        for e in ent:
            name = e.__class__.__name__
            if name == 'MovingPlatform':
                e.refreshOpacityState()

    def moveCamera(self):
        if self.cameraMove:
            dist, duration = self.cameraMove
            c = BigWorld.camera()
            if hasattr(c, 'cameraDHProvider') and c.cameraDHProvider:
                value = c.cameraDHProvider.value
                keyFrames = []
                keyFrames.append((0.0, (value[0],
                  value[1],
                  0,
                  value[3] - dist)))
                keyFrames.append((duration, (value[0],
                  value[1],
                  value[2],
                  value[3])))
                v4 = Math.Vector4Animation()
                v4.oneshot = True
                v4.duration = keyFrames[-1][0]
                v4.keyframes = keyFrames
                maxDistHalfLife = c.maxDistHalfLife
                c.maxDistHalfLife = 0
                c.cameraDHProvider = v4
                BigWorld.callback(0.05, Functor(self._resetMaxDistHalfLife, maxDistHalfLife))
            self.cameraMove = []

    def _resetMaxDistHalfLife(self, maxDistHalfLife):
        c = BigWorld.camera()
        if hasattr(c, 'maxDistHalfLife'):
            c.maxDistHalfLife = maxDistHalfLife

    def hideEntityTopLogoFunc(self, isHide):
        ent = BigWorld.entities.items()
        actorIds = [ getattr(actor, 'id', None) for actor in self.actorDict.values() ]
        for eid, e in ent:
            if eid in actorIds:
                continue
            if getattr(e, 'topLogo', None) and hasattr(e, 'beHide') and not e.beHide:
                if e == self:
                    e.topLogo.hide(isHide)
                elif e.__class__.__name__ == 'Avatar':
                    if isHide:
                        e.topLogo.hide(isHide)
                    else:
                        e.refreshOpacityState()
                elif e.__class__.__name__ in ('Dawdler',) or e.IsMonster:
                    if not (e.IsMonster and not isHide and getattr(e, 'life', 0) == gametypes.LIFE_DEAD):
                        e.topLogo.hide(isHide)
                elif e.__class__.__name__ in ('Npc', 'MovableNpc') and getattr(e, 'isScenario', None) == gameglobal.NORMAL_NPC:
                    e.topLogo.hide(isHide)

    def hideTransportFunc(self):
        self.hideTransportLog = []
        ent = BigWorld.entities.items()
        for eid, e in ent:
            name = e.__class__.__name__
            if name == 'Transport':
                e.hide(True)
                self.hideTransportLog.append(eid)

    def restoreTransportFunc(self):
        gamelog.debug('restoreRealNPC', self.hideNPCLog)
        while self.hideTransportLog:
            eid = self.hideTransportLog.pop(0)
            transport = BigWorld.entity(eid)
            if transport and transport.inWorld:
                transport.hide(False)

        self.hideTransportLog = []

    def hideRealNPC(self):
        self.hideNpcIds = [ actor.npcId for actor in self.actorDict.values() ]
        self.hideNPCLog = []
        ent = BigWorld.entities.items()
        for eid, e in ent:
            name = e.__class__.__name__
            if hasattr(e, 'npcId') and e.npcId in self.hideNpcIds:
                if name.find('Npc') != -1:
                    e.hideByScenario(const.VISIBILITY_HIDE)
                    self.hideNPCLog.append(eid)
                elif name == 'Dawdler' and e.model.visible:
                    e.hide(True)
                    self.hideNPCLog.append(eid)
            elif hasattr(e, 'questBoxType') and e.questBoxType in self.hideNpcIds:
                e.hide(True)
                self.hideNPCLog.append(eid)
            elif hasattr(e, 'treasureBoxId'):
                e.hide(True)
                self.hideNPCLog.append(eid)

    def restoreRealNPC(self):
        gamelog.debug('restoreRealNPC', self.hideNPCLog)
        while self.hideNPCLog:
            eid = self.hideNPCLog.pop(0)
            npc = BigWorld.entity(eid)
            name = npc.__class__.__name__
            if npc and npc.inWorld:
                if name.find('Npc') != -1:
                    npc.hideByScenario(const.VISIBILITY_SHOW)
                elif name == 'Dawdler' and not npc.model.visible:
                    npc.hide(False)
                elif name in ('QuestBox', 'TreasureBox'):
                    npc.refreshOpacityState()

        self.hideNpcIds = []
        self.hideNPCLog = []

    def hideTreasureBoxNearby(self):
        ents = BigWorld.entities.values()
        for ent in ents:
            if hasattr(ent, 'treasureBoxId'):
                ent.hide(True)

    def restoreTreasureBoxNearby(self):
        ents = BigWorld.entities.values()
        for ent in ents:
            if hasattr(ent, 'treasureBoxId'):
                ent.refreshOpacityState()

    def setEnableLODAll(self, value):
        if hasattr(BigWorld, 'enableLODAll'):
            BigWorld.enableLODAll(value)

    def play(self, name = None, stamp = 0, finishCallback = None, finishCallbackFor = None, copyForActor = None, notHideEnt = []):
        gamelog.debug('scenario@play', time.time(), name, stamp)
        self.finishCallback = finishCallback
        self.finishCallbackFor = finishCallbackFor
        if copyForActor:
            self.copyForActor = copyForActor
        if notHideEnt:
            self.notHideEnt = notHideEnt
        if self.usePlayerCamera:
            gameglobal.SCENARIO_PLAYING = gameglobal.SCENARIO_PLAYING_CURSOR_CAMERA
        else:
            gameglobal.SCENARIO_PLAYING = gameglobal.SCENARIO_PLAYING_TRACK_CAMERA
            gameglobal.rds.cam.restoreCameraFov(0)
            BigWorld.enableCharLod(False)
            BigWorld.enableSkipSkeletonUpdate(False)
            if hasattr(BigWorld, 'drawAllSmallFlora'):
                BigWorld.drawAllSmallFlora(True)
            if self.enableLODAll:
                self.setEnableLODAll(True)
        if not self.usePlayerCamera:
            if BigWorld.isWow64():
                BigWorld.textureLODSizeLimit('char', SCENARIO_TEXTURE_LIMIT)
            if gameglobal.rds.ui.map.isShow:
                gameglobal.rds.ui.map.realClose()
            if gameglobal.rds.ui.quest.isShow:
                gameglobal.rds.ui.quest.close()
            if gameglobal.rds.ui.npcV2.isShow:
                gameglobal.rds.ui.npcV2.leaveStage()
            if gameglobal.rds.ui.autoQuest.isShow():
                gameglobal.rds.ui.autoQuest.hide()
            gameglobal.rds.ui.hideAllUI()
            p = BigWorld.player()
            p.ap.stopMove()
            p.ap.forceAllKeysUp()
            if self.canGroupSingleEsc:
                p.cell.setInScriptFlag(True, self.eventMgr.lifetime)
            else:
                p.cell.setInScriptFlag(False, self.eventMgr.lifetime)
            p.cell.setRealInScriptFlag(True)
            if gLockKey:
                p.lockKey(gameglobal.KEY_POS_SCENARIO)
            if self.passFade:
                self.startPlay(name, stamp)
            else:
                fadein(FADE_IN_TIME, callback=Functor(self.startPlay, name, stamp))
        else:
            self.startPlay(name, stamp)

    def startPlay(self, name, stamp):
        global gVoiceHandle
        global gModelPool
        global gCanEsc
        global gfxHandle
        self.playParam = {self.NAME: name,
         self.TIME: stamp,
         'playTime': time.time()}
        self._loadingDist = gameglobal.MAX_LOADING_DIST
        gameglobal.setLoadingDist(200)
        for actor in self.actorDict.itervalues():
            actor.reset(False)

        self.eventMgr.reset()
        p = BigWorld.player()
        if p.targetLocked:
            p.unlockTarget()
        if self.hideNPC:
            self.hideRealNPC()
        if self.hideMovingPlat:
            self.refreshMovingPlatform()
        if self.hideTreasureBox:
            self.hideTreasureBoxNearby()
        if self.hideAvatar and not self.usePlayerCamera:
            beHide = gameglobal.HIDE_ALL_PLAYER_AND_ATTACK
            if self.hideAvatarExcepTeam:
                beHide = gameglobal.HIDE_NOT_TEAMER_WITHOUT_ENEMY
            p.hidePlayerNearby(beHide)
        if self.shadowDist:
            self._setShadowValue(self.shadowDist)
        if self.hideEntityTopLogo:
            self.hideEntityTopLogoFunc(True)
        if self.hideTransport:
            self.hideTransportFunc()
        self.adjustMusicVolume(self.oldBgMusicVolume, self.oldBgMusicVolume * self.musicRatio)
        if self.hidePlayer and not self.usePlayerCamera:
            p.hide(True)
        if self.fps:
            BigWorld.limitForegroundFPS(self.fps)
        if self.hideMonster and not self.usePlayerCamera:
            p.hideMonsterNearby(gameglobal.HIDE_ALL_MONSTER)
        if not self.usePlayerCamera:
            outlineHelper.setTarget(None)
            gameglobal.rds.sound.stopDelayPlay()
        if self.hideTopLogo:
            if p:
                if hasattr(p, 'topLogo'):
                    if p.topLogo != utils.MyNone and p.topLogo.gui.visible:
                        self.isTopLogoHidden = False
                        p.topLogo.hide(True)
                    else:
                        self.isTopLogoHidden = True
                for _gbId, mVal in p.members.iteritems():
                    if not mVal['isOn']:
                        continue
                    if mVal['id'] != p.id:
                        other = BigWorld.entities.get(mVal['id'])
                        if other and hasattr(other, 'topLogo'):
                            if other.topLogo != utils.MyNone and other.topLogo.gui.visible:
                                self.isOtherTopLogoHidden = False
                                other.topLogo.hide(True)
                            else:
                                self.isOtherTopLogoHidden = True
                            break

        for ent in self.notHideEnt:
            ent.hide(False)
            ent.refreshOpacityState()
            ent.refreshTopLogo()
            ent.refreshToplogoTitle()

        initSoundFlag()
        gCanEsc = self.canEsc
        self._setProjection()
        gModelPool = {}
        gfxHandle = []
        gVoiceHandle = []
        self.preLoadRes()

    def _setShadowValue(self, value):
        if value:
            BigWorld.setDynamicShadowDist(value)

    def _cycleCheck(self):
        if gameglobal.rds.ui.map.isShow:
            gameglobal.rds.ui.map.realClose()
        if gameglobal.rds.ui.quest.isShow:
            gameglobal.rds.ui.quest.close()
        if gameglobal.rds.ui.npcV2.isShow:
            gameglobal.rds.ui.npcV2.leaveStage()
        if gameglobal.rds.ui.autoQuest.isShow():
            gameglobal.rds.ui.autoQuest.hide()
        if gLockKey:
            BigWorld.player().lockKey(gameglobal.KEY_POS_SCENARIO)
        gameglobal.rds.ui.hideAllUI()
        self._realPlay()

    def _realPlay(self):
        self.needPlay = False
        name = self.playParam.get(self.NAME, None)
        actorDict = self.actorDict
        if name:
            if name not in self.actorDict:
                return
            actorDict = {name: self.actorDict[name]}
        if self.editMode:
            self.eventMgr.onPlayEndCB = self.reset
        else:
            self.eventMgr.onPlayEndCB = self.release
        if not self.usePlayerCamera:
            self.eventMgr.setFirstCamera()
        self.beginStamp = time.time()
        stamp = self.playParam.get(self.TIME, 0)
        callback = Functor(self.eventMgr.drive, actorDict, stamp, self.usePlayerCamera)
        playTime = self.playParam.get('playTime', 0)
        duration = self.beginStamp - playTime
        gamelog.debug('scenario@_realPlay', self.beginStamp, playTime, duration)
        if not self.usePlayerCamera:
            if duration >= FADE_TIME:
                fadeout(FADE_OUT_TIME, callback=Functor(self.eventMgr.processFillCam, callback))
            elif duration < FADE_TIME and duration >= 0:
                BigWorld.callback(FADE_TIME - duration, Functor(self._realPlay))
            else:
                self.eventMgr.processFillCam(callback)
        else:
            self.eventMgr.processFillCam(callback)

    def getActorByName(self, actName):
        if not self.actorDict.has_key(actName):
            return None
        else:
            actor = self.actorDict[actName]
            return actor.entity

    def preLoadRes(self):
        self.syncID += 1
        self.resLoadNum = 1
        threadID = gameglobal.URGENT_THREAD
        cbFunc = Functor(self.resLoadFinish, self.syncID)
        actorNames = sorted(self.actorDict)
        copyForActorIndex = 0
        for actorName in actorNames:
            actor = self.actorDict[actorName]
            if not hasattr(actor, 'modelId'):
                continue
            self.resLoadNum += 1
            if actor.isPlayer and self.copyForActor and copyForActorIndex < len(self.copyForActor):
                entCopy = self.copyForActor[copyForActorIndex]
                copyForActorIndex += 1
                actor.preLoadRes(threadID, cbFunc, self.setModelNeedHide, self.stopPlay, entCopy)
            else:
                actor.preLoadRes(threadID, cbFunc, self.setModelNeedHide, self.stopPlay)

        for event in self.eventMgr.eventList:
            event.preLoadRes()

        if gCameraCounter.modelPath:
            self.resLoadNum += 1
            gCameraCounter.reloadModel(threadID, cbFunc)
        self.preLoadModels(threadID, cbFunc)
        self.needPlay = True
        self.resLoadFinish(self.syncID)

    def preLoadModels(self, threadID, cbFunc = None):
        if self.preLoadModelSec:
            for mSect in self.preLoadModelSec.values():
                self.resLoadNum += 1
                res = mSect.readString('res')
                pos = tuple([ float(x) for x in mSect.readString('pos').split(',') ])
                yaw = mSect.readFloat('yaw')
                scale = tuple([ float(x) for x in mSect.readString('scale').split(',') ])
                clientUtils.fetchModel(threadID, Functor(self._afterPreLoadModel, cbFunc, pos, yaw, scale), res)

            self.preLoadModelSec = None

    def _afterPreLoadModel(self, callback, pos, yaw, scale, model):
        self.preLoadModel.append(model)
        BigWorld.player().addModel(model)
        model.position = pos
        model.yaw = yaw
        model.scale = scale
        if callback:
            callback()

    def resLoadFinish(self, syncID):
        if self.syncID != syncID:
            gamelog.error('@szh: resLoadFinish the syncID does not match', self.syncID, syncID)
            return
        self.resLoadNum -= 1
        if self.resLoadNum == 0:
            player = BigWorld.player()
            if self.needPlay and player and player.inWorld:
                self._realPlay()

    def watchCamera(self, isOpen = True):
        if self._cameraReady != isOpen:
            self._cameraReady = isOpen
            if isOpen:
                CC.newTrack()
                if hasattr(CC.TC, 'needDecay'):
                    CC.TC.needDecay = 1
            else:
                CC.endCamera()

    def addActor(self, stamp, roleName, tag, pos, yaw, npcId, showLogo, applyDrop = False):
        actor = Actor()
        actor.entity = None
        actor.name = roleName
        actor.pos = pos
        actor.destYaw = yaw
        actor.editMode = True
        actor.showLogo = showLogo
        actor.npcId = npcId
        actor.tag = tag
        actor.applyDrop = applyDrop
        if npcId == 0:
            actor.isPlayer = True
            actor.npcId = avatarNpc
        nd = NCD.data.get(npcId, None)
        if nd is None:
            actor.modelId = gameglobal.defaultModelID
        else:
            actor.modelId = nd.get('model', gameglobal.defaultModelID)
        if actor.name in self.actorDict:
            gamelog.debug('Entity exists in actor list!')
            return False
        self.actorDict[actor.name] = actor
        actor.createEntity(gameglobal.SCENARIO_EDIT_NPC)
        self.eventMgr.addActorEvent(stamp, roleName, 'born')
        return True

    def delActor(self, roleName):
        if roleName not in self.actorDict:
            gamelog.error('Not a valid actor')
            return None
        actor = self.actorDict[roleName]
        actor.reset(False)
        del self.actorDict[roleName]
        self.eventMgr.delActor(roleName)
        return actor

    def getDataByEvent(self, stamp):
        results = []
        if stamp < 0:
            return results
        event = self.eventMgr.getEvent(stamp)
        if event is None:
            return results
        envData = event.envEvent
        if envData.has_key('Effect'):
            for effect in envData['Effect'].keys():
                results.append(('Eff', effect[0], effect[1]))

        if envData.has_key('Model'):
            for model in envData['Model'].keys():
                results.append(('Model', model[0], model[1]))

        if envData.has_key('hideModel'):
            for model in envData['hideModel'].keys():
                results.append(('hideMod', model[0], model[1]))

        if envData.has_key('Dye'):
            results.append(('Dye',
             envData['Dye'][0],
             envData['Dye'][1],
             envData['Dye'][2]))
        if envData.has_key('Fade'):
            if len(envData['Fade']) == 4 and envData['Fade'][3]:
                results.append(('WhiteFade',
                 envData['Fade'][0],
                 envData['Fade'][1],
                 envData['Fade'][2]))
            else:
                results.append(('Fade',
                 envData['Fade'][0],
                 envData['Fade'][1],
                 envData['Fade'][2]))
        if envData.has_key('Fx'):
            for fxPath in envData['Fx']:
                results.append(('Fx', fxPath))

        if envData.has_key('Voice'):
            for voicePath in envData['Voice']:
                results.append(('Voice', voicePath))

        if envData.has_key('ScreenEff'):
            for info in envData['ScreenEff']:
                results.append(tuple(['ScreenEff'] + info))

        if envData.has_key('Sway'):
            results.append(tuple(['Sway'] + envData['Sway']))
        if envData.has_key('Msg'):
            for key in envData['Msg']:
                results.append(('Msg', key, envData['Msg'][key][0]))

        if envData.has_key('bgMusic'):
            results.append(('bgMusic', envData['bgMusic']))
        if envData.has_key('Plate'):
            results.append(('Plate', envData['Plate']['path']))
        if envData.has_key('projection'):
            results.append(('projection', envData['projection'][0], envData['projection'][1]))
        if envData.has_key('Dof'):
            results.append(('Dof', envData['Dof']))
        if envData.has_key('newDof'):
            results.append(('newDof', envData['newDof']))
        if envData.has_key('presetCC'):
            if envData['presetCC']:
                results.append(('presetCC', envData['presetCC']))
        if envData.has_key('Blur'):
            results.append(('Blur', envData['Blur'][0], envData['Blur'][1]))
        if envData.has_key('Weather'):
            results.append(('Weather', envData['Weather'][0], envData['Weather'][1]))
        if envData.has_key('colorGrading'):
            results.append(('colorGrading', envData['colorGrading']))
        if envData.has_key('ModelCamera'):
            results.append(('ModelCamera', envData['ModelCamera']))
        if envData.has_key('cg'):
            results.append(('cg', envData['cg']))
        if envData.has_key('swf'):
            results.append(('swf', envData['swf'][0], envData['swf'][1]))
        if envData.has_key('screenEffect'):
            results.append(('screenEffect', envData['screenEffect']))
        if envData.has_key('GUIMsg'):
            for key in envData['GUIMsg']:
                results.append(('GUIMsg', key, envData['GUIMsg'][key][0]))

        if envData.has_key('magnitude'):
            results.append(('magnitude', envData['magnitude']))
        if envData.has_key('questMsg'):
            results.append(('questMsg', envData['questMsg']))
        if envData.has_key('renderMode'):
            results.append(('renderMode', envData['renderMode']))
        actData = event.actorEvent
        for actName in actData.keys():
            results.append(('npc', actName))

        return results

    def getDataByActor(self, stamp, actName):
        results = []
        if not self.actorDict.has_key(actName):
            return results
        for event in self.eventMgr.eventList:
            if event.time != stamp:
                continue
            if event.actorEvent.has_key(actName):
                for action, param in event.actorEvent[actName]:
                    results.append((event.time, action, param))

        return results

    def setLifeTime(self, time):
        self.eventMgr.lifetime = time

    def _monsterDisplay(self):
        actors = self.actorDict.values()
        models = []
        for actor in actors:
            if actor.entity is not None and actor.entity.model is not None:
                models.append(actor.entity.model.sources)

        entities = BigWorld.entities.values()
        for entity in entities:
            if entity.model is not None and entity.model.sources in models:
                if hasattr(entity, 'refreshOpacityState'):
                    entity.refreshOpacityState()
                else:
                    entity.hide(False)

    def addTutorialEvent(self, stamp, callback, hasTutorial):
        self.eventMgr.addEvent(stamp)
        event = self.eventMgr.getEvent(stamp)
        event.addTutorialEvent(callback, hasTutorial)


class Actor(object):

    def __init__(self):
        super(Actor, self).__init__()
        self.name = ''
        self.petName = ''
        self.pos = None
        self.tag = None
        self.usePlayerCamera = 0
        self.isPlayer = False
        self.zaijuModel = None
        self.wingModel = None
        self.texturePriority = 0
        self.entity = None
        self.npcId = 0
        self.modelId = 0
        self.fullPath = ''
        self.curAction = None
        self.actions = []
        self.editMode = False
        self.applyDrop = True
        self.showLogo = True
        self.bodyModel = None
        self.modelFinishCB = None
        self.destYaw = 0
        self.attachModel = {}
        self.preLoadActs = []
        self.robNpcID = 0
        self.robNpcEntId = 0
        self.applyDrop = False

    def release(self):
        if self.entity:
            if self.entity.inWorld:
                BigWorld.destroyEntity(self.entity.id)
            self.entity = None
        if self.isPlayer:
            screenEffect.delEffect(gameglobal.EFFECT_TAG_WING_SLIDE_DASH)
        if self.bodyModel:
            self.bodyModel.texturePriority = 0
        if self.zaijuModel:
            self.zaijuModel.texturePriority = 0
        if self.wingModel:
            self.wingModel.texturePriority = 0
        for key in self.attachModel:
            if self.attachModel[key][0]:
                self.attachModel[key][0].texturePriority = 0
                self.attachModel[key][0] = None

        gamelog.debug('bgf:release', self.texturePriority)
        self.actions = []
        self.name = ''
        self.tag = None
        self.bodyModel = None
        self.modelFinishCB = None
        self.setModelNeedHide = 1
        self.zaijuModel = None
        self.wingModel = None
        self.attachModel = {}

    def load(self, sect):
        self.name = sect.name
        self.tag = sect.readString('tag')
        self.petName = sect.readString('petName')
        if self.petName is None:
            self.petName = ''
        self.showLogo = sect.readString('showLogo') != '0'
        self.npcId = sect.readInt('npcID')
        self.isPlayer = sect.readInt('isPlayer', 0)
        nd = NCD.data.get(self.npcId, None)
        if nd is None:
            self.modelId = gameglobal.defaultModelID
        elif nd.has_key('fullPath'):
            self.fullPath = nd['fullPath']
        else:
            self.modelId = nd.get('model', gameglobal.defaultModelID)
        pos = sect.readString('pos')
        self.pos = tuple([ float(x) for x in pos.split(',') ])
        self.destYaw = sect.readFloat('yaw')
        self.texturePriority = sect.readInt('texturePriority', 0)
        self.robNpcID = sect.readInt('robNpcID', 0)
        self.applyDrop = sect.readInt('applyDrop', 0)
        if self.editMode is True:
            self.createEntity(gameglobal.SCENARIO_EDIT_NPC)

    def preLoadRes(self, threadID, cbFunc = None, setModelNeedHide = 1, failCbFunc = None, entCopy = None):
        self.modelFinishCB = cbFunc
        self.setModelNeedHide = setModelNeedHide
        try:
            if self.isPlayer:
                p = BigWorld.player()
                if not entCopy:
                    entCopy = p
                if self.usePlayerCamera:
                    clientcom.fetchAvatarModel(entCopy, threadID, self.modelLoadFinish)
                else:
                    mpr = charRes.MultiPartRes()
                    mpr.queryByAvatar(entCopy)
                    mpr.isAvatar = False
                    mpr.applyConfig = False
                    res = mpr.getPrerequisites()
                    model = clientUtils.model(*res)
                    if hasattr(model, 'bkgLoadTint'):
                        model.bkgLoadTint = False
                    clientcom.copyAndSetAvatarConfig(self.modelLoadFinish, entCopy, model, True)
            elif self.usePlayerCamera:
                if self.fullPath:
                    clientUtils.fetchModel(threadID, self.modelLoadFinish, self.fullPath)
                else:
                    clientcom.fetchModel(threadID, self.modelLoadFinish, self.modelId)
            else:
                try:
                    if self.fullPath:
                        model = clientUtils.model(self.fullPath)
                    else:
                        model = clientcom.getModel(self.modelId)
                except:
                    gamelog.debug('Actor@preLoadRes no resources %s %d', self.fullPath, self.modelId)
                    model = None

                self.modelLoadFinish(model)
        except:
            if failCbFunc:
                failCbFunc()

    def modelLoadFinish(self, model):
        if not model:
            return
        self.bodyModel = model
        model.setModelNeedHide(self.setModelNeedHide, 1.0)
        if self.isPlayer:
            clientcom.getHairNode(BigWorld.player(), model)
        data = NCD.data.get(self.npcId, {})
        tintMs = data.get('materials', None)
        extraTint = data.get('extraTint', None)
        gamelog.debug('@szh: entity load model finished', model.sources, tintMs, extraTint)
        if tintMs:
            if type(tintMs) == tuple:
                tintMs = tintMs[0]
            tintalt.ta_set_static([model], tintMs)
        if extraTint:
            tintalt.ta_add([model], extraTint)
        attaches = data.get('attaches', [])
        if self.usePlayerCamera:
            self.attachModelFromDataByFetch(attaches)
            try:
                if self.preLoadActs:
                    model.fetchActions(self.preLoadActs, self._afterActionFinished)
            except:
                return

        else:
            self.attachModelFromData(attaches)
            for act in self.preLoadActs:
                model.loadActionNow(act)

        model.expandVisibilityBox(1000)
        if self.modelFinishCB:
            self.modelFinishCB()

    def _afterActionFinished(self):
        pass

    def attachModelFromData(self, attaches):
        entityModel = self.bodyModel
        try:
            for attach in attaches:
                modelPrefix = ''
                if len(attach) == 6:
                    attachHp, attachModel, _, attachScale, bias, modelPrefix = attach
                else:
                    attachHp, attachModel, _, attachScale, bias = attach
                if not modelPrefix:
                    modelPrefix = 'item/model'
                if attachScale <= 0:
                    attachScale = 1
                if attachModel and attachHp:
                    node = self.bodyModel.node(attachHp)
                    if node:
                        modelPath = '%s/%s' % (modelPrefix, attachModel)
                        attach = clientUtils.model(modelPath)
                        hairModel = ''
                        if modelPrefix.endswith('headdress'):
                            hairNodePath = modelServer.getHairNodeModel(entityModel)
                            hairModel = clientUtils.model(hairNodePath)
                            if hairModel:
                                node = entityModel.node('biped Head')
                                if node and hairModel not in node.attachments:
                                    node.attach(hairModel, 'biped Head')
                        self.afterAttachModelFinished(attachHp, attachScale, bias, hairModel, attach)

        except:
            gamelog.error('attachWeapon failed')

    def attachModelFromDataByFetch(self, attaches):
        entityModel = self.bodyModel
        for attach in attaches:
            modelPrefix = ''
            if len(attach) == 6:
                attachHp, attachModel, _, attachScale, bias, modelPrefix = attach
            else:
                attachHp, attachModel, _, attachScale, bias = attach
            if not modelPrefix:
                modelPrefix = 'item/model'
            if attachScale <= 0:
                attachScale = 1
            if attachModel and attachHp:
                threadID = gameglobal.URGENT_THREAD
                modelPath = '%s/%s' % (modelPrefix, attachModel)
                if modelPrefix.endswith('headdress'):
                    hairNodePath = modelServer.getHairNodeModel(entityModel)
                    threadID = gameglobal.URGENT_THREAD
                    clientUtils.fetchModel(threadID, Functor(self._afterHiarModelFinished, entityModel, attachHp, attachScale, bias, modelPath), hairNodePath)
                else:
                    hairModel = None
                    clientUtils.fetchModel(threadID, Functor(self.afterAttachModelFinished, attachHp, attachScale, bias, hairModel), modelPath)

    def _afterHiarModelFinished(self, entityModel, attachHp, attachScale, bias, modelPath, hairModel):
        if not entityModel:
            return
        if hairModel:
            node = entityModel.node('biped Head')
            if node and hairModel not in node.attachments:
                node.attach(hairModel, 'biped Head')
                threadID = gameglobal.URGENT_THREAD
                clientUtils.fetchModel(threadID, Functor(self.afterAttachModelFinished, attachHp, attachScale, bias, hairModel), modelPath)

    def afterAttachModelFinished(self, attachHp, attachScale, bias, hairModel, model):
        if self.bodyModel:
            try:
                bodyModel = self.bodyModel
                if hairModel:
                    bodyModel = hairModel
                bodyModel.setHP(attachHp, None)
                bodyModel.setHP(attachHp, model)
                model.texturePriority = self.texturePriority
                self.attachModel[attachHp] = [model, attachScale]
                if type(bias) == tuple:
                    model.bias = bias
                    model.action('1101')()
                if attachHp and attachScale:
                    node = bodyModel.node(attachHp)
                    if node:
                        node.scale(attachScale)
            except:
                pass

    def attachEffectFromData(self, attaches):
        for attach in attaches:
            if len(attach) == 6:
                _, _, attachEff, _, attachEffScale, _ = attach
            else:
                _, _, attachEff, _, attachEffScale = attach
            if attachEffScale <= 0:
                attachEffScale = 1
            if attachEff:
                fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (gameglobal.EFFECT_HIGH,
                 gameglobal.EFF_DEFAULT_PRIORITY,
                 self.bodyModel,
                 attachEff,
                 sfx.EFFECT_LIMIT_MISC))
                if fx:
                    for fxItem in fx:
                        fxItem.scale(attachEffScale, attachEffScale, attachEffScale)

    def createEntity(self, isScenario = gameglobal.SCENARIO_PLAY_NPC):
        param = {'roleName': self.name,
         'petName': self.petName,
         'showLogo': self.showLogo,
         'npcId': self.npcId,
         'isScenario': isScenario}
        spaceID = BigWorld.player().spaceID
        entityID = BigWorld.createEntity('Npc', spaceID, 0, self.pos, (0, 0, self.destYaw), param)
        entity = BigWorld.entity(entityID)
        if entity is None:
            gamelog.error('@szh create in scenario an None entity')
            return
        self.entity = entity
        entity.firstFetchFinished = True
        if isScenario in (gameglobal.SCENARIO_EDIT_NPC, gameglobal.SCENARIO_PLAY_NPC):
            if self.bodyModel:
                if not self.bodyModel.attached:
                    self.entity.fashion.setupModel(self.bodyModel)
                self.equipWing()
                if self.bodyModel not in self.entity.allModels:
                    self.entity.allModels.append(self.bodyModel)
                self.bodyModel.texturePriority = self.texturePriority
                gamelog.debug('bgf:createEntity', self.texturePriority, self.entity.models, self.entity.model.sources, self.entity.allModels)
        entity.enterTopLogoRange()
        entity.filter.applyDrop = self.applyDrop
        gamelog.debug('@szh: Npc entity created!', entity.id, self.entity.model.sources, entity.topLogo)
        if not self.showLogo and entity.topLogo:
            entity.topLogo.hide(True)

    def equipWing(self):
        data = NCD.data.get(self.npcId, {})
        wingId = data.get('wingId')
        if wingId:
            wingFlyAttachModel = attachedModel.WingFlyAttachModel(self.entity.id, None)
            attachmensts = wingFlyAttachModel.getAttachments(wingId)
            path = attachmensts[0][0]
            scale = attachmensts[0][3]
            modelId = path.split('/')[1]
            self.upWing(modelId, scale)

    def save(self, sect):
        if len(self.name) > 0:
            sect.deleteSection(self.name)
            mySect = sect.createSection(self.name)
            if self.tag is not None:
                mySect.writeString('tag', self.tag)
            if len(self.petName) > 0:
                mySect.writeString('petName', self.petName)
            if not self.showLogo:
                mySect.writeString('showLogo', '0')
            else:
                mySect.writeString('showLogo', '1')
            mySect.writeInt('npcID', self.npcId)
            mySect.writeInt('isPlayer', int(self.isPlayer))
            if self.pos is not None:
                pos = '%.2f,%.2f,%.2f' % self.pos
                mySect.writeString('pos', pos)
            mySect.writeString('yaw', '%.2f' % self.destYaw)
            mySect.writeInt('texturePriority', self.texturePriority)
            mySect.writeInt('robNpcID', self.robNpcID)
            mySect.writeInt('applyDrop', self.applyDrop)
        else:
            return False

    def reset(self, isBorn):
        if self.entity:
            gamelog.debug('@szh: destroy entity', self.entity.id)
            self.entity.model.texturePriority = 0
            BigWorld.destroyEntity(self.entity.id)
        if self.bodyModel:
            self.bodyModel.texturePriority = 0
        if self.zaijuModel:
            self.zaijuModel.texturePriority = 0
        if self.wingModel:
            self.wingModel.texturePriority = 0
        for key in self.attachModel:
            if self.attachModel[key][0]:
                self.attachModel[key][0].texturePriority = 0
                self.attachModel[key][0] = None

        self.bodyModel = None
        self.modelFinishCB = None
        self.wingModel = None
        self.attachModel = {}
        if isBorn is True:
            self.createEntity(gameglobal.SCENARIO_PLAY_NPC)
        else:
            self.entity = None

    def born(self):
        gamelog.debug('@szh: actor born', self.name)
        self.createEntity()
        if self.npcId and not self.isPlayer:
            data = NCD.data.get(self.npcId, {})
            attaches = data.get('attaches', [])
            self.attachEffectFromData(attaches)

    def speak(self, message):
        gamelog.debug('@szh: actor speaker', self.name, message, self.entity.id, self.entity.topLogo)
        msgList = message.split(',')
        message = msgList[0]
        if not self.entity.topLogo:
            return
        if len(msgList) == 2:
            lastTime = float(msgList[1])
            self.entity.topLogo.setChatMsg(message, lastTime)
        else:
            self.entity.topLogo.setChatMsg(message)

    def showBigEmote(self, args):
        emoteId = args
        heightOffset = 0
        if args.find(',') != -1:
            emoteId, heightOffset = args.split(',')
            heightOffset = float(heightOffset)
        if emoteId.isdigit():
            self.entity.topLogo.showBigEmote(int(emoteId), heightOffset)
        else:
            self.entity.topLogo.showEmoteByPath(emoteId, heightOffset)

    def run(self, x, y, z, time):
        pos = Math.Vector3(x, y, z)
        dis = (pos - self.entity.position).length
        speed = dis / time
        callback = self.endWingEffect if self.wingModel else None
        self.entity.filter.seek(pos, speed, callback)
        self.startWingEffect()

    def startWingEffect(self):
        if self.wingModel and self.isPlayer:
            screenEffs, _, _, _ = physicsEffect.getInfo(('WING_SLIDE_DASH_START', 'WING_SLIDE_DASH_DURATION'))
            screenEffect.startEffects(gameglobal.EFFECT_TAG_WING_SLIDE_DASH, screenEffs, False, BigWorld.player())

    def endWingEffect(self, success):
        if self.wingModel:
            screenEffect.delEffect(gameglobal.EFFECT_TAG_WING_SLIDE_DASH)

    def playAction(self, act):
        if self.curAction in self.entity.model.queue:
            self.entity.model.action(self.curAction).stop()
        try:
            self.entity.model.action(act)()
        except:
            gamelog.debug("@szh: can\'t find action:", act, self.entity.model.sources)

        self.curAction = act

    def emotionSuperpose(self, emotion):
        try:
            act = self.entity.model.action(emotion)
            act.enableAlpha(1)
            act()
        except:
            gamelog.debug("@szh: can\'t find action:", emotion, self.entity.model.sources)

    def stopCueSound(self):
        if self.curAction and self.entity and self.entity.fashion:
            self.entity.fashion._stopCueSoundAndEffect(self.curAction)

    def playEffect(self, effectId, maxDelayTime = '-1', pitch = '0', yaw = '0', roll = '0'):
        gamelog.debug('@szh: actor playEffect', effectId, roll, yaw, pitch, maxDelayTime)
        effectId = int(effectId)
        pitch = float(pitch)
        yaw = float(yaw)
        roll = float(roll)
        maxDelayTime = float(maxDelayTime)
        if self.entity:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (gameglobal.EFFECT_HIGH,
             gameglobal.EFF_DEFAULT_PRIORITY,
             self.entity.model,
             effectId,
             sfx.EFFECT_UNLIMIT,
             maxDelayTime))

    def refreshYaw(self, yaw = None):
        if self.entity:
            dYaw = yaw / 180.0 * math.pi
            self.entity.filter.yaw = dYaw
            self.entity.model.yaw = dYaw

    def setLookAt(self, coord = '0,0'):
        coord = coord.split(',')
        coordX = coord[0]
        coordY = coord[1]
        time = coord[2]
        poseNumber = coord[3]
        if self.entity:
            modelSource = self.entity.model.sources[0].split('/')
            charIndex = modelSource.index('char')
            modelId = modelSource[charIndex + 1]
            posePath = 'char/' + modelId + '/config/pose/' + poseNumber + '.xml'
            lookat_poser = BigWorld.AnimationPoser(posePath)
            self.entity.model.lookat_poser = lookat_poser
            lookat_poser.setCoord(float(coordX), float(coordY), float(time))

    def hideActor(self, isHide):
        if self.entity:
            self.entity.hide(isHide)
            if not isHide and not self.showLogo and self.entity.topLogo:
                self.entity.topLogo.hide(True)

    def addTranspare(self, value):
        if self.entity:
            if not hasattr(self.entity.model, 'fadeShader') or not self.entity.model.fadeShader:
                self.entity.model.fadeShader = BigWorld.BlendFashion()
            self.entity.model.fadeShader.dest(int(value))

    def upWing(self, model, ratio):
        if not self.bodyModel:
            self.bodyModel = self.entity.model
        self.wingModel = clientUtils.model(gameglobal.charRes + '%s/%s.model' % (model, model))
        self.wingModel.texturePriority = self.texturePriority
        am = BigWorld.ActionMatcher(self.entity)
        am.matchCaps = [keys.CAPS_IDLE0, keys.CAPS_FLY]
        self.wingModel.motors = (am,)
        self.entity.am.matchCaps = [keys.CAPS_IDLE0, keys.CAPS_FLY]
        self.bodyModel.setHP('HP_back', self.wingModel)
        self.bodyModel.node('HP_back').scale(float(ratio))
        self.entity.am.addChild(am)

    def upZaiju(self, model, ratio, matchCaps = '14'):
        if not self.bodyModel:
            self.bodyModel = self.entity.model
        try:
            self.zaijuModel = clientUtils.model(gameglobal.charRes + '%s/%s.model' % (model, model))
            self.zaijuModel.texturePriority = self.texturePriority
            ratio = float(ratio)
            matchCaps = int(matchCaps)
            self.zaijuModel.scale = (ratio, ratio, ratio)
            self.entity.fashion.setupModel(self.zaijuModel, False)
            self.zaijuModel.setHP('HP_ride', self.bodyModel)
            self.entity.am.matchCaps = [keys.CAPS_HAND_FREE, matchCaps]
            am = BigWorld.ActionMatcher(self.entity)
            self.bodyModel.motors = (am,)
            self.entity.am.addChild(am)
        except:
            pass

    def downWing(self):
        if self.wingModel:
            self.bodyModel.setHP('HP_back', None)
            self.wingModel = None
            self.entity.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND]

    def playWingAction(self, act):
        try:
            if self.wingModel:
                self.wingModel.action(act)()
        except:
            pass

    def downZaiju(self):
        if self.zaijuModel:
            self.zaijuModel.setHP('HP_ride', None)
            self.entity.fashion.setupModel(self.bodyModel)
            self.entity.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND]

    def upWeapon(self, modelPath, ratio, attachHp, biasX = 0, biasY = 0, biasZ = 0):
        if biasX or biasY or biasZ:
            biasX = float(biasX)
            biasY = float(biasY)
            biasZ = float(biasZ)
            bias = (biasX, biasY, biasZ)
        else:
            bias = ''
        attaches = [(attachHp,
          modelPath,
          '',
          float(ratio),
          bias)]
        self.attachModelFromData(attaches)

    def switchWeapon(self, delayTime, action, leftHandOldHP, leftHandNewHP, rightHandOldHP, rightHandNewHP, caps):
        try:
            delayTime = float(delayTime)
        except:
            delayTime = 0

        self.playAction(action)
        hpList = []
        if leftHandOldHP and leftHandNewHP:
            hpList.append((leftHandOldHP, leftHandNewHP))
        if rightHandOldHP and rightHandNewHP:
            hpList.append((rightHandOldHP, rightHandNewHP))
        if delayTime:
            BigWorld.callback(delayTime, Functor(self._switchWeapon, hpList, caps))
        else:
            self._switchWeapon(hpList, caps)

    def _switchWeapon(self, hpList, caps):
        for oldHP, newHP in hpList:
            if self.attachModel.has_key(oldHP) and self.attachModel[oldHP]:
                attach, attachScale = self.attachModel[oldHP]
                self.bodyModel.setHP(oldHP, None)
                self.bodyModel.setHP(newHP, attach)
                node = self.bodyModel.node(newHP)
                if node:
                    node.scale(attachScale)
                del self.attachModel[oldHP]
                self.attachModel[newHP] = [attach, attachScale]

        if caps:
            self.entity.am.matchCaps = [int(caps), keys.CAPS_GROUND]

    def setTexturePriority(self, value):
        self.texturePriority = int(value)

    def movePosition(self, x, y, z):
        self.pos = (x, y, z)
        if self.entity:
            self.entity.filter.position = self.pos

    def robNpcModel(self, npcId):
        self.robNpcID = int(npcId)


class EventMgr(object):

    def __init__(self):
        self.eventList = []
        self.actorDict = None
        self.syncID = 0
        self.onPlayEndCB = None
        self.hPlayEndCB = None
        self._driveTimer = None
        self.camReady = False
        self.lifetime = 0
        self.pauseHandle = None
        self.pauseResult = True
        self.isPause = False
        self.isEnd = False

    def reset(self):
        for event in self.eventList:
            event.release()

        self.syncID += 1
        self.restoreCam()
        if self.hPlayEndCB:
            BigWorld.cancelCallback(self.hPlayEndCB)
            self.hPlayEndCB = None
        if self._driveTimer:
            BigWorld.cancelCallback(self._driveTimer)
            self._driveTimer = None
        self.pauseHandle = None
        self.pauseResult = True
        self.isPause = False
        self.isEnd = False

    def load(self, eventSect):
        for frameSect in eventSect.values():
            event = Event()
            event.load(frameSect)
            self.eventList.append(event)

        self.eventList.sort(lambda x, y: cmp(x.time, y.time))
        if len(self.eventList) > 0 and self.lifetime < self.eventList[-1].time:
            self.lifetime = self.eventList[-1].time

    def save(self, eventSect):
        self.trimCamInfo()
        for event in self.eventList:
            frameSect = eventSect.createSection('frame')
            frameSect.writeString('time', '%.2f' % event.time)
            if len(event.actorEvent) > 0:
                actorSect = frameSect.createSection('Actor')
                for name, actions in event.actorEvent.iteritems():
                    nameSect = actorSect.createSection(name)
                    for action, param in actions:
                        nameSect.writeString(action, param)

            if len(event.envEvent) > 0:
                envSect = frameSect.createSection('Env')
                envEff = event.envEvent.get('Effect', None)
                if envEff:
                    effSect = envSect.createSection('Effect')
                    index = 1
                    for (effectId, pos), (roll, yaw, pitch, duration) in envEff.iteritems():
                        idxSect = effSect.createSection('item')
                        idxSect.writeInt('id', effectId)
                        pos = '%.2f,%.2f,%.2f' % pos
                        idxSect.writeString('pos', pos)
                        param = [ '%.2f' % x for x in [roll,
                         yaw,
                         pitch,
                         duration] ]
                        idxSect.writeString('param', ','.join(param))
                        index += 1

                envModel = event.envEvent.get('Model', None)
                if envModel:
                    modelSect = envSect.createSection('Model')
                    index = 1
                    for modelId, pos in envModel.keys():
                        param = ','.join([ '%.2f' % x for x in envModel[modelId, pos][1:] ])
                        idxSect = modelSect.createSection('item')
                        idxSect.writeString('id', modelId)
                        pos = '%.2f,%.2f,%.2f' % pos
                        idxSect.writeString('pos', pos)
                        idxSect.writeString('param', param)
                        index += 1

                envHide = event.envEvent.get('hideModel', None)
                if envHide:
                    hideSect = envSect.createSection('hideModel')
                    for modelId, pos in envHide.keys():
                        param = ', '.join([ '%d' % x for x in envHide[modelId, pos] ])
                        idxSect = hideSect.createSection('item')
                        idxSect.writeString('id', modelId)
                        pos = '%.2f,%.2f,%.2f' % pos
                        idxSect.writeString('pos', pos)
                        idxSect.writeString('param', param)

                envMsg = event.envEvent.get('Msg', None)
                if envMsg:
                    msgSect = envSect.createSection('Msg')
                    idxMaxLength = len(str(len(envMsg)))
                    idx = 1
                    for coord in envMsg:
                        info = envMsg[coord]
                        idxLength = len(str(idx))
                        idxNamePrefix = '0' * (idxMaxLength - idxLength)
                        idxSect = msgSect.createSection(idxNamePrefix + '%i' % idx)
                        coord = '%.2f,%.2f' % coord
                        idxSect.writeString('coord', coord)
                        param = '%s %x %.1f %i %i' % (info[0],
                         info[1],
                         info[2],
                         info[3],
                         info[4])
                        idxSect.writeString('param', param)
                        idxSect.writeString('font', info[5])
                        idxSect.writeInt('midSet', info[6])
                        idx += 1

                envGUIMsg = event.envEvent.get('GUIMsg', None)
                if envGUIMsg:
                    msgSect = envSect.createSection('GUIMsg')
                    idx = 1
                    for coord, info in envGUIMsg.iteritems():
                        idxSect = msgSect.createSection('%i' % idx)
                        coord = '%.2f,%.2f' % coord
                        idxSect.writeString('coord', coord)
                        idxSect.writeString('msg', info[0])
                        idxSect.writeInt('color', info[1])
                        idxSect.writeInt('duration', info[2])
                        idxSect.writeInt('size', info[3])
                        idxSect.writeInt('frame', info[4])
                        idxSect.writeInt('blackGround', info[5])
                        idxSect.writeInt('notMid', info[6])
                        idx += 1

                envPlate = event.envEvent.get('Plate', None)
                if envPlate:
                    plateSect = envSect.createSection('Plate')
                    plateSect.writeString('path', envPlate['path'])
                    plateSect.writeFloat('leftX', envPlate['leftX'])
                    plateSect.writeFloat('rightX', envPlate['rightX'])
                    plateSect.writeFloat('topY', envPlate['topY'])
                    plateSect.writeFloat('bottomY', envPlate['bottomY'])
                    plateSect.writeFloat('totalTime', envPlate['totalTime'])
                    transformSect = plateSect.createSection('transform')
                    for item in envPlate['transform']:
                        paramSect = transformSect.createSection('param')
                        paramSect.asVector4 = Math.Vector4(item)

                    plateSect.writeString('smallPath', envPlate['smallPath'])
                    plateSect.writeFloat('smallLeftX', envPlate['smallLeftX'])
                    plateSect.writeFloat('smallTopY', envPlate['smallTopY'])
                envDye = event.envEvent.get('Dye', None)
                if envDye:
                    color = envDye[0]
                    red = int(round(color[0] * 255))
                    green = int(round(color[1] * 255))
                    blue = int(round(color[2] * 255))
                    color = red << 16 | green << 8 | blue
                    color = '%x' % color
                    fadeTime = '%.2f' % envDye[1]
                    duration = '%.2f' % envDye[2]
                    envSect.writeString('Dye', ','.join((color, fadeTime, duration)))
                envFade = event.envEvent.get('Fade', None)
                if envFade:
                    envSect.writeString('Fade', ','.join([ '%.2f' % x for x in envFade ]))
                envSway = event.envEvent.get('Sway', None)
                if envSway:
                    envSect.writeString('Sway', ','.join([ '%.2f' % x for x in envSway ]))
                screenEff = event.envEvent.get('ScreenEff', None)
                if screenEff:
                    screenSect = envSect.createSection('ScreenEff')
                    for info in screenEff:
                        itemSect = screenSect.createSection('item')
                        itemSect.asString = ','.join([ '%.2f' % x for x in info ])

                envMusic = event.envEvent.get('Fx', None)
                if envMusic:
                    musicSect = envSect.createSection('Fx')
                    for i, fxPath in enumerate(envMusic):
                        itemSect = musicSect.createSection('item')
                        itemSect.asString = fxPath

                envVoice = event.envEvent.get('Voice', None)
                if envVoice:
                    musicSect = envSect.createSection('Voice')
                    for i, voicePath in enumerate(envVoice):
                        itemSect = musicSect.createSection('item')
                        itemSect.asString = voicePath

                envBgMusic = event.envEvent.get('bgMusic', None)
                if envBgMusic:
                    bgMusic = envBgMusic[0]
                    for item in envBgMusic[1:]:
                        bgMusic += ',%d' % item

                    envSect.writeString('bgMusic', bgMusic)
                envModelCamera = event.envEvent.get('ModelCamera', None)
                if envModelCamera:
                    modelId, pos, yaw, action, scale, isHideModelCamera = envModelCamera
                    modelCameraSect = envSect.createSection('ModelCamera')
                    modelCameraSect.writeInt('id', modelId)
                    modelCameraSect.writeString('pos', '%.2f,%.2f,%.2f' % pos)
                    modelCameraSect.writeString('yaw', '%.2f' % yaw)
                    modelCameraSect.writeString('act', action)
                    modelCameraSect.writeString('scale', '%.2f,%.2f,%.2f' % scale)
                    modelCameraSect.writeInt('isHideModelCamera', isHideModelCamera)
                envCg = event.envEvent.get('cg', None)
                if envCg:
                    envSect.writeString('cg', envCg)
                questMsg = event.envEvent.get('questMsg', None)
                if questMsg:
                    envSect.writeString('questMsg', '%s,%d,%d' % questMsg)
                envSwf = event.envEvent.get('swf', None)
                if envSwf:
                    envSect.writeString('swf', '%s,%.2f' % envSwf)
                envScreenEffect = event.envEvent.get('screenEffect', None)
                if envScreenEffect:
                    envSect.writeString('screenEffect', '%s,%.2f,%.2f,%.2f' % envScreenEffect)
                envProjection = event.envEvent.get('projection', None)
                if envProjection:
                    envSect.writeString('projection', '%.2f,%.2f' % (envProjection[0], envProjection[1]))
                envDof = event.envEvent.get('Dof', None)
                if envDof:
                    envSect.writeString('Dof', '%.2f,%.2f,%.2f' % envDof)
                envNewDof = event.envEvent.get('newDof', None)
                if envNewDof:
                    envSect.writeString('newDof', '%.2f,%.2f,%.2f,%.2f,%.2f,%.2f' % envNewDof)
                envPresetCC = event.envEvent.get('presetCC', None)
                if envPresetCC:
                    envSect.writeString('presetCC', '%s' % envPresetCC)
                envBlur = event.envEvent.get('Blur', None)
                if envBlur:
                    envSect.writeString('Blur', '%.2f,%.2f' % (envBlur[0], envBlur[1]))
                envWeather = event.envEvent.get('Weather', None)
                if envWeather:
                    envSect.writeString('Weather', '%s,%.2f' % (envWeather[0], envWeather[1]))
                envColorGrading = event.envEvent.get('colorGrading', None)
                if envColorGrading:
                    envSect.writeString('colorGrading', envColorGrading)
            if event.cameraInfo:
                camSect = frameSect.createSection('Camera')
                strCam = '%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.1f,%.1f' % tuple(event.cameraInfo)
                camSect.writeString('Param', strCam)
                if event.newCamTrack:
                    camSect.writeBool('NewTrack', 1)
                if event.fillCamera:
                    camSect.writeBool('FillCamera', 1)
            magnitude = event.envEvent.get('magnitude', None)
            if magnitude:
                envSect.writeString('magnitude', '%.2f,%.2f' % (magnitude[0], magnitude[1]))
            renderMode = event.envEvent.get('renderMode', -1)
            if renderMode >= 0:
                envSect.writeInt('renderMode', renderMode)

    def release(self):
        self.syncID = 0
        self.actorDict = None
        for event in self.eventList:
            event.release()

        self.eventList = []
        self.restoreCam()
        self.onPlayEndCB = None
        self.pauseHandle = None
        self.pauseResult = True
        self.isPause = False
        self.isEnd = False

    def stopPlay(self):
        if self._driveTimer:
            BigWorld.cancelCallback(self._driveTimer)
            self._driveTimer = None
        if self.hPlayEndCB:
            BigWorld.cancelCallback(self.hPlayEndCB)
            self.hPlayEndCB = None

    def continuePlay(self, isEnd, success):
        self.pauseResult = success
        self.isEnd = isEnd
        self.isPause = False
        if self.pauseHandle:
            self.pauseHandle()

    def pausePlayInEvent(self):
        self.isPause = True

    def getEvent(self, stamp):
        isSuccess, idx = self.findEventByTime(stamp)
        if isSuccess:
            return self.eventList[idx]
        else:
            return None

    def findEventByTime(self, t):
        data = self.eventList
        len_data = len(data)
        i = -1
        j = len_data
        while i + 1 != j:
            mid = i + j >> 1
            if data[mid].time < t:
                i = mid
            else:
                j = mid

        if j == len_data or data[j].time != t:
            return (False, j)
        return (True, j)

    def addEvent(self, stamp):
        found, idx = self.findEventByTime(stamp)
        if not found:
            event = Event()
            event.time = stamp
            self.eventList.insert(idx, event)
        self.lifetime = max(self.lifetime, stamp)
        return idx

    def delEventByIndex(self, index):
        if index >= len(self.eventList):
            return False
        del self.eventList[index]
        if len(self.eventList) > 0:
            self.lifetime = self.eventList[-1].time
        else:
            self.lifetime = 0
        return True

    def changeEventTime(self, oldStamp, newStamp):
        if oldStamp == newStamp:
            return
        oldEvent = self.getEvent(oldStamp)
        if oldEvent:
            suc, idx = self.findEventByTime(oldStamp)
            if suc:
                self.delEventByIndex(idx)
            suc, idx = self.findEventByTime(newStamp)
            if suc:
                self.delEventByIndex(idx)
            oldEvent.time = newStamp
            self.eventList.insert(idx, oldEvent)

    def addActorEvent(self, stamp, name, action, param = ''):
        if stamp < 0:
            return False
        found, idx = self.findEventByTime(stamp)
        if found:
            event = self.eventList[idx]
            if not event.actorEvent.has_key(name):
                event.actorEvent[name] = []
            event.actorEvent[name].append((action, param))
        else:
            event = Event()
            event.time = stamp
            event.actorEvent[name] = [(action, param)]
            self.eventList.insert(idx, event)
        self.lifetime = max(self.lifetime, stamp)
        return True

    def delActorEvent(self, stamp, name, index):
        if stamp < 0:
            return False
        found, idx = self.findEventByTime(stamp)
        if found:
            event = self.eventList[idx]
            if event.actorEvent.has_key(name) and index < len(event.actorEvent[name]):
                event.actorEvent[name].remove(event.actorEvent[name][index])
                if len(event.actorEvent[name]) == 0:
                    del event.actorEvent[name]

    def delActor(self, name):
        for event in self.eventList:
            if event.actorEvent.has_key(name):
                del event.actorEvent[name]

    def drive(self, actorDict, startTime = 0, usePlayerCamera = 0):
        self.syncID += 1
        if startTime == 0:
            idx = 0
        else:
            idx = self.findEventByTime(startTime)[1]
        self.actorDict = actorDict
        self.trimFillCam()
        self.trimCamInfo()
        self.camReady = False
        if len(self.eventList) <= idx:
            if self.onPlayEndCB:
                self.onPlayEndCB()
            return
        event = self.eventList[idx]
        self._driveTimer = BigWorld.callback(event.time - startTime, Functor(self._drive, idx, self.syncID, usePlayerCamera))
        if self.hPlayEndCB:
            BigWorld.cancelCallback(self.hPlayEndCB)
            self.hPlayEndCB = None
        if self.onPlayEndCB:
            self.hPlayEndCB = BigWorld.callback(self.lifetime - startTime, self.onPlayEndCB)

    def _drive(self, idx, syncId, usePlayerCamera = 0):
        BigWorld.worldDrawEnabled(True)
        gamelog.debug('@szh: _drive', idx, syncId, usePlayerCamera)
        eventCnt = len(self.eventList)
        if syncId != self.syncID or idx >= eventCnt:
            gamelog.error('@szh: _drive syncId is invalid', syncId, self.syncID)
            return
        event = self.eventList[idx]
        if not self.pauseResult and not self.isEnd:
            if self.onPlayEndCB:
                self.onPlayEndCB()

        def pauseFunc():
            self.pauseHandle = Functor(self._driveNext, idx, syncId, usePlayerCamera)
            if self.hPlayEndCB:
                BigWorld.cancelCallback(self.hPlayEndCB)
                self.hPlayEndCB = None

        if self.isPause:
            pauseFunc()
        elif event.checkTutorialEvent():
            event.playTutorialEvent()
            if event.checkHaveTutorial():
                pauseFunc()
            else:
                self._driveNext(idx, syncId, usePlayerCamera)
        else:
            self._driveNext(idx, syncId, usePlayerCamera)

    def _driveNext(self, idx, syncId, usePlayerCamera = 0):
        eventCnt = len(self.eventList)
        event = self.eventList[idx]
        try:
            event.play(self.actorDict, usePlayerCamera, self.pauseResult)
        except Exception as e:
            gamelog.debug('@szh: _drive exception', e)
            self.restoreCam()
            if self.hPlayEndCB:
                BigWorld.cancelCallback(self.hPlayEndCB)
                self.hPlayEndCB = None
            if self.onPlayEndCB:
                self.onPlayEndCB()
            return

        if not self.hPlayEndCB and self.onPlayEndCB:
            self.hPlayEndCB = BigWorld.callback(self.lifetime - event.time, self.onPlayEndCB)
        if not usePlayerCamera and event.newCamTrack:
            gamelog.debug('@szh: start a new camera track in frame', idx)
            self.playTrack(idx)
        if idx < eventCnt - 1:
            nextEvent = self.eventList[idx + 1]
            gamelog.debug('@szh _drive timeinternal', nextEvent.time, event.time, nextEvent.time - event.time)
            self._driveTimer = BigWorld.callback(nextEvent.time - event.time, Functor(self._drive, idx + 1, syncId, usePlayerCamera))
        else:
            gamelog.debug('@szh: the scenario is last frame')
            if self._driveTimer:
                BigWorld.cancelCallback(self._driveTimer)
            self._driveTimer = None

    def setFirstCamera(self):
        if not self.camReady:
            self.initCam()
        if len(self.eventList) == 0 or self.eventList[0] is None:
            return
        if self.eventList[0].cameraInfo is None:
            return
        CC.newTrack()
        CC.moveCamera(self.eventList[0].cameraInfo)

    def playTrack(self, eventIndex):
        if not self.camReady:
            self.initCam()
        CC.newTrack()
        dofList = []
        for event in self.eventList[eventIndex:]:
            if event.envEvent.has_key('newDof'):
                dofInfo = event.envEvent['newDof']
                dofList.append((event.time,) + dofInfo)
            if event.cameraInfo is None:
                continue
            CC.pushKey(event.cameraInfo)
            if event.cameraInfo[8] == 0:
                break

        CC.TC.deleteKey(0)
        if dofList and hasattr(CC.TC, 'scenarioDOF'):
            CC.TC.scenarioDOF(dofList)
        CC.play()

    def initCam(self):
        if self.camReady:
            return
        BigWorld.cameraBindPlayer(False)
        self.camReady = True

    def restoreCam(self):
        CC.endCamera()
        if not isinstance(BigWorld.camera(), BigWorld.CursorCamera):
            BigWorld.camera(gameglobal.rds.cam.cc)
        BigWorld.cameraBindPlayer(True)
        self.camReady = False

    def trimCamInfo(self):
        preCamEvent = None
        for event in self.eventList:
            if event.cameraInfo is None:
                continue
            if preCamEvent:
                if event.newCamTrack:
                    preCamEvent.cameraInfo[8] = 0
                    gamelog.debug('trimCamInfo0', event.newCamTrack, preCamEvent.cameraInfo)
                else:
                    preCamEvent.cameraInfo[8] = event.time - preCamEvent.time
            else:
                event.newCamTrack = True
            preCamEvent = event

        if preCamEvent and preCamEvent.cameraInfo:
            preCamEvent.cameraInfo[8] = 0

    def processFillCam(self, callback = None):
        if len(self.eventList) >= 2 and self.eventList[0].fillCamera and self.eventList[1].cameraInfo:
            oldYaw = gameglobal.rds.cam.cc.direction.yaw
            newYaw = (Math.Vector3(self.eventList[1].cameraInfo[0:3]) - gameglobal.rds.cam.cc.position).yaw
            deltaYaw = newYaw - oldYaw
            if deltaYaw > math.pi:
                deltaYaw = deltaYaw - 2 * math.pi
            elif deltaYaw < -math.pi:
                deltaYaw = deltaYaw + 2 * math.pi
            if abs(deltaYaw) >= math.pi / 4:
                self._rotateCursorCamera(deltaYaw, callback)
            elif callback:
                callback()
        elif callback:
            callback()

    def _rotateCursorCamera(self, deltaYaw, callback = None):
        num = abs(int(deltaYaw / math.pi * 180 / 2))
        deltaTime = 0.02
        deltaYaw = deltaYaw / num
        self._rotate(deltaYaw, deltaTime, num, callback)

    def _rotate(self, deltaYaw, deltaTime, num, callback = None):
        if num == 0:
            if callback:
                callback()
            return
        gameglobal.rds.cam.cc.deltaYaw += deltaYaw
        BigWorld.callback(deltaTime, Functor(self._rotate, deltaYaw, deltaTime, num - 1, callback))

    def trimFillCam(self):
        cam = gameglobal.rds.cam.cc
        m = Math.Matrix(cam.matrix)
        pos = cam.position
        quad = cameraEffect.eulerAngleToQuad(m.yaw, m.pitch, m.roll)
        fov = BigWorld.projection().fov
        if len(self.eventList):
            for i in (0, -1):
                event = self.eventList[i]
                if event.fillCamera:
                    keyData = [pos[0],
                     pos[1],
                     pos[2],
                     quad[0],
                     quad[1],
                     quad[2],
                     quad[3],
                     fov,
                     0,
                     0]
                    event.cameraInfo = keyData
                    if i == 0 and len(self.eventList) >= 2:
                        event.cameraInfo[8] = self.eventList[1].time - self.eventList[0].time
                        gamelog.debug('trimFillCam', event.cameraInfo)


class Event(object):

    def __init__(self):
        super(Event, self).__init__()
        self.time = 0
        self.actorEvent = {}
        self.envEvent = {}
        self.envDummyModels = []
        self.hEffCB = []
        self.hDyeCB = None
        self.cameraInfo = None
        self.newCamTrack = False
        self.fillCamera = False
        self.envMsgs = []
        self.cgPlayer = None

    def isEmpty(self):
        return len(self.actorEvent) == 0 and len(self.envEvent) == 0 and self.cameraInfo is None and self.fillCamera == False

    def load(self, timeSect):
        self.time = float(timeSect.readString('time'))
        self.actorEvent = {}
        actorSect = timeSect.openSection('Actor')
        if actorSect:
            for nameSect in actorSect.values():
                actions = []
                for actionSect in nameSect.values():
                    action = actionSect.name
                    param = nameSect.readString(action)
                    actions.append((action, param))

                self.actorEvent[nameSect.name] = actions

        self.envEvent = {}
        envSect = timeSect.openSection('Env')
        if envSect:
            effSect = envSect.openSection('Effect')
            if effSect:
                self.envEvent['Effect'] = {}
                for effect in effSect.values():
                    effectId = effect.readInt('id')
                    pos = effect.readString('pos')
                    pos = tuple([ float(x) for x in pos.split(',') ])
                    param = effect.readString('param').split(',')
                    self.envEvent['Effect'][effectId, pos] = tuple([ float(x) for x in param ])

            msgSect = envSect.openSection('Msg')
            if msgSect:
                self.envEvent['Msg'] = {}
                for v in msgSect.values():
                    coord = v.readString('coord')
                    coord = tuple(map(float, coord.split(',')))
                    param = v.readString('param').split(' ')
                    fontName = v.readString('font', 'Î¢ÈíÑÅºÚ')
                    midSet = v.readInt('midSet', 0)
                    msg = ' '.join(param[:-4])
                    color = long(param[-4], 16)
                    duration = float(param[-3])
                    size = int(param[-2])
                    filmEffct = int(param[-1])
                    self.envEvent['Msg'][coord] = (msg,
                     color,
                     duration,
                     size,
                     filmEffct,
                     fontName,
                     midSet)

            msgSect = envSect.openSection('GUIMsg')
            if msgSect:
                self.envEvent['GUIMsg'] = {}
                for v in msgSect.values():
                    coord = v.readString('coord')
                    coord = tuple(map(float, coord.split(',')))
                    msg = v.readString('msg')
                    color = v.readInt('color')
                    duration = v.readInt('duration')
                    size = v.readInt('size')
                    frame = v.readInt('frame')
                    blackGround = v.readInt('blackGround')
                    notMid = v.readInt('notMid')
                    self.envEvent['GUIMsg'][coord] = (msg,
                     color,
                     duration,
                     size,
                     frame,
                     blackGround,
                     notMid)

            modelSect = envSect.openSection('Model')
            if modelSect:
                self.envEvent['Model'] = {}
                for model in modelSect.values():
                    modelId = model.readString('id')
                    pos = model.readString('pos')
                    pos = tuple([ float(x) for x in pos.split(',') ])
                    roll, yaw, pitch, duration = [ float(x) for x in model.readString('param').split(',') ]
                    self.envEvent['Model'][modelId, pos] = (None,
                     roll,
                     yaw,
                     pitch,
                     duration)

            hideSect = envSect.openSection('hideModel')
            if hideSect:
                self.envEvent['hideModel'] = {}
                for model in hideSect.values():
                    modelId = model.readString('id')
                    pos = model.readString('pos')
                    pos = tuple([ float(x) for x in pos.split(',') ])
                    hideModel, whenBorn = [ int(x) for x in model.readString('param').split(',') ]
                    self.envEvent['hideModel'][modelId, pos] = (hideModel, whenBorn)

            dyeInfo = envSect.readString('Dye')
            if dyeInfo:
                param = dyeInfo.split(',')
                color = int(param[0], 16)
                red = (color & 16711680) >> 16
                green = (color & 65280) >> 8
                blue = color & 255
                color = (red / 255.0, green / 255.0, blue / 255.0)
                fadeTime = float(param[1])
                duration = float(param[2])
                self.envEvent['Dye'] = (color, fadeTime, duration)
            fadeInfo = envSect.readString('Fade')
            if fadeInfo:
                param = [ float(x) for x in fadeInfo.split(',') ]
                self.envEvent['Fade'] = param
            swayInfo = envSect.readString('Sway')
            if swayInfo:
                param = [ float(x) for x in swayInfo.split(',') ]
                self.envEvent['Sway'] = param
            screenEff = envSect.openSection('ScreenEff')
            if screenEff:
                self.envEvent['ScreenEff'] = []
                for eff in screenEff.values():
                    param = eff.asString
                    param = [ float(x) for x in param.split(',') ]
                    self.envEvent['ScreenEff'].append(param)

            musicInfo = envSect.openSection('Fx')
            if musicInfo:
                self.envEvent['Fx'] = []
                for music in musicInfo.values():
                    gamelog.debug('bgf:scenario', music, music.asString)
                    self.envEvent['Fx'].append(music.asString)

            voiceInfo = envSect.openSection('Voice')
            if voiceInfo:
                self.envEvent['Voice'] = []
                for voice in voiceInfo.values():
                    gamelog.debug('bgf:scenario', voice, voice.asString)
                    self.envEvent['Voice'].append(voice.asString)

            bgMusicInfo = envSect.readString('bgMusic')
            if bgMusicInfo:
                param = bgMusicInfo.split(',')
                self.envEvent['bgMusic'] = [param[0]]
                for item in param[1:]:
                    self.envEvent['bgMusic'].append(int(item))

            plateInfo = envSect.openSection('Plate')
            if plateInfo:
                self.envEvent['Plate'] = dataDict = {}
                dataDict['path'] = plateInfo.readString('path')
                dataDict['leftX'] = plateInfo.readFloat('leftX')
                dataDict['rightX'] = plateInfo.readFloat('rightX')
                dataDict['topY'] = plateInfo.readFloat('topY')
                dataDict['bottomY'] = plateInfo.readFloat('bottomY')
                dataDict['totalTime'] = plateInfo.readFloat('totalTime')
                transformInfo = plateInfo.openSection('transform')
                dataDict['transform'] = []
                for item in transformInfo.values():
                    x, y, scale, time = item.asVector4
                    dataDict['transform'].append((x,
                     y,
                     scale,
                     time))

                dataDict['smallPath'] = plateInfo.readString('smallPath')
                dataDict['smallLeftX'] = plateInfo.readFloat('smallLeftX')
                dataDict['smallTopY'] = plateInfo.readFloat('smallTopY')
            cgInfo = envSect.readString('cg')
            if cgInfo:
                self.envEvent['cg'] = cgInfo
            questMsg = envSect.readString('questMsg')
            if questMsg:
                questMsg = questMsg.split(',')
                self.envEvent['questMsg'] = (questMsg[0], int(questMsg[1]), int(questMsg[2]))
            swfInfo = envSect.readString('swf')
            if swfInfo:
                swfName, swfTime = swfInfo.split(',')
                self.envEvent['swf'] = (swfName, float(swfTime))
            screenEffectInfo = envSect.readString('screenEffect')
            if screenEffectInfo:
                path, time, fadein, fadeout = screenEffectInfo.split(',')
                self.envEvent['screenEffect'] = (path,
                 float(time),
                 float(fadein),
                 float(fadeout))
            projection = envSect.readString('projection')
            if projection:
                param = projection.split(',')
                self.envEvent['projection'] = [float(param[0]), float(param[1])]
            dof = envSect.readString('Dof')
            if dof:
                param = dof.split(',')
                self.envEvent['Dof'] = (float(param[0]), float(param[1]), float(param[2]))
            newDof = envSect.readString('newDof')
            if newDof:
                param = newDof.split(',')
                self.addEnvDof(*[ float(x) for x in param ])
            presetCC = envSect.readString('presetCC')
            if presetCC:
                self.envEvent['presetCC'] = envSect.readString('presetCC')
            blur = envSect.readString('Blur')
            if blur:
                param = blur.split(',')
                self.envEvent['Blur'] = [float(param[0]), float(param[1])]
            weather = envSect.readString('Weather')
            if weather:
                param = weather.split(',')
                self.envEvent['Weather'] = [str(param[0]), float(param[1])]
            colorGrading = envSect.readString('colorGrading')
            if colorGrading:
                self.envEvent['colorGrading'] = colorGrading
            modelCameraInfo = envSect.openSection('ModelCamera')
            if modelCameraInfo:
                modelId = modelCameraInfo.readInt('id')
                pos = tuple([ float(x) for x in modelCameraInfo.readString('pos').split(',') ])
                yaw = modelCameraInfo.readFloat('yaw')
                action = modelCameraInfo.readString('act')
                strscale = modelCameraInfo.readString('scale')
                isHideModelCamera = modelCameraInfo.readInt('isHideModelCamera', 0)
                if strscale != None and strscale.strip() != '':
                    scale = tuple([ float(x) for x in strscale.split(',') ])
                else:
                    scale = (1, 1, 1)
                self.envEvent['ModelCamera'] = (modelId,
                 pos,
                 yaw,
                 action,
                 scale,
                 isHideModelCamera)
            magnitude = envSect.readString('magnitude')
            if magnitude:
                self.envEvent['magnitude'] = [ float(x) for x in magnitude.split(',') ]
            renderMode = envSect.readInt('renderMode', -1)
            if renderMode >= 0:
                self.envEvent['renderMode'] = renderMode
        self.cameraInfo = None
        camSect = timeSect.openSection('Camera')
        if camSect:
            params = camSect.readString('Param')
            if len(params) > 0:
                self.cameraInfo = [ float(x) for x in params.split(',') ]
            self.cameraInfo[9] = int(self.cameraInfo[9])
            self.newCamTrack = camSect.readBool('NewTrack')
            self.fillCamera = camSect.readBool('FillCamera')

    def preLoadRes(self):
        if self.envEvent.has_key('ModelCamera'):
            modelId = self.envEvent['ModelCamera'][0]
            modelPath = 'item/model/' + str(modelId) + '/' + str(modelId) + '.model'
            gCameraCounter.modelPath = modelPath
            gCameraCounter.actions.append(self.envEvent['ModelCamera'][3])

    def play(self, actorDict = None, usePlayerCamera = 0, success = True):
        gamelog.debug('@szh Event.play', self.time)
        if actorDict is not None:
            for name, actList in self.actorEvent.iteritems():
                if not actorDict.has_key(name):
                    continue
                actor = actorDict[name]
                gamelog.debug('@szh: actor player', name, actList)
                if 'born' in [ x[0] for x in actList ]:
                    actor.born()
                for action, args in actList:
                    if action == 'speak':
                        actor.speak(args)
                    elif action == 'act' and success:
                        actor.playAction(args)
                    elif action == 'act1' and not success:
                        actor.playAction(args)
                    elif action == 'emotion' and success:
                        actor.emotionSuperpose(args)
                    elif action == 'effect':
                        args = [ x.strip() for x in args.split(',') ]
                        actor.playEffect(*args)
                    elif action == 'hide':
                        flag = args == '1'
                        actor.hideActor(flag)
                    elif action == 'yaw':
                        actor.refreshYaw(float(args))
                    elif action == 'lookAt':
                        actor.setLookAt(args)
                    elif action == 'run':
                        args = [ float(x) for x in args.split(',') ]
                        actor.run(*args)
                    elif action == 'upWing':
                        args = [ x.strip() for x in args.split(',') ]
                        actor.upWing(*args)
                    elif action == 'upZaiju':
                        args = [ x.strip() for x in args.split(',') ]
                        actor.upZaiju(*args)
                    elif action == 'downWing':
                        actor.downWing()
                    elif action == 'downZaiju':
                        actor.downZaiju()
                    elif action == 'showBigEmote':
                        actor.showBigEmote(args)
                    elif action == 'transpare':
                        actor.addTranspare(args)
                    elif action == 'upWeapon':
                        args = [ x.strip() for x in args.split(',') ]
                        actor.upWeapon(*args)
                    elif action == 'switchWeapon':
                        actor.switchWeapon(*args.split(','))
                    elif action == 'wingAction':
                        actor.playWingAction(args)

        if self.envEvent.has_key('Effect'):
            for (effectId, pos), (roll, yaw, pitch, duration) in self.envEvent['Effect'].iteritems():
                dummyModel = sfx.getDummyModel()
                self.envDummyModels.append(dummyModel)
                roll = roll * math.pi / 180
                yaw = yaw * math.pi / 180
                pitch = pitch * math.pi / 180
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, [gameglobal.EFFECT_HIGH,
                 gameglobal.EFF_DEFAULT_PRIORITY,
                 dummyModel,
                 effectId,
                 sfx.EFFECT_UNLIMIT,
                 pos,
                 roll,
                 yaw,
                 pitch,
                 duration])
                if duration > 0:
                    self.hEffCB.append(BigWorld.callback(duration, Functor(self._releaseModel, dummyModel)))

        if self.envEvent.has_key('Model'):
            player = BigWorld.player()
            envModelEvent = self.envEvent['Model']
            for (modelId, pos), (model, roll, yaw, pitch, duration) in envModelEvent.iteritems():
                if model is None:
                    if int(modelId) <= 10010:
                        modelPath = 'char/%s/base.model' % modelId
                    else:
                        modelPath = 'char/' + str(modelId) + '/' + str(modelId) + '.model'
                charRes.getSimpleModel(modelPath, None, Functor(self._afterModelFinished, pitch, yaw, roll, duration, pos, player, modelId, envModelEvent))

        if self.envEvent.has_key('hideModel'):
            hideEvent = self.envEvent['hideModel']
            for (modelId, pos), (hideModel, whenBorn) in hideEvent.iteritems():
                key = (whenBorn, modelId, pos)
                if gModelPool.has_key(key):
                    model = gModelPool[key]
                    if model.inWorld:
                        model.visible = not hideModel

        if self.envEvent.get('Msg', None) and not usePlayerCamera:
            for coord in self.envEvent['Msg']:
                msgInfo = self.envEvent['Msg'][coord]
                v = Verse(msgInfo[4])
                if not gameglobal.rds.configData.get('disableCUIFont', False):
                    v.show(msgInfo[0], coord, msgInfo[1], msgInfo[2], msgInfo[3], msgInfo[5], msgInfo[6])
                else:
                    v.show('', coord, msgInfo[1], msgInfo[2], msgInfo[3], msgInfo[5], msgInfo[6])
                    msgInfo = (msgInfo[0],
                     msgInfo[1],
                     msgInfo[2],
                     msgInfo[3] + 10,
                     0,
                     0,
                     not msgInfo[6])
                    gameglobal.rds.ui.perFontText.hide()
                    gameglobal.rds.ui.perFontText.show((coord,) + msgInfo)
                self.envMsgs.append(v)

        if self.envEvent.get('GUIMsg', None):
            msgInfo = self.envEvent['GUIMsg']
            for coord, info in msgInfo.iteritems():
                gameglobal.rds.ui.perFontText.show((coord,) + info)

        if self.envEvent.has_key('Dye'):
            dyeInfo = self.envEvent['Dye']
            self._endDye()
            BigWorld.beginGrayFilter(dyeInfo[1])
            BigWorld.grayMask(*dyeInfo[0])
            self.hDyeCB = BigWorld.callback(dyeInfo[2], self._endDye)
        if self.envEvent.has_key('Dof'):
            dofInfo = self.envEvent['Dof']
            if not appSetting.VideoQualitySettingObj.isDofForceEnable():
                BigWorld.enableU3DOF(True)
            BigWorld.setDepthOfField(True, dofInfo[0], 1.0 / dofInfo[1], 1, dofInfo[2], dofInfo[2])
        if self.envEvent.has_key('Blur'):
            blurInfo = self.envEvent['Blur']
            BigWorld.motionBlurFilter(None, 0, blurInfo[0], blurInfo[1])
        if self.envEvent.has_key('Weather'):
            weather = self.envEvent['Weather']
            BigWorld.setZonePriority(weather[0], weather[1])
        if self.envEvent.has_key('Fade'):
            if len(self.envEvent['Fade']) == 3:
                fadeInT, duration, fadeOutT = self.envEvent['Fade']
                isWhite = False
            else:
                fadeInT, duration, fadeOutT, isWhite = self.envEvent['Fade']
            fade(fadeInT, duration, fadeOutT, isWhite)
        if self.envEvent.has_key('Fx'):
            for fxPath in self.envEvent['Fx']:
                fxData = fxPath.split(',')
                fxPath = fxData[0]
                fxLeftTime = len(fxData) == 2 and float(fxData[1]) or 0.0
                handle = gameglobal.rds.sound.playFx(fxPath, BigWorld.player().position, True, BigWorld.player())
                if handle:
                    if fxLeftTime:
                        gfxHandle.append((handle, fxLeftTime))
                    else:
                        gfxHandle.append(handle)

        if self.envEvent.has_key('Voice'):
            for vociePath in self.envEvent['Voice']:
                voiceData = vociePath.split(',')
                voicePath = voiceData[0]
                voiceLeftTime = len(voiceData) == 2 and float(voiceData[1]) or 0.0
                handle = Sound.playRawfile(voicePath)
                if handle:
                    if voiceLeftTime:
                        gVoiceHandle.append((handle, voiceLeftTime))
                    else:
                        gVoiceHandle.append(handle)

        if self.envEvent.has_key('projection'):
            nearPlane, fov = self.envEvent['projection']
            BigWorld.projection().nearPlane = nearPlane
            BigWorld.projection().fov = fov
        self.playColorGrading()
        if self.envEvent.has_key('Sway') and gameglobal.ENABLE_SHAKE_CAMERA:
            cam = BigWorld.camera()
            if isinstance(cam, BigWorld.TrackCamera):
                info = self.envEvent['Sway']
                cam.sway(info[0], (info[2], info[3], info[4]), info[1])
        if self.envEvent.has_key('ScreenEff'):
            for info in self.envEvent['ScreenEff']:
                gamelog.debug('bgf:playScreenEff0', info)
                self.playScreenEff(*info)

        if self.envEvent.has_key('Plate'):
            self.playPlate()
        if self.envEvent.has_key('cg'):
            self.playMovie()
        if self.envEvent.has_key('questMsg'):
            gameglobal.rds.ui.autoQuest.show(*self.envEvent['questMsg'])
        if self.envEvent.has_key('swf'):
            self.playSwf()
        if self.envEvent.has_key('screenEffect'):
            self.playScreenEffect()
        if self.envEvent.has_key('bgMusic'):
            switchSound(self.envEvent['bgMusic'][1:])
        if self.envEvent.has_key('ModelCamera'):
            modelId, pos, yaw, actionName, scale, isHideModelCamera = self.envEvent['ModelCamera']
            model = gCameraCounter.model
            model.position = pos
            model.yaw = yaw
            model.scale = scale
            if not isHideModelCamera:
                self.showModelCamera(model)
            BigWorld.enableMultiThreadAnim(False)
            if hasattr(BigWorld, 'setCameraAnimModel'):
                BigWorld.setCameraAnimModel(model)
            model.action(actionName)(0)
        if self.envEvent.has_key('presetCC'):
            model = gCameraCounter.model
            self.showModelCamera(model)
        if self.envEvent.has_key('magnitude'):
            self.playMagnitude(*self.envEvent['magnitude'])
        if self.envEvent.has_key('renderMode'):
            self.setRenderMode(self.envEvent['renderMode'])

    def showModelCamera(self, model):
        CC.newFree()
        CC.TC.invViewProvider = model.node('camBone')

    def _afterModelFinished(self, pitch, yaw, roll, duration, pos, player, modelId, envModelEvent, model):
        if not model.inWorld:
            player.addModel(model)
        gamelog.debug('@szh: env model', modelId, pos, pitch, yaw, roll)
        model.position = pos
        model.pitch = pitch * math.pi / 180
        model.yaw = yaw * math.pi / 180
        model.roll = roll * math.pi / 180
        envModelEvent[modelId, pos] = (model,
         roll,
         yaw,
         pitch,
         duration)
        gModelPool[self.time, modelId, pos] = model
        if duration > 0:
            self.hEffCB.append(BigWorld.callback(duration, Functor(self._releaseModel, model)))

    def release(self):
        for h in self.hEffCB:
            BigWorld.cancelCallback(h)

        self.hEffCB = []
        player = BigWorld.player()
        self.envDummyModels = []
        if self.envEvent.has_key('Model'):
            envModelEvent = self.envEvent['Model']
            for modelKey in envModelEvent:
                model, duration, pitch, yaw, roll = envModelEvent[modelKey]
                if model and model.inWorld:
                    player.delModel(model)
                envModelEvent[modelKey] = (None,
                 duration,
                 pitch,
                 yaw,
                 roll)

        self._endDye()
        for m in self.envMsgs:
            m.release()

        self.envMsgs = []
        if self.envEvent.has_key('Plate'):
            gameglobal.rds.ui.scenarioPlate.closeScenarioPlate()
        if self.cgPlayer:
            self.cgPlayer.endMovie()
        if self.envEvent.has_key('Dof'):
            BigWorld.setDepthOfField(False)
            if not appSetting.VideoQualitySettingObj.isDofForceEnable():
                BigWorld.enableU3DOF(False)
        if self.envEvent.has_key('Weather'):
            BigWorld.setZonePriority(self.envEvent['Weather'][0], -100)
        if self.envEvent.has_key('magnitude'):
            self.playMagnitude(1, 0)
        if self.envEvent.has_key('renderMode'):
            self.setRenderMode(None)

    def _releaseModel(self, model):
        if model is None:
            return
        if model in self.envDummyModels:
            self.envDummyModels.remove(model)
            sfx.giveBackDummyModel(model)
        elif model.inWorld:
            BigWorld.player().delModel(model)

    def _endDye(self):
        if self.hDyeCB is None:
            return
        BigWorld.endGrayFilter(0.1)
        BigWorld.cancelCallback(self.hDyeCB)
        self.hDyeCB = None

    def addEnvEff(self, effectId, pos, roll, yaw, pitch, duration):
        if not self.envEvent.has_key('Effect'):
            self.envEvent['Effect'] = {}
        effectKey = (effectId, pos)
        self.envEvent['Effect'][effectKey] = (roll,
         yaw,
         pitch,
         duration)

    def addEnvDof(self, dofFocus = 10, dofRadius = 50, dofExp = 1, nearMaxBlur = 1, farMaxBlur = 1, minBlur = 0):
        if not self.envEvent.has_key('newDof'):
            self.envEvent['newDof'] = ()
        self.envEvent['newDof'] = (dofFocus,
         dofRadius,
         dofExp,
         nearMaxBlur,
         farMaxBlur,
         minBlur)

    def addEnvBlur(self, blurTime, blurScale):
        if not self.envEvent.has_key('Blur'):
            self.envEvent['Blur'] = []
        self.envEvent['Blur'] = [blurTime, blurScale]

    def addEnvWeather(self, zoneName, targetWeight):
        if not self.envEvent.has_key('Weather'):
            self.envEvent['Weather'] = []
        self.envEvent['Weather'] = [zoneName, targetWeight]

    def delEnvEff(self, effectId, pos):
        effectKey = (effectId, pos)
        if self.envEvent.has_key('Effect'):
            if effectKey in self.envEvent['Effect']:
                del self.envEvent['Effect'][effectKey]
            if len(self.envEvent['Effect']) == 0:
                del self.envEvent['Effect']

    def addEnvModel(self, modelId, pos, duration = 0.0, pitch = 0.0, yaw = 0.0, roll = 0.0):
        if not self.envEvent.has_key('Model'):
            self.envEvent['Model'] = {}
        modelKey = (modelId, pos)
        if modelKey not in self.envEvent['Model']:
            self.envEvent['Model'][modelKey] = (None,
             roll,
             yaw,
             pitch,
             duration)

    def delEnvModel(self, modelId, pos):
        modelKey = (modelId, pos)
        if self.envEvent.has_key('Model'):
            if modelKey in self.envEvent['Model']:
                self._releaseModel(self.envEvent['Model'][modelKey][0])
                del self.envEvent['Model'][modelKey]
            if len(self.envEvent['Model']) == 0:
                del self.envEvent['Model']

    def addEnvDye(self, color, fadeTime, duration):
        red = (color & 16711680) >> 16
        green = (color & 65280) >> 8
        blue = color & 255
        color = (red / 255.0, green / 255.0, blue / 255.0)
        self.envEvent['Dye'] = (color, fadeTime, duration)

    def delEnvDye(self):
        if self.envEvent.has_key('Dye'):
            del self.envEvent['Dye']

    def addEnvFade(self, fadeInT, duration, fadeOutT, isWhite = 0):
        self.envEvent['Fade'] = (fadeInT,
         duration,
         fadeOutT,
         isWhite)

    def delEnvFade(self):
        if self.envEvent.has_key('Fade'):
            del self.envEvent['Fade']

    def addCamera(self, isNewTrack = False, duration = 1.0, isFillCamera = False):
        CC.record()
        tc = CC.TC
        if not tc:
            return
        cameraArgs = list(tc.getKey(tc.getKeyCount() - 1))[:10]
        cameraArgs[8] = duration
        self.cameraInfo = list(cameraArgs)
        self.newCamTrack = isNewTrack
        self.fillCamera = isFillCamera

    def delCamera(self):
        self.cameraInfo = None

    def addFx(self, fxPath, time = None):
        if not self.envEvent.has_key('Fx'):
            self.envEvent['Fx'] = []
        self.envEvent['Fx'].append(fxPath)

    def delFx(self, fxPath):
        if fxPath in self.envEvent['Fx']:
            self.envEvent['Fx'].remove(fxPath)

    def addVoice(self, voicePath, time = None):
        if not self.envEvent.has_key('Voice'):
            self.envEvent['Voice'] = []
        self.envEvent['Voice'].append(voicePath)

    def delVoice(self, voicePath):
        if voicePath in self.envEvent['Voice']:
            self.envEvent['Voice'].remove(voicePath)

    def moveCamera(self):
        if self.cameraInfo:
            CC.moveCamera(self.cameraInfo)

    def getCameraFov(self):
        if self.cameraInfo:
            return self.cameraInfo[7]
        else:
            return None

    def addSway(self, hz, time, ampX, ampY, ampZ):
        self.envEvent['Sway'] = [hz,
         time,
         ampX,
         ampY,
         ampZ]

    def delSway(self):
        if self.envEvent['Sway']:
            self.envEvent['Sway'] = None
            del self.envEvent['Sway']

    def addScreenEff(self, effId, time = None):
        if not self.envEvent.has_key('ScreenEff'):
            self.envEvent['ScreenEff'] = []
        self.envEvent['ScreenEff'].append(time == None and [effId] or [effId, time])

    def delScreenEff(self, effId):
        for eff in self.envEvent['ScreenEff']:
            if eff[0] == effId:
                self.envEvent['ScreenEff'].remove(eff)

    def playScreenEff(self, effId, time = None):
        gamelog.debug('bgf:playScreenEff1', effId, time)
        if int(effId) == 1:
            screenRipple.rippleScreen()
        elif int(effId) == 2:
            screenRipple.start()
            BigWorld.callback(time, screenRipple.stop)

    def addHideModel(self, modelId, pos, isHide, whenBorn):
        if not self.envEvent.has_key('hideModel'):
            self.envEvent['hideModel'] = {}
        self.envEvent['hideModel'][modelId, pos] = (isHide, whenBorn)

    def delHideModel(self, modelId, pos):
        key = (modelId, pos)
        if self.envEvent['hideModel'].has_key(key):
            self.envEvent['hideModel'][modelId, pos] = None
            del self.envEvent['hideModel'][modelId, pos]

    def addEnvMsg(self, msg, coord, color, duration, size, filmEffect, fontName, midSet):
        if not self.envEvent.has_key('Msg'):
            self.envEvent['Msg'] = {}
        self.envEvent['Msg'][coord] = (msg,
         color,
         duration,
         size,
         filmEffect,
         fontName,
         midSet)

    def addEnvGUIMsg(self, coord, msg, color, duration, size, frame, blackGround, notMid):
        if not self.envEvent.has_key('GUIMsg'):
            self.envEvent['GUIMsg'] = {}
        self.envEvent['GUIMsg'][coord] = (msg,
         color,
         duration,
         size,
         frame,
         blackGround,
         notMid)

    def delEnvGUIMsg(self, coord):
        if self.envEvent.has_key('GUIMsg'):
            if coord in self.envEvent['GUIMsg']:
                del self.envEvent['GUIMsg'][coord]
            if len(self.envEvent['GUIMsg']) == 0:
                del self.envEvent['GUIMsg']

    def addMagnitude(self, magnitude, fadeIn):
        self.envEvent['magnitude'] = [magnitude, fadeIn]

    def delMagnitude(self):
        if self.envEvent.has_key('magnitude'):
            self.envEvent.pop('magnitude', None)

    def playMagnitude(self, magnitude, fadeIn):
        BigWorld.setParticleFrameRateMagnitude(magnitude, fadeIn)
        BigWorld.setActionFrameRateMagnitude(magnitude, fadeIn)

    def addQuestMsg(self, msg, npcId, duration):
        self.envEvent['questMsg'] = (msg, npcId, duration)

    def delQuestMsg(self):
        self.envEvent.pop('questMsg', None)

    def addRenderMode(self, index):
        self.envEvent['renderMode'] = index

    def delRenderMode(self):
        self.envEvent.pop('renderMode', None)

    def setRenderMode(self, index):
        appSetting.setShaderIndex(index, False, True)

    def delEnvMsg(self, coord):
        if self.envEvent.has_key('Msg'):
            if coord in self.envEvent['Msg']:
                del self.envEvent['Msg'][coord]
            if len(self.envEvent['Msg']) == 0:
                del self.envEvent['Msg']

    def addBgMusic(self, bgMusicPath, enableMusic, enableFx, enableStatic, enableAmbient):
        self.envEvent['bgMusic'] = [bgMusicPath,
         enableMusic,
         enableFx,
         enableStatic,
         enableAmbient]

    def addProjection(self, nearPlane, fov):
        self.envEvent['projection'] = [nearPlane, fov]

    def addColorGrading(self, tgaPath):
        self.envEvent['colorGrading'] = tgaPath

    def delColorGrading(self):
        if self.envEvent.has_key('colorGrading'):
            self.envEvent['colorGrading'] = None
            del self.envEvent['colorGrading']

    def playColorGrading(self):
        global gChangeColorGrading
        if self.envEvent.has_key('colorGrading'):
            tgaPath = self.envEvent['colorGrading']
            if tgaPath == 'restore':
                tgaPath = ''
                gChangeColorGrading = False
            else:
                gChangeColorGrading = True
            BigWorld.setColorGrading(tgaPath, 1)

    def delBgMusic(self):
        if self.envEvent['bgMusic']:
            self.envEvent['bgMusic'] = None
            del self.envEvent['bgMusic']

    def delProjection(self):
        if self.envEvent['projection']:
            del self.envEvent['projection']

    def delEnvDof(self):
        if self.envEvent['Dof']:
            del self.envEvent['Dof']

    def delEnvBlur(self):
        if self.envEvent['Blur']:
            del self.envEvent['Blur']

    def delEnvWeather(self):
        if self.envEvent['Weather']:
            del self.envEvent['Weather']

    def addPlate(self, path, leftX, rightX, topY, bottomY, time, array, smallPath = '', smallLeftX = 0, smallTopY = 0):
        self.envEvent['Plate'] = dataDict = {}
        dataDict['path'] = path
        dataDict['leftX'] = leftX
        dataDict['rightX'] = rightX
        dataDict['topY'] = topY
        dataDict['bottomY'] = bottomY
        dataDict['totalTime'] = time
        dataDict['transform'] = array
        dataDict['smallPath'] = smallPath
        dataDict['smallLeftX'] = smallLeftX
        dataDict['smallTopY'] = smallTopY

    def delPlate(self):
        if self.envEvent['Plate']:
            self.envEvent['Plate'] = None
            del self.envEvent['Plate']

    def playPlate(self):
        scenarioPlate = gameglobal.rds.ui.scenarioPlate
        dataDict = self.envEvent['Plate']
        scenarioPlate.initData(dataDict['path'], dataDict['leftX'], dataDict['rightX'], dataDict['topY'], dataDict['bottomY'], dataDict['totalTime'], dataDict['transform'], dataDict['smallPath'], dataDict['smallLeftX'], dataDict['smallTopY'])
        scenarioPlate.show()

    def addMovie(self, cgName):
        self.envEvent['cg'] = cgName

    def playMovie(self):
        cgName = self.envEvent.get('cg', None)
        if cgName:
            config = {'position': (0, 0, 0),
             'w': 2,
             'h': 2,
             'loop': False}
            if self.cgPlayer:
                self.cgPlayer.endMovie()
            self.cgPlayer = cgPlayer.CGPlayer()
            self.cgPlayer.playMovie(cgName, config)

    def delMovie(self):
        if self.envEvent['cg']:
            self.envEvent['cg'] = None
            del self.envEvent['cg']

    def addSwf(self, swfName, time):
        self.envEvent['swf'] = (swfName, time)

    def playSwf(self):
        scenarioPlate = gameglobal.rds.ui.scenarioPlate
        scenarioPlate.initSwfData(*self.envEvent['swf'])
        scenarioPlate.show()

    def delSwf(self):
        if self.envEvent['swf']:
            self.envEvent['swf'] = None
            del self.envEvent['swf']

    def addScreenEffect(self, path, time, fadein, fadeout):
        self.envEvent['screenEffect'] = (path,
         time,
         fadein,
         fadeout)

    def delScreenEffect(self):
        if self.envEvent['screenEffect']:
            self.envEvent['screenEffect'] = None
            del self.envEvent['screenEffect']

    def playScreenEffect(self):
        path, time, fadein, fadeout = self.envEvent['screenEffect']
        screenEffect.startEffectByPath(gameglobal.EFFECT_TAG_STORY_EDIT, -1, time, 'effect/screen/' + path, fadein, fadeout)

    def addModelCamera(self, modelId, pos, yaw, action, scale, isHideModelCamera):
        self.envEvent['ModelCamera'] = (modelId,
         pos,
         yaw,
         action,
         scale,
         isHideModelCamera)

    def addPresetCC(self, presetCC):
        self.envEvent['presetCC'] = int(presetCC)

    def delModelCamera(self):
        if self.envEvent.has_key('ModelCamera'):
            self.envEvent['ModelCamera'] = None
            del self.envEvent['ModelCamera']

    def checkTutorialEvent(self):
        if self.envEvent.has_key('tutorialEvent'):
            return True
        return False

    def checkHaveTutorial(self):
        if self.envEvent.has_key('tutorialEvent'):
            return self.envEvent['tutorialEvent'][1]
        return 0

    def addTutorialEvent(self, callback, hasTutorial):
        self.envEvent['tutorialEvent'] = (callback, hasTutorial)

    def playTutorialEvent(self):
        if self.envEvent.has_key('tutorialEvent'):
            callback = self.envEvent['tutorialEvent'][0]
            callback()


def getWordGUI(word, size, font, color = 4294967295L):
    wordGUI = GUI.Simple('')
    wordGUI.materialFX = 'BLEND'
    wordGUI.filterType = 'LINEAR'
    wordGUI.widthRelative = False
    wordGUI.heightRelative = False
    wordGUI.positionRelative = False
    wordGUI.verticalAnchor = 'TOP'
    wordGUI.position[2] = 0.1
    b = color & 255
    g = color >> 8 & 255
    r = color >> 16 & 255
    a = 255
    wordGUI.colour = (r,
     g,
     b,
     a)
    wordGUI.size = (size, size * 2)
    pTex = BigWorld.PyTextureProvider('')
    pTex.fillText(word, int(wordGUI.width), int(wordGUI.height), font)
    wordGUI.texture = pTex
    return wordGUI


class Verse(object):

    def __init__(self, filmEffect):
        self.alphaShader = GUI.AlphaShader('ALL')
        self.scaleShader = GUI.MatrixShader()
        self.scaleMat = Math.Matrix()
        self.scaleShader.target = self.scaleMat
        if filmEffect == FILM_EFFECT_BLACK:
            self.bkg = GUI.Simple(PATH_NAME + 'widescreenmask.dds')
        else:
            self.bkg = GUI.Simple('')
        self.filmEffect = filmEffect
        self.bkg.materialFX = 'BLEND'
        self.bkg.filterType = 'LINEAR'
        self.bkg.visible = False
        self.bkg.widthRelative = False
        self.bkg.heightRelative = False
        self.bkg.positionRelative = True
        self.bkg.size = (0, 0)
        self.bkg.position[2] = 0.1
        self.relCoord = (0, 0)
        self.hCB = None
        self.wordSize = 40
        self.font = None
        self.cameraMask = None

    def release(self):
        self.reset()
        self.bkg.delShader(self.scaleShader)
        self.bkg.delShader(self.alphaShader)

    def reset(self):
        for c in self.bkg.children:
            self.bkg.delChild(c[0])

        self.bkg.visible = False
        GUI.delRoot(self.bkg)
        if self.hCB:
            BigWorld.cancelCallback(self.hCB)
            self.hCB = None
        self.font = None
        if self.cameraMask:
            self.cameraMask.release()
            self.cameraMask = None

    def show(self, words, relCoord, color = 4294967295L, duration = -1, size = None, fontName = 'Î¢ÈíÑÅºÚ', midSet = 0):
        self.reset()
        len_words = len(words)
        self.wordSize = size
        self.font = C_ui.font(fontName, self.wordSize, -800, 0, 0, 0, 0.0, 0)
        idx = 0
        while idx < len_words:
            if ord(words[idx]) >= 128:
                w = words[idx:idx + 2]
                idx += 2
            else:
                w = words[idx]
                idx += 1
            word_gui = getWordGUI(w, self.wordSize, self.font, color)
            self.bkg.addChild(word_gui)

        self.bkg.size = (self.wordSize, self.wordSize * len(self.bkg.children))
        if not hasattr(self.bkg, 'scaleShader'):
            self.bkg.addShader(self.scaleShader, 'scaleShader')
        if not hasattr(self.bkg, 'alphaShader'):
            self.bkg.addShader(self.alphaShader, 'alphaShader')
        if self.filmEffect == FILM_EFFECT_BLACK:
            screenWidth = BigWorld.screenWidth()
            screenHeight = BigWorld.screenHeight()
            self.bkg.width = screenWidth
            self.bkg.height = screenHeight
            self.bkg.colour = (0, 0, 0, 255)
        elif self.filmEffect == FILM_EFFECT_MASK:
            self.cameraMask = CameraMask()
            self.cameraMask.fadeIn(0.3)
        elif self.filmEffect == FILM_EFFECT_MONOSPACE_MASK:
            self.cameraMask = CameraMask(MONOSPACE_ANCHOR_CONFIG)
            self.cameraMask.fadeIn(0.3)
        self.scale()
        self.arrange(words, relCoord, midSet)
        self.bkg.visible = True
        GUI.addRoot(self.bkg)
        self.alphaShader.speed = 0
        self.alphaShader.alpha = 0
        self.alphaShader.reset()
        self.alphaShader.speed = 0.3
        self.alphaShader.alpha = 1
        if duration > 0:
            self.hCB = BigWorld.callback(duration, self.fadeOut)

    def fadeOut(self, duration = 0.3):
        self.alphaShader.speed = duration
        self.alphaShader.alpha = 0
        if self.hCB:
            BigWorld.cancelCallback(self.hCB)
        self.hCB = BigWorld.callback(duration, self.release)
        if self.filmEffect and self.cameraMask:
            self.cameraMask.fadeOut(0.3)

    def scale(self):
        screenSize = BigWorld.screenSize()
        multiple = min(screenSize[0] / 800.0, screenSize[1] / 600.0)
        self.scaleMat.setScale((multiple, multiple, 0))

    def arrange(self, words, relCoord = None, midSet = False):
        if relCoord is None:
            relCoord = self.relCoord
        scrSize = (800, 600)
        coord = (round(scrSize[0] * relCoord[0]), -round(scrSize[1] * relCoord[1]))
        l = len(words)
        idx = 0
        i = 0
        x_offset = 0
        wordWidth = 0
        while idx < l:
            if ord(words[idx]) >= 128:
                idx += 2
                wordWidth = self.wordSize
            else:
                idx += 1
                wordWidth = int(self.wordSize / 2)
            c = self.bkg.children[i][1]
            c.position[0] = coord[0] + x_offset
            c.position[1] = coord[1]
            x_offset += wordWidth
            i += 1

        x_offset += wordWidth + 1
        if midSet:
            x_offset = -x_offset / 2.0 / self.scaleMat.scale[0] - coord[0]
            for c in self.bkg.children:
                c[1].position[0] += x_offset


class CameraMask(object):
    WIDTH = 1280
    HEIGHT = 128

    def __init__(self, anchorConfig = ANCHOR_CONFIG):
        self.black = []
        for i in xrange(2):
            black = GUI.Simple(anchorConfig[i][2])
            black.materialFX = 'BLEND'
            black.verticalAnchor = anchorConfig[i][0]
            black.height = anchorConfig[i][3]
            black.width = 2.02
            black.position = Math.Vector3(0, anchorConfig[i][1], 0.1)
            black.visible = True
            self.black.append(black)
            black.shader = GUI.AlphaShader('ALL')
            black.shader.reset()

        if gCanEsc:
            black = GUI.Simple(PATH_NAME + 'esc.dds')
            black.materialFX = 'BLEND'
            black.verticalAnchor = 'TOP'
            black.horizontalAnchor = 'LEFT'
            black.positionRelative = False
            sWidth, sHeight = BigWorld.screenSize()
            black.position = Math.Vector3(-sWidth / 2 + 18, sHeight / 2 - 10, 0.05)
            black.visible = True
            self.black.append(black)
            black.widthRelative = black.heightRelative = False
            black.width = 58
            black.height = 20
            gamelog.debug('black', black.width, black.height)
            black.shader = GUI.AlphaShader('ALL')
            black.shader.reset()
        self.addedToGUI = False
        self.callback_handle = None

    def release(self):
        for i in self.black:
            i.visible = False

        if self.addedToGUI:
            for i in self.black:
                GUI.delRoot(i)

            self.addedToGUI = False
        if self.callback_handle:
            BigWorld.cancelCallback(self.callback_handle)
            self.callback_handle = None

    def fadeIn(self, t = 1):
        for i in self.black:
            i.visible = True
            i.shader.speed = t
            i.shader.alpha = 0
            i.shader.reset()
            i.shader.alpha = 1

        if not self.addedToGUI:
            for i in self.black:
                GUI.addRoot(i)

            self.addedToGUI = True
        if self.callback_handle:
            BigWorld.cancelCallback(self.callback_handle)
            self.callback_handle = None

    def fadeOut(self, t = 1):
        for i in self.black:
            i.shader.speed = t
            i.shader.alpha = 1
            i.shader.reset()
            i.shader.alpha = 0
