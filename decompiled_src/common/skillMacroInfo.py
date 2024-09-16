#Embedded file name: I:/bag/tmp/tw2/res/entities\common/skillMacroInfo.o
from userInfo import UserInfo
from skillMacro import *

class skillMacroInfo(UserInfo):

    def createObjFromDict(self, dict):
        skillMacros = SkillMacro()
        for macro in dict['skillMacros']:
            tmpVal = SkillMacroVal(macro['macroId'], macro['page'], macro['slot'], macro['iconType'], macro['iconPath'], macro['name'], macro['macroList'])
            skillMacros[tmpVal.macroId] = tmpVal

        return skillMacros

    def getDictFromObj(self, obj):
        skillMacros = []
        for macro in obj.itervalues():
            tmp = {'macroId': macro.macroId,
             'page': macro.page,
             'slot': macro.slot,
             'iconType': macro.iconType,
             'iconPath': macro.iconPath,
             'name': macro.name,
             'macroList': macro.macroList}
            skillMacros.append(tmp)

        return {'skillMacros': skillMacros}

    def isSameType(self, obj):
        return type(obj) is SkillMacro


instance = skillMacroInfo()
