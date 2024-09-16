#Embedded file name: I:/bag/tmp/tw2/res/entities\client/LogonEntity.o
import BigWorld

class LogonEntity(BigWorld.Entity):

    def __init__(self):
        super(LogonEntity, self).__init__()

    def enterWorld(self):
        pass

    def leaveWorld(self):
        pass


class PlayerLogonEntity(LogonEntity):

    def __init__(self):
        super(PlayerLogonEntity, self).__init__()

    def enterWorld(self):
        pass

    def onBecomePlayer(self):
        pass

    def handleKeyEvent(self, isDown, key, mods):
        pass

    def leaveWorld(self):
        pass
