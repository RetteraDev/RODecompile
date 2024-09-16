#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Hash/SHA512.o
"""SHA-512 cryptographic hash algorithm.

SHA-512 belongs to the SHA-2_ family of cryptographic hashes.
It produces the 512 bit digest of a message.

    >>> from Crypto.Hash import SHA512
    >>>
    >>> h = SHA512.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

*SHA* stands for Secure Hash Algorithm.

.. _SHA-2: http://csrc.nist.gov/publications/fips/fips180-2/fips180-2.pdf
"""
_revision__ = '$Id$'
__all__ = ['new', 'digest_size', 'SHA512Hash']
from Crypto.Util.py3compat import *
from Crypto.Hash.hashalgo import HashAlgo
try:
    import hashlib
    hashFactory = hashlib.sha512
except ImportError:
    from Crypto.Hash import _SHA512
    hashFactory = _SHA512

class SHA512Hash(HashAlgo):
    """Class that implements a SHA-512 hash
    
    :undocumented: block_size
    """
    oid = b('	`†He')
    digest_size = 64
    block_size = 128

    def __init__(self, data = None):
        HashAlgo.__init__(self, hashFactory, data)

    def new(self, data = None):
        return SHA512Hash(data)


def new(data = None):
    """Return a fresh instance of the hash object.
    
    :Parameters:
       data : byte string
        The very first chunk of the message to hash.
        It is equivalent to an early call to `SHA512Hash.update()`.
        Optional.
    
    :Return: A `SHA512Hash` object
    """
    return SHA512Hash().new(data)


digest_size = SHA512Hash.digest_size
block_size = SHA512Hash.block_size
