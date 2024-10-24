#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\pyasn1\codec\der/encoder.o
from pyasn1.type import univ
from pyasn1.codec.cer import encoder

class SetOfEncoder(encoder.SetOfEncoder):

    def _cmpSetComponents(self, c1, c2):
        return cmp(getattr(c1, 'getEffectiveTagSet', c1.getTagSet)(), getattr(c2, 'getEffectiveTagSet', c2.getTagSet)())


codecMap = encoder.codecMap.copy()
codecMap.update({univ.BitString.tagSet: encoder.encoder.BitStringEncoder(),
 univ.OctetString.tagSet: encoder.encoder.OctetStringEncoder(),
 univ.SetOf().tagSet: SetOfEncoder()})

class Encoder(encoder.Encoder):

    def __call__(self, client, defMode = 1, maxChunkSize = 0):
        return encoder.Encoder.__call__(self, client, defMode, maxChunkSize)


encode = Encoder(codecMap)
