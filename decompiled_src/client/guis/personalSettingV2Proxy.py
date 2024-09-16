#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/personalSettingV2Proxy.o
import cPickle
import zlib
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

class PersonalSettingV2Proxy(UIProxy):
    checkVisible = ['skillShareTitle',
     'line2',
     'skillShareAll',
     'skillShareFriend',
     'skillShareForbid',
     'leaveMsgTitle',
     'line3',
     'allowAllZoneMsgBtn',
     'allowFriendZoneMsgBtn',
     'headTitile',
     'line4',
     'allowAllZoneSeeBtn',
     'allowFriendZoneSeeBtn',
     'spaceSkinTitle',
     'line5',
     'spaceSkinSettingText',
     'spaceSkinSettingBtn',
     'settingTitle',
     'line6',
     'inventoryLockSettingText',
     'setBtn',
     'inventoryLockClearText',
     'clearBtn',
     'multiLanguageTxt',
     'multiLanguageSetBtn']
    needToResetPosTiTle = ['skillShareTitle',
     'leaveMsgTitle',
     'headTitile',
     'spaceSkinTitle',
     'settingTitle']
    needToResetPosLine = ['line2',
     'line3',
     'line4',
     'line5',
     'line6']
    needToResetPosRB = ['skillShareAll',
     'skillShareFriend',
     'skillShareForbid',
     'allowAllZoneMsgBtn',
     'allowFriendZoneMsgBtn',
     'allowAllZoneSeeBtn',
     'allowFriendZoneSeeBtn']
    needToResetPosText = ['spaceSkinSettingText',
     'inventoryLockSettingText',
     'inventoryLockClearText',
     'multiLanguageTxt']
    needToResetPosBtn = ['spaceSkinSettingBtn',
     'setBtn',
     'clearBtn',
     'multiLanguageSetBtn']

    def __init__(self, uiAdapter):
        super(PersonalSettingV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.mainMc = None
        self.scrollWindowContent = None
        self.data = {}
        self.newData = {}
        self.defaultSetting = {'ckBoxRejectAddFriend': 0,
         'ckBoxRejectUnknownChat': 0,
         'ckBoxRejectAllChat': 0,
         'refuseCoupleEmoteApply': 0,
         'ckBoxRejectQiecuo': 0,
         'ckBoxFormally': 0,
         'ckBoxApprentice': 0,
         'ckBoxHideMyJieqi': 0,
         'zoneMsgPermission': 0,
         'zoneHeadIconPermission': 0,
         'skillShareAll': 1,
         'skillShareFriend': 0,
         'skillShareForbid': 0,
         'ckBoxBuffListener': 0,
         'ckBoxGroupChat': 0}

    def initPanel(self, widget):
        self.widget = widget
        self.mainMc = self.widget.canvas
        self.scrollWindowContent = self.widget.canvas.scrollWindow.canvas
        self.mainMc.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick)
        self.mainMc.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancleBtnClick)
        self.mainMc.defaultBtn.addEventListener(events.BUTTON_CLICK, self.handleDefaultBtnClick)
        self.mainMc.applyBtn.addEventListener(events.BUTTON_CLICK, self.handleApplyBtnClick)
        self.scrollWindowContent.buffSettingBtn.addEventListener(events.BUTTON_CLICK, self.handleBuffListener)
        self.scrollWindowContent.spaceSkinSettingBtn.addEventListener(events.BUTTON_CLICK, self.handleSetSpaceSkin)
        self.scrollWindowContent.setBtn.addEventListener(events.BUTTON_CLICK, self.handleSetPassWord)
        self.scrollWindowContent.clearBtn.addEventListener(events.BUTTON_CLICK, self.handleClearPassWord)
        self.scrollWindowContent.multiLanguageSetBtn.addEventListener(events.BUTTON_CLICK, self.handleShowMulLanguageSetting)
        self.scrollWindowContent.refuseCoupleEmoteApply.text = gameStrings.PERSONALSETTING_TEXT1
        self.scrollWindowContent.ckBoxRefuseTeamTrideCouple.text = gameStrings.PERSONALSETTING_TEXT2
        TipManager.addTip(self.scrollWindowContent.ckBoxRefuseTeamTrideCouple, '')
        self.scrollWindowContent.ckBoxGroupChat.visible = gameglobal.rds.configData.get('enableChatGroup', False)
        self.data = self.getPersonalConfigData()
        self.newData = copy.deepcopy(self.data)
        self.refreshUI(self.newData)
        self.setDefaultSettingData()
        BigWorld.callback(0.02, self.refreshVisible)

    def handleConfirmBtnClick(self, *args):
        self.handleApplyBtnClick(*args)
        gameglobal.rds.ui.gameSetting.hide(True)
        gameglobal.rds.sound.playSound(gameglobal.SD_2)

    def handleApplyBtnClick(self, *args):
        self.ui2Data(self.newData)
        self.settingApply(self.newData)
        AppSettings[keys.SET_REFUSE_COUPLE_EMOTE_APPLY] = int(self.data['refuseCoupleEmoteApply'])
        AppSettings[keys.SET_SKILL_SHARE_ALL] = int(self.data['skillShareAll'])
        AppSettings[keys.SET_SKILL_SHARE_FRIEND] = int(self.data['skillShareFriend'])
        AppSettings[keys.SET_SKILL_SHARE_FORBID] = int(self.data['skillShareForbid'])
        AppSettings[keys.SET_BUFF_LISTENER] = int(self.data['ckBoxBuffListener'])
        AppSettings.save()
        self.updateCommonSettingOperation()
        BigWorld.player().fashion.resetModelRoll()

    def settingApply(self, data):
        p = BigWorld.player()
        if data['ckBoxHideMyJieqi'] != self.data['ckBoxHideMyJieqi'] or data['zoneMsgPermission'] != self.data['zoneMsgPermission'] or data['zoneHeadIconPermission'] != self.data['zoneHeadIconPermission']:
            self.data['ckBoxHideMyJieqi'] = data['ckBoxHideMyJieqi']
            self.data['zoneMsgPermission'] = data['zoneMsgPermission']
            self.data['zoneHeadIconPermission'] = data['zoneHeadIconPermission']
            p.ckBoxHideMyJieqi = self.data['ckBoxHideMyJieqi']
            p.zoneMsgPermission = self.data['zoneMsgPermission']
            p.zoneHeadIconPermission = self.data['zoneHeadIconPermission']
            zoneConfig = '|'
            zoneConfig = zoneConfig.join([str(int(self.data['ckBoxHideMyJieqi'])), str(int(self.data['zoneMsgPermission'])), str(int(self.data['zoneHeadIconPermission']))])
            keyList = [const.PERSONAL_ZONE_DATA_CONFIG]
            valueList = [zoneConfig]
            gamelog.debug('valueList', valueList)
            p.base.setPersonalZoneInfo(keyList, valueList)
        if data['ckBoxRejectAddFriend'] != self.data['ckBoxRejectAddFriend']:
            p.base.setFriendOption(gametypes.FRIEND_OPTION_REJECT_ADDED_AS_FRIEND, data['ckBoxRejectAddFriend'])
            self.data['ckBoxRejectAddFriend'] = data['ckBoxRejectAddFriend']
        if data['ckBoxEnemyFriend'] != self.data['ckBoxEnemyFriend']:
            p.base.setFriendOption(gametypes.FRIEND_OPTION_REJECT_MSG_FROM_ENEMY_FRIEND, data['ckBoxEnemyFriend'])
            self.data['ckBoxEnemyFriend'] = data['ckBoxEnemyFriend']
        if data['ckBoxRejectUnknownChat'] != self.data['ckBoxRejectUnknownChat']:
            p.base.setFriendOption(gametypes.FRIEND_OPTION_REJECT_MSG_FROM_STRANGER, data['ckBoxRejectUnknownChat'])
            self.data['ckBoxRejectUnknownChat'] = data['ckBoxRejectUnknownChat']
        if data['ckBoxRejectAllChat'] != self.data['ckBoxRejectAllChat']:
            p.base.setFriendOption(gametypes.FRIEND_OPTION_REJECT_MSG_FROM_ALL, data['ckBoxRejectAllChat'])
            self.data['ckBoxRejectAllChat'] = data['ckBoxRejectAllChat']
        if data['refuseCoupleEmoteApply'] != self.data['refuseCoupleEmoteApply']:
            gameglobal.REFUSE_COUPLE_EMOTE_APPLY = data['refuseCoupleEmoteApply']
            self.data['refuseCoupleEmoteApply'] = data['refuseCoupleEmoteApply']
        if data['ckBoxRejectQiecuo'] != self.data['ckBoxRejectQiecuo']:
            p.cell.updateQiecuoRejectOpt(data['ckBoxRejectQiecuo'])
            self.data['ckBoxRejectQiecuo'] = data['ckBoxRejectQiecuo']
        if data['ckBoxFormally'] != self.data['ckBoxFormally'] or data['ckBoxApprentice'] != self.data['ckBoxApprentice']:
            if p.enableNewApprentice():
                p.base.updateApprenticeOptEx(data['ckBoxFormally'], data['ckBoxApprentice'])
            else:
                p.cell.updateApprenticeOpt(data['ckBoxFormally'], data['ckBoxApprentice'])
            self.data['ckBoxFormally'] = data['ckBoxFormally']
            self.data['ckBoxApprentice'] = data['ckBoxApprentice']
        if data['ckBoxGroupChat'] != self.data['ckBoxGroupChat']:
            p.base.setRejectChatGroupInviteOp(data['ckBoxGroupChat'])
            self.data['ckBoxGroupChat'] = data['ckBoxGroupChat']
        if data['ckBoxRefuseTeamTrideCouple'] != self.data['ckBoxRefuseTeamTrideCouple']:
            self.data['ckBoxRefuseTeamTrideCouple'] = data['ckBoxRefuseTeamTrideCouple']
        enable = data['ckBoxRefuseTeamTrideCouple']
        BigWorld.player().cell.setAutoCoupleEmote(enable)
        if int(data['ckBoxFriendRemind']) != self.data['ckBoxFriendRemind']:
            self.data['ckBoxFriendRemind'] = data['ckBoxFriendRemind']
        if int(data['skillShareAll']) != self.data['skillShareAll']:
            self.data['skillShareAll'] = data['skillShareAll']
        if int(data['skillShareFriend']) != self.data['skillShareFriend']:
            self.data['skillShareFriend'] = data['skillShareFriend']
        if int(data['skillShareForbid']) != self.data['skillShareForbid']:
            self.data['skillShareForbid'] = data['skillShareForbid']
        if int(data['ckBoxBuffListener']) != self.data['ckBoxBuffListener']:
            self.data['ckBoxBuffListener'] = data['ckBoxBuffListener']

    def updateCommonSettingOperation(self):
        p = BigWorld.player()
        p.setSavedOperationMode(p.getOperationMode())
        p.operation['commonSetting'][30] = self.data['skillShareAll']
        p.operation['commonSetting'][31] = self.data['skillShareFriend']
        p.operation['commonSetting'][32] = self.data['skillShareForbid']
        p.sendOperation()
        if self.data['ckBoxFriendRemind'] != (not p.friend.getOption(gametypes.FRIEND_OPTION_HOME_ONLINE_NOTIFY)):
            p.base.setFriendOption(gametypes.FRIEND_OPTION_HOME_ONLINE_NOTIFY, not self.data['ckBoxFriendRemind'])
        if gameglobal.rds.configData.get('enableSkillHierogramShare', False):
            if self.data['skillShareAll']:
                p.base.setCareerGuideShareOpt(gametypes.SKILL_HIEROGRAM_ALL_ALLOW)
            if self.data['skillShareFriend']:
                p.base.setCareerGuideShareOpt(gametypes.SKILL_HIEROGRAM_FRIEND_ALLOW)
            if self.data['skillShareForbid']:
                p.base.setCareerGuideShareOpt(gametypes.SKILL_HIEROGRAM_NO_ALLOW)
        buffListenerConfig = copy.deepcopy(p.buffListenerConfig)
        buffListenerConfig['buffListenerEnable'] = self.data['ckBoxBuffListener']
        p.base.setStateMonitorClientConfig(zlib.compress(cPickle.dumps(buffListenerConfig)))

    def handleCancleBtnClick(self, *args):
        gameglobal.rds.ui.gameSetting.hide(True)
        gameglobal.rds.sound.playSound(gameglobal.SD_3)

    def handleDefaultBtnClick(self, *args):
        self.newData = copy.deepcopy(self.defaultSetting)
        self.refreshUI(self.newData)

    def handleSetSpaceSkin(self, *args):
        if gameglobal.rds.configData.get('enablePersonalZoneSkin', False):
            gameglobal.rds.ui.spaceSkinSetting.show()
        else:
            BigWorld.player().showGameMsg(GMDD.data.PERSONALZONE_SKIN_IN_TEAT, ())

    def handleBuffListener(self, *args):
        gameglobal.rds.ui.buffListenerSetting.show()

    def handleSetPassWord(self, *args):
        gameglobal.rds.ui.inventory.onLatchCipherSetting()

    def handleClearPassWord(self, *args):
        gameglobal.rds.ui.inventory.onClearPassword()

    def handleShowMulLanguageSetting(self, *args):
        if not gameglobal.rds.configData.get('enableChatMultiLanguage', False):
            return
        self.uiAdapter.languageSetting.show()

    def getPersonalConfigData(self):
        p = BigWorld.player()
        data = {}
        data['ckBoxRejectAddFriend'] = int(p.friend.getOption(gametypes.FRIEND_OPTION_REJECT_ADDED_AS_FRIEND))
        data['ckBoxRejectUnknownChat'] = int(p.friend.getOption(gametypes.FRIEND_OPTION_REJECT_MSG_FROM_STRANGER))
        data['ckBoxRejectAllChat'] = int(p.friend.getOption(gametypes.FRIEND_OPTION_REJECT_MSG_FROM_ALL))
        data['refuseCoupleEmoteApply'] = AppSettings.get(keys.SET_REFUSE_COUPLE_EMOTE_APPLY, 0)
        data['ckBoxRejectQiecuo'] = p.qiecuoRejectOpt
        if p.enableNewApprentice():
            data['ckBoxApprentice'] = p.apprenticeRejectOptEx
            data['ckBoxFormally'] = p.mentorRejectOptEx
        else:
            data['ckBoxApprentice'] = p.apprenticeRejectOpt
            data['ckBoxFormally'] = p.mentorRejectOpt
        data['ckBoxEnemyFriend'] = int(p.friend.getOption(gametypes.FRIEND_OPTION_REJECT_MSG_FROM_ENEMY_FRIEND))
        data['ckBoxRefuseTeamTrideCouple'] = getattr(BigWorld.player(), 'autoCoupleEmote', 0)
        data['ckBoxHideMyJieqi'] = p.ckBoxHideMyJieqi
        data['ckBoxFriendRemind'] = not p.friend.getOption(gametypes.FRIEND_OPTION_HOME_ONLINE_NOTIFY)
        data['skillShareAll'] = p.operation['commonSetting'][30]
        data['skillShareFriend'] = p.operation['commonSetting'][31]
        data['skillShareForbid'] = p.operation['commonSetting'][32]
        data['ckBoxBuffListener'] = p.buffListenerConfig.get('buffListenerEnable', 0)
        data['zoneMsgPermission'] = p.zoneMsgPermission
        data['zoneHeadIconPermission'] = p.zoneHeadIconPermission
        data['ckBoxGroupChat'] = p.rejectChatGroupInviteOp
        p.fashion.resetModelRoll()
        return data

    def refreshUI(self, data):
        if data.has_key('ckBoxRefuseTeamTrideCouple'):
            self.scrollWindowContent.ckBoxRefuseTeamTrideCouple.selected = data['ckBoxRefuseTeamTrideCouple']
        if data.has_key('ckBoxEnemyFriend'):
            self.scrollWindowContent.ckBoxEnemyFriend.selected = data['ckBoxEnemyFriend']
        if data.has_key('ckBoxFriendRemind'):
            self.scrollWindowContent.ckBoxFriendRemind.selected = data['ckBoxFriendRemind']
        self.scrollWindowContent.ckBoxRejectAddFriend.selected = data['ckBoxRejectAddFriend']
        self.scrollWindowContent.ckBoxRejectUnknownChat.selected = data['ckBoxRejectUnknownChat']
        self.scrollWindowContent.ckBoxRejectAllChat.selected = data['ckBoxRejectAllChat']
        self.scrollWindowContent.refuseCoupleEmoteApply.selected = data['refuseCoupleEmoteApply']
        self.scrollWindowContent.ckBoxRejectQiecuo.selected = data['ckBoxRejectQiecuo']
        self.scrollWindowContent.ckBoxFormally.selected = data['ckBoxFormally']
        self.scrollWindowContent.ckBoxApprentice.selected = data['ckBoxApprentice']
        self.scrollWindowContent.ckBoxHideMyJieqi.selected = data['ckBoxHideMyJieqi']
        self.scrollWindowContent.skillShareAll.selected = data['skillShareAll']
        self.scrollWindowContent.skillShareFriend.selected = data['skillShareFriend']
        self.scrollWindowContent.skillShareForbid.selected = data['skillShareForbid']
        self.scrollWindowContent.ckBoxBuffListener.selected = data['ckBoxBuffListener']
        self.scrollWindowContent.ckBoxGroupChat.selected = data['ckBoxGroupChat']
        if data['zoneMsgPermission']:
            self.scrollWindowContent.allowFriendZoneMsgBtn.selected = 1
        else:
            self.scrollWindowContent.allowAllZoneMsgBtn.selected = 1
        if data['zoneHeadIconPermission']:
            self.scrollWindowContent.allowFriendZoneSeeBtn.selected = 1
        else:
            self.scrollWindowContent.allowAllZoneSeeBtn.selected = 1

    def ui2Data(self, newData):
        newData['ckBoxRejectAddFriend'] = 1 if self.scrollWindowContent.ckBoxRejectAddFriend.selected else 0
        newData['ckBoxRejectUnknownChat'] = 1 if self.scrollWindowContent.ckBoxRejectUnknownChat.selected else 0
        newData['ckBoxRejectAllChat'] = 1 if self.scrollWindowContent.ckBoxRejectAllChat.selected else 0
        newData['refuseCoupleEmoteApply'] = 1 if self.scrollWindowContent.refuseCoupleEmoteApply.selected else 0
        newData['ckBoxRejectQiecuo'] = 1 if self.scrollWindowContent.ckBoxRejectQiecuo.selected else 0
        newData['ckBoxFormally'] = 1 if self.scrollWindowContent.ckBoxFormally.selected else 0
        newData['ckBoxApprentice'] = 1 if self.scrollWindowContent.ckBoxApprentice.selected else 0
        newData['ckBoxRefuseTeamTrideCouple'] = 1 if self.scrollWindowContent.ckBoxRefuseTeamTrideCouple.selected else 0
        newData['ckBoxEnemyFriend'] = 1 if self.scrollWindowContent.ckBoxEnemyFriend.selected else 0
        newData['ckBoxHideMyJieqi'] = 1 if self.scrollWindowContent.ckBoxHideMyJieqi.selected else 0
        newData['zoneMsgPermission'] = 1 if self.scrollWindowContent.allowFriendZoneMsgBtn.selected else 0
        newData['zoneHeadIconPermission'] = 1 if self.scrollWindowContent.allowFriendZoneSeeBtn.selected else 0
        newData['ckBoxFriendRemind'] = 1 if self.scrollWindowContent.ckBoxFriendRemind.selected else 0
        newData['skillShareAll'] = 1 if self.scrollWindowContent.skillShareAll.selected else 0
        newData['skillShareFriend'] = 1 if self.scrollWindowContent.skillShareFriend.selected else 0
        newData['skillShareForbid'] = 1 if self.scrollWindowContent.skillShareForbid.selected else 0
        newData['ckBoxBuffListener'] = 1 if self.scrollWindowContent.ckBoxBuffListener.selected else 0
        newData['ckBoxGroupChat'] = 1 if self.scrollWindowContent.ckBoxGroupChat.selected else 0

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
            self.defaultSetting['skillShareAll'] = defaultSettingData[30]
            self.defaultSetting['skillShareFriend'] = defaultSettingData[31]
            self.defaultSetting['skillShareForbid'] = defaultSettingData[32]
            self.defaultSetting['ckBoxSpriteBlood'] = defaultSettingData[33]
            self.defaultSetting['ckBoxSpriteName'] = defaultSettingData[34]
            self.defaultSetting['ckBoxOtherSpriteBlood'] = defaultSettingData[35]
            self.defaultSetting['ckBoxOtherSpriteName'] = defaultSettingData[36]
            self.defaultSetting['ckBoxBuffListener'] = 0

    def refreshVisible(self):
        isVisible = gameglobal.rds.configData.get('enableSkillHierogramShare', False)
        self.scrollWindowContent.skillShareTitle.visible = isVisible
        self.scrollWindowContent.line2.visible = isVisible
        self.scrollWindowContent.skillShareAll.visible = isVisible
        self.scrollWindowContent.skillShareFriend.visible = isVisible
        self.scrollWindowContent.skillShareForbid.visible = isVisible
        isVisible1 = gameglobal.rds.configData.get('enableInventoryLock', False)
        self.scrollWindowContent.inventoryLockSettingText.visible = isVisible1
        self.scrollWindowContent.setBtn.visible = isVisible1
        self.scrollWindowContent.inventoryLockClearText.visible = isVisible1
        self.scrollWindowContent.clearBtn.visible = isVisible1
        isVisible2 = gameglobal.rds.configData.get('enableChatMultiLanguage', False)
        self.scrollWindowContent.multiLanguageTxt.visible = isVisible2
        self.scrollWindowContent.multiLanguageSetBtn.visible = isVisible2
        isVisible3 = isVisible1 or isVisible2
        self.scrollWindowContent.settingTitle.visible = isVisible3
        self.scrollWindowContent.line6.visible = isVisible3
        lastType = 'none'
        pos = [0, 0]
        for name in self.checkVisible:
            component = getattr(self.scrollWindowContent, name)
            if component.visible:
                if name in self.needToResetPosTiTle:
                    if lastType == 'none':
                        pos = [3, 217]
                    else:
                        pos[0] = 3
                        pos[1] = pos[1] + 35
                    lastType = 'titile'
                elif name in self.needToResetPosLine:
                    pos[0] = 0
                    pos[1] = pos[1] + 5
                    lastType = 'line'
                elif name in self.needToResetPosRB:
                    if lastType != 'radioButton':
                        pos[0] = 2
                        pos[1] = pos[1] + 10
                    else:
                        pos[0] = pos[0] + 239
                    lastType = 'radioButton'
                elif name in self.needToResetPosText:
                    pos[0] = 2
                    if lastType == 'line':
                        pos[1] = pos[1] + 20
                    else:
                        pos[1] = pos[1] + 35
                    lastType = 'text'
                elif name in self.needToResetPosBtn:
                    pos[0] = pos[0] + 549
                    lastType = 'button'
                component.x = pos[0]
                component.y = pos[1]

    def unRegisterPanel(self):
        self.widget = None
