#Embedded file name: I:/bag/tmp/tw2/res/entities\client/OreSpawnPoint.o
import BigWorld
import Math
import gameglobal
import gamelog
import gametypes
import const
import clientcom
from iCombatUnit import ICombatUnit
from Monster import Monster
from guis import ui
from guis import cursor
from sfx import sfx
from data import ore_spawn_point_data as OSPD
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class OreSpawnPoint(Monster):
    IsMonster = False

    def __init__(self):
        super(OreSpawnPoint, self).__init__()
        self.applyTints = []
        self.attachedEffect = 0
        self.IsOreSpawnPoint = True
        self.trapId = None
        self.obstacleModel = None

    def enterWorld(self):
        super(OreSpawnPoint, self).enterWorld()
        od = OSPD.data.get(self.oreSpawnPointId, {})
        radius = od.get('distance', 10)
        self.trapId = BigWorld.addPot(self.matrix, radius, self.trapCallback)

    def leaveWorld(self):
        super(OreSpawnPoint, self).leaveWorld()
        if self.obstacleModel:
            self.delModel(self.obstacleModel)
            self.obstacleModel = None
        if self.trapId:
            BigWorld.delPot(self.trapId)
            self.trapId = None
            if gameglobal.rds.ui.pressKeyF.type == const.F_ORE_SPAWN_POINT:
                if gameglobal.rds.ui.pressKeyF.oreSpawnPoint == self:
                    gameglobal.rds.ui.pressKeyF.oreSpawnPoint = None
                    gameglobal.rds.ui.pressKeyF.removeType(const.F_ORE_SPAWN_POINT)

    def removeFKey(self):
        if gameglobal.rds.ui.pressKeyF.oreSpawnPoint == self:
            gameglobal.rds.ui.pressKeyF.oreSpawnPoint = None
            gameglobal.rds.ui.pressKeyF.removeType(const.F_ORE_SPAWN_POINT)

    def set_phase(self, old):
        self.playPhaseAE(self.phase)

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if self.visibility == const.VISIBILITY_HIDE:
            return
        p = BigWorld.player()
        if p.position.y - self.position.y > SCD.data.get('trapHeight', 5):
            return
        if enteredTrap:
            gameglobal.rds.ui.pressKeyF.oreSpawnPoint = self
            gameglobal.rds.ui.pressKeyF.setType(const.F_ORE_SPAWN_POINT)
        else:
            self.removeFKey()

    def getFKey(self):
        return OSPD.data.get(self.oreSpawnPointId, {}).get('fKey', 2)

    def playPhaseAE(self, phaseID):
        gamelog.debug('jinjj--playPhaseAE-', phaseID)
        if not self.inWorld:
            return
        od = OSPD.data.get(self.oreSpawnPointId, {})
        self.removeAllFx()
        if not od:
            return
        phaseStr = 'phase%d_AE' % phaseID
        phaseContent = od.get(phaseStr, ())
        if len(phaseContent) < 2:
            self.stopActions()
            return
        actionName = phaseContent[0]
        effectList = phaseContent[1]
        if type(actionName) in (tuple, list):
            self.playActions(actionName)
        else:
            self.playActions((actionName,))
        self.attachedEffect = effectList
        if type(effectList) in (tuple, list):
            if len(effectList):
                for effect in effectList:
                    fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                     self.getBasicEffectPriority(),
                     self.model,
                     effect,
                     sfx.EFFECT_UNLIMIT))
                    self.addFx(effect, fx)

        else:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             effectList,
             sfx.EFFECT_UNLIMIT))
            self.addFx(effectList, fx)

    def afterModelFinish(self):
        super(OreSpawnPoint, self).afterModelFinish()
        self.createObstacleModel()
        self.playPhaseAE(self.phase)
        self.resetTopLogo()
        self.topLogo.titleName = self.titleName
        self.topLogo.setTitleName(self.titleName)
        self.modelServer.attachModelFromData()

    def createObstacleModel(self):
        data = OSPD.data.get(self.oreSpawnPointId, {})
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
        if model:
            model.setCollide(True)
            model.setPicker(True)
            self.obstacleModel = model
            self.addModel(model)
            self.checkCollideWithPlayer()

    def onTargetCursor(self, enter):
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                cursorType = SCD.data.get('OrgSpawnCursorType', cursor.choose)
                ui.set_cursor(cursorType)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    def use(self):
        super(OreSpawnPoint, self).use()
        if not self.inWorld:
            return
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            p.showGameMsg(GMDD.data.FORBIDDEN_WRONG_LIFE, ())
            return
        if not hasattr(p, 'guildNUID') or p.guildNUID == 0:
            p.showGameMsg(GMDD.data.ORE_SPAWN_POINT_NOT_IN_GUILD, ())
            return
        if hasattr(self, 'guildNUID'):
            if self.guildNUID != p.guildNUID:
                if self.phase != gametypes.ORE_SPAWN_POINT_CHARGING:
                    self.cell.startCharging()
                    return
                p.showGameMsg(GMDD.data.ORE_SPAWN_CHARGING, ())
            else:
                p.showGameMsg(GMDD.data.ORE_SPAWN_POINT_IN_GUILD, ())
        elif self.phase == gametypes.ORE_SPAWN_POINT_INIT:
            self.cell.startCharging()
            return

    def canBeUsedSkill(self, srcEnt, skillInfo):
        od = OSPD.data.get(self.oreSpawnPointId, {})
        validSkills = od.get('needSkills', ())
        if skillInfo.num not in validSkills:
            return False
        return True

    def set_life(self, old):
        super(OreSpawnPoint, self).set_life(old)
        if self.life == gametypes.LIFE_DEAD:
            if gameglobal.rds.ui.pressKeyF.oreSpawnPoint == self:
                gameglobal.rds.ui.pressKeyF.oreSpawnPoint = None
                gameglobal.rds.ui.pressKeyF.removeType(const.F_ORE_SPAWN_POINT)

    def isIntersectWithPlayer(self, model):
        pos = BigWorld.player().position
        minbd = model.pickbdbox[0] - Math.Vector3(0.5, 2, 0.5)
        maxbd = model.pickbdbox[1] + Math.Vector3(0.5, 0, 0.5)
        return clientcom.isInBoundingBox(minbd, maxbd, pos)

    def checkCollideWithPlayer(self, dist = 2.0):
        model = self.obstacleModel
        player = BigWorld.player()
        if not model or not model.inWorld or not model.collidable or not player.ap:
            return
        if self.isIntersectWithPlayer(model):
            invMatrix = Math.Matrix(model.matrix)
            invMatrix.invert()
            localPos = invMatrix.applyPoint(player.position)
            if localPos.x < 0:
                dstPos = Math.Vector3(0, 0, -dist)
            else:
                dstPos = Math.Vector3(0, 0, dist)
            mat = Math.Matrix(model.matrix)
            dstPos = mat.applyPoint(dstPos)
            player.ap.beginForceMove(dstPos, False)

    def skillDamage(self, host, damageResult, skillInfo, clientSkillInfo, needSplitDamage = True, extInfo = {}, showHitEff = True, strHitNodeName = None):
        if not self.inWorld:
            return
        data = OSPD.data.get(self.oreSpawnPointId, {})
        if skillInfo.num not in data.get('needSkills', ()):
            return
        ICombatUnit.skillDamage(self, host, damageResult, skillInfo, clientSkillInfo, needSplitDamage, extInfo, showHitEff, strHitNodeName)
