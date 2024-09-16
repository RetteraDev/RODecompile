#Embedded file name: I:/bag/tmp/tw2/res/entities\client/BattleFieldFlag.o
import BigWorld
import Math
import gamelog
import gameglobal
import gametypes
from helpers import modelServer
from helpers import tintalt
from guis import ui
from guis import cursor
from iClient import IClient
from data import battle_field_flag_data as BFFD
from data import duel_config_data as DCD
from cdata import game_msg_def_data as GMDD

class BattleFieldFlag(IClient):

    def __init__(self):
        super(BattleFieldFlag, self).__init__()
        self.roleName = ''

    def enterWorld(self):
        super(BattleFieldFlag, self).enterWorld()
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        self.filter = BigWorld.DumbFilter()
        maxHoldFlagDist = DCD.data.get('maxHoldFlagDist', 3)
        self.trapId = BigWorld.addPot(self.matrix, maxHoldFlagDist, self.trapCallback)

    def afterModelFinish(self):
        super(BattleFieldFlag, self).afterModelFinish()
        self.model.setModelNeedHide(0, 0.5)
        self.setTargetCapsUse(True)
        self.createObstacleModel()
        self.filter = BigWorld.DumbFilter()
        tintalt.ta_set_static([self.model], self.genTintStr())

    def getSeekDist(self):
        return DCD.data.get('maxHoldFlagDist', 3)

    def showTargetUnitFrame(self):
        return False

    def getFKey(self):
        return BFFD.data.get(self.flagId, {}).get('fKeyId', 161)

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        if enteredTrap:
            p.battleFieldFlagTrapCallback((self,))
        else:
            p.battleFieldFlagTrapCallback([])

    def createObstacleModel(self):
        modelId = BFFD.data.get(self.flagId, {}).get('obstacleModel', 0)
        scale = BFFD.data.get(self.flagId, {}).get('obstacleScale', 0.9)
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
            model.setCollide(True)

    def leaveWorld(self):
        super(BattleFieldFlag, self).leaveWorld()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
            if gameglobal.rds.ui.pressKeyF.battleFieldFlag and gameglobal.rds.ui.pressKeyF.battleFieldFlag.id == self.id:
                BigWorld.player().battleFieldFlagTrapCallback(())

    def getItemData(self):
        modelId = BFFD.data.get(self.flagId, {}).get('modelId', 60000)
        return {'model': modelId,
         'modelScale': 1}

    def use(self):
        p = BigWorld.player()
        if self.camp == p.tempCamp:
            p.showGameMsg(GMDD.data.BATTLE_FIELD_HOLD_FLAG_FAILED_DUPLICATE, ())
            return
        if self.isOccupied:
            p.showGameMsg(GMDD.data.BATTLE_FIELD_HOLD_FLAG_FAILED_OCCUPIED, ())
            return
        p.cell.clickBattleFieldFlag(self.id)

    def set_camp(self, old):
        gamelog.debug('@hjx flag#set_camp:', self.id, old, self.status, self.camp)
        tintalt.ta_set_static([self.model], self.genTintStr())

    def genTintStr(self):
        if self.status == gametypes.BATTLE_FIELD_FLAG_STATTUS_DEFAULT:
            return 'default'
        if BigWorld.player().tempCamp == self.camp:
            campStr = '2'
        else:
            campStr = '1'
        return 't_' + campStr + '_' + str(self.status)

    def set_status(self, old):
        gamelog.debug('@hjx flag#set_status:', self.id, old, self.status, self.camp)
        tintalt.ta_set_static([self.model], self.genTintStr())

    def onTargetCursor(self, enter):
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                if (self.position - BigWorld.player().position).length > cursor.TALK_DISTANCE:
                    ui.set_cursor(cursor.talk_dis)
                else:
                    ui.set_cursor(cursor.talk)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()
