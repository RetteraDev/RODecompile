#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageFileIO.o
from StringIO import StringIO

class ImageFileIO(StringIO):

    def __init__(self, fp):
        data = fp.read()
        StringIO.__init__(self, data)
