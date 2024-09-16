#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\keyczar/errors.o
"""
Contains hierarchy of all possible exceptions thrown by Keyczar.

@author: arkajit.dey@gmail.com (Arkajit Dey)
"""

class KeyczarError(Exception):
    """Indicates exceptions raised by a Keyczar class."""
    pass


class BadVersionError(KeyczarError):
    """Indicates a bad version number was received."""

    def __init__(self, version):
        KeyczarError.__init__(self, 'Received a bad version number: ' + str(version))


class Base64DecodingError(KeyczarError):
    """Indicates an error while performing Base 64 decoding."""
    pass


class InvalidSignatureError(KeyczarError):
    """Indicates an invalid ciphertext signature."""

    def __init__(self):
        KeyczarError.__init__(self, 'Invalid ciphertext signature')


class KeyNotFoundError(KeyczarError):
    """Indicates a key with a certain hash id was not found."""

    def __init__(self, hash):
        KeyczarError.__init__(self, 'Key with hash identifier %s not found.' % hash)


class ShortCiphertextError(KeyczarError):
    """Indicates a ciphertext too short to be valid."""

    def __init__(self, length):
        KeyczarError.__init__(self, 'Input of length %s is too short to be valid ciphertext.' % length)


class ShortSignatureError(KeyczarError):
    """Indicates a signature too short to be valid."""

    def __init__(self, length):
        KeyczarError.__init__(self, 'Input of length %s is too short to be valid signature.' % length)


class NoPrimaryKeyError(KeyNotFoundError):
    """Indicates missing primary key."""

    def __init__(self):
        KeyczarError.__init__(self, 'No primary key found')
