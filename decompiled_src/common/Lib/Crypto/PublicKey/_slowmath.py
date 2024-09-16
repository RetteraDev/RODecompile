#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\PublicKey/_slowmath.o
"""Pure Python implementation of the RSA-related portions of Crypto.PublicKey._fastmath."""
__revision__ = '$Id$'
__all__ = ['rsa_construct']
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from Crypto.Util.py21compat import *
from Crypto.Util.number import size, inverse, GCD

class error(Exception):
    pass


class _RSAKey(object):

    def _blind(self, m, r):
        return m * pow(r, self.e, self.n)

    def _unblind(self, m, r):
        return inverse(r, self.n) * m % self.n

    def _decrypt(self, c):
        if not self.has_private():
            raise TypeError('No private key')
        if hasattr(self, 'p') and hasattr(self, 'q') and hasattr(self, 'u'):
            m1 = pow(c, self.d % (self.p - 1), self.p)
            m2 = pow(c, self.d % (self.q - 1), self.q)
            h = m2 - m1
            if h < 0:
                h = h + self.q
            h = h * self.u % self.q
            return h * self.p + m1
        return pow(c, self.d, self.n)

    def _encrypt(self, m):
        return pow(m, self.e, self.n)

    def _sign(self, m):
        if not self.has_private():
            raise TypeError('No private key')
        return self._decrypt(m)

    def _verify(self, m, sig):
        return self._encrypt(sig) == m

    def has_private(self):
        return hasattr(self, 'd')

    def size(self):
        """Return the maximum number of bits that can be encrypted"""
        return size(self.n) - 1


def rsa_construct(n, e, d = None, p = None, q = None, u = None):
    """Construct an RSAKey object"""
    assert isinstance(n, long)
    assert isinstance(e, long)
    assert isinstance(d, (long, type(None)))
    assert isinstance(p, (long, type(None)))
    assert isinstance(q, (long, type(None)))
    assert isinstance(u, (long, type(None)))
    obj = _RSAKey()
    obj.n = n
    obj.e = e
    if d is None:
        return obj
    obj.d = d
    if p is not None and q is not None:
        obj.p = p
        obj.q = q
    else:
        ktot = d * e - 1
        t = ktot
        while t % 2 == 0:
            t = divmod(t, 2)[0]

        spotted = 0
        a = 2
        while not spotted and a < 100:
            k = t
            while k < ktot:
                cand = pow(a, k, n)
                if cand != 1 and cand != n - 1 and pow(cand, 2, n) == 1:
                    obj.p = GCD(cand + 1, n)
                    spotted = 1
                    break
                k = k * 2

            a = a + 2

        if not spotted:
            raise ValueError('Unable to compute factors p and q from exponent d.')
        assert n % obj.p == 0
        obj.q = divmod(n, obj.p)[0]
    if u is not None:
        obj.u = u
    else:
        obj.u = inverse(obj.p, obj.q)
    return obj


class _DSAKey(object):

    def size(self):
        """Return the maximum number of bits that can be encrypted"""
        return size(self.p) - 1

    def has_private(self):
        return hasattr(self, 'x')

    def _sign(self, m, k):
        if not self.has_private():
            raise TypeError('No private key')
        if not 1L < k < self.q:
            raise ValueError('k is not between 2 and q-1')
        inv_k = inverse(k, self.q)
        r = pow(self.g, k, self.p) % self.q
        s = inv_k * (m + self.x * r) % self.q
        return (r, s)

    def _verify(self, m, r, s):
        if not 0 < r < self.q or not 0 < s < self.q:
            return False
        w = inverse(s, self.q)
        u1 = m * w % self.q
        u2 = r * w % self.q
        v = pow(self.g, u1, self.p) * pow(self.y, u2, self.p) % self.p % self.q
        return v == r


def dsa_construct(y, g, p, q, x = None):
    assert isinstance(y, long)
    assert isinstance(g, long)
    assert isinstance(p, long)
    assert isinstance(q, long)
    assert isinstance(x, (long, type(None)))
    obj = _DSAKey()
    obj.y = y
    obj.g = g
    obj.p = p
    obj.q = q
    if x is not None:
        obj.x = x
    return obj
