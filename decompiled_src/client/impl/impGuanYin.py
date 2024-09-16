#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impGuanYin.o
import const
import gamelog
import gameconfigCommon
from guanYin import GuanYinSlotVal, GuanYinBookVal, GuanYin
import gameglobal
from guis import uiConst
import guanYinInfo

class ImpGuanYin(object):

    def syncGuanYinInfo(self, guanYin):
        setattr(self, 'guanYin', guanYin)

    def _initGuanYin(self):
        if not hasattr(self, 'guanYin'):
            guanYin = GuanYin()
            if gameconfigCommon.enableGuanYinThirdPhase():
                self.guanYin.initGuanYinSlot(const.MAX_GUANYIN_SLOT_NUM)
                self.guanYin.initGuanYinBook(const.DEFAULT_GUANYIN_BOOK_NUM)
            setattr(self, 'guanYin', guanYin)

    def onUpdateGuanYinSlotVal(self, slotId, guanYin):
        gamelog.info('jbx:onUpdateGuanYinSlotVal', slotId, guanYin)
        self.guanYin[slotId] = guanYin
        gameglobal.rds.ui.guanYinV3.refreshInfo()

    def onUpdateGuanYinBookVal(self, bookId, superBookId, tExpired):
        gamelog.info('jbx:onUpdateGuanYinBookVal', bookId, superBookId, tExpired)
        if not self.guanYin.books.has_key(bookId):
            self.guanYin.books[bookId] = GuanYinBookVal(bookId)
        book = self.guanYin.books[bookId]
        book.guanYinSuperBookId = superBookId
        book.guanYinSuperPskillExpire = tExpired

    def onAddGuanYinPskillEx(self, page, pos, slot, part, bookId):
        gamelog.info('jbx:onAddGuanYinPskillEx', self, page, pos, slot, part, bookId)
        guanYinSlotVal = self.guanYin.get(slot)
        guanYinSlotVal.setGuanYinInfo(part, bookId)
        if guanYinSlotVal.guanYinStat < 0:
            guanYinSlotVal.updateGuanYinStat(part)
        gameglobal.rds.ui.guanYinV3.refreshInfo()
        gameglobal.rds.ui.guanYinV3.playAddSuccessEff(slot, bookId)

    def onRemoveGuanYinPskillEx(self, slot, part, bookId):
        gamelog.info('jbx:onRemoveGuanYinPskillEx', slot, part, bookId)
        guanYinSlotVal = self.guanYin.get(slot)
        guanYinSlotVal.guanYinInfo[part] = 0
        guanYinSlotVal.updateGuanYinStat(-1)
        self.guanYin.removeBook(bookId)
        gameglobal.rds.ui.guanYinV3.refreshInfo()
        gameglobal.rds.ui.guanYinV3.playRemoveSuccessEff(slot, bookId)

    def onAddGuanYinSuperPskillEx(self, page, pos, bookId):
        gamelog.info('jbx:onAddGuanYinSuperPskillEx', page, pos, bookId)
        gameglobal.rds.ui.guanYinV3.refreshInfo()
        gameglobal.rds.ui.guanYinV3.playAddSuccessEff(uiConst.SUPER_SKILL_SLOT_POS, bookId)

    def onAddGuanYinInAlternative(self, slot, bookId):
        gamelog.info('jbx:onAddGuanYinInAlternative', slot, bookId)
        self.subGuanYinInfo[slot] = bookId
        gameglobal.rds.ui.guanYinV3.refreshInfo()

    def onRemoveGuanYinInAlternative(self, slot, bookId):
        gamelog.info('jbx:onRemoveGuanYinInAlternative', slot, bookId)
        if self.subGuanYinInfo.has_key(slot):
            self.subGuanYinInfo.pop(slot)
        gameglobal.rds.ui.guanYinV3.refreshInfo()

    def onSwitchGuanYinSucc(self, guanYin, subGuanYin):
        gamelog.info('jbx:onSwitchGuanYinSucc', guanYin, subGuanYin)
        self.guanYin = guanYin
        self.subGuanYinInfo.clear()
        for k, v in subGuanYin.iteritems():
            self.subGuanYinInfo[k] = v

        gameglobal.rds.ui.guanYinV3.isSubMode = False
        gameglobal.rds.ui.guanYinV3.refreshInfo()
