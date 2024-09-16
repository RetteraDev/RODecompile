#Embedded file name: /WORKSPACE/data/entities/common/cbgitem.o
from userSoleType import UserSoleType
from userDictType import UserDictType

class CbgItem(UserSoleType):

    def __init__(self):
        self.consignItem = {}
        self.purchaseItem = {}

    def fromDTO(self, dto):
        self.consignItem, self.purchaseItem = dto

    def getDTO(self):
        return (self.consignItem, self.purchaseItem)


class CbgStubItem(UserSoleType):

    def __init__(self, gbId = 0, roleName = '', hostId = 0, it = None, price = 0, days = 0, argue = False, tProtect = 0, favor = 0, opNUID = 0):
        self.gbId = gbId
        self.roleName = roleName
        self.hostId = hostId
        self.it = it
        self.price = price
        self.days = days
        self.argue = argue
        self.tProtect = tProtect
        self.favor = favor
        self.opNUID = opNUID


class CbgStubItemDict(UserDictType):

    def _lateReload(self):
        super(CbgStubItemDict, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
