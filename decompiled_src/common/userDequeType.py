#Embedded file name: I:/bag/tmp/tw2/res/entities\common/userDequeType.o
import BigWorld
from userType import UserType
from collections import deque
if BigWorld.component in ('base', 'cell'):
    import bwdecorator

class UserDequeType(deque, UserType):
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

    def todeque(self):
        return deque(self)

    def tolist(self):
        return list(self)

    def totuple(self):
        return tuple(self)

    def howMany(self):
        return len(self)
