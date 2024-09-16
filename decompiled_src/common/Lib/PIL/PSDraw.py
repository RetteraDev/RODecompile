#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\PIL/PSDraw.o
import EpsImagePlugin
import string

class PSDraw:

    def __init__(self, fp = None):
        if not fp:
            import sys
            fp = sys.stdout
        self.fp = fp

    def begin_document(self, id = None):
        """Write Postscript DSC header"""
        self.fp.write('%!PS-Adobe-3.0\nsave\n/showpage { } def\n%%EndComments\n%%BeginDocument\n')
        self.fp.write(EDROFF_PS)
        self.fp.write(VDI_PS)
        self.fp.write('%%EndProlog\n')
        self.isofont = {}

    def end_document(self):
        """Write Postscript DSC footer"""
        self.fp.write('%%EndDocument\nrestore showpage\n%%End\n')
        if hasattr(self.fp, 'flush'):
            self.fp.flush()

    def setfont(self, font, size):
        if not self.isofont.has_key(font):
            self.fp.write('/PSDraw-%s ISOLatin1Encoding /%s E\n' % (font, font))
            self.isofont[font] = 1
        self.fp.write('/F0 %d /PSDraw-%s F\n' % (size, font))

    def setink(self, ink):
        print '*** NOT YET IMPLEMENTED ***'

    def line(self, xy0, xy1):
        xy = xy0 + xy1
        self.fp.write('%d %d %d %d Vl\n' % xy)

    def rectangle(self, box):
        self.fp.write('%d %d M %d %d 0 Vr\n' % box)

    def text(self, xy, text):
        text = string.joinfields(string.splitfields(text, '('), '\\(')
        text = string.joinfields(string.splitfields(text, ')'), '\\)')
        xy = xy + (text,)
        self.fp.write('%d %d M (%s) S\n' % xy)

    def image(self, box, im, dpi = None):
        """Write an PIL image"""
        if not dpi:
            if im.mode == '1':
                dpi = 200
            else:
                dpi = 100
        x = float(im.size[0] * 72) / dpi
        y = float(im.size[1] * 72) / dpi
        xmax = float(box[2] - box[0])
        ymax = float(box[3] - box[1])
        if x > xmax:
            y = y * xmax / x
            x = xmax
        if y > ymax:
            x = x * ymax / y
            y = ymax
        dx = (xmax - x) / 2 + box[0]
        dy = (ymax - y) / 2 + box[1]
        self.fp.write('gsave\n%f %f translate\n' % (dx, dy))
        if (x, y) != im.size:
            sx = x / im.size[0]
            sy = y / im.size[1]
            self.fp.write('%f %f scale\n' % (sx, sy))
        EpsImagePlugin._save(im, self.fp, None, 0)
        self.fp.write('\ngrestore\n')


EDROFF_PS = '/S { show } bind def\n/P { moveto show } bind def\n/M { moveto } bind def\n/X { 0 rmoveto } bind def\n/Y { 0 exch rmoveto } bind def\n/E {    findfont\n        dup maxlength dict begin\n        {\n                1 index /FID ne { def } { pop pop } ifelse\n        } forall\n        /Encoding exch def\n        dup /FontName exch def\n        currentdict end definefont pop\n} bind def\n/F {    findfont exch scalefont dup setfont\n        [ exch /setfont cvx ] cvx bind def\n} bind def\n'
VDI_PS = '/Vm { moveto } bind def\n/Va { newpath arcn stroke } bind def\n/Vl { moveto lineto stroke } bind def\n/Vc { newpath 0 360 arc closepath } bind def\n/Vr {   exch dup 0 rlineto\n        exch dup neg 0 exch rlineto\n        exch neg 0 rlineto\n        0 exch rlineto\n        100 div setgray fill 0 setgray } bind def\n/Tm matrix def\n/Ve {   Tm currentmatrix pop\n        translate scale newpath 0 0 .5 0 360 arc closepath\n        Tm setmatrix\n} bind def\n/Vf { currentgray exch setgray fill setgray } bind def\n'
ERROR_PS = '/landscape false def\n/errorBUF 200 string def\n/errorNL { currentpoint 10 sub exch pop 72 exch moveto } def\nerrordict begin /handleerror {\n    initmatrix /Courier findfont 10 scalefont setfont\n    newpath 72 720 moveto $error begin /newerror false def\n    (PostScript Error) show errorNL errorNL\n    (Error: ) show\n        /errorname load errorBUF cvs show errorNL errorNL\n    (Command: ) show\n        /command load dup type /stringtype ne { errorBUF cvs } if show\n        errorNL errorNL\n    (VMstatus: ) show\n        vmstatus errorBUF cvs show ( bytes available, ) show\n        errorBUF cvs show ( bytes used at level ) show\n        errorBUF cvs show errorNL errorNL\n    (Operand stargck: ) show errorNL /ostargck load {\n        dup type /stringtype ne { errorBUF cvs } if 72 0 rmoveto show errorNL\n    } forall errorNL\n    (Execution stargck: ) show errorNL /estargck load {\n        dup type /stringtype ne { errorBUF cvs } if 72 0 rmoveto show errorNL\n    } forall\n    end showpage\n} def end\n'
