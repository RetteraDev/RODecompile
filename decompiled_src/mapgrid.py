#Embedded file name: /WORKSPACE/data/entities/client/helpers/mapgrid.o
import copy
import gametypes
from commonMapGrid import CommonMapGridVal, CommonMapGrid

class MapGridVal(CommonMapGridVal):

    def __init__(self, id, state = gametypes.MAP_GAME_GRID_STATE_INVALID, progress = 0, secondId = 0, rank = None):
        super(MapGridVal, self).__init__(id, state, progress, secondId)
        self.rank = copy.deepcopy(rank) if rank is not None else {}

    def fromClientDTO(self, dto, simple = True):
        if dto[0] != self.id:
            raise Exception('CommonMapGridVal.fromClientDTO, id inconsist %d %d' % (dto[0], self.id))
        if simple:
            _, self.state, self.progress, secondId = dto
        else:
            _, self.state, self.progress, secondId, rankData = dto
            self.rank.clear()
            for school, topData in rankData.iteritems():
                self.rank[str(school)] = {'ver': topData.get('ver', 0),
                 'data': []}
                for gbId, roleName, val, fromHostId in topData.get('dto'):
                    self.rank[str(school)]['data'].append((gbId,
                     roleName,
                     val,
                     fromHostId))

        if secondId and not self.secondId:
            self.cacheData.clear()
        self.secondId = secondId


class MapGrid(CommonMapGrid):

    def fromClientDTO(self, dto):
        for id, state, progress, secondId in dto:
            if not self.has_key(id):
                self[id] = MapGridVal(id, state, progress, secondId)
            else:
                self[id].state = state
                self[id].progress = progress
                if secondId and not self[id].secondId:
                    self[id].cacheData.clear()
                self[id].secondId = secondId
