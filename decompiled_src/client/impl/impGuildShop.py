#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impGuildShop.o
import BigWorld
import gameglobal

class ImpGuildShop(object):

    def _checkGuildShopVer(self, ver, shopType):
        if ver < self.guild.getShop(shopType).version:
            return False
        self.guild.getShop(shopType).version = ver
        return True

    def onGuildShopPosCountUpdated(self, shopType, posCountDict):
        if not self.guild:
            return
        self.guild.getShop(shopType).posCountDict = posCountDict

    def onGuildShopResRemove(self, stamp, shopType, page, pos):
        if not self.guild:
            return
        shop = self.guild.getShop(shopType)
        shop.stamp[page] = stamp
        shop.removeObj(page, pos)

    def onGuildShopResWrap(self, stamp, shopType, amount, page, pos):
        if not self.guild:
            return
        shop = self.guild.getShop(shopType)
        shop.stamp[page] = stamp
        it = shop.getQuickVal(page, pos)
        it.cwrap = amount
        gameglobal.rds.ui.guild.refreshMemberInfo()

    def onGuildShopRefresh(self, stamp, shopType, data):
        if not self.guild:
            return
        self.guild.updateShop(data)
        p = BigWorld.player()
        shop = p.guild.shop[shopType - 1]
        shop.stamp = stamp

    def onGuildShopBuyRecordUpdate(self, shopType, itemId, amount):
        if not self.guild:
            return
        shop = self.guild.getShop(shopType)
        shop.buyRecord[itemId] = amount
