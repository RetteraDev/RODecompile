#Embedded file name: I:/bag/tmp/tw2/res/entities\common/fishingEquipment.o
import BigWorld
import const
import gametypes
from item import Item
from userListType import UserListType
from const import FISHING_EQUIP_NUM, CONT_EMPTY_VAL
from pickledItem import PickledItem

class FishingEquipment(UserListType):
    enhanceItems = {gametypes.FISHING_EQUIP_ROD: gametypes.FISHING_EQUIP_ENHANCE_ROD,
     gametypes.FISHING_EQUIP_HOOK: gametypes.FISHING_EQUIP_ENHANCE_HOOK,
     gametypes.FISHING_EQUIP_BUOY: gametypes.FISHING_EQUIP_ENHANCE_BUOY}

    def __init__(self):
        super(FishingEquipment, self).__init__()
        self.extend([ CONT_EMPTY_VAL for x in xrange(FISHING_EQUIP_NUM) ])
        self.version = 0
        self.freeze = 0
        self.isEnhance = {gametypes.FISHING_EQUIP_ROD: False,
         gametypes.FISHING_EQUIP_HOOK: False,
         gametypes.FISHING_EQUIP_BUOY: False}

    def _lateReload(self):
        super(FishingEquipment, self)._lateReload()
        for part in xrange(len(self)):
            if self.isInvalid(part):
                continue
            if self.isEmpty(part):
                continue
            self[part].reloadScript()

    def _isValidPart(self, part):
        if 0 <= part < FISHING_EQUIP_NUM:
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

    def isConsumable(self, part):
        if part in (gametypes.FISHING_EQUIP_BAIT,
         gametypes.FISHING_EQUIP_ENHANCE_BUOY,
         gametypes.FISHING_EQUIP_ENHANCE_HOOK,
         gametypes.FISHING_EQUIP_ENHANCE_ROD):
            return True
        return False

    def switchEnhance(self, owner, part, isEnhance):
        if part in self.enhanceItems.keys():
            self.isEnhance[part] = isEnhance

    def isInvalid(self, part):
        if 0 <= part < FISHING_EQUIP_NUM:
            return False
        return True

    def isEmpty(self, part):
        return self[part] == CONT_EMPTY_VAL

    def isFill(self, part):
        return not self.isEmpty(part)

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

    def move(self, srcPart, dstPart):
        if not self._isValidPart(srcPart):
            return False
        if not self.isEmpty(dstPart):
            return False
        self[dstPart] = self[srcPart]
        self[srcPart] = CONT_EMPTY_VAL
        return True

    def isEquip(self, tp, stp):
        equiped = False
        for part in xrange(FISHING_EQUIP_NUM):
            equ = self[part]
            if equ != CONT_EMPTY_VAL and equ.type == tp and equ.fishingEquipType == stp:
                equiped = True
                break

        return equiped

    def countBlank(self):
        cnt = 0
        for part in xrange(len(self)):
            if self.isEmpty(part):
                cnt += 1

        return cnt

    def countAllObj(self):
        cnt = 0
        for part in xrange(len(self)):
            if self.isEmpty(part):
                continue
            cnt += 1

        return cnt

    def countNum(self):
        cnt = 0
        for part in xrange(len(self)):
            if not self.isEmpty(part):
                cnt += 1

        return cnt

    def findItemByAttr(self, attr):
        for part, it in enumerate(self):
            it = self.get(part)
            if it == CONT_EMPTY_VAL:
                continue
            for k, v in attr.iteritems():
                if not hasattr(it, k):
                    break
                if getattr(it, k) != v:
                    break
            else:
                return part

        return const.CONT_NO_POS

    def equipItem(self, owner, part, it):
        self.set(part, it)
        owner.client.resSet(const.RES_KIND_FISHING_QUIP, it, 0, part)
        if part == gametypes.FISHING_EQUIP_ROD:
            owner.setAspect(gametypes.EQU_PART_FISHING_ROD, it.id, useRealAspect=True)

    def unEquipItem(self, owner, part):
        self.set(part, CONT_EMPTY_VAL)
        owner.client.resRemove(const.RES_KIND_FISHING_QUIP, 0, part)
        if part == gametypes.FISHING_EQUIP_ROD:
            owner.setAspect(gametypes.EQU_PART_FISHING_ROD, 0, useRealAspect=True)

    def transfer(self, owner):
        for part, e in enumerate(self):
            if self.isEmpty(part):
                continue
            e = self.get(part)
            owner.client.resSet(const.RES_KIND_FISHING_QUIP, e, 0, part)

    def getSendData(self, changeToItem = True):
        data = [ None for x in xrange(FISHING_EQUIP_NUM) ]
        for part in xrange(FISHING_EQUIP_NUM):
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
