#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\PublicKey/__init__.o
"""Public-key encryption and signature algorithms.

Public-key encryption uses two different keys, one for encryption and
one for decryption.  The encryption key can be made public, and the
decryption key is kept private.  Many public-key algorithms can also
be used to sign messages, and some can *only* be used for signatures.

========================  =============================================
Module                    Description
========================  =============================================
Crypto.PublicKey.DSA      Digital Signature Algorithm (Signature only)
Crypto.PublicKey.ElGamal  (Signing and encryption)
Crypto.PublicKey.RSA      (Signing, encryption, and blinding)
========================  =============================================

:undocumented: _DSA, _RSA, _fastmath, _slowmath, pubkey
"""
__all__ = ['RSA', 'DSA', 'ElGamal']
__revision__ = '$Id$'
