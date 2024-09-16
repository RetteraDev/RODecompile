#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cameraProxy.o
from gamestrings import gameStrings
import time
import math
import BigWorld
import Math
from Scaleform import GfxValue
import gameglobal
import uiConst
import gamelog
import keys
import gametypes
import appSetting
import ui
from ui import gbk2unicode
from uiProxy import UIProxy
from guis import uiUtils
from sfx import screenEffect
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import map_config_data as MCD
from cdata import game_msg_def_data as GMDD
FOV_MIN = 0.01
FOV_MAX = 2.0
DOF_FOCUS_PARAM = [0, 32.0, 0]
GUANGQUAN_PARAM = [0.1, 37.1, 17.5]
JIAOJU_PARAM = [0.1, 27, 10.5]
DOF_BLUR_PARAM = [0.0, 1.0, 1.0]
MAX_DIS = 30

class CameraProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CameraProxy, self).__init__(uiAdapter)
        self.modelMap = {'hideOtherUI': self.onHideOtherUI,
         'takePhoto': self.onTakePhoto,
         'moveCamera': self.onMoveCamera,
         'getFovDist': self.onGetFovDist,
         'beginTakePhoto': self.onBeginTakePhoto,
         'getInitData': self.onGetInitData,
         'setShaderIndex': self.onSetShaderIndex,
         'focusPlayer': self.onFocusPlayer,
         'showEmotion': self.onShowEmotion,
         'setPhotoStyle': self.onSetPhotoStyle,
         'resetTilt': self.onResetTilt,
         'openDict': self.onOpenDict,
         'shareToPhone': self.onShareToPhone,
         'getCurrentPath': self.onGetCurrentPath,
         'isCameraNotifyVisibale': self.onIsCameraNotifyVisibale,
         'clickRecentPic': self.onClickRecentPic}
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
        self.dofRadius = 0
        self.dofFocus = 0
        self.dofMaxBlur = 1.0
        self.inPhotoing = False
        self.mediator = None
        self.photoStyle = 0
        self.uprightYawDelta = 0.03
        self.uprightYaw = 0
        self.uprightKey = 0
        self.photoPath = ''
        self.photoPathList = []
        self.newTakenPhotoList = []

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CAMERA:
            self.mediator = mediator
            self.isShow = True
            self.refreshCameraShare()

    def show(self):
        mapId = BigWorld.player().mapID
        mapData = MCD.data.get(mapId, {})
        if mapData.get('cameraBanned', 0):
            mapName = mapData.get('name', '')
            BigWorld.player().showGameMsg(GMDD.data.CAMERA_BANNED_TIPS, (mapName,))
            return
        elif self.isShow:
            return
        else:
            self.isHideAllUI = True
            self.uiAdapter.hideAllUI()
            self.uiAdapter.loadWidget(uiConst.WIDGET_CAMERA)
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
            gameglobal.rds.ui.realSense.initCamera()
            return

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CAMERA)
        self.isShow = False
        p = BigWorld.player()
        p.unlockKey(gameglobal.KEY_POS_UI)
        p.model.setModelNeedHide(False, 1.0)
        if self.isHideAllUI:
            self.uiAdapter.setVisRecord(uiConst.WIDGET_CAMERA, False)
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
        self.mediator = None
        self.dofRadius = 0
        self.dofFocus = 0
        self.inPhotoing = False
        BigWorld.setDepthOfField(False)
        if not appSetting.VideoQualitySettingObj.isDofForceEnable():
            BigWorld.enableU3DOF(False)
        self.photoStyle = 0
        self.uprightYaw = 0
        BigWorld.target.exclude = p
        gameglobal.rds.ui.realSense.hide()

    def onOpenDict(self, *args):
        BigWorld.ShellExecuteEx('..\\screenshot', '')

    def onGetCurrentPath(self, *args):
        if self.photoPath:
            return GfxValue(gbk2unicode('../' + self.photoPath))
        else:
            return GfxValue(gbk2unicode(''))

    def setPhotoPath(self, path):
        self.photoPath = path
        self.photoPathList.append(self.photoPath)
        self.newTakenPhotoList.append(self.photoPath)
        self.refreshNewTakenPhotoList(openedPhotoList=[])
        if self.mediator:
            self.mediator.Invoke('setCurrentImage', self.onGetCurrentPath(None))

    def refreshNewTakenPhotoList(self, openedPhotoList):
        for photoPath in openedPhotoList:
            if photoPath in self.newTakenPhotoList:
                self.newTakenPhotoList.remove(photoPath)

        if self.newTakenPhotoList == []:
            isShowNewPhotoNotify = False
        else:
            isShowNewPhotoNotify = True
        gameglobal.rds.ui.topBar.refreshPhotoNotify(isShowNewPhotoNotify)
        if self.mediator:
            self.mediator.Invoke('setCameraNotifyVisibale', GfxValue(isShowNewPhotoNotify))

    def onIsCameraNotifyVisibale(self, *arg):
        if self.newTakenPhotoList == []:
            isShowNewPhotoNotify = False
        else:
            isShowNewPhotoNotify = True
        return GfxValue(isShowNewPhotoNotify)

    def onShareToPhone(self, *args):
        if self.photoPath:
            gameglobal.rds.ui.qrCodeMultiGraph.show(self.photoPath, self.photoPathList)
        else:
            BigWorld.player().showGameMsg(GMDD.data.HAS_NO_TAKE_PHOTO, ())

    def refreshCameraShare(self):
        if self.mediator:
            self.mediator.Invoke('setCameraShareVisible', GfxValue(gameglobal.rds.configData.get('enableCameraShare', False)))

    def onHideOtherUI(self, *arg):
        self.isHideAllUI = arg[3][0].GetBool()
        gamelog.debug('onHideOtherUI', self.isHideAllUI)
        if self.isHideAllUI:
            self.uiAdapter.hideAllUI()
            self.uiAdapter.setWidgetVisible(uiConst.WIDGET_CAMERA, True)
        else:
            self.uiAdapter.setWidgetVisible(uiConst.WIDGET_CAMERA, True)
            self.uiAdapter.restoreUI()

    def onBeginTakePhoto(self, *arg):
        self.takePhoto()

    @ui.callFilter(0.5, False)
    def takePhoto(self):
        effectId = SCD.data.get('screenEffectParamCamera', 1014)
        screenEffect.startEffect(gameglobal.EFFECT_TAG_CAMERA, effectId)
        gameglobal.rds.sound.playSound(gameglobal.SD_449)
        if self.isShow and self.mediator:
            self.mediator.Invoke('beginTakePhoto')
        else:
            self.onTakePhoto(True)
        if self.isHideAllUI:
            self.uiAdapter.setWidgetVisible(uiConst.WIDGET_CAMERA, False)
        player = BigWorld.player()
        data = [str(player.spaceNo),
         str(player.position),
         str((player.roll, player.pitch, player.yaw)),
         str(BigWorld.getMemoryInfo())]
        player.base.recordClientLog(gametypes.CLIENT_RECORD_TYPE_TAKE_PHOTO, data)
        self.inPhotoing = True

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
        if self.photoStyle:
            w = BigWorld.screenWidth()
            h = BigWorld.screenHeight()
            waterMarkPosX = w if w < h else w / 2 + h / 2
            waterMarkPosY = h if h < w else w / 2 + h / 2
            if hasattr(BigWorld, 'setWaterMarkPositionBottomRight'):
                BigWorld.setWaterMarkPositionBottomRight((waterMarkPosX, waterMarkPosY))
        gameglobal.rds.ui.screenShot(timestr)
        self.uiAdapter.setVisRecord(uiConst.WIDGET_CAMERA, False)

    def onMoveCamera(self, *arg):
        sliderName = arg[3][0].GetString()
        val = arg[3][1].GetNumber()
        if sliderName == 'guangquanSlider':
            self.dofRadius = val
            self.setDof(self.dofFocus, self.dofRadius, self.dofMaxBlur)
        elif sliderName == 'depthSlider':
            self.dofMaxBlur = val
            self.setDof(self.dofFocus, self.dofRadius, self.dofMaxBlur)
        elif sliderName == 'jiaojuSlider':
            BigWorld.projection().fov = val
            gameglobal.rds.sound.playSound(gameglobal.SD_448)
        elif sliderName == 'focusSlider':
            self.dofFocus = val
            self.setDof(self.dofFocus, self.dofRadius)

    def handleMouseEvent(self, dx, dy, dz):
        if self.isShow and self.cc:
            if not BigWorld.getKeyDownState(keys.KEY_LCONTROL, 0):
                key = keys.KEY_W if dz > 0 else keys.KEY_S
                self.handleKeyEvent(True, key, 0, 0)
                BigWorld.callback(0.8, Functor(self.handleKeyEvent, False, key, 0, 0))
                return True
            step = dz / 120 * -0.03
            fov = BigWorld.projection().fov
            fov += step
            if fov >= FOV_MIN and fov <= FOV_MAX:
                BigWorld.projection().fov = fov
                self.setSliderValue('jiaojuSlider', fov)
            return True
        return False

    def setSliderValue(self, sliderName, value):
        if self.mediator:
            self.mediator.Invoke('setSliderValue', (GfxValue(sliderName), GfxValue(value)))

    def handleKeyEvent(self, down, key, vk, mods):
        if not self.isShow:
            return False
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
        elif key == keys.KEY_LEFTMOUSE and down:
            dist = self.getMouseDepth()
            self.dofFocus = dist
            self.setDof(self.dofFocus, self.dofRadius, self.dofMaxBlur)
            self.setSliderValue('focusSlider', math.log(dist, 1.25) if dist > 1.25 else dist)
        elif key in (keys.KEY_Z, keys.KEY_X):
            if key == keys.KEY_Z:
                self.uprightKey = -int(down) * self.uprightYawDelta
            elif key == keys.KEY_X:
                self.uprightKey = int(down) * self.uprightYawDelta
            if self.cameraHandle:
                BigWorld.cancelCallback(self.cameraHandle)
            self.controlCamera()

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

    def onGetFovDist(self, *arg):
        self.fovSaved = BigWorld.projection().fov
        ret = DOF_FOCUS_PARAM
        ret.extend([FOV_MIN, FOV_MAX, self.fovSaved])
        ret.extend(DOF_BLUR_PARAM)
        ret.extend(GUANGQUAN_PARAM)
        return uiUtils.array2GfxAarry(ret)

    def onGetInitData(self, *arg):
        ret = {}
        shaderList = SCD.data.get('shaderModeName', [gameStrings.TEXT_CAMERAPROXY_389,
         gameStrings.TEXT_CAMERAPROXY_389_1,
         gameStrings.TEXT_CAMERAPROXY_389_2,
         gameStrings.TEXT_CAMERAPROXY_389_3,
         gameStrings.TEXT_CAMERAPROXY_389_4,
         gameStrings.TEXT_CAMERAPROXY_389_5,
         gameStrings.TEXT_CAMERAPROXY_389_6])
        ret['shaderList'] = shaderList
        ret['shaderIndex'] = appSetting.getShaderIndex()
        ret['photoList'] = SCD.data.get('photoStyleName', [gameStrings.TEXT_CAMERAPROXY_392, gameStrings.TEXT_CAMERAPROXY_392_1])
        ret['ifEnableQRCode'] = gameglobal.rds.configData.get('enableQRCode', False)
        return uiUtils.dict2GfxDict(ret, True)

    def onSetShaderIndex(self, *arg):
        index = int(arg[3][0].GetNumber())
        appSetting.setShaderIndex(index)
        gameglobal.rds.ui.topBar.updateMode('renderMode')
        gameglobal.rds.ui.videoSetting.updateMode()

    def setDof(self, dofFocus, dofRadius, dofMaxBlur = 1.0):
        gamelog.debug('setDof', dofFocus, dofRadius)
        if dofRadius >= 3900:
            BigWorld.setDepthOfField(False)
        else:
            BigWorld.setDepthOfField(True, dofFocus, 1.0 / dofRadius, 1, dofMaxBlur, dofMaxBlur)

    def onFocusPlayer(self, *arg):
        if self.cc:
            p = BigWorld.player()
            dc = BigWorld.dcursor()
            dc.pitch = 0
            deltaYaw = p.yaw + math.pi
            if deltaYaw > math.pi:
                deltaYaw -= 2 * math.pi
            self.cc.deltaYaw += deltaYaw - self.cc.direction.yaw
            self.cc.pivotPosition = self.oldPivotPosition

    def onShowEmotion(self, *arg):
        if not gameglobal.rds.configData.get('enableNewEmotionPanel', False):
            if gameglobal.rds.ui.skill.generalMediator:
                gameglobal.rds.ui.skill.closeGeneralSkill()
            else:
                gameglobal.rds.ui.skill.showGeneralSkill(1)
        elif gameglobal.rds.ui.emoteAction.widget:
            gameglobal.rds.ui.emoteAction.clearWidget()
        else:
            gameglobal.rds.ui.emoteAction.show()

    def onSetPhotoStyle(self, *arg):
        index = int(arg[3][0].GetNumber())
        self.photoStyle = index

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

    def onResetTilt(self, *arg):
        self.uprightYaw = 0
        self.cc.uprightDirection = (0, 1, 0)

    def onClickRecentPic(self, *args):
        gameglobal.rds.ui.qrCode.showAppScanSharePhoto(self.photoPath)
