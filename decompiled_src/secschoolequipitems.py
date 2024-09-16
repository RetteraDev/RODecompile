#Embedded file name: /WORKSPACE/data/entities/common/secschoolequipitems.o
from userSoleType import UserSoleType

class SecSchoolEquip(UserSoleType):

    def __init__(self, mainEquipItems, subEquipItems, mainEquipConfig, subEquipConfig):
        self.mainEquipItems = mainEquipItems
        self.subEquipItems = subEquipItems
        self.mainEquipConfig = mainEquipConfig
        self.subEquipConfig = subEquipConfig

    def _lateReload(self):
        super(SecSchoolEquip, self)._lateReload()
