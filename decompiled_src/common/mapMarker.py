#Embedded file name: I:/bag/tmp/tw2/res/entities\common/mapMarker.o
import const
from userSoleType import UserSoleType
from userDictType import UserDictType

class MapMarkerVal(UserSoleType):

    def __init__(self, index, pos, title, desc):
        self.index = index
        self.pos = pos
        self.title = title
        self.desc = desc


class MapMarker(UserDictType):

    def __init__(self):
        super(MapMarker, self).__init__()

    def _lateReload(self):
        super(MapMarker, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def addMarker(self, index, pos, title, desc):
        if len(self.keys()) > const.MAP_MARKER_NUM:
            return False
        if self.has_key(index):
            return False
        self[index] = MapMarkerVal(index, pos, title, desc)
        return True

    def modifyMarker(self, index, pos, title, desc):
        if not self.has_key(index):
            return False
        self[index].pos = pos
        self[index].title = title
        self[index].desc = desc
        return True

    def delMarker(self, index):
        if self.pop(index, None):
            return True
        return False
