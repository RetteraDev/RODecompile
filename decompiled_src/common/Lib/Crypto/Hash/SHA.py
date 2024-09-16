#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Hash/SHA.o
"""SHA-1 cryptographic hash algorithm.

SHA-1_ produces the 160 bit digest of a message.

    >>> from Crypto.Hash import SHA
    >>>
    >>> h = SHA.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

*SHA* stands for Secure Hash Algorithm.

This algorithm is not considered secure. Do not use it for new designs.

.. _SHA-1: http://csrc.nist.gov/publications/fips/fips180-2/fips180-2.pdf
"""
_revision__ = '$Id$'
__all__ = ['new', 'digest_size', 'SHA1Hash']
from Crypto.Util.py3compat import *
from Crypto.Hash.hashalgo import HashAlgo
try:
    import hashlib
    hashFactory = hashlib.sha1
except ImportError:
    import sha
    hashFactory = sha

class SHA1Hash(HashAlgo):
    """Class that implements a SHA-1 hash
    
    :undocumented: block_size
    """
    oid = b('+')
    digest_size = 20
    block_size = 64

    def __init__(self, data = None):
        HashAlgo.__init__(self, hashFactory, data)

    def new(self, data = None):
        return SHA1Hash(data)


def new(data = None):
    """Return a fresh instance of the hash object.
    
    :Parameters:
       data : byte string
        The very first chunk of the message to hash.
        It is equivalent to an early call to `SHA1Hash.update()`.
        Optional.
    
    :Return: A `SHA1Hash` object
    """
    return SHA1Hash().new(data)


digest_size = SHA1Hash.digest_size
block_size = SHA1Hash.block_size
