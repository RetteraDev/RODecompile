#Embedded file name: I:/bag/tmp/tw2/res/entities\common/noviceDailyOnline.o
import utils
import const
from userSoleType import UserSoleType

class NoviceDailyOnline(UserSoleType):

    def __init__(self, phase = 1, total = 0, start = 0):
        self.phase = phase
        self.total = total
        self.start = start
        if not self.start:
            self.start = utils.getNow()

    def reset(self):
        self.phase = 1
        self.total = 0
        self.start = utils.getNow()

    def nextPhase(self):
        self.phase += 1
        self.total = 0
        self.start = utils.getNow()

    def logon(self, lastLogoffTime):
        now = utils.getNow()
        if not utils.isSameDay(lastLogoffTime, now) and not utils.isSameDay(self.start, now):
            self.reset()
        self.start = now

    def logoff(self):
        self.total += utils.getNow() - self.start
        self.start = utils.getNow()
        if self.total < 0 or self.total > const.SECONDS_PER_DAY:
            self.total = 0

    def getLogonTime(self):
        ret = self.total
        if self.start:
            ret += utils.getNow() - self.start
        return ret
