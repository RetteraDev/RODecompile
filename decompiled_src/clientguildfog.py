#Embedded file name: /WORKSPACE/data/entities/client/clientguildfog.o
import gameglobal
import iClientOnly
from data import guild_config_data as GCD
from sfx import sfx

class ClientGuildFog(iClientOnly.IClientOnly):
    FOG_EFFECT = 5006
    KEEPTIME = 999999999
    SCALE = 1.0

    def __init__(self):
        super(ClientGuildFog, self).__init__()
        self.handleCallback = None
        self.isRealModel = True

    def __getattr__(self, name):
        if not self.inWorld:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)
        try:
            return self.__dict__['attrs'][name]
        except KeyError:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)

    def enterWorld(self):
        super(ClientGuildFog, self).enterWorld()
        self.fogEffect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (3,
         3,
         None,
         GCD.data.get('fogEffectId', self.FOG_EFFECT),
         sfx.EFFECT_UNLIMIT,
         self.position,
         0,
         0,
         0,
         self.KEEPTIME))
        if self.fogEffect:
            for effect in self.fogEffect:
                effect and effect.scale(*self.scale)

    def leaveWorld(self):
        super(ClientGuildFog, self).leaveWorld()
        if self.fogEffect:
            for effect in self.fogEffect:
                effect and effect.stop()

        self.fogEffect = []
