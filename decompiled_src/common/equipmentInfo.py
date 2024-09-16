#Embedded file name: I:/bag/tmp/tw2/res/entities\common/equipmentInfo.o
import utils
from equipment import Equipment
from userInfo import UserInfo
from const import EQUIP_PART_NUM, CONT_EMPTY_VAL

class EquipmentInfo(UserInfo):

    def createObjFromDict(self, dict):
        equipment = Equipment()
        for child in dict['item']:
            part = child['part']
            if equipment.isInvalid(part):
                continue
            it = utils.createItemObjFromDict(child)
            equipment[part] = it

        equipment.version = dict['version']
        equipment.freeze = dict['freeze']
        equipment.suit = dict['suit']
        equipment.locker = dict['locker']
        equipment.opstr = dict['opstr']
        equipment.state = dict['state']
        equipment.consistent()
        return equipment

    def getDictFromObj(self, obj):
        them = []
        for i in xrange(EQUIP_PART_NUM):
            it = obj[i]
            if it == CONT_EMPTY_VAL:
                continue
            prop = utils.getItemSaveData_X(i, it)
            if not prop:
                continue
            them.append(prop)

        d = {'item': them,
         'suit': obj.suit,
         'version': obj.version,
         'freeze': obj.freeze,
         'locker': obj.locker,
         'opstr': obj.opstr,
         'state': obj.state}
        return d

    def isSameType(self, obj):
        return type(obj) is Equipment


instance = EquipmentInfo()
