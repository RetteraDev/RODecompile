#Embedded file name: I:/bag/tmp/tw2/res/entities\common/userInfo.o
import BigWorld
if BigWorld.component in ('base', 'cell'):
    import bwdecorator

class UserInfo(object):
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

    def fromStreamToSection(self, stream, section):
        o = self.createFromStream(stream)
        self.addToSection(o, section)

    def fromSectionToStream(self, section):
        o = self.createFromSection(section)
        return self.addToStream(o)
