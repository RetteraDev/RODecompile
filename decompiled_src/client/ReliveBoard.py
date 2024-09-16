#Embedded file name: I:/bag/tmp/tw2/res/entities\client/ReliveBoard.o
import BigWorld
import Math
import sMath
import const
import utils
import gametypes
from helpers import modelServer
from iClient import IClient
from iDisplay import IDisplay
from data import relive_board_data as RBD

class ReliveBoard(IClient, IDisplay):

    def __init__(self):
        super(ReliveBoard, self).__init__()
        self.isReliving = False
        self.reliveEndtime = 0

    def enterWorld(self):
        super(ReliveBoard, self).enterWorld()
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        self.filter = BigWorld.DumbFilter()
        radius = self.getRadius()
        self.trapId = BigWorld.addPot(self.matrix, radius, self._trapCallback)

    def getRadius(self):
        return RBD.data.get(self.rbType, {}).get('radius', 5)

    def getItemData(self):
        data = RBD.data.get(self.rbType, {})
        modelId = data.get('modelId', 0)
        scale = data.get('scale', 1.0)
        return {'model': modelId,
         'modelScale': scale}

    def afterModelFinish(self):
        super(ReliveBoard, self).afterModelFinish()
        self._checkReliveAction()
        self._updateName()

    def leaveWorld(self):
        super(ReliveBoard, self).leaveWorld()
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
            self._refreshOccupyItemIcon()
        else:
            p.hideOccupyItemIcon(self.id)

    def _refreshOccupyItemIcon(self):
        p = BigWorld.player()
        if self.canOccupy and self.tempCamp != p.getWorldWarCamp():
            p.showOccupyItemIcon(self.id)
        else:
            p.hideOccupyItemIcon(self.id)

    def createObstacleModel(self):
        modelId = self.getItemData().get('model')
        scale = self.getItemData().get('modelScale')
        if modelId:
            modelName = 'char/%d/%d.model' % (modelId, modelId)
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((scale, scale, scale))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if model:
            self.obstacleModel = model
            self.addModel(model)
            model.setEntity(self.id)
            self._updateName()

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

    def set_tempCamp(self, old):
        self._updateName()
        self._refreshOccupyItemIcon()

    def set_roleName(self, old):
        self._updateName(self.roleName)

    def _updateName(self, name = None):
        if not name:
            name = self._getName()
        if self.topLogo.__class__.__name__ != 'TopLogo':
            return
        self.topLogo.name = name
        self.topLogo.updateRoleName(self.topLogo.name)

    def _getName(self):
        if self.roleName:
            return self.roleName
        if BigWorld.player().inWorldWarEx():
            if self.tempCamp == gametypes.WORLD_WAR_CAMP_ATTACK:
                return 'π•∑Ω∏¥ªÓ’Û'
            else:
                return ' ÿ∑Ω∏¥ªÓ’Û'
        return '∏¥ªÓ’Û'
