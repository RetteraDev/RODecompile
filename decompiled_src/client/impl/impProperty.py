#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impProperty.o
from gamestrings import gameStrings
import copy
import cPickle
import zlib
import time
import BigWorld
import gameconfigCommon
import gametypes
import gameglobal
import const
import keys
import utils
import commcalc
import gamelog
import clientcom
import formula
import appSetting
from sfx import sfx
from helpers import action as ACT
from helpers import qingGong
from helpers import ufo
from helpers import charRes
from helpers.eventDispatcher import Event
from helpers import avatarMorpher
from helpers import weaponModel
from helpers import attachedModel
from helpers import aspectHelper
from helpers import gameAntiCheatingManager
from guis import events
from guis import hotkey
from guis import hotkeyProxy
from guis import uiConst
from guis import uiUtils
from guis import tipUtils
from callbackHelper import Functor
from sfx import keyboardEffect
import bufferPropertyGetter
from data import effect_lv_data as ELD
from data import sys_config_data as SYSCD
from data import game_setting_data as GSD
from data import equip_data as ED
from data import horsewing_data as HWCD
from data import game_msg_data as GMD
from data import physics_config_data as PCD
from data import ride_together_data as RTD
from data import fame_data as FD
from data import zaiju_data as ZJD
from data import carrousel_data as CD
from data import item_data as ID
from data import title_data as TD
from data import horsewing_speed_data as HWSD
from cdata import game_msg_def_data as GMDD
from cdata import prop_def_data as PDD
from data import sys_config_data as SCD
from data import couple_emote_basic_data as CEBD
from data import world_war_config_data as WWCD
from data import duel_config_data as DCD

class ImpProperty(object):

    def shortcutSendAll(self, schemes, currSchemeNo):
        self.allShortcutData = {}
        for caseNo, caseInfo in schemes.iteritems():
            try:
                case = cPickle.loads(zlib.decompress(caseInfo))
                self.allShortcutData[caseNo] = case
            except:
                case = {}
                self.allShortcutData[caseNo] = case

        data = self.allShortcutData.get(currSchemeNo, {})
        if self.isInBfChaos() and not self.allShortcutData.get(const.SHOURCUT_SCHEME_ID_CHAOS, {}):
            self.allShortcutData[const.SHOURCUT_SCHEME_ID_CHAOS] = copy.deepcopy(self.allShortcutData[const.SHORTCUT_SCHEME_ID_DEFAULT])
        self.shortcutData = data
        self.hadSetShortCutData = True
        gameglobal.rds.ui.actionbar.needRefreshCenter = True
        gameglobal.rds.ui.actionbar.setCurrSchemeNo(currSchemeNo)
        gameglobal.rds.ui.actionbar.refreshActionbar()

    def shortcutSend(self, data):
        try:
            data = cPickle.loads(zlib.decompress(data))
        except:
            data = {}

        self.shortcutData = data
        if not data:
            gameglobal.rds.ui.actionbar.needSaveClientCut = True
        self.hadSetShortCutData = True
        gameglobal.rds.ui.actionbar.needRefreshCenter = True
        gameglobal.rds.ui.actionbar.refreshActionbar()

    def onSwitchShortcutScheme(self, schemeNo):
        self.shortcutData = self.allShortcutData.get(schemeNo, {})
        self.hadSetShortCutData = True
        gameglobal.rds.ui.actionbar.setCurrSchemeNo(schemeNo)
        if self.shortcutData:
            gameglobal.rds.ui.actionbar.needRefreshCenter = True
            gameglobal.rds.ui.actionbar.setCurrSchemeNo(schemeNo)
            gameglobal.rds.ui.actionbar.refreshActionbar()
        else:
            gameglobal.rds.ui.actionbar.actionbarDataIsInit = False
            gameglobal.rds.ui.actionbar._initActionBarData()
        gameglobal.rds.ui.skill.refreshWsPanel()
        gameglobal.rds.ui.airbar.initAirBarData()
        gameglobal.rds.ui.airbar.refreshAirSkillBar()

    def saveShortcut(self, clientShortCut, schemeNo = const.SHORTCUT_SCHEME_ID_DEFAULT):
        schemeNo = gameglobal.rds.ui.actionbar.getCurrSchemeNo()
        schoolNo = self._getSchoolSwitchNo()
        if self.isOnlyWuShuangSkills(clientShortCut) or not getattr(self, 'hadSetShortCutData', False):
            return
        self.shortcutData = clientShortCut
        self.allShortcutData[schemeNo] = clientShortCut
        self.base.saveShortcut(schoolNo, zlib.compress(cPickle.dumps(clientShortCut)), schemeNo)

    def isOnlyWuShuangSkills(self, shortCutData):
        isOnlyWuShuang = True
        for key, value in shortCutData.iteritems():
            if key and type(key) == tuple and len(key) == 2 and key[0] == uiConst.SKILL_ACTION_BAR and uiConst.WUSHUANG_SKILL_START_POS_LEFT <= key[1] < uiConst.WUSHUANG_SKILL_END_POS:
                pass
            else:
                isOnlyWuShuang = False
                break

        return isOnlyWuShuang

    def set_bfChaosModeDetail(self, old):
        p = BigWorld.player()
        if self.id == p.id:
            getMergeBuffDesc = self.getMergeBuffDesc()
            gameglobal.rds.ui.player.changeMergeIcon(getMergeBuffDesc)
        if p.targetLocked and p.targetLocked == self:
            gameglobal.rds.ui.target.updateMergeBuff()

    def saveWSShortcut(self, clientShortCut):
        if not gameglobal.rds.configData.get('enableWSSchemeHotKeys', False):
            return
        wsShortCut = uiUtils.getWSSkillShortCut(clientShortCut)
        self.base.updateWSSchemeHotKeys(self.getCurWSSchemeNo(), zlib.compress(cPickle.dumps(wsShortCut)))

    def hotkeySend(self, data):
        try:
            serverKeys = cPickle.loads(zlib.decompress(data))
        except:
            serverKeys = {}

        self.hotkeyData = serverKeys
        self.doLoadHotKey()

    def applyUndisturb(self, maxHour, needCoin):
        pass

    def initDisturb(self, info):
        pass

    def addDisturb(self, dType, ratio):
        pass

    def removeDisturb(self, dType):
        pass

    def onQueryBufferTipsProperty(self, pId, args):
        gamelog.debug('@hjx query#onQueryBufferTipsProperty:', pId, args)
        func = getattr(bufferPropertyGetter, bufferPropertyGetter.bufferPropertyGetterMap[pId], None)
        if func:
            value = func(self, args)
            tipUtils.onQueryBufferTipsProperty(pId, value)

    def initOperation(self):
        self.operation = {'commonSetting': self.getDefaultCommonSetting(),
         gameglobal.KEYBOARD_MODE: list(GSD.data.get('keyboardMode', [0,
                                    0,
                                    1,
                                    1,
                                    12,
                                    0])),
         gameglobal.MOUSE_MODE: list(GSD.data.get('mouseMode', [0,
                                 0,
                                 1,
                                 1,
                                 12,
                                 0,
                                 1])),
         gameglobal.ACTION_MODE: list(GSD.data.get('actionMode', [0,
                                  0,
                                  1,
                                  1,
                                  12,
                                  1])),
         gameglobal.KEYBOARD_PLUS: gameglobal.KEYBOARD_PLUS_DICT,
         gameglobal.MOUSE_PLUS: gameglobal.MOUSE_PLUS_DICT,
         gameglobal.ACTION_PLUS: gameglobal.ACTION_PLUS_DICT}
        self.changeDefalutToSpecial()

    def changeDefalutToSpecial(self):
        if self.realSchool in (const.SCHOOL_LINGLONG, const.SCHOOL_LIUGUANG):
            self.operation[gameglobal.ACTION_MODE][7] = 1
        self.operation[gameglobal.ACTION_MODE][5] = SYSCD.data.get('defaultCrossHeight', {}).get(self.realSchool, 3)
        operationMode = self.getSavedOperationMode()
        data = self.operation[operationMode]
        strongHit = data[gameglobal.STRONG_HIT_OP_IDX[operationMode]]
        if strongHit:
            strongHitScrollRanges = SYSCD.data.get('strongHitScrollRanges', {})
            maxRange = strongHitScrollRanges.get(BigWorld.player().realSchool, 6)
            gameglobal.rds.cam.setMaxScrollRange(maxRange)
            data[gameglobal.MAX_SCROLL_RANGE_IDX] = maxRange
            if hasattr(self, 'getOperationMode') and self.getOperationMode() == gameglobal.ACTION_MODE:
                height = SYSCD.data.get('strongHitAimHeight', 2)
                data[gameglobal.AIM_CROSS_HEIGHT_IDX] = height
                gameglobal.AIM_CROSS_HEIGHT = height
                currentScrollNum = gameglobal.rds.cam.currentScrollNum
                BigWorld.player().ap.resetAimCrossPos(currentScrollNum)

    def getDefaultCommonSetting(self):
        return list(GSD.data.get('commonSetting', [0,
         1,
         0,
         1,
         1,
         1,
         1,
         1,
         1,
         1,
         1,
         1,
         1,
         1,
         6.0,
         1,
         1,
         1,
         1,
         3.0,
         0,
         0,
         1,
         0,
         1.6,
         0,
         0,
         1,
         0]))

    def checkOperation(self):
        commonSetting = self.getDefaultCommonSetting()
        keyboardModeOperation = list(GSD.data.get('keyboardMode', [0,
         0,
         1,
         2,
         10,
         1,
         10,
         0,
         0,
         1,
         0,
         0,
         1,
         1]))
        mouseModeOperation = list(GSD.data.get('mouseMode', [0,
         0,
         1,
         2,
         15,
         0,
         10,
         1,
         0,
         1,
         1,
         1,
         0,
         1]))
        actionModeOperation = list(GSD.data.get('actionMode', [0,
         0,
         1,
         2,
         10,
         2,
         10,
         0,
         0,
         0,
         1,
         0,
         0,
         1,
         1]))
        commonSettingLength = len(self.operation['commonSetting'])
        keyboardModeLength = len(self.operation[gameglobal.KEYBOARD_MODE])
        mouseModeLength = len(self.operation[gameglobal.MOUSE_MODE])
        actionModeLength = len(self.operation[gameglobal.ACTION_MODE])
        if commonSettingLength < len(commonSetting):
            self.operation['commonSetting'][commonSettingLength:] = commonSetting[commonSettingLength:]
        if keyboardModeLength < len(keyboardModeOperation):
            self.operation[gameglobal.KEYBOARD_MODE][keyboardModeLength:] = keyboardModeOperation[keyboardModeLength:]
        if mouseModeLength < len(mouseModeOperation):
            self.operation[gameglobal.MOUSE_MODE][mouseModeLength:] = mouseModeOperation[mouseModeLength:]
        if actionModeLength < len(actionModeOperation):
            self.operation[gameglobal.ACTION_MODE][actionModeLength:] = actionModeOperation[actionModeLength:]
        self.operation[gameglobal.KEYBOARD_PLUS] = self.getPlusDict(gameglobal.KEYBOARD_PLUS)
        self.operation[gameglobal.MOUSE_PLUS] = self.getPlusDict(gameglobal.MOUSE_PLUS)
        self.operation[gameglobal.ACTION_PLUS] = self.getPlusDict(gameglobal.ACTION_PLUS)

    def getPlusDict(self, key):
        tempDict = {} if not self.operation.get(key, {}) else self.operation.get(key, {})
        plusDict = {}
        if key == gameglobal.KEYBOARD_PLUS:
            plusDict = dict(gameglobal.KEYBOARD_PLUS_DICT)
        elif key == gameglobal.MOUSE_PLUS:
            plusDict = dict(gameglobal.MOUSE_PLUS_DICT)
        elif key == gameglobal.ACTION_PLUS:
            plusDict = dict(gameglobal.ACTION_PLUS_DICT)
        plusDict.update(tempDict)
        return plusDict

    def operationSend(self, data):
        try:
            data = cPickle.loads(zlib.decompress(data))
        except:
            data = ''

        self.operation = data
        if not self.operation:
            self.initOperation()
        else:
            self.checkOperation()
        operationMode = self.getSavedOperationMode()
        appSetting.GameSettingObj.switchAvatarPhysics(operationMode)
        if hasattr(self, 'ap'):
            self.ap.reset()
        self.applyModeOperation(operationMode)
        self.applyCommonOperation()

    def applyCommonOperation(self):
        appSetting.DebugSettingObj.openPathTrace(self.operation['commonSetting'][1])
        self.hidePlayerName(not self.operation['commonSetting'][2])
        self.hidePlayerTitle(not self.operation['commonSetting'][3])
        self.hidePlayerBlood(not self.operation['commonSetting'][4])
        self.hideAvatarName(not self.operation['commonSetting'][5])
        self.hideAvatarTitle(not self.operation['commonSetting'][6])
        self.hideAvatarBlood(not self.operation['commonSetting'][7])
        self.hideMonsterName(not self.operation['commonSetting'][8])
        self.hideNpcName(not self.operation['commonSetting'][8])
        self.hideMonsterTitle(not self.operation['commonSetting'][9])
        self.hideNpcTitle(not self.operation['commonSetting'][9])
        self.hideMonsterBlood(not self.operation['commonSetting'][10])
        self.hideSpriteBlood(not self.operation['commonSetting'][33])
        self.hideSpriteName(not self.operation['commonSetting'][34])
        self.hideOtherSpriteBlood(not self.operation['commonSetting'][35])
        self.hideOtherSpriteName(not self.operation['commonSetting'][36])
        gameglobal.rds.ui.actionbar.setItemMcVisible(0, self.operation['commonSetting'][11])
        gameglobal.rds.ui.map.littleMapState = self.operation['commonSetting'][12]
        gameglobal.rds.ui.littleMap.littleMapStateChanged()
        gameglobal.ENABLE_ERROR_SOUND = self.operation['commonSetting'][13]
        self.setCameraSensitivity(self.operation['commonSetting'][14])
        self.hidePlayerGuild(not self.operation['commonSetting'][15])
        self.hideAvatarGuild(not self.operation['commonSetting'][16])
        bossKeyState = appSetting.Obj.get(keys.SET_BOSS_KEY, 0)
        gameglobal.rds.ui.surfaceSettingV2.setBossKeyRegisterState(bossKeyState)
        hpMode = appSetting.Obj.get(keys.SET_HP_MODE, 0)
        gameglobal.rds.ui.player.setHpMode(hpMode)
        gameglobal.rds.ui.target.setHpMode(hpMode)
        gameglobal.rds.ui.subTarget.setHpMode(hpMode)
        gameglobal.rds.ui.airbar.refreshAirSkillBar()
        gameglobal.rds.ui.skill.refreshAirSkillbar()
        gameglobal.REFUSE_COUPLE_EMOTE_APPLY = appSetting.Obj.get(keys.SET_REFUSE_COUPLE_EMOTE_APPLY, 0)
        gameglobal.OUTLINIE_FOR_LOCK_TARGET = appSetting.Obj.get(keys.SET_OUTLINE, 0)
        gameglobal.LITTLE_MAP_UNHIT_ABLE = appSetting.Obj.get(keys.SET_LITTLE_MAP_UNHIT_ABLE, 0)
        gameglobal.ENABLE_TARGET_LOCKED_EFFECT = appSetting.Obj.get(keys.SET_TARGET_LOCKED_EFF, 1)
        self.operation['commonSetting'][17] = 0
        self.operation['commonSetting'][18] = 1
        gameglobal.rds.ui.actionbar.setItemMcVisible(1, self.operation['commonSetting'][20])
        self.updateWalkSpeed()

    def applyModeOperation(self, operationMode):
        self.lockEnemy = self.operation[operationMode][0]
        appSetting.DebugSettingObj.switchShortcutToPostion(self.operation[operationMode][1])
        gameglobal.rds.ui.castbar.autoReleaseCharge = self.operation[operationMode][2]
        gameglobal.rds.cam.setScrollSpeed(self.operation[operationMode][3])
        gameglobal.rds.cam.setMaxScrollRange(self.operation[operationMode][4])
        gameglobal.AIM_CROSS_HEIGHT = self.operation[operationMode][5]
        gameglobal.SHAKE_CAMERA_STRENGTH = self.operation[operationMode][6]
        plus = gameglobal.rds.ui.controlSettingV2.getModePlus(operationMode)
        hotkey.setCastSelfKey(self.operation[plus].get(gameglobal.PLUS_SELF_KEY))
        self.checkOperation()
        if operationMode == gameglobal.KEYBOARD_MODE:
            gameglobal.AUTOSKILL_FLAG = self.operation[operationMode][7]
            gameglobal.MOVE_STOP_GUIDE = self.operation[operationMode][8]
            gameglobal.STRONG_HIT = self.operation[operationMode][gameglobal.STRONG_HIT_OP_IDX[operationMode]]
            gameglobal.BREAK_GUIDE_SKILL = self.operation[operationMode][gameglobal.BREAK_GUIDE_OP_IDX[operationMode]]
            gameglobal.INTELLIGENT_CAST = self.operation[operationMode][gameglobal.INTELLIGENT_CAST_IDX[operationMode]]
            gameglobal.PLAY_INDICATOR_EFF = self.operation[operationMode][gameglobal.PLAY_INDICATOR_EFF_IDX[operationMode]]
            gameglobal.TAB_NOT_TO_SELECT_SPRITE = self.operation[operationMode][gameglobal.TAB_NOT_TO_SELECT_SPRITE_IDX[operationMode]]
        elif operationMode == gameglobal.MOUSE_MODE:
            gameglobal.INTELLIGENT_CAST = self.operation[operationMode][gameglobal.INTELLIGENT_CAST_IDX[operationMode]]
            gameglobal.PLAY_INDICATOR_EFF = True
            gameglobal.AUTOSKILL_FLAG = self.operation[operationMode][8]
            gameglobal.ENABLE_FREE_ROTATE_CAM = self.operation[operationMode][9]
            gameglobal.MOVE_STOP_GUIDE = self.operation[operationMode][10]
            gameglobal.STRONG_HIT = self.operation[operationMode][gameglobal.STRONG_HIT_OP_IDX[operationMode]]
            gameglobal.BREAK_GUIDE_SKILL = self.operation[operationMode][gameglobal.BREAK_GUIDE_OP_IDX[operationMode]]
            gameglobal.TAB_NOT_TO_SELECT_SPRITE = self.operation[operationMode][gameglobal.TAB_NOT_TO_SELECT_SPRITE_IDX[operationMode]]
            gameglobal.rds.cam.resetDcursorPitch()
        elif operationMode == gameglobal.ACTION_MODE:
            gameglobal.CAN_LOCK_TARGET_NPC = self.operation[operationMode][7]
            gameglobal.OPTIONAL_TARGET = self.operation[operationMode][7]
            gameglobal.MOVE_STOP_GUIDE = self.operation[operationMode][8]
            gameglobal.NEED_CHOOSE_EFFECT = self.operation[operationMode][9]
            gameglobal.STRONG_HIT = self.operation[operationMode][gameglobal.STRONG_HIT_OP_IDX[operationMode]]
            gameglobal.BREAK_GUIDE_SKILL = self.operation[operationMode][gameglobal.BREAK_GUIDE_OP_IDX[operationMode]]
            gameglobal.INTELLIGENT_CAST = self.operation[operationMode][gameglobal.INTELLIGENT_CAST_IDX[operationMode]]
            gameglobal.PLAY_INDICATOR_EFF = self.operation[operationMode][gameglobal.PLAY_INDICATOR_EFF_IDX[operationMode]]
            gameglobal.TAB_NOT_TO_SELECT_SPRITE = self.operation[operationMode][gameglobal.TAB_NOT_TO_SELECT_SPRITE_IDX[operationMode]]
            gameglobal.rds.cam.currentScrollNum, _ = gameglobal.rds.cam.checkBlock(0)
            currentScrollNum = gameglobal.rds.cam.currentScrollNum
            BigWorld.player().ap.resetAimCrossPos(currentScrollNum)
            key = self.operation[gameglobal.ACTION_PLUS].get(gameglobal.PLUS_SHOW_CURSOR_KEY, 1)
            hotkey.setShowCursorKey(key)
            gameglobal.rds.ui.systemButton.setActionModeIndicator(True, key)
            BigWorld.player().ap.reload()
            hotkeyProxy.getInstance().shortKey.setCastSelfConflict()
            gameglobal.rds.ui.changeAimCross(self.operation[gameglobal.ACTION_PLUS].get(gameglobal.PLUS_AIMCROSS_KEY, 9))

    def updateWalkSpeed(self, speed = None):
        if not speed:
            if not hasattr(self, 'operation'):
                return
            speed = self.operation['commonSetting'][19]
        self.ap.setWalkSpeed(speed)

    def sendOperation(self):
        operation = zlib.compress(cPickle.dumps(self.operation, -1))
        self.base.saveOperation(operation)

    def fishHistorySend(self, data):
        try:
            self.fishHistory = cPickle.loads(zlib.decompress(data))
        except:
            self.fishHistory = []

    def transportHistorySend(self, data):
        try:
            self.transportHistory = cPickle.loads(zlib.decompress(data))
        except:
            self.transportHistory = []

    def availableMorpherSend(self, data):
        try:
            data = cPickle.loads(zlib.decompress(data))
        except:
            data = {}

        self.availableMorpher = data

    def sendMingpaiInfo(self, data):
        self.mingpaiInfo = data
        gameglobal.rds.ui.roleInfo.refreshMingPai()

    def setSelectedMingpai(self, selectedId):
        self.selectedMPId = selectedId
        gameglobal.rds.ui.roleInfo.refreshMingPai()

    def set_itemClientEffectCache(self, old):
        removeSet = set(old.keys()) - set(self.itemClientEffectCache.keys())
        changedIds = []
        for itemId, _ in self.itemClientEffectCache.iteritems():
            if itemId in removeSet:
                continue
            oldNumKey = self.getItemClientEffectNumKey(old, itemId)
            numKey = self.getItemClientEffectNumKey(self.itemClientEffectCache, itemId)
            if oldNumKey != numKey:
                changedIds.append(itemId)

        self.refreshItemClientEffect(removeSet, changedIds)

    def releaseItemClientEffect(self, itemIds):
        if itemIds:
            for itemId in itemIds:
                effs = self.itemClientEffects.get(itemId, [])
                if effs:
                    for ef in effs:
                        if ef:
                            ef.stop()

                self.itemClientEffects.pop(itemId, [])

    def getItemClientEffectNumKey(self, cache, itemId):
        num = cache.get(itemId, 0)
        effKey = 0
        clientEffs = ID.data.get(itemId, {}).get('itemClientEffs', {})
        if clientEffs:
            keys = [ i for i in clientEffs.keys() if i <= num ]
            if keys:
                effKey = max(keys)
        return effKey

    def addItemClientEffect(self, itemIds):
        if itemIds:
            self.releaseItemClientEffect(itemIds)
            for itemId in itemIds:
                clientEffs = ID.data.get(itemId, {}).get('itemClientEffs', {})
                effKey = self.getItemClientEffectNumKey(self.itemClientEffectCache, itemId)
                if clientEffs:
                    eff = clientEffs.get(effKey, 0)
                    if eff:
                        ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
                         self.getSkillEffectPriority(),
                         self.modelServer.bodyModel,
                         eff,
                         sfx.EFFECT_UNLIMIT,
                         gameglobal.EFFECT_LAST_TIME_CONFIG))
                        if ef:
                            self.itemClientEffects[itemId] = ef

    def refreshItemClientEffect(self, removeSet, changedIds):
        self.releaseItemClientEffect(removeSet)
        self.addItemClientEffect(changedIds)

    def set_crossServerFlag(self, old):
        self.refreshOpacityState()
        pet = self._getPet()
        if pet:
            pet.refreshOpacityState()
        if BigWorld.player() == self and self._isSoul():
            gameglobal.rds.ui.pushMessage.hide()
            BigWorld.player().crossServerCipher()
        if BigWorld.player() == self and self._isReturn():
            gameglobal.rds.ui.pushMessage.setCrossMsg()

    def set_jingJie(self, old):
        if BigWorld.player().targetLocked == self:
            gameglobal.rds.ui.target.setJingjie(self.jingJie)

    def set_friendInviteRewards(self, old):
        self.updateRewardHallInfo(uiConst.REWARD_ZHIYOU)

    def refreshBufActStateQingGongCaps(self):
        if self.qinggongState in (gametypes.QINGGONG_STATE_FAST_RUN, gametypes.QINGGONG_STATE_AUTO_JUMP, gametypes.QINGGONG_STATE_SLIDING):
            self.clientStateEffect.setBufActStateQingGongCaps()
        if self.qinggongState == gametypes.QINGGONG_STATE_DEFAULT:
            self.clientStateEffect.restoreBufActState()

    def set_qinggongState(self, old):
        apEffectEx = getattr(self, 'apEffectEx', None)
        if apEffectEx:
            apEffectEx.set_qinggongState(old)
        if self.qinggongState == gametypes.QINGGONG_STATE_DEFAULT:
            self.isUseQingGong = False
            if self == BigWorld.player():
                gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_NO_SKILL)
        else:
            self.isUseQingGong = True
            if self == BigWorld.player():
                gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_NO_SKILL)
        gameAntiCheatingManager.getInstance().recordQinggongData(self.isUseQingGong)
        if self.life == gametypes.LIFE_DEAD:
            return
        elif not self.fashion:
            return
        else:
            self.qinggongMgr.startState(old)
            self.refreshBufActStateQingGongCaps()
            if self.qinggongState == gametypes.QINGGONG_STATE_FAST_RUN:
                self.cancelWeaponTimerAndHangUpWeapon()
                self.dashingStartTime = time.time()
            if self.qinggongState == gametypes.QINGGONG_STATE_MOUNT_DASH:
                self.updateSprintStart()
            self.refreshHorseWingEffect()
            self.fashion.resetTurnBodyState()
            return

    def set_pubAspect(self, old):
        self.pubAspect.calSlotCountSelf()
        self.set_aspect(old)

    def set_miniAspect(self, old):
        self.set_aspect(old)

    def set_switchedAspect(self, old):
        self.switchedAspect.calSlotCountSelf()

    def isFashionChanged(self):
        for itemId in charRes.PARTS_ASPECT_FASHION:
            if getattr(self.realAspect, itemId, 0) != getattr(self.aspectOld, itemId, 0):
                return True

        return False

    def set_aspect(self, old):
        gamelog.debug('b.e.:set_aspect')
        if self == BigWorld.player():
            aspectHelper.getInstance().refreshHackAspect(self.aspect)
            self.needCharSnapshot = True
            self.realAspect.calSlotCountSelf()
        if self.inWenQuanState:
            if self._isWearChanged():
                self.modelServer.wearUpdate()
            elif self.isFashionChanged():
                self.modelServer.bodyPartsUpdate(False, False, False)
            self.aspectOld = copy.deepcopy(self.realAspect)
            return
        else:
            if self._isWeaponChanged():
                self.modelServer.weaponUpdate()
            if self._isWearChanged():
                self.modelServer.wearUpdate()
            if self.aspect.wingFlyAttr() != self.aspectOld.wingFlyAttr():
                modelChange = self.aspect.wingFly != self.aspectOld.wingFly or self.aspect.wingFlyDyeList() != self.aspectOld.wingFlyDyeList()
                self.modelServer.wingFlyModelUpdate(modelChange)
            parts = self.isShowFashion() and charRes.PARTS_ASPECT_FASHION or charRes.PARTS_ASPECT_EQUIP
            if self.isShowClanWar():
                parts = charRes.PARTS_ASPECT_CLANWAR
            modelChange = False
            for part in parts:
                oldPart = getattr(self.aspectOld, part + 'Attr')()
                newPart = getattr(self.realAspect, part + 'Attr')()
                if oldPart != newPart:
                    modelChange = True
                    if not self.firstFetchFinished:
                        self.modelServer.bodyUpdate()
                    else:
                        self.modelServer.bodyPartsUpdate(False)
                    break

            if not modelChange:
                if self.realAspect.rongGuangs != self.aspectOld.rongGuangs:
                    self.setRongGuang()
            self.aspectOld = copy.deepcopy(self.realAspect)
            self.refreshEquipEnhanceEffects()
            if self.fashion and getattr(self.fashion, 'footTriggerMgr', None):
                self.fashion.footTriggerMgr.refreshEquipDust(self)
            return

    def getWeapon(self, isLeft):
        weaponId = 0
        if self.isShowFashionWeapon():
            if isLeft:
                weaponId = self.realAspect.leftFashionWeapon if self.realAspect.leftFashionWeapon else self.realAspect.leftWeapon
            else:
                weaponId = self.realAspect.rightFashionWeapon if self.realAspect.rightFashionWeapon else self.realAspect.rightWeapon
        else:
            weaponId = self.realAspect.leftWeapon if isLeft else self.realAspect.rightWeapon
        if self.isShowClanWar():
            weapons = SCD.data.get('armorWeaponId', gameglobal.ARMOR_WEAPON_ID[self.school])
            weaponId = weapons[int(isLeft)] if weaponId else 0
        if isLeft:
            rightWeaponId = self.getWeapon(False)
            weaponId = ED.data.get(rightWeaponId, {}).get('convertLeftHandId', 0) or weaponId
        return weaponId

    def getWeaponEnhLv(self, isLeft):
        if self.isShowFashionWeapon():
            if isLeft:
                if self.realAspect.leftFashionWeapon:
                    return self.realAspect.leftFashionWeaponEnhLv()
                return self.realAspect.leftWeaponEnhLv()
            elif self.realAspect.rightFashionWeapon:
                return self.realAspect.rightFashionWeaponEnhLv()
            else:
                return self.realAspect.rightWeaponEnhLv()
        if isLeft:
            return self.realAspect.leftWeaponEnhLv()
        return self.realAspect.rightWeaponEnhLv()

    def setRongGuang(self, needXuanren = False):
        if not self.isRealModel:
            return
        if not hasattr(self, 'rongGuangDutyList'):
            self.rongGuangDutyList = charRes.RongGuangResDutyList()
        self.rongGuangDutyList.addDuty(self, needXuanren)
        if self == BigWorld.player():
            gameglobal.rds.ui.roleInfo.takePhoto3D(0)

    def _isWearChanged(self):
        if self.realAspect.headdress != self.aspectOld.headdress or self.realAspect.headdressRight != self.aspectOld.headdressRight or self.realAspect.headdressLeft != self.aspectOld.headdressLeft or self.realAspect.facewear != self.aspectOld.facewear or self.realAspect.waistwear != self.aspectOld.waistwear or self.realAspect.backwear != self.aspectOld.backwear or self.realAspect.tailwear != self.aspectOld.tailwear or self.realAspect.chestwear != self.aspectOld.chestwear or self.realAspect.earwear != self.aspectOld.earwear:
            return True
        return False

    def _isWeaponChanged(self):
        if not self.isShowFashionWeapon():
            return self.realAspect.leftWeaponAttr() != self.aspectOld.leftWeaponAttr() or self.realAspect.rightWeaponAttr() != self.aspectOld.rightWeaponAttr() or self.realAspect.yuanLingAttr() != self.aspectOld.yuanLingAttr()
        else:
            return self.realAspect.leftFashionWeaponAttr() != self.aspectOld.leftFashionWeaponAttr() or self.realAspect.rightFashionWeaponAttr() != self.aspectOld.rightFashionWeaponAttr() or self.realAspect.leftWeaponAttr() != self.aspectOld.leftWeaponAttr() or self.realAspect.rightWeaponAttr() != self.aspectOld.rightWeaponAttr() or self.realAspect.yuanLingAttr() != self.aspectOld.yuanLingAttr() or self.realAspect.rightWeaponEnhLv() != self.aspectOld.rightWeaponEnhLv() or self.realAspect.leftWeaponEnhLv() != self.aspectOld.leftWeaponEnhLv()

    def set_physique(self, old):
        gamelog.debug('b.e.:set_physique')
        bUpdated = False
        for part in charRes.PARTS_PHYSIQUE:
            oldPart = getattr(self.physiqueOld, part)
            newPart = getattr(self.physique, part)
            if oldPart != newPart:
                if not self.firstFetchFinished:
                    self.modelServer.bodyUpdate()
                else:
                    self.modelServer.bodyPartsUpdate(False)
                bUpdated = True
                break

        self.physiqueOld = copy.deepcopy(self.physique)
        if bUpdated and self == BigWorld.player():
            self.needCharSnapshot = True

    def set_speed(self, old):
        gamelog.debug('zf:Avatar set_speed :', self.speed, old)

    def set_pkPunishTime(self, old):
        self.refreshOpacityState()
        self.topLogo.updatePkTopLogo()

    def set_lv(self, old):
        if getattr(self, 'isStraightLvUp', False):
            return
        if BigWorld.player().targetLocked == self:
            gameglobal.rds.ui.target.setLevel(self.lv)
        if BigWorld.player().optionalTargetLocked == self:
            gameglobal.rds.ui.subTarget.setLevel(self.lv)
        sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
         self.getBasicEffectPriority(),
         self.model,
         SYSCD.data.get('sfxLvUp', 11010),
         sfx.EFFECT_LIMIT_MISC,
         gameglobal.EFFECT_LAST_TIME))
        p = BigWorld.player()
        if hasattr(self, 'spaceNo') and self.inFubenTypes(const.FB_TYPE_ARENA):
            gameglobal.rds.ui.teamComm.setTeamLv(self.id, self.lv)
            gameglobal.rds.ui.teamEnemyArena.setTeamLv(self.id, self.lv)
        elif hasattr(self, 'groupNUID') and self.isInTeam() and self.groupNUID == getattr(p, 'groupNUID', 0):
            gameglobal.rds.ui.teamComm.setTeamLv(self.id, self.lv)
        if p != self and p.targetLocked == self:
            ufoType = ufo.UFO_NORMAL
            target = p.targetLocked
            if p.isEnemy(target):
                ufoType = self.getTargetUfoType(target)
            self.setTargetUfo(self, ufoType)

    def set_bianshen(self, old):
        p = BigWorld.player()
        gamelog.debug('set_bianshen', self.bianshen, old)
        self.fashion.setIdleType(gametypes.IDLE_TYPE_NORMAL)
        enableNewSchoolSummon = gameglobal.rds.configData.get('enableNewSchoolSummon', False)
        if enableNewSchoolSummon and self.bianshen[0] != gametypes.BIANSHEN_ZAIJU:
            self.cancelAvatarFollowModel()
        if self.bianshen[0] != old[0]:
            self.topLogo.updateRoleName(self.topLogo.name)
        if self.bianshen[0] == gametypes.BIANSHEN_HUMAN:
            self.inForceNavigate = False
            self.modelServer.leaveRideHB(old)
            self.fashion.autoSetStateCaps()
            if old[0] == gametypes.BIANSHEN_ZAIJU and old[1] == WWCD.data.get('robZaijuNo', 6019):
                self.stateForceSyncTime = utils.getNow() + 5
        elif self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            if old[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
                self.modelServer.leaveRideHB()
            beastKey = self.bianshen[1]
            dyeList = self.realAspect.rideDyeList()
            flyRide = ED.data.get(self.bianshen[1], {}).get('flyRide', False)
            canRideTogether = RTD.data.get(self.bianshen[1], {}).get('canRideTogether', False)
            if self.isShowClanWar() and not flyRide and not canRideTogether:
                beastKey = SYSCD.data.get('armorHorseId', gameglobal.ARMOR_HORSE_ID)
                dyeList = []
            self.modelServer.enterRideHB(beastKey, True, self.realAspect.rideEnhLv(), dyeList)
        elif self.bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
            if old[0] == gametypes.BIANSHEN_RIDING_RB:
                self.modelServer.leaveRideHB()
            beastKey = self.bianshen[1]
            self.modelServer.enterZaiju(beastKey, True, self.realAspect.rideEnhLv())
            self.fashion.autoSetStateCaps()
            if old[0] == gametypes.BIANSHEN_HUMAN and self.bianshen[0] is gametypes.BIANSHEN_ZAIJU and self.bianshen[1] == WWCD.data.get('robZaijuNo', 6019):
                self.stateForceSyncTime = utils.getNow() + 5
        self.resetFootIK()
        if self.fashion.footTriggerMgr:
            self.fashion.footTriggerMgr.refreshFootIdleEffect()
        self.fashion.resetModelRoll()
        self.refreshTRideSpecialAction()
        self.refreshYabiaoEffect()
        self.resetPhysicsModel()
        self.apEffectEx.resetEffect()
        self.refreshOpacityState()
        if p.targetLocked:
            p.refreshTargetLocked()
            if hasattr(p.targetLocked, 'gbId') and p.targetLocked.gbId == self.gbId and p.targetLocked.gbId != p.gbId:
                if p.isBianShenZaiJuInPUBG(p.targetLocked):
                    p.unlockTarget()
        BigWorld.callback(1, self.refreshWingHorseIdleEffect)

    def enterAvatarFollowModel(self):
        if self.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            avatarFollow = ZJD.data.get(self.bianshen[1], {}).get('avatarFollow', None)
            if avatarFollow:
                self.modelServer.avatarFollowModel.follow()

    def cancelAvatarFollowModel(self):
        if self.bianshen[0] != gametypes.BIANSHEN_ZAIJU:
            self.modelServer.avatarFollowModel.cancelFollow()

    def refreshTRideSpecialAction(self):
        if self == BigWorld.player():
            trideSpecialAction = self.getTRideSpecialAction()
            if trideSpecialAction:
                gameglobal.rds.ui.pressKeyF.trideSpecialAction = True
                gameglobal.rds.ui.pressKeyF.setType(const.F_TRIDE_ACTION)
            elif gameglobal.rds.ui.pressKeyF.trideSpecialAction:
                gameglobal.rds.ui.pressKeyF.trideSpecialAction = False
                gameglobal.rds.ui.pressKeyF.removeType(const.F_TRIDE_ACTION)

    def set_carrousel(self, old):
        self.refreshOpacityState()
        if self.inCarrousel():
            self.modelServer.enterCarrousel()
        else:
            self.modelServer.leaveCarrousel(old)
        if self == BigWorld.player():
            if self.carrousel[0]:
                self.showZaijuUI(showType=uiConst.ZAIJU_SHOW_TYPE_CARROUSEL)
            else:
                self.hideZaijuUI(showType=uiConst.ZAIJU_SHOW_TYPE_CARROUSEL)

    def set_schoolSwitchNo(self, old):
        self.switchAvatarConfig = self._getSchoolSwitchAvatarConfig()
        clientcom.fetchTintEffectsContents(self.id, self.afterSetTintEffects)
        self.modelServer.weaponUpdate()
        if self.topLogo:
            if self._isSchoolSwitch() and self.schoolSwitchName != self.realRoleName:
                self.topLogo.updateRoleName(self.schoolSwitchName)
                self.topLogo.removeGuildIcon()
            else:
                self.topLogo.updateRoleName(self.topLogo.name)
                if self == BigWorld.player():
                    if self.guildNUID:
                        if gameglobal.gHidePlayerGuild:
                            self.topLogo.removeGuildIcon()
                        else:
                            self.topLogo.addGuildIcon(self.guildFlag)
                elif self.guildNUID:
                    if gameglobal.gHideAvatarGuild:
                        self.topLogo.removeGuildIcon()
                    else:
                        self.topLogo.addGuildIcon(self.guildFlag)

    def set_signal(self, old):
        self._clientSignal(old)

    def _clientSignal(self, old):
        gamelog.debug('b.e.: _clientSignal', self.signal, old)
        if commcalc.getSingleBit(old, gametypes.SIGNAL_SHOW_HAT) != commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_HAT):
            pass
        if commcalc.getSingleBit(old, gametypes.SIGNAL_SHOW_FASHION) != commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_FASHION):
            if self.inWenQuanState:
                return
            self.modelServer.bodyPartsUpdate(True)
        if commcalc.getSingleBit(old, gametypes.SIGNAL_SHOW_FASHION_WEAPON) != commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_FASHION_WEAPON):
            if self.realAspect.leftFashionWeapon or self.realAspect.rightFashionWeapon:
                self.modelServer.weaponUpdate()
        if commcalc.getSingleBit(old, gametypes.SIGNAL_HAND_CLIMB) != commcalc.getSingleBit(self.signal, gametypes.SIGNAL_HAND_CLIMB):
            signal_new = commcalc.getSingleBit(self.forwardBit, gametypes.SIGNAL_HAND_CLIMB)
            self.handClimb = signal_new
            if self == BigWorld.player():
                if self.handClimb:
                    self.stateMachine.checkStatus_cancel(const.CT_HAND_CLIMB)
                    climbStartAct = '1930'
                    if climbStartAct in self.fashion.getActionNameList():
                        self.model.action(climbStartAct)(0, Functor(self.ap.beginHandClimbNotifier, 140, self.position, self.yaw, 0), 1)
                    else:
                        self.ap.beginHandClimbNotifier(140, self.position, self.yaw, 0)
                else:
                    self.ap.endHandClimbNotifier('Jump')
            elif self.handClimb:
                self.fashion.setupClimbMatcher(self, self.model, False)
                for i in self.model.queue:
                    self.model.action(i).stop()

            else:
                for a in self.model.motors:
                    if a.__name__ == 'ClimbMatcher':
                        self.model.delMotor(a)

                self.am.enable = 1
        if commcalc.getSingleBit(old, gametypes.SIGNAL_SHOW_BACK) != commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_BACK):
            self.showBackWaist = commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_BACK)
            self.modelServer.showBackAndWaist(self.showBackWaist)
        if commcalc.getSingleBit(old, gametypes.SIGNAL_SHOW_YUANLING) != commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_YUANLING):
            self.modelServer.refreshYuanLing(self.isShowYuanLing())
        if commcalc.getSingleBit(old, gametypes.SIGNAL_HIDE_FASHION_HEAD) != commcalc.getSingleBit(self.signal, gametypes.SIGNAL_HIDE_FASHION_HEAD):
            self.modelServer.bodyPartsUpdate(False, False, False, False, True)

    def isShowYuanLing(self):
        return not self.isShowClanWar()

    def isShowFashion(self):
        return not not commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_FASHION)

    def isShowFashionWeapon(self):
        return not not commcalc.getSingleBit(self.signal, gametypes.SIGNAL_SHOW_FASHION_WEAPON)

    def isHideFashionHead(self):
        return not not commcalc.getSingleBit(self.signal, gametypes.SIGNAL_HIDE_FASHION_HEAD)

    def isShowClanWar(self):
        if self._isSchoolSwitch():
            return False
        operation = getattr(BigWorld.player(), 'operation', None)
        if operation and operation.get('commonSetting', None):
            showClanWarArmor = operation['commonSetting'][17]
            notShowSelfClanWarArmor = operation['commonSetting'][18]
        else:
            showClanWarArmor = False
            notShowSelfClanWarArmor = True
        inClanWar = False
        if gameglobal.rds.GameState >= gametypes.GS_LOADING:
            if self == BigWorld.player():
                inClanWar = not notShowSelfClanWarArmor and showClanWarArmor
            else:
                inClanWar = showClanWarArmor
                if not self.realAvatarConfig:
                    inClanWar = True
        if inClanWar:
            return gameglobal.CLAN_WAR_FASHION_TYPE
        else:
            return inClanWar

    def set_pubAvatarConfig(self, old):
        if getattr(self, 'modelServer', None):
            self.modelServer.bodyPartsUpdate(False, True)
            self.modelServer.horseUpdate()
            self.modelServer.wingFlyModelUpdate()
            if self.isShowClanWar():
                self.modelServer.showOtherwears(False)
            else:
                self.modelServer.showOtherwears(True)
        if self.pubAvatarConfig:
            m = avatarMorpher.AvatarModelMorpher(self.id, True)
            m.readConfig(self.realAvatarConfig)
            m.applyBoneMorph()
            m.applyFaceMorph()

    def isShowClanWarExcludeSelf(self):
        if self._isSchoolSwitch():
            return False
        else:
            operation = getattr(BigWorld.player(), 'operation', None)
            if operation:
                showClanWarArmor = operation['commonSetting'][17]
            else:
                showClanWarArmor = False
            inClanWar = False
            if gameglobal.rds.GameState >= gametypes.GS_LOADING:
                inClanWar = showClanWarArmor
            return inClanWar

    def set_weaponState(self, oldValue):
        gamelog.debug('set_weaponState:', oldValue, self.weaponState)
        if self.isDoingAction:
            return
        if not self.fashion:
            return
        self.modelServer.refreshWeaponStateWithAct(False)
        self.resetFootIK()

    def canFly(self):
        if self.inWorld:
            data = ZJD.data.get(self.bianshen[1], {})
            flyZaiju = data.get('flyZaiju', 0)
            return self.inFly or flyZaiju
        return False

    def inFlyTypeWing(self):
        return self.inFly == gametypes.IN_FLY_TYPE_WING

    def inFlyTypeFlyRide(self):
        return self.inFly == gametypes.IN_FLY_TYPE_FLY_RIDE

    def inFlyTypeFlyZaiju(self):
        return self.inFly == gametypes.IN_FLY_TYPE_ZAIJU

    def inFlyTypeObserver(self):
        return self.inFly == gametypes.IN_FLY_OBSERVER

    def isWeaponNeedHideByHorseWing(self, equipmentId, left):
        if equipmentId:
            equipData = ED.data.get(equipmentId, {})
            horseWingData = HWCD.data.get(equipData.get('subId', [0])[0], None)
            if horseWingData:
                hideWeapon = horseWingData[0].get('hideWeapon', 0)
                if hideWeapon == gameglobal.HIDE_RIGHT_HAND_WEAPON and not left:
                    return True
                if hideWeapon == gameglobal.HIDE_LEFT_HAND_WEAPON and left:
                    return True
                if hideWeapon == gameglobal.HIDE_ALL_WEAPON:
                    return True
        return False

    def isWeaponNeedHide(self, left = True):
        if getattr(self, 'inWenQuanState', False):
            return True
        else:
            if getattr(self, 'inFly', 0) == gametypes.IN_FLY_TYPE_WING and self.weaponState == gametypes.WEAPON_HANDFREE:
                equipmentId = self.modelServer.wingFlyModel.key
                if self.isWeaponNeedHideByHorseWing(equipmentId, left):
                    return True
            if getattr(self, 'inFly', 0) == gametypes.IN_FLY_TYPE_FLY_RIDE:
                equipmentId = self.modelServer.rideAttached.key
                if self.isWeaponNeedHideByHorseWing(equipmentId, left):
                    return True
            if self.inRiding() or self.inModelReplace():
                if self.modelServer.rideAttached.isZaijuReplace():
                    return True
                equipmentId = self.modelServer.rideAttached.key
                if self.isWeaponNeedHideByHorseWing(equipmentId, left):
                    return True
            if self.bianshen and self.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
                data = ZJD.data.get(self.bianshen[1], {})
                subId = data.get('subId', 0)
                hideWeapon = HWCD.data.get(subId, [{}])[0].get('hideWeapon', gameglobal.NO_HIDE_WEAPON)
                if hideWeapon == gameglobal.HIDE_ALL_WEAPON:
                    return True
                if hideWeapon == gameglobal.HIDE_RIGHT_HAND_WEAPON and not left:
                    return True
                if hideWeapon == gameglobal.HIDE_LEFT_HAND_WEAPON and left:
                    return True
                bsType = data.get('BsType', 1)
                if left and bsType == attachedModel.ZAIJU_REPLACE and self.realSchool == const.SCHOOL_LINGLONG:
                    return True
            if self.isSkillAttachOther():
                return True
            if self.isInCoupleRide():
                return True
            if self.isRidingTogetherAsVice():
                header = self.tride.getHeader()
                if header:
                    equipmentId = header.modelServer.rideAttached.key
                    if self.isWeaponNeedHideByHorseWing(equipmentId, left):
                        return True
            if self.inCarrousel():
                carrousel = BigWorld.entities.get(self.carrousel[0], None)
                if carrousel:
                    data = CD.data.get(carrousel.carrouselId, {})
                    if data.get('hideWeapon', False):
                        return True
            if getattr(self, 'buffAttachModel', False):
                if left:
                    leftWeaponModel = self.modelServer.leftWeaponModel
                    if leftWeaponModel and leftWeaponModel.state == weaponModel.HANG_UP:
                        return True
                else:
                    rightWeaponModel = self.modelServer.rightWeaponModel
                    if rightWeaponModel and rightWeaponModel.state == weaponModel.HANG_UP:
                        return True
            return False

    def isNeedSchoolBoredAction(self):
        if self.isWeaponNeedHide(False):
            return False
        if not self.realAspect.rightWeapon:
            return False
        if self.modelServer.rightWeaponModel and self.modelServer.rightWeaponModel.models:
            modelItem = self.modelServer.rightWeaponModel.models
            if modelItem and len(modelItem[0]) > 1:
                if not modelItem[0][1]:
                    return False
        return True

    def refreshWeaponVisible(self):
        if self.isWeaponNeedHide(True):
            self.showLeftWeaponModels(False)
        else:
            self.showLeftWeaponModels(True)
        if self.isWeaponNeedHide(False):
            self.showRightWeaponModels(False)
        else:
            self.showRightWeaponModels(True)
        opaVal = self.getYuanLingOpacityValue()
        if self.modelServer.yuanLing:
            self.modelServer.yuanLing.hide(not opaVal == gameglobal.OPACITY_FULL)

    def getYuanLingOpacityValue(self):
        if self.bianshen and self.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            data = ZJD.data.get(self.bianshen[1], {})
            bsType = data.get('BsType', 1)
            if bsType == attachedModel.ZAIJU_REPLACE:
                return gameglobal.OPACITY_HIDE
        return self.getOpacityValue()[0]

    def isBackWearNeedHide(self):
        if getattr(self, 'buffAttachModel', False):
            if hasattr(self.modelServer, 'backwear') and self.modelServer.backwear:
                if self.modelServer.backwear.state == attachedModel.HANG_UP:
                    return True
        return False

    def showBackWearNeedHide(self, show):
        models = self.fashion.getBackWearModels()
        if not models:
            return
        for m in models:
            if m:
                m.visible = show

    def refreshBackWearVisible(self):
        try:
            if self.isBackWearNeedHide():
                self.showBackWearNeedHide(False)
            else:
                self.showBackWearNeedHide(True)
        except:
            pass

    def showLeftWeaponModels(self, show, force = False):
        if getattr(self, 'isFlyLeftWeapon', False):
            return
        lwm = self.fashion.getLeftWeaponModels()
        for m in lwm:
            if m in self.followModel:
                if self.isSkillAttachOther() or force or self.inModelReplace():
                    m.visible = show
                else:
                    m.visible = self.getOpacityValue()[0] == gameglobal.OPACITY_FULL
            else:
                m.visible = show

        for weapon in self.modelServer.leftWeaponBackup:
            for item in weapon.models:
                if item[1]:
                    item[0].visible = show

    def showRightWeaponModels(self, show, force = False):
        if getattr(self, 'isFlyRightWeapon', False):
            return
        lwm = self.fashion.getRightWeaponModels()
        for m in lwm:
            if m in self.followModel:
                if self.isSkillAttachOther() or force:
                    m.visible = show
                else:
                    m.visible = self.getOpacityValue()[0] == gameglobal.OPACITY_FULL
            else:
                m.visible = show

        for weapon in self.modelServer.rightWeaponBackup:
            for item in weapon.models:
                if item[1]:
                    item[0].visible = show

    def setModelActionSpeed(self, model, speedData):
        if not model or not speedData:
            return
        for k, v in speedData.iteritems():
            try:
                if str(k) in self.fashion.action.actionList:
                    aq = self.model.action(str(k))
                    aq.setMinSpeed(v[0])
                    aq.setMaxSpeed(v[1])
            except:
                pass

    def getModelSpeedData(self, speedId):
        speedData = HWSD.data.get(speedId, {})
        return speedData.get('actionSpeed', {})

    def resetAmActionSpeed(self):
        if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            speedId = self.getCompoundRideSpeedSubId()
            actionSpeedData = self.getModelSpeedData(speedId)
            self.setModelActionSpeed(self.modelServer.rideModel, actionSpeedData)
        elif self.inFly:
            speedId = self.getCompoundWingSpeedSubId()
            actionSpeedData = self.getModelSpeedData(speedId)
            self.setModelActionSpeed(self.model, actionSpeedData)

    def playLandToFlyAction(self):
        landToFlyAction = self.fashion.getLandToFlyAction()
        if landToFlyAction:
            try:
                self.model.action(landToFlyAction)()
                if getattr(self.model, 'ride', None) and landToFlyAction in self.model.ride.actionNameList():
                    self.model.ride.action(landToFlyAction)()
                    self.playRideTogetherAction(landToFlyAction)
            except:
                pass

    def playFlyToLandAction(self):
        flyToLandAction = self.fashion.getFlyToLandAction()
        if flyToLandAction:
            try:
                self.model.action(flyToLandAction)()
                if getattr(self.model, 'ride', None) and flyToLandAction in self.model.ride.actionNameList():
                    self.model.ride.action(flyToLandAction)()
                    self.playRideTogetherAction(flyToLandAction)
            except:
                pass

    def resetFly(self, showEffect = True):
        if not self.inWorld:
            return
        elif not hasattr(self, 'am'):
            return
        else:
            if self.canFly():
                if self.isJumping:
                    self.fashion.breakJump()
                self.isDashing = False
                self.am.applyFlyRoll = True
                self.playLandToFlyAction()
                state = qingGong.STATE_IN_COMBAT_IDLE if self.inCombat else qingGong.STATE_WINGFLY_IDLE
                self.qinggongMgr.setState(state)
                if self.isOnFlyRide():
                    self.modelServer.setFlyRideFloat()
                else:
                    floatage = BigWorld.PyPoseControl()
                    self.model.floatage = floatage
                    floatage.floatHeight = SYSCD.data.get('flyModelFloatHeight', 0.4)
                    floatage.popToTerrain = False
                self.model.needUpdateUnitRotation = False
                self.model.enlargeShadowBoundingBox(gameglobal.SHOWSHADOW_WINGFLY_BOUNDINGBOX[0], gameglobal.SHOWSHADOW_WINGFLY_BOUNDINGBOX[1], gameglobal.SHOWSHADOW_WINGFLY_BOUNDINGBOX[2], gameglobal.SHOWSHADOW_WINGFLY_BOUNDINGBOX[3], gameglobal.SHOWSHADOW_WINGFLY_BOUNDINGBOX[4], gameglobal.SHOWSHADOW_WINGFLY_BOUNDINGBOX[5])
            else:
                self.am.applyFlyRoll = False
                self.qinggongMgr.setState(qingGong.STATE_IDLE)
                self.modelServer.oldFootTwistSpeed = SYSCD.data.get('footTwistSpeed', gameglobal.FOOTTWISTSPEED)
                self.am.footTwistSpeed = self.modelServer.oldFootTwistSpeed
                self.playFlyToLandAction()
                if self.isOnFlyRide():
                    self.modelServer.setFlyRideFloat()
                elif hasattr(self.model, 'floatage'):
                    self.model.floatage = None
                self.model.needUpdateUnitRotation = True
                self.model.enlargeShadowBoundingBox(gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[0], gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[1], gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[2], gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[3], gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[4], gameglobal.SHOWSHADOW_DEFAULT_BOUNDINGBOX[5])
            self.modelServer.setHorseFootTwistSpeed()
            self.fashion.autoSetStateCaps()
            self.filter.applyEntityPitch = self.needApplyEntityPitch()
            self.modelServer.refreshWingFlyState(showEffect, not self.inWingTakeOff)
            self.refreshWeaponVisible()
            self.modelServer.refreshBackWearVisible()
            if self.isInCoupleRideAsHorse():
                other = BigWorld.entity(self.getOtherIDInCoupleEmote())
                if other and other.inWorld:
                    BigWorld.callback(0.1, other.resetTopLogo)
            self.resetTopLogo()
            if self.tride:
                for eid in self.tride.keys():
                    vice = BigWorld.entities.get(eid, None)
                    if vice:
                        vice.resetTopLogo()

            self.resetShadowUfo()
            self.updateBodySlope()
            gameglobal.rds.ui.mounts.refresFlyView()
            if self.canFly():
                if self.inWingTakeOff and self == BigWorld.player() and not self.takeOffActionPlayed:
                    self.takeOffActionPlayed = True
                    self.wingFlyTakeOff()
            return

    def needApplyEntityPitch(self):
        return self.inFly or self.inSwim == const.DEEPWATER

    def set_inFly(self, old):
        if not self.fashion:
            return
        self.modelServer.wingFlyModelUpdate(True)
        self.resetFly(True)
        self.resetFootIK()
        if not self.inFly and old and not self.inMoving():
            self.fashion.stopAllActions()
            wingFlyFastFallEndAction = self.fashion.getWingFlyFastFallEndAction()
            self.fashion.playSingleAction(wingFlyFastFallEndAction, ACT.WING_LAND_END_ACTION)
        if self.inFlyTypeFlyRide():
            fallAction = self.fashion.getHorseFallRunDownAction()
            if self.model and fallAction in self.model.queue:
                self.fashion.stopActionByName(self.model, fallAction)
        if self == BigWorld.player():
            self.refreshHorseWingEffect()
        if self.fashion.footTriggerMgr:
            self.fashion.footTriggerMgr.refreshFootIdleEffect()
        if old == gametypes.IN_FLY_OBSERVER or self.inFly == gametypes.IN_FLY_OBSERVER:
            self.refreshOpacityState()
        if self.modelServer:
            self.modelServer.updateFashionIdleEffect()
        p = BigWorld.player()
        if self.inFly and not old and (self.id == p.tride.header or getattr(p.getCoupleRideHorse(), 'id', 0) == self.id):
            if p.spriteObjId:
                p.suggestSpriteFly(True, False)
        self.apEffectEx.resetEffect()

    def wingFlyTakeOff(self):
        wingFlyStartReadyAction = self.fashion.action.getWingFlyStartReadyAction(self.fashion)
        wingFlyStartAction = self.fashion.action.getWingFlyStartAction(self.fashion)
        wingFlyStartToIdleAction = self.fashion.action.getWingFlyStartToIdleAction(self.fashion)
        self.modelServer.refreshWingModelOpacity()
        try:
            readyAct = self.model.action(wingFlyStartReadyAction)
            link = readyAct(0, self.wingFlyStartReadyCallback, 0)
            if wingFlyStartAction:
                link = getattr(link, wingFlyStartAction)(0, self.wingFlyStartCallback, 0)
                if wingFlyStartToIdleAction:
                    getattr(link, wingFlyStartToIdleAction)()
            effects = SYSCD.data.get('takeOffEffect')
            if effects:
                for effect in effects:
                    sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                     self.getBasicEffectPriority(),
                     self.model,
                     effect,
                     sfx.EFFECT_LIMIT_MISC,
                     gameglobal.EFFECT_LAST_TIME))

        except:
            gamelog.error('wingFlyTakeOff miss action')

    def wingFlyStartReadyCallback(self):
        if self == BigWorld.player():
            self.ap.upSpeedMultiplier = PCD.data.get('wingTakeOffSpeed', gametypes.WING_TAKE_OFF_SPEED)
            self.ap.physics.upSpeedAttenu = PCD.data.get('wingTakeOffSpeedAttenu', gametypes.WING_TAKE_OFF_SPEED_ATTENU)
            self.ap.upwardMagnitude = 1
            self.fashion.setDoingActionType(ACT.WING_TAKE_OFF_ACTION)
            self.ap.updateVelocity()

    def wingFlyStartCallback(self):
        self.inWingTakeOff = False
        self.modelServer.refreshWingModelOpacity()
        wingModel = self.modelServer.wingFlyModel.model
        wingFlyStartToIdleAction = self.fashion.action.getWingFlyStartToIdleAction(self.fashion)
        try:
            wingModel.action(wingFlyStartToIdleAction)()
        except:
            pass

        if self.fashion.doingActionType() == ACT.WING_LAND_ACTION:
            return
        if self == BigWorld.player():
            self.updateActionKeyState()
            self.ap.upwardMagnitude = 0
            self.ap.setUpSpeedMultiplier()
            self.ap.physics.upSpeedAttenu = 0
            self.ap.updateVelocity()

    def getDaZuoEff(self):
        daZuoEff = SYSCD.data.get('daZuoEff', {})
        bodyType = charRes.transBodyType(self.physique.sex, self.physique.bodyType)
        return daZuoEff.get(bodyType, ((), (), ()))

    def startDaZuo(self):
        if not self.inWorld:
            return
        else:
            self.fashion.stopAction()
            daZuoStartAction = self.fashion.action.getDaZuoStartAction(self.fashion)
            daZuoLoopAction = self.fashion.action.getDaZuoLoopAction(self.fashion)
            daZuoEff = self.getDaZuoEff()
            playSeq = []
            playSeq.append((daZuoStartAction,
             daZuoEff[0],
             ACT.DA_ZUO_ACTION,
             0,
             1.0,
             None))
            playSeq.append((daZuoLoopAction,
             daZuoEff[1],
             ACT.DA_ZUO_ACTION,
             0,
             1.0,
             None))
            self.fashion.disableFootIK(True)
            self.fashion.playActionWithFx(playSeq, ACT.DA_ZUO_ACTION, None, False, 0, 1.0, self.getBasicEffectPriority())
            if self == BigWorld.player():
                gameglobal.rds.ui.actionbar.setRideShine(True, uiConst.DAZUOING)
            return

    def resetDaZuo(self):
        if not self.inWorld:
            return
        else:
            self.fashion.stopAction()
            daZuoLoopAction = self.fashion.action.getDaZuoLoopAction(self.fashion)
            daZuoEff = self.getDaZuoEff()
            playSeq = []
            playSeq.append((daZuoLoopAction,
             daZuoEff[1],
             ACT.DA_ZUO_ACTION,
             0,
             1.0,
             None))
            self.fashion.disableFootIK(True)
            self.fashion.playActionWithFx(playSeq, ACT.DA_ZUO_ACTION, None, False, 0, 1.0, self.getBasicEffectPriority())
            return

    def stopDaZuo(self):
        if not self.inWorld:
            return
        else:
            if self.daZuoState == const.DA_ZUO_LEAVE_NORMAL:
                self.fashion.stopAction()
                playSeq = []
                daZuoStopAction = self.fashion.action.getDaZuoStopAction(self.fashion)
                daZuoEff = self.getDaZuoEff()
                playSeq.append((daZuoStopAction,
                 daZuoEff[2],
                 ACT.DA_ZUO_ACTION,
                 0,
                 1.0,
                 None))
                self.fashion.playActionWithFx(playSeq, ACT.DA_ZUO_ACTION, None, False, 0, 1.0, self.getBasicEffectPriority())
            elif self.daZuoState == const.DA_ZUO_LEAVE_NO_ACTION:
                self.fashion.stopAction()
            self.fashion.disableFootIK(False)
            if self == BigWorld.player():
                gameglobal.rds.ui.actionbar.setRideShine(False, uiConst.DAZUOING)
            return

    def set_daZuoState(self, old):
        if not self.fashion:
            return
        if self.inDaZuo():
            self.startDaZuo()
        else:
            self.stopDaZuo()

    def inDaZuo(self):
        return self.daZuoState == const.DA_ZUO_START

    def set_teleportSpell(self, old):
        if not self.fashion:
            return
        if self.inTeleportSpell():
            self.playTeleportSpell()
        else:
            self.stopTeleportSpell()

    def inTeleportSpell(self):
        return self.teleportSpell

    def isWuDiState(self):
        return self._getFlag(gametypes.SKILL_STATE_SE_WUDI) or self._getFlag(gametypes.SKILL_STATE_IMMUNE_ATTACK) or self._getFlag(gametypes.FLAG_WUDI) or self._getFlag(gametypes.FLAG_NOT_SKILL_TARGET)

    def set_flags(self, old):
        if hasattr(self, 'topLogo'):
            self.topLogo.setWuDi(self.isWuDiState())

    def set_jctSeq(self, oldValue):
        if self.jctSeq:
            self.changeClanWarHunt(True)
        elif oldValue:
            self.changeClanWarHunt(False)

    def set_publicFlags(self, old):
        if not self.inWorld:
            return
        elif not hasattr(self, 'fashion'):
            return
        else:
            if commcalc.getBitDword(self.publicFlags, gametypes.FLAG_NOT_CONTROLLABLE):
                self.am.moveNotifier = None
                if self.fashion.isPlayer:
                    self.physics.userDirected = False
                else:
                    self.am.turnModelToEntity = False
                self.filter.clientYawMinDist = 0.0
                if hasattr(self.filter, 'keepYawTime'):
                    self.filter.keepYawTime = 999999
            else:
                if self.fashion.isPlayer:
                    self.physics.userDirected = True
                self.am.moveNotifier = self.fashion.movingNotifier
            if commcalc.hasFlagChanged(self.publicFlags, old, gametypes.FLAG_HIDE):
                self.refreshOpacityState()
            if hasattr(self, 'topLogo'):
                self.topLogo.setWuDi(self.isWuDiState())
            return

    def set_currTitle(self, old):
        self.refreshToplogoTitle()

    def set_activeTitleType(self, old):
        self.refreshToplogoTitle()

    def set_currPropTitleEx(self, old):
        pass

    def set_guildName(self, old):
        if self.activeTitleType == const.ACTIVE_TITLE_TYPE_WORLD:
            currTitleId = self.currTitle[const.TITLE_TYPE_WORLD]
            if currTitleId and TD.data.get(currTitleId).get('gId') == gametypes.FAME_GROUP_GUILD:
                self.refreshToplogoTitle()

    def setExp(self, value, old, srcId):
        pass

    def set_abilityData(self, old):
        pass

    def showSpecialQuestsExp(self, targetId, incExp, times, exp):
        pass

    def setCash(self, value, old, srcId):
        pass

    def setBindCash(self, value, old, srcId):
        pass

    def setExpXiuWei(self, value, old, srcId):
        pass

    def setStorageCash(self, value, old):
        pass

    def setBirthTime(self, birthTime):
        pass

    def setOnlineTime(self, onlineTime):
        pass

    def setDelayExp(self, value, old, targetId):
        pass

    def setDelayCash(self, value, old, targetId):
        pass

    def setDelayBindCash(self, value, old, targetId):
        pass

    def onSendLvUpRewardData(self, rewardData):
        pass

    def set_isolateType(self, old):
        pass

    def getPrimaryPropBaseValue(self, propId):
        if propId not in PDD.data.PRIMARY_PROPERTIES:
            return 0
        if propId == PDD.data.PROPERTY_ATTR_PW:
            v = self.primaryProp.bpow
        elif propId == PDD.data.PROPERTY_ATTR_INT:
            v = self.primaryProp.bint
        elif propId == PDD.data.PROPERTY_ATTR_PHY:
            v = self.primaryProp.bphy
        elif propId == PDD.data.PROPERTY_ATTR_SPR:
            v = self.primaryProp.bspr
        elif propId == PDD.data.PROPERTY_ATTR_AGI:
            v = self.primaryProp.bagi
        return v

    def resSetPropValData(self, propVal):
        pass

    def resSetRadarData(self, radarData):
        pass

    def getCoupleEmoteID(self, data = None):
        if data is None:
            data = getattr(self, 'coupleEmote', (None,))
        if len(data) == 0:
            return
        else:
            return data[0]

    def isInCoupleRide(self, data = None):
        return self.getCoupleEmoteID(data)

    def isInCoupleRideAsHorse(self, data = None):
        return self.isInCoupleRide(data) and self.coupleEmote[1] == self.id

    def isInCoupleRideAsRider(self, data = None):
        return self.isInCoupleRide(data) and self.coupleEmote[2] == self.id

    def getCoupleRideHorse(self):
        if not self.isInCoupleRide():
            return None
        else:
            return BigWorld.entities.get(self.coupleEmote[1], None)

    def getCoupleKey(self, withEmoteId = False):
        other = BigWorld.entity(self.getOtherIDInCoupleEmote())
        if getattr(other, 'modelServer', None) is None or getattr(other, 'model', None) is None:
            return
        if self.coupleEmote[2] == self.id:
            man = other
            woman = self
        else:
            man = self
            woman = other
        if not man or not man.inWorld:
            return
        elif not woman or not woman.inWorld:
            return
        sexType = man.physique.sex
        if man.physique.sex == woman.physique.sex and man.physique.sex == 1:
            sexType = gameglobal.COUPLE_SEX_MAN_MAN
        if man.physique.sex == woman.physique.sex and man.physique.sex == 2:
            sexType = gameglobal.COUPLE_SEX_WOMAN_WOMAN
        if withEmoteId:
            return (self.coupleEmote[0],
             sexType,
             man.physique.bodyType,
             woman.physique.bodyType)
        else:
            return (sexType, man.physique.bodyType, woman.physique.bodyType)

    def needShowCoupleFKey(self):
        if not self.coupleEmote:
            return
        return CEBD.data.get(self.coupleEmote[0], {}).get('showFKey', 0)

    def set_coupleEmote(self, old):
        if not self.isInCoupleRide(old) and self.isInCoupleRide():
            self.lastCoupleRideTime = BigWorld.time()
            self.modelServer.enterCoupleEmote()
            self.emoteActionCancel()
            if self == BigWorld.player():
                gameglobal.rds.ui.actionbar.setRideShine(True, uiConst.COUPLEEMOTE)
                keyboardEffect.addKeyboardEffect('effect_love')
                if self.isInCoupleRideAsHorse() and self.needShowCoupleFKey():
                    gameglobal.rds.ui.pressKeyF.isKiss = True
                    gameglobal.rds.ui.pressKeyF.setType(const.F_KISS)
                fbNo = formula.getFubenNo(self.spaceNo)
                if fbNo == const.FB_NO_MARRIAGE_AMERICAN_HALL and gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
                    BigWorld.callback(1, Functor(self.wantToDoEmote, const.EMOTE_KISS_ID))
        elif self.isInCoupleRide(old) and not self.isInCoupleRide():
            self.modelServer.leaveCoupleEmote(old)
            if self == BigWorld.player():
                gameglobal.rds.ui.actionbar.setRideShine(False, uiConst.COUPLEEMOTE)
                keyboardEffect.removeKeyboardEffect('effect_love')
            if gameglobal.rds.ui.pressKeyF.isKiss:
                gameglobal.rds.ui.pressKeyF.isKiss = False
                gameglobal.rds.ui.pressKeyF.removeType(const.F_KISS)
        if self == BigWorld.player().targetLocked:
            BigWorld.player().ap.releaseTargetLockedEffect()
        if self == BigWorld.player():
            BigWorld.callback(0, gameglobal.rds.ui.actionbar.updateEmoteItemCooldown)
            BigWorld.callback(1, gameglobal.rds.ui.skill.refreshEmotePanel)

    def isRidingTogether(self):
        return self.isRidingTogetherAsMain() or self.isRidingTogetherAsVice()

    def isRidingTogetherAsMain(self):
        return hasattr(self, 'tride') and self.tride.isMajor(self.id)

    def isRidingTogetherAsVice(self):
        return hasattr(self, 'tride') and self.tride.has_key(self.id)

    def getRidingTogetherMain(self):
        if not self.isRidingTogether():
            return None
        else:
            return self.tride.getHeader()

    def set_tride(self, old):
        self.modelServer.refreshRideTogether(old)
        self.refreshOpacityState()
        targetId = getattr(BigWorld.player().targetLocked, 'id', 0)
        if self.id == targetId or targetId in self.tride.keys() or old and targetId in old.keys():
            BigWorld.callback(0.2, BigWorld.player().ap.releaseTargetLockedEffect)
        self.refreshTRideSpecialAction()

    def set_carrier(self, old):
        self.oldCarrier = old
        carrierState = self.carrier.carrierState
        oldCarrierState = old.carrierState
        if carrierState == gametypes.MULTI_CARRIER_STATE_RUNNING or oldCarrierState == gametypes.MULTI_CARRIER_STATE_RUNNING:
            carrierEntId = self.carrier.carrierEntId
            if not carrierEntId:
                carrierEntId = old.carrierEntId
            carrierEnt = BigWorld.entities.get(carrierEntId, None)
            for entId, idx in old.iteritems():
                if self.carrier.keys():
                    if not self.carrier.has_key(entId):
                        ent = BigWorld.entities.get(entId)
                        if ent and ent.inWorld:
                            ent.modelServer.leaveCarrier(carrierEnt)
                elif old.has_key(entId):
                    ent = BigWorld.entities.get(entId)
                    if ent and ent.inWorld and hasattr(ent, 'carrier') and not ent.carrier.has_key(entId):
                        ent.modelServer.leaveCarrier(carrierEnt)

        if carrierState == gametypes.MULTI_CARRIER_STATE_RUNNING:
            for entId, idx in self.carrier.iteritems():
                ent = BigWorld.entities.get(entId)
                if ent and ent.inWorld:
                    ent.modelServer.enterCarrier()

        self.resetCarrierReadyEmote(old)
        if self.modelServer.leftWeaponModel:
            BigWorld.callback(0.1, self.modelServer.leftWeaponModel.calFollowBiasPos)
        self.refreshOpacityState()

    def set_wingWorldCarrier(self, old):
        self.oldWingWorldCarrier = old
        carrierEntId = self.wingWorldCarrier.carrierEntId
        if not carrierEntId:
            carrierEntId = old.carrierEntId
        carrierEnt = BigWorld.entities.get(carrierEntId, None)
        for entId, idx in old.iteritems():
            if self.wingWorldCarrier.keys():
                if not self.wingWorldCarrier.has_key(entId):
                    ent = BigWorld.entities.get(entId)
                    if ent and ent.inWorld:
                        ent.modelServer.leaveWingWorldCarrier(carrierEnt)
            elif old.has_key(entId):
                ent = BigWorld.entities.get(entId)
                if ent and ent.inWorld and hasattr(ent, 'wingWorldCarrier') and not ent.wingWorldCarrier.has_key(entId):
                    ent.modelServer.leaveWingWorldCarrier(carrierEnt)

        for entId, idx in self.wingWorldCarrier.iteritems():
            ent = BigWorld.entities.get(entId)
            if ent and ent.inWorld:
                ent.modelServer.enterWingWorldCarrier()

        if self.modelServer.leftWeaponModel:
            BigWorld.callback(0.1, self.modelServer.leftWeaponModel.calFollowBiasPos)
        if self.isOnWingWorldCarrier():
            self.setTargetCapsUse(False)
            player = BigWorld.player()
            if player.targetLocked == self:
                player.unlockTarget()
        else:
            self.setTargetCapsUse(True)
        self.refreshOpacityState()

    def resetCarrierReadyEmote(self, oldCarrier):
        if not self.topLogo:
            return
        self.topLogo.initTopLogoAni()
        if self.carrier.isReadyState():
            if self.carrier.has_key(self.id):
                emote = SCD.data.get('multiCarrierReadyEmote')
                self.topLogo.showEmote(emote, True)
            elif oldCarrier.has_key(self.id):
                self.topLogo.stopBigEmote()
        else:
            self.topLogo.stopBigEmote()

    def inInteractiveObject(self):
        return self.interactiveObjectEntId

    def set_interactiveObjectId(self, old):
        interactiveChangeFashionId = getattr(self, 'interactiveChangeFashionId', 0)
        self.calcInteractiveChangeFashionId()
        self.modelServer.bodyPartsUpdate(False, interactiveChangeFashionIdOld=interactiveChangeFashionId)

    def set_interactiveObjectEntId(self, old):
        if self.inInteractiveObject():
            self.modelServer.enterInteractiveObject()
        else:
            self.modelServer.leaveInteractiveObject(old)
            self.interactiveActionId = None

    def isSkillAttachOther(self):
        return self.attachSkillData[0] != 0

    def isSkillBeAttached(self):
        return self.attachSkillData[1] != 0

    def getPhysicsYOffset(self):
        offsetMap = SYSCD.data.get('actionPhysicsYOffsetMap', {})
        offsets = offsetMap.get(self.realSchool, [])
        offset = offsets[gameglobal.AIM_CROSS_HEIGHT] if len(offsets) > gameglobal.AIM_CROSS_HEIGHT else None
        if offset and len(offset) >= gameglobal.ACTION_PHYSICS_Y_OFFSET_MAX_STEP:
            return offset
        else:
            return gameglobal.ACTION_PHYSICS_Y_OFFSET

    def enoughFame(self, need):
        for fId, val in need:
            if not self.fame.has_key(fId):
                fameVal = utils.getFameInitVal(fId, self.school)
                if fameVal < val:
                    return False
            elif self.fame[fId] < val:
                return False

        return True

    def confirmUpgradeSkills(self, needSkillPoint, toActivateSkillPoint, needCash):
        gamelog.info('jjh@confirmUpgradeSkills ', needSkillPoint, toActivateSkillPoint, needCash)
        msg = GMD.data.get(GMDD.data.UPGRADE_SKILL_CONSUME_CASH_DOUBLE_CONFIRM, {}).get('text', '%d%d')
        msg = msg % (toActivateSkillPoint, needCash)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(gameglobal.rds.ui.skill.skillInfoManager.confirmUpgradeSkills, needCash))

    def skillPointSchemeSend(self, schemes):
        pass

    def onCipherModified(self, cipher):
        pass

    def onCipherValidate(self, r, cipher):
        pass

    def getEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFFECT_MID
            p = BigWorld.player()
            if p.hasInDyingAround() and p.id != self.id and BigWorld.player().isInMyTeam(self):
                return gameglobal.EFFECT_CLOSE
            elif BigWorld.player().isFriend(self):
                return getattr(BigWorld.player(), 'otherAvatarEffectLv', gameglobal.EFFECT_MID)
            else:
                return getattr(BigWorld.player(), 'enemyAvatarEffectLv', gameglobal.EFFECT_MID)
        else:
            return gameglobal.EFFECT_MID

    def getSkillEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFFECT_MID
            if not self.inWorld:
                return gameglobal.EFFECT_MID
            effectLv = self.getEffectLv()
            if BigWorld.player().isEnemy(self):
                lv = ELD.data.get('enemyAvatar', {}).get('content', {}).get(effectLv)[0]
            else:
                lv = ELD.data.get('friendAvatar', {}).get('content', {}).get(effectLv)[0]
            return self.getClanWarEffectLv(lv)
        else:
            return gameglobal.EFFECT_MID

    def getBeHitEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFFECT_MID
            if not self.inWorld:
                return gameglobal.EFFECT_MID
            effectLv = self.getEffectLv()
            if BigWorld.player().isEnemy(self):
                lv = ELD.data.get('enemyAvatar', {}).get('content', {}).get(effectLv)[1]
            else:
                lv = ELD.data.get('friendAvatar', {}).get('content', {}).get(effectLv)[1]
            return self.getClanWarEffectLv(lv)
        else:
            return gameglobal.EFFECT_MID

    def getBuffEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFFECT_MID
            if not self.inWorld:
                return gameglobal.EFFECT_MID
            effectLv = self.getEffectLv()
            lv = ELD.data.get('enemyAvatar', {}).get('content', {}).get(effectLv)[2]
            return self.getClanWarEffectLv(lv)
        else:
            return gameglobal.EFFECT_MID

    def getEquipEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFFECT_MID
            if not self.inWorld:
                return gameglobal.EFFECT_MID
            effectLv = self.getEffectLv()
            if BigWorld.player().isEnemy(self):
                lv = ELD.data.get('enemyAvatar', {}).get('content', {}).get(effectLv)[3]
            else:
                lv = ELD.data.get('friendAvatar', {}).get('content', {}).get(effectLv)[3]
            return self.getClanWarEffectLv(lv)
        else:
            return gameglobal.EFFECT_MID

    def getBasicEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFFECT_MID
            if not self.inWorld:
                return gameglobal.EFFECT_MID
            effectLv = self.getEffectLv()
            if BigWorld.player().isEnemy(self):
                lv = ELD.data.get('enemyAvatar', {}).get('content', {}).get(effectLv)[4]
            else:
                lv = ELD.data.get('friendAvatar', {}).get('content', {}).get(effectLv)[4]
            return self.getClanWarEffectLv(lv)
        else:
            return gameglobal.EFFECT_MID

    def getSkillEffectPriority(self):
        if sfx.gNoAvatarEffect and (utils.instanceof(self, 'Avatar') or utils.instanceof(self, 'AvatarRobot')):
            return gameglobal.EFF_NO_PRIORITY
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFF_HIGHEST_PRIORITY
            if not self.inWorld:
                return gameglobal.EFF_LOWEST_PRIORITY
            if BigWorld.player().isFriend(self):
                return gameglobal.EFF_FRIEND_SKILL_PRIORITY
            if BigWorld.player().isEnemy(self):
                return gameglobal.EFF_ENEMY_SKILL_PRIORITY
        return gameglobal.EFF_DEFAULT_PRIORITY

    def getBeHitEffectPriority(self, host):
        if sfx.gNoAvatarEffect and (utils.instanceof(self, 'Avatar') or utils.instanceof(self, 'AvatarRobot')):
            return gameglobal.EFF_NO_PRIORITY
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFF_HIGHEST_PRIORITY
            if host and host.inWorld:
                if host == BigWorld.player():
                    return gameglobal.EFF_PLAYER_BEHIT_PRIORITY
                elif host.IsAvatar and BigWorld.player().isFriend(host):
                    return gameglobal.EFF_FRIEND_BEHIT_PRIORITY
                elif host.IsAvatar and BigWorld.player().isEnemy(host):
                    return gameglobal.EFF_ENEMY_BEHIT_PRIORITY
                else:
                    return gameglobal.EFF_MONSTER_BEHIT_PRIORITY
            else:
                return gameglobal.EFF_DEFAULT_PRIORITY
        else:
            return gameglobal.EFF_DEFAULT_PRIORITY

    def getBuffEffectPriority(self, host):
        if sfx.gNoAvatarEffect and (utils.instanceof(self, 'Avatar') or utils.instanceof(self, 'AvatarRobot')):
            return gameglobal.EFF_NO_PRIORITY
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFF_HIGHEST_PRIORITY
            if host and host.inWorld:
                if host == BigWorld.player() or BigWorld.player().isRealInFuben() and getattr(host, 'IsMonster', False):
                    return gameglobal.EFF_PLAYER_BUFF_PRIORITY
                elif host.IsAvatar:
                    return gameglobal.EFF_ENEMY_BUFF_PRIORITY
                else:
                    return gameglobal.EFF_MONSTER_BUFF_PRIORITY
            else:
                return gameglobal.EFF_DEFAULT_PRIORITY
        else:
            return gameglobal.EFF_DEFAULT_PRIORITY

    def getEquipEffectPriority(self):
        if sfx.gNoAvatarEffect and (utils.instanceof(self, 'Avatar') or utils.instanceof(self, 'AvatarRobot')):
            return gameglobal.EFF_NO_PRIORITY
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFF_HIGHEST_PRIORITY
            if not self.inWorld:
                return gameglobal.EFF_LOWEST_PRIORITY
            if BigWorld.player().isFriend(self):
                return gameglobal.EFF_FRIEND_EQUIP_PRIORITY
            if BigWorld.player().isEnemy(self):
                return gameglobal.EFF_ENEMY_EQUIP_PRIORITY
        return gameglobal.EFF_DEFAULT_PRIORITY

    def getBasicEffectPriority(self):
        if sfx.gNoAvatarEffect and (utils.instanceof(self, 'Avatar') or utils.instanceof(self, 'AvatarRobot')):
            return gameglobal.EFF_NO_PRIORITY
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if gameglobal.rds.GameState <= gametypes.GS_LOADING:
                return gameglobal.EFF_HIGHEST_PRIORITY
            if not self.inWorld:
                return gameglobal.EFF_LOWEST_PRIORITY
            if BigWorld.player().isFriend(self):
                return gameglobal.EFF_FRIEND_BASIC_PRIORITY
            if BigWorld.player().isEnemy(self):
                return gameglobal.EFF_ENEMY_BASIC_PRIORITY
        return gameglobal.EFF_DEFAULT_PRIORITY

    def showSafeMode(self):
        pass

    def onCipherResetTimeChange(self, cipherResetTime):
        self.cipherResetTime = cipherResetTime
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.cipherResetTime = self.cipherResetTime

    def upDateExpBonusData(self, freeze, data):
        self.expBonusFreeze = freeze
        for bId, remainTime, expireTime, nCurr, lastGetTime in data:
            self.expBonus[bId] = (remainTime,
             expireTime,
             nCurr,
             lastGetTime)

        gameglobal.rds.ui.expBonus.expBonusData = self.expBonus
        gameglobal.rds.ui.expBonus.isFreezed = freeze
        if gameglobal.rds.ui.expBonus.mediator:
            gameglobal.rds.ui.expBonus.updateData()
        newTotalTime = gameglobal.rds.ui.expBonus.getTotalRemainTime()
        if newTotalTime and not self.expBonusFreeze:
            gameglobal.rds.ui.expbar.setExpBgColor(True)
        else:
            gameglobal.rds.ui.expbar.setExpBgColor(False)
        expBonusEvent = Event(events.EVENT_EXP_BONUS_UPDATE, {'freeze': freeze,
         'totalTime': newTotalTime})
        gameglobal.rds.ui.dispatchEvent(expBonusEvent)
        gameglobal.rds.ui.diGongDetail.refreshDigongDetail()

    def onGetFameRewardTime(self, fameId, rewardList):
        gameglobal.rds.ui.funcNpc.refreshNpcFameSalaryOption(fameId, rewardList)

    def onApplyFameRewardSucc(self, fameId):
        gameglobal.rds.ui.fameSalary.hideByFameId(fameId)

    def onGetCustomerServiceAnnouncement(self, announcement, category):
        gamelog.debug('@zqc [impProperty.py:1383]ImpProperty.onGetCustomerServiceAnnouncement', locals())
        p = BigWorld.player()
        if not BigWorld.player():
            return
        if gameglobal.rds.configData.get('enableCustomerVipService', False):
            vipLevel = utils.getVipGrade(p)
            level1 = SCD.data.get('VIP_LEVEL_1', 3)
            if vipLevel <= level1:
                gameglobal.rds.ui.customerService.showCallBack(announcement, category)
            else:
                gameglobal.rds.ui.customerServiceVip.showCallBack(announcement, category)
        else:
            gameglobal.rds.ui.customerService.showCallBack(announcement, category)

    def onGetCustomerServiceCategory(self, category, content):
        gamelog.debug('@zqc [impProperty.py:1386]ImpProperty.onGetCustomerServiceCategory', locals())
        gameglobal.rds.ui.customerServiceSecond.show(content)

    def getIndulgeProfitState(self):
        if not gameglobal.rds.configData.get('enableAntiIndulgence', True):
            return const.INDULGE_PROFIT_HEALTHY
        elif self.getIndulgeOnlineTimeNow() < const.INDULGE_ONLINE_HALF_TIRED_TIME:
            return const.INDULGE_PROFIT_HEALTHY
        elif self.getIndulgeOnlineTimeNow() < const.INDULGE_ONLINE_TIRED_TIME:
            return const.INDULGE_PROFIT_HALF_TIRED
        else:
            return const.INDULGE_PROFIT_TIRED

    def getIndulgeOnlineTimeNow(self):
        if self.indulgeStartTime == 0:
            return self.indulgeOnlineTime
        return self.indulgeOnlineTime + utils.getNow() - self.indulgeStartTime

    def immuneControl(self):
        if self == BigWorld.player():
            return commcalc.getBitDword(self.flags, gametypes.FLAG_IMMUNE_CONTROL) or commcalc.getBitDword(self.flags, gametypes.FLAG_IMMUNE_BAD_STATE) or commcalc.getBitDword(self.flags, gametypes.FLAG_WUDI)
        else:
            return commcalc.getBitDword(self.publicFlags, gametypes.FLAG_IMMUNE_CONTROL) or commcalc.getBitDword(self.publicFlags, gametypes.FLAG_IMMUNE_BAD_STATE) or commcalc.getBitDword(self.publicFlags, gametypes.FLAG_WUDI)

    def inRoundTable(self):
        return self.belongToRoundTable != 0

    def set_belongToRoundTable(self, old):
        if self.inRoundTable():
            self.modelServer.enterRoundTable()
        else:
            self.modelServer.leaveRoundTable(old)

    def pushIndulgeMessage(self, onlineTime, offlineTime, st):
        pass

    def clearIndulgeMessage(self):
        self.showGameMsg(GMDD.data.UPDATE_INDULGE_STATE_VALID, ())
        gameglobal.rds.ui.indulgePush.clearMsg()

    def pushQumoSalaryApplyInfo(self, salaryType):
        self.updateRewardHallInfo(uiConst.REWARD_QUMO)

    def setSavedOperationMode(self, mode):
        if self.isInBfDota():
            self.operation['dotaOperationMode'] = mode
        else:
            self.operation['commonSetting'][0] = mode

    def getSavedOperationMode(self):
        if self.isInBfDota():
            return self.operation.get('dotaOperationMode', self.getOperationMode())
        else:
            return self.operation['commonSetting'][0]

    def onClickGetExtAct(self, page):
        gameglobal.rds.ui.roleInfo.show(page)

    def onJunJieSalaryApplyAvaliable(self, hasZhanXunReward, hasExtraZhanXunReward):
        if hasZhanXunReward or hasExtraZhanXunReward:
            self.updateRewardHallInfo(uiConst.REWARD_JUNJIE)

    def onApplyActivityAchieveScoreAwardAvailable(self):
        enableActivityScore = gameglobal.rds.configData.get('enableActivityScore', False)
        if enableActivityScore:
            gameglobal.rds.ui.welfareMergeServer.notifyActivityScorePushMsg()

    def showNoviceBoostPanel(self, paneClicked):
        if paneClicked:
            gameglobal.rds.ui.newbieGuide.showGuideIcon()
        else:
            gameglobal.rds.ui.newbieGuide.show()

    def pushPollInfo(self, pollId):
        self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_IMPPROPERTY_2075,))
        gameglobal.rds.ui.votePush.notifyBonusPushMsg(pollId)

    def revokePollInfo(self, pollId):
        self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_IMPPROPERTY_2079,))
        gameglobal.rds.ui.votePush.hideVote(pollId)

    def revokeAllPollInfo(self):
        self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.TEXT_IMPPROPERTY_2083,))
        gameglobal.rds.ui.votePush.hideAllVote()

    def voteForPollSucc(self, pollId):
        gameglobal.rds.ui.votePush.voteSucceed(pollId)

    def voteForPollFail(self, pollId):
        gameglobal.rds.ui.votePush.voteFailed(pollId)

    def pushSecuNotCompleteInfo(self):
        gameglobal.rds.ui.completeInfo.pushCompleteMsg()

    def pushSecuNotApplyRewardInfo(self):
        if utils.enableBindReward():
            if self.weixinBindStatus != gametypes.BIND_STATUS_SUCC:
                return
            if self.appBindStatus != gametypes.BIND_STATUS_SUCC:
                return
        gameglobal.rds.ui.completeInfo.pushRewardMsg()

    def closeSecuPanel(self):
        if gameglobal.rds.ui.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_COMPLETE_INFO):
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_COMPLETE_INFO)
        if gameglobal.rds.ui.pushMessage.msgs.has_key(uiConst.MESSAGE_TYPE_COMPLETE_INFO_REWARD):
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_COMPLETE_INFO_REWARD)

    def onSyncNoviceBoostRewardInfo(self, lowReward, highReward):
        gameglobal.rds.ui.newbieGuide.setRewardInfo(lowReward, highReward)

    def onQueryBackflowVp(self, amount):
        pass

    def onGetBackflowVp(self, ok):
        if ok:
            gameglobal.rds.ui.xiuYingExpGet.refreshInfo(ok)

    def notifyFlowbackBonusAvailableOnLogin(self):
        pass

    def notifyCompensateInfoOnLogin(self, hasAccountBonus):
        gameglobal.rds.ui.xiuYingExpGet.compensateInfoOnLogin(hasAccountBonus)

    def onGetCompensationResult(self, hasCompensateData, compId):
        if hasCompensateData:
            gameglobal.rds.ui.closeCompensation1(compId)
            gameglobal.rds.ui.closeCompensation2(compId)
            if hasattr(self, 'compInfo'):
                if len(self.compInfo) > 0:
                    self.compInfo.pop()
            else:
                self.compInfo = []
            gameglobal.rds.ui.itemQuestV2.hide()
        else:
            self.showGameMsg(GMDD.data.GET_COMPENSATION_FAIL, ())

    def addGPoint(self, delta):
        defaultName = SCD.data.get('GPointName', '')
        if defaultName != '':
            gameglobal.rds.ui.showDefaultLabel(defaultName, delta, '#FFCC31')

    def onResetDaily(self):
        pass

    def sendDailyStats(self, data):
        pass

    def set_groupType(self, old):
        gameglobal.rds.ui.refreshTeamLogoOrIdentity(self.id)

    def set_groupHeader(self, old):
        gameglobal.rds.ui.refreshTeamLogoOrIdentity(self.id)

    def set_numOfTeamMember(self, old):
        gameglobal.rds.ui.refreshTeamLogoOrIdentity(self.id)

    def set_battleFieldDotaLv(self, old):
        p = BigWorld.player()
        if p.isInBfDota() and getattr(self, 'IsAvatar', False) and hasattr(self, 'topLogo'):
            self.topLogo.setLv(self.battleFieldDotaLv)

    def set_partnerMemberCnt(self, old):
        self.refreshPartnerTitle()

    def set_partnerSigMidType(self, old):
        self.refreshPartnerTitle()

    def set_partnerSigPostfix(self, old):
        self.refreshPartnerTitle()

    def set_partnerSigPrefix(self, old):
        self.refreshPartnerTitle()

    def set_realInScriptFlag(self, old):
        self.topLogo.setAutoPlayScenarioVisible(self.realInScriptFlag)

    def onFbAvoidDieItemCntUpdate(self, num):
        self.fbAvoidDieItemCnt = num
        gameglobal.rds.ui.player.setFbAvoidDieCnt(num)

    def onGetStateMonitorClientConfig(self, pickledConfig):
        """
        \xe8\x8e\xb7\xe5\xbe\x97pickle\xe8\xbf\x87\xe7\x9a\x84\xe7\x8a\xb6\xe6\x80\x81\xe7\x9b\x91\xe6\x8e\xa7\xe9\x85\x8d\xe7\xbd\xae\xe6\x95\xb0\xe6\x8d\xae
        :param pickledConfig: \xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe9\x80\x9a\xe8\xbf\x87setStateMonitorClientConfig\xe8\xae\xbe\xe7\xbd\xae\xe7\x9a\x84\xef\xbc\x8c\xe7\x99\xbb\xe5\xbd\x95/\xe8\xb7\xa8\xe6\x9c\x8d/\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe5\x8e\x9f\xe6\xa0\xb7\xe5\x8f\x91\xe5\x9b\x9e\xe6\x9d\xa5
        
        
        pickledConfig =
        {
            buffListenerEnable : 0,           # \xe6\x98\xaf\xe5\x90\xa6\xe5\xbc\x80\xe5\x90\xafbuff\xe7\x9b\x91\xe6\x8e\xa7
        
            size : 1,                        # \xe5\xa4\xa7\xe5\xb0\x8f\xe5\xb0\xba\xe5\xaf\xb8 1 \xe5\xb0\x8f 2 \xe5\xa4\xa7
                         
            buffConfig : {                   # buff\xe5\x85\x88\xe5\x85\xb3\xe4\xbf\xa1\xe6\x81\xaf
        
                listenerType : {
        
                    listenerId : {
        
                        bListener : 0 ,
                        icon : 0 ,
        
                    }
                }
            } 
        }
        
        """
        p = BigWorld.player()
        if pickledConfig:
            configData = cPickle.loads(zlib.decompress(pickledConfig))
            gamelog.debug('@zq onGetStateMonitorClientConfig', configData)
            self.buffListenerConfig = configData
        else:
            gamelog.debug('@zq onGetStateMonitorClientConfig None')
            self.buffListenerConfig = {}
        p.reCalcBuffListenerIds()

    def reCalcBuffListenerIds(self):
        p = BigWorld.player()
        p.genAllBuffListeningIds()
        gameglobal.rds.ui.buffListenerShow.refreshInfo()
        gameglobal.rds.ui.buffListenerSetting.refreshInfo()

    def genAllBuffListeningIds(self):
        p = BigWorld.player()
        dataRet = gameglobal.rds.ui.buffListenerSetting.genListenerBuffData()
        p.listeningBuffShowData = dict()
        for data in dataRet:
            if not data.get('isTitle', 0):
                listenerId = data.get('listenerId', 0)
                if listenerId and listenerId in p.listenerBuffData and p.listenerBuffData[listenerId]['bListener']:
                    p.listeningBuffShowData[listenerId] = p.listenerBuffData[listenerId]

        return p.listeningBuffShowData

    def enableBuffListenerFunc(self, enable):
        buffListenerConfig = copy.deepcopy(self.buffListenerConfig)
        buffListenerConfig['buffListenerEnable'] = enable
        self.base.setStateMonitorClientConfig(zlib.compress(cPickle.dumps(buffListenerConfig)))

    def onCheckExpAddParamBuff(self, val):
        self.expAddParamBuffVal = val

    def onGetExpPursueGuide(self, showList):
        gameglobal.rds.ui.playRecommExpPursue.onGetExpPursueData(showList)

    def onCheckExpPursueGuide(self, isShow):
        if getattr(self, 'isShowPursueGuide', False) != isShow:
            self.isShowPursueGuide = isShow
            gameglobal.rds.ui.playRecommPushIcon.refreshExpPursueVisible()

    def writePosStrToFile(self, str):
        gamelog.info('jbx:writePosStrToFile', str)
        file = open('getPos.txt', 'a+')
        file.write(str)
        file.close()

    def onSyncPlayerMaxXiuweiLv(self, playerMaxXiuweiLv):
        self.playerMaxXiuweiLv = playerMaxXiuweiLv

    def checkRefineEquipmentFlagIdle(self):
        if self.refineEquipmentFlag and self.firstFetchFinished and gameconfigCommon.enableRefineManualEquipment():
            lastIdleTime = getattr(self, 'lastIdleTime', 0)
            lastPosition = getattr(self, 'lastPosition', self.position)
            if (self.position - lastPosition).lengthSquared > 0.1 or utils.getNow() - lastIdleTime > SCD.data.get('refineEquipmentEffectLoop', 15):
                effectId = SCD.data.get('refineEquipmentEffectId', 118131)
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 effectId,
                 sfx.EFFECT_LIMIT))
                self.lastIdleTime = utils.getNow()
                self.lastPosition = self.position

    def set_refineEquipmentFlag(self, old):
        pass

    def set_chatAnonymity(self, old):
        p = BigWorld.player()
        if p.anonymNameMgr:
            p.anonymNameMgr.updateEntityShowInfo(self)
