#Embedded file name: I:/bag/tmp/tw2/res/entities\common/lifeEquipment.o
import BigWorld
import const
import copy
from userDictType import UserDictType
from const import CONT_EMPTY_VAL
from item import Item
from pickledItem import PickledItem
from data import life_skill_equip_data as LSEPD
if BigWorld.component in ('base', 'cell'):
    import Netease
    import gameconfig
    import gameconst
    import serverlog
    import logconst
    from data import log_src_def_data as LSDD

class LifeEquipment(UserDictType):

    def __init__(self):
        super(LifeEquipment, self).__init__()
        self.version = 0
        self.freeze = 0

    def _lateReload(self):
        super(LifeEquipment, self)._lateReload()
        for val in self.itervalues():
            if val:
                val.reloadScript()

    def consistent(self):
        if not hasattr(self, 'version'):
            return False
        currVer = Item.TIMESTAMP
        if self.version == currVer:
            return False
        for subType, part in self.iterkeys():
            it = self.get(subType, part)
            if it == CONT_EMPTY_VAL:
                continue
            it.consistent()

        self.version = currVer
        return True

    def transfer(self, owner):
        for subType, part in self.iterkeys():
            it = self.get(subType, part)
            if it == CONT_EMPTY_VAL:
                continue
            owner.client.resSet(const.RES_KIND_LIFE_EQUIP, it, 0, part)

    def isEmpty(self, subType, part):
        if not self.has_key((subType, part)):
            return True
        return self[subType, part] == CONT_EMPTY_VAL

    def isFill(self, subType, part):
        if not self.has_key((subType, part)):
            return False
        return not self.isEmpty(subType, part)

    def _reportCritical(self, subType, part, obj):
        if BigWorld.component in ('base', 'cell'):
            import gameengine
            gameengine.reportCritical('Verify in Equip(%d, %d):%d(%s,%s),%d(%d)' % (subType,
             part,
             obj.id,
             obj.name,
             obj.guid(),
             obj.cwrap,
             obj.mwrap))

    def verifyObj(self, subType, part):
        obj = self[subType, part]
        if not obj:
            return
        if obj.cwrap <= 0 or obj.cwrap > obj.mwrap:
            self._reportCritical(subType, part, obj)

    def get(self, subType, part, changeToItem = True):
        try:
            it = self[subType, part]
            if it.__class__ is PickledItem and changeToItem:
                it.changeToItem()
            return it
        except:
            return CONT_EMPTY_VAL

    def set(self, subType, part, e = CONT_EMPTY_VAL):
        self[subType, part] = e
        self.verifyObj(subType, part)
        return True

    def _applyLifeEquip(self, owner, equip):
        if not owner._isValidPropSrc(gameconst.AVATAR_PROP_SRC_LIFE_EQUIP):
            return
        if not gameconfig.enableNewPropCalc():
            return
        if owner.combatProp.effective_equip.has_key(equip.uuid):
            return
        if getattr(equip, 'cdura', 0) == 0:
            return
        d = LSEPD.data.get(equip.id)
        if not d:
            return
        for prop, type, value in d.get('gProps', []):
            owner.combatProp.addPretreatProp(owner, prop, type, value)

        owner.combatProp.effective_equip[equip.uuid] = True

    def _unApplyLifeEquip(self, owner, equip):
        if not gameconfig.enableNewPropCalc():
            return
        if not owner.combatProp.effective_equip.has_key(equip.uuid):
            return
        d = LSEPD.data.get(equip.id)
        if not d:
            return
        for prop, type, value in d.get('gProps', []):
            owner.combatProp.removePretreatProp(owner, prop, type, value)

        owner.combatProp.effective_equip.pop(equip.uuid)

    def equipItem(self, owner, subType, part, it, strong = True):
        oldEquipIt = copy.deepcopy(self.get(subType, part))
        if it.isEquipBind():
            equipIt = it.deepcopy()
            it.bindItem()
            if BigWorld.component in ('base', 'cell'):
                opNUID = Netease.getNUID()
                serverlog.genItemLog(owner, equipIt, 0, opNUID, LSDD.data.LOG_SRC_EQUIP_ITEM, detail=logconst.ITEM_EQUIP_BIND)
        if oldEquipIt != CONT_EMPTY_VAL:
            self._unApplyLifeEquip(owner, oldEquipIt)
        self.set(subType, part, it)
        self._applyLifeEquip(owner, it)
        owner._initBaseProp()
        owner.client.resInsert(const.RES_KIND_LIFE_EQUIP, it, subType, part)

    def unEquipItem(self, owner, subType, part, strong = True):
        it = self.get(subType, part)
        self.set(subType, part, CONT_EMPTY_VAL)
        self._unApplyLifeEquip(owner, it)
        owner._initBaseProp()
        owner.client.resRemove(const.RES_KIND_LIFE_EQUIP, subType, part)

    def getSendData(self, changeToItem = True):
        data = {}
        for subType, part in self.iterkeys():
            it = self.get(subType, part, changeToItem=changeToItem)
            if it == CONT_EMPTY_VAL:
                continue
            data[subType, part] = it.copyDict()

        return data

    def isRefuse(self, owner):
        if self.freeze != 0:
            return True
        return False
