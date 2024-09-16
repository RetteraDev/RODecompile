#Embedded file name: I:/bag/tmp/tw2/res/entities\common/title.o
import BigWorld
import utils
import const
from userSoleType import UserSoleType
from userDictType import UserDictType
from userType import MemberProxy

class TitleVal(UserSoleType):

    def __init__(self, title = 0, tGain = 0, tAttr = 0, tOutdate = 0):
        self.title = title
        self.tGain = tGain
        self.tAttr = tAttr
        self.tOutdate = tOutdate


class Title(UserDictType):

    def __init__(self):
        super(Title, self).__init__()

    def _lateReload(self):
        super(Title, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def addTitle(self, title, tattr, tout = 0):
        now = utils.getNow()
        if self.has_key(title):
            self[title].tGain = now
            self[title].tAttr = tattr
            self[title].tOutdate = tout
        else:
            self[title] = TitleVal(title=title, tGain=now, tAttr=tattr, tOutdate=tout)

    def delTitle(self, title):
        self.pop(title, None)

    def hasTitle(self, title):
        return self.has_key(title)

    def getTitle(self):
        return self.keys()

    def isAttrOut(self, title):
        if not self.has_key(title):
            return True
        if self[title].tAttr == const.TITLE_VALID_TIME_INFINITE:
            return False
        return self[title].tAttr < self._getNow()

    def hasValidAttr(self):
        now = self._getNow()
        for v in self.itervalues():
            if v.tAttr == const.TITLE_VALID_TIME_INFINITE or v.tAttr > now:
                return True

        return False

    def isTitleOut(self, title):
        if not self.has_key(title):
            return True
        if self[title].tOutdate == const.TITLE_VALID_TIME_INFINITE:
            return False
        return self[title].tOutdate < self._getNow()

    def hasValidTitle(self):
        now = self._getNow()
        for v in self.itervalues():
            if v.tOutdate == const.TITLE_VALID_TIME_INFINITE or v.tOutdate > now:
                return True

        return False

    def _getNow(self):
        if BigWorld.component in 'client':
            return BigWorld.player().getServerTime()
        else:
            return utils.getNow()
