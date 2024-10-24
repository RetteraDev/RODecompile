#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/CurImagePlugin.o
__version__ = '0.1'
import Image, BmpImagePlugin

def i16(c):
    return ord(c[0]) + (ord(c[1]) << 8)


def i32(c):
    return ord(c[0]) + (ord(c[1]) << 8) + (ord(c[2]) << 16) + (ord(c[3]) << 24)


def _accept(prefix):
    return prefix[:4] == '   '


class CurImageFile(BmpImagePlugin.BmpImageFile):
    format = 'CUR'
    format_description = 'Windows Cursor'

    def _open(self):
        offset = self.fp.tell()
        s = self.fp.read(6)
        if not _accept(s):
            raise SyntaxError, 'not an CUR file'
        m = ''
        for i in range(i16(s[4:])):
            s = self.fp.read(16)
            if not m:
                m = s
            elif ord(s[0]) > ord(m[0]) and ord(s[1]) > ord(m[1]):
                m = s

        self._bitmap(i32(m[12:]) + offset)
        self.size = (self.size[0], self.size[1] / 2)
        d, e, o, a = self.tile[0]
        self.tile[0] = (d,
         (0, 0) + self.size,
         o,
         a)


Image.register_open('CUR', CurImageFile, _accept)
Image.register_extension('CUR', '.cur')
