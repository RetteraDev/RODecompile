#Embedded file name: /WORKSPACE/data/entities/client/helpers/dyemorpher.o
import random
import BigWorld
import ResMgr
import strmap
import charRes
import const
import gamelog
import gameglobal
import clientcom
import clientUtils
from helpers import avatarMorpherUtils as AMU
from callbackHelper import Functor
from helpers import tintalt as TA
ALPHA_MAX_LIMIT = 3500
SKIN_AVATAR_MAX_LIMIT = 1700
RGB_MAX_LIMIT = 300
EYE_BGB_MAX_LIMIT = 800
DEFAULT_DYES = ('255,255,255,255',
 '255,255,255,255',
 '1',
 '0',
 '1',
 '255,255,255,255',
 '255,255,255,255')
AVATAR_SKIN_TRANS_TINT = 'avatarSkinTrans'
TRANSPARENT_TYPE = ('body', 'cape')

def getTintByMatter(modelId, part, matter):
    if part in ('hair', 'head'):
        if matter == 'hair':
            return ('avatarHair', 'avatarSkin', None)
        if matter == 'head':
            return (charRes.retransGender(modelId) == const.SEX_MALE and 'avatarHead1' or 'avatarHead2', 'avatarSkin', None)
        if matter == 'eye':
            return ('avatarEye', None, None)
        if matter == 'eyelash':
            return ('avatarEyelash', None, None)
        if matter == 'hairDye':
            return ('avatarSkin', None, None)
    else:
        if matter == 'hair':
            return ('avatarSkin', 'avatarHair', None)
        if matter == 'head':
            return ('avatarSkin', charRes.retransGender(modelId) == const.SEX_MALE and 'avatarHead1' or 'avatarHead2', None)
    return ('avatarSkin', 'avatarSkinEquip', AVATAR_SKIN_TRANS_TINT)


def calcMinVar(it, p):
    ret = None
    minVar = -1
    for r in p:
        rs = r.split(',')
        tempVar = 0
        for i, x in enumerate(rs):
            tempVar += (it[i] - int(x)) ** 2

        if minVar == -1 or minVar > tempVar:
            minVar = tempVar
            ret = rs

    return ret


def checkColorRange(key, transform, p, r, vv):
    s1, s2, s3, s4 = r.split(',')
    if s4.isdigit():
        maxLimit = ALPHA_MAX_LIMIT
        if key in ('skinDyes', 'headDyes'):
            maxLimit = SKIN_AVATAR_MAX_LIMIT
        rgbMaxLimit = RGB_MAX_LIMIT
        if key == 'eyeDyes':
            rgbMaxLimit = EYE_BGB_MAX_LIMIT
        i1 = int(s1)
        i2 = int(s2)
        i3 = int(s3)
        i4 = int(s4)
        if not gameglobal.rds.isSinglePlayer and gameglobal.rds.configData.get('enableCheckSkin', True) and transform == 'skin_Color':
            if r not in p:
                if i4 >= maxLimit or i1 >= rgbMaxLimit or i2 >= rgbMaxLimit or i3 >= rgbMaxLimit:
                    s1, s2, s3, s4 = p[0].split(',')
                else:
                    s1, s2, s3, s4 = calcMinVar((i1,
                     i2,
                     i3,
                     i4), p)
            vv.append(','.join((s1.strip(),
             s2.strip(),
             s3.strip(),
             s4.strip())))
        else:
            i1 = AMU.valueClip(i1, 0, rgbMaxLimit)
            i2 = AMU.valueClip(i2, 0, rgbMaxLimit)
            i3 = AMU.valueClip(i3, 0, rgbMaxLimit)
            i4 = AMU.valueClip(i4, 0, maxLimit)
            vv.append('%d,%d,%d,%d' % (i1,
             i2,
             i3,
             i4))


def checkDyes(partDyes):
    if partDyes and len(partDyes) in const.DYES_INDEXS:
        return True
    return False


def getAvatarSkinParam(partDyes, isPbr = False):
    params = []
    if not checkDyes(partDyes):
        partDyes = const.DEFAULT_DYES[0:const.DYES_INDEX_PBR_TEXTURE_DEGREE]
        params.append(0)
        params.append(0)
    else:
        params.append(1)
        if len(partDyes) < const.DYES_INDEX_DUAL_COLOR:
            params.append(0)
        else:
            params.append(1)
    l = len(partDyes)
    partDyes = list(partDyes) + const.DEFAULT_DYES[l:]
    for v in partDyes[const.DYES_INDEX_COLOR:const.DYES_INDEX_TEXTURE]:
        if ',' in v:
            r, g, b, a = _getRGBA(v)
            params.append('%f %f %f %f' % (float(r) / 255.0,
             float(g) / 255.0,
             float(b) / 255.0,
             float(a) / 255.0))

    for v in partDyes[const.DYES_INDEX_TEXTURE:4]:
        params.append(float(v))

    for v in partDyes[4:const.DYES_INDEX_DUAL_COLOR]:
        params.append('char/10000/pattern/pattern_%03d.tga' % int(float(v)))

    for v in partDyes[const.DYES_INDEX_DUAL_COLOR:const.DYES_INDEX_PBR_TEXTURE_DEGREE]:
        if ',' in v:
            r, g, b, a = _getRGBA(v)
            params.append('%f %f %f %f' % (float(r) / 255.0,
             float(g) / 255.0,
             float(b) / 255.0,
             float(a) / 255.0))

    for v in partDyes[const.DYES_INDEX_PBR_TEXTURE_DEGREE:]:
        params.append(float(v))

    gamelog.debug('getAvatarSkinParam', isPbr, partDyes)
    return params


def getAvatarEquipTransparenceParam(partDyes):
    params = []
    if not checkDyes(partDyes):
        partDyes = const.DEFAULT_DYES[0:const.DYES_INDEX_PBR_TEXTURE_DEGREE]
        params.append(0)
        params.append(0)
    else:
        params.append(1)
        if len(partDyes) < const.DYES_INDEX_DUAL_COLOR:
            params.append(0)
        else:
            params.append(1)
    l = len(partDyes)
    partDyes = list(partDyes) + const.DEFAULT_DYES[l:]
    v = partDyes[const.DYES_INDEX_COLOR]
    if ',' in v:
        r, g, b, a = _getRGBA(v)
        params.append('%f %f %f %f' % (float(r) / 255.0,
         float(g) / 255.0,
         float(b) / 255.0,
         float(a) / 255.0))
    v = partDyes[const.DYES_INDEX_DUAL_COLOR]
    if ',' in v:
        r, g, b, a = _getRGBA(v)
        params.append('%f %f %f %f' % (float(r) / 255.0,
         float(g) / 255.0,
         float(b) / 255.0,
         float(a) / 255.0))
    gamelog.debug('getAvatarEquipTransparenceParam', partDyes)
    return params


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


SPECULAR_COLOR_RATIO = 1.2
SPECULAR_COLOR_ALPHA = 380
SPECULAR_POWER = 5

def getHairColor(key, value, v1, p):
    if isinstance(value, tuple):
        values = value[0].split(',')
        if len(values) == 4:
            if len(value) == 2 and value[1] == 'faxing_color1':
                return (v1[0],
                 value[0],
                 value[0],
                 '%d' % SPECULAR_POWER)
            else:
                return (value[0],
                 v1[1],
                 v1[2],
                 '%d' % SPECULAR_POWER)
        else:
            index = int(values[0])
            value = p[0][2][index]
            value = (value,) + ('faxing_color1',)
            return getHairColor(key, value, v1, p)
    else:
        return value


DYE_DATA_CACHE = {}

def getDyeConfig(modelId, configName):
    configPath = 'char/%d/config/dye/%s.xml' % (modelId, configName)
    if DYE_DATA_CACHE.has_key(configPath):
        configs = DYE_DATA_CACHE.get(configPath)
        return configs
    dataInfo = ResMgr.openSection(configPath)
    if not dataInfo:
        DYE_DATA_CACHE[configPath] = None
        return
    configs = []
    for key in dataInfo.keys():
        if '#' in key:
            raise TypeError, 'Unknown format %s in %s' % (key, configPath)
        pLines = dataInfo[key].readStrings('p')
        v = dataInfo[key].readString('v')
        if not pLines:
            raise TypeError, 'Unknown format %s in %s' % (key, configPath)
        pp = []
        state = 0
        state_len = -1
        vv = []
        for pLine in pLines:
            ps = pLine.split('|')
            t = int(ps[0])
            if t == 1:
                if state == 2:
                    raise TypeError, 'Unknown format %s in %s' % (key, configPath)
                ops = [ int(s) for s in ps[2].split(';') if s != '' ]
                if len(ops) < 1:
                    raise TypeError, 'Unknown format %s in %s' % (key, configPath)
                if state_len == -1:
                    state_len = len(ops)
                elif state_len != len(ops):
                    raise TypeError, 'Unknown format %s in %s' % (key, configPath)
                pp.append((t, ps[1], tuple(ops)))
                vv.append(ops[int(v)])
                state = 1
            elif t == 2:
                if state == 2:
                    raise TypeError, 'Unknown format %s in %s' % (key, configPath)
                ops = []
                ss = ps[2].split(';')
                for s in ss:
                    if s != '':
                        try:
                            if ',' in s:
                                s1, s2, s3, s4 = s.split(',')
                                s = ','.join((s1.strip(),
                                 s2.strip(),
                                 s3.strip(),
                                 s4.strip()))
                            else:
                                s = '%.2f' % float(s)
                        except:
                            raise TypeError, 'Unknown format %s in %s' % (key, configPath)

                        ops.append(s)

                if len(ops) < 1:
                    raise TypeError, 'Unknown format %s in %s' % (key, configPath)
                if state_len == -1:
                    state_len = len(ops)
                elif state_len != len(ops):
                    raise TypeError, 'Unknown format %s in %s' % (key, configPath)
                pp.append((t, int(ps[1]), tuple(ops)))
                vv.append(ops[int(v)])
                state = 1
            elif t == 3:
                if state == 1:
                    raise TypeError, 'Unknown format %s in %s' % (key, configPath)
                ss = ps[2].split(';')
                if len(ss) < 2 or ss[0] == '' or ss[1] == '':
                    raise TypeError, 'Unknown format %s in %s' % (key, configPath)
                m1, m2 = float(ss[0]), float(ss[1])
                pp.append((t, int(ps[1]), (m1, m2)))
                vv.append(round(float(v), 2))
                state = 2
            else:
                raise TypeError, 'Unknown format %s in %s' % (key, configPath)

        pp = tuple(pp)
        vv = tuple(vv)
        if dataInfo[key].readBool('fusion'):
            if len(pp) > 1 or pp[0][0] != 1:
                raise TypeError, 'Unknown format %s in %s' % (key, configPath)
            configs.append((key + '#1', pp, vv))
            configs.append((key + '#2', pp, vv))
        else:
            configs.append((key, pp, vv))

    DYE_DATA_CACHE[configPath] = configs
    return configs


CONFIG_NAME = ('hair',
 'head',
 'eye',
 'skin',
 'eyelash')

def getDyeColor(sex, bodyType):
    from data import morpher_color_data as MCD
    ret = {}
    for uiName in MCD.data:
        ret[uiName] = []
        mcd = MCD.data[uiName]
        for data in mcd:
            if data.get('sex', 0) == sex:
                if data.has_key('bodyType') and data['bodyType'] == bodyType or not data.has_key('bodyType'):
                    color = data.get('color', ())
                    for x in color:
                        x = x.split(',')
                        x = [ (int(value) if int(value) <= 255 else 255) for value in x ]
                        ret[uiName].append((x[0] << 16) + (x[1] << 8) + x[2])

                    break

    return ret


def getDyeColorFromAvatar(avatar):
    physique = avatar.realPhysique
    return getDyeColor(physique.sex, physique.bodyType)


class PartDyeMorpher(object):

    def __init__(self, models, modelId, dummyModelId, configName, partData = [], applyLater = False):
        self.models = models
        self.modelId = modelId
        self.dummyModelId = dummyModelId
        self.key = configName + 'Dyes'
        self.partData = partData
        self.applyLater = applyLater
        self.transformMap = {}
        self.transformKey = []
        self.valid = False
        self.partApplyNum = 0
        configData = getDyeConfig(self.dummyModelId, configName)
        if configData is None:
            gamelog.error('b.e.:DyeMorpher: %d %s config data not found' % (self.dummyModelId, configName))
            return
        self.valid = True
        for k, pp, vv in configData:
            self.transformMap[k] = [pp, vv, vv]
            self.transformKey.append(k)

    def setMorph(self, transform, value, isRatio = True):
        if not self.hasMorph(transform):
            gamelog.error('b.e.:DyeMorpher: morph %s not found' % transform)
        else:
            if transform == 'hair_Color' and isinstance(value, tuple):
                p = self.transformMap[transform][0]
                v1 = self.transformMap[transform][1]
                value = getHairColor(transform, value, v1, p)
            self.__setValue(transform, value, isRatio)

    def hasMorph(self, transform):
        return self.transformMap.has_key(transform)

    def setAndApply(self, transform, value, isRatio = True, callback = None, loadImmediate = False):
        self.setMorph(transform, value, isRatio)
        self.apply(callback, loadImmediate)

    def applyNewSkin(self, callback = None, loadImmediate = False):
        if not self.valid:
            return
        gamelog.debug('bgf@PartDyeMorpher:apply0', self.partData)
        self.partApplyNum = 1
        for part, partValue, partDyes, matter, subMatter in self.partData:
            if not (partValue == None or partValue < 0):
                self.partApplyNum += 1
                if self.isTransparentModel(partValue, part):
                    self.partApplyNum += 1

        params = []
        for k in self.transformKey:
            pp, vv, _ = self.transformMap[k]
            for i in xrange(len(pp)):
                p = pp[i]
                v = vv[i]
                if p[0] == 2:
                    if ',' in v:
                        r, g, b, a = _getRGBA(v)
                        params.extend(['%f %f %f %f' % (float(r) / 255.0,
                          float(g) / 255.0,
                          float(b) / 255.0,
                          float(a) / 255.0)] * p[1])
                    else:
                        params.extend([float(v)] * p[1])
                else:
                    params.extend([v] * p[1])

        tints = ['avatarSkinBare', None]
        self.tintaltApply(tints, params, 'skin', None, self.applyLater, callback)
        for part, partValue, partDyes, matter, subMatter in self.partData:
            if partValue == None or partValue < 0:
                continue
            tints = ['avatarSkinEquip', 'avatarSkin']
            params = getAvatarSkinParam(partDyes)
            if tints[1]:
                TA.ta_del(self.models, tints[1], matter, False, self.applyLater)
            gamelog.debug('bgf@PartDyeMorpher:applyNewSkin', self.models, tints, params, matter, self.applyLater)
            if not loadImmediate:
                for texture in params:
                    texture = str(texture).strip()
                    if texture.endswith('.tga') or texture.endswith('.dds'):
                        for model in self.models:
                            model.addTintFxTexture(texture)

            self.tintaltApply(tints, params, matter, subMatter, self.applyLater, callback)
            gamelog.debug('bgf@PartDyeMorpher:applyNewSkin1', self.isTransparentModel(partValue, part), params, '%s2' % matter)
            if self.isTransparentModel(partValue, part):
                params = getAvatarEquipTransparenceParam(partDyes)
                self.tintaltApply([AVATAR_SKIN_TRANS_TINT, None], params, '%s2' % matter, None, self.applyLater, callback)
            else:
                TA.ta_del(self.models, AVATAR_SKIN_TRANS_TINT, '%s2' % matter, False, self.applyLater)

    def isNewSkinModel(self):
        if self.partData:
            bodyModelId = self.partData[0][1]
            modelId = charRes.transRealBodyType2(self.modelId, self.dummyModelId, bodyModelId)
            if self.key == 'skinDyes' and clientcom.isNewSkinModel(modelId, bodyModelId):
                return True
        return False

    def isTransparentModel(self, bodyModelId = 0, partType = ''):
        if self.partData:
            if partType not in TRANSPARENT_TYPE:
                bodyModelId = self.partData[0][1]
            modelId = charRes.transRealBodyType2(self.modelId, self.dummyModelId, bodyModelId)
            if self.key == 'skinDyes' and clientcom.isTransparentModel(modelId, bodyModelId):
                return True
        return False

    def apply(self, callback = None, loadImmediate = False):
        if self.isNewSkinModel():
            self.applyNewSkin(callback, loadImmediate)
            return
        if not self.valid:
            return
        gamelog.debug('bgf@PartDyeMorpher:apply0', self.partData)
        self.partApplyNum = 0
        for part, partValue, partDyes, matter, subMatter in self.partData:
            if not (partValue == None or partValue < 0):
                self.partApplyNum += 1

        for part, partValue, partDyes, matter, subMatter in self.partData:
            if partValue == None or partValue < 0:
                continue
            params = []
            tgaValue = None
            for k in self.transformKey:
                pp, vv, _ = self.transformMap[k]
                for i in xrange(len(pp)):
                    p = pp[i]
                    v = vv[i]
                    if p[0] == 1:
                        if '#' in k:
                            if tgaValue == None:
                                tgaValue = v
                            else:
                                params.append(self._getDyePartTexture(part, partValue, matter, p[1], tgaValue, v))
                                tgaValue = None
                        else:
                            params.append(self._getDyePartTexture(part, partValue, matter, p[1], v))
                    elif p[0] == 2:
                        if ',' in v:
                            r, g, b, a = _getRGBA(v)
                            params.extend(['%f %f %f %f' % (float(r) / 255.0,
                              float(g) / 255.0,
                              float(b) / 255.0,
                              float(a) / 255.0)] * p[1])
                        else:
                            params.extend([float(v)] * p[1])
                    else:
                        params.extend([v] * p[1])

            tints = list(getTintByMatter(self.modelId, part, matter))
            if tints[1]:
                TA.ta_del(self.models, tints[1], matter, False, self.applyLater)
            if tints[2] == AVATAR_SKIN_TRANS_TINT:
                TA.ta_del(self.models, tints[2], '%s2' % matter, False, self.applyLater)
            if tints[0] == 'avatarSkin':
                paramDyes = getAvatarSkinParam(partDyes)
                params.extend(paramDyes)
            gamelog.debug('bgf@PartDyeMorpher:apply', self.models, tints, params, matter, self.applyLater)
            if not loadImmediate:
                for texture in params:
                    texture = str(texture).strip()
                    if texture.endswith('.tga') or texture.endswith('.dds'):
                        for model in self.models:
                            model.addTintFxTexture(texture)

            self.tintaltApply(tints, params, matter, subMatter, self.applyLater, callback)

    def tintaltApply(self, tints, params, matter, subMatter, applyLater, callback):
        for model in self.models:
            if model.entityId > 0:
                entity = BigWorld.entities.get(model.entityId)
                if not entity or not entity.inWorld:
                    return

        TA.ta_add(self.models, tints[0], params, 0, matter, False, self.applyLater, tintType=TA.AVATARTINT)
        if subMatter:
            TA.ta_set_static(self.models, subMatter, matter, applyLater=True)
        else:
            TA.ta_set_static(self.models, 'Default', matter, applyLater=True)
        self.partApplyNum -= 1
        if self.partApplyNum == 0:
            if callback:
                callback()

    def _getDyePartTexture(self, part, partValue, matter, tga, tgaValue, fusionValue = 0):
        filePath = charRes.getPartTexturePath(self.modelId, part, partValue, matter, tga, tgaValue, False, None, fusionValue)
        return filePath

    def _fileExist(self, filePath):
        if not filePath:
            return False
        exists = True
        if not clientcom.isFileExist(filePath):
            if filePath.endswith('.tga') or filePath.endswith('.bmp'):
                ddsPath = filePath[:-4] + '.dds'
                if not clientcom.isFileExist(ddsPath):
                    exists = False
            else:
                exists = False
        if not exists:
            gamelog.error('b.e.:DyeMorpher: file does not exist:', filePath)
        return exists

    def __tostring(self, filterFunc = None):
        s = []
        for k in self.transformKey:
            _, vv, _ = self.transformMap[k]
            k = filterFunc(k) if filterFunc else k
            vv = [ str(v) for v in vv ]
            s.append('%s:%s' % (k, '|'.join(vv)))

        return '\n'.join(s)

    def __fromstring(self, s, isRatio = True, filterFunc = None):
        data = s.split('\n')
        dataDict = {}
        for i in data:
            li = i.split(':')
            if len(li) != 2:
                continue
            dataDict[li[0]] = li[1]

        for k, v in AMU.DYE_INDEX_COPY.iteritems():
            if dataDict.has_key(v) and not dataDict.has_key(k):
                dataDict[k] = dataDict[v]

        for i, v in dataDict.iteritems():
            k = filterFunc(i) if filterFunc else i[0]
            if self.hasMorph(k):
                self.__setValue(k, v, isRatio)
            else:
                gamelog.error('b.e.:DyeMorpher: bad morph name: ', k)

    def __setValue(self, transform, value, isRatio):
        v = self.transformMap[transform]
        gamelog.debug('PartDyeMorpher@__setValue', transform, value, isRatio, v)
        if v == None:
            return
        pp = v[0]
        vv = []
        try:
            if isRatio:
                if isinstance(value, tuple):
                    vv.extend(value)
                else:
                    for p in pp:
                        if p[0] == 1 or p[0] == 2:
                            r = min(max(int(value), 0), len(p[2]) - 1)
                            vv.append(p[2][r])
                        else:
                            r = p[2][0] + (p[2][1] - p[2][0]) * float(value)
                            vv.append(round(r, 2))

            else:
                rs = value.split('|')
                for i in xrange(len(pp)):
                    p = pp[i]
                    r = rs[i]
                    if p[0] == 1:
                        vv.append(int(r))
                    elif p[0] == 2:
                        if ',' in p[2][0]:
                            checkColorRange(self.key, transform, p[2], r, vv)
                        else:
                            vv.append('%.2f' % float(r))
                    else:
                        x = AMU.valueClip(round(float(r), 2), *p[2])
                        vv.append(x)

        except:
            gamelog.error('b.e.:DyeMorpher: morph %s value not match' % transform)
            return

        v[1] = tuple(vv)

    @staticmethod
    def getMorphRatio(v):
        pp = v[0]
        vv = v[1]
        p = pp[0]
        if p[0] == 1 or p[0] == 2:
            l = len(pp)
            for i in xrange(len(p[2])):
                for j in xrange(l):
                    r = True
                    if pp[j][2][i] != vv[j]:
                        r = False
                        break

                if r:
                    return i

            return 0
        else:
            d = p[2][1] - p[2][0]
            if d == 0.0:
                return 0.0
            return (float(vv[0]) - p[2][0]) / d

    @staticmethod
    def getMorphValue(v):
        vv = v[1]
        return vv

    def export(self, orig, filterFunc = None):
        sm = strmap.strmap(orig)
        sm.set(self.key, self.__tostring(filterFunc))
        sm.set('dyeMode', 1)
        return sm.__str__()

    def read(self, configMap, filterFunc = None):
        config = configMap.get(self.key, '')
        isRatio = configMap.get('dyeMode', 0) == 0
        self.__fromstring(config, isRatio, filterFunc)

    def resetAndApply(self, callback = None, loadImmediate = False):
        for k in self.transformKey:
            v = self.transformMap[k]
            v[1] = v[2]

        self.apply(callback, loadImmediate)

    def exportTintInfo(self):
        ret = []
        if not self.valid:
            return ret
        for part, partValue, partDyes, matter, subMatter in self.partData:
            if partValue == None:
                continue
            params = []
            tgaValue = None
            for k in self.transformKey:
                pp, vv, _ = self.transformMap[k]
                for i in xrange(len(pp)):
                    p = pp[i]
                    v = vv[i]
                    if p[0] == 1:
                        if '#' in k:
                            if tgaValue == None:
                                tgaValue = v
                            else:
                                params.append(self._getDyePartTexture(part, partValue, matter, p[1], tgaValue, v))
                                tgaValue = None
                        else:
                            params.append(self._getDyePartTexture(part, partValue, matter, p[1], v))
                    elif p[0] == 2:
                        if ',' in v:
                            r, g, b, a = _getRGBA(v)
                            params.extend(['%f %f %f %f' % (float(r) / 255.0,
                              float(g) / 255.0,
                              float(b) / 255.0,
                              float(a) / 255.0)] * p[1])
                        else:
                            params.extend([float(v)] * p[1])
                    else:
                        params.extend([v] * p[1])

            tints = list(getTintByMatter(self.modelId, part, matter))
            if tints[1]:
                TA.ta_del(self.models, tints[1], matter, False, self.applyLater)
            if tints[0] == 'avatarSkin':
                paramDyes = getAvatarSkinParam(partDyes)
                params.extend(paramDyes)
            ret.append((tints[0], params, matter))

        return ret

    def getRandomValue(self, transform):
        if self.hasMorph(transform):
            v = self.transformMap[transform]
            p = v[0][0]
            if p[0] == 1 or p[0] == 2:
                return random.randint(0, len(p[2]) - 1)
            else:
                return random.random()
        return 0


class DyeMorpher(object):

    def __init__(self, model, modelId, dummyModelId, face, hair, head, body, hand, leg, shoe, headType = 0, dyesDict = None, mattersDict = None, cape = None):
        self.models = [model]
        self.modelId = modelId
        self.dummyModelId = dummyModelId
        headDyes = dyesDict.get('head') if dyesDict and head is not None else None
        bodyDyes = dyesDict.get('body') if dyesDict and body is not None else None
        handDyes = dyesDict.get('hand') if dyesDict and hand is not None else None
        legDyes = dyesDict.get('leg') if dyesDict and leg is not None else None
        shoeDyes = dyesDict.get('shoe') if dyesDict and shoe is not None else None
        capeDyes = dyesDict.get('cape') if dyesDict and cape is not None else None
        bodyMatter = mattersDict.get('body', None) if mattersDict and body is not None else None
        handMatter = mattersDict.get('hand', None) if mattersDict and hand is not None else None
        legMatter = mattersDict.get('leg', None) if mattersDict and leg is not None else None
        shoeMatter = mattersDict.get('shoe', None) if mattersDict and shoe is not None else None
        capeMatter = mattersDict.get('cape', None) if mattersDict and cape is not None else None
        self.partApplyNum = 0
        skinPartData = [('body',
          body,
          bodyDyes,
          'body',
          bodyMatter), ('hand',
          hand,
          handDyes,
          'hand',
          handMatter), ('leg',
          leg,
          legDyes,
          'leg',
          legMatter)]
        skinPartData.append(('shoe',
         shoe,
         shoeDyes,
         'shoe',
         shoeMatter))
        skinPartData.append(('cape',
         cape,
         capeDyes,
         'cape',
         capeMatter))
        self.dyeMorphers = {}
        self.dyeMorpherKeys = []
        if headType in (charRes.HEAD_TYPE0, charRes.HEAD_TYPE2):
            self.dyeMorphers['head'] = PartDyeMorpher(self.models, self.modelId, self.dummyModelId, 'head', [('head',
              face,
              None,
              'head',
              None)], True)
            self.dyeMorpherKeys.append('head')
            self.dyeMorphers['eye'] = PartDyeMorpher(self.models, self.modelId, self.dummyModelId, 'eye', [('head',
              face,
              None,
              'eye',
              None)], True)
            self.dyeMorpherKeys.append('eye')
            self.dyeMorphers['hair'] = PartDyeMorpher(self.models, self.modelId, self.dummyModelId, 'hair', [('hair',
              hair,
              None,
              'hair',
              None)], True)
            self.dyeMorpherKeys.append('hair')
            self.dyeMorphers['eyelash'] = PartDyeMorpher(self.models, self.modelId, self.dummyModelId, 'eyelash', [('head',
              face,
              None,
              'eyelash',
              None)], True)
            self.dyeMorpherKeys.append('eyelash')
            if headType == charRes.HEAD_TYPE2:
                skinPartData.append(('',
                 hair,
                 headDyes,
                 'hairDye',
                 None))
        self.dyeMorphers['skin'] = PartDyeMorpher(self.models, self.modelId, self.dummyModelId, 'skin', skinPartData, True)
        self.dyeMorpherKeys.append('skin')

    def setMorph(self, matters, transform, value, isRatio = True):
        if not matters:
            for key in self.dyeMorpherKeys:
                dyeMorpher = self.dyeMorphers[key]
                dyeMorpher.setMorph(transform, value, isRatio)

        else:
            for matter in matters:
                dyeMorpher = self.dyeMorphers.get(matter)
                if dyeMorpher:
                    dyeMorpher.setMorph(transform, value, isRatio)

    def setAndApply(self, matters, transform, value, isRatio = True):
        if not matters:
            self.partApplyNum = len(self.dyeMorpherKeys)
            for key in self.dyeMorpherKeys:
                dyeMorpher = self.dyeMorphers[key]
                dyeMorpher.setAndApply(transform, value, isRatio, Functor(self.realApply, self.models))

        else:
            self.partApplyNum = len(matters)
            for matter in matters:
                dyeMorpher = self.dyeMorphers.get(matter)
                if dyeMorpher:
                    dyeMorpher.setAndApply(transform, value, isRatio, Functor(self.realApply, self.models))
                else:
                    self.partApplyNum -= 1

    def getRandomValue(self, matters, transform):
        if not matters:
            return 0
        for matter in matters:
            dyeMorpher = self.dyeMorphers.get(matter)
            if dyeMorpher:
                return dyeMorpher.getRandomValue(transform)

        return 0

    def realApply(self, models):
        self.partApplyNum -= 1
        if self.partApplyNum == 0:
            TA.ta_apply(models)

    def apply(self, matters = None, loadImmediate = False):
        if not matters:
            self.partApplyNum = len(self.dyeMorpherKeys)
            for key in self.dyeMorpherKeys:
                dyeMorpher = self.dyeMorphers[key]
                if not dyeMorpher.valid:
                    self.partApplyNum -= 1
                else:
                    dyeMorpher.apply(Functor(self.realApply, self.models), loadImmediate)

        else:
            self.partApplyNum = len(matters)
            for matter in matters:
                dyeMorpher = self.dyeMorphers.get(matter)
                if dyeMorpher:
                    dyeMorpher.apply(Functor(self.realApply, self.models), loadImmediate)
                else:
                    self.partApplyNum -= 1

    def export(self, orig, filterFunc = None):
        sm = strmap.strmap(orig)
        for key in self.dyeMorpherKeys:
            dyeMorpher = self.dyeMorphers[key]
            sm.set(dyeMorpher.key, dyeMorpher._PartDyeMorpher__tostring(filterFunc))

        sm.set('dyeMode', 1)
        return sm.__str__()

    def read(self, configMap, filterFunc = None):
        isRatio = configMap.get('dyeMode', 0) == 0
        for key in self.dyeMorpherKeys:
            dyeMorpher = self.dyeMorphers[key]
            config = configMap.get(dyeMorpher.key, '')
            dyeMorpher._PartDyeMorpher__fromstring(config, isRatio, filterFunc)

    def resetAndApply(self):
        self.partApplyNum = len(self.dyeMorpherKeys)
        for key in self.dyeMorpherKeys:
            dyeMorpher = self.dyeMorphers[key]
            dyeMorpher.resetAndApply(Functor(self.realApply, self.models))

    def exportTintInfo(self):
        ret = {}
        for key in self.dyeMorpherKeys:
            dyeMorpher = self.dyeMorphers[key]
            ret[key] = dyeMorpher.exportTintInfo()

        return ret


class BuildPartDyeMorpher(object):

    def __init__(self, modelId, dummyModelId, configName, partData = []):
        self.modelId = modelId
        self.dummyModelId = dummyModelId
        self.key = configName + 'Dyes'
        self.partData = partData
        self.transformMap = {}
        self.transformKey = []
        self.matterTintMap = {}
        self.valid = False
        configData = getDyeConfig(self.dummyModelId, configName)
        if configData is None:
            return
        self.valid = True
        for k, pp, vv in configData:
            self.transformMap[k] = [pp, vv, vv]
            self.transformKey.append(k)

    def _getDyePartTexture(self, part, partValue, matter, tga, tgaValue, fusionValue = 0):
        filePath = charRes.getPartTexturePath(self.modelId, part, partValue, matter, tga, tgaValue, False, None, fusionValue)
        return filePath

    def __setValue(self, transform, value, isRatio):
        v = self.transformMap[transform]
        if v == None:
            return
        pp = v[0]
        vv = []
        try:
            if isRatio:
                for p in pp:
                    if isinstance(value, str) and value[0:6] == 'color#' and p[0] == 2:
                        vv.append(value[6:])
                    elif p[0] == 1 or p[0] == 2:
                        r = min(max(int(value), 0), len(p[2]) - 1)
                        vv.append(p[2][r])
                    else:
                        r = p[2][0] + (p[2][1] - p[2][0]) * float(value)
                        vv.append(round(r, 2))

            else:
                rs = value.split('|')
                for i in xrange(len(pp)):
                    p = pp[i]
                    r = rs[i]
                    if p[0] == 1:
                        vv.append(int(r))
                    elif p[0] == 2:
                        if ',' in p[2][0]:
                            checkColorRange(self.key, transform, p[2], r, vv)
                        else:
                            vv.append('%.2f' % float(r))
                    else:
                        x = AMU.valueClip(round(float(r), 2), *p[2])
                        vv.append(x)

        except:
            gamelog.error('b.e.:DyeMorpher: morph %s value not match' % transform)
            return

        v[1] = tuple(vv)

    def __fromstring(self, s, isRatio = True, filterFunc = None):
        data = s.split('\n')
        dataDict = {}
        for i in data:
            li = i.split(':')
            if len(li) != 2:
                continue
            dataDict[li[0]] = li[1]

        for k, v in AMU.DYE_INDEX_COPY.iteritems():
            if dataDict.has_key(v) and not dataDict.has_key(k):
                dataDict[k] = dataDict[v]

        for i, v in dataDict.iteritems():
            k = filterFunc(i) if filterFunc else i[0]
            if self.hasMorph(k):
                self.__setValue(k, v, isRatio)
            else:
                gamelog.error('b.e.:DyeMorpher: bad morph name: ', k)

    def hasMorph(self, transform):
        return self.transformMap.has_key(transform)

    def buildDynamicTintNewSkin(self, tintSection = None, tintAvtarName = None):
        if not self.valid:
            return
        self.matterTintMap = {}
        params = []
        for k in self.transformKey:
            pp, vv, init_vv = self.transformMap[k]
            for i in xrange(len(pp)):
                p = pp[i]
                try:
                    v = vv[i]
                except:
                    v = init_vv[i]

                if p[0] == 2:
                    if ',' in v:
                        r, g, b, a = _getRGBA(v)
                        params.extend(['%f %f %f %f' % (float(r) / 255.0,
                          float(g) / 255.0,
                          float(b) / 255.0,
                          float(a) / 255.0)] * p[1])
                    else:
                        params.extend([float(v)] * p[1])
                else:
                    params.extend([v] * p[1])

        tint = 'avatarSkinBare'
        if not params:
            content = TA.TAs[tint][1]
        else:
            if tintSection and tintSection.get('skin', None) and tintAvtarName and tintAvtarName.get('skin') == 'avatarSkinBare':
                content = tintSection.get('skin', None)
            else:
                content = ResMgr.createXMLSectionFromString('ta', '<ta></ta>')
                content.copy(TA.TAs[tint][1])
            try:
                TA.parse_tint_with_params(content, params)
            except Exception as e:
                reportException(tintSection, tint, self.modelId, self.dummyModelId, 'skin', 0, content, params, e)

        static = 'staticDefault'
        staticTintName = TA.build_tint_name(content, static)
        self.matterTintMap['skin'] = (staticTintName, tint, params)
        for part, partValue, partDyes, matter, subMatter in self.partData:
            if partValue == None or partValue < 0:
                continue
            params = getAvatarSkinParam(partDyes)
            content = None
            tint = 'avatarSkinEquip'
            if not params:
                content = TA.TAs[tint][1]
            else:
                if tintSection and tintSection.get(matter, None) and tintAvtarName and tintAvtarName.get(matter) == 'avatarSkinEquip':
                    content = tintSection.get(matter, None)
                else:
                    content = ResMgr.createXMLSectionFromString('ta', '<ta></ta>')
                    content.copy(TA.TAs[tint][1])
                try:
                    TA.parse_tint_with_params(content, params)
                except Exception as e:
                    reportException(tintSection, tint, self.modelId, self.dummyModelId, part, partValue, content, params, e)

            static = 'staticDefault'
            if subMatter:
                static = subMatter
            staticTintName = TA.build_tint_name(content, static)
            self.matterTintMap[matter] = (staticTintName, tint, params)
            if self.isTransparentModel(partValue, part):
                matter = '%s2' % matter
                params = getAvatarEquipTransparenceParam(partDyes)
                content = None
                tint = AVATAR_SKIN_TRANS_TINT
                if not params:
                    content = TA.TAs[tint][1]
                else:
                    if tintSection and tintSection.get(matter, None):
                        content = tintSection.get(matter, None)
                    else:
                        content = ResMgr.createXMLSectionFromString('ta', '<ta></ta>')
                        content.copy(TA.TAs[tint][1])
                    try:
                        TA.parse_tint_with_params(content, params)
                    except Exception as e:
                        reportException(tintSection, tint, self.modelId, self.dummyModelId, part, partValue, content, params, e)

                static = 'staticDefault'
                staticTintName = TA.build_tint_name(content, static)
                self.matterTintMap[matter] = (staticTintName, tint, params)

    def isNewSkinModel(self):
        if self.partData:
            bodyModelId = self.partData[0][1]
            modelId = charRes.transRealBodyType2(self.modelId, self.dummyModelId, bodyModelId)
            if self.key == 'skinDyes' and clientcom.isNewSkinModel(modelId, bodyModelId):
                return True
        return False

    def isTransparentModel(self, bodyModelId = 0, partType = ''):
        if self.partData:
            if partType not in TRANSPARENT_TYPE:
                bodyModelId = self.partData[0][1]
            modelId = charRes.transRealBodyType2(self.modelId, self.dummyModelId, bodyModelId)
            if self.key == 'skinDyes' and clientcom.isTransparentModel(modelId, bodyModelId):
                return True
        return False

    def buildDynamicTint(self, tintSection = None, tintAvtarName = None):
        if self.isNewSkinModel():
            self.buildDynamicTintNewSkin(tintSection, tintAvtarName)
            return
        if not self.valid:
            return
        self.matterTintMap = {}
        for part, partValue, partDyes, matter, subMatter in self.partData:
            if partValue == None or partValue < 0:
                continue
            params = []
            tgaValue = None
            for k in self.transformKey:
                pp, vv, init_vv = self.transformMap[k]
                for i in xrange(len(pp)):
                    p = pp[i]
                    try:
                        v = vv[i]
                    except:
                        v = init_vv[i]

                    if p[0] == 1:
                        if '#' in k:
                            if tgaValue == None:
                                tgaValue = v
                            else:
                                params.append(self._getDyePartTexture(part, partValue, matter, p[1], tgaValue, v))
                                tgaValue = None
                        else:
                            params.append(self._getDyePartTexture(part, partValue, matter, p[1], v))
                    elif p[0] == 2:
                        if ',' in v:
                            r, g, b, a = _getRGBA(v)
                            params.extend(['%f %f %f %f' % (float(r) / 255.0,
                              float(g) / 255.0,
                              float(b) / 255.0,
                              float(a) / 255.0)] * p[1])
                        else:
                            params.extend([float(v)] * p[1])
                    else:
                        params.extend([v] * p[1])

            tints = list(getTintByMatter(self.modelId, part, matter))
            if tints[0] == 'avatarSkin':
                paramDyes = getAvatarSkinParam(partDyes)
                params.extend(paramDyes)
            content = None
            tint = tints[0]
            if not params:
                content = TA.TAs[tint][1]
            else:
                if tintSection and tintSection.get(matter, None) and tintAvtarName and tintAvtarName.get(matter) == 'avatarSkin':
                    content = tintSection.get(matter, None)
                else:
                    content = ResMgr.createXMLSectionFromString('ta', '<ta></ta>')
                    content.copy(TA.TAs[tint][1])
                try:
                    TA.parse_tint_with_params(content, params)
                except Exception as e:
                    reportException(tintSection, tint, self.modelId, self.dummyModelId, part, partValue, content, params, e)

            static = 'staticDefault'
            if subMatter:
                static = subMatter
            staticTintName = TA.build_tint_name(content, static)
            self.matterTintMap[matter] = (staticTintName, tint, params)


class BuildDyeMorpher(object):

    def __init__(self, modelId, dummyModelId, face, hair, head, body, hand, leg, shoe, headType, dyesDict = None, mattersDict = None, entityId = 0, cape = None):
        self.modelId = modelId
        self.dummyModelId = dummyModelId
        self.entityId = entityId
        headDyes = dyesDict.get('head') if dyesDict and head is not None else None
        bodyDyes = dyesDict.get('body') if dyesDict and body is not None else None
        handDyes = dyesDict.get('hand') if dyesDict and hand is not None else None
        legDyes = dyesDict.get('leg') if dyesDict and leg is not None else None
        shoeDyes = dyesDict.get('shoe') if dyesDict and shoe is not None else None
        capeDyes = dyesDict.get('cape') if dyesDict and cape is not None else None
        bodyMatter = mattersDict.get('body', None) if mattersDict and body is not None else None
        handMatter = mattersDict.get('hand', None) if mattersDict and hand is not None else None
        legMatter = mattersDict.get('leg', None) if mattersDict and leg is not None else None
        shoeMatter = mattersDict.get('shoe', None) if mattersDict and shoe is not None else None
        capeMatter = mattersDict.get('cape', None) if mattersDict and cape is not None else None
        skinPartData = [('body',
          body,
          bodyDyes,
          'body',
          bodyMatter), ('hand',
          hand,
          handDyes,
          'hand',
          handMatter), ('leg',
          leg,
          legDyes,
          'leg',
          legMatter)]
        skinPartData.append(('shoe',
         shoe,
         shoeDyes,
         'shoe',
         shoeMatter))
        skinPartData.append(('cape',
         cape,
         capeDyes,
         'cape',
         capeMatter))
        self.matterDyes = []
        self.dyeMorpherKeys = []
        self.dyeMorphers = {}
        if headType in (charRes.HEAD_TYPE0, charRes.HEAD_TYPE2):
            self.dyeMorphers['head'] = BuildPartDyeMorpher(self.modelId, self.dummyModelId, 'head', [('head',
              face,
              None,
              'head',
              None)])
            self.dyeMorpherKeys.append('head')
            self.dyeMorphers['eye'] = BuildPartDyeMorpher(self.modelId, self.dummyModelId, 'eye', [('head',
              face,
              None,
              'eye',
              None)])
            self.dyeMorpherKeys.append('eye')
            self.dyeMorphers['hair'] = BuildPartDyeMorpher(self.modelId, self.dummyModelId, 'hair', [('hair',
              hair,
              None,
              'hair',
              None)])
            self.dyeMorpherKeys.append('hair')
            self.dyeMorphers['eyelash'] = BuildPartDyeMorpher(self.modelId, self.dummyModelId, 'eyelash', [('head',
              face,
              None,
              'eyelash',
              None)])
            self.dyeMorpherKeys.append('eyelash')
            if headType == charRes.HEAD_TYPE2:
                skinPartData.append(('',
                 hair,
                 headDyes,
                 'hairDye',
                 None))
        self.dyeMorphers['skin'] = BuildPartDyeMorpher(self.modelId, self.dummyModelId, 'skin', skinPartData)
        self.dyeMorpherKeys.append('skin')

    def readConfig(self, config):
        configMap = strmap.strmap(config)
        self._read(configMap, lambda v: AMU.getMorpherByIdx(v))

    def _read(self, configMap, filterFunc = None):
        isRatio = configMap.get('dyeMode', 0) == 0
        for key in self.dyeMorpherKeys:
            dyeMorpher = self.dyeMorphers[key]
            config = configMap.get(dyeMorpher.key, '')
            dyeMorpher._BuildPartDyeMorpher__fromstring(config, isRatio, filterFunc)

    def buildDynamicTintAll(self):
        self.matterDyes = []
        entity = BigWorld.entities.get(self.entityId)
        tintEffects = {}
        tintAvtarName = {}
        if entity:
            tintEffects = entity.tintAvatarTas
            tintAvtarName = entity.tintAvatarName
        for matter in self.dyeMorphers:
            self.dyeMorphers[matter].buildDynamicTint(tintEffects, tintAvtarName)
            for key in self.dyeMorphers[matter].matterTintMap:
                self.matterDyes.append((key,
                 self.dyeMorphers[matter].matterTintMap[key][0],
                 self.dyeMorphers[matter].matterTintMap[key][1],
                 self.dyeMorphers[matter].matterTintMap[key][2]))

        if entity:
            entity.tintAvatarTas = {}
            entity.tintAvatarName = {}


def reportException(tintSection, tint, modelId, dummyModelId, part, partValue, content, params, e):
    if tintSection:
        tintSection = tintSection.keys()
    contentLen = 0
    if content:
        contentLen = len(content.keys())
    msg = 'buildDynamicTint error  %s %s %d %d %s %d %d %s' % (str(tintSection),
     tint,
     modelId,
     dummyModelId,
     part,
     partValue,
     contentLen,
     str(params))
    msg += e.message[:500]
    clientUtils.reportEngineException(msg)


class HairDyeMorpher(object):
    MATTER = 'hairDye'
    TINT_NAME = 'avatarSkinEquip'

    def __init__(self, model):
        super(HairDyeMorpher, self).__init__()
        self.model = model
        self.param = []
        self.subMatter = None

    def read(self, config, subMatter = None):
        self.param = config
        self.subMatter = subMatter

    def apply(self):
        if not self.model:
            return
        params = getAvatarSkinParam(self.param)
        if self.subMatter:
            TA.ta_set_static([self.model], self.subMatter, None, applyLater=True)
        TA.addExtraTint(self.model, self.TINT_NAME, params, 0, self.MATTER)

    def getDynamicTint(self, tintSection = None):
        params = getAvatarSkinParam(self.param)
        content = None
        if tintSection:
            content = tintSection.get(self.MATTER, None)
        else:
            content = ResMgr.createXMLSectionFromString('ta', '<ta></ta>')
            content.copy(TA.TAs[self.TINT_NAME][1])
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
         self.TINT_NAME,
         params)


class CommonDyeMorpher(object):

    def __init__(self, matter, tint):
        super(CommonDyeMorpher, self).__init__()
        self.model = None
        self.param = []
        self.matterName = matter
        self.tintName = tint

    def read(self, config):
        self.param = self.calParam(config)

    def setModel(self, model):
        self.model = model

    def apply(self):
        if self.model and self.param and self.tintName:
            TA.addExtraTint(self.model, self.tintName, self.param, 0, self.matterName)

    def getDynamicTint(self, tintSection = None):
        content = None
        if tintSection:
            content = tintSection.get(self.matterName, None)
        else:
            content = ResMgr.createXMLSectionFromString('ta', '<ta></ta>')
            content.copy(TA.TAs[self.tintName][1])
        try:
            TA.parse_tint_with_params(content, self.param)
        except:
            return

        static = 'staticDefault'
        staticTintName = TA.build_tint_name(content, static)
        return (self.matterName,
         staticTintName,
         self.tintName,
         self.param)

    def calParam(self, param):
        return param


class FurnitureDyeMorpher(CommonDyeMorpher):

    def __init__(self, matter = 'furnitureLight', tint = 'furnitureLight'):
        super(FurnitureDyeMorpher, self).__init__(matter, tint)

    def calParam(self, param):
        ret = []
        if param:
            color = param[0]
            r, g, b, a = _getRGBA(color)
            ret.append('%f %f %f %f' % (float(r) / 255.0,
             float(g) / 255.0,
             float(b) / 255.0,
             float(a) / 255.0))
            ret.append(float(param[1]))
        return ret
