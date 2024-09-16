#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\PublicKey/qNEW.o
__revision__ = '$Id$'
from Crypto.PublicKey import pubkey
from Crypto.Util.number import *
from Crypto.Hash import SHA

class error(Exception):
    pass


HASHBITS = 160

def generate(bits, randfunc, progress_func = None):
    """generate(bits:int, randfunc:callable, progress_func:callable)
    
    Generate a qNEW key of length 'bits', using 'randfunc' to get
    random data and 'progress_func', if present, to display
    the progress of the key generation.
    """
    obj = qNEWobj()
    if progress_func:
        progress_func('p,q\n')
    while 1:
        obj.q = getPrime(160, randfunc)
        obj.seed = S = long_to_bytes(obj.q)
        C, N, V = 0, 2, {}
        n = (bits - 1) / HASHBITS
        b = (bits - 1) % HASHBITS
        powb = 2L << b
        powL1 = pow(long(2), bits - 1)
        while C < 4096:
            for k in range(0, n + 1):
                V[k] = bytes_to_long(SHA.new(S + str(N) + str(k)).digest())

            p = V[n] % powb
            for k in range(n - 1, -1, -1):
                p = (p << long(HASHBITS)) + V[k]

            p = p + powL1
            p = p - (p % (2 * obj.q) - 1)
            if powL1 <= p and isPrime(p):
                break
            C, N = C + 1, N + n + 1

        if C < 4096:
            break
        if progress_func:
            progress_func('4096 values of p tried\n')

    obj.p = p
    power = (p - 1) / obj.q
    if progress_func:
        progress_func('h,g\n')
    while 1:
        h = bytes_to_long(randfunc(bits)) % (p - 1)
        g = pow(h, power, p)
        if 1 < h < p - 1 and g > 1:
            break

    obj.g = g
    if progress_func:
        progress_func('x,y\n')
    while 1:
        x = bytes_to_long(randfunc(20))
        if 0 < x < obj.q:
            break

    obj.x, obj.y = x, pow(g, x, p)
    return obj


def construct(tuple):
    """construct(tuple:(long,long,long,long)|(long,long,long,long,long)
    Construct a qNEW object from a 4- or 5-tuple of numbers.
    """
    obj = qNEWobj()
    if len(tuple) not in (4, 5):
        raise error, 'argument for construct() wrong length'
    for i in range(len(tuple)):
        field = obj.keydata[i]
        setattr(obj, field, tuple[i])

    return obj


class qNEWobj(pubkey.pubkey):
    keydata = ['p',
     'q',
     'g',
     'y',
     'x']

    def _sign(self, M, K = ''):
        if self.q <= K:
            raise error, 'K is greater than q'
        if M < 0:
            raise error, 'Illegal value of M (<0)'
        if M >= pow(2, 161L):
            raise error, 'Illegal value of M (too large)'
        r = pow(self.g, K, self.p) % self.q
        s = (K - r * M * self.x % self.q) % self.q
        return (r, s)

    def _verify(self, M, sig):
        r, s = sig
        if r <= 0 or r >= self.q or s <= 0 or s >= self.q:
            return 0
        if M < 0:
            raise error, 'Illegal value of M (<0)'
        if M <= 0 or M >= pow(2, 161L):
            return 0
        v1 = pow(self.g, s, self.p)
        v2 = pow(self.y, M * r, self.p)
        v = v1 * v2 % self.p
        v = v % self.q
        if v == r:
            return 1
        return 0

    def size(self):
        """Return the maximum number of bits that can be handled by this key."""
        return 160

    def has_private(self):
        """Return a Boolean denoting whether the object contains
        private components."""
        return hasattr(self, 'x')

    def can_sign(self):
        """Return a Boolean value recording whether this algorithm can generate signatures."""
        return 1

    def can_encrypt(self):
        """Return a Boolean value recording whether this algorithm can encrypt data."""
        return 0

    def publickey(self):
        """Return a new key object containing only the public information."""
        return construct((self.p,
         self.q,
         self.g,
         self.y))


object = qNEWobj
