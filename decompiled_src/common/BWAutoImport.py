#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common/BWAutoImport.o
import __builtin__
import encodings
DEFAULT_ENCODING = 'utf-8'

def setDefaultEncoding():
    import sys
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding(DEFAULT_ENCODING)
        del sys.setdefaultencoding
    print 'Default encoding set to', 'utf-8'


def main():
    setDefaultEncoding()


main()
