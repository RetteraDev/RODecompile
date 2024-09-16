#Embedded file name: I:/bag/tmp/tw2/res/entities\client/AvatarRobot.o
import inspect
import BigWorld
import gameglobal
import Avatar

class AvatarRobotMeta(type):

    def __init__(cls, name, bases, dic):
        super(AvatarRobotMeta, cls).__init__(name, bases, dic)
        for n, f in inspect.getmembers(Avatar.Avatar, inspect.ismethod):
            setattr(cls, n, f.im_func)


class AvatarRobot(Avatar.Avatar):
    IsAvatar = False
    IsAvatarRobot = True

    def afterModelFinish(self):
        super(AvatarRobot, self).afterModelFinish()
        self.filter = BigWorld.AvatarDropFilter()
        self.filter.clientYawMinDist = gameglobal.CLIENT_MIN_YAW_DIST
        self.filter.enableBodyPitch = False
        self.am.turnModelToEntity = True
