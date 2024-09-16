#Embedded file name: /WORKSPACE/data/entities/common/wenyin.o
import BigWorld
from userSoleType import UserSoleType
from userDictType import UserDictType
from item import Item, GemSlot
import utils
import commcalc
from data import equip_data as ED
from data import equip_gem_data as EGD
from cdata import wen_yin_data as WYD
from cdata import game_msg_def_data as GMDD
GEM_TYPE_YANG = 1
GEM_TYPE_YIN = 2
BASETYPE_EQUIP_GEM = 18

class WenYinVal(UserSoleType):

    def __init__(self):
        self.yangSlots = []
        self.yinSlots = []
        self._initSlot()

    def _initSlot(self):
        for idx in xrange(Item.GEM_SLOT_MAX_CNT):
            self.yangSlots.append(GemSlot(pos=idx))
            self.yinSlots.append(GemSlot(pos=idx))

    def getEquipGemSlot(self, gemType, gemPos):
        if gemType == GEM_TYPE_YANG and hasattr(self, 'yangSlots') and gemPos < len(self.yangSlots):
            return self.yangSlots[gemPos]
        if gemType == GEM_TYPE_YIN and hasattr(self, 'yinSlots') and gemPos < len(self.yinSlots):
            return self.yinSlots[gemPos]

    def _canAddGem(self, owner, gemPos, gemItem, isReplace = False, bMsg = True):
        if BigWorld.component in 'cell':
            channel = owner.client
        elif BigWorld.component in 'client':
            channel = owner
        if not gemItem or gemItem.type != BASETYPE_EQUIP_GEM:
            return False
        if not EGD.data.has_key(gemItem.getParentId()):
            return False
        if gemItem.hasLatch():
            bMsg and channel.showGameMsg(GMDD.data.ADD_EQUIP_GEM_FAIL_GEM_LATCH, ())
            return False
        if not hasattr(self, 'yangSlots') and not hasattr(self, 'yinSlots'):
            bMsg and channel.showGameMsg(GMDD.data.ADD_EQUIP_GEM_FAIL_NO_SLOTS, ())
            return False
        gemData = utils.getEquipGemData(gemItem.id)
        gemSlot = self.getEquipGemSlot(gemData.get('type'), gemPos)
        if not gemSlot or not isReplace and not gemSlot.isEmpty():
            return False
        if not gemItem.ownedBy(owner.gbId):
            bMsg and channel.showGameMsg(GMDD.data.ADD_EQUIP_GEM_FAIL_OWNER, ())
            return False
        partId = channel.wenYin.getPartId(self)
        if BigWorld.component == 'client':
            import gameglobal
            if gameglobal.rds.ui.equipChangeInlayV2.isSubMode:
                partId = channel.subWenYin.getPartId(self)
        cfgData = WYD.data.get(partId, {})
        gtp = cfgData.get('gemEquipType')
        if gemData.has_key('equipLimit') and gtp not in gemData['equipLimit']:
            bMsg and channel.showGameMsg(GMDD.data.ADD_EQUIP_GEM_FAIL_EQUIPTYPE, ())
            return False
        return True

    def isEmpty(self):
        for slot in self.yangSlots:
            if slot.gem:
                return False

        for slot in self.yinSlots:
            if slot.gem:
                return False

        return True


class WenYin(UserDictType):

    def __init__(self):
        super(WenYin, self).__init__()
        self._initWYVal()

    def _lateReload(self):
        super(WenYin, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def _initWYVal(self):
        for part in WYD.data.iterkeys():
            if part in self:
                continue
            self[part] = WenYinVal()

    def getGemSlot(self, part, gemType, gemPos):
        if part not in self:
            return None
        wenYinVal = self[part]
        if gemType == Item.GEM_TYPE_YANG and gemPos < len(wenYinVal.yangSlots):
            return wenYinVal.yangSlots[gemPos]
        if gemType == Item.GEM_TYPE_YIN and gemPos < len(wenYinVal.yinSlots):
            return wenYinVal.yinSlots[gemPos]

    def getPartId(self, wenYinSlotVal):
        for partId, wenYinVal in self.iteritems():
            if wenYinVal == wenYinSlotVal:
                return partId

        return 0

    def getWYSlots(self, part):
        if part not in self:
            return None
        return self[part]

    def checkGemOrder(self, equipment, gemId, partId):
        if not equipment[partId]:
            return False
        gemData = utils.getEquipGemData(gemId)
        return equipment[partId].addedOrder >= gemData.get('orderLimit', 0)

    def isPartValid(self, equipment, part, gemType, gemPos):
        partEqupment = equipment[part]
        if not hasattr(partEqupment, 'yangSlots') or not hasattr(partEqupment, 'yinSlots'):
            return False
        if gemType == Item.GEM_TYPE_YANG:
            equpmentSlotValid = bool(partEqupment and gemPos < len(self.getWYSlots(part).yangSlots) and gemPos < len(partEqupment.yangSlots) and self.getWYSlots(part).yangSlots[gemPos] and self.getWYSlots(part).yangSlots[gemPos].gem and partEqupment.yangSlots[gemPos].state != Item.GEM_SLOT_LOCKED)
            equpmentSlotValid = equpmentSlotValid and self.checkGemOrder(equipment, self.getWYSlots(part).yangSlots[gemPos].gem.id, part)
        else:
            equpmentSlotValid = bool(partEqupment and gemPos < len(self.getWYSlots(part).yinSlots) and gemPos < len(partEqupment.yinSlots) and self.getWYSlots(part).yinSlots[gemPos] and self.getWYSlots(part).yinSlots[gemPos].gem and partEqupment.yinSlots[gemPos].state != Item.GEM_SLOT_LOCKED)
            equpmentSlotValid = equpmentSlotValid and self.checkGemOrder(equipment, self.getWYSlots(part).yinSlots[gemPos].gem.id, part)
        return bool(equpmentSlotValid)

    def isEmpty(self):
        for val in self.itervalues():
            if not val.isEmpty():
                return False

        return True
