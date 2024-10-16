#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\pyasn1\codec\cer/encoder.o
import string
from pyasn1.type import univ
from pyasn1.codec.ber import encoder

class BooleanEncoder(encoder.IntegerEncoder):

    def _encodeValue(self, encodeFun, client, defMode, maxChunkSize):
        if client == 0:
            substrate = ' '
        else:
            substrate = '�'
        return (substrate, 0)


class BitStringEncoder(encoder.BitStringEncoder):

    def _encodeValue(self, encodeFun, client, defMode, maxChunkSize):
        return encoder.BitStringEncoder._encodeValue(self, encodeFun, client, defMode, 1000)


class OctetStringEncoder(encoder.OctetStringEncoder):

    def _encodeValue(self, encodeFun, client, defMode, maxChunkSize):
        return encoder.OctetStringEncoder._encodeValue(self, encodeFun, client, defMode, 1000)


class SetOfEncoder(encoder.SequenceOfEncoder):

    def _cmpSetComponents(self, c1, c2):
        return cmp(getattr(c1, 'getMinimalTagSet', c1.getTagSet)(), getattr(c2, 'getMinimalTagSet', c2.getTagSet)())

    def _encodeValue(self, encodeFun, client, defMode, maxChunkSize):
        if hasattr(client, 'setDefaultComponents'):
            client.setDefaultComponents()
        client.verifySizeSpec()
        substrate = ''
        idx = len(client)
        if hasattr(client, 'getDefaultComponentByPosition'):
            comps = []
            while idx > 0:
                idx = idx - 1
                if client[idx] is None:
                    continue
                if client.getDefaultComponentByPosition(idx) == client[idx]:
                    continue
                comps.append(client[idx])

            comps.sort(self._cmpSetComponents)
            for c in comps:
                substrate = substrate + encodeFun(c, defMode, maxChunkSize)

        else:
            compSubs = []
            while idx > 0:
                idx = idx - 1
                compSubs.append(encodeFun(client[idx], defMode, maxChunkSize))

            compSubs.sort()
            substrate = string.join(compSubs, '')
        return (substrate, 1)


codecMap = encoder.codecMap.copy()
codecMap.update({univ.Boolean.tagSet: BooleanEncoder(),
 univ.BitString.tagSet: BitStringEncoder(),
 univ.OctetString.tagSet: OctetStringEncoder(),
 univ.SetOf().tagSet: SetOfEncoder()})

class Encoder(encoder.Encoder):

    def __call__(self, client, defMode = 0, maxChunkSize = 0):
        return encoder.Encoder.__call__(self, client, defMode, maxChunkSize)


encode = Encoder(codecMap)
