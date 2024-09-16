#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageWin.o
import Image

class HDC:

    def __init__(self, dc):
        self.dc = dc

    def __int__(self):
        return self.dc


class HWND:

    def __init__(self, wnd):
        self.wnd = wnd

    def __int__(self):
        return self.wnd


class Dib:

    def __init__(self, image, size = None):
        if hasattr(image, 'mode') and hasattr(image, 'size'):
            mode = image.mode
            size = image.size
        else:
            mode = image
            image = None
        if mode not in ('1', 'L', 'P', 'RGB'):
            mode = Image.getmodebase(mode)
        self.image = Image.core.display(mode, size)
        self.mode = mode
        self.size = size
        if image:
            self.paste(image)

    def expose(self, handle):
        if isinstance(handle, HWND):
            dc = self.image.getdc(handle)
            try:
                result = self.image.expose(dc)
            finally:
                self.image.releasedc(handle, dc)

        else:
            result = self.image.expose(handle)
        return result

    def draw(self, handle, dst, src = None):
        if not src:
            src = (0, 0) + self.size
        if isinstance(handle, HWND):
            dc = self.image.getdc(handle)
            try:
                result = self.image.draw(dc, dst, src)
            finally:
                self.image.releasedc(handle, dc)

        else:
            result = self.image.draw(handle, dst, src)
        return result

    def query_palette(self, handle):
        if isinstance(handle, HWND):
            handle = self.image.getdc(handle)
            try:
                result = self.image.query_palette(handle)
            finally:
                self.image.releasedc(handle, handle)

        else:
            result = self.image.query_palette(handle)
        return result

    def paste(self, im, box = None):
        im.load()
        if self.mode != im.mode:
            im = im.convert(self.mode)
        if box:
            self.image.paste(im.im, box)
        else:
            self.image.paste(im.im)

    def fromstring(self, buffer):
        return self.image.fromstring(buffer)

    def tostring(self):
        return self.image.tostring()


class Window:

    def __init__(self, title = 'PIL', width = None, height = None):
        self.hwnd = Image.core.createwindow(title, self.__dispatcher, width or 0, height or 0)

    def __dispatcher(self, action, *args):
        return apply(getattr(self, 'ui_handle_' + action), args)

    def ui_handle_clear(self, dc, x0, y0, x1, y1):
        pass

    def ui_handle_damage(self, x0, y0, x1, y1):
        pass

    def ui_handle_destroy(self):
        pass

    def ui_handle_repair(self, dc, x0, y0, x1, y1):
        pass

    def ui_handle_resize(self, width, height):
        pass

    def mainloop(self):
        Image.core.eventloop()


class ImageWindow(Window):

    def __init__(self, image, title = 'PIL'):
        if not isinstance(image, Dib):
            image = Dib(image)
        self.image = image
        width, height = image.size
        Window.__init__(self, title, width=width, height=height)

    def ui_handle_repair(self, dc, x0, y0, x1, y1):
        self.image.draw(dc, (x0,
         y0,
         x1,
         y1))
