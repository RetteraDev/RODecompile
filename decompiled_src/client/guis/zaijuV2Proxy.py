#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/zaijuV2Proxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
from gameglobal import SKILL_STAT_SKILL_TGT, SKILL_STAT_LACK_ENERGY, SKILL_STAT_NO_SKILL, SKILL_STAT_IN_SKILL_RANGE, SKILL_STAT_BAN_WS_SKILL
import uiUtils
import uiConst
import events
import formula
import const
import gametypes
import commQuest
import skillDataInfo
from gameclass import SkillInfo
from gamestrings import gameStrings
import logicInfo
import copy
import utils
import keys
from uiProxy import SlotDataProxy
from guis import hotkey as HK
from guis import hotkeyProxy
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from guis import chickenFoodFactory
from guis import ui
from data import sys_config_data as SCD
from data import zaiju_data as ZD
from data import zaiju_num_data as ZND
from data import skill_general_template_data as SGTD
from data import skill_state_client_data as SSCD
from data import duel_config_data as DCD
from data import skill_general_data as SGD
from data import skill_icon_color_data as SICD
from data import sys_config_data as SYSCD
from cdata import battle_field_dota_lv_data as BFLD
from cdata import game_msg_def_data as GMDD
from cdata import pskill_template_data as PTD
from data import wing_world_carrier_data as WWCD
SKILL_SLOT_MAX_CNT = 6
HP_BAR_POS_RANGE = (276.0, 0.0)
MP_BAR_POX_RANGE = (-256.0, 22.0)
MP_BAR_MASK_WIDTH = 288.6
MP_START_POS_X = 22
BF_DOTA_SKILL_SLOT_MAX_CNT = 8
NOR_ATT_INDEX = 0
PASSIVE_SKILL_INDEX = 1
RIGHT_MOUSE_SKILL_INDEX = 2
INITIATIVE_SKILL_RANGE = range(2, 6)
TALENT_SKILL_RANGE = range(6, 8)
SKILL_DAZHAO_HIDE_LV_START = 3
SKILL_MAX_LV = 5
SKILL_KEY_BIND_DEFAULT = ['',
 '',
 '',
 'shift',
 'E',
 'Q',
 'R',
 'T']
ITEM_KEY_BIND_DEFAULT = ['1',
 '2',
 '3',
 '4',
 '5',
 '6']
SKILL_STAT_CHECK_FUNC_MAP = {SKILL_STAT_SKILL_TGT: '_checkSkillTgt',
 SKILL_STAT_LACK_ENERGY: '_lackEnergy',
 SKILL_STAT_NO_SKILL: '_isUseSkillForbidden',
 SKILL_STAT_BAN_WS_SKILL: 'isBanWSSkill'}

class ZaijuV2Proxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ZaijuV2Proxy, self).__init__(uiAdapter)
        self.bindType = 'zaiJuV2'
        self.type = 'zaiJuV2'
        self.serverSkills = {}
        self.zaijuType = uiConst.ZAIJU_TYPE_SKILL
        self._resetData()
        self.isLearnSkillkeyDown = False

    def _resetData(self):
        self.isChickenFood = False
        self.binding = {}
        self.skills = [[0, 0]] * BF_DOTA_SKILL_SLOT_MAX_CNT
        self.keyText = ['..'] * BF_DOTA_SKILL_SLOT_MAX_CNT
        self.skillSlotCnt = BF_DOTA_SKILL_SLOT_MAX_CNT
        self.useSelfSkill = False
        self.zaijuType = uiConst.ZAIJU_TYPE_SKILL
        self.showType = uiConst.ZAIJU_SHOW_TYPE_ZAIJU
        self.widget = None
        self.slotMcList = []
        self.switchSkill = set([])
        self.skillStatCache = {}
        self.skillIconStat = {}
        self.serverSkills.clear()

    def _registerASWidget(self, widgetId, widget):
        p = BigWorld.player()
        if self.zaijuType == uiConst.ZAIJU_TYPE_SKILL and self.showType == uiConst.ZAIJU_SHOW_TYPE_ZAIJU and not p.bianshen[1]:
            self.hide()
            return
        if self.showType != uiConst.ZAIJU_SHOW_TYPE_EXIT:
            self.hideOtherWidget()
        else:
            self.enableSkillInZaiju(False)
        self.widget = widget
        self.createKeyText()
        self._initUI()
        self.refreshFrame()

    def show(self, skills, zaijuType = uiConst.ZAIJU_TYPE_SKILL, showType = uiConst.ZAIJU_SHOW_TYPE_ZAIJU):
        if self.widget:
            return
        p = BigWorld.player()
        isDotaZaiju = ZD.data.get(p._getZaijuOrBianyaoNo(), {}).get('isDotaZaiju', 0) != 0
        if isDotaZaiju and showType == uiConst.ZAIJU_SHOW_TYPE_ZAIJU and utils.isDotaBfOpen():
            showType = uiConst.ZAIJU_SHOW_TYPE_HERO
        self.skillSlotCnt = BF_DOTA_SKILL_SLOT_MAX_CNT if showType == uiConst.ZAIJU_SHOW_TYPE_HERO else SKILL_SLOT_MAX_CNT
        self.skills = list(skills)
        if showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
            self.skills.insert(1, self.getPassiveSkill())
        self.skills.extend([[0, 0]] * (self.skillSlotCnt - len(self.skills)))
        bfDotaTalentSkillIndex = getattr(p, 'bfDotaTalentSkillIndexList', [0, 1])
        if showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
            self.skills[6] = utils.getTalentSkillByIndex(bfDotaTalentSkillIndex[0])
            self.skills[7] = utils.getTalentSkillByIndex(bfDotaTalentSkillIndex[1])
        self.zaijuType = zaijuType
        self.showType = showType
        self.uiAdapter.loadWidget(uiConst.WIDGET_ZAIJU_V2)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ZAIJU_V2, True)
        self.uiAdapter.setVisRecord(uiConst.WIDGET_ZAIJU_V2, True)

    def getPassiveSkill(self):
        pskill = ZD.data.get(BigWorld.player().bianshen[1], {}).get('pskills', [])
        if len(pskill) > 0:
            return pskill[0]
        return [0, 0]

    def enableSkillInZaiju(self, enabled):
        p = BigWorld.player()
        if not p:
            return
        for skillId in p.getSkills().keys():
            state = uiConst.SKILL_ICON_STAT_USEABLE if enabled else uiConst.SKILL_ICON_STAT_GRAY
            gameglobal.rds.ui.actionbar.setSlotState(skillId, state)

    def hideOtherWidget(self):
        if gameglobal.rds.ui.actionbar.mc:
            gameglobal.rds.ui.actionbar.mc.Invoke('setVisible', GfxValue(False))
        if gameglobal.rds.ui.actionbar.wsMc:
            gameglobal.rds.ui.actionbar.wsMc.Invoke('setVisible', GfxValue(False))
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_ACTION_BARS, False)
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WUSHUANG_BARS, False)
        gameglobal.rds.ui.bullet.setVisible(False)
        if gameglobal.rds.ui.qinggongBar.thisMc:
            gameglobal.rds.ui.qinggongBar.thisMc.SetVisible(False)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ZAIJU_V2)
        self.widget = None
        p = BigWorld.player()
        if self.showType != uiConst.ZAIJU_SHOW_TYPE_EXIT:
            if not gameglobal.rds.ui.isHideAllUI():
                if gameglobal.rds.ui.actionbar.mc:
                    gameglobal.rds.ui.actionbar.mc.Invoke('setVisible', GfxValue(True))
                if gameglobal.rds.ui.actionbar.wsMc:
                    gameglobal.rds.ui.actionbar.wsMc.Invoke('setVisible', GfxValue(True))
            else:
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ACTION_BARS, True)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_WUSHUANG_BARS, True)
                gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_ZAIJU, False)
            gameglobal.rds.ui.actionbar.updateSlots()
            gameglobal.rds.ui.bullet.setVisible(True)
            if gameglobal.rds.ui.qinggongBar.thisMc:
                gameglobal.rds.ui.qinggongBar.thisMc.Invoke('forceVisibleByOther')
            if gameglobal.rds.ui.guildBusinessBag.mediator:
                gameglobal.rds.ui.guildBusinessBag.hide()
        else:
            self.enableSkillInZaiju(True)
        if not p or not p._isOnZaijuOrBianyao():
            self.uiAdapter.setVisRecord(uiConst.WIDGET_ZAIJU_V2, False)
            self._resetData()

    def handleKey(self, down, key, vk, mods):
        p = BigWorld.player()
        operationMode = p.getOperationMode() if hasattr(p, 'getOperationMode') else None
        if key == keys.KEY_LCONTROL:
            self.isLearnSkillkeyDown = down
        if operationMode == gameglobal.ACTION_MODE:
            if key == keys.KEY_LSHIFT or key == keys.KEY_RSHIFT:
                self.useSkill(0, 3, down, byBfDota=True, fromUI=True)

    def refreshFrame(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if not p:
            return
        if p.isOnWingWorldCarrier():
            carrier = p.wingWorldCarrier.getCarrierEnt()
            if carrier:
                self.refreshHpAndMp(carrier.hp, carrier.mhp, carrier.mp, carrier.mmp)
        else:
            self.refreshHpAndMp(p.hp, p.mhp, p.mp, p.mmp)
        self.refreshSkillSlotsBind()
        if self.showType == uiConst.ZAIJU_SHOW_TYPE_ZAIJU:
            gameglobal.rds.ui.actionbar.updateSlots()
        elif self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
            self.checkAllSkillStat(gameglobal.SKILL_STAT_SKILL_TGT)

    def initSkillSlots(self):
        self.slotMcList = []
        if not self.widget.mainMc.skillSlots:
            return
        if not self.showType == uiConst.ZAIJU_SHOW_TYPE_ZAIJU or not self.widget.mainMc.skillSlots:
            return
        if self.skillSlotCnt < len(self.keyText):
            self.widget.mainMc.leaveBtnText.text = self.keyText[self.skillSlotCnt]
        for i in xrange(SKILL_SLOT_MAX_CNT):
            slotMc = self.widget.mainMc.skillSlots.getChildByName('skillSlot%d' % i)
            slotMc.gotoAndStop('up')
            slotMc.mouse.visible = False
            slotMc.slot.binding = ''
            slotMc.slot.binding = 'zaiJuV2.slot%d' % i
            slotMc.slot.keyBind.text = self.keyText[i] if self.keyText[i] else str(i)
            slotMc.slot.dragable = False
            slotMc.slot.addEventListener(events.MOUSE_CLICK, self.handleSlotClick, False, 0, True)
            self.slotMcList.append(slotMc)
            if self.skills[i][0] == 0:
                slotMc.slot.lock.visible = True
                ASUtils.setHitTestDisable(slotMc.slot, True)
            else:
                slotMc.slot.lock.visible = False
                ASUtils.setHitTestDisable(slotMc.slot, False)

        self.widget.mainMc.leaveBtnText.text = self.keyText[SKILL_SLOT_MAX_CNT]

    def getSkillIndex(self, skillId):
        for index, value in enumerate(self.skills):
            if value[0] == skillId:
                return index

        return -1

    def refreshCdStoreage(self, skillId):
        if not self.widget:
            return
        index = self.getSkillIndex(skillId)
        if index < 0:
            return
        slotMc = self.widget.mainMc.skillSlots.getChildByName('skill%d' % index)
        if slotMc:
            cnt = logicInfo.cdStorageSkill.get(skillId, (0, 0))[1]
            slotMc.skill.slot.setCdStorage(cnt)

    def refreshSkillSlots(self):
        if not self.widget:
            return
        if not self.widget.mainMc.skillSlots:
            return
        self.slotMcList = []
        self.setSlotMc(NOR_ATT_INDEX)
        self.setSlotMc(PASSIVE_SKILL_INDEX)
        for i in INITIATIVE_SKILL_RANGE:
            self.setSlotMc(i)

        for i in TALENT_SKILL_RANGE:
            self.setSlotMc(i)

    def refreshSkillPoints(self):
        if not self.widget:
            return
        if not self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
            return
        p = BigWorld.player()
        for i in INITIATIVE_SKILL_RANGE:
            slotMc = self.slotMcList[i]
            skillId = self.skills[i][0]
            skillLv = self.serverSkills.get(skillId, (0, 0))[1]
            learnLv = SGD.data.get((skillId, skillLv + 1), {}).get('learnLv', 999)
            canLearn = p.battleFieldDotaLv >= learnLv
            ASUtils.setMcData(slotMc.parent.lvUpBtn, 'slotIdx', i)
            lightMc = self.widget.mainMc.skillSlots.getChildByName('lightMc%d' % (i - 2))
            ASUtils.setHitTestDisable(lightMc, True)
            if p.battleFieldDotaSkillPoint > 0 and canLearn:
                slotMc.parent.setChildIndex(slotMc.parent.lvUpBtn, slotMc.parent.numChildren - 1)
                slotMc.parent.lvUpBtn.visible = True
                slotMc.parent.lv.visible = True
                slotMc.parent.lvUpBtn.addEventListener(events.MOUSE_CLICK, self.handleLvUpBtnClick, False, 0, True)
                if skillLv >= SKILL_MAX_LV:
                    slotMc.parent.lvUpBtn.gotoAndStop('manji')
                    ASUtils.setHitTestDisable(slotMc.parent.lvUpBtn, True)
                    lightMc.visible = False
                else:
                    slotMc.parent.lvUpBtn.gotoAndStop('shengji')
                    ASUtils.setHitTestDisable(slotMc.parent.lvUpBtn, False)
                    lightMc.visible = True
            else:
                slotMc.parent.lvUpBtn.visible = False
                slotMc.parent.lv.visible = True
                lightMc.visible = False

        self.setLevelUpTipsVisible(p.battleFieldDotaSkillPoint > 0)

    def handleLvUpBtnClick(self, *args):
        e = ASObject(args[3][0])
        slotIdx = int(e.currentTarget.slotIdx)
        self.doSkillLvUp(slotIdx)

    @ui.callFilter(0.2, False)
    def doSkillLvUp(self, index):
        p = BigWorld.player()
        skillId = self.skills[index][0]
        skillLv = self.serverSkills.get(skillId, (0, 0))[1]
        learnLv = SGD.data.get((skillId, skillLv + 1), {}).get('learnLv', 999)
        if p.battleFieldDotaLv >= learnLv:
            p.cell.updateBattleFieldDotaSkillLv(skillId)

    def setSlotMc(self, index):
        p = BigWorld.player()
        if index in INITIATIVE_SKILL_RANGE:
            slotMc = self.widget.mainMc.skillSlots.getChildByName('skill%d' % index).skill
        else:
            slotMc = self.widget.mainMc.skillSlots.getChildByName('skill%d' % index)
        if slotMc.slot.lock:
            slotMc.slot.lock.visible = False
        slotMc.gotoAndStop('up')
        ASUtils.setHitTestDisable(slotMc.mouse, True)
        slotMc.slot.binding = ''
        slotMc.slot.binding = 'zaiJuV2.slot%d' % index
        operatonMode = p.getOperationMode()
        if index == NOR_ATT_INDEX and operatonMode == gameglobal.ACTION_MODE:
            slotMc.mouse.visible = True
            slotMc.mouse.gotoAndStop('zuo')
        else:
            slotMc.mouse.visible = False
        slotMc.slot.keyBind.text = self.keyText[index]
        ASUtils.textFieldAutoSize(slotMc.slot.keyBind, slotMc.slot.keyBind.text)
        slotMc.slot.dragable = False
        skillId = self.skills[index][0]
        lv = self.serverSkills.get(skillId, (0, 0))[1]
        slotMc.slot.addEventListener(events.MOUSE_CLICK, self.handleSlotClick, False, 0, True)
        for i in xrange(SKILL_MAX_LV):
            if index in INITIATIVE_SKILL_RANGE:
                lvMc = slotMc.parent.lv.getChildByName('lv%d' % i)
                if i < lv:
                    if lvMc.lv.currentFrameLabel != 'jihuo':
                        lvMc.lv.gotoAndPlay('jihuo')
                elif lvMc.lv.currentFrameLabel != 'weijihuo':
                    lvMc.lv.gotoAndStop('weijihuo')

        self.slotMcList.append(slotMc)

    def refreshSkillSlotsBind(self):
        if not self.widget:
            return
        if self.showType not in [uiConst.ZAIJU_SHOW_TYPE_HERO, uiConst.ZAIJU_SHOW_TYPE_ZAIJU]:
            return
        self.createKeyText()
        if self.showType == uiConst.ZAIJU_SHOW_TYPE_ZAIJU:
            self.initSkillSlots()
        elif self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
            self.refreshSkillSlots()
        self.checkAllSkillStat(gameglobal.SKILL_STAT_LACK_ENERGY)

    def handleSlotClick(self, *args):
        e = ASObject(args[3][0])
        key = e.currentTarget.binding
        _, slotId = self.getSlotID(key)
        p = BigWorld.player()
        self.useSkill(0, slotId, True, True, byBfDota=formula.inDotaBattleField(p.mapID))

    def _getKey(self, bar, slotId):
        return 'zaiju.slot%d' % slotId

    def shakeSlot(self, slotId):
        if slotId >= len(self.slotMcList):
            return
        if not self.slotMcList[slotId].slot:
            self._resetData()
            return
        if self.slotMcList[slotId].slot.data and self.slotMcList[slotId].slot.data.iconPath != 'notFound':
            self.slotMcList[slotId].gotoAndPlay('down')

    def onSlotMouseOver(self, *args):
        key = args[3][0].GetString()
        bar, idNum = self.getSlotID(key)
        if idNum == PASSIVE_SKILL_INDEX:
            return
        skillId, level = self.getSkillInfo(idNum)
        level = max(1, level)
        if skillId:
            BigWorld.player().playHoverEffect(skillId, level)

    def onSlotMouseOut(self, *arg):
        BigWorld.player().stopHoverEffect()

    def useSkill(self, bar, soltId, isDown = False, isKeyMode = True, autoUseSkill = False, byBfDota = False, fromUI = False):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            if not p:
                return
            inBfDota = formula.inDotaBattleField(getattr(p, 'mapID', 0))
            if inBfDota and not byBfDota or not inBfDota and byBfDota or soltId == None or byBfDota and soltId == PASSIVE_SKILL_INDEX:
                return
            if isDown:
                gameglobal.rds.bar = bar
                gameglobal.rds.soltId = soltId
            else:
                gameglobal.rds.bar = None
                gameglobal.rds.soltId = None
            if self.isLearnSkillkeyDown and byBfDota:
                self.doSkillLvUp(soltId)
                return
            if isKeyMode and isDown:
                self.shakeSlot(soltId)
            if self.widget and soltId >= len(self.skills):
                BigWorld.player().circleEffect.cancel()
                return
            skillId = self.skills[soltId][0]
            if skillId == 0:
                return
            if self.zaijuType == uiConst.ZAIJU_TYPE_WEAR and isDown:
                p.useWearSkillBySlotId(True, soltId)
                return
            realLv = self.serverSkills.get(skillId, (0, 0))[1]
            if not realLv:
                return
            isQteSkill = False
            if p.skillQteData.has_key(skillId):
                skillId = p.skillQteData[skillId].qteSkills[0]
                isQteSkill = True
            zaijuNo = p._getZaijuNo()
            if zaijuNo == 0:
                return
            if p.mapID == const.FB_NO_SPRING_ACTIVITY:
                cins = chickenFoodFactory.getInstance()
                isLight, canUse, _type, _remain, _total = cins.getSkillState(skillId)
                if not canUse or _remain > 0:
                    return
            skills = self.skills
            isSkill = False
            for id, lv in skills:
                if skillId == id:
                    isSkill = True
                    break

            if isSkill or isQteSkill:
                skillLevel = realLv
                skillInfo = SkillInfo(skillId, skillLevel)
                needAutoUseSkill = skillInfo.getSkillData('autoUseSkill', 0)
                if autoUseSkill:
                    if not needAutoUseSkill:
                        return
                skillInfo = SkillInfo(skillId, skillLevel)
                isCastSelfKeyDown = HK.isCastSelfKeyDown()
                self.useSelfSkill = False
                skillTargetType, skillTargetValue = p.getSkillTargetType(skillInfo)
                if skillTargetValue:
                    if skillTargetType == gametypes.SKILL_TARGET_SELF or skillTargetType == gametypes.SKILL_TARGET_SELF_FRIEND and (isCastSelfKeyDown or p.targetLocked == None or not p.isFriend(p.targetLocked)) or skillTargetType == gametypes.SKILL_TARGET_SELF_ENERMY and (isCastSelfKeyDown or p.targetLocked == None or not p.isEnemy(p.targetLocked)) or skillTargetType == gametypes.SKILL_TARGET_ALL_TYPE and (isCastSelfKeyDown or p.targetLocked == None or not p.targetLocked.IsCombatUnit):
                        p.lastTargetLocked = p.targetLocked
                        p.targetLocked = p
                        self.useSelfSkill = True
                if skillInfo.getSkillData('castType', gametypes.SKILL_FIRE_NORMAL) == gametypes.SKILL_FIRE_SWITCH and isDown:
                    self.switchSkill.add((skillInfo.getSkillData('switchState', 0), skillId))
                if not isKeyMode:
                    p.useSkillByMouseUp(isDown, skillInfo)
                else:
                    p.useSkillByKeyDown(isDown, skillInfo)
                if self.useSelfSkill:
                    p.targetLocked = p.lastTargetLocked
            else:
                if not p.stateMachine.checkStatus(const.CT_USE_MARKER_NPC):
                    return
                p.cell.onClickItemNearMarker(skillId)
            return

    def handleLeaveBtnClick(self, *args):
        p = BigWorld.player()
        if self.showType == uiConst.ZAIJU_SHOW_TYPE_CARROUSEL:
            p.leaveCarrousel()
        elif p.inInteractiveObject():
            p.quitInteractiveObj()
        elif self.zaijuType == uiConst.ZAIJU_TYPE_WEAR:
            if p.weaponInHandState() == gametypes.WEAR_BACK_ATTACH:
                p.updateBackWear(True)
                if p.modelServer.backwear.isActionJustSkillWear():
                    p.fashion.stopAllActions()
            elif p.weaponInHandState() == gametypes.WEAR_WAIST_ATTACH:
                p.updateWaistWear(True)
                if p.modelServer.waistwear.isActionJustSkillWear():
                    p.fashion.stopAllActions()
        elif p.isInCoupleRide():
            p.cell.cancelCoupleEmote()
        else:
            self.leaveZaiju()

    def leaveZaiju(self):
        p = BigWorld.player()
        if not p:
            return
        elif p.isInBfDota():
            return
        elif p.inPUBGPlane():
            p.cell.pubgJumpFromPlane()
            return
        elif p.inPUBGParachute():
            p.cell.pubgJumpToGround(False)
            return
        else:
            if p.isOnWingWorldCarrier():
                dist = p.qinggongMgr.getDistanceFromGround()
                if dist != p.flyHeight and dist < WWCD.data.get('heightForLeaveCarrier', 5):
                    p.cell.applyLeaveWingWorldCarrier()
                else:
                    p.showGameMsg(GMDD.data.UNABLE_TO_LEAVE_CARRIER, ())
            elif not utils.isInBusinessZaiju(p) or p.zaijuBag.countZaijuBagNum() <= 0:
                zjd = ZD.data.get(p._getZaijuNo(), {})
                if zjd.has_key('leaveZaijuNeedShowTip'):
                    msg = uiUtils.getTextFromGMD(GMDD.data.LEAVE_ZAIJU_DISAPPREAR_TIP, '')
                    self.bagMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.leaveZaiju)
                else:
                    p.cell.leaveZaiju()
            else:
                bagMsgBoxId = getattr(self, 'bagMsgBoxId', None)
                if bagMsgBoxId:
                    gameglobal.rds.ui.messageBox.dismiss(bagMsgBoxId)
                msg = uiUtils.getTextFromGMD(GMDD.data.GUILD_BUSINESS_LEAVE_ZAIJU_HINT, '')
                self.bagMsgBoxId = gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.cell.leaveZaiju)
            return

    def handleBagBtnClick(self, *args):
        gameglobal.rds.ui.guildBusinessBag.show()

    def handleBusinessFindBtnClick(self, *args):
        gameglobal.rds.ui.guildBusinessFindPath.show()

    def handleCameraBtnClick(self, *args):
        p = BigWorld.player()
        if not p:
            return
        BigWorld.player().modelServer.switchCarrouselAni()

    def _initUI(self):
        p = BigWorld.player()
        if not p:
            return
        else:
            zjd = ZD.data.get(p.bianshen[1], {})
            if self.showType == uiConst.ZAIJU_SHOW_TYPE_ZAIJU:
                self.widget.gotoAndStop('zaiju')
                leaveForbid = zjd.get('leaveForbid', 0) != 0
                self.widget.mainMc.exitBtn.enabled = not leaveForbid
                self.widget.mainMc.exitBtn.addEventListener(events.MOUSE_CLICK, self.handleLeaveBtnClick, False, 0, True)
                isBusiness = utils.isInBusinessZaiju(p)
                if isBusiness:
                    gameglobal.rds.ui.guildBusinessBag.setBagSlotCount(zjd.get('bagSlotCount', 0))
                self.widget.mainMc.bagBtn.visible = isBusiness
                self.widget.mainMc.bagBtn.addEventListener(events.MOUSE_CLICK, self.handleBagBtnClick, False, 0, True)
                TipManager.addTip(self.widget.mainMc.bagBtn, gameStrings.ZAIJU_V2_PROXY_BAG)
                self.widget.mainMc.businessFindBtn.visible = isBusiness
                self.widget.mainMc.businessFindBtn.addEventListener(events.MOUSE_CLICK, self.handleBusinessFindBtnClick, False, 0, True)
                TipManager.addTip(self.widget.mainMc.businessFindBtn, gameStrings.ZAIJU_V2_PROXY_BUSINESS_FIND)
                bfyZaijuNo = SCD.data.get('bfyZaijuNo', ())
                self.isChickenFood = p.mapID == const.FB_NO_SPRING_ACTIVITY and p._isOnZaijuOrBianyao() and p._getZaijuOrBianyaoNo() in bfyZaijuNo
                self.initSkillSlots()
                ASUtils.setHitTestDisable(self.widget.mainMc.leaveBtnText, True)
                self.refreshPhoto(zjd)
            elif self.showType == uiConst.ZAIJU_SHOW_TYPE_CARROUSEL:
                carrousel = BigWorld.entities.get(BigWorld.player().carrousel[0], None)
                if carrousel:
                    canSwitchCamera = carrousel.canSwitchCameraAni()
                    isLeaveForbid = carrousel.getItemData().get('leaveForbid', 0)
                else:
                    canSwitchCamera = False
                    isLeaveForbid = False
                self.widget.gotoAndStop('youLeChang')
                self.widget.mainMc.leaveBtn.enabled = not isLeaveForbid
                self.widget.mainMc.cameraBtn.enabled = canSwitchCamera
                self.widget.mainMc.leaveBtn.addEventListener(events.BUTTON_CLICK, self.handleLeaveBtnClick, False, 0, True)
                self.widget.mainMc.cameraBtn.addEventListener(events.BUTTON_CLICK, self.handleCameraBtnClick, False, 0, True)
                TipManager.addTip(self.widget.mainMc.leaveBtn, gameStrings.ZAIJU_V2_PROXY_LEAVE_ZAIJU)
                TipManager.addTip(self.widget.mainMc.cameraBtn, gameStrings.ZAIJU_V2_PROXY_SWITCH_CAMERA)
            elif self.showType == uiConst.ZAIJU_SHOW_TYPE_EXIT:
                self.widget.gotoAndStop('exit')
                leaveForbid = ZD.data.get(BigWorld.player()._getZaijuNo(), {}).get('leaveForbid', 0) != 0
                self.widget.mainMc.exitBtn.enabled = not leaveForbid
                self.widget.mainMc.exitBtn.addEventListener(events.BUTTON_CLICK, self.handleLeaveBtnClick, False, 0, True)
            elif self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
                self.widget.gotoAndStop('zhujineng')
                self.refreshSkillSlotsBind()
                self.refreshPhoto(zjd)
                self.refreshSkillPoints()
                energyType = zjd.get('bfDotaZaijuEnergyType', 0)
                energyTypeFrame = DCD.data.get('zaiju_energyType_map', {}).get(energyType, 'lanse')
                self.widget.mainMc.mp.bar.gotoAndStop(energyTypeFrame)
                for i in xrange(SKILL_DAZHAO_HIDE_LV_START, SKILL_MAX_LV):
                    self.widget.mainMc.skillSlots.skill5.lv.getChildByName('lv%d' % i).visible = False

            return

    def refreshPhoto(self, zjd):
        if not self.widget.mainMc.photo:
            return
        headIcon = zjd.get('headIcon', '')
        if not headIcon:
            self.widget.mainMc.photo.visible = False
        else:
            self.widget.mainMc.photo.visible = True
            self.widget.mainMc.photo.icon.loadImage('zaijuHeadIcon/%s.dds' % headIcon)
            lvStr = str(self.getZaijuLv(zjd))
            if self.widget.mainMc.photo.level.lvText.text != lvStr:
                self.widget.mainMc.photo.level.lvText.text = lvStr
                if self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
                    self.widget.mainMc.photo.lvUpEff.gotoAndPlay(1)

    def refreshLv(self):
        if not self.widget:
            return
        if not self.widget.mainMc.photo:
            return
        lvStr = str(self.getZaijuLv({}))
        if self.widget.mainMc.photo.level.lvText.text != lvStr:
            self.widget.mainMc.photo.level.lvText.text = lvStr
            if self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
                self.widget.mainMc.photo.lvUpEff.gotoAndPlay(1)

    def refreshPlayerHpAndMp(self, hp, mhp, mp, mmp):
        p = BigWorld.player()
        if p.isOnWingWorldCarrier():
            return
        self.refreshHpAndMp(hp, mhp, mp, mmp)

    def refreshHpAndMp(self, hp, mhp, mp, mmp):
        if not self.widget:
            return
        if self.showType not in (uiConst.ZAIJU_SHOW_TYPE_ZAIJU, uiConst.ZAIJU_SHOW_TYPE_HERO):
            return
        if self.isChickenFood:
            hpPercent = 1
            mpPercent = 1
        else:
            if mhp != 0:
                hpPercent = hp / (mhp * 1.0)
            else:
                hpPercent = 1.0
            if mmp != 0:
                mpPercent = mp / (mmp * 1.0)
            else:
                mpPercent = 1.0
        if not self.widget.mainMc:
            self._resetData()
            return
        if not self.widget.mainMc.hp.bar:
            return
        self.widget.mainMc.hp.bar.x = HP_BAR_POS_RANGE[0] + (HP_BAR_POS_RANGE[1] - HP_BAR_POS_RANGE[0]) * hpPercent
        self.widget.mainMc.mp.bar.x = MP_BAR_POX_RANGE[0] + (MP_BAR_POX_RANGE[1] - MP_BAR_POX_RANGE[0]) * mpPercent
        self.widget.mainMc.hp.hpText.text = '%d/%d' % (hp, mhp)
        self.widget.mainMc.mp.mpText.text = '%d/%d' % (mp, mmp)

    def createKeyText(self):
        if self.showType == uiConst.ZAIJU_SHOW_TYPE_ZAIJU:
            keyArr = [ ('..' if len(x) > 4 else x) for x in hotkeyProxy.getInstance().shortKey.getKeyDescArray()[0:6] ]
            keyArr.append(hotkeyProxy.getInstance().shortKey.getKeyDescById(HK.KEY_LEAVE_ZAIJU))
        else:
            keyArr = [ HK.HKM[x].getDesc() for x in HK.BfDotaSkillHotkeyList ]
        self.keyText = keyArr

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (0, int(idItem[4:]))

    def getSlotValue(self, movie, idItem, idCon):
        data = {}
        skillId, skillLv = self.skills[idItem]
        skillLv = self.serverSkills.get(skillId, (0, 0))[1]
        if skillLv == 0:
            skillLv = 1
        iconPath = self.getSkillIconPath(skillId, skillLv)
        data['name'] = iconPath
        data['iconPath'] = iconPath
        if utils.isCDStorageSkill(skillId, skillLv):
            data['cdStorage'] = logicInfo.cdStorageSkill.get(skillId, (0, 0))[1]
        return uiUtils.dict2GfxDict(data, True)

    def printF(self, *args):
        print args

    def getSkillIconPath(self, skillId, level = 1):
        p = BigWorld.player()
        if skillId == 0:
            return 'notFound'
        else:
            isSkill = False
            for id, lv in self.skills:
                if skillId == id:
                    isSkill = True
                    break

            if not isSkill:
                isSkill = self.serverSkills.has_key(skillId)
                if not isSkill:
                    for info in p.skillQteData.values():
                        if skillId in info.qteSkills:
                            isSkill = True
                            break

            if isSkill or self.zaijuType == uiConst.ZAIJU_TYPE_WEAR:
                isPskill = self.getPassiveSkill()[0] == skillId
                if isPskill:
                    sd = PTD.data.get(skillId, {})
                    icon = sd.get('icon', '')
                else:
                    sd = skillDataInfo.ClientSkillInfo(skillId, level)
                    icon = sd.getSkillData('icon', '')
                if icon:
                    return 'skill/icon/' + str(icon) + '.dds'
            else:
                icon = commQuest.getEmotionIcon(skillId)
                if icon != None:
                    return 'emote/%d.dds' % icon
            return 'notFound'

    def getSkillInfo(self, idItem):
        skillId, skillLv = (0, 0)
        if idItem != None and idItem < len(self.skills):
            skillId, skillLv = self.skills[idItem]
            skillLv = self.serverSkills.get(skillId, (0,
             skillLv,
             0,
             False))[1]
        return (skillId, skillLv)

    def setServerSkills(self, info, isPkill = False):
        p = BigWorld.player()
        for item in info:
            if self.serverSkills.has_key(item[0]) and item[1] > self.serverSkills[item[0]][1]:
                gameglobal.rds.sound.playSound(5612)
            self.serverSkills[item[0]] = (item[0],
             item[1],
             item[2],
             isPkill)
            logicInfo.initCdStoreageSkill(item[0])

        if self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
            bfDotaTalentSkillIndex = getattr(p, 'bfDotaTalentSkillIndexList', [0, 1])
            skillInfo = utils.getTalentSkillByIndex(bfDotaTalentSkillIndex[0])
            self.serverSkills[skillInfo[0]] = (skillInfo[0],
             skillInfo[1],
             True,
             False)
            skillInfo = utils.getTalentSkillByIndex(bfDotaTalentSkillIndex[1])
            self.serverSkills[skillInfo[0]] = (skillInfo[0],
             skillInfo[1],
             True,
             False)
        self.refreshSkillSlotsBind()
        self.refreshSkillPoints()

    def isNormalAttackSkill(self, skillId):
        return SGTD.data.get(skillId, {}).get('skillCategory') == const.SKILL_CATEGORY_BF_DOTA_NORMAL

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, idNum = self.getSlotID(key)
        if idNum == 0 and self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
            return ''
        skillId, skillLv = self.skills[idNum]
        if skillId in self.serverSkills:
            skillLv = self.serverSkills[skillId][1]
        tooltip = ''
        if skillId != 0:
            if skillLv != -1:
                skillInfo = self.serverSkills.get(skillId, (0,
                 0,
                 0,
                 False))
                isPskill = self.getPassiveSkill()[0] == skillId
                if isPskill:
                    tooltip = self.uiAdapter.skill.formatPSkillTooltip(skillId, sLv=skillLv)
                else:
                    tooltip = gameglobal.rds.ui.actionbar.formatToolTip(skillId, skillLv)
        return tooltip

    def refreshExp(self):
        p = BigWorld.player()
        exp = p.battleFieldDotaExp
        lvUpExp = BFLD.data.get(p.battleFieldDotaLv, {}).get('upNeedExp', 100000)
        self.setExp(exp / (lvUpExp * 1.0))

    def setExp(self, percent):
        if not self.widget:
            return
        self.widget.mainMc.photo.expBar.expMask.rotationZ = 108 + -109 * percent
        self.widget.mainMc.photo.expBar.cursor.rotationZ = 6 + -108 * percent

    def _getSwithIcon(self, skillId, skillLv):
        p = BigWorld.player()
        if SSCD.data.has_key((skillId, p.ammoType)):
            icon = SSCD.data.get((skillId, p.ammoType), {}).get('icon', None)
            if icon:
                return 'skill/icon/%s.dds' % str(icon)
            else:
                return self.getSkillIconPath(skillId, skillLv)
        states = p.statesServerAndOwn.keys()
        for state in states:
            if SSCD.data.has_key((skillId, state)):
                icon = SSCD.data.get((skillId, state), {}).get('icon', None)
                if icon:
                    return 'skill/icon/%s.dds' % str(icon)
                else:
                    return self.getSkillIconPath(skillId, skillLv)

        return self.getSkillIconPath(skillId, skillLv)

    def _getKeyByActionID(self, srcSkillId):
        for i in xrange(self.skillSlotCnt):
            if i >= len(self.skills):
                return
            if self.skills[i][0] == srcSkillId:
                return 'zaiJuV2.slot%d' % i

        return ''

    def changeIcon(self, srcSkillId, dstSkillId):
        if not self.widget:
            return
        if self.showType not in (uiConst.ZAIJU_SHOW_TYPE_ZAIJU, uiConst.ZAIJU_SHOW_TYPE_HERO):
            return
        iconPath = self._getSwithIcon(dstSkillId, 1)
        data = {'iconPath': iconPath}
        key = self._getKeyByActionID(srcSkillId)
        keyText = ''
        if self.binding.has_key(key):
            self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
            self.binding[key][0].Invoke('qteActivate', GfxValue(srcSkillId != dstSkillId))
            keyIndex = self.getSlotID(key)[1]
            if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE and keyIndex in (10, 11):
                keyText = '-' if keyIndex == 10 else '='
            else:
                keyText = self.keyText[keyIndex]
        gameglobal.rds.ui.actionbar.updateSlots()
        return keyText

    def showChargeSkillShine(self, skillId, isShow):
        if not self.widget:
            return
        if not self.showType == uiConst.ZAIJU_SHOW_TYPE_ZAIJU:
            return
        self.setShine(skillId, isShow)

    def setShine(self, skillId, isShow):
        for i, info in enumerate(self.skills):
            if info[0] == skillId:
                key = self._getKeyByActionID(info[0])
                if self.binding.has_key(key):
                    self.binding[key][0].Invoke('showToggleShine', GfxValue(isShow))

    def showPauseShine(self, isShow):
        if not self.widget:
            return
        elif self.showType not in (uiConst.ZAIJU_SHOW_TYPE_ZAIJU, uiConst.ZAIJU_SHOW_TYPE_HERO):
            return
        else:
            skillId = SYSCD.data.get('multiCarrierWalkSkillId', None)
            if skillId:
                self.setShine(skillId, isShow)
            return

    def showToggleShine(self, old):
        if not self.widget:
            return
        if self.showType not in (uiConst.ZAIJU_SHOW_TYPE_ZAIJU, uiConst.ZAIJU_SHOW_TYPE_HERO):
            return
        p = BigWorld.player()
        newState = set(p.statesServerAndOwn.keys())
        oldState = set(old.keys())
        addState = newState - oldState
        delState = oldState - newState
        if addState and type(addState) == set:
            for state in addState:
                skillId = self.getSwitchSkill(state)
                if skillId:
                    self.setShine(skillId, True)
                    return

        if delState and type(delState) == set:
            for state in delState:
                skillId = self.getSwitchSkill(state)
                if skillId:
                    self.setShine(skillId, False)
                    return

    def getSwitchSkill(self, state):
        if self.switchSkill:
            for stateId, skillId in self.switchSkill:
                if stateId == state:
                    return skillId

        return 0

    def getZaijuLv(self, zaijuData):
        p = BigWorld.player()
        if self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
            return p.battleFieldDotaLv
        else:
            replaceProperty = zaijuData.get('replaceProperty', 0)
            if not replaceProperty:
                return p.lv
            zaijuPropId = zaijuData.get('zaijuPropId', 0)
            lv = ZND.data.get(zaijuPropId, {}).get('lv', 0)
            return lv

    def getBinding(self, idNum):
        if not self.widget:
            return (None, None, 0, 0)
        else:
            index = self.getSkillIndex(idNum)
            if index > 0 and index < len(self.binding):
                key = 'zaiJuV2.slot%d' % index
                return (self.binding.get(key, None),
                 key,
                 0,
                 index)
            return (None, None, 0, 0)

    def checkAllSkillStat(self, skillStatType):
        for index in xrange(BF_DOTA_SKILL_SLOT_MAX_CNT):
            if index >= len(self.skills):
                break
            if index == PASSIVE_SKILL_INDEX and self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
                continue
            skillId, _ = self.skills[index]
            self.checkSkillStat(skillId, skillStatType)

    def checkSkillStat(self, skillId, skillStatType, inSkillRange = False):
        if skillId == 0:
            return
        if skillStatType == gameglobal.SKILL_STAT_IN_SKILL_RANGE:
            self._updataSkillStat(skillId, skillStatType, inSkillRange)
        else:
            funcName = SKILL_STAT_CHECK_FUNC_MAP[skillStatType]
            newStat = getattr(self, funcName)(skillId)
            self._updataSkillStat(skillId, skillStatType, newStat)
        self._updateSkillIcon(skillId)

    def _isTargetSkill(self, skillId):
        skillInfo = BigWorld.player().getSkillInfo(skillId, self.getSkillLv(skillId))
        return skillInfo.isTargetSkill()

    def _checkSkillTgt(self, skillId):
        if not self._isTargetSkill(skillId):
            return gameglobal.SKILL_TGT_NO_NEED_TGT
        p = BigWorld.player()
        skillInfo = p.getSkillInfo(skillId, self.getSkillLv(skillId))
        if p.targetLocked == None:
            return gameglobal.SKILL_TGT_UNLOCK_TGT
        elif self._isSelfSkillType(skillInfo):
            return gameglobal.SKILL_TGT_RIGHT_TGT
        elif not skillDataInfo.checkTargetRelationRequest(skillInfo, False) and hasattr(p.targetLocked, 'hp'):
            return gameglobal.SKILL_TGT_WRONG_TGT
        elif skillInfo.getSkillData('tgtLimit') == gametypes.SKILL_TGT_LIMIT_AVATAR and not utils.instanceof(p.targetLocked, 'Avatar'):
            return gameglobal.SKILL_TGT_WRONG_TGT
        else:
            return gameglobal.SKILL_TGT_RIGHT_TGT

    def _isSelfSkillType(self, skillInfo):
        p = BigWorld.player()
        skillTargetType, skillTargetValue = p.getSkillTargetType(skillInfo)
        if skillTargetValue:
            if skillTargetType in (gametypes.SKILL_TARGET_ENERMY, gametypes.SKILL_TARGET_FRIEND):
                return False
            if skillTargetType in (gametypes.SKILL_TARGET_ALL_TYPE, gametypes.SKILL_TARGET_SELF_ENERMY, gametypes.SKILL_TARGET_SELF_FRIEND):
                return True
        return False

    def _lackEnergy(self, skillId):
        lv = self.getSkillLv(skillId)
        if lv == 0:
            return True
        skillInfo = BigWorld.player().getSkillInfo(skillId, self.getSkillLv(skillId))
        if not skillDataInfo.checkSelfRequest(skillInfo, False):
            return True
        return False

    def _isUseSkillForbidden(self, skillId):
        p = BigWorld.player()
        if p.bannedSkils and skillId in p.bannedSkils:
            return True
        skillInfo = p.getSkillInfo(skillId, self.getSkillLv(skillId))
        if skillInfo.getSkillData('noInCombat', 0) and p.inCombat == True:
            return True
        return False

    def _checkInSkillRange(self, skillId):
        p = BigWorld.player()
        if not self._isTargetSkill(skillId):
            return True
        else:
            tgt = p.targetLocked
            if tgt == None:
                return True
            skillInfo = p.getSkillInfo(skillId, self.getSkillLv(skillId))
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

    def isBanWSSkill(self, skillId):
        return False

    def initSkillStat(self, skillId):
        self.skillStatCache[skillId] = [0] * gameglobal.SKILL_STAT_CNT
        self.skillIconStat[skillId] = uiConst.SKILL_ICON_STAT_USEABLE
        self.setSlotState(skillId, uiConst.SKILL_ICON_STAT_USEABLE)
        oldSkillStat = copy.deepcopy(self.skillStatCache[skillId])
        self._updataSkillStat(skillId, SKILL_STAT_SKILL_TGT, self._checkSkillTgt(skillId))
        self._updataSkillStat(skillId, SKILL_STAT_LACK_ENERGY, self._lackEnergy(skillId))
        self._updataSkillStat(skillId, SKILL_STAT_NO_SKILL, self._isUseSkillForbidden(skillId))
        self._updataSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, self._checkInSkillRange(skillId))
        self._updataSkillStat(skillId, SKILL_STAT_BAN_WS_SKILL, self.isBanWSSkill(skillId))
        if oldSkillStat != self.skillStatCache[skillId]:
            self._updateSkillIcon(skillId)

    def _updateSkillIcon(self, skillId):
        skillStat = self.skillStatCache[skillId]
        curIconStat = self.skillIconStat[skillId]
        d = SICD.data.get((skillStat[0],
         skillStat[1],
         skillStat[2],
         skillStat[3]), {})
        nextIconStat = d.get('nextStat', 1)
        if len(skillStat) > 4 and skillStat[4]:
            nextIconStat = 2
        if curIconStat == nextIconStat:
            return
        if BigWorld.player().interactiveObjectEntId:
            return
        self.setSlotState(skillId, nextIconStat)

    def setSlotState(self, skillId, state):
        self.skillIconStat[skillId] = state
        key = self._getKeyByActionID(skillId)
        if key and self.binding.get(key) != None:
            self.binding[key][0].Invoke('setSlotState', GfxValue(state))

    def _updataSkillStat(self, skillId, skillStatType, newStat):
        if not self.skillStatCache.has_key(skillId):
            self.initSkillStat(skillId)
        self.skillStatCache[skillId][skillStatType] = int(newStat)
        if skillStatType == gameglobal.SKILL_STAT_SKILL_TGT:
            if newStat == gameglobal.SKILL_TGT_NO_NEED_TGT or newStat == gameglobal.SKILL_TGT_UNLOCK_TGT:
                self._updataSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, True)

    def getTargetSkillList(self):
        res = []
        temList = self.serverSkills.keys()
        for skillId in temList:
            skillInfo = BigWorld.player().getSkillInfo(skillId, self.getSkillLv(skillId))
            if self._isTargetSkill(skillId) and skillDataInfo.checkTargetRelationRequest(skillInfo, False):
                res.append(skillId)

        return res

    def onEnterClientRangeNew(self, skillId, dist):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            if skillId == 0 or not self.serverSkills.has_key(skillId):
                return
            lv = self.getSkillLv(skillId)
            skillInfo = p.getSkillInfo(skillId, lv)
            rangeMin = skillInfo.getSkillData('rangeMin', 0)
            if rangeMin != 0 and p.targetLocked != None:
                rangeMin = self.uiAdapter.actionbar._calcRealSkillRangeMin(rangeMin)
                if dist == rangeMin:
                    self.checkSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, False)
                    return
            self.checkSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, True)
            return

    def onLeaveClientRangeNew(self, skillId, dist):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            if skillId == 0 or not self.serverSkills.has_key(skillId):
                return
            lv = self.getSkillLv(skillId)
            skillInfo = p.getSkillInfo(skillId, lv)
            rangeMin = skillInfo.getSkillData('rangeMin', 0)
            if rangeMin != 0 and p.targetLocked != None:
                rangeMin = self.uiAdapter.actionbar._calcRealSkillRangeMin(rangeMin)
                if dist == rangeMin:
                    self.checkSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, True)
                    return
            self.checkSkillStat(skillId, SKILL_STAT_IN_SKILL_RANGE, False)
            return

    def getSkillLv(self, skillId):
        if skillId in self.serverSkills:
            return self.serverSkills.get(skillId, (0, 1))[1]
        for id, lv in self.skills:
            if id == skillId:
                return lv

        return 0

    def setLevelUpTipsVisible(self, visible):
        if not self.widget or not self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO:
            return
        self.widget.mainMc.iconTips.visible = visible
        self.widget.mainMc.txtTips.visible = visible

    def setReliveCountDown(self, time):
        if not (self.widget and self.showType == uiConst.ZAIJU_SHOW_TYPE_HERO and self.widget.mainMc.txtCountDown):
            return
        timeStr = str(time) if time else ''
        self.widget.mainMc.txtCountDown.text = timeStr
        ASUtils.setMcEffect(self.widget.mainMc.photo.icon, 'gray' if timeStr else '')
