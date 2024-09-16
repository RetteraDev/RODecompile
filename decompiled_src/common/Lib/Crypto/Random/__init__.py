#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Random/__init__.o
__revision__ = '$Id$'
__all__ = ['new']
from Crypto.Random import OSRNG
from Crypto.Random import _UserFriendlyRNG

def new(*args, **kwargs):
    """Return a file-like object that outputs cryptographically random bytes."""
    return _UserFriendlyRNG.new(*args, **kwargs)


def atfork():
    """Call this whenever you call os.fork()"""
    _UserFriendlyRNG.reinit()


def get_random_bytes(n):
    """Return the specified number of cryptographically-strong random bytes."""
    return _UserFriendlyRNG.get_random_bytes(n)
