#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/PaletteFile.o
import string

class PaletteFile:
    rawmode = 'RGB'

    def __init__(self, fp):
        self.palette = map(lambda i: (i, i, i), range(256))
        while 1:
            s = fp.readline()
            if not s:
                break
            if s[0] == '#':
                continue
            if len(s) > 100:
                raise SyntaxError, 'bad palette file'
            v = map(int, string.split(s))
            try:
                i, r, g, b = v
            except ValueError:
                i, r = v
                g = b = r

            if 0 <= i <= 255:
                self.palette[i] = chr(r) + chr(g) + chr(b)

        self.palette = string.join(self.palette, '')

    def getpalette(self):
        return (self.palette, self.rawmode)
