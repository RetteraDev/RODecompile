#Embedded file name: I:/bag/tmp/tw2/res/entities\client\sfx/keyboardEffect.o
import BigWorld
import keys
import const
import gameglobal
from guis import ui
from guis import uiConst
from guis import hotkey as HK
from gameclass import Singleton
from data import keyboardEffect_config_data as KCD
BASE_PARAM_IDX = 6
HOT_PARAM_IDX = 7
ETYPE_PARAM_IDX = 9
DEF_TAG = 'idle'
DEF_COLOR = (255, 255, 255)
DEF_PRIORITY = 0
DEF_TIME = -1
DEF_BASE = False
DEF_KEY = 1
KEY_DICT = {'effect_pushMsg': (keys.KEY_J, False),
 'effect_loading': (DEF_KEY, False),
 'effect_selectChar': (keys.KEY_J, False),
 'effect_pickItem': (HK.KEY_PICK_ITEM, True),
 'effect_love': (DEF_KEY, False),
 'effect_hp': (keys.KEY_SPACE, False),
 'effect_background': (DEF_KEY, False),
 'effect_mail': (HK.KEY_SHOW_MAIL, True),
 'effect_friendMsg': (HK.KEY_SHOW_FRIEND, True)}
KEY_QINGGONG = [HK.KEY_FORWARD,
 HK.KEY_MOVELEFT,
 HK.KEY_MOVERIGHT,
 HK.KEY_BACKWARD]
HP_HIGH_COLOR = (0, 255, 0)
HP_MID_COLOR = (233, 150, 122)
HP_LOW_COLOR = (255, 0, 0)
HP_DYING_COLOR = HP_LOW_COLOR
HP_ZERO = 0
HP_DYING = 1
HP_LOW = 2
HP_MID = 3
HP_HIGH = 4
HP_COLOR = [DEF_COLOR,
 HP_DYING_COLOR,
 HP_LOW_COLOR,
 HP_MID_COLOR,
 HP_HIGH_COLOR]
SKILL_TOTALCNT = 18
SKILL_NORMALCNT = 12
NOT_SKILL = -1
SKILL_NORMAL = 0
SKILL_WUSHUANG = 1
SKILL_ZAIJU = 2
SKILL_AIR = 3
FLY_SKILL_TYPES = [SKILL_AIR]
NOT_FLY_SKILL_TYPES = [SKILL_NORMAL, SKILL_WUSHUANG, SKILL_ZAIJU]
SKILL_ETYPE_DISABLE = 0
SKILL_ETYPE_ENABLE = 1
SKILL_ETYPE_CD = 2
SKILL_ETYPE_USED = 3
SKILL_ETYPE_CANUSE = 4
SKILL_ETYPE_GUIDING = 5
SKILL_ETYPE_LIGHT = 6
SKILL_ETYPE_DARK = 7
SKILL_NORMAL_EFFECT = ['effect_skill_normal_disable',
 'effect_skill_normal_enable',
 'effect_skill_normal_cd',
 'effect_skill_normal_used',
 '',
 '']
SKILL_WUSHUANG_EFFECT = ['effect_skill_wushuang_disable',
 'effect_skill_wushuang_enable',
 'effect_skill_wushuang_cd',
 'effect_skill_wushuang_used',
 'effect_skill_wushuang_canUse',
 'effect_skill_wushuang_guiding',
 'effect_skill_wushuang_light',
 'effect_skill_wushuang_dark']
WUSHUANG_LEFT_SLOTS_ID = (12, 13, 14)
WUSHUANG_RIGHT_SLOTS_ID = (15, 16, 17)
LIUGUANG_STATE_DARK = 1
LIUGUANG_STATE_LIGHT = 2

class Slot(object):

    def __init__(self, skillSlot):
        self.slotId = skillSlot.slotId
        self.stateEffect = skillSlot.stateEffect
        self.isInCD = skillSlot.isInCD
        self.isGuiding = skillSlot.isGuiding

    def resetEffect(self):
        self.stateEffect = None
        self.isInCD = False
        self.isGuiding = False


class SkillSlot(object):

    def __init__(self, slotId):
        self.slotId = slotId
        self.skillType = SKILL_NORMAL
        self.effectName = []
        self._stateEffect = []
        self._isInCD = False
        self._isGuiding = False
        self.enable = True

    def resetEffect(self):
        self.stateEffect = None
        self.isInCD = False
        self.isGuiding = False

    def get_stateEffect(self):
        return self._stateEffect

    def set_stateEffect(self, new):
        if not self.enable:
            return
        if new is None:
            new = []
        if self._stateEffect == new:
            return
        old = self._stateEffect
        union = list(set(old).union(set(new)))
        for item in union:
            if item not in new:
                name, hotkey = self.getNameAndHotkey(item)
                self.removeSkillEffect(name, hotkey)
            if item not in old:
                name, hotkey = self.getNameAndHotkey(item)
                self.addSkillEffect(name, hotkey)

        self._stateEffect = new

    stateEffect = property(get_stateEffect, set_stateEffect)

    def get_isInCD(self):
        return self._isInCD

    def set_isInCD(self, new):
        if not self.enable:
            return
        if self._isInCD == new:
            return
        nameUsed, hotkeyUsed = self.getNameAndHotkey(SKILL_ETYPE_USED)
        nameCD, hotkeyCD = self.getNameAndHotkey(SKILL_ETYPE_CD)
        if new:
            self.addSkillEffect(nameUsed, hotkeyUsed)
            self.addSkillEffect(nameCD, hotkeyCD)
        else:
            self.removeSkillEffect(nameUsed, hotkeyUsed)
            self.removeSkillEffect(nameCD, hotkeyCD)
        self._isInCD = new

    isInCD = property(get_isInCD, set_isInCD)

    def get_isGuiding(self):
        return self._isGuiding

    def set_isGuiding(self, new):
        if not self.enable:
            return
        if self._isGuiding == new:
            return
        nameGuide, hotkey = self.getNameAndHotkey(SKILL_ETYPE_GUIDING)
        if new:
            self.addSkillEffect(nameGuide, hotkey)
        else:
            self.removeSkillEffect(nameGuide, hotkey)
        self._isGuiding = new

    isGuiding = property(get_isGuiding, set_isGuiding)

    def getNameAndHotkey(self, eType):
        name = self.effectName[eType]
        if self.skillType == SKILL_AIR:
            hotkey = AirSkillSlot.getAirbarHotKey(self.slotId)
        else:
            hotkey = HK.SHORCUT_SKILL_KEYS[self.slotId]
        return (name, hotkey)

    def addSkillEffect(self, name, key):
        tag, color, priority, time, isBase = KCD.data.get(name, (None, None, None, None, None))
        alpha = KCD.data.get('alpha', {}).get(name, 1)
        tag and ins.addKeyboardEffect(tag, key, color, priority, time, isBase, True, alpha, self.skillType)

    def removeSkillEffect(self, name, key):
        tag = KCD.data.get(name, (None,))[0]
        tag and ins.removeKeyboardEffect(tag, key)

    def setValBySlot(self, slot):
        self.slotId = slot.slotId
        self.stateEffect = slot.stateEffect
        self.isInCD = slot.isInCD
        self.isGuiding = slot.isGuiding


class NormalSkillSlot(SkillSlot):

    def __init__(self, slotId):
        super(NormalSkillSlot, self).__init__(slotId)
        self.skillType = SKILL_NORMAL
        self.effectName = SKILL_NORMAL_EFFECT


class WuShuangSkillSlot(SkillSlot):

    def __init__(self, slotId):
        super(WuShuangSkillSlot, self).__init__(slotId)
        self.skillType = SKILL_WUSHUANG
        self.effectName = SKILL_WUSHUANG_EFFECT

    def set_isInCD(self, new):
        if not self.enable:
            return
        old = self._isInCD
        super(WuShuangSkillSlot, self).set_isInCD(new)
        if old == new:
            return
        nameCanUse, hotkey = self.getNameAndHotkey(SKILL_ETYPE_CANUSE)
        if new:
            self.removeSkillEffect(nameCanUse, hotkey)
        elif SKILL_ETYPE_ENABLE in self.stateEffect:
            self.addSkillEffect(nameCanUse, hotkey)

    isInCD = property(SkillSlot.get_isInCD, set_isInCD)

    def set_stateEffect(self, new):
        if not self.enable:
            return
        if new is None:
            new = []
        old = self._stateEffect
        super(WuShuangSkillSlot, self).set_stateEffect(new)
        if old == new:
            return
        nameCanUse, hotkey = self.getNameAndHotkey(SKILL_ETYPE_CANUSE)
        if SKILL_ETYPE_DISABLE in new:
            self.removeSkillEffect(nameCanUse, hotkey)
        elif SKILL_ETYPE_ENABLE in self.stateEffect and not self.isInCD:
            self.addSkillEffect(nameCanUse, hotkey)

    stateEffect = property(SkillSlot.get_stateEffect, set_stateEffect)


class ZaijuSkillSlot(SkillSlot):

    def __init__(self, slotId):
        super(ZaijuSkillSlot, self).__init__(slotId)
        self.skillType = SKILL_ZAIJU
        self.effectName = SKILL_NORMAL_EFFECT


class AirSkillSlot(SkillSlot):

    def __init__(self, slotId):
        super(AirSkillSlot, self).__init__(slotId)
        self.skillType = SKILL_AIR
        self.effectName = SKILL_NORMAL_EFFECT
        self.hotkeys = None

    @staticmethod
    def getAirbarHotKey(slotId):
        slotKey = []
        slotKey_org = HK.SHORTCUT_KEYS[0:uiConst.MAX_AIRBAR_SLOT_NUM]
        operationMode = BigWorld.player().getOperationMode()
        if operationMode == gameglobal.ACTION_MODE:
            slotKey.extend(slotKey_org[-2:])
            slotKey.extend(slotKey_org[0:-2])
        else:
            slotKey = slotKey_org
        return slotKey[slotId]


class KeyBoardEffectManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(KeyBoardEffectManager, self).__init__()
        self.effectDict = {}
        self.skillSlots = [{},
         {},
         {},
         {}]
        self.skillCaches = [{},
         {},
         {},
         {}]
        self.guideSlot = None
        self.hpEffectId = None
        self.qinggongKey = None
        self.hpState = -1
        self.resetSKillSlot()
        self._baseColor = (0, 0, 0)
        self._zaijuState = False

    def reset(self):
        self.clear()
        self.resetSKillSlot()
        self._baseColor = (0, 0, 0)
        self._zaijuState = False

    def clear(self):
        self.removeHpEffect()
        for slots in self.skillSlots:
            for slot in slots.values():
                slot.resetEffect()

        for tagkey in self.effectDict:
            effectId = self.effectDict[tagkey][0]
            effectId and BigWorld.removeKeyboardEffect(effectId)

    def resetSKillSlot(self):
        self.skillSlots[SKILL_NORMAL] = {idx:NormalSkillSlot(idx) for idx in xrange(SKILL_NORMALCNT)}
        self.skillSlots[SKILL_WUSHUANG] = {idx:WuShuangSkillSlot(idx) for idx in xrange(SKILL_NORMALCNT, SKILL_TOTALCNT)}
        self.skillSlots[SKILL_AIR] = {idx:AirSkillSlot(idx) for idx in xrange(uiConst.MAX_AIRBAR_SLOT_NUM)}
        self.skillCaches[SKILL_NORMAL] = {idx:Slot(self.skillSlots[SKILL_NORMAL][idx]) for idx in xrange(SKILL_NORMALCNT)}
        self.skillCaches[SKILL_WUSHUANG] = {idx:Slot(self.skillSlots[SKILL_WUSHUANG][idx]) for idx in xrange(SKILL_NORMALCNT, SKILL_TOTALCNT)}
        self.skillCaches[SKILL_AIR] = {idx:Slot(self.skillSlots[SKILL_AIR][idx]) for idx in xrange(uiConst.MAX_AIRBAR_SLOT_NUM)}

    def canControlKeyboard(self):
        if not gameglobal.rds.configData.get('enableKeyboardEffect', False):
            return False
        if not hasattr(BigWorld, 'canControlKeyboard'):
            return False
        return BigWorld.canControlKeyboard()

    def get_baseColor(self):
        return self._baseColor

    def set_baseColor(self, newVal):
        if newVal == self._baseColor:
            return
        self._baseColor = newVal
        baseList = [ item for item in self.effectDict.values() if item[BASE_PARAM_IDX] ]
        for info in baseList:
            self.addKeyboardEffect(info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9])

    baseColor = property(get_baseColor, set_baseColor)

    def get_zaijuState(self):
        return self._zaijuState

    def set_zaijuState(self, newState):
        if newState == self._zaijuState:
            return
        eTypeFilter = [SKILL_NORMAL, SKILL_WUSHUANG] if newState else [SKILL_ZAIJU]
        removeList = [ item for item in self.effectDict.values() if item[ETYPE_PARAM_IDX] in eTypeFilter ]
        for item in removeList:
            self.removeKeyboardEffect(item[1], item[2])

        self._zaijuState = newState

    zaijuState = property(get_zaijuState, set_zaijuState)

    def judgeCanAddEffect(self, eType):
        p = BigWorld.player()
        if not p:
            return True
        if eType is NOT_SKILL:
            return True
        if self.zaijuState and eType != NOT_SKILL:
            return False
        return True

    def transformColor(self, color, alpha, isBase):
        if isBase:
            color = self.baseColor
        if 0 <= alpha < 1:
            color = tuple([ int(c * alpha) for c in color ])
        return color

    def addKeyboardEffect(self, tag, key, color, priority, time, isBase, isHotkey, alpha, eType = NOT_SKILL):
        if not self.judgeCanAddEffect(eType):
            return
        tagkey = tag + str(key)
        self.removeKeyboardEffect(tag, key)
        trueColor = self.transformColor(color, alpha, isBase)
        trueKey = HK.HKM[key].key if isHotkey else key
        effectId = BigWorld.addKeyboardEffect(trueKey, tag, trueColor, priority, time) if trueKey != 0 else 0
        self.effectDict[tagkey] = (effectId,
         tag,
         key,
         trueColor,
         priority,
         time,
         isBase,
         isHotkey,
         alpha,
         eType)
        return effectId

    def removeKeyboardEffect(self, tag, key):
        tagkey = tag + str(key)
        if tagkey in self.effectDict:
            effectId = self.effectDict[tagkey][0]
            effectId and BigWorld.removeKeyboardEffect(effectId)
            del self.effectDict[tagkey]

    def updateHpEffect(self):
        p = BigWorld.player()
        newState = self.getHpState(p.hp, p.mhp)
        if self.hpState == newState:
            return
        self.hpState = newState
        self.removeHpEffect()
        if self.hpState == HP_ZERO:
            return
        tag, _, priority, time, _ = self.getHpEffectParam()
        color = KCD.data.get('color_hp', HP_COLOR)[self.hpState]
        key, _ = KEY_DICT['effect_hp']
        self.hpEffectId = BigWorld.addKeyboardEffect(key, tag, color, priority, time)

    def removeHpEffect(self):
        if self.hpEffectId is None:
            return
        BigWorld.removeKeyboardEffect(self.hpEffectId)
        self.hpEffectId = None

    def getHpState(self, hp, mhp):
        hpRatio = float(1.0 * hp / mhp)
        if 0.7 <= hpRatio <= 1.0:
            return HP_HIGH
        elif 0.3 <= hpRatio < 0.7:
            return HP_MID
        elif 0.2 <= hpRatio < 0.3:
            return HP_LOW
        elif 0 < hpRatio < 0.2:
            return HP_DYING
        else:
            return HP_ZERO

    def getHpEffectParam(self):
        if self.hpState != HP_ZERO and self.hpState != HP_DYING:
            return KCD.data.get('effect_hp')
        else:
            return KCD.data.get('effect_dying')

    def refreshHotkeyEffect(self):
        hotList = [ item for item in self.effectDict.values() if item[HOT_PARAM_IDX] ]
        for info in hotList:
            self.addKeyboardEffect(info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9])

    def addGuideEffect(self, bar, slotId):
        self.guideSlot = self.setDestSlotAttr(bar, slotId, 'isGuiding', True)

    def removeGuideEffect(self):
        if self.guideSlot is None:
            return
        self.guideSlot.isGuiding = False
        self.guideSlot = None

    def changeSchoolStateEffect(self, school, state):
        if school == const.SCHOOL_LIUGUANG:
            sideSlots = WUSHUANG_LEFT_SLOTS_ID if state == LIUGUANG_STATE_DARK else WUSHUANG_RIGHT_SLOTS_ID
            self.notifyWushuangSide(sideSlots)

    def notifyWushuangSide(self, sideSlots):
        for slotId, slot in self.skillSlots[SKILL_WUSHUANG].iteritems():
            nameLight, hotkey = slot.getNameAndHotkey(SKILL_ETYPE_LIGHT)
            nameDark, hotkey = slot.getNameAndHotkey(SKILL_ETYPE_DARK)
            if slotId in sideSlots:
                slot.addSkillEffect(nameLight, hotkey)
                slot.removeSkillEffect(nameDark, hotkey)
                slot.enable = True
            else:
                slot.resetEffect()
                slot.addSkillEffect(nameDark, hotkey)
                slot.removeSkillEffect(nameLight, hotkey)
                slot.enable = False

    def hasNeedEffectMsg(self):
        pushMsgs = gameglobal.rds.ui.pushMessage.msgs
        for msg in KCD.data.get('needEffectMsgType'):
            if msg in pushMsgs:
                return True

        return False

    def getSkillTypeBySlotId(self, bar, slotId):
        skillType = SKILL_NORMAL
        if bar == uiConst.SKILL_ACTION_BAR:
            skillType = SKILL_NORMAL if slotId < SKILL_NORMALCNT else SKILL_WUSHUANG
        elif bar == uiConst.AIR_SKILL_BAR:
            skillType = SKILL_AIR
        return skillType

    def setDestSlotAttr(self, bar, slotId, attrName, attrVal):
        p = BigWorld.player()
        skillType = self.getSkillTypeBySlotId(bar, slotId)
        isInFly = p.inFly
        isFlySkill = skillType == SKILL_AIR
        if isInFly ^ isFlySkill:
            destSlot = self.skillCaches[skillType][slotId]
        else:
            destSlot = self.skillSlots[skillType][slotId]
        setattr(destSlot, attrName, attrVal)
        return destSlot


ins = KeyBoardEffectManager.getInstance()

def canControlKeyboard():
    return ins.canControlKeyboard()


def clearAllEffect():
    if not ins.canControlKeyboard():
        return
    ins.reset()


def addKeyboardEffect(name):
    if not ins.canControlKeyboard():
        return None
    key, isHotkey = KEY_DICT[name]
    tag, color, priority, time, isBase = KCD.data.get(name, (None, None, None, None, None))
    alpha = KCD.data.get('alpha', {}).get(name, 1)
    tag and ins.addKeyboardEffect(tag, key, color, priority, time, isBase, isHotkey, alpha)


def removeKeyboardEffect(name):
    if not ins.canControlKeyboard():
        return
    key = KEY_DICT[name][0]
    tag = KCD.data.get(name, (DEF_TAG,))[0]
    tag and ins.removeKeyboardEffect(tag, key)


@ui.callInCD(0.5)
def updateBaseColor(school = 0, state = 0):
    if not ins.canControlKeyboard():
        return
    old = ins.baseColor
    new = KCD.data.get('color_schoolState', {}).get(school, {}).get(state, DEF_COLOR)
    if old != new:
        ins.baseColor = new
        ins.changeSchoolStateEffect(school, state)


@ui.callInCD(0.5)
def updateZaijuState(state):
    if not ins.canControlKeyboard():
        return
    ins.zaijuState = state


@ui.callInCD(0.5)
def addSelectCharKBE(school = 0):
    if not ins.canControlKeyboard():
        return
    tag, color, priority, time, isBase = KCD.data.get('effect_selectChar', (None, None, None, None, None))
    if tag is None:
        return
    color = KCD.data.get('color_selectChar').get(school, DEF_COLOR)
    key, isHotkey = KEY_DICT['effect_selectChar']
    alpha = KCD.data.get('alpha', {}).get('effect_selectChar', 1)
    ins.addKeyboardEffect(tag, key, color, priority, time, False, isHotkey, alpha)


def refreshHotkeyEffect():
    if not ins.canControlKeyboard():
        return
    ins.refreshHotkeyEffect()


def removeSelectCharKBE():
    if not ins.canControlKeyboard():
        return
    tag = KCD.data.get('effect_selectChar', (DEF_TAG,))[0]
    key = KEY_DICT['effect_selectChar'][0]
    ins.removeKeyboardEffect(tag, key)


def getQinggongKey():
    ret = HK.KEY_FORWARD
    for key in KEY_QINGGONG:
        if HK.HKM[key].isAnyDown():
            ret = key

    return ret


def addQinggongEffect():
    if not ins.canControlKeyboard():
        return None
    if ins.qinggongKey:
        return None
    tag, color, priority, time, isBase = KCD.data.get('effect_qinggong', (None, None, None, None, None))
    alpha = KCD.data.get('alpha', {}).get('effect_qinggong', 1)
    ins.qinggongKey = getQinggongKey()
    ins.addKeyboardEffect(tag, ins.qinggongKey, color, priority, time, isBase, True, alpha)


def removeQinggongEffect():
    if not ins.canControlKeyboard():
        return
    tag = KCD.data.get('effect_qinggong', (DEF_TAG,))[0]
    ins.removeKeyboardEffect(tag, ins.qinggongKey)
    ins.qinggongKey = None


def addPushMsgEffect(msgType):
    if not ins.canControlKeyboard():
        return
    if msgType not in KCD.data.get('needEffectMsgType'):
        return
    p = BigWorld.player()
    if p and p.isInBfDota():
        return
    ins.hasNeedEffectMsg() and addKeyboardEffect('effect_pushMsg')


def removePushMsgEffect(msgType):
    if not ins.canControlKeyboard():
        return
    if msgType not in KCD.data.get('needEffectMsgType'):
        return
    ins.hasNeedEffectMsg() or removeKeyboardEffect('effect_pushMsg')


def addWASDEffect():
    if not ins.canControlKeyboard():
        return
    tag, color, priority, time, isBase = KCD.data.get('effect_wasd', (None, None, None, None, None))
    if tag is None:
        return
    alpha = KCD.data.get('alpha', {}).get('effect_wasd', 1)
    ins.addKeyboardEffect(tag, HK.KEY_FORWARD, color, priority, time, isBase, True, alpha)
    ins.addKeyboardEffect(tag, HK.KEY_BACKWARD, color, priority, time, isBase, True, alpha)
    ins.addKeyboardEffect(tag, HK.KEY_MOVELEFT, color, priority, time, isBase, True, alpha)
    ins.addKeyboardEffect(tag, HK.KEY_MOVERIGHT, color, priority, time, isBase, True, alpha)


def removeWASDEffect():
    if not ins.canControlKeyboard():
        return
    tag = KCD.data.get('effect_wasd', (None,))[0]
    if tag is None:
        return
    ins.addKeyboardEffect(tag, HK.KEY_FORWARD)
    ins.addKeyboardEffect(tag, HK.KEY_BACKWARD)
    ins.addKeyboardEffect(tag, HK.KEY_MOVELEFT)
    ins.addKeyboardEffect(tag, HK.KEY_MOVERIGHT)


@ui.callAfterTime()
def updateHpEffect():
    if not ins.canControlKeyboard():
        return
    ins.updateHpEffect()


def removeHpEffect():
    if not ins.canControlKeyboard():
        return
    ins.removeHpEffect()


def isValidBar(bar):
    return bar in [uiConst.SKILL_ACTION_BAR, uiConst.AIR_SKILL_BAR]


def addSlotCDEffect(bar, slotId):
    if not ins.canControlKeyboard():
        return
    if not isValidBar(bar):
        return
    ins.setDestSlotAttr(bar, slotId, 'isInCD', True)


def removeSlotCDEffect(bar, slotId):
    if not ins.canControlKeyboard():
        return
    if not isValidBar(bar):
        return
    ins.setDestSlotAttr(bar, slotId, 'isInCD', False)


def addSlotStateEffect(bar, slotId, state):
    if not ins.canControlKeyboard():
        return
    if not isValidBar(bar):
        return
    stateEffect = [SKILL_ETYPE_ENABLE] if state == 1 else [SKILL_ETYPE_DISABLE]
    ins.setDestSlotAttr(bar, slotId, 'stateEffect', stateEffect)


def removeSlotStateEffect(bar, slotId):
    if not ins.canControlKeyboard():
        return
    if not isValidBar(bar):
        return
    ins.setDestSlotAttr(bar, slotId, 'stateEffect', None)


def addGuideEffect(bar, slotId):
    if not ins.canControlKeyboard():
        return
    if not isValidBar(bar):
        return
    ins.addGuideEffect(bar, slotId)


def removeGuideEffect():
    if not ins.canControlKeyboard():
        return
    ins.removeGuideEffect()


def exchangeAllSlotEffect(removeSkillTypes, addSkillTypes):
    if not ins.canControlKeyboard():
        return
    for skillType in removeSkillTypes:
        for skillSlot in ins.skillSlots[skillType].values():
            slotId = skillSlot.slotId
            ins.skillCaches[skillType][slotId] = Slot(skillSlot)
            skillSlot.resetEffect()

    for skillType in addSkillTypes:
        for cacheSlot in ins.skillCaches[skillType].values():
            slotId = cacheSlot.slotId
            ins.skillSlots[skillType][slotId].setValBySlot(cacheSlot)
            cacheSlot.resetEffect()


def removeEffectsEnterBfDota():
    if not ins.canControlKeyboard():
        return
    removeKeyboardEffect('effect_pushMsg')


def addEffectsLeaveBfData():
    if not ins.canControlKeyboard():
        return
    ins.hasNeedEffectMsg() and addKeyboardEffect('effect_pushMsg')
