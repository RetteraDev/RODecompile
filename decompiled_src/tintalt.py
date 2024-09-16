#Embedded file name: /WORKSPACE/data/entities/client/helpers/tintalt.o
import ResMgr
import BigWorld
import gamelog
import gameglobal
import clientUtils
import clientcom
from callbackHelper import Functor
from data import tintMap_client_data as TMCD
from data import sys_config_data as SYSCD
UNKNOWTINT = 0
HITTINT = 1
STATETINT = 2
DIETINT = 3
BORNTINT = 4
SKILLTINT = 5
AVATARTINT = 6
NPC_LINGSHI = 7
taNameSerialId = 0
MAX_CONTENT_CACHESIZE = 150
TA_MAX_CACHESIZE = 200
TINT_NOUSE = 0
TINT_SCRIPTUSE = 2

def getTintName(tintType):
    data = TMCD.data.get(tintType, None)
    tintName = ''
    if data:
        tintName = data.get('tintName', '')
    return tintName


TAs = {}
gShaderList = []
isInited = False
TINT_COPYT_PARAM_DICT = {}

def checkTintCanReuse(tint, params):
    global TINT_COPYT_PARAM_DICT
    oldParams = TINT_COPYT_PARAM_DICT.get(tint, None)
    if not oldParams:
        TINT_COPYT_PARAM_DICT[tint] = params
        return True
    if oldParams == params:
        return True
    return False


def clearTintCopy(tintCopy):
    tints = []
    if tintCopy:
        tints = tintCopy.values()
    for tint in tints:
        if TINT_COPYT_PARAM_DICT.has_key(tint):
            TINT_COPYT_PARAM_DICT.pop(tint)


def preloadTAs():
    global isInited
    global gShaderList
    if isInited:
        return
    isInited = True
    tree = ResMgr.openSection('effect/tintalt/list.xml')
    shaderTree = ResMgr.openSection('shaders/list.xml')
    if tree == None:
        gamelog.error('effect/tintalt/list.xml not found')
        return
    key = 'effectFile'
    allEffectfileName = tree.readStrings(key)
    allShaders = shaderTree.readStrings('fx')
    for shaderName in allShaders:
        gShaderList.append(shaderName.strip().lower())

    for effectfileName in allEffectfileName:
        effectfilePath = 'effect/tintalt/' + effectfileName + '.xml'
        tree = ResMgr.openSection(effectfilePath)
        if tree == None:
            gamelog.error(effectfilePath + ' not found')
            continue
        boolvalue = tree.readString('Bool')
        if boolvalue == 'False':
            boolvalue = False
        else:
            boolvalue = True
        tas = tree.openSection('Value').openSection('ta')
        TAs[effectfileName] = [boolvalue, tas]


preloadTAs()

class TintEffectCounterMgr(object):
    MAX_TINT_EFFECT_COUNT = 30

    def __init__(self):
        self.tintTintCount = 0

    def inc(self, tintType = UNKNOWTINT):
        if tintType in [SKILLTINT, STATETINT]:
            self.tintTintCount += 1

    def dec(self, tintType = UNKNOWTINT):
        if tintType in [SKILLTINT, STATETINT]:
            self.tintTintCount -= 1

    def canAddState(self, tintType = UNKNOWTINT):
        if tintType in [SKILLTINT, STATETINT]:
            return self.tintTintCount < self.MAX_TINT_EFFECT_COUNT
        return True

    def countReset(self):
        self.tintTintCount = 0


gTintEffectCounterMgr = TintEffectCounterMgr()
ModelMatterFXNameMap = {}
ModelFxNameDict = {}

def getFXName(model, matter):
    global ModelMatterFXNameMap
    global ModelFxNameDict
    fxName = None
    if len(ModelMatterFXNameMap) > TA_MAX_CACHESIZE:
        ModelMatterFXNameMap.clear()
    if len(ModelFxNameDict) > TA_MAX_CACHESIZE:
        ModelFxNameDict.clear()
    if model.inWorld:
        if getattr(model, 'newFxName', None) and model and model.sources[0].find(matter) != -1:
            fxName = model.newFxName
            return fxName
        if ModelMatterFXNameMap.has_key(model.sources):
            for values in ModelMatterFXNameMap[model.sources]:
                if values.has_key(matter):
                    return values[matter]

        fxDict = {}
        if ModelFxNameDict.has_key(model.sources):
            fxDict = ModelFxNameDict[model.sources]
        else:
            fxDict = model.fxNameDict()
            ModelFxNameDict[model.sources] = fxDict
        if fxDict.has_key(matter):
            fx = model.fxNameDict()[matter]
        else:
            key = fxDict.keys()[0]
            fx = fxDict[key]
        fxStrs = fx.split('/')
        fxName = fxStrs[len(fxStrs) - 1]
        fxNameStrs = fxName.split('.')
        fxName = fxNameStrs[0]
        if ModelMatterFXNameMap.has_key(model.sources):
            ModelMatterFXNameMap[model.sources].append({matter: fxName})
        else:
            ModelMatterFXNameMap[model.sources] = [{matter: fxName}]
    return fxName


_MODEL_STATE_MAP = {}
_PARSE_TA_MAP = {}
_PARSE_TEXTURE_MAP = {}

def _del_model(model):
    if not model:
        return
    serialId = model.serialId
    if serialId in _MODEL_STATE_MAP:
        mo = _MODEL_STATE_MAP[serialId]
        for matter in mo:
            tintLast = mo[matter].get('last', None)
            if tintLast:
                BigWorld.setContentStateByScript(tintLast, TINT_NOUSE)
            tintStatic = mo[matter].get('static', None)
            if tintStatic:
                BigWorld.setContentStateByScript(tintStatic, TINT_NOUSE)
            tintDefault = mo[matter].get('default', None)
            if tintDefault:
                BigWorld.setContentStateByScript(tintDefault, TINT_NOUSE)

        del _MODEL_STATE_MAP[serialId]


def _add_state(model, tint, params, matter = None):
    if not model:
        return
    if not model.getMatterList():
        return
    if matter is None:
        for k, v in model.getMatterList():
            if k == 'empty':
                continue
            _add_state(model, tint, params, k)

        return
    if tint.find('gaoLiang') != -1 or tint.find('xuanren') != -1 or tint.find('addColor') != -1 or tint.find('yuan') != -1 or tint.find('rongGuang') != -1 or tint.find('cfmianban') != -1 or tint.find('cmianban') != -1 or tint.find('fmianban') != -1 or tint.find('emotionHead') != -1:
        fxName = getFXName(model, matter)
        newParams = []
        newParams.append(fxName)
        for param in params:
            newParams.append(param)

        params = newParams
    serialId = model.serialId
    if serialId not in _MODEL_STATE_MAP:
        _MODEL_STATE_MAP[serialId] = {}
    mo = _MODEL_STATE_MAP[serialId]
    if matter not in mo:
        mo[matter] = {}
    ma = mo[matter]
    if 'tas' not in ma:
        ma['tas'] = {}
    if TAs[tint][0]:
        if ma.get('default') == tint and str(ma['tas'].get(tint)) == str(params):
            ma['changed'] = False
        else:
            ma['changed'] = True
            ma['default'] = tint
            ma['tas'][tint] = params
    else:
        if 'state' not in ma:
            ma['state'] = set()
        if tint in ma['state'] and str(ma['tas'].get(tint)) == str(params):
            ma['changed'] = False
        else:
            ma['changed'] = True
            ma['state'].add(tint)
            ma['tas'][tint] = params


def _del_state(model, tint, matter = None):
    if not model:
        return
    if not model.getMatterList():
        return
    if matter is None:
        for k, v in model.getMatterList():
            if k == 'empty':
                continue
            _del_state(model, tint, k)

        return
    serialId = model.serialId
    if serialId not in _MODEL_STATE_MAP:
        return
    mo = _MODEL_STATE_MAP[serialId]
    if matter not in mo:
        return
    ma = mo[matter]
    if 'tas' in ma:
        if tint in ma['tas']:
            del ma['tas'][tint]
    if TAs.has_key(tint):
        if TAs[tint][0]:
            if 'default' not in ma:
                ma['changed'] = False
                return
            if ma['default'] != tint:
                ma['changed'] = False
                return
            ma['changed'] = True
            del ma['default']
        else:
            if 'state' not in ma:
                ma['changed'] = False
                return
            if tint not in ma['state']:
                ma['changed'] = False
                return
            ma['changed'] = True
            ma['state'].remove(tint)


def _get_def_state(model, matter):
    if not model:
        return
    serialId = model.serialId
    if serialId in _MODEL_STATE_MAP:
        if matter in _MODEL_STATE_MAP[serialId]:
            if 'default' in _MODEL_STATE_MAP[serialId][matter]:
                return _MODEL_STATE_MAP[serialId][matter]['default']
    return ''


def _get_state(model, matter):
    if not model:
        return
    serialId = model.serialId
    if serialId in _MODEL_STATE_MAP:
        if matter in _MODEL_STATE_MAP[serialId]:
            if 'state' in _MODEL_STATE_MAP[serialId][matter]:
                return _MODEL_STATE_MAP[serialId][matter]['state']
    return set()


def _get_static_state(model, matter):
    if not model:
        return
    serialId = model.serialId
    if serialId in _MODEL_STATE_MAP:
        if matter in _MODEL_STATE_MAP[serialId]:
            if 'static' in _MODEL_STATE_MAP[serialId][matter]:
                return _MODEL_STATE_MAP[serialId][matter]['static']
    return 'Default'


def _get_state_changed(model, matter):
    if not model:
        return False
    serialId = model.serialId
    if serialId in _MODEL_STATE_MAP:
        if matter in _MODEL_STATE_MAP[serialId]:
            if 'changed' in _MODEL_STATE_MAP[serialId][matter]:
                return _MODEL_STATE_MAP[serialId][matter]['changed']
    return False


def _set_matter_tint_name(model, matter, tintName):
    if not model:
        return
    serialId = model.serialId
    if serialId in _MODEL_STATE_MAP:
        if matter in _MODEL_STATE_MAP[serialId]:
            tintLast = _MODEL_STATE_MAP[serialId][matter].get('last', None)
            if tintLast:
                BigWorld.setContentStateByScript(tintLast, TINT_NOUSE)
            _MODEL_STATE_MAP[serialId][matter]['last'] = tintName
            if tintName:
                BigWorld.setContentStateByScript(tintName, TINT_SCRIPTUSE)


def _get_matter_tint_data(model, matters = None):
    tint_data = []
    if not model:
        return tint_data
    serialId = model.serialId
    if serialId in _MODEL_STATE_MAP:
        for matter, ma in _MODEL_STATE_MAP[serialId].iteritems():
            if matters is not None and matter not in matters:
                continue
            if 'last' in ma:
                tint_data.append((matter, ma['last']))

    return tint_data


def clear_ta_content_map():
    if BigWorld.getTintContentSize() > MAX_CONTENT_CACHESIZE:
        BigWorld.clearTintContents()


def build_tint_name(x_ta, static):
    global taNameSerialId
    taNameSerialId += 1
    name = '@TA.%d#%s' % (taNameSerialId, static)
    BigWorld.buildDynamicTint(name, x_ta)
    return name


def _sort_state(state_def, state_alt):
    ret = [state_def]
    if state_def == 'hide' or state_def == 'burnhead':
        return ret
    else:
        ret.extend(state_alt)
        return ret


def parse_tint_with_params(dst, params):
    index = 0
    for k, v in dst.items():
        if k == 'fx':
            dst_fx_str = v.asString
            count = dst_fx_str.count('%')
            if count:
                v.setString(dst_fx_str % tuple(params[index:index + count]))
                index = index + count
        elif k == 'property':
            dst_prop_vstr = v.child(0).asString
            count = dst_prop_vstr.count('%')
            if count:
                v.child(0).setString(dst_prop_vstr % tuple(params[index:index + count]))
                index = index + count


def _get_tint_content(model, matter, tint):
    if not model:
        return
    if tint == '':
        dst = ResMgr.createXMLSectionFromString('ta', '<ta></ta>')
        return (dst, None, None)
    serialId = model.serialId
    params = _MODEL_STATE_MAP[serialId][matter]['tas'][tint]
    try:
        if params is None:
            return (TAs[tint][1], TAs[tint][1], None)
        tintCopy = getattr(model, 'tintCopy', None)
        dst = tintCopy.get(tint, None) if tintCopy else None
        if not checkTintCanReuse(dst, params):
            dst = None
        if not dst:
            dst = ResMgr.createXMLSectionFromString('ta', '<ta></ta>')
            dst.copy(TAs[tint][1])
        parse_tint_with_params(dst, params)
        return (dst, TAs[tint][1], tuple(params))
    except:
        clientUtils.reportEngineException('failGetTintContent %s %s' % (tint, params))


def _set_static(model, tint, matter):
    if not model:
        return
    if not model.getMatterList():
        return
    if matter is None:
        for k, v in model.getMatterList():
            _set_static(model, tint, k)

        return
    serialId = model.serialId
    if serialId not in _MODEL_STATE_MAP:
        _MODEL_STATE_MAP[serialId] = {}
    if matter not in _MODEL_STATE_MAP[serialId]:
        _MODEL_STATE_MAP[serialId][matter] = {}
    if _MODEL_STATE_MAP[serialId][matter].get('static', None) != tint:
        _MODEL_STATE_MAP[serialId][matter]['static'] = tint
        _MODEL_STATE_MAP[serialId][matter]['changed'] = True


def _overwrite_ta(dst, src):
    if src is None:
        return
    sitems = src.items()
    ditems = dst.items()
    for sk, sv in sitems:
        found = 0
        for dk, dv in ditems:
            if sk == dk:
                if sk == 'property' and sv.asString == dv.asString:
                    dsize = len(dv.keys())
                    for i in xrange(0, dsize):
                        dv.delChild(dv.child(i))

                    ssize = len(sv.keys())
                    for i in xrange(0, ssize):
                        dv.copy(sv.child(i))

                    found = 1
                    break
                elif sk == 'fx':
                    dv.setString(sv.asString)
                    found = 1
                    break

        if found != 1:
            dst_cs = dst.createSection(sk)
            dst_cs.setString(sv.asString)
            if sk == 'property':
                dst_cs.copy(sv)


def parse_ta_in_map(model, tintName, matter, state_def, state_alt):
    global _PARSE_TA_MAP
    sorted_state = _sort_state(state_def, state_alt)
    x_ta = ResMgr.createXMLSectionFromString('ta', '<ta></ta>')
    modelKey = model.sources[0]
    tas = []
    for state in sorted_state:
        content, ta, pa = _get_tint_content(model, matter, state)
        if content and ta:
            tas.append((ta, pa))
        _overwrite_ta(x_ta, content)

    fx = x_ta.readString('fx')
    shaderExist = True
    fx = fx.strip().lower()
    fx = fx.replace('_hardskinned_', '_')
    fx = fx.replace('hardskinned_', '')
    fx = fx.replace('_hardskinned', '')
    fx = fx.replace('_skinned_', '_')
    fx = fx.replace('skinned_', '')
    fx = fx.replace('_skinned', '')
    fx = fx.replace('_uniform_', '_')
    fx = fx.replace('uniform_', '')
    fx = fx.replace('_uniform', '')
    if fx:
        if fx not in gShaderList:
            shaderExist = False
        else:
            model.addTintFx(fx)
    _PARSE_TA_MAP[modelKey][tintName] = (x_ta, shaderExist, tas)


def ta_apply_mm(model, matter, force, needSetAttr = True, tintName = '', needBuildName = True):
    if not model:
        return
    changed = _get_state_changed(model, matter)
    if not force and not changed:
        return
    if len(_PARSE_TA_MAP) > TA_MAX_CACHESIZE:
        _PARSE_TA_MAP.clear()
    state_def = _get_def_state(model, matter)
    state_alt = list(_get_state(model, matter))
    state_static = _get_static_state(model, matter)
    state_static = str(state_static)
    if state_def == '' and len(state_alt) == 0 and state_static.find('Default') != -1:
        model.__setattr__(matter, state_static)
        _set_matter_tint_name(model, matter, state_static)
    else:
        modelKey = model.sources[0]
        if not _PARSE_TA_MAP.has_key(modelKey):
            _PARSE_TA_MAP[modelKey] = {}
        if needBuildName:
            parse_ta_in_map(model, tintName, matter, state_def, state_alt)
            if not _PARSE_TA_MAP[modelKey][tintName][1]:
                return
            parse_texture_from_content(model, tintName, _PARSE_TA_MAP[modelKey][tintName][0])
        if (needSetAttr or state_static.find('@TA.') == -1) and needBuildName:
            name = build_tint_name(_PARSE_TA_MAP[modelKey][tintName][0], state_static)
        else:
            name = state_static
        if needSetAttr:
            model.__setattr__(matter, name)
        _set_matter_tint_name(model, matter, name)


def parse_texture_from_content(model, tintName, content):
    global _PARSE_TEXTURE_MAP
    modelKey = model.sources[0]
    if len(_PARSE_TEXTURE_MAP) > TA_MAX_CACHESIZE:
        _PARSE_TEXTURE_MAP.clear()
    if not _PARSE_TEXTURE_MAP.has_key(modelKey):
        _PARSE_TEXTURE_MAP[modelKey] = {}
    fxTextures = set()
    if _PARSE_TEXTURE_MAP[modelKey].has_key(tintName):
        fxTextures = _PARSE_TEXTURE_MAP[modelKey][tintName]
    else:
        for k, v in content.items():
            if k == 'property':
                texture = v.readString('Texture')
                if texture is None:
                    continue
                fxTextures.add(texture.strip())

        _PARSE_TEXTURE_MAP[modelKey][tintName] = fxTextures
    for i in fxTextures:
        if hasattr(model, 'addTintFxTexture'):
            model.addTintFxTexture(i)


def ta_apply(models, force = False, needSetAttr = True, tintName = ''):
    if models is None:
        return
    for m in models:
        if not m:
            continue
        if not m.getMatterList():
            return
        for k, v in m.getMatterList():
            ta_apply_mm(m, k, force, needSetAttr, tintName)


def ta_del(models, tint, matter = None, isTaAddCall = False, applyLater = False, tintType = UNKNOWTINT):
    if gameglobal.gDisableTint:
        return
    if models is None:
        return
    if not needTintAlt(models):
        return
    gamelog.debug('TA: ta_del {0} {1} {2} {3} {4}'.format(models, tint, matter, isTaAddCall, applyLater))
    for m in models:
        _del_state(m, tint, matter)

    if not applyLater:
        ta_apply(models)
    if isTaAddCall:
        gTintEffectCounterMgr.dec(tintType)


def ta_add(models, tintName, params = None, time = 0, matter = None, force = False, applyLater = False, effectHost = None, effectOwner = None, tintType = UNKNOWTINT):
    if gameglobal.gDisableTint:
        return None
    if not needTintAlt(models):
        return None
    if not gTintEffectCounterMgr.canAddState(tintType):
        return None
    if not models:
        return None
    if tintName not in TAs:
        return None
    forceDisplayTint = SYSCD.data.get('forceDisplayTint', [])
    if effectHost and effectHost.getEffectLv() < gameglobal.EFFECT_MID and tintName not in forceDisplayTint:
        return None
    if not specialCheck(tintName, effectHost):
        return None
    gamelog.debug('TA: ta_add {0} {1} {2} {3} {4} {5}'.format(models, tintName, matter, time, force, applyLater))
    for m in models:
        _add_state(m, tintName, params, matter)

    if not applyLater:
        ta_apply(models, force, True, tintName)
        gTintEffectCounterMgr.inc(tintType)
        if time > 0:
            return BigWorld.callback(time, Functor(ta_del, models, tintName, matter, True, False, tintType))


def specialCheck(tintName, host):
    if host:
        tintStateType = getattr(host, 'tintStateType', (0, None))
        if tintName == 'copperstealth_fnl' and tintName != tintStateType[1]:
            return False
    return True


def ta_addGaoLiang(models, fresnelColor = (0.2, 3.2, 0.2), time = 0.0, effectHost = None, effectOwner = None):
    if gameglobal.gDisableTint:
        return
    if models is None:
        return
    if effectHost and effectHost.getEffectLv() < gameglobal.EFFECT_MID:
        return
    for model in models:
        if model:
            model.setFresnel(0, time / 2, time, fresnelColor[0], fresnelColor[1], fresnelColor[2])


def ta_delGaoLiang(models):
    if models is None:
        return
    for model in models:
        if model:
            fresnelColor = model.fresnelColor
            model.setFresnel(0.01, 0.01, 0.2, fresnelColor[0], fresnelColor[1], fresnelColor[2])


def ta_addHitGaoLiang(models, beginTime, middleTime, endTime, fresnelColor = (0.2, 3.2, 0.2), effectHost = None, effectOwner = None):
    if gameglobal.gDisableTint:
        return
    if models is None:
        return
    if effectHost and effectHost.inWorld and effectHost.getEffectLv() < gameglobal.EFFECT_MID:
        return
    for model in models:
        if model and type(fresnelColor) == tuple:
            model.setFresnel(beginTime, middleTime, endTime, fresnelColor[0], fresnelColor[1], fresnelColor[2])


def ta_set_static(models, tint, matter = None, applyLater = False):
    if models is None:
        return
    if not needTintAlt(models):
        return
    gamelog.debug('TA: ta_set_static {0} {1} {2}'.format(models, tint, matter))
    for m in models:
        _set_static(m, tint, matter)

    if not applyLater:
        ta_apply(models)


def ta_set_static_states(model, tint, matter = None, partName = None, param = None, needBuildName = True):
    if model is None:
        return
    _set_static_state(model, tint, matter, partName, param)
    if not model.getMatterList():
        return
    if matter:
        ta_apply_mm(model, matter, False, False, '', needBuildName)
    else:
        for k, v in model.getMatterList():
            ta_apply_mm(model, k, False, False, '', needBuildName)


def _set_static_state(model, tint, matter, partName = None, param = []):
    if not model:
        return
    if not model.getMatterList():
        return
    if matter is None:
        for k, v in model.getMatterList():
            _set_static(model, tint, k)

        return
    serialId = model.serialId
    if serialId not in _MODEL_STATE_MAP:
        _MODEL_STATE_MAP[serialId] = {}
    if matter not in _MODEL_STATE_MAP[serialId]:
        _MODEL_STATE_MAP[serialId][matter] = {}
    _MODEL_STATE_MAP[serialId][matter]['static'] = tint
    _MODEL_STATE_MAP[serialId][matter]['changed'] = True
    if partName:
        if 'tas' not in _MODEL_STATE_MAP[serialId][matter]:
            _MODEL_STATE_MAP[serialId][matter]['tas'] = {}
        _MODEL_STATE_MAP[serialId][matter]['tas'][partName] = param
        if 'state' not in _MODEL_STATE_MAP[serialId][matter]:
            _MODEL_STATE_MAP[serialId][matter]['state'] = set()
        _MODEL_STATE_MAP[serialId][matter]['state'].add(partName)


def ta_reset(models):
    if models is None or len(models) <= 0:
        return
    if not needTintAlt(models):
        return
    gamelog.debug('TA: ta_reset {0}'.format(models))
    for m in models:
        _del_model(m)

    ta_apply(models, True)


def needTintAlt(models):
    for model in models:
        if not hasattr(model, 'serialId'):
            return False

    return True


def setContentStateNoUse(tintName):
    BigWorld.setContentStateByScript(tintName, TINT_SCRIPTUSE)
    BigWorld.setContentStateByScript(tintName, TINT_NOUSE)


def addExtraTint(model, tintName, time, param, matter, force = False, applyLater = False, effectHost = None, effectOwner = None, tintType = UNKNOWTINT):
    clientcom.fetchExtraTintEffectsContents(model, tintName, time, param, matter, force, applyLater, effectHost, effectOwner, tintType, clientcom.afterFetchTintEffectContents)
