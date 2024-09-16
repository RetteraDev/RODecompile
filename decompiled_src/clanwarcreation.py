#Embedded file name: /WORKSPACE/data/entities/client/clanwarcreation.o
import copy
import BigWorld
import Math
import const
import gametypes
import gameglobal
import sMath
from item import Item
from iClanWarCreation import IClanWarCreation
from data import clan_war_stone_data as CWSD
from Monster import Monster

class ClanWarCreation(Monster, IClanWarCreation):
    IsMonster = False
    IsClanWarUnit = True

    def __init__(self):
        super(ClanWarCreation, self).__init__()
        self.applyTints = []

    def chooseItem(self):
        if self.buildingType == gametypes.CLAN_WAR_BUILDING_STONE:
            p = BigWorld.player()
            if p._isSoul():
                gameglobal.rds.ui.crossServerBag.show()
            else:
                gameglobal.rds.ui.inventory.show(True)
                gameglobal.rds.ui.inventory.setFilterBySubtype(Item.SUBTYPE_2_CLAN_WAR_STONE_CORE)

    def getItemData(self):
        itemData = getattr(self, 'itemData', None)
        if itemData:
            return itemData
        md = copy.deepcopy(super(ClanWarCreation, self).getItemData())
        data = CWSD.data.get(self.buildingId, {})
        modelId = data.get('modelId')
        modelScale = data.get('scale')
        if modelId:
            md['model'] = modelId
        if modelScale:
            md['modelScale'] = modelScale
        self.itemData = md
        return md

    def afterModelFinish(self):
        super(ClanWarCreation, self).afterModelFinish()
        self.createObstacleModel()

    def getModelScale(self):
        data = CWSD.data.get(self.buildingId, {})
        scale = data.get('scale', 1.0)
        sv = (scale, scale, scale)
        self.model.scale = sv
        return sv

    def createObstacleModel(self):
        data = CWSD.data.get(self.buildingId, {})
        modelId = data.get('obstacleModel')
        if modelId:
            modelName = 'char/%d/%d.model' % (modelId, modelId)
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((1, 1, 1))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if not self.inWorld:
            return
        if model:
            model.setCollide(True)
            model.setPicker(True)
            self.obstacleModel = model
            self.addModel(model)
            IClanWarCreation.checkCollideWithPlayer(self)

    def getRadius(self):
        return CWSD.data.get(self.buildingId, {}).get('radius', 5)

    def enterWorld(self):
        super(ClanWarCreation, self).enterWorld()
        radius = self.getRadius()
        self.trapId = BigWorld.addPot(self.matrix, radius, self._trapCallback)

    def leaveWorld(self):
        super(ClanWarCreation, self).leaveWorld()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        p = BigWorld.player()
        if sMath.distance2D(p.position, self.position) < self.getRadius() or gameglobal.rds.ui.pressKeyF.clanWarCreationId == self.id:
            p.hideItemIconNearClanWarCreation(self.id)

    def _trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        if enteredTrap:
            if self.inClanWar and not self.coreFull and p.guildNUID and p.guildNUID == self.guildNUID:
                p.showItemIconNearClanWarCreation(self.id, const.CLAN_WAR_STONE_CORE_ICON)
        else:
            p.hideItemIconNearClanWarCreation(self.id)

    def set_coreFull(self, old):
        p = BigWorld.player()
        if self.coreFull:
            p.hideItemIconNearClanWarCreation(self.id)

    def needAttachUFO(self):
        return False

    def canOutline(self):
        return False
