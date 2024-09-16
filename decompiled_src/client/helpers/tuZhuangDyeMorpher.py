#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/tuZhuangDyeMorpher.o
import ResMgr
import const
import clientcom
from helpers import tintalt as TA
from data import tuzhuang_light_index_data as TZLID

def checkDyes(partDyes):
    if partDyes and type(partDyes) in (tuple, list) and len(partDyes) in const.TZ_DYES_INDEXS:
        return True
    return False


def _getRGBA(v):
    try:
        r, g, b, a = v.split(',')
        valid = True
        for x in (r,
         g,
         b,
         a):
            if not x.isdigit():
                valid = False
                break

        if not valid:
            r = g = b = a = '255'
    except:
        r = g = b = a = '255'

    return (r,
     g,
     b,
     a)


def getTuZhuangParam(partDyes):
    params = []
    if not checkDyes(partDyes):
        partDyes = const.DEFAULT_TZ_DYES[0:const.TZ_INDEX_THIRD_COLOR]
        params.append(0)
        params.append(0)
        params.append(0)
    else:
        params.append(1)
        if len(partDyes) < const.TZ_INDEX_SECOND_COLOR:
            params.append(0)
        else:
            params.append(1)
        if len(partDyes) < const.TZ_INDEX_THIRD_COLOR:
            params.append(0)
        else:
            params.append(1)
    l = len(partDyes)
    partDyes = list(partDyes) + const.DEFAULT_TZ_DYES[l:]
    for v in partDyes[:-1]:
        if ',' in v:
            r, g, b, a = _getRGBA(v)
            params.append('%f %f %f %f' % (float(r) / 255.0,
             float(g) / 255.0,
             float(b) / 255.0,
             float(a) / 255.0))
        else:
            params.append(float(v))

    lightIndex = partDyes[-1]
    if lightIndex.isdigit() and TZLID.data.has_key(int(lightIndex)):
        params.append(TZLID.data[int(lightIndex)]['texturePath'])
    else:
        params.append(lightIndex)
    return params


class TuZhuangDyeMorpher(object):
    MATTER = 'tuzhuang'
    TINT_NAME = 'tuzhuang'
    TINT_NAME2 = 'tuzhuang2'
    DDS_PATH_PREFIX = 'env/pbr_cubemap/s/'

    def __init__(self, model):
        super(TuZhuangDyeMorpher, self).__init__()
        self.model = model
        self.param = []
        self.subMatter = None
        self.tintName = self.TINT_NAME2

    def hasTexture(self):
        return self.param[-1].rfind('.dds') != -1 or self.param[0].rfind('.tga') != -1

    def read(self, config, subMatter = None):
        self.param = config
        self.subMatter = subMatter

    def getTuZhuangParam(self):
        params = self.param
        params = getTuZhuangParam(params)
        return params

    def apply(self):
        if self.model:
            params = self.getTuZhuangParam()
            if self.hasTexture():
                self.model.addTintFxTexture(params[-1])
            TA.ta_add([self.model], self.tintName, params, 0, self.MATTER, False, True)
            if self.subMatter:
                TA.ta_set_static([self.model], self.subMatter, self.MATTER, applyLater=True)
            else:
                TA.ta_set_static([self.model], 'Default', self.MATTER, applyLater=True)
            TA.ta_apply([self.model], tintName=self.tintName)

    def syncApply(self):
        clientcom.fetchTintEffectContentsByName([self.tintName], self.afterTintComplete)

    def afterTintComplete(self, tintEffects):
        model = self.model
        if not model or not model.inWorld:
            return
        if tintEffects:
            model.tintCopy = dict(zip([self.tintName], tintEffects))
            self.apply()
            TA.clearTintCopy(model.tintCopy)
            model.tintCopy = None

    def getDynamicTint(self, tintSection = None):
        params = self.getTuZhuangParam()
        content = None
        if tintSection:
            content = tintSection.get(self.MATTER, None)
        else:
            content = ResMgr.createXMLSectionFromString('ta', '<ta></ta>')
            content.copy(TA.TAs[self.tintName][1])
        try:
            TA.parse_tint_with_params(content, params)
        except:
            return

        static = 'staticDefault'
        if self.subMatter:
            static = self.subMatter
        staticTintName = TA.build_tint_name(content, static)
        return (self.MATTER,
         staticTintName,
         self.tintName,
         params)
