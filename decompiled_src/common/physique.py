#Embedded file name: I:/bag/tmp/tw2/res/entities\common/physique.o
import const
from userSoleType import UserSoleType
from userType import MemberProxy

class Physique(UserSoleType):
    school = MemberProxy('school')
    sex = MemberProxy('sex')
    face = MemberProxy('face')
    hair = MemberProxy('hair')
    bodyType = MemberProxy('bodyType')

    def __init__(self, dict):
        super(Physique, self).__init__()
        if not dict.has_key('school'):
            dict['school'] = const.SCHOOL_DEFAULT
        if not dict.has_key('sex'):
            dict['sex'] = const.SEX_UNKNOWN
        if not dict.has_key('face'):
            dict['face'] = 0
        if not dict.has_key('hair'):
            dict['hair'] = 0
        if not dict.has_key('bodyType'):
            dict['bodyType'] = 0
        self.fixedDict = dict

    def reloadScript(self):
        super(Physique, self).reloadScript()

    def deepcopy(self):
        return {'school': self.school,
         'sex': self.sex,
         'face': self.face,
         'hair': self.hair,
         'bodyType': self.bodyType}

    def isOpposite(self, sex):
        if self.sex == const.SEX_MALE and sex == const.SEX_FEMALE:
            return True
        elif self.sex == const.SEX_FEMALE and sex == const.SEX_MALE:
            return True
        else:
            return False

    def isMale(self):
        return self.sex == const.SEX_MALE

    def isFemale(self):
        return self.sex == const.SEX_FEMALE

    def coSchool(self, school):
        return self.school == school

    def __cmp__(self, v):
        return cmp(v.fixedDict, self.fixedDict)
