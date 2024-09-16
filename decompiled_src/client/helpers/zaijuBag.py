#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/zaijuBag.o
import BigWorld
import const
from container import Container

class ZaijuBag(Container):

    def __init__(self, pageCount = const.ZAIJU_BAG_PAGE_NUM, width = const.ZAIJU_BAG_WIDTH, height = const.ZAIJU_BAG_HEIGHT):
        super(ZaijuBag, self).__init__(pageCount, width, height)

    def countZaijuBagNum(self):
        num = 0
        for pos in xrange(const.ZAIJU_BAG_PAGE_SIZE):
            if self.getQuickVal(0, pos) != const.CONT_EMPTY_VAL:
                num += 1

        return num

    def searchAllPosByID(self, itemId, isBlack):
        p = BigWorld.player()
        allPos = []
        for pos in xrange(const.ZAIJU_BAG_PAGE_SIZE):
            item = self.getQuickVal(0, pos)
            if item == const.CONT_EMPTY_VAL:
                continue
            if item.id != itemId:
                continue
            elif hasattr(item, 'ownerGbId'):
                if isBlack and item.ownerGbId != p.gbId:
                    allPos.append(pos)
                elif not isBlack and item.ownerGbId == p.gbId:
                    allPos.append(pos)

        return allPos

    def getBlackItemInfo(self):
        p = BigWorld.player()
        info = {}
        for pos in xrange(const.ZAIJU_BAG_PAGE_SIZE):
            item = self.getQuickVal(0, pos)
            if item == const.CONT_EMPTY_VAL:
                continue
            if hasattr(item, 'ownerGbId') and item.ownerGbId != p.gbId:
                if not info.has_key(item.id):
                    info[item.id] = []
                info[item.id].append(pos)

        return info

    def findItemByUUID(self, uuid):
        for pos in xrange(const.ZAIJU_BAG_PAGE_SIZE):
            item = self.getQuickVal(0, pos)
            if item == const.CONT_EMPTY_VAL:
                continue
            if item.uuid != uuid:
                continue
            else:
                return (item, 0, pos)

        return (const.CONT_EMPTY_VAL, const.CONT_NO_PAGE, const.CONT_NO_POS)
