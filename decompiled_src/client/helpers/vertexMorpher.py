#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/vertexMorpher.o
import BigWorld
import strmap
import gamelog
from helpers import avatarMorpherUtils as AMU

class VertexMorpher(object):

    def __init__(self, model, transformConfig = [], key = 'morphs'):
        self.model = model
        self.transformMap = {}
        self.key = key
        for i in transformConfig:
            self.transformMap[i] = 0

    def setMorph(self, transform, ratio):
        if not self.hasMorph(transform):
            gamelog.error('b.e.:VertexMorpher: morph %s not found' % transform)
        else:
            ratio = round(float(ratio), 2)
            self.transformMap[transform] = ratio
            self.model.setMorph(1, transform, ratio)

    def hasMorph(self, transform):
        return self.transformMap.has_key(transform)

    def apply(self):
        if self.model:
            self.model.applyMorph(1)

    def setAndApply(self, transform, ratio):
        self.setMorph(transform, ratio)
        self.apply()

    def __tostring(self, filterFunc = None):
        s = []
        for k, v in self.transformMap.iteritems():
            k = filterFunc(k) if filterFunc else k
            if v != 0.0:
                s.append('%s:%.2f' % (k, v))

        return '\n'.join(s)

    def __fromstring(self, s, filterFunc = None):
        for i in s.split('\n'):
            li = i.split(':')
            if len(li) != 2:
                continue
            k = filterFunc(li[0]) if filterFunc else li[0]
            if self.hasMorph(k):
                value = AMU.valueClip(round(float(li[1]), 2), 0, 1.0)
                self.transformMap[k] = value
            else:
                gamelog.error('b.e.:VertexMorpher: bad morph name: ', k)

    def export(self, orig, filterFunc = None):
        sm = strmap.strmap(orig)
        sm.set(self.key, self.__tostring(filterFunc))
        return sm.__str__()

    def read(self, configMap, filterFunc = None):
        if not self.model:
            return
        config = configMap.get(self.key, '')
        self.__fromstring(config, filterFunc)
        for i in self.transformMap:
            self.model.setMorph(1, i, self.transformMap[i])

    def createConfig(self, config):
        configMap = strmap.strmap(config)
        config = configMap.get(self.key, '')
        self.__fromstring(config, lambda v: AMU.getMorpherByIdx(v))

    def resetAndApply(self):
        for i in self.transformMap:
            self.transformMap[i] = 0
            self.model.setMorph(1, i, 0)

        self.apply()

    def reApply(self):
        for key, value in self.transformMap.iteritems():
            self.model.setMorph(1, key, value)

        self.apply()


class AvatarFaceMorpher(VertexMorpher):

    def __init__(self, avatarId, model = None):
        if avatarId:
            avatar = BigWorld.entity(avatarId)
            model = avatar.model
            if hasattr(avatar.modelServer, 'bodyModel'):
                model = avatar.modelServer.bodyModel
            elif avatar.inRiding():
                model = avatar.model.ride
        super(AvatarFaceMorpher, self).__init__(model, AMU.FACE_MORPHER_DATA, 'faceMorphs')

    def readConfig(self, config):
        configMap = strmap.strmap(config)
        self.read(configMap, lambda v: AMU.getMorpherByIdx(v))
