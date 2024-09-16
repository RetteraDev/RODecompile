#Embedded file name: /WORKSPACE/data/entities/common/guanyin.o
import BigWorld
import const
from formula import calcCombatScoreType
import gameconfigCommon
import utils
from userSoleType import UserSoleType
from userDictType import UserDictType
from cdata import guanyin_book_data as GBD
if BigWorld.component != 'client':
    from permanentLocker import PermanentLocker

class GuanYinSlotVal(UserSoleType):

    def __init__(self, slotId, valid = False):
        self.slotId = slotId
        self.valid = valid
        self.guanYinStat = -1
        self.guanYinInfo = [-1, -1, -1]
        self.state = 0

    def setGuanYinInfo(self, part, bookId):
        if part < 0 or part >= len(self.guanYinInfo):
            return False
        self.guanYinInfo[part] = bookId

    def updateGuanYinStat(self, part):
        self.guanYinStat = part

    def checkAndUpdateGuanYinPart(self, part):
        if self.guanYinStat < 0:
            self.guanYinStat = part
            return True
        return False

    def getGuanYinPskill(self):
        if not gameconfigCommon.enableGuanYinThirdPhase():
            return []
        if self.guanYinStat < 0:
            return []
        if self.guanYinInfo[self.guanYinStat] < 0:
            return []
        bookId = self.guanYinInfo[self.guanYinStat]
        bd = GBD.data.get(bookId)
        if not bd:
            return []
        res = []
        pskIds = bd.get('pskillId', [])
        for pskId in pskIds:
            res.append((pskId, bd.get('lv', 1), self.slotId))

        return res


class GuanYinBookVal(UserSoleType):

    def __init__(self, bookId, valid = False):
        self.bookId = bookId
        self.valid = valid
        self.state = 0
        self.guanYinSuperBookId = 0
        self.guanYinSuperPskillExpire = 0

    def isExpired(self):
        if self.guanYinSuperBookId > 0 and self.guanYinSuperPskillExpire > 0 and utils.getNow() > self.guanYinSuperPskillExpire:
            return True
        return False

    def getGuanYinBookPSkill(self, ignoreTime = False):
        if not gameconfigCommon.enableGuanYinThirdPhase() or not gameconfigCommon.enableGuanYinSuperSkill():
            return []
        if self.guanYinSuperBookId <= 0:
            return []
        if not ignoreTime:
            now = utils.getNow()
            if now > self.guanYinSuperPskillExpire:
                return []
        res = []
        bd = GBD.data.get(self.guanYinSuperBookId)
        if bd:
            pskIds = bd.get('pskillId', [])
            for pskId in pskIds:
                res.append((pskId, bd.get('lv', 1), self.bookId))

        return res

    def checkGuanYinSuperSkill(self):
        if self.guanYinSuperBookId > 0 and self.guanYinSuperPskillExpire > 0 and utils.getNow() < self.guanYinSuperPskillExpire:
            return True
        return False


class GuanYin(UserDictType):

    def __init__(self):
        self.books = {}
        self.lastApplyNum = 0
        self.combatScore = 0

    def _lateReload(self):
        super(GuanYin, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def addBook(self, guanYinBook):
        if self.books.has_key(guanYinBook.bookId):
            return False
        self.books[guanYinBook.bookId] = guanYinBook

    def removeBook(self, bookId):
        if not self.books.get(bookId):
            return False
        return self.books.pop(bookId)

    def initGuanYinSlot(self, slotNum):
        for i in xrange(slotNum):
            if not self.has_key(i):
                self[i] = GuanYinSlotVal(i, valid=True)

    def initGuanYinBook(self, bookNum):
        for i in xrange(bookNum):
            if not self.books.has_key(i):
                self.addBook(GuanYinBookVal(i, valid=True))

    def setGuanYinInfo(self, slot, part, bookId):
        info = self.get(slot)
        if not info:
            return False
        return info.setGuanYinInfo(part, bookId)

    def getActiveGuanYinPskill(self, limitNo = 0):
        if not gameconfigCommon.enableGuanYinThirdPhase():
            return []
        res = []
        now = utils.getNow()
        for slotId, info in self.iteritems():
            if slotId >= limitNo:
                continue
            part = info.guanYinStat
            if part < 0:
                continue
            if info.guanYinInfo[part] < 0:
                continue
            bookId = info.guanYinInfo[part]
            bd = GBD.data.get(bookId)
            if not bd:
                continue
            pskIds = bd.get('pskillId', [])
            for pskId in pskIds:
                res.append((pskId, bd.get('lv', 1), slotId))

        for bookId, info in self.books.iteritems():
            if info.guanYinSuperBookId > 0 and now < info.guanYinSuperPskillExpire:
                bd = GBD.data.get(info.guanYinSuperBookId)
                if bd:
                    pskIds = bd.get('pskillId', [])
                    for pskId in pskIds:
                        res.append((pskId, bd.get('lv', 1), bookId))

        return res

    def calcGuanYinPSkillScore(self, validNum):
        if not gameconfigCommon.enableGuanYinThirdPhase():
            return 0
        score = 0
        for info in self.itervalues():
            if info.slotId >= validNum:
                continue
            tmax = 0
            for bookId in info.guanYinInfo:
                if bookId < 0:
                    continue
                bd = GBD.data.get(bookId)
                if not bd:
                    continue
                tmax = max(bd.get('score', 0), tmax)

            score += tmax

        return score

    def calcGuanYinPSkillScoreType(self):
        scoreType = [0,
         0,
         0,
         0]
        for info in self.itervalues():
            tmax = 0
            tmaxType = [0,
             0,
             0,
             0]
            for bookId in info:
                if bookId < 0:
                    continue
                bd = GBD.data.get(bookId)
                if not bd:
                    continue
                if bd.get('score', 0) > tmax:
                    tmax = bd.get('score', 0)
                    tmaxType = bd.get('scoreType', [])

            scoreType = calcCombatScoreType(scoreType, tmaxType, [], tmax, const.COMBAT_SCORE_TYPE_OP_COEFF)

        return scoreType

    def getAllGuanYinPskill(self):
        res = []
        for info in self.itervalues():
            for bookId in info.guanYinInfo:
                if bookId < 0:
                    continue
                bd = GBD.data.get(bookId)
                if not bd:
                    continue
                pskIds = bd.get('pskillId', [])
                for pskId in pskIds:
                    res.append(pskId)

        now = utils.getNow()
        for info in self.books.itervalues():
            if info.guanYinSuperBookId > 0 and now < info.guanYinSuperPskillExpire:
                bd = GBD.data.get(info.guanYinSuperBookId)
                if bd:
                    pskIds = bd.get('pskillId', [])
                    for pskId in pskIds:
                        res.append(pskId)

        return res

    def validGuanYinPos(self, slot, part):
        info = self.get(slot)
        if not info:
            return False
        if part < 0 or part >= len(info.guanYinInfo):
            return False
        return True

    def updateGuanYinStat(self, slot, part):
        info = self.get(slot)
        if not info:
            return
        info.guanYinStat = part

    def getValidGuanYinBookPSkill(self):
        tNow = utils.getNow()
        res = []
        for bookId, info in self.books.iteritems():
            if info.guanYinSuperBookId > 0 and tNow < info.guanYinSuperPskillExpire:
                bd = GBD.data.get(info.guanYinSuperBookId)
                if bd:
                    pskIds = bd.get('pskillId', [])
                    for pskId in pskIds:
                        res.append((pskId, bd.get('lv', 1), bookId))

        return res

    def getExpiredGuanYinBookPSkill(self):
        res = []
        for book in self.books.itervalues():
            if not book.isExpired():
                continue
            res.extend(book.getGuanYinBookPSkill(ignoreTime=True))

        return res

    def getLastExpiredGuanYinBookPSkill(self, startTime, endTime):
        res = []
        for book in self.books.itervalues():
            if startTime <= book.guanYinSuperPskillExpire < endTime:
                res.extend(book.getGuanYinBookPSkill(ignoreTime=True))

        return res

    def checkGuanYinPskillTimeOut(self, slot, part):
        if not self.validGuanYinPos(slot, part):
            return False
        now = utils.getNow()
        if not hasattr(self, 'guanYinExtraInfo'):
            return False
        extra = self.guanYinExtraInfo[slot][part]
        if extra.has_key('expireTime') and now > extra['expireTime']:
            return True
        if extra.has_key('commonExpireTime') and now > extra['commonExpireTime']:
            return True
        return False

    def getSuperSkillBook(self):
        for book in self.books.itervalues():
            if book and book.guanYinSuperBookId:
                return book

    @property
    def guanYinInfo(self):
        keys = self.keys()
        keys.sort()
        return [ self[key].guanYinInfo for key in keys ]
