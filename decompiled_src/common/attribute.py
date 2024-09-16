#Embedded file name: I:/bag/tmp/tw2/res/entities\common/attribute.o
from userSoleType import UserSoleType
from userType import MemberProxy

class Attribute(UserSoleType):
    point = MemberProxy('point')
    gpoint = MemberProxy('gpoint')
    bpow = MemberProxy('bpow')
    bint = MemberProxy('bint')
    bphy = MemberProxy('bphy')
    bspr = MemberProxy('bspr')
    bagi = MemberProxy('bagi')
    pow = MemberProxy('pow')
    int = MemberProxy('int')
    phy = MemberProxy('phy')
    spr = MemberProxy('spr')
    agi = MemberProxy('agi')

    def __init__(self, dict):
        super(Attribute, self).__init__()
        if not dict.has_key('point'):
            dict['point'] = 0
        if not dict.has_key('gpoint'):
            dict['gpoint'] = 0
        if not dict.has_key('bpow'):
            dict['bpow'] = 0
        if not dict.has_key('bint'):
            dict['bint'] = 0
        if not dict.has_key('bphy'):
            dict['bphy'] = 0
        if not dict.has_key('bspr'):
            dict['bspr'] = 0
        if not dict.has_key('bagi'):
            dict['bagi'] = 0
        if not dict.has_key('pow'):
            dict['pow'] = 0
        if not dict.has_key('int'):
            dict['int'] = 0
        if not dict.has_key('phy'):
            dict['phy'] = 0
        if not dict.has_key('spr'):
            dict['spr'] = 0
        if not dict.has_key('agi'):
            dict['agi'] = 0
        self.fixedDict = dict
