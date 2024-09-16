#Embedded file name: /WORKSPACE/data/entities/client/clienttransport.o
import BigWorld
import gametypes
import utils
import formula
import iClientOnly
from data import client_building_proxy_data as CBPD

class ClientTransport(iClientOnly.IClientOnly):

    def __init__(self):
        super(ClientTransport, self).__init__()
        self.trapId = None

    def __getattr__(self, name):
        if not self.inWorld:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)
        try:
            return self.__dict__['attrs'][name]
        except KeyError:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)

    def enterWorld(self):
        super(ClientTransport, self).enterWorld()
        self.setupFilter()
        cbpd = CBPD.data.get(self.cid, {})
        potType = cbpd.get('potType', None)
        if not potType:
            return
        if potType == 1:
            self.trapId = BigWorld.addPot(self.matrix, self.radii, self.trapCallback)
        elif potType == 2:
            self.trapId = BigWorld.addRectPot(self.matrix, self.width, self.length, self.trapCallback)

    def showDebugInfo(self):
        cbpd = CBPD.data.get(self.cid, {})
        potType = cbpd.get('potType', None)
        if not potType:
            return
        if potType == 1:
            BigWorld.player().showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_CYLINDER,
             self.position,
             self.radii,
             2,
             2))
        elif potType == 2:
            pos = utils.getRelativePosition(self.position, self.yaw, 0, -self.length)
            BigWorld.player().showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_CUBE,
             self.position,
             pos,
             self.width,
             self.length * 2,
             2,
             self.yaw))

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        if enteredTrap:
            if not self.trapConditionCheck():
                return
            p.enterClientTransportPot(self.cid)
        else:
            p.leaveClientTransportPot(self.cid)

    def trapConditionCheck(self):
        p = BigWorld.player()
        if not p:
            return False
        cbpd = CBPD.data.get(self.cid, {})
        if utils.getEnableCheckServerConfig():
            serverConfigId = cbpd.get('serverConfigId', 0)
            if serverConfigId and not utils.checkInCorrectServer(serverConfigId):
                return False
        if cbpd.has_key('spaceNo') and p.spaceNo != cbpd['spaceNo']:
            return False
        if cbpd.has_key('needHeader') and p.groupHeader != p.id:
            return False
        if cbpd.has_key('checkFbNo') and formula.inExcludeFubenList(cbpd['checkFbNo'], p.fbStatusList):
            return False
        if cbpd.has_key('needAcceptQuests') and not any([ qid in p.quests for qid in cbpd['needAcceptQuests'] ]):
            return False
        if cbpd.has_key('startTimes') and cbpd.has_key('endTimes') and not utils.inTimeTuplesRange(cbpd['startTimes'], cbpd['endTimes']):
            return False
        return True

    def loadImmediately(self):
        return True

    def setupFilter(self):
        self.filter = BigWorld.ClientFilter()
        applyDrop = True
        if getattr(self, 'noDrop', False):
            applyDrop = False
        self.filter.applyDrop = applyDrop
        self.filter.position = self.position

    def leaveWorld(self):
        super(ClientTransport, self).leaveWorld()
        if getattr(self, 'trapId', None):
            BigWorld.delPot(self.trapId)
            self.trapId = None
