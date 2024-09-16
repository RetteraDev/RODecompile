#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/surfaceSettingV2Proxy.o
import BigWorld
import gameglobal
import gametypes
import events
import const
import uiConst
import keys
import commcalc
import copy
import C_ui
import appSetting
import gamelog
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis import uiUtils
from guis.asObject import ASUtils
from gamestrings import gameStrings
from callbackHelper import Functor
from messageBoxProxy import MBButton
from helpers import outlineHelper
from appSetting import Obj as AppSettings
from cdata import game_msg_def_data as GMDD
from data import game_setting_data as GSD

class SurfaceSettingV2Proxy(UIProxy):
    PlAYER_SETTING = 0
    AVATAR_SETTING = 1
    NPC_MONSTER_SETTING = 2
    SPRITE_SETTING = 3
    OTHER_SPRITE_SETTING = 4
    SHOWMODE_DROP_DATA = [{'label': gameStrings.SURFACESETTING_PlAYER_SETTING,
      'data': gameStrings.SURFACESETTING_PlAYER_SETTING},
     {'label': gameStrings.SURFACESETTING_AVATAR_SETTING,
      'data': gameStrings.SURFACESETTING_AVATAR_SETTING},
     {'label': gameStrings.SURFACESETTING_NPC_MONSTER_SETTING,
      'data': gameStrings.SURFACESETTING_NPC_MONSTER_SETTING},
     {'label': gameStrings.SURFACESETTING_SPRITE_SETTING,
      'data': gameStrings.SURFACESETTING_SPRITE_SETTING},
     {'label': gameStrings.SURFACESETTING_OTHER_SPRITE_SETTING,
      'data': gameStrings.SURFACESETTING_OTHER_SPRITE_SETTING}]
    originPosition1 = [150, 217]
    originPosition2 = [150, 366]
    xOffset = 240
    yOffset = 26
    checkVisible1 = ['ckBoxMap',
     'hpShowMode',
     'ckBoxItemBar',
     'ckBoxOutline',
     'ckBoxItemBar2',
     'ckBoxCCMiniShow',
     'ckBoxTargetLockedEff',
     'ckBoxPathTrace',
     'ckLowLvQuest',
     'ckBoxHpShow']
    checkVisible2 = ['ckBoxDisableSemanticsRecognition',
     'ckBoxLittlemapHit',
     'ckBoxLookAt',
     'ckEnableRandWing',
     'ckBoxTeamOpenCC',
     'ckBoxZhanchangOpenCC',
     'ckBoxCCQuitConfirm',
     'ckBoxBossKey',
     'ckBoxErrorSound',
     'ckBlockFirework',
     'ckBlockSkillAppearance']
    defaultSetting = {'ckBoxPlayerBlood': 1,
     'ckBoxPlayerName': 0,
     'ckBoxPlayerGuild': 0,
     'ckBoxPlayerTitle': 0,
     'ckBoxAvatarBlood': 1,
     'ckBoxAvatarName': 1,
     'ckBoxAvatarGuild': 1,
     'ckBoxAvatarTitle': 1,
     'ckBoxOtherEntityBlood': 1,
     'ckBoxOtherEntityName': 1,
     'ckBoxOtherEntityGuild': 0,
     'ckBoxOtherEntityTitle': 1,
     'armorMode': 1,
     'showSelfArmor': 1,
     'ckBoxMap': 1,
     'ckBoxLittlemapHit': 0,
     'ckBoxItemBar': 1,
     'ckBoxPathTrace': 0,
     'ckBoxOutline': 0,
     'hpShowMode': 0,
     'uiSizeSlider': 1.0,
     'headNameSizeSlider': 15.0,
     'walkSpeedSlider': 3.0,
     'cameraSlider': 3.0,
     'ckBoxLookAt': 1,
     'ckBoxErrorSound': 1,
     'ckBoxBossKey': 1,
     'comBoxSelectMode': 0,
     'ckBoxTargetLockedEff': 1,
     'ckBoxDisableModelRoll': 0,
     'ckBoxTeamOpenCC': 1,
     'ckBoxItemBar2': 0,
     'ckLowLvQuest': 0,
     'ckBoxZhanchangOpenCC': 0,
     'ckBlockFirework': 0,
     'ckBlockSkillAppearance': 0,
     'ckEnableRandWing': 0,
     'ckBoxDisableSemanticsRecognition': 0,
     'ckBoxCCQuitConfirm': 0,
     'ckBoxCCMiniShow': 0,
     'ckBoxSpriteBlood': 1,
     'ckBoxSpriteName': 1,
     'ckBoxOtherSpriteBlood': 1,
     'ckBoxOtherSpriteName': 1,
     'ckBoxHpShow': 1}

    def __init__(self, uiAdapter):
        super(SurfaceSettingV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.mainMc = None
        self.data = {}
        self.newData = {}
        self.oldSelectMode = -1
        self.maxResolution = []
        self.selectMode = self.PlAYER_SETTING

    def initPanel(self, widget):
        self.widget = widget
        self.mainMc = widget.canvas
        self.mainMc.showMode.selectedIndex = 0
        ASUtils.setDropdownMenuData(self.mainMc.showMode, self.SHOWMODE_DROP_DATA)
        self.mainMc.showMode.addEventListener(events.INDEX_CHANGE, self.handleShowModeClick)
        self.mainMc.showMode.validateNow()
        self.mainMc.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick)
        self.mainMc.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancleBtnClick)
        self.mainMc.defaultBtn.addEventListener(events.BUTTON_CLICK, self.handleDefaultBtnClick)
        self.mainMc.applyBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyBtnClick)
        self.mainMc.uiSizeSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleUISizeSlider)
        self.mainMc.uiSizeSlider.value = 100
        self.mainMc.headNameSizeSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleHeadNameSizeSlider)
        self.mainMc.headNameSizeSlider.value = 16
        self.mainMc.walkSpeedSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleWalkSpeedSlider)
        self.mainMc.walkSpeedSlider.value = 3.0
        self.mainMc.cameraSlider.addEventListener(events.EVENT_VALUE_CHANGE, self.handleCameraSlider)
        self.mainMc.cameraSlider.value = 3.0
        TipManager.addTip(self.mainMc.ckEnableRandWing, gameStrings.CKENABLERANDWING_TIP)
        self.data = self.getSurfaceConfigData()
        self.newData = copy.deepcopy(self.data)
        self.refreshUI(self.newData)
        self.setDefaultSettingData()
        self.refreshVisible()

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

    def handleShowModeClick(self, *args):
        if self.oldSelectMode == 0:
            self.newData['ckBoxPlayerBlood'] = 1 if self.mainMc.ckBoxPlayerBlood.selected else 0
            self.newData['ckBoxPlayerName'] = 1 if self.mainMc.ckBoxPlayerName.selected else 0
            self.newData['ckBoxPlayerGuild'] = 1 if self.mainMc.ckBoxPlayerGuild.selected else 0
            self.newData['ckBoxPlayerTitle'] = 1 if self.mainMc.ckBoxPlayerTitle.selected else 0
            self.newData['showSelfArmor'] = 1 if self.mainMc.showSelfArmor.selected else 0
        elif self.oldSelectMode == 1:
            self.newData['ckBoxAvatarBlood'] = 1 if self.mainMc.ckBoxPlayerBlood.selected else 0
            self.newData['ckBoxAvatarName'] = 1 if self.mainMc.ckBoxPlayerName.selecte else 0
            self.newData['ckBoxAvatarGuild'] = 1 if self.mainMc.ckBoxPlayerGuild.selected else 0
            self.newData['ckBoxAvatarTitle'] = 1 if self.mainMc.ckBoxPlayerTitle.selectedelse else 0
        elif self.oldSelectMode == 2:
            self.newData['ckBoxOtherEntityBlood'] = 1 if self.mainMc.ckBoxPlayerBlood.selected else 0
            self.newData['ckBoxOtherEntityName'] = 1 if self.mainMc.ckBoxPlayerName.selected else 0
            self.newData['ckBoxOtherEntityTitle'] = 1 if self.mainMc.ckBoxPlayerTitle.selectedelse else 0
        elif self.oldSelectMode == 3:
            self.newData['ckBoxSpriteBlood'] = 1 if self.mainMc.ckBoxPlayerBlood.selected else 0
            self.newData['ckBoxSpriteName'] = 1 if self.mainMc.ckBoxPlayerName.selected else 0
        elif self.oldSelectMode == 4:
            self.newData['ckBoxOtherSpriteBlood'] = 1 if self.mainMc.ckBoxPlayerBlood.selected else 0
            self.newData['ckBoxOtherSpriteName'] = 1 if self.mainMc.ckBoxPlayerName.selected else 0
        self.newData['comBoxSelectMode'] = self.mainMc.showMode.selectedIndex
        self.refreshUI(self.newData)

    def handleConfirmBtnClick(self, *args):
        self.handleApplyBtnClick(*args)
        gameglobal.rds.ui.gameSetting.hide(True)
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def handleCancleBtnClick(self, *args):
        gameglobal.rds.ui.gameSetting.hide(True)
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def handleDefaultBtnClick(self, *args):
        self.newData = copy.deepcopy(self.defaultSetting)
        self.refreshUI(self.newData)

    def setDefaultSettingData(self):
        defaultSettingData = GSD.data.get('commonSetting', [])
        if defaultSettingData:
            if hasattr(BigWorld.player(), 'getOperationMode') and BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
                self.defaultSetting['ckBoxPlayerName'] = 0
                self.defaultSetting['ckBoxPlayerTitle'] = 0
                self.defaultSetting['ckBoxPlayerGuild'] = 0
            else:
                self.defaultSetting['ckBoxPlayerName'] = defaultSettingData[2]
                self.defaultSetting['ckBoxPlayerTitle'] = defaultSettingData[3]
                self.defaultSetting['ckBoxPlayerGuild'] = defaultSettingData[15]
            self.defaultSetting['ckBoxPathTrace'] = defaultSettingData[1]
            self.defaultSetting['ckBoxPlayerBlood'] = defaultSettingData[4]
            self.defaultSetting['ckBoxAvatarName'] = defaultSettingData[5]
            self.defaultSetting['ckBoxAvatarTitle'] = defaultSettingData[6]
            self.defaultSetting['ckBoxAvatarBlood'] = defaultSettingData[7]
            self.defaultSetting['ckBoxOtherEntityName'] = defaultSettingData[8]
            self.defaultSetting['ckBoxOtherEntityTitle'] = defaultSettingData[9]
            self.defaultSetting['ckBoxOtherEntityBlood'] = defaultSettingData[10]
            self.defaultSetting['ckBoxItemBar'] = defaultSettingData[11]
            self.defaultSetting['ckBoxMap'] = defaultSettingData[12]
            self.defaultSetting['ckBoxErrorSound'] = defaultSettingData[13]
            self.defaultSetting['cameraSlider'] = defaultSettingData[14]
            self.defaultSetting['ckBoxAvatarGuild'] = defaultSettingData[16]
            self.defaultSetting['armorMode'] = defaultSettingData[17]
            self.defaultSetting['showSelfArmor'] = defaultSettingData[18]
            self.defaultSetting['walkSpeedSlider'] = defaultSettingData[19]
            self.defaultSetting['ckBoxItemBar2'] = defaultSettingData[20]
            self.defaultSetting['ckBoxSpriteBlood'] = defaultSettingData[33]
            self.defaultSetting['ckBoxSpriteName'] = defaultSettingData[34]
            self.defaultSetting['ckBoxOtherSpriteBlood'] = defaultSettingData[35]
            self.defaultSetting['ckBoxOtherSpriteName'] = defaultSettingData[36]

    def handleApplyBtnClick(self, *args):
        self.ui2Data(self.newData)
        self.settingApply(self.newData)
        AppSettings[keys.SET_HIDE_PLAYER_NAME] = int(self.data['ckBoxPlayerName'])
        AppSettings[keys.SET_HIDE_PLAYER_TITLE] = int(self.data['ckBoxPlayerTitle'])
        AppSettings[keys.SET_HIDE_PLAYER_BLOOD] = int(self.data['ckBoxPlayerBlood'])
        AppSettings[keys.SET_HIDE_PLAYER_GUILD] = int(self.data['ckBoxPlayerGuild'])
        AppSettings[keys.SET_HIDE_AVATAR_NAME] = int(self.data['ckBoxAvatarName'])
        AppSettings[keys.SET_HIDE_AVATAR_TITLE] = int(self.data['ckBoxAvatarTitle'])
        AppSettings[keys.SET_HIDE_AVATAR_BLOOD] = int(self.data['ckBoxAvatarBlood'])
        AppSettings[keys.SET_HIDE_AVATAR_GUILD] = int(self.data['ckBoxAvatarGuild'])
        AppSettings[keys.SET_HIDE_OTHERENTITY_NAME] = int(self.data['ckBoxOtherEntityName'])
        AppSettings[keys.SET_HIDE_OTHERENTITY_TITLE] = int(self.data['ckBoxOtherEntityTitle'])
        AppSettings[keys.SET_HIDE_OTHERENTITY_BLOOD] = int(self.data['ckBoxOtherEntityBlood'])
        AppSettings[keys.SET_HIDE_SPRITE_BLOOD] = int(self.data['ckBoxSpriteBlood'])
        AppSettings[keys.SET_HIDE_OTHERSPRITE_NAME] = int(self.data['ckBoxOtherSpriteName'])
        AppSettings[keys.SET_HIDE_OTHERSPRITE_BLOOD] = int(self.data['ckBoxOtherSpriteBlood'])
        AppSettings[keys.SET_TARGET_LOCKED_EFF] = int(self.data['ckBoxTargetLockedEff'])
        AppSettings[keys.SET_SELECT_MODE] = int(self.data['comBoxSelectMode'])
        AppSettings[keys.SET_PATH_TRACE] = int(self.data['ckBoxPathTrace'])
        AppSettings[keys.SET_SHORTCUT_BAR] = int(self.data['ckBoxItemBar'])
        AppSettings[keys.SET_LITTLE_MAP] = int(self.data['ckBoxMap'])
        AppSettings[keys.SET_ERROR_SOUND] = int(self.data['ckBoxErrorSound'])
        AppSettings[keys.SET_BOSS_KEY] = int(self.data['ckBoxBossKey'])
        AppSettings[keys.SET_ARMORMODE_SELF] = int(self.data['showSelfArmor'])
        AppSettings[keys.SET_OUTLINE] = int(self.data['ckBoxOutline'])
        AppSettings[keys.SET_LITTLE_MAP_UNHIT_ABLE] = int(self.data['ckBoxLittlemapHit'])
        AppSettings[keys.SET_LOOK_AT] = int(self.data['ckBoxLookAt'])
        AppSettings[keys.SET_HP_MODE] = int(self.data['hpShowMode'])
        AppSettings[keys.SET_HP_SHOW] = int(self.data['ckBoxHpShow'])
        AppSettings[keys.SET_UI_SCALEDATA_SCALE] = self.data['uiSizeSlider']
        AppSettings[keys.SET_UI_SCALEDATA_TOPLOGO] = self.data['headNameSizeSlider']
        AppSettings[keys.SET_CAMERA_SENS] = self.data['cameraSlider']
        AppSettings[keys.SET_WALK_SPEED] = self.data['walkSpeedSlider']
        AppSettings[keys.SET_BLOCK_FIREWORK] = int(self.data['ckBlockFirework'])
        AppSettings[keys.SET_BLOCK_SKILL_APPEARANCE] = int(self.data['ckBlockSkillAppearance'])
        AppSettings[keys.SET_ENABLE_RAND_WING] = int(self.data['ckEnableRandWing'])
        AppSettings[keys.SET_TEAM_OPEN_CC] = int(self.data['ckBoxTeamOpenCC'])
        AppSettings[keys.SET_CC_QUIT_CONFIRM] = int(self.data['ckBoxCCQuitConfirm'])
        AppSettings[keys.SET_CC_MINI_SHOW] = int(self.data['ckBoxCCMiniShow'])
        AppSettings[keys.SET_ZHANCHANG_OPEN_CC] = int(self.data['ckBoxZhanchangOpenCC'])
        AppSettings[keys.SET_DISABLE_SEMANTICS_RECOGNITION] = int(self.data['ckBoxDisableSemanticsRecognition'])
        AppSettings.save()
        self.updateCommonSettingOperation()
        BigWorld.player().fashion.resetModelRoll()

    def settingApply(self, data):
        p = BigWorld.player()
        if data['uiSizeSlider'] != self.data['uiSizeSlider']:
            self.data['uiSizeSlider'] = data['uiSizeSlider']
            gameglobal.rds.ui.setManualScale(self.data['uiSizeSlider'], True)
        if data['ckBoxDisableSemanticsRecognition'] != self.data['ckBoxDisableSemanticsRecognition']:
            self.data['ckBoxDisableSemanticsRecognition'] = data['ckBoxDisableSemanticsRecognition']
        if data['comBoxSelectMode'] != self.data['comBoxSelectMode']:
            self.selectMode = data['comBoxSelectMode']
            self.data['comBoxSelectMode'] = data['comBoxSelectMode']
        if data['ckBoxPathTrace'] != self.data['ckBoxPathTrace']:
            appSetting.DebugSettingObj.openPathTrace(data['ckBoxPathTrace'], False)
            self.data['ckBoxPathTrace'] = data['ckBoxPathTrace']
        if self.selectMode == self.PlAYER_SETTING:
            if data['ckBoxPlayerName'] != self.data['ckBoxPlayerName']:
                p.hidePlayerName(not data['ckBoxPlayerName'])
                self.data['ckBoxPlayerName'] = data['ckBoxPlayerName']
            if data['ckBoxPlayerTitle'] != self.data['ckBoxPlayerTitle']:
                p.hidePlayerTitle(not data['ckBoxPlayerTitle'])
                self.data['ckBoxPlayerTitle'] = data['ckBoxPlayerTitle']
            if data['ckBoxPlayerBlood'] != self.data['ckBoxPlayerBlood']:
                p.hidePlayerBlood(not data['ckBoxPlayerBlood'])
                self.data['ckBoxPlayerBlood'] = data['ckBoxPlayerBlood']
            if data['ckBoxPlayerGuild'] != self.data['ckBoxPlayerGuild']:
                p.hidePlayerGuild(not data['ckBoxPlayerGuild'])
                self.data['ckBoxPlayerGuild'] = data['ckBoxPlayerGuild']
        elif self.selectMode == self.AVATAR_SETTING:
            if data['ckBoxAvatarName'] != self.data['ckBoxAvatarName']:
                p.hideAvatarName(not data['ckBoxAvatarName'])
                self.data['ckBoxAvatarName'] = data['ckBoxAvatarName']
            if data['ckBoxAvatarTitle'] != self.data['ckBoxAvatarTitle']:
                p.hideAvatarTitle(not data['ckBoxAvatarTitle'])
                self.data['ckBoxAvatarTitle'] = data['ckBoxAvatarTitle']
            if data['ckBoxAvatarBlood'] != self.data['ckBoxAvatarBlood']:
                p.hideAvatarBlood(not data['ckBoxAvatarBlood'])
                self.data['ckBoxAvatarBlood'] = data['ckBoxAvatarBlood']
            if data['ckBoxAvatarGuild'] != self.data['ckBoxAvatarGuild']:
                p.hideAvatarGuild(not data['ckBoxAvatarGuild'])
                self.data['ckBoxAvatarGuild'] = data['ckBoxAvatarGuild']
        elif self.selectMode == self.NPC_MONSTER_SETTING:
            if data['ckBoxOtherEntityName'] != self.data['ckBoxOtherEntityName']:
                p.hideMonsterName(not data['ckBoxOtherEntityName'])
                p.hideNpcName(not data['ckBoxOtherEntityName'])
                self.data['ckBoxOtherEntityName'] = data['ckBoxOtherEntityName']
            if data['ckBoxOtherEntityTitle'] != self.data['ckBoxOtherEntityTitle']:
                p.hideMonsterTitle(not data['ckBoxOtherEntityTitle'])
                p.hideNpcTitle(not data['ckBoxOtherEntityTitle'])
                self.data['ckBoxOtherEntityTitle'] = data['ckBoxOtherEntityTitle']
            if data['ckBoxOtherEntityBlood'] != self.data['ckBoxOtherEntityBlood']:
                p.hideMonsterBlood(not data['ckBoxOtherEntityBlood'])
                self.data['ckBoxOtherEntityBlood'] = data['ckBoxOtherEntityBlood']
        elif self.selectMode == self.SPRITE_SETTING:
            if data['ckBoxSpriteBlood'] != self.data['ckBoxSpriteBlood']:
                p.hideSpriteBlood(not data['ckBoxSpriteBlood'])
                self.data['ckBoxSpriteBlood'] = data['ckBoxSpriteBlood']
            if data['ckBoxSpriteName'] != self.data['ckBoxSpriteName']:
                p.hideSpriteName(not data['ckBoxSpriteName'])
                self.data['ckBoxSpriteName'] = data['ckBoxSpriteName']
        elif self.selectMode == self.OTHER_SPRITE_SETTING:
            if data['ckBoxOtherSpriteBlood'] != self.data['ckBoxOtherSpriteBlood']:
                p.hideOtherSpriteBlood(not data['ckBoxOtherSpriteBlood'])
                self.data['ckBoxOtherSpriteBlood'] = data['ckBoxOtherSpriteBlood']
            if data['ckBoxOtherSpriteName'] != self.data['ckBoxOtherSpriteName']:
                p.hideOtherSpriteName(not data['ckBoxOtherSpriteName'])
                self.data['ckBoxOtherSpriteName'] = data['ckBoxOtherSpriteName']
        if data['ckBoxItemBar'] != self.data['ckBoxItemBar']:
            gameglobal.rds.ui.actionbar.setItemMcVisible(0, data['ckBoxItemBar'])
            self.data['ckBoxItemBar'] = data['ckBoxItemBar']
        if data['ckBoxItemBar2'] != self.data['ckBoxItemBar2']:
            gameglobal.rds.ui.actionbar.setItemMcVisible(1, data['ckBoxItemBar2'])
            self.data['ckBoxItemBar2'] = data['ckBoxItemBar2']
        if data['ckBoxMap'] != self.data['ckBoxMap']:
            gameglobal.rds.ui.map.littleMapState = data['ckBoxMap']
            self.data['ckBoxMap'] = data['ckBoxMap']
            gameglobal.rds.ui.littleMap.littleMapStateChanged()
        if data['ckBoxErrorSound'] != self.data['ckBoxErrorSound']:
            gameglobal.ENABLE_ERROR_SOUND = data['ckBoxErrorSound']
            self.data['ckBoxErrorSound'] = data['ckBoxErrorSound']
        if data['ckBoxBossKey'] != self.data['ckBoxBossKey']:
            self.data['ckBoxBossKey'] = data['ckBoxBossKey']
            self.setBossKeyRegisterState(data['ckBoxBossKey'])
        if data['hpShowMode'] != self.data['hpShowMode']:
            gameglobal.rds.ui.player.setHpMode(data['hpShowMode'])
            gameglobal.rds.ui.target.setHpMode(data['hpShowMode'])
            gameglobal.rds.ui.subTarget.setHpMode(data['hpShowMode'])
            self.data['hpShowMode'] = data['hpShowMode']
        if data['showSelfArmor'] != self.data['showSelfArmor']:
            self.data['showSelfArmor'] = data['showSelfArmor']
            uiUtils.setClanWarArmorSelfMode(self.data['showSelfArmor'])
        if data['ckBoxOutline'] != self.data['ckBoxOutline']:
            gameglobal.OUTLINIE_FOR_LOCK_TARGET = data['ckBoxOutline']
            if gameglobal.OUTLINIE_FOR_LOCK_TARGET:
                outlineHelper.setLockedTarget()
            else:
                outlineHelper.clearLockedTarget()
            self.data['ckBoxOutline'] = data['ckBoxOutline']
        if data['ckBoxLittlemapHit'] != self.data['ckBoxLittlemapHit']:
            gameglobal.LITTLE_MAP_UNHIT_ABLE = data['ckBoxLittlemapHit']
            self.data['ckBoxLittlemapHit'] = data['ckBoxLittlemapHit']
            gameglobal.rds.ui.littleMap.refreshActive()
        if data['ckBoxLookAt'] != self.data['ckBoxLookAt']:
            p.modelServer.poseManager.setLookAtEnable(data['ckBoxLookAt'])
            self.data['ckBoxLookAt'] = data['ckBoxLookAt']
        if data['headNameSizeSlider'] != self.data['headNameSizeSlider']:
            self.data['headNameSizeSlider'] = data['headNameSizeSlider']
            gameglobal.rds.ui.setTopLogoFontSize(self.data['headNameSizeSlider'])
        if data['walkSpeedSlider'] != self.data['walkSpeedSlider']:
            p.updateWalkSpeed(data['walkSpeedSlider'])
            self.data['walkSpeedSlider'] = data['walkSpeedSlider']
        if data['cameraSlider'] != self.data['cameraSlider']:
            p.setCameraSensitivity(data['cameraSlider'])
            gameglobal.SHAKE_CAMERA_STRENGTH = data['cameraSlider']
            self.data['cameraSlider'] = data['cameraSlider']
        if data['ckBoxTargetLockedEff'] != self.data['ckBoxTargetLockedEff']:
            gameglobal.ENABLE_TARGET_LOCKED_EFFECT = data['ckBoxTargetLockedEff']
            self.data['ckBoxTargetLockedEff'] = data['ckBoxTargetLockedEff']
        if data['ckBlockFirework'] != self.data['ckBlockFirework']:
            self.data['ckBlockFirework'] = data['ckBlockFirework']
        if data['ckBlockSkillAppearance'] != self.data['ckBlockSkillAppearance']:
            self.data['ckBlockSkillAppearance'] = data['ckBlockSkillAppearance']
        if data['ckEnableRandWing'] != self.data['ckEnableRandWing']:
            self.data['ckEnableRandWing'] = data['ckEnableRandWing']
        enable = data['ckEnableRandWing']
        BigWorld.player().cell.updateRandWingEnable(enable)
        if int(data['ckBoxTeamOpenCC']) != self.data['ckBoxTeamOpenCC']:
            self.data['ckBoxTeamOpenCC'] = data['ckBoxTeamOpenCC']
            gameglobal.JOIN_TEAM_OPEN_CC = bool(self.data['ckBoxTeamOpenCC'])
        if int(data['ckBoxCCQuitConfirm']) != self.data['ckBoxCCQuitConfirm']:
            self.data['ckBoxCCQuitConfirm'] = data['ckBoxCCQuitConfirm']
        if int(data['ckBoxCCMiniShow']) != self.data['ckBoxCCMiniShow']:
            self.data['ckBoxCCMiniShow'] = data['ckBoxCCMiniShow']
        if int(data['ckLowLvQuest']) != self.data['ckLowLvQuest']:
            gameglobal.rds.ui.littleMap.refreshNpcPos()
            self.data['ckLowLvQuest'] = data['ckLowLvQuest']
            gameglobal.LOW_LV_QUEST_MAP = bool(self.data['ckLowLvQuest'])
        if int(data['ckBoxZhanchangOpenCC']) != self.data['ckBoxZhanchangOpenCC']:
            self.data['ckBoxZhanchangOpenCC'] = data['ckBoxZhanchangOpenCC']
            gameglobal.JOIN_ZHANCHANG_OPEN_CC = bool(self.data['ckBoxZhanchangOpenCC'])
        if data['ckBoxHpShow'] != self.data['ckBoxHpShow']:
            gameglobal.rds.ui.player.changeHpTextShow(data['ckBoxHpShow'])
            self.data['ckBoxHpShow'] = data['ckBoxHpShow']

    def setBossKeyRegisterState(self, state):
        if state:
            if hasattr(BigWorld, 'registerBossKey'):
                BigWorld.registerBossKey('CTRL + F10')
        elif hasattr(BigWorld, 'unregisterBossKey'):
            BigWorld.unregisterBossKey('CTRL + F10')

    def updateCommonSettingOperation(self):
        p = BigWorld.player()
        p.setSavedOperationMode(p.getOperationMode())
        p.operation['commonSetting'][1] = self.data['ckBoxPathTrace']
        p.operation['commonSetting'][2] = self.data['ckBoxPlayerName']
        p.operation['commonSetting'][3] = self.data['ckBoxPlayerTitle']
        p.operation['commonSetting'][4] = self.data['ckBoxPlayerBlood']
        p.operation['commonSetting'][5] = self.data['ckBoxAvatarName']
        p.operation['commonSetting'][6] = self.data['ckBoxAvatarTitle']
        p.operation['commonSetting'][7] = self.data['ckBoxAvatarBlood']
        p.operation['commonSetting'][8] = self.data['ckBoxOtherEntityName']
        p.operation['commonSetting'][9] = self.data['ckBoxOtherEntityTitle']
        p.operation['commonSetting'][10] = self.data['ckBoxOtherEntityBlood']
        p.operation['commonSetting'][11] = self.data['ckBoxItemBar']
        p.operation['commonSetting'][12] = self.data['ckBoxMap']
        p.operation['commonSetting'][13] = self.data['ckBoxErrorSound']
        p.operation['commonSetting'][14] = self.data['cameraSlider']
        p.operation['commonSetting'][15] = self.data['ckBoxPlayerGuild']
        p.operation['commonSetting'][16] = self.data['ckBoxAvatarGuild']
        p.operation['commonSetting'][18] = self.data['showSelfArmor']
        p.operation['commonSetting'][19] = self.data['walkSpeedSlider']
        p.operation['commonSetting'][20] = self.data['ckBoxItemBar2']
        p.operation['commonSetting'][21] = self.data['ckLowLvQuest']
        p.operation['commonSetting'][const.COMMON_SETTING_INDEX_ENABLE_NOTIFY_FRIEND_ONLINE_STATUS] = -1
        p.operation['commonSetting'][33] = self.data['ckBoxSpriteBlood']
        p.operation['commonSetting'][34] = self.data['ckBoxSpriteName']
        p.operation['commonSetting'][35] = self.data['ckBoxOtherSpriteBlood']
        p.operation['commonSetting'][36] = self.data['ckBoxOtherSpriteName']
        p.sendOperation()

    def handleUISizeSlider(self, *args):
        self.mainMc.uiSizeText.text = str(int(self.mainMc.uiSizeSlider.value)) + '%'

    def handleHeadNameSizeSlider(self, *args):
        self.mainMc.headNameSizeText.text = str(int(self.mainMc.headNameSizeSlider.value))

    def handleWalkSpeedSlider(self, *args):
        self.mainMc.walkSpeedSliderText.text = str(int(self.mainMc.walkSpeedSlider.value))

    def handleCameraSlider(self, *args):
        self.mainMc.cameraSliderText.text = str(int(self.mainMc.cameraSlider.value))

    def getSurfaceConfigData(self):
        p = BigWorld.player()
        data = {}
        data['comBoxSelectMode'] = self.PlAYER_SETTING
        data['ckBoxOutline'] = AppSettings.get(keys.SET_OUTLINE, 0)
        data['ckBoxLittlemapHit'] = AppSettings.get(keys.SET_LITTLE_MAP_UNHIT_ABLE, 0)
        data['ckBoxLookAt'] = AppSettings.get(keys.SET_LOOK_AT, 1)
        data['uiSizeSlider'] = AppSettings.get(keys.SET_UI_SCALEDATA_SCALE, 1.0)
        data['headNameSizeSlider'] = AppSettings.get(keys.SET_UI_SCALEDATA_TOPLOGO, uiConst.DEFAULT_FONT_SIZE)
        data['ckBoxTargetLockedEff'] = AppSettings.get(keys.SET_TARGET_LOCKED_EFF, 1)
        data['ckBoxBossKey'] = AppSettings.get(keys.SET_BOSS_KEY, 1)
        data['hpShowMode'] = AppSettings.get(keys.SET_HP_MODE, 0)
        data['ckBoxHpShow'] = AppSettings.get(keys.SET_HP_SHOW, 1)
        data['ckBoxTeamOpenCC'] = AppSettings.get(keys.SET_TEAM_OPEN_CC, 1)
        data['ckBoxCCQuitConfirm'] = AppSettings.get(keys.SET_CC_QUIT_CONFIRM, 0)
        data['ckBoxCCMiniShow'] = AppSettings.get(keys.SET_CC_MINI_SHOW, 0)
        data['ckBoxZhanchangOpenCC'] = AppSettings.get(keys.SET_ZHANCHANG_OPEN_CC, 0)
        data['ckBlockFirework'] = AppSettings.get(keys.SET_BLOCK_FIREWORK, 0)
        data['ckBlockSkillAppearance'] = AppSettings.get(keys.SET_BLOCK_SKILL_APPEARANCE, 0)
        data['ckEnableRandWing'] = AppSettings.get(keys.SET_ENABLE_RAND_WING, 0)
        data['ckBoxDisableSemanticsRecognition'] = AppSettings.get(keys.SET_DISABLE_SEMANTICS_RECOGNITION, 0)
        data['ckBoxPathTrace'] = p.operation['commonSetting'][1]
        data['ckBoxPlayerName'] = p.operation['commonSetting'][2]
        data['ckBoxPlayerTitle'] = p.operation['commonSetting'][3]
        data['ckBoxPlayerBlood'] = p.operation['commonSetting'][4]
        data['ckBoxAvatarName'] = p.operation['commonSetting'][5]
        data['ckBoxAvatarTitle'] = p.operation['commonSetting'][6]
        data['ckBoxAvatarBlood'] = p.operation['commonSetting'][7]
        data['ckBoxOtherEntityName'] = p.operation['commonSetting'][8]
        data['ckBoxOtherEntityTitle'] = p.operation['commonSetting'][9]
        data['ckBoxOtherEntityBlood'] = p.operation['commonSetting'][10]
        data['ckBoxItemBar'] = p.operation['commonSetting'][11]
        data['ckBoxMap'] = p.operation['commonSetting'][12]
        data['ckBoxErrorSound'] = p.operation['commonSetting'][13]
        data['cameraSlider'] = p.operation['commonSetting'][14]
        data['ckBoxPlayerGuild'] = p.operation['commonSetting'][15]
        data['ckBoxAvatarGuild'] = p.operation['commonSetting'][16]
        data['showSelfArmor'] = p.operation['commonSetting'][18]
        data['walkSpeedSlider'] = p.operation['commonSetting'][19]
        data['ckBoxItemBar2'] = p.operation['commonSetting'][20]
        data['ckLowLvQuest'] = p.operation['commonSetting'][21]
        data['ckBoxSpriteBlood'] = p.operation['commonSetting'][33]
        data['ckBoxSpriteName'] = p.operation['commonSetting'][34]
        data['ckBoxOtherSpriteBlood'] = p.operation['commonSetting'][35]
        data['ckBoxOtherSpriteName'] = p.operation['commonSetting'][36]
        self.selectMode = data['comBoxSelectMode']
        p.fashion.resetModelRoll()
        return data

    def refreshUI(self, data):
        self.mainMc.showMode.selectedIndex = data['comBoxSelectMode']
        self.mainMc.showSelfArmor.selected = data['showSelfArmor']
        self.mainMc.ckBoxMap.selected = data['ckBoxMap']
        self.mainMc.ckBoxLittlemapHit.selected = data['ckBoxLittlemapHit']
        self.mainMc.ckBoxItemBar.selected = data['ckBoxItemBar']
        self.mainMc.ckBoxItemBar2.selected = data['ckBoxItemBar2']
        self.mainMc.ckBoxPathTrace.selected = data['ckBoxPathTrace']
        self.mainMc.ckBoxOutline.selected = data['ckBoxOutline']
        self.mainMc.hpShowMode.selected = data['hpShowMode']
        self.mainMc.ckBoxHpShow.selected = data['ckBoxHpShow']
        self.mainMc.uiSizeSlider.enabled = True
        self.mainMc.uiSizeSlider.value = data['uiSizeSlider'] * 100
        self.mainMc.headNameSizeSlider.value = int(data['headNameSizeSlider'])
        self.mainMc.walkSpeedSlider.value = data['walkSpeedSlider']
        self.mainMc.cameraSlider.value = data['cameraSlider']
        self.mainMc.ckBoxLookAt.selected = data['ckBoxLookAt']
        self.mainMc.ckBoxErrorSound.selected = data['ckBoxErrorSound']
        self.mainMc.ckBoxBossKey.selected = data['ckBoxBossKey']
        self.mainMc.ckBoxTargetLockedEff.selected = data['ckBoxTargetLockedEff']
        self.mainMc.ckBlockFirework.selected = data['ckBlockFirework']
        self.mainMc.ckBlockSkillAppearance.selected = data['ckBlockSkillAppearance']
        self.mainMc.ckEnableRandWing.selected = data['ckEnableRandWing']
        self.mainMc.ckBoxTeamOpenCC.selected = data['ckBoxTeamOpenCC']
        self.mainMc.ckBoxZhanchangOpenCC.selected = data['ckBoxZhanchangOpenCC']
        self.mainMc.ckBoxCCQuitConfirm.selected = data['ckBoxCCQuitConfirm']
        self.mainMc.ckBoxCCMiniShow.selected = data['ckBoxCCMiniShow']
        self.mainMc.ckLowLvQuest.selected = data['ckLowLvQuest']
        self.mainMc.ckBoxDisableSemanticsRecognition.selected = data['ckBoxDisableSemanticsRecognition']
        if self.mainMc.showMode.selectedIndex == 1:
            self.mainMc.ckBoxPlayerGuild.enabled = True
            self.mainMc.ckBoxPlayerTitle.enabled = True
            self.mainMc.showSelfArmor.enabled = False
            self.mainMc.showSelfArmor.selected = False
            self.mainMc.ckBoxPlayerBlood.selected = data['ckBoxAvatarBlood']
            self.mainMc.ckBoxPlayerName.selected = data['ckBoxAvatarName']
            self.mainMc.ckBoxPlayerGuild.selected = data['ckBoxAvatarGuild']
            self.mainMc.ckBoxPlayerTitle.selected = data['ckBoxAvatarTitle']
        elif self.mainMc.showMode.selectedIndex == 2:
            self.mainMc.ckBoxPlayerTitle.enabled = True
            self.mainMc.ckBoxPlayerGuild.enabled = False
            self.mainMc.ckBoxPlayerGuild.selected = False
            self.mainMc.showSelfArmor.enabled = False
            self.mainMc.showSelfArmor.selected = False
            self.mainMc.ckBoxPlayerBlood.selected = data['ckBoxOtherEntityBlood']
            self.mainMc.ckBoxPlayerName.selected = data['ckBoxOtherEntityName']
            self.mainMc.ckBoxPlayerTitle.selected = data['ckBoxOtherEntityTitle']
        elif self.mainMc.showMode.selectedIndex == 0:
            self.mainMc.showSelfArmor.enabled = True
            self.mainMc.ckBoxPlayerGuild.enabled = True
            self.mainMc.ckBoxPlayerTitle.enabled = True
            self.mainMc.ckBoxPlayerBlood.selected = data['ckBoxPlayerBlood']
            self.mainMc.ckBoxPlayerName.selected = data['ckBoxPlayerName']
            self.mainMc.ckBoxPlayerGuild.selected = data['ckBoxPlayerGuild']
            self.mainMc.ckBoxPlayerTitle.selected = data['ckBoxPlayerTitle']
            self.mainMc.showSelfArmor.selected = data['showSelfArmor']
        elif self.mainMc.showMode.selectedIndex == 3:
            self.mainMc.ckBoxPlayerGuild.enabled = False
            self.mainMc.ckBoxPlayerGuild.selected = False
            self.mainMc.showSelfArmor.enabled = False
            self.mainMc.showSelfArmor.selected = False
            self.mainMc.ckBoxPlayerTitle.enabled = False
            self.mainMc.ckBoxPlayerTitle.selected = False
            self.mainMc.ckBoxPlayerBlood.selected = data['ckBoxSpriteBlood']
            self.mainMc.ckBoxPlayerName.selected = data['ckBoxSpriteName']
        elif self.mainMc.showMode.selectedIndex == 4:
            self.mainMc.ckBoxPlayerGuild.enabled = False
            self.mainMc.ckBoxPlayerGuild.selected = False
            self.mainMc.showSelfArmor.enabled = False
            self.mainMc.showSelfArmor.selected = False
            self.mainMc.ckBoxPlayerTitle.enabled = False
            self.mainMc.ckBoxPlayerTitle.selected = False
            self.mainMc.ckBoxPlayerBlood.selected = data['ckBoxOtherSpriteBlood']
            self.mainMc.ckBoxPlayerName.selected = data['ckBoxOtherSpriteName']
        self.oldSelectMode = self.mainMc.showMode.selectedIndex

    def refreshVisible(self):
        visibleData = {}
        visibleData['isCCVersion'] = gameglobal.rds.configData.get('isCCVersion', False)
        visibleData['enableCCBox'] = gameglobal.rds.configData.get('enableCCBox', False)
        visibleData['enableInventoryLock'] = gameglobal.rds.configData.get('enableInventoryLock', False)
        visibleData['enableSemantics'] = gameglobal.rds.configData.get('enableSemantics', False)
        visibleData['enableQingGongPathfinding'] = gameglobal.rds.configData.get('enableQingGongPathFinding', False)
        visibleData['enableAutoQuest'] = gameglobal.rds.configData.get('enableAutoQuest', False)
        visibleData['hasVipBasic'] = uiUtils.hasVipBasic()
        visibleData['vipTips'] = uiUtils.getTextFromGMD(GMDD.data.CAN_USE_AFTER_VIP_ACTIVATE_HINT, '')
        isVisible = visibleData['isCCVersion'] and visibleData['enableCCBox']
        self.mainMc.ckBoxTeamOpenCC.visible = True
        self.mainMc.ckBoxZhanchangOpenCC.visible = False
        self.mainMc.ckBoxCCQuitConfirm.visible = False
        self.mainMc.ckBoxCCMiniShow.visible = False
        self.mainMc.ckBoxDisableSemanticsRecognition.visible = visibleData['enableSemantics']
        self.mainMc.ckBlockSkillAppearance.visible = gameglobal.rds.configData.get('enableSkillAppearance', False) and gameglobal.rds.configData.get('enableSkillAppearanceBlock', False)
        count = 0
        for name in self.checkVisible1:
            if self.mainMc.getChildByName(name).visible:
                self.mainMc.getChildByName(name).x = self.originPosition1[0] + self.xOffset * (count % 3)
                self.mainMc.getChildByName(name).y = self.originPosition1[1] + self.yOffset * int(count / 3)
                count = count + 1

        count = 0
        for name in self.checkVisible2:
            if self.mainMc.getChildByName(name).visible:
                self.mainMc.getChildByName(name).x = self.originPosition2[0] + self.xOffset * (count % 3)
                self.mainMc.getChildByName(name).y = self.originPosition2[1] + self.yOffset * int(count / 3)
                count = count + 1

    def ui2Data(self, newData):
        newData['comBoxSelectMode'] = self.mainMc.showMode.selectedIndex
        if self.mainMc.showMode.selectedIndex == self.PlAYER_SETTING:
            newData['ckBoxPlayerBlood'] = int(self.mainMc.ckBoxPlayerBlood.selected)
            newData['ckBoxPlayerName'] = int(self.mainMc.ckBoxPlayerName.selected)
            newData['ckBoxPlayerGuild'] = int(self.mainMc.ckBoxPlayerGuild.selected)
            newData['ckBoxPlayerTitle'] = int(self.mainMc.ckBoxPlayerTitle.selected)
            newData['showSelfArmor'] = int(self.mainMc.showSelfArmor.selected)
        elif self.mainMc.showMode.selectedIndex == self.AVATAR_SETTING:
            newData['ckBoxAvatarBlood'] = int(self.mainMc.ckBoxPlayerBlood.selected)
            newData['ckBoxAvatarName'] = int(self.mainMc.ckBoxPlayerName.selected)
            newData['ckBoxAvatarGuild'] = int(self.mainMc.ckBoxPlayerGuild.selected)
            newData['ckBoxAvatarTitle'] = int(self.mainMc.ckBoxPlayerTitle.selected)
        elif self.mainMc.showMode.selectedIndex == self.NPC_MONSTER_SETTING:
            newData['ckBoxOtherEntityBlood'] = int(self.mainMc.ckBoxPlayerBlood.selected)
            newData['ckBoxOtherEntityName'] = int(self.mainMc.ckBoxPlayerName.selected)
            newData['ckBoxOtherEntityTitle'] = int(self.mainMc.ckBoxPlayerTitle.selected)
        elif self.mainMc.showMode.selectedIndex == self.SPRITE_SETTING:
            newData['ckBoxSpriteBlood'] = int(self.mainMc.ckBoxPlayerBlood.selected)
            newData['ckBoxSpriteName'] = int(self.mainMc.ckBoxPlayerName.selected)
        elif self.mainMc.showMode.selectedIndex == self.OTHER_SPRITE_SETTING:
            newData['ckBoxOtherSpriteBlood'] = int(self.mainMc.ckBoxPlayerBlood.selected)
            newData['ckBoxOtherSpriteName'] = int(self.mainMc.ckBoxPlayerName.selected)
        newData['ckBoxMap'] = int(self.mainMc.ckBoxMap.selected)
        newData['ckBoxLittlemapHit'] = int(self.mainMc.ckBoxLittlemapHit.selected)
        newData['ckBoxItemBar'] = int(self.mainMc.ckBoxItemBar.selected)
        newData['ckBoxItemBar2'] = int(self.mainMc.ckBoxItemBar2.selected)
        newData['ckBoxPathTrace'] = int(self.mainMc.ckBoxPathTrace.selected)
        newData['ckBoxOutline'] = int(self.mainMc.ckBoxOutline.selected)
        newData['hpShowMode'] = int(self.mainMc.hpShowMode.selected)
        newData['uiSizeSlider'] = self.mainMc.uiSizeSlider.value / 100.0
        newData['headNameSizeSlider'] = self.mainMc.headNameSizeSlider.value
        newData['walkSpeedSlider'] = self.mainMc.walkSpeedSlider.value
        newData['cameraSlider'] = self.mainMc.cameraSlider.value
        newData['ckBoxLookAt'] = int(self.mainMc.ckBoxLookAt.selected)
        newData['ckBoxErrorSound'] = int(self.mainMc.ckBoxErrorSound.selected)
        newData['ckBoxBossKey'] = int(self.mainMc.ckBoxBossKey.selected)
        newData['ckBoxTargetLockedEff'] = int(self.mainMc.ckBoxTargetLockedEff.selected)
        newData['ckBlockFirework'] = int(self.mainMc.ckBlockFirework.selected)
        newData['ckBlockSkillAppearance'] = int(self.mainMc.ckBlockSkillAppearance.selected)
        newData['ckEnableRandWing'] = int(self.mainMc.ckEnableRandWing.selected)
        newData['ckBoxTeamOpenCC'] = int(self.mainMc.ckBoxTeamOpenCC.selected)
        newData['ckBoxZhanchangOpenCC'] = int(self.mainMc.ckBoxZhanchangOpenCC.selected)
        newData['ckBoxCCQuitConfirm'] = int(self.mainMc.ckBoxCCQuitConfirm.selected)
        newData['ckBoxCCMiniShow'] = int(self.mainMc.ckBoxCCMiniShow.selected)
        newData['ckLowLvQuest'] = int(self.mainMc.ckLowLvQuest.selected)
        newData['ckBoxDisableSemanticsRecognition'] = int(self.mainMc.ckBoxDisableSemanticsRecognition.selected)
        newData['ckBoxHpShow'] = int(self.mainMc.ckBoxHpShow.selected)

    def unRegisterPanel(self):
        self.widget = None
        self.mainMc = None
        self.data = {}
        self.newData = {}
        self.oldSelectMode = -1
        self.maxResolution = []
        self.selectMode = self.PlAYER_SETTING

    def getMaxResolution(self):
        if self.maxResolution:
            return self.maxResolution
        return BigWorld.getScreenSize()

    def onUpdateClientCfg(self):
        if self.widget:
            self.refreshVisible()
