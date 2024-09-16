#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\qrcode/six.o
"""Utilities for writing code that runs on Python 2 and 3"""
from __future__ import absolute_import
import functools
import itertools
import operator
import sys
import types
__author__ = 'Benjamin Peterson <benjamin@python.org>'
__version__ = '1.9.0'
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (str,)
    integer_types = (int,)
    class_types = (type,)
    text_type = str
    binary_type = bytes
    MAXSIZE = sys.maxsize
else:
    string_types = (basestring,)
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
    if sys.platform.startswith('java'):
        MAXSIZE = int(2147483647L)
    else:

        class X(object):

            def __len__(self):
                return 2147483648L


        try:
            len(X())
        except OverflowError:
            MAXSIZE = int(2147483647L)
        else:
            MAXSIZE = int(9223372036854775807L)

        del X

def _add_doc(func, doc):
    """Add documentation to a function."""
    func.__doc__ = doc


def _import_module(name):
    """Import module, returning the module after the last dot."""
    __import__(name)
    return sys.modules[name]


class _LazyDescr(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, tp):
        result = self._resolve()
        setattr(obj, self.name, result)
        try:
            delattr(obj.__class__, self.name)
        except AttributeError:
            pass

        return result


class MovedModule(_LazyDescr):

    def __init__(self, name, old, new = None):
        super(MovedModule, self).__init__(name)
        if PY3:
            if new is None:
                new = name
            self.mod = new
        else:
            self.mod = old

    def _resolve(self):
        return _import_module(self.mod)

    def __getattr__(self, attr):
        _module = self._resolve()
        value = getattr(_module, attr)
        setattr(self, attr, value)
        return value


class _LazyModule(types.ModuleType):

    def __init__(self, name):
        super(_LazyModule, self).__init__(name)
        self.__doc__ = self.__class__.__doc__

    def __dir__(self):
        attrs = ['__doc__', '__name__']
        attrs += [ attr.name for attr in self._moved_attributes ]
        return attrs

    _moved_attributes = []


class MovedAttribute(_LazyDescr):

    def __init__(self, name, old_mod, new_mod, old_attr = None, new_attr = None):
        super(MovedAttribute, self).__init__(name)
        if PY3:
            if new_mod is None:
                new_mod = name
            self.mod = new_mod
            if new_attr is None:
                if old_attr is None:
                    new_attr = name
                else:
                    new_attr = old_attr
            self.attr = new_attr
        else:
            self.mod = old_mod
            if old_attr is None:
                old_attr = name
            self.attr = old_attr

    def _resolve(self):
        module = _import_module(self.mod)
        return getattr(module, self.attr)


class _SixMetaPathImporter(object):
    """
    A meta path importer to import six.moves and its submodules.
    
    This class implements a PEP302 finder and loader. It should be compatible
    with Python 2.5 and all existing versions of Python3
    """

    def __init__(self, six_module_name):
        self.name = six_module_name
        self.known_modules = {}

    def _add_module(self, mod, *fullnames):
        for fullname in fullnames:
            self.known_modules[self.name + '.' + fullname] = mod

    def _get_module(self, fullname):
        return self.known_modules[self.name + '.' + fullname]

    def find_module(self, fullname, path = None):
        if fullname in self.known_modules:
            return self

    def __get_module(self, fullname):
        try:
            return self.known_modules[fullname]
        except KeyError:
            raise ImportError('This loader does not know module ' + fullname)

    def load_module(self, fullname):
        try:
            return sys.modules[fullname]
        except KeyError:
            pass

        mod = self.__get_module(fullname)
        if isinstance(mod, MovedModule):
            mod = mod._resolve()
        else:
            mod.__loader__ = self
        sys.modules[fullname] = mod
        return mod

    def is_package(self, fullname):
        """
        Return true, if the named module is a package.
        
        We need this method to get correct spec objects with
        Python 3.4 (see PEP451)
        """
        return hasattr(self.__get_module(fullname), '__path__')

    def get_code(self, fullname):
        """Return None
        
        Required, if is_package is implemented"""
        self.__get_module(fullname)

    get_source = get_code


_importer = _SixMetaPathImporter(__name__)

class _MovedItems(_LazyModule):
    """Lazy loading of moved objects"""
    __path__ = []


_moved_attributes = [MovedAttribute('range', '__builtin__', 'builtins', 'xrange', 'range'),
 MovedAttribute('xrange', '__builtin__', 'builtins', 'xrange', 'range'),
 MovedModule('builtins', '__builtin__'),
 MovedModule('configparser', 'ConfigParser'),
 MovedModule('copyreg', 'copy_reg')]
for attr in _moved_attributes:
    setattr(_MovedItems, attr.name, attr)
    if isinstance(attr, MovedModule):
        _importer._add_module(attr, 'moves.' + attr.name)

del attr
_MovedItems._moved_attributes = _moved_attributes
moves = _MovedItems(__name__ + '.moves')
_importer._add_module(moves, 'moves')

def add_move(move):
    """Add an item to six.moves."""
    setattr(_MovedItems, move.name, move)


def remove_move(name):
    """Remove item from six.moves."""
    try:
        delattr(_MovedItems, name)
    except AttributeError:
        try:
            del moves.__dict__[name]
        except KeyError:
            raise AttributeError('no such move, %r' % (name,))


if PY3:
    _meth_func = '__func__'
    _meth_self = '__self__'
    _func_closure = '__closure__'
    _func_code = '__code__'
    _func_defaults = '__defaults__'
    _func_globals = '__globals__'
else:
    _meth_func = 'im_func'
    _meth_self = 'im_self'
    _func_closure = 'func_closure'
    _func_code = 'func_code'
    _func_defaults = 'func_defaults'
    _func_globals = 'func_globals'
try:
    advance_iterator = next
except NameError:

    def advance_iterator(it):
        return it.next()


next = advance_iterator
try:
    callable = callable
except NameError:

    def callable(obj):
        return any(('__call__' in klass.__dict__ for klass in type(obj).__mro__))


if PY3:

    def get_unbound_function(unbound):
        return unbound


    create_bound_method = types.MethodType
    Iterator = object
else:

    def get_unbound_function(unbound):
        return unbound.im_func


    def create_bound_method(func, obj):
        return types.MethodType(func, obj, obj.__class__)


    class Iterator(object):

        def next(self):
            return type(self).__next__(self)


    callable = callable
_add_doc(get_unbound_function, 'Get the function out of a possibly unbound function')
get_method_function = operator.attrgetter(_meth_func)
get_method_self = operator.attrgetter(_meth_self)
get_function_closure = operator.attrgetter(_func_closure)
get_function_code = operator.attrgetter(_func_code)
get_function_defaults = operator.attrgetter(_func_defaults)
get_function_globals = operator.attrgetter(_func_globals)
if PY3:

    def iterkeys(d, **kw):
        return iter(d.keys(**kw))


    def itervalues(d, **kw):
        return iter(d.values(**kw))


    def iteritems(d, **kw):
        return iter(d.items(**kw))


    def iterlists(d, **kw):
        return iter(d.lists(**kw))


    viewkeys = operator.methodcaller('keys')
    viewvalues = operator.methodcaller('values')
    viewitems = operator.methodcaller('items')
else:

    def iterkeys(d, **kw):
        return iter(d.iterkeys(**kw))


    def itervalues(d, **kw):
        return iter(d.itervalues(**kw))


    def iteritems(d, **kw):
        return iter(d.iteritems(**kw))


    def iterlists(d, **kw):
        return iter(d.iterlists(**kw))


    viewkeys = operator.methodcaller('viewkeys')
    viewvalues = operator.methodcaller('viewvalues')
    viewitems = operator.methodcaller('viewitems')
_add_doc(iterkeys, 'Return an iterator over the keys of a dictionary.')
_add_doc(itervalues, 'Return an iterator over the values of a dictionary.')
_add_doc(iteritems, 'Return an iterator over the (key, value) pairs of a dictionary.')
_add_doc(iterlists, 'Return an iterator over the (key, [values]) pairs of a dictionary.')
if PY3:

    def b(s):
        return s.encode('latin-1')


    def u(s):
        return s


    unichr = chr
    if sys.version_info[1] <= 1:

        def int2byte(i):
            return bytes((i,))


    else:
        int2byte = operator.methodcaller('to_bytes', 1, 'big')
    byte2int = operator.itemgetter(0)
    indexbytes = operator.getitem
    iterbytes = iter
    import io
    StringIO = io.StringIO
    BytesIO = io.BytesIO
    _assertCountEqual = 'assertCountEqual'
    _assertRaisesRegex = 'assertRaisesRegex'
    _assertRegex = 'assertRegex'
else:

    def b(s):
        return s


    def u(s):
        return unicode(s.replace('\\\\', '\\\\\\\\'), 'unicode_escape')


    unichr = unichr
    int2byte = chr

    def byte2int(bs):
        return ord(bs[0])


    def indexbytes(buf, i):
        return ord(buf[i])


    iterbytes = functools.partial(itertools.imap, ord)
    import StringIO
    StringIO = BytesIO = StringIO.StringIO
    _assertCountEqual = 'assertItemsEqual'
    _assertRaisesRegex = 'assertRaisesRegexp'
    _assertRegex = 'assertRegexpMatches'
_add_doc(b, 'Byte literal')
_add_doc(u, 'Text literal')

def assertCountEqual(self, *args, **kwargs):
    return getattr(self, _assertCountEqual)(*args, **kwargs)


def assertRaisesRegex(self, *args, **kwargs):
    return getattr(self, _assertRaisesRegex)(*args, **kwargs)


def assertRegex(self, *args, **kwargs):
    return getattr(self, _assertRegex)(*args, **kwargs)


if PY3:
    exec_ = getattr(moves.builtins, 'exec')

    def reraise(tp, value, tb = None):
        if value is None:
            value = tp()
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value


else:

    def exec_(_code_, _globs_ = None, _locs_ = None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec 'exec _code_ in _globs_, _locs_'


    exec_('def reraise(tp, value, tb=None):\n    raise tp, value, tb\n')
if sys.version_info[:2] == (3, 2):
    exec_('def raise_from(value, from_value):\n    if from_value is None:\n        raise value\n    raise value from from_value\n')
elif sys.version_info[:2] > (3, 2):
    exec_('def raise_from(value, from_value):\n    raise value from from_value\n')
else:

    def raise_from(value, from_value):
        raise value


print_ = getattr(moves.builtins, 'print', None)
if print_ is None:

    def print_(*args, **kwargs):
        """The new-style print function for Python 2.4 and 2.5."""
        fp = kwargs.pop('file', sys.stdout)
        if fp is None:
            return

        def write(data):
            if not isinstance(data, basestring):
                data = str(data)
            if isinstance(fp, file) and isinstance(data, unicode) and fp.encoding is not None:
                errors = getattr(fp, 'errors', None)
                if errors is None:
                    errors = 'strict'
                data = data.encode(fp.encoding, errors)
            fp.write(data)

        want_unicode = False
        sep = kwargs.pop('sep', None)
        if sep is not None:
            if isinstance(sep, unicode):
                want_unicode = True
            elif not isinstance(sep, str):
                raise TypeError('sep must be None or a string')
        end = kwargs.pop('end', None)
        if end is not None:
            if isinstance(end, unicode):
                want_unicode = True
            elif not isinstance(end, str):
                raise TypeError('end must be None or a string')
        if kwargs:
            raise TypeError('invalid keyword arguments to print()')
        if not want_unicode:
            for arg in args:
                if isinstance(arg, unicode):
                    want_unicode = True
                    break

        if want_unicode:
            newline = unicode('\n')
            space = unicode(' ')
        else:
            newline = '\n'
            space = ' '
        if sep is None:
            sep = space
        if end is None:
            end = newline
        for i, arg in enumerate(args):
            if i:
                write(sep)
            write(arg)

        write(end)


if sys.version_info[:2] < (3, 3):
    _print = print_

    def print_(*args, **kwargs):
        fp = kwargs.get('file', sys.stdout)
        flush = kwargs.pop('flush', False)
        _print(*args, **kwargs)
        if flush and fp is not None:
            fp.flush()


_add_doc(reraise, 'Reraise an exception.')
if sys.version_info[0:2] < (3, 4):

    def wraps(wrapped, assigned = functools.WRAPPER_ASSIGNMENTS, updated = functools.WRAPPER_UPDATES):

        def wrapper(f):
            f = functools.wraps(wrapped, assigned, updated)(f)
            f.__wrapped__ = wrapped
            return f

        return wrapper


else:
    wraps = functools.wraps

def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""

    class metaclass(meta):

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, 'temporary_class', (), {})


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)

        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper


def python_2_unicode_compatible(klass):
    """
    A decorator that defines __unicode__ and __str__ methods under Python 2.
    Under Python 3 it does nothing.
    
    To support Python 2 and 3 with a single code base, define a __str__ method
    returning text and apply this decorator to the class.
    """
    if PY2:
        if '__str__' not in klass.__dict__:
            raise ValueError("@python_2_unicode_compatible cannot be applied to %s because it doesn\'t define __str__()." % klass.__name__)
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return klass


__path__ = []
__package__ = __name__
if globals().get('__spec__') is not None:
    __spec__.submodule_search_locations = []
if sys.meta_path:
    for i, importer in enumerate(sys.meta_path):
        if type(importer).__name__ == '_SixMetaPathImporter' and importer.name == __name__:
            del sys.meta_path[i]
            break

    del i
    del importer
sys.meta_path.append(_importer)
