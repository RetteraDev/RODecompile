#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageSequence.o


class Iterator:

    def __init__(self, im):
        if not hasattr(im, 'seek'):
            raise AttributeError('im must have seek method')
        self.im = im

    def __getitem__(self, ix):
        try:
            if ix:
                self.im.seek(ix)
            return self.im
        except EOFError:
            raise IndexError
