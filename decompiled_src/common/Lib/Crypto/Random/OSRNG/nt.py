#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Random\OSRNG/nt.o
__revision__ = '$Id$'
__all__ = ['WindowsRNG']
import winrandom
from rng_base import BaseRNG

class WindowsRNG(BaseRNG):
    name = '<CryptGenRandom>'

    def __init__(self):
        self.__winrand = winrandom.new()
        BaseRNG.__init__(self)

    def flush(self):
        """Work around weakness in Windows RNG.
        
        The CryptGenRandom mechanism in some versions of Windows allows an
        attacker to learn 128 KiB of past and future output.  As a workaround,
        this function reads 128 KiB of 'random' data from Windows and discards
        it.
        
        For more information about the weaknesses in CryptGenRandom, see
        _Cryptanalysis of the Random Number Generator of the Windows Operating
        System_, by Leo Dorrendorf and Zvi Gutterman and Benny Pinkas
        http://eprint.iacr.org/2007/419
        """
        if self.closed:
            raise ValueError('I/O operation on closed file')
        data = self.__winrand.get_bytes(131072)
        assert len(data) == 131072
        BaseRNG.flush(self)

    def _close(self):
        self.__winrand = None

    def _read(self, N):
        self.flush()
        data = self.__winrand.get_bytes(N)
        self.flush()
        return data


def new(*args, **kwargs):
    return WindowsRNG(*args, **kwargs)
