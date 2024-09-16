#Embedded file name: I:/bag/tmp/tw2/res/entities\common/socAttribute.o
from userSoleType import UserSoleType
from userType import MemberProxy

class SocAttribute(UserSoleType):
    bstr = MemberProxy('bstr')
    bdex = MemberProxy('bdex')
    bknow = MemberProxy('bknow')
    bsense = MemberProxy('bsense')
    bstudy = MemberProxy('bstudy')
    bcharm = MemberProxy('bcharm')
    blucky = MemberProxy('blucky')
    str = MemberProxy('str')
    dex = MemberProxy('dex')
    know = MemberProxy('know')
    sense = MemberProxy('sense')
    study = MemberProxy('study')
    charm = MemberProxy('charm')
    lucky = MemberProxy('lucky')

    def __init__(self, dict):
        super(SocAttribute, self).__init__()
        if not dict.has_key('bstr'):
            dict['bstr'] = 0
        if not dict.has_key('bdex'):
            dict['bdex'] = 0
        if not dict.has_key('bknow'):
            dict['bknow'] = 0
        if not dict.has_key('bsense'):
            dict['bsense'] = 0
        if not dict.has_key('bstudy'):
            dict['bstudy'] = 0
        if not dict.has_key('bcharm'):
            dict['bcharm'] = 0
        if not dict.has_key('blucky'):
            dict['blucky'] = 0
        if not dict.has_key('str'):
            dict['str'] = 0
        if not dict.has_key('dex'):
            dict['dex'] = 0
        if not dict.has_key('know'):
            dict['know'] = 0
        if not dict.has_key('sense'):
            dict['sense'] = 0
        if not dict.has_key('study'):
            dict['study'] = 0
        if not dict.has_key('charm'):
            dict['charm'] = 0
        if not dict.has_key('lucky'):
            dict['lucky'] = 0
        self.fixedDict = dict
