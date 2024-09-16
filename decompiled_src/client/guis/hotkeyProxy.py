#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/hotkeyProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import gameglobal
import keys
import gamelog
import formula
import copy
from guis import hotkey as HK
from uiProxy import UIProxy
from gameclass import Singleton
from gameStrings import gameStrings
from cdata import key_description_data as KDD
excludeKey = (20,
 17,
 16,
 8,
 46,
 18)
excludeComKey = ((32, 1), (32, 2), (190, 2))
asc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = '0123456789'
flag = '*+E-./'
keyMap = {8: 'BACKSPACE',
 20: 'CAPSLOCK',
 17: 'CTRL',
 46: 'DELETE',
 40: gameStrings.TEXT_HOTKEYPROXY_23,
 27: 'ESC',
 18: 'ALT',
 36: 'HOME',
 45: 'INSERT',
 37: gameStrings.TEXT_HOTKEYPROXY_24,
 34: 'PAGEDOWN',
 33: 'PAGEUP',
 39: gameStrings.TEXT_HOTKEYPROXY_24_1,
 16: 'SHIFT',
 32: gameStrings.TEXT_HOTKEYPROXY_25,
 9: 'TAB',
 38: gameStrings.TEXT_HOTKEYPROXY_25_1,
 186: ';',
 187: '=',
 188: '<',
 189: '-',
 190: '>',
 191: '/',
 192: '~',
 219: '[',
 220: '\\',
 221: ']',
 222: '\"',
 144: 'NUMBERLOCK',
 258: KDD.data.get(258, {}).get('description', ''),
 259: KDD.data.get(259, {}).get('description', ''),
 260: gameStrings.TEXT_HOTKEYPROXY_28,
 261: gameStrings.TEXT_HOTKEYPROXY_28_1,
 262: gameStrings.TEXT_HOTKEYPROXY_28_2,
 263: gameStrings.TEXT_HOTKEYPROXY_28_3,
 264: gameStrings.TEXT_HOTKEYPROXY_28_4,
 265: gameStrings.TEXT_HOTKEYPROXY_28_5}
keyCodeToGameKey = {}

def getGameKey(keyCode):
    global keyCodeToGameKey
    global excludeKey
    if keyCode in excludeKey:
        return
    elif keyCodeToGameKey.has_key(keyCode):
        return keyCodeToGameKey[keyCode]
    else:
        desc = decodeKeyCode(keyCode)
        gamelog.debug('bgf:getGameKey', desc)
        if desc:
            for key in KDD.data:
                data = KDD.data[key]
                if data['description'] == desc:
                    keyCodeToGameKey[keyCode] = key
                    break

        else:
            keyCodeToGameKey[keyCode] = None
        return keyCodeToGameKey.get(keyCode, None)


def getAsKey(keyCode):
    global asc
    global flag
    global keyMap
    global num
    if not KDD.data.has_key(keyCode):
        return 0
    desc = KDD.data[keyCode]['description']
    if desc in asc:
        return 65 + asc.index(desc)
    if desc in num:
        return 48 + num.index(desc)
    if desc == gameStrings.TEXT_HOTKEYPROXY_61:
        return 108
    if desc[0:-1] == gameStrings.TEXT_HOTKEYPROXY_63:
        desc = desc[-1]
        if desc in num:
            return 96 + num.index(desc)
        if desc in flag:
            return 106 + flag.index(desc)
    else:
        if desc[0] == 'F':
            return 111 + int(desc[1:])
        for key, value in keyMap.items():
            if desc == value:
                return key

    return 0


def decodeKeyCode(keyCode):
    gamelog.debug('jjh@hotkeyProxy.decodeKeyCode', len(asc), len(num))
    if keyCode >= 65 and keyCode <= 90:
        return asc[keyCode - 65]
    elif keyCode >= 48 and keyCode <= 57:
        return num[keyCode - 48]
    elif keyCode >= 96 and keyCode <= 105:
        return gameStrings.TEXT_HOTKEYPROXY_63 + num[keyCode - 96]
    else:
        if keyCode >= 106 and keyCode <= 111:
            ret = flag[keyCode - 106]
            if ret == 'E':
                return gameStrings.TEXT_HOTKEYPROXY_61
            else:
                return gameStrings.TEXT_HOTKEYPROXY_63 + ret
        else:
            if keyCode >= 112 and keyCode <= 126:
                return 'F' + str(keyCode - 111)
            if keyCode in keyMap:
                return keyMap[keyCode]
            return None
        return None


def getKeyContent(keyIndex):
    detial = HK.HKM[keyIndex]
    key = detial.key
    mods = detial.mods
    desc = detial.getDesc()
    if not key:
        key = detial.key2
        mods = detial.mods2
        desc = detial.getDesc(2)
    return (key, mods, desc)


def getKeyBriefContent(keyIndex):
    detial = HK.HKM[keyIndex]
    key = detial.key
    mods = detial.mods
    desc = detial.getBrief()
    if not key:
        key = detial.key2
        mods = detial.mods2
        desc = detial.getBrief(2)
    return (key, mods, desc)


def getAsKeyContent(keyIndex):
    key, mods, desc = getKeyContent(keyIndex)
    asKey = getAsKey(key)
    gamelog.debug('getAsKeyContent', key, mods, desc, asKey)
    return (asKey, mods, desc)


def getPickAsKeyContent():
    return getAsKeyContent(HK.KEY_PICK_ITEM)


def getChatLogSoundRecordKey():
    return getAsKeyContent(HK.KEY_CHATLOG_SOUND_RECORD)


def getChatToFriendSoundRecordKey():
    return getAsKeyContent(HK.KEY_CHAT_TO_FRIEND_SOUND_RECORD)


def filterModsKey(isDown, key, mods):
    if key in HK.ModKeys:
        controlDownKey = getInstance().contorlKey.getDownKey()
        newMod = HK.getModsNum(key)
        if mods != newMod and len(controlDownKey) == 1:
            return (isDown,
             key,
             mods,
             None)
        gamelog.debug('filterModsKey', controlDownKey, newMod)
        if len(controlDownKey) == 1:
            newKey = controlDownKey.pop()
            if isDown:
                return (isDown,
                 newKey,
                 newMod,
                 key)
            else:
                return (1,
                 newKey,
                 0,
                 key)
        else:
            return (isDown,
             key,
             newMod,
             key)
    return (isDown,
     key,
     mods,
     None)


def getInstance():
    return HotKeyManager.getInstance()


class HotKeyManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(HotKeyManager, self).__init__()
        self.keyMap = {}
        self.hotkeyMap = HK.HKM
        self.tagArray = ['moveBtn',
         'hotBtn',
         'uiBtn',
         'teamBtn',
         'actionBtn']
        self.tagClass = [ControlKey,
         ShortKey,
         UiKey,
         TeamKey,
         ActionKey]
        for i, tag in enumerate(self.tagArray):
            self.keyMap[tag] = self.tagClass[i](tag, self, '')

    @property
    def shortKey(self):
        return self.getSubKeyByTag('hotBtn')

    @property
    def contorlKey(self):
        return self.getSubKeyByTag('moveBtn')

    def getSubKeyByTag(self, tag):
        return self.keyMap.get(tag, None)

    def getKeyDesc(self):
        array = []
        for tag in self.tagArray:
            baseKey = self.keyMap[tag]
            array.append(baseKey.getKeyDesc())

        return array

    def searchSameKey(self, key, mods):
        array = []
        for tag in self.tagArray:
            baseKey = self.keyMap[tag]
            array.extend(baseKey.searchSameKey(key, mods))

        return array

    def set(self, tag, col, row, gameCode, mods):
        baseKey = self.keyMap[tag]
        baseKey.set(col, row, gameCode, mods)

    def getSingleKeyDesc(self, tag, col, row):
        baseKey = self.keyMap[tag]
        return baseKey.getSingleKeyDesc(col, row)

    def saveHotKey(self):
        dict = {}
        for tag in self.tagArray:
            baseKey = self.keyMap[tag]
            dict.update(baseKey.saveHotKey())

        HK.sendHotkey(dict)
        gameglobal.rds.ui.chat.updateSoundRecordTip()


class BaseKey(object):

    def __init__(self, tag, manager, name = ''):
        self.manager = manager
        self.tag = tag
        self.name = name
        self._defaultKey = []

    @property
    def defaultKey(self):
        return self._defaultKey

    @defaultKey.setter
    def defaultKey(self, value):
        self._defaultKey = value

    def getKeyDesc(self):
        array = []
        array.append((self.name,
         self.tag,
         self.tag,
         False))
        for key in self.defaultKey:
            detial = HK.HKM[key['key']]
            if not gameglobal.rds.configData.get('enableSkillMacro', False) or not gameglobal.rds.configData.get('enableOpenSkillMacroEntry', True):
                if key['key'] == HK.KEY_SKILL_MACRO:
                    continue
            if not gameglobal.rds.configData.get('enableSummonedSprite', False):
                if key['key'] in (HK.KEY_SPRITE_TELEPORT_BACK,
                 HK.KEY_SPRITE_MANUAL_SKILL,
                 HK.KEY_SPRITE_WAR,
                 HK.KEY_SELECT_TEAMER_ME_SPRITE):
                    continue
            if not gameglobal.rds.configData.get('enableTopChatRoom', False):
                if key['key'] == HK.KEY_CHAT_ROOM:
                    continue
            array.append((key['name'],
             detial.getDesc(1),
             detial.getDesc(2),
             key['key'] in HK.getForbideChangeKeyList()))

        return array

    def searchSameKey(self, gameKey, mods):
        array = []
        configData = gameglobal.rds.configData
        for i, key in enumerate(self.defaultKey):
            if not configData.get('enableNewItemSearch', False):
                if key['key'] == HK.KEY_ITEM_SOURCE:
                    continue
            if not configData.get('enableSkillMacro', False):
                if key['key'] == HK.KEY_SKILL_MACRO:
                    continue
            if not configData.get('enableSummonedSprite') and key['key'] in (HK.KEY_SPRITE_TELEPORT_BACK,
             HK.KEY_SPRITE_MANUAL_SKILL,
             HK.KEY_SPRITE_WAR,
             HK.KEY_SELECT_TEAMER_ME_SPRITE):
                continue
            detial = HK.HKM[key['key']]
            idx = detial.inkeyDef(gameKey, mods)
            if idx:
                array.append((self.tag,
                 key['name'],
                 key['key'],
                 idx,
                 i))

        return array

    def set(self, col, row, gameCode, mods):
        detial = HK.HKM[self.defaultKey[col]['key']]
        detial.setPart(row, gameCode, mods)

    def getSingleKeyDesc(self, col, row):
        detial = HK.HKM[self.defaultKey[col]['key']]
        p = BigWorld.player()
        desc1 = detial.getDesc(row)
        if desc1 and hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            if self.defaultKey[col]['key'] == keys.KEY_MINUS and desc1:
                desc1 = desc1 + gameStrings.TEXT_HOTKEYPROXY_279
            if self.defaultKey[col]['key'] == keys.KEY_EQUALS and desc1:
                desc1 = desc1 + gameStrings.TEXT_HOTKEYPROXY_281
        return desc1

    def saveHotKey(self):
        return self.getKeyDic(self.defaultKey)

    def getKeyDic(self, keyList):
        dict = {}
        for key in keyList:
            if not gameglobal.rds.configData.get('enableSkillMacro', False):
                if key['key'] == HK.KEY_SKILL_MACRO:
                    continue
            id = key['key']
            detial = HK.HKM[id]
            dict[id] = detial._value2 << 14 | detial._value

        return dict


def isCastSelfKeyConflict(mods):
    if mods == 4 and HK.CAST_SELF_KEY_INDEX == 0:
        return True
    if mods == 2 and HK.CAST_SELF_KEY_INDEX == 1:
        return True
    if mods == 1 and HK.CAST_SELF_KEY_INDEX == 2:
        return True
    return False


class ControlKey(BaseKey):

    def __init__(self, tag, manager, name = ''):
        super(ControlKey, self).__init__(tag, manager, name)
        self.defaultKey3D = [{'name': gameStrings.TEXT_HOTKEYPROXY_312,
          'key': HK.KEY_PICK_ITEM},
         {'name': gameStrings.TEXT_HOTKEYPROXY_313,
          'key': HK.KEY_FORWARD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_314,
          'key': HK.KEY_BACKWARD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_315,
          'key': HK.KEY_MOVELEFT},
         {'name': gameStrings.TEXT_HOTKEYPROXY_316,
          'key': HK.KEY_MOVERIGHT},
         {'name': gameStrings.TEXT_PUPPET_ACTION_616,
          'key': keys.KEY_SPACE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_318,
          'key': HK.KEY_FORWARD_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_319,
          'key': HK.KEY_LEFT_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_320,
          'key': HK.KEY_RIGHT_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_321,
          'key': HK.KEY_BACK_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_322,
          'key': HK.KEY_UP_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_323,
          'key': HK.KEY_DOWN_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_428,
          'key': HK.KEY_LEFTTURN},
         {'name': gameStrings.TEXT_HOTKEYPROXY_429,
          'key': HK.KEY_RIGHTTURN},
         {'name': gameStrings.TEXT_HOTKEYPROXY_326,
          'key': HK.KEY_DOWN},
         {'name': gameStrings.TEXT_HOTKEYPROXY_327,
          'key': HK.KEY_WINGFLYUP},
         {'name': gameStrings.TEXT_HOTKEYPROXY_328,
          'key': keys.KEY_TAB},
         {'name': gameStrings.TEXT_HOTKEYPROXY_329,
          'key': HK.KEY_LOCK_TARGETS_TARGET},
         {'name': gameStrings.TEXT_HOTKEYPROXY_330,
          'key': HK.KEY_SIMPLE_FIND_POS},
         {'name': gameStrings.TEXT_HOTKEYPROXY_331,
          'key': HK.KEY_GROUP_FOLLOW},
         {'name': gameStrings.TEXT_HOTKEYPROXY_332,
          'key': HK.KEY_SPRITE_TELEPORT_BACK},
         {'name': gameStrings.TEXT_HOTKEYPROXY_333,
          'key': HK.KEY_SPRITE_MANUAL_SKILL},
         {'name': gameStrings.TEXT_HOTKEYPROXY_334,
          'key': HK.KEY_NPCV2_SPEED},
         {'name': gameStrings.TEXT_HOTKEYPROXY_335,
          'key': HK.KEY_NPCV2_QUICK}]
        self.defaultKey2D = [{'name': gameStrings.TEXT_HOTKEYPROXY_312,
          'key': HK.KEY_PICK_ITEM},
         {'name': gameStrings.TEXT_HOTKEYPROXY_313,
          'key': HK.KEY_FORWARD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_314,
          'key': HK.KEY_BACKWARD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_315,
          'key': HK.KEY_MOVELEFT},
         {'name': gameStrings.TEXT_HOTKEYPROXY_316,
          'key': HK.KEY_MOVERIGHT},
         {'name': gameStrings.TEXT_PUPPET_ACTION_616,
          'key': keys.KEY_SPACE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_318,
          'key': HK.KEY_FORWARD_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_319,
          'key': HK.KEY_LEFT_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_320,
          'key': HK.KEY_RIGHT_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_321,
          'key': HK.KEY_BACK_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_322,
          'key': HK.KEY_UP_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_323,
          'key': HK.KEY_DOWN_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_326,
          'key': HK.KEY_DOWN},
         {'name': gameStrings.TEXT_HOTKEYPROXY_327,
          'key': HK.KEY_WINGFLYUP},
         {'name': gameStrings.TEXT_HOTKEYPROXY_328,
          'key': keys.KEY_TAB},
         {'name': gameStrings.TEXT_HOTKEYPROXY_329,
          'key': HK.KEY_LOCK_TARGETS_TARGET},
         {'name': gameStrings.TEXT_HOTKEYPROXY_330,
          'key': HK.KEY_SIMPLE_FIND_POS},
         {'name': gameStrings.TEXT_HOTKEYPROXY_331,
          'key': HK.KEY_GROUP_FOLLOW},
         {'name': gameStrings.TEXT_HOTKEYPROXY_332,
          'key': HK.KEY_SPRITE_TELEPORT_BACK},
         {'name': gameStrings.TEXT_HOTKEYPROXY_333,
          'key': HK.KEY_SPRITE_MANUAL_SKILL},
         {'name': gameStrings.TEXT_HOTKEYPROXY_334,
          'key': HK.KEY_NPCV2_SPEED},
         {'name': gameStrings.TEXT_HOTKEYPROXY_335,
          'key': HK.KEY_NPCV2_QUICK}]
        self.defaultKeyAction = [{'name': gameStrings.TEXT_HOTKEYPROXY_312,
          'key': HK.KEY_PICK_ITEM},
         {'name': gameStrings.TEXT_HOTKEYPROXY_328,
          'key': keys.KEY_TAB},
         {'name': gameStrings.TEXT_HOTKEYPROXY_329,
          'key': HK.KEY_LOCK_TARGETS_TARGET},
         {'name': gameStrings.TEXT_HOTKEYPROXY_313,
          'key': HK.KEY_FORWARD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_314,
          'key': HK.KEY_BACKWARD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_315,
          'key': HK.KEY_MOVELEFT},
         {'name': gameStrings.TEXT_HOTKEYPROXY_316,
          'key': HK.KEY_MOVERIGHT},
         {'name': gameStrings.TEXT_PUPPET_ACTION_616,
          'key': keys.KEY_SPACE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_318,
          'key': HK.KEY_FORWARD_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_319,
          'key': HK.KEY_LEFT_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_320,
          'key': HK.KEY_RIGHT_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_321,
          'key': HK.KEY_BACK_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_322,
          'key': HK.KEY_UP_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_323,
          'key': HK.KEY_DOWN_DODGE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_428,
          'key': HK.KEY_LEFTTURN},
         {'name': gameStrings.TEXT_HOTKEYPROXY_429,
          'key': HK.KEY_RIGHTTURN},
         {'name': gameStrings.TEXT_HOTKEYPROXY_326,
          'key': HK.KEY_DOWN},
         {'name': gameStrings.TEXT_HOTKEYPROXY_327,
          'key': HK.KEY_WINGFLYUP},
         {'name': gameStrings.TEXT_HOTKEYPROXY_330,
          'key': HK.KEY_SIMPLE_FIND_POS},
         {'name': gameStrings.TEXT_HOTKEYPROXY_331,
          'key': HK.KEY_GROUP_FOLLOW},
         {'name': gameStrings.TEXT_HOTKEYPROXY_332,
          'key': HK.KEY_SPRITE_TELEPORT_BACK},
         {'name': gameStrings.TEXT_HOTKEYPROXY_333,
          'key': HK.KEY_SPRITE_MANUAL_SKILL},
         {'name': gameStrings.TEXT_HOTKEYPROXY_334,
          'key': HK.KEY_NPCV2_SPEED},
         {'name': gameStrings.TEXT_HOTKEYPROXY_335,
          'key': HK.KEY_NPCV2_QUICK}]
        self.defaultKeyDota = [{'name': gameStrings.TEXT_HOTKEYPROXY_328,
          'key': keys.KEY_TAB},
         {'name': gameStrings.TEXT_HOTKEYPROXY_313,
          'key': HK.KEY_FORWARD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_314,
          'key': HK.KEY_BACKWARD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_315,
          'key': HK.KEY_MOVELEFT},
         {'name': gameStrings.TEXT_HOTKEYPROXY_316,
          'key': HK.KEY_MOVERIGHT},
         {'name': gameStrings.TEXT_PUPPET_ACTION_616,
          'key': keys.KEY_SPACE}]
        self.defaultKey = self.defaultKey3D

    def saveHotKey(self):
        p = BigWorld.player()
        operationMode = p.getOperationMode()
        keyList = []
        if operationMode == gameglobal.KEYBOARD_MODE:
            keyList.extend(self.defaultKey3D)
        elif operationMode == gameglobal.MOUSE_MODE:
            keyList.extend(self.defaultKey2D)
        else:
            keyList.extend(self.defaultKeyAction)
        return self.getKeyDic(keyList)

    def getDownKey(self):
        keyDownSet = set()
        for key in (HK.KEY_FORWARD_DODGE,
         HK.KEY_LEFT_DODGE,
         HK.KEY_RIGHT_DODGE,
         HK.KEY_BACK_DODGE,
         HK.KEY_UP_DODGE,
         HK.KEY_DOWN_DODGE):
            if HK.HKM.has_key(key):
                detial = HK.HKM[key]
                keyDownSet |= detial.getDirDownKey()

        return keyDownSet

    def switchDefaultKey(self, keyboardMode = gameglobal.KEYBOARD_MODE):
        p = BigWorld.player()
        if formula.inDotaBattleField(p.mapID):
            self.defaultKey = self.defaultKeyDota
            if keyboardMode == gameglobal.KEYBOARD_MODE:
                self.defaultKey = copy.deepcopy(self.defaultKeyDota)
                self.defaultKey.append({'name': gameStrings.TEXT_HOTKEYPROXY_428,
                 'key': HK.KEY_LEFTTURN})
                self.defaultKey.append({'name': gameStrings.TEXT_HOTKEYPROXY_429,
                 'key': HK.KEY_RIGHTTURN})
        elif keyboardMode == gameglobal.KEYBOARD_MODE:
            self.defaultKey = self.defaultKey3D
        elif keyboardMode == gameglobal.ACTION_MODE:
            self.defaultKey = self.defaultKeyAction
        else:
            self.defaultKey = self.defaultKey2D


class ShortKey(BaseKey):

    def __init__(self, tag, manager, name = ''):
        super(ShortKey, self).__init__(tag, manager, name)
        self.defaultKeyDota = [{'name': gameStrings.TEXT_HOTKEYPROXY_445,
          'key': HK.KEY_DOTA_SKILL0},
         {'name': gameStrings.TEXT_HOTKEYPROXY_446,
          'key': HK.KEY_DOTA_SKILL2},
         {'name': gameStrings.TEXT_HOTKEYPROXY_447,
          'key': HK.KEY_DOTA_SKILL3},
         {'name': gameStrings.TEXT_HOTKEYPROXY_448,
          'key': HK.KEY_DOTA_SKILL4},
         {'name': gameStrings.TEXT_HOTKEYPROXY_449,
          'key': HK.KEY_DOTA_SKILL5},
         {'name': gameStrings.TEXT_HOTKEYPROXY_450,
          'key': HK.KEY_DOTA_SKILL6},
         {'name': gameStrings.TEXT_HOTKEYPROXY_451,
          'key': HK.KEY_DOTA_SKILL7},
         {'name': gameStrings.TEXT_HOTKEYPROXY_452,
          'key': HK.KEY_DOTA_ITEM0},
         {'name': gameStrings.TEXT_HOTKEYPROXY_453,
          'key': HK.KEY_DOTA_ITEM1},
         {'name': gameStrings.TEXT_HOTKEYPROXY_454,
          'key': HK.KEY_DOTA_ITEM2},
         {'name': gameStrings.TEXT_HOTKEYPROXY_455,
          'key': HK.KEY_DOTA_ITEM3},
         {'name': gameStrings.TEXT_HOTKEYPROXY_456,
          'key': HK.KEY_DOTA_ITEM4},
         {'name': gameStrings.TEXT_HOTKEYPROXY_457,
          'key': HK.KEY_DOTA_ITEM5},
         {'name': gameStrings.BF_DOTA_RETURN_HOME,
          'key': HK.KEY_DOTA_RETURN_HOME},
         {'name': gameStrings.BF_DOTA_LEARN_SKILL,
          'key': HK.KEY_DOTA_LEARN_SKILL},
         {'name': gameStrings.BF_DOTA_BUY_ITEM_SHORTCUT0,
          'key': HK.KEY_DOTA_BUY_ITEM_SHORTCUT0},
         {'name': gameStrings.BF_DOTA_BUY_ITEM_SHORTCUT1,
          'key': HK.KEY_DOTA_BUY_ITEM_SHORTCUT1}]
        self.defaultKeyNomal = [{'name': gameStrings.TEXT_HOTKEYPROXY_464,
          'key': keys.KEY_1},
         {'name': gameStrings.TEXT_HOTKEYPROXY_465,
          'key': keys.KEY_2},
         {'name': gameStrings.TEXT_HOTKEYPROXY_466,
          'key': keys.KEY_3},
         {'name': gameStrings.TEXT_HOTKEYPROXY_467,
          'key': keys.KEY_4},
         {'name': gameStrings.TEXT_HOTKEYPROXY_468,
          'key': keys.KEY_5},
         {'name': gameStrings.TEXT_HOTKEYPROXY_469,
          'key': keys.KEY_6},
         {'name': gameStrings.TEXT_HOTKEYPROXY_470,
          'key': keys.KEY_7},
         {'name': gameStrings.TEXT_HOTKEYPROXY_471,
          'key': keys.KEY_8},
         {'name': gameStrings.TEXT_HOTKEYPROXY_472,
          'key': keys.KEY_9},
         {'name': gameStrings.TEXT_HOTKEYPROXY_473,
          'key': keys.KEY_0},
         {'name': gameStrings.TEXT_HOTKEYPROXY_474,
          'key': keys.KEY_MINUS},
         {'name': gameStrings.TEXT_HOTKEYPROXY_475,
          'key': keys.KEY_EQUALS},
         {'name': gameStrings.TEXT_HOTKEYPROXY_476,
          'key': keys.KEY_F1},
         {'name': gameStrings.TEXT_HOTKEYPROXY_477,
          'key': keys.KEY_F2},
         {'name': gameStrings.TEXT_HOTKEYPROXY_478,
          'key': keys.KEY_F3},
         {'name': gameStrings.TEXT_HOTKEYPROXY_479,
          'key': keys.KEY_F4},
         {'name': gameStrings.TEXT_HOTKEYPROXY_480,
          'key': keys.KEY_F5},
         {'name': gameStrings.TEXT_HOTKEYPROXY_481,
          'key': keys.KEY_F6},
         {'name': gameStrings.TEXT_HOTKEYPROXY_482,
          'key': HK.KEY_USE_ITEM1},
         {'name': gameStrings.TEXT_HOTKEYPROXY_483,
          'key': HK.KEY_USE_ITEM2},
         {'name': gameStrings.TEXT_HOTKEYPROXY_484,
          'key': HK.KEY_USE_ITEM3},
         {'name': gameStrings.TEXT_HOTKEYPROXY_485,
          'key': HK.KEY_USE_ITEM4},
         {'name': gameStrings.TEXT_HOTKEYPROXY_486,
          'key': HK.KEY_USE_ITEM5},
         {'name': gameStrings.TEXT_HOTKEYPROXY_487,
          'key': HK.KEY_USE_ITEM6},
         {'name': gameStrings.TEXT_HOTKEYPROXY_488,
          'key': HK.KEY_USE_ITEM7},
         {'name': gameStrings.TEXT_HOTKEYPROXY_489,
          'key': HK.KEY_USE_ITEM8},
         {'name': gameStrings.TEXT_HOTKEYPROXY_490,
          'key': HK.KEY_USE_ITEM9},
         {'name': gameStrings.TEXT_HOTKEYPROXY_491,
          'key': HK.KEY_USE_ITEM10},
         {'name': gameStrings.TEXT_HOTKEYPROXY_492,
          'key': HK.KEY_USE_ITEM11},
         {'name': gameStrings.TEXT_HOTKEYPROXY_493,
          'key': HK.KEY_USE_ITEM12},
         {'name': gameStrings.TEXT_HOTKEYPROXY_494,
          'key': HK.KEY_USE_ITEM13},
         {'name': gameStrings.TEXT_HOTKEYPROXY_495,
          'key': HK.KEY_USE_ITEM14},
         {'name': gameStrings.TEXT_HOTKEYPROXY_496,
          'key': HK.KEY_USE_ITEM15},
         {'name': gameStrings.TEXT_HOTKEYPROXY_497,
          'key': HK.KEY_USE_ITEM16},
         {'name': gameStrings.TEXT_HOTKEYPROXY_498,
          'key': HK.KEY_USE_ITEM17},
         {'name': gameStrings.TEXT_HOTKEYPROXY_499,
          'key': HK.KEY_USE_ITEM18},
         {'name': gameStrings.TEXT_HOTKEYPROXY_500,
          'key': HK.KEY_USE_ITEM19},
         {'name': gameStrings.TEXT_HOTKEYPROXY_501,
          'key': HK.KEY_USE_ITEM20},
         {'name': gameStrings.TEXT_HOTKEYPROXY_502,
          'key': HK.KEY_USE_ITEM21},
         {'name': gameStrings.TEXT_HOTKEYPROXY_503,
          'key': HK.KEY_USE_ITEM22},
         {'name': gameStrings.TEXT_HOTKEYPROXY_504,
          'key': HK.KEY_USE_ITEM23},
         {'name': gameStrings.TEXT_HOTKEYPROXY_505,
          'key': HK.KEY_USE_ITEM24},
         {'name': gameStrings.TEXT_HOTKEYPROXY_506,
          'key': HK.KEY_USE_ITEM25},
         {'name': gameStrings.TEXT_HOTKEYPROXY_507,
          'key': HK.KEY_USE_ITEM26},
         {'name': gameStrings.TEXT_HOTKEYPROXY_508,
          'key': HK.KEY_USE_ITEM27},
         {'name': gameStrings.TEXT_HOTKEYPROXY_509,
          'key': HK.KEY_USE_ITEM28},
         {'name': gameStrings.TEXT_HOTKEYPROXY_510,
          'key': HK.KEY_USE_ITEM29},
         {'name': gameStrings.TEXT_HOTKEYPROXY_511,
          'key': HK.KEY_USE_ITEM30},
         {'name': gameStrings.TEXT_HOTKEYPROXY_512,
          'key': HK.KEY_USE_ITEM31},
         {'name': gameStrings.TEXT_HOTKEYPROXY_513,
          'key': HK.KEY_USE_ITEM32},
         {'name': gameStrings.TEXT_HOTKEYPROXY_514,
          'key': HK.KEY_USE_ITEM33},
         {'name': gameStrings.TEXT_HOTKEYPROXY_515,
          'key': HK.KEY_USE_ITEM34},
         {'name': gameStrings.TEXT_HOTKEYPROXY_516,
          'key': HK.KEY_USE_ITEM35},
         {'name': gameStrings.TEXT_HOTKEYPROXY_517,
          'key': HK.KEY_USE_ITEM36},
         {'name': gameStrings.TEXT_HOTKEYPROXY_518,
          'key': HK.KEY_USE_ITEM37},
         {'name': gameStrings.TEXT_HOTKEYPROXY_519,
          'key': HK.KEY_USE_ITEM38},
         {'name': gameStrings.TEXT_HOTKEYPROXY_520,
          'key': HK.KEY_USE_ITEM39},
         {'name': gameStrings.TEXT_HOTKEYPROXY_521,
          'key': HK.KEY_USE_ITEM40},
         {'name': gameStrings.TEXT_HOTKEYPROXY_522,
          'key': HK.KEY_USE_ITEM41},
         {'name': gameStrings.TEXT_HOTKEYPROXY_523,
          'key': HK.KEY_USE_ITEM42},
         {'name': gameStrings.TEXT_HOTKEYPROXY_524,
          'key': HK.KEY_USE_ITEM43},
         {'name': gameStrings.TEXT_HOTKEYPROXY_525,
          'key': HK.KEY_USE_ITEM44},
         {'name': gameStrings.TEXT_HOTKEYPROXY_526,
          'key': HK.KEY_USE_ITEM45},
         {'name': gameStrings.TEXT_HOTKEYPROXY_527,
          'key': HK.KEY_USE_ITEM46},
         {'name': gameStrings.TEXT_HOTKEYPROXY_528,
          'key': HK.KEY_USE_ITEM47},
         {'name': gameStrings.TEXT_HOTKEYPROXY_529,
          'key': HK.KEY_USE_ITEM48},
         {'name': gameStrings.TEXT_HOTKEYPROXY_530,
          'key': HK.KEY_QTE_SKILL1},
         {'name': gameStrings.TEXT_HOTKEYPROXY_531,
          'key': HK.KEY_QTE_SKILL2},
         {'name': gameStrings.TEXT_HOTKEYPROXY_532,
          'key': HK.KEY_LEAVE_ZAIJU},
         {'name': gameStrings.TEXT_HOTKEYPROXY_533,
          'key': HK.KEY_ASSIGN_CONFIRM},
         {'name': gameStrings.TEXT_HOTKEYPROXY_534,
          'key': HK.KEY_ASSIGN_CANCEL},
         {'name': gameStrings.TEXT_HOTKEYPROXY_535,
          'key': HK.KEY_ASSIGN_GREED},
         {'name': gameStrings.TEXT_HOTKEYPROXY_536,
          'key': HK.KEY_BF_COUNT},
         {'name': gameStrings.TEXT_HOTKEYPROXY_537,
          'key': HK.KEY_BF_RETURN},
         {'name': gameStrings.TEXT_HOTKEYPROXY_538,
          'key': HK.KEY_ITEM_SOURCE}]

    @property
    def defaultKey(self):
        p = BigWorld.player()
        if formula.inDotaBattleField(getattr(p, 'mapID', 0)):
            return self.defaultKeyDota
        else:
            return self.defaultKeyNomal

    def saveHotKey(self):
        dict = {}
        tempConflict = False
        keyList = []
        keyList.extend(self.defaultKeyNomal)
        keyList.extend(self.defaultKeyDota)
        for key in keyList:
            if not gameglobal.rds.configData.get('enableNewItemSearch', False):
                if key['key'] == HK.KEY_ITEM_SOURCE:
                    continue
            id = key['key']
            detial = HK.HKM[id]
            dict[id] = detial._value2 << 14 | detial._value
            if not tempConflict and isCastSelfKeyConflict(detial.mods):
                tempConflict = True

        gameglobal.CAST_SELF_KEY_CONFLICT = tempConflict
        keyArr = self.getKeyDescArray()
        gameglobal.rds.ui.actionbar.setSlotKeyText(keyArr)
        gameglobal.rds.ui.zaijuV2.refreshSkillSlotsBind()
        gameglobal.rds.ui.bfDotaItemAndProp.refreshItemSlots()
        gameglobal.rds.ui.bfDotaShopPush.refreshShortcutKeyDesc()
        return dict

    def setCastSelfConflict(self):
        tempConflict = False
        for key in self.defaultKey:
            if not gameglobal.rds.configData.get('enableNewItemSearch', False):
                if key['key'] == HK.KEY_ITEM_SOURCE:
                    continue
            id = key['key']
            detial = HK.HKM[id]
            if not tempConflict and isCastSelfKeyConflict(detial.mods):
                tempConflict = True

        gameglobal.CAST_SELF_KEY_CONFLICT = tempConflict

    def getKeyDesc(self):
        array = []
        array.append((self.name,
         self.tag,
         self.tag,
         False))
        for key in self.defaultKey:
            if not gameglobal.rds.configData.get('enableNewItemSearch', False):
                if key['key'] == HK.KEY_ITEM_SOURCE:
                    continue
            detial = HK.HKM[key['key']]
            desc1 = detial.getDesc(1)
            p = BigWorld.player()
            operationMode = p.getOperationMode() if hasattr(p, 'getOperationMode') else None
            if operationMode == gameglobal.ACTION_MODE:
                if key['key'] == HK.KEY_DOTA_SKILL0:
                    desc1 = gameStrings.TEXT_HOTKEYPROXY_599
                if key['key'] == keys.KEY_MINUS and desc1:
                    desc1 = desc1 + gameStrings.TEXT_HOTKEYPROXY_279
                if key['key'] in (keys.KEY_EQUALS, HK.KEY_DOTA_SKILL2) and desc1:
                    desc1 = desc1 + gameStrings.TEXT_HOTKEYPROXY_281
                if key['key'] == HK.KEY_DOTA_SKILL3 and desc1:
                    desc1 = desc1 + ' (Shift)'
            elif operationMode == gameglobal.MOUSE_MODE:
                if key['key'] == HK.KEY_DOTA_SKILL0 and desc1:
                    desc1 = desc1 + gameStrings.TEXT_HOTKEYPROXY_608
            desc1 = desc1.replace('MOUSE0', gameStrings.TEXT_HOTKEYPROXY_599)
            desc1 = desc1.replace('MOUSE1', gameStrings.TEXT_HOTKEYPROXY_610)
            array.append((key['name'],
             desc1,
             detial.getDesc(2),
             key['key'] in HK.getForbideChangeKeyList()))

        return array

    def getKeyDescArray(self):
        keyArr = []
        for key in self.defaultKey:
            if not gameglobal.rds.configData.get('enableNewItemSearch', False):
                if key['key'] == HK.KEY_ITEM_SOURCE:
                    continue
            id = key['key']
            detial = HK.HKM.get(id, None)
            if not detial:
                continue
            if detial.key != 0:
                keyArr.append(detial.getBrief())
            elif detial.key2 != 0:
                keyArr.append(detial.getBrief(2))
            else:
                keyArr.append('')

        return keyArr

    def getKeyDescById(self, id, isShort = True):
        desc = ''
        for key in self.defaultKey:
            if not gameglobal.rds.configData.get('enableNewItemSearch', False):
                if key['key'] == HK.KEY_ITEM_SOURCE:
                    continue
            if id == key['key']:
                detial = HK.HKM[id]
                if detial.key != 0:
                    if isShort:
                        desc = detial.getBrief()
                    else:
                        desc = detial.getDesc()
                elif detial.key2 != 0:
                    if isShort:
                        desc = detial.getBrief(2)
                    else:
                        desc = detial.getDesc(2)
                return desc


class UiKey(BaseKey):

    def __init__(self, tag, manager, name = ''):
        super(UiKey, self).__init__(tag, manager, name)
        self.defaultKeyNormal = [{'name': gameStrings.TEXT_HOTKEYPROXY_659,
          'key': HK.KEY_SHOW_ROLEINFO},
         {'name': gameStrings.TEXT_HOTKEYPROXY_660,
          'key': HK.KEY_RELATION},
         {'name': gameStrings.TEXT_HOTKEYPROXY_661,
          'key': HK.KEY_SHOW_BAG},
         {'name': gameStrings.TEXT_HOTKEYPROXY_662,
          'key': HK.KEY_SHOW_SKILL},
         {'name': gameStrings.TEXT_HOTKEYPROXY_663,
          'key': HK.KEY_CARD_SYSTEM},
         {'name': gameStrings.TEXT_HOTKEYPROXY_664,
          'key': HK.KEY_SHOW_GENERAL_SKILL},
         {'name': gameStrings.TEXT_HOTKEYPROXY_665,
          'key': HK.KEY_SHOW_LIFE_SKILL},
         {'name': gameStrings.TEXT_HOTKEYPROXY_666,
          'key': HK.KEY_SHOW_TASKLOG},
         {'name': gameStrings.TEXT_HOTKEYPROXY_667,
          'key': HK.KEY_SHOW_TEAMINFO},
         {'name': gameStrings.TEXT_HOTKEYPROXY_668,
          'key': HK.KEY_SHOW_FRIEND},
         {'name': gameStrings.TEXT_HOTKEYPROXY_669,
          'key': HK.KEY_SHOW_MORE_RECOMM},
         {'name': gameStrings.TEXT_FRIENDPROXY_1225,
          'key': HK.KEY_SHOW_PVP},
         {'name': gameStrings.TEXT_HOTKEYPROXY_671,
          'key': keys.KEY_Y},
         {'name': gameStrings.TEXT_HOTKEYPROXY_672,
          'key': HK.KEY_SHOW_RANK},
         {'name': gameStrings.TEXT_HOTKEYPROXY_673,
          'key': HK.KEY_SHOW_MAIL},
         {'name': gameStrings.TEXT_HOTKEYPROXY_674,
          'key': HK.KEY_SHOW_CONSIGN},
         {'name': gameStrings.TEXT_HOTKEYPROXY_675,
          'key': HK.KEY_SHOW_DELEGATION},
         {'name': gameStrings.TEXT_HOTKEYPROXY_677,
          'key': HK.KEY_SHOW_MAP},
         {'name': gameStrings.TEXT_HOTKEYPROXY_678,
          'key': HK.KEY_SHOWUI},
         {'name': gameStrings.TEXT_HOTKEYPROXY_681,
          'key': HK.KEY_SHOW_CAMERA},
         {'name': gameStrings.TEXT_HOTKEYPROXY_682,
          'key': HK.KEY_SHOW_HELP},
         {'name': gameStrings.TEXT_HOTKEYPROXY_683,
          'key': HK.KEY_SHOW_PLAYRECOMM},
         {'name': gameStrings.TEXT_HOTKEYPROXY_685,
          'key': HK.KEY_NEXT_TRACK_TAB},
         {'name': gameStrings.TEXT_HOTKEYPROXY_686,
          'key': HK.KEY_RIDE_WING},
         {'name': gameStrings.TEXT_HOTKEYPROXY_689,
          'key': HK.KEY_ROLE_CARD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_690,
          'key': HK.KEY_FENG_WU_ZHI},
         {'name': gameStrings.TEXT_HOTKEYPROXY_692,
          'key': HK.KEY_PERSON_SPACE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_693,
          'key': HK.KEY_MOUNT_WING},
         {'name': gameStrings.TEXT_HOTKEYPROXY_694,
          'key': HK.KEY_STALL},
         {'name': gameStrings.TEXT_HOTKEYPROXY_695,
          'key': HK.KEY_PVP_ENHANCE},
         {'name': gameStrings.TEXT_HOTKEYPROXY_696,
          'key': HK.KEY_CHAT_ROOM},
         {'name': gameStrings.TEXT_HOTKEYPROXY_697,
          'key': HK.KEY_JIE_QI},
         {'name': gameStrings.TEXT_HOTKEYPROXY_698,
          'key': HK.KEY_MENTOR},
         {'name': gameStrings.TEXT_HOTKEYPROXY_699,
          'key': HK.KEY_PVP_JJC},
         {'name': gameStrings.TEXT_HOTKEYPROXY_700,
          'key': HK.KEY_GUI_BAO},
         {'name': gameStrings.TEXT_HOTKEYPROXY_701,
          'key': HK.KEY_USER_BACK},
         {'name': gameStrings.TEXT_HOTKEYPROXY_702,
          'key': HK.KEY_SUMMON_FRIEND},
         {'name': gameStrings.TEXT_HOTKEYPROXY_703,
          'key': HK.KEY_SKILL_MACRO},
         {'name': gameStrings.TEXT_HOTKEYPROXY_704,
          'key': HK.KEY_SPRITE_WAR}]
        self.defaultKeyDota = [{'name': gameStrings.BF_DOTA_OPEN_SHOP,
          'key': HK.KEY_DOTA_OPEN_SHOP}, {'name': gameStrings.BF_DOTA_SHOW_DETAIL,
          'key': HK.KEY_DOTA_SHOW_DETAIL}, {'name': gameStrings.BF_DOTA_SHOW_PROP,
          'key': HK.KEY_DOTA_SHOW_PROP}]

    def saveHotKey(self):
        keyList = []
        keyList.extend(self.defaultKeyDota)
        keyList.extend(self.defaultKeyNormal)
        return self.getKeyDic(keyList)

    @property
    def defaultKey(self):
        if formula.inDotaBattleField(getattr(BigWorld.player(), 'mapID', 0)):
            return self.defaultKeyDota
        else:
            return self.defaultKeyNormal


class TeamKey(BaseKey):

    def __init__(self, tag, manager, name = ''):
        super(TeamKey, self).__init__(tag, manager, name)
        self.defaultKey = [{'name': gameStrings.TEXT_HOTKEYPROXY_732,
          'key': HK.KEY_HIDE_PLAYER_MONSTER},
         {'name': gameStrings.TEXT_HOTKEYPROXY_733,
          'key': HK.KEY_SELECT_TEAMER1},
         {'name': gameStrings.TEXT_HOTKEYPROXY_734,
          'key': HK.KEY_SELECT_TEAMER2},
         {'name': gameStrings.TEXT_HOTKEYPROXY_735,
          'key': HK.KEY_SELECT_TEAMER3},
         {'name': gameStrings.TEXT_HOTKEYPROXY_736,
          'key': HK.KEY_SELECT_TEAMER4},
         {'name': gameStrings.TEXT_HOTKEYPROXY_737,
          'key': HK.KEY_SELECT_TEAMER},
         {'name': gameStrings.TEXT_HOTKEYPROXY_738,
          'key': HK.KEY_SELECT_TEAMER_ME},
         {'name': gameStrings.TEXT_HOTKEYPROXY_739,
          'key': HK.KEY_SUMMARY},
         {'name': gameStrings.TEXT_HOTKEYPROXY_740,
          'key': HK.KEY_SHOWFPS},
         {'name': gameStrings.TEXT_HOTKEYPROXY_741,
          'key': HK.KEY_CHATLOG_SOUND_RECORD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_742,
          'key': HK.KEY_CHAT_TO_FRIEND_SOUND_RECORD},
         {'name': gameStrings.TEXT_HOTKEYPROXY_743,
          'key': HK.KEY_SELECT_TEAMER_ME_SPRITE}]


class ActionKey(BaseKey):

    def __init__(self, tag, manager, name = ''):
        super(ActionKey, self).__init__(tag, manager, name)
        self.defaultKeyNormal = [{'name': gameStrings.TEXT_HOTKEYPROXY_752,
          'key': HK.KEY_DRAG_UI},
         {'name': gameStrings.TEXT_HOTKEYPROXY_753,
          'key': keys.KEY_NUMLOCK},
         {'name': gameStrings.TEXT_HOTKEYPROXY_754,
          'key': HK.KEY_WING_SPRINT},
         {'name': gameStrings.TEXT_HOTKEYPROXY_755,
          'key': HK.KEY_WEAPON_IN_HAND},
         {'name': gameStrings.TEXT_HOTKEYPROXY_756,
          'key': HK.KEY_SWITCH_RUN_WALK},
         {'name': gameStrings.TEXT_HOTKEYPROXY_757,
          'key': HK.KEY_CAMERA_NEAR},
         {'name': gameStrings.TEXT_HOTKEYPROXY_758,
          'key': HK.KEY_CAMERA_FAR},
         {'name': gameStrings.TEXT_HOTKEYPROXY_759,
          'key': HK.KEY_TURN_CAMERA},
         {'name': gameStrings.TEXT_HOTKEYPROXY_760,
          'key': HK.KEY_VOICE}]
        self.defaultKeyDota = [{'name': gameStrings.TEXT_HOTKEYPROXY_752,
          'key': HK.KEY_DRAG_UI},
         {'name': gameStrings.TEXT_HOTKEYPROXY_753,
          'key': keys.KEY_NUMLOCK},
         {'name': gameStrings.TEXT_HOTKEYPROXY_757,
          'key': HK.KEY_CAMERA_NEAR},
         {'name': gameStrings.TEXT_HOTKEYPROXY_758,
          'key': HK.KEY_CAMERA_FAR},
         {'name': gameStrings.TEXT_HOTKEYPROXY_759,
          'key': HK.KEY_TURN_CAMERA},
         {'name': gameStrings.TEXT_HOTKEYPROXY_760,
          'key': HK.KEY_VOICE}]

    @property
    def defaultKey(self):
        if formula.inDotaBattleField(BigWorld.player().mapID):
            return self.defaultKeyDota
        else:
            return self.defaultKeyNormal

    def saveHotKey(self):
        return self.getKeyDic(self.defaultKeyNormal)


class HotkeyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(HotkeyProxy, self).__init__(uiAdapter)

    def show(self):
        gameglobal.rds.ui.gameSetting.show(uiConst.GAME_SETTING_BG_V2_TAB_CONTROL)
