#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerBooth.o
from gamestrings import gameStrings
import cPickle
import zlib
import BigWorld
import const
import gameglobal
import utils
from guis import uiConst
from item import Item
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class ImpPlayerBooth(object):

    def addBoothRecord(self, roleName):
        self.__dict__.setdefault('boothRecord', set([])).add(roleName)

    def queryBoothRecord(self, roleName):
        return roleName in getattr(self, 'boothRecord', set([]))

    def clearBoothRecord(self):
        self.__dict__.setdefault('boothRecord', set([])).clear()

    def addBoothMark(self, roleName):
        bm = self.__dict__.setdefault('boothMark', set([]))
        if roleName in bm:
            bm.discard(roleName)
        else:
            bm.add(roleName)

    def queryBoothMark(self, roleName):
        return roleName in getattr(self, 'boothMark', set([]))

    def set_boothAspect(self, old):
        pass

    def boothSetup(self, info):
        gameglobal.rds.ui.booth.show()
        BigWorld.target.exclude = None
        itemOps, buyItems = cPickle.loads(zlib.decompress(info))
        for bMove, invPage, invPos, invMany, boothPage, boothPos, price in itemOps:
            if bMove:
                self.resMove(const.RES_KIND_INV, invPage, invPos, const.RES_KIND_BOOTH, boothPage, boothPos)
            else:
                self.resMovePart(const.RES_KIND_INV, invPage, invPos, invMany, const.RES_KIND_BOOTH, boothPage, boothPos)
            self.resPrice(const.RES_KIND_BOOTH, boothPage, boothPos, price)

        for boothPage, boothPos, itemId, cwrap, price in buyItems:
            it = Item(itemId, cwrap)
            it.canOverMax = True
            it.remainNum = cwrap
            it.cwrap = cwrap
            self.resInsert(const.RES_KIND_BOOTH, it, boothPage, boothPos)
            self.resPrice(const.RES_KIND_BOOTH, boothPage, boothPos, price)

        gameglobal.rds.ui.actionbar.setRideShine(True, uiConst.BOOTH)

    def boothShutup(self):
        self.boothBuyItemCleared()
        gameglobal.rds.ui.booth.hide()
        BigWorld.target.exclude = self
        gameglobal.rds.ui.booth.ownerLogs = []
        gameglobal.rds.ui.actionbar.setRideShine(False, uiConst.BOOTH)

    def boothOpen(self, b):
        pass

    def set_boothStat(self, old):
        super(self.__class__, self).set_boothStat(old)
        gameglobal.rds.ui.buffSkill.refreshVisible()

    def set_boothName(self, old):
        gameglobal.rds.ui.booth.setBoothName(self.boothName)
        self.topLogo.setBoothName(self.boothName)

    def boothSemiData(self, ownerID, serial, itemInfo, buyItemsInfo):
        gameglobal.rds.ui.booth.show(False, (ownerID,
         serial,
         itemInfo,
         buyItemsInfo))
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def boothFullData(self, ownerID, page, pos, item):
        pass

    def boothLog(self, log):
        logs = gameglobal.rds.ui.booth.ownerLogs
        if len(logs) >= const.BOOTH_LOGS_MANY:
            logs.pop(0)
        logs.append(log)
        gameglobal.rds.ui.booth.setRecord(logs)
        gameglobal.rds.sound.playSound(gameglobal.SD_26)

    def boothLogs(self, ownerID, info):
        logs = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.booth.setRecord(logs)
        gameglobal.rds.sound.playSound(gameglobal.SD_26)
        if ownerID == self.id and not logs:
            gameglobal.rds.ui.booth.ownerLogs = []

    def boothWord(self, ownerID, info):
        word = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.booth.setMessage(word)

    def boothWordIntervalShort(self, ownerID):
        word = gameglobal.rds.ui.booth.word or []
        word.append((gameStrings.TEXT_BOOTHPROXY_694, GMD.data.get(GMDD.data.CHAT_INTERVAL_SHORT)['text'], utils.getNow()))
        gameglobal.rds.ui.booth.setMessage(word)

    def boothWordAndLogs(self, ownerID, info):
        info = cPickle.loads(zlib.decompress(info))
        word, logs = info
        gameglobal.rds.ui.booth.showBoothRecord(word, logs)

    def boothBuyItemCleared(self):
        for pg in const.BOOTH_CLIENT_PAGE_BUY.itervalues():
            for ps in xrange(self.booth.posCount):
                it = self.booth.getQuickVal(pg, ps)
                if it != const.CONT_EMPTY_VAL:
                    self.resRemove(const.RES_KIND_BOOTH, pg, ps)

    def inBooth(self):
        return self.boothStat == const.BOOTH_STAT_OPEN
