#Embedded file name: I:/bag/tmp/tw2/res/entities\common/effect.o
from userSoleType import UserSoleType
from userType import MemberProxy

class Effect(UserSoleType):
    mf = MemberProxy('mf')
    aura = MemberProxy('aura')

    def __init__(self, dict):
        super(Effect, self).__init__()
        if not dict.has_key('mf'):
            dict['mf'] = ()
        if not dict.has_key('aura'):
            dict['aura'] = ()
        self.fixedDict = dict

    def deepcopy(self):
        return {'mf': self.mf,
         'aura': self.aura}

    def __cmp__(self, v):
        return cmp(v.fixedDict, self.fixedDict)
