#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib\pyasn1\codec\ber/decoder.o
import types
from pyasn1.type import tag, univ, char, useful
from pyasn1.codec.ber import eoo
from pyasn1 import error

class AbstractDecoder:
    protoComponent = None

    def _createComponent(self, tagSet, asn1Spec):
        if asn1Spec is None:
            return self.protoComponent.clone(tagSet=tagSet)
        else:
            return asn1Spec.clone()

    def valueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        raise error.PyAsn1Error('Decoder not implemented for %s' % tagSet)

    def indefLenValueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        raise error.PyAsn1Error('Indefinite length mode decoder not implemented for %s' % tagSet)


class EndOfOctetsDecoder(AbstractDecoder):

    def valueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        return (eoo.endOfOctets, substrate)


class IntegerDecoder(AbstractDecoder):
    protoComponent = univ.Integer(0)

    def _valueFilter(self, value):
        try:
            return int(value)
        except OverflowError:
            return value

    def valueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        if not substrate:
            raise error.PyAsn1Error('Empty substrate')
        octets = map(ord, substrate)
        if octets[0] & 128:
            value = -1L
        else:
            value = 0L
        for octet in octets:
            value = value << 8 | octet

        value = self._valueFilter(value)
        return (self._createComponent(tagSet, asn1Spec).clone(value), substrate)


class BooleanDecoder(IntegerDecoder):
    protoComponent = univ.Boolean(0)

    def _valueFilter(self, value):
        if value:
            return 1
        else:
            return 0


class BitStringDecoder(AbstractDecoder):
    protoComponent = univ.BitString(())

    def valueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        r = self._createComponent(tagSet, asn1Spec)
        if tagSet[0][1] == tag.tagFormatSimple:
            if not substrate:
                raise error.PyAsn1Error('Missing initial octet')
            trailingBits = ord(substrate[0])
            if trailingBits > 7:
                raise error.PyAsn1Error('Trailing bits overflow %s' % trailingBits)
            substrate = substrate[1:]
            lsb = p = 0
            l = len(substrate) - 1
            b = []
            while p <= l:
                if p == l:
                    lsb = trailingBits
                j = 7
                o = ord(substrate[p])
                while j >= lsb:
                    b.append(o >> j & 1)
                    j = j - 1

                p = p + 1

            return (r.clone(tuple(b)), '')
        if r:
            r = r.clone(value=())
        if not decodeFun:
            return (r, substrate)
        while substrate:
            component, substrate = decodeFun(substrate)
            r = r + component

        return (r, substrate)

    def indefLenValueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        r = self._createComponent(tagSet, asn1Spec)
        if r:
            r = r.clone(value='')
        if not decodeFun:
            return (r, substrate)
        while substrate:
            component, substrate = decodeFun(substrate)
            if component == eoo.endOfOctets:
                break
            r = r + component
        else:
            raise error.SubstrateUnderrunError('No EOO seen before substrate ends')

        return (r, substrate)


class OctetStringDecoder(AbstractDecoder):
    protoComponent = univ.OctetString('')

    def valueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        r = self._createComponent(tagSet, asn1Spec)
        if tagSet[0][1] == tag.tagFormatSimple:
            return (r.clone(str(substrate)), '')
        if r:
            r = r.clone(value='')
        if not decodeFun:
            return (r, substrate)
        while substrate:
            component, substrate = decodeFun(substrate)
            r = r + component

        return (r, substrate)

    def indefLenValueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        r = self._createComponent(tagSet, asn1Spec)
        if r:
            r = r.clone(value='')
        if not decodeFun:
            return (r, substrate)
        while substrate:
            component, substrate = decodeFun(substrate)
            if component == eoo.endOfOctets:
                break
            r = r + component
        else:
            raise error.SubstrateUnderrunError('No EOO seen before substrate ends')

        return (r, substrate)


class NullDecoder(AbstractDecoder):
    protoComponent = univ.Null('')

    def valueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        r = self._createComponent(tagSet, asn1Spec)
        if substrate:
            raise error.PyAsn1Error('Unexpected substrate for Null')
        return (r, substrate)


class ObjectIdentifierDecoder(AbstractDecoder):
    protoComponent = univ.ObjectIdentifier(())

    def valueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        r = self._createComponent(tagSet, asn1Spec)
        if not substrate:
            raise error.PyAsn1Error('Empty substrate')
        oid = []
        index = 0
        subId = ord(substrate[index])
        oid.append(int(subId / 40))
        oid.append(int(subId % 40))
        index = index + 1
        substrateLen = len(substrate)
        while index < substrateLen:
            subId = ord(substrate[index])
            if subId < 128:
                oid.append(subId)
                index = index + 1
            else:
                nextSubId = subId
                subId = 0
                while nextSubId >= 128 and index < substrateLen:
                    subId = (subId << 7) + (nextSubId & 127)
                    index = index + 1
                    nextSubId = ord(substrate[index])

                if index == substrateLen:
                    raise error.SubstrateUnderrunError('Short substrate for OID %s' % oid)
                subId = (subId << 7) + nextSubId
                oid.append(subId)
                index = index + 1

        return (r.clone(tuple(oid)), substrate[index:])


class SequenceDecoder(AbstractDecoder):
    protoComponent = univ.Sequence()

    def _getAsn1SpecByPosition(self, t, idx):
        if t.getComponentType() is not None:
            if hasattr(t, 'getComponentTypeMapNearPosition'):
                return t.getComponentTypeMapNearPosition(idx)
            if hasattr(t, 'getComponentType'):
                return t.getComponentType()

    def _getPositionByType(self, t, c, idx):
        if t.getComponentType() is not None:
            if hasattr(t, 'getComponentPositionNearType'):
                effectiveTagSet = getattr(c, 'getEffectiveTagSet', c.getTagSet)()
                return t.getComponentPositionNearType(effectiveTagSet, idx)
        return idx

    def valueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        r = self._createComponent(tagSet, asn1Spec)
        idx = 0
        if not decodeFun:
            return (r, substrate)
        while substrate:
            asn1Spec = self._getAsn1SpecByPosition(r, idx)
            component, substrate = decodeFun(substrate, asn1Spec)
            idx = self._getPositionByType(r, component, idx)
            r.setComponentByPosition(idx, component)
            idx = idx + 1

        if hasattr(r, 'setDefaultComponents'):
            r.setDefaultComponents()
        r.verifySizeSpec()
        return (r, substrate)

    def indefLenValueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        r = self._createComponent(tagSet, asn1Spec)
        idx = 0
        while substrate:
            try:
                asn1Spec = self._getAsn1SpecByPosition(r, idx)
            except error.PyAsn1Error:
                asn1Spec = None

            if not decodeFun:
                return (r, substrate)
            component, substrate = decodeFun(substrate, asn1Spec)
            if component == eoo.endOfOctets:
                break
            idx = self._getPositionByType(r, component, idx)
            r.setComponentByPosition(idx, component)
            idx = idx + 1
        else:
            raise error.SubstrateUnderrunError('No EOO seen before substrate ends')

        if hasattr(r, 'setDefaultComponents'):
            r.setDefaultComponents()
        r.verifySizeSpec()
        return (r, substrate)


class SetDecoder(SequenceDecoder):
    protoComponent = univ.Set()

    def _getAsn1SpecByPosition(self, t, idx):
        if t.getComponentType() is not None:
            if hasattr(t, 'getComponentTypeMap'):
                return t.getComponentTypeMap()

    def _getPositionByType(self, t, c, idx):
        if t.getComponentType() is not None:
            if hasattr(t, 'getComponentPositionByType') and t.getComponentType():
                effectiveTagSet = getattr(c, 'getEffectiveTagSet', c.getTagSet)()
                return t.getComponentPositionByType(effectiveTagSet)
        return idx


class ChoiceDecoder(AbstractDecoder):
    protoComponent = univ.Choice()

    def valueDecoder(self, substrate, asn1Spec, tagSet, length, state, decodeFun):
        r = self._createComponent(tagSet, asn1Spec)
        if not decodeFun:
            return (r, substrate)
        if r.getTagSet() == tagSet:
            component, substrate = decodeFun(substrate, r.getComponentTypeMap())
        else:
            component, substrate = decodeFun(substrate, r.getComponentTypeMap(), tagSet, length, state)
        effectiveTagSet = getattr(component, 'getEffectiveTagSet', component.getTagSet)()
        r.setComponentByType(effectiveTagSet, component)
        return (r, substrate)

    indefLenValueDecoder = valueDecoder


class UTF8StringDecoder(OctetStringDecoder):
    protoComponent = char.UTF8String()


class NumericStringDecoder(OctetStringDecoder):
    protoComponent = char.NumericString()


class PrintableStringDecoder(OctetStringDecoder):
    protoComponent = char.PrintableString()


class TeletexStringDecoder(OctetStringDecoder):
    protoComponent = char.TeletexString()


class VideotexStringDecoder(OctetStringDecoder):
    protoComponent = char.VideotexString()


class IA5StringDecoder(OctetStringDecoder):
    protoComponent = char.IA5String()


class GraphicStringDecoder(OctetStringDecoder):
    protoComponent = char.GraphicString()


class VisibleStringDecoder(OctetStringDecoder):
    protoComponent = char.VisibleString()


class GeneralStringDecoder(OctetStringDecoder):
    protoComponent = char.GeneralString()


class UniversalStringDecoder(OctetStringDecoder):
    protoComponent = char.UniversalString()


class BMPStringDecoder(OctetStringDecoder):
    protoComponent = char.BMPString()


class GeneralizedTimeDecoder(OctetStringDecoder):
    protoComponent = useful.GeneralizedTime()


class UTCTimeDecoder(OctetStringDecoder):
    protoComponent = useful.UTCTime()


codecMap = {eoo.endOfOctets.tagSet: EndOfOctetsDecoder(),
 univ.Integer.tagSet: IntegerDecoder(),
 univ.Boolean.tagSet: BooleanDecoder(),
 univ.BitString.tagSet: BitStringDecoder(),
 univ.OctetString.tagSet: OctetStringDecoder(),
 univ.Null.tagSet: NullDecoder(),
 univ.ObjectIdentifier.tagSet: ObjectIdentifierDecoder(),
 univ.Enumerated.tagSet: IntegerDecoder(),
 univ.Sequence.tagSet: SequenceDecoder(),
 univ.Set.tagSet: SetDecoder(),
 univ.Choice.tagSet: ChoiceDecoder(),
 char.UTF8String.tagSet: UTF8StringDecoder(),
 char.NumericString.tagSet: NumericStringDecoder(),
 char.PrintableString.tagSet: PrintableStringDecoder(),
 char.TeletexString.tagSet: TeletexStringDecoder(),
 char.VideotexString.tagSet: VideotexStringDecoder(),
 char.IA5String.tagSet: IA5StringDecoder(),
 char.GraphicString.tagSet: GraphicStringDecoder(),
 char.VisibleString.tagSet: VisibleStringDecoder(),
 char.GeneralString.tagSet: GeneralStringDecoder(),
 char.UniversalString.tagSet: UniversalStringDecoder(),
 char.BMPString.tagSet: BMPStringDecoder(),
 useful.GeneralizedTime.tagSet: GeneralizedTimeDecoder(),
 useful.UTCTime.tagSet: UTCTimeDecoder()}
stDecodeTag, stDecodeLength, stGetValueDecoder, stGetValueDecoderByAsn1Spec, stGetValueDecoderByTag, stTryAsExplicitTag, stDecodeValue, stDumpRawValue, stErrorCondition, stStop = range(10)

class Decoder:
    defaultErrorState = stErrorCondition
    defaultRawDecoder = OctetStringDecoder()

    def __init__(self, codecMap):
        self.__codecMap = codecMap

    def __call__(self, substrate, asn1Spec = None, tagSet = None, length = None, state = stDecodeTag, recursiveFlag = 1):
        while state != stStop:
            if state == stDecodeTag:
                if not substrate:
                    raise error.SubstrateUnderrunError('Short octet stream on tag decoding')
                t = ord(substrate[0])
                tagClass = t & 192
                tagFormat = t & 32
                tagId = t & 31
                substrate = substrate[1:]
                if tagId == 31:
                    tagId = 0L
                    while 1:
                        if not substrate:
                            raise error.SubstrateUnderrunError('Short octet stream on long tag decoding')
                        t = ord(substrate[0])
                        tagId = tagId << 7 | t & 127
                        substrate = substrate[1:]
                        if not t & 128:
                            break

                lastTag = tag.Tag(tagClass=tagClass, tagFormat=tagFormat, tagId=tagId)
                if tagSet is None:
                    tagSet = tag.TagSet((), lastTag)
                else:
                    tagSet = lastTag + tagSet
                state = stDecodeLength
            if state == stDecodeLength:
                if not substrate:
                    raise error.SubstrateUnderrunError('Short octet stream on length decoding')
                firstOctet = ord(substrate[0])
                if firstOctet == 128:
                    size = 1
                    length = -1
                elif firstOctet < 128:
                    length, size = firstOctet, 1
                else:
                    size = firstOctet & 127
                    length = 0
                    lengthString = substrate[1:size + 1]
                    if len(lengthString) != size:
                        raise error.SubstrateUnderrunError('%s<%s at %s' % (size, len(lengthString), tagSet))
                    for char in lengthString:
                        length = length << 8 | ord(char)

                    size = size + 1
                state = stGetValueDecoder
                substrate = substrate[size:]
                if length != -1 and len(substrate) < length:
                    raise error.SubstrateUnderrunError('%d-octet short' % (length - len(substrate)))
            if state == stGetValueDecoder:
                if asn1Spec is None:
                    state = stGetValueDecoderByTag
                else:
                    state = stGetValueDecoderByAsn1Spec
            if state == stGetValueDecoderByTag:
                concreteDecoder = self.__codecMap.get(tagSet)
                if concreteDecoder:
                    state = stDecodeValue
                else:
                    concreteDecoder = self.__codecMap.get(tagSet[:1])
                    if concreteDecoder:
                        state = stDecodeValue
                    else:
                        state = stTryAsExplicitTag
            if state == stGetValueDecoderByAsn1Spec:
                if tagSet == eoo.endOfOctets.getTagSet():
                    concreteDecoder = self.__codecMap[tagSet]
                    state = stDecodeValue
                    continue
                if type(asn1Spec) == types.DictType:
                    __chosenSpec = asn1Spec.get(tagSet)
                elif asn1Spec is not None:
                    __chosenSpec = asn1Spec
                else:
                    __chosenSpec = None
                if __chosenSpec is None or not __chosenSpec.getTypeMap().has_key(tagSet):
                    state = stTryAsExplicitTag
                else:
                    baseTag = __chosenSpec.getTagSet().getBaseTag()
                    if baseTag:
                        baseTagSet = tag.TagSet(baseTag, baseTag)
                    else:
                        baseTagSet = tag.TagSet()
                    concreteDecoder = self.__codecMap.get(baseTagSet)
                    if concreteDecoder:
                        asn1Spec = __chosenSpec
                        state = stDecodeValue
                    else:
                        state = stTryAsExplicitTag
            if state == stTryAsExplicitTag:
                if tagSet and tagSet[0][1] == tag.tagFormatConstructed and tagSet[0][0] != tag.tagClassUniversal:
                    state = stDecodeTag
                else:
                    state = self.defaultErrorState
            if state == stDecodeValue:
                if recursiveFlag:
                    decodeFun = self
                else:
                    decodeFun = None
                if length == -1:
                    value, substrate = concreteDecoder.indefLenValueDecoder(substrate, asn1Spec, tagSet, length, stGetValueDecoder, decodeFun)
                else:
                    value, _substrate = concreteDecoder.valueDecoder(substrate[:length], asn1Spec, tagSet, length, stGetValueDecoder, decodeFun)
                    if recursiveFlag:
                        substrate = substrate[length:]
                    else:
                        substrate = _substrate
                state = stStop
            if state == stDumpRawValue:
                concreteDecoder = self.defaultRawDecoder
                state = stDecodeValue
            if state == stErrorCondition:
                raise error.PyAsn1Error('%s not in asn1Spec: %s' % (tagSet, asn1Spec))

        return (value, substrate)


decode = Decoder(codecMap)
