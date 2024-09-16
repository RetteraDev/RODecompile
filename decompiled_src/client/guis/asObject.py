#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/asObject.o
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
from ui import unicode2gbk, gbk2unicode
globalGfxFunc = {}

def toGfxVal(val):
    gfxVal = None
    if val.__class__.__name__ == 'int' or val.__class__.__name__ == 'float':
        return GfxValue(val)
    elif isinstance(val, list) or isinstance(val, tuple):
        ret = gameglobal.rds.ui.movie.CreateArray()
        for index, item in enumerate(val):
            ret.SetElement(index, toGfxVal(item))

        return ret
    elif isinstance(val, dict):
        ret = gameglobal.rds.ui.movie.CreateObject()
        for key, item in val.items():
            ret.SetMember(key, toGfxVal(item))

        return ret
    elif isinstance(val, GfxValue):
        return val
    elif isinstance(val, str):
        return GfxValue(gbk2unicode(val, val))
    elif isinstance(val, ASObject):
        return val.gfxVal
    elif callable(val):
        valKey = str(val)
        if not globalGfxFunc.has_key(valKey):
            gfxFunc = gameglobal.rds.ui.movie.CreateFunction(val)
            globalGfxFunc[valKey] = gfxFunc
        return globalGfxFunc.get(valKey)
    elif val == None:
        nullObj = GfxValue(1)
        nullObj.SetNull()
        return nullObj
    elif isinstance(val, long):
        return GfxValue(str(val))
    else:
        return GfxValue(val)


def encode(val, toUnicode = True):
    if isinstance(val, str):
        if toUnicode:
            return gbk2unicode(val, val)
        else:
            return unicode2gbk(val, val)
    else:
        if toUnicode and isinstance(val, long):
            return str(val)
        if isinstance(val, list):
            ret = [ encode(item, toUnicode) for item in val ]
            return ret
        if isinstance(val, tuple):
            ret = [ encode(item, toUnicode) for item in val ]
            return ret
        if isinstance(val, dict):
            val = {key:encode(item, toUnicode) for key, item in val.iteritems()}
            if not toUnicode:
                return ASDict(val)
            else:
                return val
        else:
            if isinstance(val, ASObject):
                if toUnicode:
                    return val.gfxVal
                return val
            if isinstance(val, GfxValue):
                if toUnicode:
                    return val
                else:
                    return ASObject(val)
    return val


class ASDict(dict):

    def __getattr__(self, name):
        if name in self.iterkeys():
            return self[name]
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in self.iterkeys():
            self[name] = value


testSignal = GfxValue(1)

def enableNewGfxValue():
    global testSignal
    isPub = BigWorld.isPublishedVersion()
    return (isPub and gameglobal.rds.configData.get('enableNewGfxValue', False) or not isPub) and callable(testSignal)


class ASObject(object):

    def __init__(self, gfxVal):
        self.__dict__['gfxVal'] = gfxVal
        self.__dict__['attrDict'] = {}

    def __getattr__(self, name):
        if enableNewGfxValue():
            gfxVal = self.__dict__['gfxVal']
            if gfxVal and hasattr(gfxVal, 'GetPyMember'):
                if not name.startswith('__'):
                    asObject = encode(gfxVal.GetPyMember(name), False)
                    return asObject
            try:
                return object.__getattribute__(self, name)
            except:
                return

        if self.__dict__['gfxVal'] and not name.startswith('__'):
            attr = self.__dict__['gfxVal'].GetMember(name)
            if attr:
                if attr.IsNull():
                    return
                asObj = self.__dict__['attrDict'].get(name, None)
                if asObj:
                    asObj.__dict__['gfxVal'] = attr
                else:
                    if attr.IsNumber() or attr.IsInt():
                        return attr.GetNumber()
                    if attr.IsString():
                        return unicode2gbk(attr.GetString(), attr.GetString())
                    if attr.IsBool():
                        return attr.GetBool()
                    asObj = ASObject(attr)
                    self.__dict__['attrDict'][name] = asObj
                return asObj
        try:
            return object.__getattribute__(self, name)
        except:
            return

    def __setattr__(self, name, value):
        if enableNewGfxValue():
            gfxVal = self.__dict__['gfxVal']
            if name in self.__dict__:
                object.__setattr__(self, name, value)
            elif gfxVal and hasattr(gfxVal, 'SetPyMember'):
                gfxVal.SetPyMember(name, encode(value, True))
            return
        if name in self.__dict__:
            object.__setattr__(self, name, value)
        else:
            attr = self.__dict__['gfxVal'].GetMember(name)
            if attr:
                self.__dict__['gfxVal'].SetMember(name, toGfxVal(value))
            else:
                ASUtils.setMcData(self, name, value)

    def __call__(self, *args):
        if enableNewGfxValue():
            gfxVal = self.__dict__['gfxVal']
            args = encode(args, True)
            result = gfxVal(*args)
            result = encode(result, False)
            return result
        else:
            result = None
            if not args:
                result = self.__dict__['gfxVal'].InvokeSelf()
            else:
                result = self.__dict__['gfxVal'].InvokeSelf(tuple([ toGfxVal(arg) for arg in args ]))
            if result and not result.IsNull():
                if result.IsNumber() or result.IsInt():
                    return result.GetNumber()
                elif result.IsString():
                    return unicode2gbk(result.GetString(), result.GetString())
                elif result.IsBool():
                    return result.GetBool()
                else:
                    return ASObject(result)
            return

    def __eq__(self, other):
        if other == None and (self.__dict__['gfxVal'] == None or self.__dict__['gfxVal'].IsNull()):
            return True
        elif not isinstance(other, ASObject):
            return False
        else:
            return self.__dict__['gfxVal'] == other.__dict__['gfxVal']

    def __ne__(self, other):
        return not self == other

    def __getitem__(self, key):
        gfxVal = self.__dict__['gfxVal']
        if gfxVal:
            if isinstance(key, int) and gfxVal.GetArraySize() > 0:
                val = gfxVal.GetElement(key)
                if val.IsNumber() or val.IsInt():
                    return val.GetNumber()
                elif val.IsString():
                    return unicode2gbk(val.GetString(), val.GetString())
                elif val.IsBool():
                    return val.GetBool()
                else:
                    return ASObject(val)
            elif hasattr(gfxVal, 'GetPyMember'):
                if not key.startswith('__'):
                    asObject = encode(gfxVal.GetPyMember(key), False)
                    return asObject
            return KeyError(key)
        raise KeyError(key)

    def __len__(self):
        gfxVal = self.__dict__['gfxVal']
        if gfxVal:
            if hasattr(gfxVal, 'IsArray') and gfxVal.IsArray():
                return gfxVal.GetArraySize()
            return 1
        return 0


TipManager = ASObject(None)
MenuManager = ASObject(None)
ASUtils = ASObject(None)
Tweener = ASObject(None)
RedPotManager = ASObject(None)
DisplayObjectUtils = ASObject(None)
RichItemConst = ASObject(None)
FocusManager = ASObject(None)

def initAsObject(uiObj):
    global MenuManager
    global TipManager
    try:
        TipManager.gfxVal = uiObj.Invoke('getClsByClsName', GfxValue('com.scaleform.mmo.core.manager.SimpleTipManager'))
        MenuManager.gfxVal = uiObj.Invoke('getClsByClsName', GfxValue('com.scaleform.mmo.core.manager.MenuManager'))
        ASUtils.gfxVal = uiObj.Invoke('getClsByClsName', GfxValue('com.scaleform.mmo.utils.GameUtils'))
        Tweener.gfxVal = uiObj.Invoke('getClsByClsName', GfxValue('caurina.transitions.Tweener'))
        RedPotManager.gfxVal = uiObj.Invoke('getClsByClsName', GfxValue('com.scaleform.mmo.core.manager.RedPotManager')).Invoke('getInstance')
        DisplayObjectUtils.gfxVal = uiObj.Invoke('getClsByClsName', GfxValue('com.scaleform.mmo.utils.DisplayObjectUitls'))
        RichItemConst.gfxVal = uiObj.Invoke('getClsByClsName', GfxValue('com.scaleform.mmo.core.constants.RichItemConst'))
        FocusManager.gfxVal = uiObj.Invoke('getClsByClsName', GfxValue('scaleform.gfx.FocusManager'))
    except Exception as e:
        gamelog.debug('initAsObject Error', e)
