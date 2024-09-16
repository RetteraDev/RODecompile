#Embedded file name: I:/bag/tmp/tw2/res/entities\client/MovablePot.o
import BigWorld
from iPot import IPot

class MovablePot(IPot):

    def __init__(self):
        super(MovablePot, self).__init__()

    def afterModelFinish(self):
        super(MovablePot, self).afterModelFinish()
        self.filter = BigWorld.AvatarFilter()
        self.filter.clientYawMinDist = 0.0
