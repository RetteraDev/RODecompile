#Embedded file name: I:/bag/tmp/tw2/res/entities\common/userListType.o
import BigWorld
from userType import UserType
if BigWorld.component in ('base', 'cell'):
    import bwdecorator

class ArrayProxy(object):

    def __init__(self, array):
        self.array = array

    def __len__(self):
        return len(self.array)

    def __getitem__(self, key):
        return self.array[key]

    def __setitem__(self, key, item):
        self.array[key] = item

    def __delitem__(self, key):
        del self.array[key]

    def __iter__(self):
        return iter(self.array)

    def __contains__(self, item):
        return item in self.array

    def __getattr__(self, name):
        return getattr(self.array, name)


class UserListType(list, UserType):
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

    def tolist(self):
        return list(self)

    def totuple(self):
        return tuple(self)

    def howMany(self):
        return len(self)

    def __str__(self):
        s = str(self.__class__.__name__) + ' '
        s + str(vars(self)) + '&&&&[['
        for l in self:
            s += ',,' + str(l)

        s += ']]'
        return s


class BwListType(ArrayProxy):
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

    def tolist(self):
        return list(self)

    def totuple(self):
        return tuple(self)
