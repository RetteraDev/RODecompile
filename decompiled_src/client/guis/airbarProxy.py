#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/airbarProxy.o
import BigWorld
import gameglobal
import keys
from appSetting import Obj as AppSettings
from guis import events
from guis import ui
from guis import uiConst
from guis import uiUtils
from helpers.eventDispatcher import Event
from Scaleform import GfxValue
from uiProxy import SlotDataProxy
from sfx import keyboardEffect
APP_SETTING_AIRBAR_PATH = keys.SET_UI_INFO + '/airbar/'
ASAP_LOCK = APP_SETTING_AIRBAR_PATH + 'lock'

class AirbarProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(AirbarProxy, self).__init__(uiAdapter)
        self.modelMap = {'setLockState': self.onSetLockState,
         'getLockState': self.onGetLockState,
         'getAirbarData': self.onGetAirbarData}
        self.bindType = 'airbar'
        self.type = 'airbar'
        self.binding = {}
        self.airBarMediator = None
        self.airBarWidgetId = uiConst.WIDGET_AIR_BATTLE_BAR
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.airBarWidgetId:
            self.initAirBarData()
            self.airBarMediator = mediator
            self.checkAvatarState()
            self.setSlotKeyText()

    def reset(self):
        self.airBarMediator = None
        self.isLock = AppSettings.get(ASAP_LOCK, 0) == 1
        self.showMouseIcon(True)
        self.airShortCut = {}
        self.binding = {}

    def airbarSlotKey(self):
        slotKey = []
        slotKey_org = gameglobal.rds.ui.actionbar.slotKey[0:uiConst.MAX_AIRBAR_SLOT_NUM]
        operationMode = BigWorld.player().getOperationMode()
        if operationMode == gameglobal.ACTION_MODE:
            slotKey.extend(slotKey_org[-2:])
            slotKey.extend(slotKey_org[0:-2])
        else:
            slotKey.extend(slotKey_org)
        return slotKey

    def setSlotKeyText(self):
        ret = []
        slotKey = self.airbarSlotKey()
        operationMode = BigWorld.player().getOperationMode()
        for i, item in enumerate(slotKey):
            if len(item) > 4:
                item = '...'
            ret.append(item)

        if self.airBarMediator:
            self.airBarMediator.Invoke('setSlotKeyText', (uiUtils.array2GfxAarry(ret), GfxValue(operationMode)))

    def showAirbar(self, visble):
        enableAirSkill = gameglobal.rds.configData.get('enableAirSkill', False)
        if not enableAirSkill:
            visble = False
        self.checkOtherBarState()
        if gameglobal.rds.ui.isHideAllUI():
            self.uiAdapter.setWidgetVisible(self.airBarWidgetId, visble)
        elif self.airBarMediator:
            self.airBarMediator.Invoke('setVisible', GfxValue(visble))

    def showMouseIcon(self, bShow):
        if self.airBarMediator != None:
            self.airBarMediator.Invoke('showMouseIcon', GfxValue(bShow))

    def getSlotID(self, key):
        bar, slotId = key.split('.')
        return (int(bar[6:]), int(slotId[4:]))

    def getSkillId(self, key):
        type, slotId = self.getSlotID(key)
        return self.getSkillIdByPos(type, slotId)

    def getSkillIdByPos(self, page, pos):
        if page == uiConst.AIR_SKILL_BAR:
            return self.airShortCut.get(pos, (uiConst.SHORTCUT_TYPE_SKILL, 0))[1]
        else:
            return 0

    def getPosBySkillId(self, skillId):
        for slot in xrange(uiConst.MAX_AIRBAR_SLOT_NUM):
            sid = self.getSkillIdByPos(uiConst.AIR_SKILL_BAR, slot)
            if sid == skillId:
                return slot

        return -1

    def getAirbarSkills(self):
        ret = []
        for slot in range(uiConst.MAX_AIRBAR_SLOT_NUM):
            skillId = self.getSkillIdByPos(uiConst.AIR_SKILL_BAR, slot)
            if skillId != 0:
                ret.append(skillId)

        return ret

    def _getKey(self, bar, slotId):
        return 'airbar%d.slot%d' % (bar, slotId)

    def onNotifySlotUse(self, *arg):
        page, pos = self.getSlotID(arg[3][0].GetString())
        self.useItem(page, pos, False, False)

    def onNotifySlotMouseDown(self, *arg):
        page, pos = self.getSlotID(arg[3][0].GetString())
        self.useItem(page, pos, True, False)

    def onSlotMouseOver(self, *arg):
        skillId = self.getSkillId(arg[3][0].GetString())
        if skillId != 0:
            BigWorld.player().playHoverEffect(skillId)

    def onSlotMouseOut(self, *arg):
        skillId = self.getSkillId(arg[3][0].GetString())
        if skillId != 0:
            BigWorld.player().stopHoverEffect()

    def checkOtherBarState(self):
        gameglobal.rds.ui.bullet.checkAvatarState()
        gameglobal.rds.ui.actionbar.checkAvatarState()

    def checkAvatarState(self):
        self.showAirbar(gameglobal.rds.ui.skill.inAirBattleState())

    def setAirSlotsShine(self, enabled):
        if self.airBarMediator:
            self.airBarMediator.Invoke('setAirSlotsShine', GfxValue(enabled))

    def setAirSlotsState(self, state):
        for slot in range(uiConst.MAX_AIRBAR_SLOT_NUM):
            self.setSlotState(slot, state)

        alpha = 1 if state == uiConst.SKILL_ICON_STAT_USEABLE else 0.3
        if self.airBarMediator:
            self.airBarMediator.Invoke('getWidget').SetMember('alpha', GfxValue(alpha))

    def setSlotState(self, idSlot, state):
        key = self._getKey(uiConst.AIR_SKILL_BAR, idSlot)
        if key and self.binding.get(key) != None:
            self.binding[key][0].Invoke('setSlotState', GfxValue(state))
            keyboardEffect.addSlotStateEffect(uiConst.AIR_SKILL_BAR, idSlot, state)

    def setSlotStateBySkillId(self, skillId, state):
        idSlot = self.getPosBySkillId(skillId)
        if idSlot < 0:
            return
        self.setSlotState(idSlot, state)

    def initAirBarData(self):
        if hasattr(BigWorld.player(), 'shortcutData'):
            shortCutData = BigWorld.player().shortcutData
            for i in xrange(uiConst.MAX_AIRBAR_SLOT_NUM):
                self.airShortCut[i] = shortCutData.get((uiConst.AIR_SKILL_BAR, i), (uiConst.SHORTCUT_TYPE_SKILL, 0))

        gameglobal.rds.ui.skill.initAirSkillData()

    def skillPanelOrig2Airbar(self, srcPos, desPos):
        gameglobal.rds.ui.skill.airSkillDragFromOrig2Slot(srcPos, desPos)

    def airbar2Airbar(self, srcPos, desPos):
        gameglobal.rds.ui.skill.airSkillDragFromSlot2Slot(srcPos, desPos)

    def airbar2Null(self, srcPos):
        skillId = self.getSkillIdByPos(uiConst.AIR_SKILL_BAR, srcPos)
        if skillId != 0:
            BigWorld.player().cell.disableAirSkill(skillId)
        gameglobal.rds.ui.skill.setAirSkillItem(0, srcPos)

    def setAirSkillItem(self, skillId, slotPos):
        self.stopCoolDown(uiConst.AIR_SKILL_BAR, slotPos)
        self.setSlotState(slotPos, uiConst.SKILL_ICON_STAT_USEABLE)
        self.saveAirSkillShortCut()
        self.refreshAirSkillBar()
        gameglobal.rds.ui.actionbar.initSkillStat(skillId)
        gameglobal.rds.ui.actionbar.updateSlots()

    def saveAirSkillShortCut(self):
        p = BigWorld.player()
        pShortCut = p.shortcutData
        for i in range(uiConst.MAX_AIRBAR_SLOT_NUM):
            sInfo = self.airShortCut[i]
            pKey = (uiConst.AIR_SKILL_BAR, i)
            if sInfo[1] == 0:
                if pShortCut.has_key(pKey):
                    pShortCut.pop(pKey)
                    if gameglobal.rds.ui.actionbar.clientShortCut.has_key(pKey):
                        gameglobal.rds.ui.actionbar.clientShortCut.pop(pKey)
            else:
                pShortCut[pKey] = sInfo
                gameglobal.rds.ui.actionbar.clientShortCut[pKey] = sInfo

        p.saveShortcut(pShortCut)

    def refreshAirSkillBar(self):
        if self.airBarMediator:
            self.airBarMediator.Invoke('refreshAirBattleBar')

    def transForActionMode(self, pos):
        if BigWorld.player().getOperationMode() != gameglobal.ACTION_MODE:
            return pos
        if pos == 10:
            pos = 0
        elif pos == 11:
            pos = 1
        else:
            if pos < 0 or pos >= uiConst.MAX_AIRBAR_SLOT_NUM:
                pos = -1
                return pos
            pos = (pos + 2) % uiConst.MAX_AIRBAR_SLOT_NUM
        return pos

    def useItem(self, page, pos, isDown = False, isKeyMode = True, autoUseSkill = False):
        if isKeyMode:
            pos = self.transForActionMode(pos)
        if pos < 0:
            return
        skillId = self.getSkillIdByPos(page, pos)
        if skillId == 0:
            return
        isDown = bool(isDown)
        isKeyMode = bool(isKeyMode)
        if page == uiConst.AIR_SKILL_BAR and isDown:
            if self.airBarMediator:
                self.airBarMediator.Invoke('slotShake', GfxValue(pos))
        gameglobal.rds.ui.actionbar.useSkill(page, pos, isDown, isKeyMode, autoUseSkill)

    def canUseItem(self, isDown, isKeyMode):
        return not isDown ^ isKeyMode

    def stopCoolDown(self, page, pos):
        key = self._getKey(page, pos)
        if not self.binding.has_key(key):
            return
        bindingSlot = self.binding[key]
        if bindingSlot[0] != None:
            bindingSlot[0].Invoke('stopCooldown')

    @ui.uiEvent(uiConst.WIDGET_AIR_BATTLE_BAR, events.EVENT_ACTIONBAR_LOCK)
    def onEventLockChanged(self, event):
        if event.data['lockSrc'] == self.type:
            return
        self.isLock = event.data['locked']
        AppSettings[ASAP_LOCK] = 1 if self.isLock else 0
        if self.airBarMediator:
            self.airBarMediator.Invoke('refreshLockState')

    def onSetLockState(self, *arg):
        if arg[3][0] is None:
            return
        self.isLock = arg[3][0].GetBool()
        AppSettings[ASAP_LOCK] = 1 if self.isLock else 0
        lEvent = Event(events.EVENT_ACTIONBAR_LOCK, {'lockSrc': self.type,
         'locked': self.isLock})
        self.dispatchEvent(lEvent)

    def onGetLockState(self, *arg):
        return GfxValue(self.isLock)

    def onGetAirbarData(self, *arg):
        return gameglobal.rds.ui.skill.onGetAirSkillbarInfo()

    def onGetToolTip(self, *arg):
        skillId = self.getSkillId(arg[3][0].GetString())
        if skillId == 0:
            return GfxValue('')
        else:
            return gameglobal.rds.ui.skill.formatTooltip(skillId)
