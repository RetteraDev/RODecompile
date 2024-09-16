#Embedded file name: /WORKSPACE/data/entities/client/puppet.o
import BigWorld
import Avatar

class Puppet(Avatar.Avatar):
    IsAvatar = False
    IsPuppet = True
    IsAvatarOrPuppet = True

    def afterModelFinish(self):
        super(Puppet, self).afterModelFinish()
        self.filter = BigWorld.AvatarDropFilter()
        self.filter.popDist = 3
