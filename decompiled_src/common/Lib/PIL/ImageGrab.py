#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageGrab.o
import Image
try:
    grabber = Image.core.grabscreen
except AttributeError:
    import _grabscreen
    grabber = _grabscreen.grab

def grab(bbox = None):
    size, data = grabber()
    im = Image.fromstring('RGB', size, data, 'raw', 'BGR', size[0] * 3 + 3 & -4, -1)
    if bbox:
        im = im.crop(bbox)
    return im


def grabclipboard():
    debug = 0
    data = Image.core.grabclipboard(debug)
    if Image.isStringType(data):
        import BmpImagePlugin, StringIO
        return BmpImagePlugin.DibImageFile(StringIO.StringIO(data))
    return data
