#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Random\OSRNG/fallback.o
__revision__ = '$Id$'
__all__ = ['PythonOSURandomRNG']
import os
from rng_base import BaseRNG

class PythonOSURandomRNG(BaseRNG):
    name = '<os.urandom>'

    def __init__(self):
        self._read = os.urandom
        BaseRNG.__init__(self)

    def _close(self):
        self._read = None


def new(*args, **kwargs):
    return PythonOSURandomRNG(*args, **kwargs)