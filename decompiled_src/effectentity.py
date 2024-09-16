#Embedded file name: /WORKSPACE/data/entities/client/sfx/effectentity.o
import BigWorld
import Pixie
import clientUtils
import sfx

class EffectEntity(object):

    def __init__(self):
        self.model = sfx.getDummyModel()
        self.model.dummyModel = True
        self.autoLeaveWorld = False

    def setLivingTime(self, time):
        BigWorld.callback(time, self.leaveWorld)

    def enterWorld(self):
        self.player = BigWorld.player()

    def leaveWorld(self):
        if self.model:
            sfx.giveBackDummyModel(self.model)
        self.player = None
        self.model = None
        self.release()

    def setPosition(self, position):
        self.model.position = position

    def getPosition(self):
        return self.model.position

    position = property(getPosition, setPosition)

    def getYaw(self):
        return self.model.yaw

    def setYaw(self, yaw):
        self.model.yaw = yaw

    yaw = property(getYaw, setYaw)

    def getScale(self):
        return self.model.scale[0]

    def setScale(self, scale):
        self.model.scale = (scale, scale, scale)

    scale = property(getScale, setScale)

    def addEffect(self, effectid, duration = -1):
        self.fx = clientUtils.pixieFetch(sfx.getPath(effectid))
        self.fx.setAttachMode(0, 1, 0)
        self.fx.force()
        self.model.root.attach(self.fx)
        self.autoLeaveWorld = True

    def setAutoLeaveWorld(self, autoLeaveWorld):
        self.autoLeaveWorld = autoLeaveWorld

    def delEffect(self, effectid):
        self.fx.overCallback(None)
        self.model.root.detach(self.fx)
        self.fx.stop()
        self.fx.clear()
        if self.autoLeaveWorld:
            self.leaveWorld()

    def setVisible(self, visible):
        self.model.visible = visible
