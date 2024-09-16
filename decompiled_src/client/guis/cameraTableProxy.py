#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/cameraTableProxy.o
import math
import BigWorld
import gameglobal
import uiConst
import events
import appSetting
import keys
import Npc
from appSetting import Obj as AppSettings
from uiProxy import UIProxy
from guis.asObject import ASObject
from gamestrings import gameStrings
from callbackHelper import Functor
DISPLAY_BTN_TAG = 0
LENS_BTN_TAG = 1
LVJING_BTN_TAG = 2
SIGHT_BTN_TAG = 3
LIGHT_BTN_TAG = 4
MAX_TAG_NUMBER = 5
FOV_MIN = 0.01
FOV_MAX = 2.0
DOF_FOCUS_PARAM = [0, 32.0, 0]
GUANGQUAN_PARAM = [0.1, 37.1, 17.5]
JIAOJU_PARAM = [0.1, 27, 10.5]
DOF_BLUR_PARAM = [0.0, 1.0, 1.0]
RENGXIANG_PARA = [3.0 / 100 * DOF_FOCUS_PARAM[1],
 20.0 / 100 * FOV_MAX,
 80.0 / 100,
 55.0 / 100 * GUANGQUAN_PARAM[1],
 (0, 1.567782, 1.253247)]
TEXIE_PARA = [3.0 / 100 * DOF_FOCUS_PARAM[1],
 7.0 / 100 * FOV_MAX,
 80.0 / 100,
 55.0 / 100 * GUANGQUAN_PARAM[1],
 (0, 1.567782, 1.253247)]
FENGJING_PARA = [0.0 / 100 * DOF_FOCUS_PARAM[1],
 75.0 / 100 * FOV_MAX,
 20.0 / 100,
 47.0 / 100 * GUANGQUAN_PARAM[1],
 (0, 1.567782, 0.564722)]
SHADER_INTERVAL = [0,
 1.0,
 -0.3,
 0.3,
 0,
 0.5,
 -1.0,
 1.0,
 0.2,
 1.0,
 0.0,
 4.0,
 0,
 0.8]
CAMERA_HEIGHT_NORMAL = 0.7
CAMERA_HEIGHT_TEXIE = 0.8

class CameraTableProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(CameraTableProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CAMERA_TABLE, self.hide)

    def reset(self):
        self.widget = None
        self.isShow = False
        self.pivotDistRatio = 2.0
        self.tag = LENS_BTN_TAG
        self.dofRadius = 0
        self.dofFocus = 0
        self.dofMaxBlur = 1.0
        self.intensity = 1
        self.brightness = 0
        self.contrast = 0
        self.saturation = 0
        self.vignetting = 0
        self.particle = 0
        self.softLight = 0
        self.shaderIndex = appSetting.getShaderIndex()
        self.expertMode = True
        self.colorTransParamEnable = True
        self.defultContrast = 0
        self.defultSaturation = 0
        self.defultBrightness = 0
        self.friendsVisible = True
        self.otherPlayersVisible = True
        self.monsterVisible = True
        self.npcVisible = True
        self.spriteVisible = True

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_CAMERA_TABLE:
            self.widget = widget
            self.initUI()
            self.isShow = True
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CAMERA_TABLE)
        self.isShow = False
        p = BigWorld.player()
        p and p.hide(False)
        self.refreshModelVisible()
        if p:
            self.nicknameVisibleChange([not AppSettings.get(keys.SET_HIDE_PLAYER_NAME, 1),
             not AppSettings.get(keys.SET_HIDE_AVATAR_NAME, 1),
             not AppSettings.get(keys.SET_HIDE_OTHERENTITY_NAME, 1),
             not AppSettings.get(keys.SET_HIDE_OTHERENTITY_NAME, 1),
             not AppSettings.get(keys.SET_HIDE_SPRITE_NAME, 1),
             not AppSettings.get(keys.SET_HIDE_OTHERSPRITE_NAME, 1)])
            self.designationVisibleChange([not AppSettings.get(keys.SET_HIDE_PLAYER_TITLE, 1),
             not AppSettings.get(keys.SET_HIDE_AVATAR_TITLE, 1),
             not AppSettings.get(keys.SET_HIDE_OTHERENTITY_TITLE, 1),
             not AppSettings.get(keys.SET_HIDE_OTHERENTITY_TITLE, 1)])
            self.unionIconVisibleChange([not AppSettings.get(keys.SET_HIDE_PLAYER_GUILD, 1), not AppSettings.get(keys.SET_HIDE_AVATAR_GUILD, 1)])
            self.bloodBarVisibleChange([not AppSettings.get(keys.SET_HIDE_PLAYER_BLOOD, 1), not AppSettings.get(keys.SET_HIDE_AVATAR_BLOOD, 1), not AppSettings.get(keys.SET_HIDE_OTHERENTITY_BLOOD, 1)])
            self.setShaderIndex(appSetting.getShaderIndex(), 1, True)
            BigWorld.colorVibrancePlus(False, self.defultSaturation, self.defultBrightness, self.defultContrast, 0, 1)
            BigWorld.photoAdjust(False, self.softLight, SHADER_INTERVAL[9] + SHADER_INTERVAL[8] - self.vignetting)
            BigWorld.adjustSharpenEffect(False, self.particle, self.particle)
            if hasattr(p.modelServer.poseManager.model, 'poser') and hasattr(p.modelServer.poseManager.model.poser, 'targetMatrix'):
                p.modelServer.poseManager.model.poser.targetMatrix = None
            if hasattr(BigWorld.player().modelServer.poseManager.model, 'gaze') and hasattr(p.modelServer.poseManager.model.poser, 'targetMatrix'):
                p.modelServer.poseManager.model.gaze.targetMatrix = None

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_CAMERA_TABLE)

    def initUI(self):
        self.hideAll()
        self.widget.lens.visible = True
        self.widget.lensBtn.selected = True
        self.widget.lightBtn.visible = False
        self.widget.sightBtn.tag = SIGHT_BTN_TAG
        self.widget.displayBtn.tag = DISPLAY_BTN_TAG
        self.widget.lensBtn.tag = LENS_BTN_TAG
        self.widget.lvJingBtn.tag = LVJING_BTN_TAG
        self.widget.lightBtn.tag = LIGHT_BTN_TAG
        self.widget.sightBtn.addEventListener(events.MOUSE_CLICK, self.changePanel, False, 0, True)
        self.widget.displayBtn.addEventListener(events.MOUSE_CLICK, self.changePanel, False, 0, True)
        self.widget.lensBtn.addEventListener(events.MOUSE_CLICK, self.changePanel, False, 0, True)
        self.widget.lvJingBtn.addEventListener(events.MOUSE_CLICK, self.changePanel, False, 0, True)
        self.widget.lightBtn.addEventListener(events.MOUSE_CLICK, self.changePanel, False, 0, True)
        self.widget.nextBtn.addEventListener(events.MOUSE_CLICK, self.changeMode, False, 0, True)
        fov = self.getFovDist()
        self.widget.lens.focusSlider.minimum = fov[0]
        self.widget.lens.focusSlider.maximum = fov[1]
        self.widget.lens.focusSlider.value = fov[2]
        self.widget.lens.jiaojuSlider.minimum = fov[3]
        self.widget.lens.jiaojuSlider.maximum = fov[4]
        self.widget.lens.jiaojuSlider.value = fov[5]
        self.widget.lens.depthSlider.minimum = fov[6]
        self.widget.lens.depthSlider.maximum = fov[7]
        self.widget.lens.depthSlider.value = fov[8]
        self.widget.lens.guangquanSlider.minimum = fov[9]
        self.widget.lens.guangquanSlider.maximum = fov[10]
        self.widget.lens.guangquanSlider.value = fov[11]
        self.dofRadius = self.widget.lens.guangquanSlider.value
        self.widget.lens.jiaojuSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLensSlider)
        self.widget.lens.focusSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLensSlider)
        self.widget.lens.guangquanSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLensSlider)
        self.widget.lens.depthSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLensSlider)
        self.widget.lvJing.standardBtn.addEventListener(events.MOUSE_CLICK, self.changeShader, False, 0, True)
        self.widget.lvJing.softBtn.addEventListener(events.MOUSE_CLICK, self.changeShader, False, 0, True)
        self.widget.lvJing.inkBtn.addEventListener(events.MOUSE_CLICK, self.changeShader, False, 0, True)
        self.widget.lvJing.freshBtn.addEventListener(events.MOUSE_CLICK, self.changeShader, False, 0, True)
        self.widget.lvJing.classicBtn.addEventListener(events.MOUSE_CLICK, self.changeShader, False, 0, True)
        self.widget.lvJing.darkBtn.addEventListener(events.MOUSE_CLICK, self.changeShader, False, 0, True)
        self.widget.lvJing.aBaoBtn.addEventListener(events.MOUSE_CLICK, self.changeShader, False, 0, True)
        self.widget.lvJing.intensitySlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLvJingSlider)
        self.widget.lvJing.brightnessSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLvJingSlider)
        self.widget.lvJing.contrastSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLvJingSlider)
        self.widget.lvJing.saturationSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLvJingSlider)
        self.widget.lvJing.vignettingSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLvJingSlider)
        self.widget.lvJing.particleSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLvJingSlider)
        self.widget.lvJing.softLightSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleLvJingSlider)
        self.widget.lvJing.intensitySlider.value = 10.0
        self.widget.lvJing.brightnessSlider.value = 5.0
        self.widget.lvJing.contrastSlider.value = 0
        self.widget.lvJing.saturationSlider.value = 5.0
        self.widget.lvJing.vignettingSlider.value = 0
        self.widget.lvJing.particleSlider.value = 0
        self.widget.lvJing.softLightSlider.value = 0
        self.widget.display.model.selected = True
        self.widget.display.headTitle.selected = False
        self.widget.display.self.selected = True
        self.widget.display.friends.selected = True
        self.widget.display.otherPlayer.selected = True
        self.widget.display.npc.selected = True
        self.widget.display.monster.selected = True
        self.widget.display.sprite.selected = True
        self.widget.display.nickname.selected = False
        self.widget.display.designation.selected = False
        self.widget.display.unionIcon.selected = False
        self.widget.display.bloodBar.selected = False
        self.widget.display.headTitle.addEventListener(events.MOUSE_CLICK, self.headTitleChange, False, 0, True)
        self.widget.display.model.addEventListener(events.MOUSE_CLICK, self.modelChange, False, 0, True)
        self.widget.display.self.addEventListener(events.MOUSE_CLICK, self.visibleChange, False, 0, True)
        self.widget.display.friends.addEventListener(events.MOUSE_CLICK, self.visibleChange, False, 0, True)
        self.widget.display.otherPlayer.addEventListener(events.MOUSE_CLICK, self.visibleChange, False, 0, True)
        self.widget.display.npc.addEventListener(events.MOUSE_CLICK, self.visibleChange, False, 0, True)
        self.widget.display.monster.addEventListener(events.MOUSE_CLICK, self.visibleChange, False, 0, True)
        self.widget.display.sprite.addEventListener(events.MOUSE_CLICK, self.visibleChange, False, 0, True)
        self.widget.display.nickname.addEventListener(events.MOUSE_CLICK, self.visibleChange, False, 0, True)
        self.widget.display.designation.addEventListener(events.MOUSE_CLICK, self.visibleChange, False, 0, True)
        self.widget.display.unionIcon.addEventListener(events.MOUSE_CLICK, self.visibleChange, False, 0, True)
        self.widget.display.bloodBar.addEventListener(events.MOUSE_CLICK, self.visibleChange, False, 0, True)
        self.widget.lens.focusSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.refreshValue)
        self.widget.lens.jiaojuSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.refreshValue)
        self.widget.lens.depthSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.refreshValue)
        self.widget.lens.guangquanSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.refreshValue)
        self.widget.lens.renXiang.addEventListener(events.MOUSE_CLICK, self.defultLensChange, False, 0, True)
        self.widget.lens.fengJing.addEventListener(events.MOUSE_CLICK, self.defultLensChange, False, 0, True)
        self.widget.lens.teXie.addEventListener(events.MOUSE_CLICK, self.defultLensChange, False, 0, True)
        self.widget.sight.faceOrientation.addEventListener(events.MOUSE_CLICK, self.faceOrientationSelectedChange, False, 0, True)
        self.widget.sight.eyeOrientation.addEventListener(events.MOUSE_CLICK, self.eyeOrientationSelectedChange, False, 0, True)
        self.addEvent(events.EVENT_CHANGE_GROUP_MEMBER, self.onGroupMemberChange)
        self.initShader()
        self.refreshValue()
        self.nicknameVisibleChange([not self.widget.display.nickname.selected])
        self.designationVisibleChange([not self.widget.display.designation.selected])
        self.unionIconVisibleChange([not self.widget.display.unionIcon.selected])
        self.bloodBarVisibleChange([not self.widget.display.bloodBar.selected])
        defultColorTransParam = BigWorld.getColorTransParam()
        self.colorTransParamEnable, self.defultContrast, self.defultSaturation, self.defultBrightness = defultColorTransParam

    def faceOrientationSelectedChange(self, *args):
        gameglobal.rds.ui.cameraV2.widget.faceOrientation.visible = not self.widget.sight.faceOrientation.selected

    def eyeOrientationSelectedChange(self, *args):
        gameglobal.rds.ui.cameraV2.widget.eyesFocus.visible = not self.widget.sight.eyeOrientation.selected

    def initShader(self):
        self.widget.lvJing.standardBtn.selected = False
        index = appSetting.getShaderIndex()
        if index == 0:
            self.widget.lvJing.standardBtn.selected = True
        elif index == 1:
            self.widget.lvJing.softBtn.selected = True
        elif index == 2:
            self.widget.lvJing.inkBtn.selected = True
        elif index == 3:
            self.widget.lvJing.freshBtn.selected = True
        elif index == 4:
            self.widget.lvJing.classicBtn.selected = True
        elif index == 5:
            self.widget.lvJing.darkBtn.selected = True
        elif index == 6:
            self.widget.lvJing.aBaoBtn.selected = True

    def defultLensChange(self, *args):
        self.focusPlayer()
        e = ASObject(args[3][0])
        BigWorld.callback(0.1, Functor(self.setDefultLens, e.currentTarget))

    def setDefultLens(self, target):
        p = BigWorld.player()
        playerHeight = gameglobal.rds.cam.getPlayerHeight()
        pivotMaxDist = gameglobal.rds.cam.cc.pivotMaxDist
        if target == self.widget.lens.renXiang:
            self.widget.lens.focusSlider.value = RENGXIANG_PARA[0]
            self.widget.lens.jiaojuSlider.value = RENGXIANG_PARA[1]
            self.widget.lens.depthSlider.value = RENGXIANG_PARA[2]
            self.widget.lens.guangquanSlider.value = RENGXIANG_PARA[3]
            if p.model.node('biped Spine1'):
                cameraPivotPositionY = (gameglobal.rds.cam.cc.pivotPosition - gameglobal.rds.cam.cc.position + p.model.node('biped Spine1').position).y
                gameglobal.rds.cam.cc.pivotPosition = (0, cameraPivotPositionY, pivotMaxDist - self.pivotDistRatio * playerHeight)
            else:
                gameglobal.rds.cam.cc.pivotPosition = (0, playerHeight * CAMERA_HEIGHT_NORMAL, pivotMaxDist - self.pivotDistRatio * playerHeight)
        elif target == self.widget.lens.fengJing:
            self.widget.lens.focusSlider.value = FENGJING_PARA[0]
            self.widget.lens.jiaojuSlider.value = FENGJING_PARA[1]
            self.widget.lens.depthSlider.value = FENGJING_PARA[2]
            self.widget.lens.guangquanSlider.value = FENGJING_PARA[3]
            gameglobal.rds.cam.cc.pivotPosition = (0, FENGJING_PARA[4][1], FENGJING_PARA[4][2])
        elif target == self.widget.lens.teXie:
            self.widget.lens.focusSlider.value = TEXIE_PARA[0]
            self.widget.lens.jiaojuSlider.value = TEXIE_PARA[1]
            self.widget.lens.depthSlider.value = TEXIE_PARA[2]
            self.widget.lens.guangquanSlider.value = TEXIE_PARA[3]
            if p.model.node('head_chin'):
                cameraPivotPositionY = (gameglobal.rds.cam.cc.pivotPosition - gameglobal.rds.cam.cc.position + p.model.node('head_chin').position).y
                gameglobal.rds.cam.cc.pivotPosition = (0, cameraPivotPositionY, pivotMaxDist - self.pivotDistRatio * playerHeight)
            else:
                gameglobal.rds.cam.cc.pivotPosition = (0, playerHeight * CAMERA_HEIGHT_TEXIE, pivotMaxDist - self.pivotDistRatio * playerHeight)

    def focusPlayer(self):
        p = BigWorld.player()
        dc = BigWorld.dcursor()
        dc.pitch = 0
        deltaYaw = p.yaw + math.pi
        if deltaYaw > math.pi:
            deltaYaw -= 2 * math.pi
        gameglobal.rds.cam.cc.deltaYaw += deltaYaw - gameglobal.rds.cam.cc.direction.yaw

    def refreshValue(self, *args):
        self.widget.lens.focusSliderMax.text = int(self.widget.lens.focusSlider.value / DOF_FOCUS_PARAM[1] * 100)
        self.widget.lens.jiaojuSliderMax.text = int(self.widget.lens.jiaojuSlider.value / FOV_MAX * 100)
        self.widget.lens.depthSliderMax.text = int(self.widget.lens.depthSlider.value * 100)
        self.widget.lens.guangquanSliderMax.text = int(self.widget.lens.guangquanSlider.value / GUANGQUAN_PARAM[1] * 100)

    def headTitleChange(self, *args):
        selected = not self.widget.display.headTitle.selected
        self.widget.display.nickname.selected = selected
        self.widget.display.designation.selected = selected
        self.widget.display.unionIcon.selected = selected
        self.widget.display.bloodBar.selected = selected
        hideHeadTitle = [self.widget.display.headTitle.selected]
        self.nicknameVisibleChange(hideHeadTitle)
        self.designationVisibleChange(hideHeadTitle)
        self.unionIconVisibleChange(hideHeadTitle)
        self.bloodBarVisibleChange(hideHeadTitle)

    def modelChange(self, *args):
        modelSelected = self.widget.display.model.selected
        self.widget.display.self.selected = modelSelected
        self.widget.display.friends.selected = modelSelected
        self.widget.display.otherPlayer.selected = modelSelected
        self.widget.display.monster.selected = modelSelected
        self.widget.display.npc.selected = modelSelected
        self.widget.display.sprite.selected = modelSelected
        self.friendsVisibleChange()
        self.otherPlayersVisibleChange()
        self.monsterVisibleChange()
        self.npcVisibleChange()
        self.spriteVisibleChange()
        self.selfVisibleChange(modelSelected)

    def visibleChange(self, *args):
        e = ASObject(args[3][0])
        if e.currentTarget == self.widget.display.self:
            self.selfVisibleChange(self.widget.display.self.selected)
        elif e.currentTarget == self.widget.display.friends:
            self.friendsVisibleChange()
        elif e.currentTarget == self.widget.display.otherPlayer:
            self.otherPlayersVisibleChange()
        elif e.currentTarget == self.widget.display.npc:
            self.npcVisibleChange()
        elif e.currentTarget == self.widget.display.monster:
            self.monsterVisibleChange()
        elif e.currentTarget == self.widget.display.sprite:
            self.spriteVisibleChange()
        elif e.currentTarget == self.widget.display.nickname:
            self.nicknameVisibleChange([self.widget.display.nickname.selected])
        elif e.currentTarget == self.widget.display.designation:
            self.designationVisibleChange([self.widget.display.designation.selected])
        elif e.currentTarget == self.widget.display.unionIcon:
            self.unionIconVisibleChange([self.widget.display.unionIcon.selected])
        elif e.currentTarget == self.widget.display.bloodBar:
            self.bloodBarVisibleChange([self.widget.display.bloodBar.selected])

    def selfVisibleChange(self, flag):
        BigWorld.player().hide(not flag)

    def friendsVisibleChange(self):
        self.friendsVisible = not self.friendsVisible
        ent = BigWorld.entities.items()
        members = getattr(BigWorld.player(), 'members', {})
        for eid, e in ent:
            if e.IsAvatar and hasattr(e, 'refreshOpacityState'):
                if hasattr(e, 'gbId') and not e.gbId == BigWorld.player().gbId and e.gbId in members:
                    e.refreshOpacityState()

    def otherPlayersVisibleChange(self):
        self.otherPlayersVisible = not self.otherPlayersVisible
        ent = BigWorld.entities.items()
        members = getattr(BigWorld.player(), 'members', {})
        for eid, e in ent:
            if e.IsAvatar and hasattr(e, 'refreshOpacityState'):
                if hasattr(e, 'gbId') and not e.gbId == BigWorld.player().gbId and e.gbId not in members:
                    e.refreshOpacityState()

    def npcVisibleChange(self):
        self.npcVisible = not self.npcVisible
        ent = BigWorld.entities.items()
        for eid, e in ent:
            if isinstance(e, Npc.Npc):
                e.refreshOpacityState()

    def monsterVisibleChange(self):
        self.monsterVisible = not self.monsterVisible
        ent = BigWorld.entities.items()
        for eid, e in ent:
            if e.IsMonster and hasattr(e, 'refreshOpacityState'):
                e.refreshOpacityState()

    def spriteVisibleChange(self):
        self.spriteVisible = not self.spriteVisible
        ent = BigWorld.entities.items()
        for eid, e in ent:
            if e.IsSummonedSprite and hasattr(e, 'refreshOpacityState'):
                e.refreshOpacityState()

    def refreshModelVisible(self):
        ent = BigWorld.entities.items()
        for eid, e in ent:
            if hasattr(e, 'refreshOpacityState'):
                e.refreshOpacityState()

    def nicknameVisibleChange(self, params):
        while len(params) < 6:
            params.append(params[0])

        p = BigWorld.player()
        p.hidePlayerName(params[0])
        p.hideAvatarName(params[1])
        p.hideMonsterName(params[2])
        p.hideNpcName(params[3])
        p.hideSpriteName(params[4])
        p.hideOtherSpriteName(params[5])

    def designationVisibleChange(self, params):
        while len(params) < 4:
            params.append(params[0])

        p = BigWorld.player()
        p.hidePlayerTitle(params[0])
        p.hideAvatarTitle(params[1])
        p.hideMonsterTitle(params[2])
        p.hideNpcTitle(params[3])

    def unionIconVisibleChange(self, params):
        while len(params) < 2:
            params.append(params[0])

        p = BigWorld.player()
        p.hidePlayerGuild(params[0])
        p.hideAvatarGuild(params[1])

    def bloodBarVisibleChange(self, params):
        while len(params) < 3:
            params.append(params[0])

        p = BigWorld.player()
        forceDo = p.isInBfDota()
        p.hidePlayerBlood(params[0], forceDo)
        p.hideAvatarBlood(params[1], forceDo)
        p.hideMonsterBlood(params[2], forceDo)

    def refreshInfo(self):
        if not self.widget:
            return

    def unselectedAllShaderBtn(self):
        self.widget.lvJing.classicBtn.selected = False
        self.widget.lvJing.standardBtn.selected = False
        self.widget.lvJing.softBtn.selected = False
        self.widget.lvJing.inkBtn.selected = False
        self.widget.lvJing.freshBtn.selected = False
        self.widget.lvJing.darkBtn.selected = False
        self.widget.lvJing.aBaoBtn.selected = False

    def changeShader(self, *args):
        e = ASObject(args[3][0])
        val = e.currentTarget.label
        self.unselectedAllShaderBtn()
        e.currentTarget.selected = True
        index = gameStrings.CAMERA_V2_SHADER.index(val)
        self.widget.lvJing.intensitySlider.value = 10.0
        if index != 0:
            self.widget.lvJing.standardBtn.selected = False
        self.shaderIndex = index
        self.setShaderIndex(index, self.intensity, True)
        gameglobal.rds.ui.topBar.updateMode('renderMode')
        gameglobal.rds.ui.videoSetting.updateMode()
        enable, self.contrast, self.saturation, self.brightness = BigWorld.getColorTransParam()
        self.widget.lvJing.saturationSlider.value = 10.0 * (self.saturation - SHADER_INTERVAL[6]) / (SHADER_INTERVAL[7] - SHADER_INTERVAL[6])
        self.widget.lvJing.brightnessSlider.value = 10.0 * (self.brightness - SHADER_INTERVAL[2]) / (SHADER_INTERVAL[3] - SHADER_INTERVAL[2])
        self.widget.lvJing.contrastSlider.value = 10.0 * (self.contrast - SHADER_INTERVAL[4]) / (SHADER_INTERVAL[5] - SHADER_INTERVAL[4])

    def getFovDist(self, *arg):
        gameglobal.rds.ui.cameraV2.fovSaved = BigWorld.projection().fov
        ret = DOF_FOCUS_PARAM
        ret.extend([FOV_MIN, FOV_MAX, gameglobal.rds.ui.cameraV2.fovSaved])
        ret.extend(DOF_BLUR_PARAM)
        ret.extend(GUANGQUAN_PARAM)
        return ret

    def hideAll(self):
        self.widget.sight.visible = False
        self.widget.lvJing.visible = False
        self.widget.lens.visible = False
        self.widget.display.visible = False
        self.widget.sightBtn.selected = False
        self.widget.lvJingBtn.selected = False
        self.widget.lensBtn.selected = False
        self.widget.displayBtn.selected = False
        self.widget.lightBtn.selected = False

    def handleLvJingSlider(self, *args):
        e = ASObject(args[3][0])
        val = e.currentTarget.value
        sliderName = e.currentTarget.name
        if sliderName == 'intensitySlider':
            self.intensity = val / 10.0 * (SHADER_INTERVAL[1] - SHADER_INTERVAL[0]) + SHADER_INTERVAL[0]
            self.setShaderIndex(self.shaderIndex, self.intensity, True)
            gameglobal.rds.ui.topBar.updateMode('renderMode')
            gameglobal.rds.ui.videoSetting.updateMode()
            self.widget.lvJing.intensityVal.text = int(10 * val)
            if self.intensity < 0.01:
                self.setShaderIndex(0, self.intensity, True)
        elif sliderName == 'brightnessSlider':
            self.brightness = val / 10.0 * (SHADER_INTERVAL[3] - SHADER_INTERVAL[2]) + SHADER_INTERVAL[2]
            self.widget.lvJing.brightnessVal.text = int(10 * val)
        elif sliderName == 'contrastSlider':
            self.contrast = val / 10.0 * (SHADER_INTERVAL[5] - SHADER_INTERVAL[4]) + SHADER_INTERVAL[4]
            self.widget.lvJing.contrastVal.text = int(10 * val)
        elif sliderName == 'saturationSlider':
            self.saturation = val / 10.0 * (SHADER_INTERVAL[7] - SHADER_INTERVAL[6]) + SHADER_INTERVAL[6]
            self.widget.lvJing.saturationVal.text = int(10 * val)
        elif sliderName == 'vignettingSlider':
            self.vignetting = val / 10.0 * (SHADER_INTERVAL[9] - SHADER_INTERVAL[8]) + SHADER_INTERVAL[8]
            self.widget.lvJing.vignettingVal.text = int(10 * val)
        elif sliderName == 'particleSlider':
            self.particle = val / 10.0 * (SHADER_INTERVAL[11] - SHADER_INTERVAL[10]) + SHADER_INTERVAL[10]
            self.widget.lvJing.particleVal.text = int(10 * val)
        elif sliderName == 'softLightSlider':
            self.softLight = val / 10.0 * (SHADER_INTERVAL[13] - SHADER_INTERVAL[12]) + SHADER_INTERVAL[12]
            self.widget.lvJing.softLightVal.text = int(10 * val)
        try:
            BigWorld.colorVibrancePlus(True, self.saturation, self.brightness, self.contrast, 1, 1 - self.intensity)
        except:
            pass

        BigWorld.photoAdjust(True, self.softLight, SHADER_INTERVAL[9] + SHADER_INTERVAL[8] - self.vignetting)
        BigWorld.adjustSharpenEffect(True, self.particle, self.particle)
        if sliderName == 'intensitySlider':
            self.setShaderIndex(self.shaderIndex, self.intensity, True)
            gameglobal.rds.ui.topBar.updateMode('renderMode')
            gameglobal.rds.ui.videoSetting.updateMode()

    def handleLensSlider(self, *args):
        e = ASObject(args[3][0])
        val = e.currentTarget.value
        if e.currentTarget.name == 'guangquanSlider' or e.currentTarget.name == 'focusSlider':
            if e.currentTarget.value >= 1:
                val = math.pow(1.25, e.currentTarget.value)
        self.moveCamera(e.currentTarget.name, val)

    def moveCamera(self, sliderName, val):
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

    def setDof(self, dofFocus, dofRadius, dofMaxBlur = 1.0):
        if not self.isShow or dofRadius == 0:
            return
        if dofRadius >= 3900:
            BigWorld.setDepthOfField(False)
        else:
            BigWorld.setDepthOfField(True, dofFocus, 1.0 / dofRadius, 1, dofMaxBlur, dofMaxBlur)

    def setSliderValue(self, sliderName, value):
        if hasattr(self.widget.lens, sliderName):
            slider = getattr(self.widget.lens, sliderName).value = value

    def changePanel(self, *args):
        e = ASObject(args[3][0])
        tag = e.currentTarget.tag
        self.panelShow(tag)

    def changeMode(self, *args):
        self.expertMode = not self.expertMode
        flag = self.expertMode
        self.widget.displayBtn.visible = flag
        self.widget.lensBtn.visible = flag
        self.widget.lvJingBtn.visible = flag
        self.widget.sightBtn.visible = flag
        self.widget.lens.visible = flag
        self.widget.bg.visible = flag
        if flag == False:
            self.hideAll()
        else:
            self.panelShow(gameglobal.rds.ui.cameraTable.tag)

    def panelShow(self, tag):
        self.hideAll()
        self.tag = tag
        if tag == SIGHT_BTN_TAG:
            self.widget.sight.visible = True
            self.widget.sightBtn.selected = True
        elif tag == DISPLAY_BTN_TAG:
            self.widget.display.visible = True
            self.widget.displayBtn.selected = True
        elif tag == LIGHT_BTN_TAG:
            self.widget.lightBtn.selected = True
        elif tag == LVJING_BTN_TAG:
            self.widget.lvJing.visible = True
            self.widget.lvJingBtn.selected = True
        elif tag == LENS_BTN_TAG:
            self.widget.lens.visible = True
            self.widget.lensBtn.selected = True

    def onGroupMemberChange(self):
        ent = BigWorld.entities.items()
        for eid, e in ent:
            if getattr(e, 'IsAvatar', False):
                if not getattr(e, 'gbId', BigWorld.player().gbId) == BigWorld.player().gbId:
                    e.refreshOpacityState()

    def setShaderIndex(self, index = None, rate = 0.9, needApply = True):
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
           0.05), None, 0.7),
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
        if getattr(p, 'lockShaderIndex', False):
            return
        else:
            p.recoredShaderIndex = (index, True, needApply)
            if needApply and not getattr(p, 'forbidApplyShader', False):
                if param[index][0]:
                    try:
                        BigWorld.colorVibrancePlus(param[index][0][0], param[index][0][1] * rate, param[index][0][2] * rate, param[index][0][3] * rate, 1, 1 - rate)
                        self.contrast = param[index][0][3] * rate
                        self.saturation = param[index][0][1] * rate
                        self.brightness = param[index][0][2] * rate
                        self.widget.lvJing.saturationSlider.value = 10 * (self.saturation - SHADER_INTERVAL[6]) / (SHADER_INTERVAL[7] - SHADER_INTERVAL[6])
                        self.widget.lvJing.brightnessSlider.value = 10 * (self.brightness - SHADER_INTERVAL[2]) / (SHADER_INTERVAL[3] - SHADER_INTERVAL[2])
                        self.widget.lvJing.contrastSlider.value = 10 * (self.contrast - SHADER_INTERVAL[4]) / (SHADER_INTERVAL[5] - SHADER_INTERVAL[4])
                    except:
                        pass

                if param[index][1]:
                    BigWorld.setColorGrading('env/colormap/style/' + param[index][1] + '.tga', rate)
                else:
                    BigWorld.setColorGrading('', 1)
                if param[index][2]:
                    BigWorld.setBloom(True, param[index][2] * rate)
            return

    def isHideFriends(self, gbId):
        if not self.widget:
            return False
        members = getattr(BigWorld.player(), 'members', {})
        return gbId in members and not gbId == BigWorld.player().gbId and not self.friendsVisible

    def isHideOthers(self, gbId):
        if not self.widget:
            return False
        members = getattr(BigWorld.player(), 'members', {})
        return gbId not in members and not gbId == BigWorld.player().gbId and not self.otherPlayersVisible

    def isHideNpcs(self):
        if not self.widget:
            return False
        return not self.npcVisible

    def isHideMonsters(self):
        if not self.widget:
            return False
        return not self.monsterVisible

    def isHideSprites(self):
        if not self.widget:
            return False
        return not self.spriteVisible
