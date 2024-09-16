#Embedded file name: I:/bag/tmp/tw2/res/entities\common/lifeEquipmentInfo.o
import utils
from lifeEquipment import LifeEquipment
from userInfo import UserInfo
from iStreamInfo import bindStream
from const import CONT_EMPTY_VAL

class LifeEquipmentInfo(UserInfo):

    def createObjFromDict(self, dict, isStream = False):
        equipment = LifeEquipment()
        if isStream:
            for child, subType, part in dict['items']:
                it = utils.createItemObjFromStream(child)
                equipment[subType, part] = it

        else:
            for child in dict['items']:
                subType = child['subType']
                part = child['part']
                it = utils.createItemObjFromDict(child)
                equipment[subType, part] = it

        equipment.version = dict['version']
        equipment.freeze = dict['freeze']
        equipment.consistent()
        return equipment

    def getDictFromObj(self, obj, isStream = False):
        them = []
        for subType, part in obj.keys():
            it = obj[subType, part]
            if it == CONT_EMPTY_VAL:
                continue
            if isStream:
                prop = utils.getItemStreamData_L(subType, part, it)
            else:
                prop = utils.getItemSaveData_L(subType, part, it)
            if not prop:
                continue
            them.append(prop)

        d = {'items': them,
         'version': obj.version,
         'freeze': obj.freeze}
        return d

    def _createObjFromStream(self, stream):
        return self.createObjFromDict(stream, True)

    def _getStreamFromObj(self, obj):
        return self.getDictFromObj(obj, True)

    def isSameType(self, obj):
        return type(obj) is LifeEquipment


instance = LifeEquipmentInfo()
