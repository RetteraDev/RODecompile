#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Util/py21compat.o
"""Compatibility code for Python 2.1

Currently, this just defines:
    - True and False
    - object
    - isinstance
"""
__revision__ = '$Id$'
__all__ = []
import sys
import __builtin__
try:
    (True, False)
except NameError:
    True, False = (1, 0)
    __all__ += ['True', 'False']

try:
    object
except NameError:

    class object:
        pass


    __all__ += ['object']

try:
    isinstance(5, (int, long))
except TypeError:
    __all__ += ['isinstance']
    _builtin_type_map = {tuple: type(()),
     list: type([]),
     str: type(''),
     unicode: type(''),
     int: type(0),
     long: type(0L)}

    def isinstance(obj, t):
        if not __builtin__.isinstance(t, type(())):
            return __builtin__.isinstance(obj, _builtin_type_map.get(t, t))
        else:
            for typ in t:
                if __builtin__.isinstance(obj, _builtin_type_map.get(typ, typ)):
                    return True

            return False
