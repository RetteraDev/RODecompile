#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/FontFile.o
import os
import Image
import marshal
try:
    import zlib
except ImportError:
    zlib = None

WIDTH = 800

def puti16(fp, values):
    for v in values:
        if v < 0:
            v = v + 65536
        fp.write(chr(v >> 8 & 255) + chr(v & 255))


class FontFile:
    bitmap = None

    def __init__(self):
        self.info = {}
        self.glyph = [None] * 256

    def __getitem__(self, ix):
        return self.glyph[ix]

    def compile(self):
        """Create metrics and bitmap"""
        if self.bitmap:
            return
        h = w = maxwidth = 0
        lines = 1
        for glyph in self:
            if glyph:
                d, dst, src, im = glyph
                h = max(h, src[3] - src[1])
                w = w + (src[2] - src[0])
                if w > WIDTH:
                    lines = lines + 1
                    w = src[2] - src[0]
                maxwidth = max(maxwidth, w)

        xsize = maxwidth
        ysize = lines * h
        if xsize == 0 and ysize == 0:
            return ''
        self.ysize = h
        self.bitmap = Image.new('1', (xsize, ysize))
        self.metrics = [None] * 256
        x = y = 0
        for i in range(256):
            glyph = self[i]
            if glyph:
                d, dst, src, im = glyph
                xx, yy = src[2] - src[0], src[3] - src[1]
                x0, y0 = x, y
                x = x + xx
                if x > WIDTH:
                    x, y = 0, y + h
                    x0, y0 = x, y
                    x = xx
                s = (src[0] + x0,
                 src[1] + y0,
                 src[2] + x0,
                 src[3] + y0)
                self.bitmap.paste(im.crop(src), s)
                self.metrics[i] = (d, dst, s)

    def save1(self, filename):
        """Save font in version 1 format"""
        self.compile()
        self.bitmap.save(os.path.splitext(filename)[0] + '.pbm', 'PNG')
        fp = open(os.path.splitext(filename)[0] + '.pil', 'wb')
        fp.write('PILfont\n')
        fp.write(';;;;;;%d;\n' % self.ysize)
        fp.write('DATA\n')
        for id in range(256):
            m = self.metrics[id]
            if not m:
                puti16(fp, [0] * 10)
            else:
                puti16(fp, m[0] + m[1] + m[2])

        fp.close()

    def save2(self, filename):
        """Save font in version 2 format"""
        self.compile()
        data = marshal.dumps((self.metrics, self.info))
        if zlib:
            data = 'z' + zlib.compress(data, 9)
        else:
            data = 'u' + data
        fp = open(os.path.splitext(filename)[0] + '.pil', 'wb')
        fp.write('PILfont2\n' + self.name + '\n' + 'DATA\n')
        fp.write(data)
        self.bitmap.save(fp, 'PNG')
        fp.close()

    save = save1
