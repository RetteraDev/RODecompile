#Embedded file name: I:/bag/tmp/tw2/res/entities\client/iClientOnly.o
import BigWorld
import gameglobal

class IClientOnly(BigWorld.Entity):

    @classmethod
    def classname(cls):
        return cls.__name__

    IsCombatUnit = False
    IsMonster = False
    IsAvatar = False
    IsCreation = False
    IsSummonedBeast = False
    IsFragileObject = False
    IsSummonedSprite = False
    IsPot = False
    IsSummoned = False

    def __init__(self):
        super(IClientOnly, self).__init__()
        self.fashion = None

    def enterWorld(self):
        pass

    def leaveWorld(self):
        pass

    def enterTopLogoRange(self, distance):
        pass

    def leaveTopLogoRange(self, distance):
        pass

    def enterInteractiveRange(self, rangeDist = -1):
        pass

    def leaveInteractiveRange(self, rangeDist = -1):
        pass

    def leaveDlgRange(self, unUsedDist):
        pass

    def enterLoadModelRange(self, rangeDist = -1):
        pass

    def leaveLoadModelRange(self, rangeDist = -1):
        pass

    def hide(self, isHide):
        pass

    def needSetStaticStates(self):
        return False

    def getUFOLod(self):
        return gameglobal.UFO_DIST

    def setEntityFilter(self):
        self.filter = BigWorld.AvatarDropFilter()
