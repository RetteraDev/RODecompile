#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Hash/MD2.o
"""MD2 cryptographic hash algorithm.

MD2 is specified in RFC1319_ and it produces the 128 bit digest of a message.

    >>> from Crypto.Hash import MD2
    >>>
    >>> h = MD2.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

MD2 stand for Message Digest version 2, and it was invented by Rivest in 1989.

This algorithm is both slow and insecure. Do not use it for new designs.

.. _RFC1319: http://tools.ietf.org/html/rfc1319
"""
_revision__ = '$Id$'
__all__ = ['new', 'digest_size', 'MD2Hash']
from Crypto.Util.py3compat import *
from Crypto.Hash.hashalgo import HashAlgo
import Crypto.Hash._MD2 as _MD2
hashFactory = _MD2

class MD2Hash(HashAlgo):
    """Class that implements an MD2 hash
    
    :undocumented: block_size
    """
    oid = b('*†H†÷\r')
    digest_size = 16
    block_size = 16

    def __init__(self, data = None):
        HashAlgo.__init__(self, hashFactory, data)

    def new(self, data = None):
        return MD2Hash(data)


def new(data = None):
    """Return a fresh instance of the hash object.
    
    :Parameters:
       data : byte string
        The very first chunk of the message to hash.
        It is equivalent to an early call to `MD2Hash.update()`.
        Optional.
    
    :Return: An `MD2Hash` object
    """
    return MD2Hash().new(data)


digest_size = MD2Hash.digest_size
block_size = MD2Hash.block_size
