#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageFilter.o


class Filter:
    pass


class Kernel(Filter):

    def __init__(self, size, kernel, scale = None, offset = 0):
        if scale is None:
            scale = reduce(lambda a, b: a + b, kernel)
        if size[0] * size[1] != len(kernel):
            raise ValueError('not enough coefficients in kernel')
        self.filterargs = (size,
         scale,
         offset,
         kernel)

    def filter(self, image):
        if image.mode == 'P':
            raise ValueError('cannot filter palette images')
        return apply(image.filter, self.filterargs)


class BuiltinFilter(Kernel):

    def __init__(self):
        pass


class RankFilter(Filter):
    name = 'Rank'

    def __init__(self, size, rank):
        self.size = size
        self.rank = rank

    def filter(self, image):
        if image.mode == 'P':
            raise ValueError('cannot filter palette images')
        image = image.expand(self.size / 2, self.size / 2)
        return image.rankfilter(self.size, self.rank)


class MedianFilter(RankFilter):
    name = 'Median'

    def __init__(self, size = 3):
        self.size = size
        self.rank = size * size / 2


class MinFilter(RankFilter):
    name = 'Min'

    def __init__(self, size = 3):
        self.size = size
        self.rank = 0


class MaxFilter(RankFilter):
    name = 'Max'

    def __init__(self, size = 3):
        self.size = size
        self.rank = size * size - 1


class ModeFilter(Filter):
    name = 'Mode'

    def __init__(self, size = 3):
        self.size = size

    def filter(self, image):
        return image.modefilter(self.size)


class GaussianBlur(Filter):
    name = 'GaussianBlur'

    def __init__(self, radius = 2):
        self.radius = 2

    def filter(self, image):
        return image.gaussian_blur(self.radius)


class UnsharpMask(Filter):
    name = 'UnsharpMask'

    def __init__(self, radius = 2, percent = 150, threshold = 3):
        self.radius = 2
        self.percent = percent
        self.threshold = threshold

    def filter(self, image):
        return image.unsharp_mask(self.radius, self.percent, self.threshold)


class BLUR(BuiltinFilter):
    name = 'Blur'
    filterargs = ((5, 5),
     16,
     0,
     (1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1))


class CONTOUR(BuiltinFilter):
    name = 'Contour'
    filterargs = ((3, 3),
     1,
     255,
     (-1, -1, -1, -1, 8, -1, -1, -1, -1))


class DETAIL(BuiltinFilter):
    name = 'Detail'
    filterargs = ((3, 3),
     6,
     0,
     (0, -1, 0, -1, 10, -1, 0, -1, 0))


class EDGE_ENHANCE(BuiltinFilter):
    name = 'Edge-enhance'
    filterargs = ((3, 3),
     2,
     0,
     (-1, -1, -1, -1, 10, -1, -1, -1, -1))


class EDGE_ENHANCE_MORE(BuiltinFilter):
    name = 'Edge-enhance More'
    filterargs = ((3, 3),
     1,
     0,
     (-1, -1, -1, -1, 9, -1, -1, -1, -1))


class EMBOSS(BuiltinFilter):
    name = 'Emboss'
    filterargs = ((3, 3),
     1,
     128,
     (-1, 0, 0, 0, 1, 0, 0, 0, 0))


class FIND_EDGES(BuiltinFilter):
    name = 'Find Edges'
    filterargs = ((3, 3),
     1,
     0,
     (-1, -1, -1, -1, 8, -1, -1, -1, -1))


class SMOOTH(BuiltinFilter):
    name = 'Smooth'
    filterargs = ((3, 3),
     13,
     0,
     (1, 1, 1, 1, 5, 1, 1, 1, 1))


class SMOOTH_MORE(BuiltinFilter):
    name = 'Smooth More'
    filterargs = ((5, 5),
     100,
     0,
     (1, 1, 1, 1, 1, 1, 5, 5, 5, 1, 1, 5, 44, 5, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1))


class SHARPEN(BuiltinFilter):
    name = 'Sharpen'
    filterargs = ((3, 3),
     16,
     0,
     (-2, -2, -2, -2, 32, -2, -2, -2, -2))
