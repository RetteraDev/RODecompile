#Embedded file name: I:/bag/tmp/tw2/res/entities\common/rideTogether.o
"""
Created on 2014-7-4

@author: Administrator
"""
import BigWorld
from userDictType import UserDictType
from userType import UserMultiDispatch

class RideTogether(UserDictType, UserMultiDispatch):

    def __init__(self, header = 0, typ = 0):
        super(RideTogether, self).__init__()
        self.header = header
        self.typ = typ

    def _lateReload(self):
        super(RideTogether, self)._lateReload()

    def isMajor(self, ownerID):
        return ownerID == self.header

    def inRide(self):
        return self.header > 0

    def getHeader(self):
        if self.header == 0:
            return None
        return BigWorld.entities.get(self.header)

    def canInvite(self):
        if self.header > 0 and len(self) >= 1:
            return False
        return True

    def joinRide(self, header, member):
        self.header = header
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
        self.header = 0
        self.typ = 0
        self.clear()

    def leave(self, leaveID):
        if self.isMajor(leaveID):
            self.reset()
        else:
            self.pop(leaveID, None)
            if not len(self) >= 1:
                self.reset()
