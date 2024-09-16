#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impRoundTable.o
import gameglobal
from guis import events
from helpers.eventDispatcher import Event as UIEvent

class ImpRoundTable(object):

    def onApplyForRoundTable(self, srcEntId):
        applyEvent = UIEvent(events.EVENT_RT_APPLY, {'srcEntId': srcEntId})
        gameglobal.rds.ui.dispatchEvent(applyEvent)

    def onLeaveRoundTable(self):
        gameglobal.rds.ui.dispatchEvent(events.EVENT_RT_LEAVE)

    def onJoinRoundTable(self, entId):
        self.belongToRoundTable = entId
        gameglobal.rds.ui.dispatchEvent(events.EVENT_RT_JOINED)

    def onRoundTableSeatNumChanged(self, changeNum, entIds):
        pass

    def onRoundTableEnd(self, seats, itemId = 319000):
        data = {'seats': seats,
         'itemId': itemId}
        endEvent = UIEvent(events.EVENT_RT_END, data)
        gameglobal.rds.ui.dispatchEvent(endEvent)
