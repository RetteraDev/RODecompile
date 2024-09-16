#Embedded file name: /WORKSPACE/data/entities/common/effecttitle.o
import BigWorld
import utils
import const
import gametypes
from userSoleType import UserSoleType
from userDictType import UserDictType
from userType import MemberProxy

class EffectTitleVal(UserSoleType):
    title = MemberProxy('title')
    tGain = MemberProxy('tGain')
    tExpired = MemberProxy('tExpired')
    effectLv = MemberProxy('effectLv')
    tAttr = MemberProxy('tAttr')

    def __init__(self, fixdict):
        if not fixdict.has_key('title'):
            fixdict['title'] = 0
        if not fixdict.has_key('tGain'):
            fixdict['tGain'] = 0
        if not fixdict.has_key('tExpired'):
            fixdict['tExpired'] = 0
        if not fixdict.has_key('effectLv'):
            fixdict['effectLv'] = gametypes.EFFECT_TITLE_LV_HIGH
        if not fixdict.has_key('tAttr'):
            fixdict['tAttr'] = const.EFFECT_TITLE_VALID_TIME_INFINITE
        self.fixedDict = fixdict


class EffectTitle(UserDictType):

    def __init__(self):
        super(EffectTitle, self).__init__()

    def _lateReload(self):
        super(EffectTitle, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def addTitle(self, title, tExpired = 0, tAttr = 0):
        now = utils.getNow()
        if self.has_key(title):
            tExpired = 0 if tExpired == 0 or self[title].tExpired == 0 else max(self[title].tExpired, tExpired)
            tAttr = 0 if tAttr == 0 or self[title].tAttr == 0 else max(self[title].tAttr, tAttr)
            self[title].tGain = now
            self[title].tExpired = tExpired
            self[title].tAttr = tAttr
        else:
            self[title] = EffectTitleVal({'title': title,
             'tGain': now,
             'tExpired': tExpired,
             'tAttr': tAttr})

    def delTitle(self, title):
        self.pop(title, None)

    def hasTitle(self, title):
        return self.has_key(title)

    def getTitle(self):
        return self.keys()

    def isTitleExpired(self, title):
        if not self.has_key(title):
            return True
        if self[title].tExpired == const.EFFECT_TITLE_VALID_TIME_INFINITE:
            return False
        return self[title].tExpired < self._getNow()

    def isAttrOut(self, title):
        if not self.has_key(title):
            return True
        if self[title].tAttr == const.EFFECT_TITLE_VALID_TIME_INFINITE:
            return False
        return self[title].tAttr < self._getNow()

    def _getNow(self):
        if BigWorld.component in 'client':
            return BigWorld.player().getServerTime()
        else:
            return utils.getNow()
