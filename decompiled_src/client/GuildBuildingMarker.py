#Embedded file name: I:/bag/tmp/tw2/res/entities\client/GuildBuildingMarker.o
import BigWorld
import const
import commQuest
import gameglobal
import utils
import sMath
from iClient import IClient
from iDisplay import IDisplay
from helpers import fashion
from helpers import modelServer
from helpers import ufo
from sfx import sfx
from data import npc_model_client_data as NMCD
from data import quest_marker_data as QMD
from data import sys_config_data as SCD
from data import guild_building_marker_data as GBMD

class GuildBuildingMarker(IClient, IDisplay):

    def __init__(self):
        super(GuildBuildingMarker, self).__init__()
        self.forceVisibility = None
        self.noSelected = True
        self.buildingId = GBMD.data.get(self.markerId).get('buildingId')

    def enterWorld(self):
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.initYaw = self.yaw
        self.modelServer = modelServer.SimpleModelServer(self)
        radius = self.getRadius()
        self.trapId = BigWorld.addPot(self.matrix, radius, self.trapCallback)

    def leaveWorld(self):
        if hasattr(self, 'modelServer') and self.modelServer:
            self.modelServer.release()
            self.modelServer = None
        if self.fashion != None:
            self.fashion.attachUFO(ufo.UFO_NULL)
            self.fashion.release()
            self.fashion = None
        if self.topLogo != None:
            self.topLogo.release()
            self.topLogo = utils.MyNone
        self.removeAllFx()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        p = BigWorld.player()
        if sMath.distance2D(p.position, self.position) < self.getRadius() or gameglobal.rds.ui.pressKeyF.guildBuildingMarkerId == self.id:
            p.hideItemIconNearGuildBuildingMarker(self.id)

    def afterModelFinish(self):
        super(GuildBuildingMarker, self).afterModelFinish()
        nmcd = NMCD.data.get(self.npcId, {})
        effScale = nmcd['effScale'] if nmcd.has_key('effScale') else nmcd.get('modelScale', 1)
        fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (gameglobal.EFFECT_LOW,
         self.getBasicEffectPriority(),
         self.model,
         nmcd['triggerEff'],
         sfx.EFFECT_UNLIMIT))
        if fxs:
            for fx in fxs:
                fx.scale(effScale, effScale, effScale)

            self.addFx(nmcd['triggerEff'], fxs)
        self.forceVisibility = self.visibility
        self.refreshVisibility()

    def getItemData(self):
        nd = NMCD.data.get(self.npcId, {})
        modelId = nd.get('model', 0)
        if not nd or not modelId:
            return {'model': gameglobal.defaultModelID,
             'dye': 'Default'}
        return nd

    def getRadius(self):
        qmd = QMD.data[self.npcId]
        return qmd.get('scope', 5)

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if self.visibility == const.VISIBILITY_HIDE:
            return
        p = BigWorld.player()
        if p.position.y - self.position.y > SCD.data.get('trapHeight', 5):
            return
        if enteredTrap:
            if p.guildNUID and p.guildNUID == self.guildNUID:
                itemId = commQuest.getPropItemId(self.npcId)
                p.showItemIconNearGuildBuildingMarker(self.id, itemId)
        else:
            p.hideItemIconNearGuildBuildingMarker(self.id)
            gameglobal.rds.ui.guildBuildUpgrade.hideByMarkerIdAndNpcId(self.markerId, self.id)

    def set_inClanWar(self, old):
        self.refreshVisibility()

    def set_visibility(self, old):
        self.forceVisibility = self.visibility
        self.refreshVisibility(old)

    def set_guildNUID(self, old):
        self.refreshVisibility()

    def set_clanNUID(self, old):
        self.refreshVisibility()

    def refreshVisibility(self, old = None):
        p = BigWorld.player()
        if old == None:
            old = self.visibility
        if self.forceVisibility == const.VISIBILITY_HIDE or p.guildNUID != self.guildNUID:
            self.visibility = const.VISIBILITY_HIDE
        else:
            self.visibility = const.VISIBILITY_SHOW
        super(GuildBuildingMarker, self).set_visibility(old)
        self._refreshVisibility()

    def _refreshVisibility(self):
        p = BigWorld.player()
        if p.position.y - self.position.y > SCD.data.get('trapHeight', 10):
            return
        radius = self.getRadius()
        if sMath.distance2D(p.position, self.position) > radius:
            return
        if self.visibility == const.VISIBILITY_HIDE:
            p.hideItemIconNearGuildBuildingMarker(self.id)
        else:
            itemId = commQuest.getPropItemId(self.npcId)
            p.showItemIconNearGuildBuildingMarker(self.id, itemId)

    def canOutline(self):
        return False

    def set_devState(self, old):
        pass
