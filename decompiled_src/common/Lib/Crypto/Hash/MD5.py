#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Hash/MD5.o
"""MD5 cryptographic hash algorithm.

MD5 is specified in RFC1321_ and produces the 128 bit digest of a message.

    >>> from Crypto.Hash import MD5
    >>>
    >>> h = MD5.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

MD5 stand for Message Digest version 5, and it was invented by Rivest in 1991.

This algorithm is insecure. Do not use it for new designs.

.. _RFC1321: http://tools.ietf.org/html/rfc1321 
"""
_revision__ = '$Id$'
__all__ = ['new', 'digest_size', 'MD5Hash']
from Crypto.Util.py3compat import *
from Crypto.Hash.hashalgo import HashAlgo
try:
    import hashlib
    hashFactory = hashlib.md5
except ImportError:
    import md5
    hashFactory = md5

class MD5Hash(HashAlgo):
    """Class that implements an MD5 hash
    
    :undocumented: block_size
    """
    oid = b('*†H†÷\r')
    digest_size = 16
    block_size = 64

    def __init__(self, data = None):
        HashAlgo.__init__(self, hashFactory, data)

    def new(self, data = None):
        return MD5Hash(data)


def new(data = None):
    """Return a fresh instance of the hash object.
    
    :Parameters:
       data : byte string
        The very first chunk of the message to hash.
        It is equivalent to an early call to `MD5Hash.update()`.
        Optional.
    
    :Return: A `MD5Hash` object
    """
    return MD5Hash().new(data)


digest_size = MD5Hash.digest_size
block_size = MD5Hash.block_size
