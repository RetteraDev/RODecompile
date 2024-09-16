#Embedded file name: I:/bag/tmp/tw2/res/entities\common/containerInfo.o
from userInfo import UserInfo
import utils

class ContainerInfo(UserInfo):

    def createContainer(self, dict, obj):
        posCount = obj.posCount
        pageCount = obj.pageCount
        for child in dict['item']:
            page = child['page']
            pos = child['pos']
            if page < 0 or page >= pageCount or pos < 0 or pos >= posCount:
                continue
            it = utils.createItemObjFromDict(child)
            obj.pages[page][pos] = it

        obj.consistent()
        return obj

    def saveContainer(self, obj, dict):
        if obj is not None and hasattr(obj, 'getSaveList'):
            dict['item'] = obj.getSaveList()
        else:
            dict['item'] = []
        return dict

    def createContainerFromStream(self, dict, obj):
        posCount = obj.posCount
        pageCount = obj.pageCount
        for child, page, pos in dict['item']:
            if page < 0 or page >= pageCount or pos < 0 or pos >= posCount:
                continue
            it = utils.createItemObjFromStream(child)
            obj.pages[page][pos] = it

        obj.consistent()
        return obj

    def streamContainer(self, obj, dict):
        dict['item'] = obj.getStreamList()
        return dict
