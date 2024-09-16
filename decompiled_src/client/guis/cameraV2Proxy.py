#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cameraV2Proxy.o
import time
import math
import BigWorld
import events
import Math
import gameglobal
import uiConst
import gamelog
import keys
import gametypes
import appSetting
import ui
import C_ui
import const
from appSetting import Obj as AppSettings
from ui import gbk2unicode
from sfx import screenEffect
from callbackHelper import Functor
from guis import uiUtils
from guis.asObject import TipManager
from uiProxy import UIProxy
from gamestrings import gameStrings
from guis.asObject import ASUtils
from Scaleform import GfxValue
from data import sys_config_data as SCD
from data import map_config_data as MCD
from cdata import game_msg_def_data as GMDD
MAX_DIS = 30
FOV_MIN = 0.01
FOV_MAX = 2.0
CAMERAMODE_DROP_DATA = [{'label': gameStrings.CAMERA_V2_FULL_SCREEM,
  'data': gameStrings.CAMERA_V2_FULL_SCREEM},
 {'label': gameStrings.CAMERA_V2_SQUARE,
  'data': gameStrings.CAMERA_V2_SQUARE},
 {'label': gameStrings.CAMERA_V2_PHONE_16_9,
  'data': gameStrings.CAMERA_V2_PHONE_16_9},
 {'label': gameStrings.CAMERA_V2_PHONE_4_3,
  'data': gameStrings.CAMERA_V2_PHONE_4_3},
 {'label': gameStrings.CAMERA_V2_CIRCLE,
  'data': gameStrings.CAMERA_V2_CIRCLE}]

class CameraV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CameraV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.isShow = False
        self.isHideAllUI = True
        self.fovSaved = None
        self.fovCurrent = None
        self.cc = None
        self.oldCameraDHProvider = None
        self.oldPivotPosition = None
        self.cameraHandle = None
        self.delta = [0, 0, 0]
        self.ratio = 0.75
        self.inPhotoing = False
        self.uprightYawDelta = 0.03
        self.uprightYaw = 0
        self.uprightKey = 0
        self.photoPath = ''
        self.photoPathList = []
        self.newTakenPhotoList = []
        self.shareOptionY = [89, 1]
        self.shareOptionHeight = [62, 148]
        self.resolutionArray = []
        self.scaleRate = 0
        self.dragIconSelected = False
        self.photoStyle = 0
        self.defultWidgetSize = [1102.0, 210.75]
        self.faceOrientation = False
        self.eyeOrientation = False
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CAMERA_V2, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CAMERA_V2:
            self.widget = widget
            self.isShow = True
            self.refreshCameraShare()
            self.initUI()
            self.refreshInfo()
            cameraMode = self.widget.bg.content.cameraMode
            cameraMode.selectedIndex = 0
            ASUtils.setDropdownMenuData(cameraMode, CAMERAMODE_DROP_DATA)
            cameraMode.menuRowCount = 5
            self.widget.bg.content.cameraMode.addEventListener(events.INDEX_CHANGE, self.handleCameraModeClick)
            self.widget.bg.content.cameraMode.validateNow()
            self.widget.bg.content.resolutionMenu.selectedIndex = 0
            self.resolutionArray = self.createResolutionArray()
            ASUtils.setDropdownMenuData(self.widget.bg.content.resolutionMenu, self.resolutionArray)
            self.widget.bg.content.resolutionMenu.addEventListener(events.INDEX_CHANGE, self.handleResolutionChange)

    def refreshCameraShare(self):
        ret = gameglobal.rds.configData.get('enableCameraShare', False)
        self.widget.bg.content.appSaveBtn.visible = ret
        if not ret:
            self.widget.bg.content.shareOption.visible = ret

    def clearWidget(self):
        gameglobal.rds.ui.cameraTable.clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CAMERA_V2)
        self.isShow = False
        p = BigWorld.player()
        if p:
            p.unlockKey(gameglobal.KEY_POS_UI)
            p.model.setModelNeedHide(False, 1.0)
            if self.isHideAllUI:
                self.uiAdapter.setVisRecord(uiConst.WIDGET_CAMERA_V2, False)
                self.uiAdapter.restoreUI()
                p.hideAllTeamTopLogo(False)
                self.isHideAllUI = False
            if self.fovSaved:
                BigWorld.projection().fov = self.fovSaved
                self.fovSaved = None
            BigWorld.resetDepthOfField()
            BigWorld.setOutlineParams(True, 0, 1)
            if self.cc:
                self.cc.pivotPosition = self.oldPivotPosition
                self.cc.cameraDHProvider = self.oldCameraDHProvider
                self.cc.uprightDirection = (0, 1, 0)
            self.cc = None
            self.delta = [0, 0, 0]
            gameglobal.rds.ui.cameraTable.dofRadius = 0
            gameglobal.rds.ui.cameraTable.dofFocus = 0
            self.inPhotoing = False
            BigWorld.setDepthOfField(False)
            if not appSetting.VideoQualitySettingObj.isDofForceEnable():
                BigWorld.enableU3DOF(False)
            self.uprightYaw = 0
            BigWorld.target.exclude = p
            gameglobal.rds.ui.realSense.hide()
        BigWorld.setParticleFrameRateMagnitude(1, 0)
        BigWorld.setActionFrameRateMagnitude(1, 0)
        isHide = AppSettings.get(keys.SET_TEAM_TOP_LOGO_MARK, 1)
        self.setTeamTopLogoVisible(isHide)
        if not gameglobal.rds.configData.get('enableNewEmotionPanel', False):
            if gameglobal.rds.ui.skill.generalMediator:
                gameglobal.rds.ui.skill.closeGeneralSkill()
        elif gameglobal.rds.ui.emoteAction.widget:
            gameglobal.rds.ui.emoteAction.clearWidget()

    def show(self):
        mapId = BigWorld.player().mapID
        mapData = MCD.data.get(mapId, {})
        p = BigWorld.player()
        if not p.stateMachine.checkStatus(const.CT_TAKE_PHOTO):
            return
        elif mapData.get('cameraBanned', 0):
            mapName = mapData.get('name', '')
            BigWorld.player().showGameMsg(GMDD.data.CAMERA_BANNED_TIPS, (mapName,))
            return
        else:
            if not self.widget:
                self.isHideAllUI = True
                self.uiAdapter.hideAllUI()
                self.uiAdapter.loadWidget(uiConst.WIDGET_CAMERA_V2)
                p = BigWorld.player()
                p.hideAllTeamTopLogo(True)
                p.ap.stopMove()
                p.ap.forceAllKeysUp()
                p.lockKey(gameglobal.KEY_POS_UI, False)
                p.model.setModelNeedHide(True, 1.0)
                BigWorld.setOutlineParams(False, 0, 1)
                self.cc = gameglobal.rds.cam.cc
                self.oldCameraDHProvider = self.cc.cameraDHProvider
                self.cc.cameraDHProvider = None
                self.oldPivotPosition = self.cc.pivotPosition
                gameglobal.rds.sound.playSound(gameglobal.SD_447)
                if not appSetting.VideoQualitySettingObj.isDofForceEnable():
                    BigWorld.enableU3DOF(True)
                BigWorld.target.exclude = None
                isHide = 0
                self.setTeamTopLogoVisible(isHide)
                gameglobal.rds.ui.realSense.initCamera()
                gameglobal.rds.ui.cameraTable.show()
            return

    def initUI(self):
        self.widget.bg.content.hintBtn.label = gameStrings.CAMERA_V2_HIDE_HINT
        self.widget.bg.content.hintLabel.visible = True
        self.widget.leftShader.visible = False
        self.widget.rightShader.visible = False
        self.widget.circleShader.visible = False
        self.widget.horizontalLine1.visible = False
        self.widget.horizontalLine1.alpha = 0.5
        self.widget.horizontalLine2.visible = False
        self.widget.horizontalLine2.alpha = 0.5
        self.widget.verticalLine1.visible = False
        self.widget.verticalLine1.alpha = 0.5
        self.widget.verticalLine2.visible = False
        self.widget.verticalLine2.alpha = 0.5
        self.widget.dragScreenIcon.visible = False
        self.widget.faceOrientation.visible = False
        self.widget.eyesFocus.visible = False
        self.widget.light.visible = False
        self.widget.bg.content.stopBtn.visible = False
        self.widget.bg.content.playBtn.visible = False
        self.widget.bg.content.hintBtn.addEventListener(events.MOUSE_CLICK, self.handleHint, False, 0, True)
        self.widget.defaultCloseBtn = self.widget.bg.content.quitBtn
        self.widget.bg.content.cameraBtn.addEventListener(events.MOUSE_CLICK, self.onBeginTakePhoto, False, 0, True)
        self.widget.bg.content.auxiliaryLineBtn.addEventListener(events.MOUSE_CLICK, self.handleAuxiliaryLine, False, 0, True)
        self.widget.bg.content.revertBtn.addEventListener(events.MOUSE_CLICK, self.handleFocusPlayer, False, 0, True)
        self.widget.bg.content.tiltBtn.addEventListener(events.MOUSE_CLICK, self.handleTilt, False, 0, True)
        self.widget.bg.content.emotionBtn.addEventListener(events.MOUSE_CLICK, self.handleEmotion, False, 0, True)
        self.widget.bg.content.appSaveBtn.addEventListener(events.MOUSE_CLICK, self.handleAppSave, False, 0, True)
        self.widget.bg.content.shareOption.visible = False
        self.widget.bg.content.appSaveBtn.notifyIcon.visible = self.isCameraNotifyVisibale()
        TipManager.addTip(self.widget.bg.content.appSaveBtn, gameStrings.CAMERA_V2_SAVE_PHOTO_TO_APP)
        self.widget.bg.content.shareOption.shareToPhone.icon.gotoAndPlay('iphone')
        self.widget.bg.content.shareOption.shareToPhone.icon.notifyIcon.visible = self.widget.bg.content.appSaveBtn.notifyIcon.visible
        self.widget.bg.content.shareOption.shareToPhone.addEventListener(events.MOUSE_CLICK, self.handleShareToPhone, False, 0, True)
        self.widget.bg.content.shareOption.openDict.addEventListener(events.MOUSE_CLICK, self.handleOpenDict, False, 0, True)
        self.widget.bg.content.shareOption.recentPicBtn.addEventListener(events.MOUSE_CLICK, self.handleClickRecentPic, False, 0, True)
        self.widget.bg.content.stopBtn.addEventListener(events.MOUSE_CLICK, self.handleStopAction, False, 0, True)
        self.widget.bg.content.playBtn.addEventListener(events.MOUSE_CLICK, self.handlePlayAction, False, 0, True)
        self.widget.dragScreenIcon.addEventListener(events.MOUSE_DOWN, self.dragStart)
        self.widget.faceOrientation.addEventListener(events.MOUSE_DOWN, self.faceOritentationDrag)
        self.widget.eyesFocus.addEventListener(events.MOUSE_DOWN, self.eyesFocusDrag)
        self.widget.stage.addEventListener(events.EVENT_RESIZE, self.widgetReload)
        TipManager.addTip(self.widget.bg.content.cameraBtn, gameStrings.CAMERA_V2_PR_SCRN)
        TipManager.addTip(self.widget.bg.content.revertBtn, gameStrings.CAMERA_V2_AUTO_ORITENTATION)
        TipManager.addTip(self.widget.bg.content.tiltBtn, gameStrings.CAMERA_V2_RESTORE_FLAT)
        TipManager.addTip(self.widget.bg.content.emotionBtn, gameStrings.CAMERA_V2_IMPORT_ACTION)
        screenState = BigWorld.getScreenState()
        self.widget.bg.x = 0.5 * (screenState[0] - self.widget.bg.width)
        self.widget.bg.y = screenState[1] - self.widget.bg.height
        self.widget.dragScreenIcon.y = screenState[1] * 0.75
        self.widget.faceOrientation.x = screenState[0] / 2.0 - 50
        self.widget.faceOrientation.y = screenState[1] / 1.5
        self.widget.eyesFocus.x = screenState[0] / 2.0 + 50
        self.widget.eyesFocus.y = screenState[1] / 1.5

    def refreshInfo(self):
        if not self.widget:
            return

    def faceOritentationDrag(self, *args):
        self.faceOrientation = True
        BigWorld.sendMouseMovementToScript(1)
        BigWorld.player().modelServer.poseManager.startLookAtPose()
        BigWorld.player().modelServer.poseManager.startFacePosFollow()

    def eyesFocusDrag(self, *args):
        self.eyeOrientation = True
        BigWorld.sendMouseMovementToScript(1)
        BigWorld.player().modelServer.poseManager.startLookAtPose()
        BigWorld.player().modelServer.poseManager.startEyesPosFollow()

    def handleStopAction(self, *args):
        self.widget.bg.content.stopBtn.visible = False
        self.widget.bg.content.playBtn.visible = True
        self.stopAction()

    def handlePlayAction(self, *args):
        self.widget.bg.content.playBtn.visible = False
        self.widget.bg.content.stopBtn.visible = True
        BigWorld.setParticleFrameRateMagnitude(1, 0)
        BigWorld.setActionFrameRateMagnitude(1, 0)

    def stopAction(self):
        BigWorld.setParticleFrameRateMagnitude(0.0, 0)
        BigWorld.setActionFrameRateMagnitude(0.0, 0)

    def widgetReload(self, *args):
        if self.widget:
            screenState = BigWorld.getScreenState()
            self.widget.dragScreenIcon.x = BigWorld.getScreenState()[0] * 0.5
            self.widget.dragScreenIcon.y = BigWorld.getScreenState()[1] * 0.75
            if screenState[0] <= 1280:
                self.widget.bg.width = screenState[0] / 1.3
                self.widget.bg.height = self.defultWidgetSize[1] / self.defultWidgetSize[0] * self.widget.bg.width
                self.widget.bg.x = 0.5 * (screenState[0] - self.widget.bg.width)
                self.widget.bg.y = screenState[1] - self.widget.bg.height
            else:
                self.widget.bg.height = self.defultWidgetSize[1]
                self.widget.bg.width = self.defultWidgetSize[0]
                self.widget.bg.x = 0.5 * (screenState[0] - self.widget.bg.width)
                self.widget.bg.y = screenState[1] - self.widget.bg.height
            if self.widget.bg.content.auxiliaryLineBtn.selected:
                self.resizeAuxiliaryLine()
            selectedIndex = self.widget.bg.content.cameraMode.selectedIndex
            self.widget.faceOrientation.x = screenState[0] / 2.0 - 50
            self.widget.faceOrientation.y = screenState[1] / 1.2
            self.widget.eyesFocus.x = screenState[0] / 2.0 + 50
            self.widget.eyesFocus.y = screenState[1] / 1.2
            if not selectedIndex == 0:
                self.shaderProcess()

    def handleCameraModeClick(self, *args):
        index = self.widget.bg.content.cameraMode.selectedIndex
        self.widget.dragScreenIcon.x = 0.5 * BigWorld.getScreenState()[0] - self.widget.x
        if index == 0:
            self.widget.leftShader.visible = False
            self.widget.rightShader.visible = False
            self.widget.circleShader.visible = False
            self.widget.dragScreenIcon.visible = False
        elif index == 1:
            self.scaleRate = 1.0
            self.shaderProcess()
        elif index == 2:
            self.scaleRate = 9.0 / 16
            self.shaderProcess()
        elif index == 3:
            self.scaleRate = 3.0 / 4
            self.shaderProcess()
        elif index == 4:
            self.widget.leftShader.visible = False
            self.widget.rightShader.visible = False
            self.widget.circleShader.visible = True
            self.widget.dragScreenIcon.visible = False
            self.shaderProcess()

    def dragStart(self, *args):
        self.dragIconSelected = True
        BigWorld.sendMouseMovementToScript(1)

    def shaderProcess(self):
        if not self.widget.bg.content.cameraMode.selectedIndex == 4:
            self.widget.dragScreenIcon.visible = True
            self.widget.leftShader.visible = True
            self.widget.rightShader.visible = True
            self.widget.circleShader.visible = False
            self.widget.leftShader.x = -self.widget.x + 0.5 * (BigWorld.getScreenState()[0] - self.scaleRate * BigWorld.getScreenState()[1])
            self.widget.leftShader.y = -self.widget.y
            self.widget.leftShader.height = BigWorld.getScreenState()[1]
            self.widget.leftShader.width = BigWorld.getScreenState()[0]
            self.widget.rightShader.x = -self.widget.x + 0.5 * (BigWorld.getScreenState()[0] + self.scaleRate * BigWorld.getScreenState()[1])
            self.widget.rightShader.y = -self.widget.y
            self.widget.rightShader.height = BigWorld.getScreenState()[1]
            self.widget.rightShader.width = BigWorld.getScreenState()[0]
        else:
            r = 0
            screenSize = BigWorld.getScreenState()
            if screenSize[0] > screenSize[1]:
                r = 0.5 * screenSize[1]
            else:
                r = 0.5 * screenSize[0]
            self.widget.circleShader.x = 0.5 * BigWorld.getScreenState()[0] - self.widget.x
            self.widget.circleShader.y = 0.5 * BigWorld.getScreenState()[1] - self.widget.y
            if screenSize[0] >= screenSize[1]:
                rate = 1.0 * BigWorld.getScreenState()[1] * 3 / self.widget.circleShader.height
                self.widget.circleShader.height = BigWorld.getScreenState()[1] * 3
                self.widget.circleShader.width = rate * self.widget.circleShader.width
            else:
                rate = 1.0 * screenSize[0] * 4 / self.widget.circleShader.width
                self.widget.circleShader.width = screenSize[0] * 4
                self.widget.circleShader.height = rate * self.widget.circleShader.height

    def handleHint(self, *e):
        if self.widget.bg.content.hintBtn.label == gameStrings.CAMERA_V2_HIDE_HINT:
            self.widget.bg.content.hintBtn.label = gameStrings.CAMERA_V2_SHOW_HINT
            self.widget.bg.content.hintLabel.visible = False
        else:
            self.widget.bg.content.hintBtn.label = gameStrings.CAMERA_V2_HIDE_HINT
            self.widget.bg.content.hintLabel.visible = True

    def resizeAuxiliaryLine(self):
        self.widget.horizontalLine1.width = BigWorld.getScreenState()[0]
        self.widget.horizontalLine2.width = BigWorld.getScreenState()[0]
        self.widget.horizontalLine1.height = 2.0
        self.widget.horizontalLine2.height = 2.0
        self.widget.horizontalLine1.x = -self.widget.x
        self.widget.horizontalLine2.x = -self.widget.x
        self.widget.horizontalLine1.y = 1.0 / 3 * BigWorld.getScreenState()[1] - self.widget.y
        self.widget.horizontalLine2.y = 2.0 / 3 * BigWorld.getScreenState()[1] - self.widget.y
        self.widget.verticalLine1.height = BigWorld.getScreenState()[1]
        self.widget.verticalLine2.height = BigWorld.getScreenState()[1]
        self.widget.verticalLine1.width = 2.0
        self.widget.verticalLine2.width = 2.0
        self.widget.verticalLine1.x = 1.0 / 3 * BigWorld.getScreenState()[0] - self.widget.x
        self.widget.verticalLine2.x = 2.0 / 3 * BigWorld.getScreenState()[0] - self.widget.x
        self.widget.verticalLine1.y = -self.widget.y
        self.widget.verticalLine2.y = -self.widget.y

    def handleAuxiliaryLine(self, *args):
        self.resizeAuxiliaryLine()
        self.widget.horizontalLine1.visible = not self.widget.bg.content.auxiliaryLineBtn.selected
        self.widget.horizontalLine2.visible = not self.widget.bg.content.auxiliaryLineBtn.selected
        self.widget.verticalLine1.visible = not self.widget.bg.content.auxiliaryLineBtn.selected
        self.widget.verticalLine2.visible = not self.widget.bg.content.auxiliaryLineBtn.selected

    def handleFocusPlayer(self, *args):
        if self.cc:
            p = BigWorld.player()
            dc = BigWorld.dcursor()
            dc.pitch = 0
            deltaYaw = p.yaw + math.pi
            if deltaYaw > math.pi:
                deltaYaw -= 2 * math.pi
            self.cc.deltaYaw += deltaYaw - self.cc.direction.yaw
            self.cc.pivotPosition = self.oldPivotPosition

    def handleTilt(self, *args):
        self.uprightYaw = 0
        if self.cc:
            self.cc.uprightDirection = (0, 1, 0)

    def handleEmotion(self, *args):
        if not BigWorld.player().isInBfDota():
            if not gameglobal.rds.configData.get('enableNewEmotionPanel', False):
                if gameglobal.rds.ui.skill.generalMediator:
                    gameglobal.rds.ui.skill.closeGeneralSkill()
                else:
                    gameglobal.rds.ui.skill.showGeneralSkill(1)
                    self.widget.bg.content.stopBtn.visible = True
            elif gameglobal.rds.ui.emoteAction.widget:
                gameglobal.rds.ui.emoteAction.clearWidget()
            else:
                gameglobal.rds.ui.emoteAction.show()
                self.widget.bg.content.stopBtn.visible = True
        else:
            msg = gameStrings.CAMERA_V2_EMOTE_ACTION_BANED
            gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def handleAppSave(self, *args):
        self.widget.bg.content.shareOption.visible = not self.widget.bg.content.shareOption.visible
        if self.widget.bg.content.shareOption.visible:
            path = self.onGetCurrentPath()
            self.setCurrentImage(path)

    def handleShareToPhone(self, *args):
        if self.photoPath:
            gameglobal.rds.ui.qrCodeMultiGraph.show(self.photoPath, self.photoPathList)
        else:
            BigWorld.player().showGameMsg(GMDD.data.HAS_NO_TAKE_PHOTO, ())

    def handleOpenDict(self, *args):
        BigWorld.ShellExecuteEx('..\\screenshot', '')

    def handleClickRecentPic(self, *args):
        gameglobal.rds.ui.qrCode.showAppScanSharePhoto(self.photoPath)

    def isCameraNotifyVisibale(self):
        if self.newTakenPhotoList == []:
            isShowNewPhotoNotify = False
        else:
            isShowNewPhotoNotify = True
        return isShowNewPhotoNotify

    def onBeginTakePhoto(self, *args):
        self.takePhoto()
        if self.isShow:
            BigWorld.callback(1.5, self.widgetShowUp)

    def widgetShowUp(self):
        if self.isShow:
            self.widget.visible = True
            self.widget.bg.gotoAndPlay('up')
            if not gameglobal.rds.configData.get('enableNewEmotionPanel', False):
                if gameglobal.rds.ui.skill.generalMediator:
                    self.uiAdapter.setWidgetVisible(uiConst.WIDGET_GENERAL_SKILL, True)
            elif gameglobal.rds.ui.emoteAction.widget:
                self.uiAdapter.setWidgetVisible(uiConst.WIDGET_EMOTE_ACTION, True)
            if gameglobal.rds.ui.cameraTable.isShow:
                gameglobal.rds.ui.cameraTable.widget.visible = True
            if gameglobal.rds.ui.zaiju.mediator:
                self.uiAdapter.setWidgetVisible(uiConst.WIDGET_ZAIJU, True)
            if gameglobal.rds.ui.zaijuV2.widget:
                self.uiAdapter.setWidgetVisible(uiConst.WIDGET_ZAIJU_V2, True)

    def handleKeyEvent(self, down, key, vk, mods):
        if not self.isShow:
            return False
        if key == keys.KEY_SPACE and self.widget.bg.content.playBtn.visible == True and down:
            BigWorld.setParticleFrameRateMagnitude(1, 0)
            BigWorld.setActionFrameRateMagnitude(1, 0)
            BigWorld.callback(0.1, self.stopAction)
            return True
        if key in (keys.KEY_W,
         keys.KEY_A,
         keys.KEY_S,
         keys.KEY_D,
         keys.KEY_Q,
         keys.KEY_E):
            ratio = self.ratio
            if mods == keys.MODIFIER_SHIFT:
                ratio *= 0.2
            if key == keys.KEY_W:
                self.delta[2] = int(down) * ratio
            elif key == keys.KEY_S:
                self.delta[2] = -int(down) * ratio
            elif key == keys.KEY_A:
                self.delta[0] = -int(down) * ratio
            elif key == keys.KEY_D:
                self.delta[0] = int(down) * ratio
            elif key == keys.KEY_Q:
                self.delta[1] = int(down) * ratio
            elif key == keys.KEY_E:
                self.delta[1] = -int(down) * ratio
            if self.cameraHandle:
                BigWorld.cancelCallback(self.cameraHandle)
            self.controlCamera()
        elif key == keys.KEY_LEFTMOUSE and down and gameglobal.rds.ui.cameraTable.isShow:
            dist = self.getMouseDepth()
            gameglobal.rds.ui.cameraTable.setDof(gameglobal.rds.ui.cameraTable.dofFocus, gameglobal.rds.ui.cameraTable.dofRadius, gameglobal.rds.ui.cameraTable.dofMaxBlur)
            gameglobal.rds.ui.cameraTable.setSliderValue('focusSlider', math.log(dist, 1.25) if dist > 1.25 else dist)
        elif key in (keys.KEY_Z, keys.KEY_X):
            if key == keys.KEY_Z:
                self.uprightKey = -int(down) * self.uprightYawDelta
            elif key == keys.KEY_X:
                self.uprightKey = int(down) * self.uprightYawDelta
            if self.cameraHandle:
                BigWorld.cancelCallback(self.cameraHandle)
            self.controlCamera()

    def getMouseDepth(self):
        if hasattr(BigWorld, 'getMouseDepthSlowAccurate'):
            ret = BigWorld.getMouseDepthSlowAccurate()
            if ret > 0:
                return ret
        p = BigWorld.player()
        if p.target:
            return self.getTargetLockedDepth(p.target)
        ret = BigWorld.getCursorPosInWorld(p.spaceID, 1000, False, ())
        if ret:
            worldPos = ret[0]
            camPos = Math.Matrix(BigWorld.camera().matrix).applyPoint(worldPos)
            return camPos.z
        return 50

    def controlCamera(self):
        delta = tuple(self.delta)
        if self.cc and (delta[0] or delta[1] or delta[2] or self.uprightKey):
            newPivotPosition = self.cc.pivotPosition + delta
            if newPivotPosition.length <= MAX_DIS:
                self.cc.pivotPosition += delta
            if self.uprightKey:
                self.uprightYaw += self.uprightKey
                self.cc.uprightDirection = (math.sin(self.uprightYaw), math.cos(self.uprightYaw), 0)
            self.cameraHandle = BigWorld.callback(0.1, self.controlCamera)

    def getTargetLockedDepth(self, target):
        cursor = BigWorld.getCursorPosInClip()
        nearPlane = BigWorld.projection().nearPlane
        fov = BigWorld.projection().fov
        yLength = nearPlane * math.tan(fov * 0.5)
        xLength = yLength * BigWorld.screenWidth() / BigWorld.screenHeight()
        invView = Math.Matrix(BigWorld.camera().invViewMatrix)
        nearPlanePoint = Math.Vector3(xLength * cursor.x, yLength * cursor.y, nearPlane)
        mouseRayDir = invView.applyVector(nearPlanePoint)
        mouseRayDir.normalise()
        diff = invView.applyToOrigin() - target.position
        diffXZ = Math.Vector2(diff.x, diff.z)
        dist = diffXZ.length / Math.Vector2(mouseRayDir.x, mouseRayDir.z).length
        return dist

    def handleMouseEvent(self, dx, dy, dz):
        if self.isShow and self.dragIconSelected:
            if BigWorld.getKeyDownState(keys.KEY_LEFTMOUSE, 0):
                if self.widget.leftShader.x + dx >= -self.widget.x and self.widget.rightShader.x + dx <= -self.widget.x + BigWorld.getScreenState()[0]:
                    self.widget.dragScreenIcon.x += dx
                    self.widget.rightShader.x += dx
                    self.widget.leftShader.x += dx
            else:
                self.dragIconSelected = False
                BigWorld.sendMouseMovementToScript(0)
            return True
        if self.isShow and self.faceOrientation:
            if BigWorld.getKeyDownState(keys.KEY_LEFTMOUSE, 0):
                if self.widget.faceOrientation.x + dx >= 0 and self.widget.faceOrientation.x + dx <= BigWorld.getScreenState()[0] - self.widget.faceOrientation.width and self.widget.faceOrientation.y + dy >= 0 and self.widget.faceOrientation.y + dy <= BigWorld.getScreenState()[1] - self.widget.faceOrientation.height:
                    self.widget.faceOrientation.x += dx
                    self.widget.faceOrientation.y += dy
            else:
                self.faceOrientation = False
                BigWorld.sendMouseMovementToScript(0)
            return True
        if self.isShow and self.eyeOrientation:
            if BigWorld.getKeyDownState(keys.KEY_LEFTMOUSE, 0):
                if self.widget.eyesFocus.x + dx >= 0 and self.widget.eyesFocus.x + dx <= BigWorld.getScreenState()[0] - self.widget.eyesFocus.width and self.widget.eyesFocus.y + dy >= 0 and self.widget.eyesFocus.y + dy <= BigWorld.getScreenState()[1] - self.widget.eyesFocus.height:
                    self.widget.eyesFocus.x += dx
                    self.widget.eyesFocus.y += dy
            else:
                self.eyeOrientation = False
                BigWorld.sendMouseMovementToScript(0)
            return True
        if self.isShow and self.cc:
            if not BigWorld.getKeyDownState(keys.KEY_LCONTROL, 0):
                key = keys.KEY_W if dz > 0 else keys.KEY_S
                self.handleKeyEvent(True, key, 0, 0)
                BigWorld.callback(0.8, Functor(self.handleKeyEvent, False, key, 0, 0))
                return True
            step = dz / 120 * -0.03
            fov = BigWorld.projection().fov
            fov += step
            if fov >= FOV_MIN and fov <= FOV_MAX and gameglobal.rds.ui.cameraTable.isShow:
                BigWorld.projection().fov = fov
                gameglobal.rds.ui.cameraTable.setSliderValue('jiaojuSlider', fov)
            return True
        return False

    def setCurrentImage(self, path):
        if path != '' and gameglobal.rds.configData.get('enableQRCode', False):
            self.widget.bg.content.shareOption.recentPicBtn.visible = True
        else:
            self.widget.bg.content.shareOption.recentPicBtn.visible = False
        if self.widget.bg.content.shareOption.recentPicBtn.visible:
            self.widget.bg.content.shareOption.bg.y = self.shareOptionY[1]
            self.widget.bg.content.shareOption.bg.height = self.shareOptionHeight[1]
            self.widget.bg.content.shareOption.recentPicBtn.picMC.icon.fitSize = True
            self.widget.bg.content.shareOption.recentPicBtn.picMC.icon.loadImage(path)
        else:
            self.widget.bg.content.shareOption.bg.y = self.shareOptionY[0]
            self.widget.bg.content.shareOption.bg.height = self.shareOptionHeight[0]

    def onGetCurrentPath(self, *args):
        if self.photoPath:
            return gbk2unicode('../' + self.photoPath)
        else:
            return gbk2unicode('')

    def setPhotoPath(self, path):
        self.photoPath = path
        self.photoPathList.append(self.photoPath)
        self.newTakenPhotoList.append(self.photoPath)
        self.refreshNewTakenPhotoList(openedPhotoList=[])
        self.setCurrentImage(self.onGetCurrentPath(None))

    def refreshNewTakenPhotoList(self, openedPhotoList):
        for photoPath in openedPhotoList:
            if photoPath in self.newTakenPhotoList:
                self.newTakenPhotoList.remove(photoPath)

        if self.newTakenPhotoList == []:
            isShowNewPhotoNotify = False
        else:
            isShowNewPhotoNotify = True
        gameglobal.rds.ui.topBar.refreshPhotoNotify(isShowNewPhotoNotify)
        self.setCameraNotifyVisibale(isShowNewPhotoNotify)

    def setCameraNotifyVisibale(self, isShowNewPhotoNotify):
        if self.widget and self.widget.bg.content.appSaveBtn.visible == True:
            self.widget.bg.content.appSaveBtn.notifyIcon.visible = isShowNewPhotoNotify
            self.widget.bg.content.shareOption.shareToPhone.icon.notifyIcon.visible = isShowNewPhotoNotify

    @ui.callFilter(0.5, False)
    def takePhoto(self):
        effectId = SCD.data.get('screenEffectParamCamera', 1014)
        gameglobal.rds.sound.playSound(gameglobal.SD_449)
        if self.isShow:
            self.beginTakePhoto()
        else:
            self.onTakePhoto(True)
        if self.isHideAllUI:
            self.uiAdapter.setWidgetVisible(uiConst.WIDGET_CAMERA_V2, False)
            self.uiAdapter.setWidgetVisible(uiConst.WIDGET_ZAIJU, False)
            self.uiAdapter.setWidgetVisible(uiConst.WIDGET_ZAIJU_V2, False)
        player = BigWorld.player()
        data = [str(player.spaceNo),
         str(player.position),
         str((player.roll, player.pitch, player.yaw)),
         str(BigWorld.getMemoryInfo())]
        player.base.recordClientLog(gametypes.CLIENT_RECORD_TYPE_TAKE_PHOTO, data)
        self.inPhotoing = True

    def beginTakePhoto(self):
        if self.isShow:
            self.widget.bg.gotoAndPlay('down')
            if gameglobal.rds.ui.cameraTable.isShow:
                gameglobal.rds.ui.cameraTable.widget.visible = False
            if not gameglobal.rds.configData.get('enableNewEmotionPanel', False):
                if gameglobal.rds.ui.skill.generalMediator:
                    self.uiAdapter.setWidgetVisible(uiConst.WIDGET_GENERAL_SKILL, False)
            elif gameglobal.rds.ui.emoteAction.widget:
                self.uiAdapter.setWidgetVisible(uiConst.WIDGET_EMOTE_ACTION, False)
            if gameglobal.rds.ui.zaiju.mediator:
                self.uiAdapter.setWidgetVisible(uiConst.WIDGET_ZAIJU, False)
            if gameglobal.rds.ui.zaijuV2.widget:
                self.uiAdapter.setWidgetVisible(uiConst.WIDGET_ZAIJU_V2, False)
        BigWorld.callback(0.5, self.callbackTakePhoto)

    def callbackTakePhoto(self):
        self.onTakePhoto(True)

    def onTakePhoto(self, *arg):
        try:
            highQuality = arg[3][0].GetBool()
        except:
            highQuality = arg[0]

        self.fovCurrent = BigWorld.projection().fov
        timestr = time.strftime('%Y%m%d-%H%M%S', time.localtime())
        if not highQuality:
            BigWorld.setInnerScreenSize(1.5)
        effectId = SCD.data.get('screenEffectParamCamera', 1014)
        lv, lastTime, path, fadeIn, fadeOut, ignoreSwitch = screenEffect.getScreenInfo(effectId)
        BigWorld.callback(lastTime + fadeIn + fadeOut, Functor(self.realTakePhoto, timestr))

    def realTakePhoto(self, timestr):
        BigWorld.projection().fov = self.fovCurrent
        selectedIndex = 0
        if self.isShow:
            selectedIndex = self.widget.bg.content.cameraMode.selectedIndex
        if not selectedIndex == 0:
            BigWorld.setWaterMarkPositionBottomRight((-100, -100))
        else:
            BigWorld.setWaterMarkPositionBottomRight((BigWorld.getScreenState()[0], BigWorld.getScreenState()[1]))
        gameglobal.rds.ui.screenShot(timestr)
        if self.isShow:
            self.uiAdapter.setVisRecord(uiConst.WIDGET_CAMERA_V2, False)

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
        for i, item in enumerate(resolutionList):
            width = item[0]
            height = item[1]
            showLabel = str(width) + ' x ' + str(height)
            if int(height) / int(width) < 0.6625:
                showLabel += gameStrings.SURFACESETTING_TEXT1
            resolutionArray.append({'label': showLabel,
             'data': [width, height],
             'index': i})

        return resolutionArray

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

    def handleResolutionChange(self, *args):
        _, _, windowed, state = BigWorld.getScreenState()
        w = self.resolutionArray[self.widget.bg.content.resolutionMenu.selectedIndex]['data'][0]
        h = self.resolutionArray[self.widget.bg.content.resolutionMenu.selectedIndex]['data'][1]
        appSetting.setScreenSize(w, h, windowed, True)

    def setTeamTopLogoVisible(self, isHide):
        ents = BigWorld.entities.values()
        for ent in ents:
            if ent.IsAvatar and (ent.isInTeam() or ent.isInGroup()):
                if hasattr(ent, 'topLogo'):
                    ent.topLogo.setTeamTopLogo(ent, isHide)
