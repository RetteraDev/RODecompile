#Embedded file name: /WORKSPACE/data/entities/client/helpers/performancemonitor.o
import zlib
import cPickle
import random
import BigWorld
import boolparser
import gameglobal
import utils
import const
from gameclass import Singleton

class PerformanceCondition(object):

    def __init__(self, dict):
        self.__dict__ = dict
        self.lastTime = utils.getNow()
        condition = self.condition
        self.boolParse = boolparser.BooleanParser(condition)

    def check(self):
        now = utils.getNow()
        if now - self.lastTime >= self.interval:
            self.lastTime = now
            percent = random.random()
            if percent <= self.prob:
                if self.boolParse.evaluate(self.getVars()):
                    return 1
        return 0

    def getVars(self):
        p = BigWorld.player()
        combatScore = 0
        if p.combatScoreList:
            combatScore = p.combatScoreList[const.COMBAT_SCORE]
        return dict(zip(const.CLIENT_PERFORMANCE_FILTER_CONDITION, [p.spaceNo,
         p.mapID,
         p.position.x,
         p.position.z,
         p.lv,
         p.school,
         combatScore]))


class PerformanceMonitor(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.conditions = {}

    def init(self, dict):
        self.conditions.clear()
        for key, value in dict.iteritems():
            self.conditions[key] = PerformanceCondition(value)

    def add(self, dict):
        for key, value in dict.iteritems():
            self.conditions[key] = PerformanceCondition(value)

    def remove(self, keys):
        for key in keys:
            self.conditions.pop(key, None)

    def check(self):
        for key, condition in self.conditions.iteritems():
            if condition.check():
                self.genLog(key)

    def clearAll(self):
        self.conditions.clear()

    def genLog(self, key):
        perFormanceInfo = BigWorld.getPerformanceInfo()
        if not perFormanceInfo:
            return
        p = BigWorld.player()
        log = {'commitedMem': float(perFormanceInfo['commitedmem']),
         'phyMem': float(perFormanceInfo['phymem']),
         'availMem': float(perFormanceInfo['availmem']),
         'fps': BigWorld.getFps(),
         'gbId': p.gbId,
         'key': key}
        log = zlib.compress(cPickle.dumps(log, -1))
        p.base.recordClientPerFormanceByFilter(log)
