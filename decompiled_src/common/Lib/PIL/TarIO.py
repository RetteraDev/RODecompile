#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/TarIO.o
import ContainerIO
import string

class TarIO(ContainerIO.ContainerIO):

    def __init__(self, tarfile, file):
        fh = open(tarfile, 'rb')
        while 1:
            s = fh.read(512)
            if len(s) != 512:
                raise IOError, 'unexpected end of tar file'
            name = s[:100]
            i = string.find(name, chr(0))
            if i == 0:
                raise IOError, 'cannot find subfile'
            if i > 0:
                name = name[:i]
            size = string.atoi(s[124:136], 8)
            if file == name:
                break
            fh.seek(size + 511 & -512, 1)

        ContainerIO.ContainerIO.__init__(self, fh, fh.tell(), size)
