#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageTk.o
import Tkinter, Image
_pilbitmap_ok = None

def _pilbitmap_check():
    global _pilbitmap_ok
    if _pilbitmap_ok is None:
        try:
            im = Image.new('1', (1, 1))
            Tkinter.BitmapImage(data='PIL:%d' % im.im.id)
            _pilbitmap_ok = 1
        except Tkinter.TclError:
            _pilbitmap_ok = 0

    return _pilbitmap_ok


class PhotoImage:

    def __init__(self, image = None, size = None, **kw):
        if image is None:
            if kw.has_key('file'):
                image = Image.open(kw['file'])
                del kw['file']
            elif kw.has_key('data'):
                from StringIO import StringIO
                image = Image.open(StringIO(kw['data']))
                del kw['data']
        if hasattr(image, 'mode') and hasattr(image, 'size'):
            mode = image.mode
            if mode == 'P':
                image.load()
                try:
                    mode = image.palette.mode
                except AttributeError:
                    mode = 'RGB'

            size = image.size
            kw['width'], kw['height'] = size
        else:
            mode = image
            image = None
        if mode not in ('1', 'L', 'RGB', 'RGBA'):
            mode = Image.getmodebase(mode)
        self.__mode = mode
        self.__size = size
        self.__photo = apply(Tkinter.PhotoImage, (), kw)
        self.tk = self.__photo.tk
        if image:
            self.paste(image)

    def __del__(self):
        name = self.__photo.name
        self.__photo.name = None
        try:
            self.__photo.tk.call('image', 'delete', name)
        except:
            pass

    def __str__(self):
        return str(self.__photo)

    def width(self):
        return self.__size[0]

    def height(self):
        return self.__size[1]

    def paste(self, im, box = None):
        im.load()
        image = im.im
        if image.isblock() and im.mode == self.__mode:
            block = image
        else:
            block = image.new_block(self.__mode, im.size)
            image.convert2(block, image)
        tk = self.__photo.tk
        try:
            tk.call('PyImagingPhoto', self.__photo, block.id)
        except Tkinter.TclError as v:
            try:
                import _imagingtk
                try:
                    _imagingtk.tkinit(tk.interpaddr(), 1)
                except AttributeError:
                    _imagingtk.tkinit(id(tk), 0)

                tk.call('PyImagingPhoto', self.__photo, block.id)
            except (ImportError, AttributeError, Tkinter.TclError):
                raise


class BitmapImage:

    def __init__(self, image = None, **kw):
        if image is None:
            if kw.has_key('file'):
                image = Image.open(kw['file'])
                del kw['file']
            elif kw.has_key('data'):
                from StringIO import StringIO
                image = Image.open(StringIO(kw['data']))
                del kw['data']
        self.__mode = image.mode
        self.__size = image.size
        if _pilbitmap_check():
            image.load()
            kw['data'] = 'PIL:%d' % image.im.id
            self.__im = image
        else:
            kw['data'] = image.tobitmap()
        self.__photo = apply(Tkinter.BitmapImage, (), kw)

    def __del__(self):
        name = self.__photo.name
        self.__photo.name = None
        try:
            self.__photo.tk.call('image', 'delete', name)
        except:
            pass

    def width(self):
        return self.__size[0]

    def height(self):
        return self.__size[1]

    def __str__(self):
        return str(self.__photo)


def getimage(photo):
    photo.tk.call('PyImagingPhotoGet', photo)


def _show(image, title):

    class UI(Tkinter.Label):

        def __init__(self, master, im):
            if im.mode == '1':
                self.image = BitmapImage(im, foreground='white', master=master)
            else:
                self.image = PhotoImage(im, master=master)
            Tkinter.Label.__init__(self, master, image=self.image, bg='black', bd=0)

    if not Tkinter._default_root:
        raise IOError, 'tkinter not initialized'
    top = Tkinter.Toplevel()
    if title:
        top.title(title)
    UI(top, image).pack()
