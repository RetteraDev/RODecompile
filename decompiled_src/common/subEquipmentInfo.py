#Embedded file name: I:/bag/tmp/tw2/res/entities\common/subEquipmentInfo.o
from subEquipment import SubEquipment
from containerInfo import ContainerInfo

class SubEquipmentInfo(ContainerInfo):

    def createObjFromDict(self, dict):
        subEquipment = SubEquipment()
        subEquipment.version = dict['version']
        subEquipment.freeze = dict['freeze']
        return self.createContainer(dict, subEquipment)

    def getDictFromObj(self, obj):
        dict = {}
        dict['version'] = obj.version
        dict['freeze'] = obj.freeze
        return self.saveContainer(obj, dict)

    def isSameType(self, obj):
        return type(obj) is SubEquipment


instance = SubEquipmentInfo()
