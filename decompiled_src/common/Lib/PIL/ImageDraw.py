#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageDraw.o
import Image, ImageColor
try:
    import warnings
except ImportError:
    warnings = None

class ImageDraw:

    def __init__(self, im, mode = None):
        im.load()
        if im.readonly:
            im._copy()
        blend = 0
        if mode is None:
            mode = im.mode
        if mode != im.mode:
            if mode == 'RGBA' and im.mode == 'RGB':
                blend = 1
            else:
                raise ValueError('mode mismatch')
        if mode == 'P':
            self.palette = im.palette
        else:
            self.palette = None
        self.im = im.im
        self.draw = Image.core.draw(self.im, blend)
        self.mode = mode
        if mode in ('I', 'F'):
            self.ink = self.draw.draw_ink(1, mode)
        else:
            self.ink = self.draw.draw_ink(-1, mode)
        if mode in ('1', 'P', 'I', 'F'):
            self.fontmode = '1'
        else:
            self.fontmode = 'L'
        self.fill = 0
        self.font = None

    def setink(self, ink):
        if warnings:
            warnings.warn("\'setink\' is deprecated; use keyword arguments instead", DeprecationWarning, stacklevel=2)
        if Image.isStringType(ink):
            ink = ImageColor.getcolor(ink, self.mode)
        if self.palette and not Image.isNumberType(ink):
            ink = self.palette.getcolor(ink)
        self.ink = self.draw.draw_ink(ink, self.mode)

    def setfill(self, onoff):
        if warnings:
            warnings.warn("\'setfill\' is deprecated; use keyword arguments instead", DeprecationWarning, stacklevel=2)
        self.fill = onoff

    def setfont(self, font):
        self.font = font

    def getfont(self):
        if not self.font:
            import ImageFont
            self.font = ImageFont.load_default()
        return self.font

    def _getink(self, ink, fill = None):
        if ink is None and fill is None:
            if self.fill:
                fill = self.ink
            else:
                ink = self.ink
        else:
            if ink is not None:
                if Image.isStringType(ink):
                    ink = ImageColor.getcolor(ink, self.mode)
                if self.palette and not Image.isNumberType(ink):
                    ink = self.palette.getcolor(ink)
                ink = self.draw.draw_ink(ink, self.mode)
            if fill is not None:
                if Image.isStringType(fill):
                    fill = ImageColor.getcolor(fill, self.mode)
                if self.palette and not Image.isNumberType(fill):
                    fill = self.palette.getcolor(fill)
                fill = self.draw.draw_ink(fill, self.mode)
        return (ink, fill)

    def arc(self, xy, start, end, fill = None):
        ink, fill = self._getink(fill)
        if ink is not None:
            self.draw.draw_arc(xy, start, end, ink)

    def bitmap(self, xy, bitmap, fill = None):
        bitmap.load()
        ink, fill = self._getink(fill)
        if ink is None:
            ink = fill
        if ink is not None:
            self.draw.draw_bitmap(xy, bitmap.im, ink)

    def chord(self, xy, start, end, fill = None, outline = None):
        ink, fill = self._getink(outline, fill)
        if fill is not None:
            self.draw.draw_chord(xy, start, end, fill, 1)
        if ink is not None:
            self.draw.draw_chord(xy, start, end, ink, 0)

    def ellipse(self, xy, fill = None, outline = None):
        ink, fill = self._getink(outline, fill)
        if fill is not None:
            self.draw.draw_ellipse(xy, fill, 1)
        if ink is not None:
            self.draw.draw_ellipse(xy, ink, 0)

    def line(self, xy, fill = None, width = 0):
        ink, fill = self._getink(fill)
        if ink is not None:
            self.draw.draw_lines(xy, ink, width)

    def shape(self, shape, fill = None, outline = None):
        shape.close()
        ink, fill = self._getink(outline, fill)
        if fill is not None:
            self.draw.draw_outline(shape, fill, 1)
        if ink is not None:
            self.draw.draw_outline(shape, ink, 0)

    def pieslice(self, xy, start, end, fill = None, outline = None):
        ink, fill = self._getink(outline, fill)
        if fill is not None:
            self.draw.draw_pieslice(xy, start, end, fill, 1)
        if ink is not None:
            self.draw.draw_pieslice(xy, start, end, ink, 0)

    def point(self, xy, fill = None):
        ink, fill = self._getink(fill)
        if ink is not None:
            self.draw.draw_points(xy, ink)

    def polygon(self, xy, fill = None, outline = None):
        ink, fill = self._getink(outline, fill)
        if fill is not None:
            self.draw.draw_polygon(xy, fill, 1)
        if ink is not None:
            self.draw.draw_polygon(xy, ink, 0)

    def rectangle(self, xy, fill = None, outline = None):
        ink, fill = self._getink(outline, fill)
        if fill is not None:
            self.draw.draw_rectangle(xy, fill, 1)
        if ink is not None:
            self.draw.draw_rectangle(xy, ink, 0)

    def text(self, xy, text, fill = None, font = None, anchor = None):
        ink, fill = self._getink(fill)
        if font is None:
            font = self.getfont()
        if ink is None:
            ink = fill
        if ink is not None:
            try:
                mask, offset = font.getmask2(text, self.fontmode)
                xy = (xy[0] + offset[0], xy[1] + offset[1])
            except AttributeError:
                try:
                    mask = font.getmask(text, self.fontmode)
                except TypeError:
                    mask = font.getmask(text)

            self.draw.draw_bitmap(xy, mask, ink)

    def textsize(self, text, font = None):
        if font is None:
            font = self.getfont()
        return font.getsize(text)


def Draw(im, mode = None):
    try:
        return im.getdraw(mode)
    except AttributeError:
        return ImageDraw(im, mode)


try:
    Outline = Image.core.outline
except:
    Outline = None

def getdraw(im = None, hints = None):
    handler = None
    if not hints or 'nicest' in hints:
        try:
            import _imagingagg
            handler = _imagingagg
        except ImportError:
            pass

    if handler is None:
        import ImageDraw2
        handler = ImageDraw2
    if im:
        im = handler.Draw(im)
    return (im, handler)


def floodfill(image, xy, value, border = None):
    """Fill bounded region."""
    pixel = image.load()
    x, y = xy
    try:
        background = pixel[x, y]
        if background == value:
            return
        pixel[x, y] = value
    except IndexError:
        return

    edge = [(x, y)]
    if border is None:
        while edge:
            newedge = []
            for x, y in edge:
                for s, t in ((x + 1, y),
                 (x - 1, y),
                 (x, y + 1),
                 (x, y - 1)):
                    try:
                        p = pixel[s, t]
                    except IndexError:
                        pass
                    else:
                        if p == background:
                            pixel[s, t] = value
                            newedge.append((s, t))

            edge = newedge

    else:
        while edge:
            newedge = []
            for x, y in edge:
                for s, t in ((x + 1, y),
                 (x - 1, y),
                 (x, y + 1),
                 (x, y - 1)):
                    try:
                        p = pixel[s, t]
                    except IndexError:
                        pass
                    else:
                        if p != value and p != border:
                            pixel[s, t] = value
                            newedge.append((s, t))

            edge = newedge
