#Embedded file name: I:/bag/tmp/tw2/res/entities\common/exploreEquipmentInfo.o
import utils
from exploreEquipment import ExploreEquipment
from userInfo import UserInfo
from const import EXPLORE_EQUIP_NUM, CONT_EMPTY_VAL

class ExploreEquipmentInfo(UserInfo):

    def createObjFromDict(self, dict):
        equipment = ExploreEquipment()
        for child in dict['item']:
            part = child['part']
            if equipment.isInvalid(part):
                continue
            it = utils.createItemObjFromDict(child)
            equipment[part] = it

        equipment.version = dict['version']
        equipment.freeze = dict['freeze']
        equipment.consistent()
        return equipment

    def getDictFromObj(self, obj):
        equipItems = []
        for part in xrange(EXPLORE_EQUIP_NUM):
            it = obj[part]
            if it == CONT_EMPTY_VAL:
                continue
            prop = utils.getItemSaveData_X(part, it)
            if not prop:
                continue
            equipItems.append(prop)

        d = {'item': equipItems,
         'version': obj.version,
         'freeze': obj.freeze}
        return d

    def isSameType(self, obj):
        return type(obj) is ExploreEquipment


instance = ExploreEquipmentInfo()
