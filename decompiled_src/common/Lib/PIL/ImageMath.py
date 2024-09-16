#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageMath.o
import Image
import _imagingmath
VERBOSE = 0

def _isconstant(v):
    return isinstance(v, type(0)) or isinstance(v, type(0.0))


class _Operand:

    def __init__(self, im):
        self.im = im

    def __fixup(self, im1):
        if isinstance(im1, _Operand):
            if im1.im.mode in ('1', 'L'):
                return im1.im.convert('I')
            if im1.im.mode in ('I', 'F'):
                return im1.im
            raise ValueError, 'unsupported mode: %s' % im1.im.mode
        else:
            if _isconstant(im1) and self.im.mode in ('1', 'L', 'I'):
                return Image.new('I', self.im.size, im1)
            return Image.new('F', self.im.size, im1)

    def apply(self, op, im1, im2 = None, mode = None):
        im1 = self.__fixup(im1)
        if im2 is None:
            out = Image.new(mode or im1.mode, im1.size, None)
            im1.load()
            try:
                op = getattr(_imagingmath, op + '_' + im1.mode)
            except AttributeError:
                raise TypeError, "bad operand type for \'%s\'" % op

            _imagingmath.unop(op, out.im.id, im1.im.id)
        else:
            im2 = self.__fixup(im2)
            if im1.mode != im2.mode:
                if im1.mode != 'F':
                    im1 = im1.convert('F')
                if im2.mode != 'F':
                    im2 = im2.convert('F')
                if im1.mode != im2.mode:
                    raise ValueError, 'mode mismatch'
            if im1.size != im2.size:
                size = (min(im1.size[0], im2.size[0]), min(im1.size[1], im2.size[1]))
                if im1.size != size:
                    im1 = im1.crop((0, 0) + size)
                if im2.size != size:
                    im2 = im2.crop((0, 0) + size)
                out = Image.new(mode or im1.mode, size, None)
            else:
                out = Image.new(mode or im1.mode, im1.size, None)
            im1.load()
            im2.load()
            try:
                op = getattr(_imagingmath, op + '_' + im1.mode)
            except AttributeError:
                raise TypeError, "bad operand type for \'%s\'" % op

            _imagingmath.binop(op, out.im.id, im1.im.id, im2.im.id)
        return _Operand(out)

    def __nonzero__(self):
        return self.im.getbbox() is not None

    def __abs__(self):
        return self.apply('abs', self)

    def __pos__(self):
        return self

    def __neg__(self):
        return self.apply('neg', self)

    def __add__(self, other):
        return self.apply('add', self, other)

    def __radd__(self, other):
        return self.apply('add', other, self)

    def __sub__(self, other):
        return self.apply('sub', self, other)

    def __rsub__(self, other):
        return self.apply('sub', other, self)

    def __mul__(self, other):
        return self.apply('mul', self, other)

    def __rmul__(self, other):
        return self.apply('mul', other, self)

    def __div__(self, other):
        return self.apply('div', self, other)

    def __rdiv__(self, other):
        return self.apply('div', other, self)

    def __mod__(self, other):
        return self.apply('mod', self, other)

    def __rmod__(self, other):
        return self.apply('mod', other, self)

    def __pow__(self, other):
        return self.apply('pow', self, other)

    def __rpow__(self, other):
        return self.apply('pow', other, self)

    def __invert__(self):
        return self.apply('invert', self)

    def __and__(self, other):
        return self.apply('and', self, other)

    def __rand__(self, other):
        return self.apply('and', other, self)

    def __or__(self, other):
        return self.apply('or', self, other)

    def __ror__(self, other):
        return self.apply('or', other, self)

    def __xor__(self, other):
        return self.apply('xor', self, other)

    def __rxor__(self, other):
        return self.apply('xor', other, self)

    def __lshift__(self, other):
        return self.apply('lshift', self, other)

    def __rshift__(self, other):
        return self.apply('rshift', self, other)

    def __eq__(self, other):
        return self.apply('eq', self, other)

    def __ne__(self, other):
        return self.apply('ne', self, other)

    def __lt__(self, other):
        return self.apply('lt', self, other)

    def __le__(self, other):
        return self.apply('le', self, other)

    def __gt__(self, other):
        return self.apply('gt', self, other)

    def __ge__(self, other):
        return self.apply('ge', self, other)


def imagemath_int(self):
    return _Operand(self.im.convert('I'))


def imagemath_float(self):
    return _Operand(self.im.convert('F'))


def imagemath_equal(self, other):
    return self.apply('eq', self, other, mode='I')


def imagemath_notequal(self, other):
    return self.apply('ne', self, other, mode='I')


def imagemath_min(self, other):
    return self.apply('min', self, other)


def imagemath_max(self, other):
    return self.apply('max', self, other)


def imagemath_convert(self, mode):
    return _Operand(self.im.convert(mode))


ops = {}
for k, v in globals().items():
    if k[:10] == 'imagemath_':
        ops[k[10:]] = v

def eval(expression, _dict = {}, **kw):
    args = ops.copy()
    args.update(_dict)
    args.update(kw)
    for k, v in args.items():
        if hasattr(v, 'im'):
            args[k] = _Operand(v)

    import __builtin__
    out = __builtin__.eval(expression, args)
    try:
        return out.im
    except AttributeError:
        return out
