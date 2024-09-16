#Embedded file name: I:/bag/tmp/tw2/res/entities\client/ClanWarReliveBoard.o
import copy
import BigWorld
import Math
import const
import sMath
import utils
import gameglobal
import gametypes
from Monster import Monster
from iClanWarCreation import IClanWarCreation
from data import clan_war_relive_board_data as CWRBD

class ClanWarReliveBoard(Monster, IClanWarCreation):
    IsMonster = False
    IsClanWarUnit = True

    def __init__(self):
        super(ClanWarReliveBoard, self).__init__()
        self.applyTints = []
        self.isReliving = False
        self.reliveEndtime = 0

    def getRadius(self):
        return CWRBD.data.get(self.buildingId, {}).get('radius', 5)

    def enterWorld(self):
        super(ClanWarReliveBoard, self).enterWorld()
        radius = self.getRadius()
        self.trapId = BigWorld.addPot(self.matrix, radius, self._trapCallback)

    def afterModelFinish(self):
        super(ClanWarReliveBoard, self).afterModelFinish()
        self._checkReliveAction()

    def leaveWorld(self):
        super(ClanWarReliveBoard, self).leaveWorld()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        p = BigWorld.player()
        if sMath.distance2D(p.position, self.position) < self.getRadius():
            BigWorld.player().hideDestroyableItemIcon(self.id)

    def _trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        if enteredTrap:
            if (gameglobal.rds.ui.guild.checkAuthorization(gametypes.GUILD_ACTION_DESTROY_CLAN_WAR_BUILDING, False) or p.gbId == self.creatorGbId) and p.guildNUID == self.guildNUID:
                p.showDestroyableItemIcon(self.id)
        else:
            p.hideDestroyableItemIcon(self.id)

    def getItemData(self):
        itemData = getattr(self, 'itemData', None)
        if itemData:
            return itemData
        md = copy.deepcopy(super(ClanWarReliveBoard, self).getItemData())
        modelId = CWRBD.data.get(self.buildingId, {}).get('modelId')
        if modelId:
            md['model'] = modelId
        self.itemData = itemData
        return md

    def createObstacleModel(self):
        data = CWRBD.data.get(self.buildingId, {})
        modelId = data.get('obstacleModel')
        if modelId:
            modelName = 'char/%d/%d.model' % (modelId, modelId)
            scaleMatrix = Math.Matrix()
            scale = data.get('scale', 1.0)
            scaleMatrix.setScale((scale, scale, scale))
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

    def onRelive(self, reliveInterval):
        self.reliveEndtime = utils.getNow() + reliveInterval
        self._checkReliveAction()

    def _checkReliveAction(self):
        if self.reliveEndtime > utils.getNow() and not self.isReliving and self.fashion:
            self.isReliving = True
            self.fashion.playSingleAction(const.CLAN_WAR_RELIVE_BOARD_ACTION, callback=self._onReliveActionFinished)

    def _onReliveActionFinished(self):
        if self.reliveEndtime > utils.getNow():
            self.fashion.playSingleAction(const.CLAN_WAR_RELIVE_BOARD_ACTION, callback=self._onReliveActionFinished)
        else:
            self.isReliving = False

    def needAttachUFO(self):
        return False

    def canOutline(self):
        return False

    def set_roleName(self, old):
        if self.topLogo.__class__.__name__ != 'TopLogo':
            return
        self.topLogo.name = self.roleName
        self.refreshStateUI()
