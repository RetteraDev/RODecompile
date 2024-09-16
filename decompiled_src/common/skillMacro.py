#Embedded file name: I:/bag/tmp/tw2/res/entities\common/skillMacro.o
import BigWorld
import gametypes
import re
from userSoleType import UserSoleType
from userDictType import UserDictType
from gameclass import Singleton
from cdata import skill_macro_type_data as SMTD
if BigWorld.component == 'client':
    import gameglobal
    from guis import richTextUtils
    from data import skill_macro_arg_data as SMAD
    from data import skill_macro_command_data as SMCD

def checkMacroFormat(macroList, originMacroList = None, checkedMacroList = None):
    """
    \xbc\xec\xb2\xe9\xba\xea\xd3\xef\xbe\xe4\xb8\xf1\xca\xbd\xca\xc7\xb7\xf1\xd5\xfd\xc8\xb7
    /[\xcc\xf5\xbc\xfe]\xc0\xe0\xd0\xcd \xb2\xce\xca\xfd \xb2\xce\xca\xfd
    :param macroList:
    :return:
    """
    if type(macroList) not in (list, tuple):
        if type(macroList) == str:
            macro = macroList
            macroList = []
            macroList.append(macro)
        else:
            macroList = list(macroList)
    if len(macroList) > gametypes.SKILL_MACRO_LEN_LIMIT:
        return (False, gametypes.SKILL_MACRO_LEN_ERROR)
    if getChatTypeNum(macroList) > 1:
        return (False, gametypes.SKILL_MACRO_CHAT_REPEAT)
    if originMacroList and getChatTypeNum(originMacroList) > 1:
        if getMacroType(macroList[0]) == gametypes.MACRO_TYPE_CHAT:
            return (False, gametypes.SKILL_MACRO_CHAT_REPEAT)
    for macro in macroList:
        if BigWorld.component == 'client':
            if richTextUtils.isSysRichTxt(macro):
                return (False, gametypes.SKILL_MACRO_FORMAT_ERROR)
        if len(macro) > gametypes.SKILL_MACRO_SINGLE_LENGTH_LIMIT:
            return (False, gametypes.SKILL_MACRO_SINGLE_LENGTH_ERROR)
        if checkedMacroList:
            if macro in checkedMacroList:
                return (False, gametypes.SKILL_MACRO_REPEAT_ERROR)
        if not originMacroList:
            originMacroList = macroList
        if originMacroList:
            repeatNum = 0
            for originMacro in originMacroList:
                if originMacro == macro:
                    repeatNum += 1

            if repeatNum > 1:
                return (False, gametypes.SKILL_MACRO_REPEAT_ERROR)
        macroSplit = macro.split(' ')
        if not macro:
            continue
        if len(macroSplit) < 2:
            return (False, gametypes.SKILL_MACRO_FORMAT_ERROR)
        if -1 == macroSplit[0].find('/'):
            return (False, gametypes.SKILL_MACRO_FORMAT_ERROR)
        macroType = macroSplit[0].split('/')[-1]
        if macroType not in SMTD.data.keys():
            return (False, gametypes.SKILL_MACRO_TYPE_ERROR)
        typeNum = SMTD.data[macroType].get('type', 0)
        if typeNum == gametypes.MACRO_TYPE_CHAT:
            tmpSplit = ['', '', '']
            if len(macroSplit) < 2:
                return (False, gametypes.SKILL_MACRO_ARG_NUM_ERROR)
            for i in xrange(0, len(macroSplit)):
                if i < 2:
                    tmpSplit[i] = macroSplit[i]
                elif i == 2:
                    tmpSplit[i] = macroSplit[i]
                else:
                    tmpSplit[2] = tmpSplit[2] + ' ' + macroSplit[i]

            macroSplit = tmpSplit
        for i in xrange(0, len(macroSplit)):
            if -1 != macroSplit[i].find('['):
                condition = macroSplit[i].replace('[', '').replace(']', '')
                if BigWorld.component == 'client':
                    conditionDeal = SkillMacroCondition.getInstance()
                    if conditionDeal.isCodeInCondition(condition):
                        return (False, gametypes.SKILL_MACRO_CONDITION_FORMAT_ERROR)
                    isRight, condition = conditionDeal.preDealWithCondition(condition)
                    if not isRight:
                        return (isRight, gametypes.SKILL_MACRO_CONDITION_NUM_ERROR)
                    isRight, condition = conditionDeal.dealWithCondition(condition, typeNum)
                    if not isRight:
                        return (isRight, gametypes.SKILL_MACRO_CONDITION_NOT_AVALIABLE)
                    try:
                        conditionDeal.execCondition(condition)
                    except Exception as e:
                        return (False, gametypes.SKILL_MACRO_CONDITION_FORMAT_ERROR)

                del macroSplit[i]
                break

        if typeNum == gametypes.MACRO_TYPE_CHAT:
            i = 0
            while i < len(macroSplit):
                if not macroSplit[i]:
                    del macroSplit[i]
                else:
                    i += 1

        if len(macroSplit) != gametypes.MACRO_MAX_ARG_NUM[typeNum]:
            return (False, gametypes.SKILL_MACRO_ARG_NUM_ERROR)
        argError = True
        for k, v in SMCD.data.iteritems():
            if v.get('type', 0) == typeNum or v.has_key('subType') and v['subType'] == typeNum:
                command = v.get('command', '')
                if macroSplit[1] == command.split(' ')[1]:
                    argError = False
                    break

        if argError:
            return (False, gametypes.SKILL_MACRO_ARG_ERROR)

    return (True, gametypes.SKILL_MACRO_CORRECT_TYPE)


def getMacroType(macro):
    macroSplit = macro.split(' ')
    if len(macroSplit) and macroSplit[0].find('/') >= 0:
        macroType = macroSplit[0].replace('/', '')
        return SMTD.data.get(macroType, {}).get('type', -1)
    return -1


def getChatTypeNum(macroList):
    typeNum = 0
    for macro in macroList:
        if getMacroType(macro) == gametypes.MACRO_TYPE_CHAT:
            typeNum += 1

    return typeNum


class SkillMacroCondition(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.condition = {}
        self.condition[gametypes.MACRO_CONDITION_TYPE_MAIN] = []
        self.condition[gametypes.MACRO_CONDITION_TYPE_WAY] = []
        self.condition[gametypes.MACRO_CONDITION_TYPE_CONNECT] = []
        self.buffer = {}
        for key, value in SMAD.data.iteritems():
            if value.get('code', ''):
                conditionItem = {}
                conditionItem['name'] = key
                conditionItem['code'] = value.get('code', '')
                conditionItem['type'] = value.get('arg', 0)
                conditionItem['macroType'] = value.get('macroType', ())
                self.condition[value.get('arg', 0)].append(conditionItem)

    def preDealWithCondition(self, condition):
        result = re.search('\\d+[^%,^\\d]+|\\d+$', condition)
        if result:
            return (False, condition)
        condition = re.sub('\\d+%+', self.replaceWithFloat, condition)
        return (True, condition)

    def replaceWithFloat(self, matched):
        value = matched.group(0)
        return str(float(value.replace('%', '')) / 100)

    def dealWithCondition(self, condition, targetType = -1):
        for key, value in self.condition.iteritems():
            for conditionItem in value:
                if condition.find(conditionItem.get('name', '')) != -1:
                    if conditionItem['macroType'] and targetType >= 0:
                        if targetType not in conditionItem['macroType']:
                            return (False, condition)
                condition = condition.replace(conditionItem.get('name', ''), conditionItem.get('code', ''))

        return (True, condition)

    def isCodeInCondition(self, condition):
        condition = re.sub('\\d+', '', condition)
        condition = re.sub('\\%+', '', condition)
        for key, value in self.condition.iteritems():
            for conditionItem in value:
                condition = condition.replace(conditionItem.get('name', ''), '')

        if condition:
            return True

    def execCondition(self, condition):
        if not self.buffer.get(condition, None):
            compileResult = compile(condition, '', 'eval')
            self.buffer[condition] = compileResult
        else:
            compileResult = self.buffer.get(condition, None)
        return eval(compileResult)

    def buildBuffer(self, macroList):
        for command in macroList:
            rawArgs = command.split(' ')
            condition = ''
            for i in xrange(0, len(rawArgs)):
                if -1 != rawArgs[i].find('['):
                    condition = rawArgs[i].replace('[', '').replace(']', '')
                    break

            if not condition:
                return
            isCodeIn = self.isCodeInCondition(condition)
            if isCodeIn:
                return
            isRight, condition = self.preDealWithCondition(condition)
            if not isRight:
                return
            isRight, condition = self.dealWithCondition(condition)
            if not isRight:
                return
            compileResult = compile(condition, '', 'eval')
            self.buffer[condition] = compileResult


class SkillMacroVal(UserSoleType):

    def __init__(self, macroId, page, slot, iconType, iconPath, name, macroList):
        """
        \xbc\xbc\xc4\xdc\xba\xea\xbd\xe1\xb9\xb9\xcc\xe5
        :param macroId: \xba\xeaid
        :param page: \xba\xea\xb5\xc4page
        :param slot: \xba\xea\xb5\xc4slot
        :param iconType: \xba\xea\xb5\xc4\xcd\xbc\xb1\xea\xc0\xe0\xd0\xcd
        :param iconPath: \xba\xea\xb5\xc4\xcd\xbc\xb1\xea\xc2\xb7\xbe\xb6
        :param name: \xba\xea\xb5\xc4\xc3\xfb\xb3\xc6
        :param macroList: \xba\xea\xb5\xc4\xd3\xef\xbe\xe4\xc1\xd0\xb1\xed(ARRAY OF STRING)
        """
        self.macroId = macroId
        self.page = page
        self.slot = slot
        self.iconType = iconType
        self.iconPath = iconPath
        self.name = name
        self.macroList = macroList


class SkillMacro(UserDictType):

    def _lateReload(self):
        super(SkillMacro, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def updateSkillMacro(self, macroId, page, slot, iconType, iconPath, name, macroList):
        """
        \xb8\xfc\xd0\xc2\xd2\xbb\xb8\xf6\xbc\xbc\xc4\xdc\xba\xea
        :param macroId: \xba\xeaid
        :param page: \xd2\xaa\xb8\xfc\xd0\xc2\xba\xea\xcb\xf9\xd4\xda\xb5\xc4page
        :param slot: \xd2\xaa\xb8\xfc\xd0\xc2\xba\xea\xcb\xf9\xd4\xda\xb5\xc4slot
        :param iconPath: \xd2\xaa\xb8\xfc\xd0\xc2\xba\xea\xb5\xc4\xcd\xbc\xb1\xea\xc2\xb7\xbe\xb6
        :param name: \xd2\xaa\xb8\xfc\xd0\xc2\xba\xea\xb5\xc4\xc3\xfb\xb3\xc6
        :param macroList: \xd2\xaa\xb8\xfc\xd0\xc2\xba\xea\xb5\xc4\xd3\xef\xbe\xe4\xc1\xd0\xb1\xed(ARRAY OF STRING)
        :return:
        """
        if self.has_key(macroId):
            self[macroId].page = page
            self[macroId].slot = slot
            self[macroId].iconType = iconType
            self[macroId].iconPath = iconPath
            self[macroId].name = name
            self[macroId].macroList = macroList
            return True
        self[macroId] = SkillMacroVal(macroId, page, slot, iconType, iconPath, name, macroList)
        return True

    def delSkillMacro(self, macroId):
        if not self.has_key(macroId):
            return
        self.pop(macroId, None)

    def moveSkillMacro(self, sourceMacroId, destMacroId, sourcePage, sourceSlot, destPage, destSlot):
        """
        \xd2\xc6\xb6\xaf\xd2\xbb\xb8\xf6\xbc\xbc\xc4\xdc\xba\xea
        :param sourceMacroId: \xd2\xaa\xd2\xc6\xb6\xaf\xb5\xc4\xbc\xbc\xc4\xdc\xba\xea\xb5\xc4id
        :param destMacroId: \xd2\xc6\xb6\xaf\xb5\xbd\xc4\xbf\xb1\xea\xce\xbb\xd6\xc3\xb5\xc4\xbc\xbc\xc4\xdc\xba\xeaid
        :param sourcePage: \xd2\xaa\xd2\xc6\xb6\xaf\xb5\xc4\xbc\xbc\xc4\xdc\xba\xea\xb5\xc4page
        :param sourceSlot: \xd2\xaa\xd2\xc6\xb6\xaf\xb5\xc4\xbc\xbc\xc4\xdc\xba\xea\xb5\xc4slot
        :param destPage: \xd2\xaa\xd2\xc6\xb6\xaf\xb5\xbd\xb5\xc4page
        :param destSlot: \xd2\xaa\xd2\xc6\xb6\xaf\xb5\xbd\xb5\xc4slot
        :return:
        """
        if not self.has_key(sourceMacroId):
            return
        if not destMacroId:
            self[sourceMacroId].page = destPage
            self[sourceMacroId].slot = destSlot
            return
        self[sourceMacroId].page = destPage
        self[sourceMacroId].slot = destSlot
        self[destMacroId].page = sourcePage
        self[destMacroId].slot = sourceSlot

    def resetSkillMacro(self):
        self.clear()
