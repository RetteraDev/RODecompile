#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ArgImagePlugin.o
__version__ = '0.4'
import Image, ImageFile, ImagePalette
from PngImagePlugin import i16, i32, ChunkStream, _MODES
MAGIC = 'ŠARG\r\n\n'

class ArgStream(ChunkStream):
    """Parser callbacks for ARG data"""

    def __init__(self, fp):
        ChunkStream.__init__(self, fp)
        self.eof = 0
        self.im = None
        self.palette = None
        self.__reset()

    def __reset(self):
        self.count = 0
        self.id = None
        self.action = ('NONE',)
        self.images = {}
        self.names = {}

    def chunk_AHDR(self, offset, bytes):
        """AHDR -- animation header"""
        if self.count != 0:
            raise SyntaxError, 'misplaced AHDR chunk'
        s = self.fp.read(bytes)
        self.size = (i32(s), i32(s[4:]))
        try:
            self.mode, self.rawmode = _MODES[ord(s[8]), ord(s[9])]
        except:
            raise SyntaxError, 'unknown ARG mode'

        if Image.DEBUG:
            print 'AHDR size', self.size
            print 'AHDR mode', self.mode, self.rawmode
        return s

    def chunk_AFRM(self, offset, bytes):
        """AFRM -- next frame follows"""
        if self.count != 0:
            raise SyntaxError, 'misplaced AFRM chunk'
        self.show = 1
        self.id = 0
        self.count = 1
        self.repair = None
        s = self.fp.read(bytes)
        if len(s) >= 2:
            self.id = i16(s)
            if len(s) >= 4:
                self.count = i16(s[2:4])
                if len(s) >= 6:
                    self.repair = i16(s[4:6])
                else:
                    self.repair = None
        if Image.DEBUG:
            print 'AFRM', self.id, self.count
        return s

    def chunk_ADEF(self, offset, bytes):
        """ADEF -- store image"""
        if self.count != 0:
            raise SyntaxError, 'misplaced ADEF chunk'
        self.show = 0
        self.id = 0
        self.count = 1
        self.repair = None
        s = self.fp.read(bytes)
        if len(s) >= 2:
            self.id = i16(s)
            if len(s) >= 4:
                self.count = i16(s[2:4])
        if Image.DEBUG:
            print 'ADEF', self.id, self.count
        return s

    def chunk_NAME(self, offset, bytes):
        """NAME -- name the current image"""
        if self.count == 0:
            raise SyntaxError, 'misplaced NAME chunk'
        name = self.fp.read(bytes)
        self.names[self.id] = name
        return name

    def chunk_AEND(self, offset, bytes):
        """AEND -- end of animation"""
        if Image.DEBUG:
            print 'AEND'
        self.eof = 1
        raise EOFError, 'end of ARG file'

    def __getmodesize(self, s, full = 1):
        size = (i32(s), i32(s[4:]))
        try:
            mode, rawmode = _MODES[ord(s[8]), ord(s[9])]
        except:
            raise SyntaxError, 'unknown image mode'

        if full:
            if ord(s[12]):
                pass
            if ord(s[11]):
                raise SyntaxError, 'unknown filter category'
        return (size, mode, rawmode)

    def chunk_PAST(self, offset, bytes):
        """PAST -- paste one image into another"""
        if self.count == 0:
            raise SyntaxError, 'misplaced PAST chunk'
        if self.repair is not None:
            self.images[self.id] = self.images[self.repair].copy()
            self.repair = None
        s = self.fp.read(bytes)
        im = self.images[i16(s)]
        x, y = i32(s[2:6]), i32(s[6:10])
        bbox = (x,
         y,
         im.size[0] + x,
         im.size[1] + y)
        if im.mode in ('RGBA',):
            self.images[self.id].paste(im, bbox, im)
        else:
            self.images[self.id].paste(im, bbox)
        self.action = ('PAST',)
        self.__store()
        return s

    def chunk_BLNK(self, offset, bytes):
        """BLNK -- create blank image"""
        if self.count == 0:
            raise SyntaxError, 'misplaced BLNK chunk'
        s = self.fp.read(bytes)
        size, mode, rawmode = self.__getmodesize(s, 0)
        self.action = ('BLNK',)
        self.im = Image.core.fill(mode, size, 0)
        self.__store()
        return s

    def chunk_IHDR(self, offset, bytes):
        """IHDR -- full image follows"""
        if self.count == 0:
            raise SyntaxError, 'misplaced IHDR chunk'
        s = self.fp.read(bytes)
        size, mode, rawmode = self.__getmodesize(s)
        self.action = ('IHDR',)
        self.im = Image.core.new(mode, size)
        self.decoder = Image.core.zip_decoder(rawmode)
        self.decoder.setimage(self.im, (0, 0) + size)
        self.data = ''
        return s

    def chunk_DHDR(self, offset, bytes):
        """DHDR -- delta image follows"""
        if self.count == 0:
            raise SyntaxError, 'misplaced DHDR chunk'
        s = self.fp.read(bytes)
        size, mode, rawmode = self.__getmodesize(s)
        diff = ord(s[13])
        offs = (i32(s[14:18]), i32(s[18:22]))
        bbox = offs + (offs[0] + size[0], offs[1] + size[1])
        if Image.DEBUG:
            print 'DHDR', diff, bbox
        self.action = ('DHDR', diff, bbox)
        self.im = Image.core.new(mode, size)
        self.decoder = Image.core.zip_decoder(rawmode)
        self.decoder.setimage(self.im, (0, 0) + size)
        self.data = ''
        return s

    def chunk_JHDR(self, offset, bytes):
        """JHDR -- JPEG image follows"""
        if self.count == 0:
            raise SyntaxError, 'misplaced JHDR chunk'
        s = self.fp.read(bytes)
        size, mode, rawmode = self.__getmodesize(s, 0)
        self.action = ('JHDR',)
        self.im = Image.core.new(mode, size)
        self.decoder = Image.core.jpeg_decoder(rawmode)
        self.decoder.setimage(self.im, (0, 0) + size)
        self.data = ''
        return s

    def chunk_UHDR(self, offset, bytes):
        """UHDR -- uncompressed image data follows (EXPERIMENTAL)"""
        if self.count == 0:
            raise SyntaxError, 'misplaced UHDR chunk'
        s = self.fp.read(bytes)
        size, mode, rawmode = self.__getmodesize(s, 0)
        self.action = ('UHDR',)
        self.im = Image.core.new(mode, size)
        self.decoder = Image.core.raw_decoder(rawmode)
        self.decoder.setimage(self.im, (0, 0) + size)
        self.data = ''
        return s

    def chunk_IDAT(self, offset, bytes):
        """IDAT -- image data block"""
        s = self.fp.read(bytes)
        self.data = self.data + s
        n, e = self.decoder.decode(self.data)
        if n < 0:
            if e < 0:
                raise IOError, 'decoder error %d' % e
        else:
            self.data = self.data[n:]
        return s

    def chunk_DEND(self, offset, bytes):
        return self.chunk_IEND(offset, bytes)

    def chunk_JEND(self, offset, bytes):
        return self.chunk_IEND(offset, bytes)

    def chunk_UEND(self, offset, bytes):
        return self.chunk_IEND(offset, bytes)

    def chunk_IEND(self, offset, bytes):
        """IEND -- end of image"""
        del self.decoder
        del self.data
        self.__store()
        return self.fp.read(bytes)

    def __store(self):
        cid = self.action[0]
        if cid in ('BLNK', 'IHDR', 'JHDR', 'UHDR'):
            self.images[self.id] = self.im
        elif cid == 'DHDR':
            cid, mode, bbox = self.action
            im0 = self.images[self.id]
            im1 = self.im
            if mode == 0:
                im1 = im1.chop_add_modulo(im0.crop(bbox))
            im0.paste(im1, bbox)
        self.count = self.count - 1
        if self.count == 0 and self.show:
            self.im = self.images[self.id]
            raise EOFError

    def chunk_PLTE(self, offset, bytes):
        """PLTE -- palette data"""
        s = self.fp.read(bytes)
        if self.mode == 'P':
            self.palette = ImagePalette.raw('RGB', s)
        return s

    def chunk_sYNC(self, offset, bytes):
        """SYNC -- reset decoder"""
        if self.count != 0:
            raise SyntaxError, 'misplaced sYNC chunk'
        s = self.fp.read(bytes)
        self.__reset()
        return s


def _accept(prefix):
    return prefix[:8] == MAGIC


class ArgImageFile(ImageFile.ImageFile):
    format = 'ARG'
    format_description = 'Animated raster graphics'

    def _open(self):
        if Image.warnings:
            Image.warnings.warn('The ArgImagePlugin driver is obsolete, and will be removed from a future release of PIL.  If you rely on this module, please contact the PIL authors.', RuntimeWarning)
        if self.fp.read(8) != MAGIC:
            raise SyntaxError, 'not an ARG file'
        self.arg = ArgStream(self.fp)
        cid, offset, bytes = self.arg.read()
        if cid != 'AHDR':
            raise SyntaxError, 'expected an AHDR chunk'
        s = self.arg.call(cid, offset, bytes)
        self.arg.crc(cid, s)
        self.mode = self.arg.mode
        self.size = self.arg.size

    def load(self):
        if self.arg.im is None:
            self.seek(0)
        self.im = self.arg.im
        self.palette = self.arg.palette
        Image.Image.load(self)

    def seek(self, frame):
        if self.arg.eof:
            raise EOFError, 'end of animation'
        self.fp = self.arg.fp
        while 1:
            cid, offset, bytes = self.arg.read()
            if self.arg.eof:
                raise EOFError, 'end of animation'
            try:
                s = self.arg.call(cid, offset, bytes)
            except EOFError:
                break
            except 'glurk':
                if Image.DEBUG:
                    print cid, bytes, '(unknown)'
                s = self.fp.read(bytes)

            self.arg.crc(cid, s)

        self.fp.read(4)

    def tell(self):
        return 0

    def verify(self):
        """Verify ARG file"""
        self.fp.seek(8)
        self.arg.verify(self)
        self.arg.close()
        self.fp = None


Image.register_open('ARG', ArgImageFile, _accept)
Image.register_extension('ARG', '.arg')
Image.register_mime('ARG', 'video/x-arg')
