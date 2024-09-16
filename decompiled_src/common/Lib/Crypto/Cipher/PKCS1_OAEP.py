#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Cipher/PKCS1_OAEP.o
"""RSA encryption protocol according to PKCS#1 OAEP

See RFC3447__ or the `original RSA Labs specification`__ .

This scheme is more properly called ``RSAES-OAEP``.

As an example, a sender may encrypt a message in this way:

        >>> from Crypto.Cipher import PKCS1_OAEP
        >>> from Crypto.PublicKey import RSA
        >>>
        >>> message = 'To be encrypted'
        >>> key = RSA.importKey(open('pubkey.der').read())
        >>> cipher = PKCS1_OAEP.new(key)
        >>> ciphertext = cipher.encrypt(message)

At the receiver side, decryption can be done using the private part of
the RSA key:

        >>> key = RSA.importKey(open('privkey.der').read())
        >>> cipher = PKCS1_OAP.new(key)
        >>> message = cipher.decrypt(ciphertext)

:undocumented: __revision__, __package__

.. __: http://www.ietf.org/rfc/rfc3447.txt
.. __: http://www.rsa.com/rsalabs/node.asp?id=2125.
"""
from __future__ import nested_scopes
__revision__ = '$Id$'
__all__ = ['new', 'PKCS1OAEP_Cipher']
import Crypto.Signature.PKCS1_PSS
import Crypto.Hash.SHA
from Crypto.Util.py3compat import *
import Crypto.Util.number
from Crypto.Util.number import ceil_div
from Crypto.Util.strxor import strxor

class PKCS1OAEP_Cipher:
    """This cipher can perform PKCS#1 v1.5 OAEP encryption or decryption."""

    def __init__(self, key, hashAlgo, mgfunc, label):
        """Initialize this PKCS#1 OAEP cipher object.
        
        :Parameters:
         key : an RSA key object
          If a private half is given, both encryption and decryption are possible.
          If a public half is given, only encryption is possible.
         hashAlgo : hash object
                The hash function to use. This can be a module under `Crypto.Hash`
                or an existing hash object created from any of such modules. If not specified,
                `Crypto.Hash.SHA` (that is, SHA-1) is used.
         mgfunc : callable
                A mask generation function that accepts two parameters: a string to
                use as seed, and the lenth of the mask to generate, in bytes.
                If not specified, the standard MGF1 is used (a safe choice).
         label : string
                A label to apply to this particular encryption. If not specified,
                an empty string is used. Specifying a label does not improve
                security.
        
        :attention: Modify the mask generation function only if you know what you are doing.
                    Sender and receiver must use the same one.
        """
        self._key = key
        if hashAlgo:
            self._hashObj = hashAlgo
        else:
            self._hashObj = Crypto.Hash.SHA
        if mgfunc:
            self._mgf = mgfunc
        else:
            self._mgf = lambda x, y: Crypto.Signature.PKCS1_PSS.MGF1(x, y, self._hashObj)
        self._label = label

    def can_encrypt(self):
        """Return True/1 if this cipher object can be used for encryption."""
        return self._key.can_encrypt()

    def can_decrypt(self):
        """Return True/1 if this cipher object can be used for decryption."""
        return self._key.can_decrypt()

    def encrypt(self, message):
        """Produce the PKCS#1 OAEP encryption of a message.
        
        This function is named ``RSAES-OAEP-ENCRYPT``, and is specified in
        section 7.1.1 of RFC3447.
        
        :Parameters:
         message : string
                The message to encrypt, also known as plaintext. It can be of
                variable length, but not longer than the RSA modulus (in bytes)
                minus 2, minus twice the hash output size.
        
        :Return: A string, the ciphertext in which the message is encrypted.
            It is as long as the RSA modulus (in bytes).
        :Raise ValueError:
            If the RSA key length is not sufficiently long to deal with the given
            message.
        """
        randFunc = self._key._randfunc
        modBits = Crypto.Util.number.size(self._key.n)
        k = ceil_div(modBits, 8)
        hLen = self._hashObj.digest_size
        mLen = len(message)
        ps_len = k - mLen - 2 * hLen - 2
        if ps_len < 0:
            raise ValueError('Plaintext is too long.')
        lHash = self._hashObj.new(self._label).digest()
        ps = bchr(0) * ps_len
        db = lHash + ps + bchr(1) + message
        ros = randFunc(hLen)
        dbMask = self._mgf(ros, k - hLen - 1)
        maskedDB = strxor(db, dbMask)
        seedMask = self._mgf(maskedDB, hLen)
        maskedSeed = strxor(ros, seedMask)
        em = bchr(0) + maskedSeed + maskedDB
        m = self._key.encrypt(em, 0)[0]
        c = bchr(0) * (k - len(m)) + m
        return c

    def decrypt(self, ct):
        """Decrypt a PKCS#1 OAEP ciphertext.
        
        This function is named ``RSAES-OAEP-DECRYPT``, and is specified in
        section 7.1.2 of RFC3447.
        
        :Parameters:
         ct : string
                The ciphertext that contains the message to recover.
        
        :Return: A string, the original message.
        :Raise ValueError:
            If the ciphertext length is incorrect, or if the decryption does not
            succeed.
        :Raise TypeError:
            If the RSA key has no private half.
        """
        modBits = Crypto.Util.number.size(self._key.n)
        k = ceil_div(modBits, 8)
        hLen = self._hashObj.digest_size
        if len(ct) != k or k < hLen + 2:
            raise ValueError('Ciphertext with incorrect length.')
        m = self._key.decrypt(ct)
        em = bchr(0) * (k - len(m)) + m
        lHash = self._hashObj.new(self._label).digest()
        y = em[0]
        maskedSeed = em[1:hLen + 1]
        maskedDB = em[hLen + 1:]
        seedMask = self._mgf(maskedDB, hLen)
        seed = strxor(maskedSeed, seedMask)
        dbMask = self._mgf(seed, k - hLen - 1)
        db = strxor(maskedDB, dbMask)
        valid = 1
        one = db[hLen:].find(bchr(1))
        lHash1 = db[:hLen]
        if lHash1 != lHash:
            valid = 0
        if one < 0:
            valid = 0
        if bord(y) != 0:
            valid = 0
        if not valid:
            raise ValueError('Incorrect decryption.')
        return db[hLen + one + 1:]


def new(key, hashAlgo = None, mgfunc = None, label = b('')):
    """Return a cipher object `PKCS1OAEP_Cipher` that can be used to perform PKCS#1 OAEP encryption or decryption.
    
    :Parameters:
     key : RSA key object
      The key to use to encrypt or decrypt the message. This is a `Crypto.PublicKey.RSA` object.
      Decryption is only possible if *key* is a private RSA key.
     hashAlgo : hash object
      The hash function to use. This can be a module under `Crypto.Hash`
      or an existing hash object created from any of such modules. If not specified,
      `Crypto.Hash.SHA` (that is, SHA-1) is used.
     mgfunc : callable
      A mask generation function that accepts two parameters: a string to
      use as seed, and the lenth of the mask to generate, in bytes.
      If not specified, the standard MGF1 is used (a safe choice).
     label : string
      A label to apply to this particular encryption. If not specified,
      an empty string is used. Specifying a label does not improve
      security.
    
    :attention: Modify the mask generation function only if you know what you are doing.
      Sender and receiver must use the same one.
    """
    return PKCS1OAEP_Cipher(key, hashAlgo, mgfunc, label)
