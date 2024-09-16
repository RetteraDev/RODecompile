#Embedded file name: I:/bag/tmp/tw2/res/entities\client/RoundTable.o
import BigWorld
import gameglobal
import utils
import const
from guis import events
from iNpc import INpc
from iDisplay import IDisplay
from helpers.eventDispatcher import Event as UIEvent
from data import round_table_data as RTD

class RoundTable(INpc, IDisplay):

    def __init__(self):
        super(RoundTable, self).__init__()
        self.isLeaveWorld = False
        self.data = {'model': self.modelId,
         'dye': 'Default'}
        self.data.update(RTD.data.get(self.itemId, {}))

    def getItemData(self):
        return self.data

    def set_seats(self, old):
        gameglobal.rds.ui.dispatchEvent(events.EVENT_RT_SEAT_CHAGED)
        self.refreshSeats()

    def set_tableType(self, old):
        pass

    def use(self):
        gameglobal.rds.ui.roundTable.openRoundTableByEntity(self.id)

    def enterWorld(self):
        super(RoundTable, self).enterWorld()
        self.trapId = BigWorld.addPot(self.matrix, const.NPC_USE_DIST, self.trapCallback)

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        if enteredTrap:
            applyEvent = UIEvent(events.EVENT_RT_SEAT_CREATED, {'tableType': self.tableType})
            gameglobal.rds.ui.dispatchEvent(applyEvent)
            p.roundTableTrapCallback((self,))
        else:
            p.roundTableTrapCallback([])

    def getRoundTableIdx(self, ent):
        if not ent or not ent.inWorld:
            return -1
        if ent.gbId not in self.seats:
            return -1
        data = self.seats.get(ent.gbId)
        if not data:
            return -1
        return self.seats.get(ent.gbId)[1]

    def afterModelFinish(self):
        super(RoundTable, self).afterModelFinish()
        self.refreshSeats()
        self.filter = BigWorld.DumbFilter()
        self.createExtraObstacleModel()

    def refreshSeats(self):
        if self.seats:
            for gbId, (entId, seatIdx, joinTime, offlineTime, roleName) in self.seats.iteritems():
                ent = BigWorld.entities.get(entId)
                if not ent or not ent.inWorld:
                    return
                ent.modelServer.enterRoundTable()

    def leaveWorld(self):
        if self.seats:
            try:
                for gbId, (entId, seatIdx, joinTime, offlineTime, roleName) in self.seats.iteritems():
                    cleanList = []
                    seatNode = utils.getRoundTableSeatNodeName(seatIdx)
                    for item in self.model.node(seatNode).attachments:
                        cleanList.append(item)

                    for item in cleanList:
                        self.model.node(seatNode).detach(item)

            except:
                pass

        super(RoundTable, self).leaveWorld()
        self.isLeaveWorld = True
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        self.trapCallback(False, None)
