#Embedded file name: /WORKSPACE/data/entities/common/zmjstarboss.o
import copy
from userSoleType import UserSoleType
from userDictType import UserDictType

class ZMJRoleVal(object):

    def __init__(self, gbId = 0, roleName = '', lv = 0, photo = '', borderId = 0):
        self.gbId = gbId
        self.roleName = copy.deepcopy(roleName)
        self.lv = lv
        self.photo = copy.deepcopy(photo)
        self.borderId = borderId


class ZMJStarBossVal(UserSoleType):

    def __init__(self, fbNo = 0, star = 0, tExpire = 0, tValid = 0, founder = ZMJRoleVal(), candidates = [], ownerGbId = 0, ownerName = '', killer = 0):
        self.fbNo = fbNo
        self.star = star
        self.founder = founder
        self.tExpire = tExpire
        self.tValid = tValid
        self.candidates = copy.deepcopy(candidates)
        self.ownerGbId = ownerGbId
        self.ownerName = copy.deepcopy(ownerName)
        self.killer = killer

    @property
    def founderGbId(self):
        return self.founder.gbId

    @property
    def allMembers(self):
        return self.candidates + [self.founder.gbId]


class ZMJStarBoss(UserDictType):

    def __init__(self):
        super(ZMJStarBoss, self).__init__()

    def _lateReload(self):
        super(ZMJStarBoss, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
