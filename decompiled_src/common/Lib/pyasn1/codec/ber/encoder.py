#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\pyasn1\codec\ber/encoder.o
import string
from pyasn1.type import base, tag, univ, char, useful
from pyasn1.codec.ber import eoo
from pyasn1 import error

class Error(Exception):
    pass


class AbstractItemEncoder:
    supportIndefLenMode = 1

    def _encodeTag(self, t, isConstructed):
        v = t[0] | t[1]
        if isConstructed:
            v = v | tag.tagFormatConstructed
        if t[2] < 31:
            return chr(v | t[2])
        else:
            longTag = t[2]
            s = chr(longTag & 127)
            longTag = longTag >> 7
            while longTag:
                s = chr(128 | longTag & 127) + s
                longTag = longTag >> 7

            return chr(v | 31) + s

    def _encodeLength(self, length, defMode):
        if not defMode and self.supportIndefLenMode:
            return '€'
        elif length < 128:
            return chr(length)
        else:
            substrate = ''
            while length:
                substrate = chr(length & 255) + substrate
                length = length >> 8

            if len(substrate) > 126:
                raise Error('Length octets overflow (%d)' % len(substrate))
            return chr(128 | len(substrate)) + substrate

    def _encodeValue(self, encodeFun, value, defMode, maxChunkSize):
        raise Error('Not implemented')

    def _encodeEndOfOctets(self, encodeFun, defMode):
        if defMode or not self.supportIndefLenMode:
            return ''
        else:
            return encodeFun(eoo.endOfOctets, defMode)

    def encode(self, encodeFun, value, defMode, maxChunkSize):
        substrate, isConstructed = self._encodeValue(encodeFun, value, defMode, maxChunkSize)
        tagSet = value.getTagSet()
        if tagSet:
            if not isConstructed:
                defMode = 1
            return self._encodeTag(tagSet[-1], isConstructed) + self._encodeLength(len(substrate), defMode) + substrate + self._encodeEndOfOctets(encodeFun, defMode)
        else:
            return substrate


class EndOfOctetsEncoder(AbstractItemEncoder):

    def _encodeValue(self, encodeFun, value, defMode, maxChunkSize):
        return ('', 0)


class ExplicitlyTaggedItemEncoder(AbstractItemEncoder):

    def _encodeValue(self, encodeFun, value, defMode, maxChunkSize):
        if isinstance(value, base.AbstractConstructedAsn1Item):
            value = value.clone(tagSet=value.getTagSet()[:-1], cloneValueFlag=1)
        else:
            value = value.clone(tagSet=value.getTagSet()[:-1])
        return (encodeFun(value, defMode, maxChunkSize), 1)


explicitlyTaggedItemEncoder = ExplicitlyTaggedItemEncoder()

class IntegerEncoder(AbstractItemEncoder):
    supportIndefLenMode = 0

    def _encodeValue(self, encodeFun, value, defMode, maxChunkSize):
        octets = []
        value = long(value)
        while 1:
            octets.insert(0, value & 255)
            if value == 0 or value == -1:
                break
            value = value >> 8

        if value == 0 and octets[0] & 128:
            octets.insert(0, 0)
        while len(octets) > 1 and (octets[0] == 0 and octets[1] & 128 == 0 or octets[0] == 255 and octets[1] & 128 != 0):
            del octets[0]

        return (string.join(map(chr, octets), ''), 0)


class BitStringEncoder(AbstractItemEncoder):

    def _encodeValue(self, encodeFun, value, defMode, maxChunkSize):
        if not maxChunkSize or len(value) <= maxChunkSize * 8:
            r = {}
            l = len(value)
            p = 0
            j = 7
            while p < l:
                i, j = divmod(p, 8)
                r[i] = r.get(i, 0) | value[p] << 7 - j
                p = p + 1

            keys = r.keys()
            keys.sort()
            return (chr(7 - j) + string.join(map(lambda k, r = r: chr(r[k]), keys), ''), 0)
        else:
            pos = 0
            substrate = ''
            while 1:
                v = value.clone(value[pos * 8:pos * 8 + maxChunkSize * 8])
                if not v:
                    break
                substrate = substrate + encodeFun(v, defMode, maxChunkSize)
                pos = pos + maxChunkSize

            return (substrate, 1)


class OctetStringEncoder(AbstractItemEncoder):

    def _encodeValue(self, encodeFun, value, defMode, maxChunkSize):
        if not maxChunkSize or len(value) <= maxChunkSize:
            return (str(value), 0)
        else:
            pos = 0
            substrate = ''
            while 1:
                v = value.clone(value[pos:pos + maxChunkSize])
                if not v:
                    break
                substrate = substrate + encodeFun(v, defMode, maxChunkSize)
                pos = pos + maxChunkSize

            return (substrate, 1)


class NullEncoder(AbstractItemEncoder):
    supportIndefLenMode = 0

    def _encodeValue(self, encodeFun, value, defMode, maxChunkSize):
        return ('', 0)


class ObjectIdentifierEncoder(AbstractItemEncoder):
    supportIndefLenMode = 0

    def _encodeValue(self, encodeFun, value, defMode, maxChunkSize):
        oid = tuple(value)
        if len(oid) < 2:
            raise error.PyAsn1Error('Short OID %s' % value)
        index = 0
        subid = oid[index] * 40
        subid = subid + oid[index + 1]
        if 0 > subid > 255:
            raise error.PyAsn1Error('Initial sub-ID overflow %s in OID %s' % (oid[index:], value))
        octets = [chr(subid)]
        index = index + 2
        for subid in oid[index:]:
            if subid > -1 and subid < 128:
                octets.append(chr(subid & 127))
            elif subid < 0 or subid > 4294967295L:
                raise error.PyAsn1Error('SubId overflow %s in %s' % (subid, value))
            else:
                res = [chr(subid & 127)]
                subid = subid >> 7
                while subid > 0:
                    res.insert(0, chr(128 | subid & 127))
                    subid = subid >> 7

                octets.append(string.join(res, ''))

        return (string.join(octets, ''), 0)


class SequenceOfEncoder(AbstractItemEncoder):

    def _encodeValue(self, encodeFun, value, defMode, maxChunkSize):
        if hasattr(value, 'setDefaultComponents'):
            value.setDefaultComponents()
        value.verifySizeSpec()
        substrate = ''
        idx = len(value)
        while idx > 0:
            idx = idx - 1
            if value[idx] is None:
                continue
            if hasattr(value, 'getDefaultComponentByPosition'):
                if value.getDefaultComponentByPosition(idx) == value[idx]:
                    continue
            substrate = encodeFun(value[idx], defMode, maxChunkSize) + substrate

        return (substrate, 1)


codecMap = {eoo.endOfOctets.tagSet: EndOfOctetsEncoder(),
 univ.Boolean.tagSet: IntegerEncoder(),
 univ.Integer.tagSet: IntegerEncoder(),
 univ.BitString.tagSet: BitStringEncoder(),
 univ.OctetString.tagSet: OctetStringEncoder(),
 univ.Null.tagSet: NullEncoder(),
 univ.ObjectIdentifier.tagSet: ObjectIdentifierEncoder(),
 univ.Enumerated.tagSet: IntegerEncoder(),
 univ.SequenceOf.tagSet: SequenceOfEncoder(),
 univ.SetOf.tagSet: SequenceOfEncoder(),
 univ.Choice.tagSet: SequenceOfEncoder(),
 char.UTF8String.tagSet: OctetStringEncoder(),
 char.NumericString.tagSet: OctetStringEncoder(),
 char.PrintableString.tagSet: OctetStringEncoder(),
 char.TeletexString.tagSet: OctetStringEncoder(),
 char.VideotexString.tagSet: OctetStringEncoder(),
 char.IA5String.tagSet: OctetStringEncoder(),
 char.GraphicString.tagSet: OctetStringEncoder(),
 char.VisibleString.tagSet: OctetStringEncoder(),
 char.GeneralString.tagSet: OctetStringEncoder(),
 char.UniversalString.tagSet: OctetStringEncoder(),
 char.BMPString.tagSet: OctetStringEncoder(),
 useful.GeneralizedTime.tagSet: OctetStringEncoder(),
 useful.UTCTime.tagSet: OctetStringEncoder()}

class Encoder:

    def __init__(self, _codecMap):
        self.__codecMap = _codecMap
        self.__emptyTagSet = tag.TagSet()

    def __call__(self, value, defMode = 1, maxChunkSize = 0):
        tagSet = value.getTagSet()
        if len(tagSet) > 1:
            concreteEncoder = explicitlyTaggedItemEncoder
        else:
            concreteEncoder = self.__codecMap.get(tagSet)
            if not concreteEncoder:
                baseTagSet = tagSet.getBaseTag()
                if baseTagSet:
                    concreteEncoder = self.__codecMap.get(tag.TagSet(baseTagSet, baseTagSet))
                else:
                    concreteEncoder = self.__codecMap.get(self.__emptyTagSet)
        if concreteEncoder:
            return concreteEncoder.encode(self, value, defMode, maxChunkSize)
        raise Error('No encoder for %s' % value)


encode = Encoder(codecMap)
