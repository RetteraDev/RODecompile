#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Signature/PKCS1_PSS.o
"""RSA digital signature protocol with appendix according to PKCS#1 PSS.

See RFC3447__ or the `original RSA Labs specification`__.

This scheme is more properly called ``RSASSA-PSS``.

For example, a sender may authenticate a message using SHA-1 and PSS like
this:

    >>> from Crypto.Signature import PKCS1_PSS
    >>> from Crypto.Hash import SHA
    >>> from Crypto.PublicKey import RSA
    >>> from Crypto import Random
    >>>
    >>> message = 'To be signed'
    >>> key = RSA.importKey(open('privkey.der').read())
    >>> h = SHA.new()
    >>> h.update(message)
    >>> signer = PKCS1_PSS.new(key)
    >>> signature = PKCS1_PSS.sign(key)

At the receiver side, verification can be done like using the public part of
the RSA key:

    >>> key = RSA.importKey(open('pubkey.der').read())
    >>> h = SHA.new()
    >>> h.update(message)
    >>> verifier = PKCS1_PSS.new(key)
    >>> if verifier.verify(h, signature):
    >>>     print "The signature is authentic."
    >>> else:
    >>>     print "The signature is not authentic."

:undocumented: __revision__, __package__

.. __: http://www.ietf.org/rfc/rfc3447.txt
.. __: http://www.rsa.com/rsalabs/node.asp?id=2125
"""
from __future__ import nested_scopes
__revision__ = '$Id$'
__all__ = ['new', 'PSS_SigScheme']
from Crypto.Util.py3compat import *
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from Crypto.Util.py21compat import *
import Crypto.Util.number
from Crypto.Util.number import ceil_shift, ceil_div, long_to_bytes
from Crypto.Util.strxor import strxor

class PSS_SigScheme:
    """This signature scheme can perform PKCS#1 PSS RSA signature or verification."""

    def __init__(self, key, mgfunc, saltLen):
        """Initialize this PKCS#1 PSS signature scheme object.
        
        :Parameters:
         key : an RSA key object
                If a private half is given, both signature and verification are possible.
                If a public half is given, only verification is possible.
         mgfunc : callable
                A mask generation function that accepts two parameters: a string to
                use as seed, and the lenth of the mask to generate, in bytes.
         saltLen : int
                Length of the salt, in bytes.
        """
        self._key = key
        self._saltLen = saltLen
        self._mgfunc = mgfunc

    def can_sign(self):
        """Return True if this cipher object can be used for signing messages."""
        return self._key.has_private()

    def sign(self, mhash):
        """Produce the PKCS#1 PSS signature of a message.
        
        This function is named ``RSASSA-PSS-SIGN``, and is specified in
        section 8.1.1 of RFC3447.
        
        :Parameters:
         mhash : hash object
                The hash that was carried out over the message. This is an object
                belonging to the `Crypto.Hash` module.
        
        :Return: The PSS signature encoded as a string.
        :Raise ValueError:
            If the RSA key length is not sufficiently long to deal with the given
            hash algorithm.
        :Raise TypeError:
            If the RSA key has no private half.
        
        :attention: Modify the salt length and the mask generation function only
                    if you know what you are doing.
                    The receiver must use the same parameters too.
        """
        randfunc = self._key._randfunc
        if self._saltLen == None:
            sLen = mhash.digest_size
        else:
            sLen = self._saltLen
        if self._mgfunc:
            mgf = self._mgfunc
        else:
            mgf = lambda x, y: MGF1(x, y, mhash)
        modBits = Crypto.Util.number.size(self._key.n)
        k = ceil_div(modBits, 8)
        em = EMSA_PSS_ENCODE(mhash, modBits - 1, randfunc, mgf, sLen)
        m = self._key.decrypt(em)
        S = bchr(0) * (k - len(m)) + m
        return S

    def verify(self, mhash, S):
        """Verify that a certain PKCS#1 PSS signature is authentic.
        
        This function checks if the party holding the private half of the given
        RSA key has really signed the message.
        
        This function is called ``RSASSA-PSS-VERIFY``, and is specified in section
        8.1.2 of RFC3447.
        
        :Parameters:
         mhash : hash object
                The hash that was carried out over the message. This is an object
                belonging to the `Crypto.Hash` module.
         S : string
                The signature that needs to be validated.
        
        :Return: True if verification is correct. False otherwise.
        """
        if self._saltLen == None:
            sLen = mhash.digest_size
        else:
            sLen = self._saltLen
        if self._mgfunc:
            mgf = self._mgfunc
        else:
            mgf = lambda x, y: MGF1(x, y, mhash)
        modBits = Crypto.Util.number.size(self._key.n)
        k = ceil_div(modBits, 8)
        if len(S) != k:
            return False
        em = self._key.encrypt(S, 0)[0]
        emLen = ceil_div(modBits - 1, 8)
        em = bchr(0) * (emLen - len(em)) + em
        try:
            result = EMSA_PSS_VERIFY(mhash, em, modBits - 1, mgf, sLen)
        except ValueError:
            return False

        return result


def MGF1(mgfSeed, maskLen, hash):
    """Mask Generation Function, described in B.2.1"""
    T = b('')
    for counter in xrange(ceil_div(maskLen, hash.digest_size)):
        c = long_to_bytes(counter, 4)
        T = T + hash.new(mgfSeed + c).digest()

    assert len(T) >= maskLen
    return T[:maskLen]


def EMSA_PSS_ENCODE(mhash, emBits, randFunc, mgf, sLen):
    r"""
    Implement the ``EMSA-PSS-ENCODE`` function, as defined
    in PKCS#1 v2.1 (RFC3447, 9.1.1).
    
    The original ``EMSA-PSS-ENCODE`` actually accepts the message ``M`` as input,
    and hash it internally. Here, we expect that the message has already
    been hashed instead.
    
    :Parameters:
     mhash : hash object
            The hash object that holds the digest of the message being signed.
     emBits : int
            Maximum length of the final encoding, in bits.
     randFunc : callable
            An RNG function that accepts as only parameter an int, and returns
            a string of random bytes, to be used as salt.
     mgf : callable
            A mask generation function that accepts two parameters: a string to
            use as seed, and the lenth of the mask to generate, in bytes.
     sLen : int
            Length of the salt, in bytes.
    
    :Return: An ``emLen`` byte long string that encodes the hash
            (with ``emLen = \ceil(emBits/8)``).
    
    :Raise ValueError:
        When digest or salt length are too big.
    """
    emLen = ceil_div(emBits, 8)
    lmask = 0
    for i in xrange(8 * emLen - emBits):
        lmask = lmask >> 1 | 128

    if emLen < mhash.digest_size + sLen + 2:
        raise ValueError('Digest or salt length are too long for given key size.')
    salt = b('')
    if randFunc and sLen > 0:
        salt = randFunc(sLen)
    h = mhash.new(bchr(0) * 8 + mhash.digest() + salt)
    db = bchr(0) * (emLen - sLen - mhash.digest_size - 2) + bchr(1) + salt
    dbMask = mgf(h.digest(), emLen - mhash.digest_size - 1)
    maskedDB = strxor(db, dbMask)
    maskedDB = bchr(bord(maskedDB[0]) & ~lmask) + maskedDB[1:]
    em = maskedDB + h.digest() + bchr(188)
    return em


def EMSA_PSS_VERIFY(mhash, em, emBits, mgf, sLen):
    """
    Implement the ``EMSA-PSS-VERIFY`` function, as defined
    in PKCS#1 v2.1 (RFC3447, 9.1.2).
    
    ``EMSA-PSS-VERIFY`` actually accepts the message ``M`` as input,
    and hash it internally. Here, we expect that the message has already
    been hashed instead.
    
    :Parameters:
     mhash : hash object
            The hash object that holds the digest of the message to be verified.
     em : string
            The signature to verify, therefore proving that the sender really signed
            the message that was received.
     emBits : int
            Length of the final encoding (em), in bits.
     mgf : callable
            A mask generation function that accepts two parameters: a string to
            use as seed, and the lenth of the mask to generate, in bytes.
     sLen : int
            Length of the salt, in bytes.
    
    :Return: 0 if the encoding is consistent, 1 if it is inconsistent.
    
    :Raise ValueError:
        When digest or salt length are too big.
    """
    emLen = ceil_div(emBits, 8)
    lmask = 0
    for i in xrange(8 * emLen - emBits):
        lmask = lmask >> 1 | 128

    if emLen < mhash.digest_size + sLen + 2:
        return False
    if ord(em[-1:]) != 188:
        return False
    maskedDB = em[:emLen - mhash.digest_size - 1]
    h = em[emLen - mhash.digest_size - 1:-1]
    if lmask & bord(em[0]):
        return False
    dbMask = mgf(h, emLen - mhash.digest_size - 1)
    db = strxor(maskedDB, dbMask)
    db = bchr(bord(db[0]) & ~lmask) + db[1:]
    if not db.startswith(bchr(0) * (emLen - mhash.digest_size - sLen - 2) + bchr(1)):
        return False
    salt = b('')
    if sLen:
        salt = db[-sLen:]
    hp = mhash.new(bchr(0) * 8 + mhash.digest() + salt).digest()
    if h != hp:
        return False
    return True


def new(key, mgfunc = None, saltLen = None):
    """Return a signature scheme object `PSS_SigScheme` that
    can be used to perform PKCS#1 PSS signature or verification.
    
    :Parameters:
     key : RSA key object
        The key to use to sign or verify the message. This is a `Crypto.PublicKey.RSA` object.
        Signing is only possible if *key* is a private RSA key.
     mgfunc : callable
        A mask generation function that accepts two parameters: a string to
        use as seed, and the lenth of the mask to generate, in bytes.
        If not specified, the standard MGF1 is used.
     saltLen : int
        Length of the salt, in bytes. If not specified, it matches the output
        size of the hash function.
    
    """
    return PSS_SigScheme(key, mgfunc, saltLen)
