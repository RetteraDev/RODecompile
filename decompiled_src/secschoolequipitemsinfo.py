#Embedded file name: /WORKSPACE/data/entities/common/secschoolequipitemsinfo.o
import utils
from userInfo import UserInfo
from const import EQUIP_PART_NUM
from secSchoolEquipItems import SecSchoolEquip

class SecSchoolEquipItemsInfo(UserInfo):

    def createObjFromDict(self, dict):
        mainEquipItems = {}
        subEquipItems = {}
        mainEquipConfig = dict['mainEquipConfig']
        subEquipConfig = dict['subEquipConfig']
        for child in dict['mainEquipItems']:
            part = child['part']
            it = utils.createItemObjFromDict(child)
            mainEquipItems[part] = it

        for child in dict['subEquipItems']:
            part = child['part']
            it = utils.createItemObjFromDict(child)
            subEquipItems[part] = it

        equipment = SecSchoolEquip(mainEquipItems, subEquipItems, mainEquipConfig, subEquipConfig)
        return equipment

    def getDictFromObj(self, obj):
        mainItems, subItems = [], []
        for i in xrange(EQUIP_PART_NUM):
            mainItem, subItem = obj.mainEquipItems.get(i), obj.subEquipItems.get(i)
            if mainItem:
                prop = utils.getItemSaveData_X(i, mainItem)
                prop and mainItems.append(prop)
            if subItem:
                prop = utils.getItemSaveData_X(i, subItem)
                prop and subItems.append(prop)

        d = {'mainEquipItems': mainItems,
         'mainEquipConfig': obj.mainEquipConfig,
         'subEquipItems': subItems,
         'subEquipConfig': obj.subEquipConfig}
        return d

    def isSameType(self, obj):
        return type(obj) is SecSchoolEquip


instance = SecSchoolEquipItemsInfo()
