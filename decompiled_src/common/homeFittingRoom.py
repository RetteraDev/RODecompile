#Embedded file name: I:/bag/tmp/tw2/res/entities\common/homeFittingRoom.o
import copy
from userDictType import UserDictType
from userSoleType import UserSoleType
from appearance import Appearance

class HomeFittingRoomVal(UserSoleType):

    def __init__(self, equips = {}):
        super(HomeFittingRoomVal, self).__init__()
        self.equips = copy.deepcopy(equips)
        self.aspect = Appearance({})
        self.physique = {}
        self.avatarConfig = ''
        self.hairColor = ''
        self.actionId = 0

    def hasEquip(self):
        return len(self.equips) > 0

    def _lateReload(self):
        super(HomeFittingRoomVal, self)._lateReload()
        self.aspect.reloadScript()


class HomeFittingRoom(UserDictType):

    def __init__(self):
        super(HomeFittingRoom, self).__init__()

    def _lateReload(self):
        super(HomeFittingRoom, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
