#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\qrcode\image/pil.o
from __future__ import absolute_import
try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image
    import ImageDraw

import qrcode.image.base

class PilImage(qrcode.image.base.BaseImage):
    """
    PIL image builder, default format is PNG.
    """
    kind = 'PNG'

    def new_image(self, **kwargs):
        img = Image.new('1', (self.pixel_size, self.pixel_size), 'white')
        self._idr = ImageDraw.Draw(img)
        return img

    def drawrect(self, row, col):
        box = self.pixel_box(row, col)
        self._idr.rectangle(box, fill='black')

    def save(self, stream, kind = None):
        if kind is None:
            kind = self.kind
        self._img.save(stream, kind)

    def __getattr__(self, name):
        return getattr(self._img, name)
