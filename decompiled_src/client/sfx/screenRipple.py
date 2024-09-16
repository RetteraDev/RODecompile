#Embedded file name: I:/bag/tmp/tw2/res/entities\client\sfx/screenRipple.o
import math
import random
import BigWorld
from callbackHelper import Functor
from gameclass import Singleton

class RippleRound(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.stamp = 1
        self.reset()

    def reset(self):
        self.xpos = 0
        self.ypos = 0
        self.angle = 0
        self.radius = 0.2
        self.radiusAdd = 0.05
        self.radiusMax = 0.5
        self.speed = 2
        self.randomScale = 0.02
        self.double = True

    def start(self):
        self.stamp += 1
        BigWorld.ripplePreset(0.975, 1)
        self.reset()
        self._ripple(self.stamp)

    def stop(self):
        self.stamp += 1

    def _ripple(self, stamp):
        if self.stamp != stamp:
            return
        dtime = 0.04
        self.angle += self.speed * dtime
        self.radius += self.radiusAdd * dtime
        if self.radius > self.radiusMax:
            self.radius = self.radiusMax
        self.xpos = math.sin(self.angle) * self.radius * 0.7 + (random.random() * 2 - 1) * self.randomScale
        self.ypos = math.cos(self.angle) * self.radius + (random.random() * 2 - 1) * self.randomScale
        BigWorld.addScreenRipple(self.xpos, self.ypos, 1)
        if self.double:
            BigWorld.addScreenRipple(-self.xpos, -self.ypos, 1)
        BigWorld.callback(0.02, Functor(self._ripple, stamp))

    def rippleWholeScreen(self):
        for r in xrange(0, 5):
            self.radius = 0.2 * r
            l = int(15 + r * 2)
            for x in xrange(0, l):
                self.angle = math.pi * 2 / l * x
                self.xpos = math.sin(self.angle) * self.radius * 0.7 + (random.random() * 2 - 1) * self.randomScale
                self.ypos = math.cos(self.angle) * self.radius + (random.random() * 2 - 1) * self.randomScale
                BigWorld.addScreenRipple(self.xpos, self.ypos, 1)
                BigWorld.addScreenRipple(-self.xpos, -self.ypos, 1)


def rippleScreen():
    RippleRound.getInstance().rippleWholeScreen()


def start():
    RippleRound.getInstance().start()


def stop():
    RippleRound.getInstance().stop()
