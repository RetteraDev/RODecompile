#Embedded file name: I:/bag/tmp/tw2/res/entities\common/carrouselSeats.o
"""
Created on 2014-7-4

@author: Administrator
"""
from userDictType import UserDictType
from userType import UserMultiDispatch

class CarrouselSeats(UserDictType, UserMultiDispatch):

    def __init__(self):
        super(CarrouselSeats, self).__init__()

    def _lateReload(self):
        super(CarrouselSeats, self)._lateReload()

    def joinSeat(self, member):
        if not self.has_key(member):
            self[member] = self.assignInx()

    def assignInx(self):
        inx = 1
        for i in sorted(self.itervalues()):
            if inx < i:
                break
            inx += 1

        return inx

    def reset(self):
        self.clear()

    def leave(self, leaveID):
        self.pop(leaveID, None)
        if not len(self) >= 1:
            self.reset()
