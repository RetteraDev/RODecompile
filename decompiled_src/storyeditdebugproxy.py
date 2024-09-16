#Embedded file name: /WORKSPACE/data/entities/client/debug/storyeditdebugproxy.o
import os
import ResMgr
import Math
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gamelog
from guis.ui import gbk2unicode
from guis.ui import unicode2gbk
from helpers import scenario
from guis.uiProxy import DataProxy
from guis import uiConst
from guis import uiUtils
import clientUtils
from data import npc_model_client_data
EXIST_PATH = 'res/intro/scenario/'

class StoryEditDebugProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(StoryEditDebugProxy, self).__init__(uiAdapter)
        self.bindType = 'storyEditDebug'
        self.modelMap = {'chooseFrame': self.chooseFrame,
         'chooseStory': self.chooseStory,
         'chooseData': self.chooseData,
         'fileControl': self.fileControl,
         'cameraControl': self.cameraControl,
         'frameControl': self.frameControl,
         'sceneControl': self.sceneControl,
         'roleControl': self.roleControl,
         'anotherControl': self.anotherControl,
         'changeFov': self.changeFov,
         'register': self.onRegister,
         'registerStory': self.onRegisterStory,
         'onConfirm': self.onConfirm,
         'onCancel': self.onCancel,
         'registerRole': self.onRegisterRole,
         'chooseRoleData': self.chooseRoleData,
         'editRoleContol': self.editRoleContol,
         'changeFov': self.onChangeFov,
         'usePlayerCamera': self.usePlayerCamera,
         'presetCamera': self.presetCamera,
         'searchStoryName': self.onSearchStoryName,
         'searchNpcId': self.onSearchNpcId,
         'getRunDist': self.onGetRunDist,
         'getRunInfo': self.onGetRunInfo,
         'getPosition': self.onGetPosition}
        self.pathPrefix = None
        self.storyList = []
        self.frameList = []
        self.dataList = []
        self.modelList = []
        self.roleList = []
        self.ins = scenario.Scenario.getInstance()
        self.storyName = None
        self.stamp = None
        self.cameraIsOpen = False
        self.frameMC = None
        self.storyMC = None
        self.roleMC = None
        self.emFlag = None
        self.emId = None
        self.emPos = None
        self.npcEnt = None
        self.npcDataIndex = None
        self.roleEditIndex = None
        self.oldFov = None
        self.isShow = False
        self.checkBoxMap = {'playerCheckBox': self._usePlayerCamera,
         'hideNPCCheckBox': self._hideNPC,
         'hideMovingPlatCheckBox': self._hideMovingPlat,
         'hideAvatarCheckBox': self._hideAvatar,
         'hidePlayerCheckBox': self._hidePlayer,
         'hideMonsterCheckBox': self._hideMonster,
         'canEscCheckBox': self._canEsc,
         'passFadeCheckBox': self._passFade,
         'hideBoxCheckBox': self._hideTreasureBox,
         'hideAvatarExcludeTeamCheckBox': self._hideAvatarExcludeTeam,
         'hideEntityTopLogo': self._hideEntityTopLogo,
         'hideTransport': self._hideTransport}

    def onRegister(self, *arg):
        self.frameMC = arg[3][0]

    def onRegisterStory(self, *arg):
        self.storyMC = arg[3][0]
        self.isShow = True

    def onRegisterRole(self, *arg):
        self.roleMC = arg[3][0]

    def chooseFrame(self, *arg):
        self.stamp = float(arg[3][0].GetString())
        self.storyMC.Invoke('setData', self.getDataArray())
        event = self.ins.eventMgr.getEvent(self.stamp)
        self.storyMC.Invoke('setNewPath', GfxValue(str(event.newCamTrack)))
        self.storyMC.Invoke('setFillCamera', GfxValue(str(event.fillCamera)))

    def changeFov(self, *arg):
        pass

    def chooseStory(self, *arg):
        self.storyName = arg[3][0].GetString()
        gamelog.debug('bgf:storryEdit', self.storyName)
        self.ins.release()
        self.ins.loadScript(self.storyName, True)
        self.storyMC.Invoke('setFrameData', self.getFrameArray())
        self.storyMC.Invoke('setPlayerCamera', (GfxValue('playerCheckBox'), GfxValue(self.ins.usePlayerCamera)))
        self.storyMC.Invoke('setPlayerCamera', (GfxValue('hideNPCCheckBox'), GfxValue(self.ins.hideNPC)))
        self.storyMC.Invoke('setPlayerCamera', (GfxValue('hideMovingPlatCheckBox'), GfxValue(self.ins.hideMovingPlat)))
        self.storyMC.Invoke('setPlayerCamera', (GfxValue('hideAvatarCheckBox'), GfxValue(self.ins.hideAvatar)))
        self.storyMC.Invoke('setPlayerCamera', (GfxValue('hidePlayerCheckBox'), GfxValue(self.ins.hidePlayer)))
        self.storyMC.Invoke('setPlayerCamera', (GfxValue('hideMonsterCheckBox'), GfxValue(self.ins.hideMonster)))
        self.storyMC.Invoke('setPlayerCamera', (GfxValue('canEscCheckBox'), GfxValue(self.ins.canEsc)))
        self.storyMC.Invoke('setPlayerCamera', (GfxValue('passFadeCheckBox'), GfxValue(self.ins.passFade)))
        self.storyMC.Invoke('setPlayerCamera', (GfxValue('hideEntityTopLogo'), GfxValue(self.ins.hideEntityTopLogo)))
        self.storyMC.Invoke('setPlayerCamera', (GfxValue('hideTransport'), GfxValue(self.ins.hideTransport)))

    def chooseData(self, *arg):
        index = int(arg[3][0].GetString())
        self.emFlag = self.dataList[index][0]
        self.emId = self.dataList[index][1]
        gamelog.debug('bgf:storyEdit', arg[3][0].GetString(), self.emFlag, self.emId)
        if self.emFlag not in ('npc', 'Fx', 'ScreenEff', 'Plate', 'Voice', 'bgMusic', 'ModelCamera', 'cg', 'Dof'):
            self.emPos = self.dataList[index][2]
        if self.emFlag == 'npc':
            self.npcEnt = self.ins.getActorByName(self.emId)

    def fileControl(self, *arg):
        btnName = arg[3][0].GetString()
        if btnName == 'newBtn':
            self.storyName = arg[3][1].GetString()
            self.ins.release()
            suc = self.ins.loadScript(self.storyName, True)
            if suc:
                self.storyList.append(self.storyName)
                return self.getStoryArray()
        else:
            if btnName == 'clearBtn':
                self.ins.sweep()
                return self.getFrameArray()
            if btnName == 'saveBtn':
                self.ins.saveScript()
                self.storyMC.Invoke('setFrameData', self.getFrameArray())
            elif btnName == 'deleteBtn':
                if not self.pathPrefix:
                    path = os.getcwd()
                    path = path.replace('\\', '/')
                    self.pathPrefix = path[0:path.rfind('/') + 1] + EXIST_PATH
                gamelog.debug('bgf:deltepath', self.pathPrefix, self.storyName)
                if self.storyName:
                    os.remove(self.pathPrefix + self.storyName)
                    self.storyList.remove(self.storyName)
                    self.storyName = None
                    return self.getStoryArray()

    def cameraControl(self, *arg):
        btnName = arg[3][0].GetString()
        p = BigWorld.player()
        if btnName == 'cameraBtn':
            pass
        elif btnName == 'lookCameraBtn':
            if not self.cameraIsOpen:
                self.oldFov = BigWorld.projection().fov
                if self.stamp != None:
                    self.ins.watchCamera(True)
                    p.lockKey(gameglobal.KEY_POS_SCENARIO)
                    self.cameraIsOpen = True
                    if self.stamp != None:
                        event = self.ins.eventMgr.getEvent(self.stamp)
                        event.moveCamera()
                        fov = event.getCameraFov()
                        if fov:
                            gamelog.debug('bgf:fov', fov)
                            self.storyMC.Invoke('setFov', GfxValue(fov))
            else:
                BigWorld.projection().fov = self.oldFov
                if self.stamp != None:
                    self.ins.watchCamera(False)
                    p.unlockKey(gameglobal.KEY_POS_SCENARIO)
                    self.cameraIsOpen = False
        elif btnName == 'setCameraBtn':
            gamelog.debug('bgf:stroyEdit', self.cameraIsOpen)
            if self.cameraIsOpen and self.stamp != None:
                duration = float(arg[3][1].GetString())
                isNewPath = bool(arg[3][2].GetString())
                fov = arg[3][3].GetNumber()
                isFill = bool(arg[3][4].GetString())
                event = self.ins.eventMgr.getEvent(self.stamp)
                event.addCamera(isNewPath, duration, isFill)
                gamelog.debug('bgf:storyEdit', duration, isNewPath, event.time)
        elif btnName == 'newCameraPath':
            pass
        elif btnName == 'delCameraBtn':
            if self.stamp != None:
                event = self.ins.eventMgr.getEvent(self.stamp)
                event.delCamera()

    def frameControl(self, *arg):
        btnName = arg[3][0].GetString()
        if btnName == 'addFrameBtn':
            gamelog.debug('bgf:storyEdit', arg[3][1].GetString())
            strStamp = arg[3][1].GetString()
            if not strStamp:
                return
            self.stamp = float(arg[3][1].GetString())
            self.ins.eventMgr.addEvent(self.stamp)
            return self.getFrameArray()
        if btnName == 'recoveBtn':
            self.ins.reset()
        elif btnName == 'delFrameBtn':
            isSuccess, idx = self.ins.eventMgr.findEventByTime(self.stamp)
            if isSuccess:
                self.ins.eventMgr.delEventByIndex(idx)
                return self.getFrameArray()
        elif btnName == 'reloadBtn':
            gamelog.debug('bgf:reload')
            self.ins.release()
            self.ins.loadScript(self.storyName, True)
            self.storyMC.Invoke('setFrameData', self.getFrameArray())
        elif btnName == 'changeFrameBtn':
            strStamp = arg[3][1].GetString()
            if not strStamp:
                return
            self.ins.eventMgr.changeEventTime(self.stamp, float(strStamp))
            return self.getFrameArray()

    def sceneControl(self, *arg):
        btnName = arg[3][0].GetString()
        gamelog.debug('bgf:storyEdit', btnName)
        strStamp = str(self.stamp)
        if btnName == 'sceneBtn':
            pass
        elif btnName == 'addDofBtn':
            self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))
        elif btnName == 'setCameraBtn':
            self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))
        elif btnName == 'addBlurBtn':
            self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))
        elif btnName == 'addWeatherBtn':
            self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))
        elif btnName == 'addModelBtn':
            if self.stamp != None:
                if self.emFlag == 'Mod':
                    self.frameMC.Invoke('loadModel', (GfxValue('hideModelBtn'), GfxValue(strStamp)))
                else:
                    self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))
                    self.frameMC.Invoke('setModelData', self.getModelArray())
        elif btnName == 'delSceneBtn':
            gamelog.debug('bgf:storyEdit', self.emFlag, self.emId, self.emPos)
            if self.emFlag != None:
                event = self.ins.eventMgr.getEvent(self.stamp)
                if self.emFlag == 'Eff':
                    event.delEnvEff(self.emId, self.emPos)
                elif self.emFlag in ('Mod',):
                    event.delEnvModel(self.emId, self.emPos)
                elif self.emFlag == 'hideMod':
                    event.delHideModel(self.emId, self.emPos)
                elif self.emFlag == 'Dye':
                    event.delEnvDye()
                elif self.emFlag in ('Fade', 'WhiteFade'):
                    event.delEnvFade()
                elif self.emFlag == 'Fx':
                    event.delFx(self.emId)
                elif self.emFlag == 'ScreenEff':
                    event.delScreenEff(self.emId)
                elif self.emFlag == 'Sway':
                    event.delSway()
                elif self.emFlag == 'Msg':
                    event.delEnvMsg(self.emId)
                elif self.emFlag == 'Plate':
                    event.delPlate()
                elif self.emFlag == 'Voice':
                    event.delVoice(self.emId)
                elif self.emFlag == 'bgMusic':
                    event.delBgMusic()
                elif self.emFlag == 'colorGrading':
                    event.delColorGrading()
                elif self.emFlag == 'ModelCamera':
                    event.delModelCamera()
                elif self.emFlag == 'cg':
                    event.delMovie()
                elif self.emFlag == 'swf':
                    event.delSwf()
                elif self.emFlag == 'screenEffect':
                    event.delScreenEffect()
                elif self.emFlag == 'GUIMsg':
                    event.delEnvGUIMsg(self.emId)
                elif self.emFlag == 'Dof':
                    event.delEnvDof()
                elif self.emFlag == 'magnitude':
                    event.delMagnitude()
                elif self.emFlag == 'questMsg':
                    event.delQuestMsg()
                elif self.emFlag == 'renderMode':
                    event.delRenderMode()
                self.emFlag = None
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'timeBtn':
            self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))
        elif self.stamp != None:
            gamelog.debug('bgf:storyEdit', btnName, strStamp)
            self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))

    def roleControl(self, *arg):
        btnName = arg[3][0].GetString()
        strStamp = str(self.stamp)
        if btnName == 'roleBtn':
            pass
        elif btnName == 'newRoleBtn':
            self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))
            self.frameMC.Invoke('setRoleData', self.getRoleArray())
        elif btnName == 'editRoleBtn':
            p = BigWorld.player()
            if p.targetLocked != None and p.targetLocked != p:
                self.npcEnt = BigWorld.player().targetLocked
            if self.stamp != None and self.npcEnt:
                self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_EDIT_ROLE)))
        elif btnName == 'delEventBtn':
            pass

    def anotherControl(self, *arg):
        btnName = arg[3][0].GetString()
        strStamp = str(self.stamp)
        if btnName == 'delStoryBtn':
            self.ins.release()
        elif btnName == 'delRoleBtn':
            self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))
        elif btnName == 'playStoryBtn':
            self.ins.play()
        elif btnName == 'playRoleBtn':
            pass
        elif btnName == 'musicRatioBtn':
            ratio = arg[3][1].GetString()
            ratio = ratio == None and 1.0 or float(ratio)
            self.ins.setMusicRatio(ratio)

    def getValue(self, key):
        if key == 'storyEditDebug.storyList':
            gamelog.debug('bgf:stroyEdit', self.storyList)
            return self.getStoryArray()
        if key == 'storyEditDebug.RoleList':
            return self.getRoleContentArray()

    def onConfirm(self, *arg):
        btnName = arg[3][0].GetString()
        p = BigWorld.player()
        if btnName == 'addEffectBtn':
            effectId = int(arg[3][1].GetString())
            lastTime = float(arg[3][2].GetString())
            if arg[3][3].GetString() == '':
                yaw = 0
            else:
                yaw = float(arg[3][3].GetString())
            if arg[3][4].GetString() == '':
                pitch = 0
            else:
                pitch = float(arg[3][4].GetString())
            if arg[3][5].GetString() == '':
                roll = 0
            else:
                roll = float(arg[3][5].GetString())
            gamelog.debug('bgf:storyEdit', effectId, lastTime)
            if self.stamp != None:
                event = self.ins.eventMgr.getEvent(self.stamp)
                event.addEnvEff(effectId, tuple(p.position), roll, yaw, pitch, lastTime)
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'addModelBtn':
            gamelog.debug('bgf:storyEdit', arg[3][1].GetString(), arg[3][2].GetString())
            modelId = arg[3][1].GetString()
            lastTime = 0
            if arg[3][2].GetString():
                lastTime = [ float(x) for x in arg[3][2].GetString().split(',') ]
            else:
                lastTime = [0.0]
            if self.stamp != None:
                event = self.ins.eventMgr.getEvent(self.stamp)
                event.addEnvModel(modelId, tuple(p.position), *lastTime)
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'newRoleBtn':
            gamelog.debug('bgf:storyEdit', arg[3][1].GetString(), arg[3][2].GetString(), arg[3][3].GetString(), arg[3][4].GetString(), arg[3][5].GetString())
            roleName = unicode2gbk(arg[3][1].GetString())
            if arg[3][2].GetString() == '':
                yaw = 0
            else:
                yaw = float(arg[3][2].GetString())
            modelId = unicode2gbk(arg[3][3].GetString())
            modelId = int(modelId.split(':')[0])
            isShow = bool(arg[3][4].GetString())
            tag = arg[3][5].GetString()
            applyDrop = arg[3][6].GetBool()
            if tag == '':
                tag = None
            gamelog.debug('bgf:storyEdit', roleName, yaw, modelId, isShow)
            self.ins.addActor(self.stamp, roleName, tag, tuple(p.position), yaw, modelId, isShow, applyDrop)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'addDofBtn':
            gamelog.debug('gjd:storyEdit', arg[3][1].GetString(), arg[3][2].GetString(), arg[3][3].GetString())
            dofFocus = float(arg[3][1].GetString())
            dofRadius = float(arg[3][2].GetString())
            dofExp = float(arg[3][3].GetString())
            nearMaxBlur = float(arg[3][4].GetString())
            farMaxBlur = float(arg[3][5].GetString())
            minBlur = float(arg[3][6].GetString())
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addEnvDof(dofFocus, dofRadius, dofExp, nearMaxBlur, farMaxBlur, minBlur)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'setCameraAfterScenarioBtn':
            gamelog.debug('gjd:storyEdit', arg[3][1].GetString(), arg[3][2].GetString())
            yaw = float(arg[3][1].GetString())
            pitch = float(arg[3][2].GetString())
            self.ins.setYawAndPictch(yaw, pitch)
        elif btnName == 'addBlurBtn':
            gamelog.debug('gjd:storyEdit', arg[3][1].GetString(), arg[3][2].GetString())
            blurTime = int(arg[3][1].GetString())
            blurScale = int(arg[3][2].GetString())
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addEnvBlur(blurTime, blurScale)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'addWeatherBtn':
            gamelog.debug('gjd:storyEdit', arg[3][1].GetString(), arg[3][2].GetString())
            zoneName = arg[3][1].GetString()
            targetWeight = int(arg[3][2].GetString())
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addEnvWeather(zoneName, targetWeight)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'delRoleBtn':
            roleName = unicode2gbk(arg[3][1].GetString())
            gamelog.debug('bgf:storyEdit', roleName)
            self.ins.delActor(roleName)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'sceneRenderBtn':
            self.storyMC.Invoke('setData', self.getDataArray())
            color = int(arg[3][1].GetString())
            fadeTime = float(arg[3][2].GetString())
            duration = float(arg[3][3].GetString())
            if self.stamp != None:
                event = self.ins.eventMgr.getEvent(self.stamp)
                event.addEnvDye(color, fadeTime, duration)
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'yawBtn':
            gamelog.debug('bgf:storyEdit', arg[3][1].GetString())
            yaw = arg[3][1].GetString()
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'yaw', yaw)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'lookAtBtn':
            lookAtX = arg[3][1].GetString()
            lookAtY = arg[3][2].GetString()
            time = arg[3][3].GetString()
            poseNumber = arg[3][4].GetString()
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'lookAt', lookAtX + ',' + lookAtY + ',' + time + ',' + poseNumber)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'showHideBtn':
            gamelog.debug('bgf:storyEdit', arg[3][1].GetString())
            hideActor = arg[3][1].GetString() == 'True' and '1' or '0'
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'hide', hideActor)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'transpareBtn':
            gamelog.debug('gjd:storyEdit', arg[3][1].GetString())
            transpare = int(arg[3][1].GetString())
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'transpare', transpare)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'actionBtn':
            gamelog.debug('bgf:storyEdit', arg[3][1].GetString())
            act = arg[3][1].GetString().split(':')[0]
            emotionSuperpose = arg[3][2].GetBool()
            if self.npcEnt != None:
                if not emotionSuperpose:
                    self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'act', act)
                else:
                    self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'emotion', act)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'runBtn':
            gamelog.debug('bgf:storyEdit', arg[3][1].GetString())
            time = arg[3][1].GetString()
            pos = BigWorld.player().position
            info = '%.2f, %.2f, %.2f, %s' % (pos[0],
             pos[1],
             pos[2],
             time)
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'run', info)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'talkBtn':
            gamelog.debug('bgf:storyEdit', arg[3][1].GetString(), arg[3][2].GetString())
            content = unicode2gbk(arg[3][1].GetString())
            lastTime = unicode2gbk(arg[3][2].GetString())
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'speak', content + ',' + lastTime)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'roleEffectBtn':
            gamelog.debug('bgf:storyEdit', arg[3][1].GetString())
            effectId = arg[3][1].GetString()
            lastTime = arg[3][2].GetString()
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'effect', effectId + ', ' + lastTime)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'blackFlashBtn':
            fadeIn = arg[3][1].GetString()
            last = arg[3][2].GetString()
            fadeOut = arg[3][3].GetString()
            isWhite = arg[3][4].GetBool()
            isWhite = 1 if isWhite else 0
            if fadeIn == '':
                fadeIn = 0.0
            else:
                fadeIn = float(fadeIn)
            if last == '':
                last = 0.0
            else:
                last = float(last)
            if fadeOut == '':
                fadeOut = 0.0
            else:
                fadeOut = float(fadeOut)
            gamelog.debug('bgf:fade', fadeIn, last, fadeOut, isWhite)
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addEnvFade(fadeIn, last, fadeOut, isWhite)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'timeBtn':
            t = float(arg[3][1].GetString())
            gamelog.debug('bgf:fade', t)
            self.ins.setLifeTime(t)
        elif btnName == 'musicBtn':
            fxPath = arg[3][1].GetString()
            isVoice = arg[3][2].GetBool()
            event = self.ins.eventMgr.getEvent(self.stamp)
            if isVoice:
                event.addVoice(fxPath)
            else:
                event.addFx(fxPath)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'specialFxBtn':
            fxId = float(arg[3][1].GetString())
            lastTime = None
            if arg[3][2].GetString():
                lastTime = float(arg[3][2].GetString())
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addScreenEff(fxId, lastTime)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'swayBtn':
            hz = float(arg[3][1].GetString())
            lastTime = float(arg[3][2].GetString())
            amp = arg[3][3].GetString().split(',')
            ampX, ampY, ampZ = [ float(x) for x in amp ]
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addSway(hz, lastTime, ampX, ampY, ampZ)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'hideModelBtn':
            hideModel = 0
            if arg[3][1].GetString() == 'True':
                hideModel = 1
            stamp = float(arg[3][2].GetString())
            event = self.ins.eventMgr.getEvent(stamp)
            gamelog.debug('bgf:hideModelBtn', stamp, event, self.emFlag, self.emId, self.emPos, self.stamp)
            if stamp >= self.stamp:
                event.addHideModel(self.emId, self.emPos, hideModel, self.stamp)
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'wenziBtn':
            color = int(arg[3][1].GetString())
            coord = tuple([ float(x) for x in arg[3][2].GetString().split(',') ])
            font = int(arg[3][3].GetString())
            duration = int(arg[3][4].GetString())
            msg = unicode2gbk(arg[3][5].GetString())
            filmEff = int(arg[3][6].GetNumber())
            fontName = unicode2gbk(arg[3][7].GetString())
            midSet = int(arg[3][8].GetBool())
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addEnvMsg(msg, coord, color, duration, font, filmEff, fontName, midSet)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'backMusicBtn':
            bgMusicPath = arg[3][1].GetString()
            enableMusic = arg[3][2].GetBool() is True and 1 or 0
            enableFx = arg[3][3].GetBool() is True and 1 or 0
            enableStatic = arg[3][4].GetBool() is True and 1 or 0
            enableAmbient = arg[3][5].GetBool() is True and 1 or 0
            gamelog.debug('backMusicBtn', bgMusicPath, enableMusic, enableFx, enableStatic, enableAmbient)
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addBgMusic(bgMusicPath, enableMusic, enableFx, enableStatic, enableAmbient)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'addPlateBtn':
            path = arg[3][1].GetString()
            leftTop = arg[3][2].GetString()
            rightBottom = arg[3][3].GetString()
            totalTime = arg[3][4].GetString()
            transform = arg[3][5].GetString().split(',')
            smallPath = arg[3][6].GetString()
            smallLeftTop = arg[3][7].GetString()
            leftX, topY = leftTop.split(',')
            rightX, bottomY = rightBottom.split(',')
            smallLeftX = smallTopY = 0
            if smallLeftTop:
                smallLeftX, smallTopY = smallLeftTop.split(',')
            tempArray = []
            l = len(transform)
            for i in xrange(0, l / 4):
                item = (float(transform[i * 4]),
                 float(transform[i * 4 + 1]),
                 float(transform[i * 4 + 2]),
                 float(transform[i * 4 + 3]))
                tempArray.append(item)

            gamelog.debug('addPlateBtn', tempArray, transform)
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addPlate(path, float(leftX), float(rightX), float(topY), float(bottomY), float(totalTime), tempArray, smallPath, float(smallLeftX), float(smallTopY))
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'addProjectionBtn':
            strNearPlane = arg[3][1].GetString()
            strFov = arg[3][2].GetString()
            nearPlane = BigWorld.projection().nearPlane
            fov = BigWorld.projection().fov
            if strNearPlane != '':
                nearPlane = float(strNearPlane)
            if strFov != '':
                fov = float(strFov)
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addProjection(nearPlane, fov)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'upWingBtn':
            modelId = arg[3][1].GetString()
            ratio = arg[3][2].GetString()
            if modelId and ratio:
                if self.npcEnt != None:
                    self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'upWing', modelId + ',' + ratio)
                    self.roleMC.Invoke('setListData', self.getRoleContentArray())
                    self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'upZaijuBtn':
            modelId = arg[3][1].GetString()
            ratio = arg[3][2].GetString()
            matchCaps = arg[3][3].GetString()
            if modelId and ratio and matchCaps:
                if self.npcEnt != None:
                    self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'upZaiju', modelId + ',' + ratio + ',' + matchCaps)
                    self.roleMC.Invoke('setListData', self.getRoleContentArray())
                    self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'addColorGradingBtn':
            tgaPath = arg[3][1].GetString()
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addColorGrading(tgaPath)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'addModelCameraBtn':
            try:
                modelId = int(arg[3][1].GetString())
                pos = tuple([ float(item) for item in arg[3][2].GetString().split(',') ])
                yaw = float(arg[3][3].GetString())
                action = arg[3][4].GetString()
                scale = tuple([ float(item) for item in arg[3][5].GetString().split(',') ])
                isHideModelCamera = int(arg[3][6].GetBool())
            except:
                gamelog.error('data is not valid')

            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addModelCamera(modelId, pos, yaw, action, scale, isHideModelCamera)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'bigEmoteBtn':
            emoteId = arg[3][1].GetString()
            emoteOffset = arg[3][2].GetString()
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'showBigEmote', '%s,%s' % (emoteId, emoteOffset))
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'upWeaponBtn':
            modelPath = arg[3][1].GetString()
            ratio = arg[3][2].GetString()
            hp = arg[3][3].GetString()
            if modelPath and ratio and hp:
                weaponModel = clientUtils.model('item/model/' + modelPath)
                if weaponModel and weaponModel.node(hp) and self.npcEnt:
                    self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'upWeapon', ','.join((modelPath, ratio, hp)))
                    self.roleMC.Invoke('setListData', self.getRoleContentArray())
                    self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'robBtn':
            npcId = arg[3][1].GetString()
            if self.npcEnt:
                actor = self.ins.getActor(self.npcEnt.roleName)
                actor.robNpcModel(npcId)
        elif btnName == 'addCgBtn':
            cgName = arg[3][1].GetString()
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addMovie(cgName)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'addSwfBtn':
            swfName = arg[3][1].GetString()
            swfTime = float(arg[3][2].GetString())
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addSwf(swfName, swfTime)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'switchWeaponBtn':
            delayTime = arg[3][1].GetString()
            action = arg[3][2].GetString()
            leftHandOldHP = arg[3][3].GetString()
            leftHandNewHP = arg[3][4].GetString()
            rightHandOldHP = arg[3][5].GetString()
            rightHandNewHP = arg[3][6].GetString()
            caps = arg[3][7].GetString()
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'switchWeapon', ','.join([delayTime,
                 action,
                 leftHandOldHP,
                 leftHandNewHP,
                 rightHandOldHP,
                 rightHandNewHP,
                 caps]))
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'action1Btn':
            act = arg[3][1].GetString().split(':')[0]
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'act1', act)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'addScreenEffectBtn':
            path = arg[3][1].GetString()
            time = float(arg[3][2].GetString())
            fadein = float(arg[3][3].GetString())
            fadeout = float(arg[3][4].GetString())
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addScreenEffect(path, time, fadein, fadeout)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'curvelRunBtn':
            data = arg[3][1].GetString()
            self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'curveRun', data)
            self.storyMC.Invoke('setData', self.getDataArray())
            self.roleMC.Invoke('setListData', self.getRoleContentArray())
        elif btnName == 'GUIMsgBtn':
            color = int(arg[3][1].GetString())
            coord = tuple([ float(x) for x in arg[3][2].GetString().split(',') ])
            size = int(arg[3][3].GetString())
            duration = int(arg[3][4].GetString())
            msg = unicode2gbk(arg[3][5].GetString())
            frame = int(arg[3][6].GetString())
            blackGround = arg[3][7].GetBool()
            notMid = arg[3][8].GetBool()
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addEnvGUIMsg(coord, msg, color, duration, size, frame, blackGround, notMid)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'addWingActionBtn':
            action = arg[3][1].GetString()
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'wingAction', action)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'magnitudeBtn':
            magnitude = float(arg[3][1].GetString())
            fadeIn = float(arg[3][2].GetString())
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addMagnitude(magnitude, fadeIn)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'questMsgBtn':
            msg = unicode2gbk(arg[3][1].GetString())
            npcId = int(arg[3][2].GetString())
            duration = int(arg[3][3].GetString())
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addQuestMsg(msg, npcId, duration)
            self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'renderBtn':
            index = int(arg[3][1].GetString())
            event = self.ins.eventMgr.getEvent(self.stamp)
            event.addRenderMode(index)
            self.storyMC.Invoke('setData', self.getDataArray())

    def onCancel(self, *arg):
        pass

    def scanStoryFile(self):
        curPath = ['intro/scenario/']
        if BigWorld.isPublishedVersion():
            curPath.append('../game/avatar/')
        for p in curPath:
            folderSection = ResMgr.openSection(p)
            if folderSection:
                for i in folderSection.keys():
                    i = i.lower()
                    if i.endswith('.xml'):
                        self.storyList.append(i)

    def getStoryArray(self):
        i = 0
        ar = self.movie.CreateArray()
        self.scanStoryFile()
        for item in self.storyList:
            value = GfxValue(gbk2unicode(self.storyList[i]))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def scanFrameList(self):
        self.frameList = []
        eList = self.ins.eventMgr.eventList
        for e in eList:
            self.frameList.append(str(e.time))
            gamelog.debug('bgf:storyEdit', e.time)

    def getFrameArray(self):
        i = 0
        ar = self.movie.CreateArray()
        self.scanFrameList()
        for item in self.frameList:
            value = GfxValue(gbk2unicode(self.frameList[i]))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def scanModelFile(self):
        folderSection = ResMgr.openSection(gameglobal.charRes)
        if folderSection:
            for i in folderSection.keys():
                if i.isdigit():
                    self.modelList.append(i)

    def scanRoleFile(self):
        self.roleList = []
        data = npc_model_client_data.data
        self.roleList.append('0:Ìæ´úÖ÷½Ç')
        for id in data:
            name = data[id]['name']
            self.roleList.append(str(id) + ':' + name)

        gamelog.debug('bgf:storyEdit', self.roleList)

    def getRoleArray(self):
        i = 0
        ar = self.movie.CreateArray()
        if not self.roleList:
            self.scanRoleFile()
        for item in self.roleList:
            value = GfxValue(gbk2unicode(item))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def getModelArray(self):
        i = 0
        ar = self.movie.CreateArray()
        if not self.modelList:
            self.scanModelFile()
        for item in self.modelList:
            value = GfxValue(self.modelList[i])
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def getDataArray(self):
        i = 0
        ar = self.movie.CreateArray()
        if self.stamp == None:
            return
        self.dataList = self.ins.getDataByEvent(self.stamp)
        for item in self.dataList:
            if item[0] == 'npc':
                value = GfxValue('npc,' + gbk2unicode(item[1]))
            else:
                value = GfxValue(str(item))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def getRoleAction(self):
        i = 0
        ar = self.movie.CreateArray()
        actionPair = self.npcEnt.model.actionNamePair()
        for id, name in actionPair:
            value = GfxValue(id + ':' + name)
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def showStoryEdit(self):
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_STORY_EDIT)))
        self.uiAdapter.movie.invoke(('_root.loadWidget', GfxValue(uiConst.WIDGET_CURRENT_FRAME)))

    def onClose(self, *arg):
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_STORY_EDIT)))
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_CURRENT_FRAME)))
        self.uiAdapter.movie.invoke(('_root.unloadWidget', GfxValue(uiConst.WIDGET_EDIT_ROLE)))
        self.isShow = False
        if self.cameraIsOpen:
            self.ins.watchCamera(False)
            p = BigWorld.player()
            p.unlockKey(gameglobal.KEY_POS_SCENARIO)
            self.cameraIsOpen = False

    def hideEditRole(self, *arg):
        self.roleMC.SetVisible(False)

    def editRoleContol(self, *arg):
        btnName = arg[3][0].GetString()
        strStamp = str(self.stamp)
        if btnName == 'appearanceBtn':
            pass
        elif btnName == 'editRoleBtn':
            pass
        elif btnName in ('actionBtn', 'action1Btn'):
            self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))
            self.frameMC.Invoke('setActionData', self.getRoleAction())
        elif btnName == 'roleDelBtn':
            if self.roleEditIndex != None:
                self.ins.eventMgr.delActorEvent(self.stamp, self.npcEnt.roleName, self.roleEditIndex)
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'downWingBtn':
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'downWing')
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'downZaijuBtn':
            if self.npcEnt != None:
                self.ins.eventMgr.addActorEvent(self.stamp, self.npcEnt.roleName, 'downZaiju')
                self.roleMC.Invoke('setListData', self.getRoleContentArray())
                self.storyMC.Invoke('setData', self.getDataArray())
        elif btnName == 'textureCkbox':
            value = arg[3][1].GetBool()
            actor = self.ins.getActor(self.npcEnt.roleName)
            actor.setTexturePriority(value)
        elif btnName == 'movePosition':
            pos = BigWorld.player().position
            actor = self.ins.getActor(self.npcEnt.roleName)
            actor.movePosition(pos.x, pos.y, pos.z)
        else:
            self.frameMC.Invoke('loadModel', (GfxValue(btnName), GfxValue(strStamp)))

    def chooseRoleData(self, *arg):
        gamelog.debug('bgf:storyEdit1', arg[3][0].GetString())
        self.roleEditIndex = int(arg[3][0].GetString())

    def getRoleContentArray(self):
        ar = self.movie.CreateArray()
        value = getattr(self.ins.getActor(self.npcEnt.roleName), 'texturePriority', 0)
        ar.SetElement(0, GfxValue(value))
        i = 1
        data = self.ins.getDataByActor(self.stamp, self.npcEnt.roleName)
        gamelog.debug('bgf:storyEditRole', data)
        for item in data:
            value = GfxValue(str(item[0]) + ',' + str(item[1]) + ',' + gbk2unicode(item[2]))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def onChangeFov(self, *arg):
        if self.cameraIsOpen:
            fov = float(arg[3][0].GetString())
            BigWorld.projection().fov = fov

    def _usePlayerCamera(self, isTrue):
        self.ins.useCursorCamera(isTrue)

    def _hideAvatar(self, isTrue):
        self.ins.setHideAvatar(isTrue)

    def _hideNPC(self, isTrue):
        self.ins.setHideNPC(isTrue)

    def _hideMovingPlat(self, isTrue):
        self.ins.setHideMovingPlat(isTrue)

    def _hidePlayer(self, isTrue):
        self.ins.setHidePlayer(isTrue)

    def _hideMonster(self, isTrue):
        self.ins.setHideMonster(isTrue)

    def _canEsc(self, isTrue):
        self.ins.setCanEsc(isTrue)

    def _filCamera(self, isTrue):
        self.ins.setFillCamera(isTrue)

    def _passFade(self, isTrue):
        self.ins.setPassFade(isTrue)

    def _hideTreasureBox(self, isTrue):
        self.ins.setHideTreasureBox(isTrue)

    def _hideAvatarExcludeTeam(self, isTrue):
        self.ins.setHideAvatarExcludeTeam(isTrue)

    def _hideEntityTopLogo(self, isTrue):
        self.ins.setHideEntityTopLogo(isTrue)

    def _hideTransport(self, isTrue):
        self.ins.setHideTransport(isTrue)

    def usePlayerCamera(self, *arg):
        checkBoxName = arg[3][0].GetString()
        isTrue = arg[3][1].GetBool() == True and 1 or 0
        gamelog.debug('bgf:usePlayerCamera', checkBoxName, isTrue)
        self.checkBoxMap[checkBoxName](isTrue)

    def presetCamera(self, *arg):
        isTrue = arg[3][1].GetBool()
        event = self.ins.eventMgr.getEvent(self.stamp)
        event.addPresetCC(isTrue)

    def onSearchStoryName(self, *arg):
        prefix = arg[3][0].GetString()
        if prefix == '':
            return self.getValue('storyEditDebug.storyList')
        ret = []
        for item in self.storyList:
            if item.find(prefix) != -1:
                ret.append(item)

        return uiUtils.array2GfxAarry(ret, True)

    def onSearchNpcId(self, *arg):
        prefix = arg[3][0].GetString()
        if prefix == '':
            return self.getRoleArray()
        ret = []
        if not self.roleList:
            self.scanRoleFile()
        for item in self.roleList:
            if item.find(prefix) != -1:
                ret.append(item)

        return uiUtils.array2GfxAarry(ret, True)

    def onGetRunDist(self, *arg):
        if self.npcEnt:
            newStamp = -1.0
            originalPos = self.npcEnt.position
            for event in self.ins.eventMgr.eventList:
                if event.actorEvent.has_key(self.npcEnt.roleName):
                    actorEvent = event.actorEvent[self.npcEnt.roleName]
                    for act, param in actorEvent:
                        if act == 'run' and event.time > newStamp:
                            newStamp = event.time
                            param = [ float(item) for item in param.split(',') ]
                            originalPos = Math.Vector3(param[0:3])

            destinationPos = BigWorld.player().position
            return GfxValue((destinationPos - originalPos).length)
        return GfxValue(0)

    def onGetPosition(self, *arg):
        p = BigWorld.player()
        pos = p.position
        return uiUtils.array2GfxAarry([round(pos.x, 2), round(pos.y, 2), round(pos.z, 2)])

    def onGetRunInfo(self, *arg):
        info = []
        if self.npcEnt:
            pos = tuple(self.npcEnt.position)
            pos = [ round(item, 2) for item in pos ]
            info.append((pos, 0, 0))
            lastPos = self.npcEnt.position
            for event in self.ins.eventMgr.eventList:
                if event.actorEvent.has_key(self.npcEnt.roleName):
                    actorEvent = event.actorEvent[self.npcEnt.roleName]
                    for act, param in actorEvent:
                        if act == 'run':
                            param = [ float(item) for item in param.split(',') ]
                            originalPos = Math.Vector3(param[0:3])
                            time = param[3]
                            speed = (originalPos - lastPos).length / time
                            info.append((param[0:3], time, speed))
                            lastPos = originalPos

        return uiUtils.array2GfxAarry(info)
