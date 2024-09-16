#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Cipher/DES.o
"""DES symmetric cipher

DES `(Data Encryption Standard)`__ is a symmetric block cipher standardized
by NIST_ . It has a fixed data block size of 8 bytes.
Its keys are 64 bits long, even though 8 bits were used for integrity (now they
are ignored) and do not contribute to securty.

DES is cryptographically secure, but its key length is too short by nowadays
standards and it could be brute forced with some effort.

DES should not be used for new designs. Use `AES`.

As an example, encryption can be done as follows:

    >>> from Crypto.Cipher import DES3
    >>> from Crypto import Random
    >>>
    >>> key = b'Sixteen byte key'
    >>> iv = Random.new().read(DES3.block_size)
    >>> cipher = DES3.new(key, DES3.MODE_OFB, iv)
    >>> plaintext = b'sona si latine loqueris '
    >>> msg = iv + cipher.encrypt(plaintext)

.. __: http://en.wikipedia.org/wiki/Data_Encryption_Standard
.. _NIST: http://csrc.nist.gov/publications/fips/fips46-3/fips46-3.pdf

:undocumented: __revision__, __package__
"""
__revision__ = '$Id$'
from Crypto.Cipher import blockalgo
from Crypto.Cipher import _DES

class DESCipher(blockalgo.BlockAlgo):
    """DES cipher object"""

    def __init__(self, key, *args, **kwargs):
        """Initialize a DES cipher object
        
        See also `new()` at the module level."""
        blockalgo.BlockAlgo.__init__(self, _DES, key, *args, **kwargs)


def new(key, *args, **kwargs):
    """Create a new DES cipher
    
    :Parameters:
      key : byte string
        The secret key to use in the symmetric cipher.
        It must be 8 byte long. The parity bits will be ignored.
    :Keywords:
      mode : a *MODE_** constant
        The chaining mode to use for encryption or decryption.
        Default is `MODE_ECB`.
      IV : byte string
        The initialization vector to use for encryption or decryption.
        
        It is ignored for `MODE_ECB` and `MODE_CTR`.
    
        For `MODE_OPENPGP`, IV must be `block_size` bytes long for encryption
        and `block_size` +2 bytes for decryption (in the latter case, it is
        actually the *encrypted* IV which was prefixed to the ciphertext).
        It is mandatory.
       
        For all other modes, it must be `block_size` bytes longs. It is optional and
        when not present it will be given a default value of all zeroes.
      counter : callable
        (*Only* `MODE_CTR`). A stateful function that returns the next
        *counter block*, which is a byte string of `block_size` bytes.
        For better performance, use `Crypto.Util.Counter`.
      segment_size : integer
        (*Only* `MODE_CFB`).The number of bits the plaintext and ciphertext
        are segmented in.
        It must be a multiple of 8. If 0 or not specified, it will be assumed to be 8.
    
    :Return: an `DESCipher` object
    """
    return DESCipher(key, *args, **kwargs)


MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_PGP = 4
MODE_OFB = 5
MODE_CTR = 6
MODE_OPENPGP = 7
block_size = 8
key_size = 8
