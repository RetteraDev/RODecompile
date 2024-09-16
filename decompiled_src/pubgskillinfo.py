#Embedded file name: /WORKSPACE/data/entities/common/pubgskillinfo.o
from userInfo import UserInfo
from pubgSkill import PubgSkillVal, PubgSkill

class PubgSkillInfo(UserInfo):

    def createObjFromDict(self, dictData):
        obj = PubgSkill(dictData['spaceNo'])
        for child in dictData['skills']:
            obj[child['skillId']] = PubgSkillVal(child['skillLv'])

        return obj

    def getDictFromObj(self, obj):
        skills = []
        for skillId, skillVal in obj.itervalues():
            skills.append({'skillId': skillId,
             'skillLv': skillVal.skillLv})

        return {'skills': skills,
         'spaceNo': obj.spaceNo}

    def isSameType(self, obj):
        return type(obj) is PubgSkill


skillInstance = PubgSkillInfo()
