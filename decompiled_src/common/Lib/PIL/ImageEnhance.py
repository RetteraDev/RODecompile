#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageEnhance.o
import Image, ImageFilter, ImageStat

class _Enhance:

    def enhance(self, factor):
        return Image.blend(self.degenerate, self.image, factor)


class Color(_Enhance):
    """Adjust image colour balance"""

    def __init__(self, image):
        self.image = image
        self.degenerate = image.convert('L').convert(image.mode)


class Contrast(_Enhance):
    """Adjust image contrast"""

    def __init__(self, image):
        self.image = image
        mean = int(ImageStat.Stat(image.convert('L')).mean[0] + 0.5)
        self.degenerate = Image.new('L', image.size, mean).convert(image.mode)


class Brightness(_Enhance):
    """Adjust image brightness"""

    def __init__(self, image):
        self.image = image
        self.degenerate = Image.new(image.mode, image.size, 0)


class Sharpness(_Enhance):
    """Adjust image sharpness"""

    def __init__(self, image):
        self.image = image
        self.degenerate = image.filter(ImageFilter.SMOOTH)
