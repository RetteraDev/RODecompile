#Embedded file name: I:/bag/tmp/tw2/res/entities\common/personalZoneSkin.o
import utils
from userSoleType import UserSoleType
from userDictType import UserDictType
from data import personal_zone_skin_data as PZSD

class PersonalZoneSkinVal(UserSoleType):

    def __init__(self, skinId):
        super(PersonalZoneSkinVal, self).__init__()
        self.skinId = skinId
        valid = PZSD.data.get(skinId, {}).get('validTime', None)
        if valid:
            self.expireTime = utils.getNow() + valid
        else:
            self.expireTime = 0


class PersonalZoneSkinDict(UserDictType):

    def __init__(self):
        super(PersonalZoneSkinDict, self).__init__()
        self.curUseSkinId = 0

    def _lateReload(self):
        for v in self.itervalues():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()

    def hasSkin(self, skinId):
        return self.has_key(skinId)

    def addSkin(self, skinId):
        addedSkin = None
        changedSkin = None
        if not self.has_key(skinId):
            self[skinId] = PersonalZoneSkinVal(skinId)
            addedSkin = self[skinId]
        else:
            valid = PZSD.data.get(skinId, {}).get('validTime', None)
            if valid:
                self[skinId].expireTime += valid
            else:
                self[skinId].expireTime = 0
            changedSkin = self[skinId]
        return (addedSkin, changedSkin)

    def delSkin(self, skinId):
        self.pop(skinId, None)
