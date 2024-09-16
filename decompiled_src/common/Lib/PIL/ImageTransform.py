#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageTransform.o
import Image

class Transform(Image.ImageTransformHandler):

    def __init__(self, data):
        self.data = data

    def getdata(self):
        return (self.method, self.data)

    def transform(self, size, image, **options):
        method, data = self.getdata()
        return image.transform(size, method, data, **options)


class AffineTransform(Transform):
    method = Image.AFFINE


class ExtentTransform(Transform):
    method = Image.EXTENT


class QuadTransform(Transform):
    method = Image.QUAD


class MeshTransform(Transform):
    method = Image.MESH
