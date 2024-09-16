#Embedded file name: I:/bag/tmp/tw2/res/entities\common/exploreEquipment.o
import BigWorld
import const
import gametypes
from item import Item
import utils
from userListType import UserListType
from const import EXPLORE_EQUIP_NUM, CONT_EMPTY_VAL
from pickledItem import PickledItem

class ExploreEquipment(UserListType):

    def __init__(self):
        super(ExploreEquipment, self).__init__()
        self.extend([ CONT_EMPTY_VAL for x in xrange(EXPLORE_EQUIP_NUM) ])
        self.version = 0
        self.freeze = 0

    def _lateReload(self):
        super(ExploreEquipment, self)._lateReload()
        for part in xrange(len(self)):
            if self.isInvalid(part):
                continue
            if self.isEmpty(part):
                continue
            self[part].reloadScript()

    def _isValidPart(self, part):
        if 0 <= part < EXPLORE_EQUIP_NUM:
            return True
        return False

    def consistent(self):
        if not hasattr(self, 'version'):
            return False
        currVer = Item.TIMESTAMP
        if self.version == currVer:
            return False
        for part in self.getPartTuple():
            it = self.get(part)
            if it == CONT_EMPTY_VAL:
                continue
            it.consistent()

        self.version = currVer
        return True

    def transfer(self, owner):
        for part in self.getPartTuple():
            it = self.get(part)
            if it == CONT_EMPTY_VAL:
                continue
            owner.client.resSet(const.RES_KIND_EXPLORE_EQUIP, it, 0, part)

    def isInvalid(self, part):
        if 0 <= part < EXPLORE_EQUIP_NUM:
            return False
        return True

    def isEmpty(self, part):
        return self[part] == CONT_EMPTY_VAL

    def isFill(self, part):
        return not self.isEmpty(part)

    def isConsumable(self, part):
        if part in (gametypes.EXPLORE_EQUIP_SCROLL,):
            return True
        return False

    def getPartTuple(self):
        parts = []
        for part in xrange(len(self)):
            if self._isValidPart(part):
                parts.append(part)

        return parts

    def _reportCritical(self, part, obj):
        if BigWorld.component in ('base', 'cell'):
            import gameengine
            gameengine.reportCritical('Verify in Equip(%d):%d(%s,%s),%d(%d)' % (part,
             obj.id,
             obj.name,
             obj.guid(),
             obj.cwrap,
             obj.mwrap))

    def verifyObj(self, part):
        obj = self[part]
        if not obj:
            return
        if obj.cwrap <= 0 or obj.cwrap > obj.mwrap:
            self._reportCritical(part, obj)

    def get(self, part, changeToItem = True):
        try:
            it = self[part]
            if it.__class__ is PickledItem and changeToItem:
                it.changeToItem()
            return it
        except IndexError:
            return CONT_EMPTY_VAL

    def set(self, part, e = CONT_EMPTY_VAL):
        if not self._isValidPart(part):
            return False
        self[part] = e
        self.verifyObj(part)
        return True

    def equipItem(self, owner, part, it):
        self.set(part, it)
        owner.client.resSet(const.RES_KIND_EXPLORE_EQUIP, it, 0, part)
        if part == gametypes.EXPLORE_EQUIP_COMPASS:
            self.regenTime = utils.getNow()

    def unEquipItem(self, owner, part):
        self.set(part, CONT_EMPTY_VAL)
        owner.client.resRemove(const.RES_KIND_EXPLORE_EQUIP, 0, part)

    def getSendData(self, changeToItem = True):
        data = [ None for x in xrange(EXPLORE_EQUIP_NUM) ]
        for part in xrange(EXPLORE_EQUIP_NUM):
            it = self.get(part, changeToItem=changeToItem)
            if it == CONT_EMPTY_VAL:
                continue
            data[part] = it.copyDict()

        return data

    def isRefuse(self, owner):
        if self.isLock():
            return True
        if self.freeze != 0:
            return True
        return False

    def isLock(self):
        return self.state == 1
