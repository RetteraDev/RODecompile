#Embedded file name: I:/bag/tmp/tw2/res/entities\common/userSoleType.o
import BigWorld
from userType import UserType

class UserSoleType(UserType):
    if BigWorld.component in ('base', 'cell'):

        def reloadScript(self):
            import gameconfig
            if gameconfig.enableRefreshScriptNew():
                return
            import utils
            utils.resetCls(self)
            self._lateReload()

    def _lateReload(self):
        pass
