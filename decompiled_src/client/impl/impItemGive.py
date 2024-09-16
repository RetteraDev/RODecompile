#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impItemGive.o
import gamelog
import gameglobal

class ImpItemGive(object):

    def onItemGiveRequest(self, peerID):
        gamelog.debug('kjianjun,onItemGiveRequest', peerID)
        gameglobal.rds.ui.bindItemTrade.onItemGiveRequest(peerID)

    def onItemGiveStart(self, peerID):
        gamelog.debug('kjianjun,onItemGiveStart', peerID)
        gameglobal.rds.ui.bindItemTrade.onItemGiveStart(peerID)

    def onItemAcceptStart(self, peerID):
        gamelog.debug('kjianjun,onItemAcceptStart', peerID)
        gameglobal.rds.ui.bindItemTrade.onItemAcceptStart(peerID)

    def onGiveItem(self, pos, item, serial):
        gamelog.debug('kjianjun,onItemGive', pos, item, serial)
        gameglobal.rds.ui.bindItemTrade.onItemGive(pos, item, serial)

    def onGiveItemRevert(self, pos, serial):
        gamelog.debug('kjianjun,onItemGiveRevert', pos, serial)
        gameglobal.rds.ui.bindItemTrade.onGiveItemRevert(pos, serial)

    def onItemGiven(self, pos, item, serial):
        gamelog.debug('kjianjun,onItemGiven', pos, item, serial)
        gameglobal.rds.ui.bindItemTrade.onItemGiven(pos, item, serial)

    def onItemGiveCancel(self):
        gamelog.debug('kjianjun,onItemGiveCancel')
        gameglobal.rds.ui.bindItemTrade.onItemGiveCancel()

    def onItemGiveFinal(self):
        gamelog.debug('kjianjun,onItemGiveFinal')
        gameglobal.rds.ui.bindItemTrade.onItemGiveFinal()

    def onItemGiveItemFinish(self, itemIds):
        gamelog.debug('kjianjun,onItemGiveItemFinish')
        gameglobal.rds.ui.bindItemTrade.onItemGiveItemFinish()

    def onItemGiveFinish(self):
        gamelog.debug('kjianjun,onItemGiveFinish')
        gameglobal.rds.ui.bindItemTrade.onItemGiveFinish()
