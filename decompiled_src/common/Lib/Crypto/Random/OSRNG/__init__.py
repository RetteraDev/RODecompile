#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Random\OSRNG/__init__.o
"""Provides a platform-independent interface to the random number generators
supplied by various operating systems."""
__revision__ = '$Id$'
import os
if os.name == 'posix':
    from Crypto.Random.OSRNG.posix import new
elif os.name == 'nt':
    from Crypto.Random.OSRNG.nt import new
elif hasattr(os, 'urandom'):
    from Crypto.Random.OSRNG.fallback import new
else:
    raise ImportError('Not implemented')
