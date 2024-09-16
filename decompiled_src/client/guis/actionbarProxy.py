#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/actionbarProxy.o
from gamestrings import gameStrings
gameStrings.TEXT_ACTIONBARPROXY_1
gameStrings.TEXT_ACTIONBARPROXY_2
gameStrings.TEXT_ACTIONBARPROXY_3
gameStrings.TEXT_ACTIONBARPROXY_4
gameStrings.TEXT_ACTIONBARPROXY_5
import copy
import BigWorld
from Scaleform import GfxValue
import math
import keys
import gameglobal
import logicInfo
import const
import skillDataInfo
import gametypes
import commcalc
import gamelog
import utils
import formula
import tipUtils
import wingWorldUtils
from guis import uiConst
from helpers.eventDispatcher import Event
from callbackHelper import Functor
from uiProxy import SlotDataProxy
from ui import gbk2unicode
from gameclass import SkillInfo
from skillDataInfo import checkSelfRequest, checkTargetRelationRequest
from helpers import cellCmd
from item import Item
from appSetting import Obj as AppSettings
from guis import uiUtils
from gameclass import PSkillInfo
from guis import hotkey
from guis import events
from guis import ui
from guis import chickenFoodFactory
from guis import hotkey as HK
from gameStrings import gameStrings
from sfx import keyboardEffect
from helpers.attachedModel import WEAR_ATTACH_ACTION_AS_ENTITY
from gameglobal import SKILL_STAT_SKILL_TGT, SKILL_STAT_LACK_ENERGY, SKILL_STAT_NO_SKILL, SKILL_STAT_IN_SKILL_RANGE, SKILL_STAT_BAN_WS_SKILL, SKILL_STAT_BAN_SKILL
from data import sys_config_data as SCD
from data import couple_emote_basic_data as CEBD
from cdata import home_config_data as HCD
from data import life_skill_data as LSD
from cdata import game_msg_def_data as GMDD
from data import general_skill_config_data as GSCD
from data import school_data as SD
from data import item_data as ID
from cdata import font_config_data as FCD
from data import skill_panel_data as SPD
from data import skill_icon_color_data as SICD
from data import ws_skill_config_data as WSCD
from cdata import pskill_data as PD
from data import sys_config_data as SCFD
from data import emote_data as ED
from data import consumable_item_data as CID
from data import consume_state_data as CSD
from data import school_switch_general_data as SSGD
from data import skill_general_template_data as SGTD
from data import state_data as STD
from data import skill_state_client_data as SSCD
from data import equip_data as EQD
from cdata import yaopei_lv_data as YLD
from data import skill_general_data as SGD
from data import intimacy_skill_data as ISD
from data import world_war_army_skill_data as WWASD
from cdata import pskill_data as PSD
from data import equip_data as EPD
from data import wing_world_army_skill_data as WIWASD
from data import map_config_data as MCD
from data import guild_skill_data as GSD
from data import duel_config_data as DCD
skillIconPath = 'skill/icon/'
skillIconPath64 = 'skill/icon64/'
iconSuffix = '.dds'
ALL_SKILL = 0
COMMON_SKILL = 1
WUSHUANG_SKILL = 2
APP_SETTING_ACTIONBAR_PATH = keys.SET_UI_INFO + '/itembar/'
ASAP_LOCK = APP_SETTING_ACTIONBAR_PATH + 'lock'
ASAP_TYPE = APP_SETTING_ACTIONBAR_PATH + 'type'
ASAP_TYPE2 = APP_SETTING_ACTIONBAR_PATH + 'type2'
ASAP_ROW = APP_SETTING_ACTIONBAR_PATH + 'row'
ASAP_ROW2 = APP_SETTING_ACTIONBAR_PATH + 'row2'
TWEEN_VIRUSSAFE_ADD = 1
TWEEN_VIRUSSAFE_REDUCE = 2
ITEMBAR_TYPE_1 = 0
ITEMBAR_TYPE_2 = 1
SHORT_CUT_CASE_NUM = 3

class ActionbarProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ActionbarProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'actionbar'
        self.type = 'actionbar'
        self.clientShortCut = {}
        self.actionbarDataIsInit = False
        self.callbackHandler = {}
        self.modelMap = {'getWSValue': self.onGetWSValue,
         'getWSType': self.onGetWSType,
         'getWSName': self.onGetWSName,
         'getItemBarConfig': self.onGetItemBarConfig,
         'changeItemBarType': self.onChangeItemBarType,
         'changeItembarRow': self.onChangeItembarRow,
         'getSchoolInfo': self.onGetSchoolInfo,
         'getLockState': self.onGetLockState,
         'setLockState': self.onSetLockState,
         'resetShortCut': self.onResetShortCut,
         'getInitActionbarData': self.onGetInitActionbarData,
         'getInitWuShuangbarData': self.onGetInitWuShuangbarData,
         'getInitItembarData': self.onGetInitItembarData,
         'refreshSchoolStateKBE': self.onRefreshSchoolStateKBE,
         'changeSkillCase': self.onChangeSkillCase,
         'changeEquip': self.onChangeEquip,
         'getOneKeyConfig': self.onGetOneKeyConfig}
        self.mc = None
        self.wsMc = None
        self.itemMc = [None, None]
        self.wsColorMap = {3: ['shengtang_left', 'shengtang_right'],
         4: ['yuxu_left', 'yuxu_right'],
         5: ['guangren_left', 'guangren_right'],
         6: ['yantian_left', 'yantian_right'],
         7: ['linlong_left', 'linlong_right'],
         8: ['liuguang_left', 'liuguang_right'],
         9: ['yesha_left', 'yesha_right'],
         10: ['tianzhao_left', 'tianzhao_right']}
        self.skillStates = {}
        self.slotKey = self.getDefaultKeyDesc()
        self.useSelfSkill = False
        self.switchSkill = set([])
        self.recordAnimation = [False] * 18
        self.otherSkill = {}
        self.itemBarType = [AppSettings.get(ASAP_TYPE, 1), AppSettings.get(ASAP_TYPE2, 1)]
        self.itemBarRow = [AppSettings.get(ASAP_ROW, 2), AppSettings.get(ASAP_ROW2, 2)]
        self.isLock = AppSettings.get(ASAP_LOCK, 0) == 1
        self.isShowItemBar = True
        self.isShowItemBar2 = True
        self.skillInfoCache = {}
        self.skillStatCache = {}
        self.skillIconStat = {}
        self.validateSlotCallBack = None
        self.needRefreshCenter = True
        self.uiid = 0
        self.resetActionbarMsgBoxMulId = 0
        self.currSchemeNo = 0
        self.lifeSkill = [uiConst.LIFE_SKILL_FISHING, uiConst.LIFE_SKILL_EXPLORE]
        data = LSD.data
        for key in data.keys():
            self.lifeSkill.append(key[0])

        data = GSCD.data
        for k in data:
            self.otherSkill[data.get(k).get('skillid')] = k

        self.needSaveClientCut = False

    def needHideCommonSkillActionBar(self):
        p = BigWorld.player()
        if p.bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
            return True
        if p.inInteractiveObject():
            return True
        if p.gmFollow > 0:
            return True
        if p.life == gametypes.LIFE_DEAD:
            return True
        inAirBattle = gameglobal.rds.ui.skill.inAirBattleState()
        if inAirBattle:
            return True
        if formula.getFubenNo(p.obSpaceNo) in const.GUILD_FUBEN_ELITE_NOS:
            return True
        return False

    def refreshCommonSkillActionBarOpacity(self):
        if self.mc:
            if self.needHideCommonSkillActionBar():
                self.mc.Invoke('setVisible', GfxValue(False))
            else:
                self.mc.Invoke('setVisible', GfxValue(True))

    def needHideWsSkillActionBar(self):
        p = BigWorld.player()
        if p.bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
            return True
        if p.inInteractiveObject():
            return True
        if p.gmFollow > 0:
            return True
        if p.life == gametypes.LIFE_DEAD:
            return True
        return False

    def refreshWsSkillActionBarOpacity(self):
        if self.wsMc:
            if self.needHideWsSkillActionBar():
                self.wsMc.Invoke('setVisible', GfxValue(False))
            else:
                self.wsMc.Invoke('setVisible', GfxValue(True))

    def refreshSkillActionBarOpacity(self):
        self.refreshCommonSkillActionBarOpacity()
        self.refreshWsSkillActionBarOpacity()

    def _registerMediator(self, widgetId, mediator):
        self._initActionBarData()
        if widgetId == uiConst.WIDGET_ACTION_BARS:
            self.mc = mediator
            if hasattr(BigWorld.player(), 'hotkeyData') and BigWorld.player().hotkeyData:
                self.setSlotKeyText(self.slotKey)
            else:
                self.resetSlotKey()
                self.setSlotKeyText(self.slotKey)
            if BigWorld.player().bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
                self.mc.Invoke('setVisible', GfxValue(False))
                gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ACTION_BARS, False)
            self.refreshActionbar()
        elif widgetId == uiConst.WIDGET_ITEMBAR:
            self.itemMc[0] = mediator
            if hasattr(BigWorld.player(), 'hotkeyData') and BigWorld.player().hotkeyData:
                self.setItemBarKeyText(self.slotKey[uiConst.WUSHUANG_SKILL_END_POS:])
            else:
                self.resetSlotKey()
                self.setItemBarKeyText(self.slotKey[uiConst.WUSHUANG_SKILL_END_POS:])
        elif widgetId == uiConst.WIDGET_ITEMBAR2:
            self.itemMc[1] = mediator
            if hasattr(BigWorld.player(), 'hotkeyData') and BigWorld.player().hotkeyData:
                self.setItemBarKeyText(self.slotKey[uiConst.ITEM_BAR1_END_POS:], uiConst.TYPE_ITEM_BAR2)
            else:
                self.resetSlotKey()
                self.setItemBarKeyText(self.slotKey[uiConst.ITEM_BAR1_END_POS:], uiConst.TYPE_ITEM_BAR2)
        elif widgetId == uiConst.WIDGET_WUSHUANG_BARS:
            self.wsMc = mediator
            if hasattr(BigWorld.player(), 'hotkeyData') and BigWorld.player().hotkeyData:
                self.setSlotKeyText(self.slotKey)
            else:
                self.resetSlotKey()
                self.setSlotKeyText(self.slotKey)
            if BigWorld.player().bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
                self.wsMc.Invoke('setVisible', GfxValue(False))
                gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WUSHUANG_BARS, False)
            self.changeWsBarState(False)
            self.refreshActionbar()
        self.checkAvatarState()

    def _getSkillIcon(self, skillId, level = 1, icon64 = False):
        if not skillId:
            return 'notFound'
        if GSD.data.has_key(skillId) and GSD.data.get(skillId, {}).get('clientSkill', 0):
            skillId = GSD.data.get(skillId, {}).get('clientSkill', 0)
        if skillId == uiConst.COUPLEEMOTE:
            iconPath = 'misc/coupleEmote.dds'
            return iconPath
        if skillId == uiConst.EQUIP_FEED:
            iconPath = 'misc/equipFeed.dds'
            return iconPath
        if skillId in (uiConst.INTIMACY_SKILL_AXBD,
         uiConst.INTIMACY_SKILL_SSXS,
         uiConst.INTIMACY_SKILL_DJTC,
         uiConst.INTIMACY_SKILL_MARRIAGE):
            iconPath = 'skill/icon/%d.dds' % ISD.data.get((skillId, level), {}).get('icon', 0)
            return iconPath
        whichIcon = 0
        p = BigWorld.player()
        if skillId == uiConst.HORSE_RIDING:
            whichIcon = 1 if BigWorld.player().equipment[gametypes.EQU_PART_RIDE] else 2
        elif skillId == uiConst.WING_FLYING:
            whichIcon = 1 if BigWorld.player().equipment[gametypes.EQU_PART_WINGFLY] else 2
        elif skillId == uiConst.DAZUOING:
            whichIcon = 1
        elif skillId == uiConst.BOOTH:
            whichIcon = 1
        elif skillId == uiConst.RIDE_TOGETHER:
            condition = p.tride.inRide()
            condition &= not p.isOnRideTogetherHorse()
            whichIcon = 2 if condition else 1
        else:
            whichIcon = 1
        if whichIcon > 0:
            data = GSCD.data
            for k in data:
                skill = data[k]
                if skill.get('skillid') == skillId:
                    iconPath = 'generalSkill/' + skill['icon' + str(whichIcon)] + '.dds'
                    return iconPath

        sVal = BigWorld.player().getSkills().get(skillId)
        if sVal:
            level = sVal.level
        try:
            if hasattr(p, 'skillAppearancesDetail'):
                skilldata = p.skillAppearancesDetail.getGeneralAppearanceSkillInfo(skillId, level)
            else:
                skilldata = skillDataInfo.ClientSkillInfo(skillId, level, 0)
            icon = skilldata.getSkillData('icon', 'notFound')
        except:
            icon = 'notFound'

        if icon64:
            path = skillIconPath64
        else:
            path = skillIconPath
        return path + str(icon) + iconSuffix

    def getSkillGfxData(self, skillId):
        return {'iconPath': self._getSkillIcon(skillId)}

    def getActionIDByPos(self, nBar, nSlot):
        return self.getShortCut(nBar, nSlot, [0, 0])[1]

    def _getPosByActionID(self, skillId):
        pos = self.getShortCutPos(skillId)
        return [ self._getKey(*item) for item in pos ]

    def reset(self):
        self.actionbarDataIsInit = False
        self.binding = {}
        self.clientShortCut = {}
        self.skillStates = {}
        gameglobal.rds.ui.actionbar.showMouseIcon(True)
        self.mc = None
        self.wsMc = None
        self.itemMc = [None, None]
        self.isLock = AppSettings.get(ASAP_LOCK, 0) == 1
        self.uiid = 0

    def checkState(self):
        p = BigWorld.player()
        for i, v in self.binding.items():
            bar, slot = self.getSlotID(i)
            idNum = self.getShortCut(bar, slot, [0, 0])[1]
            if p.spellingType and idNum != p.skillId or not logicInfo.isUseableSkill(idNum) or not skillDataInfo.checkSkillRequest(p.skillId, p.skillLevel):
                v[0].Invoke('setEnabled', GfxValue(False))
            else:
                v[0].Invoke('setEnabled', GfxValue(True))

    def disableSlot(self, skillId):
        key = self._getPosByActionID(skillId)
        for item in key:
            if self.binding.has_key(item) and self.skillIconStat[skillId] != uiConst.SKILL_ICON_STAT_RED:
                self.setSlotState(skillId, uiConst.SKILL_ICON_STAT_GRAY)

    def onNotifySlotUse(self, *arg):
        key = arg[3][0].GetString()
        bar, idNum = self.getSlotID(key)
        if bar == uiConst.SKILL_ACTION_BAR:
            self.useItem(bar, idNum, False, False)
        elif bar in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
            self.useItem(bar, idNum, False, False)
        elif bar == uiConst.EQUIP_ACTION_BAR:
            p = BigWorld.player()
            if p._isSchoolSwitch():
                return
            if idNum >= const.SUB_EQUIP_PART_OFFSET:
                it = commcalc.getAlternativeEquip(p, idNum - const.SUB_EQUIP_PART_OFFSET)
                isSubEquip = True
            else:
                it = p.equipment.get(idNum)
                isSubEquip = False
            if not it:
                return
            if gameglobal.rds.ui.equipFeed.mediator and not isSubEquip:
                gameglobal.rds.ui.equipFeed.setItem(bar, idNum, 0, 0, it, False)
            elif gameglobal.rds.ui.yaoPeiFeed.mediator and not isSubEquip:
                if idNum == gametypes.EQU_PART_YAOPEI:
                    gameglobal.rds.ui.yaoPeiFeed.showInEquip()
            else:
                page, pos = p.realInv.searchEmptyInPages()
                if pos != const.CONT_NO_POS:
                    if p.isInPUBG():
                        cellCmd.exchangeCrossInvEqu(page, pos, idNum)
                    else:
                        cellCmd.exchangeInvEqu(page, pos, idNum)
                else:
                    p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())

    def onNotifySlotMouseDown(self, *arg):
        key = arg[3][0].GetString()
        bar, idNum = self.getSlotID(key)
        if bar == uiConst.SKILL_ACTION_BAR:
            self.useItem(bar, idNum, True, False)
        elif bar in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
            self.useItem(bar, idNum, True, False)

    def onSlotMouseOver(self, *arg):
        key = arg[3][0].GetString()
        bar, idNum = self.getSlotID(key)
        if bar == uiConst.SKILL_ACTION_BAR:
            info = self.getShortCut(bar, idNum)
            if info and info[0] == uiConst.SHORTCUT_TYPE_SKILL:
                itemId = info[1]
                BigWorld.player().playHoverEffect(itemId)

    def onSlotMouseOut(self, *arg):
        key = arg[3][0].GetString()
        bar, idNum = self.getSlotID(key)
        if bar == uiConst.SKILL_ACTION_BAR or bar in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
            BigWorld.player().stopHoverEffect()

    def _resetWsSkillActionBar(self):
        p = BigWorld.player()
        wsValue = p.ws
        maxValue = p.mws
        val1 = self.movie.CreateArray()
        i = 0
        for item in wsValue:
            val1.SetElement(i, GfxValue(int(math.floor(item / 100.0))))
            i += 1

        val2 = self.movie.CreateArray()
        i = 0
        for item in maxValue:
            val2.SetElement(i, GfxValue(int(math.floor(item / 100.0))))
            i += 1

        self.mc.Invoke('setWS', (val1, val2, GfxValue(True)))
        self.wsMc.Invoke('setWS', (val1, val2, GfxValue(True)))

    def _getSkillLv(self, skillId):
        curLv = 1
        sVal = BigWorld.player().getSkills().get(skillId, None)
        if sVal:
            curLv = sVal.level
        return curLv

    def useSkill(self, bar, soltId, isDown = False, isKeyMode = True, autoUseSkill = False):
        utils.recusionLog(10)
        gamelog.debug('@useSkill', gameglobal.rds.bar, gameglobal.rds.soltId)
        if isDown:
            gameglobal.rds.bar = bar
            gameglobal.rds.soltId = soltId
        else:
            gameglobal.rds.bar = None
            gameglobal.rds.soltId = None
        info = self.getShortCut(bar, soltId, [0, 0])
        skillId = info[1]
        p = BigWorld.player()
        if p._isOnZaijuOrBianyao() and gameglobal.rds.soltId != None:
            if gameglobal.rds.ui.zaiju.mediator:
                skillId, skillLv = gameglobal.rds.ui.zaiju.getSkillInfo(gameglobal.rds.soltId)
            else:
                skillId, skillLv = gameglobal.rds.ui.zaijuV2.getSkillInfo(gameglobal.rds.soltId)
        p.nowSkillId = skillId
        self.useSkillById(skillId, isDown, isKeyMode, autoUseSkill)
        p.nowSkillId = None

    def useSkillById(self, skillId, isDown, isKeyMode, autoUseSkill):
        p = BigWorld.player()
        if gameglobal.rds.ui.skill.inAirBattleState() and skillId not in p.airSkills and not isDown:
            p.showGameMsg(GMDD.data.SKILL_CANT_USE_IN_FLY, ())
            return
        else:
            if p.skillQteData.has_key(skillId):
                skillId = p.skillQteData[skillId].qteSkills[0]
            if not skillId:
                return
            if skillId != BigWorld.player().circleEffect.skillID:
                BigWorld.player().circleEffect.cancel()
            if skillId != BigWorld.player().chooseEffect.skillID:
                BigWorld.player().chooseEffect.cancel()
            if p._isOnZaijuOrBianyao() and gameglobal.rds.soltId != None:
                if gameglobal.rds.ui.zaiju.mediator:
                    _, skillLevel = gameglobal.rds.ui.zaiju.getSkillInfo(gameglobal.rds.soltId)
                else:
                    _, skillLevel = gameglobal.rds.ui.zaijuV2.getSkillInfo(gameglobal.rds.soltId)
            else:
                skillLevel = self._getSkillLv(skillId)
            skillInfo = p.getSkillInfo(skillId, skillLevel)
            needAutoUseSkill = skillInfo.getSkillData('autoUseSkill', 0)
            if autoUseSkill:
                if not needAutoUseSkill:
                    return
            beastSkill = skillInfo.getSkillData('beastSkill', 0)
            beast = p.getBeast()
            if beastSkill and not beast:
                p.showGameMsg(GMDD.data.SKILL_CANT_USE_NO_BEAST, ())
                return
            isCastSelfKeyDown = hotkey.isCastSelfKeyDown()
            self.useSelfSkill = False
            oldOptionalTarget = p.optionalTargetLocked
            skillTargetType, skillTargetValue = p.getSkillTargetType(skillInfo)
            if skillTargetValue:
                if p.getOperationMode() == gameglobal.ACTION_MODE and p.optionalTargetLocked and not isCastSelfKeyDown:
                    pass
                elif skillTargetType == gametypes.SKILL_TARGET_SELF or skillTargetType == gametypes.SKILL_TARGET_SELF_FRIEND and (isCastSelfKeyDown or p.targetLocked == None or not p.isFriend(p.targetLocked) or utils.instanceof(p.targetLocked, 'OreSpawnPoint')) or skillTargetType == gametypes.SKILL_TARGET_SELF_ENERMY and (isCastSelfKeyDown or p.targetLocked == None or not p.isEnemy(p.targetLocked)) or skillTargetType == gametypes.SKILL_TARGET_ALL_TYPE and (isCastSelfKeyDown or p.targetLocked == None or not p.targetLocked.IsCombatUnit):
                    if not (gameglobal.NEED_CHOOSE_EFFECT and p.getOperationMode() == gameglobal.ACTION_MODE):
                        p.lastTargetLocked = p.targetLocked
                        if beastSkill and not isCastSelfKeyDown:
                            p.targetLocked = beast
                        else:
                            p.targetLocked = p
                        self.useSelfSkill = True
            if skillInfo.getSkillData('castType', gametypes.SKILL_FIRE_NORMAL) == gametypes.SKILL_FIRE_SWITCH and isDown:
                self.switchSkill.add((skillInfo.getSkillData('switchState', 0), skillId))
            if not isKeyMode:
                p.useSkillByMouseUp(isDown, skillInfo)
            else:
                p.useSkillByKeyDown(isDown, skillInfo)
            if self.useSelfSkill:
                temp = p.targetLocked
                p.targetLocked = p.lastTargetLocked
                if not p.targetLocked:
                    p.optionalTargetLocked = oldOptionalTarget
                if temp == p and p.targetLocked != p:
                    p.optionalTargetLocked = oldOptionalTarget
            return

    def _getKey(self, nBar, nSlot):
        return 'actionbar%d.slot%d' % (nBar, nSlot)

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[9:]), int(idItem[4:]))

    def _initActionBarData(self):
        zaiju = gameglobal.rds.ui.zaiju
        zaijuV2 = gameglobal.rds.ui.zaijuV2
        if (zaiju.mediator or zaijuV2.widget and zaijuV2.showType != uiConst.ZAIJU_SHOW_TYPE_EXIT) and self.mc:
            self.mc.Invoke('setVisible', GfxValue(False))
        if (zaiju.mediator or zaijuV2.widget and zaijuV2.showType != uiConst.ZAIJU_SHOW_TYPE_EXIT) and self.wsMc:
            self.wsMc.Invoke('setVisible', GfxValue(False))
        if gameglobal.rds.isSinglePlayer:
            return
        else:
            if not self.actionbarDataIsInit:
                self.clientShortCut = getattr(BigWorld.player(), 'shortcutData', {})
                if self.clientShortCut == {}:
                    if BigWorld.player()._isSchoolSwitch():
                        self.refreshActionbar()
                    else:
                        skillList = list(SD.data[BigWorld.player().school]['skillShortCut'])
                        generalSkills = list(SD.data[BigWorld.player().school].get('generalSkills', []))
                        for i, subList in enumerate(skillList):
                            self.clientShortCut[i] = {}
                            for j, skillId in enumerate(subList):
                                self.clientShortCut[i][uiConst.SKILL_ACTION_BAR, j] = (uiConst.SHORTCUT_TYPE_SKILL, skillId)

                            for generalSkill in generalSkills:
                                if not generalSkill[3]:
                                    self.clientShortCut[i][uiConst.SKILL_ACTION_BAR, generalSkill[2] - 1] = (generalSkill[1], generalSkill[0])

                        itemList = list(SD.data[BigWorld.player().school].get('items', []))
                        for item in itemList:
                            if BigWorld.player().realInv.hasItemInPages(item[0], includeExpired=True, includeLatch=True) and item[2]:
                                self.clientShortCut[uiConst.ITEM_ACTION_BAR, item[2] - 1] = (uiConst.SHORTCUT_TYPE_ITEM_COMSUME, item[0])

                        for generalSkill in generalSkills:
                            if generalSkill[3]:
                                self.clientShortCut[uiConst.ITEM_ACTION_BAR, generalSkill[2] - 1] = (generalSkill[1], generalSkill[0])

                        BigWorld.player().saveShortcut(self.clientShortCut)
                self._changeSelfSkills()
                self.skillStates = {}
                self.actionbarDataIsInit = True
                for k, v in self.getOtherShortCut().items():
                    if k[0] in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2] and not v[0] == uiConst.SHORTCUT_TYPE_ITEM_COMSUME:
                        self.refreshByBagUse(v[1])

                self.syncWshuangShortCutAndSelect()
                gameglobal.rds.ui.skill._initWsSkillList()
                if BigWorld.player().life == gametypes.LIFE_DEAD:
                    if self.mc != None:
                        self.mc.Invoke('setVisible', GfxValue(False))
                    if self.wsMc != None:
                        self.wsMc.Invoke('setVisible', GfxValue(False))
                    for i in xrange(2):
                        if self.itemMc[i] != None:
                            self.itemMc[i].Invoke('setVisible', GfxValue(False))

            return

    def syncWshuangShortCutAndSelect(self):
        p = BigWorld.player()
        selWsList = []
        if self.currSchemeNo == uiConst.SHORT_CUT_CASE_1:
            selWsList = p.wushuang1.selectedWs + p.wushuang2.selectedWs
        elif self.currSchemeNo == uiConst.SHORT_CUT_CASE_2:
            selWsList = p.wushuang1.selectedWs1 + p.wushuang2.selectedWs1
        elif self.currSchemeNo == uiConst.SHORT_CUT_CASE_3:
            selWsList = p.wushuang1.selectedWs2 + p.wushuang2.selectedWs2
        sc = self.getWuShuangSkillShortCut()
        shortCutList = map(lambda k: sc[k][1], sc)
        for skillId in selWsList:
            if isinstance(skillId, int) and skillId > 0 and skillId not in shortCutList:
                p.cell.removeWsSkill(skillId)

        for skillId in shortCutList:
            if isinstance(skillId, int) and skillId > 0 and skillId not in selWsList:
                try:
                    p.cell.addWsSkill(skillId)
                except:
                    pass

    def onCreateBinding(self, *arg):
        super(ActionbarProxy, self).onCreateBinding(*arg)
        key = arg[3][0].GetString()
        idCon, idItem = self.getSlotID(key)
        if idCon in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2] and not self.isItemBarInEdit():
            self.validateSlotVisible()

    def enableShortCutItem(self, id, enabled):
        for idSlot in range(uiConst.ITEM_ACTION_BAR_SLOT_NUM):
            for page in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
                ret = self.getShortCut(page, idSlot, [1, 1])
                if not (isinstance(ret, tuple) and len(ret) >= 2):
                    continue
                type = ret[0]
                idx = ret[1]
                if type != uiConst.SHORTCUT_TYPE_ITEM_COMSUME or type == uiConst.SHORTCUT_TYPE_ITEM_COMSUME and idx in self.otherSkill:
                    continue
                if id == idx:
                    if enabled:
                        self._setItemSlotState(page, idSlot, uiConst.SKILL_ICON_STAT_USEABLE)
                    else:
                        self._setItemSlotState(page, idSlot, uiConst.SKILL_ICON_STAT_RED)

    def getCountByType(self, item):
        if not item:
            return 0
        if item.type == item.BASETYPE_CONSUMABLE:
            count = BigWorld.player().realInv.countItemInPages(item.id, includeExpired=True, includeLatch=True)
            if not BigWorld.player()._isSoul() and gameglobal.rds.configData.get('enableUseCrossInv', False):
                count += BigWorld.player().crossInv.countItemInPages(item.id, includeExpired=True, includeLatch=True)
            return count
        if item.type == item.BASETYPE_EQUIP:
            obj, _, _ = BigWorld.player().realInv.findItemByUUID(item.uuid)
            if obj != const.CONT_EMPTY_VAL:
                return 1
            if self.checkHasEquipSkillItem(item):
                return 1
            ed = EPD.data.get(item.id, {})
            if ed.get('showWearId', 0):
                return 1
        return 0

    def getBagPagePosByBarPos(self, itemBarPage, itemBarPos):
        fromBag = const.RES_KIND_INV
        bagPage, bagPos = const.CONT_NO_PAGE, const.CONT_NO_POS
        if itemBarPage == const.CONT_NO_PAGE or itemBarPos == const.CONT_NO_POS:
            return (bagPage, bagPos, fromBag)
        info = self.getShortCut(itemBarPage, itemBarPos, [0, 0])
        if info[0] == uiConst.SHORTCUT_TYPE_ITEM_COMSUME:
            if not BigWorld.player()._isSoul():
                fromBag = const.RES_KIND_INV
                bagPage, bagPos = BigWorld.player().inv.findItemInPages(info[1], includeExpired=True, includeLatch=True, includeShihun=True)
                if (bagPage == const.CONT_NO_PAGE or itemBarPos == const.CONT_NO_POS) and gameglobal.rds.configData.get('enableUseCrossInv', False):
                    fromBag = const.RES_KIND_CROSS_INV
                    bagPage, bagPos = BigWorld.player().crossInv.findItemInPages(info[1], includeExpired=True, includeLatch=True, includeShihun=True)
            else:
                if gameglobal.rds.configData.get('enableCrossServerBag', False):
                    fromBag = const.RES_KIND_CROSS_INV
                else:
                    fromBag = const.RES_KIND_INV
                bagPage, bagPos = BigWorld.player().realInv.findItemInPages(info[1], includeExpired=True, includeLatch=True, includeShihun=True)
        elif info[0] == uiConst.SHORTCUT_TYPE_ITEM_EQUIP:
            fromBag = const.RES_KIND_INV
            _, bagPage, bagPos = BigWorld.player().realInv.findItemByUUID(info[-1])
        return (bagPage, bagPos, fromBag)

    def getBarPagePosByItem(self, item):
        ret = []
        page, pos = const.CONT_NO_PAGE, const.CONT_NO_POS
        if not isinstance(item, Item) or item == const.CONT_EMPTY_VAL:
            ret.append((page, pos))
            return ret
        for key, value in self.getOtherShortCut().items():
            if item.type == Item.BASETYPE_EQUIP:
                if value[0] == uiConst.SHORTCUT_TYPE_ITEM_EQUIP and value[2] == item.uuid:
                    ret.append(key)
                elif value[0] == uiConst.SHORTCUT_TYPE_ITEM_COMSUME and self.validRideItem(value[1], item.id):
                    ret.append(key)
                elif value[0] == uiConst.SHORTCUT_TYPE_EMOTE and self.validEmoteItem(value[1], item.id):
                    ret.append(key)
            elif item.type == Item.BASETYPE_CONSUMABLE:
                if value[1] == item.id:
                    ret.append(key)

        return ret

    def getItemByBarPagePos(self, page, pos):
        item = const.CONT_EMPTY_VAL
        info = self.getShortCut(page, pos, 0)
        if info:
            type = info[0]
            itemId = info[1]
            if type == uiConst.SHORTCUT_TYPE_ITEM_COMSUME:
                bagPage, bagPos = BigWorld.player().realInv.findItemInPages(itemId, includeExpired=True, includeLatch=True, includeShihun=True)
                if bagPage == const.CONT_NO_PAGE:
                    item = const.CONT_EMPTY_VAL
                else:
                    item = BigWorld.player().realInv.getQuickVal(bagPage, bagPos)
                if item == const.CONT_EMPTY_VAL:
                    item = Item(itemId, 1, False)
            elif type == uiConst.SHORTCUT_TYPE_ITEM_EQUIP:
                uuid = info[2]
                item, _, _ = BigWorld.player().realInv.findItemByUUID(uuid)
                if not item:
                    item = self.findItemInEquipMent(itemId)
            elif type == uiConst.SHORTCUT_TYPE_SKILL:
                item = itemId
            elif type == uiConst.SHORTCUT_TYPE_LIEF_SKILL:
                item = itemId
            elif type == uiConst.SHORTCUT_TYPE_EMOTE:
                item = itemId
            elif type == uiConst.SHORTCUT_TYPE_SKILL_MACRO:
                item = itemId
            if type in uiConst.SHORTCUT_TYPE_ITEM and item == const.CONT_EMPTY_VAL:
                item = Item(itemId, 1, False)
        return item

    def resetItemActionBar(self, page, pos):
        info = self.getShortCut(page, pos)
        if info:
            if info[0] == uiConst.SHORTCUT_TYPE_ITEM_COMSUME:
                itemId = info[1]
                for k, v in self.getOtherShortCut().items():
                    if v[1] == itemId:
                        page, pos = k
                        item = Item(itemId, 1, False)
                        self.setItem(item, page, pos, True, True, info[0])

            elif info[0] == uiConst.SHORTCUT_TYPE_ITEM_EQUIP:
                itemId = info[1]
                item = Item(itemId, 1, False)
                self.setItem(item, page, pos, True, True, info[0])

    def getSkillId(self, type):
        ids = []
        if type == WUSHUANG_SKILL:
            ids = [0] * 6
        elif type == COMMON_SKILL:
            ids = [0] * uiConst.WUSHUANG_SKILL_START_POS_LEFT
        elif type == ALL_SKILL:
            ids = [0] * 18
        else:
            ids = []
        for k, v in self.getAllSkillShortCut().iteritems():
            if k[0] == uiConst.SKILL_ACTION_BAR:
                if type == WUSHUANG_SKILL and k[1] >= uiConst.WUSHUANG_SKILL_START_POS_LEFT and v[0] == uiConst.SHORTCUT_TYPE_SKILL:
                    ids[k[1] - uiConst.WUSHUANG_SKILL_START_POS_LEFT] = v[1]
                elif type == COMMON_SKILL and k[1] < uiConst.WUSHUANG_SKILL_START_POS_LEFT and v[0] == uiConst.SHORTCUT_TYPE_SKILL:
                    ids[k[1]] = v[1]
                elif type == ALL_SKILL and v[1] != 0 and v[0] == uiConst.SHORTCUT_TYPE_SKILL:
                    ids[k[1]] = v[1]
            elif type == ALL_SKILL and k[0] in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2] and v[0] == uiConst.SHORTCUT_TYPE_SKILL and v[1] not in ids and v[1] != 0:
                ids.append(v[1])

        return ids

    def resetClientShortcut(self):
        self.clientShortCut = {}
        BigWorld.player().saveShortcut(self.clientShortCut)
        self.refreshAllActionbar()
        self.resetActionbarMsgBoxMulId = 0
        msg = gameStrings.TEXT_ACTIONBARPROXY_850
        BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [msg], 0, {})

    def getClientShortCut(self):
        return self.clientShortCut

    def setItemActionBarByItem(self, page, pos, item, isRefresh = True):
        info = self.getShortCut(page, pos)
        if info:
            if info[0] == uiConst.SHORTCUT_TYPE_ITEM_COMSUME:
                itemId = info[1]
                for k, v in self.getOtherShortCut().items():
                    if v[1] == itemId:
                        page, pos = k
                        self.setItem(item, page, pos, isRefresh, False, info[0])

            elif info[0] == uiConst.SHORTCUT_TYPE_ITEM_EQUIP:
                self.setItem(item, page, pos, isRefresh, False, info[0])

    def updateItemSlot(self):
        for i, v in self.binding.iteritems():
            bar, slotId = self.getSlotID(i)
            if bar not in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
                continue
            info = self.getShortCut(bar, slotId)
            if not info or info[0] not in uiConst.SHORTCUT_TYPE_ITEM:
                continue
            total = end = remain = 0
            itemId = info[1]
            idNum = itemId
            data = ID.data.get(idNum, None)
            if not data:
                if info[0] in uiConst.SHORTCUT_TYPE_ITEM and idNum not in self.otherSkill:
                    gamelog.error('item_data has no data, id =', idNum)
                continue
            typeNum = data.get('cdgroup', idNum)
            if idNum == None:
                continue
            if idNum in logicInfo.cooldownItem:
                end, total = logicInfo.cooldownItem[idNum]
                remain = end - BigWorld.time()
            if typeNum in logicInfo.commonCooldownItem:
                cend, ctotal = logicInfo.commonCooldownItem[typeNum]
                cremain = cend - BigWorld.time()
                if cremain > remain:
                    remain = cremain
                    total = ctotal
            v[0].Invoke('setShowNumber', GfxValue(True))
            if remain > 0:
                passTime = min(total - remain, total)
                v[0].Invoke('playCooldown', (GfxValue(total * 1000), GfxValue(passTime * 1000)))
                if self.callbackHandler.get(i, None):
                    BigWorld.cancelCallback(self.callbackHandler[i])
                self.callbackHandler[i] = BigWorld.callback(remain, Functor(self.afterItemEndCooldown, v[0]))

        if not gameglobal.rds.ui.inventory.mediator or gameglobal.rds.ui.inventory.page == uiConst.BAG_PAGE_QUEST:
            return
        else:
            self.updateInventoryItemCooldown()
            self.updateCrossServerItemCooldown()
            return

    def updateEmoteItemCooldown(self):
        for i, v in self.binding.items():
            bar, slotId = self.getSlotID(i)
            info = self.getShortCut(bar, slotId)
            if not info:
                continue
            total = end = remain = 0
            if info[0] == uiConst.SHORTCUT_TYPE_EMOTE and info[1] == uiConst.EMOTE_BIDONG:
                emoteId = ED.data.get(uiConst.EMOTE_BIDONG, {}).get('res', None)
                emoteId = int(emoteId) if emoteId else None
                endTime = BigWorld.player().cpEmoteSkillCD.get(emoteId, None)
                if not endTime:
                    continue
                total = CEBD.data.get(emoteId, {}).get('skillCD', 60)
                remain = endTime - utils.getNow()
            elif info[0] == uiConst.SHORTCUT_TYPE_ITEM_COMSUME and info[1] == uiConst.GO_HOME_ROOM:
                lastTime = BigWorld.player().myHome.lastUseBackHomeSkillTime
                total = HCD.data.get('backHomeSkillCD', 1800)
                remain = total + lastTime - utils.getNow()
            elif info[0] == uiConst.SHORTCUT_TYPE_ITEM_COMSUME and info[1] == uiConst.GO_WING_BORN_ISLAND:
                lastTime = BigWorld.player().wingWorldEnterSkillLastUseTime
                total = wingWorldUtils.getEnterBornIslandSkillCD()
                remain = total + lastTime - utils.getNow()
            elif info[0] == uiConst.SHORTCUT_TYPE_ITEM_COMSUME and info[1] == uiConst.LING_SHI_FLAG_SWITCH:
                total = SCD.data.get('lingShiCD', 5)
                remain = getattr(BigWorld.player(), 'lingShiNextTime', 0) - utils.getNow()
            if remain > 0:
                remain = total - remain
                if uiUtils.noNeedBackHomeCoolDown() and info[1] == uiConst.GO_HOME_ROOM:
                    v[0].Invoke('stopCooldown')
                    continue
                v[0].Invoke('playCooldown', (GfxValue(total * 1000), GfxValue(remain * 1000)))
                if self.callbackHandler.get(i, None):
                    BigWorld.cancelCallback(self.callbackHandler[i])
                self.callbackHandler[i] = BigWorld.callback(total - remain, Functor(self.afterItemEndCooldown, v[0]))

    def updateInventoryItemCooldown(self):
        for page, slot, idNum in self.getItemList():
            if page != gameglobal.rds.ui.inventory.page or id == None:
                continue
            total = end = remain = 0
            data = ID.data.get(idNum, {})
            typeNum = data.get('cdgroup', idNum)
            if idNum in logicInfo.cooldownItem:
                end, total = logicInfo.cooldownItem[idNum]
                remain = end - BigWorld.time()
            if typeNum in logicInfo.commonCooldownItem:
                cend, ctotal = logicInfo.commonCooldownItem[typeNum]
                cremain = cend - BigWorld.time()
                if cremain > remain:
                    remain = cremain
                    total = ctotal
            if remain > 0:
                bindingSlot = gameglobal.rds.ui.inventory.binding.get(slot, None)
                if bindingSlot != None:
                    bindingSlot[0].Invoke('playCooldown', (GfxValue(total * 1000), GfxValue((total - remain) * 1000)))
                    if self.callbackHandler.get(slot, None):
                        BigWorld.cancelCallback(self.callbackHandler[slot])
                    self.callbackHandler[slot] = BigWorld.callback(remain, Functor(self.afterItemEndCooldown, bindingSlot[0]))

    def updateCrossServerItemCooldown(self):
        for page, slot, idNum in self.getCrossItemList():
            if page != 0 or id == None:
                continue
            total = end = remain = 0
            data = ID.data.get(idNum, {})
            typeNum = data.get('cdgroup', idNum)
            if idNum in logicInfo.cooldownItem:
                end, total = logicInfo.cooldownItem[idNum]
                remain = end - BigWorld.time()
            if typeNum in logicInfo.commonCooldownItem:
                cend, ctotal = logicInfo.commonCooldownItem[typeNum]
                cremain = cend - BigWorld.time()
                if cremain > remain:
                    remain = cremain
                    total = ctotal
            if remain > 0:
                bindingSlot = gameglobal.rds.ui.crossServerBag.binding.get(slot, None)
                if bindingSlot != None:
                    bindingSlot[0].Invoke('playCooldown', (GfxValue(total * 1000), GfxValue((total - remain) * 1000)))
                    if self.callbackHandler.get(slot, None):
                        BigWorld.cancelCallback(self.callbackHandler[slot])
                    self.callbackHandler[slot] = BigWorld.callback(remain, Functor(self.afterItemEndCooldown, bindingSlot[0]))

    def playCooldown(self, page, pos, itemId, isAction = True, isStorage = False, isCrossBag = False):
        total = end = remain = 0
        data = ID.data.get(itemId, {})
        typeNum = data.get('cdgroup', itemId)
        if itemId == None:
            return
        else:
            if itemId in logicInfo.cooldownItem:
                end, total = logicInfo.cooldownItem[itemId]
                remain = end - BigWorld.time()
            if typeNum in logicInfo.commonCooldownItem:
                cend, ctotal = logicInfo.commonCooldownItem[typeNum]
                cremain = cend - BigWorld.time()
                if cremain > remain:
                    remain = cremain
                    total = ctotal
            if isAction:
                info = self.getShortCut(page, pos, (0, 0))
                if info[0] == uiConst.SHORTCUT_TYPE_ITEM_EQUIP and info[1] == itemId and len(info) > 2:
                    remain, total = self.checkEquipSkillCoolDown(itemId, info[2])
            if remain > 0:
                if isAction:
                    key = self._getKey(page, pos)
                    if self.binding.has_key(key):
                        bindingSlot = self.binding[key]
                        bindingSlot[0].Invoke('setShowNumber', GfxValue(True))
                    else:
                        bindingSlot = None
                elif isStorage:
                    key = gameglobal.rds.ui.storage._getKey(page, pos)
                    bindingSlot = gameglobal.rds.ui.storage.binding.get(key, None)
                elif isCrossBag:
                    key = gameglobal.rds.ui.crossServerBag._getKey(page, pos)
                    bindingSlot = gameglobal.rds.ui.crossServerBag.binding.get(key, None)
                else:
                    key = gameglobal.rds.ui.inventory._getKey(page, pos)
                    bindingSlot = gameglobal.rds.ui.inventory.binding.get(key, None)
                if bindingSlot:
                    bindingSlot[0].Invoke('playCooldown', (GfxValue(total * 1000), GfxValue((total - remain) * 1000)))
                    if self.callbackHandler.get(key, None):
                        BigWorld.cancelCallback(self.callbackHandler[key])
                    self.callbackHandler[key] = BigWorld.callback(remain, Functor(self.afterItemEndCooldown, bindingSlot[0]))
            return

    def stopCoolDown(self, page, pos, isAction = True, isStorage = False, isCross = False):
        if isAction:
            key = self._getKey(page, pos)
            if not self.binding.has_key(key):
                return
            bindingSlot = self.binding[key]
        elif isStorage:
            key = gameglobal.rds.ui.storage._getKey(page, pos)
            bindingSlot = gameglobal.rds.ui.storage.binding.get(key, None)
        elif isCross:
            key = gameglobal.rds.ui.crossServerBag._getKey(page, pos)
            bindingSlot = gameglobal.rds.ui.crossServerBag.binding.get(key, None)
        else:
            key = gameglobal.rds.ui.inventory._getKey(page, pos)
            bindingSlot = gameglobal.rds.ui.inventory.binding.get(key, None)
        if self.callbackHandler.get(key, None):
            BigWorld.cancelCallback(self.callbackHandler[key])
        if bindingSlot and bindingSlot[0] != None:
            bindingSlot[0].Invoke('stopCooldown')

    def stopCoolDownonSwitch(self, value, bar, slotId):
        if gameglobal.rds.configData.get('enableOneKeyConfig', False):
            value[0].Invoke('stopCooldown')
            keyboardEffect.removeSlotCDEffect(bar, slotId)

    @ui.callAfterTime()
    def updateSlots(self):
        endGcd = logicInfo.commonCooldownWeaponSkill[0]
        totalGcd = logicInfo.commonCooldownWeaponSkill[1]
        remainGcd = endGcd - BigWorld.time()
        p = BigWorld.player()
        isOnZaijuOrBianyao = p._isOnZaijuOrBianyao()
        if isOnZaijuOrBianyao:
            if gameglobal.rds.ui.zaijuV2.widget:
                items = gameglobal.rds.ui.zaijuV2.binding.items()
            else:
                items = gameglobal.rds.ui.zaiju.binding.items()
        else:
            items = self.binding.items()
        if gameglobal.rds.ui.skill.inAirBattleState():
            items.extend(gameglobal.rds.ui.airbar.binding.items())
        needRefreshWS = False
        for i, v in items:
            total = end = remain = 0
            if isOnZaijuOrBianyao:
                if gameglobal.rds.ui.zaiju.mediator or gameglobal.rds.ui.vehicleSkill.widget:
                    bar, slotId = gameglobal.rds.ui.zaiju.getSlotID(i)
                    idNum, _ = gameglobal.rds.ui.zaiju.getSkillInfo(slotId)
                elif gameglobal.rds.ui.zaijuV2.widget:
                    bar, slotId = gameglobal.rds.ui.zaijuV2.getSlotID(i)
                    if slotId == 0 and self.uiAdapter.zaijuV2.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
                        self.stopCoolDownonSwitch(v, bar, slotId)
                        continue
                    idNum, _ = gameglobal.rds.ui.zaijuV2.skills[slotId]
            else:
                if i.startswith('actionbar'):
                    bar, slotId = self.getSlotID(i)
                    idNum = self.getActionIDByPos(bar, slotId)
                elif i.startswith('airbar'):
                    bar, slotId = gameglobal.rds.ui.airbar.getSlotID(i)
                    idNum = gameglobal.rds.ui.airbar.getSkillIdByPos(bar, slotId)
                if p.skillQteData.has_key(idNum):
                    idNum = p.skillQteData[idNum].qteSkills[0]
            if (idNum is None or idNum == 0) and not isOnZaijuOrBianyao:
                info = self.getShortCut(bar, slotId)
                if info:
                    idNum = info[1]
            if idNum is None or idNum == 0:
                v[0].Invoke('stopCooldown')
                if self.callbackHandler.get(i, None):
                    BigWorld.cancelCallback(self.callbackHandler[i])
                self.stopCoolDownonSwitch(v, bar, slotId)
                continue
            if (bar == uiConst.ITEM_ACTION_BAR or bar == uiConst.ITEM_ACTION_BAR2) and gameglobal.rds.ui.trade.isShow:
                self.enableItemBar(False)
                self.stopCoolDownonSwitch(v, bar, slotId)
                continue
            info = self.getShortCut(bar, slotId)
            if (bar == uiConst.ITEM_ACTION_BAR or bar == uiConst.ITEM_ACTION_BAR2) and info[0] in (uiConst.SHORTCUT_TYPE_ITEM_COMSUME, uiConst.SHORTCUT_TYPE_LIEF_SKILL):
                self.stopCoolDownonSwitch(v, bar, slotId)
                continue
            if not isOnZaijuOrBianyao and info and len(info):
                if info[0] == uiConst.SHORTCUT_TYPE_SKILL_MACRO:
                    macroId = info[1]
                    macroInfo = p.getMacroInfoById(macroId)
                    if macroInfo and macroInfo.iconType == uiConst.MACRO_SKILL_ICON_TYPE:
                        skillCdIdDict = gameglobal.rds.ui.skillMacroOverview.getSkillCdIdDict()
                        idNum = skillCdIdDict[p.school].get(macroInfo.iconPath, 0)
            skillId = self.checkEquipSkillID(idNum)
            if skillId:
                idNum = skillId
            if idNum in logicInfo.cooldownSkill:
                end, total = logicInfo.cooldownSkill[idNum]
                if total == 0:
                    self.stopCoolDownonSwitch(v, bar, slotId)
                    continue
                remain = end - BigWorld.time()
                if remain < remainGcd:
                    remain = remainGcd
                    total = totalGcd
                v[0].Invoke('setShowNumber', GfxValue(True))
            elif idNum in logicInfo.cooldownGuildMemberSkill:
                end, total = logicInfo.cooldownGuildMemberSkill[idNum]
                remain = end - BigWorld.time()
                v[0].Invoke('setShowNumber', GfxValue(True))
            elif idNum in logicInfo.cooldownWWArmySkill:
                end, total = logicInfo.cooldownWWArmySkill[idNum]
                remain = end - BigWorld.time()
                v[0].Invoke('setShowNumber', GfxValue(True))
            elif idNum in logicInfo.cooldownClanWarSkill:
                end, total = logicInfo.cooldownClanWarSkill[idNum]
                remain = end - BigWorld.time()
                v[0].Invoke('setShowNumber', GfxValue(True))
            elif idNum in p.triggerPSkills:
                remain = p.triggerPSkills[idNum].nextTriggerTime - utils.getNow()
                total = PSD.data.get((idNum, p.triggerPSkills[idNum].level), {}).get('triggerCD', 0)
                v[0].Invoke('setShowNumber', GfxValue(True))
            elif p.intimacySkills.has_key(idNum):
                remain = p.intimacySkills[idNum].nextTime - utils.getNow()
                currentLevel = gameglobal.rds.ui.skill.getIntimacyCurrentLevel(idNum)
                total = ISD.data.get((idNum, currentLevel), {}).get('intimacySkillCD', 0)
                v[0].Invoke('setShowNumber', GfxValue(True))
            elif idNum == uiConst.INTIMACY_SKILL_MARRIAGE:
                total, remain = p.getMarriageSkillCd()
                v[0].Invoke('setShowNumber', GfxValue(True))
            elif idNum == uiConst.LING_SHI_FLAG_SWITCH:
                v[0].Invoke('setShowNumber', GfxValue(True))
            else:
                remain = remainGcd
                total = totalGcd
                v[0].Invoke('setShowNumber', GfxValue(False))
            if not p._isOnZaijuOrBianyao():
                info = self.getShortCut(bar, slotId, (0, 0))
                if info and len(info) > 2:
                    remain, total = self.checkEquipSkillCoolDown(info[1], info[2])
            bfyZaijuNo = SCD.data.get('bfyZaijuNo', ())
            if p.mapID == const.FB_NO_SPRING_ACTIVITY and isOnZaijuOrBianyao and p._getZaijuOrBianyaoNo() in bfyZaijuNo:
                cins = chickenFoodFactory.getInstance()
                isLight, canUse, _type, _remain, _total = cins.getSkillState(idNum)
                if canUse:
                    remain, total = _remain, _total
                else:
                    remain, total = (0, 0)
                v[0].Invoke('setLight', GfxValue(isLight))
                v[0].Invoke('setEnabled', GfxValue(canUse))
            if self.callbackHandler.get(i, None):
                BigWorld.cancelCallback(self.callbackHandler[i])
            if remain > 0:
                v[0].Invoke('playCooldown', (GfxValue(total * 1000), GfxValue((total - remain) * 1000)))
                self.callbackHandler[i] = BigWorld.callback(remain, Functor(self.afterSkillEndCooldown, v[0], idNum, bar, slotId))
                if idNum in p.wsSkills.keys():
                    needRefreshWS = True
                if remain >= totalGcd or not logicInfo.isInSkillCommonTime():
                    keyboardEffect.addSlotCDEffect(bar, slotId)
            else:
                if idNum in p.wsSkills.keys():
                    needRefreshWS = True
                v[0].Invoke('stopCooldown')
                keyboardEffect.removeSlotCDEffect(bar, slotId)

        if needRefreshWS:
            self.showWuShuangAnimation()
        self.updateItemSlot()
        self.updateEmoteItemCooldown()

    def cancelAllCallback(self):
        p = BigWorld.player()
        isOnZaijuOrBianyao = p._isOnZaijuOrBianyao()
        items = None
        if isOnZaijuOrBianyao:
            if gameglobal.rds.ui.zaiju.mediator or gameglobal.rds.ui.vehicleSkill.widget:
                items = gameglobal.rds.ui.zaiju.binding.items()
            else:
                items = gameglobal.rds.ui.zaijuV2.binding.items()
        elif gameglobal.rds.ui.skill.inAirBattleState():
            items = gameglobal.rds.ui.airbar.binding.items()
        else:
            items = self.binding.items()
        if not items:
            return
        else:
            for i, v in items:
                if not self.callbackHandler.has_key(i):
                    continue
                BigWorld.cancelCallback(self.callbackHandler[i])

            return

    def updateSlot(self, idNum):
        if idNum is None:
            return
        else:
            p = BigWorld.player()
            if idNum in logicInfo.cooldownSkill:
                end, total = logicInfo.cooldownSkill[idNum]
                if total == 0:
                    return
                remain = end - BigWorld.time()
            elif idNum in logicInfo.cooldownGuildMemberSkill:
                end, total = logicInfo.cooldownGuildMemberSkill[idNum]
                remain = end - BigWorld.time()
            elif idNum in logicInfo.cooldownWWArmySkill:
                end, total = logicInfo.cooldownWWArmySkill[idNum]
                remain = end - BigWorld.time()
            elif idNum in logicInfo.cooldownClanWarSkill:
                end, total = logicInfo.cooldownClanWarSkill[idNum]
                remain = end - BigWorld.time()
            elif idNum in p.triggerPSkills:
                remain = p.triggerPSkills[idNum].nextTriggerTime - utils.getNow()
                total = PSD.data.get((idNum, p.triggerPSkills[idNum].level), {}).get('triggerCD', 0)
            elif idNum != BigWorld.player().skillId:
                end, total = logicInfo.commonCooldownWeaponSkill
                remain = end - BigWorld.time()
            elif p.intimacySkills.has_key(idNum):
                remain = p.intimacySkills[idNum].nextTime - utils.getNow()
                currentLevel = gameglobal.rds.ui.skill.getIntimacyCurrentLevel(idNum)
                total = ISD.data.get((idNum, currentLevel), {}).get('intimacySkillCD', 0)
            elif idNum == uiConst.INTIMACY_SKILL_MARRIAGE:
                total, remain = p.getMarriageSkillCd()
            v = None
            if gameglobal.rds.ui.zaijuV2.widget and p._isOnZaiju():
                v, i, bar, slotId = gameglobal.rds.ui.zaijuV2.getBinding(idNum)
                if slotId == 0 and self.uiAdapter.zaijuV2.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
                    return
                if not v:
                    return
            else:
                pos = self._getPosByActionID(idNum)
                if not pos:
                    return
                i = pos[0]
                if self.binding.has_key(i):
                    v = self.binding[i]
                else:
                    return
                bar, slotId = self.getSlotID(i)
            if not v:
                return
            if self.callbackHandler.get(i, None):
                BigWorld.cancelCallback(self.callbackHandler[i])
            if not p._isOnZaiju():
                info = self.getShortCut(bar, slotId, (0, 0))
                if info[0] == uiConst.SHORTCUT_TYPE_ITEM_EQUIP and len(info) > 2:
                    remain, total = self.checkEquipSkillCoolDown(info[1], info[2])
            if remain > 0:
                v[0].Invoke('playCooldown', (GfxValue(total * 1000), GfxValue((total - remain) * 1000)))
                self.callbackHandler[i] = BigWorld.callback(remain, Functor(self.afterSkillEndCooldown, v[0], idNum, bar, slotId))
            else:
                v[0].Invoke('stopCooldown')
            return

    def afterItemEndCooldown(self, slot):
        slot.Invoke('endCooldown')

    def afterSkillEndCooldown(self, slot, idNum, bar, slotId):
        p = BigWorld.player()
        if not p:
            return
        else:
            if idNum in p.wsSkills.keys():
                self.showWuShuangAnimation()
            slot.Invoke('endCooldown')
            if gameglobal.rds.bar == bar and gameglobal.rds.soltId == slotId:
                p.updateUseSkillKeyState()
            logicInfo.cooldownSkill.pop(idNum, None)
            logicInfo.cooldownGuildMemberSkill.pop(idNum, None)
            logicInfo.cooldownWWArmySkill.pop(idNum, None)
            logicInfo.cooldownClanWarSkill.pop(idNum, None)
            if idNum in logicInfo.cdStorageSkill.keys():
                nextTime, cdStorage = logicInfo.cdStorageSkill[idNum]
                skillInfo = SkillInfo(idNum, 1)
                if cdStorage < skillInfo.getSkillData('cdstorage', 0):
                    logicInfo.cdStorageSkill[idNum] = (nextTime, cdStorage + 1)
                gameglobal.rds.ui.zaijuV2.refreshCdStoreage(idNum)
                if cdStorage + 1 < skillInfo.getSkillData('cdstorage', 0):
                    t = BigWorld.time()
                    skillcd = skillDataInfo.getRecoverTime(skillInfo, 0)
                    logicInfo.cooldownSkill[idNum] = (skillcd + t, skillcd)
                    self.updateSlot(idNum)
            keyboardEffect.removeSlotCDEffect(bar, slotId)
            return

    def clearCooldown(self):
        logicInfo.clearCoolDown()
        for handler in self.callbackHandler.values():
            BigWorld.cancelCallback(handler)

        self.callbackHandler = {}
        self.updateSlots()

    def clearCooldownSkill(self, skillId, clearCommon = True):
        if clearCommon:
            logicInfo.cooldownWeaponSkill = {}
            logicInfo.commonCooldownWeaponSkill = (0, 0, None)
        if skillId in logicInfo.cooldownSkill:
            del logicInfo.cooldownSkill[skillId]
        self.updateSlots()

    def notifyCooldown(self, skillId, isCommon):
        if isCommon:
            for i, v in self.binding.items():
                v[0].Invoke('endCooldown')
                BigWorld.callback(5, Functor(self.notifyCooldown, skillId, False))

        else:
            for key in self._getPosByActionID(skillId):
                self.binding[key][0].Invoke('endCooldown')

    def _checkInSkillRange(self, skId):
        p = BigWorld.player()
        if not self._isTargetSkill(skId):
            return True
        else:
            tgt = p.targetLocked
            if tgt == None:
                return True
            skillInfo = self._getSkillInfo(skId)
            rangeMax = skillInfo.getSkillData('rangeMax', None)
            if rangeMax != None:
                rangeMax += p.targetLocked.getBodySize()
                rangeMax = round(rangeMax, 2)
            rangeMin = skillInfo.getSkillData('rangeMin', 0)
            if rangeMin != 0:
                rangeMin += p.targetLocked.getBodySize()
                rangeMin = round(rangeMin, 2)
            rangeMax = max(rangeMin, ((rangeMax if rangeMax else 0) + p.skillAdd[2]) * (1 + p.skillAdd[3]))
            dist = p.position.distTo(tgt.position)
            if rangeMax != None:
                if dist > rangeMax:
                    return False
            if rangeMin != 0:
                if dist < rangeMin:
                    return False
            return True

    def updateItemActionBar(self):
        p = BigWorld.player()
        for key, value in self.getOtherShortCut().items():
            if key[0] in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
                if value[1] in tuple(self.otherSkill.keys()) + tuple(self.lifeSkill):
                    self._setItemSlotState(key[0], key[1], uiConst.SKILL_ICON_STAT_USEABLE)
                else:
                    item = Item(value[1], 1, False)
                    if value[0] in uiConst.SHORTCUT_TYPE_ITEM and not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                        self._setItemSlotState(key[0], key[1], uiConst.SKILL_ICON_STAT_RED)
                    else:
                        self._setItemSlotState(key[0], key[1], uiConst.SKILL_ICON_STAT_USEABLE)

    def getItemList(self):
        itemList = []
        p = BigWorld.player()
        for i, j, _ in p.inv.xItems():
            itemList.append((i, gameglobal.rds.ui.inventory._getKey(i, j), p.inv.getQuickVal(i, j).id))

        return itemList

    def getCrossItemList(self):
        itemList = []
        p = BigWorld.player()
        for i, j, _ in p.crossInv.xItems():
            itemList.append((i, gameglobal.rds.ui.crossServerBag._getKey(i, j), p.crossInv.getQuickVal(i, j).id))

        return itemList

    def removeItemBySkillIdList(self, skillIdList, isRefresh = True):
        for sid in skillIdList:
            self.removeItemBySkillId(sid)

        if not isRefresh:
            BigWorld.player().saveShortcut(self.clientShortCut)

    def removeItemBySkillId(self, skillId, isRefresh = True):
        for pos in xrange(uiConst.MAX_ACTIONBAR_SLOT_NUM):
            info = self.getShortCut(uiConst.SKILL_ACTION_BAR, pos, [0, 0])
            if skillId == info[1]:
                self.removeItem(uiConst.SKILL_ACTION_BAR, pos)

        for pos in xrange(uiConst.MAX_ACTIONBAR_SLOT_NUM * 2):
            for page in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
                info = self.getShortCut(page, pos, [0, 0])
                if skillId == info[1]:
                    self.removeItem(page, pos)

        if not isRefresh:
            BigWorld.player().saveShortcut(self.clientShortCut)

    def removeItemByMacroId(self, macroId, isRefresh = True):
        for pos in xrange(uiConst.MAX_ACTIONBAR_SLOT_NUM):
            info = self.getShortCut(uiConst.SKILL_ACTION_BAR, pos, [0, 0])
            if macroId == info[1]:
                self.removeItem(uiConst.SKILL_ACTION_BAR, pos)

        for pos in xrange(uiConst.MAX_ACTIONBAR_SLOT_NUM * 2):
            for page in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
                info = self.getShortCut(page, pos, [0, 0])
                if macroId == info[1]:
                    self.removeItem(page, pos)

        if not isRefresh:
            BigWorld.player().saveShortcut(self.clientShortCut)

    def modifyItemByMacroId(self, macroId, isRefresh = True):
        for pos in xrange(uiConst.MAX_ACTIONBAR_SLOT_NUM):
            info = self.getShortCut(uiConst.SKILL_ACTION_BAR, pos, [0, 0])
            if macroId == info[1]:
                self.setItem(macroId, uiConst.SKILL_ACTION_BAR, pos, False, False, uiConst.SHORTCUT_TYPE_SKILL_MACRO)

        for pos in xrange(uiConst.MAX_ACTIONBAR_SLOT_NUM * 2):
            for page in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
                info = self.getShortCut(page, pos, [0, 0])
                if macroId == info[1]:
                    self.setItem(macroId, page, pos, False, False, uiConst.SHORTCUT_TYPE_SKILL_MACRO)

        if not isRefresh:
            BigWorld.player().saveShortcut(self.clientShortCut)

    def removeItem(self, page, pos, isRefresh = True):
        key = self._getKey(page, pos)
        if self.binding.get(key, None) is not None:
            if page != uiConst.SKILL_ACTION_BAR or not BigWorld.player().inCombat:
                data = GfxValue(1)
                data.SetNull()
                self.binding[key][1].InvokeSelf(data)
            if page == uiConst.EQUIP_ACTION_BAR:
                gameglobal.rds.ui.roleInfo.setSlotState(pos, uiConst.ITEM_NORMAL)
            elif page in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
                self.clearShineState(page, pos)
                self._setItemSlotState(page, pos, uiConst.SKILL_ICON_STAT_USEABLE)
                self.stopCoolDown(page, pos)
                self.binding[key][0].Invoke('showToggleShine', GfxValue(False))
                self.validateSlotVisible()
                self.setShortCut(page, pos, (uiConst.SHORTCUT_TYPE_NONE, 0))
                self.setSlotColor(page, pos, 'nothing')
            elif page == uiConst.SKILL_ACTION_BAR:
                self.clearShineState(page, pos)
                self._setSlotState(pos, uiConst.SKILL_ICON_STAT_USEABLE)
                self.stopCoolDown(page, pos)
                data = GfxValue(1)
                data.SetNull()
                self.binding[key][1].InvokeSelf(data)
                if pos >= uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                    self.wsMc.Invoke('setSlotStar', (GfxValue(pos), GfxValue(0)))
                self.notifyWuShuangCannotUse(pos)
                self.setShortCut(uiConst.SKILL_ACTION_BAR, pos, (uiConst.SHORTCUT_TYPE_NONE, 0))
                self.setSlotColor(page, pos, 'nothing')
            if not isRefresh:
                BigWorld.player().saveShortcut(self.clientShortCut)

    def formatStr(self, font, color, strType, fStr, unit = '', isNewLine = True):
        fStr = str(fStr)
        if fStr == '' or fStr == '0' or fStr == '0.0' or fStr.find('None') >= 0:
            return ''
        elif isNewLine:
            return "<font size = \'%s\' color = \'%s\'>%s</font><br>" % (font, color, strType + fStr + unit)
        else:
            return "<font size = \'%s\' color = \'%s\'>%s</font>" % (font, color, strType + fStr + unit)

    def _getWSType(self, ws1, ws2):
        p = BigWorld.player()
        try:
            if ws1 > 0:
                return SPD.data.get(p.realSchool, {}).get('wsType1', '')
            if ws2 > 0:
                return SPD.data.get(p.realSchool, {}).get('wsType2', '')
            return ''
        except:
            (gameStrings.TEXT_ACTIONBARPROXY_1550, ws1, ws2)

    def isWsType(self, skillInfo):
        self.WsNeed = skillDataInfo.getWsNeed(skillInfo)
        return self.WsNeed[0] or self.WsNeed[1]

    def getGraphVal(self, graph):
        ret = self.movie.CreateArray()
        gamelog.debug('getGraphVal', graph)
        ret.SetElement(0, GfxValue(gbk2unicode(graph[0])))
        ret.SetElement(1, GfxValue('f' + str(graph[1])))
        ret.SetElement(2, GfxValue(gbk2unicode(graph[2])))
        return ret

    def formatToolTip(self, skillId, sLv = 0, noGems = False, option = 0):
        p = BigWorld.player()
        fixLv = 0
        if sLv != 0:
            fixLv = p.getSkillInfo(skillId, sLv).hijackData.get('skillCalcLvAdd', 0)
            skillInfo = SkillInfo(skillId, min(sLv + fixLv, const.MAX_SKILL_LEVEL))
            skillTipsInfo = p.getSkillTipsInfo(skillId, min(sLv + fixLv, const.MAX_SKILL_LEVEL))
        else:
            sVal = p.getSkills().get(skillId, None)
            fixLv = p.getSkillInfo(skillId, sVal.level).hijackData.get('skillCalcLvAdd', 0) if sVal else 0
            skillInfo = SkillInfo(skillId, min((sVal.level if sVal and sVal.level != 0 else 1) + fixLv, const.MAX_SKILL_LEVEL))
            skillTipsInfo = p.getSkillTipsInfo(skillId, min((sVal.level if sVal and sVal.level != 0 else 1) + fixLv, const.MAX_SKILL_LEVEL))
        skillName = skillDataInfo.getSkillName(skillInfo)
        wsAdd1, wsAdd2 = skillDataInfo.getWuShuang(skillInfo)
        mwsAdd = int(skillDataInfo.getWuShuangMwsAdd(skillInfo) / 100)
        wsNeed1, wsNeed2 = skillDataInfo.getWsNeed(skillInfo)
        wsNeed = '-' + str(int(math.floor(wsNeed1 / 100.0)) if wsNeed1 > 0 else int(math.floor(wsNeed2 / 100.0)))
        wsType = gameglobal.rds.ui.skill._getWSType(wsNeed1, wsNeed2, skillInfo.getSkillData('school', None))
        if wsType == '':
            wsType = gameglobal.rds.ui.skill._getWSType(wsAdd1, wsAdd2, skillInfo.getSkillData('school', None))
            wsNeed = '+' + str(wsAdd1 / 100.0 if wsAdd1 > 0 else wsAdd2 / 100.0)
        wsType = wsType
        skillLv = skillDataInfo.getSkillLv(skillInfo)
        sd = skillDataInfo.ClientSkillInfo(skillId, skillLv)
        if hasattr(p, 'skillAppearancesDetail'):
            appearanceId = p.skillAppearancesDetail.getCurrentAppearance(skillId)
            if appearanceId and appearanceId > 0:
                sd = skillDataInfo.AppearanceSkillInfo(skillId, appearanceId)
        if option:
            shortCutWithParamIcon = SGTD.data.get(skillId, {}).get('shortCutWithParamIcon', ())
            offset = option % uiConst.SKILL_SHORT_CUT_BASE
            if offset < len(shortCutWithParamIcon):
                icon = shortCutWithParamIcon[offset]
            else:
                icon = 0
        else:
            icon = sd.getSkillData('icon', None)
        schoolInfo = self._createSchoolInfo()
        if schoolInfo.get('swithIcon', None):
            iconPath = self._getSwithIcon(skillId, skillLv, True)
        else:
            iconPath = 'skill/icon64/' + str(icon) + '.dds'
        skillType = self._getSkillType(skillDataInfo.getSkillType(skillInfo))
        skillCastType = self._getCastType(skillInfo, skillDataInfo.getCastType(skillInfo))
        mpNeed = skillDataInfo.getSkillMpNeed(skillInfo)
        hpNeed = skillDataInfo.getSkillHpNeed(skillInfo)
        learnLv = skillDataInfo.getLearnLv(skillInfo)
        if mpNeed > 0:
            castNeed = mpNeed
        elif hpNeed > 0:
            castNeed = hpNeed
        else:
            castNeed = 0
        if castNeed == 0:
            castNeed = ''
        guideMpNeed = skillDataInfo.getGuideMpNeed(skillInfo)
        guideHpNeed = skillDataInfo.getGuideHpNeed(skillInfo)
        guideNeed = 0
        if guideMpNeed > 0:
            guideNeed = guideMpNeed
        elif hpNeed > 0:
            guideNeed = guideHpNeed
        if guideNeed == 0:
            guideNeed = ''
        if option:
            offset = option % uiConst.SKILL_SHORT_CUT_BASE
            mainEff = skillTipsInfo.getSkillData('shortMainEff', '')
            detailEff1 = skillTipsInfo.getSkillData('shortDetailEff1', '')
            detailEff2 = skillTipsInfo.getSkillData('shortDetailEff2', '')
            detailEff3 = skillTipsInfo.getSkillData('shortDetailEff2', '')
        else:
            mainEff = skillTipsInfo.getSkillData('mainEff', '')
            detailEff1 = skillTipsInfo.getSkillData('detailEff1', '')
            detailEff2 = skillTipsInfo.getSkillData('detailEff2', '')
            detailEff3 = skillTipsInfo.getSkillData('detailEff3', '')
        detailArr = []
        if mainEff:
            mainEff = uiUtils.calSkillTipValue(mainEff, skillLv)
        if detailEff1:
            detailArr.append(uiUtils.calSkillTipValue(detailEff1, skillLv))
        if detailEff2:
            detailArr.append(uiUtils.calSkillTipValue(detailEff2, skillLv))
        if detailEff3:
            detailArr.append(uiUtils.calSkillTipValue(detailEff3, skillLv))
        graph1 = skillDataInfo.getGraph1(skillInfo)
        graph2 = skillDataInfo.getGraph2(skillInfo)
        graph3 = skillDataInfo.getGraph3(skillInfo)
        graph4 = skillDataInfo.getGraph4(skillInfo)
        graphArr = []
        if graph1:
            graphArr.append(gameglobal.rds.ui.skill.getGraphVal(graph1))
        if graph2:
            graphArr.append(gameglobal.rds.ui.skill.getGraphVal(graph2))
        if graph3:
            graphArr.append(gameglobal.rds.ui.skill.getGraphVal(graph3))
        if graph4:
            graphArr.append(gameglobal.rds.ui.skill.getGraphVal(graph4))
        daoHang = []
        gems = []
        fireCnt = 0
        windCnt = 0
        hillCnt = 0
        forestCnt = 0
        if noGems:
            gems.extend([6] * 10)
        else:
            gemTypeMap = {gametypes.WUSHUANG_GEM_TYPE_WIND: 2,
             gametypes.WUSHUANG_GEM_TYPE_WOOD: 3,
             gametypes.WUSHUANG_GEM_TYPE_FIRE: 4,
             gametypes.WUSHUANG_GEM_TYPE_MOUNTAIN: 5}
            skVal = p.wsSkills.get(skillId, None)
            if skVal:
                for slot in skVal.slots:
                    if slot[1] == True:
                        if slot[2] == gametypes.WUSHUANG_GEM_TYPE_WIND:
                            windCnt += 1
                        elif slot[2] == gametypes.WUSHUANG_GEM_TYPE_WOOD:
                            forestCnt += 1
                        elif slot[2] == gametypes.WUSHUANG_GEM_TYPE_FIRE:
                            fireCnt += 1
                        elif slot[2] == gametypes.WUSHUANG_GEM_TYPE_MOUNTAIN:
                            hillCnt += 1
                        gems.append(gemTypeMap[slot[2]])
                    else:
                        gems.append(0)

            gems.extend([6] * (10 - len(gems)))
        for idx, item in enumerate(gems):
            daoHang.append(item)

        wsData = WSCD.data.get(skillId, {})
        daoHangDesc = []
        if windCnt != 0:
            id = wsData.get('windPSkill', [(0, 0)] * 5)[windCnt - 1]
            skillId = PD.data.get(id, {}).get('skillId')
            pskillVal = BigWorld.player().pskills.get(id[0], {}).get(skillId, None)
            pData = pskillVal.pData if pskillVal else {}
            desc = gameglobal.rds.ui.runeView.generateDesc(id[0], PSkillInfo(id[0], id[1], pData), id[1])
            daoHangDesc.append('wind:%s' % desc)
        if forestCnt != 0:
            id = wsData.get('woodPSkill', [(0, 0)] * 5)[forestCnt - 1]
            skillId = PD.data.get(id, {}).get('skillId')
            pskillVal = BigWorld.player().pskills.get(id[0], {}).get(skillId, None)
            pData = pskillVal.pData if pskillVal else {}
            desc = gameglobal.rds.ui.runeView.generateDesc(id[0], PSkillInfo(id[0], id[1], pData), id[1])
            daoHangDesc.append('wood:%s' % desc)
        if fireCnt != 0:
            id = wsData.get('firePSkill', [(0, 0)] * 5)[fireCnt - 1]
            skillId = PD.data.get(id, {}).get('skillId')
            pskillVal = BigWorld.player().pskills.get(id[0], {}).get(skillId, None)
            pData = pskillVal.pData if pskillVal else {}
            desc = gameglobal.rds.ui.runeView.generateDesc(id[0], PSkillInfo(id[0], id[1], pData), id[1])
            daoHangDesc.append('fire:%s' % desc)
        if hillCnt != 0:
            id = wsData.get('mountainPSkill', [(0, 0)] * 5)[hillCnt - 1]
            skillId = PD.data.get(id, {}).get('skillId')
            pskillVal = BigWorld.player().pskills.get(id[0], {}).get(skillId, None)
            pData = pskillVal.pData if pskillVal else {}
            desc = gameglobal.rds.ui.runeView.generateDesc(id[0], PSkillInfo(id[0], id[1], pData), id[1])
            daoHangDesc.append('hill:%s' % desc)
        shortMainEff = skillTipsInfo.getSkillData('shortMainEff', mainEff)
        if shortMainEff:
            shortMainEff = uiUtils.calSkillTipValue(shortMainEff, skillLv)
        shortDetailEff1 = skillTipsInfo.getSkillData('shortDetailEff1', '')
        shortDetailEff2 = skillTipsInfo.getSkillData('shortDetailEff2', '')
        shortDetailEff3 = skillTipsInfo.getSkillData('shortDetailEff3', '')
        shortDetailArr = []
        if shortDetailEff1:
            shortDetailArr.append(uiUtils.calSkillTipValue(shortDetailEff1, skillLv))
        if shortDetailEff2:
            shortDetailArr.append(uiUtils.calSkillTipValue(shortDetailEff2, skillLv))
        if shortDetailEff3:
            shortDetailArr.append(uiUtils.calSkillTipValue(shortDetailEff3, skillLv))
        stateIcon1 = skillInfo.getSkillData('stateIcon1', '')
        stateType1 = STD.data.get(stateIcon1, {}).get('iconShowType', 1)
        stateIcon2 = skillInfo.getSkillData('stateIcon2', '')
        stateType2 = STD.data.get(stateIcon2, {}).get('iconShowType', 1)
        stateIcon3 = skillInfo.getSkillData('stateIcon3', '')
        stateType3 = STD.data.get(stateIcon3, {}).get('iconShowType', 1)
        stateIconArr = []
        if stateIcon1:
            stateIconArr.append(['state/40/%s.dds' % STD.data.get(stateIcon1, {}).get('iconId', 0), stateType1])
        if stateIcon2:
            stateIconArr.append(['state/40/%s.dds' % STD.data.get(stateIcon2, {}).get('iconId', 0), stateType2])
        if stateIcon3:
            stateIconArr.append(['state/40/%s.dds' % STD.data.get(stateIcon3, {}).get('iconId', 0), stateType3])
        stateDesc1 = skillTipsInfo.getSkillData('stateDesc1', '')
        stateDesc2 = skillTipsInfo.getSkillData('stateDesc2', '')
        stateDesc3 = skillTipsInfo.getSkillData('stateDesc3', '')
        stateDescArr = []
        if stateDesc1:
            stateDescArr.append(uiUtils.calSkillTipValue(stateDesc1, skillLv))
        if stateDesc2:
            stateDescArr.append(uiUtils.calSkillTipValue(stateDesc2, skillLv))
        if stateDesc3:
            stateDescArr.append(uiUtils.calSkillTipValue(stateDesc3, skillLv))
        shortStateDesc1 = skillTipsInfo.getSkillData('shortStateDesc1', '')
        shortStateDesc2 = skillTipsInfo.getSkillData('shortStateDesc2', '')
        shortStateDesc3 = skillTipsInfo.getSkillData('shortStateDesc3', '')
        shortStateDescArr = []
        if shortStateDesc1:
            shortStateDescArr.append(uiUtils.calSkillTipValue(shortStateDesc1, skillLv))
        if shortStateDesc2:
            shortStateDescArr.append(uiUtils.calSkillTipValue(shortStateDesc2, skillLv))
        if shortStateDesc3:
            shortStateDescArr.append(uiUtils.calSkillTipValue(shortStateDesc3, skillLv))
        if fixLv:
            if sLv != 0:
                if sLv + fixLv > const.MAX_SKILL_LEVEL:
                    skillLvDesc = str(sLv) + "<font color=\'#7FFF95\'>+" + str(const.MAX_SKILL_LEVEL - sLv) + '</font>'
                else:
                    skillLvDesc = str(sLv) + "<font color=\'#7FFF95\'>+" + str(fixLv) + '</font>'
            else:
                sVal = p.getSkills().get(skillId, None)
                sklLv = sVal.level if sVal and sVal.level != 0 else 1
                if sklLv + fixLv > const.MAX_SKILL_LEVEL:
                    skillLvDesc = str(sklLv) + "<font color=\'#7FFF95\'>+" + str(const.MAX_SKILL_LEVEL - sklLv) + '</font>'
                else:
                    skillLvDesc = str(sklLv) + "<font color=\'#7FFF95\'>+" + str(fixLv) + '</font>'
        else:
            skillLvDesc = skillLv
        showLv = False
        if skillId in p.getSkills().keys():
            showLv = True
        if skillId in p.guildMemberSkills.keys():
            showLv = True
        levelUpCondition = ''
        worldViewDesc = SGTD.data.get(skillId, {}).get('worldViewDesc', '')
        ret = [skillName,
         wsType,
         wsNeed,
         skillLvDesc,
         iconPath,
         skillType,
         skillCastType,
         castNeed,
         guideNeed,
         mainEff,
         detailArr,
         graphArr,
         daoHang,
         daoHangDesc,
         learnLv,
         showLv,
         shortMainEff,
         shortDetailArr,
         stateIconArr,
         stateDescArr,
         shortStateDescArr,
         mwsAdd,
         levelUpCondition,
         worldViewDesc]
        return uiUtils.array2GfxAarry(ret, True)

    def _getReqCondition(self, skillInfo):
        fStr = ''
        weapon = skillDataInfo.getWeaponTips(skillInfo)
        for item in weapon:
            if item[1]:
                fStr += self.formatStr('12', '#ffffff', gameStrings.TEXT_ACTIONBARPROXY_1823, item[0])
            else:
                fStr += self.formatStr('12', '#ff0000', gameStrings.TEXT_ACTIONBARPROXY_1823, item[0])

        selfBuffer = skillDataInfo.getSelfBufferName(skillInfo)
        for item in selfBuffer:
            if item[1]:
                fStr += self.formatStr('12', '#ffffff', gameStrings.TEXT_ACTIONBARPROXY_1823, item[0])
            else:
                fStr += self.formatStr('12', '#ff0000', gameStrings.TEXT_ACTIONBARPROXY_1823, item[0])

        return fStr

    def _getCastType(self, skillInfo, castType):
        if castType == uiConst.GUID_SKILL:
            return gameStrings.TEXT_ACTIONBARPROXY_1837
        elif castType == uiConst.ACCUMULATE_SKILL:
            return gameStrings.TEXT_ACTIONBARPROXY_1839
        elif skillDataInfo.getSpellTime(skillInfo) and skillDataInfo.getPreSpell(skillInfo) != 1:
            return gameStrings.TEXT_ACTIONBARPROXY_1841
        else:
            return gameStrings.TEXT_ACTIONBARPROXY_1843

    def _getDamageType(self, damageType):
        if damageType == uiConst.MAGIC_DAMAGE_SKILL:
            return gameStrings.TEXT_ACTIONBARPROXY_1847
        elif damageType == uiConst.PHYSICS_DAMAGE_SKILL:
            return gameStrings.TEXT_ACTIONBARPROXY_1849
        else:
            return gameStrings.TEXT_ACTIONBARPROXY_1851

    def _getSkillType(self, skillType):
        if skillType == 1:
            return gameStrings.TEXT_ACTIONBARPROXY_1855
        elif skillType == 2:
            return gameStrings.TEXT_ACTIONBARPROXY_1857
        elif skillType == 3:
            return gameStrings.TEXT_ACTIONBARPROXY_1859
        elif skillType == 4:
            return gameStrings.TEXT_ACTIONBARPROXY_1861
        else:
            return ''

    def _getFaction(self, wsAdd1, wsAdd2):
        pass

    def checkEquipmentByIdAndUuid(self, itemId, uuid):
        equipments = BigWorld.player().equipment
        for equipment in equipments:
            if equipment and equipment.id == itemId and equipment.uuid == uuid:
                return equipment

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, idNum = self.getSlotID(key)
        p = BigWorld.player()
        if bar == uiConst.EQUIP_ACTION_BAR:
            if idNum >= const.SUB_EQUIP_PART_OFFSET:
                i = commcalc.getAlternativeEquip(p, idNum - const.SUB_EQUIP_PART_OFFSET)
            else:
                i = p.equipment.get(idNum)
            if i != None:
                ret = gameglobal.rds.ui.inventory.GfxToolTip(i, const.ITEM_IN_EQUIPMENT)
                return ret
        elif bar in (uiConst.SKILL_ACTION_BAR, uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2):
            info = self.getShortCut(bar, idNum)
            if not info:
                return
            itemType = info[0]
            itemId = info[1]
            if itemId in self.otherSkill:
                return self.uiAdapter.skill.getOtherSkillTip(self.otherSkill.get(itemId, 0))
            if itemType == uiConst.SHORTCUT_TYPE_LIEF_SKILL and itemId in self.lifeSkill:
                if itemId == uiConst.LIFE_SKILL_FISHING:
                    return GfxValue(gbk2unicode(gameStrings.TEXT_ACTIONBARPROXY_1899))
                elif itemId == uiConst.LIFE_SKILL_EXPLORE:
                    return GfxValue(gbk2unicode(gameStrings.TEXT_ACTIONBARPROXY_1901))
                else:
                    curLifeSkillId = uiUtils.getCurLifeSkill(itemId)
                    if curLifeSkillId[0] is None:
                        return GfxValue('')
                    lifeSkillData = LSD.data.get(curLifeSkillId, {})
                    return GfxValue(gbk2unicode(lifeSkillData.get('name', '')))
            if itemType == uiConst.SHORTCUT_TYPE_EMOTE:
                tip = gameglobal.rds.ui.emoteAction.getTip(itemId)
                return GfxValue(gbk2unicode(tip))
            if itemType == uiConst.SHORTCUT_TYPE_SKILL and itemId in uiConst.INTIMACY_SKILL_ALL:
                tip = gameglobal.rds.ui.skill.getIntimacySkillTip(itemId)
                return tip
            if itemType == uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE:
                spriteIdx, spriteId = itemId
                return GfxValue(gbk2unicode(tipUtils.getSummonedSpriteTips(int(spriteId), int(spriteIdx))))
            if itemType == uiConst.SHORTCUT_TYPE_SKILL_MACRO:
                if not hasattr(p, 'mySkillMacroInfo'):
                    return GfxValue('')
                if not p.mySkillMacroInfo.get(itemId, None):
                    return GfxValue(gbk2unicode(gameStrings.SKILL_MACRO_NOT_EXIST))
                tip = "<font size = \'%d\'>%s</font>" % (gametypes.MACRO_TIP_SIZE, p.mySkillMacroInfo.get(itemId, None).name)
                return GfxValue(gbk2unicode(tip))
            if info and len(info) > 2:
                equipment = self.checkEquipmentByIdAndUuid(info[1], info[2])
                if equipment:
                    ret = gameglobal.rds.ui.inventory.GfxToolTip(equipment, const.ITEM_IN_EQUIPMENT)
                    return ret
            page, pos = BigWorld.player().realInv.findItemInPages(info[1], includeExpired=True, includeLatch=True, includeShihun=True)
            if page == const.CONT_NO_PAGE:
                if itemId != 0:
                    if info[0] == uiConst.SHORTCUT_TYPE_SKILL:
                        if GSD.data.has_key(itemId) and GSD.data.get(itemId, {}).get('clientSkill', 0):
                            itemId = GSD.data.get(itemId, {}).get('clientSkill', 0)
                        if p.skillQteData.has_key(itemId):
                            itemId = p.skillQteData[itemId].qteSkills[0]
                        BigWorld.player().playHoverEffect(itemId)
                        if len(info) == 3:
                            optionId = info[2]
                        else:
                            optionId = 0
                        sLv = 0
                        if itemId in p.guildMemberSkills.keys():
                            sLv = p.guildMemberSkills[itemId].level
                        tooltip = self.formatToolTip(itemId, sLv, False, optionId)
                        return tooltip
                    else:
                        i = Item(itemId, 1, False)
                        if CID.data.get(itemId, {}).get('sType', None):
                            i.cstype = CID.data.get(itemId, {}).get('sType', None)
                        ret = gameglobal.rds.ui.inventory.GfxToolTip(i)
                        return ret
                return
            i = BigWorld.player().realInv.getQuickVal(page, pos)
            ret = gameglobal.rds.ui.inventory.GfxToolTip(i)
            return ret

    def checkEquipment(self, itemId):
        equipments = BigWorld.player().equipment
        for equipment in equipments:
            if equipment and equipment.id == itemId:
                return equipment

    def onGetWSValue(self, *arg):
        ret = self.movie.CreateArray()
        p = BigWorld.player()
        ret.SetElement(0, GfxValue(int(math.floor(p.ws[0] / 100.0))))
        ret.SetElement(1, GfxValue(int(math.floor(p.ws[1] / 100.0))))
        ret.SetElement(2, GfxValue(int(math.floor(p.wushuang1.getMaxMws() / 100.0))))
        ret.SetElement(3, GfxValue(int(math.floor(p.wushuang2.getMaxMws() / 100.0))))
        return ret

    def onGetWSType(self, *arg):
        ret = self.movie.CreateArray()
        school = BigWorld.player().realSchool
        ret.SetElement(0, GfxValue(self.wsColorMap[school][0]))
        ret.SetElement(1, GfxValue(self.wsColorMap[school][1]))
        return ret

    def setWS(self, wsValue, maxValue):
        flag = True
        val1 = self.movie.CreateArray()
        i = 0
        for item in wsValue:
            val1.SetElement(i, GfxValue(int(math.floor(item / 100.0))))
            i += 1

        val2 = self.movie.CreateArray()
        i = 0
        for item in maxValue:
            val2.SetElement(i, GfxValue(int(math.floor(item / 100.0))))
            i += 1

        if self.mc != None:
            self.mc.Invoke('setWS', (val1, val2, GfxValue(flag)))
        if self.wsMc != None:
            self.wsMc.Invoke('setWS', (val1, val2, GfxValue(flag)))

    def horseRide(self):
        p = BigWorld.player()
        if p.tride.inRide() and not BigWorld.player().isOnRideTogetherHorse():
            p.cancelRideTogether()
            p.leaveRide()
            return
        isInHorse = p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
        if isInHorse:
            p.leaveRide()
        else:
            p.enterRide()

    def useItem(self, page, pos, isDown = False, isKeyMode = True):
        utils.recusionLog(9)
        p = BigWorld.player()
        if page == uiConst.SKILL_ACTION_BAR and isDown:
            if pos < uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                if self.mc:
                    self.mc.Invoke('slotShake', GfxValue(pos))
            elif self.wsMc:
                self.wsMc.Invoke('slotShake', GfxValue(pos))
        info = self.getShortCut(page, pos, (0, 0))
        if info:
            if info[1] in uiConst.TUTORIAL_COMMON_SKILL_TRIGGER:
                gameglobal.rds.tutorial.onUseCommonSkillEndCheck(info[1])
            if info[0] == uiConst.SHORTCUT_TYPE_EMOTE and not isDown:
                p.wantToDoEmote(info[1])
                return
            if info[0] == uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE and self.canUseItem(isDown, isKeyMode):
                spriteIdx, spriteId = info[1]
                p.onUseActionBarSpriteItem(int(spriteIdx), int(spriteId))
                return
            if info[0] == uiConst.SHORTCUT_TYPE_SKILL_MACRO:
                if isKeyMode and not isDown or not isKeyMode and isDown:
                    return
                if not hasattr(p, 'mySkillMacroInfo'):
                    return
                macroList = gameglobal.rds.ui.skillMacroOverview.getInforFromCommands(info[1])
                gameglobal.rds.ui.skillMacroOverview.executeCommandStart(macroList, isDown, isKeyMode)
                return
            if info[1] == uiConst.HORSE_RIDING and self.canUseItem(isDown, isKeyMode):
                self.horseRide()
                return
            if info[1] == uiConst.WING_FLYING and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.skill.enterWingFly()
                return
            if info[1] == uiConst.RENEWAL_ITEM and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.skill.setRenewalItem()
                return
            if info[1] == uiConst.DAZUOING and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.skill.enterDaZuo()
                return
            if info[1] == uiConst.BOOTH and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.skill.enterBooth()
            elif info[1] == uiConst.COUPLEEMOTE and self.canUseItem(isDown, isKeyMode):
                p.applyForCoupleEmote(1)
            elif info[1] == uiConst.EQUIP_FEED and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.equipFeed.show()
            elif info[1] == uiConst.RIDE_TOGETHER and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.skill.rideTogether()
            elif info[1] == uiConst.SHOW_BACK_WEAR and self.canUseItem(isDown, isKeyMode):
                p.updateBackWear(True)
                if p.modelServer.backwear.isActionJustSkillWear():
                    p.fashion.stopAllActions()
            elif info[1] == uiConst.SHOW_WAIST_WEAR and self.canUseItem(isDown, isKeyMode):
                p.updateWaistWear(True)
                if p.modelServer.waistwear.isActionJustSkillWear():
                    p.fashion.stopAllActions()
            elif info[1] == uiConst.GEM_ADD_REMOVE and self.canUseItem(isDown, isKeyMode):
                if not gameglobal.rds.ui.inventory.mediator:
                    gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INVENTORY)
                if not gameglobal.rds.ui.equipGem.mediator:
                    gameglobal.rds.ui.equipGem.show(0)
            elif info[1] == uiConst.EQUIP_LVUP_STAR:
                gameglobal.rds.ui.equipChange.show(uiConst.EQUIPCHANGE_TAB_STAR, 1)
            elif info[1] == uiConst.CHUAN_GONG and self.canUseItem(isDown, isKeyMode):
                BigWorld.player().useTrainSkill()
            elif info[1] == uiConst.APPLY_SHUANG_XIU and self.canUseItem(isDown, isKeyMode):
                BigWorld.player().useShuangxiuSkill()
            elif info[1] == uiConst.FOCUS_SETTING and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.focusTarget.showFocus()
            elif info[1] == uiConst.TARGET_SETTING and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.focusTarget.onFocusSelect()
            elif info[1] == uiConst.MAKE_EXP_XIUWEI_ITEM and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.bottle.show()
            elif info[1] == uiConst.YAOPEI_FEED and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.yaoPeiFeed.show()
            elif info[1] == uiConst.GENERAL_SKILL_RED_PACKET and self.canUseItem(isDown, isKeyMode):
                self.uiAdapter.redPacket.show()
            elif info[1] == uiConst.GENERAL_MIX_JEWELRY and self.canUseItem(isDown, isKeyMode):
                self.uiAdapter.mixFameJewelry.show()
            elif info[1] == uiConst.SWITCH_EQUIP and self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.roleInfo.realSwitchEquip()
            elif info[1] == uiConst.GO_HOME_ROOM and self.canUseItem(isDown, isKeyMode):
                BigWorld.player().useGoHomeRoomSkill()
            elif info[1] == uiConst.GO_WING_BORN_ISLAND and self.canUseItem(isDown, isKeyMode):
                BigWorld.player().enterToWingBornIslandBySkill(True, GMDD.data.GO_WING_WORLD_BY_SKILL_CONFIRM)
            elif info[1] == uiConst.LING_SHI_FLAG_SWITCH and self.canUseItem(isDown, isKeyMode):
                BigWorld.player().switchLingShiFlag()
            if info[0] == uiConst.SHORTCUT_TYPE_LIEF_SKILL and self.canUseItem(isDown, isKeyMode):
                if info[1] == uiConst.LIFE_SKILL_FISHING:
                    gameglobal.rds.ui.fishing.show()
                elif info[1] == uiConst.LIFE_SKILL_EXPLORE:
                    gameglobal.rds.ui.explore.show()
                else:
                    gameglobal.rds.ui.lifeSkillNew.showTarget(info[1])
            bagPage, bagPos, fromBag = self.getBagPagePosByBarPos(page, pos)
            if bagPage == const.CONT_NO_PAGE:
                if info[0] == uiConst.SHORTCUT_TYPE_SKILL:
                    p.autoSkill.switchToKeyboardMode()
                    if info[1] in p.guildMemberSkills.keys():
                        if self.canUseItem(isDown, isKeyMode):
                            gameglobal.rds.ui.skill.useGuildSkill(info[1])
                    elif info[1] in uiConst.INTIMACY_SKILL_ALL:
                        if self.canUseItem(isDown, isKeyMode):
                            gameglobal.rds.ui.skill.useIntimacySkill(info[1])
                    elif wingWorldUtils.getWingArmySkillData().has_key((info[1], 1)):
                        if self.canUseItem(isDown, isKeyMode):
                            if p.inWingCity():
                                p.cell.useWingWorldArmySkill(info[1])
                            else:
                                p.showGameMsg(GMDD.data.WING_WORLD_ARMY_SKILL_NOT_IN_WING_WORLD, ())
                    elif WWASD.data.has_key((info[1], 1)):
                        if self.canUseItem(isDown, isKeyMode):
                            p.cell.useWWArmySkill(info[1])
                    elif GSD.data.has_key(info[1]):
                        if self.canUseItem(isDown, isKeyMode):
                            p.useGuildSkill(info[1])
                    elif p.isPubgSkill(info[1]):
                        if p.checkCanUsePubgSkill(info[1]) and self.canUseItem(isDown, isKeyMode):
                            tgtId = p.targetLocked.id if p.targetLocked and p.targetLocked.id else p.id
                            p.cell.usePubgSkill(info[1], tgtId)
                    else:
                        self.useSkill(page, pos, isDown, isKeyMode)
                elif info[0] == uiConst.SHORTCUT_TYPE_ITEM_EQUIP:
                    if isDown == isKeyMode:
                        self.useEquipSkill(info)
                return
            if fromBag == const.RES_KIND_CROSS_INV:
                if self.canUseItem(isDown, isKeyMode):
                    gameglobal.rds.ui.itemPushUse.isActionClick = True
                    p.useActionBarItem(bagPage, bagPos, fromBag)
                    return
            elif isDown == isKeyMode:
                invItem = p.inv.getQuickVal(bagPage, bagPos)
                if invItem and invItem.isYaoPei():
                    p.showGameMsg(GMDD.data.YAOPEI_NEED_EQUIP, ())
                    return
            if self.canUseItem(isDown, isKeyMode):
                gameglobal.rds.ui.itemPushUse.isActionClick = True
                p.useActionBarItem(bagPage, bagPos, fromBag)

    def useEquipSkill(self, info):
        p = BigWorld.player()
        equipItem = self.findItemInEquipMent(info[1])
        if equipItem:
            if not equipItem.isYaoPei():
                equipSkillInfo = equipItem.getSkillVal()
                equipPartList = equipItem.whereEquip()
                equipPart = -1
                for part in equipPartList:
                    if getattr(BigWorld.player().equipment[part], 'uuid', None) == equipItem.uuid:
                        equipPart = part
                        break

                if equipSkillInfo:
                    if equipPart != -1:
                        equipSkillId = equipSkillInfo[0]
                        if equipItem.uuid == info[2]:
                            cellCmd.useEquipmentSkill(equipPart, equipSkillId)
                else:
                    ed = EPD.data.get(equipItem.id, {})
                    showWearId = ed.get('showWearId', 0)
                    attachedWear = ed.get('attachedWear', 0)
                    if showWearId and attachedWear == WEAR_ATTACH_ACTION_AS_ENTITY:
                        cellCmd.useWearSkill(equipPart, showWearId)
            else:
                equipSkillId = getattr(equipItem, 'yaoPeiSkillId', 0)
                if equipSkillId != 0:
                    yaopeiLv = equipItem.getYaoPeiLv()
                    yaopeiSkillLv = YLD.data.get(yaopeiLv, {}).get('skillLv', 0)
                    if yaopeiSkillLv == 0:
                        p.showGameMsg(GMDD.data.EQUIP_SKILL_LV_ZERO, ())
                        return
                    equipPartList = equipItem.whereEquip()
                    equipPart = -1
                    for part in equipPartList:
                        if getattr(BigWorld.player().equipment[part], 'uuid', None) == equipItem.uuid:
                            equipPart = part
                            break

                    if equipPart != -1:
                        if equipItem.uuid == info[2]:
                            cellCmd.useEquipmentSkill(equipPart, equipSkillId)

    def checkEquipSkillID(self, equipItemId):
        equipItem = self.findItemInEquipMent(equipItemId)
        if equipItem:
            if not equipItem.isYaoPei():
                equipItemInfo = equipItem.getSkillVal()
                if equipItemInfo:
                    return equipItemInfo[0]
            else:
                return getattr(equipItem, 'yaoPeiSkillId', 0)
        return 0

    def findItemInEquipMent(self, itemId):
        equipItem = None
        for item in BigWorld.player().equipment:
            if item and item.id == itemId:
                equipItem = item

        return equipItem

    def checkHasEquipSkillItem(self, item):
        if not item.isYaoPei():
            if not item.getSkillVal():
                return False
        elif getattr(item, 'yaoPeiSkillId', 0) == 0:
            return False
        p = BigWorld.player()
        _, page, pos = p.realInv.findItemByUUID(item.uuid)
        if page != const.CONT_NO_PAGE and pos != const.CONT_NO_POS:
            return True
        if self.findItemInEquipMent(item.id):
            return True
        return False

    def canUseItem(self, isDown, isKeyMode):
        return isDown and isKeyMode or not isDown and not isKeyMode

    def setShorCutItem(self, item, page, pos):
        if item == const.CONT_EMPTY_VAL:
            return
        if item.type == item.BASETYPE_EQUIP:
            self.setShortCut(page, pos, (uiConst.SHORTCUT_TYPE_ITEM_EQUIP, item.id, item.uuid))
        elif item.type == item.BASETYPE_CONSUMABLE:
            self.setShortCut(page, pos, (uiConst.SHORTCUT_TYPE_ITEM_COMSUME, item.id))

    def setShortCut(self, page, pos, info):
        p = BigWorld.player()
        operationMode = p.getOperationMode()
        data = self.clientShortCut
        if page == uiConst.SKILL_ACTION_BAR and pos < uiConst.WUSHUANG_SKILL_START_POS_LEFT or page in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2] and p._isSchoolSwitch():
            gameStrings.TEXT_ACTIONBARPROXY_2279
            if not self.clientShortCut.has_key(operationMode):
                self.clientShortCut[operationMode] = {}
            data = self.clientShortCut[operationMode]
        if info and info[1]:
            data[page, pos] = info
        elif data.has_key((page, pos)):
            data.pop((page, pos))

    def getShortCut(self, page, pos, default = 0):
        p = BigWorld.player()
        if not p:
            return
        operationMode = p.getOperationMode()
        data = self.clientShortCut
        if page == uiConst.SKILL_ACTION_BAR and pos < uiConst.WUSHUANG_SKILL_START_POS_LEFT or (page == uiConst.ITEM_ACTION_BAR or page == uiConst.ITEM_ACTION_BAR2) and p._isSchoolSwitch():
            if self.clientShortCut.has_key(operationMode):
                data = self.clientShortCut[operationMode]
            else:
                data = {}
        return data.get((page, pos), default)

    def getShortCutPos(self, idx):
        ret = []
        p = BigWorld.player()
        operationMode = p.getOperationMode()
        for key, value in self.clientShortCut.iteritems():
            if isinstance(value, tuple) and value[1] == idx:
                ret.append(key)

        if self.clientShortCut.has_key(operationMode):
            data = self.clientShortCut[operationMode]
            for key, value in data.iteritems():
                if value[1] == idx:
                    ret.append(key)

        return ret

    def getBasicSkillShortCut(self):
        ret = {}
        p = BigWorld.player()
        if not p:
            return ret
        operationMode = p.getOperationMode()
        for key, value in self.clientShortCut.iteritems():
            if isinstance(value, tuple) and value[0] == uiConst.SHORTCUT_TYPE_SKILL:
                ret[key] = value

        if self.clientShortCut.has_key(operationMode):
            ret.update(self.clientShortCut[operationMode])
        return ret

    def getWuShuangSkillShortCut(self):
        return uiUtils.getWSSkillShortCut(self.clientShortCut)

    def getAllSkillShortCut(self):
        ret = self.getBasicSkillShortCut()
        ret.update(self.getWuShuangSkillShortCut())
        return ret

    def getOtherShortCut(self):
        ret = {}
        for key, value in self.clientShortCut.iteritems():
            if isinstance(key, tuple) and isinstance(value, tuple) and value[0] != uiConst.SHORTCUT_TYPE_SKILL:
                ret[key] = value

        p = BigWorld.player()
        operationMode = p.getOperationMode()
        if self.clientShortCut.has_key(operationMode):
            shorcuts = self.clientShortCut[operationMode]
            for key, value in shorcuts.iteritems():
                if value[0] != uiConst.SHORTCUT_TYPE_SKILL:
                    ret[key] = value

        return ret

    def travalShortCut(self):
        ret = {}
        p = BigWorld.player()
        operationMode = p.getOperationMode()
        if self.clientShortCut.has_key(operationMode):
            ret.update(self.clientShortCut[operationMode])
        for key, value in self.clientShortCut.iteritems():
            if isinstance(key, tuple):
                ret[key] = value

        return ret

    def dragItemFromBag(self, item, nPageSrc, nPosSrc, nPageDes, nPosDes):
        self.removeItem(nPageDes, nPosDes)
        sType = self._getItemType(item)
        self.setItem(item, nPageDes, nPosDes, True, False, sType)
        self.setShorCutItem(item, nPageDes, nPosDes)
        BigWorld.player().saveShortcut(self.clientShortCut)

    def dragItemFromEquipBar(self, item, nPageDes, nPosDes):
        sType = self._getItemType(item)
        self.setItem(item, nPageDes, nPosDes, True, False, sType)
        self.setShorCutItem(item, nPageDes, nPosDes)
        BigWorld.player().saveShortcut(self.clientShortCut)
        self.refreshByBagUse(item)

    def dragFromEmote(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        nSrcID = self.uiAdapter.emote.getEmoteId(nPageSrc, nItemSrc)
        self.setItem(nSrcID, nPageDes, nItemDes, True, False, uiConst.SHORTCUT_TYPE_EMOTE)
        BigWorld.player().saveShortcut(self.clientShortCut)

    def moveItem(self, nPageSrc, nPosSrc, nPageDes, nPosDes):
        info = self.getShortCut(nPageSrc, nPosSrc, (0, 0))
        if info and info[1] in self.otherSkill or info[0] in (uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE,):
            sItem = info[1]
        elif info[0] == uiConst.SHORTCUT_TYPE_ITEM_EQUIP and len(info) > 2:
            sItem, _, _ = BigWorld.player().realInv.findItemByUUID(info[2])
            if not sItem:
                sItem = self.checkEquipmentByIdAndUuid(info[1], info[2])
            if not sItem:
                sItem = Item(sItem)
        else:
            bagPage, bagPos = BigWorld.player().realInv.findItemInPages(info[1], includeExpired=True, includeLatch=True, includeShihun=True)
            if bagPage == const.CONT_NO_PAGE:
                sItem = info[1]
                self._setItemSlotState(nPageSrc, nPosSrc, uiConst.SKILL_ICON_STAT_USEABLE)
                if info[0] in uiConst.SHORTCUT_TYPE_ITEM:
                    sItem = Item(sItem)
            else:
                sItem = BigWorld.player().realInv.getQuickVal(bagPage, bagPos)
        if not info:
            self.removeItem(nPageSrc, nPosSrc, False)
            self.setItem(sItem, nPageDes, nPosDes, True, False, uiConst.SHORTCUT_TYPE_NONE)
            self.setShortCut(nPageDes, nPosDes, info)
            self.setShortCut(nPageSrc, nPosSrc, None)
            self._setItemSlotState(nPageSrc, nPosSrc, uiConst.SKILL_ICON_STAT_USEABLE)
        else:
            infoDes = self.getShortCut(nPageDes, nPosDes, (0, 0))
            if infoDes and infoDes[1] in self.otherSkill or infoDes[0] in (uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE,):
                dItem = infoDes[1]
            elif infoDes[0] == uiConst.SHORTCUT_TYPE_ITEM_EQUIP and len(infoDes) > 2:
                dItem, _, _ = BigWorld.player().realInv.findItemByUUID(infoDes[2])
                if not dItem:
                    dItem = self.checkEquipmentByIdAndUuid(infoDes[1], infoDes[2])
            else:
                dItem = self.getItemByBarPagePos(nPageDes, nPosDes)
            self.removeItem(nPageDes, nPosDes)
            self.removeItem(nPageSrc, nPosSrc)
            self.setItem(sItem, nPageDes, nPosDes, True, False, info[0])
            self.setItem(dItem, nPageSrc, nPosSrc, True, False, infoDes[0])
            self.setShortCut(nPageDes, nPosDes, info)
            self.setShortCut(nPageSrc, nPosSrc, infoDes)
        self.updateSlots()
        self.showToggleShine({})
        BigWorld.player().saveShortcut(self.clientShortCut)

    def discardItem(self, nPageSrc, nPosSrc, isDiscard = False, isRefresh = True, srcItemId = 0):
        if not isDiscard:
            self.removeItem(nPageSrc, nPosSrc, isRefresh)
        info = self.getShortCut(nPageSrc, nPosSrc)
        if info:
            itemId = info[1]
            if itemId in self.otherSkill and isDiscard:
                for k, v in self.travalShortCut().items():
                    if v[1] == itemId:
                        self.setItem(itemId, k[0], k[1], isRefresh, False, info[0])

                return
            if info[0] == uiConst.SHORTCUT_TYPE_EMOTE:
                for key, value in self.getOtherShortCut().items():
                    if self.validEmoteItem(value[1], srcItemId):
                        self.setItem(value[1], key[0], key[1], isRefresh, False, info[0])

            if not isDiscard:
                self.setShortCut(nPageSrc, nPosSrc, None)
            self._setItemSlotState(nPageSrc, nPosSrc, uiConst.SKILL_ICON_STAT_USEABLE)
            if isDiscard:
                self.resetItemActionBar(nPageSrc, nPosSrc)
            self.updateSlots()
        if not isRefresh:
            BigWorld.player().saveShortcut(self.clientShortCut)

    def _refreshItemActionBar(self, item, itemId, isRefresh = True):
        ret = self.getBarPagePosByItem(item)
        if not ret:
            return
        gameStrings.TEXT_ACTIONBARPROXY_2473
        gameStrings.TEXT_ACTIONBARPROXY_2474
        gameStrings.TEXT_ACTIONBARPROXY_2475
        k = ret[0]
        self._refreshItemActionBarSlot(k[0], k[1], isRefresh, itemId)
        if not isRefresh:
            BigWorld.player().saveShortcut(self.clientShortCut)

    def _refreshItemActionBarSlot(self, page, pos, isRefresh, srcItemId):
        p = BigWorld.player()
        if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
            return
        bagPage, bagPos, fromBag = self.getBagPagePosByBarPos(page, pos)
        if bagPage == const.CONT_NO_PAGE:
            info = self.getShortCut(page, pos, [0, 0])
            if info:
                itemId = info[1]
                equipItem = self.checkEquipment(itemId)
                if not equipItem:
                    self.discardItem(page, pos, True, isRefresh, srcItemId)
                else:
                    self.setItemActionBarByItem(page, pos, equipItem, isRefresh)
            return
        if fromBag == const.RES_KIND_INV:
            item = p.inv.getQuickVal(bagPage, bagPos)
        else:
            item = p.crossInv.getQuickVal(bagPage, bagPos)
        if not item:
            self.discardItem(page, pos, True, isRefresh, srcItemId)
        else:
            self.setItemActionBarByItem(page, pos, item, isRefresh)

    def refreshByBagUse(self, item, isRefresh = True):
        if isinstance(item, Item):
            itemId = item.id
        else:
            itemId = item
        self._refreshItemActionBar(item, itemId, isRefresh)

    def refreshActionbarItem(self, page, pos):
        i = self.getItemByBarPagePos(page, pos)
        if i:
            self.setSlotColor(page, pos, 'nothing')
            info = self.getShortCut(page, pos, [1, 1])
            if info[1] in self.otherSkill:
                self.setRideItem(info[1], page, pos, False)
            elif info[1] in self.lifeSkill:
                self.setLifeItem(info[1], page, pos, False)
            elif page == uiConst.SKILL_ACTION_BAR and (i in BigWorld.player().getSkills().keys() or info[0] in uiConst.SHORTCUT_TYPE_ITEM) or page in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
                self.setItem(i, page, pos, True, True, info[0])
        else:
            self.removeItem(page, pos)

    def getActionSkill(self):
        ret = self.getSkillId(ALL_SKILL)
        ret.extend(gameglobal.rds.ui.airbar.getAirbarSkills())
        return ret

    def getTargetSkillList(self):
        res = []
        temList = self.getActionSkill()
        p = BigWorld.player()
        for skillId in temList:
            sVal = p.getSkills().get(skillId)
            if sVal == None:
                continue
            skillInfo = self._getSkillInfo(skillId)
            if self._isTargetSkill(skillId) and checkTargetRelationRequest(skillInfo, False):
                res.append(skillId)

        return res

    def setSlotState(self, skillId, state):
        self.skillIconStat[skillId] = state
        if skillId in gameglobal.rds.ui.airbar.getAirbarSkills():
            gameglobal.rds.ui.airbar.setSlotStateBySkillId(skillId, state)
            return
        else:
            key = self._getPosByActionID(skillId)
            for item in key:
                bar, slot = self.getSlotID(item)
                if bar in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2] and gameglobal.rds.ui.trade.isShow:
                    continue
                if not self.isSkill(skillId):
                    continue
                if item and self.binding.get(item) != None:
                    self.binding[item][0].Invoke('setSlotState', GfxValue(state))
                    keyboardEffect.addSlotStateEffect(bar, slot, state)

            self.refreshEmptySlotEffect()
            return

    @ui.callAfterTime()
    def refreshEmptySlotEffect(self):
        if not keyboardEffect.canControlKeyboard():
            return
        bar = uiConst.SKILL_ACTION_BAR
        for slot in xrange(len(HK.SHORCUT_SKILL_KEYS)):
            if self.getActionIDByPos(bar, slot) == 0:
                keyboardEffect.removeSlotCDEffect(bar, slot)
                keyboardEffect.removeSlotStateEffect(bar, slot)

    def _setSlotState(self, idSlot, state):
        key = self._getKey(0, idSlot)
        if key and self.binding.get(key) != None:
            self.binding[key][0].Invoke('setSlotState', GfxValue(state))

    def _setItemSlotState(self, idBar, idSlot, state):
        key = self._getKey(idBar, idSlot)
        if key and self.binding.get(key) != None:
            self.binding[key][0].Invoke('setSlotState', GfxValue(state))

    def setSlotKeyText(self, keyArr):
        self.slotKey = keyArr
        if len(self.slotKey) == 12:
            self.slotKey.extend(['F3',
             'F4',
             'F5',
             'F6'])
        if len(self.slotKey) == 16:
            self.slotKey.extend(['S+1',
             'S+2',
             'S+3',
             'S+4',
             'S+5',
             'S+6',
             'S+7',
             'S+8',
             'S+9',
             'S+0',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             ''])
        if len(self.slotKey) == 40:
            self.slotKey.extend(['',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             ''])
        ret = self.movie.CreateArray()
        for i, item in enumerate(keyArr):
            if len(item) > 4:
                item = '...'
            ret.SetElement(i, GfxValue(gbk2unicode(item)))

        if self.mc != None:
            self.mc.Invoke('setSlotKeyText', ret)
        if self.wsMc != None:
            self.wsMc.Invoke('setSlotKeyText', ret)
        if gameglobal.rds.ui.skill.isShow:
            gameglobal.rds.ui.skill.refreshSpecialSkill()
        self.setItemBarKeyText(keyArr[uiConst.WUSHUANG_SKILL_END_POS:])
        self.setItemBarKeyText(keyArr[uiConst.ITEM_BAR1_END_POS:], uiConst.TYPE_ITEM_BAR2)
        gameglobal.rds.ui.airbar.setSlotKeyText()

    def onGetWSName(self, *arg):
        key = int(arg[3][0].GetNumber())
        return GfxValue(gbk2unicode(SPD.data[BigWorld.player().realSchool].get('wsType' + str(key), '')))

    def resetSlotKey(self):
        self.slotKey = self.getDefaultKeyDesc()

    def getDefaultKeyDesc(self):
        return [ hotkey.HKM[key].getBrief() for key in hotkey.SHORTCUT_KEYS ]

    def setSlotColor(self, idBar, idSlot, color):
        if idBar == uiConst.SKILL_ACTION_BAR:
            if self.mc != None:
                self.mc.Invoke('setSlotColor', (GfxValue(idSlot), GfxValue(color)))
        elif idBar == uiConst.ITEM_ACTION_BAR:
            if self.itemMc[0] != None:
                self.itemMc[0].Invoke('setSlotColor', (GfxValue(idSlot), GfxValue(color)))
        elif idBar == uiConst.ITEM_ACTION_BAR2:
            if self.itemMc[1] != None:
                self.itemMc[1].Invoke('setSlotColor', (GfxValue(idSlot), GfxValue(color)))

    def setEquipSlotState(self, item, idSlot):
        state = gameglobal.rds.ui.roleInfo.calcSlotState(item, False)
        gameglobal.rds.ui.roleInfo.setSlotState(idSlot, state)

    def _getWsSkillStar(self, skillId):
        if skillId == 0:
            return 0
        else:
            skill = BigWorld.player().wsSkills.get(skillId, None)
            if not skill:
                return 0
            return skillDataInfo.getWsStarLv(SkillInfo(skillId, skill.level))

    def setSpecialSlotsShine(self, enabled, type = 2):
        if self.wsMc != None:
            self.wsMc.Invoke('setSpecialSlotsShine', (GfxValue(enabled), GfxValue(type)))
        if enabled:
            if type == 0:
                for slot in xrange(uiConst.WUSHUANG_SKILL_START_POS_RIGHT, uiConst.WUSHUANG_SKILL_END_POS):
                    self._setSlotState(slot, uiConst.SKILL_ICON_STAT_RED)

            elif type == 1:
                for slot in xrange(uiConst.WUSHUANG_SKILL_START_POS_LEFT, uiConst.WUSHUANG_SKILL_START_POS_RIGHT):
                    self._setSlotState(slot, uiConst.SKILL_ICON_STAT_RED)

        else:
            for slot in xrange(uiConst.WUSHUANG_SKILL_START_POS_LEFT, uiConst.WUSHUANG_SKILL_END_POS):
                self._setSlotState(slot, uiConst.SKILL_ICON_STAT_USEABLE)

    def setNormalSlotsShine(self, enabled):
        if self.mc != None:
            self.mc.Invoke('setNormalSlotsShine', GfxValue(enabled))
        for i in xrange(2):
            if self.itemMc[i] != None:
                self.itemMc[i].Invoke('setNormalSlotsShine', GfxValue(enabled))

    def showToggleShine(self, old):
        self.uiAdapter.zaijuV2.showToggleShine(old)
        p = BigWorld.player()
        newState = set(p.statesServerAndOwn.keys())
        oldState = set(old.keys())
        addState = newState - oldState
        delState = oldState - newState
        if delState and type(delState) == set:
            for state in delState:
                skillId = self.getSwitchSkill(state)
                if skillId:
                    self.showActionBarToggleShine(False)
                    self.switchSkill.remove((state, skillId))

        if addState and type(addState) == set:
            for state in addState:
                skillId = self.getSwitchSkill(state)
                if skillId:
                    self.showActionBarToggleShine(True)

    def isBanWSSkillBuff(self, stateId):
        if gametypes.SKILL_STATE_SE_BAN_WS_SKILL in STD.data.get(stateId, {}).get('allAttrIds', []):
            return True
        return False

    def getSwitchSkill(self, state):
        if self.switchSkill:
            for stateId, skillId in self.switchSkill:
                if stateId == state:
                    return skillId

        return 0

    def notifyWuShuangCanUse(self, idSlot):
        if self.wsMc:
            self.wsMc.Invoke('playWushuangAnimation', GfxValue(idSlot))

    def notifyWuShuangCannotUse(self, idSlot):
        if self.wsMc:
            self.wsMc.Invoke('stopWushuangAnimation', GfxValue(idSlot))

    @ui.callAfterTime()
    def showWuShuangAnimation(self):
        p = BigWorld.player()
        for i, skillId in enumerate(self.getSkillId(WUSHUANG_SKILL)):
            idSlot = uiConst.WUSHUANG_SKILL_START_POS_LEFT + i
            if skillId == 0:
                if self.recordAnimation[idSlot]:
                    self.notifyWuShuangCannotUse(idSlot)
                    self.recordAnimation[idSlot] = False
                continue
            sVal = p.getSkills().get(skillId, None)
            if sVal == None:
                if self.recordAnimation[idSlot]:
                    self.notifyWuShuangCannotUse(idSlot)
                    self.recordAnimation[idSlot] = False
                continue
            skillInfo = self._getSkillInfo(skillId)
            wsVal = p.ws[0] if idSlot < uiConst.WUSHUANG_SKILL_START_POS_RIGHT else p.ws[1]
            wsNeed = skillInfo.getSkillData('wsNeed1', 0) if idSlot < uiConst.WUSHUANG_SKILL_START_POS_RIGHT else skillInfo.getSkillData('wsNeed2', 0)
            wsReduce = p.wsReduce[0] if idSlot < uiConst.WUSHUANG_SKILL_START_POS_RIGHT else p.wsReduce[1]
            if wsReduce:
                wsNeed = int(round((1 - wsReduce) * wsNeed))
            if self._checkCanShowWSAnimation(skillId, idSlot, wsVal, wsNeed):
                if not self.recordAnimation[idSlot]:
                    self.notifyWuShuangCanUse(idSlot)
                    self.recordAnimation[idSlot] = True
            elif self.recordAnimation[idSlot]:
                self.notifyWuShuangCannotUse(idSlot)
                self.recordAnimation[idSlot] = False

    def _checkCanShowWSAnimation(self, skillId, idSlot, wsVal, wsNeed):
        if self._getWSRemainTime(skillId) <= 0 and wsVal >= wsNeed:
            return True
        return False

    def _getWSRemainTime(self, skillId):
        endGcd = logicInfo.commonCooldownWeaponSkill[0]
        totalGcd = logicInfo.commonCooldownWeaponSkill[1]
        remainGcd = endGcd - BigWorld.time()
        if skillId in logicInfo.cooldownSkill:
            end, total = logicInfo.cooldownSkill[skillId]
            remain = end - BigWorld.time()
            if total != 0:
                if remain < remainGcd:
                    remain = remainGcd
                    total = totalGcd
        else:
            remain = 0
            total = 0
        return remain

    def setSpecialSlotState(self, state):
        if self.wsMc is None:
            return
        else:
            for slot in xrange(uiConst.WUSHUANG_SKILL_START_POS_LEFT, uiConst.WUSHUANG_SKILL_END_POS):
                self._setSlotState(slot, state)

            alpha = 1 if state == uiConst.SKILL_ICON_STAT_USEABLE else 0.3
            self.wsMc.Invoke('getWidget').SetMember('alpha', GfxValue(alpha))
            return

    def setNormalSlotState(self, state):
        for slot in xrange(0, uiConst.WUSHUANG_SKILL_START_POS_LEFT):
            info = self.getShortCut(0, slot)
            if info and info[0] == uiConst.SHORTCUT_TYPE_SKILL:
                self._setSlotState(slot, state)

        for slot in xrange(0, uiConst.ITEM_ACTION_BAR_SLOT_NUM * 2):
            for page in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
                info = self.getShortCut(page, slot)
                if info and info[0] == uiConst.SHORTCUT_TYPE_SKILL:
                    self._setItemSlotState(page, slot, state)

        alpha = 1 if state == uiConst.SKILL_ICON_STAT_USEABLE else 0.3
        self.mc.Invoke('getWidget').SetMember('alpha', GfxValue(alpha))
        for i in xrange(2):
            if self.itemMc[i]:
                self.itemMc[i].Invoke('getWidget').SetMember('alpha', GfxValue(alpha))

    def setAllSlotAlpha(self, state):
        if not (self.mc and self.itemMc[0] and self.wsMc and self.itemMc[1]):
            return
        alpha = 1 if state == uiConst.SKILL_ICON_STAT_USEABLE else 0.3
        self.mc.Invoke('getWidget').SetMember('alpha', GfxValue(alpha))
        for i in xrange(2):
            self.itemMc[i].Invoke('getWidget').SetMember('alpha', GfxValue(alpha))

        self.wsMc.Invoke('getWidget').SetMember('alpha', GfxValue(alpha))

    def setRideShine(self, isShow, idAction):
        for slot in xrange(uiConst.MAX_ITEMBAR_SLOT * 2):
            typeList = [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]
            for barType in typeList:
                info = self.getShortCut(barType, slot, (0, 0))
                if info and (info[1] == idAction or info[0] == uiConst.SHORTCUT_TYPE_EMOTE and idAction == uiConst.COUPLEEMOTE and ED.data.get(info[1], {}).get('funcType') == uiConst.EMOTE_FUNTYPE_COUPLE_EMOTE):
                    key = self._getKey(barType, slot)
                    if not self.binding.has_key(key):
                        continue
                    if info[0] == uiConst.SHORTCUT_TYPE_EMOTE and idAction == uiConst.COUPLEEMOTE and ED.data.get(info[1], {}).get('funcType') == uiConst.EMOTE_FUNTYPE_COUPLE_EMOTE:
                        coupleEmote = BigWorld.player().coupleEmote
                        if isShow and not (coupleEmote and coupleEmote[0] == int(ED.data.get(info[1]).get('res', 1))):
                            continue
                    self.binding[key][0].Invoke('showToggleShine', GfxValue(isShow))

        for slot in xrange(uiConst.WUSHUANG_SKILL_START_POS_LEFT):
            info = self.getShortCut(uiConst.SKILL_ACTION_BAR, slot, (0, 0))
            if info and (info[1] == idAction or info[0] == uiConst.SHORTCUT_TYPE_EMOTE and idAction == uiConst.COUPLEEMOTE and ED.data.get(info[1], {}).get('funcType') == uiConst.EMOTE_FUNTYPE_COUPLE_EMOTE):
                key = self._getKey(uiConst.SKILL_ACTION_BAR, slot)
                if not self.binding.has_key(key):
                    continue
                self.binding[key][0].Invoke('showToggleShine', GfxValue(isShow))

    def setRideItem(self, idAction, idBar, idSlot, isRefresh = True):
        self.setItem(idAction, idBar, idSlot, True, False, uiConst.SHORTCUT_TYPE_ITEM_COMSUME)
        self.setShortCut(idBar, idSlot, (uiConst.SHORTCUT_TYPE_ITEM_COMSUME, idAction))
        if not isRefresh:
            BigWorld.player().saveShortcut(self.clientShortCut)

    def setLifeItem(self, idAction, idBar, idSlot, isRefresh = True):
        self.setItem(idAction, idBar, idSlot, True, False, uiConst.SHORTCUT_TYPE_LIEF_SKILL)
        self.setShortCut(idBar, idSlot, (uiConst.SHORTCUT_TYPE_LIEF_SKILL, idAction))
        if not isRefresh:
            BigWorld.player().saveShortcut(self.clientShortCut)

    def setSpecialSlotShine(self):
        if self.wsMc != None:
            ret = self.movie.CreateArray()
            p = BigWorld.player()
            ret.SetElement(0, GfxValue(int(math.floor(p.ws[0] / 100.0))))
            ret.SetElement(1, GfxValue(int(math.floor(p.ws[1] / 100.0))))
            self.wsMc.Invoke('setWSSkillShine', ret)

    def _isWsSkill(self, skillId):
        p = BigWorld.player()
        if p.wsSkills.has_key(skillId):
            return True
        return False

    def setItemBarKeyText(self, keyArr, itemBarType = 0):
        ret = self.movie.CreateArray()
        for i, item in enumerate(keyArr):
            if len(item) > 4:
                item = '...'
            ret.SetElement(i, GfxValue(gbk2unicode(item)))

        if self.itemMc[itemBarType] != None:
            self.itemMc[itemBarType].Invoke('setItemBarText', ret)

    def setAllItemSlotVisible(self, visible):
        for i in xrange(2):
            if self.itemMc[i] != None:
                self.itemMc[i].Invoke('showAllSlotVisible', GfxValue(visible))

    def setItemSlotVisible(self, slotId, visible, itemBarType = 0):
        if self.itemMc[itemBarType] != None:
            self.itemMc[itemBarType].Invoke('setSlotVisible', (GfxValue(slotId), GfxValue(visible)))

    def validateSlotVisible(self):
        if not self.validateSlotCallBack:
            self.validateSlotCallBack = BigWorld.callback(0.1, self._innerValidateSlotVisible)

    def _innerValidateSlotVisible(self):
        self.validateSlotCallBack = None
        if not self.isShowItemBar:
            self._setItemMcVisible(0, self.isShowItemBar)
        if not self.isShowItemBar2:
            self._setItemMcVisible(1, self.isShowItemBar2)
        for i in xrange(2):
            if self.itemMc[i] != None:
                if i == ITEMBAR_TYPE_1:
                    self.itemMc[i].Invoke('validateSlotVisible', (GfxValue(self.isShowItemBar),))
                elif i == ITEMBAR_TYPE_2:
                    self.itemMc[i].Invoke('validateSlotVisible', (GfxValue(self.isShowItemBar2),))

    def isSkill(self, idx):
        for v in self.getAllSkillShortCut().itervalues():
            if v[1] == idx:
                if v[0] == uiConst.SHORTCUT_TYPE_SKILL:
                    return True

        return False

    def showActionBarToggleShine(self, isShow):
        if self.switchSkill:
            for stateId, skillId in self.switchSkill:
                keys = self._getPosByActionID(skillId)
                for key in keys:
                    if not self.binding.has_key(key):
                        continue
                    self.binding[key][0].Invoke('showToggleShine', GfxValue(isShow))

    def refreshAfterDragDisabled(self):
        self.validateSlotVisible()
        AppSettings[ASAP_TYPE] = self.itemBarType[0]
        AppSettings[ASAP_ROW] = self.itemBarRow[0]
        AppSettings[ASAP_TYPE2] = self.itemBarType[1]
        AppSettings[ASAP_ROW2] = self.itemBarRow[1]

    def enableItemBar(self, enable, itemBarType = 0):
        if self.itemMc[itemBarType] != None:
            self.itemMc[itemBarType].Invoke('enableItemBar', GfxValue(enable))

    def onGetItemBarConfig(self, *arg):
        widgetType = int(arg[3][0].GetNumber())
        ret = self.movie.CreateArray()
        if widgetType == 0:
            ret.SetElement(0, GfxValue(self.itemBarType[0]))
            ret.SetElement(1, GfxValue(self.itemBarRow[0]))
        else:
            ret.SetElement(0, GfxValue(self.itemBarType[1]))
            ret.SetElement(1, GfxValue(self.itemBarRow[1]))
        return ret

    def onChangeItemBarType(self, *arg):
        self.itemBarType[int(arg[3][0].GetNumber())] = int(arg[3][1].GetNumber())
        if gameglobal.rds.ui.trade.isShow:
            self.enableItemBar(False)

    def onChangeItembarRow(self, *arg):
        self.itemBarRow[int(arg[3][0].GetNumber())] = int(arg[3][1].GetNumber())
        if gameglobal.rds.ui.trade.isShow:
            self.enableItemBar(False)

    def setItemMcVisible(self, index, visible):
        self._setItemMcVisible(index, visible)
        self.validateSlotVisible()

    def _setItemMcVisible(self, index, visible):
        if index == 0:
            self.isShowItemBar = visible
        else:
            self.isShowItemBar2 = visible
        if self.itemMc[index] != None:
            self.itemMc[index].Invoke('showAllSlotVisible', GfxValue(visible))

    def showItemBar(self, visible):
        self.isShowItemBar = True if visible else False
        self.setAllItemSlotVisible(True)
        if not self.isShowItemBar and not self.isItemBarInEdit():
            self.validateSlotVisible()

    def checkAvatarState(self):
        inAirBattle = gameglobal.rds.ui.skill.inAirBattleState()
        p = BigWorld.player()
        gameStrings.TEXT_ACTIONBARPROXY_2978
        if gameglobal.rds.ui.isHideAllUI():
            if not p.isInBfDota():
                self.uiAdapter.setWidgetVisible(uiConst.WIDGET_ACTION_BARS, not inAirBattle)
        elif BigWorld.player().bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
            if self.mc:
                self.mc.Invoke('setVisible', GfxValue(False))
        elif self.mc:
            self.refreshCommonSkillActionBarOpacity()
        gameStrings.TEXT_ACTIONBARPROXY_2988
        if self.wsMc:
            self.wsMc.Invoke('showWSbarAndSchoolCenter', GfxValue(not inAirBattle))

    def setFirstRideShine(self):
        p = BigWorld.player()
        isInHorse = p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
        self.setRideShine(isInHorse, uiConst.HORSE_RIDING)

    def isItemBarInEdit(self, itemBarType = 0):
        if self.itemMc[itemBarType] == None:
            return False
        else:
            return self.itemMc[itemBarType].Invoke('isInEdit').GetBool()

    def _getSkillInfo(self, skillId):
        if not self.skillInfoCache.has_key(skillId):
            sVal = BigWorld.player().getSkills().get(skillId, None)
            level = sVal.level if sVal and sVal.level != 0 else 1
            self.skillInfoCache[skillId] = BigWorld.player().getSkillInfo(skillId, level)
        return self.skillInfoCache[skillId]

    def _isTargetSkill(self, skillId):
        skillInfo = self._getSkillInfo(skillId)
        return skillInfo.isTargetSkill()

    def _isSelfSkillType(self, skillInfo):
        p = BigWorld.player()
        skillTargetType, skillTargetValue = p.getSkillTargetType(skillInfo)
        if skillTargetValue:
            if skillTargetType in (gametypes.SKILL_TARGET_ENERMY, gametypes.SKILL_TARGET_FRIEND):
                return False
            if skillTargetType in (gametypes.SKILL_TARGET_ALL_TYPE, gametypes.SKILL_TARGET_SELF_ENERMY, gametypes.SKILL_TARGET_SELF_FRIEND):
                return True
        return False

    def _checkSkillTgt(self, skillId):
        if not self._isTargetSkill(skillId):
            return gameglobal.SKILL_TGT_NO_NEED_TGT
        skillInfo = self._getSkillInfo(skillId)
        p = BigWorld.player()
        if p.targetLocked == None:
            return gameglobal.SKILL_TGT_UNLOCK_TGT
        elif self._isSelfSkillType(skillInfo):
            return gameglobal.SKILL_TGT_RIGHT_TGT
        elif not checkTargetRelationRequest(skillInfo, False) and hasattr(p.targetLocked, 'hp'):
            return gameglobal.SKILL_TGT_WRONG_TGT
        else:
            return gameglobal.SKILL_TGT_RIGHT_TGT

    def _lackEnergy(self, skillId):
        lv = BigWorld.player().getSkills()[skillId].level
        skillInfo = BigWorld.player().getSkillInfo(skillId, lv)
        if not checkSelfRequest(skillInfo, False):
            return True
        return False

    def _isUseSkillForbidden(self, skillId):
        p = BigWorld.player()
        if commcalc.getBitDword(p.publicFlags, gametypes.FLAG_NO_SKILL) or p.qinggongState != gametypes.QINGGONG_STATE_DEFAULT:
            return True
        if p.doQingGongActionState:
            return True
        if skillId not in p.skills and skillId not in p.wsSkills and skillId not in p.airSkills:
            return True
        if p.bannedSkils and skillId in p.bannedSkils:
            return True
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_HOOK) and not p._isOnZaiju():
            return True
        skillInfo = self._getSkillInfo(skillId)
        if skillInfo.getSkillData('noInCombat', 0) and p.inCombat == True:
            return True
        return False

    def isBanWSSkill(self, skillId):
        p = BigWorld.player()
        lv = p.getSkills()[skillId].level
        skillInfo = p.getSkillInfo(skillId, lv)
        return skillInfo and skillInfo.isWsSkill() and p.hasStateAttr(gametypes.SKILL_STATE_SE_BAN_WS_SKILL)

    SKILL_STAT_CHECK_FUNC_MAP = {SKILL_STAT_SKILL_TGT: '_checkSkillTgt',
     SKILL_STAT_LACK_ENERGY: '_lackEnergy',
     SKILL_STAT_NO_SKILL: '_isUseSkillForbidden',
     SKILL_STAT_BAN_WS_SKILL: 'isBanWSSkill'}

    def initSkillStat(self, skillId):
        if not skillId or not BigWorld.player().getSkills().has_key(skillId):
            return
        self.skillStatCache[skillId] = [0] * gameglobal.SKILL_STAT_CNT
        self.skillIconStat[skillId] = uiConst.SKILL_ICON_STAT_USEABLE
        self.setSlotState(skillId, uiConst.SKILL_ICON_STAT_USEABLE)
        oldSkillStat = copy.deepcopy(self.skillStatCache[skillId])
        self._updataSkillStat(skillId, SKILL_STAT_SKILL_TGT, self._checkSkillTgt(skillId))
        self._updataSkillStat(skillId, SKILL_STAT_LACK_ENERGY, self._lackEnergy(skillId))
        self._updataSkillStat(skillId, SKILL_STAT_NO_SKILL, self._isUseSkillForbidden(skillId))
        self._updataSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, self._checkInSkillRange(skillId))
        self._updataSkillStat(skillId, SKILL_STAT_BAN_WS_SKILL, self.isBanWSSkill(skillId))
        self._updataSkillStat(skillId, SKILL_STAT_BAN_SKILL, self._checkNeedForceBanSkill(skillId))
        if oldSkillStat != self.skillStatCache[skillId]:
            self._updateSkillIcon(skillId)

    def _updataSkillStat(self, skillId, skillStatType, newStat):
        if not self.skillStatCache.has_key(skillId):
            self.initSkillStat(skillId)
        self.skillStatCache[skillId][skillStatType] = int(newStat)
        if skillStatType == gameglobal.SKILL_STAT_SKILL_TGT:
            if newStat == gameglobal.SKILL_TGT_NO_NEED_TGT or newStat == gameglobal.SKILL_TGT_UNLOCK_TGT:
                self._updataSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, True)

    def _checkNeedForceBanSkill(self, skillId):
        p = BigWorld.player()
        if p.isPubgCommSkillLock(skillId):
            return 1
        return 0

    def _updateSkillIcon(self, skillId):
        skillStat = self.skillStatCache[skillId]
        curIconStat = self.skillIconStat[skillId]
        d = SICD.data.get((skillStat[0],
         skillStat[1],
         skillStat[2],
         skillStat[3]), {})
        nextIconStat = d.get('nextStat', 1)
        if len(skillStat) > 4 and skillStat[4]:
            nextIconStat = uiConst.SKILL_ICON_STAT_GRAY
        if len(skillStat) == gameglobal.SKILL_STAT_CNT and skillStat[SKILL_STAT_BAN_SKILL]:
            nextIconStat = uiConst.SKILL_ICON_STAT_LOCK
        if curIconStat == nextIconStat:
            return
        if BigWorld.player().interactiveObjectEntId:
            return
        self.setSlotState(skillId, nextIconStat)

    def checkSkillStat(self, skillId, skillStatType, inSkillRange = False):
        if skillId == 0:
            return
        if skillStatType == gameglobal.SKILL_STAT_IN_SKILL_RANGE:
            self._updataSkillStat(skillId, skillStatType, inSkillRange)
        else:
            funcName = self.SKILL_STAT_CHECK_FUNC_MAP[skillStatType]
            newStat = getattr(self, funcName)(skillId)
            self._updataSkillStat(skillId, skillStatType, newStat)
        self._updateSkillIcon(skillId)

    def checkAllSkillStat(self, skillStatType):
        if formula.inDotaBattleField(BigWorld.player().mapID) and self.uiAdapter.zaijuV2.widget:
            self.uiAdapter.zaijuV2.checkAllSkillStat(skillStatType)
            return
        skills = self.getActionSkill()
        for skillId in skills:
            if skillId == 0 or not BigWorld.player().getSkills().has_key(skillId):
                continue
            self.checkSkillStat(skillId, skillStatType)

    def checkSkillMultiStat(self, skillId, statTypeList, inSkillRange = False):
        for statType in statTypeList:
            if statType == gameglobal.SKILL_STAT_IN_SKILL_RANGE:
                self._updataSkillStat(skillId, statType, inSkillRange)
            else:
                funcName = self.SKILL_STAT_CHECK_FUNC_MAP[statType]
                newStat = getattr(self, funcName)(skillId)
                self._updataSkillStat(skillId, statType, newStat)

        self._updateSkillIcon(skillId)

    def checkAllSkillMultiStat(self, skillStatTypeList):
        skills = self.getActionSkill()
        for skillId in skills:
            if skillId == 0 or not BigWorld.player().getSkills().has_key(skillId):
                continue
            self.checkSkillMultiStat(skillId, skillStatTypeList)

    @ui.callAfterTime()
    def initAllSkillStat(self):
        p = BigWorld.player()
        if not (p and p.inWorld):
            return
        skills = self.getActionSkill()
        for skillId in skills:
            if skillId == 0:
                continue
            if GSD.data.has_key(skillId) and GSD.data.get(skillId, {}).get('clientSkill', 0):
                skillId = GSD.data.get(skillId, {}).get('clientSkill', 0)
            skillLv = self._getSkillLv(skillId)
            if not SGD.data.get((skillId, skillLv), {}) and skillId not in uiConst.INTIMACY_SKILL_ALL:
                self.removeItemBySkillId(skillId)
                continue
            self.initSkillStat(skillId)

        if gameglobal.rds.ui.zaiju.exitMediator:
            gameglobal.rds.ui.zaiju.enableSkillInZaiju(False)
        elif gameglobal.rds.ui.zaijuV2.widget and gameglobal.rds.ui.zaijuV2.showType == uiConst.ZAIJU_SHOW_TYPE_EXIT:
            gameglobal.rds.ui.zaijuV2.enableSkillInZaiju(False)

    def checkSkillStatOnPropModified(self):
        self.initAllSkillStat()
        p = BigWorld.player()
        if not p.targetLocked:
            return
        if p.targetLocked.IsCombatUnit and p.targetLocked.addRanged == True:
            p.targetLocked.delRanges()
            p.targetLocked.addRanges()
        elif p.isCombatUnit(p.targetLocked):
            p.targetLocked.addRanges()

    def _calcRealSkillRangeMin(self, rangeMin):
        rangeMin += BigWorld.player().targetLocked.getBodySize()
        rangeMin = round(rangeMin, 2)
        return rangeMin

    def onEnterClientRangeNew(self, skillId, dist):
        p = BigWorld.player()
        if skillId == 0 or not p.getSkills().has_key(skillId):
            return
        else:
            lv = p.getSkills()[skillId].level
            skillInfo = p.getSkillInfo(skillId, lv)
            rangeMin = skillInfo.getSkillData('rangeMin', 0)
            if rangeMin != 0 and p.targetLocked != None:
                rangeMin = self._calcRealSkillRangeMin(rangeMin)
                if dist == rangeMin:
                    self.checkSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, False)
                    return
            self.checkSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, True)
            return

    def onLeaveClientRangeNew(self, skillId, dist):
        p = BigWorld.player()
        if skillId == 0 or not p.getSkills().has_key(skillId):
            return
        else:
            sVal = p.getSkills().get(skillId)
            skillInfo = p.getSkillInfo(skillId, sVal.level)
            rangeMin = skillInfo.getSkillData('rangeMin', 0)
            if rangeMin != 0 and p.targetLocked != None:
                rangeMin = self._calcRealSkillRangeMin(rangeMin)
                if dist == rangeMin:
                    self.checkSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, True)
                    return
            self.checkSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, False)
            return

    def showChargeSkillShine(self, skillId, isShow):
        self.uiAdapter.zaijuV2.showChargeSkillShine(skillId, isShow)
        for i, id in enumerate(self.getSkillId(ALL_SKILL)):
            if id == skillId:
                key = self._getKey(uiConst.SKILL_ACTION_BAR, i)
                if self.binding.has_key(key):
                    self.binding[key][0].Invoke('showToggleShine', GfxValue(isShow))

        for i in xrange(uiConst.MAX_ITEMBAR_SLOT):
            for page in [uiConst.ITEM_ACTION_BAR, uiConst.ITEM_ACTION_BAR2]:
                info = self.getShortCut(page, i)
                if info and info[1] == skillId:
                    key = self._getKey(page, i)
                    if self.binding.has_key(key):
                        self.binding[key][0].Invoke('showToggleShine', GfxValue(isShow))

    def refreshActionbar(self, isItemBar = True):
        if not self.mc or not self.wsMc or not hasattr(BigWorld.player(), 'shortcutData'):
            return
        p = BigWorld.player()
        if p._isSchoolSwitch():
            if p.school != p.realSchool or p.shortcutData:
                self.clientShortCut = copy.deepcopy(p.shortcutData)
        else:
            self.clientShortCut = copy.deepcopy(p.shortcutData)
        if self.mc:
            self.mc.Invoke('setCurrSchemeNo', GfxValue(self.currSchemeNo))
            self.mc.Invoke('showResetBtn', GfxValue(p._isSchoolSwitch()))
        if self.clientShortCut:
            self._changeSelfSkills()
        if self.clientShortCut == {} or p._isSchoolSwitch():
            self._checkSelfSkills()
        ws1selectedIds = []
        ws2selectedIds = []
        if self.currSchemeNo == uiConst.SHORT_CUT_CASE_1:
            ws1selectedIds = p.wushuang1.selectedWs
            ws2selectedIds = p.wushuang2.selectedWs
        elif self.currSchemeNo == uiConst.SHORT_CUT_CASE_2:
            ws1selectedIds = p.wushuang1.selectedWs1
            ws2selectedIds = p.wushuang2.selectedWs1
        elif self.currSchemeNo == uiConst.SHORT_CUT_CASE_3:
            ws1selectedIds = p.wushuang1.selectedWs2
            ws2selectedIds = p.wushuang2.selectedWs2
        if not p._isSchoolSwitch():
            for k, v in self.getWuShuangSkillShortCut().items():
                inSelected = False
                for skillId in ws1selectedIds:
                    if skillId == v[1]:
                        inSelected = True
                        break

                for skillId in ws2selectedIds:
                    if skillId == v[1]:
                        inSelected = True
                        break

                if not inSelected:
                    self.clientShortCut.pop(k)

        if self.clientShortCut.has_key(p.getOperationMode()):
            info = self.clientShortCut[p.getOperationMode()]
            for i in (gameglobal.KEYBOARD_MODE, gameglobal.MOUSE_MODE, gameglobal.ACTION_MODE):
                if not self.clientShortCut.has_key(i):
                    self.clientShortCut[i] = copy.deepcopy(info)

        filterSkills = [ skId for skId, needShow in SSGD.data.get(p._getSchoolSwitchNo(), {}).get('skillShows', []) ]
        if p._isSchoolSwitch() and p.school == p.realSchool:
            for key, value in self.clientShortCut.items():
                if isinstance(key, tuple) and key[0] != uiConst.SHORTCUT_TYPE_SKILL and value[1] not in filterSkills:
                    self.clientShortCut.pop(key)

        self.skillStates = {}
        self.refreshAllActionbar(True)
        if isItemBar:
            self.refreshAllItembar(True)
        self.refreshAllWuShuangbar()
        self.initAllSkillStat()
        self.updateSlots()
        if self.needRefreshCenter:
            self.setSchoolCenter()
            self.needRefreshCenter = False
        self.validateSlotVisible()
        if self.needSaveClientCut:
            BigWorld.player().saveShortcut(self.clientShortCut)
            self.needSaveClientCut = False

    def setCurrSchemeNo(self, currNo):
        self.currSchemeNo = currNo
        if self.mc:
            self.mc.Invoke('setCurrSchemeNo', GfxValue(currNo))

    def getCurrSchemeNo(self):
        return self.currSchemeNo

    def _changeSelfSkills(self):
        if not self.clientShortCut.has_key(gameglobal.KEYBOARD_MODE):
            tempData = {}
            for item in self.clientShortCut.keys():
                if isinstance(item, tuple):
                    page, pos = item
                    if page == uiConst.SKILL_ACTION_BAR and pos < uiConst.WUSHUANG_SKILL_START_POS_LEFT:
                        tempData[item] = self.clientShortCut[item]
                        self.clientShortCut.pop(item)

            self.clientShortCut[gameglobal.KEYBOARD_MODE] = tempData
            self.clientShortCut[gameglobal.MOUSE_MODE] = copy.deepcopy(tempData)
            self.clientShortCut[gameglobal.ACTION_MODE] = copy.deepcopy(tempData)

    def _sortSkillList(self):
        p = BigWorld.player()
        skills = [ skId for skId, needShow in SSGD.data.get(p._getSchoolSwitchNo(), {}).get('skillShows', []) ]
        skillList = []
        for skillId in p.getSkills().keys():
            if skillId in skills:
                skillList.append([skillId, skills.index(skillId)])
            else:
                skillList.append([skillId, len(p.getSkills().keys())])

        skillList.sort(key=lambda k: k[1])
        skillList = [ skillId for skillId, idx in skillList ]
        return skillList

    def _checkSelfSkills(self):
        p = BigWorld.player()
        skillList = self._sortSkillList()
        filterDict = {}
        if p._isSchoolSwitch():
            filterDict = {skId:needShow for skId, needShow in SSGD.data.get(p._getSchoolSwitchNo(), {}).get('skillShows', [])}
        for key, val in self.getAllSkillShortCut().items():
            if val[0] == uiConst.SHORTCUT_TYPE_SKILL and val[1] not in skillList:
                self.setShortCut(key[0], key[1], (uiConst.SHORTCUT_TYPE_NONE, 0))

        for skillId in skillList:
            isInShortCut = False
            for val in self.getAllSkillShortCut().values():
                if val[0] == uiConst.SHORTCUT_TYPE_SKILL and val[1] == skillId:
                    isInShortCut = True
                    break

            if not isInShortCut:
                sVal = p.getSkills().get(skillId, None)
                skillInfo = p.getSkillInfo(skillId, sVal.level)
                wsType = skillInfo.getSkillData('wsType', 1)
                sVal.wsType = wsType
                if skillInfo.hasSkillData('wsNeed1') or skillInfo.hasSkillData('wsNeed2'):
                    sVal.isWsSkill = True
                if sVal.isWsSkill:
                    if sVal.wsType == 1:
                        for pos in xrange(uiConst.WUSHUANG_SKILL_START_POS_LEFT, uiConst.WUSHUANG_SKILL_START_POS_RIGHT):
                            info = self.getShortCut(uiConst.SKILL_ACTION_BAR, pos)
                            if info:
                                if info[0] in (uiConst.SHORTCUT_TYPE_SKILL, uiConst.SHORTCUT_TYPE_NONE) and (info[1] == 0 or info[1] not in skillList):
                                    self.setShortCut(uiConst.SKILL_ACTION_BAR, pos, (uiConst.SHORTCUT_TYPE_SKILL, skillId))
                                    break
                            else:
                                self.setShortCut(uiConst.SKILL_ACTION_BAR, pos, (uiConst.SHORTCUT_TYPE_SKILL, skillId))
                                break

                    else:
                        for pos in xrange(uiConst.WUSHUANG_SKILL_START_POS_RIGHT, uiConst.WUSHUANG_SKILL_END_POS):
                            info = self.getShortCut(uiConst.SKILL_ACTION_BAR, pos)
                            if info:
                                if info[0] in (uiConst.SHORTCUT_TYPE_SKILL, uiConst.SHORTCUT_TYPE_NONE) and (info[1] == 0 or info[1] not in skillList):
                                    self.setShortCut(uiConst.SKILL_ACTION_BAR, pos, (uiConst.SHORTCUT_TYPE_SKILL, skillId))
                                    break
                            else:
                                self.setShortCut(uiConst.SKILL_ACTION_BAR, pos, (uiConst.SHORTCUT_TYPE_SKILL, skillId))
                                break

                else:
                    for pos in xrange(0, uiConst.WUSHUANG_SKILL_START_POS_LEFT):
                        info = self.getShortCut(uiConst.SKILL_ACTION_BAR, pos)
                        if info:
                            if info[0] in (uiConst.SHORTCUT_TYPE_SKILL, uiConst.SHORTCUT_TYPE_NONE) and info[1] == 0 or info[0] in (uiConst.SHORTCUT_TYPE_ITEM_COMSUME,
                             uiConst.SHORTCUT_TYPE_ITEM_EQUIP,
                             uiConst.SHORTCUT_TYPE_LIEF_SKILL,
                             uiConst.SHORTCUT_TYPE_EMOTE):
                                self.setShortCut(uiConst.SKILL_ACTION_BAR, pos, (uiConst.SHORTCUT_TYPE_SKILL, skillId))
                                break
                        elif filterDict.get(skillId, 0):
                            self.setShortCut(uiConst.SKILL_ACTION_BAR, pos, (uiConst.SHORTCUT_TYPE_SKILL, skillId))
                            break

    def refreshActionbarColor(self):
        school = BigWorld.player().realSchool
        wsType = [self.wsColorMap[school][0], self.wsColorMap[school][1]]
        if self.wsMc != None:
            self.wsMc.Invoke('refreshActionbarColor', uiUtils.array2GfxAarry(wsType))

    def showMouseIcon(self, bShow):
        if self.mc != None:
            self.mc.Invoke('showMouseIcon', GfxValue(bShow))
        gameglobal.rds.ui.airbar.showMouseIcon(bShow)

    def validRideItem(self, type, id):
        typeMap = ID.data.get(id, {}).get('rideItemType', 0)
        return typeMap == type

    def validEmoteItem(self, type, id):
        emoteIDs = EQD.data.get(id, {}).get('emoteIDs', [])
        return type in emoteIDs

    def onGetSchoolInfo(self, *arg):
        ret = self._createSchoolInfo()
        self.refreshAllActionbar(True)
        self.refreshAllItembar(True)
        self.initAllSkillStat()
        self.updateSlots()
        self.updateAllSummonedSprite()
        return uiUtils.dict2GfxDict(ret, True)

    def _createSchoolInfo(self):
        ret = {}
        p = BigWorld.player()
        ret['school'] = p.realSchool
        ret['tips'] = ''
        ret['state'] = 1
        schoolData = {}
        for key, value in CSD.data.items():
            if key[0] == p.realSchool:
                schoolData[key] = value

        if p.realSchool == const.SCHOOL_SHENTANG:
            ret['state'], ret['tips'], ret['swithIcon'] = self._isInSpecialMode(schoolData)
        elif p.realSchool == const.SCHOOL_YANTIAN:
            ret['state'], ret['tips'], ret['swithIcon'] = self._isInSpecialMode(schoolData)
        elif p.realSchool == const.SCHOOL_YUXU:
            ret['state'], ret['tips'], ret['emptyTips'], ret['swithIcon'] = self._getYuanLingState(schoolData)
            ret['num'] = p.ammoNum
        elif p.realSchool == const.SCHOOL_LINGLONG:
            ret['state'], ret['tips'], ret['swithIcon'] = self._isInSpecialMode(schoolData)
            ret['num'] = self._getLingQiNum(schoolData)
        elif p.realSchool == const.SCHOOL_GUANGREN:
            ret['state'], ret['tips'], ret['swithIcon'] = self._isInSpecialMode(schoolData)
            ret['zhanYi'] = p.zhanYi
            ret['maxZhanYi'] = self._getMaxZhanYi()
        elif p.realSchool == const.SCHOOL_LIUGUANG:
            ret['state'], ret['tips'], ret['swithIcon'] = self._isInSpecialMode(schoolData)
        elif p.realSchool == const.SCHOOL_YECHA:
            ret['state'], ret['tips'], ret['swithIcon'] = self._isInSpecialMode(schoolData)
            ret['num'] = self._getLingQiNum(schoolData)
        elif p.realSchool == const.SCHOOL_TIANZHAO:
            ret['state'], ret['tips'], ret['swithIcon'] = self._isInSpecialMode(schoolData)
            ret['tianZhaoState'] = 'tianzhaoSword'
        self.uiid = ret['state']
        return ret

    def setVirussafe(self, value, maxValue):
        if not self.wsMc:
            return
        self.wsMc.Invoke('setVirussafeValue', (GfxValue(value), GfxValue(maxValue)))

    def tweenVirussafe(self, now, time, marknum, maxVirussafe):
        if not self.wsMc:
            return
        self.wsMc.Invoke('tweenVirussafe', (GfxValue(now),
         GfxValue(time),
         GfxValue(marknum),
         GfxValue(maxVirussafe)))

    def stopTweenVirussafe(self):
        if not self.wsMc:
            return
        self.wsMc.Invoke('stopTweenVirussafe', ())

    def setYeChaVisible(self, hide):
        if not self.wsMc:
            return
        self.wsMc.Invoke('setYeChaVisible', GfxValue(hide))

    gameStrings.TEXT_ACTIONBARPROXY_3569

    def _getMaxZhanYi(self):
        zhanYiJueSkillId = 1303
        zhanyiMaxFixPart = 13
        zhanyiFixSkillId = 4309
        p = BigWorld.player()
        zhanYiList = SCFD.data.get('maxZhanYi', [])
        ret = zhanYiList[p.zhanYiLv - 1] if p.zhanYiLv <= len(zhanYiList) else 500
        sVal = p.skills.get(zhanYiJueSkillId, None)
        if sVal == None:
            return ret
        else:
            enhanceData = getattr(sVal, 'enhanceData', {})
            if enhanceData == {}:
                return ret
            if not enhanceData.has_key(zhanyiMaxFixPart):
                return ret
            lv = enhanceData[zhanyiMaxFixPart].enhancePoint
            skillInfo = PD.data.get((zhanyiFixSkillId, lv), None)
            if skillInfo == None:
                return ret
            scale = skillInfo.get('attrVal', 0)
            scale += 1
            return int(round(ret * scale))

    def _isInSpecialMode(self, data):
        p = BigWorld.player()
        defaultData = data.get((p.realSchool, 0, 0), {})
        if p.realSchool in (const.SCHOOL_LINGLONG,):
            for key, val in data.items():
                if p.ammoType == val['specialStateId']:
                    return (val['UIId'], val['desc'], val.get('swithIcon', 0))

        else:
            if p.statesServerAndOwn == {}:
                return (defaultData.get('UIId', 1), defaultData.get('desc', ''), defaultData.get('swithIcon', 0))
            states = p.statesServerAndOwn.keys()
            for state in states:
                for key, val in data.items():
                    if state == val['stateId']:
                        return (val['UIId'], val['desc'], val.get('swithIcon', 0))

        return (defaultData.get('UIId', 1), defaultData.get('desc', ''), defaultData.get('swithIcon', 0))

    def _getYuanLingState(self, data):
        p = BigWorld.player()
        UIId = 0
        desc = ''
        emptyDesc = ''
        buffId = 0
        swithIcon = 0
        for key, val in data.items():
            if p.ammoType == val['specialStateId']:
                UIId, desc, buffId, swithIcon = (val['UIId'],
                 val['desc'],
                 val['stateId'],
                 val.get('swithIcon', 0))
                break

        if buffId:
            emptyDesc = CSD.data.get((p.realSchool, 0, buffId), {}).get('desc')
        return (UIId,
         desc,
         emptyDesc,
         swithIcon)

    def _getLingQiNum(self, data):
        return BigWorld.player().ammoNum

    @ui.callAfterTime(0.1)
    def setSchoolCenter(self):
        oldUIId = self.uiid
        ret = self._createSchoolInfo()
        if self.wsMc != None:
            self.wsMc.Invoke('setSchoolInfo', uiUtils.dict2GfxDict(ret, True))
        if ret['swithIcon'] and self.uiid != oldUIId:
            self.refreshAllActionbar(True)
            self.refreshItemBarSkills(True)
            self.initAllSkillStat()
            self.updateSlots()

    def onGetLockState(self, *arg):
        return GfxValue(self.isLock)

    def onSetLockState(self, *arg):
        self.isLock = arg[3][0].GetBool()
        AppSettings[ASAP_LOCK] = 1 if self.isLock else 0
        lEvent = Event(events.EVENT_ACTIONBAR_LOCK, {'lockSrc': self.type,
         'locked': self.isLock})
        self.dispatchEvent(lEvent)

    @ui.uiEvent(uiConst.WIDGET_ACTION_BARS, events.EVENT_ACTIONBAR_LOCK)
    def onEventLockChanged(self, event):
        if event.data['lockSrc'] == self.type:
            return
        self.isLock = event.data['locked']
        AppSettings[ASAP_LOCK] = 1 if self.isLock else 0
        if self.mc:
            self.mc.Invoke('refreshLockState')

    def shortCutCanResetCheck(self):
        p = BigWorld.player()
        if not p._isSchoolSwitch():
            return False
        if self.isLock:
            p.showGameMsg(GMDD.data.ACTIONBAR_LOCKED, ())
            return False
        return True

    def onResetShortCut(self, *arg):
        if not self.shortCutCanResetCheck():
            return
        msg = gameStrings.TEXT_ACTIONBARPROXY_3689
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._doResetShortCut))

    def onChangeSkillCase(self, *args):
        case = int(args[3][0].GetNumber())
        BigWorld.player().cell.switchShortcutScheme(case)

    @ui.callInCD(1.1)
    def onChangeEquip(self, *args):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableOneKeyConfig', False):
            return
        if p.lv < SCD.data.get('oneKeyConfigMinLv', 59):
            p.showGameMsg(GMDD.data.ONE_KEY_CONFIG_BAN_LV, ())
            return
        if BigWorld.player().rebalanceMode > 0:
            p.showGameMsg(GMDD.data.FB_UNDER_BALANCE_MODE_CANNOT_DO_MSG, ())
            return
        allowOneKeyConfig = MCD.data.get(p.mapID, {}).get('allowOneKeyConfig', 0)
        if not allowOneKeyConfig:
            p.showGameMsg(GMDD.data.ONE_KEY_CONFIG_BAN_MAP, ())
            return
        gameglobal.rds.ui.quickReplaceEquipment.show()

    def onGetOneKeyConfig(self, *args):
        enableOneKeyConfig = gameglobal.rds.configData.get('enableOneKeyConfig', False)
        return GfxValue(enableOneKeyConfig)

    def setOneKeyConfigBtn(self):
        if self.mc:
            self.mc.Invoke('setOneKeyConfigBtn')

    def _doResetShortCut(self):
        if not self.shortCutCanResetCheck():
            return
        p = BigWorld.player()
        self.clientShortCut = {}
        p.saveShortcut(self.clientShortCut)
        self.refreshActionbar()

    def _getItemType(self, item):
        sType = uiConst.SHORTCUT_TYPE_NONE
        if item.type == item.BASETYPE_EQUIP:
            sType = uiConst.SHORTCUT_TYPE_ITEM_EQUIP
        elif item.type == item.BASETYPE_CONSUMABLE:
            sType = uiConst.SHORTCUT_TYPE_ITEM_COMSUME
        return sType

    def _createInitActionbarData(self, switch = False):
        p = BigWorld.player()
        ret = []
        for pos in xrange(uiConst.MAX_ACTIONBAR_SLOT_NUM):
            self.clearShineState(uiConst.SKILL_ACTION_BAR, pos)
            info = self.getShortCut(uiConst.SKILL_ACTION_BAR, pos)
            if not info:
                self._setItemSlotState(uiConst.SKILL_ACTION_BAR, pos, uiConst.SKILL_ICON_STAT_USEABLE)
                self.setSlotColor(uiConst.SKILL_ACTION_BAR, pos, 'nothing')
                ret.append(None)
                continue
            typeId = info[0]
            idx = info[1]
            if typeId == uiConst.SHORTCUT_TYPE_ITEM_COMSUME and idx in self.otherSkill:
                iconPath = self._getSkillIcon(idx)
                name = self._getSkillIcon(idx)
                obj = {'iconPath': iconPath,
                 'name': name}
                ret.append(obj)
                isInHorse = p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
                self.setRideShine(isInHorse, uiConst.HORSE_RIDING)
                self.setRideShine(p.inFlyTypeWing(), uiConst.WING_FLYING)
                continue
            if typeId == uiConst.SHORTCUT_TYPE_LIEF_SKILL and idx in self.lifeSkill:
                lifeSkillIcons = SCFD.data.get('lifeSkillIcons', {})
                if lifeSkillIcons.has_key(idx):
                    icon = lifeSkillIcons[idx]
                else:
                    curLifeSkillId = uiUtils.getCurLifeSkill(idx)
                    if curLifeSkillId == (None, None):
                        curLifeSkillId = (idx, 0)
                    lifeSkillData = LSD.data.get(curLifeSkillId, {})
                    icon = lifeSkillData.get('icon', '')
                iconPath = 'lifeskill/icon64/' + str(icon) + iconSuffix
                obj = {'iconPath': iconPath}
                ret.append(obj)
                continue
            if typeId == uiConst.SHORTCUT_TYPE_EMOTE:
                iconPath = gameglobal.rds.ui.emoteAction.getEmotePath(info[1])
                obj = {'iconPath': iconPath}
                ret.append(obj)
                continue
            if typeId == uiConst.SHORTCUT_TYPE_SKILL_MACRO:
                macroInfo = p.getMacroInfoById(info[1])
                iconPath = ''
                if macroInfo:
                    macroInfo.macroId and self.modifyItemByMacroId(macroInfo.macroId)
                    iconPath = gameglobal.rds.ui.skillMacroOverview.getIconPathByInfo(macroInfo)
                else:
                    iconPath = 'item/icon64/notFound.dds'
                obj = {'iconPath': iconPath}
                ret.append(obj)
                continue
            if typeId == uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE:
                iconPath = gameglobal.rds.ui.summonedWarSpriteGuard.getSpriteIconPath(int(info[1][1]))
                obj = {'iconPath': iconPath}
                ret.append(obj)
                continue
            item = self.getItemByBarPagePos(uiConst.SKILL_ACTION_BAR, pos)
            if type(item) == Item:
                iconPath = uiUtils.getItemIconFile40(item.id)
                count = min(999, self.getCountByType(item))
                obj = {'iconPath': iconPath,
                 'count': count}
                ret.append(obj)
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                self.setSlotColor(uiConst.SKILL_ACTION_BAR, pos, color)
                self.playCooldown(uiConst.SKILL_ACTION_BAR, pos, item.id)
                if not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                    self._setItemSlotState(uiConst.SKILL_ACTION_BAR, pos, uiConst.SKILL_ICON_STAT_RED)
                else:
                    self._setItemSlotState(uiConst.SKILL_ACTION_BAR, pos, uiConst.SKILL_ICON_STAT_USEABLE)
            else:
                info = self.getShortCut(uiConst.SKILL_ACTION_BAR, pos, (0, 0))
                if len(info) == 3:
                    optionId = info[2]
                else:
                    optionId = 0
                self.setSlotColor(uiConst.SKILL_ACTION_BAR, pos, 'nothing')
                if optionId:
                    shortCutWithParamIcon = SGTD.data.get(info[1], {}).get('shortCutWithParamIcon', ())
                    offset = optionId % uiConst.SKILL_SHORT_CUT_BASE
                    if offset < len(shortCutWithParamIcon):
                        icon = shortCutWithParamIcon[offset]
                    else:
                        icon = 0
                    iconPath = skillIconPath + str(icon) + iconSuffix
                elif switch:
                    iconPath = self._getSwithIcon(info[1])
                else:
                    iconPath = self._getSkillIcon(info[1])
                name = self._getSkillIcon(info[1])
                obj = {'iconPath': iconPath}
                ret.append(obj)

        return ret

    def refreshAllActionbar(self, switch = False):
        if self.mc:
            self.mc.Invoke('setCurrSchemeNo', GfxValue(self.currSchemeNo))
            self.mc.Invoke('setActionbarData', uiUtils.array2GfxAarry(self._createInitActionbarData(switch), True))

    def onGetInitActionbarData(self, *arg):
        ret = self._createInitActionbarData()
        self.initAllSkillStat()
        self.updateSlots()
        return uiUtils.array2GfxAarry(ret, True)

    def _createWuShuangbarData(self):
        ret = []
        for pos in xrange(uiConst.WUSHUANG_SKILL_START_POS_LEFT, uiConst.WUSHUANG_SKILL_END_POS):
            info = self.getShortCut(uiConst.SKILL_ACTION_BAR, pos, (0, 0))
            self._setItemSlotState(uiConst.SKILL_ACTION_BAR, pos, uiConst.SKILL_ICON_STAT_USEABLE)
            if not info:
                ret.append({})
                continue
            if info[1] == 0:
                if self.wsMc != None:
                    self.wsMc.Invoke('setSlotStar', (GfxValue(pos), GfxValue(0)))
                obj = {}
            else:
                iconPath = self._getSkillIcon(info[1])
                obj = {'iconPath': iconPath}
                starVal = self._getWsSkillStar(info[1])
                if self.wsMc != None:
                    self.wsMc.Invoke('setSlotStar', (GfxValue(pos), GfxValue(starVal)))
            ret.append(obj)

        return ret

    def refreshAllWuShuangbar(self):
        if self.wsMc:
            self.wsMc.Invoke('setWuShuangBarData', uiUtils.array2GfxAarry(self._createWuShuangbarData(), True))
        gameglobal.rds.ui.skill._initWsSkillList()

    def onGetInitWuShuangbarData(self, *arg):
        ret = self._createWuShuangbarData()
        self.initAllSkillStat()
        self.updateSlots()
        return uiUtils.array2GfxAarry(ret, True)

    def _createInitItembarData(self, switch = False, itemType = 0):
        p = BigWorld.player()
        ret = []
        nowBarType = uiConst.ITEM_ACTION_BAR
        if itemType:
            nowBarType = uiConst.ITEM_ACTION_BAR2
        if p._isSchoolSwitch():
            itemBarIcons = []
            isEmpty = True
            for pos in xrange(uiConst.MAX_ITEMBAR_SLOT):
                info = self.getShortCut(nowBarType, pos, (0, 0))
                if info[1]:
                    isEmpty = False
                itemBarIcons.append(info)

            if isEmpty:
                itemBarIcons = SSGD.data.get(p._getSchoolSwitchNo(), {}).get('itemBarIcons', ())
        for pos in xrange(uiConst.MAX_ITEMBAR_SLOT):
            self.clearShineState(nowBarType, pos)
            if p._isSchoolSwitch():
                self._setItemSlotState(nowBarType, pos, uiConst.SKILL_ICON_STAT_USEABLE)
                if pos >= len(itemBarIcons):
                    typeId = 0
                    idx = 0
                else:
                    typeId = itemBarIcons[pos][0]
                    idx = itemBarIcons[pos][1]
                    self.setShortCut(nowBarType, pos, (typeId, idx))
            else:
                info = self.getShortCut(nowBarType, pos, (0, 0))
                if not info:
                    self._setItemSlotState(nowBarType, pos, uiConst.SKILL_ICON_STAT_USEABLE)
                    ret.append({})
                    continue
                typeId = info[0]
                idx = info[1]
            if typeId == uiConst.SHORTCUT_TYPE_SKILL_MACRO:
                macroInfo = p.getMacroInfoById(info[1])
                iconPath = ''
                if macroInfo:
                    macroInfo.macroId and self.modifyItemByMacroId(macroInfo.macroId)
                    iconPath = gameglobal.rds.ui.skillMacroOverview.getIconPathByInfo(macroInfo)
                else:
                    iconPath = 'item/icon64/notFound.dds'
                obj = {'iconPath': iconPath}
                ret.append(obj)
                continue
            if typeId == uiConst.SHORTCUT_TYPE_ITEM_COMSUME and idx in self.otherSkill:
                iconPath = self._getSkillIcon(idx)
                name = self._getSkillIcon(idx)
                obj = {'iconPath': iconPath,
                 'name': name}
                ret.append(obj)
                isInHorse = p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
                self.setRideShine(isInHorse, uiConst.HORSE_RIDING)
                self.setRideShine(p.inFlyTypeWing(), uiConst.WING_FLYING)
                continue
            if typeId == uiConst.SHORTCUT_TYPE_LIEF_SKILL and idx in self.lifeSkill:
                lifeSkillIcons = SCFD.data.get('lifeSkillIcons', {})
                if lifeSkillIcons.has_key(idx):
                    icon = lifeSkillIcons[idx]
                else:
                    curLifeSkillId = uiUtils.getCurLifeSkill(idx)
                    if curLifeSkillId == (None, None):
                        curLifeSkillId = (idx, 0)
                    lifeSkillData = LSD.data.get(curLifeSkillId, {})
                    icon = lifeSkillData.get('icon', '')
                iconPath = 'lifeskill/icon64/' + str(icon) + iconSuffix
                obj = {'iconPath': iconPath}
                ret.append(obj)
                continue
            if typeId == uiConst.SHORTCUT_TYPE_EMOTE:
                iconPath = gameglobal.rds.ui.emoteAction.getEmotePath(info[1])
                obj = {'iconPath': iconPath}
                ret.append(obj)
                continue
            if typeId == uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE:
                iconPath = gameglobal.rds.ui.summonedWarSpriteGuard.getSpriteIconPath(int(info[1][1]))
                obj = {'iconPath': iconPath}
                ret.append(obj)
                continue
            item = self.getItemByBarPagePos(nowBarType, pos)
            if type(item) == Item:
                iconPath = uiUtils.getItemIconFile40(item.id)
                count = min(999, self.getCountByType(item))
                obj = {'iconPath': iconPath,
                 'count': count}
                ret.append(obj)
                if hasattr(item, 'quality'):
                    quality = item.quality
                else:
                    quality = ID.data.get(item.id, {}).get('quality', 1)
                color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                self.setSlotColor(nowBarType, pos, color)
                self.playCooldown(nowBarType, pos, item.id)
                if not item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                    self._setItemSlotState(nowBarType, pos, uiConst.SKILL_ICON_STAT_RED)
                else:
                    self._setItemSlotState(nowBarType, pos, uiConst.SKILL_ICON_STAT_USEABLE)
            else:
                self.setSlotColor(nowBarType, pos, 'nothing')
                if switch:
                    iconPath = self._getSwithIcon(idx)
                else:
                    iconPath = self._getSkillIcon(idx)
                name = self._getSkillIcon(idx)
                obj = {'iconPath': iconPath}
                ret.append(obj)

        return ret

    def refreshAllItembar(self, switch = False):
        for i in xrange(2):
            if self.itemMc[i]:
                self.itemMc[i].Invoke('setInitData', uiUtils.array2GfxAarry(self._createInitItembarData(switch, i), True))

    def onGetInitItembarData(self, *arg):
        widgetType = int(arg[3][0].GetNumber())
        ret = self._createInitItembarData(False, widgetType)
        self.initAllSkillStat()
        self.updateSlots()
        return uiUtils.array2GfxAarry(ret, True)

    def changeIcon(self, srcSkillId, dstSkillId):
        iconPath = self._getSwithIcon(dstSkillId)
        data = {'iconPath': iconPath}
        keys = self._getPosByActionID(srcSkillId)
        keyText = ''
        for key in keys:
            if self.binding.has_key(key):
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
                self.binding[key][0].Invoke('qteActivate', GfxValue(srcSkillId != dstSkillId))
                keyIndex = self.getSlotID(key)[1]
                if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE and keyIndex in (10, 11):
                    keyText = '-' if keyIndex == 10 else '='
                else:
                    keyText = self.slotKey[keyIndex]

        self.updateSlots()
        return keyText

    def changeWsBarState(self, isChange = False):
        if self.wsMc:
            self.wsMc.Invoke('changeWsBarState', GfxValue(isChange))

    def cancelCooldownCallback(self, skillId):
        pos = self._getPosByActionID(skillId)
        if len(pos) and pos[0] in self.callbackHandler:
            BigWorld.cancelCallback(self.callbackHandler[pos[0]])

    def clearShineState(self, page, pos):
        key = self._getKey(page, pos)
        if self.binding.has_key(key):
            self.binding[key][0].Invoke('showToggleShine', GfxValue(False))

    def showWSShine(self):
        if self.wsMc:
            self.wsMc.Invoke('showWSShine')

    def _getSwithIcon(self, skillId, skillLv = 1, icon64 = False):
        p = BigWorld.player()
        if icon64:
            path = skillIconPath64
        else:
            path = skillIconPath
        if SSCD.data.has_key((skillId, p.ammoType)):
            icon = SSCD.data.get((skillId, p.ammoType), {}).get('icon', None)
            if icon:
                return path + str(icon) + iconSuffix
            else:
                return self._getSkillIcon(skillId, skillLv, icon64)
        states = p.statesServerAndOwn.keys()
        for state in states:
            icon = None
            if hasattr(p, 'skillAppearancesDetail'):
                appearanceId = p.skillAppearancesDetail.getCurrentAppearance(skillId)
                if appearanceId <= 0:
                    icon = SSCD.data.get((skillId, state), {}).get('icon', None)
                else:
                    skillStateInfo = p.skillAppearancesDetail.getCurrentStateSkillInfo(skillId, skillLv, state)
                    icon = skillStateInfo.getSkillData('icon', None)
            elif SSCD.data.has_key((skillId, state)):
                icon = SSCD.data.get((skillId, state), {}).get('icon', None)
            if icon:
                return path + str(icon) + iconSuffix

        return self._getSkillIcon(skillId, skillLv, icon64)

    def addNewSkill(self, skillId):
        for pos in xrange(uiConst.MAX_ACTIONBAR_SLOT_NUM):
            info = self.getShortCut(uiConst.SKILL_ACTION_BAR, pos, [0, 0])
            if info[1] == 0:
                self.setItem(skillId, uiConst.SKILL_ACTION_BAR, pos, False, False, info[0])
                return

    def clearGuildSkillShortCut(self):
        self._clearGuildSkillInBar(uiConst.SKILL_ACTION_BAR)
        self._clearGuildSkillInBar(uiConst.ITEM_ACTION_BAR)
        self._clearGuildSkillInBar(uiConst.ITEM_ACTION_BAR2)
        BigWorld.player().saveShortcut(self.clientShortCut)
        self.updateSlots()

    def _clearGuildSkillInBar(self, barIdx):
        myGuildSkills = BigWorld.player().guildMemberSkills.keys()
        for pos in xrange(uiConst.MAX_ITEMBAR_SLOT):
            info = self.getShortCut(barIdx, pos, (0, 0))
            if not info:
                continue
            typeId = info[0]
            skillId = info[1]
            if typeId != uiConst.SHORTCUT_TYPE_SKILL:
                continue
            if not skillId:
                continue
            if skillId not in uiConst.GUILD_SKILL_ALL:
                continue
            if skillId not in myGuildSkills:
                self.removeItem(barIdx, pos)

    def checkEquipSkillCoolDown(self, equipItemId, uuid):
        equipItem = self.checkEquipmentByIdAndUuid(equipItemId, uuid)
        if not equipItem:
            equipItem, _, _ = BigWorld.player().inv.findItemByUUID(uuid)
        if equipItem and self.checkHasEquipSkillItem(equipItem):
            if hasattr(equipItem, 'skillNst'):
                nextTime = equipItem.skillNst
                remain = nextTime - utils.getNow()
                skId, skLevel = self._getEquipSkillInfo(equipItem)
                total = SGD.data.get((skId, skLevel), {}).get('cd', 1)
                return (remain, total)
        return (0, 1)

    def _getEquipSkillInfo(self, item):
        if not item:
            return (0, 0)
        if item.isYaoPei():
            yaoPeiSkillId = getattr(item, 'yaoPeiSkillId', 0)
            if yaoPeiSkillId != 0:
                yaopeiLv = item.getYaoPeiLv()
                yaopeiSkillLv = YLD.data.get(yaopeiLv, {}).get('skillLv', 0)
                return (yaoPeiSkillId, yaopeiSkillLv)
        return (0, 0)

    def addGuideEffect(self, skillId):
        key = self._getPosByActionID(skillId)
        for item in key:
            bar, slot = self.getSlotID(item)
            keyboardEffect.addGuideEffect(bar, slot)

    def refreshItemBarSkills(self, switch = False):
        self.refreshSkillsInItemBar(uiConst.ITEM_ACTION_BAR, switch)
        self.refreshSkillsInItemBar(uiConst.ITEM_ACTION_BAR2, switch)

    def getActionbarMc(self, barIdx):
        if barIdx == uiConst.ITEM_ACTION_BAR:
            if self.itemMc:
                return self.itemMc[0]
            return None
        elif barIdx == uiConst.ITEM_ACTION_BAR2:
            if self.itemMc:
                return self.itemMc[1]
            return None
        elif barIdx == uiConst.SKILL_ACTION_BAR:
            return self.mc
        else:
            return None

    def refreshSkillsInItemBar(self, barIdx, switch):
        refreshData = []
        barMc = self.getActionbarMc(barIdx)
        if not barMc:
            return
        for pos in xrange(uiConst.MAX_ITEMBAR_SLOT):
            info = self.getShortCut(barIdx, pos, (0, 0))
            if not info:
                continue
            typeId = info[0]
            skillId = info[1]
            if typeId != uiConst.SHORTCUT_TYPE_SKILL:
                continue
            if not skillId:
                continue
            if switch:
                iconPath = self._getSwithIcon(skillId)
            else:
                iconPath = self._getSkillIcon(skillId)
            skillData = {}
            skillData['pos'] = pos
            skillData['iconPath'] = iconPath
            refreshData.append(skillData)

        if len(refreshData) <= 0:
            return
        barMc.Invoke('refreshItemBar', uiUtils.array2GfxAarry(refreshData, True))

    def setItem(self, idAction, idBar, idSlot, isRefresh = True, isReset = False, sType = uiConst.SHORTCUT_TYPE_NONE, option = 0):
        key = self._getKey(idBar, idSlot)
        if not self.binding.has_key(key):
            return
        if idBar not in uiConst.ACTION_BARS:
            return
        if idBar == uiConst.EQUIP_ACTION_BAR:
            actionSlot = EquipActionSlot(self, sType, idAction)
        elif sType == uiConst.SHORTCUT_TYPE_ITEM_COMSUME and idAction in self.otherSkill:
            actionSlot = GeneralSkillActionSlot(self, sType, idAction)
        elif sType == uiConst.SHORTCUT_TYPE_LIEF_SKILL and idAction in self.lifeSkill:
            actionSlot = LifeSkillActionSlot(self, sType, idAction)
        elif sType == uiConst.SHORTCUT_TYPE_EMOTE and idAction in ED.data.keys():
            actionSlot = EmoteActionSlot(self, sType, idAction)
        elif sType == uiConst.SHORTCUT_TYPE_SKILL:
            actionSlot = SkillActionSlot(self, sType, idAction)
            actionSlot.updateShortCut = not isRefresh
            actionSlot.option = option
        elif type(idAction) == Item:
            actionSlot = ItemActionSlot(self, sType, idAction)
            actionSlot.isReset = isReset
        elif sType == uiConst.SHORTCUT_TYPE_SKILL_MACRO:
            actionSlot = SkillMacroActionSlot(self, sType, idAction)
            actionSlot.updateShortCut = not isRefresh
        elif sType == uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE:
            actionSlot = SummonedSpriteActionSlot(self, sType, idAction)
            actionSlot.updateShortCut = not isRefresh
        else:
            actionSlot = ActionSlot(self, sType, idAction)
        actionSlot.setSlotItem(idBar, idSlot)

    def getFirstTimeKey(self, mode):
        return 'op' + str(mode)

    def isInitOperation(self):
        key0 = self.getFirstTimeKey(0)
        key1 = self.getFirstTimeKey(1)
        key2 = self.getFirstTimeKey(2)
        return not self.clientShortCut.get(key0) and not self.clientShortCut.get(key1) and not self.clientShortCut.get(key2)

    def isFirstTimeOperation(self, mode):
        key = self.getFirstTimeKey(mode)
        return not self.clientShortCut.get(key)

    def setFirstTimeOperation(self, mode, value):
        key = self.getFirstTimeKey(mode)
        self.clientShortCut[key] = value
        BigWorld.player().saveShortcut(self.clientShortCut)

    def switchClientShortCut(self, mode, oldMode):
        self.clientShortCut[mode] = copy.deepcopy(self.clientShortCut.get(oldMode, {}))
        BigWorld.player().shortcutData[mode] = copy.deepcopy(BigWorld.player().shortcutData.get(oldMode, {}))
        BigWorld.player().saveShortcut(self.clientShortCut)

    def onRefreshSchoolStateKBE(self, *args):
        school = int(args[3][0].GetNumber())
        state = int(args[3][1].GetNumber())
        keyboardEffect.updateBaseColor(school, state)

    def updateAllSummonedSprite(self):
        ret = []
        p = BigWorld.player()
        operationMode = p.getOperationMode()
        for key, value in self.clientShortCut.iteritems():
            if isinstance(value, tuple) and value[0] == uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE:
                ret.append((key, value[1]))

        if self.clientShortCut.has_key(operationMode):
            data = self.clientShortCut[operationMode]
            for key, value in data.iteritems():
                if value[0] == uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE:
                    ret.append((key, value[1]))

        for key, value in ret:
            page, pos = key
            spriteIndex, spriteId = value
            self.setItem((spriteIndex, spriteId), page, pos, True, False, uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE)

    def refreshSummonedSprite(self, spriteIndex):
        ret = []
        p = BigWorld.player()
        operationMode = p.getOperationMode()
        spriteId = None
        for key, value in self.clientShortCut.iteritems():
            if isinstance(value, tuple) and value[0] == uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE and value[1][0] == spriteIndex:
                ret.append(key)
                spriteId = value[1][1]

        if self.clientShortCut.has_key(operationMode):
            data = self.clientShortCut[operationMode]
            for key, value in data.iteritems():
                if value[0] == uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE and value[1][0] == spriteIndex:
                    ret.append(key)
                    spriteId = value[1][1]

        for page, pos in ret:
            self.setItem((spriteIndex, spriteId), page, pos, True, False, uiConst.SHORTCUT_TYPE_SUMMONED_SPRITE)


class ActionSlot(object):

    def __init__(self, proxy, sType, actionId):
        self.actionId = actionId
        self.proxy = proxy
        self.sType = sType
        self.updateShortCut = False

    def setSlotItem(self, idBar, idSlot):
        self.proxy._setItemSlotState(idBar, idSlot, uiConst.SKILL_ICON_STAT_USEABLE)
        self.proxy.setSlotColor(idBar, idSlot, 'nothing')
        self.proxy.stopCoolDown(idBar, idSlot)
        data = {}
        key = self.proxy._getKey(idBar, idSlot)
        if self.actionId:
            iconPath = self.getSlotIconPath()
            data['name'] = iconPath
            data['iconPath'] = iconPath
            data.update(self.extraSlotData())
            self.proxy.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data, True))
        self.proxy.binding[key][0].Invoke('showToggleShine', GfxValue(self.showToggleShine()))
        self.proxy.validateSlotVisible()
        if hasattr(self.proxy, 'updateSlots'):
            self.proxy.updateSlots()
        self.setShortCut(idBar, idSlot)

    def getSlotIconPath(self):
        return self.proxy._getSkillIcon(self.actionId)

    def extraSlotData(self):
        return {}

    def slotShortCut(self):
        return (self.sType, self.actionId)

    def showToggleShine(self):
        return False

    def setShortCut(self, idBar, idSlot):
        self.proxy.setShortCut(idBar, idSlot, self.slotShortCut())


class EquipActionSlot(ActionSlot):

    def setSlotItem(self, page, pos):
        if not self.actionId:
            gameglobal.rds.ui.roleInfo.setSlotState(pos, uiConst.ITEM_NORMAL)
            return
        item = self.actionId
        itemInfo = uiUtils.getGfxItem(item)
        itemInfo['state'] = gameglobal.rds.ui.roleInfo.calcSlotState(item, False)
        key = self.proxy._getKey(page, pos)
        self.proxy.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(itemInfo, True))
        self.proxy.refreshByBagUse(item)


class GeneralSkillActionSlot(ActionSlot):

    def showToggleShine(self):
        p = BigWorld.player()
        if self.actionId == uiConst.HORSE_RIDING:
            return p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
        if self.actionId == uiConst.WING_FLYING:
            return p.inFlyTypeWing()
        if self.actionId == uiConst.DAZUOING:
            return p.inDaZuo()
        if self.actionId == uiConst.BOOTH:
            return p.inBoothing()
        if self.actionId == uiConst.COUPLEEMOTE:
            return p.isInCoupleRide()
        if self.actionId == uiConst.RIDE_TOGETHER:
            pass
        if self.actionId == uiConst.LING_SHI_FLAG_SWITCH:
            return bool(p.lingShiFlag)
        return False


class LifeSkillActionSlot(ActionSlot):

    def getSlotIconPath(self):
        skillId = self.actionId
        lifeSkillIcons = SCFD.data.get('lifeSkillIcons', {})
        if lifeSkillIcons.has_key(skillId):
            icon = lifeSkillIcons[skillId]
        else:
            curLifeSkillId = uiUtils.getCurLifeSkill(skillId)
            if curLifeSkillId == (None, None):
                curLifeSkillId = (skillId, 0)
            lifeSkillData = LSD.data.get(curLifeSkillId, {})
            icon = lifeSkillData.get('icon', '')
        return 'lifeskill/icon64/' + str(icon) + iconSuffix


class EmoteActionSlot(ActionSlot):

    def showToggleShine(self):
        if ED.data.get(self.actionId).get('funcType') == uiConst.EMOTE_FUNTYPE_COUPLE_EMOTE:
            return bool(BigWorld.player().isInCoupleRide())
        return False

    def getSlotIconPath(self):
        return gameglobal.rds.ui.emoteAction.getEmotePath(self.actionId)

    def setSlotItem(self, page, pos):
        super(EmoteActionSlot, self).setSlotItem(page, pos)


class SkillActionSlot(ActionSlot):

    def __init__(self, proxy, sType, actionId):
        super(SkillActionSlot, self).__init__(proxy, sType, actionId)
        self.updateShortCut = False
        self.option = 0

    def setSlotItem(self, page, pos):
        super(SkillActionSlot, self).setSlotItem(page, pos)
        skillId = self.actionId
        if uiConst.WUSHUANG_SKILL_START_POS_LEFT <= pos <= uiConst.WUSHUANG_SKILL_END_POS:
            starVal = self.proxy._getWsSkillStar(skillId)
            self.proxy.wsMc.Invoke('setSlotStar', (GfxValue(pos), GfxValue(starVal)))
            self.proxy.setSpecialSlotShine()
        self.proxy.updateSlots()
        self.proxy.showWuShuangAnimation()
        if self.hasSwitchSkill(skillId):
            self.proxy.showToggleShine({})
        if skillId == 0:
            self.proxy._setSlotState(pos, uiConst.SKILL_ICON_STAT_USEABLE)
        else:
            self.proxy.initSkillStat(skillId)
        if self.updateShortCut:
            BigWorld.player().saveShortcut(self.proxy.clientShortCut)

    def hasSwitchSkill(self, skill):
        if self.proxy.switchSkill:
            for stateId, skillId in self.proxy.switchSkill:
                if skillId == skill:
                    return True

        return False

    def getSlotIconPath(self):
        skillId = self.actionId
        if self.option:
            shortCutWithParamIcon = SGTD.data.get(skillId, {}).get('shortCutWithParamIcon', ())
            offset = self.option % uiConst.SKILL_SHORT_CUT_BASE
            if offset < len(shortCutWithParamIcon):
                icon = shortCutWithParamIcon[offset]
            else:
                icon = 0
            iconPath = skillIconPath + str(icon) + iconSuffix
        else:
            schoolInfo = self.proxy._createSchoolInfo()
            if schoolInfo.get('swithIcon', None):
                iconPath = self.proxy._getSwithIcon(skillId)
            else:
                iconPath = self.proxy._getSkillIcon(skillId)
        return iconPath

    def slotShortCut(self):
        if self.option:
            shotCut = (self.sType, self.actionId, self.option)
        else:
            shotCut = (self.sType, self.actionId)
        return shotCut


class ItemActionSlot(ActionSlot):

    def __init__(self, proxy, sType, actionId):
        super(ItemActionSlot, self).__init__(proxy, sType, actionId)
        self.isReset = False

    def getSlotIconPath(self):
        return uiUtils.getItemIconFile40(self.actionId.id)

    def extraSlotData(self):
        item = self.actionId
        count = 1 if item.getSkillVal() else self.proxy.getCountByType(item)
        count = min(999, count)
        data = {}
        data['id'] = item.id
        data['name'] = 'item'
        data['count'] = count
        return data

    def setSlotItem(self, page, pos):
        item = self.actionId
        super(ItemActionSlot, self).setSlotItem(page, pos)
        self.proxy.setSlotColor(page, pos, uiUtils.getItemColorByItem(item))
        self.proxy.playCooldown(page, pos, item.id)
        p = BigWorld.player()
        phy = p.physique
        realCount = self.proxy.getCountByType(item)
        hasSkill = False
        if not item.isYaoPei():
            hasSkill = item.getSkillVal()
        else:
            hasSkill = getattr(item, 'yaoPeiSkillId', 0) != 0
        if not item.canUseNow(phy.sex, phy.school, phy.bodyType, p.lv, p) or hasSkill and realCount == 0:
            self.proxy._setItemSlotState(page, pos, uiConst.SKILL_ICON_STAT_RED)
        else:
            self.proxy._setItemSlotState(page, pos, uiConst.SKILL_ICON_STAT_USEABLE)

    def setShortCut(self, idBar, idSlot):
        if self.isReset:
            return
        self.proxy.setShorCutItem(self.actionId, idBar, idSlot)


class SkillMacroActionSlot(ActionSlot):

    def checkNeedForceBanMacro(self):
        p = BigWorld.player()
        return False

    def setSlotItem(self, page, pos):
        super(SkillMacroActionSlot, self).setSlotItem(page, pos)
        if self.checkNeedForceBanMacro():
            self.proxy._setItemSlotState(page, pos, uiConst.SKILL_ICON_STAT_RED)
        if self.updateShortCut:
            BigWorld.player().saveShortcut(self.proxy.clientShortCut)

    def getSlotIconPath(self):
        p = BigWorld.player()
        macroInfo = p.getMacroInfoById(self.actionId)
        if macroInfo:
            return gameglobal.rds.ui.skillMacroOverview.getIconPathByInfo(macroInfo)
        else:
            return 'item/icon64/notFound.dds'


class SummonedSpriteActionSlot(ActionSlot):

    def setSlotItem(self, page, pos):
        super(SummonedSpriteActionSlot, self).setSlotItem(page, pos)
        p = BigWorld.player()
        index, _ = self.actionId
        if index in p.summonedSpriteLifeList or index in p.spriteBattleCallBackList:
            self.proxy._setItemSlotState(page, pos, uiConst.SKILL_ICON_STAT_GRAY)
        if index not in p.summonSpriteList or utils.getSpriteBattleState(index):
            self.proxy._setItemSlotState(page, pos, uiConst.SKILL_ICON_STAT_RED)
        if self.updateShortCut:
            BigWorld.player().saveShortcut(self.proxy.clientShortCut)

    def getSlotIconPath(self):
        _, spriteId = self.actionId
        return gameglobal.rds.ui.summonedWarSpriteGuard.getSpriteIconPath(int(spriteId))
