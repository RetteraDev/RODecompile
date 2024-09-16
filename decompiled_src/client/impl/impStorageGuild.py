#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impStorageGuild.o
import cPickle
import zlib
import BigWorld
import const
import gameglobal
import gametypes
from helpers.storageGuild import StorageGuild

class ImpStorageGuild(object):

    def _checkStorageGuildVer(self, ver):
        if ver < self.guild.storage.version:
            return False
        self.guild.storage.version = ver
        return True

    def onGuildStoragePosCountUpdated(self, posCountDict):
        if not self.guild:
            return
        self.guild.storage.posCountDict = posCountDict

    def onStorageGuildResMove(self, srcStamp, srcPage, srcPos, dstStamp, dstPage, dstPos):
        if not self.guild:
            return
        storage = self.guild.storage
        storage.stamp[srcPage] = srcStamp
        storage.stamp[dstPage] = dstStamp
        srcIt = storage.getQuickVal(srcPage, srcPos)
        storage.removeObj(srcPage, srcPos)
        storage.insertObj(srcIt, dstPage, dstPos)
        gameglobal.rds.ui.guildStorage.removeItem(srcPage, srcPos)
        gameglobal.rds.ui.guildStorage.addItem(srcIt, dstPage, dstPos)

    def onStorageGuildResRemove(self, stamp, page, pos):
        if not self.guild:
            return
        storage = self.guild.storage
        storage.stamp[page] = stamp
        storage.removeObj(page, pos)
        gameglobal.rds.ui.guildStorage.removeItem(page, pos)

    def onStorageGuildResInsert(self, stamp, item, page, pos):
        if not self.guild:
            return
        storage = self.guild.storage
        storage.stamp[page] = stamp
        storage.insertObj(item, page, pos)
        gameglobal.rds.ui.guildStorage.addItem(item, page, pos)

    def onStorageGuildResWrap(self, stamp, amount, page, pos):
        if not self.guild:
            return
        storage = self.guild.storage
        storage.stamp[page] = stamp
        item = storage.getQuickVal(page, pos)
        storage.shiftObj(page, pos, amount)
        gameglobal.rds.ui.guildStorage.addItem(item, page, pos)

    def onStorageGuildAssign(self, stamp, page, pos, assignType, toGbId, toRole):
        if not self.guild:
            return
        storage = self.guild.storage
        storage.stamp[page] = stamp
        it = storage.getQuickVal(page, pos)
        if it != const.CONT_EMPTY_VAL:
            it.gatype = assignType
            it.toGbId = toGbId
            it.toRole = toRole
        p = BigWorld.player()
        gameglobal.rds.ui.guildStorage.setAssginFlag(page, pos, gametypes.GUILD_STORAGE_ASSIGN_TYPE_ADMIN)
        if hasattr(it, 'gatype'):
            if it.gatype == gametypes.GUILD_STORAGE_ASSIGN_TYPE_MEMBER and it.toGbId == p.gbId:
                gameglobal.rds.ui.guildStorage.setAssginFlag(page, pos, gametypes.GUILD_STORAGE_ASSIGN_TYPE_MEMBER)
            elif it.gatype == gametypes.GUILD_STORAGE_ASSIGN_TYPE_ALL:
                gameglobal.rds.ui.guildStorage.setAssginFlag(page, pos, gametypes.GUILD_STORAGE_ASSIGN_TYPE_ALL)
            elif it.gatype == gametypes.GUILD_STORAGE_ASSIGN_TYPE_ADMIN:
                gameglobal.rds.ui.guildStorage.setAssginFlag(page, pos, gametypes.GUILD_STORAGE_ASSIGN_TYPE_ADMIN)

    def onStorageGuildResExchange(self, srcStamp, srcPage, srcPos, dstStamp, dstPage, dstPos):
        if not self.guild:
            return
        storage = self.guild.storage
        storage.stamp[srcPage] = srcStamp
        storage.stamp[dstPage] = dstStamp
        srcIt = storage.getQuickVal(srcPage, srcPos)
        dstIt = storage.getQuickVal(dstPage, dstPos)
        if srcIt == const.CONT_EMPTY_VAL or dstIt == const.CONT_EMPTY_VAL:
            return
        storage.insertObj(dstIt, srcPage, srcPos)
        storage.insertObj(srcIt, dstPage, dstPos)
        gameglobal.rds.ui.guildStorage.removeItem(srcPage, srcPos)
        gameglobal.rds.ui.guildStorage.removeItem(dstPage, dstPos)
        gameglobal.rds.ui.guildStorage.addItem(srcIt, dstPage, dstPos)
        gameglobal.rds.ui.guildStorage.addItem(dstIt, srcPage, srcPos)

    def onStorageGuildSort(self, stamp, data):
        if not self.guild:
            return
        data = cPickle.loads(zlib.decompress(data))
        storage = self.guild.storage
        self.guild.storage = StorageGuild()
        self.guild.storage.posCountDict = storage.posCountDict
        self.guild.storage.stamp = stamp
        storage = self.guild.storage
        for pg, ps, it in data:
            storage.insertObj(it, pg, ps)

        gameglobal.rds.ui.guildStorage.refresh()
