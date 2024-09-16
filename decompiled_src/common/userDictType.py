#Embedded file name: I:/bag/tmp/tw2/res/entities\common/userDictType.o
import BigWorld
from userType import UserType
if BigWorld.component in ('base', 'cell'):
    import bwdecorator

class UserDictType(dict, UserType):
    if BigWorld.component in ('base', 'cell'):

        @bwdecorator.callableOnGhost
        def reloadScript(self):
            import gameconfig
            if gameconfig.enableRefreshScriptNew():
                return
            import utils
            utils.resetCls(self)
            self._lateReload()

    def _lateReload(self):
        pass

    def todict(self):
        return dict(self)

    def howMany(self):
        return len(self)

    def __str__(self):
        s = str(vars(self)) + '&&&&{{'
        for key, value in self.iteritems():
            s += str(key) + '::' + str(value) + '\n'

        s += '}}'
        return s
