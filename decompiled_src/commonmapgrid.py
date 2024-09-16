#Embedded file name: /WORKSPACE/data/entities/common/commonmapgrid.o
import copy
from userSoleType import UserSoleType
from userDictType import UserDictType
from data import map_game_grid_data as MGGD
from data import map_game_grid_pos_data as MGGPD

class CommonMapGridVal(UserSoleType):

    def __init__(self, id, state = 0, progress = 0, secondId = 0):
        self.id = id
        self.state = state
        self.progress = progress
        self.cacheData = {}
        self.secondId = secondId

    def _lateReload(self):
        self.cacheData.clear()

    @property
    def contentId(self):
        if self.secondId:
            return self.secondId
        if not self.cacheData.has_key('contentId'):
            self.cacheData['contentId'] = MGGPD.data.get(self.id, {}).get('contentId', 0)
        return self.cacheData.get('contentId', 0)

    @property
    def pos(self):
        if not self.cacheData.has_key('pos'):
            self.cacheData['pos'] = MGGPD.data.get(self.id, {}).get('pos', (0, 0))
        return self.cacheData.get('pos', (0, 0))

    @property
    def progressType(self):
        if not self.cacheData.has_key('progressType'):
            self.cacheData['progressType'] = MGGD.data.get(self.contentId, {}).get('progressType', 0)
        return self.cacheData.get('progressType', 0)

    @property
    def initProgress(self):
        if not self.cacheData.has_key('initProgress'):
            self.cacheData['initProgress'] = MGGD.data.get(self.contentId, {}).get('initProgress', 0)
        return self.cacheData.get('initProgress', 0)

    @property
    def totalProgress(self):
        if not self.cacheData.has_key('totalProgress'):
            self.cacheData['totalProgress'] = MGGD.data.get(self.contentId, {}).get('totalProgress', 0)
        return self.cacheData.get('totalProgress', 0)

    @property
    def initState(self):
        return MGGD.data.get(self.contentId, {}).get('initState')

    @property
    def type(self):
        if not self.cacheData.has_key('type'):
            self.cacheData['type'] = MGGD.data.get(self.contentId, {}).get('type', 0)
        return self.cacheData.get('type', 0)

    @property
    def fubenId(self):
        if not self.cacheData.has_key('fubenid'):
            self.cacheData['fubenid'] = MGGD.data.get(self.contentId, {}).get('fubenid', 0)
        return self.cacheData.get('fubenid', 0)

    @property
    def startTime(self):
        if not self.cacheData.has_key('starttime'):
            self.cacheData['starttime'] = MGGD.data.get(self.contentId, {}).get('starttime', 0)
        return self.cacheData.get('starttime', 0)

    @property
    def endTime(self):
        if not self.cacheData.has_key('endtime'):
            self.cacheData['endtime'] = MGGD.data.get(self.contentId, {}).get('endtime', '')
        return self.cacheData.get('endtime', '')

    @property
    def addBonus(self):
        if not self.cacheData.has_key('addBonus'):
            self.cacheData['addBonus'] = MGGD.data.get(self.contentId, {}).get('addBonus', 0)
        return self.cacheData.get('addBonus', 0)

    @property
    def totalBonus(self):
        if not self.cacheData.has_key('totalBonus'):
            self.cacheData['totalBonus'] = MGGD.data.get(self.contentId, {}).get('totalBonus', 0)
        return self.cacheData.get('totalBonus', 0)

    @property
    def title(self):
        return MGGD.data.get(self.contentId, {}).get('title', '')

    @property
    def compMailId(self):
        return MGGPD.data.get(self.id, {}).get('compMailId', 0)

    @property
    def initCampId(self):
        return MGGPD.data.get(self.id, {}).get('initCampId', 0)

    @property
    def targetGridId(self):
        return MGGPD.data.get(self.id, {}).get('targetGrid', 0)

    @property
    def addTargetProgress(self):
        return MGGPD.data.get(self.id, {}).get('addTargetProgress', 0)

    @property
    def openInnerGrid(self):
        return MGGPD.data.get(self.id, {}).get('openInnerGrid', [])

    @property
    def openEdgeGrid(self):
        return MGGPD.data.get(self.id, {}).get('openEdgeGrid', [])

    @property
    def rodeGrid(self):
        if self.openEdgeGrid:
            return self.openEdgeGrid[0]
        elif self.openInnerGrid:
            return self.openInnerGrid[0]
        else:
            return 0

    def getProgressPct(self):
        import gametypes
        import math
        pct = int(math.floor(self.progress * 100 / self.totalProgress))
        pct = max(min(pct, 100), 0)
        if self.progressType == gametypes.MAP_GAME_PROGRESS_TYPE_INC:
            return pct
        if self.progressType == gametypes.MAP_GAME_PROGRESS_TYPE_DEC:
            return 100 - pct
        return 0

    def getProgressLeftPct(self):
        import gametypes
        import math
        pct = int(math.ceil(self.progress * 100.0 / self.totalProgress))
        pct = max(min(pct, 100), 0)
        if self.progressType == gametypes.MAP_GAME_PROGRESS_TYPE_INC:
            return 100 - pct
        if self.progressType == gametypes.MAP_GAME_PROGRESS_TYPE_DEC:
            return pct
        return 100


class CommonMapGrid(UserDictType):

    def _lateReload(self):
        super(CommonMapGrid, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
