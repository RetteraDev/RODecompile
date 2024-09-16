#Embedded file name: I:/bag/tmp/tw2/res/entities\client/JiGuan.o
import BigWorld
import Math
import const
import gameglobal
import utils
from iClient import IClient
from helpers import fashion
from helpers import modelServer
from helpers import ufo
from sfx import sfx
from guis import ui
from guis import cursor
from data import jiguan_client_data as JCD
from cdata import game_msg_def_data as GMDD

class JiGuan(IClient):
    TOPLOGO_OFFSET = 0.5

    def __init__(self):
        super(JiGuan, self).__init__()
        self.firstFetchFinished = False
        self.needTrapCallback = True
        self.obstacleModel = None
        self.topLogoOffset = JCD.data.get(self.jiguanId, {}).get('logoOffset', JiGuan.TOPLOGO_OFFSET)

    def enterWorld(self):
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.initYaw = self.yaw
        self.modelServer = modelServer.SimpleModelServer(self)
        self.isLeaveWorld = False
        self.roleName = JCD.data.get(self.jiguanId, {}).get('name')
        self.needTrapCallback = JCD.data.get(self.jiguanId, {}).get('needTrapCallback0', True)
        self.trapId = BigWorld.addPot(self.matrix, const.JIGUAN_USE_DIST, self.trapCallback)

    def canOutline(self):
        noOutline = JCD.data.get(self.jiguanId, {}).get('noOutline', False)
        if noOutline:
            return False
        return super(JiGuan, self).canOutline()

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        noTrap = JCD.data.get(self.jiguanId, {}).get('noTrap', False)
        if noTrap:
            return
        if self.needTrapCallback:
            self.jiguanTrapCallback()

    def jiguanTrapCallback(self):
        useDist = const.JIGUAN_USE_DIST
        entities = []
        p = BigWorld.player()
        for entity in (self,):
            if not isinstance(entity, JiGuan):
                continue
            if not (entity.position - p.position).lengthSquared < useDist * useDist:
                continue
            if entity.isLeaveWorld:
                continue
            if entity.locked:
                continue
            if entity.ownerId > 0 and entity.ownerId != p.id:
                continue
            entities.append(entity)

        BigWorld.player().jiguanTrapInCallBack(entities)

    def leaveWorld(self):
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        self.delObstacleFollower()
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
        self.isLeaveWorld = True
        if self.needTrapCallback:
            self.jiguanTrapCallback()
        self.removeAllFx()
        clientEntityId = getattr(self, 'clientEntityId', None)
        if clientEntityId:
            BigWorld.player().showClientShip(clientEntityId)

    def getItemData(self):
        return JCD.data.get(self.jiguanId, {'model': gameglobal.defaultModelID})

    def afterModelFinish(self):
        super(JiGuan, self).afterModelFinish()
        mirror = JCD.data.get(self.jiguanId, {}).get('mirror', 0)
        if mirror:
            oldScale = self.model.scale
            self.model.scale = (-oldScale[0], oldScale[1], oldScale[2])
        self.firstFetchFinished = True
        self.addObstacleFollow()
        self.refreshState(self.state)
        canSelect = JCD.data.get(self.jiguanId, {}).get('canselect', True)
        if canSelect:
            self.setTargetCapsUse(True)
            if self.locked:
                self.setTargetCapsUse(False)
        else:
            self.setTargetCapsUse(False)
        self.filter = BigWorld.AvatarFilter()
        clientEntityId = getattr(self, 'clientEntityId', None)
        if clientEntityId:
            BigWorld.player().hideClientShip(clientEntityId)
        needExpandVB = JCD.data.get(self.jiguanId, {}).get('needExpandVB', False)
        if needExpandVB and self.model:
            self.model.expandVisibilityBox(1000)
        self.setExtraDirection()
        if self.isSceneObj():
            self.model.isSceneObj = True

    def addObstacleFollow(self):
        self.obstacleModel = None
        data = JCD.data.get(self.jiguanId, {})
        modelId = data.get('followObstacleModel', None)
        if not modelId:
            return
        scaleMatrix = Math.Matrix()
        if data.get('mirror', 0):
            scaleMatrix.setScale((-1.0, 1.0, 1.0))
        else:
            scaleMatrix.setScale((1.0, 1.0, 1.0))
        mp = Math.MatrixProduct()
        mp.a = scaleMatrix
        mp.b = self.matrix
        modelPath = 'char/' + str(modelId) + '/' + str(modelId) + '.model'
        BigWorld.fetchObstacleModel(modelPath, mp, True, self.realFollow)

    def realFollow(self, model):
        if not self.inWorld:
            return
        if not model:
            return
        self.obstacleModel = model
        self.addModel(self.obstacleModel)
        data = JCD.data.get(self.jiguanId, {})
        followNodeName = data.get('followNodeName', None)
        if followNodeName:
            followNode = self.model.node(followNodeName)
        else:
            followNode = self.model.node('HP_root')
        self.obstacleModel.matrix = followNode
        self.obstacleModel.setEntity(self.id)

    def delObstacleFollower(self):
        if self.obstacleModel and self.obstacleModel.attached:
            self.delModel(self.obstacleModel)
        self.obstacleModel = None

    def startChangeState(self, oldState, newState):
        actionId = JCD.data[self.jiguanId].get('action%d-%d' % (oldState, newState))
        if actionId and actionId in self.fashion.getActionNameList():
            self.fashion.playSingleAction(actionId, keep=99999999)

    def set_state(self, old):
        self.refreshState(self.state)

    def set_locked(self, old):
        if self.needTrapCallback:
            self.jiguanTrapCallback()
        canSelect = JCD.data.get(self.jiguanId, {}).get('canselect', True)
        if canSelect:
            self.setTargetCapsUse(True)
            if self.locked:
                self.setTargetCapsUse(False)
        else:
            self.setTargetCapsUse(False)

    def refreshState(self, state):
        data = JCD.data.get(self.jiguanId, {})
        action = data.get('action%d' % state)
        if action:
            self.fashion.playSingleAction(action)
        self.needTrapCallback = data.get('needTrapCallback%d' % state, True)
        self.removeAllFx()
        effect = data.get('effect%d' % state)
        if effect:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             effect,
             sfx.EFFECT_UNLIMIT))
            self.addFx(effect, fx)

    def use(self):
        p = BigWorld.player()
        if self.ownerId > 0 and self.ownerId != p.id:
            return
        if self.locked:
            return
        if not p.stateMachine.checkStatus(const.CT_ACTION_SPELL):
            p.showGameMsg(GMDD.data.ACTION_CHECK_STATUS_DENY, ())
            return
        if not self.needTrapCallback:
            return
        self.cell.use()

    def noNeedChase(self):
        return JCD.data.get(self.jiguanId, {}).get('noNeedChase', False)

    def needBlackShadow(self):
        return not self.getItemData().get('noBlackUfo', False)

    def noNeedCursor(self):
        return JCD.data.get(self.jiguanId, {}).get('noNeedCursor', False)

    def onTargetCursor(self, enter):
        if self.noNeedCursor():
            return
        if enter:
            if ui.get_cursor_state() == ui.NORMAL_STATE:
                ui.set_cursor_state(ui.TARGET_STATE)
                if (self.position - BigWorld.player().position).length > cursor.TALK_DISTANCE:
                    ui.set_cursor(cursor.jiguan_dis)
                else:
                    ui.set_cursor(cursor.jiguan)
                ui.lock_cursor()
        elif ui.get_cursor_state() == ui.TARGET_STATE:
            ui.reset_cursor()

    def showTargetUnitFrame(self):
        return False

    def getModelScale(self):
        data = self.getItemData()
        scale = data.get('scale', 1.0)
        self.model.scale = (scale, scale, scale)
        return (scale, scale, scale)

    def needAttachUFO(self):
        return not self.getItemData().get('noUfo', False)

    def isSceneObj(self):
        if getattr(self.model, 'isSceneObj', False):
            return self.getItemData().get('isSceneObj', False)
        return False
