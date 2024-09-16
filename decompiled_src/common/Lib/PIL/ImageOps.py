#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageOps.o
import Image
import operator

def _border(border):
    if type(border) is type(()):
        if len(border) == 2:
            left, top = right, bottom = border
        elif len(border) == 4:
            left, top, right, bottom = border
    else:
        left = top = right = bottom = border
    return (left,
     top,
     right,
     bottom)


def _color(color, mode):
    if Image.isStringType(color):
        import ImageColor
        color = ImageColor.getcolor(color, mode)
    return color


def _lut(image, lut):
    if image.mode == 'P':
        raise NotImplementedError('mode P support coming soon')
    else:
        if image.mode in ('L', 'RGB'):
            if image.mode == 'RGB' and len(lut) == 256:
                lut = lut + lut + lut
            return image.point(lut)
        raise IOError, 'not supported for this image mode'


def autocontrast(image, cutoff = 0, ignore = None):
    """Maximize image contrast, based on histogram"""
    histogram = image.histogram()
    lut = []
    for layer in range(0, len(histogram), 256):
        h = histogram[layer:layer + 256]
        if ignore is not None:
            try:
                h[ignore] = 0
            except TypeError:
                for ix in ignore:
                    h[ix] = 0

        if cutoff:
            n = 0
            for ix in range(256):
                n = n + h[ix]

            cut = n * cutoff / 100
            for lo in range(256):
                if cut > h[lo]:
                    cut = cut - h[lo]
                    h[lo] = 0
                else:
                    h[lo] = h[lo] - cut
                    cut = 0
                if cut <= 0:
                    break

            cut = n * cutoff / 100
            for hi in range(255, -1, -1):
                if cut > h[hi]:
                    cut = cut - h[hi]
                    h[hi] = 0
                else:
                    h[hi] = h[hi] - cut
                    cut = 0
                if cut <= 0:
                    break

        for lo in range(256):
            if h[lo]:
                break

        for hi in range(255, -1, -1):
            if h[hi]:
                break

        if hi <= lo:
            lut.extend(range(256))
        else:
            scale = 255.0 / (hi - lo)
            offset = -lo * scale
            for ix in range(256):
                ix = int(ix * scale + offset)
                if ix < 0:
                    ix = 0
                elif ix > 255:
                    ix = 255
                lut.append(ix)

    return _lut(image, lut)


def colorize(image, black, white):
    """Colorize a grayscale image"""
    assert image.mode == 'L'
    black = _color(black, 'RGB')
    white = _color(white, 'RGB')
    red = []
    green = []
    blue = []
    for i in range(256):
        red.append(black[0] + i * (white[0] - black[0]) / 255)
        green.append(black[1] + i * (white[1] - black[1]) / 255)
        blue.append(black[2] + i * (white[2] - black[2]) / 255)

    image = image.convert('RGB')
    return _lut(image, red + green + blue)


def crop(image, border = 0):
    """Crop border off image"""
    left, top, right, bottom = _border(border)
    return image.crop((left,
     top,
     image.size[0] - right,
     image.size[1] - bottom))


def deform(image, deformer, resample = Image.BILINEAR):
    """Deform image using the given deformer"""
    return image.transform(image.size, Image.MESH, deformer.getmesh(image), resample)


def equalize(image, mask = None):
    """Equalize image histogram"""
    if image.mode == 'P':
        image = image.convert('RGB')
    h = image.histogram(mask)
    lut = []
    for b in range(0, len(h), 256):
        histo = filter(None, h[b:b + 256])
        if len(histo) <= 1:
            lut.extend(range(256))
        else:
            step = (reduce(operator.add, histo) - histo[-1]) / 255
            if not step:
                lut.extend(range(256))
            else:
                n = step / 2
                for i in range(256):
                    lut.append(n / step)
                    n = n + h[i + b]

    return _lut(image, lut)


def expand(image, border = 0, fill = 0):
    """Add border to image"""
    left, top, right, bottom = _border(border)
    width = left + image.size[0] + right
    height = top + image.size[1] + bottom
    out = Image.new(image.mode, (width, height), _color(fill, image.mode))
    out.paste(image, (left, top))
    return out


def fit(image, size, method = Image.NEAREST, bleed = 0.0, centering = (0.5, 0.5)):
    """
    This method returns a sized and cropped version of the image,
    cropped to the aspect ratio and size that you request.
    """
    if type(centering) != type([]):
        centering = [centering[0], centering[1]]
    if centering[0] > 1.0 or centering[0] < 0.0:
        centering[0] = 0.5
    if centering[1] > 1.0 or centering[1] < 0.0:
        centering[1] = 0.5
    if bleed > 0.49999 or bleed < 0.0:
        bleed = 0.0
    bleedPixels = (int(float(bleed) * float(image.size[0]) + 0.5), int(float(bleed) * float(image.size[1]) + 0.5))
    liveArea = (bleedPixels[0],
     bleedPixels[1],
     image.size[0] - bleedPixels[0] - 1,
     image.size[1] - bleedPixels[1] - 1)
    liveSize = (liveArea[2] - liveArea[0], liveArea[3] - liveArea[1])
    liveAreaAspectRatio = float(liveSize[0]) / float(liveSize[1])
    aspectRatio = float(size[0]) / float(size[1])
    if liveAreaAspectRatio >= aspectRatio:
        cropWidth = int(aspectRatio * float(liveSize[1]) + 0.5)
        cropHeight = liveSize[1]
    else:
        cropWidth = liveSize[0]
        cropHeight = int(float(liveSize[0]) / aspectRatio + 0.5)
    leftSide = int(liveArea[0] + float(liveSize[0] - cropWidth) * centering[0])
    if leftSide < 0:
        leftSide = 0
    topSide = int(liveArea[1] + float(liveSize[1] - cropHeight) * centering[1])
    if topSide < 0:
        topSide = 0
    out = image.crop((leftSide,
     topSide,
     leftSide + cropWidth,
     topSide + cropHeight))
    return out.resize(size, method)


def flip(image):
    """Flip image vertically"""
    return image.transpose(Image.FLIP_TOP_BOTTOM)


def grayscale(image):
    """Convert to grayscale"""
    return image.convert('L')


def invert(image):
    """Invert image (negate)"""
    lut = []
    for i in range(256):
        lut.append(255 - i)

    return _lut(image, lut)


def mirror(image):
    """Flip image horizontally"""
    return image.transpose(Image.FLIP_LEFT_RIGHT)


def posterize(image, bits):
    """Reduce the number of bits per color channel"""
    lut = []
    mask = ~(2 ** (8 - bits) - 1)
    for i in range(256):
        lut.append(i & mask)

    return _lut(image, lut)


def solarize(image, threshold = 128):
    """Invert all values above threshold"""
    lut = []
    for i in range(256):
        if i < threshold:
            lut.append(i)
        else:
            lut.append(255 - i)

    return _lut(image, lut)


def gaussian_blur(im, radius = None):
    """ PIL_usm.gblur(im, [radius])"""
    if radius is None:
        radius = 5.0
    im.load()
    return im.im.gaussian_blur(radius)


gblur = gaussian_blur

def unsharp_mask(im, radius = None, percent = None, threshold = None):
    """ PIL_usm.usm(im, [radius, percent, threshold])"""
    if radius is None:
        radius = 5.0
    if percent is None:
        percent = 150
    if threshold is None:
        threshold = 3
    im.load()
    return im.im.unsharp_mask(radius, percent, threshold)


usm = unsharp_mask
