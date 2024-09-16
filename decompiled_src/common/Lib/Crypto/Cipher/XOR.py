#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Cipher/XOR.o
"""XOR toy cipher

XOR is one the simplest stream ciphers. Encryption and decryption are
performed by XOR-ing data with a keystream made by contatenating
the key.

Do not use it for real applications!

:undocumented: __revision__, __package__
"""
__revision__ = '$Id$'
from Crypto.Cipher import _XOR

class XORCipher:
    """XOR cipher object"""

    def __init__(self, key, *args, **kwargs):
        """Initialize a XOR cipher object
        
        See also `new()` at the module level."""
        self._cipher = _XOR.new(key, *args, **kwargs)
        self.block_size = self._cipher.block_size
        self.key_size = self._cipher.key_size

    def encrypt(self, plaintext):
        """Encrypt a piece of data.
        
        :Parameters:
          plaintext : byte string
            The piece of data to encrypt. It can be of any size.
        :Return: the encrypted data (byte string, as long as the
          plaintext).
        """
        return self._cipher.encrypt(plaintext)

    def decrypt(self, ciphertext):
        """Decrypt a piece of data.
        
        :Parameters:
          ciphertext : byte string
            The piece of data to decrypt. It can be of any size.
        :Return: the decrypted data (byte string, as long as the
          ciphertext).
        """
        return self._cipher.decrypt(ciphertext)


def new(key, *args, **kwargs):
    """Create a new XOR cipher
    
    :Parameters:
      key : byte string
        The secret key to use in the symmetric cipher.
        Its length may vary from 1 to 32 bytes.
    
    :Return: an `XORCipher` object
    """
    return XORCipher(key, *args, **kwargs)


block_size = 1
key_size = xrange(1, 33)
