#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/storageGuild.o
import const
from storageCommon import StorageCommon
from item import Item
import gametypes
from data import item_data as ID

class StorageGuild(StorageCommon):

    def __init__(self, pageCount = const.GUILD_STORAGE_PAGE_NUM, width = const.GUILD_STORAGE_WIDTH, height = const.GUILD_STORAGE_HEIGHT):
        super(StorageGuild, self).__init__(pageCount, width, height)
        self.stamp = [0] * pageCount

    def searchEmptyInPages(self):
        for pg in xrange(0, const.GUILD_STORAGE_PAGE_NUM):
            dstPos = self.searchEmpty(pg)
            if dstPos != const.CONT_NO_POS:
                return (pg, dstPos)

        return (const.CONT_NO_PAGE, const.CONT_NO_POS)

    def searchBestInGuildStorage(self, id, amount, pg):
        if id not in ID.data or amount > ID.data[id].get('mwrap', 1):
            return const.CONT_NO_POS
        src = Item(id, cwrap=amount, genRandProp=False)
        if src.canWrap():
            posCount = min(self.getPosCount(pg), const.GUILD_STORAGE_PAGE_SIZE)
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
                if hasattr(dst, 'gatype'):
                    if dst.gatype == gametypes.GUILD_STORAGE_ASSIGN_TYPE_MEMBER or dst.gatype == gametypes.GUILD_STORAGE_ASSIGN_TYPE_ALL:
                        continue
                    elif dst.gatype == gametypes.GUILD_STORAGE_ASSIGN_TYPE_ADMIN:
                        pass
                return ps

        ps = self.searchEmpty(pg)
        if ps != const.CONT_NO_POS:
            return ps
        return const.CONT_NO_POS

    def findItemByUUID(self, uuid):
        for pg in xrange(0, const.GUILD_STORAGE_PAGE_NUM):
            posCount = min(self.getPosCount(pg), const.GUILD_STORAGE_PAGE_SIZE)
            for ps in xrange(posCount):
                it = self.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.uuid == uuid:
                    return (it, pg, ps)

        return (const.CONT_EMPTY_VAL, const.CONT_NO_PAGE, const.CONT_NO_POS)
