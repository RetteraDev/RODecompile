#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/tickManager.o
import BigWorld

class Tick(object):

    def __init__(self, interval, func, *args):
        super(Tick, self).__init__()
        self.stop = False
        self.func = func
        self.args = args
        self.interval = interval
        self.callbackId = None

    def tickFunc(self):
        if self.stop:
            return
        if not self.func:
            return
        self.func(*self.args)
        self.callbackId = BigWorld.callback(self.interval, self.tickFunc)

    def stopTick(self):
        if self.callbackId:
            BigWorld.cancelCallback(self.callbackId)
        self.callbackId = None
        self.stop = True


class TickManager(object):

    def __init__(self):
        super(TickManager, self).__init__()
        self.count = 1
        self.ticks = {}

    def addTick(self, interval, func, *args):
        tick = Tick(interval, func, *args)
        tickID = self.count
        self.ticks[self.count] = tick
        self.count += 1
        BigWorld.callback(interval, tick.tickFunc)
        return tickID

    def stopTick(self, TickID):
        tick = self.ticks.get(TickID, None)
        if tick:
            tick.stopTick()
            del self.ticks[TickID]

    def stopAllTick(self):
        tickIds = self.ticks.keys()
        for tickId in tickIds:
            if self.ticks[tickId]:
                self.ticks[tickId].stop()

        self.ticks.clear()


_tickManager = None

def getInstance():
    global _tickManager
    if not _tickManager:
        _tickManager = TickManager()
    return _tickManager


def addTick(interval, func, *args):
    return getInstance().addTick(interval, func, *args)


def stopTick(TickID):
    getInstance().stopTick(TickID)


def stopAllTick():
    getInstance().stopAllTick()
