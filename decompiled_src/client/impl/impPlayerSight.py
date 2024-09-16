#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerSight.o
import cPickle
import zlib

class ImpPlayerSight(object):

    def sightAll(self, spaceID, ver, info):
        self.buildingProxy.sightAll(spaceID, ver, info)

    def sightEnter(self, spaceID, oldID, info):
        self.buildingProxy.sightEnter(spaceID, oldID, cPickle.loads(zlib.decompress(info)))

    def sightLeave(self, oldID):
        self.buildingProxy.sightLeave(oldID)

    def sightAlterExtra(self, oldID, newInfo):
        self.buildingProxy.sightAlterExtra(oldID, cPickle.loads(zlib.decompress(newInfo)))

    def _hideSight(self, entityId):
        self.buildingProxy.hideProxy(entityId, flag=True)

    def _showSight(self, entityId):
        self.buildingProxy.hideProxy(entityId, flag=False)
