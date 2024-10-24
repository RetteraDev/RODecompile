#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\Crypto\Hash/hashalgo.o
from binascii import hexlify

class HashAlgo:
    """A generic class for an abstract cryptographic hash algorithm.
    
    :undocumented: block_size
    """
    digest_size = None
    block_size = None

    def __init__(self, hashFactory, data = None):
        """Initialize the hash object.
        
        :Parameters:
         hashFactory : callable
            An object that will generate the actual hash implementation.
            *hashFactory* must have a *new()* method, or must be directly
            callable.
         data : byte string
            The very first chunk of the message to hash.
            It is equivalent to an early call to `update()`.
        """
        if hasattr(hashFactory, 'new'):
            self._hash = hashFactory.new()
        else:
            self._hash = hashFactory()
        if data:
            self.update(data)

    def update(self, data):
        """Continue hashing of a message by consuming the next chunk of data.
        
        Repeated calls are equivalent to a single call with the concatenation
        of all the arguments. In other words:
        
           >>> m.update(a); m.update(b)
           
        is equivalent to:
        
           >>> m.update(a+b)
        
        :Parameters:
          data : byte string
            The next chunk of the message being hashed.
        """
        return self._hash.update(data)

    def digest(self):
        """Return the **binary** (non-printable) digest of the message that has been hashed so far.
        
        This method does not change the state of the hash object.
        You can continue updating the object after calling this function.
        
        :Return: A byte string of `digest_size` bytes. It may contain non-ASCII
         characters, including null bytes.
        """
        return self._hash.digest()

    def hexdigest(self):
        """Return the **printable** digest of the message that has been hashed so far.
        
        This method does not change the state of the hash object.
        
        :Return: A string of 2* `digest_size` characters. It contains only
         hexadecimal ASCII digits.
        """
        return self._hash.hexdigest()

    def copy(self):
        """Return a copy ("clone") of the hash object.
        
        The copy will have the same internal state as the original hash
        object.
        This can be used to efficiently compute the digests of strings that
        share a common initial substring.
        
        :Return: A hash object of the same type
        """
        return self._hash.copy()

    def new(self, data = None):
        """Return a fresh instance of the hash object.
        
        Unlike the `copy` method, the internal state of the object is empty.
        
        :Parameters:
          data : byte string
            The next chunk of the message being hashed.
        
        :Return: A hash object of the same type
        """
        pass
