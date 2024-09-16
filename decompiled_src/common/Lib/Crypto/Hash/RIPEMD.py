#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Hash/RIPEMD.o
"""RIPEMD-160 cryptographic hash algorithm.

RIPEMD-160_ produces the 160 bit digest of a message.

    >>> from Crypto.Hash import RIPEMD
    >>>
    >>> h = RIPEMD.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

RIPEMD-160 stands for RACE Integrity Primitives Evaluation Message Digest
with a 160 bit digest. It was invented by Dobbertin, Bosselaers, and Preneel.

This algorithm is considered secure, although it has not been scrutinized as
extensively as SHA-1. Moreover, it provides an informal security level of just
80bits.

.. _RIPEMD-160: http://homes.esat.kuleuven.be/~bosselae/ripemd160.html
"""
_revision__ = '$Id$'
__all__ = ['new', 'digest_size', 'RIPEMD160Hash']
from Crypto.Util.py3compat import *
from Crypto.Hash.hashalgo import HashAlgo
import Crypto.Hash._RIPEMD160 as _RIPEMD160
hashFactory = _RIPEMD160

class RIPEMD160Hash(HashAlgo):
    """Class that implements a RIPMD-160 hash
    
    :undocumented: block_size
    """
    oid = b('+$')
    digest_size = 20
    block_size = 64

    def __init__(self, data = None):
        HashAlgo.__init__(self, hashFactory, data)

    def new(self, data = None):
        return RIPEMD160Hash(data)


def new(data = None):
    """Return a fresh instance of the hash object.
    
    :Parameters:
       data : byte string
        The very first chunk of the message to hash.
        It is equivalent to an early call to `RIPEMD160Hash.update()`.
        Optional.
    
    :Return: A `RIPEMD160Hash` object
    """
    return RIPEMD160Hash().new(data)


digest_size = RIPEMD160Hash.digest_size
block_size = RIPEMD160Hash.block_size
