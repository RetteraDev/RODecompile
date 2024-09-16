#Embedded file name: I:/bag/tmp/tw2/res/entities\common/storageCommon.o
import const
from container import Container
from item import Item
from data import item_data as ID

class StorageCommon(Container):

    def __init__(self, pageCount = const.STORAGE_PAGE_NUM, width = const.STORAGE_WIDTH, height = const.STORAGE_HEIGHT):
        super(StorageCommon, self).__init__(pageCount, width, height)
        self.posCountDict = {}
        self.enabledPackSlotCnt = 0
        self.posCountDict[0] = self.width * self.height
        self.storagePackSlot = [const.CONT_EMPTY_VAL] * const.STORAGE_MAX_SLOT_NUM

    def getPosTuple(self, page):
        if not self._isValidPage(page):
            return ()
        return range(self.getPosCount(page))

    def getPosCount(self, page):
        return self.posCountDict.get(page, 0)

    def searchEmptyInPages(self):
        for pg in xrange(0, const.STORAGE_PAGE_NUM):
            dstPos = self.searchEmpty(pg)
            if dstPos != const.CONT_NO_POS:
                return (pg, dstPos)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def searchEmpty(self, page, startPos = 0):
        if not self._isValid(page, startPos):
            return const.CONT_NO_POS
        posCount = self.getPosCount(page)
        for ps in xrange(startPos, posCount):
            if not self.getQuickVal(page, ps):
                return ps
        else:
            return const.CONT_NO_POS

    def searchBestInPages(self, id, amount, src = None):
        if id not in ID.data or amount > ID.data[id].get('mwrap', 1):
            return (const.CONT_NO_PAGE, const.CONT_NO_POS)
        src = src or Item(id, cwrap=amount, genRandProp=False)
        if src.canWrap():
            for pg in xrange(0, const.STORAGE_PAGE_NUM):
                posCount = min(self.getPosCount(pg), const.STORAGE_PAGE_SIZE)
                for ps in xrange(posCount):
                    dst = self.getQuickVal(pg, ps)
                    if dst == const.CONT_EMPTY_VAL:
                        continue
                    if dst.id != src.id:
                        continue
                    if dst.overBear(amount):
                        continue
                    if not src.canMerge(src, dst):
                        continue
                    return (pg, ps)

        for pg in xrange(0, const.STORAGE_PAGE_NUM):
            ps = self.searchEmpty(pg)
            if ps != const.CONT_NO_POS:
                return (pg, ps)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def findItemByUUID(self, uuid):
        for pg in xrange(0, const.STORAGE_PAGE_NUM):
            posCount = min(self.getPosCount(pg), const.STORAGE_PAGE_SIZE)
            for ps in xrange(posCount):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.uuid == uuid:
                    return (it, pg, ps)

        return (const.CONT_EMPTY_VAL, const.CONT_NO_PAGE, const.CONT_NO_POS)

    def countBlankInPages(self):
        sum = 0
        for pg in self.getPageTuple():
            sum += self.countBlank(pg)

        return sum
