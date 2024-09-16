#Embedded file name: I:/bag/tmp/tw2/res/entities\client/StaticPot.o
import BigWorld
from iPot import IPot

class StaticPot(IPot):

    def __init__(self):
        super(StaticPot, self).__init__()

    def afterModelFinish(self):
        super(StaticPot, self).afterModelFinish()
        self.filter = BigWorld.DumbFilter()
        self.filter.clientYawMinDist = 0.0
