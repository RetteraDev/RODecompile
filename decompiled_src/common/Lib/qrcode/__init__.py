#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\qrcode/__init__.o
from qrcode.main import QRCode
from qrcode.main import make
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from qrcode import image

def run_example(data = 'http://www.lincolnloop.com', *args, **kwargs):
    """
    Build an example QR Code and display it.
    
    There's an even easier way than the code here though: just use the ``make``
    shortcut.
    """
    qr = QRCode(*args, **kwargs)
    qr.add_data(data)
    im = qr.make_image()
    im.show()


if __name__ == '__main__':
    import sys
    run_example(*sys.argv[1:])
