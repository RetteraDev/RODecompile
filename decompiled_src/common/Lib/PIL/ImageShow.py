#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/ImageShow.o
import Image
import os, sys
_viewers = []

def register(viewer, order = 1):
    try:
        if issubclass(viewer, Viewer):
            viewer = viewer()
    except TypeError:
        pass

    if order > 0:
        _viewers.append(viewer)
    elif order < 0:
        _viewers.insert(0, viewer)


def show(image, title = None, **options):
    for viewer in _viewers:
        if viewer.show(image, title=title, **options):
            return 1

    return 0


class Viewer:

    def show(self, image, **options):
        if image.mode[:4] == 'I;16':
            base = 'L'
        else:
            base = Image.getmodebase(image.mode)
        if base != image.mode and image.mode != '1':
            image = image.convert(base)
        self.show_image(image, **options)

    format = None

    def get_format(self, image):
        return self.format

    def get_command(self, file, **options):
        raise NotImplementedError

    def save_image(self, image):
        return image._dump(format=self.get_format(image))

    def show_image(self, image, **options):
        return self.show_file(self.save_image(image), **options)

    def show_file(self, file, **options):
        os.system(self.get_command(file, **options))
        return 1


if sys.platform == 'win32':

    class WindowsViewer(Viewer):
        format = 'BMP'

        def get_command(self, file, **options):
            return 'start /wait %s && del /f %s' % (file, file)


    register(WindowsViewer)
elif sys.platform == 'darwin':

    class MacViewer(Viewer):
        format = 'BMP'

        def get_command(self, file, **options):
            command = 'open -a /Applications/Preview.app'
            command = '(%s %s; sleep 20; rm -f %s)&' % (command, file, file)
            return command


    register(MacViewer)
else:

    def which(executable):
        path = os.environ.get('PATH')
        if not path:
            return None
        for dirname in path.split(os.pathsep):
            filename = os.path.join(dirname, executable)
            if os.path.isfile(filename):
                return filename


    class UnixViewer(Viewer):

        def show_file(self, file, **options):
            command, executable = self.get_command_ex(file, **options)
            command = '(%s %s; rm -f %s)&' % (command, file, file)
            os.system(command)
            return 1


    class DisplayViewer(UnixViewer):

        def get_command_ex(self, file, **options):
            command = executable = 'display'
            return (command, executable)


    if which('display'):
        register(DisplayViewer)

    class XVViewer(UnixViewer):

        def get_command_ex(self, file, title = None, **options):
            command = executable = 'xv'
            if title:
                command = command + ' -name \"%s\"' % title
            return (command, executable)


    if which('xv'):
        register(XVViewer)
if __name__ == '__main__':
    print show(Image.open(sys.argv[1]), *sys.argv[2:])
