#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/boneMorpher.o
import BigWorld
import ResMgr
import strmap
import gamelog
from helpers import avatarMorpherUtils as AMU
BONE_DATA_CACHE = {}

def getBoneConfig(configPath):
    configs = BONE_DATA_CACHE.get(configPath)
    if configs is not None:
        return configs
    directory = ResMgr.openSection(configPath)
    if not directory:
        return
    configs = filter(lambda s: s.endswith('.xml'), directory.keys())
    configs = [ item[:-4] for item in configs ]
    BONE_DATA_CACHE[configPath] = configs
    return configs


class BoneMorpher(object):

    def __init__(self, model, initpath, key = 'bones'):
        self.model = model
        self.transformMap = {}
        self.key = key
        self.valid = False
        self.configPath = initpath
        configData = getBoneConfig(initpath)
        if configData is None:
            gamelog.error('b.e.:BoneMorpher: config data %s not found' % initpath)
            return
        self.valid = True
        for k in configData:
            self.transformMap[k] = 0

    def setMorph(self, transform, ratio):
        if not self.hasMorph(transform):
            gamelog.error('b.e.:BoneMorpher: morph %s not found' % transform)
        else:
            ratio = round(float(ratio), 2)
            self.transformMap[transform] = ratio

    def hasMorph(self, transform):
        return self.transformMap.has_key(transform)

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
                gamelog.error('b.e.:BoneMorpher: bad bone name: ', k)

    def export(self, orig, filterFunc = None):
        sm = strmap.strmap(orig)
        sm.set(self.key, self.__tostring(filterFunc))
        return sm.__str__()

    def read(self, configMap, filterFunc = None):
        config = configMap.get(self.key, '')
        self.__fromstring(config, filterFunc)

    def toString(self):
        return self.__tostring(lambda v: AMU.getIdxByMorpher(v))


class BoneMorpherFactory(object):

    def __init__(self, model):
        self.model = model
        self.boneMorphers = []

    def register(self, boneMorpher):
        if not boneMorpher:
            return
        if not boneMorpher.valid or boneMorpher in self.boneMorphers or boneMorpher.model != self.model:
            gamelog.error('b.e.:BoneMorpher: register boneMorpher %s error' % boneMorpher.key)
            return
        self.boneMorphers.append(boneMorpher)

    def apply(self):
        config = []
        data = []
        for boneMorpher in self.boneMorphers:
            config.append(boneMorpher.configPath)
            data.append(boneMorpher.toString())

        config = tuple(config)
        data = '\n'.join(data)
        if not hasattr(self.model, 'boneScale'):
            self.model.boneScale = BigWorld.BoneScale()
        self.model.boneScale.applyAvatarConfig(config, data)

    def applyFaceBone(self):
        config = []
        data = []
        for boneMorpher in self.boneMorphers:
            if boneMorpher.key == 'faceBones':
                config.append(boneMorpher.configPath)
                data.append(boneMorpher.toString())

        config = tuple(config)
        data = '\n'.join(data)
        if not hasattr(self.model, 'boneScale'):
            self.model.boneScale = BigWorld.BoneScale()
        self.model.boneScale.applyAvatarConfig(config, data)

    def resetAndApply(self):
        for boneMorpher in self.boneMorphers:
            for k in boneMorpher.transformMap:
                boneMorpher.transformMap[k] = 0

        self.apply()
