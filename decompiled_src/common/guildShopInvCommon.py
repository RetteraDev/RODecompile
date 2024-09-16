#Embedded file name: I:/bag/tmp/tw2/res/entities\common/guildShopInvCommon.o
import const
from container import Container

class GuildShopInvCommon(Container):

    def __init__(self, pageCount = const.SHOP_PAGE_NUM, width = const.SHOP_WIDTH, height = const.SHOP_HEIGHT):
        super(GuildShopInvCommon, self).__init__(pageCount, width, height)
        self.posCountDict = {}
        self.stamp = [1] * pageCount

    def getPosTuple(self, page):
        if not self._isValidPage(page):
            return ()
        return range(self.getPosCount(page))

    def getPosCount(self, page):
        return self.posCountDict.get(page, 0)

    def cleanPages(self):
        for pg in self.getPageTuple():
            self.cleanPage(pg)
